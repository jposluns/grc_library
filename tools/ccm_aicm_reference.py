"""Authoritative CSA CCM / AICM control-code reference for citation validation.

PROVENANCE AND LICENCE (read before editing)
--------------------------------------------
This module is a **fair-use citation-verification index** derived from two
CSA-published catalogues, used as the source of truth by
``tools/lint-ccm-aicm-citations.py``:

  * CSA Cloud Controls Matrix (CCM) v4.1.0
  * CSA AI Controls Matrix (AICM) v1.1.0

It records ONLY the factual control identifiers (domain codes, control IDs)
and their short control titles - the minimum needed to verify that a citation
in the corpus names a control that actually exists and titles it correctly.
It deliberately contains NONE of the catalogues' expressive/normative content:
no control specifications, no implementation or auditing guidelines, no CAIQ
questions. Control IDs are factual identifiers (not copyrightable); the short
titles are quoted for the purpose of citation accuracy with attribution to the
Cloud Security Alliance. This is an index, NOT a redistribution of the
matrices, which carry an explicit no-redistribution clause and are obtained
directly from CSA (https://cloudsecurityalliance.org).

Maintenance: when CSA publishes a new CCM/AICM version, refresh these dicts
from the authoritative spreadsheet and bump the VERSION strings below.
"""

CCM_VERSION = "v4.1.0"
AICM_VERSION = "v1.1.0"

