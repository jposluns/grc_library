#!/usr/bin/env python3
"""Corpus-heuristic version-bump-recency audit.

For each versioned document in the corpus (markdown file with a
``**Version:**`` or ``**Library Version:**`` field in its metadata
block), this linter compares two commits:

  - the most recent commit that touched the file at all, and
  - the most recent commit that touched a Version line in the file.

If they differ, the file's body has been modified since its last
Version field bump, indicating a missed bump.

This is the corpus-side counterpart of delta gate D2 (the per-PR
version-bump check in ``tools/check-version-bump-on-pr.py``). D2
catches the failure mode at PR time, comparing the PR head to its
merge-base; this linter catches it from HEAD using git log heuristics,
covering the case where a body change landed without a Version bump
through any path (squash commit, direct push, batch merge).

Scope: ``*.md`` files under the repository root, minus the exempt set.
The linter requires a versioned-metadata field (the shared
``aiqt_corpus.head_version`` helper returns non-None; GR-3 wave 2
retired this file's private window regex for it) to bring a file into
scope; files without a Version field are silently skipped.

BOM refusal (3b89): a markdown file that begins with a UTF-8
byte-order mark (U+FEFF) is a finding, whether or not it carries a
Version field. The refusal's scope is wider than the recency scope
above, and it is also a SUPERSET of the markdown scope the push-time
version checks (delta gates D2 and D4) read. It applies only the
directory exclusions those gates share (their ``EXEMPT_PREFIXES``: the
root-level ``.corpus-management``, ``.git``, ``node_modules`` and
``__pycache__`` trees). It does NOT apply their per-file
``EXEMPT_FILES`` (CHANGELOG.md, docs/portal.md,
docs/maturity-scorecard.md, the append-only ``.working/`` logs and, in
D2, docs/reference-acquisition-manifest.md): this audit BOM-checks
those files deliberately, though D2 and D4 never read them (3b89
round 3). The recency-only DEFAULT_EXEMPT_DIRS trees, such as
``.claude/`` and ``references/``, ARE BOM-checked (3b89 round 2: the
walk previously applied DEFAULT_EXEMPT_DIRS before the BOM check,
leaving trees D2 and D4 read unprotected).

One rule per mode, stated once (3b89 round 5 replaced the per-case
parity prose that grew in rounds 2-4). The walk classifies every
``*.md`` file it reaches under ``--root``, each by its own path and by
its resolved target: a symlink is refused when either spelling lies in
the BOM scope and the content it leads to begins with a BOM, and it is
reported under its own name; a symlink loop, or a symlink chain past
the kernel's link limit (stat sets ELOOP for both), is a finding; a
path whose stat says it no longer exists (a dangling link, a file
deleted mid-run) is skipped, as are a path that exists but is not a
regular file (a directory named ``*.md``) and a regular file that is
not valid UTF-8 (``read_text_safe`` decodes it to None; no reader
this audit answers for can take a line-1 Version from it); and EVERY
other stat or filesystem read failure (an unlistable directory, a
child of a listable-but-unsearchable directory, an unreadable regular
file, a link whose target sits in a locked tree) stops the run with
exit 2. That fail-closed stat precedes the scope exclusions, so it
fires even under an exempt tree (3b89 rounds 5-6; round 5 closed only
the unlistable-directory case, and ``is_file()`` swallowed the rest
as skips). Explicit mode applies the same classification, with the
same exit-2 stat and read failures, to each argument after
``guard_explicit_paths_cwd`` refuses, with exit 2, any
argument it cannot resolve to an existing path inside ``--root``; an
argument that is itself a link outside ``--root`` is classified by its
resolved target, the one spelling inside the tree. Verdicts can differ
between the modes only where those rules differ; the regression tests
pin the differing cases.

The walk reads the working tree's filesystem, not the git index, so it
also reaches untracked and git-ignored markdown files. That includes
files under the recency-exempt trees (a local ``.claude/`` or
``.working/`` file, an in-repo ``.ref``/``.scratch``/``.private``
checkout) that D2 and D4, which read only the files a PR's git diff
changed, never see; a BOM-prefixed file there fails a local run. A
fresh CI checkout normally holds tracked files only. (Untracked files
outside those trees were walked before round 2 as well; the recency
check skips them as having no history.)

The BOM hides a line-1 metadata field from the ``head_version``-based
readers: this audit's scope check, and delta gates D2 and D4, which
read the Version through the same vendored, digest-pinned
``aiqt_corpus`` helper; the ``git log -G`` Version regex below cannot
match behind it either. (The commit-time guard is the one reader that
is NOT blind: since 3b86 it strips a single leading BOM before
matching.) So this audit refuses the BOM rather than setting it aside.
It runs in CI on pushes to main and on pull requests, in the same
workflow as D2 and D4, so a BOM-prefixed document fails CI here even
where D2 and D4 cannot see its Version.

Exempt from the recency requirement only (the BOM refusal above still
covers these): CHANGELOG.md (the file is itself the version history;
metadata is not bumped per change); generated artefacts (taxonomy.yml,
narrative.yml, docs/portal.md, docs/maturity-scorecard.md,
docs/reference-acquisition-manifest.md), which are regenerated
not edited; and the hidden directories under DEFAULT_EXEMPT_DIRS.

Exit codes: 0 pass, 1 findings, 2 internal error (git failure; an
explicit path the guard refuses or cannot resolve; or any path, in
either mode, whose stat or filesystem read fails with anything other
than "no longer exists" or ELOOP (a symlink loop or over-long chain is a
finding, exit 1, except that explicit mode refuses an argument that is
itself a loop with exit 2): an unlistable directory, a child of a
listable-but-unsearchable directory, an unreadable regular file, a
link into a locked tree. A file that reads but does not decode as
UTF-8 is a skip, not a failure).
"""

