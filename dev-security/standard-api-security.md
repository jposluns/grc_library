# API Security Standard

**Document Title:** API Security Standard\
**Document Type:** Standard\
**Version:** 0.0.3\
**Date:** 2026-06-22\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`dev-security/policy-secure-development-and-engineering.md`](policy-secure-development-and-engineering.md), [`dev-security/standard-developer-security-requirements.md`](standard-developer-security-requirements.md), [`dev-security/standard-devops-security-requirements.md`](standard-devops-security-requirements.md), [`dev-security/standard-software-composition-analysis.md`](standard-software-composition-analysis.md), [`dev-security/standard-quality-assurance-and-testing.md`](standard-quality-assurance-and-testing.md), [`security/policy-identity-and-access-management.md`](../security/policy-identity-and-access-management.md), [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`security/standard-data-loss-prevention.md`](../security/standard-data-loss-prevention.md), [`security/framework-zero-trust-architecture.md`](../security/framework-zero-trust-architecture.md), [`ai/standard-ai-access-and-agent-permissions.md`](../ai/standard-ai-access-and-agent-permissions.md)\
**Classification:** Public\
**Category:** Developer Security\
**Review Frequency:** Annual and upon material change to API portfolio, threat-pattern, or platform-native posture\
**Repository Path:** [`dev-security/standard-api-security.md`](standard-api-security.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This standard defines the minimum security controls for every API the organisation produces, exposes, or consumes. It covers REST, GraphQL, gRPC, WebSocket, and event-driven APIs. It applies whether the API is internal, partner-facing, or public.

---

## Scope

This standard applies to every API designed, implemented, deployed, or consumed by the organisation. It does not duplicate the underlying developer security or DevOps security standards; it overlays API-specific requirements on the engineering baseline.

It does not cover legacy SOAP integrations operating under a separate maintenance regime; those follow a documented exception path until retirement.

### Relationship to the API design standard and approval sequence

This standard (CISO-owned) covers API security controls. The architecture API design standard ([`architecture/standard-api-design.md`](../architecture/standard-api-design.md)) (CTO-owned) covers design choices: style (REST/RPC/GraphQL), versioning, identifiers, error model, schema, longevity.

For material new APIs the approval sequence is:

1. **Design choice gate** - the architecture review forum reviews style, schema, and contract per the API design standard. The proposer brings a draft contract and the rationale for the style choice.
2. **Threat-model gate** - the security architecture forum (or the secure code review path for routine APIs) reviews the threat model and the security controls per this standard. Inputs include the contract from step 1.
3. **Implementation** - proceeds once both gates pass.

Where step 2 surfaces a finding that requires reshaping the contract (for example, an identifier-design change to avoid enumeration), the design returns to step 1. The conditional endorsement and request-revision dispositions in the architecture review procedure handle this loop.

For routine changes within an existing API contract, the security controls in this standard apply through the secure code review procedure; the architecture review forum is not engaged.

---

## Section 1: lifecycle gates

| Stage | Required gate |
| --- | --- |
| Design | Threat model produced; data classification of inputs and outputs; lawful basis confirmed where personal data flows; ADM register entry if the API drives an automated decision |
| API specification | OpenAPI, GraphQL schema, or Protobuf definition under version control; security schemes documented; deprecation policy stated |
| Build | Static analysis runs include API-specific rules; secret detection runs |
| Test | API-specific security tests including authentication, authorisation, input fuzzing, business-logic abuse |
| Pre-deployment | Gateway configuration review; rate-limit and quota review; observability verified |
| Production | Continuous monitoring; anomaly detection; per-API SLO including error rate and latency |
| Deprecation | Public notice period; sunset header in production; migration path documented |

---

## Section 2: authentication

| Control area | Requirement |
| --- | --- |
| No anonymous APIs | Every API requires authentication; anonymous-access exceptions require CISO approval and are public-only by data classification |
| Federated identity | Human-driven APIs authenticate via the enterprise identity provider with OAuth 2.0 / OpenID Connect |
| Service-to-service | mTLS for service-to-service where the network allows; workload identity where the platform supports it |
| Token formats | JWT or platform-native; encrypted JWTs (JWE) where the token transits networks the organisation does not control |
| Token validation | Signature, issuer, audience, expiry, and nonce validated; algorithm whitelist enforced; `none` algorithm rejected |
| Refresh tokens | Bound to client and device; rotated on use; revocable centrally |
| API keys | Permitted only for low-trust scenarios; rate-limited; rotated; bound to source |
| MFA propagation | High-sensitivity API operations require step-up authentication signalled through the access token claims |

---

## Section 3: authorisation

| Control area | Requirement |
| --- | --- |
| Least privilege | Each operation declares the scope or permission it requires; the gateway and the application both enforce |
| Object-level authorisation | Per-object authorisation checks on every request that accesses or modifies a resource (mitigates BOLA / IDOR) |
| Function-level authorisation | Sensitive operations checked against the caller's role and the operation's required permission |
| Attribute-based access | Where the use case warrants, ABAC policy evaluated alongside role-based checks |
| Tenant isolation | Multi-tenant APIs enforce tenant boundaries server-side; client-supplied tenant identifiers are not trusted |
| Privilege escalation prevention | The API rejects operations that would assign privileges higher than the caller's |
| Sensitive operation confirmation | High-impact actions (payments, deletion, configuration change) require step-up or out-of-band confirmation per the data classification |

---

## Section 4: input validation and output handling

| Control area | Requirement |
| --- | --- |
| Schema validation | Every request validated against the published schema; unknown fields rejected by default |
| Type and range validation | All numeric, string, and enumerated values validated against expected types and ranges |
| Mass-assignment prevention | The API binds only explicitly-allowed fields; bulk binding from request body to model object prohibited |
| Injection prevention | Parameterised queries for SQL and NoSQL; sanitisation for shell, LDAP, XPath, header, log, and template contexts |
| Output minimisation | Responses include only fields necessary for the caller's role; sensitive fields suppressed for lower-trust callers |
| Content type enforcement | Content-Type header validated; mismatches rejected |
| Body size limits | Per-endpoint maximum body size; oversize requests rejected before parsing |
| File uploads | File type, size, and scanning per the data classification; uploads stored in dedicated storage; never executed |

---

## Section 5: transport and message security

| Control area | Requirement |
| --- | --- |
| TLS | TLS 1.3 or stronger (aligned to [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md) §1 (Encryption standards) canonical mandate); HSTS for browser-driven APIs |
| Cipher suite | Strong cipher suites only; deprecated suites rejected |
| Certificate management | Per the cryptographic key lifecycle framework |
| mTLS | For service-to-service and high-sensitivity partner integrations |
| WebSocket | Same authentication and authorisation as the equivalent REST endpoint; ping-pong heartbeats with idle timeout |
| Message integrity | Where the API supports signed message payloads, signatures are validated; replay attacks are mitigated via nonce or timestamp |

---

## Section 6: rate limiting, quotas, and abuse prevention

| Control area | Requirement |
| --- | --- |
| Per-client rate limit | Enforced at the gateway; tuned to the API's expected pattern |
| Per-operation rate limit | More restrictive on sensitive or expensive operations |
| Quotas | Per-client daily and monthly quotas where appropriate |
| Bot and abuse detection | Behavioural detection where the API faces public traffic |
| Cost-bound operations | AI-backed or expensive operations have a cost ceiling per session enforced |
| Auto-mitigation | Sustained abuse triggers automated mitigation: IP block, token revocation, account isolation; mitigation logged and reviewed |
| Distributed-denial-of-service protection | Edge protection in place for public APIs |

---

## Section 7: logging, monitoring, and observability

| Control area | Requirement |
| --- | --- |
| Request and response logging | Logged at a level appropriate to the data classification; sensitive content masked |
| Authentication and authorisation events | Logged: success, failure, step-up, denial reasons |
| Errors | Structured error logs; stack traces never returned to clients in production |
| Correlation | Correlation IDs propagated across calls |
| SIEM integration | Logs forwarded per the logging standard |
| Anomaly detection | Behavioural baselines per API; sudden volume, latency, error-rate, or distinct-caller changes alerted |
| Per-API SLO | Availability, error rate, and latency SLOs published and monitored |

---

## Section 8: API gateway and management

| Control area | Requirement |
| --- | --- |
| Gateway-fronted | Production APIs are fronted by an API gateway with policy enforcement |
| Catalogue | Every API registered in the API catalogue with owner role, data classification, lifecycle stage, dependent services |
| Versioning | Semantic versioning of public APIs; deprecation through sunset headers; version EOL documented |
| Documentation | Up-to-date documentation generated from the schema; security scheme documented |
| Discoverability | Internal discoverability through the catalogue; public discoverability limited per the publishing policy |
| Developer portal | Where the organisation operates a developer portal, the portal enforces the same authentication and authorisation as the runtime |

---

## Section 9: third-party API consumption

| Control area | Requirement |
| --- | --- |
| Third-party API inventory | All consumed third-party APIs inventoried with owner, supplier, scope, data exchanged |
| Credential storage | Third-party credentials in the secrets management service; per-environment isolation |
| Resilience | Timeouts, retries, and circuit breakers configured per the resilience programme |
| Data minimisation | Only the data necessary for the use case is sent to the third party |
| Personal data handling | DPIA and ROPA updated where personal data is sent to a third-party API |
| Cost monitoring | Per the AI inference cost governance standard where the third party is an AI provider |

---

## Section 10: AI-exposed APIs

Where an API is exposed to AI agents (organisation-internal or third-party):

| Control area | Requirement |
| --- | --- |
| Documentation for agents | OpenAPI schema annotated with semantic descriptions consumable by AI agents |
| Capability classification | API operations classified per the agent-permissions standard (Read-only Low, Write Low, Write Sensitive, Destructive) |
| Confirmation mode | Destructive or Sensitive operations require human-in-the-loop confirmation per the agent-permissions standard |
| Rate and chain-length limits | Aligned with the agent-permissions standard; agent caller identity propagated |
| Indirect prompt injection mitigations | API responses that may flow into a model prompt are delimited and identified as untrusted where the caller is an agent |

---

## Section 11: GraphQL-specific controls

| Control area | Requirement |
| --- | --- |
| Schema introspection | Disabled in production for public-facing endpoints |
| Query depth limit | Enforced |
| Query complexity scoring | Enforced; expensive queries rejected |
| Persisted queries | Preferred for public clients; ad-hoc queries restricted |
| Batching limits | Per-batch maximum enforced |
| Field-level authorisation | Per the authorisation requirements above; per-field checks where roles differ |

---

## Section 12: event-driven and webhook APIs

| Control area | Requirement |
| --- | --- |
| Webhook signing | Webhooks signed with a shared secret or asymmetric key; recipients validate signatures |
| Replay prevention | Timestamp plus nonce; recipients enforce freshness |
| Idempotency | Receivers handle duplicate delivery without side effects |
| Authentication on subscribe | Subscriptions to event streams authenticated and authorised |
| Topic isolation | Multi-tenant event systems enforce per-tenant topic isolation |
| Dead-letter handling | Failed messages routed to a dead-letter queue with monitoring |

---

## Operating expectations

1. Every production API has an owning role accountable for posture against this standard.
2. The API catalogue is treated as a production artefact; drift between the catalogue and deployed reality is a defect.
3. Annual API security review covers the catalogue and a sampled subset of production APIs.
4. Pen tests (per the penetration testing standard) include API-specific scenarios annually for Tier 1 APIs.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| OWASP API Security Top 10 (2023) | API1 to API10 | Authoritative API threat taxonomy |
| OWASP ASVS v5 | Multiple sections | Application security baseline |
| NIST SP 800-204 series | Microservices security, service mesh, DevSecOps | US baseline |
| ISO/IEC 27001:2022 | A.5.10, A.5.14, A.8.21, A.8.23 to A.8.28 | Information transfer, network security, secure development |
| NIST SP 800-95 | Guide to Secure Web Services | Web services foundation |
| RFC 6749, 7519, 8725, 9068 | OAuth 2.0, JWT, JWT BCP, OAuth 2.0 access tokens | Token standards |
| OpenID Connect Core 1.0 | OIDF | Identity layer |
| FAPI 2.0 | OIDF | Financial-grade API profile |
| CSA Cloud Controls Matrix v5 | AIS, IAM, IVS, LOG | Cross-walk |

---

## Limitations

This standard is a CC BY-SA 4.0 baseline. Specific API platform configurations vary; the standard expresses control requirements rather than vendor-specific settings. Highly-regulated APIs (open banking, healthcare interoperability, electronic identity) follow sector-specific profiles in addition to this standard.

---

**End of Document**
