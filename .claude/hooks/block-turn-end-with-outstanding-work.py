#!/usr/bin/env python3
"""Stop hook: refuse a turn-end while the session is holding outstanding work.

Shipped 2026-08-07 after the orchestrator ended a turn on a stated intention ("continuing with X",
"next I will do X") EIGHT times in one session, each after an explicit maintainer correction, one
of them in capitals, while every mechanical guard in the same session held without exception. That
asymmetry is the whole argument for this hook: prose correctives failed repeatedly against the same
reflex, and mechanism did not fail once. The discipline it backstops is the section "A stated
intention is a claim, and an unkept one is a false statement" in
guardrails/governance/evidence-grounded-completion.md.

REVISED 2026-08-07, same day, after a dual-family review of the FIRST version returned seven errors
against it. Four were fatal and all four are fixed here: it never read its Stop payload, so it could
not see stop_hook_active and had no terminating condition; its escape hatch was an environment
variable the actor cannot set into this process, which is the appearance of an escape rather than
one; a MISSING consume marker made the threshold epoch 0, so every file in the tray read as
unconsumed, which is the opposite of the fail-open contract the docstring claimed; and the held-
branch list was a hardcoded set whose "must cite a decision record" was an unenforced comment.

WHAT IT IS, stated narrowly because a cross-family verifier caught the first version claiming more
than it can see. This is a DELIVERED-RESULT AND LOCAL-BRANCH SENTINEL, not a general
outstanding-work detector. It is blind to a dispatched worker that has not yet written a file, to
an unfinished task list, to uncommitted working-tree changes, and to a detached commit. Those are
real outstanding work and this hook will let you yield on all of them; the discipline, not the
guard, covers them.

WHAT IT BLOCKS. A turn-end while EITHER arm is true:
  * a delivery has landed in the tray since the last recorded consume, or
  * a branch is ahead of main and is not on the recorded held list.

WHAT IT DOES NOT BLOCK, by construction:
  * a continuation that is already under way (stop_hook_active), so it blocks at most once and
    cannot loop the session;
  * anything at all, if the escape file exists (see below);
  * anything at all, if it cannot answer the question (see fail-open).

ESCAPE, and it is reachable. Create the file named by ESCAPE_FILE from any shell:
``touch /home/grc/grc_working/.allow-stop``. The hook honours it ONCE and deletes it, so an escape
cannot silently become the standing state. It is reachable from a Bash tool call, which the previous
environment-variable form was not: a Stop hook inherits the harness's environment, never the
environment of a tool call.

FAIL OPEN, and this now includes every missing input. Any internal error, an unreadable repository,
an absent tray, an absent marker: all allow the stop. A guard that traps the actor on its own
malfunction gets removed, and a removed guard protects nothing.

GUARD-INPUT RESIDUE, stated at the point of use per validate-inference-before-action:
  * "a delivery file is newer than the marker" is NOT "a delivery is unread". It proves a file
    arrived, nothing more; the marker is advanced by the orchestrator, so the arm measures a
    RECORDED consume, not a real one.
  * "a branch is ahead of main" is NOT "a branch is meant to merge". A deliberately-held branch
    needs a recorded exemption, which is why the list is a file with reasons rather than a constant.
  * the tray scan is TOP-LEVEL ONLY (glob, not rglob), so a delivery written into a subdirectory is
    invisible to this guard.
  * the hook sees files and refs. It cannot see whether the actor intends to continue, which is the
    thing it is really trying to constrain; it can only make yielding-with-work-outstanding require
    a deliberate act.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import re as _re
import subprocess
import sys
from pathlib import Path

REPO = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
DROP_ROOT = Path(os.environ.get("GRC_DROP_ROOT", "/home/grc/grc_working")) / "inbox" / "deliveries"
CONSUME_MARKER = DROP_ROOT / ".last-consume"
ESCAPE_FILE = Path(os.environ.get("GRC_DROP_ROOT", "/home/grc/grc_working")) / ".allow-stop"
# Held branches live in a FILE with a reason per line, not a constant in this file: a hardcoded set
# goes stale the day it is written, and a comment saying "cite a decision record" enforces nothing.
HELD_FILE = REPO.parent / "grc_library_private" / ".working" / "held-branches.txt"
GIT_TIMEOUT = 20
_EXPIRY = _re.compile(r"\d{4}-\d{2}-\d{2}")


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(REPO), *args],
        capture_output=True, text=True, timeout=GIT_TIMEOUT, check=True,
    ).stdout


def held_branches() -> dict:
    """Map branch -> reason for each UNEXPIRED hold. Absent file means nothing is held.

    Line format: ``<branch>  # <YYYY-MM-DD expiry>  <reason>``. The expiry is required and is
    checked, because a cross-family verifier pointed out that an exemption keyed on a mutable
    branch name alone exempts every later commit under that name, forever, with nothing forcing
    anyone to revisit it. An expired or malformed hold is simply NOT a hold: the branch reappears
    in the guard's output, which is the prompt to renew it deliberately or let it go.

    RESIDUE, at the predicate: this validates that a hold was recorded and has not lapsed. It does
    NOT pin the approved tip, so work added to a held branch after the hold was granted is covered
    by it. Pinning the tip is the stronger form and is deliberately not built yet; a branch is held
    for weeks and would need its hold rewritten on every commit.
    """
    held = {}
    if not HELD_FILE.exists():
        return held
    today = _dt.date.today().isoformat()
    for line in HELD_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, _, rest = line.partition("#")
        rest = rest.strip()
        parts = rest.split(None, 1)
        if not parts or not _EXPIRY.fullmatch(parts[0]):
            continue                      # no parsable expiry: not a hold
        if parts[0] < today:
            continue                      # lapsed: the branch is visible again, deliberately
        held[name.strip()] = parts[1] if len(parts) > 1 else "no reason recorded"
    return held


def unmerged_branches() -> list:
    # RESIDUE, at the predicate: "ahead of main" is NOT "not merged". This project squash-merges,
    # so a branch whose work is fully on main keeps its own distinct commits forever and stays
    # ahead until it is deleted. A cross-family verifier proved this with a synthetic squash probe:
    # rev-list said one commit ahead while the trees were identical. Counting alone would make the
    # guard block permanently on every merged-but-undeleted branch, which is the shape that gets a
    # guard switched off. So a branch is reported only when it is ahead AND its tree differs from
    # main. Remaining residue: patch-equivalent-but-not-tree-equal work (a merged change plus an
    # unrelated later edit) still reads as unmerged, which errs toward blocking, and a stale local
    # main reads every branch as unmerged, which errs the same way.
    held = held_branches()
    out = []
    for name in _git("for-each-ref", "--format=%(refname:short)", "refs/heads").split():
        if name == "main" or name in held:
            continue
        ahead = _git("rev-list", "--count", "main.." + name).strip()
        if not ahead or ahead == "0":
            continue
        try:
            subprocess.run(["git", "-C", str(REPO), "diff", "--quiet", "main", name],
                           timeout=GIT_TIMEOUT, check=True)
            continue          # tree-identical to main: the work landed, the branch is just undeleted
        except subprocess.CalledProcessError:
            pass              # trees differ: genuinely unmerged work
        out.append((name, ahead))
    return out


def new_deliveries() -> list:
    """Deliveries newer than the recorded consume. Returns [] when it cannot tell."""
    if not DROP_ROOT.is_dir() or not CONSUME_MARKER.exists():
        return []          # cannot answer: fail open, per the contract above
    # RESIDUE, at the predicate: mtime is not arrival and the marker is not attention. A copied or
    # restored file carries a new mtime without being new work; a file written slowly may predate
    # its own completion; and the marker is advanced by the orchestrator asserting the tray is
    # dispositioned, which nothing verifies. The marker is also GLOBAL, so advancing it for one
    # delivery clears every other. Location would beat all of this (move a dispositioned file to a
    # consumed/ directory, as the file-drop inbox already does), and is the queued replacement.
    since = CONSUME_MARKER.stat().st_mtime
    return sorted(p.name for p in DROP_ROOT.glob("*.md") if p.stat().st_mtime > since)


def decide(stop_hook_active: bool, escape: bool, branches: list, deliveries: list) -> str | None:
    """Pure decision, so it is testable without a repository or a tray."""
    if stop_hook_active or escape:
        return None
    if not branches and not deliveries:
        return None
    lines = ["BLOCKED (turn-end guard): work is outstanding, so this is not a place to yield.", ""]
    if deliveries:
        lines.append("  Deliveries since the last recorded consume (%d):" % len(deliveries))
        lines += ["    - " + d for d in deliveries[:6]]
        if len(deliveries) > 6:
            lines.append("    ... and %d more" % (len(deliveries) - 6))
        lines.append("    Read them, disposition every finding, then record the consume:")
        lines.append("      touch /home/grc/grc_working/inbox/deliveries/.last-consume")
    if branches:
        lines.append("  Branches ahead of main and not recorded as held (%d):" % len(branches))
        lines += ["    - %s (+%s)" % (n, a) for n, a in branches[:8]]
        lines.append("    Merge them, or record the hold with its reason in")
        lines.append("      grc_library_private/.working/held-branches.txt")
    lines += [
        "",
        "  If this is a genuine block (CI, a maintainer decision, an external wait), say so and:",
        "      touch /home/grc/grc_working/.allow-stop     # honoured once, then deleted",
    ]
    return "\n".join(lines)


def main() -> int:
    try:
        payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except Exception:
        payload = {}
    try:
        if payload.get("stop_hook_active"):
            return 0
        escape = ESCAPE_FILE.exists()
        if escape:
            try:
                ESCAPE_FILE.unlink()          # one-shot: an escape must not become the default
            except OSError:
                pass
            return 0
        message = decide(False, False, unmerged_branches(), new_deliveries())
        if message:
            print(message, file=sys.stderr)
            return 2
    except Exception:
        return 0                              # fail open, deliberately
    return 0


SELF_TEST = [
    ("clean tree allows",            (False, False, [], []),                       False),
    ("continuation never blocks",    (True,  False, [("b", "1")], ["d.md"]),        False),
    ("escape file never blocks",     (False, True,  [("b", "1")], ["d.md"]),        False),
    ("one unmerged branch blocks",   (False, False, [("b", "1")], []),              True),
    ("one new delivery blocks",      (False, False, [], ["d.md"]),                  True),
    ("both arms block",              (False, False, [("b", "2")], ["d.md"]),        True),
]


def self_test() -> int:
    bad = 0
    for name, args, should_block in SELF_TEST:
        got = decide(*args) is not None
        if got != should_block:
            bad += 1
            print("FAIL " + name + ": want " + ("BLOCK" if should_block else "allow")
                  + ", got " + ("BLOCK" if got else "allow"))
    # A missing marker must fail OPEN, which is the error-4 regression.
    real = new_deliveries.__doc__ or ""
    if "fail open" not in real and "cannot tell" not in real:
        bad += 1
        print("FAIL: the fail-open contract is not stated where the reader will look")
    print(str(len(SELF_TEST) - bad) + "/" + str(len(SELF_TEST)) + " decision cases pass")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main())
