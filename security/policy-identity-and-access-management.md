# Identity and Access Management Policy

**Document Title:** Identity and Access Management Policy\
**Document Type:** Policy\
**Version:** 1.3.10\
**Date:** 2026-07-05\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/standard-privileged-access-management.md`](standard-privileged-access-management.md), [`security/standard-authentication-and-password-management.md`](standard-authentication-and-password-management.md), [`security/standard-logging-and-monitoring.md`](standard-logging-and-monitoring.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material threat, framework, or regulatory change\
**Repository Path:** [`security/policy-identity-and-access-management.md`](policy-identity-and-access-management.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

This policy establishes the principles, control objectives, and governance requirements for identity and access management (IAM) across all systems, applications, and environments.

---

## 1. Purpose

To ensure that all users, human, service, and machine, are uniquely identified, appropriately authenticated, and authorized according to business need, while maintaining compliance with information security, privacy, and regulatory obligations.

---

## 2. Scope

1. Applies to all employees, contractors, vendors, and partners accessing organizational systems, data, or cloud environments.
2. Covers all authentication mechanisms: passwords, tokens, biometrics, certificates, federated identities, and API/service accounts.
3. Applies to all IT, OT, and AI systems managed on-premises, in cloud, or hybrid environments.
4. Includes both privileged and non-privileged access across applications, infrastructure, and data assets.

---

## 3. Governance and accountability

| Role | Responsibility |
| --- | --- |
| CIO | Accountable for IAM strategy, architecture, and integration with enterprise risk management. |
| CISO | Responsible for enforcement, compliance monitoring, and IAM control validation. |
| IT Operations / Security Engineering | Responsible for implementation, configuration, and monitoring of IAM technologies. |
| System and Application Owners | Ensure that proper access design and periodic certification are carried out within their systems. |
| Managers and Supervisors | Approve and review user access rights for their direct reports. |
| Users | Must safeguard credentials and comply with authentication requirements. |

---

## 4. Policy statements

### 4.1 Identity management

4.1.1 All identities (user, service, and device) must be uniquely identifiable and associated with a verified entity.
4.1.2 Access provisioning must follow the principle of least privilege and need to know.
4.1.3 IAM directories must maintain authoritative records of all identities, access entitlements, and authentication factors.
4.1.4 Identities must be deactivated within 24 hours of termination or contract completion.

### 4.2 Authentication

4.2.1 Multi-Factor Authentication (MFA) is mandatory for all privileged accounts and remote access.
4.2.2 Passwords and tokens must comply with NIST SP 800-63B complexity and rotation standards.
4.2.3 Where possible, passwordless authentication (FIDO2 or certificate-based) must be implemented to reduce credential theft risks.
4.2.4 Shared credentials are prohibited; each account must be traceable to a single entity.

### 4.3 Authorization

4.3.1 All access must be role-based (RBAC) or attribute-based (ABAC) where feasible. Roles must align with approved job functions, data classifications, and BASC Section 6 access-security requirements.
4.3.2 Segregation of Duties (SoD) must be implemented for high-risk roles to prevent conflicts of interest.
4.3.3 Temporary access (e.g., vendor or project) must include start and expiry dates and be reviewed prior to renewal.
4.3.4 System owners must review user entitlements at least quarterly.

### 4.4 Privileged access management (PAM)

4.4.1 Privileged accounts (administrators, root, service, and API keys) must be centrally managed and audited.
4.4.2 Privileged access sessions must be logged, monitored, and retained per the [data-retention schedule](../governance/register-data-retention-schedule.md) (2 years for privileged-access session logs).
4.4.3 Emergency ("break-glass") accounts must have documented approval, use, and expiration controls.

### 4.5 Access review and certification

4.5.1 All user and service account access rights must undergo periodic certification at least annually, with evidence maintained.
4.5.2 Any discrepancies identified during certification must be remediated within 15 business days.
4.5.3 Audit logs for provisioning, deprovisioning, and certification must be preserved for compliance verification.

### 4.6 AI and automation access controls

4.6.1 AI systems, automation agents, and APIs must have discrete non-human identities subject to equivalent authentication and access governance.
4.6.2 AI models and training environments must use signed access tokens with expiration control.
4.6.3 Access to AI model weights, embeddings, or datasets must be limited to authorized personnel and validated through logs.

### 4.7 Monitoring and logging

4.7.1 All IAM events, including logins, privilege escalations, failed authentications, and permission changes, must be logged in the SIEM per the Logging and Monitoring Standard.
4.7.2 IAM alerts must be correlated with endpoint and network telemetry to detect anomalous behaviour.
4.7.3 AI-driven anomaly detection may be used to identify compromised accounts or access misuse.

### 4.8 Compliance and audit

4.8.1 IAM compliance is monitored through periodic audits and control assessments.
4.8.2 Nonconformities or violations must be logged, remediated, and tracked through the Corrective and Preventive Action Procedure.
4.8.3 Exceptions must be documented under the Exception Management Policy and approved by the CISO.

### 4.9 Training and awareness

4.9.1 All employees must complete annual IAM and phishing awareness training.
4.9.2 Technical personnel with access to privileged systems must undergo role-specific PAM and identity-security training.

### 4.10 Continual improvement

4.10.1 IAM processes must be reviewed annually in conjunction with ISO/IEC 27001 and COBIT DSS05 controls.
4.10.2 Emerging technologies such as adaptive authentication, identity federation, and decentralized ID (DID) models must be evaluated for adoption.

---

## 5. Framework alignment

| Control Area | ISO/IEC 27001:2022 | ISO/IEC 27002:2022 | NIST | COBIT 2019 | CSA CCM v4.1 |
| --- | --- | --- | --- | --- | --- |
| Identity Management | A.5.15 to A.5.18 | §5.16 to 5.17 | SP 800-63 | DSS05 | IAM-01 to 09 |
| Authentication | A.8.5 | §8.5 | SP 800-63B | DSS05.04 | IAM-06, IAM-08 |
| Privileged Access | A.8.2 | §8.2 | SP 800-53 AC-2, AC-6 | DSS05.04 | IAM-02, IAM-04 |
| Access Review | A.5.18 | §5.18 | SP 800-53 AC-2 | MEA01 | IAM-10 |
| AI/Automation Access | A.8 (emerging) | N/A | AI RMF | DSS05.06 | IAM-14 |



**End of Document**
