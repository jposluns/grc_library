# Security Incident Response Procedure

**Document Title:** Security Incident Response Procedure\
**Document Type:** Procedure\
**Version:** 1.11.9\
**Date:** 2026-11-01\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/standard-logging-and-monitoring.md`](standard-logging-and-monitoring.md), [`security/standard-privileged-access-management.md`](standard-privileged-access-management.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`operations/standard-production-security-requirements.md`](../operations/standard-production-security-requirements.md), [`resilience/procedure-cross-domain-incident-coordination.md`](../resilience/procedure-cross-domain-incident-coordination.md), [`governance/standard-emergency-authority.md`](../governance/standard-emergency-authority.md), [`security/standard-monitoring-integrity-and-coverage.md`](standard-monitoring-integrity-and-coverage.md), [`security/standard-soc-operating-model.md`](standard-soc-operating-model.md), [`security/sop-incident-escalation-matrix.md`](sop-incident-escalation-matrix.md), [`operations/framework-it-service-management.md`](../operations/framework-it-service-management.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material threat, framework, or regulatory change\
**Repository Path:** [`security/procedure-security-incident-response.md`](procedure-security-incident-response.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customization guidance.

---

## 1. Purpose and scope

### 1.1 Purpose

This procedure defines the end-to-end lifecycle for managing information security incidents: from initial detection and triage through containment, eradication, recovery, regulatory notification, and post-incident review. It establishes mandatory roles, response timeframes, evidence-handling requirements, and escalation obligations that apply to all confirmed and suspected security incidents.

The procedure is aligned to the ISO/IEC 27035 series (Information security incident management) by part: ISO/IEC 27035-1:2023 (Part 1: Principles and process), ISO/IEC 27035-2:2023 (Part 2: Guidelines to plan and prepare for incident response) and ISO/IEC 27035-3:2020 (Part 3: Guidelines for ICT incident response operations). It is also aligned to NIST SP 800-61 Rev. 3 (Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile), COBIT 2019 DSS02, and the CSA CCM v4.1 Security Incident Management, E-Discovery, & Cloud Forensics (SEF) domain.

### 1.2 Scope

This procedure applies to:

- All employees, contractors, and third parties who detect, respond to, or are affected by a security incident.
- All systems, applications, endpoints, networks, cloud environments, identities, and data under organizational control. Sector-specific overlays (e.g., BASC-certified trade and customs systems, where the organization participates in that programme; PCI DSS-scope systems; OT/ICS) apply additional requirements documented in the relevant sector annex.
- All incident types including but not limited to: unauthorized access, malware or ransomware, data exfiltration, privilege compromise, denial of service, supply chain compromise, privacy breaches, and AI system security events.

---

## 2. Governance

### 2.1 Roles and responsibilities

| Role | Responsibilities |
| --- | --- |
| **Incident Commander** | Assumes overall command and decision-making authority for P1 and P2 incidents. Approves containment actions, isolation decisions, and external communications other than regulatory notifications, which route per section 6. No system must be isolated or reimaged without direction from the Incident Commander or, for P3 and P4 where no Incident Commander is assigned, the SOC lead, or, for P1 and P2 before an Incident Commander is assigned, the interim technical authority (section 2.2). The Incident Commander or, for P3 and P4 where no Incident Commander is assigned, the SOC lead, or, for P1 and P2 before an Incident Commander is assigned, the interim technical authority (section 2.2) notifies Legal Counsel at once when an investigation under this procedure treats a device, its user, or its data as evidence, and again when it no longer does, so the designation is known to the hold check in [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) §5.2.1 rule 2. |
| **Chief Information Security Officer (CISO)** | Accountable for the incident response programme. Notified immediately for all P1 incidents and within 1 hour for P2. For P1 and P2, is the interim technical authority, or relies on a pre-authorized duty delegate as that authority, until an Incident Commander is assigned (section 2.2). Where it relies on a duty delegate, delegates that authority in writing and makes sure the duty delegate is named in the IR Contact Register (section 2.2). Authorizes IR partner engagement. Coordinates with the DPO on regulatory notification, and submits a China Cybersecurity Law report on an incident that involves no personal data (section 6.2). |
| **Chief Information Officer (CIO)** | Notified immediately for P1 incidents. Provides executive oversight and approves communications to affected customers and partners; the regulatory notifications that section 6.1 assigns (the personal data breach notifications and the China Cybersecurity Law report) route through the DPO, or the CISO for a China Cybersecurity Law report on an incident that involves no personal data, with Legal Counsel content approval per the notification steps in this procedure. Any other regulatory notification is Legal Counsel's unless the applicable domain procedure assigns it elsewhere ([`resilience/procedure-cross-domain-incident-coordination.md`](../resilience/procedure-cross-domain-incident-coordination.md), section "Joint command structure", Legal Lead row). |
| **Security Operations Centre (SOC)** | Operates SIEM and endpoint monitoring. Performs initial triage, severity classification, and evidence preservation. Executes containment and eradication steps under direction from the Incident Commander or, for P3 and P4 where no Incident Commander is assigned, the SOC lead, or, for P1 and P2 before an Incident Commander is assigned, the interim technical authority (section 2.2). Maintains timestamped logs of all IR actions. |
| **SOC lead** | The SOC Manager, or a duty deputy the SOC Manager explicitly designates in the SOC on-call rota ([`security/standard-soc-operating-model.md`](standard-soc-operating-model.md) section 4 for the definition and section 10 for the rota). The SOC lead's incident authority and duties are only those given to the SOC lead in sections 2.1, 2.2, 5.1, 5.2, 5.4 and 7.2 of this procedure, and in [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md) section 8. Those sections hold the full list; the SOC lead holds no other Incident Commander authority. The SOC lead holds that authority and those duties only while a security P3 or P4 incident has no Incident Commander assigned; once one is assigned, that Incident Commander acts instead. This includes the section 7.2 post-incident review: for a security P3 or P4 incident that has one under section 7.1, the SOC lead conducts it only where no Incident Commander was assigned. |
| **IT Operations** | Supports containment and recovery activities. Executes technical remediation steps as directed by the Incident Commander or, for P3 and P4 where no Incident Commander is assigned, the SOC lead, or, for P1 and P2 before an Incident Commander is assigned, the interim technical authority (section 2.2). |
| **Legal Counsel** | Advises on regulatory notification obligations (for example, GDPR, PIPEDA, PIPL, the China Cybersecurity Law; plus sector-programme regulatory obligations such as BASC where the organization participates). Provides guidance on evidence preservation, litigation hold, and third-party disclosure. |
| **IR Partner** | External incident response partner engaged by the CISO for P1 incidents. Contact details are maintained in the operational state register. |
| **Data Protection Officer (DPO)** | Assesses privacy impact of incidents involving personal data. Coordinates regulatory breach notifications under GDPR, PIPEDA, Quebec Law 25, PIPL, and the China Cybersecurity Law where the incident involves personal data (the CISO reports an incident that involves none, section 6.2). |
| **All Employees** | Responsible for immediately reporting any suspected security incident to the SOC or security operations team. No silent remediation is permitted. |

Sector-conditional roles (for example, a BASC Regional Compliance Officer who is notified for any incident affecting trade, customs, or cargo systems and coordinates sector-programme reporting and corrective actions) apply where the organization participates in a covered sector programme; see [`compliance/`](../compliance/).

### 2.2 Incident commander authority

The Incident Commander has authority to perform the actions below. For technical and operational response direction and approval or deferral of system isolation, service suspension, or credential revocation (the first two bullets), authority rests with the Incident Commander or, for P3 and P4 where no Incident Commander is assigned, the SOC lead, or, for P1 and P2 before an Incident Commander is assigned, the interim technical authority described below:

- Direct all technical and operational response activities.
- Approve or defer system isolation, service suspension, or credential revocation.
- Engage external forensic or IR support.
- Authorize or restrict communications to third parties during an active incident (regulatory notifications route per section 6 and are not restricted by this authority).

During a declared P1 incident, the Incident Commander is the CIO or CISO unless delegated in writing.

**Interim technical authority for P1 and P2.** From the time an incident is first classified as P1 or P2 until an Incident Commander is assigned, the CISO, or a duty delegate the CISO has authorized in advance, is the interim technical authority. Where the CISO relies on a duty delegate, the CISO delegates that authority in writing and the duty delegate is named in the IR Contact Register, which the CISO holds and where on-call duty rotates ([`security/sop-incident-escalation-matrix.md`](sop-incident-escalation-matrix.md), sections "Notification method" and "Out-of-hours escalation"). The interim technical authority holds the authority in the first two bullets above. Wherever this procedure, or [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) through its references to this procedure, requires the Incident Commander to direct, authorize, or confirm containment, isolation, reimaging, or evidence capture, or to confirm whether an investigation treats a device, its user, or its data as evidence, the interim technical authority does so until the Incident Commander is assigned. The interim technical authority also gives the notices to Legal Counsel set out in the Incident Commander row of section 2.1. When the Incident Commander is assigned, the interim technical authority hands over to the Incident Commander and records the handover in the incident record, including the actions taken, evidence status, and pending decisions. From then on, the Incident Commander acts instead.

---

## 3. Incident severity classification

### 3.1 Severity levels

| Severity | Criteria | Examples | Response SLA | Escalation |
| --- | --- | --- | --- | --- |
| **P1: Critical** | Active or confirmed breach; ransomware deployment, whether executing, staged or dormant; data exfiltration, whether active or completed; confirmed or suspected privileged account compromise; complete service outage caused or suspected to be caused by a security incident; or threat actor present in production environment or active anywhere else in the environment. Each listed trigger is P1 whatever its scope. In the outage trigger, "security incident" has the meaning given in [`security/sop-incident-escalation-matrix.md`](sop-incident-escalation-matrix.md), section "Incident severity levels". Otherwise, a complete service outage is an IT operations P1 handled under the [IT Service Management Framework](../operations/framework-it-service-management.md), sections "Service levels" and "1. Incident management" (under "Framework principles"), not this procedure. | Ransomware executing on production systems; ransomware staged on a single endpoint but not yet executed; confirmed exfiltration of customer PII or trade data; domain administrator credential confirmed compromised; active threat actor in the environment. | Immediate (within 15 minutes of first SOC awareness, the Detection timestamp) | Incident Commander, CISO, and CIO notified immediately. IR partner notified by CISO. All IR actions logged with timestamps. |
| **P2: High** | Suspected breach; significant security event with potential for serious impact; confirmed security incident with limited blast radius, potential data exposure, or multi-system compromise, other than a P1 trigger; malware detected but not yet confirmed active, or active malware needing containment, other than ransomware deployment (P1); phishing with credential capture (P1 where the captured credential is privileged); or significant control failure. Significant operational risk. | Malware detected on a critical server; malware on a single endpoint, blocked or quarantined with no sign of spread; suspicious lateral movement observed in SIEM; failed restore test on production backup. | Within 1 hour of first SOC awareness, the Detection timestamp | CISO notified within 1 hour. Incident Commander assigned. |
| **P3: Medium** | Anomalous activity requiring or under investigation, or an anomaly requiring containment that meets no P1 or P2 criterion (a suspected breach is P2); or policy violation (a minor procedural violation with no data or system impact and no potential security significance is P4). | User account exhibiting anomalous access patterns; unauthorized software detected on production system; failed authentication threshold exceeded; minor acceptable use policy violation with no data or system impact. | Within 8 business hours of first SOC awareness | SOC lead notified. Security team investigation initiated. |
| **P4: Low** | Informational alert or informational security event with no confirmed harm; failed security scan; false positive confirmed after investigation; or minor procedural violation with no data or system impact and no potential security significance. | Failed patch scan; expired certificate on non-critical system; minor misconfiguration with no exploitation evidence. | Within 5 business days of first SOC awareness | Assigned to SOC queue. Standard change or remediation process. |

Where a case meets the criteria of more than one level, the more severe level applies.

### 3.2 Severity escalation

Severity classification must be reassessed as new information becomes available. Any analyst may escalate severity upward without management approval. Downgrading severity from P1 requires Incident Commander approval, after consulting the appropriate roles (for example whichever of the CIO and CISO is not the Incident Commander and, where personal data is involved, the Data Protection Officer). The initial classification is recorded and retained even if subsequently revised.

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
| Threat intelligence | External notification of credentials in breach databases; indicators of compromise matching organizational assets. |
| Audit and compliance reviews | Control failures discovered during audit that indicate an active or historical breach. |
| Sector-programme monitoring | Anomalies flagged by sector-programme monitoring where the organization participates (e.g., BASC for cargo, customs, and trade systems; PCI DSS file-integrity monitoring; OT historian anomalies). |

### 4.2 Triage process

Upon receipt of an alert or report, the SOC analyst must:

1. **Validate** the event: confirm it is not a false positive by corroborating evidence from at least one additional source.
2. **Classify severity** using the criteria in Section 3.
3. **Preserve evidence immediately**: capture log snapshots, SIEM query results, endpoint telemetry, and network flows before any containment action is taken. Evidence preservation takes priority over service recovery in the first hour.
4. **Assign an Incident ID** and open a formal incident record in the ticketing system.
5. **Notify** the appropriate roles per Section 3.1 escalation requirements and, for a P3 or P4 incident that endangers network security where the organization is a network operator under the China Cybersecurity Law, the CISO per section 6.2 step 1. A notification Section 3.1 requires immediately (for example, for a P1) is made without waiting for the incident record in step 4.
6. **Refer without delay to the Data Protection Officer (DPO)** any incident that involves or may involve personal data held or processed by the organization, its processors, or its sub-processors, whatever its severity, so that the DPO can assess whether it is a confirmed or suspected personal data breach within the scope of [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) section 1.2. This referral applies alongside the Section 3.1 escalation notifications and does not replace them. Where an incident is found to involve or possibly involve personal data only after triage, the SOC must make the referral as soon as that is known.
7. **Brief the Incident Commander or, for P3 and P4 where no Incident Commander is assigned, the SOC lead, or, for P1 and P2 before an Incident Commander is assigned, the interim technical authority (section 2.2)** with: what is known, what systems and data are affected, what the suspected attack vector is, and what immediate containment options are available.

### 4.3 Triage record fields

| Field | Required Content |
| --- | --- |
| Incident ID | Unique identifier |
| Detection timestamp | UTC timestamp of first SOC awareness: for an automated alert, the earliest time the alert was available to the SOC in any of its tooling, whether generated there or delivered there, not the time an analyst first viewed it; for a report, the time the SOC received it; for a finding the SOC makes itself, the time the SOC first noticed the activity, not the time it concluded that the activity was an incident; where more than one applies, the earliest. It is the end point of mean time to detect (MTTD) and the start point of mean time to initiate (MTTI); see §10 |
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

- **Do not isolate or reimage systems without direction from the Incident Commander or, for P3 and P4 where no Incident Commander is assigned, the SOC lead, or, for P1 and P2 before an Incident Commander is assigned, the interim technical authority (section 2.2).** Premature isolation may destroy volatile evidence or alert the threat actor. Before rebuilding, reimaging, re-flashing or wiping a device or storage volume, confirm that no legal hold or investigation covers the device, its user, or its data, using the two-part confirmation in [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) §5.2.1 rule 2. A check of the GRC platform and Records Register confirms only whether a hold is recorded. Under that rule, Legal Counsel or the Incident Commander or, for P3 and P4 where no Incident Commander is assigned, the SOC lead, or, for P1 and P2 before an Incident Commander is assigned, the interim technical authority (section 2.2) confirms whether an investigation under this procedure treats the device, its user, or its data as evidence. Only Legal Counsel confirms whether an investigation by an external authority treats the device, its user, or its data as evidence, and whether a hold is required but not yet recorded. Where a legal hold or investigation covers the device, or that status cannot be confirmed, keep the original device or storage volume unaltered in custody until Legal Counsel, in writing, releases or narrows the hold under [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) §5.2.1 rule 8. For an investigation without a legal hold, that release is Legal Counsel's written confirmation that the investigation no longer treats the device or its contents as evidence. A forensic image does not substitute for keeping the original. Recover service on replacement hardware, a new instance, or restored copies; never rebuild, reimage, re-flash or wipe the held original in place.
- **Evidence preservation takes priority over service recovery in the first hour.** Capture memory dumps, running process lists, active network connections, and relevant log exports before any containment action that could alter system state.
- All containment actions must be logged with the UTC timestamp, the identity of the person taking the action, and authorization from the Incident Commander or, for P3 and P4 where no Incident Commander is assigned, the SOC lead, or, for P1 and P2 before an Incident Commander is assigned, the interim technical authority (section 2.2).

### 5.2 Containment phases

| Phase | Actions | Authorization |
| --- | --- | --- |
| **Short-term containment** | Network segmentation of affected systems; block suspected attacker IP ranges at the firewall; disable suspected compromised credentials; revoke active sessions. | Incident Commander or, for P3 and P4 where no Incident Commander is assigned, the SOC lead, or, for P1 and P2 before an Incident Commander is assigned, the interim technical authority (section 2.2) |
| **Evidence capture** | Memory acquisition; disk image of affected systems; export of relevant SIEM queries; preservation of authentication logs and EDR telemetry. | SOC, under direction from the Incident Commander or, for P3 and P4 where no Incident Commander is assigned, the SOC lead, or, for P1 and P2 before an Incident Commander is assigned, the interim technical authority (section 2.2) |
| **Long-term containment** | Maintain affected systems in a contained state while investigation continues; deploy enhanced monitoring; restrict privileged access to the affected environment. | Incident Commander or, for P3 and P4 where no Incident Commander is assigned, the SOC lead, or, for P1 and P2 before an Incident Commander is assigned, the interim technical authority (section 2.2) |

### 5.3 Eradication

Before any eradication or cleanup that would alter an original device or storage volume, apply the hold and investigation safeguard in §5.1, including its check and release requirements. Where preservation is required, keep the original unaltered and perform eradication or cleanup on replacement infrastructure.

Once the scope of compromise is confirmed, the SOC and IT Operations must, subject to that safeguard:

1. Remove all identified malware, persistence mechanisms, backdoors, and unauthorized accounts.
2. Revoke and rotate all credentials that were or may have been exposed, including service accounts, API keys, and certificates.
3. Patch or mitigate the vulnerability or control weakness that allowed the incident to occur.
4. Validate eradication with a follow-on scan or forensic review before proceeding to recovery.

### 5.4 Recovery

1. Restore affected systems from known-good backups or clean-rebuilt images, verified against integrity hashes, subject to the following safeguard. Before rebuilding, reimaging, re-flashing or wiping a device or storage volume, confirm that no legal hold or investigation covers the device, its user, or its data, using the two-part confirmation in [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) §5.2.1 rule 2. A check of the GRC platform and Records Register confirms only whether a hold is recorded. Under that rule, Legal Counsel or the Incident Commander or, for P3 and P4 where no Incident Commander is assigned, the SOC lead, or, for P1 and P2 before an Incident Commander is assigned, the interim technical authority (section 2.2) confirms whether an investigation under this procedure treats the device, its user, or its data as evidence. Only Legal Counsel confirms whether an investigation by an external authority treats the device, its user, or its data as evidence, and whether a hold is required but not yet recorded. Where a legal hold or investigation covers the device, or that status cannot be confirmed, keep the original device or storage volume unaltered in custody until Legal Counsel, in writing, releases or narrows the hold under [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) §5.2.1 rule 8. For an investigation without a legal hold, that release is Legal Counsel's written confirmation that the investigation no longer treats the device or its contents as evidence. A forensic image does not substitute for keeping the original. Recover service on replacement hardware, a new instance, or restored copies; never rebuild, reimage, re-flash or wipe the held original in place.
2. Verify that all SIEM alert categories and monitoring rules are operational before returning systems to production.
3. Monitor restored systems with enhanced logging and alerting for a minimum of 14 days post-recovery.
4. Obtain formal sign-off from the Incident Commander or, for P3 and P4 where no Incident Commander is assigned, the SOC lead, and from the relevant System Owner before resuming normal operations.
5. Document the return-to-service date and the basis for confirming that the threat has been eradicated.

---

## 6. Regulatory notification

### 6.1 Notification obligations summary

| Regulation | Trigger | Notification Deadline | Notifying Authority |
| --- | --- | --- | --- |
| **GDPR (EU)** | Personal data breach within the GDPR's territorial scope, unless unlikely to result in a risk to individuals' rights and freedoms (Art. 33(1)) | Without undue delay, and where feasible within 72 hours of becoming aware | DPO to relevant supervisory authority (CISO coordinating); individuals where high risk (Art. 34) |
| **PIPEDA (Canada)** | Breach of security safeguards where it is reasonable in the circumstances to believe it creates a real risk of significant harm to an individual (PIPEDA s. 10.1(1)) | As soon as feasible after the organization determines that the breach has occurred (PIPEDA s. 10.1(2); no fixed hour or day limit) | DPO to Privacy Commissioner of Canada; each affected individual for whom the same reasonable-belief test is met, on the same clock, unless otherwise prohibited by law (s. 10.1(3) and (6)) |
| **Quebec Law 25** | Confirmed confidentiality incident involving personal information presenting a risk of serious injury | Promptly to the Commission d'accès à l'information (no fixed statutory hour-count) | DPO |
| **PIPL (China)** | A leak, distortion, or loss of personal information that has occurred or may occur (PIPL Art. 57) | No fixed deadline (PIPL Art. 57 requires remedial measures immediately and notification of the departments, but sets no separate fixed time limit for notification); without delay, as programme policy | DPO to the PIPL Art. 60 departments (CISO coordinating); individuals unless the Art. 57 exception applies (for a network operator, see the Cybersecurity Law row) |
| **Cybersecurity Law (China)** | For network operators (网络运营者, which the law defines as the owners and managers of networks and network service providers, CSL Art. 78): a leak, damage, or loss of personal information that has occurred or may occur (CSL Art. 44 para. 2); an incident endangering network security (CSL Art. 27). CSL article numbers follow the amended numbering in force 1 January 2026; English rendering of the Chinese text, which is authoritative | The CSL itself sets no fixed time limit; it requires reporting as provided (按照规定) (CSL Art. 44 para. 2 requires remedial measures immediately and notifying users and reporting to the relevant departments in charge promptly as provided; CSL Art. 27 requires activating the network security incident response plan immediately, taking corresponding remedial measures and reporting to the relevant departments in charge as provided); without delay, as programme policy. The CAC has issued National Cybersecurity Incident Reporting Measures (国家网络安全事件报告管理办法), which are not held in the reference base, so an adopter confirms directly their in-force date, any reporting time limits, and whether they apply <!-- ref-absence: National Cybersecurity Incident Reporting Measures --> | For an incident that involves personal information: DPO, with the CISO coordinating, to the relevant departments in charge (有关主管部门): under CSL Art. 44 para. 2 where a leak, damage, or loss of personal information has occurred or may occur, and under CSL Art. 27 where the incident endangers network security, with or without such a leak, damage, or loss; users promptly as provided where CSL Art. 44 para. 2 applies, with no exception stated. For an incident endangering network security that involves no personal information: CISO to the relevant departments in charge (有关主管部门, CSL Art. 27). Legal Counsel approves content in each case, and section 6.2 step 1 routes a P3 or P4 incident endangering network security to the CISO |

Sector-programme notification obligations (for example, BASC requirements for trade, cargo, or customs anomalies meeting the BASC breach threshold) apply where the organization participates in a covered sector programme. The relevant sector annex states the trigger, timeframe, and notification path; see [`compliance/`](../compliance/).

### 6.2 Regulatory notification process

1. The DPO assesses whether the incident involves personal data and whether the risk threshold for notification is met. Under the China Cybersecurity Law (CSL), the DPO assesses whether a report is required on an incident that involves personal data: under CSL Art. 44 para. 2 where a leak, damage, or loss of personal information has occurred or may occur, and under CSL Art. 27 where the incident endangers network security, with or without such a leak, damage, or loss. For an incident endangering network security that involves no personal data, the CISO assesses whether the CSL requires a report (CSL Art. 27; see section 6.1). CSL Art. 27 sets no severity threshold, and section 3.1 notifies the CISO only of P1 and P2 incidents, so where the organization is a network operator under the CSL (CSL Art. 78), the SOC refers to the CISO any P3 or P4 incident that endangers network security when it classifies or reassesses the incident; the CISO makes the Art. 27 assessment where the incident involves no personal data and passes the incident to the DPO where it involves or may involve personal data.
2. Legal Counsel reviews and approves notification content before submission.
3. The DPO submits the regulatory notification and retains a copy in the incident record; for a China Cybersecurity Law report on an incident that involves no personal data, the CISO does so.
4. If notification cannot be completed within the regulatory window, the delay must be documented with reasons, and partial information submitted where permitted.

### 6.3 Sector-programme anomalies

Where the organization participates in a sector programme that defines elevated-trigger anomaly categories (for example, BASC for cargo, customs, or trade systems with an organization-set 2-hour initial-response SLA for unauthorized access to shipment data, tampering with customs records, or suspected cargo integrity compromise), the corresponding sector annex states the triage timeframe, the sector-conditional role notified, and the supplementary documentation maintained. See [`compliance/`](../compliance/).

### 6.4 Notification confidentiality

Regulatory notifications are Restricted classification materials. Content must not be shared externally beyond regulators, the DPO, Legal, the CIO, and the CISO without written authorization. No public statements regarding the incident must be made without CIO approval and coordination with Legal Counsel.

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

For P1/P2, the PIR must be conducted by the Incident Commander. For P3/P4, it must be conducted by the Incident Commander where one was assigned, or otherwise by the SOC lead. The PIR must address:

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
| Detection timestamp | UTC; first SOC awareness (§4.3) |
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

## 9. Incident-command execution checklist

This one-page checklist summarizes the time-phased actions for a declared P1 or P2 incident. It is a quick-reference companion to the detailed mechanics in Sections 4 to 7, not a replacement for them. All actions are logged with UTC timestamps under Incident Commander direction (§5.1). Until an Incident Commander is assigned, the interim technical authority gives that direction in the Incident Commander's place, within its §2.2 authority.

**First 60 minutes: detect, declare, contain**

- Validate the event against at least one corroborating source (§4.2).
- Classify severity per §3.1 (P1 response SLA: immediate, within 15 minutes of first SOC awareness).
- Preserve evidence before any containment action: log snapshots, SIEM results, EDR telemetry, network flows (§4.2, §5.1).
- Assign an Incident ID and open the formal incident record (§4.2).
- Notify per §3.1: for a P1, the Incident Commander, CISO, and CIO immediately; the IR partner by the CISO. An immediate notification is made without waiting for the incident record (§4.2 step 5).
- Refer the incident to the DPO for breach assessment if it involves or may involve personal data (§4.2 step 6).
- Until an Incident Commander is assigned, the CISO or a pre-authorized duty delegate, delegated in writing and named in the IR Contact Register, acts as interim technical authority; record the handover in the incident record when the Incident Commander is assigned (§2.2).
- Brief the Incident Commander or, until one is assigned, the interim technical authority (§2.2), on what is known, the affected systems and data, the suspected vector, and the containment options (§4.2).
- Begin short-term containment under the direction of the Incident Commander or, until one is assigned, the interim technical authority (segmentation, block attacker IPs, disable compromised credentials, revoke sessions); do not isolate or reimage without that direction (§5.1, §5.2).

**By 4 hours: confirm containment, begin eradication**

- Confirm containment (the P1 mean-time-to-contain target is under 4 hours; see §10).
- Complete evidence capture: memory acquisition, disk images, SIEM exports, authentication and EDR telemetry (§5.2, §8.1).
- Begin eradication once scope is confirmed: remove malware, persistence mechanisms, backdoors, and unauthorized accounts; rotate exposed credentials, API keys, and certificates; patch the root vulnerability (§5.3).
- For a P1, engage the IR partner, authorized by the CISO (§3.1).
- If personal data is involved, the DPO assesses impact and coordinates with the breach-response procedure (§2.1; see [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md)).

**By 24 hours: recover, engage notification, track closure**

- Validate eradication with a follow-on scan or forensic review before recovery (§5.3).
- Recover: before rebuilding, reimaging, re-flashing or wiping a device or storage volume, confirm that no legal hold or investigation covers the device, its user, or its data, using the two-part confirmation in [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) §5.2.1 rule 2. The GRC platform and Records Register check alone does not complete it. Where a legal hold or investigation covers the device, or that status cannot be confirmed, keep the original unaltered in custody until Legal Counsel's written release or narrowing under [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) §5.2.1 rule 8; a forensic image does not substitute. Recover service on replacement hardware, a new instance, or restored copies, never on the held original in place. Restore from known-good backups or clean-rebuilt images verified against integrity hashes; confirm monitoring rules are operational; apply enhanced monitoring for at least 14 days; obtain Incident Commander and System Owner sign-off (§5.4).
- Where a regulatory threshold is met, initiate and track the notification clocks per §6 (for example, GDPR without undue delay and, where feasible, within 72 hours of becoming aware; see §6.1); Legal Counsel approves the content and the DPO submits a notification that §6.1 assigns to the DPO, or the CISO for a China Cybersecurity Law report on an incident that involves no personal data (§6).
- Document the return-to-service date and the basis for confirming eradication (§5.4).
- Initiate the post-incident review track, mandatory for P1 and P2, due within 5 business days of closure (§7.1).

---

## 10. Metrics

The SOC must track and report the following metrics at the monthly security operations review and quarterly governance review:

| Metric | Definition | Target |
| --- | --- | --- |
| **Mean Time to Detect (MTTD)** | Time from incident onset to first SOC awareness | By SOC capability tier, as defined in [`security/standard-soc-operating-model.md`](standard-soc-operating-model.md) §3; that standard's §11 sets these targets and governs: Tier A: best effort; Tier B: under 4 hours for P1/P2; Tier C: under 1 hour for P1/P2 |
| **Mean Time to Initiate (MTTI)** | Time from first SOC awareness (the Detection timestamp) to formal incident declaration and Incident Commander assignment | P1: < 15 minutes; P2: < 1 hour |
| **Mean Time to Contain (MTTC)** | Time from incident declaration to confirmed containment | P1: < 4 hours; P2: < 8 hours |
| **Mean Time to Recover (MTTR)** | Time from incident declaration to confirmed service restoration and closure | P1: < 24 hours; P2: < 72 hours |
| **SLA Adherence** | Percentage of incidents where notification and response SLAs were met | ≥ 95% |
| **Regulatory Notification Timeliness** | Percentage of notifiable breaches where regulatory notification was submitted within the required window | 100% |
| **PIR Completion Rate** | Percentage of P1/P2 incidents with PIR completed within 5 business days | ≥ 95% |
| **Repeat Incidents** | Number of incidents sharing the same root cause as a prior incident in the past 12 months | Target: 0 for P1/P2 root causes |

---

## 11. Framework alignment

| Control Area | ISO/IEC 27035-1:2023 | ISO/IEC 27035-2:2023 | ISO/IEC 27035-3:2020 | NIST SP 800-61 Rev. 3 | ISO/IEC 27001:2022 | COBIT 2019 | CSA CCM v4.1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Incident management policy and planning | Clause 5.2 | Clauses 4 to 11 | N/A | §2.3, §3.1 | A.5.24 | DSS02.01 | SEF-01, SEF-03 |
| Detection and reporting | Clause 5.3 | N/A | Clauses 7, 8 and 12 | §3.2 | A.6.8 | DSS02.02 | SEF-06 |
| Triage and classification | Clause 5.4 | Clause 6.5 | Clauses 9 and 10 | §3.2 (RS.MA-02, RS.MA-03, RS.MA-04) | A.5.25 | DSS02.02 | SEF-06 |
| Incident command and IR partner engagement | Clauses 4.5.3 and 5.5 | Clauses 7.3 and 8.3 | N/A | §3.2 (RS.MA-01) | A.5.24, A.5.26 | DSS02.04 | SEF-07 |
| Containment and evidence preservation | Clause 5.5 | N/A | Clause 11.2 | §3.2 (RS.MI-01, RS.AN-06, RS.AN-07) | A.5.26 | DSS02.04 | SEF-07, SEF-09 |
| Eradication and recovery | Clause 5.5 | N/A | Clauses 11.3 and 11.4 | §3.2 (RS.MI-02, RS.MA-05, RC.RP-01, RC.RP-02, RC.RP-03, RC.RP-04, RC.RP-05) | A.5.26 | DSS02.05 | SEF-07 |
| Regulatory notification | Clause 5.5 j), l) | N/A | Clause 12.3 | §3.2 (RS.CO-02) | A.5.5 | MEA03.01, MEA03.02 | SEF-08 |
| Post-incident review | Clause 5.6 | Clause 12 | N/A | §3.1 | A.5.27 | DSS02.06 | SEF-07, SEF-09 |
| Evidence handling | Clauses 5.3 d), i); 5.4 i), l); 5.5 f), j), m) | N/A | Clause 10.6 | §3.2 (RS.AN-06, RS.AN-07) | A.5.28 | DSS02.04 | SEF-09 |
| Incident response metrics | Clause 5.6 | Clause 12.1 | N/A | §3.1 | Clause 9.1 | MEA01.02, MEA01.03, MEA01.04 | SEF-05 |

Beyond the incident-lifecycle mappings above, this procedure aligns with NIST SP 800-184 (Guide for Cybersecurity Event Recovery) for the recovery phase, and with NIST SP 800-86 (Guide to Integrating Forensic Techniques into Incident Response) and ISO/IEC 27037:2012 (Guidelines for identification, collection, acquisition and preservation of digital evidence) for evidence handling and digital forensics. Where the IR partner or another organization takes part in the response, the procedure also draws on ISO/IEC 27035-4:2024 (Part 4: Coordination), Clauses 4.3.2 and 5.5, as guidance for coordinating with that organization; the standard recommends defining each participating party's roles and responsibilities and identifying which organization leads the response.

**Canadian federal public sector.** Where the adopter is a Government of Canada (GC) organization (see [`compliance/public-sector/annex-canada-public-sector-requirements.md`](../compliance/public-sector/annex-canada-public-sector-requirements.md)), the following held texts bear on this procedure. Each is cited at the edition held, and its currency is to be confirmed upstream before reliance. Plans and guidance are cited as such, not as statutory duties.

- **Policy on Government Security** (held text: in effect since 1 July 2019, amended effective 6 January 2025). It makes the deputy head responsible for ensuring that security incidents and other security events are assessed, investigated, documented, acted on and reported to the appropriate authority and to affected stakeholders (4.1.7).
- **Directive on Security Management** (held text: in effect since 1 July 2019). It makes senior officials responsible for establishing processes to monitor, respond to and report threats, vulnerabilities, security incidents and other security events in their area of responsibility (4.2.8). Its mandatory procedures for security event management control direct the department to designate an official departmental contact for government-wide communications (G.2.2.2), to test its security event management processes (G.2.2.6), to report events that affect or may affect government-wide preparedness, response or recovery to the appropriate lead security agency or central agency (G.2.3.2), and to report suspected criminal activity to the appropriate law enforcement authority (G.2.3.3).
- **GC Cyber Security Event Management Plan (GC CSEMP)** (held text: date modified 2026-05-20). It states that GC organizations must report all cyber security incidents to the Canadian Centre for Cyber Security (Cyber Centre), and that departments are expected to report within its Table 2-1 timeframes: an initial report as soon as possible and not more than 1 hour after initial detection, and a detailed report within 24 hours after detection, which should include likely or potential business impact where possible (§2.3.1.2). It also expects departments to report cyber incidents to the police of jurisdiction (§2.3.1.3), states that departments remain accountable for ensuring that security and privacy incidents involving third-party suppliers are identified, escalated and reported (§2.3.1.5), and sets four GC response levels, from a departmental response to an emergency (crisis) response, which the Office of the Chief Information Officer of the Treasury Board of Canada Secretariat and the Cyber Centre declare after their initial assessment (§2.3.2 and §2.3.2.1). These timeframes run alongside the severity clocks in section 3 and the regulatory clocks in section 6; they do not replace either.
- **CCCS Developing Your Incident Response Plan (ITSAP.40.003)** (held text: January 2026, awareness series). This is advisory guidance. It lists nine preparation steps for an incident response plan, the last being exercises to test the plan and the response (Main steps in your incident response plan, Preparation, steps 1 to 9), and advises testing, revisiting and revising the plan annually.
- **CCCS Baseline Cyber Security Controls for Small and Medium Organizations V1.2** (held text: February 2020). Its incident-response controls say that organizations should have a basic plan for responding to incidents of varying severity (BC.1.1) and a written incident response plan that names who handles incidents and holds contact information for external parties, stakeholders and regulators (BC.1.2), and should consider cyber security insurance that covers incident response and recovery or give a rationale for not buying it (BC.1.3).

The Directive on Security Management's Appendix I, Standard on Security Event Reporting, to which its G.2.3 refers, is not held in the reference base; confirm its reporting requirements against the official text before relying on them. <!-- ref-absence: Standard on Security Event Reporting --> The intake pointer for federal reporting is in [`resilience/procedure-security-incident-reporting-and-escalation.md`](../resilience/procedure-security-incident-reporting-and-escalation.md), and the treatment of incidents involving personal information is in [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) §12.

---

## Licence

This document is released under the **CC BY-SA 4.0** licence. See [`LICENSE`](../LICENSE) in the repository root.

---

**End of Document**
