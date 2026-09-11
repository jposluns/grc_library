# Smart-Contract and Oracle Risk Standard

**Document Title:** Smart-Contract and Oracle Risk Standard\
**Document Type:** Standard\
**Version:** 0.0.1\
**Date:** 2026-09-11\
**Owner:** Crypto-Asset Governance Approver\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`crypto/README.md`](README.md), [`crypto/framework-crypto-asset-governance.md`](framework-crypto-asset-governance.md), [`crypto/register-crypto-asset-inventory.md`](register-crypto-asset-inventory.md), [`crypto/standard-crypto-asset-service-provider-vetting.md`](standard-crypto-asset-service-provider-vetting.md), [`crypto/standard-digital-asset-custody.md`](standard-digital-asset-custody.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`dev-security/policy-secure-development-and-engineering.md`](../dev-security/policy-secure-development-and-engineering.md), [`security/standard-threat-modelling.md`](../security/standard-threat-modelling.md)\
**Classification:** Public\
**Category:** Crypto-Asset Governance\
**Review Frequency:** 6 to 12 months and upon material contract, platform, oracle, or regulatory change\
**Repository Path:** [`crypto/standard-smart-contract-and-oracle-risk.md`](standard-smart-contract-and-oracle-risk.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard sets the crypto-domain governance requirements for deploying, upgrading, relying on, and integrating smart contracts and the oracles and external data feeds they depend on. It is a requirements overlay under the [Crypto-Asset Governance Framework](framework-crypto-asset-governance.md). It governs the domain-specific decisions that surround a smart contract, the decision to deploy or rely on one, how its upgrade and change are authorized, and how its oracle and network dependencies are managed, and it does not restate code-level secure development, which the [Secure Development and Engineering Policy](../dev-security/policy-secure-development-and-engineering.md) and its companion developer-security documents own, nor the threat-modelling method, which the [Threat Modelling Standard](../security/standard-threat-modelling.md) owns.

## 2. Applicability

This standard applies to an organization that deploys smart contracts, relies on or integrates a third-party or external on-chain contract, or depends on an oracle or external data feed for an on-chain process. Not every platform runs smart contracts, and the standard applies to the extent an organization's crypto-asset activity uses them.

## 3. Requirements

### 3.1 Pre-deployment classification and approval

A smart contract is not deployed to, or relied upon on, a production ledger before the crypto-assets it governs are classified and the activity is approved through the framework's Governance requirements 1 and 2. This standard adds the deployment-specific decision record described below; it does not create a parallel approval gate.

### 3.2 Immutability-aware deployment discipline

The deployment decision explicitly accounts for the append-only nature of a distributed ledger that NIST IR 8202 describes: once committed, a contract's code and the transactions it has executed generally cannot be changed, so a defect or an unintended behaviour is not silently correctable in place. The decision records the intended permanence, the pre-deployment assurance relied upon, and the change mechanism (if any) the contract exposes.

### 3.3 Upgrade and change governance

Any upgrade, migration, proxy-pattern change, parameter change, or pause or termination of a deployed contract has a named change authority, an approval, and a record, and is treated as an organizational control the domain exercises over the contracts it deploys. A contract that exposes an upgrade or administrative mechanism records who holds that authority and how its use is controlled; a contract that is genuinely immutable records that it has no such mechanism.

### 3.4 Oracle and external-data-feed dependency

A contract that consumes off-chain data records each oracle or data feed it depends on, the trust and failure model of each, the single-point-of-failure exposure, and the effect on the contract of stale, manipulated, or unavailable data. A dependency on a third-party oracle or data-feed provider is vetted as a provider reliance: through the [Crypto-Asset Service Provider Vetting Standard](standard-crypto-asset-service-provider-vetting.md) where that provider is itself a crypto-asset service provider, and otherwise through the organization's general [Third-Party and Supply Chain Risk Standard](../risk/standard-third-party-and-supply-chain-risk.md).

### 3.5 Execution-cost and denial-of-service exposure

A contract deployed on a fee-metered platform accounts for the execution cost its callers pay, the execution-time limit the platform enforces on a call, and the resource-exhaustion denial-of-service surface where a contract can be made to consume that limit, and for their effect on the availability of the functions the organization relies on (NIST IR 8202).

### 3.6 Reliance on third-party or external on-chain contracts

Where the organization integrates or depends on a contract it did not deploy, the dependency is recorded and the external contract's provenance, upgrade authority, and failure impact are assessed. A provider-operated external contract is vetted as a provider reliance, through the provider-vetting standard where the operator is a crypto-asset service provider and otherwise through the general [Third-Party and Supply Chain Risk Standard](../risk/standard-third-party-and-supply-chain-risk.md); the code-level assurance of a relied-upon contract is obtained where available and its absence is recorded as a residual risk.

### 3.7 Fork, chain-split, and re-organization impact

A fork, chain split, or deep re-organization is a governance event that can change the rules under which a deployed or relied-upon contract runs, or duplicate its state across chains. The organization records, per contract, its position on how a fork or split affects the contract's behaviour, the assets it governs, and the client rights attached to them, drawing on the platform fork-governance characteristics that the [Crypto-Asset Domain Inventory Register](register-crypto-asset-inventory.md) records for each platform; NIST IR 8202 describes soft and hard forks and the parallel chains they can produce.

### 3.8 Code-level assurance is inherited, not restated

Secure design, secure coding, peer and independent code review, testing, and software-composition analysis for smart-contract source are governed by the developer-security domain and are applied to smart-contract code as to any other software the organization builds. This standard requires that the applicable developer-security controls have been applied and their evidence obtained before deployment; it does not define smart-contract secure-coding rules, which are deferred to a companion code-level standard pending held authoritative sources.

### 3.9 Deployment and upgrade decision record and inventory handoff

Each deployment or upgrade produces a decision record stating the contract, its platform, its purpose, the classification and approval it rests on, the assurance evidence relied upon, the upgrade authority and change mechanism, the oracle and external-contract dependencies, the fork-impact position, and the approving roles. The contract and its accountable upgrade owner are recorded in the [Crypto-Asset Domain Inventory Register](register-crypto-asset-inventory.md) per the framework's inventory obligation.

## 4. Evidence requirements

Evidence for this standard comprises the deployment and upgrade decision records; the oracle and external-data-feed dependency map with each dependency's trust and failure model; the code-level assurance evidence produced under the developer-security controls; the fork and network-event position for each deployed or relied-upon contract; and the corresponding entries in the domain inventory register. Evidence is retained through the corpus records-retention controls.

## 5. Limitations

This is original library content and reproduces no external control text; framework-grounded requirements and the technology characteristics drawn from NIST IR 8202 are named at the point of use, and an organization under another regime applies its own governing law. NIST IR 8202 is an informative 2018 technical report used only for distributed-ledger and smart-contract technology characteristics, not as a normative control. The standard is governance-scoped: it owns the domain governance of deploying, upgrading, relying on, and integrating smart contracts and their oracle dependencies, and it does not restate code-level secure development (owned by the developer-security domain) or the threat-modelling method (owned by the Threat Modelling Standard). A companion code-level smart-contract security standard, covering re-entrancy, access-control, arithmetic, oracle-manipulation, and maximal-extractable-value controls, is deferred pending acquisition of the held authoritative sources it would require, and is out of scope here rather than addressed with unsourced material.

**End of Document**
