# Session State (concurrency lease)

**Active-session:** canada-egress-request-defer-222

**Status:** active

**Last-heartbeat-UTC:** 2026-07-16T18:04:07Z

**Current-task:** ACTIVE. The 2026-07-16 resumed session (`/resume` from #968, on the VM, gh-CLI). **Maintainer switched to UNATTENDED mode ~18:00Z for the next few hours** ("continue with everything you can do as long as quality holds and there's no degradation; two workers ready"). **Merged this session: #969-#974** (credit-offload phase-3 wiring; elevated-QA-window policy; Sweep 108 close-out [loop-break for #968 PASSED]; backlog §3.82/§3.83; design-of-record worker-allocation + reference-read models + §3.85). #973 was the first worker-sourced CORPUS apply (Quebec Law 25 penalty/PIA corrections, annex v1.1.3, every figure re-verified at the held source); its offloaded `/validate-pr` (worker-b, first QA delivery) was consumed under FULL elevated QA (adversarial auditor WORKER-CLEAN-CONFIRMED). **THIS PR (egress-request + §2.22 defer):** created [`maintainer-egress-requests.md`](maintainer-egress-requests.md) (the standing channel for egress-blocked sources the maintainer downloads to `grc_library_ref/ingest/`) listing the ~16 Canada.ca §2.22 instruments, and DEFERRED §2.22 (canada.ca blocks automated re-fetch, DD-10, confirmed 2026-07-16; maintainer will download fresh copies for the expert review) - tracked in `pending-decisions.md` + the TODO §2.22 status line. Also batches #974's `/retro` row + the §3.83 validate-before-deliver nit. **NEXT (currency-independent, unattended):** CCPA §2.23 apply (first test whether California/CCPA currency is fetchable, unlike canada.ca); ref-acquisition packages (EDPB/Brazil/LatAm inbox) -> `grc_library_ref` PR + rsync; ETSI §3.14 + GR-GAP-1 §3.15 apply-drafts; deferred-protected items 8/9/6. Repo-safety: confirm target repo before every write; keep `/tmp/grc_library_ref` in sync (rsync -av --delete, no -n) on any ref update.

**Worker-dispatches:** TWO workers this session (`worker-20260716-a`, `worker-20260716-b`; both VM, Opus 4.8, role `any`). `worker-20260716-a` VALIDATED earlier (Sweep 108 delivery 1 + validate-pr-969 delivery 2, both clean elevated; now stale/out, last_seen 17:04). `worker-20260716-b` LIVE; consumed clean under elevated QA: delivery 1 (`validate-pr-973`, zero findings, adversarial auditor WORKER-CLEAN-CONFIRMED) and delivery 2 (`validate-pr-974`, one REAL finding F1 = a design-doc claim-precedence overclaim I introduced in #974, re-verified at source + fixed in this PR), so **worker-b elevated-QA window = 2 of 2-to-3** (a correct finding is a sound pass, not a reset). One more clean elevated pass then relax to routine. Offloaded worker QA/research this session: Sweep 108, validate-pr-969, canada-ca-reference-breadth, canada-annexes-source-verification, canada-matrix-fit, ccpa-regs-2026-alignment, etsi + gr-gap-1 apply-drafts, 3 ref-acquisition orders, matrix-fit + claim-fit + screen-publications cadences, validate-pr-973, validate-pr-974. **Currently queued on scratch:** `reference-audit-canada-ccpa-newingest` (prio 3). Orchestrator-side validation subagents: verifiers on #969/#970/#973 + adversarial auditors on Sweep 108, the worker-lifecycle hooks (caught 2 real shared-VM concurrency bugs), and validate-pr-973 (WORKER-CLEAN-CONFIRMED); validate-pr-974's F1 re-verified at source. Note (worker-onboarding): worker-b's validate-pr-973 result prose carried house-style dashes that reddened scratch CI (fixed post-hoc); folded into §3.83 (add a pre-`deliver` validate.py step to `/credit-offload`).

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
