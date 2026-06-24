#!/usr/bin/env python3
"""GRC compliance-matrix framework-control-code validity audit.

The GRC Library compliance-alignment matrix
(``compliance/matrix-grc-compliance-alignment.md``) maps each library
document to the control identifiers of eight frameworks. A wrong control
*mapping* (whether a document semantically belongs under a given control)
is a judgement call and stays the author's apply-time responsibility; it is
not mechanically checkable. A wrong control *code* (hallucinated, mistyped,
or drawn from a superseded edition) IS mechanically checkable, and this
gate checks it for the columns whose frameworks expose a closed, well-formed
code set.

Scope (deliberately bounded; see TODO ``4.6a``):

  * **ISO 27001:2022 column** -- every token is validated as either an
    Annex A control code ``A.<theme>.<n>`` with theme in 5-8 and ``<n>``
    within the theme's control count (A.5: 37, A.6: 8, A.7: 14, A.8: 34;
    37+8+14+34 = 93 controls), or a management-system clause ``§<n>`` /
    ``§<n>.<m>`` with the leading clause in 4-10 (clause 4 Context through
    clause 10 Improvement). A token matching neither shape is flagged.
    The Annex A control counts and the clause range are structural facts
    of ISO/IEC 27001:2022, verified against multiple published references.

  * **NIST CSF 2.0 column** -- every token is validated for
    *well-formedness* only: it must be ``FUNCTION.CATEGORY`` with FUNCTION
    one of the six CSF 2.0 Core Functions (GV, ID, PR, DE, RS, RC; the
    matrix's own column key lists these). Category-level *membership*
    (whether ``GV.OC`` etc. is a real CSF 2.0 category) is NOT validated
    here: the authoritative CSF 2.0 category set is not yet encoded in the
    repository, so validating membership would require either an
    unverified hand-encoded set (forbidden) or an authoritative source not
    currently reachable. Membership validation is deferred to a follow-up
    once the CSF 2.0 category set is sourced (TODO ``4.6a``); that
    follow-up will also catch the known CSF-1.1-era residue in this column
    (``PR.IP``, ``ID.SC``, ``ID.BE``), which is format-valid and therefore
    passes the well-formedness check.

Out of scope (by design):

  * **CSA CCM v4.1 column** -- already validated corpus-wide (including
    this matrix) by ``lint-ccm-aicm-citations.py`` (the CSA citation gate),
    which uses the authoritative ``ccm_aicm_reference.py`` index. This gate
    does not re-validate CCM codes; doing so would duplicate that gate.

  * **CTPAT / PIP / BASC v6 / WCO SAFE / AEO/AEO-S columns** -- these
    frameworks express their requirements as free-text headings and
    requirement-area labels ("Risk management", "Business partner
    requirements", "Pillar II (Customs-to-Business)"), not as a closed
    code set. There is no published code catalogue to validate them
    against, so they are not policed here.

The gate is a presence/format backstop (gate-discipline: it enforces code
*validity*, not mapping correctness). It reduces, but does not remove, the
un-gated mapping risk; the apply-time author-every-cell discipline stands.

Checks ``compliance/matrix-grc-compliance-alignment.md`` by default; a path
argument (used by the regression harness) overrides the target.

Exit codes: 0 = clean, 1 = findings, 2 = target unreadable.
"""

from __future__ import annotations

import re
import sys
from collections import namedtuple
from pathlib import Path

from lint_common import REPO_ROOT, read_text_safe

MATRIX_REL = "compliance/matrix-grc-compliance-alignment.md"
MATRIX_PATH = REPO_ROOT / MATRIX_REL

# ISO/IEC 27001:2022 Annex A control counts per theme (A.5 Organizational,
# A.6 People, A.7 Physical, A.8 Technological); 37+8+14+34 = 93 controls.
ISO_ANNEX_A_RANGES = {5: 37, 6: 8, 7: 14, 8: 34}
# ISO/IEC 27001:2022 management-system clauses: 4 (Context) through
# 10 (Improvement).
ISO_CLAUSE_MIN, ISO_CLAUSE_MAX = 4, 10

# NIST CSF 2.0 Core Function prefixes (the matrix column key lists these six).
NIST_FUNCTIONS = frozenset({"GV", "ID", "PR", "DE", "RS", "RC"})

ISO_HEADER = "ISO 27001:2022"
NIST_HEADER = "NIST CSF 2.0"

ISO_ANNEX_RE = re.compile(r"^A\.(\d+)\.(\d+)$")
ISO_CLAUSE_RE = re.compile(r"^§(\d+)(?:\.\d+)*$")
NIST_RE = re.compile(r"^([A-Z]{2})\.([A-Z]{2,})$")

Finding = namedtuple("Finding", "line rule message")


def split_row(line: str) -> list[str]:
    """Return the stripped cells of a markdown table row.

    A row ``| a | b | c |`` yields ``['a', 'b', 'c']`` (the empty strings
    produced by the bounding pipes are dropped).
    """
    parts = line.split("|")
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return [c.strip() for c in parts]


