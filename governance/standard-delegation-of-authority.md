# Delegation-of-Authority Standard

**Document Title:** Delegation-of-Authority Standard\
**Document Type:** Standard\
**Version:** 0.0.2\
**Date:** 2026-08-31\
**Owner:** GRC Programme Manager\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/register-role-authority.md`](register-role-authority.md), [`governance/register-key-terms-and-definitions.md`](register-key-terms-and-definitions.md), [`governance/policy-exception-and-risk-acceptance-management.md`](policy-exception-and-risk-acceptance-management.md), [`security/procedure-access-control.md`](../security/procedure-access-control.md), [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md), [`governance/principle-capability-is-not-authority.md`](principle-capability-is-not-authority.md), [`governance/register-data-retention-schedule.md`](register-data-retention-schedule.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual or as required by regulatory or framework change\
**Repository Path:** [`governance/standard-delegation-of-authority.md`](standard-delegation-of-authority.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines the delegation instrument: the recorded artefact by which a role holding an authority grants some part of it to another subject. The corpus provides typical, adjustable role authorities ([`governance/register-role-authority.md`](register-role-authority.md), whose column is "Typical Approval Authority") and refers to delegation only incidentally ("or delegate", "CIO or delegate"), with no standard for how a delegation is constituted, bounded, evidenced, sub-delegated, or revoked. This standard supplies that instrument, so a delegated authority is as governed as the authority it derives from.

It operationalizes the corpus definition of [`Authorize`](register-key-terms-and-definitions.md) ("a delegated grant of permission to a specific subject to perform a specific action; narrower in scope than approval and typically session- or task-bounded"), and it applies the [`capability-is-not-authority`](principle-capability-is-not-authority.md) principle: a delegate's ability to act comes from the recorded delegation, not from access, seniority, or the grantor's absence.

## 2. Applicability

Applies to every delegation of a governance, approval, access, or operational authority the corpus assigns to a role, whether the delegate is a person, a role, a system, or an AI agent, and whether the delegation is standing or temporary (including acting-in-post and emergency deputies). It does not change who holds an authority; it governs how that authority is delegated. Domain-specific delegated roles (the Delegated Security Lead, an acting Incident Commander, a delegated CAB chair) apply this standard on top of their domain procedures.

## 3. Relationship to other GRC documents

- [`governance/register-role-authority.md`](register-role-authority.md) provides the typical, adjustable role authorities (its "Typical Approval Authority" column is to be adjusted by the adopting organization by law, regulation, sector, size, and risk appetite); the adopter's authoritative authority schedule is the source a delegation is issued from, and a delegation never grants more than the grantor holds under it.
- [`governance/register-key-terms-and-definitions.md`](register-key-terms-and-definitions.md) defines `Authorize` (the delegated grant) and `Approve`; this standard operationalizes the former.
- [`governance/policy-exception-and-risk-acceptance-management.md`](policy-exception-and-risk-acceptance-management.md) uses tiered "CIO or delegate" approval; its tiered chain is the authoritative model this standard references, not restates.
- [`security/procedure-access-control.md`](../security/procedure-access-control.md) and [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md) supply the emergency-deputy construct (the Delegated Security Lead), whose approved emergency authorization is a delegation instance; the break-glass account or credential itself is a withheld capability, not a delegation (per [`principle-capability-is-not-authority`](principle-capability-is-not-authority.md)).
- [`governance/principle-capability-is-not-authority.md`](principle-capability-is-not-authority.md) is the principle this standard enforces: authority is conferred by the recorded delegation, never by capability.

## 4. Minimum requirements

### 4.1 The delegation instrument

Every delegation is a recorded instrument carrying, at minimum:

1. **Grantor**: the role holding the authority being delegated (per the adopter's authority schedule), and the incumbent subject holding that role at the time of the grant.
2. **Delegate (grantee)**: the specific subject receiving it (person, role, system, or AI agent).
3. **Scope**: the specific authority or decisions delegated, bounded to the minimum needed.
4. **Duration**: effective and expiry dates, or the condition that ends it; delegations are time-bounded by default.
5. **Constraints and conditions**: ceilings, triggers ("only when the grantor is unavailable"), and exclusions.
6. **Evidence**: the instrument is documented, dated, attributable, and traceable; delegation is granted in writing.
7. **Identifier and lineage**: a unique instrument identifier; for a sub-delegation, the parent instrument's identifier; and the identifiers of the entitlements granted under it, so revocation can propagate demonstrably.

### 4.2 Grantor authority and separation of duties

A delegation is valid only if the grantor actually holds the authority under the adopter's authoritative authority schedule (the corpus register-role-authority provides typical, adjustable authorities, not the definitive grant), the authority is delegable, and the grantor is permitted to delegate it, and it never grants more than the grantor holds. Separation of duties is preserved across the delegation: a delegation does not combine, in one subject, authorities the corpus keeps apart.

### 4.3 Sub-delegation

A delegate may onward-delegate only if the instrument expressly grants that right, never to a broader scope or a longer duration than the parent grant, and only to the depth the parent permits. Absent an express grant, sub-delegation is prohibited.

### 4.4 Revocation and revocation-propagation

The grantor can revoke a delegation, with the revocation taking effect promptly; a delegation is also revoked automatically on a lifecycle event of the grantor incumbent or the delegate appropriate to its subject type (a person's role change or separation; a role's reassignment; a system's or AI agent's decommissioning or scope change). When a delegation is revoked, every sub-delegation and every entitlement recorded in its lineage (field 7) is also revoked, and this propagation is tested rather than assumed. Delegated privileges are reviewed on a defined cadence.

## 5. Evidence requirements

- The delegation instrument for each active delegation (the fields in 4.1, including its identifier and lineage), retained under the `Governance authorization and delegation records` category in the Data Retention Schedule ([`governance/register-data-retention-schedule.md`](register-data-retention-schedule.md)) for seven years after expiry or revocation.
- Evidence that the grantor held the delegated, delegable authority under the authority schedule at the time of the grant.
- Revocation records, including the propagation check that downstream sub-delegations and entitlements were removed.
- The periodic review record of active delegated privileges.

## 6. Compliance notes

Delegation is proportionate to the authority delegated: a routine operational delegation is lighter than a delegation of an approval authority with financial or safety consequence, which carries tighter scope, shorter duration, and closer review. This standard states the instrument; the enforcing checks live in the access-control and privileged-access controls and the role-authority register, and the records-retention schedule governs how long the instruments are kept.

## 7. Framework alignment

The alignment below is analogical (each row aligns with or is informed by the cited reference) and at the control-family and category level, not a prescriptive crosswalk. Control identifiers are verified against the held source texts.

| Requirement | NIST SP 800-53 Rev. 5 | ISO/IEC 27001:2022 | NIST CSF 2.0 |
| --- | --- | --- | --- |
| Delegated authority is scoped to the minimum needed | AC-6 (Least Privilege) | A.5.15 (Access control) | PR.AA (category); PR.AA-05 |
| The grantor holds the authority; separation of duties is preserved | AC-5 (Separation of Duties) | A.5.3 (Segregation of duties) | PR.AA (category); PR.AA-05 |
| The delegation is recorded, managed, and time-bounded | AC-2 (Account Management) | A.5.18 (Access rights) | PR.AA (category) |
| Revocation is effective and delegated privileges are reviewed | AC-2 (Account Management); AC-6(7) (Review of User Privileges) | A.5.18 (Access rights) | PR.AA (category); PR.AA-05 |

A delegation is the mechanism by which one role's authority is exercised by another subject under governance; it composes with the capability-is-not-authority principle, which fixes that the authority comes from the recorded grant, never from the delegate's capability to act.
