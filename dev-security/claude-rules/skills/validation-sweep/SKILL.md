---
name: validation-sweep
description: Corpus-wide regression sweep run as a follow-up after any issue is identified and corrected, to confirm no sibling issue remains anywhere in the repository. Invoke after fixes that touch multi-surface artefacts, gate inventories, prose claims about repo state, AI-inferred citations, or generated artefacts. Combines the mechanical audit suite with a structured semantic fan-out, and loops until clean.
derives_from: ../../governance/evidence-grounded-completion.md
---

# Validation Sweep

## Overview

After a single defect is found and fixed, a sibling defect may still be lurking elsewhere: same author, same session, same inferred mental model, same blind spot. The mechanical audit gates catch their own classes; this skill is the structured corpus-wide sweep that catches what the gates do not. It targets cross-file prose drift, mis-attributed citations, multi-surface incompleteness in places the gate-name parity audit does not police, inferred-as-verified state assertions, and the other failure-mode classes catalogued below.

The sweep is fixed-point: if it finds anything, fix it, then re-run the sweep, until the sweep returns clean. The audit gates are the ground truth for mechanical claims; the parallel subagent fan-out is the ground truth for the semantic claims the gates cannot mechanise.

The skill is project-agnostic in shape but invokes project-specific commands; the GRC Library's canonical full-audit command is [`tools/run_all_audits.sh`](../../../../tools/run_all_audits.sh) and the canonical gate inventory is [`governance/specification-audit-programme.md`](../../../../governance/specification-audit-programme.md) §6.

## When to Use

- Immediately after identifying and correcting any issue in the repository, as a follow-up that confirms no sibling issue remains.
- When taking over from a previous session whose work has not been verified on the current state.
- After landing a PR that touched any "parallel surface" set: the gate inventory, a version-history table, a framework-alignment table, mirror-synced files, generated artefacts.
- Before declaring a multi-PR programme phase complete.
- Periodically, informed by the document-staleness audit (gate 31 in the canonical inventory).
- Whenever a user surfaces an AI-introduced error and asks for assurance that no sibling error remains.

## Process

The sweep runs in seven steps. Steps 1-3 establish the baseline and scope; steps 4-5 are the semantic sweep; step 6 triages; step 7 is the fixed-point loop that runs until clean.

### 1. Establish mechanical baseline

Run the canonical full-audit command standalone. For the GRC Library: `tools/run_all_audits.sh`. Capture exit code and any failure output. The expected state is exit 0 on the current working tree.

If the audit reports failures, the sweep cannot proceed semantically until the mechanical baseline is clean. Address the gate failures first, then return to this step.

### 2. Enumerate recent changes

Identify the scope of recently-touched files. The focus window is **the past two calendar days**: wide enough to span overnight handoffs, weekend work, and post-meeting reviews; narrow enough that the in-window set stays reviewable.

- `git log --since="2 days ago" --name-only --pretty=format:""` : files touched in the focus window.
- `git status --short` : files in the current working tree.
- `git log --name-only -10` : files touched in the last ten commits, as additional context.

These files are the highest-priority targets for the semantic sweep. Findings on files outside the focus window (i.e. on pre-existing issues the sweep surfaces incidentally) are still reportable and ARE handled by step 6, not silently discarded.

### 3. Identify failure-mode classes in scope

The sweep targets failure modes the mechanical gates do not cover. Each class has a known shape; new classes may surface as the corpus and the audit programme evolve.

| Class | Shape |
| --- | --- |
| Stale prose references | "N gates" or "gates 1-N" or "the N-gate programme" prose where N is no longer the canonical count; library, spec, or pack version mentioned in prose that has since bumped. |
| Mis-attributed citations | A citation of "step X" or "section Y" of another file where the cited content does not match the source; phrase-level quotes attributed to one rule but actually living in another. |
| Multi-surface incompleteness | A change that should update N surfaces but updated N-1: CHANGELOG entry coverage of files touched, README claims, pack version-history table, governance registers, doctype-doctype cross-references. |
| Inferred-as-verified state assertions | A claim about a file's contents written without re-reading the file. |
| Per-document version-bump omission | A non-exempt document substantively changed but its `Version:` field not bumped. |
| Generated-artefact lag | A source file edited but its generator not re-run, or vice versa; the gates catch the drift but the underlying lag is the failure. |
| Stale docstrings | A linter or script docstring describing behaviour that no longer matches the code. |
| Cross-document term drift | Different files use different terms for the same concept, with no canonical glossary entry to anchor the choice. |

