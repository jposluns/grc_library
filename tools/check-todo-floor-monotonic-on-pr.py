#!/usr/bin/env python3
"""Delta gate D12: the public number floor is MONOTONIC across a PR.

``tools/todo-number-floor.json`` records the highest ordinal EVER allocated per public
backlog series (gate 91 generates the ``## Number allocation`` counters from it, and gate 78
reads it for the recycle check). Those checks enforce that a counter is not BELOW the floor,
but nothing stops a hand-edit from LOWERING the floor itself: a lowered floor rewinds a
counter and silently permits recycling a retired id (the floor is its own only witness).

This delta gate closes that direction: it compares the PR's floor against the base revision
and FAILS if any series' floor DECREASED or a series was dropped. The floor may only rise
(a new allocation) or stay put. Runs PR-time, like the other ``check-*-on-pr.py`` gates.

Usage:
  python3 tools/check-todo-floor-monotonic-on-pr.py [BASE_REF] [HEAD_REF]
    BASE_REF defaults to origin/main; HEAD_REF omitted means the working tree.

A collapsed range (base and head resolving to the same commit, or the working
tree holding the base's content in the argless form) is refused as
CANNOT-EVALUATE (exit 2), never reported as a clean reflexive pass: a collapsed
range is exactly how a gate run in the wrong clone presents (orchestrator
mistake 300), the same refusal D5, D9 and D13 give.
"""
import json
import os
import subprocess
import sys

FLOOR_PATH = "tools/todo-number-floor.json"


def _ref_resolves(ref):
    """True iff ``ref`` resolves to a commit. An invalid / unfetched base ref must NOT be
    read as 'the floor is new' (that would silently waive the monotonicity check): ignorance
    about the input is a first-class REFUSE, not a permit (guard-input discipline)."""
    return subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def _rev_parse(ref):
    """The commit SHA ``ref`` resolves to (caller has verified it resolves)."""
    return subprocess.check_output(
        ["git", "rev-parse", "--verify", f"{ref}^{{commit}}"], text=True,
        stderr=subprocess.DEVNULL).strip()


def _toplevel():
    """The repository top level git selects from the current directory, so a
    collapsed-range refusal can name the clone it resolved (wrong-clone diagnosis)."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True,
            stderr=subprocess.DEVNULL).strip()
    except subprocess.CalledProcessError:
        return "(no work tree)"


def _path_at_ref(ref, path):
    """True iff ``path`` exists in ``ref``'s tree (base valid AND path present)."""
    return subprocess.run(
        ["git", "cat-file", "-e", f"{ref}:{path}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def _git_show(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True,
                                   stderr=subprocess.DEVNULL)


def _parse(text):
    return {k: int(v) for k, v in json.loads(text).items() if not k.startswith("_")}


def find_violations(base, head):
    """Series where the head floor DECREASED below base or was dropped. Empty = monotonic."""
    out = []
    for series, base_v in base.items():
        if series not in head:
            out.append(f"series {series} dropped (was {base_v})")
        elif head[series] < base_v:
            out.append(f"series {series} floor decreased {base_v} -> {head[series]} "
                       "(rewinds a counter; permits recycling a retired id)")
    return out


def main(argv):
    if len(argv) > 3 or any(a.startswith("-") for a in argv[1:]):  # 3b50b2f: only the documented forms are accepted; anything else is a usage error (exit 2)
        sys.stderr.write("usage: check-todo-floor-monotonic-on-pr.py [<base-ref> [<head-ref>]]\n")
        return 2
    if len(argv) > 1:
        base_ref = argv[1]
    else:
        gh_base = os.environ.get("GITHUB_BASE_REF")
        base_ref = f"origin/{gh_base}" if gh_base else "origin/main"
    head_ref = argv[2] if len(argv) > 2 else None
    if not _ref_resolves(base_ref):
        sys.stderr.write(f"ERROR: base ref '{base_ref}' does not resolve to a commit; cannot "
                         "verify floor monotonicity (fetch the base, or pass a valid ref). "
                         "Refusing rather than waiving the check.\n")
        return 2
    # A collapsed range would read as the clean monotonic-reflexive OK; refuse it
    # instead (the wrong-clone signature the delta gates refuse, orchestrator
    # mistake 300), BEFORE the first-introduction OK below can fire.
    base_sha = _rev_parse(base_ref)
    if head_ref is not None:
        if _ref_resolves(head_ref) and _rev_parse(head_ref) == base_sha:
            sys.stderr.write(
                f"D12 CANNOT-EVALUATE: base {base_ref} and head {head_ref} resolve "
                f"to the same commit (repo={_toplevel()} base={base_sha} "
                f"head={base_sha}); the named range is empty, so nothing was "
                f"evaluated. If the change lives in a worktree, run from that "
                f"worktree, or pass a base..head range that selects the change.\n")
            return 2
    elif subprocess.run(["git", "diff", "--quiet", base_sha, "--"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        # Argless form: the head is the working tree; a tree identical to the
        # base is the same collapsed range (only exit 0 is equality; a diff
        # error falls through to the explicit comparison below).
        head_sha = _rev_parse("HEAD") if _ref_resolves("HEAD") else "(unborn HEAD)"
        sys.stderr.write(
            f"D12 CANNOT-EVALUATE: the working tree (the default head) holds the "
            f"same content as base {base_ref} (repo={_toplevel()} base={base_sha} "
            f"head={head_sha}, working tree); the range is empty, so nothing was "
            f"evaluated. If the change lives in a worktree, run from that "
            f"worktree, or pass a base..head range that selects the change.\n")
        return 2
    if not _path_at_ref(base_ref, FLOOR_PATH):
        # base is VALID but the floor did not exist there: first introduction, nothing to compare.
        print(f"OK: {FLOOR_PATH} is new at this base ({base_ref}); no prior floor to compare.")
        return 0
    base_text = _git_show(base_ref, FLOOR_PATH)
    try:
        head_text = _git_show(head_ref, FLOOR_PATH) if head_ref else \
            open(FLOOR_PATH, encoding="utf-8").read()
    except (subprocess.CalledProcessError, FileNotFoundError):
        sys.stderr.write(f"FAIL: {FLOOR_PATH} is missing at HEAD but present at {base_ref} "
                         "(the floor must never be removed).\n")
        return 1
    base, head = _parse(base_text), _parse(head_text)
    violations = find_violations(base, head)
    if violations:
        sys.stderr.write("FAIL: the public number floor is not monotonic vs "
                         f"{base_ref}: {'; '.join(violations)}. The floor may only rise or "
                         f"stay put; restore each decreased value in {FLOOR_PATH}.\n")
        return 1
    print(f"OK: {FLOOR_PATH} is monotonic vs {base_ref} "
          f"({len(base)} series, none decreased or dropped).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
