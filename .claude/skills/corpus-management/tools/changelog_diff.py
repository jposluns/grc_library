#!/usr/bin/env python3
"""Added-line diff reading and public line shapes for the CHANGELOG checks.

The CHANGELOG checks that read the lines a change ADDS (delta gates D1
``.claude/skills/corpus-management/tools/check-changelog-on-pr.py``, D3
``.claude/skills/corpus-management/tools/check-changelog-dash-on-pr.py`` and D7 ``.claude/skills/corpus-management/tools/check-changelog-length-on-pr.py``,
and ``.claude/skills/corpus-management/tools/preflight-changelog.py``) share this one pinned ``git diff`` and its parser.

The public ``.working/CHANGELOG.md`` carries weekly summaries only (maintainer-directed
2026-11-13): a weekly paragraph headed ``**Week of YYYY-MM-DD (PRs #FIRST-#LAST)**`` and, for
periods older than 3 months, a monthly paragraph headed ``**YYYY-MM (PRs #FIRST-#LAST)**``. The
per-change entries and any daily summaries belong to the private per-change record. The line
shapes below (:func:`public_line_kind`) are the one definition D1 and D7 share.
In the earlier repository, each gate split ``git diff`` text with splitlines() and
skipped every line starting "+++", so an added line whose text starts with "++"
escaped the check, and a CR, U+2028 or U+0085 inside an added line split it into
fragments that lost their "+" marker.

This is its own module, not part of ``lint_common``, because hooks import ``lint_common``
and HookDescendantIsolationTests requires every subprocess call there to pass a literal
argument list; no hook imports this module.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Iterable


class ChangelogDiffUnreadable(ValueError):
    """The ``git diff`` output could not be read exactly; the caller reports one ERROR line and
    exits 2."""


class GitQueryFailed(Exception):
    """A ``git rev-parse``, ``ls-tree`` or ``ls-files`` that a check runs before the diff failed;
    the message names the command and git's stderr, and the caller prints it as one ERROR line and
    exits 2 (in the earlier repository, a rev-parse failure was reported as "git diff failed")."""


class GitSelectsAnotherTree(Exception):
    """git, run with this process's environment, selects another work tree or repository than
    the one the check expects; the caller prints the reason and exits 2."""


# Environment variables ``added_line_diff`` keeps from git: each changes the context lines or
# how a pathspec matches.
_DROPPED_ENV = frozenset({"GIT_DIFF_OPTS", "GIT_LITERAL_PATHSPECS", "GIT_GLOB_PATHSPECS",
                          "GIT_NOGLOB_PATHSPECS", "GIT_ICASE_PATHSPECS"})


def added_line_diff(revs: Iterable[str], paths: Iterable[str], *, cwd: "Path | str | None" = None,
                    env: "dict[str, str] | None" = None) -> bytes:
    """The bytes of ``git diff <revs> -- <paths>``, run in ``cwd`` with ``env`` (None inherits
    this process's environment), for :func:`parse_added_lines` to read.

    The flags override each setting known to reshape what the parser reads: an external diff
    driver (``diff.external``, ``GIT_EXTERNAL_DIFF``, the ``command`` of a ``diff=<driver>``
    attribute), a ``textconv`` filter, a ``-diff`` or ``binary`` attribute (it prints "Binary
    files ... differ"), colour (``color.diff``, ``color.ui``), and the ``+++ b/`` prefix
    (``diff.noprefix``, ``diff.mnemonicPrefix``, ``diff.dstPrefix``). Each leaves no ``+++ b/``
    header or ``+`` line, so a reader found 0 added lines and passed. They also pin the context:
    ``--inter-hunk-context=0`` (``diff.interHunkContext``), ``-c diff.suppressBlankEmpty=false``,
    and no ``GIT_DIFF_OPTS`` in git's environment (its ``--unified=<n>`` overrides
    ``--unified=0``), since in the earlier repository a blank context line printed as an empty
    line ended a hunk early and lost the added lines in the rest of that hunk. And they pin the
    file pairing: ``--no-renames`` (``diff.renames``, which is true by default), because a file
    that git pairs as a rename or copy of another path in the same diff prints only "similarity
    index", "rename from" or "copy from" lines and the hunk of what changed beyond that, so in
    the earlier repository a new .working/CHANGELOG.md renamed or copied from the detailed
    mirror showed no added line; and ``--no-relative`` (``diff.relative``), which run from a
    subdirectory leaves out every file outside it. They pin the pathspec reading: no
    ``GIT_LITERAL_PATHSPECS`` in git's environment, under which, in the earlier repository, git
    read ``:(top).working/CHANGELOG.md`` as a file of that literal name and the diff came back
    empty, and no ``GIT_GLOB_PATHSPECS``, ``GIT_NOGLOB_PATHSPECS`` or ``GIT_ICASE_PATHSPECS``
    either (the last also matched "changelog.md"), so a path names that file alone. And they pin
    the submodule form: ``--submodule=short`` (in the earlier repository, ``diff.submodule=log``
    printed a "Submodule" line with no file header in place of the gitlink's diff) and
    ``--ignore-submodules=none`` (``diff.ignoreSubmodules``), so the parser sees the mode of a
    gitlink. Not pinned: the source prefix (only the ``---`` line carries it, and the parser
    skips that line), and ``status.renames`` (it applies to ``git status``, not ``git diff``).
    A pathspec is still read from ``cwd``, so a caller that names a file at the repository root
    passes ``:(top)<path>`` or runs in the root. The list is not a proof that no other setting
    reshapes the diff; the parser therefore reads each hunk by its header's line counts, and a
    diff it cannot read exactly raises :class:`ChangelogDiffUnreadable` rather than yielding
    fewer added lines.

    A git failure raises ``CalledProcessError`` carrying git's ``stderr`` as text: an unread
    diff is not zero added lines."""
    cmd = ["git", "-c", "diff.suppressBlankEmpty=false", "diff", "--no-ext-diff",
           "--no-textconv", "--text", "--no-color", "--dst-prefix=b/", "--unified=0",
           "--inter-hunk-context=0", "--no-renames", "--no-relative", "--submodule=short",
           "--ignore-submodules=none", *revs, "--", *paths]
    git_env = {k: v for k, v in (os.environ if env is None else env).items()
               if k not in _DROPPED_ENV}
    proc = subprocess.run(cmd, cwd=None if cwd is None else str(cwd), capture_output=True,
                          env=git_env)
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(
            proc.returncode, cmd, proc.stdout, proc.stderr.decode("utf-8", errors="replace"))
    return proc.stdout


def _git_query(args: list[str], *, cwd: "Path | str | None" = None,
               env: "dict[str, str] | None" = None) -> bytes:
    """The stdout of ``git <args>`` run in ``cwd`` with ``env`` (None inherits this process's
    environment) less the pathspec-reading variables; a failure raises :class:`GitQueryFailed`."""
    git_env = {k: v for k, v in (os.environ if env is None else env).items()
               if k not in _DROPPED_ENV}
    proc = subprocess.run(["git", *args], cwd=None if cwd is None else str(cwd),
                          capture_output=True, env=git_env)
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", errors="replace").strip()
        raise GitQueryFailed(f"git {args[0]} failed (exit {proc.returncode})"
                             + (f": {detail}" if detail else ""))
    return proc.stdout


def foreign_repo_env() -> dict[str, str]:
    """This process's environment for git in ANOTHER repository, or in the repository git finds
    by itself: every variable that ``git rev-parse --local-env-vars`` names as local to one
    repository is dropped (GIT_INDEX_FILE, GIT_DIR, GIT_WORK_TREE, GIT_OBJECT_DIRECTORY,
    GIT_ALTERNATE_OBJECT_DIRECTORIES, GIT_COMMON_DIR, GIT_CONFIG_PARAMETERS and the rest; git
    drops the same list before it enters a submodule), and every other variable is kept. A
    pre-commit hook inherits them for the PUBLIC repository (``git commit -a`` names its
    temporary index in GIT_INDEX_FILE), and in the earlier repository the preflight's mirror
    ``git diff --cached`` in the operational store read that index through them: it found no
    staged mirror addition, so a commit the standalone aid refuses passed. A failure to list
    them raises :class:`GitQueryFailed`."""
    local = set(_git_query(["rev-parse", "--local-env-vars"]).decode("utf-8").split())
    return {k: v for k, v in os.environ.items() if k not in local}


def git_selection(cwd: "Path | str | None" = None,
                  env: "dict[str, str] | None" = None) -> tuple[Path, Path]:
    """(work tree root, repository directory) that git selects run in ``cwd`` with ``env``. A
    bare repository, or no repository, raises :class:`GitQueryFailed`."""
    top, git_dir = _git_query(["rev-parse", "--show-toplevel", "--absolute-git-dir"], cwd=cwd,
                              env=env).decode("utf-8", errors="surrogateescape").splitlines()
    return Path(top), Path(git_dir)


def check_git_selects_root(root: "Path | None" = None, *,
                           cwd: "Path | str | None" = None) -> None:
    """Raise :class:`GitSelectsAnotherTree` unless git, run in ``cwd`` with this process's
    environment (as the diff runs), selects ``root`` as its work tree (None: the work tree git
    finds by itself) and the repository it finds there by itself (shared with D3 and D7). In the
    earlier repository, ``GIT_WORK_TREE`` or ``core.worktree`` naming a subdirectory made the
    preflight's working-tree diff read that directory, so it found no .working/CHANGELOG.md change and
    passed; ``GIT_DIR`` naming a sibling repository made the preflight and D3 and D7 read that
    repository ("OK: .working/CHANGELOG.md not modified"). What git finds by itself is what ``git
    rev-parse`` reports with the variables of :func:`foreign_repo_env` dropped, so a hook's
    ``GIT_INDEX_FILE``, a ``GIT_DIR`` naming this repository, and CI's plain checkout pass. A
    failure to ask git raises :class:`GitQueryFailed`."""
    top, git_dir = git_selection(cwd)
    own_top, own_git_dir = git_selection(cwd, foreign_repo_env())
    expected = own_top if root is None else Path(root)
    if top.resolve() != expected.resolve():
        raise GitSelectsAnotherTree(f"git selects the work tree {top}, not {expected}")
    if git_dir.resolve() != own_git_dir.resolve():
        raise GitSelectsAnotherTree(f"git selects the repository {git_dir}, not {own_git_dir}")


def refuse_links(paths: Iterable[str], rev: "str | None" = None, *,
                 cwd: "Path | str | None" = None, env: "dict[str, str] | None" = None) -> None:
    """Raise :class:`ChangelogDiffUnreadable` when an entry at exactly one of ``paths`` has mode
    120000 or 160000 in the tree of commit ``rev`` (``git ls-tree``, ``paths`` from the root),
    or, when ``rev`` is None, in the index (``git ls-files --stage``, ``paths`` relative to
    ``cwd``). :func:`parse_added_lines` sees a link's mode only when the diff shows that path, so
    in the earlier repository a .working/CHANGELOG.md that was already a symbolic link at the base
    and stayed one, with a bad entry added only to the file it leads to, passed. A git failure
    raises :class:`GitQueryFailed`."""
    wanted = list(paths)
    if rev is None:
        where = "the index"
        out = _git_query(["ls-files", "--stage", "-z", "--", *wanted], cwd=cwd, env=env)
    else:
        where = f"the tree of {rev}"
        out = _git_query(["ls-tree", "--full-tree", "-z", rev, "--", *wanted], cwd=cwd,
                         env=env)
    for record in out.split(b"\0"):
        meta, _, name = record.partition(b"\t")
        mode = meta.split(b" ", 1)[0]
        path = name.decode("utf-8", errors="replace")
        if path in wanted and mode in _LINK_MODES:
            raise ChangelogDiffUnreadable(
                f"{path} has mode {mode.decode()} in {where}, {_LINK_MODES[mode]}, not a "
                "regular file or directory, so the diff does not show the lines of the file it "
                "leads to")


def read_blob(rev: str, path: str, *, cwd: "Path | str | None" = None,
              env: "dict[str, str] | None" = None) -> bytes:
    """The bytes of ``path`` (from the repository root) in the tree of commit ``rev``; a git
    failure raises :class:`GitQueryFailed`."""
    return _git_query(["show", f"{rev}:{path}"], cwd=cwd, env=env)


# Public changelog line shapes. ASCII-only, so a digit outside 0-9 never reads as a date or a
# PR number. A period heading names its first and last PR; a range must rise.
WEEKLY_HEADER_RE = re.compile(
    r"^\*\*Week of (\d{4}-\d{2}-\d{2}) \(PRs #([1-9][0-9]*)(?:-#([1-9][0-9]*))?\)\*\*$", re.ASCII)
MONTHLY_HEADER_RE = re.compile(
    r"^\*\*(\d{4}-\d{2}) \(PRs #([1-9][0-9]*)(?:-#([1-9][0-9]*))?\)\*\*$", re.ASCII)
# The weekly sections written before the per-change record moved out of the public file
# (``## Week of YYYY-MM-DD`` with ``- `` bullets) stay as history; they name no PR range.
LEGACY_WEEK_HEADING_RE = re.compile(r"^## Week of (\d{4}-\d{2}-\d{2})$", re.ASCII)
TITLE = "# Changelog"
# A daily summary heading, ``**YYYY-MM-DD (PRs #A-#B)**`` (or a version range).
DAILY_HEADING_RE = re.compile(r"^[ \t>*_#+-]*\d{4}-\d{2}-\d{2} \((?:PRs?|versions) [^)]*\)\**\s*$",
                              re.ASCII)
# Any other line that opens, after markup only, with a full date: a per-change entry
# (``**2026-11-12 | 2026.11.93 | PR #29** - ...``), a daily roll-up or a dated legacy header.
DATED_LINE_RE = re.compile(r"^[ \t>*_#+-]*\d{4}-\d{2}-\d{2}(?![0-9])", re.ASCII)
# A per-change scaffold bullet (``- PR #29: ...``).
PR_BULLET_RE = re.compile(r"^[ \t>*_#+-]*PRs? #\d+\s*:", re.ASCII | re.IGNORECASE)
SCAFFOLD_MARKERS = ("TIER-SCAFFOLD", "CONDENSE-SCAFFOLD")
# Kinds that open or close a section of the public file.
STRUCTURAL_KINDS = frozenset({"title", "weekly", "monthly", "legacy-weekly", "daily",
                              "per-change", "heading", "scaffold"})


def period_range(match: "re.Match[str]") -> tuple[int, int]:
    """(first PR, last PR) of a weekly or monthly heading match."""
    first = int(match.group(2))
    return first, int(match.group(3)) if match.group(3) else first


def public_line_kind(text: str) -> str:
    """The kind of one public changelog line (one ``str.splitlines()`` part, without its line
    end): ``blank``, ``title``, ``weekly`` or ``monthly`` (a period heading whose PR range
    rises), ``legacy-weekly``, ``daily`` (a daily summary heading), ``per-change`` (a dated
    entry or a ``PR #N:`` bullet), ``scaffold`` (an unauthored scaffold marker), ``heading``
    (any other ``#`` heading or bold line, a period heading with a falling or equal range
    among them) or ``text``."""
    if not text.strip():
        return "blank"
    if text == TITLE:
        return "title"
    for kind, pattern in (("weekly", WEEKLY_HEADER_RE), ("monthly", MONTHLY_HEADER_RE)):
        match = pattern.match(text)
        if match:
            first, last = period_range(match)
            if match.group(3) and last <= first:
                return "heading"
            return kind
    if LEGACY_WEEK_HEADING_RE.match(text):
        return "legacy-weekly"
    if any(marker in text for marker in SCAFFOLD_MARKERS):
        return "scaffold"
    if DAILY_HEADING_RE.match(text):
        return "daily"
    if DATED_LINE_RE.match(text) or PR_BULLET_RE.match(text):
        return "per-change"
    stripped = text.lstrip(" \t")
    if stripped.startswith("#") or stripped.startswith("**"):
        return "heading"
    return "text"


def public_line_parts(text: str) -> list[tuple[int, str]]:
    """(LF line number, part) for every ``str.splitlines()`` part of every LF-ended line of
    ``text``: a CR, U+2028, U+0085 or another line boundary inside a line starts a new part
    (a renderer may start a new line there), and the part keeps its LF line's number. A line
    with no text gives one empty part."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    out: list[tuple[int, str]] = []
    for number, line in enumerate(lines, start=1):
        for part in line.splitlines() or [""]:
            out.append((number, part))
    return out


_DIFF_HUNK_RE = re.compile(rb"@@ -\d+(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
# The new side's mode in a file's extended header: "new file mode", "new mode", or the mode
# both sides share at the end of the "index" line.
_NEW_MODE_RE = re.compile(rb"(?:new file mode |new mode |index [0-9a-f]+\.\.[0-9a-f]+ )(\d+)$")
_LINK_MODES = {b"120000": "a symbolic link", b"160000": "a submodule (gitlink)"}


def parse_added_lines(diff: bytes) -> list[tuple[str, str]]:
    """(file, added-line-text) for every added line in ``diff``, the bytes of a ``git diff``.

    Each hunk is read by the old and new line counts in its ``@@ -a,b +c,d @@`` header (an
    omitted count is 1): a "-" line takes one old line, a "+" line one new line, a " " line or
    an EMPTY line (a blank context line under ``diff.suppressBlankEmpty``) one of each, and a
    "\\" line ("No newline at end of file") none. So a "+" line is an added line even when its
    text starts with "++", and a hunk never ends before its counts are used up. Raises
    ChangelogDiffUnreadable, never yields fewer added lines, when a hunk line does not fit the
    counts, the output ends inside a hunk, a hunk adds lines before any ``+++ b/`` header, a "+"
    line appears outside a hunk, or an added line or a header path is not valid UTF-8. It also
    raises when a file's new side has mode 120000 or 160000: git diffs a symbolic link's target
    path and a gitlink's commit id, not the lines of the file they lead to, so in the earlier
    repository a .working/CHANGELOG.md symlinked to a file holding a bad entry showed one clean
    added line."""
    return [(name, text) for name, _, text in parse_numbered_added_lines(diff)]


def parse_numbered_added_lines(diff: bytes) -> list[tuple[str, int, str]]:
    """(file, line number, added-line-text) for every added line in ``diff``, read and refused
    exactly as :func:`parse_added_lines` reads them; the number is the line's one-based position
    in the file's new side, counted from its hunk header's ``+c`` (for the preflight's
    whole-file dash check)."""
    lines = diff.split(b"\n")
    # Split on LF only: a CR, U+2028 or U+0085 inside an added line is part of that
    # line, so no fragment of it can lose its "+" marker and escape the checks.
    if lines and lines[-1] == b"":
        lines.pop()
    results: list[tuple[str, int, str]] = []
    current: str | None = None
    link: tuple[int, bytes] | None = None  # (diff line, mode) of a link the parser is inside
    old_left = new_left = new_line = 0

    def not_a_file(name: str) -> ChangelogDiffUnreadable:
        number, mode = link
        return ChangelogDiffUnreadable(
            f"{name} has mode {mode.decode()} at diff line {number}, {_LINK_MODES[mode]}, not "
            "a regular file, so the diff shows the link and not the file's lines")

    for number, line in enumerate(lines, start=1):
        if old_left or new_left:
            marker = line[:1]
            if marker == b"+" and new_left:
                new_left -= 1
                try:
                    text = line[1:].decode("utf-8")
                except UnicodeDecodeError:
                    raise ChangelogDiffUnreadable(
                        f"an added line of {current} (diff line {number}) is not valid "
                        "UTF-8") from None
                results.append((current, new_line, text))
                new_line += 1
            elif marker == b"-" and old_left:
                old_left -= 1
            elif marker in (b" ", b"") and old_left and new_left:
                old_left -= 1
                new_left -= 1
                new_line += 1
            elif marker != b"\\":
                raise ChangelogDiffUnreadable(
                    f"diff line {number} does not fit its hunk's line counts")
            continue
        mode = _NEW_MODE_RE.match(line)
        if line.startswith(b"diff --git ") and link:
            raise not_a_file("a file")
        elif mode and mode.group(1) in _LINK_MODES:
            link = (number, mode.group(1))
        elif line.startswith(b"@@"):
            match = _DIFF_HUNK_RE.match(line)
            if match is None:
                raise ChangelogDiffUnreadable(f"diff line {number} is not a hunk header")
            old_left = 1 if match.group(1) is None else int(match.group(1))
            new_line = int(match.group(2))
            new_left = 1 if match.group(3) is None else int(match.group(3))
            if new_left and current is None:
                raise ChangelogDiffUnreadable(
                    f"the hunk at diff line {number} adds lines to no named file")
        elif line.startswith(b"+++ "):
            try:
                header = line.decode("utf-8")
            except UnicodeDecodeError:
                raise ChangelogDiffUnreadable(
                    f"the file header at diff line {number} is not valid UTF-8") from None
            current = header[len("+++ b/"):] if header.startswith("+++ b/") else None
            if link:
                raise not_a_file(current or "a file")
        elif line.startswith(b"+"):
            raise ChangelogDiffUnreadable(f"diff line {number} is an added line outside a hunk")
    if old_left or new_left:
        raise ChangelogDiffUnreadable("the diff ends inside a hunk")
    if link:
        raise not_a_file("a file")
    return results
