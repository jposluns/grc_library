# South Korea Privacy Regulatory Requirements

**Document Title:** South Korea Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.0\
**Date:** 2026-09-11\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/annex-privacy-jurisdiction-index.md`](../annex-privacy-jurisdiction-index.md), [`privacy/policy-privacy-and-data-governance.md`](../policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/jurisdictions/annex-privacy-south-korea.md`](annex-privacy-south-korea.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex defines privacy and AI regulatory requirements applicable to the processing of personal data in South Korea under the Personal Information Protection Act (PIPA). It supplements the Privacy and Data Governance Policy and the Privacy Impact and Cross-Border Transfer Procedure.

---

## Applicable laws and regulatory authorities

- **Personal Information Protection Act (PIPA)**: Most recently amended in 2023 (promulgated March 2023; key provisions effective September 2023). South Korea's primary data protection law.
- South Korea holds an EU GDPR adequacy decision (granted December 2021).
- **Key 2023 amendments:** Right to explanation for automated decisions; right to data portability; mandatory data breach notification within 72 hours; enhanced penalty regime; mobile application and online service obligations.
- **Regulatory authority:** Personal Information Protection Commission (PIPC).

---

## Core PIPA obligations and data-subject rights

The Personal Information Protection Act (PIPA) imposes the following core obligations on personal information controllers and grants the enumerated data-subject rights. Each is mapped to the library control that carries it, or flagged as a Korea-specific gap.

| PIPA obligation / right (held article) | Library disposition |
| --- | --- |
| **Protection principles (Art 3)**: the controller specifies processing purposes explicitly, collects lawfully and fairly to the minimum extent necessary, and keeps personal information accurate, complete, and up to date. | library data-governance and data-quality controls |
| **Data-subject rights (Art 4)**: the data subject has the rights to be informed of processing, to decide whether and how far to consent, to confirm processing and access the information, to suspend, correct, erase, or destroy it, and to appropriate redress. | library data-subject-rights controls (`privacy/procedure-data-subject-rights-management.md`) |
| **Lawful bases for collection and use (Art 15)**: the controller may collect and use personal information only on one of the Art 15(1) bases (consent, statutory obligation, contract performance, and the other enumerated grounds). | library lawful-basis and consent controls |
| **Collection minimization (Art 16)**: only the minimum personal information necessary for the purpose is collected, and the controller bears the burden of proof. | library data-minimization controls |
| **Provision to third parties (Art 17) and out-of-purpose limitation (Art 18)**: provision to a third party requires consent or an Art 17 basis, and the controller must not use or provide personal information beyond the Art 15/17 scope except in the Art 18 cases. | library third-party-sharing and purpose-limitation controls |
| **Destruction when the purpose is achieved (Art 21)**: the controller must destroy personal information without delay once it is no longer necessary, unless retention is required by another statute. | library data-retention and destruction controls |
| **Consent mechanics (Art 22)**: each matter requiring consent is presented distinctly and in a clearly recognizable manner, with consent obtained separately. | library consent-management controls |
| **Sensitive information (Art 23)**: processing of sensitive information (ideology, beliefs, union or political-party membership, political opinions, health, sex life, and the prescribed categories) is prohibited absent separate consent or a statutory basis, with additional safeguards. | library special-category-data controls |
| **Unique identifiers (Art 24) and resident registration numbers (Art 24-2)**: the controller must not process the identifiers prescribed by Presidential Decree except after the Art 15(2)/17(2) notification and separate consent (given apart from consent to other processing), or where a statute specifically requires or permits it; a resident registration number must not be processed except in the narrow Art 24-2 cases (which require encryption and an alternative non-RRN sign-up route). | library identifier-handling controls; the RRN rule is Korea-specific and not carried by a dedicated control |
| **Duty of safeguards (Art 29)**: the controller takes the technical, managerial, and physical measures necessary to secure personal information. | library information-security controls (`security/`) |
| **Privacy policy (Art 30)**: the controller establishes and discloses a privacy policy covering the Art 30(1) enumerated matters. | library privacy-notice controls (`privacy/template-privacy-notice.md`; adopter maps the Korea-specific policy-content items) |
| **Privacy officer / CPO (Art 31)**: the controller designates a privacy officer responsible for personal-information processing. | library accountability and privacy-officer controls |
| **Data-breach notification (Art 34)**: on becoming aware of a divulgence, the controller notifies affected data subjects of the Art 34(1) matters without delay and, for a breach above the prescribed scale, reports without delay to the Protection Commission (PIPC) or a specialized institution designated by Presidential Decree (Art 34(3)). | library incident-response and breach-notification controls |
| **Access, correction/erasure, suspension (Arts 35, 36, 37)**: a data subject may request access (Art 35), correction or erasure of accessed information (Art 36), and suspension of processing (Art 37), subject to the statutory exceptions. | library data-subject-rights controls (`privacy/procedure-data-subject-rights-management.md`, `privacy/template-dsar-workflow.md`) |
| **Compensation and statutory damages (Arts 39, 39-2)**: a data subject suffering damage from a violation may claim compensation unless the controller proves no intent or negligence (Art 39(1)); where the damage arises from loss, theft, divulgence, forgery, alteration, or damage of the information caused by wrongful intent or negligence, the court may award up to three times the damage (Art 39(3)); for those same compromise events the data subject may instead elect statutory damages up to the Art 39-2 cap. | *(Korea-specific liability; the library's disclosure-accuracy and security controls reduce the exposure)* |

## AI and privacy obligations

- **Right to explanation:** Data subjects may request an explanation of any decision made solely through automated means that significantly affects their rights or interests. The data controller must explain the criteria and logic applied and provide human review upon request.
- **Purpose limitation and data minimization:** Apply to AI training on personal data. Consent must be specific to the AI processing purpose.
- **High-risk processing:** CCTV systems, biometric systems, and credit assessment tools are subject to enhanced PIPC guidance requiring proportionality and human oversight.
- **Employment and profiling:** PIPC has issued guidance on AI use in employment screening and credit decisions, requiring proportionality and human oversight.

---

## Cross-border transfer mechanisms

- Transfers permitted to: countries designated by the PIPC as providing equivalent or higher protection; the EU (adequacy decision); with data subject-specific consent; or via PIPC-approved standard contractual clauses.
- Mandatory disclosure to data subjects of the identity, contact details, and purposes of overseas recipients at or before transfer.

---

## Enforcement and fines

- **Administrative penalties:** Up to 3% of annual revenue for violations involving processing sensitive information, unlawful third-party provision, or outsourcing without authorization.
- **Criminal penalties:** Up to 10 years imprisonment or fines up to KRW 100 million for the most serious violations.

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
