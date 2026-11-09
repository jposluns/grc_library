# When a release-signing key is compromised after software reaches production

**Document Title:** When a release-signing key is compromised after software reaches production\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-08-17\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`dev-security/standard-devops-security-requirements.md`](../../dev-security/standard-devops-security-requirements.md), [`security/framework-cryptographic-key-lifecycle.md`](../../security/framework-cryptographic-key-lifecycle.md), [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/scenarios/scenario-release-signing-key-compromise.md`](scenario-release-signing-key-compromise.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Scenario\
**Narrative Status:** Non-normative\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`dev-security/standard-devops-security-requirements.md`](../../dev-security/standard-devops-security-requirements.md), [`operations/procedure-release-management.md`](../../operations/procedure-release-management.md), [`security/framework-cryptographic-key-lifecycle.md`](../../security/framework-cryptographic-key-lifecycle.md), [`security/procedure-cryptographic-key-operations.md`](../../security/procedure-cryptographic-key-operations.md), [`security/procedure-key-escrow-and-recovery.md`](../../security/procedure-key-escrow-and-recovery.md), [`operations/standard-certificate-authority-management.md`](../../operations/standard-certificate-authority-management.md), [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-016\
**Last Reviewed:** 2026-08-17

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Scenario premise

This scenario is a composite illustration. It describes no identifiable organization, no actual system or key, and no real incident, and it makes no claim about how likely such an event is.

An organization ships software to production through a governed release process. Each release is packaged, signed, and verified before deployment, and every verification passes. Some time after a routine release, a security review surfaces something that has nothing to do with any artefact: records suggesting that the private key used to sign production releases may have been accessible outside its approved custody, over a period that spans several releases. Nothing has visibly failed. Every signature still verifies. What has failed is the assumption behind the signatures: that only the organization could have made them.

The reason this is a leadership event, not only a technical one, sits in the corpus. The [DevOps Security Requirements Standard](../../dev-security/standard-devops-security-requirements.md) makes signing and signature verification the integrity control for production artefacts (its section 2.6), so the trust the organization places in its production estate runs, in part, through this one piece of key material. Leadership now holds three questions at once: which artefacts relied on this key, on whose authority further reliance is paused or continued, and which recovery route is authorized and leaves a trace.

## How the event unfolds

**Trust is questioned.** The report concerns the key, not the software. The [Cryptographic Key Operations Procedure](../../security/procedure-cryptographic-key-operations.md) treats a suspected key compromise as a security incident (its section 8), so the event enters the [Security Incident Response Procedure](../../security/procedure-security-incident-response.md) through detection and triage (its section 4). The first factual questions about the key resolve against the Key Lifecycle Register that the [Cryptographic Key Lifecycle Management Framework](../../security/framework-cryptographic-key-lifecycle.md) requires every key to be registered in (its section 3). That register entry is a dependency of scoping the incident: without it, the organization cannot connect the suspect key to the systems and releases that relied on it. The register's fields stay in the framework.

**Release reliance is paused.** A signature that verifies is evidence that an artefact matches what the key signed. It is not evidence that the key was in trusted hands when the signature was made. That distinction is what the first decision turns on: whether the organization keeps relying on this key's signatures while the investigation runs. The corpus places that decision in named routes rather than in a fixed answer: the [Release Management Procedure](../../operations/procedure-release-management.md) owns the rollback or forward-fix decision (its Step 8), and the [key operations procedure](../../security/procedure-cryptographic-key-operations.md) owns revocation and its triggers (its section 6). Which action applies is a finding of fact for the incident authority under the incident procedure; this page prescribes no universal technical response.

**Affected artefacts are traced.** Management now needs the population: which releases carry this key's signature, and over what period. The [Release Management Procedure](../../operations/procedure-release-management.md) closes each release with a release record (its Step 9); what that record holds stays in the procedure. Where the signing identity is certificate-based, the [Certificate Authority Management Standard](../../operations/standard-certificate-authority-management.md) bounds what internal code-signing certificates may be trusted for (its section 6.3) and routes CA operations into the CA audit log (its section 11). Whether these record sets connect, so that the key record can be walked to every release that relied on the key and back, is a composite test this scenario poses across the two sources: the corpus establishes each record separately, and no single corpus document states that the join is present in every organization. The join is a dependency of a complete impact answer, and asking for it is the oversight action this page equips.

**Key disposition is decided.** The key itself needs a disposition. Revocation and compromise response belong to the [key operations procedure](../../security/procedure-cryptographic-key-operations.md) (its sections 6 and 8). Where the key falls in the strictest category of the [Key Escrow and Recovery Procedure](../../security/procedure-key-escrow-and-recovery.md), the member its key-categories section names Category 3: Root and signing keys (its Section 1), any recovery of the key runs through the documented recovery ceremony its Section 5 defines, and the procedure records where rotation is preferred to recovery. The disposition also reaches past the key: the procedure's Category 3 escrow section records the consequence a rotation carries for artefacts signed by the prior key. The triggers, approvals, ceremony steps, and that consequence live in the procedure; this page points to them and does not restate them.

**Production recovers.** Recovery is two threads that close together. The release thread runs under the [Release Management Procedure](../../operations/procedure-release-management.md): rollback or forward-fix where a release cannot stand (its Step 8), and closure with a recorded outcome (its Step 9). The incident thread runs under the [Security Incident Response Procedure](../../security/procedure-security-incident-response.md): containment through recovery (its section 5), evidence handling (its section 8), and the post-incident review (its section 7). What recovery looks like in practice, re-signing rebuilt artefacts under a successor key, rolling back, or fixing forward, depends on the facts of the event; the sequencing, sign-offs, and validation belong to those procedures, not to this page.

## Where the corpus controls engage

- **Artefact trust.** The [DevOps Security Requirements Standard](../../dev-security/standard-devops-security-requirements.md) makes a verified signature a condition of production deployment (its section 2.6): a prevention against deploying an artefact whose integrity cannot be checked, and the reason a signing key is part of the production trust decision at all. The [Release Management Procedure](../../operations/procedure-release-management.md) places signing and signature verifiability in build and packaging (its Step 2).
- **Key governance.** The [Cryptographic Key Lifecycle Management Framework](../../security/framework-cryptographic-key-lifecycle.md) defines the key lifecycle (its section 1) and requires registration in the Key Lifecycle Register (its section 3); the register is a dependency of locating the key and scoping what relied on it. The [key operations procedure](../../security/procedure-cryptographic-key-operations.md) owns revocation and compromise response (its sections 6 and 8), and the [escrow and recovery procedure](../../security/procedure-key-escrow-and-recovery.md) names the Category 3: Root and signing keys member (its Section 1) and owns that category's recovery ceremony (its Section 5).
- **Incident and recovery governance.** The [Security Incident Response Procedure](../../security/procedure-security-incident-response.md) owns detection and triage, containment through recovery, the post-incident review, and evidence requirements (its sections 4, 5, 7, and 8). The [Release Management Procedure](../../operations/procedure-release-management.md) owns the release-side recovery choice and closure (its Steps 8 and 9).
- **Audit trace.** The CA audit log the [Certificate Authority Management Standard](../../operations/standard-certificate-authority-management.md) requires (its section 11) and the closed release record (the [release procedure](../../operations/procedure-release-management.md), its Step 9) are evidence for the trace the impact assessment walks.

## What good looks like

The following reading is a composite of the sources above; see the limitations. It describes an evidence state to inspect, not a response checklist.

In a well-prepared organization, the suspect key already has a current entry in the Key Lifecycle Register, with an accountable owner recorded, before anyone needs it ([key lifecycle framework](../../security/framework-cryptographic-key-lifecycle.md), its section 3). Affected releases resolve to closed release records ([release procedure](../../operations/procedure-release-management.md), its Step 9), and the two record sets can be walked in both directions, from the key to the releases that relied on it and from a release back to its signing identity; that traceability statement is composite, and testing it is the point. The disposition of the key follows the named corpus routes, the [key operations procedure](../../security/procedure-cryptographic-key-operations.md) for revocation and compromise response and, where the strict category applies, the [escrow procedure](../../security/procedure-key-escrow-and-recovery.md)'s recovery ceremony, under the incident authority the [incident procedure](../../security/procedure-security-incident-response.md) establishes, rather than an improvised path. And every recovery decision leaves a record that can be produced afterwards: the incident record, the release record, the ceremony record where that route applied, and the CA audit log where the signing identity is certificate-based.

One caution belongs in the reading: a signature that verifies is not, by itself, evidence that the key remained in approved custody. The key-governance records above are evidence for custody assurance, not the artefact. Depicting these controls here is not evidence that they operate in any particular organization; the evidence classes below are how a governing body tests whether they do.

## Evidence to request

Each item below is an evidence class the governing body can call for from management, and each is evidence for a named control or outcome.

- **The Key Lifecycle Register record for the affected key**, as evidence for the registration control in the [Cryptographic Key Lifecycle Management Framework](../../security/framework-cryptographic-key-lifecycle.md) (its section 3).
- **The release records for the affected period**, as evidence for the release-closure control in the [Release Management Procedure](../../operations/procedure-release-management.md) (its Step 9).
- **The signature-verification record for the affected deployments**, as evidence for the artefact-integrity control in the [DevOps Security Requirements Standard](../../dev-security/standard-devops-security-requirements.md) (its section 2.6) and the signing and verifiability step in the [release procedure](../../operations/procedure-release-management.md) (its Step 2).
- **The CA audit-log extract for the signing identity, where it is certificate-based**, as evidence for the CA audit-logging control in the [Certificate Authority Management Standard](../../operations/standard-certificate-authority-management.md) (its section 11).
- **The incident record and its triage**, as evidence for the detection and triage controls in the [Security Incident Response Procedure](../../security/procedure-security-incident-response.md) (its section 4).
- **The key-disposition decision record**, as evidence for the revocation and compromise-response controls in the [Cryptographic Key Operations Procedure](../../security/procedure-cryptographic-key-operations.md) (its sections 6 and 8).
- **The recovery-ceremony record, where the Category 3 route applied**, as evidence for the recovery-ceremony control in the [Key Escrow and Recovery Procedure](../../security/procedure-key-escrow-and-recovery.md) (its Section 5).
- **The recovery validation and sign-off record**, as evidence for the recovery controls in the [incident procedure](../../security/procedure-security-incident-response.md) (its section 5) and the rollback or forward-fix step in the [release procedure](../../operations/procedure-release-management.md) (its Step 8).
- **The post-incident review**, as evidence for the learning control in the [incident procedure](../../security/procedure-security-incident-response.md) (its section 7).

## Limitations

- This scenario is illustrative and composite. It depicts no identifiable organization, no actual system, key, or certificate, and no real incident.
- This page makes no likelihood, frequency, or statistical claim, and none of its statements should be read as a probability, a frequency, or a magnitude.
- The compromise mechanism depicted, key material that may have been accessible outside approved custody, is this page's construction for the telling. It is not a corpus statement about how such events arise, and this page makes no claim about which mechanisms occur in practice.
- This page does not determine the disposition. Whether revocation, rotation, recovery, rollback, forward-fix, or another action applies in a given event is decided through the linked corpus routes and the incident authority they establish, on the facts of that event.
- This page creates no compliance and imposes no requirement. The linked corpus documents govern; where this page differs from a corpus document, the corpus document prevails.
- This page carries composite claims. The premise, the sequencing of the event across the release, key-management, and incident sources, the release-to-key traceability test, and the description of a well-prepared evidence state are synthesized across the listed sources; no single corpus document states them, and the adopting organization validates the reading against its own release and key-management architecture.
- The corpus documents this page points to carry the specific values and closed sets: the artefact-integrity requirement wording, the release-step activities and outputs, the key lifecycle phases and rotation cadences, the register fields, the revocation triggers, actions, and timing, the key categories and recovery triggers, the escrow architecture and ceremony steps, the code-signing certificate constraints, the audit-log contents and retention, the incident severities, containment phases, review deadlines, and evidence requirements. This page routes to them and does not reproduce them.

**End of Document**
