#!/usr/bin/env python3
"""Central compliance-matrix framework-control-code validity - pack engine.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(Finding, the header/regex constants, the row helpers split_row / is_separator_row /
tokenize_cell, the per-framework checks check_nist_token / check_ccm_token /
check_aicm_token / check_tsc_token, and scan_matrix) is the source of record here in the
pack; it was moved from the grc gate and has since been extended (backlog 3.57: the
optional AICPA TSC 2017 column and a row-width check). The five framework-reference predicates
(is_valid_category, relocation_note, is_ccm_v41, is_aicm_only, check_iso_token), and the
two OPTIONAL AICPA Trust Services Criteria predicates (is_valid_tsc_criterion,
is_tsc_group_heading), are supplied by the adopter via configure(ref), so the engine is
catalogue-free; a matrix carrying the TSC column while the TSC predicates are not
supplied is a finding (fail closed), never an unchecked column. The grc
wrapper (tools/lint-matrix-control-codes.py) imports the shared reference modules,
configures the engine, and keeps the matrix scan scope (MATRIX_PATH), a module-global
scan_matrix(path) shim, lint_target, main, and the exit codes.
"""

from __future__ import annotations

import re
from collections import namedtuple
from pathlib import Path

try:
    from aiqt_corpus import read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_matrix_control_codes: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# --- Framework-reference predicates: populated by configure(ref). ---
# Placeholders until an adopter calls configure(); the grc wrapper does so at import.
is_valid_category = None
relocation_note = None
is_ccm_v41 = None
is_aicm_only = None
check_iso_token = None
is_valid_tsc_criterion = None  # optional (AICPA TSC 2017 column)
is_tsc_group_heading = None    # optional


def configure(ref) -> None:
    """Populate the framework-reference predicates from the adopter's catalogue.

    ``ref`` supplies is_valid_category + relocation_note (NIST CSF), is_ccm_v41 +
    is_aicm_only (CSA CCM/AICM), and check_iso_token (ISO 27001 Annex A). It MAY also
    supply is_valid_tsc_criterion + is_tsc_group_heading (AICPA 2017 Trust Services
    Criteria); an adopter that omits them leaves the TSC column unconfigured, and
    scan_matrix reports a table carrying that column as a finding rather than skipping
    it. The check functions and scan_matrix below resolve these as module globals.
    Call once before scan_matrix().
    """
    global is_valid_category, relocation_note, is_ccm_v41, is_aicm_only, check_iso_token
    global is_valid_tsc_criterion, is_tsc_group_heading
    is_valid_category = ref.is_valid_category
    relocation_note = ref.relocation_note
    is_ccm_v41 = ref.is_ccm_v41
    is_aicm_only = ref.is_aicm_only
    check_iso_token = ref.check_iso_token
    is_valid_tsc_criterion = getattr(ref, "is_valid_tsc_criterion", None)
    is_tsc_group_heading = getattr(ref, "is_tsc_group_heading", None)


NIST_FUNCTIONS = frozenset({"GV", "ID", "PR", "DE", "RS", "RC"})

ISO_HEADER = "ISO/IEC 27001:2022"
NIST_HEADER = "NIST CSF 2.0"
CCM_HEADER = "CSA CCM v4.1"
AICM_HEADER = "CSA AICM v1.1"
TSC_HEADER = "AICPA TSC 2017"

# ISO/IEC 27001:2022 Annex A and clause validation (the structural reference
# data and ``check_iso_token``) lives in ``iso_27001_reference.py``, shared
# with gate 58 (per-document ISO Annex A), mirroring the shared
# ``nist_csf_reference`` module.
NIST_RE = re.compile(r"^([A-Z]{2})\.([A-Z]{2,})$")
# A CCM/AICM control-identifier shape: DOMAIN-NN (domain prefix, two-digit
# number). Used only to give a sharper message when a CCM-column token looks
# like a control code but is not a valid CCM v4.1 one.
CCM_CODE_RE = re.compile(r"^[A-Z&]{2,4}-[0-9]{2}$")
# An AICPA Trust Services Criteria identifier shape: a category prefix (CC common
# criteria, A availability, C confidentiality, PI processing integrity, P privacy), a
# series number, a dot, a criterion number. Used only to give a sharper message when a
# TSC-column token looks like a criterion but is not in the closed criterion set.
TSC_CODE_RE = re.compile(r"^(?:CC|PI|A|C|P)[0-9]{1,2}\.[0-9]{1,2}$")

Finding = namedtuple("Finding", "line rule message")

