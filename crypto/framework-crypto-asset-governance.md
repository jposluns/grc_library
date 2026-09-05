# Crypto-Asset Governance Framework

**Document Title:** Crypto-Asset Governance Framework\
**Document Type:** Framework\
**Version:** 0.1.2\
**Date:** 2026-09-05\
**Owner:** Crypto-Asset Governance Approver\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`crypto/README.md`](README.md), [`crypto/standard-digital-asset-custody.md`](standard-digital-asset-custody.md), [`compliance/financial-services/annex-mica-implementation.md`](../compliance/financial-services/annex-mica-implementation.md), [`security/framework-cryptographic-key-lifecycle.md`](../security/framework-cryptographic-key-lifecycle.md), [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md), [`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md)\
**Classification:** Public\
**Category:** Crypto-Asset Governance\
**Review Frequency:** 6 to 12 months and upon material crypto-asset activity, platform, threat, or regulatory change\
**Repository Path:** [`crypto/framework-crypto-asset-governance.md`](framework-crypto-asset-governance.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This framework is the governance anchor for the crypto-asset and blockchain domain. It sets the organization-neutral control model for holding, using, issuing, or servicing crypto-assets and for adopting distributed-ledger (blockchain) technology, so that crypto-asset activity is classified, approved, inventoried, and risk-managed before it begins rather than after an incident.

It complements, and does not duplicate, the EU Markets in Crypto-Assets Regulation implementation annex ([`compliance/financial-services/annex-mica-implementation.md`](../compliance/financial-services/annex-mica-implementation.md)). The annex maps a specific regime's obligations to library artefacts; this framework and the domain documents beneath it hold the reusable, regime-neutral requirements the mapping points at. Where a requirement below is grounded in a specific instrument, that instrument is named at the point of use; the requirement itself is written to be adoptable by an organization that is not itself in scope of that instrument.

## Scope

The framework covers an organization in any of these positions: a holder or user of crypto-assets; an issuer or offeror; an operator of, or participant in, a crypto-asset trading platform; a custodian of crypto-assets on behalf of others; a participant in staking or other on-chain reward mechanisms; a deployer or user of smart contracts; and an adopter evaluating whether to use a blockchain platform at all. It is technology-model-neutral (permissioned and permissionless platforms alike) and organization-neutral: an adopter applies the sections that match its activities.

Anti-money-laundering, counter-terrorist-financing, and the crypto-asset transfer "travel rule" are out of scope of this release and are addressed in the Limitations section.

## Crypto-asset classification

Classification is the first control: what an asset is determines which obligations attach to it, so no crypto-asset activity should proceed before the asset is classified. Under Regulation (EU) 2023/1114 (MiCA), the primary classification is three-way: an asset-referenced token (ART), an electronic money token (EMT), or a crypto-asset that is neither (the residual "other" category): MiCA Recital 18 sets out this three-way classification, Article 3 defines the ART and EMT types, and Titles III, IV, and II respectively carry the issuer and offeror obligations for ARTs, EMTs, and other crypto-assets. Two exclusions bound the field before classification begins: a crypto-asset that qualifies as a financial instrument within the meaning of Directive 2014/65/EU is regulated as such and falls outside MiCA, and a crypto-asset that is genuinely unique and not fungible with other crypto-assets is likewise outside MiCA's scope (MiCA Article 2). An organization outside the European Union applies the same classification discipline against its own governing regime; the three-category structure is used here as the worked model because it is the regime the library currently holds in full.

The governing control is that classification is documented, re-checked when an asset or its terms change, and recorded in the domain inventory (see Governance requirements) before the asset is issued, offered, custodied, traded, or otherwise used.

## Platform and technology model

Blockchain platforms divide first by permission model: a permissionless platform lets any party read, submit transactions, and participate in reaching consensus, whereas a permissioned platform restricts one or more of those roles to authorized participants (NIST IR 8202, Blockchain Technology Overview, section 2). The permission model drives the governance posture: who can transact, who can see data, and who decides the ledger's state.

Consensus is the mechanism by which a platform agrees its next state, and consensus families differ in their trust and failure assumptions: proof of work, proof of stake, round-robin, proof of authority or identity, and proof of elapsed time are the families surveyed in NIST IR 8202 section 4. Each family implies different concentration, censorship, and finality risks that a governance review must weigh. A fork, a divergence in the ledger's history or rules, is a governance event, not merely a technical one: it can split an asset, change the rules under which it is held, and require an explicit hold-or-follow decision (NIST IR 8202 section 5).

The framework's platform control is that a platform is vetted against its permission model, its consensus mechanism and that mechanism's failure modes, its fork-governance history, its data-visibility and throughput properties, and the prior question of whether a blockchain is needed at all, before it is adopted. The detailed vetting procedure is a separate domain document; this framework requires that the vetting occur.

## Risk domains

The domain's material risks group as follows. Custody and key-loss risk: control of a crypto-asset is control of its private keys, and loss or destruction of key material is loss of the asset, and theft of a key gives an attacker full control of the associated assets (NIST IR 8202 section 3.4.1 on private-key storage); MiCA requires a crypto-asset service provider that holds crypto-assets for clients to safeguard their ownership rights and keep those assets in safekeeping (Article 70); separately, a provider providing custody and administration of crypto-assets is liable for a loss of a client's crypto-asset that results from an incident attributable to it, capped at the market value of the lost asset at the time the loss occurred (Article 75(8)). Technology risk: the properties often assumed of blockchains have limits, including the limits of immutability, the possibility of a platform losing the participation that keeps it alive, and exposure to cyber attack and to malicious participants (NIST IR 8202 section 7). Smart-contract risk: code that executes automatically on-chain carries deployment and external-data (oracle) risks (NIST IR 8202 section 6 introduces smart contracts and oracles, with oracle risk in section 7.3 and deployment weaknesses in section 7.5.1); upgrade and change governance of deployed contracts is an organizational control this domain adds, not a MiCA or IR 8202 attribution. Market and regulatory risk: classification errors, regime change, and market abuse. Third-party and platform-concentration risk: dependence on a small number of platforms, custodians, or validators is a concentration exposure managed through the third-party assurance domain.

These risk domains are assessed within the organization's enterprise risk-management process rather than in a parallel scheme (see Integration points).

## Governance requirements

1. Classification before activity. No crypto-asset is issued, offered, custodied, traded, staked, or otherwise used before it is classified and the classification recorded.
2. Activity approval gate. Any new crypto-asset activity, or a material change to an existing one, is approved through a defined authority before it begins.
3. Platform vetting precondition. A blockchain platform is vetted (permission model, consensus and its failure modes, fork governance, data visibility, throughput, and the need-a-blockchain question) before adoption.
4. Inventory obligation. Crypto-assets held, wallets and custody arrangements, platforms in use, and deployed smart contracts are maintained in a domain inventory.
5. Custody and record-keeping floor. Where crypto-assets are custodied on behalf of others, the arrangement rests on a client agreement whose contents are defined, and records of crypto-asset services, activities, orders, and transactions are kept (MiCA Article 75 on providing custody and administration on behalf of clients, and the record-keeping regulatory technical standard under MiCA, Commission Delegated Regulation (EU) 2025/1140).
6. Role assignment and review. Accountable roles are named, and the framework and its dependent documents are reviewed on the stated cadence and upon material change.

## Integration points

The domain does not re-implement controls that exist elsewhere in the library. Key material and cryptographic-module assurance are governed by the cryptographic key lifecycle and key-management artefacts ([`security/framework-cryptographic-key-lifecycle.md`](../security/framework-cryptographic-key-lifecycle.md) and the related security key procedures); crypto-asset custody requirements relate to those rather than duplicating them. Crypto-asset risks are assessed within enterprise risk management ([`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md)). Platform, custodian, and validator dependencies are managed as third-party relationships ([`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md)). Continuity of a crypto-asset service is a resilience concern, aligned with the MiCA service-continuity regulatory technical standard (Commission Delegated Regulation (EU) 2025/299). Regime-specific obligation mapping lives in the MiCA implementation annex ([`compliance/financial-services/annex-mica-implementation.md`](../compliance/financial-services/annex-mica-implementation.md)).

## Limitations

Anti-money-laundering, counter-terrorist-financing, and the crypto-asset transfer travel rule are not covered in this release; the Financial Action Task Force guidance that grounds that content is not yet held in the reference base, and the gap is stated here rather than filled with unsourced material. It will be addressed in a dedicated document once the source is acquired.

The technology grounding in this framework draws on NIST IR 8202, which is a NIST Internal Report, a foundational technical overview, not a formal standard, and dates from 2018; its consensus-landscape detail is treated as orientation, not as a current market survey. The regime grounding draws on the EU MiCA regulation, which the library holds in full; an organization under a different regime applies the same control structure against its own governing law, and per-regime jurisdiction annexes are a planned extension of this domain as further sources are held.
