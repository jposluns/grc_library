#!/usr/bin/env python3
"""Enforce that library and document versions never decrease.

The library uses Calendar Versioning (CalVer) of the form `YYYY.MM.patch`
for the library as a whole, recorded in `README.md` as
`**Library Version:** YYYY.MM.patch`. Individual documents use semantic
versioning of the form `x.y.z` in their metadata.

This linter compares the working tree's versions to the prior committed
state (`refs/remotes/origin/main` if available, falling back to `HEAD~1`)
and fails if any version went backwards or skipped to a lower value.

Catches:
- A version going BACKWARDS (a rollback or collision). An unchanged value
  passes, so a forgotten bump is the CHANGELOG-coupling and per-PR delta
  checks' and the reviewer's territory, not this gate's.
- Accidentally rewriting an older value in a metadata field.
- Per-document semver going backwards on a change that should have
  bumped forward.

Usage:
    python3 tools/lint-library-version-monotonicity.py
    python3 tools/lint-library-version-monotonicity.py --prior-readme PATH

The ``--prior-readme`` flag overrides the git-based "prior state"
lookup for the library-version check only: the linter parses CalVer
from the given file and compares to the current README.md. Used by
the gate-36 regression test suite to exercise the version-comparison
logic without a git fixture. The document-versions check is skipped
in this mode (it requires real git history).

Exit codes:
    0   versions are monotonic non-decreasing, OR there is no prior state:
        no repository (git rev-parse --git-dir fails, REPO_ROOT has no .git
        and GIT_DIR is unset), an unborn HEAD, or a HEAD commit with no parent
        (a root commit or the boundary of a shallow clone) while origin/main
        is absent or is HEAD. No prior state is treated as a pass with a
        printed note rather than a separate exit code.
    1   one or more versions decreased.
    2   an explicit --prior-readme is missing, empty, not a regular file, or
        cannot be read (a symlink, which is not followed; nothing to compare
        against); or git cannot read the
        prior state (a bad ref, an unreadable tree, or a missing or corrupt
        object), which is not the same as a file absent at the prior ref; or
        REPO_ROOT has a .git entry, or GIT_DIR is set, and git does not open
        a repository whose work tree is REPO_ROOT: git cannot open it (a HEAD
        or config git cannot parse, an unknown repository extension, dubious
        ownership, a .git file naming no repository, GIT_DIR naming a missing
        or broken one), or skips a .git it cannot use (a garbage HEAD, no
        refs/, an empty directory, a dangling symlink) for an enclosing
        repository, or the repository it opens has no work tree or another
        one, or GIT_DIR names a repository other than the one REPO_ROOT's
        .git opens; that is not the same as no repository. Or HEAD or
        origin/main, read by its exact name, exists but does not resolve to
        a commit git can read (git cannot parse the ref, or the object it
        names is missing, malformed or not a commit), or git skips a record
        of it and reports it as absent (a malformed or unsorted packed-refs
        line, a dangling loose symlink, a loose file shadowing a packed ref),
        which is not the same as an unborn HEAD, a root commit or no
        origin/main; an absent HEAD branch or origin/main also refuses when
        git for-each-ref fails or warns, even about another ref. Or the
        current README.md, a current document under the walk, or a prior
        file the gate reads, is not valid UTF-8; or the current README.md
        or a current document under the walk is not a regular file other
        than a directory (a FIFO, a socket, a character or block device),
        which is refused without being read; or the current README.md or a
        current document under the walk cannot be read (an OSError: a
        symlink, dangling or not, which is not followed; a directory named
        *.md; no read permission). Each one is opened once, non-blocking
        and without following a symlink, its type is read from that
        descriptor (fstat), and its text is read and decoded from that same
        descriptor, so a file swapped for a FIFO after the walk listed it
        is refused, not opened blocking; or there is no current README.md
        (no entry by that name), since it holds the Library Version; or a
        directory under the walk cannot be listed (os.scandir fails on it,
        for example for want of read permission), named by its path, since
        a document in it would not be compared. Once the prior state is found (or found absent), and
        before it reads any prior file and before the no-prior pass, the
        gate reads and decodes the current README.md and every current
        document under the walk; it names every one that is missing, not a
        regular file, not UTF-8 or cannot be read, and every directory the
        walk cannot list, one stderr line each, sorted by path, and exits 2
        without comparing anything, so in that run a version that decreased
        and a library FAIL are not reported (3b624). Otherwise it then reads
        the prior README.md, and a document's prior copy only when its
        current copy has a version; a prior file that is not UTF-8 is
        reported by the generic message, unnamed. With --prior-readme, once
        the supplied file is read, the current README.md is read the same
        way, and one that is missing, not a regular file, not UTF-8 or
        cannot be read is named, exit 2; the walk is not run in that mode.
    Remaining: a REPO_ROOT with no .git, with GIT_DIR unset, inside another
    work tree reads that work tree's history, as before, and inside a
    repository git cannot open reads as no repository; with no .git, GIT_DIR
    naming any non-bare repository with no work tree set is read as
    REPO_ROOT's, because git takes REPO_ROOT as its work tree (see
    find_prior_ref). The document walk reads only *.md files, so a non-.md
    document is not compared; a current document with no version line is
    not compared, and its prior copy is not read; a document that exists
    only at the prior ref (a deletion, or the old name of a rename) is not
    compared; and the walk reads untracked .md files too, so an untracked
    one that is not UTF-8, not a regular file or cannot be read also
    refuses. The walk does not descend into a symlinked directory, and it
    does not list the exempt directories (.git, .claude, references and
    the rest of DEFAULT_EXEMPT_DIRS), so one of those that cannot be
    listed does not refuse; an exempt root (.corpus-management) is listed,
    and a directory under it that cannot be listed refuses. O_NOFOLLOW
    checks only the last path component, so a directory swapped for a
    symlink after the walk listed it is still followed; where
    the platform lacks O_NOFOLLOW or O_NONBLOCK, a symlink is followed or a
    FIFO's open can block, as before; where it lacks O_NOCTTY, opening a
    terminal device can still make it the controlling terminal. The
    --prior-readme file is opened once with the same flags, and its type is
    read from that descriptor (3b643 r2), so a symlink passed as
    --prior-readme is refused, not followed.
"""

