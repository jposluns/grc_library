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

(No runs yet. The first row is written by the first `/deep-assessment` invocation.)