def is_separator_row(cells: list[str]) -> bool:
    """True for a ``|---|---|`` style separator row (or an empty pipe line)."""
    return set("".join(cells)) <= set("-: ")


def tokenize_cell(cell: str) -> list[str]:
    """Split a code cell into individual tokens on commas and semicolons."""
    return [t.strip() for t in re.split(r"[,;]", cell) if t.strip()]


def check_iso_token(tok: str) -> tuple[str, str] | None:
    """Return ``(rule, message)`` if ``tok`` is not a valid ISO token, else None."""
    if tok == "N/A":
        return None
    m = ISO_ANNEX_RE.match(tok)
    if m:
        theme, num = int(m.group(1)), int(m.group(2))
        if theme not in ISO_ANNEX_A_RANGES:
            return (
                "iso-annex-theme",
                f"ISO 27001:2022 Annex A theme 'A.{theme}' does not exist "
                f"(valid themes: A.5-A.8): '{tok}'",
            )
        if not 1 <= num <= ISO_ANNEX_A_RANGES[theme]:
            return (
                "iso-annex-range",
                f"ISO 27001:2022 Annex A control '{tok}' out of range "
                f"(A.{theme}.1-A.{theme}.{ISO_ANNEX_A_RANGES[theme]})",
            )
        return None
    m = ISO_CLAUSE_RE.match(tok)
    if m:
        clause = int(m.group(1))
        if not ISO_CLAUSE_MIN <= clause <= ISO_CLAUSE_MAX:
            return (
                "iso-clause-range",
                f"ISO 27001:2022 clause '{tok}' out of range "
                f"(§{ISO_CLAUSE_MIN}-§{ISO_CLAUSE_MAX})",
            )
        return None
    return (
        "iso-malformed",
        f"unrecognized ISO 27001:2022 token '{tok}' "
        f"(expected an Annex A code 'A.5-A.8.N' or a clause '§4-§10')",
    )


def check_nist_token(tok: str) -> tuple[str, str] | None:
    """Return ``(rule, message)`` if ``tok`` is not a well-formed NIST token, else None.

    Well-formedness only: FUNCTION.CATEGORY with FUNCTION a CSF 2.0 Core
    Function. Category membership is intentionally not validated (deferred).
    """
    if tok == "N/A":
        return None
    m = NIST_RE.match(tok)
    if not m:
        return (
            "nist-malformed",
            f"malformed NIST CSF 2.0 token '{tok}' "
            f"(expected FUNCTION.CATEGORY, e.g. GV.OC)",
        )
    func = m.group(1)
    if func not in NIST_FUNCTIONS:
        return (
            "nist-function",
            f"invalid NIST CSF 2.0 Core Function prefix in '{tok}' "
            f"(valid: GV, ID, PR, DE, RS, RC)",
        )
    return None


def scan_matrix(path: Path) -> list[Finding]:
    """Validate the ISO and NIST framework columns of the matrix file."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[Finding] = []
    iso_idx: int | None = None
    nist_idx: int | None = None
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not line.lstrip().startswith("|"):
            iso_idx = nist_idx = None  # left a table block
            continue
        cells = split_row(line)
        if ISO_HEADER in cells and NIST_HEADER in cells:
            iso_idx = cells.index(ISO_HEADER)
            nist_idx = cells.index(NIST_HEADER)
            continue
        if is_separator_row(cells):
            continue
        if iso_idx is None:
            continue  # a table without the framework columns
        if len(cells) > iso_idx:
            for tok in tokenize_cell(cells[iso_idx]):
                result = check_iso_token(tok)
                if result:
                    findings.append(Finding(lineno, result[0], result[1]))
        if nist_idx is not None and len(cells) > nist_idx:
            for tok in tokenize_cell(cells[nist_idx]):
                result = check_nist_token(tok)
                if result:
                    findings.append(Finding(lineno, result[0], result[1]))
    return findings


def main(argv: list[str]) -> int:
    target = Path(argv[1]).resolve() if len(argv) > 1 else MATRIX_PATH
    if not target.is_file():
        print(f"ERROR: target not found: {target}", file=sys.stderr)
        return 2
    findings = scan_matrix(target)
    rel = target.relative_to(REPO_ROOT).as_posix() if target.is_relative_to(REPO_ROOT) else str(target)
    if not findings:
        print(
            f"OK: matrix framework-control codes valid in {rel} "
            f"(ISO 27001:2022 Annex A membership + clause format; "
            f"NIST CSF 2.0 well-formedness; CCM/AICM covered by the CSA citation gate)."
        )
        return 0
    print(f"=== {rel} ===")
    for f in findings:
        print(f"  L{f.line} [{f.rule}] {f.message}")
    print(
        f"\nFAIL: {len(findings)} matrix control-code issue(s). ISO codes are "
        f"validated against the ISO/IEC 27001:2022 Annex A control set and "
        f"clause range; NIST tokens against the CSF 2.0 Core Function prefixes.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
