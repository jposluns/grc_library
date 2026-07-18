---
name: pr-retrospective
description: Post-merge retrospective on each successful PR. Surfaces what went well, what caused friction, recurring patterns, and proposed improvements. Output is one entry per PR in the improvement-log register; recurring patterns become candidates for pack-rule updates, worker-brief template additions, or new audit gates. Invoke after `/validate-pr` returns and before the next-PR planning step.
derives_from: ../../governance/ai-assistant-workflow-disciplines.md
---

# PR Retrospective

## Project wiring (the parent library's instantiation; adopters substitute their own)

Portable procedure, concrete names. In the parent GRC library this skill runs with:

- Improvement-log register: `.working/improvement-log.md` (the append-only per-PR retrospective register this skill writes; one row per merged PR).
- Worker-hallucination metrics register: the worker-hallucination-metrics ledger in the consuming project's working state (the apply-time worker-correction log consumed as retrospective input).
- Worker-brief template: `.working/worker-brief-template.md` (the worker-side guard-rail carrier that pattern findings may extend).
- Sibling per-PR validation-sweep history register: `.working/validate-pr/history.md` (whose reverse-chronological row convention the improvement-log register mirrors).

- The parent register's concrete table header keeps its original columns (`Date | PR | FR closed | ...`); the generic output format below names that column `Backlog item closed`, and the parent's paired slash-command stub carries the concrete form.

An adopting project maps each bullet to its own records; the procedure below refers to them generically.

## Overview

After each successful merge and `/validate-pr` cycle, conduct a brief retrospective on the PR's process. The retrospective is **light-touch** (one entry per PR, 3-5 sentences) rather than a deep analysis; the value emerges over time as patterns surface across many entries.

