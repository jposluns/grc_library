# Malaysia Privacy Regulatory Requirements

**Document Title:** Malaysia Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.2.0\
**Date:** 2026-09-12\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/annex-privacy-jurisdiction-index.md`](../annex-privacy-jurisdiction-index.md), [`privacy/policy-privacy-and-data-governance.md`](../policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/jurisdictions/annex-privacy-malaysia.md`](annex-privacy-malaysia.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex defines privacy and AI regulatory requirements applicable to the processing of personal data in Malaysia under the Personal Data Protection Act 2010 (Act 709) as amended in 2024. It supplements the Privacy and Data Governance Policy and the Privacy Impact and Cross-Border Transfer Procedure.

---

## Applicable laws and regulatory authorities

- **Personal Data Protection Act 2010 (Act 709)**: As amended by the **Personal Data Protection (Amendment) Act 2024 (Act A1727)**. The Amendment Act commences in tranches by ministerial appointment and, among other changes, renames the "data user" role to "data controller", introduces the mandatory appointment of data protection officers, statutory breach notification, direct accountability of data processors, and the right to data portability.
- Seven data protection principles: General; Notice and Choice; Disclosure; Security; Retention; Data Integrity; Access.
- **2024 amendments introduced:**
  - **Mandatory DPO:** both data controllers and data processors must appoint one or more data protection officers, notified to the Commissioner; the appointment does not discharge the controller's or processor's own duties under the Act (s. 12A).
  - **Breach notification:** where a controller has reason to believe a personal data breach has occurred, it notifies the Commissioner as soon as practicable in the manner and form the Commissioner determines; where the breach causes or is likely to cause significant harm to the data subject, it notifies the data subject without unnecessary delay (s. 12B).
  - **Right to data portability** (s. 43A).
  - **Direct accountability of data processors:** a data processor processing on a controller's behalf complies directly with the Security Principle (s. 5(1a)) and the s. 9 practical-step security duties, and appoints its own DPO (s. 12A).
  - **Deceased individuals** are excluded from the data-subject definition (A1727 s. 3).
  - **Increased penalties** (see Enforcement and fines below).
- **Regulatory authority:** Personal Data Protection Commissioner under the Ministry of Digital. The Personal Data Protection Department (JPDP) administers the Act and issues guidelines.

---

## Core Act 709 obligations and data-subject rights

Malaysia's Personal Data Protection Act 2010 (Act 709), as amended by Act A1727, imposes the following core obligations on data controllers (and, where stated, data processors) and grants the enumerated data-subject rights. Each is mapped to the library control that carries it.

| Act 709 obligation / right (held section) | Library disposition |
| --- | --- |
| **General Principle (s. 6)**: personal data is processed only with the data subject's consent (s. 6(1)) or where a s. 6(2) ground applies (contract performance, pre-contractual steps, legal obligation, vital interests, administration of justice, statutory functions); processing must be for a lawful purpose directly related to the controller's activity, necessary for that purpose, and adequate but not excessive (s. 6(3)). | library consent-management, lawful-basis, and data-minimization controls |
| **Notice and Choice Principle (s. 7)**: written notice of the processing, the data, its purposes and source, access and correction rights, contact points, classes of third-party recipients, the choices for limiting processing, and whether supply is obligatory with the consequences of failure (s. 7(1)); given as soon as practicable at first request or collection (s. 7(2)); in the national and English languages with a clear, readily accessible means to exercise choice (s. 7(3)). | library collection-notice and transparency controls |
| **Employment and workplace monitoring**: no monitoring-specific provision; employee processing is bounded by the s. 6(3) necessity and adequate-but-not-excessive limits and the s. 7(3) bilingual notice; sensitive personal data may be processed without explicit consent where necessary to exercise or perform a right or obligation conferred or imposed by law in connection with employment (s. 40(1)(b)). | library acceptable-use and HR-privacy controls |
| **Sensitive personal data (s. 40)**: processed only with explicit consent (s. 40(1)(a)) or under a s. 40(1)(b) to (c) condition. | library special-category-data controls |
| **Access workflow (ss. 30 to 33)**: a data subject may make a data access request (s. 30); the controller complies not later than 21 days (s. 31(1)); if unable, it notifies the requestor in writing with reasons before that period expires and complies to the extent able (s. 31(2)), and completes compliance not later than 14 days after the 21-day period (s. 31(3)); refusal is only on the s. 32 closed grounds, notified with reasons (s. 33). | library data-subject-rights controls ([`privacy/procedure-data-subject-rights-management.md`](../procedure-data-subject-rights-management.md)) |
| **Correction workflow (ss. 34 to 37)**: on a data correction request (s. 34), a controller satisfied the data is inaccurate, incomplete, misleading, or not up to date corrects it, supplies the corrected copy, and takes all practicable steps to supply the corrected data with written reasons to any third party to whom the data was disclosed in the preceding 12 months and who may still be using it (s. 35(1)); the same 14-day extension mechanics apply (s. 35(2) to (3)); refusal is only on the s. 36 grounds, notified under s. 37. | library data-subject-rights and record-correction controls |
| **Data portability (s. 43A)**: a data subject may, by written notice given by electronic means, request direct controller-to-controller transmission of their personal data (s. 43A(1)); subject to technical feasibility and data-format compatibility (s. 43A(2)); transmission is completed within the period as may be prescribed, with no fixed deadline in the Act itself (s. 43A(3)). | library data-portability controls |
| **Accountability and DPO (s. 12A)**: a data controller, and a data processor processing on its behalf, each appoint one or more data protection officers accountable for compliance with the Act (s. 12A(1) to (2)); the controller notifies the Commissioner of the appointment in the manner and form the Commissioner determines (s. 12A(3)); appointment does not discharge the controller or processor from any duty under the Act (s. 12A(4)). | library accountability and DPO-designation controls |
| **Breach notification (s. 12B)**: where a controller has reason to believe a personal data breach has occurred, it notifies the Commissioner as soon as practicable (s. 12B(1)); where the breach causes or is likely to cause significant harm to the data subject, it notifies the data subject without unnecessary delay (s. 12B(2)). | library breach-notification controls |
| **Processor security (ss. 5(1a), 9)**: a processor processing on a controller's behalf complies directly with the Security Principle (s. 5(1a)); the s. 9 practical-step security duties bind controller and processor alike. | library information-security and third-party controls |

---

## AI and privacy obligations

- The seven data protection principles apply to AI systems processing personal data, including transparency (Notice and Choice), purpose limitation (Disclosure), and security requirements.
- A national AI Ethics Principle framework (2021) provides voluntary guidance for AI deployments.
- The Personal Data Protection Commissioner has confirmed that AI systems processing personal data must comply with Act 709 principles.

---

## Cross-border transfer mechanisms

- The former ministerial approved-country list (repealed s. 129(1)) was deleted by the 2024 amendment. A data controller may transfer personal data to a place outside Malaysia where there is in force in that place a law substantially similar to the Act, or where that place provides an adequate level of protection at least equivalent to the Act (amended s. 129(2)).
- Independently of s. 129(2), transfer is permitted on the s. 129(3) exceptions: the data subject's consent; performance of a contract with the data subject; conclusion or performance of a contract with a third party at the data subject's request or in their interests; legal proceedings, legal advice, or establishing, exercising, or defending legal rights; avoidance or mitigation of adverse action where written consent is impracticable but would have been given; the controller has taken all reasonable precautions and exercised all due diligence that the data will not be processed there in a way that would contravene the Act if in Malaysia; or protection of the data subject's vital interests. The former ministerial public-interest ground was deleted.
- The Act prescribes no transfer-assessment methodology; an adopter applying the library's transfer-impact-assessment procedure does so as governance practice, not as an Act 709 requirement.

---

## Enforcement and fines

Act 709 penalties are conviction-based criminal offences, not administrative fines:

- Contravention of the data protection principles by a controller (s. 5(1)), or of the processor security duty (s. 5(1a)): a fine up to MYR 1,000,000, imprisonment up to three years, or both (s. 5(2) as amended).
- Failure to notify the Commissioner of a personal data breach: a fine up to MYR 250,000, imprisonment up to two years, or both (s. 12B(3)).
- Unlawful cross-border transfer: a fine up to MYR 300,000, imprisonment up to two years, or both (s. 129(5)).

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**

