"""Canonical COBIT 2019 and ISO 31000:2018 citation reference data.

Companion data module for ``lint-cobit-iso31000-citations.py`` (the
COBIT / ISO 31000 citation-existence audit) and for the
``audit-matrix-semantic-fit.py`` worklist tool. It records ONLY the
factual identifiers needed to validate citations: the 40 COBIT 2019
governance and management objective codes with their canonical titles,
the per-objective management-practice count (every objective's
practices are contiguous from .01, so a count fully determines the
valid practice-code range), and the ISO 31000:2018 clause-number tree
with clause headings. Identifier lists and short titles are cited here
under the same fair-use citation-index rationale as
``ccm_aicm_reference.py``; no framework body text is reproduced, and
this module is not a substitute for the licensed publications.

Provenance: both sets were derived DETERMINISTICALLY (a parse script,
not hand transcription) from the reference base's held full-text
extracts, and the parse was independently cross-checked against a
second worker's manual extraction with exact agreement:

- COBIT 2019 Framework: Governance and Management Objectives (ISACA),
  held extract in the scratch reference base under
  ``ref/frameworks/COBIT/``. The 231-practice set is closed: a
  whole-extract token scan finds no practice code outside the parsed
  per-objective ranges (this is how the APO12.07 fabrication class is
  caught; APO12 ends at .06).
- ISO 31000:2018 Risk management, Guidelines (ISO, TC 262; second
  edition 2018-02), held extract in the scratch reference base under
  ``ref/standards/ISO/`` (ingested 2026-07-02). The standard has
  clauses 1-6 only (no clause 7 or higher, no annexes); the deepest
  numbering level is x.y.z. Clause 3's numbered entries (3.1-3.8) are
  term definitions, included here as valid citable numbers. ISO 31000
  is an ISO standard (not ISO/IEC); the linter flags the wrong
  designation.

Practice-level canonical TITLES are deliberately NOT recorded: the
held extract line-wraps many practice titles, so embedding them would
risk enshrining truncated strings as canonical (the fabrication class
this module exists to prevent). Existence is validated by range;
title checking applies to objective codes only, where the 40 titles
extract cleanly.

Maintenance: on a new COBIT release or ISO 31000 edition, refresh from
the newly held extract with the same deterministic parse, update the
version constants, and record the change in the CHANGELOG.
"""

COBIT_VERSION = "2019"
ISO31000_VERSION = "2018"

# The 40 COBIT 2019 governance (EDM) and management (APO/BAI/DSS/MEA)
# objectives, code -> canonical title.
COBIT_OBJECTIVES = {
    # EDM: Evaluate, Direct and Monitor
    "EDM01": "Ensured Governance Framework Setting and Maintenance",
    "EDM02": "Ensured Benefits Delivery",
    "EDM03": "Ensured Risk Optimization",
    "EDM04": "Ensured Resource Optimization",
    "EDM05": "Ensured Stakeholder Engagement",
    # APO: Align, Plan and Organize
    "APO01": "Managed I&T Management Framework",
    "APO02": "Managed Strategy",
    "APO03": "Managed Enterprise Architecture",
    "APO04": "Managed Innovation",
    "APO05": "Managed Portfolio",
    "APO06": "Managed Budget and Costs",
    "APO07": "Managed Human Resources",
    "APO08": "Managed Relationships",
    "APO09": "Managed Service Agreements",
    "APO10": "Managed Vendors",
    "APO11": "Managed Quality",
    "APO12": "Managed Risk",
    "APO13": "Managed Security",
    "APO14": "Managed Data",
    # BAI: Build, Acquire and Implement
    "BAI01": "Managed Programs",
    "BAI02": "Managed Requirements Definition",
    "BAI03": "Managed Solutions Identification and Build",
    "BAI04": "Managed Availability and Capacity",
    "BAI05": "Managed Organizational Change",
    "BAI06": "Managed IT Changes",
    "BAI07": "Managed IT Change Acceptance and Transitioning",
    "BAI08": "Managed Knowledge",
    "BAI09": "Managed Assets",
    "BAI10": "Managed Configuration",
    "BAI11": "Managed Projects",
    # DSS: Deliver, Service and Support
    "DSS01": "Managed Operations",
    "DSS02": "Managed Service Requests and Incidents",
    "DSS03": "Managed Problems",
    "DSS04": "Managed Continuity",
    "DSS05": "Managed Security Services",
    "DSS06": "Managed Business Process Controls",
    # MEA: Monitor, Evaluate and Assess
    "MEA01": "Managed Performance and Conformance Monitoring",
    "MEA02": "Managed System of Internal Control",
    "MEA03": "Managed Compliance With External Requirements",
    "MEA04": "Managed Assurance",
}

