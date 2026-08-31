#!/usr/bin/env python3
"""PreToolUse: refuse to open or merge a PR when this session ran no resume /validate (step 6a).

WHY THIS IS A HOOK. /orch step 6a mandates a corpus-wide resume /validate as the first substantive
task of a session: it is both a fresh-context drift-catch AND the compensating control for the
closing-session per-change-QA fallback. On 2026-08-31 a session skipped it silently and self-caught
~6 hours later, after five PRs had already opened. A skipped compensating control is exactly the kind
of silent gap a mechanical guard should convert into an immediate, quotable refusal.

WHAT IT READS. The private validate-sweeps history (`.working/validate-sweeps/history.md`), whose
per-iteration rows record every sweep a session runs. A row qualifies as a resume /validate when its
first cell parses as a date on or after the session's start date and the row mentions both "resume"
and "validate" (case-insensitive).

WHAT IT BLOCKS. `gh pr create` and `gh pr merge` when no qualifying row exists for the session. Once
the row exists the hook passes for the rest of the session. ALL `gh pr create`/`merge` are gated
regardless of `--repo` (the orchestrator opens PRs only against this library; over-gating a
hypothetical other-repo PR is the safe direction and the sentinel escapes it).

GUARD-INPUT AUTHORITY. The evidence is the SWEEP'S OWN artefact-of-record (the history row the
/validate activity writes), never a self-attested "step done" marker. The row is a PROXY (it proves a
row was written, not that the sweep was semantically complete); that residue is stated and layered
behind the triple-family standard and the open-findings guard.

FAIL-OPEN BY DESIGN. On ANY malfunction (a non-dict payload, a non-dict tool_input, a non-string
command, an unresolvable/unreadable history, a helper that raises, an unreadable session start) this
hook ALLOWS: every I/O call in main() is wrapped, and the pure decide() core treats every "unknown"
input as ALLOW. A guard that wedges on its own malfunction gets removed, and a removed guard protects
nothing. Adopters (no private store) are a no-op.

ESCAPE. A genuine exception (a handoff-only session that must open a PR without a sweep) is honoured
via a one-shot sentinel the actor creates, consumed only when the hook would otherwise block:
    touch "${GRC_DROP_ROOT:-/opt/grc/grc_working}/.allow-pr-without-resume-validate"
"""
from __future__ import annotations

import datetime as _dt
import io
import json
import os
import re
import shlex
import sys
from pathlib import Path

HISTORY_REL = "validate-sweeps/history.md"
SENTINEL_NAME = ".allow-pr-without-resume-validate"
BLOCKING_CMDS = (("gh", "pr", "create"), ("gh", "pr", "merge"))
PUBLIC_REPO = "jposluns/grc_library"
ALLOW, BLOCK = 0, 2

