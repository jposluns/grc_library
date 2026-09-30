# Bring Your Own Device (BYOD) Policy

**Document Title:** Bring Your Own Device (BYOD) Policy\
**Document Type:** Policy\
**Version:** 1.3.2\
**Date:** 2026-09-30\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-acceptable-use.md`](policy-acceptable-use.md), [`security/standard-authentication-and-password-management.md`](standard-authentication-and-password-management.md), [`security/standard-remote-working-security.md`](standard-remote-working-security.md), [`security/standard-data-classification-and-handling.md`](standard-data-classification-and-handling.md), [`security/procedure-onboarding-and-offboarding.md`](procedure-onboarding-and-offboarding.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material platform, regulatory, or organizational change\
**Repository Path:** [`security/policy-byod.md`](policy-byod.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This policy governs the use of personally owned devices, including smartphones, tablets, and laptops, to access corporate data and applications. It defines the technical controls applied to personal devices, the obligations of the device owner, and the boundaries of the organization's access to the device.

This policy supports three peer BYOD routes: MAM (app-level), MDM (full-device), and managed work profile (containerized), defined in the next section. The adopting organization selects the route, or a combination of routes, that matches its risk appetite and data-sensitivity profile. The route chosen determines how much of the personal device the organization controls and what it may wipe.

---

## 2. BYOD deployment models

**Hold and investigation safeguard.** Every wipe authority and requirement in this document is subject to this safeguard, including selective, corporate-container and full-device wipes. Before initiating a wipe, IT Operations must confirm whether a legal hold or investigation applies to the device, its user, or the data on it, using the two-part confirmation in rule 2 of the lost or stolen device decision table in [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) §5.2.1. A check of the GRC platform and Records Register confirms only whether a hold is recorded. Under that rule, Legal Counsel or the Incident Commander confirms whether an investigation under [`security/procedure-security-incident-response.md`](procedure-security-incident-response.md) treats the device, its user, or the data on it as evidence. Only Legal Counsel confirms whether an investigation by an external authority treats the device, its user, or the data on it as evidence, and whether a hold is required but not yet recorded. Where a legal hold or investigation applies, or its status cannot be confirmed, IT Operations must suspend the wipe and follow the lost or stolen device decision table in [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) §5.2.1 and its rules for non-destructive containment, evidence preservation and any later wipe. This includes remote lock or MAM application-layer containment within 1 hour, forensic acquisition wherever the device is reachable, cancellation of queued wipes when a hold or investigation comes to apply, and no wipe until Legal Counsel formally releases or narrows the hold as rule 8 requires. For an investigation without a legal hold, rule 8 requires Legal Counsel's written confirmation that the investigation no longer treats the device contents as evidence. An image, backup, owner's consent or immediate-wipe deadline does not override this safeguard. Preserve the management capability needed for containment and evidence acquisition; defer deprovisioning, profile removal, unenrolment, reassignment or disposal where it would destroy evidence or prevent required preservation. Corporate access revocation must still meet its existing deadline. Record the hold check, deferred actions and Legal Counsel's release or confirmation. Where no legal hold or investigation applies, the existing wipe triggers, scope, consent requirements and deadlines continue to apply.

The organization may operate one or more of the three routes below (different routes for different device classes or data sensitivities). The choice is a risk decision the organization records in its control baseline.

- **Mobile application management (MAM), container model.** The organization controls a container of corporate applications and data on the personal device, enforced by application protection policies. The device itself is not enrolled and stays fully under the owner's control; the organization applies no device-level configuration and can wipe only the corporate container. MAM is the lighter-touch model, appropriate where the organization accepts application-layer control and does not require device-level assurance. The controls in the Approved access model section below are the MAM control set.
- **Mobile device management (MDM), full-device model.** The owner explicitly enrols the personal device into the organization's device-management platform, and the organization applies device-level policies (passcode strength, disk encryption, screen-lock timeout, OS-patch enforcement, configuration profiles) and may perform a full-device wipe. MDM gives the organization device-level assurance at the cost of greater control over a personally owned device. It requires the owner's informed, written, recorded consent expressly authorizing full-device wipe, because it extends the organization's reach beyond the corporate container.
- **Managed work profile, containerized model.** The organization enrols and manages a corporate work profile kept separate from the owner's personal data. Remote wipe must be limited to that container, and full-device wipe must not occur without the owner's written consent, except where required by law.

An organization choosing MDM must obtain and record the device owner's explicit enrolment consent before applying device-level policies, and must state in its enrolment notice what the organization can see, configure, and wipe. An organization choosing MAM applies the container controls below without device enrolment. The control baseline must map each supported device class and operating system to its approved routes and data classifications. Smartphones and tablets may use MAM, full-device MDM, or a managed work profile where the required controls are supported. Laptops may use MAM or full-device MDM; a managed work profile on a laptop requires verified container isolation and selective wipe. Unsupported class and route combinations must be denied. MDM and work-profile enrolment notices must disclose configuration, visibility and wipe scope, with written consent recorded before enrolment.

---

## 3. Scope

1. Applies to all employees, contractors, and consultants who choose to access corporate applications or data using a personally owned device.
2. Covers smartphones, tablets, and any other personal device used to access the cloud productivity platform (email, collaboration, file storage) or other corporate applications.
3. BYOD use is voluntary. Personnel are not required to use personal devices for work. Company-managed devices remain the standard for all work requiring access to Confidential or Restricted data.

---

## 4. Governance and accountability

| Role | Responsibility |
| --- | --- |
| **Chief Information Security Officer (CISO)** | Owns this policy; co-approves security-related exceptions per the §4.2.2 risk-tier pathway of the [Exception and Risk Acceptance Management Policy](../governance/policy-exception-and-risk-acceptance-management.md), including exceptions permitting Confidential data access from personal devices; oversees each configured BYOD route, including controls, enrolment notices and consent records for each deployed route. |
| **IT Operations** | Configures and maintains the controls for each deployed route, MAM application-protection policies and, under MDM, device-level policies and enrolment; monitors enrolment records; initiates the route-appropriate wipe (corporate-application wipe under MAM, container-only wipe under the managed-work-profile route, or consented full-device wipe under MDM) on departure per Section 10, subject to the hold and investigation safeguard in Section 2, and, on notification of device loss or theft, only where the lost or stolen device decision table in [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) §5.2.1 selects WIPE, or, on a MAM-only device where that table selects LOCK-ONLY, through the selective wipe of corporate application data that the table permits as the application-layer fallback, and only under that fallback's conditions; and, on notification that a device still in the owner's possession is compromised, within 1 hour of notification, subject to the hold and investigation safeguard in Section 2 (Section 9). |
| **Employees / Contractors** | Comply with all requirements in this policy when using personal devices for work purposes; report loss, theft, or suspected compromise immediately. |

---

## 5. Approved access model

Under the MAM model, personal devices may access corporate applications through the cloud productivity platform (email, collaboration, file storage) only. Access is governed by the following controls, enforced at the application and identity layer. The organization must enforce these controls under all three routes, with additional device or work-profile controls appropriate to the enrolled route:

| Control | Enforcement |
| --- | --- |
| **Identity verification** | Enterprise identity provider authentication with MFA required on every access attempt. Conditional access evaluates sign-in risk and user risk at each session. |
| **Application protection policy** | MAM app protection policies are applied to all cloud productivity applications on the device. |
| **No local data download** | Corporate data cannot be downloaded to local device storage. Documents, attachments, and files remain in cloud storage and are not cached locally outside the managed application container. |
| **No screenshots of managed applications** | Screenshots of managed application screens are blocked by MAM policy. |
| **Copy/paste restrictions** | Copy and paste between managed corporate applications and unmanaged personal applications is blocked. Corporate data cannot be transferred to personal email, personal notes, personal storage, or any unmanaged application. |
| **Data transfer restrictions** | Sharing or opening corporate files in unmanaged personal applications is blocked. Corporate attachments and documents can only be opened within applications covered by the MAM policy. |
| **Application PIN or biometric** | Access to managed corporate applications requires a PIN or biometric authentication in addition to device unlock, enforced by MAM policy. |
| **Remote wipe of corporate data** | Subject to the hold and investigation safeguard in Section 2, IT Operations may remotely wipe all corporate data from managed applications on the device. Under MAM the wipe is scoped to corporate application data, and under the managed-work-profile route to the corporate container; personal data, personal applications, and personal files on the device are not affected. A full-device wipe occurs only under MDM with the owner's written consent, or where required by law. |
| **Jailbreak and root detection** | Access from jailbroken or rooted devices is blocked by MAM policy. Devices that fail integrity checks are denied corporate data access. |
| **Minimum OS version** | MAM policy enforces minimum operating system versions. Devices running OS versions below the defined minimum are blocked from accessing corporate applications. |

---

## 6. What the organization does not do

Under the MAM model, the organization does not enrol personal devices into MDM, and the following actions are explicitly not taken:

- The organization does not apply device configuration profiles to personal devices.
- The organization does not manage device-level security settings (password policy, encryption, screen lock) on personal devices.
- The organization does not monitor personal application usage, browsing history, personal email, or personal files.
- The organization does not perform a full device wipe. Remote wipe is scoped to corporate application data only.
- The organization does not track device location.

These boundaries are properties of the MAM model. Under the MDM model the organization does apply device-level configuration and may perform a full-device wipe; that model requires the owner's explicit, written, recorded enrolment consent expressly authorizing full-device wipe (see the BYOD deployment models section), and the organization states in its enrolment notice what it can configure, see, and wipe. Under the managed-work-profile route the organization manages only the corporate work profile: it does not configure, monitor, or wipe the personal side of the device, and a full-device wipe requires the owner's written consent, except where required by law.

---

## 7. Data classification restriction

By default, personal devices may be used to access Internal and lower data classifications (Public, Controlled, and Internal per the [Data Classification and Handling Standard](standard-data-classification-and-handling.md)); access to Confidential or Restricted data from a personal device is governed by the managed-work-profile route and the conditions described below. The managed-work-profile route defined in the [Endpoint Management and Device Compliance Procedure](../operations/procedure-endpoint-management-and-device-compliance.md) section 8.2 is a standing approved path for access to Confidential or Restricted data from a personal device and does not require a per-device exception under Section 12. Outside that managed-work-profile route, access to data classified as Confidential or Restricted from a personal device is not permitted. Personnel with regular access requirements for Confidential data outside that managed-work-profile route must use a company-managed device. Where a specific business need requires Confidential access from a personal device outside that managed-work-profile route, an exception approved through the §4.2.2 risk-tier pathway of the [Exception and Risk Acceptance Management Policy](../governance/policy-exception-and-risk-acceptance-management.md) (with CISO co-approval as a security-related exception) is required and a compensating control plan must be documented.

---

## 8. Acceptable use on personal devices

When accessing corporate applications on a personal device, the Acceptable Use Policy applies in full to all corporate application activity. In particular:

- Corporate data must not be deliberately transferred to personal applications, personal email, or personal storage.
- Screen recording of corporate application content is prohibited.
- Any suspected corporate data exposure must be reported immediately to IT Security.

---

## 9. Incident and loss reporting

If a personal device with active access to corporate applications is lost, stolen, or compromised, the employee must notify the IT service desk immediately.

**Lost or stolen device.** Where the device is lost or stolen, IT Operations must select the containment action for the device (WIPE, LOCK-ONLY, or KEEP) per the lost or stolen device decision table in [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) §5.2.1, which decides by verified encryption status, the highest data class on the device, and legal hold or investigation status, and does not select a wipe in every case. Where that table selects WIPE, IT Operations must initiate the model-appropriate wipe within 1 hour of notification, or as that table's rules defer it with the interim lock they require: a selective wipe of corporate application data under the MAM model, a container-only wipe under the managed-work-profile route, or a full-device wipe under the MDM model only with the owner's written, recorded consent expressly authorizing it, except where required by law. Where the table selects LOCK-ONLY on a MAM-only device, on which the organization manages no device-level lock (Section 6), the lock is executed at the application layer as that table defines: credential and session revocation, conditional-access blocking of the managed applications, and the MAM application PIN, with a selective wipe of the corporate application data as a fallback only as that table permits. Where a legal hold or investigation applies to the device, its user, or the data on it, or the hold status cannot be confirmed within 1 hour of notification, any wipe is suspended and IT Operations must instead initiate a remote lock (or the MAM application-layer equivalent) and credential revocation within 1 hour, treat the case as held until both parts of the hold check in that table's rule 2 are complete, capture a forensic image wherever the device is still reachable, limited to the route's corporate scope as that table's rule 3 defines it unless the owner consents in writing to wider acquisition or a legal obligation provides for it, and wipe only after Legal Counsel formally releases or narrows the hold, as that table directs.

**Compromised device in the owner's possession.** Where the device is compromised but remains in the owner's possession, the lost or stolen device decision table does not select the action. IT Operations must initiate the model-appropriate wipe within 1 hour of notification: a selective wipe of corporate application data under the MAM model, a container-only wipe under the managed-work-profile route, or a full-device wipe under the MDM model only with the owner's written, recorded consent expressly authorizing it, except where required by law. This wipe is subject to the hold and investigation safeguard in Section 2: where a legal hold or investigation applies to the device, its user, or the data on it, or its status cannot be confirmed within 1 hour of notification, the wipe is suspended, IT Operations must instead initiate a remote lock (or the MAM application-layer containment) within 1 hour of notification, and no wipe may follow until Legal Counsel formally releases or narrows the hold, or confirms in writing that the investigation no longer treats the device contents as evidence, as that safeguard requires. A compromised device that is also lost or stolen follows the lost or stolen device paragraph above.

**Credential revocation and records.** Whichever action is taken under this section, including KEEP, the corporate credentials and sessions associated with the device must be revoked through the enterprise identity provider within 1 hour of notification, at the same time as any wipe or lock is initiated, and a pending, failed or suspended wipe must not delay that revocation. IT Operations must record the route, wipe scope and outcome, and any consent reference or applicable legal requirement. The individual is responsible for reporting the loss to their mobile carrier and taking appropriate personal data protection steps for the device itself.

---

## 10. Termination and offboarding

All route-specific wipes and any destructive deprovisioning, work-profile removal or unenrolment below are subject to the hold and investigation safeguard in Section 2. A preservation deferral must not delay corporate access revocation.

Upon departure, corporate access is removed from personal devices as part of the standard offboarding process. Under the MAM model, corporate application data is selectively wiped and personal data is unaffected; under the MDM model, where the enrolment consent terms require a full-device wipe, the wipe is performed while management remains available and the device is then unenrolled; otherwise the device is unenrolled. Under the managed-work-profile route, IT Operations must wipe the corporate container before removing its management. The individual does not need to surrender the device.

---

## 11. Policy violations

Violations of this policy, including attempts to circumvent MAM, MDM or managed-work-profile controls, deliberate data exfiltration to personal applications, or use of jailbroken devices, are subject to disciplinary action under the Acceptable Use Policy.

---

## 12. Exceptions

Exceptions to this policy are approved through the §4.2.2 risk-tier pathway of the [Exception and Risk Acceptance Management Policy](../governance/policy-exception-and-risk-acceptance-management.md), with CISO co-approval for security-related exceptions in addition to, not in place of, the risk-tier approver, with documented business justification, a compensating control plan, and a defined expiry date not exceeding 90 days; renewals follow that policy's §4.3.5 (original approving authority, then ERC, then Board Risk Committee) within the §4.3.4 cumulative ceiling. Exception records are retained for 7 years. The prohibition on accessing Restricted-classified data from a personal device outside the standing managed-work-profile route in Section 7 is absolute and is not subject to this exception process; Restricted access requires either that managed work profile or a company-managed device.

---

## 13. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27001:2022 | A.6.7, Remote working; A.8.1, User Endpoint Devices | BYOD controls, endpoint security requirements |
| NIST SP 800-124r2 | Guidelines for Managing the Security of Mobile Devices in the Enterprise | MDM and MAM architectures, mobile security controls |
| CSA CCM v4.1 | UEM-01 Endpoint Devices; UEM-03 Compatibility; UEM-13 Remote Wipe; IAM-13 Strong Authentication | Mobile endpoint management, BYOD access controls |
| NIST SP 800-63B | Digital Identity Guidelines: Authentication | MFA and conditional access requirements |

---

**End of Document**
