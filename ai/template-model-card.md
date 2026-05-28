# Model Card Template

**Document Title:** Model Card Template  
**Document Type:** Template  
**Version:** 0.0.2  
**Date:** 2026-05-27  
**Owner:** AI Governance Maintainer  
**Approving Authority:** Governance Library Maintainer  
**Related Documents:** [`ai/framework-ai-model-risk.md`](framework-ai-model-risk.md), [`ai/standard-ai-model-risk.md`](standard-ai-model-risk.md), [`ai/procedure-ai-model-risk-assessment.md`](procedure-ai-model-risk-assessment.md), [`ai/template-system-card.md`](template-system-card.md), [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md)  
**Classification:** Public  
**Category:** AI Governance  
**Review Frequency:** 6 to 12 months and upon material AI governance, model risk, or documentation change  
**Repository Path:** [`ai/template-model-card.md`](template-model-card.md)  
**Confidentiality:** Public  
**Licence:** CC0 1.0 Universal  

---

## Purpose

This template provides a reusable structure for documenting an AI model. It records purpose, ownership, data provenance, evaluation results, limitations, model risk, monitoring, approval, retention, and retirement information.

Do not populate the public repository version with real model names, system names, people names, supplier names, customer names, datasets, internal identifiers, URLs, evidence locations, or operational details.

---

## Model Card Fields

### 1. Model Overview

| Field | Entry |
| --- | --- |
| Model Identifier |  |
| Model Name |  |
| Model Version |  |
| Model Owner Role |  |
| Data Owner Role |  |
| Control Owner Role |  |
| Supplier Owner Role |  |
| Lifecycle Status | Proposed, pilot, production, suspended, retired. |
| Approved Purpose |  |
| Prohibited Uses |  |
| Risk Tier | Low, moderate, high, critical. |

### 2. Functional Description

| Field | Entry |
| --- | --- |
| Model Type | Classification, prediction, generation, embedding, retrieval, ranking, optimization, agentic support, or other. |
| Inputs |  |
| Outputs |  |
| Output Consumers |  |
| Decision Impact |  |
| Human Oversight |  |
| Deployment Context | Internal, external service, cloud-hosted, embedded platform, API, local, hybrid. |

### 3. Data Provenance and Lineage

| Field | Entry |
| --- | --- |
| Training Data Sources |  |
| Tuning Data Sources |  |
| Retrieval Sources |  |
| Evaluation Data Sources |  |
| Inference Data Categories |  |
| Data Classification |  |
| Permitted Use Basis |  |
| Data Lineage Summary |  |
| Retention Requirements |  |
| Deletion Method |  |
| Supplier Data Handling |  |

### 4. Evaluation Summary

| Field | Entry |
| --- | --- |
| Evaluation Objective |  |
| Evaluation Data |  |
| Performance Measures |  |
| Failure Modes |  |
| Known Limitations |  |
| Sensitive Attribute or Proxy Review |  |
| Out-of-Distribution Results |  |
| Robustness Results |  |

### 5. Interpretability and Representation

| Field | Entry |
| --- | --- |
| Interpretability Method |  |
| Material Output Drivers |  |
| Representation Analysis |  |
| Bias or Disparity Indicators |  |
| Review Limitations |  |

### 6. Adversarial and Security Testing

| Field | Entry |
| --- | --- |
| Prompt Injection Exposure |  |
| Indirect Prompt Injection Exposure |  |
| Data Poisoning Exposure |  |
| Model Inversion Exposure |  |
| Membership Inference Exposure |  |
| Retrieval Leakage Exposure |  |
| Unsafe Tool Use Exposure |  |
| Training Data Leakage Exposure |  |
| Adversarial Test Summary |  |
| Remediation or Acceptance |  |

### 7. Monitoring and Operations

| Field | Entry |
| --- | --- |
| Monitoring Method |  |
| Drift Indicators |  |
| Misuse Indicators |  |
| Leakage Indicators |  |
| Alert Thresholds |  |
| Incident Response Linkage |  |
| Review Cadence |  |

### 8. Risk and Approval

| Field | Entry |
| --- | --- |
| Residual Risks |  |
| Compensating Controls |  |
| Exceptions |  |
| Approval Authority Role |  |
| Approval Decision | Approved, approved with conditions, pilot only, deferred, rejected, retired. |
| Approval Date |  |
| Next Review Date |  |

### 9. Retirement and Deletion

| Field | Entry |
| --- | --- |
| Retirement Trigger |  |
| Access Removal |  |
| Endpoint Removal |  |
| Data Retention Decision |  |
| Retrieval Store Deletion |  |
| Log Retention Decision |  |
| Supplier Deletion Confirmation |  |
| Final Status |  |

---

## Use Notes

A model card documents model-level risk and evidence. A system card documents deployment context, integrations, users, workflows, tools, and system-level controls. Both may be required for high-risk or externally integrated AI systems.

---

**End of Document**
