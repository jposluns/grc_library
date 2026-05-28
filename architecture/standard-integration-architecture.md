# Integration Architecture Standard

**Document Title:** Integration Architecture Standard 
**Document Type:** Standard 
**Version:** 0.0.1 
**Date:** 2026-05-28 
**Owner:** Chief Technology Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`architecture/framework-enterprise-architecture.md`](framework-enterprise-architecture.md), [`architecture/standard-architecture-decision-records.md`](standard-architecture-decision-records.md), [`architecture/standard-api-design.md`](standard-api-design.md), [`architecture/standard-data-architecture.md`](standard-data-architecture.md), [`dev-security/standard-api-security.md`](../dev-security/standard-api-security.md), [`operations/standard-observability-and-telemetry.md`](../operations/standard-observability-and-telemetry.md), [`operations/standard-site-reliability-engineering.md`](../operations/standard-site-reliability-engineering.md) 
**Classification:** Public 
**Category:** Architecture 
**Review Frequency:** Annual and upon material change to integration platforms, transports, or patterns 
**Repository Path:** [`architecture/standard-integration-architecture.md`](standard-integration-architecture.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This standard governs the architecture of system-to-system integration: the patterns used, the transports selected, the contracts established, and the operational characteristics required. It complements the API design standard (which governs synchronous request-response contracts) and the data architecture standard (which governs data flow) by addressing the architectural choices that determine how systems communicate over time.

---

## Scope

This standard applies to:

1. Integration between internal services, products, and platforms.
2. Integration between the organisation and customers, suppliers, partners, and regulators.
3. Integration with AI providers and AI-bearing systems.
4. Bulk data movement between systems.
5. Event-driven communication.

It does not govern intra-process communication within a single deployable unit.

---

## Section 1: principles

| Principle | Description |
| --- | --- |
| Loose coupling | Producers do not know their consumers; consumers do not depend on producer internals |
| Contract-first | Integration is governed by an explicit contract before code is written |
| Asynchronous where natural | Long-lived, fan-out, and decoupled flows are asynchronous unless synchrony is required |
| Synchronous where required | Strong-consistency, query, and short-cycle interactions are synchronous |
| Idempotent | Operations are idempotent where retry is possible |
| Observable | Integrations are observable end-to-end |
| Backpressure-aware | Producers and consumers handle saturation gracefully |
| Schema-disciplined | Schemas are explicit, versioned, and reviewed |
| Resilient | Integration tolerates partial failure of either side |
| Secure | Integration is secured per the API security and data classification standards |

---

## Section 2: pattern selection

| Pattern | When appropriate |
| --- | --- |
| Synchronous request-response | Strong consistency required; the caller cannot proceed without the response |
| Asynchronous command | A command is dispatched; the caller does not need the response immediately |
| Event notification | A producer announces "this happened"; consumers react independently |
| Event-carried state transfer | An event carries enough state for the consumer to act without callbacks |
| Publish-subscribe | One-to-many fan-out |
| Choreography | Independent services react to events without central coordination |
| Orchestration | A workflow engine coordinates a multi-step flow |
| Batch | Periodic or scheduled bulk movement |
| Webhook | A producer notifies an external consumer via HTTP |
| File exchange | Document or dataset exchange where the consumer or producer requires it |
| Streaming | Continuous flow consumed in order |

The choice is recorded as an ADR for material integrations and informed by the integration class (Section 3).

---

## Section 3: integration classes

| Class | Description |
| --- | --- |
| Internal high-volume | Between organisational services in the same trust domain; volume is high; latency budget tight |
| Internal cross-domain | Between organisational services in different trust domains |
| Customer-facing | API or event published to customers |
| Supplier-consumed | The organisation consumes a supplier's API or events |
| Partner | Bidirectional; governed by a bilateral agreement |
| Public | Public APIs or feeds |
| Regulator | Mandatory regulatory submissions or feeds |
| AI provider | Outbound to AI inference or training APIs |
| Legacy | Integration with legacy or end-of-life systems with constrained options |

---

## Section 4: contracts

| Element | Description |
| --- | --- |
| Contract first | A documented contract precedes implementation |
| Schema | Schema language is documented per the API design standard |
| Versioning | Compatibility expectations are explicit |
| Ownership | Each contract has an owner |
| Consumer registration | Internal consumers are registered against producer contracts |
| Test doubles | Producers provide test doubles or sandbox endpoints where the consumer surface justifies |
| Deprecation | Deprecation notice and sunset windows are published |
| Change review | Material contract changes are reviewed per the architecture review procedure |

---

## Section 5: event-driven integration

| Element | Description |
| --- | --- |
| Event schema | AsyncAPI or equivalent; registered |
| Event metadata | Standard envelope fields (event identifier, type, time, source, tenant, correlation, causation) |
| Schema evolution | Forward, backward, or full compatibility per the topic |
| Retention | Topic retention is deliberate; replay semantics documented |
| Ordering | Ordering guarantees explicit (per-partition or global) |
| Dead-letter handling | Documented; tested |
| Idempotent consumers | Consumers handle redelivery |
| Tenant scoping | Multi-tenant event streams scope events explicitly |
| Sensitive data | Sensitive data not carried in events without classification controls |
| Outbox pattern | Used to coordinate state change with event publication where consistency matters |

---

## Section 6: synchronous integration

| Element | Description |
| --- | --- |
| Timeout | Explicit, finite, and tuned |
| Retry | Bounded; backoff applied; idempotency keys used for non-idempotent operations |
| Circuit breaker | Used to prevent cascade failure |
| Bulkhead | Resources isolated to prevent one consumer starving another |
| Rate limit | Producers protect themselves; consumers respect rate limits |
| Caching | Used deliberately; invalidation strategy defined |
| Authentication | Per the API security standard |

---

## Section 7: batch and file exchange

| Element | Description |
| --- | --- |
| Schedule | Documented; tolerant to source variability |
| Encoding | Documented (CSV, Parquet, Avro, JSON Lines, etc.) |
| Validation | Validation rules at producer and consumer |
| Integrity | Checksums or signatures verified |
| Encryption | At-rest and in-transit encryption per the data classification |
| Idempotency | Re-processing is safe |
| Reconciliation | Reconciliation between source and destination is performed |
| Late and out-of-order arrival | Handled deliberately |

---

## Section 8: webhooks

| Element | Description |
| --- | --- |
| Subscription model | Documented |
| Delivery semantics | At-least-once with idempotency expected of the consumer |
| Retry policy | Bounded; exponential backoff |
| Signature | Webhook payloads signed; signature verified by the consumer |
| Replay protection | Per the API security standard |
| Consumer health | Stale subscriptions detected and disabled |
| Sensitive data | Sensitive content excluded; data fetched out-of-band via authenticated request where required |

---

## Section 9: integration with AI providers

| Concern | Practice |
| --- | --- |
| Provider call | Synchronous request-response is the default; streaming where the use case requires |
| Tool invocations | Agentic tool invocations governed per the AI access and agent permissions standard |
| Retry | Provider-side rate limits handled; per the AI inference cost governance standard |
| Cost | Cost telemetry per the AI inference cost governance standard |
| Audit | Per the AI logging standard |
| Provider concentration | Concentration considered; alternates identified |
| Failure path | Provider failure has a graceful fallback or controlled degradation |
| Sensitive content | Sensitive content not sent without provider's data-handling commitments per the AI vendor security questionnaire |

---

## Section 10: observability

| Element | Description |
| --- | --- |
| End-to-end tracing | Trace identifiers propagated across integration boundaries |
| Correlation identifiers | Stable correlation identifiers across event flows |
| Topic and queue metrics | Lag, throughput, dead-letter rate, processing time |
| API metrics | Per the API security standard observability requirements |
| Alerting | Per the observability and telemetry standard |
| Cost telemetry | Integration cost tracked where material |

---

## Section 11: reliability patterns

| Pattern | Description |
| --- | --- |
| Retry | Bounded, with backoff and idempotency expectations |
| Circuit breaker | Fail fast under sustained downstream failure |
| Bulkhead | Isolate resources by consumer or by operation class |
| Backpressure | Producers receive signals; consumers shed load gracefully |
| Throttling | Rate limit at the producer or gateway |
| Dead-letter queue | Failed messages parked for inspection |
| Saga | Compensating actions coordinate distributed state change |
| Outbox | Reliable event publication tied to state change |
| Inbox | Idempotent processing of inbound events |

---

## Section 12: security overlay

| Element | Description |
| --- | --- |
| Authentication | Per the API security standard |
| Authorization | Per the API security standard |
| Encryption in transit | Per the API security standard |
| Encryption at rest in queues and topics | Per the encryption policy |
| Tenant isolation | Multi-tenant integrations isolate tenants in transport and storage |
| Sensitive content | Sensitive content is classified, controlled, and minimized on integration paths |
| Webhook signing | Per Section 8 |
| Provider authentication | Outbound provider integrations authenticate per the supplier security and privacy assurance standard |

---

## Section 13: governance

| Element | Description |
| --- | --- |
| Catalogue | Integration catalogue tracks producer, consumers, contract, status, owner |
| Schema registry | Centrally registered for shared integrations |
| Review | Material integrations reviewed per the architecture review procedure |
| Pattern endorsement | Patterns endorsed by the architecture council; new patterns reviewed before adoption |
| Lifecycle | Integrations have an owner, a status, a review cadence, and a sunset path |
| Anti-pattern register | Banned patterns recorded with rationale |

---

## Section 14: anti-patterns

| Anti-pattern | Why it harms |
| --- | --- |
| Direct database access between services | Couples consumers to internal schema; impedes change |
| Shared mutable state | Hidden coupling; concurrent modification hazards |
| Synchronous chain calls | Latency compounds; one failure cascades |
| Custom transport per integration | Operational and observability burden |
| Implicit retry without idempotency | Duplicate-effect risk; reconciliation cost |
| Webhook without signature | Vulnerable to forgery |
| Sensitive content in event payload without controls | Privacy and security risk |
| Unbounded fan-out | Producers cannot reason about consumer impact |
| Ungoverned point-to-point integrations | Topology becomes unmanageable; orphan integrations accrete |

---

## Operating expectations

1. Material integrations are reviewed and recorded per the architecture review procedure and the ADR standard.
2. The integration catalogue is current; orphan integrations are not allowed to accrete.
3. Integrations are observable end-to-end; dark integrations are an incident waiting to happen.
4. Schema and contract changes follow the API design and data architecture standards.
5. AI provider integration follows the AI access and agent permissions standard and the AI inference cost governance standard.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| Enterprise Integration Patterns (Hohpe and Woolf) | Reference pattern catalogue | Pattern baseline |
| AsyncAPI Initiative | AsyncAPI Specification | Event schema |
| CloudEvents | CNCF specification | Event envelope |
| OpenAPI Initiative | OpenAPI Specification | Synchronous schema |
| Enterprise Service Bus and microservices reference architectures | Vendor-neutral references | Integration topology |
| ISO/IEC 27001:2022 | A.5.14, A.8.20 to A.8.21 | Information transfer; network security cross-walk |
| OWASP API Security Top 10 | API risk taxonomy | Cross-walk to the API security standard |
| NIST CSF 2.0 | Govern, Identify, Protect | Risk integration |

---

## Limitations

This standard is a public-domain baseline. Integration platform choices and per-pattern implementation details are organisation-specific. The standard expresses outcomes and pattern selection criteria, not specific commercial products.

---

**End of Document**
