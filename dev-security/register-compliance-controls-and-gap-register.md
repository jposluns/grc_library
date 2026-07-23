# Compliance Controls and Gap Register Template

**Document Title:** Compliance Controls and Gap Register Template\
**Document Type:** Register\
**Version:** 1.0.6\
**Date:** 2026-07-23\
**Owner:** Security Architecture Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`dev-security/standard-security-baseline-and-standards-reference.md`](standard-security-baseline-and-standards-reference.md), [`dev-security/standard-developer-security-requirements.md`](standard-developer-security-requirements.md), [`governance/matrix-cross-framework-alignment.md`](../governance/matrix-cross-framework-alignment.md), [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md)\
**Classification:** Public\
**Category:** Developer Security\
**Review Frequency:** Quarterly and upon material control implementation change\
**Repository Path:** [`dev-security/register-compliance-controls-and-gap-register.md`](register-compliance-controls-and-gap-register.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register is the primary traceability artefact for audit, insurance, board reporting, and regulatory purposes. It maps security and compliance controls to CSA CCM v4.1, AICM v1.1, and COBIT 2019 process identifiers, and records implementation status, evidence type, and responsible party for each control.

Organizations should populate this template with their specific implementation status, evidence references, and responsible parties. The register must be updated when implementation status changes and reviewed quarterly at minimum.

---

## Status definitions

| Status | Meaning |
| --- | --- |
| Implemented | Control is live and evidenced. |
| In Progress | Control is being implemented. Target date must be set. |
| Planned | Control is in the roadmap but not yet started. Target date must be set. |
| Deferred | Explicitly deferred. Documented rationale and owner required. |
| Gap: Action Required | Control is not implemented and no plan exists. Requires CIO / CISO decision. |
| Not Applicable | Not applicable; documented justification required. |
| Inherited | Satisfied by a platform or service provider. Provider compliance documentation required. |

---

## How to use this register

1. Copy this template into your organization's documentation system.
2. For each control row, set the Status field using the definitions above.
3. Record the Evidence Reference (document title, system configuration, test result, or other artefact).
4. Assign a Responsible party (role title, not personal name).
5. Add Notes for context, deferred rationale, or open items.
6. For any control with status Gap: Action Required, create a CAPA record per the CAPA Procedure.
7. Review the register quarterly and update status when changes occur.
8. Archive completed versions of this register for a minimum of 7 years.

---

## CSA CCM v4.1 control mapping

### Audit and assurance (a&a)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| A&A-01 | Audit and Assurance Policy and Procedures | | | | |
| A&A-02 | Independent Assessments | | | | |
| A&A-03 | Risk Based Planning Assessment | | | | |
| A&A-04 | Requirements Compliance | | | | |
| A&A-05 | Audit Management Process | | | | |
| A&A-06 | Remediation | | | | |

### Application and interface security (AIS)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| AIS-01 | Application and Interface Security Policy and Procedures | | | | |
| AIS-02 | Application Security Baseline Requirements | | | | |
| AIS-03 | Application Security Metrics | | | | |
| AIS-04 | Secure Application Development Lifecycle | | | | |
| AIS-05 | Application Security Testing | | | | |
| AIS-06 | Secure Application Deployment | | | | |
| AIS-07 | Application Vulnerability Remediation | | | | |
| AIS-08 | API Security | | | | |

### Business continuity management (BCR)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| BCR-01 | Business Continuity Management Policy and Procedures | | | | |
| BCR-02 | Risk Assessment and Impact Analysis | | | | |
| BCR-03 | Business Continuity Strategy | | | | |
| BCR-04 | Business Continuity Planning | | | | |
| BCR-06 | Business Continuity Exercises | | | | |
| BCR-08 | Backup | | | | |
| BCR-09 | Disaster Response Plan | | | | |
| BCR-10 | Response Plan Exercise | | | | |
| BCR-11 | Equipment Redundancy | | | | |

### Change control and configuration management (CCC)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| CCC-01 | Change Management Policy and Procedures | | | | |
| CCC-02 | Quality Testing | | | | |
| CCC-03 | Change Management Technology | | | | |
| CCC-04 | Unauthorized Change Protection | | | | |
| CCC-05 | Change Agreements | | | | |
| CCC-06 | Change Management Baseline | | | | |
| CCC-07 | Detection of Baseline Deviation | | | | |
| CCC-08 | Exception Management | | | | |
| CCC-09 | Change Restoration | | | | |

### Cryptography, encryption and key management (CEK)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| CEK-01 | Encryption and Key Management Policy and Procedures | | | | |
| CEK-03 | Data Protection | | | | |
| CEK-04 | Encryption Algorithm | | | | |
| CEK-06 | Encryption Change Cost Benefit Analysis | | | | |
| CEK-09 | Encryption and Key Management Audit | | | | |
| CEK-10 | Key Generation | | | | |
| CEK-11 | Key Purpose | | | | |
| CEK-12 | Key Rotation | | | | |
| CEK-13 | Key Revocation | | | | |
| CEK-19 | Key Compromise | | | | |
| CEK-21 | Key Inventory Management | | | | |

### Data security and privacy (DSP)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| DSP-01 | Security and Privacy Policy and Procedures | | | | |
| DSP-03 | Data Inventory | | | | |
| DSP-04 | Data Classification | | | | |
| DSP-05 | Data Flow Documentation | | | | |
| DSP-07 | Data Protection by Design and Default | | | | |
| DSP-08 | Data Privacy by Design and Default | | | | |
| DSP-09 | Data Protection Impact Assessment | | | | |
| DSP-15 | Limitation of Production Data Use | | | | |
| DSP-17 | Sensitive Data Protection | | | | |
| DSP-18 | Disclosure Notification | | | | |
| DSP-19 | Data Location | | | | |

### Datacenter security (DCS)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| DCS-01 | Physical and Environmental Security Policy and Procedures | | | | |
| DCS-04 | Secure Area Policy and Procedures | | | | |
| DCS-06 | Assets Classification | | | | |
| DCS-07 | Assets Cataloguing and Tracking | | | | |
| DCS-09 | Equipment Identification | | | | |
| DCS-11 | Surveillance System | | | | |
| DCS-12 | Adverse Event Response Training | | | | |
| DCS-13 | Cabling Security | | | | |

### Governance, risk and compliance (GRC)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| GRC-01 | Governance Program Policy and Procedures | | | | |
| GRC-02 | Risk Management Program | | | | |
| GRC-03 | Organizational Policy Reviews | | | | |
| GRC-04 | Policy Exception Process | | | | |
| GRC-05 | Information Security Program | | | | |
| GRC-06 | Governance Responsibility Model | | | | |
| GRC-07 | Information System Regulatory Mapping | | | | |

### Human resources (HRS)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| HRS-01 | Background Screening Policy and Procedures | | | | |
| HRS-02 | Acceptable Use of Technology Policy and Procedures | | | | |
| HRS-03 | Clean Desk Policy and Procedures | | | | |
| HRS-06 | Employment Termination | | | | |
| HRS-09 | Personnel Roles and Responsibilities | | | | |
| HRS-11 | Security Awareness Training | | | | |

### Identity and access management (IAM)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| IAM-01 | Identity and Access Management Policy and Procedures | | | | |
| IAM-02 | Credentials Management Policy and Procedures | | | | |
| IAM-03 | Identity Inventory | | | | |
| IAM-04 | Separation of Duties | | | | |
| IAM-05 | Least Privilege | | | | |
| IAM-07 | Access Changes and Revocation | | | | |
| IAM-08 | Access Review | | | | |
| IAM-09 | Segregation of Privileged Access Roles | | | | |
| IAM-10 | Management of Privileged Access Roles | | | | |
| IAM-12 | Unique Identities | | | | |
| IAM-13 | Strong Authentication | | | | |
| IAM-14 | Credentials Management | | | | |
| IAM-15 | Authorization Mechanisms | | | | |

### Infrastructure security (I&S)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| I&S-01 | Infrastructure and Virtualization Security Policy and Procedures | | | | |
| I&S-03 | Network Security | | | | |
| I&S-04 | OS Hardening and Base Controls | | | | |
| I&S-06 | Segmentation and Segregation | | | | |
| I&S-07 | Migration to Cloud Environments | | | | |
| I&S-08 | Network Architecture Documentation | | | | |
| I&S-09 | Network Defense | | | | |

### Logging and monitoring (LOG)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| LOG-01 | Logging and Monitoring Policy and Procedures | | | | |
| LOG-02 | Audit Logs Protection | | | | |
| LOG-03 | Security Monitoring and Alerting | | | | |
| LOG-06 | Clock Synchronization | | | | |
| LOG-07 | Logging Scope | | | | |
| LOG-09 | Log Records | | | | |
| LOG-10 | Audit Records Protection | | | | |
| LOG-12 | Transaction/Activity Logging | | | | |
| LOG-13 | Access Control Logs | | | | |
| LOG-14 | Failures and Anomalies Reporting | | | | |

### Security incident management, e-discovery, and cloud forensics (SEF)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| SEF-01 | Security Incident Management Policy and Procedures | | | | |
| SEF-03 | Incident Response Plans | | | | |
| SEF-04 | Incident Response Testing | | | | |
| SEF-07 | Incident Management and Response | | | | |
| SEF-08 | Security Breach Notification | | | | |
| SEF-09 | Incident Records Management | | | | |
| SEF-10 | Points of Contact Maintenance | | | | |

### Supply chain management (STA)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| STA-01 | Supply Chain Risk Management Policies and Procedures | | | | |
| STA-04 | SSRM Guidance | | | | |
| STA-08 | Supply Chain Inventory | | | | |
| STA-09 | Service Bill of Material (BOM) | | | | |
| STA-10 | Supply Chain Risk Management | | | | |
| STA-13 | Supply Chain Compliance Assessment | | | | |

### Threat and vulnerability management (TVM)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| TVM-01 | Threat and Vulnerability Management Policy and Procedures | | | | |
| TVM-02 | Malware and Malicious Instructions Protection Policy and Procedures | | | | |
| TVM-03 | Vulnerability Identification | | | | |
| TVM-04 | Threat Analysis and Modelling | | | | |
| TVM-05 | Detection Updates | | | | |
| TVM-06 | External Library Vulnerabilities | | | | |
| TVM-07 | Penetration Testing | | | | |
| TVM-08 | Vulnerability Remediation Schedule | | | | |
| TVM-09 | Vulnerability Prioritization | | | | |
| TVM-10 | Threat Response | | | | |

### Universal endpoint management (UEM)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| UEM-01 | Endpoint Devices Policy and Procedures | | | | |
| UEM-02 | Application and Service Approval | | | | |
| UEM-03 | Compatibility | | | | |
| UEM-05 | Endpoint Management | | | | |
| UEM-08 | Storage Encryption | | | | |
| UEM-09 | Anti-Malware Detection and Prevention | | | | |
| UEM-11 | Data Loss Prevention | | | | |
| UEM-14 | Third-Party Endpoint Security Posture | | | | |

---

## AICM v1.1: AI-specific controls

Applies to any AI or ML system in production. See [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md) for detailed requirements.

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| GRC-09 | Acceptable Use of the AI Service | | | | |
| GRC-10 | AI Impact Assessment | | | | |
| GRC-12 | Ethics Committee | | | | |
| HRS-15 | AI Acceptable Use | | | | |
| MDS-01 | Training Pipeline Security | | | | |
| MDS-02 | Model Artifact Scanning | | | | |
| MDS-03 | Model Documentation | | | | |
| MDS-04 | Model Documentation Requirements | | | | |
| MDS-05 | Model Documentation Validation | | | | |
| MDS-06 | Adversarial Attack Analysis | | | | |
| MDS-07 | Robustness against Adversarial Attack / Model Hardening | | | | |
| MDS-08 | Model Integrity Checks | | | | |
| MDS-09 | Model Signing/Ownership Verification | | | | |
| MDS-10 | Model Continuous Monitoring | | | | |
| MDS-11 | Model Failure | | | | |
| MDS-12 | Open Model Risk Assessment | | | | |
| MDS-13 | Secure Model Format | | | | |

---

## COBIT 2019 process alignment

| COBIT Process | Description | Status | Lead Role | Notes |
| --- | --- | --- | --- | --- |
| APO01 | Managed I&T Management Framework | | | |
| APO06 | Managed Budget and Costs | | | |
| APO12 | Managed Risk | | | |
| APO13 | Managed Security | | | |
| APO14 | Managed Data | | | |
| BAI03 | Managed Solutions Identification and Build | | | |
| BAI06 | Managed IT Changes | | | |
| BAI07 | Managed IT Change Acceptance and Transitioning | | | |
| BAI09 | Managed Assets | | | |
| DSS02 | Managed Service Requests and Incidents | | | |
| DSS04 | Managed Continuity | | | |
| DSS05 | Managed Security Services | | | |
| MEA02 | Managed System of Internal Control | | | |
| MEA04 | Managed Assurance | | | |

---

## Open items and gap register

Use this section to track controls with status Gap: Action Required, In Progress (overdue), or Deferred. Each entry must have a confirmed owner and target resolution date.

| Item ID | Description | Control ID(s) | Risk Level | Owner | Target Date | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| *(example)* | *(Brief description of the gap or open item)* | *(e.g. IAM-03)* | *(Critical / High / Medium / Low)* | *(Role title)* | *(YYYY-MM-DD)* | *(Open / In Progress / Resolved)* | |

---

## Deferred controls register

Use this section to document controls that have been explicitly deferred, with rationale and responsible owner.

| Control ID | Control Title | Deferral Rationale | Interim Control | Owner | Target Activation |
| --- | --- | --- | --- | --- | --- |
| *(example)* | *(Control title)* | *(Reason for deferral: e.g. dependency on infrastructure programme)* | *(Compensating control in place)* | *(Role)* | *(Target date or milestone)* |

---

## Maintenance rules

1. This register must be reviewed quarterly and updated when any control status changes.
2. Every Gap: Action Required item must have a CAPA record per the CAPA Procedure.
3. Every Deferred item must have documented rationale, an interim compensating control, and an owner.
4. Evidence references must be specific and retrievable (document title, system name, or test report reference).
5. This register must not contain personal names: use role titles only.
6. This register must not contain specific vulnerability details, incident case references, or credentials: use the incident register and vulnerability management system for those records.
7. Archive completed quarterly snapshots for 7 years.

---

**End of Document**
