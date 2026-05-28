# AI Model Risk Standard

**Document Title:** AI Model Risk Standard 
**Document Type:** Standard 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** AI Governance Maintainer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`ai/framework-ai-model-risk.md`](framework-ai-model-risk.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`ai/procedure-ai-model-risk-assessment.md`](procedure-ai-model-risk-assessment.md), [`ai/template-model-card.md`](template-model-card.md), [`ai/template-system-card.md`](template-system-card.md), [`ai/guideline-ethical-ai-use.md`](guideline-ethical-ai-use.md), [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md) 
**Classification:** Public 
**Category:** AI Governance 
**Review Frequency:** 6 to 12 months and upon material model, data, threat, regulatory, or assurance change 
**Repository Path:** [`ai/standard-ai-model-risk.md`](standard-ai-model-risk.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This standard defines minimum requirements for assessing and managing AI model risk. It operationalizes the AI Model Risk Framework through enforceable expectations for data provenance, interpretability, representation, robustness, alignment, monitoring, documentation, approval, and retirement.

---

## Applicability

This standard applies to models and model-enabled systems that materially affect business, security, privacy, legal, operational, financial, customer, employee, or public outcomes.

It applies to internally developed models, externally supplied models, fine-tuned models, embedded models, retrieval-augmented systems, generative systems, predictive systems, and models used through external services.

---

## Requirements

### 1. Model inventory and ownership

1. Each model or model-enabled system must be recorded in an AI system or model inventory.
2. Each model must have an assigned owner, data owner, control owner, and supplier owner where applicable.
3. Each model must have an approved purpose, prohibited use conditions, risk tier, lifecycle status, and review date.

### 2. Data provenance and lineage

1. Training, tuning, retrieval, evaluation, monitoring, and inference data must have documented provenance and permitted-use basis.
2. Data lineage must identify source, transformation, storage, access, retention, deletion, and supplier handling where applicable.
3. Sensitive, personal, regulated, confidential, or restricted data must not be used unless authorized, assessed, and controlled.
4. Data poisoning, evaluation contamination, unauthorized secondary use, and training data leakage must be considered during assessment.

### 3. Interpretability and documentation

1. Interpretability expectations must be proportionate to model risk and use context.
2. High-impact models must maintain evidence explaining material output drivers, limitations, assumptions, and known failure conditions.
3. Model cards or equivalent documentation must describe purpose, data, risk tier, evaluation results, limitations, intended use, prohibited use, monitoring, and approval status.
4. System cards or equivalent deployment-context documentation must describe integrations, users, data flows, access controls, tool access, logging, supplier dependencies, and human oversight.

### 4. Representation and bias review

1. Models using embeddings, features, labels, or latent representations must be assessed for unstable, sensitive, biased, or unauthorized patterns proportionate to risk.
2. Sensitive attribute and proxy risk must be reviewed where model outputs can materially affect individuals, groups, access, eligibility, pricing, safety, employment, finance, or regulated decisions.
3. Findings must be remediated, controlled, or accepted through documented risk governance.

### 5. Robustness and adversarial testing

Model testing must address, proportionate to risk:

- Prompt injection.
- Indirect prompt injection.
- Data poisoning.
- Model inversion.
- Membership inference.
- Training data leakage.
- Retrieval leakage.
- Unsafe tool use.
- Out-of-distribution behaviour.
- Input perturbation sensitivity.
- Unauthorized model or data extraction.

### 6. Alignment and human oversight

1. Model outputs and behaviours must be assessed against approved purpose, operating constraints, user expectations, and risk tolerance.
2. Human oversight must be defined where outputs may affect rights, access, eligibility, employment, finance, safety, security, legal exposure, or critical operations.
3. Reviewers must have authority and information sufficient to challenge, override, reject, or escalate model outputs.

### 7. Monitoring and re-evaluation

1. Deployed models must have monitoring proportionate to risk.
2. Monitoring should address performance, drift, misuse, leakage, prompt injection attempts, anomalous retrieval, unsafe tool activity, incidents, and control exceptions.
3. Re-evaluation must occur at defined cadence and upon material change to model, data, supplier, deployment context, threat pattern, or legal or regulatory context.

### 8. Incident and exception management

1. Model-related incidents must be managed through incident response.
2. Exceptions must record owner, scope, risk, rationale, compensating controls, expiry, and approval.
3. Critical or high-impact unresolved model risks must not proceed without explicit residual risk acceptance by the appropriate accountable authority.

### 9. Retirement and deletion

Retirement must address model endpoint removal, access removal, service account removal, data retention, retrieval store deletion, prompt and output log handling, evaluation artefact retention, supplier deletion confirmation, and inventory status update.

---

## Evidence requirements

Evidence should include inventory entry, model card, system card where applicable, data provenance record, lineage record, evaluation report, adversarial test summary, access review, monitoring plan, incident records, exception records, approval record, and retirement or deletion record.

---

## Limitations

This standard is original CC0 content. It does not reproduce external control text and does not establish compliance, certification, safety, or assurance by itself. Adopting organizations must validate applicability and operating effectiveness.

---

**End of Document**
