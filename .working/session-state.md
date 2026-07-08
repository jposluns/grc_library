# Session State (concurrency lease)

**Active-session:** claude/resume-sweep90-validate

**Status:** active

**Last-heartbeat-UTC:** 2026-07-08T21:08:42Z

**Current-task:** ACQUIRED at the 2026-07-08 `/resume` from the #713 session-closing handoff (prior lease `released`; no live `origin/claude/*` siblings inside the 60-minute window; the 17 `origin/claude/*` branches are merged squash-remnants of #700-#713; git cross-check clean). Environment: local NUC, `gh` CLI (no GitHub MCP), egress available (iso.org 403s), NO stop-hook auto-commit-push (commit and push manually), pipe-guard PreToolUse hook fires. Mode: **ATTENDED-AUTONOMOUS DAYTIME**. First PR (this close-out on `claude/resume-sweep90-validate`): ran **Sweep 90** (the loop-break corpus-wide `/validate` over the #700..#712 deltas; PASSED, no asserted-expectation contradiction; 1 in-window note B-1 = `lint-guardrail-cadence.py:74` stale inventory comment FIXED with count-free placeholders; 1 out-of-window note A-1 = `specification-master-project.md` §4.4 Principle-vs-Charter/Policy disambiguation bullet ADDED at maintainer direction), advanced the sweep cursor to Sweep 90, pruned the handoff to current + 1 prior, and ACQUIRED this lease. **Queue (maintainer-directed):** PR 2 the resume-pointer `RESUME.md` apply (Fable scratch #114); PR 3 the worker-collision START-side check (TODO/CLAUDE.md/runbook carriers + a scratch COVERAGE.md re-verdict PR); then the AIQT scratch one-liner (payload D), the first FULL `/reference-audit`, the ALLOWED_TYPES parity gate (hard CI gate), the 3.16/3.17 FULLER alignment maps; then OFFER the first `/deep-assessment`; then the standing deferred/blocked queue. **Up-front clarifications batched this resume (answered):** changelog PR 3 = keep deferred; first `/deep-assessment` = defer; 3.16/3.17 = fuller build; ALLOWED_TYPES gate = hard CI gate; A-1 = fix now (done). **PRIOR session:** the 2026-07-08 resumed session (`claude/resume-sweep89-deep-assessment`) shipped #700-#712 and released the lease at #713.

**Worker-dispatches:** the Fable worker (`worker-20260708-fable`, maintainer-directed 2026-07-08) DELIVERED apply-ready packages: `deep-assessment-build` (scratch PR #109, applied #701/#702); `aiqt-codification` (scratch PR #110, applied #705/#711/#712, with one unapplied sub-task = the scratch `CLAUDE.md` AIQT one-liner, payload section D, queued this session); `reference-audit-build` (scratch PR #111, gate-label-corrected #112, applied #706/#707); and `resume-pointer` (scratch PR #114, `inbox/worker-20260708-fable/resume-pointer/`, PENDING apply as this session's PR 2). All applied under validate-then-apply with per-PR QA. The earlier external worker session (2026-07-03) delivered 30 staged work-units to the scratch inbox; applied so far: FR-99/#681, FR-15/#682, FR-23/#683, FR-63/#697. The remaining scratch-inbox applies stay queued (serial validate-then-apply, full per-PR QA). The wave-7 staged pool (2 briefs: corpus-skill distillation, GR-GAP-1 register population) remains available for pickup. A scratch coverage-refresh sync is queued (index 28 PRs behind, 3 dead `ref/*` brief paths, 5 dead coverage anchors per `audit-brief-freshness.py`).

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
