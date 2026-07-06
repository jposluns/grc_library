# Session State (concurrency lease)

**Active-session:** none

**Status:** released

**Last-heartbeat-UTC:** 2026-07-06T17:33:08Z

**Current-task:** RELEASED at the #679 session-closing handoff. The `claude/resume-tl5rez` daytime session (ATTENDED-AUTONOMOUS) shipped **#662 through #678** and closed with the #679 handoff (which committed the batched #678 QA rows, reconciled the handoff snapshot and asserted-expectations, and released this lease). The full explicit maintainer mandate was completed (#674-#677: the three protected `.claude/CLAUDE.md` changes, TODO 1.9 closed as a documented harness limitation, the #670 lowercase-rejection confirmed); #678 triaged the TODO 3.15 protection-tooling queue (two free-prose advisories census-vetoed, GR-GAP-1 egress-gapped, all recorded in design-decisions). 0 pending decisions, 0 verifier overrides. The next session ACQUIRES this lease at `/resume` step 0 and runs the corpus-wide `/validate` (Sweep 86 over the #662..#678 deltas) FIRST, then the verified-blocked/queued items in the handoff snapshot (GR-GAP-1 with egress, the D8 narrower-standing-scan retry, P2 2.1 with held sources, the small P3 items, the scratch README refresh). PRIOR (historical): the 2026-07-05 daytime-unattended session shipped #645 through #659, landed #660 (session-closing handoff) and #661 (`/resume` `/validate` Sweep 85); the older per-session handoff blocks await the next `/resume` prune.

**Worker-dispatches:** one EXTERNAL worker session live (maintainer-launched 2026-07-03, read-only-on-main prompt constraints); it has DELIVERED all 30 staged work-units plus the read-only QA report (all merged scratch-side; 30 deliveries pending applies in the scratch inbox, fr-59 half-consumed); the wave-7 staged pool (2 briefs: corpus-skill distillation, GR-GAP-1 register population) is available for pickup

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
