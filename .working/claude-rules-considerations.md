# Claude-rules considerations (GR-P2 condense removal ledger)

**Version:** 1.0.2\
**Date:** 2026-07-12\
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

## RM-VIA-1: validate-inference-before-action.md, Cascade-failure worked example + Why-this-rule-exists

**Rule:** [`validate-inference-before-action.md`](../dev-security/claude-rules/governance/validate-inference-before-action.md). **Status:** open.
**Condensed in:** GR-P2 tranche 2 (this delivery). Operative core retained in full; 1760 -> 1301 words. Moved to this ledger: the "Cascade failure" worked example and the "Why this rule exists" narrative.

**Why removed:** the cascade-failure section is an extended worked example (the Sweep-9 six-step narrative) and the why-section restates the assertion-vs-action-boundary rationale the operative discipline steps already enact. Both are motivating rationale, not operative instruction. The operative core (inferred-premise definition, the four discipline steps, anti-patterns, tool-specific guidance, exception protocol, framework table) is retained in full.
**Expected gain:** about 459 fewer always-on words (26%), the largest tranche-2 cut, because the worked example is long; the operative steps read faster.
**Risk:** an agent loses the concrete Sweep-9 cascade illustration (mitigated: the anti-patterns list already names the skip-because-prior-run and validate-one-infer-the-rest shapes the example illustrated).
**Evidence the removal was wrong:** an agent skipping a subagent, test, or gate on an inferred "nothing changed" premise after the condense, or a maintainer re-litigating why validation is unconditional.

Removed verbatim:

```
## Cascade failure: why the rule is structural

An unvalidated inference does not just produce one wrong action. It produces a chain.

A worked example from this project's history (Sweep 9, 2026-06-20):

1. The orchestrator inferred "no parity-surface changes since the prior sweep" without checking what changed.
2. The inference drove an action: skip subagent C (the audit-programme integrity reviewer).
3. The action created a downstream gap: gate 39's source had in fact just changed in a recent PR, but no subagent reviewed the change for parity-surface implications.
4. The maintainer flagged the skip as a discipline failure.
5. Subagent C was then dispatched and surfaced two findings (one in the linter's docstring, one in a separate file's comment).
6. Subsequent subagent B in the next iteration surfaced a third related finding (a parallel stale-count occurrence in yet another file) that had been missed because the orchestrator inferred "I fixed the C-2 finding" without grepping for parallel occurrences.

The first inference (step 1) was the source. Each subsequent step depended on it. The total cost was: a discipline failure flagged by the maintainer, two follow-up findings, a third follow-up finding from a parallel pattern that escaped because the first inference was already cascading.

The discipline named by this rule would have fired at step 1. Cost: one or two tool calls. Total downstream cost prevented: every step from 2 onwards.

---

## Why this rule exists

The recurring failure mode this rule addresses: an AI coding assistant infers a premise (most commonly: "nothing changed since prior X, so skip / proceed"), acts on the inference, and the action propagates a wrong premise into downstream work. By the time the maintainer or a later check catches the failure, the cascade has touched multiple artefacts.

The rule's structural value is to interrupt the cascade at its source. The inferred premise is identified in the draft, the validation is taken before the action, and the action's premise is grounded in observation. Each step in the cascade requires its own validation; an inference cannot drive an action, and a wrong action cannot drive downstream work.

For AI coding assistants specifically: when the next sentence in a draft contains a state claim followed by an action, pause and validate the state claim. The cost of the protocol (one extra tool call) is much smaller than the cost of an unvalidated inference that the user has to catch.

This rule was added to the pack in 2026-06-21 after a recurring failure mode where an orchestrator inferred subagent-skip justifications, fix-completeness, and corpus-state without validating, and each inference cascaded into downstream rework. The mechanism is at the assertion-of-action boundary, not at the assertion-about-artefact boundary; the evidence-grounded-completion rule covers the latter, and this rule covers the former.
```

---

## RM-ABD-1: artefact-and-branch-discipline.md, Why-this-rule-exists

