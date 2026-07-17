# Session State (concurrency lease)

**Active-session:** claude/resume-sweep110-validate

**Status:** active

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-17T14:35:22Z

**Current-task:** ACTIVE. The 2026-07-17 resumed session (`/resume` from #991, on the VM, gh-CLI, no GitHub MCP; maintainer ATTENDED, mode `attended-autonomous`). Lease ACQUIRED this resume. **FIRST PR (`claude/resume-sweep110-validate`):** the mandatory loop-break Sweep 110 close-out (OFFLOADED to `worker-20260716-a`, elevated-QA consume) + records the §1.19.x discussion locks (below) + prunes the handoff (keep current+1-prior) + this lease acquire. **§1.19.x locks decided this resume (the three open items + a new deferred item):** #7 (§1.19.11) = minimal `_private` validate gate + README + CLAUDE.md; #8 (§1.19.10) = tiered public CHANGELOG (current week per-PR 1-2 sentences / 30 words per sentence; weeks < 3mo -> one <=4-sentence weekly paragraph; > 3mo -> monthly), event-driven weekly cycle, maintainer-side generated projection (NOT a CI gate), per-PR + full detail move to `_private`, folds in §1.12 + reshapes D8, git-history minability accepted; worker-lean = worker inputs stay in scratch, `_private` orchestrator-only (tightest worker read surface). NEW deferred item: unix-socket/listener worker<->orchestrator transport (tied to §3.87, later discussion). **NEXT after this PR:** EXECUTE §1.19 Phase 1 (§1.19.1-§1.19.7) fresh, as its own PRs. Also open (lower): §1.16 COBIT title normalize + gate, §1.17 r4 citation fixes (HOLD for r4 sign-off), r4 Phase-8 sign-off (HOLDS), §3.87/§3.88 credit-offload thread. §2.22 Canada = DEFERRED-BLOCKED (maintainer egress downloads). Repo-safety: read `origin/main` via `git show origin/main:<path>`; explicit `cd` on cross-repo git; `grc_library_private` clone at `/home/jposluns/grc_library_private` (direct push works).

**Worker-dispatches:** carried from the 2026-07-16c session (both `worker-20260716-a`, `worker-20260716-b`; VM, Opus 4.8, role `any`; both LIVE at this resume). Trust is session-scoped, per-`(worker+model)`; the elevated window RE-establishes each orchestrator session. **`worker-20260716-a`: RE-GRADUATED to routine trust** this resume. It served `sweep-110-validate` (claimed 2026-07-17T14:18:03Z, delivered `done`); consumed under full ELEVATED-QA (proof-of-run genuine ~359K; independent re-derivation of base #984/baseline 69-69/pre-flight 421-33-11/parity 69/counts all EXACT-MATCH; every finding re-verified at source; no red flag, no separate auditor). That is its 3rd clean post-reset elevated pass (validate-pr-988, validate-pr-990, sweep-110), so it CROSSES the 2-to-3 floor and relaxes to routine trust for the rest of this session. **`worker-20260716-b`: routine trust** last session (3 clean elevated); trust re-establishes this session on its first QA-kind delivery. Registry quirk (§3.88): `workers/`-entry heartbeats can lag the order-claim heartbeats; the availability gate keys on the fresh signal.

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
