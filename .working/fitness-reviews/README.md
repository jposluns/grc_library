# `.working/fitness-reviews/` — Maintainer Working State

This subdirectory holds project-specific working state for the `library-fitness-review` discipline. The discipline itself (persona definitions, review criteria, severity model, output structure) is template content and lives in the [`library-fitness-review` skill](../../dev-security/claude-rules/skills/library-fitness-review/SKILL.md) in the dev-security claude-rules pack; the files here are *our* log of *our* fitness reviews performed against THIS library.

Adopters cloning the library inherit no historical fitness-review entries (their own review history starts at zero when they first invoke `/fitness` in their own fork).

## Files in this subdirectory

| File | Purpose |
|---|---|
| `README.md` | This file: static convention info that applies to every fitness review |
| `history.md` | Reverse-chronological table of every fitness review: date, run ordinal, personas dispatched, finding counts, resulting PR (if findings), one-line summary. New rows on top. |
| `YYYY-MM-DD-rN.md` | Per-run detail file. **Created only when the run produced findings.** Captures the full 8-section combined report (executive summary through remediation backlog). Zero-finding runs leave only a row in `history.md`. |

## Per-run detail file format

When a fitness review produces findings, the detail file uses these eight H2 sections in order:

1. `## Executive Summary` — overall comprehensibility, usability, consistency; highest-risk issues; remediation priorities; fit-for-use assessment
2. `## Review Method` — number and type of personas dispatched; pages reviewed; evaluation criteria applied; assumptions or limitations
3. `## Page-by-Page Findings` — per-page entries with title, path, intended purpose (as inferred), actual clarity, intended audience (as inferred), key issues, severity, impact, recommended remediation, retention decision (retain / revise / merge / split / rename / retire / relocate)
4. `## Cross-Library Findings` — systemic issues: terminology inconsistencies, structural problems, missing document types, duplicated/conflicting guidance, navigation weaknesses, broken or weak cross-linking, inconsistent requirement language, missing ownership or review metadata, unclear hierarchy
5. `## Severity Model` — explicit definitions used in this run (see "Severity model" below for the canonical definitions; this section restates them so the report is self-contained)
6. `## Recommendations` — priority-grouped with recommendation, rationale, affected pages, expected benefit, estimated effort (Small/Medium/Large), suggested owner, dependencies, proposed implementation order
7. `## Standardization Recommendations` — page taxonomy, naming conventions, required metadata, required page sections, requirement-language rules, ownership model, review cadence, cross-linking model, versioning model, status labels, template recommendations
8. `## Remediation Backlog` — discrete work items with IDs (`FR-1`, `FR-2`, ...), title, description, severity, affected pages, recommended action, acceptance criteria, estimated effort, dependencies

Optional `## Final Assessment` section as a coda when sections 1 and 6-8 leave material to summarise (fit-for-use, fit-for-audit-support, fit-for-executive-consumption, fit-for-operational-execution).

Filename `YYYY-MM-DD-rN.md` where `N` is the run ordinal on that date (default `r1`; increment if multiple runs in one day).

## Why the split (history table + optional per-run detail)

- The table is a fast scan of "what reviews ran and when, with what outcome and what remediation backlog". The maintainer reading `history.md` learns trajectory without paging through full reports.
- The detail files are the persistent archive for runs that actually surfaced findings. Reconstructible audit trail.
- Zero-finding runs leave no detail file because there is no substantive content beyond "we ran the review and the library is in good shape". The history row alone is enough.

## Personas (mirror of the library-fitness-review skill's catalogue)

Each fitness review dispatches independent persona subagents who review every page from a fresh-reader perspective. The personas are deliberately diverse to surface different failure modes:

