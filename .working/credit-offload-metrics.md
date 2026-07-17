# Credit-offload metrics: worker productivity and estimated orchestrator credits conserved

**Version:** 1.0.9\
**Date:** 2026-07-17\
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
| 2026-07-16 | validate-pr-980 | qa | validate-pr | worker-20260716-b (Opus 4.8) | ~72K | #981 | ~70-85K; caught 3 stale-`~1.37M` secondary surfaces (mid-PR figure-drift), fixed in #981. worker-b's 8th delivery. |
| 2026-07-16 | ref-acquire-edpb-softlaw | research | reference-acquisition | worker-20260716-a (Opus 4.8) | not captured | ref PR #85 | 7 EDPB/WP29 GDPR soft-law PDFs acquired; 4 new ingested (E-03/E-04/E-05/WP260), 3 dups skipped. Package MANIFEST carried no token figure. |
| 2026-07-16 | ref-acquire-brazil-anpd | research | reference-acquisition | worker-20260716-a (Opus 4.8) | not captured | ref PR #86 | 3 ANPD resolutions ingested (19/2024, 2/2022, 1/2021) + 1 egress-blocked (32/2026). No token figure. |
| 2026-07-16 | ref-acquire-latam-crypto-quebec | research | reference-acquisition | worker-20260716-a (Opus 4.8) | not captured | ref PR #86 | Argentina Decreto 1558/2001 + Quebec anonymization regulation ingested + 2 egress-blocked (NYDFS, Colombia). No token figure. |
| 2026-07-16 | canada-2226-currency-classify | qa | verify | worker-20260716-a (Opus 4.8) | ~85K | ref PR #87 | classified the 27 fresh §2.22 uploads (13 dup-current / 2 dup-newer / 12 new); drove the ref-reconcile. worker-a elevated window (~3rd QA-kind, re-verified at source). |
| 2026-07-16 | deep-assessment-r4-probe | qa | deep-assessment | worker-20260716-b (Opus 4.8) | ~170K | #983 (register) + ref #87 (F-P2-1 fix) | first OFFLOADED `/deep-assessment`; partial phases 1/2/4a/aids; found F-P2-1 (ref gate-red) + OBS-1; confirmed corpus green 69/69. |
| 2026-07-16 | canada-new-items-ingest-prep | research | research | worker-20260716-a (Opus 4.8) | ~140K | ref PR #87 | extracted + draft-catalogued the 12 NEW items; corrected the AI Register record count to 412; flagged the AI Strategy fresh capture as incomplete. |
| 2026-07-16 | validate-pr-982 | qa | validate-pr | worker-20260716-b (Opus 4.8) | ~70K | #983 | SHIP; re-verified §7121 at source; one NOTE on 2 frozen #976 §7120-phasing records (corrected in #983). |
| 2026-07-16 | sweep-109-validate-2 | qa | validate | worker-20260716-b (Opus 4.8) | ~207K (gross) | this close-out PR (#985) | loop-break Sweep 109 over #969..#984; worker subagents A ~108K / B ~51K / C ~48K (worker total ~310-340K incl. its own orchestration). FIRST offloaded pass of the 2026-07-16c session, consumed under new-worker ELEVATED QA. **NET conserved is well below gross this delivery:** the orchestrator's elevated-QA validation (adversarial false-negative auditor ~216K + mechanical re-derivation) is a one-time trust-establishment cost that converts to near-gross saving on worker-b's subsequent routine-trust deliveries this session. |
| 2026-07-16 | validate-pr-985 | qa | validate-pr | worker-20260716-a (Opus 4.8) | ~70K | #986 | worker-a's FIRST QA-kind delivery this fresh session -> ELEVATED (delivery-1, PASS). Mechanical facts re-derived; Note-1 re-verified TRUE at source (the "as adjusted" clause my own Sweep-109 auditor missed). |
| 2026-07-16 | validate-pr-986 | qa | validate-pr | worker-20260716-a (Opus 4.8) | ~60K | #987 | worker-a elevated delivery-2. Surfaced the APO14 "Managed AI"->"Managed Data" title substitution (fixed #987). |
| 2026-07-16 | validate-pr-987 | qa | validate-pr | worker-20260716-a (Opus 4.8) | ~105K | #988 | worker-a elevated delivery-3. **The elevated re-derivation caught a CONFIRMED MISS** (out-of-window N1 32/25 vs true 35/28; title-case-only pattern); window RESET + escalated, N1 routed to §1.16. |
| 2026-07-16 | validate-pr-988 | qa | validate-pr | worker-20260716-a (Opus 4.8) | ~115K | #989 | worker-a's 1st delivery post-reset (PASS 1 of 2-3). Caught a real orchestrator-introduced W1 defect (offload independence). |
| 2026-07-16 | validate-pr-989 | qa | validate-pr | worker-20260716-b (Opus 4.8) | ~118K | #990 | worker-b's 3rd clean elevated pass -> **GRADUATES to routine trust** this session. |
| 2026-07-17 | validate-pr-990 | qa | validate-pr | worker-20260716-a (Opus 4.8) | ~118K | #991 | worker-a's 2nd delivery post-reset (PASS 2 of 2-3). SHIP 0/0/0. Local mirror lagged two PRs at claim (resync-resolved). |
| 2026-07-17 | sweep-110-validate | qa | validate | worker-20260716-a (Opus 4.8) | ~359K (gross) | this close-out PR (#992) | loop-break Sweep 110 over #985..#991; worker subagents A ~103K / B ~79K / C ~66K + ~110K main. **worker-a's 1st clean elevated pass THIS session** (session-scoped window; the #992 "3rd clean -> re-graduates to routine" wording was a cross-session miscount, corrected #993, worker-a stays ELEVATED 1-of-2-to-3). Consumed under ELEVATED QA (proof-of-run genuine; base #984 `28d4146b` + baseline 69/69 + pre-flight 421/33/11 + parity 69 + counts 13/23/14/18 all EXACT-MATCH; every finding re-verified at source). Found S110-1 (new CSF-2.0 `ID.AM-3`->`ID.AM-02` mis-cite, routed §1.17(d)) + S110-2 (in-window #986 CHANGELOG mis-quote, fixed) + S110-3 (known N2). Order was stuck at `status:queued` (the footgun); orchestrator flipped to `pending` so a live worker could claim it. |
| 2026-07-17 | validate-pr-992 | qa | validate-pr | worker-20260716-b (Opus 4.8) | ~132K | this close-out PR (#993) | worker-b's 1st QA-kind delivery this session -> ELEVATED window. SHIP + one WARNING (the worker-a trust-tier miscount, = the orchestrator's OWN self-catch, independently corroborated with CLAUDE.md line cites). Consumed under full ELEVATED QA incl. a delivery-1 false-negative auditor (orchestrator-run, ~255K subagent tokens, NOT offloaded) that found NO additional substantive miss. **NET-NEGATIVE this delivery** (~132K conserved vs ~255K one-time auditor cost); the auditor is a worker-b trust-establishment cost that converts to near-gross saving on its 2nd/3rd routine deliveries this session. Calibration note (retro #992): a small self-authored bookkeeping PR may be cheaper to self-`/validate-pr` than to offload+auditor. |
| 2026-07-17 | validate-pr-993 | qa | validate-pr | worker-20260716-a (Opus 4.8) | ~92K | this close-out PR (#994) | worker-a's delivery 2 of the elevated window this session (steps 1-3, NO separate auditor). SHIP 0/0/0. **NET-POSITIVE this delivery** (~92K conserved, no auditor overhead since delivery 2): the delivery-1 auditor cost is one-time, so worker-a's 2nd/3rd deliveries convert to near-gross saving as designed. Re-ran `check-portability.sh` + adversarial false-negative hunt; one FYI (relative-scope) routed §3.90. |
| 2026-07-17 | validate-pr-994 | qa | validate-pr | worker-20260716-b (Opus 4.8) | ~120K | this close-out PR (#995) | worker-b delivery 2 of the elevated window this session (steps 1-3, no separate auditor). SHIP + one in-window NOTE (the `lint_common.py` docstring lag when 3 dirs were added to `DEFAULT_EXEMPT_DIRS`; fixed #995). **NET-POSITIVE** (~120K conserved, no auditor overhead on delivery 2). Adversarial payload-accumulation + dangling-ref checks clean. worker-b now 2-of-2-to-3 (its next clean delivery re-graduates it to routine). |
| 2026-07-17 | validate-pr-995 | qa | validate-pr | worker-20260716-b (Opus 4.8) | ~150K | this close-out PR (#996) | worker-b's delivery 3 of the elevated window this session (steps 1-3, no separate auditor, no red flag). SHIP 0/0/0. Consumed under elevated QA: proof-of-run genuine (run_all_audits 70/70 + lint-sibling-placeholders rc0 + unittest 7/7 + check-changelog-length OK + `path:line`); mechanical facts independently re-derived (count 70, §1.19.4 rotation, README/spec versions) all match orchestrator authorship; enumerated the gate-70 payload-bypass vectors (extra file / dotfile / nested dir / symlink) as all caught. **NET-POSITIVE** (~150K conserved, no auditor overhead on delivery 3). **worker-b clears the 2-to-3 floor -> ROUTINE trust for its subsequent QA-kind deliveries this session.** |

**Other deliveries in the results plane (delivery-session attribution and consume status vary; NOT
counted in the session roll-up below to avoid over-attribution):** `etsi-en304223-option3-apply-draft`
(~114K), `gr-gap-1-gate-draft` (~161K), `matrix-fit-full-pass` (~153K), `claim-fit-tier-a-pass` (~46K),
`screen-publications-pending` (~55K). These are delivered-but-not-yet-consumed or from an earlier
window; they are added to the roll-up when consumed this session. (The three `ref-acquire-*` orders,
formerly listed here, are now consumed and carried as proper rows above; their token spend was not
captured.)

## Per-session roll-up

| Session (resume) | Offloaded passes counted | Est. orchestrator credits conserved (midpointed, this-session-consumed set) | Notes |
| --- | --- | --- | --- |
| 2026-07-16 (resumed from #968) | 17 with figures (+ 4 not captured) | **~1.98M tokens (est.)** | Conservative (worker-spend proxy). The Sweep-108 self-run comparable alone was ~609K vs ~237K worker, so the true conserved is higher. The +~465K over the prior ~1.51M is the Canada §2.22 pipeline consumed this stretch (currency-classify ~85K + r4-probe ~170K + ingest-prep ~140K + validate-pr-982 ~70K). Excludes 5 delivered-but-unconsumed passes (etsi/gr-gap/matrix-fit-full/claim-fit/screen-pub, ~529K more if/when consumed) and the 4 not-captured research deliveries (canada-ca-reference-breadth + the 3 ref-acquire orders). Orchestrator main-loop tokens remain `not instrumented`. |
| 2026-07-16c (resumed from #984) | 7 with figures | **~793K tokens (est., gross)** | Sweep 109 (~207K) + six offloaded `/validate-pr` deliveries (985 ~70K / 986 ~60K / 987 ~105K / 988 ~115K / 989 ~118K / 990 ~118K = ~586K). **NET is materially below gross this session** because BOTH workers were re-establishing trust in this fresh session, drawing the full new-worker ELEVATED QA (worker-b's Sweep-109 adversarial false-negative auditor ~216K + per-delivery mechanical re-derivation), AND worker-a's elevated window RESET at validate-pr-987 (a confirmed miss) re-incurred the elevated cost on validate-pr-988/990. Worker-b graduated to routine trust at validate-pr-989; worker-a re-establishing (2 of 2-3). Orchestrator main-loop tokens remain `not instrumented`. |
| 2026-07-17 (resumed from #991) | 5 with figures (ongoing) | **~853K tokens (est., gross)** | Sweep 110 loop-break `/validate` (~359K) + validate-pr-992 (~132K) + validate-pr-993 (~92K) + validate-pr-994 (~120K) + validate-pr-995 (~150K). **worker-b graduated to routine trust at validate-pr-995 (its 3rd clean elevated pass this session); worker-a stays ELEVATED (1 of 2-to-3).** **NET is materially below gross this session:** both workers are re-establishing trust in this fresh session (session-scoped window), so validate-pr-992's ~132K conserved was more than offset by its ~255K one-time delivery-1 false-negative auditor (orchestrator-run); the net saving converts positive as workers reach routine trust (2nd/3rd clean elevated pass) this session. Sweep 110 served by worker-a and consumed under ELEVATED QA (worker-a's 1st clean elevated pass this session). worker-a stays **ELEVATED (1 of 2-to-3)** this session (the #992 "re-graduated" wording was a cross-session miscount, corrected #993; the elevated window resets each session), so its subsequent deliveries this session still draw elevated-QA verification cost until it clears the floor. Roll-up refreshes as more offloads are consumed this session; the session-closing handoff folds the final figure into `session-metrics.md`. Orchestrator main-loop tokens remain `not instrumented`. |
