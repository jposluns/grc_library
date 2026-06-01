# Recovery Runbook Template

**Document Title:** Recovery Runbook Template\
**Document Type:** Template\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** Resilience Owner\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`resilience/framework-business-continuity-and-resilience.md`](framework-business-continuity-and-resilience.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](standard-business-continuity-and-disaster-recovery.md), [`resilience/plan-it-disaster-recovery.md`](plan-it-disaster-recovery.md), [`resilience/procedure-backup-and-recovery.md`](procedure-backup-and-recovery.md), [`resilience/procedure-business-impact-analysis.md`](procedure-business-impact-analysis.md), [`resilience/procedure-continuity-and-recovery-testing.md`](procedure-continuity-and-recovery-testing.md), [`operations/procedure-change-management-and-configuration-control.md`](../operations/procedure-change-management-and-configuration-control.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md)\
**Classification:** Public\
**Category:** Resilience\
**Review Frequency:** Annual and upon material change to the system, its dependencies, or its recovery objectives\
**Repository Path:** [`resilience/template-recovery-runbook.md`](template-recovery-runbook.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template defines the structure of a recovery runbook for a single in-scope service, application, or platform. Each in-scope service has its own runbook instantiated from this template. The runbook is the authoritative operating document used by the recovery team during a degraded or failed state. It is not a strategy document; it is operational.

A populated runbook contains organisation-specific system, supplier, and contact data and is sensitive operational material. This CC BY-SA 4.0 template intentionally contains no example values for any field.

---

## Scope

This template covers application and platform recovery from a degraded or failed state, returning the service to its declared recovery time and recovery point objectives. It does not cover:

1. Cross-system disaster recovery orchestration; that lives in [`resilience/plan-it-disaster-recovery.md`](plan-it-disaster-recovery.md).
2. Crisis-level governance; see [`resilience/plan-business-continuity-and-crisis-management.md`](plan-business-continuity-and-crisis-management.md).
3. Forensic preservation; the runbook integrates with the security incident response procedure where preservation is required.

---

## Runbook structure

Each runbook must include the following sections in this order.

### Section 1: System identification

| Field | Description |
| --- | --- |
| System name | Canonical name in the asset inventory |
| System owner role | Role accountable for the system |
| Service owner role | Role accountable for the customer-facing service this system supports |
| Criticality tier | Tier classification from the BIA |
| RTO | Recovery Time Objective (target time to restore service after declaration) |
| RPO | Recovery Point Objective (maximum acceptable data loss measured in time) |
| MTPD | Maximum Tolerable Period of Disruption (organisation-level tolerance) |
| Business impact summary | One paragraph describing the consequence of outage to customers, regulators, finances, safety |
| Runbook version | Version of this runbook |
| Last successful recovery test | Date and reference to the test record |

### Section 2: Dependencies

| Dependency type | Required content |
| --- | --- |
| Upstream systems | Systems this service consumes; per-dependency criticality and failure mode |
| Downstream systems | Systems that consume this service; per-consumer impact of outage |
| Third-party suppliers | Per-supplier service name, contract reference, contact path, SLA |
| Identity and access | Identity provider, secrets management, certificate authority |
| Data stores | Primary database, replicas, object storage, search indexes; per-store backup location |
| Network paths | VPN, private endpoints, egress gateways, DNS dependencies |
| Compute platform | Cloud provider, region, account or subscription, cluster |
| Monitoring and alerting | Dashboard URLs in internal use; alert routing |

### Section 3: Detection and declaration

| Field | Description |
| --- | --- |
| Detection signals | Specific alerts, thresholds, or external signals that indicate degradation or failure |
| Severity criteria | When to treat the event as P1, P2, P3, P4 per the incident severity matrix |
| Declaration authority | Role authorised to declare a recovery event |
| Declaration channel | Where the declaration is logged |
| Notification list | Roles to notify on declaration; expected notification times |

### Section 4: Pre-recovery checks

Before initiating recovery, confirm:

1. The event is confirmed as a real failure, not a false alarm.
2. The decision to recover (rather than wait, fail over, or roll back) has been made by the Declaration Authority.
3. Forensic preservation, if required by the security incident response procedure, has been completed or is running in parallel.
4. Change advisory board notification has been waived or obtained, per the change management procedure.
5. Communication channels are open to customers, internal teams, and the regulator if applicable.

### Section 5: Recovery steps

Each step is concrete and reproducible. Steps are numbered, owned by a specific role, and have an expected outcome and a verification step.

| Step | Action | Owner | Expected outcome | Verification |
| --- | --- | --- | --- | --- |
| 1 | Concrete command or task | Role | What success looks like | How to verify |
| 2 | ... | ... | ... | ... |

Steps include all of:

1. Pre-flight validation (credentials, access, target state of dependencies).
2. Stopping the failed service cleanly where possible.
3. Restoring data from the backup or replica chosen by the Declaration Authority.
4. Bringing the service back online in the correct dependency order.
5. Validating data integrity post-restore.
6. Re-enabling monitoring and alerting.
7. Resuming customer traffic in a controlled manner (canary, ramp, full).

### Section 6: Validation

Recovery is not complete until validation passes. The runbook defines specific validation tests covering:

| Validation area | Required content |
| --- | --- |
| Functional smoke tests | Specific user journeys or API calls that demonstrate the service is operating |
| Data integrity tests | Specific queries or hashes that confirm data is consistent |
| Performance check | Response time, throughput, or capacity check against an acceptance threshold |
| Security check | Authentication, authorisation, encryption-in-transit confirmation |
| Customer experience check | External monitor or canary user confirmation |

### Section 7: Communications

| Communication | Channel | Audience | Timing |
| --- | --- | --- | --- |
| Internal status updates | Operations channel | Internal responders | Every 30 minutes during active recovery |
| Customer notification | Status page; email if material | Customers | At declaration; at material milestones; at resolution |
| Regulator notification | Per regulator | Supervisory authority | Per the applicable regulatory window |
| Executive briefing | Email or call | Executive Sponsor | At declaration; hourly during P1 |
| Post-recovery report | Email | Recipients per incident report distribution | Within 5 business days of closure |

### Section 8: Rollback

If recovery fails or introduces a worse state, the rollback procedure restores the prior degraded state cleanly.

1. Criteria for invoking rollback.
2. Authority to invoke rollback.
3. Rollback steps with owner, expected outcome, verification.
4. Communication on rollback to the same audiences.

### Section 9: Closure and learning

After successful recovery and validation:

1. Confirm full service restoration with the service owner.
2. Document the timeline, deviations from the runbook, and the cause analysis.
3. Feed corrective actions into the corrective action register.
4. Update this runbook if the recovery exposed gaps or process improvements.

### Section 10: Test history

Each scheduled recovery test against this runbook is recorded with date, scope (full or partial), outcome, deviations, and corrective actions. The test history is reviewed annually as input to the BIA refresh.

---

## Operating expectations

1. Each in-scope service has its own runbook instantiated from this template before the service goes live.
2. The runbook is owned by the service owner and reviewed annually.
3. The runbook is tested per the resilience testing procedure: at minimum annually for Tier 1, at minimum every two years for Tier 2, on a defined cadence for Tier 3.
4. Runbook changes follow the change management procedure if material.
5. The populated runbook is stored in a location accessible to responders during an event; offline copy is maintained where the platform itself could be unavailable.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO 22301:2019 | §8.4 Business continuity procedures | Operational recovery |
| ISO/IEC 27031 | ICT readiness for business continuity | IT recovery |
| NIST SP 800-34 Rev 1 | Contingency Planning Guide | US federal recovery planning |
| DORA | Article 12 ICT business continuity policy | Financial sector recovery |
| NIS 2 | Article 21(2)(c) Business continuity | EU essential entity recovery |
| ITIL 4 | Service continuity management | Practice alignment |

---

## Limitations

This template is a CC BY-SA 4.0 structural baseline. Recovery runbooks are inherently system-specific; the operational fidelity of any given runbook depends on the service owner's diligence in populating it and on testing the populated runbook end to end. The template is not a substitute for testing or for the BIA-driven recovery objectives.

---

**End of Document**
