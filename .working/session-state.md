# Session State (concurrency lease)

**Active-session:** claude/1199a-gate50-floor

**Status:** active

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-18T19:53:04Z

**Current-task:** ACTIVE, 2026-07-18 resumed session (`/resume` from #1020; on the VM, gh-CLI, no GitHub MCP). Mode **attended-autonomous** (maintainer-set). Merged #1021-#1030 this session, closing §1.19.8 across #1028 (relocation) + #1029 (layered fail-loud assurance + `_private` gate/CI, closed §1.19.11) + #1030 (`_private`-pointer minimization). Then, maintainer-directed, OFFLOADED a DEEP-ASSESSMENT of the whole §1.19.8 change-set to worker-a (pinned to #1030's merge SHA); consumed under ELEVATED QA (all findings re-verified at source, 10 `_private`-content assumptions verified true), MAINTAINER-SIGNED-OFF: 7 low-severity findings (0 High). **#1031 MERGED** (§1.19.8 deep-assessment findings-fix: all 7 findings + 6 stragglers fixed; **§1.19.8 FULLY CLOSED** across #1028/#1029/#1030/#1031). **#1032 IN FLIGHT (branch `claude/1199a-gate50-floor`):** §1.19.9 PR A guard-first = gate 50's per-register dynamic floor for the dated-archive sweep (verifier CONFIRMED-CORRECT; 72/72; behaviour unchanged pre-sweep). Gate-grouping corrected at build (source-verified): only gate 50 needs the floor; gate 60 reads the newest guardrail-review row only (sweep-safety, not a cutoff); D5 reads only the PR diff (no change). #1031's validate-pr OFFLOADED to worker-b (elevated, in flight) + retro batch into #1032. **NEXT:** §1.19.9 PR B (generalize sweep tool -> _private + aged-roll-up-row sweep + guardrail-reviews newest-row safety + initial sweep) -> §1.19.10 (tiered public CHANGELOG) -> §1.19.12 apply -> §1.19.13 (gated). **`pending-decisions.md`: none open.** **Standing:** present the per-priority TODO count table after every merged PR; sync scratch every PR before any credit-offload read (§3.93); explicit `cd /home/jposluns/<repo> &&` on cross-repo git; attended-autonomous mode is maintainer-set (changes only on their signal).

**Worker-dispatches:** both `worker-20260716-a`, `worker-20260716-b` (VM, Opus 4.8, role `any`). Trust is session-scoped, per-`(worker+model)`; the elevated window RE-ESTABLISHES this fresh session. **worker-a (Opus 4.8): ROUTINE** as of its 3rd clean ELEVATED pass this session (sweep-112 d1 + validate-pr-1029 d2 + the §1.19.8-change-set deep-assessment d3; all proof-of-run genuine, mechanical facts independently re-derived MATCH). Routine consume applies to further worker-a Opus-4.8 QA deliveries (re-verify positives, trust clean-with-proof-of-run); a model change re-triggers the elevated window. **worker-b: 1 clean ELEVATED pass** (validate-pr-1028 delivery 1; needs 2 more before routine). Registry quirk (§3.88): probe the order-file `status`, not the registry heartbeat, before declaring a stall. Sync scratch `origin/main` AFTER a fetch before every coordination-plane read (§3.93).

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
