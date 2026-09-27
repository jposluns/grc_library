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
SUCCESS: NEUTRAL or SKIPPED passes only for the other checks (3b104). A required name listed in
REQUIRED_WORKFLOWS counts only from that workflow, so a same-named job elsewhere cannot stand in (3b105).
The merge is pinned to the head commit it evaluated (gh pr merge --match-head-commit), so a push
landing after the read is never merged unchecked; a missing head SHA refuses (3b106).
It also applies the open-findings guard's own decision before merging, so an undispositioned
`error` finding refuses the merge however the tool was started (3b108).

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
import re
import subprocess
import sys

_OK_CONCLUSION = {"SUCCESS", "NEUTRAL", "SKIPPED"}  # a CheckRun that finished acceptably
_OK_STATE = {"SUCCESS"}  # a legacy StatusContext that finished acceptably
# Checks that must be PRESENT and SUCCESS: NEUTRAL or SKIPPED is acceptable for any other check,
# never for these, so a skipped corpus lint cannot read as green (3b104).
REQUIRED_CHECKS = ("Lint markdown corpus", "PR attribution (title and body)")
# The workflow each default required check comes from: a same-named job in another workflow must not
# stand in for it (3b105). The binding applies to these names however they are required (the default list
# or --require); any other --require name is matched by name only. RESIDUE: a workflow name is not unique
# and a PR runs its own workflow files, so this stops an accidental or foreign same-named job, not a PR
# that edits or adds a workflow under this name; every bound entry must still succeed, and the
# workflow-file review is the control for that.
REQUIRED_WORKFLOWS = {"Lint markdown corpus": "Repository quality checks",
                      "PR attribution (title and body)": "PR attribution"}
_REPO_ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]


def evaluate(rollup: list[dict], required: tuple[str, ...] = (), workflows: dict | None = None) -> tuple[bool, str]:
    """PURE decision over a GitHub ``statusCheckRollup``: (green, reason). Fails CLOSED:
    green ONLY when at least one check exists and EVERY check is terminal-success with none
    pending; a no-checks, any-pending, any-failing, or unknown-shape check REFUSES. Each name
    in ``required`` must also be reported and must have concluded SUCCESS itself (3b104); where
    ``workflows`` names its workflow, only a CheckRun from that workflow counts (3b105)."""
    workflows = workflows or {}

    def bound(c: dict, want: str) -> bool:
        return (c.get("__typename") == "CheckRun" and c.get("name") == want
                and (want not in workflows or c.get("workflowName") == workflows[want]))
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
    absent = [w for w in required if not any(bound(c, w) for c in rollup if isinstance(c, dict))]
    def unreported(w: str) -> str:
        return f"{w} (from workflow {workflows[w]!r})" if w in workflows else w
    note = ("; required check(s) not yet reported as a CheckRun: "
            + ", ".join(unreported(w) for w in absent)) if absent else ""
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
            return False, f"required check not reported as a CheckRun: {unreported(want)}"
        for c in rollup:
            if (c.get("name") or c.get("context")) == want and c.get("__typename") != "CheckRun":
                return False, (f"required check {want} is also reported as a commit status of the same name "
                               "(a name collision); only the CheckRun may satisfy it")
            if c.get("__typename") == "CheckRun" and c.get("name") == want and not bound(c, want):
                return False, (f"required check {want} is also reported by workflow {c.get('workflowName')!r}, "
                               f"not only {workflows[want]!r} (a name collision); only its own workflow may satisfy it")
            if bound(c, want) and c.get("conclusion") != "SUCCESS":
                return False, f"required check did not succeed: {want} [{c.get('conclusion')}]"
    verified = ", ".join(required) if required else "none"
    return True, f"all {len(rollup)} check(s) completed successfully; required: {verified}"


class _Unreadable(Exception):
    """A construct the strict workflow reader does not handle; the pin then fails closed (3b105 QA r3)."""


