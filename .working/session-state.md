# Session State (concurrency lease)

**Active-session:** claude/todo-1-19-7c-adopt-ref-bootstrap

**Status:** active

**Operating-mode:** overnight-unattended

**Last-heartbeat-UTC:** 2026-07-18T02:24:06Z

**Current-task:** ACTIVE, **OVERNIGHT-UNATTENDED** (mode flipped 2026-07-18T01:16Z on the maintainer's explicit "Go"; VM, gh-CLI, no GitHub MCP). Lease on `claude/todo-1-19-7c-adopt-ref-bootstrap`; heartbeat re-stamped each PR close-out. **MERGED this session:** #1000-#1006 + grc_library_ref #88; **#1007 in flight** (§1.19.7(c) `/adopt` `.ref` bootstrap planner `tools/adopt-bootstrap-ref.py` + SKILL step-4 + pack 1.62.1; closes §1.19.7 = Phase-1 COMPLETE; also closes §1.12 subsumed + §3.18 decided; batches #1006 QA). **ALL maintainer-gated decisions pre-collected** before overnight (see `pending-decisions.md` `## 2026-07-17b overnight-transition batch`): the overnight QUEUE is in `next-prs.txt` `# then:` (codify QA-completion SOP -> §1.19.12/13/18 prep-drafts -> P1 protections §1.15a/§1.14-LayerA/gate-71/§3.90-91-92 -> decided content §1.16/§2.22/3.68-3.71/3.66/3.84/3.86/3.74 -> fill). **PARALLEL:** worker `deep-assessment-r5` dispatched (pinned a42a2a0b, priority 2) + `validate-pr-1006` consumed CLEAN. **Standing QA-completion SOP (maintainer-directed):** analyze QA results on arrival, fix non-risky in-window, DOCUMENT risky for morning review; fixing is highest-priority (finish current task, then fix). **HELD for attended tomorrow:** §1.19.8/9/10/11 + §1.19.12/13 APPLY (drafts only overnight). WORKERS both ROUTINE trust. Repo-safety: **sync scratch every PR** before any credit-offload read (§3.93); read `origin/main` via `git show`; explicit `cd /home/jposluns/<repo> &&` on cross-repo git; overnight OFF needs an EXPLICIT maintainer signal (never a timeout).

**Worker-dispatches:** both `worker-20260716-a`, `worker-20260716-b` (VM, Opus 4.8, role `any`; both LIVE this resume, fresh heartbeats after a maintainer restart). Trust is session-scoped, per-`(worker+model)`; the elevated window RE-establishes each orchestrator session, so BOTH start UNVALIDATED this fresh 2026-07-17b session regardless of last session's routine trust. **`worker-20260716-a`: ELEVATED this session, 1 of 2-to-3 clean elevated passes.** It served `sweep-111-validate` (delivered `done` 2026-07-17T20:39Z); consumed under full ELEVATED-QA with a dedicated delivery-1 false-negative auditor (CLEAN VERDICT HOLDS); no red flag. One more clean elevated pass -> routine. **`worker-20260716-b`: UNVALIDATED this session** (no QA-kind delivery yet this session); its first QA-kind delivery gets full elevated QA + a delivery-1 auditor. Registry quirk (§3.88): `workers/`-entry heartbeats can lag order-claim heartbeats; the availability gate keys on the fresh signal. NOTE (§3.93): read worker/queue/results state from scratch `origin/main` AFTER a fetch, never the un-synced local scratch checkout (the 2026-07-17 stale-read recurrence).

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
