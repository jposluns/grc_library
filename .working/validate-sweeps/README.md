# `.working/validate-sweeps/` — Per-Iteration Records

This subdirectory holds per-iteration records produced by the `/validate` slash command (underlying skill: `validation-sweep`). Each file is a frozen-state snapshot of one iteration of one sweep, written at the end of step 9 of the skill's process.

## File naming

`YYYY-MM-DD-sweepN-iterM.md`

- `YYYY-MM-DD` — calendar date of the iteration
- `sweepN` — sweep ordinal, continues the numbering in [`governance/register-sweep-history.md`](../../governance/register-sweep-history.md). Sweep 1 was the first invocation ever; the current sweep number is whatever the register's most recent entry shows (or that entry's next number if this iteration starts a new sweep)
- `iterM` — iteration within the sweep; the convergence-delta termination protocol can produce multiple iterations per sweep

Examples: `2026-06-21-sweep9-iter1.md`, `2026-06-21-sweep9-iter2.md`, `2026-06-22-sweep10-iter1.md`.

## File structure

Each file uses six top-level H2 sections in this order:

1. `## Trigger & state snapshot` — what triggered this iteration; library/pack version/gate-count/skill-count/rule-count at HEAD; iteration ordinal within the sweep
2. `## Subagent A — Recent-PR deep review` — verbatim return from subagent A
3. `## Subagent B — Corpus-wide stale-reference sweep` — verbatim return from subagent B
4. `## Subagent C — Audit-programme integrity reviewer` — verbatim return from subagent C
5. `## Orchestrator synthesis` — in-window classification, severity adjudication, dedupe choices, debate outcomes, actions decided
6. `## Resulting PR` — link to the close-out PR, or `none — zero findings`

The register entry in `governance/register-sweep-history.md` is the cumulative summary; this file is the detail.

## Relationship to the register

- Zero-finding iterations write to `.working/validate-sweeps/` but do NOT create a register entry (the convention is "zero-finding sweeps leave no trace in the register"). The per-iteration record here is the only persistent trace.
- Iterations with findings write to BOTH `.working/validate-sweeps/` (detail) and the register (summary). The two are complementary; neither replaces the other.

## Audit-gate exemption

`.working/` is in `tools/lint_common.py` `DEFAULT_EXEMPT_DIRS`. Files here are not scanned by the corpus audit gates: their `path:line` references may become stale as the corpus evolves; that staleness is expected and does not fail CI.

## Convention version

Established 2026-06-21 in PR #115 (`/validate` rename + per-run records). Prior sweeps (Sweeps 1-9) predate this convention and have only register entries, no per-iteration files here.
