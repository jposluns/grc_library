# Overnight PR

**Status:** stub

<!-- OVERNIGHT-PR-STUB -->

This file is the durable handoff record for a maintainer-authorized autonomous overnight
session. It is `stub` when no overnight session is in flight (the default state).

Lifecycle (audit gate 46 enforces it: passes on `stub` and `in-flight`, fails on `done`):

- `stub`: no overnight session in flight. This file holds only this protocol description, the `Status: stub` line, and (after a routed run) a short closure note recording where the last run's content went.
- `in-flight`: an overnight session is active. The assistant fills the file with the authorization scope, design decisions made, files being authored or modified, build progress, and open ambiguities. Each overnight PR ships `in-flight`.
- `done`: the session ended. The next-morning processing PR routes the content to the durable ledgers (design decisions to [`design-decisions.md`](design-decisions.md), closed work to [`DONE.md`](DONE.md), queued follow-ups to [`../TODO.md`](../TODO.md)) and resets this file to `stub`.

Latest-run closure note: the 2026-07-04 overnight run (PRs #622 through #627, six merges, all green with full per-PR QA) ended when the maintainer awoke after the #627 merge, with the GR-8(b) closure build in flight (completed as the #628 morning-boundary close-out), and switched the session to **daytime attended-autonomous mode** by direct message; per the awake-early exception this file transitioned `in-flight` -> `stub` directly in the #628 close-out that routed its content. The run's headline: the section-3.15 machinery wave (delta gate D6; the gate-18 trailing-link seam fix; gates 64 and 65, taking the inventory to 65 gates and the suite to 326; the `/guardrails` r4 review, 19 findings, none dropped), the worker QA-report intake (21 validated findings routed), and the section-3.1 consistency sweep; scratch-side the external worker consumed the entire staged pool (30 deliveries in the inbox pending applies). Content routed: closed work to [`DONE.md`](DONE.md); per-PR progress to `CHANGELOG.md` and git history; the r4 G-8 cadence note (a hallucination-metrics refresh row is due at the P2 applies boundary) and the forward queue (GR-8(b) close-out, S3 PR B, the P2 applies, the 3.19/3.20/3.21 interleave bundles) to [`session-handoff.md`](session-handoff.md); the open decisions to [`pending-decisions.md`](pending-decisions.md) (the 2026-07-04 morning list: WCO SAFE, the disposition vocabulary, the expiry tail, option B). Prior runs' closure notes live in this file's git history: pruned to the single latest note per the change-tracking rule's stub form, the artefact-side resolution of the r4 D-F5 finding.
