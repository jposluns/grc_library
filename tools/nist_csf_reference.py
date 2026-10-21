"""NIST Cybersecurity Framework 2.0 Category and Subcategory reference.

A citation index of the CSF 2.0 Core's Function, Category and Subcategory
identifiers, imported by four modules: ``lint-matrix-control-codes.py`` (gate
49, the central matrix's CSF column), ``lint-document-control-codes.py`` (gate
54, the corpus-wide per-document CSF codes), ``audit-matrix-semantic-fit.py``
(the matrix semantic-fit pre-filter) and ``verify-reference-modules.py`` (the
reference-module parity aid). Sharing it means the two gates cannot drift
apart. It validates that each cited ``FUNCTION.CATEGORY`` token names a real
CSF 2.0 Category, not a CSF 1.1 category removed or moved in 2.0, and that a
cited ``FUNCTION.CATEGORY-NN`` Subcategory is live in CSF 2.0, not withdrawn.

Provenance: the Function and Category identifiers and names are transcribed
from Table 1 of NIST CSWP 29, *The NIST Cybersecurity Framework (CSF) 2.0*
(2024), the authoritative Core. NIST publications are US-government work and
are not subject to copyright; this module is a plain index of the Category and
Subcategory identifiers (it carries none of the framework's Subcategory text or
implementation guidance). The source PDF was supplied by the maintainer and
read with ``pypdf``; the 22 Category codes here were extracted directly from
that text and cross-checked against the six Function names.

Subcategory provenance: ``CSF_SUBCATEGORIES`` and ``CSF_WITHDRAWN_SUBCATEGORIES``
were generated from the OSCAL catalogue held in the reference base at
``standards/NIST/oscal/NIST_CSF_v2.0_catalog.json`` (metadata title
"Electronic Version of NIST Cybersecurity Framework 2.0", version 1.2.0, OSCAL
v1.2.2, last-modified 2026-05-11T16:01:09.00000-00:00, sha256
87d31e856ab2d2b5fb78d66233cc257a2e1a6c3c51b367ab73c10124b25adc3b) by a short
one-off script and pasted here as literals, so no JSON is read when a gate runs.
The rule: a ``subcategory`` control with no ``status`` prop is live; one whose
``status`` prop is ``withdrawn`` is withdrawn, and its note is built from its
``incorporated_into`` / ``moved_to`` links. Only Subcategories under a live
Category are listed; a withdrawn Category (a CSF 1.1 code) is already reported
by the Category check, so its Subcategories never reach the Subcategory check.
CSWP 29 is not the Subcategory source because the held full-text extract yields
only 95 of the 106 live IDs under a token scan (its PDF layout loses some, for
example DE.AE-02 and ID.RA-01) and records no withdrawn IDs or where they went.
``verify-reference-modules.py`` checks these literals against the OSCAL file in
both directions, rebuilding each withdrawal note from the links.

The 22 Categories across the six Functions (6 + 3 + 5 + 2 + 4 + 2 = 22):
"""

from __future__ import annotations

CSF_VERSION = "2.0"

# Function code -> Function name.
CSF_FUNCTIONS: dict[str, str] = {
    "GV": "Govern",
    "ID": "Identify",
    "PR": "Protect",
    "DE": "Detect",
    "RS": "Respond",
    "RC": "Recover",
}

# Category code (FUNCTION.CATEGORY) -> Category name, per CSF 2.0 Table 1.
CSF_CATEGORIES: dict[str, str] = {
    # Govern
    "GV.OC": "Organizational Context",
    "GV.RM": "Risk Management Strategy",
    "GV.RR": "Roles, Responsibilities, and Authorities",
    "GV.PO": "Policy",
    "GV.OV": "Oversight",
    "GV.SC": "Cybersecurity Supply Chain Risk Management",
    # Identify
    "ID.AM": "Asset Management",
    "ID.RA": "Risk Assessment",
    "ID.IM": "Improvement",
    # Protect
    "PR.AA": "Identity Management, Authentication, and Access Control",
    "PR.AT": "Awareness and Training",
    "PR.DS": "Data Security",
    "PR.PS": "Platform Security",
    "PR.IR": "Technology Infrastructure Resilience",
    # Detect
    "DE.CM": "Continuous Monitoring",
    "DE.AE": "Adverse Event Analysis",
    # Respond
    "RS.MA": "Incident Management",
    "RS.AN": "Incident Analysis",
    "RS.CO": "Incident Response Reporting and Communication",
    "RS.MI": "Incident Mitigation",
    # Recover
    "RC.RP": "Incident Recovery Plan Execution",
    "RC.CO": "Incident Recovery Communication",
}

