# Session State (concurrency lease)

**Active-session:** claude/resume-sweep119-closeout

**Status:** active

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-23T21:10:29Z

**Current-task:** 2026-07-23b resumed session (`/resume` from the #1105 session-closing handoff; `main` at #1105 `7803d388`, 73/73). On the VM, gh-CLI, no GitHub MCP. Opened ATTENDED (maintainer sent `/resume`). Both workers live Opus 4.8; mandatory-offload active. First PR = this resume close-out: Sweep 119 loop-break `/validate` (OFFLOADED to a live worker, over the #1068..#1104 deltas, base #1067 `3ceb0c54`), handoff prune (keep current + 1 prior), lease acquire. Then the maintainer-directed queue per the #1105 NEXT block: §1.18 PR-2 (the FP-safe pack-README rule-scope-table gate, guard-first), the 1.1 discussion-vs-execution gate DESIGN (author + bring to maintainer, do NOT auto-build), the P2 2.19 Singapore + 2.17 California annexes (research delivered), then P2 by severity + P3. OPEN maintainer alert 2026-07-23-a (LOW, SHA-pinning practice) to surface + ask about clearing; OPEN pending decision OWASP §36 ASI08/09/10.

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
