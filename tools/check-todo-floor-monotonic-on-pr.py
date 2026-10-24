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
    In that argless form every working-tree read -- the tracked diff and the
    untracked listing of the collapsed-range check, and the head floor read --
    anchors to the repository top level, so a run from a subdirectory gives
    the same verdict as a run from the root (3b530 rounds 4 and 5). A run
    from inside a NESTED git repository anchors to that nested repository,
    not the outer one: it is refused when the base ref does not resolve in
    the nested repository (a freshly initialised one carries no refs), and
    otherwise evaluated against the nested repository's own base and head;
    in both cases it is never evaluated against the outer repository, so
    run from the outer repository to check the outer floor (3b540).

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
    about the input is a first-class REFUSE, not a permit (guard-input discipline).
    git not running at all (OSError, e.g. git missing from PATH) raises
    _GitCallFailed for main()'s refusal backstop, never a traceback (3b540
    round 3); a nonzero status IS the answer here, so CalledProcessError
    cannot arise (subprocess.run without check)."""
    try:
        return subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    except OSError as exc:
        raise _GitCallFailed(
            f"git rev-parse --verify --quiet {ref} (did not run: {exc})")


def _rev_parse(ref):
    """The commit SHA ``ref`` resolves to (caller has verified it resolves).
    A ref vanishing between that check and this read (CalledProcessError) or
    git itself vanishing (OSError) raises _GitCallFailed for main()'s refusal
    backstop, never a traceback (3b540 round 3)."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--verify", f"{ref}^{{commit}}"], text=True,
            stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, OSError) as exc:
        raise _GitCallFailed(f"git rev-parse --verify {ref} ({exc})")


def _toplevel():
    """The repository top level git selects from the current directory, so a
    collapsed-range refusal can name the clone it resolved (wrong-clone diagnosis).
    A message helper: git failing to run at all (OSError) or printing a top
    level the locale codec cannot decode (UnicodeDecodeError; 3b540) degrades
    to the same placeholder as a missing work tree instead of escaping the
    refusal being composed as a traceback, and only git's terminating newline
    is removed, so a top-level path whose final component ends in whitespace
    is named intact (3b530 round 5)."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True,
            stderr=subprocess.DEVNULL).removesuffix("\n")
    except (subprocess.CalledProcessError, OSError, UnicodeDecodeError):
        return "(no work tree)"


def _path_at_ref(ref, path):
    """True iff ``path`` exists in ``ref``'s tree (ref valid AND path present).
    git not running at all (OSError) raises _GitCallFailed for main()'s
    refusal backstop, never a traceback (3b540 round 3); a nonzero status IS
    the answer here, so CalledProcessError cannot arise (subprocess.run
    without check)."""
    try:
        return subprocess.run(
            ["git", "cat-file", "-e", f"{ref}:{path}"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    except OSError as exc:
        raise _GitCallFailed(f"git cat-file -e {ref}:{path} (did not run: {exc})")


class _GitCallFailed(Exception):
    """A git call the argless collapsed-range check depends on failed: a
    nonzero status other than the documented difference status, or the call
    did not run. The caller refuses as CANNOT-EVALUATE instead of guessing
    collapsed or not-collapsed either way (3b530 round 4). ``str()`` names
    the failed call."""


def _toplevel_strict():
    """The repository top level for the argless form's working-tree reads.
    Unlike ``_toplevel`` (a message helper that degrades to a placeholder),
    a top level that cannot be resolved leaves the head state undetermined,
    so any failure -- nonzero exit, git not running at all, or a top level
    the locale codec cannot decode (3b540) -- raises _GitCallFailed for the
    caller to refuse on. Only git's terminating newline is removed, so a
    top-level path whose final component ends in whitespace is not altered
    (3b530 round 5)."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True,
            stderr=subprocess.DEVNULL).removesuffix("\n")
    except (subprocess.CalledProcessError, OSError, UnicodeDecodeError) as exc:
        raise _GitCallFailed(f"git rev-parse --show-toplevel ({exc})")


