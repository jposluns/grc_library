# Action Before Explanation of Inaction

Never explain why an external action cannot or will not proceed without first attempting it (when the action is safe and reversible) or naming it and asking (when the action is destructive). Inferred reasons for inaction are the failure mode this rule prevents: a confidently-stated cause that the asserting party has not verified, that the user trusts because it sounds like a system fact, and that turns out to be wrong because the action would have succeeded if attempted.

The discipline keys on a specific surface: the moment when a draft message is about to contain a clause of the form "X cannot proceed because Y", "X is blocked / waiting on / requires / needs / would fail", "the system says I need to wait for Z". At that moment, either the action has been attempted this turn and the explanation is grounded in its actual result, or the action has not been attempted and the explanation is an inference. Inferences in this position are forbidden.

This rule applies to human developers and to AI coding assistants equally; in practice it is binding more often on AI assistants, because the failure mode (narrating a reason to wait instead of taking the cheap, reversible action that would resolve the doubt) is the dominant pattern when an assistant is uncertain and feels pressure to surface progress.

This rule does *not* override the confirm-before-destructive-action discipline. It operates only inside the safe-and-reversible action set; the second half of the rule says how to handle the destructive set without slipping into the same inferred-reason failure mode in a different costume.

---

## What counts as an inaction explanation

Any clause that asserts a reason an external action cannot or will not proceed, attached to an action the asserting party has not attempted in the current turn. Examples of the surface:

- "The PR is blocked because it needs a reviewer."
- "The merge is waiting on CI."
- "This requires admin approval."
- "That would fail because the schema doesn't accept it."
- "The deploy can't go through until the migration runs."
- "I'd need permission to delete that branch."

Each is a state assertion about an external system the speaker has not interrogated this turn. Each may be true. None are evidence.

The trigger words are not the rule; the *pattern* is the rule. "This function requires a string" is normal technical prose about an artefact, not an inaction explanation about an external action: it does not trigger. "The merge requires a reviewer," asserted without checking, does trigger.

A useful self-check before sending: for the most recent inaction explanation in the draft, can I quote the tool result that grounds it? If not, the explanation is an inference and the rule fires.

---

## The reversibility gate

Before applying the rule's protocol, classify the action.

**Safe and reversible** actions are the rule's primary surface. Defining property: if attempted and the attempt fails, the failure is bounded (no shared-state mutation, no outward-facing publish, no destruction of work that did not belong to the actor). Typical members of the set:

- Status reads (CI state, branch protection state, PR mergeability).
- Pushes to a feature branch the actor owns.
- Re-runs of a CI job, a build, a lint, a test.
- A merge of a green PR through the project's *documented* merge mechanism, in a project whose workflow has made that merge routine for the actor to perform.

Membership in this set is project-dependent. "Merging a PR" is reversible-with-a-revert in a small project the actor co-owns; the same action is outward-facing and authority-bound in a regulated repo. When the project file is silent on whether the action is routine, do not promote it into the safe set by default; treat it as destructive and ask.

**Destructive or hard-to-reverse** actions are the rule's secondary surface. Defining property: if attempted and the result is not what the actor expected, the unwind cost is substantial or impossible. Typical members:

- Force-push to a shared or protected branch.
- History rewrite.
- `reset --hard` over uncommitted work that did not belong to the actor.
- Deletion of data the actor did not create.
- Production deploy.
- Outward-facing publish (a message sent, a release tagged, a PR opened against a third-party repo).
- Anything the project's documented governance or the operator's base instructions require to be confirmed before execution.

When in doubt about which set an action is in, treat it as destructive and ask.

---

## For safe actions: explanation of inaction without a verifying tool call is forbidden

Before any clause of the form "X cannot proceed because Y", where X is in the safe set, the actor MUST attempt X and report the actual tool result.

The attempt produces one of two outcomes: success, or a specific error response. Either grounds the next sentence the actor writes. Neither can be faked.

If the attempt succeeds, the inaction explanation that was about to be drafted is moot: the action proceeded, and the message says so. If the attempt fails, the failure response names the cause, which is exactly the fact the inaction explanation was about to guess at. The draft is rewritten around the real cause.

A useful heuristic: under doubt, prefer the action. Cheap, reversible actions resolve doubt by producing real information. Narration about why the action might not work does not resolve doubt; it preserves the doubt and pretends to explain it.

---

## For destructive actions: name the action, state you have not attempted it, and ask

When the action is in the destructive set, the rule's safe-action protocol does not apply. The actor still cannot substitute a guessed cause for the missing attempt.

The acceptable shape is: "I have not run the force-push; it rewrites shared history, so I need your go-ahead." This is honest: it names the action, names the property that puts it in the destructive set, and surfaces the decision.

The unacceptable shape is: "The branch is blocked because it would require a force-push." This is the same unverified-assertion failure as the safe-action case, dressed up in a scary-sounding cause to justify waiting. The actor has not run the force-push; the "would require" clause is an inference; the user is now being asked to trust an unverified reason.

The discipline for destructive actions is therefore stricter, not looser: the destructive set forbids both "just try it" *and* "guess a destructive reason and stop". The only available move is to name the action plainly and ask.

---

## Execution doubt vs decision doubt

This rule governs execution doubt: "Will this work / what does the system actually say / is this gate going to flip / is the branch in the state I think it is." Execution doubt is resolved by attempting the safe action and reading the real result, or by naming the destructive action and asking.