from __future__ import annotations

import argparse
import errno
import os
import stat
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from aiqt_corpus import head_version, read_text_safe  # noqa: E402  # generic core (behaviour-identical to lint_common)
from lint_common import guard_explicit_paths_cwd, is_default_exempt_root, DEFAULT_EXEMPT_DIRS, REPO_ROOT  # noqa: E402  # grc-config/store, stays local

# Thread-pool width for the per-file git queries. The queries are
# independent read-only subprocesses, so the pool changes wall-clock
# time only, never the per-file results the audit compares.
GIT_POOL_WORKERS = min(16, (os.cpu_count() or 4) * 2)


# Files exempt from the recency requirement.
EXEMPT_FILES: frozenset[str] = frozenset(
    {
        "CHANGELOG.md",
        "taxonomy.yml",
        "narrative.yml",
        "docs/portal.md",
        "docs/maturity-scorecard.md",
        "docs/reference-acquisition-manifest.md",
    }
)

# The only exclusions the BOM refusal applies: the directory exclusions it shares
# with delta gates D2 and D4, their EXEMPT_PREFIXES (tools/check-version-bump-on-pr.py
# and tools/check-date-cobump-on-pr.py). Matched against the FIRST repo-relative path
# component only, root-anchored exactly as the gates' ``path.startswith(prefix)``. The
# gates' per-file EXEMPT_FILES are deliberately NOT applied, so the BOM scope here
# covers the markdown scope those push-time checks read and is a superset of it, not
# equal to it (3b89 round 3; the recency-only skips are applied after the BOM check).
BOM_SCOPE_EXEMPT_DIRS: frozenset[str] = frozenset(
    {".corpus-management", ".git", "node_modules", "__pycache__"}
)

# Regex (passed to ``git log -G``) that matches a Version metadata line
# at the start of a line. The double-escape (``\\*``) is correct: git
# log's regex backend reads a single backslash. The ``^`` anchor cannot
# see a line-1 field behind a UTF-8 BOM; a BOM-prefixed file is refused
# before any git query (3b89), so no file this regex is run on has one.
GIT_VERSION_REGEX = r"^\*\*(Library )?Version:\*\*"

