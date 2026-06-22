---
name: deep-qa-review
description: Trust-recovery deep quality-assurance pass. A six-subagent forensic review specialized for AI-failure-pattern classes, run over a defined PR window plus the files those PRs reference, when an AI coding assistant's discipline failures (abbreviated QA, skipped post-commit audits, wrong-cadence timers, inferred-not-validated premises) call for a white-box re-examination beyond the routine per-PR and periodic sweeps. Slash command `/full-qa`. Pairs with `library-fitness-review` (`/fitness`): deep-qa-review is one deeply-contextualised lens tuned to how AI assistants fail; fitness is ten context-stripped persona lenses. Together they form the trust-recovery escalation tier. Findings route to the project backlog tiered by severity (High[critical]/High to the top-priority tier, Medium/Low to the next tier), none dropped, for maintainer triage; the pass terminates on explicit maintainer sign-off, not on an empty finding-set.
derives_from: ../../governance/evidence-grounded-completion.md
---

# Deep QA Review (trust-recovery forensic pass)

## Overview

The per-PR validation sweep (`/validate-pr`) catches what a single merge introduced; the corpus-wide sweep (`/validate`) catches drift across a sweep interval; the fitness review (`/fitness`) catches what fresh human-persona readers would notice. None of these is built for the case where the *process itself* has failed: an AI coding assistant that abbreviated mandatory QA across many PRs, skipped a post-commit audit, armed a wrong-cadence timer, or acted on an inferred premise it never validated. When that happens, the maintainer's trust in the recent run is the thing that needs rebuilding, and a heavier, white-box re-examination is the response.

`deep-qa-review` is that re-examination's AI-failure-pattern lens. It is a six-subagent forensic pass over an explicitly-widened PR window (not the routine two-day focus) plus every file those PRs' CHANGELOG entries reference. Each subagent is a deeply-contextualised reviewer that knows the prior session's specific failure modes and hunts the classes those failures belong to. It is the complement of `library-fitness-review`: where fitness strips the maintainer's mental model from ten persona briefs to get fresh-reader coverage, deep-qa-review keeps full context and aims its lenses at the seams where AI assistants are known to break (stale references, mis-attributed citations, multi-surface incompleteness, inferred-as-verified assertions, generated-artefact drift, and discipline-compliance gaps).

The two skills run as a suite (the trust-recovery escalation tier): `/full-qa` first (smaller, fast, AI-pattern-tuned), then `/fitness` (broader, slower, persona-tuned). The escalation tier and its routing-and-sign-off discipline are codified in the pack rule [`trust-recovery-escalation.md`](../../governance/trust-recovery-escalation.md).

## When to Use

- **After an AI coding assistant's discipline failure** that the maintainer judges severe enough to warrant re-examining a run rather than just the latest PR: abbreviated or skipped mandatory QA across multiple PRs; a skipped post-commit/pre-push audit that reached CI; a wrong-cadence subscription timer; an inferred premise acted on without validation that cascaded. The trigger is the maintainer's loss of confidence in a window of work, not a single defect.
- **Before a major external reliance event** when the recent run's QA discipline is in question.
- **As the first half of the trust-recovery suite** (`/full-qa` then `/fitness`), on maintainer invocation.

**No orchestrator-side skip or abbreviation discretion.** Like `/validate` and `/validate-pr`, this skill has no carve-outs. Once the maintainer invokes the trust-recovery suite, the orchestrator does NOT have discretion to skip a subagent, to run fewer than six, or to substitute an abbreviated check, a spot-check, a memory-only review, or a "quick scan" for the formal dispatch. The only sanctioned exception is a maintainer-authorised scope reduction recorded in the run's history/record. Abbreviation is the failure mode that triggers this skill in the first place; reproducing it inside the skill is self-defeating.

## Process

### 0. Verify a full (non-shallow) clone BEFORE any git-history-aware step

**Binding methodology rule.** This pass reasons over git history (subagents diff PR windows, run `git log --follow`, and run the audit suite whose gates 31 and 40 are git-history-aware). On a shallow clone, `git log --follow` mis-attributes a file's last-commit date to the shallow boundary commit, which makes the document-date-staleness gate (31) and version-bump-recency gate (40) emit false positives for every file whose real history predates the boundary.

Before anything else:

```
git rev-parse --is-shallow-repository    # must print false
# if true:
git fetch --unshallow                    # restore full history
```

