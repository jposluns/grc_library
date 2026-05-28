# Service Level Management Standard

**Document Title:** Service Level Management Standard 
**Document Type:** Standard 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Officer 
**Approving Authority:** Chief Information Officer 
**Related Documents:** [`operations/framework-it-service-management.md`](framework-it-service-management.md), [`operations/register-it-operations-kpis.md`](register-it-operations-kpis.md), [`operations/register-it-security-operations.md`](register-it-security-operations.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](../resilience/standard-business-continuity-and-disaster-recovery.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md) 
**Classification:** Public 
**Category:** Operations 
**Review Frequency:** Annual and upon material service, contract, or regulatory change 
**Repository Path:** [`operations/standard-service-level-management.md`](standard-service-level-management.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This standard defines the requirements for establishing, monitoring, reviewing, and managing Service Level Agreements (SLAs) and Operational Level Agreements (OLAs) across all IT services. It establishes how service targets are set, how breaches are detected and escalated, how SLA performance is reported, and how SLAs are maintained over the service lifecycle. It supports ISO/IEC 20000-1:2018 §8.3, ITIL 4 Service Level Management practice, and COBIT 2019 DSS02.

---

## Scope

This standard applies to:

- All IT services delivered to internal customers, including business units and operational functions.
- All Operational Level Agreements between internal IT teams supporting service delivery.
- All externally sourced services where the organization is the service consumer and the supplier is subject to a contracted SLA.
- Cloud-hosted services where availability and support terms are governed by provider service agreements.

This standard does not apply to external services where the organization is the service provider to clients; those obligations are governed by customer contracts and applicable regulatory requirements.

---

## Requirements

### 1: Service catalogue and service classification

1.1 The Service Management Office must maintain a current service catalogue listing all in-scope IT services with their service classification, support tier, business criticality, and assigned Service Owner.

1.2 Services must be classified as one of the following tiers to determine the applicable SLA baseline:

| Tier | Classification | Definition |
| --- | --- | --- |
| Tier 1 | Mission Critical | Service failure causes immediate, material business interruption, regulatory breach, or safety impact. |
| Tier 2 | Business Essential | Service failure significantly impairs business operations or a material number of users within hours. |
| Tier 3 | Standard | Service failure has limited impact; workarounds are available or impact is contained to a subset of users. |
| Tier 4 | Non-Critical | Service failure has minimal impact; resolution can be deferred without business harm. |

1.3 Service classification must be reviewed annually and whenever a service's business criticality, regulatory status, or user base changes materially.

---

### 2: SLA establishment requirements

2.1 Every Tier 1 and Tier 2 service must have a documented and approved SLA before entering production. SLAs for Tier 3 and Tier 4 services are recommended but not mandatory.

2.2 Each SLA must specify:

- Service name, description, and scope.
- Service hours (planned availability window or 24/7 requirement).
- Availability target, expressed as a percentage of scheduled service hours.
- Response and resolution time targets by incident priority tier (P1 to P4).
- Planned maintenance window terms and notification requirements.
- Exclusions (events outside the service provider's control; force majeure; approved change windows).
- Service review and reporting frequency.
- Breach escalation path and compensatory action.
- SLA owner and approving authority.
- SLA effective date and scheduled review date.

2.3 SLAs must be approved by the Service Owner and acknowledged by the service consumer before activation.

2.4 Where a service is delivered by an external supplier, the supplier's contracted service terms must be reviewed against the internal SLA to confirm the supplier's obligations support the organization's service targets. Gaps must be identified and risk-accepted before service activation.

---

### 3: Operational level agreements

3.1 Where a service depends on support from one or more internal IT teams, an Operational Level Agreement must be established between the Service Owner and each supporting team.

3.2 Each OLA must define the internal team's support obligations, response targets, escalation contacts, and dependencies that underpin the service SLA.

3.3 OLA targets must be sufficient to support the upstream SLA target, accounting for handover and coordination time.

3.4 OLAs must be reviewed annually and whenever the service SLA is revised or the supporting team structure changes.

---

### 4: SLA monitoring and measurement

4.1 Service availability and performance must be measured continuously using the organization's monitoring toolset. Manual measurements are permitted only where automated monitoring is not feasible and must be documented as a known limitation.

4.2 The Service Management Office must produce a monthly SLA compliance report for all Tier 1 and Tier 2 services. The report must include:

- Achieved availability percentage versus target.
- Count of incidents by priority tier and SLA compliance rate per tier.
- SLA breaches: count, duration, and root cause summary.
- Open corrective actions from prior breaches.
- Trend comparison against the prior three months.

4.3 KPI results related to service levels must be recorded in the IT Operations KPI register (`operations/register-it-operations-kpis.md`) and reported to the CIO monthly.

4.4 SLA measurement methodology must be consistent month-to-month. Changes to measurement method require Service Owner approval and must be documented in the service record.

---

### 5: Breach detection and escalation

5.1 A breach occurs when a service availability or resolution target is not met within the measurement period and is not attributable to an approved exclusion.

5.2 The Service Management Office must detect and log breaches within one business day of the breach occurring.

5.3 Breach escalation must follow this path:

| Breach Type | Initial Escalation | Secondary Escalation | Governing Body |
| --- | --- | --- | --- |
| Single P1 SLA breach | Service Owner notified same day | CIO notified within 24 hours | CIO review within 5 business days |
| Three or more P2 breaches in a calendar month | Service Owner notified within 2 business days | CIO notified within 5 business days | Quarterly SLA review |
| Monthly availability target missed | Service Owner notified within 2 business days | CIO notified within 5 business days | CIO review within 10 business days |
| Availability below 99.0% for a Tier 1 service | CIO notified immediately | ERC notified within 3 business days | ERC review at next scheduled meeting |
| Three consecutive months of SLA breach (any tier) | CIO notified immediately | ERC notified within 3 business days | Formal service review mandated |

5.4 Every breach must result in a documented corrective action or a formal risk acceptance with a stated residual risk and review date.

---

### 6: SLA review

6.1 All SLAs must be reviewed at least annually. The review must assess:

- SLA compliance performance over the prior 12 months.
- Whether current targets remain appropriate given changes to business criticality, user base, technology, or regulatory obligations.
- Whether measurement methodology is still accurate and fit for purpose.
- Whether supplier SLAs continue to support internal targets.
- Open corrective actions from breaches.

6.2 The Service Owner and service consumer must formally acknowledge and approve any changes to SLA targets resulting from the review.

6.3 SLA reviews must be triggered outside the annual cycle when:

- A Tier 1 service experiences three consecutive months of availability below target.
- A major infrastructure change, migration, or cloud transition affects the service.
- A regulatory change introduces new availability, notification, or continuity obligations.
- A supplier contract is renegotiated or the supplier changes.

---

### 7: Supplier SLA governance

7.1 Where an external supplier is responsible for delivering or supporting a service, the organization must hold the supplier accountable to the contracted SLA through the supplier governance process defined in `supply-chain/standard-supplier-security-and-privacy-assurance.md`.

7.2 Supplier SLA performance must be reviewed at least quarterly. Material or repeated supplier SLA breaches must be escalated to the Supplier Owner and documented in the supplier risk register.

7.3 Where a supplier SLA breach causes an internal SLA breach, both must be recorded separately, and the root cause must identify whether the failure originated with the supplier.

7.4 Supplier contracts must include provisions for:

- Availability targets, measurement method, and reporting frequency.
- Breach notification and escalation requirements.
- Remediation timelines and service credits or other contractual remedies.
- Right to audit or request evidence of SLA performance.

---

### 8: Cloud provider service agreement management

8.1 Where cloud infrastructure or platform services underpin a Tier 1 or Tier 2 internal service, the relevant cloud provider service agreement must be reviewed to identify:

- Published availability SLA percentage and any service-level credits.
- Exclusions from the provider's SLA guarantee (shared responsibility model).
- Notification requirements for provider-side incidents.
- Geographic or zone-specific availability commitments.

8.2 Cloud provider SLA availability must be factored into the organization's internal SLA design. Where the cloud provider's SLA is lower than the internal service target, a compensating architecture (multi-region, failover, redundancy) must be documented.

8.3 Cloud provider service agreement terms must be reviewed when contracts are renewed and whenever a material architecture change affects the service.

---

### 9: Continuous improvement

9.1 Breach trends, repeat failures, and SLA performance patterns must be reviewed at the quarterly SLA governance meeting and fed into the ITIL 4 continual improvement cycle operated under the IT Service Management Framework.

9.2 Improvement actions arising from SLA reviews must be tracked in the Service Management Office's CAPA log and reported to the CIO.

9.3 The Service Management Office must maintain a register of all current SLAs and OLAs, including their version history, review dates, and approval status.

---

## Evidence requirements

Adopting organizations should retain:

- Approved SLA and OLA documents with version history and approval records.
- Monthly SLA compliance reports.
- Breach records and corrective action logs.
- Annual SLA review records with Service Owner acknowledgement.
- Supplier SLA performance reviews and escalation records.
- Cloud provider service agreement extracts used for architecture and SLA design.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 20000-1:2018 | §8.3 Service Level Management | SLA establishment, monitoring, and review |
| ITIL 4 | Service Level Management Practice | Service catalogue, SLA governance, continual improvement |
| COBIT 2019 | DSS02: Manage Service Requests and Incidents | Incident resolution targets and SLA governance |
| COBIT 2019 | APO09: Manage Service Agreements | Service agreement lifecycle |
| EU NIS 2 Directive | Business Continuity and Incident Reporting | Availability targets and notification timelines for significant incidents |

---

## Limitations

This standard provides a governance baseline. Adopting organizations must define their own service availability targets, breach thresholds, and escalation paths based on their service catalogue, customer contracts, regulatory obligations, and risk appetite. SLA targets in illustrative tables are placeholders only.

---

## Maintenance

This standard must be reviewed annually and upon material change to the service catalogue, IT sourcing model, regulatory obligations, or risk appetite. The Chief Information Officer is accountable for approving revisions.

---

**End of Document**
