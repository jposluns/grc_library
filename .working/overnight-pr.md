<!-- OVERNIGHT-PR-STUB -->
# Overnight PR

**Status:** stub

No overnight session is in flight. This file is the durable handoff record for a
maintainer-authorized autonomous overnight session: when one is active its `Status`
is `in-flight` and it carries the session's authorization scope, design decisions,
build progress, and surfaced ambiguities. When a session ends, the next-morning
processing routes its content to the durable ledgers (design decisions →
[`design-decisions.md`](design-decisions.md); closed work → [`DONE.md`](DONE.md);
queued follow-ups and deferred decisions → [`../TODO.md`](../TODO.md)) and resets this
file to `stub`. Audit gate 46 enforces the lifecycle: it fails on `Status: done`
(session ended but morning processing missing) and passes on `stub` / `in-flight`.

Last run: the 2026-06-23 overnight run (PRs #259-#268), paused after FR-141 on a
quality-first / degradation basis and closed out via handoff PR #268. Its morning
processing completed 2026-06-23: the 8 resolved design decisions were already recorded
in [`design-decisions.md`](design-decisions.md); the 9 deferred "Open ambiguities"
were routed to [`../TODO.md`](../TODO.md) as the `DD-1`..`DD-9` deferred-decisions
block (need maintainer triage); this file reset to `stub`.
