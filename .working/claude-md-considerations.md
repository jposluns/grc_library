# CLAUDE.md considerations (removal ledger)

**Version:** 1.0.5\
**Date:** 2026-07-04\
**License:** CC BY-SA 4.0

## Purpose

This file is the removal register for the PR #441 condense of
[`.claude/CLAUDE.md`](../.claude/CLAUDE.md) (the maintainer's Option-B "keep actionable
rules, cut rationale / war-stories / duplication" directive). The condense kept every
rule and procedure step; it cut the rationale, war-stories, and provenance that were also
recorded authoritatively elsewhere (the pack rule files, the pack README,
[`improvement-log.md`](improvement-log.md),
[`changelog-details/CHANGELOG-detailed.md`](changelog-details/CHANGELOG-detailed.md),
`design-decisions.md`). Nothing is lost: each removal is preserved verbatim here with an
analysis of why it went, the expected gain, the potential risk, and the observable signal
that would show the removal was wrong.

The verbatim removed text is quoted inside fenced code blocks. That is deliberate: gate 51
(`lint-working-prose-hygiene`) scans this `.working/` tree for em/en dashes in prose but
exempts code spans and fenced blocks, and some removed lines carry em-dashes. The fenced
block both preserves the text byte-for-byte and keeps the gate green. The analysis fields
are house-style prose (dash-free).

## Review cadence (the "advise on putting it back" loop)

- **Every `/retro`** does a quick scan of the open RM entries below.
- **The periodic hallucination-metrics review** does a deeper pass.
- For each open RM, check whether its "evidence the removal was wrong" signal has appeared
  (a recurrence of the failure class the removed text documented, a maintainer or agent
  re-litigating a settled rule, a question the removed text would have answered). If it
  has, advise the maintainer to **restore** the text (or to make a **new** CLAUDE.md
  change the removal inspired), and record the disposition in the entry's **Status**.
- A removal whose signal never appears is evidence the cut was correct; it stays out.

**Status values:** `open` (cut, watching) | `reviewed-keep-out (YYYY-MM-DD)` | `restored
(PR #N, YYYY-MM-DD)` | `inspired-change (PR #N, YYYY-MM-DD)` | `dispositioned-codified
(PR #N, YYYY-MM-DD)` (the watch signal fired and the remedy was codified into CLAUDE.md
rather than the cut text restored verbatim).

The pointer from CLAUDE.md to this file is the condense note at the top of
[`.claude/CLAUDE.md`](../.claude/CLAUDE.md); the review-cadence wiring is in
[`improvement-log.md`](improvement-log.md)'s Convention section.

---

## RM-1: PRIMORDIAL RULE provenance and checkpoint-calibration aside

**Section:** `## PRIMORDIAL RULE` | **Removed in:** PR #441 | **Status:** reviewed-keep-out (2026-07-03)

**Removed text (verbatim):**

```
(maintainer-calibrated 2026-06-22 to high-signal checkpoints only; the per-file-write and per-N-operations mechanical triggers were dropped as noise)

This rule was added 2026-06-22 by maintainer direction as the project's apex statement; it consolidates and elevates the integrity disciplines already in the `dev-security/claude-rules/governance/` pack (gate-discipline, evidence-grounded-completion, clarify-before-acting, change-tracking) under a single lexicographic priority.
```

**Why removed:** Provenance and a superseded-calibration note, not a rule. The four
checkpoints and the apex ordering are retained; the pointer to the distributable pack rule
[`project-integrity.md`](../dev-security/claude-rules/governance/project-integrity.md) is
retained. The "added 2026-06-22" lineage lives in CHANGELOG and the pack rule's own "Why
this rule exists".

**Expected gain:** A few lines off the apex section; removes a dated calibration parenthetical that could read as still-active guidance.

**Potential risk:** A reader loses the note that the per-file-write and per-N-operations triggers were deliberately dropped, and might propose re-adding mechanical triggers.

**Evidence the removal was wrong (watch for):** a proposal to add per-operation integrity-check triggers, or confusion about why the checkpoint list is only four items. If seen, restore the calibration parenthetical.

**Disposition pass (2026-07-03, GR-8(a)):** No proposal for per-operation triggers and no checkpoint-list confusion in any post-#441 record (improvement-log #442 to #588 searched).

---

## RM-2: Date/timezone PR #187 gate-31 war-story

**Section:** `## Date and timezone convention` | **Removed in:** PR #441 | **Status:** reviewed-keep-out (2026-07-03)

**Removed text (verbatim):**

```
The PR #187 gate-31 timezone-boundary edge case (the pack README's `Date` field stuck
at `2026-06-21` because both commit-date and `Date` field were `2026-06-21` at PR #187's
local-time merge moment but the UTC date had already rolled to `2026-06-22`) traces to
this convention. UTC is uniform; the gate logic and the metadata both agree on the UTC
day, and the visible "drift" is one of presentation only.
```

**Why removed:** Illustrative war-story, not a rule. The actionable rule (work in UTC; when ambiguous use the UTC date) is retained in the section. The #187 incident is in CHANGELOG history.

**Expected gain:** Four lines; removes an incident retelling a reader does not need to apply the UTC rule.

**Potential risk:** A reader hitting a UTC-versus-local mismatch loses the worked example and might re-question the UTC rule.

**Evidence the removal was wrong (watch for):** a recurrence of gate-31 date-boundary confusion, or a maintainer or agent re-litigating "local or UTC?", that the retained one-liner did not prevent. If seen, restore the example or add a `(see PR #187)` pointer.

**Disposition pass (2026-07-03, GR-8(a)):** The #187 edge class recurred once (#547: the UTC date rolled mid-commit) and the pre-push guard's D4 caught it mechanically with no re-litigation of the UTC rule; the retained convention sufficed.

---

## RM-3: PR-workflow step 1 commit-graph-gate rationale

**Section:** `## PR workflow` step 1 | **Removed in:** PR #441 | **Status:** reviewed-keep-out (2026-07-03)

**Removed text (verbatim):**

```
Git-history-aware gates
   (gate 40 in this project, plus any future gate that examines commit
   graph) only see committed state, so running the audit on the working
   tree before committing misses what would happen post-commit. Running
   between commits catches gate 40-class issues locally, before CI does.
   ...
   plus the history-aware gates that examine each file's commit graph
   (gate 45 TODO staleness, gate 40 version-bump-recency, gate 31
   document-date-staleness). That history-aware trio also runs in
   `run_all_audits.sh`; the pre-push runner re-invokes the three so a
   single pre-push command is a complete commit-graph-aware guard, which
   matters most for large multi-commit or file-move changes such as the
   governance Phase-1 migration (gates 40, 31, 45 folded in per the
   design-decisions "Gate-family coherence, Option A" decision).
```

**Why removed:** Explanatory rationale for why the runner exists and why it runs between commits. The actionable instruction (run `run_all_audits.sh` after each commit; push via the guard, which chains both runners) is retained, and the gate identities (D1-D4, 45/40/31; the delta set is D1-D6 since the #623 D6 check (D1-D5 from the #469 D5 check until then), and the condensed CLAUDE.md line was updated to D1-D5 in the section-3.14 batch) are retained in condensed form. The governance Phase-1 migration is long finished.

**Expected gain:** About twelve lines off the longest procedure step; the step now reads as instructions rather than instructions plus justification.

**Potential risk:** A reader loses the explanation of why a between-commits audit run matters (the gate-40 commit-by-commit subtlety), and might run the audit only once before push and be surprised by a gate-40 failure.

**Evidence the removal was wrong (watch for):** a recurrence of a gate-40 or gate-31 failure traced to running the audit only on the final working tree rather than after each commit, or an agent asking why the pre-push runner re-invokes gates that `run_all_audits.sh` already ran. If seen, restore the commit-graph explanation.

**Disposition pass (2026-07-03, GR-8(a)):** Near-moot: the compressed rationale survives in PR-workflow step 1 (the history-aware gates 40/31/45 see only committed state). The one between-commits lapse (#516) was a discipline slip, not a comprehension gap, and was self-caught pre-push.

---

## RM-4: PR-workflow step 5a handoff-PR loop mechanics

**Section:** `## PR workflow` step 5a | **Removed in:** PR #441 | **Status:** reviewed-keep-out (2026-07-03)

**Removed text (verbatim):**

```
Running them on a handoff PR produces
   ledger rows that, per recursion-avoidance, must batch into a *new* PR, whose
   merge triggers another `/validate-pr`, which produces more rows: at a session
   boundary there is no terminating "next substantive PR", so the cadence loops
   without end. The compensating control is that the next session's `/resume`
   runs a full corpus-wide `/validate` as its first task (stronger than the
   skipped per-PR sweep, since it re-examines the whole corpus). This exception
   is a maintainer-authorised standing rule (not the abbreviation failure mode
   the `## Throughput pressure` section forbids); it is recorded inline in the
   handoff PR's `.working/validate-pr/history.md` row Summary cell with this
   rationale, satisfying the no-skip discipline's "documented exception in the
   history row" requirement.
```

**Why removed:** The full loop-mechanics explanation is duplicated almost verbatim in
`## Session migration` item 3 (the closing-handoff-PR discipline). Step 5a now states the
exception, the compensating control, and where to record it, and points to item 3 for the
full reasoning. This is de-duplication, not a content cut.

**Expected gain:** About ten lines; the loop explanation now lives in exactly one place (item 3) instead of two.

**Potential risk:** A reader of step 5a alone gets the rule but not the full why; they must follow the pointer to item 3.

**Evidence the removal was wrong (watch for):** an agent running `/validate-pr` on a session-closing handoff PR (the exact loop the exception prevents), or asking why the handoff PR skips QA. If seen, the pointer to item 3 was insufficient; restore the inline explanation in 5a.

**Disposition pass (2026-07-03, GR-8(a)):** No handoff PR ran the trailing QA and no one questioned the exception. The #450/#451 marker-cell recurrence was a different defect in the same neighbourhood, closed by the #452 step-5a rewrite.

---

## RM-5: PR-workflow step 5c compensating-signal rationale

**Section:** `## PR workflow` step 5c | **Removed in:** PR #441 | **Status:** reviewed-keep-out (2026-07-03)

**Removed text (verbatim):**

```
These are the loop-break compensating control's cheap signal: the next session's
   `/resume` `/validate` cross-checks findings against the asserted-clean claims (a
   contradiction of a claimed-clean touched surface is a genuine miss, escalated), and
   re-running the audit confirms the green-at-`<sha>` (the one deterministic
   close-vs-start diff). This replaces a second close-time `/validate`, which would be
   noise: same commit, non-deterministic subagent layer.
```

**Why removed:** Rationale for why the asserted-expectations and green-at-sha signals exist
and why they replace a second close-time `/validate`. Step 5c retains the instruction
(refresh those surfaces at a session-closing handoff PR) and a compressed version of the
why; the full reasoning is also in `## Session migration` item 3.

**Expected gain:** About seven lines; removes a justification the actionable instruction does not need.

**Potential risk:** A reader loses the explicit "why not just run a second /validate at close" answer and might propose adding one.

**Evidence the removal was wrong (watch for):** a proposal to run a second corpus-wide `/validate` at session close, or confusion about what the asserted-expectations section is for. If seen, restore the rationale.

**Disposition pass (2026-07-03, GR-8(a)):** No second-close-time-sweep proposal appeared, and the asserted-expectations cross-check demonstrably functioned as designed (#458: Sweep 75 escalated against the #457 handoff assertion).

---

## RM-6: Session-migration checklist inline war-stories

**Section:** `## Session migration and PR close-out checklist` item 2 | **Removed in:** PR #441 | **Status:** inspired-change (PR #576, 2026-07-02)

**Removed text (verbatim):**

```
(the #372 miss: the metadata `Version` moved to
     `1.49.18` with no `1.49.18` history row, `/validate-pr`-caught not gate-caught)
...
(the #371/#374 miss:
     the `RC.IM` to `ID.IM` migration left the word "recovery" in the description,
     mismatched against the Identify function; Sweep-55-caught)
...
(e.g.
     PR #252 missed a same-file Verification criterion and Rationalizations cell when
     it revised the routing convention; `/validate-pr` caught it, but the grep would
     have caught it first)
...
(caught repeatedly, including PR #244 and the
     trust-recovery codification)
...
(improvement-log #341/#347/#349/#355)
...
(the file had reached 426
     lines / 47 stacked blocks before the 2026-06-28 first prune)

   This checklist is the convention-level companion to the queued P4.6 mechanical
   QA-cadence gate; until that gate exists, the checklist is the guard. It was added
   after two paired-bookkeeping-surface misses in one session (a validate-pr row not
   batched into the next PR; an FR closed in CHANGELOG without the TODO-to-DONE
   rotation), both degradation-shaped late-session slips.
```

**Why removed:** Each checklist item kept its imperative; the parenthetical PR-number
war-stories that justified each item were cut (they are recorded in CHANGELOG, the
improvement-log, and Sweep records). The first sentence of the closing paragraph (the
P4.6-companion framing) is retained; the "added after two misses" provenance is cut.

**Expected gain:** Roughly fifteen lines across the checklist; each item reads as a check to perform rather than a check plus its origin story.

**Potential risk:** The war-stories were load-bearing for *why each check matters*; a reader who does not believe a check is worth the effort loses the concrete failure that motivated it, and might drop the check. This is the highest-judgement removal in the condense.

**Evidence the removal was wrong (watch for):** a recurrence of any of the named failure classes (metadata-Version without a history row; a coded-value migration leaving stale description prose; a same-file convention-revision missing a sibling cell; an em-dash or British -ise in new pack prose; a paired-bookkeeping-surface miss), which would mean the de-motivated check stopped being followed. If any recurs, restore that item's war-story parenthetical.

**Disposition pass (2026-07-03, GR-8(a)):** Three of the five war-story classes recurred (sibling-carrier survivals #568/#571/#579/#587; the #580 bare-token violation on the same register family #443 taught; the repeated paired-surface misses #495/#569). The durable answers were mechanical (gate 50, gate 57 in #468, the D5 PR-time closure check in #469 broadened to three forms in #501 and six in #576) plus new, more specific inline war-stories in the current checklist. #580, a violation of a rule whose war-story sat inline beside it, is the evidence that restoring the OLD parentheticals would not prevent recurrence; the text stays out and the class is answered by gates.

---

## RM-7: Session-migration item 3 byte-identical-corpus rationale

**Section:** `## Session migration and PR close-out checklist` item 3 | **Removed in:** PR #441 | **Status:** reviewed-keep-out (2026-07-03)

**Removed text (verbatim):**

```
This is the cheap signal that replaces a
   wasteful second close-time `/validate` (the corpus is byte-identical across the
   boundary, so two non-deterministic subagent runs would differ only by sampling
   variance; the one deterministic close-vs-start diff worth keeping is the mechanical
   green-at-`<sha>`).
```

**Why removed:** The same "why not a second close-time /validate" rationale as RM-5,
stated a second time in item 3. Item 3 retains the rule (the closing PR records
asserted-expectations and green-at-sha; `/resume` cross-checks). De-duplication.

**Expected gain:** About five lines; the sampling-variance argument now appears at most once in the file.

**Potential risk:** Same as RM-5; if both RM-5 and RM-7 are out, the explicit argument against a second close-time `/validate` is gone entirely (only the instruction remains).

**Evidence the removal was wrong (watch for):** same signal as RM-5 (a proposal to add a second close-time sweep). If seen, restore one of RM-5 or RM-7.

**Disposition pass (2026-07-03, GR-8(a)):** Same searches as RM-5; no occurrence.

---

## RM-8: Wind-down framework opening war-story and provenance

**Section:** `## Wind-down decision framework` | **Removed in:** PR #441 | **Status:** inspired-change (PR #460, 2026-06-29)

**Removed text (verbatim):**

```
A recurring pattern across recent sessions (#351, #358, #361, #369, #373): after the resume
`/validate` sweep plus a few PRs, the assistant concludes "clean boundary, heavy context, Quality >
Speed, hand off" and winds the session down on its own. That conclusion is often correct, but taking
it silently is the same failure the `clarify-before-acting` and `action-before-explanation-of-inaction`
rules forbid everywhere else: narrating an inaction (the handoff) as if it were forced, without
surfacing the capability assessment that would let the maintainer redirect. This section closes that
hole at the wind-down boundary. The maintainer set it 2026-06-26 after judging that several sessions
wound down earlier than necessary.
...
(Added 2026-06-28 after a wind-down was surfaced on an ungrounded
   "context is heavy" claim; the maintainer flagged it as an unobservable-state assertion.)
```

**Why removed:** The session-list war-story and the two provenance notes. The condensed
section keeps the full trigger (the three required components, including the
un-instrumented-internal-state bar), the named options A-D, and the timeout rule. The "why
this section exists" is preserved in compressed form ("taking it silently is the same
failure the clarify rules forbid").

**Expected gain:** About ten lines off a long section; the framework reads as the procedure rather than the procedure plus its origin.

**Potential risk:** A reader loses the concrete sessions that motivated the framework and the specific 2026-06-28 "context is heavy" incident that motivated the un-observable-state bar; the bar might be weakened back toward subjective triggers.

**Evidence the removal was wrong (watch for):** a wind-down surfaced on an un-instrumented "context is heavy / feels long" justification (the exact 2026-06-28 incident), or a silent handoff with no surfaced decision. If seen, restore the provenance that anchored the un-observable-state bar.

**Disposition pass (2026-07-03, GR-8(a)):** The signal fired in full (the maintainer's 13-of-15 observation, two in-session wind-down proposals) and #460 rewrote the wind-down framework (continue-by-default, the invalid-trigger list, the calibration bar), superseding the removed provenance outright.

---

## RM-9: Throughput-pressure Sweep 22 corrective-action detail

**Section:** `## Throughput pressure does not authorize QA abbreviation` | **Removed in:** PR #441 | **Status:** reviewed-keep-out (2026-07-03)

**Removed text (verbatim):**

```
surfaced four in-window errors across 11 PRs (#231-#241) that had been recorded as
"abbreviated spot-check, 0 findings" instead of formal `/validate-pr` runs. The
abbreviation was unauthorised, the formal run would have surfaced the errors, and
the maintainer's discipline catch was the recovery path. The corrective action is
this rule plus the pack-rule and SKILL-file vocabulary updates that landed in the
same Sweep 22 close-out PR.
```

**Why removed:** The detailed Sweep 22 recount. The condensed section keeps the rule (no
abbreviation; the two sanctioned shapes; surface the pressure instead of acting on it) and
a one-line reference to Sweep 22 as the motivating incident.

**Expected gain:** About six lines; the rule keeps its teeth (the named incident) without the full post-mortem.

**Potential risk:** A reader loses the specifics (four errors, 11 PRs, the "abbreviated spot-check" phrasing) that make the prohibition vivid, and might rationalize an abbreviated check.

**Evidence the removal was wrong (watch for):** any "abbreviated /validate-pr, 0 findings" or equivalent informal-substitute record reappearing in a history row. If seen, restore the Sweep 22 detail.

**Disposition pass (2026-07-03, GR-8(a)):** No post-#441 abbreviated-QA record exists (every 'abbreviated' history row is the pre-#441 Sweep-22 era); near-moot besides, the Throughput section retains the Sweep-22 substance.

---

## RM-10: Version-bump four-questions operationalization

**Section:** `## Version-bump discipline` | **Removed in:** PR #441 | **Status:** dispositioned-codified (PR #609, 2026-07-03)

**Removed text (verbatim):**

```
**Operationalization**: at each commit, ask four questions:
1. Did this commit change a versioned document's body? → Bump that document's
   Version **and** Date in this commit.
2. Is this the last commit before push? → Bump library CalVer in
   [`README.md`](../README.md) and the README's own Version field in the same
   commit.
3. Did `tools/run_all_audits.sh` pass after this commit? → If not, fix before
   pushing. Gate 36 (linter regression) exercises gates 31 and 40 in test form
   and catches per-document-bump omissions locally before CI does.
4. Did `tools/run-pr-time-checks.sh` pass against the merge base before push? →
   If not, fix before pushing.

The post-commit `run_all_audits.sh` discipline (already specified in `## PR
workflow` step 1) is the catch-net for this rule: if the four questions are
asked and the audits pass, the rule has held.
```

**Why removed:** This operationalization is now **mechanized**: the pre-push guard
(`tools/pre-push-guard.sh`, shipped #439/#440) runs `run_all_audits.sh` (gates 40 and 36)
and `run-pr-time-checks.sh` (D2 and D4) before every push, so questions 3 and 4 are
enforced rather than remembered, and questions 1 and 2 are the body of the four-surface
list that the section retains. The condensed section replaces this with an **Enforcement**
paragraph pointing at the guard plus the two-question commit-time prompt. This is the
Option-A payoff (the guard first lets the prose collapse to a pointer).

**Expected gain:** About sixteen lines; the discipline now states the four surfaces plus "the guard enforces this" instead of a manual four-question checklist that duplicates what the guard runs.

**Potential risk:** If the guard is ever removed, bypassed, or not run (for example a direct push that skips the `&&` chain), the manual four-question fallback is no longer written down, and a version bump could be missed without the prompt. The guard's own #439 HIGH bug (it once exited 0 on failure) shows the guard is not infallible.

**Evidence the removal was wrong (watch for):** a gate-40 or gate-31 or D2 or D4 failure reaching CI (meaning the guard did not catch it and the manual prompt was not there as backup), or an agent pushing without the guard. If seen, restore the four-question operationalization as the documented fallback.

**Disposition pass (2026-07-03, GR-8(a)):** Reviewed 2026-07-03, stays open: two pipe-masked guard exits let pushes past a FAILING guard (#569, #583), a variant the removed four questions would not have prevented (they ask whether the runners passed, and the masked output is exactly what misled). The uncodified remedy (run the guard standalone and unpiped, read its exit before the chained push) is queued as a morning decision (protected-tree CLAUDE.md edit; pending-decisions entry 2026-07-03).

**CODIFIED (2026-07-03, the D5 PR):** the maintainer authorized the remedy at the 2026-07-03 morning round and the unpiped-guard sentence now lives in the CLAUDE.md PR-workflow step 2 (standalone, unpiped, read the terminal PASS/FAIL line; the incident lineage cites #569, #583, and the #608 push, a third self-caught instance that occurred the same morning the sentence was authorized). This entry closes as dispositioned-codified: the watch signal fired, the codification landed, and the residual (a guard bypassed entirely) remains covered by the D2/D4 CI gates as the entry's risk paragraph notes.

---

## RM-11: Behavioral-rule clarify rationale and Karpathy provenance

**Section:** `## Behavioral rule: clarify before acting` | **Removed in:** PR #441 | **Status:** reviewed-keep-out (2026-07-03)

**Removed text (verbatim):**

```
The library's audit programme already enforces "surgical changes" and "goal-driven
execution" mechanically through the audit gates and the user-level verification
rules; the gap this section closes is pre-implementation clarification. The
authoritative current form of this discipline lives in
`.claude/rules/governance/clarify-before-acting.md` (the pack rule, project-agnostic)
and as Rule 9 in `~/.claude/CLAUDE.md` (the user-level memory form); originally
adapted from Karpathy's "Think Before Coding" CLAUDE.md rule
(<https://github.com/multica-ai/andrej-karpathy-skills>, MIT).
```

**Why removed:** Rationale plus external attribution. The condensed section keeps the rule
(surface ambiguity in one sentence, ask before proceeding, do not silently pick) and the
two authoritative pointers (the pack rule and user-level Rule 9). The "audit programme
already enforces surgical changes" framing and the Karpathy origin are cut; the Karpathy
attribution remains in the pack rule's own provenance.

**Expected gain:** About six lines; the section is now the rule plus its authoritative pointers.

**Potential risk:** The external attribution (Karpathy, MIT) is a provenance/licence courtesy; dropping it from CLAUDE.md (it survives in the pack rule) slightly reduces visibility of the lineage.

**Evidence the removal was wrong (watch for):** a licence or attribution question about the clarify rule's origin, or confusion about how this section relates to the audit programme. If seen, restore the attribution line.

**Disposition pass (2026-07-03, GR-8(a)):** Zero post-#441 hits for the provenance question across every durable record.

---

## RM-12: Communication-conventions provenance line

**Section:** `## Communication conventions` | **Removed in:** PR #441 | **Status:** reviewed-keep-out (2026-07-03)

**Removed text (verbatim):**

```
Added 2026-06-28 by maintainer direction (the no-intensifier and `IMPORTANT:` conventions after an "honestly" intensifier crept into the assistant's chat voice; the "suggest"/"advise" interpretation rule codified the same session).
```

**Why removed:** Provenance, not a rule. The three conventions (no honesty-intensifiers, `IMPORTANT:` marker, suggest/advise interpretation) are retained verbatim.

**Expected gain:** One line; removes a dated origin note.

**Potential risk:** Negligible; the conventions stand without their origin date.

**Evidence the removal was wrong (watch for):** unlikely; a maintainer asking when these conventions were set. If seen, the date is in CHANGELOG.

**Disposition pass (2026-07-03, GR-8(a)):** No dating question arose; the section grew two new maintainer-directed bullets (#584) without the removed date being needed.

---

## RM-13: Security-and-governance per-rule long descriptions and pack version-history narrative

**Section:** `## Security and governance requirements` | **Removed in:** PR #441 | **Status:** reviewed-keep-out (2026-07-03)

This is the single largest removal: each of the eleven `governance/` pack rules carried a
multi-line description, and the section closed with a paragraph narrating the pack version
history. The condense replaced each rule's description with a one-line purpose (the rule
files themselves are authoritative) and replaced the version-history narrative with a
pointer to the pack README. The full removed descriptions and narrative:

**Removed text (verbatim):**

```
- `.claude/rules/governance/gate-discipline.md` — never weaken a gate to silence a
  failure; fix the artefact. Reinforces this project's `## Boundaries` rule and applies
  to every gate the audit programme exposes (see `tools/run_all_audits.sh` for the
  current set, including the CHANGELOG-on-PR delta gate).
- `.claude/rules/governance/change-tracking.md` — every PR carries a CHANGELOG entry,
  even if terse. Substantive entries cover anything that ships, modifies, or removes
  adopter-facing content; terse entries (date + version header + one sentence) cover
  ancillary changes (internal tooling, working-state housekeeping, pure refactors,
  typo fixes). There is no skip path. The paired DONE ledger carries 1-2-sentence
  headlines, no links — at-a-glance index, not a CHANGELOG duplicate. Generalises the
  D1 CHANGELOG-on-PR delta gate, the link-coverage gate, and the version-monotonicity
  audit into a portable discipline.
- `.claude/rules/governance/evidence-grounded-completion.md` — never claim completion
  ("done", "fixed", "ready", "shipped", "good catch"), and never assert a property of an
  artefact you have not read (that a file contains, lacks, or requires something), without
  running the verification protocol first (enumerate, re-read, quote, contradiction-search,
  distinguish mechanical from semantic verification, state unverified items). Pack-distributable
  form of the user-level Rules 6 and 7 (added 2026-05-31 and 2026-06-19); reinforces this
  project's existing Rules 1-5 about verification before dependent actions.
- `.claude/rules/governance/clarify-before-acting.md` — surface ambiguity in one
  sentence and ask before proceeding. Pack-distributable form of this project's
  `## Behavioral rule: clarify before acting` section; generalises that rule into a
  project-agnostic discipline applicable wherever an AI coding assistant participates.
- `.claude/rules/governance/artefact-and-branch-discipline.md` — generated artefacts
  are read-only (edit the source, run the generator, commit both halves together; CI
  verifies via `--check` mode); protected branches are append-only (no direct push;
  no force-push; PR-only merges). Pack-distributable form of this project's
  `## Boundaries` rules on generated files (`taxonomy.yml`, `docs/portal.md`,
  `docs/maturity-scorecard.md`) and on direct pushes to `main`; binds the
  version-monotonicity audit to
  branch protection as its primary defence.
- `.claude/rules/governance/action-before-explanation-of-inaction.md` — never explain
  why an external action cannot or will not proceed without first attempting it (when
  the action is safe and reversible) or naming it and asking (when it is destructive).
  Pack-distributable form of the user-level Rule 8 (added 2026-06-19);
  operationalises this project's `## PR workflow` discipline (the merge of a green PR
  via MCP is a safe action and should be attempted, not narrated as "blocked").
- `.claude/rules/governance/validate-inference-before-action.md` — when the next
  action depends on an inferred premise (a state claim not directly observed in the
  current turn), validate the premise via tool call before taking the action.
  Action-side counterpart of the evidence-grounded-completion rule (which is the
  assertion-side). Added 2026-06-21 after a recurring failure mode where an
  orchestrator inferred premises (subagent-skip justification, fix-completeness,
  corpus-state) without validating; each inference cascaded into downstream rework.
  The immediate trigger was a fix-completeness inference (PR #111's close-out
  inferring the fix complete after one occurrence) that Sweep 9 iteration 2 caught.
- `.claude/rules/governance/ai-assistant-workflow-disciplines.md` — five disciplines
  for an AI assistant driving multi-PR work: (1) research-assistant discipline
  (workers produce research, orchestrator authors final prose, claims verified at
  apply-time); (2) pipeline PR construction (parallel research, serial apply, CI
  gating between PRs); (3) apply-time worker correction (catch worker errors at
  apply-time, document them in the entry); (4) "always split when in doubt"
  (default to separate PRs unless tightly coherent); (5) background work during CI
  waits (read-only prep on the next PR). This project tracks the apply-time-catch
  vs shipped-escape ratio in [`.working/hallucination-metrics.md`](../.working/hallucination-metrics.md)
  as the project-specific instantiation of the research-assistant discipline's
  tracking convention. The orchestrator uses [`.working/worker-brief-template.md`](../.working/worker-brief-template.md)
  as the starting point for every worker dispatch; the template codifies the
  guard rails that prevent recurring worker-side failure modes and is updated
  inline when a new failure class is caught (per the rule's hallucination-assessment
  update protocol).
- `.claude/rules/governance/trust-recovery-escalation.md` — the escalation tier
  invoked when an AI assistant's discipline failures put a maintainer's confidence
  in a window of work in question. Names the trigger (abbreviated/skipped QA across
  changes, a skipped verification reaching the pipeline, a wrong-cadence automation,
  an unvalidated inference that cascaded), the two-skill suite (the AI-failure-pattern
  forensic pass `/full-qa` first, then the fresh-reader persona pass `/fitness`; both
  runnable in sequence via the thin `/trust-recovery` wrapper command), the
  routing convention (every confirmed finding routed, tiered by severity: H[critical]
  and High to P1, Medium and Low to P2, none dropped; apply-time-verified, deduped), and
  the sign-off discipline (terminates only on explicit maintainer sign-off, not on an
  empty finding-set). Includes the full-clone methodology rule. Added 2026-06-22 (pack
  1.47.0; routing revised to severity-tiered in 1.47.1).
- `.claude/rules/governance/project-integrity.md` — the apex rule of the pack: the
  project-agnostic distribution of this file's PRIMORDIAL RULE. Fixes the priority
  ordering on the optimization-dimension axis (**lexicographic Quality > Speed > Cost,
  project integrity non-negotiable**): where each other rule constrains a specific
  behaviour, this rule decides which dimension wins when they conflict, and re-states
  the integrity non-negotiables (no stub/mock/fabrication; no gate suppression; no
  silent changes; failing states surfaced) as the apex-precedence forms of
  `gate-discipline`, `evidence-grounded-completion`, and `clarify-before-acting`, with a
  self-reminder checkpoint at task start, before persistence, before completion claims,
  and at tension points. Added pack 1.49.0 (the distributable form the PRIMORDIAL RULE
  section above signalled was queued).
- `.claude/rules/governance/surface-counterproductive-instructions.md` — a clear
  instruction is not automatically a correct one. When following an instruction as given
  would reduce efficiency, effectiveness, or productivity, lower quality, destroy work
  already done, contradict a stated goal, or rest on a stale-state belief, stop, consider,
  and surface the concern with named options before executing (stop, consider, confirm),
  so the requestor can confirm or redirect. The charitable-interpretation corollary
  forbids silently taking a harmful literal reading or reverting committed work without
  confirming; the anti-over-ask calibration keeps it from becoming friction (fire only on
  material downside, one informed round, accept an informed override). Requestor-facing
  counterpart to `clarify-before-acting` (ambiguity) and broader than `project-integrity`
  (any net-negative effect, not only the Quality versus Speed versus Cost tradeoff). Added
  pack 1.51.0, maintainer-directed after a literal-and-silent reading of a wind-down
  instruction reverted committed work.

The `dev-security/claude-rules/` pack covers security and development-governance
discipline. The initial governance rollout completed at pack version 1.11.0
(2026-06-01) with the first five `governance/` rules listed above; pack version
1.21.0 (Library 2026.06.38) extended the set with the sixth rule; pack version
1.27.0 added the seventh rule (`validate-inference-before-action.md`); pack
version 1.36.0 added the eighth rule (`ai-assistant-workflow-disciplines.md`);
pack version 1.47.0 added the ninth rule (`trust-recovery-escalation.md`) after a
session whose discipline failures required a structured white-box re-examination of
the window; pack version 1.49.0 added the tenth rule (`project-integrity.md`), the
project-agnostic distribution of the PRIMORDIAL RULE's Quality > Speed > Cost apex
ordering; pack version 1.51.0 added the eleventh rule
(`surface-counterproductive-instructions.md`), the discipline of surfacing a
clear-but-counterproductive instruction and confirming before acting on it (the
requestor-facing counterpart to `clarify-before-acting`). See
`dev-security/claude-rules/README.md` for the authoritative pack version
history and future-work signalling. Pack changes are tracked through the
library's CHANGELOG and per-rule version metadata.
```

**Why removed:** The eleven descriptions duplicate the opening paragraph of each pack rule
file (which is authoritative and read on demand), and the version-history narrative
duplicates the pack README's authoritative history. CLAUDE.md is auto-loaded every turn,
so this is the single highest token cost in the file for content that is one click away.
The condense replaced each with a one-line purpose (enough to know which rule to open) and
a pointer to the pack README.

**Expected gain:** About eighty lines, the largest single reduction in the condense; the
section becomes a navigable index rather than a re-statement of eleven rule files.

**Potential risk:** The one-line purposes are lossy: a reader who relied on the auto-loaded
CLAUDE.md descriptions (rather than opening the rule file) loses nuance such as the
provenance of each rule, the severity-tiered routing detail of trust-recovery, and the
five named disciplines of the workflow rule. The version-history narrative is the only
place that listed which pack version added which rule in prose; that now lives only in the
pack README.

**Evidence the removal was wrong (watch for):** an agent misapplying a governance rule in a
way the fuller CLAUDE.md description would have prevented (for example, dropping a
trust-recovery finding because the one-liner did not carry the "none dropped" invariant),
or repeatedly opening the same rule file because the one-liner was insufficient to act on.
If seen, restore that specific rule's fuller description (not necessarily all eleven).

**Disposition pass (2026-07-03, GR-8(a)):** No trust-recovery run occurred post-#441; the current one-liner already carries the none-dropped invariant, and the workflow-disciplines bullet was re-expanded for new content (#461), not for this removal's signal.

---

## RM-14: PR-activity-subscription cadence rationale (light)

**Section:** `## PR activity subscription discipline` | **Removed in:** PR #441 | **Status:** reviewed-keep-out (2026-07-03)

**Removed text (verbatim):**

```
The 60-second cadence balances latency (typical `Lint markdown corpus` CI
runs settle within one to two windows) against API cost: longer windows
leave silent-success failures hanging longer than necessary; shorter
windows hammer the GitHub MCP API.
...
The pack rules say to prefer
subscriptions over polling; this section says how to do that without
sitting indefinitely on a silent-success event.
```

**Why removed:** Rationale for the 60-second number and a closing restatement of the
section's purpose. The actionable discipline (subscribe, arm a 60s timer, check on
fire-or-timeout, re-arm, `TaskStop` on merge) and the pack-rule pointers are retained; a
one-clause "balances latency against API cost" is kept.

**Expected gain:** About six lines; the section is now the procedure plus a brief why.

**Potential risk:** A reader loses the explicit reasoning for 60 seconds specifically and might change the cadence without understanding the latency-versus-API-cost tradeoff.

**Evidence the removal was wrong (watch for):** a change to the fallback-timer cadence that hammers the API or leaves CI hanging, or a question about why 60 seconds. If seen, restore the cadence rationale.

**Disposition pass (2026-07-03, GR-8(a)):** The only cadence change was the maintainer-directed 60-second background-task SOP (#584 codification after the #582 stall), a deliberate extension, not a misunderstanding the removed rationale would have prevented.

---

## RM-15: Attended-autonomous provenance asides (light)

**Section:** `## Attended-autonomous operating mode` | **Removed in:** PR #441 | **Status:** reviewed-keep-out (2026-07-03)

**Removed text (verbatim):**

```
there is a third, default-for-active-sessions mode the maintainer set
2026-06-26: **attended-autonomous**.
...
default about 2 minutes, tunable;
     mechanically a background `sleep`
...
This mode is the `clarify-before-acting` rule's "ask" refined for a
reachable-but-not-watching maintainer: still ask (surface the decision, named options), but degrade
gracefully instead of stalling, and never convert a timeout into a silent authorial pick.
```

**Why removed:** Provenance dates and a closing restatement of the mode's relationship to
`clarify-before-acting`. The three standing rules (green-CI merge authority,
stricter-is-safer, the two-path graceful-degradation mechanism with the reversibility
gate) are retained in full, including the roughly-2-minute timer.

**Expected gain:** A few lines; the mode reads as its three rules without the framing and date asides.

**Potential risk:** Low; the rules are intact. A reader loses the explicit "this is clarify-before-acting refined" framing.

**Evidence the removal was wrong (watch for):** confusion about how attended-autonomous relates to the clarify rule, or a timeout being converted into a silent authorial pick (the failure the closing sentence warned against). If seen, restore the framing sentence.

**Disposition pass (2026-07-03, GR-8(a)):** No timeout was converted into a silent authorial pick; the defer paths were used correctly (the section-4.10 hold in pending-decisions), and the 2-minute / background-sleep fragments are retained in the attended-autonomous section.

---

## Coverage note

The actionable-token survival check run at condense time confirmed every rule, path, gate
number, and procedure token still present in the condensed file. The only intentionally
dropped token was the Karpathy attribution (RM-11). The condensed file passed all 54 audit
gates. This ledger covers the substantive content removals; pure reflow (rewrapping a
paragraph, converting an em-dash to a colon, tightening a sentence without dropping a
fact) is not itemized because no content was lost.
