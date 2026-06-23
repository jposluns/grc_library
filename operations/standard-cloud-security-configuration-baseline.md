# Cloud Security Configuration Baseline

**Document Title:** Cloud Security Configuration Baseline\
**Document Type:** Standard\
**Version:** 1.4.6\
**Date:** 2026-06-23\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](../security/policy-information-security.md), [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md), [`security/standard-authentication-and-password-management.md`](../security/standard-authentication-and-password-management.md), [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md), [`operations/standard-production-security-requirements.md`](standard-production-security-requirements.md)\
**Classification:** Public\
**Category:** Operations\
**Review Frequency:** Annual and upon material platform or regulatory change\
**Repository Path:** [`operations/standard-cloud-security-configuration-baseline.md`](standard-cloud-security-configuration-baseline.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines the secure configuration baseline for cloud and cloud productivity environments. It establishes minimum security configuration requirements for the cloud platform, enterprise identity provider, cloud productivity platform, and associated services to reduce attack surface and ensure that consistent security posture across all tenants and subscriptions.

---

## 2. Scope

1. Applies to all cloud tenants and subscriptions including cloud platform, enterprise identity provider, cloud productivity platform, and endpoint and email protection platform services.
2. Covers configuration of identity, network, compute, storage, monitoring, and collaboration services.
3. Applies to all environments: DEV, TEST, and PROD. Security classification applies consistently; TEST environments are not exempt from baseline security controls.
4. Applies to IT Operations, the infrastructure programme team, and any third party managing cloud resources on behalf of the organisation.

### 2.1 Scope boundary with dev-security cloud hardening baselines

This standard and the per-provider cloud hardening baselines in `dev-security/` together cover the organisation's cloud security posture. The boundary is as follows:

| Subject | Authoritative standard |
| --- | --- |
| Enterprise-tenant administration (identity provider tenant, organisation/management-group hierarchy, tenant-wide policies, cross-account trust, productivity SaaS, email and collaboration platforms) | This standard |
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
| Chief Information Security Officer (CISO) | Owns this standard; defines baseline requirements and approves exceptions |
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
| Shared Access Signatures (SAS) | Must be time-limited; unlimited-duration SAS tokens are prohibited |
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
| CIS Cloud Foundations Benchmark | v2.0 | Secure cloud platform configuration |
| CIS Cloud Productivity Foundations Benchmark | v3.0 | Secure cloud productivity configuration |
| NIST SP 800-53 | CM-2, CM-6 | Configuration Baseline and Settings |
| COBIT 2019 | DSS05 | Manage Security Services |
| CSA CCM v4.1 | IVS-01, IVS-04 | Infrastructure and Virtualization Security |

To reduce the manual correlation an auditor would otherwise perform, the baseline's control sections map to the cited frameworks as follows. CIS benchmark recommendation numbers are version-specific; consult the applicable benchmark (Cloud Foundations Benchmark for §4 and §6, Cloud Productivity Foundations Benchmark for §5) for the exact recommendation identifiers within each named area.

| Baseline section | ISO/IEC 27001:2022 | CIS benchmark area | NIST SP 800-53 |
|---|---|---|---|
| §4 Enterprise identity provider baseline | A.8.9, A.8.24 | Identity and Access Management | CM-2, CM-6 |
| §5 Cloud productivity platform baseline | A.8.9, A.8.23 | Email and collaboration security; storage; endpoint protection | CM-2, CM-6 |
| §6 Cloud platform baseline | A.8.9, A.8.24 | Identity and Access Management; Logging and Monitoring; Networking; Storage | CM-2, CM-6 |

---

*This document is released under the CC BY-SA 4.0 licence. No rights reserved.*



**End of Document**
