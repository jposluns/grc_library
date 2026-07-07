# Session State (concurrency lease)

**Active-session:** none

**Status:** released

**Last-heartbeat-UTC:** 2026-07-07T01:04:49Z

**Current-task:** RELEASED. The `claude/grc-acquisition-reconfirm-brief-k8fppo` session shipped #685 (Sweep-87 loop-break close-out; A-F1 framework Scope fix) and RELEASES the lease in the #686 session-closing handoff PR; the next session acquires at `/resume` step 0. Session arc: ran **Sweep 87** first (loop-break control over the #680..#683 deltas, PASSED: A-F1 fixed in #685, B/C 0, no asserted-expectation contradiction); authored the maintainer-directed maximal-scope acquisition-and-reconfirm brief into `grc_library_scratch` `requests/` (scratch #107) and the owed coverage-sync (scratch #106); a mid-session **GitHub-MCP token expiry plus git-push credential outage** blocked the PR/merge pipeline, so the OVERNIGHT run was transferred to the maintainer's **NUC egress instance** (working `gh` + egress). Connectivity was restored at wind-down: this session self-merged scratch #106/#107 (Q4=B) and closes cleanly at #686. The #685 `/validate-pr` was owed (dispatched pre-outage, not persisted) and re-run at wind-down: 1 out-of-window finding (`procedure-grc-programme-management-and-annual-review.md:29` omits architecture) routed to **TODO 1.12** + the NUC handoff. **0 pending decisions, 0 verifier overrides, 0 active high-assurance items** (all three registers clean at close). **IMPORTANT, the next `/resume` runs on the maintainer's NUC (a local machine with `gh`-CLI GitHub auth + egress), not this cloud environment**: the cloud-specific `## Known environment behaviours` (stop-hook auto-commit-and-push, git-proxy 403 on direct scratch pushes, HTTPS agent proxy) must be re-verified at resume; GitHub on the NUC is via `gh` credentials (immune to the claude.ai-connector MCP outage). The NUC session runs **Sweep 88** over the #685..#686 deltas first, then the queue (TODO 1.12 annual-review architecture fix as the first corpus PR; then the Q1/Q2/Q3 overnight queue: FR-63 (2.7), the 3.16/3.17 alignment builds, small P3/P4; then, with egress, the egress-gated 1.5/1.11/GR-GAP-1/SR-1 and the 11 legislation deepenings). PRIOR (historical): `claude/resume-chptc7` (ATTENDED-AUTONOMOUS) shipped #680 (Sweep-86 close-out) + #681 (FR-99) + #682 (FR-15) + #683 (FR-23) and released the lease at #684.

**Worker-dispatches:** the external worker session (maintainer-launched 2026-07-03, read-only-on-main) DELIVERED all 30 staged work-units plus the read-only QA report (all merged scratch-side; the deliveries sit in the scratch inbox, fr-59 half-consumed). The prior `claude/resume-chptc7` session applied 3 of them (FR-99/#681, FR-15/#682, FR-23/#683); the k8fppo session applied NONE (its substantive work was the acquisition-and-reconfirm brief, scratch #107, plus the coverage-sync scratch #106). The remaining scratch-inbox applies (FR-63 and the rest, per maintainer Q2, serial validate-then-apply, full per-PR QA) move to the NUC overnight run, after its `/resume` Sweep 88 and the TODO 1.12 fix. The wave-7 staged pool (2 briefs: corpus-skill distillation, GR-GAP-1 register population) remains available for pickup.

This file is the session-concurrency lease: the declared half of the two-part interlock
that protects the shared `main` state surfaces (the session handoff, [`../TODO.md`](../TODO.md),
[`DONE.md`](DONE.md), the QA history registers, the detailed CHANGELOG mirror, and the four
version surfaces) from a second orchestrator session resuming while a prior one is still
live. The full design, including the honest limitation that this is an advisory interlock
and not a hard mutex, is recorded in [`design-decisions.md`](design-decisions.md) under
"Session-concurrency safety".

Lifecycle (audit gate 63 enforces the SHAPE; the `/resume` step-0 procedure enforces the
interlock, because CI runs per-branch and cannot see across concurrent sessions):

- **Acquire**: at session start, right after the `/resume` step-0 check passes, the
  session writes `Active-session: <its branch>`, `Status: active`, and a fresh
  `date -u +%Y-%m-%dT%H:%M:%SZ` heartbeat.
- **Refresh**: the heartbeat is re-stamped at each PR close-out (it batches into the
  recursion-avoidance refresh alongside the session handoff).
- **Release**: the session-closing handoff PR sets `Status: released` and
  `Active-session: none`, so a cleanly-closed session leaves a released lease on `main`.

The declared state above is only the LAST-MERGED session's view. The other half of the
interlock is external: `/resume` step 0 also runs a `git fetch` cross-check of unmerged
`origin/claude/*` branches for commits inside the 60-minute staleness window (the crash
net for a session that died without releasing). Status `active` or `winding-down` with a
heartbeat inside the window means a session is likely live: HOLD and surface to the
maintainer; do not proceed on a timeout. A not-`released` lease with a heartbeat OLDER
than the window is surfaced as an abandoned-session takeover decision instead.
