# Overnight PR — Library Fitness Review Skill

**Started**: 2026-06-21 (overnight session, maintainer asleep)
**Status (live)**: in progress — building skill files

This file documents work performed autonomously while the maintainer was unavailable. Every meaningful design choice is recorded with rationale so the maintainer can audit judgement at breakfast.

## Authorisation scope (per maintainer's 2026-06-21 message)

- Build `/fitness` skill end-to-end with maximum thoroughness within library-quality-review scope.
- PR + 60s wait + CI green + merge authorised.
- Run `/validate` after merge.
- **DO NOT** change any corpus files without authorisation. Corpus = domain dirs (`ai/`, `architecture/`, `compliance/`, `dev-security/<non-pack>`, `governance/`, `operations/`, `privacy/`, `resilience/`, `risk/`, `security/`, `supply-chain/`) and `dev-security/claude-rules/` content outside the new skill's subdirectory. Authorised additions: the new skill subdir, slash command, `.working/fitness-reviews/` activity dir, pack README touchpoints, linter wiring, version bumps, CHANGELOG entry, regenerated artefacts.
- Any ambiguity → this file, not unilateral resolution.

## Design decisions made

### Persona count: 10 (the original 7 + 3 high-value additions)

| # | Persona | Scope | Why included |
|---|---------|-------|--------------|
| 1 | First-time executive reader | Strategic comprehension, purpose, audience, decision points | Original 7 |
| 2 | Security practitioner | Technical security adequacy, OWASP/ASVS alignment, threat-model coverage | Original 7 |
| 3 | GRC practitioner | Governance/risk/compliance discipline, control objectives, evidence paths | Original 7 |
| 4 | Auditor / assurance reviewer | Audit-readiness: testable controls, evidence locations, exception handling | Original 7 |
| 5 | Policy and standards editor | Editorial: naming conventions, requirement-language consistency, terminology | Original 7 |
| 6 | Process owner / operational user | Usability for actual execution: roles, procedures, checklists, decision points | Original 7 |
| 7 | Skeptical reader | Ambiguity, contradictions, gaps, unusable content, "so what?" tests | Original 7 |
| 8 | **Adoption practitioner** | Closest to library's real use case: someone actually setting up a GRC programme from this | Added: the original 7 evaluate the library FROM a perspective; this one tests USING the library. Different lens. |
| 9 | **Privacy / data protection officer** | Privacy domain depth: DPO-specific obligations, jurisdiction-aware controls, data-subject rights | Added: privacy is a large library surface; GRC practitioner covers it only at programme level, not DPO-specific |
| 10 | **Newcomer / onboarding engineer** | Zero-knowledge reader: jargon-free comprehension, onboarding friction | Added: executive persona assumes business literacy; this one is true zero-knowledge |

**Cap at 10**: more personas dilutes each subagent's focus and inflates synthesis. If you want more, follow-up PR can add (security architect, accessibility reviewer, translation/localisation reviewer, legal counsel, AI ethics reviewer are candidates I considered and deferred).

### Personas deliberately EXCLUDED from this iteration

- **Security architect**: overlap with security practitioner; the latter's scope was widened to include architecture.
- **AI ethics reviewer**: overlap with GRC practitioner's coverage of AI governance content.
- **Accessibility reviewer**: would warrant a separate "documentation accessibility" review skill; out of fitness-review scope.
- **Legal counsel**: substantive interpretation of jurisdiction-specific law is beyond a quality-review skill.
- **Translation/localisation reviewer**: only relevant if the library is being prepared for translation; deferred until that's planned.

### Severity model

Confirmed per earlier discussion: SARIF-lite (High/Medium/Low/FYI) with `[critical]` flag inside the High tier for audit-failure / regulatory-exposure / control-failure class findings. Format: `[high][critical] file:line — description`.

### Output structure

