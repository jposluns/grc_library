# AI Value and Decision-Governance Framework

**Document Title:** AI Value and Decision-Governance Framework\
**Document Type:** Framework\
**Version:** 0.0.3\
**Date:** 2026-09-04\
**Owner:** AI Governance Approver\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-maturity-model.md`](framework-ai-maturity-model.md), [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/charter-ai-governance-council.md`](charter-ai-governance-council.md), [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md), [`ai/procedure-ai-audit.md`](procedure-ai-audit.md), [`ai/standard-ai-inference-cost-governance.md`](standard-ai-inference-cost-governance.md), [`ai/guideline-ethical-ai-use.md`](guideline-ethical-ai-use.md), [`governance/standard-maturity-assessment-methodology.md`](../governance/standard-maturity-assessment-methodology.md), [`ai/standard-ai-total-cost-of-ownership-governance.md`](standard-ai-total-cost-of-ownership-governance.md)\
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
- **Operational cost governance**, by scope: metered runtime cost (inference budgets, ceilings, model-choice economics) governed by [`ai/standard-ai-inference-cost-governance.md`](standard-ai-inference-cost-governance.md), and full-lifecycle total cost of ownership governed by [`ai/standard-ai-total-cost-of-ownership-governance.md`](standard-ai-total-cost-of-ownership-governance.md); this framework's benefits taxonomy (Section 6) is the value-side companion to those cost-side standards, and its net-value comparison consumes the TCO aggregate as the cost input.
- **Post-deployment performance monitoring** (metric, floor value, accountable owner recorded at deployment), governed by [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md).

## The value-maturity ladder

The value-maturity ladder is a **governance signal**, a coarse indicator of how far an AI initiative has progressed in delivering governed value. It is not the CMMI capability ladder (five tiers, Initial to Optimized) that [`governance/standard-maturity-assessment-methodology.md`](../governance/standard-maturity-assessment-methodology.md) defines and [`ai/framework-ai-maturity-model.md`](framework-ai-maturity-model.md) scores; an initiative's position on this value ladder and its process-maturity level are independent readings, and a high value tier does not by itself evidence process maturity (or the reverse).

| Value tier | Governance signal | Evidence a reviewer inspects |
| --- | --- | --- |
| **Production** | The initiative has reached a governed production deployment with a stated, tracked value hypothesis. | A deployment record with the idea-stage decision record (Section 4) closed out, and the deployment-time metric, floor value, and accountable owner recorded per [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md). |
| **Scaled** | The initiative operates reliably across more than one workflow or surface, with adoption tracked and value realization measured against the hypothesis. | Adoption tracking per deployment surface (Section 5); a current post-implementation value validation record (Section 5) comparing realized net benefit (Section 6, attributed and baseline-adjusted) against the original hypothesis. |
| **Transformation** | AI-enabled value is embedded in how the function operates, sustained and re-evaluated as a continuing capability rather than a one-off project. | A continuing-governance record (re-evaluation on the benefit re-forecast cadence of Section 6; retirement or re-scoping decisions recorded as decision-quality evidence). |

The tiers are cumulative: an initiative signals a tier only when the evidence for that tier and every lower tier is present. The ladder is a graduated value-maturity signal corroborated, by reference, against the held CMU SEI AI Adoption Maturity Model's five-level progression, whose value-delivery rungs span in-production value, at-scale reliable operation, and sustained transformation; that model is cited by reference only and is not reproduced.

## Idea-stage AI use-case decision record

The decision to pursue an AI use case is a governance decision, and its quality is evidenced by a record made **at the idea stage**, before build. The record is decision-quality evidence: a reviewer inspects it to confirm the decision rested on stated intent and named accountability rather than on undocumented enthusiasm. The record captures, at minimum:

- **A stated value hypothesis**, with the fixed key performance indicators (KPIs) by which the hypothesis will be judged. The KPIs are fixed at the idea stage so that later value realization is measured against the original intent, not a retrofitted target. Where the initiative reaches deployment, these idea-stage KPIs inform (but are distinct from) the operational performance thresholds that [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md) requires at deployment (metric, floor value, owner).
- **A recorded baseline (the pre-intervention state)** for each fixed KPI: the value of the metric as it stands before the AI intervention, measured and recorded at the idea stage alongside the target. Realized value is the change from this baseline measured in the direction that represents improvement for that KPI (a reduction in a lower-is-better metric such as cycle time, error rate, cost, or review effort is a favourable change; an unfavourable change is not signed negative but is recorded as a disbenefit of that magnitude per Section 6, so it is subtracted under the netting convention rather than double-counted), so a KPI target fixed without a baseline leaves later value realization with no before-value to compare and no honest denominator for the improvement claimed. Before favourable changes across heterogeneous KPIs are aggregated as benefits and netted against disbenefit magnitudes (Section 6: net value = benefits minus disbenefits), each is valued into a common unit (typically monetary); a dimension that cannot honestly be valued into that unit is reported separately rather than summed. Where a true pre-intervention measurement cannot be taken, the nearest available proxy is recorded and identified as such.
- **A named accountable owner** for the use case, consistent with the accountable-owner obligation the corpus already establishes (for example [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md) and [`ai/guideline-ethical-ai-use.md`](guideline-ethical-ai-use.md)). This framework does not redefine that obligation; it records the owner at the idea stage as part of the decision record.
- **The audit and assurance requirements** anticipated for the use case, cross-referenced to [`ai/procedure-ai-audit.md`](procedure-ai-audit.md), so the assurance expectation is set as a decision input rather than discovered late.

