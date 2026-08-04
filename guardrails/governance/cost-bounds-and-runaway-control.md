# Cost Bounds and Runaway Control

The apex rule of this pack, [`project-integrity`](project-integrity.md), names Cost as the lowest of its optimization dimensions: (Accuracy = Integrity = Quality = Trust) > Progress > Speed > Cost. A pack that ranks Cost last still needs a rule that governs it, for the same reason a budget that is never written down is a budget that is silently overspent. This rule is that governance: it bounds token and compute spend, runaway agentic loops, unbounded fan-out, and the cost of the pack's own verification layers, WITHOUT ever trading down the AIQT tier to do so.

The frame matters, because a naive cost rule in a pack whose apex rule calls Cost lowest-priority reads as self-contradictory. The resolution is the same shape [`project-integrity`](project-integrity.md) §2a gives Progress: **Cost targets the waste axis, never the assurance axis.** Progress is decisiveness and never shortens verification; Cost is the elimination of waste and never shortens verification either. A cost limit is inevitable in any real system (a token budget, a rate cap, a wall-clock deadline); this rule governs WHERE that limit is allowed to bind, a planned escalation at the boundary, never a silent mid-apply degradation of quality. Spending less is not the goal; spending only on what advances the work, and surfacing the moment a limit would force an AIQT compromise, is.

This rule applies to human developers and to AI coding assistants. It binds more often on AI assistants, because the failure mode it prevents (a runaway loop, an unbounded fan-out, or a quiet model-downgrade to save tokens) is exactly what an assistant under budget pressure reaches for.

---

## 1. What is bounded, and what is never bounded

Bounded (this rule's subject): token and compute budgets; the number of iterations of any repeating construct (retry loops, verify-fix loops, polling loops); the breadth of parallel fan-out and the depth of recursion and work queues; and the cost of the pack's own dual-family and high-assurance verification layers.

Never bounded to save cost: the correctness of a result; the completeness of a mandatory verification; the disposition of a finding; the honesty of a claim. These are AIQT-tier properties, and Cost sits four tiers below them. When a cost limit and an AIQT-tier obligation collide, the limit yields and the obligation is met, or the conflict is escalated (section 7); the obligation is never quietly dropped to fit the budget.

The test at every cost decision: "does this bound eliminate waste, or does it reduce assurance?" The first is this rule's job; the second is forbidden by it.

## 2. Declare the budget, and make consumption observable

A bound that is not written down is not a bound. Where a unit of work carries a budget (a token target, a compute ceiling, a time box), declare it before the work begins, and make consumption observable as the work proceeds, so that approaching the limit is visible before it is hit rather than discovered at a hard stop.

- **State the budget and its unit.** "This pass has a 500k output-token target" is a budget; "keep it cheap" is not.
- **Measure, do not estimate, spend against it.** Where the toolchain instruments consumption, read the instrument; where it does not, say so and treat the figure as an estimate, never presenting an estimate as a measurement (the [`evidence-grounded-completion`](evidence-grounded-completion.md) never-sum-measured-with-estimated discipline).
- **Surface the approach to the limit, not only the breach.** The value of an observable budget is that it lets a planned escalation happen at the boundary; a budget observed only at exhaustion has already forced the mid-apply hard stop this rule exists to avoid.

## 3. Cap every repeating construct

Every loop, retry, poll, and verify-fix cycle carries an explicit maximum. An unbounded `until` or `while` that depends on an external condition flipping is a defect: when the condition never flips, the loop never exits, no result is produced, and silence becomes indistinguishable from progress.

- **Retry loops** carry a maximum attempt count and diagnose the mechanism before re-attempting, per the repeated-failure circuit-breaker in [`validate-inference-before-action`](validate-inference-before-action.md): a byte-identical retry is the same attempt, not a new one.
- **Verify-fix loops** carry an iteration cap (the [`ai-assistant-workflow-disciplines`](ai-assistant-workflow-disciplines.md) three-iteration cap is the reference); when a finding is unresolved at the cap, the work stops and is escalated, not forced through with a further un-budgeted round.
- **Polling loops** are bounded by a maximum attempt count and a hard timeout, and are fail-loud, per the API-polling guardrails in [`evidence-grounded-completion`](evidence-grounded-completion.md); prefer a wake-on-event subscription over polling entirely.

A cap is not a licence to stop short of a mandatory obligation. Where the capped loop is the mechanism of a required verification, hitting the cap is an escalation trigger (section 7), never a silent acceptance of the unverified state.

## 4. Bound fan-out, recursion, and queue depth

Parallel breadth, recursive depth, and work-queue length each multiply cost, and each has a runaway failure mode.

- **Fan-out is bounded by an explicit concurrency cap and a maximum item count.** Fanning a task across a verified-disjoint partition is legitimate (the partitionable-work default in [`ai-assistant-workflow-disciplines`](ai-assistant-workflow-disciplines.md)); fanning it across an unbounded or unverified set is a runaway. Where a fan-out is capped and the real set is larger, the cap is stated and the dropped remainder is named, never silently truncated.
- **Recursion carries a depth limit**, and a self-invoking process (an agent that spawns agents, a workflow that runs workflows) carries an explicit nesting bound, so a crafted input cannot run the depth up without limit.
- **Queues are bounded**, and a queue filled beyond the live capacity that will serve it goes stale unserved and misreports its own depth; fill the capacity that exists, not an unbounded backlog.

## 5. The verification layers are costed by risk, and cut last

This pack's dual-family verification and high-assurance harness are its most expensive layers, and the temptation under budget pressure is to cut them first. That inverts the tier ordering: the verification layers protect the AIQT tier, so they are costed by the risk of the change, and they are the LAST thing cut, not the first.

- **Scale the verification to the change, not to the budget.** The tiered standard in [`ai-assistant-workflow-disciplines`](ai-assistant-workflow-disciplines.md) (no standing verifier for pure bookkeeping; a dual-family pair for substantive work; the full harness for the sensitive tier) is a risk calibration, not a cost one; apply it by the change's risk, and a genuinely low-risk change legitimately costs little to verify.
- **A budget that would force a mandatory verification to be skipped is a budget conflict, not a verification decision** (section 7). Throughput pressure never authorizes abbreviating a mandatory QA step; that is the [`ai-assistant-workflow-disciplines`](ai-assistant-workflow-disciplines.md) anti-abbreviation standard, and it is a cost-tier obligation as much as a quality one.
- **The one sanctioned cost exception is external unavailability, and it carries a make-up obligation.** The dual-family standard's token-unavailability carve-out (when one model family's account is exhausted, the available family runs alone, the gap is noted, and the missing family re-runs when tokens return) generalizes to a three-property template: a cost exception is legitimate only when it is (a) forced by an external unavailability rather than chosen to save spend, (b) recorded at the point it is taken, and (c) paired with a named make-up obligation that is discharged when the constraint lifts. All three properties are required; an exception that is chosen rather than forced, or unrecorded, or open-ended, is a silent degradation wearing an exception's costume.

