# Key Escrow and Recovery Procedure

**Document Title:** Key Escrow and Recovery Procedure\
**Document Type:** Procedure\
**Version:** 1.0.7\
**Date:** 2026-07-05\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-encryption-and-key-management.md`](policy-encryption-and-key-management.md), [`security/framework-cryptographic-key-lifecycle.md`](framework-cryptographic-key-lifecycle.md), [`security/procedure-cryptographic-key-operations.md`](procedure-cryptographic-key-operations.md), [`security/standard-privileged-access-management.md`](standard-privileged-access-management.md), [`security/standard-endpoint-hardening.md`](standard-endpoint-hardening.md), [`security/procedure-access-control.md`](procedure-access-control.md), [`security/procedure-security-incident-response.md`](procedure-security-incident-response.md), [`security/procedure-onboarding-and-offboarding.md`](procedure-onboarding-and-offboarding.md), [`resilience/procedure-backup-and-recovery.md`](../resilience/procedure-backup-and-recovery.md), [`security/roadmap-post-quantum-cryptography.md`](roadmap-post-quantum-cryptography.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material change to escrow architecture, cryptographic standards, or jurisdictional rules\
**Repository Path:** [`security/procedure-key-escrow-and-recovery.md`](procedure-key-escrow-and-recovery.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure governs key escrow and key recovery operations within the organization. It distinguishes recovery of productivity-data keys (where business continuity favours recovery) from recovery of cryptographic root and signing keys (where recovery is governed by stricter ceremony and dual control). It defines the escrow architecture, the authority model, the recovery triggers, the ceremony, and the auditable evidence retained.

---

## Scope

This procedure applies to keys held in the organization's secrets management service, hardware security modules, full-disk-encryption escrow, certificate authority key material, code-signing keys, secret-management keys, customer-managed cloud encryption keys, payment-related keys subject to PCI DSS scope, and equivalent. It distinguishes three categories with different recovery characteristics.

It does not cover ephemeral session keys, derived encryption keys without business-recoverability requirements, or backup data integrity keys whose recovery is implicit in the resilience programme.

---

## Section 1: key categories

| Category | Examples | Recovery characteristic |
| --- | --- | --- |
| Category 1: Productivity-data keys | Full-disk encryption recovery keys; user-mailbox encryption keys; collaboration-platform content keys | Recoverable by a controlled internal process to support business continuity |
| Category 2: Operational service keys | Service-account secrets; API keys; database encryption keys; backup encryption keys | Rotated rather than recovered where possible; recovery only in narrow incident scenarios |
| Category 3: Root and signing keys | CA root keys; code-signing root keys; HSM master keys; production payment-related keys | Recovery only under formal ceremony; rotation preferred; loss of these keys is a P1 incident |

The category determines the escrow design, the recovery authority, and the audit posture.

---

## Section 2: escrow architecture

### Category 1 escrow

| Control area | Requirement |
| --- | --- |
| Storage | Recovery keys escrowed automatically by the endpoint management platform; storage in the cloud or on-premises identity directory with platform-native protection |
| Access | Restricted to a defined administrative role; access logged |
| Backup | Escrow service has its own backup with documented restoration; loss of the escrow service does not lose the key material |
| Geographic redundancy | Where customer-managed-key configurations are used at scale, the escrow has documented geographic redundancy |

### Category 2 escrow

| Control area | Requirement |
| --- | --- |
| Storage | Secrets management service per the cryptographic key lifecycle framework |
| Versioning | Multiple versions retained where rotation is mid-roll-out; old versions purged after the rotation window |
| Access | Secrets accessed by service identities at runtime; human access restricted to break-glass scenarios |
| Backup | Per the platform's documented backup model; recovery tested |
| Compromise handling | Compromised secret rotated immediately; not recovered |

### Category 3 escrow

| Control area | Requirement |
| --- | --- |
| Storage | HSM-backed; offline or air-gapped storage for high-sensitivity keys |
| Key ceremony | Documented ceremony with multiple custodians and observers |
| Custody | M-of-N split custody (e.g. Shamir secret sharing) where the key material is sensitive enough to warrant it |
| Backup | Independent backup ceremony; backups stored in separate physical location with equivalent control posture |
| Compromise handling | Compromised root key is a P1 incident; rotation triggers cascading re-issuance for everything signed by the prior key |

---

## Section 3: recovery triggers

| Trigger | Permitted categories | Authority |
| --- | --- | --- |
| User locked out of their own encrypted device | Category 1 | IT service desk per the documented self-service workflow |
| Departed employee's encrypted device requires recovery of business-critical data | Category 1 | HR and IT Operations joint approval; legal counsel notified |
| Investigation requires access to a specific user's encrypted material under documented lawful basis | Category 1 | Legal Counsel approval; Data Protection Officer notified; investigation per the security incident response procedure |
| Service-account secret loss preventing automated workflow | Category 2 | Service owner approval; secret rotated rather than recovered where rotation is feasible |
| Material customer-impacting outage where a known secret is the blocker | Category 2 | Incident Coordinator approval as part of the IR procedure |
| Production payment-related key requires recovery (lost or corrupted) | Category 3 | Joint approval by CISO and CIO and Finance; PCI DSS implications reviewed |
| CA root or code-signing root recovery | Category 3 | Joint approval by CISO and CIO; documented ceremony |
| Disaster recovery testing | Categories 1, 2, and 3 | Per the resilience testing schedule; non-production keys preferred where possible |

Recovery is the exception; rotation is the default. Where rotation is feasible without business impact, rotation is preferred over recovery.

---

## Section 4: dual control and separation of duties

| Recovery class | Minimum control |
| --- | --- |
| Category 1 routine self-service | Single authorized role with logged action; user-side authentication |
| Category 1 departed-employee recovery | Two roles: requester (HR or IT Operations) and approver (CISO or delegate); logged action |
| Category 1 investigation recovery | Three approvals: requester (investigator), Legal Counsel, Data Protection Officer; logged action |
| Category 2 routine | Two roles: requester (service owner) and approver (security operations lead); logged action |
| Category 2 incident | Documented within the incident timeline; Incident Coordinator authority |
| Category 3 | Documented ceremony with at minimum three custodians and one independent observer; recorded and retained per the cryptographic policy |

No single role can complete a Category 2 or Category 3 recovery without separation of duties.

---

## Section 5: recovery ceremony (Category 3)

A Category 3 ceremony follows these steps. The ceremony is video-recorded where the policy permits, otherwise documented in a contemporaneous written record signed by all participants.

| Step | Action | Roles |
| --- | --- | --- |
| 1 | Pre-ceremony briefing: confirm authority, scope, expected output | All participants |
| 2 | Verify identities and clearances of all participants | Witness |
| 3 | Confirm physical environment integrity (room sweep, device check) | Witness |
| 4 | Retrieve sealed key shares from their secured storage | Custodians |
| 5 | Reconstitute the key per the M-of-N scheme | Custodians under witness observation |
| 6 | Perform the authorized operation (e.g. issue a new subordinate, re-sign, rotate) | Custodians |
| 7 | Destroy or re-seal shares per the documented protocol | Custodians under witness observation |
| 8 | Document the ceremony record: participants, actions taken, outputs, evidence references | Witness |
| 9 | Sign the ceremony record | All participants |
| 10 | File the ceremony record in the cryptographic operations register | Witness |

The ceremony record is retained for the lifetime of the key plus the documented retention period and is available for audit.

---

## Section 6: authorization flow

For every recovery the procedure produces a request record with:

| Field | Required content |
| --- | --- |
| Request ID | Unique identifier |
| Category | 1, 2, or 3 |
| Key identifier | Per the cryptographic key lifecycle framework |
| Requester role | Role making the request |
| Justification | Specific reason for recovery rather than rotation |
| Approver(s) | Per the dual-control matrix above |
| Privacy review | Where personal data is implicated |
| Legal review | Where the request relates to investigation, dispute, or compliance |
| Scheduled date | Where a ceremony is required |
| Outcome | Recovered, Refused, Rotated instead |
| Evidence reference | Pointer to ceremony record or system log |
| Closure | Date and signature |

---

## Section 7: post-recovery actions

| Action | Required content |
| --- | --- |
| Operational recovery | The recovered key supports the authorized operation only; not retained beyond the operation |
| Forced rotation | Where the key was recovered for any reason other than break-glass continuity, the key is rotated as soon as the recovery operation completes |
| Audit log review | All access to the key material around the recovery window reviewed |
| Notification | Affected parties (data subjects, regulators, customers) notified per the applicable obligations where the recovery creates a notification trigger |
| Lessons learned | Recoveries that revealed gaps feed the corrective action register |

---

## Section 8: lost or compromised key handling

| Class | Required response |
| --- | --- |
| Category 1 lost | Self-service rekey where possible; otherwise device reimage |
| Category 1 compromised (exposed escrow) | Treat as a personal-data exposure if Confidential or Restricted content was encrypted with the key; per the privacy breach response procedure |
| Category 2 lost | Rotate; affected service downtime accepted as the cost of the rotation |
| Category 2 compromised | P2 or P3 incident; rotate and investigate; cascade to dependent secrets |
| Category 3 lost | P1 incident; recovery ceremony from backup if available; full audit; consider trust-chain rotation if recovery integrity is uncertain |
| Category 3 compromised | P1 incident; immediate ceremony to rotate; full trust chain re-issued; customer and regulator notification per applicable rules |

---

## Section 9: post-quantum considerations

Where the affected key is in scope of the post-quantum cryptography roadmap:

1. Cryptographic-agility tooling supports a phased migration without losing escrow continuity.
2. Hybrid schemes (classical plus post-quantum) carry a documented escrow path during the transition window.
3. Recovery ceremonies during the transition explicitly note the cryptographic suite in use.

---

## Section 10: audit and assurance

| Activity | Cadence |
| --- | --- |
| Escrow service health check | Quarterly |
| Recovery test (non-disaster) | Quarterly for Category 1; annually for Category 2; per the ceremony cadence for Category 3 |
| Recovery-record completeness audit | Quarterly |
| Independent assurance over the procedure | Annual for Category 3 operations; every two years for Categories 1 and 2 |
| Metric reporting | Quarterly to the CISO; aggregate annual report to the Executive Sponsor |

---

## Operating expectations

1. The escrow service is treated as a tier-1 production service with the corresponding resilience, monitoring, and access posture.
2. Recovery is rare and intentional; the procedure favours rotation, key zeroization, or system rebuild over recovery where they meet the business need.
3. Ceremony participants are trained on the ceremony script; ceremonies are not conducted ad hoc.
4. Loss of key escrow integrity is treated with the same seriousness as loss of the key material itself.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27002:2022 | §8.24 to §8.28 | Cryptographic controls |
| NIST SP 800-57 Part 1 Rev. 5 | Recommendation for Key Management | Key lifecycle |
| NIST SP 800-130 | A Framework for Designing Cryptographic Key Management Systems | CKMS design |
| NIST SP 800-152 | A Profile for U.S. Federal Cryptographic Key Management Systems | Federal profile reference |
| NIST FIPS 140-3 | Security Requirements for Cryptographic Modules | HSM baseline |
| CSA Cloud Controls Matrix v4.1 | CEK domain | Cloud cryptography |
| ETSI EN 319 411 | Trust services for issuing certificates | Where the organization operates a CA |
| PCI DSS v4.0.1 | Requirement 3 | Payment-data cryptography where applicable |
| RFC 5280 | X.509 PKI | CA operations |
| Cryptographic Key Lifecycle Management Framework (internal) | Cross-walk | Authoritative cross-reference |

---

## Limitations

This procedure is a CC BY-SA 4.0 baseline. Specific cryptographic and HSM configurations vary; the procedure expresses the control and ceremony requirements rather than vendor-specific settings. Adopting organizations select escrow tooling per the supplier programme and tune the ceremony script to their specific cryptographic suite. The procedure is not a substitute for HSM vendor documentation or PCI DSS QSA guidance where in scope.

---

**End of Document**
