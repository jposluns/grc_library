# Identity Management Procedure

**Document Title:** Identity Management Procedure 
**Document Type:** Procedure 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Chief Information Officer 
**Related Documents:** [`security/procedure-access-control.md`](procedure-access-control.md), [`security/procedure-onboarding-and-offboarding.md`](procedure-onboarding-and-offboarding.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md) 
**Classification:** Public 
**Category:** Information Security 
**Review Frequency:** Annual and upon material platform or regulatory change 
**Repository Path:** [`security/procedure-identity-management.md`](procedure-identity-management.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This procedure defines the processes for managing digital identities throughout their lifecycle: creation, maintenance, authentication configuration, privileged access management, and termination. It ensures that every identity within the organisation's systems is unique, accountable, appropriately privileged, and subject to regular review.

---

## Scope

Applies to all user identities, service accounts, and machine identities across all organisational platforms including on-premises systems, cloud platforms, applications, network devices, and development environments. Covers employees, contractors, temporary workers, and third-party service accounts.

---

## Roles and responsibilities

| Role | Responsibility |
| --- | --- |
| **CISO** | Owns identity governance policy; approves privileged identity changes. |
| **IT Operations: Identity Team** | Executes identity lifecycle operations; manages identity platform. |
| **HR / People Operations** | Initiates onboarding and offboarding notifications. |
| **Manager / People Leader** | Approves identity requests for their team; confirms offboarding completeness. |
| **Internal Audit** | Reviews identity inventory and access certification completeness annually. |

---

## 1. Identity creation

1.1 Identity creation is triggered by the approved onboarding workflow initiated by HR or People Operations.

1.2 Each user receives a unique identity: shared accounts are prohibited except for approved service account use cases.

1.3 Identity creation includes:
- Unique username following the approved naming convention.
- Role-based group membership assignment aligned to job function.
- Multi-factor authentication (MFA) enrolment: mandatory before first login.
- Initial password set to a temporary value requiring change at first login.

1.4 Service account identities require:
- Named owner (role title).
- Documented business justification.
- Defined expiry date or review date.
- No interactive login where technically feasible.

1.5 All new identities are recorded in the identity management platform within 1 business day of creation.

---

## 2. Authentication standards

2.1 Multi-factor authentication (MFA) is mandatory for:
- All cloud platform and cloud application access.
- All privileged and administrative accounts.
- All remote access.
- All access to systems containing sensitive or personal data.

2.2 FIDO2 / passkey authentication is the preferred MFA method where supported.

2.3 Password requirements for accounts where password authentication applies:
- Minimum 14 characters.
- Complexity: upper/lower case, numbers, special characters.
- No reuse of the last 10 passwords.
- No periodic forced rotation unless compromise is suspected.
- Passwords must not appear in known breach databases (checked via enterprise password protection service).

2.4 Passwordless authentication is preferred and actively implemented for new systems.

---

## 3. Privileged identity management

3.1 Privileged identities (domain admin, cloud admin, root, sudo, security platform admin) are managed through the Privileged Identity Management (PIM) system.

3.2 PIM controls:
- Just-in-time activation required: no standing privileged access.
- Time-limited sessions: maximum 4 hours, extendable with re-approval.
- Approval workflow required for activation.
- Full session recording and logging.
- Quarterly access review by CISO.

3.3 Privileged accounts are separate from day-to-day user accounts: no single account is used for both standard and privileged operations.

3.4 Privileged access for external vendors is time-limited and scoped to minimum required permissions.

---

## 4. Identity maintenance

4.1 Identity attributes (role, department, manager) are maintained by HR and updated within 1 business day of change.

4.2 Role changes trigger an automatic access review notification to the system owner and Identity Team.

4.3 Accounts inactive for 45 days are automatically disabled. Accounts inactive for 90 days are reviewed for deactivation.

4.4 Service accounts are reviewed annually. Accounts with no activity in 90 days are disabled pending investigation.

---

## 5. Access certification

5.1 Access certifications confirm that each identity's access remains appropriate.

5.2 Certification frequency:
- All accounts: annual certification.
- Privileged accounts: quarterly certification.
- Third-party accounts: on contract renewal and at minimum annually.

5.3 Certification is conducted by the account owner's manager and the system owner.

5.4 Uncertified access is suspended pending confirmation and permanently revoked if not certified within 10 business days.

---

## 6. Identity termination

6.1 Identity termination is triggered by the offboarding workflow.

6.2 Termination timeline:
- Voluntary departure: all access disabled end of last working day.
- Involuntary termination: all access disabled within 1 hour of notification.

6.3 Termination includes:
- Disabling the account in all identity systems.
- Removing all group memberships and role assignments.
- Revoking all active sessions and tokens.
- Revoking or transferring any certificates or keys owned by the identity.
- Transferring ownership of data and shared resources.

6.4 Identity records are retained per the Data Retention Schedule for audit purposes.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27001:2022 | Annex A.5.15 to 5.18: Access Control | Identity lifecycle governance |
| ISO/IEC 27002:2022 | §5.16 to 5.17: Identity Management | Identity and authentication controls |
| NIST SP 800-53 | IA: Identification and Authentication Family | Identity assurance controls |
| NIST SP 800-207 | Zero Trust Architecture | Continuous identity validation |
| COBIT 2019 | DSS05: Manage Security Services | Identity security operations |
| CSA CCM v4.1 | IAM-01 through IAM-14 | Cloud identity and access management |

---

**End of Document**
