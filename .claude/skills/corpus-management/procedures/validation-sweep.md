---
name: validation-sweep
description: Corpus-wide regression sweep run as a follow-up after any issue is identified and corrected, to confirm no sibling issue remains anywhere in the repository. Invoke after fixes that touch multi-surface artefacts, gate inventories, prose claims about repository state, AI-inferred citations, or generated artefacts. Combines the mechanical audit suite with a structured semantic review, and loops until clean.
---

# Validation Sweep

## Corpus wiring (this repository's instantiation; adopters substitute their own)

Portable procedure, concrete names. In this repository the procedure runs with:

- Canonical full-audit command: [`run_all_audits.sh`](../tools/run_all_audits.sh); canonical gate inventory: [`specification-audit-programme.md`](../specs/specification-audit-programme.md) section 6.
- Deterministic pre-flight scanner: [`sweep-preflight-scanner.py`](../tools/sweep-preflight-scanner.py), with shipped pattern ids PF-01 / PF-02 / PF-03 for stale collection counts (skills, rules, generic `N <collection>`) and PF-04 for stale version literals; its machine-readable false-positive memory is the exemption file [`sweep-preflight-exemptions.json`](../tools/sweep-preflight-exemptions.json).
- Document-staleness audit: gate 31 in the canonical inventory.
- Listing-surface coverage gate: gate 47 (the document-index register and the domain READMEs); the candidate-set helper is [`suggest-listing-surfaces.py`](../tools/suggest-listing-surfaces.py).
- Linter-exemption mechanism for any archived sweep records an adopter keeps inside the repository: `DEFAULT_EXEMPT_DIRS` in [`lint_common.py`](../tools/lint_common.py).
- Sweep records: the adopting project's own working records (a private store, a wiki, or a tracked record of its choosing). This repository ships no record store, and the public gates degrade gracefully when none is present.

An adopting project maps each bullet to its own commands and records; the procedure below refers to them generically.

## Overview

After a single defect is found and fixed, a sibling defect may still be lurking elsewhere: same author, same working stretch, same inferred mental model, same blind spot. The mechanical audit gates catch their own classes; this procedure is the structured corpus-wide sweep that catches what the gates do not. It targets cross-file prose drift, mis-attributed citations, multi-surface incompleteness, inferred-as-verified state assertions, and the other failure-mode classes catalogued below.

The sweep is fixed-point: if it finds anything, fix it, then re-run the sweep, until the sweep returns clean. The audit gates are the ground truth for mechanical claims; the three semantic review passes are the ground truth for the semantic claims the gates cannot mechanize.

## When to Use

- Immediately after identifying and correcting any issue in the repository, as a follow-up that confirms no sibling issue remains.
- When taking over work whose results have not been verified on the current state.
- After landing a change that touched any "parallel surface" set: the gate inventory, a version-history table, a framework-alignment table, mirror-synced files, generated artefacts.
- Before declaring a multi-change programme phase complete.
- Periodically, informed by the document-staleness audit (the corpus wiring names the concrete gate).
- Whenever a reader surfaces an AI-introduced error and asks for assurance that no sibling error remains.
- When a scheduled mechanical sweep (the deterministic half of this discipline, run via CI on a cadence the project sets) reports a failure. A scheduled run catches time-dependent drift (citation freshness, document-date staleness, version-bump recency) when nobody has touched the content; pair the mechanical finding with the semantic review of step 4.

## Process

The sweep runs in eight steps. Steps 1-3 establish the baseline and scope; steps 4-5 are the semantic sweep; step 6 triages; step 7 is the fixed-point loop that runs until clean; step 8 records the sweep in the project's own records.

### 1. Establish mechanical baseline

Run the canonical full-audit command standalone. Capture exit code and any failure output. The expected state is exit 0 on the current working tree.

If the audit reports failures, the sweep cannot proceed semantically until the mechanical baseline is clean. Address the gate failures first, then return to this step.

### 2. Enumerate recent changes

Identify the scope of recently-touched files. The focus window is a bound the project sets; the default is **the past two calendar days**, wide enough to span weekend work and post-review follow-ups, narrow enough that the in-window set stays reviewable. A project on a different rhythm substitutes its own window and states the bounds it used when it records the sweep.

