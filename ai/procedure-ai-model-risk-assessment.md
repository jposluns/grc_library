# AI Model Risk Assessment Procedure

**Document Title:** AI Model Risk Assessment Procedure\
**Document Type:** Procedure\
**Version:** 1.0.1\
**Date:** 2026-05-28\
**Owner:** AI Governance Approver\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-model-risk.md`](framework-ai-model-risk.md), [`ai/standard-ai-model-risk.md`](standard-ai-model-risk.md), [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md), [`ai/template-model-card.md`](template-model-card.md), [`ai/template-system-card.md`](template-system-card.md), [`ai/guideline-ethical-ai-use.md`](guideline-ethical-ai-use.md), [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material model, data, supplier, threat, or regulatory change\
**Repository Path:** [`ai/procedure-ai-model-risk-assessment.md`](procedure-ai-model-risk-assessment.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure defines a reusable method for assessing AI model risk. It supports consistent evaluation of data provenance, lineage, interpretability, representation, robustness, alignment, monitoring, evidence sufficiency, residual risk, and approval readiness.

---

## Scope

This procedure applies to models and model-enabled systems developed, acquired, fine-tuned, embedded, integrated, deployed, monitored, materially changed, or retired by an adopting organisation.

---

## Procedure

### Step 1: Prepare assessment

Record model purpose, owner, risk tier, lifecycle stage, deployment context, data categories, supplier involvement, intended users, prohibited uses, and assessment trigger.

### Step 2: Validate data provenance and lineage

Review training, tuning, retrieval, evaluation, prompt, inference, monitoring, and output data. Confirm origin, permitted use, classification, transformations, retention, deletion method, supplier handling, and known quality limitations.

### Step 3: Assess interpretability

Determine interpretability requirements based on risk tier and use context. Record output drivers, known limitations, explanation method, reviewability, and suitability for human oversight.

### Step 4: Assess representation and bias risk

Evaluate whether features, labels, embeddings, latent variables, or retrieval sources may encode sensitive, biased, unstable, misleading, or unauthorized patterns. Record mitigation, limitations, and residual risk.

### Step 5: Assess robustness and adversarial exposure

Assess exposure to prompt injection, indirect prompt injection, data poisoning, model inversion, membership inference, training data leakage, retrieval leakage, unsafe tool use, unauthorized extraction, and out-of-distribution behaviour.

### Step 6: Assess alignment and oversight

Evaluate whether model behaviour aligns with approved purpose, user context, legal or regulatory constraints, operational controls, human oversight, escalation paths, and prohibited uses.

### Step 7: Assess monitoring and incident linkage

Confirm monitoring for drift, misuse, leakage, unsafe outputs, unsafe tool execution, anomalous retrieval, access-control failure, supplier change, and incidents. Link model incidents to incident response and risk governance.

### Step 8: Review documentation

Confirm that model card, system card where applicable, evaluation record, data lineage record, supplier record, monitoring plan, exception record, and approval record are complete enough for the model risk tier.

### Step 9: Determine residual risk

Record unresolved risks, compensating controls, acceptance rationale, treatment actions, owner, expiry, and review date.

### Step 10: Approve, defer, reject, or retire

The accountable approval role must decide whether the model may proceed, proceed with conditions, remain in pilot, require remediation, be rejected, or be retired.

---

## Required outputs

- Model risk assessment record.
- Model card or equivalent documentation.
- System card where applicable.
- Data provenance and lineage record.
- Evaluation and test summary.
- Monitoring requirements.
- Incident and exception linkage.
- Residual risk decision.
- Approval decision.
- Next review date.

---

## Limitations

This procedure is a CC BY-SA 4.0 baseline. Adopting organisations must define specific scoring methods, evidence repositories, approval thresholds, legal review triggers, and technical test methods internally.

---

**End of Document**
