# Session State (concurrency lease)

**Active-session:** claude/rb7-close

**Status:** active

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-22T20:01:07Z

**Current-task:** 2026-07-22 resumed session (`/resume` from #1055; on the VM, gh-CLI, no GitHub MCP; ATTENDED, maintainer actively directing). This session's assistant was a WORKER on `grc_library_ref` last session and is the ORCHESTRATOR now. Goal (maintainer-directed): assess the `_ref` ingest output (catalogue 696->727, +31 items, `_ref` main green at `3e63317`, ingest COMPLETE) and ensure all relevant newly-ingested contents have their corpus-related files updated to reference/cite as needed (TODO RB-7 + the FULL new-ingest set, maintainer-decided scope). First PR #1 = this resume close-out: the loop-break Sweep 116 `/validate` over the #1054..#1055 deltas (offloaded to worker-b), re-triage of the aged Sweep-3 follow-up at `validate-sweeps/history.md:L133` (default 30-day re-triage deadline lapsed during the multi-day gap, failing gate 43 + the FollowupAgeing regression test; NOT a corpus regression), the handoff prune, and this lease acquire. Maintainer decisions this session (recorded scratchpad `session-decisions-2026-07-22.md`): scope FULL; Wiz "Securing AI Agents 101" discard-candidate DELETE (`_ref`-side); Colombia RNBD -> maintainer-egress + clean that file of already-ingested rows; §3.70 crypto = TIGHTEN THE PACK too (parity PR).

**Worker-dispatches:** `worker-20260716-b` (role qa, VM, Opus 4.8) re-registered LIVE 2026-07-22T14:26:57Z (the maintainer set it up this resume); `worker-20260716-a` STALE (last_seen 2026-07-19). ONE live worker, so the offloadable passes (loop-break `/validate`, RB-7 `/reference-audit`) run serially through worker-b; request a second worker if parallelism is needed. worker-b's session-scoped elevated-QA window RE-ESTABLISHES this session (fresh session), so its first delivery this session (the Sweep 116 `/validate`) is consumed under full ELEVATED QA. Fetch scratch `origin/main` before every coordination-plane read (§3.93); prefer `git -C <scratch>` (or an absolute script path) for sibling tools/git.

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
