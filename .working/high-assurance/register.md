# High-Assurance Verification Register

**Version:** 1.0.3\
**Date:** 2026-06-30\
**License:** CC BY-SA 4.0

The durable, cross-session register for the **high-assurance verification** discipline (the
pack rule [`governance/high-assurance-verification.md`](../../dev-security/claude-rules/governance/high-assurance-verification.md)):
the heavier pre-apply harness invoked for *sensitive* changes, those that are gate-blind on
correctness, delicate at scale, and costly to get wrong. A sensitive change often spans more
than one session (the trigger is recognized in one, the harness runs across one or more, a
closing re-check falls in a later one), so its state must survive a session boundary; this
register is where it does.

Each row records one sensitive item: what it is and which of the three trigger conditions
make it sensitive, the harness stages run and their outcomes (research workers, the
independent adversarial verifier findings, the programmatic invariant checks, the
deterministic apply script and its re-parse result), the status, and any follow-up. New rows
on top.

**Status field**: `pending` (recognized, harness not yet run) / `in-progress` (harness
running, not yet complete) / `verified` (harness complete, retained for the audit trail) /
`deferred` (blocked on a maintainer decision or an external dependency, routed around).

**Resume surfacing**: on `/resume`, the assistant reads this register alongside the other
standing registers and surfaces every `pending`, `in-progress`, and `deferred` row before
starting the queued work, so an in-flight harness is not lost across a session boundary. A
`pending` or `in-progress` row is a standing instruction that the item is not yet cleared; it
is not silently dropped (the same discipline as the pending-decisions queue).

This file is maintainer working state, exempt from corpus audit gates.

## Active items

None currently in-flight (no `pending` / `in-progress` / `deferred` rows). The closing
whole-matrix `/matrix-fit` over the 62-row worklist (FR-167 closure, tracked in
[`TODO.md`](../../TODO.md)) is the next candidate that may warrant a register row when it
runs, if its findings touch sensitive cells.

## Completed items (retained for the audit trail)