def split_row(line: str) -> list[str]:
    """Return the stripped cells of a markdown table row.

    A row ``| a | b | c |`` yields ``['a', 'b', 'c']`` (the empty strings
    produced by the bounding pipes are dropped). Every pipe delimits (as in the shared
    lint_common.split_row); a table that needs a literal pipe in a cell writes it as an
    HTML entity. Text after the final pipe is kept as a trailing cell so the row-width
    check sees it.
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


def check_tsc_token(tok: str) -> tuple[str, str] | None:
    """Return ``(rule, message)`` if ``tok`` is not a valid AICPA TSC 2017 token, else None.

    The column is labelled "AICPA TSC 2017" (the 2017 Trust Services Criteria, TSP
    Section 100; the 2022 revision changed the points of focus, not the criterion
    identifiers), so a token must be a criterion identifier in the adopter's closed
    criterion set, or N/A. Criterion level only: a privacy group heading (P1.0 to P8.0)
    names a group of criteria and is flagged so the row cites the criterion itself; a
    criterion-shaped token outside the set (CC10.1, P9.1, CC6.9) is unknown; anything
    else (a category name, a bare series such as CC6, a lower-case identifier, a range)
    is malformed.
    """
    if tok == "N/A":
        return None
    if is_valid_tsc_criterion(tok):
        return None
    if is_tsc_group_heading is not None and is_tsc_group_heading(tok):
        return (
            "tsc-heading",
            f"'{tok}' is a Trust Services Criteria group heading, not a criterion; "
            f"cite the criterion identifier itself (for example P1.1).",
        )
    if TSC_CODE_RE.match(tok):
        return (
            "tsc-unknown",
            f"'{tok}' is not a 2017 Trust Services Criteria criterion identifier "
            f"(not in the closed criterion set).",
        )
    return (
        "tsc-malformed",
        f"unrecognized AICPA TSC 2017 token '{tok}' (expected a criterion identifier "
        f"such as 'CC6.1', 'A1.2', 'C1.1', 'PI1.3' or 'P4.1', or 'N/A').",
    )


def _tsc_cell_findings(lineno: int, cells: list[str], tsc_idx: int) -> list[Finding]:
    """Findings for one data row's AICPA TSC 2017 cell.

    Unlike the older columns, a short row or an empty cell is a finding, not a silent
    skip: the column is populated by scripted apply, whose failure shapes are exactly a
    row that was not extended or an empty cell. 'N/A' stands alone in its cell.
    """
    if len(cells) <= tsc_idx:
        return [Finding(lineno, "tsc-cell-missing",
                        f"row has no cell under the '{TSC_HEADER}' column "
                        f"(use 'N/A' for no direct mapping).")]
    toks = tokenize_cell(cells[tsc_idx])
    if not toks:
        return [Finding(lineno, "tsc-cell-empty",
                        f"the '{TSC_HEADER}' cell is empty (use 'N/A' for no direct mapping).")]
    out: list[Finding] = []
    if "N/A" in toks and len(toks) > 1:
        out.append(Finding(lineno, "tsc-na-mixed",
                           f"the '{TSC_HEADER}' cell mixes 'N/A' with criterion "
                           f"identifiers; cite the criteria, or 'N/A' alone."))
    for tok in toks:
        result = check_tsc_token(tok)
        if result:
            out.append(Finding(lineno, result[0], result[1]))
    return out


def _tsc_header_findings(lineno: int, cells: list[str]) -> list[Finding]:
    """Findings for a framework header row's Trust Services Criteria cells.

    A duplicated TSC header would leave the second column unvalidated; refuse it. The
    column is recognized by its exact label only: an adopter that must be sure a matrix
    carries the column pins its exact header set (the grc wrapper does so for the
    canonical matrix), since no wording heuristic can separate a reworded TSC label from
    an unrelated column without false positives.
    """
    out: list[Finding] = []
    if cells.count(TSC_HEADER) > 1:
        out.append(Finding(
            lineno, "tsc-header-duplicate",
            f"the header carries '{TSC_HEADER}' more than once; only the first column "
            f"would be validated.",
        ))
    return out


def scan_matrix(path: Path) -> list[Finding]:
    """Validate the CSA CCM v4.1, CSA AICM v1.1, ISO, NIST and AICPA TSC 2017 framework columns of the matrix."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[Finding] = []
    iso_idx: int | None = None
    nist_idx: int | None = None
    ccm_idx: int | None = None
    aicm_idx: int | None = None
    tsc_idx: int | None = None
    width: int | None = None        # cell count of the current framework table's header
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not line.lstrip().startswith("|"):
            iso_idx = nist_idx = ccm_idx = aicm_idx = tsc_idx = width = None  # left a table block
            continue
        cells = split_row(line)
        if ISO_HEADER in cells and NIST_HEADER in cells:
            iso_idx = cells.index(ISO_HEADER)
            nist_idx = cells.index(NIST_HEADER)
            ccm_idx = cells.index(CCM_HEADER) if CCM_HEADER in cells else None
            aicm_idx = cells.index(AICM_HEADER) if AICM_HEADER in cells else None
            tsc_idx = cells.index(TSC_HEADER) if TSC_HEADER in cells else None
            width = len(cells)
            findings.extend(_tsc_header_findings(lineno, cells))
            if tsc_idx is not None and is_valid_tsc_criterion is None:
                findings.append(Finding(
                    lineno, "tsc-unconfigured",
                    f"the table carries an '{TSC_HEADER}' column but no Trust Services "
                    f"Criteria catalogue is configured (configure(ref) supplied no "
                    f"is_valid_tsc_criterion); the column cannot be validated.",
                ))
                tsc_idx = None  # reported once per table; nothing to validate against
            continue
        if is_separator_row(cells):
            continue
        if iso_idx is None:
            continue  # a table without the framework columns
        if width is not None and len(cells) != width:
            findings.append(Finding(
                lineno, "row-width",
                f"row has {len(cells)} cells but its header has {width}; a surplus, missing, "
                f"or shifted cell (a pipe inside a cell, or text after the final "
                f"pipe) moves values out of their framework columns.",
            ))
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
        if tsc_idx is not None:
            findings.extend(_tsc_cell_findings(lineno, cells, tsc_idx))
    return findings


