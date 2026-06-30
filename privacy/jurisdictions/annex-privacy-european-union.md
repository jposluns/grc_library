# European Union Privacy Regulatory Requirements

**Document Title:** European Union Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.1\
**Date:** 2026-06-30\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/annex-privacy-jurisdiction-index.md`](../annex-privacy-jurisdiction-index.md), [`privacy/policy-privacy-and-data-governance.md`](../policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/jurisdictions/annex-privacy-european-union.md`](annex-privacy-european-union.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex defines privacy and AI regulatory requirements applicable to the processing of personal data of individuals in the European Union under the GDPR and the EU AI Act. It supplements the Privacy and Data Governance Policy and the Privacy Impact and Cross-Border Transfer Procedure.

---

## Applicable laws and regulatory authorities

- **EU General Data Protection Regulation (GDPR)**: Regulation (EU) 2016/679, effective 2018-05-25. The primary EU data protection law governing the processing of personal data of individuals in the EU.
- **EU AI Act**: Regulation (EU) 2024/1689, entered into force 2024-08-01, with phased application through 2027. The world's first comprehensive horizontal AI regulation, classifying AI systems by risk level (unacceptable, high, limited, minimal).
- **Regulatory authorities:** National supervisory authorities in each EU member state (e.g., CNIL in France, BfDI/LfDI in Germany, AEPD in Spain, DPC in Ireland). The European Data Protection Board (EDPB) provides binding decisions and guidelines. The one-stop-shop mechanism applies to organisations with cross-border processing; lead supervisory authority determined by location of main establishment.

---

## AI and privacy obligations

### GDPR obligations relevant to AI

- **Lawful basis (Article 6):** Personal data used to train or operate AI systems must have a lawful basis (consent, legitimate interests, contract, legal obligation, vital interests, or public task).
- **Special categories (Article 9):** AI systems processing biometric data, health data, political opinions, racial or ethnic origin, or other special categories require explicit consent or an Article 9(2) exemption.
- **Automated decision-making and profiling (Article 22):** Data subjects have the right not to be subject to solely automated decisions producing legal or similarly significant effects. Exceptions apply for contract necessity, legal authorization, or explicit consent: each requiring human review safeguards.
- **Data Protection Impact Assessment (Article 35):** Mandatory before processing likely to result in high risk, including systematic automated processing, large-scale processing of special categories, or systematic monitoring. AI systems processing personal data at scale will typically require a DPIA.
- **Data minimization and purpose limitation (Articles 5(1)(b) and 5(1)(c)):** AI training datasets must be limited to data adequate, relevant, and necessary for the specified purpose. Repurposing data for AI training requires a compatible purpose assessment or fresh lawful basis.
- **Transparency and right to explanation (Articles 13, 14, 22(3)):** Individuals must be informed when their data is used in automated processing. Where automated individual decision-making applies, meaningful information about the logic involved must be provided.

### EU AI act obligations (phased)

- **Prohibited practices (Article 5, applicable February 2025):** Prohibited AI applications include subliminal manipulation, exploitation of vulnerable groups, real-time remote biometric identification in public spaces (narrow law enforcement exceptions), social scoring by public authorities, and predictive policing based solely on profiling.
- **High-risk AI systems (Annex III, applicable August 2026):** AI deployed in employment management, credit scoring, biometric categorization, and critical infrastructure is subject to mandatory conformity assessments, technical documentation, human oversight mechanisms, and EU database registration.
- **General-purpose AI (GPAI) models (Articles 51 to 56, applicable August 2025):** Providers must maintain technical documentation, comply with EU copyright law, and publish training data summaries. Providers of GPAI models with systemic risk have additional obligations including adversarial testing and incident reporting.
- **Limited-risk systems (Article 50):** Chatbots and deepfake generators must disclose AI interaction or AI-generated content to users.
- **AI literacy (Article 4):** Deployers and providers must ensure that sufficient AI literacy among their staff.

---

## Cross-border transfer mechanisms

- **Adequacy decisions (Article 45):** Transfers to countries with an EU adequacy decision require no additional safeguards. Current adequacy decisions (as of 2025) include: Andorra, Argentina, Canada (commercial, PIPEDA), Faroe Islands, Guernsey, Israel, Isle of Man, Japan, Jersey, New Zealand, Republic of Korea, Switzerland, United Kingdom, United States (EU-US Data Privacy Framework), and Uruguay.
- **Standard Contractual Clauses (SCCs) (Article 46(2)(c)):** The 2021 European Commission SCCs are the primary mechanism for transfers to non-adequate third countries. SCCs must be supplemented by a Transfer Impact Assessment (TIA); see the [TIA template](../template-transfer-impact-assessment.md).
- **Binding Corporate Rules (BCRs) (Articles 46(2)(b) and 47):** Approved by a lead supervisory authority; permit intra-group international transfers. BCR approval is a multi-year process.
- **Derogations (Article 49):** Narrow exceptions for explicit consent, contract performance, vital interests, public interest, or legal claims. Not suitable as routine transfer mechanisms.

---

## GDPR Article 8 child-consent age thresholds per Member State

GDPR Article 8(1) sets the default age at 16 for child consent to information society services but permits each Member State to lower the age, "provided that such lower age is not below 13 years". The table below lists the age chosen by each EU/EEA Member State as of the date in the document header. **Adopters must verify against the current national implementing law before relying on these values**, since Member States can amend their national thresholds.

| Member State | Age for child consent (years) | National implementing law |
|---|---|---|
| Austria | 14 | DSG (Datenschutzgesetz), §4(4) |
| Belgium | 13 | Loi du 30 juillet 2018 relative à la protection des personnes physiques à l'égard des traitements de données à caractère personnel, Article 7 |
| Bulgaria | 14 | Personal Data Protection Act, Article 25h |
| Croatia | 16 | Act on the Implementation of the General Data Protection Regulation (default) |
| Cyprus | 14 | Law 125(I)/2018, Article 7 |
| Czechia | 15 | Act No. 110/2019, §7 |
| Denmark | 13 | Databeskyttelsesloven, §6 |
| Estonia | 13 | Personal Data Protection Act, §8(2) |
| Finland | 13 | Tietosuojalaki (1050/2018), §5 |
| France | 15 | Loi Informatique et Libertés, Article 45 (post-2018 amendment) |
| Germany | 16 | BDSG (default; no derogation below 16) |
| Greece | 15 | Law 4624/2019, Article 21 |
| Hungary | 16 | Act CXII of 2011 (default) |
| Iceland (EEA) | 13 | Act on Data Protection 90/2018, §10 |
| Ireland | 16 | Data Protection Act 2018, §31 |
| Italy | 14 | Decreto Legislativo 196/2003 (as amended by D.Lgs. 101/2018), Article 2-quinquies |
| Latvia | 13 | Personal Data Processing Law, §3(2) |
| Liechtenstein (EEA) | 16 | Datenschutzgesetz (default) |
| Lithuania | 14 | Law on Legal Protection of Personal Data, Article 5(2) |
| Luxembourg | 16 | Loi du 1er août 2018, Article 7 (default) |
| Malta | 13 | Data Protection Act 2018, Article 9 |
| Netherlands | 16 | UAVG (Uitvoeringswet AVG), Article 5 (default) |
| Norway (EEA) | 13 | Personopplysningsloven §5 |
| Poland | 16 | Act on Personal Data Protection of 10 May 2018, Article 5 (default) |
| Portugal | 13 | Lei n.º 58/2019, Article 16 |
| Romania | 16 | Law no. 190/2018 (default) |
| Slovakia | 16 | Act No. 18/2018 (default) |
| Slovenia | 15 | Personal Data Protection Act ZVOP-2, Article 6 |
| Spain | 14 | Ley Orgánica 3/2018, Article 7 |
| Sweden | 13 | Dataskyddslagen (2018:218), §2(3) |

**Notes**: (1) the default GDPR Article 8 age of 16 applies in Member States that have not chosen a lower age. (2) The Article 8 age governs consent to information society services (online platforms, social media, gaming, etc.); other lawful bases under Article 6 may apply at different age thresholds and other provisions of national law (such as electronic-commerce, education, or child-protection law) may impose additional age-specific obligations. (3) Adopters operating across multiple Member States must apply the per-state age to subjects in that state. (4) The UK is no longer an EU Member State; the UK age is 13 under UK GDPR Article 8 and is documented separately in the United Kingdom privacy annex.

---

## Enforcement and fines

- **Higher tier (GDPR):** Up to €20 million or 4% of total worldwide annual turnover for violations of basic principles, lawful basis, data subject rights, international transfers, and high-risk processing obligations.
- **Lower tier (GDPR):** Up to €10 million or 2% of total worldwide annual turnover for data controller and processor obligation violations and notification failures.
- **EU AI Act: prohibited practices:** Up to €35 million or 7% of worldwide annual turnover.
- **EU AI Act: high-risk/GPAI violations:** Up to €15 million or 3% of worldwide annual turnover.
- **EU AI Act: incorrect information:** Up to €7.5 million or 1.5% of worldwide annual turnover. Lower absolute caps apply to SMEs and start-ups.
- **Enforcement body (AI Act):** the EU AI Office (within DG CNECT) supervises General-Purpose AI (GPAI) at Union level (Articles 88-90, 92-94); the AI Board coordinates member-state authorities and may issue opinions (Articles 65-66); AI supervisory authorities designated by each EU member state enforce per-system obligations within their territory. The EDPB has a consultative role on the interaction between the AI Act and Union data-protection law (Article 67).

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organisations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
