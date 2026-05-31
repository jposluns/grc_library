# Supplier Audit Procedure

**Document Title:** Supplier Audit Procedure\
**Document Type:** Procedure\
**Version:** 1.0.2\
**Date:** 2026-05-28\
**Owner:** Supplier Risk Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/procedure-supplier-due-diligence.md`](procedure-supplier-due-diligence.md), [`supply-chain/annex-trade-and-supply-chain-continuity-controls.md`](annex-trade-and-supply-chain-continuity-controls.md), [`risk/procedure-risk-register.md`](../risk/procedure-risk-register.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md)\
**Classification:** Public\
**Category:** Supply Chain Governance | Third-Party Risk\
**Review Frequency:** Annual and upon material supplier, regulatory, or framework change\
**Repository Path:** [`supply-chain/procedure-supplier-audit.md`](procedure-supplier-audit.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure defines the process for conducting periodic audits of suppliers, vendors, and third-party service providers to verify adherence to contractual obligations, security standards, regulatory requirements, and ethical conduct principles.

It is aligned with ISO/IEC 27036-4:2016, COBIT 2019 BAI05.02, CSA CCM v4.1 STA-05, BASC International Standard v6 2023, and ENISA's ongoing AI cybersecurity work (feasibility studies and standardisation gap analyses under the EU Cybersecurity Act framework; no dedicated AI cybersecurity certification scheme has been formally published as of 2026).

---

## Scope

1. Applies to all suppliers, vendors, contractors, logistics partners, and service providers engaged by the organisation.
2. Covers both IT and non-IT suppliers, including logistics, customs, AI, and cloud service providers.
3. Applies globally, with additional regional audit requirements for BASC-certified operations in Latin America.

---

## Governance

| Role | Responsibility |
| --- | --- |
| Chief Information Officer | Provides executive oversight of the supplier audit programme and approves the annual audit plan. |
| Chief Information Security Officer | Defines audit scope for information security, privacy, and AI risk controls. |
| Procurement Director | Coordinates audit logistics, schedules audits with suppliers, and ensures that supplier cooperation. |
| Compliance and GRC Manager | Maintains the Supplier Audit Register, records audit evidence, and reports programme performance metrics. |
| Legal Counsel | Verifies adherence to contractual obligations, data protection law, trade regulations, and BASC requirements. |
| AI Governance Council | Reviews audit findings involving AI-enabled services or AI system vendors. |
| Enterprise Risk Committee | Reviews audit results, identifies systemic supplier risks, and approves remediation strategies. |

---

## Audit types and frequency

| Audit Type | Objective | Frequency |
| --- | --- | --- |
| Tier 1 Critical Suppliers | Verify compliance with ISO 27036, BASC, data privacy obligations, and AI governance controls. | Semi-annual. |
| Tier 2 High-Risk Suppliers | Assess cybersecurity posture, continuity readiness, and contractual performance. | Annual. |
| Tier 3 Moderate Suppliers | Evaluate service delivery quality and SLA performance. | Biennial. |
| Tier 4 Low-Risk Suppliers | Monitor via third-party attestations or self-assessment questionnaires. | Biennial. |

---

## Procedure

### Step 1: Audit planning and scoping

The Compliance and GRC Manager must maintain the Supplier Audit Register, recording for each supplier:

- Supplier name and primary contact role.
- Geographic region and operational jurisdiction.
- Tier classification and applicable regulatory frameworks.
- Date of last completed audit and date of next scheduled audit.
- Outstanding findings and CAPA status.

Audit scope for each engagement must be defined to cover, as applicable:

- Security, privacy, and data-handling practices.
- Business continuity and operational resilience.
- Contractual SLA adherence and performance obligations.
- AI governance controls (for AI-enabled or AI system vendors).
- Trade compliance, cargo security, and customs integrity (for BASC-regulated suppliers).

Suppliers must be formally notified of an upcoming audit at least 30 calendar days in advance. Notification must include the proposed audit scope, requested documentation, and the scheduled date range.

### Step 2: Pre-audit preparation

Prior to conducting the audit, the audit team must:

1. Review the supplier's current contracts, Data Processing Agreements (DPAs), and prior audit reports.
2. Confirm currency of applicable certificates (ISO/IEC 27001, SOC 2, BASC, AI certification where applicable).
3. Prepare an audit checklist aligned to the applicable frameworks and control families, including:
 - ISO/IEC 27036-4 Annex A controls.
 - COBIT 2019 BAI05.02 governance practices.
 - CSA CCM v4.1 STA-05 supply chain assurance controls.
 - BASC International Standard v6 2023, Sections 1 to 7 (for trade and logistics suppliers).
 - EU AI Act conformity-assessment requirements (Articles 9, 16-29) and ENISA AI cybersecurity guidance where applicable (for AI system suppliers).

### Step 3: Evaluation and scoring

Audit findings must be scored using a weighted compliance matrix. The weighting reflects the relative governance importance of each domain.

| Domain | Weighting |
| --- | --- |
| Security and Privacy | 25% |
| Operational Continuity | 20% |
| Legal and Contractual Compliance | 15% |
| AI Governance | 15% |
| BASC and Trade Security | 15% |
| ESG and Ethical Conduct | 10% |

Domain weights are adjusted to distribute proportionally when a domain is not applicable to a given supplier (e.g., AI Governance weight is redistributed for non-AI suppliers).

Overall audit scores are interpreted as follows:

| Score Range | Risk Rating | Required Action |
| --- | --- | --- |
| 90 to 100% | Fully Compliant | No mandatory corrective action; schedule next routine audit. |
| 75 to 89% | Partially Compliant | Minor corrective actions required; track in CAPA Register. |
| 60 to 74% | Moderate Risk | Improvement plan required within 30 days; follow-up review scheduled. |
| Below 60% | Noncompliant | Subject to re-audit within 60 days or suspension pending remediation. |

### Step 4: Reporting and findings management

A formal Supplier Audit Report must be issued within 15 business days of audit completion. The report must include:

- Executive summary of audit scope, methodology, and overall risk rating.
- Findings by domain, with severity classification and supporting evidence.
- Recommended corrective actions with proposed resolution timelines.
- Comparison with prior audit results where available.

All findings must be logged in the Corrective and Preventive Action (CAPA) Register. The Supplier Relationship Owner is responsible for tracking resolution progress and verifying closure of each finding. Critical or recurring findings must be escalated to the Enterprise Risk Committee.

### Step 5: Sector-programme trade-security compliance

For suppliers in scope of a sector programme (for example, BASC for Latin American logistics, customs brokerage, or cargo operations; CTPAT for US trade; AEO for EU trade), the audit must additionally confirm:

- Validity of current sector certification (for example, BASC, CTPAT, AEO) and scheduled renewal date.
- Compliance with the WCO SAFE Framework of Standards 2021.
- Compliance with ISO 28000:2022 supply chain security management requirements.
- Adequacy of cargo inspection procedures, seal integrity controls, and tamper-evidence mechanisms.
- Security of communication channels with customs authorities and regulatory systems.

Sector-programme compliance metrics must be reported to the sector-conditional role defined by the relevant sector annex (for example, a BASC Regional Compliance Officer where the BASC annex defines that role) and the Enterprise Risk Committee on a quarterly basis; see [`compliance/`](../compliance/).

---

## Evidence requirements

| Activity | Required Evidence |
| --- | --- |
| Audit Scheduling | Notification record, confirmed audit scope and date. |
| Pre-Audit Preparation | Document review log, certificate validation records, audit checklist. |
| Audit Execution | Interview notes, observation records, evidence artefacts collected. |
| Scoring and Evaluation | Completed compliance matrix, domain scores, overall risk rating. |
| Reporting | Issued Supplier Audit Report, CAPA Register entries. |
| BASC Compliance | BASC certificate copy, compliance metrics report, quarterly submission record. |
| Finding Closure | CAPA closure record, Supplier Relationship Owner sign-off. |

---

## Related documents

- Supplier and Cloud Governance Framework: [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md)
- Third-Party Risk Management Standard: [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md)
- Supplier Due Diligence Procedure: [`supply-chain/procedure-supplier-due-diligence.md`](procedure-supplier-due-diligence.md)
- Trade and Supply-Chain Continuity Controls Annex: [`supply-chain/annex-trade-and-supply-chain-continuity-controls.md`](annex-trade-and-supply-chain-continuity-controls.md)
- Risk Register Procedure: [`risk/procedure-risk-register.md`](../risk/procedure-risk-register.md)
- Corrective and Preventive Action Procedure: [`compliance/procedure-capa.md`](../compliance/procedure-capa.md)

---

## References

- ISO/IEC 27036-4:2016: Information security for supplier relationships - Part 4: Guidelines for security of cloud services (first edition, October 2016; the "2013" date previously used in this document was incorrect).
- COBIT 2019 BAI05.02: Manage Organizational Change.
- CSA Cloud Controls Matrix v5, STA-05: Supply Chain Management, Transparency, and Accountability.
- ENISA AI cybersecurity work (feasibility studies and standardisation gap analyses under the EU Cybersecurity Act framework; no dedicated AI cybersecurity certification scheme has been formally published as of 2026).
- BASC International Standard v6 2023: Business Alliance for Secure Commerce.
- WCO SAFE Framework of Standards 2021: World Customs Organization.
- ISO 28000:2022, Security and resilience, Security management systems for the supply chain.

---

**End of Document**
