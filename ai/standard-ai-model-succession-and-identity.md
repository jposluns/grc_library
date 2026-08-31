# AI Model Succession and Identity Continuity Standard

**Document Title:** AI Model Succession and Identity Continuity Standard\
**Document Type:** Standard\
**Version:** 0.0.1\
**Date:** 2026-08-31\
**Owner:** AI Governance Approver\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/procedure-foundation-model-lifecycle.md`](procedure-foundation-model-lifecycle.md), [`ai/procedure-ai-model-lifecycle-management.md`](procedure-ai-model-lifecycle-management.md), [`ai/standard-ai-access-and-agent-permissions.md`](standard-ai-access-and-agent-permissions.md), [`ai/register-model-registry.md`](register-model-registry.md), [`governance/standard-delegation-of-authority.md`](../governance/standard-delegation-of-authority.md), [`governance/principle-capability-is-not-authority.md`](../governance/principle-capability-is-not-authority.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material model-platform, capability, or supplier-model change\
**Repository Path:** [`ai/standard-ai-model-succession-and-identity.md`](standard-ai-model-succession-and-identity.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

When an AI model or an action-capable agent is succeeded by a new version, the predecessor's standing does not transfer to the successor by default. Standing here means the approvals the predecessor held (its production or use approval), the delegations and access granted to it, and any forum or decision standing it exercised. A successor is a new subject for authority purposes, and it establishes its own standing on evidence rather than inheriting the predecessor's by continuity of name or platform.

This standard sets the requirements for that transition: the evidence a successor presents to establish standing, a pause-and-compare validation before it assumes standing, the handling of approvals and decisions in flight at the transition moment, and the re-issuance of access and delegations to the successor identity. It complements the version-transition risk reassessment in [`ai/procedure-foundation-model-lifecycle.md`](procedure-foundation-model-lifecycle.md) and the lineage tracking in [`ai/register-model-registry.md`](register-model-registry.md), which record that a transition occurred; this standard governs what the successor must satisfy for its standing to be recognized.

## 2. Scope

This standard applies to any transition from one version of an AI model or agent to another where the successor would exercise standing the predecessor held: a foundation-model version upgrade, a fine-tuned or retrained internal model, a re-based agent, or a supplier-driven model substitution. It applies whether the successor is more, less, or equivalently capable, because standing follows the recorded grant and its evidence, not the successor's capability (per [`governance/principle-capability-is-not-authority.md`](../governance/principle-capability-is-not-authority.md)).

It does not govern the training, evaluation, or engineering of the successor itself (the model lifecycle procedures govern those), nor the retirement mechanics of the predecessor beyond the standing and access it must relinquish.

## 3. Principles

| Principle | Statement |
| --- | --- |
| No automatic inheritance | A successor does not inherit the predecessor's approvals, delegations, access, or forum standing by default; each is re-established on evidence. |
| Identity is per-version | For authority purposes each model or agent version is a distinct identity; a shared name or endpoint does not make the successor the same subject as the predecessor. |
| Evidence before standing | The successor presents the documentation, validation, and integrity evidence for the standing it seeks before that standing is recognized. |
| Pause and compare | Standing transfers only after a paused comparison of successor against predecessor on a representative set, not on release alone. |
| Least privilege across the transition | Access and delegations are re-issued to the successor scoped to the minimum the successor's task needs, never copied wholesale from the predecessor. |
| Reversibility | The predecessor's standing and access are retained until the successor's standing is validated, so a failed transition can fall back. |

---

## 4. Successor standing criteria (inheritance evidence)

A successor establishes standing by presenting, for each class of standing it seeks, the evidence that the standing's original grant required. At minimum:

1. **Model documentation.** Current documentation for the successor version (its purpose, training and data provenance, evaluation results, and known limitations), maintained to the same requirement as the predecessor's.
2. **Validation evidence.** Independent validation that the documentation is accurate and that the successor meets the acceptance criteria the standing depends on.
3. **Integrity evidence.** Confirmation that the successor artefact is the validated artefact (a recorded integrity check tying the deployed model to the one that was validated).
4. **Grant-specific evidence.** For each approval, delegation, or access the successor seeks to carry, the evidence that the original grant named (for a production-use approval, the approval's own acceptance criteria; for a delegation, a fresh delegation instrument per [`governance/standard-delegation-of-authority.md`](../governance/standard-delegation-of-authority.md)).

Standing that the successor does not seek, or cannot evidence, lapses with the predecessor rather than carrying silently.

## 5. Pause-and-compare validation

Before the successor assumes any standing, its behaviour is compared against the predecessor's in a paused state, on a representative evaluation set covering the tasks the standing authorizes:

1. The comparison runs before cutover, with the predecessor still holding standing, so the successor is not exercising authority it has not yet earned.
2. Material behaviour changes are reassessed for risk per the version-transition reassessment in [`ai/procedure-foundation-model-lifecycle.md`](procedure-foundation-model-lifecycle.md); a change that alters the risk basis of an approval requires that approval to be re-granted, not carried.
3. The comparison result is recorded against the successor's registry entry ([`ai/register-model-registry.md`](register-model-registry.md)).
4. After cutover the successor is monitored on a defined cadence so a regression that the pre-cutover comparison did not surface is detected in operation.

A successor that fails the comparison does not assume standing; the predecessor is retained per the reversibility principle.

## 6. In-flight approvals and decisions

Approvals and decisions in progress at the transition moment are handled explicitly, never carried by default:

1. An approval granted to the predecessor and not yet acted on does not transfer to the successor; it is re-issued against the successor or explicitly confirmed to still hold, with the confirmation recorded.
2. A decision or action the predecessor had begun but not completed at cutover is either completed under the predecessor's retained standing or re-initiated under the successor; it is not silently continued by the successor as though it were the same subject.
3. Any automated approval or delegation that references the predecessor identity is updated to the successor identity or revoked; a dangling grant to a decommissioned predecessor is closed.

## 7. Access and delegation transition

Access and delegations move to the successor by re-issuance, not by inheritance:

1. Access the successor needs is granted to the successor's identity, scoped to the minimum the successor's task requires; the predecessor's access set is a reference, not a template to copy.
2. Delegations the successor is to hold are re-created as fresh delegation instruments naming the successor as grantee, per [`governance/standard-delegation-of-authority.md`](../governance/standard-delegation-of-authority.md); a delegation to the predecessor is revoked on the predecessor's decommissioning, and its revocation propagates.
3. On successful transition, the predecessor's access and delegations are revoked and the revocation is confirmed, so standing does not persist on a retired identity.

## 8. Framework alignment

The alignment below is analogical (each row aligns with or is informed by the cited reference) and at the control-family and category level, not a prescriptive crosswalk. Control identifiers are verified against the held source texts.

| Framework | Reference | Relevance |
| --- | --- | --- |
| CSA AICM v1.1.0 | MDS-03 Model Documentation; MDS-05 Model Documentation Validation | Documentation and validation evidence a successor presents for standing |
| CSA AICM v1.1.0 | MDS-08 Model Integrity Checks | The successor artefact is the validated artefact |
| CSA AICM v1.1.0 | MDS-10 Model Continuous Monitoring | Post-cutover monitoring for regressions the comparison did not surface |
| ISO/IEC 42001:2023 | §8.1 operational planning and control (AI system life cycle controls) | Governing the version-transition operation |
| NIST AI RMF | MAP; MANAGE | Framing the transition risk and managing it across the successor's operation |
| CSA CCM v4.1.0 | CCC-01 Change Management Policy and Procedures | The version transition as a governed change |
| CSA CCM v4.1.0 | IAM-05 Least Privilege | Access re-issued to the successor scoped to the minimum |
| ISO/IEC 27001:2022 | A.5.18 Access rights | Re-issuance and revocation of access across the transition |
| NIST SP 800-53 Rev. 5 | AC-2 Account Management | Managing the successor and predecessor identities and their access |

---

## 9. Limitations

This standard is a CC BY-SA 4.0 baseline. It states what a successor must satisfy to establish standing; the enforcing evaluation, validation, and access-provisioning mechanics live in the model lifecycle procedures, the access and agent-permissions standard, and the delegation standard. Model-platform and supplier practices for versioning and substitution vary, and adopting organizations adapt the evidence set and the comparison method to their model estate. The standard is not a substitute for per-model evaluation or for the risk reassessment the lifecycle procedure requires.

---

**End of Document**
