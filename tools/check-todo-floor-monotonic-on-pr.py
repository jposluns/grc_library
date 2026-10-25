#!/usr/bin/env python3
"""Delta gate D12: the public number floor is MONOTONIC across a PR.

``tools/todo-number-floor.json`` records the highest ordinal EVER allocated per public
backlog series (gate 91 generates the ``## Number allocation`` counters from it, and gate 78
reads it for the recycle check). Those checks enforce that a counter is not BELOW the floor,
but nothing stops a hand-edit from LOWERING the floor itself: a lowered floor rewinds a
counter and silently permits recycling a retired id (the floor is its own only witness).

This delta gate closes that direction: it compares the PR's floor against the floor at the
PR's merge base and FAILS if any series' floor DECREASED or a series was dropped. The floor
may only rise (a new allocation) or stay put. Runs PR-time, like the other
``check-*-on-pr.py`` gates.

The merge base of the base and the head is computed once and pinned as a SHA;
its tree is what the range's emptiness is judged against and its floor is what
the head floor is compared with, in the named and the argless form alike, as
the specification states (3b577 round 3). A branch that is behind its base is
therefore judged on its own change: a floor the base raised after the branch
forked is not read as the branch lowering it, and a stale branch that changes
nothing net is refused below rather than compared with the base's newer
content. A criss-cross history has more than one merge base, and every one
is pinned: the head floor is compared with each merge base's floor and FAILS
on a decrease against any of them, and the range is empty only when the head
holds every merge base's content (3b577 round 4). A merge base that cannot be
computed (unrelated histories, a shallow clone missing the fork point, or an
unborn HEAD in the argless form) refuses as CANNOT-EVALUATE (exit 2).

Usage:
  python3 tools/check-todo-floor-monotonic-on-pr.py [BASE_REF] [HEAD_REF]
    BASE_REF defaults to origin/main; HEAD_REF omitted means the working tree,
    whose merge base is the one of BASE_REF and HEAD.
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

A collapsed range (base and head resolving to the same commit, a head that is
already contained in the base so that it is its own merge base, or the working
tree holding the merge base's content in the argless form) is refused as
CANNOT-EVALUATE (exit 2), never reported as a clean reflexive pass: a collapsed
range is exactly how a gate run in the wrong clone presents (orchestrator
mistake 300), the same refusal D5, D9 and D13 give. A net-empty named range --
a head whose tree is its merge base's, so that no file changed on the branch,
such as an empty head commit or a change and its revert, on a current or a
stale branch -- is refused the same way, as the unscoped gates D1, D2, D4, D5
and D11 refuse a named range whose changed set is empty (3b577 rounds 2 and
3). The argless form needs no separate check: it compares the working tree's
content with the merge base, so a HEAD that adds only empty commits, or a
change and its revert, is already the collapsed range above.
"""
import json
import os
import re
import reprlib
import subprocess
import sys

FLOOR_PATH = "tools/todo-number-floor.json"

# A full commit id as git prints one: 40 lowercase hexadecimal digits, or 64
# in a SHA-256 repository (3b577 round 4).
_FULL_COMMIT_ID = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")

# git ls-tree supports no pathspec magic, so an inherited GIT_GLOB_PATHSPECS
# or GIT_ICASE_PATHSPECS makes it exit 128 ("pathspec magic not supported by
# this command") and the presence check would refuse a range it can
# evaluate; _path_at_sha runs it without them (3b540 round 6).
# GIT_LITERAL_PATHSPECS and GIT_NOGLOB_PATHSPECS stay: under them ls-tree
# already reads the path literally and gives the real verdict.
_LS_TREE_DROPPED_ENV = ("GIT_GLOB_PATHSPECS", "GIT_ICASE_PATHSPECS")


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
    backstop, never a traceback (3b540 round 3); so does output the locale
    codec cannot decode (UnicodeDecodeError), as in _toplevel_strict and
    _git_show (3b540 round 4)."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--verify", f"{ref}^{{commit}}"], text=True,
            stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, OSError, UnicodeDecodeError) as exc:
        raise _GitCallFailed(f"git rev-parse --verify {ref} ({exc})")


