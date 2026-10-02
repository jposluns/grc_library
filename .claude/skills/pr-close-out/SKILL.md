---
name: pr-close-out
description: Run the full PR close-out and session-migration procedure for grc_library. Use at every PR close-out boundary (before push and before merge), at session wind-down, and whenever a change touches a gate, pack rule, skill, count, or generated artefact and the paired-surface sweep is due.
---

# PR close-out

This skill is a trigger wrapper. The procedure of record is
`.claude/playbooks/pr-lifecycle.md` (gate 80 manifest-enforced). Execute it in order:

1. `## PR workflow`: steps 1-10, each with its enforcing gate/hook.
2. `## Session migration and PR close-out checklist`: the gated bookkeeping items AND
   the un-gated grep-discipline reminders (the live control; none may be skipped).
3. `## Change-impact surface map`: run the row for every change type in the PR
   (gate/rule/skill/count/repo-root), free-prose and website columns included.
4. `## Version-bump discipline (enforcement detail)`: confirm all four version surfaces.

Do not substitute an abbreviated or memory-only pass for reading the playbook.
