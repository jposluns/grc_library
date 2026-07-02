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

- PR 1 (this PR): Sweep 82 close-out (3 in-window bookkeeping findings fixed, detail file + history row), the resume-protocol handoff prune, and this file's transition stub to in-flight.

**Open ambiguities:** none yet; anything surfacing mid-run is logged here plus [`pending-decisions.md`](pending-decisions.md) under the graceful-degradation rule.
