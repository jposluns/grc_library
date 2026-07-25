#!/usr/bin/env python3
"""audit-validation-coverage.py: cross-repo advisory audit answering "does every
repository the orchestrator writes to require changes to land through a VALIDATING
path (a PR that runs a validating CI check), or is there an ungated DIRECT-PUSH lane?"

Built after the 2026-07-24 failure: the orchestrator direct-pushed to
grc_library_private with no PR and no CI-watch, so its validate.py CI was red all day
unnoticed. The whole-project deep-assessment examines artefacts and gates, not the
assistant's OPERATION LOG, so a class of unvalidated-operation is invisible to it by
construction; this tool is that missing coverage check.

Signal. The assistant's gh token gets HTTP 403 on branch-protection READS, so this tool
cannot confirm the server-side enforcement (require-PR, block-force-push); that is
flagged maintainer-verify. What it CAN observe reliably is the LANDING MODE of recent
commits: `gh api repos/<owner>/<repo>/commits/<sha>/pulls` returns the PR a commit
landed through, or empty for a direct-push. A recent direct-push to a PR-required repo
is the ungated-landing signal (the exact _private failure signature). It also checks
that a validating CI workflow exists in each repo.

Policy per repo:
  pr-required  every landing must be a PR; a recent direct-push is a FINDING.
               (grc_library, grc_library_ref, grc_library_private)
  exchange     the non-authoritative worker channel; direct-pushes are the intended
               mechanism, so they are REPORTED but are not a finding. The tool does
               NOT confirm each was validated (the enqueue-order.sh pre-push validate
               is bypassable by a plain git push and is not observable from commit
               metadata). (grc_library_scratch)

Limitations (also surfaced in the run summary): (1) only the last N commits per repo
are classified (the tool fetches first, so origin/main is current), so an ungated
landing OLDER than the window is not checked. (2) if gh cannot classify any commit for
a repo (auth / rate-limit / 403), the verdict is UNVERIFIABLE and counted under
--strict, never OK: cannot-see is not gated. (3) the commit-to-PR endpoint returns any
PR a sha is associated with, so in the rare case a direct-pushed commit later appears
in a PR branch it could read as PR-landed; the fetch plus the recent-window make this
unlikely for a live incident.

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
from pathlib import Path

# name -> policy. Paths are resolved as siblings of this repo's root at runtime.
REPO_POLICY = {
    "grc_library": "pr-required",
    "grc_library_ref": "pr-required",
    "grc_library_private": "pr-required",
    "grc_library_scratch": "exchange",
}

DEFAULT_WINDOW = 25


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
    """(present, detail): a .github/workflows/*.yml that runs a validating step."""
    wf_dir = repo_path / ".github" / "workflows"
    if not wf_dir.is_dir():
        return False, "no .github/workflows"
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
        return True, ", ".join(hits)
    return False, "no validating workflow found"


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
# commit (the bypass class the failure is about) from a maintainer-made one (the
# repo-owner's own prerogative).
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


def verdict(policy, assistant_direct, other_direct, pr_count, unknown_count, ci_present):
    """Pure verdict function (self-tested): map the observed signals to a verdict.
    A missing validating CI is a finding for any repo. For a PR-required repo, ANY
    direct-push landing is a finding, because it means the PR requirement was not
    enforced for that commit and an unvalidated change CAN land. Attribution is an
    annotation, not the gate: an assistant-attributed direct-push (a Co-Authored-By
    trailer) is the definite bypass, but the assistant does not always add the
    trailer, so a direct-push without one is NOT assumed safe. If gh could classify
    NO commit for the repo (all unknown), the verdict is UNVERIFIABLE, not OK: a
    "cannot see" must never read as "gated". An exchange repo's direct-pushes are the
    intended mechanism (not a finding)."""
    findings = []
    if not ci_present:
        findings.append("no validating CI workflow")
    total_direct = assistant_direct + other_direct
    if policy == "pr-required" and total_direct > 0:
        findings.append(
            f"{total_direct} direct-push landing(s) on a PR-required repo "
            f"({assistant_direct} assistant-attributed, {other_direct} maintainer/other); "
            "the PR requirement was not enforced for these, confirm branch protection "
            "is now in place (token 403 cannot read it)")
    if findings:
        return "FINDING", findings
    # gh could not classify a single commit (auth / rate-limit / endpoint error):
    # cannot see is not OK, an ungated landing could hide behind the failure.
    if unknown_count > 0 and total_direct == 0 and pr_count == 0:
        return "UNVERIFIABLE", [
            f"gh could not classify any of the {unknown_count} sampled commit(s) "
            "(auth / rate-limit / endpoint error); landing mode is unknown, so an "
            "ungated landing cannot be ruled out. NOT treated as OK."]
    notes = []
    if policy == "exchange" and total_direct:
        notes.append(f"{total_direct} direct-push(es): the expected exchange-channel "
                     "mechanism. NOTE: the tool does not confirm each was validated "
                     "(the enqueue-order.sh pre-push validate is bypassable by a plain "
                     "git push and is not observable from commit metadata).")
        status = "OK-EXCHANGE"
    else:
        status = "OK"
    if unknown_count:
        notes.append(f"{unknown_count} commit(s) landing-mode unknown (gh error)")
        if status == "OK":
            status = "OK-PARTIAL"
    return status, notes


def audit_repo(name, window):
    path = sibling_path(name)
    policy = REPO_POLICY[name]
    if not (path / ".git").exists():
        return {"name": name, "policy": policy, "status": "SKIP",
                "notes": ["repository not present (portable clone / no sibling)"]}
    owner, repo = owner_repo(path)
    ci_present, ci_detail = has_validating_ci(path)
    shas = recent_shas(path, window)
    assistant_direct = other_direct = unknown = pr = 0
    assistant_direct_shas = []
    if shas is not None and owner:
        for sha in shas:
            mode = landing_mode(owner, repo, sha)
            if mode == "direct":
                if commit_is_assistant(path, sha):
                    assistant_direct += 1
                    assistant_direct_shas.append(sha[:9])
                else:
                    other_direct += 1
            elif mode == "pr":
                pr += 1
            else:
                unknown += 1
    v, notes = verdict(policy, assistant_direct, other_direct, pr, unknown, ci_present)
    return {
        "name": name, "policy": policy, "status": v,
        "ci": (ci_present, ci_detail),
        "landings": {"pr": pr, "assistant_direct": assistant_direct,
                     "other_direct": other_direct, "unknown": unknown,
                     "assistant_direct_shas": assistant_direct_shas,
                     "window": len(shas or [])},
        "notes": notes,
    }


def run(window):
    print("Validation-coverage audit (advisory; cross-repo). Anti-recurrence check "
          "for the 2026-07-24 direct-push-without-validation failure.")
    print("NOTE: the assistant token gets 403 on branch-protection reads, so "
          "require-PR / block-force-push enforcement is MAINTAINER-VERIFY, not "
          "confirmed here; this tool observes landing mode (PR vs direct-push) instead.\n")
    results = [audit_repo(n, window) for n in REPO_POLICY]
    findings = 0
    for r in results:
        line = f"[{r['status']:12}] {r['name']}  (policy {r['policy']})"
        if r["status"] == "SKIP":
            print(line + " -- " + "; ".join(r["notes"]))
            continue
        ci_present, ci_detail = r["ci"]
        lg = r["landings"]
        print(line)
        print(f"    validating CI: {'yes (' + ci_detail + ')' if ci_present else 'NO -- ' + ci_detail}")
        print(f"    last {lg['window']} main commits: {lg['pr']} PR-landed, "
              f"{lg['assistant_direct']} assistant-direct-push, "
              f"{lg['other_direct']} maintainer/other-direct-push, {lg['unknown']} unknown"
              + (f"  assistant-direct: {', '.join(lg['assistant_direct_shas'])}"
                 if lg['assistant_direct_shas'] else ""))
        for n in r["notes"]:
            print(f"    - {n}")
        if r["status"] in ("FINDING", "UNVERIFIABLE"):
            findings += 1
    print(f"\nSummary: {findings} repo(s) with a FINDING or UNVERIFIABLE verdict. "
          f"Coverage bound: only the last {window} commits per repo were classified, "
          "so an ungated landing OLDER than that window is not checked; and "
          "branch-protection enforcement (require-PR, block-force-push) remains "
          "maintainer-verify (the assistant token 403s on protection reads).")
    return findings


# --- self-test: the pure verdict logic (git/gh integration is not fixturable) ------
def _self_test():
    import tempfile
    import unittest

    # verdict signature: (policy, assistant_direct, other_direct, pr_count,
    #                     unknown_count, ci_present)
    class VerdictTests(unittest.TestCase):
        def test_pr_required_assistant_direct_is_finding(self):
            v, notes = verdict("pr-required", 2, 0, 5, 0, True)
            self.assertEqual(v, "FINDING")
            self.assertTrue(any("2 assistant-attributed" in n for n in notes))

        def test_pr_required_any_direct_is_finding_attribution_annotated(self):
            # any direct-push on a PR-required repo is a finding (the requirement was
            # not enforced); attribution is annotated, not the gate (the assistant does
            # not always add its trailer, so a non-attributed direct-push is not safe)
            v, notes = verdict("pr-required", 0, 2, 5, 0, True)
            self.assertEqual(v, "FINDING")
            self.assertTrue(any("assistant-attributed" in n and "maintainer/other" in n
                                for n in notes))

        def test_pr_required_all_pr_is_ok(self):
            self.assertEqual(verdict("pr-required", 0, 0, 12, 0, True)[0], "OK")

        def test_missing_ci_is_finding_any_policy(self):
            self.assertEqual(verdict("pr-required", 0, 0, 12, 0, False)[0], "FINDING")
            self.assertEqual(verdict("exchange", 0, 0, 12, 0, False)[0], "FINDING")

        def test_exchange_direct_push_not_a_finding(self):
            v, notes = verdict("exchange", 3, 2, 0, 0, True)
            self.assertEqual(v, "OK-EXCHANGE")
            self.assertTrue(any("expected" in n for n in notes))

        def test_all_unknown_is_unverifiable_not_ok(self):
            # gh failed for the whole repo: cannot see is NOT OK (false-negative guard)
            v, notes = verdict("pr-required", 0, 0, 0, 3, True)
            self.assertEqual(v, "UNVERIFIABLE")
            self.assertTrue(any("NOT treated as OK" in n for n in notes))

        def test_partial_unknown_with_pr_is_ok_partial(self):
            # some commits classified as PR, a few unknown: OK-PARTIAL, not UNVERIFIABLE
            self.assertEqual(verdict("pr-required", 0, 0, 10, 3, True)[0], "OK-PARTIAL")

        def test_finding_takes_precedence_over_exchange(self):
            # an exchange repo with no CI is still a finding (CI is mandatory)
            self.assertEqual(verdict("exchange", 5, 0, 0, 0, False)[0], "FINDING")

        def test_assistant_direct_is_finding_even_with_maintainer_direct(self):
            v, _ = verdict("pr-required", 1, 3, 0, 0, True)
            self.assertEqual(v, "FINDING")

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

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(VerdictTests))
    suite.addTests(loader.loadTestsFromTestCase(CiDetectionTests))
    res = unittest.TextTestRunner(verbosity=1).run(suite)
    return 0 if res.wasSuccessful() else 1


def main():
    ap = argparse.ArgumentParser(description="Cross-repo validation-coverage audit.")
    ap.add_argument("--window", type=int, default=DEFAULT_WINDOW,
                    help=f"commits per repo to classify (default {DEFAULT_WINDOW})")
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
