# Session State (concurrency lease)

**Active-session:** none

**Status:** released

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-23T01:03:24Z

**Current-task:** 2026-07-22b resumed session (`/resume` from the #1066 session-closing handoff; on the VM, gh-CLI, no GitHub MCP; ATTENDED, maintainer directing). This session ran ONE PR, the resume close-out #1067 (the loop-break Sweep 117 `/validate` over #1056..#1066, OFFLOADED to worker-b, CLEAN PASS 0/0/0/0, loop-break control for #1066 PASSES; the handoff prune; the MAINTAINER_ALERT 2026-07-22-a clear, maintainer-authorized, done scratch-side), then WOUND DOWN at the maintainer's direction because branch protection needs a `gh pr merge --admin` permission the harness classifier blocked (the maintainer will grant it and merge #1067 next session). Lease RELEASED here so that when #1067 merges, `main` lands clean-released. **NEXT SESSION: MERGE #1067 FIRST (it is this close-out; do NOT re-run Sweep 117 over #1056..#1066), then start the INDEPENDENT TOOLING QUEUE** (§1.22.3 `.working` cycle-out tool -> §1.22.4 cross-repo reference-existence tool -> §1.22.7 TODO Maintainer-or-Egress-Gated section -> §3.102 pack-distribute degradation-auto-handoff -> §1.16 COBIT guard-first). The §3.87 home-VM file-drop transport big-build WAITS for the maintainer's sudo `/home/grc` migration.

**Worker-dispatches:** `worker-20260716-b` (role qa, VM, Opus 4.8) LIVE (heartbeat 2026-07-22T20:56:46Z at the Sweep 117 delivery); `worker-20260716-a` STALE (last_seen 2026-07-19). ONE live worker, so the offloadable passes run serially through worker-b; request a second worker if parallelism is needed. worker-b's session-scoped elevated-QA window RE-ESTABLISHES this fresh session, so its first delivery this session (the Sweep 117 `/validate`) was consumed under full ELEVATED QA (independent orchestrator corroboration of the diff scope, the crypto-tighten, and the VM-timeframe probe all matched the CLEAN verdict). Fetch scratch `origin/main` before every coordination-plane read (§3.93); prefer `git -C <scratch>` (or an absolute script path) for sibling tools/git.

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
