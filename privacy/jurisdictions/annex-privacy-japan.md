# Japan Privacy Regulatory Requirements

**Document Title:** Japan Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.9\
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

- **Act on the Protection of Personal Information (APPI)**: Act No. 57 of 2003; the consolidated text as of April 1, 2023 includes conditions on third-party and cross-border provision of personal data, pseudonymized personal information as a category, rights to request cessation of use, deletion and cessation of third-party provision, and PPC recommendation, order and inspection powers.
- **Regulatory authority:** Personal Information Protection Commission (PPC).
- **PPC AI-related guidance:** The PPC has published material on applying APPI to AI systems. That specific guidance is not held in the reference base, so an adopter confirms the current PPC AI guidance directly; the APPI obligations below apply to AI processing regardless.

---

## AI and privacy obligations

- **Purpose specification:** APPI's purpose-limitation principle applies to personal information used to train AI: handling it beyond the scope necessary to achieve the specified purpose of use requires the individual's prior consent, unless an exception applies [Article 18(1), (3)]. The purpose of use may be altered only within the extent that can be appreciably linked to the prior purpose, and the altered purpose is notified or published unless an Article 21(4) exception applies [Articles 17(2), 21(3), (4)]. For third-party-sourced data, an adopter confirms the use is within the purpose for which the data was provided, or obtains consent for the new purpose.
- **Publicly available data:** APPI contains no general exemption for publicly available personal information, so it remains within scope. The proper-acquisition and inappropriate-use duties apply: a business must not acquire personal information by deception or other wrongful means [Article 20(1)], and must not utilize personal information in a way that may foment or induce an unlawful or unjust act [Article 19]. Guidance specific to web scraping for AI training is not held in the reference base; adopters confirm the current PPC position before relying on a scraping-specific interpretation.
- **Pseudonymized personal information (kamei kakō jōhō, 仮名加工情報):** May be used within the business for an altered purpose without consent, subject to the conditions in Article 41, including that it is not provided to third parties except in cases based on laws and regulations [Article 41(3), (6), (9)].
- **Third-party provision:** Consent is required before providing personal data to AI system operators as third parties, unless an exception or the notification-and-opt-out route applies [Article 27(1), (2)]. A recipient entrusted with all or part of the handling within the scope necessary for the purpose of use is not a third party for this purpose [Article 27(5)(i)].
- **Sensitive personal information:** Prior consent is required to acquire sensitive personal information (race, creed, social status, medical history, criminal record, the fact of having suffered damage by a crime, or other categories prescribed by Cabinet Order), subject to statutory exceptions [Articles 2(3), 20(2)]. The notification-and-opt-out route for third-party provision is not available for it [Article 27(2)].

---

## Operational requirements

Article numbers follow the consolidated APPI as of April 1, 2023 (confirmed against the official English translation of that consolidated text); citations to other versions may not match.

- **Breach report and individual notification (Article 26):** A business handling personal information must, pursuant to PPC rules, report a leak, loss, damage or other situation concerning the security of personal data, of a kind the PPC rules prescribe as likely to harm individual rights and interests, to the PPC, and notify the affected individual. Two exceptions are in the Act itself: a business entrusted with the handling that notifies the entrusting business or administrative entity as the PPC rules prescribe does not report to the PPC or notify the individual [Article 26(1) proviso, 26(2)], and individual notification is not required where it is difficult and necessary alternative measures are taken to protect the person's rights and interests [Article 26(2) proviso]. The specific report deadlines and category thresholds are set by the PPC Enforcement Rules, not by the Act; confirm the current rule values before encoding them in incident playbooks.
- **Data-subject requests (Articles 33 to 35):** An identifiable person may demand disclosure of retained personal data (Article 33), correction of inaccurate data (Article 34), cease-of-use or deletion where the data is handled in violation of Articles 18 or 19 or was acquired in violation of Article 20 (Article 35(1)), cessation of third-party provision made in violation of Article 27(1) or 28 (Article 35(3)), and cease-of-use, deletion or cessation of third-party provision where the business no longer needs the data, a situation described in the main clause of Article 26(1) (a leak, loss, damage or other security situation) has occurred, or handling is likely to harm the person's rights and interests (Article 35(5)). The business acts where it finds grounds for the request, and the Act allows necessary alternative measures in some cases (Article 35(2), (4), (6)). The Act's response standard is "without delay"; it sets no fixed day-count, so adopting organizations set an internal service level and record it in their DSR procedure.
- **Accuracy and deletion (Article 22):** A business must strive to keep personal data accurate and up to date within the scope necessary for the purpose of use, and to delete it without delay when its use is no longer necessary. The Act phrases this as an endeavour duty (the statutory text reads `must endeavor to`), not an absolute one; adopting organizations typically operationalize it as a firm internal control anyway.

---

## Cross-border transfer mechanisms

- Outside the Article 27(1) exceptions, providing personal data to a third party in a foreign country requires the person's consent to that foreign provision, unless the country is one the PPC has designated as having equivalent standards or the recipient has established a system conforming to PPC standards for equivalent measures [APPI Article 28(1)]. Before seeking that consent, the business gives the person information on the foreign country's protection system and the recipient's measures [Article 28(2)]; when relying on a recipient's conforming system, it takes the measures necessary so that the recipient continues to implement the equivalent measures, and informs the person of them on request [Article 28(3)]. The ordinary third-party provision rules in Article 27 still apply to a designated-country or conforming-system recipient.
- APEC CBPR participation is not covered by the held APPI text; adopters confirm Japan's current participation and its role for cross-border transfers with the PPC before relying on it.

---

## Enforcement and fines

- A corporation faces a fine of up to JPY 100 million when its representative, agent, employee or other worker, in relation to the corporation's business, violates a PPC order under Article 148(2) or (3), or provides or misappropriates a personal information database for illegal profit [Articles 178, 179, 184(1)(i)]. Contraventions such as an unlawful cross-border provision or an unreported leak may be addressed by PPC recommendations and orders, including urgent orders issued without a prior recommendation, each subject to its statutory threshold [Article 148(1) to (3)]; violating such an order is the offence. Separately, failing to submit, or falsifying, a report or material the PPC requires under Article 146(1), failing to answer or falsely answering an inspector's questions, or refusing, obstructing or evading an inspection carries a fine of up to JPY 500,000, which also applies to the corporation [Articles 146(1), 182(i), 184(1)(ii)].
- Individuals responsible may face imprisonment or fines [Articles 178, 179] or fines [Article 182].

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
