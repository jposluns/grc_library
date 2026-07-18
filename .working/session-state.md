# Session State (concurrency lease)

**Active-session:** claude/119-8-minimization

**Status:** active

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-18T17:38:38Z

**Current-task:** ACTIVE, 2026-07-18 resumed session (`/resume` from #1020; on the VM, gh-CLI, no GitHub MCP). Mode **attended-autonomous** (maintainer-set). Merged #1021-#1028 this session (through #1028 = §1.19.8 RELOCATION: 19 living docs -> `grc_library_private`, 51 refs repointed, D7 runbook-token dropped, `fr48` deleted; two pre-push adversarial verifiers + offloaded validate-pr-1028 CLEAN). Then the maintainer directed the `_private`-pointer MINIMIZATION + a LAYERED fail-loud ASSURANCE (assessment written to `grc_library_private/private-minimization-assessment.md`; hybrid + maintainer-clone-if-absent APPROVED; layered-assurance Option C APPROVED; plan approved as-is: Part 0 -> PR 1 -> PR 2). **DONE:** Part 0 (`_private` under its own validate gate + CI + CLAUDE.md + INDEX; verifier-fixed a dead -ise-stem defect; closes §1.19.11, pushed `_private`-side). **#1029 MERGED (PR 1):** the layered assurance (detect-env `private_availability` HALT + `--self-test`; `/resume` acts on it; the `block-operational-without-private` PreToolUse Edit/Write hook + 7-case self-test, registered; pre-push-guard exit-4 refuse) + §1.19.11 rotation; verifier-cleared (NO bricking risk), offloaded validate-pr-1029 CLEAN (worker-a elevated). **#1030 IN FLIGHT (PR 2):** the hybrid minimization (ONE CLAUDE.md delegation directive -> `grc_library_private/INDEX.md`; ~20 CLAUDE.md + 4 overlay + 1 spec pointers collapsed to bare stems; 3 command one-line openers; read-evidence discipline) + §1.19.8 rotation to DONE + §3.100 recreate + the #1029 QA batch; corpus 72/72. **THIS CLOSES §1.19.8.** **NEXT (maintainer-directed 2026-07-18):** after §1.19.8 closes, OFFLOAD a DEEP-ASSESSMENT of the WHOLE §1.19.8 change-set (pinned to #1030's merge SHA; relocation + assurance + minimization + `_private` Part 0), consume under ELEVATED QA, WORK ANY FINDINGS AS TOP PRIORITY, surface to the maintainer (terminates on their sign-off). Then §1.19.9 -> §1.19.10 -> §1.19.12 apply -> §1.19.13 (gated). **`pending-decisions.md`: none open.** **Standing:** present the per-priority TODO count table after every merged PR; sync scratch every PR before any credit-offload read (§3.93); explicit `cd /home/jposluns/<repo> &&` on cross-repo git; attended-autonomous mode is maintainer-set (changes only on their signal).

**Worker-dispatches:** both `worker-20260716-a`, `worker-20260716-b` (VM, Opus 4.8, role `any`). Trust is session-scoped, per-`(worker+model)`; the elevated window RE-ESTABLISHES this fresh session, so both start UNVALIDATED. **worker-a: 2 clean ELEVATED passes this session** (sweep-112 delivery 1 + validate-pr-1029 delivery 2; both proof-of-run genuine, mechanical facts independently re-derived MATCH; 1 more clean elevated pass before routine). **worker-b: 1 clean ELEVATED pass** (validate-pr-1028 delivery 1; proof-of-run genuine, re-derived MATCH, corroborated by the pre-merge adversarial verifiers; needs 2 more before routine). Registry quirk (§3.88): probe the order-file `status`, not the registry heartbeat, before declaring a stall (worker-a's registry heartbeat lagged the order heartbeat during sweep-112). Sync scratch `origin/main` AFTER a fetch before every coordination-plane read (§3.93).

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
