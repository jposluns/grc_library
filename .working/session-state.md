# Session State (concurrency lease)

**Active-session:** claude/stage-deferred-protected-machinery

**Status:** active

**Last-heartbeat-UTC:** 2026-07-15T04:14:11Z

**Current-task:** ACTIVE on branch `claude/stage-deferred-protected-machinery` (resumed VM orchestrator session). **OVERNIGHT MODE (maintainer-invoked 2026-07-15): high-assurance harness on every item; green CI = merge authority, no idle-stop; wind down only on evidence-backed quality degradation; stay in overnight mode until the maintainer explicitly says it is morning (do not exit even if the maintainer resumes mid-night).** The §2.4 website effort is live on grclibrary.ai and in a maintainer live-review loop. Merged this session: the live-review round #921-#924, the adoption round #925-#926, close-out #927, #928 (five-CTA hero + pack sidebar + Get-started cards), and #929 (the TODO permanent-numbering framework + 4 recorded items §1.14/§2.15/§2.16/§3.75 + the gate-69 rationale fix; counters P1 1.15 / P2 2.17 / P3 3.76 / P4 4.29 / P5 5.10 / P6 6.6 / P7 7.6). Merged the massive-item split wave (#930-#932), #933 (§3.50 gate-69 widening), #934 (§3.34 go-forward preflight link-resolution check). **In flight, PR #935 (this branch):** overnight prep for the remaining machinery, staged §3.22 (D7 marker fix) + §3.12 (See-Also parity gate) into [`deferred-protected-changes.md`](deferred-protected-changes.md) items 8/9 (both touch the protected `.claude/CLAUDE.md`, so daytime-apply) and recorded the §3.38 assessment (gate-39 mechanizable idioms largely covered by P8-P12; FP-safe residual needs attended census); batches #934 QA. **OVERNIGHT-SAFE UNBLOCKED QUEUE NOW EXHAUSTED:** the remaining items are protected (§3.22/§3.12, drafted for daytime), attended (§3.34-historical, §3.73 self-deferring), FP-delicate (§3.38 residual), or source/egress-gated (§2.1/§2.3/§2.15-§2.21/§1.x/§2.6). **Next:** hold at this clean state IN OVERNIGHT MODE (per the maintainer's "stay in overnight mode until I say morning"); resume building if a further unblocked overnight-safe item is identified or the maintainer redirects. Daytime priority on return: clear the deferred-protected backlog (items 6/8/9), then §3.34-historical + §3.38 residual + the routed forks + attended backlog. **Blocked / attended overnight (do NOT attempt unattended):** §2.15/§2.16 (attended-only website), §1.14 (egress), §1.1 (protected pack rule), §1.12 (gated on website work), §2.6 (maintainer console), source-gated annexes. Corpus-wide `/validate` + P1/P2 batch remain deliberately SKIPPED (crash-resume, not a QA-skipping handoff; `main` green 69/69). Green-at `99f3a5b` (#934) = 69/69. Standing cleanup: DRY the landing/pack contents-sidebar CSS. See [`session-handoff.md`](session-handoff.md) and [`overnight-pr.md`](overnight-pr.md) for the full state.

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
