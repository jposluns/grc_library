# Incident Escalation Matrix

**Document Title:** Incident Escalation Matrix 
**Document Type:** SOP 
**Version:** 1.2.0 
**Date:** 2026-05-28 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Chief Information Officer 
**Related Documents:** [`security/procedure-security-incident-response.md`](procedure-security-incident-response.md), [`resilience/procedure-security-incident-reporting-and-escalation.md`](../resilience/procedure-security-incident-reporting-and-escalation.md), [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md), [`resilience/plan-business-continuity-and-crisis-management.md`](../resilience/plan-business-continuity-and-crisis-management.md) 
**Classification:** Public 
**Category:** Information Security 
**Review Frequency:** Annual or following significant organizational or contact change 
**Repository Path:** [`security/sop-incident-escalation-matrix.md`](sop-incident-escalation-matrix.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This SOP defines the incident escalation matrix for security incidents. It specifies severity levels, notification paths, timelines, and responsible parties to ensure that every incident is escalated to the right people at the right time. It is a companion document to the Incident Response Procedure and the Security Incident Reporting and Escalation Procedure. Those documents govern the full IR lifecycle; this SOP provides a quick-reference escalation guide for the SOC and IR team.

---

## Incident severity levels

| Level | Severity | Definition |
| --- | --- | --- |
| **P1** | Critical | Active or confirmed breach, ransomware deployment, data exfiltration, complete service outage, or threat actor present in production environment. Enterprise-wide or customer-impacting. |
| **P2** | High | Confirmed security incident with limited blast radius, potential data exposure, multi-system compromise, or active malware containment. Significant operational risk. |
| **P3** | Medium | Suspected incident under investigation, policy violation, isolated malware, phishing with credential capture, or anomaly requiring containment. |
| **P4** | Low | Informational alert, false positive confirmed after investigation, or minor procedural violation with no data or system impact. |

---

## Escalation matrix

| Severity | Initial Detection | First Escalation (within) | Second Escalation (within) | Executive Notification |
| --- | --- | --- | --- | --- |
| **P1, Critical** | SOC / any staff | SOC Manager, immediate | CISO / CIO: within 30 minutes | CEO and ELT: within 1 hour |
| **P2, High** | SOC | SOC Manager, within 30 minutes | CISO: within 2 hours | CIO: within 2 hours; CEO if significant |
| **P3, Medium** | SOC | IR Coordinator, within 4 hours | CISO: within 24 hours if not resolved | CIO: if unresolved after 24 hours |
| **P4, Low** | SOC | IR Coordinator, within 24 hours | None required unless escalation triggered | None unless pattern identified |

---

## Notification method

| Recipient | Primary Contact Method | Backup Method |
| --- | --- | --- |
| SOC Manager | Collaboration platform / phone | Email |
| CISO | Phone / collaboration platform | Email + SMS |
| CIO | Phone | Email + SMS |
| CEO | Phone | Email + personal mobile |
| Legal Counsel | Email / phone | Collaboration platform |
| Privacy Officer / DPO | Email / collaboration platform | Phone |
| External IR Partner | Hotline | Partner portal |

Actual contact details (names, numbers, emails) are maintained in the confidential IR Contact Register held by the CISO. This SOP references roles only.

---

## Special escalation triggers

| Trigger | Additional Notifications Required |
| --- | --- |
| Confirmed or suspected PII data breach | Privacy Officer / DPO; Legal Counsel; initiate regulatory notification assessment |
| Ransomware deployment | CEO, CFO, Board notification pathway; external IR partner engaged immediately |
| Threat actor in production environment | External IR partner activated; affected systems isolated immediately |
| Customer system or data impacted | Legal Counsel for contract obligations review; customer notification assessment |
| BASC or customs data involved | Regional BASC Compliance Officers notified within 2 hours |
| Media or external parties involved | Communications Director and CEO manage all external statements |

---

## Out-of-hours escalation

For P1 incidents occurring outside business hours, the SOC must attempt phone contact with the CISO/CIO immediately. If unreachable within 15 minutes, escalate to the CEO.

On-call responsibility rotates as documented in the IR Contact Register. Out-of-hours P2 incidents may wait until business hours if containment is confirmed; if containment is not confirmed, treat as P1.

---

## Escalation review

Any incident where escalation did not occur within the required timeline must be reviewed in the post-incident review. Escalation failures are documented in the CAPA Register and contribute to SOC performance metrics.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27035:2023 | Information Security Incident Management | Incident classification and escalation |
| NIST SP 800-61r3 | Computer Security Incident Handling Guide | Escalation and notification guidance |
| COBIT 2019 | DSS02: Manage Service Requests and Incidents | Incident management governance |
| CSA CCM v4.1 | SEF-02: Incident Management | Cloud incident escalation |

---

**End of Document**
