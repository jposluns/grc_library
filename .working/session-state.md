# Session State (concurrency lease)

**Active-session:** none

**Status:** released

**Last-heartbeat-UTC:** 2026-07-09T00:59:55Z

**Current-task:** RELEASED at the 2026-07-08/09 session-closing OVERNIGHT-SWAP handoff (#720). This resumed session (`claude/resume-sweep90-validate` and its per-PR branches) ran the loop-break **Sweep 90** at start (#714, PASSED) and shipped **#714** (Sweep-90 close-out + B-1/A-1 fixes + lease acquire), **#715** (Fable resume-pointer `RESUME.md` apply), **#716** (worker-collision START-side check + the #715 dangling-link fix + TODO 3.22), **#717** (gate 67, the Document-Type enumeration parity audit, + the #716 F1 fix), **#718** (Fable reference-acquisition-gap apply, TODO 3.20 bullet 1), **#719** (Fable adopter-experience apply, TODO 4.6 S-a/S-b/S-e). All with full per-PR QA (refute-briefed pre-push verifier on substantive changes + post-merge `/validate-pr` + `/retro`), zero escaped findings. #720 (this handoff) carries the batched #719 count-fix + its `/validate-pr`+`/retro` rows, refreshes the handoff (CLOSING block + asserted-expectations + green-at + session-metrics), and RELEASES this lease. #720 skips its own trailing `/validate-pr`+`/retro` per the loop-break handoff-PR exception. **NEXT SESSION = OVERNIGHT BACKLOG RUN** (maintainer-directed 2026-07-09, on the NUC / local instance): scope BACKLOG ONLY (`/deep-assessment` DEFERRED); autonomy = fix + route + APPLY protected `.claude/`/pack edits (LOCAL-INSTANCE-ONLY) + stricter-safe defaults + NO idle-stop; full per-PR QA never abbreviated. Queue + authorizations in the handoff CLOSING next-actions block + [`pending-decisions.md`](pending-decisions.md) `## Overnight-run authorizations`. Run the #716 START-side check before each item.

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
