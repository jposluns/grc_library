# Data Protection and Privacy Breach Response Procedure

**Document Title:** Data Protection and Privacy Breach Response Procedure\
**Document Type:** Procedure\
**Version:** 1.10.12\
**Date:** 2026-10-27\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`security/policy-byod.md`](../security/policy-byod.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`privacy/charter-privacy-management-programme.md`](charter-privacy-management-programme.md), [`privacy/annex-privacy-jurisdiction-index.md`](annex-privacy-jurisdiction-index.md), [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/procedure-data-protection-and-privacy-breach-response.md`](procedure-data-protection-and-privacy-breach-response.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customization guidance.

---

## 1. Purpose and scope

### 1.1 Purpose

This procedure defines the lifecycle for detecting, containing, assessing, notifying, remediating, and closing personal data breaches and privacy incidents. It establishes mandatory roles, response timeframes, jurisdiction-specific notification obligations, and evidence requirements, and supports meeting regulatory notification deadlines for all applicable laws.

The procedure is aligned to ISO/IEC 27701:2025 (privacy incident management; section numbering changed in 2025 standalone revision), GDPR Articles 33 to 34, UK GDPR Articles 33 to 34, PIPEDA (Breach of Security Safeguards Regulations), PIPL Article 57, China Cybersecurity Law Article 44 para. 2 and, where the incident also endangers network security, Article 27 (in the amended numbering in force 1 January 2026), LGPD, Quebec Law 25, and CSA CCM v4.1 SEF-08 and SEF-06.

### 1.2 Scope

1. Applies to all confirmed or suspected personal data breaches involving personal data held or processed by the organization, its processors, or its sub-processors.
2. Covers trade and customs data breaches where personal data is embedded in supply chain or customs records, including BASC-certified logistics environments.
3. Covers AI training data leakage where personal data used to train or fine-tune AI models is exposed to unauthorized parties.
4. Applies across all jurisdictions in which the organization operates, including the European Union, United Kingdom, Canada (federal and provincial), China, India, Brazil, and United States.
5. This procedure operates alongside [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), which governs the technical containment and investigation lifecycle. This procedure governs the privacy-specific assessment, notification, and post-breach obligations.

### 1.3 Relationship to the incident response procedure

A personal data breach is also a security incident. The CISO and Data Protection Officer are jointly responsible for initiating breach response as documented in [`privacy/charter-privacy-management-programme.md`](charter-privacy-management-programme.md). Technical containment, evidence preservation, and eradication actions are executed per [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md). This procedure governs the parallel privacy-specific stream: breach severity assessment, regulatory notification determination, data subject notification, and privacy-focused post-breach review.

---

## 2. Governance

### 2.1 Roles and responsibilities

| Role | Responsibilities |
| --- | --- |
| **CISO** | Joint responsibility for initiating breach response. Leads the technical incident investigation and containment stream per [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md). Notified immediately for all P1 and P2 breaches. Coordinates with the Data Protection Officer on notification decisions. |
| **Chief Information Officer (CIO)** | Executive accountability for the privacy breach response programme. Notified immediately for all P1 and confirmed P2 privacy breaches. Names in advance the alternate privacy Incident Commander and, where the conflict-of-interest assessment finds a conflict, designates that alternate (section 3). While the assessment is pending, or if it cannot reach a conclusion, it is treated as a conflict and that alternate holds privacy command (section 3). |
| **Data Protection Officer** | Operational ownership of the privacy breach response process. Manages the breach register, coordinates jurisdictional notification assessment, prepares regulatory notification content, and oversees the post-breach review. Decides and submits notifications to supervisory authorities, with Legal Counsel review of content. Signs off on data subject communications. Represents the organization before regulatory authorities. |
| **Legal Counsel** | Determines notification obligations by jurisdiction. Advises on exemptions, litigation hold, evidence handling, and regulatory engagement strategy. Advises on the conflict-of-interest assessment before the Data Protection Officer takes command of a privacy response (section 3). Reviews and approves all regulatory and data subject notifications before submission. |
| **Security Operations Centre (SOC)** | Detects and triages security events that may constitute personal data breaches. Preserves evidence, executes technical containment, and provides forensic information to support the Data Protection Officer's impact assessment. |
| **IT Operations / System Owners** | Support data scope identification, access restriction, and deletion or recovery actions directed by the Data Protection Officer and CISO, subject to the technical direction and DPO consultation requirements in §3.1. |

Sector-conditional roles (for example, a BASC Regional Compliance Officer who is notified for any breach affecting trade, customs, or cargo records and coordinates sector-specific reporting, including to the authorities and the BASC Chapter) apply where the organization participates in a covered sector programme; see [`compliance/`](../compliance/).

### 2.2 Joint leadership

The CISO and Data Protection Officer are jointly responsible for initiating breach response the moment a potential personal data breach is identified. Closure requires agreement of the CISO and Data Protection Officer and CIO sign-off. Every privacy severity downgrade follows the Incident Commander approval and consultation requirement in section 3.

---

## 3. Breach severity classification

All suspected personal data breaches are classified at the point of initial detection and reassessed as additional information becomes available. Classification drives response SLAs, escalation paths, and resourcing. The Incident Commander for the privacy response is the Data Protection Officer when the incident is a privacy P1 but not a declared security-incident P1, or whenever the security procedure assigns no Incident Commander, at any privacy severity; otherwise, it is the Incident Commander assigned under [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md). Whenever a declaration, severity change, or security command reassignment changes the privacy Incident Commander under this rule, privacy command transfers immediately to the role specified by the rule, subject to the conflict-of-interest assessment below; the outgoing and incoming commanders must document the handover, including evidence status and pending decisions. The same handover record is required when a pending or inconclusive conflict-of-interest assessment later finds no conflict and privacy command passes from the CIO's pre-established alternate to the Data Protection Officer. Any privacy severity downgrade requires approval under section 3 before the resulting command transfer. The security procedure's Incident Commander rules continue to govern the security response, including its §2.2 rule for declared security-incident P1 incidents.

**Conflict-of-interest check before the Data Protection Officer takes command.** GDPR Article 38(6) allows the Data Protection Officer to fulfil other tasks and duties, and requires the controller or processor to ensure that any such tasks and duties do not result in a conflict of interests. Each time this rule would make the Data Protection Officer the privacy Incident Commander, a conflict-of-interest assessment must be documented in the breach record before the Data Protection Officer assumes command, with Legal Counsel advising. The assessment applies the Article 38(6) conflict-of-interest constraint in the DPO independence and conflict of interest section of [`privacy/charter-privacy-management-programme.md`](charter-privacy-management-programme.md): whether commanding this response would result in a conflict of interests, including whether it would have the Data Protection Officer determine, in whole or in part, the purposes and means of processing that the Data Protection Officer oversees. Where the assessment finds a conflict, the CIO designates the pre-established alternate as privacy Incident Commander in place of the Data Protection Officer. While the assessment is pending, or if it cannot reach a conclusion, it is treated as a conflict, so the CIO's pre-established alternate holds privacy command. The CIO names that alternate in advance, so the check does not delay the response. The Data Protection Officer keeps the responsibilities in section 2.1 that do not depend on holding command, including the notification decisions.

| Severity | Classification Criteria | Examples |
| --- | --- | --- |
| **P1: Critical** | Large-scale personal data exposure affecting 1,000 or more individuals (an internal P1 escalation trigger, not a statutory notification threshold; assess notification separately under §6); Restricted or sensitive personal data (health, financial, biometric, children's data) exfiltrated or exposed; BASC trade data breach with embedded personal data; credentials or encryption keys protecting personal data stores confirmed compromised; ransomware or destructive attack affecting systems holding personal data | Exfiltration of customer PII database; ransomware encrypting HR and payroll systems; confirmed compromise of credentials for the identity provider protecting personal data repositories; BASC cargo manifest breach disclosing shipper personal data at scale |
| **P2: High** | Moderate personal data exposure affecting fewer than 1,000 individuals; unauthorized access to Confidential personal data without confirmed exfiltration; accidental disclosure to an unintended recipient; supplier breach confirmed to have affected personal data held on the organization's behalf | Supplier notification of unauthorized access to a CRM extract; unauthorized internal access to payroll records |
| **P3: Medium** | Internal data only with no personal data; limited scope with no confirmed external disclosure; technical misconfiguration corrected before any confirmed access; minor policy violations | Configuration error exposing internal-only operational data to authenticated internal users; log file with non-personal technical data briefly publicly accessible |

Where criteria for more than one severity are met, the higher severity applies.

Severity is reassessed at each phase of the breach response lifecycle. Any team member may escalate severity upward. Every privacy severity downgrade requires Incident Commander approval, after consulting the appropriate roles (including the CIO, CISO, and Data Protection Officer, excluding whoever is acting as Incident Commander). This applies the approval and consultation requirement in [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) §3.2 to every privacy severity downgrade.

### 3.1 Evidence preservation obligation

For all P1 incidents, evidence preservation takes priority. At every privacy severity, systems must not be isolated, reimaged, or modified without direction from the Incident Commander assigned under [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) or, for P3 and P4 where no Incident Commander is assigned, the SOC lead, or, for P1 and P2 before an Incident Commander is assigned, the interim technical authority under that procedure's §2.2. P1, P2, P3 and P4 in this technical-direction rule are security severities under that procedure. These technical-direction requirements apply alongside the joint Data Protection Officer and CISO wipe-direction requirements in §5.2.1 rule 7 and the LOCK-ONLY action definition; wherever both apply, both must be satisfied. The Data Protection Officer must be consulted and briefed on evidence status before any action that could affect the privacy impact assessment.

---

## 4. Detection and initial assessment

### 4.1 Detection sources

Personal data breaches may be detected from any of the following sources:

- SIEM alerts or SOC investigations revealing unauthorized access to systems holding personal data.
- Endpoint detection and response (EDR) platform alerts indicating data exfiltration behaviour.
- Employee or contractor reports of lost devices, misaddressed email, or accidental disclosure.
- Supplier or processor notification of a breach affecting organizational data: suppliers (acting as data processors) must notify within 24 hours of *becoming aware* of a breach affecting organizational personal data per contractual data processing agreements. The 24-hour clock starts at the moment the processor becomes aware of the breach, not at the moment the controller is later notified (see §6.3 for the GDPR Article 33(2) basis for this asymmetry). The contractual 24 hours is an outer cap, not the statutory rule: where a law sets a stricter processor duty, that duty applies; for example, UAE Federal Decree-Law No. 45 of 2021 Art. 9(3) requires the processor to notify the controller "as soon as it becomes aware" of the breach (held as an unofficial English translation; the Arabic text is official).
- Regulator or law enforcement notification.
- Dark web monitoring alerting to the appearance of organizational data.
- BASC monitoring systems identifying anomalies in trade or customs data flows.

### 4.2 24-hour initial assessment

Within 24 hours of a potential personal data breach being identified, the Data Protection Officer and CISO jointly conduct an initial assessment, drawing in Legal where a determination requires it. Each determination has a named lead accountable for the answer:

| # | Determination | Lead |
| --- | --- | --- |
| 1 | **Is personal data involved?** Confirm whether the affected data includes information that identifies or is capable of identifying natural persons. | Data Protection Officer |
| 2 | **What is the likely scope?** Estimate the number of individuals affected, the categories of data involved, and the approximate volume of records. | Data Protection Officer |
| 3 | **Has data been accessed or exfiltrated?** Determine whether the breach is limited to availability impact (e.g., system outage) or includes confidentiality impact (unauthorized access or disclosure). | CISO |
| 4 | **What is the risk to individuals?** Assess the likely consequences for affected individuals, including risk of identity theft, financial harm, discrimination, reputational damage, or physical harm. | Data Protection Officer |
| 5 | **What is the applicable jurisdiction?** Identify which privacy laws govern the affected individuals and data. | Data Protection Officer, with Legal |
| 6 | **Is notification likely to be required?** Make a preliminary determination on whether regulatory or individual notification thresholds appear to be met, and in which jurisdictions. | Data Protection Officer, with Legal |

The assessment is documented and retained as part of the breach record.

### 4.3 AI and data-specific assessment considerations

Where the breach involves an AI system, an AI-supported workflow, or AI-related data assets, the Data Protection Officer additionally assesses each of the following dimensions during the initial assessment and revises the assessment as facts develop:

- Prompt or attached file data exposure to the model provider, intermediate logging tier, or downstream caller.
- Output disclosure of personal or regulated data, including hallucinated identifiers that may match real individuals.
- Retrieval leakage from a connected vector store, knowledge base, or document index.
- Training or fine-tuning data exposure, including review of contractual non-training clauses with the model provider.
- Model inversion or membership inference risk for any model trained or fine-tuned on personal data.
- Data poisoning effects on impacted individuals, including downstream decisions that may have been influenced.
- Supplier model or platform retention, including whether prompts, outputs, embeddings, or telemetry are retained beyond the contractual purpose.
- Logs, embeddings, vectors, caches, monitoring records, and the technical feasibility of deletion across each storage location.
- Provenance and lineage gaps that prevent a complete impact assessment, and the compensating evidence required to close the assessment.

---

## 5. Containment

### 5.1 Containment principles

Containment actions for personal data breaches follow the containment framework in [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) §5. The following privacy-specific principles additionally apply:

- **Do not destroy evidence.** No system, log, backup, or data record relevant to the breach may be deleted, overwritten, or modified pending the privacy impact assessment and regulatory notification determination. For a lost or stolen device, the decision table in §5.2.1 reconciles this principle with the §5.2 remote wipe: a wipe is permitted only where the duplicate-copy check in §5.2.1 (rule 7) confirms at decision time that the device holds a duplicate endpoint copy while the server-side records the assessment relies on are preserved, and where a legal hold or investigation applies the table selects a non-destructive action, with a forensic image first wherever the device is still reachable and rule 3 permits, and a wipe only after Legal Counsel, in writing, formally releases or narrows the hold (rule 8).
- **Scope isolation, not deletion.** Containment focuses on restricting further access to or exposure of personal data; premature deletion of breach-related data is prohibited unless specifically directed by Legal Counsel to meet a legal obligation.
- **Notify processors promptly.** If personal data held by a third-party processor is affected, the processor is notified immediately and directed to preserve evidence and assist with the impact assessment.

### 5.2 Containment actions

Containment actions vary by breach type:

| Breach Type | Typical Containment Actions |
| --- | --- |
| Unauthorized system access | Revoke compromised credentials; terminate active sessions; restrict access to affected systems; preserve authentication and access logs |
| Data exfiltration | Block egress channels identified as exfiltration routes; engage endpoint detection; preserve SIEM and network flow evidence |
| Accidental disclosure (email / file) | Request return or deletion of disclosed data from recipient; document recipient details; confirm whether data was accessed |
| Lost or stolen device | IT Operations must select the containment action for the device per the decision table in §5.2.1 (WIPE, LOCK-ONLY, or KEEP); the wipe obligations in this row apply where the table selects WIPE and the §5.2.1 rules (including the rule 7 duplicate-copy check) are satisfied, and §5.2.1 sets the lock and evidence obligations for the other outcomes, the interim lock where a wipe is deferred, and the forensic-image-first rule where a legal hold or investigation applies. IT Operations must initiate remote wipe of an organization-issued device via the endpoint management platform within 1 hour of notification, and must record the outcome, including where the device is not reachable. For a personally-owned device, IT Operations must initiate the route-appropriate wipe within 1 hour of notification, as the [BYOD Policy](../security/policy-byod.md) requires, through the applicable management platform: corporate application data only for MAM, without requiring device enrolment; the corporate container only for a managed work profile; or full-device wipe under MDM only with the owner's written, recorded consent expressly authorizing it, except where full-device wipe is required by law. For either ownership, and whichever action §5.2.1 selects, the corporate credentials and sessions associated with the device must be revoked through the enterprise identity provider within 1 hour of notification, at the same time as any wipe or lock is initiated. IT Operations must record the route, wipe scope and outcome, any consent reference or applicable legal requirement, device contents and encryption status; pending or failed wipe must not delay corporate access revocation. |
| Supplier breach | Invoke contractual breach notification clause; request evidence of containment from supplier; restrict supplier access pending investigation |
| BASC trade data breach | Notify Regional BASC Compliance Officer immediately; initiate BASC incident documentation; notify the authorities, and the BASC Chapter for record keeping, disclosing only the detail that the law in force permits (BASC International Standards Implementation Guide V6-2022); restrict access to affected customs and cargo systems |

#### 5.2.1 Lost or stolen device: WIPE, LOCK-ONLY, or KEEP

For a lost or stolen device, the evidence-preservation principle in §5.1 and the 1-hour remote wipe in §5.2 could pull in opposite directions: the wipe destroys the data on the device, and §5.1 prohibits destroying records relevant to the breach. This section reconciles them. The privacy impact assessment relies on the server-side records that §5.2 already requires (the endpoint-management inventory of device contents and encryption status, sync and access logs, and the wipe record itself), and a device wipe does not touch those records. Whether the contents of the device are only a duplicate endpoint copy of corporate data is a condition verified at decision time under rule 7, not an assumption: the endpoint inventory alone does not establish that unsynced local records or unique endpoint evidence are preserved elsewhere. Where rule 7 confirms duplication, wiping the device is scope isolation under §5.1, not evidence destruction. The device's contents and state are themselves evidence where a legal hold or an investigation applies to the device, its user, or the data on it. In that case preservation prevails: the default wipe is suspended and the decision table below governs.

For this section, a legal hold or investigation applies where a legal hold has been issued or is required because litigation, a regulatory investigation, or an audit is anticipated or underway (the legal-hold trigger in [`governance/register-data-retention-schedule.md`](../governance/register-data-retention-schedule.md)), where a retention hold has been applied or is required because a record on the device, or relating to its user or the data on it, is subject to audit, investigation, or litigation (the retention-hold trigger in [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md) §7), or where an investigation under [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) or by an external authority treats the device, its user, or the data on it as evidence. The breach assessment that this procedure opens for every lost or stolen device is not, by itself, an audit, investigation, or litigation for this purpose, and it does not require a retention hold on its own account; a hold that has in fact been applied still counts; otherwise every case would fall under the hold column and the No rows of the table would be unreachable. A legal hold that has been issued is recorded in the GRC platform, and a retention hold that has been applied is recorded in the Records Register. An investigation that treats the device, its user, or the data on it as evidence may appear in neither record, and neither record shows a hold that is required but not yet recorded; rule 2 therefore confirms both separately.

Actions under this section are subject to the technical-direction and DPO consultation requirements in §3.1. The following rules apply to every case:

1. **Credential and session revocation is unconditional.** Whichever action the table selects, the corporate credentials and sessions associated with the device must be revoked through the enterprise identity provider within 1 hour of notification (§5.2).
2. **Hold check before selecting the action.** Before selecting any action, and in every case before initiating any wipe, IT Operations must confirm whether a legal hold or investigation applies to the device, its user, or the data on it. The confirmation has two parts, and both must be complete. First, for recorded holds, IT Operations obtains the confirmation from Legal Counsel or checks both places where holds are recorded. Those places are the legal hold status tracked in the GRC platform (the Legal holds section of [`governance/register-data-retention-schedule.md`](../governance/register-data-retention-schedule.md)) and the retention hold status that the Compliance Manager tracks in the Records Register for records subject to audit, investigation, or litigation ([`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md) §7). A check of only one of those two records does not complete this part. Second, those records show only holds that have been recorded, so they cannot complete the confirmation on their own. Legal Counsel or the Incident Commander assigned under [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) or, for P3 and P4 where no Incident Commander is assigned, the SOC lead, or, for P1 and P2 before an Incident Commander is assigned, the interim technical authority under that procedure's §2.2, must confirm whether an investigation under that security procedure treats the device, its user, or the data on it as evidence; that is the only confirmation any of those security roles may give under this rule. P1, P2, P3 and P4 refer to security severities, as in §3.1. Only Legal Counsel may confirm whether an investigation by an external authority treats the device, its user, or the data on it as evidence, and whether a hold is required but not yet recorded. Where either part cannot be completed within 1 hour of notification, IT Operations must initiate a remote lock within the hour (non-destructive, or on a MAM-only device the application-layer containment defined under LOCK-ONLY), subject to the technical-direction and DPO consultation requirements in §3.1. IT Operations must then treat the case as one where a hold applies until both parts are complete. This applies on every row, including a row that would otherwise select KEEP.
3. **Forensic image first.** Wherever a legal hold or investigation applies and the device is still reachable through the endpoint management platform, a forensic image (or the fullest remote acquisition the platform supports) must be captured before any wipe, only as far as applicable law permits on Legal Counsel's advice (for a personally-owned device, the advice recorded for its route under Section 2 of the [BYOD Policy](../security/policy-byod.md) or, until that route's advice is recorded, Legal Counsel's advice on the case; for any other device, Legal Counsel's advice on the case), under direction from the Incident Commander assigned under [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) or, for P3 and P4 where no Incident Commander is assigned, the SOC lead, or, for P1 and P2 before an Incident Commander is assigned, the interim technical authority under that procedure's §2.2, and under that security procedure's §8 evidence-preservation requirements, aligned to ISO/IEC 27037:2012. P1, P2, P3 and P4 refer to security severities, as in §3.1. The Data Protection Officer must be consulted and briefed on evidence status before any action that could affect the privacy impact assessment, as required by §3.1. On a personally-owned device, acquisition is limited to the route's corporate scope, matching the wipe-scope boundaries of the [BYOD Policy](../security/policy-byod.md): corporate application data under MAM; the corporate container under a managed work profile; and, under MDM, the corporate applications, accounts, and data on the device, not the owner's personal content. Wider acquisition is permitted only where a legal obligation provides for it, or where the owner consents to it in writing and Legal Counsel has confirmed in the decision recorded for the route under Section 2 of the [BYOD Policy](../security/policy-byod.md) that such consent can serve as a valid lawful basis; until that route decision is recorded, wider acquisition on the owner's consent is unavailable.
4. **Encrypted means verified, effective at the time of loss, and uncompromised.** A device counts as encrypted only where all of the following are established at decision time: full-disk encryption that requires pre-boot authentication by a strong authenticator is verified through the endpoint management platform or key-escrow records as having been active at the time of loss, or, on a platform that cannot support pre-boot authentication (such as a smartphone), the platform-equivalent device encryption is so verified and releases its keys only after the user authenticates to the device with a strong authenticator; there is no indication that the device was lost or stolen while unlocked, or while powered on in standby with the encryption keys in memory; and the encryption key, recovery key, and gating authenticator are not compromised (for example, disclosed, recorded with the device, or exposed through a compromised escrow). Full-disk encryption that unlocks at start-up without the user authenticating (for example, a TPM-only configuration) does not meet the first condition, even where it meets the disk-encryption baseline of the [Endpoint Hardening Standard](../security/standard-endpoint-hardening.md). These conditions follow the held sources. NIST SP 800-111 §3.2 states: "For a computer that is not booted, all the information encrypted by FDE is protected, assuming that pre-boot authentication is required. When the device is booted, then FDE provides no protection; once the OS is loaded, the OS becomes fully responsible for protecting the unencrypted information." Its §3.1.1 notes, of the pre-boot authentication requirement, that "a PDA or smart phone could not display a keyboard on the screen for entering a password because that is an OS-level capability." The EDPB Guidelines 9/2022 (paragraph 80) warn that a device may be encrypted once it is switched off, but not while it is in stand-by mode. Where any of these conditions cannot be established, the device is treated as not encrypted; the decision is re-evaluated if the key or authenticator is later found to be compromised.
5. **Data class means the highest class present.** The data-class input is the highest classification of corporate data stored on or cached by the device according to the endpoint inventory, using the five levels of [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md): Public, Controlled, Internal, Confidential, Restricted. Where the highest class cannot be established, the device is treated as holding Restricted data.
6. **Queued actions on an unreachable device must be non-destructive where a hold applies.** Where a legal hold or investigation applies and the device is not reachable, IT Operations must queue a remote lock, not a wipe: a queued wipe would execute, and destroy evidence, the moment the device reconnects. A wipe may follow only under rule 8, once Legal Counsel has, in writing, formally released or narrowed the hold. Where a wipe was queued on an unreachable device while no hold applied, and a legal hold or investigation comes to apply before the device reconnects, IT Operations must cancel the queued wipe and queue a remote lock in its place as soon as it learns of the change.
7. **Duplicate-copy check before any wipe.** A wipe (of any scope, on any row) may be initiated only after IT Operations confirms, through the endpoint management sync and backup records and the server-side access logs, that the corporate data on the device is duplicated in managed server-side storage and that no unsynced local records or unique endpoint evidence relevant to the breach are known to exist only on the device. The endpoint inventory of contents alone does not establish this, and [`security/standard-endpoint-hardening.md`](../security/standard-endpoint-hardening.md) §7 backs up user data only where the role and data warrant it. Where duplication cannot be confirmed, or the device may hold the sole copy of relevant records, IT Operations must initiate LOCK-ONLY instead; the Data Protection Officer and CISO may jointly direct a wipe once preservation is confirmed, or rule 8 governs where a legal hold or investigation applies.
8. **A wipe under a hold requires the hold to be released or narrowed.** Where a legal hold or investigation applies, no wipe of any scope may be initiated, whatever imaging has been completed, until Legal Counsel, in writing, formally releases the hold or narrows it so that it no longer covers the device contents. This is consistent with [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md) §7 and the Legal holds section of [`governance/register-data-retention-schedule.md`](../governance/register-data-retention-schedule.md), each of which requires Legal Counsel's release or narrowing of a hold to be in writing. A forensic image under rule 3, including the fullest remote acquisition the platform supports, does not by itself satisfy this rule. Where an investigation applies without a legal hold, the equivalent of release or narrowing is Legal Counsel's written confirmation that the investigation no longer treats the device contents as evidence; references in this procedure to the release or narrowing of a hold include that confirmation. This is the single wipe-authority rule for every case where a hold or investigation applies.

