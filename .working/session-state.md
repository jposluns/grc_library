# Session State (concurrency lease)

**Active-session:** claude/pr964-qa-and-task1-closeout

**Status:** active

**Last-heartbeat-UTC:** 2026-07-16T01:59:58Z

**Current-task:** ACTIVE (OVERNIGHT as of ~2026-07-16T01:30Z; ends only on explicit maintainer signal). 2026-07-15 resumed session (`/resume` from #963), on the VM, gh-CLI (no GitHub MCP); ran attended-autonomous, then a long attended credit-offload co-design, then the maintainer entered OVERNIGHT mode. Merged this session: #964 (Sweep 107 `/validate` close-out; loop-break for #963 PASSES), #965 (#964 QA + task-1: AICM defect already fixed in #939, re-verified), #966 (credit-offload design record + TODO §1.15/§3.80/§3.81 + phase-3 staging + #965 QA batch). Cross-repo: `grc_library_scratch` #166 (task-2 Canada.ca ref-breadth seed + task-3 discard of 3 drifted deliveries), #167 (ETSI + GR-GAP-1 apply-drafting seeds). Tasks 1-3 done (task-1 issues; task-2 seeded; task-3 triaged: 3 discarded, the apply-ready ETSI/GR-GAP-1 re-seeded as drafting work per credit-conservation, dev-service-account deferred). **OVERNIGHT PLAN:** build credit-offload phases 1-2 on `grc_library_scratch` (queue protocol + `/credit-offload` worker command + helper tool + test order), so a worker is testable tomorrow; then P1/P3 per the running order (seed research-heavy, apply mechanical/tooling only); phase-3 wiring STAGED in `deferred-protected-changes.md` item 10 (remind maintainer on overnight exit). Repo-safety: confirm target repo before every write. **Maintainer-set running order for this session (2026-07-15): (1) correct issues; (2) reference-breadth + matrix-fit for the newly-held Canada.ca ref sources; (3) triage each of the 15 scratch inbox items for validity/relevance, process the still-valid ones (and their TODO items), delete the stale; (4) P1 TODO items; (5) P3 TODO items.** Standing steer: before each queued task, assess whether worker research would save the orchestrator >20% effort and, if so (and the item has no inter-dependencies and won't go stale in a few days), drop a research seed in `grc_library_scratch` for a worker to pick up tomorrow (the maintainer is low on usage credits and wants token-heavy research offloaded). The AICM-code defect (task-1) is to be fixed via `/matrix-fit` (maintainer-chosen). Version-maturation deferred to after P3 if credits allow. Lease active.

**Worker-dispatches:** the Sweep 107 `/validate` dispatched three read-only A/B/C subagents (recent-PR deep review, corpus-wide stale-reference, audit-programme integrity); all findings re-verified by the orchestrator at apply time. Research-seed fan-out to `grc_library_scratch` will be assessed per-item as the queue is worked (maintainer-directed credit-offload). The `grc_library_scratch` inbox holds 15 seeds (11 PENDING + 4 UNMAPPED per `tools/audit-delivery-status.py`), pending the task-3 triage this session.

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
