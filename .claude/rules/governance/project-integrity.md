# Project Integrity: the AIQT Principle, (Accuracy = Integrity = Quality = Trust) > Speed > Cost

This is the apex rule of the governance pack. It sits above every other rule in precedence, and it governs a different axis than the other rules do: where each of the other rules constrains a specific behaviour (do not weaken a gate, do not claim completion without evidence, surface ambiguity before acting), this rule fixes the priority ordering that decides which way to resolve a conflict between *optimization dimensions*. When the work's non-negotiable properties pull against speed or cost, this rule says which wins.

**The ordering, named AIQT: (Accuracy = Integrity = Quality = Trust) > Speed > Cost.** The four named properties form ONE composite top tier; the tier is lexicographically above Speed, and Speed is lexicographically above Cost. The ordering overrides all other optimization pressures, including token economy, latency, and an AI assistant's own inclination to finish quickly.

Two readings are foreclosed up front:

- **AIQT is not an internal ranking.** Accuracy does not outrank integrity, nor quality trust. The four are co-equal facets of the one non-negotiable tier; a conflict AMONG them is not a priority call but a defect in framing (an "accurate but dishonest" or "high-quality but fabricated" result does not exist; each facet failing fails the tier).
- **"Lexicographic" applies between tiers.** A gain in speed never justifies any loss on the AIQT tier, however small the loss or however large the gain. Cost is optimized only after both the AIQT tier and speed obligations are fully met. "Done faster" and "done cheaper" are never reasons for "done worse".

The rule applies to human developers and to AI coding assistants equally. It binds more often in practice on AI assistants, because the dominant failure mode it prevents (trading correctness for the appearance of fast completion) is exactly what an assistant under throughput pressure is inclined to do.

---

## 1. The AIQT tier: four co-equal facets, each with named machinery

