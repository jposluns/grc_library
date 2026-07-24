# Session State (concurrency lease)

**Active-session:** claude/overnight-setup-1109

**Status:** active

**Operating-mode:** overnight-unattended

**Last-heartbeat-UTC:** 2026-07-24T00:37:00Z

**Current-task:** 2026-07-23b resumed session, now OVERNIGHT/unattended (the maintainer switched to overnight ~00:30Z 2026-07-24 and authorized the full overnight run; do not stop until they wake). On the VM, gh-CLI, no GitHub MCP. Both workers live Opus 4.8; MANDATORY-OFFLOAD active (offload every draft / research / QA pass to conserve orchestrator credits). SHIPPED this session: #1106 (resume close-out, Sweep 119 CLEAN), #1107 (§1.18 PR-2 gate 74 rule-scope-table completeness), #1108 (§1.1 the fifteenth pack rule `express-authorization-before-execution`). CURRENT PR #1109 = overnight setup (§1.18 close + the F1 date-breadcrumb fix + the overnight-authorizations record + this mode change + the #1108 QA rows). OVERNIGHT AUTHORIZATIONS (full block at `pending-decisions.md` top): all P3 (quick-clears + machinery) + the P2 AI annexes (Singapore 2.19, California 2.17) + the OWASP-Agentic 2.27 build are authorized; content mode = build-with-verifier / high-assurance-and-merge-on-green; §1.18 = close; no idle-stop, re-assess ALL of TODO for not-hard-blocked items if the queue drains; overnight ends ONLY on an explicit maintainer signal. QUEUE next: P3 quick-clears (3.94 / 3.60 / 3.38 / 3.13 / 3.47) -> broader P3 -> P2 annexes -> OWASP build. The Singapore 2.19 annex draft is already offloaded.

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
