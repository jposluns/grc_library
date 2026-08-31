# Canada Privacy Regulatory Requirements

**Document Title:** Canada Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.20\
**Date:** 2026-08-31\
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

This annex defines privacy and AI regulatory requirements applicable to processing of personal data in Canada under PIPEDA (current), the lapsed Consumer Privacy Protection Act and Artificial Intelligence and Data Act (Bill C-27, which died on the 2025-01-06 prorogation; a privacy successor, Bill C-36 (Protecting Privacy and Consumer Data Act), was introduced 2026-06-15 and is proposed, not in force; see below), and Quebec Law 25. It supplements the Privacy and Data Governance Policy and the Privacy Impact and Cross-Border Transfer Procedure.

---

## Applicable laws and regulatory authorities

- **Personal Information Protection and Electronic Documents Act (PIPEDA)**: S.C. 2000, c. 5. Federal private-sector privacy law governing personal information that an organization collects, uses, or discloses in the course of commercial activities, or that is about an employee or applicant of the organization and is handled in connection with the operation of a federal work, undertaking, or business (s. 4(1)). Schedule 1 incorporates the CSA Model Code as fair information principles.
- **Consumer Privacy Protection Act (CPPA)**: Was Part 1 of Bill C-27 (Digital Charter Implementation Act, 2022), intended to replace PIPEDA. Bill C-27 lapsed when the Canadian Parliament was prorogued on 2025-01-06; the bill died on the order paper. CPPA is not in force; the C-27 bill itself was not reintroduced, but a distinct successor privacy bill has since been introduced. PIPEDA remains the federal private-sector privacy law. That successor, **Bill C-36 (Protecting Privacy and Consumer Data Act, PPCDA)**, was introduced 2026-06-15 and is at second reading (proposed, not in force); it would repeal Part 1 of PIPEDA, rename PIPEDA to the *Electronic Documents Act*, shift toward a legitimate-interest model, and create a Privacy and Consumer Data Commissioner. C-36 is a privacy bill and does not reintroduce AIDA. The earlier proposed CPPA framework included stronger consent requirements, rights to portability and disposal, privacy management programmes, and an independent Privacy Commissioner with order-making powers, with penalties to be imposed by the proposed Personal Information and Data Protection Tribunal on the Commissioner's recommendation.
- **Artificial Intelligence and Data Act (AIDA)**: Was Part 3 of Bill C-27. AIDA also lapsed with Bill C-27 at the January 2025 prorogation and, per the June 2025 ministerial statement, will not return in its original form. The proposed framework would have regulated high-impact AI systems, requiring an assessment of whether a system was high-impact, risk mitigation measures, transparency, and mandatory harm reporting.
- **Quebec Law 25**: Significantly amended Quebec's provincial privacy laws. Key provisions: mandatory PIAs for projects to acquire, develop, or overhaul an information system or electronic service delivery system involving personal information (s. 3.3); express consent for sensitive data; right to portability; conditional right to de-indexing (s. 28.1, for dissemination that contravenes the law or a court order, or that causes serious reputational or privacy injury, subject to the balancing conditions the section sets out); obligations for automated decision-making transparency; prompt notification to the Commission d'accès à l'information (CAI) of a confidentiality incident presenting a risk of serious injury (the Act's standard is "promptly"; it sets no fixed hour-count). Its scope is framed by the carrying-on of an enterprise (s. 1, per article 1525 of the Civil Code of Quebec) rather than an express extraterritoriality provision.
- **Privacy Act**: R.S.C. 1985, c. P-21. Federal PUBLIC-sector privacy law governing personal information held by federal government institutions (distinct from PIPEDA, which governs the private sector). Administered by the Office of the Privacy Commissioner of Canada.
- **British Columbia Personal Information Protection Act (PIPA)**: S.B.C. 2003, c. 63. Provincial private-sector privacy law for organizations in British Columbia, recognized as substantially similar to PIPEDA (so PIPEDA generally does not apply where a provincially regulated private-sector organization collects, uses, or discloses personal information within BC; federal works, undertakings, and businesses remain under PIPEDA, per BC PIPA s. 3(2)(c)). Alberta's PIPA (S.A. 2003, c. P-6.5) is the parallel Alberta statute.
- **Ontario Personal Health Information Protection Act, 2004 (PHIPA)**: S.O. 2004, c. 3, Sch. A. Ontario health-sector privacy law governing health-information custodians, recognized as substantially similar to PIPEDA for personal health information.
- **Regulatory authorities:** Office of the Privacy Commissioner of Canada (OPC) under PIPEDA; the order-making Privacy Commissioner that the lapsed CPPA proposed (not in force); Commission d'accès à l'information (CAI) for Quebec Law 25.

