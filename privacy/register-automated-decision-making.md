# Automated Decision-Making and Profiling Register

**Document Title:** Automated Decision-Making and Profiling Register\
**Document Type:** Register\
**Version:** 1.0.3\
**Date:** 2026-06-22\
**Owner:** Chief Privacy Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](procedure-privacy-impact-and-cross-border-transfer.md), [`privacy/template-privacy-notice.md`](template-privacy-notice.md), [`privacy/procedure-data-subject-rights-management.md`](procedure-data-subject-rights-management.md), [`ai/template-ai-system-register.md`](../ai/template-ai-system-register.md), [`ai/framework-ai-governance-and-risk.md`](../ai/framework-ai-governance-and-risk.md), [`ai/procedure-ai-system-impact-assessment.md`](../ai/procedure-ai-system-impact-assessment.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Quarterly and upon material change to any registered ADM system\
**Repository Path:** [`privacy/register-automated-decision-making.md`](register-automated-decision-making.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register inventories automated decision-making and profiling activities subject to GDPR Article 22, UK GDPR Article 22, EU AI Act Articles 6 and 14, LGPD Article 20, PIPL Article 24, CPPA Section 19 (proposed), CCPA / CPRA automated decision-making rules, and equivalent provisions. It supports the transparency, human-review, and explanation rights data subjects can exercise.

A populated ADM register identifies real systems and is sensitive operational data. This template is the structural baseline; populate, classify, and store internally.

---

## Scope

This register applies to every system or workflow that takes decisions based on automated processing of personal data, including profiling, where the decision has legal or similarly significant effect on the data subject. It also applies to systems where Article 22 thresholds are not yet met but the AI Governance Council or Chief Privacy Officer has elected to register the system to maintain visibility.

In-scope examples:

1. Credit, lending, or insurance underwriting decisions.
2. Employment screening, ranking, or termination decisions.
3. Fraud and abuse detection that results in service denial.
4. Access decisions for housing, education, or essential services.
5. Pricing decisions where the price is materially driven by inferred subject characteristics.
6. Content moderation decisions that suspend, demote, or remove subjects' accounts or content.
7. AI-assisted clinical or safety decisions.

Out of scope:

1. Decisions where the AI output is one of many inputs and a human reviewer exercises material discretion.
2. Decisions producing only operational effects with no legal or similarly significant effect on the subject.

---

## Register schema

Each registered ADM activity is one row. Mandatory fields:

| Field | Description |
| --- | --- |
| ADM ID | Unique identifier |
| System name | Internal name; not vendor name |
| Owning business function | Role that owns the decision outcome |
| Privacy contact | Chief Privacy Officer or domain privacy lead assigned to this activity |
| Decision category | Underwriting, employment, fraud, access, pricing, moderation, clinical, safety, other |
| Description of the decision | Plain-language summary of what the system decides |
| Legal or similarly significant effect | Statement of why the threshold is met (or that it is not met and the system is registered voluntarily) |
| Subjects affected | Customer, employee, applicant, partner, child, patient, other |
| Personal data used | Categories of input data |
| Special-category data used | Categories where applicable |
| Model or rule basis | Statistical model, rule set, hybrid, large language model, etc. |
| Logic involved (meaningful summary) | The high-level logic in language suitable for inclusion in a privacy notice and a subject's Article 15 response |
| Significance and envisaged consequences | What the decision means for the subject |
| Lawful basis | GDPR Article 6 basis; Article 22 condition (contract necessity, consent, EU or member-state law); equivalents in other jurisdictions |
| Human review pathway | The named role and channel by which a subject can request human review |
| Human review SLA | Maximum time from request to human-review outcome |
| Explanation mechanism | How the subject is provided a meaningful explanation if requested |
| Bias and fairness assessment reference | Identifier of the most recent fairness evaluation |
| DPIA reference | Where a DPIA exists |
| AI System Register cross-reference | If the system is also in the AI System Register |
| Deployment status | Active, paused, retired |
| Last reviewed | Date |

---

## Triggers for registration

A system is registered when any of the following is true:

1. The system meets the Article 22 threshold (legal or similarly significant effect, solely or substantially automated).
2. The system falls in a category that supervisory authorities have repeatedly identified as high-risk regardless of automation degree (lending, employment, insurance, essential services access).
3. The EU AI Act classifies the system in a high-risk category under Annex III.
4. The Chief Privacy Officer determines that the system warrants registration due to scale, sensitivity, or public expectation.

---

## Subject rights and operating expectations

1. Subjects affected by a registered ADM activity are informed in the privacy notice in plain language, including the existence of the activity, the logic, the significance, and the right to human review.
2. Subjects can request human review through the channel declared on the register row. Requests are handled per the data subject rights workflow.
3. Subjects can request a meaningful explanation of the logic. The explanation is provided in plain language, with examples where helpful, within the regulatory window.
4. Subjects can request rectification of input data that influenced the decision.
5. The system's bias and fairness assessment is refreshed at least annually and after any material model or data change.
6. Material changes (new input categories, new decision categories, model version with materially different behaviour) trigger a register update and a refresh of the privacy notice content.
7. Decommissioning a system is recorded; the row is retained for the audit period.

---

## Coordination with the AI governance programme

Where an ADM system is also an AI system (most modern cases), the AI System Register is the primary inventory and this register cross-references it. The Chief Privacy Officer and the AI System Inventory Keeper jointly own the consistency between the two registers. The AI System Impact Assessment Procedure governs the impact analysis; the DPIA covers the privacy dimension.

---

## Metrics

| Metric | Definition | Target |
| --- | --- | --- |
| Register completeness | Percentage of in-scope ADM systems present on the register | 100% |
| Privacy notice coverage | Percentage of registered ADM systems disclosed in the applicable privacy notice | 100% |
| Human review SLA adherence | Percentage of human-review requests answered within the declared SLA | At least 95% |
| Explanation request SLA adherence | Percentage of explanation requests fulfilled within the regulatory window | 100% |
| Bias and fairness assessment currency | Percentage of registered ADM systems with a fairness assessment less than 12 months old | At least 95% |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| GDPR | Articles 13(2)(f), 14(2)(g), 15(1)(h), 22, Recital 71 | Information duty, access, ADM rights |
| UK GDPR | Same articles | Equivalent provisions |
| EU AI Act | Articles 6, 14, 26, Annex III | High-risk AI, human oversight, transparency |
| LGPD | Article 20 | Right to review of automated decisions |
| PIPL | Article 24 | Automated decision-making transparency and refusal |
| CPPA | Section 19 (proposed) | Automated decision system rights |
| CCPA / CPRA | Section 1798.185(a)(16) | Automated decision-making rights |
| NIST AI RMF | MAP, MEASURE, MANAGE | AI risk management functions |

---

## Limitations

This register is a CC BY-SA 4.0 structural baseline. Adopting organisations must populate the schema with real systems, validate Article 22 threshold determinations with legal counsel, and integrate the register with the AI System Register and the DPIA workflow. The register is not legal advice.

---

**End of Document**
