# Session State (concurrency lease)

**Active-session:** none

**Status:** released

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-28T22:35:58Z

**Current-task:** SESSION CLOSED 2026-07-28b at #1231 (attended wind-down ~7h, maintainer-directed 7pm). Next: PR2b-2b (reword ALL .working prose + COMPLETE copy to _private, deferred to FRESH context), then PR2b-3 (delete public .working after no-pointers QA). See session-handoff.md next-actions.

**Worker-dispatches:** fleet spawned on-demand via `tools/exec-dispatch.py` (accounts in `_private/worker-accounts.json`). Concurrency-testing config (roadmap 2026-07-27): fallbacks `jposluns-work-claude` + `jeff-posluns-codex` at max 1; `security-work-claude`, `jeff-mailz-claude`, `jeff-posluns-claude`, `jeff-mailz-codex` at max 4 for aggressive testing. Short model names: claude opus/sonnet/haiku/fable; codex gpt-5.6-terra/sol/luna, gpt-5.5, gpt-5.4, gpt-5.4-mini. Order prompt MUST NOT start with `/`; codex dispatch needs `--model`.

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
