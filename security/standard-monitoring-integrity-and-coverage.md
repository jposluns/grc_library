# Monitoring Integrity and Coverage Standard

**Document Title:** Monitoring Integrity and Coverage Standard\
**Document Type:** Standard\
**Version:** 0.0.2\
**Date:** 2026-08-31\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/principle-fail-closed-automation.md`](../governance/principle-fail-closed-automation.md), [`security/standard-logging-and-monitoring.md`](standard-logging-and-monitoring.md), [`security/standard-soc-operating-model.md`](standard-soc-operating-model.md), [`operations/standard-observability-and-telemetry.md`](../operations/standard-observability-and-telemetry.md), [`operations/procedure-security-monitoring-and-alert-management.md`](../operations/procedure-security-monitoring-and-alert-management.md), [`operations/procedure-threat-intelligence-and-siem-operations.md`](../operations/procedure-threat-intelligence-and-siem-operations.md), [`security/procedure-security-incident-response.md`](procedure-security-incident-response.md), [`resilience/procedure-security-incident-reporting-and-escalation.md`](../resilience/procedure-security-incident-reporting-and-escalation.md), [`operations/register-it-operations-kpis.md`](../operations/register-it-operations-kpis.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material threat, framework, or regulatory change\
**Repository Path:** [`security/standard-monitoring-integrity-and-coverage.md`](standard-monitoring-integrity-and-coverage.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

This standard establishes enterprise-wide requirements for the integrity and coverage of monitoring itself: the health of the detection, logging, and observation systems the organization relies on to know its own security and operational state. It treats the compromise, silence, saturation, or degradation of a monitoring source as a first-class condition to be detected, classified, and, when unexplained, escalated as an incident; it requires coverage blind spots to be declared rather than discovered; and it distinguishes a demonstrated absence of adverse events from an unexamined silence. It is the control-level instantiation of the fail-closed automation principle applied to monitoring: when the organization cannot see, it does not assume all is well.

---

## 1. Purpose

Monitoring tells an organization what is happening in its systems, and every downstream security and operational decision rests on the assumption that the monitoring is working. That assumption is rarely governed as a whole. Individual controls in this library detect adverse events in monitored systems, and a few already watch specific monitoring sources for silence: a critical log source that stops feeding the security-information and event-management platform, a telemetry platform required to observe its own loss. What the library has lacked is a single standard that governs the integrity and coverage of monitoring across every domain and failure mode, so that those scoped operational checks sit under one accountable, risk-governed frame and the gaps between them are closed.

This standard governs monitoring integrity and coverage as a first-class control. It requires that monitoring sources be inventoried and owned, that their expected signals and health be defined and watched, that a failure of monitoring be recognized and, when unexplained, handled as an incident, that coverage gaps be declared in advance rather than found after an event, and that no-alert be read as evidence of safety only when the monitoring for that interval is demonstrably healthy. An attacker who cannot avoid detection will attempt to disable it; this standard raises the cost of that path and shortens the time an undetected blind spot can persist.

## 2. Scope

This standard applies to all monitoring the organization depends on to establish its security and operational state, regardless of domain or implementing team. In scope:

- Security monitoring: SIEM ingestion and correlation, endpoint detection and response, intrusion detection, network and email security telemetry, and threat-intelligence feeds.
- Operational and availability monitoring: infrastructure, application, and service-health observability and telemetry.
- Physical and environmental monitoring where it feeds security or safety decisions (for example camera and access-control telemetry).
- Compliance, privacy, and AI-system monitoring that produces evidence a control or obligation relies on.
- Supplier-provided and manually-operated monitoring where a control depends on its output.

The unit of governance is the monitoring source and the chain that carries its signal from the observed system to the human or automated decision that acts on it. Out of scope is the design of the detections themselves (governed by the logging, SOC, and observability documents in Related Documents); this standard governs whether those detections are alive, complete, and trustworthy, not what they look for. Retirement of a monitoring source without a replacement is a decommissioning activity governed elsewhere; this standard governs the health of monitoring in service.

## 3. Principles

- **Monitoring is a control, and a control can fail.** The health of a monitoring source is itself monitored, owned, and evidenced; an unmonitored monitor is an ungoverned single point of failure.
- **Fail closed on lost visibility.** When monitoring for a scope is compromised, silent, saturated, or degraded, the organization treats that scope as being in an unknown state and escalates, rather than assuming the last-known-good state persists. This is the fail-closed automation principle applied to observation.
- **Absence of evidence is not evidence of absence.** No alert and no event mean the monitored scope is safe only when coverage and pipeline health for that interval are demonstrated; otherwise the correct status is unknown or blind, not clear.
- **Blind spots are declared, not discovered.** Where coverage is knowingly incomplete, the gap is recorded in advance with its owner, cause, expiry, and compensating control, so that a decision-maker sees the limit of what the monitoring can support.
- **Detect the failure of detection.** Monitoring integrity depends on independent, out-of-band checks that do not share a failure mode with the monitoring they verify.

## 4. Ownership, inventory, and expected signals

Every monitoring source in scope has a named owner accountable for its health, an entry in a monitoring inventory, a criticality rating, a defined set of expected signals (what it should emit, and at what cadence or volume), a health service-level objective, and an independent escalation path used when the source itself fails. The inventory is the authoritative list against which coverage and silence are judged; a source that is not in the inventory cannot be reconciled and is treated as an ungoverned gap. Criticality determines the health service-level objective and the incident severity a failure of the source attracts.

## 5. Monitoring-failure taxonomy

A monitoring source can fail in four distinct ways, each of which this standard treats as a monitoring-health condition to be detected and classified:

- **Compromise:** the source or its pipeline is tampered with, spoofed, disabled, or reconfigured to suppress signal, whether by an adversary impairing defences or by an erroneous change.
- **Silence:** an expected signal or heartbeat is missing: a log source stops ingesting, an agent stops reporting, a feed stops updating.
- **Saturation:** capacity, queue, storage, or analyst attention is exhausted, so events are dropped, delayed, or lost, including the case where logging fails because storage is exceeded.
- **Degradation:** the signal continues but its fidelity falls: latency rises, sampling thins, schema or quality drifts, a detection rule breaks, or coverage silently narrows.

Each condition is defined per source against its expected signals and health service-level objective, so that the transition into the condition is detectable rather than inferred after an event.

## 6. Condition-to-incident transition

The four failure conditions in section 5 are not, by themselves, incidents; a single transition rule governs how a detected condition is dispositioned, so that "monitoring-health condition", "declared blind spot", and "incident" are not used interchangeably:

1. A monitoring-health condition is **detected** against a source's expected signals and health service-level objective.
2. If the affected scope is covered by a current **declared blind spot** (section 7), the condition is a recorded, accepted, and time-bounded gap, and is handled under that blind spot's terms rather than as a new incident.
3. If the condition has an **explained, benign cause** (planned maintenance, a scheduled change, a known and bounded outage), it is a reportable operational condition, recorded and resolved without incident escalation.
4. If the condition is **unexplained**, or is explained but suspected of masking or coinciding with adverse activity, it is escalated as an **incident** and classified by severity per section 10.

The health service-level objective and criticality of the source set the timing and severity thresholds at each step; the default on genuine ambiguity is to escalate, consistent with the fail-closed principle.

## 7. Declared blind spots

Where monitoring coverage is knowingly incomplete, the gap is recorded as a declared blind spot before it is relied upon, not surfaced after an incident. A declared blind spot records its scope, its cause, its start and expiry dates, the decisions it affects, its owner, the approval accepting the residual risk, any compensating control, and a visible statement of the risk carried while it stands. Declared blind spots are reviewed on expiry and are re-approved rather than renewed silently. An undeclared gap discovered during or after an event is a control failure; a declared blind spot is an accepted, time-bounded, and visible limit.

## 8. Absence-of-evidence discipline

A quiet monitoring surface is reported as safe only when the coverage and pipeline health for the interval in question are demonstrated. Where that health cannot be shown, the status of the scope is unknown or blind, and it is treated as such in any decision that relies on it. This discipline governs how monitoring output is read: a clean dashboard, an empty alert queue, or a zero-finding interval is a positive assurance only against demonstrated coverage, and is otherwise an open question the organization resolves before acting on it. Attestations and control-effectiveness claims that rest on monitoring output state the coverage they assume.

## 9. Detecting the failure of detection

Monitoring integrity is verified by independent mechanisms that do not share a failure mode with the monitoring they check: heartbeats and dead-man alerts that fire on the absence of an expected signal, synthetic canaries and end-to-end delivery tests that exercise the full chain from observed system to alert, expected-volume baselines that surface silence and saturation, inventory reconciliation that finds sources that have fallen out of coverage, and out-of-band checks that do not depend on the monitoring pipeline being healthy. These mechanisms are themselves owned and tested; a check that shares infrastructure with the monitored source cannot be relied upon to survive that source's failure.

## 10. Incident handling for monitoring failure

A monitoring-failure condition escalated to an incident under section 6 is triaged and classified by the criticality of the affected source, the breadth and duration of the lost visibility, whether monitoring independence has been lost, whether compromise is suspected, and whether an active investigation is impaired. A monitoring failure that coincides with, or could mask, other adverse activity is treated as higher severity, because the loss of visibility is itself a condition an adversary seeks. Monitoring-failure incidents are reported and escalated through the incident-response and reporting paths in Related Documents; this standard establishes the transition that makes the condition an incident and the factors that set its severity, and those procedures govern the response.

## 11. Testing and evidence

The organization tests monitoring integrity rather than assuming it. Tests exercise each failure mode in the taxonomy: forced silence of a source, tampering with or disabling a source, saturation of a pipeline, and degradation of signal fidelity, each confirming that the condition is detected, classified through the section 6 transition, and escalated where required. End-to-end alert-delivery tests, failover and restoration exercises, and retrospective validation after a real failure confirm that the detect-the-failure-of-detection mechanisms work in practice. Evidence of these tests, of the monitoring inventory and its health service-level objectives, of declared blind spots and their approvals, and of monitoring-failure incidents and their resolution is retained for review and audit.

## 12. Framework alignment

| Requirement | NIST CSF 2.0 | NIST SP 800-137 / 137A | ISO/IEC 27001:2022 | CSA CCM v4.1 | MITRE ATT&CK | NIST SP 800-92 |
| --- | --- | --- | --- | --- | --- | --- |
| Monitoring as a governed, health-owned control | DE.CM-09 | ISCM strategy and programme | A.8.16 | LOG-03 | n/a | Log-management infrastructure health |
| Failure of the monitoring system reported and handled | DE.AE-06, DE.AE-08 | Gap and shortcoming detection | A.8.15, A.8.16 | LOG-14 | T1685 | Response to log-management failures |
| Saturation and dropped-event handling | PR.IR-04 | Programme-gap assessment | A.8.15 | LOG-05 | T1685 | Storage-exceeded and overflow handling |
| Declared coverage limits and blind spots | GV.RM-02 | Coverage and effectiveness assessment | A.8.16 | LOG-03 | n/a | n/a |
| Detection of detection failure (independent checks) | DE.CM-09, DE.AE-08 | Continuous assessment | A.8.16 | LOG-14 | T1685 | Monitoring the log-management status |
| Incident classification for lost visibility | DE.AE-04, DE.AE-08 | n/a | A.5.25 | SEF-06, SEF-07 | T1685 | n/a |

Control identifiers are cited at the objective level; the paired procedures in Related Documents carry the operational detail. MITRE ATT&CK technique T1685 ("Disable or Modify Tools") and its sub-techniques model the adversary impairment of security tooling this standard defends against; it is the current identifier for that behaviour, superseding the retired T1562 (formerly "Impair Defenses").

## 13. Limitations

This standard governs the integrity and coverage of monitoring, not the design of the detections themselves, which the logging, SOC, observability, and threat-intelligence documents in Related Documents own; a monitoring source can be healthy and complete under this standard and still look for the wrong things. The absence-of-evidence discipline reduces, but does not eliminate, the risk that a sufficiently sophisticated adversary defeats both a monitoring source and its independent check; defence in depth across independent mechanisms is the mitigation, not a guarantee. Several requirements here are organizational design choices informed by, but not prescribed in these exact forms by, the sources in the framework-alignment table: the absence-of-evidence-versus-evidence-of-absence rule in section 8, the requirement that integrity checks be independent of a common failure mode, the declared-blind-spot record schema in section 7, and the transition that designates an unexplained monitoring failure an incident. The held sources support monitoring, failure and anomaly reporting, capacity, and gap assessment (for example CSA CCM LOG-14 on failures-and-anomalies reporting and NIST SP 800-137A on detecting gaps and shortcomings); they do not prescribe these specific control designs. Retirement of a monitoring source is governed by the organization's decommissioning and change-management controls, not by this standard.