- `git log --since="2 days ago" --name-only --pretty=format:""` : files touched in the focus window (substitute the project's window).
- `git status --short` : files in the current working tree.
- `git log --name-only -10` : files touched in the last ten commits, as additional context (substitute the project's depth).

These files are the highest-priority targets for the semantic sweep. Findings on files outside the focus window (pre-existing issues the sweep surfaces incidentally) are still reportable and ARE handled by step 6, not silently discarded.

### 3. Identify failure-mode classes in scope

The sweep targets failure modes the mechanical gates do not cover. Each class has a known shape; new classes may surface as the project and its audit programme evolve.

| Class | Shape |
| --- | --- |
| Stale prose references | "N gates" or "gates 1-N" prose where N is no longer the canonical count; a library or document version mentioned in prose that has since bumped. |
| Mis-attributed citations | A citation of "step X" or "section Y" of another file where the cited content does not match the source; phrase-level quotes attributed to one rule but actually living in another. |
| Multi-surface incompleteness | A change that should update N surfaces but updated N-1: change-record coverage of files touched, README claims, registers, cross-references. |
| Inferred-as-verified state assertions | A claim about a file's contents written without re-reading the file. |
| Per-document version-bump omission | A non-exempt document substantively changed but its `Version:` field not bumped. |
| Generated-artefact lag | A source file edited but its generator not re-run, or vice versa; the gates catch the drift but the underlying lag is the failure. |
| Stale docstrings | A linter or script docstring describing behaviour that no longer matches the code. |
| Cross-document term drift | Different files use different terms for the same concept, with no canonical glossary entry to anchor the choice. |

### 3a. Run the deterministic pre-flight scanner (optional but recommended)

Before the semantic review, run the pre-flight scanner named in the corpus wiring. This is a deterministic regex-based pass that surfaces candidate findings for shapes the high-precision mechanical gates do not catch (stale collection counts, prose-form number drift, stale version literals). The scanner exits 0 always; its output is a list of candidates, not verified findings.

Hand the scanner's output to each review pass as a "known suspect locations to verify or dismiss" list. Many candidates will be false positives (legitimate historical references, comparative prose, references to other projects' counts); that is expected: the scanner is high-recall, the semantic triage is the precision layer.

The scanner applies two layers of noise reduction so the same false positives do not re-surface on every sweep. **Layer 1, in-scanner heuristics**: skip matches preceded by section-like words, hyphenated compounds, legal bill prefixes, version-history table rows, and lines containing historical-narrative keywords. **Layer 2, the exemption file** named in the corpus wiring: per-entry `(path, pattern_id, line_hash)` records that suppress unique edge cases the heuristics miss. The `line_hash` is the 16-character prefix of SHA-256 of the stripped line content, so the exemption is stable under line-number drift but invalidates automatically when the line text changes, which forces a re-triage. The project's own false-positive record is the human-readable source of truth; the exemption file is its machine-readable mirror.

The scanner's canonical-collection constants and seed patterns target this corpus; a project adopting the pattern swaps in its own scanner patterns.

### 4. Run the three semantic review passes

**All three passes run on every full sweep.** Do not substitute an abbreviated check, a spot-check, or a memory-only review for the three passes the procedure encodes; the only sanctioned reduction is one the project's maintainer authorizes in advance and records with the sweep's record, with the rationale. Throughput pressure does not authorize abbreviation: the corpus-wide sweep IS the cadence, and "the next sweep will catch it" is the failure mode this rule prevents.

Each pass works from a self-contained brief, reads target files in full (not excerpts), and reports findings by severity. Run each pass with fresh eyes where possible: a second reviewer, an AI assistant given the brief, or the same person on a separate documented pass. The three baseline briefs:

- **Pass A, recent-change deep review**: read every file touched in the focus window in full; verify every change-record entry, commit message, and docstring claim against the actual diff; specifically flag mis-attributed citations and claims that contradict the file's actual contents.
- **Pass B, corpus-wide stale-reference sweep**: search the repository for stale gate counts, versions, and dates; cross-check against the canonical sources (the README, the canonical gate inventory). Also check listing-surface coverage drift on the SEMANTIC surfaces no gate enforces: the project's judgment-call listing surfaces (in this corpus, the framework matrices and crosswalks, the glossary and key-terms registers, and per-document `Related Documents` fields). The MECHANICAL listing surfaces are enforced by the listing-surface coverage gate, so a recently-added document missing from those is a gate failure, not a sweep finding; the sweep's value is the relevance-based surfaces where inclusion is a judgment call. The corpus wiring names the gate and the candidate-set helper.
- **Pass C, audit-programme integrity check**: independently re-verify that the project's parity surfaces agree (in this repository: the CI workflow, the local runner, the pre-commit configuration, and the specification inventory); verify mirror-sync between each mirrored source and its copies; verify any new linter's docstring matches its code; spot-check generated-artefact regeneration.

Each pass reports under 600 words, grouped by severity: **High** (factual error, stale reference in a normative document, mis-attribution), **Medium** (style inconsistency, minor wording drift, off-by-one in a count), **Low / FYI** (cosmetic, historical context, not actionable).

**Required for every finding**: a `path:line` evidence quote. A finding without an explicit file path and line number (or range) is not a finding, it is a hypothesis. Reject any pass report whose findings lack quoted evidence and redo that pass with the evidence requirement re-emphasized.

**SARIF-lite output format.** Each pass emits findings as one fenced markdown block per finding so dedupe and synthesis are mechanical rather than narrative:

```
### Finding: <one-line title>
- tool: <pass-name>               # A, B, or C
- ruleId: <short-stable-id>       # e.g. stale-version-literal
- level: error|warning|note       # SARIF v2.1.0 result.level enum
- location: <path>:<line>
- fingerprint: <ruleId>:<path>:<line>   # deterministic dedupe key
- rubric: 5.1 | 5.2 | 5.3 | 5.4 | 5.5

<evidence quote or 1-2 sentence rationale>
```

One finding equals one block; the fingerprint is deterministic (`<ruleId>:<path>:<line>`, lowercase, no spaces); the severity enum is closed (`error` / `warning` / `note`).

**Per-call verification discipline (AI-assisted passes).** Where a pass is run by an AI assistant, its brief carries the following rule (a falsification preamble). Before each tool call (a file read, a search, a command), the assistant states in one line: (a) the hypothesis this call tests, (b) the observation that would falsify it, and (c) one prior result that does not already answer the question; and it verifies the previous call's actual result before relying on it. If the falsifying observation is undefined, the call is corroboration-seeking; skip it or reframe. If a prior result already answers the question, do not re-call; cite the prior result in the finding. This produces an auditable trace (every tool call carries its own justification) and filters corroboration-only calls at the source rather than at the report-writing stage, where they have already consumed budget. A pass transcript that chains calls without these per-call statements is rejected, and the pass is redone.

If the focus window shows no recent activity (a "cold" sweep), Pass A becomes a narrower spot-check of the most recently-merged changes (`git log -5 --merges`), so the pass always has a concrete target set.

### 5. Synthesize findings

Apply the synthesis rubric, a deterministic structure that makes triage reproducible across sweeps:

**Rule 5.1, dedupe by claim, not by line.** The dedupe key is the tuple `(file_path, normalized_section_or_artefact, claim_type)`, not `(file_path, line_number)`. Two passes pointing at the same logical defect with different phrasings collapse to a single synthesized row.

**Rule 5.2, tag every synthesized finding with an evidence letter.** `R` = read-verified with a quoted line; `I` = inferred, no read in this sweep; `K` = already known from the trigger that motivated the sweep. Only `R` findings enter the actionable queue; `I` findings go to a "promote to R by reading" sub-list; `K` findings are dropped after acknowledgement.

**Rule 5.3, severity is adjudicated, not averaged.** Use a fixed three-level scale: `must-fix-now | should-fix-in-this-change | track-as-follow-up`. Where two passes disagree, pick the higher and record both raw severities.

**Rule 5.4, record pass provenance.** Each synthesized row carries the set of passes that surfaced it, so a re-run can attribute coverage gaps to a specific brief.

**Rule 5.5, re-examine large divergence.** Where two passes disagree by more than one severity level, or one reports a finding as real and another flags it as a false positive, re-read the evidence once with both claims side by side before adjudicating, and record that the finding was contested.

Cross-reference each synthesized finding against the project's **false-positive memory** (the exemption file and the project's own dismissed-finding records). Findings previously triaged as not-a-real-finding are suppressed, not re-surfaced.

