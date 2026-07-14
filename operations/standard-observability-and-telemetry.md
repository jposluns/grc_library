# Observability and Telemetry Standard

**Document Title:** Observability and Telemetry Standard\
**Document Type:** Standard\
**Version:** 0.0.6\
**Date:** 2026-07-14\
**Owner:** Chief Information Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`operations/framework-it-service-management.md`](framework-it-service-management.md), [`operations/standard-service-level-management.md`](standard-service-level-management.md), [`operations/register-it-operations-kpis.md`](register-it-operations-kpis.md), [`operations/procedure-security-monitoring-and-alert-management.md`](procedure-security-monitoring-and-alert-management.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`ai/procedure-ai-evaluation.md`](../ai/procedure-ai-evaluation.md), [`dev-security/standard-devops-security-requirements.md`](../dev-security/standard-devops-security-requirements.md)\
**Classification:** Public\
**Category:** IT Operations\
**Review Frequency:** Annual and upon material change to platform stack, telemetry tooling, or service architecture\
**Repository Path:** [`operations/standard-observability-and-telemetry.md`](standard-observability-and-telemetry.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines minimum observability and telemetry requirements for services operated by the organization. It complements the security logging and monitoring standard (which focuses on security-relevant events) and the [`AI evaluation procedure`](../ai/procedure-ai-evaluation.md) (which focuses on model behaviour) by covering operational health, performance, reliability, and customer-experience signals.

---

## 2. Scope

This standard applies to:

1. Production and pre-production services operated by the organization.
2. Customer-facing services and customer-impacting internal services.
3. Background and batch processing systems that produce a customer or business outcome.
4. Infrastructure components whose failure affects service health.
5. Vendor-managed services whose health affects organizational outcomes.

It does not cover individual workstation telemetry (governed by the endpoint hardening standard) or experimental sandboxes that produce no organizational outcome.

### 2.1 Scope boundary with the security logging and monitoring standard

This standard governs operational health signals (metrics, traces, logs of operational events, real-user monitoring, synthetic checks). Security-relevant logging, monitoring, and SIEM operations are governed by [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md). See that standard's scope-boundary table for the per-event-class routing rule. The short version: security-relevant events go to the SIEM, operational signals go to the observability platform, and dual-purpose events are emitted to both with shared trace identifiers.

---

## 3. Principles

| Principle | Description |
| --- | --- |
| Outcomes over outputs | Telemetry quality is measured by the questions it can answer, not the volume it produces |
| Three telemetry pillars | Metrics, logs, and traces are jointly designed and correlated |
| Customer-experience first | Service quality is measured from the customer's perspective; internal indicators are secondary |
| Service ownership | The team that operates a service owns its telemetry |
| Standard schemas | Common schemas across services to enable cross-service queries |
| Retention by purpose | Retention is determined by the question the data answers, not by default |
| Privacy by design | Telemetry minimization; sensitive data not captured by default |
| Cost-aware | Telemetry cost is reviewed alongside engineering and infrastructure cost |

---

## 4. Service-level signals

Every customer-facing service publishes:

| Signal | Description |
| --- | --- |
| Availability | The fraction of valid attempts that succeed |
| Latency | A percentile distribution (p50, p95, p99, p999 where appropriate) |
| Throughput | Requests per second or items per second |
| Quality | A service-specific measure of correctness (e.g. error rate, business-event success) |
| Saturation | How loaded the system is relative to its capacity |
| Freshness | For data services, how recent the data being served is |

Service-level objectives (SLOs) are defined per the service-level management standard. Telemetry is the basis of SLO measurement.

---

## 5. Metrics

| Control area | Requirement |
| --- | --- |
| Naming | Metric names follow a documented convention; namespaced by service |
| Cardinality | High-cardinality dimensions are explicit decisions; runaway-cardinality detection in place |
| Standard tags | Service, environment, region, version, team owner tags on all metrics |
| Granularity | Resolution appropriate to the question; not finer than necessary |
| Aggregation | Aggregation rules documented; histograms preferred over raw averages for latency |
| Counter integrity | Counter increments are durable; restarts do not produce data loss |
| Storage | Stored in a metric backend that supports the required retention and query latency |
| Retention | Resolution-aware retention (full-resolution short term; downsampled long term) |

---

## 6. Logs

| Control area | Requirement |
| --- | --- |
| Structured logs | Logs are structured (JSON or equivalent); not free-form |
| Required fields | Timestamp, level, service, environment, region, version, trace identifier, request identifier where applicable |
| Levels | A documented level hierarchy (debug, info, warn, error, fatal) consistent across services |
| Sampling | High-volume info logs sampled where the cost-benefit profile justifies; error logs not sampled |
| Sensitive data | Personal data, secrets, and credentials excluded; field-level redaction patterns documented |
| Transport | Reliable transport to the log destination; backpressure handled |
| Storage | Logs stored in a queryable backend; security logs route additionally per the security logging standard |
| Retention | Per the records retention schedule and the logging standard |

---

## 7. Distributed tracing

| Control area | Requirement |
| --- | --- |
| Context propagation | W3C Trace Context or equivalent propagated across service boundaries |
| Span coverage | Inbound requests, outbound calls, and significant internal operations are spans |
| Sampling | Head-based, tail-based, or hybrid sampling; sampling decisions are propagated |
| Trace storage | Traces stored in a backend that supports searches by attributes, time, latency, and error state |
| Correlation | Trace identifier is also captured in logs and metrics tags where feasible |
| Sensitive data in span attributes | Treated like logs; sensitive payloads excluded |

---

## 8. Error and exception telemetry

| Control area | Requirement |
| --- | --- |
| Exception capture | Unhandled and significant handled exceptions captured with stack trace and context |
| Grouping | Exceptions are grouped by signature; rates and trends visible |
| Suppression | Known-noise patterns suppressed with explicit documentation |
| Ownership | Each exception group has an owning team |
| Backpressure on noisy errors | Spike protection prevents an error storm from impairing telemetry |

---

## 9. Events

| Control area | Requirement |
| --- | --- |
| Business events | Significant business outcomes published as events with a stable schema |
| Change events | Deployments, configuration changes, feature flag flips, and infrastructure changes published as events |
| Annotation | Change events are surfaced on dashboards to support root-cause analysis |
| Replay | Critical event streams support replay where the architecture allows |

---

## 10. Synthetic monitoring and real-user monitoring

| Control area | Requirement |
| --- | --- |
| Synthetic checks | Critical customer journeys checked from multiple geographies on a defined cadence |
| Real-user monitoring | Customer-facing front-ends collect performance and error telemetry; consent obtained where required |
| Browser performance | Core Web Vitals or equivalent collected for web front-ends |
| Mobile performance | Crash rate, startup time, and key-flow latency collected for mobile applications per the mobile application security standard |

---

## 11. Dashboards and alerting

| Control area | Requirement |
| --- | --- |
| Service dashboard | Each service has a maintained dashboard covering its service-level signals and key dependencies |
| Operational view | A consolidated operational view supports on-call and incident response |
| Alert design | Alerts are actionable, attributable, and tied to a runbook; symptom-based preferred |
| Alert routing | Routing matches on-call ownership; per the incident response procedure |
| Alert fatigue | Alert noise is reviewed; persistently noisy alerts are tuned or retired |
| Customer-impact alerts | Customer-impact thresholds drive incident declaration per the resilience programme |

---

## 12. Privacy and data classification

| Control area | Requirement |
| --- | --- |
| Personal data | Personal data avoided in telemetry; where present, classification is recorded |
| Data subject rights | Telemetry stores are evaluated for data-subject-rights obligations |
| Cross-border | Telemetry storage location considered per the cross-border data flow register |
| Anonymization and pseudonymization | Used where the analytical question allows |
| Customer-controlled signals | Customer telemetry preferences honoured |

---

## 13. Cost governance

| Control area | Requirement |
| --- | --- |
| Cost visibility | Telemetry cost attributed to the owning service and team |
| Budget review | Telemetry cost reviewed alongside engineering and infrastructure budgets |
| High-cardinality controls | Runaway-cardinality alerts; quotas where required |
| Retention review | Retention reviewed against the cost profile and the analytical need |
| Sampling review | Sampling rates reviewed periodically against the questions asked |

---

## 14. AI and ML telemetry

| Control area | Requirement |
| --- | --- |
| Prompt and completion logging | Per the [`AI and Agentic Development Security Standard`](../ai/standard-ai-and-agentic-development-security.md) (Inference call logging control) |
| Tool invocations | Per the AI access and agent permissions standard |
| Cost telemetry | Per the AI inference cost governance standard |
| Safety classifier output | Captured for evaluation and incident review |
| Drift signals | Captured per the AI model lifecycle |
| Retrieval source telemetry | Source-of-truth tracking; per the training data governance procedure where applicable |

---

## 15. Tooling and platform

| Control area | Requirement |
| --- | --- |
| Common platform | A common observability platform is preferred; per-team tooling justified |
| OpenTelemetry alignment | OpenTelemetry collection and semantic conventions preferred for portability |
| Self-instrumentation | Library and SDK instrumentation chosen for maintenance burden, not just coverage |
| Platform health | The observability platform has its own telemetry; loss of telemetry is itself observable |
| Outage independence | The observability platform's failure modes do not coincide with the production estate's failure modes |

---

## 16. Testing

| Control area | Requirement |
| --- | --- |
| Telemetry tested | Critical telemetry is exercised in pre-production; gaps detected before production |
| Alert tested | Critical alerts have a mechanism for tested firing (chaos drill or scheduled test) |
| Dashboards tested | Dashboard queries continue to return data after schema changes |
| Game days | Telemetry quality is validated during game-day exercises |

---

## 17. Operating expectations

1. Each service onboards to this standard before acceptance into service.
2. Telemetry gaps surface in post-incident reviews and feed back to the service team.
3. Telemetry cost is a quarterly engineering finance review topic.
4. Retention and sampling decisions are revisited at least annually.

---

## 18. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| Google SRE | The four golden signals, SLOs, error budgets | Reliability practice |
| ITIL 4 | Service value chain; monitoring and event management | Service management |
| ISO/IEC 20000-1 | §9.1 Monitoring, measurement, analysis and evaluation | Service monitoring and measurement |
| ISO/IEC 27001:2022 | A.5.7, A.8.15, A.8.16 | Threat intelligence, logging, monitoring |
| NIST SP 800-137 | Information Security Continuous Monitoring | Continuous monitoring |
| OpenTelemetry | Specification and semantic conventions | Telemetry portability |
| W3C Trace Context | Trace propagation | Distributed tracing |

---

## 19. Limitations

This standard is a CC BY-SA 4.0 baseline. Telemetry tooling and vendor capabilities change; the standard expresses requirements rather than vendor-specific implementations. Adopting organizations select tooling consistent with their cost, scale, and platform diversity.

---

**End of Document**