### 3.5. Run the deterministic pre-flight scanner (optional but recommended)

Before subagent fan-out, run the pre-flight scanner: `python3 tools/sweep-preflight-scanner.py`. This is a deterministic regex-based pass that surfaces candidate findings for shapes the high-precision mechanical gates do not catch (stale skill counts, stale governance-rule counts, prose-form number drift). The scanner exits 0 always; its output is a list of candidates, not verified findings.

Pass the scanner's output to each subagent as a "known suspect locations to verify or dismiss" list. This lowers each subagent's discovery burden and guarantees candidate shapes the gates miss get semantic triage. Many candidates will be false positives (legitimate historical references, comparative prose, references to other projects' counts); that is expected: the scanner is high-recall, the subagent triage is the precision layer.

The scanner is project-specific (its `CANONICAL_COLLECTIONS` and seed patterns target this corpus); other projects adopting the validation-sweep pattern should swap in their own scanner with project-specific patterns.

### 4. Fan out parallel subagent reviews

Launch subagents in parallel for the semantic sweep. Each receives a self-contained brief, reads target files in full (not excerpts), and reports findings by severity. The three baseline briefs:

- **Subagent A : recent-PR deep review**. Read every file touched by the recent PRs in full; verify every CHANGELOG entry, commit message, and docstring claim against the actual diff; specifically flag mis-attributed citations and claims that contradict the file's actual contents.
- **Subagent B : corpus-wide stale-reference sweep**. Grep the corpus for stale gate counts, library versions, pack versions, and dates; cross-check against the canonical sources (README, spec §6 inventory).
- **Subagent C : audit-programme integrity check**. Independently re-verify that all parity surfaces agree (workflow, runner, pre-commit, spec inventory); verify mirror-sync between pack sources and local copies; verify any new linter's docstring matches its code; spot-check generated-artefact regeneration.

Each subagent reports under 600 words, grouped by severity:
- **High**: factual error, stale reference in a normative document, mis-attribution.
- **Medium**: style inconsistency, minor wording drift, off-by-one in a count.
- **Low / FYI**: cosmetic, historical context, worth noting but not actionable.

**Required for every finding**: a `path:line` evidence quote. A finding without an explicit file path and line number (or line range) is not a finding, it is a hypothesis. Reject any subagent report whose findings lack quoted evidence and re-dispatch the subagent with a re-emphasized brief. This guards against the failure mode where a subagent returns an inferred or confused report instead of read-verified findings; without enforcement of the evidence requirement, the sweep degrades into inference cascade.

If the working tree shows no recent activity (a "cold" sweep), subagent A becomes a narrower spot-check of the most recently-merged PRs (`git log -5 --merges`).

### 5. Synthesise findings

Deduplicate findings across the subagents. For each finding, record: file path + line range; concrete description; whether the subagent verified by reading or inferred (**insist on the former; reject any finding that lacks an explicit `path:line` quote**).

Cross-reference each finding against [`governance/register-sweep-history.md`](../../../../governance/register-sweep-history.md)'s **false-positive memory** section. Findings the maintainer has previously triaged as not-a-real-finding are suppressed; they should not be re-surfaced.

### 6. Triage

Triage depends on whether the finding is **in the focus window** (the past two calendar days, per step 2) or **outside the focus window** (a pre-existing issue surfaced incidentally).

**For findings IN the focus window:**

For each High and Medium finding, propose a concrete fix. For Low / FYI findings, document but do not act unless requested. Surface the proposed fix scope to the operator if any of the following is true: the fix touches a public API or branch-protected artefact; the fix involves an authorial judgement (which option, which scope); the fix spans more than five files. Otherwise, if the operator has pre-authorised the fix scope, proceed.

**For findings OUTSIDE the focus window:**

Surface each finding to the operator with named action options (action now, defer to a tracked follow-up, dismiss as not-a-real-finding). Do not auto-defer an out-of-window finding to "Low / FYI" status; the operator's per-finding decision is the point. The default action is "ask, then do what the operator says"; the failure mode this guards against is silent triage of pre-existing issues that the sweep is well-placed to surface but no longer-running ticket exists to track. The cost of asking is small; the cost of the operator not knowing the sweep saw the finding is larger.

### 7. Apply fixes, re-baseline, repeat

Apply the fixes. **Re-run step 1 (the full audit standalone) AFTER committing each fix, not on the working tree**. Per the canonical rule's "Relying on prior runs" anti-pattern, the audit must see the final state; per the git-history-aware-gates discipline, the audit's view of "final state" is the committed git history, not the uncommitted working tree. Running the audit on uncommitted changes misses what git-history-aware gates (e.g. a corpus version-bump-recency check) would flag once those changes are committed. If new findings surface, repeat from step 4. The sweep is complete when one full cycle returns no High or Medium findings.

Cap: if the cycle runs more than three iterations without converging, stop and surface the pattern to the operator. Recurring findings across iterations suggest a structural issue the sweep cannot resolve on its own.

### 8. Append to the sweep history register

After the cycle terminates, append an entry to [`governance/register-sweep-history.md`](../../../../governance/register-sweep-history.md) recording: the trigger reason, the state (library / spec / pack versions at HEAD), the count of findings by class and severity, the actions taken, and the resulting PR (if any). Update the recurring-class summary table at the same time. Findings dismissed as not-a-real-finding go into the false-positive memory section with the maintainer's rationale, so a future sweep does not re-litigate.

The register is the cumulative record of what the sweep has caught over time. Its trend signal (which classes recur, which classes have closed via mechanical gates) is the maintainer's input to the priority question "which mechanical gate should we ship next".

## Red Flags

- Running the audit suite once and declaring the sweep complete without the post-fix re-run.
- Skipping the semantic subagent fan-out because the mechanical gates passed.
- Treating Low findings as automatically actionable (they document; they do not require action).
- Looping more than three times without surfacing the pattern.
- Accepting a subagent report that infers rather than quotes (insist on quoted evidence).
- Treating "no findings" from a subagent as proof when the subagent reports no commands run or no files read.

## Verification

The sweep is complete when:
- The full audit programme passes standalone on the final state (exit 0 from the canonical full-audit command).
- All planned subagent reports have been received and synthesised.
- All High and Medium findings have been addressed in scope, or surfaced to the operator and pre-authorised to defer.
- The cycle has terminated cleanly (one full re-baseline after the last fix with no new High or Medium findings).

If any of these is missing, the sweep is incomplete and a clean-bill report is not yet permitted.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The audit gates pass; that's enough." | Gates prove what they check. The semantic sweep targets what they do not. |
| "I just fixed the one issue; nothing else can be wrong." | Same author, same session, same blind spot. Sibling defects are the typical pattern. |
| "Subagents are expensive; I'll just grep myself." | Grep finds what you search for. The subagents catch what you would not have thought to search for. |
| "The sweep returned clean last time; skip it this time." | The corpus changes between sweeps. Last time's clean does not authorise this time's skip. |
| "The fix was small; the sweep is overkill." | The sweep's cost is bounded. The cost of a sibling defect that lands compounds. |

## See Also

- Canonical rule [`governance/evidence-grounded-completion.md`](../../governance/evidence-grounded-completion.md), specifically the `## Worked example: the multi-surface gate-name parity case` section that motivates this sweep.
- Related skill [`evidence-grounded-completion`](../evidence-grounded-completion/SKILL.md): the per-claim verification protocol this sweep applies at corpus scope.
- Related skill [`gate-discipline-diagnose`](../gate-discipline-diagnose/SKILL.md): when a mechanical gate fails, that skill diagnoses; this sweep then verifies the fix is complete.
- Related skill [`clarify-before-acting`](../clarify-before-acting/SKILL.md): when the sweep surfaces a fix that requires authorial choice (which option, which scope), invoke clarify-before-acting before applying.
- Related skill [`citation-quote-verification`](../citation-quote-verification/SKILL.md): when the sweep flags a finding on citation-bearing content, this skill is the targeted follow-up that verifies quote-to-source correspondence.
- Related skill [`fresh-reader-validation`](../fresh-reader-validation/SKILL.md): when the sweep flags a substantively-revised governance document, this skill is the per-document follow-up that surfaces tacit-context gaps via a fresh-context subagent.
