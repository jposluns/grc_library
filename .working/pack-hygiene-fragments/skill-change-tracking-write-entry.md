# Removed from skills/change-tracking-write-entry/SKILL.md (pack-hygiene scrub)

Each entry preserves the verbatim original text that the pack-hygiene generalization
removed or reworded, with the location and the replacement that now stands in the SKILL.
This was a very light pass: two body lines and one frontmatter phrase carried
project-specific naming; everything else in the file was already generic.

## Frontmatter, description (D1 gate naming)

```
so an entry that would fail the link-coverage gate, the version-monotonicity audit, or the D1 delta gate is caught at the draft stage rather than at CI.
```

Replacement: "or the PR-time delta gate"; the parent library's concrete check id (D1) moved to the new project-wiring section.

## When to Use, third bullet (terse-entry scope directories)

```
- Before pushing a PR that touches only internal tooling, AI-assistant guidance (`.claude/`), working-state ledgers (`.working/`), or other ancillary surfaces (terse entry).
```

Replacement: "internal tooling, assistant-guidance trees, working-state ledgers, or other ancillary surfaces (terse entry; the parent library's concrete directories are named in the project wiring above)"; the concrete `.claude/` and `.working/` directories moved to the project-wiring section.

## Process step 1, terse-entry classification bullet (terse-entry scope directories)

```
   - **Terse entry** when the change is internal tooling invisible to adopters (changes under `.claude/`, working-state-only edits under `.working/`), a pure refactor with no behavioural change, or a typo fix in a non-citable string.
```

Replacement: "(changes under the assistant-guidance tree, working-state-only edits under the working-state ledgers; the project wiring above names the parent library's directories)"; the concrete `.claude/` and `.working/` directories moved to the project-wiring section.

## Not removed (deliberate)

The Terse Entry Discipline section's worked example (the `` `.claude/ changes for local project: ...` `` terse-entry line) mirrors the canonical change-tracking rule's own example verbatim; the rule stays as-is until the rules tranche lands, so the skill's mirrored example is retained to preserve rule/skill parity, and the wiring section already names `.claude/` as the parent library's terse-scope directory.
