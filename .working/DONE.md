# DONE

Closed-TODO ledger for the GRC Documentation Library. Records work that has shipped, keyed by the original backlog ID (PR number for PR-based items; the TODO `P-X.Y` identifier for backlog items). Reverse-chronological: newest at top.

This file complements two other working-state ledgers:

- [`CHANGELOG.md`](../CHANGELOG.md): records *what landed in each PR* (file-by-file changes, version bumps, verification). Organized by PR.
- [`design-decisions.md`](design-decisions.md): records *design decisions made* (working-state and convention decisions; decisions explicitly dropped). Organized thematically.

DONE records *which backlog items each PR closed* (cross-referencing the original TODO entries that motivated the work). Organized reverse-chronologically by closing PR. Adopters reading the corpus do not need any of these three files; they are maintainer working state and live under `.working/`.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions. It is exempt from corpus audit gates per the `.working/` directory exemption.

## How items get here

When a PR closes a TODO item, the maintainer (or the AI assistant under the corpus-management discipline) rotates the item from [`TODO.md`](../TODO.md) into this file as part of the PR's diff. The rotation is enforced by convention rather than by a gate, per the discipline section in [`dev-security/claude-rules/governance/change-tracking.md`](../dev-security/claude-rules/governance/change-tracking.md).

The format for each entry:

- `### PR #N — short title (YYYY-MM-DD merge date)` — primary header
- `### TODO P-X.Y — short title (YYYY-MM-DD shipped)` — for items that closed across multiple PRs (the primary entry sits under the PR that closed it; the P-X.Y header is a cross-reference)
- One-paragraph summary of what closed and any context a future reader needs to understand why this item existed.

---

## Closed items

### PR #138 — Shipped Priority 4 items rotation (2026-06-21)

