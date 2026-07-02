# AI Security and Risk Standard

**Document Title:** AI Security and Risk Standard\
**Document Type:** Standard\
**Version:** 1.1.2\
**Date:** 2026-07-02\
**Owner:** AI Security Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md), [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md), [`ai/register-ai-risk.md`](register-ai-risk.md), [`ai/guideline-ethical-ai-use.md`](guideline-ethical-ai-use.md), [`security/procedure-access-control.md`](../security/procedure-access-control.md), [`security/procedure-identity-management.md`](../security/procedure-identity-management.md), [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI threat, framework, or regulatory change\
**Repository Path:** [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines minimum security and risk requirements for AI systems. It is original repository content informed by common AI, cloud, privacy, and security assurance practices and does not reproduce restricted third-party control or questionnaire text.

---

## 2. Applicability

This standard applies to AI systems that create, process, retrieve, infer, classify, generate, recommend, automate, summarize, translate, code, reason, or trigger actions using organizational or user-provided data.

The standard applies regardless of whether the AI system is internally developed, externally hosted, embedded in a commercial platform, accessed through an API, used through a browser, deployed as a local model, or operated by a supplier.

---

## 3. Relationship to the AI and Agentic Development Security Standard

This standard and the [`AI and Agentic Development Security Standard`](standard-ai-and-agentic-development-security.md) both govern AI security, at different altitudes, and they apply cumulatively.

- **This standard is the governance-level baseline.** It sets the minimum security and risk requirements (the *what*) that apply to every AI system in scope, expressed as outcome obligations.
- **The AI and Agentic Development Security Standard is the technical and agentic-runtime implementation layer.** It provides the detailed *how*: a threat model, coded controls, secure-by-default parameters, and CI/CD gates for development of AI, agentic, RAG, and MCP systems.

**Precedence.** A system in scope of both standards must satisfy both. Where both address the same topic, the AI and Agentic Development Security Standard's more specific technical control governs the implementation, and this standard's requirement remains the minimum that implementation must satisfy. Neither standard relaxes the other, and a control present in only one standard applies on its own terms. (This mirrors the "more specific control governs" rule the AI and Agentic Development Security Standard already applies internally at its OFFAI-SEC-02 control.)

**Crosswalk.** The following maps this standard's requirement areas (cited by this standard's own section numbers) to the corresponding sections of the AI and Agentic Development Security Standard (cited by section name, since they belong to that document; consult it for the controlling technical detail).

| Topic area | This standard (governance baseline) | AI and Agentic Development Security Standard (technical implementation) |
| --- | --- | --- |
| Inventory and ownership | §4.1 Inventory and ownership | Model governance requirements; Agent production authority, reversibility, and recovery |
| Data governance | §4.2 Data governance | Data security requirements |
| Identity and access control | §4.3 Identity and access control | Agent security requirements; Secret handling requirements |
| Prompt, retrieval, and tool security | §4.4 Prompt, retrieval, and tool security | Mandatory input and output controls; RAG security requirements; MCP security requirements; Prompt security requirements |
| Model and data attack resistance | §4.5 Model and data attack resistance | Threat model; Threat classes |
| Testing and validation | §4.6 Testing and validation | Security testing requirements; Adversarial testing requirements; Red team requirements |
| Monitoring and logging | §4.7 Monitoring and logging | AI observability and telemetry; Logging and audit requirements |
| Human oversight | §4.8 Human oversight | Human approval boundaries; Autonomous action constraints |
| Supplier and external service controls | §4.9 Supplier and external service controls | AI supply chain security |
| Incident and exception management | §4.10 Incident and exception management | Incident detection and response |
| Decommissioning | §4.11 Decommissioning | No dedicated counterpart; the closest are data-retention and memory-purge controls found elsewhere in that standard, which do not amount to a dedicated decommissioning counterpart. This area is governed by this standard. |
| Evidence | Evidence requirements | Verification and enforcement |

Sections of the AI and Agentic Development Security Standard with no counterpart here (technical and agentic-runtime controls beyond this baseline's scope) include its trust zones, security architecture principles, secure-by-default requirements, prohibited engineering patterns, AI-assisted development controls, context isolation, memory security, runtime enforcement, infrastructure security, CI/CD pipeline controls, secure agent orchestration, sandbox and isolation, and AI-driven offensive security tooling governance; they apply on their own terms to systems in their scope.

---

## 4. Minimum requirements

### 4.1 Inventory and ownership

1. Each AI system must be recorded in the AI System Register before production use.
2. Each AI system must have an assigned AI System Owner, Data Owner, Control Owner, and Supplier Owner where applicable.
3. Each AI system must have a documented business purpose, approved use case, prohibited use conditions, lifecycle status, and review date.

### 4.2 Data governance

1. Data used by the AI system must be classified before use.
2. Data provenance must be documented for training, fine-tuning, retrieval, prompt, inference, monitoring, and evaluation data.
3. Data lineage must identify source, transformation, storage location, access path, retention period, and deletion method.
4. Sensitive data must not be used unless authorized, risk-assessed, and controlled.
5. Data used in prompts, files, retrieval stores, vector databases, logs, model evaluations, and monitoring must follow retention and deletion rules.
6. The system must not use organizational data for external model training or provider improvement unless explicitly approved and documented.

### 4.3 Identity and access control

1. Access to AI systems must use approved identity and access management processes.
2. Privileged administrative access must be restricted, logged, and reviewed.
3. API keys, tokens, service accounts, plugins, agents, and tool permissions must be inventoried and rotated according to risk.
4. Access to prompts, outputs, logs, retrieval stores, model endpoints, datasets, and evaluation records must be restricted by need to know.

### 4.4 Prompt, retrieval, and tool security

1. Systems using user prompts, retrieved content, documents, browser data, email, tickets, repositories, or web content must be assessed for prompt injection exposure.
2. Systems with tool use, code execution, workflow execution, transaction initiation, or external API access must define allowed actions and denial conditions.
3. Tool outputs must not be treated as trusted instructions without validation.
4. Retrieval content must be permission-filtered and must not expose data across users, roles, tenants, customers, or business contexts.
5. System prompts, policy prompts, guardrail instructions, and tool schemas must be protected from unauthorized disclosure and modification.

### 4.5 Model and data attack resistance

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

### 4.6 Testing and validation

1. AI systems must be tested before release and after material change. "Material" is defined by the Material change thresholds table in [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md).
2. Test coverage must include intended use, prohibited use, security boundaries, data leakage, access control, prompt injection, unsafe outputs, failure modes, and monitoring triggers.
3. High-risk AI systems must include adversarial or misuse testing proportionate to the impact of failure.
4. Test results must be retained as evidence.
5. Known limitations must be documented and communicated to users and control owners.
6. Testing and validation documentation requirements are governed by [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md).

### 4.7 Monitoring and logging

1. AI system usage must be logged according to risk, privacy, and retention requirements.
2. Logs must support investigation of misuse, leakage, unauthorized access, system drift, unexpected tool execution, and incident response.
3. Monitoring must include anomaly detection or review processes for high-risk systems.
4. Monitoring must not create unnecessary sensitive data retention.

### 4.8 Human oversight

1. Human review is required where AI outputs may materially affect rights, eligibility, access, employment, finances, safety, regulatory reporting, or critical business operations.
2. Human reviewers must receive enough context to challenge, override, or reject outputs.
3. Automation boundaries must be documented.
4. Users must not be led to treat probabilistic outputs as authoritative evidence without verification.

### 4.9 Supplier and external service controls

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

### 4.10 Incident and exception management

1. AI incidents must be classified and escalated through incident management.
2. AI-specific incidents include unauthorized disclosure, unexpected data retention, prompt injection success, unsafe tool execution, unauthorized model use, data poisoning, material output failure, and policy bypass.
3. Exceptions must have owner, risk level, justification, compensating controls, expiry, and approval.
4. High-risk exceptions must require independent review.

### 4.11 Decommissioning

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

## 5. Evidence requirements

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

## 6. Compliance notes

This standard does not establish legal compliance or certification. It defines a reusable security and risk baseline. Adopting organizations must validate requirements against applicable laws, sector obligations, contracts, deployment architecture, data categories, and risk appetite.

---

**End of Document**