# Common CSF 1.1 categories removed or relocated in CSF 2.0, mapped to a
# short note on where the content went. Used to give a more helpful diagnostic
# than "unknown category" when the matrix cites a 1.1-era code.
CSF_1_1_RELOCATED: dict[str, str] = {
    "ID.BE": "CSF 1.1 'Business Environment'; folded into GV.OC in 2.0",
    "ID.GV": "CSF 1.1 'Governance'; became the GV (Govern) Function in 2.0",
    "ID.SC": "CSF 1.1 'Supply Chain Risk Management'; became GV.SC in 2.0",
    "PR.IP": "CSF 1.1 'Information Protection Processes and Procedures'; "
    "redistributed in 2.0 (mainly PR.PS / PR.DS / ID.AM)",
    "PR.AC": "CSF 1.1 'Identity Management and Access Control'; became PR.AA in 2.0",
    "PR.MA": "CSF 1.1 'Maintenance'; redistributed in 2.0 (mainly PR.PS)",
    "PR.PT": "CSF 1.1 'Protective Technology'; redistributed in 2.0",
    "DE.DP": "CSF 1.1 'Detection Processes'; redistributed in 2.0",
    "RS.RP": "CSF 1.1 'Response Planning'; redistributed in 2.0 (mainly RS.MA)",
    "RS.IM": "CSF 1.1 'Improvements'; became ID.IM in 2.0",
    "RC.IM": "CSF 1.1 'Improvements'; became ID.IM in 2.0",
    # OSCAL: {"id":"ID.RM","class":"category","title":"Risk Management Strategy",
    # ...{"name":"status","value":"withdrawn"}],"links":[{"href":"GV.RM",
    # "rel":"incorporated_into"}]
    "ID.RM": "CSF 1.1 'Risk Management Strategy'; withdrawn, incorporated into GV.RM in 2.0",
}

# The 106 live CSF 2.0 Subcategory IDs (FUNCTION.CATEGORY-NN), grouped by
# Category, generated from the held OSCAL catalogue (see the module docstring).
CSF_SUBCATEGORIES: frozenset[str] = frozenset({
    # GV.OC
    "GV.OC-01", "GV.OC-02", "GV.OC-03", "GV.OC-04", "GV.OC-05",
    # GV.OV
    "GV.OV-01", "GV.OV-02", "GV.OV-03",
    # GV.PO
    "GV.PO-01", "GV.PO-02",
    # GV.RM
    "GV.RM-01", "GV.RM-02", "GV.RM-03", "GV.RM-04", "GV.RM-05", "GV.RM-06", "GV.RM-07",
    # GV.RR
    "GV.RR-01", "GV.RR-02", "GV.RR-03", "GV.RR-04",
    # GV.SC
    "GV.SC-01", "GV.SC-02", "GV.SC-03", "GV.SC-04", "GV.SC-05", "GV.SC-06", "GV.SC-07",
    "GV.SC-08", "GV.SC-09", "GV.SC-10",
    # ID.AM
    "ID.AM-01", "ID.AM-02", "ID.AM-03", "ID.AM-04", "ID.AM-05", "ID.AM-07", "ID.AM-08",
    # ID.IM
    "ID.IM-01", "ID.IM-02", "ID.IM-03", "ID.IM-04",
    # ID.RA
    "ID.RA-01", "ID.RA-02", "ID.RA-03", "ID.RA-04", "ID.RA-05", "ID.RA-06", "ID.RA-07",
    "ID.RA-08", "ID.RA-09", "ID.RA-10",
    # PR.AA
    "PR.AA-01", "PR.AA-02", "PR.AA-03", "PR.AA-04", "PR.AA-05", "PR.AA-06",
    # PR.AT
    "PR.AT-01", "PR.AT-02",
    # PR.DS
    "PR.DS-01", "PR.DS-02", "PR.DS-10", "PR.DS-11",
    # PR.IR
    "PR.IR-01", "PR.IR-02", "PR.IR-03", "PR.IR-04",
    # PR.PS
    "PR.PS-01", "PR.PS-02", "PR.PS-03", "PR.PS-04", "PR.PS-05", "PR.PS-06",
    # DE.AE
    "DE.AE-02", "DE.AE-03", "DE.AE-04", "DE.AE-06", "DE.AE-07", "DE.AE-08",
    # DE.CM
    "DE.CM-01", "DE.CM-02", "DE.CM-03", "DE.CM-06", "DE.CM-09",
    # RS.AN
    "RS.AN-03", "RS.AN-06", "RS.AN-07", "RS.AN-08",
    # RS.CO
    "RS.CO-02", "RS.CO-03",
    # RS.MA
    "RS.MA-01", "RS.MA-02", "RS.MA-03", "RS.MA-04", "RS.MA-05",
    # RS.MI
    "RS.MI-01", "RS.MI-02",
    # RC.CO
    "RC.CO-03", "RC.CO-04",
    # RC.RP
    "RC.RP-01", "RC.RP-02", "RC.RP-03", "RC.RP-04", "RC.RP-05", "RC.RP-06",
})