| Date | Item | Why sensitive (conditions) | Harness stages and outcome | Status | Follow-up |
|---|---|---|---|---|---|
| 2026-06-30 | FR-34: author `privacy/template-transfer-impact-assessment.md` (Transfer Impact Assessment template, EDPB Rec 01/2020 / GDPR Chapter V, PR #483) | Maintainer-directed (net-new authoring goes through the harness). Two of three conditions hold strongly: (1) gate-blind correctness (accurate GDPR Chapter V operationalization, correct attribution of the not-held EDPB methodology, and not pinning an unverified SCC version are semantic properties no gate checks); (3) high cost (a citable, adopter-consumed transfer-compliance instrument). Condition (2) delicate-scale is weaker (a single new template). | (1) Authored against the held GDPR Chapter V full text (Arts 44 to 49); the EDPB Rec 01/2020 methodology is NOT held (attributed, own prose) and the SCCs/2021-914 are NOT held (referenced generically, no version pinned). (2/3) Two independent adversarial verifiers, blind to each other: Verifier B (false-positive) found **0 defects** (all Chapter V citations accurate; SCC version correctly not pinned; EDPB attributed not quoted; Schrems II as concept; TIA effect under-claimed); Verifier A (false-negative) found **0 error-level gaps** + 2 warning-level completeness improvements applied in-window (Art 46(2)(e)/(f) tool routes; Art 48 foreign-disclosure assessment). (4) Mechanical floor: all 57 gates green. (5) Single new file; the two improvements applied and re-verified against the held GDPR text. | verified | FR-74 residual (annex/procedure Schrems II deepening) and the TIA cross-reference wiring remain as separate TODO items, not harness-gated. |
| 2026-06-30 | FR-31: author `privacy/framework-privacy-by-design.md` (Privacy by Design Framework, GDPR Article 25, PR #482) | Maintainer-directed (net-new authoring goes through the harness). Two of three conditions hold strongly: (1) gate-blind correctness (whether GDPR Art 25 is accurately operationalized, whether the seven principles are correctly attributed vs over-claimed as law, and citation-edition accuracy are semantic properties no gate checks); (3) high cost (a citable, adopter-consumed privacy framework). Condition (2) delicate-scale is weaker (a single new framework doc, not a bulk reshape). | (1) Authored against the held GDPR full text (Art 25 + Recital 78). (2/3) Two independent adversarial verifiers, blind to each other: Verifier A (false-negative, completeness vs GDPR Art 25 + the consent-framework structural bar) and Verifier B (false-positive, every quote/citation vs ground truth + the canonical-citations register) **both independently caught the same real defect**: a hallucinated `ISO/IEC 29134:2023` citation (verifiable edition is 2017; a logged recurrence of #162/#167; gate-blind, 29134 absent from the canonical register), orchestrator-introduced and propagated to the register row. Fixed to `:2017` in both places pre-merge. All GDPR Art 25(1)/(2)/(3) quotes verbatim-accurate; Recital 78 correctly framed as encouraging (not binding) producers; the seven principles correctly attributed to Cavoukian (not over-claimed as legal force). (4) Mechanical floor: all 57 gates green on the fixed state. (5) Single new file; the 29134 fix applied in-window and re-verified. | verified | None. NB: the catch is the harness backstopping an ORCHESTRATOR-introduced hallucination (not a worker draft); logged in [`hallucination-metrics.md`](../hallucination-metrics.md) as a pre-merge catch. |
| 2026-06-30 | FR-32: author `privacy/template-legitimate-interest-assessment.md` (LIA template for GDPR Article 6(1)(f), PR #480) | Maintainer-directed (net-new authoring goes through the harness). Two of three default conditions hold strongly: (1) gate-blind correctness (whether each cited article/recital is the right authority and whether the three-part test is complete is a semantic/fit property no gate checks); (3) high cost (a citable, adopter-consumed privacy template; a misquote or a missing test-limb propagates). Condition (2) delicate-scale is weaker (a ~130-line single new file, not a bulk reshape). | (1) Authored against the held GDPR full text (`grc_library_scratch/ref/legislation/EU/GDPR-Regulation-2016-679--full-text.md`). (2/3) Two independent adversarial verifiers, blind to each other and to the authoring rationale: Verifier A (false-negative, required-but-missing content vs GDPR + the DPIA structural bar) found the doc substantively complete with **2 warning-level gaps** (compressed sign-off; no Article 21(4) prominence prompt); Verifier B (false-positive, every quote/citation vs the GDPR full text + the canonical-citations register) found **0 error-level defects** (all quotes verbatim, all citations registered/current, EDPB Guidelines 1/2024 correctly not cited). (4) Mechanical floor: all 57 audit gates green on the fixed state. (5) Single new file authored (not a scripted bulk apply); both warning gaps + the FP scope-precision note applied in-window and re-verified (57/57 green, orchestrator re-read). | verified | None; the template is a structural baseline (its Limitations section directs adopters to validate against their supervisory authority's guidance). |
| 2026-06-28 | FR-167: add the CSA AICM v1.1 column to the compliance matrix (PRs #447 gate, #448 data, #449 tool-scoping) | All three: (1) gate-blind fit (a control code can exist, be in the right catalogue, pass gate 49, and still be the wrong control for the row's document); (2) delicate scale (a 261-row single-artefact reshape across all 11 domain tables); (3) high cost (the matrix is a cited, adopter-consumed artefact) | (1) 5-worker research fan-out for the per-row candidates. (2) Mechanical AI-signal grep over the negatives. (3) Two independent adversarial verifiers: Verifier A (false-negative, re-read every title-based `N/A` document) caught **9 genuine misses**; Verifier B (false-positive, judged each assigned code against its AICM v1.1 title) tightened **3 over-assignments**. (4) Programmatic invariant: every code confirmed `is_aicm_only` (34/34); gate 49 validated the column. (5) Deterministic scripted apply (dry-run-validated, idempotent-guarded, keyed on a path-to-cell map) then re-parse of all 68 rendered cells against the verified map (0 mismatches). Guard-first: #447 gate landed before #448 data. | verified | Closing whole-matrix `/matrix-fit` over the 62-row worklist remains (FR-167 closure); semantic-fit assurance for this batch is recorded in [`matrix-fit/history.md`](matrix-fit/history.md). |
