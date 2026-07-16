# Overnight PR

**Status:** stub

This file is the durable handoff record for a maintainer-authorized autonomous overnight
session. It is `stub` when no overnight session is in flight (the default state).

Lifecycle (audit gate 46 enforces it: passes on `stub` and `in-flight`, fails on `done`):

- `stub`: no overnight session in flight. This file holds only this protocol description, the `Status: stub` line, and (after a routed run) a short closure note recording where the last run's content went.
- `in-flight`: an overnight session is active. The assistant fills the file with the authorization scope, design decisions made, files being authored or modified, build progress, and open ambiguities. Each overnight PR ships `in-flight`.
- `done`: the session ended. The next-morning processing PR routes the content to the durable ledgers (design decisions to [`design-decisions.md`](design-decisions.md), closed work to [`DONE.md`](DONE.md), queued follow-ups to [`../TODO.md`](../TODO.md)) and resets this file to `stub`.

<!-- OVERNIGHT-PR-STUB -->

## Last run closure note: reset at the 2026-07-16 session-closing handoff

This file had been left `in-flight` since a 2026-07-15 overnight run (merged #929-#936: the TODO permanent-numbering framework, the massive-item TODO-split wave, and several gate/tooling and staged-protected items) that held in overnight mode and was never routed by the subsequent 2026-07-15 sessions (the #943-#953 website session and the #955-#963 session). Its content was pure build-progress narrative; the #929-#936 work is durably recorded per-PR in [`DONE.md`](DONE.md) and [`CHANGELOG.md`](../CHANGELOG.md), and no un-routed design decision remained (the design decisions of that run were recorded in-run). The build-progress noise is discarded per the protocol; this file is reset to `stub`.

The 2026-07-16 resumed session (which merged #964-#967 plus scratch #166-#170 and built the credit-offload system) ran its overnight window tracked via [`session-state.md`](session-state.md) and the per-PR records, NOT this file, so there is no separate content to route from it; its state is captured in the session handoff and the CHANGELOG. This reset is the mode-exit "route and reset overnight-pr.md" cleanup for that session's wind-down.

<!-- OVERNIGHT-PR-STUB -->
