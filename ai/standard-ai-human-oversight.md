# AI Human-Oversight Standard

**Document Title:** AI Human-Oversight Standard\
**Document Type:** Standard\
**Version:** 0.0.2\
**Date:** 2026-08-31\
**Owner:** AI Governance Lead\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](policy-ai-compliance.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`ai/standard-ai-model-risk.md`](standard-ai-model-risk.md), [`ai/standard-ai-access-and-agent-permissions.md`](standard-ai-access-and-agent-permissions.md), [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md), [`ai/template-system-card.md`](template-system-card.md), [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md), [`ai/guideline-ethical-ai-use.md`](guideline-ethical-ai-use.md), [`privacy/register-automated-decision-making.md`](../privacy/register-automated-decision-making.md), [`governance/principle-capability-is-not-authority.md`](../governance/principle-capability-is-not-authority.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI, framework, or regulatory change\
**Repository Path:** [`ai/standard-ai-human-oversight.md`](standard-ai-human-oversight.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard consolidates the organization's human-oversight requirements for AI systems into one citable statement. Oversight obligations are otherwise scattered across the AI policy, several AI standards, the system-card template, the audit-and-certification framework, and the ethical-use guideline; a reader cannot see the whole obligation in one place, and the scattered forms risk drift. This standard states the consolidated requirement, defines a six-mode human-AI interaction taxonomy so an oversight design can be named precisely, and fixes the rules for override, automation-bias prevention, negative consent, and disclosure.

It consolidates the requirement; it does not remove the domain-specific clauses it draws together. Each contributing surface continues to apply its oversight requirement in context and is expected to reference this standard as the canonical statement.

## 2. Applicability

Applies to every AI system the organization builds, deploys, procures, or operates whose outputs or actions can affect a person's rights, eligibility, access, employment, finances, health, safety, legal exposure, or the organization's critical operations, and to every agentic AI system that can take actions with side effects. It binds the AI System Owner, the deployer of a high-risk system, the assigned human overseers, and the AI Governance function. Systems whose outputs are purely informational and carry none of the effects above apply this standard proportionately, per the risk classification in the AI compliance policy.

## 3. Relationship to other GRC documents

This standard is the canonical human-oversight requirement; the following surfaces instantiate it in their own scope, and their oversight clauses are read as applications of it rather than independent rules:

- [`ai/policy-ai-compliance.md`](policy-ai-compliance.md) §5.3 (high-risk deployer oversight, EU AI Act Article 26(2));
- [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md) §4.8 (oversight where outputs materially affect rights or operations);
- [`ai/standard-ai-model-risk.md`](standard-ai-model-risk.md) §3.6 (alignment and reviewer authority);
- [`ai/standard-ai-access-and-agent-permissions.md`](standard-ai-access-and-agent-permissions.md) §6.4 (human-in-the-loop confirmation modes for agent actions);
- [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md) §24 (approval boundaries and reversibility for agent actions);
- [`ai/template-system-card.md`](template-system-card.md) (oversight, user-disclosure, and output-verification documentation);
- [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md) §5.4 (oversight as an audit criterion);
- [`ai/guideline-ethical-ai-use.md`](guideline-ethical-ai-use.md) §5 (ethical-use expectations);
- [`privacy/register-automated-decision-making.md`](../privacy/register-automated-decision-making.md) (the register of automated decisions, including the solely-automated decisions with legal or similarly significant effect subject to GDPR Article 22).

It also depends on the access-governance principle that capability is not authority ([`governance/principle-capability-is-not-authority.md`](../governance/principle-capability-is-not-authority.md)): an overseer's ability to intervene is a capability, and the authority to override is conferred by the oversight assignment recorded under this standard.

## 4. Minimum requirements

### 4.1 Oversight assignment

Human oversight is assigned to named natural persons who have the competence, training, authority, and organizational support to exercise it (EU AI Act Article 26(2)). The assignment records the overseer, the system, the oversight mode (section 4.2), and the scope of decisions the overseer may take; it is documented in the AI System Register and reviewed at least annually. An overseer's authority to override, interrupt, or disregard the system is part of the recorded assignment, not an inherent property of access.

### 4.2 The six-mode human-AI interaction taxonomy

Every AI system's oversight design names one or more of the six interaction modes below. Five modes describe the overseer's position in the decision loop, ordered by increasing human involvement (Notification, Delegation, Consultation, Confirmation, Approval); Consent is a distinct dimension, the affected person's lawful basis for the processing, which can coexist with any loop position. The decision-right boundaries distinguish them: Consultation places the human as decision-maker with the system advising; Confirmation requires a human to verify a system-proposed output before it is relied on or executed; Approval requires a human to authorize each action before the system executes it. A system may use different modes for different action classes.

| Mode | Human role | When required |
| --- | --- | --- |
| **Notification** | The system acts autonomously and informs a human after the fact. | Low-consequence, readily reversible actions only. |
| **Delegation** | The system acts semi-autonomously within a bounded scope, under a standing kill-switch. | Bounded, monitored operation where a human can interrupt at any time. |
| **Consultation** | The system advises; a human makes the decision. | Decision-support where the human is the decision-maker (AI as adviser). |
| **Confirmation** | The system proposes; a human verifies the output before it is relied on or executed. | Sensitive or material actions; probabilistic outputs used as evidence. |
| **Consent** | An affected person affirmatively opts in to the processing and, where applicable, to a solely-automated decision. | Where consent is the selected Article 6 lawful basis for processing; where explicit consent is relied on as the Article 22(2)(c) exception for a solely-automated decision with legal or similarly significant effect; and for sensitive-data or minors' processing where opt-in is required. |
| **Approval** | A human authorizes each action before the system executes it. | Destructive, financially material, or irreversible actions. |

The confirmation mode has three sub-forms drawn from the agent-permissions standard: per-action confirmation (each action confirmed; standing approval prohibited) for destructive or financially material actions; per-session confirmation (scope confirmed at session start; deviations require new confirmation) for bulk operations; and asynchronous approval (the agent produces a plan; a separate human approves before execution) for queued workflow actions.

### 4.3 When oversight is required

Human oversight is mandatory where an AI output or action may materially affect a person's rights, eligibility, access, employment, finances, health, safety, or legal exposure, or the organization's critical operations or regulatory reporting. The oversight mode is chosen from section 4.2 in proportion to consequence and reversibility: the more consequential and less reversible the action, the further toward the Approval end of the spectrum the design sits.

### 4.4 Override, intervention, and stop

Assigned overseers can, in real time, disregard, override, or reverse the output of a high-risk AI system, and can interrupt it through a stop function or safe-halt procedure (EU AI Act Article 14(4)(d) and (e)). The intervention path is tested, and its authority is recorded in the oversight assignment. For agentic systems the organization extends this to an immediate stop of the system, and the kill-switch and the approval boundaries in the agentic-development-security standard bound what the system may do between interventions.

### 4.5 Automation-bias prevention

Overseers are equipped and empowered to challenge AI outputs, not merely to rubber-stamp them (EU AI Act Article 14): they receive enough context to interpret and contest an output, are trained on the system's capabilities and limitations, and are not led to treat a probabilistic output as authoritative evidence without verification. Oversight designs avoid conditions that induce automation bias (for example, time pressure that makes confirmation perfunctory).

### 4.6 Negative consent and opt-out

Where an affected person has a right to object to or opt out of automated processing, the default is the more protective state and the opt-out is honoured without penalty. A solely-automated decision with legal or similarly significant effect requires an Article 22(2) exception (contractual necessity, authorizing law, or explicit consent) and, absent one, a genuine human-in-the-loop path; the applicable exception or human-review path is recorded in the automated-decision-making register.

### 4.7 Disclosure

Where a person interacts directly with an AI system, that fact is disclosed to them (EU AI Act Article 50, subject to its obviousness and law-enforcement exceptions). Where a person is subject to a decision by a deployed high-risk (Annex III) system, the deployer informs them (EU AI Act Article 26(11)). The organization additionally provides how to reach a human and how to contest an outcome where a contest right applies.

## 5. Evidence requirements

- The oversight assignment for each in-scope system (overseer, mode, scope, review date) in the AI System Register.
- The oversight-mode selection rationale, tied to the system's consequence-and-reversibility assessment.
- Records of intervention-path testing (override and stop) for agentic and high-risk systems.
- The applicable Article 22(2) exception (or, where none applies, the human-in-the-loop path) for each solely-automated decision with legal or similarly significant effect, in the automated-decision-making register.
- Disclosure artefacts (the notices presented to affected persons).
- Overseer competence and training records.

## 6. Compliance notes

Oversight is proportionate: a purely informational, low-consequence system is not burdened with per-action approval, and a destructive agentic action is not governed by after-the-fact notification. The taxonomy exists so the chosen point on the spectrum is explicit and defensible rather than implicit. This standard states the requirement; the enforcing checks live in the AI audit-and-certification framework and the per-system impact assessment, and the register gates record the evidence above.

## 7. Framework alignment

The alignment below is analogical (each row aligns with or is informed by the cited reference), not a prescriptive crosswalk; the referenced instruments govern AI-system behaviour and management, whereas this standard governs the organization's oversight of that behaviour. AI-assurance references are verified against the canonical-citations register.

| Framework | Reference | Relevance |
| --- | --- | --- |
| EU AI Act (Regulation (EU) 2024/1689 as amended by Regulation (EU) 2026/1744) | Article 14 | Human oversight of high-risk AI: competence, override and interruption, automation-bias prevention (sections 4.1, 4.4, 4.5). |
| EU AI Act (Regulation (EU) 2024/1689) | Article 26(2) | Deployer duty to assign oversight to competent, supported natural persons (section 4.1). |
| EU AI Act (Regulation (EU) 2024/1689) | Article 50 | Transparency to a person interacting directly with an AI system (section 4.7). |
| EU AI Act (Regulation (EU) 2024/1689) | Article 26(11) | Deployer disclosure to a person subject to a decision by a deployed high-risk (Annex III) system (section 4.7). |
| EU GDPR (Regulation 2016/679) | Article 22 | Right not to be subject to a solely-automated decision with legal or similarly significant effect; the Article 22(2) exceptions (contractual necessity, authorizing law, or explicit consent), noting that the Article 22(3) human-intervention safeguard applies to the contract and explicit-consent exceptions while the authorizing-law exception relies on that law's own suitable safeguards (sections 4.2, 4.6). |
| ISO/IEC 42001:2023 | Clause 8 (Operation); Annex A controls for controlled AI operation | Human oversight embedded in the AI management system's operating controls (sections 4.1 to 4.4). |
| NIST AI RMF 1.0 (2023) | GOVERN, MAP, MEASURE, MANAGE functions | Differentiated human-AI configuration roles and defined, documented human-oversight processes across a range from autonomous to manual (sections 4.1, 4.2). |
| ISO/IEC 23894:2023 | AI risk-management guidance | Stakeholder participation in identifying where human oversight is needed and in defining fairness and bias concerns (sections 4.1, 4.3). |

---

Human oversight is the organization's assurance that an AI system's capability is exercised under human authority; it composes with the capability-is-not-authority principle, which fixes that the ability to act is never, by itself, the authority to act.
