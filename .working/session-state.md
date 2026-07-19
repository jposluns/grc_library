# Session State (concurrency lease)

**Active-session:** claude/resume-sweep113-closeout

**Status:** active

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-19T00:41:52Z

**Current-task:** ACTIVE (2026-07-19 resumed session, `/resume` from #1039; on the VM, gh-CLI, no GitHub MCP; STARTS attended-autonomous, switches to overnight-unattended in a few hours per maintainer). Lease ACQUIRED. First PR #1040 = the Sweep 113 loop-break close-out (offloaded to worker-b, elevated-QA CLEAN, PASS for #1039) + handoff prune + lease acquire. **This session's maintainer-directed work block (privatization/guardrail tightening, outranks the queue):** (1) wrong-repo guardrail = a probe-based PreToolUse hook (no list; self-discovers sibling `tools/` locations; blocks with the correct repo); (2) `.ref`/`.scratch`/`.private` README fallback-wording fix (placeholder is an adopter signpost + hard-gated empty marker, never a maintainer content fallback); (3) `.working` cycle-out to `_private` = generalize the §1.19.9 sweep tool + an advisory staleness reporter + a session-boundary dedicated cleanup PR policy + an initial sweep of clearly-done content. **`.project-governance/` = KEEP as-is** (maintainer confirmed after reviewing the design + gate-53-retirement cost; the move was NOT worth losing the public exemplar/spec/gate). THEN the prior-locked queue: §1.19.12 (CLAUDE.md sensitivity-trim apply, SENSITIVE, classification locked) -> §1.19.13 (history scrub, MAINTAINER-GATED, LAST) -> §1.19.10a + task #4 + P1. **`pending-decisions.md`: `:333` SEF-06/SEF-07 apply pending (maintainer-decided), else none open.**

**Worker-dispatches:** both `worker-20260716-a`, `worker-20260716-b` (VM, Opus 4.8). Trust is session-scoped, per-`(worker+model)`; the elevated window RE-ESTABLISHED this fresh session. **worker-b (Opus 4.8): ELEVATED, 1 of 2-to-3 clean passes** (Sweep 113 delivery 1: proof-of-run genuine, mechanical facts independently re-derived MATCH, delivery-1 false-negative auditor CLEAN in-delta). **worker-a (Opus 4.8): UNVALIDATED this session** (no delivery yet; its first QA-kind delivery gets full ELEVATED QA incl. a delivery-1 auditor). A model change re-triggers a worker's elevated window. Registry quirk (§3.88): probe the order-file `status`, not the registry heartbeat, before declaring a stall. Sync scratch `origin/main` AFTER a fetch before every coordination-plane read (§3.93).

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