# CSA CCM v4.1.0 control ID -> canonical control title.
CCM_V41 = {
    # A&A
    "A&A-01": "Audit and Assurance Policy and Procedures",
    "A&A-02": "Independent Assessments",
    "A&A-03": "Risk Based Planning Assessment",
    "A&A-04": "Requirements Compliance",
    "A&A-05": "Audit Management Process",
    "A&A-06": "Remediation",
    # AIS
    "AIS-01": "Application and Interface Security Policy and Procedures",
    "AIS-02": "Application Security Baseline Requirements",
    "AIS-03": "Application Security Metrics",
    "AIS-04": "Secure Application Development Lifecycle",
    "AIS-05": "Application Security Testing",
    "AIS-06": "Secure Application Deployment",
    "AIS-07": "Application Vulnerability Remediation",
    "AIS-08": "API Security",
    # BCR
    "BCR-01": "Business Continuity Management Policy and Procedures",
    "BCR-02": "Risk Assessment and Impact Analysis",
    "BCR-03": "Business Continuity Strategy",
    "BCR-04": "Business Continuity Planning",
    "BCR-05": "Documentation",
    "BCR-06": "Business Continuity Exercises",
    "BCR-07": "Communication",
    "BCR-08": "Backup",
    "BCR-09": "Disaster Response Plan",
    "BCR-10": "Response Plan Exercise",
    "BCR-11": "Equipment Redundancy",
    # CCC
    "CCC-01": "Change Management Policy and Procedures",
    "CCC-02": "Quality Testing",
    "CCC-03": "Change Management Technology",
    "CCC-04": "Unauthorized Change Protection",
    "CCC-05": "Change Agreements",
    "CCC-06": "Change Management Baseline",
    "CCC-07": "Detection of Baseline Deviation",
    "CCC-08": "Exception Management",
    "CCC-09": "Change Restoration",
    # CEK
    "CEK-01": "Encryption and Key Management Policy and Procedures",
    "CEK-02": "CEK Roles and Responsibilities",
    "CEK-03": "Data Protection",
    "CEK-04": "Encryption Algorithm",
    "CEK-05": "Encryption Change Management",
    "CEK-06": "Encryption Change Cost Benefit Analysis",
    "CEK-07": "Encryption Risk Management",
    "CEK-08": "Service Customer Key Management Capability",
    "CEK-09": "Encryption and Key Management Audit",
    "CEK-10": "Key Generation",
    "CEK-11": "Key Purpose",
    "CEK-12": "Key Rotation",
    "CEK-13": "Key Revocation",
    "CEK-14": "Key Destruction",
    "CEK-15": "Key Activation",
    "CEK-16": "Key Suspension",
    "CEK-17": "Key Deactivation",
    "CEK-18": "Key Archival",
    "CEK-19": "Key Compromise",
    "CEK-20": "Key Recovery",
    "CEK-21": "Key Inventory Management",
    # DCS
    "DCS-01": "Physical and Environmental Security Policy and Procedures",
    "DCS-02": "Off-Site Equipment Disposal Policy and Procedures",
    "DCS-03": "Off-Site Transfer Authorization Policy and Procedures",
    "DCS-04": "Secure Area Policy and Procedures",
    "DCS-05": "Secure Media Transportation Policy and Procedures",
    "DCS-06": "Assets Classification",
    "DCS-07": "Assets Cataloguing and Tracking",
    "DCS-08": "Controlled Physical Access Points",
    "DCS-09": "Equipment Identification",
    "DCS-10": "Secure Area Authorization",
    "DCS-11": "Surveillance System",
    "DCS-12": "Adverse Event Response Training",
    "DCS-13": "Cabling Security",
    "DCS-14": "Environmental Systems",
    "DCS-15": "Secure Utilities",
    "DCS-16": "Equipment Location",
    "DCS-17": "Datacenter Metrics",
    "DCS-18": "Datacenter Operations Resilience",
    # DSP
    "DSP-01": "Security and Privacy Policy and Procedures",
    "DSP-02": "Secure Disposal",
    "DSP-03": "Data Inventory",
    "DSP-04": "Data Classification",
    "DSP-05": "Data Flow Documentation",
    "DSP-06": "Data Ownership and Stewardship",
    "DSP-07": "Data Protection by Design and Default",
    "DSP-08": "Data Privacy by Design and Default",
    "DSP-09": "Data Protection Impact Assessment",
    "DSP-10": "Sensitive Data Transfer",
    "DSP-11": "Personal Data Access, Reversal, Rectification and Deletion",
    "DSP-12": "Limitation of Purpose in Personal Data Processing",
    "DSP-13": "Personal Data Sub-processing",
    "DSP-14": "Disclosure of Data Sub-processors",
    "DSP-15": "Limitation of Production Data Use",
    "DSP-16": "Data Retention and Deletion",
    "DSP-17": "Sensitive Data Protection",
    "DSP-18": "Disclosure Notification",
    "DSP-19": "Data Location",
    # GRC
    "GRC-01": "Governance Program Policy and Procedures",
    "GRC-02": "Risk Management Program",
    "GRC-03": "Organizational Policy Reviews",
    "GRC-04": "Policy Exception Process",
    "GRC-05": "Information Security Program",
    "GRC-06": "Governance Responsibility Model",
    "GRC-07": "Information System Regulatory Mapping",
    "GRC-08": "Special Interest Groups",
    # HRS
    "HRS-01": "Background Screening Policy and Procedures",
    "HRS-02": "Acceptable Use of Technology Policy and Procedures",
    "HRS-03": "Clean Desk Policy and Procedures",
    "HRS-04": "Remote and Home Working Policy and Procedures",
    "HRS-05": "Asset returns",
    "HRS-06": "Employment Termination",
    "HRS-07": "Employment Agreement Process",
    "HRS-08": "Employment Agreement Content",
    "HRS-09": "Personnel Roles and Responsibilities",
    "HRS-10": "Non-Disclosure Agreements",
    "HRS-11": "Security Awareness Training",
    "HRS-12": "Personal and Sensitive Data Awareness and Training",
    "HRS-13": "Compliance User Responsibility",
    # I&S
    "I&S-01": "Infrastructure and Virtualization Security Policy and Procedures",
    "I&S-02": "Capacity and Resource Planning",
    "I&S-03": "Network Security",
    "I&S-04": "OS Hardening and Base Controls",
    "I&S-05": "Production and Non-Production Environments",
    "I&S-06": "Segmentation and Segregation",
    "I&S-07": "Migration to Cloud Environments",
    "I&S-08": "Network Architecture Documentation",
    "I&S-09": "Network Defense",
    # IAM
    "IAM-01": "Identity and Access Management Policy and Procedures",
    "IAM-02": "Credentials Management Policy and Procedures",
    "IAM-03": "Identity Inventory",
    "IAM-04": "Separation of Duties",
    "IAM-05": "Least Privilege",
    "IAM-06": "Access Provisioning",
    "IAM-07": "Access Changes and Revocation",
    "IAM-08": "Access Review",
    "IAM-09": "Segregation of Privileged Access Roles",
    "IAM-10": "Management of Privileged Access Roles",
    "IAM-11": "Service Customers Approval for Agreed Privileged Access Roles",
    "IAM-12": "Unique Identities",
    "IAM-13": "Strong Authentication",
    "IAM-14": "Credentials Management",
    "IAM-15": "Authorization Mechanisms",
    # IPY
    "IPY-01": "Interoperability and Portability Policy and Procedures",
    "IPY-02": "Application Interface Availability",
    "IPY-03": "Secure Interoperability and Portability Management",
    "IPY-04": "Data Portability Contractual Obligations",
    # LOG
    "LOG-01": "Logging and Monitoring Policy and Procedures",
    "LOG-02": "Audit Logs Protection",
    "LOG-03": "Security Monitoring and Alerting",
    "LOG-04": "Audit Logs Access and Accountability",
    "LOG-05": "Audit Logs Monitoring and Response",
    "LOG-06": "Clock Synchronization",
    "LOG-07": "Logging Scope",
    "LOG-08": "Audit Logs Sanitization",
    "LOG-09": "Log Records",
    "LOG-10": "Audit Records Protection",
    "LOG-11": "Encryption Monitoring and Reporting",
    "LOG-12": "Transaction/Activity Logging",
    "LOG-13": "Access Control Logs",
    "LOG-14": "Failures and Anomalies Reporting",
    # SEF
    "SEF-01": "Security Incident Management Policy and Procedures",
    "SEF-02": "Service Management Policy and Procedures",
    "SEF-03": "Incident Response Plans",
    "SEF-04": "Incident Response Testing",
    "SEF-05": "Incident Response Metrics",
    "SEF-06": "Event Triage Processes",
    "SEF-07": "Incident Management and Response",
    "SEF-08": "Security Breach Notification",
    "SEF-09": "Incident Records Management",
    "SEF-10": "Points of Contact Maintenance",
    # STA
    "STA-01": "Supply Chain Risk Management Policies and Procedures",
    "STA-02": "SSRM Policy and Procedures",
    "STA-03": "SSRM Supply Chain",
    "STA-04": "SSRM Guidance",
    "STA-05": "SSRM Control Ownership",
    "STA-06": "SSRM Documentation Review",
    "STA-07": "SSRM Control Implementation",
    "STA-08": "Supply Chain Inventory",
    "STA-09": "Service Bill of Material (BOM)",
    "STA-10": "Supply Chain Risk Management",
    "STA-11": "Primary Service and Contractual Agreement",
    "STA-12": "Supply Chain Agreement Review",
    "STA-13": "Supply Chain Compliance Assessment",
    "STA-14": "Supply Chain Service Agreement Compliance",
    "STA-15": "Supply Chain Governance Review",
    "STA-16": "Supply Chain Data Security Assessment",
    # TVM
    "TVM-01": "Threat and Vulnerability Management Policy and Procedures",
    "TVM-02": "Malware and Malicious Instructions Protection Policy and Procedures",
    "TVM-03": "Vulnerability Identification",
    "TVM-04": "Threat Analysis and Modelling",
    "TVM-05": "Detection Updates",
    "TVM-06": "External Library Vulnerabilities",
    "TVM-07": "Penetration Testing",
    "TVM-08": "Vulnerability Remediation Schedule",
    "TVM-09": "Vulnerability Prioritization",
    "TVM-10": "Threat Response",
    "TVM-11": "Vulnerability Management Reporting",
    "TVM-12": "Vulnerability Management Metrics",
    # UEM
    "UEM-01": "Endpoint Devices Policy and Procedures",
    "UEM-02": "Application and Service Approval",
    "UEM-03": "Compatibility",
    "UEM-04": "Endpoint Inventory",
    "UEM-05": "Endpoint Management",
    "UEM-06": "Automatic Lock Screen",
    "UEM-07": "Operating Systems",
    "UEM-08": "Storage Encryption",
    "UEM-09": "Anti-Malware Detection and Prevention",
    "UEM-10": "Software Firewall",
    "UEM-11": "Data Loss Prevention",
    "UEM-12": "Remote Locate",
    "UEM-13": "Remote Wipe",
    "UEM-14": "Third-Party Endpoint Security Posture",
}

