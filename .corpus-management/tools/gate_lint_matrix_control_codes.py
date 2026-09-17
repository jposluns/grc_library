#!/usr/bin/env python3
"""Central compliance-matrix framework-control-code validity - pack engine.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(Finding, the header/regex constants, the row helpers split_row / is_separator_row /
tokenize_cell, the per-framework checks check_nist_token / check_ccm_token /
check_aicm_token, and scan_matrix) is the source of record here in the pack, moved
verbatim from the grc gate. The five framework-reference predicates
(is_valid_category, relocation_note, is_ccm_v41, is_aicm_only, check_iso_token) are
supplied by the adopter via configure(ref), so the engine is catalogue-free; the grc
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


def configure(ref) -> None:
    """Populate the five framework-reference predicates from the adopter's catalogue.

    ``ref`` supplies is_valid_category + relocation_note (NIST CSF), is_ccm_v41 +
    is_aicm_only (CSA CCM/AICM), and check_iso_token (ISO 27001 Annex A). The check
    functions and scan_matrix below are verbatim from the original grc gate and
    resolve these as module globals. Call once before scan_matrix().
    """
    global is_valid_category, relocation_note, is_ccm_v41, is_aicm_only, check_iso_token
    is_valid_category = ref.is_valid_category
    relocation_note = ref.relocation_note
    is_ccm_v41 = ref.is_ccm_v41
    is_aicm_only = ref.is_aicm_only
    check_iso_token = ref.check_iso_token


NIST_FUNCTIONS = frozenset({"GV", "ID", "PR", "DE", "RS", "RC"})

ISO_HEADER = "ISO/IEC 27001:2022"
NIST_HEADER = "NIST CSF 2.0"
CCM_HEADER = "CSA CCM v4.1"
AICM_HEADER = "CSA AICM v1.1"

# ISO/IEC 27001:2022 Annex A and clause validation (the structural reference
# data and ``check_iso_token``) lives in ``iso_27001_reference.py``, shared
# with gate 58 (per-document ISO Annex A), mirroring the shared
# ``nist_csf_reference`` module.
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