A decision not to pursue a use case, or to stop one, is recorded the same way: the record is evidence of a governed decision, whichever way it goes.

## Workflow embedding and adoption tracking

Value from AI is realized only when the AI-enabled capability is embedded in an actual workflow and used. Post-deployment, the organization records, as governance evidence:

- **A workflow-embedding statement** per deployment surface: which workflow the AI-enabled capability is embedded in, and how the capability changes that workflow (rather than existing as an unused sandbox artefact).
- **Adoption tracking** per deployment surface: whether the intended users are actually using the capability, so that a deployed-but-unadopted initiative is visible as such and its value hypothesis (Section 4) can be judged honestly. Adoption tracking is a governance signal, not a performance-monitoring metric; it complements, and does not replace, the operational monitoring in [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md).

- **A post-implementation value validation** per initiative: a comparison of realized value (attributed and baseline-adjusted per Section 6) against the idea-stage value hypothesis (Section 4). It carries four fixed attributes so that it is an inspectable control rather than an aspiration:
  - **Timing**: conducted once the initiative has operated long enough for value to be observable (a validation window set at the idea stage, and no later than the initiative's first review-frequency cycle), then repeated on the benefit re-forecast cadence (Section 6).
  - **Owner**: the named accountable owner in the idea-stage decision record (Section 4) owns the validation; production may be delegated, accountability may not.
  - **Output artefact**: a written post-implementation validation record stating the realized net value, its attribution and evidence confidence (Section 6), the variance to hypothesis, and a recommendation (continue, re-scope, or retire).
  - **Failure consequence**: where realized value is materially below the hypothesis, or the evidence does not support the claim, the record triggers a governed decision (re-scope, further investment, or retirement) recorded as decision-quality evidence per Section 4, rather than being left as an open shortfall. A missing or overdue validation is itself a governance finding, and the initiative cannot signal the Scaled or Transformation value tier (Section 3) without a current one.

This per-surface adoption view is what distinguishes a Scaled-tier initiative (Section 3) from one that is merely deployed once.

## Benefits taxonomy: green and brown dollars, and disbenefits

The realized benefits of an AI initiative are classified so that the business case is judged on honest terms. This framework uses a three-way benefits taxonomy:

- **Green dollars**: net-new value, new revenue or capability the organization did not previously have.
- **Brown dollars**: cost avoidance and efficiency, savings against what the organization would otherwise have spent.
- **Disbenefits (red dollars)**: negative value the initiative introduces or displaces onto the organization, for example effort displaced rather than removed (it reappears elsewhere), rework of AI-produced output, added human review or oversight burden that was NOT designed in (designed-in oversight cost is carried in the TCO record per [`ai/standard-ai-total-cost-of-ownership-governance.md`](standard-ai-total-cost-of-ownership-governance.md), not double-counted here), and erosion of user or customer trust. Each disbenefit is recorded as a positive magnitude of value lost, in the same common unit as benefits, and subtracted, so the business case is judged on honest **net** terms (net value = benefits minus disbenefits), not on gross benefits. A disbenefit left unrecorded can make a gross-positive case conceal a net-negative one.

This is a benefits-classification vocabulary for business-case decision quality; the terms are financial, not environmental (they are unrelated to any environmental-sustainability sense of "green"). Classifying a benefit as green, brown, or a disbenefit, and stating which, is decision-quality evidence: it prevents a cost-avoidance case from being presented as net-new value, exposes negative value that gross figures hide, and lets a governing body weigh the net benefit mix against the initiative's full-lifecycle cost (governed on the cost side by [`ai/standard-ai-total-cost-of-ownership-governance.md`](standard-ai-total-cost-of-ownership-governance.md), which aggregates metered runtime cost per [`ai/standard-ai-inference-cost-governance.md`](standard-ai-inference-cost-governance.md)). Classifying a benefit does not by itself establish that it is real or that the initiative caused it; the attribution and evidence-confidence disciplines below supply that check.

### Benefit attribution

Before a claimed green, brown, or disbenefit figure is relied on in the business case, it is attributed to the initiative by a method proportionate to the claim's materiality:

- **Comparison to the recorded baseline** (the pre-intervention state recorded per Section 4): the realized value is the change from the baseline (per Section 4), valued into a common unit before it is netted (a favourable change contributes to benefits, an unfavourable change is recorded as a disbenefit magnitude per Section 6), not the post-intervention figure alone.
- **A counterfactual or control** where one is available: a comparable workflow, cohort, or period not exposed to the AI capability, so that value which would have arrived anyway (from a concurrent process change, seasonality, or an unrelated tailwind) is not credited to the initiative.
- **Confounder awareness**: material alternative causes are named, and where they cannot be isolated the attribution is qualified rather than asserted.

The rigour is proportionate to the claim: a small or low-materiality figure may rest on a baseline comparison alone, while a large or decision-shaping figure warrants a counterfactual and an explicit confounder review. Attribution is decision-quality evidence a reviewer inspects; a benefit or disbenefit asserted with no attribution method is recorded as unattributed and weighed accordingly.

### Benefit reforecasting

The idea-stage value hypothesis (Section 4) is not a one-time claim. Realized benefits and disbenefits are re-forecast against the hypothesis on a recurring cadence, at minimum quarterly, aligned with the cost-side re-forecast cadence that [`ai/standard-ai-inference-cost-governance.md`](standard-ai-inference-cost-governance.md) (quarterly forecast with variance analysis) and [`operations/standard-it-financial-management.md`](../operations/standard-it-financial-management.md) (annual budget, quarterly re-forecast) require, so that the value and cost sides of the same initiative move on the same rhythm. Each re-forecast records the current realized net value against the hypothesis, explains material variance, and, as a genuine forward re-forecast rather than a variance review alone, states an updated estimate of the value still to be realized, the forecast horizon it covers, and the assumptions that have changed since the last forecast; it feeds the value-tier signal (Section 3) and the post-implementation validation cadence (Section 5). A benefit that consistently under-realizes against its hypothesis is surfaced, not quietly re-baselined to the shortfall.

### Evidence confidence

A net-value figure aggregated across several benefit and disbenefit claims can mask a weakly-evidenced claim behind well-evidenced ones, the way a median can mask a low outlier. To instrument the optimism bias named in the Limitations, each claimed benefit and disbenefit carries an **evidence-confidence rating** (for example high, medium, or low) reflecting the strength of its attribution (above) and its underlying measurement. Adapting the compensating floor-check that [`ai/framework-ai-maturity-model.md`](framework-ai-maturity-model.md) applies to maturity outliers, any benefit or disbenefit rated **low** confidence, and any material benefit or disbenefit that is unattributed, is surfaced explicitly rather than absorbed into the aggregate. The net-value figure reported to a governing body is therefore the aggregate **together with its low-confidence and unattributed exceptions**, not the aggregate alone, so a reviewer sees which parts of the case are firm and which rest on optimistic or unvalidated evidence.

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| CMU SEI AI Adoption Maturity Model v1.0 | Five-level adoption ladder (cited by reference) | Corroborates the value-maturity ladder (Section 3) as a governance signal; not reproduced |
| ISO/IEC 42001:2023 | Clauses 5, 9 | Leadership and value-alignment; performance evaluation of the AI management system |
| NIST AI RMF (2023) | Govern; Map 1.4, Map 3; Manage 1.1, 2.2 | Governance of AI value and context; mapping intended business value and expected benefits (Map 1.4, Map 3); sustaining and reviewing the deployed system's realized value against stated objectives (Manage 1.1, 2.2) through attribution, re-forecasting, and post-implementation validation |
| [`ai/framework-ai-maturity-model.md`](framework-ai-maturity-model.md) | Whole document; floor-check | The process-and-capability maturity view this framework's value view sits beside (distinct axes); its compensating floor-check is adapted here for benefit evidence confidence (Section 6) |

## Limitations

This framework is original CC BY-SA 4.0 content; it is advisory governance guidance, not a normative external requirement, and adopting it does not by itself discharge any legal or regulatory obligation. Its value-delivery framing originates by reference from a practitioner "pilot to production" playbook that the reference base does not hold; no content is reproduced from that source, and the constructs here (the value tiers, the decision record, the adoption view, and the benefits taxonomy) are the corpus's own governance constructs, corroborated where possible against held sources. The three-tier value-maturity ladder cross-references the CMU SEI AI Adoption Maturity Model by reference only (that model is copyright-restricted and is not reproduced). A value tier and a benefits classification reflect the recorder's evidence and judgement and are subject to optimism bias; the benefit-attribution method and the evidence-confidence floor-check (Section 6) instrument that bias by surfacing low-confidence and unattributed claims rather than removing it, and these remain governance signals for a reviewer to inspect and challenge, not audited financial figures, and a high value tier does not by itself establish that an AI system is low-risk, high-quality, or safe (those are governed by the risk, model-risk, and assurance frameworks this document cross-references).

---

**End of Document**
