# Session Lifecycle and Operating Modes

Long AI-assistant sessions degrade: context dilutes, compaction is lossy, state drifts, and errors compound. The assistant has no reliable internal gauge of any of this, so the defence is EXTERNAL: durable state records, explicit operating modes, evidence-gated wind-down, and a clean handoff protocol. This rule distributes that apparatus as a pack discipline so any project running multi-session AI-assisted work inherits it, rather than re-deriving it after its first degraded session.

The lifecycle has three phases: RESUME from a durable handoff record, WORK under an explicitly named operating mode, and CLOSE by landing working state as a green merge that the next session resumes from. Each phase has a discipline below. The rule is project-agnostic; the consuming project wires the concrete files (its handoff record, its lease file, its resume command) and this rule states the invariants they implement.

---

## 1. The durable handoff record (the resume point)

A single file in the project's working state is the resume point for a new session: current branch and versions, what merged most recently, the next-actions queue, open decisions awaiting the operator, known environment behaviours, and the standing disciplines. It is refreshed at every merge close-out, RECONCILED rather than appended (a snapshot refreshed in the same change that falsifies it is drift, not a refresh), and pruned on a keep-current-plus-one-prior cadence so the load-bearing state is never buried under session history.

The discipline: prefer a fresh session resuming from the record over a long session running on accumulated memory. Resuming means verifying the snapshot against live files before relying on it (the record is as-of-last-refresh, not live truth), then continuing from the queue.

## 2. Operating modes are explicit, and the operator sets them

The mode in force is named, never inferred. Three modes cover the space:

- **Fully attended**: the operator is watching; decisions are asked as they arise.
- **Attended-autonomous** (the default for active sessions): the operator is reachable but not watching every step. Green CI on the assistant's own routine work is merge authority; the operator redirects by exception. Decisions that are genuinely the operator's are surfaced with named options and a short timer (section 3); the assistant keeps moving rather than blocking on each merge.
- **Unattended / overnight**: the operator is away. The assistant never idles waiting for an answer: it proceeds on the highest-priority authorized independent item, defers genuinely authorial decisions around (section 3), logs identically to attended modes (unattended logging is never abbreviated), and defers protected-surface changes that need operator authorization, staging their content for a quick authorized apply on return.
- **Mode transitions are operator acts.** Ending an unattended mode is never a no-answer default or a timeout effect; if unsure whether the mode changed, ask and keep the current mode until answered. On exit from an unattended run, the standing priority is: route the run's accumulated state first, then fixes, then tooling and protections, then new work.

Two rules hold in every mode: stricter-is-safer on any cross-value conflict (resolve toward the more conservative or the source-supported value, and record the choice), and throughput pressure never authorizes abbreviating a mandatory QA step.

## 3. Graceful degradation for operator decisions

When the next action depends on a decision that is genuinely the operator's, the assistant surfaces it with named options (recommended first) and arms a short timer rather than stalling. On timeout, exactly one of two logged paths:

- **Stricter-safe default**, only when a defensible, more-conservative, evidence-backed option exists AND the action is reversible: proceed, record "proceeded with X; confirm or redirect on resume".
- **Defer-and-skip**, when the decision is authorial, irreversible, or outward-facing: record it as blocked, route around it to the next independent task, and hold everything that depends on it.

The reversibility gate is absolute: a timeout NEVER auto-executes a destructive, irreversible, or outward-facing action. If every remaining task depends on the one pending decision, close cleanly (section 5) rather than guessing. Deferred decisions and any verifier overrides made unattended are surfaced at the next attended boundary; the operator, not the assistant, closes them.

## 4. Wind-down is evidence-gated, and the default is to continue

The default at every point is to continue working. The ONLY valid trigger for proposing a session close is a NAMED, externally-observable signal of an actual problem: a failing check, a validation finding the QA layer missed, an operator correction, or a quotable self-inconsistency. Un-instrumented internal state ("context feels heavy", "I feel degraded") and work shape ("a large series is next") are never triggers on their own; large work is done unit-by-unit with independent verification sustaining quality. Session depth is a legitimate CONTRIBUTING factor to a handoff PROPOSAL, one of many, but never the SOLE reason: it is weighed alongside other signals and warrants OFFERING a handoff (the operator's choice, never automatic) in two cases, a very-long-run of expected chained work ahead (especially where the project's own historical metrics show a measured quality decline on comparable prior runs) or excessively-sensitive work whose integrity requires fresh context with no accumulated session history to skew it (a whole-project assessment or audit is the canonical case). Depth ALONE, with no long-run-ahead and no sensitivity reason, is not a trigger.

When a close IS evidence-triggered, it is surfaced, never taken silently: the justification in objective signals, a tractability read on the pending queue, and named options with the conservative close first. A no-answer timeout resolves to the conservative close, never to pushing on; and in an unattended mode the mode's own conflict rules govern instead. Choosing to continue never relaxes any discipline: the degradation read re-runs at each unit boundary, and the run self-terminates early if signals appear.