The output is the **improvement-log register** (the project wiring above names the parent library's location; adopters relocate to a project-appropriate location). The register is append-only at the row level, ordered by PR number; the step-6 disposition scan appends tokens to earlier rows' Proposed-improvement cells without rewriting their original text. Each row carries the date, PR number, backlog item closed (if any), what-went-well note, friction note, pattern-surfaced note (if any), and proposed improvement (if any).

The skill is **the orchestrator-side process-improvement loop**. It pairs with the worker-side worker-brief template (per [`governance/ai-assistant-workflow-disciplines.md`](../../governance/ai-assistant-workflow-disciplines.md) §1 hallucination-assessment update protocol) and the apply-time-catch tracking in the worker-hallucination metrics register (both named in the project wiring above). Together the three close the per-PR learning loop:

- Worker-brief template catches recurring worker-side failure modes before they reach the orchestrator.
- Apply-time catches log orchestrator-side verifications of worker output.
- PR retrospective surfaces process-level patterns that warrant pack-rule updates, new gates, or worker-brief additions.

## When to Use

- **Mandatory** after every successful PR merge, immediately after `/validate-pr` completes. Runs as part of the post-merge sequence: sync main → delete merged branch → `/validate-pr` → `/retro` → next-PR planning.
- The retrospective is one entry per PR. If a PR cycle produced findings, the entry carries them as observed friction. If a PR cycle was clean, the entry carries the clean-result observation.

**No orchestrator-side skip discretion.** Same discipline as `/validate-pr`: every merged PR gets a `/retro` entry, even when the retrospective conclusion is "nothing new to learn." Zero-content entries (clean PR, no friction, no pattern surfaced) record that fact and serve as the proof-of-discipline (a uniformly-clean register-entry sequence is itself a signal that the workflow is calibrated). Skipping is a policy deviation requiring maintainer authorization.

## Process

The retrospective runs in six short steps.

### 1. Identify the PR and its inputs

Capture:
- PR number, merge commit SHA, backlog item(s) closed (if any).
- The `/validate-pr` findings just returned (0 findings, N findings with categories, or out-of-window observations).
- Any apply-time worker corrections logged in the worker-hallucination metrics register during the PR.
- Recently-shipped PRs in the same cluster (for pattern surfacing).

### 2. Identify what went well

One short observation. Examples:
- "Mechanical alignment to canonical source; no decision needed."
- "Subagent's deep-read caught the multi-surface inconsistency before the maintainer had to."
- "Batching rule applied cleanly; PR #N+1 carried the row without recursion."
- "Pass-1 verification surfaced two real defects the original drafting missed."

If there is genuinely nothing notable, record "Routine; no notable highlight." That's a fine entry.

### 3. Identify friction

One short observation. Examples:
- "Standards-currency gate flagged the template's illustrative `Rev. 4 → Rev. 5` example as superseded; reworded to generic framing."
- "In-flight self-correction prose escaped into the CHANGELOG entry; caught by /validate-pr."
- "A backlog finding double-counted across two triage buckets."
- "Linter gap: Python `ipaddress.is_private` doesn't include CGNAT on Python < 3.13; PR required explicit allowlist update."

If there was genuinely no friction, record "No friction observed." That's also a fine entry.

### 4. Surface patterns (if any)

If the friction in this PR matches a friction seen in a recent PR (≤ 5 PRs prior), record the pattern. Examples:
- "Third consecutive findings-producing /validate-pr (#N → 2; #N+1 → 2; #N+2 → 2). Pattern: meta-PRs that touch fitness-review and validation artefacts introduce subtle multi-surface drift."
- "Recurring acronym-expansion gap in adopter-facing surfaces (PR #N README; PR #M README; PR #P README). Pattern: each new README polish needs first-occurrence expansion checked against the existing convention."

Patterns drive proposed improvements (step 5). A single occurrence is observation; a second occurrence is signal; a third is pattern. When a pattern's recurrence count (across the improvement-log Pattern column) reaches three or more distinct PRs, it AUTO-GRADUATES to a gate-or-convention proposal in step 5: name the mechanical check that would extinguish it (a false-positive-free gate where one exists, else a convention line), because checklist prose demonstrably reduces but does not stop a thrice-recurring class.

### 5. Propose improvement (if any)

If a pattern surfaced, name a concrete improvement. Examples:
- "Add a regression-test fixture exercising CGNAT detection to the PII-in-content linter."
- "Add an acronym-expansion-discipline note to the worker-brief template's DO list."
- "Codify the no-skip-discretion discipline in the validation-sweep-pr-scoped SKILL." (an actual early retrospective outcome in the parent library, recorded retroactively.)
- "Promote the 'genericize counts in prose where the directory is the canonical authority' principle into a pack-rule."

The improvement is a **candidate** for a future PR, not work shipped in this entry. The register tracks the candidate; the next planning cycle picks it up if priority warrants.

If no pattern surfaced, leave the proposed-improvement cell empty.

### 6. Disposition scan (closure discipline)

Proposed improvements accumulate un-codified and their classes recur unless each candidate is eventually closed. After appending the row, run the closure scan:

- **Disposition what this PR landed.** If the just-merged PR codified or routed any earlier row's candidate, append the disposition token to that row's Proposed-improvement cell per the register's disposition convention: `CODIFIED in <carrier>` (the durable home shipped), `ROUTED to <destination>` (a backlog bullet or bundle now carries it), `REJECTED (<reason>)`, `EXPIRED (<date>)`, or `WATCH (fires on <n>th occurrence)` (the sanctioned holding state for conditional candidates). A non-empty cell with no token is pending by definition.
- **Carried-candidates check.** When the just-merged PR performed an authorized protected-file touch, grep the register's pending cells for carrier phrases ("next authorized touch", "row is the carrier", "next CLAUDE.md-touching") and confirm the touch carried them, or record why it did not (the dropped-candidate shape: a carried clause silently missing from the touch it waited for).
- **Rejection and expiry are maintainer calls.** The scan proposes a `REJECTED` or `EXPIRED` disposition for an aged candidate; the maintainer dispositions it. The assistant never silently drops a pending candidate (the same no-drop discipline the sweep skills carry).

## Output format

Append a row to the improvement-log register (named in the project wiring above):

```
| Date | PR | Backlog item closed | What went well | Friction | Pattern (if any) | Proposed improvement |
|---|---|---|---|---|---|---|
| YYYY-MM-DD | #N | item id (if any) | [1-2 sentences] | [1-2 sentences] | [1 sentence, blank if none] | [1 sentence, blank if none] |
```

New rows on top (reverse-chronological, matching the per-PR validation-sweep history register's convention).

The register's preamble describes the column semantics and links to this SKILL.

## Termination

Single-iteration cycle: identify → analyze → record → disposition-scan. One entry per PR.

There is no looping. The slash command `/retro` is fire-and-forget retrospective. The register accumulates entries; pattern recognition emerges from the accumulation, not from any single entry.

## Surfacing entries in chat

**When the retrospective surfaces a Pattern or Proposed-improvement entry, surface it in the chat reply** (per the chat-surfacing discipline shared with `/validate` and `/validate-pr`). The maintainer should see proposed improvements at the moment they're identified, not on their next deep-dive into the working-state archive.

For clean-PR retrospectives (no friction, no pattern, no proposed improvement), one-sentence chat acknowledgement suffices.

## Batching into the next PR (recursion-avoidance)

The improvement-log entry for PR #N appends to the register. The register addition is itself a content change; per the batching rule from [`validation-sweep-pr-scoped`](../validation-sweep-pr-scoped/SKILL.md) and [`validation-sweep`](../validation-sweep/SKILL.md), the register-row commit is **batched into the next PR, whatever its substantive purpose**. The retrospective is conducted immediately after `/validate-pr`; only the register-row commit is deferred.

A retrospective that surfaces a candidate improvement deserving its own PR (e.g., a new audit gate, a new pack-rule, a worker-brief template addition) DOES trigger that PR; but the substance of that PR is the improvement itself, not the register row. The register row is bundled into that improvement PR alongside any other queued register rows.

## Red Flags

- Skipping `/retro` because "this PR was routine; nothing to learn." No-skip discretion applies; record "Routine; no notable highlight" and move on.
- Treating `/retro` as deep analysis. The design is light-touch. Single-paragraph entries are correct.
- Treating the register as an action queue. The register tracks candidates; the next planning cycle picks them up.
- Failing to surface pattern-and-proposed-improvement entries in chat. The chat surface is for maintainer awareness; the register is for archive.
- Conducting `/retro` before `/validate-pr` completes. The retrospective consumes /validate-pr findings as input; running it first misses that input.

## Verification

The retrospective is complete when:

- One entry appended to the improvement-log register for the just-merged PR.
- Pattern and Proposed-improvement entries (if any) surfaced in chat.
- Register entry includes the date, PR number, backlog item closed (if any), and the short observation cells; any disposition tokens from the step-6 scan are appended to the originating rows.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This PR was routine; nothing to retro" | The discipline of writing the entry is itself the value. A uniformly-clean register-entry sequence is a calibration signal. |
| "I'll bundle retros for several PRs together" | The retrospective consumes /validate-pr's findings as input; bundling loses the input freshness. One entry per merge. |
| "The pattern is obvious; no need to record it" | Patterns visible in the moment fade as the session progresses. Recording locks them in for cross-session learning. |
| "I'll surface the pattern when I'm sure it's a pattern" | First occurrence is observation. Second is signal. Third is pattern. Record at each stage; the register's accumulated view shows when the pattern crystallized. |

## See Also

- Sibling skill [`validation-sweep-pr-scoped`](../validation-sweep-pr-scoped/SKILL.md) (slash command `/validate-pr`): consumed-by `/retro` as input.
- Sibling skill [`validation-sweep`](../validation-sweep/SKILL.md) (slash command `/validate`): the broader corpus-wide validation cycle.
- Worker-brief template (project-local; named in the project wiring above): codifies worker-side guard rails that `/retro` patterns may surface as additions.
- Worker-hallucination metrics register (project-local; named in the project wiring above): tracks apply-time worker corrections that `/retro` may surface as pattern candidates.
- Canonical rule [`ai-assistant-workflow-disciplines`](../../governance/ai-assistant-workflow-disciplines.md): the five disciplines this skill operationalizes (specifically: the research-assistant discipline's hallucination-assessment update protocol).
