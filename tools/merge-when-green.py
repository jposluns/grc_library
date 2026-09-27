#!/usr/bin/env python3
"""Merge-when-green guard (P-1.6): merge a PR ONLY when every CI check has completed
successfully and NONE is pending, never on a pending / failing / no-checks state.

On #1297 the orchestrator merged (``--admin``) while ``Lint markdown corpus`` was still
PENDING: the CI watch was bundled into the PR-create command so it ran before the checks
registered (exited "no checks reported"), and the merge step's ``grep -q fail`` treated
pending / no-checks as acceptable. The code was fine (locally green), but merge-on-unconfirmed-CI
violates the merge-on-green discipline. This tool makes the decision mechanical and fail-safe:
it reads the PR's ``statusCheckRollup``, REFUSES unless every check is terminal-success with
zero pending, and only then merges. Unknown / no-checks / any-pending / any-failing all REFUSE,
as does a required check (REQUIRED_CHECKS, or --require) that is missing as a CheckRun or did not conclude
SUCCESS: NEUTRAL or SKIPPED passes only for the other checks (3b104).
The merge is pinned to the head commit it evaluated (gh pr merge --match-head-commit), so a push
landing after the read is never merged unchecked; a missing head SHA refuses (3b106).

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
# Checks that must be PRESENT and SUCCESS: NEUTRAL or SKIPPED is acceptable for any other check,
# never for these, so a skipped corpus lint cannot read as green (3b104).
REQUIRED_CHECKS = ("Lint markdown corpus", "PR attribution (title and body)")


def evaluate(rollup: list[dict], required: tuple[str, ...] = ()) -> tuple[bool, str]:
    """PURE decision over a GitHub ``statusCheckRollup``: (green, reason). Fails CLOSED:
    green ONLY when at least one check exists and EVERY check is terminal-success with none
    pending; a no-checks, any-pending, any-failing, or unknown-shape check REFUSES. Each name
    in ``required`` must also be reported and must have concluded SUCCESS itself (3b104)."""
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
    # Required checks bind to CheckRuns only: a commit status of the same name must not stand in
    # for an Actions job that never ran (3b104 QA r1). Every entry under a required name must
    # have succeeded, so a skipped duplicate still refuses (deliberately fail closed).
    absent = [w for w in required
              if not any(c.get("__typename") == "CheckRun" and c.get("name") == w
                         for c in rollup if isinstance(c, dict))]
    note = ("; required check(s) not yet reported as a CheckRun: " + ", ".join(absent)) if absent else ""
    if failed or unknown:
        parts: list[str] = []
        if failed:
            parts.append("failing / non-success: " + ", ".join(failed))
        if unknown:
            parts.append("UNRECOGNIZED shape (fail-closed refuse): " + ", ".join(unknown))
        if pending:
            parts.append("pending: " + ", ".join(pending))
        return False, "; ".join(parts) + note
    if pending:
        return False, "pending / incomplete check(s): " + ", ".join(pending) + note
    for want in required:
        if want in absent:
            return False, f"required check not reported as a CheckRun: {want}"
        for c in rollup:
            if (c.get("name") or c.get("context")) == want and c.get("__typename") != "CheckRun":
                return False, (f"required check {want} is also reported as a commit status of the same name "
                               "(a name collision); only the CheckRun may satisfy it")
            if c.get("__typename") == "CheckRun" and c.get("name") == want and c.get("conclusion") != "SUCCESS":
                return False, f"required check did not succeed: {want} [{c.get('conclusion')}]"
    verified = ", ".join(required) if required else "none"
    return True, f"all {len(rollup)} check(s) completed successfully; required: {verified}"


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
    req = ("Lint",)
    for name, rollup, want_green in [
        ("required-success-green", [cr("Lint", "COMPLETED", "SUCCESS"), cr("b", "COMPLETED", "SKIPPED")], True),
        ("required-skipped-refused", [cr("Lint", "COMPLETED", "SKIPPED"), cr("b", "COMPLETED", "SUCCESS")], False),
        ("required-neutral-refused", [cr("Lint", "COMPLETED", "NEUTRAL")], False),
        ("required-missing-refused", [cr("b", "COMPLETED", "SUCCESS")], False),
        ("required-statuscontext-only-refused", [sc("Lint", "SUCCESS")], False),
        ("required-checkrun-plus-same-name-status-refused", [cr("Lint", "COMPLETED", "SUCCESS"), sc("Lint", "SUCCESS")], False),
        ("required-one-of-two-skipped-refused", [cr("Lint", "COMPLETED", "SUCCESS"), cr("Lint", "COMPLETED", "SKIPPED")], False),
    ]:
        green, _ = evaluate(rollup, req)
        checks.append((name, green == want_green))
    _, r_req = evaluate([cr("b", "COMPLETED", "SUCCESS")], req)
    checks.append(("required-missing-reason-names-check", "Lint" in r_req))
    _, r_pend_req = evaluate([cr("b", "IN_PROGRESS", None)], req)
    checks.append(("pending-reason-names-unreported-required", "not yet reported as a CheckRun: Lint" in r_pend_req))
    _, r_green = evaluate([cr("Lint", "COMPLETED", "SUCCESS")], req)
    checks.append(("green-reason-names-required", "required: Lint" in r_green))
    _, r_none = evaluate([cr("Lint", "COMPLETED", "SUCCESS")])
    checks.append(("green-reason-says-none-required", "required: none" in r_none))
    _, r_fail_req = evaluate([cr("b", "COMPLETED", "FAILURE")], req)
    checks.append(("failing-reason-names-unreported-required", "not yet reported as a CheckRun: Lint" in r_fail_req))
    _, r_coll = evaluate([cr("Lint", "COMPLETED", "SUCCESS"), sc("Lint", "SUCCESS")], req)
    checks.append(("collision-reason-says-collision", "name collision" in r_coll))
    # main() passes the default required checks through (3b104 QA r2): drive it with a stubbed gh.
    import contextlib as _cl, io as _io
    lint = REQUIRED_CHECKS[0]
    rollups = {
        "skipped": [cr(lint, "COMPLETED", "SKIPPED")] + [cr(n, "COMPLETED", "SUCCESS") for n in REQUIRED_CHECKS[1:]],
        "green": [cr(n, "COMPLETED", "SUCCESS") for n in REQUIRED_CHECKS],
    }
    head = "3f0c9e71a2b48d5609ce17f4b23a8d60e95c1b7a"  # realistic, so a hard-coded SHA cannot coincide
    def view(r, h=head, fields=None, state="OPEN"):
        # Only the requested --json fields come back, as from the real gh (3b106 QA r3).
        full = {"state": state, "statusCheckRollup": r, "headRefOid": h, "number": 1, "title": "t"}
        wanted = full.keys() if fields is None else [f for f in fields.split(",") if f]
        return json.dumps({k: full[k] for k in wanted if k in full})
    json_arg = lambda a: a[a.index("--json") + 1] if "--json" in a else ""
    real_gh = globals()["gh"]
    try:
        # Inside the stub, so even a mutated file that allows abbreviations never calls the real gh (3b104 r6).
        globals()["gh"] = lambda *a: view(rollups["green"], fields=json_arg(a))
        with _cl.redirect_stdout(_io.StringIO()), _cl.redirect_stderr(_io.StringIO()):
            try:
                main(["merge-when-green.py", "1", "--require-n", "--dry-run"])
                abbrev_refused = False
            except SystemExit as exc:
                abbrev_refused = exc.code == 2
        checks.append(("abbreviated-require-none-refused", abbrev_refused))
        for label, want_rc in (("skipped", 1), ("green", 0)):
            globals()["gh"] = lambda *a, _r=rollups[label]: view(_r, fields=json_arg(a))
            with _cl.redirect_stdout(_io.StringIO()), _cl.redirect_stderr(_io.StringIO()):
                rc = main(["merge-when-green.py", "1", "--dry-run"])
            checks.append((f"main-default-required-{label}", rc == want_rc))
        # --require replaces the list and must be enforced; --require-none must reach evaluate() as ()
        # (3b104 QA r3): a custom name missing from a green rollup refuses, and require-none passes it.
        globals()["gh"] = lambda *a: view(rollups["green"], fields=json_arg(a))
        for label, flags, want_rc in (("require-custom-missing", ["--require", "Custom check"], 1),
                                      ("require-custom-present", ["--require", lint], 0)):
            with _cl.redirect_stdout(_io.StringIO()), _cl.redirect_stderr(_io.StringIO()):
                rc = main(["merge-when-green.py", "1", "--dry-run", *flags])
            checks.append((f"main-{label}", rc == want_rc))
        globals()["gh"] = lambda *a: view(rollups["skipped"], fields=json_arg(a))
        with _cl.redirect_stdout(_io.StringIO()), _cl.redirect_stderr(_io.StringIO()):
            rc = main(["merge-when-green.py", "1", "--dry-run", "--require-none"])
        checks.append(("main-require-none-skips-required", rc == 0))
        # 3b106: the real merge call carries the evaluated head; a missing or short SHA refuses.
        calls = []
        def rec(*a, _h=head):
            calls.append(a)
            if a[:2] != ("pr", "view"):
                return ""
            # Any later read sees a moved head, so a re-read before the merge cannot match the pin (3b106 QA r2).
            seen = sum(1 for c in calls if c[:2] == ("pr", "view"))
            return view(rollups["green"], _h if seen == 1 or _h != head else "b" * 40, json_arg(a))
        def pinned(m):
            m = list(m)
            return "--match-head-commit" in m and m[m.index("--match-head-commit") + 1] == head
        # Both merge paths, plain and --admin (the working path), carry the pin (3b106 QA r1).
        for label, extra in (("plain", []), ("admin", ["--admin"])):
            calls.clear()
            globals()["gh"] = rec
            with _cl.redirect_stdout(_io.StringIO()), _cl.redirect_stderr(_io.StringIO()):
                rc = main(["merge-when-green.py", "1", *extra])
            merges = [a for a in calls if a[:2] == ("pr", "merge")]
            views = [a for a in calls if a[:2] == ("pr", "view")]
            checks.append((f"merge-pins-evaluated-head-{label}", rc == 0 and len(merges) == 1 and pinned(merges[0])
                           and len(views) == 1 and (("--admin" in merges[0]) == bool(extra))))
        # A missing, short, upper-case or non-hex head refuses, with no merge call, also on a dry run.
        for label, bad in (("missing", None), ("short", "abc123"), ("upper", "A" * 40), ("nonhex", "g" * 40)):
            for dry in ([], ["--dry-run"]):
                calls.clear()
                globals()["gh"] = lambda *a, _b=bad: rec(*a, _h=_b)
                with _cl.redirect_stdout(_io.StringIO()), _cl.redirect_stderr(_io.StringIO()):
                    rc = main(["merge-when-green.py", "1", *dry])
                merged = any(a[:2] == ("pr", "merge") for a in calls)
                checks.append((f"head-{label}-refused{'-dry' if dry else ''}", rc == 1 and not merged))
        for state in ("MERGED", "CLOSED"):
            calls.clear()
            def rec_state(*a, _s=state):
                calls.append(a)  # every call, a merge included, is recorded before dispatch
                return view(rollups["green"], head, json_arg(a), _s) if a[:2] == ("pr", "view") else ""
            globals()["gh"] = rec_state
            with _cl.redirect_stdout(_io.StringIO()), _cl.redirect_stderr(_io.StringIO()):
                rc = main(["merge-when-green.py", "1"])
            checks.append((f"not-open-{state.lower()}-refused",
                           rc == 1 and not any(c[:2] == ("pr", "merge") for c in calls)))
        # Inside the stub too, so a mutated parser that accepted both flags never reaches the real gh (3b106 QA r1).
        calls.clear()
        globals()["gh"] = rec
        with _cl.redirect_stdout(_io.StringIO()), _cl.redirect_stderr(_io.StringIO()):
            try:
                main(["merge-when-green.py", "1", "--require", "Lint", "--require-none", "--dry-run"])
                both_refused = False
            except SystemExit as exc:
                both_refused = exc.code == 2
        checks.append(("require-and-require-none-conflict-refused", both_refused and not calls))
    finally:
        globals()["gh"] = real_gh
    # The exact default list is pinned: the main() cases build rollups from REQUIRED_CHECKS itself, so
    # they cannot notice a name dropped from it (3b104 QA r4).
    checks.append(("default-required-list-exact",
                   REQUIRED_CHECKS == ("Lint markdown corpus", "PR attribution (title and body)")))
    _, r_status_only = evaluate([sc("Lint", "SUCCESS")], ("Lint",))
    checks.append(("status-only-reason-says-not-a-checkrun", "not reported as a CheckRun: Lint" in r_status_only))
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
    # No abbreviations: `--require-n` must not silently become --require-none (3b104 QA r5).
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0], allow_abbrev=False)
    ap.add_argument("pr", nargs="?", help="PR number")
    ap.add_argument("--repo", help="owner/name (defaults to the current repo's remote)")
    ap.add_argument("--merge-method", default="squash", choices=["squash", "merge", "rebase"])
    ap.add_argument("--admin", action="store_true", help="pass --admin (REVIEW_REQUIRED bypass) to gh pr merge")
    ap.add_argument("--dry-run", action="store_true", help="report the verdict; do NOT merge")
    group = ap.add_mutually_exclusive_group()  # both at once would silently drop NAME (3b104 QA r1)
    group.add_argument("--require", action="append", metavar="NAME",
                       help="a check that must be present and SUCCESS (repeatable; replaces the default list)")
    group.add_argument("--require-none", action="store_true",
                       help="require no named check (for a repository without the default checks)")
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
                 "--json", "statusCheckRollup,number,title,state,headRefOid")
        view = json.loads(raw)
    except (subprocess.CalledProcessError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: gh pr view failed: {exc}", file=sys.stderr)
        return 2
    if view.get("state") != "OPEN":
        print(f"REFUSE: PR #{args.pr} is {view.get('state')}, not OPEN.", file=sys.stderr)
        return 1
    # The merge is pinned to the head these checks describe, so a push landing between this read and
    # the merge cannot be merged unchecked (3b106).
    head = view.get("headRefOid")
    if not (isinstance(head, str) and len(head) == 40 and all(ch in "0123456789abcdef" for ch in head)):
        print(f"REFUSE: PR #{args.pr} did not report a full head commit SHA ({head!r}); cannot pin the merge.",
              file=sys.stderr)
        return 1
    required = () if args.require_none else tuple(args.require or REQUIRED_CHECKS)
    green, reason = evaluate(view.get("statusCheckRollup") or [], required)
    if not green:
        print(f"REFUSE to merge PR #{args.pr}: {reason}", file=sys.stderr)
        return 1
    print(f"PR #{args.pr} is GREEN at {head[:12]}: {reason}")
    if args.dry_run:
        print("--dry-run: not merging.")
        return 0
    merge = ["pr", "merge", args.pr, *repo_args, f"--{args.merge_method}", "--match-head-commit", head]
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
