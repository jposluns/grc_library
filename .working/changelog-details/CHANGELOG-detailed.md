# Changelog (Detailed Mirror)

All notable changes to this repository are recorded in this file with full structured-section detail. The adopter-facing root [`CHANGELOG.md`](../../CHANGELOG.md) carries only the lead-paragraph summary of each entry; this file is the maintainer-grade audit trail.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](../../specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](../../specification-master-project.md) section 4.5.

The dual-entry convention was introduced in PR #125 (2026-06-21). Historical entries before that date follow the original single-file convention (the root entry was complete; this mirror preserves that pre-split state verbatim from the moment of the split).

## 2026-06-21, Library Version 2026.06.148, PR #166

Closes FR-57 (high). The "quickstart" at `docs/template-quickstart.md` was 319 lines covering 5 dimensions × 23 modules — a composition workbook, not a quickstart. A real quickstart is a 10-minute on-ramp; the existing content's value is preserved by renaming, and a new short quickstart ships at the original path.

### Closed findings

- **FR-57** (high, `docs/template-quickstart.md` length): file size and module-catalogue depth violated the quickstart contract (10-minute on-ramp); the file functioned as a multi-hour composition workbook. Reconciled via Option B (rename + new short doc) over Option A (rewrite in place) to preserve the workbook's value for adopters who need the deeper composition.

### Renamed

- [`docs/template-quickstart.md`](../../docs/template-quickstart.md) → [`docs/template-startup-roadmap.md`](../../docs/template-startup-roadmap.md) (git mv): content preserved verbatim except metadata (Document Title, Repository Path, Version, Date) and a Purpose preface that names the relationship to the new short quickstart. Per-doc version `2.0.2 → 2.1.0` (minor: title rename + preface tightening; content sections preserved).

### Added

- [`docs/template-quickstart.md`](../../docs/template-quickstart.md) (new, version 3.0.0): a true 10-minute on-ramp. Three steps (copy the six-artefact core baseline; substitute role names; point at the portal). "Next steps" block linking to the renamed startup-roadmap (full composition workbook) and the other three adopter-facing paths (adopter-guide, decision-tree, implementation-roadmap). Body ~50 lines including the core-baseline enumeration.
  - Version starts at `3.0.0` because the file at the path `docs/template-quickstart.md` is materially redefined (different audience, different content shape); a major bump is honest. The prior v2.0.x content sequence continues at the renamed path.
  - Quickstart's "Where this fits among the adopter entry points" preface follows the FR-56 pattern; identifies the quickstart as the Day-1 entry, points at startup-roadmap for the deeper workbook.

### Changed (cross-references)

- [`docs/template-implementation-roadmap.md`](../../docs/template-implementation-roadmap.md):
  - Related Documents: added `template-startup-roadmap.md` (existing template-quickstart link remains, pointing at the new short doc).
  - §Purpose body line 21: "modules selected via [`docs/template-quickstart.md`]" → "modules selected via [`docs/template-startup-roadmap.md`]" — the roadmap follows the composition workbook, not the new short quickstart.
  - §"How to use" step 1: "Complete the quickstart composition first... Run through [`docs/template-quickstart.md`]" → "Complete the startup-roadmap composition first... Run through [`docs/template-startup-roadmap.md`]".
  - Per-doc version `1.0.2 → 1.0.3`.
- [`docs/template-maturity-self-assessment.md`](../../docs/template-maturity-self-assessment.md):
  - Related Documents: added `template-startup-roadmap.md` (existing template-quickstart link remains).
  - Per-doc version `1.0.1 → 1.0.2`.
- [`tools/build-portal.py`](../../tools/build-portal.py):
  - `PORTAL_METADATA_VERSION` bumped `1.1.0 → 1.2.0` (generator schema; emits a new portal table row).
  - The Day-1 row split into two: quickstart now answers "What do I copy on Day 1?" with the new short content description; startup-roadmap row answers "And what do I add later?" with the long-form composition description. Adopters can pick the right depth from the table without reading both documents.
- [`docs/portal.md`](../../docs/portal.md): regenerated (read-only artefact).
- [`README.md`](../../README.md): library `2026.06.147 → 2026.06.148`; README per-doc `1.9.18 → 1.9.19`. README line 27 "Adopter setting up a programme: start with adopter-guide and template-quickstart" is unchanged — the new short quickstart at the same path is exactly what a "setting up a programme" reader wants.
- [`TODO.md`](../../TODO.md): FR-57 rotated out of High tier; backlog counters updated (10 + 5 + 56 = 71 immediate; 14 deferred; 85 open). New "Backlog-listing process: effort-sizing labels" section added per maintainer direction — captures the XS/S/M/L/XL effort-label convention as a post-FR-backlog meta-improvement that will retrofit the fitness-review and validation-sweep skill files plus future TODO entries.
- [`.working/DONE.md`](../DONE.md): PR #166 entry added.

### Not changed (intentional)

- `README.md` line 27 cross-reference to `template-quickstart.md`: still points at the same path, which now hosts the new short doc; the reader's intent is still served (now better, because the new short doc is actually a quickstart).
- `docs/decision-tree.md` and `docs/adopter-guide.md` preface descriptions of template-quickstart ("what to copy on Day 1"): still accurate for the new short doc; no edit needed.
- `governance/register-document-index-and-classification.md`: does not index `docs/` files, so the rename produces no index drift.

### Verification

- `tools/run_all_audits.sh` exits 0 on all 46 gates post-commit.
- `tools/run-pr-time-checks.sh` exits 0 (D1 + D2 + gate 45).
- Generated artefact: `tools/build-portal.py` ran clean; the regenerated `docs/portal.md` now shows two rows in the entry-points table (quickstart and startup-roadmap) instead of one.
- Cross-reference validation: grep for `template-quickstart` in corpus shows only the legitimate forward-references (new short doc + Related Documents pointers); grep for `template-startup-roadmap` shows the new pointers from implementation-roadmap, maturity-self-assessment, portal, and the new quickstart's "Next steps" block. No dangling links.

### Discipline observation

This is the first file-rename PR in the fitness backlog. The git mv preserves blame history; the new short doc is a write-new operation. The version sequence at the path uses a major bump (`2.0.2 → 3.0.0`) because the file at that path is materially redefined for a different audience — adopters who land on the new short doc get a different experience than adopters who landed on the prior long doc. The prior v2.x content continues at the renamed path with a minor bump (`2.0.2 → 2.1.0`) because its shape and audience are unchanged.

The decision to split the portal's Day-1 row into two rows (quickstart + startup-roadmap) is a small but useful adopter-UX win: a reader who wanted the modules-workbook had to first land on the quickstart to discover it existed, even though the workbook content was what they actually wanted. Two rows surfaces both options directly.

The maintainer also surfaced an effort-sizing-labels meta-improvement: future backlog items should carry an XS/S/M/L/XL effort tag alongside their severity tag so prioritisation has both dimensions visible. Captured in TODO under a new "Backlog-listing process" section; will be implemented after the current FR backlog is closed (the convention applies to future fitness reviews and sweep findings, not retroactively to the in-flight backlog).

---

## 2026-06-21, Library Version 2026.06.147, PR #165

Closes FR-56 (high, adopter entry-point reconciliation). The corpus had six distinct entry-point sequences (README → portal; adopter guide → Tier 1/2/3; quickstart → core baseline + modules; decision tree → 30/90/180 sequenced reading; implementation roadmap → Phase 1/2/3 calendar; fitness-review path for maintainers). Five of those are adopter-facing and there was no document explaining how they relate; the sixth is maintainer-facing and should not surface to adopters. Adopters landing on any of the five could not pick the right path for their question without reading all five.

### Closed findings

- **FR-56** (high, multiple documents in `docs/`): Six distinct entry-point sequences created without an explicit relationship statement. PR #156 (FR-2) and PR #147 (FR-3 "New to GRC?") had implicitly elected `docs/portal.md` as the primary navigation surface; this PR makes that election explicit and reconciles the four remaining adopter-facing paths as deeper-dive branches that answer specific questions, each branching from the portal.

### Reconciliation chosen

**Option A** (least-invasive): declare `docs/portal.md` the canonical front door and document the other sequences as audience-specific paths that branch off it. Considered alternatives Option B (collapse some sequences) — rejected as too invasive (each of the five adopter-facing sequences has a genuinely distinct purpose) — and Option C (add a new "Choose your path" document) — rejected as adding a seventh entry-point document, increasing rather than reducing fragmentation.

### Changed

- [`tools/build-portal.py`](../../tools/build-portal.py):
  - `PORTAL_METADATA_VERSION` bumped `1.0.0 → 1.1.0` (generator schema constant; minor — emits a new portal section).
  - Overview prose extended with one sentence naming the portal as the canonical front door and pointing at the new "Other entry points" section.
  - New "Other entry points and when to use them" section emitted immediately after Overview. Contains a 5-row table that picks the entry point by question (role / adopt principles / Day 1 copy / reading order / calendar phasing). Each row points at the corresponding adopter-facing document with a one-line "what it gives you" description.
- [`docs/portal.md`](../../docs/portal.md): regenerated from the updated generator (lines 24-49 are the new prose + section). Read-only generated artefact per the generator-output discipline; not hand-edited.
- [`docs/adopter-guide.md`](../../docs/adopter-guide.md):
  - New "Where this fits among the adopter entry points" preface added under §Overview. Names the portal as canonical and identifies this guide as the "fork-and-adapt principles" deeper-dive path. Cross-references the other three adopter-facing paths.
  - Per-doc version `1.1.1 → 1.1.2`.
- [`docs/template-quickstart.md`](../../docs/template-quickstart.md): same preface pattern; identifies this template as the "what to copy on Day 1" path. Per-doc `2.0.1 → 2.0.2`.
- [`docs/decision-tree.md`](../../docs/decision-tree.md): same preface pattern; identifies this guide as the "sequenced reading order" path. Per-doc `1.0.0 → 1.0.1`.
- [`docs/template-implementation-roadmap.md`](../../docs/template-implementation-roadmap.md): same preface pattern; identifies this template as the "calendar phasing" path. Per-doc `1.0.1 → 1.0.2`.
- [`README.md`](../../README.md): library `2026.06.146 → 2026.06.147`; README per-doc `1.9.17 → 1.9.18`.
- [`TODO.md`](../../TODO.md): FR-56 rotated out of High tier; backlog counters updated (10 + 6 + 56 = 72 immediate; 14 deferred; 86 open). New "BYOD policy: add MDM vs MAM option" section added per maintainer-direction follow-up.
- [`.working/DONE.md`](../DONE.md): PR #165 entry added.

### Out of scope (intentional)

- **FR-57** (`docs/template-quickstart.md` is 319 lines — not a real quickstart): separate finding tracked in the High tier. The portal block cross-references the quickstart by its current shape; FR-57 will rewrite the quickstart in a separate PR.
- **Renaming `template-quickstart.md` to `framework-adoption-composition.md`**: FR-57 territory.
- **Maintainer-facing fitness-review path**: documented in `.working/fitness-reviews/README.md` as maintainer working state. Not surfaced in the adopter-facing portal block because it is not an adopter entry point.

### Verification

- `tools/run_all_audits.sh` exits 0 on all 46 gates post-commit.
- `tools/run-pr-time-checks.sh` exits 0 (D1 + D2 + gate 45).
- Generated artefact: `python3 tools/build-portal.py` ran clean; the regenerated `docs/portal.md` carries the new "Other entry points" section at lines 30-49 (verified visually).
- Cross-reference validation: each of the four adopter-facing documents now contains an explicit `[`docs/portal.md`](portal.md)` link; each names the other three documents and their respective questions; the portal's table-row links target all four.

### Discipline observation

This is the first generator-edit-in-fitness-remediation PR (the build-portal.py change is the substantive deliverable; the portal MD is the regenerated artefact). The generator-output discipline from [`.claude/rules/governance/artefact-and-branch-discipline.md`](../../.claude/rules/governance/artefact-and-branch-discipline.md) requires editing the source and committing both halves together; this PR follows that pattern.

The maintainer also surfaced a content expansion request for [`security/policy-byod.md`](../../security/policy-byod.md): add explicit MDM (Mobile Device Management) vs MAM (Mobile Application Management) options so adopters can choose based on context (personnel population, device categories, regulatory environment). Captured as a follow-up item in TODO; will be a small future PR.

---

## 2026-06-21, Library Version 2026.06.146, PR #164

Closes FR-43 (high[critical], reshape) — data-classification level reconciliation. The canonical standard at `security/standard-data-classification-and-handling.md` defines five levels (Public / Controlled / Internal / Confidential / Restricted); six subordinate documents enumerated only four (Controlled omitted) and one prose line in the remote-working standard explicitly said "four classification tiers", directly contradicting the canonical standard. Reconciled via Option A — propagate the 5-level scheme.

### Closed findings

- **FR-43 (reshape)** (high[critical]): data-classification 5-level standard vs 4-level subordinate-doc subset. The reshape from the original FR-43 ("two competing classification schemes") was completed in PR #141 (Pass-2 maintainer triage) which surfaced the actual issue as a Controlled-level omission, not a competing scheme. Closed by propagating the 5-level scheme to every subordinate document that enumerates the scheme.

### Changed

- [`security/standard-data-classification-and-handling.md`](../../security/standard-data-classification-and-handling.md):
  - Preamble (line 17) extended to state that the five classification levels are authoritative for the corpus and that subordinate documents must enumerate or reference the same five levels.
  - Per-doc version `1.3.1 → 1.3.2`; Date `2026-05-28 → 2026-06-21`.
