# India Privacy Regulatory Requirements

**Document Title:** India Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.6\
**Date:** 2026-08-15\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/annex-privacy-jurisdiction-index.md`](../annex-privacy-jurisdiction-index.md), [`privacy/policy-privacy-and-data-governance.md`](../policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/jurisdictions/annex-privacy-india.md`](annex-privacy-india.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex defines privacy and AI regulatory requirements applicable to the processing of personal data in India under the Digital Personal Data Protection Act 2023 (DPDPA) and the Digital Personal Data Protection Rules 2025. It supplements the Privacy and Data Governance Policy and the Privacy Impact and Cross-Border Transfer Procedure.

---

## Applicable laws and regulatory authorities

- **Digital Personal Data Protection Act 2023 (DPDPA)**: Enacted by the Parliament of India on 2023-08-11. India's first comprehensive data protection law.
- **Digital Personal Data Protection Rules 2025**: Draft published by the Ministry of Electronics and Information Technology (MeitY) in January 2025 for public consultation; final Rules notified by MeitY on 13 November 2025. The Rules operationalize the principal Act through a **phased commencement**: provisions establishing the Data Protection Board took immediate effect on notification; provisions governing the registration and functioning of consent managers commence 12 months after notification (approximately November 2026); the remainder of the Rules commence 18 months after notification (approximately May 2027). Adopting organizations should plan compliance programmes against the staged timeline rather than treat all obligations as effective on a single date.
- Scope: applies to the processing of digital personal data within the territory of India where the data is collected in digital form, or in non-digital form and later digitized (s. 3(a)); it also applies to processing outside India where that processing is in connection with an activity related to offering goods or services to Data Principals within the territory of India (s. 3(b)). It does not apply to personal data processed by an individual for a personal or domestic purpose, or to personal data made or caused to be made publicly available by the Data Principal, or by another person under an obligation under any law in force in India to make it public (s. 3(c)).
- **Key concepts:** Data Principals (data subjects); Data Fiduciaries (data controllers); Consent Managers (entities registered with the Data Protection Board that manage consent on behalf of Data Principals); Significant Data Fiduciaries (SDFs): large-scale or high-risk data fiduciaries designated by the Indian government and subject to enhanced obligations.
- **Regulatory authority:** Data Protection Board of India (DPBI): an independent adjudicatory body that receives complaints and imposes financial penalties.

---

## AI and privacy obligations

- **Consent:** Most processing of personal data requires consent that is free, specific, informed, unconditional, and unambiguous, given through a clear affirmative action, and limited to the personal data necessary for the specified purpose (s. 6(1)). A consent request must be in clear, plain language, with the option to access it in English or any language specified in the Eighth Schedule to the Constitution (s. 6(3)). The Consent Manager framework provides a regulated intermediary structure.
- **Purpose limitation:** Personal data may be processed only for the specified lawful purpose for which consent was given. Repurposing for AI training requires fresh consent or another valid legal ground.
- **Children's data:** Data Fiduciaries must obtain verifiable consent from a parent or guardian before processing personal data of children (a child is an individual under 18 years; under s. 9(5) the Central Government may notify, for a verifiably-safe Data Fiduciary, an age above which these children's-data duties do not apply). Tracking, behavioural monitoring, and targeted advertising directed at children are prohibited (s. 9(3)), subject to exemptions the Central Government may prescribe under s. 9(4) and 9(5).
- **Significant Data Fiduciaries (SDF):** The Central Government may notify a Data Fiduciary or class as an SDF on an assessment of factors including the volume and sensitivity of personal data processed, risk to Data Principal rights, potential impact on the sovereignty and integrity of India, risk to electoral democracy, security of the State, and public order (s. 10(1)). SDFs are subject to: mandatory DPIAs; mandatory annual data audits by an independent data auditor; appointment of a Data Protection Officer; and additional accountability mechanisms. Large AI platforms processing personal data at scale are likely SDF candidates.
- **Data used in decisions (s. 8(3)):** Where personal data is likely to be used to make a decision that affects a Data Principal, or to be disclosed to another Data Fiduciary, the Data Fiduciary must maintain the completeness, accuracy, and consistency of that data. The DPDPA and the 2025 Rules do not grant a right to an explanation of, or to contest, automated decisions; any human-review or explanation practice is an organizational choice rather than a statutory right.
- **Transparency:** A notice accompanying or preceding a consent request must inform the Data Principal of the personal data and the purpose of processing, the manner of exercising the rights to withdraw consent (s. 6(4)) and grievance redressal (s. 13), and the manner of making a complaint to the Data Protection Board (s. 5(1)); the Data Principal must be able to access the notice in English or an Eighth Schedule language (s. 5(3)). The consent request itself must provide the contact details of a Data Protection Officer, where applicable, or of another person authorized by the Data Fiduciary to respond to communications from the Data Principal for the exercise of their rights under the Act (s. 6(3)).
- **Data retention:** Personal data must be erased once the purpose for which it was collected is fulfilled or consent is withdrawn, unless retention is required by law.

---

## Cross-border transfer mechanisms

- The DPDPA does **not** use an approved-destination whitelist. Under section 16(1), the Central Government may, by notification, **restrict** the transfer of personal data to a country or territory outside India (a negative-list power); transfers are otherwise permitted, subject to the requirements below.
- Under the DPDP Rules, 2025 (Rule 15), personal data may be transferred outside India subject to any requirements the Central Government specifies, by general or special order, in respect of making that data available to a foreign State, or to a person or entity under the control of, or any agency of, such a State.
- Section 16(2) preserves the application of any Indian law that provides a higher degree of protection for, or a stricter restriction on, the transfer of personal data (for example sector-specific data-localization rules).
- Practical note: monitor Central Government notifications for any restricted destinations and any specified transfer requirements, and apply any stricter sectoral localization rules that govern the data in question.
- Rule 13(4) of the 2025 Rules imposes a category-based localization restriction specific to Significant Data Fiduciaries: personal data that the Central Government specifies (on a committee's recommendation), together with the traffic data pertaining to its flow, must not be transferred outside the territory of India. This operates independently of the s. 16(1) destination-restriction power.

---

## Enforcement and fines

The Data Protection Board adjudicates complaints and, if on conclusion of an inquiry it determines that a breach is significant, may, after giving the person an opportunity of being heard, impose the applicable Schedule monetary penalty, having regard to the statutory factors in section 33(2) (including the breach's nature, gravity, duration, and repetitive character):

| Violation Category | Maximum Penalty |
|---|---|
| Failure to implement adequate security safeguards (personal data breach, s. 8(5)) | INR 250 crore (~USD 30 million) |
| Failure to give the Data Protection Board or affected Data Principals notice of a breach (s. 8(6)) | INR 200 crore (~USD 24 million) |
| Breach of children's data obligations (s. 9) | INR 200 crore (~USD 24 million) |
| Breach of Significant Data Fiduciary additional obligations (s. 10) | INR 150 crore (~USD 18 million) |
| Breach of a Data Principal's duties under section 15 | May extend to INR 10,000 |
| Breach of a term of a voluntary undertaking accepted by the Board (s. 32) | Up to the extent applicable to the underlying breach |
| Other violations of the DPDPA or its Rules | INR 50 crore (~USD 6 million) |

There are no criminal penalties under the DPDPA; enforcement is administrative through the DPBI.

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
