# Open Findings Ledger

**Version:** 1.1.0\
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
| 2026-07-25 | warning | Gate 50 Check 1 is satisfied by row PRESENCE, so #1176's honest `DISPATCHED, RESULT PENDING` row satisfies it and the parity gate reads GREEN while that PR's `/validate-pr` has never run; an undelivered order can hold a PR's QA open indefinitely with the gate green throughout | Sweep 122 Part 3, and the maintainer's directive at the same resume | ROUTED: convention half FIXED in #1178 (CLAUDE.md close-out item 3 and pack `session-lifecycle.md` section 5); the mechanical half is TODO 3.120, a third `pending` state in Check 1, which cannot land green until #1176's own QA returns, so it is sequenced behind that |
| 2026-07-25 | warning | #1176 merged UNVALIDATED: 22 files, 813 insertions, six backlog-item closures, its `/validate-pr` order dispatched but never claimed, and the session then closed | maintainer, 2026-07-25 | ROUTED TODO 3.122 (H severity), which closes only when the result has RETURNED and every finding is dispositioned, never when the order is merely re-dispatched. Still queued and unclaimed: both codex workers declined on a documented independence conflict and both opus workers are chain-adjacent, so the fleet cannot serve it; a fresh worker is requested, and per the rule #1178 adds the orchestrator runs it directly rather than closing over it |
| 2026-07-25 | warning | `audit-selftest-discriminability.py` divided a MEASURED numerator by an ATTEMPTED denominator: its summary said `73 NOT-DETECTED across 21 tool(s)` when 10 of those 21 are VOID and contribute no figures, so the line read as full coverage of 21 tools when only 11 were measured and the other 10 carry an UNKNOWN exposure | Sweep 122 note, re-measured at source by the orchestrator | FIXED in #1178: the summary now reports measured-of-probed, names the 10 void tools, and states the total understates the truth by an unmeasured amount; self-test 17/17 and the re-run reproduced the worker's void list exactly |
| 2026-07-25 | note | The handoff's per-tool discriminability figures `9/4/14/6 (total 33)` attribute a 6 to `audit-selftest-discriminability.py`, which appears ZERO times in its own report; the three real figures sum to 27, and the two tools reporting 6 are `audit-delivery-status.py` and `audit-inbox-drops.py` | Sweep 122 note, re-measured at source | FIXED in #1178 in the live carrier (the handoff soft-spot list). The frozen `.working` records that carry the old figure (the #1175 per-PR file, its history row, the detailed CHANGELOG entry) are left as written, because a frozen record states what was believed at write time and retro-editing it is the anti-pattern; the correction is recorded here and in the Sweep 122 row |
| 2026-07-25 | note | A sweep order that directs the worker to remove `origin` from its clone makes the pre-push guard's D-series unrunnable (all eight fail rc=2 on merge-base resolution), so a handoff's pre-push-green claim is not re-derivable and comes back VOID rather than confirmed or contradicted | Sweep 122 Part 5 | ROUTED to TODO 3.121: future sweep orders either keep `origin` and give the version-monotonicity gate its own exclusion, or create a local `origin/main` ref at the base SHA. Not fixed here because changing what the guard measures is a decision, not a workaround |
| 2026-07-25 | warning | `manage-workers.py` reported NOT SUBMITTED for the `mailz` pane (payload still in the composer after 8s) while the pane in fact showed an empty composer and a completed reply, so the verdict was WRONG rather than merely the known UNVERIFIED indeterminacy | orchestrator, observed this session while nudging codex | ROUTED: folds into queue item 5 (`submit_state` indeterminacy), widening it from "returns UNVERIFIED when the composer is not in the captured tail" to "can also return a positively WRONG NOT-SUBMITTED". The pane capture is retained above as the reality fixture |
| 2026-07-25 | error | `.working/validate-sweeps/history.md` carries FIVE fused ledger rows and `matrix-fit/history.md` one, all live on `main`; four of the fusions DROPPED a sweep's row entirely (Sweeps 88, 86, 27, and one unidentified), so QA audit trail has been silently lost, and TODO 3.73 records only #915 as the class's first escape | worker `opus-20260725T121943Z-78ff` inbox issue drop, `design-3.73-ledger-row-gate` | ROUTED TODO 3.73, whose scope is corrected and sequenced in #1178 from the maintainer's repair-then-gate decision: reconstruct the four dropped rows from git history and the per-run detail files, repair all six fusions, then land the detector green against a clean tree with no grandfathered exemption set. The repair is the next PR |
| 2026-07-25 | error | `credit-offload-queue.py list-workers` returned an EMPTY registry while the file-drop plane held up to eight live workers, AND `/resume` step 3 plus the CLAUDE.md mandatory-offload gate both directed the orchestrator to that tool, so a resume would read zero workers and license self-running every offloadable pass | orchestrator, 2026-07-25 | FIXED both halves: the tool now fails loud naming the other plane, its count and the authoritative command, distinguishing an absent root from a present-but-empty one (self-test 66/66, pushed); and both instruction surfaces are repointed, each edit asserted to have landed |
| 2026-07-25 | error | The worker-id exclusion control FAILED OPEN: a transposed id named a worker present on neither plane and excluded NOBODY, silently, which is how a change merged with both independent adversarial lenses served by the same worker | maintainer alert 2026-07-25-a NOTE 2 | FIXED: dispatch now refuses when `not_worker` names an id the exchange has never seen, with an override for a genuinely not-yet-started worker; verified by replaying the alert's ACTUAL transposed id (refused) against a real id (dispatched) |
| 2026-07-25 | warning | No release path existed, so a worker that must not serve an order it holds had to deliver a NOT-RUN notice, leaving the order consumed-but-unserved; it cost two cycles the same day | maintainer alert 2026-07-24-c | FIXED: `release` added, refusing a non-holder, a missing reason and a name collision; both worker contracts updated to prefer RELEASE over NOT-RUN when the order is fine but the worker is the wrong party |
| 2026-07-25 | note | I called a helper `_clear_held_order` that does not exist anywhere in the tool, while writing the release command | orchestrator, self-caught | FIXED before any run: verified zero definitions, found that this plane derives holding from file LOCATION with no marker at all, removed the call and documented the property instead of inventing the function |
| 2026-07-25 | warning | The git-scratch queue tool had NEITHER exclusion key in its write-field list, so a rewrite SILENTLY DROPPED `not_worker` / `not_author_of` and independence was unenforced while appearing enforced | `triage-tray-34` rank 2 | FIXED: both keys added to the preserved-field list, with the revert mutation-proved DETECTED under bracketing controls; verified not to have bitten beforehand, since `reconcile-queue` uses a different write path |
| 2026-07-25 | warning | Gate 69's two blind spots remain live (part (c) of the never-recycle work, and the surviving F3 of the #1152 pre-push verify) | `triage-tray-34` ranks 4 and 20, `draft-3110c-gate69-blindspots` | ROUTED: this is TODO 3.110 part (c), already carried as a separate item with its candidate delivered and unapplied |
| 2026-07-25 | warning | Three fresh-reader findings against the adopter documentation verified still live at HEAD | `codex-fresh-reader-corpus-review` via `triage-tray-34` rank 29 | ROUTED: adopter-facing prose, queued behind the safety and correctness work; the delivery is retained in the tray until applied |
| 2026-07-25 | note | `manage-workers.py` and `collect-deliveries.py` each have one `if failures:` self-test reporting branch that the self-test cannot assert from inside itself | `audit-selftest-discriminability.py` | ACCEPTED: structurally untestable in place, and covered EXTERNALLY by the probe's positive control; now classified `INHERENT-EXTERNALLY-COVERED` rather than reported as a fixable defect |
| 2026-07-25 | note | 27 coverage-gap guards across four tools (`manage-workers` 9, `collect-deliveries` 4, `audit-worker-saturation` 8, `audit-inbox-drops` 6): guards no self-test case reaches, chiefly CLI dispatch and error paths needing a live external process | `audit-selftest-discriminability.py` | ROUTED: these are coverage gaps rather than blind cases, so the fix is a case or a recorded out-of-scope decision per guard; queued behind the error and warning work |

