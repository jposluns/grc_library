# Improvement Log Register

**Version:** 1.0.0\
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
| 2026-06-22 | #213 | — | First `/retro` skill PR. Skill design pulled cleanly from the validate-pr SKILL's structure (sibling-skill consistency); slash command + register + skill all shipped in one PR (per the maintainer's "always split when in doubt" exception for tightly-coherent work). | No friction. The pack PAIRS registry needed updating to include the new pair; standard gate-44 update. | Single occurrence; nothing to pattern yet. | — |
