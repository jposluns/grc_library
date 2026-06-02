# Site Reliability Engineering Standard

**Document Title:** Site Reliability Engineering Standard\
**Document Type:** Standard\
**Version:** 1.0.1\
**Date:** 2026-06-02\
**Owner:** Chief Information Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`operations/framework-it-service-management.md`](framework-it-service-management.md), [`operations/standard-service-level-management.md`](standard-service-level-management.md), [`operations/standard-observability-and-telemetry.md`](standard-observability-and-telemetry.md), [`operations/procedure-change-management-and-configuration-control.md`](procedure-change-management-and-configuration-control.md), [`resilience/policy-business-continuity-and-disaster-recovery.md`](../resilience/policy-business-continuity-and-disaster-recovery.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md)\
**Classification:** Public\
**Category:** IT Operations\
**Review Frequency:** Annual and upon material change to reliability practice, platform, or service architecture\
**Repository Path:** [`operations/standard-site-reliability-engineering.md`](standard-site-reliability-engineering.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This standard defines the site reliability engineering (SRE) practice for services operated by the organisation. It expresses outcomes and operating principles for reliability, not vendor-specific tooling. The standard complements the service-level management standard (which formalises the contract with the customer) and the observability and telemetry standard (which provides the measurement substrate).

---

## Scope

This standard applies to:

1. Customer-facing services that have a published service-level objective (SLO).
2. Internal services whose unavailability would have material business or operational impact.
3. Shared platform services (identity, telemetry, secrets, networking, data) that other services depend on.
4. AI inference services operated as production services.

Services that have not been classified as production are out of scope until acceptance into service.

---

## Section 1: principles

| Principle | Description |
| --- | --- |
| Reliability is a feature | Reliability is designed, measured, and traded against feature velocity |
| Service-level objectives are explicit | Targets are stated as SLOs; informal targets are insufficient |
| Error budgets shape decisions | Time-bounded budgets govern the trade between change rate and risk |
| Toil is reduced, not endured | Repetitive operational work is engineered away |
| Blameless learning | Incidents drive learning, not punishment |
| Software-defined operations | Operations are codified, tested, and version-controlled |
| Reliability is a shared outcome | SRE collaborates with engineering, security, privacy, and product |

---

## Section 2: service-level objectives and indicators

| Concept | Requirement |
| --- | --- |
| Service-level indicator (SLI) | A direct measurement of service behaviour (availability, latency, quality, freshness, throughput) |
| Service-level objective (SLO) | A target on the SLI over a defined window (e.g. 99.9% over a rolling 28 days) |
| Service-level agreement (SLA) | Customer-facing commitment; per the service-level management standard |
| Error budget | The allowed unreliability inside the SLO window |
| Burn rate | The rate at which the error budget is being consumed |
| Multi-window alerting | Alerts fire on multiple burn-rate windows to balance sensitivity and precision |
| SLO review | SLOs reviewed at least annually; aligned with customer expectations and engineering capacity |

---

## Section 3: error budget policy

| Trigger | Action |
| --- | --- |
| Budget healthy | Feature delivery proceeds at the team's normal cadence |
| Budget low (e.g. less than 25% remaining) | Reliability work is prioritized; changes are reviewed more carefully |
| Budget exhausted | Non-critical changes paused; reliability work prioritized until the budget recovers |
| Repeated exhaustion | Architectural review; SLO recalibration or platform investment |
| Budget unused | Permission to take controlled reliability risks (e.g. chaos exercises, dependency upgrades) |

The error budget policy is owned by the service team in collaboration with SRE; exceptions are escalated to the engineering leadership.

---

## Section 4: reliability practices

| Practice | Description |
| --- | --- |
| Capacity and load testing | Per the capacity and performance management standard |
| Performance regression | Performance regressions detected in pre-production; gated where appropriate |
| Failure injection | Game days and chaos exercises exercise failure modes |
| Dependency mapping | Service dependencies are mapped; critical dependencies have known failure modes |
| Graceful degradation | Services degrade gracefully under partial failure |
| Backpressure | Backpressure mechanisms prevent cascade failure |
| Circuit breaking | Downstream failure does not propagate unbounded retries |
| Idempotency | Operations are idempotent where retry is possible |
| Timeout and retry | Timeouts and retry policies are explicit; defaults reviewed |

---

## Section 5: change-related risk

| Practice | Description |
| --- | --- |
| Progressive rollout | Canary, ramp, full; each stage has acceptance criteria |
| Feature flags | High-risk features are flag-controlled; flags have ownership and expiry |
| Automated rollback | Rollback paths are tested and automatable |
| Change risk classification | Per the change management procedure |
| Production access | Per the privileged access management standard |
| Configuration changes | Configuration is treated as code; the same release rigour applies |

---

## Section 6: incident management

| Practice | Description |
| --- | --- |
| Incident declaration | Customer impact triggers declaration; impact thresholds are documented |
| Incident command | Incident commander role activated for material incidents |
| Communication | Internal and customer communication per the resilience programme communications |
| Time-bound mitigation | Mitigation is prioritized over root-cause finding during active incidents |
| Stand-down criteria | Documented criteria for declaring an incident resolved |
| Post-incident review | Conducted within a defined window; blameless format |
| Lessons recorded | Per the lessons-learned template |
| Repeat incidents | Repeat incidents trigger an architectural review |

---

## Section 7: on-call

| Practice | Description |
| --- | --- |
| Coverage | Coverage hours and rotations are documented |
| Primary and secondary | Primary on-call with documented escalation to secondary |
| Hand-off | Structured shift handover; outstanding items recorded |
| Pager load | Pager load tracked; sustained excessive load triggers reliability investment |
| Compensation | On-call practice respects working-time and compensation arrangements |
| Training | On-call engineers are trained on runbooks, incident command, and telemetry tooling |
| Well-being | On-call is structured to protect engineer well-being; per the operating expectations |
| AI assistance | AI assistants used to support on-call are governed per the AI access and agent permissions standard |

---

## Section 8: toil management

| Practice | Description |
| --- | --- |
| Toil definition | Operational work that is manual, repetitive, automatable, tactical, and devoid of enduring value |
| Toil budget | Time spent on toil is tracked; sustained excess triggers automation investment |
| Toil reduction | Service teams have a target proportion of engineering time spent on reliability work and toil reduction |
| Automation hygiene | Automation built for toil reduction is itself maintained |
| Manual interventions | Repeated manual interventions trigger root-cause analysis or automation |

---

## Section 9: runbooks and operational documentation

| Practice | Description |
| --- | --- |
| Per-alert runbooks | Every actionable alert has a runbook |
| Per-service runbook | Each service has a service runbook covering common operations |
| Per-recovery scenario runbook | Per the recovery runbook template; aligned with the resilience programme |
| Runbook validation | Runbooks are exercised during game days; stale runbooks updated |
| Searchability | Runbooks are searchable; linked from alerts and dashboards |
| Localisation | Runbooks accessible to the global on-call population |

---

## Section 10: reliability engineering practices for AI services

| Practice | Description |
| --- | --- |
| Model availability SLO | Availability targets stated separately from quality targets |
| Quality SLO | Quality targets stated per the evaluation suite |
| Provider degradation | Provider-side degradation is detected and surfaced separately from organisational service health |
| Cost runaway | Cost-anomaly detection per the AI inference cost governance standard |
| Fallback paths | Fallback to alternate models or non-AI paths where the system supports it |
| Safety classifier behaviour | Safety classifier output is part of the reliability picture |

---

## Section 11: tooling and platform

| Element | Description |
| --- | --- |
| Telemetry platform | Per the observability and telemetry standard |
| Incident management platform | Supports declaration, command, communication, and post-incident review |
| On-call paging | Reliable; tested; alternate channels available |
| Runbook platform | Versioned; linkable from alerts |
| Knowledge base | Capturing institutional reliability knowledge |
| Game-day tooling | Supports failure injection in a controlled, recoverable manner |

---

## Section 12: governance

| Element | Description |
| --- | --- |
| Reliability council | Reviews SLO portfolio, error-budget signals, repeat incidents, and platform-level reliability |
| Reliability scorecards | Per service; reviewed quarterly |
| Investment prioritisation | Reliability investments compete on equal footing with feature investments |
| Customer feedback | Customer-perceived reliability signals (support tickets, NPS, social feedback) inform investment |
| Cross-functional integration | Coordination with security, privacy, compliance, and product |

---

## Operating expectations

1. SLOs are published, monitored, and reviewed at least annually.
2. The error budget policy is enforced consistently across services.
3. Post-incident reviews occur within a defined window after material incidents.
4. On-call engineer well-being is monitored; sustained pager load triggers reliability investment.
5. Reliability investment is at least a defined share of overall engineering capacity for services with established SLOs.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| Google SRE Book and SRE Workbook | Reference SRE practice | Practice baseline |
| ITIL 4 | Service value chain; incident, problem, change practices | Service management |
| ISO/IEC 20000-1 | Service management requirements | Service management standard |
| ISO/IEC 27001:2022 | A.5.29 Information security during disruption | Resilience cross-walk |
| ISO 22301 | Business continuity management | Continuity cross-walk |
| DORA | Articles 5 to 16 (ICT risk management) | EU financial services |
| NIST CSF 2.0 | Detect, Respond, Recover | Risk function alignment |
| The Phoenix Project / The Unicorn Project | Practitioner references | Cultural baseline |

---

## Limitations

This standard is a CC BY-SA 4.0 baseline. Reliability practice is rapidly evolving; specific tooling, SLO targets, and error-budget policies are organisation-specific. Adopting organisations confirm current practice with subject-matter experts and tune targets to their customer and regulatory profile.

---

**End of Document**
