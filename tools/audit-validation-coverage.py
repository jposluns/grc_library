#!/usr/bin/env python3
"""audit-validation-coverage.py: cross-repo advisory audit answering "did every
recent commit that landed on a repository the orchestrator writes to carry a
PASSING validating CI run, or did an unvalidated change land (a red run, or a
landing with no validating run recorded)?"

Built after the 2026-07-24 failure: the orchestrator direct-pushed to
grc_library_private with no PR and no CI-watch, so its validate.py CI was red all day
unnoticed. The whole-project deep-assessment examines artefacts and gates, not the
assistant's OPERATION LOG, so a class of unvalidated-operation is invisible to it by
construction; this tool is that missing coverage check.

Signal (E9 Option C, maintainer-decided 2026-09-04). The PRIMARY signal is the
CI-RUN-STATUS PROBE: for each recent origin/main commit, `gh api
repos/<o>/<r>/actions/runs?head_sha=<sha>` (the PAT has Actions:Read; branch
protection reads 403, and gh pr checks / commits-status are not usable) is
correlated to the repo's detected validating workflow by run path. A landed
commit with a successful validating run is OK regardless of HOW it landed (PR
or direct-push) and WHO made it; a landed commit with a red validating run, or
with no validating run recorded, is the real risk this tool exists to catch: an
UNVALIDATED landing live on main (the 2026-07-24 signature). Landing mode
(PR vs direct via the commits/<sha>/pulls endpoint) and assistant attribution
(the co-author trailer) are retained as ANNOTATION only: the maintainer-vs-
assistant and PR-vs-direct axes were the wrong control for the operational
store, where both parties legitimately direct-push (the prior primary signal
produced a false "25/25 direct-push" finding there).

Policy per repo:
  pr-required  label only (annotation flavour): every landing is expected
               through a PR, and direct-pushes are annotated, but the verdict
               keys on CI-run status alone.
               (grc_library, grc_library_ref, grc_library_private)
  exchange     the non-authoritative worker channel: direct-pushes are the
               intended mechanism (annotated, never a finding) and a NO-RUN
               landing is a note, not a finding (the channel does not guarantee
               per-landing CI and the pre-push validate is not observable);
               an observed RED validating run is still a finding.
               (grc_library_scratch)

Limitations (also surfaced in the run summary): (1) only the last N commits per
repo are probed (fetch-first keeps origin/main current), so an unvalidated
landing OLDER than the window is not checked. (2) a NO-RUN result on a commit
older than the Actions retention window (~90 days, RETENTION_DAYS) may mean the
run record is absent for age-related reasons rather than that CI never ran; such
commits are counted separately (none_old) as a maintainer-verify note, never a
finding. (3) a commit predating the introduction (or rename) of the validating
workflow file reads as no-run; within the retention window that is a false
positive to triage by sha (the finding lists them). (4) if gh can read the CI
status of NO sampled commit, or nothing could be sampled at all, the verdict is
UNVERIFIABLE and counted under --strict, never OK: cannot-see is not gated.
(5) the probe requires the validating workflow to trigger on push to main; a
pull_request-only workflow would read every merge commit as no-run (verified
present for grc_library quality.yml and grc_library_ref/grc_library_private
validate.yml). (6) ~2 gh API calls per commit (~200 per default run): negligible
against the authenticated rate limit, but a rate-limited run degrades to
unknown / UNVERIFIABLE, never to OK.

Advisory: exits 0 by default (prints findings); --strict exits 1 on any FINDING or
UNVERIFIABLE verdict, for deep-assessment or CI use. Stdlib-only; shells out to git and
gh. Cross-repo: a repo or gh being absent degrades to a clearly-labelled SKIP or
UNVERIFIABLE, never a crash.
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

# name -> policy. Paths are resolved as siblings of this repo's root at runtime.
REPO_POLICY = {
    "grc_library": "pr-required",
    "grc_library_ref": "pr-required",
    "grc_library_private": "pr-required",
    "grc_library_scratch": "exchange",
}

DEFAULT_WINDOW = 25

# GitHub Actions retention: run records for commits older than this may be absent
# for age-related reasons rather than because CI never ran, so a no-run result on
# an older commit is a maintainer-verify note, not a finding (see docstring).
RETENTION_DAYS = 90


def _run(cmd, cwd=None, timeout=30):
    """Run a command, return (rc, stdout, stderr); never raise."""
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        return 127, "", str(e)


def repo_root():
    """The grc_library root (parent of this tool's directory)."""
    return Path(__file__).resolve().parent.parent


def sibling_path(name):
    root = repo_root()
    if name == root.name:
        return root
    return root.parent / name


def owner_repo(repo_path):
    """Parse (owner, repo) from the origin remote URL, or (None, None)."""
    rc, out, _ = _run(["git", "-C", str(repo_path), "remote", "get-url", "origin"])
    if rc != 0:
        return None, None
    url = out.strip()
    m = re.search(r"[:/]([^/]+)/([^/]+?)(?:\.git)?$", url)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def has_validating_ci(repo_path):
    """(present, detail, names): a .github/workflows/*.yml that runs a validating
    step; `names` is the set of matching workflow filenames, used by
    ci_run_status to correlate a commit's Actions runs to the validating
    workflow (a run's `path` basename must be one of these)."""
    wf_dir = repo_path / ".github" / "workflows"
    if not wf_dir.is_dir():
        return False, "no .github/workflows", set()
    # Match a real VALIDATING invocation, not a bare word. Bare `check` / `lint`
    # false-match `actions/checkout` and prose ("run linters"), which made the CI
    # dimension effectively never fail; require a concrete validate/audit/lint/test
    # command token instead.
    validating = re.compile(
        r"run_all_audits|run-pr-time-checks|run-linter-regression|validate\.py|"
        r"pre-commit\s+run|\bpytest\b|\bruff\b|\bflake8\b|\beslint\b|"
        r"markdownlint|shellcheck|\blint-[\w-]+\.py", re.I)
    hits = []
    for wf in sorted(wf_dir.glob("*.yml")) + sorted(wf_dir.glob("*.yaml")):
        try:
            text = wf.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if validating.search(text):
            hits.append(wf.name)
    if hits:
        return True, ", ".join(hits), set(hits)
    return False, "no validating workflow found", set()


def recent_shas(repo_path, window):
    # Fetch first: the local checkout does NOT auto-sync, so origin/main would be
    # stale and the newest remote direct-pushes (the ones most likely to be an
    # incident) would be invisible. A fetch failure is non-fatal (offline / no
    # remote); the classification then runs against whatever origin/main is present.
    _run(["git", "-C", str(repo_path), "fetch", "origin", "main", "--quiet"],
         timeout=60)
    rc, out, _ = _run(
        ["git", "-C", str(repo_path), "log", "origin/main",
         f"-{window}", "--format=%H"])
    if rc != 0:
        # fall back to local main if origin/main is not present
        rc, out, _ = _run(
            ["git", "-C", str(repo_path), "log", "main",
             f"-{window}", "--format=%H"])
    if rc != 0:
        return None
    return [s for s in out.splitlines() if s.strip()]


# The assistant co-authors every commit it makes with this trailer; a maintainer
# web-upload or manual commit does not. All commits carry the maintainer's git AUTHOR
# identity, so the trailer, not the author, is what distinguishes an assistant-made
# commit from a maintainer-made one. Under E9 Option C this is ANNOTATION only.
_ASSISTANT_TRAILER = re.compile(r"co-authored-by:\s*claude|noreply@anthropic\.com", re.I)


def landing_mode(owner, repo, sha):
    """'pr', 'direct', or 'unknown' (gh error) for a commit's landing mode."""
    rc, out, err = _run(
        ["gh", "api", f"repos/{owner}/{repo}/commits/{sha}/pulls",
         "--jq", "[.[].number]"])
    if rc != 0:
        return "unknown"
    try:
        prs = json.loads(out.strip() or "[]")
    except json.JSONDecodeError:
        return "unknown"
    return "pr" if prs else "direct"


def commit_is_assistant(repo_path, sha):
    """True if the commit carries the assistant's co-author trailer."""
    rc, out, _ = _run(["git", "-C", str(repo_path), "log", "-1", "--format=%B", sha])
    return rc == 0 and bool(_ASSISTANT_TRAILER.search(out))


def commit_age_days(repo_path, sha, now=None):
    """Age of a commit in days from its committer timestamp, or None on error."""
    rc, out, _ = _run(["git", "-C", str(repo_path), "log", "-1", "--format=%ct", sha])
    out = out.strip()
    if rc != 0 or not out.isdigit():
        return None
    return ((now if now is not None else time.time()) - int(out)) / 86400.0


# Only LANDING-validation events attest that THIS landing passed CI. A schedule /
# workflow_dispatch run carries head_sha = main's HEAD when it fired but does not
# validate the landing at push time, so counting its green could MASK a red push
# run on the same sha (the 2026-07-24 incident class this tool exists to catch);
# such non-landing runs are excluded from the correlation.
_LANDING_EVENTS = {"push", "pull_request"}


def _wf_basename(path):
    """Final workflow filename from a run `path`, tolerating GitHub's documented
    `@ref` suffix (e.g. '.github/workflows/quality.yml@main' -> 'quality.yml')."""
    return (path or "").rsplit("/", 1)[-1].split("@", 1)[0]


def _reduce_ci_runs(runs, validating_names):
    """Pure reduction (self-tested): given the actions/runs list for one sha and
    the validating-workflow filename set, return 'success'|'failure'|'none'|
    'unknown'. Correlate a run to the validating workflow by path basename (the
    documented '@ref' suffix is stripped) AND restrict to landing events
    (_LANDING_EVENTS), so a green scheduled sweep on the same head_sha cannot
    mask a red push run. 'success' if ANY landing validating run concluded
    success (re-runs update in place, so a superseded red cannot outvote a
    green); else 'failure' if a landing validating run completed non-success;
    else 'unknown' if landing validating runs exist but none completed
    (in-flight); else 'none' (no landing validating run for the sha)."""
    validating = [r for r in runs
                  if _wf_basename(r.get("path")) in validating_names
                  and r.get("event") in _LANDING_EVENTS]
    if not validating:
        return "none"
    concluded = [r for r in validating if r.get("status") == "completed"]
    if any(r.get("conclusion") == "success" for r in concluded):
        return "success"
    if concluded:
        return "failure"
    return "unknown"  # validating run(s) exist but still queued / in progress


def ci_run_status(owner, repo, sha, validating_names):
    """CI-run status for a landed commit: 'success' | 'failure' | 'none' | 'unknown'.

    Queries `gh api repos/{o}/{r}/actions/runs?head_sha={sha}` (the PAT has
    Actions:Read; `gh pr checks` and the commits/status API are not usable) and
    correlates runs to the VALIDATING workflow by path basename (the documented
    `@ref` suffix stripped) restricted to landing events, then delegates to the
    pure _reduce_ci_runs (which carries the reduction + masking discipline). Reduction across multiple runs:
    the list endpoint reports each run at its LATEST attempt (a re-run updates
    the run in place), so a superseded failed attempt cannot mask a later green;
    'success' if ANY validating run for the sha concluded success (a later
    scheduled run going red on the same head sha does not un-validate the
    landing); else 'failure' if at least one validating run completed with a
    non-success conclusion (failure / timed_out / cancelled / startup_failure /
    action_required / stale / skipped / neutral -- none of them is a PASSED
    validation); else 'unknown' if validating runs exist but none has completed
    (in-flight CI, not yet decidable); 'none' if no run of a validating workflow
    exists for the sha (never triggered, or absent for age-related reasons: the
    caller age-splits this, see RETENTION_DAYS). 'unknown' also covers gh/API/
    parse errors: cannot-see is never mapped to a definite state."""
    rc, out, _ = _run(
        ["gh", "api",
         f"repos/{owner}/{repo}/actions/runs?head_sha={sha}&per_page=100",
         "--jq", "[.workflow_runs[] | {path, status, conclusion, event}]"])
    if rc != 0:
        return "unknown"
    try:
        runs = json.loads(out.strip() or "[]")
    except json.JSONDecodeError:
        return "unknown"
    return _reduce_ci_runs(runs, validating_names)


def verdict(policy, ci_counts, landing_counts, ci_present):
    """Pure verdict function (self-tested): map the observed signals to a verdict.

    PRIMARY SIGNAL (E9 Option C, maintainer-decided 2026-09-04): CI-RUN STATUS.
    A landed commit is fine if a successful validating CI run exists for it,
    regardless of how it landed (PR or direct-push) and who made it; a landed
    commit with a red validating run, or (on a pr-required repo) with NO
    validating run recorded within the retention window, is a FINDING: an
    unvalidated change is live on main. Landing mode and assistant attribution
    are ANNOTATION only (the maintainer-vs-assistant axis was the wrong control
    for the operational store, where both legitimately direct-push).

    ci_counts: success / failure / none_recent / none_old / unknown per sampled
    commit. none_old is a no-run result on a commit older than the Actions
    retention window: possibly aged out rather than never-run, so a
    maintainer-verify note, not a finding. A missing validating CI workflow is
    a finding for any policy. If NOTHING could be sampled, or gh could read the
    CI status of NO sampled commit, the verdict is UNVERIFIABLE, never OK:
    cannot-see is not gated. Exchange policy: direct-pushes are the intended
    mechanism and a no-run landing is a note (the channel does not guarantee
    per-landing CI), but an observed RED validating run is still a finding."""
    findings = []
    if not ci_present:
        findings.append("no validating CI workflow")
    if ci_present:
        if policy == "exchange":
            unvalidated = ci_counts["failure"]
        else:
            unvalidated = ci_counts["failure"] + ci_counts["none_recent"]
        if unvalidated:
            parts = [f"{ci_counts['failure']} with a red/non-success conclusion"]
            if policy != "exchange":
                parts.append(f"{ci_counts['none_recent']} with no validating "
                             "run recorded")
            findings.append(
                f"{unvalidated} landed commit(s) without a successful validating "
                f"CI run ({'; '.join(parts)}); an unvalidated change is live on "
                "main until remediated (the 2026-07-24 failure signature)")
    if findings:
        return "FINDING", findings
    sampled = sum(ci_counts.values())
    if sampled == 0:
        return "UNVERIFIABLE", [
            "no commit could be sampled (git log / remote-owner resolution "
            "failed, or probing was skipped); CI-run status is unknown, so an "
            "unvalidated landing cannot be ruled out. NOT treated as OK."]
    if ci_counts["unknown"] == sampled:
        return "UNVERIFIABLE", [
            f"gh could not read CI-run status for any of the {sampled} sampled "
            "commit(s) (auth / rate-limit / endpoint error); an unvalidated "
            "landing cannot be ruled out. NOT treated as OK."]
    notes = []
    status = "OK"
    if ci_counts["none_old"]:
        notes.append(
            f"{ci_counts['none_old']} commit(s) older than the ~{RETENTION_DAYS}-day "
            "Actions retention window have no retained validating run: possibly "
            "aged out rather than never-run; maintainer-verify if in doubt")
        status = "OK-PARTIAL"
    if ci_counts["unknown"]:
        notes.append(f"{ci_counts['unknown']} commit(s) CI-run status unknown "
                     "(gh error or run still in flight)")
        status = "OK-PARTIAL"
    if policy == "exchange" and ci_counts["none_recent"]:
        notes.append(
            f"{ci_counts['none_recent']} landing(s) with no validating run "
            "recorded: the exchange channel does not guarantee per-landing CI "
            "(the enqueue-order.sh pre-push validate is bypassable and not "
            "observable here); reported, not a finding")
    total_direct = (landing_counts["assistant_direct"]
                    + landing_counts["other_direct"])
    if policy == "exchange" and total_direct:
        notes.append(f"{total_direct} direct-push(es): the expected "
                     "exchange-channel mechanism")
        if status == "OK":
            status = "OK-EXCHANGE"
    elif total_direct:
        notes.append(
            f"annotation: {total_direct} direct-push landing(s) "
            f"({landing_counts['assistant_direct']} assistant-attributed, "
            f"{landing_counts['other_direct']} maintainer/other); NOT a finding "
            "under the CI-run-status policy (each is covered by the CI probe "
            "above); branch-protection enforcement remains maintainer-verify "
            "(token 403 on protection reads)")
    return status, notes


def audit_repo(name, window):
    path = sibling_path(name)
    policy = REPO_POLICY[name]
    if not (path / ".git").exists():
        return {"name": name, "policy": policy, "status": "SKIP",
                "notes": ["repository not present (portable clone / no sibling)"]}
    owner, repo = owner_repo(path)
    ci_present, ci_detail, ci_names = has_validating_ci(path)
    shas = recent_shas(path, window)

    ci_counts = {"success": 0, "failure": 0, "none_recent": 0, "none_old": 0,
                 "unknown": 0}
    landing_counts = {"pr": 0, "assistant_direct": 0, "other_direct": 0,
                      "unknown": 0}
    red_shas, norun_shas, assistant_direct_shas = [], [], []
    now = time.time()
    if shas is not None and owner:
        for sha in shas:
            # primary signal: did a validating CI run pass for this landing?
            if ci_present:
                st = ci_run_status(owner, repo, sha, ci_names)
                if st == "none":
                    age = commit_age_days(path, sha, now)
                    if age is not None and age > RETENTION_DAYS:
                        ci_counts["none_old"] += 1
                    else:
                        ci_counts["none_recent"] += 1
                        norun_shas.append(sha[:9])
                else:
                    ci_counts[st] += 1
                    if st == "failure":
                        red_shas.append(sha[:9])
            # annotation: landing mode + attribution (never a finding)
            mode = landing_mode(owner, repo, sha)
            if mode == "direct":
                if commit_is_assistant(path, sha):
                    landing_counts["assistant_direct"] += 1
                    assistant_direct_shas.append(sha[:9])
                else:
                    landing_counts["other_direct"] += 1
            elif mode == "pr":
                landing_counts["pr"] += 1
            else:
                landing_counts["unknown"] += 1
    elif shas and not owner and ci_present:
        # commits exist but the remote owner is unparseable: gh cannot be asked,
        # so every sampled commit's CI status is unknown (cannot-see != gated)
        ci_counts["unknown"] = len(shas)
        landing_counts["unknown"] = len(shas)

    v, notes = verdict(policy, ci_counts, landing_counts, ci_present)
    return {
        "name": name, "policy": policy, "status": v,
        "ci": (ci_present, ci_detail),
        "ci_runs": dict(ci_counts, red_shas=red_shas, norun_shas=norun_shas),
        "landings": dict(landing_counts,
                         assistant_direct_shas=assistant_direct_shas,
                         window=len(shas or [])),
        "notes": notes,
    }


def run(window):
    print("Validation-coverage audit (advisory; cross-repo). Anti-recurrence check "
          "for the 2026-07-24 direct-push-without-validation failure.")
    print("PRIMARY SIGNAL (E9 Option C): CI-run status per landed commit via "
          "actions/runs?head_sha (Actions:Read). A landing with a successful "
          "validating run is OK however it landed; landing mode and attribution "
          "are annotation. Branch-protection enforcement remains MAINTAINER-VERIFY "
          "(token 403 on protection reads).\n")
    results = [audit_repo(n, window) for n in REPO_POLICY]
    findings = 0
    for r in results:
        line = f"[{r['status']:12}] {r['name']}  (policy {r['policy']})"
        if r["status"] == "SKIP":
            print(line + " -- " + "; ".join(r["notes"]))
            continue
        ci_present, ci_detail = r["ci"]
        cr, lg = r["ci_runs"], r["landings"]
        print(line)
        print(f"    validating CI: {'yes (' + ci_detail + ')' if ci_present else 'NO -- ' + ci_detail}")
        print(f"    CI-run status over last {lg['window']}: {cr['success']} passed, "
              f"{cr['failure']} red, {cr['none_recent']} no-run, "
              f"{cr['none_old']} no-run(>{RETENTION_DAYS}d), {cr['unknown']} unknown"
              + (f"  red: {', '.join(cr['red_shas'])}" if cr['red_shas'] else "")
              + (f"  no-run: {', '.join(cr['norun_shas'])}" if cr['norun_shas'] else ""))
        print(f"    landing modes (annotation): {lg['pr']} PR, "
              f"{lg['assistant_direct']} assistant-direct, "
              f"{lg['other_direct']} maintainer/other-direct, {lg['unknown']} unknown"
              + (f"  assistant-direct: {', '.join(lg['assistant_direct_shas'])}"
                 if lg['assistant_direct_shas'] else ""))
        for n in r["notes"]:
            print(f"    - {n}")
        if r["status"] in ("FINDING", "UNVERIFIABLE"):
            findings += 1
    print(f"\nSummary: {findings} repo(s) with a FINDING or UNVERIFIABLE verdict. "
          f"Coverage bounds: only the last {window} commits per repo were probed; "
          f"a no-run result on a commit older than ~{RETENTION_DAYS} days may be an "
          "aged-out run record rather than a never-run (maintainer-verify); "
          "branch-protection enforcement (require-PR, block-force-push) remains "
          "maintainer-verify (the assistant token 403s on protection reads).")
    return findings


# --- self-test: the pure verdict logic (git/gh integration is not fixturable) ------
def _self_test():
    import tempfile
    import unittest

    # tally-building helpers keep the cases readable
    def _ci(success=0, failure=0, none_recent=0, none_old=0, unknown=0):
        return {"success": success, "failure": failure,
                "none_recent": none_recent, "none_old": none_old,
                "unknown": unknown}

    def _landing(pr=0, assistant_direct=0, other_direct=0, unknown=0):
        return {"pr": pr, "assistant_direct": assistant_direct,
                "other_direct": other_direct, "unknown": unknown}

    class VerdictTests(unittest.TestCase):
        # verdict signature: (policy, ci_counts, landing_counts, ci_present)

        def test_direct_push_with_passing_ci_is_ok(self):
            # THE REALITY CASE (E9 Option C): the operational store's commits are
            # all direct-pushed by the maintainer or the orchestrator, and all
            # carry a green validating run: OK with an annotation, NOT a finding
            # (the false "25/25 direct-push" result this change removes).
            v, notes = verdict("pr-required", _ci(success=25),
                               _landing(other_direct=20, assistant_direct=5), True)
            self.assertEqual(v, "OK")
            self.assertTrue(any("annotation" in n for n in notes))

        def test_pr_landed_with_red_ci_is_finding(self):
            # a PR landing does NOT excuse a red validating run: the primary
            # signal is CI status, not landing mode
            v, notes = verdict("pr-required", _ci(success=24, failure=1),
                               _landing(pr=25), True)
            self.assertEqual(v, "FINDING")
            self.assertTrue(any("red/non-success" in n for n in notes))

        def test_no_ci_run_recorded_recent_is_finding(self):
            v, notes = verdict("pr-required", _ci(success=24, none_recent=1),
                               _landing(pr=25), True)
            self.assertEqual(v, "FINDING")
            self.assertTrue(any("no validating run" in n for n in notes))

        def test_aged_out_none_is_note_not_finding(self):
            # retention residual: a no-run result on a commit older than the
            # retention window may be an aged-out run, not an unvalidated landing
            v, notes = verdict("pr-required", _ci(success=20, none_old=5),
                               _landing(pr=25), True)
            self.assertEqual(v, "OK-PARTIAL")
            self.assertTrue(any("retention" in n for n in notes))

        def test_missing_ci_is_finding_any_policy(self):
            self.assertEqual(
                verdict("pr-required", _ci(), _landing(pr=12), False)[0], "FINDING")
            self.assertEqual(
                verdict("exchange", _ci(), _landing(pr=12), False)[0], "FINDING")

        def test_all_unknown_is_unverifiable_not_ok(self):
            v, notes = verdict("pr-required", _ci(unknown=3), _landing(unknown=3),
                               True)
            self.assertEqual(v, "UNVERIFIABLE")
            self.assertTrue(any("NOT treated as OK" in n for n in notes))

        def test_nothing_sampled_is_unverifiable(self):
            # closes the pre-existing hole: owner unparseable / git log failed
            # used to fall through to OK with all-zero tallies
            v, notes = verdict("pr-required", _ci(), _landing(), True)
            self.assertEqual(v, "UNVERIFIABLE")
            self.assertTrue(any("NOT treated as OK" in n for n in notes))

        def test_partial_unknown_is_ok_partial(self):
            self.assertEqual(
                verdict("pr-required", _ci(success=10, unknown=3),
                        _landing(pr=10, unknown=3), True)[0], "OK-PARTIAL")

        def test_exchange_direct_push_with_green_ci_is_ok_exchange(self):
            v, notes = verdict("exchange", _ci(success=5),
                               _landing(assistant_direct=3, other_direct=2), True)
            self.assertEqual(v, "OK-EXCHANGE")
            self.assertTrue(any("expected" in n for n in notes))

        def test_exchange_no_run_is_note_not_finding(self):
            # the exchange channel does not guarantee per-landing CI: preserved
            v, notes = verdict("exchange", _ci(none_recent=5),
                               _landing(other_direct=5), True)
            self.assertEqual(v, "OK-EXCHANGE")
            self.assertTrue(any("not a finding" in n for n in notes))

        def test_exchange_red_run_is_finding(self):
            # an observed RED validating run is a finding on any policy
            self.assertEqual(
                verdict("exchange", _ci(success=4, failure=1),
                        _landing(other_direct=5), True)[0], "FINDING")

        def test_exchange_failure_message_excludes_none_recent(self):
            # codex defect 2: exchange counts only failure as unvalidated, so the
            # finding breakdown must NOT claim the none_recent no-runs as findings
            v, notes = verdict("exchange", _ci(failure=1, none_recent=5),
                               _landing(other_direct=6), True)
            self.assertEqual(v, "FINDING")
            fnote = next(n for n in notes if "without a successful" in n)
            self.assertIn("1 landed commit", fnote)
            self.assertNotIn("no validating run recorded", fnote)

        def test_mixed_none_old_and_unknown_is_ok_partial(self):
            v, notes = verdict("pr-required", _ci(success=10, none_old=2, unknown=3),
                               _landing(pr=15), True)
            self.assertEqual(v, "OK-PARTIAL")
            self.assertTrue(any("retention" in n for n in notes))
            self.assertTrue(any("unknown" in n for n in notes))

    class CiDetectionTests(unittest.TestCase):
        """has_validating_ci is fixturable (pure string + tempfile); this catches the
        actions/checkout false-positive that a bare `check` token would let through."""

        def _wf(self, content):
            d = Path(tempfile.mkdtemp())
            wfdir = d / ".github" / "workflows"
            wfdir.mkdir(parents=True)
            (wfdir / "ci.yml").write_text(content, encoding="utf-8")
            return d

        def test_checkout_only_is_not_validating(self):
            root = self._wf("jobs:\n  x:\n    steps:\n"
                            "      - uses: actions/checkout@v4\n      - run: ./deploy.sh\n")
            self.assertFalse(has_validating_ci(root)[0])

        def test_validate_py_is_validating(self):
            root = self._wf("jobs:\n  x:\n    steps:\n"
                            "      - run: python3 tools/validate.py\n")
            self.assertTrue(has_validating_ci(root)[0])

        def test_run_all_audits_is_validating(self):
            root = self._wf("jobs:\n  x:\n    steps:\n"
                            "      - run: tools/run_all_audits.sh\n")
            self.assertTrue(has_validating_ci(root)[0])

        def test_no_workflows_is_not_validating(self):
            self.assertFalse(has_validating_ci(Path(tempfile.mkdtemp()))[0])

    class ReduceCiRunsTests(unittest.TestCase):
        """_reduce_ci_runs is pure (list of run dicts in, verdict out); pins the
        landing-event filter (a green scheduled sweep must not mask a red push on
        the same head_sha) and the @ref path normalization codex flagged."""

        def _r(self, path, conclusion, event, status="completed"):
            return {"path": f".github/workflows/{path}", "status": status,
                    "conclusion": conclusion, "event": event}

        NAMES = {"quality.yml", "nightly-sweep.yml"}

        def test_scheduled_green_does_not_mask_push_red(self):
            runs = [self._r("quality.yml", "failure", "push"),
                    self._r("nightly-sweep.yml", "success", "schedule")]
            self.assertEqual(_reduce_ci_runs(runs, self.NAMES), "failure")

        def test_push_green_is_success(self):
            self.assertEqual(
                _reduce_ci_runs([self._r("quality.yml", "success", "push")],
                                self.NAMES), "success")

        def test_ref_suffix_path_is_normalized(self):
            # codex defect 1: GitHub's documented path may carry an @ref suffix
            self.assertEqual(
                _reduce_ci_runs([self._r("quality.yml@main", "success", "push")],
                                {"quality.yml"}), "success")

        def test_only_scheduled_run_is_none(self):
            self.assertEqual(
                _reduce_ci_runs([self._r("quality.yml", "success", "schedule")],
                                self.NAMES), "none")

        def test_inflight_push_is_unknown(self):
            self.assertEqual(
                _reduce_ci_runs([self._r("quality.yml", None, "push",
                                         status="in_progress")], self.NAMES),
                "unknown")

        def test_non_validating_workflow_is_none(self):
            self.assertEqual(
                _reduce_ci_runs([self._r("web-generator-health.yml", "success",
                                         "push")], self.NAMES), "none")

        def test_pull_request_event_counts(self):
            self.assertEqual(
                _reduce_ci_runs([self._r("quality.yml", "success",
                                         "pull_request")], self.NAMES), "success")

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(VerdictTests))
    suite.addTests(loader.loadTestsFromTestCase(CiDetectionTests))
    suite.addTests(loader.loadTestsFromTestCase(ReduceCiRunsTests))
    res = unittest.TextTestRunner(verbosity=1).run(suite)
    return 0 if res.wasSuccessful() else 1


def main():
    ap = argparse.ArgumentParser(description="Cross-repo validation-coverage audit.")
    ap.add_argument("--window", type=int, default=DEFAULT_WINDOW,
                    help=f"commits per repo to probe (default {DEFAULT_WINDOW})")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if any repo has a finding (for deep-assessment / CI)")
    ap.add_argument("--self-test", action="store_true", help="run unit tests and exit")
    args = ap.parse_args()
    if args.self_test:
        sys.exit(_self_test())
    findings = run(args.window)
    sys.exit(1 if (args.strict and findings) else 0)


if __name__ == "__main__":
    main()