## 6. Cheap-first, where the saving is free

Cost is optimized only after the AIQT, Progress, and Speed obligations are met; within that space, prefer the cheaper path when it costs nothing on the higher tiers.

- **Compute a findable fact rather than dispatching for it**, and validate an inferred premise with one cheap tool call rather than acting on it and paying the cascade (the compute-first and validate-before-action disciplines); the cheap check is both cheaper and more correct.
- **Do not re-verify what a deterministic gate already proves**, and do not re-run a settled mechanical check for reassurance; add a verification layer for its assurance value, not as a ritual.
- **A model or path downgrade to save cost is forbidden the instant it touches an assurance verdict.** A production cost-governance standard may name "downgrade to a cheaper model on a ceiling breach" as a normal response, correctly, for a runtime feature; this rule diverges deliberately on the pack's own verification work, where a cheaper-model substitution on a verifier, a validator, or a judge is exactly the silent quality trade-down the AIQT tier forbids. Cheap-first governs the work; it never governs the assurance of the work.

## 7. Escalate rather than degrade, and budget exhaustion is a named wind-down trigger

When a cost limit would force a compromise on the AIQT tier, halt and escalate the tradeoff to the responsible authority, naming the specific conflict, exactly as [`project-integrity`](project-integrity.md) §4 requires for any tier conflict. Do not resolve it silently in favour of Cost. A one-sentence escalation at the moment of conflict is cheap; an unwound body of work built on a silently-chosen cost compromise is not.

Budget exhaustion is itself a named, externally-observable signal, so it is a legitimate wind-down trigger under [`session-lifecycle`](session-lifecycle.md) §4 (which requires a named signal, never an un-instrumented sense of "enough"). A run that reaches its declared budget winds down cleanly on that signal, landing its work in a green, recorded state, rather than pushing past the budget silently or stopping mid-apply. This is an extension of that rule's trigger set, not a new discipline: an exhausted declared budget is as observable as a failing check.