---

## Bill C-36 (Protecting Privacy and Consumer Data Act, PPCDA): the proposed framework in detail

The following summarizes the PPCDA as introduced (Bill C-36, first reading 2026-06-15; at second reading; PROPOSED and NOT in force, with commencement by order in council under s. 147). It is provided so an adopter can anticipate the direction of Canadian federal private-sector privacy law. Until the bill is enacted and in force, PIPEDA governs; the adopter confirms the bill's status and final text upstream before relying on any provision below.

- **Scope and appropriateness (ss. 5, 6, 12).** The PPCDA recognizes privacy as a fundamental right (s. 5) and binds organizations that collect, use, or disclose personal information in the course of commercial activities, plus employee and applicant data handled in connection with a federal work, undertaking, or business (s. 6(1)). An independent appropriateness constraint (s. 12) requires that processing be for purposes a reasonable person would consider appropriate, whether or not consent is required. The Act does not apply to Privacy Act government institutions, or to information collected, used, or disclosed solely for personal or domestic, journalistic, artistic, or literary, or employment-communication purposes, or by a provincially exempt organization for intraprovincial processing (s. 6(4)); anonymized information is outside the Act entirely (s. 6(5)).
- **Consent and the legitimate-interest basis (ss. 15, 17, 18).** Valid, generally express, consent in plain language is the default (s. 15); an individual may withdraw consent on reasonable notice, and the organization ceases the affected processing as soon as feasible (s. 17). The headline shift is s. 18(3): an organization may collect, use, or disclose personal information without the individual's knowledge or consent where it has "a legitimate interest that outweighs any reasonably foreseeable adverse effect on the individual", provided a reasonable person would expect it and it is not to influence the individual's behaviour or decisions. Before relying on it, the organization must identify and describe the legitimate interest, conduct a privacy impact assessment, and mitigate adverse effects (s. 18(4)), and keep a record of the description and assessment available to the Commission (s. 18(5)).
- **Individual rights (ss. 54, 63, 67, 71, 72).** Disposal on written request as soon as feasible, subject to listed exceptions (s. 54); access to whether, how, and to whom information is held and disclosed (s. 63), due within 30 days with defined extensions (s. 67); for a legally or similarly significant automated prediction, recommendation, or decision, an explanation on request including the type and source of data and the principal factors, with a right to make written representations to a reviewing employee (s. 63(4) to (6)); correction of inaccurate, out-of-date, or incomplete information (s. 71); and data mobility to a designated organization where both are subject to a prescribed framework (s. 72).
- **Organization obligations (ss. 7 to 9, 11, 52 to 57, 58 to 61).** Accountability for information under the organization's control with a designated responsible individual (ss. 7, 8); a privacy management program proportionate to volume and sensitivity (s. 9); equivalent protection by service providers (s. 11); retention no longer than necessary with disposal as soon as feasible (ss. 52 to 54); physical, organizational, and technological safeguards proportionate to sensitivity (s. 56); a prescribed privacy impact assessment before an international disclosure or transfer (s. 57); and breach reporting and individual notification where there is a "real risk of significant harm", due as soon as feasible, with a record of every breach (ss. 58 to 61).
- **The Privacy and Consumer Data Commissioner and Division (ss. 85, 89, 97 to 129).** A Commissioner is designated from the Commission (s. 85) and heads a Privacy and Consumer Data Division (s. 89), whose role includes dispute resolution (s. 101). The Commissioner receives and investigates complaints (ss. 97 to 108) and may audit on reasonable grounds, with powers to compel evidence and examine records (ss. 118, 122). Compliance orders are made by the Commission after review (s. 110) and are enforceable in the Federal Court (s. 129); the Commissioner is structurally separated from review and interim-order proceedings (ss. 111(2), 124(2)).
- **Penalties and offences (ss. 113, 114, 132, 145).** Administrative monetary penalties are available for listed contraventions (s. 113), capped for all contraventions from any one investigation at the greater of $10,000,000 and 3 percent of the organization's gross global revenue in the preceding financial year (s. 114). An organization that knowingly contravenes certain enumerated provisions, or that obstructs the Commissioner or their delegate in a complaint investigation or audit, or the Commission or their delegate in specified proceedings, is liable to a fine up to the greater of $25,000,000 and 5 percent of gross global revenue on indictment, or $20,000,000 and 4 percent on summary conviction (s. 145). A conditioned private right of action for loss or injury is available after specified enforcement findings or a s. 145 conviction (s. 132).
- **Effect on PIPEDA.** The bill repeals Part 1 of PIPEDA and changes the short title of the remaining Act to the "Electronic Documents Act" (Bill C-36, Part 2, per the enacting summary). The PPCDA is a privacy statute; it does not reintroduce AIDA and contains no AI-specific licensing regime.

