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
A repository listed in ACTIONS_FALLBACK, whose token cannot read Checks (its rollup then carries no
CheckRun), is decided instead from the GitHub Actions runs for the evaluated head: every run completed
success and each listed workflow ran from its own file on a pull_request event; anything the fallback
cannot confirm refuses, and the merge stays pinned to that head (3b132). Where that token cannot read the
rollup at all, so the rollup query fails with exactly the GraphQL permission error on it, the PR is read
again without the rollup and decided the same way; any other gh failure, and any unlisted repository,
still stops (3b132 QA r1).

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
# Repositories whose token cannot read Checks, so the PR's rollup carries no CheckRun: there the verdict
# falls back to the Actions runs for the head commit, and each workflow listed (its top-level name, bound
# to its file) must be among them (3b132). An unlisted repository never falls back, so an empty rollup
# there still refuses; --repo must be given, spelled exactly as here. RESIDUE: see evaluate_runs().
ACTIONS_FALLBACK = {"jposluns/grc_library_ref": {"validate": ".github/workflows/validate.yml"}}
_FALLBACK_EVENT = "pull_request"  # a required workflow counts only from a run on this event
# The one gh failure that engages the fallback before any rollup is read (3b132 QA r1): the token cannot read
# the rollup's contexts, so `gh pr view --json statusCheckRollup,...` exits 1 with exactly this one line on
# stderr (the reality fixture, jposluns/grc_library_ref #181). Anything else, an added line included, is not it.
_ROLLUP_FORBIDDEN = re.compile(r"GraphQL: Resource not accessible by personal access token "
                               r"\(repository\.pullRequest\.statusCheckRollup(?:\.[A-Za-z0-9_]+)*\)")
_VIEW_FIELDS = "number,title,state,headRefOid"  # the PR read again without its rollup
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


def evaluate_runs(payload, head: str, workflows: dict) -> tuple[bool, str]:
    """PURE decision over a GitHub Actions ``GET repos/<repo>/actions/runs?head_sha=<head>`` response, the
    fallback for a repository whose token cannot read Checks (3b132): (green, reason). Fails CLOSED: green
    ONLY when the response is a recognized, complete page, every run is for ``head``, every run completed
    with conclusion ``success`` (a run carries no per-job detail, so skipped or neutral refuses here too),
    and each workflow in ``workflows`` has a run from its own file on a pull_request event. No workflow
    configured, no runs, a truncated page, a run for another commit, a same-named run from another file,
    or an unrecognized entry REFUSES.
    RESIDUE, stated: the runs API lists Actions workflow runs only. Check runs from other apps, and any
    commit status the rollup did not show, are invisible here, as are a workflow that has not yet created
    its run, the jobs inside a run (a job skipped by an `if:` leaves its run a success), and which PR a
    run belongs to (another PR with the same head commit shares its runs). As with REQUIRED_WORKFLOWS, a
    PR that edits the bound workflow file is caught by workflow-file review, not here."""
    if not workflows:
        return False, "no required workflow configured for the Actions-runs fallback"
    total = payload.get("total_count") if isinstance(payload, dict) else None
    runs = payload.get("workflow_runs") if isinstance(payload, dict) else None
    if not isinstance(runs, list) or type(total) is not int:
        return False, "the Actions runs response has an unrecognized shape (fail-closed refuse)"
    if total != len(runs):
        return False, f"the Actions runs response lists {len(runs)} of {total} run(s); cannot see them all"
    if not runs:
        return False, f"no Actions workflow runs reported for {head[:12]} (never merge on no-checks)"
    pending: list[str] = []
    failed: list[str] = []
    unknown: list[str] = []
    for r in runs:
        if not (isinstance(r, dict) and isinstance(r.get("name"), str) and r["name"]):
            unknown.append(f"<unrecognized run entry: {r!r:.60}>")
            continue
        label = f"{r['name']} (run {r.get('id')})"
        if r.get("head_sha") != head:
            unknown.append(f"{label} [for commit {r.get('head_sha')!r}, not the evaluated head]")
        elif r.get("status") != "completed":
            pending.append(f"{label} [{r.get('status') or 'no-status'}]")
        elif r.get("conclusion") != "success":
            failed.append(f"{label} [{r.get('conclusion') or 'no-conclusion'}]")
    if failed or unknown:
        parts: list[str] = []
        if failed:
            parts.append("failing / non-success run(s): " + ", ".join(failed))
        if unknown:
            parts.append("UNRECOGNIZED run(s) (fail-closed refuse): " + ", ".join(unknown))
        if pending:
            parts.append("pending: " + ", ".join(pending))
        return False, "; ".join(parts)
    if pending:
        return False, "pending / incomplete run(s): " + ", ".join(pending)
    for want, path in workflows.items():
        named = [r for r in runs if r["name"] == want]
        if not named:
            return False, f"required workflow not among the Actions runs: {want} (from {path})"
        foreign = [r for r in named if r.get("path") != path]
        if foreign:
            return False, (f"required workflow {want} is also reported from {foreign[0].get('path')!r}, not only "
                           f"{path!r} (a name collision); only its own file may satisfy it")
        if not any(r.get("event") == _FALLBACK_EVENT for r in named):
            return False, f"required workflow {want} has no {_FALLBACK_EVENT} run for this head"
    return True, (f"all {len(runs)} Actions run(s) for {head[:12]} completed successfully; required workflow(s): "
                  + ", ".join(workflows) + " (Actions-runs fallback: the check rollup carried no CheckRun)")


