# Session State (concurrency lease)

**Active-session:** none

**Status:** released

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-19T10:47:44Z

**Current-task:** SESSION CLOSED at session-closing handoff #1043 (2026-07-19 resumed session, `/resume` from #1039; on the VM, gh-CLI, no GitHub MCP; started attended-autonomous -> overnight-unattended -> EARLY WIND-DOWN this morning on a named-degradation signal, converted to a proper session-closing handoff per the discipline #1043 codifies). Lease RELEASED. Merged #1040-#1042: **#1040** Sweep 113 loop-break close-out (PASS for #1039); **#1041** the **answered-question guardrail** (§1.22.6); **#1042** the **wrong-repo tool guardrail** (§1.22.1); **#1043** this closing handoff + the degradation-auto-handoff codification. Both maintainer-directed guardrails LIVE; net zero adopter escapes. **NEXT SESSION** (see session-handoff.md Next-actions, the authoritative resume point): `/resume` runs the compensating-control `/validate` over #1040..#1043, resolves the worker-a elevated-QA escalation + `:333`, then APPLIES THE 5 DELIVERED RESEARCH SEEDS (changelog-daily §1.22.5 first, cobit §1.16 guard-first, content-forks §3.68-70-74, canada-ca-urls §1.22.9), then the rest of the §1.22 block + §3.102 + §1.1/§1.18 + maintainer-gated §1.19.12/13. Keep the worker research pipeline FULL. **`pending-decisions.md`:** the worker-a elevated-QA escalation (for maintainer review) + `:333` SEF-06/SEF-07 apply pending.

**Worker-dispatches:** both `worker-20260716-a`, `worker-20260716-b` (VM, Opus 4.8, LIVE at close). Trust is session-scoped, per-`(worker+model)`; the elevated window re-establishes each fresh session. **worker-a (Opus 4.8): UNVALIDATED** (its first QA delivery this session, validate-pr-1041, MISSED F2, caught by the delivery-1 auditor; per the elevated-QA protocol the window did NOT advance, worker-a gets full ELEVATED QA + a delivery-1 auditor on its next QA delivery; escalation recorded in `pending-decisions.md` for maintainer review). **worker-b (Opus 4.8): 1 clean elevated pass** (Sweep 113 delivery 1, CLEAN); re-establishes next session. Registry quirk (§3.88): probe the order-file `status`, not the registry heartbeat, before declaring a stall. Sync scratch `origin/main` AFTER a fetch before every coordination-plane read (§3.93). 5 research seeds delivered (in scratch `results/`+`inbox/`); a stale `validate-pr-1042` order in scratch `queue/` to delete next session.

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
