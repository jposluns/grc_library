# Capacity and Performance Management Standard

**Document Title:** Capacity and Performance Management Standard\
**Document Type:** Standard\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** Chief Information Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`operations/framework-it-service-management.md`](framework-it-service-management.md), [`operations/standard-service-level-management.md`](standard-service-level-management.md), [`operations/standard-site-reliability-engineering.md`](standard-site-reliability-engineering.md), [`operations/standard-observability-and-telemetry.md`](standard-observability-and-telemetry.md), [`operations/standard-it-financial-management.md`](standard-it-financial-management.md), [`ai/standard-ai-inference-cost-governance.md`](../ai/standard-ai-inference-cost-governance.md), [`resilience/policy-business-continuity-and-disaster-recovery.md`](../resilience/policy-business-continuity-and-disaster-recovery.md)\
**Classification:** Public\
**Category:** IT Operations\
**Review Frequency:** Annual and upon material change to demand profile, platform, or service architecture\
**Repository Path:** [`operations/standard-capacity-and-performance-management.md`](standard-capacity-and-performance-management.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This standard governs how capacity and performance are planned, measured, tested, and adjusted for services operated by the organisation. It aligns capacity to demand at acceptable cost and performance, while preserving the headroom required for failure scenarios and growth.

---

## Scope

This standard applies to:

1. Production and pre-production services with capacity-bound resources (compute, memory, storage, network, database connections, message queues, third-party API quotas, AI inference quotas).
2. Shared platform services whose capacity affects multiple consumers.
3. Customer-facing services whose performance affects customer experience.
4. Vendor-managed services where the organisation pays for capacity-shaped commitments.

It does not cover human workforce capacity (a separate governance topic).

---

## Section 1: principles

| Principle | Description |
| --- | --- |
| Demand-led | Capacity follows expected and observed demand, not arbitrary targets |
| Headroom for failure | Capacity preserves headroom for component failure and regional impairment |
| Cost-aware | Capacity is sized to a defined cost objective, not maximized |
| Elastic where possible | Elastic platforms preferred for variable demand |
| Measured | Capacity decisions are measured, not asserted |
| Coordinated | Capacity and performance are managed jointly with reliability, security, and finance |
| Continuous | Capacity is a continuous process, not a project event |

---

## Section 2: capacity classes

| Class | Description |
| --- | --- |
| Compute | CPU, memory, accelerator capacity |
| Storage | Block, object, database, archive capacity |
| Network | Bandwidth, packet rate, connection capacity |
| Concurrency | Connection pools, thread pools, worker pools |
| Quota | Cloud-provider quotas, third-party API quotas, AI inference quotas |
| Licence | Per-seat, per-core, or per-transaction licensed capacity |
| Logical | Identifier spaces, partition counts, shard counts |
| External | Inbound peering, CDN, edge capacity |

Each capacity class has a named owner and a defined measurement.

---

## Section 3: demand forecasting

| Activity | Description |
| --- | --- |
| Historical baseline | Demand history captured over windows long enough to surface seasonality |
| Growth projection | Modelled per product roadmap, customer pipeline, and regional expansion |
| Event-driven demand | Marketing events, product launches, regulatory deadlines forecast separately |
| Adverse scenarios | Worst-case demand modelled (success-disaster scenarios, regional failover load) |
| Forecast cadence | Updated at least quarterly; high-volatility services updated more frequently |
| Forecast accuracy | Forecast vs actual reviewed; persistent under-forecast or over-forecast triggers model review |

---

## Section 4: capacity planning

| Activity | Description |
| --- | --- |
| Capacity model | Per service; ties demand to consumption of each capacity class |
| Headroom target | Headroom percentage defined per class; accounts for failure and lead-time |
| Provisioning approach | Pre-provisioned, elastic, or hybrid; choice is justified |
| Lead-time map | Each capacity class has a documented procurement or provisioning lead-time |
| Procurement cadence | Procurement aligned to forecast and lead-time |
| Quota management | Provider quotas tracked; raises requested proactively |
| Decommissioning | Capacity not under use is identified and decommissioned per the financial management standard |

---

## Section 5: performance objectives and measurement

| Activity | Description |
| --- | --- |
| Performance SLOs | Latency, throughput, freshness, and quality targets per the service-level management standard |
| Performance baseline | Recorded; performance regression detection compares to baseline |
| Customer experience | Real-user monitoring and synthetic monitoring per the observability and telemetry standard |
| End-to-end measurement | Performance measured from the customer perspective, not only inside service boundaries |
| Dependency performance | Performance of critical dependencies measured separately |

---

## Section 6: performance testing

| Activity | Description |
| --- | --- |
| Load test | Service tested at expected production load; pre-release for material changes |
| Stress test | Service tested beyond expected load to find break-points |
| Soak test | Service tested for sustained load to surface leaks and accumulation defects |
| Spike test | Service tested under rapid demand changes |
| Failover test | Performance measured during failover scenarios |
| Test cadence | Major changes; quarterly for critical services; per release for high-volatility services |
| Test environment | Sized representative of production; data and traffic representative |
| Test isolation | Tests do not impact production; production traffic-replay is sanitised |

---

## Section 7: scaling

| Activity | Description |
| --- | --- |
| Horizontal scaling | Preferred where the architecture allows |
| Vertical scaling | Used where horizontal scaling is impractical |
| Auto-scaling | Configured to respond to demand within defined response times |
| Scale-down | Scale-down behaviour validated; cool-down windows tuned |
| Scaling limits | Upper and lower bounds documented; alerts fire on saturation against the upper bound |
| Pre-scaling | Predictable demand events pre-scaled; documented in the runbook |
| AI inference scaling | Per the AI inference cost governance standard |

---

## Section 8: capacity for resilience

| Activity | Description |
| --- | --- |
| Failure-mode capacity | Capacity preserved for component failure within a zone |
| Regional failover capacity | Capacity preserved for regional impairment per the business continuity strategy |
| Quota for failover | Provider quotas in the failover region match the workload they would absorb |
| Cold-standby vs warm-standby | Choice justified per the resilience strategy |
| Tested capacity | Failover capacity is tested, not assumed |

---

## Section 9: third-party and vendor capacity

| Activity | Description |
| --- | --- |
| Vendor commitments | Capacity commitments from vendors documented and tracked |
| Provider quota tracking | Provider quotas tracked centrally |
| Burst behaviour | Vendor burst behaviour validated; rate-limit handling tested |
| Concentration risk | Capacity concentration on a single vendor surfaced per the concentration risk register |
| Alternate paths | Alternate providers or paths identified for critical-capacity dependencies |

---

## Section 10: cost governance

| Activity | Description |
| --- | --- |
| Cost attribution | Capacity cost attributed to the consuming service and team |
| Cost telemetry | Cost telemetry available alongside performance telemetry |
| Cost vs performance | Cost-vs-performance trade-offs are explicit |
| Commit-based pricing | Reserved or committed pricing used where the demand is predictable |
| Idle resource detection | Idle and over-provisioned resources detected and reclaimed |
| Cost-anomaly alerting | Sudden cost growth alerted; routed to the cost owner |

---

## Section 11: governance

| Element | Description |
| --- | --- |
| Capacity council | Reviews forecast, headroom, performance regressions, and vendor capacity quarterly |
| Per-service capacity owner | Named per service; accountable for capacity decisions |
| Capacity register | Tracks all capacity classes, owners, current utilisation, headroom, and lead-times |
| Reporting | Capacity status reported to the operations leadership; material concerns escalated to the executive |
| Exceptions | Where headroom or lead-time targets are missed, an exception is logged with a remediation plan |

---

## Section 12: AI inference capacity

| Activity | Description |
| --- | --- |
| Provider quota | Provider quotas tracked; raise paths documented |
| Regional quota | Regional quotas tracked separately |
| Burst pattern | Burst behaviour validated; rate-limit retry strategies tested |
| Concurrency limits | Provider concurrency limits captured |
| Fine-tuning capacity | Where applicable, fine-tune capacity reserved or scheduled |
| Cost projection | Cost projection accompanies inference capacity planning per the AI inference cost governance standard |

---

## Operating expectations

1. Capacity is reviewed at least quarterly per service; high-volatility services reviewed more frequently.
2. Performance regressions are detected pre-release where possible; otherwise within the post-release monitoring window.
3. Performance SLOs are aligned with customer expectations and reviewed at least annually.
4. Capacity headroom is preserved per the failure-and-lead-time profile of each class.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ITIL 4 | Capacity and performance management | Service management |
| ISO/IEC 20000-1 | §8.6 Service management | Service management standard |
| FinOps Foundation | FinOps framework | Cloud financial operations |
| Google SRE | Capacity planning | Reliability practice |
| ISO/IEC 27001:2022 | A.8.6 Capacity management | Capacity control |
| NIST SP 800-53 Rev 5 | SC-5, CP-2 | Resource availability; contingency planning |

---

## Limitations

This standard is a CC BY-SA 4.0 baseline. Capacity practice is highly platform-specific; the standard expresses requirements rather than vendor-specific implementations. Adopting organisations confirm current provider quotas, tooling, and cost models with subject-matter experts.

---

**End of Document**
