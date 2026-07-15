# Session State (concurrency lease)

**Active-session:** claude/resume-sweep105-validate

**Status:** active

**Last-heartbeat-UTC:** 2026-07-15T12:02:02Z

**Current-task:** ACTIVE. The 2026-07-15 resumed session (`/resume` from #942) holds the lease on branch `claude/resume-sweep105-validate`, attended-autonomous on the VM, gh-CLI (no GitHub MCP). Lease acquired at the `/resume` step-0 check (prior lease was `released` by #942; git cross-check found only the merged #941/#942 branches in-window). Mode is maintainer-set: **attended-autonomous**, and the maintainer directed that **website updates/enhancements take priority this session** (finish the current unit before switching to a newly-arrived website request). This first PR is the loop-break **Sweep 105** `/validate` close-out over the #918..#942 window: it fixes the one finding (A-1, `.web/build.py` domain-page secondary-sort divergence, a user-visible website ordering defect that CONTRADICTED the #942 handoff's "#940 consistent" claim), writes the sweep detail file + history row, advances the resume cursor, prunes the handoff (kept #942 + #917, dropped the #901-#913 sweep102 blocks), and acquires this lease. **NEXT after this PR:** the maintainer's pack-page card-links website request (the three §02 cards on `/pack` get linked kickers matching the landing-page pattern), then the website/§2.4 queue (§2.16 residual, publish go), then §3.43 gate-48 Check-6 (unblocked), §3.76 TYPE_ORDER DRY guard (now also covering the secondary key per A-1), §3.34/§3.38, deferred-protected items 6/8/9, routed forks.

**Worker-dispatches:** the Sweep 105 `/validate` dispatched three read-only-git subagents (A recent-PR deep review, B corpus-wide stale-reference sweep, C audit-programme integrity) on the shared tree; A returned 1 warning (the A-1 sort divergence, fixed this PR), B and C returned 0 findings, all asserted-clean surfaces corroborated except the one A-1 contradiction. The `grc_library_scratch` inbox holds 15 pure-research seeds (11 PENDING + 4 UNMAPPED per `tools/audit-delivery-status.py`), all deliberately KEPT in the §3.58 disposition; unchanged this session.

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
