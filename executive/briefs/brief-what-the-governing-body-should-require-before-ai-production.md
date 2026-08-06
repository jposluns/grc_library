# What the governing body should require before an AI system goes into production

**Document Title:** What the governing body should require before an AI system goes into production\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-08-06\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/guide-ai-board-oversight.md`](../../ai/guide-ai-board-oversight.md), [`ai/standard-ai-security-and-risk.md`](../../ai/standard-ai-security-and-risk.md), [`ai/procedure-ai-system-impact-assessment.md`](../../ai/procedure-ai-system-impact-assessment.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/briefs/brief-what-the-governing-body-should-require-before-ai-production.md`](brief-what-the-governing-body-should-require-before-ai-production.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Executive Brief\
**Narrative Status:** Explanatory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`ai/guide-ai-board-oversight.md`](../../ai/guide-ai-board-oversight.md), [`ai/standard-ai-security-and-risk.md`](../../ai/standard-ai-security-and-risk.md), [`ai/procedure-ai-system-impact-assessment.md`](../../ai/procedure-ai-system-impact-assessment.md), [`ai/framework-ai-governance-and-risk.md`](../../ai/framework-ai-governance-and-risk.md), [`ai/framework-ai-model-risk.md`](../../ai/framework-ai-model-risk.md), [`ai/template-ai-system-register.md`](../../ai/template-ai-system-register.md), [`ai/plan-ai-incident-response.md`](../../ai/plan-ai-incident-response.md), [`security/standard-data-classification-and-handling.md`](../../security/standard-data-classification-and-handling.md), [`governance/policy-exception-and-risk-acceptance-management.md`](../../governance/policy-exception-and-risk-acceptance-management.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../../supply-chain/framework-supplier-and-cloud-governance.md), [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md), [`supply-chain/template-supplier-offboarding-evidence.md`](../../supply-chain/template-supplier-offboarding-evidence.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-002\
**Last Reviewed:** 2026-08-06

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Why this matters

Putting an AI system into production is a management decision. The governing body's role is oversight: to satisfy itself, before the system goes live, that the organization is ready to operate the system and not only that the system works. Where the governance around a system (an owner, a risk classification, tested controls, monitoring, an incident path, a route to retire it) is assembled only after the system is live, the governing body's ability to shape it is reduced. Acting before production is a dependency of effective oversight.

The governing body's oversight differs in kind from management's approval. The governing body does not build the system and does not approve it into production; it sets the risk appetite the organization operates within, puts the questions an unready deployment would not withstand, and states what it expects to receive. This brief points to where the corpus defines each of those. The division of authority it draws between the governing body and management is synthesized across several corpus sources; see the limitations.

## What the corpus establishes

The corpus defines what an organization needs in place before an AI system is put into production, and it separates the governing body's role from management's.

- **A minimum control baseline.** The [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) sets the minimum AI controls an organization must have before production, covering areas including inventory and ownership, data governance, access, pre-deployment testing, monitoring and logging, human oversight, supplier assessment, an incident and exception path, and decommissioning (its section 4). Individual controls in that section carry their own lifecycle timing; this brief points to the section for the baseline and does not reproduce it.
- **Human oversight is over the system's outputs.** The [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) requires that human reviewers receive enough context to challenge, override, or reject the system's outputs (its section 4.8). This is an operating control on the AI itself, and it is not a substitute for the governing body's oversight role.
- **Production approval is a management decision.** The [AI system impact assessment procedure](../../ai/procedure-ai-system-impact-assessment.md) places the approve-or-reject decision, at its Step 9, with an accountable approving authority, escalating to the AI Governance Council for high-impact systems or unresolved high residual risk. The production gate is management's, exercised within the appetite the governing body has set.
- **The governing body sets appetite and puts the questions.** The [board oversight guide](../../ai/guide-ai-board-oversight.md) establishes that the governing body sets the organization's AI risk appetite and approves material AI policy direction while management operates within it (its section 4); it names structured interrogation as the governing body's primary oversight instrument and provides a director question set (its section 5); and it sets out governance red flags (its section 6) and what the governing body should expect to receive (its section 7).
- **High residual risk escalates above the management gate.** The [exception and risk acceptance policy](../../governance/policy-exception-and-risk-acceptance-management.md) routes acceptance of high or critical residual risk above a routine management approval, to the higher authority it designates (its section 4.2). Where a system would enter production carrying such risk, that acceptance follows this route rather than an ordinary production sign-off.
- **The supporting controls each have a home in the corpus.** Model-risk governance is set out in the [AI model risk framework](../../ai/framework-ai-model-risk.md); the reusable evidence structure for the inventory is the [AI system register template](../../ai/template-ai-system-register.md); handling of AI datasets, model artefacts, and logs is governed by the [data classification and handling standard](../../security/standard-data-classification-and-handling.md); supplier assessment and contracting sit in the [supplier and cloud governance framework](../../supply-chain/framework-supplier-and-cloud-governance.md); the incident classes and preserved evidence that apply to AI are in the [AI incident response plan](../../ai/plan-ai-incident-response.md); material-change triggers and the change lifecycle are in the [AI governance and risk framework](../../ai/framework-ai-governance-and-risk.md) and the [change management procedure](../../operations/procedure-change-management-and-configuration-control.md); and retirement, including supplier-side deletion evidence, draws on the security standard's decommissioning control and the [supplier offboarding evidence template](../../supply-chain/template-supplier-offboarding-evidence.md).

## What this means for the organization

For the governing body and accountable executive leadership, the corpus position sets a division of labour before an AI system goes live. This division is a composite reading of the sources named above.

- **The governing body does not approve the system into production; it sets the appetite and policy that management's decision operates within.** Its contribution beforehand is an approved AI risk appetite and material policy direction, so that management's Step 9 decision is exercised within limits the governing body has set.
- **The governing body should expect evidence, not assurances.** The controls the corpus calls for are visible to the governing body only when they can be shown. Its oversight before production is a dependency on management producing the evidence that each control exists and operates, which the next section expresses as evidence classes.
- **High residual risk does not pass as a routine sign-off.** Where a system would enter production carrying high or critical residual risk, the corpus escalates that risk-acceptance decision above the routine management approval, to the authority the [exception and risk acceptance policy](../../governance/policy-exception-and-risk-acceptance-management.md) designates (its section 4.2). Treating it as an ordinary production approval bypasses a control the corpus places above the management gate.
- **Some answers are weak answers.** The [board oversight guide](../../ai/guide-ai-board-oversight.md) names governance red flags (its section 6); one bears directly on a production decision, namely accountability attributed to a system or a supplier rather than to a person. Two further weak answers are worth naming against the [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) rather than the red-flag list. "We will monitor it once it is live" treats monitoring as a replacement for the pre-production controls, when the security standard places monitoring among the controls to have in place before production. And a passing internal test is evidence that a control was exercised once, not evidence that the control operates in production.

## Evidence to request

Each item below is an evidence class the governing body can call for from management, and each is evidence for a named control or outcome. The [board oversight guide](../../ai/guide-ai-board-oversight.md) provides the director question set (its section 5) that frames the questions to ask; this list frames what a strong answer produces.

- **An entry in the AI system register** for the system, as evidence of inventory and ownership. The [AI system register template](../../ai/template-ai-system-register.md) shows the structure; the requirement to record each AI system in the register before production lives in the [AI security and risk standard](../../ai/standard-ai-security-and-risk.md).
- **The completed impact assessment and its Step 9 approval record**, as evidence that the production gate operated, including the residual risk, conditions, and control owner the [AI system impact assessment procedure](../../ai/procedure-ai-system-impact-assessment.md) requires the approval to record.
- **A model card or evaluation record**, as evidence that model-risk governance was applied, per the [AI model risk framework](../../ai/framework-ai-model-risk.md).
- **The monitoring and logging design**, as evidence for the monitoring and logging control in the [AI security and risk standard](../../ai/standard-ai-security-and-risk.md).
- **The incident-response linkage**, as evidence that the AI incident classes in the [AI incident response plan](../../ai/plan-ai-incident-response.md) are covered and that the plan's evidence-preservation requirements are provided for (the plan sets the incident scope to which they apply).
- **The supplier assessment and contract control schedule**, as evidence for supplier governance where the system depends on an external provider, per the [supplier and cloud governance framework](../../supply-chain/framework-supplier-and-cloud-governance.md).
- **The risk-acceptance record**, as evidence that any high or critical residual risk carried into production followed the [exception and risk acceptance policy](../../governance/policy-exception-and-risk-acceptance-management.md).
- **The change-management and material-change plan**, as evidence that post-production changes will re-engage assessment, per the [change management procedure](../../operations/procedure-change-management-and-configuration-control.md) and the material-change triggers in the [AI governance and risk framework](../../ai/framework-ai-governance-and-risk.md).
- **The decommissioning and data-deletion plan**, as evidence that retirement is controlled, drawing on the decommissioning control in the [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) and the [supplier offboarding evidence template](../../supply-chain/template-supplier-offboarding-evidence.md).

## Limitations

- This page creates no compliance and imposes no requirement. The linked corpus documents govern; where this page differs from a corpus document, the corpus document prevails.
- This page carries composite claims. The division of authority it describes (management approves production; the governing body sets appetite and policy; high or critical residual-risk acceptance escalates above the management gate) is synthesized across several corpus sources, and the adopting organization validates that reading against its own governance and its own committee structure, which may name the escalation authority differently.
- The corpus documents this page points to carry the specific control text, thresholds, classifications, and named approval authorities. This page routes to them and does not reproduce them, so the corpus remains the single source for every value.
- This page makes no claim about how likely any failure is, and none of its statements should be read as a probability or a frequency.

**End of Document**
