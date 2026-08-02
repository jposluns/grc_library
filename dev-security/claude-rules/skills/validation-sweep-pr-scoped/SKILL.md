---
name: validation-sweep-pr-scoped
description: PR-scoped validation sweep. Runs as a PR's finalizing step, before merge, to catch issues the PR introduced before it lands. Dispatches Subagent A (recent-PR deep review) scoped to the PR's diff plus a lightweight cross-reference check for files cited by other documents. Complements the corpus-wide `validation-sweep` skill: the PR-scoped form is fast and runs on every PR; the corpus-wide form is comprehensive and runs on a periodic cadence the project sets (the parent library's is every 10 merges) or maintainer-triggered. The two skills together cover both per-PR drift (caught fast) and corpus-wide drift (caught broadly).
derives_from: ../../governance/evidence-grounded-completion.md
---

# Validation Sweep, PR-Scoped

## Project wiring (the parent library's instantiation; adopters substitute their own)

Portable procedure, concrete names. In the parent GRC library this skill runs with:

- Per-PR record path pattern: a dated per-PR record in the consuming project's working state (one dated record per merged PR, written when findings exist).
- PR-scoped history register: the PR-scoped validation history register in the consuming project's working state (one row per merged PR, including zero-finding runs and handoff-PR exemption rows; the exemption marker the parity gate recognizes in a row's Findings cell is `SKIPPED` together with `handoff`, or the phrase `handoff-PR exception`, never a bare `n/a`).
- Sibling corpus-wide register it mirrors: the sweep-history register in the consuming project's working state (the `validation-sweep` skill's register; the PR-scoped register follows its row shape).
- Bookkeeping-parity gate: gate 50, `tools/lint-bookkeeping-parity.py`, the mechanical QA-cadence gate that reads the history rows and fails when an in-window merged PR lacks its `/validate-pr` plus `/retro` rows (with the handoff-PR exemption built in).
- Mechanical baseline and pre-flight: the full audit-gate runner `tools/run_all_audits.sh`; the deterministic pre-flight scanner `tools/sweep-preflight-scanner.py` with its exemption file `tools/sweep-preflight-exemptions.json`; the detailed change-log mirror in the consuming project's working state (the surface the chat-surfacing section contrasts with).

An adopting project maps each bullet to its own record paths, registers, gate, runner, and scanner; the procedure below refers to them generically.

## Overview

PR-scoped validation runs as each PR's finalizing step, before merge, to catch issues the PR introduced before they compound across subsequent PRs. (Command names `/validate-pr`, `/validate`, and `/retro` are the parent library's paired commands, used in this document as shorthand; an adopting project reads them as its own equivalents.) Two sibling skills together cover the validation surface:

