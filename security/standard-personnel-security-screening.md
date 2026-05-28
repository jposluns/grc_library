# Personnel Security Screening Standard

**Document Title:** Personnel Security Screening Standard 
**Document Type:** Standard 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/policy-identity-and-access-management.md`](policy-identity-and-access-management.md), [`security/standard-privileged-access-management.md`](standard-privileged-access-management.md), [`security/procedure-security-incident-response.md`](procedure-security-incident-response.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md) 
**Classification:** Public 
**Category:** Information Security 
**Review Frequency:** Annual and upon material threat, framework, or regulatory change 
**Repository Path:** [`security/standard-personnel-security-screening.md`](standard-personnel-security-screening.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This standard defines the organization's minimum requirements for personnel security screening. It governs pre-employment background verification for all employees and contractors, with heightened requirements for roles with access to sensitive systems, data, or privileged accounts.

A prior security incident in which a previously active account belonging to a departed individual was exploited underscores the critical importance of sound identity lifecycle controls. Personnel screening is the first preventive layer; it must be paired with rigorous onboarding and offboarding procedures to ensure that access rights accurately reflect current employment status throughout the personnel lifecycle.

This standard supports the Identity and Access Management Policy, the Information Security Policy, and personnel security requirements under CTPAT Minimum Security Criteria and the Canada Partners in Protection (PIP) programme.

---

## Scope

1. Applies to all new hires, contractors, and consultants prior to onboarding.
2. Applies to existing personnel when promoted or reassigned into security-sensitive roles.
3. Does not apply to existing employees in their current role unless re-screening is triggered by a role change or a specific risk event.

---

## Governance and accountability

| Role | Responsibility |
| --- | --- |
| **Human Resources** | Initiates and manages the screening process; maintains screening records; notifies the Hiring Manager and CISO of any adverse findings. |
| **Chief Information Security Officer (CISO)** | Defines screening requirements for security-sensitive roles; reviews adverse findings for roles with privileged access. |
| **Hiring Manager** | Confirms role classification and security sensitivity before hire; approves any conditional onboarding pending screening completion. |
| **Legal Counsel** | Advises on applicable privacy law constraints on background check scope by jurisdiction. |

---

## Screening requirements by role tier

All personnel must be screened to the tier corresponding to their role classification. Where a role spans multiple tiers, the higher tier applies.

| Role Tier | Examples | Required Screening Elements |
| --- | --- | --- |
| **Tier 1: Standard** | All employees and contractors with system access | Identity verification; employment history confirmation; right-to-work verification |
| **Tier 2: Elevated** | Finance, HR, payroll, legal, procurement | All Tier 1 requirements; criminal record check (where permitted by jurisdiction); reference checks (minimum 2) |
| **Tier 3: Privileged** | IT Operations, system administrators, developers with production access, security personnel | All Tier 2 requirements; enhanced reference checks; verification of relevant qualifications or certifications where claimed |
| **Tier 4: Executive / High-Trust** | CxO, ELT, roles with board or audit committee access | All Tier 3 requirements; media and regulatory screening where applicable and permitted |

---

## Jurisdiction constraints

Background check scope varies by jurisdiction. Criminal record checks and certain credit-related checks are subject to provincial privacy legislation (Quebec Law 25, Ontario privacy equivalents), US state-level restrictions, and applicable local law in Latin American and European locations. Legal Counsel must confirm the permitted scope for each jurisdiction before screening is conducted. Screening must not exceed what is authorized by applicable law. Where legal constraints prohibit a required screening element, Human Resources must document the limitation and notify the CISO before onboarding proceeds.

---

## Screening timing

1. Screening must be initiated before an offer of employment is finalized.
2. Screening must be substantially complete before the individual is granted access to company systems.
3. Conditional access pending screening completion requires written CISO approval and must be documented with a defined completion deadline.
4. Access is not granted until the minimum Tier 1 requirements are verified.

---

## Adverse findings

1. Adverse findings are reviewed by Human Resources and the relevant Hiring Manager.
2. For Tier 3 and Tier 4 roles, the CISO is notified of any adverse finding related to fraud, computer crime, or breach of trust.
3. Human Resources manages the decision on offer withdrawal or role reassignment in consultation with Legal Counsel.
4. Adverse finding decisions and the rationale for each outcome are documented and retained in accordance with the Records Retention and Destruction Standard.
5. Adverse findings do not automatically disqualify a candidate; decisions must be proportionate to the nature of the finding and the sensitivity of the role.

---

## Contractor and third-party screening

1. Contractors and third-party personnel must provide evidence of background screening conducted by their employer or agency before being granted access to the organization's systems or facilities.
2. Where a third-party employer cannot confirm that screening has been conducted, the organization may:
 a. Conduct its own screening at the contractor's expense; or
 b. Restrict the contractor to lower-risk system access with appropriate technical controls applied.
3. Third-party screening requirements are included in supplier contracts per the Third-Party Risk Standard.
4. Spot-check audits of contractor screening compliance are conducted annually by Human Resources in coordination with the CISO.

---

## Records retention

Screening records, adverse finding decisions, and conditional access approvals are retained in accordance with the Records Retention and Destruction Standard. Minimum retention is five years from the date of the screening outcome.

---

## Framework alignment

| Requirement Area | ISO/IEC 27001:2022 | NIST SP 800-53 | CSA CCM v4.1 | CTPAT / PIP / BASC |
| --- | --- | --- | --- | --- |
| Pre-employment screening | A.6.1 | PS-3 | HRS-01, HRS-02 | CTPAT Personnel Security; Canada PIP: Personnel and Staffing; BASC v6 §8.3 |
| Contractor screening | A.6.6 | PS-7 | HRS-06 | CTPAT Personnel Security |
| Role-based access consideration | A.5.15 | AC-2 | IAM-02 | N/A |
| Records and accountability | A.5.33 | PS-3(1) | HRS-04 | N/A |

---

**End of Document**