| # | Persona | Scope | Focus questions |
|---|---------|-------|-----------------|
| 1 | First-time executive reader | Strategic comprehension, purpose, decision rights | Can a non-expert executive understand purpose, audience, required action? Does the page support decision-making? |
| 2 | Security practitioner | Technical security adequacy | OWASP/ASVS alignment? Threat-model coverage? Control objectives operationalised? Cryptography choices current? |
| 3 | GRC practitioner | Governance/risk/compliance discipline | Risk ownership clear? Control ownership clear? Compliance obligations cited? Exception paths documented? Evidence expectations explicit? |
| 4 | Auditor / assurance reviewer | Audit-readiness | What must be true? Who is responsible? What evidence proves it? Where is evidence stored? How often reviewed? What constitutes non-compliance? |
| 5 | Policy and standards editor | Editorial consistency | Naming conventions? Requirement-language consistency (must/should/may)? Terminology? Formatting? Document-type prefixes? Versioning? |
| 6 | Process owner / operational user | Usability for execution | Do I know what to do next? Are roles explicit? Are decision points clear? Are procedures actionable? Are templates sufficient? |
| 7 | Skeptical reader | Ambiguity, contradictions, gaps | What only makes sense to the original author? Where would a reader lose trust? What feels incomplete? Where do I ask "so what?"? |
| 8 | Adoption practitioner | Real-world adoption | Can I actually use this to set up a GRC programme? What's missing if I'm a small organisation? A large one? A regulated sector? Where do I start? |
| 9 | Privacy / data protection officer | Privacy-specific obligations | Data subject rights covered? Jurisdiction-aware? Cross-border transfer guidance? DPIA triggers? Breach notification thresholds? Vendor processor obligations? |
| 10 | Newcomer / onboarding engineer | Zero-knowledge entry | What jargon is unexplained? Where does the document assume prior context I don't have? Can I follow the navigation without a guide? What's the minimum reading order? |

Each persona has explicit exclusions to avoid overlap — see the skill's SKILL.md `## Process` step 3 for per-persona scope and exclusion definitions.

## Dispatch declaration

Every fitness-review run declares which personas were dispatched in the `Personas` column of `history.md`. Full runs dispatch all 10. Scoped runs (rare; require explicit maintainer authorisation in the Summary cell) dispatch a subset; the unsanctioned skip of a persona is a discipline failure equivalent to the validation-sweep's Rule 5.6.

## Severity model

| Severity | Meaning | Examples |
|---|---|---|
| **High** | Materially impairs usability, consistency, authority, accountability, or implementation. Action required before the next major reliance event (publication, external share, audit). | Missing role ownership, conflicting guidance across documents, unclear authority, requirement language inconsistent enough to cause misimplementation |
| **High `[critical]`** | Could cause serious misunderstanding, incorrect execution, audit failure, control failure, regulatory exposure, or operational misuse. Action required immediately. | Page that, if relied on for an audit, would produce a non-compliance finding; a control that's unenforceable as written; a requirement that contradicts a regulator's published guidance |
| **Medium** | Creates confusion, inefficiency, maintenance burden, or inconsistent interpretation. Action required in next review cycle. | Inconsistent terminology between two documents that reference the same concept; an unexplained acronym; a procedure step that's ambiguous |
| **Low** | Editorial, formatting, labelling, or minor clarity issues. Worth correcting but does not materially impair use. | Typo in non-citable string; inconsistent capitalisation in a heading; minor formatting variation |
| **FYI** | Informational observation, no action required. | A page that's well-written but could be cross-linked from one more entry point; a candidate for a future mechanical gate |

The `[critical]` flag is a tag inside the High tier, not a fifth tier. It marks findings whose downstream impact is qualitatively different (audit failure / regulatory exposure / control failure) from ordinary High findings.

## Cadence

Fitness reviews are manually triggered. Suggested triggers:

- **After major changes**: new domain directory, new document type, ≥3 governance rule additions, major corpus restructure.
- **Quarterly minimum**: default trigger if no major change fired one in the prior 90 days.
- **Pre-publication / pre-external-share**: before the library is shared with a wider audience or used as the basis for a real GRC programme.
- **On demand**: maintainer judgement.

