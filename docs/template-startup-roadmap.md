# Adopter Startup Roadmap Template

**Document Title:** Adopter Startup Roadmap Template\
**Document Type:** Template\
**Version:** 2.1.0\
**Date:** 2026-06-21\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`docs/template-quickstart.md`](template-quickstart.md), [`docs/adopter-guide.md`](adopter-guide.md), [`docs/decision-tree.md`](decision-tree.md), [`docs/maturity-scorecard.md`](maturity-scorecard.md), [`docs/template-maturity-self-assessment.md`](template-maturity-self-assessment.md), [`README.md`](../README.md), [`docs/worked-example.md`](worked-example.md)\
**Classification:** Public\
**Category:** Adopter Experience\
**Review Frequency:** Annual, and on material change to the library's domain structure or sector-conditional content\
**Repository Path:** [`docs/template-startup-roadmap.md`](template-startup-roadmap.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template helps an adopter compose a starting set of library artefacts from a small core baseline plus stacking modules. The composition matches what the organisation actually does (its activities, data scope, audience, regulatory exposure, and GRC team capacity), rather than a pre-set profile by company size or sector.

This is the long-form composition workbook. Readers who want a two-minute on-ramp first should start with [`docs/template-quickstart.md`](template-quickstart.md); this roadmap is the next step after the quickstart, for adopters ready to work through the full module catalogue.

### Where this fits among the adopter entry points

The canonical front door for adopters is [`docs/portal.md`](portal.md) (audience-keyed grouping by role). This template is one of four deeper-dive paths that branch off the portal; it answers "how do I compose the full starting set across activity, data, audience, regulatory exposure, and capacity?". The other three are [`docs/adopter-guide.md`](adopter-guide.md) (fork-and-adapt principles), [`docs/decision-tree.md`](decision-tree.md) (sequenced reading order), and [`docs/template-implementation-roadmap.md`](template-implementation-roadmap.md) (calendar phasing). For the two-minute on-ramp version, see [`docs/template-quickstart.md`](template-quickstart.md). The portal's "Other entry points and when to use them" table picks the right path by question; see the portal Overview.

The aim is to compress the adopter's first-week question (`which of the 11 domains do I need on day one?`) into: copy the core baseline, then add the modules that match the organisation. The [`docs/decision-tree.md`](decision-tree.md) covers the conditional logic; this template names the resulting compositions.

A composition is a starting point, not a final scope. Adopters typically grow into adjacent modules as the programme matures; the [`docs/adopter-guide.md`](adopter-guide.md) section "Maturity progression" describes the standard growth path.

---

## Scope

This template applies to organisations adopting the library for the first time and to organisations consolidating an existing adoption against this library's structure.

The composition shape (core baseline plus stacking modules) replaces the earlier per-profile categorisation. Categorical profiles (small business, mid-market, multi-national, etc.) were tested against real adopter shapes and found too rigid: real organisations sit across categories, and the same category contains very different operational realities. Activities, data, audience, regulatory exposure, and team capacity are the dimensions that actually drive what an organisation needs from the library.

Out of scope: bespoke profile shapes marked Out of scope in [`governance/register-coverage-gaps.md`](../governance/register-coverage-gaps.md) §1 (defence and aerospace, mining, agriculture, etc.). Adopters whose shape is materially different from anything composable here should consult the decision tree directly.

---

## The core baseline

Every adopter copies this set on Day 1, regardless of size, sector, or maturity. The reasoning: every organisation has staff data, IT, vendors, and the possibility of an incident. The baseline is the floor below which the programme cannot be defended.

| Domain | Artefact | Why it is in the baseline |
| --- | --- | --- |
| `governance/` | one foundational policy (e.g. [`security/policy-information-security.md`](../security/policy-information-security.md) or equivalent) | A single overarching policy that names the organisation's posture and the owner of that posture. |
| `security/` | [`policy-acceptable-use.md`](../security/policy-acceptable-use.md), [`policy-identity-and-access-management.md`](../security/policy-identity-and-access-management.md), [`procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) | The three documents that the largest share of incidents touch. |
| `privacy/` | [`policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md) plus the home-jurisdiction annex from [`privacy/jurisdictions/`](../privacy/jurisdictions/) | Even an organisation that does not collect customer data has staff data; the home-jurisdiction privacy law is the floor. |
| `risk/` | [`procedure-risk-register.md`](../risk/procedure-risk-register.md), with the register populated with the actual top 10 risks | A short, real risk register beats a long imagined one. Populating it is part of the baseline; copying an empty template is not. |

The baseline is six artefacts. An organisation that has copied and customised these six has a defensible floor. Layer modules on top.