def _merge_base(base_sha, head_sha):
    """Every merge base of the commits ``base_sha`` and ``head_sha``, as a
    tuple in the order ``git merge-base --all`` lists them: the revisions
    the specification compares the floor against (3b577 round 3). A
    criss-cross history has more than one, and ``git merge-base`` without
    --all prints only one of them, so a floor compared with that one alone
    could be lowered below another unseen; the caller compares the head
    with each (3b577 round 4). Both arguments are SHAs the gate resolved
    once, and the answer is pinned the same way, so every later read of the
    base side uses these SHAs. No common ancestor (unrelated histories, or
    a shallow clone that lacks the fork point) exits nonzero with no
    output; that, git not running at all (OSError), output the locale codec
    cannot decode (UnicodeDecodeError), no name at all, or any name that is
    not a full commit id (40 lowercase hexadecimal digits, or 64 in a
    SHA-256 repository) raises _GitCallFailed for the caller to refuse on,
    never a guess."""
    call = f"git merge-base --all {base_sha} {head_sha}"
    try:
        names = subprocess.check_output(
            ["git", "merge-base", "--all", base_sha, head_sha], text=True,
            stderr=subprocess.DEVNULL).split()
    except (subprocess.CalledProcessError, OSError, UnicodeDecodeError) as exc:
        raise _GitCallFailed(f"{call} ({exc})")
    if not names:
        raise _GitCallFailed(f"{call} (printed no names, expected at least 1)")
    for name in names:
        if not _FULL_COMMIT_ID.fullmatch(name):
            raise _GitCallFailed(
                f"{call} (printed {reprlib.repr(name)}, not a full commit id)")
    return tuple(names)


def _bases_desc(merge_bases, base_ref, head_name):
    """``the merge base <sha> of <base> and <head>`` (``the merge bases
    <sha>, <sha> ...`` in a criss-cross history), so a message names the
    floor revisions it read or compared, not the base ref, which can name
    other content (3b577 round 4)."""
    noun = "the merge base" if len(merge_bases) == 1 else "the merge bases"
    return f"{noun} {', '.join(merge_bases)} of {base_ref} and {head_name}"


def _entry_present(path):
    """True unless ``os.lstat`` reports ``path`` ABSENT (ENOENT). open()
    follows links, so a dangling link raises the same FileNotFoundError a
    missing floor does; lstat does not follow the final link, so it tells a
    present entry that cannot be followed from no entry at all. Any other
    lstat failure leaves presence undetermined and counts as present, so
    the caller refuses rather than reads it as removed or absent (the
    strict-lookup convention of lint_common.strict_kind; 3b577 round 3)."""
    try:
        os.lstat(path)
    except FileNotFoundError:
        return False
    except OSError:
        return True
    return True


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


def _path_at_sha(sha, path):
    """True iff the tree of commit ``sha`` LISTS an entry at ``path``, as
    ``git ls-tree --full-tree sha -- path`` reports it: empty output means
    the path is absent there, a listed entry means it is present. This
    decides presence in the tree only, not that the entry's object can be
    read: a listed blob may be missing from the object store, so a caller
    reads a listed entry with _git_show, whose failure refuses (3b540 round
    5). ``sha`` is a commit SHA the gate resolved once, never a ref name, so
    a ref that moves or vanishes mid-run cannot change the answer (3b540
    round 5). --full-tree reads ``path`` from the repository top level, as
    ``sha:path`` does, whatever the current directory. A nonzero status (the
    commit or a tree on the path unreadable) or git not running at all
    (OSError) raises _GitCallFailed for main()'s refusal backstop, never
    read as absent and never a traceback (3b540 rounds 3 and 5). The call
    runs without _LS_TREE_DROPPED_ENV, so an inherited glob or icase
    pathspec mode cannot turn that status nonzero (3b540 round 6)."""
    env = {k: v for k, v in os.environ.items() if k not in _LS_TREE_DROPPED_ENV}
    try:
        listing = subprocess.run(
            ["git", "ls-tree", "--full-tree", sha, "--", path],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env)
    except OSError as exc:
        raise _GitCallFailed(f"git ls-tree {sha} -- {path} (did not run: {exc})")
    if listing.returncode != 0:
        raise _GitCallFailed(
            f"git ls-tree {sha} -- {path} (exit {listing.returncode})")
    return listing.stdout != b""


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


