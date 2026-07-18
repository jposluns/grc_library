# Session State (concurrency lease)

**Active-session:** none

**Status:** released

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-18T12:12:03Z

**Current-task:** RELEASED at the session-closing handoff PR #1020 (2026-07-17b resumed session; `/resume` from #999; merged #1000-#1019; VM, gh-CLI, no GitHub MCP). The session ran overnight-unattended, switched to daytime-unattended at the 2026-07-18 "good morning", then to attended-autonomous to present the wind-down decisions as choice options. Wind-down was MAINTAINER-CHOSEN at a logical stopping point (§1.19 Phase 1 complete). No degradation signal all session (20 grc_library PRs #1000-#1019, all clean; caught slips were the verification layer working; net zero adopter escapes). **NEXT SESSION** resumes via `/resume` (see [`session-handoff.md`](session-handoff.md) "Next actions" for the LOCKED order): consume the pre-positioned **Sweep 112** loop-break `/validate`, then the FIRST-FIXES (SEF-07 + §1.20), then the protected-apply backlog (2-3 PRs), then §3.22 D7, then §1.19.x Phase 2 (§1.19.13 maintainer-gated, defer-if-away). `pending-decisions.md` is EMPTY. **Standing:** fixing surfaced issues outranks the queue; sync scratch every PR before any credit-offload read (§3.93); read scratch `origin/main` via `git show` after a fetch; explicit `cd /home/jposluns/<repo> &&` on cross-repo git; every egress need the session cannot fulfill goes on the maintainer-egress-request list; after every merged PR present per-priority TODO counts + the running daily added/closed tally; overnight-mode OFF needs an EXPLICIT maintainer signal (never a timeout).

**Worker-dispatches:** both `worker-20260716-a`, `worker-20260716-b` (VM, Opus 4.8, role `any`). Trust is session-scoped, per-`(worker+model)`; the elevated window re-establishes each orchestrator session. **BOTH workers reached ROUTINE trust this session** (worker-b at validate-pr-1002 its 3rd clean elevated pass; worker-a at validate-pr-1005 its 3rd); no red flag, no reset all session. All this-session orders delivered + consumed CLEAN (validate-pr-1000..1019 offloaded/self-run, plus research seeds `seed-114`, `seed-119-12`, and `deep-assessment-r5`). At close a **Sweep 112** `/validate` (over #1000..#1019, pinned to #1020's merge SHA) is being PRE-POSITIONED as an offload for the next resume's loop-break. Both workers free at wind-down. Registry quirk (§3.88): `workers/`-entry heartbeats can lag order-claim heartbeats; probe the order-file `status`, not the registry heartbeat, before declaring a stall. NOTE (§3.93): read worker/queue/results state from scratch `origin/main` AFTER a fetch, never the un-synced local scratch checkout (the 2026-07-17 stale-read recurrence, now codified as sync-scratch-every-PR).

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
