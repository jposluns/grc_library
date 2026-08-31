# Emergency Authority Standard

**Document Title:** Emergency Authority Standard\
**Document Type:** Standard\
**Version:** 0.0.1\
**Date:** 2026-08-31\
**Owner:** GRC Programme Manager\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/standard-delegation-of-authority.md`](standard-delegation-of-authority.md), [`governance/principle-capability-is-not-authority.md`](principle-capability-is-not-authority.md), [`governance/register-role-authority.md`](register-role-authority.md), [`governance/policy-exception-and-risk-acceptance-management.md`](policy-exception-and-risk-acceptance-management.md), [`security/procedure-access-control.md`](../security/procedure-access-control.md), [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`operations/procedure-change-management-and-configuration-control.md`](../operations/procedure-change-management-and-configuration-control.md), [`resilience/procedure-crisis-management-eoc-activation.md`](../resilience/procedure-crisis-management-eoc-activation.md), [`resilience/procedure-cross-domain-incident-coordination.md`](../resilience/procedure-cross-domain-incident-coordination.md), [`ai/plan-ai-incident-response.md`](../ai/plan-ai-incident-response.md), [`ai/standard-ai-human-oversight.md`](../ai/standard-ai-human-oversight.md), [`ai/standard-ai-access-and-agent-permissions.md`](../ai/standard-ai-access-and-agent-permissions.md), [`ai/framework-agentic-response-state-model.md`](../ai/framework-agentic-response-state-model.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual or as required by regulatory or framework change\
**Repository Path:** [`governance/standard-emergency-authority.md`](standard-emergency-authority.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

An emergency lets a person, a system, or an AI agent exercise authority it would not ordinarily hold, to prevent or limit harm when the normal approval path is too slow. The corpus already carries domain-specific emergency paths (break-glass access, emergency change, emergency patch, crisis activation, incident containment, precautionary suspension), each with its own approver and its own after-the-fact review. What it does not carry is the general construct those paths share: what makes an emergency grant valid, how it is bounded, when it expires, what triggers an independent review of its continuation, and how its use is judged for proportionality after the fact.

This standard states that construct once, so the domain procedures instantiate it rather than each reinventing a partial version. It is the emergency counterpart to the [Delegation of Authority Standard](standard-delegation-of-authority.md): a delegation moves an authority the grantor holds to another subject under ordinary conditions; an emergency grant confers a temporary authority beyond the ordinary, justified by the emergency and surrendered when it ends.

## 2. Applicability

This standard applies to every temporary grant of authority beyond a subject's ordinary entitlements that is justified by an emergency, across all domains: emergency access and break-glass; emergency change, patch, and release; incident containment and isolation; crisis and continuity activation; precautionary access suspension; and the emergency authority of an AI agent. It applies whether the subject is a person, a role, a system, or an AI agent, and whether the grant is approved in advance for a defined class of emergency or declared in the moment.

It does not replace the domain procedures that carry the operational mechanics (who to call, which account to use, how to roll back); it states the authority rules those procedures apply. Where a domain procedure and this standard differ, the stricter of the two governs.

## 3. Relationship to other GRC documents

The [Capability Is Not Authority Principle](principle-capability-is-not-authority.md) fixes that an emergency grant, like any authority, comes from an explicit record and not from the ability to act; a sealed break-glass credential is capability, and its use is authorized only within a declared emergency. The [Delegation of Authority Standard](standard-delegation-of-authority.md) supplies the instrument shape this standard specializes, and the [Role and Authority Register](register-role-authority.md) identifies the typical emergency grantors and the independent reviewer for an adopter to make definitive. The [Exception and Risk Acceptance Management Policy](policy-exception-and-risk-acceptance-management.md) supplies the renewal-requires-fresh-review precedent this standard applies to emergency authority. The domain procedures listed in Related Documents carry the operational paths this standard governs.

## 4. Minimum requirements

### 4.1 The emergency-authority instrument and declaration trigger

An emergency grant is a recorded instrument, created at declaration or (for a pre-approved class) referenced at use, carrying at minimum: the declared emergency and the trigger that opened it; the grantor with standing to declare it; the grantee (person, role, system, or AI agent); the specific authority granted, bounded to the minimum the emergency needs; the actions it permits; its expiry; and its unique identifier and lineage. A pre-approved emergency class (a documented break-glass path, a standing emergency-change category) is itself such an instrument, declared in advance for a named trigger; its use is recorded against it.

### 4.2 Grantor standing, grantee identity, scope, and separation of duties

An emergency grant is valid only if the grantor has standing to declare the emergency and to confer the authority, the authority is one that may be granted under emergency, and the grant is no broader than the emergency requires. Separation of duties is preserved: the subject that declares the emergency is not, by that act alone, the independent reviewer of its renewal or the sole judge of its proportionality afterwards.

### 4.3 The least-harmful, reversible-action rule

Emergency authority is exercised through the least-harmful action that is effective, preferring a reversible action over an irreversible one where both would serve. Where only an irreversible action would be effective, it is taken under the emergency grant and recorded as irreversible with its justification. This rule is general: it holds across access, change, containment, and continuity, not only where a single domain procedure happens to state it.

### 4.4 Duration, automatic expiry, and return to ordinary authority

An emergency grant is time-bounded and expires automatically at a defined point or on the resolution of the emergency, whichever is first; it does not persist by inertia. On expiry, the subject returns to its ordinary authority, and any capability opened for the emergency (an unsealed account, a widened rule, a suspended control) is closed or restored. A permanent change made under emergency authority is converted to the ordinary change path rather than left standing on the emergency grant.

### 4.5 Renewal and the independent review it triggers

Continuing an emergency grant beyond its expiry is a renewal, not a continuation, and a renewal triggers a review independent of the original grantor before the authority continues. The review confirms the emergency still holds, the authority is still the minimum needed, and the least-harmful-action rule is still being met. A later renewal warrants higher governance review than an earlier one, as the exception policy requires for its renewals. An emergency grant that is not renewed through this review lapses at expiry.

### 4.6 Revocation, hand-back, and propagation

The grantor, or the independent reviewer, can revoke an emergency grant before expiry, with the revocation taking effect promptly. On revocation or expiry, the propagation is demonstrable: every credential, entitlement, session, and onward grant opened under the emergency instrument (its lineage) is closed, and the closure is confirmed rather than assumed. An emergency grant is also revoked automatically on a lifecycle event of the grantee appropriate to its type (a person's separation, a role's reassignment, a system's or AI agent's decommissioning or scope change).

### 4.7 Retrospective proportionality review

Every exercise of emergency authority is reviewed after the fact for proportionality, independently of the subject that exercised it. The review judges necessity (was the emergency real), alternatives (was a less-harmful effective action available), scope (was the authority the minimum needed), duration (was it surrendered promptly), resulting harm (what the action cost), and restoration (was ordinary authority and control restored). This is distinct from the effectiveness or lessons-learned review a domain procedure already runs: it judges whether the emergency power was proportionate, not only whether it worked. A finding of disproportionate use routes to the responsible governance authority.

### 4.8 AI-agent emergency authority

An AI agent can hold emergency authority only under the rules above, tightened at the points where an agent's capability could substitute for a grant. An agent never declares its own emergency, expands its own scope, selects its own approver, renews its own authority, or suppresses its own review; each of those is a grant act reserved to an authorized human grantor, and the authority is enforced outside the model, not by the model's own restraint. Pre-approved autonomous action in an emergency is limited to narrow, tested, reversible fail-safe or containment classes, as the [Agentic Response State Model](../ai/framework-agentic-response-state-model.md) already governs for agent containment; an irreversible emergency action retains per-action human approval per the [AI Human-Oversight Standard](../ai/standard-ai-human-oversight.md). On expiry the agent's capability scope is restored automatically, and the agent, its human grantor and accountable owner, the trigger, the actions, the results, any reversals, and the renewal decisions all remain reconstructable. This section adds the emergency-authority lifecycle (declaration, expiry, independent renewal review, retrospective proportionality) that the existing agentic containment model does not itself provide.

## 5. Evidence requirements

- The emergency-authority instrument for each grant (the fields in 4.1, including identifier and lineage), retained under the `Governance authorization and delegation records` category in the Data Retention Schedule ([`governance/register-data-retention-schedule.md`](register-data-retention-schedule.md)).
- Evidence that the grantor held the standing to declare the emergency and confer the authority.
- The expiry and the record of return to ordinary authority, including closure or restoration of any capability opened.
- The independent-review record for each renewal.
- Revocation records, including the propagation confirmation that downstream credentials, entitlements, sessions, and onward grants were closed.
- The retrospective proportionality review for each exercise of emergency authority.

## 6. Compliance notes

Emergency authority is proportionate to the harm it averts: a short break-glass read is lighter than an emergency change to a safety-critical system, which carries tighter scope, a shorter expiry, and closer review. This standard states the authority rules; the enforcing mechanics live in the access-control, privileged-access, incident-response, change-management, and crisis procedures, and the records-retention schedule governs how long the instruments are kept. Nothing here lowers a domain procedure's stricter requirement.

## 7. Framework alignment

The alignment below is analogical (each row aligns with or is informed by the cited reference) and at the control-family and category level, not a prescriptive crosswalk. Control identifiers are verified against the held source texts.

| Requirement | CSA CCM v4.1.0 | NIST SP 800-53 Rev. 5 | ISO/IEC 27001:2022 | NIST CSF 2.0 |
| --- | --- | --- | --- | --- |
| Emergency authority is a scoped, time-bounded grant with a declaration trigger | CCC-08 (Exception Management); IAM-10 (Management of Privileged Access Roles) | AC-2(2) (Automated Temporary and Emergency Account Management) | A.8.2 (Privileged access rights); A.5.15 (Access control) | GV.RR (Roles, Responsibilities, and Authorities); PR.AA |
| Least privilege and the least-harmful reversible action | IAM-05 (Least Privilege) | AC-6 (Least Privilege) | A.5.18 (Access rights) | PR.AA |
| Automatic expiry and independent renewal review | IAM-10 (Management of Privileged Access Roles) | AC-6(7) (Review of User Privileges) | A.5.18 (Access rights) | PR.AA |
| Rollback and restoration to a known-good state | CCC-09 (Change Restoration); BCR-09 (Disaster Response Plan) | CP-10 (System Recovery and Reconstitution); IR-4(2) (Dynamic Reconfiguration) | A.5.29 (Information security during disruption); A.8.32 (Change management) | RC.RP |
| Incident containment authority | SEF-07 (Incident Management and Response); SEF-03 (Incident Response Plans) | IR-4 (Incident Handling); IR-4(5) (Automatic Disabling of System) | A.5.26 (Response to information security incidents) | RS.MA; RS.MI |
| Retrospective proportionality review | SEF-09 (Incident Records Management) | IR-8 (Incident Response Plan) | A.5.27 (Learning from information security incidents) | RS.MA |

---

## 8. Limitations

This standard is a CC BY-SA 4.0 baseline. It states the authority rules for emergencies; the operational paths, approvers, and rollback mechanics live in the domain procedures it governs, and an adopter makes the grantors, the independent reviewer, and the expiry windows definitive in its own authority schedule. The standard is not a substitute for those procedures or for per-system emergency planning.

---

**End of Document**