# The UTF-8 byte-order mark, as decoded text. It can stand only before a
# file's first line, where it hides a line-1 metadata field from the
# line-anchored Version readers this audit answers for (3b89; the module
# docstring names the exact readers and the 3b86 commit-time exception).
BOM = "\ufeff"


# The repository the git queries read. main() sets it to the resolved --root, so the
# queries no longer inherit the process cwd (3b48: run from outside --root, `git log`
# failed with "not a git repository" and every file was skipped as if it had no history).
GIT_ROOT: Path | None = None


def git(*args: str) -> str:
    anchor = ["-C", str(GIT_ROOT)] if GIT_ROOT is not None else []
    return subprocess.check_output(["git", *anchor, *args], text=True).strip()


def require_git_worktree(root: Path) -> str | None:
    """Return a refusal message when ``root`` is not inside a git work tree, else None."""
    try:
        inside = git("rev-parse", "--is-inside-work-tree")
    except (subprocess.CalledProcessError, OSError) as exc:
        return f"--root {root} is not inside a git work tree ({exc}); nothing can be checked."
    # Inside a .git directory the command exits 0 but prints "false" (3b48 r2 codex).
    if inside != "true":
        return f"--root {root} is not inside a git work tree (git reports {inside!r}); nothing can be checked."
    return None


def starts_with_bom(text: str | None) -> bool:
    """True when ``text`` (a decoded file, or ``None`` for an undecodable one) begins with a
    UTF-8 byte-order mark (3b89). A U+FEFF later in the text is ordinary content, not a BOM."""
    return text is not None and text.startswith(BOM)


def as_named(path: Path) -> Path:
    """``path`` made absolute, with its parent directories resolved but its final component
    kept as named: the spelling the walk yields, so a symlink keeps its own name rather than
    its target's (3b89 round 3)."""
    path = path.absolute()
    return path.parent.resolve() / path.name


def in_bom_scope(path: Path, root: Path) -> bool:
    """True when the absolute ``path`` lies under ``root`` and outside the root-anchored
    ``BOM_SCOPE_EXEMPT_DIRS`` (3b89)."""
    try:
        rel_parts = path.relative_to(root).parts
    except ValueError:
        return False
    return not (len(rel_parts) > 1 and rel_parts[0] in BOM_SCOPE_EXEMPT_DIRS)


def resolve_or_loop(path: Path) -> Path | None:
    """``path.resolve()``, or ``None`` when ``path`` is a symlink loop or a
    symlink chain past the kernel's link limit (3b89 rounds 5-6).

    ``Path.resolve`` is version-split on a loop: non-strict resolve raises
    (``RuntimeError``, through Python 3.12; CI runs 3.11) or returns the
    looping spelling unresolved (3.13+), where ``is_file()`` is False
    exactly as for a dangling link. Only the ``stat`` errno (ELOOP) tells
    a loop from a dangling link on every version, so both probes funnel
    into one ``None`` here and the caller fails closed: the walk used to
    crash on CI and silently skip the loop on 3.13+. ``stat`` also sets
    ELOOP for a finite chain of more links than the kernel follows, which
    ``resolve`` walks link by link without complaint, so ``None`` covers
    that chain too and the FAIL text names both cases (round 6). ``None``
    means exactly those ELOOP shapes plus the ``RuntimeError`` loop
    signal: a ``resolve`` failure that is neither propagates from here,
    and a stat failure other than ELOOP surfaces at the caller's own
    fail-closed stat, so each reaches the exit-2 handlers (or, for a path
    that no longer exists, the caller's skip) instead of being
    mislabelled a loop (round 6; round 5 caught every ``OSError`` here
    as a loop)."""
    try:
        resolved = path.resolve()
    except RuntimeError:
        return None
    except OSError as exc:
        if exc.errno == errno.ELOOP:
            return None
        raise
    try:
        path.stat()
    except OSError as exc:
        if exc.errno == errno.ELOOP:
            return None
    return resolved