from __future__ import annotations

import argparse
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from aiqt_corpus import iter_non_code_lines  # noqa: E402  # generic core (behaviour-identical to lint_common)
from lint_common import is_default_exempt_root, DEFAULT_EXEMPT_DIRS, REPO_ROOT, tree_entry_type  # noqa: E402  # grc-config/store, stays local


CALVER_RE = re.compile(r"\*\*Library Version:\*\*\s+(\d+)\.(\d+)\.(\d+)")
SEMVER_RE = re.compile(r"^\*\*Version:\*\*\s+(\d+)\.(\d+)\.(\d+)")


def parse_calver(text: str) -> tuple[int, int, int] | None:
    """Find the first ``**Library Version:** YYYY.MM.patch`` outside a fenced code block."""
    for _, line in iter_non_code_lines(text):
        m = CALVER_RE.search(line)
        if m:
            return tuple(int(x) for x in m.groups())  # type: ignore[return-value]
    return None


def parse_semver(text: str) -> tuple[int, int, int] | None:
    """Find the first ``**Version:** x.y.z`` outside a fenced code block.

    Reading the version only from non-code lines prevents template metadata
    blocks (e.g. the contributor template inside ``CONTRIBUTING.md``'s fenced
    code region, or the ``docs/worked-example.md`` walkthrough) from being
    mistaken for the file's real metadata. See the regression fixture in
    ``tests/test_linters.py::LibraryVersionMonotonicityTests`` for the
    template-version-ignored case.
    """
    for _, line in iter_non_code_lines(text):
        m = SEMVER_RE.match(line)
        if m:
            return tuple(int(x) for x in m.groups())  # type: ignore[return-value]
    return None


