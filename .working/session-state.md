# Session State (concurrency lease)

**Active-session:** none

**Status:** released

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-18T23:48:16Z

**Current-task:** SESSION CLOSED at session-closing handoff #1039 (2026-07-18b resumed session, `/resume` from #1020; on the VM, gh-CLI, no GitHub MCP; attended-autonomous throughout). Lease RELEASED (Status: released, Active-session: none). Merged #1021-#1038: **§1.19.8** (#1028-#1030 relocation + fail-loud `_private` assurance + pointer minimization; §1.19.11 closed #1029; change-set deep-assessment findings-fix #1031), **§1.19.9** (#1032-#1034 gate-50 dynamic floor + sweep-tool + the dated-archive migration, data-safe), **§1.19.10** (#1035-#1037 tiered public-CHANGELOG migration + full per-PR source to `grc_library_private`), the **maintainer-alert watchdog SOP** (#1038), plus the #1022-#1027 first-fixes + protected-apply + §1.21. Net zero adopter escapes; every PR 72/72. **NEXT SESSION** (see session-handoff.md Next-actions, the authoritative resume point): `/resume` runs the pre-positioned **Sweep 113** `/validate` (over #1021..#1038, pinned to #1039's merge SHA), then **§1.19.12** (CLAUDE.md sensitivity-trim apply, DEFERRED here, treat as SENSITIVE, classification locked) -> **§1.19.13** (history scrub, MAINTAINER-GATED, LAST) -> §1.19.10a + task #4 + P1. Both workers Opus 4.8 (Fable-5 deferred); worker-QA extra-care on §1.19.x-moves; maintainer-alert SOP LIVE; resume starts attended-autonomous then overnight in a few hours. **`pending-decisions.md`: none open.**

**Worker-dispatches:** both `worker-20260716-a`, `worker-20260716-b` (VM, Opus 4.8, role `any`). Trust is session-scoped, per-`(worker+model)`; the elevated window RE-ESTABLISHES this fresh session. **worker-a (Opus 4.8): ROUTINE** as of its 3rd clean ELEVATED pass this session (sweep-112 d1 + validate-pr-1029 d2 + the §1.19.8-change-set deep-assessment d3; all proof-of-run genuine, mechanical facts independently re-derived MATCH). Routine consume applies to further worker-a Opus-4.8 QA deliveries (re-verify positives, trust clean-with-proof-of-run); a model change re-triggers the elevated window. **worker-b (Opus 4.8): ROUTINE** as of its 3rd clean ELEVATED pass this session (validate-pr-1028 d1 + validate-pr-1031 d2 + validate-pr-1033 d3; all proof-of-run genuine, mechanical facts independently re-derived MATCH). BOTH workers now at routine trust (Opus 4.8); a model change re-triggers the elevated window. Registry quirk (§3.88): probe the order-file `status`, not the registry heartbeat, before declaring a stall. Sync scratch `origin/main` AFTER a fetch before every coordination-plane read (§3.93).

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
