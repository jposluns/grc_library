# Removed from skills/skill-authoring-discipline/SKILL.md (pack-hygiene scrub)

Each entry below preserves, verbatim, a passage removed from the skill during the
generalize-in-place scrub, with the generic replacement that took its place. Concrete
project values now live only in the skill's "Project wiring" section.

## Frontmatter `description` line

```
description: When adding a new skill to the `dev-security/claude-rules/skills/` pack, or when substantively revising an existing skill's structure or frontmatter, apply the pack's established eight-section structural template (YAML frontmatter with `derives_from`, Overview, When-to-Use, Process, Red Flags, Verification, Common Rationalizations, See Also) and validate trigger-accuracy with representative positive, negative, and boundary prompts. Catches structural drift across pack skills that accumulates silently as the pack grows: section compression, missing cross-references, missing rationalizations table, vague description wording. The mechanical gate 32 only verifies `derives_from` resolution; everything else relies on authorial discipline that this skill codifies.
```

Generic replacement: "the governance pack's `skills/` collection" and "The mechanical derives-from reference gate only verifies `derives_from` resolution"; the concrete gate number moved to the project-wiring section.

## Overview, paragraph 1 (gate naming)

```
The pack's mechanical gate 32 (Skill derives-from reference audit) enforces only one of these structural properties (the `derives_from` field); the others rely on authorial discipline.
```

Generic replacement: "The pack's mechanical derives-from reference gate enforces only one of these structural properties (the `derives_from` field); the others rely on authorial discipline."

## When to Use, bullet 1 (pack path)

```
- Before adding a new SKILL.md to `dev-security/claude-rules/skills/`. The skill is the discipline that gates the addition.
```

Generic replacement: "Before adding a new SKILL.md to the pack's `skills/` directory." (rest of the bullet unchanged).

## Process step 2 (governance-rule path)

```
Every pack skill derives from one of the governance rules under `dev-security/claude-rules/governance/`.
```

Generic replacement: "Every pack skill derives from one of the governance rules under the pack's `governance/` directory."

## Process step 7, README-tree bullet (gate naming)

```
   - **Pack README skills tree**: add the new skill to the `├── skills/` tree section in [`../../README.md`](../../README.md). Gate 41 (collection-enumeration consistency audit) enforces this.
```

Generic replacement: the same bullet with "The collection-enumeration parity gate named in the project wiring enforces this."

## Process step 7, link-depth bullet (pack path, tool link, gate number)

```
   - **Repository-internal link depth**: a SKILL.md sits at `dev-security/claude-rules/skills/<name>/SKILL.md`, so its relative links resolve from that depth: a pack governance rule is `../../governance/<rule>.md`, a sibling skill is `../<name>/SKILL.md`, and a repository-root tool or document is `../../../../<path>` (for example [`../../../../tools/run_all_audits.sh`](../../../../tools/run_all_audits.sh)). Gate 3 (broken-link) catches a wrong depth, but author it correctly the first time rather than relying on the gate.
```

Generic replacement: "a SKILL.md sits at `skills/<name>/SKILL.md` inside the pack", the repository-root depth stated as "whatever depth the pack sits in the consuming repository (in the parent library's layout, four levels up: `../../../../<path>`; the audit runner named in the project wiring is one such target)", and "The broken-link gate catches a wrong depth".

## Process step 7, PAIRS bullet (tool link and gate number)

```
   - **Slash-command sibling and PAIRS registry (paired skills only)**: if the skill is invoked by a `/<name>` slash command, create the sibling `.claude/commands/<name>.md` summary file, AND register the `(skill_path, command_path)` pair in the `PAIRS` list of [`../../../../tools/lint-paired-skill-step-parity.py`](../../../../tools/lint-paired-skill-step-parity.py) so gate 44 (paired-skill step-parity) verifies that the two files use the same step identifiers. A paired skill that is not registered in PAIRS inherits no parity check: that silent drift is the failure mode the registry exists to prevent.
```

Generic replacement: the same bullet with "the `PAIRS` list of the step-parity linter named in the project wiring, so the paired-skill step-parity gate verifies that the two files use the same step identifiers".

## Process step 7, language pre-flight bullet (tool link, gate number, close-out-checklist cross-reference)

```
   - **Language pre-flight**: run [`../../../../tools/lint-language.py`](../../../../tools/lint-language.py) on the new SKILL.md before the first commit. Freshly authored pack prose recurrently reintroduces em-dashes and British `-ise` spellings that gate 2 will block; catching them pre-commit avoids a fix-up commit (this is the close-out checklist's new-pack-prose rule applied at skill-authoring time).
```

Generic replacement: "run the language pre-flight linter named in the project wiring on the new SKILL.md before the first commit ... that the language gate will block; catching them pre-commit avoids a fix-up commit." The parenthetical tying the step to the parent library's PR close-out checklist is project process history and was dropped.

## Process step 8 (audit runner and gate numbers)

```
8. **Verify against the audit programme**. After the SKILL.md is committed, run `tools/run_all_audits.sh`. Gate 32 verifies the `derives_from` field resolves. Gate 41 verifies the README tree is in sync.
```

Generic replacement: "run the audit runner named in the project wiring. The derives-from reference gate verifies the `derives_from` field resolves; the collection-enumeration parity gate verifies the README tree is in sync."

## Verification, bullet 1 (pack path)

```
- The proposed SKILL.md is present in `dev-security/claude-rules/skills/<name>/SKILL.md` and follows the eight-section structural template.
```

Generic replacement: "present at `skills/<name>/SKILL.md` inside the pack".

## Verification, parallel-surface bullet (tool path)

```
- Every parallel surface is wired (step 7): the pack README skills tree includes the new skill; the repository-internal links resolve at the correct depth; and, for a slash-command-paired skill, the `.claude/commands/<name>.md` sibling exists AND the pair is registered in the `PAIRS` list of `tools/lint-paired-skill-step-parity.py`.
```

Generic replacement: "the pair is registered in the step-parity linter's `PAIRS` list".

## Verification, language bullet (tool name)

```
- `lint-language.py` was run on the new SKILL.md before the first commit (no em-dashes, no British `-ise`).
```

Generic replacement: "The language pre-flight was run on the new SKILL.md before the first commit (no em-dashes, no British `-ise`)."

## Verification, audit-programme bullet (gate-number enumeration)

```
- The full audit programme passes standalone after the SKILL.md is committed (gates 32, 41, 44, 3, and 2 in particular).
```

Generic replacement: "(the derives-from, collection-enumeration, step-parity, broken-link, and language gates in particular)"; the concrete gate numbers moved to the project-wiring section.

## Common Rationalizations, final row (gate number)

```
| "I added the SKILL and the README tree; the slash-command wiring can come later." | A paired skill not registered in the `PAIRS` list (and missing its `.claude/commands/` sibling) inherits no step-parity check, the exact silent drift gate 44 exists to catch. Wire all of step 7's surfaces in the same change, not "later". |
```

Generic replacement: the same row with "the exact silent drift the paired-skill step-parity gate exists to catch".

## See Also, final bullet (pack README path)

```
- The pack README's `## Version history` section (in `dev-security/claude-rules/README.md`) records each skill addition with the pack-minor-bump convention; this skill's addition is itself an instance of that pattern.
```

Generic replacement: the same bullet with "(in the pack's `README.md`)".
