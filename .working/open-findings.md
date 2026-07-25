# Open Findings Ledger

**Version:** 1.0.0\
**Date:** 2026-07-25\
**License:** CC BY-SA 4.0

Every CONFIRMED defect, from the moment it is confirmed until it is fixed or routed. One row each.

## Why this file exists

A finding that has been read but not acted on is the most expensive state a defect can be in, because
the record shows it was found, so the surface reads as examined. The project already had a rule that a
delivered QA result blocks progress, and that rule has a scope hole this ledger closes: it covered
findings arriving FROM WORKERS and said nothing about findings the orchestrator generates ITSELF while
building. On 2026-07-25 that hole cost two live defects in a file-moving tool, found by the
orchestrator's own probe, rendered as a table row, and walked past in favour of writing a summary
statistic about them. The maintainer caught it.

**So the rule is now source-independent: ANY confirmed defect, from any source, blocks progress.** A
worker delivery, a gate run, an instrument the orchestrator just wrote, a maintainer observation, a
self-caught slip mid-edit. The severity of a defect does not depend on who noticed it.

## The one act this forbids specifically

**Do not write a count, a table, or a comparative statistic about findings before every row has a
recorded disposition.** That is the precise thing that went wrong: three live defects became "3 blind
cases against 27 coverage gaps", and the summary felt like progress while the defects stayed open.
Summarising is not dispositioning.

## Severity and what each blocks

| Severity | Meaning | Blocks |
| --- | --- | --- |
| `error` | wrong behaviour, data loss, a fail-open on a destructive path, a false clean | opening or merging ANY PR, and starting new work |
| `warning` | real defect, bounded blast radius | starting NEW work; an in-flight PR may finish |
| `note` | cosmetic, or correct-but-unclear | nothing; carried to the next PR |

## Disposition values

`FIXED <pr>` (the fix landed), `ROUTED <item>` (a tracked backlog item now owns it, with its tier),
`REFUTED <evidence>` (verified not a defect, with what showed that), `ACCEPTED <rationale>` (a
deliberate, recorded decision to live with it). A row leaves this file only via one of those four; an
empty disposition is what blocks.

## Open

| Found | Severity | Finding | Source | Disposition |
| --- | --- | --- | --- | --- |
| 2026-07-25 | note | `manage-workers.py` and `collect-deliveries.py` each have one `if failures:` self-test reporting branch that the self-test cannot assert from inside itself | `audit-selftest-discriminability.py` | ACCEPTED: structurally untestable in place, and covered EXTERNALLY by the probe's positive control; now classified `INHERENT-EXTERNALLY-COVERED` rather than reported as a fixable defect |
| 2026-07-25 | note | 27 coverage-gap guards across four tools (`manage-workers` 9, `collect-deliveries` 4, `audit-worker-saturation` 8, `audit-inbox-drops` 6): guards no self-test case reaches, chiefly CLI dispatch and error paths needing a live external process | `audit-selftest-discriminability.py` | ROUTED: these are coverage gaps rather than blind cases, so the fix is a case or a recorded out-of-scope decision per guard; queued behind the error and warning work |

## Closed today

| Found | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 2026-07-25 | error | `collect-deliveries.py:81` empty-part guard in `split_name` was BLIND: the cases covered a non-tray name and a wrong extension but never an empty part, so `split_name("__x.md")` returned `("", "x")` and a caller could use an empty worker id, which the saturation tool's phantom-pending retirement depends on being well-formed | FIXED this PR; two cases added and the guard's removal now FAILS the self-test, verified |
| 2026-07-25 | error | `audit-worker-saturation.py` reported SATURATED while a worker sat idle, because the delivery tray added a third location its phantom-pending retirement did not scan, and the tray's composed filename also needed splitting | FIXED this PR; two fixture cases added, both mutation-proved load-bearing with controls bracketing the run |
| 2026-07-25 | error | The probe voided itself on any tool importing a sibling module, because it wrote the mutant into a temp SUBDIRECTORY | FIXED this PR; mutants are sibling files now, caught by the probe's own negative control |
| 2026-07-25 | error | The probe reported a FALSE CLEAN (22 detected, 0 findings) after the verdict strings gained a suffix while the filter still tested exact equality | FIXED this PR; filter matches by prefix, caught only because the number contradicted an earlier run |