- **`validation-sweep`** (slash command `/validate`, corpus-wide, periodic on the project's cadence (the parent library's is every 10 merges) or maintainer-triggered): full Subagent A + B + C sweep across the whole corpus. Catches corpus-wide drift (Subagent B's domain), audit-programme integrity issues (Subagent C's domain), and recent-PR issues (Subagent A's domain). Expensive (~150-200k tokens); runs periodically.
- **`validation-sweep-pr-scoped`** (slash command `/validate-pr`, PR-scoped, every PR): single Subagent A dispatch on the PR's diff plus a targeted cross-reference check. Cheap (~30-60k tokens); runs before merge so issues are caught within the same PR, not nine PRs later.

The two are complementary, not redundant. The corpus-wide form catches drift the per-PR scope misses (a citation in file Y becomes stale because PR X touched file Z); the per-PR form catches issues the corpus-wide form would miss between its periodic runs (per-PR issues that compound between sweeps).

## When to Use

- **Mandatory** as a PR's finalizing step, before merge (per the project's PR workflow). It runs after the first green CI and before the merge, paired with the finalizing retrospective, with both record rows committed in-PR before CI re-runs and the PR merges. (The parent library's concrete sequence: open PR -> first green CI -> `/validate-pr` -> `/retro` -> write rows in-PR -> commit -> CI -> merge -> sync main -> delete branch -> next-PR planning.)
- Optionally, after a manual investigation needs to confirm a specific PR's impact.

**No orchestrator-side skip discretion AND no abbreviation discretion.** The mandatory invocation has no carve-outs for "meta PRs", "housekeeping PRs", "sweep close-outs", "the PR that introduces this skill", or any other class. The orchestrator does NOT have discretion to skip a `/validate-pr` invocation based on a judgement that the PR is "too small to need it", "circular", or "already validated by another mechanism". Equally, the orchestrator does NOT have discretion to substitute an abbreviated check, a spot-check, a memory-only review, an orchestrator-self-check, a "quick scan", or any other informal substitute for the formal Subagent A dispatch the skill encodes. "Abbreviated /validate-pr" is not a sanctioned shape; the only sanctioned shapes are the full formal run and a maintainer-authorized explicit exception recorded in the history-row Summary cell with rationale. Throughput pressure (a long batch of PRs, a tight session window, an apparent need to make progress) does NOT authorize abbreviation; the per-PR validation IS the pace, and "the next PR will catch it" is the failure mode this rule prevents. Every successful merge triggers a formal `/validate-pr`. If the run returns zero findings, the history-row records that zero-findings state, which is itself the proof-of-discipline. Skipping or abbreviating a quality-assurance step is a policy deviation the orchestrator cannot authorize unilaterally; only the project maintainer can grant a documented exception, recorded explicitly in the history-row Summary cell with the rationale.

**The session-closing handoff PR: normal path, with a narrow fallback.** A session ends by landing its working-state on the protected branch as a green, merged PR (the session-closing handoff PR). Under the synchronous model that PR normally runs its OWN `/validate-pr` (and the paired `/retro`) before it is finalized, like any other PR: because the rows land in the PR itself rather than batching into a next PR, no recursion arises, so there is no default reason to skip. A documented FALLBACK is retained only for the genuine loop-termination edge, a handoff PR whose own QA cannot be made self-contained within it at the session boundary; in that case only, the handoff PR skips its trailing `/validate-pr` / `/retro`. Independently of the fallback, the next session's resume routine runs a full corpus-wide `/validate` as its first task; that sweep is a fresh-session drift-catch valuable in its own right (whole corpus, no accumulated session context), not merely compensation for a skipped sweep. When the fallback is taken it is recorded in the history row's Findings cell with the recognized marker and its rationale, and a mechanical QA-cadence gate must build in this handoff-PR exemption so it does not fail on the legitimately-absent row.

`/validate-pr` runs as the finalizing step BEFORE merge, on the PR's own branch state (synced to current `main`), after the first CI pass and before the merge that lands it. CI remains the mechanical pre-merge gate; `/validate-pr` is the semantic pre-merge gate, catching stale-prose and cross-document defects the mechanical gates do not. Its row is committed into the same PR and CI re-runs on the row-carrying commit before merge; the residual class of pure post-merge merge-base drift is re-checked by that re-run and by the next session's resume `/validate`.

## Process

The PR-scoped sweep runs in five steps. Steps 1-2 establish scope; step 3 is the focused subagent dispatch; step 4 is the lightweight cross-reference check; step 5 records.

### 1. Identify the PR being finalized

Capture the PR state:

- PR number (from the open PR via `gh pr view` or `mcp__github__pull_request_read`).
- The base SHA the PR branches from (`git merge-base main HEAD`).
- The PR's diff against its base (`git diff <base>...HEAD`, branch synced to `main`).
- The list of touched files in the diff (`git diff --name-only <base>...HEAD`).

### 2. Establish mechanical baseline (pre-merge, branch synced to `main`)

Run the project's full audit-gate runner (named in the project wiring above) standalone against the branch state (synced to current `main`). CI ran this on the branch; this confirms the gates are clean before the PR is finalized. Mechanical failures here are rare (they would have failed CI), but a stale branch can differ from current `main` due to merge-base drift, which is why the branch is synced to `main` before this run.

If any gate fails, fix the underlying defect first (open a hot-fix PR), then return to step 1 against the corrected state.

### 3. Dispatch Subagent A scoped to the PR's diff

Subagent A receives:

- The PR diff (full text).
- The list of touched files.
- The full state of each touched file on the branch being finalized.
- A pre-flight scanner output filtered to the touched files (run the project's deterministic pre-flight scanner and filter the output to the touched file set; if no scanner output relevant to touched files, proceed unhinted).

Subagent A looks for the same eight failure-mode classes from the corpus-wide `validation-sweep` SKILL, scoped to the touched files:

1. Stale prose references introduced by the PR.
2. Mis-attributed citations introduced by the PR.
3. Multi-surface incompleteness introduced by the PR.
4. Inferred-as-verified state assertions in the PR's prose.
5. Per-document version-bump omission (mechanically gated, but worth verifying).
6. Generated-artefact lag (mechanically gated, but worth verifying).
7. Stale docstrings in any Python file the PR touched.
8. Cross-document term drift introduced by the PR.

**Pre-tool verification preamble**: each subagent brief instructs the subagent to state in one line, before each tool call, (a) the hypothesis the call tests, (b) the observation that would falsify it, and (c) one prior tool result that does not already answer the question. Undefined falsifier means skip the call as corroboration-only.

Subagent A reports findings as SARIF-lite blocks (same format as `validation-sweep`): tool, ruleId, level, location, fingerprint, rubric, evidence. Every finding must quote a specific `path:line`.

### 4. Targeted cross-reference check

For each touched file in the PR, identify which OTHER files in the corpus cite it. Use `grep` to find citations:

```bash
for f in <touched-files>; do
  filename=$(basename "$f")
  grep -rln "$filename" --include="*.md" . 2>/dev/null | grep -v "$f"
done
```

For each citing file, do a shallow check:

- Does the citation still resolve (the cited section, version, line is still valid on the branch being finalized)?
- Has the touched file's header text changed in a way that breaks the citer's quoted text?
- Has any cross-reference become stale (e.g., the cited PR number is now wrong, the cited Version is now wrong)?

This is a subset of `validation-sweep` Subagent B's scope, restricted to citers of the touched files only. Cheap; high-signal. It catches the "PR X touched file A, but file C citing A is now stale" failure mode that the per-PR scope would otherwise miss.

### 5. Triage and record

Triage findings:

- **In-window** (the PR introduced the issue): fix it in THIS PR before finalizing. A dedicated hot-fix PR only if the fix genuinely cannot land in-PR (it runs its own sync + `/validate-pr` when merged).
- **Out-of-window** (the PR exposed a pre-existing issue not introduced by the merge): surface to the operator with named options.

Record:

- A per-PR validation record at the project's dated per-PR record path (the parent library's pattern is named in the project wiring above) with the findings and triage. Six top-level H2 sections: Trigger and state snapshot, Subagent A return, Cross-reference check, Orchestrator triage, Resulting hot-fix PR (if any), Notes.
- An entry in the PR-scoped history register (the PR-scoped mirror of the corpus-wide sweep's register; both are named in the project wiring above; one row per merged PR).

Zero-finding PR-scoped sweeps still get a history row (one line); only the per-PR record file is conditional on findings.

Before committing either surface, verify each fixed-in-window claim against the actual diff (grep for the claim's target text); a claim whose edit is absent is downgraded to routed, never recorded as fixed (the record-asserts-unapplied-fix guard, shared with the guardrail-review and corpus-sweep record steps).

The `/retro` skill (the finalizing retrospective) consumes `/validate-pr`'s findings as input for its Issues-encountered section.

## Pre-flight scanner

Run the project's deterministic pre-flight scanner (named in the project wiring above) and filter the output to the touched-files set. Hand the filtered output to Subagent A as a known-candidate list. The scanner applies in-scanner heuristics and a project-maintained exemption file.

If no scanner output is relevant to the touched files, the subagent proceeds unhinted.

## Output format

Same SARIF-lite block format as `validation-sweep`. Reuse the failure-mode catalogue and the synthesis rubric.

## Surfacing findings in chat

**When findings exist, surface them prominently in the chat reply, not only in the per-PR record file.** The chat surface is for maintainer awareness and triage; the per-PR record file is the authoritative archive. A maintainer should not need to open the dated per-PR record file or scroll through the detailed change-log mirror to see what the sweep found.

Chat-surface shape: a per-finding line (or short block) carrying the ruleId, the severity / level, the `path:line` location, a one-line evidence quote, a one-line impact, a one-line recommendation, and the in-window / out-of-window classification. Group by severity tier if multiple findings landed. Zero-finding sweeps still need a one-line chat acknowledgement that the sweep ran clean.

The chat surface is non-negotiable when the sweep produces findings: a finding that lives only in working-state record files is not surfaced to the maintainer's attention.

## Termination

The PR-scoped sweep is a single-iteration cycle: dispatch, check, triage, record. If findings produce a hot-fix PR, that hot-fix PR is itself a new merge that triggers its own `/validate-pr` cycle.

There is no fixed-point loop (unlike `/validate`'s iterative cycle). Per-PR sweeps are short-lived; the corpus-wide sweep handles deeper iteration.

### Synchronous same-PR recording (recursion-avoidance retired)

The no-skip discipline says every PR gets a `/validate-pr` and every invocation gets a history row. The old model deferred that row (and any fix) into a *next* PR to avoid a recording-triggers-a-PR cascade. The synchronous model dissolves the cascade at its root by recording in-PR: the row that records PR N is committed IN PR N, recording PR N's own number, and a finding is fixed in PR N before it merges (a dedicated hot-fix PR only when the fix cannot be co-committed). The sequence is: open PR, run the sweep, disposition findings, write the row, commit, CI re-runs, merge. There is no placeholder row and no back-fill. The audit trail is intact: the row records the PR's own number and, for a finding, that it was fixed in the same PR. The consuming project's QA-record completeness check enforces the model (its completeness window includes the PR being finalized; a present-but-still-pending row that never records a returned result fails).

## Red Flags

- `/validate-pr` skipped because "no findings expected", every merge generates new state worth checking; the per-PR record is the proof-of-check.
- Findings surfaced but not triaged.
- Per-PR record file omitted because "no findings", the history row substitutes; both record absence-of-finding so future readers know the check ran.
- Hot-fix PR opened without its own `/validate-pr` run after merging.
- Cross-reference check skipped because "Subagent A already covered it", Subagent A reviews the touched files; the cross-reference check reviews the FILES THAT CITE the touched files. Different scope; both required.

## Verification

The PR-scoped sweep is complete when:

- Mechanical baseline confirmed clean on the branch state.
- Subagent A has been dispatched on the PR's diff and returned findings (or zero-findings).
- The cross-reference check has been run on the touched files' citers.
- Findings (if any) are triaged with in-window / out-of-window classification.
- The per-PR record file is written (if findings exist).
- The history file has a new row for this PR.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The PR was small; skip /validate-pr" | Smaller PRs sometimes have cross-references missed because the orchestrator didn't think they were worth checking. Run it every merge. |
| "The next PR will catch any issues" | Maybe; but compounding is faster. Catch at the merge, not five PRs later. |
| "This is redundant with the corpus-wide /validate" | They're complementary. The corpus-wide sweep runs on its periodic cadence; /validate-pr catches issues in the PRs between sweeps. |
| "Cross-reference check is too expensive" | It's bounded to the citers of the touched files; typically 0-5 files per check. Cheap. |
| "If CI passed, the PR is clean" | CI catches mechanical defects; /validate-pr catches semantic defects (stale prose, cross-document drift) that mechanical gates do not. |

## See Also

- Sibling skill [`validation-sweep`](../validation-sweep/SKILL.md) (slash command `/validate`): corpus-wide periodic sweep.
- Related skill [`pr-retrospective`](../pr-retrospective/SKILL.md) (slash command `/retro`): consumes `/validate-pr` findings as input for the finalizing retrospective and improvement-log register.
- Canonical rule [`evidence-grounded-completion`](../../governance/evidence-grounded-completion.md): the assertion-side discipline this skill operationalizes.
- Canonical rule [`ai-assistant-workflow-disciplines`](../../governance/ai-assistant-workflow-disciplines.md): the workflow disciplines this skill supports; PR-scoped validation is the "every merge" discipline that complements the periodic full sweep (in the parent library, every 10 merges).
- Pre-flight scanner: the deterministic pre-flight check shared with the corpus-wide skill (the parent library's concrete scanner is named in the project wiring above).

## Why this skill exists

The corpus-wide `/validate` sweep runs on a periodic cadence (the parent library's is every 10 merges, or maintainer-triggered). Between sweeps, issues introduced by individual PRs compound silently: a PR touches file A; subsequent PRs cite the changed file A; the citation may have been stale from the start, but no one checks until the next corpus-wide sweep. By then, the issue has been re-cited in 5+ places.

`/validate-pr` closes this gap. Run after every merge, it catches PR-introduced issues at the moment they appear, before they compound. The cost is modest (~30-60k tokens per merge); the benefit is keeping the corpus-wide sweep's iteration count low and the per-PR feedback loop tight.

For AI coding assistants specifically: when you are finalizing a PR, before you merge it, your default steps are `/validate-pr`, then `/retro`, then the merge. The three together close the per-PR loop; the corpus-wide `/validate` closes the wider loop on its own cadence.
