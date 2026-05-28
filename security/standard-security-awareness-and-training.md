# Security Awareness and Training Standard

**Document Title:** Security Awareness and Training Standard 
**Document Type:** Standard 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/standard-privileged-access-management.md`](standard-privileged-access-management.md) 
**Classification:** Public 
**Category:** Information Security 
**Review Frequency:** Annual and upon material threat, framework, or regulatory change 
**Repository Path:** [`security/standard-security-awareness-and-training.md`](standard-security-awareness-and-training.md) 
**Confidentiality:** Public 
**Licence:** CC0 1.0 Universal 

This standard defines the requirements for a security awareness and training programme. It establishes minimum training obligations, content requirements, delivery frequency, completion tracking, and role-based training requirements for personnel with elevated security responsibilities.

---

## Purpose

To ensure that all personnel understand their security obligations, can recognize common attack vectors, and know how to respond. Supports the Information Security Policy and applicable human capital governance.

---

## Scope

1. Applies to all employees, contractors, and third-party personnel with access to company systems or data.
2. Covers general security awareness, role-based supplemental training, and mandatory regulatory and compliance training.
3. Applies across all locations and remote work arrangements.

---

## Governance and Accountability

| Role | Responsibility |
| --- | --- |
| CISO | Owns the security awareness programme; approves training content and annual curriculum. |
| Human Resources | Ensures that training completion is tracked in the HR management system; integrates security training into onboarding; reports non-completion to CISO. |
| IT Operations | Delivers platform-based training (LMS or equivalent); manages phishing simulation campaigns. |
| Managers | Ensure that their direct reports complete mandatory training within required timelines. |
| Internal Audit | Verifies training completion rates and programme effectiveness annually. |

---

## Mandatory Training Requirements

### All Personnel

| Training Module | Frequency | Completion Deadline |
| --- | --- | --- |
| Security awareness fundamentals (phishing, social engineering, password hygiene, data handling) | Annual | Within 30 days of hire; annually thereafter |
| Acceptable Use Policy acknowledgement | Annual | First day of employment; annually thereafter |
| Privacy and data protection basics (applicable legislation, personal data handling) | Annual | Within 30 days of hire; annually thereafter |
| Incident reporting (how to recognize and report a suspected security incident) | Annual | Within 30 days of hire; annually thereafter |

### Role-Based Supplemental Training

| Role | Additional Training Required | Frequency |
| --- | --- | --- |
| IT Operations / Security personnel | Advanced threat awareness; incident response; secure configuration | Annual + as tooling changes |
| Developers and DevOps | Secure development practices (aligned to Developer Security Requirements Standard) | Annual |
| Finance and payroll | Business email compromise (BEC) and payment fraud awareness | Annual |
| Privileged account holders | PAM and identity hygiene training | Annual or upon privilege grant |
| Executive and ELT | Executive-level social engineering and phishing awareness | Annual |

---

## Collaboration Platform Social Engineering Awareness

All employees must complete awareness training on collaboration platform-based social engineering attacks. This module covers: how attackers use external or spoofed tenant invitations; indicators of impersonation; the correct procedure for verifying IT requests; and how to report a suspicious interaction. This module is mandatory for all personnel and is included in the annual curriculum.

---

## Phishing Simulations

IT Operations conducts simulated phishing campaigns at minimum quarterly. Results are reported to the CISO and used to identify training gaps. Employees who repeatedly fail simulations are required to complete targeted remediation training within 10 business days. Simulation results are not used for disciplinary purposes unless repeated failure follows remediation training.

---

## Training Completion Tracking

Training completion is tracked in the Learning Management System (LMS) or equivalent. HR reports monthly completion rates to the CISO. Completion rates below 90% by the required deadline are escalated to the relevant manager. Non-completion beyond 30 days past deadline is treated as a policy violation and escalated to the CISO and HR for disciplinary consideration per the Security Disciplinary Process.

---

## Programme Effectiveness

The CISO reviews programme effectiveness annually using: training completion rates; phishing simulation click rates and trends; volume and quality of employee-reported incidents; and post-incident analysis where human behaviour was a contributing factor. Results are incorporated into the annual GRC programme review and reported to the Enterprise Risk Committee.

---

## Framework Alignment

| Control | ISO/IEC 27001 | NIST SP 800-53 | CSA CCM v5 | Trade Compliance |
| --- | --- | --- | --- | --- |
| Security awareness | A.6.3 | AT-2 | HRS-06 | CTPAT, Canada PIP |
| Role-based training | A.6.3 | AT-3 | HRS-07 | BASC v6 §7.2 |
| Training governance | Clause 7.2 | AT-1 | N/A |: |



**End of Document**
