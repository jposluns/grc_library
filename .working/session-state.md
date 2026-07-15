# Session State (concurrency lease)

**Active-session:** claude/resume-sweep107-validate

**Status:** active

**Last-heartbeat-UTC:** 2026-07-15T23:19:08Z

**Current-task:** ACTIVE. 2026-07-15 resumed session (`/resume` from #963), attended-autonomous, on the VM, gh-CLI (no GitHub MCP). First PR #964 = the loop-break Sweep 107 `/validate` close-out over the #955..#963 delta window (one low-severity in-window finding, the §2.4 `TODO section 2.4` prose-orphan in `.web/build.py` + `web-generator-health.yml` + the cloudflare runbook, contradicting the closing session's whole-repo-0-residual assertion; FIXED here). **Maintainer-set running order for this session (2026-07-15): (1) correct issues; (2) reference-breadth + matrix-fit for the newly-held Canada.ca ref sources; (3) triage each of the 15 scratch inbox items for validity/relevance, process the still-valid ones (and their TODO items), delete the stale; (4) P1 TODO items; (5) P3 TODO items.** Standing steer: before each queued task, assess whether worker research would save the orchestrator >20% effort and, if so (and the item has no inter-dependencies and won't go stale in a few days), drop a research seed in `grc_library_scratch` for a worker to pick up tomorrow (the maintainer is low on usage credits and wants token-heavy research offloaded). The AICM-code defect (task-1) is to be fixed via `/matrix-fit` (maintainer-chosen). Version-maturation deferred to after P3 if credits allow. Lease active.

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
