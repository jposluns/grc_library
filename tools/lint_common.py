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
  inline: ``.git``, ``node_modules``, ``__pycache__``, ``.claude``,
  ``.working``. Linters that need additional exempt directories pass
  them via the ``exempt_dirs`` argument.
- ``iter_markdown_targets`` and ``is_markdown_target`` deliberately
  accept ``Iterable[str]`` for ``exempt_files`` so callers can pass a
  ``set``, ``frozenset``, or ``list`` interchangeably.
- ``iter_non_code_lines`` yields ``(lineno, line)`` skipping any line
  inside a fenced code block (lines bounded by lines beginning with
  ``` ``` ```). The fence-start and fence-end lines are also skipped.
"""

from __future__ import annotations

import datetime
import re
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
    {
        ".git",
        "node_modules",
        "__pycache__",
        ".claude",
        ".working",
        # In-repo sibling-repo placeholders (TODO section 1.19.3): stub dirs that
        # stand in for the grc_library_ref / grc_library_scratch / grc_library_private
        # siblings when they are absent (an adopter clone). Each holds only a README
        # stub; the dedicated stub-guard gate (lint-sibling-placeholders.py) enforces
        # that, so the content gates exempt them here.
        ".ref",
        ".scratch",
        ".private",
    }
)


# Canonical list of audited-not-exempt top-level directories: the
# eleven domain directories plus ``.project-governance``. This is the
# single source of truth for the "explicit allow-list" content linters
# (the ones that enumerate scan roots rather than walking the
# repository root and subtracting ``DEFAULT_EXEMPT_DIRS``). Each such
# linter splats ``AUDITED_DOMAIN_DIRS`` into its scan-root list rather
# than hardcoding the directory run inline, so that adding a future
# top-level audited directory propagates to every content linter from
# one place. The directory-scan-scope parity gate
# (``tools/lint-scan-scope-parity.py``) enforces that no content
# linter hardcodes this run; the governance contract is in
# ``governance/specification-project-governance-separation.md`` section 7.4.
#
# ``docs`` is deliberately NOT in this set: it holds generated
# artefacts (``docs/portal.md``, ``docs/maturity-scorecard.md``) and is
# a per-linter extra that only the date/version-currency linters add,
# not a corpus domain. Each linter keeps its own meta-file entries
# (``README.md``, ``NOTICE.md``, the root specifications, etc.) and any
# extra directories alongside the splatted ``AUDITED_DOMAIN_DIRS``.
#
# The ordering matches the historical scan-root ordering across the
# linters (``.project-governance`` after ``governance``), so the
# refactor that introduces the splat is a no-op on the resulting file
# list.
AUDITED_DOMAIN_DIRS: tuple[str, ...] = (
    "ai",
    "architecture",
    "compliance",
    "dev-security",
    "governance",
    ".project-governance",
    "operations",
    "privacy",
    "resilience",
    "risk",
    "security",
    "supply-chain",
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


class MetadataBlock:
    """Parsed document-metadata fields from a file's head window.

    Attributes:
        fields: field name to value, with a single trailing backslash
            (the metadata hard-line-break marker) stripped from the
            value and surrounding whitespace trimmed.
        raw_lines: field name to ``(lineno, raw line)`` for callers
            that need to point a finding at the exact source line.

    A field that appears more than once inside the window keeps its
    FIRST occurrence (matching the first-match semantics of the
    per-linter parsers this helper replaces).
    """

    __slots__ = ("fields", "raw_lines")

    def __init__(self) -> None:
        self.fields: dict[str, str] = {}
        self.raw_lines: dict[str, tuple[int, str]] = {}


# The generic metadata field shape shared by every corpus document:
# ``**Field:** value`` with an optional trailing backslash. This is the
# same pattern lint-metadata.py and build-taxonomy.py use; centralized
# here so parsers stop drifting apart (guardrail review GR-3).
METADATA_FIELD_RE = re.compile(r"^\*\*([^*]+):\*\*\s*(.*?)\s*$")

# How many leading lines of a document constitute the metadata head
# window. Matches the long-standing window in the version-bump and
# co-bump gates; a ``**Field:**``-shaped line deeper in the body (for
# example a documented placeholder in a how-to section) is body prose,
# not metadata.
METADATA_HEAD_LINES = 30


def parse_metadata_block(text: str, *, head_lines: int = METADATA_HEAD_LINES) -> MetadataBlock:
    """Parse ``**Field:** value`` metadata lines from a file's head window.

    Scans the first ``head_lines`` lines of ``text`` for the corpus
    metadata-field shape and returns a :class:`MetadataBlock`. Values
    have the optional trailing backslash (hard-line-break marker)
    stripped, so ``**Date:** 2026-07-01\\`` yields ``"2026-07-01"``.

    The parser is deliberately TOLERANT at this layer: it captures
    whatever value text follows the field marker (including trailing
    annotations such as ``**Date:** 2026-07-01 (draft)``). Per-field
    validity is the CALLER's judgement, so a gate can fail loud on a
    present-but-malformed value instead of silently skipping the file
    (the gate-31 silent fail-open this helper was introduced to close);
    use a validator such as :func:`parse_iso_date` on the captured
    value and treat ``None``-on-present-field as a finding.
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

    The whole captured value must be the ISO date: a trailing
    annotation (``2026-07-01 (draft)``) returns ``None`` so the caller
    can distinguish a malformed-but-present field (a finding, under
    fail-loud semantics) from an absent one (a legitimate skip).
    """
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return None
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        return None


def head_version(text: str | None, *, head_lines: int = METADATA_HEAD_LINES) -> str | None:
    """Return the head-window ``Version`` or ``Library Version`` value, or ``None``.

    The Version-window trio's shared extraction (GR-3 wave 2: gate 40
    plus the D2 and D4 delta checks retired their identical private
    regex for this helper). Reads via :func:`parse_metadata_block`, so
    the corpus in-scope rule the trio shares is centralized here:

    - The ``Version`` field wins, then ``Library Version`` (the README's
      CalVer line); ``README Version`` is a DISTINCT field and never
      matches, exactly as the retired private regex behaved.
    - An EMPTY value is treated as absent (``None``), preserving the
      trio's scope rule that only a non-empty version value brings a
      file into scope.
    - Line-initial fields only: the retired regex tolerated leading
      whitespace before ``**Version:**``; this helper narrows to the
      canonical line-initial shape (the documented wave-2 narrowing;
      no corpus file carries an indented metadata field).
    - Three further edge-case divergences from the retired regex, each
      confirmed corpus-neutral at migration time (zero live instances):
      a no-separator value (``**Version:**1.0``) now parses (the old
      regex required whitespace before the value); precedence between
      ``Version`` and ``Library Version`` is by field name rather than
      by position in the window; and an empty first ``Version`` line no
      longer falls through to a later non-empty ``Version`` line in the
      same window.
    """
    if text is None:
        return None
    fields = parse_metadata_block(text, head_lines=head_lines).fields
    value = fields.get("Version") or fields.get("Library Version")
    return value or None


def is_fence_line(line: str) -> bool:
    """True if ``line`` is a fenced-code-block delimiter.

    A fence is a line whose left-stripped form starts with three backticks
    (``` ``` ```) OR three tildes (``~~~``). Leading whitespace is tolerated
    (CommonMark permits up to a 3-space indent; this is more permissive, which
    does not matter for the current corpus). Both fence characters count so that
    a stray CommonMark-valid ``~~~`` fence cannot silently suppress scanning of
    everything after it (the GR-4 tilde-blindness class).

    This is the SHARED fence predicate the corpus linters use for their
    in-code-block skip loops, so a fence toggle is recognized consistently
    across gates. It replaces the per-linter private ``startswith("```")``
    checks, six of which were tilde-blind before the r5 GR-4 consolidation
    (TODO 3.10). A toggle is a toggle: this predicate does not pair fences by
    character or match fence widths, consistent with :func:`iter_non_code_lines`.
    """
    stripped = line.lstrip()
    return stripped.startswith("```") or stripped.startswith("~~~")


def iter_non_code_lines(text: str) -> Iterator[tuple[int, str]]:
    """Yield ``(lineno, line)`` for each line outside a fenced code block.

    ``lineno`` is 1-indexed.

    Fence detection (deliberately simple):

      - A fence is a line whose stripped form starts with three
        backticks (``` ``` ```) OR three tildes (``~~~``). The library
        convention is backtick fences and no document currently uses
        tilde fences, but a stray CommonMark-valid ``~~~`` fence would
        otherwise silently suppress scanning of everything after it,
        so both fence characters toggle (added with the guardrail
        review's GR-4).
      - Indentation before the fence is tolerated (``line.strip()``
        is used). Per CommonMark, fences are valid up to a 3-space
        indent; this function is more permissive but the difference
        does not matter for the current corpus.
      - Fence parsing is a state toggle per fence character: every
        fence line flips ``in_code``. A line containing ``\\`\\`\\``
        inside an inline code block on its own (which is unusual but
        possible) would erroneously toggle the state. The linters that
        use this helper do not encounter this in practice. Backtick
        and tilde fences are tracked with ONE toggle, not paired by
        character (a toggle is a toggle; mixed-character fence pairs
        are not a corpus shape).

    Edge cases:

      - File starts with a fence: the fence line is consumed; lines
        until the next fence are skipped; yielding resumes after the
        close.
      - Unterminated fence: every line after the unclosed fence is
        skipped. The function does not warn about unbalanced fences.
      - Nested or re-opened fences: each fence line toggles state, so
        ``` ``` ... ``` ... ``` ... ``` ``` ``` toggles include/exclude
        in pairs.

    The function does not attempt to recognize matching fence widths
    (CommonMark requires the closing fence to be at least as wide as
    the opening fence); a toggle is a toggle.
    """
    in_code = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if is_fence_line(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        yield lineno, line


# ---------------------------------------------------------------------------
# Cross-file section-reference shared constants (gates 62 and 65).
#
# The two cross-file reference linters (lint-cross-file-section-refs.py,
# the numbers phase, and lint-cross-file-section-names.py, the names
# phase) share these extraction constants. They were duplicated
# copy-with-comment until the 2026-07-04 guardrail-review G-4 hoist;
# this single definition is now the source of truth for both, so a
# sentinel or window change cannot drift between the phases.

# Cross-file section references: a section-number citation in prose.
CROSS_REF_PATTERNS = [
    re.compile(r"§\s?(\d+(?:\.\d+){0,3})"),
    re.compile(r"\bSection\s+(\d+(?:\.\d+){0,3})\b"),
]

# A markdown link to another .md file (the reference's binding target).
CROSS_MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")

# The explicit binding sentence: section numbers on the line cite the
# named external standard, not a corpus document.
CROSS_BINDING_SENTINEL = "Section numbers below refer to that standard."

# A line naming an external standard: its section numbers cite that
# standard, not a corpus document.
CROSS_EXTERNAL_CONTEXT_RE = re.compile(
    r"\b(?:ISO(?:/IEC)?|IEC|NIST|OWASP|GDPR|BASC|CSA|CCM|AICM|COBIT|CTPAT|PIP|"
    r"HIPAA|PIPEDA|DORA|MiCA|SOX|Clause|Article|Annex|SP\s?800|SP\s?600|CSF|SSDF|ASVS)\b"
)

# Maximum distance (characters) between a reference and its naming link
# for the adjacent-link class.
CROSS_ADJACENCY_WINDOW = 40
