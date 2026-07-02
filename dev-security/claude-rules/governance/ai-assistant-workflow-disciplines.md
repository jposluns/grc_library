# AI Assistant Workflow Disciplines

When an AI coding assistant drives multi-PR work over a long session (a remediation backlog, a phased migration, a corpus-wide cleanup), five related disciplines govern how the work is structured. They share a theme: the orchestrator (the assistant doing the writing) partners with research helpers (subagents producing draft content) across many PRs, and the discipline that keeps the work honest spans the worker-orchestrator boundary, the per-PR cadence, the apply-time verification step, and the use of CI-wait windows.

This rule applies to any project where an AI assistant ships substantive work across multiple PRs with research helpers, CI gating, and a maintainer in the loop. The disciplines are project-agnostic; the failure modes they prevent are observed across projects.

The five disciplines:

1. **Research-assistant discipline.** Workers produce research; the orchestrator authors all final prose.
2. **Pipeline PR construction.** Parallel research, serial application, CI between each PR.
3. **Apply-time worker correction.** Catch worker errors at apply-time, document them in the entry.
4. **Always split when in doubt.** Default to splitting changes into separate PRs unless they're tightly coherent.
5. **Background work during CI waits.** Use the wait window for read-only prep on the next PR.

---

## 1. Research-assistant discipline

The orchestrator dispatches background workers (subagents) to produce research files for upcoming PRs. The research file is **information**, not **final prose**: it surfaces quoted lines from target files, proposes edit shapes, drafts CHANGELOG/DONE bodies, and notes caveats. The orchestrator reads the research file as input, then **independently re-reads every target file**, verifies every worker claim against the live file state, and authors the final prose.

The orchestrator does not paste worker prose into the corpus unmodified. The orchestrator's job is to verify, correct, and integrate; the worker's job is to surface candidates.

### Why the discipline exists

A worker that drafts an entire PR's prose creates two failure modes:

1. **Confabulation.** The worker references a file that does not exist, an FR cross-reference that's wrong, a version number that's stale, or a quoted line that the file does not actually contain. The orchestrator pasting worker prose unverified ships the confabulation.
2. **Style drift.** The worker's prose voice differs from the project's voice. Over many PRs, this drift compounds.

The research-assistant discipline closes both. The orchestrator re-reading target files catches confabulations; the orchestrator authoring final prose keeps voice consistent.

### The verification protocol

For each worker claim that's about to ship in the final PR:

1. **Quoted lines from target files.** The orchestrator opens the file and confirms the quoted lines match. If the worker drafted against a stale revision, the orchestrator reconciles to current state.
2. **File paths.** The orchestrator confirms the referenced file actually exists. A `find` or `Glob` is enough.
3. **Cross-references to other PRs / FRs.** The orchestrator opens the closed-PR ledger or the relevant register and confirms the referenced item. A worker drafting "FR-3 closed in PR #158" is verified by checking the closed-PR ledger; if the actual closing PR is #147, the orchestrator corrects.
4. **Version numbers.** The orchestrator confirms current per-document and library versions against the live file state. Worker drafts from earlier in the session may carry stale version numbers.
5. **External-standard citations.** The orchestrator confirms the standard's year, edition, and identifier against the project's canonical-citations register or against external sources via WebFetch / verified MCP tools.

A worker claim that survives this verification is allowed into the final prose; a claim that does not is corrected before commit.

### Tracking corrections

When the orchestrator catches a worker error at apply-time and corrects it, the correction is documented in the CHANGELOG-detailed entry under a "Discipline observation" or equivalent section. The pattern:

```
[Number] corrections to the worker draft were applied at apply-time:
(1) [what was wrong; what was corrected];
(2) [what was wrong; what was corrected].
```

The audit trail of corrections accumulates across PRs as a signal of whether the research-assistant discipline is producing quality input. A rising correction rate suggests the worker prompt needs tightening; a falling rate suggests the discipline is converging.

### Worker-brief template and hallucination-assessment update protocol

Projects that adopt this discipline maintain a project-local **worker-brief template** that the orchestrator uses as the starting point for every worker dispatch. The template codifies the guard rails (DO and DO-NOT lists) that prevent recurring worker-side failure modes. Each guard rail traces back to a logged apply-time catch; when a new failure class appears, the template is updated to prevent recurrence.

The update protocol when a new failure class is caught:

1. **Log the catch** in the project's worker-hallucination tracking artefact (in this project: `.working/hallucination-metrics.md`). Include the root-cause analysis: why did the worker produce the wrong output, and which class of guard rail would have prevented it (worker-side instruction, orchestrator-side verification, or a new mechanical gate)?
2. **Determine the guard-rail class.** If the failure can be prevented by an instruction in the worker brief, the fix is a template update. If it requires the orchestrator to verify something at apply-time, the fix is an orchestrator-checklist update (typically in this rule's §3 Apply-time worker correction). If it requires a mechanical check, the fix is a new gate (queued as a follow-up PR).
3. **Update the template inline** in the same PR (if the change is small) or queue as a follow-up PR (if substantive). Citing the source catch (PR number) inline preserves the lineage.
4. **Reference the template update** from the hallucination-metrics catch entry by template Version number, closing the loop.

This makes the discipline self-improving: each new failure class observed becomes a permanent guard rail in the template, and the next worker dispatch benefits from the lesson without the orchestrator having to remember to add the instruction ad hoc.

The template is project-local because the specific failure modes vary by project (file paths, citation registers, cross-reference conventions). Projects adopting this discipline should create a similar template at a project-appropriate location. The pack rule documents the protocol; the template documents the project's accumulated lessons.

---

## 2. Pipeline PR construction

When an AI assistant drives a backlog of related PRs (a remediation queue, a phased rollout), the work pipelines naturally:

- **Stage 1 (parallel)**: dispatch background workers in parallel to produce research files for the next N PRs (default: enough to keep the orchestrator's apply-queue non-empty).
- **Stage 2 (serial)**: the orchestrator applies one research file at a time, authoring final prose, running audits, committing, pushing, opening the PR.
- **Stage 3 (gating)**: the PR's CI must complete and the merge must land before the orchestrator starts the next apply. The next research file is already prepared; the wait is for CI, not for research.

The parallelism is at the research stage; the seriality is at the apply stage. Mixing the two (parallel applies) is the failure mode this discipline prevents: the orchestrator cannot apply multiple PRs at once without state confusion (which branch am I on; which research file matches which target file; which CHANGELOG entry got written last). One PR at a time, with the next one's research already in hand, is the right shape.

### Triggering the parallel research stage

The orchestrator dispatches workers in parallel at session-start and whenever the apply-queue thins below the desired buffer. Workers run in the background and notify on completion; the orchestrator does not block on any one worker.

The buffer size is project-configurable. A typical default: prepare research for the next 7-20 PRs so the apply-queue is rarely empty during a long working session. Larger buffers mean more upfront token cost; smaller buffers mean more idle waiting if applies finish faster than research.

### Failure modes the discipline prevents

- **Idle gaps between PRs.** Without parallel research, the orchestrator finishes one PR and waits for the next research file. With parallel research, the next file is ready.
- **Out-of-order applies.** Without serial applies, two simultaneous edits on the same target file collide. With serial applies + CI gating, each PR's changes ground in the previous PR's merged state.
- **Lost work on CI failure.** Without CI gating between applies, a failure in PR #N is discovered after PRs #N+1, #N+2 are already pushed; the cascade is expensive. With CI gating, each PR's CI completes before the next is started.

### The partitionable-work default (light SOP)

When a backlog decomposes into a verified-disjoint set of files, the orchestrator's default first move is to fan out research workers (discipline 1) across the partition rather than research each item serially. This is the standing operating default for partitionable work; the parallelism is exactly the pipeline's point (many workers research at once, the orchestrator applies one diff at a time).

The default is gated, not automatic. Fan out only when every condition holds:

- The work decomposes into files that are **verified disjoint** (no two workers touch the same file; re-verify per wave, not once, because files move and merge between waves).
- No **shared surface** is a worker's to touch (the version surfaces, the CHANGELOG, the generated artefacts, the backlog and done ledgers, the session handoff, and the QA records are orchestrator-only).
- The work is **not** a corpus-wide sweep, rename, or convention migration, and **not** a single indivisible artefact. Those touch an unbounded or non-partitionable set and stay single-session.

Crucially, the default does **not** disturb the serial-apply and CI-gating invariants of discipline 2, nor the apply-time verification of discipline 3. Each worker diff is validated and QA-checked before it is applied (the orchestrator re-reads every changed line, re-verifies citations and control identifiers, runs the relevant checks), applied in one commit, and gated through the normal pipeline. Worker provenance never reduces the QA a change receives; it only adds a pre-apply screen on top of it. There is no trusted-worker fast path: parallelism lives in the research stage, authority and seriality live in the apply stage.

Two worker primitives serve the default: **in-session subagent fan-out** (workers launched inside the orchestrator's own session, sharing its credentials, the lowest-setup form, available wherever the harness offers a subagent primitive) and **separate-session external-collaborator workers** (workers in their own sessions under their own accounts, granted write access only to an exchange channel and never to the protected repository, the least-privilege form). A project that runs multi-session or multi-worker work should keep a project-local runbook documenting its exchange channel, its durable claims-ledger coordination (read at launch, never a poll loop), and its partitionability checklist; the pack rule states the discipline, the runbook states the project's how-to.

---

## 3. Apply-time worker correction

The apply-time correction is the moment where the research-assistant discipline produces audit value. The orchestrator should treat every worker draft as a hypothesis, not a finding (per the evidence-grounded-completion rule's broader pattern). At apply-time:

1. **Open each target file in full.** The worker quoted some lines; the orchestrator confirms them.
2. **Run contradiction searches.** A `grep` for stale references, parallel occurrences elsewhere, or claims the worker did not surface.
3. **Reconcile to current state.** Versions, dates, FR cross-references, file paths that may have shifted since the worker drafted.
4. **Apply the per-file metadata-bump check.** When editing a versioned document's body, the orchestrator bumps **both** the `Version` field and the `Date` field in the same commit. Skipping either is the failure mode CI gates (version-bump-recency for Version; document-date-staleness for Date) are built to catch, but the cost of the catch is a CI-rerun loop; bumping both in the same commit avoids the loop. The corollary at PR level: when the orchestrator is about to commit, the explicit checklist item is "for every versioned file touched in this commit, did I bump Version *and* Date?", not "did I bump Version?" alone.
5. **Document corrections.** Every catch is recorded in the CHANGELOG-detailed entry per §1's tracking convention.

The discipline scales: the more PRs the assistant ships, the more pattern-recognition for worker failure modes accumulates. Common patterns: stale version numbers (worker drafted against an earlier revision); confabulated file paths (worker invented a plausible-sounding filename); incorrect PR cross-references (worker confused two PR numbers); orchestrator bumping Version but missing Date (recurring orchestrator-side oversight; CI-caught but worth designing out).

### Why apply-time, not pre-apply

The orchestrator could verify worker claims at the moment the research file arrives (pre-apply). The discipline prefers apply-time because:

- The corpus state continues to drift between research-dispatch and apply (other PRs may merge in between).
- Apply-time verification is when the orchestrator is about to write to the file system; that's the moment when an unverified claim has the highest cost.
- Apply-time verification is bounded: it covers the small number of claims that survive to apply-time, not the larger set the worker might have drafted.

---

## 4. Always split when in doubt

When two changes could plausibly land in the same PR or in separate PRs, default to **separate PRs** unless they are tightly coherent (same conceptual theme, same files, same maintainer-direction line item).

### Why default to splitting

- **Reviewer cognitive cost is non-linear.** A PR with three unrelated changes is more than 3× the review cost of three separate PRs.
- **Bisection cost.** If a defect ships in a multi-purpose PR, finding which change introduced it requires re-reading the diff. Single-purpose PRs make `git bisect` precise.
- **Revert safety.** A multi-purpose PR cannot be partially reverted; reverting it un-ships unrelated changes too.
- **Audit-trail clarity.** Each PR's CHANGELOG entry maps to one conceptual change. Bundling muddies that mapping.

### When bundling is allowed

The "tightly coherent" exception covers:

- Multiple findings in the same file from the same maintainer-direction velocity bundle (e.g., five FR fixes in the same README under a "phase 1 polish" directive).
- A rule update and the corresponding skill update for the same rule (paired-skill gate enforces parity).
- A new rule plus a new linter that enforces it.

When in doubt, ask the maintainer. The cost of asking is one round-trip; the cost of an inappropriately-bundled PR is the rest of the project's lifetime to untangle.

---

## 5. Background work during CI waits

CI cycles take time. A typical small-corpus lint run is 30 to 90 seconds; substantive PRs may run longer. The orchestrator should not sit idle during these waits.

### What's safe to do during a CI wait

**Read-only prep on the next PR's research:**

- Read the next research file in full.
- `grep` for the worker's quoted lines in current main to pre-verify.
- Confirm referenced file paths exist via `find` or `Glob`.
- Check the current per-document and library version numbers against what the worker drafted; pre-identify any version-drift corrections needed.
- Cross-check PR / FR references against the closed-PR ledger.

The discipline: **read-only operations on main (the unchanging branch during the CI wait) for the next PR's target files.** Surface any apply-time corrections that will be needed when the current PR merges, so the next apply can proceed faster.

### What's not safe during a CI wait

- **File edits.** The current PR's CI is running against a feature branch; the orchestrator must not edit anything on main or on a new branch that would interfere with the merge-back.
- **New commits to the current branch.** The CI run is against a specific commit SHA; new commits invalidate the run.
- **Pre-creating the next branch.** Branch state confusion is a real risk; wait until the current PR merges and main is synced.
- **Speculative tool calls that change state** (mutating MCP calls, API writes, etc.).

### What's not safe period

Polling for CI status in a tight loop. The discipline lives elsewhere (the webhook-subscriptions guidance in [`action-before-explanation-of-inaction.md`](action-before-explanation-of-inaction.md) and the API-polling guardrails in [`evidence-grounded-completion.md`](evidence-grounded-completion.md)): subscribe to the PR's activity, arm a paired short-cadence fallback timer, do the read-only prep, then check status when either fires.

---

## Skeptical pre-push verification (a tiered standard layered on the disciplines, not a sixth)

The apply-time correction of discipline 3 is the orchestrator re-reading its own and the worker's output. For any change beyond a quick fix, a stronger, INDEPENDENT adversarial check runs before push: a skeptical verifier subagent, briefed to REFUTE the change (hunt the defect), not to confirm it. This is a standard layered across disciplines 1 to 3, not a sixth discipline, and it applies to orchestrator-authored changes as much as to worker drafts. It is tiered by change weight, because indiscriminate verification wastes budget and erodes the signal that a change is genuinely substantive (the same calibration [`high-assurance-verification.md`](high-assurance-verification.md) applies to its own trigger):

- **Quick-fix / pure-bookkeeping tier** (version bumps, working-state records, a single-line prose or typo fix, generated-artefact regeneration): NO standing verifier. The mechanical gates, the change-log preflight, and the routine post-merge PR-scoped sweep are sufficient; a verifier here is net-negative (token cost, signal erosion).
- **Substantive tier** (a corpus-document body change, a new or edited gate or linter, a multi-surface change, a control-code / citation / normative-value change): ONE skeptical verifier subagent, pre-push, scoped to the diff, briefed to refute. It catches defects before CI and merge (cheaper than a post-merge catch plus a hot-fix) and is the mechanism that sustains quality across a long session, which is why work size or session length is never itself a reason to wind down (see the consuming project's wind-down framework).
- **Sensitive tier** (gate-blind correctness AND delicate scale AND high escaped-error cost, all three): the full [`high-assurance-verification.md`](high-assurance-verification.md) harness (two independent adversarial verifiers, deterministic apply). Unchanged; the substantive tier is its lighter sibling, not a replacement.

When genuinely in doubt between tiers, run the verifier: a false escalation costs one subagent, a false de-escalation ships a defect.

### The verifier-finding handling loop

A verifier finding is a hypothesis, not a fact, until the orchestrator validates it (per [`evidence-grounded-completion.md`](evidence-grounded-completion.md) and [`validate-inference-before-action.md`](validate-inference-before-action.md)):

1. **Validate** the finding against the artefact. If it is correct, fix; if it is genuinely a false positive, see "Overruling" below.
2. **Fix** the artefact, then **re-verify** (dispatch the verifier again on the fixed state).
3. **Loop cap, three iterations.** If a finding is not resolved after a third verify-fix iteration, STOP: do not force the change through. Defer the change pending the maintainer's review, recording the unresolved finding where the project keeps its decision queue.

### Overruling a verifier is never silent

The orchestrator may judge a finding incorrect and proceed against it, but only with a logged override. Record, in the project's durable override register, (a) the finding verbatim, (b) the validation reasoning for overruling it, and (c) the exact commit / diff / state needed to REVERT the change if the override proves wrong. An override with no recorded revert path is prohibited: the point of the log is that a wrong override can be cleanly undone.

An override made in an overnight or otherwise unattended run is surfaced to the maintainer at the next attended boundary: the end of the unattended run, the return to attended mode, or at latest the next session resume (which reads the override register alongside the other standing registers). An un-reviewed override is a standing item the maintainer clears, exactly as a pending decision is; it is never silently closed.

The override register and the resume-surfacing step are the project's operationalization; this rule states the discipline, the project wires the file and the resume hook.

---

## Prohibited anti-patterns

Across all five disciplines:

- **Pasting worker prose unverified.** The discipline is "verify, correct, integrate", not "trust the worker's draft as-is".
- **Skipping the orchestrator's re-read.** The orchestrator must open each target file at apply-time. "The worker quoted it correctly last week" is not verification.
- **Silent corrections.** Worker errors caught at apply-time should be documented, not silently overwritten. The CHANGELOG-detailed "Discipline observation" is the audit trail.
- **Parallel applies.** Two PRs being authored at the same time is state confusion waiting to happen. Apply one at a time.
- **Bundling unrelated work to "save a PR."** The cost saving is illusory; the audit-trail cost is real.
- **Idle waiting during CI.** If the next PR's research is queued, read it during the wait. If no research is queued, dispatch one.
- **Editing main during a CI wait.** Main belongs to the current PR's merge target; treat it as read-only during the wait.
- **Orchestrator-side judgment-call skipping OR abbreviation of mandatory QA / testing steps.** When the project's discipline says a quality-assurance step (per-PR validation sweep, post-merge regression check, paired-skill parity check, etc.) runs on every PR, the orchestrator does NOT have discretion to skip a specific run based on a unilateral judgment that the PR is "circular", "housekeeping", "meta", "too small to need it", "already validated by another mechanism", or any other class. **Equally, the orchestrator does NOT have discretion to substitute an abbreviated check, a spot-check, a memory-only review, an orchestrator-self-check, a "quick scan", or any other informal substitute for the formal QA invocation the discipline encodes.** The two failures share a shape (the formal step the maintainer expects to run did not run) and the same remedy (run the formal step, record the result). The discipline is mandatory; carve-outs require maintainer authorization, recorded explicitly in the relevant history row's Summary cell with rationale. **Throughput pressure does not authorize abbreviation.** A long batch of PRs about to land, a tight session window, or an apparent need to make progress is not a reason to substitute an informal check for the formal one; the per-PR QA cadence IS the pace, and "I'll catch it on the next one" is the failure mode this clause prevents. The failure mode is: orchestrator skips or abbreviates a QA step that the maintainer expects to run, the abbreviation leaves a defect uncaught, and the next maintainer review discovers both the defect AND the discipline gap. The fix is to ship the QA invocation even when the orchestrator believes it will return zero findings; the zero-finding history row IS the proof-of-discipline, and "abbreviated, 0 findings" is not a substitute for "formal run, 0 findings". **The one standing exception is the session-closing handoff PR**: the final PR of a session, whose purpose is to land working-state on the protected branch as a green merge so the next session resumes from that branch, skips its own trailing per-PR QA. The reason is loop-termination, not discretion: running the per-PR QA on the handoff PR would produce a record (and possibly fixes) that recursion-avoidance batches into a new PR, whose merge would trigger the QA again, with no terminating next substantive PR at the session boundary. The compensating control is stronger than the skipped per-PR sweep, a full corpus-wide validation sweep at the next session's start, which re-examines the whole corpus rather than only the handoff PR's diff; the exemption is a maintainer-authorized standing rule recorded inline in the relevant history row with this rationale, and any mechanical QA-cadence gate must build in the handoff-PR exemption so it does not fail on the legitimately-absent row.

---

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 |
| --- | --- | --- | --- |
| Audit trail of orchestrator corrections | PS.1, RV.2 | LOG-02, LOG-08 | A.8.15, A.5.36 |
| Verification before action | RV.1, RV.2 | GRC-05 | A.5.36 |
| Change classification at PR boundaries | PO.5 | CCC-01 to 03 | A.5.4, A.8.32 |
| Idle-time productive use | PO.5 | n/a | n/a |

The disciplines implement the same audit-trail-integrity principle the broader pack expresses: every claim a downstream reader is asked to rely on must be traceable to a verification step, and the discipline of producing those verification steps must be regular enough that the audit trail is dense rather than sparse.

---

## Why this rule exists

The five disciplines were developed during a multi-week corpus-remediation session in which an AI assistant drove 30+ PRs to close a fitness-review backlog. The session surfaced each failure mode in turn:

- **Research-assistant discipline** emerged after a worker confabulated a non-existent file path; the discipline was named so future workers would be treated as research, not as final prose.
- **Pipeline PR construction** emerged after early sessions were bottlenecked on serial research-then-apply; parallel research was added to keep the apply-queue non-empty.
- **Apply-time worker correction** emerged after several worker drafts referenced stale version numbers or wrong PR cross-references; documenting the catches turned them into a tracking signal.
- **Always split when in doubt** emerged after a maintainer noted that bundled PRs were harder to review than single-purpose ones; "split" became the default.
- **Background work during CI waits** emerged after a maintainer asked whether idle waits were necessary; they weren't, and read-only prep was identified as the safe productive use.

Each discipline pays back its complexity many times over the course of a long session. The cost of memorizing them is small; the cost of relearning them by repeated failure is large.

For AI coding assistants specifically: when you find yourself dispatching multiple workers in parallel, when you find yourself bundling changes, when you find yourself sitting idle during CI, when you find yourself pasting worker prose without re-reading the target file, pause and run the corresponding discipline. The disciplines exist because each failure mode was observed; the discipline keeps the failure mode from recurring.
