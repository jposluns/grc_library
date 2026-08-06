# What the board should require before an AI system goes into production

**Document Title:** What the board should require before an AI system goes into production\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-08-06\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/guide-ai-board-oversight.md`](../../ai/guide-ai-board-oversight.md), [`ai/standard-ai-security-and-risk.md`](../../ai/standard-ai-security-and-risk.md), [`ai/procedure-ai-system-impact-assessment.md`](../../ai/procedure-ai-system-impact-assessment.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/briefs/brief-what-the-board-should-require-before-ai-production.md`](brief-what-the-board-should-require-before-ai-production.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Executive Brief\
**Narrative Status:** Explanatory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`ai/guide-ai-board-oversight.md`](../../ai/guide-ai-board-oversight.md), [`ai/standard-ai-security-and-risk.md`](../../ai/standard-ai-security-and-risk.md), [`ai/procedure-ai-system-impact-assessment.md`](../../ai/procedure-ai-system-impact-assessment.md), [`ai/framework-ai-governance-and-risk.md`](../../ai/framework-ai-governance-and-risk.md), [`ai/framework-ai-model-risk.md`](../../ai/framework-ai-model-risk.md), [`ai/template-ai-system-register.md`](../../ai/template-ai-system-register.md), [`ai/plan-ai-incident-response.md`](../../ai/plan-ai-incident-response.md), [`security/standard-data-classification-and-handling.md`](../../security/standard-data-classification-and-handling.md), [`governance/policy-exception-and-risk-acceptance-management.md`](../../governance/policy-exception-and-risk-acceptance-management.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../../supply-chain/framework-supplier-and-cloud-governance.md), [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md), [`supply-chain/template-supplier-offboarding-evidence.md`](../../supply-chain/template-supplier-offboarding-evidence.md)\
**External Sources:** None\
**Claim Classes Present:** citation\
**Review Record:** NR-2026-002\
**Last Reviewed:** 2026-08-06

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Why this matters

Before an AI system reaches production, the board and executive leadership face a specific decision: whether the organization is ready to operate the system, not merely whether the system works. The failure pattern the corpus is built to prevent is a familiar one. A capable system goes live, the governance scaffolding around it (an owner, a risk classification, tested controls, monitoring, an incident path, a way to retire it) is assembled after the fact or not at all, and the gap becomes visible only when something goes wrong. By then the board's options are narrow.

The board's leverage sits before production, and it is different in kind from management's. The board does not build the system and does not approve it into production; it sets the risk appetite the organization operates within, asks the questions that surface an unready deployment, and requires evidence that the controls the corpus calls for are actually in place. This brief points to where the corpus defines each of those, so the board can require them rather than rediscover them after an incident.

## What the corpus establishes

The corpus already defines what an organization needs in place before an AI system is put into production, and it separates the board's role from management's.

- **A minimum control set.** The [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) sets the minimum AI controls an organization must have before production, covering inventory and ownership, data governance, access, pre-deployment testing, monitoring and logging, human oversight, supplier assessment, an incident and exception path, and decommissioning (its section 4). This brief points to that section for the control set and does not reproduce it.
- **Human oversight is over the system's outputs.** The same standard requires that human reviewers receive enough context to challenge, override, or reject the system's outputs. This is an operating control on the AI itself, distinct from, and not a substitute for, the board's governance role.
- **Production approval is a management decision.** The [AI system impact assessment procedure](../../ai/procedure-ai-system-impact-assessment.md) places the approve-or-reject decision, at its Step 9, with an accountable approving authority, escalating to the AI Governance Council for high-impact systems or unresolved high residual risk. The production gate is management's, exercised within the appetite the board has set.
- **The board's levers are appetite, questions, and risk acceptance.** The [board oversight guide](../../ai/guide-ai-board-oversight.md) establishes that the board sets the organization's AI risk appetite and approves material AI policy direction while management operates within it (its section 4), and it provides a set of questions for directors to ask management (its section 5) and a set of governance red flags (its section 6). Separately, the [exception and risk acceptance policy](../../governance/policy-exception-and-risk-acceptance-management.md) routes acceptance of high or critical residual risk to the Executive Committee or Board Risk Committee (its section 4.2). Where a system would enter production carrying high residual risk, that acceptance is a board-level decision rather than a routine management one.
- **The supporting controls each have a home in the corpus.** Model-risk governance is set out in the [AI model risk framework](../../ai/framework-ai-model-risk.md); the reusable evidence structure for the inventory is the [AI system register template](../../ai/template-ai-system-register.md); handling of AI datasets, model artefacts, and logs is governed by the [data classification and handling standard](../../security/standard-data-classification-and-handling.md); supplier assessment and contracting sit in the [supplier and cloud governance framework](../../supply-chain/framework-supplier-and-cloud-governance.md); the incident classes and preserved evidence that apply to AI are in the [AI incident response plan](../../ai/plan-ai-incident-response.md); material-change triggers and the change lifecycle are in the [AI governance and risk framework](../../ai/framework-ai-governance-and-risk.md) and the [change management procedure](../../operations/procedure-change-management-and-configuration-control.md); and retirement, including supplier-side deletion evidence, draws on the security standard's decommissioning control and the [supplier offboarding evidence template](../../supply-chain/template-supplier-offboarding-evidence.md).

