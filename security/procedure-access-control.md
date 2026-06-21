# Access Control Procedure

**Document Title:** Access Control Procedure\
**Document Type:** Procedure\
**Version:** 1.1.1\
**Date:** 2026-06-21\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`security/procedure-identity-management.md`](procedure-identity-management.md), [`security/procedure-onboarding-and-offboarding.md`](procedure-onboarding-and-offboarding.md), [`security/procedure-security-incident-response.md`](procedure-security-incident-response.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md), [`risk/procedure-risk-assessment-methodology.md`](../risk/procedure-risk-assessment-methodology.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material system or regulatory change\
**Repository Path:** [`security/procedure-access-control.md`](procedure-access-control.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure defines the processes for granting, reviewing, modifying, and revoking access to organisational systems, applications, data, and network resources. It implements the principle of least privilege and need-to-know access model across all platforms, ensuring access is appropriate, authorized, and periodically reviewed.

---

## Scope

Applies to all access to organisational systems including cloud platforms, on-premises systems, applications, network infrastructure, databases, development environments, and privileged management interfaces. Covers all user types: employees, contractors, third parties, and service accounts.

---

## Roles and responsibilities

| Role | Responsibility |
| --- | --- |
| **CISO** | Owns access control policy and reviews privileged access quarterly. |
| **IT Operations / Identity Team** | Provisions and deprovisions access; maintains access management tooling. |
| **System / Application Owner** | Approves access requests for their systems; conducts periodic access reviews. |
| **Manager / People Leader** | Initiates and approves access requests for their team members. |
| **Internal Audit** | Conducts access certification audits and reviews for compliance. |

---

## 1. Access request and approval

1.1 All access requests must be submitted through the ITSM portal with:
- User identity and role.
- System or resource requested.
- Access level required.
- Business justification.
- Approving manager confirmation.

1.2 System owners approve or decline access requests for their systems within 3 business days of submission.

1.2.1 If a system owner does not approve or decline a request within the 3-business-day SLA, the request is auto-escalated to the system owner's manager, who must approve or decline within a further 2 business days.

1.2.2 If the manager does not act within the 2-business-day escalation window, the request is auto-escalated to the CISO, who must approve or decline within a further 2 business days.

1.2.3 If the CISO does not act within the 2-business-day window, the request is auto-declined and the requester is notified. The requester may resubmit with additional justification, restarting the SLA.

1.2.4 Auto-escalation and auto-decline events are logged in the ITSM portal and reviewed by the CISO quarterly as part of the access-control programme metrics.

1.3 Privileged access (administrative rights, root/sudo, domain admin) requires additional approval from the CISO or delegated security lead.

1.4 Emergency access requests may be approved verbally only when (a) a declared incident response is active under [`security/procedure-security-incident-response.md`](procedure-security-incident-response.md) or (b) the delay imposed by ITSM-portal submission would itself cause material business or safety harm. The approver in either case is the CISO or a delegated security lead.

1.4.1 Verbal approval must be formalised by the approver as an ITSM ticket within 24 hours of grant, with the trigger condition, the named approver, the granted access, and the access expiry recorded.

1.4.2 If verbal-approval access has not been formalised within 24 hours, the Identity Team must revoke the access at the 24-hour mark and notify the CISO. Re-grant requires the standard request-and-approval flow under §1.1.

1.4.3 Emergency access events (both formalised and revoked-for-non-formalisation) are reviewed by the CISO quarterly as part of the access-control programme metrics.

---

## 2. Access provisioning

2.1 Access is provisioned by the Identity Team following approved request documentation.

2.2 Access is provisioned using role-based access control (RBAC) aligned to job function.

2.3 No account is provisioned with more access than required for the defined role (least privilege).

2.4 Service accounts are assigned the minimum permissions required for their function. Shared service account credentials are prohibited.

2.5 Privileged accounts are provisioned in the Privileged Identity Management (PIM) system with just-in-time activation and time-limited sessions.

---

## 3. Access review

3.1 System owners conduct access reviews for their systems at the following frequency:

| Access Type | Review Frequency |
| --- | --- |
| Privileged / administrative access | Quarterly |
| Standard user access: high-sensitivity systems | Semi-annual |
| Standard user access: general systems | Annual |
| Third-party / contractor access | On contract renewal and at least annually |

3.2 Access reviews confirm that each user's current access:

- Matches the access profile documented for the user's current role in the RBAC catalogue;
- Does not exceed the minimum required for the user's current responsibilities, applying the least-privilege principle stated in the Access provisioning section;
- Has a current business justification on file matching the requirements in the Access request and approval section;
- For privileged access, remains within the active membership of the corresponding PIM role.

Access that does not meet all four criteria is treated as unjustified and revoked under the next access review.

3.3 Access that cannot be justified is revoked immediately.

3.4 Access review completion status is reported to the CISO quarterly.

---

## 4. Access modification

4.1 Access must be modified when a user changes role, changes location, or when their responsibilities change materially.

4.2 Managers initiate role-change access modifications through the ITSM portal at the time of the role change.

4.3 The Identity Team processes modifications within 1 business day of approval.

---

## 5. Access revocation

5.1 Access is revoked in the following circumstances:

| Trigger | Revocation Timeline |
| --- | --- |
| Voluntary resignation | End of last working day |
| Involuntary termination | Immediate (within 1 hour) |
| Role change (access no longer required) | Within 1 business day |
| Contract expiry | At contract end date |
| Security incident or investigation | Immediate upon instruction |

5.2 The offboarding checklist confirms all access is revoked. Revocation is verified by the Identity Team within 24 hours of the effective date.

5.3 Third-party access is revoked in coordination with the supplier or contract manager.

---

## 6. Privileged access management

6.1 Privileged access is subject to the following additional controls:
- All privileged sessions are recorded and logged.
- Privileged accounts require MFA at every authentication.
- Just-in-time access activation required for all domain and cloud administrative roles.
- Privileged activity is reviewed by the CISO quarterly.

6.2 Standing privileged access is prohibited unless operationally necessary and approved by the CISO.

6.3 Break-glass (emergency) accounts are sealed, inventoried, and their use triggers an immediate security alert.

---

## 7. Third-party and vendor access

7.1 Third-party access is time-limited, scoped to the minimum required, and requires a named sponsor.

7.2 Third-party access must be reviewed at contract renewal or at least every 12 months.

7.3 Third-party privileged access follows the same controls as internal privileged access.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27001:2022 | Annex A.5.15 to 5.18: Access Control | Access governance |
| ISO/IEC 27002:2022 | §5.15 to 5.18 | Access request, review, and revocation |
| NIST SP 800-53 | AC: Access Control Family | Access management controls |
| COBIT 2019 | DSS05: Manage Security Services | Access security services |
| CSA CCM v4.1 | IAM-01 through IAM-14: Identity and Access Management | Cloud IAM controls |
| NIST SP 800-207 | Zero Trust Architecture | Least privilege and continuous authorization |

---

**End of Document**
