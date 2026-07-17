# Session State (concurrency lease)

**Active-session:** claude/todo-1-19-2-resolve-sibling

**Status:** active

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-17T18:12:32Z

**Current-task:** ACTIVE. The 2026-07-17 resumed session (`/resume` from #991, on the VM, gh-CLI, no GitHub MCP; maintainer ATTENDED, mode `attended-autonomous`). Lease ACQUIRED this resume. **#992 MERGED (`claude/resume-sweep110-validate`):** the loop-break Sweep 110 close-out (offloaded to worker-a, elevated-QA PASS, loop-break for #991 PASSED) + §1.19.x locks + handoff prune + lease acquire. **#993 IN FLIGHT (`claude/todo-1-19-1-portability-test`):** §1.19 Phase-1 item §1.19.1 = `tools/check-portability.sh` (adopter-clone portability test, PASS 69/69 sibling-free + non-vacuity proven) + the validate-pr-992 consume (worker-b, elevated, delivery-1 auditor clean) + the self-caught worker-a trust-tier correction (W1) + the trivial 174-vs-175 fix + §3.89 (D7-inert) route. **§1.19.x locks decided this resume (the three open items + a new deferred item):** #7 (§1.19.11) = minimal `_private` validate gate + README + CLAUDE.md; #8 (§1.19.10) = tiered public CHANGELOG (current week per-PR 1-2 sentences / 30 words per sentence; weeks < 3mo -> one <=4-sentence weekly paragraph; > 3mo -> monthly), event-driven weekly cycle, maintainer-side generated projection (NOT a CI gate), per-PR + full detail move to `_private`, folds in §1.12 + reshapes D8, git-history minability accepted; worker-lean = worker inputs stay in scratch, `_private` orchestrator-only (tightest worker read surface). NEW deferred item: unix-socket/listener worker<->orchestrator transport (tied to §3.87, later discussion). **NEXT after this PR:** EXECUTE §1.19 Phase 1 (§1.19.1-§1.19.7) fresh, as its own PRs. Also open (lower): §1.16 COBIT title normalize + gate, §1.17 r4 citation fixes (HOLD for r4 sign-off), r4 Phase-8 sign-off (HOLDS), §3.87/§3.88 credit-offload thread. §2.22 Canada = DEFERRED-BLOCKED (maintainer egress downloads). Repo-safety: read `origin/main` via `git show origin/main:<path>`; explicit `cd` on cross-repo git; `grc_library_private` clone at `/home/jposluns/grc_library_private` (direct push works).

**Worker-dispatches:** carried from the 2026-07-16c session (both `worker-20260716-a`, `worker-20260716-b`; VM, Opus 4.8, role `any`; both LIVE at this resume). Trust is session-scoped, per-`(worker+model)`; the elevated window RE-establishes each orchestrator session. **`worker-20260716-a`: ELEVATED this session (1 of 2-to-3).** It served `sweep-110-validate` (claimed 2026-07-17T14:18:03Z, delivered `done`); consumed under full ELEVATED-QA (proof-of-run genuine ~359K; independent re-derivation of base #984/baseline 69-69/pre-flight 421-33-11/parity 69/counts all EXACT-MATCH; every finding re-verified at source; no red flag, no separate auditor). **CORRECTION (self-caught, #993):** an earlier #992 record wrongly called this a "re-graduation to routine" by counting validate-pr-988/990 (LAST session) toward the floor; the elevated window is SESSION-SCOPED and resets each session (CLAUDE.md `## Credit-offload mode`, "it resets each session by construction"), so this session's count is 1 (sweep-110 only) and worker-a stays ELEVATED. Its next QA-kind delivery still gets elevated QA. **`worker-20260716-b`: ROUTINE trust RE-ESTABLISHED this session** at validate-pr-995 (its 3rd clean elevated pass this session: validate-pr-992 with a delivery-1 auditor + validate-pr-994 + validate-pr-995, all SHIP clean); its subsequent QA-kind deliveries this session get routine consume (re-verify positives, trust a clean result with proof-of-run). worker-a is still ELEVATED (1 of 2-to-3; only sweep-110 so far this session). Registry quirk (§3.88): `workers/`-entry heartbeats can lag the order-claim heartbeats; the availability gate keys on the fresh signal.

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
