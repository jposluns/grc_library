# Third-Party AI Due Diligence Procedure

**Document Title:** Third-Party AI Due Diligence Procedure\
**Document Type:** Procedure\
**Version:** 1.0.3\
**Date:** 2026-06-24\
**Owner:** AI Governance Approver\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/procedure-supplier-due-diligence.md`](procedure-supplier-due-diligence.md), [`supply-chain/procedure-supplier-audit.md`](procedure-supplier-audit.md), [`ai/framework-ai-governance-and-risk.md`](../ai/framework-ai-governance-and-risk.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../privacy/procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md)\
**Classification:** Public\
**Category:** Supply Chain Governance | Third-Party Risk\
**Review Frequency:** Annual and upon material supplier, regulatory, or framework change\
**Repository Path:** [`supply-chain/procedure-third-party-ai-due-diligence.md`](procedure-third-party-ai-due-diligence.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This procedure defines the AI-specific due diligence steps required before engaging any third-party AI service provider, AI model supplier, AI agent platform, or AI-enabled software-as-a-service application.

It complements the Supplier Due Diligence Procedure with controls that address the distinct risks presented by AI systems, including opacity in model behaviour, training data provenance, bias and fairness concerns, adversarial vulnerabilities, and the regulatory obligations imposed on deployers and importers of AI systems.

This procedure is synthesized from NIST AI RMF (Govern 1.1 to 1.7, Map 5.1 to 5.2), ISO/IEC 42001 §9, EU AI Act Articles 9, 13, and 28 to 29, OWASP LLM Top 10, and CSA AI Controls Matrix (AICM) v1.1.

---

## 2. Scope

This procedure applies to:

- Third-party AI model suppliers and foundation model providers.
- AI-enabled software-as-a-service applications with material AI decision-making components.
- AI agent platforms and orchestration services.
- Data labelling, training data, and synthetic data suppliers.
- Embedded AI components within cloud or managed service offerings.

This procedure applies globally across all business units and geographic regions. Where an AI system also involves personal data processing, this procedure must be applied in conjunction with the Privacy Impact and Cross-Border Transfer Procedure.

---

## 3. Governance

| Role | Responsibility |
| --- | --- |
| AI Governance Council | Leads AI supplier classification, reviews pre-engagement assessments, approves high-risk AI engagements, and oversees ongoing AI supplier monitoring. |
| Chief Information Security Officer | Evaluates security controls, adversarial robustness, and incident response capabilities of AI suppliers. |
| Data Protection Officer | Assesses training data consent, personal data processing practices, and cross-border data transfer obligations. |
| Procurement Director | Administers the AI supplier engagement process, ensures that contractual AI requirements are included, and coordinates onboarding. |
| Legal Counsel | Reviews AI contractual obligations, regulatory compliance classifications, and exit provisions. |
| Supplier Relationship Owner | Monitors ongoing AI supplier performance and escalates risk changes or incidents to the AI Governance Council. |

---

## 4. AI supplier classification

Before commencing due diligence, each AI supplier and the AI system being evaluated must be classified to determine the applicable assessment depth and contractual obligations.

### 4.1 EU AI act risk classification

| Classification | Criteria | Deployer Obligations |
| --- | --- | --- |
| High-Risk AI System | Applies to systems listed in EU AI Act Annex III (e.g., biometric identification, critical infrastructure management, employment screening, credit scoring, law enforcement). | Full due diligence required per Articles 9 and 13; deployer obligations per Articles 28 to 29 apply. |
| General Purpose AI (GPAI) | Foundation models or large language models with broad applicability across tasks. | Model card, capability documentation, and systemic risk assessment required. |
| Limited or Minimal Risk | AI systems with narrow scope and low potential for harm (e.g., spam filters, recommendation engines). | Standard due diligence; transparency disclosure required where the system interacts with individuals. |

### 4.2 NIST AI RMF tier mapping

| NIST AI RMF Tier | Description | Assessment Depth |
| --- | --- | --- |
| Tier 1: High Risk | Significant likelihood of harm; consequential automated decisions affecting individuals. | Full pre-engagement checklist; semi-annual monitoring. |
| Tier 2: Moderate Risk | Moderate automated decision support; human oversight present. | Standard pre-engagement checklist; annual monitoring. |
| Tier 3: Low Risk | Minimal automation; decisions are advisory or informational only. | Abbreviated checklist; annual attestation. |

---

## 5. Pre-engagement AI due diligence checklist

All required checklist items must be assessed before any AI supplier contract is executed. High-Risk AI systems require evidence against all items. General Purpose AI systems require evidence against all items except those marked as High-Risk only. Low-Risk systems require evidence against items marked as applicable.

| # | Due Diligence Domain | Required Evidence | Applies To |
| --- | --- | --- | --- |
| 1 | **Model Documentation** | Model card or system card describing intended use, capabilities, limitations, and performance benchmarks. | All tiers. |
| 2 | **Training Data Provenance** | Documentation of training data sources, licensing, consent mechanisms, and geographic origin of data. | All tiers. |
| 3 | **Data Consent and Ethical Sourcing** | Assurance that training data was obtained with appropriate consent and is free from prohibited categories. | All tiers. |
| 4 | **Bias and Fairness Assessment** | Results of pre-deployment bias testing across demographic or protected characteristic dimensions. | High-Risk and GPAI. |
| 5 | **Adversarial Robustness** | Evidence of testing against adversarial inputs, prompt injection, model inversion, and supply chain attacks per OWASP LLM Top 10. | All tiers. |
| 6 | **Explainability and Auditability** | Confirmation that the system supports interpretable outputs and that audit logs of model decisions are available. | High-Risk and GPAI. |
| 7 | **Security Controls** | Evidence of access controls, encryption in transit and at rest, API security, and penetration testing. | All tiers. |
| 8 | **Privacy Controls** | Data minimization, pseudonymization, retention limits, and support for data subject rights (deletion, portability). | All tiers. |
| 9 | **Regulatory Compliance Classification** | Supplier's own assessment of EU AI Act classification, supported by documentation. | All tiers. |
| 10 | **Incident Notification Capability** | Confirmation of the supplier's ability and commitment to notify within 24 hours of a security or AI system incident. | All tiers. |
| 11 | **Data Deletion on Contract Termination** | Written confirmation that all organisational data and derived model artefacts will be deleted upon termination. | All tiers. |
| 12 | **Subprocessor and Supply Chain Transparency** | Disclosure of subprocessors, data sub-labellers, infrastructure providers, and upstream model dependencies. | High-Risk and GPAI. |
| 13 | **ISO/IEC 42001 Alignment** | Evidence of AI management system practices aligned to ISO/IEC 42001 §9 (third-party AI governance). | High-Risk and GPAI. |
| 14 | **CSA AICM Alignment** | Self-assessment or independent attestation against applicable CSA AI Controls Matrix v1.1 control families. | High-Risk and GPAI. |

Suppliers that fail to provide satisfactory evidence for items applicable to their classification must submit a documented remediation plan before engagement proceeds. High-Risk AI systems where critical checklist items cannot be satisfied must be escalated to the AI Governance Council for an engagement approval decision.

---

## 6. Contractual AI requirements

All contracts with AI suppliers must include the following provisions in addition to standard third-party contractual clauses:

### 6.1 Model documentation

- Delivery of a current model card or system card at contract execution and upon each major model version release.
- Commitment to maintain and update documentation to reflect material capability or behavioural changes.

### 6.2 Explainability service level agreements

- Definition of the supplier's supported explainability methods (e.g., feature attribution, decision rationale outputs).
- Commitment to response timelines for explanation requests submitted by the organisation.

### 6.3 Incident notification

- Mandatory notification to the organisation within 24 hours of discovery of a security incident, data breach, model failure, or material AI system deviation.
- Notification must include: nature of the incident, affected data or model components, steps taken to contain the issue, and an estimated resolution timeline.

### 6.4 Data deletion on contract termination

- Certified deletion of all organisational data, derived embeddings, fine-tuning artefacts, and retrieval stores within 30 days of contract termination.
- Written confirmation of deletion provided to the organisation within 5 business days of completion.

### 6.5 Right to audit AI system logs

- The organisation retains the right to audit AI system logs, decision records, and model behaviour reports.
- Supplier must retain AI system audit logs for a minimum of 7 years, consistent with ISO/IEC 42001 and EU AI Act Annex IV requirements.

### 6.6 Model version change notification

- Supplier must provide at least 30 days' advance notice of any major model version change that may materially affect system behaviour, accuracy, or compliance properties.

---

## 7. Ongoing monitoring

AI supplier risk does not remain static after initial engagement. The following monitoring activities apply throughout the supplier relationship.

### 7.1 Quarterly model performance review

The Supplier Relationship Owner, in coordination with the AI Governance Council, must conduct a quarterly review of:

- Model performance against agreed accuracy and fairness benchmarks.
- Incident and anomaly reports submitted since the last review.
- Changes to the supplier's regulatory compliance classification.

### 7.2 Annual bias re-assessment

At least annually, the AI Governance Council must review or commission a bias and fairness re-assessment for all High-Risk and GPAI suppliers. The re-assessment must use current operational data and reflect any demographic shifts in the population served.

### 7.3 OWASP LLM top 10 re-evaluation on major version changes

Whenever a supplier releases a major model version update, a re-evaluation against the OWASP LLM Top 10 supply chain risk categories must be conducted before the new version is approved for operational use. The evaluation must specifically address:

- LLM03: Supply Chain (model and component provenance).
- LLM04: Data and Model Poisoning (training-data integrity).
- LLM09: Misinformation (including overreliance on hallucinated AI output for automated decisions).

### 7.4 Reassessment triggers

An out-of-cycle reassessment must be initiated upon any of the following events:

- A security incident or data breach affecting the supplier's AI infrastructure.
- A material change in the supplier's ownership, model architecture, or data supply chain.
- A regulatory enforcement action or compliance finding involving the supplier.
- A material change in the organisation's use of the AI system.

---

## 8. Exit and knowledge transfer

### 8.1 Exit planning

Exit planning for AI suppliers must be initiated at the contract review stage and maintained as a living document throughout the supplier relationship. The exit plan must address:

- Model repatriation (where the organisation has rights to a fine-tuned or custom model) or certified deletion.
- Migration of prompts, system configurations, integration logic, and operational parameters.
- Continuity of AI-dependent processes during the transition period.
- Identification of alternative AI suppliers or fallback operational processes.

### 8.2 Data and model deletion

Upon contract termination, the AI supplier must:

1. Permanently delete all organisational data, training fine-tuning artefacts, embeddings, and retrieval stores.
2. Provide written certified deletion confirmation within 5 business days of completion.
3. Retain deletion records for 7 years in accordance with ISO/IEC 42001 and EU AI Act Annex IV obligations.

### 8.3 Documentation retention

The organisation must retain the following AI system documentation for a minimum of 7 years:

- All model cards and system cards received from the supplier.
- Pre-engagement due diligence checklists and assessment reports.
- Contractual AI obligations and any amendments.
- Incident notification records and post-incident reports.
- Audit logs and model performance reviews.
- Exit records including certified deletion confirmations.

---

## 9. Related documents

- Supplier and Cloud Governance Framework: [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md)
- Third-Party Risk Management Standard: [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md)
- Supplier Due Diligence Procedure: [`supply-chain/procedure-supplier-due-diligence.md`](procedure-supplier-due-diligence.md)
- Supplier Audit Procedure: [`supply-chain/procedure-supplier-audit.md`](procedure-supplier-audit.md)
- AI Governance and Risk Framework: [`ai/framework-ai-governance-and-risk.md`](../ai/framework-ai-governance-and-risk.md)
- Privacy Impact and Cross-Border Transfer Procedure: [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../privacy/procedure-privacy-impact-and-cross-border-transfer.md)
- Corrective and Preventive Action Procedure: [`compliance/procedure-capa.md`](../compliance/procedure-capa.md)

---

## 10. References

- NIST AI Risk Management Framework 1.0: Govern 1.1 to 1.7; Map 5.1 to 5.2.
- ISO/IEC 42001:2023, Artificial intelligence, Management system, §9 (Performance evaluation: Third-party AI governance).
- EU AI Act (Regulation 2024/1689): Articles 9 (Risk management), 13 (Transparency and provision of information), 28 to 29 (Obligations of deployers and importers).
- OWASP LLM Top 10:2025: LLM03 Supply Chain; LLM04 Data and Model Poisoning; LLM09 Misinformation (the 2025 edition restructured and renumbered the risks; this list uses 2025 numbering).
- CSA AI Controls Matrix (AICM) v1.1: Cloud Security Alliance.
- ISO/IEC 27036-3:2023: Cybersecurity - Supplier relationships - Part 3: Guidelines for hardware, software, and services supply chain security (Edition 2; supersedes the 2013 edition titled "Information security for supplier relationships - Guidelines for ICT supply chain security").
- ENISA AI cybersecurity work (feasibility studies and standardisation gap analyses under the EU Cybersecurity Act framework; as of 2026 no dedicated AI cybersecurity certification scheme has been formally published, though the work is ongoing and adopters should monitor ENISA publications and EU AI Act conformity-assessment guidance).

---

**End of Document**
