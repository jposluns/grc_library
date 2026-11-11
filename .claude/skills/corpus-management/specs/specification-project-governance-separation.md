# Project Governance Separation Specification

**Document Title:** Project Governance Separation Specification\
**Document Type:** Specification\
**Version:** 1.0.18\
**Date:** 2026-11-10\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/register-document-index-and-classification.md`](../../../../governance/register-document-index-and-classification.md), [`governance/framework-document-architecture-and-interrelationship.md`](../../../../governance/framework-document-architecture-and-interrelationship.md), [`.claude/skills/corpus-management/specs/specification-audit-programme.md`](specification-audit-programme.md), [`governance/README.md`](../../../../governance/README.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material change to the repository's directory model or the corpus-versus-project boundary\
**Repository Path:** [`.claude/skills/corpus-management/specs/specification-project-governance-separation.md`](specification-project-governance-separation.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This specification defines the boundary between two kinds of governance artefact that both lived in the `governance/` domain directory until this specification separated them:

1. **Corpus governance** (also "library governance"): the governance, risk, and compliance content the library publishes as its deliverable. An adopter reads and adapts this content.
2. **Project governance**: the operational records of running *this* library. An adopter does not consume these; they document how the maintainer operates and audits the corpus.

It states the criterion that classifies any artefact into one of the two, the dependency-direction rule that keeps the boundary clean, the destination convention for project governance (§6), the gate consequences of the split, and the phased migration procedure. It is the reusable pattern a forker adapting the library-as-living-project would follow.

The split exists because `governance/` is meant to hold governance *documents and templates*, the deliverable, and the accumulation of operational records (a live citation-verification campaign, coverage trackers, review schedules) inside it dilutes that meaning and forces an adopter to read past project-internal state to reach the content they came for.

---

## 2. Scope

### 2.1 In scope

- Every Markdown artefact currently in `governance/`, classified in §5.
- The project-governance registers directory, `.claude/skills/corpus-management/registers/` (formerly the top-level `.project-governance/`), which holds project governance, defined in §6.
- The gate and generator consequences of the split, in §7.
- The migration procedure that moves classified artefacts to their destination, in §8.

### 2.2 Out of scope

- The pinned AIQT rules and their `.claude/` deployment. AIQT (https://aiqt.ai), which replaced the rules pack formerly maintained in this repository, is AI-assistant discipline distributed as a reusable product; it is neither corpus governance (it is not GRC content) nor project governance (it is not operational record). It keeps its own location and conventions.
- The maintainer working-state records. The rebuilt public repository keeps a root `.working/` directory holding the public backlog index and the weekly `CHANGELOG.md`; per-run records are kept in the maintainer's private store outside the repository. That working state is distinct from the project-governance registers directory (§6), which is maintained and audited (§6.3; the broken-link gate and the §6.3 content linters cover the registers directory), and neither subsumes the other.
- The substance of any classified artefact. This specification moves artefacts and re-points citations; it does not rewrite their content.

---

## 3. The two layers and the classifying criterion

### 3.1 Definitions

**Corpus governance** is content whose audience is the adopter: a reader who takes the library's GRC material and adapts it to their own organization. Policies, standards, frameworks, guidelines, charters, cross-framework matrices, and the content registers an adopter would reference (glossary, key terms, role authority, retention schedule) are corpus governance. So are the *reusable patterns* of process: a specification of how to run an audit programme, a procedure for a review cadence, a template for a verification worklist. The pattern is the deliverable; an adopter adapts it.

**Project governance** is the operational record of running this specific library: the filled-in instances that the reusable patterns produce when the maintainer actually operates the project. A live citation-verification campaign's registers and batch worklists, a coverage-gap tracker for this corpus, this project's review schedule. These are not content an adopter adapts; they are the maintainer's working record.

### 3.2 The criterion

> **A reusable governance pattern is corpus governance. A filled-in operational instance of running this project is project governance.**

The criterion turns on *reusable pattern* versus *operational instance*, not on *content* versus *process*. Process content can be either: the specification of a process is a reusable pattern (corpus); the record of having executed that process on this corpus is an operational instance (project).

Worked application to the citation-verification family, which spans the boundary:

- `specification-citation-verification.md` (how to verify a citation) is a reusable pattern → corpus.
- `template-citation-verification-worklist.md` (the blank worklist shape) is a reusable pattern → corpus.
- `register-citation-verifications.md` and the `worklist-citation-verification-batch-*.md` files (this project's actual verification results and campaign batches) are operational instances → project.

The same lens places `.claude/skills/corpus-management/tools/sweep-preflight-exemptions.json`: it is scanner-private machine configuration, an operational instance consumed only by its scanner, so it lives with that scanner in `.claude/skills/corpus-management/tools/` rather than in the registers directory.

---

## 4. The dependency-direction rule

The boundary is kept clean by a one-way dependency rule:

> **Project governance may cite corpus governance. Corpus governance must not cite project governance.**

The deliverable does not depend on the maintainer's operational internals; the operational records freely cite the deliverable they govern. This is the same layering discipline that forbids a domain layer from importing its infrastructure: dependencies point inward, toward the stable deliverable, never outward toward operational state.

Two consequences follow:

1. **`register-document-index-and-classification.md` indexes corpus files only.** The corpus document index is corpus governance; under the direction rule it cannot list project-governance artefacts. Project-governance artefacts are indexed by `.claude/skills/corpus-management/registers/README.md` instead (§6.2).
2. **Migration is citation surgery, not a file move.** Before any artefact moves to the registers directory, every inbound citation from a corpus document is severed or reworked (§8.2). A leftover corpus-to-project citation violates the direction rule, and the gate specified to detect the forbidden dependency direction is the directional-dependency gate (gate 53, §7.3), which checks links into the relocated registers directory. The broken-link gate is specified to catch only the narrower dangling case: a citation left pointing at the old path dangles in the corpus document that carries it, while a citation re-pointed into the relocated registers resolves and is gate 53's to catch.

The registers directory is specified as audited rather than exempt, so links *within* it and *into* it from non-deliverable surfaces (the repository backlog and `.working/CHANGELOG.md`, generated indexes) do not dangle; the direction rule, not link-resolvability, is what the separation turns on. A mechanical gate is specified to enforce the direction rule directly (gate 53, a check that no deliverable-corpus document links into the registers directory); §7.3 records it. The broken-link gate (gate 3) and gate 53 both apply this design to the relocated registers directory.

---

## 5. Classification of the current `governance/` corpus

The 40 Markdown artefacts that `governance/` held when this specification was first written, plus this specification itself, are classified as follows. §5.1 lists corpus governance, which stays in `governance/`; §5.2 and §5.4 list project governance, which lives in the registers directory (§6) or, for the §5.2 campaign bundle record and per-batch worklists, in the maintainer's private operational store; §5.3 gives the 2 classification questions and how each was settled. The §5.2 cluster and the §5.4 register have since migrated, and both classification questions are settled (§5.3); the tables give each artefact's classification, not a live listing of `governance/`.

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
| `register-coverage-gaps.md` | Register | Adopter-facing reference woven into the adopter guides (`governance/decision-tree.md`, `governance/template-startup-roadmap.md`) as routing logic; the honest-disclosure content an adopter references (classified corpus on the §3.1 adopter-referenced-register criterion and the §4 no-deliverable-link-into-project constraint; see §5.3) |
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

### 5.2 Project governance: the citation-verification campaign

| Artefact | Type | Why project |
| --- | --- | --- |
| `register-citation-verifications.md` | Register | This project's actual verification results |
| The campaign bundle record and the four per-batch worklists | Register and worklists | This project's filled-in campaign instances; at the public rebuild they moved to the maintainer's private operational store and are not in the public tree |

These are the purest operational instances. Before the move, their only corpus citers were the corpus index, the staying specification and the staying template, so they were the simplest cluster to separate and moved first.

### 5.3 Classification questions

Under the §9 maintenance rule, a settled question's row moves to its destination section and the resolution is recorded in the change history:

| Artefact | Type | Resolution |
| --- | --- | --- |
| `register-coverage-gaps.md` | Register | **Stays corpus** (moved to §5.1). The citation evidence showed it is woven into the adopter guides (`governance/decision-tree.md` cites it 4x as routing logic, `governance/template-startup-roadmap.md` once) and the §3.1 criterion lists adopter-referenced registers as corpus; a move would force severing adopter-guide routing with no §4-permitted re-point target (a deliverable cannot link into the registers directory). |
| `register-document-review-schedule.md` | Register | **Project governance** (§5.4); it moved to the registers directory in the second move (§8.1). It is a §3.2 filled-in operational instance (this project's review schedule); its corpus citers were severed or re-pointed to the reusable patterns. |

No classification is pending. An open classification question is settled on its own merits, not treated as a backlog of eventual moves, and "stays corpus" is a legitimate outcome, as for `register-coverage-gaps.md`.

### 5.4 Project governance: the document review schedule register

| Artefact | Type | Why project |
| --- | --- | --- |
| `register-document-review-schedule.md` | Register | This project's filled-in review schedule (a §3.2 operational instance), distinct from the reusable review-cadence procedure (`procedure-library-quality-and-review-cadence.md`) and review-record template (`template-document-review-record.md`), which stay corpus |

This single register migrated after the §5.2 cluster, resolving the heavier of the two classification questions. Its corpus citers were more woven than the §5.2 cluster's (a corpus index row, a domain README row, two staying templates' Related-Documents pointers, a staying procedure's maintenance-table row, and an adopter-template example). Each was severed (the staying templates and procedure do not depend on the project instance) or re-pointed to the reusable corpus pattern (the adopter example points to the review-cadence procedure), so no corpus deliverable links into the registers directory (§4, gate 53).

---

## 6. Destination convention: the project-governance registers directory

### 6.1 The directory

Project-governance artefacts live in `.claude/skills/corpus-management/registers/`. Their historical location was a top-level `.project-governance/` directory, whose dot prefix signalled "not the deliverable".

### 6.2 Its own index

`.claude/skills/corpus-management/registers/README.md` is the index of project-governance artefacts, the project-side counterpart to `governance/register-document-index-and-classification.md`. It carries a full metadata block and lists the directory's residents. It exists so the corpus index can stay corpus-only (§4) without leaving project artefacts unindexed.

### 6.3 Audited, not exempt

The project-governance registers directory is specified as audited, not exempt: its artefacts are to stay subject to the corpus audit sweep (metadata-block completeness, per-document version and date currency, language, citation accuracy, and link coverage), with the concrete gate wiring recorded in the audit-programme specification's §6 inventory. The shared file selection in `lint_common.py` gives the relocated registers directory this coverage: `AUDITED_DOMAIN_DIRS` names it for the allow-list linters, and `PROJECT_DOCUMENT_DIRS` admits it ahead of the `.claude/` exemption for the linters that walk the repository (§7.4). This is the deliberate contrast with the maintainer's private per-run records (§2.2): project-governance records are maintained and must stay internally honest, so they are specified to stay audited. "Separated from the corpus" means relocated and dependency-isolated, not unaudited.

The one sweep behaviour that changes is adopter-facing inclusion: the generators (taxonomy, portal, maturity scorecard) and the corpus document index treat the project-governance registers as out of the published deliverable and do not include their artefacts (§7).

---

## 7. Gate and generator consequences

### 7.1 Corpus index becomes corpus-only

`register-document-index-and-classification.md` lists corpus files only (§4 consequence 1). When the campaign cluster moved in the earlier repository, the index rows for those artefacts were removed in the same change.

### 7.2 Generators exclude the registers directory

The taxonomy, portal, and maturity-scorecard generators derive from the published corpus; they exclude the project-governance registers so project artefacts do not appear in adopter-facing generated output. The exclusion was added to the generators when the first move introduced the directory.

### 7.3 Path-targeted linters re-point; a direction gate enforces §4

Two linters reference the campaign artefacts by hardcoded path and must re-point when those artefacts move: `lint-citation-verification-freshness.py` (loads the verifications register) and `lint-citations.py` (lists a batch worklist in a citation-source set). Re-pointing keeps the freshness and citation audits live on the moved artefacts, consistent with §6.3.

The directional-dependency gate that enforces §4 is built as **gate 53** ([`.claude/skills/corpus-management/tools/lint-directional-dependency.py`](../tools/lint-directional-dependency.py)): it flags any deliverable-corpus document that contains a markdown link whose resolved target is inside the registers directory (`.claude/skills/corpus-management/registers/`), the mechanical enforcement of the one-way dependency rule. The deliverable-corpus scan set is derived from `AUDITED_DOMAIN_DIRS` minus the registers directory, plus the moved specifications directory (`.claude/skills/corpus-management/specs/`) and the root deliverable documents; the non-deliverable surfaces §4 permits to link into the directory (the repository backlog, the root `.working/CHANGELOG.md`, the generated indexes, the `.working/` tree and the rest of `.claude/`) are out of scope, and so is the registers directory itself (links within it are allowed). The skill procedures directory (`.claude/skills/corpus-management/procedures/`) is project-side and, like the adopter guides in `.claude/skills/corpus-management/docs/`, sits outside the gate's deliverable-corpus scan roots; `.claude/skills/corpus-management/specs/` is the only directory under `.claude/skills/corpus-management/` that the gate scans. Before the gate existed the rule rested on the migration discipline (§8.2) and the broken-link gate; the gate makes it a standing mechanical check, the §4 counterpart to the §7.4 scan-scope parity gate (gate 52). The gate's `PROJECT_GOV_DIR` is the registers directory path that `AUDITED_DOMAIN_DIRS` carries, and the gate stops with an error if the 2 paths differ.

### 7.4 Explicit-allow-list content linters must add the directory

The content linters that implement §6.3's audit obligations fall into two file-discovery shapes, and under the directory's former top-level `.project-governance/` name only one of them picked the directory up automatically:

- **Exempt-list walk** (the inclusive shape): the linter walks the repository root for `*.md` and subtracts `DEFAULT_EXEMPT_DIRS`. Because §6.3 deliberately keeps the registers directory out of the exempt set, these linters scanned the former top-level `.project-governance/` directory with no further change; since the move, the shared selection admits the relocated registers ahead of the `.claude/` exemption (`PROJECT_DOCUMENT_DIRS` in `lint_common.py`), so these linters still scan them. The corpus version-bump-recency audit is one such linter.
- **Explicit allow-list** (the enumerated shape): the linter selects scan roots from a list of domain directories plus repository-root meta files. Historically each such linter hardcoded the domain run inline (in a `DEFAULT_SCAN_PATHS` tuple, a `DOMAINS` list, or a function-local list), so a new top-level directory was picked up only when `.project-governance` was added to every one of those copies by hand, and the directory was silently skipped wherever a copy was missed.

The audited-domain run now has a **single source of truth**: `AUDITED_DOMAIN_DIRS` in [`.claude/skills/corpus-management/tools/lint_common.py`](../tools/lint_common.py) (the 12 domain directories plus the registers directory, as the path `.claude/skills/corpus-management/registers`). Every explicit-allow-list content linter that implements a §6.3-named obligation (metadata-block completeness, per-document version and date currency, language, citation accuracy, link coverage) splats that constant rather than hardcoding the run, so a future top-level audited directory propagates to every such linter from one place. The same applies to any further gate the maintainer classifies as part of the "full corpus audit sweep" beyond §6.3's enumerated list (the per-document review-cadence gate is one such gate, included so the directory's stated review cadences are scheduled, not merely asserted). The **directory-scan-scope parity gate** (gate 52, [`.claude/skills/corpus-management/tools/lint-scan-scope-parity.py`](../tools/lint-scan-scope-parity.py)) is the mechanical backstop for this subsection: it forbids any content linter from hardcoding the domain run (it matches the literal directory names, so it is robust to all 3 declaration styles above), with a documented `EXEMPT` set for the files that legitimately scan a *different* domain set (the section-placement gate and the taxonomy generator, which scan the corpus-document set that excludes the registers directory because those documents are outside the corpus document model, and the collection-candidate helper). The first migration originally enumerated the explicit-allow-list set incompletely (the date-staleness and review-cadence gates were missed and silently skipped the directory until a validation sweep caught them); the single-source-of-truth refactor plus gate 52 makes that gap class structurally impossible rather than relying on each addition being remembered.

---

## 8. Migration procedure

### 8.1 Phasing

In the earlier repository, the migration moved the project-governance artefacts in 2 phases. Each move shipped as a single pull request scoped to that move, after this specification had merged:

- **The §5.2 citation-verification campaign cluster** (six artefacts) moved first: it left `governance/`, the registers directory (§6.1) was created with its README index (§6.2), the §7 gate and generator changes applied, and the two path-targeted linters were re-pointed. That move created the directory as the top-level `.project-governance/` (§6.1) with its README index and moved the six artefacts into it. `register-citation-verifications.md` is now in the registers directory; at the public rebuild the campaign bundle record and the four per-batch worklists moved to the maintainer's private operational store (§5.2).
- **The §5.4 document review schedule register** (one artefact) moved only once its §5.3 classification question was settled, into the directory that the first move created; its inbound corpus citations were severed or re-pointed to the reusable corpus patterns, and the adopter-facing artefacts were regenerated. After the first move, the register moved into the existing `.project-governance/` directory, and it is now in the registers directory.
- **No classification question is pending** (§5.3): `register-coverage-gaps.md` stays corpus (§5.1) and `register-document-review-schedule.md` is project governance (§5.4).

### 8.2 Per-artefact migration discipline (applies to every move)

For each artefact moved to the project-governance registers directory:

1. **Enumerate inbound citations.** `grep -rln "<basename>" --include="*.md"` across the repository.
2. **Classify each citer.** Generated (regenerates clean), non-deliverable (link is acceptable), within-cluster (moves together), or corpus (must be reworked).
3. **Rework every corpus citer before the move.** Sever the citation, or re-point it if the relationship survives the layer split. No corpus-to-project citation may remain (the direction rule, §4).
4. **Move the file** and update its `Repository Path` metadata field and any self-referential links.
5. **Re-point any path-targeted linter or generator** that referenced the old path (§7.3).
6. **Run the full audit sweep** and the PR-time delta gates; both must pass on the post-move state.

---

## 9. Maintenance

This specification is reviewed annually and upon any material change to the repository's directory model or to the corpus-versus-project boundary. When a new artefact is created, its author classifies it under §3.2 at creation time and places it accordingly, so the corpus does not re-accumulate operational state. A §5.3 classification question is settled on its own merits under §3.2; when it is, its row moves to its destination section (§5.1, §5.2 or §5.4) and the resolution is recorded in the change history.
