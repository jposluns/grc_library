#!/usr/bin/env python3
"""Committed factual identifier registry for the alignment-citation existence gate.

Each entry is an edition-pinned, provenance-stamped catalogue of the control/section
identifiers the held editions of a framework actually define. The existence gate
(`lint-alignment-citation-existence.py`) consumes ONLY this committed registry, never the
held reference repository at run time, so the gate works in a sibling-free clone
(portability requirement, same design as `lint-ssdf-control-ids.py`). A maintainer-only
parity check of these committed sets against the held `grc_library_ref` NIST Privacy Framework
sources is a planned follow-up (P-1.63); it is NOT yet wired into `verify-reference-modules.py`,
whose current coverage is CCM, AICM, CSF, COBIT, and ISO 31000 only. The sets here were extracted
deterministically from the held sources and verified by count (PF 1.0: 18 categories, 100
subcategories; PF 1.1 IPD: 24 categories, 138 subcategories).

Registry contract per entry:
  - framework key + human name + edition
  - status: a DATA attribute recording how fully the edition's identifiers are captured -
            "complete" (every identifier of the edition present), "draft" (a not-yet-final edition,
            e.g. an IPD), or "partial" (a subset). Status does NOT determine blocking: the existence
            check validates a code against the UNION of a framework's held editions regardless of
            per-entry status, and a code absent from ALL held editions is the blocking error.
  - provenance: held-source path + extraction method + expected structural counts
  - the closed identifier set(s)

An identifier is a fabricated-code error only when it is absent from the UNION of a framework's
held editions (so a code valid in any held edition, including a `draft` IPD, passes). Everything
else is advisory or out of scope.
"""
from __future__ import annotations

# --- NIST Privacy Framework 1.0 (CSWP 01162020) ---------------------------------
# Provenance: grc_library_ref/standards/NIST/NIST-Privacy-Framework-1.0--CSWP-01162020--full-text.md
# Extraction: deterministic grep of the Core (Function/Category/Subcategory) identifiers.
# Structural invariants: 5 Functions, 18 Categories, 100 Subcategories (verified).
PF10_CATEGORIES = {
    "CM.AW-P", "CM.PO-P", "CT.DM-P", "CT.DP-P", "CT.PO-P", "GV.AT-P",
    "GV.MT-P", "GV.PO-P", "GV.RM-P", "ID.BE-P", "ID.DE-P", "ID.IM-P",
    "ID.RA-P", "PR.AC-P", "PR.DS-P", "PR.MA-P", "PR.PO-P", "PR.PT-P",
}
PF10_SUBCATEGORIES = {
    "CM.AW-P1", "CM.AW-P2", "CM.AW-P3", "CM.AW-P4", "CM.AW-P5", "CM.AW-P6",
    "CM.AW-P7", "CM.AW-P8", "CM.PO-P1", "CM.PO-P2", "CT.DM-P1", "CT.DM-P2",
    "CT.DM-P3", "CT.DM-P4", "CT.DM-P5", "CT.DM-P6", "CT.DM-P7", "CT.DM-P8",
    "CT.DM-P9", "CT.DM-P10", "CT.DP-P1", "CT.DP-P2", "CT.DP-P3", "CT.DP-P4",
    "CT.DP-P5", "CT.PO-P1", "CT.PO-P2", "CT.PO-P3", "CT.PO-P4", "GV.AT-P1",
    "GV.AT-P2", "GV.AT-P3", "GV.AT-P4", "GV.MT-P1", "GV.MT-P2", "GV.MT-P3",
    "GV.MT-P4", "GV.MT-P5", "GV.MT-P6", "GV.MT-P7", "GV.PO-P1", "GV.PO-P2",
    "GV.PO-P3", "GV.PO-P4", "GV.PO-P5", "GV.PO-P6", "GV.RM-P1", "GV.RM-P2",
    "GV.RM-P3", "ID.BE-P1", "ID.BE-P2", "ID.BE-P3", "ID.DE-P1", "ID.DE-P2",
    "ID.DE-P3", "ID.DE-P4", "ID.DE-P5", "ID.IM-P1", "ID.IM-P2", "ID.IM-P3",
    "ID.IM-P4", "ID.IM-P5", "ID.IM-P6", "ID.IM-P7", "ID.IM-P8", "ID.RA-P1",
    "ID.RA-P2", "ID.RA-P3", "ID.RA-P4", "ID.RA-P5", "PR.AC-P1", "PR.AC-P2",
    "PR.AC-P3", "PR.AC-P4", "PR.AC-P5", "PR.AC-P6", "PR.DS-P1", "PR.DS-P2",
    "PR.DS-P3", "PR.DS-P4", "PR.DS-P5", "PR.DS-P6", "PR.DS-P7", "PR.DS-P8",
    "PR.MA-P1", "PR.MA-P2", "PR.PO-P1", "PR.PO-P2", "PR.PO-P3", "PR.PO-P4",
    "PR.PO-P5", "PR.PO-P6", "PR.PO-P7", "PR.PO-P8", "PR.PO-P9", "PR.PO-P10",
    "PR.PT-P1", "PR.PT-P2", "PR.PT-P3", "PR.PT-P4",
}

