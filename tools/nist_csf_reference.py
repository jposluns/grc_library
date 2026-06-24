"""NIST Cybersecurity Framework 2.0 Category reference.

A citation index of the CSF 2.0 Core's Function and Category identifiers,
used by ``lint-matrix-control-codes.py`` to validate the NIST CSF 2.0
column of the GRC compliance-alignment matrix at the category level (does
each cited ``FUNCTION.CATEGORY`` token name a real CSF 2.0 Category, not a
CSF 1.1 category removed or moved in 2.0).

Provenance: the Function and Category identifiers and names are transcribed
from Table 1 of NIST CSWP 29, *The NIST Cybersecurity Framework (CSF) 2.0*
(2024), the authoritative Core. NIST publications are US-government work and
are not subject to copyright; this module is a plain index of the Category
identifiers (it carries none of the framework's Subcategory text or
implementation guidance). The source PDF was supplied by the maintainer and
read with ``pypdf``; the 22 Category codes here were extracted directly from
that text and cross-checked against the six Function names.

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
}


def is_valid_category(code: str) -> bool:
    """Return True if ``code`` is a real CSF 2.0 Category (FUNCTION.CATEGORY)."""
    return code in CSF_CATEGORIES


def relocation_note(code: str) -> str | None:
    """Return a CSF 1.1->2.0 relocation note for ``code``, or None if unknown."""
    return CSF_1_1_RELOCATED.get(code)
