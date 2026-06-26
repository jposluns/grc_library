<!-- OVERNIGHT-PR-STUB -->
# Overnight PR

**Status:** stub

No overnight session is in flight. This file is the durable handoff record for a
maintainer-authorized autonomous overnight session: when one is active its `Status`
is `in-flight` and it carries the session's authorization scope, design decisions,
build progress, and surfaced ambiguities. When a session ends, the next-morning
processing routes its content to the durable ledgers (design decisions to
[`design-decisions.md`](design-decisions.md); closed work to [`DONE.md`](DONE.md);
queued follow-ups and deferred decisions to [`../TODO.md`](../TODO.md)) and resets this
file to `stub`. Audit gate 46 enforces the lifecycle: it fails on `Status: done`
(session ended but morning processing missing) and passes on `stub` / `in-flight`.

Last run: the 2026-06-26 integrity-tooling run (maintainer awake then asleep, "plan the
next 20 PRs"). It shipped #352 (pack em-dash convention conformance) and #353 (the bulk
`.working/` em-dash conformance apply plus the Sweep 49 / #352-QA bookkeeping), then wound
down on maintainer direction ("we can end and resume") before the Tier-1 prose-hygiene gate
(#354 in the 20-PR plan) was wired into all four surfaces. Content routed: the 20-PR plan
and the Tier-1-gate design are captured in [`session-handoff.md`](session-handoff.md)'s
next-actions queue; the `.working/`-standardization-as-regular-activity and
hallucination-metrics-refresh-at-wind-down disciplines and the Version-Date co-bump-check
candidate are queued (TODO §4.17 plus the handoff); no design decision was left unrouted.
This file reset to `stub` by the session-closing handoff PR.
