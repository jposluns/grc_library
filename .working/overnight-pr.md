# Overnight PR

**Status:** in-flight

This file is the durable handoff record for a maintainer-authorized autonomous overnight
session. It is `stub` when no overnight session is in flight (the default state).

Lifecycle (audit gate 46 enforces it: passes on `stub` and `in-flight`, fails on `done`):

- `stub`: no overnight session in flight. This file holds only this protocol description and the `Status: stub` line.
- `in-flight`: an overnight session is active. The assistant fills the file with the authorization scope, design decisions made, files being authored or modified, build progress, and open ambiguities. Each overnight PR ships `in-flight`.
- `done`: the session ended. The next-morning processing PR routes the content to the durable ledgers (design decisions to [`design-decisions.md`](design-decisions.md), closed work to [`DONE.md`](DONE.md), queued follow-ups to [`../TODO.md`](../TODO.md)) and resets this file to `stub`.

## 2026-07-02 overnight session (authorized before maintainer sleep; runs until morning)

**Authorization scope (locked via one-by-one maintainer Q&A, then "go" and the explicit overnight-mode directive "You are in overnight mode until the morning. No more actions that require my input, any such are deferred to the morning"):**

- Green CI = merge authority, with the FULL per-PR cadence (no abbreviation): preflight-changelog, per-commit audits, pre-push guard, `/validate-pr` + `/retro` batched per recursion-avoidance, TODO/DONE rotation, handoff refresh.
- Four pre-approved change tiers: (1) defect fixes; (2) new gates plus gate policy; (3) pack design changes; (4) scratch `validate.py` upgrades (via MCP PR to `grc_library_scratch`).
- Sequence interleaved by risk: guardrail-enabler wave first, then corpus P1 fixes, then remaining machinery, pack design last. Plan of record: the approved overnight execution plan (session artefact) plus the Sweep-82-first resume protocol.
- The full `-ize`/`-ization` normalization INCLUDING the `organisation` family (~1026 occurrences) is authorized via the high-assurance harness (this resolves TODO section 7.4: harmonize, not sanction-the-exception).
- EPUBs: untrack going forward and queue history-purge instructions; the purge itself is maintainer-executed only (this resolves TODO section 7.5's direction; the decision record lands when that PR ships).
- Conflicts: stricter-safe with wide latitude (the canonical / register-supported value wins without deferring), each such resolution logged in [`pending-decisions.md`](pending-decisions.md) as "proceeded (stricter-safe); confirm or redirect on resume".
- Stop condition: queue exhaustion OR a named degradation signal, then a closing-handoff PR and a morning report in chat.

**Deferred to morning regardless of the above:** the advisory-directive codification PR (drafted, one-approval item in [`pending-decisions.md`](pending-decisions.md)); EPUB history-purge execution; stale-branch deletion; anything hitting the 3-iteration verifier cap; the ANPD item if upstream is unverifiable; any behaviour change to `.claude/CLAUDE.md` or pack rules beyond the pre-approved tiers (factual fixes within the tiers are logged per-touch).

**Progress ledger (updated as PRs land; the per-PR narrative is CHANGELOG + [`DONE.md`](DONE.md)):**

- PR 1 (#553, merged): Sweep 82 close-out (3 in-window bookkeeping findings fixed, detail file + history row), the resume-protocol handoff prune, and this file's transition stub to in-flight.
- PR 2 (#554, merged): the guardrail-review TODO intake (new sections 3.15 and 4.7, every claim re-verified at source, one lens claim refuted and dropped), the batched #553 QA rows (`/validate-pr` 2 warnings + 1 note, `/retro`), and the three #553 finding fixes (the third SR-5 carrier at the handoff State-snapshot line, the false zero-residuals claim corrected via dated addendum + correction note, the stale stub-imperative in the handoff Operating-mode line).
- PR 3 (#555): W2 / GR-2: nineteen regression tests for the D1/D2/D3/D5 delta checks and the pre-push-guard exit-code chain (suite 228 to 247; GR-2 rotated to DONE, GR-13 added from a verifier observation), the GR-P5 clause precision fix from the #554 `/validate-pr` (its out-of-window CLAUDE.md wrong-trio catch routed into GR-P5, protected file untouched), and the batched #554 QA rows.

**Open ambiguities:** none yet; anything surfacing mid-run is logged here plus [`pending-decisions.md`](pending-decisions.md) under the graceful-degradation rule.
