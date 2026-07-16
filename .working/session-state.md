# Session State (concurrency lease)

**Active-session:** credit-offload-backlog-items

**Status:** active

**Last-heartbeat-UTC:** 2026-07-16T16:07:37Z

**Current-task:** ACTIVE. The 2026-07-16 resumed session (`/resume` from #968, on the VM, gh-CLI, attended-autonomous). Merged #969 (credit-offload phase-3 wiring) + #970 (elevated-QA-window policy codification). Credit-offload is LIVE, exercised end-to-end, and `worker-20260716-a` (Opus 4.8) is VALIDATED (Sweep 108 `/validate` + #969 `/validate-pr` both offloaded + delivered ~3 min + orchestrator-validated under elevated QA incl. a WORKER-CLEAN-CONFIRMED adversarial auditor). THIS PR (#971): the Sweep 108 close-out (records the sweep-108 history row, advances the cursor, prunes the handoff to keep #964-#967 + #955-#962, applies the 2 validated worker findings in TODO §3.80 [phase-1 date `2026-07-15`->`2026-07-16` UTC; add `verify` to the offloadable list], and batches #970's self-run `/validate-pr` + `/retro`). **CCPA ref-update tracking:** the maintainer added the CCPA statute (eff. 2026-01-01) to `grc_library_ref` (`ingest/`); a worker is ingesting it to full-text. At this close-out's post-merge ref-check, catch the landed full-text, resync `/tmp/grc_library_ref`, and QUEUE the CCPA currency+alignment offload order (TODO §2.23). NEXT after the close-out: scratch PR B (the 2 worker-lifecycle hooks + serve-loop self-refresh + worker-`model` field + Fable-5 capability scaffold [§3.82] + consume the winddown delivery), then deferred items 8/9/6, then Canada §2.22 + CCPA §2.23 on worker delivery. Repo-safety: confirm target repo before every write; keep `/tmp/grc_library_ref` in sync (rsync -av --delete, no -n) on any ref update.

**Worker-dispatches:** `worker-20260716-a` (VM, Opus 4.8, egress full-except-planalto-br) is LIVE and VALIDATED this session. **Elevated-QA window (first-session, keyed worker+model): 2 of the first 2-to-3 QA-kind deliveries done, both CLEAN** (Sweep 108 = delivery 1, full elevated incl. adversarial auditor; validate-pr-969 = delivery 2, graduated elevated); one more elevated pass (or relax to routine) then routine consume. Offloaded QA subagents this session: Sweep 108 `/validate` (worker ~237K), validate-pr-969 (worker ~54K); orchestrator-side validation: 1 skeptical verifier on #969 (~198K), 1 adversarial auditor on Sweep 108 (~219K). Pre-push skeptical verifiers stay orchestrator-side (§3.81). 5 pre-existing background orders remain on scratch (the 2 remaining Canada prio-1 after canada-ca-reference-breadth was claimed, 2 apply-drafting prio-2) plus the P4/P6 research-seed inbox deliveries (unchanged). #970's `/validate-pr` and this close-out's are SELF-RUN (the worker is on the maintainer's priority Canada + CCPA-ingestion work, so offloading process-PR QA behind it would starve that queue); self-run does not advance the QA-window count. The worker has since delivered `canada-annexes-source-verification` and claimed `canada-matrix-fit` (research-kind, outside the elevated QA window; validate-then-apply at §2.22). A worker is separately ingesting the CCPA statute into `grc_library_ref` (see Current-task CCPA tracking + TODO §2.23).

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
