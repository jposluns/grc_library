---
name: validation-sweep-pr-scoped
description: PR-scoped validation sweep. Runs after every successful PR merge to catch issues the merge introduced before they compound across subsequent PRs. Dispatches Subagent A (recent-PR deep review) scoped to the just-merged PR's diff plus a lightweight cross-reference check for files cited by other documents. Complements the corpus-wide `validation-sweep` skill (`/validate`): `/validate-pr` is fast and runs after every merge; `/validate` is comprehensive and runs every 10 merges or maintainer-triggered. The two skills together cover both per-PR drift (caught fast) and corpus-wide drift (caught broadly).
derives_from: ../../governance/evidence-grounded-completion.md
---

# Validation Sweep, PR-Scoped

## Overview

PR-scoped validation runs after every merged PR to catch issues the merge introduced before they compound across subsequent PRs. Two sibling skills together cover the validation surface:

- **`validation-sweep`** (slash command `/validate`, corpus-wide, every 10 merges or maintainer-triggered): full Subagent A + B + C sweep across the whole corpus. Catches corpus-wide drift (Subagent B's domain), audit-programme integrity issues (Subagent C's domain), and recent-PR issues (Subagent A's domain). Expensive (~150-200k tokens); runs periodically.
- **`validation-sweep-pr-scoped`** (slash command `/validate-pr`, PR-scoped, every merge): single Subagent A dispatch on the just-merged PR's diff plus a targeted cross-reference check. Cheap (~30-60k tokens); runs immediately after merge so issues are caught within one PR cycle, not nine.

The two are complementary, not redundant. The corpus-wide form catches drift the per-PR scope misses (a citation in file Y becomes stale because PR X touched file Z); the per-PR form catches issues the corpus-wide form would miss in its 10-PR interval (per-PR issues that compound between sweeps).

## When to Use

- **Mandatory** after every successful PR merge (per the project's PR workflow). Runs as part of the post-merge sequence: sync main → delete merged branch → `/validate-pr` → `/retro` → next-PR planning.
- Optionally, after a manual investigation needs to confirm a specific PR's impact.

**No orchestrator-side skip discretion.** The mandatory invocation has no carve-outs for "meta PRs", "housekeeping PRs", "sweep close-outs", "the PR that introduces this skill", or any other class. The orchestrator does NOT have discretion to skip a `/validate-pr` invocation based on a judgement that the PR is "too small to need it", "circular", or "already validated by another mechanism". Every successful merge triggers a `/validate-pr`. If the run returns zero findings, the history-row records that zero-findings state, which is itself the proof-of-discipline. Skipping a quality-assurance step is a policy deviation the orchestrator cannot authorise unilaterally; only the project maintainer can grant a documented exception, recorded explicitly in the history-row Summary cell with the rationale.

`/validate-pr` does NOT run before merge (CI is the pre-merge gate). It runs AFTER merge to catch post-merge state issues , exactly the class of issue that cannot be caught by CI on the feature branch alone.

## Process

The PR-scoped sweep runs in five steps. Steps 1-2 establish scope; step 3 is the focused subagent dispatch; step 4 is the lightweight cross-reference check; step 5 records.

### 1. Identify the just-merged PR

Capture the merge state:

- PR number (from the merge commit message or via `mcp__github__pull_request_read`).
- Merge commit SHA (`git log --merges -n 1 --pretty=format:"%H %s"`).
- The PR's diff (`git diff <merge-commit>^..<merge-commit>`).
- The list of touched files in the diff (`git diff --name-only <merge-commit>^..<merge-commit>`).

### 2. Establish mechanical baseline (post-merge state)

Run `tools/run_all_audits.sh` standalone against the post-merge state. CI ran this on the feature branch; this confirms the post-merge state on main is also clean. Mechanical failures here are rare (they would have failed CI), but post-merge state can differ from feature-branch state due to merge-base drift.

If any gate fails, fix the underlying defect first (open a hot-fix PR), then return to step 1 against the corrected state.

### 3. Dispatch Subagent A scoped to the PR's diff

Subagent A receives:

- The PR diff (full text).
- The list of touched files.
- The full state of each touched file post-merge.
- A pre-flight scanner output filtered to the touched files (run `python3 tools/sweep-preflight-scanner.py` and filter the output to the touched file set; if no scanner output relevant to touched files, proceed unhinted).

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

- Does the citation still resolve (the cited section, version, line is still valid post-merge)?
- Has the touched file's header text changed in a way that breaks the citer's quoted text?
- Has any cross-reference become stale (e.g., the cited PR number is now wrong, the cited Version is now wrong)?

This is a subset of `validation-sweep` Subagent B's scope, restricted to citers of the touched files only. Cheap; high-signal. It catches the "PR X touched file A, but file C citing A is now stale" failure mode that the per-PR scope would otherwise miss.

### 5. Triage and record

Triage findings:

- **In-window** (the PR introduced the issue): the fix is the PR's responsibility. If small, queue as a hot-fix PR (or include in the next PR if the next PR naturally touches the same files); if substantive, open a dedicated follow-up PR.
- **Out-of-window** (the PR exposed a pre-existing issue not introduced by the merge): surface to the operator with named options.

Record:

- A per-PR validation record at `.working/validate-pr/<YYYY-MM-DD>-PR-<N>.md` with the findings and triage. Six top-level H2 sections: Trigger and state snapshot, Subagent A return, Cross-reference check, Orchestrator triage, Resulting hot-fix PR (if any), Notes.
- An entry in `.working/validate-pr/history.md` (similar to validate-sweeps/history.md but PR-scoped, one row per merged PR).

Zero-finding PR-scoped sweeps still get a history row (one line); only the per-PR record file is conditional on findings.

The `/retro` skill (post-merge retrospective) consumes `/validate-pr`'s findings as input for its Issues-encountered section.

## Pre-flight scanner

Run `python3 tools/sweep-preflight-scanner.py` and filter the output to the touched-files set. Hand the filtered output to Subagent A as a known-candidate list. The scanner applies in-scanner heuristics and an exemption file at `tools/sweep-preflight-exemptions.json`.

If no scanner output is relevant to the touched files, the subagent proceeds unhinted.

## Output format

Same SARIF-lite block format as `validation-sweep`. Reuse the failure-mode catalogue and the synthesis rubric.

## Surfacing findings in chat

**When findings exist, surface them prominently in the chat reply, not only in the per-PR record file.** The chat surface is for maintainer awareness and triage; the per-PR record file is the authoritative archive. A maintainer should not need to open `.working/validate-pr/<date>-PR-<N>.md` or scroll through `CHANGELOG-detailed.md` to see what the sweep found.

Chat-surface shape: a per-finding line (or short block) carrying the ruleId, the severity / level, the `path:line` location, a one-line evidence quote, a one-line impact, a one-line recommendation, and the in-window / out-of-window classification. Group by severity tier if multiple findings landed. Zero-finding sweeps still need a one-line chat acknowledgement that the sweep ran clean.

The chat surface is non-negotiable when the sweep produces findings: a finding that lives only in `.working/` files is not surfaced to the maintainer's attention.

## Termination

The PR-scoped sweep is a single-iteration cycle: dispatch, check, triage, record. If findings produce a hot-fix PR, that hot-fix PR is itself a new merge that triggers its own `/validate-pr` cycle.

There is no fixed-point loop (unlike `/validate`'s iterative cycle). Per-PR sweeps are short-lived; the corpus-wide sweep handles deeper iteration.

### Batching into the next PR (recursion-avoidance)

The no-skip-discretion discipline says every merge gets a `/validate-pr` invocation, and every invocation gets a history row. Applied naively this creates a recursion: PR #N's history row (or fix-PR) needs its own PR #N+1, whose own /validate-pr generates more recording or fix work, and so on. The PR cascade compounds even when each subsequent invocation returns trivial findings or zero findings.

**Resolution**: `/validate-pr` outputs are **batched into the next PR, whatever its substantive purpose**. Two sub-cases:

1. **Zero-finding invocations**: the history row alone is deferred. Append it to `.working/validate-pr/history.md` as part of the next PR's diff, alongside the next PR's other changes. The /validate-pr invocation itself still runs immediately after the merge it follows; only the row commit waits.

2. **Findings-producing invocations**: the fix(es) for the surfaced findings are bundled into the next PR. Do NOT open a dedicated hot-fix PR for /validate-pr findings; the next PR (whatever its purpose) absorbs the fixes alongside its own work. This keeps the PR-per-finding cascade from compounding. The findings still get a history row immediately (same as zero-finding); the row records "fixed in PR #N+M" once the next PR ships the fix.

A findings-producing `/validate` (the corpus-wide sibling) may still warrant its own close-out PR when the findings are numerous or coherent enough to make a dedicated PR clearer than a bundle, but this is the exception, not the default; for `/validate-pr` the bundle is always the default.

The batching's audit trail is intact: the history row records the originating PR number and the closing PR number, so a future reader traces from the row to both the source and the fix in one hop. The discipline is preserved; only the ship-immediacy is relaxed.

## Red Flags

- `/validate-pr` skipped because "no findings expected" , every merge generates new state worth checking; the per-PR record is the proof-of-check.
- Findings surfaced but not triaged.
- Per-PR record file omitted because "no findings" , the history row substitutes; both record absence-of-finding so future readers know the check ran.
- Hot-fix PR opened without its own `/validate-pr` run after merging.
- Cross-reference check skipped because "Subagent A already covered it" , Subagent A reviews the touched files; the cross-reference check reviews the FILES THAT CITE the touched files. Different scope; both required.

## Verification

The PR-scoped sweep is complete when:

- Mechanical baseline confirmed clean on post-merge state.
- Subagent A has been dispatched on the PR's diff and returned findings (or zero-findings).
- The cross-reference check has been run on the touched files' citers.
- Findings (if any) are triaged with in-window / out-of-window classification.
- The per-PR record file is written (if findings exist).
- The history file has a new row for this PR.

## Common Rationalizations

| Rationalisation | Reality |
|---|---|
| "The PR was small; skip /validate-pr" | Smaller PRs sometimes have cross-references missed because the orchestrator didn't think they were worth checking. Run it every merge. |
| "The next PR will catch any issues" | Maybe; but compounding is faster. Catch at the merge, not five PRs later. |
| "This is redundant with the corpus-wide /validate" | They're complementary. /validate runs every 10 merges; /validate-pr catches issues in the 9 PRs between sweeps. |
| "Cross-reference check is too expensive" | It's bounded to the citers of the touched files; typically 0-5 files per check. Cheap. |
| "If CI passed, the PR is clean" | CI catches mechanical defects; /validate-pr catches semantic defects (stale prose, cross-document drift) that mechanical gates do not. |

## See Also

- Sibling skill [`validation-sweep`](../validation-sweep/SKILL.md) (slash command `/validate`): corpus-wide periodic sweep.
- Related skill [`pr-retrospective`](../pr-retrospective/SKILL.md) (slash command `/retro`): consumes `/validate-pr` findings as input for the post-merge retrospective and improvement-log register.
- Canonical rule [`evidence-grounded-completion`](../../governance/evidence-grounded-completion.md): the assertion-side discipline this skill operationalises.
- Canonical rule [`ai-assistant-workflow-disciplines`](../../governance/ai-assistant-workflow-disciplines.md): the workflow disciplines this skill supports; PR-scoped validation is the "every merge" discipline that complements the "every 10 merges" full sweep.
- Pre-flight scanner [`tools/sweep-preflight-scanner.py`](../../../../tools/sweep-preflight-scanner.py): the deterministic pre-flight check shared with the corpus-wide skill.

## Why this skill exists

The corpus-wide `/validate` sweep runs every 10 merges (or maintainer-triggered). Between sweeps, issues introduced by individual PRs compound silently: a PR touches file A; subsequent PRs cite the changed file A; the citation may have been stale from the start, but no one checks until the next corpus-wide sweep. By then, the issue has been re-cited in 5+ places.

`/validate-pr` closes this gap. Run after every merge, it catches PR-introduced issues at the moment they appear, before they compound. The cost is modest (~30-60k tokens per merge); the benefit is keeping the corpus-wide sweep's iteration count low and the per-PR feedback loop tight.

For AI coding assistants specifically: when you have just merged a PR, your default next step is `/validate-pr`, then `/retro`, then the next PR's planning. The three together close the per-PR loop; the corpus-wide `/validate` closes the wider loop on its own cadence.
