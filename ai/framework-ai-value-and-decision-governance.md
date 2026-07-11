# AI Value and Decision-Governance Framework

**Document Title:** AI Value and Decision-Governance Framework\
**Document Type:** Framework\
**Version:** 0.0.1\
**Date:** 2026-07-11\
**Owner:** AI Governance Approver\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-maturity-model.md`](framework-ai-maturity-model.md), [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/charter-ai-governance-council.md`](charter-ai-governance-council.md), [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md), [`ai/procedure-ai-audit.md`](procedure-ai-audit.md), [`ai/standard-ai-inference-cost-governance.md`](standard-ai-inference-cost-governance.md), [`ai/guideline-ethical-ai-use.md`](guideline-ethical-ai-use.md), [`governance/standard-maturity-assessment-methodology.md`](../governance/standard-maturity-assessment-methodology.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI governance or regulatory change\
**Repository Path:** [`ai/framework-ai-value-and-decision-governance.md`](framework-ai-value-and-decision-governance.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This framework treats the **value an organization pursues from AI, and the quality of the decisions by which it pursues it, as governance evidence**. Where [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md) governs accountability, lifecycle, and risk, and [`ai/framework-ai-maturity-model.md`](framework-ai-maturity-model.md) assesses process-and-capability maturity against the corpus's CMMI ladder, this framework governs the *value and decision* axis: whether an AI initiative's intended value is stated and tracked, whether the decision to pursue it was made with the evidence a governing body would expect, and whether the realized benefits are classified honestly. These are governance constructs (signals and evidence a reviewer can inspect), not normative external requirements.

The constructs here are original CC BY-SA 4.0 content. The value-delivery framing originates by reference from a practitioner playbook (see Limitations) that the reference base does not hold; no content is reproduced from it. The three-tier value-maturity ladder in Section 3 is corroborated, by reference only, against the held CMU SEI AI Adoption Maturity Model (a copyright-restricted source that is not reproduced).

## Scope

In scope: the value and decision-governance signals an organization records for an AI use case across its life, from the idea stage through scaled operation. Applies to AI initiatives the organization builds, operates, or procures.

Out of scope, and governed elsewhere:

- **Process and capability maturity assessment** (the CMMI-laddered, domain-scored assessment), governed by [`ai/framework-ai-maturity-model.md`](framework-ai-maturity-model.md) and [`governance/standard-maturity-assessment-methodology.md`](../governance/standard-maturity-assessment-methodology.md). The value-maturity ladder here is a distinct value signal, not that capability ladder.
- **Accountability, lifecycle, and risk governance**, governed by [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md).
- **Operational cost governance** (inference budgets, cost ceilings, model-choice economics), governed by [`ai/standard-ai-inference-cost-governance.md`](standard-ai-inference-cost-governance.md); this framework's benefits taxonomy (Section 6) is the value-side companion to that cost-side standard.
- **Post-deployment performance monitoring** (metric, floor value, accountable owner recorded at deployment), governed by [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md).

## The value-maturity ladder

The value-maturity ladder is a **governance signal**, a coarse indicator of how far an AI initiative has progressed in delivering governed value. It is not the CMMI capability ladder (five tiers, Initial to Optimized) that [`governance/standard-maturity-assessment-methodology.md`](../governance/standard-maturity-assessment-methodology.md) defines and [`ai/framework-ai-maturity-model.md`](framework-ai-maturity-model.md) scores; an initiative's position on this value ladder and its process-maturity level are independent readings, and a high value tier does not by itself evidence process maturity (or the reverse).

| Value tier | Governance signal | Evidence a reviewer inspects |
| --- | --- | --- |
| **Production** | The initiative has reached a governed production deployment with a stated, tracked value hypothesis. | A deployment record with the idea-stage decision record (Section 4) closed out, and the deployment-time metric, floor value, and accountable owner recorded per [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md). |
| **Scaled** | The initiative operates reliably across more than one workflow or surface, with adoption tracked and value realization measured against the hypothesis. | Adoption tracking per deployment surface (Section 5); realized-benefit classification (Section 6) reviewed against the original hypothesis. |
| **Transformation** | AI-enabled value is embedded in how the function operates, sustained and re-evaluated as a continuing capability rather than a one-off project. | A continuing-governance record (periodic re-evaluation, retirement or re-scoping decisions recorded as decision-quality evidence). |

The tiers are cumulative: an initiative signals a tier only when the evidence for that tier and every lower tier is present. The ladder is a graduated value-maturity signal corroborated, by reference, against the held CMU SEI AI Adoption Maturity Model's five-level progression, whose value-delivery rungs span in-production value, at-scale reliable operation, and sustained transformation; that model is cited by reference only and is not reproduced.

## Idea-stage AI use-case decision record

The decision to pursue an AI use case is a governance decision, and its quality is evidenced by a record made **at the idea stage**, before build. The record is decision-quality evidence: a reviewer inspects it to confirm the decision rested on stated intent and named accountability rather than on undocumented enthusiasm. The record captures, at minimum:

- **A stated value hypothesis**, with the fixed key performance indicators (KPIs) by which the hypothesis will be judged. The KPIs are fixed at the idea stage so that later value realization is measured against the original intent, not a retrofitted target. Where the initiative reaches deployment, these idea-stage KPIs inform (but are distinct from) the operational performance thresholds that [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md) requires at deployment (metric, floor value, owner).
- **A named accountable owner** for the use case, consistent with the accountable-owner obligation the corpus already establishes (for example [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md) and [`ai/guideline-ethical-ai-use.md`](guideline-ethical-ai-use.md)). This framework does not redefine that obligation; it records the owner at the idea stage as part of the decision record.
- **The audit and assurance requirements** anticipated for the use case, cross-referenced to [`ai/procedure-ai-audit.md`](procedure-ai-audit.md), so the assurance expectation is set as a decision input rather than discovered late.

A decision not to pursue a use case, or to stop one, is recorded the same way: the record is evidence of a governed decision, whichever way it goes.

## Workflow embedding and adoption tracking

Value from AI is realized only when the AI-enabled capability is embedded in an actual workflow and used. Post-deployment, the organization records, as governance evidence:

- **A workflow-embedding statement** per deployment surface: which workflow the AI-enabled capability is embedded in, and how the capability changes that workflow (rather than existing as an unused sandbox artefact).
- **Adoption tracking** per deployment surface: whether the intended users are actually using the capability, so that a deployed-but-unadopted initiative is visible as such and its value hypothesis (Section 4) can be judged honestly. Adoption tracking is a governance signal, not a performance-monitoring metric; it complements, and does not replace, the operational monitoring in [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md).

This per-surface adoption view is what distinguishes a Scaled-tier initiative (Section 3) from one that is merely deployed once.

## Benefits taxonomy: green and brown dollars

The realized benefits of an AI initiative are classified so that the business case is judged on honest terms. This framework uses a two-way benefits taxonomy:

- **Green dollars**: net-new value, new revenue or capability the organization did not previously have.
- **Brown dollars**: cost avoidance and efficiency, savings against what the organization would otherwise have spent.

This is a benefits-classification vocabulary for business-case decision quality; the terms are financial, not environmental (they are unrelated to any environmental-sustainability sense of "green"). Classifying a claimed benefit as green or brown, and stating which, is decision-quality evidence: it prevents a cost-avoidance case from being presented as net-new value, and it lets a governing body weigh the benefit mix against the initiative's cost (governed on the cost side by [`ai/standard-ai-inference-cost-governance.md`](standard-ai-inference-cost-governance.md)). The taxonomy classifies benefits; it does not by itself validate that a claimed benefit is real, which remains a matter for the initiative's evidence.

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| CMU SEI AI Adoption Maturity Model v1.0 | Five-level adoption ladder (cited by reference) | Corroborates the value-maturity ladder (Section 3) as a governance signal; not reproduced |
| ISO/IEC 42001:2023 | Clauses 5, 9 | Leadership and value-alignment; performance evaluation of the AI management system |
| NIST AI RMF (2023) | Govern, Map | Governance of AI value and context; mapping intended benefits and impacts |
| [`ai/framework-ai-maturity-model.md`](framework-ai-maturity-model.md) | Whole document | The process-and-capability maturity view this framework's value view sits beside (distinct axes) |

## Limitations

This framework is original CC BY-SA 4.0 content; it is advisory governance guidance, not a normative external requirement, and adopting it does not by itself discharge any legal or regulatory obligation. Its value-delivery framing originates by reference from a practitioner "pilot to production" playbook that the reference base does not hold; no content is reproduced from that source, and the constructs here (the value tiers, the decision record, the adoption view, and the benefits taxonomy) are the corpus's own governance constructs, corroborated where possible against held sources. The three-tier value-maturity ladder cross-references the CMU SEI AI Adoption Maturity Model by reference only (that model is copyright-restricted and is not reproduced). A value tier and a benefits classification reflect the recorder's evidence and judgement and are subject to optimism bias; they are governance signals for a reviewer to inspect and challenge, not audited financial figures, and a high value tier does not by itself establish that an AI system is low-risk, high-quality, or safe (those are governed by the risk, model-risk, and assurance frameworks this document cross-references).

---

**End of Document**
