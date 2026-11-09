# When a crypto-asset custody key is compromised and client assets are moved on-chain

**Document Title:** When a crypto-asset custody key is compromised and client assets are moved on-chain\
**Document Type:** Executive Narrative\
**Version:** 0.0.2\
**Date:** 2026-09-13\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`crypto/standard-digital-asset-custody.md`](../../crypto/standard-digital-asset-custody.md), [`crypto/register-crypto-asset-inventory.md`](../../crypto/register-crypto-asset-inventory.md), [`crypto/standard-crypto-asset-service-provider-vetting.md`](../../crypto/standard-crypto-asset-service-provider-vetting.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/scenarios/scenario-crypto-custody-key-compromise.md`](scenario-crypto-custody-key-compromise.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Scenario\
**Narrative Status:** Non-normative\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`crypto/standard-digital-asset-custody.md`](../../crypto/standard-digital-asset-custody.md), [`crypto/register-crypto-asset-inventory.md`](../../crypto/register-crypto-asset-inventory.md), [`crypto/standard-crypto-asset-service-provider-vetting.md`](../../crypto/standard-crypto-asset-service-provider-vetting.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-026\
**Last Reviewed:** 2026-09-12

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Scenario premise

An organization custodies crypto-assets on behalf of clients. A private key controlling a warm-tier wallet is compromised, and an attacker submits an on-chain transfer that, once confirmed, is irreversible. This scenario walks the event through the controls the crypto corpus sets, to show a governing body where each control engages and what evidence a well-run response leaves behind. It reproduces no control values; it routes to the standards that hold them.

## How the event unfolds

The compromised key controls a warm-tier wallet used for routine client withdrawals. The attacker attempts to drain the wallet and move the assets to an address outside the organization's control. Because on-chain settlement is final, the organization cannot reverse the transfer; its position depends entirely on the controls that were in place before the event and the discipline of its response after it.

## Where the corpus controls engage

- **Loss containment.** Wallet tiering with a bounded value at risk per tier means the compromise reaches the warm-tier balance rather than the whole book; the [custody standard](../../crypto/standard-digital-asset-custody.md) wallet-architecture section sets that tiering, and its key-custody section sets split-knowledge and dual-control custody for the tiers that require it (its wallet-architecture and key-custody sections).
- **Incident response.** The [custody standard](../../crypto/standard-digital-asset-custody.md) incident section routes a custody compromise through security incident response, key-compromise response, and recovery (its incident section).
- **Detection and scope.** The register of positions and the reconciliation of the [crypto-asset inventory](../../crypto/register-crypto-asset-inventory.md) against on-chain balances are where the discrepancy is detected and its scope established (the custody register-of-positions section; the inventory reconciliation).
- **Client liability.** Where the loss is attributable to the custodian, the [custody standard](../../crypto/standard-digital-asset-custody.md) loss-liability section sets the client's position (its loss-liability section), routing the measure to its source rather than restating it here.
- **Third-party custody.** Where a sub-custodian holds the affected wallet, the [service-provider vetting standard](../../crypto/standard-crypto-asset-service-provider-vetting.md) authorization-and-vetting gate governs the reliance (its legal-identity-and-authorization gate).
- **Records.** The [custody standard](../../crypto/standard-digital-asset-custody.md) records section is where each key stage of the affected service can be reconstructed for the competent authority (its records section).

## What good looks like

The exposure was bounded to the warm-tier balance rather than the whole book. The discrepancy was found by the register reconciliation, not by a client. The event went through the incident-response path rather than an improvised one. Where the loss is attributable to the custodian, the client's position follows a defined rule. And the key stages are reconstructable from the records. Each is a control the organization can point to and evidence, not a matter of luck.

## Evidence to request

- The wallet-tier configuration and the maximum-value-at-risk bound for the affected tier.
- The key-custody split-knowledge and dual-control records for the compromised wallet.
- The incident record showing the classification, the escalation, and the key-compromise response steps and their timeline.
- The register-of-positions and inventory-reconciliation records that detected and scoped the loss.
- The client-liability determination and, where a sub-custodian was involved, its authorization and vetting record.

## Limitations

This page is a non-normative executive narrative that creates no compliance by itself; the linked corpus documents govern, and where this page and a corpus document differ, the corpus document prevails. It routes to the corpus rather than reproducing its values: the wallet-tier value bounds, the client-liability measure, the key-management assurance level, and the incident timelines live in the linked standards and the organization's own configuration, and are not restated here. The scenario is illustrative; a real event's facts determine which controls engage and how.

**End of Document**
