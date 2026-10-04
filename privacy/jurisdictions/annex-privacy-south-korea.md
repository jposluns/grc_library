# South Korea Privacy Regulatory Requirements

**Document Title:** South Korea Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.4\
**Date:** 2026-10-04\
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

- **Personal Information Protection Act (PIPA)**: South Korea's primary data protection law. Most recently amended by Act No. 21445 (promulgated 10 March 2026, in force 11 September 2026); the 2023 amendment (Act No. 19234, promulgated March 2023, key provisions effective September 2023) is the version held in English translation. A further amendment, Act No. 21910 (in force 9 March 2027), is pending.
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
| **Compensation and statutory damages (Arts 39, 39-2)**: a data subject suffering damage from a violation may claim compensation unless the controller proves no intent or negligence (Art 39(1)); where a data subject suffers damage from loss, theft, divulgence, forgery, alteration, or damage of their own personal information caused by the controller's intention or negligence, the court may award up to five times such damage, unless the controller proves the absence of intention or negligence (Art 39(3)); for those same compromise events the data subject may instead elect statutory damages up to the Art 39-2 cap. | *(Korea-specific liability; the library's disclosure-accuracy and security controls reduce the exposure)* |

## AI and privacy obligations

- **Right to explanation:** Data subjects may request an explanation of any decision made solely through automated means that significantly affects their rights or interests. The data controller must explain the criteria and logic applied and provide human review upon request.
- **Purpose limitation and data minimization:** Apply to AI training on personal data. Consent must be specific to the AI processing purpose.
- **High-risk processing:** PIPC guidance addresses higher-risk processing such as CCTV, biometric, and credit-assessment systems (proportionality and human oversight); that guidance is not held in the reference base, so an adopter confirms the current PIPC requirements directly. <!-- ref-absence: PIPC high-risk processing guidance | PIPC CCTV -->
- **Employment and profiling:** PIPC guidance is reported to address AI use in employment screening and credit decisions (proportionality and human oversight); that guidance is not held in the reference base, so an adopter confirms the current PIPC position directly. <!-- ref-absence: PIPC employment screening guidance | PIPC profiling -->

---

## Cross-border transfer mechanisms

Article 28-8, quoted from the KLRI English translation (Act No. 19234), with no substantive difference found against Article 28-8 of the consolidated Act No. 21445 in force since 11 September 2026 (law.go.kr, checked 3 October 2026):

> **Article 28-8(1) (transfer grounds):** No cross-border provision (including inquiry), entrusted processing, or storage (hereafter in this Section referred to as "transfer") of personal information shall be allowed by a personal information controller: Provided, That in any of the following cases, the cross-border transfer of personal information may be allowed:
>
> 1. Where separate consent is obtained from the data subject;
> 2. Where there are special provisions regarding the cross-border transfer of personal information in a statute, a treaty to which the Republic of Korea is a party, or other international conventions;
> 3. In any of the following cases where it is necessary to entrust the processing of personal information and to retain such personal information in order to conclude and perform a contract with the data subject:
>    - (a) Where the matters set forth in the subparagraphs of paragraph (2) are disclosed in the Privacy Policy provided in Article 30;
>    - (b) Where the matters provided in the subparagraphs of paragraph (2) are communicated to the data subject by means prescribed by Presidential Decree, such as electronic mail;
> 4. Where the recipient of personal information obtains certification determined and publicly notified by the Protection Commission, such as the certification of personal information protection under Article 32-2, and takes all of the following measures:
>    - (a) Safety measures necessary for protecting personal information and measures necessary for guaranteeing the rights of data subjects;
>    - (b) Measures necessary for implementing certified matters in the country to which personal information is to be transferred;
> 5. Where the Protection Commission recognizes that the personal information protection system of the country or international organization to which the personal information is to be transferred, the scope of guarantee of the rights of the data subject, and the procedures for damage relief, etc. are substantially equal to the level of personal information protection under this Act.
>
> **Article 28-8(2) (advance information for consent under paragraph (1)1):** A personal information controller shall inform data subjects of the following matters in advance when obtaining consent under paragraph (1) 1:
>
> 1. Particulars of the personal information to be transferred;
> 2. The country to which the personal information is transferred, transfer date, and method;
> 3. Name of the recipient of personal information (referring to the name of a corporation and the contact information of the corporation, if the recipient is a corporation);
> 4. The purpose of using personal information by the recipient of personal information and the period of retention and use of personal information;
> 5. The method and procedure for refusing the transfer of personal information and the effect of such refusal.
>
> **Article 28-8(3) (changes):** A personal information controller that intends to change the matters provided in any subparagraph of paragraph (2) shall inform a data subject of such change and obtain the data subject's consent thereto.
>
> **Article 28-8(4) (other provisions and protective measures):** A personal information controller shall comply with other provisions of this Act and Articles 17 through 19 and Chapter V of this Act, which are related to the cross-border transfer of personal information, and shall take protective measures prescribed by Presidential Decree, where it makes cross-border transfers of personal information pursuant to the proviso, with the exception of the subparagraphs, of paragraph (1).
>
> **Article 28-8(5) (contracts):** A personal information controller shall not enter into a contract for cross-border transfers of personal information containing terms and conditions that are in violation of this Act.
>
> **Article 28-8(6) (further criteria and procedures):** Except as provided in paragraphs (1) through (5), matters necessary for the criteria and procedures for the cross-border transfer of personal information, etc. shall be prescribed by Presidential Decree.

**Pending amendment (Act No. 21910, promulgated 8 September 2026, in force 9 March 2027):** new Article 28-15 allows the PIPC, after deliberation and resolution, to disapply Article 28-8 to the extent of overseas outsourced processing (entrusted processing abroad) where personal information is used under the Article 28-12 special case for artificial intelligence development. The Article 28-8 transfer grounds above otherwise continue to apply.

---

## Enforcement and fines

- **Administrative penalties:** Up to 3% of annual revenue for violations involving processing sensitive information, unlawful third-party provision, or outsourcing without authorization.
- **Criminal penalties:** Up to 10 years imprisonment or fines up to KRW 100 million for the most serious violations.

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
