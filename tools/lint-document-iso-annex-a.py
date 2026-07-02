#!/usr/bin/env python3
"""Per-document ISO/IEC 27001:2022 Annex A control-code validity audit (corpus-wide).

The ISO-column sibling of ``lint-document-control-codes.py`` (gate 54, NIST
CSF 2.0) and the per-document counterpart of ``lint-matrix-control-codes.py``
(gate 49, which validates the central matrix's ISO column). This audit
validates ISO/IEC 27001:2022 Annex A control codes and management-system
clause references wherever they appear in *any* corpus document's
framework-reference or crosswalk tables. The defect class it catches: a cell
that cites a non-existent Annex A control (``A.8.99``), a non-2022 theme
(``A.9.2``, a 2013-edition code), or an out-of-range clause (``§12``).

The structural reference data (Annex A theme counts A.5-A.8 = 37/8/14/34,
clauses §4-§10) and the single-token validator ``check_iso_token`` live in
the shared ``iso_27001_reference`` module, also used by gate 49, so the two
ISO gates cannot drift.

Scope (deliberately bounded, precision-first):

  * **ISO/IEC 27001:2022 only.** Validation is gated on a cell governed by an
    explicit ``ISO/IEC 27001:2022`` (or ``ISO 27001:2022``) label, so the
    2022 Annex A theme/count facts are only applied where the 2022 edition is
    named. A hypothetical ``:2013`` table (different Annex A numbering) is not
    mis-validated; the corpus today is uniformly 2022.

  * **ISO-labelled table cells only.** A token is validated only when it sits
    in a cell governed by an ISO 27001:2022 column header or framework-row
    label, mirroring gate 54's two table modes:

      - *Framework-as-column*: a header row names the ISO column; codes are
        taken from that column in each body row.
      - *Framework-as-row*: a body row whose first cell is the ISO label;
        codes are taken from the *code cell* immediately after the label
        (cell index 1), never a trailing notes cell.

    This table-scoping is the critical precision rule: a bare ``§6`` in
    document prose (almost always the document's OWN section 6, not an ISO
    clause) is never scanned; only a ``§6`` inside an ISO-labelled cell is
    treated as an ISO clause reference.

  * **Token shapes recognized** inside an ISO cell: a single Annex A control
    ``A.<5-8>.<n>``; a **theme-only** reference ``A.5``-``A.8`` (a legitimate
    citation of a whole Annex A theme, accepted as valid); a **range**
    ``A.t.n to A.t.m`` / ``A.t.n to t.m`` / ``A.t.n to m`` (same theme,
    endpoints validated, n <= m); a clause ``§<4-10>``; and comma/semicolon
    separated lists of any of these. Trailing descriptive prose after the
    codes (``A.8.20, A.8.21: Network Controls``) is ignored.

Excludes the central matrix (gate 49's exact target) and the
``dev-security/claude-rules/`` pack subtree, consistent with gate 54.

Scans the audited corpus directories by default; a path argument (used by
the regression harness) overrides the target to a single file.

Exit codes: 0 = clean, 1 = findings, 2 = target unreadable.
"""

from __future__ import annotations

import re
import sys
from collections import namedtuple
from pathlib import Path

from iso_27001_reference import (
    ISO_ANNEX_A_RANGES,
    check_iso_token,
)
from lint_common import (
    AUDITED_DOMAIN_DIRS,
    REPO_ROOT,
    iter_markdown_targets,
    read_text_safe,
)

# The central matrix is gate 49's exact target; exclude it here to avoid
# duplicate coverage. Path is relative to REPO_ROOT, posix form.
MATRIX_REL = "compliance/matrix-grc-compliance-alignment.md"

# The pack subtree holds AI-context artefacts, not governed corpus documents.
PACK_PREFIX = "dev-security/claude-rules/"

# ISO/IEC 27001:2022 label: matches "ISO/IEC 27001:2022" and "ISO 27001:2022".
# The :2022 suffix is required so validation is edition-pinned (precision-first).
ISO_LABEL_RE = re.compile(r"\bISO(?:/IEC)?\s+27001:2022\b")

# Token shapes, applied in priority order within an ISO cell. The range form
# is matched first so its leading "A.t.n" is consumed as part of the range and
# not re-counted as a stand-alone code. Range second endpoint may drop the
# "A." and the theme ("A.8.20 to 21").
RANGE_RE = re.compile(
    r"A\.(\d+)\.(\d+)\s*(?:to|through|-|–|—)\s*(?:A\.)?(?:(\d+)\.)?(\d+)\b"
)
ANNEX_CODE_RE = re.compile(r"A\.(\d+)\.(\d+)")
# Theme-only reference: "A.5" not immediately followed by ".<digit>" (which
# would make it a control code) and not preceded by a digit-dot.
THEME_ONLY_RE = re.compile(r"(?<![\d.])A\.(\d+)(?![.\d])")
CLAUSE_RE = re.compile(r"§(\d+)(?:\.\d+)*")

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


