# Executive Narrative Subtype Templates

**Document Title:** Executive Narrative Subtype Templates\
**Document Type:** Template\
**Version:** 1.0.3\
**Date:** 2026-08-08\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`specification-executive-narrative.md`](../specification-executive-narrative.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual, and upon material change to the Executive Narrative Authoring Specification\
**Repository Path:** [`governance/template-executive-narrative-subtypes.md`](template-executive-narrative-subtypes.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

## 1. Purpose

This template holds a copyable skeleton for each of the seven executive-narrative subtypes defined in the [Executive Narrative Authoring Specification](../specification-executive-narrative.md): Executive Brief, Scenario, Decision Narrative, Oversight Question Set, Story, Journey, and Outcome Map. Each skeleton carries the required metadata block, the universal authority disclaimer, and the subtype's mandatory section order, so an author starts from a conforming shape rather than assembling one by hand.

The templates live here, in the governance domain, rather than under the `executive/` narrative tree, because a live page under `executive/` is a published narrative page: it would become a narrative-registry row and surface as content before any real content exists. A fenced skeleton in this corpus document is documentation, not a page, so it publishes nothing.

## 2. How to use these templates

1. Copy the fenced skeleton for the subtype you are authoring (the content inside the triple-backtick block, not the fence markers).
2. Create the new file under the subtype's subdirectory in `executive/`, named with the subtype's filename prefix (for example `executive/briefs/brief-<topic>.md` for an Executive Brief). Each subtype's subdirectory is fixed by the subtype table in the specification, and the narrative metadata gate enforces it. Keep the file name to the subtype prefix plus three or four further words naming the topic (for example `executive/briefs/brief-ai-supply-chain-oversight.md`); the page title, not the file name, carries the full leadership question.
3. Replace every bracketed placeholder and each example value. In particular: set a real `Corpus Sources` list (each entry a plain markdown link to a corpus document the page relies on, with no version suffix), the correct `Narrative Type` and its fixed `Narrative Status`, the present `Claim Classes Present`, a `Review Record` identifier, and a `Last Reviewed` date.
4. Keep the authority disclaimer verbatim as the first body content after the metadata block; it is fixed by the specification and identical on every page.
5. Run the narrative gates against the new page before committing.

The example values in each skeleton are chosen so that a skeleton copied to its subtype's subdirectory under `executive/`, renamed to its prefix, resolves against the narrative metadata gate with minimal editing. `Corpus Sources` records dependency paths only: an executive page refers to corpus documents but never pins a version, so a corpus version change never invalidates a page. `Last Reviewed` is an advisory editorial-freshness date on a six-month cadence, not a gated requirement.

## 3. The seven subtype skeletons

### 3.1 Executive Brief (`brief-`)

```markdown
# [Executive Brief title in sentence case]

**Document Title:** [Executive Brief title in sentence case]\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-08-06\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/guide-ai-board-oversight.md`](../../ai/guide-ai-board-oversight.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/briefs/brief-example-topic-area.md`](brief-example-topic-area.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Executive Brief\
**Narrative Status:** Explanatory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`ai/guide-ai-board-oversight.md`](../../ai/guide-ai-board-oversight.md)\
**External Sources:** None\
**Claim Classes Present:** citation\
**Review Record:** NR-2026-001\
**Last Reviewed:** 2026-08-06

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Why this matters

One or two paragraphs framing the leadership stake in plain executive register. State the concern, not the mechanics.

## What the corpus establishes

Restate, in executive language, what the linked corpus sources establish. Point to each value in the corpus; never reproduce it here.

## What this means for the organization

Translate the corpus position into what the reader's organization should understand. This creates no new requirement.

## Evidence to request

What the reader should ask management for, expressed as evidence classes (reports, registers, test results, attestations). Each item is evidence for a named control or outcome.

## Limitations

At minimum: this page creates no compliance; the adopting organization validates applicability; and any subtype-specific caution.

**End of Document**
```

### 3.2 Scenario (`scenario-`)

```markdown
# [Scenario title in sentence case]

**Document Title:** [Scenario title in sentence case]\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-08-06\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`risk/register-scenario-risk-catalogue.md`](../../risk/register-scenario-risk-catalogue.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/scenarios/scenario-example-topic-area.md`](scenario-example-topic-area.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Scenario\
**Narrative Status:** Non-normative\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`risk/register-scenario-risk-catalogue.md`](../../risk/register-scenario-risk-catalogue.md)\
**External Sources:** None\
**Claim Classes Present:** composite\
**Review Record:** NR-2026-001\
**Last Reviewed:** 2026-08-06

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Scenario premise

Set up a composite, fictional situation. Describe no identifiable organization or actual incident.

## How the event unfolds

Narrate the sequence at executive altitude. Make no likelihood, frequency, or statistical claim.

## Where the corpus controls engage

Point to the corpus controls the scenario exercises, using the causal vocabulary (contribution, dependency, prevention, evidence).

## What good looks like

Describe the well-governed outcome the corpus controls support. This equips discussion; it recommends no control selection.

## Evidence to request

Evidence classes the reader should ask management for, each evidence for a named control or outcome.

## Limitations

State the illustrative and composite nature: fictional, no likelihood or frequency claim, no compliance created, and the adopting organization's own validation required.

**End of Document**
```

### 3.3 Decision Narrative (`decision-`)

```markdown
# [Decision Narrative title in sentence case]

**Document Title:** [Decision Narrative title in sentence case]\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-08-06\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/decision-narratives/decision-example-topic-area.md`](decision-example-topic-area.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Decision Narrative\
**Narrative Status:** Advisory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md)\
**External Sources:** ISO 31000\
**Claim Classes Present:** citation, sourced, composite\
**Review Record:** NR-2026-001\
**Last Reviewed:** 2026-08-06

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## The decision in front of leadership

State the choice the reader's organization faces, in one or two sentences.

## What the corpus provides

Point to the corpus sources that inform the decision. A sourced claim names its external standard inline.

## Options and their consequences

Lay out the options and what each implies, using the causal vocabulary. The decision itself remains entirely with the reader's organization.

## Questions to resolve before deciding

The open questions leadership answers before choosing.

## Evidence to request

Evidence classes to ask management for, each evidence for a named control or outcome.

## Limitations

This page creates no compliance and prescribes no outcome; the adopting organization validates applicability. Composite content present, so the reader's organization validates the synthesized position against its own context.

**End of Document**
```

### 3.4 Oversight Question Set (`oversight-questions-`)

```markdown
# [Oversight Question Set title in sentence case]

**Document Title:** [Oversight Question Set title in sentence case]\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-08-06\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/guide-ai-board-oversight.md`](../../ai/guide-ai-board-oversight.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/oversight-question-sets/oversight-questions-example-topic-area.md`](oversight-questions-example-topic-area.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Oversight Question Set\
**Narrative Status:** Advisory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`ai/guide-ai-board-oversight.md`](../../ai/guide-ai-board-oversight.md)\
**External Sources:** None\
**Claim Classes Present:** citation\
**Review Record:** NR-2026-001\
**Last Reviewed:** 2026-08-06

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Context for these questions

Frame why this line of questioning matters and what corpus area it draws on.

## Questions

Group the questions by theme. Pair each question with a note on what a strong answer contains.

### Theme A

- Question. Strong answer: what a well-evidenced response looks like.

### Theme B

- Question. Strong answer: what a well-evidenced response looks like.

## Evidence to request

Evidence classes the reader should ask management for, each evidence for a named control or outcome.

## Limitations

This page organizes questioning; it prescribes no answer and creates no compliance. The adopting organization validates applicability.

**End of Document**
```

### 3.5 Story (`story-`)

```markdown
# [Story title in sentence case]

**Document Title:** [Story title in sentence case]\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-08-06\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`risk/register-scenario-risk-catalogue.md`](../../risk/register-scenario-risk-catalogue.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/stories/story-example-topic-area.md`](story-example-topic-area.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Story\
**Narrative Status:** Non-normative\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`risk/register-scenario-risk-catalogue.md`](../../risk/register-scenario-risk-catalogue.md)\
**External Sources:** None\
**Claim Classes Present:** composite\
**Review Record:** NR-2026-001\
**Last Reviewed:** 2026-08-06

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Setting

