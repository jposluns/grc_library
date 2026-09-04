# MiCA Implementation Annex

**Document Title:** MiCA Implementation Annex\
**Document Type:** Annex\
**Version:** 0.0.1\
**Date:** 2026-09-04\
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
3. Issuer of an **e-money token (EMT)** ,  necessarily a credit institution or an electronic money institution (Art 48(1)).
4. **Crypto-asset service provider (CASP)** authorized under Art 63, or a financial entity providing crypto-asset services under Art 60.

MiCA does not apply to crypto-assets that are unique and non-fungible (Art 2(3)) or that qualify as financial instruments, deposits, funds (other than EMTs), or the other instruments listed in Art 2(4). Partial exemptions exist but do not relieve all duties: Art 4(2) disapplies Art 4(1) points (b), (c), (d), and (f) for a Title II offer of a crypto-asset other than an ART or EMT that is made to fewer than 150 persons per Member State acting on their own account, or whose total consideration over twelve months does not exceed EUR 1 000 000, or that is addressed solely to qualified investors (and can only be held by them); the remaining Art 4(1) obligations still apply. Art 16(2) disapplies the Art 16(1) authorization requirement where the ART's average outstanding value over twelve months never exceeds EUR 5 000 000 and the issuer is not linked to a network of other exempt issuers, or the offer is addressed solely to qualified investors and the ART can only be held by them, but the issuer must still draw up an ART white paper and notify it to its competent authority. Consult the article and the relevant RTS for the exact conditions.

## Application timeline

MiCA entered into force on 29 June 2023 (Art 149(1)). It applies in two phases: Titles III (asset-referenced tokens) and IV (e-money tokens) from 30 June 2024, and the remainder, including Title II offers, Title V crypto-asset services, and Title VI market abuse, from 30 December 2024 (Art 149(2) and (3)). A crypto-asset service provider that lawfully provided its services before 30 December 2024 may continue under a transitional regime until 1 July 2026 or until authorization is granted or refused, whichever is sooner, except that a Member State may shorten or disapply that regime (Art 143(3)); an adopter confirms its own Member State's transitional window, since it is not uniform across the Union.

## The three crypto-asset categories (the classification gate)

The obligations that apply turn entirely on which category a token falls in, and the distinction is precise:

- **E-money token (EMT):** purports to maintain a stable value by referencing **one official currency** (Art 3(7)); deemed electronic money (Art 48(2)); issuable only by a credit institution or EMI (Art 48(1)).
- **Asset-referenced token (ART):** any stable-value token that is **not** an EMT ,  referencing another value or right, a combination, or **one or more** official currencies (Art 3(6)); a multi-currency basket stablecoin is an ART, not an EMT.
- **Crypto-asset other than ART or EMT:** the residual category (utility tokens and other non-stable crypto-assets), governed by Title II.

Misclassification propagates into the wrong reserve, redemption, and authorization regime, so the classification is the first control an adopter documents.

## Title II: offers of crypto-assets other than ART or EMT (Arts 4-15)

| MiCA element | Library artefact |
| --- | --- |
| Legal-person requirement, white-paper drafting/notification/publication (Arts 4-9) | *(no core artefact; the white paper is a MiCA-specific supervisory document the offeror drafts to Annex I)* |
| Fair, clear, not-misleading disclosure (Art 6(2)) | `compliance/` disclosure-governance artefacts (adopter maps to the Annex I content schema) |
| Marketing-communications consistency (Art 7) | library marketing/communications controls |

Gap: the Title II crypto-asset white paper (Annex I schema, Art 6) and its notification are MiCA-specific artefacts outside the library.

## Title III: asset-referenced tokens (Arts 16-47)

| MiCA element | Library artefact |
| --- | --- |
| Authorization / fit-and-proper management body (Arts 16, 18, 34(2)) | `risk/policy-enterprise-governance-and-risk-management.md`, `governance/charter-governance-library.md` |
| Governance, internal control, risk management (Art 34) | `risk/standard-enterprise-risk-management.md`, `security/policy-information-security.md` |
| ICT risk management + data safeguarding (Art 34(10)/(11), cross-referencing DORA) | the DORA implementation annex + `security/` standards |
| Business continuity (Art 34(9)) | `resilience/framework-business-continuity-and-resilience.md` |
| Complaints-handling (Art 31; RTS 2025/293) | library complaints/CAPA procedure (adopter extends to the RTS template) |
| Conflicts of interest (Art 32; RTS 2025/1141) | library conflicts-of-interest control |
| Reserve of assets: constitution, segregation, audit (Arts 36-38) | *(MiCA-specific; no core artefact ,  the reserve is a supervised financial construct)* |
| Right of redemption at market value, in principle without a fee but subject to the Art 46 recovery options (Art 39) | *(MiCA-specific policy)* |
| Recovery and redemption plans (Arts 46-47) | `resilience/` continuity/recovery artefacts as the operational base |

Gaps: the reserve-of-assets regime (Arts 36-38 ,  legal/operational segregation, six-monthly independent audit, custody within five working days, investment constraints), the permanent right of redemption at market value (Art 39), own-funds at the highest of EUR 350 000 / 2% of reserve / a quarter of fixed overheads (Art 35, rising to 3% for significant ARTs, Art 45(5); a credit institution issuing ARTs is not subject to Art 35, Art 17(4)), and the recovery/redemption plans (Arts 46-47) are MiCA-specific supervisory artefacts the issuer maintains beyond the library baseline.

## Title IV: e-money tokens (Arts 48-58)

