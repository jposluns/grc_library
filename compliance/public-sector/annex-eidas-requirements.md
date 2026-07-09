# eIDAS Sector Requirements Annex

**Document Title:** eIDAS Sector Requirements Annex\
**Document Type:** Annex\
**Version:** 0.0.1\
**Date:** 2026-07-09\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/README.md`](../README.md), [`compliance/public-sector/README.md`](README.md), [`compliance/public-sector/annex-public-sector-requirements.md`](annex-public-sector-requirements.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](../register-global-regulatory-applicability.md), [`security/policy-identity-and-access-management.md`](../../security/policy-identity-and-access-management.md), [`security/standard-authentication-and-password-management.md`](../../security/standard-authentication-and-password-management.md), [`security/procedure-identity-management.md`](../../security/procedure-identity-management.md), [`compliance/annex-nis-2-implementation.md`](../annex-nis-2-implementation.md)\
**Classification:** Public\
**Category:** Compliance: Sector-Specific\
**Review Frequency:** Annual and upon material eIDAS implementing-act, EUDI-wallet specification, or trust-service supervision change\
**Repository Path:** [`compliance/public-sector/annex-eidas-requirements.md`](annex-eidas-requirements.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex describes how an organization in scope of the EU electronic identification and trust services framework (eIDAS) can use the core GRC library to meet its obligations, and where the framework requires artefacts and processes the library does not itself produce. The governing instrument is Regulation (EU) No 910/2014 as amended by Regulation (EU) 2024/1183 (the European Digital Identity Framework, commonly "eIDAS2"), which introduced the European Digital Identity Wallet, the wallet-relying-party regime, and a strengthened trust-services and supervision model.

This annex does not reproduce the text of the Regulation, its implementing acts, or national law. It cites obligations by their article identifier so a reader can locate the controlling text, and adopting organizations consume that text from the official source. Because obligations differ sharply by the role an organization occupies, the annex is organized around role determination and by-role obligations rather than around a single control baseline.

---

## Applicability triggers

The framework is relevant where the organization:

1. **Relies on the European Digital Identity Wallet** to identify or authenticate users for a public or private service (a wallet-relying party).
2. **Provides a trust service** (qualified or non-qualified): electronic signatures or seals, timestamps, registered delivery, website authentication certificates, or electronic attestation of attributes.
3. **Is a public-sector body** that must accept the wallet for access to its services.
4. **Provides or operates a European Digital Identity Wallet** on behalf of, under a mandate from, or recognized by a Member State.

The framework is not relevant where the organization neither relies on the wallet, provides a trust service, nor is a public-sector body within its scope. eIDAS obligations are additional to, not a substitute for, any NIS2 obligations a trust-service provider also bears (see Role determination).

---

## Role determination

Obligations differ by role, so role determination is the first operational step. An organization can hold more than one role.

| Role | Test | Principal obligations |
| --- | --- | --- |
| Wallet-relying party | Relies on the wallet to provide a public or private service | Registration, data minimization, self-identification, pseudonym acceptance (Article 5b) |
| Trust-service provider | Provides a qualified or non-qualified trust service | The qualified/non-qualified requirements and supervision; NIS2 security-measure alignment (Articles 16, 19a, and the trust-service articles) |
| Public-sector body | A public body whose services users access | Accept the wallet for access to its services (Article 5f(1), no transition clock) |
| Wallet provider | Provides a wallet directly, under a mandate, or recognized by a Member State | The wallet's functional, assurance, and user-control requirements (Article 5a) |

---

## Obligations by role

This section states obligations at the article level and does not reproduce the regulatory text.

### Wallet-relying party (Article 5b)

- **Register** in the Member State of establishment before relying on the wallet (Article 5b(1)), declaring at least the Member State, the relying party's name and (where applicable) registration number, contact details, and the intended use including the data to be requested (Article 5b(2)).
- **Request no more than the declared, necessary data** (data minimization, Article 5b(3)).
- **Self-identify to the user** (Article 5b(8)).
- **Accept pseudonyms** where identification is not required by Union or national law, and remain responsible for authenticating and validating the requested attributes (Article 5b(9)).
- **Intermediaries** acting for a relying party are themselves relying parties and must not store the transaction content (Article 5b(10)).
- **Notify changes** to the registration information without delay (Article 5b).

A phased acceptance obligation applies to certain private-sector relying parties: private relying parties (other than micro and small enterprises) that are required by law to use strong user authentication in defined sectors (including transport, energy, banking, financial services, social security, health, drinking water, postal services, digital infrastructure, education, and telecommunications) must, on the user's voluntary request, accept the wallet no later than 36 months from the entry into force of the relevant implementing acts (Article 5f(2)). This clock is relative to the implementing acts, not a fixed calendar date.

### Trust-service provider (qualified and non-qualified)

- The framework distinguishes **qualified** from **non-qualified** trust services, with a supervision split and the EU trust mark reserved to qualified services. Non-qualified providers meet the Article 19a requirements; qualified providers meet the qualified-service requirements and are supervised accordingly.
- Qualified electronic attestation of attributes is verified against authentic sources.
- **NIS2 overlap:** a trust-service provider is typically also a NIS2 essential entity ("trust service providers" are named in the NIS2 essential-entity list). eIDAS supervision cooperates with the NIS2 competent authorities, and the penalties provision applies "without prejudice to Article 31 of Directive (EU) 2022/2555" (Article 16(1)); Article 19a aligns non-qualified-provider security measures with the NIS2 regime. See the [NIS2 implementation annex](../annex-nis-2-implementation.md).

### Public-sector body (Article 5f(1))

- Must accept the wallet for access to its services where user authentication is required, with no transition clock (immediate on the wallet's availability).

### Wallet provider (Article 5a)

- Provide at least one wallet within 24 months of the entry into force of the implementing acts (Article 5a(1); a clock relative to the implementing acts, not a fixed date).
- Meet assurance level **high**, in particular for identity proofing and verification, provided under an electronic identification scheme with assurance level high (Article 5a(5)(d), (11)).
- Provide the user-control functions: selective disclosure of person identification data, locally-stored encrypted pseudonyms, wallet-to-wallet authentication, and a common dashboard logging all transactions, listing relying parties, enabling GDPR Article 17 erasure requests, and enabling a report of a relying party to the data protection authority (Article 5a(4)).
- Ensure that the user has full control and that no use information beyond what is necessary is collected (Article 5a(14)); provision is voluntary for users and free of charge for natural persons (Article 5a(13), (15)).
- Obtain conformity certification of the wallet by a designated conformity assessment body (Article 5c).

---

## Library coverage and gaps

The library provides the identity, authentication, and supply-chain baselines that support the relying-party and trust-service roles. Adopting organizations implement and evidence the controls; the wallet, the national registration, and the conformity certification are artefacts and processes the organization obtains outside the library.

| eIDAS obligation | Library coverage |
| --- | --- |
| Relying-party authentication and identity proofing (Article 5b(9)) | [`security/policy-identity-and-access-management.md`](../../security/policy-identity-and-access-management.md), [`security/standard-authentication-and-password-management.md`](../../security/standard-authentication-and-password-management.md), [`security/procedure-identity-management.md`](../../security/procedure-identity-management.md) |
| Assurance-level-high identity context (Article 5a(11)) | [`security/framework-zero-trust-architecture.md`](../../security/framework-zero-trust-architecture.md) (identity pillar) |
| Data minimization for requested attributes (Article 5b(3)) | [`privacy/policy-privacy-and-data-governance.md`](../../privacy/policy-privacy-and-data-governance.md), the data-minimization principle |
| Trust-service-provider security and supervision (Articles 16, 19a) | [`compliance/annex-nis-2-implementation.md`](../annex-nis-2-implementation.md) (the trust-service provider is a NIS2 essential entity), plus the library security baselines |

Obligations the adopter meets outside the library:

1. **Registration as a relying party** in the Member State of establishment (Article 5b(1)). A national process.
2. **Conformity certification** of a wallet (Article 5c). Performed by a designated conformity assessment body.
3. **The wallet itself**, and the implementing-act technical specifications, which the library does not carry.
4. **National penalty exposure**: Member States set penalties that are effective, proportionate, and dissuasive (Article 16(1)); for trust-service providers, national law must allow administrative fines of a maximum of at least EUR 5 000 000, or, for a legal person, EUR 5 000 000 or 1 % of total worldwide annual turnover in the preceding financial year, whichever is higher (Article 16(2)). This is a floor on the maximum that national transposition must at least reach, not a fixed ceiling.

---

## Operating expectations

1. The organization determines its eIDAS role(s) per data flow and service, since obligations differ by role.
2. A wallet-relying party registers in its Member State of establishment, declares the data it will request, and enforces that it requests no more than the declared, necessary attributes.
3. A trust-service provider aligns its security measures and incident reporting with the NIS2 regime it is also subject to, rather than treating eIDAS and NIS2 as independent.
4. The organization tracks the eIDAS implementing acts, since the wallet-provision and private-relying-party acceptance clocks (24 and 36 months) run from those acts, not from the Regulation's own entry into force.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| eIDAS | Regulation (EU) No 910/2014 as amended by Regulation (EU) 2024/1183 | Electronic identification, the European Digital Identity Wallet, and trust services |
| NIS2 | Directive (EU) 2022/2555, Article 31 | Trust-service-provider supervision and enforcement cooperation (Article 16(1)) |
| GDPR | Regulation (EU) 2016/679, Article 17 | The wallet dashboard's erasure-request function (Article 5a(4)) |
| EU Cybersecurity Act | Regulation (EU) 2019/881 | Cybersecurity certification cross-referenced by the wallet conformity regime (Article 5c) |

---

## Limitations

This annex is a CC BY-SA 4.0 navigation aid. eIDAS compliance requires the organization's national registration or certification, conformance with the implementing acts and national transposition, and supervisory engagement, none of which this library produces. The annex states obligations by article identifier and does not reproduce the regulatory text; adopting organizations consult Regulation (EU) No 910/2014 as amended by Regulation (EU) 2024/1183, its implementing acts, and their national law before relying on any obligation stated here. Because the wallet regime phases in through implementing acts, adopters confirm the current implementing-act status and the resulting deadlines at the time of reliance. This annex is not legal advice.

---

**End of Document**