Establish a composite, fictional setting. Describe no identifiable organization or actual incident.

## The story

Tell the narrative at executive altitude. Make no likelihood, frequency, or statistical claim.

## What the story illustrates

Draw out the governance point the story makes legible.

## Where the corpus controls appear

Point to the corpus controls the story surfaces, using the causal vocabulary.

## Evidence to request

Evidence classes the reader should ask management for, each evidence for a named control or outcome.

## Limitations

State the illustrative and composite nature: fictional, no likelihood or frequency claim, no compliance created, and the adopting organization's own validation required.

**End of Document**
```

### 3.6 Journey (`journey-`)

```markdown
# [Journey title in sentence case]

**Document Title:** [Journey title in sentence case]\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-08-06\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/charter-governance-library.md`](../../governance/charter-governance-library.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/journeys/journey-example-topic-area.md`](journey-example-topic-area.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Journey\
**Narrative Status:** Explanatory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`governance/charter-governance-library.md`](../../governance/charter-governance-library.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-001\
**Last Reviewed:** 2026-08-06

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Starting state

Describe where the journey begins.

## Stages

Walk the stages in order. For each stage, state what changes, which corpus documents engage, and the signals of progress.

### Stage 1

What changes. Corpus documents that engage. Signals of progress.

### Stage 2

What changes. Corpus documents that engage. Signals of progress.

## Destination state

Describe the end state the journey reaches.

## Evidence to request

Evidence classes the reader should ask management for, each evidence for a named control or outcome.

## Limitations

This page explains a path; it creates no compliance and prescribes no outcome. Composite synthesis requires the adopting organization's own validation, and applicability must be validated.

**End of Document**
```

### 3.7 Outcome Map (`outcome-map-`)

```markdown
# [Outcome Map title in sentence case]

**Document Title:** [Outcome Map title in sentence case]\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-08-06\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/outcome-maps/outcome-map-example-topic-area.md`](outcome-map-example-topic-area.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Outcome Map\
**Narrative Status:** Explanatory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md)\
**External Sources:** None\
**Claim Classes Present:** citation\
**Review Record:** NR-2026-001\
**Last Reviewed:** 2026-08-06

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Outcome statement

State the outcome the map is about, in one sentence.

## Contribution map

Each row relates one corpus control to the outcome using exactly one causal-vocabulary word (contribution, dependency, prevention, or evidence).

| Corpus control | Relationship | Note |
| --- | --- | --- |
| [corpus control, linked] | contribution | how it advances the outcome without being sufficient for it |
| [corpus control, linked] | dependency | the outcome requires this control or condition to hold |

## Gaps and dependencies

(Optional.) Named gaps and dependencies the map surfaces.

## Evidence to request

Evidence classes the reader should ask management for, each evidence for a named control or outcome.

## Limitations

This page maps contributions; it creates no compliance, presents no adoption as effectiveness, and requires the adopting organization's own validation.

**End of Document**
```

## 4. Conformance notes

- The metadata field order is the thirteen canonical fields followed by the eight narrative-extension fields, ending on `Last Reviewed` (the block's bare last line, no trailing backslash).
- Every `Corpus Sources` entry references a corpus document that lives outside `executive/`; a reference to a sibling under `executive/` or an out-of-corpus path is rejected by the narrative metadata gate.
- Narrative prose states contribution, dependency, prevention, or evidence, and avoids absolutes and unqualified archaic normative verbs; the vocabulary gate scans every narrative page.
- Em dashes and en dashes are not used anywhere; commas, colons, and parentheses carry the same load.

**End of Document**
