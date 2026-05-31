# India Privacy Regulatory Requirements

**Document Title:** India Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.0\
**Date:** 2026-05-31\
**Owner:** Chief Privacy Officer\
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
- **Digital Personal Data Protection Rules 2025**: Draft published by the Ministry of Electronics and Information Technology (MeitY) in January 2025 for public consultation; final Rules notified by MeitY on 13 November 2025. The Rules operationalize the principal Act through a **phased commencement**: provisions establishing the Data Protection Board took immediate effect on notification; provisions governing the registration and functioning of consent managers commence 12 months after notification (approximately November 2026); the remainder of the Rules commence 18 months after notification (approximately May 2027). Adopting organisations should plan compliance programmes against the staged timeline rather than treat all obligations as effective on a single date.
- Scope: applies to processing of digital personal data of individuals in India; also applies to processing outside India where data of Indian residents is processed for the purpose of offering goods or services to individuals in India.
- **Key concepts:** Data Principals (data subjects); Data Fiduciaries (data controllers); Consent Managers (accredited entities managing consent on behalf of Data Principals); Significant Data Fiduciaries (SDFs): large-scale or high-risk data fiduciaries designated by the Indian government and subject to enhanced obligations.
- **Regulatory authority:** Data Protection Board of India (DPBI): an independent adjudicatory body that receives complaints and imposes financial penalties.

---

## AI and privacy obligations

- **Consent:** Most processing of personal data requires free, specific, informed, and unambiguous consent. Consent requests must be in clear, plain language and in the language specified by the Data Principal. The Consent Manager framework provides a regulated intermediary structure.
- **Purpose limitation:** Personal data may be processed only for the specified lawful purpose for which consent was given. Repurposing for AI training requires fresh consent or another valid legal ground.
- **Children's data:** Data Fiduciaries must obtain verifiable consent from a parent or guardian before processing personal data of children (under 18 years; regulations may reduce this to 14 for certain services). Tracking, behavioural monitoring, and targeted advertising directed at children are prohibited without exception.
- **Significant Data Fiduciaries (SDF):** Entities designated based on volume of data processed, risk to Data Principal rights, potential national security implications, or societal impact. SDFs are subject to: mandatory DPIAs; mandatory annual data audits by accredited auditors; appointment of a Data Protection Officer; and additional accountability mechanisms. Large AI platforms processing personal data at scale are likely SDF candidates.
- **Automated decision-making:** Data Fiduciaries must provide transparent information about automated decision-making processes that result in significant decisions affecting Data Principals. Data Principals have the right to seek explanation and to contest such decisions.
- **Transparency:** Notice must be provided at or before the point of data collection, including: nature of data; purpose of processing; manner of exercising Data Principal rights; and contact details of the grievance officer.
- **Data retention:** Personal data must be erased once the purpose for which it was collected is fulfilled or consent is withdrawn, unless retention is required by law.

---

## Cross-border transfer mechanisms

- The DPDPA employs a **whitelist approach**: cross-border transfers of personal data are permitted only to countries and territories notified by the Indian government as permissible destinations.
- The government may restrict transfers to countries posing a risk to national security or public order.
- The 2025 Rules initiated the process for publishing the approved transfer destination list. Organisations must monitor official government notifications as the whitelist framework is progressively operationalized.
- Practical note: until the whitelist is fully published, organisations should engage early with MeitY guidance and consider contractual safeguards as interim measures.

---

## Enforcement and fines

The Data Protection Board adjudicates complaints and imposes financial penalties per instance of violation (not per affected individual):

| Violation Category | Maximum Penalty |
|---|---|
| Failure to implement adequate security safeguards (personal data breach) | INR 250 crore (~USD 30 million) |
| Failure to notify DPBI of a personal data breach | INR 200 crore (~USD 24 million) |
| Breach of children's data obligations | INR 200 crore (~USD 24 million) |
| Failure to notify affected Data Principals of a breach | INR 200 crore (~USD 24 million) |
| Other violations of the DPDPA | INR 50 crore (~USD 6 million) |

There are no criminal penalties under the DPDPA; enforcement is administrative through the DPBI.

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organisations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
