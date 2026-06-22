# Improvement Log Register

**Version:** 1.0.3\
**Date:** 2026-06-22\
**License:** CC BY-SA 4.0

Reverse-chronological register of post-merge retrospectives. One row per merged PR (per the `/retro` skill's discipline). New rows on top.

See the [`pr-retrospective` SKILL](../dev-security/claude-rules/skills/pr-retrospective/SKILL.md) for the column semantics and the five-step process. The slash-command entry point is [`/retro`](../.claude/commands/retro.md).

## Purpose

The register accumulates per-PR retrospectives. Each entry is light-touch (one paragraph per cell). The value emerges over time as patterns surface across many entries:

- First occurrence of friction is **observation**.
- Second occurrence is **signal**.
- Third occurrence is **pattern** — and the pattern earns a "Proposed improvement" candidate that the next planning cycle picks up.

The register pairs with the worker-side `worker-brief-template.md` (codifies guard rails against worker-side failures) and the apply-time-catch tracking in [`hallucination-metrics.md`](hallucination-metrics.md) (logs orchestrator-side verifications). Together the three close the per-PR learning loop:

- **Worker brief**: prevents recurring worker-side failures before they reach the orchestrator.
- **Apply-time catches**: log orchestrator-side verifications of worker output.
- **PR retrospective**: surfaces process-level patterns that warrant pack-rule updates, new gates, or worker-brief additions.

## Convention

- New entry per merged PR. The `/validate-pr` cycle completes; then `/retro` appends one row.
- Pattern and Proposed-improvement entries (if present) are surfaced in chat for maintainer awareness; the register is the archive.
- Empty cells in Pattern or Proposed-improvement are valid (most PRs have neither).
- The register's row commit is **batched into the next PR**, whatever its substantive purpose, per the recursion-avoidance rule (see [`/validate-pr` SKILL.md](../dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md) Termination section). The retrospective itself runs immediately after `/validate-pr`; only the row commit waits.

The register is maintainer working state, exempt from corpus audit gates per the `.working/` directory exemption.

## Entries

| Date | PR | FR closed | What went well | Friction | Pattern (if any) | Proposed improvement |
|---|---|---|---|---|---|---|
| 2026-06-22 | #215 | — | The `/validate` Sweep 18 iter 1 dispatched all three subagents in parallel; clean bill confirmed across 29-PR window covering the bulk of the overnight remediation work. Sweep ran cleanly without process detours. | The /validate-pr that ran post-merge on PR #215 surfaced 3 in-window findings (1 error, 2 warnings) on the same multi-surface-refresh shape that PR #190's chat-surfacing discipline was built to catch. The "24 failure-mode classes" arithmetic was technically correct (8+9+7 = 24) but contradicted the canonical SKILL definition; the TODO.md:13 line was missed in the resume-state refresh; the closing-sentence drift between root and detailed mirror is defensible. | Second occurrence of "single PR refreshes parallel surfaces and misses some lines on each" (first was PR #190's findings → chat-surfacing discipline). Signal stage per the three-occurrence progression. | Watch for a third occurrence to confirm the pattern. The shape may warrant a mechanical gate or a checklist addition to the worker-brief template's resume-state-refresh section. No action this turn. |
| 2026-06-22 | #214 | — | Morning-processing PR for the overnight session executed cleanly: design decisions routed to the design-decisions ledger, working-state overnight file reset to stub, PR #213 batched items pulled in, CMMI capability-levels TODO entry added per maintainer direction. Multi-purpose PR but tightly coherent. | The /validate-pr was skipped at the time (went straight to /validate). Backfilled retrospectively in PR #216. The TODO.md:13 line ("synced after PR #213 merge") was not updated when the rest of the resume-state was refreshed — same multi-surface-refresh-miss shape that surfaced in PR #215. | Second occurrence of "single PR refreshes parallel surfaces and misses some lines on each" (also see PR #215 row above). Pinned to PR #215 since that's where the resume-state was substantively refreshed; PR #214 may have also missed it but cannot be confirmed without a baseline. | No action this turn; pattern signal logged. |
| 2026-06-22 | #213 (meta-self) | — | The new `/retro` skill applied to its own introducing PR. The skill design pulled cleanly from the validate-pr SKILL structure (sibling-skill consistency); pattern observation #1 was generated as the proof-of-discipline output. | Drafting a new skill that crosses multiple parallel surfaces (SKILL.md + slash command + register + PAIRS registry + pack README enumeration + CLAUDE.md workflow integration) carried multiple per-surface checklist items; three pre-merge audit failures occurred (link depths, PAIRS missing, pack-README missing row) plus four em-dash style catches caught at apply-time. Each was mechanical; the cluster was not. | First occurrence of "new-skill drafting" friction cluster: each new skill that crosses these N surfaces will have the same per-surface checklist needs. | **Add a `new-skill drafting checklist` section to the worker-brief template's DO list**, enumerating the parallel surfaces (path depth in repository-internal links, pack-README skills-table row, PAIRS registry update if slash-command counterpart exists, language audit pre-flight, slash-command file as sibling). Lives in `.working/worker-brief-template.md`. Candidate for follow-up PR after one or two more new-skill PRs confirm the pattern. |
| 2026-06-22 | #213 | — | First `/retro` skill PR. Skill design pulled cleanly from the validate-pr SKILL's structure (sibling-skill consistency); slash command + register + skill all shipped in one PR (per the maintainer's "always split when in doubt" exception for tightly-coherent work). | No friction. The pack PAIRS registry needed updating to include the new pair; standard gate-44 update. | Single occurrence; nothing to pattern yet. | — |
