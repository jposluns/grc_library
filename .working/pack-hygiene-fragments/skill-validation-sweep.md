# Removed from skills/validation-sweep/SKILL.md (pack-hygiene scrub)

Each entry: where the passage lived, the verbatim original, and the generic replacement now in the skill. The concrete values themselves are consolidated in the skill's new "Project wiring" section.

## Overview, paragraph 3 (canonical command and inventory)

```
The skill is project-agnostic in shape but invokes project-specific commands; the GRC Library's canonical full-audit command is [`tools/run_all_audits.sh`](../../../../tools/run_all_audits.sh) and the canonical gate inventory is [`governance/specification-audit-programme.md`](../../../../governance/specification-audit-programme.md) §6.
```

Replaced by: "the consuming project's canonical full-audit command and canonical gate inventory are named in the project wiring above."

## When to Use, staleness-audit bullet

```
- Periodically, informed by the document-staleness audit (gate 31 in the canonical inventory).
```

Replaced by: the same bullet with "(the project wiring names the concrete gate)" in place of the gate number.

## Step 1, opening sentence

```
Run the canonical full-audit command standalone. For the GRC Library: `tools/run_all_audits.sh`. Capture exit code and any failure output.
```

Replaced by: "Run the canonical full-audit command standalone (named in the project wiring). Capture exit code and any failure output."

## Step 3a, opening sentence (scanner invocation)

```
Before subagent fan-out, run the pre-flight scanner: `python3 tools/sweep-preflight-scanner.py`. This is a deterministic regex-based pass
```

Replaced by: "run the project's deterministic pre-flight scanner (named in the project wiring)".

## Step 3a, project-specific-scanner paragraph

```
The scanner is project-specific (its `CANONICAL_COLLECTIONS` and seed patterns target this corpus); other projects adopting the validation-sweep pattern should swap in their own scanner with project-specific patterns.
```

Replaced by: the same sentence with "its canonical-collection constants and seed patterns target the consuming corpus" (the constant name moved to the wiring section).

## Step 3a, pattern-set paragraph (PF ids and the Sweep 4 lineage)

```
The scanner's pattern set is extensible. Currently shipped patterns: **PF-01 / PF-02 / PF-03** for stale collection counts (skills, governance rules, generic `N <collection>`), and **PF-04** for stale version literals (`currently 1.22.0` and similar phrases where the captured version does not match any of the canonical library, README, pack, or spec versions). PF-04 was added after the Sweep 4 finding in `docs/adopter-guide.md:57` ("ships with its own version sequence (currently `1.22.0`)") to catch the same shape mechanically on future sweeps.
```

Replaced by: a generic description of the two pattern classes plus "the parent library's concrete pattern ids are listed in the project wiring" and "The stale-version-literal pattern was added after a sweep finding of exactly that shape, so future sweeps catch it mechanically."

## Step 3a, Layer-2 exemption-file clause

```
**Layer 2, exemption file** at [`tools/sweep-preflight-exemptions.json`](../../../../tools/sweep-preflight-exemptions.json): per-entry
```

Replaced by: "**Layer 2, exemption file** (the scanner exemption file named in the project wiring): per-entry".

## Step 4, Subagent B brief (canonical sources and the listing-surface gate)

```
cross-check against the canonical sources (README, spec §6 inventory). Also check
```

```
(The MECHANICAL listing surfaces, the document-index register and the domain READMEs, are enforced by gate 47, so a recently-added document missing from those is a gate failure, not a sweep finding; the sweep's value is the relevance-based surfaces where a new document plausibly belongs but inclusion is a judgment call. `tools/suggest-listing-surfaces.py <doc>` produces the candidate set.)
```

Replaced by: "(the README, the canonical gate inventory)" and "the project's listing-surface coverage gate ... The project wiring names the gate and the candidate-set helper that produces the candidate set."

## Rule 5.6, history-register parenthetical

```
Every iteration row in the project's validation-sweep history (in this project: [`.working/validate-sweeps/history.md`](../../../../.working/validate-sweeps/history.md); adopters relocate to a project-appropriate path) names which subagents were dispatched
```

Replaced by: "Every iteration row in the project's validation-sweep history register (named in the project wiring) names which subagents were dispatched".

## Step 5, false-positive-memory parenthetical

```
Cross-reference each synthesized finding against the **false-positive memory** entries listed in the validation-sweep history README (in this project: [`.working/validate-sweeps/README.md`](../../../../.working/validate-sweeps/README.md), § Accept-list discipline; adopters relocate to a project-appropriate path).
```

Replaced by: "listed in the validation-sweep history README (named in the project wiring)."

## Step 6, accept-list composition sentence

```
The pre-flight scanner's [`tools/sweep-preflight-exemptions.json`](../../../../tools/sweep-preflight-exemptions.json) and the register's `false-positive memory` section together form the accept-list.
```

Replaced by: "The pre-flight scanner's exemption file and the register's `false-positive memory` section together form the accept-list."

## Step 8, opening sentence

```
append a row to the project's validation-sweep history (in this project: [`.working/validate-sweeps/history.md`](../../../../.working/validate-sweeps/history.md); adopters relocate to a project-appropriate path). The history file is a reverse-chronological table
```

Replaced by: "append a row to the project's validation-sweep history register (named in the project wiring)."

## Step 9, opening sentence

```
write a per-iteration detail file to the project's working directory (in this project: `.working/validate-sweeps/`; adopters may relocate to a project-appropriate path). Filename `YYYY-MM-DD-sweepN-iterM.md`
```

Replaced by: "write a per-iteration detail file to the project's per-iteration detail directory (named in the project wiring)."

## Step 9, linter-exemption sentence

```
The per-iteration record's directory should be in `tools/lint_common.py` `DEFAULT_EXEMPT_DIRS` (or the equivalent linter-exemption mechanism in adopter projects).
```

Replaced by: "covered by the project's linter-exemption mechanism (the parent library's concrete mechanism is named in the project wiring)."

## Surfacing findings in chat, detail-file and change-log paths

```
A maintainer should not need to open `.working/validate-sweeps/<date>-sweep<N>-iter<M>.md` or scroll through `CHANGELOG-detailed.md` to see what the sweep found.
```

Replaced by: "open the per-iteration detail file or scroll through the detailed change-log mirror".

## Surfacing findings in chat, working-state clause

```
The chat surface is non-negotiable when the sweep produces findings: a finding that lives only in `.working/` files is not surfaced to the maintainer's attention.
```

Replaced by: the same sentence with "working-state files" in place of the `.working/` path.
