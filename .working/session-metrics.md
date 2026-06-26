# Session Metrics

**Version:** 1.0.5\
**Date:** 2026-06-26\
**License:** CC BY-SA 4.0

A per-session ledger of the measurable cost of each working session: subagent
token consumption, wall-clock span, and PR/subagent counts. It exists to give
the maintainer a trend signal on where session cost goes (the bulk is
adversarial-subagent QA), the question that prompted the convention on
2026-06-26.

This file is maintainer working state, exempt from corpus audit gates per the
`.working/` directory exemption. It is informational and is not subject to the
library's metadata-block or audit-conformance conventions (the `Version` /
`Date` header is a courtesy for the change-tracking discipline, not a gated
field). It complements, but is deliberately kept OUT of, the adopter-facing
[`CHANGELOG.md`](../CHANGELOG.md): session cost is maintainer working-state, and
recording an estimated figure in a citable audit artefact would violate the
no-fabrication discipline ([`evidence-grounded-completion`](../dev-security/claude-rules/governance/evidence-grounded-completion.md)).

## The measured-versus-not-instrumented discipline (read before filling a row)

Record ONLY what is genuinely measurable, and label honestly. Never write an
invented exact figure into this ledger.

- **MEASURED (record as exact figures):**
  - **Subagent tokens**: the `subagent_tokens` value reported in each `Agent`
    tool result, summed and broken out by phase (validation sweeps vs PR-build
    research vs other). This is the dominant, precisely-reported cost.
  - **Wall-clock**: `date -u` captured at session start (the `/resume` step) and
    at the session-closing handoff. Record the span. It is ELAPSED time, which
    includes CI waits, fallback timers, async-subagent gaps, and maintainer idle
    time; it is not "effort" and is not comparable session-to-session as a
    workload measure. Label it elapsed.
  - **Counts**: PRs merged this session; subagents dispatched.
- **NOT INSTRUMENTED (state explicitly, do not estimate a number into the table):**
  - **Orchestrator (main-loop) tokens** are not exposed to the assistant
    mid-session (the usage view is user-facing, not artefact-injectable). Record
    `not instrumented` in the table. A rough proportion may appear in prose in
    the Notes cell ("subagent QA was the majority of token weight") but never a
    fabricated exact figure. If a future harness feature emits per-session token
    accounting into a session-readable file, this column can become measured;
    until then it is `not instrumented`.

## How a row gets here (the standing convention)

1. **At `/resume`** (session start): capture `date -u` as the session start, and
   begin accumulating the `subagent_tokens` reported by each `Agent` tool result
   as the session runs (by phase). See the `/resume` command's Session-metrics note.
2. **At the session-closing handoff PR**: write one row for the session into the
   table below (newest on top), batched into the handoff PR's diff alongside the
   other `.working/` close-out refreshes. See the close-out checklist in
   [`.claude/CLAUDE.md`](../.claude/CLAUDE.md) `## Session migration and PR close-out checklist`.

Row schema:

```
| Session (UTC) | Wall-clock (elapsed) | PRs merged | Subagents | Subagent tokens (measured) | Orchestrator tokens | Notes |
```

A worked-example row (illustrative format only, not session data):

```
| 2026-06-26 | ~3h elapsed (incl. CI + idle) | #362, #363 | 4 | ~1.0M (sweeps 766k + PR-validate ~250k) | not instrumented | QA subagents were the majority of token weight |
```

Sessions before this convention existed (2026-06-26) carry no row; rows are not
back-fabricated.

## Sessions

