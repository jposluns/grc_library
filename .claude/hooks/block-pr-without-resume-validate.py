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

WHAT IT BLOCKS. `gh pr create` and `gh pr merge`, and any command that mentions tools/merge-when-green.py
other than a simple direct --dry-run or --self-test (3b108; see invokes_merge_tool), when no qualifying
row exists for the session. Once
the row exists the hook passes for the rest of the session. ALL `gh pr create`/`merge` are gated
regardless of `--repo` (the orchestrator opens PRs only against this library; over-gating a
hypothetical other-repo PR is the safe direction and the sentinel escapes it).

GUARD-INPUT AUTHORITY. The evidence is the SWEEP'S OWN artefact-of-record (the history row the
/validate activity writes), never a self-attested "step done" marker. The row is a PROXY (it proves a
row was written, not that the sweep was semantically complete); that residue is stated and layered
behind the triple-family standard and the open-findings guard.

FAIL-OPEN BY DESIGN. On a malfunction (a non-dict payload, a non-dict tool_input, a non-string
command, an unresolvable/unreadable history, an unreadable session start) this hook ALLOWS: every
I/O call in main() is wrapped, and the pure decide() core treats every "unknown" input as ALLOW.
ONE qualification: if the WORKER-IDENTITY helper raises, ``_safe`` returns None and the session is
treated as NON-worker (``is_worker=False``) rather than auto-allowed, so a recognized PR with
readable history, no qualifying row, and no consumable sentinel can still reach BLOCK -- an
unresolvable worker identity is gated, not fail-opened. A guard that wedges on its own malfunction
gets removed, and a removed guard protects nothing. Adopters (no private store) are a no-op.

ESCAPE. A genuine exception (a handoff-only session that must open a PR without a sweep) is honoured
via a one-shot sentinel the actor creates, consumed only when the hook would otherwise block:
    touch "${GRC_DROP_ROOT:-<repo-parent>/grc_working}/.allow-pr-without-resume-validate"
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



def invokes_merge_tool(cmd: str) -> bool:
    """PURE. Could this command run tools/merge-when-green.py for a real merge (3b108)? That tool runs
    `gh pr merge` as a subprocess, so the literal-text match never sees it. Parsing shell for every way
    to run it (wrappers, bash -c, backticks, python -m, continuations, newlines) cannot be made
    complete (3b108 QA r1), so this over-gates by intent. THREAT MODEL, stated: a speed bump for an
    honest actor's slip, not an adversarial control; a deliberately obfuscated command (a glob such as
    gree[n] or gree*, a variable holding part of the name, code run through python -c) can still evade,
    and merge-when-green.py enforces the open-findings decision itself on every merge. After dropping quotes and backslash-newline
    continuations, any mention of merge-when-green gates, except a single simple command (one line,
    no shell operator, no substitution) that passes --dry-run or --self-test. A read of the file is
    gated too; that costs little, since this hook blocks only while its blocking state holds, and
    merge-when-green.py enforces the open-findings check itself on every merge."""
    if not isinstance(cmd, str):
        return False
    norm = cmd.replace("\\\n", "")
    for q in ("'", '"', "`", "\\"):  # quotes and escapes (merge-when-\\green) do not hide the name
        norm = norm.replace(q, "")
    if "merge-when-green" not in norm:
        return False
    # The exemption needs the flag among the tool's OWN arguments in a direct invocation (the tool, or a
    # python interpreter with single-letter options, then the tool): a comment, a `bash -c ... --dry-run`
    # ($0 of the inner shell) or any other placement gates (3b108 QA r2).
    simple = "\n" not in cmd.strip() and not any(op in cmd for op in (";", "&", "|", "`", "$(", "<", ">", "\\", "#"))
    if simple:
        try:
            toks = shlex.split(cmd)
        except ValueError:
            return True
        i = 0
        if toks and os.path.basename(toks[0]).startswith("python"):
            i = 1
            while i < len(toks) and len(toks[i]) == 2 and toks[i].startswith("-") and toks[i] not in ("-m", "-c"):
                i += 1
        if i < len(toks) and os.path.basename(toks[i]) == "merge-when-green.py":
            if "--dry-run" in toks[i + 1:] or "--self-test" in toks[i + 1:]:
                return False
    return True

