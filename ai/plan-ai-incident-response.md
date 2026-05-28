# AI Incident Response Plan

**Document Title:** AI Incident Response Plan 
**Document Type:** Plan 
**Version:** 0.0.1 
**Date:** 2026-05-28 
**Owner:** AI Security Maintainer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md), [`ai/guide-ai-adversarial-test-reference.md`](guide-ai-adversarial-test-reference.md), [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md), [`resilience/procedure-cross-domain-incident-coordination.md`](../resilience/procedure-cross-domain-incident-coordination.md) 
**Classification:** Public 
**Category:** AI Governance 
**Review Frequency:** Annual and upon material AI threat-pattern, regulation, or system-architecture change 
**Repository Path:** [`ai/plan-ai-incident-response.md`](plan-ai-incident-response.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This plan defines the AI-specific incident response path that operates alongside the security and privacy incident procedures. It covers prompt injection, indirect prompt injection, jailbreak, data poisoning, model inversion, membership inference, retrieval leakage, agent compromise, unsafe tool execution, hallucination causing material harm, model degradation, and supplier model incidents.

---

## Scope

This plan applies to every AI system in the AI System Register, including foundation-model-backed assistants, retrieval-augmented systems, agentic workflows, embedded inference in products, and AI-supported decision systems. It does not replace the security or privacy incident procedures; it integrates with them under the cross-domain coordination procedure when an AI incident also involves personal data or general security.

---

## AI incident classes and triggers

| Class | Detection triggers |
| --- | --- |
| Prompt injection (direct) | User input attempting to override system prompt; refusal-rate anomalies; SIEM alert on adversarial-pattern matches |
| Prompt injection (indirect) | Retrieved content containing instructions; output behaviour matching injected directive |
| Jailbreak | Refusal-bypass output; safety-classifier alert |
| Data poisoning | Training-data anomaly; sudden behaviour shift after fine-tune; integrity verification failure on training corpus |
| Model inversion or membership inference | Output containing verbatim training-data segments; targeted query patterns; researcher disclosure |
| Retrieval leakage | Retrieval-store access by unauthorised query; query-log review revealing unexpected matches |
| Agent compromise | Tool invocation outside the agent's permitted scope; rate or chain-length limits triggered; tool credentials used outside expected context |
| Unsafe tool execution | Destructive tool call without confirmation; cross-tenant action; data exfiltration via tool |
| Hallucination causing harm | Customer complaint; downstream-system failure attributable to AI-generated content; legal or safety review |
| Model degradation | Eval-suite regression beyond threshold; production-metric degradation; drift detection |
| Supplier model incident | Vendor security advisory; vendor outage; vendor disclosure of training-data exposure |

---

## Severity criteria

| Severity | Criteria | Examples |
| --- | --- | --- |
| P1 | Active exfiltration of personal or regulated data via AI; agent in production performing unauthorised actions at scale; safety-critical AI returning incorrect outputs with confirmed harm; coordinated jailbreak campaign against a customer-facing assistant | Multi-customer data exfiltration through indirect prompt injection; agent issued unauthorised payments |
| P2 | Suspected breach via AI vector; agent isolated incident with limited blast radius; degradation outside tolerance | Single-tenant prompt injection success without confirmed exfiltration |
| P3 | AI safety event with no operational impact; localised behaviour regression | Eval-suite regression on a non-customer model |
| P4 | False positive; reproducible-only-by-researcher edge case | Lab-only proof of concept with no production exposure |

The Joint Command convenes for P1 within 60 minutes of declaration; P2 within 8 business hours; P3 by next business day.

---

## Lifecycle

The AI incident lifecycle mirrors the security incident lifecycle with AI-specific actions at each phase.

### 1. Detect

| Source | AI-specific signal |
| --- | --- |
| Eval suite | Out-of-tolerance regression on a safety, accuracy, or refusal metric |
| Production monitoring | Alert on injection patterns, output classifiers, rate or chain-length triggers |
| User report | Customer complaint about output; researcher disclosure |
| Supplier notification | Vendor advisory or breach disclosure |
| Threat intelligence | Public disclosure of new attack technique against the platform |
| Internal red team | Confirmed exploitation during testing |
| Cost or telemetry anomaly | Unexpected inference cost or token consumption pattern |

### 2. Triage

Validate the signal. Confirm:

1. AI system identifier, version, and supplier from the AI System Register.
2. Production exposure: customer-facing, internal, or pre-production.
3. Severity criteria met; declare per the matrix above.
4. Whether personal data is implicated (engages the privacy stream).
5. Whether agent capability is implicated (engages the agent-permission stream).
6. Initial preservation: snapshot of prompts, retrieved content, model responses, tool invocation logs, embeddings if relevant, full session context.

### 3. Contain

AI-specific containment actions, applied per the severity and the system architecture:

| Action | When to use |
| --- | --- |
| Disable the specific capability (single tool, single skill, single endpoint) | Targeted containment without full disable |
| Disable agent autonomy (require human confirmation for every tool call) | Active agent compromise; preserves observability |
| Suspend the specific model version | Model degradation or supplier advisory |
| Suspend retrieval from the affected store | Retrieval leakage |
| Suspend training or fine-tuning pipeline | Suspected poisoning |
| Suspend the entire AI feature | P1 with broad exposure |
| Rotate API keys, model-provider credentials, retrieval-store credentials | Credential compromise suspected |
| Block specific input patterns at the gateway | Direct prompt injection campaign |
| Quarantine specific retrieved documents | Indirect prompt injection through known retrieved source |

### 4. Investigate

| Step | AI-specific investigation actions |
| --- | --- |
| Timeline reconstruction | Compose timeline including prompt history, retrieved content, tool calls, output evaluation results |
| Attack vector identification | Map to OWASP LLM Top 10 and MITRE ATLAS tactic and technique |
| Blast radius | Identify all affected sessions, customers, downstream systems, datasets, derived models |
| Evidence preservation | Prompt logs, retrieved content, model output, tool invocation logs, embeddings, training-data snapshot if poisoning suspected, eval results, dashboards |
| Lineage analysis | Trace from compromised system back to training data, fine-tuning data, retrieval source, prompt template, agent capability definition |
| Customer impact analysis | Per affected customer: data exposed, output relied upon, action taken on the basis of the output |

### 5. Eradicate

| Action | When |
| --- | --- |
| Patch prompt template; deploy patched version | Direct prompt injection |
| Update retrieved-content allow list; sanitise quarantined documents | Indirect prompt injection |
| Update agent tool allow list and confirmation rules | Agent compromise |
| Rotate compromised credentials | Credential exposure |
| Retire compromised model version; revert to a clean prior version | Poisoning or degradation |
| Update safety classifier; redeploy with updated thresholds | Repeated jailbreak success |
| Engage supplier; receive patched model | Supplier-disclosed vulnerability |
| Retrain or fine-tune from a clean dataset | Confirmed training-data poisoning |

### 6. Recover

| Step | AI-specific recovery actions |
| --- | --- |
| Validate model on the eval suite | Pre-restoration check |
| Stage rollout with canary | Avoid full re-exposure on day one |
| Re-enable capabilities incrementally | Targeted re-enable in reverse order of containment |
| Monitor with enhanced alerting | At minimum 14 days post-incident |
| Customer notification where required | Coordinate with the Communications Lead |
| Regulator notification where applicable | Coordinate with the Privacy Officer and Legal |

### 7. Post-incident review

The AI Security Maintainer leads a PIR within 10 business days for P1 and P2 events. The PIR additionally covers:

1. Whether the existing AI threat model anticipated the vector and whether the threat model needs updating.
2. Whether the eval suite would have detected the regression (and if not, what new evals to add).
3. Whether the AI System Register was complete and current at the time of the incident.
4. Whether the supplier's contractual obligations were met and whether contract terms need to change.
5. Lessons for the agent permission framework, the MCP server register, and the training data governance procedure.
6. Update to the AI Risk Register.

---

## Coordination with other streams

| Stream | When it engages |
| --- | --- |
| Security incident response | Any P1 or P2 AI incident that also affects general IT security |
| Privacy breach response | Any AI incident where personal data is implicated |
| Supplier incident management | Supplier-originated AI incidents |
| Cross-domain incident coordination | When two or more streams are active |
| AI Governance Council | All P1 events; AI Risk Register updates |

---

## Evidence requirements

The AI Security Maintainer ensures that the following evidence is preserved for every P1 or P2 incident:

| Evidence class | Detail |
| --- | --- |
| Prompt logs | Full session prompts with timestamps |
| Retrieved content | Documents and chunks retrieved during the relevant sessions |
| Model output | Responses with safety-classifier annotations |
| Tool invocation logs | Tool name, arguments, return value, confirmation status |
| Embeddings and vectors | Where relevant to retrieval leakage or membership inference |
| Training data snapshot | Where poisoning is suspected |
| Model version metadata | Identifier, hash, supplier, deployment date |
| Eval suite results | Pre-incident baseline and post-incident regression |
| Cost and telemetry | Inference cost, token consumption, latency anomalies |
| Communications | All coordination decisions and external messaging |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| OWASP LLM Top 10 (2025) | LLM01 to LLM10 | Threat taxonomy |
| MITRE ATLAS | Tactics and techniques | Adversarial ML threat catalogue |
| NIST AI RMF | MANAGE function | AI incident management |
| ISO/IEC 42001:2023 | §9, §10 | AI management system performance and improvement |
| EU AI Act | Articles 15, 17, 26 | Security, quality management, deployer obligations |
| ISO/IEC 27035-3 | Information security incident response | Underlying IR practice |

---

## Limitations

This plan is a public-domain baseline. Adopting organisations populate per-system AI incident playbooks, eval-suite specifics, supplier contact rosters, and regulatory-notification matrices. AI incident response is rapidly maturing; the plan is expected to evolve as new threat patterns emerge.

---

**End of Document**