## AI and privacy obligations

### Under PIPEDA (current)

- **Consent:** Meaningful consent required for collection, use, or disclosure. The form of consent may vary with the circumstances and sensitivity of the information; an organization should generally seek express consent for information likely to be sensitive, and implied consent is generally appropriate for less-sensitive information (PIPEDA Schedule 1, Principle 4.3).
- **Automated decision-making:** PIPEDA has no explicit equivalent to GDPR Article 22. The OPC has issued guidance that individuals should be informed when significant decisions are made using automated systems and that human review should be available.
- **Accountability:** Organizations must designate an individual responsible for compliance, develop privacy policies and procedures, and respond to individual complaints.

### Under the CPPA (lapsed; proposed, not in force)

- **Algorithmic transparency (proposed CPPA s. 63):** Where an automated decision system made a prediction, recommendation, or decision that could have a significant impact on an individual, the individual would have been able to request an explanation, which would have indicated the type and source of personal information used and the reasons or principal factors that led to the result.
- **Sensitive personal information:** Enhanced consent requirements would have applied.
- **Children's privacy:** Specific protections for minors would have applied.
- **De-identification (proposed CPPA s. 21):** Would have permitted use for internal research, analysis, and development without consent, subject to de-identification requirements and prohibitions on re-identification.

### Under the AIDA (lapsed; proposed, not in force)

- **High-impact AI systems:** Would have been those meeting criteria established in regulations; the bill text did not prescribe a list of sectors.
- **High-impact assessment (proposed AIDA s. 7):** A person responsible for an AI system would have had to assess, in accordance with the regulations, whether it was a high-impact system.
- **Mitigation measures (proposed AIDA s. 8):** Would have required a person responsible for a high-impact system to establish, in accordance with the regulations, measures to identify, assess, and mitigate the risks of harm or biased output that could result from the use of the system.
- **Transparency (proposed AIDA s. 11):** Would have required a published plain-language description of a high-impact system, including its intended use and the mitigation measures established for it.
- **Audits (proposed AIDA s. 15):** If the Minister had reasonable grounds to believe a person had contravened proposed ss. 6 to 12 or a related order, the Minister would have been able to order the person to conduct an audit or to engage an independent auditor. The Minister could designate an Artificial Intelligence and Data Commissioner to assist, and could delegate functions to the Commissioner other than regulation-making (s. 33).

### Under Quebec Law 25

- **Privacy Impact Assessments (PIAs):** Required (Quebec Law 25 s. 3.3) for any project to acquire, develop, or overhaul an information system or electronic service delivery system involving the collection, use, communication, keeping, or destruction of personal information, before implementation. A separate PIA is required before communicating personal information outside Quebec (s. 17).
- **Automated decisions (s. 12.1):** For a decision based exclusively on automated processing of personal information, organizations must inform the individual of that basis no later than the time the individual is informed of the decision, and, at the individual's request, of the personal information used, the reasons and the principal factors and parameters, and the right to correction; the individual must be given the opportunity to submit observations to a member of the enterprise's personnel who is in a position to review the decision.
- **Biometric data:** Organizations creating a biometric database must notify the CAI at least 60 days in advance.

---

## Operational requirements (PIPEDA)

- **Breach of security safeguards (s. 10.1):** An organization must report to the OPC any breach of security safeguards involving personal information under its control where it is reasonable in the circumstances to believe the breach creates a real risk of significant harm to an individual, and must notify affected individuals. Both the report and the notification are due as soon as feasible after the organization determines the breach has occurred; PIPEDA sets no fixed hour-count, and Quebec Law 25's CAI notification (above) is likewise a promptness standard rather than a fixed clock. The Breach of Security Safeguards Regulations (SOR/2018-64), in force 1 November 2018, prescribe the content of the OPC report and the individual notification, and require the organization to maintain a record of every breach of security safeguards, whether or not it met the real-risk-of-significant-harm reporting threshold, for 24 months after the day the organization determines the breach occurred. (SOR/2018-64 was verified against the consolidated Justice Laws text on 2026-07-13: in force since its 2018-11-01 coming-into-force, with no subsequent amendment.)
- **Access-request response clock (s. 8(3)):** An organization must respond to a written request for access to personal information not later than thirty days after receipt of the request. PIPEDA permits a time-limit extension in defined circumstances with notice to the requester; adopting organizations should treat thirty days as the default service level in their DSR procedure.

