# TODO

Living backlog of planned enhancements for the GRC Documentation Library. Items are added when identified and removed when completed. Completed work is recorded in [`CHANGELOG.md`](CHANGELOG.md); this file holds only pending and queued items.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions. The other repository-root meta files that share this exemption are [`CHANGELOG.md`](CHANGELOG.md) (a chronological log that mutates with every PR) and [`instruction-ai-document-ingestion.md`](instruction-ai-document-ingestion.md) (an AI system prompt, not a governance document). As of `2026-06-02`, [`README.md`](README.md), [`NOTICE.md`](NOTICE.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SECURITY.md`](SECURITY.md), [`AUTHORS.md`](AUTHORS.md), and [`docs/worked-example.md`](docs/worked-example.md) each carry the canonical 13-field metadata block and are validated by the corpus metadata audit (gate 1).

---

## Priority 4 — adopter experience

### 4.1 Quickstart templates per adopter profile

Debating the value of pre-configured starter sets for common adopter profiles:
- Small business (under 50 employees, single jurisdiction)
- Mid-market regulated industry (50-500 employees, sector compliance)
- Multi-national enterprise (500+ employees, multiple jurisdictions)
- Public-sector adopter
- Healthcare adopter
- Financial-services adopter

### 4.2 Maturity assessment interactive template

The current [`docs/maturity-scorecard.md`](docs/maturity-scorecard.md) is auto-generated and static. An interactive form (spreadsheet or guided markdown checklist) lets an adopter self-assess.

### 4.3 Implementation roadmap templates

90-day, 180-day, and one-year implementation roadmaps per adopter profile. Maps to a phased rollout of library artefacts.

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

## Pack and tooling extension

### Post-S.3 evaluation of the Claude Code Skills format

Phase S.3 (library version `2026.06.20`, shipped 2026-06-19) introduced three Claude Code Skills in the [`dev-security/claude-rules/skills/`](dev-security/claude-rules/skills/) subdirectory: [`skills/evidence-grounded-completion/`](dev-security/claude-rules/skills/evidence-grounded-completion/), [`skills/gate-discipline-diagnose/`](dev-security/claude-rules/skills/gate-discipline-diagnose/), and [`skills/clarify-before-acting/`](dev-security/claude-rules/skills/clarify-before-acting/). Phase S.4 (library version `2026.06.21`) added gate 31 ([`tools/lint-skill-derives-from.py`](tools/lint-skill-derives-from.py)) enforcing the derive-and-cite contract between each skill and its canonical pack rule.

The post-S.3 question, recorded here so it does not get lost: should additional pack rules be wrapped as skills, and if so, which?

**Decision trigger.** At the next time the maintainer touches the skills pack (an additional pack version bump, a refactor of one of the three existing skills, or the annual tooling review under [`governance/procedure-library-quality-and-review-cadence.md`](governance/procedure-library-quality-and-review-cadence.md) §7, whichever comes first), evaluate this item. The trigger is intentionally not calendar-bound: the project's work pace is uneven and a fixed-date evaluation risks either a premature decision (insufficient invocation evidence) or a forgotten one (no scheduled prompt).

**Empirical evidence to weigh at the trigger.**

- Has Claude Code's Skill discovery surfaced the three existing skills when their triggers were met? (Mechanical check: did the assistant invoke the relevant skill, or did it execute the workflow without surfacing the skill?)
- When invoked, did each skill's Process steps produce behaviour consistent with the canonical pack rule, or did the maintainer judge the skill's wording to be diverging from the rule? (Semantic check; gate 31 enforces reference integrity but not semantic drift.)
- Did the skill format require refactor during the observation period (header order, frontmatter fields, section names)? Format-altering PRs against any of the three skills are evidence that the format is not yet stable.
- Subjective maintainer judgement: were the skills useful, redundant, or noise?

**Candidate rules and selection criterion.**

Two pack governance rules remain unwrapped as skills and have workflow-shaped content suitable for the Skills format:

- [`governance/change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) — candidate skill name: `change-tracking-write-entry`. Workflow: at the moment of writing a CHANGELOG entry or applying a `Changelog: skip` trailer, follow the rule's procedure (entry must contain date+version header, structured Keep a Changelog sections, file references as markdown links, "why" not just "what", verification evidence, phase context).
- [`governance/artefact-and-branch-discipline.md`](dev-security/claude-rules/governance/artefact-and-branch-discipline.md) — candidate skill name: `artefact-discipline-check` (or similar). Workflow: when CI flags generated-artefact drift or a protected-branch operation is about to occur, follow the rule's procedure (regenerate from the source rather than hand-edit; PR-only mergers to protected branches; no force-push to protected branches).

The other rules in the pack (`secrets`, `python`, `input-validation`, `cicd-gates`, and the pack `gate-discipline` / `evidence-grounded-completion` / `clarify-before-acting` rules that are already wrapped) are either pre-development reference material (not workflow-shaped) or already represented as skills.

The selection criterion at the decision point is:

1. Which of the two candidates has had its failure mode most often observed during the observation period? (Frequent observed failures argue for the lighter-weight skill invocation surface.)
2. Which has Process steps that are clearly invocable as a workflow rather than as a reading exercise? (Workflow-shape is the format's strength; if the rule is best consumed as prose, a skill adds noise.)
3. Has the maintainer encountered a real misstep that a skill would have caught? (Concrete evidence beats hypothetical fit.)

**Possible outcomes at the trigger:**

- Add one candidate (the stronger of the two) — ship it as a new SKILL.md with the same derive-and-cite contract enforced by gate 31.
- Add both — only if both candidates clear the criterion above.
- Add neither — the three existing skills are sufficient; the additional skills would add discovery noise without benefit. This is a valid outcome and is recorded as such if chosen.
- Defer — insufficient evidence at the trigger; re-evaluate at the next trigger occurrence.

**Cross-references.** Phase S.3 and S.4 are recorded in [`CHANGELOG.md`](CHANGELOG.md) under library versions `2026.06.20` and `2026.06.21` respectively. The pack itself is versioned independently in [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) (currently `1.20.0`).

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

Decision: ship as scaffold (regex framework with unit normalisation and aggregation, conservative initial term set narrow enough to currently track 0 terms). The linter passes vacuously; the framework is in place for future term curation when the maintainer is ready to define which specific (term, SLA-dimension) pairs to enforce. Honest scope management was preferred over either (a) silently producing false positives or (b) defining the term set without sufficient operational data.

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
