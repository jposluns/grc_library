# AIQT findings loop (v1)

Version: 1.0.0 (plain semver; the AIQT release train assigns release versioning once it
exists)
Status: Phase-1 procedure; consumes the review contract (`review-contract.md`) and its
schemas. The reviewer POSTS findings; this document governs what the CONSUMING side
does with them. The `state:` annotation defined here is consumer-side bookkeeping and
is never part of the reviewer's posted schema.

## 1. Posture

A posted finding is a HYPOTHESIS, never an instruction. The consuming assistant
VALIDATES every finding against the live artefact before any action: re-read the cited
artefact, confirm the defect is present, real, and in scope, and only then act. The
loop is ADVISORY end to end: every terminal decision returns to the developer; nothing
here silently blocks a merge.

## 2. Lifecycle

One state per finding, annotated in the findings record:

    POSTED -> validate -> VALIDATED -> (AutoFix=On) -> FIXING(try n) -> RESOLVED(auto-fixed)
      |                      |                             |
      |                      |                             +- fail at n=3 -> ESCALATED(loud alert)
      |                      +- (AutoFix=Off) -----------------------------> ESCALATED(queued)
      +- validation refutes -> REFUTED (refutation recorded, never actioned)
      +- reviewed change gone -> WITHDRAWN (superseded; reason recorded)
    ESCALATED -> developer decides -> RESOLVED(fixed) | OVERRIDDEN(reason + revert path)

- POSTED: as delivered by the reviewer, schema-valid, unactioned.
- VALIDATED: re-derived against the CURRENT revision. A cited `path:line` is anchored
  to the reviewed revision; on drift the consumer re-anchors, or moves the finding to
  WITHDRAWN with the reason recorded.
- REFUTED: validation failed; the refutation (what was checked, why the finding does
  not hold) is recorded in place. A refuted finding is never silently dropped; the
  record is the audit trail.
- FIXING(try n): auto-fix path only, and the cap is the review contract's: up to 3
  repair tries on the same change, each attempt validated as targeting the SAME defect
  before it counts. Distinct findings carry distinct counters. A finding re-posted on
  a later change starts at n=1 with a link to its predecessor.
- Cross-run finding identity, for the counter: findings match across review runs on
  the same change by `ruleId` + `path`. The fingerprint's line component drifts as
  fixes land, so exact-fingerprint matching would reset counters and the cap alert
  could never fire. Residue, stated: `ruleId` + `path` can conflate two distinct
  same-class defects in one file; the validation step confirms same-defect linkage
  before incrementing, never trusting the key alone.
- ESCALATED at n=3 is the LOUD ALERT: the consumer stops fixing that finding and
  alerts the developer through the configured channel (`EscalationChannel`) with (a)
  the finding, (b) the three attempts and why each failed, and (c) named options:
  direct a fix / fix it yourself / merge anyway / override with a reason.
- OVERRIDDEN requires a recorded reason AND a revert path, and is re-surfaced at the
  next session start until acknowledged.

## 3. Where findings wait, and how they are found

- One record per review run, written by the LOCAL runtime (the session assistant or
  the local CLI): `.working/aiqt/findings/findings-<YYYYMMDD-HHMMSSZ>-<source>.md`
  (`source`: `ci-pr<N>`, `local-prepush`, `promotion`), carrying the run's SARIF-lite
  findings plus the per-finding `state:` line the consumer updates in place.
- One index: `.working/aiqt/findings/QUEUE.md`, one line per record file with state
  UNCONSUMED / CONSUMED / RESURFACE-DUE. Discovery is one read.
- Write boundary, stated: the review RUNTIME writes these operational records under
  `.working/aiqt/findings/`; the UPDATER never does (its sole write root stays
  `.working/aiqt/core/`, per the configuration format's write-boundary section).
  Records never alter guardrail content.
- A CI run's durable record TODAY is its workflow-artifact set plus the PR comment
  (the CI kit's evidence section); the local queue mirrors a CI run when a local
  assistant next engages with the change (import on next local engagement). It
  upgrades to direct queue writes when the local CLI ships its CI-import step.
- SESSION-START RULE: the consumer reads `QUEUE.md` FIRST at every AIQT session
  start; an UNCONSUMED entry blocks new work until it is read and every finding is
  dispositioned. Chat assistants without filesystem access carry the same rule as
  prose: before new work, ask for the findings queue.

## 4. Scheduled re-surface (no daemon)

Check-on-opportunity: every LOCAL AIQT entry point (session start, the wizard, the
doctor, a local review run) computes the age of every UNCONSUMED entry; older than
`ResurfaceDays` flips it to RESURFACE-DUE and the entry is raised to the developer
before new work. A repository with no activity has, by construction, nothing waiting
on its findings. The doctor's findings-queue check reports queue health on demand.
TODAY the CI lanes do not post reminder comments; that step upgrades into the kit
when the scheduled trigger class ships, with deduplication one reminder per full
window crossed, never one per run.

## 5. Decision points (advisory; the developer decides)

- MANUAL (`AutoFix=Off`), open validated findings at a merge or promotion point:
  "This change has N validated findings open (list). Fix the issues, or merge
  anyway? [fix / merge anyway / show findings]". Merging anyway records the choice
  on the change.
- AUTO-FIX exhausted (any finding at n=3): the loud alert replaces the routine
  prompt: "AIQT tried 3 fixes for finding F on this change and it still fails
  (attempts summarized). Direct a fix, fix manually, merge anyway, or override with
  a reason."
- AUTO-FIX, all resolved: no prompt; the record shows auto-fixed dispositions.

## 6. Configuration

Three knobs in `.working/aiqt/config.md`, catalogued in the configuration format
document: `AutoFix` (default On), `ResurfaceDays` (default 7), `EscalationChannel`
(default pr-comment). `AutoFix` governs FINDING REMEDIATION only; the per-guardrail
`AutoUpdate` column governs UPDATE CONSENT, a separate axis, so auto-fix-on is never
read as auto-update-on (the wizard states the distinction).

## 7. Phase boundaries

v1 ships the lifecycle, the queue formats, the session-start rule, the three knobs,
and the two prompt shapes. Deferred by design, each named where it lands: the CI
reminder step (the scheduled trigger class), queue-shape mechanical checks (the
logs-and-metrics and static-report items), cross-repo roll-up, any portal feed.
