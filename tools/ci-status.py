#!/usr/bin/env python3
"""Operator CI-status reader (3b167 ORCH-CI-STATUS): report the GitHub Actions runs for a
PR's head commit or for a given commit, through ``gh api repos/<repo>/actions/runs``.

The fleet-owned /orch command names tools/ci-status.sh, the wrapper for this module.
This operator reader uses the Actions runs endpoint (Actions:Read) and, in PR mode,
gh pr view --json headRefOid,state (Pull requests:Read). It never calls Checks or commit
statuses. Token permissions vary; the merge gate remains merge-when-green.py.

GREEN requires a recognized, complete, nonempty page, all entries for the requested
head, and completed/success for the selected run in every (workflow path, event) slot.
PR mode additionally requires the workflows configured in REQUIRED_RUNS, looked up
case-insensitively after removing a trailing .git (a trailing . is rejected);
unlisted repositories and SHA mode have no required workflow set. Before any gh call,
--repo must be owner/name: one "/", nonempty parts of ASCII letters, digits, ".", "-" and
"_", the owner starting with an ASCII letter, digit or "_", and neither part "." or "..".
Missing required runs mean PENDING unless failure, unrecognized data, a name collision,
a moved head, or an incomplete page requires NOT-GREEN. PR mode re-reads the head after
the runs read; a read error exits 2.

Before selection, validate positive integer id/run_number/run_attempt (excluding bool),
nonempty string path/event, and recognized status/conclusion combinations, requiring
the conclusion field (null only for non-completed runs). Every JSON response rejects
duplicate members before interpretation, including PR-head reads. Duplicate
run IDs or duplicate run numbers within a workflow across events fail closed, including identical entries
and multiple attempts of one run. Among distinct valid runs, the highest run_number
wins. An older run with run_attempt > 1 fails closed regardless of its conclusion:
neither attempt counters nor creation order prove cross-run retry chronology. No
timestamp ordering is assumed. An ordinary older first-attempt failure may be superseded;
a single current retry is classified by its supplied status/conclusion. A retried older
run keeps that head NOT-GREEN while it is listed, even when it and the newest run
succeeded; only a new push with a new head clears it.

On recognized page shapes, named entries remain visible. Other-head, invalid, ambiguous
and superseded entries are marked, including on incomplete pages; supersession markers
compare only received
entries. Unnamed/non-object entries are reported in the reason. Unrecognized status or
conclusion data fails closed even on a run that would otherwise be superseded.

Limitations: this is a point-in-time interpretation of the returned Actions page, not
a merge authorization or an atomic snapshot. It cannot prove server freshness or detect
unreported runs. Other apps' checks, commit statuses, individual jobs and PR association
are not evaluated. Runs for another PR sharing the head can satisfy the configured set.
A successful workflow need not mean every job ran. SHA mode has no PR head re-read.
The merge-time requirements remain merge-when-green.py's.

Usage:
    tools/ci-status.sh --repo owner/name --pr <number>
    tools/ci-status.sh --repo owner/name --sha <40-hex commit>
    python3 tools/ci-status.py --self-test

Exit codes: 0 GREEN (every current run completed successfully, required runs present); 1
NOT green (a failing or unrecognized run, an older retried run, a name collision, a moved
head, a truncated page, or no runs where no required set applies; fail-closed);
2 usage, gh, JSON or unusable-head error; 3 PENDING (no failure seen; a run not yet
completed, or a required workflow's run not yet registered).
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import re
import subprocess
import sys

GREEN, PENDING, NOT_GREEN = "GREEN", "PENDING", "NOT-GREEN"
_EXIT = {GREEN: 0, NOT_GREEN: 1, PENDING: 3}
_HEX40 = re.compile(r"[0-9a-f]{40}")
# owner/name for the gh api URL path (3b435): the owner cannot start with "." or "-" (gh pr
# view could read a leading "-" as a flag); the name may start with "." (owner/.github), and
# main() rejects a "." or ".." part, the only URL dot-segments
_REPO = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.-]*/[A-Za-z0-9_.-]+")
_PR_NUMBER = re.compile(r"[0-9]+")  # ASCII only: str.isdigit accepts non-ASCII digits
# The workflows this repository's merge gate requires of a PR, each top-level workflow name
# bound to its file the way merge-when-green.py's ACTIONS_FALLBACK binds them (3b132): a
# same-named run from another file must not stand in for it. Applied in --pr mode only, on
# the pull_request event (_PR_EVENT); --sha reads a bare commit, which may be a push to
# main, where `PR attribution` never runs. A required workflow whose run is missing reads
# as PENDING unless a failure or uncertainty requires NOT-GREEN; never GREEN.
REQUIRED_RUNS = {
    "jposluns/grc_library": {
        "Repository quality checks": ".github/workflows/quality.yml",
        "PR attribution": ".github/workflows/pr-attribution.yml",
    },
}
_PR_EVENT = "pull_request"  # a required workflow counts only from a run on this event


def gh(*args: str) -> str:
    """Run gh and return its stdout. Its stderr is captured, so a failure carries it to the
    error report; after a success it is passed through (the merge-when-green runner)."""
    done = subprocess.run(["gh", *args], text=True, capture_output=True)
    if done.returncode != 0:
        raise subprocess.CalledProcessError(done.returncode, done.args, done.stdout, done.stderr)
    if done.stderr:
        sys.stderr.write(done.stderr)
    return done.stdout


def _failure(exc: BaseException) -> str:
    """A failed gh call for the operator: the exception and, as gh() captures it, what gh printed."""
    err = getattr(exc, "stderr", None)
    return f"{exc} gh: {err.strip()}" if isinstance(err, str) and err.strip() else str(exc)


def _unique_members(pairs: list[tuple]) -> dict:
    """Reject duplicate JSON members at every nesting level before validation."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON member: {key!r}")
        result[key] = value
    return result