def _worktree_matches_base(base_sha, top):
    """True iff the working tree holds exactly the base's content: no tracked
    difference from ``base_sha`` AND no untracked, non-ignored file. An
    untracked file -- including an untracked brand-new floor file, which the
    argless head read below would evaluate -- is working-tree content, not an
    empty range (3b530 round 3). The untracked check is exact (a file whose
    NAME is whitespace still counts) and byte-level (a name that is not valid
    UTF-8, surfaced raw under core.quotePath=false, cannot crash it; 3b530
    round 5). Exactly two reads happen here and both anchor to ``top``, the
    caller-resolved repository top level: the tracked diff and the untracked
    listing each run as ``git -C top`` (3b530 round 4); the argless head
    floor read in main() anchors to the same ``top`` (3b530 round 5), so a
    run from a subdirectory gives the verdict a run from the root gives.
    A call that fails raises _GitCallFailed for the caller to refuse on."""
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
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    except OSError as exc:
        raise _GitCallFailed(f"git ls-files --others (did not run: {exc})")
    if listing.returncode != 0:
        raise _GitCallFailed(f"git ls-files --others (exit {listing.returncode})")
    return listing.stdout == b""


def _git_show(ref, path):
    """``ref:path``'s text. A blob the locale codec cannot decode leaves that
    revision's floor undetermined, so a UnicodeDecodeError raises
    _GitCallFailed for the caller to refuse on instead of escaping as a
    traceback (3b540); a show that fails (CalledProcessError, e.g. the blob
    vanishing between the caller's _path_at_ref check and this read) or git
    not running at all (OSError) raises the same _GitCallFailed, so the
    floor-removed FAIL belongs to the callers' explicit _path_at_ref / open
    checks, never to a failed read (3b540 round 3)."""
    try:
        return subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True,
                                       stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, OSError, UnicodeDecodeError) as exc:
        raise _GitCallFailed(f"git show {ref}:{path} ({exc})")


class _FloorParseError(Exception):
    """``text`` handed to ``_parse`` is not a floor document: not valid JSON,
    or valid JSON of the wrong shape. ``str()`` names the source (ref:path or
    path) and the defect; the caller refuses as CANNOT-EVALUATE instead of
    letting the defect escape as a traceback (3b540 round 2)."""


