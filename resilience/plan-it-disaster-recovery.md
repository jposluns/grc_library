# IT Disaster Recovery Plan

**Document Title:** IT Disaster Recovery Plan  
**Document Type:** Plan  
**Version:** 0.1.0  
**Date:** 2026-05-27  
**Owner:** Chief Information Officer  
**Approving Authority:** Chief Information Officer  
**Related Documents:** [`resilience/standard-business-continuity-and-disaster-recovery.md`](standard-business-continuity-and-disaster-recovery.md), [`resilience/business-continuity-and-crisis-management.md`](business-continuity-and-crisis-management.md), [`resilience/procedure-continuity-and-recovery-testing.md`](procedure-continuity-and-recovery-testing.md), [`security/procedure-incident-response.md`](../security/procedure-incident-response.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md)  
**Classification:** Public  
**Category:** Resilience  
**Review Frequency:** Annual or following any major infrastructure change or DR exercise  
**Repository Path:** [`resilience/plan-it-disaster-recovery.md`](plan-it-disaster-recovery.md)  
**Confidentiality:** Public  
**Licence:** CC0 1.0 Universal  

---

> **Document Status — Provisional:** This document is a provisional draft added to the GRC library in May 2026. Content is based on standard frameworks and best-practice assumptions, incorporating lessons learned from a prior security incident. It has not yet been reviewed or formally approved by all stakeholders. It must not be used as the basis for operational decisions or compliance claims until reviewed, updated, and approved. Target formal review: Q3 2026.

---

## Purpose

This plan defines the system-specific recovery procedures, RTO and RPO targets, and runbook references for IT Disaster Recovery (DR). It is a companion document to the BC/DR Standard and the Business Continuity and Crisis Management Plan, which govern the broader BC/DR framework. This plan focuses on IT system recovery execution rather than business continuity governance. Lessons learned from a prior security incident — which required phased recovery over approximately 30 days — directly informed the structure and priorities in this document.

---

## Scope

1. Applies to all IT systems and infrastructure supporting organisational operations, including production systems in the primary data centre and cloud platform environments.
2. Covers recovery of virtual infrastructure, identity systems, data systems, integration layer, and reporting services.
3. Covers the current infrastructure programme environment model (DEV / TEST / PROD) as it is brought into service.

---

## Governance and Accountability

| Role | Responsibility |
| --- | --- |
| **CIO** | Authorises DR plan activation and approves return to normal operations. |
| **CISO** | Ensures security controls are re-enabled before production services are restored. Approves formal "Return to Normal Operations" sign-off. |
| **IT Operations / Infrastructure Team** | Executes system recovery procedures; validates integrity before service restoration. |
| **Business Continuity Manager (BCM)** | Coordinates DR activities, tracks recovery milestones, and provides status updates to leadership. |
| **Integration / Development Team** | Restores and validates integration layer and customer-specific connections. |

---

## RTO and RPO Targets

| System / Service Tier | Examples | RTO | RPO |
| --- | --- | --- | --- |
| **Tier 1 — Mission Critical** | Core ERP, on-premises directory service, enterprise identity provider, production virtual infrastructure | 4 hours | 1 hour |
| **Tier 2 — Essential** | Email platform, collaboration platform, financial systems, HR management system | 24 hours | 4 hours |
| **Tier 3 — Important** | Reporting and analytics, departmental tools, collaboration and file storage platforms | 72 hours | 24 hours |
| **Tier 4 — Non-Critical** | Non-production environments, internal knowledge bases | 7 days | 72 hours |

Specific per-system RTO/RPO targets for ongoing system modernisation workstreams will be incorporated into this plan upon project completion.

---

## Recovery Infrastructure

**Primary site:** On-premises hypervisor infrastructure in the primary data centre.

**Recovery platform:** A cloud-based site recovery service replicates production virtual machines to the cloud platform and enables failover within defined RTO windows. Failback to the primary data centre occurs after the primary site is restored and validated.

**Cloud-native services:** Cloud productivity platform services and enterprise identity provider recover according to the cloud provider's platform SLAs and the organisation's configuration backup procedures. These services do not require replication-based DR.

---

## Phased Recovery Sequence

Recovery follows the sequence demonstrated and refined during the prior security incident response and post-incident review.

| Phase | Target | Description |
| --- | --- | --- |
| **Phase 1 — Identity and Infrastructure** | Within 4 hours | Restore on-premises directory service and enterprise identity provider. Initiate cloud-based site recovery failover for Tier 1 systems. Validate network connectivity and firewall state. Confirm all attacker access removed and security controls re-enabled. |
| **Phase 2 — Core Production Systems** | Within 2–5 days | Restore ERP, core application servers, and databases. Validate data integrity against last clean backup. Confirm cloud productivity platform services are operational and secure. |
| **Phase 3 — Integration Layer** | Within 7–10 days | Restore integration middleware and EDI integrations. Validate data integrity for integration pipeline. Initiate customer re-onboarding with integrity verification before reconnection. |
| **Phase 4 — Reporting and Full Operations** | Within 30 days | Restore reporting services, data warehouse, and analytics platforms. Complete customer-specific integration restoration. Confirm full operational recovery. |

---

## Pre-Conditions for Service Restoration

No production system is restored to service until the following conditions are confirmed:

- Attacker tooling and access paths removed and independently verified.
- All compromised credentials rotated.
- Endpoint protection in enforcement mode on all restored systems.
- Security information and event management (SIEM) log forwarding confirmed active.
- CISO sign-off obtained.

---

## Backup and Restore Requirements

All Tier 1 and Tier 2 systems must have:

- Automated daily backups with off-site or cloud copy.
- Backup integrity verified monthly via restore test.
- Backup gap not exceeding 24 hours for Tier 1 and 4 hours for time-critical data.

Backup status is reported monthly to the CISO. Any backup gap exceeding the defined RPO is treated as a P2 risk event and escalated for immediate remediation.

---

## Runbook References

System-specific recovery runbooks are maintained in the IT Operations Documentation Framework and the IT/Operations space. Runbooks must be reviewed and tested at minimum annually. Runbook currency (last tested date) is tracked in the CMDB against each in-scope system. Runbooks not tested within 13 months are flagged as non-compliant.

---

## DR Testing

DR testing requirements follow the Continuity and Recovery Testing and Exercising Procedure:

- Tier 1 systems must be included in the annual full recovery test.
- Cloud-based site recovery failover tests for production-critical virtual machines must be conducted at minimum annually.
- Test results, recovery time achieved versus RTO target, and any identified gaps are documented and reported to the CIO and ERC.
- Failures and gaps are logged in the CAPA Register.

---

## Lessons Learned: Prior Security Incident

A ransomware incident resulted in approximately a 30-day recovery window. Key lessons incorporated into this plan include:

- Hypervisor infrastructure requires explicit DR coverage via a cloud-based site recovery service.
- Identity recovery (on-premises directory service) must be the first recovery step.
- The integration layer recovery timeline (approximately 14 days) is the longest single phase and requires dedicated resourcing.
- Legacy data environments with backup gaps materially increase recovery complexity and must be eliminated.
- Evidence of attacker removal must be confirmed before any system is restored to production.

---

## Framework Alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO 22301:2019 | Business Continuity Management Systems | DR governance and testing |
| COBIT 2025 | DSS04 — Manage Continuity | IT continuity management |
| NIST SP 800-34r1 | Contingency Planning Guide for Federal Information Systems | DR plan structure |
| CSA CCM v5 | BCR-01 through BCR-07 — Business Continuity and Resilience | Cloud resilience controls |

---

**End of Document**
