#!/usr/bin/env python3
"""Per-document NIST CSF 2.0 control-code validity audit (corpus-wide).

This is the corpus-wide sibling of ``lint-matrix-control-codes.py`` (gate
49). Gate 49 validates the NIST CSF 2.0 column of the *central* compliance
matrix (``compliance/matrix-grc-compliance-alignment.md``); this audit
validates NIST CSF 2.0 codes wherever they appear in *any* corpus
document's framework-reference or crosswalk tables. The defect class it
catches is the same one gate 49 catches in the matrix, but corpus-wide: a
NIST CSF table cell that cites a CSF-1.1-era category code (``PR.IP``,
``ID.SC``, ``RS.RP``, ``DE.DP``, ``RC.IM``, etc.) that was removed or
relocated in CSF 2.0. The authoritative 22-Category CSF 2.0 set and the
CSF-1.1 relocation map both live in ``nist_csf_reference.py`` (transcribed
from NIST CSWP 29 Table 1), shared with gate 49.

Scope (deliberately bounded, precision-first):

  * **NIST CSF 2.0 only.** ISO/IEC 27001:2022 Annex A codes that appear in
    per-document tables are NOT validated here (the matrix's ISO column is
    covered by gate 49; per-document ISO codes appear as clause refs and
    ranges that are far more false-positive-prone, and are a separate
    follow-up). This audit validates exactly the framework whose stale
    codes are the documented DD-12 defect class.

  * **NIST-labelled table cells only.** A code is validated only when it
    sits in a cell governed by a NIST CSF column header or NIST CSF
    framework-row label. Two table shapes are recognised:

      - *Framework-as-column*: a header row (the row immediately before a
        ``|---|`` separator) has a cell matching the NIST CSF label; the
        codes are taken from that column in each body row.
      - *Framework-as-row*: a body row whose first cell matches the NIST
        CSF label; the codes are taken from the *code cell* immediately
        after the label (cell index 1), NOT from any trailing notes cell.

    Restricting framework-as-row extraction to the code cell is the
    precision rule that avoids flagging a CSF-1.1 code that legitimately
    appears in a *notes* cell as part of a rename note (e.g. "PR.AC was the
    CSF 1.1 subcategory; CSF 2.0 renamed it to PR.AA"). The trade-off: a
    code embedded only in a notes cell is not validated. That is an
    accepted precision boundary (the documented mapping convention puts
    codes in the code cell).

  * The NIST CSF label regex matches ``NIST CSF`` and ``NIST Cybersecurity
    Framework`` (with or without a ``2.0`` suffix). It deliberately does
    NOT match ``NIST SP 800-...`` rows, whose control families (``SA-9``,
    ``AC-2``, ``SR``) are a different, non-CSF code set.

Codes are validated at the **category** level. A subcategory suffix
(``DE.CM-7``, ``RS.RP-1``) is stripped to its ``FUNCTION.CATEGORY`` and the
category is validated; the reference module carries the 22 Categories, not
the Subcategory text. A token is flagged when its ``FUNCTION.CATEGORY`` is
not a CSF 2.0 Category: with a CSF-1.1 relocation note when the code is a
known 1.1-era category, or as an unknown category otherwise. Well-formed
codes with a non-CSF function prefix cannot occur (the token regex requires
one of the six CSF Functions).

Excludes the central matrix (gate 49's exact target) to avoid duplicate
coverage, and the ``dev-security/claude-rules/`` pack subtree (AI-context
artefacts, not governed corpus documents, consistent with the other
content linters).

Scans the audited corpus directories by default; a path argument (used by
the regression harness) overrides the target to a single file.

Exit codes: 0 = clean, 1 = findings, 2 = target unreadable.
"""

from __future__ import annotations

import re
import sys
from collections import namedtuple
from pathlib import Path

from lint_common import (
    AUDITED_DOMAIN_DIRS,
    REPO_ROOT,
    iter_markdown_targets,
    read_text_safe,
)
from nist_csf_reference import is_valid_category, relocation_note

# The central matrix is gate 49's exact target; exclude it here to avoid
# duplicate coverage. Path is relative to REPO_ROOT, posix form.
MATRIX_REL = "compliance/matrix-grc-compliance-alignment.md"

# The pack subtree holds AI-context artefacts (SKILL.md, rule files), not
# governed corpus documents; the other content linters exempt it too.
PACK_PREFIX = "dev-security/claude-rules/"

# NIST CSF label: matches "NIST CSF" / "NIST Cybersecurity Framework"
# (optionally "2.0"), but NOT "NIST SP 800-...".
NIST_CSF_LABEL_RE = re.compile(r"\bNIST\s+(?:CSF|Cybersecurity\s+Framework)\b", re.IGNORECASE)

