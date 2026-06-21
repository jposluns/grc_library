# TODO

Living backlog of planned enhancements for the GRC Documentation Library. Items are added when identified and removed when completed. Completed work is recorded in [`CHANGELOG.md`](CHANGELOG.md); this file holds only pending and queued items.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions. The other repository-root meta files that share this exemption are [`CHANGELOG.md`](CHANGELOG.md) (a chronological log that mutates with every PR) and [`instruction-ai-document-ingestion.md`](instruction-ai-document-ingestion.md) (an AI system prompt, not a governance document). As of `2026-06-02`, [`README.md`](README.md), [`NOTICE.md`](NOTICE.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SECURITY.md`](SECURITY.md), [`AUTHORS.md`](AUTHORS.md), and [`docs/worked-example.md`](docs/worked-example.md) each carry the canonical 13-field metadata block and are validated by the corpus metadata audit (gate 1).

---

## Active session work (resume here next session) — 2026-06-21

This section preserves the in-flight context for a multi-PR sequence the maintainer is working through. Each subsection is a checkpoint so the next session can pick up without re-deriving the design decisions. Remove when the sequence completes.

### Session state at pause

- **Current branch**: `main` (synced after PR #120 merge).
- **Library version at HEAD**: `2026.06.105`. **Pack version**: `1.30.0`. **README version**: `1.8.61`.
- **Audit programme**: 44 gates, all passing on `main`.
- **Last validation sweep**: Sweep 10 iteration 2 (in flight at session-pause time; close-out PR #121 covers this). Re-baseline due after the changelog-details migration if and when the maintainer reorders the queue, and after any further `.working/` moves.

### PRs completed in this session

In merge order (oldest to newest); see [`CHANGELOG.md`](CHANGELOG.md) for full details of each.

1. **PR #110** — corpus stale gate-count fixes + gate 39 pattern P6
2. **PR #111** — Sweep 9 closure: Subagent C findings + Rule 5.6 (subagent-dispatch declaration discipline)
3. **PR #112** — 7th governance rule (`validate-inference-before-action.md`) + gate 39 pattern P7
4. **PR #113** — Sweep 9 iter 3 close-out (3 prose drift findings in PR #112)
5. **PR #114** — `.working/` infrastructure (top-level README + `DEFAULT_EXEMPT_DIRS` extension)
6. **PR #115** — `/validate` slash command rename (was `/validation-sweep`) + per-iteration record convention
7. **PR #116** — Move sweep history file from `governance/` to `.working/`
8. **PR #117** — Sweep 10 iter 1 close-out (6 prose drift findings post-#114-#116)
9. **PR #118** — Restructure `.working/<activity>/` to canonical layout (README + history table + per-run detail only-when-findings)
10. **PR #119** — TODO update only (session-resume context capture); `Changelog: skip` per TODO's informational status
11. **PR #120** — `/fitness` skill (`library-fitness-review`); ten persona reviewers; canonical `.working/fitness-reviews/` activity layout; pack `1.29.0 → 1.30.0`. Authored overnight under explicit maintainer authorisation; full decision log at `.working/overnight-pr.md`
12. **PR #121** (queued, this is Sweep 10 iter 2's close-out) — Re-add preflight exemption for "Six rules" line; update TODO resume-state snapshot; fix small CHANGELOG narration claim; update overnight-pr.md status

### Queued sequence (resume in this order)

**Step A — Validation sweep against post-PR-#118 state.** First sweep under the new canonical layout. Should be cheap (the restructure was internal; corpus content unchanged). Confirms the new `Subagents` column in `history.md`, the "only if findings" convention for per-iteration detail files, and the linter target path update for gate 43 all work end-to-end.

**Step B — PR #119: Changelog details migration.** Splits the root [`CHANGELOG.md`](CHANGELOG.md) into:
- Root file keeps **only the lead paragraph** of each existing entry (and going forward).
- Copy of pre-trim full file lands at `.working/changelog-details/CHANGELOG-detailed.md` (or follow PR #118's canonical activity layout: `.working/changelog-details/README.md` + `.working/changelog-details/history.md` — TBD; need to think about whether changelog details fit the same layout pattern or if they're a single growing file).
- Header note added to root: *"Detailed maintainer-level changelog entries may be kept in a working directory."* No name, no link.
- Adopters cloning the library keep the lead paragraphs (template demonstrates the convention).
- Extend [`tools/check-changelog-on-pr.py`](tools/check-changelog-on-pr.py) (the PR-time delta gate) to also require modifications to the detailed-changelog file when root CHANGELOG is modified. Keep the gate PR-only (it runs only on `pull_request` events per `quality.yml`), so the `.working/` general audit-exemption is preserved for everything else.
- Amend [`dev-security/claude-rules/governance/change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md): the structured sections (Added/Changed/Removed/Fixed/Security) and verification evidence requirement applies to the **detailed** file; the root keeps only the lead paragraph (public-facing summary).
- Mirror the rule update to `.claude/rules/governance/change-tracking.md` via the claude-rules sync linter (gate 37 will catch any divergence).

