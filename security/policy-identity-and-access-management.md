# Identity and Access Management Policy

**Document Title:** Identity and Access Management Policy  
**Document Type:** Policy  
**Version:** 1.3.0  
**Date:** 2026-05-27  
**Owner:** Chief Information Security Officer  
**Approving Authority:** Governance Library Maintainer  
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/standard-privileged-access-management.md`](standard-privileged-access-management.md), [`security/standard-authentication-and-password-management.md`](standard-authentication-and-password-management.md), [`security/standard-logging-and-monitoring.md`](standard-logging-and-monitoring.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md)  
**Classification:** Public  
**Category:** Information Security  
**Review Frequency:** Annual and upon material threat, framework, or regulatory change  
**Repository Path:** [`security/policy-identity-and-access-management.md`](policy-identity-and-access-management.md)  
**Confidentiality:** Public  
**Licence:** CC0 1.0 Universal  

This policy establishes the principles, control objectives, and governance requirements for identity and access management (IAM) across all systems, applications, and environments.

---

## Purpose

To ensure that all users — human, service, and machine — are uniquely identified, appropriately authenticated, and authorized according to business need, while maintaining compliance with information security, privacy, and regulatory obligations.

---

## Scope

1. Applies to all employees, contractors, vendors, and partners accessing organizational systems, data, or cloud environments.
2. Covers all authentication mechanisms: passwords, tokens, biometrics, certificates, federated identities, and API/service accounts.
3. Applies to all IT, OT, and AI systems managed on-premises, in cloud, or hybrid environments.
4. Includes both privileged and non-privileged access across applications, infrastructure, and data assets.

---

## Governance and Accountability

| Role | Responsibility |
| --- | --- |
| CIO | Accountable for IAM strategy, architecture, and integration with enterprise risk management. |
| CISO | Responsible for enforcement, compliance monitoring, and IAM control validation. |
| IT Operations / Security Engineering | Responsible for implementation, configuration, and monitoring of IAM technologies. |
| System and Application Owners | Ensure proper access design and periodic certification within their systems. |
| Managers and Supervisors | Approve and review user access rights for their direct reports. |
| Users | Must safeguard credentials and comply with authentication requirements. |

---

## Policy Statements

### 1. Identity Management

1.1 All identities (user, service, and device) shall be uniquely identifiable and associated with a verified entity.
1.2 Access provisioning shall follow the principle of least privilege and need to know.
1.3 IAM directories must maintain authoritative records of all identities, access entitlements, and authentication factors.
1.4 Identities must be deactivated within 24 hours of termination or contract completion.

### 2. Authentication

2.1 Multi-Factor Authentication (MFA) is mandatory for all privileged accounts and remote access.
2.2 Passwords and tokens shall comply with NIST SP 800-63B complexity and rotation standards.
2.3 Where possible, passwordless authentication (FIDO2 or certificate-based) shall be implemented to reduce credential theft risks.
2.4 Shared credentials are prohibited; each account must be traceable to a single entity.

### 3. Authorization

3.1 All access shall be role-based (RBAC) or attribute-based (ABAC) where feasible. Roles must align with approved job functions, data classifications, and BASC Section 6 access-security requirements.
3.2 Segregation of Duties (SoD) must be implemented for high-risk roles to prevent conflicts of interest.
3.3 Temporary access (e.g., vendor or project) must include start and expiry dates and be reviewed prior to renewal.
3.4 System owners shall review user entitlements at least quarterly.

### 4. Privileged Access Management (PAM)

4.1 Privileged accounts (administrators, root, service, and API keys) must be centrally managed and audited.
4.2 Privileged access sessions must be logged, monitored, and retained for a minimum of one year.
4.3 Emergency ("break-glass") accounts shall have documented approval, use, and expiration controls.

### 5. Access Review and Certification

5.1 All user and service account access rights shall undergo periodic certification at least annually, with evidence maintained.
5.2 Any discrepancies identified during certification must be remediated within 15 business days.
5.3 Audit logs for provisioning, deprovisioning, and certification must be preserved for compliance verification.

### 6. AI and Automation Access Controls

6.1 AI systems, automation agents, and APIs shall have discrete non-human identities subject to equivalent authentication and access governance.
6.2 AI models and training environments must use signed access tokens with expiration control.
6.3 Access to AI model weights, embeddings, or datasets must be limited to authorized personnel and validated through logs.

### 7. Monitoring and Logging

7.1 All IAM events — including logins, privilege escalations, failed authentications, and permission changes — shall be logged in the SIEM per the Logging and Monitoring Standard.
7.2 IAM alerts must be correlated with endpoint and network telemetry to detect anomalous behaviour.
7.3 AI-driven anomaly detection may be used to identify compromised accounts or access misuse.

### 8. Compliance and Audit

8.1 IAM compliance is monitored through periodic audits and control assessments.
8.2 Nonconformities or violations must be logged, remediated, and tracked through the Corrective and Preventive Action Procedure.
8.3 Exceptions must be documented under the Exception Management Policy and approved by the CISO.

### 9. Training and Awareness

9.1 All employees must complete annual IAM and phishing awareness training.
9.2 Technical personnel with access to privileged systems must undergo role-specific PAM and identity-security training.

### 10. Continual Improvement

10.1 IAM processes shall be reviewed annually in conjunction with ISO 27001 and COBIT DSS05 controls.
10.2 Emerging technologies such as adaptive authentication, identity federation, and decentralized ID (DID) models shall be evaluated for adoption.

---

## Framework Alignment

| Control Area | ISO/IEC 27001 | ISO/IEC 27002 | NIST | COBIT 2025 | CSA CCM v5 |
| --- | --- | --- | --- | --- | --- |
| Identity Management | A.5.15–A.5.20 | 9.1–9.4 | SP 800-63 | DSS05 | IAM-01–09 |
| Authentication | A.8.5 | §8.3 | SP 800-63B | DSS05.04 | IAM-06, IAM-08 |
| Privileged Access | A.8.2 | §8.2 | SP 800-53 AC-2, AC-6 | DSS05.04 | IAM-02, IAM-04 |
| Access Review | A.5.18 | — | SP 800-53 AC-2 | MEA01 | IAM-10 |
| AI/Automation Access | A.8 (emerging) | — | AI RMF | DSS05.06 | IAM-14 |



**End of Document**
