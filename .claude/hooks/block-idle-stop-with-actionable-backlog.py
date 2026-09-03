#!/usr/bin/env python3
"""Stop-hook arm: refuse an IDLE-STOP while authorized backlog remains.

RETIRED 2026-09-03 (registration only): SUPERSEDED as the active Stop guard by the fleet-canonical
`stop-guard-unattended.py` (lab_infra "No Manufactured Wind-Down" adoption). This file is RETAINED on
disk (its unit tests still validate this logic; its `.allow-idle-stop` escape is preserved by the new
guard) but is NO LONGER registered in .claude/settings.json. Kept pending full retirement once the
canonical guard is proven.

Origin: 2026-08-27. The orchestrator finished a GO'd program (exception-authority
Wave 2), wrote the close-out + handoff, then ENDED THE TURN claiming "the queue is
exhausted and the rest is yours to decide" -- while ~96 ACTIONABLE backlog items and
eight already-authorized, decision-free tooling PRs sat unstarted. That is the
no-idle-stop anti-pattern (session-lifecycle rule S4; CLAUDE.md attended-autonomous
item 4). It had been observed and seeded before (guardrail-seed inbox
``SEED-idle-stop-in-unattended-with-queue.md``, 2026-08-21, an overnight recurrence)
and recurred anyway, which is exactly the case a prose rule needs a mechanical
backstop for.

The pre-existing ``block-turn-end-with-outstanding-work.py`` Stop arm cannot catch
this: it fires only on an unmerged feature branch, and at an idle-stop the last PR is
already merged (no branch), so an idle-stop with a full authorized QUEUE is invisible
to it (its own docstring admits blindness to "an unfinished task list").

WHAT THIS ARM DOES. At turn-end, if the session Operating-mode is one where the
maintainer is NOT watching every step (``attended-autonomous`` or either unattended
mode) AND the backlog audit reports >=1 ACTIONABLE item AND there is no explicit
stop-authorization, it BLOCKS once and names the next action. In those modes a
yield-with-work-remaining is an idle-stop unless a legitimate wait is declared.

The escape IS the declaration. A genuine reason to yield in these modes -- waiting on
CI, on a dispatched worker, on a maintainer decision, or a real session-closing
wind-down -- is declared by ``touch "${GRC_DROP_ROOT:-/opt/grc/grc_working}/.allow-idle-stop"`` (default ``/opt/grc/grc_working/.allow-idle-stop`` when GRC_DROP_ROOT is unset; this guard's
OWN one-shot sentinel, distinct from the branch guard's ``.allow-stop`` so the two never
race on a shared file under parallel Stop-hook execution). A wait during branch-bearing
work declares both. The reliable loop-terminator remains ``stop_hook_active``.

DESIGN INVARIANTS (each mirrors ``block-turn-end-with-outstanding-work.py``):
  * FAIL OPEN. Any exception, unreadable/ambiguous state, unknown mode, or audit
    failure resolves the blocking predicate to False (allow), with one deliberate
    exception: a failed escape CONSUMPTION (a caught unlink error) refuses the escape
    rather than granting it, then continues through the normal blocking predicate. The
    only path that blocks is the fully-parsed happy path. A guard that wedges the session
    on its own malfunction gets removed, and a removed guard protects nothing.
  * LOOP-SAFE. ``stop_hook_active`` -> allow, so it blocks at most once per stop
    attempt; the continuation then proceeds.
  * WORKER-EXEMPT. A dispatched worker cannot discharge or escape this (it has no
    backlog to work and no writable escape root), so a worker session -> allow.
  * ONE-SHOT ESCAPE. ``.allow-idle-stop`` (this guard's OWN sentinel, not shared with the
    branch guard) is consumed at the TOP of main() on any turn-end where it is present AND
    deletable; the escape is honoured ONLY after a successful deletion, so a failed unlink
    refuses the escape rather than granting it, and no path -- malformed or non-object
    payload, worker, or continuation -- can leak a consumed sentinel to a later stop, and no
    parallel-execution race with a sibling can consume it first.

RESIDUE, stated per the guard-inputs discipline:
  * "ACTIONABLE count >= 1" is a PROXY for "productive authorized work remains". It is
    the backlog audit's OWN classification, so a genuinely-blocked queue (every item
    carrying a maintainer-approved ``[BLOCKED:]`` tag) reports 0 ACTIONABLE and this
    arm does NOT trap a correctly-halted session. It cannot see uncommitted work (the
    sibling branch guard is itself BLIND to uncommitted changes; discipline covers them,
    not a guard) or a running background task (the declared-wait escape covers that).
  * Only ``attended-autonomous`` and the unattended modes arm it. FULLY ``attended``
    (the maintainer is watching and directing) -> allow: a yield there is normal.

Stdlib only. Exit 2 + reason on stderr to block (mirrors the sibling arm); exit 0 to
allow. ``--self-test`` runs the pure-logic cases and prints ``self-test: OK``.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from _hookutil import is_worker_session
except Exception:                                  # pragma: no cover - fail OPEN on import trouble
    def is_worker_session() -> bool:               # noqa: D103
        return True

REPO = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
ESCAPE_FILE = Path((os.environ.get("GRC_DROP_ROOT") or "/opt/grc/grc_working")) / ".allow-idle-stop"

# Modes where the maintainer is NOT watching every step, so a yield with authorized
# work remaining is an idle-stop unless a wait is declared. Fully "attended" is absent
# by design.
ARMED_MODES = {"attended-autonomous", "overnight-unattended", "daytime-unattended"}
# Every recognized lease mode. A parsed value outside this set is treated as
# unrecognized (None), so a word captured by accident from prose never arms the hook.
KNOWN_MODES = ARMED_MODES | {"attended", "fully-attended", "unattended"}

_TOOLS_DIR = str(Path(__file__).resolve().parents[2] / "tools")
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
try:
    from lint_common import resolve_working as _resolve_working
except Exception:                                  # pragma: no cover
    _resolve_working = None


def _session_state_path():
    """`session-state.md` resolved via the store-aware resolver (local store first)."""
    if _resolve_working is not None:
        try:
            p = _resolve_working("session-state.md", repo_root=REPO)
            if p:
                return Path(p)
        except Exception:
            pass
    return None


def _parse_mode(text: str) -> str | None:
    """Pure: extract the Operating-mode value from session-state text, or None.

    Requires the KEY syntax ``Operating-mode:`` (the colon is mandatory; markdown
    bold and a backtick-wrapped value are tolerated), so a prose sentence that merely
    begins with the words "Operating-mode" (no colon) does NOT arm the hook. First
    match wins. Testable without a filesystem.
    """
    pat = re.compile(
        r"^\**[^\S\n]*Operating-mode\**[^\S\n]*:[^\S\n]*\**[^\S\n]*`?([A-Za-z][A-Za-z-]*)`?\**[^\S\n]*\\?[^\S\n]*$"
    )
    # splitlines() splits on EVERY Unicode line boundary (\n \r \v \f
    # \x1c-\x1e \x85 \u2028 \u2029), so a key and value separated by any of
    # them land on different physical lines and cannot both match one anchored
    # line. This closes the vertical-whitespace false-arm that re.MULTILINE +
    # [^\S\n] left open (\n-only line anchoring treated \v/\f/NEL/LS/PS as
    # intra-line whitespace). First matching physical line wins.
    for line in text.splitlines():
        m = pat.match(line)
        if m:
            v = m.group(1).strip().lower()
            if v in KNOWN_MODES:
                return v
    return None


def operating_mode() -> str | None:
    """The lease Operating-mode, lowercased, or None if unreadable/ambiguous."""
    p = _session_state_path()
    if p is None:
        return None
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
    return _parse_mode(text)


def actionable_count() -> int | None:
    """ACTIONABLE backlog count from the authoritative audit, or None on any failure.

    Parses the audit's own summary line ("... ; K ACTIONABLE.") so the BLOCKED-vs-
    ACTIONABLE classification is the audit's, not re-derived here.
    """
    script = Path(_TOOLS_DIR) / "audit-backlog-actionability.py"
    if not script.exists():
        return None
    try:
        out = subprocess.run(
            [sys.executable, str(script), "--actionable-only"],
            capture_output=True, text=True, timeout=15, cwd=str(REPO),
        )
    except Exception:
        return None
    if out.returncode != 0:
        return None
    m = re.search(r";\s*(\d+)\s+ACTIONABLE\b", out.stdout)
    if not m:
        # tolerate a summary phrased "K ACTIONABLE" without the leading semicolon
        m = re.search(r"\b(\d+)\s+ACTIONABLE\b", out.stdout)
    if not m:
        return None
    try:
        return int(m.group(1))
    except ValueError:
        return None


def decide(stop_hook_active: bool, worker: bool, escape: bool,
           mode: str | None, actionable: int | None) -> str | None:
    """Pure decision, so it is testable without a repo, a lease, or the audit.

    Returns the block message, or None to allow. Blocks only on the fully-resolved
    happy path; every ambiguous input allows.
    """
    if stop_hook_active or worker or escape:
        return None
    if mode is None or mode not in ARMED_MODES:
        return None
    if actionable is None or actionable < 1:
        return None
    return (
        f"IDLE-STOP BLOCKED: Operating-mode is {mode} (no-idle-stop) and the backlog "
        f"audit reports {actionable} ACTIONABLE item(s). A yield here is an idle-stop "
        "unless a wait is declared.\n"
        "  Next action: pull the highest-priority ACTIONABLE item and do it (or dispatch it), "
        "PR-by-PR. Run `python3 tools/audit-backlog-actionability.py --actionable-only` for the list.\n"
        "  If this is a GENUINE wait (CI, a dispatched worker, a maintainer decision, or a real "
        "session-closing wind-down), declare it:\n"
        f"      touch {ESCAPE_FILE}   # this guard\x27s own one-shot sentinel\n"
        "  (the branch guard block-turn-end uses a SEPARATE .allow-stop; a wait during branch-bearing\n"
        "   work declares both. Distinct sentinels avoid a parallel-execution race on one shared file.)"
    )


def main() -> int:
    # Consume the one-shot escape at the very TOP, before any parsing, so it can NEVER
    # survive a completed stop (malformed payload, non-object payload, worker, or
    # continuation) and authorize a later one. Whether it was declared decides this stop.
    escape_declared = False
    try:
        if ESCAPE_FILE.exists():
            try:
                ESCAPE_FILE.unlink()
                escape_declared = True        # honour the escape ONLY if it was actually
            except OSError:                   # consumed; a failed unlink must NOT grant a
                pass                          # persistent authorization on later stops
    except Exception:
        pass
    try:
        payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except Exception:
        return 0                              # unparseable payload: fail open (escape already consumed)
    if not isinstance(payload, dict):
        return 0                              # non-object payload: fail open (escape already consumed)
    try:
        if payload.get("stop_hook_active"):
            return 0
        if is_worker_session():
            return 0
        if escape_declared:
            return 0
        message = decide(False, False, False, operating_mode(), actionable_count())
        if message:
            print(message, file=sys.stderr)
            return 2
    except Exception:
        return 0                              # fail open, deliberately
    return 0


SELF_TEST = [
    # (label, (stop_hook_active, worker, escape, mode, actionable), expect_block)
    ("continuation never blocks",        (True,  False, False, "attended-autonomous", 9),  False),
    ("worker session never blocks",      (False, True,  False, "overnight-unattended", 9), False),
    ("escape file never blocks",         (False, False, True,  "attended-autonomous", 9),  False),
    ("attended-autonomous + work blocks",(False, False, False, "attended-autonomous", 9),  True),
    ("overnight-unattended + work blocks",(False, False, False, "overnight-unattended", 1),True),
    ("daytime-unattended + work blocks", (False, False, False, "daytime-unattended", 5),   True),
    ("armed mode + zero actionable ok",  (False, False, False, "attended-autonomous", 0),  False),
    ("fully-attended never blocks",      (False, False, False, "attended", 9),             False),
    ("unknown mode never blocks",        (False, False, False, "some-other-mode", 9),      False),
    ("no mode (unreadable) never blocks",(False, False, False, None, 9),                   False),
    ("audit-failed count None never blocks",(False, False, False, "attended-autonomous", None), False),
]


def _self_test() -> int:
    failures = []
    for label, args, expect in SELF_TEST:
        got = decide(*args) is not None
        if got != expect:
            failures.append(f"  {label}: expected block={expect}, got block={got}")
    if failures:
        print("self-test: FAIL\n" + "\n".join(failures))
        return 1
    print(f"self-test: OK ({len(SELF_TEST)} cases)")
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv[1:]:
        raise SystemExit(_self_test())
    raise SystemExit(main())
