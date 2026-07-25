# Session State (concurrency lease)

**Active-session:** none

**Status:** released

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-25T02:21:49Z

**Current-task:** RELEASED at the #1150 session-closing handoff (2026-07-24/25 worker-wiring / file-drop-transport session; maintainer-directed ASAP wind-down once file-drop readiness was verified). The next `/resume` runs from `/home/grc/grc_library` (PATH MIGRATION: all sibling repos relocate to `/home/grc/`, off `/home/jposluns`) and must UPDATE ALL `/home/grc` repos first, then run the Sweep 120 loop-break `/validate` over #1106..#1150. File-drop transport is LIVE (workers restart onto `/home/grc/grc_working` via the transport-aware `/credit-offload`; the orchestrator dispatches via `credit-offload-filedrop.py dispatch` and consumes from `outbox/`). See the session handoff NEXT SESSION block for the full queue.

**Worker-dispatches:** opus `worker-20260716-a` + `worker-20260716-b` (Opus 4.8) and the new Codex `codex-mailz-a` (family codex, role any). At close, `worker-20260716-a` and `codex-mailz-a` were heartbeating via the file-drop transport. PENDING CONSUME next session: `validate-pr-1149` (git-scratch `_scratch` `results/`) and `fd-verify-1149-deepassess` (file-drop `codex/outbox`); re-verify positives at source. MANDATORY-OFFLOAD active; the file-drop transport is now the same-VM path (git-scratch is the cross-VM fallback).

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
