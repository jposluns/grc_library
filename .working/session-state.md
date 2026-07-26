# Session State (concurrency lease)

**Active-session:** claude/1194-close-out-3135

**Status:** active

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-26T23:37:39Z

**Current-task:** POST-WIND-DOWN RESUME 2026-07-26. Fresh session resuming after the prior session's maintainer-directed EMERGENCY WIND-DOWN (elevated error rate late in a long compacted session; see `grc_library_private/resume-winddown-2026-07-26.md`, read first per maintainer direction). Verified the clean guard-green OPEN #1193 (all 78 gates + CI green), re-dispatched an independent skeptical verifier pinned to the real committed head `bb7ff1f9` (CLEAN: it stripped D4's exemption to prove the load-bearing claim and hunted every reader of the 5 de-versioned files), then merged #1193 (`--admin --squash`, squash `1f9bfa25`, logged). The post-merge `validate-pr-1193` returned 0 error / 2 warning / 1 note: both warnings are #1193 CLOSE-OUT slips (it merged mid-wind-down, so its close-out was truncated), the spec section-6 D7 narrative left stale after the D7 SURFACES change and the TODO section-3.135-to-DONE rotation dropped. This PR (`claude/1194-close-out-3135`, #1194) is the focused close-out completion: fixes both warnings, adds #1193's merge-bypass / validate-pr / retro rows, records the findings, acquires this lease, bumps versions. Next: the loop-break `/validate` over the un-swept #1185..#1194 window, then the maintainer-approved origin-paragraph + weekly-summary PR, then band 2 (TODO 3.133/3.136/3.134/3.137).

**Worker-dispatches:** file-drop plane, **0 workers live** at resume (all ids stale/out, oldest heartbeat ~6.7h). QA this session runs as in-session subagents until a worker fleet is spun up: the #1193 pre-merge skeptical verifier (CLEAN) and `validate-pr-1193` (0e/2w/1n, both warnings fixed in #1194) both ran as in-session subagents, per the mandatory-offload no-workers fallback. The four stale worker orders from the wind-down (`verify-1193`, `verify-1193b`, `validate-pr-1193`, `retro-1193`) are INVALID (dispatched against the wrong state) and are NOT consumed.

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
