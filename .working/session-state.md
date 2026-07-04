# Session State (concurrency lease)

**Active-session:** claude/worker-onboarding-review-2r8kn2

**Status:** active

**Last-heartbeat-UTC:** 2026-07-04T18:47:48Z

**Current-task:** DAYTIME ATTENDED-AUTONOMOUS (overnight ended at the 2026-07-04 morning boundary); #631 MERGED (08c1d4e, FR-59 held-source batch PR 1, the first external-worker delivery apply) with full QA (two verifier rounds pre-push incl. the Critical Quebec 72-hour catch; /validate-pr 4 bookkeeping findings, all routed/fixed in the next PR's batch); queue re-tier DECIDED (maintainer 2026-07-04): remaining P2 applies (incl. FR-59 batch PR 2) move to a separate Opus 4.8 session; THIS session works P1/P3, #633 MERGED (8e9b2b9) with full QA; delta gate D7 (the handoff-snapshot freshness check, first P3 build of the re-tier) in flight as #634, carrying the #633 QA batch; then the remaining P3 machinery items

**Worker-dispatches:** one EXTERNAL worker session live (maintainer-launched 2026-07-03, read-only-on-main prompt constraints); it has DELIVERED all 30 staged work-units plus the read-only QA report (all merged scratch-side; applies underway, fr-59 half-consumed); the wave-7 staged pool (2 briefs: corpus-skill distillation, GR-GAP-1 register population) is available for pickup

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
