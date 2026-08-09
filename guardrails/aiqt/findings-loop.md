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
                             |                             |
                             |                             +- fail at n=3 -> ESCALATED(loud alert)
                             +- (AutoFix=Off) -----------------------------> ESCALATED(queued)
                             +- validation refutes -> REFUTED (refutation recorded, never actioned)
                             +- reviewed change gone -> WITHDRAWN (superseded; reason recorded)
    ESCALATED -> developer decides -> RESOLVED(fixed) | OVERRIDDEN(reason + revert path) -> ACKNOWLEDGED

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
  could never fire. Two residues, both stated: (a) `ruleId` + `path` can conflate two
  distinct same-class defects in one file; (b) `review-contract.md` requires `ruleId`
  stable only WITHIN a review, so two runs (possibly different pinned models) may label
  the same defect class differently and reset its counter. The validation step confirms
  same-defect linkage before incrementing, never trusting the key alone, which bounds
  both residues; a future contract revision may promote `ruleId` to cross-run stability.
- ESCALATED at n=3 is the LOUD ALERT: the consumer stops fixing that finding and
  alerts the developer through the configured channel (`EscalationChannel`) with (a)
  the finding, (b) the three attempts and why each failed, and (c) named options:
  direct a fix / fix it yourself / merge anyway / override with a reason. The alert
  ALWAYS lands: when the configured channel has no destination for the run (a
  `pr-comment` channel on a `local-prepush` or `promotion` source, which has no PR),
  the consumer FALLS BACK to the console, so a local finding that exhausts its tries
  is never silently dropped.
- OVERRIDDEN requires a recorded reason AND a revert path, and is re-surfaced at the
  next session start until the developer ACKNOWLEDGES it; acknowledgement is the
  terminal queue state (`ACKNOWLEDGED`, section 3) that stops the re-surfacing.

## 3. Where findings wait, and how they are found

- One record per review run, written by the LOCAL runtime (the session assistant or
  the local CLI): `.working/aiqt/findings/findings-<YYYYMMDD-HHMMSSZ>-<source>.md`
  (`source`: `ci-pr<N>`, `local-prepush`, `local-review`, `promotion`), carrying the run's SARIF-lite
  findings plus the per-finding `state:` line the consumer updates in place.
- One index: `.working/aiqt/findings/QUEUE.md`, one line per record file. The PERSISTED
  state is `UNCONSUMED`, `CONSUMED`, or `ACKNOWLEDGED` (the terminal state for a record
  whose overrides the developer has acknowledged). `RESURFACE-DUE` is a DERIVED view, an
  `UNCONSUMED` record older than `ResurfaceDays`, computed at read time and never
  persisted, so surfacing it requires no write (section 4). A record is `CONSUMED` only
  when every finding it carries has reached a terminal disposition (RESOLVED / REFUTED /
  WITHDRAWN / OVERRIDDEN-then-ACKNOWLEDGED). Discovery is one read.
- Write boundary, stated: the review RUNTIME writes these operational records under
  `.working/aiqt/findings/`; the UPDATER never does (its sole write root stays
  `.working/aiqt/core/`, per the configuration format's write-boundary section).
  Records never alter guardrail content.
- A CI run's durable record TODAY is its workflow-artifact set plus the PR comment
  (the CI kit's evidence section); the local queue mirrors a CI run when a local
  assistant next engages with the change (import on next local engagement). It
  upgrades to direct queue writes when the local CLI ships its CI-import step.
- SESSION-START RULE: the consumer reads `QUEUE.md` FIRST at every AIQT session
  start; an UNCONSUMED entry is RAISED to the developer before new work, consistent
  with the advisory posture (section 1), so the developer disposes of it or explicitly
  defers, never a silent hard block. Chat assistants without filesystem access carry
  the same rule as prose: before new work, ask for the findings queue.

## 4. Scheduled re-surface (no daemon)

Check-on-opportunity, NO PERSISTED FLIP: every LOCAL AIQT entry point (session start,
the wizard, the doctor, a local review run) COMPUTES the age of every `UNCONSUMED`
entry against `ResurfaceDays` and RAISES the ones past it (the derived `RESURFACE-DUE`
view) to the developer before new work. Because the state is derived and never written,
the read-only entry points honour their own contracts: the wizard still writes only
`config.md`, and the doctor still writes nothing (its findings-queue check reports the
derived counts on demand). A record leaves the derived-due view only when the writable
runtime persists its transition to `CONSUMED`/`ACKNOWLEDGED`; an already-due record is
therefore raised at EVERY entry point until that happens, not once. A repository with no
activity has, by construction, nothing waiting on its findings. TODAY the CI lanes do
not post reminder comments; that step upgrades into the kit when the scheduled trigger
class ships, with deduplication one reminder per full window crossed, never one per run.

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
read as auto-update-on. The setup wizard states this distinction where it writes the
two settings.

## 7. Phase boundaries

v1 ships the lifecycle, the queue formats, the session-start rule, the three knobs,
and the two prompt shapes. Deferred by design, each named where it lands: the CI
reminder step (the scheduled trigger class), queue-shape mechanical checks (the
logs-and-metrics and static-report items), cross-repo roll-up, any portal feed.