**Anti-rubric.** Do not average severities, and do not require consensus across all three passes: the passes have non-overlapping specializations, and a defect only one pass could plausibly find must not be down-weighted by the others' silence.

### 6. Triage

Triage depends on whether the finding is **in the configured focus window** (per step 2) or **outside the focus window** (a pre-existing issue surfaced incidentally).

**For findings IN the focus window:** for each High and Medium finding, propose a concrete fix. For Low / FYI findings, document but do not act unless requested. Surface the proposed fix scope to the maintainer when the fix touches a public API or protected artefact, involves an authorial judgement, or spans more than five files; otherwise, where the fix scope is pre-authorized, proceed.

**For findings OUTSIDE the focus window:** surface each finding to the maintainer with named action options (act now, defer to a tracked follow-up, dismiss as not-a-real-finding). Do not auto-defer an out-of-window finding to "Low / FYI" status; the maintainer's per-finding decision is the point.

**Ratcheting-baseline discipline for dismissed findings.** Dismissed findings accumulate in the false-positive memory. The accept-list discipline keeps this from drifting into permanent debt:

- **Rule 6.1, fingerprint not count.** Each dismissed finding gets a stable id: `(file_path, normalized_section_or_artefact, claim_type)` plus the `ruleId` where one was assigned. The accept-list is keyed on the fingerprint, never on a count.
- **Rule 6.2, expiry plus rationale.** Each accept-list entry carries a one-line rationale and an `expires: YYYY-MM-DD` date (default `accepted_on + 90 days`). On expiry, the entry is re-triaged, not auto-renewed.
- **Rule 6.3, net-negative invariant on close.** A sweep cannot close green when the accept-list grew net of fixes.

