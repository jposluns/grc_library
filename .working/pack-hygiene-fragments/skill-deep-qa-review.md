# Removed from skills/deep-qa-review/SKILL.md (pack-hygiene scrub)

Each entry preserves the original project-specific wording verbatim; the concrete values now live in the skill's `## Project wiring` section, and the body refers to them generically.

## Process step 0, opening paragraph (gate numbers)

```
**Binding methodology rule.** This pass reasons over git history (subagents diff PR windows, run `git log --follow`, and run the audit suite whose gates 31 and 40 are git-history-aware). On a shallow clone, `git log --follow` mis-attributes a file's last-commit date to the shallow boundary commit, which makes the document-date-staleness gate (31) and version-bump-recency gate (40) emit false positives for every file whose real history predates the boundary.
```

Replaced by: "the audit suite, whose history-aware gates are named in the project wiring" and "the history-aware gates"; the gate numbers 31 and 40 with their functional names moved to the project wiring section.

## Process step 0, closing paragraph (audit runner, iteration-1 incident detail)

```
Then confirm the mechanical baseline (`tools/run_all_audits.sh` exit 0) on the full clone. A subagent that reports a mass git-history-gate failure (e.g. "gate 31 fails on N documents") on a shallow clone is reporting an environment artifact, not a corpus defect; the orchestrator MUST validate clone depth before routing any such finding. This rule exists because iteration 1 (2026-06-22) caught exactly this: a subagent reported gate 31 failing on 153 documents; the container was a depth-50 shallow clone; after `git fetch --unshallow` the audit exited 0 and the failure did not reproduce. A less strict pass would have shipped a 153-document false emergency.
```

Replaced by: "the audit runner named in the project wiring", "a history-aware gate fails on N documents", and a genericized incident narrative ("the pass's first run in the parent library ... a history-aware gate failing on well over one hundred documents ... a shallow clone ... a mass false emergency"); the date 2026-06-22, gate 31, the depth-50 figure, and the 153-document count are archived here.

## Process step 1, Baseline bullet (audit runner)

```
- **Baseline**: `tools/run_all_audits.sh` exit 0 on the full clone (step 0). If a gate fails for a real reason, fix it first; if it fails as a shallow-clone artifact, unshallow and re-run.
```

Replaced by: "the audit runner exits 0 on the full clone (step 0)"; the runner path moved to the project wiring section.

## Process step 3 (canonical false-positive example)

```
Worker false positives (the shallow-clone gate-31 artifact is the canonical example) and over-classifications are caught here, not shipped.
```

Replaced by: "the shallow-clone history-gate artifact is the canonical example".

## Process step 5 (per-run record path)

```
Write a per-run record (project-specific location; in this project `.working/full-qa/YYYY-MM-DD-iterN.md`) with one section per subagent (A-F), an orchestrator-synthesis-and-verification section, a findings-routed section, and a trust-recovery-framing section naming the prior run's discipline failures and the elevated rules applied. Append a history row. The record directory carries a README codifying the step-0 full-clone rule.
```

Replaced by: "(the per-run record location named in the project wiring)"; the concrete path moved to the project wiring section.

## Common Rationalizations table, second row (gate-31 / 153-failure figure)

```
| "This subagent's finding is obviously real; route it." | The shallow-clone gate-31 artifact looked like 153 real failures. Re-read the source before routing every finding, especially the alarming ones. |
```

Replaced by: "The parent library's shallow-clone history-gate artifact looked like well over one hundred real failures."; gate 31 and the 153 count are archived here.

## Why this skill exists (153-document figure)

```
Its first run immediately justified the step-0 rule by catching a shallow-clone false positive that would otherwise have shipped as a 153-document emergency.
```

Replaced by: "a mass false emergency spanning well over one hundred documents"; the 153 count is archived here.