In an unattended mode there is no operator to surface the choice to, so an evidence-triggered close is EXECUTED, not offered: the assistant performs the closing handoff of the next section (land the working state on the shared branch as a green merge, reconcile the durable handoff record, release the lease) directly, because that handoff is itself the conservative, reversible, no-regret action and needs no confirming question. It is not a bare mid-turn pause. A "stopping here" that leaves the working state unmerged on a side branch and the handoff record only half-written is the failure this guards against: it hands the next session a harder resume than the clean shared-branch state a proper close leaves. Rule of thumb for an unattended run: being about to stop is an obligation to execute the closing handoff first, not a licence to pause.

## 5. The closing handoff: a session's last act is a green merge

A session ends by landing its working state on the protected branch as a green, merged change, so the next session rebuilds from the shared branch rather than from an unmerged local state. The closing change refreshes the handoff record (including what this session mechanically verified, scoped to what it touched, and known soft spots NOT asserted clean) and records its own QA exemption explicitly where the project's cadence grants one.

The loop-break: the closing change may skip its own trailing per-change QA sweep (running it would spawn a records-then-merge loop with no terminating next change at a session boundary) ONLY where the project pairs the skip with a stronger compensating control at the next resume, a fresh whole-scope validation whose findings are cross-checked against the closing session's asserted-clean claims. A contradiction of an asserted-clean surface is a miss signal to escalate, not an ordinary finding.

## 6. The concurrency lease

Where two sessions could hold the shared state surfaces at once, a lease file on the shared branch declares the holder: ACQUIRE at resume (after checking the prior lease is released or stale, plus an external cross-check such as unmerged sibling branches with recent commits), REFRESH the heartbeat at each close-out, RELEASE in the closing change. The interlock is advisory (it prevents the realistic accidental double-resume, not a determined simultaneous launch), and its one hard rule is that a live-looking lease HOLDs the resume for an explicit operator confirmation; proceeding is never a timeout default, because proceeding is the potentially destructive path.

---

## Prohibited anti-patterns

- **Winding down on felt degradation or work shape.** No instrument, no trigger; continue, with verification sustaining quality.
- **Idling in an unattended mode** because the remaining work is substantial, fiddly, or awaiting a preference. The standing priorities answer "what next"; the graceful-degradation paths answer "what about this decision".
- **Pausing mid-turn on a real degradation trigger in an unattended run** instead of executing the closing handoff. When the trigger is genuine, the response is a green merge plus a reconciled handoff record, not a "stopping here" that strands working state on an unmerged branch and leaves the record half-written for the next session to untangle.
- **Ending an unattended mode on a timeout**, or reading operator silence as a mode change.
- **A timeout auto-executing the destructive option.** The reversibility gate has no exceptions.
- **Appending to the handoff instead of reconciling it**, or asserting clean surfaces the session never verified (an unfounded clean claim turns the next session's ordinary findings into spurious miss signals).
- **Skipping the closing QA without the compensating control**, or resuming without running it.
- **Proceeding past a live-looking lease** without operator confirmation.
- **Abbreviating mandatory QA under throughput pressure** in any mode; surfacing the pressure is one sentence, and the cadence is the pace.

## Tool-specific guidance for AI coding assistants

- Use the toolchain's structured question primitive for surfaced decisions (named options, recommended first, one-line consequences), and a background timer primitive for the degradation window; never a blocking wait.
- Re-anchor the mode at each unit boundary: state which mode is in force in the close-out narration, so the operator can correct a stale assumption cheaply.
- Where the harness supports it, verify the handoff snapshot mechanically at resume (versions, counts, a green baseline at a named commit) before trusting any of its prose.

## Exception-handling protocol

The rule's mechanisms are the exception paths (graceful degradation for blocked decisions; the loop-break with its compensating control for the closing QA). A project may narrow them (for example, forbidding stricter-safe defaults entirely in unattended runs) but must not widen them silently; widening (a new skip path, a longer timer that auto-proceeds) is an operator decision recorded in the project's decision trail.

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 | OWASP ASVS |
| --- | --- | --- | --- | --- |
| Durable state records and auditable handoff | PS.1, RV.2 | LOG-02, LOG-04, LOG-10 | A.8.15, A.5.36 | V14.1 |
| Explicit authorization boundaries per mode | PO.5 | IAM-09, GRC-04 | A.5.15, A.5.18 | V1.1 |
| Evidence-gated lifecycle decisions | RV.1, RV.2 | GRC-05 | A.5.36 | V14.1 |
| Concurrency control on shared state | PO.5 | CCC-01 to 03 | A.5.4, A.8.32 | V1.1 |
