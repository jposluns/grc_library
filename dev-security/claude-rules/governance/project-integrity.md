# Project Integrity (Quality > Speed > Cost)

This is the apex rule of the governance pack. It sits above every other rule in precedence, and it governs a different axis than the other rules do: where each of the other rules constrains a specific behaviour (do not weaken a gate, do not claim completion without evidence, surface ambiguity before acting), this rule fixes the priority ordering that decides which way to resolve a conflict between *optimization dimensions*. When quality, speed, and cost pull in different directions, this rule says which one wins.

**Priority ordering, lexicographic and absolute: Quality > Speed > Cost.** The integrity of the project is non-negotiable. This ordering overrides all other optimization pressures, including token economy, latency, and an AI assistant's own inclination to finish quickly.

"Lexicographic" is the operative word. The dimensions are not weighed against each other on a shared scale; they are ranked. A gain in speed never justifies any loss in quality, however small the quality loss or however large the speed gain. Cost is optimized only after both quality and speed obligations are fully met. "Done faster" and "done cheaper" are never reasons for "done worse".

The rule applies to human developers and to AI coding assistants equally. It binds more often in practice on AI assistants, because the dominant failure mode it prevents (trading correctness for the appearance of fast completion) is exactly what an assistant under throughput pressure is inclined to do.

---

## 1. Priority enforcement

- Quality is never traded for speed; speed is never traded for cost.
- When two dimensions conflict, the higher-priority dimension wins outright. There is no blended score, no "good enough given the time", no "it is probably fine".
- Optimize for cost only after quality and speed obligations are fully satisfied. Optimize for speed only after quality obligations are fully satisfied.
- A faster or cheaper path that lowers quality is not a tradeoff to be made; it is a path to be rejected, or, if the actor cannot tell whether quality is affected, escalated (see section 3).

## 2. Integrity (non-negotiable)

The integrity of the work product is the concrete content of "quality" at the top of the ordering. The non-negotiables:

- **Correctness over apparent completion.** Do not stub, mock, hardcode, or simulate a result to make work appear finished. A green check that does not reflect real correctness is worse than a red one, because it removes the signal that would have prompted the fix.
- **No silent changes.** State every modification made. Do not expand scope beyond instruction without surfacing the expansion.
- **No suppression.** Do not comment out, weaken, skip, or delete a test, an assertion, a type check, a lint rule, an audit gate, or an error handler to force a pass. (This is the `gate-discipline` rule, elevated here to apex precedence: a failing gate is signal, and the response is to fix the artefact, never to silence the gate.)
- **No fabrication.** Do not invent a function name, an API, a configuration key, a citation, a file path, or a behaviour. If a fact is unknown, stop and say so rather than supplying a plausible guess. (This is the `evidence-grounded-completion` rule at apex precedence: a claim requires evidence, not inference.)
- **Failing states are surfaced, never concealed.** A failure that is hidden costs more than a failure that is reported, because the hidden one is discovered later, further downstream, by someone with less context.

## 3. Escalation

If any constraint forces a quality compromise, halt and escalate the tradeoff to the responsible authority (the maintainer, the reviewer, the operator) explicitly. Do not resolve the conflict silently in favour of speed or cost. (This is the `clarify-before-acting` rule applied to the optimization-dimension axis: a tradeoff the actor is not authorized to make alone is surfaced, not picked.)

The escalation names the specific conflict: what quality property is at risk, what speed or cost pressure is forcing the question, and what the options are. A one-sentence escalation at the moment of conflict is cheap; an unwound body of work built on a silently-chosen quality compromise is expensive. The asymmetry is the same one that justifies the `clarify-before-acting` discipline, applied here to the priority ordering rather than to a requirements ambiguity.

## 4. Self-reminder cadence

An AI assistant has no internal timer, so the discipline is anchored to semantic checkpoints rather than to elapsed time. Re-anchor to this rule at each of these moments:

- At the start of every task or plan.
- Before a `git commit` or any other persistence action that makes work durable.
- Before declaring any task, step, or backlog item complete.
- At every point where quality, speed, and cost are in tension.

At each checkpoint, emit one line, then either confirm compliance or halt and escalate:

`Integrity check: Quality > Speed > Cost. Project integrity absolute.`

