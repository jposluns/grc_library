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

Last run: the 2026-06-25 multi-session overnight run, authorized green-CI = merge
through the P1/P2 backlog with the priority order multi-session capability first, then
FR-167, then the decided content items. It ran across several `/resume` sessions and
shipped the multi-session / multi-worker capability (the runbook in #330, the light SOP
in #332, the pre-push-runner gate in #333, and gate 50 bookkeeping-parity in #343, with
the first `/guardrails` coherence review in #344), the project-governance separation
Phase 1 migration (#336), FR-167 batch 4 (the supply-chain matrix section, #341), the
Philip Veilleux AUTHORS addition (#335), and the per-session resume bookkeeping and
loop-break sweeps (#329 through #345). The maintainer ended overnight mode on 2026-06-25
and directed this morning-processing (PR #347), retaining a standing attended green-CI =
merge authority that is deliberately *not* overnight mode (normal per-PR logging, no
in-flight lifecycle on this file). This file's content was routed: the two genuinely
unrouted 2026-06-25 decisions, FR-58 (the canonical 3-label inheritance vocabulary) and
the deepen-all thin-baseline cluster decision, were recorded in
[`design-decisions.md`](design-decisions.md) and as dispositions on their TODO items; the
2026-06-23 carried authorizations were already in [`design-decisions.md`](design-decisions.md);
the remaining queued work (FR-167 batch 5 onward, the decided content series, the §4.11
follow-up gates) stays in [`../TODO.md`](../TODO.md); the build-progress log was discarded
as pure-noise per the protocol. The two open maintainer actions (re-seed the scratch
reference binaries durably; provision the external-collaborator worker account) remain
recorded in [`session-handoff.md`](session-handoff.md) and
[`third-party-issues.md`](third-party-issues.md). This file reset to `stub`.
