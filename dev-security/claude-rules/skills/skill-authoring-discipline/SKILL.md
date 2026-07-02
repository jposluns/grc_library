---
name: skill-authoring-discipline
description: When adding a new skill to the `dev-security/claude-rules/skills/` pack, or when substantively revising an existing skill's structure or frontmatter, apply the pack's established eight-section structural template (YAML frontmatter with `derives_from`, Overview, When-to-Use, Process, Red Flags, Verification, Common Rationalizations, See Also) and validate trigger-accuracy with representative positive, negative, and boundary prompts. Catches structural drift across pack skills that accumulates silently as the pack grows: section compression, missing cross-references, missing rationalizations table, vague description wording. The mechanical gate 32 only verifies `derives_from` resolution; everything else relies on authorial discipline that this skill codifies.
derives_from: ../../governance/evidence-grounded-completion.md
---

# Skill Authoring Discipline

## Overview

Every pack skill ships with the same structural template: YAML frontmatter pointing at a governance rule via `derives_from`; `## Overview` framing the failure mode; `## When to Use` triggers; `## Process` numbered steps; `## Red Flags` anti-patterns; `## Verification` exit criteria; `## Common Rationalizations` an internal-honesty table; `## See Also` cross-references. The pack's mechanical gate 32 (Skill derives-from reference audit) enforces only one of these structural properties (the `derives_from` field); the others rely on authorial discipline.

The failure mode this skill prevents is structural drift: as the pack grows, each subsequent addition is at risk of compressing a section, skipping the Common Rationalizations table because "this one is obvious", or omitting the When-to-Use enumeration because "the description covers it". Drift accumulates silently; a few skills later, the pack reads as a patchwork.

This skill is a checklist + a validation step. The checklist confirms structural template adherence; the validation step confirms the skill's frontmatter `description` triggers reliably on prompts that should invoke it and does not trigger on prompts that should not.

## When to Use

- Before adding a new SKILL.md to `dev-security/claude-rules/skills/`. The skill is the discipline that gates the addition.
- Before substantively revising an existing skill's structure (re-ordering sections, removing sections, changing the frontmatter shape). Cosmetic revisions inside an existing section do not warrant this skill.
- When pack version is about to bump (minor) for a skill addition, this skill's process is the precondition.

## Process

1. **Confirm the skill is needed**. Audit the existing pack skills against the proposed skill's brief. If the proposed skill's process is already covered (or could be covered) by composing two existing skills, drop the proposal. Skill count is not a virtue; coverage of failure modes is.
2. **Identify the parent governance rule**. Every pack skill derives from one of the governance rules under `dev-security/claude-rules/governance/`. Pick the rule whose discipline the proposed skill operationalizes. Multiple skills may derive from the same rule (the validation-sweep + evidence-grounded-completion + citation-quote-verification + fresh-reader-validation triple all derive from evidence-grounded-completion; that is fine).
3. **Apply the structural template**. The proposed SKILL.md must contain, in order:
   - YAML frontmatter with `name`, `description`, `derives_from`.
   - `# <Title>` H1 (single, matching `name`).
   - `## Overview`, failure mode framing, 2-4 paragraphs.
   - `## When to Use`, bulleted enumeration of triggers.
   - `## Process`, numbered steps, each step actionable.
   - `## Red Flags`, bulleted anti-patterns, conversational tone.
   - `## Verification`, bulleted exit criteria.
   - `## Common Rationalizations`, two-column markdown table.
   - `## See Also`, bulleted cross-references to the parent rule and related skills.
4. **Write the description for trigger accuracy**. The frontmatter `description` is the primary trigger for Claude Code's skill discovery. It must:
   - Lead with a clear when-to-use signal ("Before X", "When Y", "On every Z").
   - Name the specific failure mode the skill addresses (one sentence).
   - End with what the skill catches that other mechanisms do not.
   - Be 60-130 words. Shorter is under-triggered; longer is over-triggered.
5. **Validate trigger accuracy with representative prompts**. Run 5-10 prompts past the description (mentally, or in a fresh session, or via a validation subagent):
   - **Positive cases** (should trigger): prompts that describe the failure mode the skill addresses.
   - **Negative cases** (should NOT trigger): prompts that look superficially similar but are out of scope.
   - **Boundary cases**: prompts in the grey zone between this skill and a sibling skill.
   - If any positive case is missed or any negative case is triggered, rewrite the description.
