---
name: fresh-reader-validation
description: Before declaring a new or substantively-revised governance document complete, dispatch a fresh subagent with no session context to read the document and surface tacit-context gaps (ambiguous terms, missing definitions, implicit assumptions, unresolved references that the author knows but did not write down). Catches the failure mode the author cannot catch directly: the "I know what I meant" blind spot that fills the document's gaps invisibly during authoring.
derives_from: ../../governance/evidence-grounded-completion.md
---

# Fresh Reader Validation

## Overview

An author who has just written a document carries the document's tacit context in their head. The terms they used, the assumptions they made, the references they treated as obvious, these all feel anchored to the reader from the author's vantage point, because the author has the anchors. A fresh reader, with no project context loaded, has only what is on the page. Where the page leaves something tacit, the fresh reader sees the gap that the author cannot see.

This skill uses a fresh subagent (no session history, no other files loaded, no shared context) to read a newly-authored or substantively-revised governance document and surface the gaps the author's tacit context filled invisibly. The pattern is borrowed from Anthropic's `doc-coauthoring` skill's "fresh-Claude reader testing" stage, re-derived in this pack as a standalone verification step.

The skill targets a defect class the mechanical gates cannot reach: ambiguity that compiles fine. A passive-voice sentence with two reasonable readings is still well-formed markdown; a term used without definition is still a legal identifier; an implicit assumption ("the audit programme runs in CI") is still grammatical prose. The author cannot catch these because they know which reading is correct, who the assumed reader is, and what context the assumed reader carries.

## When to Use

- Before declaring a **new governance document** complete (a new policy, standard, framework, procedure, register, annex). The document is most fragile to tacit-context gaps when it has just been authored.
- Before declaring a **substantive revision** complete when the revision changes the document's meaning (new requirements, new scope, new exceptions, restructured sections). Trivial typo fixes or version bumps do not warrant a fresh-reader pass.
- Before the document is cited by another document in the corpus (a downstream reader is about to depend on the document's clarity).
- When the [`evidence-grounded-completion`](../evidence-grounded-completion/SKILL.md) skill's protocol is being applied and the document is the primary artefact (this skill complements the protocol's re-read step by adding an outside reader).

## Process

1. **Define the success criteria** for the fresh reader. What questions should the reader be able to answer after one read? Examples: "Who is the owner of this control?", "What is the cadence?", "What is the exception process?", "What is the relationship to standard X?". Write these down before dispatching the subagent so the verification is bounded.
2. **Dispatch the fresh subagent**. Use the `Agent` tool (or equivalent) with a brief that loads NO project context. The subagent's brief must include only: the document content (as quoted text or a file path); the success criteria from step 1; instructions to surface any ambiguities, missing definitions, implicit assumptions, or unresolved references.
3. **Receive the subagent's findings**. Read them in full. Each finding is one of:
   - **Ambiguity**: the document supports two or more reasonable readings, and which one is correct cannot be determined from the document alone.
   - **Missing definition**: a term is used without definition, and the reader cannot reasonably infer its meaning from context.
   - **Implicit assumption**: a statement only holds if a prior condition is true, but the prior condition is not stated.
   - **Unresolved reference**: a link, a section reference, a citation, or a cross-document pointer does not resolve to a specific target the reader can follow.
4. **Triage each finding**:
   - **Real gap**: the finding identifies a tacit-context gap that needs to be filled in the document. Resolve by adding the definition, the qualifier, the explicit assumption, or the resolved reference.
   - **False positive**: the finding misreads the document or the subagent's brief did not include sufficient context. Resolve by re-reading the document and confirming the finding is not actually a gap; document the dismissal.
   - **Scope expansion**: the finding identifies a gap the document chose not to fill (e.g., the document references a separate document for the definition). Resolve by confirming the chosen scope and ensuring the cross-reference is well-formed.
5. **Apply the fixes**. After applying, the document has fewer tacit-context gaps. Optionally re-run the skill (a second fresh-reader pass) if the changes were substantial.

## Red Flags

- Dispatching the subagent with the rest of the project's context loaded (defeats the "fresh" condition; the subagent will share the author's blind spots).
- Treating the subagent's findings as suggestions rather than the verification output. Each finding is signal, not noise.
- Dismissing a finding as "obvious" without checking. The finding is precisely what was NOT obvious.
- Skipping the success-criteria step. Without criteria, the subagent's read is unbounded and the verification is unfocused.
- Running the skill but not applying the fixes (the verification surfaces gaps; the maintainer's job is to close them).

## Verification

This skill is complete when:

- Success criteria were defined in writing before the subagent was dispatched.
- A fresh subagent has been dispatched with no project context loaded and has returned findings.
- Each finding has been triaged (real gap / false positive / scope-expansion).
- Real-gap findings have been applied to the document.
- The dismissal of any false-positive finding is documented (so a future reviewer can understand why it was not addressed).

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I just wrote it; I know it's clear." | The "I know it's clear" feeling IS the blind spot. A fresh reader is the test. |
| "The terms are obvious to anyone in this field." | Define your "anyone". The corpus's audience is broader than your immediate peers. |
| "It will be reviewed by humans anyway; they'll catch it." | Humans share authorial blind spots more often than fresh subagents do. The skill is a cheap pre-review step. |
| "The subagent doesn't have the context to judge." | That is the point. The reader who will arrive at the document later also lacks your context. |
| "The audit programme will catch the issues." | The audit programme catches format issues. Tacit-context gaps compile fine. |

## See Also

- Canonical rule [`governance/evidence-grounded-completion.md`](../../governance/evidence-grounded-completion.md): the per-claim verification protocol this skill applies to a new or revised document as a whole.
- Related skill [`evidence-grounded-completion`](../evidence-grounded-completion/SKILL.md): the six-step verification protocol; this skill's fresh-reader pass complements step 2 (re-read each file in full) with an outside reader.
- Related skill [`clarify-before-acting`](../clarify-before-acting/SKILL.md): when the fresh reader surfaces an ambiguity the document chose not to resolve, surface it via clarify-before-acting before completing.
- Related skill [`validation-sweep`](../validation-sweep/SKILL.md): when the sweep surfaces a document that has had substantive revisions, this skill is the per-document follow-up.
