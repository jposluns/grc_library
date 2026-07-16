# Session State (concurrency lease)

**Active-session:** claude/credit-offload-worker-qa-policy

**Status:** active

**Last-heartbeat-UTC:** 2026-07-16T14:46:31Z

**Current-task:** ACTIVE. The 2026-07-16 resumed session (`/resume` from #968, on the VM, gh-CLI, attended-autonomous). Merged #969 (credit-offload phase 3 wiring). The credit-offload machine was EXERCISED and the worker VALIDATED: the mandatory Sweep 108 `/validate` (#964..#968) and the #969 `/validate-pr` were both OFFLOADED to `worker-20260716-a` (Opus 4.8) and delivered in ~3 min; the orchestrator validated delivery 1 (Sweep 108) under full ELEVATED QA (independent re-derivation of SHAs/counts/gate-54/pre-flight, all exact-match + a WORKER-CLEAN-CONFIRMED adversarial false-negative auditor) and delivery 2 (validate-pr-969) under graduated elevated QA. Sweep 108 = 0 error / 0 warning / 1 note (phase-1 date drift); validate-pr-969 = 1 note (`verify` enum drift); the worker also caught a real orchestrator error (a SHA-field typo in the validate-pr order). Loop-break control for #968 PASSES. THIS PR (#970): codifies the elevated-QA-window policy (maintainer-directed: reset per session, QA-kind only, keyed on worker+model, floor-not-cap, graduated auditor) in `.claude/CLAUDE.md` + the design-of-record, and batches #969's offloaded-and-validated `/validate-pr` + `/retro` rows. NEXT: the Sweep 108 close-out PR (record the sweep row + advance cursor + prune handoff + apply the 2 worker findings in TODO §3.80), then scratch PR B (the 2 worker-lifecycle hooks + serve-loop self-refresh + worker-`model` field + capability scaffold + consume the winddown delivery), then deferred items 8/9/6. Repo-safety: confirm target repo before every write; keep `/tmp/grc_library_ref` in sync (rsync -av --delete, no -n) on any ref update.

**Worker-dispatches:** `worker-20260716-a` (VM, Opus 4.8, egress full-except-planalto-br) is LIVE and VALIDATED this session. **Elevated-QA window (first-session, keyed worker+model): 2 of the first 2-to-3 QA-kind deliveries done, both CLEAN** (Sweep 108 = delivery 1, full elevated incl. adversarial auditor; validate-pr-969 = delivery 2, graduated elevated); one more elevated pass (or relax to routine) then routine consume. Offloaded QA subagents this session: Sweep 108 `/validate` (worker ~237K), validate-pr-969 (worker ~54K); orchestrator-side validation: 1 skeptical verifier on #969 (~198K), 1 adversarial auditor on Sweep 108 (~219K). Pre-push skeptical verifiers stay orchestrator-side (§3.81). 5 pre-existing background orders remain on scratch (the 2 remaining Canada prio-1 after canada-ca-reference-breadth was claimed, 2 apply-drafting prio-2) plus the P4/P6 research-seed inbox deliveries (unchanged).

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
