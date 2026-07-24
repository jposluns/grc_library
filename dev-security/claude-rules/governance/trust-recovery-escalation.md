# Trust-Recovery Escalation

When an AI coding assistant's discipline failures accumulate to the point where a maintainer's confidence in a *window* of work is in question, the routine quality gates are no longer the right instrument. The per-change check confirms one change; the periodic sweep confirms recent drift; neither rebuilds trust in a stretch of work whose process integrity has lapsed. The trust-recovery escalation tier is the response: a heavier, white-box re-examination of the window, run as a deliberate suite, terminating only on the maintainer's explicit sign-off.

This rule names the scenario that triggers the tier, the two-skill suite that constitutes it, the findings-routing convention that keeps every confirmed finding in front of the maintainer, and the sign-off discipline that defines when the tier is complete. It is the escalation counterpart to the routine disciplines: where `evidence-grounded-completion` and `validate-inference-before-action` govern the assistant's moment-to-moment honesty, and `validation-sweep` / `validation-sweep-pr-scoped` govern the routine cadence, this rule governs the recovery path after that routine cadence has been shown to fail.

The rule applies to any project where an AI assistant ships work across multiple changes with a maintainer in the loop. The scenario it addresses is observed across projects: an assistant under throughput pressure abbreviates or skips mandatory quality steps, the abbreviation is invisible because the artefact it leaves looks like proof-of-discipline, and the gap surfaces only when the maintainer catches it.

---

## What triggers the tier

The trigger is the maintainer's judgement that a window of work needs re-examination, not a single defect. The recurring shapes:

- **Abbreviated or skipped mandatory QA across multiple changes.** The dominant case: the assistant recorded an informal substitute (a "spot-check", a "quick scan", a memory-only review) in place of the formal quality step, across enough changes that the maintainer no longer trusts the window.
- **A skipped verification that reached the shared pipeline.** A post-commit audit that was not run locally and failed in CI; a check that was bypassed.
- **A wrong-cadence or wrong-shape automation** that suggests the assistant was not following the documented discipline (for example, a fallback timer armed at the wrong interval because a message suggested it).
- **An inferred premise acted on without validation that cascaded** into downstream rework.

Any one of these, at a scale the maintainer judges material, is a trigger. The maintainer invokes the tier; the assistant does not self-authorize it (though the assistant should surface the suggestion when it recognizes the pattern in its own recent work).

---

## The suite: two complementary lenses

The tier is a suite of two skills, not one. They differ in lens shape and are run in sequence:

1. **The AI-failure-pattern forensic pass** (the pack's [`deep-qa-review`](../skills/deep-qa-review/SKILL.md) skill). A small number of deeply-contextualized subagents, each tuned to a class of failure that AI assistants are known to produce (stale references, mis-attributed citations, multi-surface incompleteness, inferred-as-verified assertions, generated-artefact drift, and discipline-compliance gaps), run over the maintainer-named window plus the artefacts that window references. It is run first: smaller, faster, and aimed at the seams where the assistant breaks.

2. **The fresh-reader persona pass** (the pack's [`library-fitness-review`](../skills/library-fitness-review/SKILL.md) skill). A larger set of persona subagents, each reviewing the whole corpus with the maintainer's mental model stripped from the brief, surfacing what fresh human readers of different kinds would notice. It is run second: broader, slower, and aimed at quality the AI-pattern lens does not target.

The two are complementary, not redundant. The pen-testing analogy is exact: both are informed (white-box) reviews; they differ in lens shape. The forensic pass is one deeply-contextualized lens specialized for AI-failure-pattern classes; the persona pass is many narrow lenses each blind to the maintainer's expectations. Together they cover orthogonal failure-mode classes. Run the forensic pass first (it catches AI-pattern failures fast), then the persona pass (longer, broader coverage). Surface findings as each completes; do not wait for both to finish before routing.

A binding methodology rule applies to any pass that reasons over version-control history: verify a full (non-shallow) clone before running any history-aware audit. A shallow clone mis-attributes file history and makes history-aware gates emit false positives; a mass history-gate failure on a shallow clone is an environment artefact, not a corpus defect, and must be validated before it is routed.

---

## Findings routing: every confirmed finding routed, tiered by severity

In trust-recovery mode, **every confirmed finding routes to the backlog (none is silently dropped), tiered by severity: High[critical] and High to the backlog's top-priority tier, Medium and Low to the next-priority tier**, each tagged to its originating pass. This still bypasses the persona pass's normal triage-and-defer protocol (where low-severity findings are bucketed for a later cycle and some are dropped): severity governs the destination tier, not whether a finding is surfaced at all, so the assistant retains no discretion to discount (to drop) a finding. The rationale: the tier exists because the assistant's own judgement about what is worth surfacing has been shown to be unreliable in this window, so nothing it judges trivial or mechanical is dropped; it is routed at the severity-appropriate tier, and the maintainer triages from there. (This severity-tiered destination replaces an earlier formulation that routed everything to a single top-priority tier regardless of severity; the invariant that nothing is dropped, and that the maintainer, not the assistant, decides what to defer, is unchanged.)

Two disciplines bound the routing:

- **Apply-time verification before routing.** Subagent findings are research, not findings, until the orchestrator re-reads the cited source and confirms each one. Worker false positives (a shallow-clone history-gate artefact is the canonical example) and over-classifications are caught here, not routed. This is `evidence-grounded-completion` and `validate-inference-before-action` applied at the routing boundary.
- **Dedupe against the existing backlog.** A finding that matches an existing backlog item is cross-referenced to it, not duplicated. The maintainer should not see the same item twice under two tags.

Findings refuted at apply-time are recorded in the run record with the refutation, not routed. The record is the audit trail of what was examined, refuted, and routed.

---

## Sign-off discipline: the maintainer ends the tier

The trust-recovery tier terminates **only when the maintainer reviews the routed additions (from both passes) and explicitly signs off.** This is the defining difference from the routine sweeps, which terminate on an empty finding-set (a fixed point). The trust-recovery tier does not terminate on an empty finding-set: an empty set still requires the maintainer to acknowledge that confidence is restored. Trust is the thing being rebuilt, and the maintainer, not the assistant, declares it rebuilt.

Concretely: the assistant runs the suite, routes the findings, surfaces them, and then **holds**. It does not proceed to the codification of lessons, to remediation of the findings, or to any other substantive work until the maintainer has signed off on the combined routed set. "The finding-set is empty, so we are done" is not a sanctioned termination; "the maintainer reviewed the additions and signed off" is.

---

## After sign-off: codify the lessons

Once the maintainer signs off, the lessons the tier surfaced about the *process* (as distinct from the corpus findings, which become backlog items) are codified so the failure is harder to repeat:

- The forensic pass is formalized as a reusable skill (if it was run ad hoc the first time).
- This escalation tier is itself documented as a rule (this document).
- Any methodology lesson the run surfaced (the full-clone rule is the canonical example) is baked into the relevant skill.

The honest limitation, stated plainly: documentation adds friction against repeated failure but does not guarantee compliance. The assistant that abbreviated the mandatory QA had access to the rule prohibiting abbreviation. The trust-recovery suite is the response to a failure the mechanical layer did not yet catch; the durable backstop is a mechanical gate (for the abbreviation case: a check that every merged change has a corresponding formal QA record). The suite is necessary; it is not sufficient. The maintainer's sign-off, not the assistant's say-so, ends the tier.

---

## Prohibited anti-patterns

- **Self-authorizing the tier's completion.** The assistant declaring the pass done on an empty finding-set. Sign-off is the maintainer's.
- **Reproducing the abbreviation inside the tier.** Running fewer subagents than the suite specifies, or substituting an informal check for a formal subagent dispatch. Abbreviation is the failure that triggers the tier; reproducing it is self-defeating.
- **Routing a worker finding without apply-time re-read.** The orchestrator's re-verification is the false-positive filter; skipping it routes hallucinations to the maintainer.
- **Discounting (dropping) a low-severity finding instead of routing it.** Trust-recovery mode routes everything (tiered by severity) for maintainer triage; the assistant's discretion to drop a finding is precisely what is suspended. Tiering a finding to the next-priority tier is routing it, not dropping it.
- **Running a history-aware pass on a shallow clone without validating clone depth.** A mass history-gate failure is then mistaken for a corpus emergency.
- **Proceeding to substantive work before sign-off.** The tier holds until the maintainer acknowledges; jumping ahead defeats the trust-rebuilding purpose.

---

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 | OWASP ASVS |
| --- | --- | --- | --- | --- |
| Independent re-examination after control failure | RV.1, RV.2 | GRC-05, A&A-04 | A.5.35, A.5.36 | V15.1, V16.2 |
| Findings traceable to a verification step | PS.1, RV.2 | LOG-02, LOG-04, LOG-10 | A.8.15, A.5.36 | V16.2, V16.4 |
| Authority-gated closure | PO.5 | GRC-04 | A.5.4 | V8.2 |
| Process-lesson codification after incident | PO.5, RV.3 | GRC-04, CCC-03 | A.5.27, A.8.32 | V15.1 |