_HOOK_DIR = Path(__file__).resolve().parent
for _p in (str(_HOOK_DIR.parents[1] / "tools"), str(_HOOK_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
try:
    from lint_common import resolve_working as _resolve_working
except Exception:  # pragma: no cover - fail-safe
    _resolve_working = None
try:
    from _session_clock import session_start_dt as _session_start_dt
except Exception:  # pragma: no cover
    _session_start_dt = None
try:
    from _hookutil import is_worker_session as _is_worker_session
except Exception:  # pragma: no cover
    _is_worker_session = None


def project_root() -> Path:
    return _HOOK_DIR.parents[1]


def _working_file(rel_below: str, root: Path):
    if _resolve_working is not None:
        return _resolve_working(rel_below, repo_root=root)
    cand = root / ".working" / rel_below
    return cand if cand.exists() else None


def _tokens(cmd: str):
    """PURE. shlex-tokenize with bash-style `#` comment handling; None on an unparseable command
    (unbalanced quotes). `comments=True` makes a trailing `# ...` a comment, as bash does."""
    try:
        # punctuation_chars=True (a shlex.shlex ctor arg, not a split() kwarg) splits shell operators
        # (`&& ; | < > ( )`) into their own tokens, so a verb glued to an operator (`create&&echo`)
        # becomes the token `create`, closing the glued-verb gap that otherwise combines with an
        # interleaved flag to evade detection. whitespace_split + posix mirror shlex.split; the default
        # commenters `#` drops a trailing bash comment.
        lex = shlex.shlex(cmd, posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        return list(lex)
    except ValueError:
        return None


def is_blocking_command(cmd: str) -> bool:
    """PURE. Does this command open or merge a PR? Deliberately robust (over-gating is the safe
    direction; the costly error is a MISSED create/merge). Two complementary detectors, OR'd:

      (1) SUBSTRING on the whitespace-flattened command -- catches operator-glued / semicolon-chained
          / unbalanced-quote forms (`gh pr create&&echo`, `gh pr merge;x`, `gh pr create # '`).
      (2) ORDERED TOKEN SUBSEQUENCE `gh` -> `pr` -> `create`|`merge` over shlex tokens -- catches
          quoted subcommands (`gh "pr" create`, `gh pr 'create'`) and interleaved flags
          (`gh -R x pr create`), which the substring misses because shlex unquotes and reorders.

    Token parsing uses `punctuation_chars=True`, so operator-glued verbs (`create&&echo`) split to a
    bare `create` token and are caught even when combined with interleaved flags.

    RESIDUE (stated): the `gh` token is matched bare OR as a path (`*/gh`). Only a deliberately obfuscated
    command (variable indirection like `c=create; gh pr $c`, or a shell alias) can still evade. Accepted: this guard is a SPEED BUMP for an
    honest actor's slipped resume-/validate, matching the sentinel's own "not a security boundary"
    stance, NOT an adversarial control."""
    if not isinstance(cmd, str):
        return False
    flat = " ".join(cmd.split())
    if any(" ".join(parts) in flat for parts in BLOCKING_CMDS):
        return True
    toks = _tokens(cmd)
    if toks is None:
        return False  # unparseable is already covered by the substring pass above
    seen_gh = seen_pr = False
    for tk in toks:
        if tk == "gh" or tk.endswith("/gh"):   # bare `gh` or an absolute/relative path to it
            seen_gh, seen_pr = True, False
        elif seen_gh and tk == "pr":
            seen_pr = True
        elif seen_pr and tk in ("create", "merge"):
            return True
    return False



def parse_date(cell: str):
    """PURE. Parse a leading YYYY-MM-DD from a cell, or None."""
    m = re.match(r"\s*(\d{4})-(\d{2})-(\d{2})", cell or "")
    if not m:
        return None
    try:
        return _dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def has_qualifying_row(text: str, threshold_date: _dt.date) -> bool:
    """PURE. Is there a resume-/validate history row dated >= threshold mentioning resume + validate?"""
    for line in (text or "").splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", s)]
        if cells and cells[0] == "":
            cells = cells[1:]
        if not cells:
            continue
        d = parse_date(cells[0])
        if d is None or d < threshold_date:
            continue
        low = s.lower()
        if "resume" in low and "validate" in low:
            return True
    return False


def _sentinel_path() -> Path:
    root = os.environ.get("GRC_DROP_ROOT") or "/opt/grc/grc_working"
    return Path(root) / SENTINEL_NAME


def _consume_sentinel() -> bool:
    p = _sentinel_path()
    try:
        if p.is_file():
            p.unlink()
            return True
    except Exception:
        return False
    return False


def decide(cmd, is_worker: bool, hist_text, start_date, sentinel_present: bool) -> int:
    """PURE decision core; main() gathers the I/O and CALLS this (single source of truth).

    ALLOW when: not a PR-open/merge command; a worker session; no private
    history (adopter/unreadable, hist_text is None); no readable session start (start_date is None);
    a qualifying row exists; or the sentinel authorizes. BLOCK only on a readable history with no
    qualifying row and no sentinel."""
    if not is_blocking_command(cmd):
        return ALLOW
    if is_worker:
        return ALLOW
    if hist_text is None:
        return ALLOW
    if start_date is None:
        return ALLOW
    if has_qualifying_row(hist_text, start_date):
        return ALLOW
    if sentinel_present:
        return ALLOW
    return BLOCK


def _block_message(threshold) -> str:
    when = threshold.isoformat() if threshold else "the session start"
    return (
        "BLOCKED (resume-/validate guard): this session has no corpus-wide resume /validate row in "
        f"{HISTORY_REL} dated on/after {when}, so a PR must not open or merge yet.\n\n"
        "/orch step 6a mandates a resume /validate as the session's first substantive task: it is the "
        "fresh-context drift-catch AND the compensating control for the closing-session QA fallback. "
        "Dispatch the triple-family corpus-wide /validate, record its history row, then re-run this.\n\n"
        "Genuine exception (e.g. a handoff-only session): create the one-shot sentinel, then retry:\n"
        '    touch "${GRC_DROP_ROOT:-/opt/grc/grc_working}/.allow-pr-without-resume-validate"'
    )


def _safe(fn, *a, **k):
    """Call fn, swallowing ANY exception to None (so a raising helper fails OPEN, never crashes)."""
    try:
        return fn(*a, **k)
    except Exception:
        return None


def _run(stdin) -> int:
    stream = stdin if stdin is not None else sys.stdin
    try:
        payload = json.load(stream)
    except Exception:
        return ALLOW
    if not isinstance(payload, dict):
        return ALLOW
    if payload.get("tool_name") != "Bash":
        return ALLOW
    ti = payload.get("tool_input")
    cmd = ti.get("command", "") if isinstance(ti, dict) else ""
    if not isinstance(cmd, str):
        cmd = ""
    # Cheap pure gates first (no I/O): if not a library PR-open/merge, allow without touching state.
    if not is_blocking_command(cmd):
        return ALLOW

    is_worker = bool(_safe(_is_worker_session)) if _is_worker_session is not None else False
    if is_worker:
        return ALLOW

    hist = _safe(_working_file, "validate-sweeps/history.md", project_root())
    hist_text = _safe(lambda p: p.read_text(encoding="utf-8"), hist) if hist is not None else None
    if hist_text is None:
        return ALLOW

    transcript = payload.get("transcript_path")
    start_dt = _safe(_session_start_dt, transcript) if (_session_start_dt and transcript) else None
    start_date = start_dt.date() if start_dt is not None else None
    if start_date is None:
        print("NOTE (resume-/validate guard): session start unreadable; allowing (fail-open). "
              "Confirm a resume /validate ran this session.", file=sys.stderr)
        return ALLOW

    # Pure decision (single source of truth), sentinel not yet consumed.
    if decide(cmd, is_worker, hist_text, start_date, sentinel_present=False) != BLOCK:
        return ALLOW
    # Would block: honour a one-shot sentinel, else refuse.
    if _consume_sentinel():
        print("resume-/validate guard: one-shot sentinel consumed; allowing this PR. Record the "
              "exception and its reason in the sweep history Summary or the PR.", file=sys.stderr)
        return ALLOW
    print(_block_message(start_date), file=sys.stderr)
    return BLOCK


def main(stdin=None) -> int:
    """Top-level fail-open wrapper: ANY unexpected exception (a stderr write OSError, a helper
    returning a non-datetime, anything) ALLOWS, so the guard can never wedge the session on its own
    malfunction."""
    try:
        return _run(stdin)
    except Exception:
        return ALLOW


def self_test() -> int:
    cases, fails = 0, []

    def ck(name, got, want):
        nonlocal cases
        cases += 1
        if got != want:
            fails.append(f"{name}: {got!r} != {want!r}")
        print(f"  {'PASS' if got == want else 'FAIL'}: {name}")

    today = _dt.date(2026, 8, 31)
    yday = _dt.date(2026, 8, 30)
    hist = ("| Date | Sweep | Detail |\n"
            "| 2026-08-31 | resume /validate (mandatory, overnight) | a5908326 |\n"
            "| 2026-08-30 | resume /validate (mandatory) | PR #1800 |\n")

    ck("today's resume row qualifies", has_qualifying_row(hist, today), True)
    ck("prior-day-only does not qualify",
       has_qualifying_row("| 2026-08-30 | resume /validate | x |\n", today), False)
    ck("no resume row blocks", has_qualifying_row("| 2026-08-31 | matrix-fit | x |\n", today), False)
    ck("missing 'validate' no-qualify",
       has_qualifying_row("| 2026-08-31 | resume drift-scan | x |\n", today), False)
    ck("missing 'resume' no-qualify",
       has_qualifying_row("| 2026-08-31 | corpus /validate | x |\n", today), False)
    ck("midnight-span qualifies for a prior-day start", has_qualifying_row(hist, yday), True)
    ck("non-table line ignored", has_qualifying_row("resume /validate ran\n", today), False)

    # is_blocking_command: token-based + unparseable substring fallback + comment handling
    ck("gh pr create blocks", is_blocking_command("gh pr create --base main"), True)
    ck("gh pr merge blocks", is_blocking_command("gh pr merge 1840 --admin"), True)
    ck("gh pr checks not blocking", is_blocking_command("gh pr checks 1840 --watch"), False)
    ck("git push not blocking", is_blocking_command("git push -u origin br"), False)
    ck("body text containing the phrase is OVER-gated (substring, safe direction)",
       is_blocking_command("gh pr view 5 --body 'run gh pr create later'"), True)
    ck("UNPARSEABLE command containing the phrase is still blocking (no bypass)",
       is_blocking_command("gh pr create # '"), True)
    ck("'&&'-chained create still detected", is_blocking_command("gh pr create&&echo done"), True)
    ck("quoted subcommand token detected (gh \"pr\" create)", is_blocking_command('gh "pr" create'), True)
    ck("quoted verb token detected (gh pr \'create\')", is_blocking_command("gh pr 'create'"), True)
    ck("interleaved flag detected (gh -R x pr create)", is_blocking_command("gh -R jposluns/grc_library pr create"), True)
    ck("interleaved-flag merge detected", is_blocking_command("gh --json x pr merge 1"), True)
    ck("absolute-path gh + interleaved + glued detected",
       is_blocking_command("/usr/bin/gh -R jposluns/grc_library pr create&&echo done"), True)
    ck("./gh path form detected", is_blocking_command("./gh pr create"), True)
    ck("gh repo create is NOT a pr command", is_blocking_command("gh repo create foo"), False)
    ck("gh pr list then gh repo create is not a pr-create", is_blocking_command("gh pr list && gh repo create x"), False)
    ck("non-string command is not blocking", is_blocking_command(None), False)

    # decide() core -- the single source of truth main() calls
    ck("decide blocks: library create, no sweep, no sentinel",
       decide("gh pr create --base main", False, "| 2026-08-31 | other | x |", today, False), BLOCK)
    ck("decide allows: qualifying sweep", decide("gh pr create", False, hist, today, False), ALLOW)
    ck("decide allows: sentinel", decide("gh pr create", False, "no rows", today, True), ALLOW)
    ck("decide allows: worker", decide("gh pr create", True, "no rows", today, False), ALLOW)
    ck("decide allows: adopter (hist None)", decide("gh pr create", False, None, today, False), ALLOW)
    ck("decide allows: start None", decide("gh pr create", False, "no rows", None, False), ALLOW)
    ck("decide allows: not a PR command", decide("git push", False, "no rows", today, False), ALLOW)

    # main() I/O fail-open (malformed payloads) -- main() CALLS decide()
    ck("main allows non-JSON", main(io.StringIO("not json")), ALLOW)
    ck("main allows non-dict payload []", main(io.StringIO("[]")), ALLOW)
    ck("main allows non-dict tool_input",
       main(io.StringIO(json.dumps({"tool_name": "Bash", "tool_input": [1]}))), ALLOW)
    ck("main allows non-Bash", main(io.StringIO(json.dumps({"tool_name": "Read"}))), ALLOW)
    ck("main allows non-blocking Bash",
       main(io.StringIO(json.dumps({"tool_name": "Bash", "tool_input": {"command": "git status"}}))),
       ALLOW)

    # GRC_DROP_ROOT="" falls back to the default root (matching the documented ${VAR:-default})
    _saved = os.environ.get("GRC_DROP_ROOT")
    try:
        os.environ["GRC_DROP_ROOT"] = ""
        ck("empty GRC_DROP_ROOT uses the default sentinel root",
           str(_sentinel_path()), "/opt/grc/grc_working/" + SENTINEL_NAME)
    finally:
        if _saved is None:
            os.environ.pop("GRC_DROP_ROOT", None)
        else:
            os.environ["GRC_DROP_ROOT"] = _saved

    print(f"self-test: {cases} cases, {len(fails)} failed")
    for f in fails:
        print(f"  FAIL {f}")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main())
