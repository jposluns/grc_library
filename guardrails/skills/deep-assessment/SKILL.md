---
name: deep-assessment
description: Maintainer-invoked, rare-cadence whole-project deep assessment. Runs the full layered examination of the project and its quality machinery from a fresh session, composing the configured semantic instruments by invocation and adding the lenses the routine cadence does not apply to itself: gate-efficacy probing, ground-truth citation sampling, adoptability and pipeline-integrity review, and a QA-ledger meta-audit. Multi-session and re-entrant: a durable register carries phase state across session boundaries, every confirmed finding is routed tiered with none dropped, and the pass terminates on the QA-activity completion standard its component instruments already use, not on a separate maintainer sign-off, and never on a self-declared "done" before the phases have run.
derives_from: ../../governance/trust-recovery-escalation.md
---

# Deep Assessment (whole-project peace-of-mind review)

## Project wiring (the parent library's instantiation; adopters substitute their own)

Portable procedure, concrete names. In the parent GRC library this skill runs with:

- Phase-state register: the deep-assessment phase-state register in the consuming project's working state (durable, non-dated,
  in-repo; carries run and phase state across session boundaries).
- Per-run record pattern: a dated per-run record in the consuming project's working state (the dated-file
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

The routine cadence examines changes, recent project-wide drift, and named semantic
classes. None of it examines the quality system itself from outside: the gates check
project artefacts, the skills check those artefacts and the gates' outputs, and the same
assistant lineage may have authored both the content and the machinery. This skill is
the rare-cadence instrument for that residual: a deliberate whole-project pass that
runs configured instruments formally and probes what they cannot see, including gate
pattern width, exemption blind spots, citation accuracy against held source texts where
available, fresh-reader adoptability, delivery-pipeline integrity, and QA-ledger honesty.

Structurally this is the trust-recovery suite run proactively, at maintainer direction,
without a discipline-failure trigger. It inherits TWO of that rule's load-bearing
conventions: findings routing (every confirmed finding routed, tiered by severity, none
dropped) and apply-time verification before routing. It does NOT inherit the
maintainer-sign-off terminal state (maintainer-directed 2026-07-27): the sign-off exists
in the reactive trust-recovery tier to let the maintainer declare confidence RESTORED
after a discipline lapse, and the proactive deep-assessment has no lapsed confidence to
restore. Every component instrument it composes (`/validate`, `/full-qa`, `/fitness`,
`/matrix-fit`, `/claim-fit`, `/reference-audit`, `/screen-publications`, `/guardrails`, the gate-efficacy probes)
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
- **NOT a substitute** for the adopting project's configured per-change, project-wide,
  or reactive trust-recovery cadences.

## Process

### 1. Establish run state, environment integrity, and the live inventory

Read the phase-state register named in the project wiring. If a run is `in-progress`,
resume at its next incomplete phase; otherwise open a new run row and a per-run record
file (the dated per-run record pattern named in the project wiring; the non-dated
register stays in-repo by design). Environment preconditions, each verified
mechanically, never assumed: a full clone (`git rev-parse --is-shallow-repository` must
print `false`; unshallow first otherwise, per the full-clone methodology rule), every
repository and operational store named in the project wiring present, and the
session-concurrency interlock satisfied. Derive the live
instrument inventory from the repo, not from this skill's text: the gate list from the
audit runner, the PR-time checks from the delta runner, the skill and command set from
the command directory and the pack skills directory, the advisory tools from the tools
directory, and the specification's gate inventory section (each named in the project
wiring). Record the inventory and the HEAD SHA in the run record.

### 2. Confirm the mechanical baseline

Run, standalone and unpiped, every configured baseline validator: the full audit runner,
change-scoped runner, linter regression suite, generator checks, and validation gates for
each in-scope repository. All must exit 0 before any semantic phase; a failure is itself
a finding and is fixed or routed before proceeding. A non-green validation surface has
the same standing regardless of which configured repository owns it. Record the
green-at-revision baseline and cross-check it against the project's current session or
handoff record where one exists.

### 3. Run the project's semantic instruments, formally