def classify_markdown(path: Path, root: Path) -> str:
    """Classify one markdown ``path`` against ``root``: ``"bom"`` (begins
    with a UTF-8 BOM, refused), ``"loop"`` (a symlink loop or a symlink
    chain past the kernel's link limit: stat sets ELOOP for both, neither
    can be read, and non-strict ``resolve()`` raises on a loop through
    Python 3.12, so each is a finding, never a crash or a silent skip;
    3b89 rounds 5-6), ``"target"`` (versioned recency target) or
    ``"skip"`` (no longer exists, not a regular file, not valid UTF-8,
    outside the BOM scope, or recency-exempt). Every OTHER stat or
    filesystem read failure raises
    ``OSError`` out of this function and both modes convert it to exit 2:
    a child of a listable-but-unsearchable directory, an unreadable
    regular file and a link into a locked tree used to slip through
    ``is_file()``, which swallows the EACCES, as skips (3b89 round 6).
    ``path`` is the spelling the caller reports; the walk and
    explicit-path mode both classify through this one function, the
    module docstring states the one rule each mode applies around it, and
    verdicts can differ between the modes only where those rules differ.

    Order matters. The loop probe runs first, before anything else that
    stats the path. The fail-closed stat runs second, BEFORE the scope
    checks, so an unreachable file stops the run even under an exempt
    tree. The BOM check runs next, across every markdown file outside the
    root-anchored ``BOM_SCOPE_EXEMPT_DIRS``, the directory exclusions
    shared with delta gates D2 and D4; it skips none of their per-file
    exemptions, so its scope is a superset of theirs. A symlink is in
    that scope when EITHER its own path or its resolved target is (3b89
    round 3: the stricter of the two readings the modes used to take).
    The recency-only skips, the ``.corpus-management`` root then
    DEFAULT_EXEMPT_DIRS then EXEMPT_FILES then the Version filter, come
    after it. A BOM hides a line-1 Version from ``head_version``, so a
    BOM-prefixed file would otherwise leave scope silently, and a recency
    exemption does not make a BOM visible to the other Version readers."""
    try:
        rel_parts = path.relative_to(root).parts
    except ValueError:
        return "skip"
    resolved = resolve_or_loop(path)
    if resolved is None:
        return "loop"
    # The fail-closed stat (3b89 round 6): ``is_file()`` swallowed every stat
    # error, so a child of a listable-but-unsearchable (read-without-execute)
    # directory and a link into a locked tree classified as skips and the run
    # reported OK over them. Only "no longer exists" stays a skip (a dangling
    # link, a file deleted mid-run), and a directory named ``*.md`` is not a
    # markdown document (the shape the pre-3b89-round-2 explicit mode set
    # aside with the same guard); every other stat error raises and the mode
    # handlers exit 2.
    try:
        file_mode = path.stat().st_mode
    except OSError as exc:
        if exc.errno == errno.ENOENT:
            return "skip"
        raise
    if not stat.S_ISREG(file_mode):
        return "skip"
    if not (in_bom_scope(path, root) or in_bom_scope(resolved, root)):
        return "skip"
    text = read_text_safe(path)
    if starts_with_bom(text):
        return "bom"
    # Recency-only from here. is_default_exempt_root resolves the path, as the
    # walk's first check did before round 3, so the recency target set is
    # unchanged in walk mode. A symlink is recency-queried as named (3b89
    # round 3: the pre-fix explicit mode resolved a link first and queried
    # the TARGET's history under the target's name).
    if is_default_exempt_root(path, repo_root=root):
        return "skip"
    if set(rel_parts) & DEFAULT_EXEMPT_DIRS:
        return "skip"
    if "/".join(rel_parts) in EXEMPT_FILES:
        return "skip"
    if head_version(text) is None:
        return "skip"
    return "target"


