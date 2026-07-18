# Session State (concurrency lease)

**Active-session:** claude/119-8-relocate-living-docs

**Status:** active

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-18T15:52:01Z

**Current-task:** ACTIVE, 2026-07-18 resumed session (`/resume` from #1020; on the VM, gh-CLI, no GitHub MCP). Mode **attended-autonomous** (maintainer-set). Merged #1021-#1027 this session (Sweep-112 close-out; SEF-07; §1.20; §1.21; §1.19.12-lock #1025; protected bundle §1.15 CLOSED + QA-completion standard + §3.93 currency #1026; §1.19.12 review COMPLETE + maintainer-confirmed FINAL #1027). P1 CLOSED this session: §1.20, §1.21, §1.15. **#1028 IN FLIGHT: §1.19.8 RELOCATION** (19 living docs -> `grc_library_private` at `c2daf53`; 51 refs repointed + 16 public-CHANGELOG refs reworded to prose; D7 `runbook` version-token dropped; `fr48-deferred-worklist` deleted; corpus 72/72). Two pre-push adversarial verifiers + the /validate-pr on #1027 ran; all findings (4 missed overlay repoints, the "49"->51 accounting correction, 2 handoff/TODO strays, a stale draft count, 2 Low #1027 items) fixed in-window. **§1.19.8 stays OPEN**: the `_private`-INTEGRATION wiring (the `/resume` clone-if-absent + `--add-dir` provisioning, and the `tension-scan`/`residual-scan` `resolve_sibling` rewiring) is DEFERRED. **NEXT (maintainer-directed 2026-07-18, DO NOT IMPLEMENT before discussing):** assess ALL grc_library components/pointers that use or reference `_private` and propose minimizing/centralizing them (ideally ONE CLAUDE.md directive delegating to `_private`) - produce FOR DISCUSSION after #1028 merges. Then the deferred §1.19.8 wiring -> §1.19.9 -> §1.19.10 -> §1.19.11 -> Phase-5 CLAUDE.md trim (§1.19.12 apply) -> §1.19.13 (history scrub, LAST, maintainer-gated). **`pending-decisions.md`: none open.** **Standing:** present the per-priority TODO count table (Priority / Currently Open / Completed today / Added today) after every merged PR; sync scratch every PR before any credit-offload read (§3.93); explicit `cd /home/jposluns/<repo> &&` on cross-repo git; attended-autonomous mode is maintainer-set (changes only on their signal).

**Worker-dispatches:** both `worker-20260716-a`, `worker-20260716-b` (VM, Opus 4.8, role `any`). Trust is session-scoped, per-`(worker+model)`; the elevated window RE-ESTABLISHES this fresh session, so both start UNVALIDATED. **worker-a: 1 clean ELEVATED pass so far** (sweep-112-validate, delivery 1; proof-of-run genuine, mechanical facts independently re-derived MATCH, dedicated false-negative auditor dispatched); needs 2-3 clean elevated passes before routine. **worker-b: free, unvalidated this session** (0 passes). Registry quirk (§3.88): probe the order-file `status`, not the registry heartbeat, before declaring a stall (worker-a's registry heartbeat lagged the order heartbeat during sweep-112). Sync scratch `origin/main` AFTER a fetch before every coordination-plane read (§3.93).

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
