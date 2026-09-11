# Kenya Privacy Regulatory Requirements

**Document Title:** Kenya Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.0\
**Date:** 2026-09-11\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/annex-privacy-jurisdiction-index.md`](../annex-privacy-jurisdiction-index.md), [`privacy/policy-privacy-and-data-governance.md`](../policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/jurisdictions/annex-privacy-kenya.md`](annex-privacy-kenya.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex defines privacy and AI regulatory requirements applicable to the processing of personal data in Kenya under the Data Protection Act 2019. It supplements the Privacy and Data Governance Policy and the Privacy Impact and Cross-Border Transfer Procedure.

---

## Applicable laws and regulatory authorities

- **Data Protection Act 2019 (Act No. 24 of 2019)**: Fully in force. Applies to a data controller or processor established or ordinarily resident in Kenya that processes personal data while in Kenya, and to a controller or processor not established in Kenya that processes the personal data of data subjects located in Kenya, and only to personal data entered in a record by automated or non-automated means (non-automated data forming part of a filing system) (s. 4).
- Key rights: access to personal data; correction; deletion; portability; right to object to processing; right not to be subject to automated decision-making.
- Mandatory breach notification to the Data Commissioner without delay and within 72 hours of becoming aware, where personal data has been accessed or acquired by an unauthorized person and there is a real risk of harm (s. 43).
- A data controller or processor may designate a data protection officer (s. 24); the Data Commissioner sets the thresholds for mandatory registration of controllers and processors (s. 18).
- **Regulatory authority:** Office of the Data Protection Commissioner (ODPC).

---

## Core data-protection obligations and rights (DPA 2019)

Kenya's Data Protection Act, 2019 imposes the following core obligations on data controllers and processors and grants the enumerated data-subject rights. Each is mapped to the library control an adopter would use, with any Kenya-specific element that the library does not carry flagged as a gap.

| DPA 2019 obligation / right (held section) | Library disposition |
| --- | --- |
| **Principles of data protection (s. 25)**: personal data is processed in accordance with the data subject's right to privacy; processed lawfully, fairly, and transparently; collected for explicit, specified, and legitimate purposes; adequate, relevant, and limited to what is necessary; collected with a valid explanation where family or private affairs are concerned; kept accurate and up to date; retained no longer than necessary; and not transferred outside Kenya without proof of adequate safeguards or the data subject's consent. | adopter maps to library data-governance and data-quality controls; the s. 25(a) privacy-right, s. 25(e) family/private-affairs, and s. 25(h) cross-border limbs are Kenya-specific |
| **Rights of a data subject and their exercise (ss. 26-27)**: subject to the exceptions in the Act, the data subject has the rights to be informed of the use of their data, to access it, to object to processing, and to correction or deletion of false or misleading data (s. 26); a right may be exercised by a person with parental authority or a guardian where the data subject is a minor, and by the enumerated others (s. 27). | adopter maps to library data-subject-rights controls (`privacy/procedure-data-subject-rights-management.md`); the Kenya-specific exercise rules and timelines are an adopter gap |
| **Collection and duty to notify (ss. 28-29)**: personal data is collected directly from the data subject subject to the s. 28 exceptions, and, before collecting personal data, a data controller or data processor must, in so far as practicable, inform the data subject of the s. 29 matters. | adopter maps to library collection and privacy-notice controls (`privacy/template-privacy-notice.md`); the s. 29 processor duty and Kenya-specific notice items are an adopter gap |
| **Lawful processing and consent (ss. 30, 32)**: processing rests on one of the s. 30 bases; consent must meet the s. 32 conditions, with the controller or processor bearing the burden of proof and the data subject entitled to withdraw. | adopter maps to library lawful-basis and consent-management controls |
| **Sensitive and health data (ss. 44-46)**: sensitive personal data is processed only on the s. 45 permitted grounds, with additional rules for health data (s. 46). | adopter maps to library special-category-data controls |
| **Children's data (s. 33)**: processing a child's personal data requires the consent of the child's parent or guardian and that the processing protect and advance the rights and best interests of the child, with appropriate age-verification and consent mechanisms (s. 33(1)-(2)); a controller or processor providing counselling or child-protection services exclusively may not be required to obtain parental consent (s. 33(4)). | adopter maps to library children's-data controls (the age-assurance mechanisms are provided by the children's-data framework); the s. 33 best-interests duty and the s. 33(4) counselling carve-out are Kenya-specific |
| **Restrictions and automated decision-making (ss. 34-35)**: the s. 34 restrictions on processing apply, and a data subject has the right under s. 35 not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning or significantly affects the data subject, except where the decision is necessary for a contract, authorized by law with suitable safeguards, or based on the data subject's consent (s. 35(2)) (the operational statement of this right is in the AI section below). | adopter maps to library data-subject-rights and automated-decision controls |
| **Objection, portability, rectification, and erasure (ss. 36, 38, 40)**: the data subject may object to processing (s. 36), request data portability (s. 38), and request rectification or erasure (s. 40). | adopter maps to library data-subject-rights controls (`privacy/procedure-data-subject-rights-management.md`, `privacy/template-dsar-workflow.md`); the s. 38 Kenya-specific timeline is an adopter gap |
| **Data protection impact assessment (s. 31)**: a controller or processor carries out a DPIA, prior to the processing, where a processing operation is likely to result in high risk to the rights and freedoms of a data subject by virtue of its nature, scope, context, and purposes; the report is submitted 60 days prior to the processing, and the controller or processor consults the Data Commissioner where the DPIA indicates the processing would still result in high risk (ss. 31(3), 31(5)). | adopter maps to library privacy-impact-assessment controls (the DPIA template carries the prior-processing trigger and content requirements); the s. 31(5) 60-day submission and s. 31(3) Data Commissioner consultation are Kenya-specific, and the s. 31 processor-side DPIA duty is not carried by the controller-scoped template |
| **Retention limitation (s. 39)**: personal data is retained only as long as may be reasonably necessary to satisfy the purpose for which it is processed, unless retention is required or authorized by law or one of the other s. 39 grounds applies. | adopter maps to library data-retention controls |
| **Data protection by design and by default (ss. 41-42)**: the controller and processor implement appropriate technical and organizational measures by design and by default (s. 41), determined by the s. 42 particulars. | adopter maps primarily to the library privacy-by-design framework (`privacy/framework-privacy-by-design.md`), with security-by-design and information-security controls as supporting instruments; the s. 41 processor-side by-design duty is Kenya-specific |
| **Breach notification (s. 43)**: where personal data is accessed or acquired by an unauthorized person and there is a real risk of harm, the controller notifies the Data Commissioner without delay and within 72 hours of awareness, and communicates to the affected data subject in writing within a reasonably practicable period, unless the data subject's identity cannot be established (s. 43(1)(b)); communication may be delayed or restricted as necessary and proportionate for the prevention, detection, or investigation of an offence by the concerned relevant body (s. 43(4)), and is not required where the controller or processor has implemented appropriate safeguards such as encryption of the affected data (s. 43(6)); where a data processor becomes aware of a breach it notifies the controller without delay and, where reasonably practicable, within 48 hours of awareness (s. 43(3)). | adopter maps to library incident-response and breach-notification controls; the Kenya Data Commissioner recipient, timelines, and processor duty are an adopter gap |

## AI and privacy obligations

- Data subjects have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning, or significantly affects, them, except where the decision is necessary for a contract, authorized by law with suitable safeguards, or based on their consent (s. 35(1)-(2)).
- Where such a decision is taken, the controller or processor must notify the data subject in writing as soon as reasonably practicable; the data subject may then request that the decision be reconsidered or that a new decision not based solely on automated processing be taken, and the controller or processor must, within a reasonable period, consider the request, comply with it, and notify the data subject in writing of the steps taken and the outcome (s. 35(3)-(4)).
- The Data Commissioner may issue guidelines or codes of practice for controllers, processors, and data protection officers (s. 74(1)(a)), and the Cabinet Secretary may make further regulations concerning solely automated decision-making (s. 35(5)).

---

## Cross-border transfer mechanisms

- A controller or processor may transfer personal data out of Kenya only where it has given the Data Commissioner proof of appropriate safeguards for the security and protection of the data (including transfer to jurisdictions with commensurate data protection laws), or where the transfer is necessary on one of the s. 48(c) grounds (contract with or in the interest of the data subject, a matter of public interest, legal claims, protecting the vital interests of the data subject or others where the subject is physically or legally incapable of giving consent, or compelling legitimate interests that are not overridden by the data subjects' interests, rights, and freedoms) (s. 48).
- Transfer of sensitive personal data out of Kenya requires both the data subject's consent and confirmation of appropriate safeguards (s. 49(1)); the Data Commissioner may require proof of the safeguards' effectiveness and may prohibit, suspend, or condition a transfer to protect data subjects (s. 49(2)-(3)).

---

## Enforcement and fines

- Administrative fines (ODPC penalty notice): up to KES 5 million, or one per cent of an undertaking's annual turnover, whichever is lower (Data Protection Act 2019, s. 63).
- General penalty on conviction: for an offence with no specific penalty, a fine up to KES 3 million or imprisonment up to 10 years, or both (s. 73).
- The Data Commissioner may serve an enforcement notice requiring specified remedial steps (s. 58) and may issue a penalty notice of up to KES 5 million, or for an undertaking up to 1% of preceding-year annual turnover, whichever is lower (ss. 62-63); the Office may also conduct assessments of processing (s. 8).

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
