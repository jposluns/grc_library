# Validation Sweep History Register

**Document Title:** Validation Sweep History Register\
**Document Type:** Register\
**Version:** 1.3.0\
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

**Reading the table**: C3 (multi-surface incompleteness) remains the dominant failure class at 6 cumulative findings; C1 (stale-prose) is now at 2 after Sweep 4 surfaced a pack-version literal in the adopter guide. The project's accumulated mechanical defences against C3 (gates 35 gate-name parity, 39 gate-count consistency, 41 collection-enumeration consistency) close the gate-shaped C3 surface, but the prose-and-numbering-shaped C3 surface (Sweep 3: cross-file step-numbering drift between a SKILL.md heading and a slash-command numbered step) and prose-version literals (Sweep 4: `currently `1.22.0`` in the adopter guide) still fall to the semantic subagent layer. Two consecutive sweeps now point at the same gap: the next mechanical gate worth considering is a cross-document term-and-identifier consistency check (something that can detect stale version literals and inconsistent step identifiers across parallel surfaces) beyond the existing collection-enumeration scope.

## Maintenance protocol

- A new sweep entry is appended after each `/validation-sweep` invocation that produces actionable findings. Trivial sweeps (zero findings) may be recorded as a single line under a "trivial sweeps" sub-section if the maintainer wishes; otherwise omitted.
- Each entry includes the trigger reason, state, finding counts per class, and the resulting PR (if any).
- A finding dismissed as not-a-real-finding is recorded in the false-positive memory section with the maintainer's rationale, so a future sweep does not re-litigate.
- The recurring-class summary table is updated cumulatively. When a class accumulates enough findings to suggest a new mechanical gate, the maintainer can use the table as priority signal.

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 |
| --- | --- | --- | --- |
| Audit trail of verification activity | PS.1, RV.2 | LOG-02, LOG-08 | A.8.15 |
| Trend analysis of defect categories | RV.1 | GRC-05 | A.5.36 |
| Documented false-positive handling | PO.5 | GRC-04 | A.5.4 |
