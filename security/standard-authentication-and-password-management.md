# Authentication and Password Management Standard

**Document Title:** Authentication and Password Management Standard 
**Document Type:** Standard 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`security/policy-identity-and-access-management.md`](policy-identity-and-access-management.md), [`security/standard-privileged-access-management.md`](standard-privileged-access-management.md) 
**Classification:** Public 
**Category:** Information Security 
**Review Frequency:** Annual and upon material threat, framework, or regulatory change 
**Repository Path:** [`security/standard-authentication-and-password-management.md`](standard-authentication-and-password-management.md) 
**Confidentiality:** Public 
**Licence:** CC0 1.0 Universal 

This standard defines authentication and password management requirements across all systems, applications, and services. It consolidates requirements referenced across the PAM Standard, Cloud Security Configuration Baseline, and IAM Policy into a single authoritative reference.

---

## Purpose

To establish consistent, risk-proportionate authentication controls that reduce the risk of credential theft, brute force, and account takeover.

---

## Scope

1. Applies to all user accounts, service accounts, and system accounts across on-premises and cloud environments.
2. Covers password construction, MFA requirements, session management, and authentication exception handling.
3. Applies to all personnel and systems.

---

## Governance and Accountability

| Role | Responsibility |
| --- | --- |
| CISO | Owns this standard; approves exceptions to MFA requirements. |
| IT Operations / IAM Team | Enforces authentication controls via Conditional Access, enterprise identity provider, and endpoint management platform; manages MFA configuration. |
| System / Application Owners | Ensure that their systems enforce password and authentication policies; report deviations to IT Operations. |

---

## Password Requirements

| Parameter | Requirement |
| --- | --- |
| Minimum length | 14 characters for standard accounts; 20 characters for privileged accounts |
| Complexity | Must include characters from at least 3 of: uppercase, lowercase, numerals, special characters. Passphrases are preferred over complex short passwords. |
| Prohibited passwords | Banned via enterprise password protection service (common passwords, company name variants, sequential patterns). Dictionary words as sole content are prohibited. |
| Password reuse | Last 12 passwords may not be reused. |
| Maximum age | No mandatory expiry for accounts protected by MFA, per NIST SP 800-63B guidance. Passwords must be changed immediately upon suspected compromise. |
| Storage | Passwords must never be stored in plaintext. All systems must use salted cryptographic hashing (bcrypt, Argon2, or equivalent). Stored secrets are managed by the secrets management service. |

---

## Multi-Factor Authentication (MFA)

MFA is mandatory for all accounts without exception. There are no circumstances under which a user account may access company resources without MFA enrolled.

**MFA method hierarchy (in order of preference):**
1. FIDO2 hardware security key
2. Authenticator app with number matching enabled
3. Software TOTP token
4. SMS OTP: permitted only where no other method is technically feasible; deprecated by default. SMS OTP is **not** permitted for privileged accounts.

MFA is enforced at the enterprise identity provider Conditional Access layer.

---

## Session Management

Sessions on cloud and productivity platforms are governed by Conditional Access sign-in frequency policies:
- Maximum session lifetime before re-authentication: 8 hours for standard users; 1 hour for privileged role activations.
- Idle session timeout on managed devices: 15 minutes, enforced via endpoint management platform compliance policy.
- Persistent browser sessions are disabled for high-sensitivity applications.

---

## Service Account Authentication

Service accounts must use managed identities, workload identities, or certificate-based authentication wherever technically feasible.

Password-based service account authentication is only permitted where no alternative exists, and must be documented as an exception with a compensating control and a remediation target date. Service account passwords must meet privileged account length requirements and be stored in the secrets management service.

---

## Exceptions

Exceptions to any requirement in this standard require CISO approval and must be documented with a compensating control and a remediation target date. No exception may remain open beyond 12 months without re-approval.

---

## Framework Alignment

| Control | NIST SP 800-63B | ISO/IEC 27001 | CSA CCM v5 | CIS |
| --- | --- | --- | --- | --- |
| Password requirements | §5.1.1 | A.8.5 | IAM-06 | Control 5 |
| MFA | §6.3 | A.8.5 | IAM-08 | Control 6 |
| Session management | §7.1 | A.8.5 | IAM-09 | Control 5 |
| Service account auth | N/A | A.8.2 | IAM-02 | Control 5 |



**End of Document**
