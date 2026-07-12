# Removed from skills/matrix-fit/SKILL.md (pack-hygiene scrub)

Each entry below preserves, verbatim, a passage removed from the skill during the
generalize-in-place scrub, with the generic replacement that took its place. Concrete
project values now live only in the skill's "Project wiring" section.

## Frontmatter `description` line

```
description: Cadenced semantic-fit audit of the compliance matrix and per-document framework-alignment tables. Catches the gate-blind "valid code, wrong control" class: a control identifier that EXISTS in its catalogue (so the existence gates 48/49/54/58/61 pass it) but is the WRONG control for the row's document. Run after each FR-167 matrix-expansion batch, once at matrix completion, and ad-hoc when a control-code citation is in doubt. It dispatches a semantic judge over the recall-oriented worklist that `tools/audit-matrix-semantic-fit.py` produces, adjudicating each cited code against the source control TITLE in the reference base, then routes confirmed mismatches. It catches what the existence-and-membership gates structurally cannot: semantic fit needs a read of the source title, not a catalogue-membership check.
```

Generic replacement: "the existence gates pass it", "each matrix-expansion batch", and "the worklist the project's recall-oriented pre-filter produces"; the concrete gate list and tool name moved to the project-wiring section.

## Overview, paragraph 1 (per-gate enumeration)

```
The audit gates that guard control-code citations check existence and catalogue membership, not semantic fit. Gate 48 confirms a CSA CCM / AICM code is cited from the right catalogue; gate 49 confirms a matrix row's codes are well-formed and in-catalogue; gate 54 confirms NIST CSF 2.0 codes in any per-document framework table are valid Category codes; gate 58 does the same for ISO/IEC 27001:2022 Annex A codes, and gate 61 for COBIT 2019 objective/practice codes and ISO 31000:2018 clause numbers.
```

Generic replacement: "one gate family confirms each cited code is drawn from the right catalogue and well-formed, per framework (the parent library's concrete gate list is in the project wiring above)".

## Overview, paragraph 2 (incident lineage)

```
The class is not hypothetical. The 2026-06-27 trust-recovery `/full-qa` found eight matrix rows and seven source-doc framework-table rows carrying valid-but-wrong codes, all remediated in PR #392; the same class had recurred across PRs #390/#391/#392 (improvement-log #392).
```

Generic replacement: "A trust-recovery forensic pass in the parent library found fifteen valid-but-wrong codes across matrix and source-document rows, and the class had recurred across consecutive changes before this cadence existed."

## Overview, paragraph 3 (tool provenance and the PR-A design lesson)

```
It is the semantic-judge half of a two-part instrument whose recall-oriented triage half is the advisory tool `tools/audit-matrix-semantic-fit.py` (shipped in PR #394, explicitly NOT a gate).
```

```
The design lesson from PR A is binding: judge against the source control TITLE, not a lexical proxy, because a correct GRC mapping routinely shares no vocabulary with the document title (the tool's own worklist is recall-oriented precisely because the lexical signal is too weak to certify correctness).
```

Generic replacement: "the advisory pre-filter named in the project wiring (explicitly NOT a gate)" and "The design lesson from the pre-filter's construction is binding: ...".

## Overview, paragraph 4 (cadence naming)

```
It runs on a cadence (after each FR-167 matrix-expansion batch, once at matrix completion, and ad-hoc), surfaces confirmed mismatches, and routes or fixes them under the normal in-window / out-of-window triage.
```

Generic replacement: "after each matrix-expansion batch" (the backlog id is project history).

## When to Use, bullet 1

```
- **After each FR-167 matrix-expansion batch.** A batch authors many new mapping rows; a fit pass over the batch's worklist catches the valid-but-wrong codes before they compound across later batches. This is the primary cadence.
```

Generic replacement: "**After each matrix-expansion batch.**" (rest of the bullet unchanged).

## When to Use, bullet 4 (gate enumeration)

```
- **NOT as a replacement for the existence gates.** Gates 48/49/54/58/61 still run on every PR; `matrix-fit` is the semantic layer on top of them, not a substitute. A row must pass the gates first; this skill judges fit among rows that already pass.
```

Generic replacement: "The existence gates still run on every change" (rest of the bullet unchanged).

## Process step 1 (runner, validator-module paths, reference-base paths)

