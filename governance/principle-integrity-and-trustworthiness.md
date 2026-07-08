# Integrity and Trustworthiness Principle

**Document Title:** Integrity and Trustworthiness Principle\
**Document Type:** Principle\
**Version:** 0.0.1\
**Date:** 2026-07-08\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`dev-security/claude-rules/governance/project-integrity.md`](../dev-security/claude-rules/governance/project-integrity.md), [`governance/framework-continuous-assurance-and-improvement.md`](framework-continuous-assurance-and-improvement.md), [`governance/specification-audit-programme.md`](specification-audit-programme.md), [`ai/framework-ai-governance-and-risk.md`](../ai/framework-ai-governance-and-risk.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material governance, AI, or regulatory change\
**Repository Path:** [`governance/principle-integrity-and-trustworthiness.md`](principle-integrity-and-trustworthiness.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This document states the library's foundational production principle in citable, adopter-facing form: the **AIQT Principle**, the priority ordering **(Accuracy = Integrity = Quality = Trust) > Speed > Cost**. It is the corpus counterpart to the governance pack's apex rule ([`governance/project-integrity.md`](../dev-security/claude-rules/governance/project-integrity.md)): where the pack rule governs how the library is produced and maintained, this document explains the principle to a reader of the library and records, in source-verified form, how the four facets align with the trustworthiness vocabularies of the AI-assurance and general-assurance frameworks the corpus draws on.

The principle governs the integrity of the work product and its production process. It is distinct from, and complementary to, the AI-system trustworthiness the corpus's AI-governance documents address: those govern the behaviour of a deployed AI system; this governs whether the documentation and tooling the library ships are what they claim to be.

## Scope

Applies to every artefact the library produces (the governed documents, the audit tooling, the working-state records) and to every contributor, human or AI-assistant, who produces or maintains them. It is a principle, not a control: it fixes the priority ordering that resolves a conflict between the work's non-negotiable properties and the pressures of speed and cost, and it names the machinery that enforces each property. The enforcing controls live in the audit programme ([`governance/specification-audit-programme.md`](specification-audit-programme.md)) and the governance pack rules; this document does not restate them.

## 1. The principle

**(Accuracy = Integrity = Quality = Trust) > Speed > Cost.**

The four named properties form **one composite top tier** with no internal ranking; the tier is lexicographically above Speed, and Speed above Cost. Two readings are foreclosed:

- **AIQT is not an internal ranking.** Accuracy does not outrank Integrity, nor Quality Trust. The four are co-equal facets of one non-negotiable tier; a conflict *among* them is a framing defect to surface, not a priority call to make (an "accurate but fabricated" or "high-quality but dishonest" result does not exist; each facet's failure fails the tier).
- **"Lexicographic" applies between tiers.** A gain in speed never justifies any loss on the AIQT tier, however small the loss or large the gain. Cost is optimized only after both the AIQT tier and speed obligations are met. "Done faster" and "done cheaper" are never reasons for "done worse".

## 2. The four facets

Each facet is defined below with the machinery that enforces it. (Definitions are the pack apex rule's, verbatim in substance.)

### 2.1 Accuracy

Every factual claim matches its source, and every state assertion rests on an observation, not an inference. A citation names what the source actually says; a value attributed to a standard is one the standard states; a "done" reflects a verification that ran. Enforced by the evidence-grounded-completion discipline and, in the corpus, by the citation, currency, and control-code audit gates plus the semantic-precision cadences (`/matrix-fit`, `/claim-fit`, `/reference-audit`) layered above them.

### 2.2 Integrity

The work product is what it appears to be: no stubbed, mocked, hardcoded, or simulated results presented as finished work; no suppressed or weakened checks; no fabricated names, APIs, citations, or behaviour; no silent changes; failing states surfaced, never concealed. Enforced by the gate-discipline rule (a failing gate is fixed, never silenced) and the integrity non-negotiables of the apex rule.

### 2.3 Quality

The work meets the standard the project sets for craft: correct against requirements, consistent with the corpus's conventions, complete across every paired surface a change touches. Enforced by the audit programme and the per-change and periodic quality-assurance cadences (the validation sweeps and the tiered skeptical-verifier discipline).

### 2.4 Trust

Trust is **warranted by the record and granted by the maintainer**; it is never claimed by the producer. Every claim a reader relies on is traceable to evidence; every override of a verifier is logged with a revert path; every change carries its audit-trail entry; and when process integrity lapses, the recovery path runs to the maintainer's explicit sign-off, not the producer's self-assessment. Enforced by the change-tracking discipline, the override register, and the trust-recovery escalation tier.

## 3. Priority ordering and escalation

When the AIQT tier conflicts with speed or cost, the higher tier wins outright: there is no blended score, no "good enough given the time". If any constraint forces a compromise on the AIQT tier, the producer halts and escalates the tradeoff to the maintainer explicitly, naming which facet is at risk and what pressure forces the question, rather than resolving it silently in favour of speed or cost. A one-sentence escalation at the moment of conflict is cheap; an unwound body of work built on a silently-chosen compromise is expensive.

## 4. Framework alignment

The four facets align, at the concept level, with the trustworthiness vocabularies of the AI-assurance frameworks the corpus holds and cites. The alignment is **many-to-many and analogical, not a prescriptive crosswalk**: several facets draw on the same source construct, and the AI-assurance frameworks govern the trustworthiness of a deployed AI system's *outputs*, whereas the AIQT facets govern the integrity of a *work product and its production*. Each row below is "aligns with / is informed by", never "is prescribed by". The AI-assurance mappings are verified against the held source texts (NIST AI RMF 1.0 / AI 100-1; ISO/IEC 42001:2023; ISO/IEC TR 24028:2020); the general-framework column records the corpus's own established alignment (see the pack rules' framework-alignment tables) and is not a per-source-text claim.

| AIQT facet | NIST AI RMF 1.0 characteristic | ISO/IEC 42001:2023 | ISO/IEC TR 24028:2020 | General assurance (corpus convention) |
|---|---|---|---|---|
| **Accuracy** | Valid and Reliable (the "accuracy"/validation measure) | A.6.2.4 verification and validation; A.7.4 data quality | §5.3 integrity attributes (accuracy, consistency); verification (3.47) | NIST SSDF RV.1/RV.2; CSA CCM GRC-05, LOG-02; ISO/IEC 27001 A.5.36, A.8.15 |
| **Integrity** | (no direct characteristic; nearest is Accountable and Transparent, via disclosure and non-concealment) | A.8 information for interested parties; A.6.2.8 event-log record-keeping | §5.3 integrity ("respect of sound moral and ethical principles; information will not be manipulated in a malicious way") | NIST SSDF PW.7, RV.1; CSA CCM GRC-05, A&A-04; ISO/IEC 27001 A.5.36, A.8.34 |
| **Quality** | Valid and Reliable (reliability, robustness) | A.6.2.2 requirements; A.6.2.3 design documentation; A.7.4 data quality | quality named as a trustworthiness characteristic (points to the SQuaRE series) | NIST SSDF PO.1, PO.5; CSA CCM GRC-01, GRC-04; ISO/IEC 27001 A.5.1, A.5.4 |
| **Trust** | Accountable and Transparent ("trustworthy AI depends upon accountability; accountability presupposes transparency") | A.3 accountability; A.5 impact-assessment documentation; A.10.2 responsibility allocation | trust (3.41), trustworthiness as verifiability (3.42), accountability as traceability (3.1) | NIST SSDF PS.1, RV.2; CSA CCM LOG-02, LOG-08, GRC-04; ISO/IEC 27001 A.8.15, A.5.36 |

**Alignment caveats (deliberate, source-verified):**
- **Accuracy** aligns with the NIST *Valid and Reliable* characteristic only at the concept level: the RMF's "accuracy" measures an AI system's output closeness to true values (a model-performance property), whereas the AIQT Accuracy facet is claim-to-source fidelity in produced work. The shared idea is "correctness confirmed through objective evidence". ISO/IEC TR 24028 §5.3 (which lists accuracy and consistency among the attributes of integrity) is the stronger held-text anchor.
- **Integrity** has **no direct NIST AI RMF characteristic**: the RMF has no work-product-honesty property. The nearest is *Accountable and Transparent* (via disclosure and non-concealment), an analogy, not a match. The precise held-text anchor is ISO/IEC TR 24028 **§5.3** ("respect of sound moral and ethical principles"), NOT the standard's clause-3.21 "integrity" (which is the confidentiality-integrity-availability sense, a false friend for this facet).
- **Quality** is native to ISO/IEC 42001 (a management-system standard: requirements, design documentation, data quality) but only *listed*, not defined, in ISO/IEC TR 24028; treat 42001 as the primary anchor and TR 24028 as corroborating.
- The NIST AI RMF characteristics not mapped (Safe; Secure and Resilient; Explainable and Interpretable; Privacy-Enhanced; Fair with Harmful Bias Managed) address AI-system output risk, outside the AIQT facets' scope (the integrity of the work product and its production), and are deliberately not force-fit.

## 5. Adoption guidance

An adopter reusing this library inherits the AIQT ordering as the tiebreaker for their own production of governed content. To operationalize it: fix the ordering once, at the highest precedence, so it is not re-litigated under deadline pressure; name, for each facet, the specific machinery (gates, reviews, audit trail) that enforces it in your environment; and make escalation, not silent compromise, the sanctioned response when a constraint pressures the tier. The pack rule [`governance/project-integrity.md`](../dev-security/claude-rules/governance/project-integrity.md) is the project-agnostic distributable form; this document is the corpus's citable statement of the same principle with its framework alignment.

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO/IEC 27001 | NIST AI RMF 1.0 | ISO/IEC 42001:2023 |
| --- | --- | --- | --- | --- | --- |
| Quality prioritized over schedule and cost | PO.1, PO.5 | GRC-01, GRC-04 | A.5.1, A.5.4 | Valid and Reliable | A.6.2.2 |
| Integrity of work product (no fabrication, no suppression) | PW.7, RV.1 | GRC-05, A&A-04 | A.5.36, A.8.34 | Accountable and Transparent | A.8 |
| Evidence-grounded accuracy | RV.1, RV.2 | GRC-05, LOG-02 | A.5.36, A.8.15 | Valid and Reliable | A.6.2.4 |
| Trust warranted by an audit trail and authority-gated closure | PS.1, RV.2 | LOG-02, LOG-08, GRC-04 | A.8.15, A.5.36 | Accountable and Transparent | A.3, A.5 |

This principle document carries the AI-assurance mappings the pack apex rule refers to but deliberately does not restate; the AI-assurance columns are verified against the held source texts, the general columns against the corpus's established framework alignment.