# CSA AICM v1.1.0 control ID -> canonical control title.
AICM_V11 = {
    # A&A
    "A&A-01": "Audit and Assurance Policy and Procedures",
    "A&A-02": "Independent Assessments",
    "A&A-03": "Risk Based Planning Assessment",
    "A&A-04": "Requirements Compliance",
    "A&A-05": "Audit Management Process",
    "A&A-06": "Remediation",
    # AIS
    "AIS-01": "Application and Interface Security Policy and Procedures",
    "AIS-02": "Application Security Baseline Requirements",
    "AIS-03": "Application Security Metrics",
    "AIS-04": "Secure Application Development Lifecycle",
    "AIS-05": "Application Security Testing",
    "AIS-06": "Secure Application Deployment",
    "AIS-07": "Application Vulnerability Remediation",
    "AIS-08": "API Security",
    "AIS-09": "Input Validation",
    "AIS-10": "Output Validation",
    "AIS-11": "Agents Security Boundaries",
    "AIS-12": "Source Code Management",
    "AIS-13": "AI Sandboxing",
    "AIS-14": "AI Cache Protection",
    "AIS-15": "Prompt Differentiation",
    # BCR
    "BCR-01": "Business Continuity Management Policy and Procedures",
    "BCR-02": "Risk Assessment and Impact Analysis",
    "BCR-03": "Business Continuity Strategy",
    "BCR-04": "Business Continuity Planning",
    "BCR-05": "Documentation",
    "BCR-06": "Business Continuity Exercises",
    "BCR-07": "Communication",
    "BCR-08": "Backup",
    "BCR-09": "Disaster Response Plan",
    "BCR-10": "Response Plan Exercise",
    "BCR-11": "Equipment Redundancy",
    # CCC
    "CCC-01": "Change Management Policy and Procedures",
    "CCC-02": "Quality Testing",
    "CCC-03": "Change Management Technology",
    "CCC-04": "Unauthorized Change Protection",
    "CCC-05": "Change Agreements",
    "CCC-06": "Change Management Baseline",
    "CCC-07": "Detection of Baseline Deviation",
    "CCC-08": "Exception Management",
    "CCC-09": "Change Restoration",
    # CEK
    "CEK-01": "Encryption and Key Management Policy and Procedures",
    "CEK-02": "CEK Roles and Responsibilities",
    "CEK-03": "Data Protection",
    "CEK-04": "Encryption Algorithm",
    "CEK-05": "Encryption Change Management",
    "CEK-06": "Encryption Change Cost Benefit Analysis",
    "CEK-07": "Encryption Risk Management",
    "CEK-08": "Service Customer Key Management Capability",
    "CEK-09": "Encryption and Key Management Audit",
    "CEK-10": "Key Generation",
    "CEK-11": "Key Purpose",
    "CEK-12": "Key Rotation",
    "CEK-13": "Key Revocation",
    "CEK-14": "Key Destruction",
    "CEK-15": "Key Activation",
    "CEK-16": "Key Suspension",
    "CEK-17": "Key Deactivation",
    "CEK-18": "Key Archival",
    "CEK-19": "Key Compromise",
    "CEK-20": "Key Recovery",
    "CEK-21": "Key Inventory Management",
    # DCS
    "DCS-01": "Physical and Environmental Security Policy and Procedures",
    "DCS-02": "Off-Site Equipment Disposal Policy and Procedures",
    "DCS-03": "Off-Site Transfer Authorization Policy and Procedures",
    "DCS-04": "Secure Area Policy and Procedures",
    "DCS-05": "Secure Media Transportation Policy and Procedures",
    "DCS-06": "Assets Classification",
    "DCS-07": "Assets Cataloguing and Tracking",
    "DCS-08": "Controlled Physical Access Points",
    "DCS-09": "Equipment Identification",
    "DCS-10": "Secure Area Authorization",
    "DCS-11": "Surveillance System",
    "DCS-12": "Adverse Event Response Training",
    "DCS-13": "Cabling Security",
    "DCS-14": "Environmental Systems",
    "DCS-15": "Secure Utilities",
    "DCS-16": "Equipment Location",
    "DCS-17": "Datacenter Metrics",
    "DCS-18": "Datacenter Operations Resilience",
    # DSP
    "DSP-01": "Security and Privacy Policy and Procedures",
    "DSP-02": "Secure Disposal",
    "DSP-03": "Data Inventory",
    "DSP-04": "Data Classification",
    "DSP-05": "Data Flow Documentation",
    "DSP-06": "Data Ownership and Stewardship",
    "DSP-07": "Data Protection by Design and Default",
    "DSP-08": "Data Privacy by Design and Default",
    "DSP-09": "Data Protection Impact Assessment",
    "DSP-10": "Sensitive Data Transfer",
    "DSP-11": "Personal Data Access, Reversal, Rectification and Deletion",
    "DSP-12": "Limitation of Purpose in Personal Data Processing",
    "DSP-13": "Personal Data Sub-processing",
    "DSP-14": "Disclosure of Data Sub-processors",
    "DSP-15": "Limitation of Production Data Use",
    "DSP-16": "Data Retention and Deletion",
    "DSP-17": "Sensitive Data Protection",
    "DSP-18": "Disclosure Notification",
    "DSP-19": "Data Location",
    "DSP-20": "Data Provenance and Transparency",
    "DSP-21": "Data Poisoning Prevention & Detection",
    "DSP-22": "Privacy Enhancing Technologies",
    "DSP-23": "Data Integrity Check",
    "DSP-24": "Data Differentiation and Relevance",
    # GRC
    "GRC-01": "Governance Program Policy and Procedures",
    "GRC-02": "Risk Management Program",
    "GRC-03": "Organizational Policy Reviews",
    "GRC-04": "Policy Exception Process",
    "GRC-05": "Information Security Program",
    "GRC-06": "Governance Responsibility Model",
    "GRC-07": "Information System Regulatory Mapping",
    "GRC-08": "Special Interest Groups",
    "GRC-09": "Acceptable Use of the AI Service",
    "GRC-10": "AI Impact Assessment",
    "GRC-11": "Bias and Fairness Assessment",
    "GRC-12": "Ethics Committee",
    "GRC-13": "Explainability Requirement",
    "GRC-14": "Explainability Evaluation",
    "GRC-15": "Human supervision",
    # HRS
    "HRS-01": "Background Screening Policy and Procedures",
    "HRS-02": "Acceptable Use of Technology Policy and Procedures",
    "HRS-03": "Clean Desk Policy and Procedures",
    "HRS-04": "Remote and Home Working Policy and Procedures",
    "HRS-05": "Asset returns",
    "HRS-06": "Employment Termination",
    "HRS-07": "Employment Agreement Process",
    "HRS-08": "Employment Agreement Content",
    "HRS-09": "Personnel Roles and Responsibilities",
    "HRS-10": "Non-Disclosure Agreements",
    "HRS-11": "Security Awareness Training",
    "HRS-12": "Personal and Sensitive Data Awareness and Training",
    "HRS-13": "Compliance User Responsibility",
    "HRS-14": "AI Competency Training",
    "HRS-15": "AI Acceptable Use",
    # I&S
    "I&S-01": "Infrastructure and Virtualization Security Policy and Procedures",
    "I&S-02": "Capacity and Resource Planning",
    "I&S-03": "Network Security",
    "I&S-04": "OS Hardening and Base Controls",
    "I&S-05": "Production and Non-Production Environments",
    "I&S-06": "Segmentation and Segregation",
    "I&S-07": "Migration to Hosted Environments",
    "I&S-08": "Network Architecture Documentation",
    "I&S-09": "Network Defense",
    # IAM
    "IAM-01": "Identity and Access Management Policy and Procedures",
    "IAM-02": "Credentials Management Policy and Procedures",
    "IAM-03": "Identity Inventory",
    "IAM-04": "Separation of Duties",
    "IAM-05": "Least Privilege",
    "IAM-06": "Access Provisioning",
    "IAM-07": "Access Changes and Revocation",
    "IAM-08": "Access Review",
    "IAM-09": "Segregation of Privileged Access Roles",
    "IAM-10": "Management of Privileged Access Roles",
    "IAM-11": "Service Customers' Approval for Agreed Privileged Access Roles",
    "IAM-12": "Unique Identities",
    "IAM-13": "Strong Authentication",
    "IAM-14": "Credentials Management",
    "IAM-15": "Authorization Mechanisms",
    "IAM-16": "Knowledge Access Control - Need to Know",
    "IAM-17": "Output Modification and Special Authorization",
    "IAM-18": "Agent Access Restriction",
    # IPY
    "IPY-01": "Interoperability and Portability Policy and Procedures",
    "IPY-02": "Application Interface Availability",
    "IPY-03": "Secure Interoperability and Portability Management",
    "IPY-04": "Data Portability Contractual Obligations",
    # LOG
    "LOG-01": "Logging and Monitoring Policy and Procedures",
    "LOG-02": "Audit Logs Protection",
    "LOG-03": "Security Monitoring and Alerting",
    "LOG-04": "Audit Logs Access and Accountability",
    "LOG-05": "Audit Logs Monitoring and Response",
    "LOG-06": "Clock Synchronization",
    "LOG-07": "Logging Scope",
    "LOG-08": "Audit Logs Sanitization",
    "LOG-09": "Log Records",
    "LOG-10": "Audit Records Protection",
    "LOG-11": "Encryption Monitoring and Reporting",
    "LOG-12": "Transaction/Activity Logging",
    "LOG-13": "Access Control Logs",
    "LOG-14": "Failures and Anomalies Reporting",
    "LOG-15": "Input Monitoring",
    "LOG-16": "Output Monitoring",
    # MDS
    "MDS-01": "Training Pipeline Security",
    "MDS-02": "Model Artifact Scanning",
    "MDS-03": "Model Documentation",
    "MDS-04": "Model Documentation Requirements",
    "MDS-05": "Model Documentation Validation",
    "MDS-06": "Adversarial Attack Analysis",
    "MDS-07": "Robustness against Adversarial Attack / Model Hardening",
    "MDS-08": "Model Integrity Checks",
    "MDS-09": "Model Signing/Ownership Verification",
    "MDS-10": "Model Continuous Monitoring",
    "MDS-11": "Model Failure",
    "MDS-12": "Open Model Risk Assessment",
    "MDS-13": "Secure Model Format",
    # SEF
    "SEF-01": "Security Incident Management Policy and Procedures",
    "SEF-02": "Service Management Policy and Procedures",
    "SEF-03": "Incident Response Plans",
    "SEF-04": "Incident Response Testing",
    "SEF-05": "Incident Response Metrics",
    "SEF-06": "Event Triage Processes",
    "SEF-07": "Incident Management and Response",
    "SEF-08": "Security Breach Notification",
    "SEF-09": "Incident Records Management",
    "SEF-10": "Points of Contact Maintenance",
    # STA
    "STA-01": "Supply Chain Risk Management Policies and Procedures",
    "STA-02": "SSRM Policy and Procedures",
    "STA-03": "SSRM Supply Chain",
    "STA-04": "SSRM Guidance",
    "STA-05": "SSRM Control Ownership",
    "STA-06": "SSRM Documentation Review",
    "STA-07": "SSRM Control Implementation",
    "STA-08": "Supply Chain Inventory",
    "STA-09": "Service Bill of Material (BOM)",
    "STA-10": "Supply Chain Risk Management",
    "STA-11": "Primary Service and Contractual Agreement",
    "STA-12": "Supply Chain Agreement Review",
    "STA-13": "Supply Chain Compliance Assessment",
    "STA-14": "Supply Chain Service Agreement Compliance",
    "STA-15": "Supply Chain Governance Review",
    "STA-16": "Supply Chain Data Security Assessment",
    # TVM
    "TVM-01": "Threat and Vulnerability Management Policy and Procedures",
    "TVM-02": "Malware and Malicious Instructions Protection Policy and Procedures",
    "TVM-03": "Vulnerability Identification",
    "TVM-04": "Threat Analysis and Modelling",
    "TVM-05": "Detection Updates",
    "TVM-06": "External Library Vulnerabilities",
    "TVM-07": "Penetration Testing",
    "TVM-08": "Vulnerability Remediation Schedule",
    "TVM-09": "Vulnerability Prioritization",
    "TVM-10": "Threat Response",
    "TVM-11": "Vulnerability Management Reporting",
    "TVM-12": "Vulnerability Management Metrics",
    "TVM-13": "Guardrails",
    # UEM
    "UEM-01": "Endpoint Devices Policy and Procedures",
    "UEM-02": "Application and Service Approval",
    "UEM-03": "Compatibility",
    "UEM-04": "Endpoint Inventory",
    "UEM-05": "Endpoint Management",
    "UEM-06": "Automatic Lock Screen",
    "UEM-07": "Operating Systems",
    "UEM-08": "Storage Encryption",
    "UEM-09": "Anti-Malware Detection and Prevention",
    "UEM-10": "Software Firewall",
    "UEM-11": "Data Loss Prevention",
    "UEM-12": "Remote Locate",
    "UEM-13": "Remote Wipe",
    "UEM-14": "Third-Party Endpoint Security Posture",
}

