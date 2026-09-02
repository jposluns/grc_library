"""Canonical ISO/IEC 27001:2022 Annex A control citation reference data.

Companion data module for ``audit-matrix-semantic-fit.py`` (the control-code
worklist tool). It records ONLY the factual identifiers needed to assess
citation fit: the 93 ISO/IEC 27001:2022 Annex A control codes with their
canonical short titles, keyed in the ``A.<theme>.<n>`` form the corpus and the
compliance matrix cite (e.g. ``A.5.1``, ``A.7.10``, ``A.8.34``). Identifier
lists and short titles are recorded here under the same fair-use
citation-index rationale as ``ccm_aicm_reference.py`` and
``cobit_iso31000_reference.py``; no framework body text is reproduced, and
this module is not a substitute for the licensed standard.

Provenance: the 93 code -> title pairs are the ISO/IEC 27001:2022 Annex A
(Table A.1) controls, cross-checked against the reference base's held
full-text extract
(``grc_library_ref/standards/ISO/ISO-IEC-27001-2022--ISMS-requirements--full-text.md``,
the Annex A control table beginning around line 879) and independently
re-verified by a triple-family panel against the canonical Annex A control
list. The four themes are closed and contiguous: Organizational A.5.1-A.5.37
(37), People A.6.1-A.6.8 (8), Physical A.7.1-A.7.14 (14), Technological
A.8.1-A.8.34 (34); 37 + 8 + 14 + 34 = 93.

Why titles here (unlike COBIT practice titles, which are deliberately absent):
the Annex A control titles are short, canonical, and stable across the
standard; the held extract line-wraps some of them in its PDF-derived layout,
so the titles here are the reconciled canonical strings, not a raw parse of a
wrapped line. Existence of an Annex A code is fully determined by membership
in this closed 93-control set.
"""

from __future__ import annotations

# ISO/IEC 27001:2022 Annex A control code -> canonical short title.
# Keyed in the "A.<theme>.<n>" citation form used across the corpus.
ISO27001_2022_ANNEX_A: dict[str, str] = {
    # A.5 Organizational controls (37)
    "A.5.1": "Policies for information security",
    "A.5.2": "Information security roles and responsibilities",
    "A.5.3": "Segregation of duties",
    "A.5.4": "Management responsibilities",
    "A.5.5": "Contact with authorities",
    "A.5.6": "Contact with special interest groups",
    "A.5.7": "Threat intelligence",
    "A.5.8": "Information security in project management",
    "A.5.9": "Inventory of information and other associated assets",
    "A.5.10": "Acceptable use of information and other associated assets",
    "A.5.11": "Return of assets",
    "A.5.12": "Classification of information",
    "A.5.13": "Labelling of information",
    "A.5.14": "Information transfer",
    "A.5.15": "Access control",
    "A.5.16": "Identity management",
    "A.5.17": "Authentication information",
    "A.5.18": "Access rights",
    "A.5.19": "Information security in supplier relationships",
    "A.5.20": "Addressing information security within supplier agreements",
    "A.5.21": "Managing information security in the information and communication technology (ICT) supply chain",
    "A.5.22": "Monitoring, review and change management of supplier services",
    "A.5.23": "Information security for use of cloud services",
    "A.5.24": "Information security incident management planning and preparation",
    "A.5.25": "Assessment and decision on information security events",
    "A.5.26": "Response to information security incidents",
    "A.5.27": "Learning from information security incidents",
    "A.5.28": "Collection of evidence",
    "A.5.29": "Information security during disruption",
    "A.5.30": "ICT readiness for business continuity",
    "A.5.31": "Legal, statutory, regulatory and contractual requirements",
    "A.5.32": "Intellectual property rights",
    "A.5.33": "Protection of records",
    "A.5.34": "Privacy and protection of personal identifiable information (PII)",
    "A.5.35": "Independent review of information security",
    "A.5.36": "Compliance with policies, rules and standards for information security",
    "A.5.37": "Documented operating procedures",
    # A.6 People controls (8)
    "A.6.1": "Screening",
    "A.6.2": "Terms and conditions of employment",
    "A.6.3": "Information security awareness, education and training",
    "A.6.4": "Disciplinary process",
    "A.6.5": "Responsibilities after termination or change of employment",
    "A.6.6": "Confidentiality or non-disclosure agreements",
    "A.6.7": "Remote working",
    "A.6.8": "Information security event reporting",
    # A.7 Physical controls (14)
    "A.7.1": "Physical security perimeters",
    "A.7.2": "Physical entry",
    "A.7.3": "Securing offices, rooms and facilities",
    "A.7.4": "Physical security monitoring",
    "A.7.5": "Protecting against physical and environmental threats",
    "A.7.6": "Working in secure areas",
    "A.7.7": "Clear desk and clear screen",
    "A.7.8": "Equipment siting and protection",
    "A.7.9": "Security of assets off-premises",
    "A.7.10": "Storage media",
    "A.7.11": "Supporting utilities",
    "A.7.12": "Cabling security",
    "A.7.13": "Equipment maintenance",
    "A.7.14": "Secure disposal or re-use of equipment",
    # A.8 Technological controls (34)
    "A.8.1": "User end point devices",
    "A.8.2": "Privileged access rights",
    "A.8.3": "Information access restriction",
    "A.8.4": "Access to source code",
    "A.8.5": "Secure authentication",
    "A.8.6": "Capacity management",
    "A.8.7": "Protection against malware",
    "A.8.8": "Management of technical vulnerabilities",
    "A.8.9": "Configuration management",
    "A.8.10": "Information deletion",
    "A.8.11": "Data masking",
    "A.8.12": "Data leakage prevention",
    "A.8.13": "Information backup",
    "A.8.14": "Redundancy of information processing facilities",
    "A.8.15": "Logging",
    "A.8.16": "Monitoring activities",
    "A.8.17": "Clock synchronization",
    "A.8.18": "Use of privileged utility programs",
    "A.8.19": "Installation of software on operational systems",
    "A.8.20": "Networks security",
    "A.8.21": "Security of network services",
    "A.8.22": "Segregation of networks",
    "A.8.23": "Web filtering",
    "A.8.24": "Use of cryptography",
    "A.8.25": "Secure development life cycle",
    "A.8.26": "Application security requirements",
    "A.8.27": "Secure system architecture and engineering principles",
    "A.8.28": "Secure coding",
    "A.8.29": "Security testing in development and acceptance",
    "A.8.30": "Outsourced development",
    "A.8.31": "Separation of development, test and production environments",
    "A.8.32": "Change management",
    "A.8.33": "Test information",
    "A.8.34": "Protection of information systems during audit testing",
}

# Closed-set sanity: the four themes are contiguous and total 93.
assert len(ISO27001_2022_ANNEX_A) == 93, (
    f"expected 93 Annex A controls, have {len(ISO27001_2022_ANNEX_A)}")
