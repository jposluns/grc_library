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
drop the longer-check-in option). The item numbering below preserves the original staging
order; item 5's remaining sub-items 5(b) and the `/claim-fit` candidate are unstarted._

### 2. [TODO 3.18] Pack-tree ATLAS technique-ID currency refresh

- **Targets:** `dev-security/claude-rules/ai/{agent-security.md, ai-security.md,
  rag-security.md, mcp-security.md}` (8 `AML.T0048` citations + gloss drifts on T0024, T0051).
- **Prep status:** DRAFT DURING OVERNIGHT RUN, re-map every pack-tree ATLAS ID and gloss
  against the held CSVs at `grc_library_scratch/ref/frameworks/MITRE/ATLAS-2026.06--*.csv`
  (do NOT map from memory). Record the verified old→new map here before daytime.
- **QA:** pack Version + `## Version history` co-bump (D6); byte-identical local mirrors where
  files are mirrored; `lint-language.py`.

### 3. [TODO 3.15 D-F2] Guardrail-review SKILL cadence clause

- **Target:** `dev-security/claude-rules/skills/guardrail-review/SKILL.md` (the auto-prompt
  description bullet; mirror per gate 44 if step text changes).
- **Draft intent:** one clause noting the SKILL's deferral is bounded by gate 60 (warn below
  drift 3, fail at 3), and naming gate 60 in the mechanical-gates bullet (currently unnamed).
  Draft the exact wording during the overnight run against the current SKILL text.

### 4. [TODO 3.15 D-F3] Evidence-grounded-completion one-liner corollaries

- **Targets:** pack `dev-security/claude-rules/CLAUDE.md`, pack README tree blurb + scope row,
  project `.claude/CLAUDE.md` index bullet (the r3 D-3 fix shape, one clause per surface).
- **Draft intent:** add the rule's un-observable-state / inventory / external-version-currency
  corollaries to each of the four enumeration surfaces. Draft exact per-surface clauses during
  the overnight run.

### 5. [TODO 3.15 r5] Two CLAUDE.md items

- **Target:** `.claude/CLAUDE.md`.
- **(a) MEDIUM, live self-contradiction:** the attended-autonomous rule-3 fallback says "wrap
  a clean handoff or idle on a longer check-in rather than guessing" while the 2026-07-04
  no-long-interval-check-ins clause forbids deferred check-ins "of any shape" in the same file.
  Reword the fallback, or carve out the everything-blocked-on-one-decision wait explicitly
  (maintainer's call, surface the two options at daytime).
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
