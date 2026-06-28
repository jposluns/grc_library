#!/usr/bin/env python3
"""GRC compliance-matrix framework-control-code validity audit.

The GRC Library compliance-alignment matrix
(``compliance/matrix-grc-compliance-alignment.md``) maps each library
document to the control identifiers of nine frameworks. A wrong control
*mapping* (whether a document semantically belongs under a given control)
is a judgement call and stays the author's apply-time responsibility; it is
not mechanically checkable. A wrong control *code* (hallucinated, mistyped,
or drawn from a superseded edition) IS mechanically checkable, and this
gate checks it for the columns whose frameworks expose a closed, well-formed
code set.

Scope (deliberately bounded):

  * **ISO 27001:2022 column** -- every token is validated as either an
    Annex A control code ``A.<theme>.<n>`` with theme in 5-8 and ``<n>``
    within the theme's control count (A.5: 37, A.6: 8, A.7: 14, A.8: 34;
    37+8+14+34 = 93 controls), or a management-system clause ``§<n>`` /
    ``§<n>.<m>`` with the leading clause in 4-10 (clause 4 Context through
    clause 10 Improvement). A token matching neither shape is flagged.
    The Annex A control counts and the clause range are structural facts
    of ISO/IEC 27001:2022, verified against multiple published references.

  * **NIST CSF 2.0 column** -- every token is validated for both
    *well-formedness* and category-level *membership*. Well-formedness:
    the token must be ``FUNCTION.CATEGORY`` with FUNCTION one of the six
    CSF 2.0 Core Functions (GV, ID, PR, DE, RS, RC; the matrix's own
    column key lists these). Membership: the full ``FUNCTION.CATEGORY``
    code must name a real CSF 2.0 Category, validated against the
    authoritative 22-Category set encoded in ``nist_csf_reference.py``
    (transcribed from NIST CSWP 29 Table 1, *The NIST Cybersecurity
    Framework (CSF) 2.0*). A token that is well-formed but names a
    CSF-1.1-era category removed or relocated in 2.0 (``PR.IP``, ``ID.SC``,
    ``ID.BE``, etc.) is flagged with a relocation note pointing at where
    the content went in 2.0.

  * **CSA CCM v4.1 column** -- every token is validated for *catalogue
    membership*: it must be a CSA CCM v4.1.0 control identifier
    (``ccm_aicm_reference.CCM_V41``). A token that is a valid AICM v1.1.0
    identifier but NOT a CCM v4.1.0 one (the AICM-only ``MDS`` domain is the
    canonical case) is flagged: the column is labelled "CSA CCM v4.1", so an
    AICM code does not belong in it even though it is a real CSA control.
    This is a *catalogue-discipline* check (CCM-vs-AICM separation) that the
    corpus-wide CSA citation gate (``lint-ccm-aicm-citations.py``) does not
    enforce here, because that gate validates a matrix code against the
    AICM-wins *union* and so passes an AICM-only code in the CCM column. The
    two gates are complementary: the citation gate checks title accuracy
    against whichever catalogue the context names; this gate enforces that
    the v4.1-labelled column carries only v4.1 codes. Title accuracy of CCM
    codes stays the citation gate's job; this gate does not re-check titles.

  * **CSA AICM v1.1 column** -- the symmetric counterpart of the CCM-column
    check. AICM v1.1 is CSA's AI-focused *extension* of CCM v4.1 (it restates
    the CCM control base and adds AI-specific controls), so this column exists
    to carry only the AI-specific delta: a token must be an AICM-*only*
    identifier (``ccm_aicm_reference.is_aicm_only`` -- in AICM v1.1.0 but not
    CCM v4.1.0; the ``MDS`` Model-Security domain, ``GRC-09..15``, ``AIS-09..15``,
    ``DSP-20..24``, ``HRS-14/15``, ``IAM-16..18``, ``LOG-15/16``, ``TVM-13``).
    A CCM v4.1 base control (which AICM also restates) is flagged: it belongs
    in the "CSA CCM v4.1" column, so that the AICM column adds AI-specific
    signal rather than duplicating the CCM column. ``N/A`` is allowed (most
    non-AI rows). Title accuracy stays the CSA citation gate's job.

Out of scope (by design):

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

from ccm_aicm_reference import is_aicm_only, is_ccm_v41
from lint_common import REPO_ROOT, read_text_safe
from nist_csf_reference import is_valid_category, relocation_note

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
CCM_HEADER = "CSA CCM v4.1"
AICM_HEADER = "CSA AICM v1.1"

ISO_ANNEX_RE = re.compile(r"^A\.(\d+)\.(\d+)$")
ISO_CLAUSE_RE = re.compile(r"^§(\d+)(?:\.\d+)*$")
NIST_RE = re.compile(r"^([A-Z]{2})\.([A-Z]{2,})$")
# A CCM/AICM control-identifier shape: DOMAIN-NN (domain prefix, two-digit
# number). Used only to give a sharper message when a CCM-column token looks
# like a control code but is not a valid CCM v4.1 one.
CCM_CODE_RE = re.compile(r"^[A-Z&]{2,4}-[0-9]{2}$")

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
    """Return ``(rule, message)`` if ``tok`` is not a valid NIST token, else None.

    Three checks in order: well-formedness (FUNCTION.CATEGORY shape), Core
    Function prefix membership, then full-code Category membership against
    the authoritative CSF 2.0 set in ``nist_csf_reference``.
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
    if not is_valid_category(tok):
        note = relocation_note(tok)
        if note:
            return (
                "nist-category",
                f"'{tok}' is not a CSF 2.0 Category ({note})",
            )
        return (
            "nist-category",
            f"'{tok}' is not a CSF 2.0 Category "
            f"(no such FUNCTION.CATEGORY in the CSF 2.0 Core)",
        )
    return None