---

## Prohibited anti-patterns

- **Cutting a mandatory verification to fit a budget.** The verification protects the AIQT tier; the budget is four tiers below it. Escalate the conflict; never drop the obligation.
- **Downgrading a verifier, validator, or judge to a cheaper model to save tokens.** A silent quality trade-down on an assurance verdict, forbidden even though a runtime feature may downgrade legitimately.
- **An unbounded loop, poll, recursion, or fan-out.** Silence becomes indistinguishable from progress; every repeating construct carries an explicit maximum.
- **A budget that is never declared.** An undeclared budget is silently overspent, and its approach is invisible until the hard stop.
- **Presenting an estimated spend as a measured one.** A ratio or total of a measurement and an estimate is an estimate, however many digits it prints.
- **Silently truncating a capped set.** A cap is stated and the dropped remainder is named; a silent top-N reads as full coverage.
- **Retrying a byte-identical attempt after a repeated failure.** The same attempt is not a new one; diagnose the mechanism before re-attempting.
- **Forcing a finding through at the verify-fix cap.** The cap reached is an escalation trigger, not a licence to ship the unresolved change.
- **Taking a cost exception that is chosen, unrecorded, or open-ended.** The only sanctioned exception is externally forced, recorded, and paired with a discharged make-up obligation, all three.
- **Pushing past a declared budget silently.** An exhausted budget is a named wind-down signal; wind down cleanly on it rather than overspending in silence.
- **Ritual re-verification.** Re-running a settled deterministic check for reassurance spends cost with no assurance gain; add a layer for its value, not as habit.
- **Treating "cheaper" as a reason on its own.** Cost is optimized only after the higher tiers are satisfied; a cheaper path that lowers any AIQT facet is rejected, not chosen.

## Relationship to the rest of the pack

This rule is the Cost-tier counterpart to the discipline [`project-integrity`](project-integrity.md) §2a gives Progress and Speed: each throughput-or-efficiency value gets a rule that bounds it WITHOUT letting it touch the assurance axis. It composes with, and does not restate:

- [`project-integrity`](project-integrity.md) fixes the tier ordering (Cost lowest) and the escalate-rather-than-silently-compromise discipline; this rule applies both to the Cost dimension specifically.
- [`validate-inference-before-action`](validate-inference-before-action.md) supplies the repeated-failure circuit-breaker (bounded retries) and the compute-first cheap-check; this rule generalizes them to every repeating construct.
- [`ai-assistant-workflow-disciplines`](ai-assistant-workflow-disciplines.md) supplies the verify-fix iteration cap, the partitionable-fan-out default, the tiered-verification risk calibration, the dual-family token-unavailability exception, and the anti-abbreviation standard; this rule reads them as cost obligations, not only quality ones.
- [`session-lifecycle`](session-lifecycle.md) supplies the named-signal wind-down; this rule adds budget exhaustion to its trigger set.
- [`evidence-grounded-completion`](evidence-grounded-completion.md) supplies the bounded-fail-loud polling guardrails and the never-sum-measured-with-estimated discipline; this rule leans on both for observable budgets.

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 | OWASP ASVS |
| --- | --- | --- | --- | --- |
| Bounded consumption of costly resources | PO.5 | I&S-02 | A.8.6 | V2.4 |
| Runaway-loop and fan-out control | PO.5, RV.1 | I&S-02 | A.8.6, A.8.16 | V2.4 |
| Verification proportional to risk (not to budget) | PO.5, RV.1 | GRC-05 | A.5.36 | V15.1 |
| Escalation of a budget-forced tier conflict | PO.5 | GRC-04 | A.5.4 | V15.1 |

OWASP ASVS V2.4.1 (Anti-automation) is the closest verbatim anchor: it requires controls "to protect against excessive calls to application functions that could lead to ... quota exhaustion, rate-limit breaches, denial-of-service, or overuse of costly resources." CSA CCM I&S-02 is "Capacity and Resource Planning." NIST SSDF has no dedicated cost or capacity practice, so the PO.5 planning mapping is by analogy rather than a tight fit, stated here rather than forced. The rule expresses the same audit-trail-integrity principle as the rest of the pack, at the cost boundary: a bound reached must be traceable to a declared budget and a named escalation, never to a silent compromise discovered downstream.