- [`security/standard-remote-working-security.md`](../../security/standard-remote-working-security.md):
  - §7.1.1 table extended from 4 rows to 5 (added Controlled row matching the canonical standard's external-share-OK definition; remote-access posture mirrors Public).
  - §7.1.1 prose corrected from "four classification tiers" to "five classification levels".
  - Per-doc version `1.0.2 → 1.0.3`.
- [`security/policy-byod.md`](../../security/policy-byod.md):
  - Line 80 clarifying parenthetical added — "(Public, Controlled, and Internal per the [Data Classification and Handling Standard](standard-data-classification-and-handling.md))" — making the meaning of "Internal and lower" explicit rather than implicit.
  - Per-doc version `1.0.0 → 1.0.1`.
- [`privacy/policy-privacy-and-data-governance.md`](../../privacy/policy-privacy-and-data-governance.md):
  - §2 inline enumeration at line 76 extended from "Public, Internal, Confidential, and Restricted" to "Public, Controlled, Internal, Confidential, and Restricted" with explicit cross-reference to the canonical standard.
  - Opportunistic `shall → must` per PR #159 / FR-44 §6.1 convention rolled into the same edit (this is the first corpus-wide-harmonisation contribution).
  - Per-doc version `1.3.0 → 1.4.0` (minor: adds a classification level + opportunistic verb harmonisation).
- [`operations/register-asset-inventory.md`](../../operations/register-asset-inventory.md):
  - Asset Record Schema "Data Classification" field value-list at line 58 extended from four levels to five, with cross-reference to the canonical standard.
  - Per-doc version `1.0.1 → 1.0.2`.
- [`dev-security/standard-security-baseline-and-standards-reference.md`](../../dev-security/standard-security-baseline-and-standards-reference.md):
  - Classification table extended from 4 rows to 5; new Controlled row mirrors the canonical standard's definition.
  - Per-doc version `1.0.0 → 1.1.0` (minor: extends the published scheme).
- [`dev-security/standard-security-quick-reference.md`](../../dev-security/standard-security-quick-reference.md):
  - Practitioner classification table extended from 4 rows to 5; new Controlled row describes encryption (not required at rest; TLS 1.2+ for external sharing in transit) and external-recipient access posture.
  - Per-doc version `1.0.1 → 1.1.0`.
- [`README.md`](../../README.md): library `2026.06.145 → 2026.06.146`; README per-doc `1.9.16 → 1.9.17`.
- [`TODO.md`](../../TODO.md): FR-43 rotated out of High[critical] tier; backlog counters updated (10 + 7 + 56 = 73 immediate; 14 deferred; 87 open). New durable-rule items added to the session-feedback section: (a) validate-cadence amended to 1-8 PRs per batch (was strictly 5); (b) DONE format mirrors TODO format (FR-N (severity) at heading level).
- [`.working/DONE.md`](../DONE.md): PR #164 entry added.

### Documents already at 5 levels (no change)

- `security/standard-data-loss-prevention.md` (two tables, both 5-level)
- `operations/procedure-media-handling-and-transport.md` (§3 and §5.1)
- `governance/standard-records-retention-and-destruction.md` (§"Records classification")

### Verification

- `tools/run_all_audits.sh` exits 0 on all 46 gates post-commit.
- `tools/run-pr-time-checks.sh` exits 0 (D1 + D2 + gate 45).
- Cross-doc validation: every retrofitted document carries an explicit cross-reference to the canonical standard, so a future audit gate could mechanically check that documents enumerating data-classification levels point at the standard's authoritative list.

### Discipline observation

This is the first in-PR application of FR-44's "shall → must" opportunistic conversion (PR #159 / §6.1 rule 4: "legacy 'shall' usage is converted to 'must' opportunistically as documents are revised"). The privacy policy was the natural touch surface here because the edit was already changing that exact bullet's enumeration; bundling the verb fix is lighter-touch than a separate corpus-wide sweep. Surfaced as evidence that opportunistic harmonisation works: FR-44 generalisation is now in progress as a side-effect of in-flight FR remediation rather than as a dedicated sweep PR.

This PR also captures two durable maintainer-direction updates: (a) the validate-cadence rule changes from strictly 5 PRs per batch to 1-8 PRs per batch when logical grouping warrants (a single large PR may justify its own validate; a coherent batch of up to 8 PRs may proceed without a mid-batch validate); (b) the DONE format mirrors TODO's tier-grouped one-line bullet format at the heading level. Both are recorded in TODO's "Critical user feedback to remember across sessions" §.

---

## 2026-06-21, Library Version 2026.06.145, PR #163

Maintainer-directed format harmonisation: `.working/DONE.md` H3 headings now surface `FR-N (severity)` matching the TODO backlog's tier-grouped one-line bullet format. This is a process / maintainability change; no FR item is closed by this PR.

### Maintainer instruction

The maintainer observed that the DONE file did not use the same format as the TODO file, and that scanning large numbers of items across the two surfaces was difficult. Format asymmetry traced to the change-tracking pack rule's "one-paragraph summary" guidance, which described DONE entries as prose without specifying a structured heading. As the fitness backlog grew through 23 closed items across PRs #142-#162, the cost of the mid-body FR-N + severity pattern compounded. The maintainer asked for an assessment of the harmonisation complexity and selected Option A (the lightest-touch path: retrofit the H3 headings, preserve body paragraphs verbatim).

### Changed

- [`.working/DONE.md`](../DONE.md):
  - "How items get here" § rewritten to document the five canonical heading shapes (single-FR PR, multi-FR PR, sweep close-out, non-FR PR, FR-N cross-reference) with severity values mirroring the TODO backlog tiers (`high[critical]`, `high`, `medium`, `low`). The Pass-1 ⚠️ confirmed-with-modification flag is informational and stays in the body, not the heading.
  - 22 historical PR headings retrofitted to surface `FR-N (severity)` at the heading level: PRs #142, #143, #144, #145, #146, #147, #149, #150, #151, #152 (multi-FR), #153, #155, #156, #157, #158, #159, #161, #162. Sweep close-out PRs (#148, #154, #160) unchanged (no single FR anchor).
  - 7 FR-only cross-reference entries retrofitted with severity tags: FR-9, FR-10, FR-13, FR-21, FR-54, FR-55, FR-103.
  - Pre-fitness historical entries (PRs #141 and earlier) left in their original form — those entries pre-date the FR backlog and don't share TODO's tier-grouped scannability problem.
- [`README.md`](../../README.md): library `2026.06.144 → 2026.06.145`; README per-doc `1.9.15 → 1.9.16`.
- [`TODO.md`](../../TODO.md): session-resume snapshot updated. No backlog counter change (this PR doesn't close an FR item).

### Verification

- `tools/run_all_audits.sh` exits 0 on all 46 gates post-commit.
- `tools/run-pr-time-checks.sh` exits 0 (D1 + D2 + gate 45).
- Manual readback: each retrofitted heading now matches the canonical shape documented in the "How items get here" §; body paragraphs preserved verbatim (`git diff --word-diff-regex='[^ ]+' .working/DONE.md` shows only heading-line tokens added, no body changes).

### Discipline observation

The format drift between TODO (bullet form) and DONE (prose form) accumulated over the fitness backlog's growth and was not caught by any audit gate because both formats are valid markdown and `.working/` is exempt from corpus audit gates. A scannability-driven convention is one of the failure-mode classes the mechanical audits don't cover; the maintainer's catch is the kind of feedback that a corpus-management discipline rule could codify. Surfaced as a candidate generalisation for the corpus-management discipline (TODO P4.6): when an ongoing-backlog file and its closed-items companion drift in format, the lighter-touch reconciliation (retrofit headings, keep bodies) is usually preferable to a full content rewrite.

The body text on individual DONE entries still uses inconsistent severity language ("High-severity finding closed", "High[critical] finding closed", etc.). This PR does not touch the bodies; the heading is the authoritative source of severity going forward. Body harmonisation is deferred indefinitely as low-value cleanup.

---

## 2026-06-21, Library Version 2026.06.144, PR #162

Closes FR-29 (high[critical]). The Privacy Impact and Cross-Border Transfer Procedure references a DPIA process but did not previously provide a working DPIA template; adopters could not evidence GDPR Article 35 compliance without inventing one.

### Closed findings

- **FR-29** (high[critical], `privacy/procedure-privacy-impact-and-cross-border-transfer.md` + new template): DPIA methodology and trigger checklist absent. Closed by shipping a new structural template that operationalises the three Article 35 limbs (when a DPIA is required, the EDPB high-risk indicators, what the DPIA must contain) and by cross-referencing it from the operative procedure and the document index.

### Added

- [`privacy/template-dpia.md`](../../privacy/template-dpia.md) (new, version 1.0.0): Data Protection Impact Assessment Template. CC BY-SA 4.0 structural template covering:
  - §1 Article 35(1) trigger checklist: the three explicit Article 35(3) triggers (T1 evaluation/profiling with legal effects; T2 large-scale special-category or criminal-conviction data; T3 large-scale systematic monitoring of publicly accessible area) plus supervisory-authority-list consultation per Articles 35(4) and 35(5).
  - §2 EDPB WP248 nine-criteria framework (endorsed by the EDPB 25 May 2018): the nine indicators of high-risk processing with the "two or more = DPIA required" decision rule, plus the documented-rationale requirement when only one applies.
  - §3 Article 35(7) DPIA content checklist: the four mandatory content blocks split across §3.1 (systematic description), §3.2 (necessity and proportionality), §3.3 (risks to rights and freedoms), §3.4 (mitigation measures). Each block carries a field table operationalising the requirements; risk and treatment rows are cross-referenced.
  - §4 sign-off and review: assessor, DPO review, approver, next-review date, ROPA cross-reference, privacy notice cross-reference.
  - Framework alignment table citing GDPR Articles 35 and 36, UK GDPR Article 35, EDPB WP248 rev.01, LGPD Article 38, PIPL Article 55, EU AI Act Article 27, ISO/IEC 29134:2023, ISO/IEC 27701:2025, NIST Privacy Framework (CT.PO-P5, CM.AW-P5), and AIDA §29.
  - Limitations section explicitly notes the template is a structural baseline; supervisory-authority-published instruments prevail on conflict.

### Changed

- [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../../privacy/procedure-privacy-impact-and-cross-border-transfer.md):
  - §Related Documents: new cross-reference to [`privacy/template-dpia.md`](../../privacy/template-dpia.md).
  - Step 1 (Initiation): adds an explicit anchor for the Article 35(1) trigger and EDPB WP248 checklists, pointing at §1 and §2 of the new template.
  - Step 6 (Record keeping and documentation): the "Completed PIA/AI-IA report" bullet now points at the template for the structural shape.
  - Per-doc version `1.3.2 → 1.3.3` (patch: adds template cross-reference; no substantive procedural change).
- [`governance/register-document-index-and-classification.md`](../../governance/register-document-index-and-classification.md): one new row added in the Privacy domain between the existing DSAR Workflow Template and the Consent Management Framework rows, registering the DPIA template with its applicable framework citations. Per-doc `1.27.24 → 1.27.25` (patch: one row added).
- [`README.md`](../../README.md): library `2026.06.143 → 2026.06.144`; README per-doc `1.9.14 → 1.9.15`.
- [`TODO.md`](../../TODO.md): FR-29 rotated out of High[critical] tier; backlog counters updated (11 + 7 + 56 = 74 immediate; 14 deferred; 88 open).
- [`.working/DONE.md`](../DONE.md): PR #162 entry added.

### Verification

- `tools/run_all_audits.sh` exits 0 on all 46 gates post-commit.
- `tools/run-pr-time-checks.sh` exits 0 (D1 + D2 + gate 45).
- New template carries the canonical 13-field metadata block (gate 1 verifies).
- Cross-references between procedure, template, and document index all resolve.

### Discipline observation

This is the first new-artefact PR in the FR backlog stream (the prior remediation PRs touched existing documents; PR #138 was the closest equivalent — rotation work, not a new artefact). The new artefact carries the canonical metadata block, registers itself in the document index, is cross-referenced bidirectionally from the operative procedure, and lists its applicable framework alignments in the same table-shape used by other templates. The pattern is now in evidence for the remaining new-artefact items in the FR backlog (FR-30 DPA template, FR-31 Privacy-by-Design framework, FR-32 Legitimate Interest Assessment, FR-34 Transfer Impact Assessment).

The DPIA template explicitly does not cover Transfer Impact Assessments (FR-34 / FR-74). The scope discipline is recorded in the template's §Limitations and in the §Scope paragraph that points at the operative procedure's Step 4 as the controller for TIAs until the TIA template ships.

---

## 2026-06-21, Library Version 2026.06.143, PR #161

Closes FR-17 (high, Pass-1 ⚠️ confirmed-with-modification). The exception policy and the Role Authority Register named overlapping approval authorities but did not declare a single source of truth, and the register's RACI row carried a stub placeholder ("Risk Accountable Role") that did not match any role defined in its own authority table. The fix replaces the stub with a tiered reference that mirrors the policy's §2.2 chain, and adds a reciprocal cross-reference clause to the policy that declares §2.2 / §3.5 as the source of truth.

### Closed findings

- **FR-17** (high, `governance/register-role-authority.md` + `governance/policy-exception-and-risk-acceptance-management.md`): RACI "Approve exception" row Accountable cell read "Risk Accountable Role", a placeholder not defined in the register's own authority table; the policy's §2.2 named Department Head / CIO / Executive Committee or Board Risk Committee for the four risk-classified tiers; §3.5 (added in PR #157) anchored renewals on "the §2 approval pathway" with ERC and Board Risk Committee tiers. The two documents did not declare which was authoritative.

### Changed

- [`governance/register-role-authority.md`](../../governance/register-role-authority.md):
  - RACI "Approve exception" row Accountable cell (line 73): "Risk Accountable Role" → "Tiered by risk level per [`governance/policy-exception-and-risk-acceptance-management.md`](policy-exception-and-risk-acceptance-management.md) §2.2 (Department Head for low; CIO for medium; Executive Committee or Board Risk Committee for high or critical; ERC for renewals beyond the original approver, see §3.5)". Convention matches other RACI rows that name a pathway rather than a single role (e.g., "Approve standard" → "Domain Executive or Delegate"; "Perform assurance review" → "Internal Audit or Assurance Function").
  - Per-doc version `1.3.1 → 1.3.2`; Date `2026-06-19 → 2026-06-21`.
- [`governance/policy-exception-and-risk-acceptance-management.md`](../../governance/policy-exception-and-risk-acceptance-management.md):
  - §2 gains a new §2.4 declaring §2.2 (and §3.5) as the source of truth for the RACI's "Approve exception" chain. §2.4 names the adopter-tunable seams explicitly: tier thresholds in §2.2 may be tuned to local governance structure, and named bodies in §3.5 (Board Risk Committee in particular) may be substituted via the §3.4 / §3.5 substitution clauses where the organisation has no equivalent committee. The §2.4 also explains that the RACI row's reference to §2.2 is what makes adopter-local tuning propagate without requiring the RACI to be re-edited.
  - Per-doc version `1.1.1 → 1.2.0` (minor: new §2.4 introduces a new normative cross-reference clause naming the source of truth for the RACI chain).
- [`README.md`](../../README.md): library `2026.06.142 → 2026.06.143`; README per-doc `1.9.13 → 1.9.14`.
- [`TODO.md`](../../TODO.md): FR-17 rotated out of High tier; backlog counters updated (12 + 7 + 56 = 75 immediate; 14 deferred; 89 open).
- [`.working/DONE.md`](../DONE.md): PR #161 entry added.

### Verification

- `tools/run_all_audits.sh` exits 0 on all 46 gates post-commit.
- `tools/run-pr-time-checks.sh` exits 0 (D1 + D2 + gate 45).
- Cross-reference validation: register's "Approve exception" row now links to the policy's §2.2 (path resolves); policy §2.4 links back to the register (path resolves); §3.5 renewal-ceiling pathway introduced in PR #157 remains intact and is now explicitly connected to the RACI via §2.4.
- Pattern consistency: register's other RACI rows that use a "pathway" Accountable formulation (rows "Approve standard", "Perform assurance review") follow the same convention as the new row, so the fix does not introduce a new RACI pattern.

### Discipline observation

This is the second instance in the corpus where a stub or under-specified RACI cell was caught by fitness review (the first was FR-9 / FR-10's CRO accountability shipped in PR #143). Both fixes followed the same shape: name the role in the document that owns the substantive content (the standard or policy that defines the underlying activity), then point the RACI at that document so the RACI stays one-line and the document stays the source of truth. Surfaced as a candidate generalisation for the corpus-management discipline (TODO P4.6): when the RACI calls out a placeholder role not defined in the register's own authority table, the fix is to point at the operative document rather than to add a new role to the register's table.

---

## 2026-06-21, Library Version 2026.06.142, PR #160

Sweep 14 iteration 1 close-out. Four in-window findings caught by Subagents A and B; Subagent C zero findings. All four are FR-44-self-violations or related drift introduced (or surfaced) by the same-day PRs #157 + #159 landing in this batch.

### Closed findings

- **`specification-master-project.md:126`** (multi-surface-incompleteness, warning, in-window): "No directory shall contain non-canonical document types." — PR #159 (FR-44) added §6.1 Requirement-language register to this very same file at line 277, reserving "shall" for external-standard quotations or legacy content. Line 126 is internal normative prose, not a quotation; the spec contradicts the rule it defines. Subagents A and B independently surfaced this finding; deduplicated to one entry.
- **`governance/policy-exception-and-risk-acceptance-management.md:88`** (multi-surface-incompleteness, warning, in-window): "A 4th renewal may not be granted by any authority." — PR #157 (FR-16) authored this prohibition the same day PR #159 (FR-44) introduced §6.1 rule 3 ("Do not use 'may not' as a prohibition... Where the intent is a prohibition, write 'must not'."). The verb-register convention and the new prohibition contradict each other.
- **`governance/policy-exception-and-risk-acceptance-management.md:94`** (multi-surface-incompleteness, warning, in-window): "Re-baselining may not be used to bypass the ceiling" — same class as the line 88 finding.
- **`TODO.md:22`** (stale-pr-reference, note, in-window): "Next, PR #N: First fitness-remediation PR (maintainer-directed)... No remediation begins until the maintainer directs." — 21 fitness-remediation PRs have shipped under maintainer direction since this text was written. Subagent B surfaced this.

### Changed

- [`specification-master-project.md`](../../specification-master-project.md):
  - §4.1 rule 2: "No directory shall contain non-canonical document types." → "Directories must not contain non-canonical document types." Sentence rephrased to read naturally with "must not" (the original "No directory shall" passive-voice construction does not flip cleanly to "No directory must"; the active-voice "Directories must not" preserves the prohibition).
  - Per-doc version `1.6.0 → 1.6.1`.
- [`governance/policy-exception-and-risk-acceptance-management.md`](../../governance/policy-exception-and-risk-acceptance-management.md):
  - §3.5 table 4th-renewal row last sentence: "A 4th renewal may not be granted by any authority." → "A 4th renewal must not be granted by any authority."
  - §3.6 Re-baselining carve-out: "Re-baselining may not be used to bypass the ceiling" → "Re-baselining must not be used to bypass the ceiling".
  - Per-doc version `1.1.0 → 1.1.1` (patch: targeted normative-vocabulary fixes; no semantic change).
- [`TODO.md`](../../TODO.md): Queued-sequence section rewritten. The "Next, PR #N: First fitness-remediation PR" framing is replaced by a description of the working pattern (the assistant picks 5 at a time, runs a worker-drafts pipeline, applies serially with CI gating, runs `/validate` after each 5-PR batch; maintainer direction supersedes the assistant's pick at any time). The "Then, fitness backlog Pass-2 batches" paragraph is removed (subsumed). FR-14 maturity-ladder reconciliation and FR-44-generalisation are named as queued large items needing deliberate scheduling.
- [`README.md`](../../README.md): library `2026.06.141 → 2026.06.142`; README per-doc `1.9.12 → 1.9.13`.
- [`.working/DONE.md`](../DONE.md): PR #160 entry added.
- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md): Sweep 14 iter 1 row added (reverse-chronological top); per-doc `2.0.6 → 2.0.7`.
- [`.working/validate-sweeps/2026-06-21-sweep14-iter1.md`](../validate-sweeps/2026-06-21-sweep14-iter1.md): per-iteration detail file created with the six required H2 sections.

### Verification

- `tools/run_all_audits.sh` exits 0 on all 46 gates post-commit.
- `tools/run-pr-time-checks.sh` exits 0 (D1 + D2 + gate 45).
- Contradiction grep for "shall" in `specification-master-project.md`: 3 remaining occurrences, all in §6.1 itself describing the convention (lines 277-280) — meta-references, not normative uses. Master spec is now consistent with its own §6.1.
- Contradiction grep for "may not" used as prohibition in `governance/policy-exception-and-risk-acceptance-management.md`: zero occurrences post-edit.

### Discipline observation

This Sweep 14 iteration surfaced a recurring failure mode: **same-day same-batch convention-self-violation**. PR #157 authored new prohibitions in §3.5 / §3.6 of the exception policy on 2026-06-21; PR #159 authored the §6.1 verb register prohibiting that exact construct, also on 2026-06-21. The two PRs were prepared in parallel by the worker-drafts pipeline (FR-16 worker did not see FR-44 worker's draft and vice versa); the maintainer applied them serially with passing CI on each, but the CI did not check cross-PR coherence because the convention rule it would have violated was not yet committed at the time PR #157's pre-commit ran.

A future audit-gate candidate to address this class: a "convention-introduction batch-coherence" check that, when a PR adds a new convention rule, scans the same PR's diff (and ideally adjacent PRs in the same /validate batch) for violations of that rule. Not in scope for this PR; surfaced for future consideration. The current /validate sweep at end-of-batch is the existing safety net for this class — and it worked: Subagents A and B both caught the contradiction independently.

The Subagent C future-gate candidates (ordinal-ceiling pattern; numerical-coherence retention-period extension) are recorded in this entry for traceability but not actioned.

---

## 2026-06-21, Library Version 2026.06.141, PR #159

Closes FR-44 (high, requirement-language register drift). The library had a de facto "must" / "must not" requirement-language convention but the convention had never been documented at the library level. The master specification now states it explicitly so reviewers and authors can cite it.

### Closed findings

- **FR-44** (high, multiple documents): Requirement-language register drift — "must" vs "shall" used inconsistently across the corpus with no documented convention. The fitness review confirmed the corpus is predominantly "must" (e.g., 24 "must" vs 1 "shall" in `security/standard-remote-working-security.md`) but the project had never declared this as policy. PR #150 (FR-45) and PR #154 implicitly settled on "must" / "must not" for prohibitions; this PR documents the convention as library-wide.

### Changed

- [`specification-master-project.md`](../../specification-master-project.md):
  - New §6.1 "Requirement-language register" added immediately after the §6 numbered list. States RFC 2119 / RFC 8174 semantics for "must" / "must not" / "should" / "should not" / "may"; reserves "shall" / "shall not" for direct quotation of external standards (ISO/IEC, NIST SP, IEC) or legacy content awaiting harmonisation; calls out the FR-45 "may not" ambiguity and prohibits "may not" as a prohibition.
  - Five numbered rules in §6.1 plus a closing paragraph noting that a future audit gate may mechanise the rule.
  - Per-doc version `1.5.2 → 1.6.0` (minor: new normative library-wide convention with citable external-standard cross-references; not a patch because the rule is new content rather than a clarification, not major because it does not invalidate prior content).
- [`README.md`](../../README.md): library `2026.06.140 → 2026.06.141`; README per-doc `1.9.11 → 1.9.12`.
- [`TODO.md`](../../TODO.md): FR-44 rotated out of High tier; backlog counters updated (12 + 8 + 56 = 76 immediate; 14 deferred; 90 open). A separate "FR-44 follow-up / FR-44-generalisation" item added under Backlog totals to track the corpus-wide harmonisation sweep deferred from this PR.
- [`.working/DONE.md`](../DONE.md): PR #159 entry added.

### Verification

- `tools/run_all_audits.sh` exits 0 on all 46 gates post-commit.
- `tools/run-pr-time-checks.sh` exits 0 (D1 + D2 + gate 45).
- Manual readback: §6.1 cross-references resolve (`compliance/procedure-capa.md` §6.3.1 mentioned in the rationale but not as a hard link, intentional — the rule does not bind that procedure, only states a parallel cadence); RFC 2119 / RFC 8174 cited with authors (Bradner / Leiba) and years for traceability.

### Discipline observation

This is the third recent PR (after FR-1 framing-drift and FR-2 navigation-drift) where the corpus had implicitly adopted a convention through accumulated practice but had not declared it formally. The pattern: a convention emerges from incremental decisions during fitness-driven remediation; the convention works because individual authors mirror existing files; but a new author or a strict reviewer cannot cite a source for the rule. Surfaced as a candidate generalisation: at every fitness review, check whether implicit conventions have crystallised that should be promoted into the master spec. Not in scope for this PR.

The FR-44 corpus-wide harmonisation sweep (legacy "shall" → "must" across the corpus) is deferred to a separate cleanup batch. The convention statement is the deliverable this PR closes; the sweep is a derivative item now tracked in TODO.

---

## 2026-06-21, Library Version 2026.06.140, PR #158

Closes FR-80 (high[critical], SIEM / cloud-activity-log retention contradiction). Two documents disagreed on the retention period for cloud-activity logs forwarded into the SIEM: `governance/register-data-retention-schedule.md` row "SIEM event logs" said 3 years (1y hot + 2y cold), while `operations/standard-cloud-security-configuration-baseline.md` §6.3 said 90 days minimum. The 90-day figure was best read as the platform-side forwarding floor (so the SIEM has a window in which to ingest events) rather than the authoritative retention; the two documents now say so explicitly with cross-references to each other.

### Closed findings

- **FR-80** (high[critical], cross-document retention contradiction): The 90-day cloud-platform minimum and the 3-year SIEM retention sat at different layers of a forwarding pipeline but neither document said so; the contradiction was silent. The reconciliation treats the cloud platform as the source-of-truth for the most recent 90 days and the SIEM as the authoritative retention for the long-tail. Real-world cloud platforms ship 90-day defaults on their native activity-log services (Azure Activity Log, AWS CloudTrail event history, GCP Cloud Audit Logs free tier); forcing a 1-year platform-side floor would either require a paid retention upgrade or a separate long-term storage configuration on every platform, whereas the forwarding-floor framing achieves the same outcome at lower operational cost.

### Changed

- [`operations/standard-cloud-security-configuration-baseline.md`](../../operations/standard-cloud-security-configuration-baseline.md):
  - §6.3 third bullet (line 150): "Activity log retention minimum: 90 days." expanded to clarify the 90-day figure is the platform-side forwarding floor; once forwarded, events are retained per the SIEM event-logs row of the data retention schedule (1y hot + 2y cold). Cross-link to the retention schedule added.
  - Per-doc version `1.4.3 → 1.4.4`; Date `2026-06-20 → 2026-06-21`.
- [`governance/register-data-retention-schedule.md`](../../governance/register-data-retention-schedule.md):
  - §3 "Information security records" SIEM event logs row (line 67): row title clarified to "SIEM event logs (including cloud platform activity logs forwarded into the SIEM)"; rationale expanded to note this row is the authoritative retention for cloud activity-log events forwarded from cloud platforms, with the platform-side 90-day minimum cross-referenced.
  - Per-doc version `1.0.0 → 1.0.1`; Date `2026-05-27 → 2026-06-21`.
- [`README.md`](../../README.md): library `2026.06.139 → 2026.06.140`; README per-doc `1.9.10 → 1.9.11`.
- [`TODO.md`](../../TODO.md): FR-80 rotated out of High[critical] tier; backlog counters updated (12 + 9 + 56 = 77 immediate; 14 deferred; 91 open). New top-level section "Pack: dev-security/claude-rules language coverage review" added at maintainer's direction: review whether mainstream non-Python languages need baseline files in the pack and whether the pack should reference dedicated technical-security projects for deeper coverage.
- [`.working/DONE.md`](../DONE.md): PR #158 entry added.

### Verification

- `tools/run_all_audits.sh` exits 0 on all 46 gates post-commit.
- `tools/run-pr-time-checks.sh` exits 0 (D1 + D2 + gate 45).
- Manual readback: cloud baseline §6.3 link to retention schedule resolves; retention schedule SIEM row link to cloud baseline resolves; no remaining mention of "90 days" or "3 years" in either document drifts away from the new framing.

### Discipline observation

This is a class of cross-document defect (two documents naming the same numeric threshold from different layers of a pipeline without the relationship documented) that the mechanical numerical-coherence audit could have caught — `tools/lint-cross-doc-numbers.py` already detects same-term divergence and would have flagged this pair if the regex had pattern-matched "SIEM" or "cloud activity log" against an hours/days value. The current pattern set is narrowly scoped to high-confidence cases (GDPR breach-notification hours, P1/P2/P3 acknowledgement times). Expanding the pattern set to cover retention periods is a candidate audit-programme enhancement; surfaced as a future consideration. Not in scope for this PR.

---

## 2026-06-21, Library Version 2026.06.139, PR #157

Closes FR-16 (high[critical], exception register hard caps + renewal-ceiling escalation pathway). The exception register schema previously lacked hard ceiling fields, and §3.1 used a soft "should not exceed 180 days" clause that allowed indefinite drift under repeated soft renewals. The fix mirrors PR #152's FR-19 CAPA §6.3.1 ceiling pattern so the two registers escalate on the same cadence when both have been opened against the same underlying gap.

### Closed findings

- **FR-16** (high[critical], `governance/policy-exception-and-risk-acceptance-management.md`): Exception register schema lacked `max_duration` and `renewal_count_limit` fields; the "should not exceed 180 days" clause was unenforceable. The fix adds both fields to the schema (§1.2 and §5.1), strengthens §3.1 to a hard initial-term cap, and introduces §3.4 (cumulative max_duration), §3.5 (renewal-ceiling escalation pathway), §3.6 (re-baselining carve-out with anti-abuse condition), and §3.7 (rationale for the specific numbers).

### Changed

- [`governance/policy-exception-and-risk-acceptance-management.md`](../../governance/policy-exception-and-risk-acceptance-management.md):
  - §1.2 (Exception request and registration): schema extended to require `max_duration` (default 540 days) and `renewal_count_limit` (default 3) on every register entry, with forward cross-references to §3.4 and §3.5.
  - §3.1 (Duration and renewal): weak "should not exceed 180 days unless renewed with justification" replaced by a hard 180-day initial-term cap. The renewal scope moves to §3.4 / §3.5 below.
  - §3.4 (new): cumulative `max_duration` ceiling of 540 days (three 180-day terms) unless an explicit higher cap is approved by the Board Risk Committee at original registration. When reached, the exception must be remediated, descoped, converted to a formal risk acceptance, or replaced by a re-baselined entry; further renewal is not permitted at any authority level.
  - §3.5 (new): renewal-ceiling escalation pathway with a 4-row table: 1st renewal at the original approver per §2.2; 2nd at the ERC (remediation-feasibility memo + compensating-control revalidation required); 3rd at the Board Risk Committee (root-cause-and-remediation-pathway memo + explicit residual-risk acceptance); 4th absolutely prohibited (forces close, descope, conversion to risk acceptance, or re-baseline). The `renewal_count_limit` field defaults to 3; a lower limit may be set per-entry but a higher limit cannot be set (policy-wide prohibition).
  - §3.6 (new): re-baselining carve-out for materially-changed scope (ERC-approved, with anti-abuse condition: a re-baseline without material change is treated as the next renewal in the sequence).
  - §3.7 (new): rationale paragraph explaining why 540/3/4 were chosen (mirrors CAPA §6.3.1 cadence for cross-register escalation consistency).
  - §5.1 (Tracking and reporting): central register field list extended in lock-step with `max_duration`, `renewal_count_limit`, and current renewal count.
  - Per-doc version `1.0.3 → 1.1.0` (minor: schema-level addition of two required fields + four new subsections in §3).
- [`README.md`](../../README.md): library `2026.06.138 → 2026.06.139`; README per-doc `1.9.9 → 1.9.10`.
- [`TODO.md`](../../TODO.md): FR-16 rotated out of High[critical] tier; backlog counters updated (13 + 9 + 56 = 78 immediate; 14 deferred; 92 open).
- [`.working/DONE.md`](../DONE.md): PR #157 entry added.

### Verification

- `tools/run_all_audits.sh` exits 0 on all 46 gates post-commit.
- `tools/run-pr-time-checks.sh` exits 0 (D1 + D2 + gate 45).
- Cross-reference validation: §3.4 cross-reference to `risk/procedure-risk-acceptance.md` resolves; §3.7 cross-reference to `compliance/procedure-capa.md` §6.3.1 resolves; §5.2 reciprocal field (added in PR #148) is preserved unchanged.
- No corpus citations to the prior "should not exceed 180 days" language found anywhere else in the corpus (grep clean).

### Discipline observation

This is the second instance in the corpus where an open-ended renewal/extension authority has been hardened with a 1-2-3-prohibited escalation pattern (the first was PR #152 / FR-19 for CAPA target-date extensions). The two registers now use mathematically-identical thresholds at the same governance tiers (1st at original approver, 2nd at ERC, 3rd at Board Risk Committee, 4th not permitted), with the re-baselining carve-out structured the same way in each. This is intentional: when the same underlying gap produces both an open CAPA and an active exception, the two are designed to escalate together rather than at different cadences. Surfaced as a candidate generalisation: a future "governance-ceiling pattern" rule in the discipline pack could document this 1-2-3-prohibited shape as the canonical form for any open-ended authority that needs a hard upper bound. Not in scope for this PR.

---

## 2026-06-21, Library Version 2026.06.138, PR #156

Closes FR-2 (high, README "How to use" step 1 navigation). The "How to use" section's step 1 had directed readers to the 300-row document index before the audience-keyed portal. A first-time visitor reading the README sequentially landed first on the "New to GRC?" block (which points at [`docs/portal.md`](../../docs/portal.md)) and then on "How to use" step 1 (which contradicted that signposting by pointing at the document index instead). Step 1 now opens with the portal as the primary pointer.

### Closed findings

- **FR-2** (high, `README.md`): "How to use" step 1 buried the audience-keyed entry by pointing at the 300-row document index first. The fix reorders so [`docs/portal.md`](../../docs/portal.md) is the primary pointer in step 1, with the document index retained as a named secondary pointer for readers who already know what they want.

### Changed

- [`README.md`](../../README.md): "How to use" step 1 now opens with "Start at the audience-keyed portal" pointing at [`docs/portal.md`](../../docs/portal.md). The document index reference is preserved as a secondary pointer in the same step. Steps 2-5 unchanged.
- [`README.md`](../../README.md): library `2026.06.137 → 2026.06.138`; README per-doc `1.9.8 → 1.9.9`.
- [`TODO.md`](../../TODO.md): FR-2 rotated out of High tier; backlog counters updated (14 + 9 + 56 = 79 immediate; 14 deferred; 93 open).
- [`.working/DONE.md`](../DONE.md): PR #156 entry added.

### Verification

- `tools/run_all_audits.sh` exits 0 on all 46 gates post-commit.
- `tools/run-pr-time-checks.sh` exits 0 (D1 + D2 + gate 45).
- Manual re-read confirmed: step 1 leads with the portal; document index retained as secondary pointer; steps 2-5 unchanged; no contradiction with the "New to GRC?" block.

### Discipline observation

PR #147 added the "New to GRC?" block on the README routing first-time visitors to the portal; the older "How to use" step 1 was authored before the portal existed and pointed at the document index, which was the canonical navigation surface at that time. The drift accumulated because the older content was not revisited when the newer block was added. Surfaced as a candidate generalisation: when introducing a new navigation surface, audit existing sequential navigation pointers in the same document to ensure they are consistent with the new top-of-funnel.

---

## 2026-06-21, Library Version 2026.06.137, PR #155

Closes FR-1 (high, README "What this repository is" framing). The previous "two coordinated halves" formulation gave the GRC corpus and the AI-assisted-maintenance reference implementation equal billing. The fitness review judged this misframed the project's primary value: the corpus is the product, the maintenance discipline is the methodology that keeps it consistent. This PR re-frames the section so the corpus is the unambiguous headline product and the audit toolchain plus the `dev-security/claude-rules/` pack are positioned as the operational layer.

### Closed findings

- **FR-1** (high, `README.md`): "Dual-mission" / "two coordinated halves" framing elevated the AI-assisted-maintenance work to equal billing with the GRC corpus. The fix re-frames the section so the corpus is the headline; the toolchain and pack are described as the methodology used to maintain the corpus. Factual content (existence of pack, co-evolution history) preserved.

### Changed

- [`README.md`](../../README.md): "What this repository is" section rewritten. The corpus is named as the primary identity in the first paragraph. The audit toolchain and the pack appear in the second paragraph as the operational layer supporting maintenance, with the pack's standalone use case retained as a factual statement (consistent with the "Three adoption modes" section that follows, which is untouched). The co-evolution paragraph is preserved but reordered to make the causal direction explicit (the corpus generated the disciplines, not the reverse).
- [`README.md`](../../README.md): library `2026.06.136 → 2026.06.137`; README per-doc `1.9.7 → 1.9.8`.
- [`TODO.md`](../../TODO.md): FR-1 rotated out of High tier; backlog counters updated (14 + 10 + 56 = 80 immediate; 14 deferred; 94 open).
- [`.working/DONE.md`](../DONE.md): PR #155 entry added.

### Preserved

- The "Three adoption modes" section is untouched; the pack-only adoption mode remains a documented option.
- All factual claims about the existence and content of the audit toolchain and the pack remain. The change is one of framing and emphasis.
- The CC BY-SA 4.0 licensing claim and the eleven-domain inventory remain unchanged.

### Verification

- `tools/run_all_audits.sh` exits 0 on all 46 gates post-commit.
- `tools/run-pr-time-checks.sh` exits 0 (D1 + D2 + gate 45).
- Contradiction grep for `two coordinated halves`, `content half`, `Dual-mission`, `dual mission` across the corpus: zero post-edit occurrences.

### Discipline observation

The original "two coordinated halves" framing was likely written when the pack was newer and more attention-grabbing than the corpus. As the corpus has matured (300+ documents, 11 domains, 46 audit gates), the framing has drifted out of accurate proportion. This is a class of finding (framing-drift over time) that audit gates cannot catch — only periodic editorial review or fitness-style external reads will surface it. Surfaced as a candidate generalisation for the corpus-management discipline (TODO P4.6): when a project's primary deliverable matures faster than its surrounding methodology, the framing of the methodology may need periodic re-grounding.

---

## 2026-06-21, Library Version 2026.06.136, PR #154

Sweep 13 iteration 1 close-out. Five out-of-window findings from Subagent A (recent-PR deep review); Subagents B (corpus-wide stale-reference) and C (audit-programme integrity) returned zero findings each. Detail report at [`.working/validate-sweeps/2026-06-21-sweep13-iter1.md`](../validate-sweeps/2026-06-21-sweep13-iter1.md).

### Closed findings

- **FR-45-generalisation, ai/ domain** (3 occurrences, multi-surface incompleteness): PR #150's "may not" → "must not be" RFC 2119 fix had scoped its corpus-wide grep to `security/` only, missing three parallel occurrences in `ai/`. Each had the same MUST-NOT semantics as the originally-fixed lines.
- **FR-92-generalisation, BASC IT KPIs register** (1 occurrence, multi-surface incompleteness): PR #153 added `Escalation Owner` + `Remediation Sign-off` columns to the IT-ops register and introduced the design principle requiring both fields on every KPI. The parallel BASC sector-specific KPI register has the same structural role (per-KPI table with Owner column) but lacked the new columns.
- **Document history table drift, BASC IT KPIs register** (1 occurrence, stale prose reference): file's frontmatter declared Version 1.1.1, but the embedded Document history table only listed 1.0.0. Frontmatter-vs-history-table consistency gap.

### Changed

- [`ai/standard-ai-and-agentic-development-security.md`](../../ai/standard-ai-and-agentic-development-security.md):
  - `ADTEST-SEC-02` (line 543): `Test cases may not be removed from the suite without CISO approval.` → `Test cases must not be removed from the suite without CISO approval.`
  - `OFFAI-SEC-10` (line 718): `...may not be embedded in proprietary tooling chains;` → `...must not be embedded in proprietary tooling chains;` (within the existing AGPLv3/GPL-3.0 licence-restriction context, where the intent is a legal prohibition).
  - Per-doc version `1.8.1 → 1.8.2`; Date `2026-06-19 → 2026-06-21`.
- [`ai/guide-ai-adversarial-test-reference.md`](../../ai/guide-ai-adversarial-test-reference.md):
  - Line 164 parallel restatement of `ADTEST-SEC-02`: `Test cases may not be removed without CISO approval` → `Test cases must not be removed without CISO approval`. Updated in lock-step with the standard.
  - Per-doc version `1.3.0 → 1.3.1`; Date `2026-05-28 → 2026-06-21`.
- [`compliance/logistics/register-basc-it-compliance-kpis.md`](../../compliance/logistics/register-basc-it-compliance-kpis.md):
  - Single KPI table gains two new columns: `Escalation Owner` and `Remediation Sign-off`. Role assignments mirror PR #153's design rule: CISO escalation for IT-ops-style KPIs (training completion is ERC because owner is already CISO; phishing simulation, patching, MFA, access review, offboarding, vulnerability remediation all CISO); ERC escalation where Owner Role is already CISO (incident volume, MTTR, exception register currency, training completion).
  - Document history table backfilled with rows for `1.1.0`, `1.1.1`, and `1.2.0` to reconcile the frontmatter-vs-history-table discontinuity.
  - Per-doc version `1.1.1 → 1.2.0` (minor: schema-level column addition).
  - Date `2026-05-28 → 2026-06-21`.
- [`README.md`](../../README.md): library `2026.06.135 → 2026.06.136`; README `1.9.6 → 1.9.7`.
- [`TODO.md`](../../TODO.md): session-resume snapshot updated to reflect Sweep 13 close-out.
- [`.working/DONE.md`](../DONE.md): PR #154 entry added.
- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md): Sweep 13 iter 1 row added (reverse-chronological top).
- [`.working/validate-sweeps/2026-06-21-sweep13-iter1.md`](../validate-sweeps/2026-06-21-sweep13-iter1.md): per-iteration detail file created with the six required H2 sections (Trigger & state snapshot; Subagent A; Subagent B; Subagent C; Orchestrator synthesis; Resulting PR).

### Verification

- `tools/run_all_audits.sh` exits 0 on all 46 gates post-commit.
- `tools/run-pr-time-checks.sh` exits 0 (D1 + D2 + gate 45).
- Corpus-wide grep for `may not` (used as a prohibition) in `ai/`: zero occurrences post-edit on the three target lines.

### Discipline observation

The FR-45 scope-limitation in PR #150 (corpus grep restricted to `security/`) is the proximate cause of the three `ai/` findings surfacing in Sweep 13 rather than being caught at PR-150-merge time. Generalising the FR-45 corpus grep to the full corpus when the original PR ships would have caught these. A future audit gate or sweep heuristic that flags "may not" used as a prohibition across the full corpus would catch the same pattern systematically; surfaced for future consideration. Not in scope for this PR.

The FR-92 design principle introduced in PR #153 was framed as a register-local rule for the IT-ops register; whether it should be promoted to a corpus-normative requirement (i.e., every KPI register must carry these two columns) is a separate question. This close-out applies it to the one clearly-parallel register identified by Subagent A but does not declare a corpus-wide invariant.

---

## 2026-06-21, Library Version 2026.06.135, PR #153

Closes FR-92 (high). The IT Operations KPI register defined targets without identifying who escalates when a target is missed and who signs off that a breach event is closed; the register now records both roles per KPI.

### Closed findings

- **FR-92** (high, ✅ confirmed-as-stated, `operations/register-it-operations-kpis.md`): KPI tables defined Owner Role (the operating-accountability role) but no Escalation Owner (the role paged when the target is breached) and no Remediation Sign-off (the role that closes the breach). A breached KPI had no documented governance path: the Owner Role is responsible for measurement, not for breach response. Audit-trail gap: an auditor reviewing a breach record could not determine from the register alone who authorised the remediation or who signed it off.

### Changed

- [`operations/register-it-operations-kpis.md`](../../operations/register-it-operations-kpis.md):
  - All eight KPI tables (Sections 1-8) gain two new columns: `Escalation Owner` and `Remediation Sign-off`. The columns are positioned after `Evidence Class` and before `Notes` so the breach-response governance is adjacent to the evidence-class field that supports it.
  - KPI design principles gain a new principle 2 requiring both fields to be populated from the [Role Authority Register](../../governance/register-role-authority.md); existing principles 2-6 renumber to 3-7.
  - `Related Documents` field gains `governance/register-role-authority.md`.
  - Per-doc version `1.0.0 → 1.1.0` (minor: schema-level addition of two columns and one design principle).
  - Date `2026-05-27 → 2026-06-21`.
- [`README.md`](../../README.md): library `2026.06.134 → 2026.06.135`; README `1.9.5 → 1.9.6`.
- [`TODO.md`](../../TODO.md): FR-92 rotated out of the High tier; backlog counters updated (14 + 11 + 56 = 81 immediate; 14 deferred; 95 open).
- [`.working/DONE.md`](../DONE.md): PR #153 entry added.

### Role-assignment rationale

- **Default Escalation Owner = Chief Information Officer** for IT-operations KPIs (Sections 1, 2, 3, 4, 6, 7).
- **Default Escalation Owner = Chief Information Security Officer** for security-flavoured KPIs (Section 5 patch/vulnerability/EDR; Section 8 security operations).
- **Escalation Owner = Enterprise Risk Committee** where the KPI's Owner Role is already CIO (e.g., `Major incident frequency`) or CISO (e.g., `NIS 2 notification compliance`); a role cannot meaningfully escalate to itself, so the next governance tier (ERC) takes that role.
- **Remediation Sign-off = same role as Escalation Owner**: the role that owns the breach response is also the role that confirms the breach is closed; splitting these would create unnecessary co-ordination overhead.

### Verification

- `tools/run_all_audits.sh` exits 0 on all 46 gates post-commit.
- `tools/run-pr-time-checks.sh` exits 0 (D1 + D2 + gate 45).
- Manual readback: every KPI row now has both new columns populated; no empty cells; role names verbatim from `governance/register-role-authority.md`.

### Discipline observation

This is a schema-level change to a register document, so the per-doc version receives a minor bump (`1.0.0 → 1.1.0`) rather than a patch. The pattern echoes PR #147's `1.8.84 → 1.9.0` for the README "New to GRC?" section: structural additions that downstream consumers of the artefact would need to be aware of warrant a minor bump under the project's semver convention.

The two-column shape was selected over alternatives (sidecar block per KPI, single new section listing per-KPI escalation owners) because locality wins: the breach-response governance lives next to the KPI it governs, making it discoverable from a single row read and avoiding the maintenance burden of keeping a separate section synchronised.

---

## 2026-06-21, Library Version 2026.06.134, PR #152

Closes FR-19 (high[critical]) and FR-20 (high), both in [`compliance/procedure-capa.md`](../../compliance/procedure-capa.md). FR-19 addressed the absence of a hard ceiling on CAPA target-date extensions: §6.3 documented per-extension approval authority but no cap, allowing Critical findings to remain open indefinitely under repeated single-step CISO sign-off. FR-20 addressed the absence of a quality checklist for CAPA root-cause statements: §4.1's aspirational "specific and actionable" wording was satisfied by bare category labels like "process gap".

### Closed findings

- **FR-19** (high[critical]): CAPA extension governance ceiling. §6.3 / §9.1 documented per-extension approval authorities (CISO for Critical, GRC Manager for High/Moderate/Low) but no cap on the *number* of extensions before a higher tier of governance had to look at the item. The §9.1 escalation table's last row ("Repeated extensions or sustained non-closure") gestured at ERC review but left it as "determines appropriate response" with no quantitative trigger. The pre-existing "extended more than twice" soft trigger for Moderate/Low CAPAs in the sentence after the §9.1 table was the closest thing to a ceiling but did not extend to Critical/High and was not paired with an escalation pathway.
- **FR-20** (high): CAPA root-cause quality checklist. §4.1 stated "the root cause statement must be specific and actionable" without defining either term, so bare category labels from the §4.3 taxonomy (e.g., "Process gap") satisfied the wording as written. The §4.3 taxonomy is for *pattern aggregation*, not per-statement quality, but the procedure did not distinguish the two uses.

### Changed

- [`compliance/procedure-capa.md`](../../compliance/procedure-capa.md):
  - §4.1: new subsection 4.1.1 "Root cause statement quality checklist" added between the existing "specific and actionable" paragraph and the timing paragraph. Five-criterion checklist (Specific / Causal / Actionable / Bounded / Evidence-anchored) with explicit exclusions; applied by the GRC Manager during verification (Section 7.2). The §4.3 root-cause-category taxonomy is explicitly subordinated to the per-statement checklist so category-only statements fail the Specific criterion regardless of category accuracy.
  - §6.3: new subsection 6.3.1 "Extension ceiling and escalation pathway" added after the existing §6.3 closing paragraph. Hard ceiling: 2nd extension to ERC, 3rd to Board Risk Committee, 4th not permitted (forcing close / descope / re-baseline). Re-baselining carve-out for materially-changed root causes (ERC-approved, with anti-abuse condition).
  - §9.1: "Repeated extensions or sustained non-closure" row updated to cross-reference §6.3.1 instead of the prior open-ended wording. Trailing sentence about Moderate/Low CAPAs rewritten so the pre-existing inconsistent "extended more than twice" soft trigger is replaced by an explicit cross-reference to the §6.3.1 ceiling, which applies uniformly to all classifications.
  - Per-doc version `1.0.1 → 1.0.2`; Date `2026-05-28 → 2026-06-21`.
- [`README.md`](../../README.md): library `2026.06.133 → 2026.06.134`; README `1.9.4 → 1.9.5`.
- [`TODO.md`](../../TODO.md): FR-19 rotated out of High[critical] tier; FR-20 rotated out of High tier. Backlog counters updated (14 + 12 + 56 = 82 immediate; 14 deferred; 96 open).
- [`.working/DONE.md`](../DONE.md): PR #152 entry added.

### Verification

- `tools/run_all_audits.sh` exits 0 on all 46 gates post-commit.
- `tools/run-pr-time-checks.sh` exits 0 (D1 + D2 + gate 45).
- Manual cross-reference: every section number cited in the new text (§4.1, §4.3, §6.3, §7.2, §8.1, §9.1, §9.2) is present in the document and referenced as labelled.

### Discipline observation

The 2/3/4 ceiling defaults were selected to (a) match the pre-existing Moderate/Low "extended more than twice" soft trigger at the 2-extension threshold, (b) reflect that a CAPA which has slipped three times is a governance-risk issue requiring highest-body acceptance of residual exposure, and (c) force a binary decision rather than allowing indefinite drift through serial approvals. The re-baselining mechanism in §6.3.1 has an anti-abuse condition (re-baseline requires a materially-changed root cause, is itself ERC-approved, and a re-baseline not resting on a material change is treated as the next extension) so it cannot be used to silently reset the count.

Two findings bundled in one PR because both live in the same file; the audit programme treats this as a single change.

---

## 2026-06-21, Library Version 2026.06.133, PR #151

Closes FR-35 (high, ✅ confirmed-as-stated, privacy breach-response). The privacy breach-response procedure mentioned the contractual 24-hour supplier notification window in three places but never anchored its clock-start to processor awareness — the GDPR Article 33(2) trigger. Adopters reading the procedure in isolation could reasonably interpret the 24-hour window as starting at controller notification (inverting Article 33(2)) or at some later containment/assessment milestone. This PR makes the asymmetry explicit and ties it directly to Article 33(2).

### Closed findings

- **FR-35** (high, ✅, `privacy/procedure-data-protection-and-privacy-breach-response.md`): Article 33(2) processor-to-controller breach timeline asymmetry not made explicit. The procedure's §4.1 detection-sources bullet, §6.3 supplier-notification section, and §10 supplier-notification metric all named the 24-hour contractual window without specifying that the clock starts at *processor* awareness. The companion document `supply-chain/standard-supplier-security-and-privacy-assurance.md` line 91 already states "Data breach notification within 24 hours of awareness" and cites GDPR Article 33(2); the privacy procedure now matches.

### Changed

- [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../../privacy/procedure-data-protection-and-privacy-breach-response.md):
  - §4.1 detection-sources bullet (line 89): clock-start anchored to "becoming aware" with cross-reference to §6.3 for the Article 33(2) basis.
  - §6.3 Supplier notification: new "**Note: processor-to-controller timeline asymmetry under GDPR Article 33(2)**" callout explaining that the 24-hour contractual clock and the 72-hour Article 33(1) regulatory clock anchor to two different awareness events, that the 24-hour clock starts at *processor* awareness (not controller notification, not controller awareness, not any later containment milestone), and that a delayed Article 33(2) notification erodes the controller's 72-hour Article 33(1) budget. Existing bullet list tightened in parallel to say "within 24 hours of becoming aware".
  - §10 metric "Supplier Breach Notification Timeliness": definition reworded to specify the supplier's awareness as the clock-start, with explicit Article 33(2) citation and §6.3 cross-reference.
  - Per-doc version `1.4.3 → 1.4.4`; Date `2026-06-20 → 2026-06-21`.
- [`README.md`](../../README.md): library `2026.06.132 → 2026.06.133`; README `1.9.3 → 1.9.4`.
- [`TODO.md`](../../TODO.md): FR-35 rotated out of High tier; backlog counters updated (15 + 13 + 56 = 84 immediate; 14 deferred; 98 open).
- [`.working/DONE.md`](../DONE.md): PR #151 entry added.

### Verification

- Local audit: `tools/run_all_audits.sh` exits 0 on all 46 gates post-commit.
- Local PR-time checks: `tools/run-pr-time-checks.sh` exits 0.
- Contradiction grep: `grep -nE '24[- ]hour' privacy/procedure-data-protection-and-privacy-breach-response.md` confirms every remaining mention of the 24-hour processor-notification window is anchored to processor awareness or cross-references §6.3.
- Cross-corpus consistency: `supply-chain/standard-supplier-security-and-privacy-assurance.md` line 91 already cited GDPR Article 33(2) and "24 hours of awareness"; the privacy procedure now agrees with that framing.

### Discipline observation

The pattern this finding exposes is **timeline-asymmetry under-specification**: a regulation that ties two related clocks to different awareness events (Article 33(1) at controller awareness; Article 33(2) at processor awareness) is easy to under-document by stating each clock separately without explaining the asymmetry. A candidate generalisation for the corpus-management discipline (TODO P4.6): whenever a procedure describes more than one regulatory clock with different anchor events, an explicit asymmetry note is preferable to scattered per-clock anchoring statements. Not in scope for this PR; surfaced for future consideration.

---

## 2026-06-21, Library Version 2026.06.132, PR #150

Closes FR-45 (high, ⚠️ confirmed-with-modification). Two RFC 2119 normative-vocabulary fixes: "may not" → "must not be" in the password-history requirement and the BYOD-with-Confidential/Restricted-data prohibition.

### Closed findings

- **FR-45** (high, ⚠️, two files): "may not be reused" (password history) and "may not be used" (BYOD with Confidential/Restricted data) parsed as permissible-negative under a strict RFC 2119 reading, where the surrounding requirement-language context makes the intent unambiguously MUST NOT. Pass-1's ⚠️ modification correctly noted the strict-reading ambiguity; the remediation chooses each file's predominant normative verb ("must") rather than introducing "shall" alongside the dominant idiom.

### Changed

- [`security/standard-authentication-and-password-management.md`](../../security/standard-authentication-and-password-management.md):
  - §"Password requirements" table, `Password reuse` row: `Last 12 passwords may not be reused.` → `The last 12 passwords must not be reused.` (article inserted for grammaticality with the new normative verb).
  - Per-doc version `1.0.1 → 1.0.2`; Date `2026-05-27 → 2026-06-21`.
- [`security/standard-remote-working-security.md`](../../security/standard-remote-working-security.md):
  - §8.2 (Bring-your-own device): `Personal devices may not be used to access data classified as Confidential or Restricted...` → `Personal devices must not be used to access data classified as Confidential or Restricted...`.
  - Per-doc version `1.0.1 → 1.0.2`; Date `2026-05-28 → 2026-06-21`.
- [`README.md`](../../README.md): library `2026.06.131 → 2026.06.132`; README `1.9.2 → 1.9.3`.
- [`TODO.md`](../../TODO.md): FR-45 rotated out of High tier; backlog counters updated (15 + 14 + 56 = 85 immediate; 14 deferred; 99 open).
- [`.working/DONE.md`](../DONE.md): PR #150 entry added.

### Verification

- Corpus-wide grep for `may not` in `security/`: only the two cited lines existed pre-edit; zero occurrences post-edit (each file).
- Local audit: `tools/run_all_audits.sh` exits 0 on all gates post-commit.
- Local PR-time checks: `tools/run-pr-time-checks.sh` exits 0.
- Per-doc Version bumps mechanically required by gate D2; both bumped.
- Semantic check: the password-history row remains in the prohibitions column of the table by adjacency and reads as a complete imperative; the BYOD line preserves its existing carve-out ("without explicit written approval from the CISO and a documented compensating control") so the policy substance is unchanged.

### Discipline observation

This is a vocabulary-tightening fix, not a substantive policy change. The strict RFC 2119 reading that flagged "may not" as ambiguous is a useful audit signal even where the surrounding prose makes intent obvious to a human reader; machine-readable normative-verb auditing (e.g., a future lint that flags "may not" anywhere in a requirements document) would catch this class systematically. Surfaced for future consideration; not in scope for this PR.

---

## 2026-06-21, Library Version 2026.06.131, PR #149

Closes FR-21 (high[critical]). The compliance-obligations register template's Source Reference field is tightened to require full citation granularity so the register fulfils its audit-prep purpose.

### Closed findings

- **FR-21** (high[critical], `compliance/register-compliance-obligations-template.md`): Source Reference field accepted low-precision citations such as "NIST 800-53" or "ISO 27001" without revision/year/control granularity. An auditor reading the register could not resolve the obligation to a specific source location; populators following the prior description ("Specific law, regulation, clause, or standard section") could legitimately enter the standard name alone. The single in-table example was precise (`GDPR Article 32; Recital 83`) but the description did not require that precision, so the example acted as a hint rather than a constraint.

### Changed

- [`compliance/register-compliance-obligations-template.md`](../../compliance/register-compliance-obligations-template.md):
  - Source Reference description rewritten to require version (revision, year, or edition) AND specific provision (article, clause, control, sub-control). The in-table example tightened from `GDPR Article 32; Recital 83` to `GDPR Article 32(1)(b); Recital 83`.
  - New sub-section `#### Source Reference granularity requirements` added immediately under the Identification fields table. Single table listing minimum-granularity requirements per source type with acceptable and unacceptable example citations: NIST publications, ISO/IEC standards, statutes/regulations, COBIT, PCI DSS, CSA CCM, contracts, voluntary commitments.
  - Two trailing notes added: (1) multi-provision obligations list each provision separately; (2) drift in source versions is itself an obligation-management event triggering review under existing Ownership and monitoring fields.
  - Per-doc `1.0.2 → 1.0.3`; Date `2026-05-28 → 2026-06-21`.
- [`README.md`](../../README.md): library `2026.06.130 → 2026.06.131`; README `1.9.1 → 1.9.2`.
- [`TODO.md`](../../TODO.md): FR-21 rotated out of High[critical] tier. Backlog: 15 + 15 + 56 = 86 immediate-priority; 14 deferred; 100 open.
- [`.working/DONE.md`](../DONE.md): PR #149 entry + FR-21 cross-reference entry added.

### Verification

- All 46 audit gates pass; PR-time checks pass.
- Manual re-read: Identification fields table still has five rows; new sub-section sits between Identification fields and Applicability fields; all backtick-wrapped citation examples follow the code-span convention.
- First worker-subagent-prepared draft applied. QA review caught no issues; the draft's structure matched the orchestrator's expectations and was applied with placeholder substitutions only (PR number, library version, date).

---

## 2026-06-21, Library Version 2026.06.130, PR #148

Sweep 12 iteration 1 close-out. The first validation sweep since Sweep 11 iter 1 (PR #127); six fitness-remediation PRs landed in between (PRs #142-#147). Subagents A, B, C all dispatched per Rule 5.6 declaration.

### Sweep findings (3 in-window, all fixed)

- **(H) cross-doc-stale-cio-erm** (Subagents A and B, dedupe-confirmed): [`risk/policy-enterprise-governance-and-risk-management.md`](../../risk/policy-enterprise-governance-and-risk-management.md) still named "Chief Information Officer" as Owner and as accountable for the enterprise risk management framework in §3 governance table. PR #143 had updated the companion standard `risk/standard-enterprise-risk-management.md` to CRO but did not touch the policy. Fix: Owner field CIO → CRO; new CRO row added to §3 governance table positioned after AI Governance Council and before Chief Information Officer; CIO row reshaped from "Accountable for the enterprise risk management framework" to "Provides executive support to the ERM programme on technology-risk integration; ensures that IT-strategy risk is reflected in the enterprise risk register" — mirrors the parallel reshape PR #143 made in the standard. Per-doc `1.4.1 → 1.4.2`; Date `2026-05-28 → 2026-06-21`.

- **(M) missing-sampling-justification-link** (Subagent B): [`compliance/procedure-control-testing.md`](../../compliance/procedure-control-testing.md) §2.2 defined the three-tier sample-size methodology (High 25-40, Medium 15-25, Low 5-15) but did not point at the new "Sampling justification" field added to [`compliance/template-audit-evidence-package.md`](../../compliance/template-audit-evidence-package.md) in PR #144. Auditors reading the procedure had no pathway to discover the template's required field. Fix: paragraph added immediately after the sample-size bullet list, naming the template's §"Operating evidence" per-test field set and explaining that the audit-evidence-package surface is where the chosen sample size and selection method appear to external auditors. Per-doc `1.0.0 → 1.0.1`; Date `2026-05-27 → 2026-06-21`.

- **(L) missing-reciprocal-risk-acceptance-link** (Subagent B, rubric `K`): [`governance/policy-exception-and-risk-acceptance-management.md`](../../governance/policy-exception-and-risk-acceptance-management.md) §5 (Tracking and reporting) lacked a reciprocal "Related risk acceptance" field that pairs with the field PR #146 added to `risk/procedure-risk-acceptance.md`. The bidirectional asymmetry was acknowledged in PR #146's detailed CHANGELOG as a latent follow-up but never separately filed as an FR-N or TODO item; it would have continued to drift had this sweep not surfaced it. Fix: new §5.2 added that requires each exception register entry to record the ID of the related risk-acceptance record (or `None` if the exception is a policy/control deviation that did not produce a separate risk acceptance). Existing §§5.2 and 5.3 renumbered to 5.3 and 5.4 to accommodate. Per-doc `1.0.2 → 1.0.3`; Date `2026-05-27 → 2026-06-21`.

Subagent C zero findings: four-surface parity (46 gates), spec self-consistency, regression-test coverage, gate-39 cleanliness, gate-40 version-bump-recency, skill-and-command step parity all verified sound.

### Changed

- [`risk/policy-enterprise-governance-and-risk-management.md`](../../risk/policy-enterprise-governance-and-risk-management.md): Owner field; §3 governance table CRO row added, CIO row reshaped.
- [`compliance/procedure-control-testing.md`](../../compliance/procedure-control-testing.md): §2.2 cross-reference added.
- [`governance/policy-exception-and-risk-acceptance-management.md`](../../governance/policy-exception-and-risk-acceptance-management.md): new §5.2; original §5.2 and §5.3 renumbered.
- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md): new Sweep 12 iter 1 row at top; version `2.0.3 → 2.0.4`.
- [`.working/validate-sweeps/2026-06-21-sweep12-iter1.md`](../validate-sweeps/2026-06-21-sweep12-iter1.md): new per-iteration detail file with the six required H2 sections (trigger / Subagent A / Subagent B / Subagent C / Orchestrator synthesis / Resulting PR).
- [`README.md`](../../README.md): library `2026.06.129 → 2026.06.130`; README `1.9.0 → 1.9.1`.
- [`TODO.md`](../../TODO.md): session resume metadata refreshed; "Last validation sweep" cursor advanced to Sweep 12 iter 1.
- [`.working/DONE.md`](../DONE.md): PR #148 entry added at top.

### Verification

- Local audit: `tools/run_all_audits.sh` exits 0 on all 46 gates post-commit.
- Local PR-time checks: `tools/run-pr-time-checks.sh` exits 0.
- Three per-doc Version bumps mechanically required by gate D2 (Per-PR version-bump check); all bumped.

### Discipline observation

The cross-doc-stale-cio-erm finding illustrates a recurring failure-mode class that mechanical gates currently do not catch: **doctype-pair consistency drift**. Standard and Policy documents about the same subject (here: enterprise risk management) form a logical pair; an edit to one should typically cascade to the other. The audit programme has no gate that enforces this pairing. Pattern surfaces also in FR-43 (data classification: standard vs subordinate-doc subset), FR-47 (DPO role attribution across multiple privacy procedures), FR-13 (CPPA disambiguation needed in multiple framework-alignment tables). 

This pattern is a candidate for a future mechanical gate ("known doctype pairs must agree on Owner, governance, and key role-attribution fields") and for inclusion in the corpus-management-discipline shareable skill (TODO P4.6) under "Pair-aware doctype consistency". Not in scope for this sweep; surfaced for future consideration.

---

## 2026-06-21, Library Version 2026.06.129, PR #147

Closes FR-3 (high, newcomer-onboarding). The README gains a "New to GRC? Start here" section so first-time readers have an entry point before the §Purpose paragraph that previously assumed the reader knew the discipline.

### Closed findings

- **FR-3** (high, README): The title `Governance, Risk, and Compliance Documentation Library` carried the acronym `GRC` but the term was never expanded on the page. The §Purpose paragraph at line 14 onwards described what the library is (a CC BY-SA 4.0 reference set for building an organisation-neutral programme) but presupposed the reader knew what governance, risk, and compliance are as disciplines. A reader landing on the README with no prior exposure had no entry point.

### Changed

- [`README.md`](../../README.md): new top-level section `## New to GRC? Start here` inserted between the CalVer note and `## Purpose`. The section has three parts:
  1. Three-bullet plain-language definition of Governance, Risk, and Compliance (what each discipline does, with one example artefact-class each).
  2. A paragraph explaining why this library covers security, privacy, resilience, supplier/third-party governance, and AI governance as sibling domains under the GRC umbrella (organisations operate them together).
  3. Five intent-keyed "where to go next" pointers: first-time visitor / adopter / auditor / maintainer / glossary-lookup, each linking to the most relevant entry-point document.
- README per-doc version `1.8.84 → 1.9.0` (minor bump: new top-level section, not just a tweak).
- Library `2026.06.128 → 2026.06.129`.
- [`TODO.md`](../../TODO.md): FR-3 rotated out of High tier. Backlog: 16 + 15 + 56 = 87 immediate-priority; 14 deferred; 101 open.
- [`.working/DONE.md`](../DONE.md): PR #147 entry added.

### Verification

- All 46 audit gates pass; PR-time checks pass.
- Manual re-read: new section is positioned correctly (after metadata block + CalVer note, before §Purpose); GRC is expanded inline at the start of the section; all five "where to go next" links are valid repository paths.
- Markdown formatting: H2 heading uses sentence case (lowercase after first word), per the library's heading convention; bullets use the `**bold-name**: explanation` form consistent with other top-level READMEs.

### Discipline observation

This PR's value is asymmetric: small structural change in the README, large impact on newcomer onboarding. The §Purpose paragraph remains in place unchanged — the new section sits above it as an explicit on-ramp. Adopters who already know GRC can skim past this section; adopters new to the discipline now have the entry point that was missing.

The section also addresses an adjacent finding category (acronyms-without-expansion) at the most-visible surface: by expanding GRC and naming the sibling domains explicitly, several downstream "what does this term mean" questions are resolved before the reader hits them in subordinate docs.

---

## 2026-06-21, Library Version 2026.06.128, PR #146

Closes FR-96 (high, ⚠️ confirmed-with-modification). The risk-acceptance procedure now records its linkage to the exception register at schema level.

### Closed findings

- **FR-96** (high, ⚠️, `risk/procedure-risk-acceptance.md`): Acceptance record fields lacked an explicit cross-reference to the exception register. Pass-1 noted the modification: "the linkage is conceptual rather than schema-level." The cross-reference exists conceptually (an exception in `governance/policy-exception-and-risk-acceptance-management.md` typically pairs with a risk acceptance) but no field captured the bidirectional traceability. Audit traceability required.

### Changed

- [`risk/procedure-risk-acceptance.md`](../../risk/procedure-risk-acceptance.md):
  - "Required record fields" extended with `Related exception register entry: ID of the corresponding entry in the exception register if this acceptance derives from or relates to a documented policy / control exception (see governance/policy-exception-and-risk-acceptance-management.md); record None if the acceptance is a pure risk acceptance unrelated to a policy exception. This linkage makes the two registers cross-traversable: an auditor reviewing an exception can find the corresponding risk acceptance and vice versa.`
  - Per-doc version `1.0.0 → 1.0.1`; Date `2026-05-27 → 2026-06-21`.
- [`README.md`](../../README.md): library `2026.06.127 → 2026.06.128`; README `1.8.83 → 1.8.84`.
- [`TODO.md`](../../TODO.md): FR-96 rotated out. Backlog: 16 + 16 + 56 = 88 immediate; 14 deferred; 102 open.
- [`.working/DONE.md`](../DONE.md): PR #146 entry added.

### Verification

- All 46 audit gates pass; PR-time checks pass.
- Cross-reference check: the bidirectional traceability now has a schema-level field; `governance/policy-exception-and-risk-acceptance-management.md` should also gain a reciprocal "Related risk acceptance" field for full traceability, but that's a separate finding outside the current FR-96 scope (could be filed as a small follow-up if not already covered by other backlog items).

---

## 2026-06-21, Library Version 2026.06.127, PR #145

Closes FR-95 (high). The risk register template's Acceptance section gains a mandatory `Compensating Controls` field so each acceptance record is self-contained and auditable.

### Closed findings

- **FR-95** (high, `risk/template-enterprise-risk-register.md`): the Acceptance section captured rationale, conditions, and expiry but lacked a compensating-controls field. `risk/procedure-risk-acceptance.md` §5 already requires compensating-controls analysis as part of acceptance; the template's omission meant the analysis could be performed but not recorded in the register row, requiring an auditor to reconstruct the linkage from the acceptance-record artefact each time.

### Changed

- [`risk/template-enterprise-risk-register.md`](../../risk/template-enterprise-risk-register.md):
  - Acceptance section field-table extended with a new `Compensating Controls` row positioned between `Acceptance Conditions` and `Accepted By`. Description: "Controls in place that reduce residual risk to the level being accepted; list each by control ID with a brief note on how it offsets the un-treated risk. Required by `risk/procedure-risk-acceptance.md` §5; recorded here so the acceptance record is self-contained and auditable."
  - Per-doc version `1.0.1 → 1.0.2`; Date `2026-05-28 → 2026-06-21`.
- [`README.md`](../../README.md): library `2026.06.126 → 2026.06.127`; README `1.8.82 → 1.8.83`.
- [`TODO.md`](../../TODO.md): FR-95 rotated out. Backlog: 16 + 17 + 56 = 89 immediate; 14 deferred; 103 open.
- [`.working/DONE.md`](../DONE.md): PR #145 entry added.

### Verification

- All 46 audit gates pass; PR-time checks pass.
- Cross-reference check: `procedure-risk-acceptance.md` §5 already specifies compensating-controls requirement; the template now mirrors that requirement at the schema level.

---

## 2026-06-21, Library Version 2026.06.126, PR #144

Closes FR-22 (high). The audit-evidence template gains a mandatory sampling-justification field so external auditors see the statistical-basis justification for every sample without reconstructing it from peer documents.

### Closed findings

- **FR-22** (high, `compliance/template-audit-evidence-package.md`): Template lacked a mandatory sampling-justification field. External auditors require statistical-basis justification for sample sizes; `procedure-control-testing.md` §2.2 defines ranges (25-40 for high-risk controls) but the evidence template didn't surface that justification to the auditor reviewing the package.

### Changed

- [`compliance/template-audit-evidence-package.md`](../../compliance/template-audit-evidence-package.md):
  - Test 1 example (Quarterly access review) extended with `Sampling justification` as a mandatory field. The field's prompt asks for: statistical or judgemental basis; cite `procedure-control-testing.md` sample-size table (e.g. "25-40 for high-risk per §2.2") or document the rationale for a different size; state population size, sample size, selection method (random / stratified / judgemental), and confidence-level assumption if statistical; "100% population review" is the explicit response when the test covers the entire population.
  - Test 2 example (Annual policy review) extended with `Sampling justification: "100% population review" for single-artefact controls like policy reviews; otherwise as above.` Demonstrates the "non-sampling" response for single-artefact tests.
  - Per-doc version `1.0.0 → 1.0.1`; Date `2026-06-20 → 2026-06-21`.
- [`README.md`](../../README.md): library version `2026.06.125 → 2026.06.126`; README version `1.8.81 → 1.8.82`.
- [`TODO.md`](../../TODO.md): FR-22 rotated out of High tier. Backlog totals: 16 + 18 + 56 = 90 immediate-priority; 14 deferred; 104 open. Session resume metadata refreshed.
- [`.working/DONE.md`](../DONE.md): PR #144 entry added at top of "Closed items".

### Verification

- Local audit: `tools/run_all_audits.sh` exits 0 on all 46 gates.
- Local PR-time checks: `tools/run-pr-time-checks.sh` exits 0.
- Manual re-read: both test-example entries in the template now carry the `Sampling justification` field; cross-reference to `procedure-control-testing.md` §2.2 sample-size table is link-correct.

### Discipline observation

This is the second steady-state fitness-remediation PR (single FR-N, single-file edit, small focused PR). The amendment adds a mandatory field rather than restructuring the template — the template's existing per-control structure remains intact; only the field set per-test grows by one. Adopters using the template prior to this change continue to satisfy the new field by adding it during their next regular cycle; no migration is required.

---

## 2026-06-21, Library Version 2026.06.125, PR #143

Closes FR-9 (high[critical]) and FR-10 (high), bundled because both relate to Chief Risk Officer presence in [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md). One file, two structural fixes, single per-doc bump.

### Closed findings

- **FR-9** (high[critical]): the standard's `Owner` field was "Chief Information Officer". Enterprise risk is a CRO/CFO/Board accountability in most operating models; CIO ownership of the ERM standard read as a category error. Resolved to **Chief Risk Officer** per the finding text's first-listed alternative and consistent with FR-10's parallel call.
- **FR-10** (high): §3 Governance table omitted CRO entirely despite CRO being a defined role in the role-authority register and referenced in `procedure-risk-register.md`. Added a CRO row at the top of the table scoped to risk strategy, risk appetite stewardship, ERM programme outcomes, and Board / Risk Committee reporting.

### Changed

- [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md):
  - `Owner` field: `Chief Information Officer` → `Chief Risk Officer`.
  - §3 Governance table: new CRO row added at the top with responsibility scoped to risk strategy, risk-appetite stewardship, ERM-programme outcomes, Board / Risk Committee reporting.
  - §3 Governance table: pre-existing CIO row reshaped from "Accountable for the overall enterprise risk management framework" to "Provides executive support to the ERM programme on technology-risk integration; ensures that IT-strategy risk is reflected in the enterprise risk register". This reshape preserves CIO's technology-risk role without conflicting with CRO's new ERM-framework accountability.
  - Per-doc version `1.3.3 → 1.3.4`; Date `2026-06-21` (unchanged within the same day's batch).
- [`README.md`](../../README.md): library version `2026.06.124 → 2026.06.125`; README version `1.8.80 → 1.8.81`.
- [`TODO.md`](../../TODO.md): FR-9 rotated out of High[critical] tier; FR-10 rotated out of High tier. Backlog totals: 16 + 19 + 56 = 91 immediate-priority; 14 deferred; 105 open. Session resume metadata refreshed.
- [`.working/DONE.md`](../DONE.md): PR #143 entry + FR-9 and FR-10 cross-reference entries added at top of "Closed items".

### Verification

- Local audit: `tools/run_all_audits.sh` exits 0 on all 46 gates.
- Local PR-time checks: `tools/run-pr-time-checks.sh` exits 0.
- Manual re-read: ERM standard's Owner field shows "Chief Risk Officer"; §3 Governance table shows CRO row first followed by the reshaped CIO row.
- Cross-reference check: `procedure-risk-register.md` and `register-role-authority.md` already mention CRO; this PR makes the ERM standard consistent with those without introducing new content elsewhere.

### Discipline observation

Bundling FR-9 and FR-10 in one PR matches the "more PRs, keep each one clean" preference's exception: when two findings affect the same file and the same logical concept, splitting them into separate PRs creates artificial separation. The CRO addition is one structural fix that closes two findings; splitting would have required two per-doc version bumps in adjacent PRs with the second touching the same governance table the first just edited.

---

## 2026-06-21, Library Version 2026.06.124, PR #142

First fitness-remediation PR. Closes four unambiguous quick-win findings at maintainer direction ("pick some quick wins that are absolutely certainly in need of working and proceed with those") while the maintainer reviews the broader 111-item backlog. Each finding had: single-file scope; unambiguous fix (no judgement call); high value-per-effort; no cross-cutting impact.

### Closed findings

- **FR-13** (Medium, ERM standard): `CPPA` in [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md) §10 framework alignment table was ambiguous between the Canadian Consumer Privacy Protection Act (Bill C-27) and the California Privacy Protection Agency. The surrounding row "As applicable to Canadian personal information" made the intent clear in context but the acronym still required reader inference. Expanded to `CPPA (Canadian Consumer Privacy Protection Act, Bill C-27)`. Per-doc `1.3.2 → 1.3.3`; Date `2026-05-28 → 2026-06-21`.
- **FR-54** (Low, naming) and **FR-55** (Low, naming): `sop-` and `roadmap-` doctype prefixes are used in filenames and `SOP` / `Roadmap` are allowed doctypes in [`specification-master-project.md`](../../specification-master-project.md) §4.3, but the prefix-to-type mapping was only documented in a single sentence in `specification-ingestion.md:196`. Added an explicit prefix-mapping table to §4.3 listing all 17 doctypes and their canonical lowercase prefixes (`charter-`, `framework-`, `policy-`, `standard-`, `procedure-`, `sop-`, `plan-`, `roadmap-`, `guideline-`, `guide-`, `register-`, `matrix-`, `specification-`, `template-`, `annex-`, `checklist-`, `worklist-`). Per-doc `1.5.1 → 1.5.2`; Date `2026-06-19 → 2026-06-21`. The new table also closes a class of latent finding: any future doctype addition now requires an explicit prefix entry rather than relying on inferred convention.
- **FR-103** (Low, 3LoD): the "Governance and accountability" table in [`governance/framework-continuous-assurance-and-improvement.md`](../../governance/framework-continuous-assurance-and-improvement.md) omitted Chief Compliance Officer despite CCO being relevant to compliance-domain assurance closure (referenced in the exception-policy closure-validation requirement). Added a CCO row scoped to compliance-domain assurance outcomes, closure validation chairmanship, and assurance-calendar alignment with regulatory obligation cadence. Per-doc `1.0.1 → 1.0.2`; Date `2026-05-28 → 2026-06-21`.

### Changed

- [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md): §10 framework alignment row updated for CPPA; per-doc version + Date bumped.
- [`governance/framework-continuous-assurance-and-improvement.md`](../../governance/framework-continuous-assurance-and-improvement.md): new CCO row added in the Governance and accountability table; per-doc version + Date bumped.
- [`specification-master-project.md`](../../specification-master-project.md): §4.3 reshaped from a bullet list of doctype names to a two-column prefix-mapping table; per-doc version + Date bumped.
- [`README.md`](../../README.md): library version `2026.06.123 → 2026.06.124`; README version `1.8.79 → 1.8.80`.
- [`TODO.md`](../../TODO.md): four FR-IDs rotated out of the Fitness review backlog (FR-13 from Medium tier, FR-54 / FR-55 / FR-103 from Low tier). Backlog totals updated to 93 immediate-priority + 14 deferred = 107 open. Session resume metadata refreshed.
- [`.working/DONE.md`](../DONE.md): PR #142 entry + four `### FR-N` cross-reference entries added at top of "Closed items".

### Verification

- Local audit: `tools/run_all_audits.sh` exits 0 on all 46 gates.
- Local PR-time checks: `tools/run-pr-time-checks.sh` exits 0.
- Manual re-read: each of the four affected files contains the new content; ERM standard's §10 row now spells out CPPA; framework-continuous-assurance has a new CCO row; specification-master-project's §4.3 has the new mapping table.
- TODO backlog totals match: 17 + 20 + 56 + 14 = 107 (was 17 + 20 + 57 + 17 = 111 before PR #142).

### Discipline observation

This PR is the steady-state shape of fitness-remediation work: pick a coherent micro-batch (here, four findings unified by "unambiguous quick wins"), close them in one focused PR, rotate them out of TODO and into DONE. The "more PRs, keep each one clean" preference holds: four findings in one PR is reasonable when each fix is small and they share a common rationale (quick wins); a larger PR with a heterogeneous fix set would be harder to review.

The maintainer's "while I'm reviewing them all" instruction is also a worked example of the TODO-as-prioritization-surface discipline introduced in PR #141. The maintainer can review the structured backlog at their own cadence; the orchestrator picks unambiguous fixes to maintain forward momentum without preempting maintainer choices on judgement-bearing findings. The 107 remaining open findings continue to await maintainer direction.

---

## 2026-06-21, Library Version 2026.06.123, PR #141

Pass-2 of the fitness review per the discipline introduced in PR #139. Surfaced the four Pass-1 buckets to the maintainer via structured AskUserQuestion and processed the outcomes. **No remediation work begins until the maintainer reviews the backlog and directs the order**; this PR's sole deliverable is the prioritized TODO backlog plus the report-side documentation of Pass-2 decisions.

### Pass-2 outcomes (per maintainer triage)

- **✅ batch (91 confirmed-as-stated)**: accepted with severity-tier deferral. High[critical] / High / Medium tiers are immediate-priority backlog. Low tier deferred to a later routine cleanup cycle.
- **⚠️ batch (16 confirmed-with-modification)**: accepted with the orchestrator's inline modifications. Severity unchanged across all 16.
- **🤔 batch (2 ambiguous-needs-maintainer)**:
  - FR-14 (maturity-ladder fragmentation): resolved to ✅ with library-wide CMMI propagation plan. Scope: rename CMMI-canonical tiers in `docs/template-maturity-self-assessment.md`; replace 4-tier DTI variant in `governance/register-digital-trust-and-assurance-metrics.md`; baseline `governance/framework-governance-performance-and-improvement.md` (already CMMI). Forward-looking convention: candidate audit gate for maturity-tier vocabulary, OR documented standard in `governance/`.
  - FR-110 (subjective "forbidding for newcomers"): resolved to ✅ at Medium severity. README navigation flow warrants redesign to prioritize the decision-tree or audience-keyed portal over the document-index for newcomers.
- **❌ batch (2 rejected)**:
  - FR-43 reshape: original framing was a policy-vs-policy mismatch; actual issue is **5-level standard vs 4-level subordinate-doc subset**. Reshape kept at High[critical] because the underlying corpus inconsistency is real and load-bearing.
  - FR-53 reshape: original "every document carries both Classification and Confidentiality" claim was empirically false. Reshape as lighter-weight question: "evaluate whether to deprecate one of the two fields, or document the semantic distinction." Severity downgraded from Medium to Low.

Zero findings removed; both ❌ rejections led to reshape rather than removal.

### Added

- [`TODO.md`](../../TODO.md) "Fitness review backlog (from r1, Pass-2 confirmed in PR #141)" section. Contains: intro paragraph + status legend + severity-tier prioritization preamble; "Special: FR-14" subsection for the library-wide CMMI propagation plan; High[critical] tier (17 findings with brief 1-line summaries); High tier (20 findings with brief summaries); Medium tier (57 findings grouped by topical cluster with FR-ID lists); Low tier (17 deferred findings, cross-reference-only); backlog totals. ⚠️ entries flagged so the maintainer can recognize the modification framing during review.

### Changed

- [`.working/fitness-reviews/2026-06-21-r1.md`](../fitness-reviews/2026-06-21-r1.md):
  - §8.5 aggregate-counts line: `93 ✅ / 14 ⚠️` corrected to `91 ✅ / 16 ⚠️` (PR #140 narrative miscount).
  - §8.5 Pass-1 summary by bucket: count line corrected to `91` and `16`.
  - New §8.6 "Pass-2 Maintainer-Interactive Outcomes" appended after §8.5 documenting the bucket decisions, FR-14 propagation plan, FR-110 promotion, FR-43 reshape framing, FR-53 reshape + downgrade.
- [`TODO.md`](../../TODO.md):
  - "Next" PR item updated: previously "Fitness backlog Pass-2"; now "First fitness-remediation PR (maintainer-directed)" — maintainer reviews the backlog and selects work; no remediation begins until directed.
  - Session resume metadata refreshed (`2026.06.122 → 2026.06.123`).
- [`README.md`](../../README.md): library version `2026.06.122 → 2026.06.123`; README version `1.8.78 → 1.8.79`.
- [`.working/DONE.md`](../DONE.md): PR #141 entry added at top of "Closed items".

### Not changed (deliberately)

- Source corpus documents are untouched. PR #141 is purely the prioritization PR; no remediation work has begun. The 111 findings remain documented in r1.md §3; r1.md §8.5 carries the Pass-1 verdicts; r1.md §8.6 carries the Pass-2 outcomes; TODO carries the maintainer-reviewable backlog. Subsequent PRs will action specific FR-Ns at the maintainer's direction.

### Verification

- Local audit: `tools/run_all_audits.sh` exits 0 on all 46 gates.
- Local PR-time checks: `tools/run-pr-time-checks.sh` exits 0.
- Manual cross-reference: 17 + 20 + 57 + 17 = 111 FR-IDs accounted for in the TODO backlog grouping (verified by manual sum across the four severity tiers; the 17 deferred Low tier matches the 17 Low findings minus FR-53 reshape downgrade plus FR-53 reshape = same count).

### Discipline observation

This PR is the second steady-state application of the verify-then-act discipline introduced in PR #139 (Pass-1 was the first). The end-to-end exercise demonstrates that the discipline:

1. **Caught the synthesis-stage approximation** (PR #124's wrongly-counted findings) by mechanizing the count check at the Pass-1 verdict table.
2. **Caught the per-finding misframing failures** (FR-43 and FR-53) that would have driven misdirected remediation absent Pass-1 verification.
3. **Surfaced the maintainer's content-policy judgements** (FR-14 CMMI library-wide propagation) as Pass-2 outputs rather than treating them as orchestrator-resolvable.

The maintainer's directive ("review them all in TODO before working through them") is itself a meta-discipline that PR #141 honours: the deliverable is the structured backlog, not the remediation. Future fitness reviews can follow the same multi-PR rhythm: PR-N writes the report; PR-N+1 runs Pass-1; PR-N+2 runs Pass-2 and produces the TODO backlog; PR-N+3 onwards are individual remediation work at maintainer direction.

---

## 2026-06-21, Library Version 2026.06.122, PR #140

Applies Pass-1 verification (introduced in PR #139) retroactively against the existing 111 FR-N findings in [`.working/fitness-reviews/2026-06-21-r1.md`](../fitness-reviews/2026-06-21-r1.md). The Pass-1 protocol per PR #139: orchestrator re-reads each cited source location and applies one of four verdict tags. Five verification-task subagents dispatched in parallel handled the work; each was given a ~22-finding slice plus explicit instructions (direct file reads only, no persona role, single verdict per finding with brief inline note for non-`✅` verdicts).

### Aggregate Pass-1 results

| Verdict | Count | Examples |
|---|---|---|
| ✅ confirmed-as-stated | 93 | majority across all severity tiers |
| ⚠️ confirmed-with-modification | 14 | FR-8, FR-17, FR-23, FR-45, FR-51, FR-65, FR-68, FR-75, FR-76, FR-86, FR-96, FR-99, FR-101, FR-104, FR-109, FR-111 |
| 🤔 ambiguous-needs-maintainer | 2 | FR-14 (which maturity-ladder model), FR-110 (subjective "forbidding for newcomers") |
| ❌ rejected | 2 | FR-43 (inter-policy classification mismatch as framed — both policies use the same 4-level subset), FR-53 ("every document" claim — actually only 1 of ~410) |

The two rejected findings illustrate the failure mode this PR's discipline catches: FR-43's claim was framed as an inter-policy mismatch where both policies actually agree on a 4-level subset (the 5-vs-4 mismatch is between the 5-level *standard* and the 4-level *subset* used in subordinate docs — a real issue but not the policy-vs-policy mismatch the finding claimed); FR-53's "every document carries both" claim was false on direct inspection (only 1 of ~410 documents matches the pattern). Both findings would have produced misdirected remediation work absent verification.

### Changed

- [`.working/fitness-reviews/2026-06-21-r1.md`](../fitness-reviews/2026-06-21-r1.md):
  - New §8.5 "Pass-1 Verification Results" appended before the closing italic note. Section contains: introductory paragraph naming the four verdict tags + aggregate counts; full verdict table for FR-1 through FR-111; per-bucket summary identifying which FR-IDs fall into each non-`✅` bucket with inline modification notes.
  - §3 retroactive note rewritten to point at §8.5 rather than describe the unverified state.
  - Closing italic note extended to mention Pass-1 dispatch.
- [`README.md`](../../README.md): library version `2026.06.121 → 2026.06.122`; README version `1.8.77 → 1.8.78`.
- [`TODO.md`](../../TODO.md): the "fitness backlog Pass-1" item rotated to DONE; next queued is Pass-2 (maintainer-interactive bucket processing). Session resume metadata refreshed.
- [`.working/DONE.md`](../DONE.md): PR #140 entry added at top of "Closed items".

### Verification

- Local audit: `tools/run_all_audits.sh` exits 0 on all 46 gates.
- Local PR-time checks: `tools/run-pr-time-checks.sh` exits 0.
- Subagent outputs cross-checked: each batch's verdict tags integrated verbatim from the subagent's table; modification notes preserved.

### Discipline observation

This PR is the first end-to-end exercise of the Pass-1 protocol shipped in PR #139. Two structural observations:

1. **The discipline caught real failure modes.** FR-43 and FR-53 would have produced misdirected remediation if treated as confirmed without verification. FR-43 in particular would have driven work to reconcile two policies that already agree, missing the actual 5-vs-4 split surface (standard vs subordinate docs). The verification step turned a plausible-sounding finding into a specific corrected description.

2. **Subagent dispatch is the right shape for batch verification.** The SKILL.md prose said "orchestrator (not a subagent)" intending to exclude *persona* subagents (who would re-introduce interpretive lens). Verification-task subagents (direct reads, no persona role, single-verdict output) are qualitatively different and don't re-introduce the lens. The discipline should be amended to clarify this; queued as a small follow-up PR.

The 14 ⚠️ findings and 2 🤔 findings carry forward to Pass-2 with inline modification or open-question notes; the maintainer adjudicates each in the next PR's interactive cycle. The 93 ✅ findings carry forward to Pass-2 for batch confirmation. The 2 ❌ findings leave the backlog unless escalated.

---

## 2026-06-21, Library Version 2026.06.121, PR #139

Amends the `library-fitness-review` skill (`/fitness`) to introduce the unverified→confirmed labelling discipline. The amendment addresses the failure mode where synthesis-stage approximations propagate downstream as if confirmed (precedent: PR #124's `"95 unique findings, 18 H[critical] / 22 H / 31 M / 24 L"` framing, corrected to mechanical tabulation in PR #127; per-finding-content drift would be a worse instance of the same shape).

### Changed

- [`dev-security/claude-rules/skills/library-fitness-review/SKILL.md`](../../dev-security/claude-rules/skills/library-fitness-review/SKILL.md) Step 5 restructured from a single triage section into four sub-steps:
  - 5.1 Output the report with all findings marked `verification: unverified`.
  - 5.2 Pass-1, orchestrator verification: re-read each cited source location; apply one of four verdict tags (`✅ confirmed-as-stated`, `⚠️ confirmed-with-modification`, `❌ rejected`, `🤔 ambiguous-needs-maintainer`); update the report's `verification:` annotation in place.
  - 5.3 Pass-2, maintainer-interactive bucket processing: surface the four buckets to the maintainer; `✅` cluster gets a batch confirmation; `⚠️` cluster gets per-finding prompts with the orchestrator's recommended adjustment plus alternatives; `🤔` cluster gets per-finding prompts with the open question; `❌` cluster gets a batch presentation with optional per-finding escalation.
  - 5.4 Triage and severity-tier action for confirmed findings only. Rejected findings recorded in the report (with rationale) but excluded from the backlog. Confirmed findings produce TODO entries carrying `FR-<n>` ID + originating run reference + Pass-2 verification date.
- [`.claude/commands/fitness.md`](../../.claude/commands/fitness.md) step 5 rewritten to mirror the SKILL.md restructure (paired-skill step-parity gate 44 enforces alignment).
- [`.working/fitness-reviews/README.md`](../fitness-reviews/README.md) "Output flow per run" section extended from 9 steps to 11 steps. New steps 6 (Pass-1) and 7 (Pass-2) inserted; subsequent steps renumbered. Step 5 amended to note that synthesis is a dedupe-and-tagging pass, not a verification pass, and that all findings are written with `verification: unverified` at synthesis time.
- [`.working/fitness-reviews/2026-06-21-r1.md`](../fitness-reviews/2026-06-21-r1.md): a verification-status note added at the top of §3 (Page-by-Page Findings). The note retroactively marks all FR-1 through FR-111 findings as `verification: unverified`, pending Pass-1 in the next PR. The severity tags and persona provenance remain authoritative.
- [`dev-security/claude-rules/README.md`](../../dev-security/claude-rules/README.md): pack version `1.33.0 → 1.34.0`; version-history table row added describing the SKILL.md amendment.
- [`README.md`](../../README.md): library version `2026.06.120 → 2026.06.121`; README version `1.8.76 → 1.8.77`.
- [`TODO.md`](../../TODO.md): the "Fitness skill amendment" item rotated to DONE; the next queued PR becomes "Fitness backlog Pass-1 (orchestrator verification)". Session resume metadata refreshed.
- [`.working/DONE.md`](../DONE.md): PR #139 entry added at the top of "Closed items".

### Verification

- Local audit: `tools/run_all_audits.sh` exits 0 on all 46 gates. Gate 44 (paired-skill step-parity) confirms SKILL.md and the slash command remain in step alignment.
- Local PR-time checks: `tools/run-pr-time-checks.sh` exits 0.
- Manual cross-reference: every Pass-1 verdict tag (`✅ confirmed-as-stated`, `⚠️ confirmed-with-modification`, `❌ rejected`, `🤔 ambiguous-needs-maintainer`) appears identically in SKILL.md, the slash command, and `.working/fitness-reviews/README.md`. The four buckets and their Pass-2 handling appear identically across the three surfaces.

### Discipline observation

This amendment addresses the failure mode the orchestrator already exhibited once in production. PR #124's first-fitness-review wording carried a synthesis-stage approximation ("about 95 unique findings, 18 H[critical] / 22 H / 31 M / 24 L") that downstream surfaces (TODO, CHANGELOG, fitness history table) treated as authoritative for several PRs. PR #127 corrected the counts after Sweep 11 caught the mismatch. The Pass-1 orchestrator-verification step is the structural fix: by the time a count or finding becomes downstream-actionable, it has been re-read against the source. The discipline is the same one the `evidence-grounded-completion` pack rule encodes for assertions about artefacts; this PR applies it to fitness-review findings specifically.

The next PR runs Pass-1 against the existing 111 findings in `2026-06-21-r1.md`. Pass-2 runs after that with maintainer participation. After Pass-2, confirmed findings produce TODO entries that drive subsequent remediation PRs through the project's normal cadence.

---

## 2026-06-21, Library Version 2026.06.120, PR #138

Rotates the five shipped Priority 4 items (P4.1 through P4.5) from [`TODO.md`](../../TODO.md) into [`.working/DONE.md`](../DONE.md). Maintainer-surfaced during PR #131's work: TODO's P4.1 through P4.5 sections all carried `Shipped 2026-06-20 as ...` framing — they were completed work entries, not forward-looking backlog. The rotation finishes the TODO-content cleanup that began with the decisions-log migration in PR #135.

### Changed

- [`TODO.md`](../../TODO.md):
  - Priority 4 sections 4.1 through 4.5 (`Quickstart templates per adopter profile`, `Maturity assessment interactive template`, `Implementation roadmap templates`, `Regulator interaction templates`, `Audit evidence package templates`) removed from this file.
  - P4.6 (corpus-management discipline as a shareable skill) preserved verbatim; it remains forward-looking.
  - Sweep 4 follow-up historical note (`The Sweep 4 follow-up (classification-convention documentation) resolved within its own close-out ... and is no longer tracked here.`) removed from "Open follow-ups from validation sweeps". The note was already documenting that the item was resolved and not tracked; the meta-note about no-longer-tracking is itself stale and the section is clearer without it.
  - Queued-sequence "Shipped Priority 4 items rotation" item rotated out (this PR closes it). Fitness skill amendment becomes the new "Next".
  - Session resume metadata refreshed (`2026.06.119 → 2026.06.120`; sync after PR #138).
- [`.working/DONE.md`](../DONE.md): Six new entries at the top of "Closed items" — PR #138 (this PR) plus `### TODO P4.1` through `### TODO P4.5`, each carrying the same paragraph the TODO file used to carry but reframed as a closed-item entry under its original P-X.Y identifier. The reframing demonstrates the rotation discipline: closed items keep their original backlog ID for cross-reference while moving to the appropriate home.
- [`README.md`](../../README.md): library version `2026.06.119 → 2026.06.120`; README version `1.8.75 → 1.8.76`.

### Verification

- Local audit: `tools/run_all_audits.sh` exits 0 on all 46 gates.
- Local PR-time checks: `tools/run-pr-time-checks.sh` exits 0.
- Manual cross-reference: every P4.x section moved out of TODO has its corresponding entry in DONE with the same paragraph content (verified by reading both before and after the diff).

### Discipline observation

This is the second steady-state application of the TODO/DONE rotation discipline (the first being the AUTHORS update in PR #132). It also demonstrates the cross-reference convention: closed items rotated to DONE can carry their original backlog identifier (`P4.1`, `P4.2`, etc.) as the entry header, separately from the PR-number-keyed entry that closed them. The two-key convention (`### PR #N — ...` for the PR-level entry, `### TODO P-X.Y — ...` for the original backlog item) lets a future reader search by either dimension.

The pattern of multi-PR TODO cleanup (PR #131 created DONE infrastructure, PR #135 restructured design-decisions, PR #138 rotates the shipped P4 items) is the natural shape: each PR has its own focused scope, but the cumulative effect is a TODO that holds only forward-looking content. Future maintainers performing similar restructuring on adopter forks can use these three PRs as worked examples.

---

## 2026-06-21, Library Version 2026.06.119, PR #137

Implements the maintainer-confirmed overnight-work protocol. The protocol provides structured handoff for autonomous overnight sessions: the assistant fills a designated file with session state (authorization scope, design decisions, build progress, open ambiguities), and a new audit gate ensures the file is processed by the next-morning PR rather than left lingering.

### Added

- [`.working/overnight-pr.md`](../overnight-pr.md) (new, stub form): the overnight-work file. Carries `**Status:** stub` plus a description of the protocol. The file persists in stub form when no overnight session is in flight; the first overnight PR transitions it to `Status: in-flight`; the session's final commit transitions to `Status: done`; the next-morning processing PR resets to `stub`.
- [`tools/lint-overnight-file.py`](../../tools/lint-overnight-file.py) (new, ~90 lines, stdlib-only): gate 46. Scans the overnight file's `**Status:**` field. Exit codes: 0 on `stub` or `in-flight`; 1 on `done` (with a diagnostic explaining the morning-processing requirement); 1 on any other invalid Status value; 2 on missing file or missing Status line.
- [`tests/test_linters.py`](../../tests/test_linters.py): `OvernightFileTests` class with 6 tests: smoke (corpus at HEAD in stub form), regex matches for each valid Status value (stub, in-flight, done), and structural tests confirming the pass/fail sets are correctly partitioned.

### Changed

- [`.github/workflows/quality.yml`](../../.github/workflows/quality.yml): new step `Overnight-work file audit` appended after `TODO staleness audit`.
- [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh): new `run_gate "Overnight-work file audit"` invocation appended after the TODO staleness gate.
- [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml): new hook `lint-overnight-file` appended after the TODO staleness hook.
- [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md):
  - §6 inventory table extended with row 46.
  - §5 category 7 (Freshness and lifecycle) gains gate 46 with rationale referencing the overnight-work protocol and explaining the three-value Status field.
  - New paragraph describing gate 46's behaviour and the design rationale (three-state Status rather than binary stub-vs-content) appended after gate 45's description.
  - Version `1.13.1 → 1.14.0`. The MINOR bump reflects the new gate row.
- [`dev-security/claude-rules/governance/change-tracking.md`](../../dev-security/claude-rules/governance/change-tracking.md): new "Overnight-work protocol" subsection added under "PR finalization protocol" (after the "Anti-patterns" subsection). Documents the file's lifecycle, the three Status values, the morning-processing PR, the stub-form contents, the initial overnight commit, the final overnight commit, and the exception path. Project-agnostic; adopters supply the overnight-file location.
- [`.claude/rules/governance/change-tracking.md`](../../.claude/rules/governance/change-tracking.md): mirrored from the pack source per the claude-rules sync convention.
- [`dev-security/claude-rules/README.md`](../../dev-security/claude-rules/README.md): pack version `1.32.0 → 1.33.0`; version-history row added.
- [`README.md`](../../README.md): library version `2026.06.118 → 2026.06.119`; README version `1.8.74 → 1.8.75`.
- [`TODO.md`](../../TODO.md): overnight-protocol item rotated out of the queued sequence (closed by this PR); session resume metadata refreshed; shipped-P4-items rotation becomes the new "Next" PR; fitness work shifts forward.
- [`.working/DONE.md`](../DONE.md): PR #137 entry added at the top of "Closed items".

### Verification

- Local audit: `tools/run_all_audits.sh` exits 0 on all gates including the new gate 46 against the stub file.
- Local PR-time checks: `tools/run-pr-time-checks.sh` exits 0.
- Regression suite: `python3 tools/run-linter-regression.py` includes the 6 new OvernightFileTests; all pass.
- Gate-name parity (gate 35) confirms the new gate appears identically in the §6 inventory, the workflow, the runner, and the pre-commit config.

### Discipline observation

The three-state design (rather than the binary stub-vs-non-stub that the user's original proposal sketched and I initially advocated) was the resolution of a tension I surfaced before building: a pure binary gate would have blocked overnight PRs from landing through CI, breaking the overnight workflow itself. The three-state Status field threads the needle — the gate provides the morning-processing pressure exactly when needed (after session end) while letting overnight PRs land cleanly while the session is in flight.

The maintainer's pattern of surfacing a structural standard ("add this gate") and the assistant's pattern of building it with attention to workflow constraints ("this design tension exists; here's the resolution") is itself one of the patterns that the future corpus-management-discipline shareable skill (TODO P4.6) will want to capture.

---

## 2026-06-21, Library Version 2026.06.118, PR #135

Restructures the working-state ledgers per the maintainer's directive that "DONE should be for things that are DONE; we have the .working directory for our work, let's be as organized as we can moving forward." Three concerns combined:

1. Design-decision content rotated out of DONE.md into its own file [`.working/design-decisions.md`](../design-decisions.md). DONE.md is now strictly closed-TODO items.
2. `.working/overnight-pr.md` deleted. Substantive content (fitness-skill design decisions) migrated to design-decisions.md; procedural content (authorization scope, build progress checklist, files-touched lists, morning-review handoff notes) had no forward-looking value.
3. TODO's "Decisions log" section migrated to design-decisions.md as "Decisions explicitly dropped". TODO is now strictly forward-looking.

The maintainer also confirmed the next-PR adoption of an overnight-pr.md stub format plus audit gate; that work is queued as PR #136 in the new TODO queued sequence.

### Added

- [`.working/design-decisions.md`](../design-decisions.md) (new, ~200 lines): reference log of design decisions organized thematically. Sections: "Working state and `.working/` convention" (six decisions: `.working/` top-level, canonical activity layout, template-vs-application, fork guidance, top-level-files-vs-activities); "Slash commands, skills, and the validation-sweep / fitness-review surface" (eight decisions including the full 10-persona model with the EXCLUDED list, severity, output structure, cadence triggers, scope boundaries); "CHANGELOG and TODO/DONE conventions" (five decisions including PR sequencing, CHANGELOG split, dual-entry, snapshot framing, TODO/DONE rotation, after-merge list-next-5-PRs); "Audit programme architecture" (three decisions: Rule 5.6 silent-skip prevention, wrapper-script-plus-corpus-runner, decorative-gate-counts-forbidden); "Language and style" (Canadian-first convention); "Decisions explicitly dropped" (four decisions migrated from TODO's decisions log: strict-Related-Documents-reciprocity, cross-document-numerical-coherence-as-scaffold, phase-completion-gating-via-full-sweep, no-verification-of-standard-content-versus-library-interpretation).

### Removed

- [`.working/overnight-pr.md`](../overnight-pr.md) (deleted): the file documented PR #120's overnight authoring session. Its substantive design-decisions content has been migrated to [`design-decisions.md`](../design-decisions.md) (the persona model with EXCLUDED list, severity, output structure, cadence triggers, scope boundaries). The remaining content (authorization scope from the one-off message, files-being-authored work plan, files-NOT-touched scope confirmation, build-progress checklist, morning-review handoff notes, files-this-overnight-touched, corpus-boundary-respected confirmation) is procedural detail about a specific event with no forward-looking value. If a similar overnight session ever happens, a fresh scope-authorization file would be written from the maintainer's then-current instruction. The future overnight-pr.md stub format (queued as PR #136) will document the standard.

### Changed

- [`.working/DONE.md`](../DONE.md):
  - Preamble extended with a three-bullet enumeration of the working-state ledgers: CHANGELOG (by PR), design-decisions.md (thematic), DONE (by closed item).
  - Entire "Design decisions made (rotated from TODO 2026-06-21 as part of DONE infrastructure)" section removed (~70 lines).
  - PR #135 entry added at the top of "Closed items".
- [`.working/README.md`](../README.md): Top-level files table extended with the new `design-decisions.md` row. The table now lists DONE.md (PR #131) and design-decisions.md (PR #135).
- [`TODO.md`](../../TODO.md):
  - Top-of-file blurb updated to reference DONE.md AND design-decisions.md as the destinations for completed work and design decisions.
  - Queued sequence updated: previously-stale "TODO content cleanup" item rewritten as the overnight-protocol-with-stub-and-gate PR #136 (per maintainer's just-confirmed stub-with-gate approach), plus a new "Shipped Priority 4 items rotation" item as PR #137 (split off from the previous TODO content cleanup scope because P4.1-4.5 rotation was not in the design-decisions restructure scope of this PR), with fitness work continuing at PR #138.
  - "Decisions log" section deleted entirely (content migrated to design-decisions.md). A brief one-line pointer was considered but discarded in favor of the cleaner "completed migration" framing.
  - "Notes on maintenance" rewritten: now says "delete from this file (no strikethroughs) and add an entry to DONE.md in the same PR" instead of the older "remove and record in CHANGELOG.md" framing. New bullet added about design decisions going to design-decisions.md.
  - Session resume metadata refreshed (`2026.06.117 → 2026.06.118`; sync after PR #135).
- [`README.md`](../../README.md): library version `2026.06.117 → 2026.06.118`; README version `1.8.73 → 1.8.74`.

### Verification

- Local audit: `tools/run_all_audits.sh` exits 0 on all gates.
- Local PR-time checks: `tools/run-pr-time-checks.sh` exits 0.
- Manual cross-reference check: every design decision listed in DONE before this PR was migrated to design-decisions.md (verified by grep of section headings); every fitness-specific decision in overnight-pr.md was migrated (verified by reading the deleted file's content against design-decisions.md's "Slash commands, skills, and the validation-sweep / fitness-review surface" section); every decision in TODO's decisions log was migrated (verified by reading the deleted section against design-decisions.md's "Decisions explicitly dropped" section).
- Working-state ledger triad now has three roles: CHANGELOG (file changes per PR), DONE (closed-TODO items per PR), design-decisions (thematic decision rationale).

### Discipline observation

This PR's surface is structural rather than content-creating: no new corpus content, no linter behaviour change, no new gate. The structural fix matters because: the working-state ledgers were drifting toward overlap (design decisions in DONE; procedural log in overnight-pr.md; decisions log in TODO). The maintainer surfaced the misplacement explicitly ("DONE should be for things that are DONE"); this PR realigns the three files to their distinct roles.

The maintainer's broader pattern of surfacing "we should organize this better" mid-work and the assistant's pattern of routing the surfaced concerns into a focused PR is itself the corpus-management discipline the project has been accumulating. The future "corpus-management discipline as a shareable skill" (TODO P4.6) will want to capture this routing pattern as a structured workflow: when a working-state file shows symptoms of role drift (mixed-purpose content, redundant entries, gradually accumulating procedural debris), the assistant proposes a restructure PR rather than waiting for the maintainer to spot it.

---

## 2026-06-21, Library Version 2026.06.117, PR #134

Gate 45 (TODO staleness audit) regex tightened to eliminate a false positive that took down the post-PR-#133 merge `push`-event CI run on `main`. The earlier regex used an `[^\n]{0,80}` window between "next/queued/pending/upcoming" markers and `PR #<digit>`, which matched too broadly: any digit-bearing PR ref within 80 characters would trigger the queued-PR-already-merged finding, even when the queued PR was actually a placeholder (`PR #N`) and the digit-bearing reference was an unrelated historical parenthetical aside.

### Fixed

- [`tools/lint-todo-staleness.py`](../../tools/lint-todo-staleness.py): `QUEUED_PR_PATTERN` regex updated:
  - Before: `r"\b(?:next|queued|pending|upcoming)\b[^\n]{0,80}PR\s*#(\d+)"`
  - After: `r"\b(?:next|queued|pending|upcoming)\b[\s,:—–-]*PR\s*#(\d+)"`
  - The new character class `[\s,:—–-]*` allows only whitespace, commas, colons, hyphens, en-dashes, and em-dashes between the marker and the digit-bearing PR ref. Word characters and parentheses are excluded, so the queued PR must be the immediately-following PR target.
- Inline regex-source comment block rewritten to explain the tightening rationale and the specific false-positive shape that motivated it.

### Verification

- The TODO.md line that took down PR #133's post-merge run (`**Next, PR #N: TODO content cleanup.** Maintainer-surfaced (2026-06-21, during PR #133):`) no longer matches:
  - "Next" + ", " + "PR #N" → "N" not a digit → no match at the queued-PR target.
  - "Next" + " (60+ chars including word characters and parentheses) " + "PR #133" → word characters between are NOT in the new character class → no match.
- Real-drift cases continue to match. Smoke test verifies `Next, PR #128`, `Next — PR #128`, and `queued PR #128` shapes (the regression suite's positive tests).
- Local audit: `tools/run_all_audits.sh` exits 0 on all 45 gates.
- Local PR-time checks: `tools/run-pr-time-checks.sh` exits 0.
- Regression suite (`python3 tools/run-linter-regression.py`): all 110 tests pass.

### Changed

- [`README.md`](../../README.md): library `2026.06.116 → 2026.06.117`; README `1.8.72 → 1.8.73`.

### Discipline observation

This is gate 45's second production catch and the second post-merge-`main` failure since gate 45 shipped (PR #128). The first catch (PR #128's own merge) was a genuine queued-PR-merged drift in TODO; this catch was a false positive caused by the regex being too permissive.

The pattern across the two events: gate 45's regex was designed against a small set of training-input shapes (the TODO drift cases from sweeps 10-11) and didn't anticipate the parenthetical-historical-reference shape that the post-PR-#131 TODO-rotation discipline made common (every queued item's description now references the PR that surfaced it). The fix is to tighten the regex to match only the structural queued-PR target, not any digit-bearing PR ref within proximity.

The broader lesson: regex-based gates with permissive proximity matching catch real cases AND false positives in roughly the same proportion. The remediation is conservative regex (require structural adjacency) plus documentation of the rationale so future maintainers don't loosen the regex back when they encounter a missed real-drift case. Each loosening should add a specific test fixture for the case it accommodates.

---

## 2026-06-21, Library Version 2026.06.116, PR #133

Documents the project's language convention as **Canadian English first, Commonwealth (UK / Australian) English second, other dialects last**. Maintainer surfaced the framing mid-PR-#131: the `-ize` forms the linter enforces are the Canadian-orthography manifestation of the convention (Canadian English adopted the Oxford `-ize` convention; the orthography is shared with American English but the dialect attribution is Canadian). The linter's behaviour is unchanged; only the rationale narrative is reframed across three surfaces.

### Changed

- [`tools/lint-language.py`](../../tools/lint-language.py) module docstring:
  - Opening narrative paragraph added (before the existing "Checks for:" list) naming the convention as Canadian-first, Commonwealth-second, other-dialects-last, with a note that Canadian shares `-ize` with American via the Oxford convention.
  - "British `-ise` endings (use `-ize` / `-ization`; `ISE_PATTERN` enumerates the word list)." → "Commonwealth `-ise` endings used where Canadian `-ize` is preferred (`ISE_PATTERN` enumerates the word list; the rule is the Canadian-orthography form, not a generic American mandate)."
  - "Sanitisation-table source terms" → "Sanitization-table source terms" (Canadian spelling applied to the project's own docstring; the term `SANITISATION_TERMS` itself is a code identifier and is unchanged).
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) Conventions section: new "Language convention" subsection after the existing Conventions bullets. Names the convention as Canadian-first; explains the orthographic relationship with American English; restates the em-dash / en-dash prohibition for completeness.
- [`CONTRIBUTING.md`](../../CONTRIBUTING.md) Style requirements section:
  - New leading bullet stating the convention: `**Language convention: Canadian English first, Commonwealth (UK / Australian) second, other dialects last.**` followed by the same orthographic explanation.
  - Original `Use Oxford English with -ize forms` bullet rewritten to `Use -ize forms (e.g. organize, prioritize, recognize) per the Canadian-orthography rule above.` This avoids the dual misattribution (the prior text said "Oxford English" which is a UK-publishing-house convention; the actual Canadian rule is "Canadian English shares the Oxford `-ize` convention with American English" — different rationale).
  - Em-dash prohibition extended from `No em dashes or en dashes` to `No em dashes or en dashes; use commas, colons, or parentheses` (explicit replacement guidance; matches the linter's `replace with hyphen, colon, or parentheses` framing).
  - `capitalised` (Commonwealth `-ised` form) replaced with `capitalized` in two places, applying the Canadian-orthography rule to the document itself.
  - Per-document version `1.1.0 → 1.2.0`; Date `2026-06-19 → 2026-06-21`.
- [`README.md`](../../README.md): library version `2026.06.115 → 2026.06.116`; README version `1.8.71 → 1.8.72`.
- [`TODO.md`](../../TODO.md): the Canadian-language-convention item rotated to DONE in the same commit. New "TODO content cleanup" item queued as the new "Next" (rotation of decisions log + shipped P4.1-4.5 items to DONE per the maintainer's just-surfaced directive). Session resume metadata refreshed.
- [`.working/DONE.md`](../DONE.md): PR #133 entry added at the top of "Closed items".

### Not changed (deliberately)

- `tools/lint-language.py`'s `ISE_PATTERN` word list is unchanged. The Canadian-orthography rule produces the same set of disallowed forms as the prior framing.
- `SANITISATION_TERMS` (the code identifier and variable name) and `SANITISATION` references in other linters / specs are unchanged. Code identifiers are not corpus prose; renaming them is a separate, larger refactor with its own gate-39 / gate-37 / dependency cascade. The docstring usage of the word "sanitization" (Canadian form) is what changes here.
- Pack-side analogue (a `governance/language-convention.md` rule, or an existing rule's Tool-specific subsection) was considered and deferred. The convention is project-specific; adopters who fork the library and want a different convention can change `ISE_PATTERN` locally. If the future "corpus-management discipline as a shareable skill" (TODO P4.6) ships, it can name "configurable language convention" as a parameter; not in scope here.

### Verification

- Local audit: `tools/run_all_audits.sh` exits 0 on all gates after the edits.
- Local PR-time checks: `tools/run-pr-time-checks.sh` exits 0.
- Linter behaviour verification: `python3 tools/lint-language.py` exits 0 on the current corpus, confirming the docstring change did not introduce a behavioural drift.

### Discipline observation

The mis-attribution surfaced because the prior framing (`"British -ise endings"`) was a plausible-but-incorrect rationale. The linter's behaviour was correct; only the explanation was wrong. The pattern is worth noting: linter docstrings carry rationale, and rationale can be wrong even when behaviour is right. Audit gates verify behaviour, not rationale. The discipline this PR exercises is the rationale-side equivalent of the gate-discipline rule: when the rationale is wrong, fix the rationale, not the behaviour.

The maintainer's surfacing of this convention also reveals a broader pattern: the project has accumulated several behavioural conventions (em-dash prohibition, ensure-with-that, sentence-case headings, etc.) whose rationale was previously implicit or under-documented. The language-convention reframing here is the first explicit "what dialect does the project speak?" statement. If/when the corpus-management-discipline-shareable-skill PR (TODO P4.6) ships, this is exactly the kind of convention that needs a configurable parameter rather than a hard-coded rule.

---

## 2026-06-21, Library Version 2026.06.115, PR #132

Adds [Ryk Edelstein](https://github.com/fedelst) to the Acknowledged contributors list in [`AUTHORS.md`](../../AUTHORS.md). Maintainer-requested in the chat thread during PR #131's work. Small focused PR per the "more PRs, keep each one clean" preference. First PR exercising the post-PR-#131 steady-state TODO/DONE rotation discipline: the AUTHORS-update item that was queued as the "next PR" in TODO when PR #131 merged is removed from TODO and added to [`.working/DONE.md`](../DONE.md) in the same commit. Also a one-time bootstrap correction: PR #131 itself is added to DONE retroactively, since PR #131 created the DONE file but did not include its own entry (the bootstrap chicken-and-egg).

### Changed

- [`AUTHORS.md`](../../AUTHORS.md): Acknowledged contributors list extended with one new entry: `- **Ryk Edelstein** ([@fedelst](https://github.com/fedelst))`. Per-document version `1.1.0 → 1.1.1`; Date `2026-06-19 → 2026-06-21`.
- [`README.md`](../../README.md): library version `2026.06.114 → 2026.06.115`; README version `1.8.70 → 1.8.71`.
- [`TODO.md`](../../TODO.md): "AUTHORS.md" item removed from Queued sequence (rotated to DONE); language-convention item now the new "Next" PR (queued by the maintainer during the same chat thread); Session resume metadata refreshed (`2026.06.114 → 2026.06.115`; branch synced after PR #132).
- [`.working/DONE.md`](../DONE.md): two new entries at the top of the "Closed items" section — PR #132 (this PR) and PR #131 (the bootstrap correction noted above).

### Discipline observation

This PR is the first steady-state application of the rotation discipline established in PR #131. The full cycle:

1. Maintainer requested the AUTHORS edit mid-PR-#131. The new item was added to TODO's Queued sequence before PR #131 merged (per the "new items added to TODO before list is published" discipline).
2. PR #131 merged. The assistant listed the upcoming next 5 PRs from TODO, starting with this AUTHORS update.
3. PR #132 makes the AUTHORS edit AND removes the corresponding TODO item AND adds the DONE entry in the same commit. All three edits ship together.
4. Future readers asking "did PR #132 ship the AUTHORS update?" can look at DONE; "what does PR #132 contain in detail?" can look at the CHANGELOG; "is the AUTHORS update still queued?" can look at TODO and confirm it isn't.

The bootstrap correction is a one-time event: PR #131 ships the DONE.md file, so PR #131 cannot add its own entry in the same commit (chicken-and-egg). PR #132 corrects this retroactively. From PR #132 onward every PR adds its own entry.

The language-convention item (Canadian-first spelling) is now queued as the next PR. It surfaced during this PR's work when the maintainer clarified that the project's `-ized` form is Canadian (which shares with American) rather than American-only — the [`tools/lint-language.py`](../../tools/lint-language.py) module docstring's framing of the rule as `"British -ise endings (use -ize / -ization)"` mis-attributes the convention's origin. The fix is doc-only (the linter's behaviour is correct); scope captured in the TODO entry.

---

## 2026-06-21, Library Version 2026.06.114, PR #131

Introduces [`.working/DONE.md`](../DONE.md), the closed-TODO ledger; refactors [`TODO.md`](../../TODO.md) to be forward-looking only by rotating all historical content into DONE; amends the [`change-tracking.md`](../../dev-security/claude-rules/governance/change-tracking.md) pack rule with a "PR finalization protocol" section that formalises three disciplines (TODO is forward-looking; DONE ledger complements CHANGELOG; after-merge listing of next-N planned PRs); operationalises both in [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md). This PR is the first application of its own discipline: PR #130 has just shipped, and instead of being added to a "PRs completed" subsection in TODO, it goes straight to DONE.

### Added

- [`.working/DONE.md`](../DONE.md) (new): closed-TODO ledger with two top-level sections: (a) "Closed items" with reverse-chronological entries for PRs #110-#130, each one-paragraph keyed by PR number; (b) "Design decisions made (rotated from TODO 2026-06-21 as part of DONE infrastructure)" with the 11 design decisions previously in TODO's "Key design decisions made this session" subsection, plus four additional decisions surfaced in the current PR sequence (snapshot-as-of-last-refresh, dual-entry CHANGELOG enforcement, wrapper-script-plus-corpus-runner discipline, no-decorative-gate-counts). File-level documentation at the top explains the convention, the relationship to CHANGELOG, and the rotation discipline.

### Changed

- [`TODO.md`](../../TODO.md):
  - Top-of-file blurb updated to reflect that completed items move to DONE rather than vanishing into the CHANGELOG diff: `Completed work is recorded in CHANGELOG.md; this file holds only pending and queued items` → `Completed items move to .working/DONE.md (closed-TODO ledger); historical change detail lives in CHANGELOG.md. This file holds only pending and queued items.`
  - Section restructure:
    - "Active session work (resume here next session) — 2026-06-21" wrapper section removed; its contents either rotated to DONE or kept as their own top-level sections.
    - "Session state at pause" renamed to "Session resume metadata"; library/pack/README versions refreshed to current `2026.06.114 / 1.32.0 / 1.8.70`; PR-cursor updated to "after PR #131 merge".
    - "PRs completed in this session" (entire subsection with 19 PR entries) **rotated to DONE** and removed from TODO.
    - "Key design decisions made this session" (entire subsection with 11 numbered decisions) **rotated to DONE** and removed from TODO.
    - "Queued sequence (next PRs)" promoted to a top-level section; rewritten to remove the two stale follow-up proposals (DONE.md is this PR; gate-count cleanup shipped in PR #130). Now lists only forward-looking items: fitness skill amendment, fitness backlog Pass-1, fitness backlog Pass-2 batches.
    - "Other queued moves" kept verbatim (forward-looking).
    - "Critical user feedback to remember across sessions" kept; reformatted to add explicit links to the pack rules / SKILL.md sections where each piece of guidance is now operationalised. Two new items added: TODO-is-forward-looking discipline (operationalised in change-tracking.md) and list-next-5-PRs-after-merge discipline (operationalised in CLAUDE.md and change-tracking.md).
    - "Open follow-ups from validation sweeps" kept verbatim (forward-looking).
- [`.working/README.md`](../README.md):
  - New "Top-level files" subsection before "Activities" listing single-file artefacts like `DONE.md` that don't fit the activity-subdirectory shape.
  - Closing instruction "To add a new activity" extended to mention top-level single-file artefacts go in the Top-level files table.
- [`dev-security/claude-rules/governance/change-tracking.md`](../../dev-security/claude-rules/governance/change-tracking.md):
  - New top-level section "PR finalization protocol" inserted before "Exception-handling protocol".
  - Section content covers three disciplines, each as its own subsection: "TODO is forward-looking; historical state rotates out"; "DONE ledger keyed by original backlog ID"; "After-merge: list the upcoming next-N planned PRs".
  - Each subsection includes worked-example detail and contrasts with anti-patterns. The "Anti-patterns" subsection at the end of the new section names five concrete failure modes to avoid: strikethrough-instead-of-delete, recently-completed-subsection-in-TODO, close-in-CHANGELOG-only, list-from-memory, phantom-backlog-item.
  - No metadata-block edit (this rule does not carry a per-file Version field; pack version tracks it).
- [`.claude/rules/governance/change-tracking.md`](../../.claude/rules/governance/change-tracking.md): mirrored from the pack source per the claude-rules sync convention. Gate 37 (claude-rules sync) enforces parity.
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): PR workflow section extended with two new steps. Step 6 codifies the after-every-merge list-next-5-PRs discipline (consult TODO; refresh first if new items have surfaced). Step 7 codifies the TODO/DONE rotation discipline (delete from TODO + add to DONE in the same PR; TODO holds only forward-looking content). Both steps cross-reference the pack rule for the project-agnostic form of the discipline.
- [`dev-security/claude-rules/README.md`](../../dev-security/claude-rules/README.md): pack version `1.31.0 → 1.32.0`; version-history table row added describing the PR finalization protocol addition.
- [`README.md`](../../README.md): library version `2026.06.113 → 2026.06.114`; README version `1.8.69 → 1.8.70`.

### Verification

- Local audit: `tools/run_all_audits.sh` exits 0 on all gates after the edits.
- Local PR-time checks: `tools/run-pr-time-checks.sh` exits 0.
- Manual contradiction-search: grep TODO.md for "PRs completed in this session", "Key design decisions made this session" — returns no matches (the subsections were rotated out cleanly).
- Manual cross-reference check: every PR # mentioned in the rotated DONE entries is real and present in the git log; every link in DONE.md resolves (the file is under `.working/` so the broken-link audit doesn't scan it, but a manual review confirms link integrity).
- Pack sync: `tools/lint-claude-rules-sync.py` (gate 37) confirms the local copy at `.claude/rules/governance/change-tracking.md` matches the pack source.

### Discipline observation

This PR is the first application of its own discipline. Three discipline-relevant observations:

1. **The before-state was the failure mode the discipline prevents.** TODO carried 19 PRs in a "PRs completed this session" subsection and 11 "Key design decisions made this session" entries. Both were historical context that had no place in a forward-looking backlog. The maintainer surfaced the issue: "PRs completed this session talks about yesterday, and that has no place in the TODO now that the DONE is about to be created." This PR rotates all of it.

2. **The next PR after this one will rotate this PR's TODO entry.** Before this PR, the queued-sequence section would have shown the fitness-skill amendment as "Next, PR #N" with the gate-count cleanup as item "(b)" in a follow-up paragraph. After this PR, the queued sequence is clean and the assistant's post-merge protocol is to list the next 5 PRs from that clean sequence. Concrete demonstration that the discipline reduces the cumulative cognitive load.

3. **The maintainer surfaced the list-next-5-PRs-after-merge standard mid-PR.** Captured durably in CLAUDE.md and in the pack rule so it survives across sessions. The maintainer's pattern of surfacing process disciplines mid-work and the assistant's pattern of capturing them in the change-tracking layer that ships them to other adopters via the pack is itself one of the patterns the future "corpus-management discipline as a shareable skill" (TODO P4.6) will want to capture.

---

## 2026-06-21, Library Version 2026.06.113, PR #130

Removes decorative gate-count narrations from prose throughout the corpus and tooling. The §6 inventory in [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md) remains the canonical source for both the gate list and the current count; downstream prose now points to it rather than carrying a stale-prone literal N. Gate 39 (cross-file gate-count consistency audit) remains operational as the defence against new decorations creeping back in.

### Changed

- [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md):
  - §2.1 in-scope line: `The 45 audit gates currently wired into the audit-programme (see §6).` → `The audit gates currently wired into the audit-programme (see §6 for the canonical inventory and current count).`
  - §6.1 delta-gates paragraph: `Delta gates are not part of the 45-gate corpus inventory above` → `Delta gates are not part of the corpus inventory above`.
  - Gate 39's own description retained verbatim because gate 39's purpose statement explicitly references the patterns it scans for (the description is documenting the linter's logic, not making a count claim).
  - Version `1.13.0 → 1.13.1` (patch: prose-only edit, no inventory change).
- [`governance/procedure-library-quality-and-review-cadence.md`](../../governance/procedure-library-quality-and-review-cadence.md): `The full 45-gate audit programme` → `The full audit programme`; trailing parenthetical extended to point at §6 for current gate count. Version `1.0.12 → 1.0.13`.
- [`governance/register-coverage-gaps.md`](../../governance/register-coverage-gaps.md): "Audit programme" row's right-hand summary cell rewritten. Previously enumerated all ~45 gate names inline (a long mirror of §6 that broke every time a gate was added); now reads `Audit programme running in CI on every PR (see ... §6 for the canonical gate inventory and current gate count); coverage spans metadata integrity, language and style, reference integrity, content-drift defence, programme and index integrity, security and privacy, and freshness and lifecycle (see specification §5 for the functional categorisation and §6 for the per-gate detail)`. Removes the brittle inline enumeration; readers go to §5/§6 for detail. Version `1.1.14 → 1.1.15`.
- [`governance/register-document-index-and-classification.md`](../../governance/register-document-index-and-classification.md): row 53 "Audit Programme Specification" description cell: `Defines the 45-gate audit programme` → `Defines the audit programme: gate inventory (current count in spec §6)`. Version `1.27.23 → 1.27.24`.
- [`governance/register-main-branch-protection.md`](../../governance/register-main-branch-protection.md): two locations.
  - Line 47 row "Required status check" right-hand cell: `The CI job that runs the 45-gate audit programme` → `The CI job that runs the audit programme`.
  - Line 109 narrative: `The 45-gate audit programme assumes ... gates 1-45 still run` → `The audit programme assumes ... every corpus gate still runs`.
  - Version `1.0.12 → 1.0.13`.
- [`tools/README.md`](../../tools/README.md): five locations.
  - Line 7 lede: `consists of **45 gates**` → `is a set of linters, build-and-check generators, and the linter regression test suite`; canonical-source pointer expanded to mention current gate count lives in §6.
  - Line 21: `runs all 45 gates in the order defined in ...` → `runs every gate in the order defined in ...`.
  - Line 44: `wires all 45 gates as local hooks` → `wires every gate as a local hook`.
  - Line 51: `the full 45-gate audit programme` → `the full audit programme`.
  - Line 59: `runs the same 45 gates` → `runs the same gate set`.
- [`tools/check-changelog-on-pr.py`](../../tools/check-changelog-on-pr.py) docstring: `not part of the 45-gate corpus audit programme. The 45 corpus gates check repository state at HEAD` → `not part of the corpus audit programme. The corpus gates check repository state at HEAD`.
- [`tools/check-version-bump-on-pr.py`](../../tools/check-version-bump-on-pr.py) docstring: `not part of the 45-gate corpus audit` → `not part of the corpus audit`.
- [`tools/lint-audit-gate-parity.py`](../../tools/lint-audit-gate-parity.py) line 71 comment: `of the 45-gate corpus inventory in §6` → `of the corpus inventory in §6`.
- [`tools/run-pr-time-checks.sh`](../../tools/run-pr-time-checks.sh) two header comment lines: `the 45 corpus gates` → `the corpus gates`.
- [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh): top-of-file comment `current sweep is 45 gates` reframed to `current sweep covers the full corpus inventory; see ... section 6 for the canonical inventory and current gate count`. Sub-group comment `Markdown linters (sub-group of the 45 corpus gates)` → `... sub-group of the corpus gates`.
- [`README.md`](../../README.md): library version `2026.06.112 → 2026.06.113`; README version `1.8.68 → 1.8.69`.

### Not changed (deliberately)

- The §6 inventory table itself in `specification-audit-programme.md` carries explicit row numbers (1 through 45 at the time of this PR). Those are structural: §6 IS the canonical list and the numbers are how readers locate individual gates ("gate 35", "gate 45"). Not decoration.
- Comments in [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh) of the form "Generator-output drift gates (2 gates)", "Self-parity gate (1 gate)", "Linter regression test suite (1 gate)" — these describe a one- or two-gate sub-group within the runner and are sized-and-stable; not brittle.
- Gate 39's docstring patterns (`"N-gate"`, `"gates 1-N"`, etc.) are pattern documentation (the gate's regexes), not claims about the count.
- Gate 39 itself is not retired or modified. It remains the defence against new decorations creeping back in. After this PR most prose has no number for the gate to match against, but if a future PR re-introduces a decorative `"the 47-gate audit programme"` narration, gate 39 will catch it on the very next run.

### Verification

- Local audit: `tools/run_all_audits.sh` exits 0 on all gates after the edits.
- Local PR-time checks: `tools/run-pr-time-checks.sh` exits 0.
- Manual contradiction search: `grep -nE '\b[0-9]+[- ]gate|\b[0-9]+ +(audit|corpus) +gate|all +[0-9]+ +gate|\bgates? +1[-]'` against the corpus + tools tree returns no decorative N-gate references after the edits. Only references that remain are inside `.working/` (exempt) and the gate 39 linter's own pattern documentation.

### Discipline observation

This PR is a structural defence against the same churn pattern that surfaced visibly in the immediately-preceding PRs:

- PR #128 cascaded ten "44 gate" → "45 gate" reference updates across seven files in a single PR; gate 39 caught all ten on the first audit run but the work to write the edits, the version bumps that came with them, and the contradiction-search to find them all was real per-PR cost.
- PR #129 then cascaded one more (a `gates 1-44` → `gates 1-45` reference that landed inside register-main-branch-protection.md as part of the gate-45 work, and got missed at first because the regex pattern P3 captures with a different shape).
- The maintainer surfaced the proposal directly: "why not change [decorative gate counts] to be 'passing through all gates' so that we reduce the number of edits needed when we add/remove a gate?" The maintainer's intuition is right: the count is a leaky abstraction. Readers who want it can read it from §6 in one click.

The wider lesson: literal numeric references to corpus-shape state (gate count; rule count; persona count; skill count; framework count) should always either (a) be the canonical single source (§6 itself) or (b) point to (a). Decorative repetitions of the count in narrative prose pay zero ongoing cost only if the count never changes, which in a growing project it always does. Removing them is purely a friction reduction.

Same lesson applies to other corpus-shape state: pack rule count, pack skill count, persona count for `/fitness`, etc. Those references also tend to creep into procedural prose (`"the seven pack rules"`, `"the ten persona reviewers"`). They are stable currently but will need the same treatment when they next change. Not in scope for this PR; flagged for the wider clean-up TODO.

---

## 2026-06-21, Library Version 2026.06.112, PR #129

Post-PR-#128 catch-up. Gate 45 (just added in PR #128) correctly flagged `TODO.md` line 47 ("Next — PR #128: Gate 45 (TODO staleness audit).") on the post-merge `main` `push`-event run, because PR #128 had now merged. PR #128's own PR-event run was green because at PR-time the merge had not yet happened; the failure surfaced one event-cycle later. The fix is the standard "rotate PR from queued to completed" TODO maintenance.

### Fixed

- [`TODO.md`](../../TODO.md) lines 22-49 (PRs-completed list + Queued sequence): PR #128 moved from "Queued sequence" (where it appeared as "Next — PR #128: Gate 45 ...") into the PRs-completed list with its summary. Queued sequence rebased to start with the fitness-skill amendment (formerly "PR #129"; now framed generically as "Next, PR #N" since the actual PR number depends on whatever lands next). Two new follow-up design proposals captured in a paragraph at the bottom of the Queued sequence section: (a) `.working/DONE.md` as a closed-TODO ledger; (b) decorative-gate-count cleanup (P3 candidate).
- [`TODO.md`](../../TODO.md) lines 17-20 (Session state at pause): version snapshot `2026.06.109 → 2026.06.111`; README `1.8.65 → 1.8.67`; branch synced-after marker `PR #126 → PR #128`; gate-count line replaced with "all gates passing" (per the maintainer's just-surfaced "remove decorative gate-count narrations" proposal — applied here ahead of the formal P3 PR because the line was being edited anyway).

### Changed

- [`README.md`](../../README.md): library version `2026.06.111 → 2026.06.112`; README version `1.8.67 → 1.8.68`.

### Verification

- Local audit: `python3 tools/lint-todo-staleness.py` returns 0 after the TODO edits (previously returned 1 with "L47 [queued-PR-merged] line marks PR #128 as queued/next/pending/upcoming but PR #128 has merged into the current branch").
- Full sweep: `tools/run_all_audits.sh` exits 0 on all gates post-commit.
- PR-time checks: `tools/run-pr-time-checks.sh` exits 0 (D1, D2, gate 45 all clean).

### Discipline observation

This PR is gate 45's own first catch in production. The cycle that triggered it:

1. PR #128 added gate 45.
2. PR #128's PR-event CI run executed gate 45; at that point PR #128 was still open, so the merge commit was not in git history. Gate 45 passed.
3. PR #128 merged. The merge commit "Merge pull request #128 from ..." now appeared in `git log --format=%s --all`.
4. The post-merge `push`-event run on `main` executed gate 45 again. The same `TODO.md` line that passed at PR-time now matched the queued-PR-already-merged pattern (because `merged_prs()` returned `{128}` for the first time). Gate failed.
5. The maintainer received a CI-failure email and surfaced it; this PR's catch-up edits resolve the lingering state.

The pattern (gate's own first finding is the PR that added the gate) is unusual but logically consistent: the discipline the gate enforces wasn't yet operational when PR #128 itself was being drafted. Going forward, every PR's pre-merge checklist should include "move this PR from 'Queued' to 'PRs completed'" — which the maintainer also surfaced as the broader proposal (DONE.md or rotate-at-PR-finalization).

The wider lesson aligns with the user's proposal received just before this catch-up began: a PR-finalization step that compares the PR's content against TODO and rotates entries is exactly the discipline that would have prevented this failure mode. Recorded as a queued follow-up under the Queued sequence section. The structural fix is real; the manual workaround in this PR is one-time.

---

## 2026-06-21, Library Version 2026.06.111, PR #128

New audit gate 45 (TODO staleness audit) plus a PR-time-checks wrapper script. Gate 45 mechanically catches the two TODO drift shapes that recurred across four consecutive validation sweeps (queued PR already merged; sweep cursor behind history); the wrapper `tools/run-pr-time-checks.sh` bundles the two PR-only delta gates (D1 CHANGELOG-on-PR, D2 per-PR version-bump) and gate 45 into one local runner the maintainer invokes before push. The two-runner split (`run_all_audits.sh` plus `run-pr-time-checks.sh`) is a structural fix for the version-bump-omission failure mode that surfaced in PR #127's first push: every gate now has a local invocation path so PR-time delta-gate omissions are caught before push, not after CI flips red.

### Added

- [`tools/lint-todo-staleness.py`](../../tools/lint-todo-staleness.py) (new, ~210 lines, stdlib-only): scans `TODO.md` for two drift patterns. Pattern 1 (queued-PR-already-merged): regex `\b(?:next|queued|pending|upcoming)\b[^\n]{0,80}PR\s*#(\d+)` matches lines marking a PR as queued; if `git log --format=%s --all` shows a "Merge pull request #N" subject for that PR, the line is stale. Pattern 2 (sweep-cursor-behind-history): regex `\bLast\s+validation\s+sweep[:\s]+Sweep\s+(\d+)\s+iter(?:ation)?\s+(\d+)` matches the sweep cursor in TODO; if `.working/validate-sweeps/history.md` contains a more recent `(sweep_n, iter_m)` tuple, the cursor is stale. Both patterns produce explicit findings with file path + line number + suggested fix. Exit codes: 0 clean, 1 stale, 2 environment error.
- [`tools/run-pr-time-checks.sh`](../../tools/run-pr-time-checks.sh) (new, executable): wrapper that invokes D1 (CHANGELOG-on-PR), D2 (per-PR version-bump), and gate 45 against `${BASE_REF:-origin/main}..${HEAD_REF:-HEAD}`. Reuses each script's positional `base head` argument convention so the same code path works locally and in CI. Exit code: first failing rc, or 0 on all-pass.
- [`tests/test_linters.py`](../../tests/test_linters.py): `TodoStalenessTests` class with five tests — smoke-test against corpus HEAD, queued-PR-already-merged positive case, queued-PR-not-yet-merged negative case, sweep-cursor-behind-history positive case, sweep-cursor-current negative case. Tests use module-loading pattern (importlib spec_from_file_location) to call `check_file` directly with synthetic inputs, mirroring `PairedSkillStepParityTests`.

### Changed

- [`.github/workflows/quality.yml`](../../.github/workflows/quality.yml): new step `TODO staleness audit` appended after `Paired-skill step-parity audit`, before the PR-only delta gates. Step invokes `python3 tools/lint-todo-staleness.py`. Mirrors the existing step shape exactly.
- [`tools/run_all_audits.sh`](../../tools/run_all_audits.sh): new `run_gate "TODO staleness audit"` invocation appended to the tail. Top-of-file comment `current sweep is 44 gates` → `current sweep is 45 gates`. Scope comment updated.
- [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml): new hook `lint-todo-staleness` appended to the tail. Mirrors the existing hook shape exactly (`pass_filenames: false`, `types: [markdown]`).
- [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md): §6 inventory table extended with row 45 (TODO staleness audit). §5 category 7 (Freshness and lifecycle) gains gate 45 with rationale referencing the four-consecutive-sweep recurring pattern. §2.1 "44 audit gates" → "45 audit gates". §6.1 "44-gate corpus inventory" → "45-gate corpus inventory". New paragraph describing gate 45's two-pattern detection logic and the deliberate version-snapshot-field non-enforcement decision (per the PR #127 convention amendment). Version `1.12.1 → 1.13.0`; the MINOR bump reflects the new gate row, not a patch-level edit.
- [`governance/register-coverage-gaps.md`](../../governance/register-coverage-gaps.md): row "Audit programme (automated linting and conformance)" updated: "44 gates running in CI" → "45 gates running in CI"; gate-list narrative extended with "and TODO staleness". Version `1.1.13 → 1.1.14`; Date `2026-06-20 → 2026-06-21`.
- [`tools/README.md`](../../tools/README.md): three references to "44 gates" → "45 gates" (file mentions; pre-commit subsection; CI subsection).
- [`TODO.md`](../../TODO.md): line 19 audit-programme line `44 gates` → `45 gates`. Preamble (line 5) amended to record the narrow gate-45 exception to TODO's "informational only" status: TODO is now subject to one specific audit gate (gate 45) while remaining exempt from the other 44. New P4.6 section ("Corpus-management discipline as a shareable skill") added per maintainer authorisation: future deliverable to package the cumulative discipline as a standalone Claude Code skill anyone managing a documentation corpus could install; scheduled after the FR-1..FR-111 fitness backlog closes.
- [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md): PR workflow step 1 amended to require both `tools/run_all_audits.sh` AND `tools/run-pr-time-checks.sh` pass before push. Rationale: the two-runner split is the structural fix for the PR-time-delta-gate omission failure mode that surfaced in PR #127's first push (version-bump on `.working/fitness-reviews/history.md` body change was caught by D2 in CI rather than locally; if `run-pr-time-checks.sh` had existed and been invoked, the maintainer would have caught it before push).
- [`README.md`](../../README.md): library version `2026.06.110 → 2026.06.111`; README version `1.8.66 → 1.8.67`.

### Verification

- Local sweep: `tools/run_all_audits.sh` exits 0 on all 45 gates (including gate 45 itself, run against TODO.md at HEAD).
- Local PR-time checks: `tools/run-pr-time-checks.sh` exits 0 (this PR modifies CHANGELOG.md AND detailed mirror; bumps README version; TODO.md is up-to-date).
- Regression suite: `python3 tools/run-linter-regression.py` includes the new `TodoStalenessTests` class; all 5 tests pass.
- Gate-name parity (gate 35) confirms the new gate appears identically in the spec inventory, the workflow, the runner, and the pre-commit config.
- Manual contradiction-search: grep for `44 gate|gate 44` across corpus files (excluding `.working/` which is exempt) returned only the expected stale references that this PR updates; no stale references remain post-edit.

### Discipline observation

This PR is the structural pair to PR #127's content-correction work. PR #127 corrected the four-sweep recurring TODO drift symptom (counts, snapshots, cursors) and amended the convention framing at the source. This PR ships the mechanical defence (gate 45) plus the structural defence (the wrapper script) so the next recurrence is caught before it reaches CI. The two PRs together close the loop: convention reframe (PR #127) + mechanical enforcement (PR #128).

The wrapper-script motivation is direct user feedback: "It's great that this was caught, but the fact that you forgot concerns me. Advise." The structural fix is to make the discipline mechanical rather than relying on the assistant remembering. The wrapper is short (~80 lines) and adds the missing local-invocation path for the PR-only delta gates that `run_all_audits.sh` could not cover (because their inputs include git-history range, not just HEAD state).

The new TODO P4.6 entry records the maintainer's authorisation to package the cumulative discipline (seven governance rules + two periodic-review skills + audit-programme architecture) as a shareable Claude Code skill. Scheduled after the fitness backlog closes so the calibration the backlog is still surfacing can inform the shareable form.

---

## 2026-06-21, Library Version 2026.06.110, PR #127

Sweep 11 iteration 1 close-out. Eight in-window findings actioned: corrected the fitness report's count mismatch across six surfaces (95/18/22/31/24 → mechanically-tabulated 111/17/20/57/17); updated `governance/specification-audit-programme.md` D1 description for dual-entry post-PR-#125; refreshed TODO and reframed its session-pause snapshot as "as-of-last-refresh" (one-time convention amendment to address the four-consecutive-sweep recurring drift); softened workflow ordering in `change-tracking.md`; renamed `.working/README.md` "Created by" column to "Origin"; bumped library version.

### Fixed

- [`.working/fitness-reviews/2026-06-21-r1.md`](../fitness-reviews/2026-06-21-r1.md) §1 + §8: claimed "95 unique findings / 18 H[critical] / 22 H / 31 M / 24 L". Mechanical tabulation of FR-1 through FR-111 (verified by orchestrator with explicit Python tally) yields **111 unique findings / 17 H[critical] / 20 H / 57 M / 17 L**. §1 corrected with explanatory note documenting the discrepancy and the Sweep 11 iter 1 correction; §8 backlog summary corrected to authoritative mechanical counts. (Subagent A finding A11-1; High; corroborated by orchestrator re-tabulation.)
- [`.working/fitness-reviews/history.md`](../fitness-reviews/history.md) Findings column for r1 row: updated to `111 (17 H[critical], 20 H, 57 M, 17 L)` with note `counts corrected from PR #124's "95/18/22/31/24" approximation in Sweep 11 iter 1`.
- [`governance/specification-audit-programme.md:144`](../../governance/specification-audit-programme.md): D1 description was stale post-PR-#125. Said "fails when CHANGELOG.md is not in the diff"; now correctly says "BOTH the root CHANGELOG.md AND the detailed mirror at `.working/changelog-details/CHANGELOG-detailed.md` must be in the diff (lock-step); modifying one without the other fails the gate". Spec version `1.12.0 → 1.12.1`; Date `2026-06-20 → 2026-06-21`. (Subagent A finding A11-2; Medium.)
- [`TODO.md`](../../TODO.md): four findings (B-1 through B-4) — version snapshot stale (2026.06.107 vs canonical 2026.06.109), PRs-completed list ends at #121 (missing #122-#126), sweep cursor stale (Sweep 10 iter 2 vs current Sweep 11 iter 1), "Next — PR #122" framed as queued despite #122 having merged. All four resolved via PRs-completed list extension (now includes #122-#127) and Queued-sequence section rewrite. Plus a convention amendment: the "Session state at pause" preamble now explicitly frames the version-snapshot field as "as-of-last-refresh", not "at HEAD", with explanatory note about expected drift. This addresses the four-consecutive-sweep recurring pattern at its source. (Subagent B findings B-1 through B-4; Medium + 3 Low.)
- [`dev-security/claude-rules/governance/change-tracking.md:147-151`](../../dev-security/claude-rules/governance/change-tracking.md): "Two-file split workflow" subsection lists steps 1 and 2 as if sequential (write detailed first, then root). Softened to "Authorship order within the commit is the author's choice; the gate only checks the diff." Mirrored to [`.claude/rules/governance/change-tracking.md`](../../.claude/rules/governance/change-tracking.md). (Subagent A finding A11-3; Low.)
- [`.working/README.md:31`](../README.md): "Created by" column heading renamed to "Origin" for clarity (rows are PR refs, not authorship). "To add a new activity" instruction updated to match. (Subagent A finding A11-4; Low.)

### Changed

- [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md): version `2.0.2 → 2.0.3`. Sweep 11 iter 1 row appended with `Subagents: A, B, C` per Rule 5.6.
- [`README.md`](../../README.md): library version `2026.06.109 → 2026.06.110`; README version `1.8.65 → 1.8.66`.

### Added (under `.working/`, exempt from corpus audit gates)

- [`.working/validate-sweeps/2026-06-21-sweep11-iter1.md`](../validate-sweeps/2026-06-21-sweep11-iter1.md): per-iteration detail file with A/B/C subagent reports, eight-finding synthesis, severity adjudication, and pattern observation about recurring TODO drift.

### Pattern observation (recurring meta-finding now resolved at source)

Four consecutive sweeps (Sweep 10 iter 2, iter 3 close-out, iter 3 catch-back, and now Sweep 11 iter 1) caught the same TODO drift shape: the "Library version at HEAD" snapshot becoming stale as subsequent PRs landed before resume. Each iteration fixed the symptom (refresh the snapshot) but the convention's framing ("at HEAD" = current-state claim) re-introduced the drift on the next close-out PR that bumped versions. This PR addresses the root cause by reframing the snapshot as "as-of-last-refresh" with explicit drift-is-expected wording. Gate 45 (queued for PR #128) will catch the harder-to-tolerate drift shapes (Next-PR-marked-merged, sweep-cursor-behind-history) mechanically at PR time.

### Verification

All 44 audit gates pass standalone post-commit. Pre-flight scanner returns 0 candidates. Mechanical tabulation of FR-1..FR-111 in the fitness report confirmed via `grep + Python` orchestrator-level re-count.

### Discipline observation

This iteration validates the user's recent proposal to introduce unverified→confirmed labelling for fitness findings: I (the orchestrator) accepted the subagent-aggregate "95 findings" number without re-tabulating against the actual FR-N enumeration, and that error propagated across six surfaces. The PR #128 amendment to the fitness skill (queued) will close this gate by making orchestrator-level verification a required step.

---

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
