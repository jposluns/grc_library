# Japan Privacy Regulatory Requirements

**Document Title:** Japan Privacy Regulatory Requirements\
**Document Type:** Annex\
**Version:** 1.1.0\
**Date:** 2026-07-04\
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
- **PPC AI Guidelines (2024):** Guidelines addressing the application of APPI to AI systems, including requirements for lawful basis when using personal information for AI training, restrictions on use of third-party data, and transparency obligations.

---

## AI and privacy obligations

- **Purpose specification:** Personal information used to train AI must be handled in compliance with APPI's purpose specification principle. Using personal information obtained by a third party for AI training requires that it was originally provided for a compatible purpose or that explicit consent exists for repurposing.
- **Publicly available data:** The PPC has issued guidance that even publicly available personal information must be handled in compliance with APPI; scraping for AI training may constitute a violation.
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

- Cross-border third-party provision requires either consent of the data subject, or the recipient is in a country designated by the PPC as having equivalent protection (EU and UK recognized), or the recipient has established a personal information protection system equivalent to APPI standards (BCRs or equivalent contractual obligations).
- The PPC has issued guidance on required contractual and monitoring obligations for cross-border transfers.
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
