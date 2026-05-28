# Post-Quantum Cryptography Readiness Plan

**Document Title:** Post-Quantum Cryptography Readiness Plan 
**Document Type:** Plan 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Chief Information Officer 
**Related Documents:** [`security/framework-cryptographic-key-lifecycle.md`](framework-cryptographic-key-lifecycle.md), [`security/procedure-cryptographic-key-operations.md`](procedure-cryptographic-key-operations.md), [`governance/policy-governance-and-risk-management.md`](../governance/policy-governance-and-risk-management.md) 
**Classification:** Public 
**Category:** Information Security 
**Review Frequency:** Annual and upon significant NIST, ETSI, or national standards developments 
**Repository Path:** [`security/roadmap-post-quantum-cryptography.md`](roadmap-post-quantum-cryptography.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

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
| **CRYSTALS-Kyber (ML-KEM)** | FIPS 203 (2024) | Key encapsulation / key exchange |
| **CRYSTALS-Dilithium (ML-DSA)** | FIPS 204 (2024) | Digital signatures |
| **SPHINCS+ (SLH-DSA)** | FIPS 205 (2024) | Digital signatures (stateless hash-based; backup algorithm) |

Hybrid schemes combining classical and PQC algorithms (e.g., X25519 + Kyber) are required during the transition period to protect against both classical and quantum threats simultaneously.

---

## Migration scope

| Cryptographic Function | Current Algorithm | PQC Migration Target | Priority |
| --- | --- | --- | --- |
| TLS/HTTPS key exchange | ECDH (P-256/P-384) | Kyber hybrid | High |
| Code signing | RSA-4096 / ECDSA | Dilithium hybrid | High |
| PKI / certificate signatures | RSA-4096 / ECDSA | Dilithium hybrid | High |
| SSH authentication | RSA-4096 / Ed25519 | Dilithium hybrid | Medium |
| Document and data signing | RSA-4096 | Dilithium | Medium |
| Encrypted backup keys | RSA-4096 | Kyber | High |
| BASC/customs encrypted communications | AES-256 + RSA | AES-256 + Kyber hybrid | High |
| API tokens (long-lived) | HMAC-SHA256 | HMAC-SHA384 (retain) | Low |

---

## Phased migration roadmap

### Phase 1: discovery and inventory (2025: complete)

- Conduct cryptographic asset discovery across all environments.
- Identify all systems, applications, and protocols using public-key cryptography.
- Classify by data sensitivity and operational criticality.
- Identify dependencies on hardware cryptographic modules.
- Assess vendor and platform PQC readiness (TLS libraries, HSM firmware, certificate authorities).

**Deliverable:** Cryptographic asset inventory registered in the Key Lifecycle Register.

### Phase 2: standards and architecture (2026)

- Adopt NIST FIPS 203, 204, and 205 as the organizational PQC standard.
- Define hybrid algorithm transition schemes for each cryptographic function.
- Update the Cryptographic Key Lifecycle Management Framework with PQC requirements.
- Evaluate and procure PQC-capable HSMs, TLS libraries, and certificate authority services.
- Update the cloud-based PKI service to support PQC hybrid certificates.

**Deliverable:** Updated cryptographic standards; PQC-capable infrastructure procured.

### Phase 3: pilot and new systems (2026 to 2027)

- Deploy PQC hybrid TLS in new system builds and infrastructure programme environments.
- Issue PQC hybrid certificates for all new PKI enrolments.
- Require PQC-compliant cryptography for all new systems entering service.
- Test PQC algorithms in production-equivalent environments.

**Deliverable:** All new systems deployed with PQC hybrid cryptography.

### Phase 4: production migration: high priority systems (2027)

- Migrate PKI root and intermediate CAs to Dilithium hybrid.
- Migrate Tier 1 (Mission Critical) systems' TLS and key management to PQC hybrid.
- Migrate BASC/customs communication encryption to AES-256 + Kyber hybrid.
- Migrate code signing infrastructure to Dilithium.
- Rekey encrypted backups with Kyber-protected keys.

**Deliverable:** All Tier 1 systems and PKI migrated to PQC hybrid cryptography.

### Phase 5: full production migration (2028)

- Complete PQC hybrid migration across all Tier 2 and Tier 3 systems.
- Migrate SSH authentication infrastructure to Dilithium hybrid.
- Retire legacy RSA-2048 and ECC P-256 certificates and keys.
- Achieve full PQC hybrid coverage across all cryptographic functions.

**Deliverable:** Organization-wide PQC transition complete; legacy algorithm retirement.

### Phase 6: pure PQC transition (2030 target, pending standards maturity)

- Remove classical algorithm components from hybrid schemes where standards and interoperability allow.
- Transition to pure PQC for newly issued certificates and keys.
- Maintain hybrid interoperability for external communications as long as required.

---

## Governance

The PQC Roadmap is reviewed annually by the CISO and Security Architecture team. Milestone progress is reported to the ERC annually. Material deviations from the roadmap require CISO approval and risk documentation.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| NIST SP 800-208 | Recommendation for Stateful Hash-Based Signature Schemes | PQC transition planning |
| NIST FIPS 203 | ML-KEM (CRYSTALS-Kyber) | Key encapsulation standard |
| NIST FIPS 204 | ML-DSA (CRYSTALS-Dilithium) | Digital signature standard |
| NIST FIPS 205 | SLH-DSA (SPHINCS+) | Stateless hash-based signatures |
| NSA CNSA 2.0 Suite | Commercial National Security Algorithm Suite 2.0 | High-assurance PQC guidance |
| ETSI TR 103 619 | Migration Strategies for Quantum-Safe Cryptography | Migration planning guidance |
| ISO/IEC 27001:2022 | Annex A.8.24 | Cryptographic controls |
| BASC International Standard v6 | Trade and customs encryption | Trade system cryptography requirements |

---

**End of Document**
