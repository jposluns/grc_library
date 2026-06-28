# Overnight PR

**Status:** in-flight

## Active overnight session (2026-06-28, guard-rails-prompts resume)

**Authorization (maintainer 2026-06-28).** After merging the guard-rail rule PR #423, the maintainer directed: enter overnight mode and continue this session with PR-E (the reverted FR-178/194/199 work), then the P3-batch-in-one-fan-out test, then a session-closing handoff. Maintainer reachable for a short period. Attended-autonomous green-CI = merge authority; stricter-is-safer on conflicts; surface genuinely-authorial irreversible decisions rather than guess.

**Done / in flight this session.**
- #423 (merged): the eleventh governance rule `surface-counterproductive-instructions` + the #422 fold-in + Sweep 69 (1 Low, fixed).
- PR-E (#424, this PR): FR-178 (both policies fully to "must", maintainer Option B; replace-all verified safe, 31 + 23 occurrences), FR-194 (ELT glossary row), FR-199 (two soft-law register cells to "Original (no later revision)"; the "do not fabricate 1.0" catch honored). Every value re-verified against live files before applying.

**Next.** After PR-E merges, re-assess degradation at that boundary (wind-down framework) before the P3-batch test; then the session-closing handoff, which resets this file to `stub`.

**Open ambiguities.** None blocking.

This file is the durable handoff record for a maintainer-authorized autonomous overnight
session. It is `stub` when no overnight session is in flight (the default state).

Lifecycle (audit gate 46 enforces it: passes on `stub` and `in-flight`, fails on `done`):

- `stub`: no overnight session in flight. This file holds only this protocol description and the `Status: stub` line.
- `in-flight`: an overnight session is active. The assistant fills the file with the authorization scope, design decisions made, files being authored or modified, build progress, and open ambiguities. Each overnight PR ships `in-flight`.
- `done`: the session ended. The next-morning processing PR routes the content to the durable ledgers (design decisions to [`design-decisions.md`](design-decisions.md), closed work to [`DONE.md`](DONE.md), queued follow-ups to [`../TODO.md`](../TODO.md)) and resets this file to `stub`.

The 2026-06-27 overnight FR-167 run (batches 7-9 plus the directive-tasks interlude) was ended by maintainer direction ("End overnight mode") and morning-processed in the trust-recovery remediation PR: its durable design-decision content was routed to [`design-decisions.md`](design-decisions.md), its closed follow-up (the source-document framework-table code cleanup) to [`DONE.md`](DONE.md), and this file was reset to `stub`. The standing operating mode returns to attended-autonomous.
