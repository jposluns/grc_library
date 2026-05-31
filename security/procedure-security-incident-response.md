# Security Incident Response Procedure

**Document Title:** Security Incident Response Procedure\
**Document Type:** Procedure\
**Version:** 1.3.4\
**Date:** 2026-05-28\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/standard-logging-and-monitoring.md`](standard-logging-and-monitoring.md), [`security/standard-privileged-access-management.md`](standard-privileged-access-management.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`operations/standard-production-security-requirements.md`](../operations/standard-production-security-requirements.md), [`resilience/procedure-cross-domain-incident-coordination.md`](../resilience/procedure-cross-domain-incident-coordination.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material threat, framework, or regulatory change\
**Repository Path:** [`security/procedure-security-incident-response.md`](procedure-security-incident-response.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose and scope

### 1.1 Purpose

This procedure defines the end-to-end lifecycle for managing information security incidents: from initial detection and triage through containment, eradication, recovery, regulatory notification, and post-incident review. It establishes mandatory roles, response timeframes, evidence-handling requirements, and escalation obligations that apply to all confirmed and suspected security incidents.

The procedure is aligned to ISO/IEC 27035 (Information Security Incident Management), NIST SP 800-61 Rev 3 (Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile), COBIT 2019 DSS02, and CSA CCM v4.1 SEF-01 through SEF-10.

### 1.2 Scope

This procedure applies to:

- All employees, contractors, and third parties who detect, respond to, or are affected by a security incident.
- All systems, applications, endpoints, networks, cloud environments, identities, and data under organisational control. Sector-specific overlays (e.g., BASC-certified trade and customs systems, where the organisation participates in that programme; PCI DSS-scope systems; OT/ICS) apply additional requirements documented in the relevant sector annex.
- All incident types including but not limited to: unauthorized access, malware or ransomware, data exfiltration, privilege compromise, denial of service, supply chain compromise, privacy breaches, and AI system security events.

---

## 2. Governance

### 2.1 Roles and responsibilities

| Role | Responsibilities |
| --- | --- |
| **Incident Commander** | Assumes overall command and decision-making authority for P1 and P2 incidents. Approves containment actions, isolation decisions, and external communications. No system shall be isolated or reimaged without the Incident Commander's direction. |
| **Chief Information Security Officer (CISO)** | Accountable for the incident response programme. Notified immediately for all P1 incidents and within 4 hours for P2. Authorizes IR partner engagement. Oversees regulatory notification decisions. |
| **Chief Information Officer (CIO)** | Notified immediately for P1 incidents. Provides executive oversight and approves communications to affected customers, partners, and regulators. |
| **Security Operations Centre (SOC)** | Operates SIEM and endpoint monitoring. Performs initial triage, severity classification, and evidence preservation. Executes containment and eradication steps under Incident Commander direction. Maintains timestamped logs of all IR actions. |
| **IT Operations** | Supports containment and recovery activities. Executes technical remediation steps as directed by the Incident Commander. |
| **Legal Counsel** | Advises on regulatory notification obligations (for example, GDPR, CPPA, PIPL; plus sector-programme regulatory obligations such as BASC where the organisation participates). Provides guidance on evidence preservation, litigation hold, and third-party disclosure. |
| **IR Partner** | External incident response partner engaged by the CISO for P1 incidents. Contact details are maintained in the operational state register. |
| **Privacy Lead / Acting DPO** | Assesses privacy impact of incidents involving personal data. Coordinates regulatory breach notifications under GDPR, CPPA, and PIPL. |
| **All Employees** | Responsible for immediately reporting any suspected security incident to the SOC or security operations team. No silent remediation is permitted. |

Sector-conditional roles (for example, a BASC Regional Compliance Officer who is notified for any incident affecting trade, customs, or cargo systems and coordinates sector-programme reporting and corrective actions) apply where the organisation participates in a covered sector programme; see [`compliance/`](../compliance/).

### 2.2 Incident commander authority

The Incident Commander has authority to:

- Direct all technical and operational response activities.
- Approve or defer system isolation, service suspension, or credential revocation.
- Engage external forensic or IR support.
- Authorize or restrict communications to third parties during an active incident.

During a declared P1 incident, the Incident Commander is the CIO or CISO unless delegated in writing.

---

## 3. Incident severity classification

### 3.1 Severity levels

| Severity | Criteria | Examples | Response SLA | Escalation |
| --- | --- | --- | --- | --- |
| **P1: Critical** | Confirmed active breach, ransomware in execution, active data exfiltration, or confirmed privileged account compromise. | Ransomware executing on production systems; confirmed exfiltration of customer PII or trade data; domain administrator credential confirmed compromised; active threat actor in the environment. | Immediate (within 15 minutes of detection) | Incident Commander, CISO, and CIO notified immediately. IR partner notified by CISO. All IR actions logged with timestamps. |
| **P2: High** | Suspected breach or significant security event with potential for serious impact; malware detected but not yet confirmed active; significant control failure. | Malware detected on a critical server; suspicious lateral movement observed in SIEM; single privileged account compromise suspected; failed restore test on production backup. | 4-hour initial response | CISO notified within 1 hour. Incident Commander assigned. |
| **P3: Medium** | Anomalous activity requiring investigation; policy violation with potential security significance; isolated endpoint compromise. | Single endpoint malware detection; user account exhibiting anomalous access patterns; unauthorized software detected on production system; failed authentication threshold exceeded. | Same-day (within 8 business hours) | SOC lead notified. Security team investigation initiated. |
| **P4: Low** | Policy violations; failed security scans; informational security events with no confirmed harm. | Failed patch scan; acceptable use policy violation; expired certificate on non-critical system; minor misconfiguration with no exploitation evidence. | Within 5 business days | Assigned to SOC queue. Standard change or remediation process. |

### 3.2 Severity escalation

Severity classification must be reassessed as new information becomes available. Any analyst may escalate severity upward without management approval. Downgrading severity from P1 requires Incident Commander approval. The initial classification is recorded and retained even if subsequently revised.

---

## 4. Detection and triage

### 4.1 Detection sources

Security incidents may be detected from any of the following sources:

| Source | Examples |
| --- | --- |
| SIEM alerts | Brute-force authentication, privileged access outside change windows, mass file encryption, large outbound data transfers, emergency account usage, PAM bypass, trust and directory changes. |
| Endpoint detection and response (EDR) | Malware detection, suspicious process execution, lateral movement indicators, ransomware behaviour patterns. |
| Vulnerability scanners | Critical vulnerability actively exploited in the environment. |
| User reports | Employee or contractor reporting suspicious activity, phishing, unauthorized access, or missing data. |
| Third-party or supplier notification | Supplier reporting a breach affecting shared systems or data. |
| Threat intelligence | External notification of credentials in breach databases; indicators of compromise matching organisational assets. |
| Audit and compliance reviews | Control failures discovered during audit that indicate an active or historical breach. |
| Sector-programme monitoring | Anomalies flagged by sector-programme monitoring where the organisation participates (e.g., BASC for cargo, customs, and trade systems; PCI DSS file-integrity monitoring; OT historian anomalies). |

### 4.2 Triage process

Upon receipt of an alert or report, the SOC analyst shall:

1. **Validate** the event: confirm it is not a false positive by corroborating evidence from at least one additional source.
2. **Classify severity** using the criteria in Section 3.
3. **Preserve evidence immediately**: capture log snapshots, SIEM query results, endpoint telemetry, and network flows before any containment action is taken. Evidence preservation takes priority over service recovery in the first hour.
4. **Assign an Incident ID** and open a formal incident record in the ticketing system.
5. **Notify** the appropriate roles per Section 3.1 escalation requirements.
6. **Brief the Incident Commander** with: what is known, what systems and data are affected, what the suspected attack vector is, and what immediate containment options are available.

### 4.3 Triage record fields

| Field | Required Content |
| --- | --- |
| Incident ID | Unique identifier |
| Detection timestamp | UTC timestamp of initial detection |
| Detection source | SIEM, EDR, user report, third party, etc. |
| Initial severity | P1 / P2 / P3 / P4 |
| Affected systems | Hostnames, IPs, cloud resources |
| Affected data classes | PII, trade data, credentials, etc. |
| Suspected vector | Phishing, vulnerability exploit, insider, etc. |
| Evidence preserved | List of artefacts captured |
| Analyst name and role | Identifying the triage analyst |
| Escalation actions | Roles notified and timestamps |

---

## 5. Containment, eradication, and recovery

### 5.1 Containment principles

- **Do not isolate or reimage systems without direction from the Incident Commander.** Premature isolation may destroy volatile evidence or alert the threat actor.
- **Evidence preservation takes priority over service recovery in the first hour.** Capture memory dumps, running process lists, active network connections, and relevant log exports before any containment action that could alter system state.
- All containment actions must be logged with the UTC timestamp, the identity of the person taking the action, and the Incident Commander's authorization.

### 5.2 Containment phases

| Phase | Actions | Authorization |
| --- | --- | --- |
| **Short-term containment** | Network segmentation of affected systems; block suspected attacker IP ranges at the firewall; disable suspected compromised credentials; revoke active sessions. | Incident Commander |
| **Evidence capture** | Memory acquisition; disk image of affected systems; export of relevant SIEM queries; preservation of authentication logs and EDR telemetry. | SOC, under Incident Commander direction |
| **Long-term containment** | Maintain affected systems in a contained state while investigation continues; deploy enhanced monitoring; restrict privileged access to the affected environment. | Incident Commander |

### 5.3 Eradication

Once the scope of compromise is confirmed, the SOC and IT Operations shall:

1. Remove all identified malware, persistence mechanisms, backdoors, and unauthorized accounts.
2. Revoke and rotate all credentials that were or may have been exposed, including service accounts, API keys, and certificates.
3. Patch or mitigate the vulnerability or control weakness that allowed the incident to occur.
4. Validate eradication with a follow-on scan or forensic review before proceeding to recovery.

### 5.4 Recovery

1. Restore affected systems from known-good backups or clean-rebuilt images, verified against integrity hashes.
2. Verify that all SIEM alert categories and monitoring rules are operational before returning systems to production.
3. Monitor restored systems with enhanced logging and alerting for a minimum of 14 days post-recovery.
4. Obtain formal sign-off from the Incident Commander and the relevant System Owner before resuming normal operations.
5. Document the return-to-service date and the basis for confirming that the threat has been eradicated.

---

## 6. Regulatory notification

### 6.1 Notification obligations summary

| Regulation | Trigger | Notification Deadline | Notifying Authority |
| --- | --- | --- | --- |
| **GDPR (EU)** | Confirmed breach of personal data of EU data subjects with likely risk to individuals | 72 hours from confirmation | CISO / Privacy Lead to relevant supervisory authority; individuals where high risk |
| **CPPA (Canada)** | Confirmed breach of personal information with real risk of significant harm | As soon as feasible (72-hour target) | CIO (acting DPO) to Privacy Commissioner of Canada |
| **Quebec Law 25** | Confirmed breach of personal information with serious risk of injury | 72 hours to Commission d'accès à l'information | CIO (acting DPO) |
| **PIPL (China)** | Confirmed breach of personal data of China data subjects | Immediately / without delay | CISO / Privacy Lead to relevant authority |

Sector-programme notification obligations (for example, BASC requirements for trade, cargo, or customs anomalies meeting the BASC breach threshold) apply where the organisation participates in a covered sector programme. The relevant sector annex states the trigger, timeframe, and notification path; see [`compliance/`](../compliance/).

### 6.2 GDPR and CPPA notification process

1. The Privacy Lead assesses whether the incident involves personal data and whether the risk threshold for notification is met.
2. Legal Counsel reviews and approves notification content before submission.
3. The CIO (acting DPO) submits the regulatory notification and retains a copy in the incident record.
4. If notification cannot be completed within the regulatory window, the delay must be documented with reasons, and partial information submitted where permitted.

### 6.3 Sector-programme anomalies

Where the organisation participates in a sector programme that defines elevated-trigger anomaly categories (for example, BASC for cargo, customs, or trade systems with a 2-hour initial response SLA for unauthorized access to shipment data, tampering with customs records, or suspected cargo integrity compromise), the corresponding sector annex states the triage timeframe, the sector-conditional role notified, and the supplementary documentation maintained. See [`compliance/`](../compliance/).

### 6.4 Notification confidentiality

Regulatory notifications are Restricted classification materials. Content shall not be shared externally beyond regulators, Legal, the CIO, and the CISO without written authorization. No public statements regarding the incident shall be made without CIO approval and coordination with Legal Counsel.

---

## 7. Post-incident review

### 7.1 PIR requirements

| Severity | PIR Required | Deadline |
| --- | --- | --- |
| P1: Critical | Mandatory | Within 5 business days of incident closure |
| P2: High | Mandatory | Within 5 business days of incident closure |
| P3: Medium | Required | Within 15 business days |
| P4: Low | At SOC discretion | Next monthly review cycle |

### 7.2 PIR process

The PIR shall be conducted by the Incident Commander (for P1/P2) or SOC lead (for P3/P4) and shall address:

1. **Timeline reconstruction**: complete chronological sequence from initial indicator to closure, with timestamps.
2. **Root cause analysis**: the fundamental control failure, vulnerability, or process gap that enabled the incident.
3. **Detection effectiveness**: how the incident was detected; whether automated controls fired correctly; mean time to detect (MTTD).
4. **Containment effectiveness**: adequacy and timeliness of containment actions.
5. **Recovery effectiveness**: time to restore services; completeness of eradication.
6. **Regulatory and legal compliance**: whether all notification obligations were met within required timeframes.
7. **Control gaps**: specific controls that failed, were absent, or were insufficient.
8. **Corrective actions**: named owners, deadlines, and tracking mechanism for each gap.
9. **Risk register update**: confirm whether existing risks require re-scoring or new risks require addition.

### 7.3 PIR output

The PIR report is a Restricted document. It is provided to the CISO, CIO, and Internal Audit. Corrective actions are tracked in the security remediation register and reported at the quarterly security governance review.

---

## 8. Evidence and documentation requirements

### 8.1 Evidence preservation

All evidence collected during an incident must be:

- Captured as close to the time of discovery as possible.
- Stored in a tamper-evident location (WORM storage or write-protected media) separate from the affected systems.
- Documented in an evidence index with: item description, source, collection method, UTC timestamp of collection, and custodian identity.
- Retained for a minimum of 7 years, or longer if subject to litigation hold or regulatory request.

The following evidence classes must be preserved for any P1 or P2 incident:

| Evidence Class | Description |
| --- | --- |
| SIEM logs | Relevant queries and exports from the detection period |
| EDR telemetry | Process trees, network connections, file events for affected hosts |
| Authentication logs | Successful and failed authentication events for implicated accounts |
| Network flow data | NetFlow or equivalent for suspected C2 or exfiltration traffic |
| Memory dump | Volatile memory image from affected live systems where feasible |
| Disk image | Forensic image of affected systems where justified by incident severity |
| Containment records | Timestamped log of all containment actions taken |
| Communications | All internal communications related to the incident, including approvals |

### 8.2 Mandatory incident record fields

Every incident, regardless of severity, must have a completed incident record containing:

| Field | Description |
| --- | --- |
| Incident ID | Unique identifier |
| Severity (initial and final) | P1 to P4 with rationale |
| Detection timestamp | UTC |
| Detection source | SIEM, EDR, user, external, etc. |
| Affected systems and data | Hostnames, data classifications, record count where known |
| Timeline | Key events with UTC timestamps |
| Containment actions | What was done, by whom, when, and under whose authorization |
| Eradication actions | Steps taken to remove the threat |
| Recovery actions | Steps taken to restore service |
| Regulatory notifications | Regulations triggered, dates notified, references |
| Evidence index | List of artefacts preserved |
| PIR completion date | Date PIR was completed |
| Corrective actions | Summary list with owners and deadlines |
| Closure approval | Name, role, and date |

---

## 9. Metrics

The SOC shall track and report the following metrics at the monthly security operations review and quarterly governance review:

| Metric | Definition | Target |
| --- | --- | --- |
| **Mean Time to Detect (MTTD)** | Time from incident onset to first detection signal | P1/P2: < 1 hour; P3: < 4 hours |
| **Mean Time to Initiate (MTTI)** | Time from detection to formal incident declaration and Incident Commander assignment | P1: < 15 minutes; P2: < 1 hour |
| **Mean Time to Contain (MTTC)** | Time from incident declaration to confirmed containment | P1: < 4 hours; P2: < 8 hours |
| **Mean Time to Recover (MTTR)** | Time from incident declaration to confirmed service restoration and closure | P1: < 24 hours; P2: < 72 hours |
| **SLA Adherence** | Percentage of incidents where notification and response SLAs were met | ≥ 95% |
| **Regulatory Notification Timeliness** | Percentage of notifiable breaches where regulatory notification was submitted within the required window | 100% |
| **PIR Completion Rate** | Percentage of P1/P2 incidents with PIR completed within 5 business days | ≥ 95% |
| **Repeat Incidents** | Number of incidents sharing the same root cause as a prior incident in the past 12 months | Target: 0 for P1/P2 root causes |

---

## 10. Framework alignment

| Control Area | ISO/IEC 27035 | NIST SP 800-61 | ISO/IEC 27001:2022 | COBIT 2019 | CSA CCM v4.1 |
| --- | --- | --- | --- | --- | --- |
| Incident management policy and planning | Clause 5 | §2.3, §3.1 | A.5.24 | DSS02.01 | SEF-01, SEF-02 |
| Detection and reporting | Clause 6.3 | §3.2 | A.5.25 | DSS02.02 | SEF-03 |
| Triage and classification | Clause 6.4 | §3.2 | A.5.25 | DSS02.03 | SEF-04 |
| Containment and evidence preservation | Clause 6.5 | §3.3 | A.5.26 | DSS02.04 | SEF-05 |
| Eradication and recovery | Clause 6.6 | §3.4 | A.5.26 | DSS02.05 | SEF-06 |
| Post-incident review | Clause 7 | §3.5 | A.5.27 | DSS02.06 | SEF-07 |
| Evidence handling | Clause 6.5 | §3.3 | A.5.28 | DSS02.04 | SEF-08 |
| Incident response metrics | Clause 8 | §4 | A.5.35 | MEA01 | SEF-09, SEF-10 |

---

## Licence

This document is released under the **CC BY-SA 4.0** CC BY-SA 4.0 licence. To the extent possible under law, all copyright and related rights are waived. See `LICENSE` in the repository root.

---

**End of Document**