---

## How to use the modules

Modules are organised in five dimensions. For each dimension, identify which modules apply to your organisation and copy the artefacts each module names. Modules are additive (you can pick more than one in each dimension); they are also independent (you can pick A2 without A1 if you ship external-facing SaaS but do not build it in-house).

| Dimension | Question to ask |
| --- | --- |
| A. Activity | What do we do? |
| B. Data scope | What data do we handle? |
| C. Audience | Who do we serve? |
| D. Regulatory exposure | Who regulates us? |
| E. GRC team capacity | How much can we maintain? |

Dimension E (capacity) scales every other module: an organisation with a one-person GRC function copies the minimum viable subset of each chosen module; an organisation with a department copies the full set plus measurement infrastructure.

---

## Module catalogue

### Dimension A: Activity (what we DO)

#### A1: We build software in-house (custom internal development)

Triggered by any in-house software development, including internal tools, automation, scripting, infrastructure-as-code, and customisation of off-the-shelf platforms.

Adopt:
- [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md): the floor for any internal development.
- [`dev-security/standard-devops-security-requirements.md`](../dev-security/standard-devops-security-requirements.md): if the team operates pipelines.
- [`dev-security/guideline-ai-coding-assistant-security.md`](../dev-security/guideline-ai-coding-assistant-security.md): if developers use Claude Code, Copilot, Cursor, or equivalent.
- [`dev-security/claude-rules/`](../dev-security/claude-rules/) pack as project-loaded session context: if any AI coding assistant is used.

#### A2: We ship external-facing software (SaaS, downloadable, embedded)

Triggered by software that runs on customer infrastructure, in a customer-accessible cloud tenancy, or as a downloadable artefact.

Adopt the A1 set plus:
- [`operations/`](../operations/): runbook-style procedures for the recurring operational interactions.
- [`architecture/`](../architecture/): lighter set; the reference-architecture artefacts for the patterns the team builds.
- [`resilience/`](../resilience/): light; business-continuity and incident-aligned recovery procedures.

#### A3: We use AI in operations (any AI deployment)

Triggered by use of AI in customer-facing or internal workflows: chat assistants, document summarisation, decision support, content generation, recommendation systems, etc.

Adopt:
- [`ai/policy-ai-compliance.md`](../ai/policy-ai-compliance.md): the AI policy floor.
- [`ai/template-ai-system-register.md`](../ai/template-ai-system-register.md): inventory each AI system in scope.
- [`ai/template-system-card.md`](../ai/template-system-card.md): per-system documentation for high-tier systems.
- [`ai/checklist-ai-algorithmic-compliance.md`](../ai/checklist-ai-algorithmic-compliance.md): if the AI use case touches regulated decision-making.

#### A4: We develop or train AI models

Triggered by training models in-house, fine-tuning, or building AI products that depend on the model artefact being part of the deliverable.

Adopt the A3 set plus:
- [`ai/template-model-card.md`](../ai/template-model-card.md): per-model.
- [`ai/template-dataset-datasheet.md`](../ai/template-dataset-datasheet.md): per-dataset.
- [`ai/template-ai-red-team-report.md`](../ai/template-ai-red-team-report.md): for high-tier systems.
- [`ai/framework-ai-model-documentation-and-transparency.md`](../ai/framework-ai-model-documentation-and-transparency.md): the documentation discipline.

#### A5: We have critical-availability operations

Triggered by contractual SLAs, regulated availability requirements (DORA, NIS 2, CNI duties), or business-critical processes whose interruption is materially damaging.

Adopt:
- [`resilience/`](../resilience/) full set.
- [`operations/`](../operations/) operational-discipline artefacts.
- [`risk/`](../risk/) deeper risk register with availability-tier classifications.

#### A6: We have physical operations

Triggered by logistics, manufacturing, healthcare delivery, retail estate, transportation, energy distribution, or any operation that materially depends on physical processes and assets.

Adopt:
- [`operations/`](../operations/) full set.
- The sector overlay under [`compliance/`](../compliance/) for the relevant industry (logistics, healthcare, energy-and-utilities, etc.).
- [`resilience/`](../resilience/): physical operations have physical resilience needs.

### Dimension B: Data scope (what we HANDLE)

#### B1: Customer or external personal data

Triggered by any processing of personal data belonging to people outside the organisation (customers, prospects, members, patients, etc.). Most organisations trigger this.

Adopt:
- [`privacy/`](../privacy/) core: policy, jurisdiction annex(es), [`template-record-of-processing-activities.md`](../privacy/template-record-of-processing-activities.md), [`procedure-data-subject-rights-management.md`](../privacy/procedure-data-subject-rights-management.md).
- [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md).