**Rule:** [`artefact-and-branch-discipline.md`](../dev-security/claude-rules/governance/artefact-and-branch-discipline.md). **Status:** open.
**Condensed in:** GR-P2 tranche 2 (this delivery). Operative core retained in full; 1816 -> 1590 words. Moved to this ledger: the "Why this rule exists" narrative.

**Why removed:** the why-section restates the generator-is-canonical and branch-is-canonical rationale the operative workflows and prohibited-anti-patterns already enforce. The operative core (generated-artefact and protected-branch definitions and workflows, prohibited anti-patterns, the version-monotonicity contract, the tool-specific guidance, both exception protocols, framework table) is retained in full.
**Expected gain:** about 226 fewer always-on words (12%).
**Risk:** an adopter loses the hand-edit-and-force-push-look-like-progress framing (mitigated: the prohibited-anti-patterns list already forbids both paths explicitly).
**Evidence the removal was wrong:** an agent hand-editing a generated artefact or force-pushing a protected branch to "save a round-trip" after the condense.

Removed verbatim:

```
## Why this rule exists

A generator is the canonical statement of how an artefact derives from its source. A hand-edit silently substitutes the human's judgement for the generator's; future regenerations will not preserve the hand-edit, and the artefact will diverge from the source in a way that is invisible until the next regeneration. The drift check is the contract that says "what the generator would produce" and "what is committed" must match; hand-editing breaks the contract.

A protected branch is the canonical statement of what the project's history looks like. A force-push silently rewrites that history; downstream branches that had pulled the old history are now broken; CI runs whose state depended on the old history must be re-run; auditors who cited specific commits now have dangling references. The version-monotonicity audit is the last line of defence against history rewrites that drop version-bearing entries, but it depends on the branch being append-only to begin with.

For AI coding assistants specifically: when CI flags a generated-artefact drift, the answer is "regenerate locally and commit the result," not "hand-edit the artefact to match what the generator would have produced." When CI flags a branch-protection violation, the answer is "rebase and re-push the feature branch through the PR," not "force-push past the check." The hand-edit and the force-push look like fast paths; they are defects in disguise.
```

---

## RM-TRE-1: trust-recovery-escalation.md, Why-this-rule-exists

**Rule:** [`trust-recovery-escalation.md`](../dev-security/claude-rules/governance/trust-recovery-escalation.md). **Status:** open.
**Condensed in:** GR-P2 tranche 2 (this delivery). Operative core retained in full; 1876 -> 1598 words. Moved to this ledger: the "Why this rule exists" narrative.

**Why removed:** the why-section recounts the originating incident (the eleven-PR abbreviation window) and the tier's value proposition, which the operative trigger, suite, findings-routing, and sign-off sections already encode. The operative core (the trigger, the two-skill suite, the severity-tiered findings-routing, the sign-off discipline, the after-sign-off codification, prohibited anti-patterns, framework table) is retained in full.
**Expected gain:** about 278 fewer always-on words (14%).
**Risk:** the originating-incident context is no longer inline (mitigated: it is preserved verbatim here, and the operative trigger list names the same failure shapes).
**Evidence the removal was wrong:** a maintainer or agent unsure when the tier fires, or self-authorizing its completion, after the condense.

Removed verbatim:

```
## Why this rule exists

The escalation tier was developed after a session in which an AI assistant abbreviated a mandatory per-change quality step across eleven consecutive changes, skipped a post-commit audit that then failed the shared pipeline twice, and armed a fallback timer at the wrong interval. The mechanical layer had not yet grown a gate to catch the abbreviation; the maintainer's manual catch was the only backstop. The maintainer's response was not a single re-check but a structured re-examination of the whole window, run as a suite of two complementary reviews, with every confirmed finding routed (none discounted) and the maintainer's explicit sign-off as the terminal condition.

That structure is this rule. It is invoked rarely, by maintainer judgement, when confidence in a window of work has lapsed. Its value is that it is heavier and more honest than the routine cadence: it assumes the assistant's own judgement about the window is unreliable (that is why the tier was triggered), so it removes the assistant's discretion to abbreviate, to discount findings, and to declare completion. The maintainer rebuilds confidence by reviewing what the suite surfaced and signing off. The first run of the tier immediately justified the full-clone methodology rule by catching a shallow-clone false positive that would otherwise have shipped as a corpus emergency.

For AI coding assistants specifically: if you recognize the trigger pattern in your own recent work, surface it to the maintainer rather than hoping it goes unnoticed. The tier is not a punishment; it is the path back to a trusted state, and naming the need for it is itself an act of the integrity the tier exists to restore.
```

