# MiCA Implementation Annex

**Document Title:** MiCA Implementation Annex\
**Document Type:** Annex\
**Version:** 0.3.0\
**Date:** 2026-09-11\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/README.md`](../README.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](../register-global-regulatory-applicability.md), [`compliance/financial-services/annex-financial-services-sector-requirements.md`](annex-financial-services-sector-requirements.md), [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md), [`resilience/framework-business-continuity-and-resilience.md`](../../resilience/framework-business-continuity-and-resilience.md), [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../../supply-chain/standard-supplier-security-and-privacy-assurance.md), [`compliance/financial-services/annex-dora-implementation.md`](annex-dora-implementation.md)\
**Classification:** Public\
**Category:** Compliance: Sector-Specific\
**Review Frequency:** Annual and upon material MiCA Regulatory Technical Standards (RTS), Implementing Technical Standards (ITS), or supervisory guidance change\
**Repository Path:** [`compliance/financial-services/annex-mica-implementation.md`](annex-mica-implementation.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex describes how an entity in scope of the EU Markets in Crypto-Assets Regulation (Regulation (EU) 2023/1114, "MiCA") can use the core GRC library to implement its obligations as an issuer of asset-referenced tokens, an issuer of e-money tokens, or a crypto-asset service provider. The annex maps the library to MiCA's structure by crypto-asset category and by service, identifies the supervisory artefacts MiCA requires, and notes the phased application timeline.

MiCA is binding Union law, directly applicable in every Member State (Art 149), so, unlike a voluntary industry framework, its requirements are legal obligations rather than good-practice recommendations. This annex does not reproduce MiCA articles, RTS, or ITS text. Adopting entities consume those from the official EUR-Lex, EBA, and ESMA sources.

## Applicability triggers

MiCA applies to persons engaged in the issuance, offer to the public, or admission to trading of crypto-assets in the Union, or providing crypto-asset services in the Union (Art 2(1)). The library is relevant where the entity is one of the in-scope roles:

1. Offeror or person seeking admission to trading of a crypto-asset **other than an ART or EMT** (Title II).
2. Issuer of an **asset-referenced token (ART)** (Title III).
3. Issuer of an **e-money token (EMT)**, necessarily a credit institution or an electronic money institution (Art 48(1)).
4. **Crypto-asset service provider (CASP)** authorized under Art 63, or a financial entity providing crypto-asset services under Art 60.

MiCA does not apply to crypto-assets that are unique and non-fungible (Art 2(3)) or that qualify as financial instruments, deposits, funds (other than EMTs), or the other instruments listed in Art 2(4). Partial exemptions exist but do not relieve all duties: Art 4(2) disapplies Art 4(1) points (b), (c), (d), and (f) for a Title II offer of a crypto-asset other than an ART or EMT that is made to fewer than 150 persons per Member State acting on their own account, or whose total consideration over twelve months does not exceed EUR 1 000 000, or that is addressed solely to qualified investors (and can only be held by them); the remaining Art 4(1) obligations still apply. Art 16(2) disapplies the Art 16(1) authorization requirement where the ART's average outstanding value over twelve months never exceeds EUR 5 000 000 and the issuer is not linked to a network of other exempt issuers, or the offer is addressed solely to qualified investors and the ART can only be held by them, but the issuer must still draw up an ART white paper and notify it to its competent authority. Consult the article and the relevant RTS for the exact conditions.

## Application timeline

MiCA entered into force on 29 June 2023 (Art 149(1)). It applies in two phases: Titles III (asset-referenced tokens) and IV (e-money tokens) from 30 June 2024, and the remainder, including Title II offers, Title V crypto-asset services, and Title VI market abuse, from 30 December 2024 (Art 149(2) and (3)). A crypto-asset service provider that lawfully provided its services before 30 December 2024 may continue under a transitional regime until 1 July 2026 or until authorization is granted or refused, whichever is sooner, except that a Member State may shorten or disapply that regime (Art 143(3)); an adopter confirms its own Member State's transitional window, since it is not uniform across the Union.

## The three crypto-asset categories (the classification gate)

The obligations that apply turn entirely on which category a token falls in, and the distinction is precise:

- **E-money token (EMT):** purports to maintain a stable value by referencing **one official currency** (Art 3(7)); deemed electronic money (Art 48(2)); issuable only by a credit institution or EMI (Art 48(1)).
- **Asset-referenced token (ART):** any stable-value token that is **not** an EMT, referencing another value or right, a combination, or **one or more** official currencies (Art 3(6)); a multi-currency basket stablecoin is an ART, not an EMT.
- **Crypto-asset other than ART or EMT:** the residual category (utility tokens and other non-stable crypto-assets), governed by Title II.

Misclassification propagates into the wrong reserve, redemption, and authorization regime, so the classification is the first control an adopter documents.

## Title II: offers of crypto-assets other than ART or EMT (Arts 4-15)

Title II governs the crypto-asset white-paper lifecycle for offers to the public and admissions to trading of crypto-assets that are neither asset-referenced tokens (ART) nor e-money tokens (EMT). The white paper is a MiCA-specific supervisory document the offeror or person seeking admission drafts to the Annex I schema; the library holds the surrounding disclosure, marketing, conflict-of-interest, safeguarding, and regulator-interaction controls, but not the white paper or its notification, which are MiCA-specific. The obligations below rest on the MiCA Level 1 text (Regulation (EU) 2023/1114); the Art 6(11) or (12) technical standards are not held (see the technical-standards note).

### White-paper lifecycle and offer conditions (Arts 4-15)

| MiCA obligation (held cite) | Library artefact / disposition |
| --- | --- |
| **Offer-to-public preconditions (Art 4(1))**: a person must not offer such a crypto-asset to the public unless it is a legal person and has drawn up (Art 6), notified (Art 8), and published (Art 9) a white paper and drafted any marketing communications to Art 7. | *(MiCA-specific gap: the white paper and its notification; the library holds the disclosure-governance and marketing controls the offeror applies)* |
| **Partial exemptions and thresholds (Art 4(2))**: several Art 4(1) points are disapplied for an offer to fewer than 150 natural or legal persons per Member State acting on their own account, a total consideration not exceeding EUR 1 000 000 over 12 months, or an offer solely to qualified investors where the crypto-asset can only be held by such investors. | *(scoping gate; an adopter scopes applicability against these thresholds)* |
| **Utility-token offer duration (Art 4(6))**: an offer of a utility token for a good or service not yet in operation runs no more than 12 months from white-paper publication. | *(MiCA-specific gap)* |
| **Admission-to-trading preconditions (Art 5)**: a person seeking admission to trading meets the same legal-person, white-paper, and marketing preconditions; where the platform operator draws up the paper, Art 5 allocates the responsibility. | *(MiCA-specific gap)* |
| **Result of offer and safeguarding (Art 10)**: publish the offer result (time-limited offers within 20 working days; open-ended offers, the units in circulation at least monthly), and safeguard the funds and crypto-assets raised, held in custody by a credit institution (where funds are raised) or a crypto-asset service provider (for crypto-assets), or both, for time-limited offers and, for open-ended offers, until the Art 13 withdrawal right expires. | library safeguarding and asset-segregation controls (adopter maps); MiCA-specific reporting is a gap |
| **Passporting and no further information requirements (Art 11)**: after publication (and any Art 12 modification), the offeror may offer the crypto-asset throughout the Union, and is not subject to any further information requirements for that offer or admission. | *(the passporting relief is MiCA-specific; no artefact)* |
| **White-paper content and quality (Art 6(1)-(2))**: the paper carries the Annex I information (below), fair, clear and not misleading, with no material omission, in a concise and comprehensible form. | `compliance/` disclosure-governance artefacts (adopter maps to the Annex I schema) |
| **Mandatory white-paper statements (Art 6(3),(5),(6))**: the first-page "not approved by any competent authority" statement (Art 6(3)); the risk and value warnings (Art 6(5)); the management-body statement (Art 6(6)). | *(MiCA-specific gap)* |
| **Form obligations (Art 6(4),(7),(8),(9),(10))**: no assertions of future value (Art 6(4)); a summary (Art 6(7)); a date and table of contents (Art 6(8)); an official or customary language (Art 6(9)); a machine-readable format (Art 6(10)). | *(MiCA-specific gap)* |
| **Consensus-mechanism environmental disclosure (Art 6(1)(j))**: the principal adverse impacts on the climate and other environment-related adverse impacts of the consensus mechanism. | ESG and disclosure controls (adopter maps); MiCA-specific detail is a gap |
| **Marketing communications (Art 7)**: identifiable as such; fair, clear and not misleading; consistent with the white paper; carrying the standard statement that they have not been reviewed by a competent authority. | library marketing and communications controls |
| **Notification to the competent authority (Art 8)**: notify the home-Member-State authority of the white paper (and the marketing communications on request) before publication, with the Art 8 content. | [`compliance/template-regulator-interaction.md`](../template-regulator-interaction.md) (the adopter's regulator-notification channel) |
| **Publication (Art 9)**: publish the white paper and any marketing communications on a publicly accessible website by the offer start and keep them available while the crypto-assets are held by the public. | *(MiCA-specific gap)* |
| **Modification of a published white paper (Art 12)**: on a significant new factor, material mistake, or material inaccuracy capable of affecting the assessment of the crypto-assets, modify the white paper and notify the authority per the Art 12 procedure. | `compliance/` change and disclosure controls (adopter maps); the MiCA-specific procedure is a gap |
| **Right of withdrawal (Art 13)**: retail holders have 14 calendar days to withdraw from a purchase agreement, free of charge and without reasons, for a public offer (not for admission to trading), running from the date of agreement. | *(MiCA-specific gap)* |
| **Ongoing conduct obligations (Art 14)**: act honestly, fairly and professionally; communicate fairly and not misleadingly; identify, prevent, manage and disclose conflicts of interest; maintain systems and secure access protocols. | library governance, conflict-of-interest, and security controls |
| **Civil liability for the white paper (Art 15)**: the offeror or person seeking admission, and the members of its management body, are liable where the white paper is not fair, clear and not misleading or omits key information. | *(MiCA-specific gap; the library's disclosure-accuracy controls reduce the exposure)* |

### White-paper content schema (Annex I)

The Art 6 white paper follows the Annex I schema, nine lettered parts: **Part A** the offeror or person seeking admission to trading; **Part B** the issuer, if different; **Part C** the operator of the trading platform, where it draws up the paper; **Part D** the crypto-asset project; **Part E** the offer to the public or the admission to trading; **Part F** the crypto-assets; **Part G** the rights and obligations attached to the crypto-assets; **Part H** the underlying technology; **Part I** the risks (of the offer, the issuer, the crypto-assets, project implementation, and the technology used). Responsibility for having the white paper drawn up rests with the offeror, the person seeking admission to trading, or the applicable trading-platform operator; Parts A and D to I always apply, while Part B applies only where the issuer differs from the offeror or person seeking admission, and Part C only where the platform operator draws up the paper. All nine parts are MiCA-specific content, and the library holds no white-paper template.

### Technical standards (held status)

Art 6(11) mandates ESMA implementing technical standards (standard forms, formats, and templates for the white paper) and Art 6(12) mandates regulatory technical standards. **`grc_library_ref` does not hold the Title II white-paper ITS or RTS** (the held MiCA delegated-act set covers other Titles (III to VII), not Title II); they are acquisition items (egress-gated), and the mapping above rests on the MiCA Level 1 text alone.

## Title III: asset-referenced tokens (Arts 16-47)

| MiCA element | Library artefact |
| --- | --- |
| Authorization / fit-and-proper management body (Arts 16, 18, 34(2)) | `risk/policy-enterprise-governance-and-risk-management.md`, `governance/charter-governance-library.md` |
| Governance, internal control, risk management (Art 34) | `risk/standard-enterprise-risk-management.md`, `security/policy-information-security.md` |
| ICT risk management + data safeguarding (Art 34(10)/(11), cross-referencing DORA) | the DORA implementation annex + `security/` standards |
| Business continuity (Art 34(9)) | `resilience/framework-business-continuity-and-resilience.md` |
| Complaints-handling (Art 31; RTS 2025/293) | no direct carrier; `compliance/procedure-capa.md` covers internal corrective and preventive action only, so the adopter provides a MiCA complaints-handling procedure per RTS 2025/293 |
| Conflicts of interest (Art 32; RTS 2025/1141) | library conflicts-of-interest control |
| Reserve of assets: constitution, segregation, audit (Arts 36-38) | *(MiCA-specific; no core artefact, the reserve is a supervised financial construct)* |
| Right of redemption at market value, in principle without a fee but subject to the Art 46 recovery options (Art 39) | *(MiCA-specific policy)* |
| Recovery and redemption plans (Arts 46-47) | `resilience/` continuity/recovery artefacts as the operational base |

Gaps: the reserve-of-assets regime (Arts 36-38, legal/operational segregation, six-monthly independent audit, custody within five working days, investment constraints), the permanent right of redemption at market value (Art 39), own-funds at the highest of EUR 350 000 / 2% of reserve / a quarter of fixed overheads (Art 35, rising to 3% for significant ARTs, Art 45(5); a credit institution issuing ARTs is not subject to Art 35, Art 17(4)), and the recovery/redemption plans (Arts 46-47) are MiCA-specific supervisory artefacts the issuer maintains beyond the library baseline.

## Title IV: e-money tokens (Arts 48-58)

| MiCA element | Library artefact |
| --- | --- |
| Credit-institution / EMI status + white-paper notification (Art 48) | governance/authorization artefacts (status is an external licence) |
| Issue at par value, redeem at par value at any time, in principle without a fee but subject to the Art 46 recovery options (Art 49) | *(MiCA-specific; note: par value, unlike ART market value)* |
| Interest prohibition (Art 50) | *(MiCA-specific policy)* |
| Safeguarding of funds: at least 30% deposited, remainder in highly liquid low-risk instruments (Art 54) | `risk/` + `supply-chain/` custody controls as inputs |
| Recovery/redemption plans (Art 55, applying Title III Ch 6) | `resilience/` artefacts |
| Significant-EMT additional obligations (Art 58, applying Arts 36-38, 45; RTS 2025/1264, 2025/418) | as for significant ARTs |

Gap: an ordinary EMT uses the EMD safeguarding regime plus Art 54, not the Art 36 reserve; however, an electronic money institution issuing a **significant** EMT is subject to Arts 36 to 38 in place of the EMD safeguarding regime (Art 58(1)), and a competent authority may impose those requirements on a non-significant EMT issued by an EMI (Art 58(2)). An adopter applies the Art 54 regime by default and the Art 36 reserve only where Art 58 brings it in, so it does not apply the ART reserve rules to an ordinary EMT.

## Title V: crypto-asset service providers (Arts 59-85)

| MiCA element | Library artefact |
| --- | --- |
| Authorization / EU-establishment conditions (Arts 59, 62-63; RTS 2025/305, ITS 2025/306) | governance/authorization artefacts |
| Notification route for financial entities (Art 60; RTS 2025/303, ITS 2025/304) | as above |
| Act honestly/fairly, fair-clear-not-misleading, risk warnings (Art 66) | `compliance/` conduct + disclosure controls |
| Prudential safeguards (Art 67, the higher of the Annex IV permanent minimum capital or a quarter of the preceding year's fixed overheads; a financial entity providing services under Art 60 is not subject to Art 67) | `risk/` capital/financial-control artefacts as inputs |
| Governance, fit-and-proper, continuity, AML, records (Art 68; RTS 2025/299, 2025/1140) | `risk/standard-enterprise-risk-management.md`, `resilience/framework-business-continuity-and-resilience.md`, `security/standard-logging-and-monitoring.md` |
| ICT continuity per DORA (Art 68(7), citing DORA Arts 11-12) | the DORA implementation annex |
| Safekeeping of clients' crypto-assets and funds; insolvency protection (Art 70) | [`crypto/standard-digital-asset-custody.md`](../../crypto/standard-digital-asset-custody.md) (segregation, next-business-day fund placement) + `security/` + `operations/` key controls |
| Complaints-handling (Art 71; RTS 2025/294) | no direct carrier; `compliance/procedure-capa.md` covers internal corrective and preventive action only, so the adopter provides a MiCA CASP complaints-handling procedure per RTS 2025/294 |
| Conflicts of interest, reviewed annually (Art 72; RTS 2025/1142) | library conflicts-of-interest control |
| Outsourcing, incl. contingency + exit strategies (Art 73) | `supply-chain/framework-supplier-and-cloud-governance.md`, `supply-chain/procedure-supplier-exit-and-data-return.md`, `supply-chain/standard-supplier-security-and-privacy-assurance.md` |
| Orderly wind-down plan, for CASPs providing the services in Arts 75 to 79 (Art 74) | `resilience/` recovery artefacts |
| Custody-specific: register of positions, custody policy, statements at least once every three months, legal/operational segregation, liability (Art 75) | [`crypto/standard-digital-asset-custody.md`](../../crypto/standard-digital-asset-custody.md) (register of positions, custody policy, agreement content, statement cadence, Art 75(8) attributable-loss liability) |
| Trading-platform operating rules, order-book records (Art 76; RTS 2025/416) | `operations/` + market-integrity controls |

Gaps: the crypto custody standard now supplies the reusable core of client-asset segregation, the custody policy, the register of positions, and the RTS 2025/1140 records medium and client-distinguishability (Arts 70, 75; RTS 2025/1140 Arts 2, 5); the Article 68(9) general record-keeping obligation (records of all crypto-asset services, activities, orders, and transactions, provision to clients on request, and five-to-seven-year retention), the Annex IV prudential-safeguards calculation (Art 67), and the service-specific operating rules for the other crypto-asset services (Arts 76-82) remain MiCA-specific and maintained beyond the library baseline.

## Title VI: market abuse (Arts 86-92)

Title VI imposes an EU market-abuse regime on crypto-assets that are admitted to trading, or for which a request for admission to trading has been made, applying to acts by any person and whether carried out on or off a trading platform (Art 86). The regime rests on the disclosure duty (Art 88) and the prohibitions on insider dealing (Art 89), unlawful disclosure (Art 90), and market manipulation (Art 91), backed by a prevention-and-detection duty (Art 92). Two Title VI technical standards are held and cited below: the ITS 2024/2861 (an implementing technical standard under Art 88(4)) and the RTS 2025/885 (a regulatory technical standard under Art 92(2)); the Art 92(3) ESMA guidelines are soft law and are not held.

| MiCA obligation (held cite) | Library artefact / disposition |
| --- | --- |
| **Scope of the market-abuse rules (Art 86)**: the Title applies to acts concerning crypto-assets admitted to, or requested for admission to, trading, by any person and whether on or off a trading platform. | *(scoping gate; the prohibitions and duties below are the operative controls)* |
| **Inside-information definition (Art 87)**: information of a precise nature, not made public, relating directly or indirectly to issuers, offerors, persons seeking admission, or crypto-assets, which if made public would likely have a significant effect on the prices of those or related crypto-assets. | *(definitional; informs the disclosure and insider-dealing controls below)* |
| **Public disclosure of inside information (Art 88(1))**: issuers, offerors, and persons seeking admission inform the public as soon as possible of inside information that directly concerns them. | library disclosure-governance controls (adopter maps); the MiCA-specific timing is a gap |
| **Delayed disclosure and its notification (Art 88(2)-(3))**: disclosure may be delayed, on the person's own responsibility, only where the Art 88(2) conditions are met; the person then informs the competent authority that disclosure was delayed and provides a written explanation of how those conditions were met, immediately after the information is disclosed to the public (Art 88(3); a Member State may instead require that the explanation be provided only on the authority's request). | library disclosure-governance and decision-record controls; the MiCA-specific delay procedure is a gap |
| **Technical means for public disclosure (Art 88(4); ITS 2024/2861)**: disclose to a wide public, free of charge and simultaneously, through the technical means the ITS prescribes. | *(MiCA-specific gap; the held ITS 2024/2861 supplies the technical means for reference)* |
| **Prohibition of insider dealing (Art 89)**: a person possessing inside information must not use it to acquire or dispose of the related crypto-assets, cancel or amend an order that was placed before the person possessed the information, or recommend or induce another to do so. | library insider-dealing, conflict-of-interest, and code-of-conduct controls |
| **Prohibition of unlawful disclosure of inside information (Art 90)**: a person possessing inside information must not unlawfully disclose it, except in the normal exercise of employment, a profession, or duties. | library information-handling and confidentiality controls |
| **Prohibition of market manipulation (Art 91)**: no person may engage, or attempt to engage, in market manipulation, including giving false or misleading signals, securing a price at an abnormal or artificial level, employing fictitious devices, or disseminating misleading information. | library conduct and market-integrity controls (adopter maps); the MiCA-specific application is a gap |
| **Prevention-and-detection arrangements and suspicious-transaction-and-order reporting (Art 92; RTS 2025/885)**: any person professionally arranging or executing transactions in crypto-assets maintains effective arrangements, systems, and procedures to prevent and detect market abuse, and reports suspicious transactions and orders to the competent authority without delay, per the RTS 2025/885 detection, reporting-template, and record-retention requirements. | `operations/procedure-threat-intelligence-and-siem-operations.md`, `security/standard-logging-and-monitoring.md` (monitoring base; the market-abuse detection template and the suspicious-transaction-and-order report are MiCA-specific) |

Art 92(3) provides for ESMA guidelines on the consistency of supervisory practices under Art 92; those guidelines are soft law and are not held in `grc_library_ref`.

## Supervisory architecture (Title VII)

MiCA is supervised two-tier: national competent authorities designated under Art 93 supervise CASPs, Title II offerors, and non-significant ART/EMT issuers (a Title II white paper is notified, not approved: the competent authority does not require prior approval, Art 8(3)); **EBA** supervises **significant** ARTs and, for a significant EMT issued by an electronic money institution, compliance with Arts 55 and 58 (Art 117(4)), the significant-token classification triggering EBA's role (Arts 43(7), 56(6)), except that supervision of a significant EMT denominated in a non-euro Member-State currency does not transfer where at least 80% of holders and transactions are domestic (Art 56(7)); **ESMA** maintains the public register of white papers, issuers, and CASPs (Art 109) and, with EBA, develops the RTS/ITS; the **ECB and national central banks** hold monetary-sovereignty opinion rights over tokens referencing their currency (Arts 17(5), 43). An adopter identifies its home-Member-State competent authority (and, for a significant token, EBA) as its supervisor.


## Held MiCA technical standards (RTS and ITS) map

`grc_library_ref` holds twenty MiCA Level 2 technical standards. An RTS is a regulatory (delegated) technical standard; an ITS is an implementing technical standard. Most are cited inline in the Title sections above; this table consolidates them as a single index of what is held, the MiCA article each derives from (verified against each instrument's own citation of Regulation (EU) 2023/1114), and the library disposition. It also records three instruments not otherwise mapped above: RTS 2025/413 and RTS 2025/414 (qualifying holdings) and RTS 2025/297 (supervisory colleges).

| Instrument | Type | MiCA basis (Title / Article) | Subject | Library disposition |
| --- | --- | --- | --- | --- |
| RTS 2025/1125 | RTS | Title III / Art 18(6) | Information in an application for authorization to offer ARTs | governance authorization controls (adopter maps); the MiCA application is a gap |
| ITS 2025/1126 | ITS | Title III / Art 18(7) | Standard forms and templates for the ART authorization application | *(MiCA-specific gap)* |
| RTS 2025/293 | RTS | Title III / Art 31(5) | Complaints-handling procedures for ART issuers | no direct carrier; adopter provides a MiCA complaints procedure (`compliance/procedure-capa.md` is internal CAPA, not consumer complaints) |
| RTS 2025/1141 | RTS | Title III / Art 32(5) | Conflicts-of-interest policy for ART issuers | library conflicts-of-interest control |
| RTS 2025/413 | RTS | Title III / Art 42(4) | Information to assess a proposed acquisition of a qualifying holding in an ART issuer | *(MiCA-specific gap; the proposed acquirer's disclosure is MiCA-specific)* |
| RTS 2025/1264 | RTS | Title III / Art 45(7) | Minimum contents of the liquidity-management policy for issuers of significant ARTs and significant EMTs (and non-significant classes where the competent authority requires) | library liquidity and resilience controls (adopter maps); the MiCA-specific content is a gap |
| RTS 2025/418 | RTS | Title III / Art 45(7) | Governance of the remuneration policy for issuers of significant ARTs and significant EMTs (and non-significant classes where the competent authority requires) | *(MiCA-specific gap; the library carries no remuneration-governance control)* |
| RTS 2025/303 | RTS | Title V / Art 60(13) | Information notified by financial entities intending to provide crypto-asset services | governance notification controls (adopter maps); the MiCA notification is a gap |
| ITS 2025/304 | ITS | Title V / Art 60(14) | Standard forms and templates for the financial-entity notification | *(MiCA-specific gap)* |
| RTS 2025/305 | RTS | Title V / Art 62(5) | Information in an application for authorization as a CASP | governance authorization controls (adopter maps); the MiCA application is a gap |
| ITS 2025/306 | ITS | Title V / Art 62(6) | Standard forms and templates for the CASP authorization application | *(MiCA-specific gap)* |
| RTS 2025/299 | RTS | Title V / Art 68(10) | Continuity and regularity in the performance of crypto-asset services | `resilience/` continuity controls |
| RTS 2025/1140 | RTS | Title V / Art 68(10) | Records of all crypto-asset services, activities, orders, and transactions | `crypto/register-crypto-asset-inventory.md` and library record-keeping controls |
| RTS 2025/294 | RTS | Title V / Art 71(5) | Complaints-handling procedures for CASPs | no direct carrier; adopter provides a MiCA complaints procedure |
| RTS 2025/1142 | RTS | Title V / Art 72(5) | Conflicts-of-interest policy for CASPs | library conflicts-of-interest control |
| RTS 2025/416 | RTS | Title V / Art 76(16) | Content and format of order-book records for trading-platform CASPs | `operations/` logging and record controls (adopter maps); the MiCA format is a gap |
| RTS 2025/414 | RTS | Title V / Art 84(4) | Information to assess a proposed acquisition of a qualifying holding in a CASP | *(MiCA-specific gap; the proposed acquirer's disclosure is MiCA-specific)* |
| ITS 2024/2861 | ITS | Title VI / Art 88(4) | Technical means for public disclosure and delay of inside information | *(MiCA-specific gap; supplies the Art 88 technical means for reference)* |
| RTS 2025/885 | RTS | Title VI / Art 92(2) | Arrangements, systems, and procedures to prevent, detect, and report market abuse | `operations/procedure-threat-intelligence-and-siem-operations.md`, `security/standard-logging-and-monitoring.md` (monitoring base; the detection template and report are MiCA-specific) |
| RTS 2025/297 | RTS | Title VII / Art 119(8) | Conditions for the establishment and functioning of consultative supervisory colleges | *(supervisory-architecture matter; no adopter artefact)* |

## Library gaps requiring additional documentation

1. **Crypto-asset white papers** (Title II Annex I; ART Annex II; EMT Annex III), MiCA-specific, per category.
2. **Reserve-of-assets construction, segregation, custody, and six-monthly independent audit** for ARTs (Arts 36-38).
3. **Own-funds / prudential-safeguards calculation** (Arts 35, 67; Annex IV).
4. **Client-asset segregation and insolvency-protection evidence** (Arts 70, 75).
5. **Recovery and redemption plans** (Arts 46-47, 55).
6. **RTS/ITS-templated submissions**, complaints (2025/293, 2025/294), conflicts (2025/1141, 2025/1142), records (2025/1140), order-book (2025/416), liquidity (2025/1264), remuneration (2025/418), market-abuse detection (2025/885), and the authorization and notification submissions, where the RTS specify the required information and their paired ITS provide the forms (2025/305, 2025/306, 2025/303, 2025/304, 2025/1125, 2025/1126).

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| MiCA | Regulation (EU) 2023/1114 | Primary regulation |
| MiCA RTS and ITS | Multiple 2024-2025 Delegated/Implementing Regulations (cited in the Title tables and the library-gaps list above) | Implementing detail |
| DORA | Regulation (EU) 2022/2554 | ICT risk management cross-referenced by MiCA Arts 34(10)/(11), 68(7)/(8) |
| Directive 2009/110/EC (EMD2) | E-money directive | Governs EMT issuers (Art 48(3)) |
| Directive (EU) 2015/849 (AMLD) | Anti-money-laundering | CASP AML obligations (Arts 60, 68, 76) |
| ISO/IEC 27001:2022 | Annex A | Underlying control catalogue |

## Limitations

This annex is a CC BY-SA 4.0 navigation aid. MiCA compliance requires category-correct classification, regulator-specific white papers and submissions on the RTS/ITS templates, evidence at the granularity the RTS require, and supervisory engagement with the competent authority (and EBA for significant tokens). Adopting entities consult the regulation, the published RTS and ITS, and the EBA/ESMA/competent-authority guidance applicable to their role. This annex is not legal advice and does not establish compliance.
