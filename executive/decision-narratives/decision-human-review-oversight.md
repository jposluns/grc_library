# Choosing between human review, human oversight, and autonomous authority for AI-assisted work

**Document Title:** Choosing between human review, human oversight, and autonomous authority for AI-assisted work\
**Document Type:** Executive Narrative\
**Version:** 0.0.3\
**Date:** 2026-08-17\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/standard-ai-security-and-risk.md`](../../ai/standard-ai-security-and-risk.md), [`ai/standard-ai-and-agentic-development-security.md`](../../ai/standard-ai-and-agentic-development-security.md), [`ai/standard-ai-access-and-agent-permissions.md`](../../ai/standard-ai-access-and-agent-permissions.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/decision-narratives/decision-human-review-oversight.md`](decision-human-review-oversight.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Decision Narrative\
**Narrative Status:** Advisory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`ai/standard-ai-security-and-risk.md`](../../ai/standard-ai-security-and-risk.md), [`ai/standard-ai-model-risk.md`](../../ai/standard-ai-model-risk.md), [`ai/standard-ai-and-agentic-development-security.md`](../../ai/standard-ai-and-agentic-development-security.md), [`ai/standard-ai-access-and-agent-permissions.md`](../../ai/standard-ai-access-and-agent-permissions.md), [`ai/framework-ai-governance-and-risk.md`](../../ai/framework-ai-governance-and-risk.md), [`ai/procedure-ai-system-impact-assessment.md`](../../ai/procedure-ai-system-impact-assessment.md), [`ai/template-ai-system-register.md`](../../ai/template-ai-system-register.md), [`ai/standard-ai-testing-validation-and-documentation.md`](../../ai/standard-ai-testing-validation-and-documentation.md), [`ai/guide-ai-board-oversight.md`](../../ai/guide-ai-board-oversight.md), [`governance/policy-exception-and-risk-acceptance-management.md`](../../governance/policy-exception-and-risk-acceptance-management.md), [`risk/procedure-risk-acceptance.md`](../../risk/procedure-risk-acceptance.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-014\
**Last Reviewed:** 2026-08-15

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## The decision in front of leadership

For each AI-assisted activity, leadership faces one question: who holds authority over the outcome, and at what point does a human exercise it? This page organizes that choice as three operating models, in increasing order of machine authority.

1. **Human review.** A person confirms each consequential output or action before it takes effect.
2. **Human oversight.** The system operates within a scope a person approved in advance, under monitoring, with a recorded review point and override authority.
3. **Autonomous authority.** The system executes production actions without per-action human involvement, within granted permission boundaries, with a named human accountable for the outcome.

These are operating models for individual activities, not a maturity ladder for the organization: the corpus's own recording grain is per system and, for action-capable agents, at the finer action-class grain those sources define (the [AI system register template](../../ai/template-ai-system-register.md) register fields; the [agentic development security standard](../../ai/standard-ai-and-agentic-development-security.md) AGENT-PROD-02). The three model names are this page's framing, not corpus vocabulary; the controls that give each model its content are the corpus's, and the next section points to them. The framing is a composite claim, acknowledged in the limitations.

The choice engages the governing body's own role as the corpus defines it. The [board oversight guide](../../ai/guide-ai-board-oversight.md) sets out the governing body's role relative to management (its section 4) and its **Governance red flags** (its section 6); use those two sections for the body's role and for the indicators of inadequate oversight. The decision this page frames remains entirely with the reader's organization.

## What the corpus provides

- **A line below which human review is required.** The [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) requires human review where AI outputs may materially affect the areas its section 4.8 lists, and sets the reviewer conditions its section 4.8 defines (the same section). For models, the [AI model risk standard](../../ai/standard-ai-model-risk.md) requires human oversight to be defined where outputs may affect the areas its section 3.6 lists, on the reviewer conditions its section 3.6 defines (the same section).
- **A default for systems that act.** The [agentic development security standard](../../ai/standard-ai-and-agentic-development-security.md) sets the default operating posture in its AUTON-SEC-01, names the action categories that are permanently confirmed rather than autonomous in its AUTON-SEC-02, and names in its AGENT-PROD-02 the action classes kept under per-action human confirmation on the same permanent basis. Use those three controls for the default posture and the permanently confirmed categories.
- **A conditional route to autonomous execution.** The corpus defines the conditions under which production action authority is granted. The agentic standard's AGENT-PROD-01 sets the production-authority precondition; use AGENT-PROD-01 for the precondition and its evidence requirement. The [AI access and agent permissions standard](../../ai/standard-ai-access-and-agent-permissions.md) governs the agent capability scopes and their approval authorities (its section 6.2), the human confirmation modes (its section 6.4), and the per-session limits (its section 6.5); use those sections for that content.
- **A boundary on autonomy.** The [AI governance and risk framework](../../ai/framework-ai-governance-and-risk.md) sets the autonomy boundary in its Safety control domain; use that domain for the safe-state and human-determination requirements.
- **Accountability that stays with a person.** The framework locates authority and accountability as its Human Oversight control domain defines, not in the agent, and the agentic standard's AGENT-PROD-05 assigns each action-capable agent a named accountable human owner recorded in the AI system register. Use the framework's Human Oversight domain and AGENT-PROD-05 for where authority resides and for the accountability assignment and its record.
- **Machinery that records the choice and reopens it.** The [AI system impact assessment procedure](../../ai/procedure-ai-system-impact-assessment.md) owns a ten-step process, including its members labelled **Assign risk tier** (Step 7) and **Approve or reject** (Step 9); use those steps for the risk-tier basis and the approval record. The [AI system register template](../../ai/template-ai-system-register.md) carries the fields the choice writes down, in its Human Oversight row and, for action-capable agents, its agent-specific rows, with a next review date per system; use the template for those fields. The [testing, validation and documentation standard](../../ai/standard-ai-testing-validation-and-documentation.md) sets additional testing requirements under its own separately determined testing-tier vocabulary (its section 8). The framework's material-change thresholds call for reassessment when a system changes, on the dimensions its material-change-thresholds section defines.
- **A recorded route for gaps.** Where a required control is not operated, the [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) requires the exception record its section 4.10 defines. The [exception and risk acceptance policy](../../governance/policy-exception-and-risk-acceptance-management.md) governs exception approval (its section 4.2) and maintenance (its section 4.3). The [risk acceptance procedure](../../risk/procedure-risk-acceptance.md) places acceptance of the higher residual-risk levels with the authorities its **Approval guidance** names.

## Options and their consequences

Each option assigns one operating model to one activity and, for systems that can act, to one class of action.

- **Assign human review.** For some work this is not an open option: the corpus requires human review where outputs may materially affect the areas the [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) lists (its section 4.8), and keeps the action categories AUTON-SEC-02 and the action classes AGENT-PROD-02 name permanently under human confirmation (the [agentic development security standard](../../ai/standard-ai-and-agentic-development-security.md)). Where it is chosen rather than required, the model carries a dependency on reviewer capacity and on the reviewer meeting the conditions the security standard's section 4.8 sets, and, for models, those the [AI model risk standard](../../ai/standard-ai-model-risk.md) section 3.6 sets.
- **Assign human oversight.** The middle model exchanges per-action confirmation for an approved scope plus supervision. The [AI access and agent permissions standard](../../ai/standard-ai-access-and-agent-permissions.md) defines the confirmation modes this model can use (its section 6.4); where a mode still requires a human to approve before execution, that pre-execution approval boundary holds and the activity is not purely advance scope plus monitoring. The corpus attaches dependencies to this model: the security standard's section 4.8 requires the automation boundary to be documented; monitoring must cover the dimensions the [AI governance and risk framework](../../ai/framework-ai-governance-and-risk.md) lists in its Monitoring control domain; and the register's Human Oversight row must be completed (the [AI system register template](../../ai/template-ai-system-register.md)).
- **Assign autonomous authority.** Open only where the production-authority precondition is satisfied and evidenced, and never for the action categories or classes AGENT-PROD-02 keeps permanently under human confirmation. Continued authority is not a one-time grant but is maintained under those controls; use AGENT-PROD-01, AGENT-PROD-03, and AGENT-PROD-06 for the grant conditions and their maintenance.
- **Route what cannot be met as an exception.** Where the model an activity requires cannot be operated yet, the corpus's recorded route is the exception and risk-acceptance machinery, which records and governs the gap but confers no production authority and does not displace the permanently human-confirmed action categories: the exception record the security standard's section 4.10 defines, approved and maintained under the [exception and risk acceptance policy](../../governance/policy-exception-and-risk-acceptance-management.md) sections 4.2 and 4.3, and, for the higher residual-risk levels it names, accepted at the authorities the [risk acceptance procedure](../../risk/procedure-risk-acceptance.md) names in its **Approval guidance**.

## Questions to resolve before deciding

Each question resolves against a corpus source already cited above; none introduces a new claim.

- Which of our AI-assisted activities produce outputs inside the impact areas the [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) lists (its section 4.8), and which of our models fall within the areas the [AI model risk standard](../../ai/standard-ai-model-risk.md) lists (its section 3.6)?
- For systems that can act: which action classes fall under the permanently human-confirmed categories AUTON-SEC-02 and AGENT-PROD-02 name, and is per-action confirmation in place for each?
- Does each register entry complete the template's Human Oversight row, and do its reviewers meet the conditions the security standard's section 4.8 and the model-risk standard's section 3.6 set?
- For each candidate for autonomous authority: is each of the four preconditions evidenced, and is the recovery test status recorded as passed for every action class AGENT-PROD-03's recovery testing covers?
- Who is the accountable owner AGENT-PROD-05 names, recorded for each action-capable system?
- Which material-change dimensions apply to each system, and is the reassessment they call for recorded, per the framework's change record?
- Is every gap between the model an activity requires and what operates today routed through the security standard's section 4.10 and approved and maintained under the exception policy's sections 4.2 and 4.3?

## Evidence to request

Each item below is an evidence class leadership can call for from management, and each is evidence for a named control or outcome. The [board oversight guide](../../ai/guide-ai-board-oversight.md) provides the director question set that frames the conversation (its section 5).

- **The AI system register entry** for each system, completed against the template's Human Oversight and action-capable-agent rows, as evidence that an operating model is assigned and recorded, per the [AI system register template](../../ai/template-ai-system-register.md).
- **The Step 9 approval record** (the procedure's **Approve or reject** member), as evidence that the approval gate operated; use Step 9 of the [AI system impact assessment procedure](../../ai/procedure-ai-system-impact-assessment.md) for the record's required fields.
- **The production-authority evidence record** for any system holding autonomous authority, as evidence that the four preconditions were satisfied when authority was granted and that the record remains current, per the [agentic development security standard](../../ai/standard-ai-and-agentic-development-security.md) (its AGENT-PROD-06).
- **Tool-invocation logs carrying the confirmation-evidence field**, as evidence attributing each confirmed action to the human who confirmed it, per the [AI access and agent permissions standard](../../ai/standard-ai-access-and-agent-permissions.md) (its sections 6.4 and 6.6).
- **Action-lineage records** covering the five-element lineage the agentic standard requires (its AGENT-PROD-04), as evidence for the audit-trail reconstruction and the register's action-lineage coverage field records.
- **Test results for the applicable testing tier**, as evidence that testing met the requirements the [testing, validation and documentation standard](../../ai/standard-ai-testing-validation-and-documentation.md) sets for the system's applicable testing tier (its section 8).
- **Exception register entries** completed against the exception policy's section 4.5, as evidence that each recorded exception carries its tracking fields and is time-bound, per the [exception and risk acceptance policy](../../governance/policy-exception-and-risk-acceptance-management.md).

## Limitations

- This page creates no compliance, prescribes no outcome, and imposes no requirement. The linked corpus documents govern; where this page differs from a corpus document, the corpus document prevails.
- This page carries composite claims. The three-model framing (human review, human oversight, autonomous authority) is this page's synthesis: the corpus defines the underlying controls but does not itself group them under these three names. The adopting organization validates the framing, and the authorities it implies, against its own governance and committee structure.
- The corpus documents carry the specific content this page refers to: the impact-area lists, the permanently human-confirmed action categories, the capability scope definitions and their approvers, the confirmation-mode definitions, the session limits, the reversibility classes, the material-change dimensions and thresholds, and the exception durations, renewal ceilings, and approval authorities. This page routes to that content rather than restating it.
- An approval record, a passed test, or a granted authority is evidence that a gate operated on a recorded date. Nothing on this page should be read as stating that a control operates effectively in any organization today.
- This page states no jurisdiction's legal requirements for automated decision-making. Organizations subject to such regimes validate, with legal advice, where human review or human determination is legally required, which may exceed anything described here.
- This page makes no likelihood, frequency, or statistical claim, and none of its statements should be read as one.

**End of Document**
