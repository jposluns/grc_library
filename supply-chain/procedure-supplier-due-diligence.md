# Supplier Due Diligence Procedure

**Document Title:** Supplier Due Diligence Procedure\
**Document Type:** Procedure\
**Version:** 1.1.6\
**Date:** 2026-07-02\
**Owner:** Supplier Risk Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/procedure-supplier-audit.md`](procedure-supplier-audit.md), [`supply-chain/annex-trade-and-supply-chain-continuity-controls.md`](annex-trade-and-supply-chain-continuity-controls.md), [`risk/procedure-risk-register.md`](../risk/procedure-risk-register.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md)\
**Classification:** Public\
**Category:** Supply Chain Governance | Third-Party Risk\
**Review Frequency:** Annual and upon material supplier, regulatory, or framework change\
**Repository Path:** [`supply-chain/procedure-supplier-due-diligence.md`](procedure-supplier-due-diligence.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure defines the methodology for pre-qualification, risk assessment, and ongoing compliance review of suppliers, vendors, and third-party partners. It establishes a consistent, evidence-based approach to evaluating supplier fitness prior to engagement and at defined reassessment intervals throughout the supplier lifecycle.

This procedure is aligned with ISO/IEC 27036-2, COBIT 2019 BAI05, and CSA CCM v4.1 STA-01. Sector-specific framework alignments (for example, BASC International Standard v6 2022 for trade and logistics suppliers) apply where the organisation participates in a covered programme; see [`compliance/`](../compliance/).

---

## Scope

1. Applies to all suppliers and third-party entities engaged to provide goods or services to the organisation.
2. Covers pre-engagement due diligence, contract validation, and periodic compliance reassessment.
3. Applies globally; sector-specific overlays (for example, BASC for trade and logistics partners) apply where the organisation participates in a covered programme, per [`compliance/`](../compliance/).
4. Applies to suppliers providing AI systems, cloud services, logistics solutions, or data-handling activities.

---

## Governance and accountability

| Role | Responsibility |
| --- | --- |
| Chief Information Officer | Approves the supplier due diligence framework and ensures that integration with risk management processes is maintained. |
| Chief Information Security Officer | Evaluates the information security and privacy posture of potential and existing suppliers. |
| Procurement Director | Administers supplier assessments, manages onboarding processes, and ensures that contract compliance is maintained. |
| Compliance and GRC Manager | Oversees due diligence documentation, evidence collection, and audit readiness. |
| Legal Counsel | Verifies contractual and regulatory compliance, including data protection and trade law clauses. |
| Sustainability Officer | Reviews environmental and social responsibility disclosures submitted by suppliers. |
| AI Governance Council | Reviews AI-enabled vendors for ethical, transparency, security, and regulatory compliance. |

Sector-specific reviewer roles (for example, Regional Compliance Officers for sector-regulated operations) apply where the organisation participates in a covered programme; see [`compliance/`](../compliance/).

---

## Procedure

### Step 1: Supplier pre-qualification

All suppliers must complete a Supplier Pre-Qualification Questionnaire (SPQ) before contract initiation. The SPQ must address the following domains:

- Corporate registration, ownership structure, and beneficial ownership disclosure.
- Financial stability and credit standing.
- Applicable security certifications (for example, ISO/IEC 27001, SOC 2; plus sector-specific certifications such as BASC where the supplier is in scope of a covered programme, per [`compliance/`](../compliance/)).
- Data privacy compliance posture (GDPR, PIPEDA, PIPL, LGPD).
- Environmental, social, and governance (ESG) and sustainability disclosures.

Suppliers providing AI or cloud services must additionally submit:

- Model transparency documentation.
- Bias testing and fairness assessment results.
- Ethical AI practices and governance documentation.

Suppliers failing to meet the minimum baseline requirements defined in the SPQ scoring rubric must be rejected or formally flagged for remediation prior to any engagement proceeding.

### Step 2: Risk assessment and tier classification

Each supplier must be assessed and assigned a risk tier based on business impact, sensitivity of data accessed, and geographic or regulatory exposure. Tier assignment determines the applicable audit cadence.

| Tier | Classification | Criteria | Audit Cadence |
| --- | --- | --- | --- |
| Tier 1 | Critical | Access to sensitive or regulated data, AI systems, or critical infrastructure. | Semi-annual. |
| Tier 2 | High | Cloud, logistics, or key service dependencies with moderate data exposure. | Annual. |
| Tier 3 | Moderate | Non-sensitive, indirect services with limited organisational impact. | Biennial. |
| Tier 4 | Low | Low-value, non-sensitive relationships with negligible data or system access. | Biennial or attestation. |

### Step 3: Due diligence evaluation

Assessments must be conducted across all applicable domains. Suppliers scoring below 70% of the maximum assessment score require documented remediation plans before engagement may proceed.

| Domain | Assessment Focus | Applicable Standards |
| --- | --- | --- |
| Security Controls | Encryption, access control, incident response, vulnerability management. | ISO/IEC 27001, SOC 2. |
| Privacy Compliance | Data protection obligations, consent management, cross-border transfer controls. | GDPR, PIPEDA, LGPD, PIPL. |
| Business Continuity | Recovery capabilities, resilience planning, dependency management. | ISO 22301, COBIT DSS04. |
| AI Governance | Model transparency, bias controls, fairness, auditability. | ISO/IEC 42001, CSA AICM. |
| Trade Security | Supply chain security programme compliance (where the supplier is in scope). | WCO SAFE Framework 2021, ISO 28000:2022; plus sector-specific overlays per [`compliance/`](../compliance/). |
| Sustainability | Energy management and environmental responsibility. | ISO 50001. |

### Step 4: Contractual review

All supplier contracts must include, at minimum:

- Data protection and confidentiality clauses aligned to applicable jurisdictional requirements.
- Right-to-audit provisions exercisable by the organisation or its appointed representative.
- AI ethics and transparency requirements for AI service providers.
- Sector-specific obligations (for example, BASC, CTPAT, AEO, PIP compliance clauses) where the supplier is in scope of a covered programme; see [`compliance/`](../compliance/).
- Environmental and sustainability obligations consistent with the organisation's ESG commitments.
- Mandatory reporting timelines for security incidents, privacy breaches, or compliance failures.

Legal Counsel must review and approve all third-party contracts prior to execution.

### Step 5: Compliance assessment and re-audit

All Tier 1 and Tier 2 suppliers must undergo periodic compliance audits in accordance with the Supplier Audit Procedure. Re-audits may be triggered by any of the following events:

- A security incident or data breach involving the supplier.
- A contract breach or material SLA failure.
- Lapse, suspension, or revocation of a required regulatory or certification status.
- A material change in the supplier's ownership, infrastructure, or service delivery model.

All corrective actions identified through due diligence or re-audit must be logged in the Corrective and Preventive Action (CAPA) Register and tracked to closure.

### Step 6: Sector-programme compliance integration

For suppliers in scope of a sector-specific programme (for example, BASC for trade and logistics, CTPAT for US trade, AEO for EU trade, PIP for Canadian trade), the following additional integration applies:

- Sector certification status must be verified prior to engagement and tracked for renewal throughout the supplier relationship.
- Sector-specific compliance requirements (per the corresponding sector annex in [`compliance/`](../compliance/) or the relevant compliance annex in [`compliance/`](../compliance/)) must be confirmed.
- Sector-specific documentation, integrity practices, and reporting accuracy must be reviewed as part of the periodic assessment.

A sector-supplier compliance log maintained by the appropriate sector-conditional role (for example, BASC Regional Compliance Officer where the sector annex defines that role) must be synchronised with the global Supplier Risk Register at least quarterly.

---

## Evidence requirements

| Activity | Required Evidence |
| --- | --- |
| Supplier Pre-Qualification | Completed SPQ, scoring summary, approval or rejection record. |
| Risk Assessment | Tier classification record, assessment report. |
| Due Diligence Evaluation | Domain assessment results, evidence artefacts, remediation plan where required. |
| Contractual Review | Executed contract with required clauses confirmed, Legal Counsel approval. |
| Periodic Re-Assessment | Updated TPRAQ or equivalent, reassessment report, CAPA entries where applicable. |
| Sector-Programme Compliance | Sector certificate copy (for example, BASC, CTPAT, AEO, PIP where applicable), compliance log entry, renewal tracking record. |

---

## Related documents

- Supplier and Cloud Governance Framework: [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md)
- Third-Party Risk Management Standard: [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md)
- Supplier Audit Procedure: [`supply-chain/procedure-supplier-audit.md`](procedure-supplier-audit.md)
- Trade and Supply-Chain Continuity Controls Annex: [`supply-chain/annex-trade-and-supply-chain-continuity-controls.md`](annex-trade-and-supply-chain-continuity-controls.md)
- Risk Register Procedure: [`risk/procedure-risk-register.md`](../risk/procedure-risk-register.md)
- Corrective and Preventive Action Procedure: [`compliance/procedure-capa.md`](../compliance/procedure-capa.md)

---

## References

- ISO/IEC 27036-2:2022: Cybersecurity - Supplier relationships - Part 2: Requirements.
- COBIT 2019 BAI05: Managed Organizational Change.
- CSA Cloud Controls Matrix v4.1, STA-01: Supply Chain Management, Transparency, and Accountability.
- WCO SAFE Framework of Standards 2021: World Customs Organization.
- ISO 28000:2022, Security and resilience, Security management systems for the supply chain.

Sector-specific references (for example, BASC International Standard v6 2022 for trade and logistics) apply where the organisation participates in a covered programme; see [`compliance/`](../compliance/).

---

**End of Document**
