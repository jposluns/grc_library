# Session State (concurrency lease)

**Active-session:** claude/takeover-reconcile

**Status:** active

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-26T13:51:11Z

**Current-task:** ORCHESTRATOR TAKEOVER 2026-07-26. A new orchestrator identity (the current maintainer account) took over from the prior session, which ran out of usage mid-work on #1181 during its 2026-07-25 overnight-unattended run (last live action about 01:33Z, a worker-nudge loop). The takeover ran read-only assessment first, then verified and landed the interrupted #1181 (the seven-lost-QA-rows ledger repair): pre-push guard green (78/78 plus all PR-time checks), and an INDEPENDENT adversarial worker verify (`verify-1181-ledger-repair`) confirmed nothing invented and nothing lost before merge. #1181 merged clean at `13861709` via `--admin` (logged). This PR (`claude/takeover-reconcile`, #1182) reconciles the takeover state: this lease, #1181's validate-pr / retro / bypass rows, the restored nudge-log, and one recorded finding (a destructive fail-open in `tools/sweep-working-records-to-private.py`, ROUTED TODO 3.129). Deferred queue (mostly staged worker candidates): Phase-3 tray processing (18 archive / 20 open / 10 route-to-maintainer per `reconcile-delivery-tray`), the `/restore-broken` command, TODO 3.128 + `/sitrep` (bundled), and the codex-`exec`-serve-loop (post-resume; design in `grc_library_private/codex-exec-serve-loop-decision.md`). Plan: reconcile, then build the deliverables, then a session-closing handoff, after which the maintainer resumes THIS session in a tmux via `/resume`.

**Worker-dispatches:** file-drop plane. LIVE: two Opus 4.8 workers, `opus-20260726T123931Z-f6b9` (worker1) and `opus-20260726T134016Z-5b06` (worker, restarted into a tmux session). Consumed this session and re-verified at source: `verify-1181-ledger-repair` (independent adversarial verify of #1181, CLEAN) and `reconcile-delivery-tray` (candidate tray classification). Codex family: all ids stale/out and HELD until the environment is confirmed clean (maintainer decision); the codex build is post-resume. The `worker_private_access` / `worker_scratch_access` toggles and `check_perms.sh` in `/home/grc` now enforce the worker-access permission model (workers read-only on the corpus, denied the shared `grc_library_scratch` and `grc_library_private`, read-write only on the `grc_working` exchange; `check_perms.sh --check` PASSES).

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
