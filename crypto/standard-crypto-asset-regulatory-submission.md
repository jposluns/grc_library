# Crypto-Asset MiCA Regulatory Submission and Templated-Filing Standard

**Document Title:** Crypto-Asset MiCA Regulatory Submission and Templated-Filing Standard\
**Document Type:** Standard\
**Version:** 0.0.1\
**Date:** 2026-09-12\
**Owner:** Crypto-Asset Governance Approver\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`crypto/README.md`](README.md), [`crypto/framework-crypto-asset-governance.md`](framework-crypto-asset-governance.md), [`crypto/standard-crypto-asset-reserve-and-prudential-requirements.md`](standard-crypto-asset-reserve-and-prudential-requirements.md), [`crypto/standard-crypto-asset-white-paper-disclosure.md`](standard-crypto-asset-white-paper-disclosure.md), [`crypto/standard-crypto-asset-service-provider-vetting.md`](standard-crypto-asset-service-provider-vetting.md), [`compliance/financial-services/annex-mica-implementation.md`](../compliance/financial-services/annex-mica-implementation.md)\
**Classification:** Public\
**Category:** Crypto-Asset Governance\
**Review Frequency:** 6 to 12 months and upon material regulatory, submission-template, or filing-obligation change\
**Repository Path:** [`crypto/standard-crypto-asset-regulatory-submission.md`](standard-crypto-asset-regulatory-submission.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard states the organization-neutral controls that govern how a crypto-asset market participant prepares, attests, submits, and maintains the regulatory filings the Markets in Crypto-Assets Regulation (Regulation (EU) 2023/1114, MiCA) and its implementing and regulatory technical standards require: the asset-referenced-token issuer authorization application, the crypto-asset-service-provider authorization application, the notification by an already-authorized financial entity intending to provide crypto-asset services, and the ongoing obligations and event-driven notifications that follow authorization. It is the submitter-side control layer: what an applicant must assemble, how it attests to completeness and accuracy, which delegated-regulation form or template carries each submission, and how it keeps a submitted file current.

This standard is distinct from [`crypto/standard-crypto-asset-service-provider-vetting.md`](standard-crypto-asset-service-provider-vetting.md), which is written from the adopter-as-customer view (how an organization vets a third-party provider it engages); this standard is the applicant-as-submitter view (how an organization assembles its own regulatory submission). It cross-references [`crypto/standard-crypto-asset-reserve-and-prudential-requirements.md`](standard-crypto-asset-reserve-and-prudential-requirements.md) and [`crypto/standard-crypto-asset-white-paper-disclosure.md`](standard-crypto-asset-white-paper-disclosure.md) for the underlying reserve, prudential, and white-paper obligations whose evidence a submission carries, and the regulation-to-library navigation map is [`compliance/financial-services/annex-mica-implementation.md`](../compliance/financial-services/annex-mica-implementation.md).

This standard states the submission-governance controls and cites the article and delegated regulation at the point of use; it does not reproduce the implementing-technical-standard forms and templates verbatim.

## 2. Applicability

This standard applies to:

- An asset-referenced-token issuer applying for authorization under MiCA Article 18 (section 3.2).
- A person applying for authorization as a crypto-asset service provider under MiCA Article 62 (section 3.3).
- A financial entity already authorized under Union law that intends to provide crypto-asset services and notifies its competent authority under MiCA Article 60 (section 3.5).
- Any authorized issuer or provider maintaining the ongoing obligations and event-driven notifications that follow authorization (section 3.6).

A credit institution issuing an asset-referenced token submits its white paper for approval under MiCA Article 17 rather than seeking Article 21 authorization, and files the crypto-asset-specific information Article 17 requires on top of the banking authorization it already holds; the Regulation (EU) 2025/1125 content set in section 3.2 governs the Article 18 authorization route, not this Article 17 route. An asset-referenced-token issuer whose offer is exempt from authorization under Article 16(2) does not file an Article 18 authorization application; it draws up and notifies its white paper (governed by [`crypto/standard-crypto-asset-white-paper-disclosure.md`](standard-crypto-asset-white-paper-disclosure.md)) and maintains the applicable ongoing obligations of section 3.6, rather than filing an Article 18 authorization.

## 3. Requirements

### 3.1 Common submission spine and completeness attestation

Every MiCA authorization submission is assembled against the delegated regulation that specifies its required information, submitted on the standard form and template the paired implementing technical standard prescribes, and lodged through the channel the competent authority designates (an internet-portal upload where the implementing standard so provides). The submission carries the completeness attestation in the mandated terms, certifying that the information is true, accurate, complete, up to date, and not misleading, with any future-dated information identified as such (the asset-referenced-token attestation is in the ITS (EU) 2025/1126 Annex; the crypto-asset-service-provider attestation is in the ITS (EU) 2025/306 Annex).

An incomplete application is notified to the applicant with a deadline for the missing information, and the substantive assessment runs from receipt of a complete application rather than from lodgement, while the completeness review begins on initial receipt (ITS (EU) 2025/1126 Article 2; MiCA Article 20). The applicant therefore treats completeness as the trigger and assembles the full evidence set before submitting.

### 3.2 Asset-referenced-token issuer authorization submission

An asset-referenced-token issuer's authorization application under MiCA Article 18 contains the information specified by Regulation (EU) 2025/1125 (based on Article 18(6)), submitted on the form and template of Regulation (EU) 2025/1126 (based on Article 18(7)):

- The identity and legal-status information of the applicant issuer (RTS (EU) 2025/1125 Article 1).
- A programme of operations setting out the business model, strategy, and risk assessment (Article 2).
- A business plan explaining initial viability and ongoing sustainability over at least three years (Article 3).
- The internal-governance and structural-organization description: the organigram, the management-body terms of reference, the human and technical resources, and the code of conduct (Article 4).
- The internal-control framework: the compliance function, the risk-management framework, the information-and-communication-technology arrangements aligned with the Digital Operational Resilience Act (Regulation (EU) 2022/2554), and business-continuity arrangements (Article 5).
- The liquidity-management, reserve-of-assets, and redemption-right evidence: reserve constitution, composition, and segregation, and the stabilization-mechanism policy (Article 6), for which the operational controls are carried by [`crypto/standard-crypto-asset-reserve-and-prudential-requirements.md`](standard-crypto-asset-reserve-and-prudential-requirements.md).
- The fit-and-proper evidence for each management-body member: good repute, knowledge, skills, experience, and sufficient time commitment (Article 7).
- The identity and suitability of shareholders and members with qualifying holdings, with the qualifying-holding assessment following Regulation (EU) 2025/413 (Article 8).

The application also incorporates the asset-referenced-token white paper, whose content controls are in [`crypto/standard-crypto-asset-white-paper-disclosure.md`](standard-crypto-asset-white-paper-disclosure.md); on authorization that white paper is deemed approved (MiCA Article 21(1)).

### 3.3 Crypto-asset-service-provider authorization submission

A person seeking authorization as a crypto-asset service provider under MiCA Article 62 assembles the information specified by Regulation (EU) 2025/305 (based on Article 62(5)) and submits it on the form of Regulation (EU) 2025/306 (based on Article 62(6)):

- General identity and legal-status information (RTS (EU) 2025/305 Article 1).
- A programme of operations over three years (Article 2).
- The prudential safeguards evidence for the Article 67 requirement (Article 3).
- The governance, internal-control, and conflicts-of-interest arrangements (Article 4).
- The service-specific modules for the services the applicant intends to provide, keyed to the MiCA Article 62(2) points, including the custody-and-administration standard client agreement (Article 75(1)), the trading-platform operating rules and market-abuse-detection arrangements, and the further per-service modules (RTS (EU) 2025/305 Articles 12 to 17, section 3.4).

The competent authority acknowledges receipt of the application (ITS (EU) 2025/306; MiCA Article 63).

### 3.4 Service-specific submission modules

Where the applicant intends to provide a specific crypto-asset service, it files the corresponding evidence: for custody and administration, the standard client agreement (Regulation (EU) 2025/305 Article 12, MiCA Article 75(1)) and the register of positions (MiCA Article 75(2)); for operating a trading platform, the operating rules, admission criteria, and market-abuse-detection and reporting arrangements (Article 13); for execution of orders, the execution and best-execution arrangements (Article 15); for reception and transmission of orders, the procedures and arrangements evidencing MiCA Article 80 compliance (Article 2(2)); for placing, the conflicts-of-interest procedures and the MiCA Article 79 arrangements (Article 2(3)); for exchange of crypto-assets, the commercial policy and pricing methodology (Article 14); and the further per-service modules of Regulation (EU) 2025/305 for advice, portfolio management, and transfer services. A module is filed for each service sought and omitted for services not sought.

### 3.5 Financial-entity notification submission

A financial entity already authorized under Union law that intends to provide crypto-asset services notifies its competent authority under MiCA Article 60, at least 40 working days before it begins, assembling the information specified by Regulation (EU) 2025/303 (based on Article 60(13)) on the form of Regulation (EU) 2025/304 (based on Article 60(14)):

- A programme of operations over three years (RTS (EU) 2025/303 Article 1, MiCA Article 60(7)(a)).
- A business-continuity plan (Article 2, MiCA Article 60(7)(b)).
- The anti-money-laundering and countering-the-financing-of-terrorism arrangements (Article 3).
- The further governance and control evidence the notification requires.

The notification is a leaner filing than a full authorization because the notifying entity already holds an authorization whose governance and prudential base the competent authority has assessed. The competent authority acknowledges the notification within five working days (ITS (EU) 2025/304), and the notifying entity notifies the competent authority of any change to the notified information, without undue delay (ITS (EU) 2025/304 Article 4).

### 3.6 Ongoing obligations and event-driven notifications

After authorization, the issuer or provider maintains the records, policies, and procedures the delegated regulations require and makes the event-driven notifications MiCA sets:

- Record-keeping: a crypto-asset service provider keeps the records the record-keeping regulation lists, retained and kept at the competent authority's disposal (Regulation (EU) 2025/1140).
- Order-book records: a trading-platform crypto-asset service provider records each order in the prescribed electronic, machine-readable format and keeps it at the authority's disposal (Regulation (EU) 2025/416).
- Remuneration governance: an issuer of a significant asset-referenced token or significant e-money token, and a non-significant issuer where the competent authority so requires, maintains the remuneration-policy governance arrangements (Regulation (EU) 2025/418).
- Complaints handling: an issuer and any third-party distributor establishes and maintains the complaints-handling procedures (Regulation (EU) 2025/293 for asset-referenced tokens, and the paired instrument for crypto-asset service providers).
- Conflicts-of-interest policy: the policy content the conflicts regulations specify (Regulation (EU) 2025/1141 for issuers under MiCA Article 32(5), and Regulation (EU) 2025/1142 for crypto-asset service providers under Article 72(5)).

The issuer notifies the competent authority immediately of any change to its management body (MiCA Article 33), and re-files a modified white paper or application under the modification path the governing article sets when a change requires it.

## 4. Evidence requirements

Evidence for this standard comprises the assembled submission file for each authorization or notification lodged, on the prescribed form and template; the completeness attestation in the mandated terms; the competent-authority acknowledgement of receipt and the recorded date of receipt of the complete application; the per-service evidence modules filed for the services sought; the record-keeping, order-book, remuneration, complaints, and conflicts records and policies maintained after authorization; and the change log showing each change notified to the competent authority without undue delay.

## 5. Limitations

This standard states organization-neutral submission-governance controls grounded in MiCA Level 1 (Regulation (EU) 2023/1114) and the enumerated implementing and regulatory technical standards; it is not legal advice, and an adopter confirms the current consolidated text and any amending or superseding delegated act against the authoritative source before relying on a specific instrument. It states the controls and cites the article and delegated regulation at the point of use; it does not reproduce the implementing-technical-standard forms and templates verbatim, and where a delegated instrument referenced by the submission regime is not held it is acquired or the reliance waits. This standard governs the submission and filing lifecycle; the underlying reserve, prudential, white-paper, and custody obligations whose evidence a submission carries are governed by the related crypto-asset standards.

**End of Document**
