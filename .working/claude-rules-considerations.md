# Claude-rules considerations (GR-P2 condense removal ledger)

**Version:** 1.0.5\
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

## RM-EGC-1: evidence-grounded-completion.md

**Rule:** [`evidence-grounded-completion.md`](../dev-security/claude-rules/governance/evidence-grounded-completion.md). **Status:** open.
**Condensed in:** GR-P2 tranche 4 (this delivery, the final content tranche). Operative core retained in full; 4342 -> 3724 words. Moved to this ledger: the "Worked example: the multi-surface gate-name parity case" section and the "Why this rule exists" narrative.

**Why removed:** the worked example is an extended illustration and the why-section restates the summary-composed-from-inference failure mode; both are motivating, not operative. The operative core (the completion-claim definition, the beyond-completion state-assertion discipline, the un-observable/inventory/currency corollaries, the six-step verification protocol, anti-patterns, all tool-specific guidance including pipe-masked-exit-codes / API-polling / no-decorative-links, exception protocol, framework table) is retained in full.
**Expected gain:** about 618 fewer always-on words (14%), the largest single-rule cut in the whole GR-P2 pass, because the worked example is long.
**Risk:** an agent loses the multi-surface gate-name-parity illustration (mitigated: the operative verification protocol step 5 and the "run the parity check on the final state" discipline encode the lesson).
**Evidence the removal was wrong:** an agent declaring "all gates pass" from a prior run rather than the current state after the condense, or asserting an artefact property it did not read.

Removed verbatim:

```
## Worked example: the multi-surface gate-name parity case

A common shape of this rule's failure mode in governed codebases: a session adds a new audit gate to a programme that declares its gates across several parallel surfaces (CI workflow, local runner, pre-commit config, audit-programme specification). The session wires the gate into all but one of the surfaces, touching exactly the files it needed to touch for the implementation work, and prepares the changeset for the next operator with a summary claim of the form "all N audit gates pass on this state". The omitted surface is the one that did not appear on the session's working set, so the session's mental model of "did I do the wiring?" centred on the surfaces it did touch, and the missing one slipped past.

A gate-name parity audit, itself one of the N gates, would have caught the omission. The session's summary, though, was composed from inference ("I added the gate; the audit was passing earlier; it should still pass") rather than from running the audit on the final state. When the work was picked up next, the full audit run reported the parity gate failing with the correct diagnostic, and a one-block fix closed the loop. The total recovery cost was one extra audit-and-fix loop; the avoidable cost was the operator's reasonable trust in a summary that did not match the working tree.

The mechanical defence existed and worked. The discipline failure was the rule's *Relying on prior runs* anti-pattern: "it passed last time, and the only change is small" does not substitute for running the gates on the current state. The protocol applies even when the session is not in doubt; a claim that the audit suite passes on the current state requires running the audit on the current state, not on a state from earlier in the session.

The wider lesson for any work that touches several parallel surfaces (gate-name parity, generator-output drift checks, mirror-sync between a source-of-truth and its copies, polyglot lockfiles, cross-package version registers): the verification protocol must explicitly include "run the parity check on the final state, after every other change has been made". A session that did the wiring without the final-state check has completed the implementation tasks but not the verification task; the verification task is part of the work, not a coda to it.

---

## Why this rule exists

The classic failure mode this rule addresses: an AI coding assistant runs a passing audit, infers that the work is done, writes "all gates pass; ready to ship", and is wrong because the audit covered some claims and not others. A reviewer reads the summary, trusts the assistant, and the unsupported claim lands.

The discipline reverses the flow. The summary is composed *after* the verification, *from* the evidence, not from inference. The vocabulary of completion ("done", "fixed", "ready") becomes a flag that the assistant must satisfy the protocol before emitting; the protocol is mechanical (enumerate, re-read, quote, contradiction-search) so it can be checked without subjective judgement.

The cost of the protocol (a few extra tool calls and a more careful summary) is small. The cost of an unsupported completion claim that lands and gets relied on (a defect that ships, a reviewer's trust eroded, a user who later has to catch what the assistant should have caught) is much larger. The asymmetry justifies the discipline.

For AI coding assistants specifically: if a user catches an inconsistency that this rule's protocol would have caught, the right response is not "good catch" (which implies you understood and have it under control). The right response is "you caught what I should have caught; rerunning the verification protocol now", followed by actually rerunning the protocol.
```

---

## RM-CT-1: change-tracking.md