def check_ccm_token(tok: str) -> tuple[str, str] | None:
    """Return ``(rule, message)`` if ``tok`` is not a valid CCM v4.1 token, else None.

    The column is labelled "CSA CCM v4.1", so a token must be a CCM v4.1.0
    control identifier. An AICM-only identifier (a real CSA control, but from
    the AI Controls Matrix, not CCM v4.1) is the specific confusion this check
    catches; the canonical case is the AICM ``MDS`` (Model Security) domain.
    """
    if tok == "N/A":
        return None
    if is_ccm_v41(tok):
        return None
    if is_aicm_only(tok):
        return (
            "ccm-aicm-confusion",
            f"'{tok}' is an AICM v1.1.0 code, not a CSA CCM v4.1.0 code; it "
            f"does not belong in the 'CSA CCM v4.1' column (CCM/AICM "
            f"catalogue confusion). Use the CCM v4.1 control, or map AICM "
            f"codes in an AICM-labelled surface.",
        )
    if CCM_CODE_RE.match(tok):
        return (
            "ccm-unknown",
            f"'{tok}' is not a valid CSA CCM v4.1.0 control identifier "
            f"(not in the authoritative CCM v4.1.0 catalogue).",
        )
    return (
        "ccm-malformed",
        f"unrecognized CSA CCM v4.1 token '{tok}' "
        f"(expected a control identifier 'DOMAIN-NN' or 'N/A').",
    )


