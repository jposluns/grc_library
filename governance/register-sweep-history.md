# Validation Sweep History Register

**Document Title:** Validation Sweep History Register\
**Document Type:** Register\
**Version:** 1.0.0\
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

## False-positive memory

Findings the maintainer has triaged as not-a-real-finding. Subsequent sweeps should not re-surface these; if they do, the maintainer's prior triage is the answer.

*(None yet. First entries will appear as sweeps surface findings the maintainer dismisses.)*

## Recurring-class summary

Cumulative count of findings per class, across all sweeps:

| Class | Total findings | Last seen |
| --- | --- | --- |
| C1: stale-prose | 1 | Sweep 2 |
| C3: multi-surface-incomplete | 5 | Sweep 2 |
| Discipline self-violation (new) | 1 | Sweep 2 |

Other classes (C2, C4, C5, C6, C7, C8): zero findings in the two sweeps run to date.

**Reading the table**: C3 (multi-surface incompleteness) is the dominant failure class so far. This is consistent with the project's history: the audit programme has multiple parallel surfaces (workflow, runner, pre-commit, spec inventory; pack README + project CLAUDE + pack CLAUDE for governance enumeration; etc.) and the per-PR discipline of updating all surfaces is the most-violated. The Layer 2 mechanical gates (35 gate-name parity, 39 gate-count consistency, 41 collection-enumeration consistency) are the project's accumulated mechanical defences against C3; they have closed the C3 instances the sweep would otherwise re-discover each invocation.

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
