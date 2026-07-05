# Brazil Privacy Regulatory Requirements

**Document Title:** Brazil Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.1\
**Date:** 2026-07-05\
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
- **Regulatory authority:** Brazilian Data Protection Authority (ANPD). Restructured as the Agência Nacional de Proteção de Dados, a regulatory agency (agência reguladora), by Lei No. 15.352/2026 (converting Medida Provisória No. 1.317/2025, which amended LGPD Articles 5 and 55-A); previously the Autoridade Nacional de Proteção de Dados. (The 2025 to 2026 restructuring instruments, Lei No. 15.352/2026, Medida Provisória No. 1.317/2025, and the amended LGPD Article 55-A, postdate this library's independently verified reference sources and are pending primary-source verification against the official record at Planalto; confirm the current designation before relying on it.)

---

## AI and privacy obligations

- **Lawful basis (Article 7):** Processing by AI systems requires one of ten lawful bases including consent, legitimate interest, contract performance, legal obligation, and research in the public interest.
- **Sensitive personal data (Article 11):** AI systems processing health, biometric, racial or ethnic origin, religious belief, political opinion, sexual orientation, genetic, or children's data require consent or another specific Article 11 basis. Consent must be specific, prominent, and separate.
- **Automated decisions (Article 20):** Data subjects have the right to request review of decisions made solely on the basis of automated processing that affect their interests, including decisions defining personal, professional, consumer, or credit profiles. The controller must provide clear and adequate information about the criteria and procedures used.
- **Data-subject requests (Articles 18 to 19):** Article 18 rights (confirmation of processing, access, correction, anonymization or deletion, portability, and others) must be answered on two statutory tracks under Article 19: confirmation-of-existence and access requests are met either immediately in a simplified format, or by a complete declaration within 15 days from the data subject's request. Other Article 18 rights carry no fixed day-count in the Act; adopting organizations set an internal service level and record it in their DSR procedure.
- **Records of processing (Article 37):** The controller and the processor must keep records of the personal data processing operations they carry out, especially when the processing is based on legitimate interest. This is the LGPD's ROPA obligation, the analogue of GDPR Article 30.
- **Data Protection Officer (DPO) (Articles 41 to 43):** Controllers must designate a DPO (Encarregado). Contact details must be published.
- **DPIA (Article 38):** The ANPD may require a Data Protection Impact Assessment (RIPD) for high-risk processing, including processing based on legitimate interest and large-scale processing of sensitive data.
- **Legitimate interest (Article 10):** Controllers relying on legitimate interest for AI processing must conduct a balancing test and, when requested by the ANPD, provide a DPIA.
- **Breach notification (Articles 48 to 49):** The controller must notify the ANPD and affected data subjects of a security incident that may cause relevant risk or harm, within a reasonable period as defined by the national authority. ANPD Resolution CD/ANPD No. 15/2024 (the Security Incident Communication Regulation) operationalizes this as 3 business days from awareness that the incident affected personal data, for notification to both the ANPD and affected data subjects, with staged communication permitted (complementary information within 20 business days) and deadlines doubled for small-scale agents; Resolution CD/ANPD No. 2 is the small-agents regulation, not the breach-notification rule. (Resolution CD/ANPD No. 15/2024 and Resolution CD/ANPD No. 2 are pending primary-source verification against the ANPD's official publication.)
- **ANPD guidance (2024 to 2025):** ANPD has published guidance stating that AI training using personal data requires a specific lawful basis and that data minimization and purpose limitation apply. ANPD has signalled intent to issue sector-specific AI guidance.

---

## Cross-border transfer mechanisms

International transfers of personal data from Brazil are permitted only when (LGPD Articles 33 to 36):

1. **Adequacy:** Transfer to a country with adequate protection as determined by the ANPD. As of 2025, the ANPD has not yet issued adequacy decisions.
2. **Standard Contractual Clauses:** Transfer subject to ANPD-approved standard contractual clauses (Resolution CD/ANPD No. 19/2023; pending primary-source verification).
3. **Binding Corporate Rules:** Intra-group transfers subject to BCRs approved by the ANPD.
4. **Regulatory cooperation:** Transfer to countries where cooperation agreements exist between the ANPD and the foreign data protection authority.
5. **Derogations (Article 33, II):** Transfers with explicit consent, necessary for contract performance, to protect life, for public health, or for fulfilment of legal obligation.

ANPD-approved standard contractual clauses (Resolution CD/ANPD No. 19/2023) are the primary mechanism for routine international transfers from Brazil until adequacy decisions are issued. (Resolution CD/ANPD No. 19/2023 is pending primary-source verification against the ANPD's official publication.)

---

## Enforcement and fines

- **Simple fine (Article 52):** Up to 2% of the revenue of the private legal entity, group, or conglomerate in Brazil in its last fiscal year (excluding taxes), up to a maximum of BRL 50 million per violation.
- **Daily fine:** To compel cessation of the violation, up to BRL 50 million in total.
- Additional sanctions: warning; obligation to publish the incident; temporary blocking or deletion of data; partial or total suspension of the database; partial or total prohibition of data processing activities.
- ANPD began imposing administrative sanctions in 2023. Early enforcement has focused on breach notification and consent practices.

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
