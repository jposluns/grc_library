# TODO

Forward-looking backlog of planned enhancements for the GRC Documentation Library. Items are added when identified and rotated out when completed. Completed items move to [`.working/DONE.md`](.working/DONE.md) (closed-TODO ledger, keyed by original backlog ID); historical change detail lives in [`CHANGELOG.md`](CHANGELOG.md). This file holds only pending and queued items.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions, with one narrow exception: [`tools/lint-todo-staleness.py`](tools/lint-todo-staleness.py) (gate 45) scans this file for two specific drift shapes (queued PR already merged, sweep cursor behind history). All other audit gates skip this file.

Items are organised by priority (P1-P7); fitness-review findings (from `.working/fitness-reviews/2026-06-21-r1.md` and `.working/fitness-reviews/2026-06-22-r1.md`) are placed by severity into the matching priority section, not in their own area. Each item carries its identifier (FR-N or descriptive ID), a severity tag where applicable (`H[critical]`, `H`, `M`, `L`, or `FYI`), an effort estimate where known (`XS`, `S`, `M`, `L`, `XL` per the proposed convention in P4), and a one-line description of what to do plus the location reference.

---

## Session resume metadata

These are **as-of-session-pause snapshots**, not "current HEAD" claims. They reflect state at the moment this section was last refreshed. The version snapshot and last-validation-sweep cursor each drift forward as the project advances; that drift is expected and not a defect. Gate 45 (TODO staleness audit) catches genuine staleness shapes (queued PR already merged; sweep cursor behind history); other drift is informational.

