# Data Classification and Handling Standard

**Document Title:** Data Classification and Handling Standard 
**Document Type:** Standard 
**Version:** 1.3.1 
**Date:** 2026-05-28 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md), [`compliance/register-global-regulatory-applicability.md`](../compliance/register-global-regulatory-applicability.md) 
**Classification:** Public 
**Category:** Information Security 
**Review Frequency:** Annual and upon material threat, framework, or regulatory change 
**Repository Path:** [`security/standard-data-classification-and-handling.md`](standard-data-classification-and-handling.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

This standard defines the classification, labelling, protection, retention, and destruction requirements for all information assets.

---

## Purpose

To ensure that consistent handling of information according to its sensitivity, regulatory obligations, and business impact, while supporting confidentiality, integrity, and availability. Aligns with ISO/IEC 27002:2022 §§5.12 to 5.15, COBIT 2019 DSS05, CSA CCM v4.1 DSP-02, GDPR Article 32, ISO/IEC 27701:2019 §8.8, and BASC International Standard (v6 2023).

---

## Scope

1. Applies to all information assets owned, controlled, or processed, including digital and physical records, databases, documents, emails, collaboration tools, backups, and AI datasets and model artifacts.
2. Applies to all employees, contractors, suppliers, and partners with access to systems or data.
3. Covers all storage and communication media: servers, endpoints, cloud, and mobile devices.
4. Encompasses regional data handling obligations including BASC compliance for Latin American logistics and trade data.

---

## Governance and accountability

| Role | Responsibility |
| --- | --- |
| CIO | Approves data classification framework and ensures that enterprise-wide adoption. |
| CISO | Enforces encryption, labelling, and protection controls. |
| Data Owners / Department Heads | Classify and label data assets according to business and regulatory sensitivity. |
| IT Operations / Cloud Administrators | Implement and maintain automated labelling, DLP, and encryption solutions. |
| Privacy Officer | Ensures that alignment with privacy and data protection laws. |
| AI Governance Council | Oversees classification and protection of AI datasets and model data. |

Sector-conditional roles (for example, a BASC Regional Compliance Officer who ensures that classification of customs, trade, and cargo data meets BASC confidentiality standards) apply where the organisation participates in a covered sector programme; see [`sectors/`](../sectors/).

---

## Data classification levels

| Classification | Definition | Handling Requirements | Examples |
| --- | --- | --- | --- |
| **Public** | Information approved for open distribution. | No restriction. Public dissemination allowed. | Press releases, marketing materials, published reports. |
| **Controlled** | Information that may be shared externally at discretion; disclosure poses low risk. | Share externally under context; management awareness required. | Product overviews, proposals, general client communications. |
| **Internal** | Restricted to employees and authorized contractors; external sharing requires approval or NDA. | Store in internal systems; encryption optional. | Internal procedures, reports, project data. |
| **Confidential** | Contains sensitive business, financial, or personal data. Unauthorized disclosure may cause harm. | Encryption at rest and in transit; access by authorization only. | Contracts, client data, payroll, incident reports. |
| **Restricted** | Highest sensitivity; includes trade secrets, privileged data, or AI model code. | Strong encryption, strict access control, PAM enforcement, audit logging. | Source code, credentials, merger data, BASC customs data, AI model weights. |

---

## 1. Classification and labelling

1.1 Data Owners are responsible for classifying data upon creation or receipt.
1.2 All digital files must display classification labels within document metadata, filenames, or headers.
1.3 Automated classification and handling enforcement via the data classification platform is required (cloud productivity platform).
1.4 Physical records must be stamped or marked with classification level on each page or cover.
1.5 System-generated or AI-derived data inherits the classification of its source unless explicitly reclassified.

---

## 2. Handling requirements

| Control Area | Requirement |
| --- | --- |
| Storage | Use encrypted storage for Confidential and Restricted data (AES-256). |
| Transmission | Use TLS 1.3 or stronger encryption for data transfers. |
| Access Control | Grant least-privilege access based on role. |
| Collaboration | Share via approved platforms with classification awareness. |
| Logging and Monitoring | Record all access to Restricted and Confidential data in the SIEM. |
| Printing and Disposal | Print only when necessary; shred Confidential or higher data after use. |
| Cloud DLP | Enforce classification-based DLP policies across cloud productivity and storage platforms. |

---

## 3. AI data classification and handling

3.1 AI datasets, model artifacts, and logs must follow equivalent or stricter handling than Confidential data.
3.2 Datasets containing personal or proprietary information must be anonymized, pseudonymized, or encrypted.
3.3 AI model weights, training scripts, and inference APIs classified as Restricted must reside in secure, access-controlled repositories.
3.4 Model outputs with potential regulatory or ethical implications (e.g., automated decision logs) must be preserved per the Records Retention Standard.
3.5 For AI systems supporting BASC or customs automation:
- Training and operational data must comply with BASC confidentiality controls and ISO 28000 trade data requirements.
- AI model audit logs must be tamper-proof and available for customs review.

---

## 4. Retention and destruction

4.1 Data retention periods are defined in the Records Retention and Destruction Standard.
4.2 Upon expiration of retention, data must be securely destroyed via:
- Cryptographic erasure for digital data (per NIST SP 800-88).
- Cross-cut shredding for physical media.
4.3 Certificates of Destruction must be logged and archived for seven years.
4.4 AI datasets and BASC trade data must undergo destruction validation to ensure that data lineage tracking integrity.

---

## 5. Encryption requirements

| Classification | Encryption Requirement |
| --- | --- |
| Public | Not required. |
| Controlled | Optional; required if transmitted externally. |
| Internal | Encrypt when stored on portable devices. |
| Confidential | Mandatory (AES-256 at rest, TLS 1.3 in transit). |
| Restricted | Mandatory; hardware security modules (HSMs) and key rotation every 90 days. |

Encryption keys must be managed under the Encryption and Key Management Policy.

---

## 6. Sector-programme data handling overlays

Where the organisation participates in a sector programme that imposes additional handling requirements on programme-specific data (for example, BASC for customs, cargo, and personnel data classified as Restricted by default; healthcare regulation for PHI; financial-services regulation for payment-card or fraud data), the corresponding sector annex states the additional classification, storage, physical-copy, and incident-treatment requirements. See [`sectors/`](../sectors/).

---

## 7. Monitoring and compliance

7.1 The CISO and Compliance Manager perform quarterly reviews of classification and handling adherence.
7.2 Automated DLP reports must be analyzed monthly to detect potential misclassifications or policy breaches.
7.3 Noncompliance or mishandling triggers investigation and remediation under the Corrective and Preventive Action Procedure.
7.4 Annual ISO and BASC audits verify adherence to classification standards and encryption controls.

---

## Framework alignment

| Control Area | ISO/IEC 27002 | COBIT 2019 | CSA CCM v4.1 | Legal / Regulatory |
| --- | --- | --- | --- | --- |
| Classification and labelling | §§5.12 to 5.15 | DSS05 | DSP-02 | GDPR Art. 32, CPPA |
| Encryption | §8.24 | DSS05.03 | CEK-01 to 21 | BASC §6 |
| Retention and disposal | §8.10 | DSS05 | DSP-07 | ISO/IEC 27701 §8.8 |
| AI data handling | N/A | DSS05.06 | N/A | AIDA, PIPEDA |
| Trade data (BASC) | N/A |: | N/A | BASC v6, ISO 28000 |



**End of Document**
