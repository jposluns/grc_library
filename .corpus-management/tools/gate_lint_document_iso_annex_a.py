#!/usr/bin/env python3
"""Per-document ISO/IEC 27001:2022 Annex A validity check (grc gate): pack-owned engine.

Validate ISO/IEC 27001:2022 Annex A control codes cited in a document's
ISO-labelled framework tables: theme-only references (``A.<theme>``), single
controls (``A.<theme>.<num>``), ranges (``A.8.20 to 21``), and ``§`` clauses are
each validated against the authoritative Annex A structure; an out-of-range,
non-existent, wrong-theme, or inverted-range code is flagged. Both table
orientations are handled (framework-as-column and framework-as-row).

Engine/wrapper split (Group-A content-generic lane, Pattern A): this engine carries
the PURE scan (``_check_theme``, ``_check_range``, ``findings_in``, ``scan_file``)
plus the ISO parsing patterns. The Annex A reference is supplied by the caller as a
predicate (``check_iso_token``) and the theme set (``iso_annex_a_ranges``), and
``repo_root`` is passed in, so the engine is repository-root-free and holds no
reference data; the project wrapper (``tools/lint-document-iso-annex-a.py``) imports
the shared ISO reference, supplies those, and keeps the scan scope
(``collect_targets``) and reporting.

Exit codes (the wrapper returns these): 0 clean; 1 findings; 2 explicit target not found.
"""

from __future__ import annotations

import re
from collections import namedtuple
from pathlib import Path

try:
    from aiqt_corpus import is_fence_line, is_separator_row, read_text_safe, split_row
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_document_iso_annex_a: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# ISO/IEC 27001:2022 label: matches "ISO/IEC 27001:2022" and "ISO 27001:2022".
ISO_LABEL_RE = re.compile(r"\bISO(?:/IEC)?\s+27001:2022\b")

# Token shapes, applied in priority order within an ISO cell. The range form is
# matched first so its leading "A.t.n" is consumed as part of the range.
RANGE_RE = re.compile(
    r"A\.(\d+)\.(\d+)\s*(?:to|through|-|\u2013|\u2014)\s*(?:A\.)?(?:(\d+)\.)?(\d+)\b"
)
ANNEX_CODE_RE = re.compile(r"A\.(\d+)\.(\d+)")
THEME_ONLY_RE = re.compile(r"(?<![\d.])A\.(\d+)(?![.\d])")
CLAUSE_RE = re.compile(r"§(\d+)(?:\.\d+)*")

Finding = namedtuple("Finding", "path line rule message")


def _check_theme(theme: int, tok: str, iso_annex_a_ranges) -> tuple[str, str] | None:
    """Validate a theme-only reference ``A.<theme>``."""
    if theme not in iso_annex_a_ranges:
        return (
            "iso-annex-theme",
            f"ISO/IEC 27001:2022 Annex A theme 'A.{theme}' does not exist "
            f"(valid themes: A.5-A.8): '{tok}'",
        )
    return None


def _check_range(m: re.Match, check_iso_token) -> tuple[str, str] | None:
    """Validate a range match (groups: t1, n1, t2-or-None, n2)."""
    t1, n1 = int(m.group(1)), int(m.group(2))
    t2 = int(m.group(3)) if m.group(3) is not None else t1
    n2 = int(m.group(4))
    tok = m.group(0)
    for theme, num in ((t1, n1), (t2, n2)):
        result = check_iso_token(f"A.{theme}.{num}")
        if result:
            return (result[0], f"in range '{tok}': {result[1]}")
    if t1 != t2:
        return (
            "iso-annex-range",
            f"ISO/IEC 27001:2022 Annex A range '{tok}' spans two themes "
            f"(A.{t1} and A.{t2}); a range stays within one theme",
        )
    if n1 > n2:
        return (
            "iso-annex-range",
            f"ISO/IEC 27001:2022 Annex A range '{tok}' is inverted (A.{t1}.{n1} > A.{t2}.{n2})",
        )
    return None


def findings_in(cell: str, check_iso_token, iso_annex_a_ranges) -> list[tuple[str, str]]:
    """Return ``(rule, message)`` for every invalid ISO token in ``cell``."""
    out: list[tuple[str, str]] = []
    masked = cell
    for m in RANGE_RE.finditer(cell):
        result = _check_range(m, check_iso_token)
        if result:
            out.append(result)
        masked = masked[: m.start()] + (" " * (m.end() - m.start())) + masked[m.end():]

    for m in ANNEX_CODE_RE.finditer(masked):
        result = check_iso_token(m.group(0))
        if result:
            out.append(result)
    masked2 = ANNEX_CODE_RE.sub(lambda m: " " * len(m.group(0)), masked)
    for m in THEME_ONLY_RE.finditer(masked2):
        result = _check_theme(int(m.group(1)), m.group(0), iso_annex_a_ranges)
        if result:
            out.append(result)
    for m in CLAUSE_RE.finditer(masked):
        result = check_iso_token(m.group(0))
        if result:
            out.append(result)
    return out


def scan_file(path: Path, repo_root: Path, check_iso_token, iso_annex_a_ranges) -> list[Finding]:
    """Validate ISO/IEC 27001:2022 Annex A codes in the ISO-labelled tables of ``path``."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[Finding] = []
    rel = path.relative_to(repo_root).as_posix() if path.is_relative_to(repo_root) else str(path)

    lines = text.splitlines()
    in_fence = False
    prev_cells: list[str] | None = None
    iso_col: int | None = None

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if is_fence_line(line):
            in_fence = not in_fence
            prev_cells = None
            iso_col = None
            continue
        if in_fence:
            continue
        if not stripped.startswith("|"):
            prev_cells = None
            iso_col = None
            continue

        cells = split_row(line)

        if is_separator_row(cells):
            if prev_cells is not None and iso_col is None:
                for idx, c in enumerate(prev_cells):
                    if ISO_LABEL_RE.search(c):
                        iso_col = idx
                        break
            continue

        if iso_col is not None:
            if len(cells) > iso_col and not ISO_LABEL_RE.search(cells[iso_col]):
                for rule, msg in findings_in(cells[iso_col], check_iso_token, iso_annex_a_ranges):
                    findings.append(Finding(rel, lineno, rule, msg))
        elif cells and ISO_LABEL_RE.search(cells[0]) and len(cells) > 1:
            for rule, msg in findings_in(cells[1], check_iso_token, iso_annex_a_ranges):
                findings.append(Finding(rel, lineno, rule, msg))

        prev_cells = cells

    return findings