# The 26 withdrawn Subcategories whose parent Category is live in CSF 2.0,
# mapped to a note built from their OSCAL incorporated_into / moved_to links.
CSF_WITHDRAWN_SUBCATEGORIES: dict[str, str] = {
    "ID.AM-06": "incorporated into GV.RR-02, GV.SC-02",
    "PR.AT-03": "incorporated into PR.AT-01, PR.AT-02",
    "PR.AT-04": "incorporated into PR.AT-02",
    "PR.AT-05": "incorporated into PR.AT-02",
    "PR.DS-03": "incorporated into ID.AM-08, PR.PS-03",
    "PR.DS-04": "moved to PR.IR-04",
    "PR.DS-05": "incorporated into PR.DS-01, PR.DS-02, PR.DS-10",
    "PR.DS-06": "incorporated into PR.DS-01, DE.CM-09",
    "PR.DS-07": "incorporated into PR.IR-01",
    "PR.DS-08": "incorporated into ID.RA-09, DE.CM-09",
    "DE.AE-01": "incorporated into ID.AM-03",
    "DE.AE-05": "moved to DE.AE-08",
    "DE.CM-04": "incorporated into DE.CM-01, DE.CM-09",
    "DE.CM-05": "incorporated into DE.CM-01, DE.CM-09",
    "DE.CM-07": "incorporated into DE.CM-01, DE.CM-03, DE.CM-06, DE.CM-09",
    "DE.CM-08": "incorporated into ID.RA-01",
    "RS.AN-01": "incorporated into RS.MA-02",
    "RS.AN-02": "incorporated into RS.MA-02, RS.MA-03, RS.MA-04",
    "RS.AN-04": "moved to RS.MA-03",
    "RS.AN-05": "moved to ID.RA-08",
    "RS.CO-01": "incorporated into PR.AT-01",
    "RS.CO-04": "incorporated into RS.MA-01, RS.MA-04",
    "RS.CO-05": "incorporated into RS.CO-03",
    "RS.MI-03": "incorporated into ID.RA-06",
    "RC.CO-01": "incorporated into RC.CO-04",
    "RC.CO-02": "incorporated into RC.CO-04",
}


def is_valid_category(code: str) -> bool:
    """Return True if ``code`` is a real CSF 2.0 Category (FUNCTION.CATEGORY)."""
    return code in CSF_CATEGORIES


def relocation_note(code: str) -> str | None:
    """Return a CSF 1.1->2.0 relocation note for ``code``, or None if unknown."""
    return CSF_1_1_RELOCATED.get(code)


def is_valid_subcategory(code: str) -> bool:
    """Return True if ``code`` is a live CSF 2.0 Subcategory (FUNCTION.CATEGORY-NN)."""
    return code in CSF_SUBCATEGORIES


def withdrawal_note(code: str) -> str | None:
    """Return the OSCAL withdrawal note for Subcategory ``code``, or None if not withdrawn."""
    return CSF_WITHDRAWN_SUBCATEGORIES.get(code)
