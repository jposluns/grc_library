# Credit-offload metrics: worker productivity and estimated orchestrator credits conserved

**Version:** 1.0.0\
**Date:** 2026-07-16\
**License:** CC BY-SA 4.0

Running tab of what the credit-offload workers have done and, per session, the **estimated
orchestrator credits conserved** by offloading passes to them. Maintainer-directed 2026-07-16
(chosen shape: this ledger plus a short chat surface at each major activity; metric = estimated
orchestrator credits conserved; no per-DONE-entry line).

## The metric (and its honest caveats)

**Estimated orchestrator credits conserved** = the worker's own best-effort token-spend estimate
for an offloaded pass, treated as a conservative proxy for what the orchestrator would have spent
had it self-run that pass. Read it with three caveats, always:

1. **Estimate, not instrumented.** A worker cannot read an exact in-session token count, so every
   figure here is the worker's best-effort estimate (usually a subagent-output-budget sum), not a
   measured value. Ranges are midpointed for the roll-up.
2. **Shifts cost across accounts; does not reduce total spend.** Credit-offload moves token cost
   from the orchestrator's account to a worker account. The headline "conserved" figure is what the
   ORCHESTRATOR did not spend; the total tokens spent across all accounts is not reduced (and the
   orchestrator still pays a small consume/verify cost per delivery, plus the pre-push verifier,
   which stay orchestrator-side).
3. **Conservative proxy.** Where a direct self-run comparable exists it can exceed the worker
   spend (the Sweep-108 corpus `/validate` conserved about 609K, since a self-run cost about 609K
   at Sweep 107, while the worker ran it in about 237K); using worker-spend as the conserved figure
   therefore UNDER-states the saving for such passes. The direct comparable, where known, is in Notes.

The net saving is real only when the other accounts have spare capacity.

## Convention (how this is maintained and surfaced)

- **Append one row per offloaded delivery** when the orchestrator consumes it (or at delivery).
- **Surface a short chat tally (a couple of lines) at each major activity**, a worker delivering a
  result and a PR finishing, of the form: "Workers this session (est., not instrumented): N passes,
  est. ~Xk orchestrator tokens conserved" plus any standout. This is the running-tab surface the
  maintainer reads; the ledger is the durable record. (No per-DONE-entry line, by maintainer choice
  2026-07-16.)
- **Per-session roll-up** at the bottom, refreshed as rows are added; the session-closing handoff
  can fold the roll-up figure into the [`session-metrics.md`](session-metrics.md) row.
- Figures come from the worker result's proof-of-run/token-spend section; where a worker did not
  record a figure, the row says `not captured` (honest gap, not zero).

## Running ledger

| Date (UTC) | Order | Kind | Command | Worker (model) | Est. worker spend (= est. orchestrator credits conserved) | Consumed/applied in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-16 | sweep-108-validate | qa | validate | worker-20260716-a (Opus 4.8) | ~237K | #971 | corpus-wide `/validate`; subagents A ~81K / B ~56K / C ~101K. **Direct self-run comparable ~609K** (Sweep 107), so true conserved is nearer ~609K. |
| 2026-07-16 | validate-pr-969 | qa | validate-pr | worker-20260716-a (Opus 4.8) | ~54K | #970 | caught a real orchestrator SHA-typo in the order (offload independence). |
| 2026-07-16 | canada-annexes-source-verification | research | verify | worker-20260716-a (Opus 4.8) | ~179K | #973 | AI annex ~99K + privacy annex ~80K; drove the Quebec Law 25 penalty/PIA corrections. |
| 2026-07-16 | canada-ca-reference-breadth | research | reference-audit | worker-20260716-a (Opus 4.8) | not captured | deferred (§2.22, egress) | proof-of-run carried no token figure. |
| 2026-07-16 | canada-matrix-fit | research | matrix-fit | worker-20260716-a (Opus 4.8) | ~222K | deferred (§2.22, egress) | ~63K + ~159K. |
| 2026-07-16 | ccpa-regs-2026-alignment | qa | reference-audit | worker-20260716-a (Opus 4.8) | ~133K | #976-#979 | ~47K + ~86K; drove the whole CCPA §2.23 regs-alignment. |
| 2026-07-16 | validate-pr-973 | qa | validate-pr | worker-20260716-b (Opus 4.8) | ~70K | #975 | first QA delivery; full elevated QA. |
| 2026-07-16 | validate-pr-974 | qa | validate-pr | worker-20260716-b (Opus 4.8) | ~90K | #975 | caught the F1 design-doc overclaim (offload independence). |
| 2026-07-16 | validate-pr-975 | qa | validate-pr | worker-20260716-b (Opus 4.8) | ~112K | #976 | |
| 2026-07-16 | validate-pr-976 | qa | validate-pr | worker-20260716-b (Opus 4.8) | ~120K | #977 | |
| 2026-07-16 | validate-pr-977 | qa | validate-pr | worker-20260716-b (Opus 4.8) | ~72K | #978 | |
| 2026-07-16 | validate-pr-978 | qa | validate-pr | worker-20260716-b (Opus 4.8) | ~82K | #979 | |
| 2026-07-16 | validate-pr-979 | qa | validate-pr | worker-20260716-b (Opus 4.8) | ~72K | #980 | first delivery under the aligned `## Token spend` format; worker-b cumulative self-estimate ~550-700K in + 70-90K out across its 7 orders (cross-checks this ledger). |

**Other deliveries in the results plane (delivery-session attribution and consume status vary; NOT
counted in the session roll-up below to avoid over-attribution):** `etsi-en304223-option3-apply-draft`
(~114K), `gr-gap-1-gate-draft` (~161K), `matrix-fit-full-pass` (~153K), `claim-fit-tier-a-pass` (~46K),
`screen-publications-pending` (~55K), `ref-acquire-{brazil-anpd,edpb-softlaw,latam-crypto-quebec}` (not
captured). These are delivered-but-not-yet-consumed or from an earlier window; they are added to the
roll-up when consumed this session.

## Per-session roll-up

| Session (resume) | Offloaded passes counted | Est. orchestrator credits conserved (midpointed, this-session-consumed set) | Notes |
| --- | --- | --- | --- |
| 2026-07-16 (resumed from #968) | 12 with figures (+ 1 not captured) | **~1.44M tokens (est.)** | Conservative (worker-spend proxy). The Sweep-108 self-run comparable alone was ~609K vs ~237K worker, so the true conserved is higher. Excludes 5 delivered-but-unconsumed passes (etsi/gr-gap/matrix-fit-full/claim-fit/screen-pub, ~529K more if/when consumed) and the 4 not-captured research deliveries. Orchestrator main-loop tokens remain `not instrumented`. |