**Rule:** [`change-tracking.md`](../dev-security/claude-rules/governance/change-tracking.md). **Status:** open.
**Condensed in:** GR-P2 tranche 4 (this delivery, the final content tranche). Operative core retained in full; 4425 -> 4216 words. Moved to this ledger: the "Why this rule exists" narrative only (all operative how-to KEPT: the monorepo-coordination and generated-CHANGELOG subsections, the PR-finalization protocol, the overnight-work protocol).

**Why removed:** the why-section restates the CHANGELOG-is-institutional-memory cost argument the operative entry-content requirements and CI-gate contract already enforce. Only the why-section moved; the monorepo and generated-CHANGELOG subsections are operative how-to, not rationale, so they were KEPT (this is why the cut is a modest 4%: most of this rule is operative protocol).
**Expected gain:** about 209 fewer always-on words (4%); the rule is mostly operative, so the proportional cut is small by design.
**Risk:** an adopter loses the per-entry-cost-vs-compounding-cost framing (mitigated: the terse-entry convention and the no-skip-path rule encode it operatively).
**Evidence the removal was wrong:** an agent shipping a change with no CHANGELOG entry, or a vague/batched entry, after the condense.

Removed verbatim:

```
## Why this rule exists

A CHANGELOG is the cheapest form of long-term institutional memory a project has. Code review answers "is this change correct now"; the CHANGELOG answers "what changed and why" months or years later, after the original reviewer has rotated off the project and the original PR thread is buried.

The cost of an entry (one short section) is paid once, by the person closest to the change. The cost of *not* having an entry compounds: each future reader who hits the artefact and asks "when did this happen?" pays the price of reading the diff, reconstructing the rationale, and risking a wrong inference. Multiplied across years and contributors, the total cost dwarfs the per-entry cost by orders of magnitude.

The opt-out path exists because some changes are genuinely invisible to consumers and an entry would be noise. It is a documented trailer, mechanically inspectable, reviewer-approved; it is not silence. Silence is exactly what the audit trail is supposed to prevent.

For AI coding assistants specifically: when shipping a change, the entry is part of the change, not a separate concern to be added later. Treat a PR without an entry the same way you would treat a PR without a test: incomplete by construction.
```

---

## RM-AWD-1: ai-assistant-workflow-disciplines.md

**Rule:** [`ai-assistant-workflow-disciplines.md`](../dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md). **Status:** open.
**Condensed in:** GR-P2 tranche 4 (this delivery, the final content tranche). Operative core retained in full; 4236 -> 3975 words. Moved to this ledger: the "Why this rule exists" narrative (which carried the per-discipline emergence narratives).

