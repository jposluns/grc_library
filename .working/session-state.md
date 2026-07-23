# Session State (concurrency lease)

**Active-session:** claude/resume-sweep118-closeout

**Status:** active

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-23T15:17:36Z

**Current-task:** 2026-07-23 resumed session (`/resume` from the #1066 handoff; #1067 merged FIRST per its NEXT block, `main` now at #1067). On the VM, gh-CLI, no GitHub MCP. Opened ATTENDED (maintainer directing: resync repos, batch overnight decisions), then the maintainer set OVERNIGHT/unattended (~01:34Z "Go into overnight mode now") and went to sleep. At resume the GitHub credential was dead (401 on push / gh / sibling fetches); the maintainer added a new token and access was restored (all three siblings resynced; `/tmp/grc_library_ref` re-synced to `8126580` for the workers). **PLAN (maintainer-directed this session):** the INDEPENDENT TOOLING QUEUE (§1.22.3 `.working` cycle-out tool -> §1.22.4 cross-repo reference-existence tool -> §1.22.7 TODO Maintainer-or-Egress-Gated section -> §3.102 pack-distribute degradation-auto-handoff -> §1.16 COBIT guard-first), THEN clear as many P1/P3 QUICK-WIN items as possible to reduce the TODO count. **New content WAITS** (the new-`_ref`-ingest citation work is captured in §3.42 / RB-7 residual / §2.22 / §2.23, all deferred). Offload maximally (do not exhaust orchestrator credits); egress-blocked items go to `_private/maintainer-egress-requests.md`. First PR #0 = this resume close-out: Sweep 118 loop-break `/validate` (offloaded to a worker, over the #1067 delta), handoff prune, lease acquire, inbox-delivery cleanup (maintainer-directed).

**Worker-dispatches:** BOTH live Opus 4.8 (the maintainer spun up the second this session): `worker-20260716-a` (role any) + `worker-20260716-b` (role qa). worker-a claimed the blocking prio-0 `sweep-118-validate`; background research orders queued for worker-b: `research-1223-working-cycleout` (§1.22.3 seed, prio 2), `research-inbox-delivery-triage` (prio 2), `research-p1p3-quickclear-survey` (prio 3). Both workers' session-scoped elevated-QA windows RE-ESTABLISH this fresh session, so first deliveries are consumed under full ELEVATED QA. Fetch scratch `origin/main` before every coordination-plane read (§3.93); prefer `git -C <scratch>` (or an absolute script path) for sibling tools/git.

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
