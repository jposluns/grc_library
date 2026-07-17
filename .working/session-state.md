# Session State (concurrency lease)

**Active-session:** claude/delivery-status-coded-id

**Status:** active

**Last-heartbeat-UTC:** 2026-07-17T01:58:42Z

**Current-task:** ACTIVE. The 2026-07-16c resumed session (`/resume` from #984, on the VM, gh-CLI, no GitHub MCP). Attended-autonomous at the start (maintainer present, then stepping out for ~1h, then overnight). **THIS PR (the Sweep 109 close-out)** = the loop-break corpus-wide `/validate` (Sweep 109, over #969..#984), OFFLOADED to `worker-20260716-b` and orchestrator-validated under ELEVATED QA (worker B first QA-kind delivery this session: mechanical facts re-derived EXACT-MATCH + adversarial false-negative auditor NO-MISSED-FINDING; **PASS**, 1 of 2-3 clean passes). Worker B's sweep found 0; the elevated-QA auditor surfaced 1 note (`S109-N1`: US privacy annex section 7120 cyber-audit threshold parenthetical omitted the section 7120(b)(1) revenue trigger + the (b)(2) section 1798.140(d)(1)(A) conjunct), verified at held source and FIXED in-window (annex 1.2.3->1.2.4). This PR also prunes the handoff (dropped the 2026-07-15 #955-#962 stack), advances the sweep cursor, and ACQUIRES this lease. **Maintainer directives this session (codified in `grc_library_scratch`):** (1) workers resync-CHECK the pinned grc_library SHA when picking up a task (deliver BLOCKED rather than run against a stale SHA); (2) stagger worker check-ins at 5/N-min offsets across N live workers. **Offload note:** worker B clones from GitHub (self-serviceable); worker A clones from the stale local mirror `/home/worker/grc_library` (#968), which needs a maintainer/worker-side refresh before worker A can serve #984-pinned corpus orders (surfaced to the maintainer). **NEXT (pre-loaded, maintainer-authorized unattended queue):** (A) the worker-process-improvement brief (item 1 F1/F2 fixes first: the vacuous-test rewrite + the unpushed-commit-lost-on-rerun path, delicate git logic, skeptical verifier; then items 2/4/5/3/6/7); (B) the section 2.22 Canada CORPUS apply (apply-everything-with-verifier); (C) the 3 AI-annex seeds (high-assurance, merge unattended); (D) ETSI section 3.14; (E) P6 section 6.1/6.4/6.5; (F) the deferred-protected backlog; (G) the r4 deep-assessment continuation (phases 3/4b-d/5/6, enqueue after section 2.22). Repo-safety: read `origin/main` via `git show origin/main:<path>` (not a stale working-tree read after a bare fetch); prefix cross-repo git/greps with explicit `cd`; keep `/tmp/grc_library_ref` synced on any ref update.

**Worker-dispatches:** TWO workers this session (`worker-20260716-a`, `worker-20260716-b`; both VM, Opus 4.8, role `any`). Trust is session-scoped and re-established this fresh session (per-`(worker+model)` elevated window). **`worker-20260716-b`:** delivered `sweep-109-validate-2` (the loop-break Sweep 109), its FIRST QA-kind delivery this session, consumed under ELEVATED QA = **PASS** (1 of 2-3 clean elevated passes; re-derivation exact-match + adversarial auditor clean). Clones from GitHub, reaches #984. Now free. **`worker-20260716-a`:** UNVALIDATED this session (0 elevated passes); clones from the stale mirror `/home/worker/grc_library` (#968), cannot serve #984-pinned corpus orders until its mirror is refreshed. Treat any worker-a QA-kind delivery under the ELEVATED window. Both workers check in on a ~5-minute interval (staggered 5/N per the new codification).

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
