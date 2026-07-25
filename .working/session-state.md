# Session State (concurrency lease)

**Active-session:** claude/sweep122-closeout-and-ledger-repair

**Status:** active

**Operating-mode:** fully-attended

**Last-heartbeat-UTC:** 2026-07-25T23:32:22Z

**Current-task:** ACQUIRED at the 2026-07-25c `/resume` (branch `claude/sweep122-closeout-and-ledger-repair`). Live state verified: 78/78 green at `c3cefd8f`, counts 78/15/24/15, library `2026.07.665`, pack `1.65.14`. Sweep 122 (loop-break `/validate` for #1169..#1177) was PRE-QUEUED at the prior wind-down, delivered, and CONSUMED: PASS, zero genuine misses. Maintainer directive this session: a session must not close with a large unvalidated PR (#1176 merged with its `/validate-pr` dispatched-never-served); and the six fused ledger rows are REPAIR-FIRST-THEN-GATE. Queue: this close-out PR, then the ledger-fusion repair, then TODO 3.73's gate, then 3.120 once #1176's QA returns. `validate-pr-1176` is queued with no eligible claimant; a fresh codex worker is requested from the maintainer.

**Worker-dispatches:** file-drop plane. LIVE at acquire: `opus-20260725T121943Z-78ff` (delivered `sweep122-resume-validate`, consumed under elevated QA), `codex-20260725T041432Z-f8b8` (holds `fnaudit-sweep121`), `codex-20260725T210500Z-81f5` (holds `selftest-gaps-workers-deliveries`, revived after a tmux nudge). OUTSTANDING and UNSERVABLE: `validate-pr-1176`, declined by both codex workers on a documented independence conflict. Maintainer directive 2026-07-25c: nudge stale or stopped workers via tmux injection (`tools/manage-workers.py --send wake`) for the rest of this session. 30 deliveries sit in the tray and 8 inbox drops are unprocessed, four of them worker-raised issues, all read this session.

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