# Union view (AICM extends CCM): control ID -> title, AICM titles win on overlap
# where AICM re-states a CCM control (titles are identical for the shared base).
ALL_TITLES = {**CCM_V41, **AICM_V11}

# Valid domain code -> highest control number, for a given catalogue.
def _domains_of(catalogue):
    dom = {}
    for code in catalogue:
        prefix, num = code.rsplit("-", 1)
        dom[prefix] = max(dom.get(prefix, 0), int(num))
    return dom


# Domains by catalogue. CCM v4.1.0 has 17 domains; AICM v1.1.0 adds the
# AI-specific MDS (Model Security) domain, so AICM has 18. Keeping the two
# sets distinct (rather than only the blended union) lets a caller enforce
# catalogue discipline: a code in a column or section labelled "CSA CCM v4.1"
# must be a CCM v4.1 code, not an AICM-only one (e.g. an ``MDS-`` code).
CCM_DOMAINS = _domains_of(CCM_V41)
AICM_DOMAINS = _domains_of(AICM_V11)

# Valid domain code -> highest control number, across both matrices (union).
# Retained for the corpus-wide CSA citation gate, which validates a token
# against whichever catalogue its section/context names (CCM, AICM, or the
# union when unscoped).
VALID_DOMAINS = _domains_of(ALL_TITLES)


