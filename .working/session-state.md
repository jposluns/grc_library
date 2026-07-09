# Session State (concurrency lease)

**Active-session:** claude/resume-sweep91-validate

**Status:** active

**Last-heartbeat-UTC:** 2026-07-09T05:45:33Z

**Current-task:** ACQUIRED at the `/resume` from session-closing OVERNIGHT-SWAP handoff #720 (prior lease `released`, no live `origin/claude/*` sibling inside the 60-minute window; the recent sibling commits are #720's own now-merged branches, HEAD `ca33c49`). This is the **OVERNIGHT BACKLOG RUN** (maintainer-directed 2026-07-09, on the local NUC `nuc125h-a`; protected-apply AUTHORIZED because local-instance). Environment: local NUC, `gh` CLI (no GitHub MCP), `CLAUDE_CODE_CHILD_SESSION` set BUT the PreToolUse pipe-guard hook DOES fire here (the NUC harness resolves the hook path even with `CLAUDE_PROJECT_DIR` unset; the earlier acquire-time note that it does not fire was wrong and is corrected across the session records); run verification unpiped by habit either way. **Progress:** shipped #721 (Sweep-91 close-out, loop-break `/validate` clean), ref #29 + #722 (2.11 + SR-2), #723 (3.21), #724 (3.18), #725 (GR-P1 13th rule), #726 (GR-P2 tranche 1, tranches 2-12 HELD), #727 (GR-P3/4/5a), ref #30 (SR-3), all with full per-PR QA and zero escaped findings. **Current PR #728:** SR-3 grc_library-side close + TODO 3.20-B1 pack cross-reference + batched #727 QA rows. The readily-applicable backlog is now essentially exhausted (remaining items HELD/egress-blocked/authorial); the last non-blocked work is the scratch-side coverage-refresh sync + fragments, then the session-closing handoff. Autonomy = fix + route + APPLY protected `.claude/`/pack edits (LOCAL-INSTANCE) + stricter-safe defaults + NO idle-stop; full per-PR QA never abbreviated; green CI = merge authority. Run the #716 START-side check before each item.

**Worker-dispatches:** the Fable worker (`worker-20260708-fable`) applied so far: `deep-assessment-build` (#701/#702), `aiqt-codification` (#705/#711/#712, scratch `CLAUDE.md` one-liner still owed), `reference-audit-build` (#706/#707), `resume-pointer` (#715). The START-side check at this resume found MANY further Fable/Opus deliveries staged as UNMERGED scratch PR branches, to apply this overnight run: `pubscreen-delivery` (2.11), `claimfit321-delivery` (3.21), `envdetect-delivery` (3.18), `grp2-delivery` + `worker/gr-p2-tranche{2,3,4}` (GR-P2), `grp345-delivery` (GR-P3/4/5), `lifecycle-delivery` (GR-P1), `sr3-delivery` (SR-3), `rootlog-delivery` (3.19 root reformat), plus `refacq-delivery`/`adopter-delivery` (already applied #718/#719). **Status change vs the handoff:** `worker/etsi-sai-crosswalk-316`, `worker/fix-etsi316-bare-ensure`, and `worker/atlas-crosswalk-317` delivery branches now EXIST (Fable delivered 3.16/3.17 since the handoff was written), so they move from "in-flight, do not touch" into the apply queue at lower priority (verify delivery completeness before applying). The scratch `claims-ledger.md`/`COVERAGE.md` on scratch `main` are STALE (claim rows for the newer deliveries live on the unmerged `fable-claims-batch{,2,3}` branches); the coverage-refresh sync stays queued. The earlier external worker session (2026-07-03) delivered 30 staged work-units; applied: FR-99/#681, FR-15/#682, FR-23/#683, FR-63/#697; the FR-59/60/74/154/41/DORA/NIS2 research files remain to author.

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
