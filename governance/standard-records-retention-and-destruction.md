# Records Retention and Destruction Standard

**Document Title:** Records Retention and Destruction Standard\
**Document Type:** Standard\
**Version:** 1.4.11\
**Date:** 2026-07-02\
**Owner:** Chief Information Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md), [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md)\
**Classification:** Public\
**Category:** Governance\
**Review Frequency:** Annual or as required by regulatory or framework changes\
**Repository Path:** [`governance/standard-records-retention-and-destruction.md`](standard-records-retention-and-destruction.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard establishes controls, retention schedules, destruction methods, and documentation requirements for managing information and records throughout their lifecycle. It ensures that records, both physical and digital, are retained, secured, and disposed of in compliance with legal, regulatory, contractual, and operational requirements, including those governing privacy, AI governance, supply-chain trade compliance (BASC), and data protection.

---

## 2. Scope

1. Applies to all organizational records including business documents, electronic files, system logs, datasets, AI model artifacts, and contractual records.
2. Covers all systems, storage media, and cloud environments that hold information subject to regulatory, audit, or contractual retention obligations.
3. Applies globally across all entities and regional subsidiaries. Sector-specific retention overlays (for example, BASC trade and customs retention) apply where the organization participates in a covered programme; see [`compliance/`](../compliance/).
4. Includes AI-specific content such as model training datasets, testing results, and explainability documentation.

---

## 3. Governance and accountability

| Role | Responsibility |
|---|---|
| **Chief Information Officer (CIO)** | Provides executive oversight of information lifecycle management and ensures that resources for compliance are provided. |
| **Chief Information Security Officer (CISO)** | Enforces technical and security controls for data retention, backup, and secure destruction. |
| **Compliance Manager / Records Officer** | Maintains the Records Retention Schedule (RRS) register operationally, tracks retention obligations, and coordinates audits. The RRS register ([`governance/register-data-retention-schedule.md`](register-data-retention-schedule.md)) is owned (accountable) by the Data Protection Officer and approved by the CIO per its metadata; this operational-maintenance role sits under that ownership. |
| **Department Heads / Data Owners** | Classify and manage records according to business and regulatory requirements. |
| **Legal Counsel** | Validates retention periods based on jurisdictional and contractual obligations. |
| **AI Governance Council (AIGC)** | Defines retention and destruction controls for AI datasets, model versions, and audit logs. |

Sector-conditional roles (for example, a BASC Regional Compliance Officer where the organization participates in BASC) apply retention controls per the relevant sector annex; see [`compliance/`](../compliance/).

---

## 4. Records classification

| Classification | Examples | Minimum Retention |
|---|---|---|
| **Public** | Marketing materials, published financials | 1 year |
| **Controlled** | Non-sensitive client communications, reference documentation | 3 years |
| **Internal** | Internal reports, operational procedures, user manuals | 5 years |
| **Confidential** | Contracts, HR files, financial data, personal data | 7 years or as required by applicable law |
| **Restricted** | Trade secrets, encryption keys, M&A files, AI model source code | 10 years or indefinite with periodic review |

---

## 5. Records retention schedule

The Records Retention Schedule (RRS) defines minimum retention periods based on:

- Legal or regulatory mandates.
- Contractual obligations.
- Business or audit requirements.
- Data protection laws including GDPR, PIPEDA, and LGPD.

### 5.1 Domain-specific minimum retention periods

| Domain | Minimum Retention |
|---|---|
| Corporate Governance | 7 years |
| Financial | 7 years |
| Human Resources | 7 years after separation |
| IT / Security | Tiered by record class per [`register-data-retention-schedule.md`](register-data-retention-schedule.md) (authoritative; 1 to 7 years, e.g. access logs 1 year, security incident records 5 years, AI decision and detection logs 7 years) |
| Legal and Compliance | 7 years |
| Privacy / Data Subject Requests (DSR) | 3 years post-closure (per [`register-data-retention-schedule.md`](register-data-retention-schedule.md), Data subject access request records) |
| AI Systems | 5 years post-decommission |

Sector-specific retention categories (for example, trade and customs records under BASC, healthcare records under HIPAA, financial-services records under sector-specific regulation) apply where the organization participates in a covered programme; see [`compliance/`](../compliance/).

> Retention periods longer than 7 years require written approval from Legal Counsel.

---

## 6. Secure storage and access

Records must be stored in secure, access-controlled systems with encryption applied at rest and in transit. Requirements include:

- Cloud-hosted storage must conform to ISO 27018 and CSA CCM DSP controls.
- Access must follow least-privilege principles as defined in the Access Control Procedure.
- Critical records require multi-region backup and tamper-proof logging.

---

## 7. Retention hold and litigation freeze

When a record is subject to audit, investigation, or litigation, a retention hold must be applied immediately. The following controls apply:

1. The Compliance Manager documents the hold in the Records Register and notifies the relevant Data Owner.
2. Records under hold cannot be altered or deleted until Legal Counsel formally lifts the restriction.
3. The hold status is tracked in the Records Register until closure.

---

## 8. Secure destruction

Upon expiration of the applicable retention period and confirmation that no active hold exists, records must be securely destroyed using an approved method.

### 8.1 Acceptable destruction methods

| Media Type | Accepted Methods |
|---|---|
| **Paper / Physical** | Cross-cut shredding or contracted secure disposal service |
| **Electronic / Digital** | Cryptographic erasure, secure overwrite (IEEE 2883 Clear), or physical drive destruction |

### 8.2 Destruction documentation

All destruction actions must be logged in the Destruction Register. Each entry must include:

- Record identifier and classification level.
- Destruction method applied.
- Date of destruction.
- Role of responsible person.
- Witness signature (required for physical destruction).

Certificates of Destruction must be retained for a minimum of 7 years.

---

## 9. AI dataset and model record retention

All AI training datasets, test results, and model versions must be retained to support audit and reproducibility obligations per ISO/IEC 42001 §9. Required records include:

- Dataset lineage and source validation documentation.
- Model architecture and configuration files.
- Training parameters, bias testing results, and validation metrics.
- Explainability reports and decision logs.

Retention ensures that traceability is preserved under EU AI Act Annex IV, OECD AI Principles (2019, updated 2024), and Canada AIDA (Bill C-27 lapsed January 2025; section reference retained as a record of the proposed law). AI datasets containing personal data must follow anonymization or deletion requirements upon expiry of the retention period, in accordance with ISO/IEC 27701:2025 (privacy information management; section numbering changed in 2025 standalone revision).

---

## 10. Sector-specific retention overlays

Where the organization participates in a sector-specific programme that imposes its own retention obligations (for example, BASC for trade and logistics operations, sector-specific financial-services or healthcare regulations), the corresponding sector annex defines the additional retention categories, minimum retention periods, and destruction requirements. See [`compliance/`](../compliance/) and the sector-specific compliance annexes in [`compliance/`](../compliance/).

Sector overlays extend (do not contradict) the retention requirements defined elsewhere in this standard. Where the overlay specifies a longer retention period than the base requirement, the longer period applies.

---

## 11. Monitoring and compliance

### 11.1 Quarterly reviews

Quarterly reviews confirm:

- Timely destruction of records whose retention period has expired.
- No records deleted while subject to an active hold.
- Compliance with privacy and AI recordkeeping standards.

Non-compliance identified during reviews triggers investigation under the Corrective and Preventive Action (CAPA) Procedure.

### 11.2 Annual audit

Annual audits verify:

- Retention practices across all domains.
- Evidence of destruction and completeness of the Destruction Register.
- System access logs and access control compliance.

---

## 12. Framework alignment

| Framework | Relevance |
|---|---|
| ISO 15489:2016 | Records Management |
| ISO/IEC 27701:2025 | Data Retention and Deletion (privacy information management system; section numbering changed in 2025 standalone revision) |
| COBIT 2019 DSS01 | Manage Operations |
| CSA CCM v4.1 DSP-02 | Data Retention, Disposal, and Destruction |
| ISO/IEC 42001:2023 §9 | AI Recordkeeping and Traceability |
| EU AI Act Annex IV | AI System Documentation |

Sector-specific framework alignments (for example, BASC International Standard v6 2022 and WCO SAFE Framework 2021 for trade and customs records retention) apply where the organization participates in a covered programme; see [`compliance/`](../compliance/).

---

*This document is released under the CC BY-SA 4.0 licence. No rights reserved.*



**End of Document**
