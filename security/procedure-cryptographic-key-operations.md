# Cryptographic Key Operations Procedure

**Document Title:** Cryptographic Key Operations Procedure\
**Document Type:** Procedure\
**Version:** 1.5.0\
**Date:** 2026-10-14\
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
| **Legal Counsel** | Confirms under 7.1 whether a legal hold or investigation covers data a key protects, and is the only role that can confirm an external-authority investigation or a hold that is required but not yet recorded; gives the written release under 7.1. |
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
- Status: Pre-activation on generation, changed to Active only when the key is authorized and available for use (NIST SP 800-57 Part 1 Rev. 5, section 7.1).

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
4. Key is removed from use for applying new cryptographic protection; controlled access for decryption or verification may be retained where the key's state and recipient-usage period permit, until dependent data is re-encrypted or destroyed (NIST SP 800-57 Part 1 Rev. 5, sections 5.3.6 and 7.4).
5. All systems dependent on the revoked key are identified and migrated to replacement keys within 24 hours for critical systems and 72 hours for non-critical systems.
6. Revocation event is logged with: key ID, reason, operator, date/time.

---

## 7. Key destruction

7.1 Secret and private keys are destroyed when: revoked and no longer needed, at end of planned lifecycle, or upon system decommission. A retired or expired public key or public-key certificate is not subject to the all-traces destruction in 7.2 (NIST SP 800-57 Part 1 Rev. 5, section 8.3.4). As an organizational rule, it is removed from active use and distribution so that it is not used to apply new cryptographic protection. It is retained or archived for as long as needed to verify information signed with the corresponding private key (section B.3.1.2); otherwise it may be retained or destroyed (section 8.3.4), subject to the legal hold and investigation check below. When a public key or public-key certificate is retained or archived, the Key Custodian sets its KLR status to Deactivated unless it is Revoked, and records the retention or archive location and reason in its Destruction Record. A data-encryption key is destroyed only after the data it protects has been re-encrypted under a new key or destroyed, and a key-wrapping key is retained while any key it protects is still needed ([Encryption and Key Management Policy](policy-encryption-and-key-management.md), section 5.5). Before a key is destroyed or zeroized, including the purge of a superseded key version and the destruction of key shares, the Key Custodian confirms whether a legal hold or investigation covers data the key protects, directly or through a key it wraps. For a public key, data the key protects includes information signed with the corresponding private key. This is the single key destruction check, and the [Key Escrow and Recovery Procedure](procedure-key-escrow-and-recovery.md) sends its purge, share destruction and zeroization steps here. The check uses the two-part confirmation in rule 2 of the lost or stolen device decision table in [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) §5.2.1, applied to that data. First, for recorded holds, the Key Custodian obtains the confirmation from Legal Counsel or checks both the retention hold recorded in the Records Register ([Records Retention and Destruction Standard](../governance/standard-records-retention-and-destruction.md), section 7, Retention hold and litigation freeze) and the legal hold status tracked in the GRC platform ([Data Retention Schedule](../governance/register-data-retention-schedule.md), Legal holds). Second, those records alone do not complete the check, because neither shows an investigation or a hold that is required but not yet recorded. Legal Counsel or the Incident Commander or, for P3 and P4 where no Incident Commander is assigned, the SOC lead confirms whether an investigation under the [Security Incident Response Procedure](procedure-security-incident-response.md) treats that data or the key as evidence. Only Legal Counsel confirms whether an investigation by an external authority does so, and whether a hold is required but not yet recorded. If a hold or investigation applies, or either part cannot be completed, the key is retained under Key Custodian custody and is not destroyed or zeroized. It stays retained until Legal Counsel, in writing, releases the hold or narrows it so that it no longer covers that data, or, for an investigation without a legal hold, confirms that the investigation no longer treats that data or the key as evidence, consistent with rule 8 of the same decision table.

