# AI Model Documentation and Transparency Framework

**Document Title:** AI Model Documentation and Transparency Framework\
**Document Type:** Framework\
**Version:** 1.0.9\
**Date:** 2026-07-12\
**Owner:** Chief Information Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`ai/charter-ai-governance-council.md`](charter-ai-governance-council.md), [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md), [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material AI framework or regulatory change\
**Repository Path:** [`ai/framework-ai-model-documentation-and-transparency.md`](framework-ai-model-documentation-and-transparency.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customization guidance.

---

## Purpose

This framework defines the documentation and transparency requirements for all AI systems deployed or developed by the organization. It establishes minimum standards for model cards, AI Impact Assessments, training data records, and transparency disclosures, ensuring that AI systems are understandable, auditable, and accountable to stakeholders, regulators, and affected individuals.

---

## Scope

Applies to all AI systems, machine learning models, generative AI tools, and automated decision-making systems in the AI System Inventory. Includes both internally developed and third-party AI systems integrated into operational workflows.

---

## Governance and accountability

| Role | Responsibility |
| --- | --- |
| **AI Governance Council (AIGC)** | Approves documentation standards; reviews completeness for High-risk systems. |
| **AI System Owner** | Accountable for maintaining current documentation for their AI system. |
| **AI Development / Data Science Teams** | Produce and maintain model documentation throughout the lifecycle. |
| **Data Protection Officer (DPO)** | Reviews AI documentation for privacy and personal data compliance. |
| **Internal Audit** | Audits documentation completeness and currency annually. |

---

## 1. Model card requirements

Every AI system must have a current Model Card. Model Cards are living documents updated at each major version or retraining event.

**Mandatory Model Card sections:**

| Section | Content |
| --- | --- |
| **Model Overview** | Model name, version, type (classification, generation, prediction, etc.), and brief description of purpose |
| **Intended Use** | Specific tasks and contexts the model is designed for |
| **Out-of-Scope Uses** | Uses the model is not designed for and should not be applied to |
| **Inputs and Outputs** | Description of input data types and output format |
| **Training Data** | Summary of training data sources, volume, and date range (detailed record maintained separately) |
| **Performance Metrics** | Key accuracy, precision, recall, F1, or task-specific metrics with evaluation conditions |
| **Known Limitations** | Identified edge cases, failure modes, or performance degradation conditions |
| **Bias and Fairness** | Fairness evaluation methodology and results; identified residual biases |
| **Explainability** | Explainability method used; representative example explanations |
| **Privacy** | Personal data processing summary; consent and legal basis if applicable |
| **Risk Tier** | Organizational AI risk classification: Minimal / Limited / High / Unacceptable |
| **Owner** | Role title of AI System Owner |
| **Version History** | Version, date, and summary of changes |

---

## 2. AI impact assessment

An AI Impact Assessment (AI-IA) is required for all Limited and High-risk AI systems before deployment and following any material change.

**AI-IA content requirements:**

1. **Context and purpose:** Business context, stakeholder groups affected, and decision-making role of the AI system.
2. **Risk identification:** Potential harms to individuals, groups, or society arising from AI outputs.
3. **Bias assessment:** Evaluation of training data representativeness and model output fairness across affected groups.
4. **Privacy analysis:** Personal data processing review, purpose limitation, and proportionality assessment.
5. **Transparency obligations:** What disclosures are required to affected individuals or regulators.
6. **Accountability mapping:** Who is responsible for AI decisions and how redress is provided.
7. **Mitigation measures:** Controls to address identified risks.
8. **Residual risk:** Documented acceptance of remaining risk by the AI System Owner and AIGC.

---

## 3. Training data record

All AI systems must maintain a Training Data Record covering:

- Data sources (with provenance information).
- Data collection dates and volumes.
- Data preprocessing and transformation steps.
- Consent, licensing, or legal basis for data use.
- Known gaps, biases, or limitations in the training data.
- Data retention and disposal plan for training datasets.

---

## 4. Transparency disclosures

The organization's transparency disclosures follow the transparency taxonomy of ISO/IEC 12792:2025, which structures disclosures across four levels, context (§7), system (§8), model (§9), and dataset (§10), and three transparency objectives, right to know, proper usage, and traceability (§6.2). Each objective is realized through a stakeholder pair, a content-providing role and a content-receiving role (§6.1; the pairs are enumerated in §6.3). The disclosures below map the organization's governance roles to those objectives and stakeholder pairs. The ISO/IEC 12792 role names (AI provider, AI deployer, AI subject, relevant authorities, AI auditor) are the external taxonomy the organization's roles align to, not a renaming of the organization's own roles.

### 4.1 Internal transparency

All stakeholders with governance responsibility for an AI system must have access to the current Model Card and AI Impact Assessment.

The AI System Inventory published by the GRC Programme Manager provides a summary view of all deployed AI systems and their risk tiers.

This realizes the traceability and proper-usage objectives (ISO/IEC 12792:2025 §6.2) among the internal provider and governance roles (the AI-producer-to-AI-provider stakeholder pairing in §6.3).

### 4.2 Affected individual transparency

Where an AI system makes or materially influences decisions affecting individuals (customers, employees, suppliers), the organization must:

- Disclose that an AI system is involved in the decision.
- Provide a plain-language explanation of the factors that influenced the outcome.
- Provide a mechanism for individuals to request human review of AI-influenced decisions (GDPR Article 22 right).
- Document the explanation provided and retain for audit purposes.

This realizes the right-to-know objective (ISO/IEC 12792:2025 §6.2) for the affected individual, who is the AI subject in the AI-deployer-to-AI-subject stakeholder pair (§6.3).

### 4.3 Regulatory transparency

For High-risk AI systems under the EU AI Act, technical documentation per Annex IV must be maintained and available to competent authorities on request.

This realizes the traceability objective (ISO/IEC 12792:2025 §6.2) through the AI-provider-to-relevant-authorities and AI-provider-to-AI-auditor stakeholder pairs (§6.3).

### 4.4 General-purpose AI model transparency (EU AI Act Article 53)

Where the organization is a provider of a general-purpose AI model placed on the EU market, the AI Act Article 53(1)(a) and (b) documentation obligations apply (technical documentation for the model, and information and documentation for downstream providers). The EU AI Office's *General-Purpose AI Code of Practice, Transparency Chapter* (July 2025) is the Article 56 co-regulatory instrument for demonstrating that compliance, and its **Model Documentation Form** (Measure 1.1) is the recognized means of compiling the documentation; adherence is voluntary soft law and not conclusive evidence of compliance, with the binding provision remaining Article 53 itself. The regime framing lives in [`ai/jurisdictions/annex-ai-european-union.md`](jurisdictions/annex-ai-european-union.md); information intended for the AI Office or national competent authorities is disclosed only on request and is subject to the Article 78 confidentiality and trade-secret protections.

The Model Documentation Form's fields, consolidated below by model-card affinity (the Form's own section structure is regrouped here, not mirrored one-to-one), map onto this framework's model-card model, so a GPAI provider satisfies the Form by maintaining an extended model card:

| Model Documentation Form fields | Model card section |
| --- | --- |
| General information (legal name of the provider; model name and unique identifier; model authenticity; release date; Union market release date; model dependencies) | [`ai/template-model-card.md`](template-model-card.md) §1 Model overview |
| Model properties, distribution, and use (architecture; input and output modalities and sizes; total model size; distribution channels and licence; intended and prohibited uses; means and required hardware/software for integration) | §2 Functional description |
| Training process (design specifications of the training process; decision rationale) | §4 Evaluation summary (model build procedure and hyperparameters) |
| Data used (type and provenance of training, testing, and validation data; how data was obtained and selected; number of data points; curation methodologies) | §3 Data provenance and lineage; the Form's measures-to-detect-identifiable-biases field maps to §5 Interpretability and representation |
| Computational resources and energy (training time; amount of computation and its measurement methodology; energy consumption) | §2 Functional description (compute and environmental-footprint fields) |

A provider adds any Form field with no direct model-card counterpart (for example the AI Office / national-competent-authority / downstream-provider recipient flag each Form item carries) to the model card as an annex, so the single extended card serves both the Form and the corpus documentation model.

---

## 5. Documentation lifecycle

| Event | Documentation Action |
| --- | --- |
| New AI system registered | Model Card created; AI-IA completed for Limited/High |
| Major retraining | Model Card updated; AI-IA reviewed and updated if scope changes |
| Performance drift detected | Model Card updated with drift details and remediation plan |
| AI incident | Model Card incident history updated; AI-IA reviewed |
| System decommissioned | Final documentation retained per Data Retention Schedule |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 42001:2023 | §7.5: Documented information | AI documentation requirements |
| EU AI Act (2024) | Annex IV: Technical Documentation | High-risk AI documentation |
| EU GPAI Code of Practice, Transparency Chapter (July 2025) | Measure 1.1 (Model Documentation Form); AI Act Article 53(1)(a)-(b) | GPAI-provider model documentation (Article 56 co-regulatory instrument, voluntary) |
| NIST AI RMF (2023) | MAP and MANAGE functions | AI transparency and documentation |
| ISO/IEC 12792:2025 | §6.2 transparency objectives; §6.1 and §6.3 stakeholder pairs; §7 to §10 taxonomy levels | AI transparency taxonomy structuring Section 4 |
| NIST IR 8312 | Four Principles of Explainable Artificial Intelligence | Explainability principles |
| OECD AI Principles (2019, updated 2024) | Transparency and Explainability | AI transparency obligations |
| GDPR (2018) | Article 22: Automated Decision-Making | Transparency and human review rights |

---

**End of Document**
