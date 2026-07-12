# Removed from skills/claim-fit/SKILL.md (pack-hygiene scrub)

Each entry records a project-specific passage removed or genericized in the pack-hygiene
generalization pass, verbatim as it stood before the scrub, with one line naming what
replaced it. Project-specific tool paths, reference-base paths, and gate numbers now live
in the skill's `## Project wiring` section.

## Frontmatter `description` (project-identified clauses)

```
description: Cadenced citation-precision audit of normative-attribution claims. Catches the gate-blind FR-120 class, "attributed value, silent source": a sentence ties a specific value (a retention period, a clock, a threshold) to a named normative source, the source exists and the citation is well-formed (so the existence and citation gates pass), but the source does not actually prescribe the attributed value. Run the one-time full Tier-A pass at adoption, then ad-hoc when a claim is in doubt and after any batch that adds or edits normative-value claims. It dispatches a semantic judge over the tiered worklist that `tools/audit-claim-precision.py` produces, adjudicating each claim against the held source TEXT in the reference base, then routes confirmed misattributions. It catches what the existence gates structurally cannot: claim precision needs a read of the source clause, not a source-exists check.
```

Replaced by the same description with "the gate-blind FR-120 class" genericized to "the gate-blind \"attributed value, silent source\" class" and the tool path genericized to "the project's recall-oriented pre-filter".

## Overview, paragraph 2 (the identified motivating incident and census)

```
The class is not hypothetical. The motivating incident (FR-120, PR #294): a policy attributed a fixed "180-day baseline" to NIST SP 800-53 CA-6 and ISO/IEC 27001 Clause 9.2, and neither source prescribes a fixed interval. The census that shipped with the triage tool surfaced the standing candidate shapes: three carriers attributing a 7-year retention to ISO/IEC 42001 plus EU AI Act Annex IV (the ISO half informs the figure without prescribing it; the Annex IV half, the adoption pass found, carries no retention obligation at all; the value is the corpus's own canonical choice per DD-6/DD-7), and a 24-hour supplier-notification KPI citing GDPR Article 33(2), which sets "without undue delay", not a fixed clock.
```

Replaced by the same paragraph with the FR-120 / PR #294 identifiers dropped ("The motivating incident in the parent library") and "per DD-6/DD-7" genericized to "recorded as such in the project's decision trail"; the external standard names are retained as generic teaching content.

## Overview, paragraph 3 (tool path and FR-120 shape reference)

```
`claim-fit` is the semantic-judge half of a two-part instrument whose recall-oriented triage half is the advisory tool `tools/audit-claim-precision.py` (explicitly NOT a gate; always exits 0; CI cannot host the check because the ground truth lives in the sibling private reference repo). The tool tiers the worklist by risk: TIER A rows (a specific value tied to a named normative source in one clause, both orders, the exact FR-120 shape) are judged EVERY one; TIER B rows (soft-alignment phrasing with no specific value) are sampled on cadence.
```

Replaced by "the advisory pre-filter named in the project wiring above" and "the exact motivating-incident shape"; the rest of the paragraph is unchanged.

## Verdict bullet `informed-not-prescribed` (design-decision ids)

```
- **`informed-not-prescribed`**: the source motivates the value but does not state it (the 7-year DD-6/DD-7 shape).
```

Replaced by "(the 7-year retention shape from the census above)".

## Verdict bullet `mis-attributed` (FR id)

```
- **`mis-attributed`**: the source states a different value, or none, where the sentence asserts one (the FR-120 and Article 33(2) shapes).
```

Replaced by "(the motivating-incident and Article 33(2) shapes)".

## Verdict bullet `source-not-held` (design-decision id)

```
(the evidence-grounded-completion external-version corollary and the DD-10 egress constraint both bind here)
```

Replaced by "(the evidence-grounded-completion external-version corollary binds here, as does any project egress constraint on fetching new sources)".

## When to Use, second bullet (backlog-phase id)

```
- **After any batch that adds or edits normative-value claims** (a P2-style content batch, a jurisdiction annex, a KPI or SLA table): run the tool, judge the NEW Tier-A rows the batch introduced, and sample its Tier-B rows.
```

Replaced by "(a substantive content batch, a jurisdiction annex, a KPI or SLA table)".

## Process step 1 (runner path and reference-base paths)

```
Name the scope for this run: the full Tier-A census (the adoption pass), the rows a just-applied batch introduced (the per-batch cadence), or a flagged set (the ad-hoc cadence). Confirm `tools/run_all_audits.sh` exits 0 first; a precision pass judges among claims that already pass the mechanical gates. Confirm the reference base is available: the `grc_library_ref` indexes (`grc_library_ref/INDEX.md`, `grc_library_ref/catalogue.yml`, `grc_library_ref/SECTION-INDEX.md`) locate the held source texts, and the per-source currency rule applies (confirm a held source is current before relying on it, per the `grc_library_ref` invariants; a superseded held text is grounds to defer, not to judge against the stale text silently).
```

Replaced by "the project's all-gates suite (named in the project wiring above)", "its indexes locate the held source texts", and "per the reference base's own invariants".

## Process step 2 (tool invocation and reference-base index name)

```
Run `python3 tools/audit-claim-precision.py --ref-base <path-to-grc_library_ref-checkout>` (add `--tier A` for the Tier-A-only cadence). The tool always exits 0; its output is a recall-oriented worklist, tiered, with each named source family's held-state reported best-effort from the grc_library_ref indexes.
```

Replaced by "Run the recall-oriented pre-filter named in the project wiring, pointing it at the reference base (restrict to Tier A for the Tier-A-only cadence)" and "from the reference-base indexes"; the concrete invocation and flags now live in the project wiring section.

## Process step 3 (reference-base index name)

```
The judge brief: locate the named source's held text via the `grc_library_ref` indexes, read the specific clause, article, or annex the claim points at,
```

Replaced by "via the reference-base indexes".

## Red Flags, fourth bullet (design-decision ids)

```
- Fixing an `informed-not-prescribed` finding by changing the VALUE. The value is frequently the corpus's own canonical choice (DD-6/DD-7 class); the defect is the attribution phrasing, and silently changing a canonical value is an authorial decision the maintainer owns.
```

Replaced by "(the canonical-choice class the census above illustrates)".

## Verification, first bullet (runner path)

```
- The scope was named and the mechanical baseline was clean (`tools/run_all_audits.sh` exit 0) before the semantic read.
```

Replaced by "(the project's all-gates suite exit 0)".

## See Also, advisory-tool bullet (tool path, link, and flags)

```
- The advisory tool [`tools/audit-claim-precision.py`](../../../../tools/audit-claim-precision.py): the recall-oriented triage step that feeds this skill's worklist (not a gate; always exits 0; `--tier A` for the judge-every-row tier, `--ref-base` to report source held-state from the reference-base indexes).
```

Replaced by "The recall-oriented pre-filter named in the project wiring above: ..." with the flags restated generically; the concrete path and flags now live in the project wiring section.

## See Also, reference-base bullet (repository name and index paths)

```
- The reference base: the `grc_library_ref` repo located via its indexes (`grc_library_ref/INDEX.md`, `grc_library_ref/catalogue.yml`, `grc_library_ref/SECTION-INDEX.md`), with the per-source currency confirmation and trust-bucket rules the `grc_library_ref` repo's own conventions define.
```

Replaced by "The reference base named in the project wiring above: located via its own indexes, ..."; the concrete repository name and index paths now live in the project wiring section.
