# Session State (concurrency lease)

**Active-session:** claude/resume-planning-questions-dd9mxk

**Status:** active

**Last-heartbeat-UTC:** 2026-07-05T15:54:27Z

**Current-task:** DAYTIME-UNATTENDED run (2026-07-05, switched from OVERNIGHT at ~08:15Z by explicit maintainer message). grc_library merged through #655; scratch merged through #105. Per the mode-exit ordering the deferred-protected-backlog clearance runs first: #652 landed CLAUDE.md items 1 and 5a, #653 the two TODO-lifecycle codifications (DONE-completion summary; accepted-unverified tracker), #654 the pack-tree MITRE ATLAS technique-ID currency refresh (TODO 3.18 pack half closed), #655 the guardrail-review SKILL cadence clause (TODO 3.15 D-F2 closed: the auto-prompt bullet names gate 60 and states the deferral is bounded, warn at drift 1 to 2, fail at 3), and #656 (building now) is the evidence-grounded-completion one-liner corollaries named on three pack surfaces (TODO 3.15 r4 D-F3 pack half; 3.15 stays open, the project `.claude/CLAUDE.md` clause rides the #657 bundle), carrying the batched #655 QA rows. Next after #656: the #657 bundle (the 3.15 D-F3 project-CLAUDE.md clause, the 3.15 r5 close-out clauses, and the reinforced summary/description-lag checklist half-line, all `.claude/CLAUDE.md` touches), then the GR-P1 to P5 design track, then P1 1.9 harness-fix investigation and the egress-gated 1.11 and 1.5, then the P3 cleanup items (3.1 FIT-8 + the matrix gate-49-coupled PR, 3.21 residuals, 3.13/3.16/3.17/3.4), the scratch originals/README refresh, the Sweep-84 Brazil annotation, then P2 2.1. Remaining deferred protected-file edits still staged in deferred-protected-changes.md.

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
