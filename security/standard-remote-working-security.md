# Remote Working Security Standard

**Document Title:** Remote Working Security Standard\
**Document Type:** Standard\
**Version:** 1.0.7\
**Date:** 2026-06-29\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/policy-acceptable-use.md`](policy-acceptable-use.md), [`security/standard-authentication-and-password-management.md`](standard-authentication-and-password-management.md), [`operations/procedure-endpoint-management-and-device-compliance.md`](../operations/procedure-endpoint-management-and-device-compliance.md), [`security/standard-data-classification-and-handling.md`](standard-data-classification-and-handling.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material change\
**Repository Path:** [`security/standard-remote-working-security.md`](standard-remote-working-security.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines the minimum security requirements for personnel working remotely: that is, working from any location outside a corporate office, including home, hotels, client sites, co-working spaces, and public locations. It establishes enforceable requirements for device security, network usage, physical workspace protection, and data handling when work is conducted outside the controlled office environment.

This standard supports the Information Security Policy, the Acceptable Use Policy, and the Authentication and Password Management Standard, and aligns to ISO/IEC 27001:2022 Annex A control A.6.7 (Remote working).

---

## 2. Scope

2.1 This standard applies to all employees, contractors, consultants, and third-party workers who access organisational systems, applications, or data from any location outside a corporate office.

2.2 It covers all company-owned managed devices used for remote work.

2.3 Personal device access is governed by conditional access policy enforcement and is subject to the requirements in Section 7 (Bring-Your-Own Device). A formal BYOD policy will supplement this standard when approved.

2.4 This standard does not govern access controls for on-premises systems or in-office working, except where those controls intersect with remote access technology (e.g., VPN, enterprise identity provider).

---

## 3. Governance and accountability

| Role | Responsibility |
| --- | --- |
| Chief Information Security Officer (CISO) | Owns this standard. Approves exceptions to remote working security requirements, including high-risk data access from non-standard devices or networks. Reviews compliance reports quarterly. |
| IT Operations | Maintains and enforces conditional access policies, VPN and secure access tooling, and the endpoint management platform configuration. Monitors device compliance and reports deviations to the CISO. |
| Line Managers | Ensure that direct reports are aware of and comply with this standard prior to commencing remote work. Approve requests for exceptions in the first instance before escalation to the CISO. |
| All Employees and Contractors | Comply with all requirements in this standard. Report suspected incidents, device loss, or suspected compromise immediately to the IT service desk. |

---

## 4. Device requirements

### 4.1 Managed device requirement

4.1.1 Remote work must be conducted exclusively on a company-managed device enrolled in the endpoint management platform. The endpoint management platform enforces configuration baselines and conditional access policy enforcement prevents access from non-compliant or unmanaged devices.

4.1.2 Devices must maintain compliance with the endpoint configuration baseline at all times. The baseline requires, at minimum:

| Control | Requirement |
| --- | --- |
| Endpoint protection software | Enabled, current signature database, real-time scanning active |
| Full-disk encryption | Active and verified on all storage volumes |
| Operating system patching | Within the patch compliance window defined in the Endpoint Management and Device Compliance Procedure |
| Screen lock | Activates after no more than 5 minutes of inactivity; requires authentication to unlock |
| VPN client | Installed, current version, and functional |
| Certificate-based authentication | Device certificate provisioned and valid; used for network authentication and conditional access |

### 4.2 Device compliance grace period

4.2.1 Where a device falls out of compliance (e.g., due to a missed patch cycle or lapsed certificate), IT Operations will alert the device owner and the device will enter a compliance remediation period.

4.2.2 The compliance grace period is a maximum of 24 hours from the time non-compliance is detected. If the device is not remediated within 24 hours, conditional access policy enforcement will block access to organisational systems until compliance is restored.

4.2.3 During the grace period, access to Confidential and Restricted data is suspended regardless of the nature of the non-compliance.

### 4.3 Device maintenance

4.3.1 Remote workers must not disable, circumvent, or interfere with any security controls enforced by the endpoint management platform.

4.3.2 Software installation on managed devices must comply with the Acceptable Use Policy. Unapproved software that may conflict with endpoint protection software or the endpoint management platform agent must not be installed.

---

## 5. Network requirements

### 5.1 Public and untrusted networks

5.1.1 Organisational work must not be conducted on public or untrusted Wi-Fi networks (e.g., coffee shops, hotels, airports, conference venues) without first establishing a VPN or equivalent encrypted tunnel.

5.1.2 Where a VPN connection cannot be established, personnel must use a personal mobile hotspot (mobile data connection) as an alternative to an untrusted public network before conducting any organisational work.

5.1.3 The following network types require VPN regardless of the nature of work being conducted:

- Public Wi-Fi (any network not under the control of the organisation or the remote worker's household)
- Hotel or hospitality networks
- Client site networks unless a formal network access agreement is in place

### 5.2 Home networks

5.2.1 Home networks are the minimum acceptable connection for standard access to cloud productivity platform services protected by conditional access.

5.2.2 The following activities require an active VPN connection regardless of network type:

- Access to on-premises systems or internal network resources
- Access to sensitive databases
- Access to data classified as Confidential or Restricted
- Administrative or privileged access to any system

### 5.3 VPN split tunnelling

5.3.1 VPN split tunnelling, the configuration that routes only some traffic through the VPN while other traffic accesses the internet directly, must not be enabled by end users without explicit IT Operations approval.

5.3.2 Where split tunnelling is configured by IT Operations for performance reasons (e.g., to allow direct routing of cloud productivity platform traffic), the configuration must ensure that all access to on-premises resources and Confidential or Restricted data is routed through the VPN tunnel.

5.3.3 Any approved split tunnelling configuration must be documented, reviewed annually, and subject to the exception management process in Section 9.

### 5.4 Home router security

5.4.1 Home networks used for remote work must use WPA3 wireless encryption. Where untrusted IoT devices cannot support WPA3, place them on a separate SSID and VLAN, or on an isolated guest network, so they do not share the WPA3 network used for organisational work. Remote workers are also expected to apply the following baseline home network security practices:

- Change the router's default administrator credentials
- Keep router firmware current

5.4.2 Apart from the WPA3 requirement in 5.4.1, the organisation does not mandate home router configuration, but notes that a compromised home network increases the risk of credential interception. The VPN provides the primary compensating control for home network risks.

---

## 6. Workspace and physical security

6.1 Personnel working remotely must ensure that screens displaying organisational information are not visible to others in public locations or shared living spaces.

6.2 Devices must be locked immediately when stepping away, even briefly. Screen lock must not be disabled.

6.3 Devices must never be left unattended in public locations (e.g., coffee shops, libraries) or in vehicles.

6.4 Sensitive calls, video meetings, or conversations involving Confidential or Restricted information must not be conducted in public spaces where conversations may be overheard by third parties.

6.5 Clean desk principles apply when not actively working: documents must be put away, screens locked, and physical notes containing sensitive information must be stored securely.

6.6 Printed documents containing organisational information must be stored securely when not in use and disposed of via cross-cut shredding. Printing of Confidential or Restricted data at home or public locations requires prior written approval from the relevant line manager and the CISO.

---

## 7. Data handling and classification

### 7.1 Classification and storage

7.1.1 Remote workers must handle data in accordance with the Data Classification and Handling Standard at all times. The five classification levels and their remote working implications are summarized below:

| Classification | Remote Access Permitted | Storage Requirements | VPN Required |
| --- | --- | --- | --- |
| **Public** | Yes, on any compliant managed device | Company-managed storage | No |
| **Controlled** | Yes, on any compliant managed device | Company-managed storage | No |
| **Internal** | Yes, on any compliant managed device | Company-managed storage | No (cloud); Yes (on-premises) |
| **Confidential** | Yes, on compliant managed device; personal devices require CISO approval | Company-managed encrypted storage; personal cloud storage prohibited | Yes (on-premises access); Yes (all access from non-home networks) |
| **Restricted** | Managed device only; CISO approval required for remote access | Company-managed encrypted storage; no personal storage of any kind | Yes, always |

7.1.2 All data must remain in company-managed storage. Data must not be saved to personal cloud storage services, personal drives, or any storage medium not under the control of the organisation.

### 7.2 Collaboration and file sharing

7.2.1 Files must be shared using the organisation's approved collaboration and file storage platform. Email attachments containing Confidential or Restricted data must not be sent to personal email addresses.

7.2.2 Screen-sharing sessions via the collaboration platform must not expose Confidential or Restricted content to participants who do not have a legitimate business need.

---

## 8. Bring-your-own device (BYOD)

8.1 A formal BYOD policy is pending approval. In the interim, the following requirements apply to any use of personal devices to access organisational systems:

8.2 Personal devices must not be used to access data classified as Confidential or Restricted without explicit written approval from the CISO and a documented compensating control.

8.3 Where the CISO approves personal device access, the minimum compensating controls are:

- Enrolment in the endpoint management platform (where technically feasible) or equivalent mobile device management
- Conditional access policy enforcement applied to the personal device
- Prohibition on local data storage: access must be read-only or via browser-based thin client; any deviation requires CISO approval recorded as an exception in the risk register
- The CISO approval must be documented, time-limited (maximum 90 days per the exception process in Section 9), and reviewed on renewal

8.4 Personal devices may access Public and Internal data via cloud productivity platform browser interfaces subject to conditional access policy enforcement, without CISO approval, provided no data is downloaded to the personal device.

---

## 9. Incident reporting and response

### 9.1 Reporting obligation

9.1.1 Remote workers must report any of the following events to the IT service desk immediately and in no case later than 1 hour after discovery:

- Loss or theft of a managed device
- Suspected device compromise (malware, unauthorized access, unusual behaviour)
- Suspected interception of credentials or data
- Connection of a managed device to a potentially hostile network without VPN

9.1.2 Reports must be made by telephone to the IT service desk. Email alone is not acceptable for urgent device loss or compromise reports.

### 9.2 Response actions

9.2.1 Upon receipt of a device loss or theft report, IT Operations will initiate a remote wipe of the managed device via the endpoint management platform within 1 hour of notification.

9.2.2 Credential reset and session revocation via the enterprise identity provider will be initiated simultaneously with the remote wipe.

9.2.3 The incident will be logged and managed in accordance with the Incident Response Procedure.

### 9.3 Post-incident review

9.3.1 Following any device loss, theft, or compromise involving a remote working scenario, a post-incident review will be conducted within 5 business days.

9.3.2 The review will assess whether this standard's controls were followed, identify any gaps, and produce recommendations for any required standard updates.

---

## 10. Exceptions

10.1 Exceptions to any requirement in this standard must be approved in writing by the CISO before the exception is applied.

10.2 Exception requests must include:

- The specific requirement(s) for which an exception is sought
- The business justification
- A documented compensating control that mitigates the associated risk
- A proposed end date

10.3 Exceptions are granted for a maximum of 90 calendar days. Renewal requires a fresh application and re-approval.

10.4 All approved exceptions are recorded in the policy exception register maintained under the Exception and Risk Acceptance Management Policy.

10.5 The CISO may revoke an exception at any time if the risk profile changes or the compensating control is found to be ineffective.

---

## 11. Compliance and enforcement

11.1 Compliance with this standard is mandatory for all personnel within scope.

11.2 IT Operations will monitor device compliance posture via the endpoint management platform and report non-compliance to the CISO on a monthly basis, or immediately for critical non-compliance events.

11.3 Breaches of this standard will be handled in accordance with the organisation's disciplinary procedures. Repeated or wilful non-compliance may result in remote access privileges being suspended or terminated.

11.4 Contractors and third-party workers who breach this standard may have their access revoked immediately pending investigation.

---

## 12. Framework alignment

| Framework | Reference | Alignment |
| --- | --- | --- |
| ISO/IEC 27001:2022 | A.6.7 Remote working | Primary alignment: this standard operationalizes A.6.7 requirements |
| ISO/IEC 27001:2022 | A.8.1 User endpoint devices | Device security and compliance baseline requirements |
| ISO/IEC 27001:2022 | A.6.6 Confidentiality or non-disclosure agreements | Data handling obligations for remote workers |
| ISO/IEC 27002:2022 | §6.7 Remote working | Detailed implementation guidance for teleworking controls |
| NIST SP 800-46 Rev. 2 | §3 Security for Telework and Remote Access Solutions | Network, device, and data handling requirements |
| NIST SP 800-46 Rev. 2 | §4 Securing Telework Client Devices | Endpoint compliance baseline |
| NIST Cybersecurity Framework 2.0 | PR.AA (Identity Management, Authentication, and Access Control) | Conditional access and device compliance enforcement. Note: PR.AC was the CSF 1.1 subcategory; CSF 2.0 renamed it to PR.AA and added Authentication explicitly. |
| NIST Cybersecurity Framework 2.0 | PR.DS (Data Security) | Remote data handling and classification requirements |
| CSA CCM v4.1 | HRS-04 Remote and Home Working | Direct alignment: remote working security requirements |
| CSA CCM v4.1 | UEM-01 Endpoint Devices | Managed device and MDM requirements |
| CIS Controls v8 | Control 4 (Secure Configuration of Enterprise Assets) | Device baseline configuration requirements |
| CIS Controls v8 | Control 12 (Network Infrastructure Management) | VPN, split tunnelling, and network security guidance |

---

**End of Document**
