# Skeptical-Verifier Override Register

**Version:** 1.0.1\
**Date:** 2026-07-15\
**License:** CC BY-SA 4.0

The durable, cross-session register for skeptical-verifier **overrides** (the pack rule
[`governance/ai-assistant-workflow-disciplines.md`](../dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md),
"Skeptical pre-push verification" standard, "Overruling a verifier is never silent").

The skeptical pre-push verifier is briefed to refute a substantive change before push. When
it raises a finding, the orchestrator validates the finding (per
[`evidence-grounded-completion`](../dev-security/claude-rules/governance/evidence-grounded-completion.md)
and [`validate-inference-before-action`](../dev-security/claude-rules/governance/validate-inference-before-action.md)):
a correct finding is fixed and re-verified; a finding that survives a third verify-fix
iteration defers the change to maintainer review. The remaining case is the one this register
exists for: the orchestrator judges the finding **incorrect** (a genuine false positive) and
proceeds against it. That is an **override**, and it is never silent.

There is a real risk the assistant drifts or hallucinates and declares the verifier wrong
just to get past it. This register is the control against that risk: every override is logged
with enough information to cleanly REVERT the change if the override later proves wrong, and
every override is surfaced to the maintainer for review. The assistant may debate or overrule
a verifier, but never without this record.

## What every override row must record

1. **The finding, verbatim.** The verifier's finding as written (`path:line` quote and the
   claimed defect), not a paraphrase.
2. **The validation reasoning for overruling.** Why the orchestrator judged the finding a
   false positive, grounded in a read of the artefact (the evidence, not an assertion).
3. **The exact revert information.** The commit SHA / diff / file-and-line state needed to
   undo the change if the override proves wrong. An override with no recorded revert path is
   prohibited.
4. **Attended or unattended.** Whether the override was made with the maintainer reachable
   (attended / attended-autonomous) or in an overnight / unattended run.

## Status field

- `pending`: override made, not yet reviewed by the maintainer. A standing item the
  maintainer clears; never silently closed.
- `reviewed`: the maintainer has seen the override and confirmed it (or directed the revert,
  in which case the Follow-up cell records the reverting PR).

## Resume and attended-boundary surfacing

An override made in an overnight or otherwise unattended run is surfaced to the maintainer at
the next attended boundary: the end of the unattended run, the return to attended mode, or at
latest the next session resume. On `/resume`, the assistant reads this register alongside the
other standing registers (the pending-decisions queue, the high-assurance register, the
matrix-fit history) and surfaces every `pending` row before starting the queued work, so an
un-reviewed override is not lost across a session boundary. A `pending` override is resolved
to `reviewed` only by the maintainer, exactly as a pending decision is.

This file is maintainer working state, exempt from corpus audit gates.

## Active overrides (pending maintainer review)

None pending. The first-ever verifier override (PR #955, the Canada AI annex FPS
fourth-principle "trusted" false positive) was made and maintainer-reviewed within the
same attended session; it is recorded in the Reviewed table below.

## Reviewed overrides (retained for the audit trail)

| Date | PR | Finding (verbatim, with `path:line`) | Validation reasoning for overruling | Revert information | Attended? | Status | Follow-up |
|---|---|---|---|---|---|---|---|
| 2026-07-15 | #955 | Pre-push verifier, HIGH, DO-NOT-SHIP: "`annex-ai-canada.md:47` ... names the four principles as 'human-centred, collaborative, ready, and responsible'. Multiple canada.ca-scoped searches converge on the fourth principle being 'trusted', not 'responsible' ... precisely the class of error a Canada AI Alliance expert would catch on sight." | False positive. The canada.ca "AI Strategy for the Federal Public Service 2025-2027: Overview" Principles section (provided verbatim by the maintainer, twice) lists the four as Human centred / Collaborative / Ready / Responsible; the fourth principle's own description reads "so that they trust that our use of AI ...", which the verifier's snippet-based web search latched onto and mis-reported, conflating the Overview "Principles" with the separate "Priority areas" page. Canada.ca blocks direct curl and WebFetch (403), so the maintainer's verbatim page is the authoritative source. Maintainer confirmed "Responsible" via AskUserQuestion and re-pasted the Principles section. | Branch `claude/canada-ai-annex-updates`; if wrong, change "responsible" to "trusted" in `ai/jurisdictions/annex-ai-canada.md` line 47 (FPS principles list) and the CHANGELOG-detailed FPS bullet. | Attended | reviewed (maintainer-confirmed 2026-07-15) | None; "Responsible" confirmed correct. The verifier's valid secondary point (the CHANGELOG over-claimed held-source coverage of the not-held FPS section) was fixed in the same PR. |
