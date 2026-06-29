# Skeptical-Verifier Override Register

**Version:** 1.0.0\
**Date:** 2026-06-29\
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

None. No verifier override has been made yet. (The skeptical-verifier standard itself was
codified in PR #461; the first override, if any, will be logged here.)

## Reviewed overrides (retained for the audit trail)

| Date | PR | Finding (verbatim, with `path:line`) | Validation reasoning for overruling | Revert information | Attended? | Status | Follow-up |
|---|---|---|---|---|---|---|---|
| (none yet) | | | | | | | |
