# What the governing body should require for AI incident-response readiness before production

**Document Title:** What the governing body should require for AI incident-response readiness before production\
**Document Type:** Executive Narrative\
**Version:** 0.0.3\
**Date:** 2026-08-06\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/plan-ai-incident-response.md`](../../ai/plan-ai-incident-response.md), [`ai/guide-ai-board-oversight.md`](../../ai/guide-ai-board-oversight.md), [`ai/standard-ai-security-and-risk.md`](../../ai/standard-ai-security-and-risk.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/briefs/brief-ai-incident-response-readiness.md`](brief-ai-incident-response-readiness.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Executive Brief\
**Narrative Status:** Explanatory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`ai/plan-ai-incident-response.md`](../../ai/plan-ai-incident-response.md), [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md), [`resilience/procedure-cross-domain-incident-coordination.md`](../../resilience/procedure-cross-domain-incident-coordination.md), [`ai/standard-ai-security-and-risk.md`](../../ai/standard-ai-security-and-risk.md), [`ai/framework-ai-governance-and-risk.md`](../../ai/framework-ai-governance-and-risk.md), [`ai/procedure-ai-model-lifecycle-management.md`](../../ai/procedure-ai-model-lifecycle-management.md), [`ai/standard-ai-and-agentic-development-security.md`](../../ai/standard-ai-and-agentic-development-security.md), [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md), [`resilience/template-tabletop-exercise.md`](../../resilience/template-tabletop-exercise.md), [`ai/charter-ai-governance-council.md`](../../ai/charter-ai-governance-council.md), [`ai/guide-ai-board-oversight.md`](../../ai/guide-ai-board-oversight.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-003\
**Last Reviewed:** 2026-08-06

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Why this matters

An AI system in production can experience an incident: a compromise, a harmful or manipulated output, a data exposure, or a failure that crosses into other systems. The readiness question the governing body faces before go-live is not whether an incident is possible but whether the organization can detect it, respond to it, coordinate across the teams it touches, and learn from it. The corpus defines a dedicated path for exactly that; readiness is having the path in place before production, not assembling it during the first incident.

The governing body's role here is oversight, not operation. It does not run the response; it satisfies itself beforehand that the response capability exists, is exercised, and reports back to it. This brief points to where the corpus defines each element of that capability. The readiness picture it draws is synthesized across several corpus sources; see the limitations.

## What the corpus establishes

The corpus defines AI incident-response readiness as a set of capabilities that exist before an AI system goes into production.

- **A dedicated AI incident-response path.** The [AI incident response plan](../../ai/plan-ai-incident-response.md) sets out AI-specific incident classes and triggers, severity criteria, a defined lifecycle, and the evidence to preserve, operating alongside the general security and privacy procedures rather than replacing them.
- **A general incident procedure the AI path runs alongside.** The [security incident response procedure](../../security/procedure-security-incident-response.md) requires evidence preservation and a post-incident review scaled to incident severity; the AI path inherits that baseline.
- **Cross-domain coordination.** When an AI incident also implicates personal data or general security, the [cross-domain incident coordination procedure](../../resilience/procedure-cross-domain-incident-coordination.md) runs it as a coordinated multi-stream response under a joint command, and it makes cross-stream exercising a standing obligation.
- **Detection, logging, and incident management as pre-production controls.** The [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) requires monitoring and logging as a dependency of investigation and of the classification and escalation of AI incidents through incident management (its sections 4.7 and 4.10); its evidence expectations (its section 5) are stated as what a system should maintain. The [AI logging and traceability requirements](../../security/standard-logging-and-monitoring.md) require AI systems to produce the event logs an investigation depends on, and the [AI development security standard](../../ai/standard-ai-and-agentic-development-security.md) adds concrete AI incident indicators and AI-specific response steps.
- **Incident response as a required control domain.** The [AI governance and risk framework](../../ai/framework-ai-governance-and-risk.md) treats incident response as one of the control domains a production AI system carries and, in its lifecycle model, releases a system with incident response among its operating capabilities; the [AI model lifecycle procedure](../../ai/procedure-ai-model-lifecycle-management.md) sets the pre-deployment gates a system passes before that release.
- **An escalation path and a reporting line.** The corpus defines a chartered executive AI governance body that receives escalated AI-related security or ethics incidents and approves responses to AI system failures with significant impact (the [executive AI governance charter](../../ai/charter-ai-governance-council.md), its section 4); this brief routes to that body rather than naming it. Above it, the [board oversight guide](../../ai/guide-ai-board-oversight.md) establishes the governing body's non-delegable accountability for AI outcomes and states what it should expect to receive, which includes significant AI incidents and their resolution (its section 7).
- **A way to exercise the capability.** The [tabletop exercise template](../../resilience/template-tabletop-exercise.md) provides a reusable structure for rehearsing an AI incident before a real one occurs.

## What this means for the organization

For the governing body and accountable executive leadership, incident-response readiness translates into a small set of things that are true before an AI system goes live. (This readiness reading is a composite of the sources above.)

- **The capability exists before production, not after the first incident.** The AI incident-response path, the detection and logging that contribute to it, and the escalation route are a dependency of an effective response; standing them up during an incident is standing them up too late.
- **The response is coordinated, not siloed.** When an AI incident engages more than one response domain, the joint-command arrangement the corpus defines is a dependency of the coordinated multi-stream response, and the streams respond as one rather than in parallel.
- **Accountability does not transfer to a supplier.** The governing body's accountability for AI outcomes is non-delegable; "the vendor handles incidents" answers a question the corpus places with the organization, not its provider.
- **The governing body has a reporting line into it.** Readiness includes the expectation, which the corpus states as a should, that the governing body receives significant AI incidents and their resolution on a regular cadence, and that critical AI risks escalate to it through the chartered executive AI governance body.
- **A rehearsed capability is evidence a documented one is not.** A plan that has been exercised through a tabletop is evidence of readiness in a way an unexercised document is not.

## Evidence to request

Each item is an evidence class the governing body can call for from management, and each is evidence for a named control or outcome.

- **The AI incident-response plan**, as evidence that the AI-specific classes, severity model, lifecycle, and evidence requirements in the [plan](../../ai/plan-ai-incident-response.md) are in place.
- **The evidence-preservation and post-incident-review process**, as evidence that the [security incident procedure](../../security/procedure-security-incident-response.md) baseline the AI path depends on is operating.
- **The cross-domain coordination arrangement**, as evidence that a multi-stream AI incident would run under the joint command the [coordination procedure](../../resilience/procedure-cross-domain-incident-coordination.md) defines.
- **The AI monitoring, logging, and traceability design**, as evidence for the detection and investigation controls in the [AI security standard](../../ai/standard-ai-security-and-risk.md) and the [logging and traceability requirements](../../security/standard-logging-and-monitoring.md).
- **The AI incident indicators and AI-specific response steps**, as evidence that the additions in the [AI development security standard](../../ai/standard-ai-and-agentic-development-security.md) are covered.
- **A completed tabletop exercise and its after-action report** for an AI incident, as evidence that the capability has been rehearsed per the [exercise template](../../resilience/template-tabletop-exercise.md).
- **The escalation and reporting path**, as evidence that escalated AI-related security or ethics incidents reach the chartered executive AI governance body defined in the [charter](../../ai/charter-ai-governance-council.md) and that significant incidents reach the governing body per the [oversight guide](../../ai/guide-ai-board-oversight.md).

## Limitations

- This page creates no compliance and imposes no requirement. The linked corpus documents govern; where this page differs from a corpus document, the corpus document prevails.
- This page carries composite claims. The readiness picture it draws is synthesized across several corpus sources, and the adopting organization validates that reading against its own structure and its own incident-response arrangements.
- The corpus documents this page points to carry the specific severity tiers, timeframes, retention periods, and named bodies. This page routes to them and does not reproduce them, so the corpus remains the single source for every value.
- This page makes no claim about how likely any incident is, and none of its statements should be read as a probability or a frequency.

**End of Document**