- **Branch at last refresh**: `main` (synced after PR #229 merge).
- **Library version**: `2026.06.207`. **Pack version**: `1.45.1`. **README version**: `1.9.78`.
- **Audit programme**: all 46 gates passing on `main`.
- **Last validation sweep**: Sweep 21 iter 1 (post PRs #229-#236 Batch 1 effort-first run; 0 in-window, 0 out-of-window across all 3 subagents; empty-delta termination; row carried into Batch 2 PR-A per recursion-avoidance).
- **Last fitness review**: 2026-06-22's r1; Pass-1 verification complete in PR #204.
- **Timezone convention**: UTC (codified in CLAUDE.md per PR #190).

---

## Queueing rules

- Orchestrator picks the next batch from **Priority 1 first, then Priority 2**, in highest-severity order.
- **1-8 PRs per batch** (logical grouping); `/validate` after each batch.
- Maintainer direction supersedes the orchestrator's pick at any time.
- Lower priorities (P3-P7) are picked deliberately, not from the routine batch queue, unless the maintainer triggers them.

---

## Priority 1 — Urgent quality (High[critical] and High severity)

### High[critical] severity (immediate priority)

- **FR-30 (H[critical], L)**: Ship `privacy/template-dpa-article-28.md` standalone GDPR Article 28 Data Processing Agreement template. Currently no DPA template exists; controller-processor obligations are scattered.
- **FR-31 (H[critical], L)**: Ship `privacy/framework-privacy-by-design.md` operationalising GDPR Article 25 by mapping the seven foundational privacy-by-design principles to architecture and dev-security workflows.
- **FR-32 (H[critical], L)**: Ship `privacy/template-legitimate-interest-assessment.md` (LIA) covering the three-part balancing test (purpose, necessity, balancing) per Article 6(1)(f).
- **FR-34 (H[critical], L)**: Ship `privacy/template-transfer-impact-assessment.md` covering the EDPB Recommendation 01/2020 six-step methodology. **Consolidates with FR-74**.
- **FR-70 (H[critical], XL)**: New domain for crypto-asset / blockchain governance. Covers digital-asset custody, staking, smart-contract risk, blockchain platform vetting. Regulatory references: DORA, MiCA, NYDFS BitLicense. (Cross-references P6.x for domain-level shaping.)
- **FR-71 (H[critical], L)**: Ship dedicated M&A due-diligence procedure. `procedure-grc-programme-management-and-annual-review.md` names M&A as a trigger but has no checklist, pre-close template, or integration playbook.
- **FR-72 (H[critical], L)**: Ship dedicated sanctions / OFAC / export-control framework with UBO (ultimate-beneficial-owner) verification and denied-party-list integration. Current treatment is superficial.
- **FR-73 (H[critical], M)**: Separate AI ethics review from compliance/risk body in `ai/charter-ai-governance-council.md`; introduce an independent ethics panel or challenge mechanism.

### High severity (immediate priority)

- **FR-58 (H, M)**: Define inheritance vocabulary (library-internal vs template vs reference content). Multiple documents are inconsistent on what kind-of-content is being referenced.
- **FR-59 (H, L)**: Privacy jurisdiction annexes are too shallow for operational sufficiency; deepen the 25 country annexes to operational level.
- **FR-60 (H, L)**: HIPAA adopter has no operational detail beyond a single 261-line sector annex in `compliance/healthcare`. Deepen.
- **FR-61 (H, L)**: Financial-services adopters outside EU/US lack regulatory regimes: UK PRA/FCA, US OCC/FRB/FDIC, MAS, FSA, APRA, OSFI, HKMA, FINMA.

---

## Priority 2 — Substantive improvements (Medium severity)

Each item is an individual document or focused multi-doc improvement. Most are clustered into the **Phase 2 execution plan** below, which the orchestrator runs in serial PR batches.

### Phase 2 execution plan (current sequence)

Research files for every queued P2.x cluster are prepared in advance (per the research-assistant discipline in [`.claude/rules/governance/ai-assistant-workflow-disciplines.md`](.claude/rules/governance/ai-assistant-workflow-disciplines.md)) and held in the session scratchpad; the orchestrator applies them serially. Pause after Phase 2 completes for a `/fitness` run.

- **P2.1 — Privacy completion (1 remaining)**: **FR-41 (M, L)** AI Article 22 + EU AI Act + FRIA dual/triple-compliance workflow not documented as a unified workflow. (Closed: FR-37 PR #224, FR-38 PR #225, FR-39 PR #226, FR-40 PR #227, FR-42 PR #228.)
- **P2.2 — Continuous assurance / 3LoD (4 items)**: **FR-99 (M, M) ⚠️** per-control effectiveness metrics; **FR-100 (M, S)** cloud baseline cites families not sub-controls; **FR-101 (M, S) ⚠️** closure sign-off authority implicit; **FR-102 (M, S)** change management binary.
- **P2.3 — Cross-framework matrix (2 items)**: **FR-97 (M, S)** ISO 31000 clause numbering; **FR-98 (M, S)** NIS 2 annex evidence-class column.
- **P2.4 — Adopter cluster (3 items)**: **FR-64 (M, S)** contribution path workflow-shaped not pattern-shaped; **FR-65 (M, S) ⚠️** upstream-sync underspecified; **FR-66 (M, S)** tooling assumes maintainer context.
- **P2.5 — Coverage-gap small (2 items)**: **FR-77 (M, S)** 3LoD model used without explanation; **FR-78 (M, S)** framework-document-architecture maintainer voice.
- **P2.6 — KRI/KPI (2 items)**: **FR-93 (M, S)** KRI escalation owner missing; **FR-94 (M, S)** Linked controls register dependency.
- **P2.7 — FR-15 (M, M)**: Maturity-ladder methodology — median-of-medians scoring concern.
- **P2.8 — FR-23 (M, M) ⚠️**: Audit-evidence assembler-verification standard absent.
- **P2.9 — FR-24 (M, M)**: Control-testing procedure thinner than peers.
- **P2.11 — FR-48 (M, L)**: H2 numbering patterns drift — multi-doctype structural rename. Deferred until a dedicated session is scheduled.
- **P2.12 — FR-58 (M, M)**: Inheritance vocabulary (also listed under P1 Highs).
- **P2.13 — FR-63 (M, M)**: Worked example walks ingestion not adoption.
- **P2.14 — FR-83 (M, S)**: IC (independent challenge) checklist absent.

### Other Medium-severity items (not in a P2.x cluster)

- **FR-62 (M, S)**: AI jurisdiction annexes absent. (Cross-references P5.8.)
- **FR-74 (M, M)**: Schrems II-light treatment. **Consolidates with FR-34** (Transfer Impact Assessment in P1).
- **FR-75 (M, S) ⚠️**: ESG materiality threshold.
- **FR-76 (M, S) ⚠️**: Sustainability framework escalation triggers.
- **FR-120 (M, S)**: 180-day baseline citation imprecise/circular in [`governance/policy-exception-and-risk-acceptance-management.md`](governance/policy-exception-and-risk-acceptance-management.md) line 99 (NIST CA-6 specifies annual+; ISO 27001:2022 Clause 9.2 doesn't prescribe interval).
- **FR-12 within-document closure was PR #178**; this follow-up is the cross-document harmonisation.

### Substantive content adds (medium scope, non-fitness origin)

- **BYOD policy: MDM vs MAM option (M, S)**: Expand [`security/policy-byod.md`](security/policy-byod.md) to explicitly distinguish (a) MDM (organisation manages the entire device; higher visibility, privacy concerns for personnel) and (b) MAM (organisation controls a container of org applications and data; container-level policy, device-wide privacy preserved). Adopters choose MDM, MAM, or both depending on context. Per maintainer direction.

### Working-state file relocations (small focused PRs)

- **(M, XS)** `tools/sweep-preflight-exemptions.json` → `.working/validate-sweeps/preflight-exemptions.json` (co-locate with the validate-sweeps activity).
- **(M, XS)** Citation-verification cluster (6 files): `register-citation-verifications.md` + `register-citation-verification-bundle.md` + four `worklist-citation-verification-batch-*.md` → `.working/citation-verifications/`. Project-specific in-flight verification campaign.
- **(M, XS)** `governance/register-main-branch-protection.md` → `.working/` somewhere. Snapshot of THIS repo's branch protection; meaningless to adopters configuring their own.

Each file relocation updates the document-index, sibling references, taxonomy/portal regen, version bumps, CHANGELOG entry. Small per item.

---

## Priority 3 — Low-priority cleanup (Low severity / FYI)

Deferred to a routine cleanup batch when convenient. Cross-reference only.

### Low-severity fitness findings (from 2026-06-21 review)

- **FR-68 (L, S) ⚠️**: Adopter edge case — mandatory-except-when-not.
- **FR-69 (L, S)**: Adopter edge case — three baseline sizes.
- **FR-84 (L, S)**: Regression-testing checklist as a discrete artefact.
- **FR-85 (L, S)**: Per-question owner in breach-response runbook.
- **FR-86 (L, S) ⚠️**: Recovery runbook crisis-communications cross-reference. (Pass-1 noted runbook itself was hard to locate; revisit at remediation time.)
- **FR-90 (L, S)**: CSP / Trusted Types / HSTS-preload guidance.
- **FR-109 (L, S) ⚠️**: Charter purpose paragraph density.
- **FR-53 (L, S) (reshape)**: Metadata field unification — evaluate whether to deprecate Classification or Confidentiality as redundant, OR document the semantic distinction.

### FYI-tier from 2026-06-22 review


### Routine cleanup items (non-fitness origin)

- **FR-44-generalisation (L, M)**: Corpus-wide sweep replacing legacy "shall" / "shall not" in normative prose with "must" / "must not" where the verb is not a direct quotation of an external standard. Per file: small but numerous. The FR-44 convention statement itself was documented in PR #159 (master spec §6.1); this is the derivative harmonisation pass.
- **Sweep 3 follow-up (L, S)**: Cross-document term-and-identifier consistency gap (the prose-and-numbering-shaped C3 surface that mechanical gates 35/39/41 don't cover). Candidate for a future mechanical gate; in the meantime a manual sweep pass closes the open items.

---

## Priority 4 — Adopter experience (process and meta improvements)

Items that affect how the library is used, evolved, or extended by maintainers and adopters. Not direct corpus content changes.

### 4.1 Corpus-management discipline as a shareable skill (M, XL)

Package the cumulative documentation-and-corpus discipline this project has accumulated as a standalone Claude Code skill that anyone managing a documentation corpus with an AI coding assistant could install.

- **Trigger surface**: users running Claude Code against a structured Markdown corpus (governance, policy, technical-spec libraries) who want the same disciplines that have prevented drift in this project: metadata blocks, audit gates, generator-output drift checks, version monotonicity, change-tracking conventions, sweep-style validation, fitness-style periodic review.
- **Distillation source**: the eight `governance/` pack rules form the discipline core. The `validation-sweep` and `library-fitness-review` skills form the periodic-review surface. The audit-programme architecture (`tools/lint-*.py` + four-surface wiring + regression fixtures) forms the mechanical-enforcement surface.
- **Generalisation**: the patterns are corpus-shape agnostic but reference GRC-specific document types. The shareable form would carry the patterns and discipline (what to enforce, why, how) without the GRC-specific control-set citations. Adopters supply their own document-type model and metadata-field set.
- **Format**: a skill (or skill family) under `dev-security/claude-rules/skills/` with a top-level `corpus-management-discipline/` directory.
- **Sequencing**: starts after the fitness backlog (FR-1 through FR-111) is closed, since some of the discipline is still being calibrated against the backlog.
- **Open questions**: omnibus skill vs skill family; include linter scaffolds vs prescriptive-only; ship under existing pack (1.x bump) vs new pack.

### 4.2 Backlog effort-sizing labels convention (M, S)

Currently backlog items carry severity (H[critical] / H / M / L) but no effort estimate. The 2026-06-21 mid-batch prioritisation showed effort is needed alongside severity to sequence well. Proposed scale:

| Label | Per-item effort | Bundleable per PR |
|---|---|---|
| **XS** (single-line / single-cell) | 5-15 min | 5-10 items |
| **S** (single-doc section add) | 30-90 min | 2-4 items |
| **M** (multi-doc, bounded) | 2-4 hrs | 1 item |
| **L** (new artefact, multi-doc propagation) | 4-8 hrs | 1 item |
| **XL** (new domain, library-wide reshape) | 1-3 days | 1 item, may split |

**Format**: `**FR-N (severity, XS)**: description` — already in use in this reorganized TODO.

**Surfaces to update when the convention formally lands**:
1. `dev-security/claude-rules/skills/library-fitness-review/SKILL.md`.
2. `dev-security/claude-rules/skills/validation-sweep/SKILL.md`.
3. This file (already in use).
4. `.working/DONE.md` heading shape.
5. Future fitness-review templates and sweep detail files.

Schedule: after the current FR backlog closes (substantive coverage).

### 4.3 Standard-version-upgrade process (M, M)

When an external standard the corpus cites is republished (e.g., `ISO/IEC 27001:2013` → `2022`; `ISO/IEC 27701:2019` → `2025`; future COBIT release), the library needs a documented process to transition. Sweep 15's `ISO/IEC 29134:2023` hallucination plus the FR-21 work that caught `ISO/IEC 27701:2019 → 2025` show ad-hoc updates produce drift.

The seven-step process:
1. Diff old and new version; use the publisher's transition guide as authoritative input.
2. Sweep the corpus (grep + canonical-citations register) for every cited location.
3. Classify each citation as positional-only or substantive.
4. Apply updates per classification (positional: year bump; substantive: rewrite affected content with per-document version bump).
5. Update [`governance/register-canonical-citations.md`](governance/register-canonical-citations.md) and verifications register; mark old version superseded with effective-date.
6. Confirm gate 27 (`tools/lint-standards-currency.py`) flags the supersession.
7. CHANGELOG entry covering the upgrade campaign (often multi-PR); TODO row if substantive rewrites span multiple PRs.

**Deliverable**: `governance/procedure-standard-version-upgrade.md` documenting the process with worked examples. **Side benefit**: also documents the canonical-citations register discipline.

### 4.4 Pack: dev-security/claude-rules language coverage review (M, M)

Review the language-specific security rules in [`dev-security/claude-rules/`](dev-security/claude-rules/). Today the pack ships Python-focused guidance plus external overlay rules.

Two questions:
1. **Are mainstream languages missing?** Candidates likely worth a starter file: JavaScript / TypeScript (Node and browser), Go, Java / Kotlin, Rust, C# / .NET, Swift / Kotlin (mobile). Decide which subset belongs in a GRC-baseline pack vs which to defer to dedicated technical-security sources.
2. **Should we explicitly reference dedicated technical-security projects** (OWASP cheat sheets, language-specific SAST rule packs, vendor secure-coding guides) rather than try to be one?

**Scope**: one or more small PRs that each add a language baseline file (mirror `python.md`'s shape) OR update the pack's README to set the positioning. Small per language.

### 4.5 Audit-gate candidates from 2026-06-22 review (M, S each)

Three new audit-gate candidates surfaced; each needs separate maintainer decision before adding.

- **S1 Cross-document retention-consistency gate**: verify retention periods cited in `governance/register-data-retention-schedule.md` match the procedures (`compliance/standard-internal-audit.md`, `compliance/procedure-capa.md`, `compliance/procedure-control-testing.md`). Would catch C3-class issues mechanically.
- **S2 Role definition consistency gate**: verify every role mentioned in normative documents has a row in `governance/register-role-authority.md`. Would catch FR-115-class issues mechanically.
- **S3 Citation-precision-for-claim gate**: flag "aligned with [normative source] X" claims and verify X actually contains the supporting language. Would catch FR-120-class issues mechanically.

---

## Priority 5 — Content expansion (country / programme / regulator overlays)

Adding new content / coverage to existing domains. Each subitem is a separate small or medium PR; the maintainer schedules deliberately.

### 5.1 Logistics country / programme expansion

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

Within `compliance/financial-services/`:

- UK PRA / FCA (`annex-uk-pra-fca.md`)
- US OCC / FRB / FDIC / SEC / FINRA
- Canada OSFI
- Australia APRA
- Singapore MAS
- Japan FSA

### 5.3 Healthcare country regulator overlays

Within `compliance/healthcare/`:

- US HIPAA detail (Privacy Rule, Security Rule, Breach Notification Rule, HITECH)
- UK NHS DSPT (Data Security and Protection Toolkit)
- EU MDR / IVDR (Medical Device Regulation; In-Vitro Diagnostic Regulation)
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

### 5.6 Public-sector country / regulator overlays

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
- Re-review of EU member-state derogations where applicable

### 5.8 AI jurisdiction overlays

The library cites EU AI Act extensively but lacks a dedicated `ai/jurisdictions/` subdirectory parallel to `privacy/jurisdictions/`. Candidates:

- EU AI Act detailed annex (`ai/jurisdictions/annex-ai-european-union.md`)
- Canada AIDA
- UK AI policy framework
- US state-by-state AI laws (Colorado AI Act, NYC bias audit law, etc.; partial coverage exists today inside the US privacy annex)
- China generative AI rules (partial coverage exists today inside the China privacy annex)
- Korea AI framework

---

## Priority 6 — Domain-level expansion (new domains, longer-term)

Entirely new domains, multi-week scope each. The maintainer schedules deliberately rather than picking these into routine batches.

### 6.1 Multi-cloud governance overlay (XL)

Per-cloud hardening baselines for AWS, Azure, and GCP exist in `dev-security/`. The remaining gap is multi-cloud governance (cross-cloud risk taxonomy, cross-cloud incident coordination, cloud-portfolio-level controls). Could live in `operations/` or warrant a new `cloud/` domain.

### 6.2 Identity-specific content depth (L)

Customer Identity (CIAM) governance, workforce identity governance, identity federation patterns, passwordless adoption playbooks. The library has an Identity and Access Management policy and procedure but no dedicated content for these patterns.

### 6.3 Quantum cryptography readiness deepening (L)

The library has a PQC roadmap at phase level ([`security/roadmap-post-quantum-cryptography.md`](security/roadmap-post-quantum-cryptography.md)) covering discovery, standards, pilot, migration phases but not detailed implementation content. Pending additions: PQC migration playbook (operational steps per system class), crypto-agility patterns (key abstraction, algorithm switching, hybrid schemes), and post-quantum-ready CA / PKI management.

### 6.4 Cross-framework matrix expansion (L)

Current matrix ([`governance/matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md)) covers major frameworks; expand coverage to additional sectoral and regional frameworks as the country/sector content under P5 grows.

### 6.5 CMMI capability levels alongside maturity levels (L)

Per maintainer direction 2026-06-22 (low priority, scheduled after the FR backlog completes). The corpus currently uses the 5-tier maturity-level scale at both organisation-wide and per-domain granularity; CMMI Institute's canonical model distinguishes the two (maturity levels 1-5 for organisation-wide rollup; capability levels 0-3 for per-practice-area performance). Introducing capability levels formally would: (1) add a capability-level scheme to [`governance/framework-governance-performance-and-improvement.md`](governance/framework-governance-performance-and-improvement.md) §2 alongside the existing maturity-level scheme; (2) update [`docs/template-maturity-self-assessment.md`](docs/template-maturity-self-assessment.md) to use capability levels per domain and aggregate to maturity levels at the programme rollup; (3) possibly extend [`governance/register-digital-trust-and-assurance-metrics.md`](governance/register-digital-trust-and-assurance-metrics.md) DTI thresholds with a capability-level surface. Reference: CMMI Institute's "Appraisals > Levels" page (canonical two-axis model).

---

## Priority 7 — Awaiting maintainer decision

Items requiring user decision or external dependency before becoming actionable. Promoted from the prior "Investigation / blocked" meta-section since the decision queue deserves its own priority slot.

### Maintainer-surfaced from /validate Sweep 20 (2026-06-22)


### Formal closure pending review


### Decisions explicitly dropped (recorded for audit trail)

These are NOT pending decisions; they were dropped after maintainer review and are listed here so the audit trail is complete. See [`.working/design-decisions.md`](.working/design-decisions.md) "Decisions explicitly dropped" section for rationale.

- **FR-104**: Per-regulation context not pursued.
- **FR-130**: Portal reorder not pursued (README stays at decision-tree item 1).

---

## Standing conventions

Durable behavioural guidance from the maintainer. Each item links to its operationalisation where one exists. NOT actionable items; reference material for the orchestrator and future contributors.

- **"More PRs, keep each one clean"** — favor small focused PRs.
- **"I prefer /validate, not /validation-sweep"** — short slash commands; skill names stay descriptive.
- **"Don't explicitly name or link `.working/`"** in template-content files that adopters see (e.g., the root CHANGELOG header note for the changelog split).
- **"Inference must be validated before committing or before anything else uses that information"** — operationalised in the pack rule [`validate-inference-before-action.md`](dev-security/claude-rules/governance/validate-inference-before-action.md).
- **Activity directories should be self-contained** — operationalised in the canonical `.working/<activity>/` layout.
- **Zero-finding sweeps still need history rows but no detail files** — operationalised in [`SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) step 9 of the validation-sweep skill.
- **Sweep history is project-application, not template content** — operationalised by keeping the history file in `.working/`.
- **TODO is forward-looking; historical state rotates to DONE.md** — operationalised in [`change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) PR-finalization-protocol section.
- **After completing a merge, list the upcoming next 5 planned PRs from TODO** — operationalised in [`.claude/CLAUDE.md`](.claude/CLAUDE.md) PR-workflow section and the same pack rule.
- **Validate cadence is 1-8 PRs per batch, not strictly 5** — the 5-PR cadence is default; the maintainer (or the assistant in maintainer's authorised autonomous mode) chooses the batch boundary at the natural seam.
- **DONE format mirrors TODO format** — DONE H3 headings carry `FR-N (severity)` so the two ledgers are scannable in the same shape. Harmonised in PR #163.

---

## Backlog totals

Active backlog at the time of this reorganization (post PR #229):

- **P1 (urgent quality)**: 14 items (8 H[critical] + 6 H).
- **P2 (substantive improvements)**: ~30 items (Medium fitness findings + Phase 2 clusters + BYOD + relocations).
- **P3 (low-priority cleanup)**: ~16 items.
- **P4 (adopter experience)**: 5 items (sharable skill, effort-sizing, version-upgrade procedure, language coverage, S1/S2/S3 gates).
- **P5 (content expansion)**: 8 subsections (5.1-5.8) with multiple country/regulator items each.
- **P6 (domain-level)**: 5 items (6.1-6.5).
- **P7 (awaiting decision)**: 3 active decisions + 2 dropped-decision audit-trail entries.

---

## Notes on maintenance

- Add new items at the appropriate priority. Move items between priorities as context changes (e.g., severity escalation may move an item from P2 to P1).
- When an item is completed, delete it from this file (no strikethroughs, no `[done]` suffixes) and add an entry to [`.working/DONE.md`](.working/DONE.md) in the same PR. The rotation discipline is documented in the PR-finalization-protocol section of [`.claude/rules/governance/change-tracking.md`](.claude/rules/governance/change-tracking.md).
- Design decisions (working-state conventions, audit-programme architecture decisions, decisions explicitly dropped) belong in [`.working/design-decisions.md`](.working/design-decisions.md), not in TODO. The "Decisions explicitly dropped" subsection of P7 cross-references those decisions for audit-trail completeness without duplicating the rationale.
- Sub-items can be promoted to their own priority section if scope grows.
- This file is the source of truth for what's queued; conversation history is not.
- Fitness-review backlogs (currently `.working/fitness-reviews/2026-06-21-r1.md` and `.working/fitness-reviews/2026-06-22-r1.md`) remain the authoritative per-finding evidence source; this file is the action-organized view. The two are kept in sync at fitness-review-cycle time, not continuously.