def iter_targets(root: Path) -> tuple[list[Path], list[Path], list[Path]]:
    """Walk the repository root. Return ``(targets, bom_prefixed, loops)``:
    the markdown files with a metadata-block Version field minus the exempt
    set, the markdown files that begin with a UTF-8 BOM (3b89), and the
    markdown-named symlink loops and over-long chains (3b89 rounds 5-6,
    stat errno ELOOP for both). The per-file rules,
    including the BOM-before-exemptions ordering, live in
    ``classify_markdown``. The walk reads the filesystem, not the git
    index, so untracked and git-ignored files are classified too (the
    module docstring states the consequence). It uses ``os.walk`` with a
    raising ``onerror``, not ``Path.rglob``: rglob silently suppresses the
    traversal error on an existing-but-unlistable directory, so a BOM file
    inside one passed unseen (3b89 round 5; the fail-closed pattern of the
    guardrails repo's ``tools/_walk.py``). ``classify_markdown``'s own
    fail-closed stat and read errors (3b89 round 6) raise out of the walk
    the same way; the caller converts any raised ``OSError`` to exit 2."""
    def _raise(exc: OSError) -> None:
        raise exc

    targets: list[Path] = []
    bom_prefixed: list[Path] = []
    loops: list[Path] = []
    for dirpath, _dirnames, filenames in os.walk(root, onerror=_raise):
        for name in filenames:
            if not name.endswith(".md"):
                continue
            path = Path(dirpath) / name
            verdict = classify_markdown(path, root)
            if verdict == "bom":
                bom_prefixed.append(path)
            elif verdict == "loop":
                loops.append(path)
            elif verdict == "target":
                targets.append(path)
    return sorted(targets), sorted(bom_prefixed), sorted(loops)


class GitQueryError(RuntimeError):
    """A per-file git query failed (3b48 r3 codex). A failure is not "no history": an
    untracked file yields empty output with exit 0, so a non-zero exit means git could not
    answer, and treating it as absent history let the audit pass without checking."""


def last_file_commit(rel: str) -> str | None:
    try:
        out = git("log", "-1", "--format=%H", "--", rel)
    except subprocess.CalledProcessError as exc:
        raise GitQueryError(f"git log failed for {rel} ({exc})") from exc
    return out or None


def last_version_commit(rel: str) -> str | None:
    """Return the SHA of the most recent commit that modified a
    Version metadata line in ``rel``. Returns None if no such commit
    exists (e.g. the file was just added and the Version line has not
    been changed since)."""
    try:
        out = git("log", "-1", "--format=%H", "-G", GIT_VERSION_REGEX, "--", rel)
    except subprocess.CalledProcessError as exc:
        raise GitQueryError(f"git log -G failed for {rel} ({exc})") from exc
    return out or None


