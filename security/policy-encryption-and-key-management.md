# Encryption and Key Management Policy

**Document Title:** Encryption and Key Management Policy\
**Document Type:** Policy\
**Version:** 1.3.13\
**Date:** 2026-07-24\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/standard-data-classification-and-handling.md`](standard-data-classification-and-handling.md), [`security/standard-data-loss-prevention.md`](standard-data-loss-prevention.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material threat, framework, or regulatory change\
**Repository Path:** [`security/policy-encryption-and-key-management.md`](policy-encryption-and-key-management.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

Defines mandatory encryption and cryptographic key management requirements. Ensures that confidentiality, integrity, and availability are protected through consistent encryption controls for data at rest, in transit, and in use.

---

## 2. Scope

1. Applies to all digital and physical information assets including: databases, file systems, and backups; cloud-hosted systems, SaaS platforms, and endpoint devices; AI datasets, model artifacts, and inference logs; trade and customs data governed by BASC across Latin American operations.
2. Covers encryption during all states: at rest, in transit, in use.
3. Applies to all employees, contractors, vendors, and service providers with system access.
4. Encompasses key generation, storage, distribution, rotation, and destruction.

---

## 3. Governance and accountability

| Role | Responsibility |
|---|---|
| CIO | Approves encryption standards and ensures that alignment with enterprise risk strategy is maintained. |
| CISO | Owns encryption controls, defines key management processes, and ensures that compliance monitoring is performed. |
| IT Operations / Security Engineering | Ensures that all cryptographic implementation procedures and key-management runbooks are maintained for traceability and lifecycle verification. |
| Application Owners / Developers | Ensure that encryption requirements are applied within systems and APIs. |
| Compliance / GRC Programme Manager | Monitors adherence and maintains evidence for audit and certification. |
| AI Governance Council (AIGC) | Oversees encryption of AI datasets, model artifacts, and explainability data. |

Sector-conditional roles (for example, a BASC Regional Compliance Officer who verifies trade-data encryption and customs-communication security for organizations participating in BASC) apply where the organization participates in a covered sector programme; see [`compliance/`](../compliance/).

---

## 4. Encryption standards

| State | Requirement | Approved Standards |
|---|---|---|
| At Rest | Encrypt all sensitive, confidential, and restricted data. | AES-256 or stronger (FIPS 140-3 validated). |
| In Transit | Encrypt all external and internal communications. | TLS 1.3 or stronger; SSH 2.0 or stronger. |
| In Use | Protect data processed in volatile memory through secure enclaves or hardware encryption where supported. | Trusted Execution Environments (TEE), SGX, SEV. |
| AI and Model Data | Apply encryption for model weights, datasets, and configuration files. | AES-256-GCM (AEAD: confidentiality with built-in integrity tag); HKDF-SHA-256 for key derivation from high-entropy material; Argon2id (or scrypt) for password-derived keys. SHA-512 alone is a hash function, not a key-derivation function. |
| BASC Customs and Trade Data | Ensure that encryption is applied for all cargo manifests, customs documentation, and trade communications. | AES-256 + PKI certificates validated by BASC chapter or WCO SAFE authority. |

---

## 5. Cryptographic key management

### 5.1 Key generation

Keys generated using FIPS 140-3 certified hardware or software modules. Default, hard-coded, or vendor-supplied keys are prohibited.

### 5.2 Key distribution

Symmetric keys distributed via encrypted channels (TLS 1.3+). Asymmetric key exchange via authenticated PKI.

### 5.3 Key storage

Keys stored in dedicated Hardware Security Modules (HSMs) or a cloud key management service (KMS). Keys must never be stored in plaintext or embedded in source code.

### 5.4 Key rotation

Encryption keys rotated at least every 90 days for Restricted data and annually for other categories. Immediate rotation required after personnel changes or suspected compromise. This classification-based cadence corresponds to the key-type cadence in the Cryptographic Key Lifecycle Management Framework: the 90-day Restricted cycle aligns with symmetric keys, and the annual other-category cycle with asymmetric keys.

### 5.5 Key destruction

Retired or expired keys destroyed using cryptographic erase (per NIST SP 800-88). Destruction events logged in the Key Lifecycle Register and retained for seven years.

---

## 6. Cryptographic algorithms and hashing

| Category | Approved Algorithms |
|---|---|
| Symmetric encryption | AES-256, ChaCha20-Poly1305 |
| Asymmetric encryption | RSA-4096, ECC P-384 or stronger |
| Hashing | SHA-512, BLAKE2b |
| Password-based encryption | Argon2id (preferred) at minimum m=19456 (19 MiB), t=2, p=1; or PBKDF2-HMAC-SHA256 at minimum 600,000 iterations (PBKDF2-HMAC-SHA512 at minimum 220,000), per the OWASP Password Storage Cheat Sheet |
| Post-quantum cryptography | ML-KEM (formerly CRYSTALS-Kyber; NIST FIPS 203, August 2024) for key encapsulation and ML-DSA (formerly CRYSTALS-Dilithium; NIST FIPS 204, August 2024) for digital signatures, at NIST security category 3 as the baseline (ML-KEM-768, ML-DSA-65) and category 5 (ML-KEM-1024, ML-DSA-87) for long-lived or high-assurance data; SLH-DSA (NIST FIPS 205, August 2024) where a conservative hash-only signature assumption is required; hybrid key exchange (ECC + PQC) during migration. See the [Post-Quantum Cryptography Readiness Roadmap](roadmap-post-quantum-cryptography.md) for parameter-set selection and crypto-agility |

---

## 7. Cloud and SaaS encryption requirements

### 7.1 Cloud storage

Cloud storage must enforce:

- Customer-managed keys (CMK) with a defined rotation schedule.
- Audit logging for all key access and rotation events.
- Integration with centralized Key Management Service (KMS).

### 7.2 Cloud productivity and collaboration platforms

Cloud productivity platform, collaboration platform, and file storage must use sensitivity labels and encryption policies mapped to classification levels per the Data Classification and Handling Standard.

### 7.3 Data loss prevention

DLP enforcement must block or encrypt Restricted and Confidential data shared externally.

---

## 8. BASC trade-data protection

### 8.1 Encryption requirements

All trade, customs, and cargo data in BASC-certified regions (Colombia, Mexico, Peru, Chile) must:

- Be encrypted at rest and in transit per ISO 28000 and BASC Section 6.
- Utilize PKI authentication for customs and government system integration.
- Maintain tamper-proof audit logs of encryption and decryption events.

### 8.2 Key custody

Trade-data decryption keys must remain under organizational or BASC-validated custody only.

### 8.3 Violations

Unauthorized decryption, key export, or sharing constitutes a Critical BASC Violation and triggers investigation under the Incident Response Procedure.

---

## 9. AI and data encryption requirements

### 9.1 Dataset encryption

AI datasets containing personal or proprietary information must be encrypted in transit and at rest.

### 9.2 Key separation

Encryption keys must be separate from AI training environments and stored in secure HSMs.

### 9.3 Model encryption logs

Model encryption logs must be linked to AI system entries in the AI Audit Repository.

### 9.4 Explainability files

Model explainability files (e.g., SHAP/LIME outputs) must be encrypted and access-controlled per Restricted classification.

---

## 10. Monitoring and compliance

| Activity | Frequency | Owner |
|---|---|---|
| Continuous encryption compliance monitoring via SIEM and KMS dashboards | Ongoing | CISO / IT Operations |
| Encryption compliance audit | Quarterly | CISO and Compliance Manager |
| Sector-programme audit of programme-specific encryption (for example, customs data and cargo communications encryption under BASC where the organization participates) | At the cadence stated by the relevant sector annex | Sector-conditional role per the annex; see [`compliance/`](../compliance/) |
| Findings and remediation actions logged in CAPA Register | Per finding | Compliance / GRC Programme Manager |

---

## 11. Exceptions

### 11.1 Standard exceptions

Exceptions require:

- Written approval from the CISO and CIO.
- Documented business justification and risk assessment.
- A temporary exception record in the Exception Register.

### 11.2 Sector-programme exceptions

Where the organization participates in a sector programme that imposes additional encryption requirements (for example, BASC for customs-data encryption), exceptions to those programme-specific controls are not permitted unless explicitly authorized by the sector-conditional role defined by the relevant sector annex and the Enterprise Risk Committee; see [`compliance/`](../compliance/).

---

## 12. Continual improvement

### 12.1 Annual review

The CISO and AIGC review encryption standards annually against evolving regulatory, quantum, and BASC requirements.

### 12.2 Lessons learned

Lessons learned from incidents or audits feed into the continual improvement cycle.

### 12.3 Policy metrics

| Metric | Description |
|---|---|
| Encryption coverage | Coverage by classification level |
| Key rotation SLA adherence | Percentage of keys rotated within scheduled windows |
| BASC encryption compliance rate | Success rate across BASC-certified regions |
| PQC algorithm adoption progress | Percentage of eligible systems migrated to hybrid or PQC schemes |

---

## 13. Framework alignment

| Framework | Reference |
|---|---|
| ISO/IEC 27002:2022 | §§8.24 to 8.28: Cryptographic Controls |
| COBIT 2019 | DSS05.03: Protect Against Data Leakage |
| CSA CCM v4.1 | CEK-01: Encryption and Key Management |
| NIST SP 800-57 | Key Management Guidelines |
| NIST SP 800-208 | Post-Quantum Cryptography Readiness |
| PCI DSS v4.0.1 | Requirement 3: Encryption and Key Management |
| BASC International Standard (v6 2022) | Trade and Customs Data Security |
| WCO SAFE Framework (2025 edition) | Supply Chain Security |
| ISO 28000:2022 | Supply-Chain Security and Resilience |

---

*This document is released under CC BY-SA 4.0. No rights reserved.*



**End of Document**
