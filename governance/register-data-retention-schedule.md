# Data Retention Schedule

**Document Title:** Data Retention Schedule 
**Document Type:** Register 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Privacy Officer 
**Approving Authority:** Chief Information Officer 
**Related Documents:** [`governance/standard-records-retention-and-destruction.md`](standard-records-retention-and-destruction.md), [`governance/policy-governance-and-risk-management.md`](policy-governance-and-risk-management.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../compliance/policy-legal-and-regulatory-compliance.md) 
**Classification:** Public 
**Category:** Governance 
**Review Frequency:** Annual and upon material regulatory or operational change 
**Repository Path:** [`governance/register-data-retention-schedule.md`](register-data-retention-schedule.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This register defines the mandatory retention periods for each category of organizational data and records. It implements the Records Retention and Destruction Standard and ensures that compliance with applicable privacy laws (GDPR, PIPEDA, Quebec Law 25, UK GDPR, LGPD, PIPL), regulatory requirements, and contractual obligations.

---

## Principles

1. Data is retained only as long as necessary for its stated purpose.
2. Retention periods are set to the minimum required by law, regulation, or business need.
3. Data that has reached its retention limit is destroyed promptly unless subject to a legal hold.
4. Legal holds override all retention schedules until the hold is lifted.
5. Destruction is documented and irreversible.

---

## Data retention schedule

### 1. Human resources and employment records

| Record Type | Retention Period | Legal Basis / Rationale |
| --- | --- | --- |
| Employee personnel files | 7 years after employment ends | Employment law; tax and payroll obligations |
| Payroll and compensation records | 7 years | Tax and audit requirements |
| Background screening records | Duration of employment + 3 years | Personnel security; legal defensibility |
| Onboarding and offboarding checklists | Duration of employment + 3 years | Audit evidence |
| Disciplinary and grievance records | Resolution + 5 years | Legal defensibility |
| Training completion records | Duration of employment + 3 years | Compliance evidence |

### 2. Financial and accounting records

| Record Type | Retention Period | Legal Basis / Rationale |
| --- | --- | --- |
| General ledger and financial statements | 7 years | Tax and audit requirements |
| Invoices and purchase orders | 7 years | Tax and audit requirements |
| Contracts and agreements | Term + 7 years | Legal and contractual obligations |
| Insurance records | Term + 7 years | Legal defensibility |

### 3. Information security records

| Record Type | Retention Period | Legal Basis / Rationale |
| --- | --- | --- |
| Access logs (user authentication) | 1 year | Security monitoring; incident investigation |
| Privileged access session logs | 2 years | Audit and forensic requirements |
| Security incident records | 5 years | Regulatory and legal requirements |
| Penetration test reports | 5 years | Compliance evidence |
| Vulnerability scan results | 3 years | Compliance and audit evidence |
| CAPA records | 5 years after closure | Quality management; audit evidence |
| SIEM event logs | 1 year hot + 2 years cold | Security investigation and compliance |

### 4. Privacy and personal data records

| Record Type | Retention Period | Legal Basis / Rationale |
| --- | --- | --- |
| Privacy impact assessments | 5 years after associated system decommission | GDPR; PIPEDA accountability |
| Data subject access request records | 3 years | GDPR Article 30; accountability |
| Consent records | Duration of processing + 3 years | GDPR Article 7 |
| Privacy breach notifications | 5 years | GDPR; PIPEDA; regulatory requirements |
| Processing records (Article 30 ROPA) | Active + 5 years | GDPR Article 30 |

### 5. Audit and compliance records

| Record Type | Retention Period | Legal Basis / Rationale |
| --- | --- | --- |
| Internal audit reports | 5 years | ISO 19011; compliance evidence |
| External audit and certification records | Certification period + 5 years | ISO 27001; certification requirements |
| Regulatory correspondence | 7 years | Legal and regulatory requirements |
| Compliance attestations | 5 years | Compliance evidence |
| Control testing evidence | 5 years | Audit and certification support |

### 6. Governance and GRC records

| Record Type | Retention Period | Legal Basis / Rationale |
| --- | --- | --- |
| Board and committee minutes | Permanent | Corporate governance |
| Policy and standards versions | Superseded version + 7 years | Audit and legal reference |
| Risk register entries | Closed + 5 years | Risk governance; audit trail |
| Business continuity test records | 5 years | ISO 22301; certification evidence |
| DR test records | 5 years | Compliance and insurance requirements |

### 7. AI governance records

| Record Type | Retention Period | Legal Basis / Rationale |
| --- | --- | --- |
| Model cards and validation reports | Model decommission + 5 years | EU AI Act; ISO 42001 accountability |
| AI Impact Assessments | Model decommission + 5 years | EU AI Act Article 9 |
| AI audit reports | 5 years | ISO 42001; regulatory compliance |
| Training data provenance records | Model decommission + 5 years | EU AI Act; bias accountability |
| AI incident records | 5 years | EU AI Act; regulatory requirements |

### 8. BASC and trade compliance records

| Record Type | Retention Period | Legal Basis / Rationale |
| --- | --- | --- |
| Customs declarations and entries | 7 years | CBSA; HMRC; WCO SAFE |
| BASC audit records and certifications | Certification period + 7 years | BASC International Standard v6 |
| Cargo manifest and chain of custody | 7 years | CTPAT; NEEC; AEO compliance |
| Personnel security screening (trade) | Duration of employment + 5 years | BASC v6 Chapter 6 |
| Cryptographic key audit records (trade) | 7 years | BASC v6; WCO SAFE |

### 9. Supplier and third-party records

| Record Type | Retention Period | Legal Basis / Rationale |
| --- | --- | --- |
| Supplier contracts | Term + 7 years | Legal and contractual obligations |
| Supplier security assessments | Assessment date + 5 years | Supply chain security governance |
| Supplier audit reports | 5 years | Compliance and certification support |
| Data processing agreements | Term + 5 years | GDPR Article 28 |

---

## Legal holds

When litigation, regulatory investigation, or audit is anticipated or underway:

1. The Legal Counsel or Compliance Officer issues a Legal Hold Notice.
2. All retention schedule timers for affected records are suspended.
3. Affected records are preserved and clearly labelled as subject to legal hold.
4. Destruction of held records is prohibited until the Legal Counsel formally releases the hold.
5. Legal hold status is tracked in the GRC platform.

---

## Destruction

Records reaching the end of their retention period are destroyed per the Records Retention and Destruction Standard:
- Electronic records: secure deletion using approved methods (NIST SP 800-88 or equivalent).
- Physical records: cross-cut shredding or certified destruction service.
- Destruction is documented with: record type, volume, destruction date, method, and authorizing role.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| GDPR (2018) | Articles 5, 17, 30 | Personal data retention and deletion |
| PIPEDA / Quebec Law 25 | Accountability and retention | Canadian privacy obligations |
| UK GDPR | Articles 5, 17 | UK retention requirements |
| ISO/IEC 27001:2022 | Annex A.5.33: Protection of Records | Records protection and retention |
| ISO/IEC 27002:2022 | §5.33 to 5.34 | Records management controls |
| BASC International Standard v6 | Chapter 3: Document Retention | Trade record retention |
| COBIT 2025 | APO14: Manage Data | Data governance and retention |

---

**End of Document**
