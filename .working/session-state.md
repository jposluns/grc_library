# Session State (concurrency lease)

**Active-session:** none

**Status:** released

**Operating-mode:** overnight-unattended

**Last-heartbeat-UTC:** 2026-07-27T03:18:01Z

**Current-task:** SESSION-CLOSING HANDOFF at #1199 (overnight-unattended, evidence-triggered wind-down: A12 threshold met + a named RM-10 slip; see the handoff CURRENT block and degradation-watch-log 2026-07-27). Shipped #1193-#1199 (concurrency registry code half landed at cap 1, NOT enabled; all CHANGELOG roll-up + codifications done). Lease RELEASED. Morning pre-queue: vpr-1199b (#1199 validation, jposluns-work), the 3.145 fail-closed candidate (delivered, unapplied), the 3.133 close-out tool (security-work). The morning /resume runs the loop-break /validate over #1195..#1199 and consumes the pre-queue first.

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