def is_blocking_command(cmd: str) -> bool:
    """PURE. Does this command open or merge a PR? Deliberately robust (over-gating is the safe
    direction; the costly error is a MISSED create/merge). Two complementary detectors, OR'd:

      (1) SUBSTRING on the whitespace-flattened command -- catches operator-glued / semicolon-chained
          / unbalanced-quote forms (`gh pr create&&echo`, `gh pr merge;x`, `gh pr create # '`).
      (2) ORDERED TOKEN SUBSEQUENCE `gh` -> `pr` -> `create`|`merge` over shlex tokens -- catches
          quoted subcommands (`gh "pr" create`, `gh pr 'create'`) and interleaved flags
          (`gh -R x pr create`), which the substring misses because shlex removes the quotes and the token order ignores flags.

    Token parsing uses `punctuation_chars=True`, so operator-glued verbs (`create&&echo`) split to a
    bare `create` token and are caught even when combined with interleaved flags.

    The gh detectors read the text as written, with every backslash-newline joined, and joined as bash
    joins, and read line by line and a shell's -c argument or eval's as a command too; any match blocks (3b112 QA r1-r3).

    The `gh` token is matched bare OR as a path (`*/gh`). RESIDUE, not exhaustive: shell forms this does not model still evade, for
    example a word held in a variable (c=merge; gh pr $c), an alias, ANSI-C quoting (gh pr $'merge'),
    brace expansion (gh pr {merge,}), an unquoted mid-word # earlier on the line (shlex starts a
    comment there, bash does not), or a heredoc body with an unbalanced quote followed by a verb split
    across a continuation. Accepted: this guard is a SPEED BUMP for an
    honest actor's slipped resume-/validate, matching the sentinel's own "not a security boundary"
    stance, NOT an adversarial control."""
    if not isinstance(cmd, str):
        return False
    if invokes_merge_tool(cmd):  # the sanctioned merge path runs gh pr merge as a subprocess (3b108)
        return True
    # Three readings of the text: as written, with every backslash-newline joined, and joined as bash joins
    # (not after an even backslash run, in a comment, or in single quotes). Each is read whole and line by
    # line, so one unparseable line (an apostrophe in a heredoc body) cannot hide the rest; the argument of
    # a shell's -c option or of eval is read as a command too (3b112 QA r1-r4). Blocking on any over-gates,
    # the safe direction. The merge-tool exemption above reads only the text as written.
    for text in (cmd, cmd.replace("\\\n", ""), _bash_join(cmd)):
        for part in (text, *text.split("\n")):
            if _gh_pr_verb(part):
                return True
            toks = _tokens(part) or []
            for i, tk in enumerate(toks[1:], 1):
                prev = toks[i - 1]
                shell_c = (prev.startswith("-") and prev.endswith("c") and i >= 2
                           and os.path.basename(toks[i - 2]) in ("bash", "sh", "zsh", "dash", "ksh"))
                if (shell_c or prev == "eval") and _gh_pr_verb(tk):
                    return True
    return False


def _bash_join(cmd: str) -> str:
    """PURE. Remove the backslash-newlines bash treats as line continuations: outside single quotes and
    comments, and only where the backslash is not itself escaped (3b112 QA r3). A model, not a shell."""
    out, i, n = [], 0, len(cmd)
    single = double = comment = False
    word_start = True
    while i < n:
        c = cmd[i]
        if comment:
            out.append(c)
            if c == "\n":
                comment, word_start = False, True
            i += 1
            continue
        if single:
            out.append(c)
            single = c != "'"
            i += 1
            continue
        if c == "\\" and i + 1 < n:
            if cmd[i + 1] == "\n":
                i += 2
                continue
            out.append(cmd[i:i + 2])
            i, word_start = i + 2, False
            continue
        if c == "'" and not double:
            single = True
        elif c == '"':
            double = not double
        elif c == "#" and not double and word_start:
            comment = True
        out.append(c)
        word_start = c in " \t\n;&|()"
        i += 1
    return "".join(out)