#### B2: Special-category personal data (health, biometric, ethnic origin, religious, sexual orientation, trade union, political opinion, genetic)

Triggered by processing data classified as special-category under GDPR or equivalent regimes.

Adopt the B1 set plus:
- [`privacy/standard-pseudonymisation-and-anonymisation.md`](../privacy/standard-pseudonymisation-and-anonymisation.md).
- The relevant framework documents (e.g. [`privacy/framework-consent-management.md`](../privacy/framework-consent-management.md)).
- Stricter retention controls per the data type.

#### B3: Children's data

Triggered by processing data about people under the relevant age-of-majority threshold (typically 16 or 18, jurisdiction-dependent).

Adopt the B1 set plus:
- [`privacy/framework-childrens-data.md`](../privacy/framework-childrens-data.md).
- The home-jurisdiction children-data-specific regulation if dedicated.

#### B4: Cross-border data transfers

Triggered by personal data flowing across jurisdictional boundaries (cloud hosted in a different country than data subjects, multi-region operations, vendor processors abroad).

Adopt:
- [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../privacy/procedure-privacy-impact-and-cross-border-transfer.md).
- The annex for each jurisdiction the data flows into or out of (from [`privacy/jurisdictions/`](../privacy/jurisdictions/)).
- [`privacy/register-cross-border-data-flow.md`](../privacy/register-cross-border-data-flow.md).

#### B5: Payment card data (PCI scope)

Triggered by storage, processing, or transmission of payment card data, or by being in the cardholder data environment of a payment processor.

Adopt:
- [`security/`](../security/) full set.
- [`supply-chain/`](../supply-chain/) heavy: PCI assessments depend on third-party attestations.
- The financial-services sector overlay if applicable.

#### B6: Government or classified data

Triggered by processing data classified by a government as restricted, confidential, or above.

Adopt:
- [`compliance/public-sector/`](../compliance/public-sector/) full set.
- The jurisdiction-specific classified-information framework.
- Significantly heavier security stack.

### Dimension C: Audience (who we SERVE)

#### C1: Consumers (B2C)

Adopt:
- B1 with consumer-facing emphasis: cookies and tracker register, privacy notice, consent management.
- Breach-notification procedure tuned to consumer-notification timelines (often regulated; e.g. 72 hours under GDPR; specific state laws in the US).

#### C2: Businesses (B2B; your customers are other organisations)

