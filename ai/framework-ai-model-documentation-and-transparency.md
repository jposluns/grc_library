# AI Model Documentation and Transparency Framework

**Document Title:** AI Model Documentation and Transparency Framework\
**Document Type:** Framework\
**Version:** 1.0.0\
**Date:** 2026-05-27\
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

## Purpose

This framework defines the documentation and transparency requirements for all AI systems deployed or developed by the organisation. It establishes minimum standards for model cards, AI Impact Assessments, training data records, and transparency disclosures, ensuring that AI systems are understandable, auditable, and accountable to stakeholders, regulators, and affected individuals.

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
| **Privacy Officer / DPO** | Reviews AI documentation for privacy and personal data compliance. |
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
| **Risk Tier** | Organisational AI risk classification: Minimal / Limited / High / Unacceptable |
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

### 4.1 Internal transparency

All stakeholders with governance responsibility for an AI system must have access to the current Model Card and AI Impact Assessment.

The AI System Inventory published by the GRC Programme Manager provides a summary view of all deployed AI systems and their risk tiers.

### 4.2 Affected individual transparency

Where an AI system makes or materially influences decisions affecting individuals (customers, employees, suppliers), the organisation must:

- Disclose that an AI system is involved in the decision.
- Provide a plain-language explanation of the factors that influenced the outcome.
- Provide a mechanism for individuals to request human review of AI-influenced decisions (GDPR Article 22 right).
- Document the explanation provided and retain for audit purposes.

### 4.3 Regulatory transparency

For High-risk AI systems under the EU AI Act, technical documentation per Annex IV must be maintained and available to competent authorities on request.

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
| ISO/IEC 42001:2023 | §8.4: AI System Documentation | AI documentation requirements |
| EU AI Act (2024) | Annex IV: Technical Documentation | High-risk AI documentation |
| NIST AI RMF (2023) | MAP and MANAGE functions | AI transparency and documentation |
| OECD AI Principles (2023) | Transparency and Explainability | AI transparency obligations |
| GDPR (2018) | Article 22: Automated Decision-Making | Transparency and human review rights |

---

**End of Document**
