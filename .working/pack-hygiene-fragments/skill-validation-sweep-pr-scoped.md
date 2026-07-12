# Removed from skills/validation-sweep-pr-scoped/SKILL.md (pack-hygiene scrub)

Each entry preserves the verbatim original text that the pack-hygiene generalization
removed or reworded, with the location and the replacement that now stands in the SKILL.

## Process step 2, mechanical-baseline sentence (audit-runner path)

```
Run `tools/run_all_audits.sh` standalone against the post-merge state.
```

Replacement: "Run the project's full audit-gate runner (named in the project wiring above) standalone against the post-merge state." The concrete runner path moved to the project-wiring section.

## Process step 3, Subagent A input bullet (pre-flight scanner command)

```
- A pre-flight scanner output filtered to the touched files (run `python3 tools/sweep-preflight-scanner.py` and filter the output to the touched file set; if no scanner output relevant to touched files, proceed unhinted).
```

Replacement: "run the project's deterministic pre-flight scanner and filter the output to the touched file set"; the concrete scanner path moved to the project-wiring section.

## Process step 5, record bullets (per-PR record path and history-register paths)

```
- A per-PR validation record at `.working/validate-pr/<YYYY-MM-DD>-PR-<N>.md` with the findings and triage. Six top-level H2 sections: Trigger and state snapshot, Subagent A return, Cross-reference check, Orchestrator triage, Resulting hot-fix PR (if any), Notes.
- An entry in `.working/validate-pr/history.md` (similar to validate-sweeps/history.md but PR-scoped, one row per merged PR).
```

Replacement: the record path became "the project's dated per-PR record path" and the register became "the PR-scoped history register (the PR-scoped mirror of the corpus-wide sweep's register)"; the concrete `.working/validate-pr/` and `.working/validate-sweeps/history.md` paths moved to the project-wiring section. The six-section record shape is retained verbatim.

## Pre-flight scanner section (scanner command and exemption-file path)

```
Run `python3 tools/sweep-preflight-scanner.py` and filter the output to the touched-files set. Hand the filtered output to Subagent A as a known-candidate list. The scanner applies in-scanner heuristics and an exemption file at `tools/sweep-preflight-exemptions.json`.
```

Replacement: "Run the project's deterministic pre-flight scanner (named in the project wiring above) ... The scanner applies in-scanner heuristics and a project-maintained exemption file." Both concrete paths moved to the project-wiring section.

## Surfacing-findings section, record-file sentence (record path and CHANGELOG mirror name)

```
A maintainer should not need to open `.working/validate-pr/<date>-PR-<N>.md` or scroll through `CHANGELOG-detailed.md` to see what the sweep found.
```

Replacement: "open the dated per-PR record file or scroll through the detailed change-log mirror"; the mirror's concrete path is in the project-wiring section.

## Surfacing-findings section, closing sentence (`.working/` naming)

```
The chat surface is non-negotiable when the sweep produces findings: a finding that lives only in `.working/` files is not surfaced to the maintainer's attention.
```

Replacement: "a finding that lives only in working-state record files is not surfaced to the maintainer's attention."

## Batching sub-case 1 (history-register path)

```
1. **Zero-finding invocations**: the history row alone is deferred. Append it to `.working/validate-pr/history.md` as part of the next PR's diff, alongside the next PR's other changes. The /validate-pr invocation itself still runs immediately after the merge it follows; only the row commit waits.
```

Replacement: "Append it to the PR-scoped history register as part of the next PR's diff"; the rest of the sub-case is retained verbatim.

## See Also, pre-flight scanner bullet (scanner path and repository-relative link)

```
- Pre-flight scanner [`tools/sweep-preflight-scanner.py`](../../../../tools/sweep-preflight-scanner.py): the deterministic pre-flight check shared with the corpus-wide skill.
```

Replacement: "- Pre-flight scanner: the deterministic pre-flight check shared with the corpus-wide skill (the parent library's concrete scanner is named in the project wiring above)." The repository-relative link is dropped; the concrete scanner is in the project-wiring section.