def is_ccm_v41(code: str) -> bool:
    """True if ``code`` is a real CSA CCM v4.1.0 control identifier."""
    return code in CCM_V41


def is_aicm(code: str) -> bool:
    """True if ``code`` is a real CSA AICM v1.1.0 control identifier."""
    return code in AICM_V11


def is_aicm_only(code: str) -> bool:
    """True if ``code`` exists in AICM v1.1.0 but NOT in CCM v4.1.0.

    These are the codes that must never appear in a column or section
    labelled "CSA CCM v4.1": they are valid AICM identifiers (so a bare
    existence check against the blended union passes them), but they are
    not CCM v4.1 controls. The canonical example is the AICM ``MDS``
    (Model Security) domain, which CCM v4.1 does not have.
    """
    return code in AICM_V11 and code not in CCM_V41

# Superseded / non-existent domain codes seen historically in the corpus, mapped
# to the correct current code, so the linter can emit an actionable message.
KNOWN_BAD_DOMAINS = {
    "GOV": "GRC (CCM/AICM governance domain; there is no GOV domain)",
    "IVS": "I&S (CCM v4.1.0 renamed the v4.0 IVS domain to I&S)",
    "NET": "I&S (network controls live in the I&S domain; there is no NET domain)",
    "GRM": "GRC (GRM was the CCM v3.0.1 code; v4.1 uses GRC)",
    "AUD": "A&A (audit/assurance is the A&A domain)",
    "EKM": "CEK (CCM v4.1 cryptography/key domain is CEK, not the v3 EKM)",
    "MOS": "UEM (CCM v4.1 mobile controls moved into Universal Endpoint Management)",
    "DSI": "DSP (CCM v4.1 data domain is DSP, not the v3 DSI)",
}