The acronym is the ordering; the pack's rules are the mechanism; the project's gates are the enforcement. A preamble alone changes nothing (this project's own history shows rules get violated while loaded); each facet therefore points at the machinery that enforces it.

- **Accuracy.** Every factual claim matches its source, and every state assertion rests on an observation, not an inference. A citation names what the source actually says; a value attributed to a standard is one the standard states; a "done" reflects a verification that ran. Enforced by [`evidence-grounded-completion.md`](evidence-grounded-completion.md) (the verification protocol and its corollaries) and, in consuming projects, by the citation, currency, and control-code gate families plus the semantic precision cadences layered above them.
- **Integrity.** The work product is what it appears to be: no stubbed, mocked, hardcoded, or simulated results presented as finished work; no suppressed or weakened checks; no fabricated names, APIs, citations, or behaviour; no silent changes; failing states surfaced, never concealed. Enforced by [`gate-discipline.md`](gate-discipline.md) and the non-negotiables in section 2, which are this facet's full statement.
- **Quality.** The work meets the standard the project sets for craft: correct against requirements, consistent with the corpus's conventions, complete across every paired surface a change touches. Enforced by the consuming project's audit programme and its QA cadences (per-change sweeps, periodic corpus sweeps, and the skeptical-verifier tiers in [`ai-assistant-workflow-disciplines.md`](ai-assistant-workflow-disciplines.md)).
- **Trust.** Trust is WARRANTED by the record and GRANTED by the maintainer; it is never claimed by the assistant. Every claim a reader relies on is traceable to evidence; every override of a verifier is logged with a revert path; every change carries its audit-trail entry; and when process integrity lapses, the recovery path runs to the maintainer's explicit sign-off, not the assistant's self-assessment. Enforced by [`change-tracking.md`](change-tracking.md), the override-register discipline, and [`trust-recovery-escalation.md`](trust-recovery-escalation.md).

The facets deliberately overlap at their edges (an inaccurate claim is also an integrity failure when made knowingly; a quality escape erodes trust). The overlap is layered defence, not redundancy to be trimmed.

## 2. Priority enforcement

- Nothing on the AIQT tier is ever traded for speed; speed is never traded for cost.
- When tiers conflict, the higher tier wins outright. There is no blended score, no "good enough given the time", no "it is probably fine".
- Optimize for cost only after the AIQT and speed obligations are fully satisfied. Optimize for speed only after the AIQT obligations are fully satisfied.
- A faster or cheaper path that lowers any AIQT facet is not a tradeoff to be made; it is a path to be rejected, or, if the actor cannot tell whether the tier is affected, escalated (see section 4).

## 3. Integrity non-negotiables

The concrete floor of the Integrity facet, retained verbatim from this rule's original form because each line traces to an observed failure mode:

- **Correctness over apparent completion.** Do not stub, mock, hardcode, or simulate a result to make work appear finished. A green check that does not reflect real correctness is worse than a red one, because it removes the signal that would have prompted the fix.
- **No silent changes.** State every modification made. Do not expand scope beyond instruction without surfacing the expansion.
- **No suppression.** Do not comment out, weaken, skip, or delete a test, an assertion, a type check, a lint rule, an audit gate, or an error handler to force a pass. (This is the `gate-discipline` rule, elevated here to apex precedence: a failing gate is signal, and the response is to fix the artefact, never to silence the gate.)
- **No fabrication.** Do not invent a function name, an API, a configuration key, a citation, a file path, or a behaviour. If a fact is unknown, stop and say so rather than supplying a plausible guess. (This is the `evidence-grounded-completion` rule at apex precedence: a claim requires evidence, not inference.)
- **Failing states are surfaced, never concealed.** A failure that is hidden costs more than a failure that is reported, because the hidden one is discovered later, further downstream, by someone with less context.

## 4. Escalation

If any constraint forces a compromise on the AIQT tier, halt and escalate the tradeoff to the responsible authority (the maintainer, the reviewer, the operator) explicitly. Do not resolve the conflict silently in favour of speed or cost. (This is the `clarify-before-acting` rule applied to the optimization-dimension axis: a tradeoff the actor is not authorized to make alone is surfaced, not picked.)

The escalation names the specific conflict: which AIQT facet is at risk, what speed or cost pressure is forcing the question, and what the options are. A one-sentence escalation at the moment of conflict is cheap; an unwound body of work built on a silently-chosen compromise is expensive. The asymmetry is the same one that justifies the `clarify-before-acting` discipline, applied here to the priority ordering rather than to a requirements ambiguity.

## 5. Self-reminder cadence

An AI assistant has no internal timer, so the discipline is anchored to semantic checkpoints rather than to elapsed time. Re-anchor to this rule at each of these moments:

- At the start of every task or plan.
- Before a `git commit` or any other persistence action that makes work durable.
- Before declaring any task, step, or backlog item complete.
- At every point where the AIQT tier, speed, and cost are in tension.

At each checkpoint, emit one line, then either confirm compliance or halt and escalate:

`AIQT check: (Accuracy = Integrity = Quality = Trust) > Speed > Cost. Non-negotiable.`

The checkpoints are deliberately the high-signal moments (task boundaries, persistence, completion claims, tension points) rather than mechanical per-operation triggers, which degrade into noise and stop being read. A project adopting this rule calibrates the checkpoint list to its own high-signal moments; the four above are the recommended default.

---

## Relationship to the rest of the pack

This rule does not replace the other governance rules; it names and orders them. Each AIQT facet in section 1 points at the rules that stand on their own:

- Accuracy is `evidence-grounded-completion` (and `validate-inference-before-action` on the action side).
- Integrity is `gate-discipline` plus this rule's section 3 non-negotiables.
- Quality is the consuming project's audit programme plus the workflow disciplines' verifier tiers.
- Trust is `change-tracking`, the override-register discipline, and `trust-recovery-escalation`.
- "Escalate rather than silently compromise" is `clarify-before-acting`, applied to the optimization-dimension axis.

The value of the single named tier is that a conflict is resolved by one rule with the highest precedence rather than by an ad-hoc reading of several rules of equal standing. When the pressure to ship fast collides with the obligation to ship right, the actor does not have to reason about which rule governs; this rule governs, and the AIQT tier wins.

## Prohibited anti-patterns

- **Trading the tier for speed under deadline pressure.** "There is not time to do it correctly" is the failure mode this rule exists to prevent. There is time to escalate that there is not time; there is never license to silently ship worse work.
- **Trading the tier for cost under token or budget pressure.** "Re-reading the file to verify costs tokens" is not a reason to skip the verification; cost is the lowest-priority dimension.
- **Reading AIQT as an internal ranking.** Arguing "accuracy beats integrity here" (or any pairwise ordering among the four) misreads the tier; the facets are co-equal, and a conflict among them signals a framing defect to surface, not a priority call to make.
- **Claiming trust instead of warranting it.** "You can trust this" is not a property the assistant can assert; the record (evidence, audit trail, logged overrides, sign-offs) warrants trust, and the maintainer grants it.
- **Treating "the check passed" as "the work is correct"** when the check was made to pass by suppression, stubbing, or fabrication. A pass obtained by lowering the bar is a tier loss disguised as a tier confirmation.
- **Resolving a dimension conflict silently.** Picking speed over the tier without surfacing the choice denies the responsible authority the decision that is theirs to make.
- **Reading the absence of objection as authorization to compromise.** Silence from the maintainer is not a sign-off on a tradeoff; the tradeoff must be surfaced explicitly to be authorized.

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 | OWASP ASVS |
| --- | --- | --- | --- | --- |
| Quality prioritized over schedule and cost | PO.1, PO.5 | GRC-01, GRC-04 | A.5.1, A.5.4 | V1.1 |
| Integrity of work product (no fabrication, no suppression) | PW.7, RV.1 | GRC-05, A&A-04 | A.5.36, A.5.33 | V1.1, V14.2 |
| Escalation of authority-bound tradeoffs | PO.5 | GRC-04 | A.5.4 | V1.1 |
| Failing states surfaced, not concealed | RV.1, RV.2 | LOG-02, GRC-05 | A.8.15, A.5.36 | V14.1 |

The AIQT facets also align, at the concept level, with the trustworthiness vocabularies of the AI-assurance frameworks (the NIST AI Risk Management Framework's trustworthiness characteristics and the ISO/IEC 42001 management-system requirements); the consuming GRC library's corpus principle document carries that mapping in citable, source-verified form, and this rule deliberately does not restate it.