def _gh_pr_verb(cmd: str) -> bool:
    """PURE. The substring pass and the ordered shlex token pass for `gh pr create|merge`."""
    flat = " ".join(cmd.split())
    if any(" ".join(parts) in flat for parts in BLOCKING_CMDS):
        return True
    toks = _tokens(cmd)
    if toks is None:
        return False  # unparseable: the caller also reads each line on its own
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
    root = os.environ.get("GRC_DROP_ROOT") or str((Path(__file__).resolve().parents[3] / "grc_working"))
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
        "BLOCKED (pr-without-resume-validate): a PR open/merge without a corpus-wide resume /validate row in "
        f"{HISTORY_REL} dated on/after {when}.\n"
        "WHY: /orch step 6a mandates a resume /validate as the session's first substantive task: it is "
        "the fresh-context drift-catch AND the compensating control for the closing-session QA fallback.\n"
        "CONSIDER INSTEAD: dispatch the triple-family corpus-wide /validate and record its history row, "
        "then re-run this. For a genuine exception (e.g. a handoff-only session), create the one-shot "
        "sentinel then retry:\n"
        # The resolved path, shell-quoted: a literal <repo-parent> fallback does not run (P-1.21 r2, codex).
        f"    touch {shlex.quote(str(_sentinel_path()))}"
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
    # 3b108: the sanctioned merge path runs gh pr merge as a subprocess, so the tool itself is gated;
    # detection over-gates by intent (QA r1: shell parsing could not be made complete).
    for c in ("python3 tools/merge-when-green.py 12 --repo o/r --admin",
              "for i in 1; do out=$(python3 -B /x/tools/merge-when-green.py 12 --admin 2>&1); done",
              "./tools/merge-when-green.py 12",
              "python3 tools/merge-when-green.py 12 --admin\npython3 tools/merge-when-green.py 13 --dry-run",
              "timeout 60 ./tools/merge-when-green.py 12", "bash -c 'tools/merge-when-green.py 12 --admin'",
              "out=`python3 tools/merge-when-green.py 12`", 'out="$(python3 tools/merge-when-green.py 12)"',
              "python3 -m tools.merge-when-green 12", "python3 tools/merge-when-\\\ngreen.py 12",
              'python3 tools/merge-when-""green.py 12 --admin', "python3 tools/merge-when-green.py 12 --admin # ' --dry-run",
              "python3 tools/merge-when-green.py 12 --admin > --dry-run", "grep -n x tools/merge-when-green.py",
              "python3 tools/merge-when-green.py 12 --admin # --dry-run",
              "bash -c 'python3 tools/merge-when-green.py 12 --admin' --dry-run",
              "sh -c 'tools/merge-when-green.py 12' --self-test", "env python3 tools/merge-when-green.py 12 --dry-run",
              "python3 -c 'import os' tools/merge-when-green.py --dry-run",
              "python3 tools/merge-when-\\green.py 12 --admin",
              "python3 -c 'print(1) or 1/merge-when-green.py' --dry-run"):
        ck(f"gated: {c[:48]}", is_blocking_command(c), True)
    for c in ("python3 tools/merge-when-green.py 12 --dry-run", "python3 tools/merge-when-green.py --self-test",
              "python3 -B /opt/x/tools/merge-when-green.py 2620 --repo o/r --dry-run", "git status --short",
              "/usr/bin/python3.12 -B tools/merge-when-green.py --self-test", "./tools/merge-when-green.py 12 --dry-run"):
        ck(f"not gated: {c[:48]}", is_blocking_command(c), False)
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
    ck("pr merge without gh does not block", is_blocking_command("echo pr merge"), False)
    ck("backslash-newline continuation blocks (3b112 QA r1)", is_blocking_command("gh pr \\\nmerge 1"), True)
    # 3b112 QA r2: bash does not join after an even backslash run or inside a comment; both texts are checked
    for s in ("echo x\\\\\ngh pr 'merge' 1", "# note \\\ngh pr 'merge' 1", "true # trailing\\\ngh pr 'create'",
              '# note \\\ngh "pr" create'):
        ck(f"unjoined text still checked: {s!r}", is_blocking_command(s), True)
    # 3b112 QA r3: mixed continuations (one bash joins, one it does not) and a nested shell
    for s in ("x\\\\\ngh pr 'me'\\\nrge 1", "# x \\\ngh pr 'me'\\\nrge 1", 'echo n # c \\\ngh "pr" me\\\nrge',
              "# note \\\ngh -R o/r pr \\\nmerge 1", 'bash -c "gh -R o/r pr merge"', "bash -c \"gh 'pr' merge\"",
              "sh -c 'gh \"pr\" merge 1'"):
        ck(f"r3 form blocks: {s!r}", is_blocking_command(s), True)
    ck("quoted text without gh does not block", is_blocking_command('git commit -m "merge the pr"'), False)
    # 3b112 QA r4: a heredoc apostrophe does not hide a later command; ordinary quoted data does not block
    ck("heredoc apostrophe then flagged verb blocks",
       is_blocking_command("cat <<EOF >/dev/null\nit's done\nEOF\ngh pr -R o/r merge 12"), True)
    for s in ('git commit -m "update gh and pr to merge"', 'git commit -m "docs: gh for pr create flows"',
              "python3 tools/x.py --note 'gh then pr then merge'"):
        ck(f"quoted data does not block: {s!r}", is_blocking_command(s), False)
    ck("eval argument read as a command", is_blocking_command("eval \"gh -R o/r pr merge 1\""), True)
    ck("bash -lc argument read as a command", is_blocking_command("bash -lc \"gh 'pr' merge\""), True)
    ck("quoted --dry-ru<nl>n is not a dry-run exemption",
       is_blocking_command("python3 tools/merge-when-green.py 12 '--dry-\\\nrun'"), True)

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
           str(_sentinel_path()), str(Path(__file__).resolve().parents[3] / "grc_working" / SENTINEL_NAME))
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