6. **Cross-reference bidirectionally**. Add `## See Also` entries pointing to: the parent governance rule; sibling skills that should be invoked alongside (e.g., before, after, as fallback). Then update those sibling skills' `## See Also` sections to point back at the new skill (uni-directional cross-references rot; bi-directional ones survive maintenance).
7. **Wire the skill into every parallel surface.** A new skill crosses several surfaces beyond its own file; missing any one leaves a gate red or a latent inconsistency, so confirm each:
   - **Pack README skills tree**: add the new skill to the `├── skills/` tree section in [`../../README.md`](../../README.md). Gate 41 (collection-enumeration consistency audit) enforces this.
   - **Repository-internal link depth**: a SKILL.md sits at `dev-security/claude-rules/skills/<name>/SKILL.md`, so its relative links resolve from that depth: a pack governance rule is `../../governance/<rule>.md`, a sibling skill is `../<name>/SKILL.md`, and a repository-root tool or document is `../../../../<path>` (for example [`../../../../tools/run_all_audits.sh`](../../../../tools/run_all_audits.sh)). Gate 3 (broken-link) catches a wrong depth, but author it correctly the first time rather than relying on the gate.
   - **Slash-command sibling and PAIRS registry (paired skills only)**: if the skill is invoked by a `/<name>` slash command, create the sibling `.claude/commands/<name>.md` summary file, AND register the `(skill_path, command_path)` pair in the `PAIRS` list of [`../../../../tools/lint-paired-skill-step-parity.py`](../../../../tools/lint-paired-skill-step-parity.py) so gate 44 (paired-skill step-parity) verifies that the two files use the same step identifiers. A paired skill that is not registered in PAIRS inherits no parity check: that silent drift is the failure mode the registry exists to prevent.
   - **Language pre-flight**: run [`../../../../tools/lint-language.py`](../../../../tools/lint-language.py) on the new SKILL.md before the first commit. Freshly authored pack prose recurrently reintroduces em-dashes and British `-ise` spellings that gate 2 will block; catching them pre-commit avoids a fix-up commit (this is the close-out checklist's new-pack-prose rule applied at skill-authoring time).
8. **Verify against the audit programme**. After the SKILL.md is committed, run `tools/run_all_audits.sh`. Gate 32 verifies the `derives_from` field resolves. Gate 41 verifies the README tree is in sync.

## Red Flags

- Compressing a section because "this skill is small enough". Section consistency across the pack matters more than per-skill brevity.
- Omitting the Common Rationalizations table because "no obvious rationalizations exist". The table is the author's commitment to anticipate the discipline-relaxation moves; if you can't find any, look harder.
- Writing the `description` field after the body. The description is the trigger; it must be the focus of the authoring effort, not an afterthought.
- Skipping trigger-accuracy validation. The skill's effectiveness depends on whether it fires when needed; "I think it'll trigger" is not validation.
- Cross-referencing in one direction only. Bidirectional cross-references survive pack growth; uni-directional ones do not.
- Treating the parent governance rule as ornamental. The `derives_from` field is a structural constraint; the skill's process should be a direct operationalization of the rule.

## Verification

This skill is complete when:

- The proposed SKILL.md is present in `dev-security/claude-rules/skills/<name>/SKILL.md` and follows the eight-section structural template.
- The frontmatter has `name`, `description`, and `derives_from` fields; `derives_from` points at an existing governance rule.
- Trigger-accuracy validation has been performed with at least 5 representative prompts (positive + negative + boundary cases) and the description rewritten if needed.
- Bidirectional `## See Also` cross-references are in place between the new skill and its siblings.
- Every parallel surface is wired (step 7): the pack README skills tree includes the new skill; the repository-internal links resolve at the correct depth; and, for a slash-command-paired skill, the `.claude/commands/<name>.md` sibling exists AND the pair is registered in the `PAIRS` list of `tools/lint-paired-skill-step-parity.py`.
- `lint-language.py` was run on the new SKILL.md before the first commit (no em-dashes, no British `-ise`).
- The full audit programme passes standalone after the SKILL.md is committed (gates 32, 41, 44, 3, and 2 in particular).

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The existing pack covers this already." | Then drop the skill; do not write it just to have written a skill. Skill count is not a virtue. |
| "I'll trim the template; this skill doesn't need all sections." | The template is the pack's structural commitment. Trim the template and the next skill author will trim more. |
| "The trigger description is fine; the user will figure out when to call it." | Skill discovery in Claude Code reads the description. If the description is vague, the skill never triggers when it should. |
| "Cross-references are tedious; I'll add them later." | Later does not come. Add them now. |
| "Common Rationalizations table is filler." | The table is the author's commitment to think one move ahead of the next maintainer. If the table is empty, the skill's discipline is not yet fully understood. |
| "I added the SKILL and the README tree; the slash-command wiring can come later." | A paired skill not registered in the `PAIRS` list (and missing its `.claude/commands/` sibling) inherits no step-parity check, the exact silent drift gate 44 exists to catch. Wire all of step 7's surfaces in the same change, not "later". |

## See Also

- Canonical rule [`governance/evidence-grounded-completion.md`](../../governance/evidence-grounded-completion.md): the verification discipline that this skill applies to skill authoring itself (trigger-accuracy validation is verification before the new skill is claimed complete).
- Related skill [`evidence-grounded-completion`](../evidence-grounded-completion/SKILL.md): the protocol this skill defers to for the verification step.
- Related skill [`change-tracking-write-entry`](../change-tracking-write-entry/SKILL.md): adding a new skill is a tracked change; the CHANGELOG entry follows the change-tracking discipline.
- Related skill [`artefact-discipline-check`](../artefact-discipline-check/SKILL.md): the new skill creates new artefacts in the pack; the artefact-discipline-check confirms generated-vs-source separation is respected.
- Related skill [`guardrail-review`](../guardrail-review/SKILL.md) (`/guardrails`): the system-level counterpart to this per-skill template; it reviews the whole machinery (rules, skills, gates) for overlap, gap, and drift, where this skill governs the addition of one skill.
- The pack README's `## Version history` section (in `dev-security/claude-rules/README.md`) records each skill addition with the pack-minor-bump convention; this skill's addition is itself an instance of that pattern.
