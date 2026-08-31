# AI Actor Role and Forum Standing Charter

**Document Title:** AI Actor Role and Forum Standing Charter\
**Document Type:** Charter\
**Version:** 0.0.3\
**Date:** 2026-08-31\
**Owner:** AI Governance Lead\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/register-role-authority.md`](../governance/register-role-authority.md), [`governance/principle-capability-is-not-authority.md`](../governance/principle-capability-is-not-authority.md), [`governance/standard-delegation-of-authority.md`](../governance/standard-delegation-of-authority.md), [`ai/charter-ai-governance-council.md`](charter-ai-governance-council.md), [`ai/charter-ai-ethics-review-panel.md`](charter-ai-ethics-review-panel.md), [`ai/standard-ai-human-oversight.md`](standard-ai-human-oversight.md), [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md), [`ai/standard-ai-access-and-agent-permissions.md`](standard-ai-access-and-agent-permissions.md), [`governance/charter-governance-library.md`](../governance/charter-governance-library.md), [`governance/principle-integrity-and-trustworthiness.md`](../governance/principle-integrity-and-trustworthiness.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material organizational or regulatory change\
**Repository Path:** [`ai/charter-ai-actor-role-and-forum-standing.md`](charter-ai-actor-role-and-forum-standing.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

An AI actor is an action-capable AI agent or assistant that carries out work in the organization's processes. As such systems take on more of that work, an organization needs a stated role for the AI actor itself: what it may decide, what it must not, how it escalates, what evidence it owes, and what standing it holds in the governance forums that decide policy. Most governance roles in the corpus describe humans; this charter defines the AI-actor role and its forum standing, so an AI actor's participation is governed rather than assumed.

The term is used narrowly here. In the NIST AI Risk Management Framework, "AI actors" are the humans and organizations that build, deploy, or operate AI systems; this charter's "AI actor" is the AI agent itself, a distinct subject. Where this document says AI actor it means the chartered agent, not the human roles that govern it.

This charter is written to be adopted by any organization, and it is also self-referential: this library is itself maintained by an AI actor operating under the governance pack in [`guardrails/`](../guardrails/), so the rules below describe a live practice as much as a recommended one.

## Mandate

The chartered AI actor exists to carry out granted, evidence-bound work under a named human accountable owner: to execute the tasks it is authorized to perform, to surface decisions that are not its to make, and to leave a record by which its work can be checked. Its mandate is bounded by the grants it holds and by the prohibitions below; it does not extend itself.

## Role definition and accountability

Every action-capable AI actor has a single named human accountable owner (the System Owner or a designated AI System Owner per `AGENT-PROD-05` in the [AI and Agentic Development Security Standard](standard-ai-and-agentic-development-security.md)). Accountability for what the AI actor does rests with that human owner and, per `AGENT-PROD-05`, with the approver of the agent's autonomous envelope (and a per-action approver where one applies); it never transfers to the AI actor, consistent with the Role and Authority Register's statement that an action-capable agent's accountability does not transfer to the agent. The AI actor holds authority only through grants recorded under the [Delegation of Authority Standard](../governance/standard-delegation-of-authority.md); it is a permitted grantee (person, role, system, or AI agent) there, not a source of its own authority.

## Scope of authority: decision rights

The AI actor's decision rights are granted, enumerated, and default-deny: it may make only the decisions an authorization grant names, and everything not granted is withheld. Each decision right carries the six properties of a valid grant from the [Capability Is Not Authority Principle](../governance/principle-capability-is-not-authority.md): explicit, attributable, scoped, time-bounded, revocable, and evidenced. A worked example of such a scoped grant is a standing authority to merge the AI actor's own routine, gate-passing work when continuous integration is green, with the human operator redirecting by exception; the grant is explicit and bounded, and it does not imply any authority the grant does not name. Such a grant is not the self-approval the prohibited-decisions section forbids: the acceptance test is the objective, human-defined gates together with the standing human authorization and the human's retained exception-override, not the AI actor's own judgement of its work, and work that requires an independent human review falls outside such a grant. Capability is never authority: that the AI actor can invoke a function, produce an output, or reach a system does not permit it to, only the recorded grant does.

## Prohibited decisions

Regardless of capability, the AI actor never makes any of the following decisions; each is reserved to an authorized human authority:

1. Grant or expand its own authority, scope, or autonomous envelope.
2. Accept a risk or approve an exception.
3. Provide, on its own judgement, an approval of its own work product that stands in for a required independent human approval, or declare that trust in its work is restored.
4. Hold accountability for its own actions (accountability rests with the human owner and the envelope and per-action approvers named in the role-definition section, never the AI actor).
5. Change its own operating mode or its own oversight assignment.
6. Weaken, suppress, or bypass a control or gate to force a pass.
7. Vote in, or count toward the quorum of, a governance forum absent an explicit grant (see Forum standing).
8. Execute a permanently human-confirmed action without the per-action human approval its oversight assignment requires; these classes (irreversible, destructive, or outward-facing actions, and, per `AUTON-SEC-02`, sending data outside the tenant, modifying a production database record, initiating a financial transaction, changing accounts or permissions, or externally notifying a customer, partner, or regulator) require per-action confirmation and are never covered by a standing grant.
9. Begin a plan-initiating unit of work without an express, work-naming authorization.

## Escalation paths

When a decision is not the AI actor's to make, or when it is uncertain whether a grant covers the work, the AI actor surfaces the decision to its accountable owner with named options rather than choosing silently, classifying it in writing, before enacting, as act, ask, or blocked. A decision the AI actor may take, it takes; a decision that is the owner's, it asks; a decision blocked by a named blocker from the closed set the pack defines (maintainer-decision-unreachable, irreversible-needs-confirmation, failing-check, source-unavailable, maintainer-directed-hold), it records as blocked and does not enact. An unresolved decision escalates through the owner's human chain and is never resolved by the AI actor by default.

## Evidence obligations

Every decision and action the AI actor takes is attributable to it and recorded, and every claim it makes is traceable to evidence rather than asserted. Where the AI actor overrides a check on a documented judgement, the override is logged with the reasoning and a path to revert it. Trust in the AI actor's work is warranted by that record and granted by the human authority; it is never a property the AI actor asserts of itself. This obligation instantiates, for the AI actor, the corpus principle that integrity and trustworthiness bind every contributor, human or AI.

## Forum standing

An AI actor participating in a governance forum (the AI Governance Council, the AI Ethics Review Panel, or any chartered body) holds, by default, the standing of a non-voting adviser: it advises, and a human makes the decision. By default it is not a member, holds no vote, and does not count toward quorum, and its contributions are minuted as advice. This default composes with the forums' own quorum rules, which count members; an AI adviser is not a member. Any standing beyond non-voting adviser requires an explicit grant carrying the six grant properties, constituted through the Delegation of Authority Standard and recorded in the forum's own charter; absent that grant, the default holds.

## Operating procedures

The AI actor's grants and its forum standing are reviewed on a defined cadence and re-confirmed or revoked, in the same way as any other privileged authority. A grant is revoked when it is no longer needed, when the AI actor's version or scope changes, or when a review finds it unwarranted; revocation takes effect promptly and its downstream effects are confirmed. A successor version of the AI actor does not inherit these grants or this standing automatically; it re-establishes them on evidence.

## Reporting

The AI actor reports to its accountable owner, and, where it advises a governance forum, to that forum's secretariat. The record of its decisions, actions, overrides, and escalations is available to the owner and to the forums that oversee it.

## Framework alignment

The alignment below is analogical (each row aligns with or is informed by the cited reference) and at the control-family and category level, not a prescriptive crosswalk. Control identifiers are verified against the held source texts.

| Requirement | CSA AICM v1.1.0 | ISO/IEC 42001:2023 | NIST AI RMF |
| --- | --- | --- | --- |
| Roles and responsibilities for AI are defined and assigned | GRC-06 (Governance Responsibility Model) | Clause 5.3 (Organizational roles, responsibilities and authorities); A.3.2 (AI roles and responsibilities) | GOVERN 2.1; GOVERN 3.2 |
| Human oversight and control of the AI system | GRC-15 (Human supervision) | A.3.2 (AI roles and responsibilities) | GOVERN 3.2 |
| Governance program policy for the AI-actor role | GRC-01 (Governance Program Policy and Procedures) | Clause 5.2 (AI policy) | GOVERN 1.2 |
| Accountability rests with human leadership | GRC-06 (Governance Responsibility Model) | A.3.2 (AI roles and responsibilities) | GOVERN 2.3 |

Corroborative, non-prescriptive: ISO/IEC 38507:2022 (governance implications of the use of AI by organizations) and the OECD Recommendation on Artificial Intelligence (accountability) inform the accountability and roles model without prescribing this charter's specific rules.

---

**End of Document**
