# CLAUDE.md sensitivity-trim review draft (TODO §1.19.12, Phase 5; MAINTAINER ACTION)

**Status: REVIEWED ONE-BY-ONE + maintainer-confirmed 2026-07-18 (attended, #1027). Classification FINAL.**
The maintainer walked the whole worklist section-by-section (AskUserQuestion batches) and confirmed
every verdict, with ONE change from the draft: **Date and timezone convention = KEEP whole** (was
SPLIT). Two sections were added by the #1026 protected bundle and classified in the same review:
**Boundaries = SPLIT** (item 11's cross-repo-write private-sibling/path specifics move; the rest
stays) and **QA-activity completion standard = KEEP** (portable, pack-rule twin). Final tally:
**32 sections, 2 MOVE / 17 KEEP / 13 SPLIT.** This is the FINAL input to the Phase-5 CLAUDE.md trim
(the actual content move to `_private`, sequenced with §1.19.8; the operating CLAUDE.md stays public
per §1.19.8, so only the MOVE + SPLIT-flagged content moves).
The maintainer reviewed and approved this classification ("proceed and lock classifications
first", 2026-07-18, attended-autonomous): the 2 MOVE / 15 KEEP / 13 SPLIT verdicts below are
LOCKED as the input to the Phase-5 CLAUDE.md trim (the actual move to `_private`, sequenced
with §1.19.8's relocation work; operating `CLAUDE.md` stays public per §1.19.8, so the trim
moves only the MOVE/SPLIT-flagged content). Decision points resolved (see below). The three
strictness calls I did not take are resolved to the broad-trim-as-drafted lean; the maintainer
can tighten (go stricter on provenance tails) at apply.

Original prep note: §1.19.12 is a maintainer action; the worklist was the prepared input so the
review was quick. Seeded by the offloaded `seed-119-12-claudemd-trimlist` research order
(worker-20260716-b, 2026-07-18) and re-authored plus spot-checked against the live project
CLAUDE.md structure by the orchestrator (research-assistant discipline: the seed is a hypothesis;
the verdicts below are the orchestrator's after checking each section, now maintainer-approved).

## Rubric

- **MOVE**: the whole section is operational state or process narrative (war-stories with PR
  numbers or dates, maintainer / machine / account specifics, internal process-improvement
  mechanics, private-sibling-file pointers): the class the 2026-07-17 cold-sales email mined.
- **KEEP**: a portable governance discipline an adopter fork inherits and runs (the AIQT
  rule, the PR-workflow steps, version-bump discipline, the abstract gate / QA cadences,
  pack-rule pointers).
- **SPLIT**: a section that mixes a portable rule WITH its war-story or operational
  justification: keep the rule public, move the story to `_private`.
- **Broad-trim lean applied** (maintainer choice): flag as move-worthy where genuinely
  operational.

## Worklist (by section, file order; maintainer-reviewed one-by-one 2026-07-18, attended; 32 sections: 2 MOVE / 17 KEEP / 13 SPLIT)

| Section | Verdict | If SPLIT: the sensitive part to move |
| --- | --- | --- |
| Condense note (PR #441 top block) | MOVE | whole block (points at the private `claude-md-considerations` ledger) |
| PRIMORDIAL RULE / AIQT (+ user-level reconciliation note) | KEEP | |
| Project / Why / Commands / Structure / Conventions | KEEP | |
| Language convention / Testing | KEEP | |
| Date and timezone convention | KEEP | **maintainer-confirmed KEEP WHOLE 2026-07-18** (override of the draft SPLIT; the America/Toronto maintainer-side note stays public) |
| PR workflow | SPLIT | the RM-10 seven-incident enumeration; the #866 collision; the #438/#439 momentum-bypass; the #445/#450 handoff-marker recurrence; the #495 rotation miss; the D5 eight-closure-form evolution log; the #847 next-prs drift note |
| Session migration + close-out checklist | SPLIT (bullet-wise) | KEEP the portable disciplines (paired-surface completeness, count-staleness timing, bare-token and corpus-wide contradiction greps, preflight, new-pack-prose lint); MOVE the worker-brief coverage-pairing, session-metrics / credit-offload / sync-scratch bullets, concurrency-lease and session-handoff mechanics, and the incident refs (#443/#614/#594/#455/#458/#612/#619/#622/#628) |
| Multi-session orchestration | SPLIT (lean MOVE) | keep the one-line partitionable-work pack-rule pointer; move the scratch exchange-channel mechanics, the claims-ledger / COVERAGE start-side check, the delivery-status-claim discipline, the 2026-07-09 recurrences, the runbook pointer |
| Credit-offload mode | MOVE | whole section (credit economics, worker-account topology, QA-trust-tier mechanics, the metrics tab, VM specifics, 2026-07-16/17 war-stories, design/metrics pointers): the exact class the cold-sales email mined |
| `/matrix-fit` and `/claim-fit` cadences | KEEP | (optionally trim the trivial #394/#399 and #621/#630 provenance tails) |
| Whole-project deep assessment (`/deep-assessment`) | SPLIT | the register + dated-file pointers, the hooks / #701 / #702 provenance, the 2026-07-08 coverage-obligation dated directive |
| Reference-breadth cadence (`/reference-audit`) | SPLIT | the doc-state ledger pointer and the dated (2026-07-08) trust-tier decisions |
| Publications screening (`/screen-publications`) | KEEP | re-read #1025: no `_private` pointer, no dated directive; portable cadence (maintainer-confirmed) |
| Reference-version currency | SPLIT | the 2026-07-17 ref-holds grep recurrence; the git-proxy-403 maintainer-setup detail + the third-party-issues pointer; the runbook pointer; the #505/#751 provenance |
| Missing-reference-document SOP | SPLIT (small) | the DD-10 egress refs and the runbook section-6 pointer |
| Attended-autonomous operating mode | SPLIT (lean MOVE) | keep the mode concept + stricter-is-safer + graceful-degradation principle; move the mode-exit priority ordering (with the overnight-pr pointer), the protected-backlog clearance (with the deferred-protected-changes pointer), the verifier-overrides / pending-decisions mechanics, the hook specifics, and the war-stories (2026-07-06 idle, 2026-07-17 r4 roughly-7-hour idle) |
| Wind-down decision framework | SPLIT (lean MOVE) | keep the continue-is-default rule; move the "13 of 15" (2026-06-29) and 2026-07-09 calibrations, the hallucination / session-metrics ledger pointers, the #425 recurrence |
| QA-activity completion standard (NEW, item 12, added #1026) | KEEP | portable governance discipline; has a pack-rule twin (`ai-assistant-workflow-disciplines`) an adopter inherits (maintainer-confirmed) |
| Throughput pressure does not authorize QA abbreviation | SPLIT (small) | the "Sweep 22 surfaced four errors across 11 PRs" incident |
| PR activity subscription discipline | SPLIT | keep the subscribe / fallback-timer / bounded-watch and background-task-check SOP; move the 2026-07-12 gh-CLI incident, the #582 stall, the dated directive tags |
| Version-bump discipline | KEEP | |
| Boundaries | SPLIT | **item 11's cross-repo-write specifics** (the private-sibling repo names + the `/home/jposluns/` path); KEEP the generic write-safety principle + the other boundaries (generated files, gates, secrets/PII, no-push-to-main, the force-push procedure) (maintainer-confirmed, reclassified from KEEP by item 11) |
| Behavioral rule: clarify before acting | KEEP | |
| Communication conventions | KEEP | (optionally trim the 2026-07-02 date tags) |
| Security and governance requirements | SPLIT (small) | the private-file pointers embedded in the rule descriptions (hallucination-metrics, verifier-overrides, high-assurance register, worker-brief-template) |

## Maintainer decision points (RESOLVED 2026-07-18, attended)

1. **Provenance tails** ("shipped in #NNN", "(maintainer-directed YYYY-MM-DD)") on otherwise-KEEP
   cadence sections: **RESOLVED = KEEP (broad-trim-as-drafted lean; NOT the stricter split-them-out
   option).** They narrate no incident and are harmless to an adopter. The maintainer may tighten
   to SPLIT at apply if desired; locked as KEEP for now.
2. **`/screen-publications`**: **RESOLVED = KEEP.** Re-read of the live CLAUDE.md body confirms no
   `_private` pointer and no maintainer/machine-specific or dated-directive content, only the
   portable screening cadence + standing rules, a `publications/SCREENING.md` reference-base-register
   pointer (adopter-relevant, not private), and a PR-provenance tail (KEEP per point 1).
3. **Session migration checklist**: **RESOLVED = bullet-wise apply** (re-author bullet-by-bullet
   per the row-34 split, not a whole-section block move).

## Net shape

The broad-trim concentrates the private material in FOUR sections (Credit-offload mode =
whole MOVE; Multi-session orchestration, Attended-autonomous mode, Wind-down = lean-MOVE
SPLITs) plus the operational bullets inside Session migration. The portable governance spine
(AIQT, the PR-workflow steps, version-bump, Boundaries, the clarify / evidence /
gate-discipline pointers, the QA cadences) stays public, so an adopter fork loses no runnable
discipline. Apply is Phase-5, held for attended; this draft is the input.
