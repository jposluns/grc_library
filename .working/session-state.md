# Session State (concurrency lease)

**Active-session:** claude/resume-sweep120-closeout

**Status:** active

**Operating-mode:** overnight-unattended

**Last-heartbeat-UTC:** 2026-07-25T03:47:17Z

**Current-task:** ACQUIRED at the 2026-07-25 `/resume` (branch `claude/resume-sweep120-closeout`). Mode moved ATTENDED to OVERNIGHT-UNATTENDED at maintainer direction ~03:5xZ with express authorization of the full queue INCLUDING merging H-01 on green (the maintainer chose the merge option with the no-human-review tradeoff stated; the orchestrator compensates by running the full high-assurance harness on H-01 rather than the single pre-push verifier). All four `/home/grc` repos synced; 77/77 green at `1b8cb202`. Sweep 120 loop-break `/validate` OFFLOADED and in flight (worker-20260716-a). Overnight queue: consume Sweep 120; apply the saturation file-drop-awareness patch; fix the 5 deep-assessment command lockstep findings; widen gate 44 guard-first; H-01 retention (2 carriers) under high assurance; consume the 2 scratch triage passes and execute the prune; process the 3 maintainer alerts (fix, leave UNCLEARED, clearing is the maintainer's decision); refresh handoff plus session metrics.

**Worker-dispatches:** Fleet on the file-drop transport, worker ids CHURNED this session (the collision defect): opus `worker-20260716-a` (holds `sweep-120-validate`), opus `worker-20260725-c` (holds `fix-worker-id-collision-phase1`), codex `codex-mailz-a` (holds `scratch-queue-results-prune-list` AND `codex-env-package-phase1`, a one-at-a-time violation nothing enforced). CONSUMED this session: `fd-verify-1149-deepassess` (codex, PASS, 4 claims independently re-derived) and its `fnaudit-fd-verify-1149` auditor (opus-c, REFUTED the no-drift conclusion with 2 error findings). DELIVERED, pending consume: `fix-saturation-filedrop-awareness`, `codex-hooks-integration-test` (NOT-READY, 3 HIGH). MANDATORY-OFFLOAD active; git-scratch delivery instruction RETIRED (it caused a worker to rewrite the shared `.git/index`).

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