Single combined file per run at `.working/fitness-reviews/YYYY-MM-DD-rN.md` (canonical activity layout per PR #118). Eight H2 sections following the original prompt:

1. `## Executive Summary`
2. `## Review Method`
3. `## Page-by-Page Findings`
4. `## Cross-Library Findings`
5. `## Severity Model`
6. `## Recommendations` (priority-grouped)
7. `## Standardization Recommendations`
8. `## Remediation Backlog` (discrete IDs `FR-1`, `FR-2`, ...)

Plus `## Final Assessment` if the prompt's section 9 produces actionable content; otherwise folded into section 1. Decision deferred to actual content.

### Cadence triggers (documented in skill's When-to-Use section)

- After major changes (new domain dir, new document type, ≥3 governance rule additions, major restructure)
- Quarterly minimum (default if no major changes triggered it)
- Pre-publication / pre-external-share
- Manual trigger at any time

### What this skill is NOT

Deliberate scope boundaries:

- **Not a per-PR gate** (the validation-sweep is). Fitness review runs on demand or periodically, not on every PR.
- **Not a security audit** (that's `security-review` skill territory).
- **Not a citation-verification campaign** (that has its own register and worklist process).
- **Not a fact-check of external standards** (per Citation Verification Specification §14, the library does not verify standard content vs. library interpretation).
- **Not enforced by a mechanical gate** — it's a deliverable that informs human prioritisation.

## Files being authored / modified

### New (pack content, per maintainer authorisation for this skill)

- `dev-security/claude-rules/skills/library-fitness-review/SKILL.md` — full 8-section skill per `skill-authoring-discipline`
- `.claude/commands/fitness.md` — slash command

### New (working state, exempt from corpus gates)

- `.working/fitness-reviews/README.md` — activity convention info (personas, file format, severity, output flow, fork guidance)
- `.working/fitness-reviews/history.md` — empty cumulative table

### Modified (pack metadata only)

- `dev-security/claude-rules/README.md` — directory tree row, "When to use each skill" row, version-history row, pack version `1.29.0 → 1.30.0`
- `tools/lint-paired-skill-step-parity.py` — `PAIRS` table entry
- `tools/lint-collection-enumeration-consistency.py` — IF it enumerates skills (will verify)
- `.working/README.md` — activity table row

### Modified (meta files only)

- `CHANGELOG.md` — entry
- `README.md` — library version `2026.06.104 → 2026.06.105`; README version `1.8.60 → 1.8.61`
- Regenerated: `taxonomy.yml`, `docs/portal.md`, `docs/maturity-scorecard.md`

## Files NOT touched (corpus boundary respected)

- All `ai/`, `architecture/`, `compliance/`, `governance/`, `operations/`, `privacy/`, `resilience/`, `risk/`, `security/`, `supply-chain/` content
- `dev-security/standard-*.md`, `dev-security/guideline-*.md`, `dev-security/policy-*.md`, `dev-security/register-*.md` (corpus dev-security)
- `dev-security/claude-rules/` outside the new skill subdir (governance rules, core security rules, AI rules, languages, pipeline, other skills)
- Other `tools/lint-*.py` files (only the two enumeration-related linters above touched)

## Open ambiguities surfaced (for morning review)

*(will populate as I encounter them; will not unilaterally resolve)*

## Build progress

- [x] Skeleton overnight-pr.md (this file)
- [x] `.working/fitness-reviews/README.md` — convention info, ten-persona catalogue, severity model, output flow
- [x] `dev-security/claude-rules/skills/library-fitness-review/SKILL.md` — full 8-section skill per `skill-authoring-discipline`
- [x] `.claude/commands/fitness.md` — slash command with 9-step process matching SKILL.md
- [x] `.working/fitness-reviews/history.md` — empty cumulative table
- [x] `.working/README.md` activity table update
- [x] `dev-security/claude-rules/README.md` directory tree entry + pack version `1.29.0 -> 1.30.0` + version-history row
- [x] `tools/lint-paired-skill-step-parity.py` PAIRS entry for fitness skill + slash command
- [x] `tools/lint-collection-enumeration-consistency.py` check (no code change needed; gate auto-detects new skill in dir tree)
- [x] Library version `2026.06.104 -> 2026.06.105`; README version `1.8.60 -> 1.8.61`
- [x] CHANGELOG entry (full structured format; lead paragraph + Added + Changed + Design decisions + Verification)
- [x] Regenerate taxonomy.yml, docs/portal.md, docs/maturity-scorecard.md
- [x] Audit pass (all 44 gates pass standalone)
- [ ] Commit + push + PR
- [ ] Wait 60s + CI green + merge
- [ ] Sync main
- [ ] Run `/validate` (Sweep 10 iter 2)
- [ ] Address any /validate findings (if in-window prose drift, fix; if substantive, defer to maintainer)
- [ ] Final summary in this file

## Notes for morning review

*(will populate before signing off)*
