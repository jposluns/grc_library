# Crypto-Asset Domain Inventory Register

**Document Title:** Crypto-Asset Domain Inventory Register\
**Document Type:** Register\
**Version:** 0.0.1\
**Date:** 2026-09-11\
**Owner:** Crypto-Asset Governance Approver\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`crypto/README.md`](README.md), [`crypto/framework-crypto-asset-governance.md`](framework-crypto-asset-governance.md), [`crypto/standard-digital-asset-custody.md`](standard-digital-asset-custody.md), [`crypto/standard-crypto-asset-service-provider-vetting.md`](standard-crypto-asset-service-provider-vetting.md), [`security/framework-cryptographic-key-lifecycle.md`](../security/framework-cryptographic-key-lifecycle.md), [`operations/register-asset-inventory.md`](../operations/register-asset-inventory.md)\
**Classification:** Public\
**Category:** Crypto-Asset Governance\
**Review Frequency:** 6 to 12 months and upon material holding, platform, custody-arrangement, or contract change\
**Repository Path:** [`crypto/register-crypto-asset-inventory.md`](register-crypto-asset-inventory.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register is the authoritative, organization-neutral record of the crypto-assets the organization holds, the wallets, accounts, and custody arrangements through which they are controlled, the blockchain platforms in use, and the smart contracts it has deployed. It is the domain inventory that the [Crypto-Asset Governance Framework](framework-crypto-asset-governance.md) mandates as Governance requirement 4, and against which the [Digital Asset Custody Standard](standard-digital-asset-custody.md) reconciles. It records the RESULT of the framework's classification and approval controls; it does not restate the rules that produce those results.

## Scope

The register covers the four object classes the framework's inventory obligation enumerates: crypto-assets held, wallets and custody arrangements, platforms in use, and deployed smart contracts. It applies whether an asset is held on the organization's own account or on behalf of clients, and it records the platform's network characteristics as an attribute of the platform rather than as a separate object. An entry exists before an asset is issued, offered, custodied, traded, or otherwise used, per the framework's classification-timing control. The per-client register of positions that a custodian keeps under the custody standard (MiCA Article 75(2)) is a distinct artefact; this register records that a custody arrangement exists and its reconciliation status, not the client-level positions.

## Crypto-asset classification

Each asset records the classification result assigned under the framework's classification rules: its MiCA class (asset-referenced token, e-money token, or other crypto-asset) or its recorded exclusion (a financial instrument under Directive 2014/65/EU, or a genuinely unique and non-fungible crypto-asset). The classification rules and their re-check triggers live in the framework and are referenced, not reproduced; a change to an asset or its terms re-opens the classification and updates this record.

## Record schema

### Crypto-assets held

Each crypto-asset holding records: an internal asset identifier; the asset name, ticker, and on-chain identifier (for example a token contract address); the recorded MiCA class or exclusion; the holding basis (proprietary or custodied for clients); the platform and ledger on which it exists; the wallet or account reference and the custody arrangement (self-custody, third-party custodian, or hybrid); a pointer to the key-control record in the [cryptographic key lifecycle](../security/framework-cryptographic-key-lifecycle.md) where the organization controls the keys; the classification and activity-approval status required by the framework's Governance requirements 1 and 2; a pointer to the service-provider relationship record in the [provider-vetting standard](standard-crypto-asset-service-provider-vetting.md) where a provider is involved; the accountable owner; and the date the entry was added and last reviewed.

### Platforms in use

Each platform records its permission model (permissionless or permissioned), its consensus family, and the failure modes and fork-governance history relevant to its assurance, drawing on the technology characteristics NIST IR 8202 describes; the data-visibility model; and a reference to the platform-vetting decision the framework requires as a precondition to use. This register records the platform's identity and characteristics; the framework owns the vetting judgement.

### Wallets and custody arrangements

Each wallet or custody arrangement records its reference, the custody model, and the accountable owner, and points to the custody standard for the wallet architecture, key custody, and register-of-positions controls it must satisfy. This register records existence and reconciliation status; the custody standard owns the mechanics.

### Deployed smart contracts

Each deployed contract records its on-chain address, its platform, its purpose, and the accountable owner for its upgrade and change governance, which is an organizational control this domain exercises over the contracts it deploys.

## Governance and maintenance

The Crypto-Asset Governance Approver is accountable for the register's completeness and accuracy. An entry is created before the asset is issued, offered, custodied, traded, or otherwise used, and is re-checked when the asset, its terms, its platform, or its custody arrangement materially changes. The domain inventory, the custody standard's register of positions, and the on-chain balances are reconciled on an organization-defined cadence, and a reconciliation discrepancy is handled as a custody incident. Where the organization is itself a crypto-asset service provider, the records MiCA requires are kept for the five-year period Article 68 sets (extendable to seven where a competent authority so requests before five years elapse); this register defers the retention duration to the corpus records-retention controls where the organization is not a provider.

## Lifecycle management

An entry moves through the states registered, active, terms-changed or re-classified, and disposed or derecognized, each with its trigger and the action it requires. Disposal of a custodied asset references the custody standard's return and recovery controls; disposal of a deployed contract records the change-governance decision that retired it.

## Limitations

This is original library content and reproduces no external control text; MiCA-grounded record and retention requirements are named at the point of use, and an organization under another regime applies its own governing law. The register records the results of the framework's classification, approval, and platform-vetting controls and the custody standard's custody controls; it does not restate those rules, and it owns only the inventory record itself, its schema, its maintenance cadence, and the reconciliation obligation. NIST IR 8202 is an informative 2018 technical report, used only for platform and network characteristics, not as a normative control. Anti-money-laundering, counter-terrorist-financing, and travel-rule obligations are out of scope for this register, consistent with the domain's stated limitations.

**End of Document**
