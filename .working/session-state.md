# Session State (concurrency lease)

**Active-session:** claude/resume-sweep94-validate

**Status:** active

**Last-heartbeat-UTC:** 2026-07-10T16:13:13Z

**Current-task:** ACQUIRED at the sweep94 `/resume` (2026-07-10 UTC, ATTENDED-AUTONOMOUS on the NUC). Resumed cleanly from the released #760 lease (no live sibling branch inside the 60-min window). Session plan (maintainer-directed at this resume): (1) the loop-break corpus-wide **Sweep 94** `/validate` over the **#753..#759** window (mandatory first task); (2) then a maintainer-directed **log-mining pass** (review the improvement / hallucination logs, extract TODO-worthy improvements, assess each, populate TODO, add an "assessed-through" marker, propose cycling fully-mined old rows to scratch); (3) then the signed-off deep-assessment r1 actionable items (R1/R3/F3/F6/R8a small; R7 apply-directly PROTECTED, R2/R11/R12/R9/R10 delicate-at-scale). Green-at `4115ada` (#759) = 67/67 confirmed live at resume; HEAD #760.

**PRIOR (released):** the sweep93 `/resume` session (2026-07-10, DAYTIME ATTENDED-AUTONOMOUS then OVERNIGHT UNATTENDED on the VM) resumed from #752, ran the loop-break **Sweep 93** `/validate` (clean; the one out-of-window ADMT-gloss note fixed in #753), then ran the first-ever **`/deep-assessment` r1** end-to-end and the maintainer SIGNED OFF (0 errors / 7 warnings / 27 reference-breadth recs; 4 clear fixes + 13 routed; register row r1 = signed-off), recorded/routed in #754. Then a maintainer-directed **whole-TODO restructure** (#756) and the r1 clear/precision fixes: #755 F1 (jurisdiction count), #757 F12+§3.28 (EU AI Act citation sweep), #758 §3.26+§3.27 (claim-precision), #759 §3.24 (matrix GRC-07). All full per-PR QA, ZERO escaped defects. #760 (that handoff) batched #759's QA rows, refreshed the handoff, wrote the session-metrics row, and RELEASED the lease on a recorded degradation trigger (the §N-orphan cross-reference-bookkeeping class recurred 3x).

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