def _parse(text, source=FLOOR_PATH):
    """The floor mapping (series -> highest ordinal ever allocated) in
    ``text``. The shape validation lives HERE and only here, so no call site
    can parse a floor without it (3b540 round 2): the content must be valid
    JSON, the top level a JSON object, every non-comment key an integer
    string or the TF series, and every value a NON-NEGATIVE JSON integer
    (true/false are booleans, not integers; a floor records the highest
    ordinal ever allocated, so a negative value is no floor at all, while
    zero is the producer's no-allocation default --
    build-todo-number-allocation.py reads ``floor.get(s, 0)`` and
    ``tf = 0`` -- and stays allowed) (3b540 round 3). Underscore-prefixed
    keys are comments, skipped before validation. Any defect raises
    _FloorParseError naming ``source`` for the caller to refuse on."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise _FloorParseError(
            f"{source} is not valid JSON ({exc.__class__.__name__}: {exc})")
    if not isinstance(data, dict):
        raise _FloorParseError(
            f"{source} is not a JSON object (the top level is "
            f"{type(data).__name__}, expected series -> floor)")
    floor = {}
    for k, v in data.items():
        if k.startswith("_"):
            continue
        if k != "TF" and not (k.isascii() and k.isdigit()):
            raise _FloorParseError(
                f"{source} has a series key that is not an integer string "
                f"or TF: {k!r}")
        if isinstance(v, bool) or not isinstance(v, int):
            raise _FloorParseError(
                f"{source} has a floor value that is not an integer "
                f"(series {k!r}: {v!r})")
        if v < 0:
            raise _FloorParseError(
                f"{source} has a negative floor value (series {k!r}: {v!r}); "
                f"a floor records the highest ordinal ever allocated and is "
                f"never below 0")
        floor[k] = v
    return floor


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
    """_run() behind the one refusal backstop for _GitCallFailed: every git
    helper maps a call that fails outright (CalledProcessError where a status
    is not the documented answer, or OSError, e.g. FileNotFoundError when git
    is missing) to _GitCallFailed naming the call, so the mapping lives once
    in the helpers; call sites that can say WHAT was being evaluated catch it
    with a tailored D12 CANNOT-EVALUATE, and every other site falls through
    to this backstop -- the same refusal, never a traceback (3b540 round 3)."""
    try:
        return _run(argv)
    except _GitCallFailed as exc:
        sys.stderr.write(
            f"D12 CANNOT-EVALUATE: {exc} failed (repo={_toplevel()}); the "
            f"repository state is undetermined, so nothing was evaluated. "
            f"Fix the git installation or repository state and re-run.\n")
        return 2


def _run(argv):
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
            top = _toplevel_strict()
            collapsed = _worktree_matches_base(base_sha, top)
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
    try:
        base_text = _git_show(base_ref, FLOOR_PATH)
    except _GitCallFailed as exc:
        # The base floor exists (checked above) but could not be read back as
        # text; refuse rather than evaluate on an undetermined base (3b540).
        sys.stderr.write(
            f"D12 CANNOT-EVALUATE: {exc} failed while reading the base floor "
            f"{base_ref}:{FLOOR_PATH} (repo={_toplevel()} base={base_sha}); "
            f"nothing was evaluated. Fix the repository state and re-run.\n")
        return 2
    if head_ref and not _path_at_ref(head_ref, FLOOR_PATH):
        # The explicit-head twin of the base _path_at_ref check above: the
        # floor-removed FAIL is decided by this path check, so a _git_show
        # that then fails (the blob vanishing, or git itself) is a refusal
        # via the helpers' _GitCallFailed, never read as a removed floor and
        # never a traceback (3b540 round 3).
        sys.stderr.write(f"FAIL: {FLOOR_PATH} is missing at HEAD but present at {base_ref} "
                         "(the floor must never be removed).\n")
        return 1
    head_desc = f"{head_ref}:{FLOOR_PATH}" if head_ref else os.path.join(top, FLOOR_PATH)
    try:
        # The argless head read anchors to the same resolved top level as the
        # collapsed-range check above, so a run from a subdirectory reads the
        # real floor instead of reporting it missing (3b530 round 5). What a
        # read returns is then parsed through the guarded _parse calls below
        # -- one refusal clause per floor, each naming its source -- so no
        # content defect (not JSON, or JSON of the wrong shape) can escape
        # as a traceback from any of the three forms (3b540 round 2).
        if head_ref:
            head_text = _git_show(head_ref, FLOOR_PATH)
        else:
            head_text = open(head_desc, encoding="utf-8").read()
    except FileNotFoundError:
        sys.stderr.write(f"FAIL: {FLOOR_PATH} is missing at HEAD but present at {base_ref} "
                         "(the floor must never be removed).\n")
        return 1
    except (_GitCallFailed, OSError, UnicodeDecodeError) as exc:
        # A head floor that exists but cannot be read -- a directory in its
        # place, a permission error, bytes that are not valid UTF-8, or an
        # undecodable git show -- leaves the head state undetermined: neither
        # the floor-removed FAIL above nor any verdict applies, so refuse
        # instead of escaping as a traceback (3b540).
        sys.stderr.write(
            f"D12 CANNOT-EVALUATE: cannot read the head floor {head_desc} "
            f"({exc.__class__.__name__}: {exc}) while comparing against base "
            f"{base_ref} (repo={_toplevel()} base={base_sha}); the head state "
            f"is undetermined, so nothing was evaluated. Fix the floor file "
            f"and re-run.\n")
        return 2
    try:
        base = _parse(base_text, f"{base_ref}:{FLOOR_PATH}")
    except _FloorParseError as exc:
        # The base floor was read back but is not a floor document; the base
        # state is undetermined, so no verdict applies (3b540 round 2).
        sys.stderr.write(
            f"D12 CANNOT-EVALUATE: the base floor {exc} "
            f"(repo={_toplevel()} base={base_sha}); the base state is "
            f"undetermined, so nothing was evaluated. Fix the floor at the "
            f"base and re-run.\n")
        return 2
    try:
        head = _parse(head_text, head_desc)
    except _FloorParseError as exc:
        # Same refusal for the head floor, whichever form supplied it (an
        # explicit head ref or the argless working tree) (3b540 round 2).
        sys.stderr.write(
            f"D12 CANNOT-EVALUATE: the head floor {exc} "
            f"(repo={_toplevel()} base={base_sha}); the head state is "
            f"undetermined, so nothing was evaluated. Fix the floor file "
            f"and re-run.\n")
        return 2
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
