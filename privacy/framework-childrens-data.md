# Children's Data Framework

**Document Title:** Children's Data Framework\
**Document Type:** Framework\
**Version:** 1.0.8\
**Date:** 2026-07-02\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/framework-consent-management.md`](framework-consent-management.md), [`privacy/template-privacy-notice.md`](template-privacy-notice.md), [`privacy/register-automated-decision-making.md`](register-automated-decision-making.md), [`privacy/annex-privacy-jurisdiction-index.md`](annex-privacy-jurisdiction-index.md), [`ai/framework-ai-governance-and-risk.md`](../ai/framework-ai-governance-and-risk.md), [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material regulatory, jurisdictional, or product change\
**Repository Path:** [`privacy/framework-childrens-data.md`](framework-childrens-data.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customization guidance.

---

## Purpose

This framework defines the safeguards that apply when the organization processes personal data of children. It addresses age assurance, parental or guardian consent, special-category treatment of children's data, design defaults, profiling and ADM restrictions, and the special obligations under COPPA, GDPR-K, UK Children's Code (Age Appropriate Design Code), Quebec under-14 rules, AB 1394 and similar US state laws, and equivalents.

---

## Scope

This framework applies wherever the organization knowingly processes personal data of children, where there is reason to believe the user base includes children, or where a product is directed to children. It applies across all channels and product surfaces.

The framework deliberately uses "child" rather than a single age threshold because the threshold varies by jurisdiction. Adopting organizations populate the per-jurisdiction threshold from the jurisdiction index annex.

---

## Per-jurisdiction age thresholds (illustrative)

| Jurisdiction | Threshold for parental consent | Notes |
| --- | --- | --- |
| EU member states | 13 to 16 depending on the state (GDPR Article 8) | National derogation; the state's chosen age applies to subjects in that state. See [`privacy/jurisdictions/annex-privacy-european-union.md`](jurisdictions/annex-privacy-european-union.md) "GDPR Article 8 child-consent age thresholds per Member State" for the per-state table covering all 27 EU Member States plus the three EEA countries (Iceland, Liechtenstein, Norway). |
| United Kingdom | 13 (UK GDPR Article 8) | Age Appropriate Design Code applies to a broader age range up to 17 |
| United States: COPPA | Under 13 | Verifiable parental consent required |
| United States: California (CCPA, AB 1394) | Specific opt-in for sale or sharing for under 16; under 13 requires parental opt-in | California-specific |
| Canada (federal): PIPEDA | No fixed numeric age but heightened obligations where the data subject is a child | Office of the Privacy Commissioner guidance applies |
| Canada (Quebec): Law 25 | Under 14 requires parental consent | Quebec-specific |
| Brazil: LGPD | Under 18 considered child or adolescent; under 12 child | Best-interest principle |
| China: PIPL | Under 14 | Parental or guardian consent required |
| Japan: APPI | No fixed statutory numeric age; guardian involvement expected for minors under PPC guidance | Personal Information Protection Commission guidance applies |
| South Korea: PIPA | Under 14 | Parental consent required |

Adopting organizations validate these against the jurisdiction index and applicable legal advice at the time of processing.

---

## Special-category treatment

Children's data is treated with elevated protection across the organization:

1. The default privacy posture is the most protective default available, irrespective of jurisdictional minimum.
2. The data classification is at minimum the same level as adult special-category personal data.
3. Access is restricted to roles with a documented operational need; access reviews occur quarterly rather than annually.
4. Logging on access to children's data records is enhanced and retained for a longer period.
5. Retention is the minimum required for the operational purpose; default retention is shorter than equivalent adult data.

---

## Age assurance

Age assurance is the set of measures used to determine whether a subject is a child. Where the organization knows or has reason to believe the user is a child, the children's data framework applies.

| Approach | Description | Use case |
| --- | --- | --- |
| Self-declared age | Subject states their date of birth | Acceptable for services not specifically directed to children and not likely to attract significant child usage |
| Self-declared with confirmation | Subject re-confirms or is asked again at intervals | Adds friction to age misrepresentation |
| Age estimation | Behavioural, biometric, or document-free estimation | Where self-declared is insufficient and an explicit identity check would be disproportionate |
| Hard age verification | Document or strong-identity check | Where required by law (gambling, alcohol, certain financial services) |

Age assurance is risk-proportionate. The framework does not require document-based age verification in all cases; the standard is appropriate measures given the risk of the product to children.

---

## Parental or guardian consent

