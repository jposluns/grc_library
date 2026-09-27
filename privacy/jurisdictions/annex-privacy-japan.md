# Japan Privacy Regulatory Requirements

**Document Title:** Japan Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.5\
**Date:** 2026-09-27\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/annex-privacy-jurisdiction-index.md`](../annex-privacy-jurisdiction-index.md), [`privacy/policy-privacy-and-data-governance.md`](../policy-privacy-and-data-governance.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/jurisdictions/annex-privacy-japan.md`](annex-privacy-japan.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex defines privacy and AI regulatory requirements applicable to the processing of personal data in Japan under the Act on the Protection of Personal Information (APPI). It supplements the Privacy and Data Governance Policy and the Privacy Impact and Cross-Border Transfer Procedure.

---

## Applicable laws and regulatory authorities

- **Act on the Protection of Personal Information (APPI)**: Substantially amended in 2022 (effective April 2022) to introduce stricter consent requirements for third-party provision, cross-border transfer restrictions, pseudonymous information as a new category, rights to request suspension of third-party provision and deletion, and expanded enforcement powers.
- **Regulatory authority:** Personal Information Protection Commission (PPC).
- **PPC AI-related guidance:** The PPC has published material on applying APPI to AI systems. That specific guidance is not held in the reference base, so an adopter confirms the current PPC AI guidance directly; the APPI obligations below apply to AI processing regardless.

---

## AI and privacy obligations

- **Purpose specification:** APPI's purpose-limitation principle applies to personal information used to train AI: using it beyond the originally specified purpose of utilization generally requires the individual's consent. For third-party-sourced data, an adopter confirms the use is within the purpose for which the data was provided, or obtains consent for the new purpose.
- **Publicly available data:** APPI contains no general exemption for publicly available personal information, so it remains within scope. The proper-acquisition duty applies: a business must not acquire personal information by deception or other wrongful means [Article 20(1)], and must not utilize personal information in a way that may foment or induce an unlawful or unjust act [Article 19]. Guidance specific to web scraping for AI training is not held in the reference base; adopters confirm the current PPC position before relying on a scraping-specific interpretation.
- **Pseudonymous information (kamei kakō jōhō, 仮名加工情報: 2022 amendment):** May be used for internal analysis without consent under certain conditions, providing a lawful basis for some internal AI processing.
- **Third-party provision:** Consent is required before providing personal data to AI system operators as third parties, unless an exception applies [Article 27(1)].
- **Sensitive personal information:** Prior consent is required to acquire sensitive personal information (race, creed, social status, medical history, criminal record, the fact of having suffered damage by a crime, or other categories prescribed by Cabinet Order), subject to statutory exceptions [Articles 2(3), 20(2)]. The notification-and-opt-out route for third-party provision is not available for it [Article 27(2)].

---

## Operational requirements

Article numbers follow the current consolidated APPI (confirmed against the official English translation of the consolidated text; the pre-2022 amendment texts number these provisions differently).

- **Breach report and individual notification (Article 26):** A business handling personal information must, pursuant to PPC rules, report a leak, loss, or damage of personal data of a kind the PPC rules prescribe as likely to harm individual rights and interests to the PPC, and notify the affected individual. Two exceptions are in the Act itself: a business entrusted with the handling that notifies the entrusting business or administrative entity as the PPC rules prescribe does not report to the PPC or notify the individual [Article 26(1) proviso, 26(2)], and individual notification is not required where it is difficult and necessary alternative measures are taken to protect the person's rights and interests [Article 26(2) proviso]. The specific report deadlines and category thresholds are set by the PPC Enforcement Rules, not by the Act; confirm the current rule values before encoding them in incident playbooks.
- **Data-subject requests (Articles 33 to 35):** An identifiable person may demand disclosure of retained personal data (Article 33), correction of inaccurate data (Article 34), and cease-of-use or deletion on the grounds Article 35 sets out: handling in violation of Articles 18 or 19, acquisition in violation of Article 20, the business no longer needing the data, a reportable leak under Article 26(1), or handling likely to harm the person's rights and interests (Article 35(1), (5)). The business acts where it finds grounds for the request, and the Act allows necessary alternative measures in some cases (Article 35(2), (6)). The Act's response standard is "without delay"; it sets no fixed day-count, so adopting organizations set an internal service level and record it in their DSR procedure.
- **Accuracy and deletion (Article 22):** A business must strive to keep personal data accurate and up to date within the scope necessary for the purpose of use, and to delete it without delay when its use is no longer necessary. The Act phrases this as an endeavour duty (the statutory text reads `must endeavor to`), not an absolute one; adopting organizations typically operationalize it as a firm internal control anyway.

---

## Cross-border transfer mechanisms

- Outside the Article 27(1) exceptions, providing personal data to a third party in a foreign country requires the person's consent to that foreign provision, unless the country is one the PPC has designated as having equivalent standards or the recipient has established a system conforming to PPC standards for equivalent measures [APPI Article 28(1)]. Before seeking that consent, the business gives the person information on the foreign country's protection system and the recipient's measures [Article 28(2)]; when relying on a recipient's conforming system, it takes the measures necessary so that the recipient continues to implement the equivalent measures, and informs the person of them on request [Article 28(3)]. The ordinary third-party provision rules in Article 27 still apply to a designated-country or conforming-system recipient.
- Japan participates in the APEC CBPR framework.

---

## Enforcement and fines

- A corporation faces a fine of up to JPY 100 million when its representative, agent, employee or other worker, in relation to the corporation's business, violates a PPC order under Article 148(2) or (3), or provides or misappropriates a personal information database for illegal profit [Articles 178, 179, 184(1)(i)]. Contraventions such as an unlawful cross-border provision or an unreported leak are addressed by PPC recommendations and orders, including urgent orders issued without a prior recommendation [Article 148(1) to (3)]; violating such an order is the offence. Failing to report to the PPC, or obstructing a PPC inspection, is a separate offence with a fine of up to JPY 500,000, which also applies to the corporation [Articles 146(1), 182, 184(1)(ii)].
- Individuals responsible may face imprisonment or fines [Articles 178, 179, 182].

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
