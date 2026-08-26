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
one; and the held-branch list was a hardcoded set whose "must cite a decision record" was an
unenforced comment.

WHAT IT IS, stated narrowly because a cross-family verifier caught the first version claiming more
than it can see. This is a LOCAL-BRANCH SENTINEL, not a general
outstanding-work detector. It is blind to a still-running dispatched worker, to an unfinished task list, to uncommitted
working-tree changes, and to a detached commit. Those are
real outstanding work and this hook will let you yield on all of them; the discipline, not the
guard, covers them.

WHAT IT BLOCKS. A turn-end while a branch is ahead of main and is not on the recorded held list.

WHAT IT DOES NOT BLOCK, by construction:
  * a continuation that is already under way (stop_hook_active), so it blocks at most once and
    cannot loop the session;
  * anything at all, if the escape file exists (see below);
  * anything at all, if it cannot answer the question (see fail-open);
  * anything at all, inside a dispatched worker session: a worker's fan-out cannot discharge any of
    this guard's remedies, so the check is skipped there (#1695).

ESCAPE, and it is reachable. Create the file named by ESCAPE_FILE from any shell:
``touch /opt/grc/grc_working/.allow-stop``. The hook honours it ONCE and deletes it, so an escape
cannot silently become the standing state. It is reachable from a Bash tool call, which the previous
environment-variable form was not: a Stop hook inherits the harness's environment, never the
environment of a tool call.

FAIL OPEN. Any internal error or an unreadable repository allows the stop. A guard that traps the
actor on its own malfunction gets removed, and a removed guard protects nothing.

GUARD-INPUT RESIDUE, stated at the point of use per validate-inference-before-action:
  * "a branch is ahead of main" is NOT "a branch is meant to merge". A deliberately-held branch
    needs a recorded exemption, which is why the list is a file with reasons rather than a constant.
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from _hookutil import is_worker_session
except Exception:                                  # pragma: no cover - fail OPEN on import trouble
    def is_worker_session() -> bool:               # noqa: D103
        return True

REPO = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
ESCAPE_FILE = Path(os.environ.get("GRC_DROP_ROOT", "/opt/grc/grc_working")) / ".allow-stop"
# Held branches live in a FILE with a reason per line, not a constant in this file: a hardcoded set
# goes stale the day it is written, and a comment saying "cite a decision record" enforces nothing.
# The file is resolved via the store-aware resolver (local operational store preferred, the
# grc_library_private/.working sibling a transitional fallback), never a hardcoded sibling-store path,
# so this guard follows the migration of the working store to local. Fail-safe: a resolver-load
# failure leaves _resolve_working None and _working_file falls back to the in-repo .working/ path.
_TOOLS_DIR = str(Path(__file__).resolve().parents[2] / "tools")
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
try:
    from lint_common import resolve_working as _resolve_working
except Exception:  # pragma: no cover - fail-safe: never let a helper-load failure break the hook
    _resolve_working = None


def _working_file(rel_below, root):
    """`.working/<rel_below>` resolved via lint_common (local store preferred), or None."""
    if _resolve_working is not None:
        return _resolve_working(rel_below, repo_root=root)
    cand = root / ".working" / rel_below
    return cand if cand.exists() else None


HELD_FILE = _working_file("held-branches.txt", REPO)
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
    if HELD_FILE is None or not HELD_FILE.exists():
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