### 7. Apply fixes, re-baseline, repeat

Apply the fixes. **Re-run step 1 (the full audit standalone) AFTER committing each fix, not on the working tree**: git-history-aware gates (such as the version-bump-recency check) only see committed history. If new findings surface, repeat from step 4. The sweep is complete when one full cycle returns no High or Medium findings.

**Termination conditions** (first matching condition fires):

1. **Empty-delta (primary, principled stop).** An iteration produces zero new High or Medium findings AND the synthesized finding-set is identical (by dedupe key) to the previous iteration's set. The sweep has reached a fixed point.
2. **Patience-plateau (secondary, structural-stall stop).** Two consecutive iterations produce no strict shrinkage of the finding-set. The remaining findings are structurally unresolvable by this sweep alone; surface the residual to the maintainer with a named decision (defer, escalate, descope).
3. **Hard ceiling (runaway guard, defect signal).** Six iterations regardless of state. Hitting this is a signal that something is wrong (a fix-cycle or scope creep), not a signal of completion; report which.

### 8. Record the sweep

Record every sweep, including zero-finding ones, in the project's own working records: the date, the scope bounds used, which of the three passes ran (and the maintainer authorization where a pass was reduced), the findings with their dispositions, and the resulting change. The record is the audit trail that lets a later reader reconstruct the sweep without the working conversation; the trend signal (which classes recur, how iteration counts shrink) lives in it. Before recording a fixed-in-window claim, verify the claim against the actual diff (search for the claim's target text); a claim whose edit is absent is recorded as routed, never as fixed. Where a project keeps archived sweep records inside the repository, place them under a directory its linter-exemption mechanism covers (the corpus wiring names this repository's mechanism); archived records are frozen state, and their `path:line` references are kept verbatim even when lines later shift.

## Reporting

When findings exist, present them prominently to the maintainer at the end of the sweep, not only in the archived record: per finding, the ruleId, the severity, the `path:line` location, a one-line evidence quote, a one-line impact, a one-line recommendation, and the in-window / out-of-window classification. Zero-finding sweeps still get a one-line acknowledgement.

## Red Flags

- Running the audit suite once and declaring the sweep complete without the post-fix re-run.
- Skipping the semantic review because the mechanical gates passed.
- Treating Low findings as automatically actionable (they document; they do not require action).
- Looping past the termination conditions without surfacing the recurring pattern.
- Accepting a review report that infers rather than quotes (insist on quoted evidence).
- Treating "no findings" from a pass as proof when the pass reports no commands run or no files read.

## Verification

The sweep is complete when:

- The full audit programme passes standalone on the final state (exit 0 from the canonical full-audit command).
- All planned review passes have been completed and synthesized.
- All High and Medium findings have been addressed in scope, or surfaced to the maintainer and authorized to defer.
- The cycle has terminated cleanly (one full re-baseline after the last fix with no new High or Medium findings).

If any of these is missing, the sweep is incomplete and a clean-bill report is not yet permitted.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The audit gates pass; that's enough." | Gates prove what they check. The semantic sweep targets what they do not. |
| "I just fixed the one issue; nothing else can be wrong." | Same author, same blind spot. Sibling defects are the typical pattern. |
| "A quick grep will do." | Grep finds what you search for. The structured passes catch what you would not have thought to search for. |
| "The sweep returned clean last time; skip it this time." | The project changes between sweeps. Last time's clean does not authorize this time's skip. |
| "The fix was small; the sweep is overkill." | The sweep's cost is bounded. The cost of a sibling defect that lands compounds. |

## See Also

- Sibling procedure [`validation-sweep-pr-scoped.md`](validation-sweep-pr-scoped.md): the change-scoped form that runs before every merge; this corpus-wide form runs on a periodic cadence.
- Related procedure [`matrix-fit.md`](matrix-fit.md): the semantic-fit audit this sweep can flag control-code doubts to.
- Related procedure [`claim-fit.md`](claim-fit.md): the citation-precision audit this sweep can flag attribution doubts to.
- Canonical gate inventory: [`specification-audit-programme.md`](../specs/specification-audit-programme.md).