def _yaml_scalar(raw: str) -> str:
    """A single-line YAML scalar: plain (an inline ` #` comment dropped), single-quoted (a doubled quote is
    a literal quote), or double-quoted without escapes. Anything else raises _Unreadable rather than
    returning a guess, so a misread can only fail the pin, never pass it (3b105 QA r2, r3)."""
    s = raw.strip(" ")  # YAML whitespace is the space (tabs are refused); Unicode spaces are content (r4)
    if s.startswith("#"):
        return ""  # only a comment follows the key
    if s[:1] in ("{", "[", "|", ">", "&", "*", "!"):
        raise _Unreadable(f"unsupported scalar form: {s[:20]!r}")
    if s[:1] == "'":
        out, i = [], 1
        while i < len(s):
            if s[i] == "'":
                if s[i + 1:i + 2] == "'":
                    out.append("'")
                    i += 2
                    continue
                rest = s[i + 1:].strip(" ")
                if rest and not rest.startswith("#"):
                    raise _Unreadable("text after a quoted scalar")
                return "".join(out)
            out.append(s[i])
            i += 1
        raise _Unreadable("unterminated single-quoted scalar")
    if s[:1] == '"':
        end = s.find('"', 1)
        if end < 0 or "\\" in s[:end]:
            raise _Unreadable("unterminated or escaped double-quoted scalar")
        rest = s[end + 1:].strip(" ")
        if rest and not rest.startswith("#"):
            raise _Unreadable("text after a quoted scalar")
        return s[1:end]
    cut = s.find(" #")
    return (s[:cut] if cut >= 0 else s).strip(" ")


def _check_value(value: str) -> None:
    """Refuse a value the reader cannot bound to its own line: a flow collection or an unterminated quote
    could carry a `name:` on a later line (3b105 QA r3)."""
    v = value.strip(" ")
    if v[:1] in ("{", "["):
        raise _Unreadable("flow collection inside jobs")
    if v[:1] in ("&", "*", "!"):  # an anchor can front a flow collection or a quote (3b105 QA r4)
        raise _Unreadable("anchor, alias or tag inside jobs")
    if v[:1] in ("'", '"'):
        _yaml_scalar(v)


def workflow_names(text: str) -> tuple[str | None, set[str]]:
    """(top-level name, set of job names) from a workflow file, read with the stdlib: the top-level `name:`
    and the `name:` of each job directly under `jobs:`, at the indentation of that job's own properties, so
    a step's or an env block's `name:` is not taken for a job name (3b105 QA r2). Constructs it recognizes
    as outside its grammar (a tab; inside jobs a flow collection, an anchor, alias or tag, an unterminated
    or escaped quote; a quote left open at the top level; a name continued on the next line; a duplicate
    name) make it return (None, set()), so the pin fails on them (3b105 QA r3, r4). Block-scalar bodies
    are skipped.
    RESIDUE, stated: this is an early-warning pin for a plain rename, NOT a YAML parser. Constructs it
    does not recognize (for example a duplicate non-name key, whose last value YAML keeps) can still
    mislead it in either direction. That delays detection, never a wrong merge: evaluate() refuses at
    merge time whenever GitHub reports the required job under another name or workflow."""
    try:
        return _workflow_names(text)
    except _Unreadable:
        return None, set()


