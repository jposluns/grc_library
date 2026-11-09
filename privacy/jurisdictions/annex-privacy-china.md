# China Privacy Regulatory Requirements

**Document Title:** China Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.18\
**Date:** 2026-10-26\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/annex-privacy-jurisdiction-index.md`](../annex-privacy-jurisdiction-index.md), [`privacy/policy-privacy-and-data-governance.md`](../policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/jurisdictions/annex-privacy-china.md`](annex-privacy-china.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex defines privacy and AI regulatory requirements applicable to the processing of personal data in China under the Personal Information Protection Law (PIPL), Cybersecurity Law (CSL), and Data Security Law (DSL), and the Generative AI Regulations. It supplements the Privacy and Data Governance Policy and the Privacy Impact and Cross-Border Transfer Procedure.

---

## Applicable laws and regulatory authorities

- **Personal Information Protection Law (PIPL)**: Effective 2021-11-01. China's comprehensive personal information protection law. Applies to processing of personal information of individuals in China and to offshore processing of personal information of Chinese individuals for the purpose of providing goods or services or analyzing behaviour.
- **Cybersecurity Law (CSL)**: Effective 2017-06-01 (CSL Art. 81); amended by the NPC Standing Committee decision of 28 October 2025, in force 1 January 2026 (本决定自2026年1月1日起施行, the decision's closing clause; promulgated by Presidential Order No. 61), which also renumbered the articles; CSL article numbers in this annex follow the amended text. Governs network security obligations for network operators (网络运营者, which the law defines as the owners and managers of networks and network service providers, CSL Art. 78). Requires network operators to perform security protection obligations under the requirements of the cybersecurity multi-level protection scheme (网络安全等级保护制度, the scheme this annex calls MLPS) (CSL Art. 23). Requires critical information infrastructure operators to store within China the personal information and important data they collect and generate in their operations within China; where provision abroad is truly necessary for business needs, a security assessment is conducted under measures jointly formulated by the national cybersecurity and informatization department and relevant departments of the State Council, unless laws or administrative regulations provide otherwise (CSL Art. 39). The CSL's domestic-storage duty names critical information infrastructure operators only; it is not a general localization duty for every network operator (for transfers by other handlers, see "Cross-border transfer mechanisms" below). (English rendering of the Chinese text, which is authoritative; its clause 国家网信部门会同国务院有关部门制定 is the same Chinese wording the DSL translation renders as "jointly formulated by the national cybersecurity and informatization department and relevant departments of the State Council", DSL Art. 31.)
- **Data Security Law (DSL)**: Effective 2021-09-01. Establishes a data security protection system based on data classification and grading. Introduces concepts of "important data" and "core national data" with associated localization and security assessment requirements.
- **Generative AI Regulations (Interim Measures for the Management of Generative AI Services, effective August 2023):** Regulates provision of generative AI services to the public in China. Requires pre-deployment security assessments, content moderation, AI-generated content labelling, transparency about training data, and real-name user registration.
- **Provisions on Promoting and Regulating the Cross-Border Flow of Data (CAC, effective 22 March 2024):** Implementing regulation under PIPL and DSL that revises personal-data export thresholds, introduces safe-harbor exemptions for low-volume and contract-performance transfers, and extends the validity of a CAC security assessment from two years to three years. See "Cross-border transfer mechanisms" below.
- **Algorithm Recommendation Regulations (effective March 2022):** Regulates use of recommendation algorithms in online information services, requiring transparency, user control, and labelling of algorithm-driven content.
- **Deep Synthesis Regulations (effective January 2023):** Regulates provision of deep synthesis technology services (deepfakes), requiring content labelling and prohibiting disinformation generation.
- **Regulatory authority:** Cyberspace Administration of China (CAC) as the coordinating regulator, with relevant State Council departments supervising within their respective scopes (PIPL Art. 60); in practice these include SAMR, MIIT, PBOC, and sectoral authorities (the named agencies reflect administrative practice, not an enumeration in the held statute).

---

## AI and privacy obligations

### PIPL and AI

- **Lawful basis (Article 13):** Processing requires one of: consent; where necessary to conclude or perform a contract to which the individual is a party, or to conduct human-resources management under lawfully formulated labour rules and lawfully concluded collective contracts; where necessary to perform a statutory duty or obligation; where necessary to respond to a public-health emergency or to protect a natural person's life, health, or property in an emergency; processing within a reasonable scope to carry out news reporting, public-opinion supervision, and other such activities in the public interest; processing within a reasonable scope, in accordance with this Law, of personal information the individual has disclosed or that has otherwise been lawfully disclosed; or other circumstances provided by laws and administrative regulations. PIPL has no general legitimate-interests basis (unlike the GDPR). Consent must be fully informed, voluntary, and explicit (Article 14).
- **Sensitive personal information (Articles 28 to 32):** Separate and express consent required. Sensitive categories include biometric identification, religious beliefs, specially-designated status, medical health, financial accounts, whereabouts/location, and personal information of minors under 14.
- **Automated decision-making (Article 24):** Organizations must ensure that transparency and fairness are upheld. No unreasonable differential treatment of individuals in terms of transaction price or conditions. Individuals have the right to receive an explanation and to opt out of automated decision-making significantly affecting their interests.
- **Person in charge of personal information protection (Article 52):** Large-scale personal information processors must designate a responsible person whose name and contact information must be disclosed publicly.
- **DPIA (Article 55):** Required before: processing sensitive personal information; using personal information for automated decision-making; entrusting, sharing, or publicly disclosing personal information; cross-border transfers; and processing activities with significant impact on personal rights. The impact-assessment report and processing records must be retained for at least three years (Article 56).

### Generative AI regulations

- **Pre-deployment security assessment:** Required for public-facing generative AI services meeting CAC thresholds.
- **Training data obligations:** Must be lawfully acquired; no personal information without consent; intellectual property rights must be respected.
- **Content moderation:** Mechanisms must prevent generation of content prohibited by Chinese law.
- **Labelling:** All AI-generated content must be labelled per CAC standards.
- **Real-name registration:** Providers must verify user identity.
- **Incident reporting:** The PIPL baseline duty for personal information incidents applies: where a personal information leak, distortion, or loss has occurred or may occur, the handler must notify the departments fulfilling personal information protection duties and responsibilities and the individuals (PIPL Art. 57; the trigger is rendered from the Chinese text 发生或者可能发生, which is authoritative, where the held unofficial English translation reads "occurs or might have occurred"). The handler is permitted not to notify individuals where its measures are able to effectively avoid harm, but those departments may require it to notify individuals where they believe harm may have been created (PIPL Art. 57). Those departments include the State cybersecurity and informatization department (国家网信部门, the same Chinese term the DSL translation's editor's note describes as a common reference to the Cyberspace Administration of China, CAC; the PIPL does not name the CAC) (PIPL Art. 60). For data security incidents, the Data Security Law requires the handler to take methods to address them immediately, "promptly notifying users and reporting to relevant departments in charge as provided" (DSL Art. 29). For personal information incidents, the Cybersecurity Law requires network operators (网络运营者, which the law defines as the owners and managers of networks and network service providers, CSL Art. 78), where a personal information leak, damage, or loss has occurred or may occur, to take remedial measures immediately, promptly notifying users and reporting to relevant departments in charge as provided (CSL Art. 44, so numbered since the renumbering in force 1 January 2026 under the amending decision of 28 October 2025, which lists no change to this duty; English rendering of the Chinese text, which is authoritative; its clause 按照规定及时告知用户并向有关主管部门报告 is the same Chinese wording the DSL translation renders as "promptly notifying users and reporting to relevant departments in charge as provided"). Where the incident also endangers network security, the Cybersecurity Law also requires those network operators to report to the relevant departments in charge as provided (CSL Art. 27; English rendering of the Chinese text, which is authoritative). The CAC has issued National Cybersecurity Incident Reporting Measures (国家网络安全事件报告管理办法), which are not held in the reference base, so an adopter confirms directly their in-force date, any reporting time limits, and whether they apply. <!-- ref-absence: National Cybersecurity Incident Reporting Measures --> The Interim Measures for the Management of Generative Artificial Intelligence Services are not held in the reference base, so an adopter confirms any incident-reporting duties they add directly. <!-- ref-absence: Interim Measures for the Management of Generative Artificial Intelligence Services -->

### Cybersecurity law / MLPS

- The State implements the cybersecurity multi-level protection scheme (国家实行网络安全等级保护制度). Where an organization operating an AI system that processes personal information is a network operator (CSL Art. 78), it must perform security protection obligations under the scheme's requirements: formulating internal security management rules and operating procedures, designating a person responsible for network security and implementing network security protection responsibility; taking technical measures against computer viruses, network attacks, network intrusions and other conduct endangering network security; taking technical measures to monitor and record network operating status and network security incidents, and retaining the relevant network logs as provided for no less than six months; taking measures such as data classification and backup and encryption of important data; and other obligations under laws and administrative regulations (CSL Art. 23; English rendering of the Chinese text, which is authoritative). Critical information infrastructure receives key protection on the basis of the scheme (CSL Art. 33).
- The CSL does not define the scheme's protection levels, assign a system or a volume of personal information to a level, or name a level-based assessment, so the held text does not settle which level an AI system falls in or what assessment, if any, that level requires; an adopter confirms both directly.

---

## Cross-border transfer mechanisms

PIPL (Articles 38 to 43) permits cross-border transfer only through one of three mechanisms: CAC security assessment, the PIPL Standard Contract, or third-party certification. The CAC's **Provisions on Promoting and Regulating the Cross-Border Flow of Data**, issued 22 March 2024 with immediate effect, revised the thresholds and introduced safe-harbor exemptions. The thresholds below reflect the post-March-2024 regime.

The thresholds are evaluated on a cumulative calendar-year basis starting 1 January.

1. **Safe-harbor exemptions (no mechanism required):** A non-Critical Information Infrastructure Operator (CIIO) transferring fewer than 100,000 individuals' non-sensitive personal data in the calendar year is exempt. Specific exemptions are also available for transfers necessary for HR administration under a labour contract or employment policy, transfers necessary for the performance of a contract with the data subject (such as cross-border commerce, money remittance, account opening, travel booking, and visa services), and transfers necessary in cross-border emergencies for the protection of life, health, or property.

2. **PIPL Standard Contract plus filing:** Required for non-CIIO transfers of non-sensitive personal data of 100,000 to fewer than 1,000,000 individuals in the calendar year, or any transfer of sensitive personal data of fewer than 10,000 individuals. The controller must conduct a PIA, sign the CAC-published Standard Contract with the recipient, and file the signed contract together with the PIA with the provincial-level CAC.

3. **CAC Security Assessment (mandatory):** Required for any transfer by a CIIO; any transfer of "important data" (under the DSL); any non-CIIO transfer of non-sensitive personal data of 1,000,000 or more individuals in the calendar year; or any transfer of sensitive personal data of 10,000 or more individuals in the calendar year. The 2024 Provisions extend the validity of a passed security assessment from two years to three years.

4. **Third-party certification:** From a recognized professional institution as specified by the CAC; primarily applicable to intra-group transfers.

**Important data:** Transfer of "important data" under the DSL is subject to the security assessment regardless of volume thresholds.

**Practical note:** The cross-border transfer regime is among the most stringent globally. The March 2024 Provisions materially relaxed the lower thresholds (the safe-harbor under 100,000 individuals removed a substantial number of routine transfers from the formal mechanism set) but did not change the security-assessment threshold for CIIOs or large transfers. Early engagement with CAC requirements remains essential for any international data transfer programme involving China-origin personal information.

---

## Enforcement and fines

### PIPL

- Warning, correction order, confiscation of illegal gains, or suspension of services.
- Fines: Up to RMB 50 million or 5% of the previous year's annual revenue for serious violations.
- Responsible persons may be fined up to RMB 1 million and prohibited from serving in senior roles.

### CSL

The CSL provisions below are an English rendering of the Chinese text, which is authoritative.

- Fixed-amount fines reach RMB 10 million (一千万元) under the CSL as amended with effect from 1 January 2026 (CSL Art. 61 para. 3; Art. 69 para. 2). Two fines are set as multiples, not fixed amounts, and have no fixed ceiling: one to ten times the purchase amount for a critical information infrastructure operator that uses network products or services that have not undergone, or have failed, security review (CSL Art. 67), and one to five times the illegal gains, where those gains are RMB 100,000 or more, for selling or providing critical network equipment or specialized cybersecurity products that have not undergone, or have failed, the required certification or testing (CSL Art. 63). A network operator that fails its multi-level protection duties (Art. 23) or its Art. 27 duties (formulating a network security incident response plan; promptly dealing with security risks such as system vulnerabilities, computer viruses, network attacks and network intrusions; and, when an incident endangering network security occurs, immediately activating the plan, taking corresponding remedial measures and reporting to the relevant departments in charge as provided) may be fined RMB 10,000 to 50,000, and is fined RMB 50,000 to 500,000 where it refuses to correct or harm to network security results (CSL Art. 61 para. 1); a critical information infrastructure operator that fails its Arts. 35, 36, 38 or 40 duties may be fined RMB 50,000 to 100,000, and is fined RMB 100,000 to 1 million where it refuses to correct or harm to network security results (CSL Art. 61 para. 2); either is fined RMB 500,000 to 2 million where serious harm to network security, such as a large volume of data leaked, results, and RMB 2 million to 10 million where especially serious harm, such as the loss of main functions of critical information infrastructure, results (CSL Art. 61 para. 3). A network operator that fails to deal with information that laws and administrative regulations prohibit from being published or transmitted, as Art. 49 requires or as the relevant departments require under Art. 52, may be fined RMB 50,000 to 500,000, and is fined RMB 500,000 to 2 million where it refuses to correct or the circumstances are serious, and RMB 2 million to 10 million where the impact or consequences are especially serious (CSL Art. 69 paras. 1 and 2).
- Directly responsible persons in charge and other directly responsible personnel are fined separately, up to RMB 1 million at the highest tiers (CSL Art. 61 para. 3; Art. 69 para. 2).
- Violations of the CSL's personal information provisions (Art. 24 para. 3 and Arts. 43 to 45, including the Art. 44 incident duty) that infringe personal information rights and interests, and of the critical information infrastructure operator domestic-storage duty (Art. 39) are handled and penalized under the relevant laws and administrative regulations (依照有关法律、行政法规的规定处理、处罚), so the CSL itself sets no fine amount for them (CSL Art. 71, as merged and amended by item 12 of the amending decision); network operators processing personal information must comply with the CSL, the Civil Code and the PIPL, among other laws and administrative regulations (CSL Art. 42 para. 2; for PIPL fines, see above).
- Suspension of related business, suspension of operations for rectification, and revocation of related business permits or business licences may be ordered where the circumstances are serious (情节严重) for selling or providing critical network equipment or specialized cybersecurity products that have not undergone, or have failed, the required certification or testing (Art. 63); where there is a refusal to correct (拒不改正) or the circumstances are serious for real-identity failures (Art. 64), for conducting cybersecurity certification, testing or risk assessment, or publishing cybersecurity information such as system vulnerabilities, in breach of Art. 28 (Art. 65), and for prohibited-information failures (Art. 69 para. 1); and are ordered for prohibited-information failures with especially serious impact or consequences (Art. 69 para. 2). Arts. 64, 65 and 69 add closure of websites or applications on the same conditions. None of these provisions is limited to critical information infrastructure operators. A critical information infrastructure operator that uses network products or services that have not undergone, or have failed, security review is ordered to correct within a time limit, stop using them and eliminate the effect on national security, and is fined one to ten times the purchase amount (CSL Art. 67).
- Where the Administrative Penalty Law's circumstances for a lighter, mitigated or no penalty exist, the penalty is lightened, mitigated or not imposed accordingly (CSL Art. 73, added by item 13 of the amending decision).

### DSL

The DSL provisions below are drawn from an unofficial English translation; the Chinese text is authoritative, so an adopter confirms the amounts against it before relying on them.

- An organization or individual conducting data handling activities that fails its data security protection duties under DSL Arts. 27, 29 or 30 may be fined RMB 50,000 to 500,000, and is fined RMB 500,000 to 2 million where it refuses to correct or serious consequences, such as a large-scale data leak, result (DSL Art. 45 para. 1). Where core national data management systems are violated, endangering national sovereignty, security or development interests, the fine is RMB 2 million to 10 million (DSL Art. 45 para. 2, as the unofficial translation numbers it; the reproduction of the Chinese text on the translation's page prints Art. 44 between Art. 45's first paragraph and this one).
- Providing important data abroad in breach of Art. 31 may be fined RMB 100,000 to 1 million (DSL Art. 46). The held translation's Art. 46 text appears incomplete: its fine on directly responsible personnel, RMB 100,000 to 1 million, is the same range as its fine for the breach, where Art. 45 para. 1, Art. 47 and Art. 48 set RMB 10,000 to 100,000 for such personnel at their lowest tier; its text reads "a a fine"; and the unofficial reproduction of the Chinese text on the translation's page, which has a known article-order defect (see Art. 45 para. 2 above), sets, in its Art. 46, a personnel fine of RMB 10,000 to 100,000 (一万元以上十万元以下) and a further tier where the circumstances are serious (情节严重的，处一百万元以上一千万元以下罚款, a fine of RMB 1 million to 10 million) that the translation does not render. An adopter confirms the Art. 46 tiers against the authoritative Chinese text before relying on them.
- An institution providing data transaction intermediary services that fails its Art. 33 duties is fined one to ten times its unlawful gains, a multiple with no fixed ceiling, or RMB 100,000 to 1 million where there are no unlawful gains or they are less than RMB 100,000 (DSL Art. 47).
- Refusing to cooperate with the obtaining of data under Art. 35 is fined RMB 50,000 to 500,000 (DSL Art. 48 para. 1). Providing data to foreign justice or law enforcement institutions without approval, in breach of Art. 36, may be fined RMB 100,000 to 1 million, and is fined RMB 1 million to 5 million where serious consequences result (DSL Art. 48 para. 2).
- Directly responsible management personnel and other directly responsible personnel are also subject to fines (DSL Art. 45 para. 1; Arts. 46 to 48).

### Generative AI regulations

- Suspension of services, fines, and criminal referral for serious violations. Reports of CAC enforcement against generative-AI service providers are not corroborated by held sources, so an adopter confirms the current enforcement position directly.

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
