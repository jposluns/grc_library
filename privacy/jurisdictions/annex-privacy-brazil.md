# Brazil Privacy Regulatory Requirements

**Document Title:** Brazil Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.7\
**Date:** 2026-07-22\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/annex-privacy-jurisdiction-index.md`](../annex-privacy-jurisdiction-index.md), [`privacy/policy-privacy-and-data-governance.md`](../policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/jurisdictions/annex-privacy-brazil.md`](annex-privacy-brazil.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex defines privacy and AI regulatory requirements applicable to the processing of personal data in Brazil under the Lei Geral de Proteção de Dados Pessoais (LGPD). It supplements the Privacy and Data Governance Policy and the Privacy Impact and Cross-Border Transfer Procedure.

---

## Applicable laws and regulatory authorities

- **Lei Geral de Proteção de Dados Pessoais (LGPD)**: Law No. 13,709/2018, as amended by Law No. 13,853/2019, in force September 2020. Brazil's comprehensive data protection law, closely modelled on GDPR. Applies to any processing of personal data of individuals located in Brazil, regardless of where the processor is located, provided that the processing takes place in Brazil, the purpose of processing is offering goods or services in Brazil, or the personal data was collected in Brazil.
- **Brazilian Internet Act (Marco Civil da Internet)**: Law No. 12,965/2014. Establishes principles, rights, and duties for internet use in Brazil, including data protection principles for connection and application providers.
- **Regulatory authority:** Brazilian Data Protection Authority (ANPD). Restructured as the Agência Nacional de Proteção de Dados, a regulatory agency (agência reguladora), by Lei No. 15.352/2026 (of 25 February 2026, converting Medida Provisória No. 1.317/2025, which gave new wording to LGPD Articles 5 and 55-A); previously the Autoridade Nacional de Proteção de Dados. (Verified against the Planalto primary sources on 2026-07-07: Lei No. 15.352/2026 and Medida Provisória No. 1.317/2025 both confirmed on planalto.gov.br, and LGPD Article 55-A confirmed in the consolidated Lei No. 13.709/2018 text.)

---

## AI and privacy obligations

- **Lawful basis (Article 7):** Processing by AI systems requires one of ten lawful bases including consent, legitimate interest, contract performance, legal obligation, and research in the public interest.
- **Sensitive personal data (Article 11):** AI systems processing health, biometric, racial or ethnic origin, religious belief, political opinion, sexual orientation, genetic, or children's data require consent or another specific Article 11 basis. Consent must be specific, prominent, and separate.
- **Automated decisions (Article 20):** Data subjects have the right to request review of decisions made solely on the basis of automated processing that affect their interests, including decisions defining personal, professional, consumer, or credit profiles. The controller must provide clear and adequate information about the criteria and procedures used.
- **Data-subject requests (Articles 18 to 19):** Article 18 rights (confirmation of processing, access, correction, anonymization or deletion, portability, and others) must be answered on two statutory tracks under Article 19: confirmation-of-existence and access requests are met either immediately in a simplified format, or by a complete declaration within 15 days from the data subject's request. Other Article 18 rights carry no fixed day-count in the Act; adopting organizations set an internal service level and record it in their DSR procedure.
- **Records of processing (Article 37):** The controller and the processor must keep records of the personal data processing operations they carry out, especially when the processing is based on legitimate interest. This is the LGPD's ROPA obligation, the analogue of GDPR Article 30.
- **Data Protection Officer (DPO) (Articles 41 to 43):** Controllers must designate a DPO (Encarregado). Contact details must be published. Resolution CD/ANPD No. 18/2024 (of 16 July 2024, the Regulation on the activities of the encarregado) is the ANPD rule operationalizing the appointment, definition, attributions, and performance of the encarregado under LGPD Article 41: who may serve, how the designation is formalized, conflict-of-interest limits, whether a legal entity may serve, and when a substitute is required. (Resolution CD/ANPD No. 18/2024 was verified against the ANPD's official regulations publication on 2026-07-13, confirming the 16 July 2024 enactment and the 17 July 2024 Diário Oficial da União publication; it remains in force with no amendment.)
- **DPIA (Article 38):** The ANPD may require a Data Protection Impact Assessment (RIPD) for high-risk processing, including processing based on legitimate interest and large-scale processing of sensitive data.
- **Legitimate interest (Article 10):** Controllers relying on legitimate interest for AI processing must conduct a balancing test and, when requested by the ANPD, provide a DPIA.
- **Breach notification (Articles 48 to 49):** The controller must notify the ANPD and affected data subjects of a security incident that may cause relevant risk or harm, within a reasonable period as defined by the national authority. ANPD Resolution CD/ANPD No. 15/2024 (the Security Incident Communication Regulation) operationalizes this as 3 business days from awareness that the incident affected personal data, for notification to both the ANPD and affected data subjects, with staged communication permitted (complementary information within 20 business days) and deadlines doubled for small-scale agents; Resolution CD/ANPD No. 2/2022 is the small-agents regulation, not the breach-notification rule. (Resolution CD/ANPD No. 15/2024, dated 24 April 2024, and Resolution CD/ANPD No. 2/2022, dated 27 January 2022, were verified against the ANPD's official publication on 2026-07-07, confirming the 3-business-day rule and the 20-business-day complementary window; the "deadlines doubled for small-scale agents" sub-clause was confirmed against the Resolution 15/2024 text on 2026-07-08: Article 6 §8 doubles both the ANPD-notification deadline (3 to 6 business days) and the 20-business-day complementary-information window (to 40), and Article 9 §6 doubles the data-subject-notification deadline (3 to 6 business days), the text reading "contados em dobro para os agentes de pequeno porte" (the small-scale-agent definition being that of Resolution CD/ANPD No. 2/2022). This was confirmed against the primary Diário Oficial da União text of Resolution CD/ANPD No. 15/2024 (DOU 26 April 2024, Edição 81, Seção 1, Página 114), now held in the reference base: Article 6 §8 reads "Os prazos constantes no caput e no § 3º deste artigo são contados em dobro para os agentes de pequeno porte" and Article 9 §6 the equivalent for the data-subject-notification deadline.)
- **ANPD guidance (2024 to 2025):** ANPD has published guidance stating that AI training using personal data requires a specific lawful basis and that data minimization and purpose limitation apply. ANPD has signalled intent to issue sector-specific AI guidance.

---

## Cross-border transfer mechanisms

International transfers of personal data from Brazil are permitted only when (LGPD Articles 33 to 36):

1. **Adequacy:** Transfer to a country or international organization the ANPD recognizes as providing an adequate level of protection (LGPD Article 33, item I). The ANPD issued its first adequacy decision in Resolution CD/ANPD No. 32 of 26 January 2026, recognizing the European Union (extending to all EU Member States, the three European Free Trade Association states in the European Economic Area (Iceland, Liechtenstein, Norway), and the institutions, bodies, and agencies of the European Union); the decision is subject to reassessment within four years.
2. **Standard Contractual Clauses:** Transfer subject to ANPD-approved standard contractual clauses (Resolution CD/ANPD No. 19/2024, of 23 August 2024, the International Data Transfer Regulation).
3. **Binding Corporate Rules:** Intra-group transfers subject to BCRs approved by the ANPD.
4. **Regulatory cooperation:** Transfer to countries where cooperation agreements exist between the ANPD and the foreign data protection authority.
5. **Derogations (Article 33, II):** Transfers with explicit consent, necessary for contract performance, to protect life, for public health, or for fulfilment of legal obligation.

ANPD-approved standard contractual clauses (Resolution CD/ANPD No. 19/2024) remain the primary mechanism for routine international transfers to destinations not covered by an adequacy decision; the first adequacy decision (Resolution CD/ANPD No. 32 of 26 January 2026, recognizing the European Union and the EFTA states in the European Economic Area) provides an alternative route for transfers to those recognized destinations. (Resolution CD/ANPD No. 19/2024, of 23 August 2024, was verified against the ANPD's official international-data-transfer publication on 2026-07-07; the earlier "No. 19/2023" designation was a year error, corrected here.)

---

## Enforcement and fines

- **Simple fine (Article 52):** Up to 2% of the revenue of the private legal entity, group, or conglomerate in Brazil in its last fiscal year (excluding taxes), up to a maximum of BRL 50 million per violation.
- **Daily fine:** To compel cessation of the violation, up to BRL 50 million in total.
- Additional sanctions: warning; obligation to publish the incident; temporary blocking or deletion of data; partial or total suspension of the database; partial or total prohibition of data processing activities.
- **Fine dosimetry (Resolution CD/ANPD No. 4/2023):** The Article 52 percentages and ceilings above are the statutory maximums, not the method for setting a given fine. Resolution CD/ANPD No. 4/2023 (of 24 February 2023, the Regulation on Dosimetry and Application of Sanctions) establishes the parameters and criteria the ANPD applies to calculate the base value of a fine sanction and to apply the Article 52 sanctions; it amended the fiscalization-and-sanctioning-process regulation approved by Resolution CD/ANPD No. 1/2021. (Resolution CD/ANPD No. 4/2023 was verified against the ANPD's official publication on 2026-07-13: published in the Diário Oficial da União on 27 February 2023, amending Resolution No. 1/2021 of 28 October 2021; in force.)
- ANPD began imposing administrative sanctions in 2023. Early enforcement has focused on breach notification and consent practices.

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
