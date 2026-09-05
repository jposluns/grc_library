#!/usr/bin/env python3
"""Generic corpus-tool core: the shared discovery, text, date, git, and metadata
primitives a Markdown-corpus linter needs, with no corpus-specific policy baked in.

This is a SHIPPED, importable pack module. AIQT's own gates and any external
adopter (a downstream corpus-management project that takes the AIQT pack as a
dependency) import these helpers instead of each keeping a private copy, so a
fence toggle, a table split, an ISO-date parse, or a metadata-field read is
recognized identically everywhere.

The module is deliberately POLICY-FREE. It carries the generic MECHANISM only;
every corpus-specific choice is passed in by the caller, never hardcoded here:

  - the exempt-directory set and the scan roots are function arguments
    (``exempt_dirs`` / ``exempt_files`` and the ``paths`` a caller enumerates),
    with a minimum-common-denominator default that names only the universal
    VCS/build directories (``.git``, ``node_modules``, ``__pycache__``);
  - the repository root is a required argument to the scan-root walker, never a
    module constant, so a tool with a ``--root`` flag binds its own value;
  - the metadata parser is field-agnostic: it captures every ``**Field:**`` line
    in the head window and returns them, leaving the required-field list and
    per-field validity entirely to the caller.

Stdlib-only, Python 3.11+. No third-party dependencies. Import mechanics: the
pack ships this file under ``tools/``, so a consumer puts that directory on
``sys.path`` and imports by module name, exactly as the pack's own gates do::

    import sys
    from pathlib import Path
    sys.path.insert(0, str(PACK_TOOLS_DIR))   # e.g. Path(__file__).resolve().parent
    from aiqt_corpus import iter_markdown_targets, iter_non_code_lines, parse_metadata_block
"""

from __future__ import annotations

import datetime
import re
import subprocess
from collections.abc import Iterable, Iterator
from pathlib import Path

__all__ = [
    # discovery / targeting
    "is_target",
    "is_markdown_target",
    "iter_targets",
    "iter_markdown_targets",
    "iter_scan_roots_markdown",
    "read_text_safe",
    # text / markdown primitives
    "split_row",
    "is_separator_row",
    "strip_code_spans",
    "is_fence_line",
    "iter_non_code_lines",
    # date
    "parse_iso_date",
    "add_months",
    # git
    "git",
    "git_show",
    # metadata parse mechanism
    "MetadataBlock",
    "parse_metadata_block",
    "head_version",
    # constants
    "MARKDOWN_SUFFIXES",
    "DEFAULT_EXEMPT_DIRS",
    "CODE_SPAN_RE",
    "SIMPLE_CODE_SPAN_RE",
    "METADATA_FIELD_RE",
    "METADATA_HEAD_LINES",
]

# The universal Markdown suffix set. Generic: a caller that scans other suffixes
# passes its own ``suffixes`` argument.
MARKDOWN_SUFFIXES: frozenset[str] = frozenset({".md"})

# Minimum-common-denominator exempt directories: the VCS and build-artefact
# directories no corpus linter should ever descend into. Frozen so callers
# cannot mutate the shared default. This is deliberately the SMALLEST generic
# set; a corpus that exempts further directories (an AI-config directory, a
# working-state directory, an operational-prose directory) passes them through
# the ``exempt_dirs`` argument rather than expecting them to live here.
DEFAULT_EXEMPT_DIRS: frozenset[str] = frozenset({".git", "node_modules", "__pycache__"})


