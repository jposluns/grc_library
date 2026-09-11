# Thailand Privacy Regulatory Requirements

**Document Title:** Thailand Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.0\
**Date:** 2026-09-11\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/annex-privacy-jurisdiction-index.md`](../annex-privacy-jurisdiction-index.md), [`privacy/policy-privacy-and-data-governance.md`](../policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/jurisdictions/annex-privacy-thailand.md`](annex-privacy-thailand.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex defines privacy and AI regulatory requirements applicable to the processing of personal data in Thailand under the Personal Data Protection Act B.E. 2562 (2019) (PDPA). It supplements the Privacy and Data Governance Policy and the Privacy Impact and Cross-Border Transfer Procedure.

---

## Applicable laws and regulatory authorities

- **Personal Data Protection Act B.E. 2562 (2019) (PDPA)**: In force for general compliance obligations since 2022-06-01. Closely modelled on GDPR.
- Lawful bases: consent, vital interests, legitimate interests, public task, legal obligation, and contract performance.
- Mandatory breach notification within 72 hours where feasible.
- Sensitive personal data categories: health, biometric, genetic, political opinion, religious or philosophical belief, sexual behaviour, criminal records, and disability data.
- DPOs required (s. 41) where the controller or processor is a Committee-prescribed public authority, where its activities require regular monitoring of personal data by reason of a Committee-prescribed large data volume, or where its core activity is processing sensitive personal data under s. 26.
- **Regulatory authority:** Personal Data Protection Committee (PDPC), under the Ministry of Digital Economy and Society.

---

## Core PDPA obligations and data-subject rights

Thailand's Personal Data Protection Act (B.E. 2562/2019) imposes the following core obligations on data controllers and grants the enumerated data-subject rights. Each is mapped to the library control that carries it, or flagged as a Thailand-specific gap.

| PDPA obligation / right (held section) | Library disposition |
| --- | --- |
| **Consent and lawful basis (s. 19)**: a data controller must not collect, use, or disclose personal data without the data subject's consent, unless another PDPA basis applies; a consent request must be explicit, in a form clearly distinguishable from other matters, and in plain, accessible language. | library consent-management and lawful-basis controls |
| **Purpose and collection (ss. 21-25)**: personal data is collected, used, or disclosed according to the purpose notified to the data subject (s. 21); collection is limited to the extent necessary for the lawful purpose (s. 22); the data subject is given the s. 23 notice at or before collection; collection without consent is confined to the s. 24 bases; and collection from a source other than the data subject is restricted by s. 25. | library purpose-limitation, data-minimization, and collection-notice controls |
| **Sensitive personal data (s. 26)**: data revealing racial or ethnic origin, political opinions, religious or philosophical beliefs, sexual behaviour, criminal records, health, disability, trade-union membership, genetic, or biometric data must not be collected without explicit consent or an s. 26 exception. | library special-category-data controls |
| **Use and disclosure (s. 27)**: the controller must not use or disclose personal data without the data subject's consent, unless the data was collected under an s. 24 or s. 26 exception; a recipient's further use or disclosure is bounded accordingly. | library purpose-limitation and third-party-sharing controls |
| **Data-subject rights (ss. 30-36)**: subject to the grounds, exceptions, and refusal conditions in the cited sections, the data subject may request access and a copy (s. 30), data portability (s. 31), object to processing (s. 32), request erasure, destruction, or anonymization (s. 33), request restriction of use (s. 34), and request rectification to keep data accurate, current, and complete (s. 36). | library data-subject-rights controls (`privacy/procedure-data-subject-rights-management.md`, `privacy/template-dsar-workflow.md`) |
| **Controller duties, security, and breach (s. 37)**: the controller provides appropriate security measures (s. 37(1)), acts to prevent a recipient from unauthorized or unlawful use or disclosure (s. 37(2)), maintains an examination system for erasure or destruction of personal data on expiry of the retention period or where a request or withdrawal of consent applies (s. 37(3)), and notifies the Office without delay and, where feasible, within 72 hours of awareness of a breach, unless the breach is unlikely to result in a risk to rights and freedoms, notifying the data subject and the remedial measures where the risk is high (s. 37(4)). | library information-security and breach-notification controls (`security/`) |
| **Records of processing (s. 39)**: the controller maintains a record of processing activities (s. 39(1)-(8)); items (1)-(6) and (8) may not apply to a qualifying small organization unless its processing is risky, is not occasional, or involves s. 26 sensitive data. | library records-of-processing controls |
| **Data Protection Officer (s. 41)**: a controller or processor designates a DPO where it is a public authority as prescribed and announced by the Committee (s. 41(1)), where its collection, use, or disclosure activities require regular monitoring of the personal data or the system by reason of having a large amount of personal data as prescribed and announced by the Committee (s. 41(2)), or where its core activity is the processing of sensitive personal data under s. 26 (s. 41(3)). | library accountability and DPO-designation controls |
| **Liability and penalties (ss. 77-90)**: violations carry civil liability, including punitive damages the court may order up to twice the amount of actual damages (ss. 77-78), together with the administrative fines and criminal penalties in ss. 79-90. | *(Thailand-specific liability; the library's disclosure-accuracy and security controls reduce the exposure)* |

Cross-border transfers are governed by ss. 28-29 and are treated in the cross-border section below.

## AI and privacy obligations

- PDPC guidance states that AI systems processing personal data must comply with PDPA principles.
- Automated decision-making producing legal or significantly impactful effects requires human oversight and a mechanism for data subjects to contest decisions.
- Purpose limitation and data minimization apply to personal data used in AI training and inference.

---

## Cross-border transfer mechanisms

- Transfers permitted with: consent; vital interests; legal claims; public interest; or adequacy as determined by the PDPC (adequacy list under development).
- Contractual safeguards are the primary interim mechanism pending PDPC adequacy determinations.

---

## Enforcement and fines

- Administrative fines: up to THB 5 million (~USD 140,000).
- Criminal fines: up to THB 1 million.
- The PDPC may issue compliance orders and cease-processing directions.

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
