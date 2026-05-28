# Bring Your Own Device (BYOD) Policy

**Document Title:** Bring Your Own Device (BYOD) Policy  
**Document Type:** Policy  
**Version:** 1.0.0  
**Date:** 2026-05-27  
**Owner:** Chief Information Security Officer  
**Approving Authority:** Governance Library Maintainer  
**Related Documents:** [`security/policy-acceptable-use.md`](policy-acceptable-use.md), [`security/standard-authentication-and-password-management.md`](standard-authentication-and-password-management.md), [`security/standard-remote-working-security.md`](standard-remote-working-security.md), [`security/standard-data-classification-and-handling.md`](standard-data-classification-and-handling.md), [`security/procedure-onboarding-and-offboarding.md`](procedure-onboarding-and-offboarding.md)  
**Classification:** Public  
**Category:** Information Security  
**Review Frequency:** Annual and upon material platform, regulatory, or organisational change  
**Repository Path:** [`security/policy-byod.md`](policy-byod.md)  
**Confidentiality:** Public  
**Licence:** CC0 1.0 Universal  

---

## Purpose

This policy governs the use of personally owned devices — including smartphones, tablets, and laptops — to access corporate data and applications. It defines the technical controls applied to personal devices, the obligations of the device owner, and the boundaries of the organisation's access to the device.

The organisation's BYOD model uses mobile application management (MAM) without device enrolment. The organisation does not enrol personal devices into device management (MDM) and does not apply device-level policies. Controls are applied at the application and data layer only. The device itself remains under the full ownership and control of the individual.

---

## Scope

1. Applies to all employees, contractors, and consultants who choose to access corporate applications or data using a personally owned device.
2. Covers smartphones, tablets, and any other personal device used to access the cloud productivity platform (email, collaboration, file storage) or other corporate applications.
3. BYOD use is voluntary. Personnel are not required to use personal devices for work. Company-managed devices remain the standard for all work requiring access to Confidential or Restricted data.

---

## Governance and Accountability

| Role | Responsibility |
| --- | --- |
| **Chief Information Security Officer (CISO)** | Owns this policy; approves exceptions for Confidential data access from personal devices; oversees MAM policy configuration. |
| **IT Operations** | Configures and maintains MAM policies; monitors MAM enrolment records; initiates selective wipe on notification of device loss or departure. |
| **Employees / Contractors** | Comply with all requirements in this policy when using personal devices for work purposes; report loss, theft, or suspected compromise immediately. |

---

## Approved Access Model

Personal devices may access corporate applications through the cloud productivity platform (email, collaboration, file storage) only. Access is governed by the following controls, enforced at the application and identity layer:

| Control | Enforcement |
| --- | --- |
| **Identity verification** | Enterprise identity provider authentication with MFA required on every access attempt. Conditional access evaluates sign-in risk and user risk at each session. |
| **Application protection policy** | MAM app protection policies are applied to all cloud productivity applications on the device. |
| **No local data download** | Corporate data cannot be downloaded to local device storage. Documents, attachments, and files remain in cloud storage and are not cached locally outside the managed application container. |
| **No screenshots of managed applications** | Screenshots of managed application screens are blocked by MAM policy. |
| **Copy/paste restrictions** | Copy and paste between managed corporate applications and unmanaged personal applications is blocked. Corporate data cannot be transferred to personal email, personal notes, personal storage, or any unmanaged application. |
| **Data transfer restrictions** | Sharing or opening corporate files in unmanaged personal applications is blocked. Corporate attachments and documents can only be opened within applications covered by the MAM policy. |
| **Application PIN or biometric** | Access to managed corporate applications requires a PIN or biometric authentication in addition to device unlock, enforced by MAM policy. |
| **Remote wipe of corporate data** | IT Operations may remotely wipe all corporate data from managed applications on the device. The wipe is scoped to corporate application data only. Personal data, personal applications, and personal files on the device are not affected. |
| **Jailbreak and root detection** | Access from jailbroken or rooted devices is blocked by MAM policy. Devices that fail integrity checks are denied corporate data access. |
| **Minimum OS version** | MAM policy enforces minimum operating system versions. Devices running OS versions below the defined minimum are blocked from accessing corporate applications. |

---

## What the Organisation Does Not Do

The organisation does not enrol personal devices into MDM. The following actions are explicitly not taken under this policy:

- The organisation does not apply device configuration profiles to personal devices.
- The organisation does not manage device-level security settings (password policy, encryption, screen lock) on personal devices.
- The organisation does not monitor personal application usage, browsing history, personal email, or personal files.
- The organisation does not perform a full device wipe. Remote wipe is scoped to corporate application data only.
- The organisation does not track device location.

These boundaries are enforced by the MAM-without-MDM architecture. Enrolment of personal devices into MDM requires separate explicit consent and is not covered by this policy.

---

## Data Classification Restriction

Personal devices may only be used to access Internal and lower data classifications. Access to data classified as Confidential or Restricted from a personal device is not permitted. Personnel with regular access requirements for Confidential data must use a company-managed device. Where a specific business need requires Confidential access from a personal device, written CISO approval is required and a compensating control plan must be documented.

---

## Acceptable Use on Personal Devices

When accessing corporate applications on a personal device, the Acceptable Use Policy applies in full to all corporate application activity. In particular:

- Corporate data must not be deliberately transferred to personal applications, personal email, or personal storage.
- Screen recording of corporate application content is prohibited.
- Any suspected corporate data exposure must be reported immediately to IT Security.

---

## Incident and Loss Reporting

If a personal device with active access to corporate applications is lost, stolen, or compromised, the employee must notify the IT service desk immediately. IT Operations will initiate a selective wipe of corporate application data within 1 hour of notification. The individual is responsible for reporting the loss to their mobile carrier and taking appropriate personal data protection steps for the device itself.

---

## Termination and Offboarding

Upon departure, all corporate application data is selectively wiped from personal devices as part of the standard offboarding process. The individual does not need to surrender the device. Corporate applications and data are removed; the device and personal data are unaffected.

---

## Policy Violations

Violations of this policy — including attempts to circumvent MAM controls, deliberate data exfiltration to personal applications, or use of jailbroken devices — are subject to disciplinary action under the Acceptable Use Policy.

---

## Exceptions

Exceptions to this policy require CISO approval, documented business justification, a compensating control plan, and a defined expiry date not exceeding 90 days. Exception records are retained for 7 years.

---

## Framework Alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27001:2022 | A.6.2 — Teleworking; A.8.1 — User Endpoint Devices | BYOD controls, endpoint security requirements |
| NIST SP 800-124r2 | Guidelines for Managing the Security of Mobile Devices in the Enterprise | MAM-without-MDM architecture, mobile security controls |
| CSA CCM v5 | UEM-03, UEM-06 — Mobile Device Management and BYOD | Mobile endpoint management, BYOD access controls |
| NIST SP 800-63B | Digital Identity Guidelines — Authentication | MFA and conditional access requirements |

---

**End of Document**
