---
name: guardrail-review
description: When the governance machinery itself (the rules, skills, and audit gates that keep a governed codebase honest, plus their wiring surfaces) needs a structural-integrity review, run this skill. It is the periodic guard-rail review: a judgment-based pass over the machinery for overlap (two rules or gates covering the same ground), gap (a stated discipline no gate enforces, a recurring failure mode no rule names), and drift (a rule, skill, or gate whose intent has diverged across its wiring surfaces in a way the mechanical parity gates cannot detect, because they check identity and count, not meaning). Maintainer-triggered, and auto-prompted after any PR that adds, removes, or renames a rule, skill, or gate. Catches the architectural erosion the per-PR and corpus-content sweeps are not built to see. Slash command `/guardrails`.
derives_from: ../../governance/gate-discipline.md
---

# Guardrail Review (governance-machinery structural integrity)

## Project wiring (the parent library's instantiation; adopters substitute their own)

Portable procedure, concrete names. In the parent GRC library this skill runs with:

- Per-run record path: `.working/guardrail-reviews/YYYY-MM-DD-rN.md`, with a row appended to the review history beside it.
- Failure-mode ledgers the gap lens reads: `.working/improvement-log.md` and the worker-hallucination-metrics ledger (in the consuming project's working state).
- Mechanical baseline runner: `tools/run_all_audits.sh` (must exit 0 before the semantic review begins); the baseline run includes the git-history-aware gates 31 and 40, which misfire on a shallow clone.
- Mechanical parity gates that must be green first: gates 35 (gate-name parity), 37 (claude-rules-sync), 39 (gate-count consistency), 41 (collection-enumeration), and 44 (paired-skill step-parity).
- Cadence-currency backstop: gate 60 (guardrail-review cadence currency) compares the live machinery inventory (the gate, rule, skill, and command counts) against the newest history row's as-of counts, passing with a warning while the summed per-axis drift is 1 or 2 and failing the build once the drift reaches 3.
- Inventory surfaces: governance rules under `dev-security/claude-rules/governance/` with their `.claude/rules/governance/` mirror and three enumeration surfaces (the pack README tree, the pack `CLAUDE.md`, and the project `.claude/CLAUDE.md`); skills under `dev-security/claude-rules/skills/` with the PAIRS registry; gates declared across the four parity surfaces (the CI workflow, the local runner, the pre-commit config, and the audit-programme specification's gate-inventory section).

An adopting project maps each bullet to its own record path, ledgers, baseline runner, parity gates, cadence backstop, and inventory surfaces; the procedure below refers to them generically.

## Overview

A governed codebase accumulates machinery: governance rules, the skills that operationalize them, the audit gates that enforce them, and the wiring surfaces that keep all three in lock-step (a gate declared across every parity surface the project maintains; a rule mirrored from the pack into a local rules copy and enumerated wherever the project lists its rules; a skill paired with a slash command and registered for step-parity). The mechanical parity gates verify that these surfaces agree by identity and count: the gate names match across their surfaces, the rule mirror is byte-identical, the skills directory matches the enumeration tree, the paired step-identifiers match. What no mechanical gate can verify is whether the machinery is *coherent*: whether two rules overlap, whether a stated discipline has no enforcing gate, whether a gate has quietly become decorative, whether a rule's intent has drifted from the skill that claims to operationalize it.

`guardrail-review` is that coherence review. It is the periodic structural-integrity pass over the machinery, run with three lenses: **overlap** (redundant or contradictory coverage), **gap** (a discipline, failure mode, or surface that nothing enforces), and **drift** (a meaning that has diverged across wiring surfaces below the resolution of the mechanical parity gates). It is judgment-based, because each of these questions requires reading the machinery as a designer would, not as a string-matcher does.

It is distinct from the content sweeps and the trust-recovery suite, and the distinction is the point. `/validate` and `/validate-pr` review the *corpus content* for regression. `/full-qa` and `/fitness` form the trust-recovery escalation tier, re-examining a *window of work* when an assistant's discipline has lapsed. `guardrail-review` reviews the *machinery itself*: the rules, skills, and gates as a system, asking whether the system is still well-formed. The content sweeps ask "is the corpus right?"; guardrail-review asks "is the apparatus that keeps the corpus right still well-built?".

## When to Use

- **Maintainer-triggered**, as a periodic structural deliverable (a natural cadence is at batch boundaries, before a pack release, or whenever the machinery has grown enough that its coherence is worth re-confirming). Like `library-fitness-review`, it is a periodic review, not a per-PR gate.
- **Auto-prompted after any PR that adds, removes, or renames a rule, skill, or gate.** When the machinery inventory changes, its coherence is exactly what a mechanical parity gate cannot re-confirm; the assistant surfaces a one-line prompt offering the review. The maintainer decides whether to run it now or defer, but the deferral is bounded rather than open-ended: a cadence-currency backstop gate (named in the project wiring) compares the live machinery inventory against the newest history row's as-of counts, passing with a warning while the drift stays small and failing the build once the drift crosses the gate's threshold, so a deferred review is mechanically forced before the machinery drifts far.
- **Before distributing the pack as a standalone baseline.** In pack-distribution mode the machinery *is* the product; a structural review before release is the equivalent of a content proof-read.
- **NOT** as a substitute for the mechanical parity gates named in the project wiring. Those run every PR and catch identity/count drift mechanically; guardrail-review is the semantic layer above them, not a replacement for them.

## Process

### 1. Establish the machinery inventory and the mechanical baseline

Run the project's full audit suite (the mechanical baseline runner named in the project wiring) and confirm it exits 0. The mechanical parity gates named in the project wiring must be green before the semantic review begins: a red parity gate is an identity/count defect to fix mechanically first, not a structural finding for this skill. (Where the baseline run includes git-history-aware gates, a shallow clone makes them misfire, so confirm `git rev-parse --is-shallow-repository` prints `false`, and `git fetch --unshallow` first if it does not.)

Then enumerate the current machinery as the inventory under review:

- **Governance rules**: the pack's rule files, their project-local mirror, and every enumeration surface that lists them (the concrete surfaces are named in the project wiring).
- **Skills**: the pack's skill directories, each with its `derives_from` parent, its slash-command counterpart (if paired), its pairing registration, and its enumeration-tree entry.
- **Gates**: the audit gates declared across the project's parity surfaces (named in the project wiring), each with its linter and the discipline it enforces.

### 2. Review the inventory through three lenses

Each lens is a systematic pass (or a dispatched subagent); every finding quotes `path:line`.

- **Overlap**: do two rules, two skills, or two gates cover the same ground? Redundant coverage is a maintenance cost (two surfaces to keep in sync) and a contradiction risk (the two can drift apart). For each candidate pair, decide: is the overlap deliberate and documented (different lenses on one surface, like `/full-qa`'s subagents A and F), or is it accidental redundancy that should be merged or one side retired?
- **Gap**: is there a stated discipline (in a rule, in `CLAUDE.md`, in a SKILL) that no gate enforces? a recurring failure mode (visible in the failure-mode ledgers named in the project wiring) that no rule names and no gate catches? a rule with no operationalizing skill where one is warranted? a gate that covers one surface while a sibling surface is ungated? A gap is where the machinery says it does something the machinery does not actually enforce.
- **Drift**: has a rule's, skill's, or gate's *meaning* diverged across its wiring surfaces in a way the mechanical parity gates cannot see? The parity gates check that the gate names match, the mirror is byte-identical, the counts agree; they do not check that a rule's pack copy and the one-line `CLAUDE.md` bullet describing it still mean the same thing, that a gate's docstring still matches what its code enforces, or that a skill's `description` still matches its parent rule's intent. Semantic drift below the parity gates' resolution is this lens's quarry. (The recurring real instance in the parent library: a convention revised in the rule but left stale in a one-line enumeration description, caught only later by a routine content sweep.)

### 3. Synthesize and verify at apply-time

Dedupe findings by `(surface, item, lens)`; adjudicate severity (pick the higher of adjacent disagreements; no averaging); and **re-read each cited source before routing any finding**. A lens pass (or subagent) produces research, not findings; the orchestrator confirms each against the live source, because a structural claim about an unread surface is a hypothesis. Findings refuted at apply-time are recorded with the refutation, not routed.

### 4. Route findings to the backlog, severity-tiered

Route every confirmed finding to the project backlog, tagged with the run-keyed parenthetical the backlog uses (a `(rN guardrails, size, effort)` marker naming the originating run, for example `(r8 guardrails, M, S)`), tiered by severity (High[critical]/High to the top-priority tier, Medium/Low to the next), none dropped. Structural findings frequently *propose a machinery change* (merge two overlapping rules, add a gate to close an enforcement gap, retire a decorative check, reconcile a drifted description). These are proposals for maintainer triage, not changes the skill applies autonomously: changing the machinery is a design decision the maintainer owns. Findings that dedupe against an existing backlog item are cross-referenced, not duplicated.

### 5. Record

Write a per-run record (at the per-run record path named in the project wiring) with one section per lens (overlap, gap, drift), an orchestrator-synthesis-and-verification section, and a findings-routed section. Append a row to the review history. Zero-finding runs still get a history row; the record file is conditional on findings, matching the sibling sweeps' convention. Before committing the record, verify each fixed-in-window claim against the actual diff (grep the diff for the claim's target text) and downgrade to routed any claim whose edit is absent: a record written from fix intent rather than from the diff is the record-asserts-unapplied-fix escape a pre-push verifier caught in the parent library's history, and the false claim propagates to every surface that restates the record's counts.

### 6. Surface to the maintainer (termination)

Surface the confirmed findings inline in chat (per-finding: lens, severity, `path:line`, evidence quote, the proposed machinery change). The review is a single pass, not a fix-to-fixed-point loop: structural findings are maintainer-decision proposals, so the skill does not re-run itself to convergence the way `/validate` does. It terminates when the findings are routed and surfaced. (When the maintainer accepts a proposed machinery change, that change is its own PR, which itself becomes a trigger under the auto-prompt cadence.)

## Red Flags

- Running guardrail-review while a mechanical parity gate is red. Fix the identity/count defect mechanically first; the semantic review assumes the mechanical baseline is green.
- A finding without a quoted `path:line` (it is a hypothesis, not a finding).
- Routing a lens finding without the orchestrator's own re-read (apply-time verification is the false-positive filter, the same as in the content sweeps).
- Applying a proposed machinery change autonomously. Overlap-merges, gate additions, and rule retirements are maintainer-owned design decisions; the skill proposes, the maintainer disposes.
- Treating guardrail-review as a per-PR gate. It is a periodic deliverable; running it on every PR is both wasteful and not what the cadence calls for.
- Confusing this skill with the content sweeps. If the question is "is the corpus right?", that is `/validate`; if it is "is the machinery well-built?", that is this skill.

## Verification

The review is complete on a given run when: the mechanical baseline was confirmed green (the parity gates in particular); the machinery inventory was enumerated across rules, skills, and gates; all three lenses (overlap, gap, drift) were applied with evidence-quoted findings; the orchestrator re-read each cited source and confirmed or refuted it; every confirmed finding was routed to its severity-appropriate backlog tier tagged with the `(rN guardrails, size, effort)` parenthetical, none dropped, with proposed machinery changes flagged as maintainer-decision proposals; and the per-run record and history row were written and the findings surfaced in chat.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The parity gates pass, so the machinery is fine." | The parity gates check identity and count, not coherence. They pass while two rules overlap, a discipline goes unenforced, or a description drifts in meaning. That gap is exactly what this skill reviews. |
| "This overlap is obviously fine; skip it." | Then record it as a confirmed deliberate overlap with the reason. An undocumented "obviously fine" is how accidental redundancy hides until the two surfaces contradict each other. |
| "There is no gap; everything important has a gate." | "Important" is the judgment under review. Check the failure-mode ledgers named in the project wiring for recurring failure modes; a pattern with no rule and no gate is a gap regardless of how it felt. |
| "I found a drifted description, so I'll just fix it now." | Fixing a stale description is a content fix (fine to bundle). Merging rules, adding a gate, or retiring a check is a machinery change the maintainer owns; route it as a proposal, do not apply it autonomously. |
| "Run it every PR to be safe." | It is a periodic review, not a gate. The mechanical parity gates run every PR; this skill runs on the maintainer trigger and the inventory-change auto-prompt. |

## See Also

- Canonical rule [`governance/gate-discipline.md`](../../governance/gate-discipline.md): the rule this skill operationalizes at the machinery level (a gate, and by extension the whole apparatus, derives its value from being meaningful and unconditional, not decorative).
- Related skill [`skill-authoring-discipline`](../skill-authoring-discipline/SKILL.md): the per-skill structural template; guardrail-review is the system-level counterpart that reviews the machinery as a whole rather than one new skill.
- Related skill [`deep-qa-review`](../deep-qa-review/SKILL.md) (`/full-qa`): its audit-programme-integrity subagent (C) checks the gate-wiring parity within a trust-recovery window; guardrail-review generalizes that check to the standing machinery and adds the overlap and gap lenses.
- Sibling skills [`validation-sweep`](../validation-sweep/SKILL.md) (`/validate`) and [`library-fitness-review`](../library-fitness-review/SKILL.md) (`/fitness`): the content-regression and fresh-reader reviews; guardrail-review is the machinery-structure review that complements them.
- Canonical rule [`governance/evidence-grounded-completion.md`](../../governance/evidence-grounded-completion.md): the apply-time re-read discipline each finding meets before routing.

## Why this skill exists

The governance machinery of the parent library grew severalfold across its rules, skills, and gates, each addition wired across multiple surfaces. The mechanical parity gates grew alongside it and reliably catch identity and count drift: a gate missing from one of its parity surfaces, a rule mirror that fell out of sync, a skill absent from the enumeration tree. What they cannot catch is the slow architectural erosion that comes with growth: two rules that have come to overlap, a discipline added to a `CLAUDE.md` section that no gate ever enforced, a one-line rule description that drifted in meaning from the rule it describes while the mechanical mirror check stayed green. Each of those is a structural defect invisible to a string-matcher and visible to a designer reading the machinery as a system. A routine content sweep in the parent library caught a concrete instance (a routing convention revised in the rule but left stale in two enumeration descriptions); guardrail-review is the standing, periodic review that hunts that class deliberately rather than waiting for a content sweep to stumble on it. It is judgment-based and maintainer-gated by design: the mechanical layer is the per-PR enforcer, and this skill is the periodic architect's walk-through of what the mechanical layer cannot see.
