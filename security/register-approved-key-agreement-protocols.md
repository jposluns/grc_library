# Approved Key-Agreement Protocols Register

**Document Title:** Approved Key-Agreement Protocols Register\
**Document Type:** Register\
**Version:** 0.0.1\
**Date:** 2026-10-15\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Chief Information Security Officer\
**Related Documents:** [`security/procedure-cryptographic-key-operations.md`](procedure-cryptographic-key-operations.md), [`security/framework-cryptographic-key-lifecycle.md`](framework-cryptographic-key-lifecycle.md), [`security/policy-encryption-and-key-management.md`](policy-encryption-and-key-management.md), [`operations/register-asset-inventory.md`](../operations/register-asset-inventory.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon approval, withdrawal, or material change of a listed protocol\
**Repository Path:** [`security/register-approved-key-agreement-protocols.md`](register-approved-key-agreement-protocols.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register lists the protocols that may be approved protocols, within which the ephemeral key-agreement key exemptions in the [Cryptographic Key Operations Procedure](procedure-cryptographic-key-operations.md) and the [Cryptographic Key Lifecycle Management Framework](framework-cryptographic-key-lifecycle.md) apply. A protocol is an approved protocol only when it is listed here and the adopting organization's Security Architecture has recorded the date and reference of its approval in the protocol's row; until then the exemptions do not apply to it. For each protocol, the register also records the one-time CISO approval that the procedure, section 4.3, requires before the protocol is used for ephemeral key-agreement keys on a high-sensitivity system. The register records these approvals; it does not restate the rules for ephemeral key-agreement keys, which the procedure holds.

---

## Scope

The register covers protocols in which peers agree keys through an ephemeral key agreement. Listing a protocol does not approve any algorithm, key length, or cipher suite; those remain governed by the [Encryption and Key Management Policy](policy-encryption-and-key-management.md) and the framework, section 2.

---

## Register fields

| Field | Description |
| --- | --- |
| **Protocol** | Protocol name and version |
| **Ephemeral key agreement** | The key-agreement mechanism within the protocol to which the exemptions apply |
| **Security Architecture approval** | Date and reference of the Security Architecture approval |
| **CISO approval for high-sensitivity systems** | Date and reference of the one-time CISO approval under the procedure, section 4.3, or "Not approved" |
| **Last reviewed** | Date of the most recent review of the entry |

---

## Listed protocols

| Protocol | Ephemeral key agreement | Security Architecture approval | CISO approval for high-sensitivity systems | Last reviewed |
| --- | --- | --- | --- | --- |
| TLS 1.3 | ECDHE or DHE key exchange in the handshake | Seed entry; no approval recorded yet | Not approved | To be recorded |
| SSH 2.0 | ECDH or DH key exchange in the transport layer | Seed entry; no approval recorded yet | Not approved | To be recorded |
| IPsec (IKEv2 or greater) | ECDH or DH key exchange in Internet Key Exchange (IKE) | Seed entry; no approval recorded yet | Not approved | To be recorded |

---

## Governance and maintenance

Security Architecture maintains the entries in this register. Apart from the seed entries, it adds a protocol only after approving it and removes a protocol when it withdraws the approval; a removed protocol is no longer an approved protocol. The CISO's one-time approval for high-sensitivity systems is recorded in the protocol's row. The procedure, section 4.3, defines a high-sensitivity system. The seed entries are the library's baseline: an adopting organization's Security Architecture confirms or removes each one and records its approval. A seed entry becomes an approved protocol only when the date and reference of that approval are recorded in its row; until then the ephemeral key-agreement key exemptions do not apply to it. Internal Audit may use this register as evidence when it audits key operation logs.

---

## Limitations

This is organization-neutral library content and reproduces no external control text. The register records approvals; the Cryptographic Key Operations Procedure holds the rules that the approvals enable, and the policy and framework hold the algorithm requirements.

---

**End of Document**
