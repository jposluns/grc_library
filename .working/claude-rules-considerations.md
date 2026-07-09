# Claude-rules considerations (GR-P2 condense removal ledger)

**Version:** 1.0.0\
**Date:** 2026-07-08\
**License:** CC BY-SA 4.0

## Purpose

This file is the removal register for the GR-P2 two-layer condense of the governance
pack rules under [`dev-security/claude-rules/governance/`](../dev-security/claude-rules/governance/)
(TODO 4.7 GR-P2). The condense keeps the always-on **operative core** of each rule (the
normative statements, the numbered procedures, the prohibited-response and
correct-response lists, the anti-patterns, the exception protocol, the tool-specific
guidance) and moves the **rationale and provenance** (the "Why this rule exists"
narrative, the extended worked examples, and repeated restatements of the audit-trail
axiom) here. The compact framework-alignment control-mapping table STAYS in each rule:
the pack README names the canonical rule as the source of truth for framework alignment
and carries no per-rule matrix, so the table is distributed traceability, not rationale to
cut (a design decision surfaced for the maintainer; see the delivery payload). It is the exact method the PR
#441 [`.claude/CLAUDE.md`](../.claude/CLAUDE.md) condense used, applied to the pack rules;
that condense's own ledger is [`claude-md-considerations.md`](claude-md-considerations.md).

Nothing is lost. Each removal is preserved verbatim below (inside fenced code blocks, so
gate 51's dash scan of this `.working/` tree stays green while the text is byte-for-byte
intact) with an analysis of why it went, the expected gain, the potential risk, and the
observable signal that would show the removal was wrong.

## Review cadence (the "advise on putting it back" loop)

Identical to the #441 ledger: every `/retro` scans the open RM entries; the periodic
hallucination-metrics review does a deeper pass. For each open entry, check whether its
"evidence the removal was wrong" signal has appeared (a recurrence of the failure class
the removed text documented, an agent or maintainer re-litigating a settled rule, a
question the removed text would have answered). If it has, advise restoring the text or
making a new rule change, and record the disposition in the entry's Status. A removal
whose signal never appears is evidence the cut was correct.

**Status values:** `open` (cut, watching) | `reviewed-keep-out (YYYY-MM-DD)` | `restored (PR #N, YYYY-MM-DD)` | `inspired-change (PR #N, YYYY-MM-DD)` | `dispositioned-codified (PR #N, YYYY-MM-DD)`.

---

## RM-GDP-1: gate-discipline.md Why-this-rule-exists section (framework table considered, KEPT)

**Rule:** [`gate-discipline.md`](../dev-security/claude-rules/governance/gate-discipline.md). **Status:** open.
**Condensed in:** GR-P2 tranche 1 (this delivery). Operative core retained in full (prohibited-responses, correct-responses, per-tool anti-patterns, exception protocol, AND the framework-alignment table); 1559 -> 1173 words (measured). Only the why-section is moved here.

**Why removed:** the why-section is motivating rationale that restates the "a silenced gate is decoration / the cost asymmetry justifies the discipline" axiom the operative core already enacts. The framework-alignment table is NOT removed: the pack README (line 34) names the canonical RULE as the source of truth for framework alignment and carries no per-rule alignment matrix, so stripping the table would lose distributed traceability adopters rely on. See the payload's surfaced design decision.
**Expected gain:** ~410 fewer always-on words for a rule of this shape (the why-section); the operative core reads faster. Rules with large why-sections and worked examples reduce far more.
**Risk:** an adopter loses the AI-assistant "do not suppress as a first move" framing (mitigated: the operative prohibited-list already forbids every suppression path).
**Evidence the removal was wrong:** an agent re-litigating whether a gate may be silenced after the condense.

Removed verbatim (the why-section only; the framework table stays in the rule):

```
## Why this rule exists

Audit and governance programmes derive their value from being unconditional. A "gate" that can be silenced when inconvenient is not a gate; it is decoration. The maintainability cost of fixing the artefact is bounded and accrues to the team that introduced the defect. The cost of letting one defect through accrues to every future user of the artefact and compounds with every subsequent defect the gate would have caught. The asymmetry justifies the discipline.

The exception process exists precisely so that legitimate, time-bounded deviations are possible without normalizing bypass as a routine response. If the exception process feels burdensome, that is the control working as designed: the friction is proportional to the residual risk of holding a known defect open.

For AI coding assistants specifically: when a gate fails, do not propose suppressing it as a first move. Diagnose the failure, propose a fix to the artefact, and surface the choice to the human operator. If the operator wants to suppress, that decision is theirs, documented under the exception process; it is not yours to make unilaterally.
```

---

## Pending rule entries (per-rule worklist for GR-P2 tranches 2+)

Each remaining rule condenses on the same split. This worklist records the pre-analyzed
operative-vs-rationale boundary so a later tranche (or the orchestrator) applies it
per-rule without re-deriving it. Entries are added here verbatim as each rule is
condensed.

| Rule | Words | Operative core (KEEP) | Move to ledger (rationale) | Est. reduction |
| --- | --- | --- | --- | --- |
| `gate-discipline.md` | 1559 | prohibited/correct responses, per-tool anti-patterns, exception protocol, framework table | why-section | done (-26%) |
| `evidence-grounded-completion.md` | 4342 | the verification protocol steps, the un-observable/inventory/currency corollaries, anti-patterns, tool-specific guidance, framework table | why-section, the multi-surface worked example | high (~-40%) |
| `change-tracking.md` | 4422 | entry-content requirements, terse-entry convention, prohibited anti-patterns, CI-gate contract, PR-finalization protocol, overnight-work protocol, framework table | why-section, extended monorepo/generated-changelog rationale | high (~-35%) |
| `ai-assistant-workflow-disciplines.md` | 4236 | the five disciplines' rules, the skeptical-verifier tiers, the prohibited anti-patterns, framework table | why-section, the per-discipline origin narratives | high (~-35%) |
| `surface-counterproductive-instructions.md` | 2526 | the trigger classes, the stop-consider-confirm protocol, the charitable-interpretation corollary, calibration, anti-patterns, framework table | why-section, relationship-to-pack prose | medium |
| `action-before-explanation-of-inaction.md` | 2504 | the inaction-explanation definition, the reversibility gate, the safe/destructive protocols, anti-patterns, tool guidance, framework table | why-section | medium |
| `clarify-before-acting.md` | 2212 | ambiguity classes, ask-vs-default gate, compute-first gate, how-to-ask, anti-patterns, tool guidance, framework table | why-section | medium |
| `project-integrity.md` | 2231 | the AIQT tier + machinery, priority enforcement, integrity non-negotiables, escalation, self-reminder cadence, framework table, AND the relationship-to-pack section (operative cross-wiring) | why-section | low-medium |
| `high-assurance-verification.md` | 2414 | the trigger conditions, the five-stage harness, persistence/register, anti-patterns, framework table | why-section, relationship-to-pack prose | medium |
| `trust-recovery-escalation.md` | 1876 | the trigger, the two-skill suite, findings-routing, sign-off discipline, anti-patterns, framework table | why-section | medium |
| `artefact-and-branch-discipline.md` | 1816 | generated-artefact + protected-branch definitions and workflows, prohibited anti-patterns, version-monotonicity contract, exception protocols, framework table | why-section | medium |
| `validate-inference-before-action.md` | 1760 | the inferred-premise definition, the discipline steps, anti-patterns, tool guidance, exception protocol, framework table | why-section, the cascade-failure worked example | medium |
