# Supplier Due Diligence Procedure

**Document Title:** Supplier Due Diligence Procedure 
**Document Type:** Procedure 
**Version:** 1.0.1 
**Date:** 2026-05-28 
**Owner:** Supplier Risk Maintainer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/procedure-supplier-audit.md`](procedure-supplier-audit.md), [`supply-chain/annex-trade-and-supply-chain-continuity-controls.md`](annex-trade-and-supply-chain-continuity-controls.md), [`risk/procedure-risk-register.md`](../risk/procedure-risk-register.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md) 
**Classification:** Public 
**Category:** Supply Chain Governance | Third-Party Risk 
**Review Frequency:** Annual and upon material supplier, regulatory, or framework change 
**Repository Path:** [`supply-chain/procedure-supplier-due-diligence.md`](procedure-supplier-due-diligence.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This procedure defines the methodology for pre-qualification, risk assessment, and ongoing compliance review of suppliers, vendors, and third-party partners. It establishes a consistent, evidence-based approach to evaluating supplier fitness prior to engagement and at defined reassessment intervals throughout the supplier lifecycle.

This procedure is aligned with ISO/IEC 27036-2, COBIT 2019 BAI05, CSA CCM v4.1 STA-01, and BASC International Standard v6 2023.

---

## Scope

1. Applies to all suppliers and third-party entities engaged to provide goods or services to the organization.
2. Covers pre-engagement due diligence, contract validation, and periodic compliance reassessment.
3. Includes global operations with additional requirements for BASC-certified logistics and trade partners in Latin America.
4. Applies to suppliers providing AI systems, cloud services, logistics solutions, or data-handling activities.

---

## Governance

| Role | Responsibility |
| --- | --- |
| Chief Information Officer | Approves the supplier due diligence framework and ensures that integration with risk management processes. |
| Chief Information Security Officer | Evaluates the information security and privacy posture of potential and existing suppliers. |
| Procurement Director | Administers supplier assessments, manages onboarding processes, and ensures that contract compliance. |
| Compliance and GRC Manager | Oversees due diligence documentation, evidence collection, and audit readiness. |
| Legal Counsel | Verifies contractual and regulatory compliance, including data protection and trade law clauses. |
| Sustainability Officer | Reviews environmental and social responsibility disclosures submitted by suppliers. |
| Regional Compliance Officers | Oversee trade and customs integrity checks for Latin American and other regionally regulated operations. |
| AI Governance Council | Reviews AI-enabled vendors for ethical, transparency, security, and regulatory compliance. |

---

## Procedure

### Step 1: Supplier pre-qualification

All suppliers must complete a Supplier Pre-Qualification Questionnaire (SPQ) before contract initiation. The SPQ must address the following domains:

- Corporate registration, ownership structure, and beneficial ownership disclosure.
- Financial stability and credit standing.
- Applicable security certifications (ISO/IEC 27001, SOC 2, BASC).
- Data privacy compliance posture (GDPR, CPPA, PIPL, LGPD).
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
| Tier 3 | Moderate | Non-sensitive, indirect services with limited organizational impact. | Biennial. |
| Tier 4 | Low | Low-value, non-sensitive relationships with negligible data or system access. | Biennial or attestation. |

### Step 3: Due diligence evaluation

Assessments must be conducted across all applicable domains. Suppliers scoring below 70% of the maximum assessment score require documented remediation plans before engagement may proceed.

| Domain | Assessment Focus | Applicable Standards |
| --- | --- | --- |
| Security Controls | Encryption, access control, incident response, vulnerability management. | ISO/IEC 27001, SOC 2. |
| Privacy Compliance | Data protection obligations, consent management, cross-border transfer controls. | GDPR, CPPA, LGPD, PIPL. |
| Business Continuity | Recovery capabilities, resilience planning, dependency management. | ISO 22301, COBIT DSS04. |
| AI Governance | Model transparency, bias controls, fairness, auditability. | ISO/IEC 42001, CSA AICM. |
| BASC Compliance | Customs integrity, cargo security, anti-smuggling controls (Latin America). | BASC International Standard v6 2023. |
| Trade Security | Supply chain security programme compliance. | WCO SAFE Framework 2021, ISO 28000:2022. |
| Sustainability | Energy management and environmental responsibility. | ISO 50001 Addendum 2026. |

### Step 4: Contractual review

All supplier contracts must include, at minimum:

- Data protection and confidentiality clauses aligned to applicable jurisdictional requirements.
- Right-to-audit provisions exercisable by the organization or its appointed representative.
- AI ethics and transparency requirements for AI service providers.
- BASC compliance obligations for Latin American logistics and trade partners.
- Environmental and sustainability obligations consistent with the organization's ESG commitments.
- Mandatory reporting timelines for security incidents, privacy breaches, or compliance failures.

Legal Counsel must review and approve all third-party contracts prior to execution.

### Step 5: Compliance assessment and re-audit

All Tier 1 and Tier 2 suppliers must undergo periodic compliance audits in accordance with the Supplier Audit Procedure. Re-audits may be triggered by any of the following events:

- A security incident or data breach involving the supplier.
- A contract breach or material SLA failure.
- Lapse, suspension, or revocation of a required regulatory or certification status (including BASC).
- A material change in the supplier's ownership, infrastructure, or service delivery model.

All corrective actions identified through due diligence or re-audit must be logged in the Corrective and Preventive Action (CAPA) Register and tracked to closure.

### Step 6: BASC and regional compliance integration

For suppliers engaged in Latin American logistics, customs, or trade operations, the following additional requirements apply:

- BASC certification must be verified prior to engagement and tracked for renewal throughout the supplier relationship.
- Compliance with the WCO SAFE Framework 2021 and ISO 28000:2022 must be confirmed.
- Trade documentation, cargo integrity practices, and customs reporting accuracy must be reviewed as part of the periodic assessment.

Regional Compliance Officers must maintain a BASC Supplier Compliance Log that is synchronized with the global Supplier Risk Register at least quarterly.

---

## Evidence requirements

| Activity | Required Evidence |
| --- | --- |
| Supplier Pre-Qualification | Completed SPQ, scoring summary, approval or rejection record. |
| Risk Assessment | Tier classification record, assessment report. |
| Due Diligence Evaluation | Domain assessment results, evidence artefacts, remediation plan where required. |
| Contractual Review | Executed contract with required clauses confirmed, Legal Counsel approval. |
| Periodic Re-Assessment | Updated TPRAQ or equivalent, reassessment report, CAPA entries where applicable. |
| BASC Compliance | BASC certificate copy, compliance log entry, renewal tracking record. |

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

- ISO/IEC 27036-2:2014: Information security for supplier relationships: Requirements.
- COBIT 2019 BAI05: Managed Organizational Change.
- CSA Cloud Controls Matrix v5, STA-01: Supply Chain Management, Transparency, and Accountability.
- BASC International Standard v6 2023: Business Alliance for Secure Commerce.
- WCO SAFE Framework of Standards 2021: World Customs Organization.
- ISO 28000:2022, Security and resilience, Security management systems for the supply chain.

---

**End of Document**
