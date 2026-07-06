# Session State (concurrency lease)

**Active-session:** claude/resume-tl5rez

**Status:** active

**Last-heartbeat-UTC:** 2026-07-06T16:14:01Z

**Current-task:** ACTIVE session `claude/resume-tl5rez` (ATTENDED-AUTONOMOUS, daytime). Has shipped **#662 through #676** and holds **#677 in flight** (close TODO 1.9 as a documented harness limitation plus record the #670 lowercase-rejection confirmation, carrying the batched #676 `/validate-pr` + `/retro` rows and the #636 disposition-token fix). The daytime mode-exit priority ordering has been worked: overnight cleanup (#673), then the three maintainer-authorized `.claude/CLAUDE.md` protected-backlog changes (#674 `/claim-fit` cadence section, #675 D5 eighth closure-form, #676 counts-adjacent-to-enumerations recount residual), then the pending decisions (#677: TODO 1.9 close, #670 rejection confirm). 0 pending decisions (TODO 1.9 RESOLVED and #670 rejection CONFIRMED 2026-07-06), 0 verifier overrides. Corpus green 66/66 at `6038f98` (= #676). NEXT after #677: the standing priority order (tooling/protections then new work): the remaining small P3 items (3.21 residuals if any remain, 3.13/3.16/3.17/3.4), the scratch `originals/README.md` live-manifest refresh (a scratch PR), then P2 2.1 FR-59 privacy-jurisdiction deepening; egress-gated 1.11-verify and 1.5 wait on egress; the GR-P1 to P5 design track (TODO 4.7) DEFERS. PRIOR (historical): the 2026-07-05 daytime-unattended session shipped #645 through #659, landed #660 (session-closing handoff) and #661 (`/resume` `/validate` Sweep 85 close-out); the older per-session handoff blocks await the next `/resume` prune.

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
