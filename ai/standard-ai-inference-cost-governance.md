# AI Inference Cost Governance Standard

**Document Title:** AI Inference Cost Governance Standard 
**Document Type:** Standard 
**Version:** 0.0.1 
**Date:** 2026-05-28 
**Owner:** AI Governance Approver 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md), [`ai/standard-ai-access-and-agent-permissions.md`](standard-ai-access-and-agent-permissions.md), [`ai/register-model-registry.md`](register-model-registry.md), [`ai/procedure-foundation-model-lifecycle.md`](procedure-foundation-model-lifecycle.md), [`operations/standard-service-level-management.md`](../operations/standard-service-level-management.md), [`governance/framework-sustainability-and-responsible-technology.md`](../governance/framework-sustainability-and-responsible-technology.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md) 
**Classification:** Public 
**Category:** AI Governance 
**Review Frequency:** Annual and upon material AI portfolio, provider-pricing, or capacity-planning change 
**Repository Path:** [`ai/standard-ai-inference-cost-governance.md`](standard-ai-inference-cost-governance.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This standard defines how the organisation governs the cost of AI inference and training: budgeting, allocation, ceiling enforcement, model-choice criteria, monitoring, anomaly response, and reporting. AI costs are volatile and easily exceed forecasts; this standard ensures that AI use is economically rational and that runaway spend cannot occur silently.

---

## Scope

This standard applies to:

1. **Inference cost** of foundation models consumed from external providers.
2. **Training and fine-tuning cost** for internally-trained, fine-tuned, or open-source-deployed models.
3. **Hosting cost** of self-hosted models including compute (GPU and accelerator), storage, and networking.
4. **Vector store and retrieval cost** where retrieval supports AI features.
5. **Tool-invocation cost** where AI agents trigger downstream paid APIs.
6. **Evaluation cost** where evaluation runs consume substantial inference or compute.

It does not duplicate the broader IT financial management standard; it overlays AI-specific requirements on cost ownership and control.

---

## Section 1: principles

| Principle | Statement |
| --- | --- |
| Per-feature accountability | Every production AI feature has a named owning role accountable for its cost |
| Cost transparency | Inference cost is observable per request, per session, per feature, per customer where applicable |
| Cost ceilings | Every AI feature has a hard ceiling on cost per session or per defined unit; exceeded ceilings halt and report |
| Model-choice rigour | Model choice considers cost alongside capability, safety, and latency; the cheapest model that meets requirements is preferred |
| Anomaly response | Cost anomalies trigger investigation as a security signal (potential abuse or compromise) and as a financial signal |
| Sustainability | Inference and training compute is tracked for energy and carbon impact per the sustainability framework |

---

## Section 2: budgeting and allocation

| Control area | Requirement |
| --- | --- |
| Annual budget | Each owning function commits to an annual AI cost budget, broken down by feature and by provider |
| Quarterly forecast | Forecast updated quarterly with variance analysis |
| Allocation model | Costs allocated to the owning function via showback at minimum; chargeback where the organisation operates internal financial accountability at this granularity |
| Customer-level cost attribution | Where the AI feature is customer-facing and material, per-customer cost attribution supports product economics |
| Cost-tier classification | Each AI feature classified as High Cost, Medium Cost, Low Cost based on per-unit and aggregate spend; classification drives controls |

---

## Section 3: cost ceilings and rate limits

Every production AI feature enforces:

| Control area | Requirement |
| --- | --- |
| Per-request ceiling | Maximum allowed cost per inference call; exceeded calls are short-circuited or downgraded to a cheaper model |
| Per-session ceiling | Maximum allowed cost per user session or per agent session; exceeded sessions halt with an alert and a user-visible message where appropriate |
| Per-feature daily ceiling | Maximum aggregate spend per feature per day; exceeded ceilings trigger an alert; persistent breach triggers feature suspension |
| Per-customer ceiling | Where applicable for customer-facing features; exceeded ceilings trigger account-level review |
| Hard kill switch | Each feature has a documented kill switch that disables AI processing while preserving non-AI service continuity |

The ceilings are configured per the cost-tier classification and reviewed at minimum quarterly.

---

## Section 4: model-choice criteria

When selecting a model for a use case, the model registry entry documents the rationale across these criteria:

| Criterion | Requirement |
| --- | --- |
| Capability fit | The model demonstrably passes the use-case eval suite |
| Safety profile | The model passes safety, refusal, and adversarial evaluations |
| Latency | The model meets the SLA committed to the user |
| Cost per unit | The model's cost per inference unit (token, image, second) under expected usage patterns |
| Cost predictability | Pricing stability and the provider's notice period for price changes |
| Substitutability | Effort to migrate to an alternative |
| Sustainability | Documented energy or emissions footprint where available |
| Restricted-data fit | The model's contractual and architectural fit for the data classification involved |

The standard prefers the smallest, fastest, cheapest model that meets the requirements. Use of frontier-class models for routine tasks requires documented justification.

---

## Section 5: monitoring and anomaly response

| Monitoring area | Requirement |
| --- | --- |
| Per-feature daily cost dashboard | Always-on; reviewed by owners weekly minimum |
| Token consumption per feature | Tracked; growth trends flagged |
| Prompt-length distribution | Tracked; sudden tail shifts investigated |
| Output-length distribution | Tracked |
| Rate-limit hits | Tracked; persistent hitting triggers capacity review |
| Cost anomaly alerts | Threshold-based; 2x daily baseline triggers investigation |
| Cost-per-customer outliers | Top decile reviewed monthly for legitimate use versus potential abuse |
| Training cost actuals vs forecast | Reviewed at training-run completion |
| Provider invoice reconciliation | Monthly reconciliation of metered usage against the provider's invoice |

Cost anomalies are dual-routed:

1. **Financial response.** Owner investigates; budget variance recorded; corrective action if persistent.
2. **Security response.** AI Security Maintainer investigates whether the anomaly indicates abuse, agent misbehaviour, or compromise. Cost runaway is a documented signal in the AI incident response plan.

---

## Section 6: feature lifecycle controls

| Lifecycle stage | Cost control |
| --- | --- |
| Design | Cost forecast included in the design document; cost-tier classification proposed |
| Build | Cost telemetry instrumented from the first integration |
| Pre-production | Load-test results include cost projection at expected production volume |
| Acceptance into service | Cost ceiling, kill switch, and dashboard verified before go-live |
| Production | Monitored per Section 5; ceilings enforced |
| Material change | Cost-impact assessment for any change projected to alter per-unit or aggregate cost by 20% or more |
| Retirement | Final cost reconciliation; supplier obligations closed; cost attribution archived |

---

## Section 7: agent and autonomous workflow controls

Agentic and autonomous workflows have outsized cost-runaway potential.

| Control area | Requirement |
| --- | --- |
| Chain-length limit | Maximum sequential tool invocations per agent session; exceeded chains halt |
| Cost-per-session ceiling | Halts session when reached |
| Recursive workflow detection | Workflows that invoke themselves directly or indirectly are flagged and require explicit approval |
| Scheduled-task ceilings | Scheduled or background agents have daily and weekly aggregate cost ceilings |
| Idle-session timeout | Sessions with no user interaction for a defined period are closed even if technical liveness remains |

---

## Section 8: customer-facing cost transparency

Where the AI feature is customer-facing and the cost is passed through or otherwise relevant to the customer:

| Requirement |
| --- |
| Customer-facing pricing is communicated in the product documentation and the customer agreement |
| Where AI feature usage is metered, the metric and the cost basis are explicit |
| Sudden customer-spend spikes are surfaced to customer success or account management |
| Customer-controllable cost limits are offered where the customer is otherwise exposed to runaway costs |

---

## Section 9: provider-side cost-management

For external providers:

| Action | Requirement |
| --- | --- |
| Reserved-capacity or commit-based discounts | Where capacity is predictable, commit-based pricing is evaluated |
| Caching | Prompt and result caching where the use case allows |
| Cheaper-model fallback | Tiered routing: heavyweight model only where light-weight model is insufficient |
| Batch APIs | Use of provider batch APIs for non-interactive workloads |
| Off-peak scheduling | Non-interactive training and evaluation runs scheduled where compute is cheapest |

---

## Section 10: reporting

| Report | Cadence | Audience |
| --- | --- | --- |
| Per-feature cost dashboard | Continuous | Owners, AI Governance Approver |
| Quarterly AI cost report | Quarterly | AI Governance Council, Finance |
| Annual AI cost report | Annual | Executive Sponsor, Board where required |
| Anomaly summary | Per anomaly | AI Governance Approver, AI Security Maintainer, Finance |
| Variance to forecast | Quarterly | Owners, Finance |
| Per-customer cost outliers | Monthly | Customer success, product, risk |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 42001:2023 | §8 operation; §9 performance evaluation | AI management system |
| ISO/IEC 5055 | Automated source code quality measures | Where applicable |
| NIST AI RMF | MEASURE, MANAGE | Risk and operational management |
| FinOps Foundation Framework | Principles and capabilities | Industry practice for cloud cost governance |
| ISO/IEC 30134 series | Data centre energy efficiency | Sustainability cross-walk |
| EU AI Act | Article 26 (deployer obligations including efficient use); Articles 53, 55 (GPAI obligations) | EU regulation |
| GHG Protocol | Scope 2 and Scope 3 emissions | Sustainability accounting |

---

## Limitations

This standard is a public-domain baseline. AI provider pricing models, capability tiers, and platform features change frequently; specific commercial decisions belong to the procurement and finance functions. The standard provides the governance overlay; it does not substitute for FinOps practice, capacity planning, or specialist cost-engineering work.

---

**End of Document**