def git_show(ref: str, path: str) -> str | None:
    """Return file content at the given git ref, or None if ``ref`` holds no file at ``path``.

    A failed read is None only when ``tree_entry_type`` establishes that no blob is there; a
    bad ref, an unreadable tree or a missing or corrupt blob raises CalledProcessError, which
    main() reports as exit 2, so a git failure cannot read as "no prior to compare" (3b551). A
    blob that is not UTF-8 raises UnicodeDecodeError, which main() also reports as exit 2. The
    trailing ``--`` makes git read ``ref:path`` only as an object name, so an absent path holding
    a glob character is a failed read (then None), not a pathspec that prints nothing."""
    try:
        return subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "show", f"{ref}:{path}", "--"],
            stderr=subprocess.PIPE,
        ).decode("utf-8")
    except subprocess.CalledProcessError:
        if tree_entry_type(ref, path, repo=REPO_ROOT) != "blob":
            return None
        raise


class CurrentDocumentsUnreadable(Exception):
    """One or more current documents are not valid UTF-8, are not a regular file, or cannot be
    read (an OSError: a symlink, a directory, no permission), a directory under the
    walk cannot be listed, or README.md is missing, so versions cannot be read (3b624);
    ``problems`` holds (path, reason) pairs, and main() names each one and reports exit 2."""

    def __init__(self, problems: list[tuple[str, str]]) -> None:
        super().__init__(", ".join(rel for rel, _ in problems))
        self.problems = problems


UNREAD = "; its version cannot be read"

SPECIAL_FILES = ((stat.S_ISFIFO, "a FIFO"), (stat.S_ISSOCK, "a socket"),
                 (stat.S_ISCHR, "a character device"), (stat.S_ISBLK, "a block device"))

OPEN_FLAGS = (os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0)
              | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOCTTY", 0))


def read_current(path: Path, rel: str, problems: list[tuple[str, str]]) -> str | None:
    """Return the decoded text of the current file ``path``, or None after appending
    (``rel``, reason) to ``problems`` when it is not UTF-8, is not a regular file, or cannot
    be read (3b624).

    ``path`` is opened once with OPEN_FLAGS, and its type and text both come from that
    descriptor (r5). r4 stat'ed the path and then opened it again by name, so a file swapped
    for a FIFO between the two calls was opened blocking and the gate hung. O_NONBLOCK makes
    opening a FIFO return at once; fstat then refuses anything but a regular file or a
    directory (a FIFO, a device) without reading it. Opening a Unix socket fails (ENXIO), so
    a socket never reaches fstat and is refused as an open error. O_NOFOLLOW makes a symlink,
    dangling or not, fail the open (ELOOP), so it is refused as an open error, the way round 3
    refused a dangling one. A directory falls through to the read, which refuses it as round 3
    did (IsADirectoryError). O_NOCTTY keeps a terminal device named *.md from becoming the
    controlling terminal of a gate run as a session leader with none; fstat then refuses it as a
    character device (3b643). The text is decoded as read_text() decoded it (UTF-8, universal
    newlines)."""
    try:
        fd = os.open(path, OPEN_FLAGS)
    except OSError as exc:
        problems.append((rel, f"cannot be read ({type(exc).__name__}){UNREAD}"))
        return None
    try:
        mode = os.fstat(fd).st_mode
        if not stat.S_ISREG(mode) and not stat.S_ISDIR(mode):
            kind = next((name for test, name in SPECIAL_FILES if test(mode)), "a special file")
            problems.append((rel, f"is not a regular file ({kind}), so it is not read{UNREAD}"))
            return None
        with open(fd, encoding="utf-8", closefd=False) as handle:
            return handle.read()
    except UnicodeDecodeError:
        problems.append((rel, f"is not valid UTF-8{UNREAD}"))
    except OSError as exc:
        problems.append((rel, f"cannot be read ({type(exc).__name__}){UNREAD}"))
    finally:
        os.close(fd)
    return None


def read_prior_readme(path: Path) -> str | None:
    """Return the decoded --prior-readme file ``path``, or None when there is no entry by that
    name or it is not a regular file; another OSError or a UnicodeDecodeError propagates.

    ``path`` is opened once with OPEN_FLAGS, as read_current opens a document, and fstat on that
    descriptor refuses anything but a regular file without reading it (3b643 r2). It used to be
    checked with is_file() and then opened again by read_text(), without O_NOCTTY, so a path
    swapped for a terminal device between the two calls was opened without it. O_NOFOLLOW makes
    a symlink fail the open (ELOOP), so it is refused as an open error; is_file() followed it."""
    try:
        fd = os.open(path, OPEN_FLAGS)
    except FileNotFoundError:
        return None
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            return None
        with open(fd, encoding="utf-8", closefd=False) as handle:
            return handle.read()
    finally:
        os.close(fd)


