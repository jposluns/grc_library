---
name: validation-sweep-pr-scoped
description: Change-scoped validation sweep. Runs as a change set's finalizing step, before merge, to catch issues the change introduced before it lands. Performs a deep review scoped to the change's diff plus a lightweight cross-reference check for files cited by other documents. Complements the corpus-wide validation-sweep procedure, which is comprehensive and runs on a periodic cadence the project sets; the change-scoped form is fast and runs on every change set. The two together cover both per-change drift (caught fast) and corpus-wide drift (caught broadly).
---

# Validation Sweep, Change-Scoped

## Corpus wiring (this repository's instantiation; adopters substitute their own)

Portable procedure, concrete names. In this repository the procedure runs with:

- Mechanical baseline: the full audit-gate runner [`run_all_audits.sh`](../tools/run_all_audits.sh).
- Deterministic pre-flight scanner: [`sweep-preflight-scanner.py`](../tools/sweep-preflight-scanner.py) with its exemption file [`sweep-preflight-exemptions.json`](../tools/sweep-preflight-exemptions.json).
- Sibling corpus-wide procedure: [`validation-sweep.md`](validation-sweep.md).
- Run records: the adopting project's own working records; this repository ships no record store.

An adopting project maps each bullet to its own runner, scanner, and records; the procedure below refers to them generically.

## Overview

Change-scoped validation runs as each change set's finalizing step, before merge, to catch issues the change introduced before they compound across subsequent changes. Two sibling procedures together cover the validation surface:

- **`validation-sweep`** (corpus-wide, periodic on the project's cadence or maintainer-triggered): the full three-pass sweep across the whole project scope. Catches corpus-wide drift and audit-programme integrity issues. Expensive relative to the change-scoped form; runs periodically.
- **`validation-sweep-pr-scoped`** (change-scoped, every change set): a single focused review of the change's diff plus a targeted cross-reference check. Cheap relative to the corpus-wide sweep; runs before merge so issues are caught within the same change, not many merges later.

The two are complementary, not redundant. The corpus-wide form catches drift the per-change scope misses (a citation in file Y becomes stale because a change touched file Z); the per-change form catches issues that would otherwise compound between periodic sweeps.

## When to Use

- As every change set's finalizing step, before merge, on the committed branch state. Run it on every change set, however small; where the project's maintainer grants a documented exception, record the exception and its rationale with the run record. CI remains the mechanical pre-merge gate; this sweep is the semantic pre-merge gate, catching stale-prose and cross-document defects the mechanical gates do not.
- Optionally, after a manual investigation needs to confirm a specific change's impact.

Do not substitute an abbreviated check, a spot-check, or a memory-only review for the formal review this procedure encodes. Throughput pressure (a long batch of changes, a tight window) does not authorize abbreviation; the per-change validation IS the pace, and "the next change will catch it" is the failure mode this rule prevents. A run that returns zero findings is itself worth recording: the record is the proof the check ran.

## Process

The change-scoped sweep runs in five steps. Steps 1-2 establish scope; step 3 is the focused review; step 4 is the lightweight cross-reference check; step 5 triages and records.

### 1. Identify the change set being finalized

Capture the change state:

- The base revision the change branches from (`git merge-base <base-branch> HEAD`, where `<base-branch>` is the project's protected base branch).
- The diff against its base (`git diff <base>...HEAD`, branch synced to the base branch).
- The list of touched files (`git diff --name-only <base>...HEAD`).

### 2. Establish mechanical baseline (pre-merge, branch synced to the base branch)

Run the project's full audit-gate runner standalone against the branch state, synced to the current base branch. This confirms the gates are clean before the change is finalized. A stale branch can differ from the current base branch due to merge-base drift, which is why the branch is synced first. If any gate fails, fix the underlying defect first (in this change, or a separate fix if it is pre-existing and out of scope), then return to step 1 against the corrected state.

### 3. Review the change's diff in depth

The reviewer (a second person, an AI assistant given a self-contained brief, or the author on a separate documented pass) receives:

- The diff (full text).
- The list of touched files.
- The full state of each touched file on the branch being finalized.
- The pre-flight scanner's output filtered to the touched files (run the scanner named in the corpus wiring and filter its output; when no scanner output is relevant to the touched files, proceed unhinted).

The review looks for the same eight failure-mode classes catalogued in the corpus-wide [`validation-sweep.md`](validation-sweep.md), scoped to the touched files:

1. Stale prose references introduced by the change.
2. Mis-attributed citations introduced by the change.
3. Multi-surface incompleteness introduced by the change.
4. Inferred-as-verified state assertions in the change's prose.
5. Per-document version-bump omission (mechanically gated, but worth verifying).
6. Generated-artefact lag (mechanically gated, but worth verifying).
7. Stale docstrings in any Python file the change touched.
8. Cross-document term drift introduced by the change.

Findings use the same SARIF-lite block format as `validation-sweep`: ruleId, level, location, fingerprint, evidence. Every finding must quote a specific `path:line`; a finding without quoted evidence is a hypothesis, not a finding.

**Per-call verification discipline (AI-assisted review).** Where the review is run by an AI assistant, its brief carries the rule the corpus-wide sweep's step 4 states: before each tool call, state in one line (a) the hypothesis the call tests, (b) the observation that would falsify it, and (c) one prior result that does not already answer the question, and verify the previous call's actual result before relying on it; an undefined falsifier means the call is corroboration-seeking, so skip it or reframe it. A review transcript that chains calls without these per-call statements is rejected, and the review is redone.

One shared-tree safety rule binds any review run in the same working tree as live work: inspect version history READ-ONLY (`git show <sha>:<path>`, `git diff`, `git log`) and never run `git checkout`, `git switch`, `git reset`, or anything that moves the working tree's branch or HEAD.

### 4. Targeted cross-reference check

For each touched file, identify which OTHER files in the project cite it:

```bash
for f in <touched-files>; do
  filename=$(basename "$f")
  grep -rln "$filename" --include="*.md" . 2>/dev/null | grep -v "$f"
done
```

For each citing file, do a shallow check:

- Does the citation still resolve (the cited section, version, or line is still valid on the branch being finalized)?
- Has the touched file's header text changed in a way that breaks the citer's quoted text?
- Has any cross-reference become stale (a cited version that is now wrong)?

This is a subset of the corpus-wide sweep's Pass B scope, restricted to citers of the touched files only. Cheap; high-signal. It catches the "this change touched file A, and file C citing A is now stale" failure mode that the per-change scope would otherwise miss.

### 5. Triage and record

Triage findings:

- **In-window** (the change introduced the issue): fix it in THIS change before finalizing. A separate follow-up change only when the fix genuinely cannot land here, and that follow-up runs its own change-scoped sweep before it merges.
- **Out-of-window** (the change exposed a pre-existing issue): surface to the maintainer with named options (act now, defer tracked, dismiss).

Record the run in the project's own working records: the change identifier or branch, the date, the findings (or the zero-finding result) with dispositions, and the cross-reference check result. Before recording a fixed-in-window claim, verify it against the actual diff (search for the claim's target text); a claim whose edit is absent is recorded as routed, never as fixed.

When findings exist, present them prominently to the maintainer: per finding, the ruleId, severity, `path:line` location, a one-line evidence quote, impact, recommendation, and the in-window / out-of-window classification. A zero-finding run gets a one-line acknowledgement.

## Termination

The change-scoped sweep is a single-iteration cycle: review, check, triage, record. There is no fixed-point loop (unlike the corpus-wide sweep's iterative cycle). Per-change sweeps are short-lived; the corpus-wide sweep handles deeper iteration.

## Red Flags

- The sweep skipped because "no findings expected": every change produces new state worth checking, and the record is the proof-of-check.
- Findings surfaced but not triaged.
- A follow-up fix change merged without its own change-scoped sweep.
- The cross-reference check skipped because "the diff review already covered it": the diff review covers the touched files; the cross-reference check covers the FILES THAT CITE the touched files. Different scope; both required.

## Verification

The change-scoped sweep is complete when:

- The mechanical baseline was confirmed clean on the synced branch state.
- The diff review ran over the change's diff and returned findings or an explicit zero-finding result.
- The cross-reference check ran on the touched files' citers.
- Findings (if any) are triaged with in-window / out-of-window classification.
- The run is recorded in the project's own working records.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The change was small; skip the sweep." | Small changes still break cross-references no one thought to check. Run it on every change. |
| "The next change will catch any issues." | Maybe; but compounding is faster. Catch at the merge, not five merges later. |
| "This is redundant with the corpus-wide sweep." | They are complementary. The corpus-wide sweep runs periodically; this one catches issues in the changes between sweeps. |
| "The cross-reference check is too expensive." | It is bounded to the citers of the touched files, typically a handful per check. Cheap. |
| "If CI passed, the change is clean." | CI catches mechanical defects; this sweep catches semantic defects (stale prose, cross-document drift) that mechanical gates do not. |

## See Also

- Sibling procedure [`validation-sweep.md`](validation-sweep.md): the corpus-wide periodic sweep, including the failure-mode catalogue and the synthesis rubric this procedure reuses.
- Canonical gate inventory: [`specification-audit-programme.md`](../specs/specification-audit-programme.md).

## Why this procedure exists

The corpus-wide sweep runs on a cadence the project sets. Between sweeps, issues introduced by individual changes compound silently: a change touches file A; later changes cite the changed file; the citation may have been stale from the start, but nobody checks until the next corpus-wide sweep. By then the issue has been re-cited in several places.

The change-scoped sweep closes this gap. Run on every change set before it merges, it catches introduced issues before they land and compound. The cost is modest; the benefit is keeping the corpus-wide sweep's iteration count low and the per-change feedback loop tight.
