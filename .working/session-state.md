# Session State (concurrency lease)

**Active-session:** claude/todo-3-92b-adopt-preflight-guard

**Status:** active

**Operating-mode:** overnight-unattended

**Last-heartbeat-UTC:** 2026-07-18T05:07:00Z

**Current-task:** ACTIVE, **OVERNIGHT-UNATTENDED** (mode flipped 2026-07-18T01:16Z on the maintainer's explicit "Go"; VM, gh-CLI, no GitHub MCP). Lease on `claude/todo-3-92b-adopt-preflight-guard`; heartbeat re-stamped each PR close-out. **MERGED this session:** #1000-#1016 + grc_library_ref #88; **#1017 in flight** = §3.92(b) tool-side (`tools/adopt-preflight-guard.py`, fail-safe pre-flight refusing `/adopt` on a non-adopter clone via detect-env classification; +5 tests; `/adopt` step-1 invocation staged deferred item 14; batches #1016 QA). **#1016 done** = §3.92(a) detect-env adopt-config flag. **SAFE-OVERNIGHT MACHINERY QUEUE ESSENTIALLY EXHAUSTED:** remaining safe = §3.93(c) (scratch credit-offload-queue auto-fetch, COMPLETE but edits the live coordination tool I'm using -> session-boundary-better, deferring to avoid mid-session coordination risk), §3.92(c) (classification-coupling note/parity, marginal), §1.14 Layer B (egress-blocked); all else protected (deferred items 6/8/9/11/12/13/14), citation-content, or held. Continuing per no-idle-stop (cannot self-end overnight; needs EXPLICIT maintainer signal). **#1013 done** = §1.15a(a) cross-repo write-guard `tools/repo-guard.sh` + `RepoGuardTests`; part(b) staged deferred item 11. **#1012 done** = Quebec-Law-25 citation ESCALATION (verifier caught 3.3-not-23.3; held source PDF-corrupted; #973 annex-canada 23.3 live error; §3.84 reversed; §3.100 opened; §2.22 DEFERRED); validate-pr-1012 offloaded + consumed CLEAN, INDEPENDENTLY confirmed s.3.3 at held source + upstream LegisQuebec. **ALL maintainer-gated decisions pre-collected** before overnight (see `pending-decisions.md` `## 2026-07-17b overnight-transition batch`): the overnight QUEUE is in `next-prs.txt` `# then:` (codify QA-completion SOP -> §1.19.12/13/18 prep-drafts -> P1 protections §1.15a/§1.14-LayerA/gate-71/§3.90-91-92 -> decided content §1.16/§2.22/3.68-3.71/3.66/3.84/3.86/3.74 -> fill). **PARALLEL:** worker `deep-assessment-r5` dispatched (pinned a42a2a0b, priority 2) + `validate-pr-1006` consumed CLEAN. **Standing QA-completion SOP (maintainer-directed):** analyze QA results on arrival, fix non-risky in-window, DOCUMENT risky for morning review; fixing is highest-priority (finish current task, then fix). **HELD for attended tomorrow:** §1.19.8/9/10/11 + §1.19.12/13 APPLY (drafts only overnight). WORKERS both ROUTINE trust. Repo-safety: **sync scratch every PR** before any credit-offload read (§3.93); read `origin/main` via `git show`; explicit `cd /home/jposluns/<repo> &&` on cross-repo git; overnight OFF needs an EXPLICIT maintainer signal (never a timeout).

**Worker-dispatches:** both `worker-20260716-a`, `worker-20260716-b` (VM, Opus 4.8, role `any`; both LIVE this resume, fresh heartbeats after a maintainer restart). Trust is session-scoped, per-`(worker+model)`; the elevated window re-establishes each orchestrator session. **BOTH workers reached ROUTINE trust this session** (worker-b at validate-pr-1002 its 3rd clean elevated pass; worker-a at validate-pr-1005 its 3rd), so routine consume applies (re-verify positives at source, trust clean-with-proof-of-run). **Recent dispatches (all delivered + consumed):** `worker-20260716-a` served `validate-pr-1012` (CLEAN, the Quebec upstream re-verification) and `seed-114-layer-a-currency-cadence-gate` (research seed, §1.14 gate design, re-authored into gate 72 at #1015). `worker-20260716-b` served `seed-119-12`, `validate-pr-1013/1014/1015` (all CLEAN). `worker-20260716-a` is currently serving `validate-pr-1016` (in flight, rides #1017). All routine consume; no red flag, no reset this session; deliveries 9-11 (b) + validate-pr-1012 & seed-114 (a). (One §3.88-adjacent note: `validate-pr-1013` ran ~4 min with a frozen order heartbeat, a slow run not a stall, because the QA re-fetches the pinned SHA from upstream + runs 71 gates; probe the order-file `status` not the registry heartbeat before declaring a stall.) Registry quirk (§3.88): `workers/`-entry heartbeats can lag order-claim heartbeats; the availability gate keys on the fresh signal. NOTE (§3.93): read worker/queue/results state from scratch `origin/main` AFTER a fetch, never the un-synced local scratch checkout (the 2026-07-17 stale-read recurrence).

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