```
Name the scope for this run: a single domain section (the FR-167-batch cadence), the whole matrix (the completion cadence), or a maintainer-flagged set of rows (the ad-hoc cadence). Confirm `tools/run_all_audits.sh` exits 0 first; a fit pass judges among rows that already pass the existence gates, so a red gate is a defect to fix mechanically before the semantic read. Confirm the reference base is available: the in-repo validator modules [`tools/ccm_aicm_reference.py`](../../../../tools/ccm_aicm_reference.py), [`tools/nist_csf_reference.py`](../../../../tools/nist_csf_reference.py), and [`tools/cobit_iso31000_reference.py`](../../../../tools/cobit_iso31000_reference.py) carry the gate-validated control codes and titles, and the `grc_library_ref` reference base carries the full source-text extracts (the CSA CCM v4.1 catalogue CSV under `grc_library_ref/frameworks/CSA/`, the NIST CSF 2.0 text under `grc_library_ref/standards/NIST/`, and the other source families per the `grc_library_ref` index). The judge reads control TITLES from these, never from memory.
```

Generic replacement: "(the matrix-expansion-batch cadence)", "the project's full audit-gate suite exits 0", and "the reference base named in the project wiring is available: the gate-validated control codes and titles, and the full source-text extracts for each cited framework family".

## Process step 2 (tool invocation and the Sweep-61 known-residual example)

```
Run `python3 tools/audit-matrix-semantic-fit.py` (add `--matrix-only` or `--source-docs-only` to match the scope from step 1). The tool always exits 0; its output is a recall-oriented worklist of rows that lack any lexical anchor between the document subject and the cited control titles. Treat the worklist as the judge's input-narrowing step, NOT a defect list: a listed row is a candidate to read, a non-listed row is deprioritized (not certified correct). Add to the worklist any row the maintainer or a prior `/validate` / `/full-qa` note flagged (the known residual case is the loose-supporting-code-on-an-anchored-row, which the tool intentionally does not list, e.g. the Sweep-61 `TVM-06` note on a pen-testing standard).
```

Generic replacement: "Run the pre-filter named in the project wiring, scoped to match the scope from step 1 where the pre-filter supports scoping" and "(the known residual case is a loose supporting code on an already-anchored row, which the pre-filter intentionally does not list)".

## Process step 4 (project checklist pointer)

```
When a mismatch is fixed, re-read the paired description cell in the same row for echoes of the old code's meaning (the migration-leaves-stale-prose class, CLAUDE.md close-out checklist).
```

Generic replacement: "(the migration-leaves-stale-prose class, the project's close-out checklist)".

## Red Flags, bullet 1 (PR-A lesson)

```
- Judging fit from the code's familiarity or a remembered meaning instead of reading the source control TITLE. The PR-A design lesson is that the title is the only evidence; a remembered meaning is the failure mode that produced the valid-but-wrong codes in the first place.
```

Generic replacement: "The pre-filter's founding design lesson is that the title is the only evidence" (rest of the bullet unchanged).

## Verification, bullet 1 (runner path)

```
- The scope was named and the mechanical baseline was clean (`tools/run_all_audits.sh` exit 0) before the semantic read.
```

Generic replacement: "(the project's full audit-gate suite exit 0)".

## Common Rationalizations, row 1 (gate enumeration)

```
| "Gates 48/49/54/58/61 pass, so the codes are fine." | Those gates check existence and catalogue membership, not fit. A valid code can be the wrong control; only a title read decides. |
```

Generic replacement: `"The existence gates pass, so the codes are fine."` (Reality cell unchanged).

## See Also, tool and reference-base bullets

```
- The advisory tool [`tools/audit-matrix-semantic-fit.py`](../../../../tools/audit-matrix-semantic-fit.py): the recall-oriented triage step that feeds this skill's worklist (not a gate; always exits 0).
- The reference base: the in-repo validator modules [`tools/ccm_aicm_reference.py`](../../../../tools/ccm_aicm_reference.py), [`tools/nist_csf_reference.py`](../../../../tools/nist_csf_reference.py), and [`tools/cobit_iso31000_reference.py`](../../../../tools/cobit_iso31000_reference.py) (gate-validated codes and titles) and the `grc_library_ref` full-text extracts (source control titles; the CSA catalogues under `grc_library_ref/frameworks/CSA/`, the NIST CSF text under `grc_library_ref/standards/NIST/`).
```

Generic replacement: "The advisory pre-filter named in the project wiring: ..." and "The reference base named in the project wiring: the gate-validated control codes and titles plus the full source-text extracts from which the judge reads control TITLES."
