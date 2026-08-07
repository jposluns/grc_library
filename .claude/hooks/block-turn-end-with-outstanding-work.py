#!/usr/bin/env python3
"""Stop hook: refuse turn-end while the orchestrator has outstanding, actionable work.

WHY THIS EXISTS
The orchestrator ended a turn on a stated intention ("continuing with X", "next I will
do X") seven times in one session, each after an explicit maintainer correction, once in
capitals. Prose correctives failed seven times; every mechanical guard in this repository
held. The maintainer's framing is the operative one: a turn ending on "continuing with X"
that then does not continue is not a pause, it is a FALSE STATEMENT about the assistant's
own next action, so it belongs to the accuracy facet rather than to workflow tidiness.

WHAT IT BLOCKS
Turn-end when either holds:
  (a) a dispatched worker DELIVERED a result that has not been marked consumed, or
  (b) a feature branch carries commits not reachable from origin/main.

GUARD-INPUT RESIDUE (validate-inference-before-action, "Guard inputs")
Stated at the point of use, because both observables are proxies:
  - "delivered" is a file in the deliveries tray newer than the consume marker. It shows
    a delivery arrived and was not marked consumed. It does NOT show the content is
    unread, nor that the delivery is semantically complete.
  - "unmerged" is commits on a local claude/* branch not reachable from origin/main. It
    does NOT show the branch is meant to merge; a deliberately-held branch looks
    identical, which is why HELD_BRANCHES exists and must cite a decision record.

FAIL-OPEN, DELIBERATELY
Any internal error, missing path or git failure allows the stop. A guard that traps the
assistant on its own malfunction gets switched off, and a switched-off guard protects
nothing. This catches the routine case; it is not meant to be inescapable.

ESCAPE HATCH
GRC_ALLOW_STOP=1 allows one stop, for a genuine block (CI, a maintainer decision, an
external wait). Its use is visible in shell history, which is the point: an escape that
leaves no trace becomes the default.
"""
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DROP_ROOT = Path("/home/grc/grc_working")
DELIVERIES = DROP_ROOT / "inbox" / "deliveries"
CONSUME_MARKER = DROP_ROOT / ".last-consume"

# Branches deliberately held by a recorded maintainer decision. A held branch is not
# outstanding work. Keep this short and cite the record for each entry.
HELD_BRANCHES = {
    # HELD per the 2026-08-04 attended resolution: "1.26.9 HELD (batch more umbrella
    # rules -> one /guardrails review + gate 81)".
    "claude/1.26.9-cost-tier",
}


def _git(*args):
    return subprocess.run(
        ["git", "-C", str(REPO), *args],
        capture_output=True, text=True, timeout=15,
    ).stdout.strip()


def unmerged_branches():
    out = _git("for-each-ref", "--format=%(refname:short)", "refs/heads/claude")
    found = []
    for branch in filter(None, out.splitlines()):
        if branch in HELD_BRANCHES:
            continue
        ahead = _git("rev-list", "--count", "origin/main.." + branch)
        if ahead.isdigit() and int(ahead) > 0:
            found.append(branch + " (+" + ahead + ")")
    return found


def unconsumed_deliveries():
    if not DELIVERIES.is_dir():
        return []
    since = CONSUME_MARKER.stat().st_mtime if CONSUME_MARKER.exists() else 0
    return sorted(p.name for p in DELIVERIES.glob("*.md") if p.stat().st_mtime > since)


def main():
    if os.environ.get("GRC_ALLOW_STOP") == "1":
        return 0
    try:
        branches = unmerged_branches()
        deliveries = unconsumed_deliveries()
    except Exception:
        return 0  # fail open, deliberately

    if not branches and not deliveries:
        return 0

    out = ["BLOCKED (turn-end guard): outstanding work exists, so the turn must not end.", ""]
    if deliveries:
        out.append("  Unconsumed deliveries (" + str(len(deliveries)) + "):")
        out += ["    - " + d for d in deliveries[:6]]
        if len(deliveries) > 6:
            out.append("    ... and " + str(len(deliveries) - 6) + " more")
        out.append("    Read each, then mark consumed: touch " + str(CONSUME_MARKER))
    if branches:
        out.append("  Unmerged branches (" + str(len(branches)) + "):")
        out += ["    - " + b for b in branches]
        out.append("    Finish and merge it, or add it to HELD_BRANCHES with its decision record.")
    out += [
        "",
        "Do the next unit of work in THIS turn. Ending on a stated intention",
        "('continuing with X') without doing it is a false statement about your own next",
        "action, not a pause.",
        "",
        "Genuinely blocked (CI, a maintainer decision, an external wait)? GRC_ALLOW_STOP=1.",
    ]
    print("\n".join(out), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
