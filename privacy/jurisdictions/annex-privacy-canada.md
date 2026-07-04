# Canada Privacy Regulatory Requirements

**Document Title:** Canada Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.0\
**Date:** 2026-07-04\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/annex-privacy-jurisdiction-index.md`](../annex-privacy-jurisdiction-index.md), [`privacy/policy-privacy-and-data-governance.md`](../policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/jurisdictions/annex-privacy-canada.md`](annex-privacy-canada.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex defines privacy and AI regulatory requirements applicable to processing of personal data in Canada under PIPEDA (current), the anticipated Consumer Privacy Protection Act and Artificial Intelligence and Data Act (Bill C-27), and Quebec Law 25. It supplements the Privacy and Data Governance Policy and the Privacy Impact and Cross-Border Transfer Procedure.

---

## Applicable laws and regulatory authorities

- **Personal Information Protection and Electronic Documents Act (PIPEDA)**: S.C. 2000, c. 5. Federal private-sector privacy law governing collection, use, and disclosure of personal information in commercial activity. Schedule 1 incorporates the CSA Model Code as fair information principles.
- **Consumer Privacy Protection Act (CPPA)**: Was Part 1 of Bill C-27 (Digital Charter Implementation Act, 2022), intended to replace PIPEDA. Bill C-27 lapsed when the Canadian Parliament was prorogued on 2025-01-06; the bill died on the order paper. CPPA is not in force and would require reintroduction in a future Parliament. PIPEDA remains the federal private-sector privacy law. Adopting entities should monitor for any reintroduction; the proposed CPPA framework included stronger consent requirements, rights to portability and disposal, privacy management programmes, and an independent Privacy Commissioner with order-making and penalty powers.
- **Artificial Intelligence and Data Act (AIDA)**: Was Part 3 of Bill C-27. AIDA also lapsed with Bill C-27 at the January 2025 prorogation and would require reintroduction. The proposed framework would have regulated high-impact AI systems, requiring impact assessments, mitigation measures, transparency, and mandatory harm reporting.
- **Quebec Law 25**: Significantly amended Quebec's provincial privacy laws. Key provisions: mandatory PIAs for projects involving personal information; express consent for sensitive data; right to portability; right to be de-indexed; obligations for automated decision-making transparency; prompt notification to the Commission d'accès à l'information (CAI) of a confidentiality incident presenting a risk of serious injury (the Act's standard is "promptly"; it sets no fixed hour-count). Extraterritorial application to organizations processing information about Quebec residents.
- **Regulatory authorities:** Office of the Privacy Commissioner of Canada (OPC) under PIPEDA; Privacy Commissioner with order-making powers under anticipated CPPA; Commission d'accès à l'information (CAI) for Quebec Law 25.

---

## AI and privacy obligations

### Under PIPEDA (current)

- **Consent:** Meaningful consent required for collection, use, or disclosure. Implied consent for non-sensitive; express consent for sensitive information.
- **Automated decision-making:** PIPEDA has no explicit equivalent to GDPR Article 22. The OPC has issued guidance that individuals should be informed when significant decisions are made using automated systems and that human review should be available.
- **Accountability:** Organizations must designate an individual responsible for compliance, develop privacy policies and procedures, and respond to individual complaints.

### Under CPPA (anticipated)

- **Algorithmic transparency (s. 63 CPPA):** Individuals would have the right to request explanation of predictions, recommendations, or decisions by automated decision systems that significantly affect them, and to challenge those decisions.
- **Sensitive personal information:** Enhanced consent requirements.
- **Children's privacy:** Specific protections for minors.
- **De-identification:** Permitted for internal research and AI training without consent, subject to de-identification requirements and prohibitions on re-identification.

### Under AIDA (anticipated)

- **High-impact AI systems:** Defined by regulation; expected to include AI in employment, credit, healthcare, and law enforcement contexts.
- **Impact assessments:** Mandatory before deployment.
- **Mitigation measures:** Documentation of harm and bias mitigation.
- **Transparency:** Public disclosure that a high-impact AI system is in use.
- **Audits:** The AI and Data Commissioner would have audit powers.

### Under quebec law 25

- **Privacy Impact Assessments (PIAs):** Required for any project involving personal information before implementation.
- **Automated decisions:** Organizations must inform individuals before or at the time of automated decisions and provide the right to request human review.
- **Biometric data:** Organizations creating a biometric database must notify the CAI at least 60 days in advance.

---

## Operational requirements (PIPEDA)

- **Breach of security safeguards (s. 10.1):** An organization must report to the OPC any breach of security safeguards involving personal information under its control where it is reasonable in the circumstances to believe the breach creates a real risk of significant harm to an individual, and must notify affected individuals. Both the report and the notification are due as soon as feasible after the organization determines the breach has occurred; PIPEDA sets no fixed hour-count, and Quebec Law 25's CAI notification (above) is likewise a promptness standard rather than a fixed clock.
- **Access-request response clock (s. 8(3)):** An organization must respond to a written request for access to personal information not later than thirty days after receipt of the request. PIPEDA permits a time-limit extension in defined circumstances with notice to the requester; adopting organizations should treat thirty days as the default service level in their DSR procedure.

---

## Cross-border transfer mechanisms

### Under PIPEDA

- PIPEDA does not prohibit cross-border transfers but requires comparable protection for personal information transferred to third parties including foreign affiliates. Contractual provisions are used to achieve this.
- The OPC recommends assessing recipient jurisdiction laws and disclosing to individuals that their information may be accessible to foreign authorities.

### Under quebec law 25

- Transfers outside Quebec require a Privacy Impact Assessment.
- Transfers may proceed only if the receiving jurisdiction offers adequate protection or the organization takes steps to mitigate risks.
- Privacy policy must disclose that personal information may be communicated outside Quebec.

### Adequacy

- Canada (private-sector organizations subject to PIPEDA) benefits from an EU adequacy decision.
- Bill C-27/CPPA would introduce updated transfer mechanisms more closely aligned with GDPR-style adequacy and contractual mechanisms.

---

## Enforcement and fines

### PIPEDA (current)

- The OPC can investigate and issue findings but has no order-making or fine-imposing powers under PIPEDA. The OPC may make recommendations and bring matters to the Federal Court.

### CPPA (anticipated)

- Administrative monetary penalties: Up to CAD 10 million or 3% of global revenue for general violations; up to CAD 25 million or 5% of global revenue for the most serious violations.
- Privacy Commissioner would have order-making powers.

### Quebec law 25

- CAI administrative penalties: up to CAD 10 million or 2% of worldwide turnover (less serious); up to CAD 25 million or 4% of worldwide turnover (more serious).
- Penal fines: CAD 15,000 to 25,000,000 for organizations.

### AIDA (anticipated)

- Penalties up to CAD 10 million or 3% of global revenues (general); up to CAD 25 million or 5% (most serious violations).
- Criminal penalties for intentional violations causing harm.

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