# A NIST CSF code token: FUNCTION.CATEGORY with FUNCTION one of the six
# CSF Functions, optionally a -N subcategory suffix. The function set is
# embedded in the alternation so the regex never matches an ISO "A.5.19"
# (single leading letter) or a NIST SP "SA-9" (no dot) token.
NIST_CODE_RE = re.compile(r"\b((?:GV|ID|PR|DE|RS|RC)\.[A-Z]{2})(?:-\d+)?\b")

Finding = namedtuple("Finding", "path line rule message")


def split_row(line: str) -> list[str]:
    """Return the stripped cells of a markdown table row (bounding pipes dropped)."""
    parts = line.split("|")
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return [c.strip() for c in parts]


def is_separator_row(cells: list[str]) -> bool:
    """True for a ``|---|---|`` style separator row (or an empty pipe line)."""
    return bool(cells) and set("".join(cells)) <= set("-: ")


def check_code(tok: str) -> tuple[str, str] | None:
    """Return ``(rule, message)`` if ``tok`` (FUNCTION.CATEGORY) is not a CSF 2.0
    Category, else ``None``."""
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
    """Return the distinct CSF FUNCTION.CATEGORY codes in ``cell`` (suffix stripped),
    in first-appearance order."""
    found: list[str] = []
    for m in NIST_CODE_RE.finditer(cell):
        code = m.group(1)
        if code not in found:
            found.append(code)
    return found


def scan_file(path: Path) -> list[Finding]:
    """Validate NIST CSF 2.0 codes in the NIST-labelled tables of ``path``."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[Finding] = []
    rel = path.relative_to(REPO_ROOT).as_posix() if path.is_relative_to(REPO_ROOT) else str(path)

    lines = text.splitlines()
    in_fence = False
    prev_cells: list[str] | None = None  # the previous table row, for header lookahead
    nist_col: int | None = None  # set when the current table is framework-as-column

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            prev_cells = None
            nist_col = None
            continue
        if in_fence:
            continue
        if not stripped.startswith("|"):
            # Left a table block; reset table state.
            prev_cells = None
            nist_col = None
            continue

        cells = split_row(line)

        if is_separator_row(cells):
            # The row before a separator is the header. If it names a NIST
            # CSF column, switch this table into framework-as-column mode.
            if prev_cells is not None and nist_col is None:
                for idx, c in enumerate(prev_cells):
                    if NIST_CSF_LABEL_RE.search(c):
                        nist_col = idx
                        break
            continue

        # A non-separator table row.
        if nist_col is not None:
            # Framework-as-column: validate the NIST column cell only.
            if len(cells) > nist_col and not NIST_CSF_LABEL_RE.search(cells[nist_col]):
                for code in codes_in(cells[nist_col]):
                    result = check_code(code)
                    if result:
                        findings.append(Finding(rel, lineno, result[0], result[1]))
        elif cells and NIST_CSF_LABEL_RE.search(cells[0]) and len(cells) > 1:
            # Framework-as-row: validate the code cell (cell 1) only, never
            # the trailing notes cell(s).
            for code in codes_in(cells[1]):
                result = check_code(code)
                if result:
                    findings.append(Finding(rel, lineno, result[0], result[1]))

        prev_cells = cells

    return findings


def collect_targets(argv: list[str]) -> list[Path]:
    """Resolve the scan targets: a single explicit path, or the audited corpus."""
    if len(argv) > 1:
        return [Path(argv[1]).resolve()]
    roots = [REPO_ROOT / d for d in AUDITED_DOMAIN_DIRS]
    targets = iter_markdown_targets(roots)
    out: list[Path] = []
    for p in targets:
        rel = p.relative_to(REPO_ROOT).as_posix() if p.is_relative_to(REPO_ROOT) else str(p)
        if rel == MATRIX_REL:
            continue
        if rel.startswith(PACK_PREFIX):
            continue
        out.append(p)
    return out


def main(argv: list[str]) -> int:
    explicit = len(argv) > 1
    targets = collect_targets(argv)
    if explicit and not targets[0].is_file():
        print(f"ERROR: target not found: {targets[0]}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    for path in targets:
        findings.extend(scan_file(path))

    if not findings:
        scope = targets[0].name if explicit else f"{len(targets)} corpus document(s)"
        print(
            f"OK: NIST CSF 2.0 codes in per-document framework tables are valid "
            f"({scope}; CSF 2.0 Category membership; matrix and pack excluded)."
        )
        return 0

    by_file: dict[str, list[Finding]] = {}
    for f in findings:
        by_file.setdefault(f.path, []).append(f)
    for rel in sorted(by_file):
        print(f"=== {rel} ===")
        for f in by_file[rel]:
            print(f"  L{f.line} [{f.rule}] {f.message}")
    print(
        f"\nFAIL: {len(findings)} per-document NIST CSF 2.0 control-code issue(s) "
        f"across {len(by_file)} file(s). Codes are validated at the Category level "
        f"against the authoritative CSF 2.0 22-Category set; CSF-1.1-era codes are "
        f"flagged with a relocation note.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