This rule does *not* govern decision doubt: "Which of these reasonable options does the user want / which target branch / does this ambiguous date mean X or Y / should I be making this authorial choice at all." Decision doubt is resolved by asking with named alternatives, per the clarify-before-acting rule.

When trigger words appear *and* an authorial or ambiguous choice is in scope, the clarify rule takes precedence over this one. The right move is the clarifying question, not the optimistic attempt; an attempted action grounded in a guess at the user's intent is the same silent-pick failure mode the clarify rule is built to prevent.

---

## Prohibited anti-patterns

- **Inferring a destructive reason to justify waiting.** "The branch is blocked because it would need a force-push," asserted without checking, is the rule's failure mode in a destructive costume. Either name the action and ask, or check the actual state.
- **Padding the inaction with hedge words while still making a state assertion.** "It looks like the merge might be blocked" is still a state assertion the reader will rely on. Either it is blocked (quote the tool result) or you have not checked (say so).
- **Polling instead of subscribing.** If the platform offers a wake-on-event primitive (webhook subscription, MCP `subscribe_pr_activity` or equivalent), use it. Polling against an external API to "wait until X" is the same failure class as a pipe-masked exit code, with additional ways to fail silently (rate-limit responses, transient HTTP errors, indefinite loops).
- **Reading the user's silence as confirmation that the inaction was correct.** Silence is not signal. The user may not have noticed the inaction explanation, or may have read past it, or may be waiting for the actor to attempt the action without a further prompt.
- **Composing the inaction summary in parallel with the tool call that would have grounded or refuted it.** The summary is downstream of the tool result, not upstream of it; commit to the result first, then write.
- **Conflating "the action did not happen" with "the action could not happen".** The first is a description of the actor's behaviour ("I did not run the merge"). The second is an assertion about the world ("the merge could not have run"). The second requires evidence the first does not.

---

## Tool-specific guidance for AI coding assistants

### Status reads vs polling

When the verification needed is "what does the system currently say about X", prefer a single authenticated status read over a polling loop. Status reads are cheap, deterministic, and produce a result the next sentence can be grounded in. Polling loops are an exception, justified only when no event primitive is available and the condition is not event-shaped; see the canonical evidence-grounded-completion rule's "API polling and webhook subscriptions" section for the guardrails when polling is unavoidable.

### Webhook subscriptions

When the platform's MCP server or SDK exposes an event-subscription primitive (the canonical example: `mcp__github__subscribe_pr_activity` on the Claude Code GitHub MCP server), arming a subscription before a long-running external event is the right move. Subscribing replaces inaction explanation with event-driven action: the next turn fires on a real event payload, and the explanation is grounded in that payload. Trust the subscription's negative space, with the discipline named in the canonical rule: subscriptions deliver failure events but typically not success transitions, so once a relevant interaction occurs, resolve the ambiguity with one explicit status check rather than a polling loop.

### Stop-hook and pre-commit feedback

If a stop hook or pre-commit check fires during a turn (typical signal: "there are uncommitted changes in the repository"), the right response is to address the underlying state, not to draft an inaction explanation for why the state is the way it is. The hook is reporting a real condition; explaining it in narrative form without acting is the same anti-pattern as the broader rule, scoped down to the harness's signal.

### MCP and rate limits

When an MCP tool returns a rate-limit error, the inaction explanation that follows ("the API is rate-limited") is grounded *if and only if* the actor quotes the error response and either retries with backoff (when the action is safe) or names the action and asks (when the action is destructive). Reading "rate-limited" as a reason to stop without surfacing the specific error response and the next action is the same anti-pattern.

---

## Exception-handling protocol

There is no general exception that excuses this rule. The discipline's whole value is that the safe-and-reversible set is broad enough to cover most external actions an AI coding assistant takes, and the destructive set has its own clear protocol (name and ask). The "I attempted X and the result was Y" form is always available; the "I have not attempted X because Z is destructive" form is always available; nothing else is needed.

The narrowest legitimate exception is the case where the action is in the safe set but the actor genuinely cannot attempt it in the current turn (the tool is unavailable; the network is partitioned; the credentials have not been provided). In that case the acceptable shape is: "I cannot attempt X right now because [the tool is not exposed / I have no credentials for the target / the network is unreachable]; the explanation for the underlying inaction would require attempting it." This is honest about what was tried and what was not, and it does not substitute a guess for the missing attempt.

---

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 | OWASP ASVS |
| --- | --- | --- | --- | --- |
| Action-grounded explanations of inaction | RV.1 | GRC-05 | A.5.36 | V16.2 |
| Reversibility classification before acting | PO.5, RV.2 | GRC-04 | A.5.4 | V15.1 |
| Confirm-before-destructive-action discipline | PO.5 | GRC-04 | A.5.4, A.5.18 | V15.1 |
| Subscription-over-polling for event-shaped waits | RV.2 | LOG-02 | A.8.15 | V15.1 |

The discipline implements the same audit-trail-integrity principle the broader pack expresses: every assertion the user is asked to rely on must be traceable to a verifiable artefact (a tool result, a quoted response, a named missing attempt). The cost of an unverifiable assertion compounds: each one the user accepts erodes the discipline that catches the next.

<!-- PROJECT-OVERLAY: not part of the distributable pack -->

## Project overlay (grc_library wiring and lineage; local copy only)

- Project instantiation: the CLAUDE.md `PR activity subscription discipline`
  (subscribe plus a 60-second fallback timer; the background-task check SOP).
