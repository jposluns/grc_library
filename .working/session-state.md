# Session State (concurrency lease)

**Active-session:** none

**Status:** released

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-17T11:14:14Z

**Current-task:** ACTIVE. The 2026-07-16c resumed session (`/resume` from #984, on the VM, gh-CLI, no GitHub MCP); maintainer now ATTENDED and steering closely (mode `attended-autonomous`). **MERGED this session:** #985-#989 (Sweep-109, QA-consume, §3.61 delivery-status, §2.22-A2, and #989 = the D8 CHANGELOG-length gate + r4 consume + §1.18 surface-map). **THIS PR (#990, `claude/mistake-prevention-fixes`):** the two maintainer-chosen mistake-prevention fixes for the session's flagged errors, plus the #989 QA batch. **Mistake 2 (A):** `tools/ref-holds.py` forcing-function tool (held/not-held from the ref INDEX, quoted, never a partial grep; the ISO-27002 error) + the executed-not-narrated rule in CLAUDE.md. **Mistake 1 (both):** a `**Operating-mode:**` field in this file (gate-63-validated) + a PreToolUse hook `block-askuserquestion-unattended.py` that blocks `AskUserQuestion` in unattended mode (the 7h-idle AskUserQuestion error) + the CLAUDE.md mechanical-backstop rule + gate-63 test fixtures + the spec §6 gate-63 prose. Also fixes validate-pr-989's NOTE-1 (the r4 W2 paired-surface lag). **NEXT (maintainer priority order):** (1) the `.working` relocation to `grc_library_private` (PAUSE for the low-scroll `_private`-move design discussion FIRST, maintainer-requested); (2) assess anything else to move to `_private`; (3) the deferred history scrub (last). Also queued: §1.12 CHANGELOG remediation (compress ~25 drifted root entries; D8 now guards new ones), §1.16 COBIT title normalize + gate, §1.18 surface-map, r4 Phase-8 sign-off (HOLDS). Repo-safety: read `origin/main` via `git show origin/main:<path>`; explicit `cd` on cross-repo git; `grc_library_private` clone at `/home/jposluns/grc_library_private` (direct push works).

**Worker-dispatches:** TWO workers this session (`worker-20260716-a`, `worker-20260716-b`; both VM, Opus 4.8, role `any`). Trust is session-scoped, per-`(worker+model)` elevated window. **`worker-20260716-b`: GRADUATED to routine trust** (3 clean elevated passes): `sweep-109-validate-2` (d1 PASS), `deep-assessment-r4-continuation` (d2, findings re-verified at source), `validate-pr-989` (d3 PASS, caught the real NOTE-1 W2 paired-surface lag). Clones from GitHub. **`worker-20260716-a`: elevated window RESET** on the validate-pr-987 d3 miss (N1 enumeration undercount 32/25 vs true 35/28; escalated); its FIRST post-reset delivery `validate-pr-988` was a **PASS** (1 of 2-3 toward re-establishing routine; caught the real P3-counter defect), so worker-a is at 1 clean post-reset, still ELEVATED. Both check in ~5-min (staggered). Registry quirk: worker `workers/`-entry heartbeats lag the order-claim heartbeats (a worker refreshes its order heartbeat but its registry entry can read `stale/out`), and there is no stale-entry auto-prune (§3.88); the availability gate keys on the fresh signal, so this is hygiene, not correctness.

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