## What this means for the organization

For the board and executive leadership, the corpus position translates into a clear division of labour before an AI system goes live.

- **The board does not approve the system into production; it sets the conditions under which management may.** The board's contribution before production is to have an approved AI risk appetite and policy direction in place, so that management's Step 9 decision is bounded by something the board set. A board that has not set an appetite has removed its own principal lever.
- **The board requires evidence, not assurances.** The controls the corpus calls for are real to the board only if they can be shown. The board's oversight before production depends on management producing the evidence that each control exists and operates, which the next section expresses as evidence classes.
- **High residual risk is the board's to accept, or not.** If a system would enter production carrying high or critical residual risk, the corpus routes that risk-acceptance decision to the Executive Committee or Board Risk Committee. Letting it pass as a routine management approval bypasses a control the corpus deliberately places above the management production gate.
- **Some answers are weak answers.** The board oversight guide's red flags name several; three recur before production. "The vendor is responsible for that" attributes accountability to a system or a supplier rather than to a person, which the guide flags directly. "We will monitor it once it is live" treats monitoring as a replacement for pre-production controls, when the corpus makes monitoring a dependency of safe operation rather than a substitute for testing and oversight. And a passing internal test or a completed checklist is evidence that a control was exercised once, not evidence that it operates in production: the adoption of a control is not the same as its effectiveness.

## Evidence to request

Each item below is an evidence class the board can require from management, and each is evidence for a named control or outcome. The board oversight guide's director question set (its section 5) frames the questions to ask; this list frames what a strong answer produces.

- **An entry in the AI system register** for the system, as evidence of inventory and ownership. The [register template](../../ai/template-ai-system-register.md) shows the structure; the requirement to maintain an authoritative inventory lives in the security standard.
- **The completed impact assessment and its Step 9 approval record**, as evidence that the production gate operated, including the residual risk, conditions, and control owner the [impact assessment procedure](../../ai/procedure-ai-system-impact-assessment.md) requires the approval to record.
- **A model card or evaluation record**, as evidence that model-risk governance was applied, per the [AI model risk framework](../../ai/framework-ai-model-risk.md).
- **The monitoring and logging design**, as evidence for the security standard's monitoring and logging control.
- **The incident-response linkage**, as evidence that the AI incident classes in the [AI incident response plan](../../ai/plan-ai-incident-response.md) are covered and their evidence is preserved.
- **The supplier assessment and contract control schedule**, as evidence for supplier governance where the system depends on an external provider, per the [supplier and cloud governance framework](../../supply-chain/framework-supplier-and-cloud-governance.md).
- **The risk-acceptance record**, as evidence that any high or critical residual risk carried into production followed the [exception and risk acceptance policy](../../governance/policy-exception-and-risk-acceptance-management.md).
- **The change-management and material-change plan**, as evidence that post-production changes will re-engage assessment, per the [change management procedure](../../operations/procedure-change-management-and-configuration-control.md) and the material-change triggers in the [AI governance and risk framework](../../ai/framework-ai-governance-and-risk.md).
- **The decommissioning and data-deletion plan**, as evidence that retirement is controlled, drawing on the security standard's decommissioning control and the [supplier offboarding evidence template](../../supply-chain/template-supplier-offboarding-evidence.md).

## Limitations

- This page creates no compliance and imposes no requirement. The linked corpus documents govern; where this page differs from a corpus document, the corpus document prevails.
- The adopting organization validates applicability. The division of authority described here (management approves production; the board sets appetite and accepts high or critical residual risk) reflects the corpus's governance model and the named bodies in the exception and risk acceptance policy; an organization with a different committee structure adapts those bodies to its own governance, as the policy's own tuning provisions allow.
- The corpus documents this page points to carry the specific control text, thresholds, and classifications. This page routes to them and does not reproduce them, so the corpus remains the single source for every value.
- This page makes no claim about how likely any failure is, and none of its statements should be read as a probability or a frequency.

**End of Document**
