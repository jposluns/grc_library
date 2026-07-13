# Session State (concurrency lease)

**Active-session:** claude/deep-assessment-r3-phase6

**Status:** active

**Last-heartbeat-UTC:** 2026-07-13T22:36:49Z

**Current-task:** ACTIVE, **attended-autonomous** (maintainer-set at the 2026-07-13 resume; green CI = merge authority, decisions surfaced by exception, full per-PR `/validate-pr` + `/retro`, stricter-is-safer). Running the maintainer-invoked formal **`/deep-assessment` r3** (continue-in-session, maintainer-chosen at the mid-run checkpoint). Phases 1-2 complete; Phase-3 semantic instruments `/validate` (Sweep 101), `/guardrails` (r10), `/claim-fit`, `/screen-publications`, `/matrix-fit`, `/full-qa`, and now `/fitness` all COMPLETE; Phase-4 gate-efficacy substantially complete. Phases 1 to 6 are now COMPLETE. CURRENT PR (this branch): Phase 6 (pipeline integrity: 1 Low F-1 nightly-sweep SHA-pin FIXED in-window, secret scan clean across 1123 commits, guard/hook fail-loud, branch protection verified; QA-ledger meta-audit: record HONEST, 0 sham, 0 uncaught escape; adoptability on-ramp resolves) + #896 batched QA. NEXT: Phase 7 routing-consolidation + Phase 8 PRESENT-for-maintainer-sign-off and HOLD (the only terminal state; no self-sign-off). r3 register `in-progress`, Phase 8 HELD. Standing high-assurance items: DA-ASVS (the ASVS 5.0.0 chapter remap) + the three AI-annex items. Green-at `a5d2edd` (#887, r3 base) = 69/69; each PR verified post-merge.

**Worker-dispatches:** none active this session. The `grc_library_scratch` inbox holds 15 pure-research seeds (11 PENDING + 4 UNMAPPED per `tools/audit-delivery-status.py`), all deliberately KEPT in the §3.58 disposition and schedule-gated (P4/P6 new-domain builds, FR-59, the 3.15/3.16 crosswalks); no seed is apply-ready or dispatched this session. The `/fitness` pass dispatched ten read-only persona subagents (P1 to P10) plus #893's `/validate-pr` Subagent A this branch; all returned.

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
