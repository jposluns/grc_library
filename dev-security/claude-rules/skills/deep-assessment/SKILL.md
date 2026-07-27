---
name: deep-assessment
description: Maintainer-invoked, rare-cadence whole-project deep assessment. Runs the full layered examination of the library and its own quality machinery from a fresh session, composing the existing semantic instruments (/validate, /full-qa, /fitness, /matrix-fit, /claim-fit, /reference-audit, /screen-publications, /guardrails) by invocation and adding the lenses the routine cadence does not apply to itself, gate-efficacy probing (mutation and blind-spot analysis), ground-truth citation sampling, adoptability and pipeline-integrity review, and a QA-ledger meta-audit. Multi-session and re-entrant: a durable register carries phase state across session boundaries, every confirmed finding is routed tiered with none dropped, and the pass terminates on the QA-activity completion standard its component instruments already use (every finding validated and fixed-or-routed), not on a separate maintainer sign-off, and never on a self-declared "done" before the phases have run.
derives_from: ../../governance/trust-recovery-escalation.md
---

# Deep Assessment (whole-project peace-of-mind review)

## Project wiring (the parent library's instantiation; adopters substitute their own)

Portable procedure, concrete names. In the parent GRC library this skill runs with:

- Phase-state register: `.working/deep-assessment/register.md` (durable, non-dated,
  in-repo; carries run and phase state across session boundaries).
- Per-run record pattern: `.working/deep-assessment/YYYY-MM-DD-rN.md` (the dated-file
  convention the fitness-review records use).
