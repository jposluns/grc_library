# Privileged Access Management Standard

**Document Title:** Privileged Access Management Standard 
**Document Type:** Standard 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`security/policy-identity-and-access-management.md`](policy-identity-and-access-management.md), [`security/policy-information-security.md`](policy-information-security.md), [`security/standard-authentication-and-password-management.md`](standard-authentication-and-password-management.md) 
**Classification:** Public 
**Category:** Information Security 
**Review Frequency:** Annual and upon material threat, framework, or regulatory change 
**Repository Path:** [`security/standard-privileged-access-management.md`](standard-privileged-access-management.md) 
**Confidentiality:** Public 
**Licence:** CC0 1.0 Universal 

This standard defines the requirements for managing privileged access across systems and environments. It establishes controls for the identification, provisioning, monitoring, and revocation of privileged accounts to minimize the risk of unauthorized access, credential abuse, and lateral movement.

---

## Purpose

To ensure that privileged accounts are managed, monitored, and revoked according to a documented, auditable process that reduces the attack surface available to insider threats and external adversaries.

---

## Scope

1. Applies to all accounts with elevated privileges including domain administrators, local administrators, service accounts, cloud management identities, and database administrator accounts.
2. Covers on-premises directory services, enterprise identity provider (cloud and hybrid), productivity platform, cloud resources, and any other platform granting privileged access.
3. Applies to all employees, contractors, and third-party providers who hold or require privileged access.

---

## Governance and Accountability

| Role | Responsibility |
| --- | --- |
| CIO | Executive accountability for the PAM programme and alignment with enterprise risk posture. |
| CISO | Owns this standard, defines privileged account policy, and oversees monitoring and audit. |
| IT Operations / IAM Team | Implements PAM controls, manages PIM configuration, and conducts access reviews. |
| System and Application Owners | Identify privileged accounts within their systems and confirm access appropriateness. |
| Internal Audit | Conducts periodic reviews of privileged account usage and PAM control effectiveness. |

---

## PAM Approach

### Primary Tool: Privileged Identity Management (PIM)

The primary PAM approach uses Privileged Identity Management (PIM), which provides just-in-time (JIT) privileged access, time-bound role activation, approval workflows, and audit logging for cloud and productivity platform roles. PIM is the default implementation for all cloud directory and platform privileged roles.

Third-party PAM solutions remain available for extended use cases including on-premises systems and external vendor access management.

### Key PAM Controls

| Control | Requirement |
| --- | --- |
| Just-in-Time Access | Privileged roles must be activated on demand for defined time periods. Permanent standing privilege is prohibited for all accounts where JIT activation is available. |
| Approval Workflows | High-risk role activations require approval from a designated approver before access is granted. |
| Multi-Factor Authentication | MFA is required for all privileged role activations without exception. |
| Time-Bound Activation | Role activations are time-limited. Default maximum activation period is 8 hours; extended periods require justification and approval. |
| Least Privilege | Privileged access is scoped to the minimum permissions required for the task. Broad administrative roles are not assigned where narrower roles are available. |
| Separation of Duties | Accounts used for standard day-to-day work are separate from privileged administrative accounts. |
| Service Account Controls | Service accounts must use managed identities or dedicated non-interactive accounts. Service account passwords must meet complexity requirements and be rotated at least annually or upon staff change. |
| Emergency / Break-Glass Accounts | Emergency access accounts must be documented, credentials securely stored, and usage subject to immediate notification and post-access review. |

---

## Privileged Account Lifecycle

**Provisioning:** All privileged account requests must be approved by the account owner's manager and the CISO or delegate. Requests must include business justification and expected duration. Accounts are created following the principle of least privilege.

**Access Reviews:** All privileged accounts undergo access review at minimum quarterly. Reviews are conducted by System Owners and validated by the IAM Team. Accounts that cannot be justified are revoked immediately.

**Monitoring and Alerting:** All privileged account activations, role assignments, and access events are logged to the SIEM. Alerts are configured for anomalous activity including off-hours activations, repeated failed activations, and bulk role assignments.

**Revocation:** Privileged access is revoked within 24 hours of role change, departure, or project completion. Service account access is revoked when the associated application is decommissioned.

---

## Incident Response

Suspected compromise of a privileged account constitutes a P1 security incident. The IAM Team must immediately disable the account, revoke active sessions, and notify the CISO. All privileged credential compromises follow the Incident Response Procedure.

---

## Framework Alignment

| Control | ISO/IEC 27001 | NIST SP 800-53 | COBIT 2025 | CSA CCM v5 | CIS |
| --- | --- | --- | --- | --- | --- |
| Privileged access rights | A.8.2 | AC-2, AC-6 | DSS05.04 | IAM-02, IAM-04 | Control 5 |
| Just-in-time access | A.5.18 | AC-2(7) | N/A | IAM-04 | Control 6 |
| Emergency access | A.5.17 | AC-2(2) | DSS05.04 | IAM-03 | N/A |
| Session logging | A.8.15 | AU-2, AU-12 | DSS05.04 | IAM-06 | Control 8 |



**End of Document**
