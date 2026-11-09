# Cryptographic Key Lifecycle Management Framework

**Document Title:** Cryptographic Key Lifecycle Management Framework\
**Document Type:** Framework\
**Version:** 1.10.0\
**Date:** 2026-10-15\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`security/procedure-cryptographic-key-operations.md`](procedure-cryptographic-key-operations.md), [`security/roadmap-post-quantum-cryptography.md`](roadmap-post-quantum-cryptography.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md), [`supply-chain/procedure-supplier-audit.md`](../supply-chain/procedure-supplier-audit.md), [`security/register-approved-key-agreement-protocols.md`](register-approved-key-agreement-protocols.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material cryptographic standard or regulatory change\
**Repository Path:** [`security/framework-cryptographic-key-lifecycle.md`](framework-cryptographic-key-lifecycle.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This framework establishes the strategic governance, lifecycle controls, and operational standards for managing cryptographic keys across the organization's IT, OT, cloud, and BASC-certified trade environments. It defines a unified structure for key generation, distribution, storage, rotation, revocation, and destruction, aligned with NIST SP 800-57 and ISO/IEC 27002:2022 §8.24, and applicable to BASC-certified and WCO SAFE trade environments (which prescribe no cryptographic standard of their own).

---

## Scope

Applies to all enterprise systems, databases, applications, network devices, and BASC-certified logistics systems utilizing cryptography. Covers symmetric keys (AES-256), asymmetric key pairs (RSA, ECC, PQC hybrid), API tokens, SSH keys, digital certificates, and HSM-managed keys.

---

## 1. Key lifecycle phases

| Phase | Objective | Core Activities |
| --- | --- | --- |
| **Generation** | Securely create cryptographic keys using approved algorithms and entropy sources. | HSM-based key creation; PQC hybrid generation (ML-KEM + ECC). An approved protocol is a protocol approved by Security Architecture, which also approves key generation requests (Cryptographic Key Operations Procedure, section 1.2), and listed in the [Approved Key-Agreement Protocols Register](register-approved-key-agreement-protocols.md). A private or public ephemeral key-agreement key generated within an approved protocol is outside the ITSM request, Security Architecture approval, dual control at generation and generation logging (that procedure's steps 1.1, 1.2, 1.4 and 1.6; exemption stated in 1.1); the requirement in that procedure's section 1.3 to use a FIPS 140-3 validated hardware security module or an approved software cryptographic library still applies to it. A symmetric session key derived within an approved protocol from an ephemeral key agreement is treated in this framework as a private ephemeral key-agreement key (Cryptographic Key Operations Procedure, section 1.1). |
| **Registration** | Record metadata in the Key Lifecycle Register (KLR) for audit. | Assign unique ID, owner, usage scope, and validity period. |
| **Distribution** | Deliver keys securely to authorized endpoints or systems. | Use PKI or encrypted APIs (TLS 1.3+); enforce MFA and RBAC. The export of a public ephemeral key-agreement key to the peer within an approved protocol is outside this row (Cryptographic Key Operations Procedure, section 3.1). |
| **Activation** | Enable keys for cryptographic operations. | Integration with encryption libraries and system credentials. |
| **Rotation** | Periodically replace active keys to reduce risk of compromise. | Rotate symmetric keys every 90 days; asymmetric every 12 months. These are key-type baselines; where a key also carries a data-classification cadence (see the Encryption and Key Management Policy), apply the shorter applicable interval. NIST SP 800-57 Part 1 (section 5.3.6) sets a key's cryptoperiod from its type, usage environment, and data characteristics together, as rough guidance rather than a fixed one-to-one mapping. |
| **Revocation** | Immediately invalidate compromised keys and keys revoked for other reasons. | Update CRL or OCSP for revocation only, including a certificate superseded at rotation before it expires, which is revoked on the CRL; an expired certificate needs no CRL action. Apart from that CRL entry, a key retired at rotation or at the end of its validity is not revoked, and its status is set as in the Status field in section 3. Remove a revoked or retired key from use for applying new cryptographic protection in all dependent systems. Controlled access for decryption or verification may be retained where the key's state and recipient-usage period permit, until dependent data is re-encrypted or destroyed, as set out in the Cryptographic Key Operations Procedure, section 6.2, step 4 (NIST SP 800-57 Part 1 Rev. 5, sections 5.3.6, 7.4 and 7.5); for a compromised symmetric key or the public key that corresponds to a compromised private key, this processing is done only under highly controlled conditions where the users of the information are fully aware of the possible consequences (section 7.5), and the CISO approves each such use and its conditions, and the approval, the conditions, the users told of the consequences and the period of use are recorded in the KLR. As an organizational rule, a compromised private key is not used for any processing; section 7.5 names only a compromised symmetric key or the public key that corresponds to a compromised private key as usable for processing. A public key or public-key certificate is also removed from active use and distribution and retained or archived as set out in the Destruction row. |
| **Destruction** | Securely destroy obsolete or retired secret and private keys. | Destroy a data-encryption key only after the data it protects is re-encrypted or destroyed, and retain a key-wrapping key while any key it protects is still needed (Encryption and Key Management Policy, section 5.5). Before destruction, confirm whether a legal hold or investigation covers data the key protects, directly or through a key it wraps. The check follows rule 2's two-part confirmation, as set out in the [Cryptographic Key Operations Procedure](procedure-cryptographic-key-operations.md), section 7.1. Recorded hold status alone does not complete the check. Legal Counsel or the Incident Commander or, for security P3 and P4 where no Incident Commander is assigned, the SOC lead confirms whether an investigation under the [Security Incident Response Procedure](procedure-security-incident-response.md) treats that data or the key as evidence. Only Legal Counsel confirms whether an investigation by an external authority does so, and whether a hold is required but not yet recorded. Retain the key if a hold or investigation applies, or either part of the check is incomplete. The key stays retained until Legal Counsel, in writing, releases the hold or narrows it so that it no longer covers that data. For an investigation without a legal hold, it stays retained until Legal Counsel confirms in writing that the investigation no longer treats that data or the key as evidence. Destroy every copy of a secret or private key (NIST SP 800-57 Part 1 Rev. 5, section 8.3.4), and perform zeroization where the storage supports it (the key sanitization technique NIST SP 800-88 Rev. 2, section 3.2.3, recommends for the target cryptographic keys of a cryptographic erase), otherwise use another destruction method, in either case removing all traces of the key so that it cannot be recovered by physical or electronic means (as NIST SP 800-57 Part 1 Rev. 5, section 8.3.4, requires for secret and private keys); document certificate of destruction. A retired or expired public key or public-key certificate is not subject to the all-traces destruction requirement (NIST SP 800-57 Part 1 Rev. 5, section 8.3.4). As an organizational rule, remove it from active use and distribution so that it is not used to apply new cryptographic protection. Retain or archive it for as long as needed to verify information signed with the corresponding private key (section B.3.1.2); otherwise it may be retained or destroyed (section 8.3.4), subject to the legal hold and investigation check above. An asymmetric public authorization key is instead destroyed when the corresponding private key is destroyed (NIST SP 800-57 Part 1 Rev. 5, section 7.2, State Transition 5). For a public key, data the key protects includes information signed with the corresponding private key. A private ephemeral key-agreement key is destroyed within the protocol immediately after use, and the corresponding public ephemeral key-agreement key when the private key is destroyed (State Transition 5); neither has a KLR entry, and both are outside the check and the certificate of destruction in this row (Cryptographic Key Operations Procedure, section 7.1). The protocol's or system's own logging is the record of their destruction, which State Transition 5 requires to be recorded (see SP 800-152). |

---

## 2. Key management controls

**Approved algorithms:**

- Symmetric: AES-256 and ChaCha20-Poly1305
- Asymmetric: RSA-4096, ECC P-384, ML-KEM/ML-DSA hybrids (PQC), and SLH-DSA (FIPS 205) where a conservative hash-only signature assumption is required
- Hashing: SHA-512 or BLAKE2b-512

**Control requirements:**

- Key separation is mandatory: encryption, signing, and authentication keys must be segregated.
- Dual control is required for any key activation or export operation, except the activation of a private or public ephemeral key-agreement key by its use within an approved protocol and the export of the public ephemeral key-agreement key to the peer within that protocol.
- All root and master keys are stored in FIPS 140-3 compliant Hardware Security Modules (HSMs).
- PQC hybrid key issuance in PKI environments follows the Post-Quantum Cryptography Roadmap.

---

## 3. Key lifecycle register (KLR)

All cryptographic keys must be registered in the Key Lifecycle Register with the following mandatory fields, except a private or public ephemeral key-agreement key, which is destroyed within the protocol as set out in the Destruction row in section 1, has no KLR entry, and is outside every requirement in this framework to record in or read from the KLR:

| Field | Requirement |
| --- | --- |
| Key ID | Unique identifier assigned at generation |
| Key Type | Symmetric, asymmetric, certificate, token |
| Algorithm | AES-256, RSA-4096, ECC P-384, ML-KEM, etc. |
| Owner | Role title of responsible party |
| Usage Scope | System, application, or service authorized to use the key |
| Validity Period | Issue date and expiry date |
| Rotation Schedule | Next scheduled rotation date |
| Status | Pre-activation, active, suspended, deactivated, compromised, revoked, or destroyed; pre-activation applies from generation until the key is authorized for use (NIST SP 800-57 Part 1 Rev. 5, section 7.1); compromised applies to a key whose integrity, or confidentiality where the key requires confidentiality protection, is suspect or that has been provided to or determined by an unauthorized entity, and to both keys of a compromised key pair (sections 7.2 and 7.5); revoked applies to a key revoked for reasons other than compromise; a key retired at rotation or at the end of its validity, including a key whose certificate is superseded at rotation and revoked on the CRL, is deactivated (NIST SP 800-57 Part 1 Rev. 5, section 7.2, State Transition 8), except that the following keys are destroyed (State Transition 5), as set out in the Cryptographic Key Operations Procedure, section 6.1: a private signature key or private authentication key at the end of its originator-usage period, a symmetric RBG key when it is replaced by a new key or when the RBG will no longer be used, a symmetric master or key-derivation key or a symmetric authorization key at the end of its originator-usage period, an asymmetric private authorization key at the end of its cryptoperiod, and an asymmetric public authorization key when the corresponding private key is destroyed; a key in this list that is not yet destroyed, unless its status is revoked or compromised, including one retained for a legal hold or investigation under that procedure's section 7.1, is deactivated until its status is set to destroyed under that procedure's section 7.2, step 6; a retired or expired public key or public-key certificate retained or archived under the Destruction row in section 1 is deactivated (NIST SP 800-57 Part 1 Rev. 5, section 7.4) unless its status is revoked or compromised |
| Key Copies | For a secret or private key, list each copy, its location and its holder; not applicable to public keys. Keep this list current as copies are made, distributed, escrowed or destroyed, using distribution events logged under the Cryptographic Key Operations Procedure, section 3.4, and escrow and backup records; these are also sources used in that procedure's section 7.2, step 1 |
| Destruction Record | Destruction method, date and operator for every destroyed key; for a public key or public-key certificate retained or archived instead of destroyed, record the retention or archive location and reason; for a secret or private key, record the method, date and operator for each copy, including the provider's or holder's documented destruction method where applicable; for a destroyed key, include a reference to the certificate of destruction |

---

## 4. Governance and accountability

| Role | Responsibility |
| --- | --- |
| **CISO** | Approves cryptographic standards and key management policy; approves once, in addition to Security Architecture, each approved protocol used for ephemeral key-agreement keys on high-sensitivity systems, in place of per-key approval of their activation (Cryptographic Key Operations Procedure, section 4.3); approves each use of a compromised key for processing under controlled conditions, and those conditions (NIST SP 800-57 Part 1 Rev. 5, section 7.5), with the approval, the conditions, the users told of the consequences and the period of use recorded in the KLR; reviews KLR quarterly. |
| **Security Architecture** | Designs key management architecture; selects approved algorithms and HSM platforms; approves the protocols within which the ephemeral key-agreement key exemptions in this framework apply, and maintains the Approved Key-Agreement Protocols Register. |
| **IT Operations** | Executes key rotation, distribution, and revocation procedures. |
| **Internal Audit** | Verifies KLR completeness and control adherence annually. |

Sector-conditional roles (for example, a BASC Regional Compliance Officer who maintains trade-system key registrations for BASC-certified operations) apply where the organization participates in a covered sector programme; see [`compliance/`](../compliance/).

---

## 5. Sector-programme cryptographic integration

Where the organization participates in a sector programme for trade and customs systems (for example, BASC or WCO SAFE AEO participation), the organization applies its own cryptographic baseline to those systems (AES-256, with a post-quantum hybrid-encryption migration on the roadmap; WCO SAFE prescribes no cryptographic algorithm or migration deadline, and any BASC-specific requirement is stated in the relevant sector annex), and the keys used for sector-programme communications must:

- Be uniquely identifiable in the Key Lifecycle Register.
- Have documented ownership by the sector-conditional role defined by the relevant sector annex (for example, a BASC Regional Compliance Officer for the BASC programme).
- Be rotated at the cadence stated by the annex (default: annually unless the annex specifies a shorter interval).
- Be validated during sector-programme audits.
- Have audit evidence retained for the period stated by the annex (default: 7 years).

See [`compliance/`](../compliance/) for the sector annex applicable to the organization's covered programmes.

---

## 6. Post-quantum cryptography transition

In alignment with the Post-Quantum Cryptography Roadmap, the organization must:

1. Inventory all cryptographic dependencies by 2025 (complete).
2. Deploy PQC hybrid algorithms in new systems from 2026.
3. Migrate production PKI to post-quantum algorithms by 2027.
4. Complete full PQC transition across all critical systems by 2028.

ML-KEM (key encapsulation; formerly CRYSTALS-Kyber) and ML-DSA (digital signatures; formerly CRYSTALS-Dilithium) are the designated primary PQC algorithms per NIST FIPS 203 (August 2024) and FIPS 204 (August 2024). The "ML-KEM" / "ML-DSA" names are the official NIST designations; the older "Kyber" / "Dilithium" names from the NIST PQC competition remain in common informal use.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27002:2022 | §8.24: Use of cryptography | Key management lifecycle governance |
| NIST SP 800-57 Part 1 Rev. 5 | Recommendation for Key Management, Part 1: General | Key generation, rotation, and destruction |
| NIST SP 800-57 Part 2 Rev. 1 | Recommendation for Key Management, Part 2: Best Practices for Key Management Organizations | Key management organization practices |
| NIST SP 800-57 Part 3 Rev. 1 | Recommendation for Key Management, Part 3: Application-Specific Key Management Guidance | Application-specific key management |
| NIST SP 800-208 | Recommendation for Stateful Hash-Based Signature Schemes | Stateful hash-based signature key management (LMS, HSS, XMSS, XMSS^MT) |
| NIST FIPS 203 / 204 | ML-KEM and ML-DSA Standards | PQC algorithm selection |
| NIST FIPS 197-upd1 | Advanced Encryption Standard (AES) (November 2001, updated May 2023) | AES-256 in the approved symmetric algorithms |
| NIST FIPS 186-5 | Digital Signature Standard (DSS) (February 2023) | RSA and ECDSA digital signatures in the approved asymmetric algorithms |
| NIST FIPS 180-4 | Secure Hash Standard (SHS) (August 2015) | SHA-512 in the approved hashing algorithms |
| NIST SP 800-131A Rev. 2 | Transitioning the Use of Cryptographic Algorithms and Key Lengths (March 2019) | Acceptability of NIST-approved algorithms and key lengths |
| NIST SP 800-90B | Recommendation for the Entropy Sources Used for Random Bit Generation (January 2018) | Entropy sources for the random bit generation used in key generation |
| NIST SP 800-130 | A Framework for Designing Cryptographic Key Management Systems (August 2013), 6.2.1 Metadata Elements | Key metadata recorded in the Key Lifecycle Register |
| COBIT 2019 | DSS05: Managed Security Services | Security service controls |
| CSA CCM v4.1 | CEK-01: Encryption and Key Management | Cloud key management controls |
| CSA CCM v4.1 | CEK-04: Encryption Algorithm | Approved encryption algorithm standards |
| CSA CCM v4.1 | CEK-10: Key Generation | Key generation controls (HSM, approved algorithms, entropy) |
| CSA CCM v4.1 | CEK-12: Key Rotation | Cryptoperiod-based key rotation |
| CSA CCM v4.1 | CEK-14: Key Destruction | Secure key destruction (zeroization) |
| WCO SAFE Framework (2025 edition) | Annex IV F: Information Exchange, Access and Confidentiality | Documented information-security policy and protection of entrusted information against unauthorized alteration (general information security, not a key-lifecycle mandate) |

---

**End of Document**
