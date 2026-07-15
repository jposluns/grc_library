# Session State (concurrency lease)

**Active-session:** claude/landing-nav-nested-216

**Status:** active

**Last-heartbeat-UTC:** 2026-07-15T10:44:12Z

**Current-task:** ACTIVE, ATTENDED, winding down toward a fresh morning session, on branch `claude/landing-nav-nested-216`. The maintainer returned attended (2026-07-15) and directed a task sequence plus a wind-down; the website work was moved into this session so the maintainer reviews the deployed site during wind-down/resume. **Merged this session through #940** (`main` green at `781c0f7`). This turn's PRs: #939 (AICM matrix-fit, 7 fabricated codes -> real AICM v1.1.0, maintainer-approved), #940 (domain-page type-priority ordering: `.web/build.py` page-sort + `build-taxonomy.py` TYPE_ORDER, website pages now read govern->define->do->reference), and IN FLIGHT #941 (this branch) landing-nav two-level nesting (11 domains nested under "By domain", 6 Standards sub-links, Licence, new Contributors->`/about` link, indent CSS; scrollspy + Get-started nesting deferred as the §2.16 residual). **Maintainer decisions applied earlier this turn:** §3.47 rescoped (keep `(was X.Y)` per #929), §3.8 CLOSED keep-as-is, AICM mapping approved, ordering = source+type-priority, website nav = this session. **Batched QA in flight:** #940's `/validate-pr` (SHIP-WITH-NOTES: 1 in-window working-state warning, the lease append-not-reconcile LEAD, FIXED in this #941 full rewrite) + `/retro` ride #941. **Next:** #941 (this) then #942 (session-closing handoff: full handoff / asserted-expectations / session-metrics refresh, RELEASE the lease, exempt from the trailing /validate-pr; next /resume corpus-wide /validate is the compensating control). **Morning session:** review the deployed site (ordering + nav); then the §2.16 residual (scrollspy + Get-started nesting), §3.47 editorial sweep (scope-confirmed), §3.34/§3.38, §3.43 Check-6 (unblocked now AICM is fixed), §3.76 TYPE_ORDER drift guard, deferred-protected 6/8/9, routed forks. Green-at `781c0f7` (#940) = 69/69.

**Worker-dispatches:** across the website effort each substantive PR ran a pre-push refute-briefed skeptical verifier plus a post-merge `/validate-pr` Subagent A, all read-only-git on the shared tree; verdicts SHIP or SHIP-WITH-NOTES with every finding fixed in-window (the only mediums: #922 dev-security dangling-colon intro, #925 a rule-description misstatement; internal notes: recurring build.py docstrings + lease-lag, all fixed). PR8 (#928) ran a pre-push skeptical verifier (SHIP, 0 material) and its post-merge `/validate-pr` returned SHIP-WITH-NOTES (Subagent A, one internal count note, fixed in #929). PR #929 (the numbering framework) ran two independent high-assurance verifiers (correctness + completeness lenses) plus one re-verify, final SHIP, with four findings caught and fixed pre-push (P1 count, P6 counter off-by-one, two stale gate-69 rationale surfaces, missing severity tokens); its post-merge `/validate-pr` returned SHIP 0/0/0. PR #930 (the first TODO split) runs two HA verifiers (correctness + completeness) on the rotation and batches the #929 QA. Overnight-mode HA-for-all is in force from #930 onward. The `grc_library_scratch` inbox holds 15 pure-research seeds (11 PENDING + 4 UNMAPPED per `tools/audit-delivery-status.py`), all deliberately KEPT in the §3.58 disposition; unchanged this session.

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
