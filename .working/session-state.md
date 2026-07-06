# Session State (concurrency lease)

**Active-session:** claude/resume-chptc7

**Status:** active

**Last-heartbeat-UTC:** 2026-07-06T21:58:00Z

**Current-task:** ACTIVE on `claude/resume-chptc7` (ATTENDED-AUTONOMOUS), acquired at the 2026-07-06 `/resume` step 0 (prior lease `released`, no live `origin/claude/*` siblings, git cross-check clean). Ran **Sweep 86** (the loop-break corpus-wide `/validate` over the #662..#679 deltas) as the first task: the compensating control PASSED, no in-window regression and no asserted-expectation contradiction; 1 warning + 7 notes (8 findings across 6 F-classes), all pre-existing/marginal gate-blind ISO-designation debt. F1/F3/F5 fixed and F2/F4 routed in the Sweep-86 close-out PR (#680), which also prunes the handoff (keep current + 1 prior), records the step-5 decisions, and closes the TODO 3.15 D8 candidate (rest-on-convention). **Progress:** #680 (Sweep-86 close-out) merged; **FR-99 applied (#681)**, **FR-15 applied (#682)**, **FR-23 applied (#683)**; handoff requested (#683 is the last substantive PR; a session-closing handoff PR follows). **Maintainer Option B (2026-07-06):** the 11 legislation-citing deepenings (fr-59/60/74/41, the 5 annexes, dora, nis2) are deferred pending the egress instance. **Queue:** the non-legislation set this session, serial validate-then-apply, full per-PR QA: FR-63 (2.7), the 3.16/3.17 Q3 alignment builds (surface-then-build), small P3/P4 (gr-10, pack-language, s-c/s-d); the scratch coverage-refresh sync folds into a consolidated post-batch sync; egress-gated 1.5/1.11/GR-GAP-1 wait on the egress instance. **0 pending decisions, 0 verifier overrides, 0 active high-assurance items.** PRIOR (historical): the `claude/resume-tl5rez` session shipped #662 through #678 and closed with the #679 handoff.

**Worker-dispatches:** the external worker session (maintainer-launched 2026-07-03, read-only-on-main) DELIVERED all 30 staged work-units plus the read-only QA report (all merged scratch-side; the 30 deliveries sit in the scratch inbox, fr-59 half-consumed). This session is APPLYING those 30 deliveries (maintainer Q2, serial validate-then-apply, full per-PR QA), after the queued scratch coverage-refresh sync. The wave-7 staged pool (2 briefs: corpus-skill distillation, GR-GAP-1 register population) remains available for pickup.

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
