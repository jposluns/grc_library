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

## Guard inputs: a correct check on an unsound input

A guard is a premise-driven action, so this rule reaches it: `if P(x): refuse` acts on the premise that `x` represents the thing `P` is asking about. The failure this section names is a guard whose logic is right and whose INPUT cannot answer the question asked of it. The guard then does its job perfectly on a value that does not mean what the code believes it means.

The failure hides from the usual instrument, and the scope of that blindness is worth stating precisely, because the loose version of this claim contradicts its own remedy. Mutating the DECISION verifies that `P` fires correctly GIVEN `x` and says nothing about whether `x` is faithful. Mutating the OBSERVER can say something, so the blindness is not structural, and a rule claiming otherwise would make its own "mutate the observer" advice incoherent.

**But observer mutation is bounded by the same case coverage as decision mutation, and that is the part a reader will underestimate.** It detects only what some case already discriminates on. Measured against a real defect: of three observer-mutation strategies applied to a live one (an entry missing from a runtime-to-family map), only one was detected; the two that mapped most directly onto the actual defect, dropping the entry and returning the wrong key, BOTH missed it, because the test had no case for that entry at all, so no mutation involving it could ever fail. So observer mutation is a companion to the reality-fixture practice below, never a substitute for it: where no case discriminates, no mutation of either kind can help.

A guard can therefore be mutation-proved, documented, and still be worthless, and the proof will read as reassurance.

The recurring shape is **a proxy standing in for the real question**, where nobody asked whether the source is authoritative for what is being asked of it. Three observed instances, which share one shape:

| Guard input | Its source | Why the source cannot answer |
| --- | --- | --- |
| which process occupies this session | a per-run process id | the id encodes nothing about the session it runs in |
| is this file complete | the file exists | existence is not completeness |
| is this worker still working | its heartbeat | the heartbeat and the work loop are separate code paths, so one survives the other |

### The discipline

- **Ask the authority question for every consequential guard.** Not "is this value correct" but "can this source, even in principle, answer the question I am asking of it?" A per-run identifier cannot answer "where is it running"; no amount of careful coding fixes that, and the answer is to change the input rather than harden the check. This question is cheap, and it is the one that catches the class.
- **Make "I don't know" a first-class return value, and make ignorance refuse.** This is the highest-value structural change. An observer with two outcomes for three real states must encode ignorance as one of the two, and the permissive one is the usual choice, which is how ignorance becomes a silent permit. An observer feeding a consequential guard should be able to return an explicit unknown, and every caller must handle it: a destructive action proceeding on an unknown gate is the defect, and refusing on an unknown gate is the fix. Scope the conservatism so it stays proportionate, because a guard that refuses far too broadly is one somebody switches off.
- **Keep a reality fixture for every observer defect found.** When an observation is found unsound, capture the ACTUAL state that exposed it, verbatim, as a permanent test fixture with the correct verdict recorded. This is the only technique that tests an observer against the world rather than against the author's model of it, and it costs one fixture per defect. Never paraphrase the state into something tidier; the tidying is where the defect hides.
- **Mutate the observer, not only the decision.** Extend the mutation discipline past `if` statements: drop a field the mapping should carry, collapse two cases it should distinguish, return the wrong key, and confirm the test notices. An observer mutation that changes nothing observable is the same finding as an undetectable guard, and it is reported the same way.
- **Where a proxy is unavoidable, state in the artefact what it does NOT establish.** A documented proxy whose residue is written down and whose failure direction is safe is a legitimate engineering choice; an undocumented one invites the next reader to trust it further than it earns. Name the residue at the point of use, and prefer the failure direction that refuses.
- **Separate observation from decision in the code.** A pure decision function driven by constructed facts, with a thin observer that gathers and decides nothing, makes both halves testable: the decision by mutation, the observer by reality fixtures. Where the two are entangled, neither is properly reachable.

### A mutation harness is itself an instrument, and an unverified one produces false findings

The discipline above leans on mutation testing to bound a guard. That makes the HARNESS a measuring instrument, and an instrument nobody calibrated reports confidently wrong answers. Three observed failures in a single day, all from ad-hoc harnesses written to check a specific guard:

- **A non-mutation read as a coverage gap.** The edit changed a string literal no assertion reads, and separately performed a consistent rename. Neither can change behaviour, so the test passed, and the passing test was reported as NOT DETECTED, which reads exactly like a missing case.
- **A harness logic bug inverting every verdict.** Its collection step relied on a call whose return value was truthy, so a short-circuit gathered every candidate into the failure list. It reported all nine guards undetected when all nine were detected.
- **A degenerate return read as a finding.** A real function was called with an input too small to satisfy its preconditions, returned empty, and the empty result was read as evidence that a guard had been removed. The guard was present and correct.

The response is to treat the harness as needing its own verification, which costs little and is mechanical:

- **Bracket every run with controls, and refuse to report if they fail.** A POSITIVE control forces the self-test to fail and confirms the harness SEES a failure: a harness that cannot observe a failing test produces NOT-DETECTED verdicts that are void rather than evidence, and this alone catches the inverted-verdict class. A NEGATIVE control makes a change that cannot matter (a comment) and confirms the test still passes: a harness that flags a comment is over-sensitive, and its DETECTED verdicts mean nothing either. Controls failing invalidates the whole run, not one row of it.
- **Screen each candidate for semantic effect BEFORE interpreting its result.** An edit that cannot change behaviour is reported INVALID, never NOT-DETECTED, because its passing test says nothing about coverage. Never mutate a string literal and never rename: both are behaviour-preserving by construction. Mutate control flow only, meaning conditions, comparisons, return values and boundaries.
- **Establish a true positive before believing a negative.** Before concluding a guard is undetectable, confirm the UN-mutated code produces the expected finding on a known-good input. If it cannot, the invocation is wrong rather than the code, and this is the discipline that catches the degenerate-return class.
- **Prefer the project's own test harness to a hand-rolled caller.** A suite's helpers set up roots, fixtures and paths correctly; a fragment assembled by hand bypasses exactly that setup, which is where the precondition failures come from.
- **Where mutation claims recur, build the probe as a TOOL rather than re-improvising.** Three false signals in one day is the signal that the technique has outgrown ad-hoc scripting. A probe that enforces the controls and the semantic screen mechanically cannot forget them, and it makes the claim reproducible by someone other than its author.

### Prohibited anti-patterns

- **Reading a mutation proof as proof the guard is sound.** It bounds the check, never the data reaching it. A guard's proof and its input's fidelity are separate claims requiring separate evidence.
- **Encoding ignorance as absence.** Collapsing "I could not determine this" into "there is nothing here", when absence is the permissive branch.
- **Hardening the check instead of fixing the input.** Adding conditions to a predicate whose input cannot answer the question makes the defect harder to see without making it less real.
- **Asserting a proxy as the thing itself.** Treating "the file exists" as "the file is complete", or "it is heartbeating" as "it is working", in prose or in a variable name that claims more than the value carries.

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

### The ambient working directory is an inferred premise

In a multi-repository workspace, the shell's current working directory is itself an inferred premise for any command that resolves relative to it: a bare tool invocation (`tools/x`), a repository-relative path, or a bare version-control command (`git add`, `git commit`, `git push`). The working directory drifts between calls (a prior `cd` into a sibling repository persists), so such a command silently acts on whichever repository the cwd happens to be, not the one intended. This is this rule's inference cascade applied to the shell: an unvalidated "I am in repository X" premise drives a mutating command against repository Y.

Validate the target explicitly rather than trusting the working directory:
- **Prefer a cwd-independent form by default:** an absolute tool path (`python3 /abs/path/<repo>/tools/x`) or a repository-pinned flag (`git -C /abs/path/<repo> ...`), which cannot be redirected by drift.
- **Reserve an explicit `cd <repo-root> &&` prefix** for the narrow case of a tool that must run from its own root; when used, type the `cd` as the literal first tokens of the command and read the command string back before submitting, because narrating a `cd` the command does not actually contain is an intent-versus-artefact gap: what you intend is not what the command string says.
- **Never let a repository-mutating command (stage, commit, push, reset, checkout) run cwd-relative:** the blast radius of a wrong-repository mutation is large and hard to reverse, so it always carries `-C` or an explicit `cd`.

Where the harness supports it, a pre-execution guard that blocks a cwd-relative sibling-repository tool or a repo-mutating bare version-control command is the mechanical backstop; the discipline (cwd-independent commands by default) is the primary control.

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
| Validated premise before action | RV.1, RV.2 | GRC-05, LOG-02 | A.5.36, A.8.15 | V15.1, V16.2 |
| Cascade prevention discipline | PO.5 | GRC-04 | A.5.4 | V15.1 |
| Audit trail of validations | PS.1, RV.2 | LOG-02, LOG-04, LOG-10 | A.8.15, A.5.36 | V16.2, V16.4 |
| Diagnosis before retry after repeated failure | RV.1, RV.2 | GRC-05 | A.5.36 | V15.1 |

The discipline implements the same audit-trail-integrity principle the broader pack expresses: every action driven by a premise must be traceable to a validation of the premise. The cost of an unvalidated premise compounds; the cost of one extra tool call does not.

<!-- PROJECT-OVERLAY: not part of the distributable pack -->

## Project overlay (grc_library wiring and lineage; local copy only)

- The register in which validation-sweep dispatch declarations are recorded
  (the skill's Rule 5.6): `.working/validate-sweeps/history.md`.
- The repeated-failure circuit-breaker is enforced mechanically by the
  [`block-repeated-tool-failure.py`](../../hooks/block-repeated-tool-failure.py)
  PreToolUse hook (GUARD 2: on two or more consecutive same-class blocks it requires a
  written mechanism diagnosis before any retry), and the degradation hypothesis, if
  raised, is recorded and assessed in `grc_library_private/degradation-watch-log.md`
  before it is asserted.
