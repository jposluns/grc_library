# Session State (concurrency lease)

**Active-session:** claude/resume-sweep103-validate

**Status:** active

**Last-heartbeat-UTC:** 2026-07-14T14:07:36Z

**Current-task:** ACTIVE, **attended-autonomous** (maintainer-set at the 2026-07-14 sweep103 resume via `AskUserQuestion`: green CI = merge authority, decisions surfaced by exception, full per-PR `/validate-pr` + `/retro`, stricter-is-safer, genuine maintainer decisions asked not deferred). Resumed from #914 (the 2026-07-14 r3-remediation session's closing handoff; lease was RELEASED). The loop-break **Sweep 103** `/validate` over #901..#914 ran (A: 0 / B: 0 genuine / C: 1 in-window note), loop-break control for #914 **PASSED**, all asserted expectations corroborated; the one note (gate-50 §6 detailed prose omitted the #913 Check-5 register row-order guard) FIXED this close-out PR (spec `1.17.3`->`1.17.4`, artefacts regenerated). Queue after this PR (follow-handoff order, banked in [`pending-decisions.md`](pending-decisions.md)): (1) P1 §1.2 CHANGELOG #902+ compact reformat + guardrail strengthening; (2) deferred protected r3 machinery (G1 branch-to-main `.claude/hooks/` edit guard [VM-authorized] + handoff-self-row D-check); (3) routed forks (FR-205 MFA = option A; the rest stricter-safe-where-defensible, route genuine authorial calls); (4) low-risk cleanup (coverage-refresh sync, index 185 PRs behind; P3). See [`session-handoff.md`](session-handoff.md) for the full state. Green-at `f40a042` (#914) = 69/69 (verified this resume).

**Worker-dispatches:** Sweep 103 dispatched three read-only `/validate` subagents (A recent-PR / B stale-reference / C audit-programme); A and B clean, C surfaced the one in-window note (fixed this PR). No apply-stage workers yet this session. The `grc_library_scratch` inbox holds 15 pure-research seeds (11 PENDING + 4 UNMAPPED per `tools/audit-delivery-status.py`), all deliberately KEPT in the §3.58 disposition and schedule-gated; no seed is apply-ready or dispatched.

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
