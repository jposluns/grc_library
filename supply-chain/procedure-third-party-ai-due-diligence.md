# Third-Party AI Due Diligence Procedure

**Document Title:** Third-Party AI Due Diligence Procedure\
**Document Type:** Procedure\
**Version:** 1.0.28\
**Date:** 2026-10-27\
**Owner:** AI Governance Approver\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/procedure-supplier-due-diligence.md`](procedure-supplier-due-diligence.md), [`supply-chain/procedure-supplier-audit.md`](procedure-supplier-audit.md), [`ai/framework-ai-governance-and-risk.md`](../ai/framework-ai-governance-and-risk.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../privacy/procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md)\
**Classification:** Public\
**Category:** Supply Chain Governance | Third-Party Risk\
**Review Frequency:** 6 to 12 months and upon material supplier, regulatory, or framework change\
**Repository Path:** [`supply-chain/procedure-third-party-ai-due-diligence.md`](procedure-third-party-ai-due-diligence.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This procedure defines the AI-specific due diligence steps required before engaging any third-party AI service provider, AI model supplier, AI agent platform, or AI-enabled software-as-a-service application.

It complements the Supplier Due Diligence Procedure with controls that address the distinct risks presented by AI systems, including opacity in model behaviour, training data provenance, bias and fairness concerns, adversarial vulnerabilities, and the regulatory obligations imposed on deployers and importers of AI systems.

This procedure is synthesized from NIST AI RMF 1.0 (Govern 1.1 to 1.7, Map 5.1 to 5.2), ISO/IEC 42001:2023 Annex A.10 and B.10.3 (Third-party and customer relationships, Suppliers), EU AI Act Articles 2(2), 2(13), 6(1), 6(1a) to 6(1c), 6(3), 9, 13, 23, 26, 50, 51, 55(1)(b), 111(2), 111(4), and 113, as amended by Regulation (EU) 2026/1744, OWASP LLM Top 10, and CSA AI Controls Matrix (AICM) v1.1.

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
| AI Governance Council | Leads AI supplier classification, reviews pre-engagement assessments, approves each engagement where the supplier is High Risk under the Section 4.2 supplier tier or the AI system is a High-Risk AI System under the Section 4.1 EU AI Act classification, and oversees ongoing AI supplier monitoring. |
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
| High-Risk AI System | Applies to systems within the EU AI Act Annex III use cases (e.g., biometric identification, critical infrastructure management, employment screening, credit scoring, law enforcement), subject to the Article 6(3) non-high-risk derogation; an AI system referred to in Annex III that performs profiling of natural persons is always high-risk (Article 6(3)). Also applies to an AI system that is, or is a safety component of, a product covered by the Union harmonization legislation listed in Annex I and required to undergo a third-party conformity assessment (Article 6(1)), bounded by Article 6(1a) to (1c) as inserted by Regulation (EU) 2026/1744: an AI system used solely for non-safety aspects of user assistance, performance optimization, service efficiency, automation, convenience, or quality control is not a safety component unless its failure or malfunctioning would endanger health and safety, and a product that is required to undergo a third-party conformity assessment solely due to risks other than risks to health and safety is not considered to fulfil the condition in Article 6(1), point (b). | Core and Extended items (Section 5), which are the organization's means of evidencing the provider's risk management system (Article 9) and its transparency and provision of information to deployers (Article 13); the organization requires them for every High-Risk AI System as its own requirement, whatever the statutory position. Statutory obligations: the requirements under Articles 9 and 13, deployer obligations per Article 26, and importer obligations per Article 23 apply from 2 December 2027 for a system classified under Article 6(2) and Annex III, and from 2 August 2028 for a system classified under Article 6(1) and Annex I (Article 113, third paragraph, point (c), as replaced by Regulation (EU) 2026/1744). For a system classified under Article 6(1), delegated acts adopted under Article 2(13) (as added by Regulation (EU) 2026/1744; due by 2 August 2027) may limit the application of specific requirements or obligations in Articles 9 to 15 and 17 to 25, which include Articles 9, 13, and 23, where and to the extent that both of the following conditions are met: (a) the Union harmonization legislation listed in Section A of Annex I provides a level of protection of health, safety, or fundamental rights equivalent to or higher than that of the requirement or obligation concerned, and (b) the limitation does not reduce the overall level of protection that the Regulation provides; Legal Counsel confirms the position against the delegated acts as adopted. Without prejudice to the application of Article 5 as referred to in Article 113, third paragraph, point (a), for a high-risk AI system, other than a system referred to in Article 111(1), that was placed on the market or put into service before the date of application of Chapter III that applies to it (2 December 2027 or 2 August 2028), the Regulation applies to its operators only if, as from that date, the system is subject to significant changes in its design; in any case, providers and deployers of a high-risk AI system intended to be used by public authorities must take the necessary steps to comply by 2 August 2030 (Article 111(2), as replaced by Regulation (EU) 2026/1744). These statutory qualifications do not affect the organization's own Core and Extended requirement. The organization may apply these controls earlier as internal policy; an early control does not mean that its statutory deadline has arrived. For a system classified under Article 6(1) that relates to a product covered by the Union harmonization legislation listed in Section B of Annex I, only Article 6(1), Article 60a, and Articles 102 to 112 apply, and Articles 57, 58, and 59 apply only in so far as the requirements for high-risk AI systems under the Regulation have been integrated into that Union harmonization legislation (Article 2(2), as replaced by Regulation (EU) 2026/1744), so Articles 9, 13, 23, and 26 do not apply to it as statutory obligations. |
| General Purpose AI (GPAI) | Foundation models or large language models with broad applicability across tasks. | Core and Extended items (Section 5), including the model card and capability documentation (item 1), plus item 15 (systemic risk assessment) where the supplied model is a general-purpose AI model with systemic risk (Article 51) or the system is based on one. |
| Limited or Minimal Risk | AI systems with narrow scope and low potential for harm (e.g., spam filters, recommendation engines). | Core items (Section 5), plus the Article 50 transparency obligations set out below the table. |

Except for a high-risk AI system related to a product under Section B of Annex I, addressed at the end of this paragraph, the Article 50 transparency obligations apply whatever the classification in the table above, alongside the obligations in each row: Article 50(2) names general-purpose AI systems, and Article 50(6) provides that Article 50(1) to (4) do not affect the requirements and obligations in Chapter III for high-risk AI systems. Where their conditions apply, and subject to their exceptions, the provider must ensure that individuals are informed that they are interacting with an AI system (Article 50(1)) and must mark synthetic audio, image, video, or text output in a machine-readable format as artificially generated or manipulated (Article 50(2)); the deployer must inform individuals exposed to an emotion recognition or biometric categorization system (Article 50(3)) and must disclose deep fakes, and text published to inform the public on matters of public interest, as artificially generated or manipulated (Article 50(4)). A provider of a system generating synthetic content that was placed on the market before 2 August 2026 must comply with Article 50(2) by 2 December 2026 (Article 111(4), as added by Regulation (EU) 2026/1744). Article 50 is not among the provisions that Article 2(2) applies to a high-risk AI system related to a product under Section B of Annex I; Legal Counsel confirms the transparency position for such a system.

### 4.2 Organization-defined AI risk tier mapping

The NIST AI RMF 1.0 does not prescribe a risk-tier taxonomy; it directs each organization to define its own risk tolerance (AI RMF 1.0, Risk Tolerance). The tiers below are organization-defined, informed by the AI RMF's risk-management approach. They set the depth of supplier due diligence and are named, not numbered: they are not the organizational AI risk classification (Minimal, Limited, High, Unacceptable) recorded for each AI system in the AI System Register.

| Risk tier (organization-defined) | Description | Assessment Depth |
| --- | --- | --- |
| High Risk | Significant likelihood of harm; consequential automated decisions affecting individuals. | Core and Extended items (Section 5); semi-annual monitoring. |
| Moderate Risk | Moderate automated decision support; human oversight present. | Core items (Section 5); annual monitoring. |
| Low Risk | Minimal automation; decisions are advisory or informational only. | Core items (Section 5); annual attestation. |

---

## 5. Pre-engagement AI due diligence checklist

All required checklist items must be assessed before any AI supplier contract is executed. This procedure applies to every AI supplier within the scope in Section 2, whatever its criticality tier; for a third party that uses AI systems in service delivery but falls outside Section 2, the AI systems row of Section 4.1 of [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md) and the paragraph that follows it govern instead. The Applies To column marks each item Core or Extended, except item 15, which applies only where the supplied model is a general-purpose AI model with systemic risk (EU AI Act Article 51) or the General Purpose AI system is based on one. Mandatory evidence is set separately on each of three scales, which remain distinct: the two scales in Section 4, and the criticality tier (Tier 1 to Tier 4) assigned under [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md) Section 3. A rating on one scale does not determine the rating on another.

- **Section 4.2 supplier tier:** for a High Risk supplier, evidence must be obtained against every Core and Extended item; for a Moderate Risk or Low Risk supplier, evidence must be obtained against every Core item.
- **Section 4.1 EU AI Act classification:** for a High-Risk AI System, a General Purpose AI system, or a supplied general-purpose AI model (with or without systemic risk), evidence must be obtained against every Core and Extended item, and, where the supplied model is a general-purpose AI model with systemic risk or the General Purpose AI system is based on one, also against item 15; for a Limited or Minimal Risk system, evidence must be obtained against every Core item.
- **Criticality tier under the Third-Party and Supply Chain Risk Standard:** for a Tier 1 supplier, for which that standard requires Full AI due diligence, evidence must be obtained against every Core and Extended item; for a Tier 2, Tier 3, or Tier 4 supplier, evidence must be obtained against every Core item.

The strictest evidence requirement across the three scales governs: an item is mandatory when the rule for any scale requires it. Evidence must therefore be obtained against every Core and Extended item where any scale calls for full due diligence (a Tier 1 supplier, a High Risk supplier, or a High-Risk AI System, a General Purpose AI system, or a supplied general-purpose AI model with or without systemic risk), and against at least every Core item otherwise; item 15 is also mandatory wherever the supplied model is a general-purpose AI model with systemic risk or the General Purpose AI system is based on one. The organization chose the strictest requirement because it is the safer choice: a lower rating on one scale must not waive evidence that another scale requires.

| # | Due Diligence Domain | Required Evidence | Applies To |
| --- | --- | --- | --- |
| 1 | **Model Documentation** | Model card or system card describing intended use, capabilities, limitations, and performance benchmarks. | Core. |
| 2 | **Training Data Provenance** | Documentation of training data sources, licensing, consent mechanisms, and geographic origin of data. | Core. |
| 3 | **Data Consent and Ethical Sourcing** | Assurance that training data was obtained with appropriate consent and is free from prohibited categories. | Core. |
| 4 | **Bias and Fairness Assessment** | Results of pre-deployment bias testing across demographic or protected characteristic dimensions. | Extended. |
| 5 | **Adversarial Robustness** | Evidence of testing against adversarial inputs, prompt injection, model inversion, and supply chain attacks per OWASP LLM Top 10. | Core. |
| 6 | **Explainability and Auditability** | Confirmation that the system supports interpretable outputs and that audit logs of model decisions are available. | Extended. |
| 7 | **Security Controls** | Evidence of access controls, encryption in transit and at rest, API security, and penetration testing. | Core. |
| 8 | **Privacy Controls** | Data minimization, pseudonymization, retention limits, and support for data subject rights (deletion, portability). | Core. |
| 9 | **Regulatory Compliance Classification** | Supplier's own assessment of EU AI Act classification, supported by documentation. | Core. |
| 10 | **Incident Notification Capability** | Confirmation of the supplier's ability and commitment to notify within 24 hours of a security or AI system incident. The 24-hour clock is uniform and governs regardless of supplier criticality tier (see Section 6.3). | Core. |
| 11 | **Data Return and Deletion on Contract Termination** | Written commitment to the data-return, export-verification, deletion, and certification requirements in Section 6.4, including preservation of the applicable cloud export window and identification of any records subject to mandatory retention. | Core. |
| 12 | **Subprocessor and Supply Chain Transparency** | Disclosure of subprocessors, data sub-labellers, infrastructure providers, and upstream model dependencies. | Extended. |
| 13 | **ISO/IEC 42001:2023 Alignment** | Evidence of AI management system practices aligned to ISO/IEC 42001:2023 Annex A.10 and B.10.3 (Third-party and customer relationships, Suppliers). | Extended. |
| 14 | **CSA AICM Alignment** | Self-assessment or independent attestation against applicable CSA AI Controls Matrix v1.1 control families. | Extended. |
| 15 | **Systemic Risk Assessment** | Evidence of the systemic risk assessment and mitigation that EU AI Act Article 55(1)(b) requires of the provider of the general-purpose AI model with systemic risk that is supplied or on which the system is based, or that provider's summary of it, supported by documentation. | A supplied general-purpose AI model with systemic risk (EU AI Act Article 51), or a General Purpose AI system based on one, only. |

Suppliers that fail to provide satisfactory evidence for one or more items mandatory under this section, on any scale, must submit a documented remediation plan before engagement proceeds. Where the supplier is High Risk under the Section 4.2 supplier tier or the AI system is a High-Risk AI System under the Section 4.1 EU AI Act classification, and satisfactory evidence cannot be obtained for one or more items mandatory under this section, the engagement must be escalated to the AI Governance Council for an engagement approval decision.

---

## 6. Contractual AI requirements

All contracts with AI suppliers must include the following provisions in addition to standard third-party contractual clauses:

### 6.1 Model documentation

- Delivery of a current model card or system card at contract execution and upon each major model version release.
- Commitment to maintain and update documentation to reflect material capability or behavioural changes.

### 6.2 Explainability service level agreements

- Definition of the supplier's supported explainability methods (e.g., feature attribution, decision rationale outputs).
- Commitment to response timelines for explanation requests submitted by the organization.

### 6.3 Incident notification

- Mandatory notification to the organization within 24 hours of discovery of a security incident, data breach, model failure, or material AI system deviation.
- Notification must include: nature of the incident, affected data or model components, steps taken to contain the issue, and an estimated resolution timeline.
- This 24-hour clock is uniform across every AI supplier and governs regardless of the supplier's criticality tier; it applies to every AI supplier, and a lower criticality tier under [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md) does not waive it. Where it overlaps the tiered notification windows in that standard and in [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md), the stricter 24-hour AI clock applies and the tiered 72-hour window does not extend it; because this clock runs from discovery (above), it is also the stricter obligation where a tiered window is nominally 24 hours but runs only from a confirmed incident. For non-AI supplier relationships, those tiered windows continue to govern as written in the supplier standards.

### 6.4 Data return and deletion on contract termination

- For AI suppliers within the scope of [`supply-chain/standard-cloud-exit-and-data-portability.md`](standard-cloud-exit-and-data-portability.md), contracts must preserve the organization's data-export right for an agreed window of at least 90 calendar days following contract termination. Before deletion, the organization must verify the completeness, integrity, readability, and receipt of the export in organization-controlled storage. Export and return must cover organizational data and derived embeddings, fine-tuning artefacts, and retrieval stores to which the organization has return rights.
- For those suppliers, certified deletion of all organizational data, derived embeddings, fine-tuning artefacts, and retrieval stores, including provider-held and subprocessor-held copies and backups, must be completed within 30 calendar days after both the agreed export window has ended and successful export verification has been recorded. The organization may expressly authorize an earlier end to the window in writing after verification, identifying the data covered; in that case the 30-calendar-day deletion period begins on that authorization. Completion of an export alone does not waive the remaining window. If verification is incomplete at the end of the window, the supplier must preserve the affected data and export access until verification is completed, and the organization must escalate the delay to Legal and the Contract Owner.
- For AI suppliers outside the cloud-exit standard's scope, certified deletion remains due within 30 calendar days of contract termination; any required data return and verification must be completed before deletion.
- Written certified deletion confirmation must be provided to the organization within 5 business days of completion. Only specifically identified records subject to a mandatory legal or corpus retention requirement, including the AI system audit logs required by Section 6.5 and deletion records required by Section 8.2, may remain. The confirmation must identify retained records, their retention basis, and the applicable retention period rather than certify that those records have been deleted. Retained records must be segregated, access-restricted, used only for the required retention purpose, and deleted when that requirement expires.

### 6.5 Right to audit AI system logs

- The organization retains the right to audit AI system logs, decision records, and model behaviour reports.
- Supplier must retain AI system audit logs for a minimum of 7 years, the organization's canonical AI-audit-log retention floor (ISO/IEC 42001:2023 requires event-log record keeping and retention control without prescribing a period, and the EU AI Act's own log-keeping minimum is shorter; the 7-year figure is the organization's contractual requirement).

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

At least annually, the AI Governance Council must review or commission a bias and fairness re-assessment for every High Risk supplier under the Section 4.2 supplier tier, and for every supplier whose AI system is a High-Risk AI System or a General Purpose AI system, or whose supplied model is a general-purpose AI model (with or without systemic risk), under the Section 4.1 EU AI Act classification. The re-assessment must use current operational data and reflect any demographic shifts in the population served.

### 7.3 OWASP LLM top 10 re-evaluation on major version changes

Whenever a supplier releases a major model version update, a re-evaluation against the OWASP LLM Top 10 supply chain risk categories must be conducted before the new version is approved for operational use. The evaluation must specifically address:

- LLM04:2026: Supply Chain (model and component provenance).
- LLM05:2026: Data and Model Poisoning (training-data integrity).
- LLM07:2026: Misinformation (including overreliance on hallucinated AI output for automated decisions).

### 7.4 Reassessment triggers

An out-of-cycle reassessment must be initiated upon any of the following events:

- A security incident or data breach affecting the supplier's AI infrastructure.
- A material change in the supplier's ownership, model architecture, or data supply chain.
- A regulatory enforcement action or compliance finding involving the supplier.
- A material change in the organization's use of the AI system.

---

## 8. Exit and knowledge transfer

### 8.1 Exit planning

Exit planning for AI suppliers must be initiated at the contract review stage and maintained as a living document throughout the supplier relationship. The exit plan must address:

- Model repatriation (where the organization has rights to a fine-tuned or custom model) or certified deletion.
- Migration of prompts, system configurations, integration logic, and operational parameters.
- Continuity of AI-dependent processes during the transition period.
- Identification of alternative AI suppliers or fallback operational processes.

### 8.2 Data and model deletion

Upon contract termination, the AI supplier must follow the coordinated data-return and deletion sequence in Section 6.4:

1. Preserve the applicable export window and access, support required data return and organizational verification, and then permanently delete all organizational data, training fine-tuning artefacts, embeddings, and retrieval stores, including copies and backups, within the applicable Section 6.4 deadline and subject only to its mandatory-records-retention qualification.
2. Provide written certified deletion confirmation within 5 business days of completion, identifying any records retained under Section 6.4 and their retention basis and period.
3. Retain deletion records for 7 years per the organization's canonical AI-records retention floor (ISO/IEC 42001:2023 requires records retention without prescribing the period; the figure is the organization's contractual requirement).

### 8.3 Documentation retention

The organization must retain the following AI system documentation for a minimum of 7 years:

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
- ISO/IEC 42001:2023, Artificial intelligence, Management system, Annex A.10 and B.10.3 (Third-party and customer relationships, Suppliers), applied to third-party AI governance.
- EU AI Act (Regulation 2024/1689): Articles 2(2) (Scope, as replaced by Regulation (EU) 2026/1744), 2(13) (as added by Regulation (EU) 2026/1744), 6(1) and 6(3) (Classification rules for high-risk AI systems), 6(1a) to 6(1c) (as inserted by Regulation (EU) 2026/1744), 9 (Risk management), 13 (Transparency and provision of information), 23 (Obligations of importers), 26 (Obligations of deployers of high-risk AI systems), 50 (Transparency obligations for providers and deployers of certain AI systems), 51 (Classification of general-purpose AI models as general-purpose AI models with systemic risk), 55(1)(b) (Obligations of providers of general-purpose AI models with systemic risk), 111(2) (as replaced by Regulation (EU) 2026/1744), 111(4) (as added by Regulation (EU) 2026/1744), and 113 (Entry into force and application; third paragraph, point (c), as replaced by Regulation (EU) 2026/1744).
- Regulation (EU) 2026/1744 (Digital Omnibus on AI), Article 1 (Amendments to Regulation (EU) 2024/1689), which replaces or inserts the EU AI Act provisions cited above as amended by it: Articles 2(2) and 2(13), 6(1a) to 6(1c), 111(2) and 111(4), and 113, third paragraph, point (c).
- OWASP LLM Top 10:2026: LLM04:2026 Supply Chain; LLM05:2026 Data and Model Poisoning; LLM07:2026 Misinformation (the 2026 edition renumbered the risks; this list uses 2026 numbering).
- CSA AI Controls Matrix (AICM) v1.1: Cloud Security Alliance.
- ISO/IEC 27036-3:2023: Cybersecurity - Supplier relationships - Part 3: Guidelines for hardware, software, and services supply chain security (Edition 2; supersedes the 2013 edition titled "Information security for supplier relationships - Guidelines for ICT supply chain security").
- ENISA AI cybersecurity work (feasibility studies and standardization gap analyses under the EU Cybersecurity Act framework; as of 2026 no dedicated AI cybersecurity certification scheme has been formally published, though the work is ongoing and adopters should monitor ENISA publications and EU AI Act conformity-assessment guidance).

---

**End of Document**
