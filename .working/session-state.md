# Session State (concurrency lease)

**Active-session:** claude/canada-2226-agentic

**Status:** active

**Last-heartbeat-UTC:** 2026-07-17T10:04:43Z

**Current-task:** ACTIVE. The 2026-07-16c resumed session (`/resume` from #984, on the VM, gh-CLI, no GitHub MCP), now overnight-unattended. **THIS PR (#988, `claude/canada-2226-agentic`):** §2.22 first bite (A2, the TBS Guide on the Use of Agentic AI sector-neutral comparator row in `ai/standard-ai-access-and-agent-permissions.md`, standard 0.0.9->0.0.10) + the #987 QA batch (validate-pr-987 SHIP row + #987 retro row) + design/backlog records: the local-VM exchange-transport design (`design-decisions.md` + new TODO §3.87, resolves §3.85), and TODO §1.16 (COBIT title normalization + title-text gate) routed from validate-pr-987 N1. **Worker-a elevated-window RESET this PR:** validate-pr-987 was worker-a's delivery-3 (was 2/2-3); its in-window SHIP verdict was independently re-derived correct, but the elevated-QA mechanical re-derivation caught a CONFIRMED MISS (its out-of-window N1 enumeration undercounted 32/25 vs the true 35/28), so worker-a does NOT graduate to routine, stays under elevated scrutiny, and the miss is ESCALATED to the maintainer. **NEW maintainer directive (2026-07-17, TOP of queue):** root CHANGELOG entries drifted long again (~PR 950+); remediate them to the short compact form AND harden the generation/guard so it stops recurring ("fix it so it doesn't break again"). This is §1.12 (P1), now actively directed; it is the IMMEDIATE next PR after #988. **THEN:** the COBIT title normalization + gate (§1.16), the deep-assessment r4 continuation (worker B running it now), the P3-triage decision application, §2.22 continuation, item-1 worker-hardening (when workers idle). Repo-safety: read `origin/main` via `git show origin/main:<path>`; prefix cross-repo git/greps with explicit `cd`; keep `/tmp/grc_library_ref` synced on any ref update.

**Worker-dispatches:** TWO workers this session (`worker-20260716-a`, `worker-20260716-b`; both VM, Opus 4.8, role `any`). Trust is session-scoped, per-`(worker+model)` elevated window. **`worker-20260716-b`:** delivered `sweep-109-validate-2` (Sweep 109), delivery-1 = **PASS** (re-derivation exact-match + adversarial auditor clean); now running `deep-assessment-r4-continuation`. Clones from GitHub. **`worker-20260716-a`** (mirror refreshed by the maintainer, now reaches #987): delivered `validate-pr-985` (d1 **PASS**) and `validate-pr-986` (d2 **PASS**), then `validate-pr-987` (d3) which the elevated-QA re-derivation found had a **CONFIRMED MISS** (N1 enumeration undercounted 32/25 vs true 35/28). Per the discipline the miss **RESETS worker-a's elevated window** (does NOT graduate to routine; back to 0 clean toward the 2-3 floor), keeps it under elevated scrutiny for the rest of the session, and is **ESCALATED to the maintainer**. The in-window verdicts of d1/d2/d3 were all independently re-derived correct; the reset is for the d3 out-of-window enumeration miss, not a wrong verdict. Both workers check in on a ~5-minute interval (staggered 5/N).

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