Maintainer-surfaced (during PR #131): TODO's Priority 4 items 4.1 through 4.5 were "Shipped 2026-06-20 as ..." entries — completed work, not forward-looking backlog. Rotated to DONE as five separate `### TODO P4.x` entries (preserved here cross-referenced to the original "shipped" framing); P4.6 (corpus-management discipline as a shareable skill) remains forward-looking in TODO. Also removes the Sweep 4 follow-up historical note from "Open follow-ups from validation sweeps" (already resolved and noted as no-longer-tracked). Library `2026.06.119 → 2026.06.120`. Closes the TODO content cleanup queued since PR #135.

### TODO P4.1 — Quickstart templates per adopter profile (shipped 2026-06-20)

Shipped as [`docs/template-quickstart.md`](../docs/template-quickstart.md) (v2.0.0). Core baseline plus five stacking dimensions (Activity, Data scope, Audience, Regulatory exposure, GRC capacity) with about twenty modules; three worked examples. The original v1.0.0 fixed-profile structure (PR #103) was rejected by the maintainer as too rigid; the rewrite (PR #105) adopts an activity-modular composition shape that lets adopters combine modules à la carte.

### TODO P4.2 — Maturity assessment interactive template (shipped 2026-06-20)

Shipped as [`docs/template-maturity-self-assessment.md`](../docs/template-maturity-self-assessment.md). Guided markdown checklist covering 11 library domains across a 5-tier maturity ladder (Initial / Developing / Defined / Managed / Optimising); per-tier next-step guidance; recording template.

### TODO P4.3 — Implementation roadmap templates (shipped 2026-06-20)

Shipped as [`docs/template-implementation-roadmap.md`](../docs/template-implementation-roadmap.md). Three-phase (Floor / Operational / Year-1 close) sequence at 90 / 180 / 365 days for the reference E2 pace, with pace adjustments for E1, E3, E4 capacity tiers and for composition complexity. Designed to sequence the modules picked via the quickstart template; not per-profile.

### TODO P4.4 — Regulator interaction templates (shipped 2026-06-20)

Shipped as [`compliance/template-regulator-interaction.md`](../compliance/template-regulator-interaction.md). Five sub-templates in one consolidated document: breach notification, attestation submission, examination support, periodic report submission, regulatory inquiry response. Shape-only; jurisdiction- and sector-specific timing/format requirements live in the relevant annex or sector folder.

### TODO P4.5 — Audit evidence package templates (shipped 2026-06-20)

Shipped as [`compliance/template-audit-evidence-package.md`](../compliance/template-audit-evidence-package.md). Cover page, control inventory index, per-control sections (framework references, implementation and operating evidence, gaps and compensating controls, per-control sign-off), optional per-domain summaries for 50+ control packages, optional cross-reference index for shared evidence, package-level sign-off. Anti-patterns to watch and eight review questions.

### PR #137 — Overnight-work protocol: stub format for `overnight-pr.md` + audit gate 46 + pack rule amendment (2026-06-21)

Implements the maintainer-confirmed overnight-work protocol. New stub-form [`.working/overnight-pr.md`](overnight-pr.md) with `**Status:**` field; new gate 46 ([`tools/lint-overnight-file.py`](../tools/lint-overnight-file.py)) scanning the file and failing on `Status: done`; new "Overnight-work protocol" subsection in [`change-tracking.md`](../dev-security/claude-rules/governance/change-tracking.md) documenting the lifecycle. Three-state Status field (`stub` / `in-flight` / `done`) rather than binary so overnight PRs land cleanly while the gate still applies mechanical pressure for morning processing once a session ends. Pack `1.32.0 → 1.33.0`; spec `1.13.1 → 1.14.0`; library `2026.06.118 → 2026.06.119`. The maintainer-confirmed standard (chat message 2026-06-21 mid-PR-#135) is the closing trigger for this PR.

### PR #135 — Restructure design-decisions into its own file; clean up `overnight-pr.md` (2026-06-21)

Creates [`design-decisions.md`](design-decisions.md) as the new home for design-decision content; rotates the "Design decisions made" section out of DONE; migrates fitness-skill-specific decisions out of `overnight-pr.md`; migrates TODO's "Decisions log" section in as "Decisions explicitly dropped"; deletes [`overnight-pr.md`](overnight-pr.md) (purely procedural detail with no forward-looking value after the overnight session it documented). [`README.md`](README.md) (`.working/`) Top-level files table extended with the new file. Implements the maintainer's "DONE should be for things that are DONE; we have the .working directory for our work, let's be as organized as we can moving forward" directive. The TODO's "Decisions log" subsection was specifically called out as misplaced and migrated.

### PR #134 — Gate 45 false-positive fix: tighten queued-PR regex (2026-06-21)

Post-PR-#133 merge `push`-event CI run on `main` failed because gate 45's regex was too permissive: an `[^\n]{0,80}` window between "next/queued/pending" markers and `PR #<digit>` matched a historical parenthetical reference (`...during PR #133`) instead of the intended queued-PR target (which was a placeholder `PR #N`). Regex tightened to `[\s,:—–-]*` so the queued PR must be the immediately-following PR ref structurally, not any PR ref within 80 chars. Real-drift cases (`Next, PR #128`, `queued PR #128`, etc.) continue to match. Library `2026.06.116 → 2026.06.117`. This is gate 45's second production catch and the second post-merge-`main` failure since gate 45 shipped (PR #128); the first was a genuine drift, this was a false positive.

### PR #133 — Document the project's Canadian-first language convention (2026-06-21)

Maintainer-surfaced during PR #131's chat thread: the project's `-ized`/`-ization` orthography is Canadian (which shares the Oxford convention with American English), not American-attributed. The convention is named explicitly as **Canadian English first, Commonwealth second, other dialects last**. Doc-only PR: [`tools/lint-language.py`](../tools/lint-language.py) module docstring rewritten to name the convention as Canadian (linter behaviour unchanged); new "Language convention" section in [`.claude/CLAUDE.md`](../.claude/CLAUDE.md) Conventions section; [`CONTRIBUTING.md`](../CONTRIBUTING.md) Style requirements section rewritten to lead with the convention statement instead of just the linter rule. CONTRIBUTING per-doc `1.1.0 → 1.2.0`; library `2026.06.115 → 2026.06.116`.

### PR #132 — Add Ryk Edelstein to `AUTHORS.md` (2026-06-21)

Single-line addition to the Acknowledged contributors list in [`AUTHORS.md`](../AUTHORS.md) for [Ryk Edelstein](https://github.com/fedelst). Per-doc version `1.1.0 → 1.1.1`; library `2026.06.114 → 2026.06.115`. Closes the maintainer-surfaced TODO item from PR #131 ("In the next PR, add ..."). First PR using the post-PR-#131 steady-state discipline of TODO/DONE rotation in the same PR.

### PR #131 — DONE.md infrastructure + TODO refactored to forward-looking only (2026-06-21)

Bootstrap entry (added retroactively in PR #132 — PR #131 created this file but did not add its own entry; recorded here per the discipline that every PR henceforth adds its own DONE entry). PR #131 introduced [`.working/DONE.md`](DONE.md) as the closed-TODO ledger; rotated all "PRs completed this session" (PRs #110-#130) and "Key design decisions made this session" content out of [`TODO.md`](../TODO.md) into DONE; added a new "PR finalization protocol" section to the [`change-tracking.md`](../dev-security/claude-rules/governance/change-tracking.md) pack rule documenting three disciplines (TODO is forward-looking; DONE keyed by backlog ID; after-merge list-next-N PRs); operationalised both in [`.claude/CLAUDE.md`](../.claude/CLAUDE.md). Pack `1.31.0 → 1.32.0`; library `2026.06.113 → 2026.06.114`.

### PR #130 — Remove decorative gate-count narrations (2026-06-21)

Replaced 11 prose `"the N-gate audit programme"` references across 7 files with `"the audit programme"`; the spec §6 inventory remains the canonical source for both the gate list and the current count. Implements the maintainer's just-surfaced proposal that decorative counts add no information beyond what readers can derive from §6 and cost real PR friction on every gate-add. PR #128 cascaded ten such references; PR #129 cascaded one more. Gate 39 (cross-file gate-count consistency audit) retained as the defence against new decorations creeping back in. Library `2026.06.112 → 2026.06.113`. Was queued as proposal "(b)" in TODO's Queued sequence follow-up paragraph after PR #129; closed in this PR.

### PR #129 — PR #128 catch-up: TODO drift caught by gate 45 on post-merge `main` (2026-06-21)

The post-merge `push`-event CI run on `main` (commit `1ee9dda`) failed because [`TODO.md`](../TODO.md) line 47 still framed PR #128 as "Next" while PR #128 had merged. Gate 45 (TODO staleness audit, the gate PR #128 itself introduced) correctly flagged the line. This was gate 45's first production catch and is precisely the failure mode it was built to detect. The fix is mechanical TODO rotation: PR #128 moved from Queued sequence into PRs-completed list; queued sequence rebased; two design proposals from the maintainer captured as follow-ups. Library `2026.06.111 → 2026.06.112`.

### PR #128 — Gate 45 (TODO staleness audit) + PR-time-checks wrapper (2026-06-21)

New audit gate 45 ([`tools/lint-todo-staleness.py`](../tools/lint-todo-staleness.py)) catches the two TODO drift shapes that recurred across four consecutive validation sweeps (queued PR already merged; sweep cursor behind history). Bundled with [`tools/run-pr-time-checks.sh`](../tools/run-pr-time-checks.sh), a local wrapper that runs the two PR-only delta gates (D1 CHANGELOG-on-PR, D2 per-PR version-bump) plus gate 45, so every gate the CI workflow runs has a local invocation path before push. Spec `1.12.1 → 1.13.0`; library `2026.06.110 → 2026.06.111`. Added TODO P4.6 (corpus-management discipline as a shareable skill).

### PR #127 — Sweep 11 iter 1 close-out (2026-06-21)

Eight in-window findings actioned: corrected the fitness report's count mismatch across six surfaces (`95/18/22/31/24 → 111/17/20/57/17`); updated [`governance/specification-audit-programme.md`](../governance/specification-audit-programme.md) D1 description for dual-entry post-PR-#125; refreshed TODO and reframed its session-pause snapshot as "as-of-last-refresh" (one-time convention amendment to address the four-consecutive-sweep recurring drift); softened workflow ordering in [`change-tracking.md`](../dev-security/claude-rules/governance/change-tracking.md); renamed [`.working/README.md`](README.md) "Created by" column to "Origin". Library `2026.06.109 → 2026.06.110`.

### PR #126 — `.working/README.md` Activities table row for `changelog-details/` (2026-06-21)

Single-row addition to [`.working/README.md`](README.md) Activities table for the `changelog-details/` activity (the activity directory itself was introduced in PR #125 but the README row was missed). Library `2026.06.109 → 2026.06.109` (no library bump, README-only edit).

### PR #125 — CHANGELOG two-file split: root keeps lead paragraphs, detailed mirror keeps full structured entries (2026-06-21)

Splits the CHANGELOG into a two-file convention: root [`CHANGELOG.md`](../CHANGELOG.md) carries lead-paragraph summaries (adopter-facing); detailed mirror at [`.working/changelog-details/CHANGELOG-detailed.md`](changelog-details/CHANGELOG-detailed.md) carries full structured-section entries (maintainer-grade). 2926 → 675 lines in root. Delta gate (`check-changelog-on-pr.py`) extended to require lock-step modification. Pack `1.30.0 → 1.31.0`. Library `2026.06.108 → 2026.06.109`.

### PR #124 — First-ever fitness review (run r1, ten persona subagents) (2026-06-21)

First invocation of the `library-fitness-review` skill (`/fitness`) shipped in PR #120. Ten persona subagents dispatched in parallel. **111 unique findings** (17 H[critical], 20 H, 57 M, 17 L; counts originally reported as "95/18/22/31/24" approximation, corrected in PR #127). Findings are FR-1 through FR-111 in [`.working/fitness-reviews/2026-06-21-r1.md`](fitness-reviews/2026-06-21-r1.md). Library `2026.06.107 → 2026.06.108`.

### PR #123 — Sweep 10 iter 3 close-out (2026-06-21)

One in-window Medium finding actioned: TODO version-snapshot drift fix. Convergence-delta narrowing from iter 2's 7 findings to iter 3's 1 (strong narrowing but not yet empty). Library `2026.06.106 → 2026.06.107`.

### PR #122 — TODO cleanup: removed completed Steps A/C/D/E from queued sequence (2026-06-21)

Removed completed steps from the queued sequence section; renumbered next step. Pure TODO maintenance; no library content change. `Changelog: skip` per TODO's informational status (pre-dating the PR #125 dual-entry convention).

### PR #121 — Sweep 10 iter 2 close-out: post-overnight-sequence cleanup (2026-06-21)

Seven in-window findings actioned post the three-PR overnight sequence (PRs #118-#120): re-added preflight exemption for "Six rules" line (new `line_hash` post-PR-#117 content change); refreshed TODO resume-state snapshot; fixed small CHANGELOG narration claim ("(new, version 1.0.0)" → "(new)"); updated [`.working/overnight-pr.md`](overnight-pr.md) status to merged. Library `2026.06.105 → 2026.06.106`.

### PR #120 — `/fitness` skill (`library-fitness-review`) (2026-06-21)

Adds a new skill to the `dev-security/claude-rules/` pack invoked via the `/fitness` slash command. Whole-corpus library-quality review dispatching ten persona reviewers in parallel (executive, security practitioner, GRC practitioner, auditor, policy editor, process owner, skeptical reader, adoption practitioner, privacy officer, newcomer). Canonical `.working/fitness-reviews/` activity layout. Pack `1.29.0 → 1.30.0`. Authored end-to-end during an overnight session under explicit maintainer authorisation; full decision log at [`.working/overnight-pr.md`](overnight-pr.md). Library `2026.06.104 → 2026.06.105`.

### PR #119 — TODO update only (session-resume context capture) (2026-06-21)

Session-resume context capture in TODO; `Changelog: skip` per TODO's informational status (pre-dating the PR #125 dual-entry convention). No library content change.

### PR #118 — Restructure `.working/<activity>/` to canonical layout (2026-06-21)

Restructured [`.working/validate-sweeps/`](validate-sweeps/) to the canonical `<activity>/{README, history, detail-files}` layout that becomes the standard for any `.working/<activity>/` subdirectory going forward. The validation-sweep history file moved into the subdirectory; verbose static content moved to the subdirectory's README; the history file became a slim reverse-chronological table; per-iteration detail files are created only when findings exist. Library `2026.06.103 → 2026.06.104`.

### PR #117 — Sweep 10 iter 1 close-out: six prose-drift findings post-PRs-#114-#116 (2026-06-21)

Six in-window prose-drift findings actioned, all introduced or made visible by the three-PR `.working/` sequence (PRs #114-#116). Stale step counts in SKILL.md and slash command; stale subdir inventory in `.working/README.md`; three-way section-header drift; awkward possessive; stale "Four rules" → "Six rules". Library `2026.06.102 → 2026.06.103`.

### PR #116 — Move validation-sweep history file from `governance/` to `.working/` (2026-06-21)

Validation-sweep history is project-specific application of the validation-sweep discipline, not template content for adopters. Application belongs in `.working/`; template content (the failure-mode class taxonomy, the maintenance protocol, the false-positive accept-list rules, the dispatch-declaration discipline) lives in the [`validation-sweep` SKILL.md](../dev-security/claude-rules/skills/validation-sweep/SKILL.md). Library `2026.06.101 → 2026.06.102`.

### PR #115 — `/validate` slash command rename + per-iteration record convention (2026-06-21)

Slash command rename from `/validation-sweep` to `/validate` per the maintainer's "short ergonomic verbs for slash commands" preference. Skill name remains `validation-sweep`. Added per-iteration record convention to the validation-sweep skill (detail files only when findings; history table row for every iteration including zero-finding ones). Library `2026.06.100 → 2026.06.101`.

### PR #114 — `.working/` top-level convention infrastructure (2026-06-21)

Established the `.working/` top-level convention for maintainer working state. First of a four-PR sequence (`.working/` infrastructure, `/validate` rename + per-run records, `/fitness` skill, changelog-details migration). Created [`.working/README.md`](README.md); added `.working/` to `DEFAULT_EXEMPT_DIRS` in [`tools/lint_common.py`](../tools/lint_common.py). Library `2026.06.99 → 2026.06.100`.

### PR #113 — Sweep 9 iter 3 close-out: three documentation findings from Subagent A's deep-review of PR #112 (2026-06-21)

Three documentation findings actioned from Subagent A's deep review of PR #112. Convergence-delta narrowing from iter 2 to iter 3. Library `2026.06.98 → 2026.06.99`.

### PR #112 — 7th governance rule (`validate-inference-before-action.md`) + gate 39 pattern P7 (2026-06-21)

New seventh pack rule [`dev-security/claude-rules/governance/validate-inference-before-action.md`](../dev-security/claude-rules/governance/validate-inference-before-action.md): action-side counterpart of the evidence-grounded-completion rule. When the next action depends on an inferred premise, validate the premise via tool call before taking the action. Gate 39 pattern P7 ("N \<word\> gates") added. Pack `1.27.0`; library `2026.06.97 → 2026.06.98`.

### PR #111 — Sweep 9 closure: Subagent C findings + Rule 5.6 (subagent-dispatch declaration discipline) (2026-06-21)

Sweep 9 closure: actioned Subagent C findings; added Rule 5.6 to the validation-sweep SKILL.md (subagent dispatch declaration: every iteration must declare which subagents were dispatched in the history register's `Subagents` column). Library `2026.06.96 → 2026.06.97`.

### PR #110 — Corpus stale gate-count fixes + gate 39 pattern P6 (2026-06-21)

Corpus-wide stale gate-count reference fixes (the cascade-class issue that PR #130 ultimately addressed at the source by removing decorative gate-count narrations). Added gate 39 pattern P6 ("N gates" without preceding qualifier). Library `2026.06.95 → 2026.06.96`.