---

## RM-ABE-1: action-before-explanation-of-inaction.md, Why-this-rule-exists

**Rule:** [`action-before-explanation-of-inaction.md`](../dev-security/claude-rules/governance/action-before-explanation-of-inaction.md). **Status:** open.
**Condensed in:** GR-P2 tranche 2 (this delivery). Operative core retained in full; 2504 -> 2206 words. Moved to this ledger: the "Why this rule exists" narrative.

**Why removed:** the why-section restates the inference-vs-evidence failure mode and the rule's structural reversal, which the operative reversibility gate, the safe-action and destructive-action protocols, and the execution-vs-decision-doubt section already enact. The operative core (the inaction-explanation definition, the reversibility gate, both action protocols, the execution-vs-decision-doubt distinction, anti-patterns, tool-specific guidance, exception protocol, framework table) is retained in full.
**Expected gain:** about 298 fewer always-on words (11%).
**Risk:** an agent loses the narrative of why a guessed inaction-reason erodes trust (mitigated: the operative safe-action protocol already forbids the unverified inaction explanation directly).
**Evidence the removal was wrong:** an agent drafting an unverified "X is blocked because Y" inaction explanation without attempting the safe action, after the condense.

Removed verbatim:

```
## Why this rule exists

The classic failure mode this rule addresses: an AI coding assistant encounters a state it has not interrogated this turn (a CI status, a PR's mergeability, a branch's protection rules, a permission boundary), drafts an inaction explanation grounded in inference rather than evidence, and the user trusts the explanation because it sounds like a system fact. The user then either waits unnecessarily (the action would have proceeded), takes the wrong corrective action (the explanation pointed at the wrong cause), or loses some trust in the assistant when the inaction explanation turns out to be wrong. Each outcome is worse than the cheap, reversible action that would have produced a real result.

The rule's structure reverses the failure mode. The trigger is the specific surface (inaction-explanation vocabulary attached to an external action) where the inference-vs-evidence question is decided in writing, in a way the actor can catch in their own draft. The fail-safe is the reversibility gate, which keeps "default to the action" from collapsing into "default to recklessness" against destructive actions. The destructive-set protocol prevents the same inference failure from migrating into a scary-sounding rationale for waiting. The execution-doubt-vs-decision-doubt clause keeps the rule from being misread as a lean-away-from-asking on authorial choices, where asking is the right move.

For AI coding assistants specifically: when the next sentence in your draft is about to explain why an external action cannot proceed, pause and run the reversibility gate. If the action is safe, attempt it and rewrite the sentence around the real result. If the action is destructive, name it and ask. The cost of the protocol (one tool call or one explicit "I have not attempted X") is much smaller than the cost of an unverified inaction explanation that the user relies on.
```

---

## RM-CBA-1: clarify-before-acting.md, Why-this-rule-exists

**Rule:** [`clarify-before-acting.md`](../dev-security/claude-rules/governance/clarify-before-acting.md). **Status:** open.
**Condensed in:** GR-P2 tranche 3 (this delivery). Operative core retained in full; 2212 -> 2022 words. Moved to this ledger: the "Why this rule exists" narrative only (the relationship-to-pack section, where present, was KEPT).