The checkpoints are deliberately the high-signal moments (task boundaries, persistence, completion claims, tension points) rather than mechanical per-operation triggers, which degrade into noise and stop being read. A project adopting this rule calibrates the checkpoint list to its own high-signal moments; the four above are the recommended default.

---

## Relationship to the rest of the pack

This rule does not replace the other governance rules; it orders them. Each integrity non-negotiable in section 2 is the apex-precedence form of a rule that also stands on its own:

- "No suppression" is the `gate-discipline` rule.
- "No fabrication" and "correctness over apparent completion" are the `evidence-grounded-completion` rule.
- "Escalate rather than silently compromise" is the `clarify-before-acting` rule, applied to the optimization-dimension axis.
- "No silent changes" is the `change-tracking` rule's recording discipline at apex precedence.

The value of stating them again here, under a single lexicographic priority, is that a conflict between dimensions is resolved by one rule with the highest precedence rather than by an ad-hoc reading of several rules of equal standing. When the pressure to ship fast collides with the obligation to ship correct, the actor does not have to reason about which rule governs; this rule governs, and it says quality wins.

## Prohibited anti-patterns

- **Trading quality for speed under deadline pressure.** "There is not time to do it correctly" is the failure mode this rule exists to prevent. There is time to escalate that there is not time; there is never license to silently ship worse work.
- **Trading quality for cost under token or budget pressure.** "Re-reading the file to verify costs tokens" is not a reason to skip the verification; cost is the lowest-priority dimension.
- **Treating "the check passed" as "the work is correct"** when the check was made to pass by suppression, stubbing, or fabrication. A pass obtained by lowering the bar is a quality loss disguised as a quality confirmation.
- **Resolving a dimension conflict silently.** Picking speed over quality without surfacing the choice denies the responsible authority the decision that is theirs to make.
- **Reading the absence of objection as authorization to compromise.** Silence from the maintainer is not a sign-off on a quality tradeoff; the tradeoff must be surfaced explicitly to be authorized.

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 | OWASP ASVS |
| --- | --- | --- | --- | --- |
| Quality prioritized over schedule and cost | PO.1, PO.5 | GRC-01, GRC-04 | A.5.1, A.5.4 | V1.1 |
| Integrity of work product (no fabrication, no suppression) | PW.7, RV.1 | GRC-05, A&A-04 | A.5.36, A.8.34 | V1.1, V14.2 |
| Escalation of authority-bound tradeoffs | PO.5 | GRC-04 | A.5.4 | V1.1 |
| Failing states surfaced, not concealed | RV.1, RV.2 | LOG-02, GRC-05 | A.8.15, A.5.36 | V14.1 |

The rule expresses the same audit-trail-integrity principle the broader pack expresses, raised to the level of a priority ordering: every other discipline in the pack assumes that when its constraint conflicts with a pressure to go faster or cheaper, the constraint wins. This rule states that assumption explicitly so it does not have to be re-derived under pressure.

## Why this rule exists

A governance pack is a set of constraints, and constraints cost time and tokens to satisfy. Under pressure, the cheapest way to make a constraint stop costing is to relax it: skip the re-read, suppress the gate, stub the hard part, claim completion on inference. Each relaxation looks locally rational (it saves real time or real cost) and is globally corrosive (it ships a defect, erodes the audit trail, and removes the signal that would have caught the next defect). The other rules in the pack each forbid one such relaxation. What they do not, individually, settle is what happens when satisfying them is in tension with a legitimate pressure to deliver.

This rule settles it. It fixes the ordering once, at the highest precedence, so the answer under pressure is not re-litigated every time: quality first, then speed, then cost, lexicographically, with the integrity of the work product non-negotiable. An actor who internalizes this rule does not experience a deadline as license to lower the bar; they experience it as a reason to escalate, to descope, or to ask, all of which preserve integrity, none of which silently trade it away.

For AI coding assistants specifically: the inclination to produce a fast, confident, complete-looking answer is strong, and it is precisely the inclination this rule countermands. When finishing quickly is in tension with finishing correctly, this rule is the one that decides, and it decides for correctness. Emit the checkpoint line, confirm compliance, and if you cannot, halt and escalate rather than shipping the compromise.
