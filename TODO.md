# TODO

Forward-looking backlog of planned enhancements for the GRC Documentation Library. Items are added when identified and rotated out when completed. Completed items move to [`.working/DONE.md`](.working/DONE.md) (closed-TODO ledger, keyed by original backlog ID); historical change detail lives in [`CHANGELOG.md`](CHANGELOG.md). This file holds only pending and queued items.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions, with one narrow exception: [`tools/lint-todo-staleness.py`](tools/lint-todo-staleness.py) (gate 45) scans this file for two specific drift shapes (queued PR already merged, sweep cursor behind history). All other audit gates skip this file. The other repository-root meta files that share the broader exemption are [`CHANGELOG.md`](CHANGELOG.md) (a chronological log that mutates with every PR) and [`instruction-ai-document-ingestion.md`](instruction-ai-document-ingestion.md) (an AI system prompt, not a governance document). As of `2026-06-02`, [`README.md`](README.md), [`NOTICE.md`](NOTICE.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SECURITY.md`](SECURITY.md), [`AUTHORS.md`](AUTHORS.md), and [`docs/worked-example.md`](docs/worked-example.md) each carry the canonical 13-field metadata block and are validated by the corpus metadata audit (gate 1).

---

## Session resume metadata

These are **as-of-session-pause snapshots**, not "current HEAD" claims. They reflect the state at the moment this section was last refreshed. The version snapshot and last-validation-sweep cursor each drift forward as the project advances — that drift is expected and not a defect. Gate 45 (TODO staleness audit) catches genuine staleness shapes (queued PR already merged; sweep cursor behind history); other drift is informational.

- **Branch at last refresh**: `main` (synced after PR #174 merge).
- **Library version as of last refresh**: `2026.06.154`. **Pack version**: `1.35.0`. **README version**: `1.9.25`.
- **Audit programme**: all gates passing on `main` as of last refresh.
- **Last validation sweep**: Sweep 15 iteration 1 (close-out PR #167).

---

## Queued sequence (upcoming PRs)

Fitness-remediation PRs are now in flight under maintainer direction. PRs #142-#172 have closed 34 findings to date (most recently PR #169 FR-26+27+28, PR #172 FR-4+5+6+7+8 as the Phase 1 README polish bundle that closes Rec-6 from the fitness review; plus the meta-PRs #163 DONE format harmonisation, #170 CLAUDE.md version-bump rule, #171 CLAUDE.md subscription discipline, and Sweep close-outs #148/#154/#160/#167). The next batch is chosen from the Fitness review backlog section below in highest-certainty order; the assistant picks 1-8 at a time (per the amended validate-cadence rule), runs a research-assistant pipeline (workers produce research files; orchestrator authors all final prose) to prepare drafts in parallel, applies serially with CI gating, and runs `/validate` after each batch. Maintainer direction supersedes the assistant's pick at any time.

Open large items still queued explicitly:

- **FR-14** (maturity-ladder reconciliation, library-wide CMMI propagation): touches `governance/framework-governance-performance-and-improvement.md`, `docs/template-maturity-self-assessment.md`, `governance/register-digital-trust-and-assurance-metrics.md`. Likely a multi-PR batch; flagged for the maintainer to schedule deliberately rather than picked into a routine 5-PR batch.
- **FR-44-generalisation**: corpus-wide harmonisation of legacy "shall" → "must" outside external-standard quotations. Routine cleanup batch, scheduled after the high-priority backlog is closed.

---

## Fitness review backlog (from r1, Pass-2 confirmed in PR #141)

Source: [`.working/fitness-reviews/2026-06-21-r1.md`](.working/fitness-reviews/2026-06-21-r1.md) — see its Page-by-Page Findings section for per-finding evidence and its Pass-1 / Pass-2 Verification Results sections for the verdict tables. Verified via Pass-1 (PR #140) + Pass-2 (PR #141). Each item carries its `FR-<n>` ID; refer to r1.md for the full per-finding evidence.

**Status legend:** entries marked `⚠️` carry the orchestrator's modification framing from Pass-1 (see r1.md §8.5 for the modification note). Entries marked `(reshape)` were reshaped during Pass-2 from their original framing.

**Severity-tier prioritization (per Pass-2 decision):** High[critical] / High / Medium are immediate-priority. Low is deferred to a later routine cleanup cycle.

**No remediation work has begun.** This section is the maintainer's review surface for prioritization. Each FR-N becomes its own (or grouped) PR at the maintainer's direction.

### Special: FR-14 — Maturity-ladder reconciliation, library-wide CMMI propagation

Resolved from `🤔` to `✅` in Pass-2 with a library-wide propagation plan:

- Reconcile to **CMMI 5-tier** (Initial / Managed / Defined / Quantitatively Managed / Optimized). The authoritative source.
- Concrete scope:
  - `governance/framework-governance-performance-and-improvement.md` — already CMMI; baseline. No change unless audit surfaces drift.
  - `docs/template-maturity-self-assessment.md` — rename Tier 2 "Managed" (currently "Developing") and Tier 4 "Quantitatively Managed" (currently "Managed") back to CMMI canonical.
  - `governance/register-digital-trust-and-assurance-metrics.md` — replace the 4-tier DTI variant (Developing/Managed/Integrated/Optimized) with CMMI 5-tier.
- Forward-looking convention: prevent future divergence. Candidate mechanisms:
  - New audit gate: prose-scan for maturity-tier vocabulary against CMMI canonical names.
  - Or a documented standard in `governance/` (`standard-maturity-tier-vocabulary.md`) that other documents cite.
- Severity: High[critical] (was high[critical]). Originating run: r1.

### High[critical] tier — 10 findings (immediate priority)

- **FR-14** (maturity ladder): see Special section above.
- **FR-30** (privacy + supply-chain): No standalone Article 28 DPA template. Ship `privacy/template-dpa-article-28.md`.
- **FR-31** (privacy): Privacy by Design (Article 25) has no operational artefact. Ship `privacy/framework-privacy-by-design.md` mapping seven foundational principles to architecture/dev-security workflows.
- **FR-32** (privacy): No Legitimate Interest Assessment template. Ship `privacy/template-legitimate-interest-assessment.md`.
- **FR-33** (`privacy/procedure-privacy-impact-and-cross-border-transfer.md`): Article 36 prior-consultation pathway absent. Add §Step 5 pathway distinct from internal ERC approval.
- **FR-34** (privacy): Transfer Impact Assessment methodology referenced but defined nowhere. Ship `privacy/template-transfer-impact-assessment.md` with EDPB Recommendation 01/2020 six-step methodology. (Consolidates with FR-74.)
- **FR-70** (crypto-asset / blockchain governance): Domain entirely absent. Ship dedicated governance content covering digital-asset custody, staking, smart-contract risk, blockchain platform vetting. DORA, MiCA, NYDFS BitLicense.
- **FR-71** (M&A due diligence): `procedure-grc-programme-management-and-annual-review.md` names M&A as trigger but no checklist/pre-close template/integration playbook. Ship dedicated procedure.
- **FR-72** (sanctions/OFAC/export control): Superficial. Ship dedicated framework with UBO verification + denied-party-list integration.
- **FR-73** (AI ethics review): `charter-ai-governance-council.md` collapses ethics into the compliance/risk body. Separate ethics panel or independent challenge mechanism needed.

### High tier — 5 findings (immediate priority)

- **FR-36** (`privacy/framework-childrens-data.md` + EU annex): EU member-state per-state Article 8 age table missing.
- **FR-58** (multiple): No inheritance vocabulary (library-internal vs template vs reference content).
- **FR-59** (privacy jurisdictions): Annexes too shallow for operational sufficiency.
- **FR-60** (`compliance/healthcare`): HIPAA adopter has no operational detail beyond a single 261-line sector annex.
- **FR-61** (`compliance/financial-services`): FS adopters outside EU/US lack regulatory regimes (UK PRA/FCA, US OCC/FRB/FDIC, MAS, FSA, APRA, OSFI, HKMA, FINMA).

### Medium tier — 48 findings (immediate priority)

Full list with one-line summaries available in r1.md §3 (`.working/fitness-reviews/2026-06-21-r1.md`). Grouped by topical cluster:

- **ERM standard** (2): FR-11 (Risk Owner not defined as distinct role), FR-12 (treatment vocabulary divergence).
- **Maturity ladder methodology** (1): FR-15 (median-of-medians scoring suspect).
- **Exception policy** (1): FR-18 (180-day default not traceable to normative source).
- **Audit evidence template** (1): FR-23 ⚠️ (assembler-verification standard absent).
- **Control testing** (2): FR-24 (procedure thinner than peers), FR-25 (5y retention below SOX 7y).
- **Privacy completion** (6): FR-37 (joint controller Art 26), FR-38 (DSAR Art 12(5) thin), FR-39 (EU representative Art 27), FR-40 (PIPL Art 38-40), FR-41 (AI Art 22 + EU AI Act + FRIA workflow), FR-42 (DPO independence Art 38(3)).
- **Editorial consistency** (7): FR-46 (role-name "Chief" inconsistency), FR-47 (DPO ambiguous role), FR-48 (H2 numbering patterns drift), FR-49 (Governance heading drift), FR-50 (NIST citation format drift), FR-51 ⚠️ (ISO 27001 Annex-form drift), FR-52 (review frequency "and" vs "or").
- **Adopter cluster** (5): FR-62 (AI jurisdiction annexes absent), FR-63 (worked example walks ingestion not adoption), FR-64 (contribution path workflow-shaped not pattern-shaped), FR-65 ⚠️ (upstream-sync underspecified), FR-66 (tooling assumes maintainer context).
- **Coverage gaps** (6): FR-74 (Schrems II-light; consolidates with FR-34), FR-75 ⚠️ (ESG materiality threshold), FR-76 ⚠️ (sustainability framework escalation triggers), FR-77 (3LoD model used without explanation), FR-78 (framework-document-architecture maintainer voice), FR-79 (ITSM portal tool-leakage).
- **Cross-document contradictions** (2): FR-81 (TLS floor inconsistency), FR-82 (key hashing ambiguity).
- **Operational/runbook** (1): FR-83 (IC checklist absent).
- **Security-content refinement** (2): FR-87 (SSRF range list incomplete), FR-88 (cipher suite enumeration missing).
- **KRI/KPI** (2): FR-93 (KRI escalation owner missing), FR-94 (Linked controls assume control register).
- **Cross-framework matrix** (2): FR-97 (ISO 31000 clause numbering), FR-98 (NIS 2 annex evidence-class column).
- **Continuous-assurance / 3LoD** (4): FR-99 ⚠️ (per-control effectiveness metrics), FR-100 (cloud baseline cites families not sub-controls), FR-101 ⚠️ (closure sign-off authority implicit), FR-102 (change management binary).
- **Newcomer** (4): FR-104 ⚠️ (decision-tree per-regulation context), FR-105 (ISMS framework-citation ordering), FR-106 (trade-programme acronym cluster), FR-110 (document-index as primary navigation).

### Low tier — 14 findings (deferred to later routine cleanup cycle)

Cross-reference only. No immediate-priority action; queue for a routine cleanup PR when convenient.

- **Adopter edge cases** (3): FR-67 (zero-headcount-with-contractor), FR-68 ⚠️ (mandatory-except-when-not), FR-69 (three baseline sizes).
- **Operational/runbook detail** (3): FR-84 (regression testing checklist as artefact), FR-85 (per-question owner in breach response), FR-86 ⚠️ (recovery runbook crisis-comms cross-reference — Pass-1 noted the runbook itself was hard to locate; revisit at remediation time).
- **Security low-impact** (3): FR-89 (JWT algorithm-key-type binding), FR-90 (CSP/Trusted Types/HSTS-preload guidance), FR-91 (webhook constant-time comparison).
- **Newcomer low-impact** (4): FR-107 (glossary surface earlier), FR-108 (Key Terms vs Glossary cognitive hop), FR-109 ⚠️ (charter purpose paragraph density), FR-111 ⚠️ (Tier 1 reading-time estimate).
- **Metadata field unification (reshape, downgraded)** (1): FR-53 (reshape) — evaluate whether to deprecate Classification or Confidentiality as redundant metadata, or document the semantic distinction.

### Backlog totals

- 10 + 5 + 48 = **63 immediate-priority findings** (High[critical], High, Medium tiers)
- **14 deferred** (Low tier)
- **77 open** (34 closed across PRs #142-#172). Total surfaced in r1: 111.

### FR-44 follow-up

The FR-44 convention statement is now documented (PR #159, master spec §6.1). A corpus-wide harmonisation of legacy "shall" → "must" occurrences is left as a separate FR-44-derivative item:

- **FR-44-generalisation**: corpus-wide sweep replacing legacy "shall" / "shall not" in normative prose with "must" / "must not" where the verb is not a direct quotation of an external standard. Per file: small but numerous. Owner: maintainer. Schedule: routine cleanup batch after the immediate-priority backlog is closed.

---

## Other queued moves (small PRs preferred per maintainer)

Files identified earlier as project-specific application that should move from `governance/` or `tools/` to `.working/`. Each as its own small PR:

- **`tools/sweep-preflight-exemptions.json`** → likely `.working/validate-sweeps/preflight-exemptions.json` (co-located with the validate-sweeps activity since that's what the file is for). Maintainer-curated false-positive memory for OUR project's specific false positives; adopters will curate their own.
- **Citation-verification cluster** (6 files): `register-citation-verifications.md` + `register-citation-verification-bundle.md` + four `worklist-citation-verification-batch-*.md` files. → `.working/citation-verifications/` following the canonical layout. Project-specific in-flight verification campaign for OUR citations (Phase 23.6 work).
- **`governance/register-main-branch-protection.md`** → `.working/` somewhere. Snapshot of THIS repo's branch protection; meaningless to adopters who configure their own.

Each requires updating the document-index, sibling references, regenerating taxonomy/portal, version bumps, CHANGELOG entry.

---

## BYOD policy: add MDM vs MAM option (maintainer-directed)

Maintainer feedback: [`security/policy-byod.md`](security/policy-byod.md) currently treats personal-device access as a single category. The policy should be expanded to explicitly distinguish two enforcement models:

- **MDM (Mobile Device Management)**: organisation manages the entire device. Higher visibility (organisation sees device-wide telemetry, can wipe the device, can enforce device-level policy) but creates privacy concerns for personnel because the organisation gains visibility into non-work-related device contents.
- **MAM (Mobile Application Management)**: organisation controls a container holding organisational applications and data. Container-level policy applies (encryption, password, remote wipe of the container only); device-wide privacy is preserved for the personnel.

Adopting organisations should be able to choose MDM, MAM, or both depending on context (target personnel population, device categories, regulatory environment, data classification). The policy should:

1. Define both options with their visibility and privacy implications spelled out.
2. Let the adopter choose one or both for their context.
3. Note that the choice can vary by personnel group (e.g., MDM for company-issued devices used for high-classification data; MAM for personal devices used for general business communications).
4. Cross-reference the data-classification standard so the choice is tied to the level of data accessed.

Owner: maintainer. Effort: small (single policy file expansion, table-driven). Schedule: a future small PR.

---

## Pack: dev-security/claude-rules language coverage review

Review the language-specific security rules in [`dev-security/claude-rules/`](dev-security/claude-rules/) (currently the `python.md` family plus the external overlay rules from TikiTribe, Kariedo, addyosmani). Two questions to answer:

1. **Are mainstream languages missing?** Today the pack ships Python-focused guidance. Candidates likely worth at least a starter file: JavaScript / TypeScript (Node and browser surfaces), Go, Java / Kotlin, Rust, C# / .NET, Swift / Kotlin (mobile). Decide which subset belongs in a GRC-baseline pack vs which the pack should defer to dedicated technical-security sources.
2. **Should we explicitly reference dedicated technical-security projects** rather than try to be one? The library's positioning is GRC-oriented: we want enough language-specific baseline information to help an adopter who needs immediate guardrails, but the corpus is not the authoritative source for, e.g., browser XSS prevention or memory-safe Rust idioms. Decide whether to add a "for deeper coverage, see ..." pointer (OWASP cheat sheets, language-specific SAST rule packs, vendor secure-coding guides) and where it lives.

Scope: one or more small PRs that each add a language baseline file or update the pack's README to set the positioning. Owner: maintainer. Effort: small per language (mirror `python.md`'s shape: prohibitions, required patterns, framework alignment table).

---

## Backlog-listing process: effort-sizing labels (post-FR-backlog meta-improvement)

Maintainer-directed process improvement, deferred until the current FR backlog is closed.

**Problem**: when a fitness review or sweep produces a multi-item backlog, items currently land in TODO with severity (High[critical] / High / Medium / Low) but no estimate of work effort. The 2026-06-21 mid-batch prioritisation exercise showed that effort estimates are needed alongside severity to make sequencing decisions (a Medium-severity XS item can ship in a bundle of 5; a High[critical] XL item warrants its own multi-PR campaign).

**Proposed convention**: at item-add time, each backlog item gains an effort label per the following scale, stored in TODO and surfaced in the same shape as severity:

| Label | Per-item effort | Bundleable per PR |
|---|---|---|
| **XS** (single-line / single-cell) | 5-15 min | 5-10 items |
| **S** (single-doc section add) | 30-90 min | 2-4 items |
| **M** (multi-doc, bounded) | 2-4 hrs | 1 item |
| **L** (new artefact, multi-doc propagation) | 4-8 hrs | 1 item |
| **XL** (new domain, library-wide reshape) | 1-3 days | 1 item, may split |

**Format suggestion** (mirroring DONE's FR-N (severity) heading shape from PR #163): item bullets become `**FR-N (severity, XS)**: description`. The two tags are independent — a High[critical] item can be XS (one-cell fix) or XL (new domain); a Low item can be S (clarification) or M (sweep).

**Surfaces to update when the convention lands**:
1. `dev-security/claude-rules/skills/library-fitness-review/SKILL.md` — Pass-1 instructions add effort-sizing alongside severity-tagging.
2. `dev-security/claude-rules/skills/validation-sweep/SKILL.md` — sweep-finding shape gains an effort-label slot.
3. `TODO.md` — fitness-review backlog format documents the convention.
4. `.working/DONE.md` — heading shape extends to `### PR #N — FR-X (severity, effort): title`.
5. Future fitness-review templates and sweep detail files use the convention by default.

**Owner**: maintainer. **Effort**: M (skill-file edits, format-convention statement, retrofit of existing surfaces). **Schedule**: after the current FR backlog is closed (85 → 0 items). Capturing now so the convention is documented before the next fitness review produces a new batch.

---

## Standard-version-upgrade process (maintainer-directed)

Maintainer-directed deliverable: when an external standard the corpus cites is republished at a new version (e.g., `ISO/IEC 27001:2013` → `ISO/IEC 27001:2022`; `ISO/IEC 27701:2019` → `ISO/IEC 27701:2025`; `COBIT 2019` → a future COBIT release), the library needs a documented process to transition. Sweep 15's `ISO/IEC 29134:2023` hallucination plus the FR-21 work that caught `ISO/IEC 27701:2019 → 2025` show that ad-hoc citation-by-citation updates produce drift; a systematic process is needed.

The process must cover, at minimum:

1. **Diff between old and new version.** Capture what the standard changed: renamed clauses, deleted controls, added controls, restructured numbering. Many standards publish a "transition guide" or an annex listing the changes; treat the publisher's transition guide as authoritative input.
2. **Look up all references in the corpus.** Mechanical sweep (grep + canonical-citations register) to enumerate every document, register row, and CHANGELOG entry that cites the old version. Output a worklist.
3. **Assess content based on the old version.** For each cited location, determine whether the citation is purely positional (a reference to the standard exists, no content drift) or substantive (the corpus content quotes, restates, or maps to old-version clauses/controls that have changed). Classify each as positional-only or substantive.
4. **Systematic update to new-version compliance.** Apply the changes per classification:
   - Positional-only: update the year/version in the citation; no content change.
   - Substantive: rewrite the affected content to match the new-version requirement; track the rewrite as its own per-document version bump.
5. **Update the canonical citations register and verifications register.** Add the new version with publisher-source verification; mark the old version as superseded with an effective-date.
6. **Audit-gate integration.** The standards-currency linter (`tools/lint-standards-currency.py`, gate 27) should flag superseded versions; the canonical-citations register entry is what makes that gate see the supersession.
7. **Communication.** A CHANGELOG entry covering the upgrade campaign (often multi-PR); a TODO row tracking outstanding substantive rewrites if they don't all fit in one PR.

**Deliverable**: a procedure document at `governance/procedure-standard-version-upgrade.md` (or similar path) that documents the seven-step process above, with worked examples (e.g., ISO/IEC 27001:2013 → 2022 if applicable; ISO/IEC 27701:2019 → 2025 retrospective). Owner: maintainer. Effort: M (one new procedure document, citation-register cross-references, possibly an audit-gate enhancement to flag the supersession class systematically). Schedule: after the FR backlog completes (will be more valuable when the corpus is stable than during in-flight remediation).

**Side benefit**: the procedure also documents the canonical-citations register discipline (which exists but has not been formally written down as a process), so future contributors understand why citations should be entered in the register before being introduced into corpus prose.

---

## Critical user feedback to remember across sessions

Durable behavioural guidance from the maintainer. Each item links to its operationalisation where one exists.

- **"More PRs, keep each one clean"** — favor small focused PRs.
- **"I prefer /validate, not /validation-sweep"** — short slash commands; skill names stay descriptive.
- **"Don't explicitly name or link `.working/`"** in template-content files that adopters see (e.g., the root CHANGELOG header note for the changelog split).
- **"Inference must be validated before committing or before anything else uses that information"** — operationalised in the 7th pack rule [`validate-inference-before-action.md`](dev-security/claude-rules/governance/validate-inference-before-action.md).
- **Activity directories should be self-contained** — operationalised in the canonical `.working/<activity>/` layout.
- **Zero-finding sweeps still need history rows but no detail files** — operationalised in [`SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) step 9 of the validation-sweep skill.
- **Sweep history is project-application, not template content** — operationalised by keeping the history file in `.working/`.
- **TODO is forward-looking; historical state rotates to DONE.md** — operationalised in [`change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) PR-finalization-protocol section.
- **After completing a merge, list the upcoming next 5 planned PRs from TODO** — operationalised in [`.claude/CLAUDE.md`](.claude/CLAUDE.md) PR-workflow section and the same pack rule.
- **Validate cadence is 1-8 PRs per batch, not strictly 5** — original standing rule was "after each 5 PRs perform a validate". Maintainer subsequently authorised wider tolerance: a logical-grouping batch may be smaller (down to 1 PR if it's large enough to warrant its own validate) or larger (up to 8 PRs if the items fit a coherent thread). The 5-PR cadence remains the default; the maintainer (or the assistant in maintainer's authorised autonomous mode) chooses the batch boundary at the natural seam.
- **DONE format mirrors TODO format** — DONE H3 headings carry `FR-N (severity)` so the two ledgers are scannable in the same shape. Operationalised in [`.working/DONE.md`](.working/DONE.md) "How items get here" §, harmonised in PR #163.

---

## Open follow-ups from validation sweeps (deferred items not yet closed)

Pre-dates the dating-discipline convention (2026-06-20) so no `surfaced` / `re-triage-by` stamp. From [`.working/validate-sweeps/history.md`](.working/validate-sweeps/history.md):

- **Sweep 3 follow-up**: cross-document term-and-identifier consistency gap. The prose-and-numbering-shaped C3 surface that mechanical gates 35/39/41 don't cover. Candidate for a future mechanical gate.

---

## Priority 4 — adopter experience

### 4.6 Corpus-management discipline as a shareable skill

Package the cumulative documentation-and-corpus discipline this project has accumulated as a standalone Claude Code skill that anyone managing a documentation corpus with an AI coding assistant could install. Scope and shape (to be refined when work begins, after the fitness backlog is closed):

- **Trigger surface**: users running Claude Code against a structured Markdown corpus (governance, policy, technical-spec libraries) who want the same disciplines that have prevented drift in this project: metadata blocks, audit gates, generator-output drift checks, version monotonicity, change-tracking conventions, sweep-style validation, fitness-style periodic review.
- **Distillation**: the seven `governance/` pack rules (gate-discipline, change-tracking, evidence-grounded-completion, clarify-before-acting, artefact-and-branch-discipline, action-before-explanation-of-inaction, validate-inference-before-action) form the discipline core. The `validation-sweep` and `library-fitness-review` skills form the periodic-review surface. The audit-programme architecture (`tools/lint-*.py` + four-surface wiring + regression fixtures) forms the mechanical-enforcement surface.
- **Generalisation**: the patterns are corpus-shape agnostic but reference GRC-specific document types. The shareable form would carry the patterns and discipline (what to enforce, why, how) without the GRC-specific control-set citations. Adopters would supply their own document-type model and metadata-field set.
- **Format**: a skill (or skill family) under `dev-security/claude-rules/skills/` with a top-level `corpus-management-discipline/` directory; mirrors the existing pack-shipping shape.
- **Sequencing**: starts after the fitness backlog (FR-1 through FR-111) is closed, since some of the discipline is still being calibrated against the backlog and the calibration informs what to ship.
- **Open questions to resolve at work-start time**: whether to ship as one omnibus skill or a family of smaller skills; whether to include linter scaffolds (stdlib-only Python templates adopters can adapt) or stay prescriptive-only; whether to ship under the existing pack (1.x bump) or as a new pack with its own version line.

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

## Notes on maintenance

- Add new items at the appropriate priority. Move items between priorities as context changes.
- When an item is completed, delete it from this file (no strikethroughs, no `[done]` suffixes) and add an entry to [`.working/DONE.md`](.working/DONE.md) in the same PR. The rotation discipline is documented in the PR-finalization-protocol section of [`.claude/rules/governance/change-tracking.md`](.claude/rules/governance/change-tracking.md).
- Design decisions (working-state conventions, audit-programme architecture decisions, decisions explicitly dropped) belong in [`.working/design-decisions.md`](.working/design-decisions.md), not in TODO.
- Sub-items can be promoted to their own priority section if scope grows.
- This file is the source of truth for what's queued; conversation history is not.
