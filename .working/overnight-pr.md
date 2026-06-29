<!-- OVERNIGHT-PR-STUB -->
# Overnight PR

**Status:** stub

This file is the durable handoff record for a maintainer-authorized autonomous overnight
session. It is `stub` when no overnight session is in flight (the default state).

Lifecycle (audit gate 46 enforces it: passes on `stub` and `in-flight`, fails on `done`):

- `stub`: no overnight session in flight. This file holds only this protocol description and the `Status: stub` line.
- `in-flight`: an overnight session is active. The assistant fills the file with the authorization scope, design decisions made, files being authored or modified, build progress, and open ambiguities. Each overnight PR ships `in-flight`.
- `done`: the session ended. The next-morning processing PR routes the content to the durable ledgers (design decisions to [`design-decisions.md`](design-decisions.md), closed work to [`DONE.md`](DONE.md), queued follow-ups to [`../TODO.md`](../TODO.md)) and resets this file to `stub`.

No overnight session is in flight. The 2026-06-28 overnight run (PRs #451 through #463) ended when the maintainer returned to **unattended (attended-autonomous) mode** on 2026-06-29 and directed wind-down after PR #463; per the overnight protocol's awake-early exception this file was transitioned `in-flight` -> `stub` directly (its content was already captured durably: the per-PR progress in `CHANGELOG.md` / [`DONE.md`](DONE.md) / git history, the four maintainer-resolved directives in [`pending-decisions.md`](pending-decisions.md)'s "Resolved overnight directives" section, and the forward queue in [`../TODO.md`](../TODO.md) §4.5 and [`session-handoff.md`](session-handoff.md)). The durable content of those directives (net-new content gets the high-assurance harness; the FR-59/61/62 download-attempt-then-defer rule; the in/out scope list; ISO Annex A titles are usable) remains a standing decision in `pending-decisions.md`; only the overnight-specific "no-answer maintains overnight" framing lapses with the return to attended mode.
