# Session State (concurrency lease)

**Active-session:** claude/lock-119-12-classification

**Status:** active

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-18T14:03:37Z

**Current-task:** ACTIVE, 2026-07-18 resumed session (`/resume` from #1020; on the VM, gh-CLI, no GitHub MCP). Maintainer returned ~14:00Z and set **attended-autonomous**. Session so far: Sweep-112 close-out (#1021, CLEAN loop-break for #1020 PASSES) + SEF-07 (#1022) + §1.20 (#1023) + §1.21 (#1024), 2 P1 closed, net zero escapes. NOW: **closing out the §1.19.x series** attended, maintainer-directed order = lock the §1.19.12 CLAUDE.md classification FIRST (broad-trim as drafted), then §1.19.8 (relocate living docs to `_private`) -> §1.19.9 (dated-archive sweep + dynamic gate cutoffs) -> §1.19.10 (tiered public CHANGELOG) -> §1.19.11 (`_private` hygiene) -> §1.19.13 (history scrub, LAST, maintainer-gated). Held-then-unblocked protected-apply bundle (items 11/12/15 CLAUDE.md + 8 D7) still pending. :333 SEF-02 fit decision pending maintainer. **Consumed the pre-positioned Sweep 112** loop-break `/validate` (worker-a, CLEAN A:0/B:0/C:0, loop-break for #1020 PASSES) under ELEVATED QA (worker-a delivery 1 this fresh session). **LOCKED next-work order (maintainer-directed):** (0) fixing surfaced issues outranks the queue; (1) [done] consume Sweep 112; (2) FIRST-FIXES SEF-07 (r5-routed CCM SEF-02->SEF-07 remap) + §1.20 (adopt-preflight test portability); (3) protected-apply backlog small items ([`deferred-protected-changes.md`](deferred-protected-changes.md) items 11/12/13/14/15 quick prose + item 8 §3.22 D7; item 9 See-Also gate DEFERRED [37 candidate pairs, not a clean win]; item 6 GR-P design-tier, assess later); (4) §1.19.x Phase 2 (§1.19.8-11). **HELD for maintainer return:** §1.19.12 (CLAUDE.md review, maintainer explicitly asked to review together on return); §1.19.13 (history scrub, maintainer-gated). `pending-decisions.md` EMPTY. **Standing:** present the new per-priority TODO count table (Priority header / Currently Open / Completed today / Added today) after every merged PR; sync scratch every PR before any credit-offload read (§3.93); explicit `cd /home/jposluns/<repo> &&` on cross-repo git; maintainer-egress-request list for any egress the session cannot fulfill; daytime-unattended ends only on the maintainer's next prompt.

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