---

## Cross-border transfer mechanisms

### Under PIPEDA

- PIPEDA does not prohibit cross-border transfers but requires comparable protection for personal information transferred to third parties including foreign affiliates. Contractual provisions are used to achieve this.
- The OPC recommends assessing recipient jurisdiction laws and disclosing to individuals that their information may be accessible to foreign authorities.

### Under Quebec Law 25

- A transfer outside Quebec may proceed only where a privacy impact assessment establishes that the information would receive adequate protection (s. 17); the transfer must then be the subject of a written agreement that takes the assessment into account and, where applicable, the measures agreed to mitigate the risks identified. Mitigation forms part of that agreement rather than an alternative to the adequate-protection conclusion. Section 17 does not apply to a communication under s. 18, first paragraph, subparagraph 7.
- At collection and on request, the individual must be informed of the possibility that their personal information could be communicated outside Quebec (s. 8).

### Adequacy

- Canada (private-sector organizations subject to PIPEDA) benefits from an EU adequacy decision.
- Bill C-27's proposed CPPA would have required an organization transferring personal information to a service provider to ensure that the service provider, by contract or otherwise, provided a level of protection equivalent to that required of the organization (s. 11); it did not establish an adequacy-decision mechanism. Bill C-27 lapsed at the 2025-01-06 prorogation and is not in force; PIPEDA's existing mechanisms remain.

---

## Enforcement and fines

### PIPEDA (current)

- The OPC can investigate and issue findings but has no order-making or fine-imposing powers under PIPEDA. The OPC may make recommendations and bring matters to the Federal Court.

### CPPA (lapsed; proposed penalties, not in force)

- Administrative monetary penalty (proposed CPPA s. 95(4)): on the Commissioner's recommendation (s. 94), the Personal Information and Data Protection Tribunal could have imposed a penalty; the maximum for all contraventions in a recommendation taken together would have been the greater of CAD 10 million and 3% of the organization's gross global revenue in the financial year before the one in which the penalty was imposed.
- Offences (proposed CPPA s. 128): for knowingly contravening specified provisions, or for obstructing the Commissioner or their delegate in an investigation, inquiry, or audit, an organization would have been liable on indictment to a fine up to the greater of CAD 25 million and 5% of gross global revenue, or on summary conviction up to the greater of CAD 20 million and 4%.
- The Privacy Commissioner would have had order-making powers.

### Quebec Law 25

- CAI administrative monetary penalty (s. 90.12): a single maximum of the greater of CAD 10 million or 2% of worldwide turnover for the preceding fiscal year; up to CAD 50,000 for a natural person.
- Penal fines (s. 91): organizations CAD 15,000 to 25,000,000 or, if greater, 4% of worldwide turnover for the preceding fiscal year; natural persons CAD 5,000 to 100,000.

### AIDA (lapsed; proposed penalties, not in force)

- Administrative monetary penalties (proposed AIDA s. 29): a person found under the regulations to have committed a designated violation would have been liable to an administrative monetary penalty established by those regulations; the bill text itself set no AMP maximum.
- Offences (proposed AIDA): contravening proposed ss. 6 to 12, or obstructing the Minister or an auditor (s. 30), would have carried a corporate fine on indictment up to the greater of CAD 10 million and 3% of gross global revenues (summary conviction: the greater of CAD 5 million and 2%). Two further offences, possessing or using personal information while knowing or believing it was obtained through an offence, for the purpose of an AI system (s. 38), and making an AI system available in either of two circumstances: without lawful excuse, knowing or reckless as to whether its use was likely to cause serious physical or psychological harm to a person or substantial damage to their property, where its use then caused that harm or damage; or with intent to defraud the public and cause substantial economic loss to an individual, where its use then caused that loss (s. 39), would have carried, on their shared punishment provision (s. 40), a corporate fine on indictment up to the greater of CAD 25 million and 5% (summary conviction: the greater of CAD 20 million and 4%).

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
