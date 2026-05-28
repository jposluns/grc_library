# Cloud Security Configuration Baseline

**Document Title:** Cloud Security Configuration Baseline 
**Document Type:** Standard 
**Version:** 1.3.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`security/policy-information-security.md`](../security/policy-information-security.md), [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md), [`security/standard-authentication-and-password-management.md`](../security/standard-authentication-and-password-management.md), [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md), [`operations/standard-production-security-requirements.md`](standard-production-security-requirements.md) 
**Classification:** Public 
**Category:** Operations 
**Review Frequency:** Annual and upon material platform or regulatory change 
**Repository Path:** [`operations/standard-cloud-security-configuration-baseline.md`](standard-cloud-security-configuration-baseline.md) 
**Confidentiality:** Public 
**Licence:** CC0 1.0 Universal 

---

## 1. Purpose

This standard defines the secure configuration baseline for cloud and cloud productivity environments. It establishes minimum security configuration requirements for the cloud platform, enterprise identity provider, cloud productivity platform, and associated services to reduce attack surface and ensure that consistent security posture across all tenants and subscriptions.

---

## 2. Scope

1. Applies to all cloud tenants and subscriptions including cloud platform, enterprise identity provider, cloud productivity platform, and endpoint and email protection platform services.
2. Covers configuration of identity, network, compute, storage, monitoring, and collaboration services.
3. Applies to all environments: DEV, TEST, and PROD. Security classification applies consistently; TEST environments are not exempt from baseline security controls.
4. Applies to IT Operations, the infrastructure programme team, and any third party managing cloud resources on behalf of the organization.

---

## 3. Governance

| Role | Responsibility |
|---|---|
| Chief Information Security Officer (CISO) | Owns this standard; defines baseline requirements and approves exceptions |
| IT Operations / Cloud Team | Implements and maintains baseline configurations; remediates configuration drift |
| Infrastructure Programme Team | Ensures that all new infrastructure deployments conform to this standard from initial build |
| Internal Audit | Reviews compliance against baseline using the cloud security posture score and cloud security posture management (CSPM) tooling |

---

## 4. Enterprise Identity Provider Baseline

### 4.1 Multi-Factor Authentication (MFA)

- MFA is required for all users.
- Conditional Access policies enforce MFA for all cloud resource access.
- Legacy authentication protocols (basic auth, SMTP auth, IMAP) are blocked at the identity provider level.

### 4.2 Conditional Access

- Conditional Access is the primary enforcement layer for access policies.
- Risk-based policies (sign-in risk and user risk) are enabled.
- Compliant device requirement is enforced for access to corporate data.

### 4.3 Privileged Identity Management (PIM)

- PIM is enabled for all Global Administrator, Privileged Role Administrator, and cloud resource Owner roles.
- Standing (permanent) assignment to these roles is prohibited; time-bound activation is required.
- See the Privileged Access Management Standard for full requirements.

### 4.4 Enterprise Password Protection Service

- The enterprise password protection service is deployed to the on-premises directory to enforce banned-password lists.
- Password spray protection is enabled.

### 4.5 Security Defaults

- Security Defaults are superseded by Conditional Access policies.
- Where Conditional Access does not cover a scenario, Security Defaults provide fallback protection.

### 4.6 Guest Access

- External guest access is restricted to approved partner domains.
- Guest users cannot enumerate the directory or invite additional guests.
- Guest account lifecycle reviews occur quarterly.

---

## 5. Cloud Productivity Platform Baseline

### 5.1 Email Platform

| Control | Requirement |
|---|---|
| Anti-spoofing | DMARC, DKIM, and SPF configured and enforced |
| Safe Links | Enabled for all users |
| Safe Attachments | Enabled for all users |
| External email warning | Warning banners enabled on all inbound external email |
| Audit logging | Enabled for all mailboxes |

### 5.2 Collaboration Platform

- External communication restricted to approved domains.
- Anonymous access to meetings is disabled.
- Recording retention policies are configured per the data retention schedule.

### 5.3 Collaboration and File Storage Platform

- External sharing scoped to approved domains only.
- Unmanaged device access restricted to view-only.
- Sensitivity labels applied to classify and protect data per the Data Classification Standard.

### 5.4 Endpoint and Email Protection Platform

- Enabled at the equivalent of Plan 2 feature tier.
- Attack simulation training enabled.
- Preset security policies applied as baseline; custom tuning performed where needed.

---

## 6. Cloud Platform Baseline

### 6.1 Subscription and Resource Access

| Control | Requirement |
|---|---|
| Identity and access management | Governed by enterprise identity provider RBAC |
| Privileged roles | Owner and Contributor roles at subscription scope require PIM activation |
| Resource locks | Applied to all production resource groups to prevent accidental deletion or modification |

### 6.2 Network Security

- Network security groups (NSGs) applied to all subnets.
- No resources are directly exposed to the internet without a cloud firewall or web application firewall (WAF).
- RDP and SSH inbound access from the internet is blocked at the NSG level.

### 6.3 Monitoring and Logging

- The cloud monitoring service and SIEM are the primary platforms for monitoring and log aggregation.
- Diagnostic settings enabled for all resource types; log data forwarded to the SIEM workspace.
- Activity log retention minimum: 90 days.

### 6.4 Cloud Security Posture Management (CSPM)

- CSPM enabled across all subscriptions.
- Cloud security posture score reviewed monthly.
- High and Critical recommendations remediated within the timeframes defined in the Vulnerability Management Procedure.

### 6.5 Storage Accounts

| Control | Requirement |
|---|---|
| Public blob access | Disabled by default |
| Secure transfer | HTTPS only required |
| Shared Access Signatures (SAS) | Must be time-limited; unlimited-duration SAS tokens are prohibited |
| Storage protection | Cloud storage threat protection enabled |

### 6.6 Secrets Management Service

- All secrets, keys, and certificates must be stored in the secrets management service.
- Soft-delete and purge protection enabled.
- Access governed by enterprise identity provider RBAC; PIM activation required for high-privilege operations.

---

## 7. Configuration Drift

| Condition | Response |
|---|---|
| Drift detected | CSPM policy compliance and cloud security posture score monitoring trigger alert |
| Review cadence | Drift reviewed weekly |
| High-risk drift (score reduction > 5%, or critical security control disabled) | Treated as P2 incident; remediated within 48 hours |
| All configuration changes | Must follow the Change Management Procedure |

---

## 8. Framework Alignment

| Framework | Reference | Topic |
|---|---|---|
| ISO/IEC 27001:2022 | A.8.9 | Configuration Management |
| CIS Cloud Foundations Benchmark | v2.0 | Secure cloud platform configuration |
| CIS Cloud Productivity Foundations Benchmark | v3.0 | Secure cloud productivity configuration |
| NIST SP 800-53 | CM-2, CM-6 | Configuration Baseline and Settings |
| COBIT 2025 | DSS05 | Manage Security Services |
| CSA CCM v5 | IVS-01, IVS-04 | Infrastructure and Virtualization Security |

---

*This document is released under the CC0 1.0 Universal Public Domain Dedication. No rights reserved.*



**End of Document**
