# Records Retention and Destruction Standard

**Document Title:** Records Retention and Destruction Standard 
**Document Type:** Standard 
**Version:** 1.3.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md), [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md) 
**Classification:** Public 
**Category:** Governance 
**Review Frequency:** Annual or as required by regulatory or framework changes 
**Repository Path:** [`governance/standard-records-retention-and-destruction.md`](standard-records-retention-and-destruction.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This standard establishes controls, retention schedules, destruction methods, and documentation requirements for managing information and records throughout their lifecycle. It ensures that records, both physical and digital, are retained, secured, and disposed of in compliance with legal, regulatory, contractual, and operational requirements, including those governing privacy, AI governance, supply-chain trade compliance (BASC), and data protection.

---

## Scope

1. Applies to all organizational records including business documents, electronic files, system logs, datasets, AI model artifacts, and contractual records.
2. Covers all systems, storage media, and cloud environments that hold information subject to regulatory, audit, or contractual retention obligations.
3. Applies globally across all entities and regional subsidiaries, including BASC-governed logistics and customs operations.
4. Includes AI-specific content such as model training datasets, testing results, and explainability documentation.

---

## Governance

| Role | Responsibility |
|---|---|
| **Chief Information Officer (CIO)** | Provides executive oversight of information lifecycle management and ensures that resources for compliance. |
| **Chief Information Security Officer (CISO)** | Enforces technical and security controls for data retention, backup, and secure destruction. |
| **Compliance Manager / Records Officer** | Maintains the Records Retention Schedule (RRS), tracks retention obligations, and coordinates audits. |
| **Department Heads / Data Owners** | Classify and manage records according to business and regulatory requirements. |
| **Legal Counsel** | Validates retention periods based on jurisdictional and contractual obligations. |
| **AI Governance Council (AIGC)** | Defines retention and destruction controls for AI datasets, model versions, and audit logs. |
| **Regional Compliance Officers** | Ensure that BASC-specific retention for customs, trade, and cargo-related records. |

---

## Records classification

| Classification | Examples | Minimum Retention |
|---|---|---|
| **Public** | Marketing materials, published financials | 1 year |
| **Controlled** | Non-sensitive client communications, reference documentation | 3 years |
| **Internal** | Internal reports, operational procedures, user manuals | 5 years |
| **Confidential** | Contracts, HR files, financial data, personal data | 7 years or as required by applicable law |
| **Restricted** | Trade secrets, encryption keys, M&A files, AI model source code | 10 years or indefinite with periodic review |

---

## Section 1: records retention schedule

The Records Retention Schedule (RRS) defines minimum retention periods based on:

- Legal or regulatory mandates.
- Contractual obligations.
- Business or audit requirements.
- Data protection laws including GDPR, CPPA, and LGPD.

### Domain-specific minimum retention periods

| Domain | Minimum Retention |
|---|---|
| Corporate Governance | 7 years |
| Financial | 7 years |
| Human Resources | 7 years after separation |
| IT / Security | 1 to 3 years |
| Legal and Compliance | 7 years |
| Privacy / Data Subject Requests (DSR) | 2 years post-closure |
| AI Systems | 5 years post-decommission |
| BASC Trade and Customs | 5 years or per applicable BASC chapter policy |

> Retention periods longer than 7 years require written approval from Legal Counsel.

---

## Section 2: secure storage and access

Records must be stored in secure, access-controlled systems with encryption applied at rest and in transit. Requirements include:

- Cloud-hosted storage must conform to ISO 27018 and CSA CCM DSP controls.
- Access must follow least-privilege principles as defined in the Access Control Procedure.
- Critical records require multi-region backup and tamper-proof logging.

---

## Section 3: retention hold and litigation freeze

When a record is subject to audit, investigation, or litigation, a retention hold must be applied immediately. The following controls apply:

1. The Compliance Manager documents the hold in the Records Register and notifies the relevant Data Owner.
2. Records under hold cannot be altered or deleted until Legal Counsel formally lifts the restriction.
3. The hold status is tracked in the Records Register until closure.

---

## Section 4: secure destruction

Upon expiration of the applicable retention period and confirmation that no active hold exists, records must be securely destroyed using an approved method.

### Acceptable destruction methods

| Media Type | Accepted Methods |
|---|---|
| **Paper / Physical** | Cross-cut shredding or contracted secure disposal service |
| **Electronic / Digital** | Cryptographic erasure, secure overwrite per NIST SP 800-88, or physical drive destruction |

### Destruction documentation

All destruction actions must be logged in the Destruction Register. Each entry must include:

- Record identifier and classification level.
- Destruction method applied.
- Date of destruction.
- Role of responsible person.
- Witness signature (required for physical destruction).

Certificates of Destruction must be retained for a minimum of 7 years.

---

## Section 5: AI dataset and model record retention

All AI training datasets, test results, and model versions must be retained to support audit and reproducibility obligations per ISO/IEC 42001 §9. Required records include:

- Dataset lineage and source validation documentation.
- Model architecture and configuration files.
- Training parameters, bias testing results, and validation metrics.
- Explainability reports and decision logs.

Retention ensures that traceability under EU AI Act Annex IV, OECD AI Principles 2026, and Canada AIDA §29. AI datasets containing personal data must follow anonymization or deletion requirements upon expiry of the retention period, in accordance with ISO/IEC 27701 §8.8.

---

## Section 6: BASC trade and customs records

For operations governed by BASC International Standards in Latin America, retention must include:

- Cargo and shipment manifests.
- Inspection logs and security seal records.
- Personnel background verification records.
- Customs communications and export declarations.

Minimum retention is 5 years or as required by the applicable national customs authority. Once retention obligations expire, trade data must be destroyed using the approved secure methods defined in Section 4.

---

## Section 7: monitoring and compliance

### Quarterly reviews

Quarterly reviews confirm:

- Timely destruction of records whose retention period has expired.
- No records deleted while subject to an active hold.
- Compliance with privacy and AI recordkeeping standards.

Non-compliance identified during reviews triggers investigation under the Corrective and Preventive Action (CAPA) Procedure.

### Annual audit

Annual audits verify:

- Retention practices across all domains.
- Evidence of destruction and completeness of the Destruction Register.
- System access logs and access control compliance.

---

## Framework alignment

| Framework | Relevance |
|---|---|
| ISO 15489:2016 | Records Management |
| ISO/IEC 27701:2019 §8.8 | Data Retention and Deletion |
| COBIT 2025 DSS01 | Manage Operations |
| CSA CCM v5 DSP-02 | Data Retention, Disposal, and Destruction |
| ISO/IEC 42001:2023 §9 | AI Recordkeeping and Traceability |
| EU AI Act Annex IV | AI System Documentation |
| BASC International Standard v6 2023 | Supply-Chain and Customs Records Retention |
| WCO SAFE Framework 2021 | Trade Compliance Documentation |

---

*This document is released under the CC0 1.0 Universal public domain dedication. No rights reserved.*



**End of Document**
