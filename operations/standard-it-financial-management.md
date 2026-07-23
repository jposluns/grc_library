# IT Financial Management Standard

**Document Title:** IT Financial Management Standard\
**Document Type:** Standard\
**Version:** 1.0.5\
**Date:** 2026-07-23\
**Owner:** Chief Information Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`operations/framework-it-service-management.md`](framework-it-service-management.md), [`operations/standard-capacity-and-performance-management.md`](standard-capacity-and-performance-management.md), [`operations/register-asset-inventory.md`](register-asset-inventory.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`ai/standard-ai-inference-cost-governance.md`](../ai/standard-ai-inference-cost-governance.md), [`governance/procedure-grc-programme-management-and-annual-review.md`](../governance/procedure-grc-programme-management-and-annual-review.md)\
**Classification:** Public\
**Category:** IT Operations\
**Review Frequency:** Annual and upon material change to financial reporting, cloud commitment posture, or AI cost profile\
**Repository Path:** [`operations/standard-it-financial-management.md`](standard-it-financial-management.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines how IT expenditure is planned, allocated, monitored, attributed, and optimized. It expresses outcomes and governance expectations, not a specific accounting policy. The standard supports the capacity and performance management standard, the AI inference cost governance standard, and the supplier and third-party risk management policy by providing the financial discipline within which those operate.

---

## 2. Scope

This standard applies to:

1. Capital and operating IT expenditure.
2. Cloud, SaaS, AI inference, and managed-service expenditure.
3. Hardware, software, and licensing expenditure.
4. Internal labour cost attribution where IT outcomes are part of the organization's service cost.
5. Vendor commitments (reserved instances, committed-use discounts, prepaid SaaS, AI inference prepay).
6. Charge-back and show-back arrangements with internal consumers.

It does not cover external customer pricing of products (which is a commercial topic).

---

## 3. Principles

| Principle | Description |
| --- | --- |
| Financial transparency | Cost is visible to the team that incurs it |
| Cost ownership | Every cost has a named owner |
| Cost vs value | Cost is evaluated against the outcome it produces |
| Forecast discipline | Spend is forecast, tracked against forecast, and explained when it deviates |
| Optimization as practice | Cost optimization is continuous, not episodic |
| Risk-adjusted savings | Cost savings are weighed against resilience, security, and customer-experience risk |
| Vendor lock-in awareness | Cost decisions account for the future cost of switching providers |
| Sustainability | Where the organization has sustainability commitments, cost decisions reflect them |

---

## 4. Cost taxonomy

| Cost category | Description |
| --- | --- |
| Cloud infrastructure | Compute, storage, network, platform services |
| Software licensing | Commercial software, SaaS subscriptions |
| AI and machine learning | Inference, training, fine-tuning, evaluation, monitoring services |
| Hardware | Servers, network equipment, end-user devices |
| Telecommunications | Connectivity, voice, wireless |
| Managed services | Operating contracts with vendors |
| Professional services | Project-based vendor engagement |
| Internal labour | Engineering, operations, support time |
| Security tooling | Security platforms, threat intelligence subscriptions |
| Observability tooling | Telemetry platforms |
| Other | Categorized explicitly; the "Other" bucket is small |

Each category has a documented definition and an owner.

---

## 5. Attribution

| Element | Description |
| --- | --- |
| Tagging and labelling | Resources tagged with cost-centre, application, environment, owner per the cloud baselines |
| Charge-back vs show-back | The organization's accounting policy selects between fully-allocated charge-back, partial charge-back, or show-back |
| Unallocated cost | Unattributed cost is investigated; sustained un-attributable cost is a finding |
| Shared services | Allocation method for shared services is documented |
| Internal labour | Where internal labour is attributed, the basis is documented |
| AI cost attribution | Per the AI inference cost governance standard, including agentic cost amplification |

---

## 6. Budgeting

| Activity | Description |
| --- | --- |
| Annual budget | Approved per the organization's financial cycle |
| Quarterly re-forecast | Re-forecast updates the trajectory against actuals and emerging signals |
| Project budgeting | Discrete initiatives have their own budget with go and no-go gates |
| Run vs change | Run cost (steady-state operation) separated from change cost (initiatives) |
| Budget governance | Approval thresholds documented; sign-off authority matches the magnitude |
| Contingency | Budget contingency held for incident response and unforeseen capacity needs |

---

## 7. Monitoring and forecasting

| Activity | Description |
| --- | --- |
| Daily and weekly cost telemetry | Available at the team and application level |
| Anomaly detection | Sudden cost growth alerts the cost owner |
| Forecast trajectory | Burn-rate forecasting against budget; alerts on projected overrun |
| Variance review | Material variance is investigated and explained |
| Provider invoice reconciliation | Provider invoices reconciled to internal telemetry |
| Reporting cadence | Cost reporting cadence to leadership and to the board where relevant |

---

## 8. Optimization

| Practice | Description |
| --- | --- |
| Rightsizing | Compute and storage rightsized against observed utilization |
| Idle and zombie resources | Detected and reclaimed |
| Commitment management | Reserved and committed pricing applied where demand is predictable |
| Spot and preemptible | Used where the workload tolerates interruption |
| Storage tiering | Cold and archive tiers used per the records retention schedule |
| Network egress | Egress patterns reviewed; architecture adjustments where the cost-benefit profile justifies |
| Licence rightsizing | Per-seat, per-core, and per-transaction licences reconciled with actual use |
| AI model selection | Model selection per the AI inference cost governance standard |
| SaaS rationalization | Overlapping SaaS detected and consolidated |
| Sunset | Unused or low-value services sunset on a documented schedule |

---

## 9. Vendor commitment management

| Practice | Description |
| --- | --- |
| Commitment register | Active vendor commitments inventoried with expiry dates |
| Commitment-vs-demand | Commitments validated against forecast demand; over- or under-commitment surfaced |
| Renewal lead-time | Renewals planned with sufficient lead-time to negotiate |
| Concentration risk | Commitment concentration considered alongside supplier concentration per the concentration register |
| Exit cost | Exit cost is part of the commitment evaluation; per the cloud exit and data portability standard |
| Negotiated discounts | Negotiated discounts tracked; expiry and step-down handled |

---

## 10. AI cost governance

| Practice | Description |
| --- | --- |
| Cost telemetry | Per the AI inference cost governance standard |
| Cost ceilings | Per-application and per-tenant ceilings configured |
| Agent chain controls | Limits on agentic chain length and per-task cost |
| Provider mix | Cost-aware routing across providers and models where justified |
| Fine-tuning vs prompting trade-off | Periodically reassessed |
| Training cost | Tracked separately from inference where the organization trains or fine-tunes |
| Cost as a risk | Sustained unjustified AI cost growth treated as a finding |

---

## 11. Green and sustainability considerations

| Practice | Description |
| --- | --- |
| Provider sustainability commitments | Reviewed in supplier selection |
| Region selection | Region selection weighs sustainability where the organization has commitments and the data residency profile allows |
| Workload efficiency | Efficiency improvements counted as both cost and emissions reductions |
| Decommissioning | Decommissioning is environmentally responsible; per the secure decommissioning procedure |
| Reporting | Where the organization publishes sustainability metrics, IT contribution is included |

---

## 12. Governance

| Element | Description |
| --- | --- |
| FinOps function | A named function (team or role) owns IT financial management |
| Cross-functional engagement | Engineering, operations, security, finance, and procurement are joint stakeholders |
| Cost councils | Periodic forums review cost trends, optimization opportunities, and commitment decisions |
| Decision rights | Documented decision rights for spend authorization, commitment, and exception |
| Performance metrics | Cost-per-customer, cost-per-transaction, cost-per-service, and unit economics tracked where applicable |
| Reporting | Reporting to executive, finance leadership, and the board where material |

---

## 13. Integration with related programmes

| Programme | Integration point |
| --- | --- |
| Capacity and performance management | Capacity decisions cost-aware; cost decisions performance-aware |
| Service-level management | SLOs and cost trade-offs explicit |
| Asset inventory | Asset inventory is the basis for cost attribution |
| Supplier and third-party risk | Cost is a supplier dimension alongside risk |
| AI governance | AI cost is a governance dimension |
| Resilience programme | Resilience headroom cost is justified and budgeted |
| Sustainability reporting | IT contribution reported where applicable |

---

## 14. Financial reporting and compliance

| Element | Description |
| --- | --- |
| Audit trail | Cost data is auditable; sources, transformations, and allocations documented |
| Period-end close | IT cost contributions to period-end close are timely and accurate |
| Capitalization policy | Capitalization of software and infrastructure follows the organization's accounting policy |
| Tax considerations | Where tax treatment depends on IT cost classification, classification is consistent |
| Internal control | IT financial processes are subject to the organization's internal control framework |
| External reporting | Where IT cost contributes to external reporting (regulated disclosures, sustainability, customer-facing transparency), the contribution is supported by evidence |

---

## 15. Operating expectations

1. Annual budget, quarterly re-forecast, and continuous cost telemetry are the baseline cadence.
2. Cost optimization is a continuous engineering and operations practice, not an annual project.
3. Vendor commitments are reviewed before each renewal and validated against demand.
4. AI cost growth is reviewed monthly with engineering and finance.
5. Cost-related decisions are documented; sustained unattributed spend is investigated.

---

## 16. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| FinOps Foundation | FinOps framework | Cloud financial operations |
| ITIL 4 | Service financial management | Service management |
| ISO/IEC 20000-1 | §8.4.1 Budgeting and accounting for services | Budgeting and accounting for services |
| COBIT 2019 | APO06 Managed Budget and Costs | Governance of enterprise IT |
| ISO/IEC 27001:2022 | A.5.13 Labelling of information, A.5.14 Information transfer (tangentially) | Tagging discipline |
| ISO 14001 | Environmental management | Sustainability cross-walk |
| GAAP and IFRS | Capitalization and depreciation of software and infrastructure | Accounting |

---

## 17. Limitations

This standard is a CC BY-SA 4.0 baseline. IT financial practice is highly organization-specific and depends on the accounting policy in force. The standard expresses outcomes and governance expectations rather than specific accounting treatments. Adopting organizations confirm current accounting policy and select tooling and allocation methods consistent with that policy.

---

**End of Document**
