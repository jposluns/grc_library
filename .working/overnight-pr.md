# Overnight PR

**Status:** stub

This file is the durable handoff record for a maintainer-authorized autonomous overnight
session. It is `stub` when no overnight session is in flight (the default state).

Lifecycle (audit gate 46 enforces it: passes on `stub` and `in-flight`, fails on `done`):

- `stub`: no overnight session in flight. This file holds only this protocol description and the `Status: stub` line.
- `in-flight`: an overnight session is active. The assistant fills the file with the authorization scope, design decisions made, files being authored or modified, build progress, and open ambiguities. Each overnight PR ships `in-flight`.
- `done`: the session ended. The next-morning processing PR routes the content to the durable ledgers (design decisions to [`design-decisions.md`](design-decisions.md), closed work to [`DONE.md`](DONE.md), queued follow-ups to [`../TODO.md`](../TODO.md)) and resets this file to `stub`.

The 2026-06-28 overnight run (the guard-rails-prompts resume: the PR-E rebuild of the reverted FR-178/194/199 work, shipped as #424) was ended at the post-#424 wind-down boundary, where the `AskUserQuestion` flaked and the framework's no-answer timeout defaulted to handoff. All of its work landed in #423 and #424; the P3-batch-in-one-fan-out test it was authorized to attempt was deferred to a fresh session per the wind-down default. The session-closing handoff PR reset this file to `stub` directly (the exception path: `in-flight` to `stub` when the content has been processed). The standing operating mode returns to attended-autonomous.

The 2026-06-27 overnight FR-167 run (batches 7-9 plus the directive-tasks interlude) was ended by maintainer direction ("End overnight mode") and morning-processed in the trust-recovery remediation PR: its durable design-decision content was routed to [`design-decisions.md`](design-decisions.md), its closed follow-up (the source-document framework-table code cleanup) to [`DONE.md`](DONE.md), and this file was reset to `stub`. The standing operating mode returns to attended-autonomous.