def _age(r: dict) -> int:
    """Creation order within a validated (path, event) slot, not retry chronology.

    GitHub keeps run_number and id across retries; run_attempt is local to one run.
    Duplicate IDs/numbers and retries of older runs are rejected by classify().
    """
    return r["run_number"]


def _metadata_error(r: dict) -> str:
    """Validate verdict-relevant fields before any entry can be superseded."""
    for key in ("id", "run_number", "run_attempt"):
        if type(r.get(key)) is not int or r[key] < 1:
            return f"invalid {key}"
    for key in ("path", "event"):
        if not isinstance(r.get(key), str) or not r[key].strip():
            return f"invalid {key}"
    if "conclusion" not in r:
        return "missing conclusion"
    status, conclusion = r.get("status"), r["conclusion"]
    if not isinstance(status, str) or status not in (
            "completed", "queued", "in_progress", "requested", "waiting", "pending"):
        return "unrecognized status"
    if status == "completed":
        if not isinstance(conclusion, str) or conclusion not in (
                "success", "failure", "neutral", "cancelled", "skipped", "timed_out",
                "action_required", "stale", "startup_failure"):
            return "unrecognized completed conclusion"
    elif conclusion is not None:
        return "non-completed run has a conclusion"
    return ""


def classify(payload, head: str, required: dict | None = None) -> tuple[str, list[str], str]:
    """Return (verdict, per-run lines, reason) for an Actions runs page.

    Required maps workflow names to exact paths on pull_request events. Validate before
    selecting by run_number; reject duplicate identities and older retried runs.
    Failures and uncertainty outrank pending/missing runs. See the module contract.
    """
    required = dict(required or {})
    total = payload.get("total_count") if isinstance(payload, dict) else None
    runs = payload.get("workflow_runs") if isinstance(payload, dict) else None
    if not isinstance(runs, list) or type(total) is not int:
        return NOT_GREEN, [], "the Actions runs response has an unrecognized shape (fail-closed: not green)"

    def line(r: dict, note: str = "") -> str:
        status, concl = r.get("status"), r.get("conclusion")
        return (f"{r['name']}  {status or 'no-status'}  {concl or '-'}"
                f"  (run {r.get('id')}, {r.get('event')}, {r.get('path')}){note}")

    named = [r for r in runs if isinstance(r, dict) and isinstance(r.get("name"), str) and r["name"]]
    truncated = total != len(runs)
    if not runs and not truncated:
        if required:
            return PENDING, [], (
                f"no Actions workflow runs registered yet for {head[:12]}; required workflow "
                "run(s) missing (a missing run reads as pending, never green): "
                + ", ".join(f"{w} (from {p})" for w, p in required.items()))
        return NOT_GREEN, [], (f"no Actions workflow runs reported for {head[:12]} (fail-closed: not green; "
                               "a just-pushed head may not have registered its runs yet, so re-read "
                               "before concluding CI never ran)")
    newest: dict[tuple, dict] = {}
    errors: dict[int, str] = {}
    seen_ids: dict[int, dict] = {}
    seen_numbers: dict[tuple, dict] = {}
    for r in named:
        error = _metadata_error(r)
        if error:
            errors[id(r)] = error
            continue
        key = (r["path"], r["event"])
        for seen, identity in ((seen_ids, r["id"]),
                               (seen_numbers, (r["path"], r["run_number"]))):
            if identity in seen:
                errors[id(r)] = "duplicate run ID or workflow run number"
                errors[id(seen[identity])] = errors[id(r)]
            seen[identity] = r
        if r.get("head_sha") == head and (key not in newest or _age(r) > _age(newest[key])):
            newest[key] = r
    lines: list[str] = []
    live: list[dict] = []
    pending: list[str] = []
    failed: list[str] = []
    unknown: list[str] = []
    retried: list[str] = []
    for r in runs:
        if not (isinstance(r, dict) and isinstance(r.get("name"), str) and r["name"]):
            unknown.append(f"<unrecognized run entry: {r!r:.60}>")
            continue
        label = f"{r['name']} (run {r.get('id')})"
        if r.get("head_sha") != head:
            lines.append(line(r, "  [other commit]"))
            unknown.append(f"{label} [for commit {r.get('head_sha')!r}, not the requested head]")
            continue
        if id(r) in errors:
            lines.append(line(r, f"  [{errors[id(r)]}]"))
            unknown.append(f"{label} [{errors[id(r)]}]")
            continue
        current = newest[(r["path"], r["event"])]
        if current is not r:
            if r["run_attempt"] > 1:
                note = "older run was retried; attempt chronology is unproven"
                lines.append(line(r, f"  [{note}]"))
                retried.append(f"{label} [{note}]")
            else:
                lines.append(line(r, f"  [superseded by run {current.get('id')}]"))
            continue
        lines.append(line(r))
        live.append(r)
        status, concl = r.get("status"), r.get("conclusion")
        if status != "completed":
            pending.append(f"{label} [{status or 'no-status'}]")
        elif concl != "success":
            failed.append(f"{label} [{concl or 'no-conclusion'}]")
    retry_reason = ("older retried run(s) keep this head NOT-GREEN while listed; "
                    "push a new commit with a new head to clear it: " + ", ".join(retried))
    if truncated:
        return NOT_GREEN, lines, (
            f"the Actions runs response lists {len(runs)} of {total} run(s); cannot see them "
            "all (fail-closed: not green; markers compare received entries only)"
            + ("; UNRECOGNIZED: " + ", ".join(unknown) if unknown else "")
            + ("; " + retry_reason if retried else ""))
    missing: list[str] = []
    collision: list[str] = []
    for want, path in required.items():
        runs_named = [r for r in live if r["name"] == want]
        foreign = [r for r in runs_named if r.get("path") != path]
        if foreign:
            collision.append(f"{want} is also reported from {foreign[0].get('path')!r}, not "
                             f"only {path!r} (only its own file may satisfy it)")
        if not any(r.get("path") == path and r.get("event") == _PR_EVENT for r in runs_named):
            missing.append(f"{want} (from {path}, on a {_PR_EVENT} event)")
    if failed or unknown or collision or retried:
        parts: list[str] = []
        if failed:
            parts.append("failing / non-success run(s): " + ", ".join(failed))
        if unknown:
            parts.append("UNRECOGNIZED run(s) (fail-closed: not green): " + ", ".join(unknown))
        if retried:
            parts.append(retry_reason)
        if collision:
            parts.append("required-workflow name collision (fail-closed: not green): "
                         + ", ".join(collision))
        if pending:
            parts.append("still pending: " + ", ".join(pending))
        if missing:
            parts.append("required workflow run(s) missing: " + ", ".join(missing))
        return NOT_GREEN, lines, "; ".join(parts)
    if pending or missing:
        parts = []
        if pending:
            parts.append("pending / incomplete run(s): " + ", ".join(pending))
        if missing:
            parts.append("required workflow run(s) not yet registered (a missing run reads as "
                         "pending, never green): " + ", ".join(missing))
        return PENDING, lines, "; ".join(parts)
    need = ("; required workflow(s) present and green: " + ", ".join(required)) if required else ""
    return GREEN, lines, f"all {len(live)} current Actions run(s) for {head[:12]} completed successfully{need}"


