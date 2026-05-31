# Endpoint Hardening Standard

**Document Title:** Endpoint Hardening Standard\
**Document Type:** Standard\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/policy-byod.md`](policy-byod.md), [`security/standard-authentication-and-password-management.md`](standard-authentication-and-password-management.md), [`security/standard-data-loss-prevention.md`](standard-data-loss-prevention.md), [`security/standard-data-classification-and-handling.md`](standard-data-classification-and-handling.md), [`security/standard-remote-working-security.md`](standard-remote-working-security.md), [`security/procedure-vulnerability-management.md`](procedure-vulnerability-management.md), [`security/framework-zero-trust-architecture.md`](framework-zero-trust-architecture.md), [`operations/procedure-endpoint-management-and-device-compliance.md`](../operations/procedure-endpoint-management-and-device-compliance.md), [`operations/procedure-patch-management.md`](../operations/procedure-patch-management.md), [`operations/procedure-media-handling-and-transport.md`](../operations/procedure-media-handling-and-transport.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material change to OS platforms, threat-actor tradecraft, or hardware capabilities\
**Repository Path:** [`security/standard-endpoint-hardening.md`](standard-endpoint-hardening.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This standard defines the hardening baseline for endpoints used in the organisation's environment. It covers managed workstations and laptops on all major operating systems, mobile devices, and the BYOD posture for unmanaged personal devices that access organisational resources. The standard is the technical companion to the endpoint management procedure (which governs operations) and the BYOD policy (which governs scope).

---

## Scope

This standard applies to:

1. **Managed corporate workstations and laptops** running supported operating systems (Windows, macOS, major Linux distributions used at scale).
2. **Mobile devices** (iOS and Android) issued by the organisation or enrolled under BYOD policy.
3. **Privileged access workstations** used for administering production environments.
4. **Developer workstations** with additional considerations for build chains and AI coding assistants.
5. **Kiosks, shared devices, and unattended terminals** in operational settings.

It does not cover servers, network appliances, IoT or OT devices, or container hosts; those follow the production security and cloud baseline standards.

---

## Section 1: identity and authentication

| Control area | Requirement |
| --- | --- |
| Local accounts | Local administrator accounts disabled or randomised per device; recovery handled via the endpoint management platform |
| Sign-in | Federated sign-in against the enterprise identity provider; standalone local sign-in to organisational data prohibited |
| Authentication strength | Phishing-resistant authentication on all managed devices where the OS and hardware support it; passcode minimum complexity per the authentication standard |
| Biometrics | Platform biometric authentication permitted; secure-enclave-backed |
| Privileged-action elevation | UAC, sudo, or equivalent enabled; standing local administrative rights prohibited; just-in-time elevation per the privileged access standard |
| Screen lock | Auto-lock after 5 minutes of inactivity or sooner; unlock requires authentication |
| Session lock on idle | Per the data classification of the device's expected content |

---

## Section 2: device integrity

| Control area | Requirement |
| --- | --- |
| Secure boot | Enabled and enforced on every managed device |
| Firmware integrity | Firmware updates managed centrally; firmware-level passwords set where the platform supports it |
| Trusted Platform Module or Secure Enclave | Enabled and used for credential storage, disk encryption, and platform attestation |
| Disk encryption | Full-disk encryption enabled; key escrow integrated with the endpoint management platform |
| Endpoint attestation | Device posture attested at sign-in; non-compliant attestation blocks access per the zero trust framework |
| Hypervisor-based protections | Enabled where the OS supports memory-integrity and credential-isolation protections (e.g. virtualisation-based security) |
| Recovery key handling | Recovery keys stored centrally; access logged and audited |

---

## Section 3: software and configuration

| Control area | Requirement |
| --- | --- |
| OS version | Within the current vendor-supported version; EOL versions prohibited in production use |
| Patch compliance | Per the patch management procedure |
| Approved software | Software installed from an approved catalogue or vendor; non-approved installation restricted |
| Application allow-list | Where the role and platform support it, application allow-list enforced; otherwise application reputation enforced |
| Browser hardening | Approved browsers configured to enforce phishing protection, secure-DNS, certificate pinning where supported, extension governance |
| Macro and active content | Office macros disabled by default; PDF active content restricted |
| Unused services | Disabled (e.g. unused network sharing, legacy protocols) |
| Removable media | Per the media handling standard; controlled per data classification |
| Network adapters | Wired-and-wireless simultaneity disabled where it creates path crossings into restricted networks |
| Bluetooth and short-range wireless | Configured per role; unused protocols disabled |

---

## Section 4: endpoint detection and response

| Control area | Requirement |
| --- | --- |
| EDR agent | Installed and healthy on every managed endpoint; tamper protection enabled |
| EDR telemetry | Forwarded to the SIEM per the logging standard |
| Behavioural detection | Enabled with vendor-recommended detection content plus organisation-specific custom content |
| Response capability | Containment actions (isolate, quarantine file, kill process) available to the SOC per the SOC standard |
| Coverage validation | Quarterly verification that every managed endpoint has a healthy EDR agent |
| Tamper response | EDR agent tampering or stop attempts route as a high-severity alert |

---

## Section 5: data protection

| Control area | Requirement |
| --- | --- |
| Data loss prevention | Per the DLP standard; agent enabled on managed endpoints |
| Removable storage | Encrypted-by-default for organisation data; unencrypted use prohibited |
| Print and copy controls | Per the data classification of the role; sensitive content requires labelled or controlled print |
| Cloud sync clients | Approved sync clients only; personal cloud sync restricted per the acceptable use policy |
| Local data residency | Sensitive data discouraged from local storage; user content directed to managed cloud platforms |
| Backup | Per the resilience programme; user data backed up where the role and data warrant it |

---

## Section 6: network and connectivity

| Control area | Requirement |
| --- | --- |
| Local firewall | Enabled and policy-managed |
| VPN client | Installed per the network communications policy; split tunnelling per the remote working standard |
| Wi-Fi profiles | Auto-connect to unknown open networks disabled; corporate Wi-Fi authenticated |
| DNS | Secure DNS enabled where supported; resolution routes through the organisation's DNS security service |
| Proxy and inspection | Where in use, configured at the platform level; bypass restricted |
| IPv6 | Enabled or disabled per the network design; not left at default-on if the network is not IPv6-ready |

---

## Section 7: privileged access workstations (PAW)

Devices used to administer production environments meet a stricter baseline.

| Control area | Requirement |
| --- | --- |
| Hardware dedication | The PAW is used only for administrative tasks; no email, browsing, productivity, or personal use |
| Network segregation | The PAW reaches only administrative networks; access to general internet restricted to an approved subset for vendor portals |
| Hardware token | Hardware-backed phishing-resistant authentication for the administrative identity |
| Application restriction | Minimal application set; administrative tooling only |
| Per-session credentials | Credentials retrieved from the PAM vault per session; no standing credentials |
| Session recording | Administrative sessions recorded where the action class warrants it |
| Rotation | Hardware refreshed on the standard PAW lifecycle; the prior device wiped and recycled per the disposal standard |

---

## Section 8: developer workstations

| Control area | Requirement |
| --- | --- |
| Local administrator scope | Developer admin rights scoped to the local machine; not to network shares or central systems |
| Container and virtualisation | Permitted; configured per the platform's secure defaults |
| AI coding assistant | Per the AI coding assistant security guideline; rules and allow-lists applied |
| Code repository access | Federated identity; SSH keys hardware-backed where the platform supports it |
| Local secrets | Prohibited; secrets accessed from the secrets management service |
| Source-of-truth IDE configuration | Provided where it materially improves baseline posture; bring-your-own IDE permitted within the secure-development standard |
| Telemetry | Developer-tool telemetry routed per the privacy notice |

---

## Section 9: BYOD and unmanaged devices

| Control area | Requirement |
| --- | --- |
| Posture floor | Per the BYOD policy; conditional access enforces minimum posture before access |
| Application containerisation | Where supported, organisation data accessed within a managed app or browser profile that the organisation can selectively wipe |
| No persistent local data | Organisation data does not persist on the unmanaged device; cache cleared on session end |
| Personal-account separation | Personal and organisational accounts on the same device do not share data |
| Compromise indicators | Where the unmanaged device shows indicators (jailbreak, root, untrusted certificate), access is blocked |
| Privacy | The organisation does not monitor the personal partition of the device; the privacy notice describes the scope |

---

## Section 10: mobile devices

| Control area | Requirement |
| --- | --- |
| Enrolment | Enrolled in the endpoint management platform before accessing organisation data |
| OS version | Within the vendor-supported and patched version |
| Passcode | Per the authentication standard |
| Biometrics | Platform biometric permitted; secure-enclave-backed |
| Wipe capability | Remote-wipe (full device or work profile) available; tested |
| Containerisation | Work profile or work container used where the platform supports it |
| Camera and microphone | Controlled per role and per facility policy |
| Public-Wi-Fi posture | Per the remote working standard; VPN engaged on untrusted networks |
| Sideload | Sideloading of unsigned applications prohibited |

---

## Section 11: kiosks and shared devices

| Control area | Requirement |
| --- | --- |
| Account model | Single-purpose account; no general internet or productivity use |
| Auto-reset | Session cleared after each user or on idle |
| Restricted shell | Locked-down launcher; user cannot escape to the underlying OS |
| Physical security | Tamper-evident enclosure where the device is in a public area |
| Inventory | Per the asset inventory; physical location recorded |

---

## Section 12: lifecycle and disposal

| Stage | Required action |
| --- | --- |
| Procurement | Per the supplier programme; hardware certified to meet the standard's hardware-feature expectations |
| Provisioning | Image or zero-touch provisioning enrols the device with the baseline applied |
| In service | Posture monitored continuously; non-compliance triggers conditional access enforcement |
| Refresh | Within the documented lifecycle; refresh not exceeding the OS-supported window |
| Reassignment | Wiped and re-enrolled before reassignment |
| Disposal | Per the media handling standard with verified data sanitisation |
| Loss or theft | Immediate report; remote wipe attempted; access revocation |

---

## Operating expectations

1. The endpoint baseline is documented per OS platform and per role tier (general, developer, PAW, mobile, shared).
2. Posture is verified continuously through the endpoint management platform; deviations trigger conditional access enforcement.
3. Hardening configuration is reviewed annually against current vendor baselines (CIS Benchmarks, vendor-published security guidance).
4. Material configuration changes follow the change management procedure.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| CIS Benchmarks | Per OS platform | Authoritative configuration baselines |
| NIST SP 800-46 Rev 2 | Guide to Enterprise Telework, Remote Access, and Bring Your Own Device | Remote and BYOD context |
| NIST SP 800-124 Rev 2 | Guidelines for Managing the Security of Mobile Devices | Mobile baseline |
| ISO/IEC 27001:2022 | A.8.1 (user endpoints), A.8.3, A.8.7 | Endpoint controls |
| CSA Cloud Controls Matrix | UEM domain | Cross-walk |
| Microsoft Security Compliance Toolkit | Vendor baseline | Where applicable |
| macOS Security Compliance Project | Open standard | Where applicable |
| Apple Platform Security and Android Enterprise security models | Vendor documentation | Mobile baselines |

---

## Limitations

This standard is a CC BY-SA 4.0 baseline. Specific OS, hardware, and management-platform configurations vary; the standard expresses the control requirements rather than vendor-specific settings. Adopting organisations select the appropriate CIS Benchmark level (Level 1 for typical use; Level 2 for high-sensitivity environments) and document any deviations as exceptions.

---

**End of Document**
