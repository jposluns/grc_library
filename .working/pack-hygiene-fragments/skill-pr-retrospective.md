# Removed from skills/pr-retrospective/SKILL.md (pack-hygiene scrub)

Each entry preserves the verbatim original text that the pack-hygiene generalization
removed or reworded, with the location and the replacement that now stands in the SKILL.

## Overview, output-register paragraph (register path and FR column naming)

```
The output is the **improvement-log register** at `.working/improvement-log.md` (this project's path; adopters relocate to a project-appropriate location). The register is append-only at the row level, ordered by PR number; the step-6 disposition scan appends tokens to earlier rows' Proposed-improvement cells without rewriting their original text. Each row carries the date, PR number, FR closed (if any), what-went-well note, friction note, pattern-surfaced note (if any), and proposed improvement (if any).
```

Replacement: the register is named generically ("the improvement-log register"), the concrete `.working/improvement-log.md` path moved to the new project-wiring section, and "FR closed" became "backlog item closed".

## Overview, learning-loop paragraph (hallucination-metrics link)

```
The skill is **the orchestrator-side process-improvement loop**. It pairs with the worker-side `worker-brief-template.md` (per [`governance/ai-assistant-workflow-disciplines.md`](../../governance/ai-assistant-workflow-disciplines.md) §1 hallucination-assessment update protocol) and the apply-time-catch tracking in [`hallucination-metrics.md`](../../../../.working/hallucination-metrics.md). Together the three close the per-PR learning loop:
```

Replacement: "the apply-time-catch tracking in the worker-hallucination metrics register (both named in the project wiring above)"; the concrete `.working/hallucination-metrics.md` path moved to the project-wiring section; the pack-internal rule link is retained.

## Process step 1, capture bullets (FR wording and hallucination-metrics link)

```
Capture:
- PR number, merge commit SHA, FR(s) closed (if any).
- The `/validate-pr` findings just returned (0 findings, N findings with categories, or out-of-window observations).
- Any apply-time worker corrections logged in [`hallucination-metrics.md`](../../../../.working/hallucination-metrics.md) during the PR.
- Recently-shipped PRs in the same cluster (for pattern surfacing).
```

Replacement: "backlog item(s) closed (if any)" and "logged in the worker-hallucination metrics register during the PR".

## Process step 3, friction example (FR-114)

```
- "FR-114 double-counted across the maintainer-decided and active-verified buckets."
```

Replacement: anonymized to "A backlog finding double-counted across two triage buckets."

## Process step 4, pattern examples (concrete PR numbers)

```
- "Third consecutive findings-producing /validate-pr (#187 → 2; #188 → 2; #189 → 2). Pattern: meta-PRs that touch fitness-review and validation artefacts introduce subtle multi-surface drift."
- "Recurring acronym-expansion gap in adopter-facing surfaces (PR #172 README; PR #179 README; PR #196 README). Pattern: each new README polish needs first-occurrence expansion checked against the existing convention."
```

Replacement: example output shapes kept with anonymized placeholders, "(#N → 2; #N+1 → 2; #N+2 → 2)" and "(PR #N README; PR #M README; PR #P README)".

## Process step 5, improvement examples (linter path and PR #187 provenance)

```
- "Add a regression-test fixture exercising CGNAT detection to `tools/lint-pii-in-content.py`."
```

```
- "Codify the no-skip-discretion discipline in the validation-sweep-pr-scoped SKILL." (this was the PR #187 retrospective outcome, retroactively.)
```

Replacement: the linter is named generically ("the PII-in-content linter"); the provenance parenthetical became "(an actual early retrospective outcome in the parent library, recorded retroactively.)".

## Output format section (register path link, FR column, sibling-register path)

````
Append a row to [`.working/improvement-log.md`](../../../../.working/improvement-log.md):

```
| Date | PR | FR closed | What went well | Friction | Pattern (if any) | Proposed improvement |
|---|---|---|---|---|---|---|
| YYYY-MM-DD | #N | FR-X (if any) | [1-2 sentences] | [1-2 sentences] | [1 sentence, blank if none] | [1 sentence, blank if none] |
```

New rows on top (reverse-chronological, matching the validate-pr/history.md convention).

The register's preamble describes the column semantics and links to this SKILL.
````

Replacement: "Append a row to the improvement-log register (named in the project wiring above)"; the "FR closed" / "FR-X (if any)" cells became "Backlog item closed" / "item id (if any)"; "matching the validate-pr/history.md convention" became "matching the per-PR validation-sweep history register's convention" (the concrete `.working/validate-pr/history.md` path is in the project-wiring section).

## Verification section, register-entry bullet (FR wording)

```
- Register entry includes the date, PR number, FR closed (if any), and the short observation cells; any disposition tokens from the step-6 scan are appended to the originating rows.
```

Replacement: "backlog item closed (if any)".

## See Also section, project-local register bullets

```
- Worker-brief template at `.working/worker-brief-template.md` (project-local): codifies worker-side guard rails that `/retro` patterns may surface as additions.
- [`hallucination-metrics.md`](../../../../.working/hallucination-metrics.md) (project-local): tracks apply-time worker corrections that `/retro` may surface as pattern candidates.
```

Replacement: both bullets now name the artefacts generically ("Worker-brief template (project-local; named in the project wiring above)"; "Worker-hallucination metrics register (project-local; named in the project wiring above)"); the concrete `.working/` paths live in the project-wiring section.
