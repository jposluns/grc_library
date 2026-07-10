# Endpoint Management and Device Compliance Procedure

**Document Title:** Endpoint Management and Device Compliance Procedure\
**Document Type:** Procedure\
**Version:** 1.3.7\
**Date:** 2026-07-10\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](../security/policy-information-security.md), [`operations/standard-production-security-requirements.md`](standard-production-security-requirements.md), [`security/procedure-vulnerability-management.md`](../security/procedure-vulnerability-management.md), [`security/standard-authentication-and-password-management.md`](../security/standard-authentication-and-password-management.md)\
**Classification:** Public\
**Category:** Operations\
**Review Frequency:** Annual and upon material platform or regulatory change\
**Repository Path:** [`operations/procedure-endpoint-management-and-device-compliance.md`](procedure-endpoint-management-and-device-compliance.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

This procedure defines the end-to-end lifecycle for provisioning, hardening, monitoring, and decommissioning endpoints and servers to ensure that a consistent, auditable, and compliant device estate is maintained.

---

## 1. Purpose and scope

### 1.1 Purpose

To ensure that all organizational endpoints, including workstations, laptops, servers, and mobile devices, are enrolled, hardened, continuously monitored, and maintained in a compliant state throughout their operational lifetime, reducing the risk of compromise arising from misconfiguration, unpatched software, or unsanctioned devices accessing corporate resources.

### 1.2 Scope

1. Applies to all endpoints and servers owned or leased by the organization, including physical and virtual machines, on-premises and cloud-hosted servers, and organization-issued mobile devices.
2. Applies to personally-owned (BYOD) devices that access corporate systems, data, or networks.
3. Covers IT Operations, Security Operations, System Owners, and all employees or contractors using organization-managed or BYOD devices.
4. Includes cloud platform virtual machines and containerized workloads that carry an identifiable OS layer enrolled in endpoint management.

---

## 2. Governance

| Role | Responsibility |
| --- | --- |
| **CISO** | Owns this procedure; approves exceptions; receives monthly compliance metrics; approves EOL exceptions with CIO co-approval. |
| **IT Operations** | Manages the endpoint management platform; deploys and maintains endpoint protection and hardening baselines; maintains the asset register; executes decommissioning and disposal. |
| **Security Operations (SOC)** | Monitors endpoint protection alerts forwarded to the SIEM; triages endpoint-related security events; escalates confirmed incidents to the Incident Response Procedure. |
| **System Owners** | Accountable for the compliance status of servers and applications within their scope; coordinate patch and remediation activities within defined SLAs. |
| **All Employees and Contractors** | Responsible for adhering to device compliance requirements, reporting lost or stolen devices promptly, and completing mandatory security awareness training covering endpoint obligations. |
| **Internal Audit** | Reviews programme effectiveness, coverage metrics, and exception governance annually. |

---

## 3. Device inventory and asset management

### 3.1 Mandatory registration before use

No endpoint or server may connect to the corporate network or access corporate resources before it is registered in the asset register and enrolled in the endpoint management platform. This requirement applies to:

- New organization-issued workstations and laptops before first use.
- New or replacement servers before promotion to any environment.
- BYOD devices before accessing corporate systems (see §8).
- Temporary or loaner devices issued by IT Operations.

### 3.2 Asset register

IT Operations maintains a single authoritative asset register that includes, at minimum:

| Field | Requirement |
| --- | --- |
| Asset identifier | Unique tag or serial number |
| Asset type | Workstation / Laptop / Server / Mobile / Virtual |
| Assigned user or team | Named individual or functional team |
| OS version and patch level | Updated within 48 hours of change |
| Endpoint management platform enrolment status | Enrolled / Pending / Exempt |
| Endpoint protection status | Active / Alert / Offline |
| Compliance status | Compliant / Non-compliant / Exempt |
| Location | Physical site or cloud region |
| Acquisition and warranty dates | Including projected EOL date |

The asset register is reviewed quarterly to reconcile against the endpoint management platform inventory. Discrepancies are investigated and resolved within 5 business days. Unresolved discrepancies involving unknown active devices are treated as a P2 security incident.

### 3.3 Automated discovery

The endpoint management platform performs automated device discovery to identify endpoints active on the network that are not enrolled. Discovery findings are reviewed weekly by IT Operations. Any unregistered device discovered on the network is isolated pending investigation.

---

## 4. Endpoint protection deployment

### 4.1 Mandatory deployment

The enterprise endpoint detection and response (EDR) platform must be deployed on all managed devices, including:

- All organization-issued workstations and laptops.
- All on-premises and cloud platform servers (physical and virtual).
- All on-premises servers enrolled in cloud-based hybrid server management.

Endpoint protection deployment is validated as part of the pre-go-live security gate defined in the Production Security Requirements Standard §4.2 before any server is promoted to production.

### 4.2 Alert forwarding to SIEM

All endpoint protection alerts must be forwarded to the SIEM in near-real-time. Alert categories include but are not limited to: malware and ransomware detection, behavioural anomalies, credential theft attempts, lateral movement indicators, and tamper attempts against the endpoint protection agent itself. Alert forwarding is verified weekly; any gap in forwarding from a production endpoint is treated as a P2 incident.

### 4.3 Coverage targets

| Asset Type | Endpoint Protection Coverage Target |
| --- | --- |
| Organization-issued workstations and laptops | 100% |
| On-premises servers | 100% |
| Cloud platform virtual machines | 100% |
| Organization-issued mobile devices | 100% |

Coverage below 98% on any asset class triggers an immediate remediation plan and CISO notification. Any single unprotected Tier 0 or Tier 1 server is treated as a P2 incident.

### 4.4 Agent health monitoring

The endpoint management platform health dashboard is reviewed daily by IT Operations. Agents in an inactive, error, or tampered state are remediated within 4 hours for servers and 24 hours for workstations.

---

## 5. Configuration compliance

### 5.1 Hardening baselines

Approved hardening baselines are deployed to all managed device classes via the endpoint management platform. Baselines are aligned with CIS Benchmark recommendations at Level 1 (workstations) and Level 2 (servers). The following device classes have defined baselines:

| Device Class | Baseline Reference |
| --- | --- |
| Windows workstations and laptops | CIS Microsoft Windows Benchmark, Level 1 |
| Windows servers | CIS Microsoft Windows Server Benchmark, Level 2 |
| Linux servers | CIS Linux Benchmark, Level 2 |
| Mobile devices (corporate-issued) | CIS Mobile Benchmark, Level 1 |

Baselines are reviewed annually and updated within 30 days of a new CIS Benchmark release affecting an in-scope device class.

### 5.2 Configuration drift detection

The endpoint management platform performs continuous compliance assessment against deployed baselines. Configuration drift is reported in real time. Drift from the approved baseline is classified as non-compliant. High-risk drift, such as disabling screen lock, disabling endpoint protection, or removing required security policies, triggers an automated alert to Security Operations within 15 minutes.

### 5.3 Workstation screen lock

All workstations and laptops must lock automatically after a maximum of 15 minutes of inactivity. This control is enforced via endpoint management platform policy and verified as part of the compliance assessment cycle. Manual bypass or policy exception requires CISO written approval.

### 5.4 Compliance remediation

Non-compliant devices detected by the endpoint management platform are subject to the following response:

| Non-compliance Type | Response |
| --- | --- |
| Missing baseline configuration item | Automatic re-application of policy via endpoint management platform; IT Operations notified. |
| Endpoint protection offline or tampered | IT Operations notified immediately; device flagged for investigation; policy-based access controls block access pending resolution. |
| EOL OS detected | Escalated to System Owner and CISO; EOL handling per §5.5. |
| Unauthorized software installed | Alert raised; software quarantined if possible; IT Operations investigates. |

### 5.5 EOL operating system prohibition

No end-of-life operating system version is permitted in production. OS versions approaching EOL are tracked using the classification defined in the Vulnerability Management Procedure §5:

- At 180 days before EOL: upgrade plan initiated; owner and budget assigned.
- At 90 days before EOL: upgrade in active execution.
- At 30 days before EOL: emergency remediation; monthly status reported to the CIO.
- At EOL without remediation: immediate escalation; CISO and CIO-approved exception with documented compensating controls is mandatory before the system may continue operating.

---

## 6. Conditional access enforcement

### 6.1 Compliance as an access condition

Device compliance status is evaluated by the enterprise identity provider at every authentication event for corporate resources. Devices that are not enrolled in the endpoint management platform or that are marked as non-compliant are blocked from accessing:

- Corporate email and collaboration platforms.
- Internal applications and portals.
- VPN and remote access infrastructure.
- Cloud platform resources.

The enterprise identity provider is the authoritative enforcement point for policy-based access controls. Application and infrastructure teams must not implement workarounds or exceptions to policy-based access controls without written CISO approval.

### 6.2 Conditional access policy governance

policy-based access controls are defined and owned by the CISO. All policy changes require a High-risk change request per the Change Management and Configuration Control Procedure. Changes to policy-based access controls are logged, reviewed at CAB, and subject to post-implementation review within 48 hours.

### 6.3 Grace period for newly enrolled devices

Newly enrolled devices are granted a grace period of up to 8 business hours from enrolment to achieve full compliance status before policy-based access controls restrictions are applied. Grace period extensions require IT Operations Manager approval.

---

## 7. Patch and vulnerability management for endpoints

### 7.1 Patch deployment

Endpoint and server patching follows the remediation SLAs defined in the Vulnerability Management Procedure and the Production Security Requirements Standard. Patches are deployed via the endpoint management platform using the following approach:

| Patch Category | Deployment Method |
| --- | --- |
| OS security updates | Automatic deployment via endpoint management platform policy within the applicable SLA |
| Application patches (managed software) | Deployed via endpoint management platform within the applicable SLA |
| Firmware and BIOS updates | Managed deployment via IT Operations with Change Management approval |
| Third-party application patches | Deployed via approved software catalogue or direct push within the applicable SLA |

### 7.2 Patch compliance reporting

The endpoint management platform generates a weekly patch compliance report. IT Operations reviews the report within 48 hours. Devices that have not received a critical or high patch within the applicable SLA are flagged as non-compliant and subject to policy-based access controls restriction until patched.

### 7.3 Patch testing

Critical OS patches that affect server workloads are tested in a non-production environment before production deployment where technically feasible. The testing window must not exceed 48 hours for critical patches. Emergency patches may proceed directly to production with an approved Emergency Change; the Change Manager and CISO are notified immediately.

---

## 8. Mobile and BYOD devices

### 8.1 Corporate-issued mobile devices

Organization-issued mobile devices are enrolled in the endpoint management platform and subject to all controls in this procedure, including:

- Remote wipe capability enabled.
- Encryption enabled (hardware-backed where supported).
- Screen lock enforced with a maximum 5-minute inactivity timeout.
- Access to corporate resources governed by policy-based access controls.

### 8.2 BYOD device requirements

Personally-owned devices that access corporate systems must meet minimum security requirements before access is permitted. The enterprise identity provider evaluates device compliance at authentication via the endpoint management platform. Minimum BYOD requirements are:

| Requirement | Minimum Standard |
| --- | --- |
| OS version | Supported, non-EOL version |
| Screen lock | Enabled, maximum 5-minute timeout |
| Device encryption | Enabled (full-device or work profile) |
| Endpoint protection | Organization-approved app or OS-native security |
| OS patches | Current within 30 days |

Access to Restricted or Confidential data from a BYOD device is prohibited unless the device is enrolled in a managed work profile within the endpoint management platform. BYOD devices are not permitted to access the management VLAN, PAM infrastructure, or server administration interfaces under any circumstances.

### 8.3 Personal device separation

Where a managed work profile is deployed to a BYOD device, corporate data is containerized and isolated from personal data. IT Operations may remotely wipe the managed work profile without affecting personal data. Remote wipe of the full device is not performed on BYOD devices without the device owner's written consent, except where required by law.

---

## 9. Decommissioning and disposal

### 9.1 Decommissioning process

When an endpoint or server is retired, the following steps must be completed before the device leaves IT custody:

1. Confirm active data backup or migration of any data required for retention under the Records Retention and Destruction Standard.
2. Revoke the device from the endpoint management platform and enterprise identity provider.
3. Remove the device from any active policy-based access controls or policy assignments.
4. Perform media sanitization per §9.2.
5. Update the asset register to reflect decommissioned status with the date and method of disposal.
6. Obtain a Certificate of Destruction where required by §9.3.

### 9.2 Media sanitization

All storage media must be sanitized before a device leaves IT custody, consistent with the Media Handling and Transport Procedure and NIST SP 800-88 guidelines:

| Media Type | Required Method |
| --- | --- |
| Solid-state drives (SSD) | Cryptographic erasure (ATA Secure Erase or equivalent) |
| Hard disk drives (HDD) | Overwrite (IEEE 2883 Clear) or degaussing followed by verification |
| Non-erasable or damaged media | Physical destruction |
| Mobile device storage | Factory reset with cryptographic erasure where supported by OS |

Sanitization must be verified and documented before the asset register is updated to "disposed."

### 9.3 Certificate of destruction

A Certificate of Destruction is required for:

- All devices that held Confidential or Restricted data.
- All servers and managed workstations.
- Any mobile device enrolled in the endpoint management platform.

Certificates of Destruction are retained for a minimum of 7 years per the Records Retention and Destruction Standard.

### 9.4 Secure disposal vendor

Where physical destruction is performed by a third-party vendor, the vendor must hold documented accreditation (e.g., R2, e-Stewards, or equivalent) and provide Certificates of Destruction for each disposal event. Vendor selection and contract terms are reviewed annually by the CISO.

---

## 10. Metrics

The following metrics are reported to the CISO monthly and reviewed at the quarterly security review:

| Metric | Target |
| --- | --- |
| Endpoint protection coverage (all asset classes) | 100% |
| Configuration compliance rate (compliant / total enrolled) | ≥ 98% |
| Patch SLA adherence: Critical | ≥ 95% |
| Patch SLA adherence: High | ≥ 90% |
| Asset register reconciliation pass rate | 100% quarterly |
| Non-compliant devices blocked by policy-based access controls (count) | Reviewed; zero tolerance for unresolved > 24 hours |
| Devices with EOL OS in production (count) | Zero; any exception reported to CISO immediately |
| Disposal events with Certificate of Destruction | 100% of qualifying disposals |

---

## 11. Framework alignment

| Control Area | ISO/IEC 27001:2022 | NIST SP 800-124 | CSA CCM v4.1 | COBIT 2019 |
| --- | --- | --- | --- | --- |
| Asset inventory and lifecycle | A.8.1 to A.8.3 | §4.1 Device Inventory | UEM-04 | DSS05.01 |
| Endpoint protection deployment | A.8.7 | §4.2 Configuration Mgmt | UEM-09 | DSS05.03 |
| Configuration compliance and hardening | A.8.9 | §4.3 Security Baseline | UEM-05 | DSS05.04 |
| Policy-based access-control enforcement | A.5.15, A.8.2 | §4.4 Access Control | UEM-05 | DSS05.05 |
| Patch and vulnerability management | A.8.8 | §4.5 Patch Management | UEM-07, TVM-06 | DSS05.07 |
| Mobile and BYOD | A.8.1, A.6.7 | §4.6 Mobile Devices | UEM-01 | DSS05.03 |
| Decommissioning and media sanitization | A.8.10 | §4.7 Disposal | DSP-02 | DSS05.06 |

---

*This document is released under CC BY-SA 4.0. No rights reserved.*



**End of Document**
