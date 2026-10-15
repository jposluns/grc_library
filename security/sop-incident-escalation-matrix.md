# Incident Escalation Matrix

**Document Title:** Incident Escalation Matrix\
**Document Type:** SOP\
**Version:** 1.3.0\
**Date:** 2026-10-15\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`security/procedure-security-incident-response.md`](procedure-security-incident-response.md), [`resilience/procedure-security-incident-reporting-and-escalation.md`](../resilience/procedure-security-incident-reporting-and-escalation.md), [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md), [`resilience/plan-business-continuity-and-crisis-management.md`](../resilience/plan-business-continuity-and-crisis-management.md), [`operations/framework-it-service-management.md`](../operations/framework-it-service-management.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual or following significant organizational or contact change\
**Repository Path:** [`security/sop-incident-escalation-matrix.md`](sop-incident-escalation-matrix.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This SOP defines the incident escalation matrix for security incidents. It specifies severity levels, notification paths, timelines, and responsible parties to ensure that every incident is escalated to the right people at the right time. It is a companion document to the Incident Response Procedure and the Security Incident Reporting and Escalation Procedure. Those documents govern the full IR lifecycle; this SOP provides a quick-reference escalation guide for the SOC and IR team.

---

## Incident severity levels

| Level | Severity | Definition |
| --- | --- | --- |
| **P1** | Critical | Active or confirmed breach, ransomware deployment, data exfiltration, confirmed or suspected privileged account compromise, complete service outage caused or suspected to be caused by a security incident, or threat actor present in production environment. Each listed trigger is P1 whatever its scope. Otherwise, a complete service outage is an IT operations P1 handled under the [IT Service Management Framework](../operations/framework-it-service-management.md), sections "Service levels" and "1. Incident management" (under "Framework principles"), not the security incident-response procedure. |
| **P2** | High | Suspected breach, or confirmed security incident (other than a P1 trigger) with limited blast radius, potential data exposure, multi-system compromise, or active malware containment. Significant operational risk. |
| **P3** | Medium | Anomalous activity under investigation (a suspected breach is P2), policy violation, isolated malware, phishing with credential capture (P1 where the captured credential is privileged), or anomaly requiring containment. |
| **P4** | Low | Informational alert, false positive confirmed after investigation, or minor procedural violation with no data or system impact. |

**Meaning of "security incident".** In the P1 trigger "complete service outage caused or suspected to be caused by a security incident", "security incident" has the meaning of "information security incident" in ISO/IEC 27035-1:2023, clause 3.1.5: one or more related and identified information security events that can harm the organization's assets or compromise its operations. An information security event is an occurrence indicating a possible breach of information security or failure of controls (clause 3.1.4). A security incident can be deliberate, accidental (for example, caused by inadvertent human error) or environmental (for example, caused by fire or flood), and can include the unavailability of information (clause 4.1). Malicious activity is not required.

**Assessing whether an outage is security-related.** When the SOC learns of a complete service outage, it assesses whether a security incident caused or is suspected to have caused it. The test is whether the evidence indicates a possible breach of information security or a failure of information security controls, whatever the cause. An absence of signs of malicious activity is not, on its own, enough to rule out a security incident. The SOC reassesses as new information becomes available; if a security incident is later identified or suspected as the cause, the outage becomes a security P1 under this SOP.

---

## Escalation matrix

| Severity | Initial Detection | First Escalation (within) | Second Escalation (within) | Executive Notification |
| --- | --- | --- | --- | --- |
| **P1, Critical** | SOC / any staff | SOC Manager, immediate | CISO / CIO: immediate (per the incident response procedure, which notifies both immediately for all P1 incidents) | CEO and ELT: within 1 hour |
| **P2, High** | SOC | SOC Manager, within 30 minutes | CISO: within 1 hour | CIO: within 2 hours; CEO if significant |
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
| Data Protection Officer (DPO) | Email / collaboration platform | Phone |
| External IR Partner | Hotline | Partner portal |

Actual contact details (names, numbers, emails) are maintained in the confidential IR Contact Register held by the CISO. This SOP references roles only.

---

## Special escalation triggers

| Trigger | Additional Notifications Required |
| --- | --- |
| Confirmed or suspected PII data breach | Data Protection Officer (DPO); Legal Counsel; initiate regulatory notification assessment |
| Ransomware deployment | CEO, CFO, Board notification pathway; external IR partner engaged immediately |
| Threat actor in production environment | External IR partner activated; affected systems isolated immediately |
| Customer system or data impacted | Legal Counsel for contract obligations review; customer notification assessment |
| Sector-programme data involved (where the organization participates in a covered programme) | Sector-conditional role per the relevant sector annex (for example, a BASC Regional Compliance Officer for trade or customs data) notified per the annex's stated timeframe; see [`compliance/`](../compliance/) |
| Media or external parties involved | Communications Director and CEO manage all external statements |

---

## Out-of-hours escalation

For P1 incidents occurring outside business hours, the SOC must attempt phone contact with the CISO/CIO immediately. If unreachable within 15 minutes, escalate to the CEO.

On-call responsibility rotates as documented in the IR Contact Register. The P2 notification clocks in the escalation matrix must continue outside business hours: SOC Manager within 30 minutes, CISO within 1 hour, and CIO within 2 hours. Only non-urgent follow-up investigation and remediation may wait until business hours when containment is confirmed, provided monitoring continues and applicable response and reporting deadlines are met; if containment is not confirmed, the incident must be treated as P1.

---

## Escalation review

Any incident where escalation did not occur within the required timeline must be reviewed in the post-incident review. Escalation failures are documented in the CAPA Register and contribute to SOC performance metrics.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27035-1:2023 | Information security incident management, Part 1: Principles and process | Incident classification and escalation |
| NIST SP 800-61r3 | Incident Response Recommendations and Considerations for Cybersecurity Risk Management (CSF 2.0 Community Profile) | Escalation and notification guidance |
| COBIT 2019 | DSS02: Managed Service Requests and Incidents | Incident management governance |
| CSA CCM v4.1 | SEF-07: Incident Management and Response; SEF-03: Incident Response Plans; SEF-08: Security Breach Notification | Cloud incident escalation |

---

**End of Document**
