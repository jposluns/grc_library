# Session State (concurrency lease)

**Active-session:** claude/preflight-mirror-link-resolution

**Status:** active

**Last-heartbeat-UTC:** 2026-07-15T03:55:03Z

**Current-task:** ACTIVE on branch `claude/preflight-mirror-link-resolution` (resumed VM orchestrator session). **OVERNIGHT MODE (maintainer-invoked 2026-07-15): high-assurance harness on every item; green CI = merge authority, no idle-stop; wind down only on evidence-backed quality degradation; stay in overnight mode until the maintainer explicitly says it is morning (do not exit even if the maintainer resumes mid-night).** The §2.4 website effort is live on grclibrary.ai and in a maintainer live-review loop. Merged this session: the live-review round #921-#924, the adoption round #925-#926, close-out #927, #928 (five-CTA hero + pack sidebar + Get-started cards), and #929 (the TODO permanent-numbering framework + 4 recorded items §1.14/§2.15/§2.16/§3.75 + the gate-69 rationale fix; counters P1 1.15 / P2 2.17 / P3 3.76 / P4 4.29 / P5 5.10 / P6 6.6 / P7 7.6). Merged the massive-item split wave (#930 §3.57/§3.62/§3.63/§3.68, #931 §2.4, #932 §2.5), then #933 (§3.50 CLOSED, gate 69 widened to catch `TODO item N.M`). **In flight, PR #934 (this branch):** advanced §3.34 (extended `preflight-changelog.py` to flag a newly-added CHANGELOG line whose in-repo relative markdown-link target does not resolve; FP-safe per a 10-case behaviour test; cross-repo/external/code-span excluded) and folded in the #933 cosmetic docstring-parallelism note; batches #933 QA. **§3.34 stays OPEN** for the ~23 historical-dangler cleanup (attended/fresh, careful per-link target fixes). **Next actions (overnight-safe):** §3.38 (broaden gate-39 count-idiom coverage, an analogous gate-logic widening + FP analysis + fixture) and §3.22 (fix D7's marker defeated by the #746 handoff restructure). **Deferred overnight:** §3.12 (new gate ripples the gate-count into the protected `.claude/` surface + high-touch), §3.73 (self-defers to fresh session), §3.34-historical (careful per-link fixes), and the egress/attended/source-gated/protected items. **Blocked / attended overnight (do NOT attempt unattended):** §2.15/§2.16 (attended-only website), §1.14 (egress), §1.1 (protected pack rule), §1.12 (gated on website work), §2.6 (maintainer console), source-gated annexes. Corpus-wide `/validate` + P1/P2 batch remain deliberately SKIPPED (crash-resume, not a QA-skipping handoff; `main` green 69/69). Green-at `09c3102` (#933) = 69/69. Standing cleanup: DRY the landing/pack contents-sidebar CSS. See [`session-handoff.md`](session-handoff.md) and [`overnight-pr.md`](overnight-pr.md) for the full state.

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