**Why removed:** the why-section recounts how each of the five disciplines emerged during the originating remediation session; that is provenance, not operative instruction. The operative core (the five disciplines with their rules, the partitionable-work default, the apply-time correction, the skeptical-pre-push-verification tiers, the verifier-finding handling loop, the overruling-is-never-silent rule, the prohibited anti-patterns including the QA-abbreviation clause, framework table) is retained in full.
**Expected gain:** about 261 fewer always-on words (6%).
**Risk:** an agent loses the per-discipline origin stories (mitigated: each discipline's operative statement stands on its own; the provenance is preserved verbatim here).
**Evidence the removal was wrong:** an agent pasting worker prose unverified, running parallel applies, or abbreviating mandatory QA after the condense.

Removed verbatim:

```
## Why this rule exists

The five disciplines were developed during a multi-week corpus-remediation session in which an AI assistant drove 30+ PRs to close a fitness-review backlog. The session surfaced each failure mode in turn:

- **Research-assistant discipline** emerged after a worker confabulated a non-existent file path; the discipline was named so future workers would be treated as research, not as final prose.
- **Pipeline PR construction** emerged after early sessions were bottlenecked on serial research-then-apply; parallel research was added to keep the apply-queue non-empty.
- **Apply-time worker correction** emerged after several worker drafts referenced stale version numbers or wrong PR cross-references; documenting the catches turned them into a tracking signal.
- **Always split when in doubt** emerged after a maintainer noted that bundled PRs were harder to review than single-purpose ones; "split" became the default.
- **Background work during CI waits** emerged after a maintainer asked whether idle waits were necessary; they weren't, and read-only prep was identified as the safe productive use.

Each discipline pays back its complexity many times over the course of a long session. The cost of memorizing them is small; the cost of relearning them by repeated failure is large.

For AI coding assistants specifically: when you find yourself dispatching multiple workers in parallel, when you find yourself bundling changes, when you find yourself sitting idle during CI, when you find yourself pasting worker prose without re-reading the target file, pause and run the corresponding discipline. The disciplines exist because each failure mode was observed; the discipline keeps the failure mode from recurring.
```

## RM-SL-1: session-lifecycle.md Why-this-rule-exists section

**Rule:** [`session-lifecycle.md`](../dev-security/claude-rules/governance/session-lifecycle.md). **Status:** open.
**Condensed in:** the GR-P2 phase-1 close-out (the 13th-rule follow-up; session-lifecycle was added after the 12-rule GR-P2 set was scoped, so it had no worker candidate and was condensed on the same two-layer split). Operative core retained in full (the six RESUME/WORK/CLOSE disciplines, the prohibited anti-patterns, the tool-specific guidance, the exception-handling protocol, and the framework-alignment table); 1816 -> 1621 words (measured). Only the why-section is moved here.

**Why removed:** the why-section is motivating provenance (the failure modes each mechanism was earned against) that the operative six disciplines already enact; it restates the "name the mode, surface the decision, let evidence decide" axiom the rule body prescribes.
**Expected gain:** about 195 fewer always-on words (11%); the operative disciplines read faster.
**Risk:** an adopter loses the provenance narrative that motivates the wind-down and concurrency-lease mechanisms (mitigated: the operative sections state each mechanism's rule directly).
**Evidence the removal was wrong:** an agent treating a lifecycle decision (wind-down, idle, proceed-past-lease) as forced rather than operator-owned after the condense.

Removed verbatim (the why-section only; the framework table stays in the rule):

```
## Why this rule exists

Every mechanism above was earned in one project's multi-week AI-assisted run: sessions that degraded without their operator noticing until a maintainer catch; a wind-down proposed roughly thirteen of fifteen times when continuing was right, fixed by evidence-gating the trigger; an unattended run that idled overnight on a question its standing priorities already answered; a handoff snapshot falsified by the very change that refreshed it; and an accidental double-resume prevented only by luck before the lease existed. The pack form exists because none of this is project-specific: any documentation corpus, codebase, or governed artefact set run through multi-session AI assistance meets the same failure modes, and the apparatus (a durable handoff, named modes, degradation paths, an evidence-gated wind-down, a green-merge close with a compensating control, a lease) is the same defence everywhere.

For AI coding assistants specifically: the pull this rule countermands is narrating a lifecycle decision (winding down, idling, proceeding past a lease) as if it were forced, when it is actually a choice the operator owns. Name the mode, surface the decision with options, act on the answer, and let the evidence, not the feeling, decide when a session ends.
```

## Pending rule entries (per-rule worklist for GR-P2 tranches 2+)

Each remaining rule condenses on the same split. This worklist records the pre-analyzed
operative-vs-rationale boundary so a later tranche (or the orchestrator) applies it
per-rule without re-deriving it. Entries are added here verbatim as each rule is
condensed.

| Rule | Words | Operative core (KEEP) | Move to ledger (rationale) | Est. reduction |
| --- | --- | --- | --- | --- |
| `gate-discipline.md` | 1559 | prohibited/correct responses, per-tool anti-patterns, exception protocol, framework table | why-section | done (-26%) |
| `evidence-grounded-completion.md` | 4342 | the verification protocol steps, the un-observable/inventory/currency corollaries, anti-patterns, tool-specific guidance, framework table | why-section, the multi-surface worked example | done (-14%) |
| `change-tracking.md` | 4422 | entry-content requirements, terse-entry convention, prohibited anti-patterns, CI-gate contract, PR-finalization protocol, overnight-work protocol, framework table | why-section, extended monorepo/generated-changelog rationale | done (-5%) |
| `ai-assistant-workflow-disciplines.md` | 4236 | the five disciplines' rules, the skeptical-verifier tiers, the prohibited anti-patterns, framework table | why-section, the per-discipline origin narratives | done (-6%) |
| `session-lifecycle.md` | 1816 | the six RESUME/WORK/CLOSE disciplines, prohibited anti-patterns, tool guidance, exception protocol, framework table | why-section | done (-11%) (13th-rule follow-up) |
| `surface-counterproductive-instructions.md` | 2526 | the trigger classes, the stop-consider-confirm protocol, the charitable-interpretation corollary, calibration, anti-patterns, framework table | why-section | done (-12%) |
| `action-before-explanation-of-inaction.md` | 2504 | the inaction-explanation definition, the reversibility gate, the safe/destructive protocols, anti-patterns, tool guidance, framework table | why-section | done (-11%) |
| `clarify-before-acting.md` | 2212 | ambiguity classes, ask-vs-default gate, compute-first gate, how-to-ask, anti-patterns, tool guidance, framework table | why-section | done (-9%) |
| `project-integrity.md` | 2231 | the AIQT tier + machinery, priority enforcement, integrity non-negotiables, escalation, self-reminder cadence, framework table, AND the relationship-to-pack section (operative cross-wiring) | why-section | done (-16%) |
| `high-assurance-verification.md` | 2414 | the trigger conditions, the five-stage harness, persistence/register, anti-patterns, framework table | why-section | done (-13%) |
| `trust-recovery-escalation.md` | 1876 | the trigger, the two-skill suite, findings-routing, sign-off discipline, anti-patterns, framework table | why-section | done (-14%) |
| `artefact-and-branch-discipline.md` | 1816 | generated-artefact + protected-branch definitions and workflows, prohibited anti-patterns, version-monotonicity contract, exception protocols, framework table | why-section | done (-12%) |
| `validate-inference-before-action.md` | 1760 | the inferred-premise definition, the discipline steps, anti-patterns, tool guidance, exception protocol, framework table | why-section, the cascade-failure worked example | done (-26%) |

## RM-SCRUB-1: phase-3 zero-history scrub, six rules, fourteen passages (project wiring to overlays)

**Rules:** [`trust-recovery-escalation.md`](../dev-security/claude-rules/governance/trust-recovery-escalation.md), [`ai-assistant-workflow-disciplines.md`](../dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md), [`change-tracking.md`](../dev-security/claude-rules/governance/change-tracking.md), [`gate-discipline.md`](../dev-security/claude-rules/governance/gate-discipline.md), [`high-assurance-verification.md`](../dev-security/claude-rules/governance/high-assurance-verification.md), [`evidence-grounded-completion.md`](../dev-security/claude-rules/governance/evidence-grounded-completion.md). **Status:** open.
**Removed in:** the pack adoption-hygiene programme phase 3 (the D1 zero-history scrub). Unlike the GR-P2 rows above, nothing here is rationale: these are the residual "(in this project: ...)" wirings and out-of-pack links the condense left behind. Each removed value now lives in the corresponding `.claude/rules/` copy's PROJECT-OVERLAY block (the D2 marked-overlay architecture), so the local session loses nothing.
**Why removed:** the pack is adopted clean (D1); a project path, slash command, or gate number in a pack rule binds adopters to this project's layout.
**Expected gain:** zero out-of-pack relative links in the governance rules; every "(in this project ...)" instantiation relocated to the overlay layer.
**Risk:** a local session reading the PACK copy instead of its `.claude/rules/` copy loses the wiring pointer (mitigated: sessions load `.claude/rules/`, which carries the overlay).
**Evidence the removal was wrong:** a local session failing to find a register or command because it read the pack copy.

Removed or changed verbatim (pack-side originals; the overlay carries each value):

```
(in this project: `deep-qa-review`, slash command `/full-qa`)
(in this project: `library-fitness-review`, slash command `/fitness`)
(in this project: `.working/hallucination-metrics.md`)
from the hallucination-metrics catch entry by template Version number
(project-specific location; in this project: `.working/changelog-details/CHANGELOG-detailed.md`)
(not an audit gate; an orchestrator close-out step; in this project `tools/sweep-working-records-to-scratch.py`)
### Document corpora (this project's case)
### PR #172: FR-4+5+6+7+8: README polish bundle (2026-06-21)
A working-directory location is the recommended default; under this project's convention, `.working/DONE.md`. The exact location is project-specific.
(project-specific location; in this project: `.working/overnight-pr.md`)
(in this project, the exchange repository, as weekly Monday-dated files)
*The why-this-rule-exists narrative is retained in the removal ledger [`.working/claude-rules-considerations.md`](../../../.working/claude-rules-considerations.md) (the GR-P2 two-layer condense): it is motivating rationale, not operative instruction.
The mechanism is a persistent register at [`.working/high-assurance/register.md`](../../../.working/high-assurance/register.md) (relative to the corpus root; this rule ships in the pack, the register lives in the consuming project's working state).
verified by the broken-link audit (the gate's number is project-specific; in the GRC Library it is gate 3)
```

---