PF10 = {
    "name": "NIST Privacy Framework",
    "edition": "1.0",
    "status": "complete",
    "provenance": "grc_library_ref/standards/NIST/NIST-Privacy-Framework-1.0--CSWP-01162020--full-text.md",
    "counts": {"categories": 18, "subcategories": 100},
    "categories": PF10_CATEGORIES,
    "subcategories": PF10_SUBCATEGORIES,
    # The whole valid set (category-level and subcategory-level are both citable).
    "all": PF10_CATEGORIES | PF10_SUBCATEGORIES,
    # Token grammar: XX.YY-P optionally suffixed by a subcategory number.
    "id_regex": r"\b[A-Z]{2}\.[A-Z]{2}-P[0-9]*\b",
}

# --- NIST Privacy Framework 1.1 (CSWP 40, Initial Public Draft) -------------------
# Provenance: grc_library_ref/standards/NIST/NIST-Privacy-Framework-1.1--CSWP-40-ipd-draft--full-text.md
# Extraction: deterministic grep of the draft Core identifiers. status="draft" (an IPD, not final),
# held so the existence check validates against the UNION of held editions and does not false-flag a
# 1.1-only code (e.g. the new GV.RR-P GOVERN structure) as fabricated. Counts: 24 categories, 138 subcategories.
PF11_CATEGORIES = {
    "CM.AW-P", "CM.PO-P", "CT.DM-P", "CT.DP-P", "CT.PO-P", "GV.AT-P",
    "GV.DE-P", "GV.MT-P", "GV.OV-P", "GV.PO-P", "GV.RM-P", "GV.RR-P",
    "ID.BE-P", "ID.DE-P", "ID.IM-P", "ID.RA-P", "PR.AA-P", "PR.AC-P",
    "PR.DS-P", "PR.IR-P", "PR.MA-P", "PR.PO-P", "PR.PS-P", "PR.PT-P",
}
PF11_SUBCATEGORIES = {
    "CM.AW-P1", "CM.AW-P2", "CM.AW-P3", "CM.AW-P4", "CM.AW-P5", "CM.AW-P6",
    "CM.AW-P7", "CM.AW-P8", "CM.PO-P1", "CM.PO-P2", "CT.DM-P1", "CT.DM-P2",
    "CT.DM-P3", "CT.DM-P4", "CT.DM-P5", "CT.DM-P6", "CT.DM-P7", "CT.DM-P8",
    "CT.DM-P9", "CT.DM-P10", "CT.DM-P11", "CT.DP-P1", "CT.DP-P2", "CT.DP-P3",
    "CT.DP-P4", "CT.DP-P5", "CT.PO-P1", "CT.PO-P2", "CT.PO-P3", "CT.PO-P4",
    "GV.AT-P1", "GV.AT-P2", "GV.AT-P3", "GV.AT-P4", "GV.DE-P1", "GV.DE-P2",
    "GV.DE-P3", "GV.DE-P4", "GV.DE-P5", "GV.MT-P1", "GV.MT-P2", "GV.MT-P3",
    "GV.MT-P4", "GV.MT-P5", "GV.MT-P6", "GV.MT-P7", "GV.OV-P1", "GV.OV-P2",
    "GV.OV-P3", "GV.PO-P1", "GV.PO-P2", "GV.PO-P3", "GV.PO-P4", "GV.PO-P5",
    "GV.PO-P6", "GV.PO-P7", "GV.RM-P1", "GV.RM-P2", "GV.RM-P3", "GV.RM-P4",
    "GV.RM-P5", "GV.RM-P6", "GV.RM-P7", "GV.RR-P1", "GV.RR-P2", "GV.RR-P3",
    "GV.RR-P4", "ID.BE-P1", "ID.BE-P2", "ID.BE-P3", "ID.BE-P4", "ID.BE-P5",
    "ID.BE-P6", "ID.DE-P1", "ID.DE-P2", "ID.DE-P3", "ID.DE-P4", "ID.DE-P5",
    "ID.IM-P1", "ID.IM-P2", "ID.IM-P3", "ID.IM-P4", "ID.IM-P5", "ID.IM-P6",
    "ID.IM-P7", "ID.IM-P8", "ID.RA-P1", "ID.RA-P2", "ID.RA-P3", "ID.RA-P4",
    "ID.RA-P5", "ID.RA-P6", "PR.AA-P1", "PR.AA-P2", "PR.AA-P3", "PR.AA-P4",
    "PR.AA-P5", "PR.AA-P6", "PR.AC-P1", "PR.AC-P2", "PR.AC-P3", "PR.AC-P4",
    "PR.AC-P5", "PR.AC-P6", "PR.DS-P1", "PR.DS-P2", "PR.DS-P3", "PR.DS-P4",
    "PR.DS-P5", "PR.DS-P6", "PR.DS-P7", "PR.DS-P8", "PR.DS-P9", "PR.DS-P10",
    "PR.IR-P1", "PR.IR-P2", "PR.IR-P3", "PR.IR-P4", "PR.MA-P1", "PR.MA-P2",
    "PR.PO-P1", "PR.PO-P2", "PR.PO-P3", "PR.PO-P4", "PR.PO-P5", "PR.PO-P6",
    "PR.PO-P7", "PR.PO-P8", "PR.PO-P9", "PR.PO-P10", "PR.PS-P1", "PR.PS-P2",
    "PR.PS-P3", "PR.PS-P4", "PR.PT-P1", "PR.PT-P2", "PR.PT-P3", "PR.PT-P4",
}