**Why removed:** the why-section restates the silent-authorial-decision and wrong-scope-work failure modes and the ask-is-an-action framing the operative ambiguity classes, the ask-vs-default gate, the compute-first gate, and the how-to-ask rules already enact. The operative core (ambiguity classes, ask-vs-default gate, compute-first gate, how-to-ask, anti-patterns, tool-specific guidance, exception protocol, framework table) is retained in full.
**Expected gain:** about 190 fewer always-on words (8%).
**Risk:** an agent loses the "confidence grows when you ask sharp questions" framing (mitigated: the operative how-to-ask and anti-patterns sections already encode it).
**Evidence the removal was wrong:** an agent silently picking a target branch, date format, or dependency after the condense, or over-asking on findable facts.

Removed verbatim:

```
## Why this rule exists

The two failure modes a clarify-before-acting discipline prevents are:

1. **Silent authorial decisions**. The assistant picks for the user; the user discovers the pick after the fact; the user pays the unwind cost. Over time, the user learns to over-specify requests, which is friction in the other direction.
2. **Wrong-scope work**. The assistant interprets the request more broadly (or more narrowly) than the user intended, ships the wrong-scope work, and the mismatch surfaces in review or in production. The cost of the mismatch is borne by the user.

The discipline shifts both costs back to the moment of choice. A one-sentence clarification at the start of the work is the lowest-friction intervention available. The cost is one round-trip; the benefit is correctly-scoped, correctly-aimed work.

For AI coding assistants specifically: the pressure to "make progress" can manifest as silent picking. Resist this. The user's confidence in the assistant grows when the assistant asks sharp, specific questions and shrinks when the assistant ships work the user did not authorize. A clarification is not a failure to act; it is the action that the situation calls for.
```

---

## RM-SCI-1: surface-counterproductive-instructions.md, Why-this-rule-exists

**Rule:** [`surface-counterproductive-instructions.md`](../dev-security/claude-rules/governance/surface-counterproductive-instructions.md). **Status:** open.
**Condensed in:** GR-P2 tranche 3 (this delivery). Operative core retained in full; 2526 -> 2229 words. Moved to this ledger: the "Why this rule exists" narrative only (the relationship-to-pack section, where present, was KEPT).

**Why removed:** the why-section recounts the motivating wind-down-reverted-committed-work incident, which the operative trigger classes, the stop-consider-confirm protocol, and the charitable-interpretation corollary already encode. The operative core (the five trigger classes, the stop-consider-confirm protocol, the charitable-interpretation corollary, the calibration, anti-patterns, tool-specific guidance, the relationship-to-pack section, exception protocol, framework table) is retained in full; the relationship-to-pack section was KEPT (conservative, see the payload note).
**Expected gain:** about 297 fewer always-on words (11%).
**Risk:** the concrete wind-down incident is no longer inline (mitigated: preserved verbatim here; the charitable-interpretation corollary names the same shape operatively).
**Evidence the removal was wrong:** an agent executing a clear-but-counterproductive instruction (reverting committed work on a literal reading) without surfacing the cost, after the condense.

Removed verbatim:

```
## Why this rule exists

The motivating incident: a maintainer said "after the current piece of work is done, we will wind down". By the time the instruction arrived, the assistant had already started and committed the next piece. Read literally and silently, "wind down" was taken to override the committed work, and the assistant reverted it. The maintainer had meant one of two sensible things ("wind down after the next piece, since it is already underway", or "stop and ask me what to do with the in-flight work"), and neither was "destroy the committed work". The literal-and-destructive reading was the one path the maintainer did not intend, and it was taken without a word of confirmation.

Two disciplines already in the pack would each have caught it: `clarify-before-acting` (the instruction admitted more than one reading) and the confirm-before-destructive-action discipline (reverting committed work is destructive). What was missing was a rule that names the general case directly, so the assistant recognizes it at the moment of intake rather than reconstructing it from two adjacent rules under time pressure. That general case is: an instruction can be clear and still be the wrong thing to do, and the assistant's job is to notice that, surface it once with the cost and the options, and let the requestor make the call with full information.

For AI coding assistants specifically: the pull toward fast, compliant execution is strong, and it is precisely the pull this rule countermands. When executing the instruction in front of you would cost the requestor something they did not foresee, the right move is not to execute quickly and the right move is not to refuse; it is to stop, name the cost in one sentence, offer the better path, and act on the answer.
```

