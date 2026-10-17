#!/usr/bin/env python3
"""Startup character and core-line ceiling audit (gate 106).

Runs both halves of delta gate D10 (`tools/check-claude-md-size.py`) from
`tools/run_all_audits.sh`, so a run of the corpus gates shows a breach of
either D10 ceiling before the pre-push guard does: the core-line ceiling
(`.claude/CLAUDE.md` at most `CEILING` lines) and the startup character
ceiling (`.claude/CLAUDE.md` plus every unscoped `.claude/rules/` file at most
`STARTUP_CHARACTER_CEILING` Unicode characters). D10 runs only in the PR-time
runner and the workflow's pull-request steps; a change that passed every
corpus gate could still fail D10 at push time on either ceiling.

The counts, the scope rules, the ceilings and the warning threshold are D10's
own: this wrapper loads `check-claude-md-size.py` by path and calls its
`line_count()`, `evaluate()`, `census()`, `CLAUDE_MD`, `CEILING`,
`STARTUP_CHARACTER_CEILING` and `STARTUP_HEADROOM_WARNING`, so the two checks
cannot disagree on what is counted or where a ceiling sits. A separate script,
rather than a mode flag on D10, keeps gate 35's exclusion guard sound: that
guard fails when a delta-gate step's script is also a section 6 inventory
script.

Prints the core-line verdict and the startup headroom (ceiling minus the
measured startup characters) on every run that reaches a verdict (exit 0 or
1), and a WARN line when that headroom is under D10's warning threshold, as
D10 warns; on exit 2 the gate itself prints nothing to stdout (anything D10
prints while loading passes through). `tools/run_all_audits.sh`
hides a passing gate's output, so under the runner this gate prints the
runner-echo marker line with the runner's token (the gate 72 opt-in) and the
WARN line is shown on a pass. The WARN never changes the exit code.

Exit: 0 = both counts at or under their ceilings; 1 = either over; 2 = an
argument was given (this tool takes none), or D10 could not be loaded or read
or its census failed: an unreadable, malformed or symlinked rule file, a
missing CLAUDE.md or rules directory, a git failure (which D10 also refuses),
a renamed or missing D10 constant, function or census key, a D10 that does not
parse, fails to import, raises or calls sys.exit() while loading, a changed
function signature, a count or constant that is not an int (the core line
count and `CEILING` are checked before `evaluate()` is called), an
`evaluate()` code that is not the int 0 or 1, an `evaluate()` message that is
not a str, or any other exception while loading D10 or computing on its values.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
D10_PATH = REPO_ROOT / "tools" / "check-claude-md-size.py"

# tools/run_all_audits.sh hides a passing gate's output, but shows this gate's
# WARN and NOTE lines when the output has this exact line followed by a space
# and the token run_gate passed in RUNNER_ECHO_TOKEN_ENV (the gate 72 opt-in;
# run_gate holds the same string). With the variable unset or empty (a direct
# run, the pre-commit hook, the quality.yml gate step) the line is not printed.
RUNNER_ECHO_MARKER = (
    "runner-echo: tools/run_all_audits.sh shows this gate's advisory lines on a pass"
)
RUNNER_ECHO_TOKEN_ENV = "GRC_RUNNER_ECHO_TOKEN"


def _d10():
    """Load delta gate D10's module (hyphenated file name, so by path)."""
    spec = importlib.util.spec_from_file_location("_d10_claude_md_size", D10_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    # Every read of D10 and every computation on its values sits inside the try,
    # so any failure (an import error, a top-level NameError or sys.exit(), a
    # changed signature, a non-int count) exits 2, never the over-ceiling code 1
    # or D10's own exit code.
    try:
        d10 = _d10()
        lines = d10.line_count(d10.CLAUDE_MD)
        line_ceiling = d10.CEILING
        startup = d10.census(REPO_ROOT)["startup"]
        ceiling = d10.STARTUP_CHARACTER_CEILING
        warn_below = d10.STARTUP_HEADROOM_WARNING
        used = startup["characters"]
        files = startup["files"]
        for name, value in (("line count", lines), ("CEILING", line_ceiling),
                            ("characters", used), ("files", files),
                            ("STARTUP_CHARACTER_CEILING", ceiling),
                            ("STARTUP_HEADROOM_WARNING", warn_below)):
            if type(value) is not int:
                raise TypeError(f"{name} is {type(value).__name__} {value!r}, not int")
        line_code, line_message = d10.evaluate(lines, line_ceiling)
        if type(line_code) is not int or line_code not in (0, 1):
            raise TypeError(f"evaluate() returned code {line_code!r}, not int 0 or 1")
        if type(line_message) is not str:
            raise TypeError(f"evaluate() returned message {line_message!r}, not str")
        headroom = ceiling - used
        over = used > ceiling
        warn = headroom < warn_below
        summary = (f"{used} startup characters in {files} files, "
                   f"ceiling {ceiling}, headroom {headroom}")
        code = 1 if over else line_code
    except (Exception, SystemExit) as exc:
        print(f"ERROR: D10 load or census failed: {type(exc).__name__}: {exc} "
              f"{getattr(exc, '__notes__', [])}", file=sys.stderr)
        return 2
    token = os.environ.get(RUNNER_ECHO_TOKEN_ENV, "")
    if token:
        print(RUNNER_ECHO_MARKER + " " + token)
    print(line_message)
    if over:
        print(f"FAIL: startup character ceiling {ceiling} exceeded ({summary}). "
              "Trim or relocate always-loaded text (.claude/CLAUDE.md and every "
              "unscoped .claude/rules/ file); raising the ceiling needs explicit "
              "maintainer authorization (see tools/check-claude-md-size.py).")
    else:
        print(f"OK: {summary}.")
    if warn:
        print(f"WARN: startup headroom is {headroom} characters (under {warn_below}, "
              "D10's warning threshold); preserve clauses when making room.")
    return code


if __name__ == "__main__":
    # As gate 72 does: this tool takes no argument; an unknown or surplus one
    # is refused (exit 2) before the check runs.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from lint_common import strict_flags
    strict_flags(sys.argv[1:], ())
    sys.exit(main())