Invoke, in their full sanctioned shapes with their own records and history rows, every
semantic instrument configured for this adoption. Apply project-wide instruments to the
whole configured content scope, mapping instruments to the whole configured mapping
surface, reference-breadth instruments to the configured content and source stores, and
screening instruments to each configured untrusted-source worklist. The parent GRC
library's concrete command set and publication status are labelled provenance, not
portable required topology. Run configured advisory aids whose outputs feed later phases.
Each instrument's findings enter this run's routing in addition to the instrument's own
record; no abbreviation of any invoked instrument is sanctioned. Where the harness
supports per-dispatch model selection, assign work according to the adopting project's
model policy and set the session model deliberately at phase boundaries.

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
hallucination ledgers still have no gate or convention guard. (d) **independent parity re-derivation**: reconcile every configured declaration and
execution inventory by hand, explaining or routing every discrepancy rather than
trusting the parity gate's own pass. (e) **validation-coverage**: run the configured
coverage tool, which reports, per repository the assistant writes to, whether a
validating workflow reaches it and whether recent changes landed through the project's
approved reviewed path or an ungated direct push. The other lenses examine artefacts and
their gates, not the landing sequence, so an unvalidated operation, such as a direct push
to a protected branch that never triggered the configured review and validation path, is
otherwise invisible by construction. This sub-pass reads the durable landing evidence.
An ungated landing on a repository that should require review is a HIGH trust-recovery
finding; unreadable branch-protection enforcement routes as a maintainer-verify deferral.

### 5. Sample content accuracy against ground truth

A stratified sample across the adopting project's configured frameworks and domains,
judged against held source texts through the configured source index, with the upstream
currency rule applied per source this turn: does the cited clause state what project
content attributes to it, do quotes correspond, and are editions current upstream. Fan
out adversarial readers briefed to refute cross-document coherence beyond deterministic
consistency gates. Label unverifiable items and give each accepted-unverified item a
durable tracker.

### 6. Assess adoptability, pipeline integrity, and the QA ledgers

Four sub-passes: (a) **fresh-adopter simulation**: from a bare clone with no project
context, follow the project's documented entry path to complete one representative core
workflow (in the parent library, its README, portal, and scorecard to select and tailor
one document); score discoverability, adoption friction, toolchain portability (the project's stated toolchain claims; for the parent library, its stdlib-only tooling and Python version envelope), and the documented adopter options. (b) **pipeline
integrity**: review the delivery workflow's hardening (permissions scoping, action
pinning) against the project's own pack and local rules, verify protected-branch
enforcement via the platform API rather than assuming it, run a full-history secret and
PII scan, and verify the guard and hook defences fire in the current environment.
(c) **ledger meta-audit**: sample QA history rows against their run records for the
sham-pass shape, trend the hallucination and session metrics, and reconcile the
cross-repo coverage surfaces. (d) **operational-store document consistency**: because an
operational store can receive direct-push operations that no gate content-checks, read
the load-bearing operational documents of each operational store named in the project
wiring for internal consistency and against the project content and ledgers they
coordinate (in the parent library: its decision-log against the closed-item and
pending-decisions state, its design-decisions record, its operating runbook against the
live process and the repo model, its egress and activity requests for staleness, and its
store index against what the store actually holds). A divergence is a finding routed
like any in this phase; this is the content half of the coverage the phase-2 gate cannot
give, since such a store has no content gate. Where an operational store is not in a
worker's read surface, this sub-pass, that store's phase-2 gate, and its phase-4(e) row
are run by the orchestrator directly.

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
workers, coordinated through the configured phase-state register or work-claim mechanism.
Each unit is claimed before work and reported on completion, pinned to the run revision.
The mechanical baseline is a BARRIER: every configured baseline unit must be green before
any semantic-phase unit starts. Any repository or operational resource outside worker read
authority remains orchestrator-only; all other units are dispatchable according to the
adopting project's worker-exchange and access model. The parent GRC library's private,
corpus, reference, and worker-exchange split is not a portable requirement. After the
baseline join, independent semantic units may fan out; synthesis and final recording remain
orchestrator-only.

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