def _workflow_names(text: str) -> tuple[str | None, set[str]]:
    if "\t" in text:
        raise _Unreadable("tab")
    top, jobs = None, set()
    in_jobs, key_indent, prop_indent, job_named = False, None, None, False
    block_indent = None  # indentation of a key whose block-scalar body is being skipped
    name_at = None  # indentation of the name line just read: a deeper next line would continue it (r4)
    for line in text.splitlines():
        if not line.strip(" ") or line.lstrip(" ").startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if block_indent is not None:
            if indent > block_indent:
                continue
            block_indent = None
        if name_at is not None and indent > name_at:
            raise _Unreadable("a name continued on the next line")
        name_at = None
        stripped = line.strip(" ")
        is_item = stripped.startswith("- ")
        item = stripped[2:].lstrip() if is_item else stripped
        key, sep, value = item.partition(":")
        is_key = bool(sep) and bool(key) and not key.startswith(("-", "'", '"')) and (value[:1] in ("", " "))
        if is_key and re.match(r"[|>][-+0-9]*\s*(#.*)?$", value.strip() or "x"):
            block_indent = indent
        if indent == 0:
            if not is_key:
                raise _Unreadable("top-level line that is not a key")
            in_jobs = key == "jobs"
            key_indent = prop_indent = None
            if in_jobs and _yaml_scalar(value) if value.strip(" ") else False:
                raise _Unreadable("jobs: with a value on its own line")
            if value.strip(" ")[:1] in ("'", '"'):
                _yaml_scalar(value)  # a quote left open could hide a fake jobs block (3b105 QA r4)
            if key == "name":
                if top is not None:
                    raise _Unreadable("duplicate top-level name")
                top = _yaml_scalar(value)
                name_at = indent
            continue
        if not in_jobs:
            continue
        if is_key and value.strip():
            _check_value(value)
        elif is_item:
            _check_value(item)
        if key_indent is None:
            key_indent = indent
        if indent < key_indent:
            raise _Unreadable("line outdented past the job keys")
        if indent == key_indent:
            if is_item or not (is_key and not value.strip()):
                raise _Unreadable("job entry that is not a block mapping")
            prop_indent, job_named = None, False
            continue
        if prop_indent is None:
            prop_indent = indent
        if indent == prop_indent and is_key and not is_item and key == "name":
            if job_named:
                raise _Unreadable("duplicate job name")
            jobs.add(_yaml_scalar(value))
            job_named = True
            name_at = indent
    return top, jobs


def pin_ok(text: str, check: str) -> bool:
    """The workflow file names the check's workflow at the top level and carries a job of that name."""
    top, jobs = workflow_names(text)
    return top == REQUIRED_WORKFLOWS[check] and check in jobs


