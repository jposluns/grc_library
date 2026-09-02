#!/usr/bin/env python3
"""Committed factual identifier registry for the alignment-citation existence gate.

Each entry is an edition-pinned, provenance-stamped catalogue of the control/section
identifiers a named framework edition actually defines. The existence gate
(`lint-alignment-citation-existence.py`) consumes ONLY this committed registry, never the
held reference repository at run time, so the gate works in a sibling-free clone
(portability requirement, same design as `lint-ssdf-control-ids.py`). A maintainer-only
parity check of these committed sets against the held `grc_library_ref` PF 1.0 source is a
planned follow-up (P-1.63); it is NOT yet wired into `verify-reference-modules.py`, whose
current coverage is CCM, AICM, CSF, COBIT, and ISO 31000 only. The sets here were extracted
deterministically from the held source and verified by count (18 categories, 100 subcategories).

Registry contract per entry:
  - framework key + human name + edition
  - status: "complete" (every identifier of the edition is present -> a miss is BLOCKING)
            or "partial" (advisory only, never blocking)
  - provenance: held-source path + extraction method + expected structural counts
  - the closed identifier set(s)

Only an unknown identifier attributed to a COMPLETE, edition-matched catalogue is a
fabricated-code error. Everything else is advisory or out of scope.
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

# Registry index (extended one edition at a time, each after a completeness review).
REGISTRY = {
    "nist-privacy-framework-1.0": PF10,
}
