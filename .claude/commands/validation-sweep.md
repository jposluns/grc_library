Invoke the `validation-sweep` skill defined in this project's pack at [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](../../dev-security/claude-rules/skills/validation-sweep/SKILL.md). Execute the corpus-wide regression sweep per the seven-step process the skill encodes:

1. **Establish mechanical baseline**: run `tools/run_all_audits.sh` standalone and capture the result. If any gate fails, fix the underlying defect first, then return to this step.
2. **Enumerate recent changes**: identify the focus window of the past two calendar days via `git log --since="2 days ago" --name-only --pretty=format:""`, plus the current working tree via `git status --short`.
3. **Identify failure-mode classes in scope**: review the catalogued classes the mechanical gates do not cover (stale prose references, mis-attributed citations, multi-surface incompleteness, inferred-as-verified state assertions, per-document version-bump omission, generated-artefact lag, stale docstrings, cross-document term drift).
4. **Fan out parallel subagent reviews**: launch three sub-investigations concurrently (recent-PR deep review, corpus-wide stale-reference sweep, audit-programme integrity check). Each subagent reads target files in full and reports findings grouped by severity.
5. **Synthesise findings**: deduplicate across subagents; for each, record file path, line range, description, and whether the subagent verified by reading or inferred.
6. **Triage**: for findings within the focus window, propose a concrete fix per the in-window protocol. For findings outside the focus window (pre-existing issues surfaced incidentally), surface as questions to the operator with named action options — do NOT auto-defer to "Low / FYI".
7. **Apply fixes, re-baseline, repeat**: apply the fixes, **commit them**, then re-run `tools/run_all_audits.sh` on the committed state (git-history-aware gates only see committed history). Repeat from step 4 if new findings surface. The sweep is complete when one full cycle returns no High or Medium findings.

Cap: stop after three iterations if the cycle does not converge, and surface the pattern to the operator.

Report back: the audit baseline result, the subagent findings (grouped by severity), the fixes applied, and the final clean-bill status.
