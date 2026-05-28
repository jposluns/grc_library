# Data Loss Prevention Standard

**Document Title:** Data Loss Prevention Standard 
**Document Type:** Standard 
**Version:** 1.3.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/standard-data-classification-and-handling.md`](standard-data-classification-and-handling.md), [`security/policy-encryption-and-key-management.md`](policy-encryption-and-key-management.md), [`security/procedure-incident-response.md`](procedure-incident-response.md) 
**Classification:** Public 
**Category:** Information Security 
**Review Frequency:** Annual and upon material threat, framework, or regulatory change 
**Repository Path:** [`security/standard-data-loss-prevention.md`](standard-data-loss-prevention.md) 
**Confidentiality:** Public 
**Licence:** CC0 1.0 Universal 

---

## 1. Purpose

This standard defines the governance, architecture, and technical controls for the Data Loss Prevention (DLP) programme. It establishes how the organization detects, monitors, and prevents unauthorised disclosure, transfer, or loss of data across all platforms. It ensures that consistent protection of sensitive data in use, at rest, and in motion in accordance with the Data Classification Model.

---

## 2. Scope

1. Applies to all employees, contractors, and third parties who handle organizational data regardless of format or location.
2. Covers all information systems, cloud services, endpoints, and collaboration platforms including the cloud productivity platform, collaboration platform, file storage, email platform, cloud access security broker (CASB), and endpoints.
3. Includes protection of AI datasets, models, and outputs containing classified or sensitive content.
4. Applies to all data classified under the 5-level Data Classification Model.

---

## 3. Governance

| Role | Responsibility |
|---|---|
| Chief Information Officer (CIO) | Executive sponsor; ensures that DLP aligns with enterprise risk and compliance objectives |
| Chief Information Security Officer (CISO) | Accountable for DLP programme design, governance, monitoring, and continual improvement |
| DLP Administrator / Security Engineer | Manages enterprise DLP platform configurations, monitors alerts, and maintains the DLP workbook |
| Security Operations Centre (SOC) | Triages alerts, investigates events, and coordinates incident response |
| Data Owners | Ensure that classification accuracy and authorize exceptions or overrides |
| Compliance and Legal | Validate DLP policies for regulatory, contractual, and privacy obligations |
| End Users | Handle information responsibly and comply with DLP policy prompts and awareness requirements |

---

## 4. Data Classification Labels

The organization applies a 5-level Data Classification Model. DLP controls are calibrated to each level.

| Level | Definition | Sharing Restrictions |
|---|---|---|
| Public | Approved for open distribution | May be freely shared without restriction |
| Controlled | May be shared externally on demand where disclosure poses low risk | Shareable with external parties under appropriate context without NDA |
| Internal | Restricted to employees and authorized contractors | Limited to internal systems and approved collaboration tools |
| Confidential | Sensitive business, legal, financial, or personal data (PII, PHI, trade secrets) | Restricted to explicitly authorized individuals; external release only under NDA |
| Restricted | Top-tier data: merger plans, executive communications, system credentials | Strictly controlled; additional audit trail, DLP enforcement, and PAM integration apply |

---

## 5. DLP Protection Framework

### 5.1 Data States

| Data State | Description | Primary Controls |
|---|---|---|
| Data at Rest | Stored data on systems, repositories, and cloud storage | Enterprise DLP platform, information protection scanner, auto-labelling, encryption |
| Data in Use | Data being processed on endpoints, browsers, and collaboration tools | Endpoint DLP agents, browser-based DLP, insider risk adaptive protection |
| Data in Motion | Data transmitted via email, collaboration platform, web upload, or external sharing | Email and collaboration platform DLP, CASB, Conditional Access |

### 5.2 Adaptive Enforcement by Classification Level

| Classification Level | Enforcement Action |
|---|---|
| Public | Alert-only |
| Controlled | Alert-only |
| Internal | Monitor with optional user override |
| Confidential | Block and log |
| Restricted | Block, encrypt, and generate SOC alert |

---

## 6. DLP Architecture and Implementation

1. **Core Platform:** The enterprise DLP platform is integrated with the CASB. Detection logic uses built-in and custom Sensitive Information Types (SITs) and sensitivity labels tied to classification levels.
2. **SIEM Integration:** DLP events feed into the SIEM for correlation. Alerts automatically open incident tickets for SOC triage.
3. **Sensitivity Labels:** Applied across the cloud productivity platform, email platform, and collaboration and file storage platform to enforce classification-aligned controls at the point of creation and sharing.
4. **Insider Risk:** Adaptive protection connects insider risk signals to DLP enforcement, dynamically tightening controls for elevated-risk users.

---

## 7. Monitoring and Reporting

### 7.1 Incident Logging

- DLP incidents are logged centrally within the enterprise DLP platform and CASB.
- All incidents are correlated in the SIEM and linked to associated tickets.

### 7.2 Key Performance Indicators

| Metric | Target |
|---|---|
| False positive rate | < 5% |
| Recurring violations per quarter | < 10% |
| Mean time to resolution (MTTR) | < 5 business days |

### 7.3 Reporting Cadence

- Key metrics tracked: incidents per classification level; false positive and negative rates; mean time to identify (MTTI) and MTTR.
- Quarterly DLP metrics reviewed by the CISO and presented to the executive risk committee (ERC).

---

## 8. Framework Alignment

| Framework | Reference | Topic |
|---|---|---|
| ISO/IEC 27002:2022 | §8.10 to 8.11 | Data Leakage Prevention |
| ISO/IEC 27701:2019 | §8.9 | Privacy Incident Management |
| COBIT 2025 | DSS05.03 | Protect Against Data Leakage |
| CSA CCM v5 | DSP-04 | Data Leakage Prevention |
| NIST SP 800-53 Rev. 5 | SI-4, SC-7 | System Monitoring and Boundary Protection |

---

*This document is released under the CC0 1.0 Universal Public Domain Dedication. No rights reserved.*



**End of Document**
