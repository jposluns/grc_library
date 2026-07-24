# Post-Quantum Cryptography Readiness Roadmap

**Document Title:** Post-Quantum Cryptography Readiness Roadmap\
**Document Type:** Roadmap\
**Version:** 1.1.4\
**Date:** 2026-07-24\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`security/framework-cryptographic-key-lifecycle.md`](framework-cryptographic-key-lifecycle.md), [`security/procedure-cryptographic-key-operations.md`](procedure-cryptographic-key-operations.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon significant NIST, ETSI, or national standards developments\
**Repository Path:** [`security/roadmap-post-quantum-cryptography.md`](roadmap-post-quantum-cryptography.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This roadmap defines the organization's strategy and phased plan for transitioning cryptographic systems to post-quantum cryptography (PQC) algorithms. It responds to the threat posed by cryptographically relevant quantum computers (CRQCs) to current public-key cryptographic algorithms, and establishes a time-bound migration plan aligned with NIST PQC standards, NIST SP 800-208, and NSA CNSA 2.0 Suite guidance.

---

## The quantum threat

Current widely-deployed public-key algorithms, RSA, ECC (ECDSA, ECDH), and DSA, are vulnerable to Shor's algorithm on a cryptographically relevant quantum computer. While CRQCs capable of breaking current key sizes do not yet exist, the threat model requires action now because:

1. **Harvest-now, decrypt-later attacks:** Adversaries may be harvesting encrypted communications today for decryption once CRQCs become available.
2. **Long-lifecycle data:** Data with confidentiality requirements extending to 2030 and beyond must be protected against future quantum decryption.
3. **Migration complexity:** Replacing cryptographic infrastructure requires significant time; migration must begin well before CRQCs are expected.

Symmetric encryption (AES-256) and hash functions (SHA-256 with adequate output length, SHA-384, SHA-512) are considered quantum-resistant at current key sizes and do not require immediate migration.

---

## Target PQC algorithms

The organization will adopt NIST-standardized post-quantum algorithms:

| Algorithm | NIST Standard | Use Case |
| --- | --- | --- |
| **ML-KEM (formerly CRYSTALS-Kyber)** | FIPS 203 (August 2024) | Key encapsulation / key exchange |
| **ML-DSA (formerly CRYSTALS-Dilithium)** | FIPS 204 (August 2024) | Digital signatures |
| **SLH-DSA (formerly SPHINCS+)** | FIPS 205 (August 2024) | Digital signatures (stateless hash-based; conservative hash-only alternative to ML-DSA) |

Hybrid schemes combining classical and PQC algorithms (e.g., X25519 + ML-KEM) are required during the transition period to protect against both classical and quantum threats simultaneously. The "ML-KEM" / "ML-DSA" names are the official NIST FIPS 203 / FIPS 204 (August 2024) designations; the older "Kyber" / "Dilithium" names from the NIST PQC competition remain in common informal use.

### Parameter sets and NIST security categories

Each standardized algorithm defines parameter sets keyed to a NIST post-quantum security category. Categories 1, 3, and 5 correspond to the difficulty of an exhaustive key search against AES-128, AES-192, and AES-256 respectively; a higher category is more conservative, at a cost in key size, signature size, and performance. The organization adopts **category 3 as the interoperability baseline** and selects category 5 for long-lived (post-2030 confidentiality) or high-assurance contexts.

| Algorithm | Parameter sets by security category | Baseline selection |
| --- | --- | --- |
| ML-KEM (FIPS 203) | ML-KEM-512 (category 1), ML-KEM-768 (category 3), ML-KEM-1024 (category 5) | ML-KEM-768 |
| ML-DSA (FIPS 204) | ML-DSA-44 (category 2; reduced to category 1 only when an approved RBG below 192 bits of security is used), ML-DSA-65 (category 3), ML-DSA-87 (category 5) | ML-DSA-65 |
| SLH-DSA (FIPS 205) | SLH-DSA-SHA2 and SLH-DSA-SHAKE at the 128-bit (category 1), 192-bit (category 3), and 256-bit (category 5) strengths, each in a small-signature (s) and fast-signing (f) variant | category 3, variant per signing profile |

Parameter-set names and category assignments are drawn from FIPS 203, FIPS 204, and FIPS 205 (SLH-DSA parameter sets and their categories are specified in FIPS 205 Section 11); the tables above are illustrative selection guidance for adopters, not a reproduction of the standards' normative bodies.

**Choosing between ML-DSA and SLH-DSA.** ML-DSA is the default signature algorithm for general use: it produces smaller signatures and signs and verifies faster. SLH-DSA is preferred where a conservative, hash-only security assumption is required: its security rests solely on the underlying hash function, with no lattice assumption, which suits long-lived or high-assurance signatures (for example firmware and root-of-trust signing) where the larger signature size and slower signing are acceptable. Within SLH-DSA, the small-signature (s) variant minimizes signature size at a cost in signing speed, and the fast-signing (f) variant makes the opposite trade.

---

## Migration scope

| Cryptographic Function | Current Algorithm | PQC Migration Target | Priority |
| --- | --- | --- | --- |
| TLS/HTTPS key exchange | ECDH (P-256/P-384) | ML-KEM hybrid | High |
| Code signing | RSA-4096 / ECDSA | ML-DSA hybrid | High |
| PKI / certificate signatures | RSA-4096 / ECDSA | ML-DSA hybrid | High |
| SSH authentication | RSA-4096 / Ed25519 | ML-DSA hybrid | Medium |
| Document and data signing | RSA-4096 | ML-DSA | Medium |
| Encrypted backup keys | RSA-4096 | ML-KEM | High |
| BASC/customs encrypted communications | AES-256 + RSA | AES-256 + ML-KEM hybrid | High |
| API tokens (long-lived) | HMAC-SHA256 | HMAC-SHA384 (retain) | Low |

---

## Phased migration roadmap

### Phase 1: Discovery and inventory (2025: complete)

- Conduct cryptographic asset discovery across all environments.
- Identify all systems, applications, and protocols using public-key cryptography.
- Classify by data sensitivity and operational criticality.
- Identify dependencies on hardware cryptographic modules.
- Assess vendor and platform PQC readiness (TLS libraries, HSM firmware, certificate authorities).

**Deliverable:** Cryptographic asset inventory registered in the Key Lifecycle Register.

### Phase 2: Standards and architecture (2026)

- Adopt NIST FIPS 203, 204, and 205 as the organizational PQC standard.
- Define hybrid algorithm transition schemes for each cryptographic function.
- Update the Cryptographic Key Lifecycle Management Framework with PQC requirements.
- Evaluate and procure PQC-capable HSMs, TLS libraries, and certificate authority services.
- Update the cloud-based PKI service to support PQC hybrid certificates.

**Deliverable:** Updated cryptographic standards; PQC-capable infrastructure procured.

### Phase 3: Pilot and new systems (2026 to 2027)

- Deploy PQC hybrid TLS in new system builds and infrastructure programme environments.
- Issue PQC hybrid certificates for all new PKI enrolments.
- Require PQC-compliant cryptography for all new systems entering service.
- Test PQC algorithms in production-equivalent environments.

**Deliverable:** All new systems deployed with PQC hybrid cryptography.

### Phase 4: Production migration: high priority systems (2027)

- Migrate PKI root and intermediate CAs to ML-DSA hybrid.
- Migrate Tier 1 (Mission Critical) systems' TLS and key management to PQC hybrid.
- Migrate BASC/customs communication encryption to AES-256 + ML-KEM hybrid.
- Migrate code signing infrastructure to ML-DSA.
- Rekey encrypted backups with ML-KEM-protected keys.

**Deliverable:** All Tier 1 systems and PKI migrated to PQC hybrid cryptography.

### Phase 5: Full production migration (2028)

- Complete PQC hybrid migration across all Tier 2 and Tier 3 systems.
- Migrate SSH authentication infrastructure to ML-DSA hybrid.
- Retire legacy RSA-2048 and ECC P-256 certificates and keys.
- Achieve full PQC hybrid coverage across all cryptographic functions.

**Deliverable:** Organization-wide PQC transition complete; legacy algorithm retirement.

### Phase 6: Pure PQC transition (2030 target, pending standards maturity)

- Remove classical algorithm components from hybrid schemes where standards and interoperability allow.
- Transition to pure PQC for newly issued certificates and keys.
- Maintain hybrid interoperability for external communications as long as required.

---

## Crypto-agility

The transition above is possible only if cryptographic primitives are treated as configuration, not as hardcoded implementation choices. The durable lesson of the PQC migration, beyond the specific algorithms, is that the next algorithm change (a parameter-set bump, a primitive found weak, the eventual pure-PQC cutover) must be a configuration rotation rather than a re-architecture. The organization therefore requires that:

- **Algorithm identifiers, parameter sets, and key sizes are externalized as configuration**, negotiated or versioned, never compiled in as the sole supported option.
- **A crypto-agility inventory records every point where an algorithm is pinned** (protocol negotiation defaults, certificate profiles, HSM firmware, and embedded or long-lived firmware images), maintained alongside the Phase 1 cryptographic asset inventory.
- **Systems support algorithm negotiation and graceful fallback** across the hybrid transition, so that a migrated peer and a not-yet-migrated peer still interoperate.
- **Rotation is exercised, not assumed**: the ability to change a cryptographic primitive without redeploying application code is validated in testing, as Phase 3 requires for PQC hybrid deployment.

Pinning points that cannot be rotated by configuration (typically long-lived firmware and hardware roots of trust) are the highest-priority migration targets, because they cannot be corrected later by a configuration change.

---

## Governance and accountability

The PQC Roadmap is reviewed annually by the CISO and Security Architecture team. Milestone progress is reported to the ERC annually. Material deviations from the roadmap require CISO approval and risk documentation.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| NIST SP 800-208 | Recommendation for Stateful Hash-Based Signature Schemes | PQC transition planning |
| NIST FIPS 203 | ML-KEM (formerly CRYSTALS-Kyber) | Key encapsulation standard |
| NIST FIPS 204 | ML-DSA (formerly CRYSTALS-Dilithium) | Digital signature standard |
| NIST FIPS 205 | SLH-DSA (SPHINCS+) | Stateless hash-based signatures |
| NSA CNSA 2.0 Suite | Commercial National Security Algorithm Suite 2.0 | High-assurance PQC guidance |
| ETSI TR 103 619 | Migration Strategies for Quantum-Safe Cryptography | Migration planning guidance |
| ISO/IEC 27001:2022 | Annex A.8.24 | Cryptographic controls |
| BASC International Standard v6 | Trade and customs encryption | Trade system cryptography requirements |

---

**End of Document**
