# Session State (concurrency lease)

**Active-session:** 2026-07-08-fr63-adoption-worked-example

**Status:** active

**Last-heartbeat-UTC:** 2026-07-08T04:56:57Z

**Current-task:** OVERNIGHT (2026-07-08; maintainer switched to overnight mode "I'm going to sleep. Swap to overnight mode"). This session merged #693 (reference-information cleanup, `/full-qa`'d) and #694 (the `/full-qa` follow-up fixes), then is building the maintainer-directed **changelog-restructure** (current-week model: detailed mirror + records keep the current week in-repo, completed weeks swept to `grc_library_scratch` weekly Monday-dated archives; root kept full but compressed to the compact 1-2-sentence format; `.gitattributes export-ignore` on `.working/`). Sequenced PR 1 machinery (gate-59 dynamic cutoff + sweep tool + export-ignore + docs, no data moved) -> PR 2 the data-safe sweep + per-PR step -> PR 3+ root reformat/compress. Protected-file edits (change-tracking rule/skill, CLAUDE.md) staged in [`deferred-protected-changes.md`](deferred-protected-changes.md). After the restructure: the egress-prioritized queue. HISTORICAL: ACTIVE (acquired at `/resume` step 0 on the maintainer's NUC; prior lease `released`, no live `origin/claude/*` siblings, git cross-check clean). Mode: **DAYTIME-UNATTENDED** (maintainer reachable, glanceable periodically; green CI = merge authority; no idle-stop; stricter-is-safer; graceful-degradation defers/skips authorial/irreversible decisions; NOT overnight, so no skip-to-morning / no overnight-off protection). Environment re-verified: local Linux NUC, `gh` CLI (no GitHub MCP), egress available, NO stop-hook auto-commit-push (commit and push manually), the pipe-guard PreToolUse hook DOES fire here. First PR (#687, this close-out): ran **Sweep 88** (loop-break corpus-wide `/validate` over the #685..#686 deltas, PASSED: 2 out-of-window low-severity findings both fixed this PR, no asserted-expectation contradiction), fixed **TODO 1.12** (annual-review procedure architecture domain), pruned + reconciled the handoff to daytime-unattended and the reference-library split (scratch -> scratch + `grc_library_ref`). Queue after this PR: the reference-library split (3a additive populate `grc_library_ref`, then a CHECKPOINT for maintainer go-ahead before the cutover 3b); then the fast-follow ref schema + citation-not-embed gate + forkability note; then (post-cutover, with egress) the egress-gated 1.5/1.11/GR-GAP-1/SR-1 + the 11 legislation deepenings; the split-independent non-legislation queue (FR-63, 3.16/3.17, small P3/P4) is the fallback while the checkpoint holds. PRIOR (historical): `claude/grc-acquisition-reconfirm-brief-k8fppo` shipped #685 (Sweep-87 close-out) + #686 (session-closing handoff, NUC transfer) and released the lease at #686.

**Worker-dispatches:** the external worker session (maintainer-launched 2026-07-03, read-only-on-main) DELIVERED all 30 staged work-units plus the read-only QA report (all merged scratch-side; the deliveries sit in the scratch inbox, fr-59 half-consumed). Applied so far: FR-99/#681, FR-15/#682, FR-23/#683 (by `claude/resume-chptc7`); the k8fppo session applied none. The remaining scratch-inbox applies (FR-63 and the rest, serial validate-then-apply, full per-PR QA) are queued on this NUC session after the reference-library split. The wave-7 staged pool (2 briefs: corpus-skill distillation, GR-GAP-1 register population) remains available for pickup.

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
