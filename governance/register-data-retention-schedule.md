# Data Retention Schedule

**Document Title:** Data Retention Schedule\
**Document Type:** Register\
**Version:** 1.0.20\
**Date:** 2026-07-25\
**Owner:** Data Protection Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`governance/standard-records-retention-and-destruction.md`](standard-records-retention-and-destruction.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../compliance/policy-legal-and-regulatory-compliance.md)\
**Classification:** Public\
**Category:** Governance\
**Review Frequency:** Annual and upon material regulatory or operational change\
**Repository Path:** [`governance/register-data-retention-schedule.md`](register-data-retention-schedule.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register defines the mandatory retention periods for each category of organizational data and records. It implements the Records Retention and Destruction Standard and supports the organization's compliance with applicable privacy laws (GDPR, PIPEDA, Quebec Law 25, UK GDPR, LGPD, PIPL), regulatory requirements, and contractual obligations.

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
| Security incident records | 7 years | Regulatory and legal requirements; aligned to the forensic-evidence minimum in [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) Section 8 and the privacy-breach row's floor (a privacy breach is a security-incident subclass) |
| Penetration test reports | 5 years | Compliance evidence |
| Vulnerability scan results | 3 years | Compliance and audit evidence |
| CAPA records | 7 years after closure | Quality management; audit evidence; matches [`compliance/procedure-capa.md`](../compliance/procedure-capa.md) §12 (Evidence retention) canonical 7-year mandate; preserves the audit-evidence chain with control-testing-evidence retention (7y) |
| SIEM event logs (including cloud platform activity logs forwarded into the SIEM) | 1 year hot + 2 years cold | Security investigation and compliance. This row is the authoritative retention for activity-log events forwarded from cloud platforms; the cloud platform's own 90-day minimum (see [`operations/standard-cloud-security-configuration-baseline.md`](../operations/standard-cloud-security-configuration-baseline.md) §6.3) is the platform-side forwarding floor, not a full retention figure. |

### 4. Privacy and personal data records

| Record Type | Retention Period | Legal Basis / Rationale |
| --- | --- | --- |
| Privacy impact assessments | 7 years, or 5 years after associated system decommission, whichever is longer | GDPR; PIPEDA accountability; matches the Step 6 record-keeping minimum in [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../privacy/procedure-privacy-impact-and-cross-border-transfer.md) |
| Data subject access request records | 3 years | GDPR Article 30; accountability |
| Consent records | Duration of processing + 3 years | GDPR Article 7 |
| Privacy breach notifications | 7 years | GDPR; PIPEDA; regulatory requirements; matches the breach-evidence minimum in [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) Section 9.2 |
| Processing records (Article 30 ROPA) | Active + 5 years | GDPR Article 30 |

### 5. Audit and compliance records

| Record Type | Retention Period | Legal Basis / Rationale |
| --- | --- | --- |
| Internal audit reports | 7 years | ISO 19011; compliance evidence; matches [`compliance/standard-internal-audit.md`](../compliance/standard-internal-audit.md):360 §8.3 (Evidence retention) canonical 7-year mandate for audit working papers, evidence, draft findings, management responses, and final reports |
| External audit and certification records | Certification period + 5 years | ISO/IEC 27001; certification requirements |
| Regulatory correspondence | 7 years | Legal and regulatory requirements |
| Compliance attestations | 5 years | Compliance evidence |
| Control testing evidence | 7 years | Audit and certification support; aligns with Sarbanes-Oxley §103 audit-evidence retention and the records-retention standard's 7-year financial / legal / compliance domain default; matches the 3.5 evidence-retention statement in [`compliance/procedure-control-testing.md`](../compliance/procedure-control-testing.md) |

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
| Model cards and validation reports | Model decommission + 5 years, or 10 years where either EU AI Act keeping period applies (for Article 11 technical documentation of a high-risk system, 10 years after that SYSTEM is placed on the market or put into service; for Annex XI technical documentation of a general-purpose AI model, 10 years after that MODEL is placed on the market), whichever is longer | The 5-year figure is the organization's own model-artefact floor: no provision of the EU AI Act anchors any retention obligation to decommission, end of life, or withdrawal, so the Act is not its source. The statutory floor is Article 18(1), which requires a PROVIDER (Article 3(3)) of a high-risk system (Article 6) to keep the Article 11 technical documentation, the Article 17 quality-management-system documentation, notified-body decisions, and the Article 47 EU declaration of conformity at the disposal of national competent authorities for 10 years after the system is placed on the market or put into service. Validation reports sit in that set expressly (Annex IV item 2(g), test logs and test reports); a model card sits in it only as the carrier of Annex IV items 1, 3, and 4, since the Act's sole use of the term is the non-binding recital 89. The duty follows the provider role: it reaches a distributor, importer, deployer, or third party that becomes a provider under Article 25(1), and the provider's representative in the Union under Article 22(3)(b). An importer's own 10-year set (Article 23(5)) is narrower and excludes the technical documentation. **The Act has a SECOND 10-year clock and this row reaches it.** For a general-purpose AI model, the documentation set is ANNEX XI rather than Annex IV and the anchor is the MODEL being placed on the market rather than the system: Article 53(1)(a) imposes the documentation duty on the GPAI-model provider without stating a period, and Article 54(3)(b) states the 10 years expressly, as a task the provider's Union representative must be mandated to perform: it must KEEP A COPY of the Annex XI documentation for 10 years after the model is placed on the market. The provider's own duty rests on Article 53(1)(a), which obliges it to draw up and KEEP UP TO DATE the technical documentation of the model, a duty it could not discharge on destroyed documentation; Article 54(2) (the provider `shall` enable its representative to perform the mandated tasks, in the Act's wording) and Article 54(3)(c) (the representative must supply that documentation to the AI Office on a reasoned request) corroborate it. The route matters: Article 54(3)(b) binds the REPRESENTATIVE and speaks of its own copy, so it does not by itself stop a provider destroying the master. This matters here specifically because the corpus makes a model card the GPAI documentation vehicle: [`ai/framework-ai-model-documentation-and-transparency.md`](../ai/framework-ai-model-documentation-and-transparency.md) states that a GPAI provider satisfies the Model Documentation Form by maintaining an extended model card. Where the provider is established in the Union and appoints no representative, the Act states no period and the organization's own floor governs. Composed as a floor rather than a replacement so the period is never shortened for a long-lived model. ISO/IEC 42001 accountability |
| AI Impact Assessments | 7 years, or 5 years after associated system decommission, whichever is longer | The organization's canonical assessment-retention floor, informed by the EU AI Act Article 9 risk-management obligations (which prescribe no retention period); matches the Step 6 record-keeping minimum in [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../privacy/procedure-privacy-impact-and-cross-border-transfer.md) (which covers the PIA/AI-IA report); the system anchor is deliberate: an impact assessment attaches to the AI system, and a system outlives routine model swaps (the adjacent model-decommission rows are model-artefact records) |
| AI audit reports | 7 years, or 5 years after the associated system's decommission, whichever is longer | ISO/IEC 42001; regulatory compliance; the [`compliance/policy-compliance-and-audit-management.md`](../compliance/policy-compliance-and-audit-management.md) Section 4.7.1 seven-year audit-records floor governs, composed with the AI-Systems domain minimum in [`governance/standard-records-retention-and-destruction.md`](standard-records-retention-and-destruction.md) Section 5 (5 years post-decommission), so neither source is weakened for any system lifetime; matches the Section 5.4 retention statement in [`ai/procedure-ai-audit.md`](../ai/procedure-ai-audit.md) |
| Training data provenance records | Model decommission + 5 years, or 10 years where either EU AI Act keeping period applies (Article 11 / Annex IV for a high-risk system, anchored to the SYSTEM; Annex XI for a general-purpose AI model, anchored to the MODEL), whichever is longer | As with the adjacent model-artefact row, the 5-year figure is the organization's own floor and the Act anchors nothing to decommission. Training-data provenance sits inside the Article 11 set EXPRESSLY: Annex IV item 2(d) requires information about the provenance of the data sets, so for a high-risk system these records are within the Article 18(1) 10-year documentation-keeping duty described in the row above. They are equally inside the general-purpose-model set: Annex XI Section 1, point 2(c) requires information on the data used for training, testing, and validation (the point number matters: Section 1 contains two items lettered (c), and point 1(c) is the unrelated date-of-release item), including the type and PROVENANCE of the data and the curation methodologies, so the Article 54(3)(b) 10-year period described in the row above reaches these records too. Composed as a floor rather than a replacement. Bias accountability |
| AI incident records | 5 years, or 5 years after the associated system's decommission, whichever is longer | EU AI Act; regulatory requirements; composed with the AI-Systems domain minimum in [`governance/standard-records-retention-and-destruction.md`](standard-records-retention-and-destruction.md) Section 5 (5 years post-decommission), the adjacent composed rows' proven shape, so an incident record on a long-lived system is not destroyed while the system still runs |
| AI decision and detection logs (inputs, outputs, model version, confidence scores) | 7 years, or 5 years after the associated system's decommission, whichever is longer | The organization's canonical AI-audit-log floor, informed by ISO/IEC 42001's retention requirements and the EU AI Act's documentation and log-keeping obligations (Articles 18 and 19), neither of which prescribes the 7-year figure; AI-decision accountability (longer than the general SIEM event tier); composed with the AI-Systems domain minimum in [`governance/standard-records-retention-and-destruction.md`](standard-records-retention-and-destruction.md) Section 5, so the canonical 7-year floor is preserved for every system lifetime |

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
| Supplier audit reports | 7 years | Compliance and certification support; the [`compliance/policy-compliance-and-audit-management.md`](../compliance/policy-compliance-and-audit-management.md) Section 4.7.1 seven-year audit-records floor governs; matches the Step 4 report-retention statement in [`supply-chain/procedure-supplier-audit.md`](../supply-chain/procedure-supplier-audit.md) |
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
| COBIT 2019 | APO14: Managed Data | Data governance and retention |

---

**End of Document**