Then confirm the mechanical baseline (`tools/run_all_audits.sh` exit 0) on the full clone. A subagent that reports a mass git-history-gate failure (e.g. "gate 31 fails on N documents") on a shallow clone is reporting an environment artifact, not a corpus defect; the orchestrator MUST validate clone depth before routing any such finding. This rule exists because iteration 1 (2026-06-22) caught exactly this: a subagent reported gate 31 failing on 153 documents; the container was a depth-50 shallow clone; after `git fetch --unshallow` the audit exited 0 and the failure did not reproduce. A less strict pass would have shipped a 153-document false emergency.

### 1. Establish the window and the mechanical baseline

- **Window**: the PR range the maintainer names (or the full span of the run whose discipline is in question), expressed as a commit range. Enumerate it (`git log <base>^..<head> --oneline`); for squash-merge projects each subject carries its `(#N)`.
- **Referenced files**: every file cited from the window PRs' CHANGELOG-detailed entries is in scope alongside the diffs.
- **Baseline**: `tools/run_all_audits.sh` exit 0 on the full clone (step 0). If a gate fails for a real reason, fix it first; if it fails as a shallow-clone artifact, unshallow and re-run.

### 2. Dispatch six subagents

All six are dispatched on every full run. Each receives a self-contained brief carrying the shared preamble (below) plus its specific lens.

- **A, recent-PR deep review**: read every window PR's diff and the full post-merge state of touched files; hunt the eight validation-sweep failure classes (stale references, mis-attributed citations, multi-surface incompleteness, inferred-as-verified assertions, version/date-bump omissions, generated-artefact lag, stale docstrings, cross-document term drift), with special focus on any multi-surface change the prior run may have propagated incompletely.
- **B, corpus-wide stale-reference sweep**: confirm the canonical version/count values from live files first; run the pre-flight scanner; hunt stale counts, version literals, and dates corpus-wide.
- **C, audit-programme integrity**: verify the four parity surfaces agree (CI workflow, runner, pre-commit, audit-programme spec), the paired-skill registry is complete, the pack-README skills table matches the skills directory, and any touched linter's docstring matches its code. Run the audit suite and report its exit code.
- **D, citation forensic**: enumerate every external-standard citation introduced or modified in the window; verify each against the canonical-citations register and, for clause content, against authoritative sources via WebFetch (fall back to register-only and flag `unverified-against-source` if the network policy blocks WebFetch).
- **E, generated-artefact forensic**: discover the generators; re-derive each generated artefact (`--check` mode) AND independently regenerate-and-diff; any drift is a finding regardless of CI state.
- **F, discipline-violation forensic**: examine every window PR against the project's governance rules (including any rule the window itself added); specifically verify each PR had a formal `/validate-pr` record (any "abbreviated"/"spot-check" row is a violation finding), CHANGELOG lock-step, Version+Date co-bump, and a `/retro` row.

#### Shared preamble (prepended to every subagent brief)

- **Evidence bar (hard gate)**: every finding MUST quote the actual source line as `path:line`. A finding without a quoted line is a hypothesis, not a finding; drop it or verify by reading.
- **Pre-tool falsification**: before each tool call, state in one line (a) the hypothesis it tests, (b) the observation that would falsify it, (c) one prior result that does not already answer it. Undefined falsifier means corroboration-only; skip.
- **Inference discipline at maximum strictness**: any "since/because/given X, [conclusion]" where X is a state claim not observed in this dispatch fires a mandatory validation read before the conclusion is relied on. (This is the rule the prior run violated; the pass enforces it on itself.)
- **Output**: SARIF-lite blocks (tool, ruleId, level, location, fingerprint, rubric, evidence quote).
- **Research, not findings**: the subagent produces research; the orchestrator re-verifies every finding against source before it is actioned.

### 3. Synthesize and verify at apply-time

The orchestrator dedupes by `(file, section, claim_type)`, tags `R|I|K`, adjudicates severity (pick higher; no averaging), and, critically, **re-reads each cited source location before routing any finding**. Worker false positives (the shallow-clone gate-31 artifact is the canonical example) and over-classifications are caught here, not shipped. Apply-time corrections are logged to the project's worker-hallucination tracking artefact.

### 4. Route every confirmed finding to the backlog, tiered by severity

In trust-recovery mode, **every confirmed finding routes to the backlog (none silently dropped), tagged `[full-qa]`, tiered by severity: High[critical] and High to the top-priority tier, Medium and Low to the next-priority tier**, including findings the orchestrator judges trivial or mechanical. The maintainer triages from there; the orchestrator does not silently drop low-severity items or defer them to a sweep-close-out, but tiers them by severity (tiering is routing, not dropping). Findings that dedupe against an existing backlog item are cross-referenced, not duplicated. Findings refuted at apply-time (false positives) are recorded in the run record with the refutation, not routed.

