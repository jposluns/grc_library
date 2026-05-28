# IT Onboarding and Offboarding Procedure

**Document Title:** IT Onboarding and Offboarding Procedure 
**Document Type:** Procedure 
**Version:** 1.0.1 
**Date:** 2026-05-28 
**Owner:** Chief Information Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/policy-acceptable-use.md`](policy-acceptable-use.md), [`security/standard-privileged-access-management.md`](standard-privileged-access-management.md), [`operations/procedure-endpoint-management-and-device-compliance.md`](../operations/procedure-endpoint-management-and-device-compliance.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md) 
**Classification:** Public 
**Category:** Information Security 
**Review Frequency:** Annual and upon material change 
**Repository Path:** [`security/procedure-onboarding-and-offboarding.md`](procedure-onboarding-and-offboarding.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## 1. Purpose

This procedure governs the provisioning and deprovisioning of system access and IT assets across the full personnel lifecycle: pre-joining, first-day onboarding, role transfers and changes, voluntary departure, and involuntary termination. It ensures that access rights are granted on a least-privilege basis, are aligned to approved role profiles, and are removed promptly and completely when no longer required.

This procedure supports the Information Security Policy and aligns to ISO/IEC 27001:2022 Annex A controls A.6.1 (Screening), A.6.2 (Terms and conditions of employment), and A.6.5 (Responsibilities after termination or change of employment), NIST SP 800-53 Rev. 5 PS (Personnel Security) control family, and CIS Controls v8 Control 5 (Account Management).

---

## 2. Scope

2.1 This procedure applies to all employees (permanent and fixed-term), contractors, consultants, and third-party workers who are granted access to any organisational system, application, network, or physical IT asset.

2.2 It covers all user account types including standard user accounts, privileged accounts, shared accounts, service accounts provisioned to individuals, and third-party portal credentials.

2.3 It applies regardless of whether personnel are onboarded or offboarded locally or remotely, and regardless of whether access is to on-premises, cloud, or hybrid systems.

2.4 Physical access (key cards, building access) is subject to separate facilities management processes but is included in the deprovisioning checklist in Section 10 to ensure that coordinated revocation.

---

## 3. Governance and accountability

| Role | Responsibility |
| --- | --- |
| Chief Information Officer (CIO) | Owns this procedure. Ensures that IT Operations has capacity and processes to meet the timelines defined herein. Receives escalated exceptions. |
| Chief Information Security Officer (CISO) | Provides oversight of access provisioning governance. Reviews privileged access provisioning and deprovisioning. Receives reports on deprovisioning SLA compliance. |
| Human Resources (HR) | Triggers all onboarding and offboarding notifications to IT Operations within the timeframes specified. Notifies IT Operations of role changes within 24 hours of approval. Owns the hire, departure, and role-change notification forms. |
| IT Operations | Executes account provisioning and deprovisioning. Maintains access profiles per role. Manages the deprovisioning checklist. Reports SLA compliance monthly to the CISO and CIO. |
| Line Manager | Provides business approval for access requests that deviate from the standard role profile. Confirms departure dates and manages device collection for voluntary departures. Notified at the time of involuntary termination. |
| Internal Audit | Periodically samples deprovisioning records to verify completeness and timeliness. |

---

## 4. Pre-joining and hire notification

### 4.1 HR notification to IT operations

4.1.1 HR must notify IT Operations of a new hire a minimum of 5 business days before the individual's start date. The notification must include:

| Field | Notes |
| --- | --- |
| Full legal name | As it will appear in the identity directory |
| Job title and department | Used to match against the access profile matrix |
| Start date | Required for device preparation and account activation scheduling |
| Manager name and department | For approval chain configuration |
| Access profile required | Standard role profile or custom (custom requires line manager written approval) |
| Device type required | Laptop, desktop, mobile device, or combination |
| Remote or on-site working | Affects device configuration and VPN provisioning |
| Elevated or privileged access | Flagged for CISO awareness; requires separate PAM onboarding |

4.1.2 Late notification (fewer than 5 business days) must be approved by the CIO and may result in delayed account activation or device availability on the start date. IT Operations will communicate any delays to HR and the line manager.

### 4.2 Provisional account creation

4.2.1 Upon receipt of a valid hire notification, IT Operations will create the individual's account in the enterprise identity provider in a provisional (disabled) state.

4.2.2 Provisional accounts must not be activated until the individual's confirmed start date.

4.2.3 Role-based access permissions are configured against the pre-approved access profile for the role. Any access that exceeds the standard role profile requires written approval from the line manager and, for Confidential or Restricted data access, the CISO or data owner.

---

## 5. First-day provisioning

### 5.1 Device readiness

5.1.1 A configured, enrolled, and compliant managed device must be available for the individual on their first working day. The device will be enrolled in the endpoint management platform and meet the endpoint configuration baseline.

5.1.2 For remote joiners, the device must be shipped in advance to arrive before the start date, or alternative arrangements confirmed with IT Operations and the line manager.

### 5.2 Credential issuance

5.2.1 Initial credentials (username and temporary password) must be issued in one of the following secure ways only:

- In person at the IT service desk or office location, with identity verified against a government-issued photo ID
- Via a secure one-time link delivered to the individual's personal email address (pre-registered with HR during the hiring process) that expires after first use and within 24 hours of generation

5.2.2 Credentials must not be sent in plain text via email, instant message, or any other unencrypted channel.

5.2.3 The individual must change their temporary password on first login.

### 5.3 Multi-factor authentication enrolment

5.3.1 MFA must be enrolled on the individual's first working day, before access to any Confidential or Restricted data is granted.

5.3.2 IT Operations will guide first-day MFA enrolment as part of the standard onboarding session.

5.3.3 MFA requirements are governed by the Authentication and Password Management Standard.

### 5.4 Role-based access provisioning

5.4.1 Access is provisioned in accordance with the pre-approved role access profile. Access beyond the standard profile is not activated until line manager written approval is confirmed.

5.4.2 Privileged access (administrator accounts, service accounts) is subject to the Privileged Access Management Standard and must not be provisioned as part of first-day standard onboarding without CISO notification.

5.4.3 Access to the collaboration platform, cloud productivity platform, collaboration and file storage platform, and other standard productivity tools will be activated on day one as part of the standard role profile.

---

## 6. Role changes and transfers

### 6.1 HR notification

6.1.1 HR must notify IT Operations within 24 hours of a role change or internal transfer being approved. The notification must include the individual's name, previous role, new role, effective date of change, and any changes to access requirements.

### 6.2 Access review

6.2.1 An access review for the transferred individual must be triggered within 3 business days of HR notification.

6.2.2 The access review will compare the individual's current access rights against the access profile for their new role. Any access that is no longer required in the new role is classified as excess access.

### 6.3 Excess access removal

6.3.1 All excess access identified in the access review must be removed within 5 business days of HR notification.

6.3.2 Where the line manager believes that transitional access to the former role's systems is temporarily necessary, they must submit a written request to IT Operations and the CISO. Transitional access may be granted for a maximum of 30 days and must be fully removed thereafter.

6.3.3 Privileged access associated with the former role must be revoked within 2 hours of the effective date of the role change, consistent with the timeline in Section 9.

---

## 7. Voluntary departure

### 7.1 Notice and pre-departure preparation

7.1.1 HR must notify IT Operations a minimum of 5 business days before the individual's last working day. Where notice is shorter (e.g., immediate resignation), IT Operations must be notified on the same day.

7.1.2 IT Operations will initiate the deprovisioning checklist (Section 10) upon receipt of departure notification.

### 7.2 Last working day

7.2.1 All user accounts for the departing individual must be suspended (not merely password-reset) at the end of their last working day. Suspension means the account is disabled in the enterprise identity provider and cannot be used to authenticate.

7.2.2 Active sessions must be terminated and refresh tokens revoked at the time of account suspension.

### 7.3 Post-departure account deletion

7.3.1 All accounts must be fully deprovisioned (deleted or permanently disabled) within 7 calendar days of the individual's last working day, unless a longer retention period is required for legal hold, investigation, or data retrieval purposes approved by the CISO or Legal.

### 7.4 Device collection

7.4.1 The managed device must be collected on or before the individual's last working day. The line manager is responsible for coordinating device collection.

7.4.2 Where in-person collection is not possible (e.g., remote worker), a prepaid return courier must be arranged by IT Operations and the device must be received within 5 calendar days of the last working day.

7.4.3 Remote wipe will be initiated via the endpoint management platform if the device is not returned within the required timeframe.

### 7.5 Data retrieval

7.5.1 Any organisational data stored in the individual's collaboration and file storage platform workspace must be reviewed and, where required, transferred to the line manager or a designated successor within 7 calendar days of departure.

7.5.2 Personal email forwarding from a corporate account to a personal account must not be set up and will be removed as part of the deprovisioning checklist.

---

## 8. Involuntary departure

### 8.1 Account suspension

8.1.1 In the event of involuntary termination (dismissal, redundancy with immediate effect, or any termination where the individual is not permitted to work their notice), all accounts must be suspended on the same business day, effective at the time the termination decision is implemented.

8.1.2 Where possible, account suspension should be coordinated to occur at the same time as, or immediately before, the individual is informed of the termination.

### 8.2 Access removal timeline

8.2.1 All access must be fully removed within 4 hours of the suspension instruction being received by IT Operations. This includes:

- Enterprise identity provider account suspension
- Revocation of all active sessions and tokens
- Removal from all security groups and distribution lists
- Revocation of VPN certificates
- Suspension of collaboration platform access

### 8.3 Device collection

8.3.1 The managed device must be collected on the same day as termination where the individual is on site. Where same-day collection is not possible, the device must be collected or secured within 1 business day.

8.3.2 IT Operations must initiate a remote wipe via the endpoint management platform immediately if there is any risk that the individual may attempt to access or remove data from the device before collection.

### 8.4 Line manager notification

8.4.1 The individual's line manager will be notified at the time the termination decision is communicated, to coordinate device return and brief their team as appropriate.

8.4.2 HR retains responsibility for communicating the termination to IT Operations and initiating the deprovisioning workflow.

---

## 9. Contractor and third-party offboarding

9.1 Contractors and third-party workers with system access are subject to the same deprovisioning timelines as employees (Sections 7 and 8, as applicable depending on whether departure is voluntary or involuntary).

9.2 Third-party system access, including access to client portals, supplier systems, or external platforms, must be reviewed and removed as part of the deprovisioning checklist.

9.3 Where a contractor or third-party worker shared credentials with other members of their organisation (e.g., a shared service account for a supplier), those shared credentials must be rotated immediately upon the individual's departure, regardless of whether other authorized users continue to require access.

9.4 IT Operations must confirm with the relevant line manager or contract owner that all third-party access has been removed before closing the offboarding record.

---

## 10. Privileged access deprovisioning

10.1 All privileged accounts held by a departing individual, including local administrator accounts, domain administrator accounts, cloud platform administrative roles, PAM vault accounts, and any other elevated access, must be reviewed and revoked within 2 hours of the departure notification being received by IT Operations.

10.2 This timeline applies to both voluntary and involuntary departures. For involuntary departures, privileged access revocation is the first priority action, preceding completion of all other deprovisioning steps.

10.3 Service accounts that are registered to or owned by the departing individual must be addressed as follows:

| Scenario | Required Action |
| --- | --- |
| Service account used by systems the individual managed | Re-assign ownership to another authorized IT staff member immediately |
| Service account used only by the departing individual | Disable the service account immediately; confirm with the application owner that no downstream dependency exists before permanent deletion |
| Service account credentials known only to the departing individual | Reset credentials immediately; document and re-issue to the new owner |

10.4 IT Operations must report completion of privileged access deprovisioning to the CISO within 24 hours of the departure event.

---

## 11. Deprovisioning checklist

The following checklist must be completed for every departure. IT Operations is responsible for completion and verification. The completed checklist is retained as an evidence record.

| # | Action Item | Responsible Party | Target Timeline | Verification Step |
| --- | --- | --- | --- | --- |
| 1 | User account disabled in enterprise identity provider | IT Operations | Last day (voluntary) / 4 hours (involuntary) | Confirm account status in identity provider console |
| 2 | All active sessions terminated and refresh tokens revoked | IT Operations | Simultaneous with account disable | Session log confirms no active sessions |
| 3 | MFA tokens and authenticator app enrolments removed | IT Operations | Within 4 hours of departure | MFA device list confirmed empty |
| 4 | VPN certificate revoked | IT Operations | Within 4 hours of departure | Certificate revocation confirmed in PKI management console |
| 5 | Email access removed and mailbox converted or archived | IT Operations | Last day (voluntary) / 4 hours (involuntary) | Mailbox status confirmed in mail admin console |
| 6 | Email forwarding to personal account removed and blocked | IT Operations | Last day | Mail routing confirmed; no forwarding rules active |
| 7 | Shared mailbox access removed | IT Operations | Within 24 hours | Access list confirmed in mail admin console |
| 8 | Collaboration platform access removed | IT Operations | Within 4 hours of departure | User removed from collaboration platform tenant |
| 9 | Collaboration and file storage platform access removed | IT Operations | Within 4 hours of departure | Access confirmed removed; data transferred to line manager |
| 10 | Managed device returned and confirmed received | Line Manager / IT Operations | Last day (voluntary) / 1 business day (involuntary) | Device serial number recorded as returned; chain of custody documented |
| 11 | Remote wipe of managed device initiated (if not returned) | IT Operations | Within 1 business day of non-return | Wipe confirmation recorded from endpoint management platform |
| 12 | All privileged accounts revoked | IT Operations | Within 2 hours of departure notification | PAM vault audit confirms no active privileged sessions |
| 13 | Service accounts re-assigned or disabled | IT Operations | Within 2 hours of departure notification | Service account ownership register updated |
| 14 | Service desk / ITSM account closed | IT Operations | Within 7 calendar days | Account status confirmed in ITSM system |
| 15 | Third-party portal access removed | IT Operations / Line Manager | Within 7 calendar days | Each portal confirmed; documented in offboarding record |
| 16 | Shared credentials rotated (contractors/third parties) | IT Operations | Immediately upon departure | Credential rotation confirmed; new credentials distributed to remaining authorized users |
| 17 | Physical access cards and office keys returned | Facilities / Line Manager | Last day | Facilities receipt or confirmation email |
| 18 | Security group and distribution list memberships removed | IT Operations | Within 24 hours | Directory groups confirmed |
| 19 | Software licences released and reclaimed | IT Operations | Within 7 calendar days | Licence management platform updated |
| 20 | Offboarding record completed and filed | IT Operations | Within 7 calendar days of departure | Record accessible in ITSM with all checklist items verified |

---

## 12. Evidence and records retention

12.1 A completed deprovisioning checklist record must be created and retained for every individual offboarded, without exception.

12.2 Deprovisioning records must be retained for a minimum of 7 years from the date of departure. This supports audit requirements, regulatory inquiry, and legal proceedings.

12.3 Records must be stored in the organisation's approved records management system with access restricted to IT Operations, CISO, CIO, HR, and Internal Audit.

12.4 Onboarding records (access provisioning approvals, role-profile assignments, initial MFA enrolment confirmation) must similarly be retained for 7 years from the date of offboarding of the individual to whom they relate.

12.5 Records must be retained and destroyed in accordance with the Records Retention and Destruction Standard.

---

## 13. Framework alignment

| Framework | Reference | Alignment |
| --- | --- | --- |
| ISO/IEC 27001:2022 | A.6.1 Screening | Pre-joining verification and account creation in provisional state |
| ISO/IEC 27001:2022 | A.6.2 Terms and conditions of employment | Access provisioning tied to accepted terms; acknowledgement required before access granted |
| ISO/IEC 27001:2022 | A.6.5 Responsibilities after termination or change of employment | Deprovisioning timelines, device return, data handling post-departure |
| ISO/IEC 27001:2022 | A.5.18 Access rights | Role-based provisioning, excess access removal, and access review on role change |
| ISO/IEC 27001:2022 | A.8.11 Data masking; A.8.12 Data leakage prevention | Data retrieval and forwarding controls on departure |
| ISO/IEC 27002:2022 | §6.5 Responsibilities after termination or change of employment | Detailed implementation guidance for offboarding controls |
| NIST SP 800-53 Rev. 5 | PS-4 Personnel Termination | Account suspension, credential revocation, device return timelines |
| NIST SP 800-53 Rev. 5 | PS-5 Personnel Transfer | Access review and excess access removal on role change |
| NIST SP 800-53 Rev. 5 | PS-6 Access Agreements | Acknowledgement of acceptable use prior to access provisioning |
| NIST SP 800-53 Rev. 5 | AC-2 Account Management | Account lifecycle management from provisioning to deprovisioning |
| CIS Controls v8 | Control 5 (Account Management) | Account provisioning, deprovisioning, and access review processes |
| CIS Controls v8 | Control 6 (Access Control Management) | Least-privilege access, role-based profiles, privileged account management |

---

**End of Document**
