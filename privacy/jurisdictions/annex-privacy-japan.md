# Japan Privacy Regulatory Requirements

**Document Title:** Japan Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.1\
**Date:** 2026-09-04\
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
- **Publicly available data:** APPI contains no general exemption for publicly available personal information, so it remains within scope. The proper-acquisition duty applies: a business must not acquire personal information by deceit or other improper means [Article 17], and must not use personal information by a method that may foment or prompt an unlawful or unfair act [Article 16-2]. Guidance specific to web scraping for AI training is not held in the reference base; adopters confirm the current PPC position before relying on a scraping-specific interpretation.
- **Pseudonymous information (kamei kakō jōhō, 仮名加工情報: 2022 amendment):** May be used for internal analysis without consent under certain conditions, providing a lawful basis for some internal AI processing.
- **Third-party provision:** Consent is required before providing personal information to AI system operators as third parties, unless an exception applies.
- **Sensitive personal information:** Explicit opt-in consent required for processing of sensitive categories (race, creed, social status, medical history, criminal record, etc.) in AI systems.

---

## Operational requirements

Article numbers follow the current consolidated APPI (confirmed against the official English translation of the consolidated text; the pre-2022 amendment texts number these provisions differently).

- **Breach report and individual notification (Article 26):** A business handling personal information must, pursuant to PPC rules, report a leakage, loss, or damage of personal data that is likely to harm an individual's rights and interests to the PPC, and notify the affected individual. The specific report deadlines and category thresholds are set by the PPC Enforcement Rules, not by the Act; confirm the current rule values before encoding them in incident playbooks.
- **Data-subject requests (Articles 33 to 35):** An identifiable person may demand disclosure of retained personal data (Article 33), correction of inaccurate data (Article 34), and cease-of-use or deletion (Article 35). The Act's response standard is "without delay"; it sets no fixed day-count, so adopting organizations set an internal service level and record it in their DSR procedure.
- **Accuracy and deletion (Article 22):** A business must strive to keep personal data accurate and up to date within the scope necessary for the purpose of use, and to delete it without delay when its use is no longer necessary. The Act phrases this as an endeavour duty (the statutory text reads `shall strive to`), not an absolute one; adopting organizations typically operationalize it as a firm internal control anyway.

---

## Cross-border transfer mechanisms

- Cross-border third-party provision requires either consent of the data subject, or the recipient is in a country designated by the PPC as having equivalent protection, or the recipient has established a personal information protection system conforming to PPC rules [APPI Article 24].
- Japan participates in the APEC CBPR 2.0 framework.

---

## Enforcement and fines

- Fines up to JPY 100 million for organizations for violations, including unlawful cross-border transfers and failure to notify the PPC of data breaches.
- Individuals responsible may face criminal penalties.

---

## Limitations

This document is a CC BY-SA 4.0 reference baseline. It does not constitute legal advice. Adopting organizations must obtain jurisdiction-specific legal advice and validate applicability against their operating model, sector, processing activities, and contractual obligations. Regulatory frameworks change frequently; verify currency before reliance.

---

**End of Document**
