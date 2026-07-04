# Session State (concurrency lease)

**Active-session:** claude/worker-onboarding-review-2r8kn2

**Status:** active

**Last-heartbeat-UTC:** 2026-07-04T14:42:47Z

**Current-task:** DAYTIME ATTENDED-AUTONOMOUS (overnight ended at the 2026-07-04 morning boundary); #629 MERGED (4ab8f6d) with full QA, and the wave-7 scratch sync MERGED (scratch #102, e3a088f); S3 PR B in flight on `claude/s3-claim-fit-2r8kn2` (the /claim-fit skill + Tier-A pass, carrying the #629 QA batch, both routed finding fixes, and the maintainer-accepted snapshot-check TODO item); then the P2 applies (with the metrics refresh row at that boundary), 3.19/3.20/3.21 as interleave; the 2026-07-04 morning decision list is RESOLVED (13 answers received and executed into TODO / pending-decisions / design-decisions)

**Worker-dispatches:** one EXTERNAL worker session live (maintainer-launched 2026-07-03, read-only-on-main prompt constraints); it has DELIVERED all 30 staged work-units plus the read-only QA report (all merged scratch-side; applies pending); the staged pool is empty, so the worker idles pending the wave-7 staged briefs landing (the morning decisions themselves are resolved)

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
