#!/usr/bin/env python3
"""Per-document framework control-code validity check (grc gate): pack-owned engine.

Validate the NIST CSF 2.0 control codes that appear in a document's NIST-labelled
framework tables: every ``FUNCTION.CATEGORY`` code cited in a NIST-CSF table cell
must be a real CSF 2.0 Category; a CSF-1.1-era code is flagged with a relocation
note. The engine handles both table orientations: framework-as-column (a table
whose header names a NIST CSF column) and framework-as-row (a row whose first cell
names NIST CSF, with the codes in the second cell).

Engine/wrapper split (Group-A content-generic lane, Pattern A): this engine carries
the PURE scan (``check_code``, ``codes_in``, ``scan_file``) plus the NIST-CSF
parsing patterns (the label regex and the FUNCTION.CATEGORY token regex). The
framework CATALOGUE is supplied by the caller as two predicates
(``is_valid_category`` and ``relocation_note``), and ``repo_root`` is passed in, so
the engine is repository-root-free and holds no catalogue of its own; the project
wrapper (``tools/lint-document-control-codes.py``) imports the shared NIST CSF
reference, supplies those predicates, and keeps the scan scope
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
        "gate_lint_document_control_codes: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# NIST CSF label: matches "NIST CSF" / "NIST Cybersecurity Framework"
# (optionally "2.0"), but NOT "NIST SP 800-...".
NIST_CSF_LABEL_RE = re.compile(r"\bNIST\s+(?:CSF|Cybersecurity\s+Framework)\b", re.IGNORECASE)

# A NIST CSF code token: FUNCTION.CATEGORY with FUNCTION one of the six CSF
# Functions, optionally a -N subcategory suffix. The function set is embedded in
# the alternation so the regex never matches an ISO "A.5.19" or a NIST SP "SA-9".
NIST_CODE_RE = re.compile(r"\b((?:GV|ID|PR|DE|RS|RC)\.[A-Z]{2})(?:-\d+)?\b")

Finding = namedtuple("Finding", "path line rule message")


def check_code(tok: str, is_valid_category, relocation_note) -> tuple[str, str] | None:
    """Return ``(rule, message)`` if ``tok`` is not a CSF 2.0 Category, else None."""
    if is_valid_category(tok):
        return None
    note = relocation_note(tok)
    if note:
        return (
            "nist-csf1-carrier",
            f"'{tok}' is a CSF-1.1-era code, not a CSF 2.0 Category ({note})",
        )
    return (
        "nist-unknown-category",
        f"'{tok}' is not a CSF 2.0 Category (no such FUNCTION.CATEGORY in the CSF 2.0 Core)",
    )


def codes_in(cell: str) -> list[str]:
    """Return the distinct CSF FUNCTION.CATEGORY codes in ``cell`` (suffix stripped)."""
    found: list[str] = []
    for m in NIST_CODE_RE.finditer(cell):
        code = m.group(1)
        if code not in found:
            found.append(code)
    return found


def scan_file(path: Path, repo_root: Path, is_valid_category, relocation_note) -> list[Finding]:
    """Validate NIST CSF 2.0 codes in the NIST-labelled tables of ``path``."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[Finding] = []
    rel = path.relative_to(repo_root).as_posix() if path.is_relative_to(repo_root) else str(path)

    lines = text.splitlines()
    in_fence = False
    prev_cells: list[str] | None = None  # the previous table row, for header lookahead
    nist_col: int | None = None  # set when the current table is framework-as-column

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if is_fence_line(line):
            in_fence = not in_fence
            prev_cells = None
            nist_col = None
            continue
        if in_fence:
            continue
        if not stripped.startswith("|"):
            prev_cells = None
            nist_col = None
            continue

        cells = split_row(line)

        if is_separator_row(cells):
            if prev_cells is not None and nist_col is None:
                for idx, c in enumerate(prev_cells):
                    if NIST_CSF_LABEL_RE.search(c):
                        nist_col = idx
                        break
            continue

        if nist_col is not None:
            if len(cells) > nist_col and not NIST_CSF_LABEL_RE.search(cells[nist_col]):
                for code in codes_in(cells[nist_col]):
                    result = check_code(code, is_valid_category, relocation_note)
                    if result:
                        findings.append(Finding(rel, lineno, result[0], result[1]))
        elif cells and NIST_CSF_LABEL_RE.search(cells[0]) and len(cells) > 1:
            for code in codes_in(cells[1]):
                result = check_code(code, is_valid_category, relocation_note)
                if result:
                    findings.append(Finding(rel, lineno, result[0], result[1]))

        prev_cells = cells

    return findings
