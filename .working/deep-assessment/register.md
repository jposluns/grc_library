# Deep-assessment run register

Durable phase-state register for the `/deep-assessment` skill (the rare-cadence
whole-project deep assessment). One row per run. A row with Status `in-progress` is a
standing instruction to a future session: the run is not finished, and a bare
`/deep-assessment` invocation resumes it at the next incomplete phase. Rows close only
on explicit maintainer sign-off (recorded in the Sign-off column), never on an empty
finding set. Per-run detail lives in this directory as dated files `<YYYY-MM-DD-rN>.md`.

Phase key: 1 run-state and inventory; 2 mechanical baseline; 3 semantic instruments;
4 audit-programme audit; 5 ground-truth sampling; 6 adoptability, pipeline, ledgers;
7 routing; 8 record and sign-off. Per-phase status values: `pending` / `in-progress` /
`complete` / `deferred(<reason>)`.

| Run | Opened (UTC) | Baseline SHA | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | Status | Findings routed | Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 | 2026-07-10 | `4f043f6` (#753) | complete | complete | complete | complete | complete | complete | complete | complete | signed-off | 4 fixed in-window (F1/F3/F6/F12) + 13 routed (R1-R13) | maintainer 2026-07-10: signed off on the finding set; authorized actioning every actionable routed item overnight (R6 source-not-held + R8b GitHub-setting excepted), incl. protected R7 + generator R2 |

Per-run detail: [`2026-07-10-r1.md`](2026-07-10-r1.md). Run r1 is the first-ever `/deep-assessment`, maintainer-invoked 2026-07-10 (attended-autonomous, VM). Phases 1-2 (run-state/inventory + mechanical baseline) complete: full clone, all three repos present, lease held by this session; live inventory 67 gates / 14 commands / 21 skills / 13 governance rules / 15 advisory tools; green-at `4f043f6` = 67/67 with all sibling and generator checks clean. Phases 3-7 complete in the 2026-07-10 overnight run: the six semantic instruments ran as parallel judges (full-qa, fitness, matrix-fit, claim-fit, reference-audit, guardrails; `/validate` of record = this session's Sweep 93; `/screen-publications` omitted per finding F18); the audit-programme audit (blind-spot map clean, mutation probe 8/0/0, dead-gate/parity all reconciled to 67); ground-truth sampling (8 Tier-A claims all clean, incl. the FR-120-class); adoptability/pipeline/ledger review (branch protection confirmed via ruleset; full-history secret scan clean; one ledger-miss escape = F1). **21 findings + 27 reference-breadth recs, 0 error, 7 warning, rest note.** Disposition: 4 clear-mechanical fixes shipped in-window (F1 jurisdiction count, F3 tooling SyntaxWarning, F6 compliance link-hygiene, F12 EU AI Act Chapter-V locator); 13 items routed to TODO (R1-R13). Phase 8 holds: the run stays **in-progress pending explicit maintainer sign-off** (an empty set would still be presented for sign-off; a non-empty one certainly is).