def is_target(
    path: Path,
    *,
    suffixes: Iterable[str] = MARKDOWN_SUFFIXES,
    exempt_dirs: Iterable[str] = DEFAULT_EXEMPT_DIRS,
    exempt_files: Iterable[str] = (),
) -> bool:
    """Return True if ``path`` is a file a linter should scan.

    A path is a target when:
      - its suffix is in ``suffixes``;
      - none of its directory parts appears in ``exempt_dirs``;
      - its filename (``path.name``) is not in ``exempt_files``.

    The caller passes its own suffix and exempt sets. The defaults are the
    minimum-common-denominator across Markdown linters: scan only ``.md``; skip
    ``.git``, ``node_modules``, ``__pycache__``; no per-file exemptions.

    Implementation note: if the same exempt sets are checked many times (for
    example during a recursive walk), prefer to pass pre-constructed ``set`` /
    ``frozenset`` values so the conversion happens once rather than per call.
    ``iter_targets`` does this internally.
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
    """Return True if ``path`` is a Markdown file a linter should scan.

    Convenience wrapper around :func:`is_target` with the Markdown suffix set.
    Retained for callers that scan only ``.md``.
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
    """Return a deduplicated, ordered list of targets matching ``suffixes``.

    For each entry in ``paths``:
      - if it is a file and matches :func:`is_target`, include it;
      - if it is a directory, walk it recursively and include every file whose
        suffix is in ``suffixes`` and that passes :func:`is_target`.

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
    """Return a deduplicated, ordered list of Markdown targets under ``paths``.

    Convenience wrapper around :func:`iter_targets` with the Markdown suffix
    set. Retained for callers that scan only ``.md``.
    """
    return iter_targets(
        paths,
        suffixes=MARKDOWN_SUFFIXES,
        exempt_dirs=exempt_dirs,
        exempt_files=exempt_files,
    )


def iter_scan_roots_markdown(
    paths: Iterable[str],
    *,
    repo_root: Path,
) -> list[Path]:
    """Sorted, deduplicated ``.md`` files under explicit repo-relative scan roots.

    The allow-list walker shared by the explicit-scan-root content linters: they
    enumerate their scan roots (a corpus-specific domain-directory list plus any
    root meta files) and subtract per-linter exempt files/prefixes at the call
    site, rather than walking the repository root and subtracting an exempt-dir
    set the way :func:`iter_markdown_targets` callers do.

    Each entry is taken relative to ``repo_root``: a ``.md`` FILE entry is
    included as-is; a DIRECTORY entry contributes every ``.md`` beneath it
    recursively. Deliberately NO exempt-directory subtraction happens here (an
    allow-list linter's scan roots ARE its scope) and paths are not resolved, so
    reported paths and ordering match the caller's scan-root spelling.

    ``repo_root`` is required: this helper carries no module-level root default,
    so a caller (including one whose ``--root`` flag rebinds its own root) always
    passes the root explicitly.
    """
    files: set[Path] = set()
    for p in paths:
        path = repo_root / p
        if path.is_file() and path.suffix == ".md":
            files.add(path)
        elif path.is_dir():
            files.update(path.rglob("*.md"))
    return sorted(files)


def read_text_safe(path: Path) -> str | None:
    """Read ``path`` as UTF-8 text; return ``None`` on a decode error.

    Linters that scan a heterogeneous file tree should skip files that are not
    valid UTF-8 (binary files mis-named with ``.md``, lock files, and so on)
    rather than aborting the entire run. The contract is: a successful return is
    a string; ``None`` signals "skip this file".

    Filesystem errors (FileNotFoundError, PermissionError) are not caught: those
    represent a real environmental problem the caller should surface.
    """
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


# The generic metadata field shape shared by corpus documents: ``**Field:**
# value`` with an optional trailing backslash (the hard-line-break marker).
METADATA_FIELD_RE = re.compile(r"^\*\*([^*]+):\*\*\s*(.*?)\s*$")

# How many leading lines of a document constitute the metadata head window. A
# ``**Field:**``-shaped line deeper in the body (for example a documented
# placeholder in a how-to section) is body prose, not metadata.
METADATA_HEAD_LINES = 30


class MetadataBlock:
    """Parsed document-metadata fields from a file's head window.

    Attributes:
        fields: field name to value, with a single trailing backslash (the
            metadata hard-line-break marker) stripped from the value and
            surrounding whitespace trimmed.
        raw_lines: field name to ``(lineno, raw line)`` for callers that need to
            point a finding at the exact source line.

    A field that appears more than once inside the window keeps its FIRST
    occurrence.
    """

    __slots__ = ("fields", "raw_lines")

    def __init__(self) -> None:
        self.fields: dict[str, str] = {}
        self.raw_lines: dict[str, tuple[int, str]] = {}


def parse_metadata_block(text: str, *, head_lines: int = METADATA_HEAD_LINES) -> MetadataBlock:
    """Parse ``**Field:** value`` metadata lines from a file's head window.

    Scans the first ``head_lines`` lines of ``text`` for the corpus metadata
    field shape and returns a :class:`MetadataBlock`. Values have the optional
    trailing backslash (hard-line-break marker) stripped, so
    ``**Date:** 2026-07-01\\`` yields ``"2026-07-01"``.

    The parser is deliberately field-agnostic and TOLERANT at this layer: it
    captures whatever value text follows the field marker (including trailing
    annotations such as ``**Date:** 2026-07-01 (draft)``), and it does not know
    or enforce any required-field list. Which fields are required, and whether a
    captured value is valid, is the CALLER's judgement, so a gate can fail loud
    on a present-but-malformed value instead of silently skipping the file. Use
    a validator such as :func:`parse_iso_date` on the captured value and treat
    ``None``-on-a-present-field as a finding.
    """
    block = MetadataBlock()
    for lineno, line in enumerate(text.splitlines()[:head_lines], start=1):
        match = METADATA_FIELD_RE.match(line)
        if not match:
            continue
        field = match.group(1)
        if field in block.fields:
            continue
        value = match.group(2)
        if value.endswith("\\"):
            value = value[:-1].rstrip()
        block.fields[field] = value
        block.raw_lines[field] = (lineno, line)
    return block


def parse_iso_date(value: str) -> datetime.date | None:
    """Return ``value`` as a date if it is EXACTLY ``YYYY-MM-DD``, else ``None``.

    The whole captured value must be the ISO date: a trailing annotation
    (``2026-07-01 (draft)``) returns ``None`` so the caller can distinguish a
    malformed-but-present field (a finding, under fail-loud semantics) from an
    absent one (a legitimate skip).
    """
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return None
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        return None


def head_version(text: str | None, *, head_lines: int = METADATA_HEAD_LINES) -> str | None:
    """Return the head-window ``Version`` or ``Library Version`` value, or ``None``.

    Reads via :func:`parse_metadata_block`, centralizing the in-scope rule the
    version-window checks share:

    - The ``Version`` field wins, then ``Library Version``; a distinct field
      such as ``README Version`` never matches.
    - An EMPTY value is treated as absent (``None``), so only a non-empty
      version value brings a file into scope.
    - Line-initial fields only (the canonical metadata shape; no leading
      whitespace before ``**Version:**``).
    - Precedence between ``Version`` and ``Library Version`` is by field name,
      not by position in the window.
    """
    if text is None:
        return None
    fields = parse_metadata_block(text, head_lines=head_lines).fields
    value = fields.get("Version") or fields.get("Library Version")
    return value or None


def add_months(d: datetime.date, months: int) -> datetime.date:
    """Return ``d`` advanced by ``months`` calendar months.

    Handles month-end roll-forward: 31 January + 1 month yields 28/29 February.
    Stdlib-only; avoids a dateutil dependency.
    """
    total_month_index = d.month - 1 + months
    new_year = d.year + total_month_index // 12
    new_month = total_month_index % 12 + 1
    # Clamp day to the last day of the new month.
    if new_month == 12:
        next_month_first = datetime.date(new_year + 1, 1, 1)
    else:
        next_month_first = datetime.date(new_year, new_month + 1, 1)
    last_day_of_new_month = (next_month_first.toordinal() - 1)
    last_day_of_new_month_date = datetime.date.fromordinal(last_day_of_new_month)
    new_day = min(d.day, last_day_of_new_month_date.day)
    return datetime.date(new_year, new_month, new_day)


def split_row(line: str) -> list[str]:
    """Return the stripped cells of a Markdown table row (bounding pipes dropped)."""
    parts = line.split("|")
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return [c.strip() for c in parts]


def is_separator_row(cells: list[str]) -> bool:
    """True for a ``|---|---|`` style separator row.

    ``cells`` is a :func:`split_row` result. An EMPTY cell list is not a
    separator (returns False); a caller that wants empty-is-separator semantics
    keeps its own variant.
    """
    return bool(cells) and set("".join(cells)) <= set("-: ")


CODE_SPAN_RE = re.compile(r"(`+)(.+?)\1")

SIMPLE_CODE_SPAN_RE = re.compile(r"`[^`]*`")


def strip_code_spans(line: str) -> str:
    """Return ``line`` with multi-backtick-aware inline code spans removed."""
    return CODE_SPAN_RE.sub("", line)


def is_fence_line(line: str) -> bool:
    """True if ``line`` is a fenced-code-block delimiter.

    A fence is a line whose left-stripped form starts with three backticks
    (``` ``` ```) OR three tildes (``~~~``). Leading whitespace is tolerated
    (CommonMark permits up to a 3-space indent; this is more permissive, which
    does not matter in practice). Both fence characters count so that a stray
    CommonMark-valid ``~~~`` fence cannot silently suppress scanning of
    everything after it.

    This is the SHARED fence predicate for in-code-block skip loops, so a fence
    toggle is recognized consistently. A toggle is a toggle: this predicate does
    not pair fences by character or match fence widths, consistent with
    :func:`iter_non_code_lines`.
    """
    stripped = line.lstrip()
    return stripped.startswith("```") or stripped.startswith("~~~")


def iter_non_code_lines(text: str) -> Iterator[tuple[int, str]]:
    """Yield ``(lineno, line)`` for each line outside a fenced code block.

    ``lineno`` is 1-indexed.

    Fence detection (deliberately simple):

      - A fence is a line whose stripped form starts with three backticks
        (``` ``` ```) OR three tildes (``~~~``). Both fence characters toggle so
        a stray CommonMark-valid ``~~~`` fence cannot silently suppress scanning
        of everything after it.
      - Indentation before the fence is tolerated.
      - Fence parsing is a state toggle: every fence line flips ``in_code``.
        Backtick and tilde fences are tracked with ONE toggle, not paired by
        character (a toggle is a toggle; mixed-character fence pairs are not a
        recognized shape).

    Edge cases:

      - File starts with a fence: the fence line is consumed; lines until the
        next fence are skipped; yielding resumes after the close.
      - Unterminated fence: every line after the unclosed fence is skipped; the
        function does not warn about unbalanced fences.
      - Nested or re-opened fences: each fence line toggles state.

    The function does not attempt to recognize matching fence widths; a toggle
    is a toggle.
    """
    in_code = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if is_fence_line(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        yield lineno, line


def git(*args: str) -> str:
    """Run ``git <args>``; return stdout with only trailing newlines removed.

    Uses ``.rstrip("\\n")`` NOT ``.strip()``: a ``-z`` caller gets NUL-delimited
    output whose paths may begin or end with whitespace, and stripping the whole
    string corrupts the first path's leading whitespace; removing only trailing
    newlines still drops the trailing newline that non-``-z`` callers rely on.
    Raises on non-zero exit.
    """
    return subprocess.check_output(["git", *args], text=True).rstrip("\n")


def git_show(ref: str, path: str) -> str | None:
    """Return file content at ``ref:path`` or ``None`` if the file is absent."""
    try:
        return subprocess.check_output(
            ["git", "show", f"{ref}:{path}"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return None


if __name__ == "__main__":
    import sys

    # This is an importable library module, not a runnable gate. Its unit suite
    # lives in the sibling ``selftest_aiqt_corpus.py`` (the standalone-selftest
    # house pattern), run as ``python3 -I -B tools/selftest_aiqt_corpus.py``.
    print(
        "aiqt_corpus is an importable library module; run its unit suite with "
        "`python3 -I -B tools/selftest_aiqt_corpus.py`.",
        file=sys.stderr,
    )
    raise SystemExit(2)
