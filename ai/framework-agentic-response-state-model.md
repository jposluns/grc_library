# Agentic Response State Model Framework

**Document Title:** Agentic Response State Model Framework\
**Document Type:** Framework\
**Version:** 0.0.2\
**Date:** 2026-08-31\
**Owner:** AI Governance Approver\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/plan-ai-incident-response.md`](plan-ai-incident-response.md), [`ai/standard-ai-human-oversight.md`](standard-ai-human-oversight.md), [`ai/standard-ai-access-and-agent-permissions.md`](standard-ai-access-and-agent-permissions.md), [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md), [`operations/procedure-threat-intelligence-and-siem-operations.md`](../operations/procedure-threat-intelligence-and-siem-operations.md), [`governance/principle-capability-is-not-authority.md`](../governance/principle-capability-is-not-authority.md), [`governance/principle-fail-closed-automation.md`](../governance/principle-fail-closed-automation.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`governance/register-canonical-citations.md`](../governance/register-canonical-citations.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI, threat, or regulatory change\
**Repository Path:** [`ai/framework-agentic-response-state-model.md`](framework-agentic-response-state-model.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This framework defines a state model for automated (agentic) response to a detected condition (a security event, an operational anomaly, a policy breach). The corpus governs the human incident lifecycle ([`ai/plan-ai-incident-response.md`](plan-ai-incident-response.md)) and requires human review before containment ([`operations/procedure-threat-intelligence-and-siem-operations.md`](../operations/procedure-threat-intelligence-and-siem-operations.md)), but it has no state machine for what an agent may do autonomously between detection and human authorization. This framework supplies that: the states an agentic response moves through, the transitions between them, and, at each transition, the containment-authority boundary that separates what the agent may do within its existing observation-and-analysis grant from what requires a further human grant.

Its organizing rule is the [`capability-is-not-authority`](../governance/principle-capability-is-not-authority.md) principle: an agent's technical ability to contain (revoke a token, isolate a host, kill a process) is never, by itself, the authority to do so; that authority is conferred by a human grant or a pre-approved autonomous policy, never by the agent's reach.

## Scope

Applies to every agentic AI system that can observe a condition and act on it with side effects, in security, operations, or privacy contexts. It governs the agent's response states and the authority to transition between them; it does not replace the human incident lifecycle it feeds, the agent-permission scopes it honours, or the domain procedures that own each action. Purely advisory agents (that surface a finding for a human to act on) occupy only the pre-containment states.

## The state model

An agentic response moves through six states: four in the response path and two terminal dispositions reached after human review of the containment.

| State | Meaning | Agent autonomy | Next |
| --- | --- | --- | --- |
| **Detected** | A trigger condition is observed. | The agent enters this state autonomously. | Triaged |
| **Triaged** | The condition is classified and scoped (severity, affected assets, false-positive likelihood). | Autonomous: triage and enrichment are read-only and reversible. | Corroborated |
| **Corroborated** | The condition is confirmed against independent sources, and a proposed containment action is prepared. | Autonomous: corroboration is read-only; preparing (not executing) the action is permitted. | Contained (at the authority boundary) |
| **Contained** | A containment action has been executed (isolate, revoke, block, halt). | **Not autonomous by default** (see the authority boundary). | Resolved or Disputed |
| **Resolved** | A human confirms the response was correct. | Human-determined. | terminal; the incident proceeds to the human Recover phase |
| **Disputed** | A human rejects the response. | Human-determined. | terminal; the agent rolls back to the pre-Contained state and the incident escalates to the human Investigate phase |

## State transitions and the containment-authority boundary

The transitions Detected to Triaged to Corroborated may execute autonomously within the agent's recorded observation-and-analysis grant: they are read-only or reversible and change no external state, so no additional per-transition authorization grant is needed.

The **Corroborated to Contained transition is the containment-authority boundary**. Executing a containment action changes external state and is often hard to reverse, so it requires a human authorization grant before execution, consistent with the human-review-before-containment rule ([`operations/procedure-threat-intelligence-and-siem-operations.md`](../operations/procedure-threat-intelligence-and-siem-operations.md)) and the oversight modes of [`ai/standard-ai-human-oversight.md`](standard-ai-human-oversight.md) (Approval or Confirmation). The agent's containment capability does not authorize the crossing; the recorded grant does.

Two bounded exceptions may cross the boundary autonomously, and only when pre-approved, recorded, and narrow:

- **A safety or resource fail-safe** where NOT acting is the greater, less-reversible harm (a token or cost runaway, an unbounded loop), consistent with the [`fail-closed-automation`](../governance/principle-fail-closed-automation.md) principle: the safe action is the bounded, reversible halt, and it is still logged and reviewed after the fact.
- **A pre-approved autonomous containment policy** for a specific, narrowly-scoped, reversible condition class, authorized in advance by the accountable owner. Such a policy **never covers an irreversible action** (irreversible classes are permanently subject to per-action human confirmation and cannot be reclassified as autonomous, per [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md)); it satisfies that standard's production-authority prerequisites (permission boundaries, immutable auditability, tested reversibility, named human accountability) and its grant carries the six properties of a valid authorization (explicit, attributable, scoped, time-bounded, revocable, evidenced) per [`capability-is-not-authority`](../governance/principle-capability-is-not-authority.md).

**AI-assisted security detections are excluded from the pre-approved-policy exception**: the SIEM-operations procedure requires that all AI-assisted detections be reviewed by a human analyst before any containment ([`operations/procedure-threat-intelligence-and-siem-operations.md`](../operations/procedure-threat-intelligence-and-siem-operations.md) §6.4), an unconditional rule this framework does not relax; only the safety/resource fail-safe may act in that scope, and it too is reviewed after the fact.

Absent one of these, a Corroborated response that is not human-authorized waits; it does not self-authorize on the strength of its own capability.

## Alignment with the human incident lifecycle

The state model runs parallel to, and feeds, the seven-phase human incident lifecycle ([`ai/plan-ai-incident-response.md`](plan-ai-incident-response.md)): Detected feeds Detect and Triaged feeds Triage; the Corroborated-to-Contained boundary is the hand-off to Contain, where a human authorizes the action; Investigate and Eradicate remain human-led (the agent supports but does not own them); Resolved feeds Recover and then Post-incident review, while Disputed returns the incident to Investigate. The agent does not run a containment loop independent of that lifecycle; it prepares and proposes, the human authorizes, and the outcome returns to the human record.

## Assurance requirements

- Every state transition is logged, attributable, and explainable, per [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md) and the SIEM-operations review requirement.
- The containment-authority grant (human or pre-approved policy) is recorded for each Contained transition, with the authorizing subject and scope.
- Each autonomous-crossing exception carries its pre-approval record and its after-the-fact review.
- The Corroborated to Contained boundary and the rollback from Disputed are tested, not assumed.

## Framework alignment

The alignment below is analogical (each row aligns with or is informed by the cited reference), not a prescriptive crosswalk; the references govern incident response, AI oversight, and AI-threat context, whereas this framework governs the agent's response states and the authority to transition them. References are verified against the canonical-citations register.

| Framework | Reference | Relevance |
| --- | --- | --- |
| EU AI Act (Regulation (EU) 2024/1689 as amended by Regulation (EU) 2026/1744) | Article 14 | Human oversight of the containment decision at the authority boundary. |
| ISO/IEC 42001:2023 | Clause 8 (Operation) | Controlled operation of the agentic response within the AI management system. |
| NIST AI RMF 1.0 (2023) | GOVERN 3.2; MANAGE 2.4, MANAGE 4.1 | Defined human-AI configuration and oversight roles (GOVERN 3.2); mechanisms to disengage or deactivate an AI system (MANAGE 2.4) and to override or appeal an automated response (MANAGE 4.1). |
| NIST SP 800-61 Rev. 3 | Incident-response lifecycle | The human lifecycle this state model runs parallel to and feeds. |
| MITRE ATLAS (2026.07) | Adversarial-ML tactics and techniques | Threat context for the conditions an agentic response detects and corroborates. |

## Limitations

This framework governs the states and authority of an agentic response; it does not specify the detection logic, the containment mechanisms, or the domain procedures that own each action, which live in the security, operations, and AI-security documents. It assumes the agent's capability scope is already governed by the agent-permissions standard; a scope defect there is not corrected here. The autonomous-crossing exceptions are deliberately narrow, and widening them is a governance decision, not an engineering convenience.