The fitness review is heavyweight (10 personas dispatched in parallel; whole-corpus scope; ~30-60 minutes wall-clock for a 200+ document corpus). It is not a per-PR gate. The per-PR regression check is the `validation-sweep` skill (`/validate`), which is lightweight and runs after every substantive PR.

## Output flow per run

1. **Maintainer invokes `/fitness`** (or the skill is triggered by another agent).
2. **Orchestrator establishes mechanical baseline**: runs `tools/run_all_audits.sh` standalone to confirm starting state.
3. **Orchestrator dispatches 10 persona subagents in parallel.** Each gets the same corpus access, the same review brief, and a persona-specific lens. No subagent inherits the orchestrator's mental model.
4. **Subagents review every page from their persona's perspective** and return findings as structured blocks: page title, path, persona inference of purpose and audience, actual clarity, key issues with severity, impact, recommendation, retention decision.
5. **Orchestrator synthesises** into the 8-section combined report. Dedupe across personas; adjudicate severity (pick higher); group by recommendation priority; assemble remediation backlog with discrete IDs.
6. **Orchestrator surfaces issues, recommendations, and choices in chat** for maintainer prioritisation. This is the actionable layer.
7. **If findings exist**: write the combined report to `.working/fitness-reviews/YYYY-MM-DD-rN.md`; append a row to `history.md`.
8. **If zero findings**: append only the row to `history.md` with summary "library passes fitness review".
9. **Remediation work**: discrete remediation backlog IDs (`FR-1`, `FR-2`, ...) become the seed for follow-up PRs. The maintainer prioritises, then drives each through the normal PR cadence.

## Relationship to `validation-sweep` (`/validate`)

| Aspect | `/validate` (validation-sweep) | `/fitness` (library-fitness-review) |
|---|---|---|
| Cadence | Every PR + after every substantive change | After major changes + quarterly minimum + on demand |
| Scope | Recent PRs + corpus-wide stale-reference + audit-programme integrity | Whole corpus, every page |
| Subagents | 3 (A: recent-PR deep review; B: stale-reference; C: audit-programme integrity) | 10 (multiple personas) |
| Output | Per-iteration record (`.working/validate-sweeps/`) when findings; row in history always | Per-run report (`.working/fitness-reviews/`) when findings; row in history always |
| Cost | Lightweight (~5-10 minutes) | Heavyweight (~30-60 minutes) |
| Purpose | Catch what changed; regression check | Evaluate what's there; quality review |

The two are complementary. `/validate` answers "did my recent change break anything?". `/fitness` answers "is the library in good shape for adoption / publication / audit / executive consumption?". Both can coexist; neither replaces the other.

## Audit-gate exemption

The `.working/` directory tree is in `tools/lint_common.py` `DEFAULT_EXEMPT_DIRS`. Files here are exempt from corpus audit gates: broken-link drift, language-style drift, citation staleness, orphan status are expected and do not fail CI.

## Adopter guidance

If you fork this library:
- **The convention** (this README, the SKILL.md, the slash command) is template content. Adopt it directly. Adjust persona definitions if your library's domain has different perspectives than ours.
- **The contents of `history.md` and any per-run files** are upstream maintainer's working state. You may keep them as historical reference of the upstream library's quality trajectory, or delete and start fresh from your first `/fitness` invocation. Either is fine.

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 |
| --- | --- | --- | --- |
| Periodic library-quality review | PS.3, RV.1 | GRC-04, GRC-05 | A.5.36, A.5.37 |
| Multi-perspective assessment | RV.1, RV.3 | GRC-05, A&A-04 | A.5.36, A.8.34 |
| Audit-trail of review activity | PS.1, RV.2 | LOG-02, LOG-08 | A.8.15 |
| Remediation backlog tracking | PO.5, RV.2 | CCC-03 | A.5.4, A.8.32 |
