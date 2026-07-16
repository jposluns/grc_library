# Session State (concurrency lease)

**Active-session:** none

**Status:** released

**Last-heartbeat-UTC:** 2026-07-16T11:16:48Z

**Current-task:** RELEASED. The 2026-07-16 resumed session (`/resume` from #963, on the VM, gh-CLI) closed at the session-closing handoff PR #968; the lease is released for the next session to `/resume`. The session ran attended-autonomous, then a long attended credit-offload co-design, then an overnight window, then a morning wind-down at the maintainer's signal. Merged: #964 (Sweep 107 `/validate` close-out; loop-break for #963 PASSED), #965 (task-1 AICM close-out: already fixed #939, re-verified), #966 (credit-offload design of record + backlog §1.15/§3.80/§3.81 + phase-3 staging + #965 QA), #967 (Canada.ca reference-utilization §2.22 + #966 QA + 2 design-doc note fixes). Cross-repo `grc_library_scratch` #166-#170 (credit-offload phase 1-2 build + the Canada/ETSI/GR-GAP-1 credit-offload seeds; 5 orders queued). **NEXT SESSION (maintainer-directed 2026-07-16): after the mandatory resume activities (Sweep 108 `/validate` over #964..#968), the FIRST substantive task is credit-offload PHASE 3, and the FIRST step of that is to ASK the maintainer about [`deferred-protected-changes.md`](deferred-protected-changes.md) item 10 (the staged phase-3 wiring for `/resume` + `.claude/CLAUDE.md`) and surface any decisions BEFORE applying.** Then: Canada.ca §2.22 apply on worker delivery (Canada-priority), P1 (§1.12/§1.14/§1.1), P3. A worker can be checked in per `grc_library_scratch`'s `WORKER-ONBOARDING-credit-offload.md` (5 orders queued, 3 Canada priority-1). Repo-safety: confirm target repo before every write. Lease released.

**Worker-dispatches:** the Sweep 107 `/validate` (A/B/C) and a `/validate-pr` Subagent A on each of #964-#967 ran read-only; all findings re-verified by the orchestrator at apply time. No substantive-PR skeptical verifiers this session (working-state/design/backlog/scratch tier). The credit-offload build stocked `grc_library_scratch` with 5 queued orders (3 Canada priority-1: `canada-ca-reference-breadth`, `canada-annexes-source-verification`, `canada-matrix-fit`; 2 apply-drafting priority-2: `etsi-en304223-option3-apply-draft`, `gr-gap-1-gate-draft`) for tomorrow's `/credit-offload` workers, plus the pre-existing P4/P6 research-seed inbox deliveries (unchanged).

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