---

## RM-PI-1: project-integrity.md, Why-this-rule-exists

**Rule:** [`project-integrity.md`](../dev-security/claude-rules/governance/project-integrity.md). **Status:** open.
**Condensed in:** GR-P2 tranche 3 (this delivery). Operative core retained in full; 2231 -> 1864 words. Moved to this ledger: the "Why this rule exists" narrative only (the relationship-to-pack section, where present, was KEPT).

**Why removed:** the why-section restates the constraints-cost-under-pressure argument the operative priority-enforcement, integrity-non-negotiables, escalation, and self-reminder-cadence sections already fix. The operative core (the lexicographic Quality > Speed > Cost ordering, priority enforcement, the integrity non-negotiables, escalation, the self-reminder cadence, the relationship-to-pack cross-wiring, anti-patterns, framework table) is retained in full; the relationship-to-pack section was KEPT (it carries operative cross-wiring naming which non-negotiable maps to which sibling rule).
**Expected gain:** about 367 fewer always-on words (16%), the largest tranche-3 cut.
**Risk:** an adopter loses the "each relaxation looks locally rational and is globally corrosive" framing (mitigated: the apex-rule ordering and the non-negotiables already enact it).
**Evidence the removal was wrong:** an agent trading quality for speed under deadline or token pressure after the condense, or resolving a dimension conflict silently.

Removed verbatim:

```
## Why this rule exists

A governance pack is a set of constraints, and constraints cost time and tokens to satisfy. Under pressure, the cheapest way to make a constraint stop costing is to relax it: skip the re-read, suppress the gate, stub the hard part, claim completion on inference. Each relaxation looks locally rational (it saves real time or real cost) and is globally corrosive (it ships a defect, erodes the audit trail, and removes the signal that would have caught the next defect). The other rules in the pack each forbid one such relaxation. What they do not, individually, settle is what happens when satisfying them is in tension with a legitimate pressure to deliver.

This rule settles it. It fixes the ordering once, at the highest precedence, so the answer under pressure is not re-litigated every time: the AIQT tier first, then speed, then cost, with the tier itself non-negotiable. An actor who internalizes this rule does not experience a deadline as license to lower the bar; they experience it as a reason to escalate, to descope, or to ask, all of which preserve the tier, none of which silently trade it away.

**Provenance of the AIQT naming (2026-07-08, maintainer-directed).** This rule originally stated the ordering as "Quality > Speed > Cost" with project integrity named as absolute; that formulation and its checkpoint line ("Integrity check: ...") are superseded by the AIQT form, which names all four facets the original folded into "quality plus the integrity non-negotiables". The substance is unchanged: the non-negotiables, the escalation protocol, and the checkpoint cadence carry over verbatim; what the rename adds is that accuracy and trust, previously implicit components, are first-class named facets each mapped to its enforcing machinery. Historical records citing the earlier formulation remain accurate as records of their time.

For AI coding assistants specifically: the inclination to produce a fast, confident, complete-looking answer is strong, and it is precisely the inclination this rule countermands. When finishing quickly is in tension with finishing right, this rule is the one that decides, and it decides for the AIQT tier. Emit the checkpoint line, confirm compliance, and if you cannot, halt and escalate rather than shipping the compromise.
```

---

## RM-HAV-1: high-assurance-verification.md, Why-this-rule-exists

**Rule:** [`high-assurance-verification.md`](../dev-security/claude-rules/governance/high-assurance-verification.md). **Status:** open.
**Condensed in:** GR-P2 tranche 3 (this delivery). Operative core retained in full; 2414 -> 2107 words. Moved to this ledger: the "Why this rule exists" narrative only (the relationship-to-pack section, where present, was KEPT).

