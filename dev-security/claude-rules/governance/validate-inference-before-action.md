# Validate Inference Before Action

When the next action depends on an inferred premise (a claim about state that has not been directly observed in the current turn), validate the premise before taking the action. The validation is a tool call, a file read, or another concrete observation that confirms or refutes the inference. Acting on an unvalidated inference propagates: if the inference is wrong, the action is wrong, and any downstream work that depends on the action is wrong. The cascade cost compounds.

This rule is the action-side counterpart of the evidence-grounded-completion rule. That rule catches the failure at the assertion site ("I claim X is true" without evidence). This rule catches the failure at the action site ("I will skip / choose / proceed because X is true" without evidence). The trigger surfaces differ; the discipline is the same.

The rule applies to human developers and to AI coding assistants equally. AI assistants face the discipline more often because the failure mode (inferring a state that justifies a shortcut, then taking the shortcut without checking) is the dominant pattern when an assistant feels pressure to make progress.

---

## What an inferred premise looks like

An inferred premise is a claim about state where the next action depends on the claim being true, and the claim has not been directly observed in the current turn. Examples of the surface:

- "The previous sweep covered this scope, so the current sweep can skip subagent C." (Premise: nothing changed in C's scope since the prior sweep. Inferred; not observed in this turn.)
- "Nothing material changed since last commit, so the audit will pass." (Premise: no relevant change since the prior audit. Inferred.)
- "The user said X earlier, so they want Y now." (Premise: prior consent extends to the current scope. Inferred.)
- "This file is the same as last time, so I don't need to re-read it." (Premise: file state unchanged. Inferred.)
- "All occurrences are in this one file, so the fix is complete." (Premise: no parallel occurrences elsewhere. Inferred.)
- "The test passed last time and only a comment changed, so I can skip re-running." (Premise: comment-only change has no behavioural effect. Inferred.)

The trigger pattern in writing: clauses of the form "since/because/given X, [action]" where X is a state claim that has not been observed in the current turn. When that pattern appears in the draft, the rule fires.

---

## The discipline

When an action depends on an inferred premise:

1. **Identify the inference.** Pause at the surface clause ("since/because/given X, [action]") and name X. If the writer cannot name X precisely, the premise is too vague to act on; refine before continuing.
2. **Cost the validation.** A validation is one or two tool calls: a file read, a `grep`, a `git status`, a status API call. Each takes seconds. The cost of an unvalidated inference cascading into a wrong action is usually orders of magnitude larger.
3. **Validate.** Take the tool call that would confirm or refute the inference. Read the result.
4. **Act on the validated observation.** The action's premise is now grounded. The clause becomes "since X [validated by Y], [action]" rather than "since X [inferred], [action]".

The validation must be a concrete observation, not another inference. "I assume X because last time Y" is not a validation; it is a second inference resting on the first.

---

## Anti-patterns

- **Skipping a subagent, a test, or a gate "because the prior run covered it".** The prior run is not the current state. Validate by checking what changed.
- **Treating "this looks like a simple change" as evidence the audit will pass.** The audit's view of "simple" differs from the writer's; validate by running the audit.
- **Assuming "this fix is complete" because the named occurrence is fixed.** Other parallel occurrences may exist; validate by greping for the pattern.
- **Treating a prior approval as durable when the scope has changed.** Re-confirm the approval covers the current scope.
- **Acting on a screenshot or quote from a prior turn as if it were current state.** State drifts between turns; validate by re-reading.
- **Substituting a confident assertion for a tool call.** "Surely X" without the tool call is the failure mode the rule prevents.
- **Validating one occurrence and inferring the rest.** If finding one stale `N gates` reference (where `N` is an out-of-date count) suggests the pattern may exist elsewhere, the validation is a corpus-wide search, not "I'll just fix this one and hope".

---

## The repeated-failure circuit-breaker

When the same action has been blocked or has failed in the same way two or more times in a row, the premise that the next attempt will fare differently is itself unvalidated, and retrying on it is this rule's cascade in its most acute form: a retry loop. Before any further attempt, stop and write a concrete mechanism diagnosis: (1) what literally failed, the exact error or block, quoted; (2) the exact fix the failure calls for; and (3) how this attempt differs, byte for byte, from the blocked one. A retry whose command or input is byte-identical to the blocked one is the same attempt, not a new one, and it fails the same way. A common mechanism is editing the description of an action while leaving the action itself unchanged.

Do not attribute the loop to session length, context depth, or degradation as a first move: those are un-observable states (see [`evidence-grounded-completion`](evidence-grounded-completion.md), "Un-observable state is never assertable"), never a valid diagnosis. Diagnose the mechanism. If, after diagnosing the mechanism, a degradation hypothesis is still to be raised, it must rest on a named, externally-observable signal (a compaction event, a quoted self-inconsistency, a failing check), recorded and assessed, not asserted.

---

## Tool-specific guidance for AI coding assistants

### Inference triggers in drafts

When the draft contains "since / because / given / per / per the / based on / following / according to" followed by a state claim, the rule fires. Pause and identify whether the state claim has been observed in the current turn. If not, validate.

### Cheap-validation defaults

Most validations are cheap. The recurring shapes:

- `git status` / `git diff` for "what changed".
- `grep` / `Grep` for "are there parallel occurrences".
- File read for "what does this file actually say now".
- Status API call for "what is the current state of this resource".
- Re-running a check for "does the audit still pass".

Each is one tool call, typically seconds. The cost is bounded; the cascade cost is unbounded.

### When the validation contradicts the inference

If the validation refutes the inferred premise, the planned action was wrong. Replan from the validated observation. Do not partially adjust the action; replan.

### Recording the validation

When a sweep, an audit, or any structured cycle includes the validation step, the validation result is recorded alongside the action so a future reader can trace the chain. The validation-sweep skill's Rule 5.6 (dispatch declaration in the register) is one such mechanism: a silent skip cannot be reconstructed later, so the register entry must declare what was validated.

### Inference inside a subagent

A subagent's pre-tool verification preamble (state hypothesis / falsifier / prior result before each tool call) is the per-call form of this rule. The current rule is the broader form: it fires not just before tool calls within a subagent, but at every decision an orchestrator makes between actions.

---

## Exception-handling protocol

There is no general exception. The rule's value is unconditional.

The narrowest legitimate carve-out is the case where the action is fully reversible and the validation cost approaches the action cost. Example: re-reading a file is itself a tool call; if the next action is also a single tool call against the same file, the validation and the action collapse. In that case, the action is its own validation.

The other narrow case is when the orchestrator has just observed the state in the current turn and is using that observation. The current-turn observation is the validation; the rule has already fired and been satisfied.

Any other "we can skip the validation because..." is the failure mode the rule exists to prevent. The exception is itself an inference that would need its own validation; do not regress.

---

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 | OWASP ASVS |
| --- | --- | --- | --- | --- |
| Validated premise before action | RV.1, RV.2 | GRC-05, LOG-02 | A.5.36, A.8.15 | V1.1, V14.1 |
| Cascade prevention discipline | PO.5 | GRC-04 | A.5.4 | V1.1 |
| Audit trail of validations | PS.1, RV.2 | LOG-02, LOG-04, LOG-10 | A.8.15, A.5.36 | V14.1 |
| Diagnosis before retry after repeated failure | RV.1, RV.2 | GRC-05 | A.5.36 | V14.1 |

The discipline implements the same audit-trail-integrity principle the broader pack expresses: every action driven by a premise must be traceable to a validation of the premise. The cost of an unvalidated premise compounds; the cost of one extra tool call does not.
