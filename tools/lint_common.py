"""Shared helpers for the audit-programme linters in ``tools/``.

This module exposes functions that 11+ linters previously copied
verbatim: the repository root constant, the default-exempt-directory
set, the markdown-target eligibility check, the directory-walking
target iterator, the UTF-8-safe text reader, and the
fenced-code-block-aware line iterator.

The module is deliberately minimal. It does not encapsulate per-linter
exemption lists, per-linter regex patterns, or per-linter scan logic;
each linter retains its own rule set, and the helpers expose hooks for
linters to pass their own exempt-file / exempt-directory sets.

Stdlib-only Python 3.11. No third-party dependencies.

Scope notes:

- ``REPO_ROOT`` is computed from this file's location: the parent of
  ``tools/`` is the repository root. Linters that import this constant
  inherit the same value.
- ``DEFAULT_EXEMPT_DIRS`` mirrors the set 13+ linters already defined
  inline: ``.git``, ``node_modules``, ``__pycache__``. Linters that
  need additional exempt directories pass them via the ``exempt_dirs``
  argument.
- ``iter_markdown_targets`` and ``is_markdown_target`` deliberately
  accept ``Iterable[str]`` for ``exempt_files`` so callers can pass a
  ``set``, ``frozenset``, or ``list`` interchangeably.
- ``iter_non_code_lines`` yields ``(lineno, line)`` skipping any line
  inside a fenced code block (lines bounded by lines beginning with
  ``` ``` ```). The fence-start and fence-end lines are also skipped.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from pathlib import Path

# Repository root: the parent of ``tools/``.
REPO_ROOT: Path = Path(__file__).resolve().parent.parent

# Default directory parts that every linter skips when walking the
# repository. Frozen so callers cannot mutate the shared default.
# ``.claude`` holds this project's Claude Code AI-assistant config
# (project CLAUDE.md and draggable rule files copied from the
# dev-security/claude-rules/ pack); like that pack directory, its
# contents are AI-context artefacts, not governed corpus documents,
# so the corpus linters skip it.
# ``.working`` holds maintainer working state: per-run records from
# /validate, /fitness, and other maintainer-invoked activities. The
# contents are frozen-state archives by design (cross-references
# accurate as-of write-time, not maintained against subsequent corpus
# changes), so the corpus linters skip them. See ``.working/README.md``
# for the convention.
DEFAULT_EXEMPT_DIRS: frozenset[str] = frozenset(
    {".git", "node_modules", "__pycache__", ".claude", ".working"}
)


# Default suffix set for markdown-only linters.
MARKDOWN_SUFFIXES: frozenset[str] = frozenset({".md"})


def is_target(
    path: Path,
    *,
    suffixes: Iterable[str] = MARKDOWN_SUFFIXES,
    exempt_dirs: Iterable[str] = DEFAULT_EXEMPT_DIRS,
    exempt_files: Iterable[str] = (),
) -> bool:
    """Return True if ``path`` is a file the linter should scan.

    A path is a target when:
      - its suffix is in ``suffixes``;
      - none of its directory parts appears in ``exempt_dirs``;
      - its filename (``path.name``) is not in ``exempt_files``.

    The caller passes its own suffix and exempt sets. The defaults are
    the minimum-common-denominator across markdown linters: scan only
    ``.md``; skip ``.git``, ``node_modules``, ``__pycache__``; no
    per-file exemptions.

    Implementation note: if the same exempt sets are checked many times
    (e.g., during a recursive walk), prefer to pass pre-constructed
    ``set`` / ``frozenset`` values so the conversion happens once
    rather than per call. ``iter_targets`` does this internally.
    """
    suffixes_set = suffixes if isinstance(suffixes, (set, frozenset)) else set(suffixes)
    exempt_dirs_set = exempt_dirs if isinstance(exempt_dirs, (set, frozenset)) else set(exempt_dirs)
    exempt_files_set = exempt_files if isinstance(exempt_files, (set, frozenset)) else set(exempt_files)
    if path.suffix not in suffixes_set:
        return False
    if any(part in exempt_dirs_set for part in path.parts):
        return False
    if path.name in exempt_files_set:
        return False
    return True


def is_markdown_target(
    path: Path,
    *,
    exempt_dirs: Iterable[str] = DEFAULT_EXEMPT_DIRS,
    exempt_files: Iterable[str] = (),
) -> bool:
    """Return True if ``path`` is a markdown file the linter should scan.

    Convenience wrapper around :func:`is_target` with the markdown suffix
    set. Retained for callers that scan only ``.md``.
    """
    return is_target(
        path,
        suffixes=MARKDOWN_SUFFIXES,
        exempt_dirs=exempt_dirs,
        exempt_files=exempt_files,
    )


def iter_targets(
    paths: Iterable[str | Path],
    *,
    suffixes: Iterable[str] = MARKDOWN_SUFFIXES,
    exempt_dirs: Iterable[str] = DEFAULT_EXEMPT_DIRS,
    exempt_files: Iterable[str] = (),
) -> list[Path]:
    """Return deduplicated, ordered list of targets matching ``suffixes``.

    For each entry in ``paths``:
      - if it is a file and matches :func:`is_target`, include it;
      - if it is a directory, walk it recursively and include every
        file whose suffix is in ``suffixes`` and that passes
        :func:`is_target`.

    Paths are resolved before deduplication. Order across the input is
    preserved.
    """
    targets: list[Path] = []
    seen: set[Path] = set()
    suffixes_set = set(suffixes)
    exempt_dirs_set = set(exempt_dirs)
    exempt_files_set = set(exempt_files)

    for raw in paths:
        p = Path(raw).resolve()
        if p.is_file():
            if is_target(
                p,
                suffixes=suffixes_set,
                exempt_dirs=exempt_dirs_set,
                exempt_files=exempt_files_set,
            ):
                if p not in seen:
                    targets.append(p)
                    seen.add(p)
        elif p.is_dir():
            for f in p.rglob("*"):
                if not f.is_file():
                    continue
                if is_target(
                    f,
                    suffixes=suffixes_set,
                    exempt_dirs=exempt_dirs_set,
                    exempt_files=exempt_files_set,
                ):
                    if f not in seen:
                        targets.append(f)
                        seen.add(f)
    return targets


def iter_markdown_targets(
    paths: Iterable[str | Path],
    *,
    exempt_dirs: Iterable[str] = DEFAULT_EXEMPT_DIRS,
    exempt_files: Iterable[str] = (),
) -> list[Path]:
    """Return deduplicated, ordered list of markdown targets under ``paths``.

    Convenience wrapper around :func:`iter_targets` with the markdown
    suffix set. Retained for callers that scan only ``.md``.
    """
    return iter_targets(
        paths,
        suffixes=MARKDOWN_SUFFIXES,
        exempt_dirs=exempt_dirs,
        exempt_files=exempt_files,
    )


def read_text_safe(path: Path) -> str | None:
    """Read ``path`` as UTF-8 text; return ``None`` on a decode error.

    Linters that scan a heterogeneous file tree should skip files that
    are not valid UTF-8 (binary files mis-named with ``.md``, lock
    files, etc.) rather than aborting the entire run. The contract is:
    successful return is a string; ``None`` signals "skip this file".

    Filesystem errors (FileNotFoundError, PermissionError) are not
    caught: those represent a real environmental problem the caller
    should surface.
    """
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def iter_non_code_lines(text: str) -> Iterator[tuple[int, str]]:
    """Yield ``(lineno, line)`` for each line outside a fenced code block.

    ``lineno`` is 1-indexed.

    Fence detection (deliberately simple):

      - A fence is a line whose stripped form starts with three
        backticks (``` ``` ```). Lines whose only content is a tilde
        fence (``~~~``) are NOT treated as fences. (The library
        convention is backtick fences; no document currently uses
        tilde fences.)
      - Indentation before the backticks is tolerated (``line.strip()``
        is used). Per CommonMark, fences are valid up to a 3-space
        indent; this function is more permissive but the difference
        does not matter for the current corpus.
      - Fence parsing is a state toggle: every fence line flips
        ``in_code``. A line containing ``\\`\\`\\`` inside an
        inline code block on its own (which is unusual but possible)
        would erroneously toggle the state. The linters that use this
        helper do not encounter this in practice.

    Edge cases:

      - File starts with a fence: the fence line is consumed; lines
        until the next fence are skipped; yielding resumes after the
        close.
      - Unterminated fence: every line after the unclosed fence is
        skipped. The function does not warn about unbalanced fences.
      - Nested or re-opened fences: each fence line toggles state, so
        ``` ``` ... ``` ... ``` ... ``` ``` ``` toggles include/exclude
        in pairs.

    The function does not attempt to recognise matching fence widths
    (CommonMark requires the closing fence to be at least as wide as
    the opening fence); a toggle is a toggle.
    """
    in_code = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        yield lineno, line