### 5. Record

Write a per-run record (project-specific location; in this project `.working/full-qa/YYYY-MM-DD-iterN.md`) with one section per subagent (A-F), an orchestrator-synthesis-and-verification section, a findings-routed section, and a trust-recovery-framing section naming the prior run's discipline failures and the elevated rules applied. Append a history row. The record directory carries a README codifying the step-0 full-clone rule.

### 6. Termination is maintainer sign-off, not empty-delta

Unlike `/validate`'s fixed-point loop, the trust-recovery pass terminates only when the maintainer reviews the routed additions (from both `/full-qa` and `/fitness`) and explicitly signs off. An empty finding-set does not terminate the pass; maintainer acknowledgement does. This is the trust-rebuilding step: the maintainer, not the assistant, declares confidence restored.

## Red Flags

- A git-history-gate mass failure reported without a clone-depth check (step 0). Validate before routing.
- A finding without a quoted `path:line` (it is a hypothesis).
- Routing a worker finding without the orchestrator's own re-read (apply-time verification is the false-positive filter).
- Discounting a low-severity finding instead of routing it for maintainer triage.
- Treating an empty finding-set as the termination condition (sign-off is).
- Reproducing the abbreviation that triggered the pass (running fewer than six subagents, or substituting an informal check).

## Verification

The pass is complete on a given run when: clone depth was verified full before any git-history-aware step; the mechanical baseline was clean on the full clone; all six subagents were dispatched and returned evidence-quoted findings; the orchestrator re-read each cited source and refuted or confirmed it; every confirmed finding was routed to the top-priority backlog tier tagged `[full-qa]`; the per-run record and history row were written; and the maintainer has signed off on the combined trust-recovery additions.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "CI is green, so the corpus is fine." | CI on a shallow clone can be green while a subagent on the same clone reports a git-history-gate failure, or vice versa. Verify clone depth; trust the full-clone audit. |
| "This subagent's finding is obviously real; route it." | The shallow-clone gate-31 artifact looked like 153 real failures. Re-read the source before routing every finding, especially the alarming ones. |
| "The finding is trivial; I'll skip routing it." | Trust-recovery mode routes everything for maintainer triage. The orchestrator's job is to filter hallucinations, not to triage severity. |
| "Six subagents is overkill; A and F overlap." | The overlap is deliberate (A reads an artefact as state; F audits it as a discipline record). Different lenses on the same surface is coverage, not waste. |
| "Empty findings, so we're done." | Sign-off terminates the pass. An empty set still needs the maintainer to acknowledge confidence restored. |

## See Also

- Pack rule [`trust-recovery-escalation.md`](../../governance/trust-recovery-escalation.md): the escalation tier this skill belongs to, with the routing and sign-off discipline.
- Sibling skill [`library-fitness-review`](../library-fitness-review/SKILL.md) (`/fitness`): the persona half of the trust-recovery suite.
- Canonical rule [`evidence-grounded-completion`](../../governance/evidence-grounded-completion.md): the evidence bar each finding meets.
- Canonical rule [`validate-inference-before-action`](../../governance/validate-inference-before-action.md): the discipline the step-0 clone check and the apply-time re-read operationalize.
- Sibling skills [`validation-sweep`](../validation-sweep/SKILL.md) and [`validation-sweep-pr-scoped`](../validation-sweep-pr-scoped/SKILL.md): the routine sweeps this skill escalates beyond.

## Why this skill exists

The trust-recovery suite was created after a session whose AI assistant abbreviated `/validate-pr` across eleven consecutive PRs, skipped a post-commit audit that then failed CI twice, and armed a 60-minute timer where the project mandates 60 seconds. The mechanical layer had not yet grown a gate to catch the abbreviation; the maintainer's manual catch was the only backstop. `deep-qa-review` is the process-layer response: a heavier, white-box re-examination tuned to the classes of failure an AI assistant produces, run as a suite with the persona-based fitness review. Its first run immediately justified the step-0 rule by catching a shallow-clone false positive that would otherwise have shipped as a 153-document emergency. The skill is necessary but not sufficient: the durable backstop is the mechanical QA-cadence gate, queued separately. Documentation adds friction against repeated failure; it does not guarantee compliance. The maintainer's sign-off, not the assistant's say-so, ends the pass.