1. Where parental consent is the lawful basis (or the consent vehicle to meet GDPR Article 8), the consent capture and verification produces an evidentiary record stored against the child's account.
2. The verification mechanism is risk-proportionate. Acceptable mechanisms include: parent's government-issued identifier verification, parent's payment-card holder verification, parent's video or photo identification, parent's confirmation via an authenticated parent account that the controller already holds.
3. The parent or guardian retains rights on behalf of the child: access, correction, restriction, deletion. The child's own evolving capacity is recognized; the framework supports the child exercising rights directly where appropriate and lawful.
4. Withdrawal of parental consent is a route the parent or guardian can exercise; on withdrawal, processing under that consent stops and dependent data is deleted unless another lawful basis applies.

---

## Design defaults (Age Appropriate Design Code style)

These defaults apply by design wherever the product or feature is likely to be accessed by children. They are protective starting points; the organization may relax them where there is a clear best-interest justification.

| Design default | Default state |
| --- | --- |
| High-privacy default | All privacy settings start at the most protective configuration |
| No detrimental use of data | No use of children's data in ways shown or likely to be detrimental to their wellbeing |
| No behavioural advertising | No profiling-based advertising directed at children |
| Geolocation | Off by default; if on, a clear obvious indicator is displayed each time |
| Connected toys and devices | Equivalent protections; data collection minimized; deactivation control accessible |
| Nudge techniques | Not used to encourage children to weaken their privacy settings or to share more data |
| Default sharing | Off by default; opt-in only |
| Reporting and complaint route | Visible, child-friendly, and effective |
| Detrimental algorithmic content amplification | Off by default in algorithmic feeds where children are present |

---

## Profiling and automated decision-making

1. Profiling of children for marketing or advertising purposes is prohibited unless explicit lawful basis exists and best-interest analysis justifies it.
2. Automated decision-making with legal or similarly significant effect on a child requires Data Protection Officer review beyond the standard ADM register entry. Where lawful, additional human-review safeguards apply.
3. AI systems used in services likely to be accessed by children undergo an enhanced AI System Impact Assessment that explicitly considers child wellbeing.

---

## Operating expectations

1. Each product or feature likely to be accessed by children is assessed against the framework before launch.
2. The product team identifies the applicable jurisdictional thresholds and consent mechanisms in advance.
3. Marketing and growth experiments involving children require Data Protection Officer review; A/B tests on consent or privacy controls in the child-accessible surface require enhanced documentation.
4. Incident response procedures for children's data classify breaches at one severity level higher than equivalent adult data by default.
5. Annual review of children's data processing activities is conducted by the Data Protection Officer with input from a designated child-safety reviewer where the product is materially directed to children.

---

## Metrics

| Metric | Definition | Target |
| --- | --- | --- |
| Children's data product coverage | Percentage of products likely to be accessed by children that have a current framework assessment | 100% |
| Parental consent verification adherence | Percentage of records requiring parental consent that have a valid verification record | 100% |
| Design defaults adherence | Percentage of child-accessible products meeting all design defaults at launch | At least 95% |
| Child-impact AI impact assessment currency | Percentage of AI systems used in child-accessible products with an in-date AISIA explicitly considering child wellbeing | 100% |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| GDPR | Article 8, Recital 38 | Child consent and protection |
| UK GDPR | Article 8 | Equivalent provisions |
| UK ICO Age Appropriate Design Code | 15 standards | Design defaults and best interests |
| COPPA | 16 CFR 312 | Children under 13 in the US |
| California AB 2273 (Age-Appropriate Design Code Act, 2022) | Multiple sections | Design-defaults and best-interests obligations for online services likely accessed by minors. Note: AB 2273 has been partially enjoined by the Ninth Circuit in 2024; adopters should monitor injunction status. |
| California AB 1394 (Social Media Platform Duty to Children, 2023) | Health and Safety Code Div. 110 | Distinct from AB 2273; addresses social-media-platform duties regarding child sexual abuse material (CSAM) and known minor users |
| LGPD | Article 14 | Child consent and best interest |
| PIPL | Article 31 | Children under 14 |
| EU AI Act | Article 5(1)(b) | Prohibition on exploiting vulnerabilities of children |
| UN Convention on the Rights of the Child General Comment 25 | Children's rights in the digital environment | Best-interest principle |

---

## Limitations

This framework is a CC BY-SA 4.0 baseline. Adopting organizations must populate jurisdictional thresholds from the applicable jurisdiction annexes, validate consent verification mechanisms with legal counsel, design product flows in collaboration with child-safety specialists where the product is materially directed to children, and conduct independent reviews of automated systems that may affect children. The framework is not legal advice and does not establish certification.

---

**End of Document**
