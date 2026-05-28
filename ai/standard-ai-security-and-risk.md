# AI Security and Risk Standard

**Document Title:** AI Security and Risk Standard 
**Document Type:** Standard 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** AI Security Maintainer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md), [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md), [`ai/register-ai-risk.md`](register-ai-risk.md), [`ai/guideline-ethical-ai-use.md`](guideline-ethical-ai-use.md), [`security/procedure-access-control.md`](../security/procedure-access-control.md), [`security/procedure-identity-management.md`](../security/procedure-identity-management.md), [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md) 
**Classification:** Public 
**Category:** AI Governance 
**Review Frequency:** 6 to 12 months and upon material AI threat, framework, or regulatory change 
**Repository Path:** [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This standard defines minimum security and risk requirements for AI systems. It is original repository content informed by common AI, cloud, privacy, and security assurance practices and does not reproduce restricted third-party control or questionnaire text.

---

## Applicability

This standard applies to AI systems that create, process, retrieve, infer, classify, generate, recommend, automate, summarize, translate, code, reason, or trigger actions using organizational or user-provided data.

The standard applies regardless of whether the AI system is internally developed, externally hosted, embedded in a commercial platform, accessed through an API, used through a browser, deployed as a local model, or operated by a supplier.

---

## Minimum requirements

### 1. Inventory and ownership

1. Each AI system must be recorded in the AI System Register before production use.
2. Each AI system must have an assigned AI System Owner, Data Owner, Control Owner, and Supplier Owner where applicable.
3. Each AI system must have a documented business purpose, approved use case, prohibited use conditions, lifecycle status, and review date.

### 2. Data governance

1. Data used by the AI system must be classified before use.
2. Data provenance must be documented for training, fine-tuning, retrieval, prompt, inference, monitoring, and evaluation data.
3. Data lineage must identify source, transformation, storage location, access path, retention period, and deletion method.
4. Sensitive data must not be used unless authorized, risk-assessed, and controlled.
5. Data used in prompts, files, retrieval stores, vector databases, logs, model evaluations, and monitoring must follow retention and deletion rules.
6. The system must not use organizational data for external model training or provider improvement unless explicitly approved and documented.

### 3. Identity and access control

1. Access to AI systems must use approved identity and access management processes.
2. Privileged administrative access must be restricted, logged, and reviewed.
3. API keys, tokens, service accounts, plugins, agents, and tool permissions must be inventoried and rotated according to risk.
4. Access to prompts, outputs, logs, retrieval stores, model endpoints, datasets, and evaluation records must be restricted by need to know.

### 4. Prompt, retrieval, and tool security

1. Systems using user prompts, retrieved content, documents, browser data, email, tickets, repositories, or web content must be assessed for prompt injection exposure.
2. Systems with tool use, code execution, workflow execution, transaction initiation, or external API access must define allowed actions and denial conditions.
3. Tool outputs must not be treated as trusted instructions without validation.
4. Retrieval content must be permission-filtered and must not expose data across users, roles, tenants, customers, or business contexts.
5. System prompts, policy prompts, guardrail instructions, and tool schemas must be protected from unauthorized disclosure and modification.

### 5. Model and data attack resistance

Controls must address, proportionate to risk:

- Prompt injection.
- Indirect prompt injection.
- Data poisoning.
- Training data leakage.
- Retrieval data leakage.
- Model inversion.
- Membership inference.
- Jailbreak attempts.
- Unsafe tool invocation.
- Cross-context data exposure.
- Unauthorized model extraction.
- Evaluation data contamination.

### 6. Testing and validation

1. AI systems must be tested before release and after material change. "Material" is defined by the Material change thresholds table in [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md).
2. Test coverage must include intended use, prohibited use, security boundaries, data leakage, access control, prompt injection, unsafe outputs, failure modes, and monitoring triggers.
3. High-risk AI systems must include adversarial or misuse testing proportionate to the impact of failure.
4. Test results must be retained as evidence.
5. Known limitations must be documented and communicated to users and control owners.
6. Testing and validation documentation requirements are governed by [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md).

### 7. Monitoring and logging

1. AI system usage must be logged according to risk, privacy, and retention requirements.
2. Logs must support investigation of misuse, leakage, unauthorized access, system drift, unexpected tool execution, and incident response.
3. Monitoring must include anomaly detection or review processes for high-risk systems.
4. Monitoring must not create unnecessary sensitive data retention.

### 8. Human oversight

1. Human review is required where AI outputs may materially affect rights, eligibility, access, employment, finances, safety, regulatory reporting, or critical business operations.
2. Human reviewers must receive enough context to challenge, override, or reject outputs.
3. Automation boundaries must be documented.
4. Users must not be led to treat probabilistic outputs as authoritative evidence without verification.

### 9. Supplier and external service controls

External AI services must be assessed for:

- Data retention.
- Training or improvement use.
- Subprocessors.
- Data residency.
- Access control.
- Logging.
- Encryption.
- Incident notification.
- Deletion and export capability.
- Service continuity.
- Exit support.
- Contractual control commitments.

### 10. Incident and exception management

1. AI incidents must be classified and escalated through incident management.
2. AI-specific incidents include unauthorized disclosure, unexpected data retention, prompt injection success, unsafe tool execution, unauthorized model use, data poisoning, material output failure, and policy bypass.
3. Exceptions must have owner, risk level, justification, compensating controls, expiry, and approval.
4. High-risk exceptions must require independent review.

### 11. Decommissioning

AI systems must be retired with controls for:

- Access removal.
- API key revocation.
- Dataset retention or deletion.
- Retrieval store deletion.
- Log retention decisions.
- Supplier deletion confirmation where applicable.
- Integration removal.
- Monitoring closure.
- Register status update.

---

## Evidence requirements

At minimum, each AI system should maintain:

- AI system register entry.
- Impact assessment.
- Data classification record.
- Data provenance and lineage record.
- Access review.
- Supplier assessment where applicable.
- Test results.
- Monitoring plan.
- Incident and exception records where applicable.
- Decommissioning record when retired.

---

## Compliance notes

This standard does not establish legal compliance or certification. It defines a reusable security and risk baseline. Adopting organizations must validate requirements against applicable laws, sector obligations, contracts, deployment architecture, data categories, and risk appetite.

---

**End of Document**