7.2 Destruction procedure. Where a public key or public-key certificate is destroyed by choice under 7.1, the Key Custodian attaches the record of both parts of the 7.1 check to the destruction request and obtains CISO approval before destruction, without the per-copy listing in step 1; steps 2, 6 and 7 apply, with step 6 confirming destruction of the key as identified in the destruction request and the certificate of destruction identifying the key instead of each copy, and steps 3 to 5 do not apply. Otherwise:
1. Key Custodian must identify every copy of a secret or private key and ensure that every copy is destroyed as soon as it is no longer required, subject to section 7.1 (NIST SP 800-57 Part 1 Rev. 5, section 8.2.2, Backup Storage subsection, and section 8.3.4). Before seeking CISO approval, the Key Custodian uses the KLR, the distribution events logged under 3.4, and escrow and backup records to list every copy and its location in the destruction request, including backup, archived, escrowed, wrapped and replicated copies, copies in other HSMs or cloud key services, copies held by third parties, and key shares on cards or paper. The Key Custodian attaches the record of both parts of the 7.1 check and obtains CISO approval of the complete request before any destruction.
2. Two Key Custodians must witness or cryptographically authenticate destruction.
3. Where section 7.1 retains the key, no copy is destroyed or zeroized, and the Key Custodian records each listed copy in the destruction request with its location, custodian and retention reason; destruction remains deferred until section 7.1 permits it. Otherwise, every listed copy is destroyed using the applicable method in step 4 or 5.
4. Each listed copy stored in an HSM is destroyed via the HSM's zeroization function so that, for a secret or private key, all traces of that copy are removed and that copy cannot be recovered by physical or electronic means (NIST SP 800-57 Part 1 Rev. 5, section 8.3.4).
5. Each listed copy stored in software is overwritten using approved secure deletion methods so that, for a secret or private key, all traces of that copy are removed and that copy cannot be recovered by physical or electronic means (NIST SP 800-57 Part 1 Rev. 5, section 8.3.4). Where HSM zeroization or software overwrite is not applicable to a listed copy, including copies in cloud key services, key shares on cards or paper, or copies held by a third party, use the provider's or holder's documented destruction method that, for a secret or private key, removes all traces of the key material so that it cannot be recovered by physical or electronic means. For destruction performed by a provider or holder, the dual control required by step 2 is met when two Key Custodians authorize the destruction request and review the provider's or holder's destruction evidence.
6. The Key Custodian sets the KLR status to Destroyed and records the destruction method, date and operator and, for a secret or private key, each copy's method, date and operator in the key record's Destruction Record only after confirming that every listed copy has been destroyed; otherwise, the status must not be set to Destroyed and the outstanding copies and their disposition are recorded in the destruction request.
7. A certificate of destruction is retained in the compliance repository for destruction performed, identifying each copy destroyed, its location, the method used, the destruction date, the operator and the witnessing or authenticating Key Custodians, and including supporting evidence from the provider or holder where its documented destruction method was used. The Key Custodian records the certificate reference in the key record's Destruction Record or, where destruction is incomplete, in the destruction request with the outstanding copies; when destruction completes, the Destruction Record references every certificate issued for the key, including any recorded earlier in the destruction request.

---

## 8. Key compromise response

8.1 Any suspected key compromise is treated as a security incident and reported to the CISO immediately.

8.2 Compromised keys are revoked within 1 hour of confirmed compromise.

8.3 The incident is logged in the incident management system and a post-incident review conducted within 5 business days.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27002:2022 | §8.24: Use of cryptography | Key operation controls |
| NIST SP 800-57 Part 1 Rev. 5 | Recommendation for Key Management, Part 1: General | Key operational procedures |
| NIST SP 800-57 Part 2 Rev. 1 | Recommendation for Key Management, Part 2: Best Practices for Key Management Organizations | Key management organization procedures |
| NIST SP 800-57 Part 3 Rev. 1 | Recommendation for Key Management, Part 3: Application-Specific Key Management Guidance | Application-specific key operational procedures |
| NIST FIPS 140-3 | Security Requirements for Cryptographic Modules | HSM and module requirements |
| NIST SP 800-38F | Recommendation for Block Cipher Modes of Operation: Methods for Key Wrapping (December 2012), 3.1 Overview | Protection of symmetric keys distributed by key wrapping |
| NIST SP 800-130 | A Framework for Designing Cryptographic Key Management Systems (August 2013), 6.2.1 Metadata Elements (b) to (d) and 8.2.4 Auditing and Remote Monitoring | Key identifier, owner and lifecycle-state metadata; audit of key generation, activation, revocation and destruction events with time and initiator |
| NIST SP 800-88 Rev. 2 | Guidelines for Media Sanitization (September 2025), 3.2.3 Sanitization of Keys | Recommended zeroization of target cryptographic keys for cryptographic erase |
| COBIT 2019 | DSS05: Managed Security Services | Security service operations |
| CSA CCM v4.1 | CEK-02, CEK-10, CEK-11, CEK-12, CEK-13, CEK-14, CEK-15, CEK-21, LOG-12 | Cloud key management operations |

---

**End of Document**