- Gate-efficacy tools (phase 4's deterministic halves): `tools/audit-gate-blindspots.py`
  and `tools/audit-gate-mutation.py` with its variant library
  `tools/gate-mutation-variants.json`; and the validation-coverage tool for phase 4(e),
  `tools/audit-validation-coverage.py`.
- Phase-3 advisory aids: `tools/verify-reference-modules.py`,
  `tools/audit-brief-freshness.py`, `tools/residual-scan.py`, and `tools/tension-scan.py`
  (the last two run over the QA ledgers).
- Sibling-repo set: the corpus repo (`grc_library`), the reference base
  (`grc_library_ref`, the held source texts and indexes phase 5 judges against), the
  worker exchange (`grc_library_scratch`, the delivery pipeline phase 6 reviews), and the
  private operational store (`grc_library_private`, the orchestrator's operational state:
  the decision-log, the design-decisions record, the operating runbook, the egress and
  activity requests, and the store index; phase 2 runs its gate and phase 6(d)
  content-reviews it). Each sibling carries its own validation gate (`tools/validate.py`);
  `grc_library` carries `tools/run_all_audits.sh` instead. CAUTION: `grc_library_private`
  has received direct-push-to-`main` operations that bypassed the PR and CI path, so its
  content is not gate-verified by construction, and it is not in a worker's read surface,
  so its baseline gate, its validation-coverage row, and its phase-6(d) content review are
  orchestrator-only.
- Phase-1 inventory sources: the audit runner `tools/run_all_audits.sh`, the PR-time
  delta runner `tools/run-pr-time-checks.sh`, the `.claude/commands/` directory plus the
  pack skills directory, the advisory tools under `tools/`, and the audit-programme
  specification's gate inventory section.

An adopting project maps each bullet to its own register, record convention,
gate-efficacy probes, advisory aids, sibling repositories, and inventory sources; the
procedure below refers to them generically.

## Overview

The routine cadence examines changes (per-PR sweeps), recent drift (corpus sweeps), and
named semantic classes (matrix-fit, claim-fit). None of it examines the quality system
itself from outside: the gates check the corpus, the skills check the corpus and the
gates' outputs, and the same assistant lineage that authors the content built the
machinery. This skill is the rare-cadence instrument for that residual: a deliberate,
whole-project pass that runs the existing instruments formally AND probes what they
cannot see, the width of the gates' own patterns, the union of their exemption blind
spots, the semantic accuracy of citations against held source texts, the adoptability
of the library by a fresh reader, the integrity of the delivery pipeline, and the
honesty of the QA ledgers.

Structurally this is the trust-recovery suite run proactively, at maintainer direction,
without a discipline-failure trigger. It inherits TWO of that rule's load-bearing
conventions: findings routing (every confirmed finding routed, tiered by severity, none
dropped) and apply-time verification before routing. It does NOT inherit the
maintainer-sign-off terminal state (maintainer-directed 2026-07-27): the sign-off exists
in the reactive trust-recovery tier to let the maintainer declare confidence RESTORED
after a discipline lapse, and the proactive deep-assessment has no lapsed confidence to
restore. Every component instrument it composes (`/validate`, `/full-qa`, `/fitness`,
`/matrix-fit`, `/claim-fit`, `/reference-audit`, `/guardrails`, the gate-efficacy probes)
already terminates by validate-and-fix, so the composite terminates on the same
QA-activity completion standard, not on a redundant sign-off gate. It differs from
trust-recovery in trigger (maintainer peace of mind, not lapsed confidence) and in scope
(the whole project including the audit programme itself, not a window of work).

Two design rules keep a rarely-run procedure from rotting. First, the skill is
COUNT-FREE and INVENTORY-DERIVING: no step names a gate count, skill count, or file
list; step 1 re-derives the live instrument inventory from the repo at run time
(from the runner scripts, command directory, and specification gate inventory named in
the project wiring). The live inventory of quality machinery IS the scope by construction:
every gate, skill, command, advisory tool, and check the repo holds is in scope, and any
quality-check process or instrument added in future is included automatically, with no
edit to this skill. The obligation runs the other way too: adding a quality-check
instrument carries the duty to ensure that this pass covers it, so a new gate gains a
phase-4 mutation-probe variant, a new slash-command or skill joins the phase-3 invocation
set, and a new advisory tool joins the phase-3 aids. The phase-3 instrument set is
therefore a named enumeration this obligation keeps synced with the live inventory,
not an auto-derived list: "inventory-deriving" describes the SCOPE re-derivation of
step 1 (nothing falls out of scope silently), while a newly-shipped instrument is
added to the phase-3 invocations by this duty, as `/screen-publications` was when its
cadence shipped. Second, phase state lives in a durable register (the phase-state
register named in the project wiring), so the pass survives session boundaries and a
bare re-invocation resumes rather than restarts.

## When to Use

- **Maintainer-invoked, rare cadence.** This is a heavy, deliberate pass (multiple
  sessions, substantial token cost). It is not part of the per-PR or per-batch cadence
  and is never self-invoked by the assistant.
- **Resume.** Invoked with no arguments while a run is in flight, the skill continues
  at the next incomplete phase from the register.
- **NOT a substitute** for the per-PR `/validate-pr` + `/retro` cadence, the corpus
  `/validate` cadence, or `/trust-recovery` (which remains the reactive tier for
  lapsed-confidence windows and keeps its own trigger and semantics).

## Process

### 1. Establish run state, environment integrity, and the live inventory

Read the phase-state register named in the project wiring. If a run is `in-progress`,
resume at its next incomplete phase; otherwise open a new run row and a per-run record
file (the dated per-run record pattern named in the project wiring; the non-dated
register stays in-repo by design). Environment preconditions, each verified
mechanically, never assumed: a full clone (`git rev-parse --is-shallow-repository` must
print `false`; unshallow first otherwise, per the full-clone methodology rule), the
corpus repo, the reference base, the worker exchange, and the private operational store
(as named in the project wiring) all present, and the session-concurrency interlock
satisfied. Derive the live
instrument inventory from the repo, not from this skill's text: the gate list from the
audit runner, the PR-time checks from the delta runner, the skill and command set from
the command directory and the pack skills directory, the advisory tools from the tools
directory, and the specification's gate inventory section (each named in the project
wiring). Record the inventory and the HEAD SHA in the run record.

### 2. Confirm the mechanical baseline

Run, standalone and unpiped: the audit runner and the PR-time delta runner (named in
the project wiring), the linter regression suite, every generator `--check` invocation,
and each sibling repo's own validation gate. All must exit 0 before any semantic phase;
a failure here is itself a finding and is fixed or routed before proceeding. A sibling
gate that went red while ungated direct-push operations kept landing on that sibling is
the exact failure this phase now catches, so a non-green sibling gate is a finding of the
same standing as a red corpus gate, not a silent condition. Record the green-at-SHA
baseline in the register and cross-check it against the session handoff's asserted
expectations.

