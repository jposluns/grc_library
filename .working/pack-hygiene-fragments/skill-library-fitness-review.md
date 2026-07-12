# Removed from skills/library-fitness-review/SKILL.md (pack-hygiene scrub)

Each entry names the location, quotes the removed original verbatim in a fenced block,
and states the generic replacement used. The project-concrete values now live in the
skill's `## Project wiring` section; this file preserves the removed lineage and
project-specific phrasing for the removal ledger.

## Frontmatter, `description`

```
description: Trigger a comprehensive whole-corpus library-fitness review with ten persona reviewers when a governance/security documentation library undergoes a major change (new domain dir, new document type, multiple governance rule additions, major restructure) or quarterly minimum. Each invocation dispatches a fan-out of independent persona subagents (executive, security practitioner, GRC practitioner, auditor, policy editor, process owner, skeptical reader, adoption practitioner, privacy officer, newcomer) who review every page from a fresh-reader perspective without inheriting maintainer mental models.
```

Replacement: "with a project-defined catalogue of persona reviewers" and a short example list "(for example an executive reader, a security practitioner, an auditor, a newcomer)"; the rest of the description line is unchanged.

## Overview, second paragraph

```
It runs heavyweight (10 persona subagents dispatched in parallel; whole-corpus scope) and infrequently
```

Replacement: "It runs heavyweight (the full persona catalogue dispatched in parallel; whole-corpus scope) and infrequently".

## When to Use, "On demand" bullet

```
The 10-persona fan-out surfaces what the maintainer's recall does not.
```

Replacement: "The full persona fan-out surfaces what the maintainer's recall does not."

## When to Use, "Not when" second bullet

```
The cost (10 persona dispatches) doesn't match the scope.
```

Replacement: "The cost (a full persona fan-out) doesn't match the scope."

## When to Use, "Not when" fourth bullet

```
(per Citation Verification Specification §14, the library does not verify standard content vs. library interpretation)
```

Replacement: "(per the citation-accuracy boundary named in the project wiring, the library does not verify standard content vs. library interpretation)"; the concrete specification and its §14 are recorded in the project-wiring bullet.

## Process step 1 (Establish mechanical baseline)

```
Run `tools/run_all_audits.sh` (or the project's equivalent) standalone.
```

Replacement: "Run the project's full mechanical audit suite (the baseline command named in the project wiring) standalone."

## Process step 2 (Identify scope and run ordinal)

```
The run ordinal is the next `N` after the most recent entry in `.working/fitness-reviews/history.md`.
```

Replacement: "The run ordinal is the next `N` after the most recent entry in the history register named in the project wiring."

## Process step 3, persona-brief bullet

```
the persona briefs in `.working/fitness-reviews/README.md` are the canonical source for this project's personas.
```

Replacement: "the persona briefs in the catalogue document named in the project wiring are the canonical source for the project's personas."

## Process step 3, persona-list introduction

```
The ten personas (project-specific catalogue in `.working/fitness-reviews/README.md`):
```

Replacement: "In the parent library the persona catalogue (the document named in the project wiring) defines these lenses; an adopting project defines its own:". The enumerated persona list itself was retained in the body as the parent library's worked example.

## Process step 3, dispatch instruction

```
Dispatch all ten on every full run.
```

Replacement: "Dispatch the full catalogue on every full run."

## Process step 5, intro paragraph (verification-discipline precedent)

```
The verification discipline added at PR #139 catches the failure mode where a synthesis-stage approximation propagates downstream as if confirmed (the precedent: PR #124's "95 unique findings, 18 H[critical] / 22 H / 31 M / 24 L" wording, corrected to the mechanical tabulation 111 / 17 / 20 / 57 / 17 in PR #127; the same failure mode at finding-content granularity would be worse).
```

Replacement (anonymized, lesson kept): "This verification discipline catches the failure mode where a synthesis-stage approximation propagates downstream as if confirmed (the precedent in the parent library: a run report's summary count and severity tabulation, written from the synthesis narrative rather than recounted mechanically from the finding rows, shipped wrong and was corrected only in a follow-up change; the same failure mode at finding-content granularity would be worse)."

## Process step 6, opening sentence

```
Single combined Markdown file at `.working/fitness-reviews/YYYY-MM-DD-rN.md` (this project's path; adopters relocate to a project-appropriate location). Eight H2 sections in this order (see `.working/fitness-reviews/README.md` for full content spec):
```

Replacement: "Single combined Markdown file at the run-record path named in the project wiring (date-and-run-ordinal named; adopters relocate to a project-appropriate location). Eight H2 sections in this order (see the catalogue document named in the project wiring for the full content spec):"

