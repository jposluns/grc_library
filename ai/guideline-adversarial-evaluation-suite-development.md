# Adversarial Evaluation Suite Development Guideline

**Document Title:** Adversarial Evaluation Suite Development Guideline\
**Document Type:** Guideline\
**Version:** 1.0.2\
**Date:** 2026-07-11\
**Owner:** AI Security Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-model-risk.md`](framework-ai-model-risk.md), [`ai/standard-ai-model-risk.md`](standard-ai-model-risk.md), [`ai/procedure-ai-model-risk-assessment.md`](procedure-ai-model-risk-assessment.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`ai/template-model-card.md`](template-model-card.md), [`ai/template-system-card.md`](template-system-card.md), [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI threat, model, data, supplier, or assurance change\
**Repository Path:** [`ai/guideline-adversarial-evaluation-suite-development.md`](guideline-adversarial-evaluation-suite-development.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This guideline provides an organization-neutral method for developing adversarial evaluation suites for AI models and AI systems. It supports repeatable testing for misuse resistance, data leakage, prompt injection, unsafe tool use, robustness, and lifecycle assurance.

---

## Scope

This guideline applies to predictive models, generative models, retrieval-augmented systems, embedding systems, AI agents, external model services, and AI-enabled workflows requiring adversarial or misuse-oriented evaluation.

---

## Development method

### 1. Define evaluation objectives

Define the evaluation purpose, model or system scope, approved use, prohibited use, risk tier, users, data classes, deployment model, and required evidence.

### 2. Identify attack surfaces

Assess attack surfaces including prompts, retrieved content, uploaded files, APIs, plugins, tools, code execution, browser content, email, documents, connectors, retrieval stores, model endpoints, logs, and supplier-operated services.

### 3. Define threat scenarios

Threat scenarios should consider:

- Prompt injection.
- Indirect prompt injection.
- Data poisoning.
- Training data leakage.
- Retrieval leakage.
- Model inversion.
- Membership inference.
- Unsafe tool invocation.
- Unauthorized data extraction.
- Out-of-distribution behaviour.
- Evaluation data contamination.
- Excessive agency or automation.
- Cross-user or cross-tenant data exposure.
- Supplier control failure.

### 4. Build test cases

Each test case should define objective, target control, input design, expected safe behaviour, failure condition, evidence to capture, severity criteria, and remediation path.

### 5. Protect test data

Adversarial evaluation must not use real personal data, confidential data, customer data, supplier data, credentials, secrets, production tokens, or internal incident details in public templates or reusable test examples.

### 6. Execute and record results

Record results with sufficient detail for review without exposing sensitive prompts, system prompts, internal data, credentials, or exploit details that should remain restricted.

### 7. Determine residual risk

Classify findings, assign owners, define mitigation, determine compensating controls, and record whether residual risk is accepted, deferred, or blocking.

### 8. Update governance artefacts

Update model cards, system cards, impact assessments, risk registers, monitoring requirements, supplier reviews, and incident playbooks where findings indicate control gaps.

---

## Minimum test case fields

| Field | Description |
| --- | --- |
| Test ID | Unique internal identifier. |
| Threat Scenario | Threat or failure mode being evaluated. |
| Target Boundary | Model, retrieval, prompt, tool, data, access, supplier, or workflow boundary. |
| Test Objective | What the test is intended to determine. |
| Input Class | General class of input without sensitive details. |
| Expected Safe Behaviour | Required safe outcome. |
| Failure Condition | Behaviour that constitutes a failure. |
| Evidence Captured | Logs, output sample, decision record, monitoring signal, or reviewer notes. |
| Severity | Low, moderate, high, or critical. |
| Remediation | Required control or design change. |
| Retest Requirement | Whether retest is required before approval. |

---

## Evidence requirements

Maintain evaluation plan, test case inventory, execution summary, findings, remediation record, residual risk decision, approval record, and update log for affected model or system documentation.

---

## Informative references

| Reference | Relevance |
| --- | --- |
| NIST AI 100-2e2025 | Adversarial machine-learning attack taxonomy; the threat-scenario source (Section 3) |
| NIST SP 800-218A | PW.3.3 (include adversarial samples in training and testing data; Sections 3 and 4); PW.8 (test executable code, among which red teaming and adversarial testing; Section 6) |
| ETSI EN 304 223 V2.1.1 | Provision 5.1.3 (evaluate threats and manage risks; Sections 2 and 3); Provision 5.2.5 (appropriate testing and evaluation; Sections 6 and 7) |

---

## Limitations

This guideline is a CC BY-SA 4.0 baseline. Adopting organizations must define specific technical methods, tooling, restricted test prompts, evidence repositories, legal review triggers, and disclosure controls internally.

---

**End of Document**