def _check_theme(theme: int, tok: str) -> tuple[str, str] | None:
    """Validate a theme-only reference ``A.<theme>``."""
    if theme not in ISO_ANNEX_A_RANGES:
        return (
            "iso-annex-theme",
            f"ISO 27001:2022 Annex A theme 'A.{theme}' does not exist "
            f"(valid themes: A.5-A.8): '{tok}'",
        )
    return None


def _check_range(m: re.Match) -> tuple[str, str] | None:
    """Validate a range match (groups: t1, n1, t2-or-None, n2)."""
    t1, n1 = int(m.group(1)), int(m.group(2))
    t2 = int(m.group(3)) if m.group(3) is not None else t1
    n2 = int(m.group(4))
    tok = m.group(0)
    # Validate each endpoint as a single Annex A control.
    for theme, num in ((t1, n1), (t2, n2)):
        result = check_iso_token(f"A.{theme}.{num}")
        if result:
            return (result[0], f"in range '{tok}': {result[1]}")
    if t1 != t2:
        return (
            "iso-annex-range",
            f"ISO 27001:2022 Annex A range '{tok}' spans two themes "
            f"(A.{t1} and A.{t2}); a range stays within one theme",
        )
    if n1 > n2:
        return (
            "iso-annex-range",
            f"ISO 27001:2022 Annex A range '{tok}' is inverted (A.{t1}.{n1} > A.{t2}.{n2})",
        )
    return None


def findings_in(cell: str) -> list[tuple[str, str]]:
    """Return ``(rule, message)`` for every invalid ISO token in ``cell``.

    Ranges are matched and consumed first; remaining single codes, theme-only
    references, and clauses are validated on the cell with the range spans
    blanked out so a range endpoint is not re-counted as a bare code.
    """
    out: list[tuple[str, str]] = []
    masked = cell
    for m in RANGE_RE.finditer(cell):
        result = _check_range(m)
        if result:
            out.append(result)
        # Blank the consumed span so the single-code / theme passes skip it.
        masked = masked[: m.start()] + (" " * (m.end() - m.start())) + masked[m.end():]

    for m in ANNEX_CODE_RE.finditer(masked):
        result = check_iso_token(m.group(0))
        if result:
            out.append(result)
    # Blank single codes before the theme-only pass so "A.5" inside "A.5.19"
    # (already counted as a code) is not also read as a theme-only token.
    masked2 = ANNEX_CODE_RE.sub(lambda m: " " * len(m.group(0)), masked)
    for m in THEME_ONLY_RE.finditer(masked2):
        result = _check_theme(int(m.group(1)), m.group(0))
        if result:
            out.append(result)
    for m in CLAUSE_RE.finditer(masked):
        result = check_iso_token(m.group(0))
        if result:
            out.append(result)
    return out


def scan_file(path: Path) -> list[Finding]:
    """Validate ISO 27001:2022 Annex A codes in the ISO-labelled tables of ``path``."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[Finding] = []
    rel = path.relative_to(REPO_ROOT).as_posix() if path.is_relative_to(REPO_ROOT) else str(path)

    lines = text.splitlines()
    in_fence = False
    prev_cells: list[str] | None = None
    iso_col: int | None = None

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
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
            # Framework-as-column: validate the ISO column cell only (skip the
            # header cell, which is the label itself).
            if len(cells) > iso_col and not ISO_LABEL_RE.search(cells[iso_col]):
                for rule, msg in findings_in(cells[iso_col]):
                    findings.append(Finding(rel, lineno, rule, msg))
        elif cells and ISO_LABEL_RE.search(cells[0]) and len(cells) > 1:
            # Framework-as-row: validate the code cell (cell 1) only.
            for rule, msg in findings_in(cells[1]):
                findings.append(Finding(rel, lineno, rule, msg))

        prev_cells = cells

    return findings


def collect_targets(argv: list[str]) -> list[Path]:
    """Resolve the scan targets: a single explicit path, or the audited corpus."""
    if len(argv) > 1:
        return [Path(argv[1]).resolve()]
    roots = [REPO_ROOT / d for d in AUDITED_DOMAIN_DIRS]
    out: list[Path] = []
    for p in iter_markdown_targets(roots):
        rel = p.relative_to(REPO_ROOT).as_posix() if p.is_relative_to(REPO_ROOT) else str(p)
        if rel == MATRIX_REL or rel.startswith(PACK_PREFIX):
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
            f"OK: ISO/IEC 27001:2022 Annex A codes in per-document framework tables are valid "
            f"({scope}; Annex A theme/control ranges and clause range; matrix and pack excluded)."
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
        f"\nFAIL: {len(findings)} per-document ISO 27001:2022 Annex A control-code "
        f"issue(s) across {len(by_file)} file(s). Codes are validated against the "
        f"authoritative 2022 Annex A theme/control ranges (A.5-A.8) and clause range "
        f"(§4-§10); only cells governed by an ISO 27001:2022 label are scanned.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
