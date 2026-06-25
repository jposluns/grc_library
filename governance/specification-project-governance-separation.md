# Project Governance Separation Specification

**Document Title:** Project Governance Separation Specification\
**Document Type:** Specification\
**Version:** 1.0.2\
**Date:** 2026-06-25\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md), [`governance/framework-document-architecture-and-interrelationship.md`](framework-document-architecture-and-interrelationship.md), [`governance/specification-audit-programme.md`](specification-audit-programme.md), [`governance/README.md`](README.md), [`.working/README.md`](../.working/README.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material change to the repository's directory model or the corpus-versus-project boundary\
**Repository Path:** [`governance/specification-project-governance-separation.md`](specification-project-governance-separation.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This specification defines the boundary between two kinds of governance artefact that have, until now, both lived in the `governance/` domain directory:

1. **Corpus governance** (also "library governance"): the governance, risk, and compliance content the library publishes as its deliverable. An adopter reads and adapts this content.
2. **Project governance**: the operational records of running *this* library. An adopter does not consume these; they document how the maintainer operates and audits the corpus.

It states the criterion that classifies any artefact into one of the two, the dependency-direction rule that keeps the boundary clean, the destination convention for project governance (the `.project-governance/` directory), the gate consequences of the split, and the phased migration procedure. It is the decision record that supersedes the deferred backlog items R2 (citation-verification cluster relocation) and is the reusable pattern a forker adapting the library-as-living-project would follow.

The split exists because `governance/` is meant to hold governance *documents and templates*, the deliverable, and the accumulation of operational records (a live citation-verification campaign, coverage trackers, review schedules) inside it dilutes that meaning and forces an adopter to read past project-internal state to reach the content they came for.

---

## 2. Scope

### 2.1 In scope

- Every Markdown artefact currently in `governance/`, classified in §5.
- The `.project-governance/` directory created to hold project governance, defined in §6.
- The gate and generator consequences of the split, in §7.
- The migration procedure that moves classified artefacts to their destination, in §8.

### 2.2 Out of scope

- The `dev-security/claude-rules/` pack and its `.claude/` deployment. That pack is AI-assistant discipline distributed as a reusable product; it is neither corpus governance (it is not GRC content) nor project governance (it is not operational record). It keeps its own location and conventions.
- The `.working/` directory, which holds frozen-state archives (per-run records from `/validate`, `/fitness`, and similar). `.working/` is unmaintained-after-write and exempt from corpus gates; `.project-governance/` is maintained and audited (§6.3). The two are distinct and neither subsumes the other.
- The substance of any classified artefact. This specification moves artefacts and re-points citations; it does not rewrite their content.

---

## 3. The two layers and the classifying criterion

### 3.1 Definitions

**Corpus governance** is content whose audience is the adopter: a reader who takes the library's GRC material and adapts it to their own organisation. Policies, standards, frameworks, guidelines, charters, cross-framework matrices, and the content registers an adopter would reference (glossary, key terms, role authority, retention schedule) are corpus governance. So are the *reusable patterns* of process: a specification of how to run an audit programme, a procedure for a review cadence, a template for a verification worklist. The pattern is the deliverable; an adopter adapts it.

**Project governance** is the operational record of running this specific library: the filled-in instances that the reusable patterns produce when the maintainer actually operates the project. A live citation-verification campaign's registers and batch worklists, a coverage-gap tracker for this corpus, this project's review schedule. These are not content an adopter adapts; they are the maintainer's working record.

### 3.2 The criterion

> **A reusable governance pattern is corpus governance. A filled-in operational instance of running this project is project governance.**

The criterion turns on *reusable pattern* versus *operational instance*, not on *content* versus *process*. Process content can be either: the specification of a process is a reusable pattern (corpus); the record of having executed that process on this corpus is an operational instance (project).

Worked application to the citation-verification family, which spans the boundary:

- `specification-citation-verification.md` (how to verify a citation) is a reusable pattern → corpus.
- `template-citation-verification-worklist.md` (the blank worklist shape) is a reusable pattern → corpus.
- `register-citation-verifications.md` and the `worklist-citation-verification-batch-*.md` files (this project's actual verification results and campaign batches) are operational instances → project.

The same lens explains the earlier R1 decision: `tools/sweep-preflight-exemptions.json` was scanner-private machine configuration, an operational instance consumed only by its scanner, and it correctly lives with that scanner in `tools/`.

---

## 4. The dependency-direction rule

The boundary is kept clean by a one-way dependency rule:

> **Project governance may cite corpus governance. Corpus governance must not cite project governance.**

The deliverable does not depend on the maintainer's operational internals; the operational records freely cite the deliverable they govern. This is the same layering discipline that forbids a domain layer from importing its infrastructure: dependencies point inward, toward the stable deliverable, never outward toward operational state.

Two consequences follow:

1. **`register-document-index-and-classification.md` indexes corpus files only.** The corpus document index is corpus governance; under the direction rule it cannot list project-governance artefacts. Project-governance artefacts are indexed by `.project-governance/README.md` instead (§6.2).
2. **Migration is citation surgery, not a file move.** Before any artefact moves to `.project-governance/`, every inbound citation from a corpus document is severed or reworked (§8.2). A leftover corpus-to-project citation violates the direction rule and, because both layers are audited (§6.3), is caught by the broken-link gate.

Because `.project-governance/` is audited rather than exempt, links *within* it and *into* it from non-deliverable surfaces (the pack, the repository backlog and `CHANGELOG.md`, generated indexes) do not dangle; the direction rule, not link-resolvability, is what the separation turns on. A future mechanical gate can enforce the direction rule directly (a check that no corpus document links into `.project-governance/`); §7.3 records it as queued.

---

## 5. Classification of the current `governance/` corpus

The 40 Markdown artefacts in `governance/` as of this specification's date, plus this specification itself, classify as follows. "Stays" means the artefact remains corpus governance in `governance/`. "Move (Phase 1)" and "Deferred" are project-governance artefacts; the phase column records when they migrate (§8).

### 5.1 Corpus governance (stays in `governance/`)

| Artefact | Type | Why corpus |
| --- | --- | --- |
| `README.md` | Register | Domain index of the corpus governance directory |
| `charter-governance-library.md` | Charter | Published charter |
| `framework-continuous-assurance-and-improvement.md` | Framework | Published framework |
| `framework-document-architecture-and-interrelationship.md` | Framework | Published framework (the doc model an adopter adapts) |
| `framework-governance-performance-and-improvement.md` | Framework | Published framework |
| `framework-human-capital-and-ethical-conduct.md` | Framework | Published framework |
| `framework-metrics-monitoring-and-performance-reporting.md` | Framework | Published framework |
| `framework-sustainability-and-responsible-technology.md` | Framework | Published framework |
| `guideline-esg-and-ai-ethics-disclosure.md` | Guideline | Published guideline |
| `guideline-minimum-viable-governance-structure.md` | Guideline | Published guideline |
| `matrix-cross-framework-alignment.md` | Matrix | Published crosswalk |
| `matrix-reverse-framework-control-crosswalk.md` | Matrix | Published crosswalk |
| `policy-digital-twin-and-simulation-governance.md` | Policy | Published policy |
| `policy-exception-and-risk-acceptance-management.md` | Policy | Published policy |
| `procedure-continuous-improvement-register.md` | Procedure | Reusable procedure pattern |
| `procedure-grc-programme-management-and-annual-review.md` | Procedure | Reusable procedure pattern |
| `procedure-library-quality-and-review-cadence.md` | Procedure | Reusable procedure pattern |
| `procedure-whistleblower-and-incident-reporting.md` | Procedure | Published procedure |
| `register-ai-security-tooling-landscape.md` | Register | Adopter-facing reference landscape |
| `register-canonical-citations.md` | Register | Reusable citation *reference* an adopter adapts; the verification *log* (`register-citation-verifications.md`) is the operational instance, not this list |
| `register-data-retention-schedule.md` | Register | Adopter-facing reference content |
| `register-digital-trust-and-assurance-metrics.md` | Register | Adopter-facing reference content |
| `register-document-index-and-classification.md` | Register | Corpus index (corpus files only, per §4) |
| `register-glossary.md` | Register | Adopter-facing reference content |
| `register-key-terms-and-definitions.md` | Register | Adopter-facing reference content |
| `register-role-authority.md` | Register | Adopter-facing reference content |
| `specification-audit-programme.md` | Specification | Reusable specification pattern |
| `specification-citation-verification.md` | Specification | Reusable specification pattern |
| `specification-project-governance-separation.md` | Specification | This document; reusable specification pattern |
| `standard-records-retention-and-destruction.md` | Standard | Published standard |
| `template-citation-verification-worklist.md` | Template | Reusable template pattern |
| `template-document-review-record.md` | Template | Reusable template pattern |
| `template-library-health-report.md` | Template | Reusable template pattern |

### 5.2 Project governance, Move in Phase 1 (the citation-verification campaign)

| Artefact | Type | Why project |
| --- | --- | --- |
| `register-citation-verifications.md` | Register | This project's actual verification results |
| `register-citation-verification-bundle.md` | Register | This project's campaign bundle record |
| `worklist-citation-verification-batch-q2-iso-iec.md` | Worklist | A campaign batch instance |
| `worklist-citation-verification-batch-q3-1-new-citations.md` | Worklist | A campaign batch instance |
| `worklist-citation-verification-batch-q3-ai-tooling.md` | Worklist | A campaign batch instance |
| `worklist-citation-verification-batch-q4-canonical-citations.md` | Worklist | A campaign batch instance |

These six are the purest operational instances and their inbound corpus citations are bounded (the corpus index, the staying spec, and the staying template), so they migrate first.

### 5.3 Project governance candidates, Deferred (decide per artefact in a later phase)

| Artefact | Type | Why deferred |
| --- | --- | --- |
| `register-coverage-gaps.md` | Register | Operational tracker, but woven into adopter guides (`docs/decision-tree.md`, `docs/template-startup-roadmap.md`); inbound rework is larger |
| `register-document-review-schedule.md` | Register | Operational schedule, but cited by adopter templates (`docs/template-maturity-self-assessment.md`) and staying procedures/templates |

The deferred set is not a backlog of "move eventually"; each is an open classification question that a later phase resolves on its own merits, with "stays corpus" a legitimate outcome.

---

## 6. Destination convention: `.project-governance/`

### 6.1 The directory

Project-governance artefacts live in a new top-level directory, `.project-governance/`. The dot prefix signals "not the deliverable", consistent with the repository's existing meta directories (`.working/`, `.claude/`, `.github/`).

### 6.2 Its own index

`.project-governance/README.md` is the index of project-governance artefacts, the project-side counterpart to `governance/register-document-index-and-classification.md`. It carries a full metadata block and lists the directory's residents. It exists so the corpus index can stay corpus-only (§4) without leaving project artefacts unindexed.

### 6.3 Audited, not exempt

`.project-governance/` is **not** added to the linters' `DEFAULT_EXEMPT_DIRS`. Its artefacts receive the full corpus audit sweep: metadata-block completeness, per-document version and date currency, language, citation accuracy, and link coverage. This is the deliberate contrast with `.working/`: project-governance records are maintained and must stay internally honest, so they stay audited. "Separated from the corpus" means relocated and dependency-isolated, not unaudited.

The one sweep behaviour that changes is adopter-facing inclusion: the generators (taxonomy, portal, maturity scorecard) and the corpus document index treat `.project-governance/` as out of the published deliverable and do not include its artefacts (§7).

---

## 7. Gate and generator consequences

### 7.1 Corpus index becomes corpus-only

`register-document-index-and-classification.md` lists corpus files only (§4 consequence 1). When Phase 1 moves the campaign cluster, the index's rows for those artefacts are removed in the same change.

### 7.2 Generators exclude `.project-governance/`

The taxonomy, portal, and maturity-scorecard generators derive from the published corpus; they exclude `.project-governance/` so project artefacts do not appear in adopter-facing generated output. The exclusion is added to the generators when Phase 1 introduces the directory.

### 7.3 Path-targeted linters re-point; a direction gate is queued

Two linters reference the campaign artefacts by hardcoded path and must re-point when those artefacts move: `lint-citation-verification-freshness.py` (loads the verifications register) and `lint-citations.py` (lists a batch worklist in a citation-source set). Re-pointing keeps the freshness and citation audits live on the moved artefacts, consistent with §6.3.

A new directional-dependency gate is queued (not built in this specification): a check that no corpus document contains a link whose target path is under `.project-governance/`. It is the mechanical enforcement of §4; until it exists, the rule is enforced by the migration discipline (§8.2) and the broken-link gate.

### 7.4 Explicit-allow-list content linters must add the directory

The content linters that implement §6.3's audit obligations fall into two file-discovery shapes, and only one of them picks up `.project-governance/` automatically:

- **Exempt-list walk** (the inclusive shape): the linter walks the repository root for `*.md` and subtracts `DEFAULT_EXEMPT_DIRS`. Because §6.3 deliberately keeps `.project-governance/` out of the exempt set, these linters scan it with no further change. The corpus version-bump-recency audit is one such linter.
- **Explicit allow-list** (the enumerated shape): the linter selects scan roots from a hardcoded list of domain directories plus repository-root meta files (a `DEFAULT_SCAN_PATHS` or `DOMAINS` constant). These linters do **not** pick up a new top-level directory automatically; `.project-governance` must be added to the constant, or the directory is silently skipped.

Every gate that implements a §6.3-named obligation (metadata-block completeness, per-document version and date currency, language, citation accuracy, link coverage) and uses the explicit-allow-list shape must therefore include `.project-governance` in its scan constant. The same applies to any further gate the maintainer classifies as part of the "full corpus audit sweep" beyond §6.3's enumerated list (the per-document review-cadence gate is one such gate, included by maintainer decision so the directory's stated review cadences are scheduled, not merely asserted). When Phase 1 introduces the directory, this addition is made to each explicit-allow-list content linter alongside the path-targeted re-pointing in §7.3, and each addition is protected by a scope-coverage regression assertion so a future refactor cannot silently drop the directory. The Phase-1 migration originally enumerated the explicit-allow-list set incompletely (the date-staleness and review-cadence gates were missed and silently skipped the directory until a validation sweep caught them); this subsection makes the completeness obligation explicit so the gap class does not recur.

---

## 8. Migration procedure

### 8.1 Phasing

- **Phase 1** moves the §5.2 citation-verification campaign cluster (six artefacts), creates `.project-governance/` and its README index, applies the §7 gate and generator changes, and re-points the two path-targeted linters. Phase 1 is a single PR scoped to the move; it ships after this specification (PR 1) merges.
- **Later phases** resolve each §5.3 deferred candidate on its own merits.

### 8.2 Per-artefact migration discipline (applies to every move)

For each artefact moved to `.project-governance/`:

1. **Enumerate inbound citations.** `grep -rln "<basename>" --include="*.md"` across the repository.
2. **Classify each citer.** Generated (regenerates clean), non-deliverable (link is acceptable), within-cluster (moves together), or corpus (must be reworked).
3. **Rework every corpus citer before the move.** Sever the citation, or re-point it if the relationship survives the layer split. No corpus-to-project citation may remain (the direction rule, §4).
4. **Move the file** and update its `Repository Path` metadata field and any self-referential links.
5. **Re-point any path-targeted linter or generator** that referenced the old path (§7.3).
6. **Run the full audit sweep** and the PR-time delta gates; both must pass on the post-move state.

### 8.3 Relationship to R1 and R2

- **R1** (`sweep-preflight-exemptions.json`) was closed won't-move because the file already lived correctly in `tools/`; §3.2 records why that was the right call under this criterion.
- **R2** (the citation-verification cluster relocation) is superseded by this specification: the cluster is classified project governance (§5.2) and migrates in Phase 1 (§8.1). R2 as a standalone open decision is closed; the work it described is now the Phase-1 migration.

---

## 9. Maintenance

This specification is reviewed annually and upon any material change to the repository's directory model or to the corpus-versus-project boundary. When a new artefact is created, its author classifies it under §3.2 at creation time and places it accordingly, so the corpus does not re-accumulate operational state. When a deferred §5.3 candidate is resolved, its row moves to §5.1 or §5.2 and the resolution is recorded in the change history.