The actions are defined as:

- **WIPE**: subject to rule 7, initiate the ownership- and route-scoped remote wipe described in §5.2 within 1 hour of notification. Where rule 3 requires a forensic image and the device is reachable, or rule 8 applies, initiate a remote lock within 1 hour of notification instead and initiate the wipe after the image is captured and, where a legal hold or investigation applies, only once rule 8 is satisfied.
- **LOCK-ONLY**: initiate a remote lock (and, where the platform supports them, passcode rotation and activation lock) within 1 hour of notification; do not destroy device contents, except through the MAM selective-wipe fallback described below and only under its conditions. On a MAM-only personal device, where the [BYOD Policy](../security/policy-byod.md) applies no device-level controls and no device lock is available, LOCK-ONLY is executed at the application layer within the same hour: credential and session revocation (rule 1), conditional-access blocking of the managed applications, and the MAM application PIN requirement; a selective wipe of the managed corporate application data (the BYOD Policy's MAM wipe scope) is the fallback where the platform cannot otherwise contain access, and, because it destroys the container contents, it is permitted only where no legal hold or investigation applies and rule 7 is satisfied, and, where a legal hold or investigation applies, only under rule 8, in either case subject to the technical-direction and DPO consultation requirements in §3.1. A later wipe requires rule 8 to be satisfied where a legal hold or investigation applies, or the direction of the Data Protection Officer and CISO jointly, subject to rule 7, where none does.
- **KEEP**: take no destructive or locking action against the device contents. Revoke credentials and sessions per rule 1, record the decision and its basis in the breach record, and re-evaluate if the encryption verification (including later compromise of the key or authenticator), the data-class information, or the legal hold or investigation status changes.

| Device encryption status | Highest data class on device | Legal hold or investigation | Action |
| --- | --- | --- | --- |
| Encrypted (verified per rule 4: pre-boot authentication or the platform equivalent required, active at the time of loss, not lost unlocked or in standby, key and authenticator not compromised) | Public or Controlled | No | KEEP |
| Encrypted (verified) | Internal | No | LOCK-ONLY |
| Encrypted (verified) | Confidential or Restricted | No | WIPE (defence in depth), subject to the rule 7 duplicate-copy check |
| Encrypted (verified) | Any | Yes | LOCK-ONLY within 1 hour; forensic image first wherever the device is reachable (rule 3); a later wipe only after the image and once rule 8 is satisfied |
| Not encrypted, or encryption unverified | Public | No | KEEP |
| Not encrypted, or encryption unverified | Controlled | No | LOCK-ONLY |
| Not encrypted, or encryption unverified | Internal, Confidential, or Restricted | No | WIPE within 1 hour (the §5.2 default), subject to the rule 7 duplicate-copy check |
| Not encrypted, or encryption unverified | Public or Controlled | Yes | LOCK-ONLY within 1 hour; forensic image wherever the device is reachable (rule 3); no wipe unless rule 8 is satisfied |
| Not encrypted, or encryption unverified | Internal, Confidential, or Restricted | Yes | LOCK-ONLY (remote lock) within 1 hour, then forensic image wherever the device is reachable (rule 3), then WIPE only once rule 8 is satisfied; where the device is not reachable, queue LOCK-ONLY (rule 6) pending that release or narrowing |

> **Encryption and the notification assessment.** Verified encryption bears on notification as well as containment. Under GDPR Article 34(3)(a), communication to data subjects is not required where the controller has applied measures that render the personal data unintelligible to any person who is not authorized to access it, such as encryption; the EDPB's Guidelines 9/2022 on personal data breach notification (Version 2.0, adopted 28 March 2023) treat the theft of securely encrypted media as possibly not reportable at all while the data are encrypted with a state-of-the-art algorithm, backups of the data exist, the key is not compromised, and the data can be restored in good time; paragraph 79 of the Guidelines adds that even where a backup exists, the loss may still be a reportable breach, depending on the length of time taken to restore the data from that backup. The KEEP and LOCK-ONLY rows for verified-encrypted devices rest on the same reasoning, which is why rule 4 also requires pre-boot authentication (or the platform equivalent), that the key and authenticator are not compromised, and that the device was not lost unlocked or in standby. The notification assessment in section 6 still runs for every lost or stolen device.

---

## 6. Notification assessment

### 6.1 Assessment framework

Following containment and initial assessment, the Data Protection Officer and Legal Counsel conduct a formal notification assessment determining:

- Whether a notifiable breach has occurred in each applicable jurisdiction.
- The deadline for regulatory notification.
- Whether data subjects must be individually notified, and which notification options the applicable law allows (for example, Australia Privacy Act 1988 s 26WL(2): take such steps as are reasonable in the circumstances to notify the contents of the statement to (a) each individual to whom the relevant information relates, where that is practicable, or (b) each individual who is at risk from the eligible data breach, where that is practicable; and (c) only if neither (a) nor (b) applies, publish a copy of the statement on the entity's website, if any, and take reasonable steps to publicise its contents).
- The content requirements for notifications.

The notification assessment is documented in the breach record and approved by the DPO before any notification is submitted.

### 6.2 Jurisdiction-specific notification requirements

| Jurisdiction | Governing Law | Regulatory Authority | Notification Trigger | Regulatory Deadline | Individual Notification |
| --- | --- | --- | --- | --- | --- |
| **European Union** | GDPR Arts. 33 to 34 | Relevant lead supervisory authority (EDPB member authority); where UK GDPR also applies, notify the UK regulator as well (see the United Kingdom row) | Personal data breach, unless unlikely to result in a risk to the rights and freedoms of natural persons (Art. 33(1); individuals notified where high risk, Art. 34(1)) | Without undue delay and, where feasible, within 72 hours of becoming aware (Art. 33(1)) | Without undue delay where the breach is likely to result in a high risk to individuals (Art. 34(1)) |
| **United Kingdom** | UK GDPR Arts. 33 to 34 | Information Commission | Same threshold as EU GDPR | Without undue delay and, where feasible, within 72 hours of becoming aware (UK GDPR Art. 33(1)) | Without undue delay where high risk |
| **Canada (Federal)** | PIPEDA (Breach of Security Safeguards Regulations); successor Bill C-36 (PPCDA) proposed, not in force | Office of the Privacy Commissioner of Canada (OPC) | Reasonable belief, in the circumstances, that the breach creates a real risk of significant harm to an individual (PIPEDA s. 10.1(1)) | As soon as feasible after the organization determines that the breach has occurred (PIPEDA s. 10.1(2); no fixed hour or day limit) | As soon as feasible after the organization determines that the breach has occurred, where it is reasonable in the circumstances to believe the breach creates a real risk of significant harm to that individual, unless otherwise prohibited by law (PIPEDA s. 10.1(3) and (6)) |
| **Quebec (Provincial)** | Quebec Law 25 (Bill 64); Act Respecting the Protection of Personal Information | Commission d'accès à l'information (CAI) | Confidentiality incident creating a serious injury risk | Promptly to the CAI (the Act sets no fixed hour-count); affected individuals must also be notified (the Act states the duty without a timeliness standard) | Promptly, as programme policy (the Act states no sequencing or timeliness standard) |
| **Ontario (public sector)** | FIPPA s. 40.1 (provincial institutions; in force since 2025-07-01); MFIPPA s. 30.1 (municipal institutions; not yet in force, comes into force 2027-01-01) | Information and Privacy Commissioner | Theft, loss or unauthorized use or disclosure of personal information in the institution's custody or control, where it is reasonable in the circumstances to believe that there is real risk that a significant harm to an individual would result, or other prescribed circumstances (FIPPA s. 40.1(1); from 2027-01-01, MFIPPA s. 30.1(1)) | As soon as feasible after the head determines that the theft, loss or unauthorized use or disclosure has occurred, with the prescribed information, in the prescribed form and manner (FIPPA s. 40.1(2); from 2027-01-01, MFIPPA s. 30.1(2)) | Unless otherwise prohibited by law, "if it is reasonable in the circumstances to believe that there is a real risk of significant harm to the individual or if any other prescribed circumstances exist", as soon as feasible after the head determines that the theft, loss or unauthorized use or disclosure has occurred; the notice contains a statement that the individual is entitled to make a complaint to the Commissioner and any other prescribed information, in the prescribed form and manner (FIPPA s. 40.1(3) and (4); from 2027-01-01, MFIPPA s. 30.1(3) and (4)) |
| **China** | PIPL Art. 57; Cybersecurity Law (CSL) Art. 44 para. 2, for network operators (网络运营者, which the CSL defines as the owners and managers of networks and network service providers, CSL Art. 78; CSL article numbers follow the amended numbering in force 1 January 2026; English rendering of the Chinese text, which is authoritative; its clause 按照规定及时告知用户并向有关主管部门报告 is the same Chinese wording the DSL translation renders as "promptly notifying users and reporting to relevant departments in charge as provided", DSL Art. 29); CSL Art. 27, for the same network operators, where the incident also endangers network security | Departments fulfilling personal information protection duties and responsibilities (PIPL Art. 60): the State cybersecurity and informatization department (国家网信部门, the same Chinese term the DSL translation's editor's note describes as a common reference to the Cyberspace Administration of China, CAC; the PIPL does not name the CAC), relevant State Council departments, and county-level and higher people's governments' relevant departments, whose duties are determined according to relevant State provisions; under the CSL, the relevant departments in charge (有关主管部门, CSL Art. 44 para. 2 and Art. 27) | A leak, distortion, or loss of personal information that has occurred or may occur (PIPL Art. 57); under the CSL, a leak, damage, or loss of personal information that has occurred or may occur (CSL Art. 44 para. 2), and an incident endangering network security (CSL Art. 27) | No fixed deadline under the PIPL (PIPL Art. 57 requires remedial measures immediately and notification of the departments, but sets no separate fixed time limit for notification); the CSL itself sets no fixed time limit and requires reporting as provided (按照规定) (CSL Art. 44 para. 2 requires remedial measures immediately and reporting to the relevant departments in charge promptly as provided; CSL Art. 27 requires activating the network security incident response plan immediately, taking corresponding remedial measures and reporting to the relevant departments in charge as provided); without delay, as programme policy. The CAC has issued National Cybersecurity Incident Reporting Measures (国家网络安全事件报告管理办法), which are not held in the reference base, so an adopter confirms directly their in-force date, any reporting time limits, and whether they apply <!-- ref-absence: National Cybersecurity Incident Reporting Measures --> | Required (PIPL Art. 57 sets no separate fixed time limit); promptly, as programme policy; under the PIPL, notification may be omitted only where measures taken are able to effectively avoid harm, subject to authority direction (the authority may still require it); CSL Art. 44 para. 2 requires a network operator to notify users promptly as provided and states no such exception |
| **India** | DPDPA 2023; Digital Personal Data Protection Rules 2025 | Data Protection Board of India (DPBI) | Personal data breach (failure to implement adequate security safeguards, or any breach affecting Data Principals) | Without delay, a description of the breach to the Board; within 72 hours of becoming aware (or a longer period the Board allows on a written request), a detailed report (Rule 7(2)); Rule 7 comes into force eighteen months after Gazette publication on 13 November 2025, on or about 13 May 2027 (Rule 1(4)) | Required once Rule 7 is in force: the Data Fiduciary must notify each affected Data Principal without delay (Rule 7(1)) |
| **Indonesia** | UU PDP (Law No. 27 of 2022) Art. 46 | Data protection institution (*lembaga*), established by the President (Art. 58(2)-(3)); confirm the current arrangement (see [`jurisdictions/annex-privacy-indonesia.md`](jurisdictions/annex-privacy-indonesia.md)) | Failure of personal data protection (Art. 46(1)) | Written notice within 3 x 24 hours to the data protection institution (Art. 46(1)(b)) | Written notice within 3 x 24 hours to the data subject (Art. 46(1)(a)); in certain cases the controller also notifies the public (Art. 46(3)) |
| **Brazil** | LGPD Arts. 48 to 49 | Agência Nacional de Proteção de Dados (ANPD) | Security incident that may cause risk or relevant harm to data subjects ("risco ou dano relevante"): it may significantly affect their interests and fundamental rights and involves at least one of: sensitive data; data of children, adolescents or older persons; financial data; authentication data; data under legal, judicial or professional secrecy; or large-scale data (Resolution CD/ANPD No. 15/2024 Art. 5) | 3 business days from awareness that the incident affected personal data, per Resolution CD/ANPD No. 15/2024 (the Security Incident Communication Regulation, dated 24 April 2024, verified against the ANPD publication 2026-07-07; staged communication permitted, complementary information within 20 business days; deadlines doubled for small-scale agents, the doubling confirmed against the primary Diário Oficial da União text (DOU 26 April 2024) per Article 6 §8 and Article 9 §6 ("contados em dobro")) | 3 business days from awareness, per the same regulation |
| **Turkey** | Law No. 6698 (KVKK) Art. 12(5) (English rendering of the Turkish text, which is authoritative) | Personal Data Protection Board (Kişisel Verileri Koruma Kurulu) | Processed personal data obtained by others through unlawful means (Art. 12(5)) | As soon as possible ("en kısa sürede", Art. 12(5)) | As soon as possible, to the data subject (Art. 12(5)); the Board may, where necessary, announce the breach on its website or by another method it considers appropriate |
| **United States** | State breach notification laws (varies) | Varies by state (e.g., State Attorney General) | Personal information of state residents exposed | Varies by state; refer to [`compliance/register-global-regulatory-applicability.md`](../compliance/register-global-regulatory-applicability.md) for current state-level mapping | Varies by state; generally without unreasonable delay |
| **United States (federal agencies)** | FISMA 2014, Pub. L. 113-283 §2(d) (44 U.S.C. 3553 note) | The committees of Congress the note names (an intelligence community element notifies only the appropriate committees, §2(d)(4)) | Unauthorized acquisition or access, under OMB data breach notification policies and guidelines (§2(d)(1)); §2(d)(1) directs the Director of OMB to ensure that those policies and guidelines require the notices in this row, so the agency's duty arises through OMB policy, not directly from the statute | Expeditiously and not later than 30 days after the agency discovered the unauthorized acquisition or access, as the OMB policies and guidelines are to require (§2(d)(1)(A)(i)) | As expeditiously as practicable and without unreasonable delay after the agency discovers the unauthorized acquisition or access (§2(d)(1)(B)); the Attorney General, the head of an intelligence community element, or the Secretary of Homeland Security may delay it if the notice would disrupt a law enforcement investigation, endanger national security, or hamper security remediation actions (§2(d)(2)) |

> **Note:** The GDPR Article 33(1) clock (without undue delay and, where feasible, within 72 hours) starts from the moment the controller becomes aware that a breach of personal data has occurred: not from the moment the breach occurred. "Becoming aware" is interpreted as when the controller has a reasonable degree of certainty that a security incident has taken place that has led to personal data being compromised.

> **Adopter register and internal target.** The table above is illustrative. The organization maintains its own applicable regulators, their current deadlines and triggers, and an **internal target** set tighter than each regulatory deadline, in the [breach-notification regulator register](template-breach-notification-regulator-register.md). This notification assessment consults that register to identify the controlling (strictest) regulatory deadline and the internal target the incident team runs to; where a breach engages more than one regime, the organization acts within the strictest applicable requirement (the earliest deadline and the broadest individual-notification obligation).

### 6.3 Supplier notification

Where a processor or sub-processor is involved, the organization:

- Notifies the processor of the breach (if the processor is the affected party, they must have already notified the organization within 24 hours of becoming aware per §4.1, or sooner where a law requires it; the 24 hours is an outer cap, §4.1).
- Coordinates to ensure that the processor preserves evidence and supports the impact assessment.
- Confirms contractual notification obligations have been met and documents the confirmation.

> **Note: processor-to-controller timeline asymmetry under GDPR Article 33(2).** The 24-hour contractual supplier clock and the Article 33(1) regulatory clock in §6.2 (without undue delay and, where feasible, within 72 hours of becoming aware) anchor to **two different awareness events**. GDPR Article 33(2) requires the processor to notify the controller "without undue delay after becoming aware" of a personal data breach. The contractual 24-hour window operationalizes that "without undue delay" for the organization's processors. The 24-hour clock therefore starts when the **processor** becomes aware of the breach, **not** when the controller is notified, **not** when the controller becomes aware, and **not** at any later containment or assessment milestone. The controller's Article 33(1) clock then starts when the controller becomes aware (typically on receipt of the processor's Article 33(2) notification), and from that point the controller must notify a notifiable breach to the supervisory authority without undue delay and, where feasible, within 72 hours. Where the controller first becomes aware of the breach through the processor's Article 33(2) notification, a processor that delays that notification delays the START of the controller's Article 33(1) clock (which runs from the controller's awareness, not from the breach itself), postponing the point at which the organization can assess the breach and notify the supervisory authority. Where the controller instead becomes aware independently and earlier (through any of the detection sources in section 4.1), its clock starts at that earlier awareness regardless of the processor's delay. The 24-hour contractual cap exists to minimize the delay before the organization becomes aware, not to protect an Article 33(1) notification window that has not yet begun to run. The EDPB's **Guidelines 9/2022 on personal data breach notification** (Version 2.0, adopted 28 March 2023) are the authoritative interpretation: once the controller has become aware, a notifiable breach must be notified without undue delay and, where feasible, not later than 72 hours, and Article 33(2) requires a processor that becomes aware of a breach to notify the controller without undue delay.

---

## 7. Notification content requirements

All regulatory and individual notifications must contain the following information to the extent known at the time of notification. Where information is not yet available, the notification states this and provides a timeline for supplementary notification.

### 7.1 Regulatory notification content

1. **Nature of the breach:** Description of what happened, when it occurred, and when it was discovered.
2. **Data categories and approximate volume:** Categories of personal data affected (e.g., contact details, financial data, health data, credentials) and approximate number of records and individuals affected.
3. **Likely consequences:** Assessment of the likely consequences of the breach for affected individuals.
4. **Measures taken or proposed:** Description of containment, mitigation, and remediation measures taken or planned.
5. **Contact details:** Name and contact details of the DPO for further liaison with the supervisory authority.
6. **Affected jurisdictions:** Where the breach affects individuals in multiple jurisdictions, the notification identifies the lead authority and confirms cross-border scope.
7. **Affected systems and presumed cause:** Where the applicable law requires them, the initial detail of the affected systems and the presumed cause of the breach (for example, Ecuador's LOPDP Regulation, Decreto Ejecutivo 904 of 2023, Art. 26, items 3 and 4; English rendering of the Spanish text, which is authoritative).

### 7.2 Individual notification content

Individual notifications are written in plain, accessible language and include:

1. A clear description of the nature of the breach.
2. The name and contact details of the Data Protection Officer.
3. A description of the likely consequences of the breach for the individual.
4. Actions taken by the organization to address the breach and mitigate its effects.
5. Steps the individual can take to protect themselves (e.g., change passwords, monitor financial accounts, contact credit bureaus; in the United States, where the individual suspects in good faith that they have been or are about to become a victim of fraud or related crime, including identity theft, ask a nationwide consumer reporting agency that maintains a file on them for a fraud alert; once the agency has received appropriate proof of identity, it keeps the alert in the file for not less than 1 year, unless the individual or their representative requests earlier removal and the agency has received appropriate proof of the requester's identity for that purpose, FCRA, 15 U.S.C. 1681c-1(a)(1)).
6. Where the applicable law requires them, the initial detail of the affected systems and the presumed cause of the breach (for example, Ecuador's LOPDP Regulation, Decreto Ejecutivo 904 of 2023, Art. 28, which carries the content of the notification to the authority, §7.1 item 7, into the notice to the data subject; English rendering of the Spanish text, which is authoritative).
7. Where Ontario FIPPA s. 40.1 applies (or, once it comes into force on 2027-01-01, Ontario MFIPPA s. 30.1), a statement that the individual is entitled to make a complaint to the Information and Privacy Commissioner, and any other prescribed information (FIPPA s. 40.1(4); from 2027-01-01, MFIPPA s. 30.1(4)).

Individual notifications must not contain information that could compromise an ongoing investigation. Legal Counsel reviews all individual notification content before distribution.

### 7.3 Phased notification

Where full information is not available within the notification deadline, a phased notification approach is used:

1. **Initial notification:** Submit within the regulatory deadline with available information, clearly indicating that the notification is being submitted in phases.
2. **Supplementary notification:** Submit additional information as it becomes available without undue delay, clearly cross-referencing the original notification.

---

## 8. Post-breach review

### 8.1 Post-incident review (PIR) requirement

A formal post-breach review (PIR) is mandatory for all P1 and P2 privacy breaches and must be completed within 5 business days of incident closure.

| Severity | PIR Required | Deadline |
| --- | --- | --- |
| P1: Critical | Mandatory | Within 5 business days of closure |
| P2: High | Mandatory | Within 5 business days of closure |
| P3: Medium | At Data Protection Officer discretion | Within 20 business days of closure |

### 8.2 PIR scope

The PIR addresses:

1. **Timeline reconstruction:** Complete chronology from initial data compromise to discovery, containment, notification, and closure.
2. **Root cause analysis:** The underlying control failure, process gap, or configuration weakness that caused or enabled the breach.
3. **Data impact assessment:** Final confirmed scope of affected individuals, data categories, and records.
4. **Notification compliance:** Whether all regulatory notification deadlines were met; explanation and documentation of any deadline exceptions.
5. **Detection effectiveness:** Time from breach occurrence to organizational awareness; assessment of whether monitoring controls were adequate.
6. **Control gaps:** Specific controls that failed, were absent, or were insufficient to prevent or detect the breach.
7. **Corrective actions:** Named control owners, remediation actions, implementation deadlines, and tracking mechanism.
8. **Risk register update:** Confirmation that existing risk entries have been re-scored or new risks added to reflect the lessons learned.

### 8.3 PIR output

The PIR report is classified Restricted. It is provided to the CIO, CISO, Data Protection Officer, and Internal Audit. Corrective actions are tracked in the privacy remediation register and reported at the quarterly Privacy Governance Review. Where the breach was subject to regulatory notification, the regulator may request the PIR findings as part of their investigation.

---

## 9. Record keeping

### 9.1 Breach register

The Data Protection Officer maintains a breach register documenting every suspected or confirmed personal data breach, regardless of whether regulatory notification was required. The breach register is a living document retained and available for regulatory inspection.

Each breach register entry includes:

| Field | Description |
| --- | --- |
| Breach ID | Unique identifier |
| Date and time of discovery | UTC |
| Date and time of occurrence (if known) | UTC or estimated range |
| Breach type | Unauthorized access / Accidental disclosure / Exfiltration / Lost device / Supplier breach / Other |
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

### 9.2 Evidence retention

All breach evidence, forensic artefacts, SIEM log exports, investigation records, containment records, notification drafts and submissions, authority correspondence, PIR reports, and corrective action records, must be retained for a minimum of 7 years, consistent with the retention schedule register ([`governance/register-data-retention-schedule.md`](../governance/register-data-retention-schedule.md)) and the holds regime in [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md).

Where Vietnam's Decree 356/2025/ND-CP applies to a violation involving location data or biometric data, the violation dossiers are kept for at least 5 years from the date the incident is fully remedied (Art. 29(1)(c), drawn from an unofficial English translation; the Vietnamese text is authoritative), and whichever period ends later applies.

Records subject to regulatory investigation, litigation hold, or authority request are retained until Legal Counsel, in writing, formally releases the hold or narrows it so that it no longer covers them.

### 9.3 Regulatory notification records

Copies of all submitted regulatory notifications, including phased supplementary notifications and authority correspondence, are retained in the breach case file as Restricted documents. Access is limited to the Data Protection Officer, CIO, CISO, and Legal Counsel.

---

## 10. Privacy breach-response execution checklist

This one-page checklist summarizes the time-phased actions for a P1 or P2 personal data breach. The privacy stream runs in parallel with the technical incident-response stream (§1.3); its clock keys on awareness of the breach. It is a quick-reference companion to Sections 4 to 7, not a replacement for them. An up-to-date hard copy of this procedure, as the written breach response plan, including this checklist and the contact information for communicating with external parties, stakeholders and regulators, is kept available for situations where soft copies are not available (CCCS Baseline Cyber Security Controls for Small and Medium Organizations V1.2, BC.1.2).

**First 60 minutes: initiate, joint command, protect evidence**

- The CISO and DPO jointly initiate breach response the moment a potential personal data breach is identified (§2.2, §1.3).
- Notify per severity: for a P1, the CISO, the DPO, and the CIO immediately (§2.1, §3).
- Where §3 would make the DPO the privacy Incident Commander, document the conflict-of-interest assessment, with Legal Counsel advising, before the DPO takes command; where it finds a conflict, the CIO designates the pre-established alternate; while it is pending, or if it cannot reach a conclusion, it is treated as a conflict and that alternate holds privacy command (§3).
- Protect evidence: do not delete, overwrite, or modify any system, log, backup, or data record pending the impact assessment and notification determination, except that for a lost or stolen device the §5.2.1 decision table and its rules govern whether and when the device may be wiped (lost or stolen device bullet below); obtain direction from the Incident Commander assigned under the security incident-response procedure or, for security P3 and P4 where no Incident Commander is assigned, the SOC lead, or, for security P1 and P2 before an Incident Commander is assigned, the interim technical authority (CISO or pre-authorized duty delegate), before isolating, reimaging, or modifying systems; consult and brief the DPO on evidence status before any action that could affect the privacy impact assessment; also satisfy the joint DPO and CISO wipe-direction requirements wherever §5.2.1 requires them (§3.1, §5.1, §5.2.1).
- If a third-party processor holds the affected data, notify it immediately to preserve evidence and confirm it notified the organization within its contractual window (§5.1, §6.3).
- For a lost or stolen device, IT Operations must select WIPE, LOCK-ONLY, or KEEP per the §5.2.1 decision table (hold check and duplicate-copy check before any wipe; forensic image first wherever a legal hold or investigation applies and the device is still reachable, as far as rule 3 permits), must initiate the selected ownership- and route-scoped wipe or lock under §5.2 and §5.2.1 within 1 hour of notification, except that where the §5.2.1 rules defer a WIPE pending a forensic image, confirmation of duplication, or Legal Counsel's release or narrowing of a hold, IT Operations must initiate a remote lock within the hour (as it must where the hold status cannot be confirmed within the hour, §5.2.1 rule 2) and wipe once those rules are satisfied, and must revoke the associated credentials and sessions within the same hour whichever action is selected.

**By 4 hours: contain by breach type**

- Responders must execute the privacy-specific containment for the breach type: revoke credentials and sessions for unauthorized system access; block exfiltration egress; request return or deletion for misdirected email or files; confirm the lost or stolen device action selected under the §5.2.1 decision table (WIPE, LOCK-ONLY, or KEEP), or the interim remote lock where §5.2.1 defers the wipe pending a forensic image, confirmation of duplication, or Legal Counsel's release or narrowing of a hold, and the concurrent credential and session revocation were initiated within 1 hour of notification under §5.2 and §5.2.1, including corporate-application containment for MAM without device enrolment and the forensic-image-first rule where a legal hold or investigation applies; invoke the supplier breach clause; for a trade-data breach notify the Regional BASC Compliance Officer (§5.2). Personal-device wipe must remain limited to corporate application data or the corporate work-profile container; full-device wipe under MDM must require the owner's written, recorded consent expressly authorizing it, except where required by law.
- Apply scope isolation, not deletion: restrict further access and exposure; no premature deletion unless directed by Legal Counsel (§5.1).
- Where an AI system or AI-related data asset is involved, begin the AI-specific assessment dimensions (§4.3).

**By 24 hours: complete assessment, engage notification**

- Complete the 24-hour initial assessment (personal data involved? scope? accessed or exfiltrated? risk to individuals? applicable jurisdiction? notification likely?) and retain it in the breach record (§4.2).
- Conduct the formal notification assessment with Legal Counsel (notifiable per jurisdiction? deadline? individual notification? content?); the DPO approves before any submission (§6.1).
- Initiate and track the jurisdictional notification clocks (for example, GDPR and UK GDPR without undue delay and, where feasible, within 72 hours of awareness, Quebec Law 25 promptly, PIPL and China Cybersecurity Law (CSL) Art. 44 para. 2 without delay, as programme policy (PIPL Art. 57 sets no separate fixed time limit for notification; the CSL itself sets no fixed time limit, and CSL Art. 44 para. 2 requires notifying users and reporting to the relevant departments in charge promptly as provided, 按照规定), CSL Art. 27, where the incident also endangers network security, without delay, as programme policy (the CSL itself sets no fixed time limit, and CSL Art. 27 requires activating the network security incident response plan immediately, taking corresponding remedial measures and reporting to the relevant departments in charge as provided, 按照规定), Brazil LGPD 3 business days per Resolution CD/ANPD No. 15/2024, verified 2026-07-07) (§6.2). For the CSL, the CAC has issued National Cybersecurity Incident Reporting Measures (国家网络安全事件报告管理办法), which are not held in the reference base, so an adopter confirms directly their in-force date, any reporting time limits, and whether they apply (§6.2). <!-- ref-absence: National Cybersecurity Incident Reporting Measures -->
- Open or update the breach register entry (§9.1).
- Initiate the post-incident review track, mandatory for P1 and P2, within 5 business days of closure (§8.1).

---

## 11. Metrics

The following metrics are tracked and reported to the CIO and CISO at the quarterly Privacy Governance Review:

| Metric | Definition | Target |
| --- | --- | --- |
| **Breaches by Severity** | Total personal data breaches confirmed in the reporting period, broken down by P1, P2, and P3 | Tracked; volume and severity trend monitored |
| **Regulatory Notification SLA Adherence (%)** | Percentage of notifiable breaches where regulatory notifications were submitted within the applicable jurisdictional deadline | 100% |
| **Mean Time to Notify (MTTN)** | Average time in hours from organizational awareness of a notifiable breach to submission of the regulatory notification | Target: ≤ 48 hours (an internal performance target). Assess each GDPR and UK GDPR notification against the Article 33(1) standard: without undue delay and, where feasible, within 72 hours of becoming aware. Assess each other notification against its own jurisdiction's deadline. |
| **Individual Notification Timeliness (%)** | Percentage of cases requiring individual notification where notification was issued without undue delay, in line with the applicable jurisdiction's timing | 100% |
| **PIR Completion Rate (%)** | Percentage of P1 and P2 breaches with PIR completed within 5 business days of closure | ≥ 95% |
| **Corrective Action Closure Rate (%)** | Percentage of PIR-identified corrective actions closed within their agreed deadline | ≥ 90% |
| **Supplier Breach Notification Timeliness** | Percentage of supplier-involved breaches where the supplier notified the organization within 24 hours of the *supplier's* awareness of the breach (the contractual operationalization of GDPR Article 33(2)'s "without undue delay" standard; see §6.3) | Tracked; persistent non-compliance triggers contract review |

---

## 12. Framework alignment

This table lists the primary breach-notification regimes and the frameworks this procedure aligns to. Other held sources that the body cites for a single requirement are cited where they apply and are not repeated here: Australia Privacy Act 1988 s 26WL (§6.1), UAE Federal Decree-Law No. 45 of 2021 Art. 9(3) (§4.1), FCRA, 15 U.S.C. 1681c-1(a)(1) (§7.2), Ecuador's LOPDP Regulation, Decreto Ejecutivo 904 of 2023, Arts. 26 and 28 (§7.1 and §7.2), Vietnam's Decree 356/2025/ND-CP Art. 29(1)(c) (§9.2), CCCS Baseline Cyber Security Controls for Small and Medium Organizations V1.2, BC.1.2 (§10), and the BASC International Standards Implementation Guide V6-2022 (§5.2).

| Control Area | Framework Reference |
| --- | --- |
| Privacy breach response programme | ISO/IEC 27701:2025 (privacy incident management); CSA CCM v4.1 SEF-08, SEF-03 |
| Regulatory breach notification: EU/UK | GDPR Arts. 33 to 34 (Art. 33(1) notification to the supervisory authority; Art. 34(1) communication to the data subject); UK GDPR Arts. 33 to 34; EDPB Guidelines 9/2022 on personal data breach notification (Version 2.0; paragraph 118: the number of affected individuals as one risk factor, while a breach can severely affect even one individual, depending on the nature of the data and the context) |
| Regulatory breach notification: Canada | PIPEDA Breach of Security Safeguards Regulations (successor Bill C-36/PPCDA proposed, not in force); Quebec Law 25; Ontario FIPPA s. 40.1 (in force since 2025-07-01); Ontario MFIPPA s. 30.1 (not yet in force; comes into force 2027-01-01) |
| Cyber security incident involving personal information: Canada (federal public sector) | GC Cyber Security Event Management Plan §2.3.1.4 (held text: date modified 2026-05-20, cited at the edition held, currency to be confirmed upstream); [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) §11; [`resilience/procedure-security-incident-reporting-and-escalation.md`](../resilience/procedure-security-incident-reporting-and-escalation.md) |
| Regulatory breach notification: China | PIPL Art. 57; Cybersecurity Law Art. 44 para. 2 and, where the incident also endangers network security, Art. 27 (amended numbering, in force 1 January 2026) |
| Regulatory breach notification: India | DPDPA 2023; Digital Personal Data Protection Rules 2025; DPBI |
| Regulatory breach notification: Indonesia | UU PDP (Law No. 27 of 2022) Art. 46 |
| Regulatory breach notification: Brazil | LGPD Arts. 48 to 49 |
| Regulatory breach notification: Turkey | Law No. 6698 (KVKK) Art. 12(5) |
| Regulatory breach notification: US | FISMA 2014 (44 U.S.C. 3553 note) for federal agencies; State breach notification laws; refer to [`compliance/register-global-regulatory-applicability.md`](../compliance/register-global-regulatory-applicability.md) |
| Security incident response | ISO/IEC 27035-1:2023; ISO/IEC 27035-2:2023; ISO/IEC 27035-3:2020; NIST SP 800-61 Rev. 3, including §2.3 (roles and authorities to confiscate, disconnect or shut down technology assets); [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) |
| Evidence preservation | ISO/IEC 27037:2012 §5.4.1 (minimize handling of the original; document unavoidable changes); [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) §8 |
| Lost or stolen device containment | NIST SP 800-124 Rev. 2 §4.3.3 (remote wipe scope and its limits as a sole control); ISO/IEC 27037:2012 §5.4.1; NIST SP 800-111 §§3.1.1 and 3.2 (pre-boot authentication); EDPB Guidelines 9/2022 (Version 2.0) paragraphs 78 to 80 and Annex B example (i); GDPR Art. 34(3)(a); [`security/policy-byod.md`](../security/policy-byod.md) |
| SIEM alert integration | CSA CCM v4.1 SEF-06; [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md) |
| Record keeping and retention | ISO/IEC 27701:2025 §7.5.3, Annex A.3.14; [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md) |
| AI training data leakage | ISO/IEC 27701:2025 Annex A.3.12; [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md) |
| BASC trade data | BASC International Standard v6; [`supply-chain/annex-trade-and-supply-chain-continuity-controls.md`](../supply-chain/annex-trade-and-supply-chain-continuity-controls.md) |

**Canadian federal public sector.** The GC Cyber Security Event Management Plan (held text: date modified 2026-05-20; the held edition is the one cited, and its currency is to be confirmed upstream) expects the appropriate authorities to be notified where personal information may be involved in a cyber security incident. For Government of Canada organizations subject to the Privacy Act and the Policy on Privacy Protection, that includes notifying the departmental Access to Information and Privacy (ATIP) office immediately to determine whether a privacy breach has occurred, and the plan says the process should involve an assessment of whether personal information may be involved (§2.3.1.4). The plan points to privacy breach plans and procedures set out in the Directive on Privacy Practices, which is not held in the reference base, so an adopter confirms them against the official text. <!-- ref-absence: Directive on Privacy Practices --> Reporting the cyber security incident to the Canadian Centre for Cyber Security runs in parallel, under the security incident response procedure §11.

---

*This document is released under the CC BY-SA 4.0 licence. See [`LICENSE`](../LICENSE) in the repository root.*

---

**End of Document**
