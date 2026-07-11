# AI Ethics Review Panel Charter

**Document Title:** AI Ethics Review Panel Charter\
**Document Type:** Charter\
**Version:** 1.0.3\
**Date:** 2026-07-11\
**Owner:** Chief Risk Officer\
**Approving Authority:** Chief Risk Officer\
**Related Documents:** [`ai/charter-ai-governance-council.md`](charter-ai-governance-council.md), [`ai/guideline-ethical-ai-use.md`](guideline-ethical-ai-use.md), [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md), [`ai/procedure-ai-audit.md`](procedure-ai-audit.md), [`governance/register-role-authority.md`](../governance/register-role-authority.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material organizational or regulatory change\
**Repository Path:** [`ai/charter-ai-ethics-review-panel.md`](charter-ai-ethics-review-panel.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title, matching the [AI Governance Council Charter](charter-ai-governance-council.md). Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork. See the [role authority register](../governance/register-role-authority.md) for the canonical role definitions and adopter-customization guidance.

---

## Purpose

This charter establishes the mandate, composition, authority, responsibilities, and operating procedures of the **AI Ethics Review Panel** (the Panel). The Panel provides **independent ethical review** of the organization's artificial intelligence systems, separate from the body that performs the organization's AI risk and compliance governance.

The Panel exists because ethical review needs a degree of independence from the body whose decisions it reviews. The [AI Governance Council](charter-ai-governance-council.md) (the AIGC) governs AI risk and compliance and approves AI deployments; if the same body also self-certified the ethics of those deployments, the ethical review would lack the independence to challenge a decision the AIGC was otherwise inclined to make. The Panel is that independent reviewer and challenge function. It does not replace the AIGC; it sits alongside it, applies the [Ethical AI Use Guideline](guideline-ethical-ai-use.md) as the organization's ethical reference, and can formally challenge an AIGC decision on ethical grounds through the mechanism defined below.

The Panel's independence is structural: it reports outside the AIGC's reporting line (to the Chief Risk Officer and, for unresolved challenges, to the Board or the highest governance authority), and its chair and a majority of its voting seats are held by people who are not voting members of the AIGC.

---

## Mandate

The AI Ethics Review Panel is mandated to:

1. Provide independent ethical review of AI systems, assessing them against the organization's ethical principles as set out in the [Ethical AI Use Guideline](guideline-ethical-ai-use.md) and applicable law and standards (including ISO/IEC 42001, the EU AI Act, the NIST AI RMF, and the OECD AI Principles).
2. Review the ethics dimension of AI Impact Assessments for high-risk and contested AI systems, complementing the AIGC's risk and compliance review.
3. Raise, and where unresolved escalate, ethical objections to AI system deployments, significant lifecycle changes, and AI uses that the Panel judges to conflict with the organization's ethical principles, through the independent challenge mechanism.
4. Advise the AIGC, the Chief Risk Officer, and executive leadership on AI ethics matters, including fairness, bias, transparency, explainability, human oversight, and the rights and interests of affected individuals and groups.
5. Maintain the organization's ethical-review practice in alignment with ISO/IEC 42001, the EU AI Act, the NIST AI RMF, and the OECD AI Principles.

The Panel's mandate is ethical review and challenge. It does not approve deployments (that authority remains with the AIGC), and it does not perform the AIGC's risk-taxonomy classification or compliance assurance.

---

## Scope of authority

The Panel has authority to:

- Conduct independent ethical reviews of any AI system the organization deploys or develops, on its own initiative or on referral from the AIGC, the Chief Risk Officer, or executive leadership.
- Require access to the AI Impact Assessment, model and system documentation, and evaluation evidence needed for its review, subject to the organization's confidentiality and need-to-know controls.
- Issue a documented ethical opinion on a reviewed AI system, including a recommendation to proceed, proceed with conditions, or not proceed on ethical grounds.
- **Formally challenge an AIGC decision on ethical grounds** through the independent challenge mechanism, requiring the AIGC to reconsider and respond in writing.
- Escalate an unresolved ethical objection to the Board or the highest governance authority for resolution.

The Panel does not hold deployment-approval, remediation-ordering, or decommissioning authority; those remain with the AIGC. The Panel's instrument is independent review, documented opinion, and challenge, not approval. Where the Panel's opinion and the AIGC's decision diverge and the divergence is not resolved between them, the challenge mechanism governs.

---

## Composition

| Role | Seat |
| --- | --- |
| **Chair** | Independent Ethics Adviser (external or non-executive; not a voting member of the AIGC) |
| **Member** | Chief Risk Officer |
| **Member** | General Counsel |
| **Member** | Data Protection Officer |
| **Member** | Responsible-AI / Ethics Lead (per the role authority register) |
| **Member** | Affected-stakeholder or employee representative |
| **Member** | Domain or technical expert (rotating; appointed for the system under review) |
| **Standing observer** | AI Governance Lead (the AIGC secretariat, for liaison; non-voting) |

The Panel's independence requires that its Chair and a majority of its voting members are not voting members of the AIGC. The AI Governance Lead attends as a non-voting liaison so that the Panel and the AIGC stay informed of each other's work; the liaison does not vote on the Panel's opinions. Seats that an adopting organization cannot fill from its own role inventory are mapped to the nearest equivalent per the [role authority register](../governance/register-role-authority.md), preserving the independence requirement.

Quorum requires attendance of the Chair (or an independent member designated by the Chair) plus at least three members, of whom a majority must be independent of the AIGC. Opinions and challenges are recorded with the date, attendees, and the reasoning.

---

## Responsibilities

### 1. Independent ethical review

- Review high-risk and contested AI systems against the [Ethical AI Use Guideline](guideline-ethical-ai-use.md) and the organization's ethical principles.
- Assess fairness, bias, transparency, explainability, human oversight, and the impact on affected individuals and groups, drawing on the evidence in the AI Impact Assessment and the system's evaluation record.
- Issue a documented ethical opinion (proceed, proceed with conditions, or do not proceed on ethical grounds).

### 2. Challenge and escalation

- Raise a formal ethical challenge to an AIGC decision through the mechanism in the next section.
- Escalate an unresolved challenge to the Board or the highest governance authority.
- Record each challenge, the AIGC's response, and the resolution.

### 3. Advice and guidance

- Advise the AIGC, the Chief Risk Officer, and executive leadership on AI ethics matters.
- Recommend updates to the [Ethical AI Use Guideline](guideline-ethical-ai-use.md) where the Panel's reviews surface gaps.

### 4. Reporting

- Report the Panel's ethical opinions, challenges, and their resolution to the Chief Risk Officer and, on the reporting cadence below, to the Board.

---

## Independent challenge mechanism

The independent challenge mechanism is the core control this charter establishes. It gives the Panel a structured, documented way to challenge an AIGC decision on ethical grounds without holding approval authority itself, so that ethical review is independent of, and can act against, the body whose decisions it reviews.

1. **Trigger.** The Panel may challenge an AIGC decision (for example, an approval of a high-risk AI deployment or a significant lifecycle change) when the Panel's documented ethical opinion conflicts with the decision. A challenge is raised in writing, with the Panel's reasoning and the ethical principles at issue.
2. **Reconsideration.** On receiving a challenge, the AIGC formally reconsiders the decision and responds to the Panel in writing within a defined period (*[adopter-defined]*; a short, bounded period is recommended so a contested deployment does not proceed unreviewed). The AIGC's response records whether it upholds, modifies, or reverses the decision, and its reasoning.
3. **Hold pending reconsideration.** A challenged decision that authorizes an irreversible or high-impact action does not proceed until the AIGC has responded to the challenge, unless an overriding safety or legal obligation requires otherwise (recorded with its justification). This reflects the UNESCO Recommendation on the Ethics of AI (paragraph 26): where an impact is irreversible, difficult to reverse, or may involve life and death, final human determination should apply.
4. **Escalation.** If the Panel judges the AIGC's response to leave the ethical objection unresolved, the Panel escalates the challenge, with both positions documented, to the Board or the highest governance authority, which resolves it. The escalation route is independent of the AIGC's own reporting line.
5. **Record.** Every challenge, the AIGC's response, any escalation, and the final resolution are recorded and retained, so the organization has an auditable trail of how contested ethical questions were decided (consistent with OECD Principle 1.5 accountability, which calls for traceability of the datasets, processes, and decisions across the AI system life cycle).

The mechanism is a challenge-and-escalation control, not a veto: the Panel cannot unilaterally block a deployment, and the AIGC retains approval authority, but the AIGC cannot dispose of an ethical challenge without a documented reconsideration, and an unresolved challenge reaches the Board rather than ending at the body that made the contested decision.

---

## Operating procedures

| Activity | Frequency |
| --- | --- |
| Regular Panel meeting | Quarterly |
| Ethical review of a high-risk or contested AI system | As required (on referral or Panel initiative) |
| Response to a Panel challenge (by the AIGC) | Within the *[adopter-defined]* reconsideration period |
| Ethics report to the Chief Risk Officer | Quarterly |
| Ethics report to the Board | Annual, and on any escalated unresolved challenge |

Meetings are minuted. Opinions, challenges, the AIGC's responses, escalations, and resolutions are recorded and retained in the governance document repository.

---

## Reporting

The Panel reports to the **Chief Risk Officer** and, for escalated unresolved challenges and the annual ethics report, to the **Board or the highest governance authority**. This reporting line is deliberately independent of the AIGC (which reports to the Enterprise Risk Committee), so the Panel can challenge an AIGC decision without reporting through the body it is challenging. Reports include:

- Ethical opinions issued and their dispositions.
- Challenges raised, the AIGC's responses, and resolutions.
- Escalations to the Board and their outcomes.
- Themes and recommended updates to the [Ethical AI Use Guideline](guideline-ethical-ai-use.md).

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 42001:2023 | §5: Leadership and Governance | Independent governance of AI ethics within the AI management system |
| EU AI Act (2024) | Chapter III: High-Risk AI Systems | Independent ethical review and human oversight of high-risk AI |
| NIST AI RMF (2023) | GOVERN function | Independent oversight and accountability structure |
| OECD AI Principles (2019, updated 2024) | Accountability and oversight (Principle 1.5) | Independent ethics review, challenge, and the record step |
| UNESCO Recommendation on the Ethics of AI (2021) | Paragraphs 35-36 (human oversight and determination); paragraph 26 (irreversibility) | Human oversight and the hold-pending-reconsideration step |
| CAN/DGSI 101:2025 | Ethical impact assessment; diverse and inclusive reviewer representation | The Panel's ethical-review mandate and diverse composition |

---

**End of Document**