| MiCA element | Library artefact |
| --- | --- |
| Credit-institution / EMI status + white-paper notification (Art 48) | governance/authorization artefacts (status is an external licence) |
| Issue at par value, redeem at par value at any time, in principle without a fee but subject to the Art 46 recovery options (Art 49) | *(MiCA-specific; note: par value, unlike ART market value)* |
| Interest prohibition (Art 50) | *(MiCA-specific policy)* |
| Safeguarding of funds: 30% deposited, remainder in highly liquid low-risk instruments (Art 54) | `risk/` + `supply-chain/` custody controls as inputs |
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
| Safekeeping of clients' crypto-assets and funds; insolvency protection (Art 70) | `security/` + `operations/` custody controls (adopter extends to segregation + next-day placement) |
| Complaints-handling (Art 71; RTS 2025/294) | library complaints procedure |
| Conflicts of interest, reviewed annually (Art 72; RTS 2025/1142) | library conflicts-of-interest control |
| Outsourcing, incl. contingency + exit strategies (Art 73) | `supply-chain/framework-supplier-and-cloud-governance.md`, `supply-chain/procedure-supplier-exit-and-data-return.md`, `supply-chain/standard-supplier-security-and-privacy-assurance.md` |
| Orderly wind-down plan, for CASPs providing the services in Arts 75 to 79 (Art 74) | `resilience/` recovery artefacts |
| Custody-specific: register of positions, custody policy, quarterly statements, legal/operational segregation, liability (Art 75) | `security/` custody controls (adopter maps to Art 75 minimum agreement content) |
| Trading-platform operating rules, order-book records (Art 76; RTS 2025/416) | `operations/` + market-integrity controls |

Gaps: the client-asset segregation and insolvency-protection regime (Arts 70, 75(7)), the five-to-seven-year record-keeping obligation (Art 68(9); RTS 2025/1140), the Annex IV prudential-safeguards calculation (Art 67), and the service-specific operating rules (Arts 75-82) are MiCA-specific and maintained beyond the library baseline.

## Title VI: market abuse (Arts 86-92)

MiCA imposes an EU market-abuse regime on crypto-assets admitted to (or requested for admission to) trading, applying to any person and on or off a trading platform (Art 86). Obligations: public disclosure of inside information (Art 88), and prohibitions on insider dealing (Art 89), unlawful disclosure (Art 90), and market manipulation (Art 91).

| MiCA element | Library artefact |
| --- | --- |
| Prevent-and-detect arrangements + suspicious-transaction reporting (Art 92; RTS 2025/885) | `operations/procedure-threat-intelligence-and-siem-operations.md`, `security/standard-logging-and-monitoring.md` (monitoring base; the market-abuse detection template is MiCA-specific) |
| Inside-information disclosure mechanics (Art 88; ITS 2024/2861) | library disclosure-governance controls |

## Supervisory architecture (Title VII)

MiCA is supervised two-tier: national competent authorities designated under Art 93 supervise CASPs, Title II offerors, and non-significant ART/EMT issuers (a Title II white paper is notified, not approved: the competent authority does not require prior approval, Art 8(3)); **EBA** supervises **significant** ARTs and, for a significant EMT issued by an electronic money institution, compliance with Arts 55 and 58 (Art 117(4)), the significant-token classification triggering EBA's role (Arts 43(7), 56(6)), except that supervision of a significant EMT denominated in a non-euro Member-State currency does not transfer where at least 80% of holders and transactions are domestic (Art 56(7)); **ESMA** maintains the public register of white papers, issuers, and CASPs (Art 109) and, with EBA, develops the RTS/ITS; the **ECB and national central banks** hold monetary-sovereignty opinion rights over tokens referencing their currency (Arts 17(5), 43). An adopter identifies its home-Member-State competent authority (and, for a significant token, EBA) as its supervisor.

## Library gaps requiring additional documentation

1. **Crypto-asset white papers** (Title II Annex I; ART Annex II; EMT Annex III) ,  MiCA-specific, per category.
2. **Reserve-of-assets construction, segregation, custody, and six-monthly independent audit** for ARTs (Arts 36-38).
3. **Own-funds / prudential-safeguards calculation** (Arts 35, 67; Annex IV).
4. **Client-asset segregation and insolvency-protection evidence** (Arts 70, 75).
5. **Recovery and redemption plans** (Arts 46-47, 55, 74).
6. **RTS/ITS-templated submissions** ,  complaints (2025/293, 2025/294), conflicts (2025/1141, 2025/1142), records (2025/1140), order-book (2025/416), liquidity (2025/1264), remuneration (2025/418), market-abuse detection (2025/885), and the authorization and notification submissions, where the RTS specify the required information and their paired ITS provide the forms (2025/305, 2025/306, 2025/303, 2025/304, 2025/1125, 2025/1126).

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| MiCA | Regulation (EU) 2023/1114 | Primary regulation |
| MiCA RTS and ITS | Multiple 2024-2025 Delegated/Implementing Regulations (see the RTS/ITS table) | Implementing detail |
| DORA | Regulation (EU) 2022/2554 | ICT risk management cross-referenced by MiCA Arts 34(10)/(11), 68(7)/(8) |
| Directive 2009/110/EC (EMD2) | E-money directive | Governs EMT issuers (Art 48(3)) |
| Directive (EU) 2015/849 (AMLD) | Anti-money-laundering | CASP AML obligations (Arts 60, 68, 76) |
| ISO/IEC 27001:2022 | Annex A | Underlying control catalogue |

## Limitations

This annex is a CC BY-SA 4.0 navigation aid. MiCA compliance requires category-correct classification, regulator-specific white papers and submissions on the RTS/ITS templates, evidence at the granularity the RTS require, and supervisory engagement with the competent authority (and EBA for significant tokens). Adopting entities consult the regulation, the published RTS and ITS, and the EBA/ESMA/competent-authority guidance applicable to their role. This annex is not legal advice and does not establish compliance.
