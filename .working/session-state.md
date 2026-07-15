# Session State (concurrency lease)

**Active-session:** claude/todo-permanent-numbering

**Status:** active

**Last-heartbeat-UTC:** 2026-07-15T02:05:51Z

**Current-task:** ACTIVE on branch `claude/todo-permanent-numbering` (resumed VM orchestrator session; ATTENDED-autonomous, green CI = merge authority). **The §2.4 website effort is live on grclibrary.ai and in a live-review loop with the maintainer.** Merged this session: the live-review round #921-#924, the adoption round #925-#926, close-out #927, and #928 (five-CTA hero, pack sidebar lists all 23 skills, Get-started cards match the page). **In flight, PR #929 (this branch):** the TODO permanent-numbering framework, item numbers never recycle, each priority section carries a `Next item number` counter (P1 1.15 / P2 2.17 / P3 3.76 / P4 4.29 / P5 5.10 / P6 6.6 / P7 7.6 after this PR's additions), plus four maintainer-confirmed backlog items recorded via the counters (§1.14 external-source currency mechanism, §2.15 standards-list source links, §2.16 two-level landing nav, §3.75 website-corpus link-integrity gate) and the batched #928 QA (SHIP-WITH-NOTES, one note fixed). **Next actions:** (a) PR-2, split the massive partially-done items (§2.4 / §2.5 / §3.57 / §3.68 / §3.62 / §3.63) so completed components rotate to DONE and only the remaining parts stay, each drawing fresh counter numbers; (b) build the confirmed website items §2.15 + §2.16; (c) the §1.14 / §3.75 machinery; (d) absorb any further maintainer site-review fixes. Remaining §2.4: watch-paths §2.6 (maintainer console) + the publish go; §2.4 stays OPEN until publish. Deferred: §1.12 (root CHANGELOG length remediation), after the website work. Corpus-wide `/validate` + P1/P2 batch remain deliberately SKIPPED (crash-resume, not a QA-skipping handoff; `main` green 69/69). Green-at `7479db5` (#928) = 69/69. Standing cleanup: DRY the landing/pack contents-sidebar CSS into the shared partial. See [`session-handoff.md`](session-handoff.md) for the full state.

**Worker-dispatches:** across the website effort each substantive PR ran a pre-push refute-briefed skeptical verifier plus a post-merge `/validate-pr` Subagent A, all read-only-git on the shared tree; verdicts SHIP or SHIP-WITH-NOTES with every finding fixed in-window (the only mediums: #922 dev-security dangling-colon intro, #925 a rule-description misstatement; internal notes: recurring build.py docstrings + lease-lag, all fixed). PR8 (#928) ran a pre-push skeptical verifier (SHIP, 0 material) and its post-merge `/validate-pr` returned SHIP-WITH-NOTES (Subagent A, one internal count note, fixed in #929). PR #929 (the numbering framework) runs its own pre-push skeptical verifier and batches the #928 QA. The `grc_library_scratch` inbox holds 15 pure-research seeds (11 PENDING + 4 UNMAPPED per `tools/audit-delivery-status.py`), all deliberately KEPT in the §3.58 disposition; unchanged this session.

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
