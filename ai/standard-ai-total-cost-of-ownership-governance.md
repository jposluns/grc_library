# AI Total Cost of Ownership Governance Standard

**Document Title:** AI Total Cost of Ownership Governance Standard\
**Document Type:** Standard\
**Version:** 0.0.1\
**Date:** 2026-09-04\
**Owner:** AI Governance Approver\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-value-and-decision-governance.md`](framework-ai-value-and-decision-governance.md), [`ai/standard-ai-inference-cost-governance.md`](standard-ai-inference-cost-governance.md), [`operations/standard-it-financial-management.md`](../operations/standard-it-financial-management.md), [`ai/standard-ai-model-succession-and-identity.md`](standard-ai-model-succession-and-identity.md), [`ai/standard-ai-human-oversight.md`](standard-ai-human-oversight.md), [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md), [`ai/register-model-registry.md`](register-model-registry.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material AI portfolio, provider-pricing, or sourcing-model change\
**Repository Path:** [`ai/standard-ai-total-cost-of-ownership-governance.md`](standard-ai-total-cost-of-ownership-governance.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard governs the full-lifecycle cost of an AI capability as governance evidence. A business case, or a continue-or-retire decision, judged on metered runtime spend alone systematically understates cost, because the costs that make an AI capability's lifecycle total diverge from its provider invoice are the non-metered ones: people, integration, oversight, governance overhead, model succession, and decommission. Recording, owning, and re-forecasting the total lets the cost side of an AI decision be weighed on lifecycle terms.

It is the cost-side companion to two existing documents and does not restate either. The value side of an AI decision (the value hypothesis, benefit classification, attribution, and value re-forecasting) is governed by [`ai/framework-ai-value-and-decision-governance.md`](framework-ai-value-and-decision-governance.md); the metered runtime cost controls (inference, training, hosting, retrieval, tool invocation, and evaluation budgeting, ceilings, enforcement, and anomaly response) are governed by [`ai/standard-ai-inference-cost-governance.md`](standard-ai-inference-cost-governance.md). This standard supplies the lifecycle cost aggregate that the value framework weighs, and consumes the inference standard's actuals as one line of that aggregate.

The constructs here are original CC BY-SA 4.0 content. This standard does not imply certification or conformity assessment against any external cost-management methodology, and it is an overlay on, not a substitute for, an organization's finance function.

---

## 2. Scope

In scope: the per-capability TCO record, its eight lifecycle cost categories, its forecast-actual-re-forecast cadence, and its use in governance decisions. A TCO record attaches at the initiative or use-case granularity, matching the decision record of [`ai/framework-ai-value-and-decision-governance.md`](framework-ai-value-and-decision-governance.md), so cost and value pair up for the same decision; the runtime row aggregates that initiative's features.

Out of scope, with the governing document named:

- The value side of the decision: [`ai/framework-ai-value-and-decision-governance.md`](framework-ai-value-and-decision-governance.md).
- Runtime cost control (ceilings, enforcement, anomaly response): [`ai/standard-ai-inference-cost-governance.md`](standard-ai-inference-cost-governance.md); this standard consumes its actuals and quarterly forecast as the runtime row and adds nothing on runtime control.
- The enterprise cost taxonomy, attribution, and budgeting base: [`operations/standard-it-financial-management.md`](../operations/standard-it-financial-management.md); this standard overlays the AI-lifecycle-specific requirements on that base and figures roll up to it.
- The model-succession transition process: [`ai/standard-ai-model-succession-and-identity.md`](standard-ai-model-succession-and-identity.md); this standard owns only the cost dimension of succession.
- Decommissioning mechanics: [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md); this standard owns only the cost dimension of decommission.

---

## 3. Principles

| Principle | Statement |
| --- | --- |
| Lifecycle completeness | Every cost category is estimated; a category recorded as zero states why it is zero, rather than being omitted as unexamined. |
| Single named owner | Each TCO record has one accountable owner (the owner of the initiative's decision record); production may be delegated, accountability may not. |
| Forecast before commitment | A capability is not procured or built without a TCO record forecast at the idea stage. |
| Non-metered costs are first-class | Human oversight, governance overhead, and internal labour are estimated and carried, not treated as free because they carry no invoice. |
| No double-counting with value | A cost carried in the TCO record and a disbenefit recorded in the value case do not both count the same effort against the initiative. |
| Figures carry their evidence quality | Each category figure is labelled measured or estimated; a mixed total says so. |

---

## 4. TCO cost taxonomy

The total cost of ownership of an AI capability is the sum of eight lifecycle cost categories. Each category in a TCO record carries an estimate or an actual; a category recorded as zero states why. These categories are AI-lifecycle refinements of the enterprise cost taxonomy in [`operations/standard-it-financial-management.md`](../operations/standard-it-financial-management.md); they do not replace it, and figures roll up to it.

| Category | Definition | Typical components | Governing activity (referenced, not duplicated) |
| --- | --- | --- | --- |
| Acquisition and build | One-time cost of obtaining or constructing the capability | Licence and subscription commitments, procurement and vendor-negotiation effort, initial engineering and prompt or workflow development, initial evaluation-suite construction | Vendor assessment per the supply-chain documents |
| Data | Cost of the data the capability depends on | Data acquisition and licensing, preparation and labelling, quality validation, ongoing refresh | Data quality per [`ai/standard-ai-data-quality-and-readiness-validation.md`](standard-ai-data-quality-and-readiness-validation.md); training data per [`ai/procedure-training-data-governance.md`](procedure-training-data-governance.md) |
| Runtime | Metered operating cost | Inference, training and fine-tuning, hosting, retrieval, tool invocation, evaluation runs | Governed by [`ai/standard-ai-inference-cost-governance.md`](standard-ai-inference-cost-governance.md); the TCO record consumes its actuals and quarterly forecast as this row |
| Integration | Cost of connecting the capability to the workflows it serves | Interface and middleware engineering, workflow redesign, user training and change management | Workflow embedding per [`ai/framework-ai-value-and-decision-governance.md`](framework-ai-value-and-decision-governance.md) (which governs whether embedding happened, not what it cost) |
| Human oversight and governance overhead | Recurring cost of the human and governance controls the capability's risk tier requires | Review and approval effort per [`ai/standard-ai-human-oversight.md`](standard-ai-human-oversight.md), audit and assurance effort per [`ai/procedure-ai-audit.md`](procedure-ai-audit.md), impact assessments, incident-response readiness, compliance reporting | The oversight obligations are governed by the named documents; this standard prices them |
| Monitoring and maintenance | Recurring cost of keeping the capability performing | Performance and drift monitoring, evaluation refresh, prompt and configuration maintenance, telemetry tooling | Monitoring per [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md) |
| Model succession | Recurring cost of transitioning to successor models | Successor evaluation and pause-and-compare validation, regression testing, migration engineering, parallel-run cost, re-issuance of access and standing | The transition process is governed by [`ai/standard-ai-model-succession-and-identity.md`](standard-ai-model-succession-and-identity.md); this standard requires it be costed as a recurring category, because provider-driven model retirements make succession a certainty on external models, not a contingency |
| Decommission | Terminal cost of retiring the capability | Data disposition, contract exit, workflow reversion or replacement, archive and record retention, final reconciliation | Decommission mechanics per [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md) |

---

## 5. The TCO record

Each AI capability carries a TCO record, created at the idea stage beside the idea-stage decision record of [`ai/framework-ai-value-and-decision-governance.md`](framework-ai-value-and-decision-governance.md), so the decision to pursue the use case is made against a lifecycle cost estimate rather than a runtime quote.

| Attribute | Requirement |
| --- | --- |
| Creation | At the idea stage, before build or procurement commitment; a capability procured or built without a TCO record is a governance finding. |
| Content | A per-category forecast across all eight categories; the estimation basis for each (metered actuals, vendor quote, effort estimate, or analogy to a comparable capability); and the accrual convention for one-time costs (expensed, or amortized over a stated assumed capability life). |
| Owner | The named accountable owner of the idea-stage decision record owns the TCO record. |
| Actuals | Metered categories accrue from telemetry and invoices per the inference-cost standard; non-metered categories accrue as measured actuals where invoice or contract evidence exists (for example licence, subscription, and data-licensing costs) and otherwise on the section-6 estimation bases, refreshed at each re-forecast. |
| Re-forecast cadence | Quarterly, aligned with the inference-cost standard's quarterly forecast and the value framework's benefit re-forecast, so the cost and value sides of an initiative move on the same rhythm; each re-forecast records variance by category and explains material variance. |
| Evidence quality | Each category figure is labelled measured or estimated; measured and estimated figures are reported in separate columns, and a combined total states that it mixes the two (a lifecycle total is at best as firm as its estimated categories). |
| Consumption | The current TCO figure is the cost input to the value framework's net-value comparison and to any continue, re-scope, or retire recommendation. |

---

## 6. Non-metered and internal cost requirements

Runtime cost is metered and therefore visible; the costs that make an AI capability's lifecycle total diverge from its invoice are the non-metered ones, and a TCO discipline that prices only what a provider bills has reproduced the failure it exists to prevent.

1. **Human oversight is priced.** Where the capability's risk tier requires human review, approval, or exception handling per [`ai/standard-ai-human-oversight.md`](standard-ai-human-oversight.md), the recurring effort is estimated (reviewer hours at a loaded rate, or an equivalent internal convention) and carried in the TCO record. An oversight burden that grows with volume is forecast as volume-scaled, not flat.
2. **Governance and compliance overhead is priced.** Audit and assurance effort, impact assessments, incident-response readiness, and compliance reporting attributable to the capability are estimated and carried. Where overhead is shared across a portfolio, an apportionment convention is stated once and applied consistently rather than re-argued per capability.
3. **Internal labour is priced.** Engineering, data, and operations time on build, integration, maintenance, and succession is estimated and carried, on the same internal-labour basis the enterprise financial-management taxonomy uses.
4. **Double-counting with the value side is prevented.** The value framework records added review effort and rework as disbenefits where they offset a claimed benefit. A cost carried in the TCO record and a disbenefit recorded in the value case must not both count the same effort against the initiative. The convention: designed-in oversight and operating cost belong in the TCO record; unplanned rework and displaced effort discovered after deployment belong on the value side as disbenefits. The TCO record and the value validation each state which side carries a contested item.

Estimates are governance signals, not audited figures; each carries its estimation basis so a reviewer can challenge it.

---

## 7. Lifecycle-stage TCO controls

| Lifecycle stage | TCO control |
| --- | --- |
| Idea | TCO record created with all eight categories forecast; the decision record cross-references it. |
| Build | Acquisition, data, and integration actuals accrued against forecast; a material forecast breach is surfaced before acceptance, not after. |
| Acceptance into service | TCO record refreshed with as-built figures; the runtime row reconciled to the cost ceiling and telemetry set-up the inference-cost standard requires at this stage. |
| Production | Quarterly re-forecast; runtime actuals from the inference-cost standard; non-metered accruals refreshed. |
| Succession event | Succession cost accrued against the succession category; a supplier-forced succession whose cost was not forecast is a variance to explain, and repeated unforecast successions raise the category's forward estimate. |
| Decommission | Terminal costs accrued; a final TCO statement (lifetime total by category, against the original idea-stage forecast) closes the record and is retained as decision-quality evidence for future business cases. |

---

## 8. TCO in governance decisions

The TCO figure is consumed at the decisions where lifecycle cost matters:

- **Build-versus-buy and sourcing.** The comparison weighs lifecycle totals, not acquisition price or runtime quote alone.
- **Net-value judgement.** The current TCO is the cost input to the value framework's net-value comparison; the two are read together.
- **Continue, re-scope, or retire.** A TCO materially exceeding its forecast, without matching value, is a governance finding routed like a value shortfall.
- **Portfolio roll-up.** Per-capability TCO records roll up to a portfolio view for governing-body oversight.

---

## 9. Reporting

| Report | Cadence | Audience |
| --- | --- | --- |
| Per-capability TCO record | At creation, then quarterly re-forecast | Capability owner, governance function |
| Portfolio TCO summary | Quarterly | Governing body, finance function |
| Decision-time TCO statement | At each build-or-buy, continue-or-retire decision | Decision authority |

---

## 10. Framework alignment

| Framework | Reference point | Relationship |
| --- | --- | --- |
| NIST AI RMF 1.0 (NIST AI 100-1) | MAP 3 (expected benefits and costs identified) and MANAGE (resources to manage AI risks; mechanisms to sustain the value of deployed systems) | Lifecycle-cost recording is the cost half of MAP 3's benefit-and-cost identification and supports the resourcing the MANAGE function expects. |
| ISO/IEC 42001:2023 | Clause 7 (support and resources); clauses 8 and 9 (operation, performance evaluation) | The TCO record is the resource-cost evidence for clause 7 and feeds performance evaluation; see-also for adopters who hold the standard. |
| COBIT 2019 | APO06 Managed Budget and Costs | The per-capability TCO record is the AI-specific instance of budget-and-cost management for AI capabilities. |
| NIST AI 600-1 (Generative AI Profile) | Environmental impacts | The environmental-cost angle is carried by [`ai/standard-ai-inference-cost-governance.md`](standard-ai-inference-cost-governance.md); this standard references it rather than restating. |

Corpus-internal: [`operations/standard-it-financial-management.md`](../operations/standard-it-financial-management.md) is the enterprise cost-taxonomy base this standard overlays; [`ai/framework-ai-value-and-decision-governance.md`](framework-ai-value-and-decision-governance.md) is the value-side companion.

---

## 11. Limitations

This is a CC BY-SA 4.0 reference baseline, not audited financial guidance. TCO figures rest on estimates for the non-metered categories and are governance signals, not audited financials. The standard is an overlay on, not a substitute for, an organization's FinOps or management-accounting function; allocation conventions such as amortization schedules and shared-platform apportionment belong to the finance function. Adopting organizations validate applicability against their own operating model and cost-accounting conventions.

---

**End of Document**
