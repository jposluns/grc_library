# South Africa Privacy Regulatory Requirements

**Document Title:** South Africa Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.1\
**Date:** 2026-09-11\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/annex-privacy-jurisdiction-index.md`](../annex-privacy-jurisdiction-index.md), [`privacy/policy-privacy-and-data-governance.md`](../policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/jurisdictions/annex-privacy-south-africa.md`](annex-privacy-south-africa.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex defines privacy and AI regulatory requirements applicable to the processing of personal data in South Africa under the Protection of Personal Information Act, 2013 (POPIA). It supplements the Privacy and Data Governance Policy and the Privacy Impact and Cross-Border Transfer Procedure.

---

## Applicable laws and regulatory authorities

- **Protection of Personal Information Act, 2013 (POPIA)**: Act No. 4 of 2013, fully in effect since 2021-07-01. One of the most comprehensive privacy laws in Africa, enacted to regulate the processing of personal information in harmony with international standards (s. 2). Applies to processing of personal information by responsible parties established in South Africa, or not established in South Africa but who make use of automated or non-automated means in South Africa.
- **Eight conditions for lawful processing:** Accountability; Processing Limitation; Purpose Specification; Further Processing Limitation; Information Quality; Openness; Security Safeguards; Data Subject Participation.
- **Special personal information (s. 26):** processing is prohibited, subject to the s. 27 authorizations, for a data subject's religious or philosophical beliefs, race or ethnic origin, trade union membership, political persuasion, health or sex life, or biometric information, and for criminal behaviour. A child's personal information is governed separately (ss. 34-35).
- **Regulatory authority:** Information Regulator.

---

## Eight conditions for lawful processing (POPIA)

POPIA (Chapter 3) sets eight conditions for the lawful processing of personal information by a responsible party. Each is mapped to the library control that carries it, or flagged as a South Africa-specific gap.

| POPIA condition (held section) | Library disposition |
| --- | --- |
| **Condition 1 - Accountability (s. 8)**: the responsible party is responsible for complying with the Chapter 3 conditions and the measures giving effect to them, at the time the purpose and means are determined and during the processing. | library accountability and data-governance controls |
| **Condition 2 - Processing limitation (ss. 9-12)**: processing is lawful and is carried out in a reasonable manner that does not infringe the data subject's privacy (s. 9), is minimal (adequate, relevant, not excessive, s. 10), rests on one of the s. 11(1) grounds (consent; necessity for a contract; a legal obligation; protection of a legitimate interest of the data subject; a public-law duty; or a legitimate interest of the responsible party or a third party) with the burden of proof for consent on the responsible party (s. 11(2)) and a right to object on reasonable grounds to the paragraph (d)-(f) grounds (s. 11(3)), and is collected directly from the data subject subject to the s. 12 exceptions. | library lawful-basis, consent, and data-minimization controls |
| **Condition 3 - Purpose specification (ss. 13-14)**: information is collected for a specific, explicitly defined, and lawful purpose (s. 13) and is not retained longer than necessary for that purpose, subject to the s. 14 exceptions. | library purpose-limitation and retention controls |
| **Condition 4 - Further processing limitation (s. 15)**: further processing is compatible with the original collection purpose, assessed against the s. 15(2) factors. | library purpose-compatibility controls |
| **Condition 5 - Information quality (s. 16)**: the responsible party takes reasonably practicable steps to keep personal information complete, accurate, not misleading, and updated where necessary. | library data-quality controls |
| **Condition 6 - Openness (ss. 17-18)**: the responsible party maintains the s. 17 processing documentation (per PAIA ss. 14 or 51) and notifies the data subject of the s. 18 matters when collecting. | library records-of-processing and privacy-notice controls (`privacy/template-privacy-notice.md`) |
| **Condition 7 - Security safeguards (ss. 19-22)**: the responsible party secures the integrity and confidentiality of personal information through appropriate, reasonable technical and organizational measures (s. 19), binds operators/processors (ss. 20-21), and notifies the Information Regulator and, subject to s. 22(3), the affected data subjects (unless the data subject's identity cannot be established) of a compromise as soon as reasonably possible (s. 22). | library information-security and breach-notification controls (`security/`) |
| **Condition 8 - Data subject participation (ss. 23-25)**: on adequate proof of identity, the data subject may confirm what personal information is held and request access (s. 23), made in the manner set out in s. 25, and may request correction or deletion of the information in the prescribed manner (s. 24). | library data-subject-rights controls (`privacy/procedure-data-subject-rights-management.md`, `privacy/template-dsar-workflow.md`) |

Special personal information (religion or philosophy, race or ethnic origin, trade-union membership, political persuasion, health or sex life, biometric information, and criminal behaviour) may not be processed absent an s. 27 authorization or a specific ss. 28-33 ground (s. 26); processing of children's personal information is likewise prohibited absent an s. 35 ground (s. 34). The **Information Regulator**, established under s. 39, monitors and enforces compliance with POPIA under its s. 40 powers, duties, and functions, and electronic direct marketing is prohibited unless the data subject has consented or is an existing customer within the s. 69 soft opt-in.

## AI and privacy obligations

- **Processing Limitation (Condition 2) and Purpose Specification (Condition 3):** Apply to the use of personal information in AI training and operation.
- **Automated decision-making (POPIA Section 71):** a data subject may not be subject to a decision that results in legal consequences, or affects the data subject to a substantial degree, based solely on automated processing intended to profile the data subject (s. 71(1)). This does not apply where the decision is taken in connection with a contract (with the data subject's request met or appropriate safeguards taken) or is governed by a law or code of conduct in which appropriate measures safeguard the data subject's legitimate interests (s. 71(2)). Where the contractual route is relied on, those appropriate measures (s. 71(2)(a)(ii)) must give the data subject an opportunity to make representations and sufficient information about the underlying logic (s. 71(3)).
- **Security safeguards (Condition 7):** Responsible parties must implement appropriate technical and organizational measures to protect personal information processed in AI systems.
- The concrete high-risk mechanism is prior authorization: a responsible party must obtain the Regulator's prior authorization before it links a unique identifier, for a purpose other than the one it was collected for, with information processed by other responsible parties; processes criminal or unlawful-conduct information for third parties; processes information for credit reporting; or transfers special or children's information to a foreign country without adequate protection (s. 57(1)), unless a Chapter 7 code of conduct for the sector is in force (s. 57(3)).

---

## Cross-border transfer mechanisms

- **Section 72:** a responsible party may transfer personal information to a third party in a foreign country only where: the recipient is subject to a law, binding corporate rules, or binding agreement providing an adequate level of protection substantially similar to POPIA's conditions and onward-transfer rules (s. 72(1)(a)); the data subject consents (b); the transfer is necessary to perform a contract with the data subject or for pre-contractual measures at the data subject's request (c); the transfer is necessary to conclude or perform a contract concluded in the data subject's interest between the responsible party and a third party (d); or the transfer is for the data subject's benefit where obtaining consent is not reasonably practicable but the data subject would likely give it (e).

---

## Enforcement and fines

- Administrative fines up to ZAR 10 million (approximately USD 535,000).
- Criminal penalties on conviction for the enumerated offences: up to 10 years' imprisonment or a fine (or both) for the s. 100/103(1)/104(2)/105(1)/106 offences, and up to 12 months or a fine (or both) for the s. 59/101/102/103(2)/104(1) offences (s. 107).
- Private right of action for damages.

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
