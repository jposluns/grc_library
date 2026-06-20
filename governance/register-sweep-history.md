# Validation Sweep History Register

**Document Title:** Validation Sweep History Register\
**Document Type:** Register\
**Version:** 1.7.0\
**Date:** 2026-06-20\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](../dev-security/claude-rules/skills/validation-sweep/SKILL.md), [`governance/specification-audit-programme.md`](specification-audit-programme.md), [`governance/register-coverage-gaps.md`](register-coverage-gaps.md), [`CHANGELOG.md`](../CHANGELOG.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** On every validation-sweep invocation\
**Repository Path:** [`governance/register-sweep-history.md`](register-sweep-history.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register is the cumulative log of validation-sweep invocations and the findings each surfaced. It exists to give the maintainer (and any AI session running the sweep) three signals the one-off sweep reports cannot provide:

1. **Trend tracking**: which failure-mode classes recur most often, signalling priorities for new mechanical audit gates.
2. **False-positive memory**: findings the maintainer has triaged as not-a-real-finding, suppressed in subsequent sweeps so the maintainer does not pay the triage cost repeatedly.
3. **Delta-per-sweep**: each sweep should ideally find less than the prior one as mechanical gates close failure classes; a sweep that finds *more* than the prior is signal that something has regressed.

The register is hand-maintained, each `/validation-sweep` invocation appends an entry; entries are not generated.

## Scope

Each entry records:

- **Sweep date and trigger**: when the sweep ran and why (on-demand, post-handoff, nightly, etc.).
- **Library + spec + pack versions at HEAD**: the state the sweep saw.
- **Findings count by class and severity**: how many High / Medium / Low / FYI findings in each of the eight catalogued failure-mode classes.
- **Actions taken**: which findings were actioned vs deferred vs dismissed; if dismissed, why (added to the false-positive memory below).
- **Resulting PRs**: links to PRs that closed the actioned findings.

The register does NOT record:
- Per-finding line numbers or file paths (those live in the sweep's transient output / PR descriptions).
- The full subagent reports (those are session-local artefacts).

## Failure-mode classes (mirror of the validation-sweep skill's catalogue)

The eight classes the sweep targets, as a stable identifier set for the entries below:

| Class | Shape |
| --- | --- |
| C1: stale-prose | Stale gate-counts / version-mentions in prose |
| C2: mis-attribution | Citation of "step X" / "section Y" where cited content does not match source |
| C3: multi-surface-incomplete | Change updates N-1 of N surfaces |
| C4: inferred-state-assertion | Claim about file contents without re-reading |
| C5: version-bump-omission | Non-exempt document changed without `Version:` bump |
| C6: generated-artefact-lag | Source edited but generator not re-run |
| C7: stale-docstring | Linter/script docstring no longer matches code |
| C8: term-drift | Different files use different terms for same concept |

### Classification convention: primary plus optional secondary

A finding may belong to more than one class at once. A multi-surface miss that surfaces as stale prose is both a C3 (mechanism) and a C1 (symptom); a term-drift between two files that share a generated artefact is both a C8 and a C6. The classification convention is:

1. **Each finding is tagged with a primary class** that names its dominant mechanism (the root cause an audit gate or skill would target to prevent recurrence). For a multi-surface miss that surfaces as prose drift, the primary class is C3.
2. **Each finding may optionally carry one or more secondary classes** that name the symptom shape a reader would notice first. For the same multi-surface miss, the secondary class is C1.
3. **The recurring-class summary table tracks primary-class counts** as its main signal (these are what mechanical defences should target). **A separate footnote tracks secondary-class participation** so the maintainer can see which symptom shapes are most common even when the mechanism is captured under a different primary class.
4. **Sweep entries record findings as `primary [+ secondary]`** (e.g. `C3+C1` for a multi-surface miss that surfaced as prose drift, or just `C1` for a pure stale-prose finding with no multi-surface mechanism).

Historical entries from Sweeps 1-3 were classified before this convention was documented; their primary classes are preserved as-is. Sweep 4 onwards records primary plus secondary where applicable. The classification rule is documented here once the convention exists; it is not retro-applied to rewrite historical findings.

## Sweep entries

### 2026-06-20, Sweep 1 (post-PR-#61 → PR #63)

- **Trigger**: maintainer requested "review for inconsistencies / errors" after overnight session caught a multi-surface incompleteness in PR #59.
- **State**: library 2026.06.46; spec 1.6.0; pack 1.24.2; 38 corpus gates.
- **Findings**: C3 (multi-surface-incomplete) × 4, three pre-existing prior-corpus-count references (the prose said "37" before gate 38 landed) in the audit-programme spec / coverage-gaps register / main-branch-protection register / document-index-and-classification register that PR #61 (the cleanup pass) had also missed; one missed §2.1 corpus-count reference. All actioned in PR #63.
- **Sweep value**: caught what PR #61 (the unaided cleanup) had not, by running corpus-wide rather than against the maintainer's recall.

### 2026-06-20, Sweep 2 (post-PR-#74 → PR #76)

- **Trigger**: maintainer requested `/validation-sweep` after pack 1.26.0 added three new skills (citation-quote-verification, fresh-reader-validation, skill-authoring-discipline) and the Layer 3 slash-command landed.
- **State**: library 2026.06.61; spec 1.10.0; pack 1.26.0; 42 corpus gates; 10 pack skills.
- **Findings** (all in-window):
  - **C1 (stale-prose)** × 1: `skill-authoring-discipline/SKILL.md` line 13 said "the pack now ships seven skills" / "past seven skills", written when the count was 7; pack now has 10. Rephrased to number-stable wording.
  - **C3 (multi-surface-incomplete)** × 1: the three new skills added See Also references from themselves to siblings, but did not add the reverse back-references in those siblings. The new `skill-authoring-discipline` skill explicitly prescribes bidirectional cross-references; its own first instance violated that rule.
  - **Discipline self-violation** × 1 (new shape, candidate for catalogue addition): `skill-authoring-discipline` description field shipped at 57 words; the skill itself prescribes 60-130 words. Expanded to 91 words.
- **Sweep value**: caught two meta-ironic instances of a skill violating the very discipline it codifies, on the same day the skill was authored. The strongest possible validation of the discipline.
- **Resulting PR**: [#76](https://github.com/jposluns/grc_library/pull/76).

### 2026-06-20, Sweep 3 (post-PR-#79 -> PR #80)

- **Trigger**: maintainer's standing "run a full validation after every three PRs and merges" cadence, fired after the third PR in the validation-sweep enhancement batch (PRs #77, #78, #79) merged.
- **State**: library 2026.06.65; spec 1.10.0; pack 1.26.4; 42 corpus gates; 10 pack skills.
- **Findings** (in-window):
  - **C3 (multi-surface-incomplete)** x 1: PR #78 introduced the deterministic pre-flight scanner under two different identifiers across parallel surfaces. The SKILL.md heading used `### 3.5.`; the slash-command file used `3a.`. Same logical step, two names. The CHANGELOG entry for PR #78 noted both names explicitly but neither file referenced the other's identifier. Surfaced by subagent A. Actioned by renaming the SKILL.md heading to `### 3a.` in PR #80; the integer-indexed step sequence (1, 2, 3, 3a, 4, 5, 6, 7, 8) is now consistent across both surfaces. The PR #78 CHANGELOG entry retains its "step 3.5" historical wording per Keep a Changelog convention.
- **Out-of-window incidental items (Low/FYI, no action this sweep)**:
  - `.github/workflows/quality.yml` uses tag-pinned actions (`actions/checkout@v4`, `actions/setup-python@v5`) rather than SHA-pinned; the external tikitribe pack recommends SHA pinning but no internal audit gate enforces this. The same pattern is now mirrored in the new `nightly-sweep.yml`. Pre-existing for the lifetime of the workflow. Not actioned this sweep.
  - `.github/workflows/quality.yml` lacks the top-level `permissions: {}` block now present on `nightly-sweep.yml`. Pre-existing. Not actioned this sweep.
- **Sweep value**: caught a same-day cross-surface naming drift introduced by my own PR #78. The pre-flight scanner correctly surfaced 12 candidates (all dismissed as legitimate historical references after subagent triage), demonstrating that the high-recall / subagent-precision split works as intended.
- **Resulting PR**: [#80](https://github.com/jposluns/grc_library/pull/80).

### 2026-06-20, Sweep 4 (post-PR-#82 -> PR #83)

- **Trigger**: maintainer's standing "run a full validation after every three PRs and merges" cadence, fired after the third PR following Sweep 3 (PRs #80, #81, #82) merged.
- **State**: library 2026.06.68; spec 1.10.0; pack 1.26.6; 42 corpus gates; 10 pack skills.
- **First sweep to apply the four-rule synthesis rubric** (introduced in PR #82). Findings are tagged with the rubric's evidence-letter (`R` / `I` / `K`) and three-level severity (`must-fix-before-merge` / `should-fix-this-PR` / `track-as-follow-up`).
- **Findings**:
  - **C1 (stale-prose)** x 1, in-window: [Subagent B] [R] [should-fix-this-PR] `docs/adopter-guide.md:57` "ships with its own version sequence (currently `1.22.0`)" when pack is at 1.26.6. Actioned in [PR #83](https://github.com/jposluns/grc_library/pull/83) with number-stable wording rather than a literal bump (literal would re-drift on next pack bump).
  - **Classification-convention follow-up** x 1, out-of-window: [Subagent A] [R] [track-as-follow-up] `register-sweep-history.md` failure-mode-classes table (lines 47-56) does not document the classification rule that Sweep 1 used when it rolled stale-corpus-count references ("37" prose when gate 38 had landed) into C3 rather than C1. The current convention appears to be "if the primary mechanism is multi-surface miss, classify by mechanism (C3) regardless of symptom shape (prose drift)"; if formalised, the failure-mode-classes table should say so. Surfaced separately to the maintainer for a classification-convention decision.
- **Pre-flight scanner**: returned the same 12 candidates as Sweep 3, all already triaged as false positives; no new candidates surfaced.
- **Sweep value**: caught one prose-drift instance (pack version literal in adopter guide) that the gates would not have caught and that none of the prior sweeps' grep passes surfaced. The new rubric made the synthesis step deterministic: subagent B's report quoted the exact line, the parent applied severity adjudication without ambiguity, and the in-window vs out-of-window split routed each finding to the correct protocol.
- **Resulting PR**: [#83](https://github.com/jposluns/grc_library/pull/83).

### 2026-06-20, Sweep 5 (post-PR-#85; thin sweep)

- **Trigger**: maintainer's standing "run a full validation after every three PRs and merges" cadence, fired after the third PR following Sweep 4 (PRs #83, #84, #85). All three were closure-PRs of Sweep 4 itself (the in-window fix, the register entry, the classification-convention documentation).
- **State at sweep**: library 2026.06.71; spec 1.10.0; pack 1.26.6; 42 corpus gates; 10 pack skills.
- **Scope reduction**: since the closure-PRs were scope-narrow (no audit-programme integrity change, no corpus-wide content change), only Subagent A (recent-PR deep review) was dispatched. Subagents B (corpus-wide stale-reference sweep) and C (audit-programme integrity check) were skipped because they verified the same corpus state in Sweep 4 less than an hour earlier and nothing in the closure-PRs touches their scopes.
- **Findings**: none. The closure-PR set is internally consistent with the Sweep 4 outcomes it records.
- **Pre-flight scanner**: returned 12 known false positives (same set as Sweep 4) plus one new candidate at `dev-security/claude-rules/skills/validation-sweep/SKILL.md:89` triggered by the new synthesis-rubric prose ("Four rules, no ceremony"); also a false positive (the four sub-rules 5.1-5.4 of the rubric, not a governance-rule count). All 13 dismissed.
- **Post-sweep action**: the maintainer observed that the same false positives have surfaced on every sweep since Sweep 3 and asked whether the scanner should be enhanced. The decision (option 3 of the named alternatives) was implemented in [PR #86](https://github.com/jposluns/grc_library/pull/86): in-scanner heuristics plus an exemption file at [`tools/sweep-preflight-exemptions.json`](../tools/sweep-preflight-exemptions.json). After PR #86, the same corpus produces 0 candidates rather than 12-13.
- **Resulting PR**: no fix PR (zero findings); the scanner-enhancement PR #86 is recorded under its own scope.

### 2026-06-20, Sweep 6 (post-PR-#88; full sweep, zero findings)

- **Trigger**: maintainer's standing "run a full validation after every three PRs and merges" cadence, fired after the third PR following Sweep 5 (PRs #86, #87, #88).
- **State**: library 2026.06.74; spec 1.10.0; pack 1.26.8; 42 corpus gates; 10 pack skills.
- **First sweep to apply two new disciplines together**: the four-rule synthesis rubric (PR #82) and the pre-tool verification preamble (PR #88). Subagent B's report explicitly tracked its pre-tool preamble usage ("4 grep/read calls, each with hypothesis/falsifier/prior-result"), the first observable use of the discipline.
- **Pre-flight scanner**: post-PR-86 scanner returned 1 candidate (down from 12-13 in prior sweeps) at `governance/register-sweep-history.md:119`, the Sweep 5 entry's meta-quote of the prior "Four rules, no ceremony" false positive. Triaged as the register's narrative quoting past state; added to the exemption file in this PR (`tools/sweep-preflight-exemptions.json` entry for `register-sweep-history.md:119` with line_hash `90a973f0358432ef`). Post-exemption: 0 candidates.
- **Findings**: none across all three subagents (A: recent-PR deep review; B: corpus-wide stale-reference; C: audit-programme integrity).
- **Sweep value**: confirmed that the two new disciplines are in lock-step. The scanner noise reduction (PR #86) and the pre-tool preamble (PR #88) together delivered a sweep where the only candidate surfaced was a known-shape meta-quote in the register itself, which the false-positive memory mechanism handles. The cycle is now genuinely converging: 4+ findings in Sweep 1, 3 in Sweep 2, 1 in Sweep 3, 1 in Sweep 4, 0 in Sweep 5, 0 in Sweep 6.
- **Resulting PR**: this PR ([#89](https://github.com/jposluns/grc_library/pull/89)) for the register entry + exemption update. No fix PR (zero findings).

### 2026-06-20, Sweep 7 (post-PR-#91; thin; empty-delta convergence reached)

- **Trigger**: maintainer's standing "run a full validation after every three PRs and merges" cadence, fired after the third PR following Sweep 6 (PRs #89, #90, #91, all workflow-prose PRs with no corpus-content change).
- **State**: library 2026.06.77; spec 1.10.0; pack 1.26.9; 42 corpus gates; 10 pack skills.
- **First sweep to formally apply the new convergence-delta termination conditions** (from PR #91). Subagents B and C skipped because their scopes (corpus-wide stale-reference sweep, audit-programme integrity check) had no surface changes since Sweep 6 less than an hour earlier; per the pre-tool verification preamble, rerunning them would be corroboration-seeking with an undefined falsifier.
- **Pre-flight scanner**: 17 candidates suppressed (11 by heuristic, 6 by exemption file), 0 candidates surfaced.
- **Findings**: none (Subagent A only; B and C scope-skipped).
- **Empty-delta primary stop applies**: Sweep 7 finding-set is empty; Sweep 6 finding-set was empty. The dedupe-key-equal empty-set match satisfies the primary termination condition introduced in PR #91. The cycle has reached a fixed point for the current corpus.
- **Convergence pattern across all 7 sweeps**: 4+, 3, 1, 1, 0, 0, 0. Three consecutive zero-finding sweeps is a strong fixed-point signal. The discipline is genuinely converging, not just exhausting itself.
- **Sweep value**: confirmed that the new termination conditions fire correctly on a real empty-delta. The discipline is observable: Subagent A's report explicitly named hypothesis/falsifier/prior-result in its pre-tool preamble, the synthesis rubric handled the (empty) finding-set, and the convergence-delta termination resolved on empty-delta primary.
- **Resulting PR**: this PR for the register entry. No fix PR (zero findings).

## False-positive memory

Findings the maintainer has triaged as not-a-real-finding. Subsequent sweeps should not re-surface these; if they do, the maintainer's prior triage is the answer.

*(None yet. First entries will appear as sweeps surface findings the maintainer dismisses.)*

## Recurring-class summary

Cumulative count of findings per class, across all sweeps:

| Class | Total findings (primary) | Last seen |
| --- | --- | --- |
| C1: stale-prose | 2 | Sweep 4 |
| C3: multi-surface-incomplete | 6 | Sweep 3 |
| Discipline self-violation (new) | 1 | Sweep 2 |

Other classes (C2, C4, C5, C6, C7, C8): zero primary-class findings in the four sweeps run to date.

**Secondary-class participation** (per the classification convention documented above): no historical findings carry a secondary class because historical entries were classified before the convention was established. Sweep 5 onwards will populate this footnote when a finding's primary mechanism differs from its symptom shape.

**Reading the table**: C3 (multi-surface incompleteness) remains the dominant failure class at 6 cumulative findings; C1 (stale-prose) is at 2 after Sweep 4 surfaced a pack-version literal in the adopter guide. Sweeps 5, 6, and 7 all produced zero primary-class findings (convergence: 4+, 3, 1, 1, 0, 0, 0). Sweep 7 was the first to formally apply the new empty-delta primary stop from PR #91 and reached fixed-point convergence cleanly. The project's accumulated mechanical defences against C3 (gates 35 gate-name parity, 39 gate-count consistency, 41 collection-enumeration consistency) close the gate-shaped C3 surface, but the prose-and-numbering-shaped C3 surface (Sweep 3 step-numbering drift) and prose-version literals (Sweep 4 adopter-guide `currently `1.22.0``) still fall to the semantic subagent layer. PR #86 closed the recurring-noise problem; PR #88 made subagent tool calls auditable; PR #91 formalised when to stop iterating. The underlying cross-document term-and-identifier consistency gap remains as a candidate for a future mechanical gate.

## Maintenance protocol

- A new sweep entry is appended after each `/validation-sweep` invocation that produces actionable findings. Trivial sweeps (zero findings) may be recorded as a single line under a "trivial sweeps" sub-section if the maintainer wishes; otherwise omitted.
- Each entry includes the trigger reason, state, finding counts per class, and the resulting PR (if any).
- A finding dismissed as not-a-real-finding is recorded in the false-positive memory section with the maintainer's rationale, so a future sweep does not re-litigate.
- The recurring-class summary table is updated cumulatively. When a class accumulates enough findings to suggest a new mechanical gate, the maintainer can use the table as priority signal.

### Dating discipline for deferred findings

Findings the maintainer defers (out-of-window, track-as-follow-up, or otherwise not actioned in the surfacing PR) accumulate ageing risk: without a date stamp, a 6-month-old follow-up is indistinguishable from a 6-day-old one, and the operator loses the prioritisation signal Wikipedia editors get from `{{citation needed|date=June 2024}}`-style maintenance tags. The convention:

- **`surfaced: YYYY-MM-DD` on every deferred finding entry.** ISO 8601, sortable lexicographically. The date is when the sweep first surfaced the finding, not when the maintainer noticed. Missing field is a documentation defect.
- **`re-triage-by: YYYY-MM-DD` is optional and defaults to `surfaced + 30 days`.** Mirrors the GitHub `actions/stale` 30-day default and the project's existing exception-register default in `dev-security/claude-rules/governance/change-tracking.md`. When the deadline passes, the maintainer either re-triages (record a `re-triaged: YYYY-MM-DD` line on the entry), closes the follow-up, or extends `re-triage-by` with a one-line rationale.
- **A future `lint-followup-ageing.py` gate is queued** to fail the build when `today() > re-triage-by` and the entry has no fresh `re-triaged:` trailer. Not implemented this PR; the convention ships now (low scope), the gate is queued as an "extending the framework" task.

Sources: Wikipedia `{{citation needed|date=...}}` maintenance-template convention; GitHub `actions/stale` 30-day default; Self-Admitted Technical Debt (SATD) issue-tracker dating (Bavota and Russo, arXiv:2007.01568); ISO 8601 audit-trail encoding. Recreated as CC BY-SA 4.0 prose; no external rule files imported.

Existing deferred findings in this register (e.g. the Sweep 3 follow-up on cross-document term-and-identifier consistency, the Sweep 4 classification-convention follow-up) were surfaced before this convention existed; they are not retro-stamped. The convention applies to findings deferred from Sweep 7 onwards.

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 |
| --- | --- | --- | --- |
| Audit trail of verification activity | PS.1, RV.2 | LOG-02, LOG-08 | A.8.15 |
| Trend analysis of defect categories | RV.1 | GRC-05 | A.5.36 |
| Documented false-positive handling | PO.5 | GRC-04 | A.5.4 |