def _worktree_matches_base(merge_bases, top):
    """True iff the working tree holds exactly the content of every merge
    base: no tracked difference from any of ``merge_bases`` (the pinned
    merge bases of the base and HEAD, not the base itself; 3b577 rounds 3
    and 4) AND no untracked, non-ignored file. An
    untracked file -- including an untracked brand-new floor file, which the
    argless head read below would evaluate -- is working-tree content, not an
    empty range (3b530 round 3). The untracked check is exact (a file whose
    NAME is whitespace still counts) and byte-level (a name that is not valid
    UTF-8, surfaced raw under core.quotePath=false, cannot crash it; 3b530
    round 5). One tracked diff per merge base (until one differs) and one
    untracked listing happen here, and all anchor to ``top``, the
    caller-resolved repository top level: each runs as ``git -C top``
    (3b530 round 4); the argless head
    floor read in main() anchors to the same ``top`` (3b530 round 5), so a
    run from a subdirectory gives the verdict a run from the root gives.
    A call that fails raises _GitCallFailed for the caller to refuse on."""
    for merge_base in merge_bases:
        try:
            diff_rc = subprocess.run(
                ["git", "-C", top, "diff", "--quiet", merge_base, "--"],
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


def _range_is_empty(merge_bases, head_sha):
    """True iff the commit ``head_sha`` records the same root tree as every
    commit in ``merge_bases``, so no file differs between the head and any
    merge base. Distinct commits can still
    select nothing (an empty head commit, or a change and its revert), and
    such a range reads as the clean monotonic-reflexive OK, so the caller
    refuses it as the unscoped delta gates refuse an empty changed set
    (3b577 round 2). The caller passes the pinned merge bases, not the base
    itself, so a stale branch is judged on what it changed since it forked,
    not on what the base gained since (3b577 round 3); a head whose tree is
    one merge base's but not another's in a criss-cross history still
    differs from the other, so it is not empty (3b577 round 4). All
    arguments are SHAs the gate resolved once, never ref names (3b540 round
    5). Only the tree names are compared, so no blob
    is read: a floor blob missing from the object store still reaches the
    floor reads below and their refusals (3b540 round 5), which a
    ``git diff --quiet`` here (exit 128 on that blob) would preempt. A read
    that fails (CalledProcessError), git not running at all (OSError),
    output the locale codec cannot decode (UnicodeDecodeError) or output
    that is not one tree name per commit raises _GitCallFailed for main()'s
    refusal backstop."""
    revs = [f"{sha}^{{tree}}" for sha in (*merge_bases, head_sha)]
    call = f"git rev-parse {' '.join(revs)}"
    try:
        trees = subprocess.check_output(
            ["git", "rev-parse", *revs],
            text=True, stderr=subprocess.DEVNULL).split()
    except (subprocess.CalledProcessError, OSError, UnicodeDecodeError) as exc:
        raise _GitCallFailed(f"{call} ({exc})")
    if len(trees) != len(revs):
        raise _GitCallFailed(
            f"{call} (printed {len(trees)} names, expected {len(revs)})")
    return all(tree == trees[-1] for tree in trees[:-1])


def _git_show(ref, path):
    """``ref:path``'s text. A blob the locale codec cannot decode leaves that
    revision's floor undetermined, so a UnicodeDecodeError raises
    _GitCallFailed for the caller to refuse on instead of escaping as a
    traceback (3b540); a show that fails (CalledProcessError, e.g. a blob
    the caller's _path_at_sha check listed but the object store does not
    hold; 3b540 round 5) or git not running at all (OSError) raises the
    same _GitCallFailed, so the floor-removed FAIL belongs to the callers'
    explicit _path_at_sha / open checks, never to a failed read (3b540
    round 3)."""
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
    _FloorParseError naming ``source`` for the caller to refuse on: that
    includes text the decoder cannot hold, which raises not
    JSONDecodeError but its superclass ValueError (an integer longer than
    the interpreter's digit limit) or RecursionError (nesting deeper than
    the decoder's stack), and a value nested too deep to repr, which the
    messages below bound with reprlib (3b577 round 4)."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise _FloorParseError(
            f"{source} is not valid JSON ({exc.__class__.__name__}: {exc})")
    except (ValueError, RecursionError) as exc:
        raise _FloorParseError(
            f"{source} cannot be decoded as JSON ({exc.__class__.__name__}: {exc})")
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
                f"(series {k!r}: {reprlib.repr(v)})")
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
    is missing) and, where it decodes git's output as text, a
    UnicodeDecodeError (3b540 round 4) to _GitCallFailed naming the call, so
    the mapping lives once in the helpers (only the message helper _toplevel
    degrades to a placeholder instead, so composing a refusal cannot raise);
    call sites that can say WHAT was being evaluated catch it with a tailored
    D12 CANNOT-EVALUATE, and every other site falls through to this backstop
    -- the same refusal, never a traceback (3b540 round 3)."""
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
    # A collapsed or net-empty range would read as the clean monotonic-reflexive
    # OK; refuse it instead (the wrong-clone signature the delta gates refuse,
    # orchestrator mistake 300), BEFORE the first-introduction OK below can fire.
    # Each ref is resolved to its commit SHA once, here, and so is every merge
    # base of the two, and every later git read -- the collapsed-range and
    # net-empty checks, the floor-path checks, the floor reads -- uses those
    # SHAs, never the ref names, so a ref that moves or vanishes mid-run cannot
    # change what is evaluated (3b540 round 5; the merge base 3b577 round 3,
    # every merge base round 4).
    base_sha = _rev_parse(base_ref)
    head_sha = None  # the argless head is the working tree, read by path below
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
        head_sha = _rev_parse(head_ref)
        if head_sha == base_sha:
            sys.stderr.write(
                f"D12 CANNOT-EVALUATE: base {base_ref} and head {head_ref} resolve "
                f"to the same commit (repo={_toplevel()} base={base_sha} "
                f"head={head_sha}); the named range is empty, so nothing was "
                f"evaluated. If the change lives in a worktree, run from that "
                f"worktree, or pass a base..head range that selects the change.\n")
            return 2
        head_commit, head_name = head_sha, head_ref
    else:
        # The argless head is the working tree checked out on HEAD, so its
        # merge base is the base's with HEAD. An unborn HEAD has none, and
        # with no merge base there is nothing to compare the floor against
        # (3b577 round 3).
        if not _ref_resolves("HEAD"):
            sys.stderr.write(
                f"D12 CANNOT-EVALUATE: HEAD does not resolve to a commit (an "
                f"unborn branch), so the working tree (the default head) has no "
                f"merge base with base {base_ref} (repo={_toplevel()} "
                f"base={base_sha}); D12 compares the floor against the merge "
                f"base, so nothing was evaluated. Commit the change first, or "
                f"pass a base..head range that selects it.\n")
            return 2
        head_commit, head_name = _rev_parse("HEAD"), "HEAD"
    try:
        merge_bases = _merge_base(base_sha, head_commit)
    except _GitCallFailed as exc:
        # No merge base, no comparison point: refuse rather than fall back to
        # the base itself, which would compare a stale branch's floor with
        # content the branch never saw (3b577 round 3).
        sys.stderr.write(
            f"D12 CANNOT-EVALUATE: {exc} failed: base {base_ref} and head "
            f"{head_name} have no merge base git can compute (repo={_toplevel()} "
            f"base={base_sha} head={head_commit}); D12 compares the floor "
            f"against the merge base, so nothing was evaluated. Fetch the full "
            f"history (a shallow clone can lack the fork point) and re-run.\n")
        return 2
    # Every merge base is named in the pins, comma-separated when a
    # criss-cross history has more than one (3b577 round 4).
    merge_base_pin = ",".join(merge_bases)
    bases_desc = _bases_desc(merge_bases, base_ref, head_name)
    # "each of their N merge bases" when there are several, so a refusal
    # says the head was judged against all of them (3b577 round 4).
    their_bases = ("their merge base" if len(merge_bases) == 1
                   else f"each of their {len(merge_bases)} merge bases")
    if head_ref is not None:
        if head_sha in merge_bases:
            # The head is already contained in the base: a clone whose HEAD
            # sits at the branch point after the base moved on, the
            # wrong-clone shape again, selects nothing (3b577 round 3).
            sys.stderr.write(
                f"D12 CANNOT-EVALUATE: head {head_ref} is an ancestor of base "
                f"{base_ref}, so it is its own merge base (repo={_toplevel()} "
                f"base={base_sha} head={head_sha} merge-base={merge_base_pin}); the "
                f"named range is empty, so nothing was evaluated. If the change "
                f"lives in a worktree, run from that worktree, or pass a "
                f"base..head range that selects the change.\n")
            return 2
        if _range_is_empty(merge_bases, head_sha):
            # A head whose tree is every merge base's changed no file on the
            # branch (an empty head commit, or a change and its revert, on a
            # current or a stale branch): the same empty range, refused as D1,
            # D2, D4, D5 and D11 refuse an empty changed set (3b577 rounds 2
            # to 4).
            sys.stderr.write(
                f"D12 CANNOT-EVALUATE: base {base_ref} and head {head_ref} are "
                f"distinct commits but no files changed between {their_bases} "
                f"and the head "
                f"(repo={_toplevel()} base={base_sha} head={head_sha} "
                f"merge-base={merge_base_pin}); the named range is empty, so nothing "
                f"was evaluated. If the change lives in a worktree, run from that "
                f"worktree, or pass a base..head range that selects the change.\n")
            return 2
    else:
        try:
            top = _toplevel_strict()
            collapsed = _worktree_matches_base(merge_bases, top)
        except _GitCallFailed as exc:
            # A failed diff or ls-files call leaves the working-tree state
            # undetermined; refuse rather than evaluate on it (3b530 round 4).
            sys.stderr.write(
                f"D12 CANNOT-EVALUATE: {exc} failed while comparing the working "
                f"tree (the default head) against {bases_desc} "
                f"(repo={_toplevel()} base={base_sha} "
                f"merge-base={merge_base_pin}); cannot tell a collapsed range from a "
                f"real change, so nothing was evaluated. Fix the repository "
                f"state and re-run.\n")
            return 2
        if collapsed:
            # Argless form: the head is the working tree; a tree whose content
            # is exactly every merge base's (no tracked change, no untracked
            # non-ignored file) is the same collapsed range.
            sys.stderr.write(
                f"D12 CANNOT-EVALUATE: the working tree (the default head) shows no "
                f"tracked change against {bases_desc} "
                f"and holds no untracked, non-ignored file "
                f"(repo={_toplevel()} base={base_sha} head={head_commit}, working "
                f"tree; merge-base={merge_base_pin}); the range is empty, so nothing "
                f"was evaluated. If the change lives in a worktree, run from that "
                f"worktree, or pass a base..head range that selects the change.\n")
            return 2
    # Every verdict line and both head-floor refusals name the SHAs evaluated,
    # as the refusals above name the base, so a ref that moves after pinning
    # cannot point the reader at other content; the argless head is the
    # working tree, which has no SHA (3b540 round 6). The merge bases, whose
    # floors are the ones compared, are named too (3b577 rounds 3 and 4).
    pins = (f"base={base_sha} head={head_sha if head_ref else 'working tree'} "
            f"merge-base={merge_base_pin}")
    # No merge base whose tree lists the floor is the first introduction,
    # with no prior floor to compare. Its OK still waits until the head floor
    # has been read and parsed below like any other head floor, so an
    # introduced floor that cannot be read or is not a floor document refuses
    # instead of passing unread (3b577). Each listed floor is read at its
    # merge base and labelled with that SHA, the revision actually read,
    # never with the base ref, which names other content once the base has
    # moved on; a merge base that does not list the floor, beside one that
    # does in a criss-cross history, has nothing to compare (3b577 round 4).
    listed = [sha for sha in merge_bases if _path_at_sha(sha, FLOOR_PATH)]
    base_listed = bool(listed)
    base_texts = {}
    for sha in listed:
        try:
            base_texts[sha] = _git_show(sha, FLOOR_PATH)
        except _GitCallFailed as exc:
            # The merge base's tree lists the floor (checked above) but it could
            # not be read back as text -- its blob missing from the object
            # store, or undecodable; refuse rather than evaluate on an
            # undetermined base, and never read it as the first-introduction OK
            # (3b540, round 5).
            sys.stderr.write(
                f"D12 CANNOT-EVALUATE: {exc} failed while reading the merge-base "
                f"floor {sha}:{FLOOR_PATH}, the floor at "
                f"{_bases_desc((sha,), base_ref, head_name)} (repo={_toplevel()} "
                f"{pins}); nothing was evaluated. Fix the repository state and "
                f"re-run.\n")
            return 2
    listed_desc = _bases_desc(listed, base_ref, head_name) if listed else None
    head_desc = f"{head_ref}:{FLOOR_PATH}" if head_ref else os.path.join(top, FLOOR_PATH)
    head_text = None  # stays None only when neither the merge base nor the head has a floor
    if head_ref and not _path_at_sha(head_sha, FLOOR_PATH):
        # The explicit-head twin of the base _path_at_sha check above: the
        # floor-removed FAIL is decided by this path check, so a _git_show
        # that then fails (a listed blob missing from the object store, or
        # git itself) is a refusal via the helpers' _GitCallFailed, never
        # read as a removed floor and never a traceback (3b540 rounds 3
        # and 5).
        if base_listed:
            sys.stderr.write(f"FAIL: {FLOOR_PATH} is missing at HEAD but present at "
                             f"{listed_desc} ({pins}); the floor must never be removed.\n")
            return 1
    else:
        read_error = None
        try:
            # The argless head read anchors to the same resolved top level as the
            # collapsed-range check above, so a run from a subdirectory reads the
            # real floor instead of reporting it missing (3b530 round 5). What a
            # read returns is then parsed through the guarded _parse calls below
            # -- one refusal clause per floor, each naming its source -- so no
            # content defect (not JSON, or JSON of the wrong shape) can escape
            # as a traceback from any of the three forms (3b540 round 2).
            if head_ref:
                head_text = _git_show(head_sha, FLOOR_PATH)
            else:
                head_text = open(head_desc, encoding="utf-8").read()
        except FileNotFoundError as exc:
            # Only the argless open() raises this, and it follows links, so a
            # dangling link in the floor's place raises it too. lstat tells
            # the two apart: a path present but unreadable refuses below, with
            # or without a floor at the merge base, never the floor-removed
            # FAIL and never the first-introduction OK (3b577 round 3).
            if _entry_present(head_desc):
                read_error = (f"{exc.__class__.__name__}: {exc}; the path is present "
                              f"but cannot be followed, a dangling link say")
            elif base_listed:
                sys.stderr.write(f"FAIL: {FLOOR_PATH} is missing at HEAD but present at "
                                 f"{listed_desc} ({pins}); the floor must never "
                                 f"be removed.\n")
                return 1
        except (_GitCallFailed, OSError, UnicodeDecodeError) as exc:
            # A head floor that exists but cannot be read -- a directory in its
            # place, a permission error, bytes that are not valid UTF-8, or an
            # undecodable git show -- leaves the head state undetermined: neither
            # the floor-removed FAIL above nor any verdict applies, so refuse
            # instead of escaping as a traceback (3b540).
            read_error = f"{exc.__class__.__name__}: {exc}"
        if read_error is not None:
            sys.stderr.write(
                f"D12 CANNOT-EVALUATE: cannot read the head floor {head_desc} "
                f"({read_error}) while comparing against the floor at "
                f"{bases_desc} (repo={_toplevel()} {pins}); the head state "
                f"is undetermined, so nothing was evaluated. Fix the floor file "
                f"and re-run.\n")
            return 2
    bases = {}
    for sha in listed:
        try:
            bases[sha] = _parse(base_texts[sha], f"{sha}:{FLOOR_PATH}")
        except _FloorParseError as exc:
            # The merge-base floor was read back but is not a floor document;
            # the floor the head is compared with is undetermined, so no
            # verdict applies (3b540 round 2). The base may have fixed its
            # floor since the branch forked, so the remedy covers both cases
            # (3b577 round 4).
            sys.stderr.write(
                f"D12 CANNOT-EVALUATE: the merge-base floor {exc}; it is the floor "
                f"at {_bases_desc((sha,), base_ref, head_name)} "
                f"(repo={_toplevel()} {pins}); the floor the head is compared "
                f"with is undetermined, so nothing was evaluated. If {base_ref} "
                f"has fixed its floor since the branch forked, bring the branch "
                f"up to date with {base_ref} (merge or rebase) and re-run; "
                f"otherwise fix the floor on {base_ref} first.\n")
            return 2
    if head_text is not None:
        try:
            head = _parse(head_text, head_desc)
        except _FloorParseError as exc:
            # Same refusal for the head floor, whichever form supplied it (an
            # explicit head ref or the argless working tree) (3b540 round 2).
            sys.stderr.write(
                f"D12 CANNOT-EVALUATE: the head floor {exc} "
                f"(repo={_toplevel()} {pins}); the head state is "
                f"undetermined, so nothing was evaluated. Fix the floor file "
                f"and re-run.\n")
            return 2
    # Each verdict line names what it compared: the head floor and the floor
    # at each merge base it was compared with, by SHA, not the base ref
    # (3b577 round 4).
    if not base_listed:
        if head_text is None:
            # Neither the merge base nor the head has a floor: nothing was
            # introduced and nothing compared, which the first-introduction OK
            # below would misstate (3b577 round 3).
            print(f"OK: no floor on either side: {FLOOR_PATH} is absent at "
                  f"{bases_desc} and at the head ({pins}); nothing to compare.")
            return 0
        # Every merge base is VALID but the floor did not exist at any of
        # them: first introduction, nothing to compare.
        print(f"OK: {FLOOR_PATH} is new since the merge base: absent at "
              f"{bases_desc}, and the head floor {head_desc} is a valid floor "
              f"document ({pins}); no prior floor to compare.")
        return 0
    # A decrease against ANY merge base's floor fails: in a criss-cross
    # history git's single pick can be the merge base with the lower floor
    # (3b577 round 4).
    violations = []
    for sha in listed:
        found = find_violations(bases[sha], head)
        violations += found if len(listed) == 1 else [f"vs {sha}: {v}" for v in found]
    if violations:
        sys.stderr.write(f"FAIL: the head floor {head_desc} is not monotonic vs the floor "
                         f"at {listed_desc} ({pins}): {'; '.join(violations)}. The floor may "
                         f"only rise or stay put; restore each decreased value in "
                         f"{FLOOR_PATH}.\n")
        return 1
    series = set().union(*bases.values())
    print(f"OK: the head floor {head_desc} is monotonic vs the floor at {listed_desc} "
          f"({pins}; {len(series)} series, none decreased or dropped).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
