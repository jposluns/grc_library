# IT Operations Key Performance Indicators Register

**Document Title:** IT Operations Key Performance Indicators Register 
**Document Type:** Register 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Officer 
**Approving Authority:** Chief Information Officer 
**Related Documents:** [`operations/framework-it-service-management.md`](framework-it-service-management.md), [`operations/standard-service-level-management.md`](standard-service-level-management.md), [`operations/register-it-security-operations.md`](register-it-security-operations.md), [`operations/procedure-patch-management.md`](procedure-patch-management.md), [`operations/procedure-security-monitoring-and-alert-management.md`](procedure-security-monitoring-and-alert-management.md), [`governance/register-digital-trust-and-assurance-metrics.md`](../governance/register-digital-trust-and-assurance-metrics.md), [`resilience/register-resilience-metrics-and-testing-log.md`](../resilience/register-resilience-metrics-and-testing-log.md) 
**Classification:** Public 
**Category:** Operations 
**Review Frequency:** Annual and upon material service, infrastructure, or regulatory change 
**Repository Path:** [`operations/register-it-operations-kpis.md`](register-it-operations-kpis.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This register defines the key performance indicators (KPIs) used to measure IT operations effectiveness across availability, incident management, change management, problem management, patch and vulnerability management, capacity, service desk, and security operations. KPIs support governance reporting to the CIO and Executive Risk Committee (ERC) and align with ISO/IEC 20000-1:2018, ITIL 4, COBIT 2025, and EU NIS 2 Directive obligations.

This register is a public-domain baseline. Adopting organizations must populate target values, reporting owners, and evidence sources that match their own service catalogue, risk appetite, contractual obligations, and regulatory requirements.

---

## Scope

This register applies to all IT services, infrastructure, cloud environments, and operational functions managed by or on behalf of the organization.

---

## KPI design principles

1. Each KPI must have a defined measurement rule, target or threshold, frequency, owner role, and evidence class.
2. KPIs must distinguish activity metrics from effectiveness metrics.
3. KPIs must not create incentives that reward superficial performance over risk reduction.
4. KPIs must connect to evidence classes that can be independently verified.
5. Known limitations and data-quality issues must be documented alongside the KPI.
6. KPIs must be reviewed when service scope, risk profile, or contractual obligations materially change.

---

## Section 1: availability and infrastructure

| KPI | Measurement Rule | Target | Frequency | Owner Role | Evidence Class | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Critical service availability | Percentage of scheduled operational time that critical services are available, excluding approved maintenance windows. | 99.5% monthly per critical service | Monthly | Service Owner | Monitoring platform availability record, SLA report | Define service tiers and approved maintenance windows in the service catalogue. |
| Infrastructure component uptime | Percentage uptime for core infrastructure components (compute, storage, network, identity services) measured per component group. | 99.9% monthly per component group | Monthly | IT Operations Manager | Platform availability log, cloud provider status record | Separate internal infrastructure from cloud provider availability where dependencies differ. |
| Planned maintenance compliance | Percentage of planned maintenance windows completed within approved schedule and duration. | 95% | Monthly | Change Manager | Change record, maintenance window log | Overruns without approval are recorded as change deviations. |
| Cloud capacity utilization | Average utilization of provisioned cloud compute and storage capacity as a percentage of approved budget envelope. | 70 to 85% utilization band | Monthly | IT Operations Manager | Cloud cost management report, capacity dashboard | Values below 70% indicate over-provisioning; values above 85% indicate capacity risk. |

---

## Section 2: incident management

| KPI | Measurement Rule | Target | Frequency | Owner Role | Evidence Class | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| P1 incident resolution within SLA | Percentage of P1 (Critical) incidents resolved within the 4-hour resolution target defined in the IT Service Management Framework. | 90% | Monthly | Service Management Office | Incident record, SLA report | Resolution time is measured from incident creation to service restoration. |
| P2 incident resolution within SLA | Percentage of P2 (High) incidents resolved within the 8-hour resolution target. | 90% | Monthly | Service Management Office | Incident record, SLA report | |
| Mean time to detect (MTTD) | Average elapsed time between the occurrence of a service disruption and its detection, based on confirmed P1 and P2 incidents. | Trend tracking; establish baseline in Year 1 | Monthly | Service Management Office | Incident record, monitoring alert log | MTTD depends on monitoring coverage; track alongside monitoring coverage KPI. |
| Mean time to restore (MTTR) | Average elapsed time between incident detection and service restoration for P1 and P2 incidents. | P1: ≤ 4 hours; P2: ≤ 8 hours | Monthly | Service Management Office | Incident record, resolution log | |
| Major incident frequency | Count of P1 incidents per calendar month. | Trend reduction year-on-year | Monthly | Chief Information Officer | Incident register | No fixed target; trend reduction is the governance objective. |
| Incident recurrence rate | Percentage of P1 and P2 incidents that are repeat occurrences of a known issue without a permanent fix applied. | < 10% | Monthly | Problem Manager | Incident record, problem register | High recurrence indicates unresolved underlying causes. |
| NIS 2 notification compliance | Percentage of significant cybersecurity incidents for which EU NIS 2 early warning (24-hour) and full notification (72-hour) obligations were met. | 100% | Per occurrence; quarterly review | Chief Information Security Officer | Notification record, incident log | Applies where EU NIS 2 is in scope. Track separately from general incident SLA. |

---

## Section 3: change management

| KPI | Measurement Rule | Target | Frequency | Owner Role | Evidence Class | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Successful change rate | Percentage of implemented changes that achieve their stated objective without unplanned rollback, service impact, or post-implementation incident within 5 business days. | 95% | Monthly | Change Manager | Change record, post-implementation review | |
| Failed and rolled-back change rate | Percentage of implemented changes requiring rollback or causing a post-implementation P1 or P2 incident. | < 3% | Monthly | Change Manager | Change record, incident record | |
| Emergency change rate | Emergency changes as a percentage of total changes implemented per month. | < 5% | Monthly | Change Manager | Change record | High emergency change rates indicate inadequate change planning or release management. |
| Emergency change CAB retrospective compliance | Percentage of emergency changes reviewed by the Change Advisory Board within 5 business days of implementation. | 100% | Monthly | Change Manager | Change record, CAB minutes | Required by the IT Service Management Framework. |
| Change implementation on schedule | Percentage of approved Normal changes implemented within the approved implementation window. | 90% | Monthly | Change Manager | Change record | |

---

## Section 4: problem management

| KPI | Measurement Rule | Target | Frequency | Owner Role | Evidence Class | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Problem records opened for major incidents | Percentage of P1 incidents for which a formal problem record is opened within 2 business days of resolution. | 100% | Monthly | Problem Manager | Incident record, problem register | Required by the IT Service Management Framework. |
| Root cause analysis completion rate | Percentage of open problem records for which a root cause analysis is completed within 15 business days of problem record creation. | 90% | Monthly | Problem Manager | Problem record, RCA report | |
| Known Error Database (KEDB) review currency | Percentage of Known Error Database entries reviewed within the last 30 days for continued applicability and workaround accuracy. | 100% | Monthly | Problem Manager | KEDB record | Stale KEDB entries degrade incident resolution speed. |
| Problem record closure rate | Percentage of open problem records resolved and closed within 60 business days of creation, excluding formally deferred items. | 80% | Monthly | Problem Manager | Problem register | Deferred items must have an approved deferral reason and review date. |

---

## Section 5: patch and vulnerability management

| KPI | Measurement Rule | Target | Frequency | Owner Role | Evidence Class | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Critical vulnerability patch compliance | Percentage of internet-facing and internal systems patched or mitigated within 7 calendar days of a Critical-severity patch release. | 100% | Monthly | IT Operations Manager | Vulnerability scan, patch deployment record | Critical severity is defined by CVSS base score ≥ 9.0 or vendor critical rating. |
| High vulnerability patch compliance | Percentage of systems patched or mitigated within 14 calendar days of a High-severity patch release. | 95% | Monthly | IT Operations Manager | Vulnerability scan, patch deployment record | High severity is CVSS base score 7.0 to 8.9. |
| Vulnerability scan coverage | Percentage of in-scope systems scanned by the authorized vulnerability management tool within the last 7 days. | 100% | Weekly | IT Operations Manager | Vulnerability scan record | Coverage gaps must be tracked as exceptions. |
| Unmitigated critical and high vulnerability age | Count of open Critical and High vulnerabilities exceeding the patching timeline without a formal exception and compensating control. | 0 | Monthly | IT Operations Manager | Vulnerability register, exception register | Any non-zero value triggers a mandatory risk review. |
| Endpoint detection and response (EDR) coverage | Percentage of managed endpoints with a deployed and active endpoint detection and response agent. | 100% | Monthly | IT Security Manager | Endpoint management platform report | Exclusions require formal exception with compensating control. |

---

## Section 6: capacity management

| KPI | Measurement Rule | Target | Frequency | Owner Role | Evidence Class | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| CPU utilization: production systems | Average CPU utilization across production compute workloads as a percentage of provisioned capacity. | 40 to 75% sustained average | Monthly | IT Operations Manager | Capacity dashboard, cloud monitoring report | Sustained utilization above 75% triggers capacity planning review. |
| Storage utilization | Percentage of provisioned storage capacity in use across production environments. | < 80% | Monthly | IT Operations Manager | Storage management report | Alert threshold at 70%; capacity action required above 80%. |
| Network bandwidth utilization | Average bandwidth utilization on primary internet and inter-site links as a percentage of contracted capacity. | < 70% average; < 85% peak | Monthly | Network Operations | Network monitoring log | Sustained peak above 85% requires capacity planning review. |
| Capacity forecast accuracy | Variance between forecast capacity requirements (90-day forward estimate) and actual consumption, expressed as a percentage. | ± 15% | Quarterly | IT Operations Manager | Capacity plan, usage record | Accuracy below threshold triggers review of forecasting model. |

---

## Section 7: service desk and request fulfilment

| KPI | Measurement Rule | Target | Frequency | Owner Role | Evidence Class | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Service request SLA compliance | Percentage of service requests fulfilled within the agreed target time by priority tier. | 90% | Monthly | Service Desk Manager | ITSM portal request record | Define request categories and target times in the service catalogue. |
| First-contact resolution rate | Percentage of service desk contacts resolved at first contact without escalation to a second or third-line team. | 70% | Monthly | Service Desk Manager | ITSM portal record | Low rates indicate inadequate self-service content or knowledge base gaps. |
| Abandoned call or ticket rate | Percentage of inbound service desk contacts (calls, chat, tickets) abandoned before acknowledgement. | < 5% | Monthly | Service Desk Manager | ITSM portal record, telephony report | |
| Knowledge article currency | Percentage of service desk knowledge articles reviewed within the last 180 days. | 100% | Quarterly | Service Desk Manager | Knowledge management system record | |
| User satisfaction score | Average user satisfaction rating collected post-resolution per a defined scoring model. | Establish baseline in Year 1; target improvement year-on-year | Monthly | Service Desk Manager | Satisfaction survey record | Survey methodology and scale must be defined consistently to permit trend comparison. |

---

## Section 8: security operations

| KPI | Measurement Rule | Target | Frequency | Owner Role | Evidence Class | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Alert triage completion rate | Percentage of security alerts acknowledged and triaged within the defined SLA per alert severity tier. | 95% | Monthly | IT Security Manager | SIEM alert log, triage record | Triage SLA must be defined by alert severity tier in the security operations procedure. |
| False positive rate | Percentage of security alerts triaged and closed as false positives. | Baseline in Year 1; trend reduction thereafter | Monthly | IT Security Manager | SIEM alert log, triage record | High false positive rates indicate detection rule quality issues. |
| SIEM log source coverage | Percentage of in-scope log sources actively forwarding events to the SIEM within expected latency and volume thresholds. | 100% | Monthly | IT Security Manager | SIEM configuration record, source inventory | Log source gaps must be tracked as exceptions with compensating controls. |
| Security monitoring hours coverage | Percentage of calendar hours covered by active security monitoring (24/7 = 100%). | Defined by service model; document actual coverage | Monthly | IT Security Manager | Monitoring schedule, SIEM availability record | Where 24/7 coverage is not resourced, document hours covered and risk acceptance for uncovered periods. |
| Privileged account review compliance | Percentage of privileged accounts subject to access review within the required quarterly cadence. | 100% | Quarterly | IT Security Manager | Access review record, IAM platform export | |

---

## Section 9: reporting and governance

| Report | Frequency | Recipients | Owner Role | Content |
| --- | --- | --- | --- | --- |
| IT Operations KPI Dashboard | Monthly | CIO, Service Owners, Process Owners | Service Management Office | KPI results vs target for all eight categories; trend indicators; open exceptions. |
| SLA Performance Report | Monthly | CIO, Service Owners | Service Management Office | SLA compliance rates by service and priority; breach root causes; corrective actions. |
| Patch and Vulnerability Summary | Monthly | CIO, CISO | IT Operations Manager | Vulnerability count by severity, patch compliance rates, unmitigated critical items. |
| Capacity Review Report | Quarterly | CIO | IT Operations Manager | Utilization trends, capacity headroom, forecast vs actual, planned expansion. |
| Executive Summary: IT Governance | Quarterly | ERC | Chief Information Officer | Aggregated KPI trend, major incident summary, significant risks, improvement plan status. |
| Annual IT Operations Review | Annual | ERC, Internal Audit | Chief Information Officer | Full-year KPI performance, SLA breach analysis, capacity programme outcomes, improvement plan. |

---

## Evidence requirements

Adopting organizations must retain the following to substantiate KPI results:

- Monitoring platform availability exports and capacity dashboards.
- Incident register extracts and SLA compliance reports.
- Change records, CAB meeting minutes, post-implementation review summaries.
- Problem records and root cause analysis reports.
- Vulnerability scan outputs and patch deployment records.
- ITSM portal request and service desk records.
- SIEM alert logs and triage records.
- Satisfaction survey results.
- Capacity plans and utilization trend exports.

---

## Limitations

This register is a public-domain baseline. It does not define an adopting organization's actual service targets, risk appetite, contractual SLAs, or regulatory thresholds. Targets in this document are illustrative. Adopting organizations must substitute values consistent with their service model, customer contracts, regulatory obligations, and risk acceptance decisions.

---

## Maintenance

This register must be reviewed annually and when the service catalogue, technology stack, regulatory obligations, or risk profile changes materially. KPI targets must be calibrated against historical performance before being used as breach triggers for governance escalation.

---

**End of Document**