def rollup_forbidden(exc: BaseException) -> bool:
    """PURE: whether a failed gh call is exactly the rollup permission error (3b132 QA r1): exit status 1 and
    a stderr that is that one line. Another message (an integration token's included), a path outside the
    rollup, another exit status, any other output, or no captured stderr is not, and the caller then stops
    as on any gh failure.
    RESIDUE, stated: this matches the gh CLI's wording as captured in the reality fixture. A gh release that
    rewords the error, or a response carrying more than one error, is not matched, so the fallback is
    unreachable again for it: that refuses, and never merges."""
    return (isinstance(exc, subprocess.CalledProcessError) and exc.returncode == 1
            and isinstance(exc.stderr, str) and _ROLLUP_FORBIDDEN.fullmatch(exc.stderr.rstrip("\n")) is not None)


class _Unreadable(Exception):
    """A construct the workflow reader recognizes as outside its grammar; the pin then fails (3b105 QA r3, r4)."""


def _yaml_scalar(raw: str) -> str:
    """A single-line YAML scalar: plain (an inline ` #` comment dropped), single-quoted (a doubled quote is
    a literal quote), or double-quoted without escapes. A scalar form it recognizes as outside that set
    raises _Unreadable rather than returning a guess (3b105 QA r2, r3)."""
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
    mislead it in either direction. A misread does not by itself cause a wrong merge, since this pin runs
    only in the self-test: it removes the early warning of a rename. evaluate() still requires a
    successful CheckRun with the required name from the bound workflow; a same-named job added under that
    workflow is the REQUIRED_WORKFLOWS residue, whose control is workflow-file review (3b105 QA r5)."""
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
        is_item = stripped.startswith("- ") or stripped == "-"  # a bare dash opens an item (3b105 QA r6)
        item = stripped[2:].lstrip() if is_item else stripped
        key, sep, value = item.partition(":")
        key = key.rstrip(" ")  # `name :` is the key name (3b105 QA r6)
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
        if indent == prop_indent and not is_key and not is_item:
            raise _Unreadable("a job property that is not a plain key (a quoted key, for example)")
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
    """Run gh and return its stdout. Its stderr is captured, so a failure carries it to rollup_forbidden()
    and to the error report (3b132 QA r1); after a success it is passed through."""
    done = subprocess.run(["gh", *args], text=True, capture_output=True)
    if done.returncode != 0:
        raise subprocess.CalledProcessError(done.returncode, done.args, done.stdout, done.stderr)
    if done.stderr:
        sys.stderr.write(done.stderr)
    return done.stdout


def _failure(exc: BaseException) -> str:
    """A failed gh call for the operator: the exception and, as gh() now captures it, what gh printed."""
    err = getattr(exc, "stderr", None)
    return f"{exc} gh: {err.strip()}" if isinstance(err, str) and err.strip() else str(exc)


def _self_test_actions_fallback() -> list[tuple[str, bool]]:
    """The Actions-runs fallback (3b132): evaluate_runs() on its own, then main() with a stubbed gh."""
    import contextlib as _cl, io as _io
    checks = []
    head = "3f0c9e71a2b48d5609ce17f4b23a8d60e95c1b7a"
    path = ".github/workflows/validate.yml"
    wf = {"validate": path}
    def run(name="validate", status="completed", concl="success", sha=head, p=path, event="pull_request", rid=1):
        return {"id": rid, "name": name, "path": p, "event": event, "status": status, "conclusion": concl,
                "head_sha": sha}
    page = lambda runs, total=None: {"total_count": len(runs) if total is None else total, "workflow_runs": runs}
    other = run("other", p=".github/workflows/other.yml", event="push", rid=2)
    for name, payload, want_green in [
        ("runs-green", page([run()]), True),
        ("runs-green-with-other-workflow", page([run(), other]), True),
        ("runs-green-pr-and-push", page([run(), run(event="push", rid=2)]), True),
        ("runs-none-refused", page([]), False),
        ("runs-in-progress-refused", page([run(status="in_progress", concl=None)]), False),
        ("runs-queued-refused", page([run(status="queued", concl=None)]), False),
        ("runs-waiting-refused", page([run(status="waiting", concl=None)]), False),
        ("runs-failure-refused", page([run(concl="failure")]), False),
        ("runs-skipped-refused", page([run(concl="skipped")]), False),
        ("runs-neutral-refused", page([run(concl="neutral")]), False),
        ("runs-startup-failure-refused", page([run(concl="startup_failure")]), False),
        ("runs-completed-null-conclusion-refused", page([run(concl=None)]), False),
        ("runs-upper-case-refused", page([run(status="COMPLETED", concl="SUCCESS")]), False),
        ("runs-other-workflow-failing-refused", page([run(), dict(other, conclusion="failure")]), False),
        ("runs-other-workflow-pending-refused", page([run(), dict(other, status="in_progress", conclusion=None)]), False),
        ("runs-required-missing-refused", page([other]), False),
        ("runs-other-commit-refused", page([run(), run(sha="b" * 40, rid=2)]), False),
        ("runs-truncated-refused", page([run()], total=2), False),
        ("runs-foreign-file-refused", page([run(p=".github/workflows/fake.yml")]), False),
        ("runs-collision-refused", page([run(), run(p=".github/workflows/fake.yml", rid=2)]), False),
        ("runs-push-only-refused", page([run(event="push")]), False),
        ("runs-non-dict-entry-refused", page([run(), "x"]), False),
        ("runs-nameless-entry-refused", page([run(), dict(run(), name=None)]), False),
        ("runs-payload-list-refused", [run()], False),
        ("runs-payload-none-refused", None, False),
        ("runs-payload-runs-not-list-refused", {"total_count": 1, "workflow_runs": "x"}, False),
        ("runs-payload-count-missing-refused", {"workflow_runs": [run()]}, False),
        ("runs-payload-count-bool-refused", {"total_count": True, "workflow_runs": [run()]}, False),
    ]:
        checks.append((name, evaluate_runs(payload, head, wf)[0] == want_green))
    checks.append(("runs-no-workflow-configured-refused", not evaluate_runs(page([run()]), head, {})[0]))
    _, r_missing = evaluate_runs(page([other]), head, wf)
    checks.append(("runs-missing-reason-names-workflow", "validate" in r_missing and path in r_missing))
    _, r_green = evaluate_runs(page([run()]), head, wf)
    checks.append(("runs-green-reason-says-fallback", "Actions-runs fallback" in r_green))
    checks.append(("fallback-map-exact", ACTIONS_FALLBACK == {
        "jposluns/grc_library_ref": {"validate": ".github/workflows/validate.yml"}}))
    # 3b132 QA r1: exactly the reality fixture's permission error engages the fallback; nothing else does.
    fx = ("GraphQL: Resource not accessible by personal access token (repository.pullRequest."
          "statusCheckRollup.nodes.0.commit.statusCheckRollup.contexts.nodes.0)\n")
    denied = lambda err=fx, rc=1: subprocess.CalledProcessError(rc, ["gh"], "", err)
    for name, exc, want in [
        ("forbidden-fixture", denied(), True),
        ("forbidden-no-trailing-newline", denied(fx.rstrip("\n")), True),
        ("forbidden-rollup-root", denied(fx.split(".nodes")[0] + ")\n"), True),
        ("forbidden-integration-token-not", denied(fx.replace("personal access token", "integration")), False),
        ("forbidden-pr-path-not", denied(fx.split(".statusCheckRollup")[0] + ")\n"), False),
        ("forbidden-other-field-not",
         denied(fx.replace("pullRequest.statusCheckRollup", "pullRequest.commits", 1)), False),
        ("forbidden-longer-field-not",
         denied(fx.replace("statusCheckRollup.nodes", "statusCheckRollupX.nodes", 1)), False),
        ("forbidden-extra-line-not", denied(fx + "HTTP 502\n"), False),
        ("forbidden-leading-line-not", denied("warning\n" + fx), False),
        ("forbidden-two-errors-not", denied(fx.rstrip("\n") + ", " + fx[len("GraphQL: "):]), False),
        ("forbidden-exit-4-not", denied(rc=4), False),
        ("forbidden-no-stderr-not", subprocess.CalledProcessError(1, ["gh"]), False),
        ("forbidden-bytes-stderr-not", subprocess.CalledProcessError(1, ["gh"], b"", fx.encode()), False),
        ("forbidden-os-error-not", OSError(fx), False),
        ("forbidden-other-graphql-not",
         denied("GraphQL: Could not resolve to a PullRequest with the number of 181. (repository.pullRequest)\n"), False),
    ]:
        checks.append((name, rollup_forbidden(exc) == want))
    # gh() captures stderr, so the error can reach rollup_forbidden(): subprocess.run is stubbed here.
    seen, captured, real_run = [], None, subprocess.run
    subprocess.run = lambda cmd, **kw: (seen.append((cmd, kw)), subprocess.CompletedProcess(cmd, 1, "", fx))[1]
    try:
        gh("pr", "view", "1")
    except subprocess.CalledProcessError as exc:
        captured = exc
    finally:
        subprocess.run = real_run
    checks.append(("gh-captures-stderr", captured is not None and rollup_forbidden(captured)
                   and seen == [(["gh", "pr", "view", "1"], {"text": True, "capture_output": True})]))
    # main(): the fallback engages only for a listed --repo whose rollup carries no CheckRun, reads the runs
    # for the evaluated head, and pins the merge to it; every refusal makes no merge call.
    repo = "jposluns/grc_library_ref"
    calls = []
    json_arg = lambda a: a[a.index("--json") + 1] if "--json" in a else ""
    def stub(rollup=(), runs=None, h=head, api_error=None, rollup_error=None, view_error=None, state="OPEN"):
        def gh_(*a):
            calls.append(a)  # every call, a merge included, is recorded before dispatch
            if a[:2] == ("pr", "view"):
                with_rollup = "statusCheckRollup" in json_arg(a).split(",")
                if with_rollup and rollup_error is not None:
                    raise rollup_error
                if not with_rollup and view_error is not None:
                    raise view_error
                full = {"state": state, "statusCheckRollup": list(rollup), "headRefOid": h, "number": 1, "title": "t"}
                return json.dumps({k: full[k] for k in json_arg(a).split(",") if k in full})
            if a[:1] == ("api",):
                if api_error is not None:
                    raise api_error
                return runs if isinstance(runs, str) else json.dumps(page([run()]) if runs is None else runs)
            return ""
        return gh_
    def drive(flags, **kw):
        calls.clear()
        globals()["gh"] = stub(**kw)
        with _cl.redirect_stdout(_io.StringIO()), _cl.redirect_stderr(_io.StringIO()):
            return main(["merge-when-green.py", "1", *flags])
    api = lambda: [c for c in calls if c[:1] == ("api",)]
    merges = lambda: [c for c in calls if c[:2] == ("pr", "merge")]
    pinned = lambda m: "--match-head-commit" in m and m[m.index("--match-head-commit") + 1] == head
    status = lambda st: {"__typename": "StatusContext", "context": "ci", "state": st}
    real_gh, real_block = globals()["gh"], globals()["open_findings_block"]
    # The ledger check is stubbed, as in _self_test(), so these cases never read the live ledger (3b108).
    globals()["open_findings_block"] = lambda root, ledger=None: (0, "")
    try:
        rc = drive(["--repo", repo, "--dry-run"])
        checks.append(("fallback-green-dry-run-never-merges", rc == 0 and not merges()
                       and api() == [("api", f"repos/{repo}/actions/runs?head_sha={head}&per_page=100")]))
        for label, extra in (("plain", []), ("admin", ["--admin"])):
            rc = drive(["--repo", repo, *extra])
            m = merges()
            checks.append((f"fallback-merge-pins-evaluated-head-{label}",
                           rc == 0 and len(m) == 1 and pinned(m[0]) and ("--admin" in m[0]) == bool(extra)))
        rc = drive(["--repo", repo, "--dry-run"], rollup=[status("SUCCESS")])
        checks.append(("fallback-status-green-plus-runs-green", rc == 0 and len(api()) == 1))
        # A CheckRun in the rollup means Checks are readable: the rollup decides, with no runs read.
        crun = {"__typename": "CheckRun", "name": "validate", "status": "COMPLETED", "conclusion": "SUCCESS",
                "workflowName": "validate"}
        rc = drive(["--repo", repo, "--dry-run", "--require-none"], rollup=[crun], runs=page([]))
        checks.append(("fallback-not-engaged-with-a-checkrun", rc == 0 and not api()))
        # (label, flags, stub arguments, exit code, whether the runs may be read); none may merge.
        for label, flags, kw, want_rc, reads in (
            ("unlisted-repo", ["--repo", "other/repo"], {}, 1, False),
            ("no-repo", [], {}, 1, False),
            ("explicit-require", ["--repo", repo, "--require", "validate"], {}, 1, False),
            ("bad-head", ["--repo", repo], {"h": "abc123"}, 1, False),
            ("status-failing", ["--repo", repo], {"rollup": [status("FAILURE")]}, 1, False),
            ("status-pending", ["--repo", repo], {"rollup": [status("PENDING")]}, 1, False),
            ("runs-none", ["--repo", repo], {"runs": page([])}, 1, True),
            ("runs-pending", ["--repo", repo], {"runs": page([run(status="in_progress", concl=None)])}, 1, True),
            ("runs-other-commit", ["--repo", repo], {"runs": page([run(sha="b" * 40)])}, 1, True),
            ("require-none-still-needs-workflow", ["--repo", repo, "--require-none"], {"runs": page([other])}, 1, True),
            ("api-error", ["--repo", repo], {"api_error": subprocess.CalledProcessError(1, "gh")}, 2, True),
            ("api-not-json", ["--repo", repo], {"runs": "<html>"}, 2, True),
        ):
            rc = drive(flags, **kw)
            checks.append((f"fallback-{label}-refused", rc == want_rc and not merges() and (reads or not api())))
        # 3b132 QA r1: the rollup query fails with the permission error (the reality fixture); the PR is read
        # again without the rollup, the runs for that head decide, and the merge is pinned to it.
        views = lambda: [c for c in calls if c[:2] == ("pr", "view")]
        reread = [("pr", "view", "1", "--repo", repo, "--json", _VIEW_FIELDS)]
        runs_call = [("api", f"repos/{repo}/actions/runs?head_sha={head}&per_page=100")]
        rc = drive(["--repo", repo, "--dry-run"], rollup_error=denied())
        checks.append(("forbidden-green-dry-run-never-merges", rc == 0 and not merges() and len(views()) == 2
                       and views()[1:] == reread and api() == runs_call))
        for label, extra in (("plain", []), ("admin", ["--admin"])):
            rc = drive(["--repo", repo, *extra], rollup_error=denied())
            m = merges()
            checks.append((f"forbidden-merge-pins-evaluated-head-{label}", rc == 0 and len(m) == 1 and pinned(m[0])
                           and ("--admin" in m[0]) == bool(extra) and api() == runs_call))
        # (label, flags, stub arguments, exit code, whether the runs may be read, whether the PR is read again);
        # none may merge. Any error but the exact one, or an unlisted repository, stops at the first read.
        gh_err = lambda err, rc=1: {"rollup_error": denied(err, rc)}
        for label, flags, kw, want_rc, reads, again in (
            ("unlisted-repo", ["--repo", "other/repo"], gh_err(fx), 2, False, False),
            ("no-repo", [], gh_err(fx), 2, False, False),
            ("integration-token", ["--repo", repo], gh_err(fx.replace("personal access token", "integration")),
             2, False, False),
            ("pr-path", ["--repo", repo], gh_err(fx.split(".statusCheckRollup")[0] + ")\n"), 2, False, False),
            ("extra-line", ["--repo", repo], gh_err(fx + "HTTP 502\n"), 2, False, False),
            ("exit-status-4", ["--repo", repo], gh_err(fx, 4), 2, False, False),
            ("no-stderr", ["--repo", repo], {"rollup_error": subprocess.CalledProcessError(1, ["gh"])},
             2, False, False),
            ("os-error", ["--repo", repo], {"rollup_error": OSError("gh not found")}, 2, False, False),
            ("reread-fails", ["--repo", repo], dict(gh_err(fx), view_error=denied("HTTP 502\n")), 2, False, True),
            ("reread-not-open", ["--repo", repo], dict(gh_err(fx), state="MERGED"), 1, False, True),
            ("reread-bad-head", ["--repo", repo], dict(gh_err(fx), h="abc123"), 1, False, True),
            ("explicit-require", ["--repo", repo, "--require", "validate"], gh_err(fx), 1, False, True),
            ("runs-failing", ["--repo", repo], dict(gh_err(fx), runs=page([run(concl="failure")])), 1, True, True),
            ("runs-none", ["--repo", repo], dict(gh_err(fx), runs=page([])), 1, True, True),
            ("runs-other-commit", ["--repo", repo], dict(gh_err(fx), runs=page([run(sha="b" * 40)])),
             1, True, True),
        ):
            rc = drive(flags, **kw)
            checks.append((f"forbidden-{label}-refused", rc == want_rc and not merges() and (reads or not api())
                           and len(views()) == (2 if again else 1)))
    finally:
        globals()["gh"] = real_gh
        globals()["open_findings_block"] = real_block
    return checks


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
    # carrying the required check's name. A plain rename in either file fails here rather than first at
    # merge time; the reader's residue (workflow_names) names what it cannot see.
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
    # 3b105 QA r3: the pin fails on each way the job or workflow can be absent, and on the constructs the
    # reader recognizes as outside its grammar (reviewers' reproductions included; the residue is stated).
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
        ("quoted-name-key", H_ + "jobs:\n  lint:\n    name: Lint markdown corpus\n    \"name\": Renamed\n"),
        ("spaced-name-key", H_ + "jobs:\n  lint:\n    name: Lint markdown corpus\n    name : Renamed\n"),
        ("jobs-with-value", H_ + "jobs: &j\n  lint:\n    name: Lint markdown corpus\n"),
        ("open-quote-top", "name: Repository quality checks\nenv: 'x\njobs:\n  lint:\n    name: Lint markdown corpus\n'\n"),
    ):
        checks.append((f"pin-refuses-{label}", not pin_ok(text, lint_)))
    # The quoted-key refusal stays narrow: list items at the property indentation, a bare dash, comments and
    # blank lines still read (3b105 QA r6).
    styles = ("name: W\njobs:\n  lint:\n    name: Lint markdown corpus\n    steps:\n    - run: x\n    -\n"
              "      uses: y\n\n    # c\n    runs-on: z\n")
    checks.append(("reader-narrow-refusal", workflow_names(styles) == ("W", {lint_})))
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
    checks.extend(_self_test_actions_fallback())
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
                       help="require no named check (for a repository without the default checks); an "
                            "ACTIONS_FALLBACK repository still requires its workflows")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv[1:])
    if args.self_test:
        return _self_test()
    if not args.pr:
        ap.print_usage(sys.stderr)
        print("ERROR: give a PR number (or --self-test).", file=sys.stderr)
        return 2
    repo_args = ["--repo", args.repo] if args.repo else []
    fallback = ACTIONS_FALLBACK.get(args.repo or "")
    unreadable = False  # the token could not read the rollup at all (3b132 QA r1)
    try:
        try:
            raw = gh("pr", "view", args.pr, *repo_args,
                     "--json", "statusCheckRollup,number,title,state,headRefOid")
        except subprocess.CalledProcessError as exc:
            if fallback is None or not rollup_forbidden(exc):
                raise
            # A listed repository whose token cannot read the rollup: read the PR again without it, and the
            # Actions runs for its head decide below. Any other failure stops here, as before.
            unreadable = True
            raw = gh("pr", "view", args.pr, *repo_args, "--json", _VIEW_FIELDS)
        view = json.loads(raw)
    except (subprocess.CalledProcessError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: gh pr view failed: {_failure(exc)}", file=sys.stderr)
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
    rollup = [] if unreadable else (view.get("statusCheckRollup") or [])
    if fallback is not None and isinstance(rollup, list) and not any(
            isinstance(c, dict) and c.get("__typename") == "CheckRun" for c in rollup):
        # This repository's token cannot read Checks: the Actions runs for the head decide (3b132).
        if args.require:
            print(f"REFUSE to merge PR #{args.pr}: --require names check runs, which the Actions-runs fallback "
                  "cannot see; its required workflows are set in ACTIONS_FALLBACK", file=sys.stderr)
            return 1
        green, reason = evaluate(rollup) if rollup else (True, "")  # a commit status present must still pass
        if green:
            try:
                runs = json.loads(gh("api", f"repos/{args.repo}/actions/runs?head_sha={head}&per_page=100"))
            except (subprocess.CalledProcessError, OSError, json.JSONDecodeError) as exc:
                print(f"ERROR: gh api actions/runs failed: {_failure(exc)}", file=sys.stderr)
                return 2
            green, runs_reason = evaluate_runs(runs, head, fallback)
            reason = f"{runs_reason}; commit statuses: {reason}" if (green and reason) else runs_reason
            if green and unreadable:
                reason += "; the check rollup itself was not readable, so no commit status was seen"
    else:
        required = () if args.require_none else tuple(args.require or REQUIRED_CHECKS)
        workflows = REQUIRED_WORKFLOWS  # a default name binds to its workflow even via --require (3b105 QA r1)
        green, reason = evaluate(rollup, required, workflows)
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
        print(f"ERROR: gh pr merge failed: {_failure(exc)}", file=sys.stderr)
        return 2
    print(f"MERGED PR #{args.pr} ({args.merge_method}).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