### 3. Run the project's semantic instruments, formally

Invoke, in their full sanctioned shapes with their own records and history rows: the
sweep pre-flight scanner then a corpus-wide `/validate`; `/full-qa` over the whole
corpus; `/fitness`; `/matrix-fit` over the whole matrix; `/claim-fit` over Tier A with
a Tier-B sample; `/reference-audit` in FULL mode over the whole corpus and the in-scope reference base; `/screen-publications` over the reference base's `pending` publications rows; and `/guardrails`. Run the advisory aids whose outputs feed later
phases (the phase-3 advisory aids named in the project wiring, including the ledger
scanners). Each instrument's findings enter this run's
routing (step 7) in addition to the instrument's own record; no abbreviation of any
invoked instrument is sanctioned. Where the harness supports per-dispatch model
selection, run the orchestration and finding-adjudication work on the strongest available
model tier, the wide fan-out readers on a cheaper tier, and treat the mechanical phases as
model-indifferent; the invoked instruments' own subagents inherit the invoking session's
model, so set the session model deliberately at phase boundaries.

### 4. Audit the audit programme itself

The phase the routine cadence never runs. Five sub-passes, each recorded: (a)
**blind-spot map**: run the blind-spot mapping tool named in the project wiring to
compute, from every
linter's own exemption configuration, which repo surfaces are scanned by which gates
and which are scanned by none; every fully-unscanned surface gets a manual review
noted in the run record. (b) **mutation probe**: in a DISPOSABLE copy of the repo
outside the working tree, seed defect variants per gate class with the mutation-probe
tool named in the project wiring and confirm each gate detects its class at pattern
widths beyond the regression fixtures (position, separator, encoding, and phrasing
variants); undetected variants are findings against the gate. The working repos are
never mutated. (c) **dead-gate and coverage analysis**: from full history, which gates
have never fired, and which recurring failure classes in the improvement and
hallucination ledgers still have no gate or convention guard. (d) **independent parity
re-derivation**: reconcile the workflow, runner, pre-commit, and specification
inventories by hand, explaining or routing every count discrepancy rather than
trusting the parity gate's own pass. (e) **validation-coverage**: run the
validation-coverage tool named in the project wiring, which reports, per repository the
assistant writes to, whether a validating CI workflow reaches it and whether recent
commits landed through a PR (with a validating workflow present in the repo) or an
ungated direct-push. The other lenses of
this phase examine the ARTEFACTS and the GATES that check them; none examines the
sequence of pushes that actually landed, so a whole class of unvalidated operation (a
direct push to `main` that never opened a PR and never triggered CI) is invisible by
construction: no artefact is wrong and every gate that ran was green, yet a change landed
unchecked. This sub-pass reads the durable evidence that operation leaves, the git
landing pattern and the CI-workflow presence, not an operation log there is none to
trust. An ungated landing on a repo that should require PRs is a HIGH trust-recovery
finding (it is the class this lens exists to close); a branch-protection enforcement the
assistant's token cannot read routes as a maintainer-verify deferral in the phase-8
record, never silently cleared.

### 5. Sample content accuracy against ground truth

A stratified sample per framework and domain, judged against the held texts in the
reference base via its indexes, with the upstream currency rule applied per source this
turn: does the cited clause state what the corpus attributes to it (beyond what
`/matrix-fit` and `/claim-fit` already worklist), do quotes correspond, and are
editions current upstream. Fan out per-domain adversarial readers briefed to REFUTE
cross-document coherence (values, terminology, roles, scope boundaries) beyond the
hard-coded consistency gates. Unverifiable items are labelled, never asserted, and
each accepted-unverified item gets a durable tracker.

### 6. Assess adoptability, pipeline integrity, and the QA ledgers