def report_unreadable_path(exc: OSError) -> None:
    """The one fail-closed message both modes print before exiting 2 when a
    stat or read fails with anything other than "no longer exists" (3b89
    round 6). Round 5's walk-only message said "directory", but the same
    handler fires for an unreadable regular file and for a link into a
    locked tree, so it says path; the regression tests pin the wording in
    both modes."""
    print(
        f"ERROR: cannot read a path under --root ({exc}); an unreadable "
        f"directory, file or symlink target would otherwise be skipped "
        f"silently, so the audit stops instead of passing over it (3b89 "
        f"rounds 5-6).",
        file=sys.stderr,
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the corpus for versioned documents whose body has changed "
            "more recently than their Version field."
        ),
    )
    parser.add_argument(
        "--root",
        default=str(REPO_ROOT),
        help="Repository root to scan (default: REPO_ROOT).",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help=(
            "Optional explicit paths to check instead of walking the root. "
            "Used by the regression test."
        ),
    )
    args = parser.parse_args(argv[1:])
    root = Path(args.root).resolve()
    global GIT_ROOT
    GIT_ROOT = root
    # Fail loud when --root is not inside a git work tree, before any per-file query: the
    # whole audit reads that tree's history (per-file query failures raise GitQueryError).
    problem = require_git_worktree(root)
    if problem:
        print(f"ERROR: {problem}", file=sys.stderr)
        return 2

    if args.paths:
        given = list(args.paths)
        # 3b48: explicit paths are refused when missing or outside --root (the check reads
        # that tree's git history; a missing path used to count as a scanned document with
        # no history, and an outside one passed over a git fatal), else normalized.
        try:
            args.paths = guard_explicit_paths_cwd(args.paths, repo_root=root)
        except (OSError, RuntimeError) as exc:
            # The guard's own refusals are SystemExit(2) and pass through this
            # handler. What lands here is an argument the filesystem cannot
            # resolve: a symlink loop raises from non-strict resolve() through
            # Python 3.12 (CI runs 3.11); on 3.13+ the guard already refuses a
            # loop as non-existent. Same fail-closed exit, no traceback (3b89
            # round 5).
            print(
                f"ERROR: {exc}; the explicit path(s) cannot be resolved, so "
                f"nothing was checked.",
                file=sys.stderr,
            )
            return 2
        # 3b89: an explicit BOM-prefixed file is refused before any git query. Round 3:
        # the guard returns each path with its symlinks resolved, so classify the path
        # as named instead (see as_named); a link that itself sits outside --root has
        # no as-named spelling under root and is classified by its resolved target,
        # which the guard has checked lies inside. The module docstring states the one
        # rule each mode applies; the guard's fail-closed exit-2 refusals predate
        # round 3 and stay.
        targets: list[Path] = []
        bom_prefixed: list[Path] = []
        loop_paths: list[Path] = []
        try:
            for p, resolved in zip(given, args.paths):
                path = as_named(Path(p))
                if root not in path.parents:
                    path = Path(resolved)
                if not path.name.endswith(".md"):
                    continue
                verdict = classify_markdown(path, root)
                if verdict == "bom":
                    bom_prefixed.append(path)
                elif verdict == "loop":
                    # Reachable (3b89 round 6, r5 codex): the guard resolves a
                    # symlink chain link by link, so a finite chain past the
                    # kernel's limit resolves to an existing target and passes
                    # it, while stat on the as-named spelling fails with ELOOP
                    # and classification refuses the chain as a finding. A
                    # true loop never gets here (the guard refuses it as
                    # unresolvable); the branch also keeps a race from
                    # downgrading a loop to a skip.
                    loop_paths.append(path)
                elif verdict == "target":
                    targets.append(path)
        except OSError as exc:
            # 3b89 round 6: the stat and read failures that stop the walk stop
            # explicit mode too, through the same message. An unreadable
            # regular file used to escape here as a traceback with exit 1, the
            # findings code.
            report_unreadable_path(exc)
            return 2
    else:
        try:
            targets, bom_prefixed, loop_paths = iter_targets(root)
        except OSError as exc:
            report_unreadable_path(exc)
            return 2

    def _rel(path: Path) -> str:
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            return path.as_posix()

    rels = [_rel(path) for path in targets]
    bom_rels = [_rel(path) for path in bom_prefixed]
    loop_rels = [_rel(path) for path in loop_paths]

    # The two git-log queries per file dominated this audit's runtime
    # (two subprocesses x ~490 versioned files, serial). Issue the SAME
    # per-file queries on a thread pool: per-file history simplification
    # (`git log -1 -- <path>`) has no faithful single-call batch form on
    # a history with merge commits, so the commands themselves stay
    # unchanged and only their scheduling is concurrent.
    # Parallelize ACROSS files while preserving the original per-file
    # sequencing EXACTLY: last_version_commit is issued only when
    # last_file_commit succeeded (the serial short-circuit), so the git
    # subprocesses issued (and thus any git diagnostics) are identical to
    # the serial form, and duplicate explicit paths are each processed
    # (map iterates the list; it does not key by rel, which would collapse
    # duplicates). Only scheduling is concurrent. last_file_commit /
    # last_version_commit raise GitQueryError on a git failure (3b48); map
    # re-raises the first one here and the audit exits 2 rather than passing.
    def _per_file_history(rel: str) -> tuple[str | None, str | None]:
        file_commit = last_file_commit(rel)
        if file_commit is None:
            return (None, None)
        return (file_commit, last_version_commit(rel))

    try:
        with ThreadPoolExecutor(max_workers=GIT_POOL_WORKERS) as pool:
            per_file = list(pool.map(_per_file_history, rels))
    except GitQueryError as exc:
        print(f"ERROR: {exc}; the audit cannot be completed.", file=sys.stderr)
        return 2

    findings: list[tuple[str, str, str]] = []
    scanned = 0
    skipped_single_commit = 0
    for rel, (file_commit, version_commit) in zip(rels, per_file):
        scanned += 1
        if file_commit is None:
            # Path not tracked yet (new file in the working tree); skip.
            continue
        if version_commit is None:
            # File exists in history but no commit touched a Version line.
            # This typically means the file was added once with the Version
            # field present and nothing since. If the file's only commit
            # added the Version field, file_commit == version_commit would
            # hold and we would not be here. Skip to avoid noise.
            skipped_single_commit += 1
            continue
        if file_commit != version_commit:
            findings.append((rel, file_commit[:8], version_commit[:8]))

    if not findings and not bom_rels and not loop_rels:
        print(
            f"OK: {scanned} versioned document(s) scanned; "
            f"all have a Version field bumped at or after their most-recent "
            f"body change. {skipped_single_commit} document(s) had no "
            f"Version-line commit history (likely single-commit add)."
        )
        return 0

    for rel in bom_rels:
        print(
            f"FAIL {rel}: the file begins with a UTF-8 byte-order mark (U+FEFF), "
            f"which hides a line-1 metadata field from this audit and from "
            f"delta gates D2 and D4; save the file as UTF-8 without a BOM."
        )
    for rel in loop_rels:
        print(
            f"FAIL {rel}: the path is a symlink loop or a symlink chain past "
            f"the kernel's link limit (stat fails with ELOOP), so it cannot "
            f"be read or classified; it is refused rather than skipped (fail "
            f"closed)."
        )
    for rel, file_sha, version_sha in findings:
        print(
            f"FAIL {rel}: last body commit {file_sha}, "
            f"last Version-line commit {version_sha}; "
            f"the body has changed since the Version was last bumped."
        )
    if bom_rels:
        print(
            f"\n{len(bom_rels)} markdown file(s) begin with a UTF-8 byte-order "
            f"mark. The line-anchored Version readers (this audit's scope "
            f"check and git log -G query, and delta gates D2 and D4) cannot "
            f"see a Version on line 1 behind it, so each such file is refused "
            f"rather than skipped (3b89). Remove the BOM.",
            file=sys.stderr,
        )
    if loop_rels:
        print(
            f"\n{len(loop_rels)} markdown path(s) are symlink loops or symlink "
            f"chains past the kernel's link limit: stat fails with ELOOP on "
            f"both, neither can be read, and resolving a true loop raises on "
            f"Python 3.12 and earlier, so each is a finding, never a crash or "
            f"a silent skip (3b89 rounds 5-6). Remove, shorten or retarget "
            f"the link.",
            file=sys.stderr,
        )
    if findings:
        print(
            f"\n{len(findings)} versioned document(s) have body changes that "
            f"post-date the file's last Version bump. Each finding is the "
            f"corpus-heuristic counterpart of delta gate D2 (which catches the "
            f"same shape at PR time). Resolve by bumping the document's Version "
            f"field, or document the divergence per the project's exception "
            f"protocol.",
            file=sys.stderr,
        )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
