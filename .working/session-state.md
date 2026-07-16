# Session State (concurrency lease)

**Active-session:** claude/credit-offload-phase3

**Status:** active

**Last-heartbeat-UTC:** 2026-07-16T13:52:53Z

**Current-task:** ACTIVE. The 2026-07-16 resumed session (`/resume` from #968, on the VM, gh-CLI, attended-autonomous) acquired the lease. Step-0 interlock passed (prior lease released, heartbeat 2h+ stale, no live sibling). Mandatory resume mechanics done: 69/69 green at `37abc69`/#968 (descendant of the asserted green-at `6c28f57`/#967, no drift); versions match snapshot. The maintainer started a LIVE credit-offload worker (`worker-20260716-a`) and directed: (1) OFFLOAD the mandatory loop-break Sweep 108 `/validate` (#964..#968) to the worker as the test (ENQUEUED as blocking prio-0 order `sweep-108-validate` on scratch `main`; awaiting delivery to `results/sweep-108-validate.md`); (2) apply deferred-protected item 10 (credit-offload phase 3) as designed + consume/develop the worker's `worker-lifecycle-winddown` design brief (scratch commit `5f14df1`); (3) then the whole remaining deferred-protected backlog (items 6/8/9). Per-PR `/validate-pr` this session is OFFLOADED to the worker (credit-conservation, the credit-offload model). Repo-safety: confirm target repo before every write; keep `/tmp/grc_library_ref` in sync on any ref update.

**Worker-dispatches:** `worker-20260716-a` (VM, egress none) is LIVE, claimed `canada-ca-reference-breadth` (token 1), heartbeating. Orchestrator ENQUEUED `sweep-108-validate` (blocking, prio 0) as the credit-offload test. Sweep 108 `/validate` and per-PR `/validate-pr` subagents are offloaded to the worker this session; the orchestrator re-verifies positives and writes the audit-trail rows. Pre-push skeptical verifiers stay orchestrator-side (§3.81, critical-path). 5 pre-existing background orders on scratch (3 Canada prio-1, 2 apply-drafting prio-2) plus the P4/P6 research-seed inbox deliveries (unchanged).

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
