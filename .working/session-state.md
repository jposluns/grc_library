# Session State (concurrency lease)

**Active-session:** none

**Status:** released

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-27T21:44:08Z

**Current-task:** RESUME from #1200 (2026-07-27 morning, maintainer present, "good morning + swap to daytime mode"). Acquired the lease at 11:19:54Z. Mode swapped overnight-unattended -> attended-autonomous (daytime; maintainer reachable, green-CI = merge authority, decisions surfaced by exception). Corpus green at `8094b06d` (78/78 gates), non-shallow, detect-env maintainer/all-siblings-ok. First tasks: loop-break corpus-wide /validate over #1195..#1199 (compensating control for the #1200 handoff); then the morning pre-queue (vpr-1199b, 3.145 fail-closed candidate, 3.133 close-out tool); process 5 open MAINTAINER_ALERTs + 12 unprocessed inbox drops.

**Worker-dispatches:** file-drop standing-poll plane shows **0 live workers** at resume (all ids stale/out, oldest ~38h). The exec-dispatch harness (`tools/exec-dispatch.py`) spawns a fresh worker per order on demand (accounts in `_private/worker-accounts.json`), so 0 standing-poll workers is NOT "no workers": offloadable passes dispatch via exec-dispatch. Concurrency stays at cap 1 (per-account) until TODO 3.145 (fail-closed registry) lands.

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
