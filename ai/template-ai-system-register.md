# AI System Register Template

**Document Title:** AI System Register Template\
**Document Type:** Template\
**Version:** 1.1.0\
**Date:** 2026-06-19\
**Owner:** AI System Inventory Keeper\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md), [`ai/register-ai-risk.md`](register-ai-risk.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI governance change\
**Repository Path:** [`ai/template-ai-system-register.md`](template-ai-system-register.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template defines a reusable structure for recording AI systems, owners, risk tiering, lifecycle status, data categories, suppliers, controls, approvals, and evidence. It must be adapted by adopting organisations before use in an internal environment.

Do not populate this public template with real systems, company names, personal names, customer names, suppliers, internal identifiers, data samples, or incident details.

---

## Register fields

| Field | Description | Required |
| --- | --- | --- |
| System ID | Organisation-defined identifier. Use a non-sensitive identifier. | Yes |
| System Name | Name of the AI system. Avoid sensitive naming in public artefacts. | Yes |
| Business Purpose | Approved purpose and business process. | Yes |
| Lifecycle Status | Proposed, pilot, production, suspended, retired. | Yes |
| AI Capability Type | Classification, prediction, generation, retrieval, automation, agentic workflow, decision support, monitoring, or other. | Yes |
| System Owner | Role accountable for the system. | Yes |
| Data Owner | Role accountable for data used by the system. | Yes |
| Control Owner | Role accountable for control implementation and evidence. | Yes |
| Supplier Owner | Role accountable for external provider oversight, where applicable. | Conditional |
| Deployment Model | Internal, external service, cloud-hosted, embedded platform, API, local model, hybrid. | Yes |
| User Population | Internal users, external users, customers, suppliers, public users, service accounts. | Yes |
| Data Categories | Personal, sensitive, confidential, regulated, public, synthetic, operational, security, financial, employee, customer. | Yes |
| Data Provenance | Source and rights basis for data use. | Yes |
| Data Lineage | Data flow, transformation, storage, retrieval, and deletion path. | Yes |
| Training or Improvement Use | Whether submitted or stored data is used for training, fine-tuning, provider improvement, or evaluation. | Yes |
| Retrieval Sources | Document stores, vector stores, databases, applications, memory sources, or knowledge bases accessed by the system. | Conditional |
| Tool Access | APIs, plugins, code execution, workflow actions, transaction actions, or external system actions. | Conditional |
| Reversibility Classification | For action-capable agents: per production-impacting action class, Reversible, Compensable, or Irreversible, per the agentic development security standard. | Conditional |
| Recovery Test Status | For action-capable agents: not required, planned, passed, or failed, for the reversal or compensating mechanism of each Reversible or Compensable action class. | Conditional |
| Production Action Authority | For action-capable agents: withheld, supervised, or granted, with a reference to the production-authority evidence record. | Conditional |
| Action Lineage Coverage | For action-capable agents: whether the audit trail links trigger, agent decision, tool invocation, system action, and resulting data or configuration change. | Conditional |
| Risk Tier | Low, moderate, high, critical. | Yes |
| Impact Assessment Status | Not started, in progress, approved, approved with conditions, rejected, retired. | Yes |
| Human Oversight | Required reviewer, review point, escalation path, and override authority. | Conditional |
| Security Testing Status | Not required, planned, complete, failed, remediation required. | Yes |
| Monitoring Method | Logs, alerts, sampling, review queue, drift monitoring, misuse monitoring, incident reporting. | Yes |
| Supplier Assessment Status | Not applicable, required, in progress, approved, rejected, expired. | Conditional |
| Exception Reference | Link or identifier for any approved deviation. | Conditional |
| Approval Authority | Role approving use. | Yes |
| Approval Date | Date of approval. | Conditional |
| Next Review Date | Date for periodic review. | Yes |
| Retirement Date | Date retired, where applicable. | Conditional |
| Deletion Confirmation | Confirmation that data, logs, retrieval stores, keys, access, and supplier-held records were handled. | Conditional |

---

## Example empty register table

| System ID | System Name | Lifecycle Status | Owner Role | Data Categories | Deployment Model | Risk Tier | Impact Assessment Status | Supplier Assessment Status | Next Review Date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | Proposed | | | | | Not started | Not applicable | |

---

## Review questions

1. Is the system recorded before use?
2. Is the business purpose approved and specific?
3. Are prohibited uses documented?
4. Is data provenance known?
5. Is data lineage documented across collection, storage, processing, inference, monitoring, retention, and deletion?
6. Is provider training or improvement use prohibited, controlled, or explicitly approved?
7. Are prompt injection, data poisoning, leakage, model inversion, membership inference, and unsafe tool use considered?
8. Is access to prompts, outputs, logs, retrieval stores, datasets, and tools controlled?
9. Is human oversight sufficient for the impact level?
10. Are supplier commitments documented and reviewable?
11. Are monitoring and incident response defined?
12. Is decommissioning feasible and evidenced?

---

**End of Document**
