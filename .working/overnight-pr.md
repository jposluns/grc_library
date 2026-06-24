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

Last run: the 2026-06-24 CCM/AICM-and-relocations overnight run (PRs #301-#305),
authorized to close out the XS/S backlog and as many Medium items as possible. It
shipped #301 (Sweep 36 close-out, CCM/AICM citation-residual completion), #302
(guardrail-review word-form gate count), #303 (Day-1-floor option A), #304 (R3
relocation), and prepared #305 (loop-break generalization into the pack) which could
not be merged at the time because the GitHub MCP server disconnected (recorded in
[`third-party-issues.md`](third-party-issues.md)). The fresh morning session (2026-06-24)
merged #305 once MCP reconnected, ran the corpus-wide Sweep 37 loop-break control
(close-out PR #306, which fixed the two out-of-window CCM v4.0 domain-name residuals
Sweep 36 had surfaced), and morning-processed this file. Its content was routed:
DD-overnight-1 (the gate-48 bare-domain-code coverage gap) and the R1 won't-move
decision were recorded in [`design-decisions.md`](design-decisions.md); R1 (the
sweep-preflight-exemptions.json relocation) was closed won't-move and rotated to
[`DONE.md`](DONE.md); the two morning-review items (the operations-file CCM residuals,
and R1) were resolved by the maintainer this morning; R2 (the citation-cluster
relocation) remains a deferred follow-up in [`../TODO.md`](../TODO.md) with its
convention-conflict noted. This file reset to `stub`.