# Per-objective management-practice count. Every objective's practices
# are contiguous .01..N (closed-set verified against the held extract),
# so a code XXXnn.mm is valid iff XXXnn is an objective and
# 1 <= mm <= COBIT_PRACTICE_COUNTS[XXXnn]. Total: 231 practices.
COBIT_PRACTICE_COUNTS = {
    "EDM01": 3, "EDM02": 4, "EDM03": 3, "EDM04": 3, "EDM05": 3,
    "APO01": 11, "APO02": 6, "APO03": 5, "APO04": 6, "APO05": 5,
    "APO06": 5, "APO07": 6, "APO08": 5, "APO09": 5, "APO10": 5,
    "APO11": 5, "APO12": 6, "APO13": 3, "APO14": 10,
    "BAI01": 9, "BAI02": 4, "BAI03": 12, "BAI04": 5, "BAI05": 7,
    "BAI06": 4, "BAI07": 8, "BAI08": 4, "BAI09": 5, "BAI10": 5,
    "BAI11": 9,
    "DSS01": 5, "DSS02": 7, "DSS03": 5, "DSS04": 8, "DSS05": 7,
    "DSS06": 6,
    "MEA01": 5, "MEA02": 4, "MEA03": 4, "MEA04": 9,
}

# ISO 31000:2018 clause tree, clause number -> canonical heading.
# Clauses 1-6 only; deepest level x.y.z; 3.1-3.8 are numbered term
# definitions (valid citable numbers). No clause 7+, no annexes.
ISO31000_CLAUSES = {
    "1": "Scope",
    "2": "Normative references",
    "3": "Terms and definitions",
    "3.1": "risk",
    "3.2": "risk management",
    "3.3": "stakeholder",
    "3.4": "risk source",
    "3.5": "event",
    "3.6": "consequence",
    "3.7": "likelihood",
    "3.8": "control",
    "4": "Principles",
    "5": "Framework",
    "5.1": "General",
    "5.2": "Leadership and commitment",
    "5.3": "Integration",
    "5.4": "Design",
    "5.4.1": "Understanding the organization and its context",
    "5.4.2": "Articulating risk management commitment",
    "5.4.3": "Assigning organizational roles, authorities,"
             " responsibilities and accountabilities",
    "5.4.4": "Allocating resources",
    "5.4.5": "Establishing communication and consultation",
    "5.5": "Implementation",
    "5.6": "Evaluation",
    "5.7": "Improvement",
    "5.7.1": "Adapting",
    "5.7.2": "Continually improving",
    "6": "Process",
    "6.1": "General",
    "6.2": "Communication and consultation",
    "6.3": "Scope, context and criteria",
    "6.3.1": "General",
    "6.3.2": "Defining the scope",
    "6.3.3": "External and internal context",
    "6.3.4": "Defining risk criteria",
    "6.4": "Risk assessment",
    "6.4.1": "General",
    "6.4.2": "Risk identification",
    "6.4.3": "Risk analysis",
    "6.4.4": "Risk evaluation",
    "6.5": "Risk treatment",
    "6.5.1": "General",
    "6.5.2": "Selection of risk treatment options",
    "6.5.3": "Preparing and implementing risk treatment plans",
    "6.6": "Monitoring and review",
    "6.7": "Recording and reporting",
}


def is_valid_cobit_code(code: str) -> bool:
    """True iff code is a valid COBIT 2019 objective or practice code."""
    if "." in code:
        obj, _, prac = code.partition(".")
        if obj not in COBIT_PRACTICE_COUNTS:
            return False
        try:
            num = int(prac)
        except ValueError:
            return False
        return 1 <= num <= COBIT_PRACTICE_COUNTS[obj]
    return code in COBIT_OBJECTIVES


def is_valid_iso31000_clause(clause: str) -> bool:
    """True iff clause is a numbered clause/term of ISO 31000:2018."""
    return clause in ISO31000_CLAUSES
