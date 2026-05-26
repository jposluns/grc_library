# Data Classification and Handling Standard

**Document Title:** Data Classification and Handling Standard
**Document Type:** Standard
**Version:** 0.0.1
**Date:** 2026 05 26
**Owner:** Chief Data Officer
**Approving Authority:** Governance Library Maintainer
**Related Documents:** `privacy/policy-privacy-and-data-governance.md`, `security/policy-information-security.md`, `ai/standard-ai-security-and-risk.md`, `core/register-global-regulatory-applicability.md`
**Classification:** Public
**Category:** Information Security
**Review Frequency:** Annual and upon material data, privacy, AI, or regulatory change
**Repository Path:** `security/standard-data-classification-and-handling.md`
**Confidentiality:** Public
**Licence:** CC0 1.0 Universal

---

## Purpose

This standard defines an organization-neutral model for classifying and handling data according to confidentiality, integrity, availability, privacy, regulatory exposure, business criticality, and lifecycle obligations.

---

## Classification Levels

| Level | Description | Typical Handling Intent |
| --- | --- | --- |
| Public | Approved for unrestricted disclosure. | May be published without additional authorization. |
| Internal | Intended for internal business use. | Access limited to authorized internal roles. |
| Confidential | Unauthorized disclosure could create business, contractual, privacy, security, or operational harm. | Access restricted, monitored where appropriate, and shared only for approved purposes. |
| Restricted | Unauthorized disclosure, alteration, or loss could create material legal, regulatory, safety, financial, security, or individual impact. | Strong access control, encryption, logging, retention control, and formal approval for sharing. |

Adopting organizations may rename or extend levels, but handling rules must remain clear and enforceable.

---

## Data Categories

Data classification must consider:

- Personal data.
- Sensitive personal data.
- Employee data.
- Customer data.
- Supplier data.
- Confidential business data.
- Security telemetry.
- Authentication and authorization data.
- Financial data.
- Regulated records.
- AI training, prompt, retrieval, inference, output, evaluation, and monitoring data.
- Model weights, embeddings, system prompts, tool schemas, and model configuration data.

---

## Handling Requirements

1. Data must be classified before storage, sharing, publication, AI system use, supplier transfer, or cross-border transfer.
2. Access must be role-based and limited to authorized purposes.
3. Restricted and confidential data must be encrypted in storage and transit where feasible and appropriate.
4. Sharing must be approved, logged where required, and subject to contractual or regulatory restrictions.
5. Data retained in logs, prompts, outputs, embeddings, retrieval stores, or monitoring records must follow classification and retention rules.
6. Data must not be used for AI training, fine-tuning, retrieval, evaluation, or service improvement unless authorized and documented.
7. Data deletion must address primary records, derived datasets, embeddings, caches, backups where feasible, supplier-held copies, and logs according to documented requirements.
8. Declassification or publication must be approved by the data owner or equivalent accountable role.

---

## Evidence Requirements

Evidence may include classification records, data inventories, access approvals, transfer assessments, retention schedules, deletion records, AI data lineage records, supplier data processing terms, and exception approvals.

---

**End of Document**