Four sub-passes: (a) **fresh-adopter simulation**: from a bare clone with no project
context, follow the README, portal, and scorecard to select and tailor one document;
score discoverability, tailoring friction, toolchain portability (the project's stated toolchain claims; for the parent library, its stdlib-only tooling and Python version envelope), and the documented adopter options. (b) **pipeline
integrity**: review the CI workflow's hardening (permissions scoping, action pinning)
against the project's own pack and overlay rules, verify branch protection is enforced
via the platform API rather than assumed, run a full-history secret and PII scan, and
verify the guard and hook defences fire in the current environment. (c) **ledger
meta-audit**: sample QA history rows against their run records for the sham-pass
shape, trend the hallucination and session metrics, and reconcile the cross-repo
coverage surfaces. (d) **private-store operational-document consistency**: because the
private operational store (named in the project wiring) has received direct-push
operations that no gate content-checks, read its load-bearing operational docs for
internal consistency and against the corpus and ledgers they coordinate: its decision-log
(do resolved entries match the corpus closed-item and pending-decisions state), its
design-decisions record, its operating runbook (does it still describe the live process
and the repo model), its egress and activity requests (are recorded requests still
accurate, not stale), and its store index (does it enumerate what the store actually
holds). A divergence is a finding routed like any in this phase; this is the content half
of the coverage the phase-2 gate cannot give, since the private store has no content gate.
Where the private store is not in a worker's read surface, this sub-pass, the private
store's phase-2 gate, and its phase-4(e) row are run by the orchestrator directly.

### 7. Verify, dedupe, tier, and route every finding

Per the trust-recovery routing convention: each subagent or tool finding is a
hypothesis until the orchestrator re-reads the cited source and confirms it;
refutations are recorded with their evidence, not routed. Confirmed findings are
deduped against the existing backlog (cross-referenced, not duplicated), severity
tiered (High[critical] and High to the backlog's top-priority tier, Medium and Low to
the next), tagged to their originating phase, and routed with NONE dropped. In-window
mechanical fixes may ship as normal PRs under the full per-PR QA cadence; everything
else routes.

### 8. Record, surface, and route to a terminal disposition

Write the run record (per-phase outcomes, the inventory, the baseline, the findings
register with verified / refuted / routed status) and update the register row. Surface
the routed set to the maintainer, tiered, so they SEE the outcome. The run terminates on
the QA-activity completion standard (maintainer-directed 2026-07-27): it is complete when
it ran in the sanctioned formal shape, every finding is triaged to a terminal disposition
(fixed in-window OR routed to the backlog with a severity tier), positives were re-verified
at source, the history row is recorded, and any deferred fix is documented. There is NO
separate maintainer-sign-off gate; a zero-finding run still gets its record and register-row
closure. The register row stays `in-progress` only while a phase is incomplete or a finding
is still un-triaged, and the next `/resume` surfaces such a row like the other standing
registers.

### Parallel execution (worker fan-out)

Every phase decomposes into disjoint units the orchestrator may dispatch to parallel
workers, coordinated through the phase-state register extended from per-phase to per-unit
rows: each unit is claimed before work and reported on completion, pinned to the run HEAD
SHA, the same claims-ledger discipline the project's worker exchange already uses. Two
constraints bound the fan-out. The mechanical baseline (phase 2) is a BARRIER: every
baseline unit, including each sibling gate, must be green before any semantic-phase unit
starts, so phase 2 is dispatched then joined, never overlapped with phases 3 to 6. And the
private operational store is not in a worker's read surface, so its baseline gate, its row
of the phase-4(e) validation-coverage sub-pass, and its phase-6(d) operational-document
review are orchestrator-only units; everything on the corpus, the reference base, and the
worker exchange is worker-dispatchable. After the phase-2 join, phases 3, 4, 5, and 6 run
as one parallel fan-out, each semantic instrument, each phase-4 sub-pass, each citation
batch, and each phase-6 slice a separate unit; phase 7 (synthesis) joins them and is
orchestrator-only, as is phase 8 (record and route). A full pass's wall-clock then drops
from serial to about the slowest unit per phase plus the two barriers.

## Red Flags

- Self-invoking the skill. The TRIGGER is the maintainer's: it runs only on explicit
  maintainer invocation, never self-scheduled. (The terminal state, by contrast, is no
  longer a maintainer sign-off; it is the QA-activity completion standard, reached when
  every finding is validated and fixed-or-routed.)
- Self-declaring the run "done" before the phases actually ran, or before every finding
  is triaged to a terminal disposition. A zero-finding run is legitimately complete once
  the phases ran and the record and register-row closure are written; skipping the phases
  is not.
- Running any phase-3 instrument in an abbreviated shape. The instruments' own
  no-abbreviation rules apply unchanged inside this skill.
- Hard-coding a gate count, skill list, or file inventory into the run instead of
  deriving it in step 1. A rare-cadence procedure with baked-in counts is stale by its
  second run.
- Mutating the working repos in the mutation probe. Phase 4(b) runs only in a
  disposable copy; the probe script must refuse a target inside a live checkout.
- Running history-aware analysis on a shallow clone. Verify clone depth first; a mass
  history-gate failure on a shallow clone is an environment artefact.
- Dropping a low-severity finding instead of routing it at the appropriate tier.
- Trusting the parity gate to check itself in phase 4(d), or a ledger row to prove the
  QA it records actually ran in phase 6(c). Both are re-derived independently.
- Losing an in-flight run across a session boundary. The register row is the carrier;
  update it at every phase boundary, not only at the end.

## Verification

A run is complete on a given invocation when:

- The register shows every phase `complete` (or `deferred` with a maintainer-visible
  reason), each with a dated record file at the per-run record location named in the
  project wiring.
- The environment preconditions were mechanically verified and the green-at-SHA
  baseline recorded before any semantic phase ran.
- Every phase-3 instrument has its own formal record and history row in addition to
  this run's record.
- Every finding in the run record carries a verified / refuted / routed status with
  evidence, and the routed set is deduped against the backlog.
- Every finding in the routed set is triaged to a terminal disposition (fixed or routed
  with a severity tier), positives re-verified at source; the register row is then closed
  with the completion date. A run with an incomplete phase or an un-triaged finding is
  `in-progress`, whatever the finding count. (There is no separate maintainer sign-off gate;
  the run is surfaced to the maintainer, but completion is the QA-activity completion standard.)

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The gates are green, so the deep pass is redundant." | The gates prove what the gates check. This skill exists for what they structurally cannot check: their own pattern width, their blind spots, semantic accuracy, adoptability, and the ledgers' honesty. |
| "The regression suite already tests the linters." | It proves one fixture per rule fires. The mutation probe tests pattern WIDTH, which is where the project's own escape history lives. |
| "Zero findings, so we are done." | Completion is the QA-activity standard met (the phases actually ran, in formal shape, with the record and history row written), not a self-declared "done"; a zero-finding run still gets its record and register-row closure. |
| "Skip the fitness pass this time; full-qa covered it." | The two lenses are complementary by design (the trust-recovery rule's pen-testing analogy); dropping one is abbreviation. |
| "The register slows things down; just run it end to end." | The pass spans sessions. Without the register a boundary silently truncates it, and a truncated deep pass reads as a completed one. |
| "Probe the gates in place; it is faster than a copy." | A mutation in a live checkout risks the exact corruption the pass exists to prevent. Disposable copy only. |

## See Also

- Canonical rule [`trust-recovery-escalation`](../../governance/trust-recovery-escalation.md):
  the suite shape, routing convention, and full-clone methodology this skill inherits and
  applies proactively. The sign-off discipline is trust-recovery-specific (it lets the
  maintainer declare lapsed confidence restored) and is NOT inherited by the proactive
  deep-assessment, which terminates on the QA-activity completion standard.
- Canonical rule [`evidence-grounded-completion`](../../governance/evidence-grounded-completion.md):
  the verification protocol behind every phase's claims, including the
  external-version-currency corollary phase 5 applies.
- Canonical rule [`high-assurance-verification`](../../governance/high-assurance-verification.md):
  the register-persistence pattern this skill's run register mirrors.
- The invoked instruments: [`validation-sweep`](../validation-sweep/SKILL.md),
  [`deep-qa-review`](../deep-qa-review/SKILL.md),
  [`library-fitness-review`](../library-fitness-review/SKILL.md),
  [`matrix-fit`](../matrix-fit/SKILL.md), [`claim-fit`](../claim-fit/SKILL.md),
  [`reference-audit`](../reference-audit/SKILL.md),
  [`publication-screening`](../publication-screening/SKILL.md),
  [`guardrail-review`](../guardrail-review/SKILL.md). This skill composes them by
  invocation and deliberately does not restate their procedures, so they cannot drift.
- The gate-efficacy tools named in the project wiring (phase 4's deterministic halves;
  not gates; always exit 0 on completion of their report, 2 only on a safety refusal or
  internal error).