def check_aicm_token(tok: str) -> tuple[str, str] | None:
    """Return ``(rule, message)`` if ``tok`` is not a valid AICM-only token, else None.

    The column is labelled "CSA AICM v1.1" and exists to carry the AI-specific
    controls AICM v1.1.0 adds on top of CCM v4.1.0 (the AICM-only set: AIS-09..15,
    the MDS Model-Security domain, GRC-09..15, DSP-20..24, HRS-14/15, IAM-16..18,
    LOG-15/16, TVM-13). AICM v1.1 is CSA's AI-focused extension of CCM v4.1, so its
    code set restates the CCM base and adds these; a CCM v4.1 base control therefore
    belongs in the "CSA CCM v4.1" column, NOT here. This is the symmetric counterpart
    of ``check_ccm_token``'s AICM-only-in-the-CCM-column check: it keeps the AICM
    column to the AI-specific delta so the column adds signal rather than duplicating
    the CCM column.
    """
    if tok == "N/A":
        return None
    if is_aicm_only(tok):
        return None
    if is_ccm_v41(tok):
        return (
            "aicm-is-ccm-base",
            f"'{tok}' is a CSA CCM v4.1.0 base control, not an AICM-only "
            f"(AI-specific) control; the 'CSA AICM v1.1' column carries only the "
            f"controls AICM v1.1 adds on top of CCM v4.1, so cite '{tok}' in the "
            f"'CSA CCM v4.1' column instead (CCM/AICM catalogue discipline).",
        )
    if CCM_CODE_RE.match(tok):
        return (
            "aicm-unknown",
            f"'{tok}' is not a valid CSA AICM v1.1.0 control identifier "
            f"(not in the authoritative AICM v1.1.0 catalogue).",
        )
    return (
        "aicm-malformed",
        f"unrecognized CSA AICM v1.1 token '{tok}' "
        f"(expected a control identifier 'DOMAIN-NN' or 'N/A').",
    )


def scan_matrix(path: Path) -> list[Finding]:
    """Validate the CSA CCM v4.1, CSA AICM v1.1, ISO and NIST framework columns of the matrix."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[Finding] = []
    iso_idx: int | None = None
    nist_idx: int | None = None
    ccm_idx: int | None = None
    aicm_idx: int | None = None
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not line.lstrip().startswith("|"):
            iso_idx = nist_idx = ccm_idx = aicm_idx = None  # left a table block
            continue
        cells = split_row(line)
        if ISO_HEADER in cells and NIST_HEADER in cells:
            iso_idx = cells.index(ISO_HEADER)
            nist_idx = cells.index(NIST_HEADER)
            ccm_idx = cells.index(CCM_HEADER) if CCM_HEADER in cells else None
            aicm_idx = cells.index(AICM_HEADER) if AICM_HEADER in cells else None
            continue
        if is_separator_row(cells):
            continue
        if iso_idx is None:
            continue  # a table without the framework columns
        if ccm_idx is not None and len(cells) > ccm_idx:
            for tok in tokenize_cell(cells[ccm_idx]):
                result = check_ccm_token(tok)
                if result:
                    findings.append(Finding(lineno, result[0], result[1]))
        if aicm_idx is not None and len(cells) > aicm_idx:
            for tok in tokenize_cell(cells[aicm_idx]):
                result = check_aicm_token(tok)
                if result:
                    findings.append(Finding(lineno, result[0], result[1]))
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
            f"(CSA CCM v4.1 column membership, no AICM-only codes; "
            f"CSA AICM v1.1 column membership, AICM-only codes only, no CCM-base codes; "
            f"ISO 27001:2022 Annex A membership + clause format; "
            f"NIST CSF 2.0 well-formedness + Category membership; "
            f"CCM/AICM title accuracy covered by the CSA citation gate)."
        )
        return 0
    print(f"=== {rel} ===")
    for f in findings:
        print(f"  L{f.line} [{f.rule}] {f.message}")
    print(
        f"\nFAIL: {len(findings)} matrix control-code issue(s). CSA CCM v4.1 "
        f"column tokens are validated for CCM v4.1.0 catalogue membership "
        f"(AICM-only codes rejected); CSA AICM v1.1 column tokens for AICM-only "
        f"(AI-specific) membership (CCM-base codes rejected); ISO codes against "
        f"the ISO/IEC 27001:2022 Annex A control set and clause range; NIST tokens "
        f"against the CSF 2.0 Core Function prefixes and the authoritative 22-Category set.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