**Why removed:** the why-section recounts the originating compliance-matrix-column incident (the nine false-negative misses a single pass produced), which the operative trigger conditions, the five-stage harness, and the persistence/register sections already encode. The operative core (the three trigger conditions, the five-stage harness, the persistence/register model, prohibited anti-patterns, the relationship-to-pack section, framework table) is retained in full; the relationship-to-pack section was KEPT (it delineates this tier from trust-recovery-escalation and the routine disciplines, operative cross-wiring).
**Expected gain:** about 307 fewer always-on words (12%).
**Risk:** the concrete nine-misses illustration is no longer inline (mitigated: preserved verbatim here; the stage-3 adversarial-verifier and open-on-negative-with-signal rules encode the lesson operatively).
**Evidence the removal was wrong:** an agent reaching for the routine flow plus a careful hand-edit on a gate-blind, delicate-scale, high-cost change after the condense, instead of the harness.

Removed verbatim:

```
## Why this rule exists

The harness was developed after a maintainer-directed sensitive change: adding an AI-specific control-framework column to a compliance matrix, a wide single-artefact reshape where each cell carries a control code whose *fit* (is this the right control for this row's document?) no existence gate can check. The maintainer directed that integrity be made absolute through independent rechecking rather than trusted to a single pass. The layered harness that resulted caught real defects a single pass missed: the fast first-pass research, uneven in depth, inferred many "not applicable" verdicts from document titles without opening the documents; an independent false-negative verifier, re-reading those negatives, found nine genuine misses (each a document with a dedicated section the title did not advertise), and a false-positive verifier tightened three over-assignments. The mechanical floor (every code confirmed in the canonical set, the existence gate, and a deterministic re-parse of the rendered cells against the verified map) made the apply itself correct independent of the long hand-edit it replaced.

The lesson generalized: when a change is gate-blind on correctness, delicate at scale, and costly to get wrong, the routine layers are not enough, and the right response is not "be more careful" (an un-instrumented intention) but a structured harness whose independent adversarial stages and deterministic apply *produce* the assurance. The persistent register and the resume surfacing make it a recurring discipline rather than a one-session effort, so a sensitive item recognized in one session is verified to completion across whatever sessions the work spans.

For AI coding assistants specifically: when you recognize the three conditions in a change in front of you, do not reach for the routine flow and a careful hand-edit. Escalate to the harness, record the item in the persistent register, and let the independent verification and the deterministic apply carry the correctness, not your confidence.
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
| `surface-counterproductive-instructions.md` | 2526 | the trigger classes, the stop-consider-confirm protocol, the charitable-interpretation corollary, calibration, anti-patterns, framework table | why-section, relationship-to-pack prose | done (-12%) |
| `action-before-explanation-of-inaction.md` | 2504 | the inaction-explanation definition, the reversibility gate, the safe/destructive protocols, anti-patterns, tool guidance, framework table | why-section | done (-11%) |
| `clarify-before-acting.md` | 2212 | ambiguity classes, ask-vs-default gate, compute-first gate, how-to-ask, anti-patterns, tool guidance, framework table | why-section | done (-9%) |
| `project-integrity.md` | 2231 | the AIQT tier + machinery, priority enforcement, integrity non-negotiables, escalation, self-reminder cadence, framework table, AND the relationship-to-pack section (operative cross-wiring) | why-section | done (-16%) |
| `high-assurance-verification.md` | 2414 | the trigger conditions, the five-stage harness, persistence/register, anti-patterns, framework table | why-section, relationship-to-pack prose | done (-13%) |
| `trust-recovery-escalation.md` | 1876 | the trigger, the two-skill suite, findings-routing, sign-off discipline, anti-patterns, framework table | why-section | done (-14%) |
| `artefact-and-branch-discipline.md` | 1816 | generated-artefact + protected-branch definitions and workflows, prohibited anti-patterns, version-monotonicity contract, exception protocols, framework table | why-section | done (-12%) |
| `validate-inference-before-action.md` | 1760 | the inferred-premise definition, the discipline steps, anti-patterns, tool guidance, exception protocol, framework table | why-section, the cascade-failure worked example | done (-26%) |
