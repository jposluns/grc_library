# South Korea Privacy Regulatory Requirements

**Document Title:** South Korea Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.5\
**Date:** 2026-10-21\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/annex-privacy-jurisdiction-index.md`](../annex-privacy-jurisdiction-index.md), [`privacy/policy-privacy-and-data-governance.md`](../policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md), [`ai/jurisdictions/annex-ai-south-korea.md`](../../ai/jurisdictions/annex-ai-south-korea.md)\
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
- South Korea holds an EU GDPR adequacy decision (Commission Implementing Decision (EU) 2022/254, granted December 2021); that decision is not held in the reference base, so an adopter confirms its current scope and status directly. <!-- ref-absence: Implementing Decision (EU) 2022/254 | EU adequacy decision for the Republic of Korea -->
- **Key 2023 amendments:** Right to explanation for automated decisions; right to data portability; data-breach notification to data subjects "without delay" (Article 34(1)) and reporting "without delay" to the Protection Commission (PIPC) or a specialized institution designated by Presidential Decree, as prescribed by Presidential Decree in consideration of the types of personal information, the process and scale of divulgence, and other factors (Article 34(3)), both quoted below, with the timing, methods, and procedures for reporting delegated to Presidential Decree (Article 34(4)); enhanced penalty regime; mobile application and online service obligations.
- **Breach-reporting deadline:** a 72-hour reporting period is reported to be set by the PIPA Enforcement Decree; that decree is not held in the reference base, so an adopter confirms the current deadline directly. <!-- ref-absence: PIPA Enforcement Decree | Enforcement Decree of the Personal Information Protection Act -->
- **Regulatory authority:** Personal Information Protection Commission (PIPC).

Article 34(1), introductory text, and Article 34(3), first sentence, quoted from the KLRI English translation (Act No. 19234); these provisions were not compared against Act No. 21445 (in force since 11 September 2026), so an adopter confirms the current text directly:

> **Article 34(1), introductory text (notification):** A personal information controller shall notify data subjects of the following matters without delay when the personal information controller becomes aware of loss, theft, or divulgence (hereafter in this Article referred to as "divulgence, etc.") of personal information: Provided, That if the contact information of the data subject is unknown or if any other good cause exists, a measure may be taken in lieu of giving notice, as prescribed by Presidential Decree:
>
> **Article 34(3), first sentence (reporting):** Upon becoming aware of divulgence, etc. of personal information, the personal information controller shall, without delay, file a report with the Protection Commission or a specialized institution designated by Presidential Decree with respect to the matters provided in the subparagraphs of paragraph (1), as prescribed by Presidential Decree in consideration of the types of personal information, the process and scale of divulgence, etc., and other factors.

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
| **Data-breach notification (Art 34)**: on becoming aware of a divulgence, the controller notifies affected data subjects of the Art 34(1) matters without delay and reports without delay to the Protection Commission (PIPC) or a specialized institution designated by Presidential Decree, as prescribed by Presidential Decree (the PIPA Enforcement Decree, not held) in consideration of the types of personal information, the process and scale of divulgence, and other factors (Art 34(3)); for the status of that decree and the reporting period, see the Breach-reporting deadline line above. | library incident-response and breach-notification controls |
| **Access, correction/erasure, suspension (Arts 35, 36, 37)**: a data subject may request access (Art 35), correction or erasure of accessed information (Art 36), and suspension of processing (Art 37), subject to the statutory exceptions. | library data-subject-rights controls (`privacy/procedure-data-subject-rights-management.md`, `privacy/template-dsar-workflow.md`) |
| **Compensation and statutory damages (Arts 39, 39-2)**: a data subject suffering damage from a violation may claim compensation unless the controller proves no intent or negligence (Art 39(1)); where a data subject suffers damage from loss, theft, divulgence, forgery, alteration, or damage of their own personal information caused by the controller's intention or negligence, the court may award up to five times such damage, unless the controller proves the absence of intention or negligence (Art 39(3)); for those same compromise events the data subject may instead elect statutory damages up to the Art 39-2 cap. | *(Korea-specific liability; the library's disclosure-accuracy and security controls reduce the exposure)* |

## AI and privacy obligations

- **Right to explanation:** Data subjects may request an explanation of any decision made solely through automated means that significantly affects their rights or interests. The data controller must explain the criteria and logic applied and provide human review upon request.
- **Purpose limitation and data minimization:** Apply to AI training on personal data. Consent must be specific to the AI processing purpose.
- **High-risk processing:** PIPC guidance addresses higher-risk processing such as CCTV, biometric, and credit-assessment systems (proportionality and human oversight); that guidance is not held in the reference base, so an adopter confirms the current PIPC requirements directly. <!-- ref-absence: PIPC high-risk processing guidance | PIPC CCTV -->
- **Employment and profiling:** PIPC guidance is reported to address AI use in employment screening and credit decisions (proportionality and human oversight); that guidance is not held in the reference base, so an adopter confirms the current PIPC position directly. <!-- ref-absence: PIPC employment screening guidance | PIPC profiling -->
- **AI Basic Act:** South Korea's AI statute is covered in [`ai/jurisdictions/annex-ai-south-korea.md`](../../ai/jurisdictions/annex-ai-south-korea.md); among its basic principles, the held English translation of the AI Basic Act provides that affected persons are to be "provided with a clear and meaningful explanation of the key criteria and principles, used to derive the final AI outcomes, to the extent technically and reasonably possible" (Article 3(2)). In the held translation Article 3 is headed "Basic Principles and Obligations of the Nation"; the operator-level explanation duty is a separate article, Article 34(1)2, under which AI business operators providing high-impact AI or AI-based products and services establish and implement, as prescribed by Presidential Decree and to the extent technically feasible, a plan to provide explanations for AI-generated outputs, including the key criteria used to derive such outputs and an overview of the learning data used in the development and utilization of AI.

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

Figures below are taken, and triggers summarized, from the held KLRI English translation (Act No. 19234); these provisions were not compared against Act No. 21445 (in force since 11 September 2026), so an adopter confirms the current text directly.

- **Penalty surcharges (Article 64-2):** the PIPC "may impose a penalty surcharge on the relevant personal information controller within the scope not exceeding 3/100 of the total sales" (Article 64-2(1)), calculated "based on the gross sales net of the sales unrelated to the violation" (Article 64-2(2)); where no sales have been made or sales are impracticable to calculate, a surcharge "not exceeding two billion won may be imposed in cases prescribed by Presidential Decree" (Article 64-2(1) proviso). The triggers (Article 64-2(1)1 to 9) are processing in violation of Articles 15(1), 17(1), 18(1) and (2), or 19; processing a child's personal information (under 14) without the legal representative's consent (Article 22-2(1)); processing sensitive information without the data subject's consent (Article 23(1)1); processing personally identifiable information or resident registration numbers in violation of Articles 24(1) and 24-2(1); neglecting management, supervision, or education under Article 26(4), thereby causing the entrusted person to violate the Act; processing to uniquely identify an individual in violation of Article 28-5(1); cross-border transfer in violation of Article 28-8(1); failing to comply with a transfer-suspension order under Article 28-9(1); and loss, theft, divulgence, forgery, alteration, or damage of personal information, unless the controller has taken all the Article 29 safety measures. Where the controller refuses to submit sales calculation data or submits false data without good cause, the PIPC may calculate the sales based on the controller's gross sales (Article 64-2(3)), or may presume sales "based on the scale of personal information retained, accounting data such as financial statements, prices of products and services, and other data regarding the business state of a personal information controller with a size similar to that of the relevant personal information controller" (Article 64-2(3) proviso). The PIPC need not impose a surcharge where the person is objectively deemed unable to pay "due to insolvency, suspension of payment, capital impairment, etc." (Article 64-2(5)1), where there is good cause for the person to mistakenly believe that the conduct is not illegal (Article 64-2(5)2), where the violation is minor or the assessed surcharge is small (Article 64-2(5)3), or where a Presidential Decree ground exists on which the data subject has suffered no or minor damage (Article 64-2(5)4). The detailed calculation criteria and procedures are prescribed by Presidential Decree (Article 64-2(6)); that decree is not held in the reference base, so an adopter confirms the current calculation criteria directly. <!-- ref-absence: PIPA Enforcement Decree | Enforcement Decree of the Personal Information Protection Act -->
- **Criminal penalties (Articles 70 to 73):** the highest tier is "imprisonment with labor for not more than 10 years, or by a fine not exceeding 100 million won" (Article 70), for altering or erasing personal information processed by a public institution to disturb its processing and so cause suspension, paralysis, or other severe hardship of its work, and for obtaining personal information processed by third parties by fraud or other improper means and providing it to a third party for a profit-making or unjust purpose, or abetting or arranging such conduct. Article 71 sets "imprisonment with labor for not more than five years, or by a fine not exceeding 50 million won" for violations including providing personal information to a third party without the data subject's consent in violation of Article 17(1)1 where Article 17(1)2 is not applicable, together with a person who knowingly receives such personal information (Article 71, subparagraph 1), out-of-purpose use or provision (Article 18(1) and (2)), and processing sensitive information (Article 23(1)) or personally identifiable information (Article 24(1)) in violation of the Act. Article 72 sets imprisonment with labor for not more than three years or a fine not exceeding 30 million won, and Article 73(1) sets imprisonment with labor for not more than two years or a fine not exceeding 20 million won, for lower-tier offences. Under the Article 74 joint penalty provisions, where the representative of a corporation, or an agent or employee of, or any other person employed by, a corporation or an individual commits an offence in connection with the business affairs of the corporation or individual, the corporation or individual is also punished, by "a fine not exceeding 70 million won" for an Article 70 offence (Article 74(1)) and by "a fine prescribed in the relevant Article" for an Article 71 to 73 offence (Article 74(2)), except where it "has not been negligent in taking due care and supervisory activities concerning the relevant affairs to prevent such offense" (Article 74(1) and (2) provisos).
- **Administrative fines (Article 75):** Article 75 sets administrative fines in four tiers, not exceeding 50 million won, 30 million won, 20 million won, and 10 million won (Article 75(1) to (4)).

Article 26(8) applies Articles 34 and 64-2, among others, mutatis mutandis to the person entrusted with processing, and each Article 64-2(1) trigger other than subparagraph 5 (the entrusting controller's own Article 26(4) management, supervision, or education failure) states that it includes application mutatis mutandis under Article 26(8), with subparagraphs 7 and 8 also extending through Article 28-11:

> **Article 26(8):** Articles 15 through 18, 21, 22, 22-2, 23, 24, 24-2, 25, 25-2, 27, 28, 28-2 through 28-5, 28-7 through 28-11, 29, 30, 30-2, 31, 33, 34, 34-2, 35, 35-2, 36, 37, 37-2, 38, 59, 63, 63-2, and 64-2 shall apply mutatis mutandis to outsourcees. In such cases, "personal information controller" shall be construed as "person entrusted".

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
