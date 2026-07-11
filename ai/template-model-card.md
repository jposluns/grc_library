# Model Card Template

**Document Title:** Model Card Template\
**Document Type:** Template\
**Version:** 1.0.2\
**Date:** 2026-07-11\
**Owner:** AI System Inventory Keeper\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-model-risk.md`](framework-ai-model-risk.md), [`ai/standard-ai-model-risk.md`](standard-ai-model-risk.md), [`ai/procedure-ai-model-risk-assessment.md`](procedure-ai-model-risk-assessment.md), [`ai/template-system-card.md`](template-system-card.md), [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI governance, model risk, or documentation change\
**Repository Path:** [`ai/template-model-card.md`](template-model-card.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template provides a reusable structure for documenting an AI model. It records purpose, ownership, data provenance, evaluation results, limitations, model risk, monitoring, approval, retention, and retirement information.

Do not populate the public repository version with real model names, system names, people names, supplier names, customer names, datasets, internal identifiers, URLs, evidence locations, or operational details.

---

## Model card fields

### 1. Model overview

| Field | Entry |
| --- | --- |
| Model Identifier | |
| Model Name | |
| Model Version | |
| Model Owner Role | |
| Data Owner Role | |
| Control Owner Role | |
| Supplier Owner Role | |
| Lifecycle Status | Proposed, pilot, production, suspended, retired. |
| Approved Purpose | |
| Prohibited Uses | |
| Risk Tier | Low, moderate, high, critical. |

### 2. Functional description

| Field | Entry |
| --- | --- |
| Model Type | Classification, prediction, generation, embedding, retrieval, ranking, optimization, agentic support, or other. |
| Inputs | |
| Outputs | |
| Output Consumers | |
| Decision Impact | |
| Human Oversight | |
| Deployment Context | Internal, external service, cloud-hosted, embedded platform, API, local, hybrid. |
| Compute Hardware | Type of compute hardware on which the model is built and run (ISO/IEC 12792:2025 §9.4.7). |
| Computational Cost | Compute cost of building and of operating the model, for example GPU-hours per input sample (ISO/IEC 12792:2025 §9.4.8). |
| Environmental Footprint | Estimated energy consumption and carbon and water footprint of training and operation (ISO/IEC 12792:2025 §7.3.2). |

### 3. Data provenance and lineage

| Field | Entry |
| --- | --- |
| Training Data Sources | |
| Tuning Data Sources | |
| Retrieval Sources | |
| Evaluation Data Sources | |
| Inference Data Categories | |
| Data Classification | |
| Permitted Use Basis | |
| Data Lineage Summary | |
| Retention Requirements | |
| Deletion Method | |
| Supplier Data Handling | |

### 4. Evaluation summary

| Field | Entry |
| --- | --- |
| Evaluation Objective | |
| Evaluation Data | |
| Performance Measures | |
| Failure Modes | |
| Known Limitations | |
| Sensitive Attribute or Proxy Review | |
| Out-of-Distribution Results | |
| Robustness Results | |
| Model Build Procedure | How the model was built after algorithmic choices: loss function, optimization procedure, training-data iteration, and any fine-tuning (ISO/IEC 12792:2025 §9.4.4). |
| Hyperparameters and Selection | Key hyperparameters and the procedure used to select their values (ISO/IEC 12792:2025 §9.4.5). |
| Knowledge Limits | Conditions under which the model is designed to operate, and the confidence threshold below which it should abstain, defer, or flag that its output is unreliable (NIST IR 8312 §2.4). |

### 5. Interpretability and representation

| Field | Entry |
| --- | --- |
| Interpretability Method | |
| Material Output Drivers | |
| Representation Analysis | |
| Bias or Disparity Indicators | |
| Bias Source Categories | Which bias sources were assessed: human and cognitive, data and statistical, and engineering-decision (ISO/IEC TR 24027:2021). |
| Review Limitations | |

### 6. Adversarial and security testing

| Field | Entry |
| --- | --- |
| Prompt Injection Exposure | |
| Indirect Prompt Injection Exposure | |
| Data Poisoning Exposure | |
| Model Inversion Exposure | |
| Membership Inference Exposure | |
| Retrieval Leakage Exposure | |
| Unsafe Tool Use Exposure | |
| Training Data Leakage Exposure | |
| Adversarial Test Summary | |
| Remediation or Acceptance | |

### 7. Monitoring and operations

| Field | Entry |
| --- | --- |
| Monitoring Method | |
| Drift Indicators | |
| Misuse Indicators | |
| Leakage Indicators | |
| Alert Thresholds | |
| Incident Response Linkage | |
| Review Cadence | |

### 8. Risk and approval

| Field | Entry |
| --- | --- |
| Residual Risks | |
| Compensating Controls | |
| Exceptions | |
| Approval Authority Role | |
| Approval Decision | Approved, approved with conditions, pilot only, deferred, rejected, retired. |
| Approval Date | |
| Next Review Date | |

### 9. Retirement and deletion

| Field | Entry |
| --- | --- |
| Retirement Trigger | |
| Access Removal | |
| Endpoint Removal | |
| Data Retention Decision | |
| Retrieval Store Deletion | |
| Log Retention Decision | |
| Supplier Deletion Confirmation | |
| Final Status | |

---

## Use notes

A model card documents model-level risk and evidence. A system card documents deployment context, integrations, users, workflows, tools, and system-level controls. Both may be required for high-risk or externally integrated AI systems.

---

**End of Document**
