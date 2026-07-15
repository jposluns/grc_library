# Session State (concurrency lease)

**Active-session:** claude/matrixfit-aicm-guideline

**Status:** active

**Last-heartbeat-UTC:** 2026-07-15T10:01:25Z

**Current-task:** ACTIVE, ATTENDED, winding down toward a morning session on branch `claude/matrixfit-aicm-guideline`. The maintainer returned attended (2026-07-15 ~10:00Z), directed the AICM matrix-fit + corrections, answered the pending decisions, and asked for a wind-down to a fresh morning session. **Merged this session through #938** (`main` green at `4f4b5e4`; run: #929 numbering framework, #930-#932 split wave, #933 gate-69 widening, #934 preflight link-check, #935 protected-machinery staging, #936 resting-point, #937 §3.10 fence-predicate consolidation, #938 batch+route). **Maintainer decisions applied this turn (ride PR #939):** (1) §3.43 AICM matrix-fit: the 7 fabricated `AI-*-NN` codes in `dev-security/guideline-ai-coding-assistant-security.md`'s CSA AICM column remapped to real AICM v1.1.0 codes (GRC-09 / DSP-07 / AIS-10 / AIS-15 / AIS-11 / TVM-13 / SEF-08), maintainer-approved, gate 48 clean; (2) §3.47 rescoped (keep `(was X.Y)` per #929, strip the rest; still attended-preferred, queued); (3) §3.8 CLOSED keep-as-is (no gate-31/40 subprocess batching; correctness over speed). **Domain-page ordering (maintainer-chosen): source + type-priority sort** = change `build-taxonomy.py` to order docs by (domain, type-reading-rank, title) not alphabetical path, then regenerate taxonomy + portal + scorecard; TO IMPLEMENT as PR #940. **Wind-down PR plan:** #939 (AICM fix + §3.47/§3.8 records + #938 QA batch), #940 (taxonomy type-priority ordering + regen), #941 (session-closing handoff: full handoff / asserted-expectations / session-metrics refresh, RELEASE the lease, exempt from the trailing /validate-pr per the handoff loop-break; the next /resume's corpus-wide /validate is the compensating control). **Batched QA in flight:** #937's /validate-pr row shipped in #938; #938's /validate-pr (SHIP-WITH-NOTES, 2 cosmetic notes fixed) + /retro rows ride #939. Green-at `4f4b5e4` (#938) = 69/69.

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
