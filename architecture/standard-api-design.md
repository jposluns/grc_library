# API Design Standard

**Document Title:** API Design Standard 
**Document Type:** Standard 
**Version:** 0.0.1 
**Date:** 2026-05-28 
**Owner:** Chief Technology Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`architecture/framework-enterprise-architecture.md`](framework-enterprise-architecture.md), [`architecture/standard-architecture-decision-records.md`](standard-architecture-decision-records.md), [`architecture/standard-integration-architecture.md`](standard-integration-architecture.md), [`architecture/standard-data-architecture.md`](standard-data-architecture.md), [`dev-security/standard-api-security.md`](../dev-security/standard-api-security.md), [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md) 
**Classification:** Public 
**Category:** Architecture 
**Review Frequency:** Annual and upon material change to API tooling, transport, or interface conventions 
**Repository Path:** [`architecture/standard-api-design.md`](standard-api-design.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This standard governs the design of application programming interfaces (APIs) produced by the organisation. It complements the API security standard (which governs the security controls on APIs) by addressing the design choices that determine usability, longevity, and correctness.

---

## Scope

This standard applies to:

1. APIs exposed externally to customers, partners, or the public.
2. APIs exposed internally between products, services, or platforms.
3. APIs exposed between the organisation and its suppliers.
4. APIs exposed by AI-bearing systems (including agent-callable tools).
5. Asynchronous interfaces (event streams, webhooks) where a contract is offered to consumers.

It does not govern private interfaces wholly within a single deployable unit.

---

## Section 1: principles

| Principle | Description |
| --- | --- |
| Consumer-first | The API exists for its consumers; their experience is the design's primary measure |
| Predictable | Like things look like one another; surprise is a design defect |
| Honest | The API does what its contract says; it does not hide failure or surprise the consumer |
| Forward-compatible | Additive change does not break existing consumers |
| Versioned | Breaking change is announced, versioned, and communicated |
| Documented | A documented API is a usable API; tooling generates and verifies documentation |
| Secure | Security is a design input, not a retrofit; per the API security standard |
| Discoverable | A consumer can find the API, understand it, and try it without negotiating |
| Tested | The contract is exercised in tests |
| Bounded | The API does one thing; it does not become an everything-bucket |

---

## Section 2: style choice

| Style | When appropriate |
| --- | --- |
| REST | The default for resource-oriented synchronous interfaces |
| RPC (e.g. gRPC) | When low-latency strongly-typed inter-service calls are warranted |
| GraphQL | When consumers benefit from a flexible query interface and the operational cost is justified |
| Event-driven | When the interaction is naturally asynchronous; per the integration architecture standard |
| Webhook | When the producer notifies the consumer of events |
| Bulk file | When the volume or shape demands batch processing |

The choice is recorded as an ADR for material APIs.

---

## Section 3: REST design conventions

| Element | Convention |
| --- | --- |
| Resource model | Resources represent nouns; verbs are HTTP methods |
| URI structure | Consistent across the organisation; documented in a URI conventions guide |
| HTTP methods | GET (safe, idempotent), PUT (idempotent), POST (non-idempotent), DELETE (idempotent), PATCH (with documented semantics) |
| Status codes | 2xx for success, 4xx for client error, 5xx for server error; specific codes used consistently |
| Content negotiation | JSON is the default; alternatives via Accept header |
| Pagination | Cursor-based for large collections preferred over offset |
| Filtering and sorting | Documented query-parameter conventions |
| Partial response | Field-selection where the cost-benefit profile justifies |
| Caching | Cache headers used deliberately |
| Compression | Supported where the payload size justifies |
| HATEOAS | Optional; if used, applied consistently |

---

## Section 4: contract and schema

| Element | Convention |
| --- | --- |
| Schema language | OpenAPI for REST; Protobuf for RPC; JSON Schema for events; documented choice per API |
| Source of truth | The schema is the source of truth; documentation is generated |
| Schema review | Schema changes go through code review |
| Schema testing | Contract tests exercise the schema |
| Generated clients and servers | Generated where the consumer surface justifies |
| Schema registry | Centrally registered for shared APIs |

---

## Section 5: identifiers

| Element | Convention |
| --- | --- |
| Resource identifiers | Opaque strings; no business semantics in the identifier |
| Format | Documented format (e.g. ULID, UUID, KSUID, custom) is consistent within an API |
| Stable | Identifiers do not change; an identifier is a permanent reference |
| Avoid integer surrogates | Sequential integers leak volume and ordering |
| Tenant scoping | Where the API is multi-tenant, identifier scoping is explicit |
| Privacy considerations | Identifiers do not embed personal data |
| Hierarchical paths | Hierarchical identifiers are used deliberately; consider future re-parenting |

---

## Section 6: errors

| Element | Convention |
| --- | --- |
| Error model | Consistent across the organisation; documented |
| Error code | Stable, machine-readable error code separate from human-readable message |
| Error message | Human-readable; safe for surfacing to end users where appropriate |
| Field-level errors | Where multiple field-level errors apply, returned as a collection |
| Idempotency-key handling | Documented behaviour for duplicate requests |
| Retry semantics | Retryable vs not-retryable indicated |
| Rate limit responses | 429 with documented headers per the API security standard |
| Problem-details format | RFC 7807 problem-details JSON format preferred |

---

## Section 7: versioning

| Element | Convention |
| --- | --- |
| Additive change | Adding optional fields, new endpoints, new optional query parameters is not a breaking change |
| Breaking change | Removing or renaming fields, changing required-ness, changing semantics, changing error codes is a breaking change |
| Versioning approach | URI versioning (e.g. `/v2/`) preferred for major versions; header versioning where the deployment platform constrains |
| Version coexistence | Major versions coexist for a documented window |
| Deprecation | Deprecation announced via response headers and via consumer communication |
| Sunset | Sunset date communicated well in advance; per the API security standard expectations |
| Schema evolution | Documented schema-evolution rules for events (forward, backward, full compatibility) |

---

## Section 8: time, units, and locale

| Element | Convention |
| --- | --- |
| Timestamps | ISO 8601 with timezone offset; UTC is the default |
| Duration | ISO 8601 duration format |
| Monetary amounts | Decimal-safe representation with currency; not floating point |
| Units | Explicit (e.g. include unit suffixes or separate unit field) |
| Locale | Locale-sensitive output identified; defaults documented |
| Internationalisation | Strings intended for end-user display are localisable |

---

## Section 9: documentation

| Element | Convention |
| --- | --- |
| Reference documentation | Generated from the schema |
| Conceptual documentation | Hand-written; explains the model, the lifecycle, and the choices |
| Quickstart | A worked example consumers can follow |
| Authentication and authorisation | Documented per the API security standard |
| Rate limits and quotas | Documented |
| Changelog | Maintained per API |
| Migration guides | Provided for breaking changes |
| Examples | Realistic examples in multiple languages where the consumer surface justifies |
| Test environment | A sandbox or test environment available where consumer trust requires |

---

## Section 10: pagination, filtering, and search

| Element | Convention |
| --- | --- |
| Pagination | Cursor-based preferred; opaque cursor; consistent across the organisation |
| Result ordering | Documented and stable; ties broken deterministically |
| Filtering | Documented conventions; complex filtering may warrant a query endpoint |
| Search | When the data warrants it, a dedicated search endpoint with documented relevance and recall behaviour |
| Aggregation | Documented; large aggregations have safeguards |

---

## Section 11: idempotency and consistency

| Element | Convention |
| --- | --- |
| Idempotency keys | Client-supplied idempotency keys for non-idempotent operations |
| Conditional requests | Optimistic concurrency via ETag / If-Match where applicable |
| Eventual consistency | Documented; consumers warned where reads may lag writes |
| Read-your-writes | Where the architecture supports it, the API guarantees read-your-writes |
| Bulk operations | Semantics documented for partial success |

---

## Section 12: AI and agent-callable APIs

| Concern | Convention |
| --- | --- |
| Tool definitions | Aligned with the AI access and agent permissions standard; tool descriptions are durable, accurate, and minimal |
| Capability scopes | Capability scopes are explicit and least-privilege |
| Confirmation modes | Confirmation modes are explicit per the AI access standard |
| Idempotency | Agent-driven retry is anticipated; idempotency keys are a default |
| Audit | Tool invocations are logged per the AI access standard |
| Cost telemetry | Cost telemetry per the AI inference cost governance standard |
| Output validation | The agent's invocation is validated; the API does not assume the caller has perfect intent |

---

## Section 13: customer-facing APIs

| Concern | Convention |
| --- | --- |
| Onboarding | Self-service onboarding where appropriate |
| Sandbox | A sandbox environment for development |
| Support | Documented support channel; documented SLOs |
| Status communication | A status page; subscribable notifications |
| Backward-compatibility commitment | A documented commitment to consumers |
| Pricing model | Where the API is monetised, the pricing model is documented and stable |
| Terms | Terms of service documented |
| Acceptable use | An acceptable use policy is published |

---

## Section 14: governance

| Element | Description |
| --- | --- |
| API design review | New material APIs reviewed per the architecture review procedure |
| Style council | A small group that maintains the conventions and rules on edge cases |
| Linter | API definitions are linted; lint findings are gates |
| Schema registry | Shared APIs are registered |
| Catalogue | The API catalogue lists all APIs with owner, status, version, and consumers |
| Sunset register | Sunset APIs are tracked through the sunset path |
| Deprecation reporting | Deprecation usage is tracked; consumer-by-consumer where feasible |

---

## Operating expectations

1. Material new APIs are reviewed for design before commitment.
2. The schema is the source of truth; documentation is generated.
3. Breaking changes are deliberate; their announcement and sunset windows are honoured.
4. The API catalogue is current; orphan APIs are not allowed to accrete.
5. Customer-facing APIs maintain a backward-compatibility commitment that the organisation actually honours.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| OpenAPI Initiative | OpenAPI Specification | REST schema |
| AsyncAPI Initiative | AsyncAPI Specification | Event schema |
| gRPC and Protobuf | RPC schema | RPC schema |
| GraphQL Foundation | GraphQL Specification | Graph schema |
| RFC 7807 | Problem Details for HTTP APIs | Error model |
| Google API Improvement Proposals (AIPs) | Vendor-neutral REST conventions | Design guidance |
| Microsoft REST API Guidelines | Vendor-neutral REST conventions | Design guidance |
| ISO/IEC 27001:2022 | A.8.26 Application security requirements | Information security cross-walk |
| OWASP API Security Top 10 | API risk taxonomy | Cross-walk to the API security standard |

---

## Limitations

This standard is a public-domain baseline. The specific URI conventions, error model, schema registry, and tooling are organisation-specific. The standard expresses design principles and outcomes, not a single canonical layout.

---

**End of Document**
