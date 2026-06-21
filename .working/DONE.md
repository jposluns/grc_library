# DONE

Closed-TODO ledger for the GRC Documentation Library. Records work that has shipped, keyed by the original backlog ID (PR number for PR-based items; the TODO `P-X.Y` identifier for backlog items). Reverse-chronological: newest at top.

This file complements [`CHANGELOG.md`](../CHANGELOG.md). Where the CHANGELOG records *what landed in each PR* (file-by-file changes, version bumps, verification), DONE records *which backlog items each PR closed* (cross-referencing the original TODO entries that motivated the work). Adopters reading the corpus do not need DONE; it is maintainer working state and lives under `.working/`.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions. It is exempt from corpus audit gates per the `.working/` directory exemption.

## How items get here

When a PR closes a TODO item, the maintainer (or the AI assistant under the corpus-management discipline) rotates the item from [`TODO.md`](../TODO.md) into this file as part of the PR's diff. The rotation is enforced by convention rather than by a gate, per the discipline section in [`dev-security/claude-rules/governance/change-tracking.md`](../dev-security/claude-rules/governance/change-tracking.md).

The format for each entry:

- `### PR #N — short title (YYYY-MM-DD merge date)` — primary header
- `### TODO P-X.Y — short title (YYYY-MM-DD shipped)` — for items that closed across multiple PRs (the primary entry sits under the PR that closed it; the P-X.Y header is a cross-reference)
- One-paragraph summary of what closed and any context a future reader needs to understand why this item existed.

---

## Closed items

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

---

## Design decisions made (rotated from TODO 2026-06-21 as part of DONE infrastructure)

These were not "closed TODO items" — they are design decisions that the session made during the work above. Captured here so future sessions can find the decision rationale without spelunking through CHANGELOG entries or PR descriptions. The decisions remain in force unless explicitly revisited.

### `.working/` convention (decided 2026-06-21, PRs #114-#118)

Maintainer working state: not corpus content; not for adopter consumption; exempt from corpus audit gates (in `DEFAULT_EXEMPT_DIRS`); frozen-state archive (cross-references accurate as-of write-time; staleness expected). Top-level dot-prefix matches the existing tooling-dir convention (`.git/`, `.github/`, `.claude/`).

### Canonical activity layout under `.working/<activity>/` (decided PR #118)

Each subdirectory contains:

- `README.md` — static convention info (what the activity is, file format spec, taxonomies, protocols, framework alignment, fork guidance)
- `history.md` — reverse-chronological table (new rows on top); columns: Date | Sweep/Run | Subagents | Findings | Resulting PR | Detail | Summary
- `YYYY-MM-DD-<run-id>.md` — per-run detail file, **only created when findings exist**
- `Subagents` column declares dispatch (Rule 5.6) for every row including zero-finding runs

### Slash commands vs skill names are independent identifiers (decided PR #115)

Short ergonomic verbs for slash commands (`/validate`, `/fitness`); descriptive names for skills (`validation-sweep`, `library-fitness-review`). The slash command file wraps the skill invocation.

### Template content vs project-application (decided PR #116)

`governance/` holds template content (specifications, frameworks, registers as document-type templates that adopters cite); `.working/` holds project-specific application of those templates (our log of our sweeps, our verification campaign progress, our branch-protection snapshot).

### Fork-time guidance for `.working/` (decided PR #114)

Adopters cloning the library may delete `.working/` outright or keep it as historical reference. Both fine. Adopters should not extend the upstream `.working/` with their own working state — fresh `.working/` for their own outputs preserves audit trails on both sides.

### PR sequencing principle (durable from earlier sessions, restated PRs #114-#130)

"More PRs, keep each one clean." Favor small focused PRs over bundled ones. Validation sweeps run between substantive PRs.

### CHANGELOG split convention (decided PR #125)

Root [`CHANGELOG.md`](../CHANGELOG.md) keeps the lead paragraph only; structured sections + verification evidence + discipline observations move to [`.working/changelog-details/CHANGELOG-detailed.md`](changelog-details/CHANGELOG-detailed.md). Going forward, every PR writes BOTH. PR-time gate (`check-changelog-on-pr.py`) enforces dual-entry. The general `.working/` audit exemption is preserved for everything else.

### Fitness review convention (decided PR #120)

10 personas parallel (original prompt's 7 + adoption practitioner + privacy/DPO + newcomer); whole-corpus each run; output to [`.working/fitness-reviews/YYYY-MM-DD-rN.md`](fitness-reviews/) only when findings; 8-section combined file. Severity: SARIF-lite + `[critical]` flag in High. Manual trigger only; no mechanical gate enforces it.

### Subagent dispatch (Rule 5.6) audit trail (decided PR #111)

Every validation-sweep iteration declares which subagents were dispatched in the `Subagents` column of [`history.md`](validate-sweeps/history.md). Cannot reconstruct silent skips later.

### Convergence-delta termination (decided PR #115; validation-sweep)

Empty-delta primary stop; patience-plateau secondary (2 consecutive iterations no shrinkage); hard-ceiling 6 iterations.

### Per-iteration detail files: comma form for H2 headings (decided PR #118)

Gate-2 enforces no em-dashes; comma is the canonical form across SKILL.md, slash command, and [`.working/validate-sweeps/README.md`](validate-sweeps/README.md).

### Session-state snapshot as-of-last-refresh (decided PR #127, mechanically enforced via gate 45 in PR #128)

The "Session state at pause" subsection in [`TODO.md`](../TODO.md) is intentionally frozen at session-pause time. The version snapshot, PRs-completed list, and sweep-cursor each drift forward as the project advances — that drift is expected and not a defect. Gate 45 (TODO staleness audit) catches the harder shapes (queued PR already merged; sweep cursor behind history) mechanically; other drift is informational.

### Two-file CHANGELOG dual-entry enforcement (decided PR #125)

The PR-time delta gate `check-changelog-on-pr.py` requires BOTH the root CHANGELOG and the detailed mirror to be in the diff (lock-step). Modifying one without the other fails the gate. The opt-out `Changelog: <reason>` trailer in any commit message satisfies the gate regardless of split.

### Wrapper-script-plus-corpus-runner discipline (decided PR #128)

Local PR-time discipline requires running BOTH [`tools/run_all_audits.sh`](../tools/run_all_audits.sh) (corpus gates) AND [`tools/run-pr-time-checks.sh`](../tools/run-pr-time-checks.sh) (PR-only delta gates D1 + D2 + gate 45) before push. The two runners together cover every gate the CI workflow runs. Structural fix for the PR-time-delta-gate omission failure mode that surfaced in PR #127's first push.

### Decorative gate-count narrations are forbidden in prose (decided PR #130)

Phrases like `"the N-gate audit programme"`, `"all N gates"`, `"gates 1-N"` are removed from corpus prose. The spec §6 inventory in [`governance/specification-audit-programme.md`](../governance/specification-audit-programme.md) is the canonical single source for both the gate list and the current count; downstream prose points to §6 instead of repeating the count. Gate 39 (cross-file gate-count consistency audit) retained as the defence against new decorations creeping back in.