def decide(stop_hook_active: bool, escape: bool, branches: list) -> str | None:
    """Pure decision, so it is testable without a repository."""
    if stop_hook_active or escape:
        return None
    if not branches:
        return None
    lines = ["BLOCKED (turn-end guard): work is outstanding, so this is not a place to yield.", ""]
    if branches:
        lines.append("  Branches ahead of main and not recorded as held (%d):" % len(branches))
        lines += ["    - %s (+%s)" % (n, a) for n, a in branches[:8]]
        lines.append("    Merge them, or record the hold with its reason in")
        # Show the ACTUAL resolved held-branches path (resolve_working -> local store), never a
        # hardcoded sibling path, so the remediation the guard prints follows the store migration.
        lines.append("      %s" % (HELD_FILE if HELD_FILE is not None
                                   else "the held-branches file (resolved via lint_common.resolve_working)"))
    lines += [
        "",
        "  If this is a genuine block (CI, a maintainer decision, an external wait), say so and:",
        "      touch /opt/grc/grc_working/.allow-stop     # honoured once, then deleted",
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
        if is_worker_session():
            # A dispatched worker cannot discharge ANY of this guard's remedies: it cannot
            # merge the orchestrator's branch (merging is orchestrator-only work), it cannot
            # write the `_private` held-branches record, and it cannot create the escape file,
            # all three sitting outside a worker's writable root. So the guard could only wedge
            # a worker at the end of an order it had already completed. The branch it names is
            # the ORCHESTRATOR's outstanding work, and the orchestrator's own turn-end is where
            # that gets enforced. Observed 2026-08-20: a /validate-pr worker delivered its full
            # verdict, then spent its remaining turns unable to satisfy or escape this guard.
            return 0
        escape = ESCAPE_FILE.exists()
        if escape:
            try:
                ESCAPE_FILE.unlink()          # one-shot: an escape must not become the default
            except OSError:
                pass
            return 0
        message = decide(False, False, unmerged_branches())
        if message:
            print(message, file=sys.stderr)
            return 2
    except Exception:
        return 0                              # fail open, deliberately
    return 0


SELF_TEST = [
    ("clean tree allows",            (False, False, []),           False),
    ("continuation never blocks",    (True,  False, [("b", "1")]), False),
    ("escape file never blocks",     (False, True,  [("b", "1")]), False),
    ("one unmerged branch blocks",   (False, False, [("b", "1")]), True),
]


def self_test() -> int:
    import io
    from unittest import mock

    bad = 0
    for name, args, should_block in SELF_TEST:
        got = decide(*args) is not None
        if got != should_block:
            bad += 1
            print("FAIL " + name + ": want " + ("BLOCK" if should_block else "allow")
                  + ", got " + ("BLOCK" if got else "allow"))

    # Worker scoping lives in main(), not the pure branch decision. Assert that a
    # positively identified worker returns before it probes either the escape or branches.
    module = sys.modules[__name__]
    worker_escape = mock.Mock()
    with mock.patch.dict(
        os.environ, {"CLAUDE_CONFIG_DIR": "/run/orch/orch-worker.Ab3xZ9"}
    ), mock.patch.object(
        sys, "stdin", io.StringIO("{}")
    ), mock.patch.object(
        module, "ESCAPE_FILE", worker_escape
    ), mock.patch.object(
        module, "unmerged_branches"
    ) as branch_scan:
        worker_rc = main()
    if worker_rc != 0 or worker_escape.exists.called or branch_scan.called:
        bad += 1
        print("FAIL worker session allows before escape/branch probes")

    # A normal orchestrator path must retain the current branch-blocking contract.
    orchestrator_escape = mock.Mock()
    orchestrator_escape.exists.return_value = False
    with mock.patch.dict(
        os.environ, {"CLAUDE_CONFIG_DIR": "/opt/orch-accounts/test/orchestrator"}
    ), mock.patch.object(
        sys, "stdin", io.StringIO("{}")
    ), mock.patch.object(
        sys, "stderr", io.StringIO()
    ), mock.patch.object(
        module, "ESCAPE_FILE", orchestrator_escape
    ), mock.patch.object(
        module, "unmerged_branches", return_value=[("b", "1")]
    ) as branch_scan:
        orchestrator_rc = main()
    if orchestrator_rc != 2 or branch_scan.call_count != 1:
        bad += 1
        print("FAIL orchestrator session did not retain branch block")

    total = len(SELF_TEST) + 2
    print(str(total - bad) + "/" + str(total) + " decision cases pass")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main())