## Closed today

| Found | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 2026-07-25 | warning | `collect-deliveries.py`'s `report()` was ENTIRELY untested, all four branches genuine coverage gaps: the function that says what was held back and why, so an untested report is how a held-back file becomes the silent skip the tool's design forbids | FIXED; 8 output-asserting cases added, all four branches mutation-proved DETECTED with corrected controls |
| 2026-07-25 | note | I claimed `collect-deliveries.py` had 9 guards; an independent audit measured 21 control-flow decision sites. I had counted my own hand-picked mutation list and called it the population | ACCEPTED and recorded: the probe now discovers sites rather than taking a hand-listed set, which is why it is a tool |


| Found | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 2026-07-25 | error | `collect-deliveries.py:81` empty-part guard in `split_name` was BLIND: the cases covered a non-tray name and a wrong extension but never an empty part, so `split_name("__x.md")` returned `("", "x")` and a caller could use an empty worker id, which the saturation tool's phantom-pending retirement depends on being well-formed | FIXED this PR; two cases added and the guard's removal now FAILS the self-test, verified |
| 2026-07-25 | error | `audit-worker-saturation.py` reported SATURATED while a worker sat idle, because the delivery tray added a third location its phantom-pending retirement did not scan, and the tray's composed filename also needed splitting | FIXED this PR; two fixture cases added, both mutation-proved load-bearing with controls bracketing the run |
| 2026-07-25 | error | The probe voided itself on any tool importing a sibling module, because it wrote the mutant into a temp SUBDIRECTORY | FIXED this PR; mutants are sibling files now, caught by the probe's own negative control |
| 2026-07-25 | error | The probe reported a FALSE CLEAN (22 detected, 0 findings) after the verdict strings gained a suffix while the filter still tested exact equality | FIXED this PR; filter matches by prefix, caught only because the number contradicted an earlier run |