## Process step 7, opening sentence

```
Add a row to the top of `.working/fitness-reviews/history.md` with columns:
```

Replacement: "Add a row to the top of the history register named in the project wiring with columns:"

## Process step 7, Personas-column bullet

```
- **Personas** is `A through J` for a full ten-persona dispatch, or a comma-separated subset for a scoped run (rare; with authorization reason in the Summary cell).
```

Replacement: "**Personas** is the register's full-dispatch marker for a full-catalogue dispatch, or a comma-separated subset for a scoped run (rare; with authorization reason in the Summary cell)." The `A through J` marker is recorded in the project-wiring history-register bullet.

## Process step 9, backlog-table bullet

```
- Update the **Open remediation backlog** table in `.working/fitness-reviews/history.md` with each item's status (`pending` / `in-progress` / `closed`) and the assigned PR.
```

Replacement: "Update the **Open remediation backlog** table in the history register named in the project wiring with each item's status (`pending` / `in-progress` / `closed`) and the assigned PR."

## Red Flags, prior-run bullet

```
"Subagent A returned zero last time, skip this run" is the inference-cascade failure mode the project's 7th pack rule (`validate-inference-before-action`) prevents.
```

Replacement: the pack-ordinal phrasing "the project's 7th pack rule" became "the pack's `validate-inference-before-action` rule" (a pack ordinal is a project-drifting count).

## Red Flags, skipped-personas bullet

```
Full ten-persona dispatch is the default; scoped runs require explicit maintainer authorization recorded in the history-row Summary.
```

Replacement: "Full-catalogue dispatch is the default; scoped runs require explicit maintainer authorization recorded in the history-row Summary."

## Verification, first bullet

```
- All ten personas have been dispatched (or a scoped subset has been authorized by the maintainer with the authorization recorded in the history-row Summary).
```

Replacement: "Every persona in the catalogue has been dispatched (or a scoped subset ...)".

## Verification, report bullet

```
- The combined report (`.working/fitness-reviews/YYYY-MM-DD-rN.md`) has all 8 H2 sections (plus optional `## Final Assessment`) written.
```

Replacement: "The combined report (at the run-record path named in the project wiring) has all 8 H2 sections (plus optional `## Final Assessment`) written."

## Verification, history-row bullet

```
- The history-row has been appended to `.working/fitness-reviews/history.md` with all columns populated.
```

Replacement: "The history-row has been appended to the history register named in the project wiring with all columns populated."

## Common Rationalizations, persona-count row

```
| "Ten personas is overkill for our small library." | The persona count is tuned to the failure-mode space, not the library size. Each persona catches a class of finding the others systematically miss. Reducing to 5 personas drops 5 classes of finding. If the library is genuinely small, the run is fast (fewer pages); persona count stays constant. |
```

Replacement: "A full persona catalogue is overkill ..." / "The catalogue is tuned to the failure-mode space ... Dropping personas drops finding classes ... the catalogue stays constant." (count-free phrasing).

## Common Rationalizations, auditor-persona row (final sentence)

```
Run the full ten-persona dispatch every time.
```

Replacement: "Run the full-catalogue dispatch every time."

## Common Rationalizations, consolidation row (rationalization cell)

```
| "The personas overlap; let me consolidate to 5." |
```

Replacement: "The personas overlap; let me consolidate to fewer." (reality cell unchanged).

## See Also, `validation-sweep` bullet (final sentence)

```
See `.working/fitness-reviews/README.md` § "Relationship to `validation-sweep`" for the comparison table.
```

Replacement: "See the catalogue document named in the project wiring, its \"Relationship to `validation-sweep`\" section, for the comparison table."

## See Also, `fresh-reader-validation` bullet

```
`library-fitness-review` runs ten personas on the whole corpus.
```

Replacement: "`library-fitness-review` runs the full persona catalogue on the whole corpus."

## See Also, evidence-grounded-completion bullet

```
the skill operationalizes evidence-grounded-completion across ten parallel lenses.
```

Replacement: "the skill operationalizes evidence-grounded-completion across the catalogue's parallel lenses."

## See Also, activity-convention-document bullet

```
- The activity convention document at `.working/fitness-reviews/README.md` (this project's path; adopters relocate to a project-appropriate location): the canonical source for the project-specific persona catalogue, the severity-model definitions, the per-run file format, and the operational guidance.
```

Replacement: "The activity convention document named in the project wiring (adopters relocate to a project-appropriate location): the canonical source ..." (rest unchanged).
