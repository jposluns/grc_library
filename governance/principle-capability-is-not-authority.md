# Capability Is Not Authority Principle

**Document Title:** Capability Is Not Authority Principle\
**Document Type:** Principle\
**Version:** 0.0.2\
**Date:** 2026-08-30\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/framework-zero-trust-architecture.md`](../security/framework-zero-trust-architecture.md), [`ai/standard-ai-access-and-agent-permissions.md`](../ai/standard-ai-access-and-agent-permissions.md), [`security/procedure-access-control.md`](../security/procedure-access-control.md), [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md), [`operations/standard-network-security-and-segmentation.md`](../operations/standard-network-security-and-segmentation.md), [`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`governance/principle-integrity-and-trustworthiness.md`](principle-integrity-and-trustworthiness.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material governance, AI, or regulatory change\
**Repository Path:** [`governance/principle-capability-is-not-authority.md`](principle-capability-is-not-authority.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This document states, in citable adopter-facing form, a foundational access-governance principle: **capability is not authority**. The technical ability to perform an action never, on its own, constitutes authorization to perform it. The principle names the recurring failure it forecloses, treating the existence of a means as permission to use it, and points at the corpus controls that already instantiate it. It is the access-governance counterpart to the library's [`principle-integrity-and-trustworthiness`](principle-integrity-and-trustworthiness.md): where that principle governs the integrity of the work product, this one governs when an actor, human or automated, is permitted to act.

The principle is stated separately because the fallacy it corrects is stated nowhere in the corpus as a principle, only enforced piecewise. Making it citable lets every access control, agent-permission rule, and network policy point to a single statement of why default-deny, least privilege, and explicit approval are the rule rather than an inconvenience.

## Scope

Applies to every access decision within the corpus's reach: human, service-account, and AI-agent actors; and every resource, tool, dataset, network path, credential, and model capability they might reach. It is a principle, not a control: it fixes the rule that resolves the recurring "the actor could, therefore the actor may" fallacy, and it names the machinery that enforces it. The enforcing controls live in the access-control, zero-trust, privileged-access, network-segmentation, and AI-agent-permission documents; this document does not restate them.

## 1. The principle

**Capability is not authority. Only a current, in-scope authorization grant confers authority; every other signal is a means to act, never a permission to act.**

Authentication establishes *who* an actor is. Authorization, recorded separately, establishes *what that actor may do*. The gap between the two is where this principle lives: an actor may be fully authenticated, technically capable, and network-reachable, and still have no authority for the action in front of it. The default, absent a matching authorization grant, is deny.

Two readings are foreclosed:

- **Presence of a means is not a grant.** That a path exists, a tool is installed, a key is held, or a login succeeds says nothing about whether the action is permitted. Each is a precondition an attacker or a mis-scoped agent also satisfies.
- **The authorization grant is the sole source of authority.** Authority is not inferred from capability, convenience, precedent, or silence. It is read from an explicit, attributable, scoped, time-bounded, revocable, and recorded grant, or it is absent.

## 2. The seven capability vectors

Each vector below is routinely, and wrongly, treated as if it conferred authority. Each is a *capability*; none is an *authorization*.

### 2.1 Technical access
Holding a login, a session, a file handle, or a role binding is the ability to reach a resource, not permission to use it for a given purpose. Access provisioning is governed by least privilege and explicit authorization ([`security/procedure-access-control.md`](../security/procedure-access-control.md)), not by what a credential happens to reach.

### 2.2 Tool availability
That a tool, API, or command is installed, exposed, or reachable does not authorize its use. New tools, data scopes, and capabilities are unavailable until explicitly approved ([`ai/standard-ai-access-and-agent-permissions.md`](../ai/standard-ai-access-and-agent-permissions.md)); availability is a deployment fact, authorization is a governance decision.

### 2.3 Model capability
That an AI model *can* produce an output, invoke a function, or take an action does not authorize it to. Capability is a property of the model; authority is a property of the recorded grant. An agent's competence to act is never its licence to act ([`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md)).

### 2.4 Monitoring visibility
That an actor, tool, or role *can see* data, logs, or telemetry does not authorize use of what is seen, nor action upon it. Visibility for one purpose (observability, security monitoring) is not authorization for another (decision-making, disclosure, enforcement).

### 2.5 Key possession
Holding a credential, token, certificate, or private key is the ability to authenticate or decrypt, not standing authority to act. Break-glass and privileged credentials exist as capabilities that are withheld from routine authority: their use is separated, logged, and reviewed ([`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md)) and bounded to an authorized emergency ([`security/procedure-access-control.md`](../security/procedure-access-control.md)).

### 2.6 Network reachability
That one system can reach another over the network does not authorize the traffic. Zone boundaries and perimeter gateways operate default-deny; inter-zone communication requires an explicit, approved, documented rule ([`operations/standard-network-security-and-segmentation.md`](../operations/standard-network-security-and-segmentation.md)). Reachability is topology; authority is policy.

### 2.7 Authentication success
That an actor has proven its identity does not establish what it may do. Authentication and authorization are distinct steps: every access request is authenticated *and* authorized, regardless of source, per the zero-trust rule "never trust, always verify" ([`security/framework-zero-trust-architecture.md`](../security/framework-zero-trust-architecture.md)). A valid login is the beginning of an authorization decision, not its conclusion.

## 3. What creates authority: the authorization record

The single thing that turns a capability into a permitted action is a **current, in-scope authorization grant**. To confer authority, the grant is:

- **Explicit** (an affirmative grant, never inferred from absence of objection),
- **Attributable** (to a grantor with the standing to grant it),
- **Scoped** (bounded to specific actions, resources, and conditions),
- **Time-bounded** (with an expiry or a review cadence, so authority does not outlive its purpose),
- **Revocable** (withdrawable, with the withdrawal taking effect), and
- **Evidenced** (recorded as the durable artefact an audit reads).

Where no such record covers the action, the action is unauthorized regardless of how easily it could be performed. This is the fail-closed default: on a missing, ambiguous, or expired authorization, deny rather than fall through to a permissive path ([`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md)). Where an emergency path permits a verbal grant, the grant is still an authorization (attributable and time-bounded) and its durable record is formalized within the window the access-control procedure sets ([`security/procedure-access-control.md`](../security/procedure-access-control.md)): the grant is the authority, the record its evidence.

## 4. Instantiation in the corpus

This principle is not new machinery; it is the statement of a rule the corpus already enforces piecewise. The principle document exists so those controls can cite a single "why".

| Instantiation | Corpus control | Vector it enforces |
| --- | --- | --- |
| Default deny (new tools/scopes/capabilities unavailable until approved) | [`ai/standard-ai-access-and-agent-permissions.md`](../ai/standard-ai-access-and-agent-permissions.md) | Tool availability; model capability |
| Default-deny zone and perimeter rules | [`operations/standard-network-security-and-segmentation.md`](../operations/standard-network-security-and-segmentation.md) | Network reachability |
| Never trust, always verify; per-request authorization | [`security/framework-zero-trust-architecture.md`](../security/framework-zero-trust-architecture.md) | Authentication success; technical access |
| Least privilege; explicit, reviewed authorization | [`security/procedure-access-control.md`](../security/procedure-access-control.md) | Technical access |
| Break-glass separated, logged, and reviewed | [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md) | Key possession |
| Fail closed on error or validation failure | [`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md) | Model capability |
| Log and telemetry access restricted to authorized personnel | [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md) | Monitoring visibility |

The production-process analogue of this principle is the governance pack's express-authorization discipline (a shared understanding of what could be done is not an instruction to do it); this document is the access-governance form, and the two are conceptual siblings.

## 5. Adoption guidance

An adopter reusing this library inherits "capability is not authority" as the rule that resolves every "the actor could, so the actor may" question. To operationalize it: make default-deny the posture at every boundary (access, tool, network, agent capability), so authority must be granted rather than assumed; require an authorization record with the six properties in section 3 for any action beyond the default-allowed baseline; keep authentication and authorization as distinct, separately-recorded steps; and treat a missing or expired record as deny, never as tacit permission. The principle is the "why" an adopter cites when a stakeholder asks why access is not simply granted to whoever can technically reach the resource.

## Framework alignment

| Requirement | NIST SP 800-53 Rev. 5 | ISO/IEC 27001:2022 | NIST CSF 2.0 | CSA CCM v4.1 |
| --- | --- | --- | --- | --- |
| Access is enforced only per an approved authorization | AC-3 (Access Enforcement); AC-24 (Access Control Decisions) | A.5.15 (Access control); A.8.3 (Information access restriction) | PR.AA (category); PR.AA-05 | IAM-15 (Authorization Mechanisms); IAM-06 (Access Provisioning) |
| Capability granted only at minimum scope | AC-6 (Least Privilege) | A.8.2 (Privileged access rights) | PR.AA (category) | IAM-05 (Least Privilege) |
| Authentication is distinct from, and precedes, authorization | IA-2 (Identification and Authentication (Organizational Users)); AC-3 | A.8.5 (Secure authentication); A.5.15 | PR.AA (category); PR.AA-03 | IAM-13 (Strong Authentication); IAM-15 (Authorization Mechanisms) |
| Access rights are provisioned, reviewed, and revoked over their lifecycle | AC-6 (Least Privilege); AC-24 (Access Control Decisions) | A.5.18 (Access rights); A.5.15 | PR.AA (category); PR.AA-05 | IAM-08 (Access Review); IAM-06 (Access Provisioning) |

Control identifiers are verified against the held source texts (NIST SP 800-53 Rev. 5 catalogue; ISO/IEC 27001:2022 Annex A; NIST CSF 2.0 category PR.AA; CSA Cloud Controls Matrix v4.1 IAM domain). NIST SP 800-207 (Zero Trust Architecture) is the primary reference for the per-request, capability-independent authorization model this principle expresses.