def read_current_readme(problems: list[tuple[str, str]]) -> str | None:
    """Return the decoded current README.md, or None after appending a problem (3b624 r4).

    README.md holds the Library Version this gate compares, so a missing one is named like one
    that cannot be read, in every mode (with a prior state, on a root commit, and under
    --prior-readme); it used to raise FileNotFoundError later, a traceback with exit 1, or pass
    unread with no prior state."""
    readme = REPO_ROOT / "README.md"
    if not os.path.lexists(readme):
        problems.append(("README.md", "does not exist; the library version cannot be read"))
        return None
    return read_current(readme, "README.md", problems)


def report_unreadable(problems: list[tuple[str, str]]) -> int:
    """Print one stderr line per current document that cannot be read; return exit 2."""
    for rel, reason in problems:
        print(f"ERROR: {rel} {reason}, so monotonicity is unchecked.", file=sys.stderr)
    return 2


class GitStateUnreadable(Exception):
    """git does not open REPO_ROOT's own repository, or HEAD or origin/main exists but does not
    resolve to a commit git can read, or git skips a record of it (3b551); main() reports it as
    exit 2."""


def find_prior_ref() -> str | None:
    """Return a git ref naming the prior committed state, or None when there is none.

    On a feature branch, prefer origin/main (``refs/remotes/origin/main``) as the comparison
    point. When HEAD matches origin/main (we're on main, or main is up to date), fall through to
    HEAD~1. Local `main` is not used because it can be stale.

    The repository read must be REPO_ROOT's own (3b551). When REPO_ROOT has a ``.git`` entry (a
    directory, a gitdir file, or a symlink, dangling or not) or GIT_DIR is set, git must open a
    repository whose work tree (``rev-parse --show-toplevel``) is REPO_ROOT; otherwise this
    raises GitStateUnreadable naming the repository git refused (REPO_ROOT's ``.git``, or the
    one GIT_DIR names). That covers a repository git cannot open (a HEAD or config it cannot
    parse, an unknown repository extension, dubious ownership, a ``.git`` file naming no
    repository, GIT_DIR naming a missing or broken one); a ``.git`` git skips as unusable (a
    garbage HEAD, no ``refs/``, an empty directory, a dangling symlink) while it opens an
    enclosing repository instead; and a repository with no work tree or another one (a bare
    GIT_DIR, GIT_WORK_TREE or ``core.worktree`` naming another directory or a missing one).
    With GIT_DIR set beside a ``.git``, ``rev-parse --absolute-git-dir`` must name the same git
    dir with and without GIT_DIR: a git hook exports GIT_DIR naming the repository it runs in,
    the one discovery finds, but with no work tree set git takes REPO_ROOT as the work tree of
    any non-bare repository GIT_DIR names. With no ``.git`` and GIT_DIR unset, a failed
    ``rev-parse --git-dir`` is no repository. Residuals: such a REPO_ROOT inside another work
    tree still reads that work tree's history, and inside a broken repository (one git cannot
    open) fails that read too and still reads as no repository; and with no ``.git``, GIT_DIR
    naming any non-bare repository with no work tree set, or one whose work tree is REPO_ROOT,
    is read as REPO_ROOT's.

    HEAD and origin/main are read by their exact names. ``symbolic-ref -q`` follows a symbolic
    ref to the last name in its chain (exit 0), exits 1 for a name that is not symbolic or does
    not exist, and 128 when git cannot parse a ref in the chain; ``show-ref --verify`` then
    reads that one name. rev-parse's lookup also tries ``refs/<name>``, ``refs/tags/<name>``,
    ``refs/heads/<name>``, ``refs/remotes/<name>`` and ``refs/remotes/<name>/HEAD`` and skips one
    that is broken, so a ref by any of those names stood in for a broken or absent HEAD or
    origin/main (and a short ``origin/main`` meant a local branch or tag first). The object the
    name holds is read as ``<object>^{commit}``, which makes git parse the commit, so a missing
    commit or a malformed parent line fails there, not at HEAD~1, where it would look like a
    root commit. A ref is absent only when its chain ends at a ref that does not exist (an
    unborn HEAD, no origin/main, a dangling symbolic origin/main); one git cannot parse, or
    whose object is missing, malformed or not a commit, raises GitStateUnreadable. git also
    reads some records it skips as a ref that does not exist (``show-ref --verify`` exits 1 and
    ``symbolic-ref -q`` exits 1): a malformed or unsorted packed-refs line, a dangling loose
    symlink, a loose file where a directory on the ref's path should be. So a ref reads as
    absent only when ``for-each-ref``, which reads every record, exits 0, writes nothing to
    stderr and does not list it, and its loose path (``rev-parse --git-path``) holds nothing or
    a plain directory (a remote branch ``main/x`` keeps ``refs/remotes/origin/main/``);
    otherwise it raises GitStateUnreadable. An unrelated ref that makes ``for-each-ref`` fail or
    warn therefore refuses an absent HEAD branch or origin/main too: a false refusal, not a
    pass. There is no prior state when there is no repository, when HEAD is unborn, or when
    HEAD's commit has no parent (a root commit, or the boundary of a shallow clone) and
    origin/main is absent or is HEAD. The plumbing predates ``show-ref --exists``.
    ``show-ref --verify`` reads HEAD from git 2.12; an older git refuses a detached HEAD rather
    than reading it as absent. The names returned are read again by git_show, whose lookup
    tries the exact name first, and that name resolved here.
    """
    def git(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", str(REPO_ROOT), *args],
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    def commit(name: str) -> str | None:
        chain = git("symbolic-ref", "-q", name)
        if chain.returncode not in (0, 1):
            raise GitStateUnreadable(f"cannot read {name}: git cannot parse it or a ref it points "
                                     f"to (git symbolic-ref -q exited {chain.returncode})")
        ref = os.fsdecode(chain.stdout.strip()) if chain.returncode == 0 else name
        label = name if ref == name else f"{name} ({ref})"
        exact = git("show-ref", "--verify", "--hash", ref)
        if exact.returncode == 0:
            oid = exact.stdout.decode().strip()
            read = git("rev-parse", "--verify", "--quiet", f"{oid}^{{commit}}")
            if read.returncode == 0:
                return read.stdout.decode().strip()
            raise GitStateUnreadable(f"cannot read {label}: it names {oid}, which is not a commit "
                                     f"git can read (git rev-parse --verify exited "
                                     f"{read.returncode})")
        listed = git("show-ref", "--verify", "--quiet", ref).returncode
        # 1 is a ref that does not exist (symbolic-ref refused one git cannot parse). HEAD always
        # exists in a repository git opens, so a detached HEAD read as absent is a git before
        # 2.12, whose show-ref --verify does not read HEAD.
        if listed != 1 or ref == "HEAD":
            raise GitStateUnreadable(f"cannot read {label}: git cannot find the object it names, "
                                     f"or cannot read the ref (git show-ref --verify exited "
                                     f"{exact.returncode}, and {listed} with --quiet)")
        # Iteration reads every ref record, so it reports one the exact read skipped as absent.
        every = subprocess.run(["git", "-C", str(REPO_ROOT), "for-each-ref",
                                "--format=%(refname)"], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        if (every.returncode != 0 or every.stderr.strip()
                or os.fsencode(ref) in every.stdout.splitlines()):
            raise GitStateUnreadable(f"cannot read {label}: git lists it, or cannot list "
                                     f"every ref (git for-each-ref exited {every.returncode})")
        git_path = git("rev-parse", "--git-path", ref)
        if git_path.returncode != 0:
            raise GitStateUnreadable(f"cannot read {label}: git cannot name its loose path (git "
                                     f"rev-parse --git-path exited {git_path.returncode})")
        loose = os.fsdecode(git_path.stdout.rstrip(b"\n"))
        path = os.path.join(REPO_ROOT, loose)
        # A plain directory there holds other refs: a branch main/x keeps refs/remotes/origin/main/.
        if os.path.lexists(path) and not (os.path.isdir(path) and not os.path.islink(path)):
            raise GitStateUnreadable(f"cannot read {label}: {loose} exists")
        return None

    gitdir = os.environ.get("GIT_DIR")
    repository = (str(REPO_ROOT / ".git") if gitdir is None
                  else f"the repository GIT_DIR names ({gitdir})")
    named = gitdir is not None or os.path.lexists(REPO_ROOT / ".git")
    opened = git("rev-parse", "--git-dir")
    if opened.returncode != 0:
        if not named:
            return None
        raise GitStateUnreadable(f"git will not open {repository} (git rev-parse --git-dir exited "
                                 f"{opened.returncode})")
    if named:
        top = git("rev-parse", "--show-toplevel")
        refused = f"git will not open {repository} as {REPO_ROOT}'s repository"
        if top.returncode != 0:
            raise GitStateUnreadable(f"{refused}: the repository it opens has no work tree (git "
                                     f"rev-parse --show-toplevel exited {top.returncode})")
        work_tree = os.fsdecode(top.stdout.rstrip(b"\n"))
        try:
            own = os.path.samefile(work_tree, REPO_ROOT)
        except OSError:
            own = False
        if not own:
            raise GitStateUnreadable(f"{refused}: the repository it opens has its work tree at "
                                     f"{work_tree}")
    if gitdir is not None and os.path.lexists(REPO_ROOT / ".git"):
        # A hook's GIT_DIR names the git dir discovery finds; with no work tree set, git takes
        # REPO_ROOT as the work tree of any non-bare repository GIT_DIR names.
        named_dir = git("rev-parse", "--absolute-git-dir")
        found = subprocess.run(["git", "-C", str(REPO_ROOT), "rev-parse", "--absolute-git-dir"],
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                               env={k: v for k, v in os.environ.items() if k != "GIT_DIR"})
        dirs = [os.fsdecode(r.stdout.rstrip(b"\n")) if r.returncode == 0
                else f"nothing (exit {r.returncode})" for r in (found, named_dir)]
        try:
            same = found.returncode == named_dir.returncode == 0 and os.path.samefile(*dirs)
        except OSError:
            same = False
        if not same:
            raise GitStateUnreadable(f"{refused}: it is not {REPO_ROOT / '.git'} (git rev-parse "
                                     f"--absolute-git-dir prints {dirs[0]} without GIT_DIR, "
                                     f"{dirs[1]} with it)")
    origin_main = "refs/remotes/origin/main"
    head = commit("HEAD")
    origin_main_commit = commit(origin_main)
    if origin_main_commit and head and origin_main_commit != head:
        return origin_main
    # Fallback: HEAD~1. HEAD's commit parsed above, so this fails only when it has no parent.
    # Unpeeled on purpose: HEAD~1^{commit} fails on a missing parent, reading as a root commit.
    if head and git("rev-parse", "--verify", "--quiet", "HEAD~1").returncode == 0:
        return "HEAD~1"
    return None


def check_library_version(prior_ref: str, current_text: str) -> tuple[bool, str]:
    """Return (ok, message). ok=True if current >= prior.

    ``current_text`` is the current README.md as read_current_documents() decoded it, so the
    file is not read a second time."""
    current = parse_calver(current_text)
    prior_text = git_show(prior_ref, "README.md")
    prior = parse_calver(prior_text) if prior_text else None
    if current is None:
        return (False, "Library Version not found in current README.md")
    if prior is None:
        return (True, f"current {current} (no prior to compare)")
    if current < prior:
        return (
            False,
            f"Library Version decreased: current {'.'.join(map(str, current))} "
            f"< prior {'.'.join(map(str, prior))}",
        )
    return (True, f"current {'.'.join(map(str, current))} >= prior {'.'.join(map(str, prior))}")


def walk_current_documents(problems: list[tuple[str, str]]) -> list[tuple[Path, str]]:
    """Return (path, rel) for every current document under the walk, without reading any.

    The walk lists every entry named *.md under REPO_ROOT, of any type, and does not descend
    into a symlinked directory: the set Path.rglob("*.md") yields. It used rglob, which drops
    a directory it cannot list without a word, so a document in one was never compared and the
    gate printed OK (3b624 r4). os.walk reports that failure to ``onerror``, which appends the
    directory to ``problems``. The exempt directories are pruned by name, so one of them that
    cannot be listed is not reported; every path the walk yields is still filtered as before."""
    skip_dirs = DEFAULT_EXEMPT_DIRS

    def unlisted(exc: OSError) -> None:
        where = Path(os.fsdecode(exc.filename)) if exc.filename is not None else REPO_ROOT
        if any(part in skip_dirs for part in where.parts):
            return
        try:
            rel = where.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            rel = str(where)
        problems.append((rel, f"is a directory that cannot be listed ({type(exc).__name__}); "
                              f"the versions of the documents in it cannot be read"))

    found: list[tuple[Path, str]] = []
    # Walk markdown files in artefact domains; skip non-artefact directories.
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT, onerror=unlisted):
        names = [*dirnames, *filenames]
        dirnames[:] = [name for name in dirnames if name not in skip_dirs]
        for name in names:
            if not name.endswith(".md"):
                continue
            path = Path(dirpath) / name
            if is_default_exempt_root(path, repo_root=REPO_ROOT):
                continue
            if any(part in skip_dirs for part in path.parts):
                continue
            rel = path.relative_to(REPO_ROOT).as_posix()
            # Skip README.md (covered by library version check above).
            if rel == "README.md":
                continue
            # Skip CHANGELOG (no Version metadata field).
            if rel == "CHANGELOG.md":
                continue
            found.append((path, rel))
    return found


def read_current_documents(
        require_readme: bool = False) -> tuple[str | None, list[tuple[str, str]]]:
    """Read and decode the current README.md and every current document under the walk;
    return the README.md text and the documents' (path, text) pairs.

    Every document is decoded before any prior blob is read, so a document that is not valid
    UTF-8 or cannot be read is named even when a prior read would fail. The current README.md,
    which the walk skips, is decoded here too: when ``require_readme`` is set (main() sets it)
    a missing one is a problem, otherwise it is read only when there is an entry by that name
    and its text is None when there is not. The walk yields every entry named *.md, so a
    symlink or a directory is opened and refused, not skipped: the walk never skipped one (its
    read raised), and git can hold a document at that path in the prior state; a FIFO or a
    device is opened without blocking and refused without being read, each from the one
    descriptor read_current() opens, and a socket, which cannot be opened (ENXIO), is
    refused as an open error. If any is not UTF-8, is not a
    regular file or cannot be read, or a directory under the walk cannot be listed, this
    raises CurrentDocumentsUnreadable naming every one (3b624)."""
    documents: list[tuple[str, str]] = []
    problems: list[tuple[str, str]] = []
    readme_text = None
    if require_readme or os.path.lexists(REPO_ROOT / "README.md"):
        readme_text = read_current_readme(problems)
    for path, rel in walk_current_documents(problems):
        text = read_current(path, rel, problems)
        if text is not None:
            documents.append((rel, text))
    if problems:
        raise CurrentDocumentsUnreadable(sorted(problems))
    return readme_text, documents


def check_document_versions(prior_ref: str,
                            documents: list[tuple[str, str]] | None = None) -> list[tuple[str, str]]:
    """Return list of (path, message) for documents whose version decreased.

    ``documents`` is read_current_documents()'s list of documents; when omitted it is read
    here, so a current document that is not UTF-8 or cannot be read raises
    CurrentDocumentsUnreadable before any prior read."""
    findings: list[tuple[str, str]] = []
    if documents is None:
        documents = read_current_documents()[1]
    for rel, current_text in documents:
        current = parse_semver(current_text)
        if current is None:
            continue
        prior_text = git_show(prior_ref, rel)
        if prior_text is None:
            continue
        prior = parse_semver(prior_text)
        if prior is None:
            continue
        if current < prior:
            findings.append(
                (
                    rel,
                    f"Version decreased: current {'.'.join(map(str, current))} "
                    f"< prior {'.'.join(map(str, prior))}",
                )
            )
    return findings


def check_library_version_against_text(prior_text: str, current_text: str) -> tuple[bool, str]:
    """Variant of check_library_version that takes prior README text directly.

    Used by the ``--prior-readme`` mode to exercise the version-comparison
    logic without invoking git. ``current_text`` is the current README.md as
    read_current_readme() decoded it.
    """
    current = parse_calver(current_text)
    prior = parse_calver(prior_text)
    if current is None:
        return (False, "Library Version not found in current README.md")
    if prior is None:
        return (False, "Library Version not found in supplied prior README")
    if current < prior:
        return (
            False,
            f"Library Version decreased: current {'.'.join(map(str, current))} "
            f"< prior {'.'.join(map(str, prior))}",
        )
    return (True, f"current {'.'.join(map(str, current))} >= prior {'.'.join(map(str, prior))}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Enforce that library and document versions never decrease."
    )
    parser.add_argument(
        "--prior-readme",
        type=Path,
        default=None,
        help="Compare against the CalVer in this file instead of git history "
             "(library-version check only; document-versions skipped).",
    )
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    if args.prior_readme is not None:
        # 3b50b2d2: a missing, empty or non-file --prior-readme used to raise a traceback.
        # 3b643 r2: it is opened once, with O_NOCTTY, and its type read from that descriptor.
        prior_text = None
        if str(args.prior_readme).strip() and str(args.prior_readme) != ".":
            try:
                prior_text = read_prior_readme(args.prior_readme)
            except (OSError, UnicodeDecodeError) as exc:
                print(f"ERROR: --prior-readme {args.prior_readme}: cannot be read ({exc}).",
                      file=sys.stderr)
                return 2
        if prior_text is None:
            print(f"ERROR: --prior-readme {args.prior_readme}: not a regular file; nothing to "
                  f"compare against.", file=sys.stderr)
            return 2
        # 3b624 r3: the current README.md is decoded as in read_current_documents, so one that
        # is not UTF-8 or cannot be read is named with exit 2, not a traceback; r4: a missing
        # one too.
        problems: list[tuple[str, str]] = []
        current_text = read_current_readme(problems)
        if problems or current_text is None:
            return report_unreadable(problems)
        lib_ok, lib_msg = check_library_version_against_text(prior_text, current_text)
        if lib_ok:
            print(f"OK: library version is monotonic non-decreasing (vs supplied prior).")
            print(f"  Library: {lib_msg}")
            return 0
        print(f"FAIL [library]: {lib_msg}")
        return 1

    try:
        prior_ref = find_prior_ref()
    except GitStateUnreadable as exc:
        print(f"ERROR: {exc}. That is a git read failure, not no repository, an unborn HEAD, a "
              f"root commit or no origin/main, so monotonicity is unchecked.", file=sys.stderr)
        return 2
    # 3b624: every current document is decoded before any prior read and before the no-prior
    # return, so each one that is not UTF-8 or cannot be read is named, on a root commit too;
    # r4: so is a missing README.md and a directory the walk cannot list.
    try:
        readme_text, documents = read_current_documents(require_readme=True)
    except CurrentDocumentsUnreadable as exc:
        return report_unreadable(exc.problems)
    assert readme_text is not None  # require_readme: a missing README.md raised above
    if prior_ref is None:
        print("OK: no prior committed state available; monotonicity not checked.")
        return 0
    try:
        lib_ok, lib_msg = check_library_version(prior_ref, readme_text)
        doc_findings = check_document_versions(prior_ref, documents)
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: cannot read the prior state at {prior_ref} ({exc}); a git read failure is "
              f"not an absent prior version, so monotonicity is unchecked.", file=sys.stderr)
        return 2
    except UnicodeDecodeError as exc:
        print(f"ERROR: a file at {prior_ref} is not valid UTF-8 ({exc}); its "
              f"version cannot be read, so monotonicity is unchecked.", file=sys.stderr)
        return 2
    if lib_ok and not doc_findings:
        print(f"OK: library and document versions are monotonic non-decreasing (vs {prior_ref}).")
        print(f"  Library: {lib_msg}")
        return 0
    if not lib_ok:
        print(f"FAIL [library]: {lib_msg}")
    if doc_findings:
        print(f"FAIL [documents]: {len(doc_findings)} version regression(s) vs {prior_ref}:")
        for rel, msg in doc_findings:
            print(f"  {rel}: {msg}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
