# Cloud Security Configuration Baseline

**Document Title:** Cloud Security Configuration Baseline\
**Document Type:** Standard\
**Version:** 1.4.23\
**Date:** 2026-10-27\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](../security/policy-information-security.md), [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md), [`security/standard-authentication-and-password-management.md`](../security/standard-authentication-and-password-management.md), [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md), [`operations/standard-production-security-requirements.md`](standard-production-security-requirements.md), [`operations/standard-network-security-and-segmentation.md`](standard-network-security-and-segmentation.md), [`compliance/public-sector/annex-canada-public-sector-requirements.md`](../compliance/public-sector/annex-canada-public-sector-requirements.md)\
**Classification:** Public\
**Category:** Operations\
**Review Frequency:** Annual and upon material platform or regulatory change\
**Repository Path:** [`operations/standard-cloud-security-configuration-baseline.md`](standard-cloud-security-configuration-baseline.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines the secure configuration baseline for cloud and cloud productivity environments. It establishes minimum security configuration requirements for the cloud platform, enterprise identity provider, cloud productivity platform, and associated services to reduce attack surface and ensure that a consistent security posture is maintained across all tenants and subscriptions.

---

## 2. Scope

1. Applies to all cloud tenants and subscriptions including cloud platform, enterprise identity provider, cloud productivity platform, and endpoint and email protection platform services.
2. Covers configuration of identity, network, compute, storage, monitoring, and collaboration services.
3. Applies to all environments: DEV, TEST, and PROD. Security classification applies consistently; TEST environments are not exempt from baseline security controls.
4. Applies to IT Operations, the infrastructure programme team, and any third party managing cloud resources on behalf of the organization.

### 2.1 Scope boundary with dev-security cloud hardening baselines

This standard and the per-provider cloud hardening baselines in `dev-security/` together cover the organization's cloud security posture. The boundary is as follows:

| Subject | Authoritative standard |
| --- | --- |
| Enterprise-tenant administration (identity provider tenant, organization/management-group hierarchy, tenant-wide policies, cross-account trust, productivity SaaS, email and collaboration platforms) | This standard |
| Workload accounts/subscriptions/projects and the IaC that provisions them | [`dev-security/standard-cloud-hardening-baseline-aws.md`](../dev-security/standard-cloud-hardening-baseline-aws.md), [`standard-cloud-hardening-baseline-azure.md`](../dev-security/standard-cloud-hardening-baseline-azure.md), [`standard-cloud-hardening-baseline-gcp.md`](../dev-security/standard-cloud-hardening-baseline-gcp.md) |
| Identity federation between the enterprise IdP and workload accounts | Both: federation is configured per this standard; consumption inside the workload is per the dev-security baseline |
| Centralized audit log destination | This standard defines the destination; the dev-security baselines define what each workload emits |
| Workload network segmentation, encryption, secrets handling, and infrastructure-as-code | The dev-security baselines |
| Provider quotas, billing controls, and cross-tenant administration | This standard |

A workload built on a cloud provider must conform to both: the enterprise-tenant rules here, and the workload-level rules in the matching dev-security baseline. Where a conflict appears, escalate to the architecture review forum.

---

## 3. Governance

| Role | Responsibility |
|---|---|
| Chief Information Security Officer (CISO) | Owns this standard; defines baseline requirements; co-approves security-related exceptions per the §4.2.2 risk-tier pathway of the [Exception and Risk Acceptance Management Policy](../governance/policy-exception-and-risk-acceptance-management.md) |
| IT Operations / Cloud Team | Implements and maintains baseline configurations; remediates configuration drift |
| Infrastructure Programme Team | Ensures that all new infrastructure deployments conform to this standard from initial build |
| Internal Audit | Reviews compliance against baseline using the cloud security posture score and cloud security posture management (CSPM) tooling |

---

## 4. Enterprise identity provider baseline

### 4.1 Multi-factor authentication (MFA)

- MFA is required for all users.
- Policy-based access controls enforce MFA for all cloud resource access.
- Legacy authentication protocols (basic auth, SMTP auth, IMAP) are blocked at the identity provider level.

### 4.2 Policy-based access controls

- Policy-based access controls are the primary enforcement layer for access policies.
- Risk-based conditions (sign-in risk and user risk) are evaluated and enforced.
- Compliant-device requirement is enforced for access to corporate data.

### 4.3 Just-in-time privileged role activation

- Just-in-time activation is enabled for all tenant administrator, privileged role administrator, and cloud resource Owner roles.
- Standing (permanent) assignment to these roles is prohibited; time-bound activation is required.
- See the Privileged Access Management Standard for full requirements.

### 4.4 Enterprise password protection service

- The enterprise password protection service is deployed to the on-premises directory to enforce banned-password lists.
- Password spray protection is enabled.

### 4.5 Default baseline policies

- Default baseline policies are superseded by the granular policy-based access controls.
- Where granular access policies do not cover a scenario, the default baseline policies provide fallback protection.

### 4.6 Guest access

- External guest access is restricted to approved partner domains.
- Guest users cannot enumerate the directory or invite additional guests.
- Guest account lifecycle reviews occur quarterly.

---

## 5. Cloud productivity platform baseline

### 5.1 Email platform

| Control | Requirement |
|---|---|
| Anti-spoofing | DMARC, DKIM, and SPF configured and enforced |
| Safe Links | Enabled for all users |
| Safe Attachments | Enabled for all users |
| External email warning | Warning banners enabled on all inbound external email |
| Audit logging | Enabled for all mailboxes |

### 5.2 Collaboration platform

- External communication restricted to approved domains.
- Anonymous access to meetings is disabled.
- Recording retention policies are configured per the data retention schedule.

### 5.3 Collaboration and file storage platform

- External sharing scoped to approved domains only.
- Unmanaged device access restricted to view-only.
- Sensitivity labels applied to classify and protect data per the Data Classification Standard.

### 5.4 Endpoint and email protection platform

- Enabled at the equivalent of Plan 2 feature tier.
- Attack simulation training enabled.
- Preset security policies applied as baseline; custom tuning performed where needed.

---

## 6. Cloud platform baseline

### 6.1 Subscription and resource access

| Control | Requirement |
|---|---|
| Identity and access management | Governed by enterprise identity provider RBAC |
| Privileged roles | Owner and Contributor roles at subscription scope require PIM activation |
| Resource locks | Applied to all production resource groups to prevent accidental deletion or modification |

### 6.2 Network security

- Network security groups (NSGs) applied to all subnets.
- No resources are directly exposed to the internet without a cloud firewall or web application firewall (WAF).
- RDP and SSH inbound access from the internet is blocked at the NSG level.

### 6.3 Monitoring and logging

- The cloud monitoring service and SIEM are the primary platforms for monitoring and log aggregation.
- Diagnostic settings enabled for all resource types; log data forwarded to the SIEM workspace.
- Cloud platform activity log retention minimum: 90 days. This is the platform-side forwarding floor that ensures that the SIEM has a window in which to ingest activity events; it is not the authoritative retention for the events themselves. Once forwarded, events are retained per the [SIEM event logs row of the data retention schedule](../governance/register-data-retention-schedule.md) (1 year hot plus 2 years cold). The SIEM is the authoritative retention authority for the long-tail; the cloud platform is the source-of-truth for the most recent 90 days.

### 6.4 Cloud security posture management (CSPM)

- CSPM enabled across all subscriptions.
- Cloud security posture score reviewed monthly.
- High and Critical recommendations remediated within the timeframes defined in the Vulnerability Management Procedure.

### 6.5 Storage accounts

| Control | Requirement |
|---|---|
| Public blob access | Disabled by default |
| Secure transfer | HTTPS only required |
| Shared Access Signatures (SAS) | Must be time-limited; unlimited-duration SAS tokens are prohibited. This prohibition is absolute and is not subject to the exception pathway described in Section 3. |
| Storage protection | Cloud storage threat protection enabled |

### 6.6 Secrets management service

- All secrets, keys, and certificates must be stored in the secrets management service.
- Soft-delete and purge protection enabled.
- Access governed by enterprise identity provider RBAC; PIM activation required for high-privilege operations.

---

## 7. Configuration drift

| Condition | Response |
|---|---|
| Drift detected | CSPM policy compliance and cloud security posture score monitoring trigger alert |
| Review cadence | Drift reviewed weekly |
| High-risk drift (score reduction > 5%, or critical security control disabled) | Treated as P2 incident; remediated within 48 hours |
| All configuration changes | Must follow the Change Management Procedure |

---

## 8. Framework alignment

| Framework | Reference | Topic |
|---|---|---|
| ISO/IEC 27001:2022 | A.8.9, A.8.23, A.8.24 | Configuration management (A.8.9), web filtering (A.8.23), use of cryptography (A.8.24) |
| ISO/IEC 27017:2026 | Information security controls based on ISO/IEC 27002 for cloud services | Cloud-service-specific control baseline |
| CIS Cloud Foundations Benchmark | v2.0 | Secure cloud platform configuration |
| CIS Cloud Productivity Foundations Benchmark | v3.0 | Secure cloud productivity configuration |
| NIST SP 800-53 Rev. 5 | CM-2, CM-6 | Configuration Baseline and Settings |
| NIST SP 800-210 | General Access Control Guidance for Cloud Systems | Cloud access-control model for the identity-provider baseline |
| COBIT 2019 | DSS05 | Managed Security Services |
| CSA CCM v4.1 | I&S-01, I&S-04 | Infrastructure Security |
| TBS Direction on the Secure Use of Commercial Cloud Services, SPIN 2017-01 | 6.1.1, 6.1.2, 6.1.3, 6.2.4, 6.3.2 | Categorization, graduated safeguards, third-party assurance, network security, and incident management for cloud services |
| CCCS ITSP.50.103, Guidance on the Security Categorization of Cloud-Based Services | §7, §7.4, §7.5, §8 | Control profile selection, tailoring, control allocation, and deployment and service models |
| CCCS Medium Cloud Control Profile (ITSP.50.103 Annex B) | SC-7, SC-7(3), SC-7(5) | Boundary protection |
| CCCS Baseline Cyber Security Controls for Small and Medium Organizations V1.2 | BC.10.1 to BC.10.5 | Secure cloud and outsourced IT services |

**Canadian cloud sources.** The four Canadian rows above are paraphrased from the held texts, with pinpoints. Each row cites the held edition; its currency is to be confirmed upstream before an adopter relies on it. The public-sector applicability model is in the [Canada Public Sector GRC Requirements Annex](../compliance/public-sector/annex-canada-public-sector-requirements.md), and network zoning is mapped in section 11 of the [Network Security and Segmentation Standard](standard-network-security-and-segmentation.md). A mapping row here does not establish implementation or compliance.

- **SPIN 2017-01 (dated 1 November 2017 and modified 23 June 2022, per the held text's header; the held text's page footer shows a later web-page date, "Date modified: 2025-10-22").** The SPIN applies to departments within the meaning of Schedules I, I.1, II, IV, and V of the Financial Administration Act, unless excluded (SPIN section 4), and to information categorized Protected B, medium integrity, and medium availability; its requirements "should also be applied" to Protected A information where a risk assessment justifies it (section 2).
  - Before using cloud services, departments "must identify and categorize" information by the injury expected from a compromise of its confidentiality, integrity, and availability (6.1.1). The categorization method is in the ITSP.50.103 paragraph of the [Data Classification and Handling Standard](../security/standard-data-classification-and-handling.md).
  - Departments "must apply graduated safeguards" commensurate with the risk, and control profiles can support this (6.1.2). The held SPIN still names the earlier GC Security Control Profile for Cloud-Based GC IT Services as a starting point. The held text of that profile says its Appendix A control list has been replaced by the CCCS Medium Cloud Control Profile in ITSP.50.103 Annex B (its Note to Readers), so this baseline treats the earlier profile as historical and maps to Annex B.
  - Where physical inspection and audit are not feasible, departments "can leverage" independent reporting, such as ISO/IEC 27001, 27017, and 27018, FedRAMP, PCI DSS, CSA STAR, and AICPA SOC audit reports or certifications, to establish third-party assurance (6.1.3).
  - Data in transit "must be adequately protected" by encryption and network safeguards; all external interfaces of a cloud service "must be identified" and protected, and management interfaces "may require" increased protection (6.2.4). This supports section 6.2. Section 6.2.4 points to CSE cryptographic guidance ITSP.40.111 (written in the held SPIN as TSP.40.111) and ITSP.40.062, and to ITSG-38 for placing services within zones; those three publications are not held in the reference base, so no requirement from them is stated here. <!-- ref-absence: ITSP.40.111 | ITSP.40.062 | ITSG-38 -->
  - The GC "must continue to have" the ability to respond to cyber security events consistently, in alignment with the GC Cyber Security Event Management Plan and in coordination with the Canadian Centre for Cyber Security; departments provisioning cloud services are responsible for response mechanisms and for exchanging incident information with lead departments (6.3.2).
- **ITSP.50.103 (takes effect on 20 May 2020, per the held text).** An organization "should select" one of the Cyber Centre's cloud control profiles in Annexes A and B, after validating the business, technical, and threat contexts and tailoring the controls in its scope (§7). Tailoring rationale and decisions "should" be documented (§7.4). Control allocations show whether the provider or the consumer is responsible for each control; for IaaS and PaaS, the consumer is responsible for the systems it configures and manages in the cloud (§7.5). The deployment and service model depends on the services needed, the control the organization wants to keep, and its operating maturity (§8). The section 2.1 scope boundary with the dev-security cloud hardening baselines follows the same consumer-side split.
- **Medium Cloud Control Profile (ITSP.50.103 Annex B; held spreadsheet titled CCCS Cloud Security Control Recommendations, 31 May 2019).** SC-7 calls for monitoring and controlling communications at external and key internal boundaries, separate sub-networks for publicly accessible components, and external connections only through managed interfaces; SC-7(3) limits the number of external network connections; SC-7(5) denies traffic by default at managed interfaces and allows it by exception. The control statements are written in the present tense without a modal verb. The spreadsheet allocates SC-7 and SC-7(5) to the consumer for IaaS and PaaS but not for SaaS, and SC-7(3) to the consumer for both. These support section 6.2.
- **Small and medium organizations baseline (CCCS Baseline Cyber Security Controls for Small and Medium Organizations V1.2 §3.10).** Every BC.10 control uses "should": require a SOC 3 report from cloud service providers (BC.10.1); evaluate how outsourced providers handle and access sensitive information (BC.10.2) and the legal jurisdictions where they store or use it (BC.10.3); communicate securely with all cloud services (BC.10.4); and use two-factor authentication for cloud administrative accounts that differ from internal administrator accounts (BC.10.5). Sections 4.1 and 4.3 correspond to BC.10.5.

To reduce the manual correlation an auditor would otherwise perform, the baseline's control sections map to the cited frameworks as follows. CIS benchmark recommendation numbers are version-specific; consult the applicable benchmark (Cloud Foundations Benchmark for §4 and §6, Cloud Productivity Foundations Benchmark for §5) for the exact recommendation identifiers within each named area.

| Baseline section | ISO/IEC 27001:2022 | CIS benchmark area | NIST SP 800-53 Rev. 5 |
|---|---|---|---|
| §4 Enterprise identity provider baseline | A.8.9, A.8.5, A.8.2 | Identity and Access Management | CM-2, CM-6 |
| §5 Cloud productivity platform baseline | A.8.9, A.8.23 | Email and collaboration security; storage; endpoint protection | CM-2, CM-6 |
| §6 Cloud platform baseline | A.8.9, A.8.24 | Identity and Access Management; Logging and Monitoring; Networking; Storage | CM-2, CM-6 |

Categorizing the business processes and information that a cloud service supports comes before selecting the controls for it: under CCCS ITSP.50.103, the service inherits the resulting security category (section 2), and the category informs the choice of security control profile (section 7). The categorization sources, including, for a Canadian federal department, the Treasury Board Standard on Security Categorization (Directive on Security Management, Appendix J), are in section 12 of the [Data Classification and Handling Standard](../security/standard-data-classification-and-handling.md).

---

*This document is released under the CC BY-SA 4.0 licence.*



**End of Document**
