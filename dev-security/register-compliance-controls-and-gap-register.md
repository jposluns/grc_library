# Compliance Controls and Gap Register Template

**Document Title:** Compliance Controls and Gap Register Template 
**Document Type:** Register 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Security Architecture Maintainer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`dev-security/standard-security-baseline-and-standards-reference.md`](standard-security-baseline-and-standards-reference.md), [`dev-security/standard-developer-security-requirements.md`](standard-developer-security-requirements.md), [`governance/matrix-cross-framework-alignment.md`](../governance/matrix-cross-framework-alignment.md), [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md) 
**Classification:** Public 
**Category:** Developer Security 
**Review Frequency:** Quarterly and upon material control implementation change 
**Repository Path:** [`dev-security/register-compliance-controls-and-gap-register.md`](register-compliance-controls-and-gap-register.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This register is the primary traceability artefact for audit, insurance, board reporting, and regulatory purposes. It maps security and compliance controls to CSA CCM v5, AICM v1.0.3, and COBIT 2025 process identifiers, and records implementation status, evidence type, and responsible party for each control.

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

## CSA CCM v5 control mapping

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
| AIS-01 | Application Security Policy | | | | |
| AIS-02 | Application Security Baseline | | | | |
| AIS-03 | Application Security Metrics | | | | |
| AIS-04 | Secure Application Development Lifecycle | | | | |
| AIS-05 | Application Security Testing | | | | |
| AIS-06 | Secure Application Deployment | | | | |
| AIS-07 | Application Vulnerability Remediation | | | | |
| AIS-08 | API Security | | | | |

### Business continuity management (BCR)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| BCR-01 | BCM Policy and Procedures | | | | |
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
| CCC-01 | Change Management Policy | | | | |
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
| CEK-01 | Encryption and Key Management Policy | | | | |
| CEK-03 | Data Protection | | | | |
| CEK-04 | Encryption Algorithm | | | | |
| CEK-06 | Encryption Change Management | | | | |
| CEK-09 | Encryption Key Generation | | | | |
| CEK-10 | Encryption Key Purpose | | | | |
| CEK-11 | Encryption Key Rotation | | | | |
| CEK-12 | Encryption Key Revocation | | | | |
| CEK-13 | Encryption Key Destruction | | | | |
| CEK-19 | Encryption Key Inventory | | | | |
| CEK-21 | Unmanaged Certificates | | | | |

### Data security and privacy (DSP)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| DSP-01 | Security and Privacy Policy | | | | |
| DSP-03 | Data Inventory | | | | |
| DSP-04 | Data Classification | | | | |
| DSP-05 | Data Flow Documentation | | | | |
| DSP-07 | Secure Disposal | | | | |
| DSP-08 | Privacy by Design | | | | |
| DSP-09 | Data Protection Impact Assessment | | | | |
| DSP-15 | Limitation of Production Data Use | | | | |
| DSP-17 | Personal Data Access | | | | |
| DSP-18 | Disclosure Notification | | | | |
| DSP-19 | Data Location | | | | |

### Datacenter security (DCS)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| DCS-01 | Off-site Equipment Disposal | | | | |
| DCS-04 | Secure Area Authorization | | | | |
| DCS-06 | Secure Area Visitor Access | | | | |
| DCS-07 | Secure Area System Installation | | | | |
| DCS-09 | Controlled Access Points | | | | |
| DCS-11 | CCTV | | | | |
| DCS-12 | Cabling Security | | | | |
| DCS-13 | Environmental Risks | | | | |

### Governance, risk and compliance (GRC)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| GRC-01 | Governance Programme Policy | | | | |
| GRC-02 | Risk Management Programme | | | | |
| GRC-03 | Organizational Policy Reviews | | | | |
| GRC-04 | Policy Exception Process | | | | |
| GRC-05 | Information Security Programme | | | | |
| GRC-06 | Regulatory Change | | | | |
| GRC-07 | Information System Regulatory Mapping | | | | |

### Human resources (HRS)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| HRS-01 | Background Verification | | | | |
| HRS-02 | Acceptable Use Policy | | | | |
| HRS-03 | Clean Desk Policy | | | | |
| HRS-06 | Employment Termination | | | | |
| HRS-09 | Personnel Training and Awareness | | | | |
| HRS-11 | Security Awareness Training | | | | |

### Identity and access management (IAM)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| IAM-01 | IAM Policy and Procedures | | | | |
| IAM-02 | Strong Password Policy and Procedures | | | | |
| IAM-03 | Identity Inventory | | | | |
| IAM-04 | Separation of Duties | | | | |
| IAM-05 | Least Privilege | | | | |
| IAM-07 | Access Changes and Revocation | | | | |
| IAM-08 | Access Review | | | | |
| IAM-09 | Segregation of Privileged Access | | | | |
| IAM-10 | Management of Privileged Access | | | | |
| IAM-12 | Unique Identities | | | | |
| IAM-13 | Strong Authentication | | | | |
| IAM-14 | Credentials Management | | | | |
| IAM-15 | Authorization Mechanisms | | | | |

### Infrastructure and virtualization security (IVS)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| IVS-01 | Audit Logging and Monitoring | | | | |
| IVS-03 | Migration and Asset Ownership | | | | |
| IVS-04 | Network Architecture | | | | |
| IVS-06 | Network Defense | | | | |
| IVS-07 | Segmentation and Segregation | | | | |
| IVS-08 | Production and Non-Production Environments | | | | |
| IVS-09 | Vulnerability and Patch Management | | | | |

### Logging and monitoring (LOG)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| LOG-01 | Logging and Monitoring Policy | | | | |
| LOG-02 | Audit Logs Protection | | | | |
| LOG-03 | Security Monitoring and Alerting | | | | |
| LOG-06 | Clock Synchronization | | | | |
| LOG-07 | Logging Scope | | | | |
| LOG-09 | Log Records | | | | |
| LOG-10 | Audit Records Protection | | | | |
| LOG-12 | Transaction / Activity Logging | | | | |
| LOG-13 | Access Control Logs | | | | |
| LOG-14 | Failures and Anomalies Reporting | | | | |

### Security incident management, e-discovery, and cloud forensics (SEF)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| SEF-01 | Security Incident Management Policy | | | | |
| SEF-03 | Incident Response Plans | | | | |
| SEF-04 | Incident Response Testing | | | | |
| SEF-07 | Incident Management and Response | | | | |
| SEF-08 | Security Breach Notification | | | | |
| SEF-09 | Incident Records Management | | | | |
| SEF-10 | Points of Contact Maintenance | | | | |

### Supply chain management (STA)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| STA-01 | Supply Chain Risk Management Policy | | | | |
| STA-04 | Supply Chain Agreement Review | | | | |
| STA-08 | Supply Chain Inventory | | | | |
| STA-09 | Service Bill of Materials | | | | |
| STA-10 | Supply Chain Risk Management | | | | |
| STA-13 | Supply Chain Agreement | | | | |

### Threat and vulnerability management (TVM)

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| TVM-01 | TVM Policy and Procedures | | | | |
| TVM-02 | Malware Protection Policy | | | | |
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
| UEM-01 | Endpoint Devices Policy | | | | |
| UEM-02 | Application and Service Approval | | | | |
| UEM-03 | Endpoint Inventory | | | | |
| UEM-05 | Mobile Endpoint Management | | | | |
| UEM-08 | Operating System Hardening | | | | |
| UEM-09 | Protection of Data on End-User Devices | | | | |
| UEM-11 | BYOD / Personal Device Policy | | | | |
| UEM-14 | Third-Party Application Security | | | | |

---

## AICM v1.0.3: AI-specific controls

Applies to any AI or ML system in production. See [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md) for detailed requirements.

| Control ID | Control Title | Status | Responsible | Evidence Reference | Notes |
| --- | --- | --- | --- | --- | --- |
| GRC-09 | Acceptable Use of AI Service | | | | |
| GRC-10 | AI Impact Assessment | | | | |
| GRC-12 | Ethics Committee | | | | |
| HRS-15 | AI Acceptable Use | | | | |
| MDS-01 | Model Inventory | | | | |
| MDS-02 | Model Documentation | | | | |
| MDS-03 | Training Data Governance | | | | |
| MDS-04 | Model Bias and Fairness Assessment | | | | |
| MDS-05 | Explainability and Transparency | | | | |
| MDS-06 | Adversarial Robustness Testing | | | | |
| MDS-07 | Model Access Controls | | | | |
| MDS-08 | Inference Input Validation | | | | |
| MDS-09 | Model Output Validation | | | | |
| MDS-10 | Prompt Injection Controls | | | | |
| MDS-11 | Agents Security Boundaries | | | | |
| MDS-12 | Model Monitoring and Drift Detection | | | | |
| MDS-13 | Model Decommissioning | | | | |

---

## COBIT 2025 process alignment

| COBIT Process | Description | Status | Lead Role | Notes |
| --- | --- | --- | --- | --- |
| APO01 | Managed IT Management Framework | | | |
| APO06 | Managed Budget and Costs | | | |
| APO12 | Managed Risk | | | |
| APO13 | Managed Security | | | |
| APO14 | Managed AI | | | |
| BAI03 | Managed Solutions Identification and Build | | | |
| BAI06 | Managed IT Changes | | | |
| BAI07 | Managed IT Change Acceptance | | | |
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
