# System Card Template

**Document Title:** System Card Template\
**Document Type:** Template\
**Version:** 1.1.2\
**Date:** 2026-07-11\
**Owner:** AI System Inventory Keeper\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/framework-ai-model-risk.md`](framework-ai-model-risk.md), [`ai/template-model-card.md`](template-model-card.md), [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md), [`ai/procedure-ai-evaluation.md`](procedure-ai-evaluation.md), [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI system, supplier, data, architecture, or control change\
**Repository Path:** [`ai/template-system-card.md`](template-system-card.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template provides a reusable structure for documenting an AI system that includes one or more models, retrieval sources, tools, integrations, workflows, suppliers, or user-facing capabilities.

Do not populate the public repository version with real system names, people names, supplier names, customer names, URLs, internal identifiers, evidence locations, architecture diagrams, or operational details.

---

## System card fields

### 1. System overview

| Field | Entry |
| --- | --- |
| System Identifier | |
| System Name | |
| System Version | |
| System Owner Role | |
| Data Owner Role | |
| Control Owner Role | |
| Supplier Owner Role | |
| Lifecycle Status | Proposed, pilot, production, suspended, retired. |
| Approved Purpose | |
| Prohibited Uses | |
| Risk Tier | Low, moderate, high, critical. |

### 2. System boundary

| Field | Entry |
| --- | --- |
| User Population | |
| Business Process | |
| Deployment Model | Internal, external service, cloud-hosted, embedded platform, API, local, hybrid. |
| System Components | |
| Integrated Models | |
| Retrieval Sources | |
| Tool or Action Access | |
| Upstream Dependencies | |
| Downstream Dependencies | |
| Supplier Dependencies | |
| Cross-Jurisdiction Data Flow | Whether and how data moves between locations or jurisdictions across the system's components (ISO/IEC 12792 §8.5.5). |
| Environmental Footprint | Estimated energy consumption and carbon and water footprint of the deployed system (ISO/IEC 12792 §7.3.2). |

### 3. Data lifecycle

| Field | Entry |
| --- | --- |
| Data Inputs | |
| Data Outputs | |
| Data Transformations | |
| Prompt Data Categories | |
| Retrieval Data Categories | |
| Inference Data Categories | |
| Monitoring Data Categories | |
| Data Provenance | |
| Data Lineage | |
| Data Retention | |
| Enforceable Deletion Method | |
| Supplier Data Handling | |

### 4. Security and access controls

| Field | Entry |
| --- | --- |
| Authentication Method | |
| Authorization Model | |
| Privileged Access | |
| Service Accounts or Workload Identities | |
| API Keys, Tokens, or Secrets | |
| Logging and Monitoring | |
| Encryption and Key Management | |
| Network or Exposure Boundary | |
| Tool Permission Boundary | |
| Action Lineage Coverage | For action-capable agents: whether the audit trail links trigger, agent decision, tool invocation, system action, and resulting data or configuration change. |

### 5. AI risk and testing

| Field | Entry |
| --- | --- |
| Prompt Injection Testing | |
| Indirect Prompt Injection Testing | |
| Data Poisoning Review | |
| Model Inversion Review | |
| Membership Inference Review | |
| Retrieval Leakage Review | |
| Unsafe Tool Use Review | |
| Output Quality and Failure Modes | |
| Human Oversight Testing | |
| Resilience or Fallback Testing | |
| Reversibility Classification | For action-capable agents: per production-impacting action class, Reversible, Compensable, or Irreversible. |
| Reversal and Recovery Testing | For action-capable agents: result of testing the reversal or compensating mechanism for each Reversible or Compensable action class. |
| User Controllability | Whether a human or another external agent can intervene in the system's functioning in a timely manner (ISO/IEC 25059 §5.2). |
| Intervenability and Safe-State Transition | Mechanism to observe system state and transition from an unsafe to a safe state; a system-quality property distinct from the agentic reversibility classification above (ISO/IEC 25059 §5.7). |

### 6. Human oversight and decision impact

| Field | Entry |
| --- | --- |
| Decision Impact | |
| Human Review Point | |
| Override Authority | |
| Escalation Path | |
| User Disclosure Requirement | |
| Output Verification Requirement | |

### 7. Supplier and external service review

| Field | Entry |
| --- | --- |
| Supplier Role | |
| Data Residency | |
| Training or Improvement Use | |
| Retention Commitments | |
| Subprocessor Exposure | |
| Incident Notification | |
| Deletion and Export Capability | |
| Exit Support | |

### 8. Monitoring, incident, and change control

| Field | Entry |
| --- | --- |
| Monitoring Method | |
| Incident Indicators | |
| Escalation Criteria | |
| Change Triggers | |
| Reassessment Triggers | |
| Exception References | |
| Corrective Action References | |

### 9. Approval and review

| Field | Entry |
| --- | --- |
| Impact Assessment Status | Not started, in progress, approved, approved with conditions, rejected, retired. |
| Approval Authority Role | |
| Approval Decision | Approved, approved with conditions, pilot only, deferred, rejected, retired. |
| Approval Date | |
| Next Review Date | |
| Residual Risk Summary | |
| Production Action Authority | For action-capable agents: withheld, supervised, or granted, with a reference to the production-authority evidence record (the four preconditions per the agentic development security standard). |

### 10. Retirement and decommissioning

| Field | Entry |
| --- | --- |
| Retirement Trigger | |
| Access Removal | |
| Integration Removal | |
| Model Endpoint Removal | |
| Retrieval Store Deletion | |
| Log Retention Decision | |
| Supplier Deletion Confirmation | |
| Final Status | |

---

## Use notes

A system card documents deployment context and system-level risk. Model-level details should be recorded in model cards and linked by internal reference in adopting organizations.

---

**End of Document**
