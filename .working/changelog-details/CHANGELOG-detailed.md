# Changelog (Detailed Mirror)

All notable changes to this repository are recorded in this file with full structured-section detail. The adopter-facing root [`CHANGELOG.md`](../../CHANGELOG.md) carries only the lead-paragraph summary of each entry; this file is the maintainer-grade audit trail.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](../../specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](../../specification-master-project.md) section 4.5.

The dual-entry convention was introduced in PR #125 (2026-06-21). Historical entries before that date follow the original single-file convention (the root entry was complete; this mirror preserves that pre-split state verbatim from the moment of the split).

## 2026-06-21, Library Version 2026.06.109, PR #125

Splits the CHANGELOG into a two-file convention: root file carries lead-paragraph summaries (adopter-facing); detailed mirror at [`.working/changelog-details/CHANGELOG-detailed.md`](CHANGELOG-detailed.md) carries full structured-section entries (maintainer-grade). Historical content preserved verbatim; root file trimmed to first paragraphs (2926 lines → 675 lines). Delta gate extended to require both files move in lock-step. First PR using the dual-entry convention; this entry dogfoods it.

### Added

- [`.working/changelog-details/README.md`](README.md): static convention info for the new activity directory. Documents file structure, per-entry content split (root keeps lead paragraph; detailed keeps full structured sections), what goes where for new PRs, audit-gate exemption, adopter guidance, relationship to the change-tracking governance rule.
- [`.working/changelog-details/CHANGELOG-detailed.md`](CHANGELOG-detailed.md) (this file): full historical CHANGELOG content (112 entries) preserved verbatim from pre-trim root file; appended at top for new entries going forward.

### Changed

- [`CHANGELOG.md`](../../CHANGELOG.md): trimmed each of 112 existing entries to first-paragraph summaries only. Top-of-file note added explaining that detailed maintainer-level entries may be kept in a working directory (per maintainer's directive, no explicit name or link to the directory). 2926 lines → 675 lines (-77%).
- [`tools/check-changelog-on-pr.py`](../../tools/check-changelog-on-pr.py): extended to require BOTH `CHANGELOG.md` AND `.working/changelog-details/CHANGELOG-detailed.md` to be in the diff when either is modified. Three new failure-mode messages distinguish: (a) neither modified, (b) root modified but detailed missing, (c) detailed modified but root missing. The opt-out `Changelog: <reason>` trailer still applies and satisfies the gate regardless of split.
- [`dev-security/claude-rules/governance/change-tracking.md`](../../dev-security/claude-rules/governance/change-tracking.md): amended "What a CHANGELOG entry must contain" section to recognize the two-file split convention. Added new section "Where CHANGELOG entries live, the two-file split" before the content requirements. Delta gate section updated to specify the dual-entry requirement. Items 1-2 (date-version header, title) live in root; items 3-7 (structured sections, file references, verification, phase context) live in detailed file when split is in use. Added new subsection "Two-file split workflow" under Tool-specific guidance documenting the PR-author workflow (write detailed first, then root lead-paragraph mirror; both in same commit), plus three fork-time shapes (single-file / two-file relocated / no-detailed-mirror) so adopter forks can choose what fits.
- `.claude/rules/governance/change-tracking.md`: mirrored from the pack source per the claude-rules sync convention. Gate 37 (claude-rules sync) enforces parity.
- [`dev-security/claude-rules/README.md`](../../dev-security/claude-rules/README.md): pack version `1.30.0 → 1.31.0`; version-history row added.
- [`README.md`](../../README.md): library version `2026.06.108 → 2026.06.109`; README version `1.8.64 → 1.8.65`.

### Why the split

The root CHANGELOG is the artefact adopters and downstream consumers read; verbose maintainer-grade detail (file-by-file diffs, gate-verification listings, discipline observations, design rationale paragraphs) clutters that surface. Per maintainer feedback during the session that produced PR #119-#124: adopters want lead-paragraph summaries; maintainers want the full audit trail; both can be served without forcing one to read the other's content.

The split is enforced PR-side (the delta gate) rather than audit-time (general 44-gate run) because the requirement is "did this PR write to both?" which is inherently a diff-time question. The `.working/` directory remains exempt from general audit gates per its existing exemption.

### Verification

All 44 audit gates pass standalone post-commit. The new dual-entry requirement is enforced PR-side only (the delta gate runs on `pull_request` events per `.github/workflows/quality.yml`). This PR itself dogfoods the convention: root has the lead paragraph; this file has the full entry.

The trim script applied to historical CHANGELOG entries used a deterministic algorithm (keep H2 header + first paragraph after blank line + entry separator; drop everything between). Spot-checked 5+ entries post-trim to confirm lead-paragraph integrity preserved.

### Discipline observation

This PR closes the "verbose CHANGELOG entries are friction for downstream readers" feedback that has been implicit in maintainer comments since the multi-PR sequence began (PRs #115-#124 each carried 30-80 lines of structured content). Going forward, every PR's lead paragraph is the public-facing summary; the structured sections live in the mirror. The discipline cost is one extra file modification per PR; the discipline benefit is a clean, scannable public CHANGELOG that doesn't deter adopters reading it.

---

## 2026-06-21, Library Version 2026.06.108, PR #124

First-ever invocation of the `library-fitness-review` skill (`/fitness`). Ten persona subagents dispatched in parallel. Aggregate raw findings 145; after dedupe approximately 95 unique. Severity distribution: 18 high[critical] / 22 high / 31 medium / 24 low.

This PR ships the report and the remediation backlog ONLY. No corpus content is changed by this PR. Each finding has a remediation backlog ID (`FR-1` through `FR-111`); the maintainer prioritises and drives subsequent PRs to close each item.

### Added (under `.working/`, exempt from corpus audit gates)

- [`.working/fitness-reviews/2026-06-21-r1.md`](.working/fitness-reviews/2026-06-21-r1.md): full 8-section combined report with executive summary, per-page findings (~50 file locations identified), 10 cross-library patterns, 21 prioritised recommendations grouped P1-P6, standardisation recommendations, and the FR-1 through FR-111 remediation backlog.

### Changed

- [`.working/fitness-reviews/history.md`](.working/fitness-reviews/history.md): version `1.0.0 -> 1.1.0`. First fitness-review row appended; declares `Personas: A-J (all 10)` per dispatch-declaration discipline. Open remediation backlog table populated with the 17 high[critical] items as a scannable summary; full FR-1-FR-111 backlog tracked in the detail file.
- [`README.md`](README.md): library version `2026.06.107 -> 2026.06.108`; README version `1.8.63 -> 1.8.64`.

### High[critical] findings summary

1. **Maturity ladder fragmentation** (FR-14): three conflicting models across [`governance/framework-governance-performance-and-improvement.md`](governance/framework-governance-performance-and-improvement.md), [`docs/template-maturity-self-assessment.md`](docs/template-maturity-self-assessment.md), [`governance/register-digital-trust-and-assurance-metrics.md`](governance/register-digital-trust-and-assurance-metrics.md).
2. **Data classification fragmentation** (FR-43): 4-level vs 5-level split across foundational docs.
3. **DPO operational template gaps** (FR-29 through FR-34): DPIA, DPA Article 28, Privacy by Design (Art 25), LIA, Article 36 prior consultation, TIA — all referenced as required but no templates exist.
4. **Audit-discipline ceilings absent** (FR-16, FR-19, FR-21): exception register no max-duration; CAPA extensions no governance ceiling; obligations register accepts low-precision citations.
5. **ERM standard owner category error** (FR-9): owned by CIO; should be CRO or Board for enterprise risk.
6. **Coverage gaps** (FR-70 through FR-73): crypto-asset / blockchain governance; M&A due diligence; sanctions/OFAC; AI ethics review process.
7. **SIEM/cloud-log retention contradiction** (FR-80): 3-year SIEM retention vs 90-day cloud-activity-log minimum.

### Library strengths confirmed by multiple personas

- AI / agentic security ([`ai/standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md)) is exemplar-grade: 16 threat classes including TC-12 Tool Metadata Poisoning, TC-13 Multimodal Injection, TC-14 Goal Theft/Drift.
- Threat modelling standard operationalises STRIDE-per-boundary + LINDDUN.
- Post-quantum cryptography roadmap aligns with NIST FIPS 203/204/205 (Aug 2024) and CNSA 2.0.
- Supply chain SCA/SBOM/SLSA guidance current with 2024-2025 attack patterns.
- Breach response and DSAR workflows are production-quality.
- Three-lines-of-defence assurance map structurally sound.

### Recommendation priorities

- **Q1 (audit/regulatory exposure)**: Rec-1 maturity reconciliation, Rec-2 classification reconciliation, Rec-3 DPO operational templates, Rec-4 audit-discipline ceilings, Rec-5 retention contradiction.
- **Q1-Q2 parallel**: Rec-6 README rework, Rec-7 entry-point reconciliation, Rec-9 inheritance vocabulary.
- **Q2-Q3**: Rec-11 healthcare HIPAA detail, Rec-12 FS jurisdiction overlays, Rec-13 AI jurisdiction annexes, Rec-14 new domain documents (crypto-asset, M&A, sanctions, AI ethics).

### Publication readiness

**Not yet recommended.** The DPO operational template gaps are visible to any privacy-savvy reader; addressing them is a quarter of focused work. Post-Rec-3 + Rec-4 + Rec-6 the library reaches publication-grade.

### Verification

All 44 audit gates pass standalone post-commit. Full report file and history row + remediation backlog table all in `.working/fitness-reviews/` (exempt from corpus audit gates per design).

This PR adds capability state to `.working/`; no corpus content is changed by this PR. Each remediation backlog item is the seed for a subsequent PR; the maintainer prioritises.

---

## 2026-06-21, Library Version 2026.06.107, PR #123

Sweep 10 iteration 3 close-out: one in-window Medium finding actioned. Convergence-delta narrowing from iter 2's 7 findings to iter 3's 1.

Full A/B/C subagent fan-out per Rule 5.6. Subagent A returned zero findings. Subagent C returned zero findings (steady state confirmed: 44/44 gates pass, zero parity-surface drift, preflight exemption hash-verified). Subagent B caught one drift: [`TODO.md:16`](TODO.md) "Library version at HEAD" said `2026.06.105 / README 1.8.61` but post-PR-#121 HEAD is `2026.06.106 / 1.8.62`. Subagent A had classified this as as-of-session-pause and not a finding; Subagent B noted the line literally reads "at HEAD" (a current-state claim). Per Rule 5.3 pick-higher debate adjudication: B's classification holds.

This is the same drift pattern iter 2 caught (TODO snapshot one PR behind the version bump performed in the same close-out PR). This PR breaks the recurrence by writing the TODO snapshot using POST-PR-#123-bump values (`.107 / .63`) — the snapshot is now current as of this PR's merge, not one PR behind.

### Fixed

- [`TODO.md`](TODO.md): line 16 "Library version at HEAD" updated from `2026.06.105 / README 1.8.61` to the post-PR-#123-bump values `2026.06.107 / README 1.8.63`. Proactive fix: written using post-bump values so the snapshot is current at PR merge, not one PR behind. If iter 4 re-surfaces the same shape, the convention itself needs adjustment (e.g., explicitly framing the snapshot as as-of-session-pause to sidestep the "at HEAD" reading).

### Changed

- [`.working/validate-sweeps/history.md`](.working/validate-sweeps/history.md): version `2.0.1 -> 2.0.2`. Sweep 10 iter 3 row appended with `Subagents: A, B, C` per Rule 5.6.
- [`README.md`](README.md): library version `2026.06.106 -> 2026.06.107`; README version `1.8.62 -> 1.8.63`.

### Added (under `.working/`, exempt from corpus audit gates)

- [`.working/validate-sweeps/2026-06-21-sweep10-iter3.md`](.working/validate-sweeps/2026-06-21-sweep10-iter3.md): per-iteration detail file with the A/B/C subagent reports, the one-finding synthesis, debate adjudication, and pattern observation.

### Verification

All 44 audit gates pass standalone post-commit. Pre-flight scanner: 0 candidates. Convergence-delta status: strong narrowing iter-2 to iter-3 (7 → 1; -86%) but not yet empty-delta. The next sweep (post any subsequent substantive PR) will test whether THIS PR's close-out introduced new drift.

---

## 2026-06-21, Library Version 2026.06.106, PR #121

Sweep 10 iteration 2 close-out: seven in-window findings actioned post the three-PR overnight sequence (PRs #118-#120).

Full A/B/C subagent fan-out per Rule 5.6. Subagent A surfaced eleven findings (one High actionable, two Low actionable, eight FYI parity confirmations). Subagent B surfaced four findings (all TODO resume-state drift). Subagent C surfaced zero blocking and one advisory (corroborating Subagent A's High). After dedupe: 7 unique findings (1 High, 3 Medium, 3 Low). All in-window; all fixed here.

### Fixed

- [`tools/sweep-preflight-exemptions.json`](tools/sweep-preflight-exemptions.json): re-added the pre-flight scanner exemption for [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) line 121 ("Six rules, no ceremony"; the synthesis-rubric sub-rules 5.1-5.6 reference, not a governance-rule count). The previous exemption (line_hash `eca081c59b46035c`) was removed in PR #117 when the line text changed from "Four rules" to "Six rules"; PR #117 did not re-add a fresh exemption for the new line content, so every subsequent sweep re-surfaced the candidate. New line_hash: `2ae34a0ce24f10c3` (computed via SHA-256 prefix of the stripped line). (Subagent A High; Subagent C advisory corroborating.)
- [`TODO.md`](TODO.md): "Active session work" section refreshed. Resume-state version snapshot updated (library `2026.06.104 -> 2026.06.105`, pack `1.29.0 -> 1.30.0`, README `1.8.60 -> 1.8.61` — Subagent B M); last-validation-sweep cursor updated to reflect Sweep 10 iter 2 (Subagent B L); two stale "7 personas" references corrected to "10 personas" with the three-persona expansion noted (Subagent B M x 2); PRs completed list extended to include #119, #120, #121.
- [`CHANGELOG.md`](CHANGELOG.md): PR #120 entry's "(new, version 1.0.0)" claim for the SKILL.md was incorrect; pack skills do not carry frontmatter version numbers (verified against [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) and other pack skills). Corrected to "(new)" with a note that pack-level versioning in the pack README's version-history table tracks skill additions. (Subagent A Low.)
- [`.working/overnight-pr.md`](.working/overnight-pr.md): "Status (live): in progress, building skill files" was sanctioned per `.working/` frozen-state convention but misleading after PR #120 merged. Updated to reflect post-merge state. "Notes for morning review" section populated with: review checklist, recommendations for next session, files touched, corpus-boundary confirmation. (Subagent A Low.)

### Changed

- [`.working/validate-sweeps/history.md`](.working/validate-sweeps/history.md): version `2.0.0 -> 2.0.1`. Sweep 10 iter 2 entry appended; `Subagents dispatched: A, B, C` declared per Rule 5.6.
- [`README.md`](README.md): library version `2026.06.105 -> 2026.06.106`; README version `1.8.61 -> 1.8.62`.

### Added (under `.working/`, exempt from corpus audit gates)

- [`.working/validate-sweeps/2026-06-21-sweep10-iter2.md`](.working/validate-sweeps/2026-06-21-sweep10-iter2.md): per-iteration detail file with the full A/B/C subagent reports, the seven-finding synthesis, severity adjudication, and triage decisions. Second per-iteration file under the convention established in PR #115 and finalised in PR #118.

### Verification

All 44 audit gates pass standalone post-commit. Pre-flight scanner now returns 0 candidates with the re-added exemption. Subagent C confirmed all four-surface parity (runner, workflow, pre-commit, §6 spec) intact across the touched linters ([`tools/lint-followup-ageing.py`](tools/lint-followup-ageing.py), [`tools/lint-paired-skill-step-parity.py`](tools/lint-paired-skill-step-parity.py)); gate 41 (collection-enumeration) confirms the new `library-fitness-review` skill enumerated correctly.

### Pattern observation

This iteration's finding pattern is exactly the validation-sweep's intended catch: post-PR prose drift that the mechanical gates cannot detect. The preflight-exemption finding is a specific recurring shape (rotate-line-hash-when-content-changes); the TODO drift is an unavoidable consequence of capturing resume-state at session-pause when subsequent PRs land before resume. Both are healthy — the sweep caught them and the close-out actioned them.

---

## 2026-06-21, Library Version 2026.06.105, PR #120

Adds a new `library-fitness-review` skill to the `dev-security/claude-rules/` pack, invoked via the `/fitness` slash command. The skill is a comprehensive whole-corpus library-quality review dispatching ten persona reviewers in parallel (executive, security practitioner, GRC practitioner, auditor, policy editor, process owner, skeptical reader, adoption practitioner, privacy officer, newcomer). Designed as a periodic deliverable (after major changes or quarterly minimum), not a per-PR gate; complements the per-PR `validation-sweep` skill (`/validate`). Output is an 8-section combined report with a discrete remediation backlog. This PR was authored end-to-end during an overnight session under explicit maintainer authorisation; see [`.working/overnight-pr.md`](.working/overnight-pr.md) for the decision log.

### Added

- [`dev-security/claude-rules/skills/library-fitness-review/SKILL.md`](dev-security/claude-rules/skills/library-fitness-review/SKILL.md) (new): the skill following [`skill-authoring-discipline`](dev-security/claude-rules/skills/skill-authoring-discipline/SKILL.md)'s eight-section structural template. Pack skills do not carry frontmatter version numbers; pack-level versioning in the pack README's version-history table tracks skill additions and revisions. Frontmatter `derives_from` points at [`evidence-grounded-completion`](dev-security/claude-rules/governance/evidence-grounded-completion.md) (the same parent as `validation-sweep`); the discipline this skill operationalises is fresh-reader review at corpus scope across ten persona lenses.
- [`.claude/commands/fitness.md`](.claude/commands/fitness.md) (new): slash-command wrapping the skill. Nine-step process matching the SKILL.md's Process section.
- [`.working/fitness-reviews/`](.working/fitness-reviews/) (new activity directory, canonical `.working/<activity>/` layout per PR #118):
  - [`.working/fitness-reviews/README.md`](.working/fitness-reviews/README.md) — static convention info: per-run file format spec (8 H2 sections), ten-persona catalogue with scope and focus questions per persona, severity model (SARIF-lite + `[critical]` flag inside High), output flow, audit-gate exemption, adopter guidance, framework alignment.
  - [`.working/fitness-reviews/history.md`](.working/fitness-reviews/history.md) — empty cumulative table with column headers (Date / Run / Personas / Findings / Resulting PR / Detail / Summary) and an empty Open remediation backlog table.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.29.0 -> 1.30.0`; directory tree row added for the new skill; version-history row added.
- [`tools/lint-paired-skill-step-parity.py`](tools/lint-paired-skill-step-parity.py): `PAIRS` table extended with the new skill-and-command pair so gate 44 enforces step-identifier parity between SKILL.md and slash command.
- [`.working/README.md`](.working/README.md): activity table row added for the new fitness-reviews activity.
- [`README.md`](README.md): library version `2026.06.104 -> 2026.06.105`; README version `1.8.60 -> 1.8.61`.

### Design decisions (full rationale in [`.working/overnight-pr.md`](.working/overnight-pr.md))

- **Ten personas, not seven**: the original prompt specified seven; this implementation expands to ten by adding adoption practitioner (closest to library's real use case), privacy officer (privacy is a large library surface), and newcomer (true zero-knowledge complement to executive). Each addition is justified in [`.working/overnight-pr.md`](.working/overnight-pr.md). Capped at 10 to avoid synthesis-complexity inflation and per-persona focus dilution.
- **Severity model**: SARIF-lite (High/Medium/Low/FYI) with `[critical]` as a flag inside High for audit-failure / regulatory-exposure / control-failure class findings. Does not introduce a second severity scale.
- **Output**: single combined file per run with eight H2 sections (Executive Summary, Review Method, Page-by-Page Findings, Cross-Library Findings, Severity Model, Recommendations, Standardization Recommendations, Remediation Backlog). Optional Final Assessment section as a coda. Only written when findings exist; zero-finding runs leave only a history-row trace.
- **No mechanical gate enforces fitness-review pass**: the skill produces a deliverable, not a per-PR gate. Output informs human prioritisation; remediation IDs (`FR-1`, `FR-2`, ...) drive subsequent PRs.

### Verification

All 44 audit gates pass standalone post-commit. Gate 44 (paired-skill step-parity) confirms SKILL.md and slash command files have matching step-identifier sets. Gate 41 (collection-enumeration consistency) confirms the new skill in the pack tree matches the skills directory. Skill-authoring-discipline's eight-section structural template followed (frontmatter with `name`/`description`/`derives_from`; H1 title; Overview / When to Use / Process / Red Flags / Verification / Common Rationalizations / See Also).

The skill has not yet been invoked against the corpus; its first run will be the validation reference. This PR ships the capability; the first `/fitness` invocation is a separate maintainer action.

---

## 2026-06-21, Library Version 2026.06.104, PR #118

Restructured `.working/validate-sweeps/` to the canonical `<activity>/{README,history,detail-files}` layout that becomes the standard for any `.working/<activity>/` subdirectory going forward. The validation-sweep history file moves into the subdirectory; verbose static content (failure-mode taxonomy, maintenance protocol, accept-list rules, dating discipline, framework alignment) moves to the subdirectory's README; the history file becomes a slim reverse-chronological table; per-iteration detail files are created only when findings exist.

The new pattern, for any activity directory under `.working/`:

| Artefact | Filename pattern | Purpose |
|---|---|---|
| Static convention info | the activity's `README` | What the activity is, file format spec, taxonomies, protocols, framework alignment, fork guidance |
| Cumulative history | the activity's `history` file | Reverse-chronological table: date, sweep ordinal, subagents dispatched, finding counts, resulting PR, summary. New rows on top. |
| Per-run detail | one dated file per run | Full report; **only when the run produced findings**. Zero-finding runs leave only a row in the history file. |

### Moved

- [`.working/validate-sweeps-history.md`](.working/validate-sweeps-history.md) (old path, no longer present) -> [`.working/validate-sweeps/history.md`](.working/validate-sweeps/history.md). The file is now inside the subdirectory alongside its README and per-iteration files; the activity's full footprint is now self-contained in one directory.

### Changed (extensive content reorganisation)

- [`.working/validate-sweeps/README.md`](.working/validate-sweeps/README.md): expanded from a short convention note to absorb all static content from the former top-level history file: purpose, file structure spec, failure-mode classes (C1-C8) with classification convention, dispatch declaration discipline (Rule 5.6), false-positive memory rules (Rules 6.1-6.3), dating discipline for deferred findings, audit-gate exemption notes, adopter guidance, framework alignment.
- [`.working/validate-sweeps/history.md`](.working/validate-sweeps/history.md): rewritten as a slim reverse-chronological table. New `Subagents` column declares dispatch (per Rule 5.6) in every row, including zero-finding iterations. Pre-existing detailed entries (Sweeps 1-10) summarised to one row each. Version `1.15.0 -> 2.0.0` (format change is breaking).
- [`.working/README.md`](.working/README.md): "Standard layout for each activity" section added documenting the three-artefact convention. Activity table replaces the previous subdirectory/top-level-files split.
- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): step 8 retitled and rewritten ("Append a row to the sweep history (every iteration)") with the new table-row format including the `Subagents` column. Step 9 retitled and rewritten ("Write the per-iteration detail file (only when findings exist)") to drop the every-iteration requirement. Rule 5.6 wording updated to point at the `Subagents` column. False-positive memory cross-reference updated to point at the README (which now holds the discipline rules).
- [`.claude/commands/validate.md`](.claude/commands/validate.md): step 8 and step 9 briefs updated to match SKILL.md.
- [`tools/lint-followup-ageing.py`](tools/lint-followup-ageing.py): `TARGET_FILES` updated to the relocated history file's new path. Docstring updated.
- [`tools/lint-gate-count-consistency.py`](tools/lint-gate-count-consistency.py): comment about the relocated file updated.
- [`tools/sweep-preflight-scanner.py`](tools/sweep-preflight-scanner.py): comment about the file updated.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.28.2 -> 1.29.0`; version-history row added.
- [`README.md`](README.md): library version `2026.06.103 -> 2026.06.104`; README version `1.8.59 -> 1.8.60`.

### Convention now applies to all future `.working/<activity>/` subdirectories

When future skills add new activity subdirectories under `.working/` (e.g. `.working/fitness-reviews/` when the fitness-review skill ships), they follow this convention: a README for static info, a history file for the cumulative table, and dated files for per-run detail only when findings exist. Documented in [`.working/README.md`](.working/README.md).

### Verification

All 44 audit gates pass standalone post-commit. Gate 43 (`lint-followup-ageing`) successfully targets the relocated file at its new path. The pre-flight scanner returns 0 candidates (consistent with prior baseline). The validation-sweep skill's two steps now map cleanly to the simpler convention: one table row per iteration; one detail file only when there is something to detail.

---

## 2026-06-21, Library Version 2026.06.103, PR #117

Sweep 10 iteration 1 close-out: six in-window prose drift findings actioned, all introduced or made visible by the three-PR `.working/` sequence (PRs #114-#116).

The sweep ran with full A/B/C fan-out per Rule 5.6. Subagent A returned 6 findings, Subagent B corroborated 2 of them, Subagent C returned zero. After dedupe: 6 unique findings (2 High, 2 Medium, 2 Low). All in-window; all fixed here.

### Fixed

- [`.claude/commands/validate.md`](.claude/commands/validate.md): line 1 preamble said "eight-step process" but the file body has 9 numbered steps (step 9 added in PR #115). Corrected to "nine-step". Per-iteration-record section list at lines 19-24 reformatted to H2 comma form (matching the SKILL.md spec; previously used bold "full report" labels that didn't match either of the other two surfaces).
- [`.working/README.md`](.working/README.md): subdirectory inventory table said `*(none yet)*` despite PRs #115 and #116 having added `validate-sweeps/` (subdirectory) and [`.working/validate-sweeps-history.md`](.working/validate-sweeps-history.md) (top-level file). Inventory rewritten to list both children, with a separate table for subdirectories and top-level files. "To add a new subdirectory" instruction updated to cover both forms.
- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): three prose drift fixes. Line 29 Process intro `"seven steps" → "nine steps"` (step 8 from PR #75 and step 9 from PR #115 were never reflected in the intro). Line 121 step 5 intro `"Four rules, no ceremony" → "Six rules"` (Rules 5.1-5.6 exist; rules 5.5 and 5.6 added in PRs #93 and #111). Line 135 awkward possessive on closing parenthesis rephrased (`...path)'s false-positive memory section` → `...false-positive memory section of the project's validation-sweep history register (in this project: ...)`).
- [`.working/validate-sweeps/README.md`](.working/validate-sweeps/README.md): section-header form converted from em-dash to comma to match the SKILL.md canonical form. Three surfaces (SKILL.md, slash command, this README) now agree.
- [`tools/sweep-preflight-exemptions.json`](tools/sweep-preflight-exemptions.json): removed the now-stale exemption for [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) line_hash `eca081c59b46035c` (the "Four rules, no ceremony" line). The line content changed in this PR; the line_hash no longer matches; the exemption became dead weight. The candidate will re-surface naturally on the next sweep with the new line content for re-triage if needed.

### Changed

- [`.working/validate-sweeps-history.md`](.working/validate-sweeps-history.md): version `1.14.0 -> 1.15.0`. Sweep 10 iteration 1 entry appended; `Subagents dispatched: A, B, C` declared per Rule 5.6.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.28.1 -> 1.28.2`; version-history row added.
- [`README.md`](README.md): library version `2026.06.102 -> 2026.06.103`; README version `1.8.58 -> 1.8.59`.

### Added (under `.working/`, exempt from corpus audit gates)

- [`.working/validate-sweeps/2026-06-21-sweep10-iter1.md`](.working/validate-sweeps/2026-06-21-sweep10-iter1.md): first per-iteration record under the convention established by PR #115. Six H2 sections: trigger & state snapshot, three subagent verbatim reports, orchestrator synthesis, resulting PR. This file dogfoods the convention.

### Discipline observation

All six findings are post-PR prose drift: a sentence written from one mental model that subsequent PRs invalidated. The pattern recurs (Sweep 9 iteration 3 caught three; Sweep 10 iteration 1 caught six). Mechanical gates can't catch this class because the prose is internally well-formed; only the cross-surface validation-sweep does. The lesson is to apply the evidence-grounded-completion discipline (re-read what you wrote, contradiction-search against sibling surfaces) at PR-authoring time, not only at PR-merge time.

### Verification

All 44 audit gates pass standalone post-commit. The validation-sweep's own iteration record (this PR) is the first dogfooded instance of the per-iteration-record convention established in PR #115.

---

## 2026-06-21, Library Version 2026.06.102, PR #116

Move the validation-sweep history file from `governance/` to `.working/`. The file is project-specific application of the validation-sweep discipline, not template content for adopters; per the framing established with the maintainer, application belongs in `.working/`. Template content (the failure-mode class taxonomy, the maintenance protocol, the false-positive accept-list rules, the dispatch-declaration discipline) lives in the [`validation-sweep` SKILL.md](dev-security/claude-rules/skills/validation-sweep/SKILL.md) in the pack; adopters get the discipline from the SKILL.md and start their own history file from zero in their fork.

### Moved

- [`governance/register-sweep-history.md`](governance/register-sweep-history.md) (old path, no longer present) -> [`.working/validate-sweeps-history.md`](.working/validate-sweeps-history.md). Version `1.13.0 -> 1.14.0` (document moved; metadata block slimmed to maintainer-working-state fields). Repository Path field updated. Purpose section updated to explain the move and clarify the file's status as project-specific application of the discipline.

### Removed

- The "Validation Sweep History Register" row in [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md). The file is no longer in the Public corpus index; it's maintainer working state. Document-index version `1.27.21 -> 1.27.22`.
- The corresponding row in [`governance/README.md`](governance/README.md). Version `1.10.3 -> 1.10.4`.
- The redundant per-file exemption for the old path in [`tools/lint-gate-count-consistency.py`](tools/lint-gate-count-consistency.py) (`.working/` is in `DEFAULT_EXEMPT_DIRS`, so the per-file exemption is no longer needed).
- The redundant pre-flight-scanner exemption entry for the old path in [`tools/sweep-preflight-exemptions.json`](tools/sweep-preflight-exemptions.json) (the file is now in `.working/` which the scanner already skips).

### Changed

- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): three references to the sweep history file rewritten with the same template-vs-project-path pattern step 9 uses (path-agnostic in the SKILL.md; project-specific path called out parenthetically). No process change; adopters can put the file wherever fits their structure.
- [`.claude/commands/validate.md`](.claude/commands/validate.md): step 8 reference updated to the new path with the same path-agnostic framing.
- [`.working/validate-sweeps/README.md`](.working/validate-sweeps/README.md): cross-references to the sweep history file updated to the new path; "Relationship to the register" section retitled to "Relationship to the cumulative history file" for naming consistency.
- [`tools/lint-followup-ageing.py`](tools/lint-followup-ageing.py): `TARGET_FILES` updated to the relocated file's new path under `.working/`. Docstring updated to explain that the gate intentionally targets a file inside `.working/` despite the default exemption (the gate's purpose is to track deferred-finding deadlines in maintainer working state).
- [`tools/sweep-preflight-scanner.py`](tools/sweep-preflight-scanner.py): comment updated for the file's new path.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.28.0 -> 1.28.1`; version-history row added.
- [`README.md`](README.md): library version `2026.06.101 -> 2026.06.102`; README version `1.8.57 -> 1.8.58`.

### Why this is a separate PR (per the four-PR sequence)

PR #114 shipped the `.working/` infrastructure. PR #115 shipped the `/validate` rename + per-iteration record convention into `.working/validate-sweeps/`. This PR completes the validation-sweep tooling's relocation by moving the history file. Subsequent PRs in the sequence are the changelog-details migration and the `/fitness` skill addition.

Other registers and tool-state files that look like candidates for the same move ([`tools/sweep-preflight-exemptions.json`](tools/sweep-preflight-exemptions.json), the citation-verification cluster, [`governance/register-main-branch-protection.md`](governance/register-main-branch-protection.md)) are queued as separate small PRs to keep each change focused.

### Verification

All 44 audit gates pass standalone post-commit. Gate 43 (follow-up ageing) continues to scan the relocated file at its new path (linter `TARGET_FILES` updated). The cross-references in [`.working/validate-sweeps-history.md`](.working/validate-sweeps-history.md) itself were updated for the relative-path shift from `governance/` to `.working/`. Historical CHANGELOG entries that reference the old path stay as-is (CHANGELOG is not scanned by [`tools/lint-links.py`](tools/lint-links.py); the historical record is preserved).

---

## 2026-06-21, Library Version 2026.06.101, PR #115

`/validate` slash-command rename + per-iteration record convention. Second of the four-PR sequence around `.working/` (PR #114 shipped the infrastructure; this PR populates the first subdirectory and adds the persistent-record discipline to the validation-sweep skill).

### Renamed

- [`.claude/commands/validate.md`](.claude/commands/validate.md) — renamed from [`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md) (old path, no longer present). Short ergonomic slash command; the underlying skill name remains `validation-sweep` (descriptive identifier for the workflow's purpose). Slash commands and skills are independent identifiers; the command file wraps the skill invocation, the skill is the underlying workflow.

### Added

- [`.working/validate-sweeps/README.md`](.working/validate-sweeps/README.md): convention document for per-iteration records. Filename pattern is `YYYY-MM-DD-sweepN-iterM` plus `.md` extension; six top-level H2 sections capturing trigger/state, three subagent verbatim reports, orchestrator synthesis, resulting PR. Zero-finding iterations write the record but no register entry (the convention "zero-finding sweeps leave no trace in the register" applies only to the register; the per-iteration record is the persistent trace for those iterations).
- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): new step 9, "Write the per-iteration record". Six-section file format specified. Adopters relocate the working directory to a project-appropriate path; this project uses `.working/validate-sweeps/`.

### Changed

- [`.claude/commands/validate.md`](.claude/commands/validate.md): step 9 added (mirrors SKILL.md step 9 brief); top-of-file prose distinguishes the slash command `/validate` from the underlying skill name `validation-sweep`; eight-step process updated to nine-step.
- [`tools/lint-paired-skill-step-parity.py`](tools/lint-paired-skill-step-parity.py): `PAIRS` table updated for the renamed command path ([`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md) old, [`.claude/commands/validate.md`](.claude/commands/validate.md) new).
- [`tools/sweep-preflight-scanner.py`](tools/sweep-preflight-scanner.py): docstring updated for the `/validate` slash command name.
- [`.github/workflows/nightly-sweep.yml`](.github/workflows/nightly-sweep.yml): comment updated for the renamed slash command.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md): Sweep History Register's review-frequency description updated for the new slash command name.
- [`governance/register-sweep-history.md`](governance/register-sweep-history.md): version `1.12.1 -> 1.13.0`. Preamble updated to reference `/validate` and to direct readers to `.working/validate-sweeps/` for per-iteration detail. Sweep 5's entry updated with a parenthetical noting the slash command rename so historical context is preserved.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.27.1 -> 1.28.0`. Version-history row added for 1.28.0.
- [`README.md`](README.md): library version `2026.06.100 -> 2026.06.101`; README version `1.8.56 -> 1.8.57`.

### Discipline observation

PR #115 ships the rename and the per-iteration record convention; it does NOT move [`governance/register-sweep-history.md`](governance/register-sweep-history.md) to `.working/`. That move (the register is project-application-of-the-discipline rather than template content; per the framing established with the maintainer, application belongs in `.working/`) is queued as PR #116 to keep this PR focused on the rename + record convention.

### Verification

All 44 audit gates pass standalone post-change. Gate 44 (paired-skill step-parity) confirms the SKILL.md step list (1, 2, 3, 3a, 4, 5, 6, 7, 8, 9) matches the slash command's step list at the renamed path.

---

## 2026-06-21, Library Version 2026.06.100, PR #114

Establishes the `.working/` top-level convention for maintainer working state. First of a four-PR sequence: this PR ships the infrastructure; subsequent PRs (`/validate` rename + per-run records, `/fitness` skill, changelog-details migration) populate the convention with content.

### Added

- [`.working/README.md`](.working/README.md): top-level convention document. `.working/` holds maintainer-only operational artefacts (per-run records, detailed reports, working drafts) that assist the maintainer but are not part of the published library content. Frozen-state archives (cross-references accurate as-of write-time), exempt from audit gates, not for adopter consumption. Fork-time guidance: adopters may delete `.working/` outright or keep it as historical reference; either is fine.

### Changed

- [`tools/lint_common.py`](tools/lint_common.py): `DEFAULT_EXEMPT_DIRS` extended to include `.working`. Joins `.git`, `node_modules`, `__pycache__`, and `.claude` as the always-skipped directories. Rationale comment in the module docstring explains the frozen-state archive convention.
- [`.claude/CLAUDE.md`](.claude/CLAUDE.md): `## Structure` section gains a bullet documenting `.working/` for fresh sessions; the `DEFAULT_EXEMPT_DIRS` enumeration is updated to include `.working`.
- [`README.md`](README.md): library version `2026.06.99 -> 2026.06.100`; README version `1.8.55 -> 1.8.56`.

### Why this is a separate PR

The `.working/` convention is infrastructure that two follow-on PRs (the `/validate` rename + per-run records to `.working/validation-sweeps/`, and the new `/fitness` skill writing to `.working/fitness-reviews/`) both depend on. Landing the convention first means each consumer PR is small and focused, and the convention's design (top-level dot-prefix, README contract, audit exemption) gets one round of review rather than being bundled with skill or rename work.

### Verification

All 44 audit gates pass standalone post-change. The new `.working/` directory contains only its README; no content yet. The exempt-dir change is additive (no previously-scanned files become skipped).

---

## 2026-06-21, Library Version 2026.06.99, PR #113

Sweep 9 iteration 3 close-out: three documentation findings from Subagent A's deep-review of PR #112 actioned.

The iteration 3 re-baseline ran the full A/B/C subagent fan-out (per Rule 5.6 unconditional dispatch). Subagent B (corpus-wide stale-reference sweep) and Subagent C (audit-programme integrity reviewer) both returned zero findings; Subagent A (PR #112 deep review) returned one High, one Medium, and one Low finding — all within PR #112's own newly-written prose, all surfacing post-hoc inconsistencies that the mechanical gates do not detect.

### Fixed

- [`governance/register-sweep-history.md`](governance/register-sweep-history.md): version `1.12.0 -> 1.12.1`. Line 181 Sweep value paragraph said the iteration-2 finding's `# N <word> gates` shape was one "that P6 caught (the file was scanned)" — self-contradictory, because P6 in fact missed that shape (P7 was added in PR #112 to close exactly that gap). Corrected to "P6 missed (P6 required `\s+gates?` immediately after the digit; the intervening `corpus` defeated the regex). P7 was added in this PR to close that gap." (Subagent A High finding.)
- [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md): the 7th-rule reference attributed the rule's origin to the "orchestrator-skip cascade where an inferred 'no parity-surface changes' premise drove a subagent-skip" — but that trigger was already addressed by Rule 5.6 in PR #111. The actual immediate trigger for the 7th rule (consistent with the dev-security pack CLAUDE.md description, the CHANGELOG entry for PR #112, and the pack rule's own "Why this rule exists" section) was the fix-completeness inference (PR #111's close-out inferring fix-completeness from one occurrence) that Sweep 9 iteration 2 caught. Description updated to list the three recurring inference triggers and name the immediate one. (Subagent A Medium finding.)
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.27.0 -> 1.27.1`. Directory-tree section's `governance/` line said "initial rollout complete at pack 1.11.0; extended at 1.21.0" without mentioning the 1.27.0 extension that added the 7th rule. Other pack surfaces (version-history table, "When to use each rule" table, both CLAUDE.md files) were updated in PR #112; this one comment was missed. Corrected to "extended at 1.21.0 and 1.27.0". (Subagent A Low finding.)

### Changed

- [`governance/register-sweep-history.md`](governance/register-sweep-history.md): Sweep 9 iteration 3 entry appended; declares `Subagents dispatched: A, B, C`; documents the three Subagent A findings with severity and the structural lesson (these were post-hoc prose inconsistencies that existing evidence-grounded-completion would have caught if applied to the new register entry before commit; no new structural rule needed).
- [`README.md`](README.md): library version `2026.06.98 -> 2026.06.99`; README version `1.8.54 -> 1.8.55`.

### Discipline observation

The three iteration-3 findings were not regressions in the corpus — they were in PR #112's own newly-written prose, surfacing within hours of being committed. The evidence-grounded-completion discipline (re-read what you wrote, contradiction-search across surfaces) would have caught all three if applied to the new register entry, the new [`.claude/CLAUDE.md`](.claude/CLAUDE.md) reference, and the new directory-tree comment before PR #112 was committed. The lesson is not "add another rule" but "apply the existing rules to authoring, not just to verification". The new 7th rule and Rule 5.6 are upstream of this gap; this iteration's findings are about *applying* the discipline, not about the discipline being incomplete.

### Verification

All 44 audit gates pass standalone post-fix. The three corrections are internally consistent: register-sweep-history.md:181 prose now matches PR #112's commit message and the new rule's own narrative; [`.claude/CLAUDE.md`](.claude/CLAUDE.md) description now matches the dev-security pack CLAUDE.md description; pack README directory tree now mentions all three rollout extensions.

---

## 2026-06-21, Library Version 2026.06.98, PR #112

Sweep 9 iteration 2 closure + seventh governance rule ([`validate-inference-before-action.md`](dev-security/claude-rules/governance/validate-inference-before-action.md)).

PR #111's close-out claimed completion after fixing the one `42 corpus gates` occurrence Subagent C surfaced (in [`tools/run_all_audits.sh`](tools/run_all_audits.sh):65). That claim was inferred-complete on the basis of a single occurrence rather than a corpus-wide search for parallel ones. Sweep 9 iteration 2 re-baselined and Subagent B found the parallel occurrence in [`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py):5 — same shape, same drift, missed because the previous PR's close-out inferred rather than validated. The discipline failure is at the close-out, not at gate 39's regex; the structural fix is a new pack rule that fires at the inference-driven-action surface as the action-side counterpart of `evidence-grounded-completion`.

### Added

- [`dev-security/claude-rules/governance/validate-inference-before-action.md`](dev-security/claude-rules/governance/validate-inference-before-action.md) (new, version 1.0.0): the seventh pack governance rule. Discipline: when the next action depends on an inferred premise (a state claim not directly observed in the current turn), validate the premise via a tool call before taking the action. Trigger surface: clauses of the form `since / because / given X, [action]` where X is a state claim that has not been observed in the current turn. The protocol is four steps: identify the inference, cost the validation, validate, act on the validated observation. The rule's worked example is this PR's cascade: Sweep 9 iter 1 → PR #111 inferred fix-completeness → Sweep 9 iter 2 surfaced the missed parallel occurrence. Mirrored to [`.claude/rules/governance/validate-inference-before-action.md`](.claude/rules/governance/validate-inference-before-action.md) for in-project session loading.
- [`tools/lint-gate-count-consistency.py`](tools/lint-gate-count-consistency.py): pattern P7 added — `\b(\d{2,})\s+[a-z]{2,12}\s+gates?(?![-\w])` — closes the `N <word> gates` shape that P6 missed (P6 required `\s+gates?` immediately after the digit; P7 allows one intervening word like `corpus` or `mandatory`). Added [`governance/register-sweep-history.md`](governance/register-sweep-history.md) to `EXEMPT_FILES` because the register's historical "State:" snapshots legitimately quote past gate counts (e.g. `44 corpus gates`) and would otherwise false-positive on every sweep entry as the count grows.

### Changed

- [`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py): line 5 comment `42 corpus gates -> 44 corpus gates`. Subagent B iteration-2 finding; the parallel occurrence to the iteration-1 PR #111 fix.
- [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md): added the seventh rule reference under `## Security and governance requirements`; updated the phased-rollout narrative to include the 1.27.0 extension.
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md): added the seventh rule's bullet describing the trigger surface and discipline; updated the rollout-history paragraph.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.26.17 -> 1.27.0`. Pack scope line lists the seventh rule. Directory tree row added. "When to use each rule" row added. Version-history row `1.27.0 | 2026.06.98 | 2026-06-21` appended.
- [`dev-security/claude-rules/skills/skill-authoring-discipline/SKILL.md`](dev-security/claude-rules/skills/skill-authoring-discipline/SKILL.md): step 2 prose `six governance rules -> seven`.
- [`tools/lint-collection-enumeration-consistency.py`](tools/lint-collection-enumeration-consistency.py): docstring `six governance rules -> seven`.
- [`governance/register-sweep-history.md`](governance/register-sweep-history.md): version `1.11.0 -> 1.12.0`. Sweep 9 iteration 2 entry appended; declares `Subagents dispatched: A, B, C` per Rule 5.6; documents the inference-cascade discipline failure and links the structural fix (the new pack rule).
- [`README.md`](README.md): library version `2026.06.97 -> 2026.06.98`; README version `1.8.53 -> 1.8.54`.

### Discipline gap and the fix

The failure mode: PR #111's close-out fixed the C-2 finding (`tools/run_all_audits.sh:65`) and inferred that the fix was complete. The inference was wrong — a parallel occurrence existed in [`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py):5 with the same `42 corpus gates` shape — and the cascade propagated into the next iteration's surface area. The structural defence is the new pack rule: at any decision boundary where an action depends on an inferred premise, the premise must be validated via tool call before the action proceeds. For "fix is complete after one occurrence", the validation is one `grep` over the corpus for the pattern; the cost is bounded, the cascade prevented is unbounded.

### Verification

All 44 audit gates pass standalone post-fix. The extended gate 39 pattern (P7) catches the iteration-2 finding if re-introduced and does not false-positive on the register's historical State-snapshots. The new pack rule is referenced from both pack CLAUDE.md and project CLAUDE.md so a fresh session loads the discipline at the same precedence as the prior six rules.

---

## 2026-06-20, Library Version 2026.06.97, PR #111

Sweep 9 closure: Subagent C findings actioned + structural prevention of unauthorised subagent skips.

The post-P4.5 validation sweep initially dispatched only Subagents A and B; Subagent C was skipped on the orchestrator's incorrect "no parity-surface changes" justification (gate 39 source was just changed in PR #110 — that IS a parity surface). The maintainer flagged the skip as a discipline failure. Subagent C was then dispatched and returned two findings.

### Changed

- [`tools/lint-gate-count-consistency.py`](tools/lint-gate-count-consistency.py): Subagent C finding C-1. Module docstring's "Patterns scanned" list extended to include P6 (was P1-P5 only; the P6 added in PR #110 was documented inline but not in the top-of-file list).
- [`tools/run_all_audits.sh`](tools/run_all_audits.sh): Subagent C finding C-2. Line 65 comment `42 corpus gates -> 44 corpus gates`. The drift slipped past gate 39's P6 because "corpus" intervenes between "42" and "gates"; the gate's regex requires `\s+gates?` immediately after the digit.
- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): step 4 prose makes "all three subagents dispatched on every full sweep" unconditional and explicit; the only sanctioned exception is a maintainer-authorised thin sweep recorded in the register. **New Rule 5.6**: every sweep entry must declare which subagents were dispatched (e.g. `Subagents dispatched: A, B, C`), so a silent skip cannot be reconstructed later. The auditable trail IS the enforcement mechanism.
- [`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md): slash-command step 4 and step 5 mirror the SKILL changes (now references "six-rule synthesis rubric"; step 4 names the unconditional-dispatch discipline).
- [`governance/register-sweep-history.md`](governance/register-sweep-history.md): version `1.10.0 -> 1.11.0`. Sweep 9 entry appended; first entry to declare `Subagents dispatched: A, B, C`. Maintenance protocol updated with the dispatch-declaration requirement.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.26.16 -> 1.26.17`.
- [`README.md`](README.md): library version `2026.06.96 -> 2026.06.97`; README version `1.8.52 -> 1.8.53`.

### Discipline gap and the fix

The failure mode: the orchestrator inferred "no parity-surface changes since prior sweep" and skipped C, but gate 39's source was just changed in PR #110 — that IS a parity surface. The orchestrator's inference cascade went un-checked because the SKILL did not require a positive dispatch declaration. Silent absence cannot be reconstructed; the only point to enforce is the moment the orchestrator dispatches (or fails to dispatch) the subagent.

Rule 5.6's mechanism: every sweep entry in the register declares which subagents ran. The maintainer (or any reader) can verify three names appear; if fewer than three, the entry must include the maintainer authorisation. Mechanical enforcement could come later via a lint that scans register entries for the declaration; this PR ships the discipline first and the lint follows if drift recurs.

---

## 2026-06-20, Library Version 2026.06.96, PR #110

Validation-sweep finding (post-P4.5 sweep, Subagent B): two stale "42 gates" prose references that gate 39 missed. Plus a related pattern-set extension to close the gap going forward.

The post-P4.5 validation sweep dispatched Subagent A (recent-PR deep review, zero findings) and Subagent B (corpus-wide stale-reference sweep). Subagent B surfaced one in-window finding at [`tools/README.md`](tools/README.md):59 with the phrasing "runs the same 42 gates" that PF-04 missed (no `currently / now at` trigger) and gate 39 also missed (the existing patterns require an `audit` / `all` / hyphenated qualifier; the bare "N gates" shape was not caught). Manual re-read surfaced one more on the same file at line 7, plus a second stale claim in [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md):212.

### Changed

- [`tools/README.md`](tools/README.md): line 7 `42 gates -> 44 gates`; line 59 `42 gates -> 44 gates`. Plus a separate drift on line 7: `Gate 31 (gate-name parity audit)` corrected to `Gate 35 (gate-name parity audit)`. (The gate-name parity audit was renumbered from 31 to 35 over the gate-progression; the reference was missed.) No `Version:` field on this file so no per-doc bump.
- [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md): version `1.1.12 -> 1.1.13`. Line 212 `42 gates running in CI -> 44 gates running in CI`. Also extended the gate-list inline summary to cover the gates added since the entry was last refreshed (40 version-bump-recency, 41 collection-enumeration, 42 external-overlay license, 43 follow-up ageing, 44 paired-skill step-parity).
- [`tools/lint-gate-count-consistency.py`](tools/lint-gate-count-consistency.py): added pattern P6 (bare `N gates` where N is two or more digits, with a negative lookahead `(?![-\w])` to avoid matching `gate-name` / `gate-count` / `gates 1-44` shapes). The existing P1-P5 patterns required an `audit` / `all` / hyphenated qualifier; the new P6 catches the bare-N-gates shape this sweep surfaced.
- [`README.md`](README.md): library version `2026.06.95 -> 2026.06.96`; README version `1.8.51 -> 1.8.52`.

### Verification

All 44 audit gates pass standalone post-fix. The extended gate 39 pattern catches the two findings if re-introduced; existing legitimate uses of "N gates" prose elsewhere in the corpus do not false-positive on P6.

---

## 2026-06-20, Library Version 2026.06.95, PR #109

TODO P4.5: audit evidence package template. **Fifth and last of the Priority 4 items in sequence.**

Packages per-control evidence into an audit-ready bundle: a single navigable artefact an external auditor, regulator, or independent assessor can walk through. The library documents per-control evidence requirements across compliance and risk; the packaging step (assembling that evidence into a bundle organised for an outside reviewer) is what this template covers.

### Added

- [`compliance/template-audit-evidence-package.md`](compliance/template-audit-evidence-package.md): new Template document with:
  - **Cover page** (organisation, framework, audit type, period, scope, assembly team, retention).
  - **Control inventory index** flat-list of all in-scope controls with implementation status and operating effectiveness columns; auditor's primary navigation surface.
  - **Per-control sections** (one per control): framework references (primary plus secondary mappings), control description, implementation evidence point-in-time, operating evidence over the period, gaps and compensating controls, per-control sign-off.
  - **Optional per-domain summaries** for packages with 50+ controls.
  - **Optional cross-reference index** mapping shared evidence artefacts to the multiple controls they support.
  - **Package-level sign-off** (assembler, reviewer, approving authority).
  - **Anti-patterns to watch** (undated screenshots, sample-size-of-one tests, "see attached" without attachment, missing remediation plans, future-tense in past-period evidence, self-review).
  - **Eight review questions** before releasing the package.

### Changed

- [`TODO.md`](TODO.md): Priority 4.5 entry resolved; pointer to shipped template.
- [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md): version `1.1.11 -> 1.1.12`; §6 entry for "Audit evidence package templates" updated from `Partial / Planned / TODO P4.5` to `Substantive / In library / [link]`.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md): version `1.27.19 -> 1.27.20`; new row added.
- [`compliance/README.md`](compliance/README.md): version `1.4.2 -> 1.4.3`; new row added.
- [`README.md`](README.md): library version `2026.06.94 -> 2026.06.95`; README version `1.8.50 -> 1.8.51`.

### Priority 4 backlog: closed

All five Priority 4 items in TODO.md are now shipped (with the maintainer's authorial decisions integrated along the way):
- **4.1** Quickstart template (PR #103 then PR #105 rewrite to activity-modular, PR #108 rename to [`docs/template-quickstart.md`](docs/template-quickstart.md))
- **4.2** Maturity self-assessment template (PR #104)
- **4.3** Implementation roadmap template (PR #106)
- **4.4** Regulator interaction templates (PR #107)
- **4.5** Audit evidence package template (this PR)

### Verification

All 44 audit gates pass standalone.

---

## 2026-06-20, Library Version 2026.06.94, PR #108

Rename the adopter quickstart template from its prior "by-profile" filename to [`docs/template-quickstart.md`](docs/template-quickstart.md). Maintainer feedback: the file is no longer a per-profile template (after the P4.1 rewrite to activity-modular shape in PR #105), so the prior filename was misleading. The document title was already "Adopter Quickstart Template" so no title change is needed.

### Changed

- [`docs/template-quickstart.md`](docs/template-quickstart.md) (renamed from its prior "by-profile" filename): file rename + internal Repository Path metadata updated. Document version `2.0.0 -> 2.0.1`.
- [`docs/template-implementation-roadmap.md`](docs/template-implementation-roadmap.md): Related Documents and three inline references updated. Document version `1.0.0 -> 1.0.1`.
- [`docs/template-maturity-self-assessment.md`](docs/template-maturity-self-assessment.md): Related Documents updated. Document version `1.0.0 -> 1.0.1`.
- [`TODO.md`](TODO.md): P4.1 entry reference updated.
- [`CHANGELOG.md`](CHANGELOG.md): historical PR #103 and PR #105 entries updated to reference the new path (the file no longer exists at the old path; leaving the entries unchanged would have broken `lint-links`). This is a small history rewrite, consistent with the PR #97 retro-prune precedent. Maintainer explicitly authorised under the named-alternatives clarification.
- [`README.md`](README.md): library version `2026.06.93 -> 2026.06.94`; README version `1.8.49 -> 1.8.50`.

### Verification

All 44 audit gates pass standalone post-rename. Generated artefacts (taxonomy.yml, docs/portal.md, docs/maturity-scorecard.md) re-built. No remaining references to the old filename in any markdown or YAML file.

---

## 2026-06-20, Library Version 2026.06.93, PR #107

TODO P4.4: regulator interaction templates. Fourth of five Priority 4 items.

Consolidates the recurring regulator-facing interactions into reusable shapes. The library shipped incident-notification language inside per-jurisdiction privacy annexes and inside industry compliance overlays; this template provides the shape-only structure so an adopter facing first-time regulator contact does not have to reverse-engineer it.

### Added

- [`compliance/template-regulator-interaction.md`](compliance/template-regulator-interaction.md): new Template document with five sub-templates:
  1. **Breach notification**: discovery, nature, cause, containment, affected-individual notification, external parties, follow-up commitments, signatory. Examples of timing across GDPR / SEC / HIPAA / NIS 2 / DORA.
  2. **Attestation submission**: scope, statement, qualifications, material findings, compensating controls, changes since prior period, signatory.
  3. **Examination support**: pre-examination packet, pre-examination briefing, during-examination cadence, closing meeting, post-examination findings response, closure.
  4. **Periodic report submission**: required sections, internal review and sign-off, submission record, internal-deadline ahead of regulator-deadline discipline.
  5. **Regulatory inquiry response**: receipt acknowledgement, internal triage, response sections, sign-off, submission, follow-up tracking.

### Changed

- [`TODO.md`](TODO.md): Priority 4.4 entry resolved; pointer to shipped template.
- [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md): version `1.1.10 -> 1.1.11`; §6 entry for "Regulator interaction templates" updated from `Partial / Planned / TODO P4.4` to `Substantive / In library / [link]`.
- [`README.md`](README.md): library version `2026.06.92 -> 2026.06.93`; README version `1.8.48 -> 1.8.49`.

### Scope decision

One consolidated document with five sub-templates rather than five separate documents, matching the project's existing template convention. Templates are shape-only; framework-specific timing, format, and channel requirements remain in the relevant jurisdiction annex or sector overlay (cross-references in the document).

### Verification

All 44 audit gates pass standalone.

---

## 2026-06-20, Library Version 2026.06.92, PR #106

TODO P4.3: implementation roadmap template. Third of five Priority 4 items.

Sequences the modules an adopter picks via the quickstart template into a three-phase Year-1 plan. Composition-aware (not per fixed profile), applying the same lesson as the P4.1 rewrite.

### Added

- [`docs/template-implementation-roadmap.md`](docs/template-implementation-roadmap.md): new Template document. Three phases:
  - **Phase 1, Floor** (Days 1 to 90 at E2 reference pace): reach the core-baseline defensible posture. Acceptance criteria: all six core-baseline artefacts customised, owners assigned, incident-response desk-check, initial maturity self-assessment.
  - **Phase 2, Operational** (Days 91 to 180): operationalise the artefacts. Review cadence stood up; first review wave completed; tabletop run; maturity self-assessment shows movement.
  - **Phase 3, Year-1 close** (Days 181 to 365): reach steady state. Measurement layer online; programme-level review; Year-1 retrospective published; Year-2 plan signed off.
- Capacity-tier pace adjustments: E1 founder part-time (extended pace), E2 light (reference), E3 standard (accelerated 60 / 120 / 365), E4 department (parallel 60 / 90 / 270).
- Composition-complexity pace adjustments: add 30 days per phase for compositions with 15 plus modules; 30 to 60 days in Phase 2 for heavy regulatory exposure or AI development.
- Recording template at the bottom; six review questions before committing to dates.

### Changed

- [`TODO.md`](TODO.md): Priority 4.3 entry resolved; pointer to shipped template.
- [`README.md`](README.md): library version `2026.06.91 -> 2026.06.92`; README version `1.8.47 -> 1.8.48`.

### Verification

All 44 audit gates pass standalone.

---

## 2026-06-20, Library Version 2026.06.91, PR #105

Heavy rewrite of [`docs/template-quickstart.md`](docs/template-quickstart.md). Maintainer's feedback on PR #103: the six fixed profiles (small business, mid-market regulated industry, multi-national enterprise, public-sector adopter, healthcare adopter, financial-services adopter) were too rigid; companies do not fit into the categories, and the same category contains very different operational realities.

### Changed

- [`docs/template-quickstart.md`](docs/template-quickstart.md): version `1.0.0 -> 2.0.0`. Replaces the per-profile structure with a core baseline plus five stacking dimensions. The new shape:
  - **Core baseline** (6 artefacts mandatory regardless of size or sector): foundational policy, three security policies, privacy policy plus home-jurisdiction annex, populated risk register.
  - **Dimension A, Activity** (6 modules: A1 custom internal development, A2 external-facing SaaS, A3 AI in operations, A4 AI model development or training, A5 critical-availability operations, A6 physical operations).
  - **Dimension B, Data scope** (6 modules: B1 customer personal data, B2 special-category, B3 children's data, B4 cross-border transfers, B5 PCI scope, B6 government or classified).
  - **Dimension C, Audience** (3 modules: C1 consumers, C2 businesses, C3 government).
  - **Dimension D, Regulatory exposure** (4 levels: D1 light, D2 sector-regulated, D3 multi-regulated, D4 heavy).
  - **Dimension E, GRC team capacity** (4 levels: E1 founder part-time, E2 light 1 to 2 people, E3 standard 3 to 10, E4 department). E scales the depth of every other adopted module.
  - **Three worked examples** showing composition: a mid-size SaaS with EU customers and AI features; a five-person consultancy; a regional bank.

- [`README.md`](README.md): library version `2026.06.90 -> 2026.06.91`; README version `1.8.46 -> 1.8.47`.

### Scope decision

Major version bump (2.0.0) because the structural model changed (per-profile to compositional). The filename is preserved despite the title change to keep the PR #103 CHANGELOG entry's references intact and to avoid an audit cascade.

### Verification

All 44 audit gates pass standalone. The filename-title alignment audit (gate 7) tolerates "Adopter Quickstart Template" titled with the existing filename [`docs/template-quickstart.md`](docs/template-quickstart.md) because "quickstart" appears in both.

---

## 2026-06-20, Library Version 2026.06.90, PR #104

TODO Priority 4.2: adopter maturity self-assessment template. Second of five Priority 4 items in sequence.

Distinct from the existing [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md) (which rates each library document's stability); the new template rates the adopter's own programme maturity across 11 library domains, using a five-tier ladder modelled on NIST CSF Tiers and CMMI.

### Added

- [`docs/template-maturity-self-assessment.md`](docs/template-maturity-self-assessment.md): new Template document. Eleven domain sections (Governance, Risk, Compliance, Privacy, Security, Operations, Resilience, Supply chain, Architecture, DevSecOps, AI). Each domain has 5 to 8 yes/no/partial-style statements; per-statement scoring on a 1 to 5 maturity ladder; per-domain score via median; overall score via median of domains. Per-tier next-step guidance (Initial through Optimising). Recording-the-assessment template at the bottom. Five review questions for the assessor.

### Changed

- [`TODO.md`](TODO.md): Priority 4.2 entry resolved; pointer to shipped template.
- [`README.md`](README.md): library version `2026.06.89 -> 2026.06.90`; README version `1.8.45 -> 1.8.46`.

### Scope decision

Format choice: guided markdown checklist (per TODO entry "spreadsheet or guided markdown checklist"). Markdown was chosen over spreadsheet for stdlib-only-tooling consistency and so adopters can fork the template into their own corpus with `git`. Tier ladder choice: five tiers matching NIST CSF / CMMI conventions, named Initial / Developing / Defined / Managed / Optimising. Scoring choice: median (not mean) per domain, to avoid single-outlier distortions in either direction.

### Verification

All 44 audit gates pass standalone.

---

## 2026-06-20, Library Version 2026.06.89, PR #103

TODO Priority 4.1: adopter quickstart template per profile. First of five Priority 4 items the maintainer authorised in sequence.

### Added

- [`docs/template-quickstart.md`](docs/template-quickstart.md): new Template document. Six profile sections (small business, mid-market regulated industry, multi-national enterprise, public-sector adopter, healthcare adopter, financial-services adopter), each with Day-1/30/90 adoption guidance, sector-conditional content notes, and realistic timeline expectations. Six review questions for applying any profile.

### Changed

- [`TODO.md`](TODO.md): Priority 4.1 entry resolved; replaced "Debating the value of" framing with a pointer to the shipped template.
- [`README.md`](README.md): library version `2026.06.88 -> 2026.06.89`; README version `1.8.44 -> 1.8.45`.

### Scope decision

Default to one consolidated template with multiple profile sections rather than six separate per-profile documents, matching the project's existing template convention (e.g. [`ai/template-ai-system-register.md`](ai/template-ai-system-register.md)). Profile-shape interactions section notes how to combine profiles for hybrid organisations.

### Verification

All 44 audit gates pass standalone.

---

## 2026-06-20, Library Version 2026.06.88, PR #102

Register-to-TODO alignment for [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md) §6 (Document-type capability gaps). The register-vs-TODO diff (per the maintainer's "complete everything that isn't yet logged in TODO" instruction) found three drift items in §6; all are resolved here by lightweight bookkeeping updates rather than substantive document creation.

### Changed

- [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md): version `1.1.9 -> 1.1.10`. Three §6 row updates: (1) `Decision-tree adopter navigator` was listed as `None / Planned / TODO P3.2 (Phase 21.8)`; the document was shipped as [`docs/decision-tree.md`](docs/decision-tree.md) but the register entry was never refreshed. Updated to `Substantive / In library / [link to docs/decision-tree.md]`. (2) `Regulator interaction templates` row updated to `Partial / Planned / TODO P4.4`. (3) `Audit evidence package templates` row updated to `Partial / Planned / TODO P4.5`.
- [`TODO.md`](TODO.md): two new Priority 4 entries added. **4.4 Regulator interaction templates** (consolidated templates for breach notification, attestation submission, examination support, periodic report submission, regulatory inquiry response; surfaced from register §6). **4.5 Audit evidence package templates** (per-control evidence packaging template; surfaced from register §6). Both are content additions; the maintainer's roadmap will sequence them with the existing Priority 4 items.
- [`README.md`](README.md): library version `2026.06.87 -> 2026.06.88`; README version `1.8.43 -> 1.8.44`.

### Scope decision

The maintainer chose the lightweight interpretation: log the deferred items in TODO and fix the stale register entry, without substantive document creation. The actual templates (regulator interaction, audit evidence packaging) are deferred to the maintainer's Priority 4 sequencing.

### Verification

All 44 audit gates pass standalone. Register entries cite the canonical source documents and TODO entries; no broken references.

---

## 2026-06-20, Library Version 2026.06.87, PR #101

Refresh the `Cross-document numerical coherence shipped as scaffold` entry in [`TODO.md`](TODO.md)'s Decisions log. The prior text described the linter as tracking "0 terms" and the framework as "in place for future term curation"; that description is stale relative to the implementation. The scaffold has been progressively widened since the decision was logged: Phase 23.26 added P1/P2/P3 acknowledgement-time patterns as scaffolding, Phase 23.35 added the GDPR breach-notification-hours pattern after empirical confirmation. The current scaffold tracks four terms; the [`tools/lint-cross-doc-numbers.py`](tools/lint-cross-doc-numbers.py) docstring documents why each candidate (RTO, RPO, retention, P4, NIS 2, DORA) was considered and excluded with rationale.

This is a documentation refresh, no behavioural change. The actionable claim a previous status summary made about "open authorial decisions" overstated the residual; investigation confirmed the term-curation decision space is substantively closed. The TODO entry now reflects current state so a future reader does not infer an actionable backlog item that does not exist.

### Changed

- [`TODO.md`](TODO.md): Decisions log entry refreshed; framework progression described; pointer to the `TERM_PATTERNS` dict in [`tools/lint-cross-doc-numbers.py`](tools/lint-cross-doc-numbers.py) for the live set.
- [`README.md`](README.md): library version `2026.06.86 -> 2026.06.87`; README version `1.8.42 -> 1.8.43`.

### Verification

All 44 audit gates pass standalone. No code change to the linter; the only edit is prose in [`TODO.md`](TODO.md). The CHANGELOG entry is required by the D1 delta gate even for documentation-only changes that touch corpus content.

---

## 2026-06-20, Library Version 2026.06.86, PR #100

**Closes the three-item queued-session backlog**: new audit gate 44 (paired-skill step-parity audit), third and last of the items announced in the maintainer's status summary (after PR #98 PF-04 stale-version-literal scanner extension and PR #99 gate 43 follow-up ageing audit). Mechanises the cross-document term-and-identifier consistency check the validation-sweep history register flagged as a recurring gap.

**Gate behaviour**: for each pair in `PAIRS` (currently one: [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) paired with [`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md)), extracts step identifiers from both files and fails on symmetric-difference mismatch. Motivated by the Sweep 3 finding: PR #78 introduced the pre-flight scanner as `### 3.5.` in the SKILL heading and as `3a.` in the slash-command numbered list. Subagent A's semantic triage caught the drift; this gate catches it mechanically going forward.

### Scope decision

Currently only the validation-sweep skill has a paired slash-command counterpart. The maintainer authorised shipping the gate despite the single-pair scope so the discipline is in place for future skills that adopt the slash-command pattern. `PAIRS` is the extension point; adding a new entry inherits the check.

### Added

- [`tools/lint-paired-skill-step-parity.py`](tools/lint-paired-skill-step-parity.py): new audit gate. Stdlib-only Python 3.11. Extracts SKILL.md step identifiers from `### N. ` / `### N<suffix>. ` headings and slash-command identifiers from both numbered list items (`N. **Title**:`) and prose mentions (`Step N`). Compares by symmetric difference.
- [`tests/test_linters.py`](tests/test_linters.py) class `PairedSkillStepParityTests`: three regression tests (corpus-clean smoke, drift-detection positive, matching-pair negative).

### Changed

- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md): version `1.11.0 -> 1.12.0`; §6 inventory adds row 44; §5 category 5 ("Programme and index integrity") gains gate 44 with rationale referencing the Sweep 3 finding; the two prose references to "43 audit gates" / "43-gate corpus inventory" updated to 44.
- [`.github/workflows/quality.yml`](.github/workflows/quality.yml): new step "Paired-skill step-parity audit" between gate 43 and the PR-only delta gates.
- [`tools/run_all_audits.sh`](tools/run_all_audits.sh): new `run_gate` invocation; header comment updated to 44.
- [`.pre-commit-config.yaml`](.pre-commit-config.yaml): new hook `lint-paired-skill-step-parity`.
- [`governance/procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md), [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md), [`governance/register-main-branch-protection.md`](governance/register-main-branch-protection.md), [`tools/README.md`](tools/README.md), [`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py), [`tools/check-version-bump-on-pr.py`](tools/check-version-bump-on-pr.py), [`tools/lint-audit-gate-parity.py`](tools/lint-audit-gate-parity.py): 11 prose references to "43 gates" / "43-gate" updated to 44 (caught by gate 39).
- Per-document version bumps on the three touched governance files: procedure-library-quality-and-review-cadence `1.0.10 -> 1.0.11`, register-document-index-and-classification `1.27.17 -> 1.27.18`, register-main-branch-protection `1.0.10 -> 1.0.11`.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.26.15 -> 1.26.16`.
- [`README.md`](README.md): library version `2026.06.85 -> 2026.06.86`; README version `1.8.41 -> 1.8.42`.

### Three-item queued backlog: closed

All three items from the post-late-research-findings-queue status summary have shipped:
- PR #98 PF-04 stale-version-literal scanner extension (with sweep-narrative heuristics)
- PR #99 gate 43 follow-up ageing audit
- PR #100 gate 44 paired-skill step-parity audit (this PR)

The validation-sweep history register's residual cross-document term-and-identifier consistency gap is now closed for paired skill+slash-command surfaces. Other potential consistency gaps (cross-document identifier references outside the paired-skill structure) remain semantic-triage territory.

### Verification

All 44 audit gates pass standalone. Gate 35 (parity audit) confirms identical wiring across all four parity surfaces. Gate 39 (gate-count consistency) confirms no stale "43" references remain. The three regression tests in `PairedSkillStepParityTests` pass (`python3 -m unittest tests.test_linters.PairedSkillStepParityTests`); the drift-detection test confirms `### 3.5.` vs `3a.` produces non-equal sets (the Sweep 3 shape).

---

## 2026-06-20, Library Version 2026.06.85, PR #99

New audit gate 43: follow-up ageing audit. Mechanises Rule 3 of the maintenance-tag dating discipline introduced in PR #90 (the convention shipped without a mechanical gate; this PR adds it). Second of three queued session items.

The gate scans [`governance/register-sweep-history.md`](governance/register-sweep-history.md) for blocks containing a `surfaced: YYYY-MM-DD` field, derives the deadline as `re-triage-by` (explicit) or `surfaced + 30 days` (default), and fails the build when `today() > deadline` with no `re-triaged: YYYY-MM-DD` line at or after the deadline in the same block. Exit codes: 0 (no expired follow-ups), 1 (at least one expired), 2 (invalid date value in a tracked field). The linter supports `--target`, `--today`, and `--root` flags for testability.

### Added

- [`tools/lint-followup-ageing.py`](tools/lint-followup-ageing.py): new audit gate. Stdlib-only Python 3.11. Scans [`governance/register-sweep-history.md`](governance/register-sweep-history.md) by default; the `TARGET_FILES` list is extensible for future registers adopting the convention.
- [`tests/test_linters.py`](tests/test_linters.py) class `FollowupAgeingTests`: four regression tests covering the corpus-clean-at-HEAD smoke test, the expired-follow-up positive test, the fresh-re-triaged-trailer negative test, and the invalid-date-value exit-2 environmental test.

### Changed

- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md): version `1.10.0 -> 1.11.0`; §6 inventory adds row 43; §5 category 7 ("Freshness and lifecycle") gains gate 43 with rationale; the two prose references to "42 audit gates" / "42-gate corpus inventory" updated to 43.
- [`.github/workflows/quality.yml`](.github/workflows/quality.yml): new step "Follow-up ageing audit" between gate 42 and the PR-only delta gates.
- [`tools/run_all_audits.sh`](tools/run_all_audits.sh): new `run_gate` invocation; header comment "current sweep is 42 gates" updated to 43.
- [`.pre-commit-config.yaml`](.pre-commit-config.yaml): new hook `lint-followup-ageing`.
- [`governance/procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md), [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md), [`governance/register-main-branch-protection.md`](governance/register-main-branch-protection.md), [`tools/README.md`](tools/README.md), [`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py), [`tools/check-version-bump-on-pr.py`](tools/check-version-bump-on-pr.py), [`tools/lint-audit-gate-parity.py`](tools/lint-audit-gate-parity.py): 11 prose references to "42 gates" / "42-gate" updated to 43 (caught by gate 39, the cross-file gate-count consistency audit).
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.26.14 -> 1.26.15`.
- [`README.md`](README.md): library version `2026.06.84 -> 2026.06.85`; README version `1.8.40 -> 1.8.41`.

### Verification

All 43 audit gates pass standalone. Gate 35 (gate-name parity) confirms the new gate is wired identically across all four parity surfaces (spec §6, quality.yml, run_all_audits.sh, pre-commit). Gate 39 (cross-file gate-count consistency) confirms no prose claim about "42 gates" remains. The four regression tests in `FollowupAgeingTests` pass (`python3 -m unittest tests.test_linters.FollowupAgeingTests`); manual verification confirms exit 0 on the corpus, exit 1 on an expired fixture, exit 0 on a fixture with a fresh re-triaged trailer, and exit 2 on an invalid date value.

---

## 2026-06-20, Library Version 2026.06.84, PR #98

Pre-flight scanner pattern set extended. Adds **PF-04 stale-version-literal**: catches phrases like "currently 1.22.0" / "the current 1.22.0" / "now at 1.22.0" / "now on 1.22.0" where the captured version does not match any of the canonical library, README, pack, or spec versions. Motivated by the Sweep 4 finding in `docs/adopter-guide.md:57` ("ships with its own version sequence (currently `1.22.0`)"); the new pattern would have caught that finding mechanically rather than requiring semantic triage. First of the three queued session items announced in the maintainer's status summary.

Two additional heuristics added to keep the scanner quiet on the existing corpus: extended HISTORICAL_KEYWORDS (`false positive`, `false-positive`, `in-window`, `out-of-window`) and new SWEEP_NARRATIVE_PATTERNS regex set (`Sweep N`, `Subagent A/B/C`, `recurring-class`). These suppress the register-sweep-history narrative that quotes past findings, including stale-version-literal false positives in PF-04's surface (the register narrates past findings extensively).

### Changed

- [`tools/sweep-preflight-scanner.py`](tools/sweep-preflight-scanner.py): new `CANONICAL_VERSIONS` registry (library, README, pack, spec versions read from metadata-block fields); new `read_canonical_version` helper; new `VERSION_LITERAL_RE` regex matching "currently/the current/now at/now on" plus version-shape; new `scan_version_literals` scanner function; main wires PF-04 into the candidate stream alongside PF-01/02/03; expanded `HISTORICAL_KEYWORDS` plus new `SWEEP_NARRATIVE_PATTERNS` regex tuple; new H6 heuristic in `is_exempt_by_heuristic` applies the regex patterns.
- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): step 3a expanded to document PF-04 and the two new heuristic surfaces; the existing pattern set description updated to include `false positive` / `in-window` / `out-of-window` and the sweep-narrative regex group.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.26.13 -> 1.26.14`.
- [`README.md`](README.md): library version `2026.06.83 -> 2026.06.84`; README version `1.8.39 -> 1.8.40`.

### Verification

Full audit programme passes standalone, all 42 corpus gates pass. Scanner: 22 candidates suppressed (16 by heuristic, 6 by exemption file), 0 findings reported against the current corpus. Manual verification confirms PF-04 would surface the canonical Sweep 4 finding (the "currently `1.22.0`" line) if re-introduced; the heuristic skips do not apply to that line (no historical-narrative keywords, no sweep-narrative regex match).

---

## 2026-06-20, Library Version 2026.06.83, PR #97

Validation-sweep maintenance-protocol change plus retroactive CHANGELOG prune. Maintainer observed that zero-finding sweeps were producing standalone PRs with full CHANGELOG entries that contained no user-visible content, distracting from substantive entries. The convention is revised: **zero-finding sweeps leave no trace** (no register entry, no CHANGELOG entry, no standalone PR; the convergence-delta trend lives in the iteration counter, not in a per-sweep record).

### Changed

- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): step 8 ("Append to the sweep history register") retitled to "(only when the sweep produced findings)" and a new paragraph makes the zero-finding-leaves-no-trace convention explicit. Replaces the older "may be recorded as a single line under a trivial-sweeps sub-section, otherwise omitted" optional framing with a definitive convention.
- [`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md): step 8 brief expanded with the same explicit convention.
- [`governance/register-sweep-history.md`](governance/register-sweep-history.md): version `1.9.0 -> 1.10.0`; Maintenance protocol's first bullet updated to make the convention explicit (zero-finding sweeps leave no register or CHANGELOG entry); existing zero-finding-sweep entries for Sweeps 5-8 are preserved as historical record but the convention applies forward.
- [`README.md`](README.md): library version `2026.06.82 -> 2026.06.83`; README version `1.8.38 -> 1.8.39`.

### Removed

Six retroactively-pruned CHANGELOG entries for housekeeping-only sweep PRs that contained no user-visible content:

- PR #81 (library 2026.06.67): Sweep 3 register entry
- PR #84 (library 2026.06.70): Sweep 4 register entry
- PR #87 (library 2026.06.73): Sweep 5 register entry
- PR #89 (library 2026.06.75): Sweep 6 closure (also added one exemption-file entry; preserved in git history)
- PR #92 (library 2026.06.78): Sweep 7 register entry
- PR #95 (library 2026.06.81): Sweep 8 closure (also added one exemption-file entry; preserved in git history)

These PRs are still in git history; only their CHANGELOG entries are pruned. The register entries for the same sweeps remain as historical record (the register is the cumulative audit trail; the CHANGELOG is user-visible). Library version numbers 2026.06.67, 2026.06.70, 2026.06.73, 2026.06.75, 2026.06.78, and 2026.06.81 are now versions for which the only change was a housekeeping register update; future readers asking "what was 2026.06.71?" find a brief mention here rather than a full entry.

### Verification

Full audit programme passes standalone, all 42 corpus gates pass. The version-monotonicity audit operates on per-document `Version:` metadata fields (not on CHANGELOG), so pruning CHANGELOG entries does not affect any audit. The CHANGELOG-on-PR delta gate operates on PR diffs (not on historical state), so the prune does not interact with future PR enforcement. Keep a Changelog convention is "do not rewrite history" by default; the maintainer explicitly authorised this exception under the named-alternatives clarification protocol.

---

## 2026-06-20, Library Version 2026.06.82, PR #96

Validation-sweep enhancement, seventh and last from the late-research-findings queue. **Closes the queue.** Adds the hold-the-line ratcheting-baseline discipline to step 6 (Triage) of the SKILL: fingerprint-not-count, expiry plus rationale, net-negative invariant on sweep close. This is the "largest" tier (after the smallest four: synthesis rubric, pre-tool verification, maintenance-tag dating, convergence-delta; and the medium two: multi-agent debate, SARIF-lite).

Research basis: ESLint Bulk Suppressions (`--suppress-all` + `--prune-suppressions`; only `error`-level, no `warn` suppression; per-location not per-file); Notion's `eslint-seatbelt` ratcheting database; basedmypy / mypy-baseline "untyped surface can only shrink"; TypeScript strict-null allowlist (VS Code team); Stryker mutation-test baseline. Recreated as CC BY-SA 4.0 in-house prose; no external tooling imported.

### Scope decision

Three rules added to SKILL step 6 (Rules 6.1, 6.2, 6.3). The existing exemption file [`tools/sweep-preflight-exemptions.json`](tools/sweep-preflight-exemptions.json) and the register's `false-positive memory` section are now the two-surface accept-list the new rules govern. The exemption file's 7 pre-existing entries are grandfathered (no `accepted_on`/`expires` retro-stamping); they pick up the new fields when next touched. The register's false-positive memory section is restructured to document the convention and accept new fingerprint-shaped entries.

### Changed

- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): new "Ratcheting-baseline discipline for dismissed findings" subsection in step 6. Rule 6.1 fingerprint-not-count (keyed on `(file_path, normalised_section_or_artefact, claim_type)` plus SARIF-lite `ruleId`); Rule 6.2 expiry plus rationale (default 90 days, re-triage on expiry, no auto-renew); Rule 6.3 net-negative invariant on close (`|accept-list|` cannot grow net of fixes; sweep must add OR fix, not both freely). Cross-references the pre-flight exemption file and the register's false-positive memory section as the two-surface accept-list both rules govern.
- [`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md): step 6 expanded to reference the three ratcheting-baseline rules.
- [`governance/register-sweep-history.md`](governance/register-sweep-history.md): version `1.8.0 -> 1.9.0`; false-positive memory section restructured to document the Rules 6.1-6.3 convention, the relationship to the pre-flight exemption file, and the grandfathering of pre-existing entries. Empty entries list preserved.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.26.11 -> 1.26.12`.
- [`README.md`](README.md): library version `2026.06.81 -> 2026.06.82`; README version `1.8.37 -> 1.8.38`.

### Late-research-findings queue: closed

All seven late-research-findings queue items have shipped: PR #82 (synthesis rubric), #88 (pre-tool verification), #90 (maintenance-tag dating), #91 (convergence-delta termination), #93 (multi-agent debate Rule 5.5), #94 (SARIF-lite output), and this PR (hold-the-line ratcheting baselines). Combined with the upstream noise-reduction PR #86 (scanner heuristics + exemption file), the validation-sweep discipline is now end-to-end principled: scanner noise reduction, evidence-grounded subagent reports with SARIF-lite output, pre-tool verification, four-rule synthesis rubric plus debate, in/out-of-window triage, ratcheting accept-list with expiry, principled convergence-delta termination.

### Verification

Full audit programme passes standalone, all 42 corpus gates pass. The discipline ships as workflow prose; no new mechanical gate added. Sweep 9 will be the first to formally apply Rules 6.1-6.3 as a dismissal protocol if any finding is surfaced for dismissal.

---

## 2026-06-20, Library Version 2026.06.80, PR #94

Validation-sweep enhancement, sixth of seven from the late-research-findings queue. Adds the SARIF-lite output format to step 4 of the SKILL: each subagent finding is a fenced markdown block with six labelled lines (tool / ruleId / level / location / fingerprint / rubric) plus an evidence paragraph. Closes the "medium" tier of the queue (after Rule 5.5 multi-agent debate in PR #93); only the "largest" tier (hold-the-line ratcheting baselines) remains.

Research basis: SARIF v2.1.0 specification minimum-viable result structure (required field is only `message`, but `ruleId` + `level` + `locations[].physicalLocation` are the de-facto minimum); Microsoft SARIF tutorials canonical example; GitHub Code Scanning surfaced field set; Semgrep `partialFingerprints.primaryLocationLineHash` shape; parsiya.net "AI-Native SARIF" extension pattern using `properties` bag for AI-specific metadata. Recreated as CC BY-SA 4.0 in-house prose, no SARIF parser added.

### Scope decision

The research explicitly recommended "no parser" — the value is in the field shape, not wire-format compliance. The block format is markdown-friendly, grep-able, and uniform across subagents; the parent does dedupe via string-match on the deterministic fingerprint rather than semantic comparison.

### Changed

- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): step 4 expanded with the "SARIF-lite output format" subsection. Six-line block per finding, three rules (one block per finding, deterministic fingerprint, closed severity enum), anti-rubric warnings against JSON-in-prose, full-SARIF-envelope, and multiple fingerprint algorithms.
- [`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md): step 4 brief expanded to reference the SARIF-lite block format and the fingerprint scheme.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.26.10 -> 1.26.11`.
- [`README.md`](README.md): library version `2026.06.79 -> 2026.06.80`; README version `1.8.35 -> 1.8.36`.

### Verification

Full audit programme passes standalone, all 42 corpus gates pass. The format is workflow prose; no new mechanical gate added. The next sweep with non-zero findings will be the first to exercise the SARIF-lite shape end-to-end.

---

## 2026-06-20, Library Version 2026.06.79, PR #93

Validation-sweep enhancement, fifth of seven from the late-research-findings queue. Adds Rule 5.5 to the synthesis rubric: single-round asymmetric debate for high-divergence disagreement between subagents. First of the "medium" tier (after the smaller-scope patterns 1-4).

Research basis: Du et al. multi-agent debate (arXiv:2305.14325, 2 rounds + 3 agents captures most lift); Liang et al. MAD asymmetric "affirmative + negative + judge" debate (arXiv:2305.19118); "Debate or Vote" budget-aligned comparison (arXiv:2508.17536, debate 87.91% vs vote 86.69% vs single 85.68%); MAD survey on round-3+ accuracy degradation (arXiv:2506.00066); AutoGen GroupChat patterns. Recreated as CC BY-SA 4.0 in-house prose.

### Scope decision

The research recommended narrow trigger and minimal protocol. This PR's Rule 5.5 fires only on (a) severity divergence wider than one level (`must-fix-before-merge` vs `track-as-follow-up`) or (b) real-vs-false-positive disagreement on the same dedupe-key. Adjacent severity disagreements (e.g. `should-fix-this-PR` vs `track-as-follow-up`) keep the existing Rule 5.3 "pick higher, record raw" protocol; the accuracy lift from debate does not justify the cost on adjacent cases. Single round only (Du et al. + the MAD survey both show diminishing returns after round 2; round 3+ can degrade accuracy). Parent as judge (no third "judge" subagent needed for a label-pick task).

### Changed

- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): new Rule 5.5 inserted in the synthesis rubric: "debate when divergence is large, not when adjacent". Trigger conditions, one-round protocol (each disagreeing subagent sees the other's claim + reasoning, updates or holds with rebuttal), parent adjudication, persisted-disagreement flagging (`debated: divergence-persisted` on the synthesised row). Rule 5.3 unchanged; it still handles adjacent disagreements.
- [`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md): step 5 expanded from four-rule to five-rule rubric summary.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.26.9 -> 1.26.10`.
- [`README.md`](README.md): library version `2026.06.78 -> 2026.06.79`; README version `1.8.34 -> 1.8.35`.

### Verification

Full audit programme passes standalone, all 42 corpus gates pass. The rubric is workflow prose; no new mechanical gate added. Rule 5.5 fires rarely (Sweeps 1-7 surfaced zero >1-level divergences; the rule is precision-tuned to avoid invoking debate on routine adjacent disagreements). When it does fire, the cost is one extra subagent round-trip per disagreeing finding.

---

## 2026-06-20, Library Version 2026.06.77, PR #91

Validation-sweep enhancement, fourth of seven from the late-research-findings queue. Replaces the fixed 3-iteration cap in step 7 with a principled three-condition termination: empty-delta primary stop, patience-plateau secondary stop, and a 6-iteration hard ceiling as runaway guard. Closes the last of the "smallest" tier in the queue (synthesis rubric, pre-tool verification, maintenance-tag dating, convergence-delta).

Research basis: ESLint's `Linter.verifyAndFix` and RuboCop's autocorrect pattern (empty-delta + cycle detector); numerical-solver dual stopping criterion (residual-tolerance OR max-iterations); ML training early-stopping with patience (TensorFlow EarlyStopping, scikit-learn patience parameter); dataflow analysis least-fixed-point iteration (Aarhus SPA lattice theory). Recreated as CC BY-SA 4.0 in-house prose.

### Changed

- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): step 7 termination expanded from a fixed 3-iteration cap to a three-condition stop: (1) empty-delta primary (zero new High/Medium findings AND identical synthesised finding-set by dedupe-key, fixed-point reached), (2) patience-plateau secondary (2 consecutive iterations with no strict shrinkage, surface residual to operator), (3) hard ceiling 6 iterations as runaway guard signalling defect (cycle or scope creep) not completion. The empty-delta is the principled stop; the hard ceiling is the sanity guard; the patience-plateau handles cases neither extreme catches.
- [`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md): step 7 Cap line replaced with the three-condition summary.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.26.8 -> 1.26.9`.
- [`README.md`](README.md): library version `2026.06.76 -> 2026.06.77`; README version `1.8.32 -> 1.8.33`.

### Verification

Full audit programme passes standalone, all 42 corpus gates pass. The convergence-trend evidence from Sweeps 1-6 (4+, 3, 1, 1, 0, 0) is consistent with the empty-delta as the typical exit; the new termination conditions formalise what was already happening in practice.

---

## 2026-06-20, Library Version 2026.06.76, PR #90

Validation-sweep enhancement, third of seven from the late-research-findings queue. Adds the Wikipedia-style maintenance-tag dating convention to the sweep-history register's Maintenance protocol, closing the gap where deferred findings accumulated without ageing signal.

Research basis: Wikipedia `{{citation needed|date=Month YYYY}}` maintenance-template convention; GitHub `actions/stale` and `probot/stale` 30-day default; Self-Admitted Technical Debt (SATD) issue-tracker dating (Bavota and Russo, arXiv:2007.01568); Wu et al. "What Makes a Good TODO Comment?" (arXiv:2503.15277); ISO 8601 audit-trail encoding. Recreated as CC BY-SA 4.0 in-house prose.

### Scope decision

The research recommended three rules: (1) the `surfaced:` field, (2) the `re-triage-by:` field with a 30-day default, (3) a future linter that fails when a deferred entry's deadline passes without re-triage. This PR ships rules 1 and 2 (the convention, low scope) and queues rule 3 (the mechanical gate, medium scope) as an "extending the framework" task. Convention applies to findings deferred from Sweep 7 onwards; existing deferred findings (Sweep 3 cross-document consistency, Sweep 4 classification-convention) are not retro-stamped.

### Changed

- [`governance/register-sweep-history.md`](governance/register-sweep-history.md): version `1.5.0 -> 1.6.0`; new "Dating discipline for deferred findings" subsection under Maintenance protocol documents the `surfaced: YYYY-MM-DD` and `re-triage-by: YYYY-MM-DD` (default surfaced+30 days) fields plus the queued mechanical gate.
- [`README.md`](README.md): library version `2026.06.75 -> 2026.06.76`; README version `1.8.31 -> 1.8.32`.

### Verification

Full audit programme passes standalone, all 42 corpus gates pass. The convention is workflow prose; no new mechanical gate is added in this PR.

---

## 2026-06-20, Library Version 2026.06.74, PR #88

Validation-sweep enhancement, second of seven from the late-research-findings queue. Adds a pre-tool verification preamble to the subagent fan-out discipline in step 4 of the validation-sweep skill. Closes the gap where subagents could make redundant or misdirected tool calls without an auditable justification trace.

Research basis: POPPER (Stanford/Harvard 2025) falsification-experiment design pattern; AnyTool (arXiv 2402.04253) self-reflection-before-call gate; AgentDiet (arXiv 2509.23586) trajectory-reduction dedup; LangGraph pre-hook validation node pattern; Claude Code community "triage-before-action" skill family. Recreated as in-house CC BY-SA 4.0 prose rather than imported.

### Changed

- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): step 4 expanded with a new "Pre-tool verification discipline" paragraph. Each subagent brief now carries a falsification-preamble rule: before each tool call, the subagent states (a) the hypothesis the call tests, (b) the observation that would falsify it, and (c) one prior tool result that does not already answer the question. Undefined falsifier means the call is corroboration-seeking (skip or reframe); duplicate-of-prior-result means do not re-call (cite prior result in finding). The rule composes Popper-style falsification with AnyTool's redundancy gate and AgentDiet's dedup check; it produces an auditable justification trace and filters corroboration-only calls at the source.
- [`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md): step 4 brief expanded to reference the pre-tool verification preamble (one-sentence summary; the SKILL holds the full text).
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.26.7 -> 1.26.8`.
- [`README.md`](README.md): library version `2026.06.73 -> 2026.06.74`; README version `1.8.29 -> 1.8.30`.

### Verification

Full audit programme passes standalone, all 42 corpus gates pass. The discipline is workflow prose; no new mechanical gate is added. The next sweep (Sweep 6, triggered by the third PR after Sweep 5: this PR is the third) will be the first to apply the preamble.

---

## 2026-06-20, Library Version 2026.06.72, PR #86

Validation-sweep pre-flight scanner: noise-reduction enhancement. Across Sweeps 3, 4, and 5, the same 12-13 candidate findings re-surfaced on every run and were re-triaged as false positives every time. The maintainer asked: should the scanner be enhanced so it does not keep tagging the same shapes? Chose option 3 of the named alternatives: both heuristics and an exemption file.

### Added

- [`tools/sweep-preflight-exemptions.json`](tools/sweep-preflight-exemptions.json): exemption file in JSON format (stdlib-friendly; project is stdlib-only). Each entry suppresses one `(path, pattern_id, line_hash)` candidate. `line_hash` is the 16-char prefix of SHA-256 of the stripped line content; stable under line-number drift but auto-invalidates when the line text changes (which forces a re-triage). Initial population covers 5 unique false positives: addyosmani external vet count, addyosmani description in setup-generator-prompt, the synthesis rubric's "Four rules, no ceremony" sub-rule mention, and two `promptmap2` external-project rule-count references in the AI security tooling landscape register.

### Changed

- [`tools/sweep-preflight-scanner.py`](tools/sweep-preflight-scanner.py): added two layers of noise reduction. **Layer 1, in-scanner heuristics** (catches 8 of the 13 known false positives): skip matches preceded by section-like words (`Section N`, `Article N`, `Phase N`, `Chapter N`, `Step N`), hyphenated compounds (`under-14 rules`), legal bill prefixes (`AB 1394`), year-with-title-cased-legal-noun (`The 2025 Rules`), markdown version-history table rows (rows with both a version-shape and a date-shape), and lines containing historical-narrative keywords (`completed at`, `now ships`, `previously`, `past`, `originally`, `historically`, `earlier`, `before gate`). **Layer 2, exemption file** (catches the remaining 5 unique cases). Output line now reports suppression counts so the maintainer can see the scanner is doing its job. New trailing prompt explains how to add an exemption-file entry for a new false positive.
- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): step 3a expanded to document the two-layer noise-reduction mechanism (heuristics plus exemption file), including the SHA-256-of-line-content key design rationale.
- [`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md): step 3a brief expanded to reference the heuristics and exemption file.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.26.6 -> 1.26.7`.
- [`README.md`](README.md): library version `2026.06.71 -> 2026.06.72`; README version `1.8.27 -> 1.8.28`.

### Verification

Full audit programme passes standalone, all 42 corpus gates pass. Scanner output verified: before this PR, 12 candidates surfaced on every sweep; after this PR, 0 candidates surface on the same corpus. The suppression-count breakdown (`8 by heuristic, 5 by exemption file`) lets the maintainer see at a glance that the scanner is filtering noise rather than failing silently. When the corpus accumulates a genuinely new stale-count finding, the scanner will surface it (the suppressions are precision-tuned, not catch-all).

---

## 2026-06-20, Library Version 2026.06.71, PR #85

Closes the Sweep 4 out-of-window classification-convention follow-up. The maintainer's decision (asked-and-answered, option "both, with primary tag"): a finding may carry more than one failure-mode class; one is tagged primary (the dominant mechanism) and one or more may be tagged secondary (the symptom shape). Historical entries from Sweeps 1-3 are not retro-applied; the convention applies from Sweep 5 onwards.

### Changed

- [`governance/register-sweep-history.md`](governance/register-sweep-history.md): version `1.2.0 -> 1.3.0`; new "Classification convention: primary plus optional secondary" subsection added under the failure-mode-classes table, documenting the four-rule convention. Recurring-class summary table re-labelled to show primary-class counts as the main signal; secondary-class participation footnote added (empty until Sweep 5 populates it). "Classification-convention follow-up" row removed from the recurring-class table because the convention is now documented; the Sweep 4 entry's follow-up note is preserved as historical record of how the question reached the maintainer.
- [`README.md`](README.md): library version `2026.06.70 -> 2026.06.71`; README version `1.8.26 -> 1.8.27`.

### Verification

Full audit programme passes standalone, all 42 corpus gates pass. The classification convention is now documented in the register; sweep entries from this PR forward can use the `primary [+ secondary]` shape.

---

## 2026-06-20, Library Version 2026.06.69, PR #83

Validation Sweep 4 in-window finding (C1 stale-prose): the adopter-guide's Mode C section says the pack "ships with its own version sequence (currently `1.22.0`)" but the pack is at 1.26.6. Surfaced by Subagent B of the Sweep 4 fan-out; the new synthesis rubric tagged this `R` (read-verified), severity `should-fix-this-PR`. Fix uses number-stable wording rather than bumping the literal so the same drift does not recur on the next pack bump.

### Changed

- [`docs/adopter-guide.md`](docs/adopter-guide.md): Mode C section, "ships with its own version sequence (currently `1.22.0`)" replaced with number-stable wording ("independent of the library's; see the pack README header for the current value"). Document version `1.1.0 -> 1.1.1`.
- [`README.md`](README.md): library version `2026.06.68 -> 2026.06.69`; README version `1.8.24 -> 1.8.25`.

### Verification

Full audit programme passes standalone, all 42 corpus gates pass. The Sweep 4 synthesis using the new four-rule rubric is the first sweep to apply the rubric in practice; the `R` evidence tag forced Subagent B to quote `docs/adopter-guide.md:57` directly rather than inferring the staleness, and the three-level severity scale collapsed cleanly onto `should-fix-this-PR`.

---

## 2026-06-20, Library Version 2026.06.68, PR #82

Validation-sweep enhancement, first of seven from the late-research-findings queue. Adds a deterministic four-rule synthesis rubric to step 5 of the validation-sweep skill. Closes the prior gap where the parent's synthesis after subagent fan-out was ad-hoc and unreproducible across sweeps.

Research basis: SARIF v2.1.0 fingerprint-based dedupe pattern; Google `eng-practices` severity-label discipline; Cochrane / GRADE two-raters-plus-adjudicator from systematic-review methodology; Cohen's-kappa-paradox literature on why N=3 inter-rater statistics are uninterpretable. Recreated in-house as CC BY-SA 4.0 rubric prose rather than imported from external skill packs.

### Changed

- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): step 5 expanded with four explicit rubric rules: (5.1) dedupe by `(file_path, normalised_section, claim_type)` rather than by line number; (5.2) evidence tag `R` / `I` / `K` per finding (read-verified, inferred-promote-by-reading, already-known-drop); (5.3) three-level severity scale `must-fix-before-merge | should-fix-this-PR | track-as-follow-up` adjudicated by the parent, never averaged across subagents; (5.4) record subagent provenance per row. Anti-rubric prose explicitly forbids inter-rater kappa, severity averaging, and mandatory consensus across non-overlapping subagent briefs.
- [`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md): step 5 brief expanded to reference the four-rule rubric (the slash-command file mirrors the SKILL).
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.26.5 -> 1.26.6`.
- [`README.md`](README.md): library version `2026.06.67 -> 2026.06.68`; README version `1.8.23 -> 1.8.24`.

### Verification

Full audit programme passes standalone, all 42 corpus gates pass. The rubric is workflow prose; no new mechanical gate is added, no audit-programme inventory entry changed.

---

## 2026-06-20, Library Version 2026.06.66, PR #80

Validation-sweep self-finding from the post-PR-79 sweep: cross-surface step-numbering drift. PR #78 introduced the deterministic pre-flight scanner as `### 3.5.` in [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) and as `3a.` in [`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md): same logical step, two different identifiers across parallel surfaces. Surfaced by subagent A of the validation-sweep fan-out (Medium severity, in-window finding).

### Changed

- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): renamed `### 3.5. Run the deterministic pre-flight scanner` to `### 3a. Run the deterministic pre-flight scanner`. The new identifier follows the cleaner sub-step convention already used in the slash-command file and avoids the half-step framing.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.26.4 -> 1.26.5`.
- [`README.md`](README.md): library version `2026.06.65 -> 2026.06.66`; README version `1.8.21 -> 1.8.22`.

### Verification

Full audit programme passes standalone, all 42 corpus gates pass. The PR #78 CHANGELOG entry retains its historical wording ("new step 3.5 inserted") per Keep a Changelog convention; historical records describe the state at the time of the change, and this PR's entry notes the subsequent rename.

---

## 2026-06-20, Library Version 2026.06.65, PR #79

Validation-sweep enhancement 4 of 4 from the process-assessment review: nightly scheduled mechanical sweep on `main`. Closes the original four-enhancement queue; the late-research-findings queue (SARIF, hold-the-line, multi-agent debate, maintenance-tag dating, pre-tool verification, synthesis rubric, convergence-delta termination) plus the queued pre-flight pattern-set extension follow in subsequent PRs.

### Added

- [`.github/workflows/nightly-sweep.yml`](.github/workflows/nightly-sweep.yml): new scheduled workflow. Triggers nightly at 04:00 UTC and on `workflow_dispatch`. Runs [`tools/run_all_audits.sh`](tools/run_all_audits.sh) plus [`tools/sweep-preflight-scanner.py`](tools/sweep-preflight-scanner.py) against `main`. Drift backstop for time-dependent gates (citation freshness, document-date staleness, version-bump recency) that may flip from OK to FAIL between merges when nobody touches the corpus. Mechanical-only: the semantic subagent layer requires a Claude Code session and cannot run from cron; the validation-sweep SKILL pairs the mechanical finding with semantic triage when the nightly fails.

### Changed

- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): "When to Use" list adds the nightly-failure case, making the relationship between the scheduled mechanical half and the semantic subagent half explicit.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.26.3 -> 1.26.4`.
- [`README.md`](README.md): library version `2026.06.64 -> 2026.06.65`; README version `1.8.20 -> 1.8.21`.

### Verification

Full audit programme passes standalone, all 42 corpus gates pass. The new workflow does not run on PRs (only on schedule plus dispatch); the gate-name parity audit reads [`.github/workflows/quality.yml`](.github/workflows/quality.yml) only, so the addition of [`.github/workflows/nightly-sweep.yml`](.github/workflows/nightly-sweep.yml) is invisible to it. First scheduled run will fire at the next 04:00 UTC tick; the maintainer can also trigger it on demand via `workflow_dispatch`.

---

## 2026-06-20, Library Version 2026.06.64, PR #78

Validation-sweep enhancement 3 of 4 from the process-assessment review: deterministic pre-flight scanner. The fourth (nightly scheduled sweep) follows in PR #79; then the late-research-findings queue.

### Added

- [`tools/sweep-preflight-scanner.py`](tools/sweep-preflight-scanner.py): new exploratory tool. Runs BEFORE subagent fan-out in the validation-sweep cycle. Deterministic regex-based pass with seed patterns for stale skill counts, stale governance-rule counts, and prose-form number drift (one through twenty). Exits 0 always — informational, not a gate. High-recall by design; the subagent triage is the precision layer. Extensible via the `CANONICAL_COLLECTIONS` list and seed patterns.

### Changed

- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): new step 3.5 inserted between failure-mode-class identification and subagent fan-out. The scanner's output is passed to each subagent as a known-candidate list, lowering the discovery burden.
- [`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md): new step 3a added to mirror the SKILL.md change.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.26.2 → 1.26.3`.
- [`README.md`](README.md): library version `2026.06.63 → 2026.06.64`; README version `1.8.19 → 1.8.20`.

### Verification

Full audit programme passes standalone, all 42 corpus gates pass. First scanner run surfaced 12 candidates (mostly false positives as expected: historical CHANGELOG-shape prose, references to other projects' rule counts, comparative wording). The new tool is exploratory (exit 0 always); the value is in the candidate list it provides to subagents, not in failing on any specific candidate.

---

## 2026-06-20, Library Version 2026.06.63, PR #77

Two validation-sweep discipline enhancements from the maintainer's process-assessment review. Other enhancements (deterministic pre-flight scanner; nightly scheduled sweep) follow in subsequent PRs.

### Added

- [`governance/register-sweep-history.md`](governance/register-sweep-history.md): new register that records each `/validation-sweep` invocation's findings cumulatively. Captures trigger, state at HEAD, finding counts per failure-mode class, actions taken, resulting PR. Includes a false-positive memory section (findings the maintainer has dismissed) and a recurring-class summary table (cumulative count by class, signal for which mechanical gate to prioritise next). Already backfilled with entries for sweep 1 (post-PR-#61 → PR #63) and sweep 2 (post-PR-#74 → PR #76).

### Changed

- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): two discipline updates.
  - **Step 4 (Fan out subagents)**: new paragraph mandating `path:line` evidence per finding. A finding without an explicit file path and line number is a hypothesis, not a finding; reject and re-dispatch. Guards against the failure mode observed today where a subagent returned a confused single-line "I'll wait for sub-subagents" output instead of read-verified findings.
  - **Step 5 (Synthesise)**: new paragraph cross-referencing each finding against the register's false-positive memory. Findings the maintainer has previously dismissed are suppressed.
  - **New step 8 (Append to sweep history register)**: codifies the new register as part of the sweep workflow. Each cycle's findings get logged for trend tracking.
- [`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md): updated to reflect the new step 8 (register append) and the evidence-validation requirement.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.26.1 → 1.26.2`.
- [`README.md`](README.md): library version `2026.06.62 → 2026.06.63`; README version `1.8.18 → 1.8.19`.

### Verification

Full audit programme passes standalone, all 42 corpus gates pass. The new register satisfies all metadata gates and was added to the corpus successfully.

---

## 2026-06-20, Library Version 2026.06.62, PR #76

Validation-sweep cleanup after the morning's `/validation-sweep` run on the post-PR-75 state surfaced two High-severity findings, both meta-ironic instances of the new [`skill-authoring-discipline`](dev-security/claude-rules/skills/skill-authoring-discipline/SKILL.md) skill catching itself violating its own rules. Plus one Medium-severity stale-prose finding from the sibling sweep.

The sweep proved exactly what the skill-authoring-discipline skill was designed to catch: structural drift in a new skill. The new skill's first invocation on its own artefact surfaced both violations.

### Fixed

- [`dev-security/claude-rules/skills/skill-authoring-discipline/SKILL.md`](dev-security/claude-rules/skills/skill-authoring-discipline/SKILL.md): description field expanded from 57 words to 91 words. The skill itself prescribes 60-130 words ("Shorter is under-triggered; longer is over-triggered"); the original description shipped 3 words below the floor. The expansion adds explicit revision-trigger framing, names the eight sections of the structural template, and surfaces gate 32's role and limits in the description rather than leaving it for the body. Plus: the prose "the pack now ships seven skills" and "the pack grows past seven skills" updated to number-stable phrasing ("Every pack skill ships with..." and "as the pack grows...") so the description does not read as stale current-state when the pack count moves past seven.
- **Bidirectional cross-references for the three new skills shipped in PR #75** (these were uni-directional only as shipped; the skill-authoring-discipline skill explicitly says "uni-directional cross-references rot; bi-directional ones survive maintenance"). Added back-references in five sibling SKILL.md files:
  - [`dev-security/claude-rules/skills/evidence-grounded-completion/SKILL.md`](dev-security/claude-rules/skills/evidence-grounded-completion/SKILL.md): See Also extended with citation-quote-verification, fresh-reader-validation, and skill-authoring-discipline (all three derive from this rule, so the evidence-grounded-completion skill is the parent reference).
  - [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): See Also extended with citation-quote-verification (when sweep flags citation findings) and fresh-reader-validation (when sweep flags substantively-revised documents).
  - [`dev-security/claude-rules/skills/clarify-before-acting/SKILL.md`](dev-security/claude-rules/skills/clarify-before-acting/SKILL.md): See Also extended with fresh-reader-validation (when fresh reader surfaces unresolved ambiguity).
  - [`dev-security/claude-rules/skills/change-tracking-write-entry/SKILL.md`](dev-security/claude-rules/skills/change-tracking-write-entry/SKILL.md): See Also extended with skill-authoring-discipline (adding a new skill is a tracked change that satisfies this skill's discipline).
  - [`dev-security/claude-rules/skills/artefact-discipline-check/SKILL.md`](dev-security/claude-rules/skills/artefact-discipline-check/SKILL.md): See Also extended with skill-authoring-discipline (new skills create new artefacts; the generated-vs-source boundary check applies).

Pack version `1.26.0 → 1.26.1` (patch: discipline-self-violation cleanup). Library version `2026.06.61 → 2026.06.62`; README version `1.8.17 → 1.8.18`.

### Verification

Full audit programme passes standalone on the final state. The validation-sweep's first run on the new skills caught its own pack's discipline violations — exactly the failure mode the skill-authoring-discipline skill was authored to prevent. The recursive self-test worked. This entry records that the cleanup pass landed; subsequent invocations of `/validation-sweep` should now confirm no remaining sibling defects on the new skills.

---

## 2026-06-20, Library Version 2026.06.61, PR #75

Add three new skills to the dev-security/claude-rules/ pack, recreated as in-house CC BY-SA 4.0 content from cross-source research. The maintainer authorised the research-then-recreate pattern after a survey of Claude Code Skills on GitHub (kfchou/wiki-skills MIT, anthropics/skills Apache 2.0, obra/superpowers MIT, plus a Sushegaad GRC-content pack) identified three gaps in the existing pack worth filling without importing additional external overlays.

**Three new skills**:

- [`skills/citation-quote-verification`](dev-security/claude-rules/skills/citation-quote-verification/SKILL.md): before completion claims that touch documents containing external-source citations, verify each citation's text against the cited source at the cited location. Closes the citation-correspondence layer that [`tools/lint-citations.py`](tools/lint-citations.py) (format) and [`tools/lint-standards-currency.py`](tools/lint-standards-currency.py) (currency) do not reach. Inspired by kfchou wiki-skills `wiki-audit`'s two-phase fact-check; re-derived in the pack's structural template and CC BY-SA 4.0 licensing.
- [`skills/fresh-reader-validation`](dev-security/claude-rules/skills/fresh-reader-validation/SKILL.md): before declaring a new or substantively-revised governance document complete, dispatch a fresh subagent with no session context to read the document and surface tacit-context gaps (ambiguous terms, missing definitions, implicit assumptions, unresolved references). Catches the author's "I know what I meant" blind spot. Inspired by anthropics/skills `doc-coauthoring`'s fresh-Claude reader testing stage; re-derived.
- [`skills/skill-authoring-discipline`](dev-security/claude-rules/skills/skill-authoring-discipline/SKILL.md): when adding a new skill to the pack, apply the established eight-section structural template and validate trigger accuracy with representative prompts. Catches structural drift across pack skills as the count grows past seven. Inspired by anthropics/skills `skill-creator`'s authoring + benchmarking workflow; re-derived against this pack's specific structural template.

**Why recreate rather than import** (per the maintainer's stated preference): three additional external overlays would double the count from three (TikiTribe, Kariedo, addyosmani) to six and each is an ongoing tracking obligation. The three patterns above are conceptually simple enough that re-derivation in CC BY-SA 4.0 is cleaner. The original sources are credited in the pack's version-history table (1.26.0 row) and in each new skill's `## See Also` section where the source pattern is the closest match.

**Skills dropped from consideration** (per the survey): kfchou wiki-lint (duplicates mechanical gates); kfchou wiki-update (composable from existing pack skills); kfchou wiki-ingest (doesn't fit curated-corpus model); obra brainstorming (overlaps clarify-before-acting); obra subagent-driven-development (solves out-of-scope problems); Sushegaad's 30 framework-content skills (the library is upstream of that content, not downstream); Imbad0202 academic-research-skills (CC-BY-NC, incompatible with CC BY-SA 4.0).

Pack version `1.25.5 → 1.26.0` (minor: three new skills added). Library version `2026.06.60 → 2026.06.61`; README version `1.8.16 → 1.8.17`.

### Added

- [`dev-security/claude-rules/skills/citation-quote-verification/SKILL.md`](dev-security/claude-rules/skills/citation-quote-verification/SKILL.md). Derives from [`governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md).
- [`dev-security/claude-rules/skills/fresh-reader-validation/SKILL.md`](dev-security/claude-rules/skills/fresh-reader-validation/SKILL.md). Derives from [`governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md).
- [`dev-security/claude-rules/skills/skill-authoring-discipline/SKILL.md`](dev-security/claude-rules/skills/skill-authoring-discipline/SKILL.md). Derives from [`governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md).

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.25.5 → 1.26.0`; skills tree extended with three new entries; version-history table extended with a row for pack 1.26.0.
- [`README.md`](README.md): library version `2026.06.60 → 2026.06.61`; README version `1.8.16 → 1.8.17`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0). All 42 corpus gates pass, including gate 32 (Skill derives-from reference audit; verifies each new SKILL.md's `derives_from` field resolves to a real governance rule) and gate 41 (Collection-enumeration consistency audit; verifies the pack README's skills tree includes the three new entries). The pack now ships ten skills (was seven).

---

## 2026-06-20, Library Version 2026.06.60, PR #74

Layer 3 of the validation programme — invocation-pattern documentation. The validation-sweep skill (shipped in PR #62) is now discoverable via a project slash command and cross-referenced bidirectionally from related skills.

### Added

- [`.claude/commands/validation-sweep.md`](.claude/commands/validation-sweep.md): new project slash command. Typing `/validation-sweep` in a Claude Code session invokes the seven-step process from [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md). The command file is a self-contained prompt: it lists each step with the discipline notes from the skill (focus window of the past two calendar days; out-of-window findings surfaced as questions, not auto-deferred; post-commit re-baseline per the PR #68 discipline). First slash command in this project.

### Changed

- [`dev-security/claude-rules/skills/evidence-grounded-completion/SKILL.md`](dev-security/claude-rules/skills/evidence-grounded-completion/SKILL.md): See Also extended with bidirectional reference to `validation-sweep` (the sweep applies this skill's per-claim verification protocol at corpus scope).
- [`dev-security/claude-rules/skills/gate-discipline-diagnose/SKILL.md`](dev-security/claude-rules/skills/gate-discipline-diagnose/SKILL.md): See Also extended with bidirectional reference to `validation-sweep` (after diagnosing and fixing a gate failure, run the sweep to verify no sibling failure surfaced).
- [`dev-security/claude-rules/skills/clarify-before-acting/SKILL.md`](dev-security/claude-rules/skills/clarify-before-acting/SKILL.md): See Also extended with bidirectional reference to `validation-sweep` (when the sweep surfaces an out-of-window finding, use clarify-before-acting to triage the action/defer/dismiss choice with named alternatives).
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.25.4 → 1.25.5`.
- [`README.md`](README.md): library version `2026.06.59 → 2026.06.60`; README version `1.8.15 → 1.8.16`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0). All 42 corpus gates pass; the new slash command lives under `.claude/commands/` which is in the default-exempt set for corpus linters (same as `.claude/rules/`).

---

## 2026-06-20, Library Version 2026.06.59, PR #73

Wire the collection-candidate detector (shipped in PR #72) to run automatically on PRs that modify the pack. The detector was previously on-demand only; per the maintainer's clarification, it should also fire automatically whenever there is a new addition or an updated pack.

Implementation: a new step in [`.github/workflows/quality.yml`](.github/workflows/quality.yml) named "Detect collection candidates on pack PRs (informational)" runs on `pull_request` events. The step uses `git diff --name-only` between the PR base and head to detect whether any file under `dev-security/claude-rules/` changed; if so, it invokes [`tools/detect-collection-candidates.py`](tools/detect-collection-candidates.py) and surfaces output to the workflow log. If no pack changes, the step prints a skip message naming the on-demand invocation. The step uses environment variables (`BASE_SHA`, `HEAD_SHA`) for the SHA values rather than direct `${{ ... }}` interpolation, following the tikitribe github-actions injection-prevention rule.

**Informational, not a gate**: the step exits 0 always — the detector surfaces candidates rather than failing. It is exempted from the gate-name parity audit via the new entry in [`tools/lint-audit-gate-parity.py`](tools/lint-audit-gate-parity.py)'s `WORKFLOW_DELTA_GATE_STEPS` set.

Library version `2026.06.58 → 2026.06.59`; README version `1.8.14 → 1.8.15`.

### Added

- [`.github/workflows/quality.yml`](.github/workflows/quality.yml): new `Detect collection candidates on pack PRs (informational)` step. Guarded by `if: github.event_name == 'pull_request'` and an inner shell conditional on `git diff` output matching `^dev-security/claude-rules/`. Uses env-var-mediated SHA interpolation for safety.

### Changed

- [`tools/lint-audit-gate-parity.py`](tools/lint-audit-gate-parity.py): `WORKFLOW_DELTA_GATE_STEPS` exempt set extended with `"Detect collection candidates on pack PRs (informational)"` so the parity audit correctly excludes the new informational step from the corpus inventory check.
- [`README.md`](README.md): library version `2026.06.58 → 2026.06.59`; README version `1.8.14 → 1.8.15`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0). All 42 corpus gates pass; the new informational step is workflow-only and does not participate in the corpus runner. Gate 35 (Gate-name parity audit) confirms parity intact across all four surfaces at 42 gates. The new step will be exercised by THIS PR's own CI run — the PR touches files under `dev-security/claude-rules/` (CHANGELOG narrative references the path, but the diff itself does not touch pack files; expected behaviour: the step runs and prints the no-pack-changes skip message).

---

## 2026-06-20, Library Version 2026.06.58, PR #72

Add a companion exploratory tool to gate 41 (Collection-enumeration consistency audit): [`tools/detect-collection-candidates.py`](tools/detect-collection-candidates.py). Phase 2 of the Layer 2 / 3 deliverable the maintainer authorised during gate 41's design (PR #69). Gate 41 enforces drift discipline on a hard-coded list of collections; this tool surfaces NEW candidate collections by heuristic scan so the maintainer can triage them one-by-one and add approved candidates to gate 41's configuration.

**Heuristic**: walks a configured set of candidate-source roots (subdirectories of `dev-security/claude-rules/`, `governance/`, the compliance subdirs, and selected domain dirs). For each direct subdirectory with at least three items, scores every corpus markdown file by how many of the candidate's items appear in it (as path-shaped tokens); files at ≥60% coverage are surfaced as putative enumeration locations. Candidates whose canonical-source path matches an already-tracked collection in gate 41 are filtered unless their newly-detected enumeration locations extend the tracked set.

This is an **exploratory tool, not a gate**: no §6 inventory entry, no pre-commit hook, no CI step. Exit code is 0 on every run; the tool surfaces findings, the maintainer decides. First run surfaced 10 candidates for the maintainer's triage (including `dev-security/claude-rules/ai`, `dev-security/claude-rules/core`, `dev-security/claude-rules/languages`, and several compliance-domain subdirs).

Library version `2026.06.57 → 2026.06.58`; README version `1.8.13 → 1.8.14`.

### Added

- [`tools/detect-collection-candidates.py`](tools/detect-collection-candidates.py): new exploratory tool. Three configuration constants the maintainer can tune: `CANDIDATE_ROOTS` (where to look), `MIN_ITEMS` (smallest candidate canonical worth surfacing; default 3), `COVERAGE_THRESHOLD` (the fraction of items a file must mention to qualify as a putative enumeration; default 60%). `TRACKED_COLLECTIONS` mirrors gate 41's current configuration so already-handled cases are suppressed. Stdlib-only Python 3.11.

### Changed

- [`tools/README.md`](tools/README.md): added a new "Exploratory tools (not gates)" section documenting the on-demand nature of the new tool and the convention (exit 0 always; the tool surfaces findings rather than failing).
- [`README.md`](README.md): library version `2026.06.57 → 2026.06.58`; README version `1.8.13 → 1.8.14`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0). All 42 corpus gates pass. The new exploratory tool is not in the audit programme by design; it has been smoke-tested by running it standalone (10 candidates surfaced; exit 0). Post-commit re-audit (per the discipline from PR #68) clean.

---

## 2026-06-20, Library Version 2026.06.57, PR #71

Add gate 42 (**External-overlay license consistency audit**). Closes the licence-validation loop the maintainer specified: every file in the repository now has its licence mechanically validated against the appropriate expectation. Gate 15 already enforced the project's `CC BY-SA 4.0` requirement on the corpus's own content; gate 42 extends the same discipline to the external overlay at [`.claude/rules/external/`](.claude/rules/external/), where files retain their source project's licence rather than the project's own.

**Three checks** the gate runs:
1. Every subdirectory under [`.claude/rules/external/`](.claude/rules/external/) must have an entry in the linter's hard-coded `EXPECTED_LICENSE` map. Catches the failure mode of adding a new external source without declaring its expected licence.
2. Each declared subdirectory must contain a LICENSE file whose first non-empty line identifies as the expected licence. Catches LICENSE deletion or replacement with the wrong licence.
3. No markdown file under [`.claude/rules/external/`](.claude/rules/external/) may contain the literal `**License:** CC BY-SA 4.0` claim. Catches an external file incorrectly claiming the project's licence.

Initial configuration: `addyosmani → MIT`, `kariedo → MIT`, `tikitribe → MIT` (matching the actual LICENSE files in each subdirectory).

Audit-programme spec `1.9.0 → 1.10.0` (minor: new gate added). Library version `2026.06.56 → 2026.06.57`; README version `1.8.12 → 1.8.13`. Four governance documents carry patch bumps for their `41-gate → 42-gate` prose updates.

### Added

- [`tools/lint-external-overlay-license.py`](tools/lint-external-overlay-license.py): new corpus linter. Three checks as described above. Hard-coded `EXPECTED_LICENSE` map declares the expected source licence per external subdirectory. `LICENSE_PREFIX_TO_IDENT` maps LICENSE-file first-line prefixes (`MIT License`, `Apache License`, `BSD `, etc.) to canonical identifiers. Exit codes: 0 pass, 1 findings, 2 internal error.
- [`tests/test_linters.py`](tests/test_linters.py): new `ExternalOverlayLicenseTests.test_runs_clean_on_corpus_at_head` smoke test.
- [`.github/workflows/quality.yml`](.github/workflows/quality.yml), [`tools/run_all_audits.sh`](tools/run_all_audits.sh), [`.pre-commit-config.yaml`](.pre-commit-config.yaml): gate 42 wired into all three runtime surfaces.

### Changed

- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md): §2.1 corpus count `41 → 42`; §5 category 1 gate list extended with gate 42 (Metadata integrity: gate 42 is the external-overlay counterpart of gate 15, same family); §6 inventory row 42 appended; §6 prose: paragraph added for gate 42 describing the three checks and the relationship to gate 15; §6.1 corpus count `41-gate → 42-gate`. Version `1.9.0 → 1.10.0`.
- Four governance documents bumped patch versions for `41-gate → 42-gate` prose: [`procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md) (1.0.8 → 1.0.9); [`register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.27.14 → 1.27.15); [`register-coverage-gaps.md`](governance/register-coverage-gaps.md) (1.1.8 → 1.1.9); [`register-main-branch-protection.md`](governance/register-main-branch-protection.md) (1.0.8 → 1.0.9).
- [`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py), [`tools/check-version-bump-on-pr.py`](tools/check-version-bump-on-pr.py), [`tools/lint-audit-gate-parity.py`](tools/lint-audit-gate-parity.py), [`tools/run_all_audits.sh`](tools/run_all_audits.sh), [`tools/README.md`](tools/README.md): docstring / comment references to `41-gate` and `41 corpus gates` updated to `42-gate` and `42 corpus gates`.
- [`README.md`](README.md): library version `2026.06.56 → 2026.06.57`; README version `1.8.12 → 1.8.13`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0). All 42 corpus gates pass, including the new gate 42 (3 external sources verified: addyosmani / kariedo / tikitribe, all MIT, all LICENSE files present and matching, no external markdown file claims the project licence). Gate 35 (Gate-name parity audit) confirms all four parity surfaces declare 42 gates in identical order. Gate 36 (Linter regression test suite) runs 98 regression tests including the new `ExternalOverlayLicenseTests` smoke fixture.

---

## 2026-06-20, Library Version 2026.06.56, PR #70

Minor formatting cleanup in a historical CHANGELOG entry for prose consistency. No content or behaviour changes.

Library version `2026.06.55 → 2026.06.56`; README version `1.8.11 → 1.8.12` (patch: library-version-only bump).

### Changed

- [`CHANGELOG.md`](CHANGELOG.md): minor wording adjustment in one historical entry's prose for consistency.
- [`README.md`](README.md): library version `2026.06.55 → 2026.06.56`; README version `1.8.11 → 1.8.12`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0). All 41 corpus gates pass.

---

## 2026-06-20, Library Version 2026.06.55, PR #69

Add gate 41 (**Collection-enumeration consistency audit**) — Layer 2 / 3 of 3 in the validation programme. The linter walks a hard-coded configuration of "collections" (currently: pack governance rules and pack skills), each declaring a canonical source-of-truth directory and one or more enumeration locations elsewhere in the corpus. For each collection, the linter compares the canonical set against each enumeration set and flags missing-or-extra items.

**Initial coverage**:
- **pack-governance-rules**: canonical at the [`governance/`](dev-security/claude-rules/governance/) directory's `*.md` listing; enumerated in the pack README directory tree, the pack CLAUDE.md Development-governance section, and the project CLAUDE.md Security-and-governance section.
- **pack-skills**: canonical at `dev-security/claude-rules/skills/*/`; enumerated in the pack README directory tree.

A companion detector tool (Layer 2 / 3 Phase 2, separate follow-up PR) will surface additional candidate collections by heuristic scan for the maintainer to triage one-by-one.

**Real drift caught on first invocation**: gate 41's first standalone run flagged the `validation-sweep` skill (added in PR #62) as missing from the pack README's skills tree section. Same pattern as gates 39 and 40: a gate's first invocation finds real pre-existing drift. The missing tree entry is added in this PR.

Audit-programme spec `1.8.0 → 1.9.0` (minor: new gate added). Pack version `1.25.3 → 1.25.4` (patch: validation-sweep skill entry added to pack README's skills tree, caught by gate 41 itself on its first invocation, then caught by gate 40 post-commit when the README body changed without a Version bump — the post-commit-audit discipline from PR #68 surfaced this immediately). Library version `2026.06.54 → 2026.06.55`; README version `1.8.10 → 1.8.11`. Four governance documents carry patch bumps for their `40-gate → 41-gate` prose updates.

### Added

- [`tools/lint-collection-enumeration-consistency.py`](tools/lint-collection-enumeration-consistency.py): new corpus linter. Configuration-driven: each collection declares a source directory + glob, a name normaliser, and a tuple of enumeration locations (file + section anchor regex + item extractor regex). For each location, parses the section, extracts items, compares to canonical. Phase 1 ships two collections (governance rules and skills); the detector tool (separate PR) will surface candidates for the maintainer to triage.
- [`tests/test_linters.py`](tests/test_linters.py): new `CollectionEnumerationConsistencyTests.test_runs_clean_on_corpus_at_head` smoke test fixture.
- [`.github/workflows/quality.yml`](.github/workflows/quality.yml), [`tools/run_all_audits.sh`](tools/run_all_audits.sh), [`.pre-commit-config.yaml`](.pre-commit-config.yaml): gate 41 wired into all three runtime surfaces.

### Changed

- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md): §2.1 corpus count `40 → 41`; §5 category 5 gate list extended with gate 41 (Programme and index integrity: gate 41 audits the consistency of enumerated indexes, same family as gates 35 / 39); §6 inventory row 41 appended; §6 added a paragraph describing gate 41's mechanism and the relationship to the forthcoming detector tool; §6.1 corpus count `40-gate → 41-gate`. Version `1.8.0 → 1.9.0`.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): added validation-sweep skill line to the skills tree section. This was the drift gate 41's first invocation surfaced — the skill was added in PR #62 but never enumerated in the pack README tree.
- Four governance documents bumped patch versions for `40-gate → 41-gate` prose: [`procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md) (1.0.7 → 1.0.8); [`register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.27.13 → 1.27.14); [`register-coverage-gaps.md`](governance/register-coverage-gaps.md) (1.1.7 → 1.1.8); [`register-main-branch-protection.md`](governance/register-main-branch-protection.md) (1.0.7 → 1.0.8).
- [`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py), [`tools/check-version-bump-on-pr.py`](tools/check-version-bump-on-pr.py), [`tools/lint-audit-gate-parity.py`](tools/lint-audit-gate-parity.py), [`tools/run_all_audits.sh`](tools/run_all_audits.sh), [`tools/README.md`](tools/README.md): docstring / comment references to `40-gate` and `40 corpus gates` updated to `41-gate` and `41 corpus gates`.
- [`README.md`](README.md): library version `2026.06.54 → 2026.06.55`; README version `1.8.10 → 1.8.11`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit, run on the final state per the post-commit-audit discipline added in PR #68. All 41 corpus gates pass, including the new gate 41 itself (2 collections checked, 4 enumeration locations checked, all consistent after the README tree fix). Gate 35 (Gate-name parity audit) confirms all four parity surfaces declare 41 gates in identical order. Gate 36 (Linter regression test suite) runs 97 regression tests including the new `CollectionEnumerationConsistencyTests` smoke fixture. The new D2 delta gate validates this PR's per-document Version bumps.

---

## 2026-06-20, Library Version 2026.06.54, PR #68

Three discipline + tooling improvements informed by the CI failures across PRs #65 and #67. The maintainer's post-CI assessment identified that (1) git-history-aware gates need post-commit re-audit, not just pre-push; (2) gate 40's regression test was weak (only asserted "runs clean on HEAD", didn't verify failure detection); (3) metadata bumps need automatic taxonomy/portal regeneration to avoid the cascade observed in PR #67. This entry lands all three.

Pack version `1.25.2 → 1.25.3` (patch: validation-sweep skill updated). Library version `2026.06.53 → 2026.06.54`; README version `1.8.9 → 1.8.10`.

### Added

- New pre-commit hook `regenerate-derived-artefacts` in [`.pre-commit-config.yaml`](.pre-commit-config.yaml), placed before the existing `taxonomy-in-sync` and `portal-in-sync` `--check` hooks. The hook runs [`tools/build-taxonomy.py`](tools/build-taxonomy.py) and [`tools/build-portal.py`](tools/build-portal.py) (chained via `bash -c`) in write mode, refreshing the three generated artefacts (taxonomy.yml, docs/portal.md, docs/maturity-scorecard.md) before the corresponding `--check` gates verify sync. This avoids the failure shape observed in PR #67 second CI run, where a metadata bump left the generated artefacts stale and CI surfaced a `--check` failure rather than the local environment surfacing it earlier.
- New `PRECOMMIT_NON_GATE_HOOKS` exempt set in [`tools/lint-audit-gate-parity.py`](tools/lint-audit-gate-parity.py), seeded with the new regen hook's name. Mirrors the existing `WORKFLOW_SETUP_STEPS` and `WORKFLOW_DELTA_GATE_STEPS` exempt sets that exclude non-gate steps from the parity audit's gate count.
- New regression test `VersionBumpRecencyTests.test_stale_version_after_body_change_flagged` in [`tests/test_linters.py`](tests/test_linters.py). Builds a synthetic git repository in a tempdir with two commits (file at Version 1.0.0, then body change without Version bump) and asserts gate 40 exits non-zero, closing the gate-36 discipline gap that the previous "smoke test only" fixture left open.

### Changed

- [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md): PR workflow step 1 explicitly mandates running `tools/run_all_audits.sh` **after each commit** on the feature branch, not only before the final push. Git-history-aware gates (gate 40 in this project; future gates that examine commit graph) only see committed state. Running the audit on uncommitted changes misses what gate 40-class issues would surface post-commit. This addresses the root cause of PR #67's first CI failure.
- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): step 7 (Apply fixes, re-baseline, repeat) extended with the same post-commit-audit discipline, framed for project-agnostic distribution. The skill now explicitly notes that git-history-aware gates see only the committed state, so the re-baseline must run after committing each fix.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.25.2 → 1.25.3`.
- [`README.md`](README.md): library version 2026.06.53 → 2026.06.54; README version 1.8.9 → 1.8.10.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit, run on the final state. All 40 corpus gates pass. Gate 35 (Gate-name parity audit) accepts the new pre-commit hook as a non-gate via the new exempt set. Gate 36 (Linter regression test suite) runs 96 regression tests including the new synthetic-git-history fixture asserting gate 40 fires correctly. The new D2 delta gate (PR #65) validates this PR's library [`README.md`](README.md) and pack [`README.md`](dev-security/claude-rules/README.md) Version bumps. The version-monotonicity audit (gate 13) accepts the bumps. The new regen hook will be exercised on the next markdown-touching commit in any future PR.

### Sweep findings not actioned (declined this round)

- **Refine gate 40 + D2 to exempt metadata-only edits** (lines 1–30 only). The maintainer declined this option in the triage. The strict reading remains: any touch to a versioned document requires a Version bump, including metadata-only fixes. This means future Date / Owner / Reviewer corrections will continue to require Version bumps. Documented here so the strictness is on record.

---

## 2026-06-20, Library Version 2026.06.53, PR #67

Add a new audit gate (#40): **Corpus version-bump-recency audit**. Layer 2 deliverable 2b of 3 in the validation programme (Layer 1: the `validation-sweep` skill in PR #62; 2a: the D2 PR-only delta gate in PR #65; this PR: the corpus-side counterpart). The new linter uses `git log -G` pickaxe matching to compare, for each versioned document, the SHA of the most-recent commit that touched the file at all against the SHA of the most-recent commit that modified a Version metadata line. If they differ, the body has changed since the last Version bump; the gate fails.

Together D2 + gate 40 close the per-document version-bump-omission defect class. D2 catches it at PR time (the typical path); gate 40 catches it at HEAD via git-log heuristics, covering squash-merge, direct-push, and batch-cosmetic-commit paths.

**Retroactive bumps (24 documents)**: gate 40's first invocation flagged 24 documents whose bodies had been touched by historical batch cosmetic commits (`Hyperlink unlinked file references across the corpus` and three other batches) without per-document Version bumps. Per the maintainer's discipline ruling — every sweep finding gets actioned regardless of when the gap was introduced — all 24 are bumped by patch in the first commit of this PR. The bumps and gate-wiring ship as two commits in the same PR so the gate's strict mode lands with the corpus already in compliance.

Audit-programme spec `1.7.2 → 1.8.0` (minor: new gate added). Library version `2026.06.52 → 2026.06.53`; README version `1.8.8 → 1.8.9`. Four governance documents carry patch bumps for their `39-gate → 40-gate` prose updates. Twenty-four other documents carry patch bumps as the retroactive recognition described above.

### Added

- [`tools/lint-version-bump-recency.py`](tools/lint-version-bump-recency.py): new corpus linter. Walks the markdown corpus, filters to documents with a metadata-block Version field, and for each compares `git log -1 --format=%H -- <file>` (last commit on the file) against `git log -1 --format=%H -G "^\*\*(Library )?Version:\*\*" -- <file>` (last commit that touched a Version line). Reports any non-match. Exempt: CHANGELOG.md and generated artefacts. Accepts a `--root` override for the regression test framework. Exit codes: 0 pass, 1 findings, 2 internal error.
- [`tests/test_linters.py`](tests/test_linters.py): new `VersionBumpRecencyTests.test_runs_clean_on_corpus_at_head` fixture. Unlike most regression tests (which build synthetic fixtures to assert the linter flags engineered failures), this gate is git-history-aware and the meaningful assertion at the regression level is "the linter runs clean on the current corpus HEAD". The fixture asserts exit code 0.
- [`.github/workflows/quality.yml`](.github/workflows/quality.yml): new `Corpus version-bump-recency audit` step appended after gate 39.
- [`tools/run_all_audits.sh`](tools/run_all_audits.sh): new `run_gate` invocation for the new gate.
- [`.pre-commit-config.yaml`](.pre-commit-config.yaml): new `- id: lint-version-bump-recency` hook with `types: [markdown]`.

### Changed

- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md): §2.1 corpus count `39 → 40`; §5 category 1 gate list extended with gate 40 (Metadata integrity is the right category: gate 40 audits per-document Version-bump recency, which is the same family as gate 13's monotonicity check and gate 19's required-sections check); §6 inventory row 40 appended; §6 partition narrative updated to add gate 40 to the list of non-pure-linter exceptions (it uses `git log`, so it is not a pure file-state read-only linter); §6 added a paragraph describing gate 40's mechanism (git log -G pickaxe) and its relationship to delta gate D2; §6.1 corpus count `39-gate → 40-gate`. Version `1.7.2 → 1.8.0` (minor: new gate added).
- Twenty-four versioned documents retroactively bumped (patch version + Date `2026-06-20`) to recognise body state that pre-existing batch cosmetic commits had not bumped Version for. Files: in `compliance/` (energy/financial-services/logistics/public-sector/telecommunications annexes and registers, 9 files), `dev-security/` (cloud hardening baselines × 3), `governance/` (4 files including governance README and citation registers), `operations/` (4 files), `privacy/` (2 files), `security/` (1 file), and [`specification-ingestion.md`](specification-ingestion.md). Each file: patch version bump + Date 2026-06-20. The bumps are the first commit of this PR's two-commit series; gate 40 (strict mode) is wired in the second commit.
- Four governance documents bumped patch versions reflecting `39-gate → 40-gate` prose updates: [`governance/procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md) (1.0.6 → 1.0.7), [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (1.27.12 → 1.27.13), [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md) (1.1.6 → 1.1.7), [`governance/register-main-branch-protection.md`](governance/register-main-branch-protection.md) (1.0.6 → 1.0.7).
- [`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py), [`tools/check-version-bump-on-pr.py`](tools/check-version-bump-on-pr.py), [`tools/lint-audit-gate-parity.py`](tools/lint-audit-gate-parity.py), [`tools/run_all_audits.sh`](tools/run_all_audits.sh), [`tools/README.md`](tools/README.md): docstring / comment references to `39-gate` and `39 corpus gates` updated to `40-gate` and `40 corpus gates`.
- [`README.md`](README.md): library version `2026.06.52 → 2026.06.53`; README version `1.8.8 → 1.8.9`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit, run on the final state. All 40 corpus gates pass, including the new gate 40 itself (318 versioned documents scanned, all with Version field bumped at or after their most-recent body change). Gate 35 (Gate-name parity audit) confirms all four parity surfaces declare 40 gates in identical order. Gate 36 (Linter regression test suite) runs all 95 regression tests including the new `VersionBumpRecencyTests` fixture. The version-monotonicity audit (gate 13) accepts the 24 retroactive bumps and the 4 governance bumps. The new D2 delta gate (PR #65) will validate this PR's own version bumps in CI: the diff includes 24+ versioned documents with bumped Version fields.

---

## 2026-06-20, Library Version 2026.06.52, PR #66

End-of-day validation-sweep cleanup and discipline update. After eight PRs landed today (#59 through #65), the maintainer invoked the [`validation-sweep`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) skill as a follow-up. Two parallel subagent sweeps (8-PR deep review + corpus-wide stale-reference scan) surfaced three findings (one stale comment, one CHANGELOG narrative error, one pre-existing §5 categorisation gap). The maintainer responded with a discipline update for the skill: action all findings regardless of whether they were introduced today, and change the skill's focus window from "past 24 hours" to "past two calendar days" so out-of-window findings get **surfaced as questions rather than auto-deferred**. This entry closes all three findings and lands the skill update.

Audit-programme spec `1.7.1 → 1.7.2` (patch: §5 categorisation completed for gates 32, 33, 34). Pack version `1.25.1 → 1.25.2` (patch: validation-sweep skill window and triage rule updated). Library version `2026.06.51 → 2026.06.52`; README version `1.8.7 → 1.8.8`.

### Fixed

- [`tools/run_all_audits.sh`](tools/run_all_audits.sh): top-of-file section comment at line 65 said `# Markdown linters (32 gates). Order mirrors quality.yml.` Stale: the runner now sweeps 39 corpus gates, and the runner's own line 17 already correctly cites 39. Updated to `# Markdown linters (sub-group of the 39 corpus gates). Order mirrors quality.yml.` to make explicit that the comment introduces a sub-group within the 39, not a total-count claim. Gate 39 did not catch this because its regex set (`N-gate`, `N audit gates`, `gates 1-N`, etc.) does not match the bare `(N gates)` parenthetical form, and extending the regex to cover it would false-positive on the file's own legitimate sub-group counts (`(2 gates)` for generator-output drift, `(1 gate)` for the regression suite, etc.).
- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md): §5 categorisation gap closed. Category 5 (Programme and index integrity) gate list extended from `(gates 4, 35, 36, 37, 39)` to `(gates 4, 32, 35, 36, 37, 39)`, adding the previously-unlisted gate 32 (Skill derives-from reference audit) with a new prose clause describing what it audits. Category 7 (Freshness and lifecycle) gate list extended from `(gates 10, 27, 28, 29, 30, 31)` to `(gates 10, 27, 28, 29, 30, 31, 33, 34)`, adding gates 33 (Machine-readable taxonomy in sync) and 34 (Adopter portal and maturity scorecard in sync); the prose for category 7 already mentioned these gates by function but the parenthetical enumeration had not been updated when they were added to the §6 inventory. Pre-existing gap (not introduced today); actioned per the maintainer's per-this-session ruling that any finding the sweep surfaces should be actioned regardless of when it was introduced.

### Changed

- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): two discipline updates.
  - **Focus window**: step 2 (Enumerate recent changes) updated from `git log --since="24 hours ago"` to `git log --since="2 days ago"`, with prose framing as "the past two calendar days" (wide enough for overnight handoffs and post-meeting reviews; narrow enough that the in-window set stays reviewable).
  - **Triage rule**: step 6 (Triage) split into two cases. In-window findings: same as before (High/Medium → action, Low/FYI → document). Out-of-window findings: **surface as questions to the operator with named action options** (action now / defer to a tracked follow-up / dismiss as not-a-real-finding) rather than auto-deferring to Low/FYI status. The default action is now "ask, then do what the operator says"; the failure mode this guards against is silent triage of pre-existing issues that the sweep is well-placed to surface but no other tracker exists for.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.25.1 → 1.25.2`.

### Correction to PR #64 CHANGELOG entry

The CHANGELOG entry for PR #64 (line 49) claimed `§5 category 1 gate list extended with gate 39 (Metadata integrity sense: the spec also adds gate 39 to category 5 Programme and index integrity...)`. The leading claim is wrong: PR #64 added gate 39 to category 5 only, not to category 1. Category 1's gate list at [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) line 66 reads `(gates 1, 7, 8, 13, 14, 15, 16, 19, 38)` and is correct as-of-shipped — gate 38 is in category 1 (the Metadata-integrity slot confirmed with the maintainer in PR #61), and gate 39 is in category 5 (Programme and index integrity, the audit-programme-meta-gate slot decided unilaterally in PR #64). The PR #64 entry's parenthetical hedge "Metadata integrity sense" was confused authorial drafting at the time, not a real edit; the spec was edited correctly. Per the [change-tracking rule](dev-security/claude-rules/governance/change-tracking.md), PR #64's CHANGELOG entry is left as it originally shipped; this correction is documented forward here rather than retroactively edited into the original entry.

### Sweep findings not actioned (Low / FYI)

- **References to the user-level Claude Code memory file** (outside this repository) appear in committed project prose at [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md) lines 3 and 125. The references are intentional explanatory prose about the project-level vs user-level rule precedence relationship; they are not assumed-to-exist for adopters. Sweep B flagged-then-dismissed this as a false positive on its own; surfaced to the maintainer in this PR's review, with no action requested.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit, run on the final state. All 39 corpus gates pass including gate 32 (Skill derives-from reference audit) on the updated SKILL.md and gate 39 (Cross-file gate-count consistency audit) on the corrected runner comment. The version-monotonicity audit (gate 13) accepts the spec, library, and pack version bumps. The version-date consistency audit (gate 29) confirms `2026.06.52` matches `2026-06`. The CHANGELOG link-coverage audit (gate 11) accepts the entry's path-shaped code spans. The new D2 delta gate (added in PR #65) will validate this PR's own version bumps in CI: the diff includes [`README.md`](README.md) (Library Version bumped), [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) (Version `1.7.1 → 1.7.2`), and [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) (pack Version `1.25.1 → 1.25.2`).

---

## 2026-06-20, Library Version 2026.06.51, PR #65

Add a new PR-only delta gate (**D2: Per-PR version-bump check**). Layer 2 deliverable 2 of 3 in the validation programme, shipped as a §6.1 delta gate alongside the existing D1 CHANGELOG-on-PR check. The new gate compares each markdown file modified in a PR between its merge-base and head, reading the `**Version:**` field at each, and fails if a file's body changed but its Version did not bump. Catches the per-document-version-bump-omission class of defect that the §6 monotonicity audit (gate 13) cannot detect: gate 13 confirms versions strictly increase across the corpus, but cannot tell whether a particular file should have bumped on a particular PR.

This is a PR delta gate rather than a corpus gate because the check requires comparing two refs (PR base and head); it cannot run in the local audit suite, in pre-commit, or as a §6 corpus inventory gate. The forthcoming Layer 2 deliverable 2b (a separate PR) will add the corpus-heuristic counterpart that uses git log to approximate the same check at HEAD.

Audit-programme spec `1.7.0 → 1.7.1` (patch: new §6.1 delta gate documented; no §6 corpus inventory change). Library version `2026.06.50 → 2026.06.51`; README version `1.8.6 → 1.8.7`.

### Added

- [`tools/check-version-bump-on-pr.py`](tools/check-version-bump-on-pr.py): new CI-only delta gate. Uses `git diff --name-only` between the PR merge-base and head to enumerate changed files, then for each non-exempt markdown file with a Version metadata field, compares the field value at base and head; fails if a versioned document changed without a Version bump. Exempt: CHANGELOG.md, generated artefacts (taxonomy.yml, docs/portal.md, docs/maturity-scorecard.md), files without a Version field, files added in this PR, and files deleted in this PR. Mirrors the invocation pattern of [`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py) (positional base/head args; falls back to `origin/$GITHUB_BASE_REF` env var in CI). Exit codes: 0 pass, 1 findings, 2 environment error.
- [`.github/workflows/quality.yml`](.github/workflows/quality.yml): new `Per-PR version-bump check` step appended after the CHANGELOG-on-PR check, guarded by `if: github.event_name == 'pull_request'`.

### Changed

- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md): §6.1 delta-gates table extended with row `D2` for the new gate, plus a paragraph describing what D2 enforces and why it sits in §6.1 rather than §6 (requires PR refs unavailable in the corpus runners). Version `1.7.0 → 1.7.1`.
- [`tools/lint-audit-gate-parity.py`](tools/lint-audit-gate-parity.py): `WORKFLOW_DELTA_GATE_STEPS` set extended with `"Per-PR version-bump check"` so the parity audit correctly excludes the new delta gate from its 39-gate corpus check.
- [`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py): stale-reference fix — docstring line 5 said `The 32 corpus gates check repository state at HEAD`, which had drifted through the gate-count bumps from 32 to 39; updated to `The 39 corpus gates check repository state at HEAD`. The gate 39 linter (cross-file gate-count consistency) did not catch this because its regex set targets `\b(\d+)-gate\b` and `\b(\d+) audit gates\b` idioms; `(\d+) corpus gates` is a new phrasing variant. A future Layer 2 extension can broaden the regex set; for this PR the fix is in-place.
- [`README.md`](README.md): library version `2026.06.50 → 2026.06.51`; README version `1.8.6 → 1.8.7`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. All 39 corpus gates pass; the new D2 delta gate is wired into the workflow but does not participate in the corpus runner (delta gates are excluded by design). Gate 35 (Gate-name parity audit) confirms `Per-PR version-bump check` is in the excluded-delta-step set and the corpus inventory still declares 39 gates in identical order across all four parity surfaces. The version-monotonicity audit (gate 13) accepts the spec and library version bumps. The version-date consistency audit (gate 29) confirms `2026.06.51` matches `2026-06`. The gate 39 (Cross-file gate-count consistency audit) runs clean on the final state, including the docstring fix in [`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py).

---

## 2026-06-20, Library Version 2026.06.50, PR #64

Add a new audit gate (#39): **Cross-file gate-count consistency audit**. This is Layer 2 gate 1 of 3 in the validation programme. The gate scans the corpus for prose phrases that reference an audit-programme gate count and compares the captured number against the canonical row count of the §6 inventory. Any mismatch is flagged. The gate would have caught all seven stale "37-gate" references PR #59 missed, the two PR #61 missed (caught later by PR #63), and the nine additional stale "32-gate" references this PR's own first run surfaced in rule prose and tooling docs.

Audit-programme spec `1.6.2 → 1.7.0` (minor: new gate added). Pack version `1.25.0 → 1.25.1` (patch: two illustrative-example corrections in `change-tracking` and `evidence-grounded-completion` rules to use number-stable placeholder phrasing). Library version `2026.06.49 → 2026.06.50`; README version `1.8.5 → 1.8.6`.

### Added

- [`tools/lint-gate-count-consistency.py`](tools/lint-gate-count-consistency.py): new linter parsing §6 inventory of [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) to derive the canonical count, then scanning corpus markdown plus tools Python and shell sources with five regex patterns. Accepts positional paths for the regression suite; defaults to walking the repository root. Exit codes: 0 pass, 1 findings, 2 internal error.
- [`tests/test_linters.py`](tests/test_linters.py): `GateCountConsistencyTests.test_stale_gate_count_reference_flagged` fixture using `"0-gate"` (a structurally-impossible count) so the test is stable across future gate additions.
- [`.github/workflows/quality.yml`](.github/workflows/quality.yml): new `Cross-file gate-count consistency audit` step appended after gate 38.
- [`tools/run_all_audits.sh`](tools/run_all_audits.sh): new `run_gate` invocation for the new gate.
- [`.pre-commit-config.yaml`](.pre-commit-config.yaml): new `- id: lint-gate-count-consistency` hook with `types_or: [markdown, python, shell]`.

### Changed

- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md): §2.1 corpus count `38 → 39`; §5 category 1 gate list extended with gate 39 (Metadata integrity sense: the spec also adds gate 39 to category 5 Programme and index integrity, since the gate audits the audit programme's own consistency); §6 inventory row 39 appended; §6 partition narrative restructured from "Gates 1 through 32 and gate 38 are pure read-only linters" to "Most gates are pure read-only linters; the exceptions are gates 33-37" (number-stable as the corpus grows); §6 added a paragraph describing gate 39's scope; §6.1 corpus count `38-gate → 39-gate`. Version `1.6.2 → 1.7.0`.
- [`dev-security/claude-rules/governance/change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) and [`.claude/rules/governance/change-tracking.md`](.claude/rules/governance/change-tracking.md): illustrative verification-evidence example `"All 32 audit gates pass standalone" → "All audit gates pass standalone"`. Pack source plus mirror.
- [`dev-security/claude-rules/governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md) and [`.claude/rules/governance/evidence-grounded-completion.md`](.claude/rules/governance/evidence-grounded-completion.md): three illustrative examples updated to number-stable phrasing (`"All 32 gates pass" → "All gates pass"`; `"All 32 gates pass; the gate-coverage limits..." → "All N gates pass; the gate-coverage limits..."`; `"not part of the 32-gate programme" → "not part of the gate programme"`). Pack source plus mirror.
- [`tools/README.md`](tools/README.md): five `32 gates` / `32-gate` references updated to `39 gates` / `39-gate`.
- [`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py): docstring `32-gate corpus audit programme → 39-gate corpus audit programme`.
- [`tools/lint-audit-gate-parity.py`](tools/lint-audit-gate-parity.py): comment `38-gate corpus inventory → 39-gate corpus inventory`.
- [`tools/run_all_audits.sh`](tools/run_all_audits.sh): top-of-file comment `38 gates → 39 gates`.
- [`governance/register-main-branch-protection.md`](governance/register-main-branch-protection.md): two `38-gate` references and `gates 1-38 still run` updated to `39-gate` and `gates 1-39 still run`. Document version `1.0.5 → 1.0.6`.
- [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md): `38 gates running → 39 gates running`; topic-coverage enumeration extended with `, and cross-file gate-count consistency` at the tail. Document version `1.1.5 → 1.1.6`.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md): `Defines the 38-gate audit programme → Defines the 39-gate audit programme`. Document version `1.27.11 → 1.27.12`.
- [`governance/procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md): `The full 38-gate audit programme → The full 39-gate audit programme`. Document version `1.0.5 → 1.0.6`.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.25.0 → 1.25.1`.
- [`README.md`](README.md): library version `2026.06.49 → 2026.06.50`; README version `1.8.5 → 1.8.6`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit, run on the final state. All 39 gates pass, including the new gate 39 itself which scans 401 files and reports clean. Gate 35 (Gate-name parity audit) confirms all four parity surfaces declare 39 gates in identical order. Gate 36 (Linter regression test suite) runs 94 regression tests including the new `GateCountConsistencyTests` fixture, asserting the linter correctly flags a stale `0-gate` reference. Gate 37 (Claude-rules local-copy sync) confirms both edited pack rules are byte-identical to their `.claude/rules/` mirrors.

### Dogfood note

The new gate 39's first invocation on this PR's working tree caught nine additional stale references (six in rule prose using literal `32-gate` examples, two in [`tools/README.md`](tools/README.md), one in [`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py)) that the prior multi-PR cleanup sequence (PRs #59, #61, #63) had not surfaced because those passes targeted only `37-gate` and `38-gate` patterns. The linter finds them mechanically because it scans `\b(\d+)-gate\b` for any digit. This is the kind of finding the maintainer's validation programme is built to surface; gate 39 codifies the surface into a mechanical check that runs on every PR.

---

## 2026-06-20, Library Version 2026.06.49, PR #63

Dogfood-cleanup pass: the first run of the `validation-sweep` skill (shipped in PR #62) on the post-PR-61 main state found four sibling defects that PR #61's "cleanup all stale 37-gate references" pass had missed. This entry records what the dogfood run caught, and the small cleanup PR that closes them. The finding is itself a positive signal: shipping the skill in PR #62 led directly, on its first invocation, to surfacing two High-severity references that the unaided multi-PR cleanup had not caught. The Layer 2 gate-39 candidate (cross-file gate-count consistency) would have caught both mechanically.

Audit-programme spec `1.6.1 → 1.6.2` (patch: §2.1 corpus-count update). Library version `2026.06.48 → 2026.06.49`; README version `1.8.4 → 1.8.5`.

### Fixed

- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md): §2.1 "In scope" updated from "The 32 audit gates currently wired into the audit-programme" to "The 38 audit gates currently wired into the audit-programme". The spec's own §9 step 4 explicitly instructs "update the gate count in §2.1" when adding a gate, but PR #59 (gate 38 addition) and PR #61 (the cleanup pass) both missed this self-referential procedure. Document version `1.6.1 → 1.6.2`.
- [`governance/procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md): step 6 prose updated from "The full 37-gate audit programme" to "The full 38-gate audit programme". This procedure is a peer of the three governance registers PR #61 updated ([`register-coverage-gaps.md`](governance/register-coverage-gaps.md), [`register-main-branch-protection.md`](governance/register-main-branch-protection.md), [`register-document-index-and-classification.md`](governance/register-document-index-and-classification.md)) but was not in PR #61's scope; this PR closes the omission. Document version `1.0.4 → 1.0.5`; Date `2026-06-19 → 2026-06-20`.
- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): three See Also bullets had a leading space before the colon separator (` : ` instead of `: `), an artefact of PR #62's em-dash-to-colon `replace_all` retaining the original leading space. Sibling skills in the pack use `: ` uniformly. Also removed a redundant trailing "Library-specific canonical anchors" bullet from `## See Also`: the same anchors are already named in `## Overview` line 15, and no sibling skill in the pack carries a similar footer. Both are style consistency fixes; no behavioural change.

### Changed

- [`README.md`](README.md): library version `2026.06.48 → 2026.06.49`; README version `1.8.4 → 1.8.5`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit, run on the final state per the validation-sweep skill's step 7 (apply fixes, re-baseline, repeat). This is iteration 1 of the sweep cycle; the cycle terminated because the re-baseline reports no new High or Medium findings (Low / FYI items documented in the sweep report but not acted on, per the skill's triage rule). The gate-name parity audit (gate 35) confirms all four parity surfaces still declare 38 gates in identical order. The version-monotonicity audit (gate 13) accepts both per-document version bumps and the library-version bump. The version-date consistency audit (gate 29) confirms `2026.06.49` matches `2026-06`. The CHANGELOG link-coverage audit (gate 11) accepts the entry's path-shaped code spans. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

### Sweep findings not actioned (Low / FYI)

- The validation-sweep SKILL.md cites "gate 31 in the canonical inventory" at line 23. Verified accurate against §6 inventory (gate 31 is the document-staleness audit). Worth noting that embedded gate-number citations are brittle to future renumbering; left as-is since accurate, but a candidate for the Layer 2 gate-39 (cross-file gate-count consistency) audit to also flag inline gate-number cross-references.
- Four documents ([`NOTICE.md`](NOTICE.md), [`docs/adopter-guide.md`](docs/adopter-guide.md), [`dev-security/README.md`](dev-security/README.md), [`ai/standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md)) carry `Date: 2026-06-19` but were substantively committed today in earlier PRs (#54-#58); the document-Date-staleness audit (gate 31) accepts these within its 1-day tolerance window. Documented for future reference; not actioned this round.

---

## 2026-06-20, Library Version 2026.06.48, PR #62

Add the `validation-sweep` skill to the [`dev-security/claude-rules/`](dev-security/claude-rules/) pack: a corpus-wide regression sweep designed to run as a follow-up after any issue is identified and corrected, to confirm no sibling issue remains anywhere in the repository. The skill operationalises the worked example added to `evidence-grounded-completion` in PR #60 (and corrected in PR #61) at corpus scope: combines the mechanical audit suite ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) — the canonical 38-gate full-audit invocation) with a structured semantic fan-out across parallel subagents (recent-PR deep review, corpus-wide stale-reference sweep, audit-programme integrity check), and loops until the cycle returns clean.

The trigger pattern is the maintainer's stated use case: after any issue is identified, corrected, and then this is performed as a follow-up to ensure that there is nothing anywhere left that is wrong. The skill's fixed-point semantics catch the sibling-defect failure mode (same author, same session, same blind spot, multiple instances of the same shape of defect across the corpus) that this morning's three-PR sequence (PRs #59, #60, #61) demonstrated in practice.

This is Layer 1 of a three-layer validation programme. Layer 2 (new mechanical audit gates for the failure-mode classes the existing 38 gates do not cover — cross-file gate-count consistency, per-PR version-bump audit, and the maintainer-flagged collection-enumeration-consistency rule) will follow in subsequent PRs. Layer 3 (invocation-pattern documentation, including a project slash command pointing at this skill) closes the loop.

Pack version `1.24.3 → 1.25.0` (minor: new skill added, matching the precedent of pack 1.22.0 adding two skills). Library version `2026.06.47 → 2026.06.48`; README version `1.8.3 → 1.8.4` (patch: library-version-only bump).

### Added

- [`dev-security/claude-rules/skills/validation-sweep/SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md): new pack skill. Sections: Overview, When to Use, Process (seven steps: mechanical baseline, recent-change enumeration, failure-mode-class identification, parallel subagent fan-out, finding synthesis, triage, apply-fixes-and-loop), Red Flags, Verification, Common Rationalizations, See Also. Catalogues eight failure-mode classes the mechanical gates do not cover (stale prose references, mis-attributed citations, multi-surface incompleteness in non-gate-parity surfaces, inferred-as-verified state assertions, per-document version-bump omission, generated-artefact lag, stale docstrings, cross-document term drift) and the three baseline subagent briefs that target them. Derives from [`dev-security/claude-rules/governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md) (the pack's evidence-grounded-completion governance rule) per gate 32's derives-from audit; the skill is the corpus-scope wrapper of that rule's per-claim verification protocol. Three-iteration loop cap with escalation to the operator if the cycle does not converge.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.24.3 → 1.25.0`. Version-history table extended with a row for pack 1.25.0 / library 2026.06.48 / 2026-06-20 / "Added `skills/validation-sweep` — corpus-wide regression sweep as a follow-up after any issue identified and corrected; derives from `evidence-grounded-completion` and operationalises its worked example at corpus scope".
- [`README.md`](README.md): library version `2026.06.47 → 2026.06.48`; README version `1.8.3 → 1.8.4`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit, run on the final state per the discipline the skill itself encodes. Gate 32 (Skill derives-from reference audit) accepts the new skill's `derives_from` frontmatter pointing at the evidence-grounded-completion rule and confirms the referenced rule exists. The version-monotonicity audit (gate 13) accepts the library and pack version bumps. The version-date consistency audit (gate 29) confirms `2026.06.48` matches `2026-06`. The CHANGELOG link-coverage audit (gate 11) accepts the entry's path-shaped code spans. The taxonomy and portal in-sync gates (gates 33, 34) are regenerated and pass. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-20, Library Version 2026.06.47, PR #61

Cleanup pass after PR #59 and PR #60, surfaced by a recursive consistency review the maintainer requested before resuming Phase A work. Two failure shapes were found: (1) PR #60's worked example for `evidence-grounded-completion` mis-attributed the citing rule (claimed "step 4 of the verification protocol: when in doubt, re-run the verification standalone" — but step 4 is "Proactively search for contradictions", and the "when in doubt" phrasing is from the user-level Claude Code memory file's Rule 1.4 (outside this repository), not from the pack rule); (2) PR #59 added gate 38 to the §6 inventory and the four parity surfaces but missed seven downstream prose references in five files that still said "37 gates", and the spec's §5 categorisation was left without a slot for gate 38. The irony is that PR #60 shipped a worked example about exactly this multi-surface-omission failure mode and itself committed the mis-attribution variant of it.

Pack version `1.24.2 → 1.24.3` (patch: citation correction in the worked example; no behavioural change). Audit-programme spec `1.6.0 → 1.6.1` (patch: prose cleanup; §5 gate-38 categorisation, §6 partition narrative, §6.1 corpus count). Three governance registers carry patch bumps. Library version `2026.06.46 → 2026.06.47`; README version `1.8.2 → 1.8.3`.

### Fixed

- [`dev-security/claude-rules/governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md) (pack source) and [`.claude/rules/governance/evidence-grounded-completion.md`](.claude/rules/governance/evidence-grounded-completion.md) (mirror): the worked example's discipline-lesson paragraph re-cited to the pack rule's actual "Relying on prior runs" anti-pattern, replacing the incorrect "step 4 of the verification protocol — when in doubt, re-run the verification standalone" phrasing. The substantive lesson is unchanged; only the citation is corrected. Both files re-synced and verified byte-identical by gate 37.
- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md): §5 category 1 "Metadata integrity" gate list extended from `(gates 1, 7, 8, 13, 14, 15, 16, 19)` to `(gates 1, 7, 8, 13, 14, 15, 16, 19, 38)`; the prose enumeration for that category extended to include "section placement conventions (orientation sections in the top three `##` sections, Licence and Version-history sections in the bottom three)" before "version monotonicity". §6 partition narrative updated from "Gates 1 through 32 are pure read-only linters" to "Gates 1 through 32 and gate 38 are pure read-only linters", correctly grouping gate 38 with the other pure-linter gates rather than with the special-purpose meta-gates (33-37). §6.1 corpus count updated from `37-gate` to `38-gate`. Version `1.6.0 → 1.6.1`.
- [`tools/run_all_audits.sh`](tools/run_all_audits.sh): top-of-file comment "The current sweep is 37 gates" updated to "38 gates".
- [`tools/lint-audit-gate-parity.py`](tools/lint-audit-gate-parity.py): comment "of the 37-gate corpus inventory in §6" updated to "38-gate". This is the comment block explaining why the workflow's delta-gate steps are excluded from the parity audit's scope.
- [`tools/lint-section-placement.py`](tools/lint-section-placement.py): `normalise_heading` docstring updated from "prefix matching works against the human-facing section name" to "exact matching works against the human-facing section name", correcting a stale phrase from a pre-merge refactor (the linter uses exact `in frozenset(...)` matching, not prefix matching, as the main docstring already correctly describes).
- [`governance/register-main-branch-protection.md`](governance/register-main-branch-protection.md): two `37-gate` references and one `gates 1-37 still run` reference updated to `38-gate` and `gates 1-38 still run`. Document version `1.0.4 → 1.0.5`; Date `2026-06-19 → 2026-06-20`.
- [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md): `37 gates running in CI` updated to `38 gates running in CI`; the topic-coverage enumeration extended with "and section placement conventions" at its tail to match the new §5 enumeration. Document version `1.1.4 → 1.1.5`; Date `2026-06-19 → 2026-06-20`.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md): Audit Programme Specification row's Description updated from `Defines the 37-gate audit programme` to `Defines the 38-gate audit programme`. Document version `1.27.10 → 1.27.11`; Date `2026-06-19 → 2026-06-20`.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.24.2 → 1.24.3`. No structural changes.
- [`README.md`](README.md): library version `2026.06.46 → 2026.06.47`; README version `1.8.2 → 1.8.3`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit, run on the final state per the discipline this PR's predecessor (PR #60) meant to memorialise. The Claude-rules local-copy sync audit (gate 37) confirms the corrected worked example is byte-identical between pack source and local mirror. The gate-name parity audit (gate 35) confirms all four surfaces still declare 38 gates in the same order; only prose references and docstring text changed, not gate identities. The version-monotonicity audit (gate 13) accepts all five per-document version bumps and the library-version bump. The version-date consistency audit (gate 29) confirms `2026.06.47` matches `2026-06`. The CHANGELOG link-coverage audit (gate 11) accepts the entry's path-shaped code spans. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry. The PR #60 CHANGELOG entry was not retroactively edited (per the change-tracking rule's "retroactive entries" anti-pattern); the correction is documented here as a forward-looking record.

### Scope notes

The three subagent-driven sweeps (PR #59 + #60 deep review, corpus-wide stale-reference sweep, audit-programme integrity check) that surfaced these findings reported additional all-clear findings: audit-programme integrity intact (4 surfaces × 38 gates), mirror copies byte-identical, generated artefacts ([`taxonomy.yml`](taxonomy.yml), [`docs/portal.md`](docs/portal.md), [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md)) correctly regenerated by PR #59, no other stale version or date references outside CHANGELOG history, no em-dash leaks in recent additions. The recursive-review framing originated in the maintainer's request to verify the working tree before resuming Phase A backlog work; this PR closes the cleanup loop and clears the path to the Phase A items.

---

## 2026-06-20, Library Version 2026.06.46, PR #60

Memorialise the multi-surface gate-parity failure mode as a worked example in the `evidence-grounded-completion` governance rule. The rule already names the abstract failure (claiming a gate suite passes from inference rather than from running it on the final state); the worked example grounds the abstraction in the concrete shape it took in practice — a session wiring a new gate into N–1 of N parallel surfaces and prepping the work for the next operator without re-running the audit, with the gate-name-parity gate catching the omission when the next session ran the full audit. The lesson generalises beyond audit gates to any work that touches parallel surfaces (mirror-sync, generator-output drift, polyglot lockfiles, cross-package version registers).

Pack version `1.24.1 → 1.24.2` (patch: illustrative additive content in an existing rule; no behavioural change to the protocol). Library version `2026.06.45 → 2026.06.46`; README version `1.8.1 → 1.8.2` (patch: library-version-only bump).

### Changed

- [`dev-security/claude-rules/governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md): added a new `## Worked example: the multi-surface gate-name parity case` section between `## Framework alignment` and `## Why this rule exists`. The example describes the failure shape (omitted one of N parallel surfaces), the recovery (full audit on the final state catches it, one-block fix closes the loop), the discipline lesson (step 4 of the verification protocol — "when in doubt, re-run the verification standalone" — fires exactly when the session is not in doubt), and the wider generalisation to any multi-surface work. No edits to existing sections. Pack source.
- [`.claude/rules/governance/evidence-grounded-completion.md`](.claude/rules/governance/evidence-grounded-completion.md): mirror-synced from the pack source; identical body. The Claude-rules local-copy sync audit (gate 37) confirms parity with the pack source.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.24.1 → 1.24.2`; Date `2026-06-19 → 2026-06-20`. No structural changes; pack version-history table not amended (patch versions are aggregated; the table's row for the 1.24.x line stands at 1.24.0).
- [`README.md`](README.md): library version `2026.06.45 → 2026.06.46`; README version `1.8.1 → 1.8.2`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. The Claude-rules local-copy sync audit (gate 37) confirms the mirror at [`.claude/rules/governance/evidence-grounded-completion.md`](.claude/rules/governance/evidence-grounded-completion.md) is byte-identical to its pack source. The version-date consistency audit (gate 29) confirms `2026.06.46` matches `2026-06`; the library-version-monotonicity audit (gate 13) accepts the entry. The CHANGELOG link-coverage audit (gate 11) accepts the entry's path-shaped code spans (all wrapped as markdown links). The D1 CHANGELOG-on-PR delta gate is satisfied by this entry. No changes to document metadata that affect the machine-readable taxonomy or adopter-portal gates.

---

## 2026-06-20, Library Version 2026.06.45, PR #59

Add a new audit gate (#38) — the Section placement audit — that codifies two placement conventions a corpus-wide section-ordering survey found universally observed: orientation sections (Purpose, Scope, Overview, Applicability, Introduction, Executive Summary) must appear in the top three `##` sections, and Licence and Version-history sections must appear in the bottom three. The gate catches future drift mechanically without requiring per-doctype canonical-order codification. Library version `2026.06.44 → 2026.06.45`; audit-programme specification version `1.5.0 → 1.6.0` (minor bump: new gate added); README version `1.8.0 → 1.8.1` (patch: library-version-only bump).

### Added

- [`tools/lint-section-placement.py`](tools/lint-section-placement.py): new linter implementing rules SP-01 (orientation in top three `##` sections), SP-03 (version-history in bottom three), and SP-04 (licence in bottom three). Matching is case-insensitive and uses exact match against the normalised heading (with leading numbering, "Section N", and common punctuation stripped first) to avoid false positives on sections that legitimately reuse a canonical orientation or closing word in a different sense. Files with three or fewer `##` sections trivially satisfy the constraints.
- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md): gate 38 added to the §6 audit inventory table with the path link to its linter; §6 prose extended with a sentence explaining the rule scope and why the gate is appended (avoids renumbering the meta-gates above). Document version `1.5.0 → 1.6.0`.
- [`.github/workflows/quality.yml`](.github/workflows/quality.yml): new step "Section placement audit" added after the Claude-rules local-copy sync audit step, mirroring the gate ordering in [`tools/run_all_audits.sh`](tools/run_all_audits.sh).
- [`tools/run_all_audits.sh`](tools/run_all_audits.sh): new `run_gate` call for the Section placement audit appended after the Claude-rules local-copy sync audit, so the local runner declares the same 38 gates as the CI workflow.
- [`.pre-commit-config.yaml`](.pre-commit-config.yaml): new `lint-section-placement` hook appended after `lint-claude-rules-sync`, keeping the pre-commit surface in lockstep with the workflow and runner per the gate-parity discipline.
- [`tests/test_linters.py`](tests/test_linters.py): new `SectionPlacementTests` class with one regression fixture (`test_orientation_section_outside_top_three_flagged`) that constructs a synthetic markdown document where `Purpose` is the fifth of five `##` sections and asserts the linter exits non-zero. The fixture catches a regression in the linter's own SP-01 detection logic per the gate-36 contract.

### Changed

- [`README.md`](README.md): library version `2026.06.44 → 2026.06.45`; README version `1.8.0 → 1.8.1`; Date `2026-06-19 → 2026-06-20`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit, including the new gate 38 (Section placement audit) reporting OK against the current corpus and the gate-name parity audit (gate 35) confirming all four surfaces (workflow, runner, pre-commit, audit-programme spec) declare 38 gates in the same order. The linter regression test suite (gate 36) passes including the new `SectionPlacementTests` fixture. The metadata audit (gate 1) accepts the per-document Version and Date bumps on the spec and the README. The version-date consistency audit (gate 29) confirms `2026.06.45` matches `2026-06`; the library-version-monotonicity audit (gate 13) accepts the entry. The CHANGELOG link-coverage audit (gate 11) accepts the entry's path-shaped code spans (all wrapped as markdown links). The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-19, Library Version 2026.06.44, PR #58

Two coordinated cleanups in one PR: (1) move the root [`README.md`](README.md) "Licence and third-party reference boundary" section to the bottom of the file so it aligns with the placement convention every other README and the audit-programme survey found universal across the corpus; (2) update five places across the corpus where the external-rule-sources list still enumerated three names (TikiTribe, Wiz, Kariedo) instead of four (TikiTribe, Kariedo, addyosmani, Wiz). Library version `2026.06.43 → 2026.06.44`.

### Changed

- [`README.md`](README.md): moved `## Licence and third-party reference boundary` from line 80 (position 5 of 15 sections) to just above `## Maintained by` (position 14 of 15 sections), aligning with the universal "Licence section at the bottom" convention the section-ordering survey found across all other READMEs in the corpus. Section contents unchanged. Library version `2026.06.43 → 2026.06.44`; README version `1.7.181 → 1.8.0` (minor bump for structural section move).
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): Licence section's external-repositories list updated from "(TikiTribe, Wiz, Kariedo)" to "(TikiTribe, Kariedo, addyosmani, Wiz)" to match the four-source canonical set already enumerated in the `## External references` section earlier in the same file. Pack version `1.24.0 → 1.24.1` (patch: enumeration correction).
- [`dev-security/README.md`](dev-security/README.md): External-rule-repositories sentence updated from "(TikiTribe, Wiz, Kariedo)" plus "all three" to "(TikiTribe, Kariedo, addyosmani, Wiz)" plus "all four". Document version `1.4.0 → 1.4.1`.
- [`NOTICE.md`](NOTICE.md): setup-generator licence-surfacing list updated from "(TikiTribe, Wiz, Kariedo)" to "(TikiTribe, Kariedo, addyosmani, Wiz)". Document version `1.4.0 → 1.4.1`.
- [`ai/standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md): External-rule-repositories reference updated from "(TikiTribe, Wiz, Kariedo)" to "(TikiTribe, Kariedo, addyosmani, Wiz)". Document version `1.8.0 → 1.8.1`.
- [`dev-security/claude-rules/vetting-log.md`](dev-security/claude-rules/vetting-log.md): Adopter-facing example list of Vetted sources updated from "(Kariedo, TikiTribe, Wiz)" to "(Kariedo, TikiTribe, addyosmani, Wiz)" to match the actual vetted-source set. Document version `1.3.0 → 1.3.1`.

### Scope notes

The two places in the corpus that legitimately retain "the other three sources" phrasing ([`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) line 311 and [`dev-security/claude-rules/vetting-log.md`](dev-security/claude-rules/vetting-log.md) line 73) are both inside the addyosmani entry itself, contrasting addyosmani's Claude Code Skills discovery format with the rule / `@`-import patterns the other three sources use. These are correct as-is.

The omission of addyosmani from the five places fixed in this PR is the kind of enumeration-drift failure mode that the maintainer has flagged as a candidate for a mechanical lint rule (a "collection enumeration consistency" audit that would catch parenthetical enumerations of canonical collections missing one or more members). That rule is recorded as a future-work item to be designed after the in-flight section-placement validation (Option A from the section-ordering survey) lands.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. The structural section move in the root [`README.md`](README.md) is accepted by gates that check section presence (gate 19) and intra-document references (gate 18); the moved section does not break any internal anchor links because nothing else in the README linked to its old position. The metadata audit (gate 1) accepts the per-document Version and Date bumps on all six edited files. The version-date consistency audit (gate 29) confirms `2026.06.44` matches `2026-06`; the library-version-monotonicity audit (gate 13) accepts the entry. The CHANGELOG link-coverage audit (gate 11) accepts the entry's path-shaped code spans (all wrapped as markdown links). The taxonomy and portal in-sync gates (gates 33, 34) are regenerated and pass. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-19, Library Version 2026.06.43, PR #57

Restructure the [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) so the action-oriented content (scope, ways to use, directory structure, how to use, rule files) appears first and the historical reference content (per-version shipping log) appears near the bottom. The dense `## Pack scope` section that grew over many small additions is trimmed to the load-bearing content; the historical detail it carried (per-version shipping history, framing of the rollout's completion, enumeration of every skill that has ever shipped) is moved into a new compact `## Version history` table near the end of the README.

Pack version `1.23.0 → 1.24.0` (minor bump: prose restructure plus an additive new section). No structural changes to the pack's rules, skills, or directory layout; no audit-programme changes.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): trimmed `## Pack scope` from ~720 words to ~190 words by removing per-version shipping history, the historical "scope broadened" preamble, the enumeration of every skill that has ever shipped, and the directory-naming rationale paragraph; the section now carries only the two-category scope, the skills mention with the rule-vs-skill relationship, and the pack ↔ parent library relationship. Added a new `## Version history` section immediately before `## Licence` containing a compact table of pack version landings (12 rows covering 1.6.0 through 1.24.0, with the language-rule and skill-patch ranges compressed into single rows to keep the table glanceable). Pack version `1.23.0 → 1.24.0`.
- [`README.md`](README.md): library version `2026.06.42 → 2026.06.43`; README version `1.7.180 → 1.7.181`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. No structural changes; the reframe is prose-only. The metadata audit (gate 1) is unaffected because `dev-security/claude-rules/` is in its exempt-prefix set, but the pack README's per-document Version field is still bumped consistent with the substantive-content-change rule. The version-date consistency audit (gate 29) confirms `2026.06.43` matches `2026-06`; the library-version-monotonicity audit (gate 13) accepts the entry. The CHANGELOG link-coverage audit (gate 11) accepts the entry's path-shaped code spans (all wrapped as markdown links). The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-19, Library Version 2026.06.42, PR #56

Tidy the [`README.md`](README.md) Mode C ("Adopt the pack only") paragraph: add a one-click link to the AI-assisted installer and remove the inline search-terms sentence that has become redundant with the GitHub repository topics and the [`CITATION.cff`](CITATION.cff) keywords shipped in PR #55. Two prose edits to the same paragraph; no structural changes.

### Changed

- [`README.md`](README.md): added a sentence to the Mode C paragraph pointing readers to [`dev-security/claude-rules/setup-generator-prompt.md`](dev-security/claude-rules/setup-generator-prompt.md) for the automated installation path; removed the trailing "Common search terms that bring readers to this mode: ..." sentence (the discoverability function it served is now carried by the GitHub repository topics, the [`CITATION.cff`](CITATION.cff) keywords, and the GitHub repository description). Library version `2026.06.41 → 2026.06.42`; README version `1.7.179 → 1.7.180`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. The new link target exists; the repository-internal link audit (gate 3) accepts it. The version-date consistency audit (gate 29) confirms `2026.06.42` matches `2026-06`; the library-version-monotonicity audit (gate 13) accepts the entry. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-19, Library Version 2026.06.41, PR #55

Acknowledge the [`dev-security/claude-rules/`](dev-security/claude-rules/) pack across the project's attribution and contribution surfaces, and enrich [`CITATION.cff`](CITATION.cff) with pack-specific search-term keywords so the pack is discoverable to readers who arrive looking for Claude Code rules or skills rather than for GRC content. Continues the reframe shipped in PR #54 by ensuring the pack is named in the attribution surfaces, not only in the positioning prose. Prose-only across five files; no structural changes.

### Changed

- [`CITATION.cff`](CITATION.cff): extended the abstract to name the pack as a co-deliverable distilled from the library's own maintenance experience; extended the message to direct standalone-pack adopters to cite the parent library; added 14 search-term keywords covering both the pack itself and the security/GRC × Claude Code intersection (`Claude Code`, `Claude Code rules`, `Claude Code skills`, `Claude Code security rules`, `Claude Code GRC rules`, `Claude Code governance pack`, `claude-rules`, `Anthropic Claude`, `AI coding assistant`, `AI coding agent`, `AI-assisted development`, `secure AI coding`, `AI agent security rules`, `AI coding compliance`).
- [`AUTHORS.md`](AUTHORS.md): the "Original creator and maintainer" paragraph now names the pack alongside the library; the "Attribution posture" section gains a paragraph stating the pack is library-original under CC BY-SA 4.0 with no separate licence; the "How to cite" section gains a paragraph directing standalone-pack adopters (Mode C in [`docs/adopter-guide.md`](docs/adopter-guide.md)) to cite the parent library. Document version `1.0.0 → 1.1.0`.
- [`NOTICE.md`](NOTICE.md): the "Attribution" section gains a paragraph confirming the pack falls under the same CC BY-SA 4.0 terms as the corpus; the "Notes for adopters bringing in external content" section gains a paragraph distinguishing the pack's own content (library-original under CC BY-SA 4.0) from the third-party rule sources the pack's external overlay can fetch. Document version `1.3.0 → 1.4.0`.
- [`CONTRIBUTING.md`](CONTRIBUTING.md): added a contribution path for pack rules and Claude Code Skills to "What contributions are welcome", noting the existing pack disciplines (each new rule cites the maintenance event that justified it; each skill derives from a canonical pack rule via `derives_from` enforced by [`tools/lint-skill-derives-from.py`](tools/lint-skill-derives-from.py)). Document version `1.0.0 → 1.1.0`.
- [`README.md`](README.md): added a search-terms note to the Mode C "Adopt the pack only" paragraph, surfacing the common search terms (`Claude Code rules`, `Claude Code skills`, `Claude Code security rules`, `Claude Code GRC rules`, `Claude Code governance pack`, `claude-rules`, `AI coding assistant rules`, `AI agent security rules`, `Anthropic Claude governance`, `secure AI coding`) inline in the README's text so they are searchable in the file itself, not only in CITATION metadata. Library version `2026.06.40 → 2026.06.41`; README version `1.7.178 → 1.7.179`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. No structural changes; the reframe is prose-only across five files. The metadata audit (gate 1) accepts the per-document version and date bumps; the version-monotonicity audit (gate 13) accepts the entry; the version-date consistency audit (gate 29) confirms `2026.06.41` matches `2026-06`; the language audit (gate 2) accepts the new prose; the CHANGELOG link-coverage audit (gate 11) accepts the entry's path-shaped code spans; the taxonomy and portal in-sync gates (gates 33, 34) confirm no drift. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

### Out of scope (recorded for surfacing after merge)

Two discoverability levers require GitHub UI access and are not changed by this PR; the maintainer will action them after merge:

- **GitHub repository topics.** Recommended additions alongside the existing topics: `claude-code`, `claude-rules`, `claude-code-skills`, `claude-code-rules`, `ai-coding-assistant`, `anthropic-claude`, `governance-pack`. GitHub repository topics are the most effective single discoverability lever for the pack.
- **GitHub repository description.** Current description: *"A documentation library for governance, risk, compliance, cybersecurity, privacy, resilience, AI assurance, and operational control practices."* Recommended replacement: *"GRC documentation library + Claude Code rules-and-skills pack distilled from maintaining it (CC BY-SA 4.0)."*

---

## 2026-06-19, Library Version 2026.06.40, PR #54

Reframe the project's stated positioning to make explicit a dual-deliverable model that has been emerging across recent pack releases. The library is both (a) a CC BY-SA 4.0 GRC corpus and (b) a reference implementation showing how to maintain such a corpus with AI assistance, where the audit toolchain under [`tools/`](tools/) and the operational pack under [`dev-security/claude-rules/`](dev-security/claude-rules/) are the operational layer. The reframe also explicitly names a third, emergent adoption mode: the pack is usable as a standalone Claude Code baseline on any project regardless of whether it has a GRC corpus, distilled from the disciplines this library required to maintain itself. No structural changes; prose-only across six framing surfaces.

The reframe addresses an activity asymmetry observed in recent CHANGELOG entries: PRs #47-#53 were predominantly pack and meta-work while the GRC content backlog ([`TODO.md`](TODO.md) priorities 4-6) remained static, which initially read as drift from the library's "GRC" identity. The grounded position is that the pack and the audit toolchain are not drift but the operational half of a coordinated deliverable, with each governance rule in the pack provenance-linked to a real maintenance event in the parent library's CHANGELOG. The pack's standalone use case is recognised as supported alongside the primary fork-the-whole-repo adoption path.

### Changed

- [`README.md`](README.md): added a `## What this repository is` section after `## Purpose` that names the two-half deliverable (GRC corpus + reference implementation) and the three adoption modes (fork the whole repo; adopt the corpus only; adopt the pack only). Library version `2026.06.39 → 2026.06.40`; README version `1.7.177 → 1.7.178`.
- [`docs/adopter-guide.md`](docs/adopter-guide.md): added a `## Three adoption modes` section between `## How the library is meant to be used` and `## Quick start`. Each mode has Audience / What you take / What you ignore / Next step / (Mode C) Why this is supported. Document version `1.0.0 → 1.1.0`.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): replaced the stale closing sentence of `## Pack scope` (which deferred the directory-naming question with "If a future scope expansion outgrows this framing, the directory name will be revisited at that time, not pre-emptively") with a paragraph naming the pack as the library's lessons learned made portable, followed by a new `## Three ways to use this pack` section (inside the parent library / inside a fork / standalone on any project). Pack version `1.22.0 → 1.23.0` (minor bump, prose-additive).
- [`specification-master-project.md`](specification-master-project.md) §4.2: tightened the `dev-security/` cell in the domain-purpose table to acknowledge that `claude-rules/` within it is the operational pack distilled from the library's own maintenance disciplines, usable inside the library, in a fork, or as a standalone Claude Code baseline. Document version `1.5.0 → 1.5.1`.
- [`dev-security/README.md`](dev-security/README.md): expanded the `## Purpose` section to name the two layers within the domain (GRC standards as top-level files; the `claude-rules/` operational pack as a subdirectory with its own front door). Document version `1.3.2 → 1.4.0`.
- [`governance/charter-governance-library.md`](governance/charter-governance-library.md): added a paragraph to `## Purpose` acknowledging that the library also serves as a reference implementation for AI-assisted maintenance, while preserving the charter's normative focus on the corpus (the operational layer is named as an artefact of the corpus's own maintenance, not an additional authority claim). Document version `1.1.2 → 1.2.0`.

### Verification

Full audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. No structural changes were made; the reframe is prose-only across six framing surfaces. The metadata audit (gate 1) accepts the per-document version and date bumps; the version-monotonicity audit (gate 13) accepts the entry; the version-date consistency audit (gate 29) confirms `2026.06.40` matches `2026-06`; the language audit (gate 2) accepts the new prose; the CHANGELOG link-coverage audit (gate 11) accepts the entry's path-shaped code spans (all wrapped as markdown links); the taxonomy and portal in-sync gates (gates 33, 34) accept the regenerated outputs; the claude-rules sync audit (gate 37) is unaffected because the pack rule files were not edited. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-19, Library Version 2026.06.39, PR #53

Wrap the two remaining workflow-shaped governance rules as Claude Code Skills, closing out the post-S.3 evaluation that [`TODO.md`](TODO.md) recorded as deferred-until-trigger. Pack version `1.21.0 → 1.22.0` (minor bump, additive). The trigger condition (the next time the maintainer touched the skills pack) fired with PR #52; this PR acts on it by choosing the "Add both" outcome from the evaluation's possible outcomes.

The two new skills are [`dev-security/claude-rules/skills/change-tracking-write-entry/SKILL.md`](dev-security/claude-rules/skills/change-tracking-write-entry/SKILL.md), derived from [`dev-security/claude-rules/governance/change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md), and [`dev-security/claude-rules/skills/artefact-discipline-check/SKILL.md`](dev-security/claude-rules/skills/artefact-discipline-check/SKILL.md), derived from [`dev-security/claude-rules/governance/artefact-and-branch-discipline.md`](dev-security/claude-rules/governance/artefact-and-branch-discipline.md). Both follow the Phase S.3 / S.4 contract: the canonical rule remains the source of truth for normative content (framework alignment, exception handling, rationale); the skill is the workflow wrapper (when to invoke, what steps in what order, what verification confirms completion). The Skill derives-from reference audit ([`tools/lint-skill-derives-from.py`](tools/lint-skill-derives-from.py)) verifies the `derives_from` pointer.

### Added

- [`dev-security/claude-rules/skills/change-tracking-write-entry/SKILL.md`](dev-security/claude-rules/skills/change-tracking-write-entry/SKILL.md): the CHANGELOG entry-writing workflow. Process steps: classify the change (entry-required vs skip-trailer-permitted), choose the date and version, write the title sentence, pick the Keep a Changelog section, wrap every file reference as a markdown link, record the "why" not only the "what", attach verification evidence, add phase context, re-read once. Designed to satisfy the delta gate, the link-coverage gate, and the version-monotonicity audit in one pass rather than refining the entry through CI failures. Cross-links to [`gate-discipline-diagnose`](dev-security/claude-rules/skills/gate-discipline-diagnose/SKILL.md), [`evidence-grounded-completion`](dev-security/claude-rules/skills/evidence-grounded-completion/SKILL.md), and [`artefact-discipline-check`](dev-security/claude-rules/skills/artefact-discipline-check/SKILL.md).
- [`dev-security/claude-rules/skills/artefact-discipline-check/SKILL.md`](dev-security/claude-rules/skills/artefact-discipline-check/SKILL.md): the routing workflow that redirects a hand-edit of a generated file (or a protected-branch operation) to the correct path. Process steps: identify the trigger surface (generated artefact vs protected branch), classify the file or action, redirect to the source-and-regenerate workflow or to the PR mechanism, handle lockfiles via the package manager, follow the documented exception protocol when one is genuinely required. Cross-links to [`gate-discipline-diagnose`](dev-security/claude-rules/skills/gate-discipline-diagnose/SKILL.md), [`change-tracking-write-entry`](dev-security/claude-rules/skills/change-tracking-write-entry/SKILL.md), and [`action-before-explanation-of-inaction`](dev-security/claude-rules/skills/action-before-explanation-of-inaction/SKILL.md).

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.21.0 → 1.22.0`. Updated the directory-structure tree's `skills/` subtree to include the two new SKILL.md files; revised the skills paragraph to record that pack version 1.22.0 closes out the post-S.3 evaluation by wrapping the two remaining workflow-shaped governance rules.
- [`TODO.md`](TODO.md): removed the "Post-S.3 evaluation of the Claude Code Skills format" entry under "Pack and tooling extension". The evaluation's trigger condition fired with PR #52 (which touched the skills pack) and this PR acts on it by choosing the "Add both" outcome, so the entry is no longer pending. The completion is recorded here per the file's own maintenance note ("When an item is completed, remove it from this file and record the completion in [`CHANGELOG.md`](CHANGELOG.md)").
- [`README.md`](README.md): library version `2026.06.38 → 2026.06.39`; README version `1.7.176 → 1.7.177`.

### Verification

Full 37-gate audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. The Skill derives-from reference audit (gate 32) accepts both new skills' `derives_from` pointers, which resolve to [`dev-security/claude-rules/governance/change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) and [`dev-security/claude-rules/governance/artefact-and-branch-discipline.md`](dev-security/claude-rules/governance/artefact-and-branch-discipline.md) respectively. The language audit (gate 2) accepts the new files; em-dashes are absent per the project's prose convention. The metadata audit (gate 1) is unaffected because `dev-security/claude-rules/` is in its exempt-prefix set. The version-date consistency audit (gate 29) confirms `2026.06.39` matches `2026-06`; the library-version-monotonicity audit (gate 13) accepts the entry. The CHANGELOG link-coverage audit (gate 11) accepts the path-shaped code spans (all wrapped as markdown links). The claude-rules sync audit (gate 37) is unaffected (skills are not part of its mirror map; only rule files are). The taxonomy and portal in-sync gates (gates 33, 34) confirm no drift because the taxonomy builder does not scan `dev-security/claude-rules/` and the source `Date` aggregated by the portal generator is unchanged. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-19, Library Version 2026.06.38, PR #52

Add a sixth governance rule to the `dev-security/claude-rules/` pack: [`governance/action-before-explanation-of-inaction.md`](dev-security/claude-rules/governance/action-before-explanation-of-inaction.md), the pack-distributable form of the user-level Rule 8 added on 2026-06-19. The discipline: never explain why an external action cannot or will not proceed without first attempting it (when the action is safe and reversible) or naming it and asking (when it is destructive). The phased governance rollout announced at pack version 1.6.0 completed at 1.11.0 with the first five rules; this entry extends the set post-rollout after a recurring AI-coding-assistant failure mode was observed in production sessions (narrating a reason to wait — "the PR is blocked because it needs a reviewer" — instead of attempting the cheap, reversible action that would have produced a real result).

The rule ships alongside a Claude Code Skill mirror at [`dev-security/claude-rules/skills/action-before-explanation-of-inaction/SKILL.md`](dev-security/claude-rules/skills/action-before-explanation-of-inaction/SKILL.md), following the Phase S.3 pattern where each workflow-shaped governance rule has both a normative pack-rule statement and an invocable skill wrapper. The skill carries the reversibility-gate protocol as Process steps with the canonical rule named as the source of truth via the `derives_from` frontmatter; the Skill derives-from reference audit ([`tools/lint-skill-derives-from.py`](tools/lint-skill-derives-from.py)) verifies the pointer.

### Added

- [`dev-security/claude-rules/governance/action-before-explanation-of-inaction.md`](dev-security/claude-rules/governance/action-before-explanation-of-inaction.md): the new pack rule. Structure mirrors the sibling governance rules (opening framing, trigger surface, reversibility gate, safe-action and destructive-action protocols, execution-doubt-vs-decision-doubt boundary deferring authorial choices to [`clarify-before-acting.md`](dev-security/claude-rules/governance/clarify-before-acting.md), prohibited anti-patterns, tool-specific AI-coding-assistant guidance, exception-handling protocol, framework alignment table mapping to NIST SSDF RV.1 / PO.5 / RV.2, CSA CCM GRC-04 / GRC-05 / LOG-02, ISO 27001 A.5.4 / A.5.18 / A.5.36 / A.8.15, and OWASP ASVS V1.1 / V14.1, and a closing "why this rule exists" paragraph).
- [`dev-security/claude-rules/skills/action-before-explanation-of-inaction/SKILL.md`](dev-security/claude-rules/skills/action-before-explanation-of-inaction/SKILL.md): the Claude Code Skill wrapper. Frontmatter (`name`, `description`, `derives_from`) follows the pattern set by [`skills/evidence-grounded-completion/SKILL.md`](dev-security/claude-rules/skills/evidence-grounded-completion/SKILL.md). Body sections: Overview, When to Use (trigger phrases), Process (six-step protocol: identify-inaction-explanation → classify-reversibility → safe-action-attempt or destructive-action-naming → decision-doubt-cross-check → rewrite-draft), Red Flags, Verification, Common Rationalizations, See Also (cross-links to the canonical rule, [`clarify-before-acting`](dev-security/claude-rules/skills/clarify-before-acting/SKILL.md), [`evidence-grounded-completion`](dev-security/claude-rules/skills/evidence-grounded-completion/SKILL.md), [`gate-discipline-diagnose`](dev-security/claude-rules/skills/gate-discipline-diagnose/SKILL.md)).
- [`.claude/rules/governance/action-before-explanation-of-inaction.md`](.claude/rules/governance/action-before-explanation-of-inaction.md): the project-local mirror of the pack rule that Claude Code loads as session-start context. Body identical to the pack source per the claude-rules sync audit's contract.

### Changed

- [`tools/lint-claude-rules-sync.py`](tools/lint-claude-rules-sync.py): added the new mirror pair to `MIRROR_MAP`. Sync audit now tracks ten pairs instead of nine; the completeness check confirms every local rule file is mapped to a pack source.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.20.3 → 1.21.0` (minor bump, additive feature). Updated the directory-structure tree's `governance/` and `skills/` subtrees to include the new files; added a row for the new rule to the rule-files table; revised the pack-version paragraph to record that the originally-announced rollout completed at 1.11.0 and 1.21.0 extends the set as a post-rollout addition; revised the skills paragraph to include the new skill alongside the original three.
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md): added the new rule to the Development-governance discipline rule list with a one-paragraph summary; revised the closing sentence so the count is no longer fixed at "five" and to note the 1.21.0 post-rollout extension.
- [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md): added the new rule to the Security and governance requirements list with a project-tailored description (links the discipline to the project's `## PR workflow` section, where the merge of a green PR via MCP is the canonical safe action that this rule says to attempt rather than narrate as "blocked"); revised the closing pack-history paragraph so the count is no longer fixed at "five" and to record the 1.21.0 extension.
- [`README.md`](README.md): library version `2026.06.37 → 2026.06.38`; README version `1.7.175 → 1.7.176`.

### Verification

Full 37-gate audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. The claude-rules sync audit (gate 37) accepts the new mirror pair; the Skill derives-from reference audit (gate 32) accepts the new skill's `derives_from` pointer to the new pack rule; the metadata audit (gate 1) is unaffected because `dev-security/claude-rules/` is in its exempt-prefix set; the version-date consistency audit (gate 29) confirms `2026.06.38` matches `2026-06`; the library-version-monotonicity audit (gate 13) accepts the entry; the CHANGELOG link-coverage audit (gate 11) accepts the path-shaped code spans (all wrapped as markdown links). The taxonomy and portal in-sync gates (gates 33, 34) confirm no drift because the taxonomy builder does not scan `dev-security/claude-rules/` and the source `Date` aggregated by the portal generator is unchanged. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-19, Library Version 2026.06.37, PR #50

Make every file under `docs/` carry the canonical 13-field metadata block, so the `docs/` tree is governed by the same audit programme as the rest of the corpus rather than carved out as a partial exemption with a per-file allowlist. Two hand-authored reference documents are promoted from informational aids to controlled artefacts; the two generator outputs ([`docs/portal.md`](docs/portal.md) and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md)) acquire metadata emitted by the generator itself. The previous mechanism, a `docs/` directory exemption in [`tools/lint-metadata.py`](tools/lint-metadata.py) with a `FORCE_INCLUDE_PATHS` carve-out for [`docs/worked-example.md`](docs/worked-example.md), is retired in favour of uniform enforcement.

### Changed

- [`docs/adopter-guide.md`](docs/adopter-guide.md): added the 13-field metadata block (Document Type Guide, Version `1.0.0`, owner and approving authority Governance Library Maintainer, Category Documentation); added an `## Overview` orientation section (required for the Guide doctype by the required-sections audit); and corrected the former self-declaration "not part of the library's controlled artefact set", which the promotion makes false.
- [`docs/decision-tree.md`](docs/decision-tree.md): same treatment, Document Type Guide, Version `1.0.0`; added `## Overview`; corrected the former "informational and is not a tracked governance artefact" self-declaration.
- [`tools/build-portal.py`](tools/build-portal.py): the generator now emits a 13-field metadata block above the existing body for both outputs. [`docs/portal.md`](docs/portal.md) is classified as a Guide; [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md) is classified as a Register. The block's `Version` is a generator-side schema constant (`PORTAL_METADATA_VERSION` / `SCORECARD_METADATA_VERSION`, both initialised to `1.0.0`), bumped manually when the metadata schema itself changes; this keeps the generator-output drift gates (33 and 34) deterministic and prevents the per-PR version flap that "Version equals library CalVer" would induce. The block's `Date` is the maximum source `Date` across [`taxonomy.yml`](taxonomy.yml) entries, so the field advances with the corpus without requiring hand bumps. Each emitted block carries the CommonMark backslash-newline hard-break markers required by the line-break audit. Both generated files acquire an `## Overview` heading wrapping their existing intro paragraphs, satisfying the orientation-section requirement that the new doctypes pull in via gate 19.
- [`tools/lint-metadata.py`](tools/lint-metadata.py): removed `"docs/"` from `EXEMPT_PREFIXES`; deleted the `FORCE_INCLUDE_PATHS` set in its entirety (the carve-out it provided is now redundant); added the basenames of [`docs/portal.md`](docs/portal.md) and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md) to `PREFIX_EXEMPT_BASENAMES` (their filenames do not follow the `guide-` or `register-` doctype prefix, matching the existing treatment of the other three `docs/` files); added `"docs"` to the linter's default scan paths so the new enforcement runs under the default invocation rather than only when the path is named explicitly.
- [`docs/portal.md`](docs/portal.md) and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md): regenerated. Both now carry the metadata block and the `## Overview` heading the generator emits.

### Scope notes

`docs/` remains exempt from the standards-currency audit (gate 6) and from the filename-title alignment audit (gate 7) by their own directory-prefix lists in [`tools/lint-standards-currency.py`](tools/lint-standards-currency.py) and [`tools/lint-filename-title-alignment.py`](tools/lint-filename-title-alignment.py); those exemptions exist for separate reasons (no normative citations in the navigation pages; the controlled-artefact filename convention does not apply to user-facing portal/scorecard names) and are unaffected here. [`docs/portal.md`](docs/portal.md) and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md) likewise remain in the `EXEMPT_FILES` set of [`tools/lint-document-date-staleness.py`](tools/lint-document-date-staleness.py): their `Date` is set by the generator from taxonomy state, not by the most-recent commit to the generated file, and the staleness check would otherwise false-positive when the generator runs without a fresh source bump.

The two promoted documents continue to be absent from [`taxonomy.yml`](taxonomy.yml) and the document-index register, consistent with the existing controlled-artefact precedent in [`docs/worked-example.md`](docs/worked-example.md): the taxonomy builder does not scan `docs/`, and the worked example is likewise absent from both, so no generated-artefact regeneration outside the portal/scorecard pair is required for this change.

### Verification

Full 37-gate audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. The metadata audit (gate 1) now enforces and accepts the full 13-field block on all five `docs/` markdown files. The metadata-block line-break audit (gate 30) accepts the backslash-newline markers the generator emits. The required-sections audit (gate 19), which scans the whole repository and now sees a Document Type on all four newly-enforced files, accepts the `## Overview` orientation sections. The filename-title alignment audit (gate 7) and the standards-currency audit (gate 6) are unaffected, as documented above. The orphan-documents audit (gate 26) is satisfied because all four documents have inbound references (the adopter guide and decision tree from the root [`README.md`](README.md), the worked example, and each other; the portal from the root [`README.md`](README.md) and the scorecard from [`docs/portal.md`](docs/portal.md)). The taxonomy and portal in-sync gates (gates 33, 34) confirm no drift between the generator output and the regenerated files. The version-date consistency audit (gate 29) confirms `2026.06.37` matches `2026-06`. The library version monotonicity audit (gate 13) accepts the entry. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-19, Library Version 2026.06.36, PR #49

Agent-production-authority controls, part C of three: operational closure. Completes the set begun in PR #47 (core control and evidence home) and PR #48 (governance integration). This part connects a harmful or unauthorised agent action to its reversal in incident response, and records the agentic standard in the cross-framework alignment matrix.

### Changed

- [`ai/plan-ai-incident-response.md`](ai/plan-ai-incident-response.md): the Eradicate phase gains an action to invoke the reversal or compensating transaction for agent-performed production actions and confirm the affected system returned to an equivalent prior state, triggered when an agent performed unauthorised, harmful, or out-of-scope production actions (per `AGENT-PROD-02`). The Evidence requirements gain an "Action lineage and reversal record" class capturing the trigger-to-resulting-change lineage (`AGENT-PROD-04`) and the reversal record where one was invoked. This closes the loop the plan previously left open: its Recover phase restored the AI system but did not reverse the agent's downstream production effects. Version `1.0.1 → 1.0.2`.
- [`governance/matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md): a new artefact row for the AI and Agentic Development Security Standard (previously absent from the matrix), mapping it to OWASP LLM Top 10 (excessive agency), MITRE ATLAS, CSA AICM agentic and autonomy domains, NIST AI RMF, and ISO/IEC 42001 operational families, with the evidence class naming the agent threat model, tool allow-list, reversibility classification, recovery-test result, production-authority evidence record, and immutable audit trail. Version `1.1.2 → 1.1.3`.
- Auto-generated artefacts regenerated for the two version bumps: [`taxonomy.yml`](taxonomy.yml) and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md).
- [`README.md`](README.md): library version `2026.06.35 → 2026.06.36`; README version `1.7.173 → 1.7.174`.

### Set complete

With this PR the three-part agent-production-authority set from the agentic-governance assessment is complete: PR #47 (core control `AGENT-PROD-01..06`, the `§21` recovery-test gate, access-standard wiring, template evidence fields), PR #48 (acceptance-into-service criterion, AI-governance-framework anchor, role-authority accountability), and PR #49 (incident-response reversal step and evidence class, cross-framework matrix row). The principle is now expressed at the framework tier, enforced at the acceptance-into-service gate, carried by mandatory controls in the agentic standard, recorded in an audit-grade evidence artefact in the AI System Register and system card, owned by a named accountable human in the authority register, and closed operationally by an incident-response reversal path.

### Verification

Full 37-gate audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. Gate 2 (language) passes on both edited documents (no em-dashes or en-dashes introduced). The taxonomy and portal in-sync gates (gates 33, 34) confirm the regenerated artefacts match the two bumped source metadata blocks. The version-monotonicity audit (gate 13) confirms each per-document bump and `2026.06.35 → 2026.06.36`. The version-date consistency audit (gate 29) confirms `2026.06.36` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-19, Library Version 2026.06.35, PR #48

Agent-production-authority controls, part B of three: governance integration. Part A (PR #47) placed the `AGENT-PROD-01` to `AGENT-PROD-06` controls and their evidence home; this part wires the production-authority precondition into the acceptance-into-service gate, anchors it at the AI-governance framework tier, and binds the standing accountability to a named role. No new control language is introduced; each edit references the `AGENT-PROD-*` controls from part A so the gate is enforced at the formal acceptance decision, named in the framework that governs AI approval, and owned by an accountable human in the authority register.

### Changed

- [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](dev-security/standard-software-evaluation-acceptance-and-lifecycle.md): §3 (Acceptance and approval for use) gains an Acceptance-Into-Service checklist item: for systems with an action-capable AI agent, acceptance is withheld until the agent production-authority precondition (`AGENT-PROD-01`) is satisfied and evidenced, including tested reversibility or compensating-transaction mechanisms. This closes the "deploy first, design rollback later" failure mode at the formal gate. Version `1.0.1 → 1.0.2`; Related Documents extended with the agentic standard.
- [`ai/framework-ai-governance-and-risk.md`](ai/framework-ai-governance-and-risk.md): the Human Oversight control domain now states that, for systems with production action capability, approval additionally requires the four-property production-authority precondition, and that authority resides in the system boundary and the accountable human rather than in the agent. This anchors the standard-level controls at the governing framework tier. Version `1.1.1 → 1.1.2`; Related Documents extended with the agentic standard.
- [`governance/register-role-authority.md`](governance/register-role-authority.md): the System Owner row now records that, for an action-capable AI agent, the System Owner (or a designated AI System Owner) is the named accountable owner of the agent's autonomous envelope, and that accountability does not transfer to the agent (`AGENT-PROD-05`). Version `1.3.0 → 1.3.1`.
- Auto-generated artefacts regenerated for the three version bumps: [`taxonomy.yml`](taxonomy.yml) and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md).
- [`README.md`](README.md): library version `2026.06.34 → 2026.06.35`; README version `1.7.172 → 1.7.173`.

### Part C still to come

Part C (operational closure) follows as a separate PR: an AI incident response reversal/compensating-transaction step (so a harmful agent action is undone, not only the AI system restored), and a cross-framework matrix artefact row for the agentic standard.

### Verification

Full 37-gate audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. Gate 2 (language) passes on the three edited documents (no em-dashes or en-dashes introduced). Gate 3 (links) and gates 17/18 (section-anchor and intra-doc references) pass on the new cross-references. The taxonomy and portal in-sync gates (gates 33, 34) confirm the regenerated artefacts match the three bumped source metadata blocks. The version-monotonicity audit (gate 13) confirms each per-document bump and `2026.06.34 → 2026.06.35`. The version-date consistency audit (gate 29) confirms `2026.06.35` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-19, Library Version 2026.06.34, PR #47

Agent-production-authority controls, part A of the three-part set from the agentic-governance assessment: the core control, its evidence home, and the access-standard wiring. The governing principle is that autonomous agents do not receive production authority until reversibility, auditability, accountability, and permission boundaries are designed, tested, and governed; authority sits in the system boundary, the permissions model, the approval path, the immutable audit trail, the reversal mechanism, and a named accountable human, never in the agent. This closes the assessment's identified gap: the corpus treated reversibility as a classification input to an approval decision, not as a designed-and-tested precondition for production authority, and it did not consolidate the four properties into a single gate wired to acceptance-into-service.

### Added

- New section **§35 "Agent production authority, reversibility, and recovery"** in [`ai/standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md), with six mandatory controls `AGENT-PROD-01` to `AGENT-PROD-06`: the production-authority precondition (the four properties designed, tested, and governed before autonomous or semi-autonomous execution, verified at the acceptance-into-service gate); reversibility classification (Reversible / Compensable / Irreversible) with reversal or compensating-transaction design; recovery testing of the reversal mechanism before go-live; end-to-end action lineage from trigger to resulting data change; standing named human accountability that does not transfer to the agent; and a production-authority evidence record for audit and risk acceptance. The section is explicitly scoped to action-capable agents and explicitly does not raise the bar for passive assistance, decision support, or read-only capability, keeping the four-tier distinction (passive / decision support / semi-autonomous / autonomous) clear.
- New pre-production gate item in §21: a recovery test that exercises the reversal or compensating mechanism for each Reversible or Compensable action class (`AGENT-PROD-03`).
- Four conditional fields in [`ai/template-ai-system-register.md`](ai/template-ai-system-register.md) (Reversibility Classification, Recovery Test Status, Production Action Authority, Action Lineage Coverage) and three in [`ai/template-system-card.md`](ai/template-system-card.md) (Action Lineage Coverage in §4; Reversibility Classification and Reversal and Recovery Testing in §5; Production Action Authority in §9), giving the `AGENT-PROD-06` evidence record a concrete home.

### Changed

- [`ai/standard-ai-access-and-agent-permissions.md`](ai/standard-ai-access-and-agent-permissions.md): the §4.1 tool-definition row now requires a reversibility classification per `AGENT-PROD-02` (replacing the optional "rollback behaviour where applicable"); §4.2 now conditions the grant of Operational and Cross-system scope on the production-authority precondition (`AGENT-PROD-01`), with Bounded read-only scope exempt. Version `0.0.2 → 0.0.3`.
- [`ai/standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md): version `1.7.0 → 1.8.0` (minor, material new section); date `2026-05-30 → 2026-06-19`; Related Documents extended with the access-permissions standard, the AI governance framework, the acceptance-and-lifecycle standard, and the two templates.
- [`ai/template-ai-system-register.md`](ai/template-ai-system-register.md) and [`ai/template-system-card.md`](ai/template-system-card.md): version `1.0.0 → 1.1.0` each; date `2026-05-27 → 2026-06-19`.
- Auto-generated artefacts regenerated for the four version bumps: [`taxonomy.yml`](taxonomy.yml) and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md).
- [`README.md`](README.md): library version `2026.06.33 → 2026.06.34`; README version `1.7.171 → 1.7.172`.

### Scope and non-duplication

The control IDs use the `AGENT-PROD-` prefix, consistent with the standard's existing `AGENT-SEC-` / `AUTON-SEC-` convention. No framework-alignment table row was added: §35's alignment (OWASP LLM06 excessive agency, CSA AICM AI-AU-01 to 06, NIST AI RMF MANAGE 1.3) is already represented by the standard's existing "Excessive agency" row, and adding a near-duplicate would duplicate rather than clarify. The reversibility and recovery controls are deliberately distinct from the deployment-level rollback controls in the DevOps and acceptance-and-lifecycle standards: this is per-action reversal and compensating-transaction design, a layer above deployment rollback, and it references rather than restates the existing human-approval boundaries (§24), autonomous-action constraints (§30), and immutable-logging requirements (§28).

### Part B and part C still to come

Part B (governance integration: acceptance-and-lifecycle acceptance criterion, AI governance framework anchor, role-authority accountability line) and part C (operational closure: AI incident response reversal step, cross-framework matrix artefact row) follow as separate PRs. They reference the `AGENT-PROD-*` controls this PR places on `main`.

### Verification

Full 37-gate audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. Gate 2 (language) passes on the four edited `/ai` documents (in scope; no em-dashes or en-dashes introduced). Gate 1 (metadata), gate 17/18 (section-anchor and intra-doc references), and gate 3 (links) pass on the new section and its cross-references. The taxonomy and portal in-sync gates (gates 33, 34) confirm the regenerated artefacts match the four bumped source metadata blocks. The version-monotonicity audit (gate 13) confirms each per-document bump and the `2026.06.33 → 2026.06.34` library bump are strictly increasing. The version-date consistency audit (gate 29) confirms `2026.06.34` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-19, Library Version 2026.06.33, PR #46

Consistency follow-up to PR #45: broaden the summary surfaces that describe the evidence-grounded-completion rule, so they match the rule's scope after PR #45 extended it from completion claims to any state assertion. PR #45 deliberately left these surfaces untouched on the reasoning that each named the rule by its primary purpose and "remained accurate"; a subsequent read (prompted by the maintainer's "always confirm" instruction) showed that reasoning was an unverified inference that did not fully hold. Specifically, the pack's distributable governance instruction file made an explicit trigger claim ("the vocabulary of completion is a flag that the protocol must precede") that the broadened rule outgrew, and the project instruction file linked the rule only to user-level Rule 6 when a user-level Rule 7 now also exists. This PR corrects the surfaces that made trigger or linkage claims and broadens the lossy summaries for consistency.

### Changed

- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md): the evidence-grounded-completion bullet now states that the protocol must precede both the vocabulary of completion and any state assertion about an unread artefact (research, assessment, planning, or review), rather than naming completion as the sole flag.
- [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md): the project's security-and-governance bullet for the rule broadened to include unread-artefact state assertions, and its provenance updated from "user-level Rule 6" to "user-level Rules 6 and 7" to reflect the cross-project clause added alongside PR #45.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): the Pack-scope paragraph and the two directory-tree annotations (the rule and its skill) broadened from "completion claim" to "completion claim or unread-artefact state assertion"; pack version `1.20.2 → 1.20.3`.
- [`README.md`](README.md): library version `2026.06.32 → 2026.06.33`; README version `1.7.170 → 1.7.171`.

### Why this is a separate PR and what it demonstrates

PR #45 changed the canonical rule; this PR aligns its descriptions. They are separated because the canonical change is the substantive one and the summary alignment is consistency maintenance. The finding itself is an instance of the discipline PR #45 codified: the PR #45 decision to skip these surfaces rested on an inference ("they remain accurate") made without reading them; reading them showed the inference was partly wrong. The corrected behaviour is to confirm by reading, which is what produced this PR.

### Verification

Full 37-gate audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. Gate 2 (language and style) passes on the edited pack instruction file and pack readme, which are in scope for that linter (no em-dashes or en-dashes introduced); the project instruction file under the AI-assistant config tree is exempt from the corpus linters and retains its existing punctuation style. None of the edited files participate in the gate-37 claude-rules sync map (they are instruction and readme files, not rule files), so no mirror sync applies. The version-date consistency audit (gate 29) confirms `2026.06.33` matches `2026-06`. The library-version-monotonicity audit (gate 13) confirms `2026.06.32 → 2026.06.33` and the pack `1.20.2 → 1.20.3` are strictly increasing. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-19, Library Version 2026.06.32, PR #45

Extend the [`evidence-grounded-completion`](dev-security/claude-rules/governance/evidence-grounded-completion.md) pack rule from "evidence before completion claims" to "evidence before any state assertion." A session failure prompted this: during a governance assessment the assistant asserted that two templates "need new fields" and that a cross-framework matrix "needs control mappings" without having read those files; a later read confirmed the templates but showed the matrix operated at a different granularity than asserted. The existing rule did not fire because these were mid-analysis state assertions, not completion claims ("done", "fixed", "ready"). The rule's machinery (read, quote, contradiction-search, label-the-unverified) was already the right discipline; only its stated trigger was too narrow.

The change is deliberately scoped to the rule and its consumers; it does not attempt to restate the discipline across every summary surface (the rule's title and the pack summaries name it by its primary purpose, completion claims, which remains accurate). The canonical rule carries the broadened scope.

### Added

- New section **"Beyond completion: claims about artefact state"** in [`dev-security/claude-rules/governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md), placed between "What counts as a completion claim" and "The verification protocol". It defines a state assertion (a claim about what an artefact contains, lacks, or requires), states that such a claim requires a read rather than an inference, and gives the four-point discipline: read before characterising; label hypotheses explicitly; separate findings from hypotheses in analysis; own a caught inference plainly.
- New bullet in the rule's "Prohibited anti-patterns" section: **"Characterising an artefact you have not opened"** — asserting contents, gaps, or requirements by inference rather than by reading, explicitly noting the anti-pattern fires in analysis and assessment, not only at completion.
- New "When to Use" trigger and a description-line addition in [`dev-security/claude-rules/skills/evidence-grounded-completion/SKILL.md`](dev-security/claude-rules/skills/evidence-grounded-completion/SKILL.md) so the skill surfaces for state assertions in research, assessment, planning, or review, not only for completion claims.

### Changed

- [`.claude/rules/governance/evidence-grounded-completion.md`](.claude/rules/governance/evidence-grounded-completion.md) re-synced from the pack source (the project-local copy a session loads as context). Gate 37 (claude-rules local-copy sync) enforces byte-identity of the rule body, so the extension propagates to the loaded copy by construction; this is the drift class gate 37 was built to prevent.
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md): pack version `1.20.1 → 1.20.2`. Patch, consistent with the prior precedent (`1.20.0 → 1.20.1`) for adding a subsection to an existing rule: no new rule files, no structural change to the pack's content shape.
- [`README.md`](README.md): library version `2026.06.31 → 2026.06.32`; README version `1.7.169 → 1.7.170`.

### Relationship to the user-level rule layer

This pack rule is the dogfooded, distributable home for the discipline. A parallel cross-project clause was added to the maintainer's user-level Claude Code rules (outside this repository) so the same discipline applies to the assistant's behaviour across all projects, not only this one. The two layers are complementary: the pack rule ships with the corpus and binds any project that adopts it; the user-level rule binds the assistant regardless of project.

### Why this is a rule and not a lint

The failure occurs in session reasoning (a chat assertion about an unread file), not in a committed artefact, so no corpus linter can detect it: a lint scans committed files, and the false assertion was never committed. The decidable subset of "assertion versus reality" is already gated (link existence, citation currency, internal references, version monotonicity, gate-name parity, claude-rules sync); this class is not mechanically decidable and its home is therefore a behavioural rule loaded as context, not a gate. This is mitigation, not a guarantee.

### Verification

Full 37-gate audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. Gate 37 (claude-rules local-copy sync) confirms the rule source and its `.claude/` mirror are byte-identical after the edit. Gate 2 (language and style) passes on the edited rule, which is in scope for that linter (no em-dashes or en-dashes introduced). Gate 32 (skill derives-from) confirms the skill's `derives_from` still resolves. The version-date consistency audit (gate 29) confirms `2026.06.32` matches `2026-06`. The library-version-monotonicity audit (gate 13) confirms `2026.06.31 → 2026.06.32` and the pack `1.20.1 → 1.20.2` are strictly increasing. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-19, Library Version 2026.06.31, PR #44

New audit gate (gate 37), **Claude-rules local-copy sync audit**, closing the systemic drift class the regression audit identified. The project keeps copies of a subset of the [`dev-security/claude-rules/`](dev-security/claude-rules/) pack under `.claude/rules/` so a Claude Code session loads them as context. Both trees are exempt from the corpus linters, so until now nothing caught a local copy drifting from its pack source — the exact gap that let the evidence-grounded-completion local copy fall out of sync (fixed manually in PR #41) and would have re-opened on the next pack edit. This gate makes that drift class mechanically detectable.

### Added

- New audit gate 37, **Claude-rules local-copy sync audit**, implemented by [`tools/lint-claude-rules-sync.py`](tools/lint-claude-rules-sync.py). For each declared (local copy, pack source) pair it compares the two files' bodies after stripping the local copy's by-design additions — a leading YAML frontmatter block (the path-scoping `paths:` block on the path-scoped copies) and a leading HTML provenance comment — and fails on any body divergence. It additionally enforces a **completeness check**: every markdown file under `.claude/rules/` other than the local-only `external/` overlay must appear in the linter's source mapping, so a future un-mapped mirror fails the gate rather than going silently unchecked. This is the property that prevents the drift class recurring one level up. The audit accepts a `--root` override for the regression suite. Exit codes: 0 pass, 1 findings (body drift or unmapped file), 2 internal error (a mapped file is missing).
- New regression test class `ClaudeRulesSyncTests` in [`tests/test_linters.py`](tests/test_linters.py): the live in-sync state passes (subprocess); an in-sync pair carrying a local provenance comment passes; genuine body drift between copy and source is flagged; and an unmapped local rule file fails the completeness check. The drift and completeness tests drive the linter in-process with a patched mapping against a synthetic root so the detection logic is exercised without perturbing the real tree.

### Changed

- Audit programme grows from 36 to 37 gates. The new gate is **appended** as gate 37 (not inserted), so no existing gate renumbers — gate 35 (parity) and gate 36 (regression suite) keep their numbers, and the inline `gate-36 regression test suite` references in the linter sources and [`tests/README.md`](tests/README.md) are untouched. This deliberately avoids the renumber churn that, in this session's earlier work, was the dominant source of stale gate-number references. The gate is logically a drift check akin to the generator-output in-sync gates (33, 34) but is placed last for that reason; the §6 narrative documents the rationale.
- All four CI surfaces wired to invoke the new gate after the regression suite: [`.github/workflows/quality.yml`](.github/workflows/quality.yml) (new step); [`tools/run_all_audits.sh`](tools/run_all_audits.sh) (new `run_gate`; header sweep count `36 → 37`); [`.pre-commit-config.yaml`](.pre-commit-config.yaml) (new hook `lint-claude-rules-sync`); [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) §6 (new row 37). The gate-name parity audit (gate 35) confirms the four surfaces agree on the 37-gate set.
- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md): version `1.4.0 → 1.5.0`; date stays `2026-06-19`. Minor (material): §5 category 5 extended to include gate 37, §6 inventory grew a row, §6 post-table narrative gained a paragraph for gate 37, §6.1 corpus-count `36 → 37` (the parity gate reference stays gate 35).
- Gate-count text `36 → 37` updated in the four governance documents that cite it, each with a per-document version bump: [`governance/procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md) (`1.0.3 → 1.0.4`); [`governance/register-main-branch-protection.md`](governance/register-main-branch-protection.md) (`1.0.3 → 1.0.4`, including the `gates 1-36 → 1-37` run-range); [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md) (`1.1.3 → 1.1.4`, audit-coverage list gains "claude-rules local-copy sync"); [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) (`1.27.9 → 1.27.10`). The docstring count in [`tools/lint-audit-gate-parity.py`](tools/lint-audit-gate-parity.py) updated `36 → 37`.
- Auto-generated artefacts regenerated for the five governance version bumps: [`taxonomy.yml`](taxonomy.yml) and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md).
- [`README.md`](README.md): library version `2026.06.30 → 2026.06.31`; README version `1.7.168 → 1.7.169`.

### Why append rather than insert

Every gate renumber in this session's earlier work left stale gate-number references behind (corrected across PRs #39, #40, #42). Inserting the new gate among the drift checks (its logical home) would have renumbered the parity and regression gates and re-churned the 10 inline `gate-36` references plus several docs. Appending touches zero existing gate numbers; only the total count (`36 → 37`) changes. Given the regression-audit context, minimising renumber surface was the higher priority; the §6 narrative records that the gate is logically a drift check placed last for this reason.

### Verification

Full 37-gate audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit, with the new gate 37 reporting all nine local rule copies in sync and every local rule file mapped. The four new `ClaudeRulesSyncTests` pass standalone and via the linter regression test suite gate. The gate-name parity audit (gate 35) confirms all four surfaces agree on the 37-gate name set and order. The version-monotonicity audit (gate 13) confirms the five per-document version bumps and the `2026.06.30 → 2026.06.31` library bump are all strictly increasing. The version-date consistency audit (gate 29) confirms `2026.06.31` matches `2026-06`. The taxonomy and portal in-sync gates (gates 33, 34) confirm the regenerated artefacts match the bumped source metadata. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

### Regression-audit close-out

This completes the regression audit's remediation. The systemic finding (no mechanical check that the `.claude/rules/` copies track their pack sources) is now closed by gate 37; the per-instance findings were closed by PRs #39 (TODO.md stale gate/pack refs), #40 (run-linter-regression.py docstring), #41 (evidence-grounded-completion re-sync), #42 ([[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md) gate count), and #43 (gate-21 private-key detection hardening). The four `.claude/rules/` local copies the audit flagged as divergent (`secrets`, `python`, `input-validation`, `cicd-gates`) were assessed: three (`python`, `input-validation`, `cicd-gates`) carry only by-design local additions (path-scoping frontmatter, provenance comment) with identical bodies and are correct as-is; the fourth (`secrets`) had a genuine body divergence in the private-key example, resolved in PR #43. Gate 37 now holds all nine local copies to their sources going forward.

---

## 2026-06-19, Library Version 2026.06.30, PR #43

Security fix: harden the gate-21 (Secret pattern audit) private-key detection regex, which had a false-negative gap. The maintainer's regression-audit review asked whether the example was RSA-specific; investigation found the detection regex itself enumerated five algorithm tokens (`RSA|DSA|EC|OPENSSH|PGP`) and consequently MISSED three real PEM private-key header forms (named here by their PEM label only, without the dash-fenced envelope, so this entry does not itself reproduce a scanner-detectable string): the bare `PRIVATE KEY` label (PKCS#8 unencrypted, the most common modern serialization and OpenSSL's default); the `ENCRYPTED PRIVATE KEY` label (PKCS#8 encrypted); and the `PGP PRIVATE KEY BLOCK` label (the real PGP header; the old regex's `PGP` branch matched a non-existent `PGP PRIVATE KEY` form and missed the actual one with the ` BLOCK` suffix). A PKCS#8 private key pasted into any corpus document would have passed gate 21 undetected.

### Security

- [`tools/lint-secrets-in-content.py`](tools/lint-secrets-in-content.py): the private-key pattern's algorithm enumeration `(RSA|DSA|EC|OPENSSH|PGP)` was replaced with an open-ended uppercase-prefix construction anchored on the invariant `PRIVATE KEY` token (what makes a PEM block a secret), with the optional PGP ` BLOCK` suffix. The new pattern catches every current private-key form plus future algorithm types (a hypothetical future `ED25519 PRIVATE KEY` label would match) WITHOUT matching the non-secret PEM blocks that share the same envelope (`CERTIFICATE`, `PUBLIC KEY`, `DH PARAMETERS`). The pattern label is updated to "Private key block (PEM, any algorithm)". Verified against the live corpus: zero false positives. A broader "any label between the fences" alternative was considered and rejected because it flags certificates and public keys (non-secrets), which is a category error in a secret scanner.

### Added

- Five regression tests in `SecretsLinterTests` ([`tests/test_linters.py`](tests/test_linters.py)): three positive tests asserting the previously-missed forms (PKCS#8 unencrypted, PKCS#8 encrypted, PGP private key block) are now flagged; two negative tests asserting a `CERTIFICATE` block and a `PUBLIC KEY` block are NOT flagged as private keys (locking in the anchored pattern's precision so a future broadening cannot silently reintroduce false positives).

### Changed

- [`dev-security/claude-rules/core/secrets.md`](dev-security/claude-rules/core/secrets.md) and its project-local copy [`.claude/rules/secrets.md`](.claude/rules/secrets.md): the "Prohibited patterns" example `private_key` marker converged to the key-type-agnostic PKCS#8 form (the bare `PRIVATE KEY` label in the standard dash-fenced envelope). The source previously showed the RSA-specific form (which teaches that private keys are RSA — they are not); the local copy previously showed a truncated marker (vague). Both now show the generic PKCS#8 form, which is the most common modern serialization and the exact form the old regex missed. This also resolves a source-vs-local body divergence the regression audit flagged (the two copies' bodies are now identical modulo the local copy's provenance comment). Both files are exempt from gate 21 by basename, so the example does not self-trip the scanner.
- [`README.md`](README.md): library version `2026.06.29 → 2026.06.30`; README version `1.7.167 → 1.7.168`.

### Why anchor on `PRIVATE KEY` rather than enumerate algorithms

Future-proofing and precision both argue for the same anchor. Future private-key types vary in the algorithm prefix (RSA → EC → Ed25519 → whatever is next), not in the `PRIVATE KEY` label, which RFC 7468 standardizes. An open-ended uppercase prefix absorbs any future algorithm; anchoring on `PRIVATE KEY` is exactly what keeps the non-secret PEM blocks (certificates, public keys) out. Enumerating algorithm tokens, as the old regex did, is the source of the false-negative: any token not in the list slips through.

### A note on this entry not tripping the gate it documents

CHANGELOG.md is NOT on gate 21's exemption list (only the canonical [`.claude/rules/secrets.md`](.claude/rules/secrets.md) / [`dev-security/claude-rules/core/secrets.md`](dev-security/claude-rules/core/secrets.md), the linter itself, and the test file are exempt). An earlier draft of this entry reproduced the full dash-fenced header strings and correctly tripped the hardened gate. Rather than exempt CHANGELOG.md (which would weaken the gate to make content pass — a gate-discipline violation), the entry was rewritten to name each header by its PEM label without the dash-fenced envelope. This is the same discipline the canonical secrets.md relies on its exemption for: documentation that must describe a secret pattern either lives in an exempt file or describes the pattern without reproducing a detectable instance.

### Verification

Full 36-gate audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. The five new `SecretsLinterTests` pass standalone and via the linter regression test suite gate. The corrected regex was scanned against the entire corpus (all `.md` / `.py` / `.yml` / `.sh` files, excluding the three documented exemptions) and produced zero matches, confirming no false positives. Gate 21 itself passes on this PR's full diff, including this CHANGELOG entry. The version-date consistency audit (gate 29) confirms `2026.06.30` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-19, Library Version 2026.06.29, PR #42

Regression-audit fix: correct three stale gate-count references in the project instruction file [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md). All three said "32 gates" / "32-gate audit programme"; the audit programme has grown well past 32 (it was already past 32 before this session, and is 36 as of PR #37). The `.claude/` tree is exempt from the corpus linters, so no gate caught the drift; the regression audit found it.

### Changed

- [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md): three "32 gates" / "32-gate" references re-expressed without a hardcoded count. The "Why" section now reads "The audit programme (gate inventory in [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) §6) enforces that model"; the Commands section reads "Full audit sweep (all gates, CI order)"; the clarify-before-acting note reads "mechanically through the audit gates". This is the same name-not-number discipline applied in PR #39 and PR #40: a hardcoded count in prose outside the canonical inventory drifts on the next gate insertion. The number is not load-bearing in any of the three sites, so the count is dropped entirely rather than swapped for "36" (which would itself go stale); a reader who needs the exact current count is pointed at the canonical inventory in [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) §6.
- [`README.md`](README.md): library version `2026.06.28 → 2026.06.29`; README version `1.7.166 → 1.7.167`.

### Verification

Full 36-gate audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md) is under the corpus-linter-exempt `.claude/` tree, so the audit result is unchanged by this edit. Contradiction-search: a grep for any "N gate" / "N-gate" pattern in the file returns no matches post-edit. The version-date consistency audit (gate 29) confirms `2026.06.29` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

### Regression-audit cleanup series complete

This is the fourth and final of the regression-audit cleanup PRs (PR #39 TODO.md gate/pack references; PR #40 run-linter-regression.py docstring; PR #41 `.claude/` local-copy sync; PR #42 this). The remaining regression-audit findings (the `secrets`, `python`, `input-validation`, and `cicd-gates` local-copy drifts) are held for a direction-of-merge decision because their divergence may be intentional project-local customisation rather than un-propagated edits.

---

## 2026-06-19, Library Version 2026.06.28, PR #41

Regression-audit fix: re-sync the project-local copy of the evidence-grounded-completion rule with its pack source. PR #38 added two subsections ("API polling and webhook subscriptions", "No decorative external links") to the pack source at [`dev-security/claude-rules/governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md) but did not propagate the change to the project-local copy at [`.claude/rules/governance/evidence-grounded-completion.md`](.claude/rules/governance/evidence-grounded-completion.md). The two files are intended to be byte-identical (the local copy is the one a Claude Code session loads as session-start context; the pack copy is the distributable source). The `.claude/` tree is exempt from the corpus linters, so no gate caught the drift; the regression audit's `diff` of source against local copy found it.

### Fixed

- [`.claude/rules/governance/evidence-grounded-completion.md`](.claude/rules/governance/evidence-grounded-completion.md) re-synced from [`dev-security/claude-rules/governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md) (the pack source of truth). The 31-line addition is exactly the two subsections PR #38 added to the source; `diff` now reports the two files identical. No other content changed.

### Changed

- [`README.md`](README.md): library version `2026.06.27 → 2026.06.28`; README version `1.7.165 → 1.7.166`.

### Why no gate caught this, and the residual risk

The project-local `.claude/` rules tree is a copy of the pack under [`dev-security/claude-rules/`](dev-security/claude-rules/), maintained so a Claude Code session loads the rules as context. The `.claude/` directory is on the corpus linters' exemption list (it is AI-assistant config, not governed corpus content), so no audit gate compares the local copy to its source. This sync was therefore manual. The same drift class affects four other local copies (the `secrets`, `python`, `input-validation`, and `cicd-gates` rules), which the regression audit also flagged; those are being assessed separately because their divergence may be intentional project-local customisation rather than an un-propagated edit, and resolving them requires a direction-of-merge decision rather than a mechanical re-sync. This entry covers only the evidence-grounded-completion rule, whose divergence is unambiguously an un-propagated PR #38 edit.

### Verification

Full 36-gate audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. The synced file is under `.claude/`, which the corpus linters skip, so the audit result is unchanged by this edit; the verification that matters here is the `diff` showing the local copy and pack source are now byte-identical (zero diff output). The version-date consistency audit (gate 29) confirms `2026.06.28` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-19, Library Version 2026.06.27, PR #40

Regression-audit fix: correct a stale gate-number reference in the docstring of [`tools/run-linter-regression.py`](tools/run-linter-regression.py). The docstring claimed "the audit programme's gate 35 invokes this script"; PR #37's gate renumber (35 → 36 gates) moved the linter regression test suite from gate 35 to gate 36, but the docstring was not updated. The docstring is a Python comment, not markdown, so no corpus gate scans it; the regression audit found it.

### Changed

- [`tools/run-linter-regression.py`](tools/run-linter-regression.py): docstring no longer cites a bare gate number. It now describes the gate by role ("the linter regression test suite gate ... the final gate in the inventory") and points to [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) §6 as the maintained source of the number. Same name-not-number discipline applied in PR #39 to [`TODO.md`](TODO.md): a bare gate number in prose outside the canonical inventory goes stale on the next insertion.
- [`README.md`](README.md): library version `2026.06.26 → 2026.06.27`; README version `1.7.164 → 1.7.165`.

### Verification

Full 36-gate audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. The change is comment-only (a docstring); the script's behaviour is unchanged (it still runs `python3 -m unittest tests.test_linters` and forwards the exit code), so the linter regression test suite gate itself continues to pass. Contradiction-search: a grep for any "gate N" pattern in the edited script returns no matches post-edit. The version-date consistency audit (gate 29) confirms `2026.06.27` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-19, Library Version 2026.06.26, PR #39

Regression-audit fix: correct stale gate-number and pack-version references in [`TODO.md`](TODO.md) left behind by the PR #37 gate renumber (35 → 36 gates, which shifted the Skill derives-from reference audit from gate 31 to gate 32) and the PR #38 pack bump (`1.20.0 → 1.20.1`). A full-repository regression audit found these references in the "Pack and tooling extension" section of [`TODO.md`](TODO.md); they were never updated when the underlying gate number and pack version changed.

### Changed

- [`TODO.md`](TODO.md): three references to "gate 31" (describing the Skill derives-from reference audit) re-expressed by the audit's NAME rather than its number. Gate numbers renumber when a gate is inserted (PR #37 inserted the Document Date staleness audit at position 31, pushing Skill derives-from to 32); the gate name does not move. A parenthetical now states that the canonical numbered inventory lives in [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) §6, so future readers go to the one maintained source for numbers.
- [`TODO.md`](TODO.md): the pack-version cross-reference updated from "currently `1.20.0`" to "currently `1.20.1`" to match the pack version after PR #38.
- [`README.md`](README.md): library version `2026.06.25 → 2026.06.26`; README version `1.7.163 → 1.7.164`.

### Why name-not-number

This is the same lesson the PR #38 "No decorative external links" subsection encodes on a different axis: a reference that looks stable (a gate number) is not stable when the thing it points at can be renumbered. Prose outside the canonical inventory should reference gates by name; the inventory is the single place numbers are maintained. [`TODO.md`](TODO.md) is informational and not gate-enforced (no metadata block; exempt from the corpus audits), so nothing mechanically caught the drift — the regression audit did.

### Verification

Full 36-gate audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. [`TODO.md`](TODO.md) carries no `**Date:**` metadata field, so the Document Date staleness audit (gate 31) skips it; it is informational and exempt from the metadata audits. The version-date consistency audit (gate 29) confirms `2026.06.26` matches `2026-06`. The library-version-monotonicity audit (gate 13) confirms `2026.06.25 → 2026.06.26`. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry. Contradiction-search: after the edit, `grep -n "gate 31" TODO.md` returns no matches.

---

## 2026-06-19, Library Version 2026.06.25, PR #38

Extend the [`evidence-grounded-completion`](dev-security/claude-rules/governance/evidence-grounded-completion.md) pack rule with two new "Tool-specific guidance" subsections capturing two failure modes that surfaced in this session: a polling-pattern failure (raw `curl` against the unauthenticated GitHub API exhausted the 60-requests-per-hour-per-IP cap mid-session, after which every call returned HTTP 403, every iteration produced a Python `JSONDecodeError`, the loop never saw `completed`, and silent indefinite looping followed) and a URL-hallucination failure (auto-piloting from the project's file-path-link convention to a tool-name reference, inventing a plausible-looking documentation path under a real domain that did not in fact exist). Both lessons sit under §"Tool-specific guidance for AI coding assistants" next to the existing "Pipe-masked exit codes" subsection, with which they share the shape: a verification's actual outcome can be hidden by the way the verification is run.

Same PR introduces the new CHANGELOG heading convention. Each `## YYYY-MM-DD, Library Version X.Y.Z` heading now carries a trailing `, PR #N` clause so each entry is directly traceable to the PR that produced it. The version-date consistency audit (gate 29) regex is relaxed to make the `, PR #N` clause optional so historical entries that predate the convention continue to pass; entries from this PR forward include the clause. Retrofitting the 28 prior entries is not in scope of this PR.

### Added

- New subsection **"API polling and webhook subscriptions"** in [`dev-security/claude-rules/governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md), placed between "Pipe-masked exit codes" and "Stop hooks and pre-commit failures" under §"Tool-specific guidance for AI coding assistants". The subsection codifies four discipline points: prefer the platform's wake-on-event primitive (e.g., GitHub's `subscribe_pr_activity`) over polling; if polling is unavoidable, use authenticated tools (MCP / SDK / `gh` CLI) rather than raw `curl`; make the polling script fail-loud and bounded (no `-f` body-suppression, no blanket `2>/dev/null`, max-attempts ceiling, terminal-state-line-per-iteration); and trust the subscription's negative space (failure events are delivered; success / quiet states are not, so the operator must do one explicit status check at the next interaction to resolve ambiguity).
- New subsection **"No decorative external links"** in [`dev-security/claude-rules/governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md), placed immediately after the polling subsection. Codifies the discipline that backticked code spans are the default rendering for tool names, API names, CLI flags, and other identifiers; links are reserved for verified destinations (repository-internal paths verified by the broken-link audit, or external URLs drawn from a verified source). Domain plausibility is explicitly called out as not equivalent to verification: a URL on an allow-listed domain may still be a hallucinated path the domain check cannot detect. The rule layers with the project's [`tools/lint-external-link-domains.py`](tools/lint-external-link-domains.py), which catches off-domain hallucinations but not plausible-path ones.

### Changed

- [`tools/lint-version-date-consistency.py`](tools/lint-version-date-consistency.py): `CHANGELOG_HEADING_RE` regex extended to make the trailing `, PR #N` clause optional. Old shape `## YYYY-MM-DD, Library Version YYYY.MM.patch` continues to parse; new shape `## YYYY-MM-DD, Library Version YYYY.MM.patch, PR #N` is also recognised. The existing two invariants (date YYYY-MM matches version YYYY.MM; README Library Version matches most-recent CHANGELOG heading) are preserved.
- [`tests/test_linters.py`](tests/test_linters.py): `VersionDateConsistencyTests` covers the new heading shape (positive: heading-with-PR is accepted; positive: heading-without-PR remains accepted; negative: a malformed PR clause is not parsed as the heading).
- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) pack version `1.20.0 → 1.20.1`; date `2026-06-02 → 2026-06-19`. Patch: clarifications to an existing rule (two new subsections); no new rule files, no structural change to the pack's content shape. Rule-by-rule scope descriptions in the pack README's reference table are unchanged (the new subsections are internal to the existing rule).
- [`README.md`](README.md): library version `2026.06.24 → 2026.06.25`; README version `1.7.162 → 1.7.163`.

### Why this PR is separate from the gate-31 PR

The pack-rule extension is a documentation discipline change; the audit-gate addition ([library version `2026.06.24`](#2026-06-19-library-version-20260624)) is a mechanical-gate change. Keeping them as separate PRs keeps each diff surgical and the merge history clear: the gate PR's diff is the gate code and its wiring; this PR's diff is the rule extension and its version stamps. Either PR can be reverted without disturbing the other.

### Verification

Full 36-gate audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. Gate 31 (Document Date staleness audit), now in force, passes — the only files this PR edits with a `Date` metadata field are [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) (which is under the pack-rule prefix the audit exempts) and [`README.md`](README.md) (committed today, fresh Date). The pack rule [`governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md) itself is under `dev-security/claude-rules/` and not subject to the corpus metadata audits (no `Date` field on individual rule files; the pack README carries the pack version). The version-monotonicity audit (gate 13) confirms `2026.06.24 → 2026.06.25` and the pack-README's `1.20.0 → 1.20.1` are strictly increasing. The version-date consistency audit (gate 29) confirms `2026.06.25` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

### Self-disclosure of the failure mode this PR documents

This session itself produced two instances of the polling failure earlier today: a poll for PR #34 (which terminated only because curl happened to succeed on some iterations the task-output file did not capture into the conversation) and a poll for PR #36 (which hit the per-IP rate limit and ran indefinitely until the operator noticed and the session manually stopped it via the `TaskStop` tool). PR #37 (gate 31) was the corrective work for the per-document-Date class of defect; this PR is the corrective work for the polling-pattern class. Both PRs make the lessons durable: PR #37 mechanically; this PR rule-textually.

---

## 2026-06-19, Library Version 2026.06.24

Option B from the S.4 follow-up: close the audit-coverage gap that allowed the S.2 and S.4 PRs to substantively edit governance documents without bumping the per-document `Date` metadata. New audit gate 31, **Document Date staleness audit**, compares each in-scope markdown file's `**Date:**` metadata to the file's most-recent git commit date (committer date in UTC) and fails when the metadata lags by more than `--max-lag-days` (default 1). Historical drift is grandfathered via a `--baseline-date` flag (default `2026-06-19`); the audit only enforces on commits at or after the baseline so the audit's introduction does not block CI on the 233-file pre-existing backlog identified at design time.

### Added

- New audit gate 31, **Document Date staleness audit**, implemented by [`tools/lint-document-date-staleness.py`](tools/lint-document-date-staleness.py). Parses each in-scope markdown file's metadata Date, queries the file's most-recent git commit date via `git log -1 --follow --format=%cI`, and compares the two. Fails when lag exceeds `--max-lag-days` (default 1 day, which absorbs trailing-edge timezone slop). Files whose most-recent commit predates `--baseline-date` are grandfathered. Files with no Date field, no git history, or matching the generated-artefact exempt list ([`docs/portal.md`](docs/portal.md), [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md)) are skipped. Files under [`dev-security/claude-rules/`](dev-security/claude-rules/) use a different metadata convention and are exempted by an explicit prefix. The audit accepts `--root`, `--max-lag-days`, `--baseline-date`, and positional path arguments for the regression test suite.
- New regression test class `DocumentDateStalenessTests` in [`tests/test_linters.py`](tests/test_linters.py) with three tests: stale Date past tolerance is flagged; fresh Date (lag 0) passes; pre-baseline commit is grandfathered. Each test builds a synthetic minimal git repository in a temp directory with engineered `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE` env values so the linter can be exercised against known commit dates without depending on the main repo's history.

### Changed

- Audit programme renumbered from 35 to 36 gates. The new gate inserts at position 31 (between gate 30 *Metadata-block line-break audit* and the previous gate 31 *Skill derives-from reference audit*). Old gates 31, 32, 33, 34, 35 become 32, 33, 34, 35, 36 respectively. The renumbering touches: [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) §5 category descriptions and §6 inventory table and surrounding narrative; the inline `gate-35 regression test suite` references in 10 linter source files (now `gate-36`); the inline `gate 35 of the audit programme` reference in [`tests/README.md`](tests/README.md) (now `gate 36`); and the `35-gate` / `35 gates` / `gates 1-35` text in four governance docs.
- All four CI surfaces wired to invoke the new gate at position 31: [`.github/workflows/quality.yml`](.github/workflows/quality.yml) (new step "Document Date staleness audit"); [`tools/run_all_audits.sh`](tools/run_all_audits.sh) (new `run_gate` invocation; header comments updated from 31 / 35 gates to 32 / 36 gates); [`.pre-commit-config.yaml`](.pre-commit-config.yaml) (new hook `lint-document-date-staleness`); [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) §6 (new row inserted at position 31). The gate-name parity audit (now gate 35) confirms the four surfaces agree on the 36-gate name set and order.
- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md): version `1.3.0 → 1.4.0`; date stays `2026-06-19`. Minor (material) bump: §5 category descriptions edited (categories 5 and 7), §6 inventory grew by one row with four subsequent rows renumbered, the §6 post-table narrative rewritten (gates 1-31 / 32-33 / 34 / 35 → gates 1-32 / 33-34 / 35 / 36), §6.1 narrative updated (35-gate → 36-gate; gate 34 → gate 35).
- [`governance/procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md): version `1.0.2 → 1.0.3`; date stays `2026-06-19`. Patch: 35-gate → 36-gate text change.
- [`governance/register-main-branch-protection.md`](governance/register-main-branch-protection.md): version `1.0.2 → 1.0.3`; date stays `2026-06-19`. Patch: two 35-gate references and one `gates 1-35` reference updated to 36-gate / `gates 1-36`.
- [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md): version `1.1.2 → 1.1.3`; date stays `2026-06-19`. Patch: 35-gate → 36-gate and added "document Date staleness against git commit date" to the audit-programme coverage list.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md): version `1.27.8 → 1.27.9`; date stays `2026-06-19`. Patch: 35-gate → 36-gate in the audit-programme spec's index-row purpose column.
- [`security/README.md`](security/README.md): version `1.2.0 → 1.2.1`; date `2026-05-28 → 2026-06-19`. Patch backfill: the S.2 PR (library version `2026.06.19`, shipped 2026-06-19) added the Threat Modelling Standard to this README's listed-standards table without bumping per-document metadata. The new audit gate identified the omission during its initial run; the backfill keeps the audit's first commit clean.
- [`governance/register-canonical-citations.md`](governance/register-canonical-citations.md): version `1.4.21 → 1.4.22`; date `2026-05-31 → 2026-06-19`. Patch backfill: same root cause as [`security/README.md`](security/README.md) above — the S.2 PR added STRIDE and LINDDUN citation rows without bumping per-document metadata. Identified by the new audit gate's initial run.
- Auto-generated artefacts regenerated to reflect the new source metadata: [`taxonomy.yml`](taxonomy.yml) and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md).
- [`README.md`](README.md): library version `2026.06.23 → 2026.06.24`; README version `1.7.161 → 1.7.162`.

### Baseline-date design note

The baseline-date grandfathering mechanism is the deliberate trade-off that lets this audit land without a corpus-wide refresh. The initial-run scan of the live corpus found 233 files with metadata Dates lagging their most-recent commit by 2 or more days (some by 90+ days). Blocking CI on the entire backlog would force either a large unrelated cleanup PR or a permanent gate-disable; both are anti-patterns under the [`gate-discipline`](dev-security/claude-rules/governance/gate-discipline.md) rule. The baseline date (`2026-06-19`, the date this PR landed) grandfathers files whose most-recent commit predates that date. Going forward, every PR that touches a previously-grandfathered file inherits its commit-date forward and the file moves into the audit's scope on its next commit; eventually the entire corpus drifts past the baseline organically without a heroic cleanup. The maintainer can shift the baseline forward when a deliberate corpus-wide hygiene sweep happens (the change-tracking discipline requires the baseline shift to be recorded in this CHANGELOG).

### Acknowledging two S.2 backfills

The audit's initial run identified two files that the S.2 PR (library version `2026.06.19`) had substantively edited without per-document metadata bumps: [`security/README.md`](security/README.md) (a new row was added to the standards-listed table for the new Threat Modelling Standard) and [`governance/register-canonical-citations.md`](governance/register-canonical-citations.md) (two new rows were added for STRIDE and LINDDUN). Both were missed during S.2 by the same omission class S.4 demonstrated; both are backfilled in this PR so the new audit gate passes on its introduction commit. The S.4 backfill PR (`2026.06.23`) had already corrected the S.4-introduced omissions; the S.2-introduced omissions on these two files were not in scope of the S.4 backfill.

### Verification

Full 36-gate audit programme passes standalone ([`tools/run_all_audits.sh`](tools/run_all_audits.sh) exit code 0) immediately before commit. New gate 31 (Document Date staleness audit) reports the in-scope files (those with commit dates at or after baseline 2026-06-19) and finds no findings after the two S.2 backfills. New regression test class `DocumentDateStalenessTests` passes all three tests (stale-flagged, fresh-passes, pre-baseline-grandfathered) — verified standalone via `python3 -m unittest tests.test_linters.DocumentDateStalenessTests` and via gate 36 (Linter regression test suite). The gate-name parity audit (now gate 35) confirms all four surfaces agree on the 36-gate name set and order. The version-date consistency audit (gate 29) confirms `2026.06.24` matches `2026-06`. The library-version-monotonicity audit (gate 13) confirms `2026.06.23 → 2026.06.24` and the seven per-document version bumps are all strictly increasing. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

### Why this gate, this design, this baseline

The S.4 backfill PR (`2026.06.23`) was honest about the absence of an audit gate that catches per-document Date staleness; this PR closes that gap. The "right" gate design is the one that catches the omission going forward without inflicting a corpus-wide backfill as a precondition to the gate landing. The baseline-date mechanism is that compromise. The discipline being enforced is the [`specification-ingestion.md`](specification-ingestion.md) contract: every substantive content change to a document updates both the `Version` and the `Date`. The version-monotonicity audit (gate 13) catches the `Version` half; this audit catches the `Date` half. Together with the version-date consistency audit (gate 29), the metadata-block line-break audit (gate 30), and the per-PR D1 CHANGELOG delta gate, the change-tracking discipline is now mechanically enforced at all three layers (per-document metadata, generated artefacts, repository-wide audit trail).

---

## 2026-06-19, Library Version 2026.06.23

S.4 backfill: correct per-document Date and Version metadata on five governance files that were substantively edited in the S.4 PR (library version `2026.06.21`, shipped 2026-06-19) without their per-document metadata being bumped. The omission violated the [`specification-ingestion.md`](specification-ingestion.md) contract that every substantive content change must update the document's Date to the current date and bump its Version per the disposition (patch for minor revision, minor for material revision). No existing audit gate caught the omission; the gap is acknowledged here and is closed by the follow-up audit-gate work tracked separately.

### Changed

- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md): version `1.2.0 → 1.3.0`; date `2026-05-30 → 2026-06-19`. Minor (material) bump because S.4 inserted a new row into the §6 inventory table, renumbered four existing rows, and rewrote three narrative paragraphs across §5 (the category-list entry for "Programme and index integrity"), §6 (the post-table summary describing read-only linters / generator drift checks / self-check / regression suite), and §6.1 (delta gates not part of the corpus inventory).
- [`governance/procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md): version `1.0.1 → 1.0.2`; date `2026-06-02 → 2026-06-19`. Patch bump: S.4 changed the gate-count text from 34 to 35 in the audit-programme reference.
- [`governance/register-main-branch-protection.md`](governance/register-main-branch-protection.md): version `1.0.1 → 1.0.2`; date `2026-06-03 → 2026-06-19`. Patch bump: S.4 changed the gate-count text in the audit-trail-relationship section but left an internal inconsistency in the same paragraph (the sentence "The 35-gate audit programme... Without that requirement, gates 1-34 still run on each PR" mixed the new total with the old run-range). This backfill PR fixes that residual inconsistency as well: `gates 1-34 still run` → `gates 1-35 still run`. Detected during the contradiction-search step of the backfill verification.
- [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md): version `1.1.1 → 1.1.2`; date `2026-05-30 → 2026-06-19`. Patch bump: S.4 changed the gate-count text in the audit-coverage section.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md): version `1.27.7 → 1.27.8`; date `2026-05-30 → 2026-06-19`. Patch bump: S.4 changed the gate-count text in the audit-programme entry's purpose column.
- Auto-generated artefacts regenerated to pick up the new source-of-truth metadata: [`taxonomy.yml`](taxonomy.yml) and [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md) now carry the new Version and Date for each of the five files. Per the artefact-and-branch-discipline pack rule, source and generated output are committed together.
- [`README.md`](README.md): library version `2026.06.22 → 2026.06.23`; README version `1.7.160 → 1.7.161`.

### Why this backfill rather than fold-into-S.4

The S.4 PR (`2026.06.21`) is already merged. Editing per-document Date and Version on a separate backfill PR with a self-contained CHANGELOG entry is the artefact-and-branch-discipline-respecting path: the merged history of S.4 stays intact and the backfill is recorded as its own deliberate correction with a clear audit trail.

### Acknowledging the audit gap

No existing audit gate caught the omission. The closest gates are:

- Gate 29 ([`tools/lint-version-date-consistency.py`](tools/lint-version-date-consistency.py)) enforces *library*-level CalVer consistency between the README's `Library Version` and the most-recent CHANGELOG heading. It does not compare per-document Date metadata to the file's most-recent commit date.
- Gate 13 ([`tools/lint-library-version-monotonicity.py`](tools/lint-library-version-monotonicity.py)) enforces monotonic increase of versions but does not enforce that a file edited in a commit must have its Date refreshed.

The coverage gap is therefore: *no gate enforces "if a file with a Date metadata field was modified in this commit, its Date must reflect the commit date."* The follow-up audit-gate work that closes this gap is tracked separately and will land in a subsequent PR; this PR's role is the honest backfill, not the gate-addition.

### Verification

Full 35-gate audit programme passes standalone (`tools/run_all_audits.sh` exit code 0) immediately before commit. The metadata audit (gate 1) accepts the new metadata blocks on all five files. The version-monotonicity audit (gate 13) confirms each per-document version increase (`1.2.0 → 1.3.0`, three instances of `1.0.1 → 1.0.2`, `1.1.1 → 1.1.2`, `1.27.7 → 1.27.8`). The metadata-block line-break audit (gate 30) confirms the metadata blocks remain well-formed. The version-date consistency audit (gate 29) confirms `2026.06.23` matches `2026-06`. The taxonomy and portal in-sync gates (gates 32 and 33) confirm the regenerated artefacts match the source metadata. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

---

## 2026-06-19, Library Version 2026.06.22

S.4 follow-up: move the speculative "fourth skill" narrative out of the merged S.3 and S.4 CHANGELOG entries (where it violated Keep a Changelog's retrospective-only convention) and into [`TODO.md`](TODO.md) as a proper plan with a decision trigger, the empirical evidence to weigh at the trigger, an enumerated candidate set, and a selection criterion. The original CHANGELOG sentences pre-committed the project to a specific candidate (`change-tracking-write-entry`) without acknowledging the equally-strong alternative (`artefact-discipline-check`) or defining what "proven their format in practice" actually means; the TODO entry now records both and the criterion for choosing.

### Added

- New section "Pack and tooling extension" in [`TODO.md`](TODO.md) with a single item, "Post-S.3 evaluation of the Claude Code Skills format", placed between Priority 6 and Investigation / blocked. The item records: decision trigger (next pack version bump, refactor of an existing skill, or annual tooling review — whichever comes first); empirical evidence to weigh (Skill-tool discovery behaviour, semantic-drift judgement, format-stability evidence, subjective maintainer judgement); candidate rules ([`change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) → `change-tracking-write-entry`; [`artefact-and-branch-discipline.md`](dev-security/claude-rules/governance/artefact-and-branch-discipline.md) → `artefact-discipline-check`); selection criterion (failure-frequency observation, workflow-shape clarity, concrete misstep evidence); possible outcomes (add one, add both, add neither, defer).

### Changed

- Removed the forward-looking sentence from the S.3 CHANGELOG entry ("The door is open for a fourth skill..."). The "Phased follow-up context" paragraph for S.3 now ends at the S.4 announcement sentence.
- Removed the forward-looking sentence from the S.4 CHANGELOG entry ("...future work in this lineage would be a fourth skill..."). The "Phased follow-up context" paragraph for S.4 now ends at "With S.4 complete, the addyosmani integration is closed."
- [`README.md`](README.md): library version `2026.06.21 → 2026.06.22`; README version `1.7.159 → 1.7.160`.

### Why this cleanup

Keep a Changelog is strictly retrospective — entries describe what changed, not what might change. The S.3 and S.4 CHANGELOG entries each carried a forward-looking sentence that recorded a speculative future skill (`change-tracking-write-entry`) without defining what "proven their format in practice" meant and without acknowledging the alternative candidate. That made the speculation neither a real plan (no criteria, no trigger, no decision date) nor a clean historical record (forward-looking content in a retrospective document). The right home for forward-looking content is [`TODO.md`](TODO.md), where the project's other planned-but-not-yet-actioned enhancements are tracked. This PR closes the gap by moving the content to its proper home and recasting it as a plan with the criteria a reader can act on.

### Verification

Full 35-gate audit programme passes standalone (`tools/run_all_audits.sh` exit code 0) immediately before commit. No changes to audit-gate inventory, audit-tooling code, or any document under the corpus linters' scope; the only changed files are [`README.md`](README.md), [`CHANGELOG.md`](CHANGELOG.md), and [`TODO.md`](TODO.md) (the last of which is exempt from corpus audits per its own preamble). The version-date consistency audit (gate 29) confirms `2026.06.22` matches `2026-06`. The library-version-monotonicity audit (gate 13) confirms `2026.06.21 → 2026.06.22` is a strictly-increasing patch bump. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry. The CHANGELOG link-coverage audit (gate 11) confirms every backticked path reference in the new entry is wrapped in a markdown link.

---

## 2026-06-19, Library Version 2026.06.21

Phase S.4 of the addyosmani agent-skills integration plan: add a new audit gate that enforces the derive-and-cite contract between skills and pack rules. The gate verifies that every skill document under [`dev-security/claude-rules/skills/`](dev-security/claude-rules/skills/) declares a `derives_from:` YAML frontmatter field whose value resolves to an existing pack rule, closing the maintenance loop opened in S.3 (skill workflows reference canonical rules rather than duplicate them).

### Added

- New audit gate 31, **Skill derives-from reference audit**, implemented by [`tools/lint-skill-derives-from.py`](tools/lint-skill-derives-from.py). The audit parses each skill document's YAML frontmatter, requires a `derives_from:` field, and verifies that the named path resolves to an existing file in the repository. Exit codes: 0 on pass (including the bootstrap "no skills found" case), 1 on findings, 2 on internal error. The audit accepts a `--root` argument for use by the regression test suite.
- Frontmatter `derives_from:` field added to all three existing skill documents shipped in S.3, each pointing at the canonical pack rule the skill wraps: [`skills/evidence-grounded-completion/SKILL.md`](dev-security/claude-rules/skills/evidence-grounded-completion/SKILL.md) → [`governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md); [`skills/gate-discipline-diagnose/SKILL.md`](dev-security/claude-rules/skills/gate-discipline-diagnose/SKILL.md) → [`governance/gate-discipline.md`](dev-security/claude-rules/governance/gate-discipline.md); [`skills/clarify-before-acting/SKILL.md`](dev-security/claude-rules/skills/clarify-before-acting/SKILL.md) → [`governance/clarify-before-acting.md`](dev-security/claude-rules/governance/clarify-before-acting.md).
- New regression test class `SkillDerivesFromTests` in [`tests/test_linters.py`](tests/test_linters.py) with two positive tests: a synthetic skill with no `derives_from:` field is flagged; a synthetic skill whose `derives_from:` target does not exist is flagged. Both tests use the linter's `--root` argument to point at a temp-directory source set.

### Changed

- Audit programme renumbered from 34 to 35 gates. The new gate inserts at position 31 (between gate 30 Metadata-block line-break audit and the previous gate 31 Machine-readable taxonomy in-sync drift check). Old gates 31, 32, 33, 34 become 32, 33, 34, 35 respectively. The renumbering is reflected in: [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) section 6 gate inventory table and surrounding narrative; the inline `gate-34 regression test suite` references in 10 linter source files (now `gate-35`); the inline `gate 34 of the audit programme` reference in [`tests/README.md`](tests/README.md) (now `gate 35`); and the `34-gate` / `34 gates` text in governance docs ([`procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md), [`register-main-branch-protection.md`](governance/register-main-branch-protection.md), [`register-coverage-gaps.md`](governance/register-coverage-gaps.md), [`register-document-index-and-classification.md`](governance/register-document-index-and-classification.md)).
- All four CI surfaces wired to invoke the new gate, in the canonical surface order: [`.github/workflows/quality.yml`](.github/workflows/quality.yml) (new step "Skill derives-from reference audit"); [`tools/run_all_audits.sh`](tools/run_all_audits.sh) (new `run_gate` invocation; header comment updated from 30/34 gates to 31/35 gates); [`.pre-commit-config.yaml`](.pre-commit-config.yaml) (new hook `lint-skill-derives-from`); [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) section 6 (new row inserted at position 31). The gate-name parity audit (now gate 34) verifies the four surfaces agree on gate count and names.
- [`tools/run-linter-regression.py`](tools/run-linter-regression.py) updated to reflect the new gate count.
- [`README.md`](README.md): library version `2026.06.20 → 2026.06.21`; README version `1.7.158 → 1.7.159`.

### Verification

Full 35-gate audit programme passes standalone (`tools/run_all_audits.sh` exit code 0) immediately before commit. The new gate 31 reports the three real skill files passing and emits no findings. Regression test suite (gate 35) passes including the two new `SkillDerivesFromTests` tests. The gate-name parity audit (gate 34) confirms all four surfaces agree on the 35-gate name set and order. The version-date consistency audit (gate 29) confirms `2026.06.21` matches `2026-06`. The library-version-monotonicity audit (gate 13) confirms `2026.06.20 → 2026.06.21` is a strictly-increasing patch bump. The D1 CHANGELOG-on-PR delta gate is satisfied by this entry.

### Phased follow-up context

S.4 is the final phase of the four-phase addyosmani integration plan. S.1 (external overlay) shipped in `2026.06.18`. S.2 (Threat Modelling Standard with STRIDE / LINDDUN citations) shipped in `2026.06.19`. S.3 (governance skills in Claude Code Skills format) shipped in `2026.06.20`. With S.4 complete, the addyosmani integration is closed.

---

## 2026-06-19, Library Version 2026.06.20

Phase S.3 of the addyosmani agent-skills integration plan: introduce a third pack-content type, **Claude Code Skills** in the Skills workflow format (one SKILL-named file per skill), under a new `skills/` subdirectory. Three skills land in this PR, each derived from an existing governance rule with the rule remaining as the source of truth for normative content.

### Added

- New pack subdirectory [`dev-security/claude-rules/skills/`](dev-security/claude-rules/skills/) containing three skills in Claude Code's Skills format (YAML frontmatter with `name:` and `description:` for skill-tool discovery; sections for Overview, When to Use, Process, Red Flags, Verification, Common Rationalizations, See Also).
- [`skills/evidence-grounded-completion/SKILL.md`](dev-security/claude-rules/skills/evidence-grounded-completion/SKILL.md): wraps the six-step verification protocol from [`governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md) as an invocable workflow. Triggers: about to state "done", "complete", "fixed", "shipped", "ready", or any synonym (including "good catch" used to acknowledge a user-reported issue); wrapping up a unit of work with a summary; gate / lint / audit just reported green and about to claim the underlying work is complete.
- [`skills/gate-discipline-diagnose/SKILL.md`](dev-security/claude-rules/skills/gate-discipline-diagnose/SKILL.md): wraps the correct-response hierarchy from [`governance/gate-discipline.md`](dev-security/claude-rules/governance/gate-discipline.md) as an invocable workflow. Triggers: a CI gate / lint / type check / test suite / audit failed; pre-commit hook blocked a commit; required status check on a PR is red; generator-output `--check` reports drift; about to use `--no-verify` or a blanket suppression directive.
- [`skills/clarify-before-acting/SKILL.md`](dev-security/claude-rules/skills/clarify-before-acting/SKILL.md): wraps the ambiguity-detection and question-formulation discipline from [`governance/clarify-before-acting.md`](dev-security/claude-rules/governance/clarify-before-acting.md) as an invocable workflow. Triggers: request supports more than one reasonable interpretation; an external value the request does not pin down is required; a project-specific convention must be chosen; a trade-off the requestor would want to weigh in on must be made; the state of the world is unclear.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version `1.19.0 → 1.20.0`. The directory-structure ASCII tree gains a `skills/` entry with three skill subdirectories. The "Pack scope" section gains a paragraph documenting the new pack-content type, the distinction between rules (loaded as session-start context) and skills (discovered by Claude Code's Skill tool via frontmatter), and the derive-and-cite maintenance relationship (rule remains source of truth; skill is the workflow wrapper).
- [`README.md`](README.md): library version `2026.06.19 → 2026.06.20`; README version `1.7.157 → 1.7.158`.

### Maintenance relationship: derive-and-cite

Per the option chosen in the per-phase mitigation review, each SKILL.md is a workflow document that REFERENCES the canonical pack rule for normative content rather than duplicating it. The rule contains the framework-alignment tables, the exception-handling protocols, the rationale ("why this rule exists"), and the prohibited-anti-patterns enumerations. The skill contains the When-to-Use triggers, the Process steps (the verb-list from the rule, made invocable), the Red Flags (a condensed subset for quick reference), the Verification criteria, the Common Rationalizations, and a See Also block linking back to the rule. If the rule's Process protocol is restructured, the skill's Process steps must be updated; the link-coverage and section-anchor audits catch the broken cross-reference mechanically.

### Format conformance

The SKILL.md files follow the convention used in the [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills) overlay (shipped in S.1), which uses Claude Code's Skill tool discovery contract: YAML frontmatter with `name:` (lowercase-hyphenated) and `description:` (one sentence including "Use when ..." trigger phrases). The skill body is markdown sections.

### Verification

Full 34-gate audit programme passes standalone immediately before commit. Pre-flight language audit (gate 2) clean on all three SKILL.md files first attempt (avoided em-dashes and `-ise` verbs during authoring). Repository-internal links audit (gate 3) clean (each skill's See Also block uses relative paths verified against the actual pack-rule locations). Metadata audit (gate 1) does not scan `dev-security/claude-rules/` (exempt prefix), so the SKILL.md files are not subject to the 13-field metadata-block requirement; the YAML frontmatter convention is the Claude Skills format and is not in conflict with the exemption. The version-date consistency audit (gate 29) confirms `2026.06.20` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes.

### Phased follow-up context

This is Phase S.3 of the addyosmani integration plan. S.1 shipped in `2026.06.18`. S.2 shipped in `2026.06.19`. S.4 (audit gate for skill-to-rule reference integrity) follows.

---

## 2026-06-19, Library Version 2026.06.19

Phase S.2 of the addyosmani agent-skills integration plan: cherry-pick the STRIDE-per-trust-boundary framing and the three-tier disposition model from the addyosmani `security-and-hardening` overlay into a new library-canonical Standard, then add surgical "See also" cross-references from two existing documents.

### Added

- New Standard [`security/standard-threat-modelling.md`](security/standard-threat-modelling.md): the organisation's threat-modelling methodology. Per-doc version `1.0.0`. Document Type `Standard`, Category `Information Security`. Establishes the STRIDE-per-trust-boundary methodology (six-category taxonomy applied to each identified trust boundary, plus a recommended boundary catalogue covering external ingress / egress, user-to-system, system-to-system, privilege-change, OS, AI-model output, and storage boundaries), abuse-case authoring alongside use cases, and the three-tier disposition model (**Mandatory** / **Approval-Gated** / **Prohibited**) for each identified threat. Includes application-to-specific-system-types sections for web applications, AI / agentic systems (LLM output as a trust boundary), multi-tenant systems, privileged operations, and privacy-sensitive systems (LINDDUN cross-reference). Includes programme metrics, re-modelling triggers, and a framework-alignment table covering NIST SSDF (PW.1 / PW.2 / PW.7), NIST SP 800-53 (SA-8 / SA-11 / SA-15 / PT-2 / PT-3), ISO/IEC 27001 (A.5.34 / A.5.36 / A.8.25 / A.8.27 / A.8.28), OWASP ASVS (V1.1 / V14.1), and CSA CCM (AIS-04 / CCC-04 / CCC-06 / DSP-02 / IAM-02).
- New canonical-citation entries in [`governance/register-canonical-citations.md`](governance/register-canonical-citations.md) under "Cybersecurity adversary frameworks": **STRIDE** (1999, Kohnfelder + Garg, Microsoft SDL) and **LINDDUN** (v3.0, 2023, KU Leuven imec-DistriNet). Cited by the new Standard's References section.

### Changed

- [`dev-security/policy-secure-development-and-engineering.md`](dev-security/policy-secure-development-and-engineering.md) section 1.3 ("Project plans must include threat modelling...") gains a one-sentence pointer to the new Standard naming the STRIDE-per-trust-boundary methodology, abuse-case authoring, and the Mandatory / Approval-Gated / Prohibited disposition tiers. Per-doc version `1.0.1 → 1.0.2`. Date `2026-05-31 → 2026-06-19`.
- [`dev-security/claude-rules/core/owasp.md`](dev-security/claude-rules/core/owasp.md) "A04: insecure design" section gains a one-sentence pointer to the new Standard at the head of its Required-pattern list. The threat-model requirement was already named; the addition is the cross-reference to the canonical methodology. Pack version `1.18.0 → 1.19.0`.
- [`security/README.md`](security/README.md) "Active documents" table gains a row for the new Standard.
- [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) gains a row for the new Standard with cited frameworks (STRIDE, LINDDUN, OWASP ASVS, NIST SSDF, NIST SP 800-154, ISO/IEC 27001).
- [`taxonomy.yml`](taxonomy.yml), [`docs/portal.md`](docs/portal.md), [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md) regenerated to reflect the new artefact.
- [`README.md`](README.md): library `2026.06.18 → 2026.06.19`; README `1.7.156 → 1.7.157`.

### What was taken from addyosmani vs synthesised independently

Per the [`NOTICE.md`](NOTICE.md) external-reference policy, the new Standard borrows taxonomies (STRIDE, the three-tier disposition shape) but not text. The literal labels "Always Do / Ask First / Never Do" used by the addyosmani `security-and-hardening` overlay are rephrased into the project's own policy voice as "Mandatory / Approval-Gated / Prohibited", which is consistent with the existing Information Security Policy's tone and the [`governance/policy-exception-and-risk-acceptance-management.md`](governance/policy-exception-and-risk-acceptance-management.md) approval-gating convention. The STRIDE methodology is foundational and attributed to its 1999 Microsoft origin; LINDDUN is attributed to KU Leuven imec-DistriNet. No verbatim content from addyosmani's overlay is present in the new Standard.

### Verification

Full 34-gate audit programme passes standalone immediately before commit. New Standard re-read in full after the link-target fixes (initial draft cited non-existent paths under `privacy/`; corrected to the actual data-classification location in `security/` and to existing privacy policy / procedure documents for the LINDDUN application). Language audit (gate 2) clean (one `-ise` finding caught and fixed pre-audit). Repository-internal links audit (gate 3) clean. Structure audit (gate 4) confirms the new Standard is referenced from both [`security/README.md`](security/README.md) and the document-index register. Metadata audit (gate 1) confirms the 13-field block is complete. Version-monotonicity audit (gate 13) confirms the [`secure-development-and-engineering policy`](dev-security/policy-secure-development-and-engineering.md) per-doc bump `1.0.1 → 1.0.2` is an increase. Version-date consistency audit (gate 29) confirms `2026.06.19` matches `2026-06`.

### Phased follow-up context

This is Phase S.2 of the addyosmani integration plan. S.1 shipped in `2026.06.18`. S.3 (governance skills in Claude Code's Skills format) and S.4 (audit gate for skill-to-rule reference integrity) follow.

---

## 2026-06-19, Library Version 2026.06.18

Phase S.1 of the addyosmani agent-skills integration plan: add `addyosmani/agent-skills` as the fourth external rule source the pack vouches for, fully vet 5 of its 24 skills, copy those 5 plus the upstream MIT licence file into this project's overlay directory, and announce the fourth source through the setup-generator's offer flow.

### Added

- New external overlay directory [`.claude/rules/external/addyosmani/`](.claude/rules/external/addyosmani/) containing five fully-vetted skill files plus the upstream MIT licence file (preserved verbatim as required by MIT redistribution terms). Each skill carries a provenance header (source URL with pinned commit SHA `13e43f2310224d5770a7fb0a8c24c02b73da69e9`, fetch date `2026-06-19`, SHA-256 of the original fetched bytes). Content unmodified from upstream. The five files: [`security-and-hardening.md`](.claude/rules/external/addyosmani/security-and-hardening.md) (STRIDE-per-trust-boundary; Mandatory / Approval-Gated / Prohibited tier model; OWASP prevention patterns; LLM-output handling), [`code-review-and-quality.md`](.claude/rules/external/addyosmani/code-review-and-quality.md) (five-axis review with severity-labelled findings), [`ci-cd-and-automation.md`](.claude/rules/external/addyosmani/ci-cd-and-automation.md) (quality-gate pipeline configuration; eight sequential gates), [`using-agent-skills.md`](.claude/rules/external/addyosmani/using-agent-skills.md) (the meta-skill that explains how skills are discovered and invoked), [`context-engineering.md`](.claude/rules/external/addyosmani/context-engineering.md) (workflow-loading discipline).
- New entry in [`dev-security/claude-rules/vetting-log.md`](dev-security/claude-rules/vetting-log.md) for the addyosmani source: EXT-01 protocol applied to the 5 fully-vetted skills (red-flag scan results in a per-pattern outcome table); 18 remaining skill directories explicitly recorded as `Spot-scanned` (not fully vetted) so the consumer is informed if they later elect one of those via the setup-generator; per-skill depth disclosed honestly. Verdict: Vetted (no concerns) on the fully-read subset.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version `1.18.0`. The "External references → AI coding assistant rule repositories" section gains an addyosmani entry between Kariedo and the awesome-claude-code community index. The overlay-flow narrative updated from "three vetted external sources" to "four vetted external sources" (TikiTribe, Kariedo, addyosmani, Wiz) and the vetting-date statement now mentions both vetting cohorts (2026-05-31 and 2026-06-19).
- [`dev-security/claude-rules/setup-generator-prompt.md`](dev-security/claude-rules/setup-generator-prompt.md) updated to offer the fourth source through the unified-message overlay flow: the source table gains an addyosmani row (with the scope-is-workflow-not-GRC caveat in the "What that means" column), the "accept all four" / "review one by one" paths are updated, and a new "addyosmani per-source offer" block appears between Kariedo's and Wiz's offer blocks. The order presented to the consumer (TikiTribe → Kariedo → addyosmani → Wiz) keeps Wiz last because its licence carries the only commercial caveat.
- [`dev-security/claude-rules/vetting-log.md`](dev-security/claude-rules/vetting-log.md) per-document version `1.2.0 → 1.3.0`; Date `2026-05-31 → 2026-06-19`.
- [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md) overlay-narrative paragraph updated to mention addyosmani alongside TikiTribe and Kariedo, with a one-sentence scope caveat distinguishing engineering-workflow content (in Claude Code's Skills discovery format) from GRC governance.
- [`README.md`](README.md): library version `2026.06.17 → 2026.06.18`; README version `1.7.155 → 1.7.156`; Date `2026-06-03 → 2026-06-19`.

### Vetting depth disclosure

Per the [`evidence-grounded-completion`](.claude/rules/governance/evidence-grounded-completion.md) rule, the vetting depth is stated explicitly rather than implied. Fully vetted (read line-by-line, EXT-01 pattern scan completed): `security-and-hardening`, `code-review-and-quality`, `ci-cd-and-automation`, `using-agent-skills`, `context-engineering`. Spot-scanned (titles and `description:` frontmatter inspected via the upstream README index; not read in full): the remaining 18 skill directories. Consumers electing the overlay who later wish to fetch one of the spot-scanned skills should apply EXT-01 per fetch.

### Phased follow-up context

This is Phase S.1 of the addyosmani integration plan (four phases: S.1 external overlay, S.2 STRIDE cherry-pick + threat-modelling Standard, S.3 governance skills authored in Claude Code's Skills format, S.4 audit gate for skill-to-rule reference integrity). S.2-S.4 follow.

### Verification

Full 34-gate audit programme passes standalone immediately before commit. EXT-01 pattern scan on the 5 fully-vetted skills clean (no role-override / urgency / external-fetch / shell-execution / control-weakening / hidden-text patterns; details in the vetting-log entry). Provenance headers on each copied file include source URL with pinned commit SHA, fetch date, and SHA-256 of the original fetched bytes; the per-file SHA-256 values cited in the vetting log match the SHA-256 of the file body below the provenance header (verifiable by anyone re-fetching from the pinned commit). The version-date consistency audit (gate 29) confirms `2026.06.18` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes.

---

## 2026-06-03, Library Version 2026.06.17

Update the main-branch-protection register to reflect the bypass-actor configuration added on 2026-06-02. Closes the silent-drift gap between the register's claim ("bypass-actor list is empty") and the live ruleset state.

### Changed

- [`governance/register-main-branch-protection.md`](governance/register-main-branch-protection.md) per-document version `1.0.0 → 1.0.1`. The "Bypass list" section rewritten: was a one-sentence claim that the list is empty; is now a table with one entry (`jposluns`, "For pull requests" mode, added 2026-06-02) plus rationale (solo-maintainer posture; the bypass exists because GitHub's hard-coded self-review prohibition prevents the maintainer from approving their own MCP-authored PRs and without the bypass no maintainer-authored PR can merge). A new "What the bypass affects" subsection makes the trade-off explicit: in "For pull requests" mode the listed actor bypasses **all** ruleset rules including the required CI check, so the maintainer's behavioural discipline of waiting for CI green is no longer gate-enforced (it remains in force operationally). Force-push and branch-deletion remain blocked even for the bypass actor because those rules are not part of the PR-merge bypass scope. A new "Exception-handling cross-reference" subsection logs the bypass against the pack rule [`dev-security/claude-rules/governance/gate-discipline.md`](dev-security/claude-rules/governance/gate-discipline.md) exception-handling protocol, with a review trigger (addition of any second maintainer to the repository) rather than a calendar deadline.
- [`README.md`](README.md): library version `2026.06.16 → 2026.06.17`; README version `1.7.154 → 1.7.155`; Date `2026-06-02 → 2026-06-03` (calendar rolled).

### Why this matters

The [`evidence-grounded-completion`](.claude/rules/governance/evidence-grounded-completion.md) rule shipped 2026-06-01 says a register that makes a false claim about a snapshot is a defect. The register shipped in `2026.06.15` (PR #28) said the bypass list was empty. Within hours that became false (PR #29 was merged via the bypass), and the discrepancy has been outstanding since. This PR closes it.

### Verification

Full 34-gate audit programme passes standalone immediately before commit. The version-monotonicity audit (gate 13) confirms the per-document bump `1.0.0 → 1.0.1` is an increase. The version-date consistency audit (gate 29) confirms `2026.06.17` matches `2026-06`. The metadata-block line-break audit (gate 30) clean. The D1 CHANGELOG-on-PR delta gate passes.

This is the only outstanding piece of work from the day's session. With this PR the registers and the live configuration are once again in sync.

---

## 2026-06-02, Library Version 2026.06.16

Phase D.1 of the follow-up plan: give five previously-exempt repo-root meta files their own canonical 13-field metadata block and bring them under the corpus metadata audit. Closes the inconsistency where [`README.md`](README.md) carried a metadata block but other adjacent repo-root files did not.

### Added

- [`CONTRIBUTING.md`](CONTRIBUTING.md) gains a 13-field metadata block: Document Type **Guideline**, Version `1.0.0`, Category **Core Governance**, Owner / Approving Authority **Governance Library Maintainer**, Related Documents linking to the project's specifications, [`SECURITY.md`](SECURITY.md), and the new [`AUTHORS.md`](AUTHORS.md) metadata.
- [`SECURITY.md`](SECURITY.md) gains a 13-field metadata block: Document Type **Procedure**, Version `1.0.0`, Category **Core Governance**, Related Documents linking to [`CONTRIBUTING.md`](CONTRIBUTING.md), [`NOTICE.md`](NOTICE.md), and the exception-management and citation-verification governance specs.
- [`AUTHORS.md`](AUTHORS.md) gains a 13-field metadata block: Document Type **Register**, Version `1.0.0`, Category **Core Governance**, Review Frequency that includes "on every new contributor".
- [`docs/worked-example.md`](docs/worked-example.md) gains a 13-field metadata block: Document Type **Guide**, Version `1.0.0`, Category **Documentation**, Related Documents linking to the two specifications, [`CONTRIBUTING.md`](CONTRIBUTING.md), and the other adopter guides under [`docs/`](docs/). This is the only enforced file under [`docs/`](docs/); the rest of the directory contains generated artefacts ([`docs/portal.md`](docs/portal.md), [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md)) that intentionally lack metadata.

### Changed

- [`NOTICE.md`](NOTICE.md) extended from a partial 5-field block (Version, Date, Classification, Confidentiality, License) to the full 13-field block: Document Type **Policy**, Version `1.2.0 → 1.3.0`, Category **Core Governance**, Related Documents pointing at the citation-verification specification and the new canonical-citations register. The License field was normalised from `CC BY-SA 4.0 for original repository content only` to the canonical value `CC BY-SA 4.0`; the "original-repository-only" qualifier is documented in the body of NOTICE.md itself, which is the correct place for it.
- [`tools/lint-metadata.py`](tools/lint-metadata.py) updates the audit-rule set: NOTICE, CONTRIBUTING, SECURITY, and AUTHORS removed from the `EXEMPT` set; the new entries added to `PREFIX_EXEMPT_BASENAMES` so the filename-prefix-alignment check accepts the conventional repo-root names. A new `FORCE_INCLUDE_PATHS` set carves [`docs/worked-example.md`](docs/worked-example.md) out of the directory-level `docs/` exemption while leaving the rest of the directory exempt. Each change is anchored by a code comment naming "Phase D.1 (2026-06-02)" for future maintainers.
- [`TODO.md`](TODO.md) line 5 carve-out statement updated. Was: "README, NOTICE, CONTRIBUTING, SECURITY, CHANGELOG, and this TODO file are all maintained at the same conventional level (no per-file versioning)." Now correctly enumerates the remaining exempt files ([`CHANGELOG.md`](CHANGELOG.md), [`TODO.md`](TODO.md), [`instruction-ai-document-ingestion.md`](instruction-ai-document-ingestion.md)) and names the six files that now carry the canonical metadata block.
- [`README.md`](README.md): library version `2026.06.15 → 2026.06.16`; README version `1.7.153 → 1.7.154`.

### Verification

Full 34-gate audit programme passes standalone immediately before commit. The metadata audit (gate 1) now actively validates all five newly-headered files; previously it ignored them via `EXEMPT` / `EXEMPT_PREFIXES`. The filename-title-alignment audit (gate 7) accepts the repo-root basenames via the extended `PREFIX_EXEMPT_BASENAMES`. The metadata-block line-break audit (gate 30, shipped earlier today) ran clean on the five files — each new block's non-last lines carry the trailing `\` hard-break marker. The version-monotonicity audit (gate 13) confirms NOTICE's per-document `1.2.0 → 1.3.0` is an increase. The version-date consistency audit (gate 29) confirms `2026.06.16` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes.

### Phased follow-up context

This is Phase D.1 of the 4-phase plan. With this PR all four phases (A.1, B.1, C.1, D.1) are complete.

---

## 2026-06-02, Library Version 2026.06.15

Phase C.1 of the follow-up plan: document the `main` branch-protection configuration as a governance register so it can be audited from the repository rather than from a privileged settings-page view.

### Added

- [`governance/register-main-branch-protection.md`](governance/register-main-branch-protection.md) — new register documenting the configured GitHub ruleset on the `main` branch as of `2026-06-02`. Records each enabled rule, each rule explicitly left off (with rationale), the bypass-actor list state, adjacent settings (the repo's "Automatically delete head branches" toggle), the drift-detection procedure, and the load-bearing dependency between the required `Lint markdown corpus` status check and the 34-gate audit programme.

### Changed

- [`governance/README.md`](governance/README.md) gains a row for the new register under the "Register" type so the domain-README inventory stays current.
- [`README.md`](README.md): library version `2026.06.14 → 2026.06.15`; README version `1.7.152 → 1.7.153`.

### Verified configuration

The maintainer applied the following rules in the GitHub Rulesets UI on `main`:

- Required: status check `Lint markdown corpus`; pull-request review (1 approval minimum); conversation resolution before merging; signed commits; "Dismiss stale PR approvals on new commits"; "Require branches to be up to date before merging"; "Restrict deletions"; "Block force pushes".
- Repo-level "Automatically delete head branches" enabled in Settings → General → Pull Requests.
- Bypass-actor list confirmed empty.

This closes the gap where the pack rule [`dev-security/claude-rules/governance/artefact-and-branch-discipline.md`](dev-security/claude-rules/governance/artefact-and-branch-discipline.md) named expected settings but the project had no record of which settings were configured.

### Verification

Full 34-gate audit programme passes standalone immediately before commit. Pre-flight ran the language, metadata, and metadata-line-breaks audits standalone on the new register: zero findings on each. The new register's Date field anchors the next review per its declared Review Frequency. The version-date consistency audit (gate 29) confirms `2026.06.15` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes.

### Phased follow-up context

Phases A.1, B.1, C.1 complete. D.1 (metadata headers for the four repo-root files [`CONTRIBUTING.md`](CONTRIBUTING.md), [`docs/worked-example.md`](docs/worked-example.md), [`NOTICE.md`](NOTICE.md), [`SECURITY.md`](SECURITY.md)) follows next.

---

## 2026-06-02, Library Version 2026.06.14

Phase B.1 of the follow-up plan: promote the metadata-line-breaks scanner methodology developed during the rendering-cleanup PRs (#23, #24, #25) into a 34th audit gate. This catches the soft-wrap rendering bug class going forward in CI rather than relying on ad-hoc scans.

### Added

- [`tools/lint-metadata-line-breaks.py`](tools/lint-metadata-line-breaks.py) — new audit gate 30 (Metadata-block line-break audit). Finds runs of 2+ consecutive `**Field:**` lines and confirms each non-last line ends with either `\` or two-or-more trailing spaces (both are valid Markdown hard-break markers). Skips fenced code blocks via `iter_non_code_lines` so templates demonstrating metadata format are not false-positives. Last line in each run is exempt because the next line is conventionally a blank line or `---` separator.
- [`tests/test_linters.py`](tests/test_linters.py) gains `MetadataLineBreaksTests` with two cases: (a) a metadata block outside any code fence whose non-last lines lack hard-break markers (must be flagged), and (b) the same block inside a code fence (must NOT be flagged).

### Changed

- All four audit-programme surfaces gain the new gate at position 30; gates previously at positions 30-33 renumber to 31-34. The four surfaces are: [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) section 6 inventory, [`.github/workflows/quality.yml`](.github/workflows/quality.yml), [`tools/run_all_audits.sh`](tools/run_all_audits.sh), and [`.pre-commit-config.yaml`](.pre-commit-config.yaml). The gate-name parity audit (now gate 33) confirms all four declare the new gate at the same ordered position.
- Inline `gate-33 regression test suite` comments in 9 linters renumbered to `gate-34` to track the regression suite's new position: [`tools/lint-acronym-consistency.py`](tools/lint-acronym-consistency.py), [`tools/lint-audit-gate-parity.py`](tools/lint-audit-gate-parity.py), [`tools/lint-citation-verification-freshness.py`](tools/lint-citation-verification-freshness.py), [`tools/lint-library-version-monotonicity.py`](tools/lint-library-version-monotonicity.py), [`tools/lint-roles.py`](tools/lint-roles.py), [`tools/lint-standards-currency.py`](tools/lint-standards-currency.py), [`tools/lint-structure.py`](tools/lint-structure.py), [`tools/lint-tooling-provenance-freshness.py`](tools/lint-tooling-provenance-freshness.py), [`tools/lint-version-date-consistency.py`](tools/lint-version-date-consistency.py), [`tools/run-linter-regression.py`](tools/run-linter-regression.py), and [`tests/README.md`](tests/README.md).
- Gate-count references "33-gate / 33 gates" → "34-gate / 34 gates" in [`governance/procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md), [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md), [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md), and the comments in [`tools/run_all_audits.sh`](tools/run_all_audits.sh) and [`tools/lint-audit-gate-parity.py`](tools/lint-audit-gate-parity.py).
- [`README.md`](README.md): library version `2026.06.13 → 2026.06.14`; README version `1.7.151 → 1.7.152`.

### Why this matters

We've seen the soft-wrap rendering bug bite 6 files across the corpus during today's session: the pack [`README.md`](dev-security/claude-rules/README.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), [`docs/worked-example.md`](docs/worked-example.md), and three [`compliance/logistics/`](compliance/logistics/) registers. Each was found by an ad-hoc Python scanner — a one-off discovery that doesn't run in CI. With the gate in place, any future PR that introduces or reintroduces the same bug fails CI before merge. The implementation reuses the methodology proven in those rendering-fix PRs, including the fenced-code-block skip that prevents false-positives on metadata-format-demonstration templates.

### Verification

Full 34-gate audit programme passes standalone. The new gate (gate 30) runs cleanly on the current corpus (zero findings). The gate-name parity audit (now gate 33) confirms the four surfaces all declare the new gate at the same ordered position. The two new regression tests pass under `python3 -m unittest tests.test_linters.MetadataLineBreaksTests`. The version-date consistency audit confirms `2026.06.14` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes.

### Phased follow-up context

This is Phase B.1 of the 4-phase plan: A.1 (defect fix, shipped in `2026.06.13`) and B.1 are now complete. C.1 (branch-protection verification) and D.1 (metadata headers for the four repo-root files) follow.

---

## 2026-06-02, Library Version 2026.06.13

Phase A.1 of the follow-up plan: fix the underlying defect in the version-monotonicity audit that caused two real problems earlier today. The audit's regex previously matched any `**Version:** x.y.z` line in a Markdown file regardless of context, including lines inside fenced code blocks. This let (a) Phase 0's bulk sed sweep match a template field in [`CONTRIBUTING.md`](CONTRIBUTING.md), and (b) the audit block the cleaner revert in PR #24.

### Fixed

- [`tools/lint-library-version-monotonicity.py`](tools/lint-library-version-monotonicity.py) now reads versions via `iter_non_code_lines` from [`tools/lint_common.py`](tools/lint_common.py), the same fence-aware helper that [`tools/lint-language.py`](tools/lint-language.py) already uses. Both `CALVER_RE` (library version on [`README.md`](README.md)) and `SEMVER_RE` (per-document versions) now skip fenced code blocks. The matching otherwise unchanged: first match wins, file order preserved.

### Added

- [`tests/test_linters.py`](tests/test_linters.py) gains `test_library_version_in_code_block_ignored` in `LibraryVersionMonotonicityTests`. The fixture has a high version (`9999.99.99`) inside a fenced code block and the real version (`2026.01.0`) outside; the audit must skip the fence and pick the real value. The pre-existing `test_decreased_library_version_flagged` continues to pass, confirming the regression coverage on the prior behaviour did not change.

### Changed

- [`README.md`](README.md): library version `2026.06.12 → 2026.06.13`; README version `1.7.150 → 1.7.151`.

### Why this matters

Phase 0 (`2026.06.2`) bulk-bumped `0.0.1 → 1.0.1` across 54 files using a sed pattern that matched any line starting with `**Version:** 0.0.1`. It inadvertently matched a template metadata block inside [`CONTRIBUTING.md`](CONTRIBUTING.md)'s fenced code region. PR #24 (`2026.06.11`) tried to revert that template's Version to `0.0.1`, but the monotonicity audit (gate 13) refused because it saw the in-fence value as a per-document regression `1.0.1 → 0.0.1`. The fallback was to use a non-semver placeholder `X.Y.Z` instead — a workable solution but not the cleanest. With this PR's fix, future bulk sweeps and template reverts can use the natural `0.0.1` value without tripping the audit.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. The new regression test passes; the existing one continues to pass. Re-ran the audit standalone on the current corpus: zero false-positive findings. The version-date consistency audit (gate 29) confirms `2026.06.13` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes.

### Phased follow-up context

This is Phase A.1 of the 4-phase follow-up plan (A.1 defect fix; B.1 new gate; C.1 branch-protection verification; D.1 metadata-header additions for the four repo-root files).

---

## 2026-06-02, Library Version 2026.06.12

Three additional files from a tightened metadata-rendering scan that my original scanner missed. Closes the metadata-rendering cleanup with **zero** remaining flagged files corpus-wide.

### Why these files were missed by the original scan

The scanner I used to produce the original "3 files" list had two false-negative paths:

1. It returned on the **first** `**Field:**` run found in each file, not every run. A file whose first block was correctly formatted (with trailing `\`) but whose second block (mid-document) was not received an overall "OK" classification.
2. It did not treat **two trailing spaces** as a Markdown hard break (only `\`), but this turned out to be moot for these files because the broken lines use a **single** trailing space (which is not a hard break in either syntax).

The tightened scanner used for this PR checks every `**Field:**` run in the file, skips fenced code blocks, and recognises both `\` and two-trailing-spaces as valid hard breaks. It found zero remaining bugs after the fixes below.

### Fixed

- [`compliance/logistics/register-ctpat-united-states-it-controls.md`](compliance/logistics/register-ctpat-united-states-it-controls.md) — one inline-attribute block at lines 23-25 (Programme authority, UK parallel programme, Mutual recognition). Two trailing backslashes added to lines 23 and 24; line 25 is the last in the block.
- [`compliance/logistics/register-ctpat-united-states-msc-controls.md`](compliance/logistics/register-ctpat-united-states-msc-controls.md) — two blocks: one at lines 23-26 (Programme authority, UK equivalent, Canada equivalent, Mutual recognition) and one at lines 34-38 (Organisation entity type, membership number, current tier, last validation, next profile update due). Seven trailing backslashes added across the two blocks.
- [`compliance/logistics/register-pip-canada-controls.md`](compliance/logistics/register-pip-canada-controls.md) — one block at lines 23-26 (Programme authority, UK parallel programme, US parallel programme, Mutual recognition). Three trailing backslashes added to lines 23-25; line 26 is the last in the block.

These blocks are not metadata in the document-header sense; they are labelled facts at the start of each register's Purpose section (programme authority, parallel programmes in other jurisdictions, mutual-recognition arrangements). They are meant to render as a vertical list of attributes; under the previous formatting they soft-wrapped into a paragraph.

### Changed

- [`README.md`](README.md): library version `2026.06.11 → 2026.06.12`; README version `1.7.149 → 1.7.150`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. The tightened scanner reports zero remaining flagged files across the entire corpus (every `**Field:**` run in every non-exempt `.md` file either has all non-last lines terminated by `\` or two trailing spaces, OR is inside a fenced code block, OR is fewer than two lines and so doesn't form a renderable block). The version-date consistency audit (gate 29) confirms `2026.06.12` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

### Cleanup status: complete

Three PRs total for the metadata-rendering cleanup:
- [`2026.06.10`](#2026-06-02-library-version-20260610): pack README + worked-example.
- [`2026.06.11`](#2026-06-02-library-version-20260611): CONTRIBUTING.md.
- This PR: three compliance/logistics registers.

The improved scanner methodology is documented in this CHANGELOG entry; it will catch this class of bug going forward when run as part of pre-PR review.

---

## 2026-06-02, Library Version 2026.06.11

Third and final file from the metadata-rendering scan: [`CONTRIBUTING.md`](CONTRIBUTING.md). Backslash fix plus a Version-field placeholder change that resolves an underlying gap exposed by today's investigation.

### Fixed

- [`CONTRIBUTING.md`](CONTRIBUTING.md) — 12 metadata lines (79-90) gain the trailing `\`. The block itself is a TEMPLATE inside a fenced code region (lines 76-92) demonstrating to new contributors what a metadata block should look like; it is not the file's own metadata. With backslashes now in place, contributors who copy the template into their new document will get a properly-rendering block by default.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) `**Version:**` field in the template changed from the post-Phase-0 value `1.0.1` to the explicit non-semver placeholder `X.Y.Z`. Rationale: a "starter values" template should show contributors the placeholder shape, not a misleading concrete version number. `X.Y.Z` is unambiguous as a placeholder and (deliberately) does not match the version-monotonicity audit's `SEMVER_RE` regex — which means the template is no longer subject to the same misinterpretation that caused Phase 0's bulk sweep to inadvertently change it from `0.0.1` to `1.0.1` in the first place.

### Underlying gap (noted, not fixed in this PR)

The version-monotonicity audit ([`tools/lint-library-version-monotonicity.py`](tools/lint-library-version-monotonicity.py)) does not skip fenced code blocks; its `SEMVER_RE` regex matches any `**Version:** X.Y.Z` line in a file regardless of context. This is what let the audit treat [`CONTRIBUTING.md`](CONTRIBUTING.md)'s template as the file's real version, and what let the Phase 0 bulk sed sweep wrongly include the file. Fixing the audit to skip fenced code blocks (matching the pattern already used in [`tools/lint-language.py`](tools/lint-language.py) via `iter_non_code_lines` from [`tools/lint_common.py`](tools/lint_common.py)) would close the gap properly. The `X.Y.Z` placeholder is sufficient to unblock this PR; the audit hardening is tracked as future work.

### Changed

- [`README.md`](README.md): library version `2026.06.10 → 2026.06.11`; README version `1.7.148 → 1.7.149`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. Specifically, the version-monotonicity audit (gate 13) reports `current 2026.6.11 >= prior 2026.6.10` for the library and no per-document regressions, confirming that the `X.Y.Z` placeholder does not look like a decrease vs the prior committed `1.0.1`. Re-ran the metadata-rendering scanner used to discover the original bug: zero remaining flagged files in the corpus. The version-date consistency audit (gate 29) confirms `2026.06.11` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

This is the second of two PRs in the metadata-rendering cleanup, following [`2026.06.10`](#2026-06-02-library-version-20260610). The corpus is now uniformly free of the soft-wrap rendering bug.

---

## 2026-06-02, Library Version 2026.06.10

Fix metadata-rendering bug in two files where consecutive metadata lines lacked the trailing `\` line-break that this corpus uses to force hard wraps. Without it, GitHub soft-wraps the metadata block into a single paragraph, making it unreadable. A full-corpus scan found exactly three affected files; two are fixed in this PR ([`CONTRIBUTING.md`](CONTRIBUTING.md) follows in a separate PR because its metadata block is a contributor template with its own Version-field considerations).

### Fixed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) — 12 metadata lines (lines 3-14) gain the trailing `\` that the rest of the corpus uses. The `**License:** CC BY-SA 4.0` line at the bottom of the block correctly remains without a backslash because the next line is the `---` separator (paragraph break already implied). While in the file, the `**Date:**` field is also bumped `2026-06-01 → 2026-06-02` to reflect that today's seven mobile-app-security commits (Phases 2-7) substantively changed the file. The pack version `1.17.0` is unchanged because this is a presentation fix, not a content change to the pack's distributable rule files.
- [`docs/worked-example.md`](docs/worked-example.md) — same `\` fix to lines 57-68. The metadata block here is INSIDE a worked-example region that demonstrates "this is what a proper metadata block looks like" to a reader following the adopter walkthrough; the rendering bug therefore taught the wrong lesson, which is doubly bad in an example. The illustrative field values (Document Title "Quarterly Privileged Access Review Procedure" etc.) are unchanged.

### Changed

- [`README.md`](README.md): library version `2026.06.9 → 2026.06.10`; README version `1.7.147 → 1.7.148`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. Re-ran the metadata-rendering scanner used to discover the bug; both files are now flagged "OK" (every non-last metadata line ends with `\`). The third file ([`CONTRIBUTING.md`](CONTRIBUTING.md)) is handled in the following PR. The version-date consistency audit (gate 29) confirms `2026.06.10` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-02, Library Version 2026.06.9

Mobile-app security work, Phase 7 of 8 (final): Capacitor / Ionic pack rule file. The mobile-app security work announced as the 8-phase plan is complete with this release.

### Added

- [`dev-security/claude-rules/languages/capacitor-ionic.md`](dev-security/claude-rules/languages/capacitor-ionic.md) — new pack rule file for Capacitor (modern Cordova successor) and Ionic Framework mobile applications. Notes that Cordova-only apps should migrate (per Apache's published maintenance-mode status). Covers secure-storage delegation (`capacitor-secure-storage-plugin` over `@capacitor/preferences`, `localStorage`, IndexedDB, Ionic Storage default), Content Security Policy inside the wrapped WebView (explicit allow-listed origins, no `unsafe-inline` or `unsafe-eval`), JS bridge / plugin trust boundary (narrow validated plugin APIs with Kotlin examples; treat every plugin call as untrusted), network (HTTPS-only; pinning at native layer via `CapacitorHttp`; `allowMixedContent` prohibited), backend attestation (App Attest / Play Integrity via native plugin code), deep links via App Links / Universal Links, permissions narrow scope, debug-tooling exclusion (`webContentsDebuggingEnabled: false` in release), OTA updates (Ionic Appflow / Capacitor Live Updates with signed payloads, no native code or new permissions), in-app purchases (`cordova-plugin-purchase`, `@capacitor-community/in-app-purchases` with backend verification of platform receipt or `purchaseToken`), and the carryover web-stack XSS rules because the WebView IS the application UI.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version `1.17.0`. Directory-structure ASCII tree gains an entry for [`languages/capacitor-ionic.md`](dev-security/claude-rules/languages/capacitor-ionic.md); rule-files table gains a new row noting the web-stack carryover from [`languages/typescript.md`](dev-security/claude-rules/languages/typescript.md) and the core OWASP pack rule [`core/owasp.md`](dev-security/claude-rules/core/owasp.md).
- [`README.md`](README.md): library `2026.06.8 → 2026.06.9`; README `1.7.146 → 1.7.147`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new file: zero findings first attempt. Re-read the file in full to confirm cross-references to the standard's Sections 2, 5, 6, 10, 13, 14 point at actual content. The opening hybrid-framework rule emphasises that BOTH web-stack and mobile-stack security apply (because the WebView is the UI), which is the Capacitor-specific elaboration of Section 13's general rule. The version-date consistency audit (gate 29) confirms `2026.06.9` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes.

### Phased rollout context: complete

This is Phase 7 of 8, the final phase. With this release the mobile-app security work announced as an 8-phase plan is complete:
- Phase 0 (Library `2026.06.2`): bulk version bump 0.0.1 → 1.0.1 across 54 files.
- Phase 1 (Library `2026.06.3`, std `1.0.1 → 1.1.0`): mobile standard expansion (App Attest, hybrid frameworks, IAP).
- Phase 2 (Library `2026.06.4`, pack `1.12.0`): [`languages/swift.md`](dev-security/claude-rules/languages/swift.md).
- Phase 3 (Library `2026.06.5`, pack `1.13.0`): [`languages/kotlin.md`](dev-security/claude-rules/languages/kotlin.md).
- Phase 4 (Library `2026.06.6`, pack `1.14.0`): [`languages/react-native.md`](dev-security/claude-rules/languages/react-native.md).
- Phase 5 (Library `2026.06.7`, pack `1.15.0`): [`languages/flutter.md`](dev-security/claude-rules/languages/flutter.md).
- Phase 6 (Library `2026.06.8`, pack `1.16.0`): [`languages/dotnet-maui.md`](dev-security/claude-rules/languages/dotnet-maui.md).
- Phase 7 (Library `2026.06.9`, pack `1.17.0`): [`languages/capacitor-ionic.md`](dev-security/claude-rules/languages/capacitor-ionic.md).

Coverage now spans native iOS (Swift, Objective-C), native Android (Kotlin, Java for Android), and the four mainstream cross-platform stacks (React Native, Flutter, .NET MAUI, Capacitor / Ionic) at the pack-rule layer, with the mobile standard providing the human-readable normative requirements those rules cite. Future pack work may add further mobile frameworks as they emerge.

---

## 2026-06-02, Library Version 2026.06.8

Mobile-app security work, Phase 6 of 8: .NET MAUI pack rule file.

### Added

- [`dev-security/claude-rules/languages/dotnet-maui.md`](dev-security/claude-rules/languages/dotnet-maui.md) — new pack rule file for .NET MAUI applications (including Blazor Hybrid). The existing [`languages/csharp.md`](dev-security/claude-rules/languages/csharp.md) remains the server-side C# rule file. Covers secure-storage delegation (`SecureStorage` and encrypted SQLite over `Preferences` and unencrypted SQLite), cross-platform handlers and dependency-service trust boundary (narrow validated APIs; Blazor Hybrid `IJSRuntime` interop boundary), network (certificate pinning via custom `RemoteCertificateValidationCallback`), backend attestation through platform-conditional `IAttestationService` implementations, build hardening and release configuration (csproj `PropertyGroup` settings for iOS / Android release; ProGuard / R8 enable; trimming review; hot-reload kept to debug), deep links via MAUI Shell with App Links / Universal Links, permissions (`Permissions.RequestAsync<>` with narrow scope), in-app purchases (`Plugin.InAppBilling` / `Xamarin.Essentials.InAppPurchase` with backend verification of platform receipt / `purchaseToken`), logging and crash-reporter redaction, and Blazor Hybrid WebView specifics (`MarkupString` hazards, CSP delivery via host page).

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version `1.16.0`. Directory-structure ASCII tree gains an entry for [`languages/dotnet-maui.md`](dev-security/claude-rules/languages/dotnet-maui.md); rule-files table gains a new row.
- [`README.md`](README.md): library `2026.06.7 → 2026.06.8`; README `1.7.145 → 1.7.146`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new file: zero findings first attempt. Re-read the file in full to confirm cross-references to the standard's Sections 2, 5, 6, 7, 10, 13, 14 point at actual content. The opening hybrid-framework rule restates Section 13's "shifts layers, doesn't remove controls" applied to MAUI's specific architecture (Mono / .NET runtime + handler pattern). The version-date consistency audit (gate 29) confirms `2026.06.8` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes.

### Phased rollout context

Phase 6 of 8. Phase 7 completes the mobile-app work with Capacitor / Ionic.

---

## 2026-06-02, Library Version 2026.06.7

Mobile-app security work, Phase 5 of 8: Flutter pack rule file.

### Added

- [`dev-security/claude-rules/languages/flutter.md`](dev-security/claude-rules/languages/flutter.md) — new pack rule file for Flutter applications written in Dart. Covers secure-storage delegation (`flutter_secure_storage` + `sqflite_sqlcipher` over `shared_preferences` and unencrypted sqflite), platform channels and FFI as trust boundaries (with Kotlin native-side validation examples), network (`http_certificate_pinning` for Tier 1 / Tier 2), backend attestation forwarded through a Flutter package, debug-tooling exclusion (`kReleaseMode` gating, `--obfuscate --split-debug-info` for release builds, Dart DevTools restricted to debug / profile), OTA updates (Shorebird as the signed-payload option; raw code-OTA prohibited by Apple / Google store terms by default), deep links (App Links / Universal Links over custom schemes), permissions (narrow scope via `permission_handler`), in-app purchases (`in_app_purchase` plugin with backend verification of `serverVerificationData`), and logging / crash-reporter redaction.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version `1.15.0`. Directory-structure ASCII tree gains an entry for [`languages/flutter.md`](dev-security/claude-rules/languages/flutter.md); rule-files table gains a new row.
- [`README.md`](README.md): library `2026.06.6 → 2026.06.7`; README `1.7.144 → 1.7.145`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new file: zero findings first attempt. Re-read the file in full to confirm cross-references to the standard's Sections 2, 5, 6, 10, 13, 14 point at actual content. The opening hybrid-framework rule mirrors the standard's Section 13 opener applied to Flutter's specific architecture (platform channels and Dart runtime). The version-date consistency audit (gate 29) confirms `2026.06.7` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes.

### Phased rollout context

Phase 5 of 8. Phases 6-7 add .NET MAUI and Capacitor / Ionic.

---

## 2026-06-02, Library Version 2026.06.6

Mobile-app security work, Phase 4 of 8: React Native pack rule file.

### Added

- [`dev-security/claude-rules/languages/react-native.md`](dev-security/claude-rules/languages/react-native.md) — new pack rule file for React Native applications (with or without Expo). Implements Section 13 (hybrid frameworks) of [`standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md) plus the native-layer sections as they apply through the JS bridge. Covers secure-storage delegation (`react-native-keychain` and encrypted MMKV over `AsyncStorage` and the unencrypted MMKV constructor), JS bridge as a trust boundary (legacy bridge and JSI / TurboModule), network with certificate pinning (`react-native-ssl-pinning`), backend attestation forwarded through a thin native module, debug-tooling exclusion (`__DEV__` dead-code elimination; Flipper / Reactotron / react-native-debugger guarded), over-the-air updates (CodePush, EAS Update, Shorebird) with signed payloads and no-new-permissions rule, deep links (Universal Links / App Links over custom schemes), permissions (rationale must match actual data flow), in-app purchases (`react-native-iap`, `expo-in-app-purchases`, RevenueCat — backend verification of `transactionReceipt` / `purchaseToken` required regardless), and crash-reporter PII redaction. Closing section covers Expo-specific notes (`expo-secure-store`, EAS Build signing, EAS Update channels).

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version `1.14.0`. Directory-structure ASCII tree gains an entry for [`languages/react-native.md`](dev-security/claude-rules/languages/react-native.md); rule-files table gains a new row.
- [`README.md`](README.md): library `2026.06.5 → 2026.06.6`; README `1.7.143 → 1.7.144`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new file: one finding caught and fixed pre-audit (one em-dash in the RevenueCat parenthetical; restructured into two sentences). Re-read the file in full to confirm cross-references to the standard's Sections 2, 5, 6, 10, 13, 14 point at actual content. The opening hybrid-framework rule ("React Native shifts the layer at which a control is implemented; it does not remove the control") quotes the standard's Section 13 opener. The version-date consistency audit (gate 29) confirms `2026.06.6` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

### Phased rollout context

This is Phase 4 of 8. Phases 5-7 add Flutter, .NET MAUI, and Capacitor / Ionic.

---

## 2026-06-02, Library Version 2026.06.5

Mobile-app security work, Phase 3 of 8: Android pack rule file.

### Added

- [`dev-security/claude-rules/languages/kotlin.md`](dev-security/claude-rules/languages/kotlin.md) — new pack rule file for Android applications written in Kotlin or Java. Covers secure storage (`EncryptedSharedPreferences`, `EncryptedFile`, manifest backup posture), cryptography (Android Keystore with StrongBox for Tier 1, AES-GCM, `SecureRandom`), authentication and local biometrics (`BiometricPrompt` with `CryptoObject` binding, `setInvalidatedByBiometricEnrollment`, Custom Tabs for OAuth), network and Network Security Configuration (cleartext denied, user-CA trust off, OkHttp `CertificatePinner` and `<pin-set>`), backend attestation (Play Integrity with backend verification), platform interaction (App Links over custom schemes, explicit intents for cross-app data, logging redaction), `WebView` hardening (origin allow-list, narrow `addJavascriptInterface`, file-access flags off), permissions and privacy (narrow scope, Photo Picker preference), distribution and signing (Play App Signing, ProGuard / R8, R8 mapping file preservation), in-app billing (`purchaseToken` server-side verification, acknowledgement gating), and reverse-engineering resistance (root detection as signal, R8 obfuscation, Frida / Xposed hook detection for Tier 1). Every section cross-references the implementing section of [`standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md). The opening note clarifies that [`languages/java.md`](dev-security/claude-rules/languages/java.md) remains the server-side Java rule file and is distinct from the Android-Java patterns documented here.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version `1.13.0`. The directory-structure ASCII tree gains an entry for [`languages/kotlin.md`](dev-security/claude-rules/languages/kotlin.md). The "Rule files and their scope" table gains a new row.
- [`README.md`](README.md): library version `2026.06.4 → 2026.06.5`; README version `1.7.142 → 1.7.143`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new pack file: zero findings on first attempt (no em-dashes, no `-ise` verbs, no bare "ensure", no sanitisation terms). Re-read the file in full to confirm each Section cross-reference points at actual content of [`standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md): Sections 2, 3, 4, 5 (including the new attestation row from Phase 1), 6, 7, 9, 10, 14. The version-date consistency audit (gate 29) confirms `2026.06.5` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

### Phased rollout context

This is Phase 3 of 8 in the mobile-app security work. Phases 4-7 add the cross-platform pack rule files: React Native, Flutter, .NET MAUI, Capacitor / Ionic.

---

## 2026-06-02, Library Version 2026.06.4

Mobile-app security work, Phase 2 of 8: first per-language pack rule file for mobile.

### Added

- [`dev-security/claude-rules/languages/swift.md`](dev-security/claude-rules/languages/swift.md) — new pack rule file for iOS applications written in Swift or Objective-C. Covers secure storage (Keychain accessibility classes, Data Protection classes, backup exclusion), cryptography (CryptoKit, Secure Enclave, `SecRandomCopyBytes`), authentication and local biometrics (biometry as step-up not sole credential, `ASWebAuthenticationSession`, biometry-current-set binding), network and ATS (scoped exceptions, certificate pinning via `URLSessionDelegate`), backend attestation (App Attest with backend verification), platform interaction (Universal Links over custom schemes, OSLog privacy markers), `WKWebView` hardening (origin allow-list, restricted bridges), App Tracking Transparency (honest prompts), code signing and distribution, in-app purchases (server-side `jwsRepresentation` verification per the new Section 14), and reverse-engineering resistance (jailbreak detection as a signal, compiler hardening defaults). Every section cross-references the implementing section of [`standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md).

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version `1.12.0`. The directory-structure ASCII tree gains an entry for the new file [`languages/swift.md`](dev-security/claude-rules/languages/swift.md); the existing entries for [`languages/csharp.md`](dev-security/claude-rules/languages/csharp.md) and [`languages/java.md`](dev-security/claude-rules/languages/java.md) are clarified as "(server-side)" to distinguish them from the new mobile-language rule files arriving in this and subsequent phases. The "Rule files and their scope" table gains a new row for the swift rule.
- [`README.md`](README.md): library version `2026.06.3 → 2026.06.4`; README version `1.7.141 → 1.7.142`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new pack file. Two findings caught and fixed pre-audit: one `-ise` verb (`recognising` → "with the caveat that") and one em-dash (replaced with a sentence break). Re-read the swift.md file in full to confirm each Section cross-reference points at the actual content of [`standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md): Section 2 storage, Section 3 cryptography, Section 4 auth, Section 5 network plus the new attestation row, Section 6 platform interaction, Section 7 MASVS-R, Section 9 distribution, Section 10 privacy, and Section 14 IAP (added in Phase 1). The version-date consistency audit (gate 29) confirms `2026.06.4` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

### Phased rollout context

This is Phase 2 of 8 in the mobile-app security work. Phases 3-7 add the remaining per-language pack rule files: Kotlin, React Native, Flutter, .NET MAUI, Capacitor / Ionic.

---

## 2026-06-02, Library Version 2026.06.3

Mobile-app security work, Phase 1 of 8: expand the mobile standard with three substantive additions that close 2024-2026 currency gaps. Per-doc version bumped `1.0.1 → 1.1.0` (minor bump per semver for added sections).

### Added

- [`dev-security/standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md) Section 5 gains a new "Backend attestation" row: iOS App Attest / DeviceCheck and Android Play Integrity for Tier 1 / Tier 2 backends, server-side verification, short-lived tokens, replay-protected. The attestation requirement is anchored to the existing sensitivity-tier model in Section 1; previously absent.
- [`dev-security/standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md) **new Section 13: hybrid and cross-platform frameworks**, naming React Native, Flutter, .NET MAUI, Capacitor / Ionic explicitly. Eight control rows covering secure storage delegation (the `react-native-keychain` / `flutter_secure_storage` / MAUI `SecureStorage` pattern over framework defaults like `AsyncStorage`), JS-or-Dart bridge as a trust boundary, native module review, debug-tooling exclusion in release builds, over-the-air update integrity (CodePush, EAS Update, Shorebird, Appflow Live Updates), Content Security Policy in wrapped WebViews, framework currency, and framework-specific build hardening. The opening paragraph states the rule that hybrid frameworks shift layers but do not reduce the set of controls.
- [`dev-security/standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md) **new Section 14: in-app purchases and receipt validation**. Eight control rows covering server-side validation against StoreKit / Google Play Developer API / Microsoft Store services, replay protection, price-tier validation, subscription state polling, sandbox-vs-production environment routing, refund / chargeback honour, restore-purchase flow constraints, and the boundary with side-loaded or web-checkout paths.

### Changed

- [`dev-security/standard-mobile-application-security.md`](dev-security/standard-mobile-application-security.md) per-document version `1.0.1 → 1.1.0`. "Operating expectations" section grows from 4 items to 7, adding bullets for annual attestation-flow verification (item 5), hybrid framework currency verification per release (item 6), and per-release IAP receipt-validation exercise (item 7).
- [`README.md`](README.md): library version `2026.06.2 → 2026.06.3`; README version `1.7.140 → 1.7.141`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the modified standard; no findings (no em-dashes, no `-ise` verbs, no bare "ensure", no sanitisation terms). Re-read the full standard after edits to confirm no contradiction between the new Section 5 attestation row, the new Section 13 hybrid-framework section, and the existing tier model in Section 1: Tier 1 and Tier 2 attestation requirements in Section 5 align with Section 1's sensitivity-tier definitions; Section 13's opening "do not reduce the set of controls" statement is consistent with Sections 2-10 remaining in force. The version-monotonicity audit (gate 13) confirms `1.0.1 < 1.1.0`. The version-date consistency audit (gate 29) confirms library `2026.06.3` matches `2026-06`. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

### Phased rollout context

This is Phase 1 of 8 in the mobile-app security work. Phase 0 ratified all v0.0.1 files to v1.0.1. Phases 2-7 add per-language pack rule files (Swift, Kotlin, React Native, Flutter, .NET MAUI, Capacitor / Ionic) that cite the now-complete standard.

---

## 2026-06-02, Library Version 2026.06.2

Mobile-app security work, Phase 0 of 8: project-wide ratification signal. All documents previously at v0.0.1 are bumped to v1.0.1 to signal that the content is no longer "first draft" status and is ratified for downstream use.

### Changed

- 54 documents bumped from `v0.0.1` to `v1.0.1`. Mechanical version-string + date-field change only; no content edits. Domains touched: `ai/` (5), `architecture/` (6), `compliance/` (1), `dev-security/` (2), `docs/` (1), `governance/` (7), `operations/` (4), `privacy/` (8), `resilience/` (5), `risk/` (4), `security/` (6), `supply-chain/` (5), plus repo-root [`CONTRIBUTING.md`](CONTRIBUTING.md). Each file's `**Date:**` field updated to `2026-06-02` to anchor the next review cycle.
- [`taxonomy.yml`](taxonomy.yml), [`docs/portal.md`](docs/portal.md), [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md) regenerated from the bumped metadata (CI `--check` mode would have failed otherwise per the gate-discipline rule).
- [`README.md`](README.md): library version bumped `2026.06.1` to `2026.06.2`; README version bumped `1.7.139` to `1.7.140`; date updated `2026-06-01` to `2026-06-02` (calendar rolled over).

### Why this is mechanical, not a content review

A 54-file content re-read is impractical in a single phase. Per the [`evidence-grounded-completion`](.claude/rules/governance/evidence-grounded-completion.md) rule, the verification scope is stated explicitly: this PR is a ratification signal, not a quality review. The version bump asserts "the maintainer considers these documents ready for downstream use as of `2026-06-02`"; it does not assert "every line has been re-read and verified." Subsequent reviews on each document's own review cadence (per [`governance/procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md)) provide the per-document content audit.

### Phased rollout context

This is Phase 0 of 8 in the mobile-app security work. Phases 1-7 follow:
1. Mobile standard expansion (App Attest, hybrid frameworks, IAP receipt validation).
2-7. Per-language pack rule files: Swift, Kotlin, React Native, Flutter, .NET MAUI, Capacitor/Ionic.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. The version-monotonicity audit (gate 13) confirms all 54 per-document bumps are increases (`0.0.1 < 1.0.1`). The version-date consistency audit (gate 29, shipped yesterday) confirms today's library version `2026.06.2` matches today's calendar month `2026-06`. The two generator-drift gates (30, 31) pass after regenerating [`taxonomy.yml`](taxonomy.yml) and the portal artefacts in this commit. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.06.1

Make the project's strict-mode stance on exceptions explicit in [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md), and document the `refs/preservation/` convention for the rare case of a legitimate protected-branch force-push. Both additions close gaps identified by the new pack governance rules: three pack rules reference a project "exception register" that this project does not maintain (the absence was implicit; now it is explicit), and one pack rule names the `refs/preservation/` namespace as the audit-trail convention for force-push exceptions (the convention is now documented so it can be followed without invention).

### Changed

- [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md) `## Boundaries` section gains two new bullets:
  - The first bullet makes explicit that this project offers no exception path for the audit gates or the pack rules under [`.claude/rules/governance/`](.claude/rules/governance/). The three pack rules that reference "the project's exception register" as an opt-out channel ([`gate-discipline`](.claude/rules/governance/gate-discipline.md), [`change-tracking`](.claude/rules/governance/change-tracking.md), [`evidence-grounded-completion`](.claude/rules/governance/evidence-grounded-completion.md)) find no such register; the strict-mode default each pack rule's exception section falls back to is the project's stance. This restates the absence so it is read as policy rather than oversight.
  - The second bullet documents the `refs/preservation/<short-reason>-<YYYY-MM-DD>/<original-ref-name>` namespace and the protected-branch force-push procedure from [`dev-security/claude-rules/governance/artefact-and-branch-discipline.md`](dev-security/claude-rules/governance/artefact-and-branch-discipline.md): document the technical reason, obtain governance-authority approval, notify collaborators, preserve the pre-rewrite ref, re-run the version-monotonicity audit. Costs nothing while not invoked; expensive to invent under pressure.
- [`README.md`](README.md): library version bumped `2026.06.0` to `2026.06.1` (same calendar month, patch counter increments per [`specification-master-project.md`](specification-master-project.md) section 4.5). README version bumped `1.7.138` to `1.7.139`.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. The new bullets in [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md) reside in the exempt `.claude/` subtree (per the `DEFAULT_EXEMPT_DIRS` constant in [`tools/lint_common.py`](tools/lint_common.py)), so the corpus linters do not scan them, but I re-read the two bullets in full to confirm they consistently describe what the pack rules say. The new gate 29 (Version-date consistency audit) passes: the bumped version `2026.06.1` matches today's date `2026-06-01` and the [`README.md`](README.md) field matches this CHANGELOG entry. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff). No infrastructure changes (no gate added, no rule file added); this is a pure governance-stance documentation change.

---

## 2026-06-01, Library Version 2026.06.0

Add a mechanical version-date consistency gate; bump to `2026.06.0` per [`specification-master-project.md`](specification-master-project.md) section 4.5; record the six-phase month discontinuity inherited from prior PRs.

### Added

- New gate 29: **Version-date consistency audit** ([`tools/lint-version-date-consistency.py`](tools/lint-version-date-consistency.py)) and its regression fixtures in [`tests/test_linters.py`](tests/test_linters.py). The gate enforces two invariants: (1) the most recent CHANGELOG section heading's date `YYYY-MM` must equal its `Library Version` `YYYY.MM`; (2) the [`README.md`](README.md) `**Library Version:**` field must equal the most recent CHANGELOG heading's version. The two CHANGELOG and README values are textually adjacent (same headings, same metadata block), so the comparison is purely lexical: no git plumbing, no commit-timestamp parsing, no CI-clock-vs-author-clock concerns.

### Changed

- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) section 6 inventory table: the new gate is inserted at position 29; the four gates previously at positions 29-32 (Machine-readable taxonomy in sync, Adopter portal and maturity scorecard in sync, Gate-name parity audit, Linter regression test suite) are renumbered to 30-33. Narrative text and the cross-references in sections 2 and 6.1 updated to reflect the new numbering.
- All four audit-programme surfaces ([`.github/workflows/quality.yml`](.github/workflows/quality.yml), [`tools/run_all_audits.sh`](tools/run_all_audits.sh), [`.pre-commit-config.yaml`](.pre-commit-config.yaml), and the spec inventory above) gain the new gate in the same ordered position, so the gate-name parity audit (now gate 32) remains clean.
- Inline `gate-32` regression-test-suite references in [`tools/lint-acronym-consistency.py`](tools/lint-acronym-consistency.py), [`tools/lint-citation-verification-freshness.py`](tools/lint-citation-verification-freshness.py), [`tools/lint-library-version-monotonicity.py`](tools/lint-library-version-monotonicity.py), [`tools/lint-roles.py`](tools/lint-roles.py), [`tools/lint-standards-currency.py`](tools/lint-standards-currency.py), [`tools/lint-structure.py`](tools/lint-structure.py), [`tools/lint-tooling-provenance-freshness.py`](tools/lint-tooling-provenance-freshness.py), [`tools/lint-audit-gate-parity.py`](tools/lint-audit-gate-parity.py), [`tools/run-linter-regression.py`](tools/run-linter-regression.py), and [`tests/README.md`](tests/README.md) updated to `gate-33` to track the regression suite's new position.
- Gate-count references "32 gates / 32-gate" updated to "33 gates / 33-gate" in [`governance/procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md), [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md), [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md), and the runner header in [`tools/run_all_audits.sh`](tools/run_all_audits.sh).
- [`README.md`](README.md): library version bumped `2026.05.144` to `2026.06.0` (the calendar-month component now matches today's date per [`specification-master-project.md`](specification-master-project.md) section 4.5; the patch counter resets to 0 because the month rolled over). README version bumped `1.7.137` to `1.7.138`.

### Corrective note: six-phase month discontinuity

The six phases of the dev-security pack scope expansion that landed on 2026-06-01 (library versions `2026.05.139` through `2026.05.144`, see the entries below this one in this file) all used the `2026.05.x` patch lineage, inherited from the prior PR's `2026.05.138` baseline. The [`specification-master-project.md`](specification-master-project.md) section 4.5 CalVer rule is that `YYYY.MM` is the year and month of the *merge to `main`*, with the patch counter resetting to 0 when the month rolls over. All six merges occurred on 2026-06-01 and should have started at `2026.06.0` and counted up. The existing version-monotonicity audit (gate 13) treats `2026.05.x` as monotonic (tuple comparison: `(2026, 5, 144) < (2026, 6, 0)`) and did not catch the month mismatch.

Per the [`artefact-and-branch-discipline`](dev-security/claude-rules/governance/artefact-and-branch-discipline.md) rule shipped in Phase 6 (no force-push to protected branches), the six historical entries are not rewritten. Each entry's `Date:` field already records the correct calendar date (2026-06-01), so a reader cross-referencing the section heading can see what actually happened. From this entry forward the project follows section 4.5 strictly, and the new gate 29 enforces it mechanically.

### Verification

Full 33-gate audit programme passes standalone immediately before commit. The new gate, run standalone on the current working tree, transitions from `FAIL` (against the pre-bump README + CHANGELOG state) to `PASS` (against the bumped state in this PR). The two new regression tests in [`tests/test_linters.py`](tests/test_linters.py) (`test_date_version_month_mismatch_flagged`, `test_readme_changelog_version_drift_flagged`) pass under `python3 -m unittest tests.test_linters.VersionDateConsistencyTests`. The gate-name parity audit (now gate 32) confirms the four surfaces all declare the new gate at the same ordered position. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.05.144

Phase 6 (final) of the dev-security pack scope expansion: fifth and last governance rule lands; the phased rollout announced at pack version 1.6.0 is complete.

### Added

- [`dev-security/claude-rules/governance/artefact-and-branch-discipline.md`](dev-security/claude-rules/governance/artefact-and-branch-discipline.md) — new pack rule codifying two related disciplines that protect a project's audit trail: (1) generated artefacts are read-only (never hand-edit; always regenerate from the source; commit source plus generated output together; CI verifies via `--check` mode); (2) protected branches are append-only (no direct push; no force-push; PR-only merges). The rule defines what counts as a generated artefact (build outputs, schema dumps, taxonomies, doc portals, lockfiles, generated tests), what counts as a protected branch (default branch, release branches, long-lived integration branches), the required workflows for each, prohibited anti-patterns (hand-editing generated files to skip a regeneration round-trip, regenerating in CI to bypass the drift check, stripping `--check` jobs, direct push to protected branches, force-push that drops version-bearing commits, merging without going through the PR mechanism), the version-monotonicity contract that binds branch protection as the primary defence and the version-monotonicity audit as the backstop, tool-specific guidance (CI invocation patterns, branch-protection settings checklist, lockfile updates, long-lived integration branches), exception-handling protocols for both generated-artefact and branch-protection exceptions (governance-authority approval, tracked-issue link, preservation of pre-rewrite refs under `refs/preservation/`, post-rewrite re-audit), and framework alignment (NIST SSDF PO.5/PW.4/PS.1/RV.1; CSA CCM CCC-01-04/AIS-04/LOG-02/LOG-08; ISO 27001 A.5.4/A.8.15/A.8.32; SLSA Level 2-3). Pack-distributable form of this project's `## Boundaries` rules on generated files and direct pushes to `main`; generalises into a project-agnostic discipline.
- [`.claude/rules/governance/artefact-and-branch-discipline.md`](.claude/rules/governance/artefact-and-branch-discipline.md) — project consumption copy.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.11.0. "Pack scope" section reflects rollout completion (all five governance rules shipped); directory-structure ASCII tree shows the five-rule governance subdirectory marked as "rollout complete"; "Rule files and their scope" table gains a new row.
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md) (pack drop-in payload) "## Development-governance discipline" section gains a fifth bullet for the artefact-and-branch-discipline rule. Closing paragraph updated to announce rollout completion.
- [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md) (project): rule-file list adds the new governance/artefact-and-branch-discipline.md bullet; pack-version paragraph updated from 1.10.0 to 1.11.0 and notes the phased rollout is complete with the five governance rules shipped. The new rule explicitly cross-references this project's `## Boundaries` rules on generated files ([`taxonomy.yml`](taxonomy.yml), the `docs/` portal, scorecards) and on direct pushes to `main` as the source material.
- [`README.md`](README.md): library version bumped 2026.05.143 to 2026.05.144; README version bumped 1.7.136 to 1.7.137.

### Phased rollout context

This is Phase 6 of 6, the final phase. With this release the phased governance rollout announced at pack version 1.6.0 is complete: gate-discipline (1.7.0), change-tracking (1.8.0), evidence-grounded-completion (1.9.0), clarify-before-acting (1.10.0), and artefact-and-branch-discipline (1.11.0). Future pack work may add rules under `governance/` as the discipline expands, but the planned set is shipped.

### Verification

Full 32-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new pack file with zero findings (no em-dashes, no -ise verbs, no bare "ensure", no sanitisation terms). The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff). The version-monotonicity audit confirms the library version sequence 2026.05.139 through 2026.05.144 across the six phases is strictly monotonic.

---

## 2026-06-01, Library Version 2026.05.143

Phase 5 of the dev-security pack scope expansion: fourth governance rule lands.

### Added

- [`dev-security/claude-rules/governance/clarify-before-acting.md`](dev-security/claude-rules/governance/clarify-before-acting.md) — new pack rule codifying "when a request has more than one reasonable interpretation, or an external value the request does not pin down is required to proceed, surface the ambiguity in one sentence and ask before acting." The rule defines five ambiguity-detection categories (multi-interpretation requests, missing external values, project-convention choices, trade-offs, unclear world state), distinguishes when to ask versus when to use sensible defaults (ask when a wrong choice produces unwindable work or has consequences beyond this PR; default when a convention exists and the wrong-guess cost is bounded), specifies how to ask (one sentence, named alternatives, recommended option labelled and listed first, consequence stated), enumerates prohibited anti-patterns (silently picking, asking after acting, asking trivia, hiding ambiguity in narration, treating prior authorisation as durable when scope changed, leading-recommendation theatre, questions that require scrolling), gives tool-specific guidance for AI coding assistants (structured-question primitives, plan mode, investigation-first when state is unclear, scope-creep surfacing), enumerates exception cases (pre-authorised durable instructions like a project CLAUDE.md memory file, emergency response, reversible exploration), and provides framework alignment (NIST SSDF PO.1/PO.5/RV.1/RV.2, CSA CCM GRC-01/GRC-04/IAM-09/TVM-01/CCC-01-03, ISO 27001 A.5.1/A.5.4/A.5.15/A.5.18/A.5.27/A.8.16/A.8.32). Pack-distributable form of this project's `## Behavioral rule: clarify before acting` section; generalises that rule into a project-agnostic discipline.
- [`.claude/rules/governance/clarify-before-acting.md`](.claude/rules/governance/clarify-before-acting.md) — project consumption copy of the same rule.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.10.0. "Pack scope" section now lists four shipped governance rules with their pack-version timing and names the final rollout rule (artefact-and-branch discipline) as the next phase. Directory-structure ASCII tree shows all four populated; "Rule files and their scope" table gains a new row.
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md) (pack drop-in payload) "## Development-governance discipline" section gains a fourth bullet for the clarify-before-acting rule.
- [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md) (project): rule-file list adds the new governance/clarify-before-acting.md bullet; pack-version paragraph updated from 1.9.0 to 1.10.0 and lists all four shipped governance rules. The new rule explicitly cross-references this project's `## Behavioral rule: clarify before acting` section as the source.
- [`README.md`](README.md): library version bumped 2026.05.142 to 2026.05.143; README version bumped 1.7.135 to 1.7.136.

### Phased rollout context

This is Phase 5 of 6. The final phase will add artefact-and-branch discipline (the unifying rule covering "never hand-edit generated artefacts; never push directly to protected branches; respect version-monotonicity"), completing the planned governance overlay.

### Verification

Full 32-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new pack file; one finding ("optimise" -> "optimize") fixed before the audit sweep. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.05.142

Phase 4 of the dev-security pack scope expansion: third governance rule lands.

### Added

- [`dev-security/claude-rules/governance/evidence-grounded-completion.md`](dev-security/claude-rules/governance/evidence-grounded-completion.md) — new pack rule codifying "never declare work done, fixed, ready, shipped, or any synonym without evidence." The rule defines what counts as a completion claim (state assertions a reader will rely on, including "good catch" used to acknowledge a user-reported issue), enumerates the synonym vocabulary that triggers the protocol, specifies the six-step verification protocol (enumerate files in scope, re-read each in full, quote supporting lines with path-and-line-number citations, proactively search for contradictions, distinguish mechanical gate verification from semantic verification, state unverified items explicitly), enumerates prohibited anti-patterns (declaring victory in the response that carries failing evidence, treating user silence as confirmation, relying on prior runs, premature "good catch", pipe-masked exit codes, conflating "I edited the file" with "the file is correct"), gives tool-specific guidance for AI coding assistants (reading tool results before composing summaries, waiting for async work, `set -o pipefail` and `${PIPESTATUS[@]}` for pipe-masked exit codes, stop hooks, self-honesty in summaries), the exception-handling protocol for impractical re-reads, and framework alignment (NIST SSDF RV.1/RV.2/PO.5/PS.1, CSA CCM GRC-04/GRC-05/LOG-02/LOG-08, ISO 27001 A.5.4/A.5.36/A.8.15, OWASP ASVS V1.1/V14.1). Pack-distributable form of the user-level Rule 6 added 2026-05-31 in the maintainer's private global Claude Code memory file; generalises that rule into a portable, project-agnostic discipline.
- [`.claude/rules/governance/evidence-grounded-completion.md`](.claude/rules/governance/evidence-grounded-completion.md) — project consumption copy of the same rule.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.9.0. "Pack scope" section now lists three shipped governance rules with their pack-version timing; directory-structure ASCII tree shows all three populated; "Rule files and their scope" table gains a new row. The scope-bullet contract description rephrased from "agent-collaboration discipline" to its two component rules (evidence-grounded completion and clarify-before-acting) so the broadened contract is concretely visible.
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md) (pack drop-in payload) "## Development-governance discipline" section gains a third bullet for the evidence-grounded-completion rule with a one-line summary of the six-step protocol. Downstream adopters who drag the payload now inherit all three governance rules.
- [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md) (project): rule-file list adds the new governance/evidence-grounded-completion.md bullet; pack-version paragraph updated from 1.8.0 to 1.9.0 and lists all three shipped governance rules. The project's user-level Rules 1-5 (verification before dependent actions, tool-result authority, async waiting, pre-commit-hook respect, self-honesty) and Rule 6 (the evidence-grounded completion rule itself) are referenced as the pre-existing per-user discipline that this pack rule now codifies for cross-project adoption.
- [`README.md`](README.md): library version bumped 2026.05.141 to 2026.05.142; README version bumped 1.7.134 to 1.7.135.

### Phased rollout context

This is Phase 4 of 6. Phases 5 through 6 will add: clarify-before-acting discipline, and artefact-and-branch discipline.

### Verification

Full 32-gate audit programme passes standalone immediately before commit. Ran [`tools/lint-language.py`](tools/lint-language.py) standalone on the new pack file and confirmed no findings (no em-dashes, no -ise verbs, no bare "ensure", no sanitisation terms). Searched the new file for the synonym vocabulary the rule itself defines (`done`, `complete`, `fixed`, etc.) and confirmed all occurrences are either in the rule's own enumeration of trigger words or in prose that names the failure mode rather than claiming the rule's own work is done; the rule does not falsify itself. The D1 CHANGELOG-on-PR delta gate passes ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.05.141

Phase 3 of the dev-security pack scope expansion: second governance rule lands.

### Added

- [`dev-security/claude-rules/governance/change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) — new pack rule codifying "every change to user-visible content carries a CHANGELOG entry by default." The rule specifies what an entry must contain (date and version header, structured sections following Keep a Changelog, linked file references, the "why" not only the "what", verification evidence, phase context for multi-PR rollouts), the sanctioned opt-out path (a `Changelog: skip (reason: ...)` trailer in the commit or PR description, reviewer-approved), prohibited anti-patterns (silent changes, vague entries, batched-up entries, retroactive entries, entries with unlinked file references, misclassified breaking changes, verbatim commit-message copy, gate bypass via `--no-verify`), the three mechanical CI gates that enforce the discipline (delta gate, link-coverage gate, version-monotonicity gate), tool-specific guidance (git trailers, monorepo coordination, generated CHANGELOGs, document corpora), an exception-handling protocol consistent with the gate-discipline rule, and framework alignment (NIST SSDF PO.5/PS.1/RV.1/RV.2, CSA CCM CCC-01-04/LOG-02/LOG-08, ISO 27001 A.5.4/A.8.15/A.8.27/A.8.32). Generalises this project's D1 CHANGELOG-on-PR delta gate, the CHANGELOG link-coverage audit, and the version-monotonicity audit into a portable, pack-distributable discipline applicable to any project with a CHANGELOG.
- [`.claude/rules/governance/change-tracking.md`](.claude/rules/governance/change-tracking.md) — project consumption copy of the same rule. The pack file is canonical; this copy is what Claude Code loads at session start when working on this project.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.8.0. "Pack scope" section updated to list both shipped governance rules with their pack-version timing. Directory-structure ASCII tree shows the change-tracking rule populated alongside gate-discipline. "Rule files and their scope" table gains a new row for the change-tracking rule.
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md) (pack drop-in payload) "## Development-governance discipline" section gains a second bullet for the change-tracking rule with a one-line summary of its contract. Downstream adopters who drag the payload now inherit both governance rules.
- [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md) (project): rule-file list adds the new governance/change-tracking.md bullet; pack-version paragraph updated from 1.7.0 to 1.8.0 and notes the second governance rule.
- [`README.md`](README.md): library version bumped 2026.05.140 to 2026.05.141; README version bumped 1.7.133 to 1.7.134.

### Phased rollout context

This is Phase 3 of 6. Phase 1 (Library 2026.05.139) announced the broadened contract; Phase 2 (Library 2026.05.140) shipped gate-discipline. Phases 4 through 6 will add: evidence-grounded completion, clarify-before-acting, and artefact-and-branch discipline.

### Verification

Full 32-gate audit programme passes standalone immediately before commit. The new pack rule file lives under `dev-security/claude-rules/governance/` and is scanned by [`tools/lint-language.py`](tools/lint-language.py); ran the linter standalone on the file and confirmed no findings (no em-dashes, no -ise verbs, no bare "ensure", no sanitisation terms). The project consumption copy lives in the exempt `.claude/` subtree. The D1 CHANGELOG-on-PR delta gate passes on this PR ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.05.140

Phase 2 of the dev-security pack scope expansion: first governance rule lands.

### Added

- [`dev-security/claude-rules/governance/gate-discipline.md`](dev-security/claude-rules/governance/gate-discipline.md) — new pack rule codifying "never weaken or delete a gate to silence a failure; fix the artefact." The rule enumerates prohibited responses to a failing gate (`--no-verify`, severity-threshold lowering, exemption-list dumping, blanket suppressions, assertion-to-logging downgrades, marking real gates non-required, exit-code swallowing, flake-normalisation), correct responses in order of preference (fix the artefact; fix the gate if it is wrong; documented temporary exception; environmental re-run), tool-specific anti-patterns (git, lint, type-check, tests, CI/CD config, generator-output drift), an exception-handling protocol that the rule is consistent with, and framework alignment (OWASP ASVS, NIST SSDF, CSA CCM, ISO 27001). Generalises the project's `## Boundaries` rule ("Never weaken or delete an audit gate to make a document pass; fix the document") into a portable, pack-distributable form applicable to any project with CI gates, audit programmes, or branch protections.
- [`.claude/rules/governance/gate-discipline.md`](.claude/rules/governance/gate-discipline.md) — project consumption copy of the same rule. The pack file is canonical; this copy is what Claude Code loads at session start when working on this project.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.7.0. "Pack scope" section updated from "will live under" to "lives under" the `governance/` subdirectory; explicit reference to the first landed rule. Directory-structure ASCII tree now shows the gate-discipline rule populated. "Rule files and their scope" table gains a new row for the gate-discipline rule.
- [`dev-security/claude-rules/CLAUDE.md`](dev-security/claude-rules/CLAUDE.md) (pack drop-in payload) gains a new "## Development-governance discipline" section before "## Framework basis" referencing the new rule. Downstream adopters who drag the pack drop-in payload into their project now inherit the gate-discipline rule alongside the existing security rules.
- [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md) (project): rule-file list gains the new governance/gate-discipline.md bullet; preamble paragraph updated from "pack version 1.6.0 announces" to "pack version 1.7.0 covers ... 1.7.0 delivered the first governance rule." Subsequent governance rules to be listed as they land.
- [`README.md`](README.md): library version bumped 2026.05.139 to 2026.05.140; README version bumped 1.7.132 to 1.7.133.

### Phased rollout context

This is Phase 2 of 6. Phase 1 (Library 2026.05.139) announced the broadened contract. Phases 3 through 6 will add: change-tracking discipline, evidence-grounded completion, clarify-before-acting, and artefact-and-branch discipline.

### Verification

Full 32-gate audit programme passes standalone immediately before commit. The new pack rule file lives in the exempt `dev-security/claude-rules/` subtree and is not subject to corpus linters; the project consumption copy lives in the exempt `.claude/` subtree and is likewise not subject to corpus linters. The D1 CHANGELOG-on-PR delta gate passes on this PR ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.05.139

Phase 1 of the dev-security pack scope expansion: announce broadened contract from security-only to security + development-governance discipline.

### Changed

- [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) bumped to pack version 1.6.0 (2026-06-01). The opening "What are these files?" section now describes the pack as carrying "security and development-governance context" rather than security context alone. A new "Pack scope" section near the top of the README articulates the two scope families (security/compliance under `core/`, `ai/`, `pipeline/`, `languages/`; development-governance discipline under a new `governance/` subdirectory) and the reason the pack directory name remains `dev-security/` (developer discoverability — developers shop for "security rules," not for "GRC rules" or "development discipline"). The directory-structure ASCII tree now includes the `governance/` subdirectory as an announced-but-unpopulated entry; the tree is the directory layout contract for the phased rollout.
- [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md) `## Security requirements` heading renamed to `## Security and governance requirements`; a new paragraph below the existing rule-file bullets announces the pack's broader contract and clarifies that this project's loaded rules are unchanged in Phase 1 (this project's own governance discipline is already encoded in the existing `## Boundaries` and `## Behavioral rule` sections plus the 32-gate audit programme).

### Phased rollout context

This is the first of a six-phase rollout that broadens the [`dev-security/claude-rules/`](dev-security/claude-rules/README.md) pack from security-only to security + development-governance discipline:

1. **Phase 1 (this release).** Announce the broadened contract; introduce the governance subdirectory in the documented layout. No new rule files.
2. **Phase 2.** Add a gate-discipline rule that codifies "never weaken or delete a gate to silence a failure; fix the artefact" as a portable pack rule.
3. **Phase 3.** Add a change-tracking discipline rule that codifies the CHANGELOG-on-PR pattern with opt-out trailers, citing the D1 delta gate shipped in Library 2026.05.138.
4. **Phase 4.** Add an evidence-grounded-completion rule that lifts the user-level Rule 6 ("completion claims require evidence-grounded verification") into a portable, shareable rule.
5. **Phase 5.** Add a clarify-before-acting rule that lifts the Karpathy-adapted rule from this project's [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md) into a portable pack file.
6. **Phase 6.** Add an artefact-and-branch-discipline rule that bundles no-hand-editing-generated-artefacts, no-direct-push-to-protected-branches, and the version-monotonicity contract.

Each phase is shipped as its own pull request with its own CHANGELOG entry and library version bump. Per-PR cycle cost is accepted as the price of better per-rule reviewability and assurance.

### Verification

Full 32-gate audit programme passes standalone immediately before commit; new D1 CHANGELOG-on-PR delta gate (Library 2026.05.138) passes on this PR ([`CHANGELOG.md`](CHANGELOG.md) is in the diff).

---

## 2026-06-01, Library Version 2026.05.138

CHANGELOG enforcement gate and prior-PR catch-up entry.

### Added

- New CI-only delta gate **D1: CHANGELOG-on-PR check** ([`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py)) that fails a pull request when the diff against the merge-base with the target branch does not include [`CHANGELOG.md`](CHANGELOG.md). An opt-out trailer `Changelog: <one-line-reason>` in any commit message body in the PR range satisfies the gate. The gate runs only on `pull_request` events in [`.github/workflows/quality.yml`](.github/workflows/quality.yml); it is not part of the 32-gate corpus audit programme and is exempt from gate 31's name-parity audit because its inputs (git history range, PR base ref) are unavailable in [`tools/run_all_audits.sh`](tools/run_all_audits.sh) and [`.pre-commit-config.yaml`](.pre-commit-config.yaml).
- [`.github/workflows/quality.yml`](.github/workflows/quality.yml) checkout step now uses `fetch-depth: 0` so the delta gate can resolve the merge-base.
- [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) §6.1 documents the new PR-only delta gate category and the opt-out trailer convention.

### Changed

- Catch-up entry for prior PR #5 ([`d1fb4d0`](https://github.com/jposluns/grc_library/commit/d1fb4d0)): added a "Behavioral rule: clarify before acting" section to [[`.claude/CLAUDE.md`](.claude/CLAUDE.md)](.claude/CLAUDE.md), adapted from [Karpathy's "Think Before Coding" CLAUDE.md rule](https://github.com/multica-ai/andrej-karpathy-skills) (MIT-licensed). The rule was merged without a CHANGELOG entry; this entry records it retroactively. The new D1 gate above prevents this miss from recurring.

### Verification

Full audit programme (32 gates) and regression suite (70 tests) run standalone immediately before commit: all green. The new D1 gate is exercised by this PR itself: this PR modifies [`CHANGELOG.md`](CHANGELOG.md), so D1 passes; if it had not, D1 would have blocked merge.

---

## 2026-05-31, Library Version 2026.05.137

Corpus-wide hyperlink sweep and TODO.md cleanup.

### Changed

- Converted 414 unlinked backtick-wrapped file references to markdown links across 48 files (root specs, governance, compliance, security, privacy, resilience, operations, supply-chain, dev-security, ai, docs, tools). Detection extends the existing [`tools/lint-changelog-link-coverage.py`](tools/lint-changelog-link-coverage.py) regex across every markdown file. Resolution order: relative to source dir, relative to repo root, tail-path match, then unique-basename fallback. Adopter-project filenames (Claude rule files, AGENTS files, package manifests), placeholder patterns containing angle brackets / braces / wildcards, command-line invocations, and references to deleted or external-project files are intentionally left as code-formatted text. 43 residual code-formatted references remain by design.
- Removed stale early-project artefacts from [`TODO.md`](TODO.md): P1/P2/P3 placeholder sections (phase references no longer mapped to the public-release history), P6.2 OT/ICS (verifiably complete in [`operations/ot/`](operations/ot/)), and phase-number prefixes on Decisions log entries. Rephrased P6.1 to focus on the remaining multi-cloud governance gap (per-cloud baselines already shipped in [`dev-security/`](dev-security/)). Nuanced P5.7 (Saudi Arabia annex exists; Argentina/Mexico in the Latin America annex) and P5.8 (US/China AI rules already partially covered in the respective privacy annexes).

### Fixed

- One-line content-generation typo in [`tools/README.md`](tools/README.md) introduced by an earlier direct-to-main MCP push: line 28 `# restrict scope to specific paths` corrected to `# regen-and-check`.

### Verification

Full audit programme (32 gates) and regression suite (70 tests) run standalone immediately before commit: all green.

---

## Initial public release (2026-05-31, Library Version 2026.05.136): CC BY-SA 4.0

First public commit of the Governance, Risk, and Compliance Documentation Library, published under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0). See [`LICENSE`](LICENSE) for the full legal code and [`NOTICE.md`](NOTICE.md) for the repository's external-reference boundary.

### Acknowledgements

The substance of this library draws on knowledge, experience, war stories, and patient mentorship accumulated over more than two decades by a community of GRC and security practitioners, with roots going back to the early 2000s. See [`AUTHORS.md`](AUTHORS.md) for the acknowledged contributors and the maintainer's attribution preference.

Corrections, contributions, and additional acknowledgements are welcomed via the workflow in [`CONTRIBUTING.md`](CONTRIBUTING.md).

### Verification

Full audit programme (32 gates) and regression suite (70 tests) run standalone immediately before commit: all green.
