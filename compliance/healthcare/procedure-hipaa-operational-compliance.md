# HIPAA Operational Compliance Procedure

**Document Title:** HIPAA Operational Compliance Procedure\
**Document Type:** Procedure\
**Version:** 0.0.1\
**Date:** 2026-07-09\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/healthcare/annex-healthcare-sector-requirements.md`](annex-healthcare-sector-requirements.md), [`compliance/healthcare/README.md`](README.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../policy-legal-and-regulatory-compliance.md), [`privacy/policy-privacy-and-data-governance.md`](../../privacy/policy-privacy-and-data-governance.md), [`privacy/procedure-data-subject-rights-management.md`](../../privacy/procedure-data-subject-rights-management.md), [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../../supply-chain/standard-supplier-security-and-privacy-assurance.md)\
**Classification:** Public\
**Category:** Compliance: Sector-Specific\
**Review Frequency:** Annual and upon material change to 45 CFR Part 164\
**Repository Path:** [`compliance/healthcare/procedure-hipaa-operational-compliance.md`](procedure-hipaa-operational-compliance.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure operationalizes the HIPAA obligations that a covered entity or business associate must execute on a clock: the HIPAA Privacy Rule individual-rights response timelines, the Notice of Privacy Practices and minimum-necessary duties, the cross-rule six-year documentation-retention requirement, the breach-determination test that decides whether the notification clock starts, and the business associate agreement content requirement. It translates the regulatory landscape mapped in the [Healthcare Sector GRC Requirements Annex](annex-healthcare-sector-requirements.md) into repeatable operational steps, so a compliance office can run its request-handling, records-retention, breach-response, and vendor-assurance programmes directly.

The governing text is 45 CFR Part 164 (the HIPAA Privacy, Security, and Breach Notification Rules). Section citations are given so each step traces to its authority; confirm the consolidated text against the current eCFR before relying on a specific paragraph, because Part 164 is amended from time to time.

---

## Scope

1. Applies to the organization when it acts as a HIPAA covered entity or as a business associate (including a subcontractor business associate) that creates, receives, maintains, or transmits protected health information (PHI) or electronic PHI (ePHI).
2. Covers the operational obligations that carry a statutory clock or a defined content requirement: individual right of access, amendment, and accounting of disclosures; the Notice of Privacy Practices; minimum necessary; documentation and retention; breach determination and notification; and business associate agreements.
3. Does not restate the Security Rule administrative, physical, and technical safeguards (mapped in the annex, Key regulatory requirements) or the country-regulator overlay structure; it is HIPAA operational depth, not a jurisdiction overlay.
4. Applies to the Chief Compliance Officer, the Data Protection Officer (privacy lead), Security Owners, business relationship owners, and Internal Audit, as set out below.

---

## Governance and accountability

| Role | Responsibility |
| --- | --- |
| **Chief Compliance Officer** | Owns this procedure and the HIPAA compliance programme; approves exceptions; receives the request-handling and breach-log reporting. |
| **Data Protection Officer** | Operates the individual-rights request handling (access, amendment, accounting), the Notice of Privacy Practices, and the minimum-necessary determinations; is the privacy lead for breach risk assessment. |
| **Security Owner** | Maintains the Security Rule safeguards the annex maps, and supports breach investigation for ePHI incidents. |
| **Business relationship owner** | Confirms a compliant business associate agreement is in place before PHI is shared with a vendor, and tracks subcontractor flow-down. |
| **Internal Audit** | Reviews retention-schedule adherence, request-clock performance, and breach-determination records at the review frequency. |

---

## 1. Individual right of access

1. On receipt of an individual's request for access to PHI in a designated record set, act on the request no later than **30 days** after receipt (45 CFR 164.524(b)(2)(i)).
2. Where the 30-day deadline cannot be met, take **one** extension of no more than **30 additional days**, and within the original 30 days give the individual a written statement of the reason for the delay and the date by which action will be completed. Only one extension is permitted (45 CFR 164.524(b)(2)(ii)).
3. Record the request, the response date, and any extension in the request log retained under section 6.

---

## 2. Amendment of protected health information

1. On receipt of a request to amend PHI in a designated record set, act on the request no later than **60 days** after receipt (45 CFR 164.526(b)(2)(i)).
2. Where the 60-day deadline cannot be met, take one extension of no more than 30 additional days, with a written statement of the reason and the completion date within the original 60 days.
3. On a denial, provide the individual the statement-of-disagreement process the rule requires, and record the outcome in the request log.

---

## 3. Accounting of disclosures

1. On receipt of a request for an accounting of disclosures, provide the accounting no later than **60 days** after receipt (45 CFR 164.528(c)(1)).
2. One 30-day extension is available on the same written-notice basis as sections 1 and 2.
3. Maintain the disclosure records needed to produce the accounting for the retention period in section 6.

---

## 4. Notice of Privacy Practices

1. Maintain a Notice of Privacy Practices that describes the uses and disclosures the organization may make and the individual's rights (45 CFR 164.520).
2. Make uses and disclosures of PHI consistent with the notice in effect (45 CFR 164.502(i)).
3. Retain each issued notice and any acknowledgments of receipt under the documentation duty in section 6 (45 CFR 164.530(j)).

---

## 5. Minimum necessary

1. When using, disclosing, or requesting PHI, limit it to the minimum necessary to accomplish the intended purpose, except for the uses and disclosures the rule excepts (for example, treatment) (45 CFR 164.502(b)).
2. Implement role-based access policies and the reasonable-reliance conditions that operationalize minimum necessary (45 CFR 164.514(d)).

---

## 6. Documentation and retention

1. Retain required HIPAA documentation for **six years** from the date of its creation or the date it was last in effect, whichever is later. This applies to the Security Rule policies, procedures, and required documentation (45 CFR 164.316(b)(2)(i)) and to the Privacy Rule documentation, including the items sections 1 to 4 generate (45 CFR 164.530(j)).
2. Keep the request log, breach-determination records, and business associate agreements within this schedule.
3. The six-year duty is independent of, and additional to, any longer retention a state law, a contract, or another regulation imposes.

---

## 7. Breach determination and notification

1. On discovery of an acquisition, access, use, or disclosure of PHI not permitted under the Privacy Rule, run the **breach-determination test**: the event is presumed to be a breach unless a risk assessment demonstrates a **low probability** that the PHI has been compromised, based on at least the four factors of 45 CFR 164.402: (i) the nature and extent of the PHI involved, including identifiers and the likelihood of re-identification; (ii) the unauthorized person who used the PHI or to whom the disclosure was made; (iii) whether the PHI was actually acquired or viewed; and (iv) the extent to which the risk to the PHI has been mitigated. PHI that was encrypted to the "unsecured PHI" safe-harbour standard is out of scope of the notification duty.
2. Where notification is required, notify affected individuals without unreasonable delay and no later than **60 calendar days** after discovery (45 CFR 164.404(b)); provide the media notice for a breach affecting more than 500 residents of a state or jurisdiction (45 CFR 164.406); and, where the organization is a business associate, notify the covered entity within the same 60-day limit (45 CFR 164.410).
3. For a breach affecting **500 or more** individuals, notify HHS contemporaneously with the individual notice; for breaches affecting **fewer than 500** individuals, maintain a log and notify HHS no later than 60 days after the end of the calendar year (45 CFR 164.408).
4. The organization bears the burden of demonstrating that required notifications were made or that the event did not constitute a breach (45 CFR 164.414(b)). Coordinate the investigation with the incident-response procedure.

---

## 8. Business associate agreements

1. Before PHI is created, received, maintained, or transmitted by a vendor on the organization's behalf, obtain satisfactory assurances through a written business associate agreement that meets the applicable requirements of 45 CFR 164.504(e) (Privacy Rule) and 45 CFR 164.314(a) (Security Rule), as required by 45 CFR 164.502(e).
2. Ensure that the agreement flows the equivalent requirements down to any subcontractor that creates, receives, maintains, or transmits PHI on the business associate's behalf (45 CFR 164.308(b) and 164.504(e)).
3. The business relationship owner confirms the agreement is executed before data sharing begins and retains it under section 6.

---

## Framework alignment

| Operational area | 45 CFR Part 164 | ISO/IEC 27001:2022 | NIST reference |
| --- | --- | --- | --- |
| Individual rights (access, amendment, accounting) | 164.524, 164.526, 164.528 | A.5.34 | SP 800-66r2 |
| Notice and minimum necessary | 164.520, 164.502, 164.514 | A.5.34 | SP 800-66r2 |
| Documentation and retention | 164.316(b)(2), 164.530(j) | A.5.33 | SP 800-66r2 |
| Breach determination and notification | 164.402, 164.404, 164.406, 164.408, 164.410, 164.414 | A.5.26 | SP 800-66r2 |
| Business associate agreements | 164.502(e), 164.504(e), 164.314(a) | A.5.20 | SP 800-66r2 |

NIST SP 800-66r2 (Implementing the HIPAA Security Rule) is the HHS-referenced implementation guide for the Security Rule safeguards this procedure depends on; consult it for risk-analysis and safeguard-implementation detail.

---

**End of Document**