def open_findings_block(root, ledger=None) -> tuple[int, str]:
    """(exit code, message) from the open-findings guard's own decision on the ledger (3b108).

    The PreToolUse hook that refuses a merge while an `error` finding is undispositioned matches the
    shell command text, which a merge through this tool can evade in many shell forms; checking here
    makes the rule hold for every invocation. It reuses the hook's parse and decision functions, so the
    two can never disagree. No hook file (an adopter checkout) or no readable ledger allows, matching the
    hook's fail-open posture; a hook file that exists but cannot be loaded REFUSES (ignorance refuses)."""
    import contextlib
    import importlib.util
    import io
    from pathlib import Path
    hook = Path(root) / ".claude" / "hooks" / "block-on-open-findings.py"
    if not hook.is_file():
        return 0, ""
    try:
        spec = importlib.util.spec_from_file_location("_mwg_open_findings", hook)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        path = ledger if ledger is not None else mod._working_file("open-findings.md", Path(root))
    except Exception as exc:  # noqa: BLE001 - any load failure refuses
        return 1, f"the open-findings guard could not be loaded ({exc}); refusing to merge unchecked"
    if path is None:
        return 0, ""
    try:
        text = Path(path).read_text(encoding="utf-8")
        rows = mod.parse_open_rows(text)
    except Exception:  # noqa: BLE001 - an unreadable ledger allows, as in the hook
        return 0, ""
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        code = mod.decide_exit(rows, text)
    return (1 if code else 0), err.getvalue().strip()


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
    crw = lambda n, s, c: dict(cr(n, s, c), workflowName=REQUIRED_WORKFLOWS.get(n))
    rollups = {
        "skipped": [crw(lint, "COMPLETED", "SKIPPED")] + [crw(n, "COMPLETED", "SUCCESS") for n in REQUIRED_CHECKS[1:]],
        "green": [crw(n, "COMPLETED", "SUCCESS") for n in REQUIRED_CHECKS],
        # 3b105 QA r1: main() must hand the workflow map to evaluate(); these pass on names alone.
        "foreign": [dict(cr(n, "COMPLETED", "SUCCESS"), workflowName="Other") for n in REQUIRED_CHECKS],
        "no-workflow": [cr(n, "COMPLETED", "SUCCESS") for n in REQUIRED_CHECKS],
        "collision": [crw(n, "COMPLETED", "SUCCESS") for n in REQUIRED_CHECKS]
                     + [dict(cr(lint, "COMPLETED", "SUCCESS"), workflowName="Other")],
    }
    head = "3f0c9e71a2b48d5609ce17f4b23a8d60e95c1b7a"  # realistic, so a hard-coded SHA cannot coincide
    def view(r, h=head, fields=None, state="OPEN"):
        # Only the requested --json fields come back, as from the real gh (3b106 QA r3).
        full = {"state": state, "statusCheckRollup": r, "headRefOid": h, "number": 1, "title": "t"}
        wanted = full.keys() if fields is None else [f for f in fields.split(",") if f]
        return json.dumps({k: full[k] for k in wanted if k in full})
    json_arg = lambda a: a[a.index("--json") + 1] if "--json" in a else ""
    real_gh = globals()["gh"]
    real_block = globals()["open_findings_block"]
    # The stubbed main() cases must not depend on the live ledger: the check is stubbed here and tested
    # on its own below with fixture ledgers (3b108).
    globals()["open_findings_block"] = lambda root, ledger=None: (0, "")
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
        for label, want_rc in (("skipped", 1), ("green", 0), ("foreign", 1), ("no-workflow", 1), ("collision", 1)):
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
        # A default name named through --require still binds to its workflow (3b105 QA r1).
        globals()["gh"] = lambda *a: view(rollups["foreign"], fields=json_arg(a))
        with _cl.redirect_stdout(_io.StringIO()), _cl.redirect_stderr(_io.StringIO()):
            rc = main(["merge-when-green.py", "1", "--dry-run", "--require", lint])
        checks.append(("main-require-default-name-foreign-workflow", rc == 1))
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
        # A dry run on a green PR reports and never merges, with or without --admin (3b106 QA r4).
        for extra in ([], ["--admin"]):
            calls.clear()
            globals()["gh"] = rec
            with _cl.redirect_stdout(_io.StringIO()), _cl.redirect_stderr(_io.StringIO()):
                rc = main(["merge-when-green.py", "1", "--dry-run", *extra])
            checks.append((f"dry-run-never-merges{'-admin' if extra else ''}",
                           rc == 0 and not any(c[:2] == ("pr", "merge") for c in calls)))
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
        # A blocked ledger stops main() before any merge, on a dry run too (3b108).
        globals()["open_findings_block"] = lambda root, ledger=None: (1, "an open error finding")
        for dry in ([], ["--dry-run"]):
            calls.clear()
            globals()["gh"] = rec
            with _cl.redirect_stdout(_io.StringIO()), _cl.redirect_stderr(_io.StringIO()):
                rc = main(["merge-when-green.py", "1", "--admin", *dry])
            checks.append((f"open-finding-blocks-main{'-dry' if dry else ''}",
                           rc == 1 and not any(c[:2] == ("pr", "merge") for c in calls)))
    finally:
        globals()["gh"] = real_gh
        globals()["open_findings_block"] = real_block
    # 3b108: the tool applies the open-findings guard itself, with the hook's own decision.
    import tempfile as _tf
    from pathlib import Path as _P
    with _tf.TemporaryDirectory() as _d:
        led = _P(_d) / "open-findings.md"
        head_rows = "## Open\n| Date | Severity | Finding | Source | Disposition |\n| --- | --- | --- | --- | --- |\n"
        led.write_text(head_rows + "| 2026-09-27 | error | a live defect | probe |  |\n", encoding="utf-8")
        code, msg = open_findings_block(_REPO_ROOT, led)
        checks.append(("open-error-refuses-merge", code == 1 and "a live defect" in msg))
        led.write_text(head_rows + "| 2026-09-27 | error | a fixed defect | probe | FIXED #1 |\n", encoding="utf-8")
        checks.append(("dispositioned-error-allows", open_findings_block(_REPO_ROOT, led)[0] == 0))
        checks.append(("no-hook-allows", open_findings_block(_P(_d), led)[0] == 0))
        broken = _P(_d) / ".claude" / "hooks"
        broken.mkdir(parents=True)
        (broken / "block-on-open-findings.py").write_text("raise RuntimeError('broken')\n", encoding="utf-8")
        checks.append(("unloadable-guard-refuses", open_findings_block(_P(_d), led)[0] == 1))
    # 3b105: a required check binds to its workflow; a same-named job from another workflow refuses.
    wf = {"Lint": "Repository quality checks"}
    for name, rollup, want_green in [
        ("workflow-bound-green", [dict(cr("Lint", "COMPLETED", "SUCCESS"), workflowName="Repository quality checks")], True),
        ("workflow-missing-refused", [cr("Lint", "COMPLETED", "SUCCESS")], False),
        ("workflow-other-only-refused", [dict(cr("Lint", "COMPLETED", "SUCCESS"), workflowName="Other")], False),
        ("workflow-collision-refused", [dict(cr("Lint", "COMPLETED", "SUCCESS"), workflowName="Repository quality checks"),
                                        dict(cr("Lint", "COMPLETED", "SUCCESS"), workflowName="Other")], False),
    ]:
        checks.append((name, evaluate(rollup, ("Lint",), wf)[0] == want_green))
    checks.append(("default-workflows-exact", REQUIRED_WORKFLOWS == {
        "Lint markdown corpus": "Repository quality checks", "PR attribution (title and body)": "PR attribution"}))
    # The map matches the workflow files themselves (3b105 QA r1): each file's top-level name, and a job
    # carrying the required check's name. A rename in either file fails here, not first at merge time.
    wf_files = {"Lint markdown corpus": "quality.yml", "PR attribution (title and body)": "pr-attribution.yml"}
    for check, fname in wf_files.items():
        try:
            text = (_REPO_ROOT / ".github" / "workflows" / fname).read_text(encoding="utf-8")
        except OSError:
            text = ""
        checks.append((f"workflow-file-{fname}", pin_ok(text, check)))
    # The reader takes job names only, and reads quoted and commented scalars (3b105 QA r2).
    wf = ("name: \"Repository quality checks\"  # quoted\non:\n  pull_request:\njobs:\n  lint:\n"
          "    name: 'Lint markdown corpus' # commented\n    runs-on: x\n    env:\n      name: Env name\n"
          "    steps:\n      - name: Step name\n        uses: a\n      - uses: b\n        name: Mapped step\n"
          "  other:\n    name: Other job\n# name: Commented out\n")
    checks.append(("workflow-reader-jobs-only", workflow_names(wf) == ("Repository quality checks",
                                                                      {"Lint markdown corpus", "Other job"})))
    nested_only = "name: W\njobs:\n  lint:\n    name: Renamed\n    env:\n      name: Lint markdown corpus\n"
    checks.append(("workflow-reader-nested-name-not-a-job", "Lint markdown corpus" not in workflow_names(nested_only)[1]))
    # 3b105 QA r3: the pin fails on each way the job or workflow can be absent, and the strict reader fails
    # closed on every construct it cannot bound (codex and claude fail-open reproductions included).
    lint_ = "Lint markdown corpus"
    good = "name: Repository quality checks\njobs: # CI\n  lint:\n    name: Lint markdown corpus # plain\n    runs-on: x\n"
    checks.append(("pin-good", pin_ok(good, lint_)))
    for label, text in (
        ("renamed-top", good.replace("name: Repository quality checks", "name: Other")),
        ("renamed-job", good.replace("name: Lint markdown corpus", "name: Renamed")),
        ("empty-file", ""),
        ("flow-env", "name: Repository quality checks\njobs:\n  lint:\n    name: Renamed\n    env: {A: 1,\n"
                     "    name: Lint markdown corpus\n    }\n"),
        ("flow-job", "name: Repository quality checks\njobs:\n  lint: {name: Renamed, env: {\n"
                     "    name: Lint markdown corpus}}\n"),
        ("open-quote-if", "name: Repository quality checks\njobs:\n  lint:\n    name: Renamed\n    if: \"a &&\n"
                          "    name: Lint markdown corpus\n    && b\"\n"),
        ("doubled-quote", "name: Repository quality checks\njobs:\n  lint:\n    name: 'Lint markdown corpus'' renamed'\n"),
        ("doubled-quote-top", good.replace("name: Repository quality checks", "name: 'Repository quality checks'' x'")),
        ("duplicate-job-name", good.replace("    runs-on: x\n", "    name: Renamed\n    runs-on: x\n")),
        ("tab", good.replace("    runs-on", "\trun")),
        ("mixed-job-indent", "name: Repository quality checks\njobs:\n  a:\n      name: A\n  lint:\n    name: Renamed\n"
                             "    env:\n      name: Lint markdown corpus\n"),
        ("flow-env-unnamed", "name: Repository quality checks\njobs:\n  lint:\n    runs-on: x\n    env: {A: 1,\n"
                             "    name: Lint markdown corpus\n    }\n"),
        ("open-quote-unnamed", "name: Repository quality checks\njobs:\n  lint:\n    runs-on: x\n    if: 'a &&\n"
                               "    name: Lint markdown corpus\n    && b'\n"),
        ("second-top-after-jobs", "name: Repository quality checks\njobs:\n  lint:\n    name: Renamed\nenv:\n"
                                  "  lint:\n    name: Lint markdown corpus\n"),
    ):
        checks.append((f"pin-refuses-{label}", not pin_ok(text, lint_)))
    block = good + "    steps:\n      - run: |\n          name: Lint markdown corpus\n          note: 'it\n"
    checks.append(("pin-block-scalar-body-skipped", pin_ok(block, lint_)))
    checks.append(("reader-plain-comment", workflow_names(good)[1] == {lint_}))
    odd = "name: W\njobs:\n  a:\n    name: 'Lint''s job'\n  b:\n    name: C#-lint # c\n"
    # 3b105 QA r4: fail-open reproductions from all three families, each now refused.
    H_ = "name: Repository quality checks\non: push\n"
    for label, text in (
        ("folded-job-name", H_ + "jobs:\n  lint:\n    name: Lint markdown corpus\n      renamed\n"),
        ("folded-top-name", "name: Repository quality checks\n  renamed\njobs:\n  lint:\n    name: Lint markdown corpus\n"),
        ("anchored-flow", H_ + "jobs:\n  lint:\n    env: &e {A: 1,\n    name: Lint markdown corpus\n    }\n"),
        ("anchored-quote", H_ + "jobs:\n  lint:\n    if: &q 'a\n    name: Lint markdown corpus\n    b'\n"),
        ("unicode-space", H_ + "jobs:\n  lint:\n    name: Lint markdown corpus\u00a0\n"),
        ("jobs-with-value", H_ + "jobs: &j\n  lint:\n    name: Lint markdown corpus\n"),
        ("open-quote-top", "name: Repository quality checks\nenv: 'x\njobs:\n  lint:\n    name: Lint markdown corpus\n'\n"),
    ):
        checks.append((f"pin-refuses-{label}", not pin_ok(text, lint_)))
    # Defence in depth: where PyYAML is importable, every text the pin accepts must read the same there.
    try:
        import yaml as _yaml
    except ImportError:
        _yaml = None
    if _yaml is not None:
        accepted = [good, block] + [(_REPO_ROOT / ".github" / "workflows" / f).read_text(encoding="utf-8")
                                    for f in wf_files.values()]
        for i, text in enumerate(accepted):
            doc = _yaml.safe_load(text) or {}
            want = (doc.get("name"), {j.get("name") for j in (doc.get("jobs") or {}).values() if isinstance(j, dict)} - {None})
            checks.append((f"pyyaml-agrees-{i}", workflow_names(text) == want))
    checks.append(("reader-doubled-quote-and-plain-hash", workflow_names(odd) == ("W", {"Lint's job", "C#-lint"})))
    _, r_foreign = evaluate([dict(cr("Lint", "COMPLETED", "SUCCESS"), workflowName="Other")], ("Lint",),
                            {"Lint": "Repository quality checks"})
    checks.append(("foreign-reason-names-workflow", "from workflow 'Repository quality checks'" in r_foreign))
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
                       help="a check that must be present and SUCCESS (repeatable; replaces the default list; a default "
                            "check name still binds to its workflow)")
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
    workflows = REQUIRED_WORKFLOWS  # a default name binds to its workflow even via --require (3b105 QA r1)
    green, reason = evaluate(view.get("statusCheckRollup") or [], required, workflows)
    if not green:
        print(f"REFUSE to merge PR #{args.pr}: {reason}", file=sys.stderr)
        return 1
    blocked, why = open_findings_block(_REPO_ROOT)
    if blocked:
        print(f"REFUSE to merge PR #{args.pr}: {why}", file=sys.stderr)
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
