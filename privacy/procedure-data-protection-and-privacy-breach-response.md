# Data Protection and Privacy Breach Response Procedure

**Document Title:** Data Protection and Privacy Breach Response Procedure  
**Document Type:** Procedure  
**Version:** 1.3.0  
**Date:** 2026-05-27  
**Owner:** Chief Information Officer  
**Approving Authority:** Governance Library Maintainer  
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`security/procedure-incident-response.md`](../security/procedure-incident-response.md), [`privacy/charter-privacy-management-programme.md`](charter-privacy-management-programme.md), [`privacy/annex-regional-privacy-requirements.md`](annex-regional-privacy-requirements.md)  
**Classification:** Public  
**Category:** Privacy  
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change  
**Repository Path:** [`privacy/procedure-data-protection-and-privacy-breach-response.md`](procedure-data-protection-and-privacy-breach-response.md)  
**Confidentiality:** Public  
**Licence:** CC0 1.0 Universal  

---

## 1. Purpose and Scope

### 1.1 Purpose

This procedure defines the lifecycle for detecting, containing, assessing, notifying, remediating, and closing personal data breaches and privacy incidents. It establishes mandatory roles, response timeframes, jurisdiction-specific notification obligations, and evidence requirements, and ensures that regulatory notification deadlines are met for all applicable laws.

The procedure is aligned to ISO/IEC 27701:2019 §8.9, GDPR Articles 33–34, UK GDPR Articles 33–34, CPPA, PIPL Article 57, LGPD, Quebec Law 25, and CSA CCM v5 PRI-05 and SEF-02.

### 1.2 Scope

1. Applies to all confirmed or suspected personal data breaches involving personal data held or processed by the organisation, its processors, or its sub-processors.
2. Covers trade and customs data breaches where personal data is embedded in supply chain or customs records, including BASC-certified logistics environments.
3. Covers AI training data leakage where personal data used to train or fine-tune AI models is exposed to unauthorised parties.
4. Applies across all jurisdictions in which the organisation operates, including the European Union, United Kingdom, Canada (federal and provincial), China, Brazil, and United States.
5. This procedure operates alongside [`security/procedure-incident-response.md`](../security/procedure-incident-response.md), which governs the technical containment and investigation lifecycle. This procedure governs the privacy-specific assessment, notification, and post-breach obligations.

### 1.3 Relationship to the Incident Response Procedure

A personal data breach is also a security incident. The CISO and Privacy Officer are jointly responsible for initiating breach response as documented in [`privacy/charter-privacy-management-programme.md`](charter-privacy-management-programme.md). Technical containment, evidence preservation, and eradication actions are executed per [`security/procedure-incident-response.md`](../security/procedure-incident-response.md). This procedure governs the parallel privacy-specific stream: breach severity assessment, regulatory notification determination, data subject notification, and privacy-focused post-breach review.

---

## 2. Governance

### 2.1 Roles and Responsibilities

| Role | Responsibilities |
| --- | --- |
| **CISO** | Joint responsibility for initiating breach response. Leads the technical incident investigation and containment stream per [`security/procedure-incident-response.md`](../security/procedure-incident-response.md). Notified immediately for all P1 and P2 breaches. Coordinates with the Privacy Officer on notification decisions. |
| **Chief Information Officer (CIO, acting DPO)** | Executive accountability for regulatory notification decisions. Approves all notifications to supervisory authorities. Signs off on data subject communications. Represents the organisation before regulatory authorities. Notified immediately for all P1 and confirmed P2 privacy breaches. |
| **Privacy Officer** | Operational ownership of the privacy breach response process. Manages the breach register, coordinates jurisdictional notification assessment, prepares regulatory notification content, and oversees the post-breach review. |
| **Legal Counsel** | Determines notification obligations by jurisdiction. Advises on exemptions, litigation hold, evidence handling, and regulatory engagement strategy. Reviews and approves all regulatory and data subject notifications before submission. |
| **Security Operations Centre (SOC)** | Detects and triages security events that may constitute personal data breaches. Preserves evidence, executes technical containment, and provides forensic information to support the Privacy Officer's impact assessment. |
| **IT Operations / System Owners** | Support data scope identification, access restriction, and deletion or recovery actions directed by the Privacy Officer and CISO. |
| **Regional BASC Compliance Officer** | Notified for any breach affecting BASC trade, customs, or cargo records. Coordinates BASC-specific reporting. |

