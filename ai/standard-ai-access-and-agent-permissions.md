# AI Access and Agent Permissions Standard

**Document Title:** AI Access and Agent Permissions Standard 
**Document Type:** Standard 
**Version:** 0.0.1 
**Date:** 2026-05-28 
**Owner:** AI Security Maintainer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md), [`ai/register-mcp-server.md`](register-mcp-server.md), [`ai/register-model-registry.md`](register-model-registry.md), [`ai/plan-ai-incident-response.md`](plan-ai-incident-response.md), [`security/policy-identity-and-access-management.md`](../security/policy-identity-and-access-management.md), [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md), [`security/procedure-access-control.md`](../security/procedure-access-control.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md) 
**Classification:** Public 
**Category:** AI Governance 
**Review Frequency:** Annual and upon material agent capability, threat-pattern, or supplier integration change 
**Repository Path:** [`ai/standard-ai-access-and-agent-permissions.md`](standard-ai-access-and-agent-permissions.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This standard defines the access governance for AI systems and agents: who can use which AI capability, what an AI agent is permitted to do on the user's behalf, how identity propagates through agentic actions, and how access is reviewed. It extends the identity and access management policy to the AI-specific surface where the actor is not a person but a model invoking tools.

---

## Scope

This standard applies to:

1. **Human access to AI capabilities.** Who can use an AI feature; what data flows into the model; what outputs the user receives.
2. **Service-to-AI access.** Backend systems invoking a model API; the identity, scope, and rate limits of the calling service.
3. **AI-to-tool access (agentic).** A model invoking external tools or APIs on a user's or service's behalf.
4. **AI-to-data access (retrieval and context).** A model retrieving documents, embeddings, or other context from data stores.
5. **AI-to-AI access.** A model invoking another model (orchestration, classifier cascades, ensembles).

It does not replace the general IAM policy and standards; it overlays them where the actor or the action is AI-mediated.

---

## Section 1: principles

| Principle | Statement |
| --- | --- |
| Least privilege | Each AI system, each agent capability, and each tool invocation operates with the narrowest set of permissions sufficient for the task. |
| Separation of identities | AI agents have distinct service identities from the users they serve; the agent's identity does not impersonate the user end-to-end. |
| Bounded autonomy | Agentic actions outside a defined safe envelope require human confirmation; the envelope is explicit and minimal. |
| Auditable propagation | Every tool invocation is logged with the agent identity, the user identity on whose behalf the agent acted, the tool name and arguments, and the outcome. |
| Default deny | New tools, new data scopes, new model capabilities are unavailable until explicitly approved. |
| Symmetric controls | Permissions for AI actors are reviewed and re-certified on the same cadence as human privileged access. |

---

## Section 2: human access to AI capabilities

| Control area | Requirement |
| --- | --- |
| AI feature access | Per-feature access is granted by role per the AI System Register; access reviews follow the IAM access review cadence |
| Sensitive AI features | AI features that operate on Confidential or Restricted data require additional approval per the data classification standard |
| Personal data input restrictions | Users entering personal data into an AI feature must be informed per the privacy notice; the feature must indicate the supported data classes |
| Data egress controls | DLP controls apply to AI-feature interactions; sensitive content is detected at the boundary |
| Audit | All user-AI interactions on production features are logged at the metadata level; full-content logging is restricted per privacy and risk policy |
| Termination handling | Access to AI features is revoked at the same cadence as other access on termination or transfer |

---

## Section 3: service-to-AI access

Backend services that invoke a model on behalf of the organisation:

| Control area | Requirement |
| --- | --- |
| Service identity | Each calling service has its own identity; no shared service identities across systems |
| Credential lifecycle | API keys and tokens are managed in the secrets management service; rotation per the cryptographic key lifecycle framework |
| Scope binding | The service identity is scoped to specific endpoints, models, or capabilities; cross-scope use requires explicit permission |
| Rate and cost limits | Each service identity has a rate limit and a cost ceiling consistent with capacity planning and cost governance |
| Tenancy | Where the AI provider is multi-tenant, the service identity ensures that tenant isolation holds end to end |
| Network controls | Egress from the service to the AI provider is constrained to the provider's documented endpoints |

---

## Section 4: AI-to-tool access (agentic systems)

Agentic systems where a model invokes tools (functions, APIs, scripts) on behalf of a user or service.

### 4.1 Tool allow-list

| Requirement |
| --- |
| Each agent has an explicit tool allow-list; tools not in the allow-list cannot be invoked |
| The allow-list is reviewed at minimum quarterly and at every material capability change |
| Tools are classified by risk (Read-only Low; Write Low; Write Sensitive; Destructive) per the agentic development standard |
| Tools rated Write Sensitive or Destructive require human confirmation per invocation by default |
| Tool definitions explicitly document expected input schema, side effects, and rollback behaviour where applicable |

### 4.2 Agent capability scopes

Each agent runs within a defined capability scope. Three levels are recognized:

| Scope | Definition | Approval |
| --- | --- | --- |
| Bounded | Read-only operations on a defined dataset; output to the user only | Service-owner approval |
| Operational | Read and write within a single system; defined safe actions only | AI Security Maintainer plus service-owner approval |
| Cross-system | Read or write across multiple systems; capability to chain actions | AI Security Maintainer plus CISO approval; impact assessment required |

Cross-system agents must additionally satisfy the agentic development security standard's separation-of-duty controls.

### 4.3 Identity propagation

| Control area | Requirement |
| --- | --- |
| User on whose behalf the agent acts | Identity captured at session start; propagated to every downstream call |
| Authorisation check at the tool boundary | The downstream tool authorises against the user's identity, not the agent's; the agent is the channel, not the principal |
| Agent identity for unauthenticated paths | Where the agent acts without a user (scheduled tasks, autonomous workflows), the agent has its own service identity scoped per the operational or cross-system rules above |
| Token forwarding restrictions | The agent does not pass bearer tokens beyond what the downstream tool requires |
| Sensitive credential handling | The agent does not store credentials beyond a session; secrets are retrieved from the secrets management service per invocation |

### 4.4 Human-in-the-loop confirmation

Sensitive or destructive actions require explicit human confirmation. The standard recognises three confirmation modes:

| Mode | Use case | Requirement |
| --- | --- | --- |
| Per-action confirmation | Destructive or financially material actions | The user confirms each action explicitly; standing approval is prohibited |
| Per-session confirmation | Bulk operations within a single session | The user confirms the scope at session start; the agent operates within the scope; deviations require new confirmation |
| Asynchronous approval | Workflow actions queued for later human approval | The agent produces the action plan; a separate human approves before execution |

### 4.5 Rate and chain-length limits

| Control area | Requirement |
| --- | --- |
| Rate limit per tool per session | Enforced at the agent boundary; configurable per tool classification |
| Chain-length limit | Maximum sequential tool invocations per agent session; exceeded chains halt and request human input |
| Cost ceiling per session | Inference and tool-execution cost capped per session; exceeded ceilings halt and report |
| Time-out per session | Sessions that exceed a wall-clock limit halt automatically |

### 4.6 Logging

Every agent tool invocation logs:

| Field | Description |
| --- | --- |
| Session ID | Stable identifier for the agent session |
| Agent identity | The agent's service identity |
| User identity | The user on whose behalf the agent acts; null for autonomous agents |
| Tool name | The invoked tool |
| Tool arguments | Sanitised arguments where the arguments may contain sensitive data |
| Tool outcome | Success, failure with reason, partial |
| Confirmation evidence | Where applicable; the user identity that confirmed |
| Timestamp | UTC |
| Cost | Inference cost plus tool cost where applicable |

Logs are retained per the logging and monitoring standard with a minimum AI-specific retention of 12 months.

---

## Section 5: AI-to-data access (retrieval and context)

Retrieval-augmented generation and other context-injection patterns:

| Control area | Requirement |
| --- | --- |
| Retrieval scope binding | The retrieval scope is bound to the user's identity; users cannot retrieve documents they would not otherwise be authorised to read |
| Embedding-store access control | The embedding store applies the same access control as the source documents; deleted or restricted documents propagate to embeddings within a defined window |
| Indirect prompt injection mitigations | Retrieved content is delimited and identified as untrusted in the prompt template |
| Personal data in retrieval | Personal data presence is detected; redaction or refusal applies per the consent management framework |
| Audit | Retrieval queries and returned chunks are logged per the logging standard |
| Search-result poisoning | Where retrieval consumes external content (web search, third-party knowledge bases), the content is identified as external and subjected to the same indirect-injection mitigations |

---

## Section 6: AI-to-AI access

| Control area | Requirement |
| --- | --- |
| Model-to-model invocation | Each downstream model invocation carries its own identity; orchestration is logged at every hop |
| Classifier cascade | Safety classifiers running on input or output operate on their own scope and do not see content beyond their need |
| Ensemble or routing | Routing decisions are recorded with the chosen model and the rationale |
| MCP server access | Where models access MCP servers, the access follows the MCP server register's permitted-capability list |

---

## Section 7: access review

| Review type | Cadence |
| --- | --- |
| Human access to AI features | At the IAM cadence; quarterly for privileged AI features |
| Service-to-AI service identities | Quarterly |
| Agent tool allow-lists | Quarterly; at every release that adds tools |
| Agent capability scopes | Annually for Bounded; semi-annually for Operational; quarterly for Cross-system |
| Retrieval scope bindings | Annually; ad-hoc at every material data store change |
| MCP server permitted-capability lists | Per the MCP server register |
| Logging coverage | Annually |

---

## Section 8: incident-time controls

| Trigger | Required action |
| --- | --- |
| Suspected agent compromise | Immediate suspension of the agent's autonomy; human-in-the-loop confirmation required for every action; coordination per the AI incident response plan |
| Tool credential exposure | Immediate rotation per the secrets management service; affected sessions terminated |
| Retrieval-store leak | Affected store quarantined; embeddings invalidated where required |
| Cross-tenant action observed | Affected agent disabled; impact analysis; customer notification per the contract |
| Cost or chain-length runaway | Session terminated by limits; alert generated; capability scope reviewed |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 42001:2023 | §8 operation | AI operational controls |
| EU AI Act | Articles 14, 15, 26 | Human oversight, accuracy and security, deployer obligations |
| NIST AI RMF | MANAGE | Risk management of operational AI |
| OWASP LLM Top 10 | LLM05 improper output handling; LLM06 excessive agency; LLM08 vector and embedding weaknesses | Agentic and retrieval risks |
| MITRE ATLAS | Tactics relating to tool abuse and credential access | Adversarial ML threat catalogue |
| NIST SP 800-53 Rev 5 | AC family | Access control baseline |
| ISO/IEC 27001:2022 | A.5.15 to A.5.18, A.8.2 | Access control and privileged access |

---

## Limitations

This standard is a public-domain baseline. Agentic capability is rapidly evolving; the standard expects to be revised more frequently than mature security standards. Adopting organisations adapt the tool allow-list approach, capability scopes, and human-in-the-loop confirmation modes to their specific agent platform and use cases. The standard is not a substitute for per-system threat modelling and impact assessment.

---

**End of Document**
