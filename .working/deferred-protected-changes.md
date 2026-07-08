# Deferred protected-file changes (overnight → daytime apply queue)

**Purpose / persistent reminder (maintainer-directed 2026-07-05).** In OVERNIGHT mode,
protected-file edits are DEFERRED: they need the maintainer's authorization (a click/tap the
maintainer cannot give while away), per the A1 answer at the 2026-07-05 resume ("in overnight
mode I won't be there to authorize claude.md changes; do not pause asking me for
authorization, anything that requires me to click/tap must be deferred to day time runs").
Protected surfaces are `.claude/` (including `.claude/CLAUDE.md`, commands, hooks, settings)
and the `dev-security/claude-rules/` governance pack. This file is the persistent staging
area for those deferred changes; it lives in `.working/` (not protected), so it can be
written during the overnight run and survives across sessions on `main`.

**Mode-transition protocol (overnight → daytime).** When the maintainer switches the session
from overnight to daytime / attended mode:

1. **Finish the then-current PR** (do not abandon it mid-flight).
2. **Then clear this backlog**: apply every prepared protected-file change below, each as its
   own PR or a coherently-grouped one, with `tools/lint-language.py` run on the new/edited
   pack prose BEFORE the first commit, and full per-PR `/validate-pr` + `/retro`.
3. **Rotate each item out** of this file as it lands (record in CHANGELOG + DONE as usual);
   when the file is empty it holds only this header.

The items below are **drafted in advance during the overnight run** so the daytime apply is
quick: the content is ready and only the authorized apply + QA remains.

---

## Prepared items (apply at daytime, in this order)

_Landed in PR #652 (2026-07-05): item 1 (codify the mode-transition protocol in CLAUDE.md,
now the `Overnight-to-daytime protected-backlog clearance` paragraph in the
`## Attended-autonomous operating mode` section) and item 5(a) (reword the rule-3 fallback to
drop the longer-check-in option). Landed in PR #654 (2026-07-05): item 2 (the pack-tree ATLAS
technique-ID currency refresh, TODO 3.18 closed: eight `AML.T0048` re-pointed to `AML.T0053`
and two gloss drifts corrected against the held ATLAS 2026.06 CSVs). Landed in PR #655
(2026-07-05): item 3 (the guardrail-review SKILL cadence clause, TODO 3.15 D-F2 closed: the
auto-prompt bullet now names gate 60 and states the deferral is bounded, warn at drift 1 to 2,
fail at 3). Landed in PR #656 (2026-07-05): item 4's PACK surfaces (the D-F3 corollary clauses
on the pack CLAUDE.md rule-index one-liner, the pack README tree blurb, and the pack README
scope row; pack `1.54.6`). Landed in PR #657 (2026-07-05): item 4's remaining
project-CLAUDE.md clause, so TODO 3.15 D-F3 is now FULLY closed and item 4 is rotated out.
Item 5's remaining r5 close-out-checklist clauses re-scope from the former #657 bundle to a
focused #658 (maintainer-directed 2026-07-05: after #657, small Priority 3 and Priority 1
items first to clear TODO count; the larger GR-P design track, item 6, defers). Landed in PR #674 (2026-07-06): item 5's remaining `/claim-fit` cadence-section clause, applied as a new `## Normative-attribution claim-precision cadence (/claim-fit)` section in `.claude/CLAUDE.md` sibling to `/matrix-fit`, so item 5 is fully rotated out; only item 6 (the GR-P design track) remains._

### 6. [TODO 4.7 GR-P1..P5] Pack design improvements (design-tier)

- **Targets:** the `dev-security/claude-rules/` pack (rules, skills, README, overlay pointers).
- **Prep status:** design-tier, larger; draft the shape proposals during the overnight run if
  time permits after the corpus/tooling/P2 work, else leave prep notes. GR-P1 session-lifecycle
  pack rule; GR-P2 rule operative-core condense; GR-P3 third-occurrence-to-gate escalation;
  GR-P4 overlay primary-wins pointers + pruning stance; GR-P5 `derives_from` re-point + exception-
  register hoist + the CLAUDE.md Boundaries-line wrong-trio correction. These are their own PRs.

### 7. [changelog-restructure] Current-week model + compact root format (descriptive doc edits)

- **Targets:** the change-tracking governance rule (`dev-security/claude-rules/governance/change-tracking.md` and its `.claude/rules/governance/change-tracking.md` mirror), the `change-tracking-write-entry` skill (pack + `.claude/` copies), and `.claude/CLAUDE.md`.
- **Why deferred:** protected surfaces; the non-protected machinery (gate-59 dynamic cutoff, `tools/sweep-working-records-to-scratch.py`, `.gitattributes`, `.working/changelog-details/README.md`) shipped in the overnight PR 1, but the prose that DESCRIBES the model and wires the per-PR step into the workflow lives in protected files.
- **Prepared edits (apply at daytime):**
  1. **change-tracking rule (both copies):** add the current-week model, the in-repo detailed mirror holds only the current week; completed weeks are swept to the `grc_library_scratch` weekly Monday-dated archives via `tools/sweep-working-records-to-scratch.py` (data-safe: emit-then-verify-then-prune); gate 59's cutoff is a dynamic floor `max(CUTOFF_PR, oldest in-repo mirror PR)`. State that removed content remains in git history, so the sweep is tree-tidiness, not clone-cleanliness. Document the compact root-entry format: `**YYYY-MM-DD | X.Y.Z | PR #N** - one-or-two-sentence summary`, blank line between entries, plain hyphen separator (no em/en dash).
  2. **change-tracking-write-entry skill (both copies):** the write path is UNCHANGED (new detailed entries still prepend to `.working/changelog-details/CHANGELOG-detailed.md`; only completed weeks are swept out later); add the compact root-entry format instruction for the root `CHANGELOG.md` lead line.
  3. **CLAUDE.md:** add the per-PR sweep step to the PR-workflow close-out (run `tools/sweep-working-records-to-scratch.py --emit-archive <scratch>/archive` then `--prune --verify-archived <scratch>/archive` as a cross-repo follow-up, like `/validate-pr`); describe the current-week model + the `.gitattributes export-ignore` fork-hygiene (3.19 resolution) + the compact root format; note the detailed-mirror path description is now "current week only".
- **Cross-refs:** the machinery landed in changelog-restructure PR 1; the initial sweep in PR 2; the root reformat/compress in PR 3+. TODO 3.19 is resolved (export-ignore adopted; current-week model instead of a full `.working` migration).

---

_Empty of items = nothing deferred. Add an item whenever an overnight task turns out to need a
protected-file edit; draft its content here rather than deferring it as a bare pointer._