def head_for_pr(pr: str, repo: str) -> tuple[str, str]:
    """The PR's current head commit and state, via ``gh pr view --json headRefOid,state``
    (Pull requests:Read; deliberately not the Checks API). An unusable head raises ValueError."""
    data = json.loads(gh("pr", "view", pr, "--repo", repo, "--json", "headRefOid,state"),
                      object_pairs_hook=_unique_members)
    head = data.get("headRefOid") if isinstance(data, dict) else None
    if not (isinstance(head, str) and _HEX40.fullmatch(head.lower())):
        raise ValueError(f"gh pr view returned no usable head commit for PR #{pr}: {head!r}")
    return head.lower(), str(data.get("state"))


def _self_test() -> int:
    """classify() fixtures (the green page, each pending route, a missing required run, each
    not-green route, newest-run dedup, truncation diagnostics) plus the moved-head re-read,
    driven through main() with gh stubbed in-module: pure, no real gh call, no network."""
    head = "3f0c9e71a2b48d5609ce17f4b23a8d60e95c1b7a"

    def run(name="quality", status="completed", concl="success", sha=head, rid=1, event="push",
            path=".github/workflows/quality.yml"):
        return {"id": rid, "run_number": rid, "run_attempt": 1,
                "name": name, "path": path, "event": event,
                "status": status, "conclusion": concl, "head_sha": sha}

    def page(runs, total=None):
        return {"total_count": len(runs) if total is None else total, "workflow_runs": runs}

    req = {"Repository quality checks": ".github/workflows/quality.yml",
           "PR attribution": ".github/workflows/pr-attribution.yml"}

    def qrun(**kw):
        kw.setdefault("name", "Repository quality checks")
        kw.setdefault("event", _PR_EVENT)
        return run(**kw)

    def arun(**kw):
        kw.setdefault("name", "PR attribution")
        kw.setdefault("path", ".github/workflows/pr-attribution.yml")
        kw.setdefault("event", _PR_EVENT)
        kw.setdefault("rid", 2)
        return run(**kw)

    cases = [
        ("green-one-run", page([run()]), GREEN, None),
        ("green-many-runs", page([run(), run(name="attribution", rid=2, event="pull_request",
                                             path=".github/workflows/attribution.yml")]), GREEN, None),
        ("pending-in-progress", page([run(status="in_progress", concl=None)]), PENDING, None),
        ("pending-queued", page([run(status="queued", concl=None)]), PENDING, None),
        ("unknown-no-status", page([run(status=None, concl=None)]), NOT_GREEN, None),
        ("pending-beside-green", page([run(), run(name="b", rid=2, path="b.yml",
                                                  status="in_progress", concl=None)]), PENDING, None),
        ("failure", page([run(concl="failure")]), NOT_GREEN, None),
        ("cancelled", page([run(concl="cancelled")]), NOT_GREEN, None),
        ("skipped-is-not-success", page([run(concl="skipped")]), NOT_GREEN, None),
        ("no-conclusion-completed", page([run(concl=None)]), NOT_GREEN, None),
        ("failure-outranks-pending", page([run(concl="failure"),
                                           run(name="b", rid=2, path="b.yml",
                                               status="queued", concl=None)]), NOT_GREEN, None),
        ("no-runs", page([]), NOT_GREEN, None),
        ("truncated-page", page([run()], total=2), NOT_GREEN, None),
        ("foreign-head", page([run(sha="b" * 40)]), NOT_GREEN, None),
        ("unrecognized-entry", page([run(), "garbage"]), NOT_GREEN, None),
        ("unnamed-run", page([run(name="")]), NOT_GREEN, None),
        ("non-dict-payload", ["not", "a", "page"], NOT_GREEN, None),
        ("shapeless-page", {"workflow_runs": {}, "total_count": 1}, NOT_GREEN, None),
        ("float-total", {"workflow_runs": [run()], "total_count": 1.0}, NOT_GREEN, None),
        # newest-run-per-(path, event) dedup: a superseded failure clears; a newest failure stays
        ("superseded-failure-newest-green", page([run(concl="failure"), run(rid=2)]), GREEN, None),
        ("superseded-green-newest-failure", page([run(), run(rid=2, concl="failure")]), NOT_GREEN, None),
        # the required set (REQUIRED_RUNS, --pr mode): a missing run is PENDING, never GREEN
        ("required-all-present", page([qrun(), arun()]), GREEN, req),
        ("required-missing-quality-run", page([arun()]), PENDING, req),
        ("required-no-runs-yet", page([]), PENDING, req),
        ("required-wrong-event-only", page([qrun(event="push"), arun()]), PENDING, req),
        ("required-path-collision", page([qrun(path=".github/workflows/other.yml"), arun()]),
         NOT_GREEN, req),
        ("required-missing-beside-failure", page([arun(concl="failure")]), NOT_GREEN, req),
        ("edited-then-fixed", page([qrun(), arun(rid=2, concl="failure"), arun(rid=3)]), GREEN, req),
        ("edited-then-broken", page([qrun(), arun(rid=2), arun(rid=3, concl="failure")]),
         NOT_GREEN, req),
    ]
    cases.append(("required-missing-attribution", page([qrun()]), PENDING, req))
    for field in ("id", "run_number", "run_attempt", "path", "event", "status", "conclusion"):
        broken = dict(run(rid=2), **{field: []})
        cases.append((f"malformed-{field}", page([run(), broken]), NOT_GREEN, None))
    for label, entries, want in (
        ("number-before-id", [dict(run(rid=9, concl="failure"), run_number=1),
                              dict(run(rid=1), run_number=2)], GREEN),
        ("duplicate-attempts", [run(), dict(run(concl="failure"), run_attempt=2)], NOT_GREEN),
        ("duplicate-number", [run(), dict(run(rid=2), run_number=1)], NOT_GREEN),
        ("older-retry", [dict(run(concl="failure"), run_attempt=2), run(rid=2)], NOT_GREEN),
        ("single-retry-success", [dict(run(), run_attempt=2)], GREEN),
        ("single-retry-failure", [dict(run(concl="failure"), run_attempt=2)], NOT_GREEN),
    ):
        for reverse in (False, True):
            cases.append((f"{label}-{reverse}", page(entries[::-1] if reverse else entries), want, None))
    bad = []
    if REQUIRED_RUNS.get("jposluns/grc_library") != req:
        bad.append("required workflow configuration changed")
    for name, payload, want, required in cases:
        verdict, _, reason = classify(payload, head, required)
        if verdict != want:
            bad.append(f"{name}: wanted {want}, got {verdict} ({reason})")
    # the per-run report carries each run's name, status and conclusion
    _, lines, _ = classify(page([run(status="in_progress", concl=None)]), head)
    if not (len(lines) == 1 and "quality" in lines[0] and "in_progress" in lines[0]):
        bad.append(f"report lines: wanted name+status in one line, got {lines!r}")
    # a superseded run stays visible as a marked display line; only the newest is classified
    _, lines, _ = classify(page([qrun(), arun(rid=2, concl="failure"), arun(rid=3)]), head, req)
    if not (len(lines) == 3 and any("superseded by run 3" in ln for ln in lines)):
        bad.append(f"superseded display: wanted 3 lines with a superseded marker, got {lines!r}")
    # a truncated page still reports the runs it did receive (fail-closed, with diagnostics)
    verdict, lines, reason = classify(
        page([run(sha="b" * 40), run(rid=2), run(rid=3)], total=4), head)
    if not (verdict == NOT_GREEN and len(lines) == 3
            and "[other commit]" in lines[0] and "[superseded by run 3]" in lines[1]
            and "3 of 4 run(s)" in reason):
        bad.append(f"truncation diagnostics: wanted the received run kept, got {lines!r} ({reason})")
    # the moved-head re-read, driven through main() with gh stubbed (no real gh call)
    global gh
    real_gh, heads = gh, iter([head, "c" * 40])

    def _stub_gh(*a):
        if a[:2] == ("pr", "view"):
            return json.dumps({"headRefOid": next(heads), "state": "OPEN"})
        return json.dumps(page([qrun(), arun()]))

    gh = _stub_gh
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main(["ci-status.py", "--repo", "jposluns/grc_library", "--pr", "7"])
    finally:
        gh = real_gh
    if not (rc == 1 and "moved" in buf.getvalue()):
        bad.append(f"moved-head: wanted exit 1 with a moved-head reason, got rc={rc}: {buf.getvalue()!r}")
    if bad:
        print("SELF-TEST FAILED:\n  " + "\n  ".join(bad), file=sys.stderr)
        return 1
    print(f"OK: ci-status classify self-test passed ({len(cases) + 4} cases)")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__.split("\n\n", 1)[0],
        epilog="Exit codes:" + __doc__.split("Exit codes:", 1)[1],
        formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False)
    ap.add_argument("--repo", help="owner/name (required; no default; required-workflow "
                                   "lookup is case-insensitive)")
    what = ap.add_mutually_exclusive_group()
    what.add_argument("--pr", metavar="N", help="PR number: read the runs for its current head commit")
    what.add_argument("--sha", metavar="SHA", help="full 40-hex commit to read the runs for")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv[1:])
    if args.self_test:
        return _self_test()
    if args.repo and args.repo.lower().endswith(".git"):
        args.repo = args.repo[:-4]
    if (not args.repo or not _REPO.fullmatch(args.repo)
            or any(part in (".", "..") for part in args.repo.split("/"))
            or args.repo.endswith(".") or args.repo.lower().endswith(".git")):
        print("ERROR: --repo owner/name is required", file=sys.stderr)
        return 2
    required: dict = {}
    if args.pr:
        if not _PR_NUMBER.fullmatch(args.pr):
            print(f"ERROR: --pr takes a PR number, got {args.pr!r}", file=sys.stderr)
            return 2
        try:
            head, state = head_for_pr(args.pr, args.repo)
        except (subprocess.CalledProcessError, OSError, json.JSONDecodeError, ValueError) as exc:
            print(f"ERROR: gh pr view failed: {_failure(exc)}", file=sys.stderr)
            return 2
        target = f"PR #{args.pr} ({state})"
        required = REQUIRED_RUNS.get(args.repo.lower(), {})
    elif args.sha:
        if not _HEX40.fullmatch(args.sha.lower()):
            print(f"ERROR: --sha takes a full 40-hex commit, got {args.sha!r}", file=sys.stderr)
            return 2
        head, target = args.sha.lower(), "commit"
    else:
        print("ERROR: one of --pr <number> or --sha <40-hex commit> is required", file=sys.stderr)
        return 2
    try:
        payload = json.loads(gh("api", f"repos/{args.repo}/actions/runs?head_sha={head}&per_page=100"),
                             object_pairs_hook=_unique_members)
    except (subprocess.CalledProcessError, OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: gh api actions/runs failed: {_failure(exc)}", file=sys.stderr)
        return 2
    verdict, lines, reason = classify(payload, head, required)
    if args.pr:
        # Re-read the head AFTER the runs read: a push between the two reads means the runs
        # above describe a superseded head, and that must never read as the current head's
        # green (vpr 3b167 r1 CI-01). Fail-closed, like every other unconfirmable state.
        try:
            head_now, _ = head_for_pr(args.pr, args.repo)
        except (subprocess.CalledProcessError, OSError, json.JSONDecodeError, ValueError) as exc:
            print(f"ERROR: gh pr view (head re-read) failed: {_failure(exc)}", file=sys.stderr)
            return 2
        if head_now != head:
            verdict = NOT_GREEN
            reason = (f"the PR head moved during the read ({head[:12]} to {head_now[:12]}); the "
                      f"runs above describe the superseded head {head[:12]}, so this read proves "
                      "nothing about the current head: re-run (fail-closed: not green)")
    print(f"CI for {target} at {head[:12]} in {args.repo}:")
    for line in lines:
        print("  " + line)
    print(f"{verdict}: {reason}")
    return _EXIT[verdict]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