Adopt:
- [`supply-chain/`](../supply-chain/) (you ARE someone's vendor): vendor security questionnaire, attestation patterns, contract security terms.
- Customer-due-diligence response templates.

#### C3: Government clients

Adopt:
- [`compliance/public-sector/`](../compliance/public-sector/) full set.
- Attestation patterns specific to the relevant government framework (FedRAMP, IL4/IL5, GovAssure, ISM, etc.).

### Dimension D: Regulatory exposure (who regulates us)

#### D1: Light (basic privacy law only, no sector regulator)

The core baseline plus the home-jurisdiction privacy annex is enough. No further D-dimension content needed.

#### D2: Sector-regulated (one dominant regulator: FCA, PRA, HIPAA, FDA, NERC, MAS, etc.)

Adopt the relevant sector folder under [`compliance/`](../compliance/) in full. Identify the primary sector via the decision tree.

#### D3: Multi-regulated (multiple sectors or jurisdictions)

Adopt multiple sector folders under [`compliance/`](../compliance/) plus multi-jurisdiction privacy annexes. Establish a cross-framework alignment matrix (consider [`compliance/matrix-grc-compliance-alignment.md`](../compliance/matrix-grc-compliance-alignment.md)).

#### D4: Heavy (financial services, healthcare, public-sector cyber, critical infrastructure)

Adopt the full sector folder plus [`resilience/`](../resilience/), [`supply-chain/`](../supply-chain/) deep, and [`risk/`](../risk/) full. Heavy regulatory exposure is the typical driver for a dedicated GRC function, which then layers Dimension E content.

### Dimension E: GRC team capacity (how much we can maintain)

Dimension E scales the depth of every other adopted module.

#### E1: None or founder part-time

Copy the minimum viable subset of each chosen module. Skip framework documents and charter documents at this layer; the policies and procedures are enough. Skip programme-level performance reviews.

#### E2: Light (1 to 2 people)

Copy the core artefacts of each chosen module and customise them. Skip programme-performance-review documents (e.g. [`governance/framework-governance-performance-and-improvement.md`](../governance/framework-governance-performance-and-improvement.md)) until capacity exists to operate them.

#### E3: Standard (3 to 10 people)

Copy the full set of each chosen module. A quarterly review cycle is realistic. Programme-performance reviews are tractable.

#### E4: Heavy (a department)

Copy the full set of each module plus measurement infrastructure (metrics, dashboards, board-level reports). The library's [`docs/template-maturity-self-assessment.md`](template-maturity-self-assessment.md) Tier 4 / 5 guidance applies.

---

## Worked examples

### Example 1: Mid-size SaaS with EU customers and AI features

A 60-person SaaS company. Customers across EU, UK, and US. Custom internal development, external-facing SaaS. Uses AI for feature delivery (text summarisation, recommendation). Lightly regulated (general privacy law only). One-person privacy function plus part-time engineering-security lead (E2-bordering-E3).

Composition:
- Core baseline (mandatory).
- A1 (custom internal dev), A2 (ships external SaaS), A3 (AI in operations).
- B1 (customer personal data), B4 (cross-border, EU plus US).
- C1 (consumer-facing if customers are individuals) or C2 (B2B) depending on contract type.
- D1 (light regulatory exposure).
- E2 (capacity scale).

Adopt order: Days 1 to 30 the core baseline plus A1, A2, B1, B4. Days 30 to 90 the A3 module and the C dimension. Defer the deeper architecture and resilience stack until E grows.

### Example 2: Five-person consultancy with no software

A consulting firm. Five staff. No software shipped; all customer engagement is through consulting deliverables. Customer data is meeting notes, contact details, and engagement documents. B2B audience. Light regulatory exposure (general privacy law of the home jurisdiction). Founder is the GRC function (E1).

Composition:
- Core baseline (mandatory), minus the A1 elements since no software is shipped (dev-security is optional at this scale; including it costs more than it saves).
- B1 (customer data, modest scope).
- C2 (B2B audience).
- D1.
- E1 (capacity scale).

The result is a small, sustainable adopted set: six baseline artefacts plus the B1 privacy module plus a vendor security questionnaire response template. The firm can defensibly answer customer security-due-diligence questionnaires with this set.

### Example 3: Regional bank

A 1,200-person regional bank. Custom in-house development for digital banking products. Mainframe and legacy operations for core banking. Customer personal data, payment card data, cross-border (some international wires). Consumer plus business customers. Heavy financial-services regulatory exposure (home-jurisdiction prudential regulator plus AML / sanctions / CCAR-style requirements plus DORA if EU). Dedicated GRC department (E4).

Composition:
- Core baseline (mandatory).
- A1 (custom dev), A5 (critical-availability operations: digital banking SLAs), A6 (physical operations: branches).
- B1 (customer data), B5 (payment cards), B4 (cross-border for wires).
- C1 (consumer) plus C2 (business banking).
- D4 (heavy financial-services regulation).
- E4 (capacity).

Adopt order: the full library is in scope. Day 1 the core baseline, plus the full financial-services sector overlay under [`compliance/financial-services/`](../compliance/financial-services/), plus the resilience and supply-chain domains. Day 30 the A1 / A5 / A6 modules. Day 90 a first programme-level maturity self-assessment with the goal of identifying which Tier-3 to Tier-4 gaps the department closes in year one.

---

## Review questions

When applying a composition, answer the following before going live with the adopted set:

1. Have we copied and customised the core baseline (the six artefacts everyone needs)?
2. Have we identified the activity modules that apply (Dimension A)?
3. Have we identified the data-scope modules that apply (Dimension B)? In particular, have we surfaced any special-category, children's, or cross-border processing?
4. Have we identified the audience modules (Dimension C)?
5. Have we set our regulatory-exposure level (Dimension D) and copied the relevant sector overlays?
6. Have we set our GRC capacity (Dimension E) and scaled the depth of each module accordingly?
7. Have we run an initial maturity-scorecard self-assessment using [`docs/template-maturity-self-assessment.md`](template-maturity-self-assessment.md) against the adopted set?
8. Have we logged the modules we identified but deferred so they are not silently dropped?

---

## Maintenance

This template is updated when:

- The library adds or removes a domain that materially changes the core baseline or a module's adopted artefacts.
- A new activity, data, audience, or regulatory dimension is identified that the existing five dimensions do not cover.
- Adopter feedback identifies a module that consistently splits into two natural sub-modules (in which case the module is decomposed).

Major version bumps to this template are warranted when the dimension model itself changes. Minor bumps cover module additions, artefact additions inside a module, and worked-example updates. The composition shape should not change frequently; it is meant to be stable across the library's growth.

---

## Licence

CC BY-SA 4.0. Adapt and share, including for commercial use; preserve the licence on derivative works.
