# Session State (concurrency lease)

**Active-session:** claude/resume-planning-questions-dd9mxk

**Status:** active

**Last-heartbeat-UTC:** 2026-07-05T16:48:14Z

**Current-task:** DAYTIME-UNATTENDED run (2026-07-05, switched from OVERNIGHT at ~08:15Z by explicit maintainer message). grc_library merged through #656; scratch merged through #105. Per the mode-exit ordering the deferred-protected-backlog clearance ran first: #652 landed CLAUDE.md items 1 and 5a, #653 the two TODO-lifecycle codifications, #654 the pack-tree MITRE ATLAS technique-ID currency refresh (TODO 3.18 pack half), #655 the guardrail-review SKILL cadence clause (TODO 3.15 D-F2), #656 the evidence-grounded-completion corollaries on three pack surfaces (TODO 3.15 D-F3 pack half), and #657 (building now) is the project-CLAUDE.md D-F3 corollary clause (closing the TODO 3.15 D-F3 item, all four surfaces now naming the corollaries) plus the #656 improvement-log-repair-narrative correction, carrying the batched #656 QA rows. MAINTAINER-DIRECTED 2026-07-05 (two messages): after #657, stay on small Priority 3 and Priority 1 items first to clear as much TODO count as possible, with TODO 3.15's many small sub-items an endorsed pool: #658 = the 3.15 r5 close-out-checklist clauses (D7-naming, summary/description-lag half-line, /claim-fit cadence candidate), then the other small 3.15 items, the P3 cleanup items (3.1 FIT-8 + the matrix gate-49-coupled PR, 3.21 residuals, 3.13/3.16/3.17/3.4), and P1 1.9 harness-fix; the egress-gated 1.11 and 1.5 wait on egress; the larger GR-P1 to P5 design track (TODO 4.7) DEFERS; P2 2.1 after. Remaining deferred protected-file edits staged in deferred-protected-changes.md (item 5 = #658 r5 clauses; item 6 = GR-P track).

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
