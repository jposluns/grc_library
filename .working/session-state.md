# Session State (concurrency lease)

**Active-session:** claude/resume-sweep111-closeout

**Status:** active

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-17T21:01:10Z

**Current-task:** ACTIVE. The 2026-07-17b resumed session (`/resume` from the session-closing handoff #999, on the VM, gh-CLI, no GitHub MCP; maintainer ATTENDED, mode `attended-autonomous`). Lease ACQUIRED this resume (`claude/resume-sweep111-closeout`); heartbeat re-stamped each PR close-out. **First task done:** consumed the pre-positioned **Sweep 111** loop-break `/validate` (worker-a delivery, order `sweep-111-validate` pinned `65c5075b`/#999, deltas #992..#998) under full ELEVATED-QA (worker-a delivery 1 this fresh session): proof-of-run genuine (~296K, A/B/C returns), independent re-derivation of HEAD/counts/pre-flight 422-32-11/versions all EXACT-MATCH, both notes re-verified at source, a dedicated delivery-1 false-negative auditor returned CLEAN VERDICT HOLDS. **CLEAN PASS (0 error / 0 warning / 0 new); loop-break control for #999 PASSES.** **PR plan this session:** PR1 = this Sweep-111 close-out (lease acquire + validate-sweeps row + cursor + §3.93 TODO item); PR2 = record the r4 Phase-8 maintainer SIGN-OFF (2026-07-17b) + apply the §1.17 corpus citation fixes (W1/N2/W2 + S110-1, held-source-verified, skeptical verifier); PR3 = the §3.93 fetch-scratch-every-PR codification; then §1.19.7 (last Phase-1 item, worker-offloaded manifest), then Phase 2 (§1.19.8-§1.19.13). Also open (lower): §1.16 COBIT title normalize + gate, §1.18 surface map, §3.88 registry auto-prune, §3.91/§3.92. §2.22 Canada = DEFERRED-BLOCKED (maintainer egress downloads to grc_library_ref/ingest/). Repo-safety: **sync scratch every PR** (`cd grc_library_scratch && git fetch && git reset --hard origin/main`) BEFORE any credit-offload read (§3.93, the 2026-07-17 recurrence); read `origin/main` via `git show origin/main:<path>`; explicit `cd` on cross-repo git; `grc_library_private` clone at `/home/jposluns/grc_library_private` (direct push works); create the feature branch BEFORE editing after a merge+sync.

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