| Session (UTC) | Wall-clock (elapsed) | PRs merged | Subagents | Subagent tokens (measured) | Orchestrator tokens | Notes |
|---|---|---|---|---|---|---|
| 2026-06-26 (resume from handoff #377) | ~1h06m elapsed (20:51 to 21:57 UTC; session-start `date -u` NOT armed at this resume, so the start is taken from the session transcript's first timestamp; incl. CI waits, 60s fallback timers, the ~2-min wind-down timer, async-subagent gaps) | #378 (+ this session-closing handoff #379) | 9 (Sweep 56 A/B/C; FR-167 batch 5 workers W1-W5; `/validate-pr` #378 A) | **2,089,484 across 8 of the 9** (Sweep 56: A 237,274 + B 273,539 + C 272,202 = 783,015; FR-167 batch 5 workers: 252,490 + 260,709 + 261,946 + 265,325 + 265,999 = 1,306,469). The `/validate-pr` #378 Subagent A token count was **not captured** in the retrievable transcript (it fell in a compacted window, the same gap class as the prior #362 row); a pre-compaction working note put it near 130k, but that approximation is not re-verifiable as an exact figure, so it is excluded from the measured sum rather than recorded as precise. | not instrumented | FR-167-batch-5 session (resilience matrix expansion). Sweep 56 (clean) then #378 (matrix Resilience 3 rows to 21, via a 5-worker research-assistant fan-out). The 5 FR-167 research workers were the single largest phase (1.31M measured), the corpus-wide Sweep 56 next (783k); both dwarf the per-PR `/validate-pr`. `AskUserQuestion` errored all session (a known environment flake), so the resume clarifications, the §5.3 decision, and the wind-down decision were surfaced in plain chat; this did not affect the subagent token tally. QA + research subagents were the clear majority of measured token weight; orchestrator main-loop authoring (every matrix cell, the CHANGELOG/handoff prose, the close-out bookkeeping) is not instrumented. | | ~45m elapsed (approx 19:58 to 20:43 UTC; session-start `date -u` NOT armed at this resume, so the start is inferred from the first audit run preceding the #374 CI at 20:08; incl. CI waits, 60s fallback timers, the ~2-min wind-down timer, async-subagent gaps) | #374, #375, #376 (+ this session-closing handoff #377) | 6 (Sweep 55 A/B/C; `/validate-pr` #374 A, #375 A, #376 A) | **1,329,034** (Sweep 55: A 253,835 + B 141,078 + C 256,412 = 651,325; `/validate-pr`: #374 A 239,130 + #375 A 217,156 + #376 A 221,423 = 677,709) | not instrumented | Wind-down-decision-framework session. Sweep 55 (1 in-window finding A-1, fixed in #374) then #375 (codified the `## Wind-down decision framework`) then #376 (its first live application, option B: the two paired-surface guard rails). #376's `/validate-pr` surfaced 1 finding (the worker-brief protocol's hallucination-metrics loop-closure half omitted, itself the paired-surface class #376 codifies), fixed in this handoff. Wall-clock start not armed at `/resume` (a process slip to correct next session); the figure is an inferred bound, not a measured span. QA subagents (the corpus-wide sweep plus 3 per-PR Subagent A dispatches) were the clear majority of measured token weight; orchestrator main-loop authoring (the framework prose, the guard-rail prose, the close-out bookkeeping) is not instrumented. |
| 2026-06-26 (resume from handoff #369) | ~1h11m elapsed (18:12 to 19:23 UTC; incl. CI waits, 60s fallback timers, async-subagent gaps) | #370, #371, #372 (+ this session-closing handoff #373) | 6 (Sweep 54 A/B/C; `/validate-pr` #370 A, #371 A, #372 A) | **1,413,463** (Sweep 54: A 279,132 + B 159,816 + C 279,335 = 718,283; `/validate-pr`: #370 A 266,448 + #371 A 234,573 + #372 A 194,159 = 695,180) | not instrumented | Complete row (tally armed at `/resume`). The gate-49-extension track end-to-end: Sweep 54 (clean) then the 3-PR track (scanner #370 → DD-12 CSF-1.1 migration #371 → gate 54 wiring #372). #372's `/validate-pr` surfaced 1 paired-surface finding (pack version-history row omitted), fixed in this handoff. QA subagents (the corpus-wide sweep plus 3 per-PR Subagent A dispatches) were the clear majority of measured token weight; orchestrator main-loop authoring (the scanner build, the corpus migration, four-surface gate wiring, CHANGELOG/handoff prose) is not instrumented. |
| 2026-06-26 (resume from handoff #365) | ~1h05m elapsed (16:36 to 17:41 UTC; incl. CI waits, 60s fallback timers, async-subagent gaps) | #366, #367, #368 (+ this session-closing handoff #369) | 6 (Sweep 53 A/B/C; `/validate-pr` #366 A, #367 A, #368 A) | **1,559,560** (Sweep 53: A 285,756 + B 286,319 + C 294,430 = 866,505; `/validate-pr`: #366 A 176,120 + #367 A 253,823 + #368 A 263,112 = 693,055) | not instrumented | **First complete row** (tally armed at `/resume` per the #364 convention). Integrity-tooling session: Sweep 53 (1 OOW note routed to DD-12) then 3 integrity gates/aids (D4 Version-Date co-bump, §4.15 §5 currency, §4.14 CHANGELOG-hygiene pre-flight). QA subagents (the corpus-wide sweep plus 3 per-PR Subagent A dispatches) were the clear majority of measured token weight; orchestrator main-loop authoring (gate build, four-surface wiring, CHANGELOG/handoff prose) is not instrumented but was the bulk of the non-subagent work. |
| 2026-06-26 (resume from handoff #361) | not captured (convention added mid-session; no `date -u` armed at this resume) | #362, #363, #364, #365 | 5 (Sweep 52 A/B/C; `/validate-pr` #362 A; `/validate-pr` #364 A) | **partial: at least 1,004,629** (Sweep 52: A 271,038 + B 247,968 + C 247,118 = 766,124; `/validate-pr` #364 A 238,505); `/validate-pr` #362 A return fell in a compacted window and was not captured | not instrumented | **First (partial) row; convention was added mid-session in #364**, so the early-session tally is incomplete (the `/validate-pr` #362 subagent token count was not captured, and no session-start `date -u` was armed). Subagent QA (the two validation sweeps plus per-PR Subagent A dispatches) was the clear majority of token weight. Subsequent sessions arm the tally at `/resume` and record a complete row. |
