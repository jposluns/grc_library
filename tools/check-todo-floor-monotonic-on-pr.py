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


class _GitCallFailed(Exception):
    """A git call the argless collapsed-range check depends on failed: a
    nonzero status other than the documented difference status, or the call
    did not run. The caller refuses as CANNOT-EVALUATE instead of guessing
    collapsed or not-collapsed either way (3b530 round 4). ``str()`` names
    the failed call."""


def _worktree_matches_base(base_sha):
    """True iff the working tree holds exactly the base's content: no tracked
    difference from ``base_sha`` AND no untracked, non-ignored file. An
    untracked file -- including an untracked brand-new floor file, which the
    argless head read below would evaluate -- is working-tree content, not an
    empty range (3b530 round 3). The untracked check is exact (a file whose
    NAME is whitespace still counts), and both calls anchor to the repository
    top level, so a run from a subdirectory sees root files (3b530 round 4).
    A call that fails raises _GitCallFailed for the caller to refuse on."""
    try:
        top = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True,
            stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, OSError) as exc:
        raise _GitCallFailed(f"git rev-parse --show-toplevel ({exc})")
    try:
        diff_rc = subprocess.run(
            ["git", "-C", top, "diff", "--quiet", base_sha, "--"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
    except OSError as exc:
        raise _GitCallFailed(f"git diff --quiet (did not run: {exc})")
    if diff_rc == 1:
        # The documented difference status: a real tracked change, not collapsed.
        return False
    if diff_rc != 0:
        raise _GitCallFailed(f"git diff --quiet (exit {diff_rc})")
    try:
        listing = subprocess.run(
            ["git", "-C", top, "ls-files", "--others", "--exclude-standard"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    except OSError as exc:
        raise _GitCallFailed(f"git ls-files --others (did not run: {exc})")
    if listing.returncode != 0:
        raise _GitCallFailed(f"git ls-files --others (exit {listing.returncode})")
    return listing.stdout == ""


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
        if not _ref_resolves(head_ref):
            # An unresolvable NAMED head must not be read as 'the working tree'
            # or reach the first-introduction OK below: like the base guard
            # above, ignorance about the input is a refusal, not a waiver
            # (3b530 round 3).
            sys.stderr.write(
                f"D12 CANNOT-EVALUATE: head ref '{head_ref}' does not resolve to "
                f"a commit (repo={_toplevel()} base={base_sha}); cannot verify "
                "floor monotonicity (fetch the head, or pass a valid ref). "
                "Refusing rather than waiving the check.\n")
            return 2
        if _rev_parse(head_ref) == base_sha:
            sys.stderr.write(
                f"D12 CANNOT-EVALUATE: base {base_ref} and head {head_ref} resolve "
                f"to the same commit (repo={_toplevel()} base={base_sha} "
                f"head={base_sha}); the named range is empty, so nothing was "
                f"evaluated. If the change lives in a worktree, run from that "
                f"worktree, or pass a base..head range that selects the change.\n")
            return 2
    else:
        try:
            collapsed = _worktree_matches_base(base_sha)
        except _GitCallFailed as exc:
            # A failed diff or ls-files call leaves the working-tree state
            # undetermined; refuse rather than evaluate on it (3b530 round 4).
            sys.stderr.write(
                f"D12 CANNOT-EVALUATE: {exc} failed while comparing the working "
                f"tree (the default head) against base {base_ref} "
                f"(repo={_toplevel()} base={base_sha}); cannot tell a collapsed "
                f"range from a real change, so nothing was evaluated. Fix the "
                f"repository state and re-run.\n")
            return 2
        if collapsed:
            # Argless form: the head is the working tree; a tree whose content
            # is exactly the base's (no tracked change, no untracked
            # non-ignored file) is the same collapsed range.
            head_sha = _rev_parse("HEAD") if _ref_resolves("HEAD") else "(unborn HEAD)"
            sys.stderr.write(
                f"D12 CANNOT-EVALUATE: the working tree (the default head) shows no "
                f"tracked change against base {base_ref} and holds no untracked, "
                f"non-ignored file (repo={_toplevel()} base={base_sha} "
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
