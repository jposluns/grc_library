#!/usr/bin/env python3
"""Merge-when-green guard (P-1.6): merge a PR ONLY when every CI check has completed
successfully and NONE is pending, never on a pending / failing / no-checks state.

On #1297 the orchestrator merged (``--admin``) while ``Lint markdown corpus`` was still
PENDING: the CI watch was bundled into the PR-create command so it ran before the checks
registered (exited "no checks reported"), and the merge step's ``grep -q fail`` treated
pending / no-checks as acceptable. The code was fine (locally green), but merge-on-unconfirmed-CI
violates the merge-on-green discipline. This tool makes the decision mechanical and fail-safe:
it reads the PR's ``statusCheckRollup``, REFUSES unless every check is terminal-success with
zero pending, and only then merges. Unknown / no-checks / any-pending / any-failing all REFUSE.

It does NOT replace the CI WAIT (use ``gh pr checks <N> --watch`` first, per the PR-activity
discipline); it is the final GATE on the merge itself. ``--dry-run`` reports the verdict without
merging.

Usage:
    python3 tools/merge-when-green.py <PR> --repo owner/name --admin
    python3 tools/merge-when-green.py <PR> --repo owner/name --dry-run
    python3 tools/merge-when-green.py --self-test

Exit codes: 0 merged (or dry-run green); 1 REFUSED (pending / failing / no-checks / not-open);
2 usage or gh error. The refusal is the whole point: it fails CLOSED (never merges on doubt).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

_OK_CONCLUSION = {"SUCCESS", "NEUTRAL", "SKIPPED"}  # a CheckRun that finished acceptably
_OK_STATE = {"SUCCESS"}  # a legacy StatusContext that finished acceptably


def evaluate(rollup: list[dict]) -> tuple[bool, str]:
    """PURE decision over a GitHub ``statusCheckRollup``: (green, reason). Fails CLOSED:
    green ONLY when at least one check exists and EVERY check is terminal-success with none
    pending; a no-checks, any-pending, any-failing, or unknown-shape check REFUSES."""
    if not rollup:
        return False, "no checks reported for this PR (never merge on no-checks)"
    pending: list[str] = []
    failed: list[str] = []
    unknown: list[str] = []
    for c in rollup:
        if not isinstance(c, dict):
            unknown.append(f"<non-dict entry: {c!r}>")
            continue
        typename = c.get("__typename")
        name = c.get("name") or c.get("context") or "<check>"
        if typename == "CheckRun":
            status, concl = c.get("status"), c.get("conclusion")
            if status != "COMPLETED":
                pending.append(f"{name} [{status or 'no-status'}]")
            elif concl not in _OK_CONCLUSION:
                failed.append(f"{name} [{concl or 'no-conclusion'}]")
        elif typename == "StatusContext":
            state = c.get("state")
            if state in (None, "PENDING", "EXPECTED"):
                pending.append(f"{name} [{state or 'no-state'}]")
            elif state not in _OK_STATE:
                failed.append(f"{name} [{state}]")
        else:
            # UNRECOGNIZED check shape -> REFUSE fail-closed, REGARDLESS of any `state`
            # field: a new / unknown GitHub check type (or a malformed entry) must never be
            # waved through green. A green verdict comes ONLY from a recognized CheckRun or
            # StatusContext (codex vpr1327: the else-via-state branch fail-OPENED on an
            # unknown typename carrying state=SUCCESS).
            unknown.append(f"{name} [unrecognized shape: {typename!r}]")
    if failed or unknown:
        parts: list[str] = []
        if failed:
            parts.append("failing / non-success: " + ", ".join(failed))
        if unknown:
            parts.append("UNRECOGNIZED shape (fail-closed refuse): " + ", ".join(unknown))
        if pending:
            parts.append("pending: " + ", ".join(pending))
        return False, "; ".join(parts)
    if pending:
        return False, "pending / incomplete check(s): " + ", ".join(pending)
    return True, f"all {len(rollup)} check(s) completed successfully"


def gh(*args: str) -> str:
    return subprocess.check_output(["gh", *args], text=True)


def _self_test() -> int:
    checks = []
    cr = lambda n, s, c: {"__typename": "CheckRun", "name": n, "status": s, "conclusion": c}
    sc = lambda n, st: {"__typename": "StatusContext", "context": n, "state": st}
    cases = [
        ("all-green-checkruns", [cr("a", "COMPLETED", "SUCCESS"), cr("b", "COMPLETED", "SKIPPED")], True),
        ("no-checks-refused", [], False),
        ("one-pending-refused", [cr("a", "COMPLETED", "SUCCESS"), cr("b", "IN_PROGRESS", None)], False),
        ("queued-refused", [cr("a", "QUEUED", None)], False),
        ("failure-refused", [cr("a", "COMPLETED", "SUCCESS"), cr("b", "COMPLETED", "FAILURE")], False),
        ("completed-null-conclusion-refused", [cr("a", "COMPLETED", None)], False),
        ("unknown-shape-with-state-SUCCESS-refused", [{"__typename": "Weird", "name": "x", "state": "SUCCESS"}], False),
        ("non-dict-entry-refused", ["not-a-dict"], False),
        ("timed-out-refused", [cr("a", "COMPLETED", "TIMED_OUT")], False),
        ("action-required-refused", [cr("a", "COMPLETED", "ACTION_REQUIRED")], False),
        ("stale-refused", [cr("a", "COMPLETED", "STALE")], False),
        ("waiting-status-refused", [cr("a", "WAITING", None)], False),
        ("statuscontext-error-refused", [sc("ci", "ERROR")], False),
        ("statuscontext-null-state-refused", [sc("ci", None)], False),
        ("cancelled-refused", [cr("a", "COMPLETED", "CANCELLED")], False),
        ("statuscontext-success", [sc("ci", "SUCCESS")], True),
        ("statuscontext-pending-refused", [sc("ci", "PENDING")], False),
        ("statuscontext-failure-refused", [sc("ci", "FAILURE")], False),
        ("unknown-shape-refused", [{"__typename": "Weird", "name": "x"}], False),  # no state -> pending
        ("mixed-green", [cr("a", "COMPLETED", "SUCCESS"), sc("b", "SUCCESS"), cr("c", "COMPLETED", "NEUTRAL")], True),
    ]
    for name, rollup, want_green in cases:
        green, _ = evaluate(rollup)
        checks.append((name, green == want_green))
    # a failure names the failing check; a pending names the pending one
    _, r_fail = evaluate([cr("Lint", "COMPLETED", "FAILURE")])
    checks.append(("failure-reason-names-check", "Lint" in r_fail))
    _, r_pend = evaluate([cr("Lint", "IN_PROGRESS", None)])
    checks.append(("pending-reason-names-check", "Lint" in r_pend))
    bad = [n for n, ok in checks if not ok]
    if bad:
        print(f"merge-when-green self-test: FAIL {bad}")
        return 1
    print(f"merge-when-green self-test: OK ({len(checks)} checks)")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pr", nargs="?", help="PR number")
    ap.add_argument("--repo", help="owner/name (defaults to the current repo's remote)")
    ap.add_argument("--merge-method", default="squash", choices=["squash", "merge", "rebase"])
    ap.add_argument("--admin", action="store_true", help="pass --admin (REVIEW_REQUIRED bypass) to gh pr merge")
    ap.add_argument("--dry-run", action="store_true", help="report the verdict; do NOT merge")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv[1:])
    if args.self_test:
        return _self_test()
    if not args.pr:
        ap.print_usage(sys.stderr)
        print("ERROR: give a PR number (or --self-test).", file=sys.stderr)
        return 2
    repo_args = ["--repo", args.repo] if args.repo else []
    try:
        raw = gh("pr", "view", args.pr, *repo_args,
                 "--json", "statusCheckRollup,number,title,state")
        view = json.loads(raw)
    except (subprocess.CalledProcessError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: gh pr view failed: {exc}", file=sys.stderr)
        return 2
    if view.get("state") != "OPEN":
        print(f"REFUSE: PR #{args.pr} is {view.get('state')}, not OPEN.", file=sys.stderr)
        return 1
    green, reason = evaluate(view.get("statusCheckRollup") or [])
    if not green:
        print(f"REFUSE to merge PR #{args.pr}: {reason}", file=sys.stderr)
        return 1
    print(f"PR #{args.pr} is GREEN: {reason}")
    if args.dry_run:
        print("--dry-run: not merging.")
        return 0
    merge = ["pr", "merge", args.pr, *repo_args, f"--{args.merge_method}"]
    if args.admin:
        merge.append("--admin")
    try:
        gh(*merge)
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"ERROR: gh pr merge failed: {exc}", file=sys.stderr)
        return 2
    print(f"MERGED PR #{args.pr} ({args.merge_method}).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
