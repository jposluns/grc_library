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
scope row; pack `1.54.6`). The item numbering below preserves the original staging order;
item 4's remaining project-CLAUDE.md clause and item 5's sub-item 5(b) plus the `/claim-fit`
candidate, all `.claude/CLAUDE.md` touches, are grouped as the #657 bundle._

### 4. [TODO 3.15 D-F3] Evidence-grounded-completion one-liner corollaries: project-CLAUDE.md remnant

- **Landed (#656):** the three PACK surfaces (pack `dev-security/claude-rules/CLAUDE.md`
  rule-index one-liner, pack README tree blurb, pack README scope row) each gained a condensed
  clause naming the rule's un-observable-state / inventory / external-version-currency corollaries.
- **Remaining (rides #657 with item 5):** the project `.claude/CLAUDE.md` index bullet's matching
  clause, grouped into the item-5 `.claude/CLAUDE.md` bundle so all project-CLAUDE.md touches land together.

### 5. [TODO 3.15 r5] Two CLAUDE.md items

- **Target:** `.claude/CLAUDE.md`.
- **(a) DONE, landed in #652 (2026-07-05):** the maintainer chose "reword the fallback"; the
  attended-autonomous rule-3 fallback now drops the "idle on a longer check-in" option and
  cross-references the no-long-interval-check-ins clause, so the self-contradiction is resolved.
- **(b) LOW:** the close-out checklist's reconcile bullet does not name D7 as the now-mechanized
  version-token half (the gate-50 naming pattern); one clause.
- Also rides this bundle: the already-staged `/claim-fit` cadence-section candidate (#630
  out-of-window observation).

### 6. [TODO 4.7 GR-P1..P5] Pack design improvements (design-tier)

- **Targets:** the `dev-security/claude-rules/` pack (rules, skills, README, overlay pointers).
- **Prep status:** design-tier, larger; draft the shape proposals during the overnight run if
  time permits after the corpus/tooling/P2 work, else leave prep notes. GR-P1 session-lifecycle
  pack rule; GR-P2 rule operative-core condense; GR-P3 third-occurrence-to-gate escalation;
  GR-P4 overlay primary-wins pointers + pruning stance; GR-P5 `derives_from` re-point + exception-
  register hoist + the CLAUDE.md Boundaries-line wrong-trio correction. These are their own PRs.

---

_Empty of items = nothing deferred. Add an item whenever an overnight task turns out to need a
protected-file edit; draft its content here rather than deferring it as a bare pointer._
