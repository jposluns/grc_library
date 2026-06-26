# Session Metrics

**Version:** 1.0.1\
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
| 2026-06-26 (resume from handoff #361) | not captured (convention added mid-session; no `date -u` armed at this resume) | #362, #363, #364, #365 | 5 (Sweep 52 A/B/C; `/validate-pr` #362 A; `/validate-pr` #364 A) | **partial: at least 1,004,629** (Sweep 52: A 271,038 + B 247,968 + C 247,118 = 766,124; `/validate-pr` #364 A 238,505); `/validate-pr` #362 A return fell in a compacted window and was not captured | not instrumented | **First (partial) row; convention was added mid-session in #364**, so the early-session tally is incomplete (the `/validate-pr` #362 subagent token count was not captured, and no session-start `date -u` was armed). Subagent QA (the two validation sweeps plus per-PR Subagent A dispatches) was the clear majority of token weight. Subsequent sessions arm the tally at `/resume` and record a complete row. |