PF11 = {
    "name": "NIST Privacy Framework",
    "edition": "1.1-ipd",
    "status": "draft",
    "provenance": "grc_library_ref/standards/NIST/NIST-Privacy-Framework-1.1--CSWP-40-ipd-draft--full-text.md",
    "counts": {"categories": 24, "subcategories": 138},
    "categories": PF11_CATEGORIES,
    "subcategories": PF11_SUBCATEGORIES,
    "all": PF11_CATEGORIES | PF11_SUBCATEGORIES,
    "id_regex": r"\b[A-Z]{2}\.[A-Z]{2}-P[0-9]*\b",
}

# The UNION of every held Privacy Framework edition. The existence check validates a PF-family code
# against this union: a code present in ANY held edition is valid; only a code absent from ALL of them
# (e.g. CT.PO-P5, absent from both 1.0 and the 1.1 IPD) is a fabricated-code error. This makes the gate
# edition-robust rather than pinned to a single edition (which would false-flag a legitimate 1.1 cite).
PF_ALL_EDITIONS_VALID = PF10["all"] | PF11["all"]

# Registry index (extended one edition at a time, each after a completeness review).
REGISTRY = {
    "nist-privacy-framework-1.0": PF10,
    "nist-privacy-framework-1.1-ipd": PF11,
}
