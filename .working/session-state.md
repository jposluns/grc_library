# Session State (concurrency lease)

**Active-session:** claude/resume-planning-questions-dd9mxk

**Status:** active

**Last-heartbeat-UTC:** 2026-07-05T08:09:08Z

**Current-task:** OVERNIGHT run (2026-07-05, maintainer away). grc_library merged through #651; scratch merged through #105. This turn: SR re-scoping against live scratch state CLOSED SR-4 (scratch PR #104 item-31 count corrections, independently verifier-confirmed, plus #105 item-30 WP-BCR failed-stub drop). Surfaced a new pending item (scratch `originals/README.md` stale 2026-06-27 delivery snapshot; dated-snapshot-vs-rebuild decision, pending item 4). SR-1/SR-2/SR-3 assessed BLOCKED, not quick wins: SR-1 decided (presence+backfill) but egress-gated; SR-2 has no screening-record convention; SR-3 item-29 not locally testable (no PyMuPDF/docx libs) and item-28 needs roughly 20 CSVs catalogued first. 3.21 decision-parked. Next unblocked: non-protected tooling, then P2 (per A4). The grc_library feature branch carries un-PR'd working-state (the consolidation checkpoint, the #650/#651 QA rows, and this SR-4-closure bookkeeping) that rides #652. Protected-file edits DEFERRED to daytime (staged in deferred-protected-changes.md)

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
