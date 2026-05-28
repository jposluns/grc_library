# China Privacy Regulatory Requirements

**Document Title:** China Privacy Regulatory Requirements 
**Document Type:** Annex 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Privacy Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`privacy/jurisdictions/annex-privacy-jurisdiction-index.md`](../jurisdictions/annex-privacy-jurisdiction-index.md), [`privacy/policy-privacy-and-data-governance.md`](../policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md) 
**Classification:** Public 
**Category:** Privacy 
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change 
**Repository Path:** [`privacy/jurisdictions/annex-privacy-china.md`](annex-privacy-china.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal

---

## Purpose

This annex defines privacy and AI regulatory requirements applicable to the processing of personal data in China under the Personal Information Protection Law (PIPL), Cybersecurity Law (CSL), and Data Security Law (DSL), and the Generative AI Regulations. It supplements the Privacy and Data Governance Policy and the Privacy Impact and Cross-Border Transfer Procedure.

---

## Applicable laws and regulatory authorities

- **Personal Information Protection Law (PIPL)**: Effective 2021-11-01. China's comprehensive personal information protection law. Applies to processing of personal information of individuals in China and to offshore processing of personal information of Chinese individuals for the purpose of providing goods or services or analyzing behaviour.
- **Cybersecurity Law (CSL)**: Effective 2017-06-01. Governs network security obligations for network operators. Requires compliance with Multi-Level Protection Scheme (MLPS), implementation of security measures, and localization of personal information and important data collected in China.
- **Data Security Law (DSL)**: Effective 2021-09-01. Establishes a data security protection system based on data classification and grading. Introduces concepts of "important data" and "core state data" with associated localization and security assessment requirements.
- **Generative AI Regulations (Interim Measures for the Management of Generative AI Services, effective August 2023):** Regulates provision of generative AI services to the public in China. Requires pre-deployment security assessments, content moderation, AI-generated content labelling, transparency about training data, and real-name user registration.
- **Algorithm Recommendation Regulations (effective March 2022):** Regulates use of recommendation algorithms in online information services, requiring transparency, user control, and labelling of algorithm-driven content.
- **Deep Synthesis Regulations (effective January 2023):** Regulates provision of deep synthesis technology services (deepfakes), requiring content labelling and prohibiting disinformation generation.
- **Regulatory authority:** Cyberspace Administration of China (CAC) as primary regulator; concurrent jurisdiction with SAMR, MIIT, PBOC, and sectoral authorities.

---

## AI and privacy obligations

### PIPL and AI

- **Lawful basis (Article 13):** Processing requires one of: consent; contract performance or HR management; legal obligation; vital interests; public interest or journalism; or other legitimate interests (narrower than GDPR). Consent must be voluntary, specific, informed, and unambiguous.
- **Sensitive personal information (Articles 28 to 32):** Separate and express consent required. Sensitive categories include biometric identification, religious beliefs, specially-designated status, medical health, financial accounts, whereabouts/location, and personal information of minors under 14.
- **Automated decision-making (Article 24):** Organizations must ensure that transparency and fairness. No unreasonable differential treatment of individuals in terms of transaction price or conditions. Individuals have the right to receive an explanation and to opt out of automated decision-making significantly affecting their interests.
- **Person in charge of personal information protection (Article 52):** Large-scale personal information processors must designate a responsible person whose name and contact information must be disclosed publicly.
- **DPIA (Article 55):** Required before: processing sensitive personal information; using personal information for automated decision-making; entrusting, sharing, or publicly disclosing personal information; cross-border transfers; and processing activities with significant impact on personal rights. Records must be retained for at least three years.

### Generative AI regulations

- **Pre-deployment security assessment:** Required for public-facing generative AI services meeting CAC thresholds.
- **Training data obligations:** Must be lawfully acquired; no personal information without consent; intellectual property rights must be respected.
- **Content moderation:** Mechanisms must prevent generation of content prohibited by Chinese law.
- **Labelling:** All AI-generated content must be labelled per CAC standards.
- **Real-name registration:** Providers must verify user identity.
- **Incident reporting:** Security incidents must be reported to the CAC.

### Cybersecurity law / MLPS

- AI systems processing personal information at scale may require MLPS assessments at Level 2 or above.

---

## Cross-border transfer mechanisms

PIPL (Articles 38 to 43) permits cross-border transfer only through one of three mechanisms:

1. **CAC Security Assessment (Mandatory threshold):** Mandatory for transfers by critical information infrastructure operators; transfers of personal information of more than 1 million individuals; cumulative transfers of more than 100,000 individuals or sensitive personal information of more than 10,000 individuals since 1 January of the prior year.
2. **Standard Contracts:** Where the security assessment threshold is not triggered: PIPL Standard Contract Clauses published by the CAC (effective June 2023). Organizations must conduct a DPIA and file the signed standard contract with the local CAC within 10 working days.
3. **Certification:** From a recognized professional institution as specified by the CAC; primarily applicable to intra-group transfers.

**Important data:** Transfer of "important data" under the DSL is subject to separate security assessment requirements regardless of volume thresholds.

**Practical note:** The cross-border transfer regime is among the most stringent globally. Early engagement with CAC requirements is essential for any international data transfer programme involving China-origin personal information.

---

## Enforcement and fines

### PIPL

- Warning, correction order, confiscation of illegal gains, or suspension of services.
- Fines: Up to RMB 50 million or 5% of the previous year's annual revenue for serious violations.
- Responsible persons may be fined up to RMB 1 million and prohibited from serving in senior roles.

### CSL

- Fines up to RMB 1 million for operators; additional fines for responsible persons.
- Suspension of business, revocation of licenses for critical information infrastructure operators.

### DSL

- Fines up to RMB 10 million for processors of core state data; up to RMB 5 million for processors of important data; up to RMB 500,000 for general data security violations.

### Generative AI regulations

- Suspension of services, fines, and criminal referral for serious violations. As of 2025, the CAC has commenced enforcement actions against generative AI service providers.

---

## Limitations

This document is a public-domain reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
