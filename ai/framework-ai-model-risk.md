# AI Model Risk Framework

**Document Title:** AI Model Risk Framework\
**Document Type:** Framework\
**Version:** 1.0.2\
**Date:** 2026-07-11\
**Owner:** AI Governance Approver\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/standard-ai-model-risk.md`](standard-ai-model-risk.md), [`ai/procedure-ai-model-risk-assessment.md`](procedure-ai-model-risk-assessment.md), [`ai/matrix-ai-model-risk-control-to-lifecycle-mapping.md`](matrix-ai-model-risk-control-to-lifecycle-mapping.md), [`ai/template-model-card.md`](template-model-card.md), [`ai/template-system-card.md`](template-system-card.md), [`ai/guideline-ethical-ai-use.md`](guideline-ethical-ai-use.md), [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material model, data, threat, regulatory, or assurance change\
**Repository Path:** [`ai/framework-ai-model-risk.md`](framework-ai-model-risk.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This framework defines an organization-neutral model for identifying, assessing, treating, monitoring, and evidencing risks arising from AI model behaviour, data representation, robustness, interpretability, lifecycle control, and deployment context.

The framework treats data as the primary risk surface. Model behaviour is governed through controls over data provenance, lineage, training or tuning data, retrieval sources, prompts, inference inputs, monitoring records, retention, deletion, and lifecycle evidence.

---

## Scope

This framework applies to predictive models, classification models, generative models, retrieval-augmented systems, embedding models, decision-support models, fine-tuned models, externally supplied models, and AI systems that materially influence business, security, legal, operational, customer, employee, or public outcomes.

It applies across design, data preparation, development, training, validation, deployment, monitoring, material change, incident response, re-evaluation, and retirement.

---

## Model risk domains

| Domain | Risk Description |
| --- | --- |
| Interpretability Risk | Model behaviour, influencing inputs, decision logic, or output drivers cannot be sufficiently examined for the system's risk level. |
| Representation Risk | Embeddings, latent variables, labels, features, or hidden states encode unstable, biased, sensitive, misleading, or unauthorized patterns. |
| Data Provenance Risk | Training, tuning, retrieval, evaluation, or inference data lacks documented origin, rights, lineage, quality, or permitted-use basis. |
| Adversarial Robustness Risk | Inputs, prompts, documents, perturbations, or tool outputs can cause unsafe, unintended, unauthorized, or misleading behaviour. |
| Generalization Risk | Model performance degrades outside the conditions represented in training, evaluation, or operational monitoring. |
| Alignment and Objective Risk | Outputs or behaviours diverge from approved purpose, constraints, user expectations, legal requirements, or operating boundaries. |
| Drift Risk | Data, behaviour, performance, usage, or threat conditions change after deployment without adequate detection or response. |
| Lifecycle Governance Risk | Documentation, ownership, approval, evidence, monitoring, incident response, change control, or retirement controls are incomplete. |
| Supplier Model Risk | Externally supplied models or platforms limit visibility into data use, retention, evaluation, security, monitoring, or deletion. |

---

## Inherent and residual model risk

The domains above characterize inherent model risk: the risk arising from a model's fundamental characteristics and its materiality to the organization, before controls. The risk that remains after controls, validation, and monitoring is the residual model risk. Rate each model's inherent risk from quantitative criteria (for example, the scale and growth of the affected population or process, and the potential operational, security, or financial impact) and qualitative criteria (business use, model complexity or level of autonomy, reliability of data inputs, impact on individuals, and regulatory exposure). An organization may define a negligible-risk rating category that exempts a model from the full lifecycle-governance requirements, provided the exemption is approved and tracked. This inherent-versus-residual distinction and the rating approach are adopted, sector-neutrally, from OSFI Guideline E-23 (Model Risk Management, 2025, effective 2027); the domains correspond to the risk sources catalogued in ISO/IEC 23894:2023 Annex B (among them complexity of environment, machine-learning risk sources such as continuous learning, system life-cycle issues, and technology readiness).

---

## Lifecycle control model

| Lifecycle Stage | Model Risk Focus | Evidence Class |
| --- | --- | --- |
| Design | Intended use, prohibited use, risk tier, oversight, and evaluation strategy. | Use case record, model risk classification. |
| Data Preparation | Provenance, lineage, classification, quality, representativeness, rights, retention, and deletion. | Data documentation, lineage record, rights review. |
| Development | Model architecture, features, embeddings, prompts, retrieval design, and tool boundaries. | Development record, architecture record, threat model. |
| Validation | Performance, robustness, interpretability, bias, misuse, security, privacy, and failure modes. | Validation report, adversarial evaluation, model card. |
| Deployment | Approval, access, logging, monitoring, human oversight, supplier controls, and rollback. | Deployment approval, system card, monitoring plan. |
| Monitoring | Drift, leakage, prompt injection, unsafe tool use, anomalies, incidents, and control exceptions. | Monitoring records, incident records, exception register. |
| Re-evaluation | Periodic or trigger-based review of risk, control effectiveness, data, suppliers, and evidence. | Re-evaluation report, residual risk decision. |
| Retirement | Access removal, model endpoint removal, data retention, deletion, archive, and supplier confirmation. | Retirement checklist, deletion or retention attestation. |

---

## Evaluation requirements

Model risk evaluation should be proportionate to risk and may include:

- Interpretability and explainability review.
- Feature attribution review.
- Representation and embedding analysis.
- Sensitive attribute and proxy review.
- Adversarial testing.
- Prompt injection and indirect prompt injection testing.
- Data poisoning review.
- Model inversion and membership inference exposure assessment.
- Training, tuning, retrieval, and inference data leakage testing.
- Out-of-distribution testing.
- Drift monitoring.
- Human oversight review.
- Supplier assurance review.

---

## Governance requirements

Each model or model-enabled system should have:

- Assigned owner.
- Approved purpose.
- Risk tier.
- Data provenance and lineage record.
- Model card or equivalent documentation.
- System card or equivalent deployment context documentation where applicable.
- Evaluation evidence.
- Monitoring requirements.
- Incident response linkage.
- Exception and residual risk record where applicable.
- Retirement and deletion requirements.

---

## Limitations

This framework is a CC BY-SA 4.0 baseline. It does not reproduce external framework text and does not establish legal compliance, certification, model safety, or operating effectiveness. Adopting organizations must validate requirements against their own AI systems, data categories, suppliers, jurisdictions, sectors, and risk appetite.

---

**End of Document**
