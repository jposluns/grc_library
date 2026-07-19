# Session State (concurrency lease)

**Active-session:** claude/119-12-claudemd-trim

**Status:** active

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-19T16:08:21Z

**Current-task:** 2026-07-19b resumed session (`/resume` from #1043; on the VM, gh-CLI, no GitHub MCP; ATTENDED, maintainer actively directing). Lease ACQUIRED. Sweep 114 loop-break `/validate` offloaded to worker-b, DELIVERED (PASS; F1 = TODO §1.22.6 rotation debris at `TODO.md:80`, fix at first close-out). Order LOCKED by maintainer: (1) **§1.19.12 CLAUDE.md sensitivity-trim** (move-map offloaded to worker-a; split destination = `grc_library_private/orchestrator-claude.md` LOADED at `/resume` + passive removal-ledger archive); (2) **self-guard bundle** (repeat-block hook + diagnosis circuit-breaker wired to an evidence-validated `grc_library_private/degradation-watch-log.md` + read-back + intent-vs-artefact disciplines); (3) **credit-offload bundle** (idle-heartbeat fix + clear alert 2026-07-19-a on merge + elevated-QA window ->1 + worker session-start-time reporting + orchestrator restart-advice); (4) **§1.22.2 stub-README fix**. First PR = the trim, carrying the resume close-out (this lease, handoff prune, Sweep 114 row, F1 fix).

**Worker-dispatches:** both `worker-20260716-a` (role any), `worker-20260716-b` (role qa), VM, Opus 4.8, RESTARTED by the maintainer 2026-07-19 ~07:16 Toronto (fresh sessions; each `(worker+model)` elevated window RE-ESTABLISHES). **worker-b delivery 1 this session = Sweep 114 (elevated QA):** genuine proof-of-run, F1 correctly caught, no worker miss (consume at first close-out). **worker-a:** claimed `research-119-12-trim-movemap` (in progress). Maintainer-directed protocol changes to codify in bundle 3: elevated-QA window -> **1 delivery**; workers report **session start-time** at registration/check-in; orchestrator **advises the maintainer when a worker needs a restart**. Fetch scratch `origin/main` before every coordination-plane read (§3.93); prefer `git -C <scratch>` for sibling git.

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