### 2.2 Joint Leadership

The CISO and Privacy Officer are jointly responsible for initiating breach response the moment a potential personal data breach is identified. Neither role may unilaterally close or downscale a privacy breach without agreement of the other and CIO sign-off.

---

## 3. Breach Severity Classification

All suspected personal data breaches are classified at the point of initial detection and reassessed as additional information becomes available. Classification drives response SLAs, escalation paths, and resourcing.

| Severity | Classification Criteria | Examples |
| --- | --- | --- |
| **P1 — Critical** | Large-scale personal data exposure affecting more than 1,000 individuals; Restricted or sensitive personal data (health, financial, biometric, children's data) exfiltrated or exposed; BASC trade data breach with embedded personal data; credentials or encryption keys protecting personal data stores confirmed compromised; ransomware or destructive attack affecting systems holding personal data | Exfiltration of customer PII database; ransomware encrypting HR and payroll systems; confirmed compromise of credentials for the identity provider protecting personal data repositories; BASC cargo manifest breach disclosing shipper personal data at scale |
| **P2 — High** | Moderate personal data exposure affecting fewer than 1,000 individuals; unauthorised access to Confidential personal data without confirmed exfiltration; accidental disclosure to an unintended recipient; supplier breach confirmed to have affected personal data held on the organisation's behalf | Single employee medical record emailed to wrong recipient; supplier notification of unauthorised access to a CRM extract; unauthorised internal access to payroll records |
| **P3 — Medium** | Internal data only with no personal data; limited scope with no confirmed external disclosure; technical misconfiguration corrected before any confirmed access; minor policy violations | Configuration error exposing internal-only operational data to authenticated internal users; log file with non-personal technical data briefly publicly accessible |

Severity is reassessed at each phase of the breach response lifecycle. Any team member may escalate severity upward. Downgrading from P1 requires CIO approval.

### 3.1 Evidence Preservation Obligation

For all P1 incidents, evidence preservation takes priority. Systems must not be isolated, reimaged, or modified without direction from the Incident Commander as defined in [`security/procedure-incident-response.md`](../security/procedure-incident-response.md) §5.1. The Privacy Officer must be briefed on evidence status before any containment action that could affect the completeness of the privacy impact assessment.

---

## 4. Detection and Initial Assessment

### 4.1 Detection Sources

Personal data breaches may be detected from any of the following sources:

- SIEM alerts or SOC investigations revealing unauthorised access to systems holding personal data.
- Endpoint detection and response (EDR) platform alerts indicating data exfiltration behaviour.
- Employee or contractor reports of lost devices, misaddressed email, or accidental disclosure.
- Supplier or processor notification of a breach affecting organisational data — suppliers must notify within 24 hours of a breach affecting organisational personal data per contractual data processing agreements.
- Regulator or law enforcement notification.
- Dark web monitoring alerting to the appearance of organisational data.
- BASC monitoring systems identifying anomalies in trade or customs data flows.

### 4.2 24-Hour Initial Assessment

Within 24 hours of a potential personal data breach being identified, the Privacy Officer and CISO jointly conduct an initial assessment to determine:

1. **Is personal data involved?** Confirm whether the affected data includes information that identifies or is capable of identifying natural persons.
2. **What is the likely scope?** Estimate the number of individuals affected, the categories of data involved, and the approximate volume of records.
3. **Has data been accessed or exfiltrated?** Determine whether the breach is limited to availability impact (e.g., system outage) or includes confidentiality impact (unauthorised access or disclosure).
4. **What is the risk to individuals?** Assess the likely consequences for affected individuals, including risk of identity theft, financial harm, discrimination, reputational damage, or physical harm.
5. **What is the applicable jurisdiction?** Identify which privacy laws govern the affected individuals and data.
6. **Is notification likely to be required?** Make a preliminary determination on whether regulatory or individual notification thresholds appear to be met, and in which jurisdictions.

The assessment is documented and retained as part of the breach record.

---

## 5. Containment

### 5.1 Containment Principles

Containment actions for personal data breaches follow the containment framework in [`security/procedure-incident-response.md`](../security/procedure-incident-response.md) §5. The following privacy-specific principles additionally apply:

- **Do not destroy evidence.** No system, log, backup, or data record relevant to the breach may be deleted, overwritten, or modified pending the privacy impact assessment and regulatory notification determination.
- **Scope isolation, not deletion.** Containment focuses on restricting further access to or exposure of personal data; premature deletion of breach-related data is prohibited unless specifically directed by Legal Counsel to meet a legal obligation.
- **Notify processors promptly.** If personal data held by a third-party processor is affected, the processor is notified immediately and directed to preserve evidence and assist with the impact assessment.

### 5.2 Containment Actions

Containment actions vary by breach type:

| Breach Type | Typical Containment Actions |
| --- | --- |
| Unauthorised system access | Revoke compromised credentials; terminate active sessions; restrict access to affected systems; preserve authentication and access logs |
| Data exfiltration | Block egress channels identified as exfiltration routes; engage endpoint detection; preserve SIEM and network flow evidence |
| Accidental disclosure (email / file) | Request return or deletion of disclosed data from recipient; document recipient details; confirm whether data was accessed |
| Lost or stolen device | Initiate remote wipe via endpoint management platform if device is enrolled and reachable; document device contents and encryption status |
| Supplier breach | Invoke contractual breach notification clause; request evidence of containment from supplier; restrict supplier access pending investigation |
| BASC trade data breach | Notify Regional BASC Compliance Officer immediately; initiate BASC incident documentation; restrict access to affected customs and cargo systems |

---

## 6. Notification Assessment

### 6.1 Assessment Framework

Following containment and initial assessment, the Privacy Officer and Legal Counsel conduct a formal notification assessment determining:

- Whether a notifiable breach has occurred in each applicable jurisdiction.
- The deadline for regulatory notification.
- Whether data subjects must be individually notified.
- The content requirements for notifications.

The notification assessment is documented in the breach record and approved by the CIO (acting DPO) before any notification is submitted.

### 6.2 Jurisdiction-Specific Notification Requirements

| Jurisdiction | Governing Law | Regulatory Authority | Notification Trigger | Regulatory Deadline | Individual Notification |
| --- | --- | --- | --- | --- | --- |
| **European Union** | GDPR Arts. 33–34 | Relevant lead supervisory authority (EDPB member authority); ICO for UK data subjects | Breach likely to result in a risk to the rights and freedoms of natural persons | 72 hours from the point of becoming aware of the breach | Without undue delay where the breach is likely to result in a high risk to individuals |
| **United Kingdom** | UK GDPR Arts. 33–34 | Information Commissioner's Office (ICO) | Same threshold as EU GDPR | 72 hours from becoming aware | Without undue delay where high risk |
| **Canada (Federal)** | CPPA; PIPEDA (until CPPA in force) | Office of the Privacy Commissioner of Canada (OPC) | Real risk of significant harm to the individual | Without unreasonable delay (72-hour target) | As soon as feasible after the determination that significant harm is likely |
| **Quebec (Provincial)** | Quebec Law 25 (Bill 64); Act Respecting the Protection of Personal Information | Commission d'accès à l'information (CAI) | Confidentiality incident creating a serious injury risk | 72 hours to the CAI; promptly to affected individuals | Promptly after notifying CAI |
| **China** | PIPL Art. 57 | Cyberspace Administration of China (CAC) / relevant PIPC authority | Breach of personal information | Immediately / without delay upon discovery | Promptly to affected individuals if high risk; may be deferred if measures have effectively prevented harm, subject to authority direction |
| **Brazil** | LGPD Arts. 48–49 | Autoridade Nacional de Proteção de Dados (ANPD) | Breach likely to cause risk or harm to data subjects | Within reasonable period per ANPD guidelines (ANPD Resolution CD/ANPD No. 2 guidance: 2 business days for initial notification; 5 business days for full report) | Without undue delay |
| **United States** | State breach notification laws (varies) | Varies by state (e.g., State Attorney General) | Personal information of state residents exposed | Varies by state; refer to [`compliance/register-global-regulatory-applicability.md`](../compliance/register-global-regulatory-applicability.md) for current state-level mapping | Varies by state; generally without unreasonable delay |

> **Note:** The 72-hour GDPR clock starts from the moment the controller becomes aware that a breach of personal data has occurred — not from the moment the breach occurred. "Becoming aware" is interpreted as when the controller has a reasonable degree of certainty that a security incident has taken place that has led to personal data being compromised.

### 6.3 Supplier Notification

Where a processor or sub-processor is involved, the organisation:

- Notifies the processor of the breach (if the processor is the affected party, they must have already notified the organisation within 24 hours per §4.1).
- Coordinates to ensure the processor preserves evidence and supports the impact assessment.
- Confirms contractual notification obligations have been met and documents the confirmation.

---

## 7. Notification Content Requirements

All regulatory and individual notifications must contain the following information to the extent known at the time of notification. Where information is not yet available, the notification states this and provides a timeline for supplementary notification.

### 7.1 Regulatory Notification Content

1. **Nature of the breach:** Description of what happened, when it occurred, and when it was discovered.
2. **Data categories and approximate volume:** Categories of personal data affected (e.g., contact details, financial data, health data, credentials) and approximate number of records and individuals affected.
3. **Likely consequences:** Assessment of the likely consequences of the breach for affected individuals.
4. **Measures taken or proposed:** Description of containment, mitigation, and remediation measures taken or planned.
5. **Contact details:** Name and contact details of the DPO (or acting DPO/CIO) for further liaison with the supervisory authority.
6. **Affected jurisdictions:** Where the breach affects individuals in multiple jurisdictions, the notification identifies the lead authority and confirms cross-border scope.

### 7.2 Individual Notification Content

Individual notifications are written in plain, accessible language and include:

1. A clear description of the nature of the breach.
2. The name and contact details of the Privacy Officer or acting DPO.
3. A description of the likely consequences of the breach for the individual.
4. Actions taken by the organisation to address the breach and mitigate its effects.
5. Steps the individual can take to protect themselves (e.g., change passwords, monitor financial accounts, contact credit bureaus).

Individual notifications must not contain information that could compromise an ongoing investigation. Legal Counsel reviews all individual notification content before distribution.

### 7.3 Phased Notification

Where full information is not available within the notification deadline, a phased notification approach is used:

1. **Initial notification:** Submit within the regulatory deadline with available information, clearly indicating that the notification is being submitted in phases.
2. **Supplementary notification:** Submit additional information as it becomes available without undue delay, clearly cross-referencing the original notification.

---

## 8. Post-Breach Review

### 8.1 Post-Incident Review (PIR) Requirement

A formal post-breach review (PIR) is mandatory for all P1 and P2 privacy breaches and must be completed within 10 business days of incident closure.

| Severity | PIR Required | Deadline |
| --- | --- | --- |
| P1 — Critical | Mandatory | Within 10 business days of closure |
| P2 — High | Mandatory | Within 10 business days of closure |
| P3 — Medium | At Privacy Officer discretion | Within 20 business days of closure |

### 8.2 PIR Scope

The PIR addresses:

1. **Timeline reconstruction:** Complete chronology from initial data compromise to discovery, containment, notification, and closure.
2. **Root cause analysis:** The underlying control failure, process gap, or configuration weakness that caused or enabled the breach.
3. **Data impact assessment:** Final confirmed scope of affected individuals, data categories, and records.
4. **Notification compliance:** Whether all regulatory notification deadlines were met; explanation and documentation of any deadline exceptions.
5. **Detection effectiveness:** Time from breach occurrence to organisational awareness; assessment of whether monitoring controls were adequate.
6. **Control gaps:** Specific controls that failed, were absent, or were insufficient to prevent or detect the breach.
7. **Corrective actions:** Named control owners, remediation actions, implementation deadlines, and tracking mechanism.
8. **Risk register update:** Confirmation that existing risk entries have been re-scored or new risks added to reflect the lessons learned.

### 8.3 PIR Output

The PIR report is classified Restricted. It is provided to the CIO, CISO, Privacy Officer, and Internal Audit. Corrective actions are tracked in the privacy remediation register and reported at the quarterly Privacy Governance Review. Where the breach was subject to regulatory notification, the regulator may request the PIR findings as part of their investigation.

---

## 9. Record Keeping

### 9.1 Breach Register

The Privacy Officer maintains a breach register documenting every suspected or confirmed personal data breach, regardless of whether regulatory notification was required. The breach register is a living document retained and available for regulatory inspection.

Each breach register entry includes:

| Field | Description |
| --- | --- |
| Breach ID | Unique identifier |
| Date and time of discovery | UTC |
| Date and time of occurrence (if known) | UTC or estimated range |
| Breach type | Unauthorised access / Accidental disclosure / Exfiltration / Lost device / Supplier breach / Other |
| Data categories affected | e.g., Contact details, financial, health, credentials, biometric, children's data |
| Approximate number of individuals affected | Confirmed or estimated |
| Severity classification | P1 / P2 / P3 |
| Containment actions summary | Key actions taken |
| Risk to individuals assessment | None / Low / Moderate / High |
| Notification decision (by jurisdiction) | Required / Not required / Deferred / Not applicable |
| Regulatory notifications submitted | Authority, date submitted, reference number |
| Individual notifications | Method, date, estimated count |
| PIR completion date | Date PIR was signed off |
| Corrective actions | Summary with owners and deadlines |
| Closure date | Date formally closed |
| CIO sign-off | Date and confirmation |

### 9.2 Evidence Retention

All breach evidence — forensic artefacts, SIEM log exports, investigation records, containment records, notification drafts and submissions, authority correspondence, PIR reports, and corrective action records — must be retained for a minimum of 7 years, consistent with the retention schedule in [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md).

Records subject to regulatory investigation, litigation hold, or authority request are retained until the hold is formally lifted by Legal Counsel.

### 9.3 Regulatory Notification Records

Copies of all submitted regulatory notifications, including phased supplementary notifications and authority correspondence, are retained in the breach case file as Restricted documents. Access is limited to the Privacy Officer, CIO, CISO, and Legal Counsel.

---

## 10. Metrics

The following metrics are tracked and reported to the CIO and CISO at the quarterly Privacy Governance Review:

| Metric | Definition | Target |
| --- | --- | --- |
| **Breaches by Severity** | Total personal data breaches confirmed in the reporting period, broken down by P1, P2, and P3 | Tracked; volume and severity trend monitored |
| **Regulatory Notification SLA Adherence (%)** | Percentage of notifiable breaches where regulatory notifications were submitted within the applicable jurisdictional deadline | 100% |
| **Mean Time to Notify (MTTN)** | Average time in hours from organisational awareness of a notifiable breach to submission of the regulatory notification | Target: ≤ 48 hours (comfortably within 72-hour deadlines) |
| **Individual Notification Timeliness (%)** | Percentage of cases requiring individual notification where notification was issued without undue delay following regulatory notification | ≥ 95% |
| **PIR Completion Rate (%)** | Percentage of P1 and P2 breaches with PIR completed within 10 business days of closure | ≥ 95% |
| **Corrective Action Closure Rate (%)** | Percentage of PIR-identified corrective actions closed within their agreed deadline | ≥ 90% |
| **Supplier Breach Notification Timeliness** | Percentage of supplier-involved breaches where the supplier notified within the contractual 24-hour window | Tracked; persistent non-compliance triggers contract review |

---

## 11. Framework Alignment

| Control Area | Framework Reference |
| --- | --- |
| Privacy breach response programme | ISO/IEC 27701:2019 §8.9; CSA CCM v5 PRI-05 |
| Regulatory breach notification — EU/UK | GDPR Arts. 33–34; UK GDPR Arts. 33–34 |
| Regulatory breach notification — Canada | CPPA; PIPEDA Breach of Security Safeguards Regulations; Quebec Law 25 |
| Regulatory breach notification — China | PIPL Art. 57 |
| Regulatory breach notification — Brazil | LGPD Arts. 48–49 |
| Regulatory breach notification — US | State breach notification laws; refer to [`compliance/register-global-regulatory-applicability.md`](../compliance/register-global-regulatory-applicability.md) |
| Security incident response | ISO/IEC 27035; NIST SP 800-61 Rev 2; [`security/procedure-incident-response.md`](../security/procedure-incident-response.md) |
| Evidence preservation | ISO/IEC 27037; [`security/procedure-incident-response.md`](../security/procedure-incident-response.md) §8 |
| SIEM alert integration | CSA CCM v5 SEF-02; [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md) |
| Record keeping and retention | ISO/IEC 27701 §8.9; [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md) |
| AI training data leakage | ISO/IEC 27701 §8.9; [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md) |
| BASC trade data | BASC International Standard v6; [`supply-chain/annex-trade-and-supply-chain-continuity-controls.md`](../supply-chain/annex-trade-and-supply-chain-continuity-controls.md) |

---

*This document is released under the CC0 1.0 Universal public domain dedication. To the extent possible under law, all copyright and related rights are waived. See `LICENSE` in the repository root.*

---

**End of Document**