**Step C — Validation sweep against post-PR-#119 state.** Verifies the changelog split didn't break the change-tracking discipline anywhere.

**Step D — PR #120: `/fitness` skill (library-fitness-review).** New skill that runs a comprehensive 7-persona corpus-wide review (heavyweight; manual trigger; not per-PR). Per the design discussion:
- **Skill name**: `library-fitness-review` (descriptive name in the pack)
- **Slash command**: `/fitness` (short ergonomic verb)
- **Skill file**: `dev-security/claude-rules/skills/library-fitness-review/SKILL.md`, derives from `dev-security/claude-rules/governance/evidence-grounded-completion.md`
- **Slash command file**: `.claude/commands/fitness.md`
- **Output directory**: `.working/fitness-reviews/` (follows PR #118's canonical activity layout: README + history table + per-run detail only-when-findings)
- **10 personas (parallel subagents)** as shipped in PR #120 (the original prompt specified 7; the implementation expanded to 10 with three additions justified in [`.working/overnight-pr.md`](.working/overnight-pr.md)): (1) first-time executive reader; (2) security practitioner; (3) GRC practitioner; (4) auditor/assurance reviewer; (5) policy and standards editor; (6) process owner / operational user; (7) skeptical reader; (8) adoption practitioner; (9) privacy/data protection officer; (10) newcomer/onboarding engineer. All 10 dispatched on every full run.
- **Scope per run**: whole corpus, every run.
- **Cadence**: manual trigger (after "major changes" — new domain dir, new document type, pack rule additions, major restructure; quarterly minimum if no major changes; pre-publication / pre-external-share).
- **Output format per run**: one combined Markdown file at `.working/fitness-reviews/YYYY-MM-DD-rN.md` with 8 top-level H2 sections following the prompt's structure (Executive Summary, Review Method, Page-by-Page Findings, Cross-Library Findings, Severity Model, Recommendations, Standardization Recommendations, Remediation Backlog, Final Assessment). Discrete remediation IDs (`FR-1`, `FR-2`, …) drive subsequent PRs.
- **Output to chat**: issues + recommendations + choices surfaced for maintainer action; the committed file is the persistent archive.
- **Severity**: keep project's existing SARIF-lite (High/Medium/Low/FYI); treat the prompt's "Critical" as a `[critical]` flag inside High (`[high][critical] file:line — description`). Two severity scales not introduced.
- **No mechanical gate**: the fitness review is a deliverable, not a per-PR gate. Output informs human prioritisation.
- **Pack version bumps to 1.30.0** (new skill = pack minor bump per `skill-authoring-discipline`).
- **Touchpoints per skill-authoring-discipline**: pack README directory tree + "When to use each skill" table + version-history row; `.working/README.md` activity table; `tools/lint-collection-enumeration-consistency.py` if it enumerates skills.

**Step E — Validation sweep against post-PR-#120 state.** Re-baseline after the new skill ships.

### Other queued moves (after Step E; small PRs preferred per maintainer)

Files identified earlier as project-specific application that should move from `governance/` or `tools/` to `.working/`. Each as its own small PR:

- **`tools/sweep-preflight-exemptions.json`** → likely `.working/validate-sweeps/preflight-exemptions.json` (co-located with the validate-sweeps activity since that's what the file is for). Maintainer-curated false-positive memory for OUR project's specific false positives; adopters will curate their own.
- **Citation-verification cluster** (6 files): `register-citation-verifications.md` + `register-citation-verification-bundle.md` + four `worklist-citation-verification-batch-*.md` files. → `.working/citation-verifications/` following the canonical layout. Project-specific in-flight verification campaign for OUR citations (Phase 23.6 work).
- **`governance/register-main-branch-protection.md`** → `.working/` somewhere. Snapshot of THIS repo's branch protection; meaningless to adopters who configure their own.

Each requires updating the document-index, sibling references, regenerating taxonomy/portal, version bumps, CHANGELOG entry.

### Key design decisions made this session (for context if details fade)

1. **`.working/` convention**: maintainer working state; not corpus content; not for adopter consumption; exempt from corpus audit gates (in `DEFAULT_EXEMPT_DIRS`); frozen-state archive (cross-references accurate as-of write-time; staleness expected). Top-level dot-prefix matches the existing tooling-dir convention (`.git/`, `.github/`, `.claude/`).

2. **Canonical activity layout under `.working/<activity>/`**:
   - `README.md` — static convention info (what the activity is, file format spec, taxonomies, protocols, framework alignment, fork guidance)
   - `history.md` — reverse-chronological table (new rows on top); columns: Date | Sweep/Run | Subagents | Findings | Resulting PR | Detail | Summary
   - `YYYY-MM-DD-<run-id>.md` — per-run detail file, **only created when findings exist**
   - `Subagents` column declares dispatch (Rule 5.6) for every row including zero-finding runs

3. **Slash commands vs skill names are independent identifiers**: short ergonomic verbs for commands (`/validate`, `/fitness`), descriptive names for skills (`validation-sweep`, `library-fitness-review`). The slash command file wraps the skill invocation.

4. **Template content vs project-application**: `governance/` holds template content (specifications, frameworks, registers as document-type templates that adopters cite); `.working/` holds project-specific application of those templates (our log of our sweeps, our verification campaign progress, our branch protection snapshot).

5. **Fork-time guidance**: adopters cloning the library may delete `.working/` outright or keep it as historical reference. Both fine.

6. **PR sequencing principle**: "More PRs, keep each one clean." Favor small focused PRs over bundled ones. Validation sweeps run between substantive PRs.

7. **CHANGELOG split convention (PR #119)**: root keeps the lead paragraph; structured sections + verification evidence + discipline observations move to `.working/changelog-details/`. Going forward, every change writes BOTH. PR-time gate (`check-changelog-on-pr.py`) enforces dual-entry. The general `.working/` audit exemption is preserved for everything else.

8. **Fitness review convention (shipped in PR #120)**: 10 personas parallel (original prompt's 7 + adoption practitioner + privacy/DPO + newcomer), whole-corpus each run, output to `.working/fitness-reviews/YYYY-MM-DD-rN.md` only when findings, 8-section combined file. Severity: SARIF-lite + `[critical]` flag in High. Manual trigger only; no mechanical gate enforces it.

9. **Subagent dispatch (Rule 5.6) audit trail**: every validation-sweep iteration declares which subagents were dispatched in the `Subagents` column of `history.md`. Cannot reconstruct silent skips later.

10. **Convergence-delta termination** (validation-sweep): empty-delta primary stop / patience-plateau secondary (2 consecutive iterations no shrinkage) / hard-ceiling 6 iterations.

11. **Per-iteration detail files: comma form for H2 headings** (gate-2 enforces no em-dashes; comma is the canonical form across SKILL.md, slash command, and `.working/validate-sweeps/README.md`).

### Critical user feedback to remember across sessions

- **"More PRs, keep each one clean"** — favor small focused PRs.
- **"I prefer /validate, not /validation-sweep"** — short slash commands; skill names stay descriptive.
- **"Don't explicitly name or link `.working/`"** in template-content files that adopters see (e.g., root CHANGELOG header note for the changelog split).
- **"Inference must be validated before committing or before anything else uses that information"** — addressed by 7th pack rule [`governance/validate-inference-before-action.md`](dev-security/claude-rules/governance/validate-inference-before-action.md) (PR #112).
- **Activity directories should be self-contained** — drove PR #118's restructure (history file in subdir alongside README + per-iteration files).
- **Zero-finding sweeps still need history rows but no detail files** — drove the "only if findings" rule in SKILL.md step 9.
- **Sweep history is project-application not template content** — drove PR #116 move from `governance/` to `.working/`.

### Open follow-ups from validation sweeps (deferred items not yet closed)

Both pre-date the dating-discipline convention (2026-06-20) so neither has a `surfaced` / `re-triage-by` stamp. From [`.working/validate-sweeps/history.md`](.working/validate-sweeps/history.md):

- **Sweep 3 follow-up**: cross-document term-and-identifier consistency gap. The prose-and-numbering-shaped C3 surface that mechanical gates 35/39/41 don't cover. Candidate for a future mechanical gate.
- **Sweep 4 follow-up**: classification-convention documentation. Resolved within the Sweep 4 close-out (the failure-mode-classes table in `.working/validate-sweeps/README.md` now documents the primary-plus-secondary classification convention).

---

## Priority 4 — adopter experience

### 4.1 Quickstart templates per adopter profile

Shipped 2026-06-20 as [`docs/template-quickstart.md`](docs/template-quickstart.md) (v2.0.0). Core baseline plus five stacking dimensions (Activity, Data scope, Audience, Regulatory exposure, GRC capacity) with about twenty modules; three worked examples. The original v1.0.0 fixed-profile structure (PR #103) was rejected by the maintainer as too rigid; the rewrite (PR #105) adopts an activity-modular composition shape that lets adopters combine modules à la carte.

### 4.2 Maturity assessment interactive template

Shipped 2026-06-20 as [`docs/template-maturity-self-assessment.md`](docs/template-maturity-self-assessment.md). Guided markdown checklist covering 11 library domains across a 5-tier maturity ladder (Initial / Developing / Defined / Managed / Optimising); per-tier next-step guidance; recording template.

### 4.3 Implementation roadmap templates

Shipped 2026-06-20 as [`docs/template-implementation-roadmap.md`](docs/template-implementation-roadmap.md). Three-phase (Floor / Operational / Year-1 close) sequence at 90 / 180 / 365 days for the reference E2 pace, with pace adjustments for E1, E3, E4 capacity tiers and for composition complexity. Designed to sequence the modules picked via the quickstart template; not per-profile.

### 4.4 Regulator interaction templates

Shipped 2026-06-20 as [`compliance/template-regulator-interaction.md`](compliance/template-regulator-interaction.md). Five sub-templates in one consolidated document: breach notification, attestation submission, examination support, periodic report submission, regulatory inquiry response. Shape-only; jurisdiction- and sector-specific timing/format requirements live in the relevant annex or sector folder.

### 4.5 Audit evidence package templates

Shipped 2026-06-20 as [`compliance/template-audit-evidence-package.md`](compliance/template-audit-evidence-package.md). Cover page, control inventory index, per-control sections (framework references, implementation and operating evidence, gaps and compensating controls, per-control sign-off), optional per-domain summaries for 50+ control packages, optional cross-reference index for shared evidence, package-level sign-off. Anti-patterns to watch and eight review questions.

---

## Priority 5 — content expansion

### 5.1 Logistics country/programme expansion

The WCO AEO Compendium identifies 77+17 ≈ 94 trusted-trader programmes globally; the library currently covers 4 (BASC, CTPAT-US, AEO-UK, PIP-Canada). Highest-priority additions:
- EU AEO (covers 27 member states under EU Union Customs Code Art 38)
- Mexico NEEC / OEA
- Australia Trusted Trader (ATT)
- Singapore STP / STP-Plus
- Japan AEO
- Korea AEO
- New Zealand Secure Exports Scheme (SES)
- China AEO

### 5.2 Financial-services country regulator overlays

Country-level financial-regulator annexes within `compliance/financial-services/`:
- UK PRA/FCA (`annex-uk-pra-fca.md`)
- US OCC/FRB/FDIC/SEC/FINRA
- Canada OSFI
- Australia APRA
- Singapore MAS
- Japan FSA

### 5.3 Healthcare country regulator overlays

Within `compliance/healthcare/`:
- US HIPAA detail (Privacy Rule, Security Rule, Breach Notification Rule, HITECH)
- UK NHS DSPT (Data Security and Protection Toolkit)
- EU MDR/IVDR (Medical Device Regulation; In-Vitro Diagnostic Regulation)
- Canada PHIPA and provincial frameworks
- Australia My Health Records Act

### 5.4 Energy and utilities country regulator overlays

Within `compliance/energy-and-utilities/`:
- US NERC CIP standards (electricity reliability)
- US TSA pipeline cybersecurity directives
- UK Ofgem cyber requirements
- EU ENISA sectoral guidance

### 5.5 Telecommunications country regulator overlays

Within `compliance/telecommunications/`:
- EU EECC (European Electronic Communications Code)
- UK Ofcom telecom security framework
- US FCC regulations
- Australia ACMA requirements

### 5.6 Public-sector country/regulator overlays

Within `compliance/public-sector/`:
- UK Government Cyber Security Strategy and GovAssure
- Australia ISM (Information Security Manual) and PSPF (Protective Security Policy Framework)
- Canada IT Standards for federal departments
- EU eIDAS public-sector authentication

### 5.7 Privacy jurisdiction gaps

Existing privacy domain covers 25 country annexes. Known gaps or stale entries:
- Argentina (PDPA 2025 update pending; currently covered in the Latin America annex)
- Saudi Arabia PDPL (dedicated annex exists; recent updates pending)
- Mexico LFPDPPP (currently covered in the Latin America annex; standalone annex possible)
- Re-review of EU member state derogations where applicable

### 5.8 AI jurisdiction overlays

The library cites EU AI Act extensively but lacks a dedicated `ai/jurisdictions/` subdirectory parallel to `privacy/jurisdictions/`. Candidates:
- EU AI Act detailed annex (`ai/jurisdictions/annex-ai-european-union.md`)
- Canada AIDA
- UK AI policy framework
- US state-by-state AI laws (Colorado AI Act, NYC bias audit law, etc.; partial coverage exists today inside the US privacy annex but a dedicated AI-jurisdiction annex would be cleaner)
- China generative AI rules (partial coverage exists today inside the China privacy annex)
- Korea AI framework

---

## Priority 6 — domain-level expansion (longer-term)

### 6.1 Multi-cloud governance overlay

Per-cloud hardening baselines for AWS, Azure, and GCP exist in `dev-security/`. The remaining gap is multi-cloud governance (cross-cloud risk taxonomy, cross-cloud incident coordination, cloud-portfolio-level controls). Could live in `operations/` or warrant a new `cloud/` domain.

### 6.2 Identity-specific content depth

Customer Identity (CIAM) governance, workforce identity governance, identity federation patterns, passwordless adoption playbooks. The library has an Identity and Access Management policy and procedure but no dedicated content for these patterns.

### 6.3 Quantum cryptography readiness deepening

The library has a PQC roadmap at phase level ([`security/roadmap-post-quantum-cryptography.md`](security/roadmap-post-quantum-cryptography.md)). The roadmap covers discovery, standards, pilot, and migration phases but not detailed implementation content. Pending additions: PQC migration playbook (operational steps per system class), crypto-agility patterns (key abstraction, algorithm switching, hybrid schemes), and post-quantum-ready CA / PKI management.

### 6.4 Cross-framework matrix expansion

Current matrix ([`governance/matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md)) covers major frameworks; could expand coverage to additional sectoral and regional frameworks as the country/sector content under Priority 5 grows.

---

## Investigation / blocked

Items requiring user decision or external dependency before becoming actionable.

- *(none currently)*

---

## Decisions log

Items considered and explicitly dropped, with rationale. Recorded here so the reasoning is preserved if the question recurs.

### Strict Related-Documents reciprocity dropped

Original plan: add a linter enforcing that if document A's Related Documents lists B, then B's Related Documents lists A. Empirical run found 1,269 non-reciprocal references across 266 of 280 active documents.

The library's actual convention is **asymmetric** Related Documents: each document lists "what this document consumes / relates to from its own perspective", not "the complete bidirectional graph". This is a reasonable, content-author-friendly convention.

The underlying concern (catching half-updated cross-references during refactors) is already covered by [`lint-links.py`](tools/lint-links.py) (broken-link detection).

Decision: dropped. Not pursued in narrower form (doctype-pair rules) because the marginal value over [`lint-links.py`](tools/lint-links.py) does not justify the maintenance cost of a curated rule set with many exemptions.

### Cross-document numerical coherence shipped as scaffold

Original plan in the audit-roadmap: a linter that flags numerical drift on canonical-term thresholds (RTO, RPO, P1/P2/P3/P4 acknowledgement times, retention periods) across documents.

Empirical analysis found that incident-severity terminology (P1/P2/P3/P4) legitimately carries different numeric values per SLA dimension: acknowledgement time, resolution time, escalation interval, notification time. A naive "same Pn = same value" check would false-positive on legitimate per-dimension variation.

Decision: ship as scaffold (regex framework with unit normalisation and aggregation), with the term set widened incrementally as empirical data warranted. The scaffold's progression:

- Phase 23.26 added P1/P2/P3 acknowledgement-time patterns as scaffolding (each requires a Pn-prefix-with-explicit-acknowledgement-time prose shape on the same line; the patterns match 0 documents on the current corpus by design, since the corpus carries Pn-acknowledgement times in tabular form rather than the strict prose shape).
- Phase 23.35 added the GDPR breach-notification-hours pattern after empirical confirmation that 8 or more documents reference the statutory 72-hour deadline and all agree on the value.

The current scaffold tracks four terms (P1/P2/P3 acknowledgement-time patterns plus GDPR-breach-notification-hours); see `TERM_PATTERNS` in [`tools/lint-cross-doc-numbers.py`](tools/lint-cross-doc-numbers.py) for the live set. The linter's docstring documents why RTO, RPO, retention periods, P4 acknowledgement, NIS 2 reporting windows, and DORA reporting windows are deliberately NOT curated (each is either context-dependent, has multiple legitimate per-deadline sub-patterns that need separate regex, or appears too few times in the corpus to justify a curated pattern).

Honest scope management is preferred over either (a) silently producing false positives or (b) defining the term set without sufficient operational data. The maintainer revisits the term set when corpus evolution introduces a new prose shape that warrants pattern coverage.

### Phase-completion gating requires the full audit-programme sweep

A prior bundled commit's pre-merge audit pass omitted several gates and consequently merged 5 audit-gate violations (filename/doctype prefix mismatch on the bundle index, 15 em-dash language findings, one broken intra-repo link, one mislabelled hallucinated framework version, one unresolved intra-document reference). All were caught and corrected in the immediately following cleanup.

Decision: phase-completion gating requires the full audit-programme sweep ([`tools/run_all_audits.sh`](tools/run_all_audits.sh); see [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) §6 for the canonical inventory) to pass locally before any push. The pre-commit hook configuration operationalises this in git itself.

The convention is: at each commit, the maintainer (or AI verifier) runs every gate in a single batch (not a selective subset) and only proceeds to push when zero violations remain.

### No verification of standard content versus library interpretation

When the AI Security Tooling Landscape Register was created, it asserted capability claims for each project. The Citation Verification Specification §14 explicitly excludes "verification of standard content versus the library's interpretation of it" from the methodology scope.

Decision: verification covers metadata (existence, version, publication date, supersedence, ID format) and integrity anchors (commit SHA, Wayback snapshot URL). It does NOT verify that the library's prose interpretation of a project's capabilities is accurate. That would require the library to engage in interpretation disputes with project authors; the methodology stays at the citation-metadata layer.

---

## Notes on maintenance

- Add new items at the appropriate priority. Move items between priorities as context changes.
- When an item is completed, remove it from this file and record the completion in [`CHANGELOG.md`](CHANGELOG.md).
- Sub-items can be promoted to their own priority section if scope grows.
- This file is the source of truth for what's queued; conversation history is not.
