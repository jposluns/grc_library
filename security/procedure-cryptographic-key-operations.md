# Cryptographic Key Operations Procedure

**Document Title:** Cryptographic Key Operations Procedure\
**Document Type:** Procedure\
**Version:** 1.0.3\
**Date:** 2026-07-23\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`security/framework-cryptographic-key-lifecycle.md`](framework-cryptographic-key-lifecycle.md), [`security/roadmap-post-quantum-cryptography.md`](roadmap-post-quantum-cryptography.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material cryptographic standard or operational change\
**Repository Path:** [`security/procedure-cryptographic-key-operations.md`](procedure-cryptographic-key-operations.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure defines the step-by-step operational instructions for all cryptographic key operations including generation, registration, distribution, activation, rotation, revocation, and destruction. It implements the controls established in the Cryptographic Key Lifecycle Management Framework and ensures that consistent, auditable execution of key management operations is achieved.

---

## Scope

Applies to all cryptographic key operations performed by IT Operations, Security Architecture, and any personnel authorized to manage cryptographic material. Covers symmetric keys, asymmetric key pairs, digital certificates, SSH keys, and API tokens across all organizational platforms.

---

## Roles and responsibilities

| Role | Responsibility |
| --- | --- |
| **Security Architecture** | Designs key management architecture; approves new key types and algorithms. |
| **IT Operations: Key Custodian** | Executes key operations; maintains Key Lifecycle Register. |
| **CISO** | Approves non-standard key operations; reviews KLR quarterly. |
| **System / Application Owner** | Requests keys for their systems; approves rotation schedules. |
| **Internal Audit** | Audits KLR completeness and key operation logs annually. |

Dual control is required for all key generation, export, and destruction operations: no single person may perform these operations unilaterally.

---

## 1. Key generation

1.1 Submit a key generation request through the ITSM portal specifying: key type, algorithm, key length, intended use, system/application, and required validity period.

1.2 The Security Architecture team reviews and approves the request, confirming algorithm compliance with the Cryptographic Key Lifecycle Management Framework.

1.3 Key generation is performed using FIPS 140-3 validated Hardware Security Modules (HSMs) or approved software cryptographic libraries.

1.4 Two authorized Key Custodians must be present or cryptographically authenticate for key generation.

1.5 Upon generation, the Key Custodian registers the key in the Key Lifecycle Register with all required fields.

1.6 Key generation events are logged with: date/time, key ID, algorithm, key length, generating system, and operator identities.

---

## 2. Key registration

2.1 All generated keys must be registered in the Key Lifecycle Register within 1 business day of generation.

2.2 Required registration fields:
- Unique key ID.
- Key type and algorithm.
- Key length.
- Owner (role title).
- Intended usage scope.
- Validity period (issue and expiry dates).
- Rotation schedule.
- Storage location (HSM slot, certificate store, etc.).
- Status: Active.

---

## 3. Key distribution

3.1 Keys are distributed only to authorized systems and personnel as defined in the approved access list.

3.2 Distribution channels:
- Public keys: distributed via PKI certificate exchange or encrypted API (TLS 1.3+).
- Symmetric keys: distributed via HSM-to-HSM transfer or encrypted key wrapping.
- Certificates: distributed via enterprise PKI or approved cloud-based PKI service.

3.3 No key material is transmitted in plaintext. Email distribution of key material is prohibited.

3.4 Distribution events are logged with: key ID, recipient system/role, distribution method, date/time.

---

## 4. Key activation

4.1 Keys are activated in the target system or application by the system owner or authorized operator.

4.2 Activation is recorded in the Key Lifecycle Register: activation date, activating operator, target system.

4.3 For high-sensitivity systems, activation requires CISO approval.

---

## 5. Key rotation

5.1 Keys are rotated per the schedule defined in the Cryptographic Key Lifecycle Management Framework:
- Symmetric keys: every 90 days.
- Asymmetric key pairs: every 12 months.
- Digital certificates: before expiry, with a minimum 30-day lead time.
- SSH keys: annually or upon personnel change.

5.2 Rotation procedure:
1. Generate new key following Section 1 above.
2. Register new key in KLR.
3. Deploy and activate new key in target system(s).
4. Verify system operation with new key.
5. Revoke old key following Section 6 below.
6. Update KLR with rotation event and new rotation schedule.

5.3 Automated rotation alerts are configured in the key management system for keys approaching expiry.

---

## 6. Key revocation

6.1 Keys are revoked immediately upon: suspected compromise, confirmed compromise, employee departure (where key is personal), or at end of key validity.

6.2 Revocation procedure:
1. CISO or Key Custodian initiates revocation with documented justification.
2. Key status is updated to Revoked in the KLR immediately.
3. For certificate keys: Certificate Revocation List (CRL) or OCSP is updated.
4. Key is removed from all dependent systems.
5. All systems dependent on the revoked key are identified and migrated to replacement keys within 24 hours for critical systems and 72 hours for non-critical systems.
6. Revocation event is logged with: key ID, reason, operator, date/time.

---

## 7. Key destruction

7.1 Keys are destroyed when: revoked and no longer needed, at end of planned lifecycle, or upon system decommission.

7.2 Destruction procedure:
1. Key Custodian submits a destruction request approved by CISO.
2. Two Key Custodians must witness or cryptographically authenticate destruction.
3. Keys stored in HSMs are destroyed via the HSM's cryptographic erasure function.
4. Keys stored in software are overwritten using approved secure deletion methods.
5. KLR is updated: status set to Destroyed, destruction date and operator recorded.
6. A certificate of destruction is retained in the compliance repository.

---

## 8. Key compromise response

8.1 Any suspected key compromise is treated as a security incident and reported to the CISO immediately.

8.2 Compromised keys are revoked within 1 hour of confirmed compromise.

8.3 The incident is logged in the incident management system and a post-incident review conducted within 5 business days.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27002:2022 | §8.24 to §8.28: Cryptographic Controls | Key operation controls |
| NIST SP 800-57 Parts 1 to 3 | Key Management Guidelines | Key operational procedures |
| NIST FIPS 140-3 | Security Requirements for Cryptographic Modules | HSM and module requirements |
| COBIT 2019 | DSS05: Managed Security Services | Security service operations |
| CSA CCM v4.1 | CEK-01 through CEK-04 | Cloud key management operations |

---

**End of Document**
