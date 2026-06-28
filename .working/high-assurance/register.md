# High-Assurance Verification Register

**Version:** 1.0.0\
**Date:** 2026-06-28\
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
| 2026-06-28 | FR-167: add the CSA AICM v1.1 column to the compliance matrix (PRs #447 gate, #448 data, #449 tool-scoping) | All three: (1) gate-blind fit (a control code can exist, be in the right catalogue, pass gate 49, and still be the wrong control for the row's document); (2) delicate scale (a 261-row single-artefact reshape across all 11 domain tables); (3) high cost (the matrix is a cited, adopter-consumed artefact) | (1) 5-worker research fan-out for the per-row candidates. (2) Mechanical AI-signal grep over the negatives. (3) Two independent adversarial verifiers: Verifier A (false-negative, re-read every title-based `N/A` document) caught **9 genuine misses**; Verifier B (false-positive, judged each assigned code against its AICM v1.1 title) tightened **3 over-assignments**. (4) Programmatic invariant: every code confirmed `is_aicm_only` (34/34); gate 49 validated the column. (5) Deterministic scripted apply (dry-run-validated, idempotent-guarded, keyed on a path-to-cell map) then re-parse of all 68 rendered cells against the verified map (0 mismatches). Guard-first: #447 gate landed before #448 data. | verified | Closing whole-matrix `/matrix-fit` over the 62-row worklist remains (FR-167 closure); semantic-fit assurance for this batch is recorded in [`matrix-fit/history.md`](matrix-fit/history.md). |
