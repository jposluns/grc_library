# Session State (concurrency lease)

**Active-session:** claude/protected-claudemd-bundle

**Status:** active

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-18T14:32:41Z

**Current-task:** ACTIVE, 2026-07-18 resumed session (`/resume` from #1020; on the VM, gh-CLI, no GitHub MCP). Mode **attended-autonomous** (maintainer returned ~14:00Z). Merged #1021-#1025 this session (Sweep-112 close-out; SEF-07; §1.20; §1.21; §1.19.12-lock); **#1026 in flight** (protected bundle items 11/12/15: §1.15 CLOSED, QA-completion standard added to CLAUDE.md + the pack rule, §3.93 currency fix). P1 CLOSED this session: §1.20, §1.21, §1.15. Net zero escapes. **NOW closing out the §1.19.x series** (maintainer-directed): §1.19.12 classification LOCKED (broad-trim, #1025); next = RE-RUN the §1.19.12 assessment over the updated CLAUDE.md (items 11/12 added) -> the one-by-one keep/move/split REVIEW with the maintainer -> §1.19.8 (relocate living docs to `_private`, move-list reviewed-with-maintainer-first) -> §1.19.9 (dated-archive sweep + gate cutoffs) -> §1.19.10 (tiered public CHANGELOG) -> §1.19.11 (`_private` hygiene) -> §1.19.13 (history scrub, LAST, maintainer-gated). §1.19.10/11 shapes CONFIRMED locked. **Still pending before §1.19.8:** item 8 (D7 fix) + items 13/14 (adopt/resume wiring) from the protected backlog; :333 RESOLVED (SEF-06+SEF-07, maintainer-approved) apply pending in its own PR. **`pending-decisions.md`: :333 resolved, none open.** **Standing:** present the per-priority TODO count table (Priority / Currently Open / Completed today / Added today) after every merged PR; sync scratch every PR before any credit-offload read (§3.93); explicit `cd /home/jposluns/<repo> &&` on cross-repo git; attended-autonomous mode is maintainer-set (changes only on their signal).

**Worker-dispatches:** both `worker-20260716-a`, `worker-20260716-b` (VM, Opus 4.8, role `any`). Trust is session-scoped, per-`(worker+model)`; the elevated window RE-ESTABLISHES this fresh session, so both start UNVALIDATED. **worker-a: 1 clean ELEVATED pass so far** (sweep-112-validate, delivery 1; proof-of-run genuine, mechanical facts independently re-derived MATCH, dedicated false-negative auditor dispatched); needs 2-3 clean elevated passes before routine. **worker-b: free, unvalidated this session** (0 passes). Registry quirk (§3.88): probe the order-file `status`, not the registry heartbeat, before declaring a stall (worker-a's registry heartbeat lagged the order heartbeat during sweep-112). Sync scratch `origin/main` AFTER a fetch before every coordination-plane read (§3.93).

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
