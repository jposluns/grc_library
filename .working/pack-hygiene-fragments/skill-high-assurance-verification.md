# Removed from skills/high-assurance-verification/SKILL.md (pack-hygiene scrub)

## When to Use, first bullet (motivating-case clause)

```markdown
- **Before applying a sensitive change**, one that meets all three trigger conditions (gate-blind correctness, delicate scale, high escaped-error cost). The motivating case: adding a control-framework column to the compliance matrix, where each cell carries a control code whose fit no existence gate can check.
```

Replaced by a generic "canonical shape" clause pointing at the project wiring, where the motivating case now lives.

## When to Use, third bullet (register path and resume command)

```markdown
- **When resuming a sensitive item left open** in the persistent register ([`.working/high-assurance/register.md`](../../../../.working/high-assurance/register.md)) with status `pending` or `in-progress`, surfaced at `/resume`.
```

Replaced by "the persistent register named in the project wiring, ... surfaced at session resume"; the concrete path and the `/resume` convention moved to the project-wiring section.

## Process step 1 (register path)

```markdown
Open a row in the persistent register ([`.working/high-assurance/register.md`](../../../../.working/high-assurance/register.md)) recording the item, which of the three conditions make it sensitive, and status `in-progress`, so the item survives a session boundary.
```

Replaced by "the persistent register named in the project wiring"; the concrete path moved to the project-wiring section.

## Process step 7 (resume command)

```markdown
leave the row `pending` / `in-progress` (or `deferred` with the blocker named) so the next `/resume` re-surfaces it.
```

Replaced by "so the next session resume re-surfaces it"; the `/resume` convention moved to the project-wiring section.

## See Also, final bullet (register path and resume command)

```markdown
- The persistent register: [`.working/high-assurance/register.md`](../../../../.working/high-assurance/register.md), surfaced at `/resume`.
```

Replaced by "The persistent register named in the project wiring above, surfaced at session resume."
