# Session State (concurrency lease)

**Active-session:** claude/resume-planning-questions-dd9mxk

**Status:** active

**Last-heartbeat-UTC:** 2026-07-05T11:49:27Z

**Current-task:** DAYTIME-UNATTENDED run (2026-07-05, switched from OVERNIGHT at ~08:15Z by explicit maintainer message: "change to daytime unattended; ask questions, complete P3 and P1, then start P2"). grc_library merged through #651; scratch merged through #105. Eight decisions batched and resolved this round (recorded in pending-decisions.md, now 0 pending): Brazil-annotate, FIT-8 coherence-preserving, matrix ISO-header coupled-lockstep-PR, originals/README refresh-to-live, 3.21 all-per-recommendations, 1.9 pursue-harness-fix (maintainer override), 3.15-r5a reword, P2-start = 2.1. Per the mode-exit ordering, overnight cleanup goes first: the deferred-protected-backlog clearance. Building PR #652 now (the first daytime PR): CLAUDE.md deferred-protected item 1 (mode-transition protocol) + item 5a (rule-3 fallback reword), the deferred-protected + pending-decisions rotations, and the batched #651-QA/SR-4/1.9/consolidation working-state, plus README/CHANGELOG/handoff/lease refresh. Next after #652: remaining deferred-protected backlog (3.18 ATLAS pack refresh; 3.15 pack clauses; GR-P design), P1 1.9 harness-fix investigation, P3 (3.1 FIT-8 + matrix gate-49-coupled PR, 3.21 residuals, 3.13/3.16/3.17/3.4), scratch originals/README refresh, Sweep-84 Brazil annotation, then P2 2.1. Remaining deferred protected-file edits still staged in deferred-protected-changes.md.

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
