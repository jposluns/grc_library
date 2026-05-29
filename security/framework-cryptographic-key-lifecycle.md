# Cryptographic Key Lifecycle Management Framework

**Document Title:** Cryptographic Key Lifecycle Management Framework\
**Document Type:** Framework\
**Version:** 1.0.1\
**Date:** 2026-05-28\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`security/procedure-cryptographic-key-operations.md`](procedure-cryptographic-key-operations.md), [`security/roadmap-post-quantum-cryptography.md`](roadmap-post-quantum-cryptography.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md), [`supply-chain/procedure-supplier-audit.md`](../supply-chain/procedure-supplier-audit.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material cryptographic standard or regulatory change\
**Repository Path:** [`security/framework-cryptographic-key-lifecycle.md`](framework-cryptographic-key-lifecycle.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## Purpose

This framework establishes the strategic governance, lifecycle controls, and operational standards for managing cryptographic keys across the organisation's IT, OT, cloud, and BASC-certified trade environments. It defines a unified structure for key generation, distribution, storage, rotation, revocation, and destruction, aligned with NIST SP 800-57, ISO/IEC 27002:2022 §8.24 to §8.28, BASC v6, and the WCO SAFE Framework.

---

## Scope

Applies to all enterprise systems, databases, applications, network devices, and BASC-certified logistics systems utilizing cryptography. Covers symmetric keys (AES-256), asymmetric key pairs (RSA, ECC, PQC hybrid), API tokens, SSH keys, digital certificates, and HSM-managed keys.

---

## 1. Key lifecycle phases

| Phase | Objective | Core Activities |
| --- | --- | --- |
| **Generation** | Securely create cryptographic keys using approved algorithms and entropy sources. | HSM-based key creation; PQC hybrid generation (Kyber + ECC). |
| **Registration** | Record metadata in the Key Lifecycle Register (KLR) for audit. | Assign unique ID, owner, usage scope, and validity period. |
| **Distribution** | Deliver keys securely to authorized endpoints or systems. | Use PKI or encrypted APIs (TLS 1.3+); enforce MFA and RBAC. |
| **Activation** | Enable keys for cryptographic operations. | Integration with encryption libraries and system credentials. |
| **Rotation** | Periodically replace active keys to reduce risk of compromise. | Rotate symmetric keys every 90 days; asymmetric every 12 months. |
| **Revocation** | Immediately invalidate compromised or expired keys. | Update CRL or OCSP; remove from all dependent systems. |
| **Destruction** | Securely destroy obsolete or retired keys. | Perform cryptographic erasure; document certificate of destruction. |

---

## 2. Key management controls

**Approved algorithms:**

- Symmetric: AES-256 and ChaCha20-Poly1305
- Asymmetric: RSA-4096, ECC P-384, Kyber/Dilithium hybrids (PQC)
- Hashing: SHA-512 or BLAKE2b

**Control requirements:**

- Key separation is mandatory: encryption, signing, and authentication keys must be segregated.
- Dual control is required for any key activation or export operation.
- All root and master keys are stored in FIPS 140-3 compliant Hardware Security Modules (HSMs).
- PQC hybrid key issuance in PKI environments follows the Post-Quantum Cryptography Roadmap.

---

## 3. Key lifecycle register (KLR)

All cryptographic keys must be registered in the Key Lifecycle Register with the following mandatory fields:

| Field | Requirement |
| --- | --- |
| Key ID | Unique identifier assigned at generation |
| Key Type | Symmetric, asymmetric, certificate, token |
| Algorithm | AES-256, RSA-4096, ECC P-384, Kyber, etc. |
| Owner | Role title of responsible party |
| Usage Scope | System, application, or service authorized to use the key |
| Validity Period | Issue date and expiry date |
| Rotation Schedule | Next scheduled rotation date |
| Status | Active, suspended, revoked, or destroyed |
| Destruction Record | Cryptographic erasure method and date |

---

## 4. Governance and accountability

| Role | Responsibility |
| --- | --- |
| **CISO** | Approves cryptographic standards and key management policy; reviews KLR quarterly. |
| **Security Architecture** | Designs key management architecture; selects approved algorithms and HSM platforms. |
| **IT Operations** | Executes key rotation, distribution, and revocation procedures. |
| **Internal Audit** | Verifies KLR completeness and control adherence annually. |

Sector-conditional roles (for example, a BASC Regional Compliance Officer who maintains trade-system key registrations and validates keys during BASC audits) apply where the organisation participates in a covered sector programme; see [`compliance/`](../compliance/).

---

## 5. Sector-programme cryptographic integration

Where the organisation participates in a sector programme that imposes additional cryptographic requirements (for example, BASC and WCO SAFE for trade and customs systems requiring AES-256 with PQC hybrid encryption by 2027), the keys used for sector-programme communications must:

- Be uniquely identifiable in the Key Lifecycle Register.
- Have documented ownership by the sector-conditional role defined by the relevant sector annex (for example, a BASC Regional Compliance Officer for the BASC programme).
- Be rotated at the cadence stated by the annex (default: annually unless the annex specifies a shorter interval).
- Be validated during sector-programme audits.
- Have audit evidence retained for the period stated by the annex (default: 7 years).

See [`compliance/`](../compliance/) for the sector annex applicable to the organisation's covered programmes.

---

## 6. Post-quantum cryptography transition

In alignment with the Post-Quantum Cryptography Roadmap, the organisation shall:

1. Inventory all cryptographic dependencies by 2025 (complete).
2. Deploy PQC hybrid algorithms in new systems from 2026.
3. Migrate production PKI to post-quantum algorithms by 2027.
4. Complete full PQC transition across all critical systems by 2028.

Kyber (key encapsulation) and Dilithium (digital signatures) are the designated primary PQC algorithms per NIST FIPS 203 and FIPS 204.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27002:2022 | §8.24 to §8.28: Cryptographic Controls | Key management lifecycle governance |
| NIST SP 800-57 Parts 1 to 3 | Key Management Guidelines | Key generation, rotation, and destruction |
| NIST SP 800-208 | PQC Transition Planning | Post-quantum algorithm migration |
| NIST FIPS 203 / 204 | Kyber and Dilithium Standards | PQC algorithm selection |
| COBIT 2019 | DSS05: Manage Security Services | Security service controls |
| CSA CCM v4.1 | CEK-01: Encryption and Key Management | Cloud key management controls |
| CSA CCM v4.1 | DSP-02: Data Security / Protection | Data encryption requirements |
| BASC International Standard v6 | Trade and Customs Encryption Integrity | Trade system key management |
| WCO SAFE Framework (2021) | AEO cryptographic integrity | Customs communication security |

---

**End of Document**
