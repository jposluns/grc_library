# Adopter Quickstart Template by Profile

**Document Title:** Adopter Quickstart Template by Profile\
**Document Type:** Template\
**Version:** 1.0.0\
**Date:** 2026-06-20\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`docs/adopter-guide.md`](adopter-guide.md), [`docs/decision-tree.md`](decision-tree.md), [`docs/maturity-scorecard.md`](maturity-scorecard.md), [`README.md`](../README.md), [`docs/worked-example.md`](worked-example.md)\
**Classification:** Public\
**Category:** Adopter Experience\
**Review Frequency:** Annual, and on material change to the library's domain structure or sector-conditional content\
**Repository Path:** [`docs/template-quickstart-by-profile.md`](template-quickstart-by-profile.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template provides a pre-configured starter set per common adopter profile. Each profile section names the library domains to copy first, the sector-conditional folders to include, the jurisdictions to start with, and the artefacts to defer until later phases of adoption.

The aim is to compress the adopter's first-week question (`which of the 11 domains do I need on day one?`) into a profile-shaped checklist. The decision-tree at [`docs/decision-tree.md`](decision-tree.md) covers the conditional logic; this template materialises the answer for the six most common profile shapes.

A profile is a starting point, not a final scope. Adopters typically grow into adjacent domains as the programme matures; the [`docs/adopter-guide.md`](adopter-guide.md) section "Maturity progression" describes the standard growth path.

---

## Scope

This template applies to organisations adopting the library for the first time and to organisations consolidating an existing adoption against this library's structure. It covers six profile shapes:

1. **Small business** (under 50 employees, single jurisdiction).
2. **Mid-market regulated industry** (50 to 500 employees, sector-specific compliance).
3. **Multi-national enterprise** (500 plus employees, multiple jurisdictions).
4. **Public-sector adopter** (government agency, public body, or supplier to public sector).
5. **Healthcare adopter** (provider, payer, medtech, or healthcare platform).
6. **Financial-services adopter** (bank, investment firm, insurance, payment provider, or financial market infrastructure).

Out of scope: bespoke profile shapes (defence and aerospace, mining, agriculture, and the other industry sectors marked Out of scope in [`governance/register-coverage-gaps.md`](../governance/register-coverage-gaps.md) §1). Adopters whose shape does not match a profile here should consult the [`docs/decision-tree.md`](decision-tree.md) and the adopter guide directly.

---

## How to use this template

For each profile, the section is laid out as:

- **Define**: the profile's defining characteristics.
- **Adopt first** (Day-1 and first 30 days): the minimum set of library domains and artefacts that materially reduce risk on first contact with auditors, regulators, customers, or incident.
- **Layer next** (Days 30 to 90): the artefacts that build on the first-30-day set and address the most-likely follow-up questions.
- **Defer** (Day 90 plus): artefacts useful at scale or under specific triggers, but not essential for first contact.
- **Skip unless triggered**: artefacts that require a specific organisational or regulatory trigger before they materially matter.
- **Sector-conditional content**: the sector or jurisdiction sub-folders the profile materially needs.
- **Realistic first-90-day timeline expectations**.

The "Adopt first" set is intentionally narrow; adopters can copy the full library and selectively populate it, but going live with a small set the organisation can actually maintain is better than going live with a large set that gathers dust.

---

## Profile 1: Small business (under 50 employees, single jurisdiction)

### Define

- Headcount: under 50.
- Geographic scope: one country or one regulatory zone.
- Regulatory exposure: privacy law of the home jurisdiction, basic information-security expectations from customers, and any sector-specific licensing the business operates under.
- Compliance posture: lean, founder-led or small-team-led; the goal is "we can answer audit questions consistently" rather than "we have a 30-control programme".

### Adopt first (Day-1 to Day-30)

| Domain | Artefacts | Why |
| --- | --- | --- |
| `governance/` | `policy-information-and-cybersecurity.md`, `charter-governance-library.md` (as a model) | One overarching policy plus a charter shape adapted to the founder/CEO as policy owner. |
| `security/` | `policy-acceptable-use.md`, `policy-access-control.md`, `procedure-incident-response.md` | The three documents that most small-business incidents touch. |
| `privacy/` | `policy-privacy-and-data-governance.md`, plus the home-jurisdiction annex from [`privacy/jurisdictions/`](../privacy/jurisdictions/) | Privacy law compliance is the most common single regulatory exposure for a small business. |
| `dev-security/` | `standard-developer-security-requirements.md` | Even small teams ship software; the standard is the floor. |
| `risk/` | `register-operational-risk-template.md`, populated with the top 10 risks | A short, real risk register beats a long imagined one. |

### Layer next (Day-30 to Day-90)

- `compliance/`: `policy-compliance-and-audit-management.md` plus the [`compliance/matrix-grc-compliance-alignment.md`](../compliance/matrix-grc-compliance-alignment.md) for cross-referencing.
- `supply-chain/`: `policy-supply-chain-and-third-party-security.md` once the vendor count crosses 5 to 10.
- `operations/`: the `policy-operations-management.md` shape for day-to-day operational discipline.

### Defer (Day-90 plus)

- `architecture/`: full enterprise-architecture documents; small businesses do not have an enterprise architecture function.
- `resilience/`: dedicated business-continuity content; the incident response procedure covers most small-business resilience needs at this scale.

### Skip unless triggered

- `ai/`: only when the business builds or operationally depends on AI systems.
- `compliance/financial-services/`, `compliance/healthcare/`, etc.: only when the business is in that sector.

### Sector-conditional content

The home-jurisdiction annex from `privacy/jurisdictions/` is the only conditional content most small businesses need on day one.

### Realistic timeline

Day 30: policies copied, jurisdiction annex adopted, top-10 risk register populated. Day 60: incident-response procedure tested at desk-check level. Day 90: first internal review against the maturity scorecard at the "Foundational" level.

---

## Profile 2: Mid-market regulated industry (50 to 500 employees, sector compliance)

### Define

- Headcount: 50 to 500.
- Geographic scope: typically one or two countries.
- Regulatory exposure: sector-specific compliance (the sector overlay in [`compliance/`](../compliance/)) plus the home-jurisdiction privacy law plus baseline information-security expectations.
- Compliance posture: a small dedicated compliance or risk function; the goal is "we can pass a customer or regulator audit on the sector-specific controls".

### Adopt first (Day-1 to Day-30)

The small-business "Adopt first" set, plus:

- `compliance/<sector>/`: the entire folder for the regulated sector. The sector overlay is the load-bearing differentiator at this scale.
- `compliance/policy-compliance-and-audit-management.md`: the compliance-function policy.
- `compliance/standard-internal-audit.md`: the internal-audit shape.

### Layer next (Day-30 to Day-90)

- `supply-chain/`: the full domain plus `procedure-third-party-ai-due-diligence.md` if AI vendors are in the supply chain.
- `risk/`: the full domain. A mid-market regulated firm has enough operational complexity to warrant a structured risk programme.
- `dev-security/`: the full set if the firm ships software.

### Defer (Day-90 plus)

- `architecture/`: useful but not load-bearing for sector audit.
- Multi-jurisdiction privacy annexes beyond the home jurisdiction.

### Skip unless triggered

- `ai/`: only if AI systems are operationally relevant.
- Multiple sector overlays: stick to the primary sector unless the firm operates across sectors.

### Sector-conditional content

The full sector overlay from [`compliance/<sector>/`](../compliance/) is mandatory. Identify the primary sector via the decision-tree at [`docs/decision-tree.md`](decision-tree.md) and copy the whole folder.

### Realistic timeline

Day 30: sector overlay copied and reviewed against the firm's current control set; gaps logged. Day 90: first sector-audit-readiness review.

---

## Profile 3: Multi-national enterprise (500 plus employees, multiple jurisdictions)

### Define

- Headcount: 500 plus.
- Geographic scope: three or more jurisdictions.
- Regulatory exposure: multiple privacy regimes, sector-specific compliance, cross-border transfer obligations, vendor-and-customer expectations across geographies.
- Compliance posture: dedicated functions for compliance, risk, security, privacy, and (typically) internal audit; the goal is "we can defend our programme against any auditor, regulator, customer, or shareholder query".

### Adopt first (Day-1 to Day-30)

The full library, with the following emphasis:

- All `governance/` artefacts: the charter, the framework, the document-architecture spec.
- All `compliance/` cross-cutting artefacts plus the relevant sector overlays.
- All `privacy/` artefacts plus every jurisdiction the firm operates in (consult [`privacy/jurisdictions/`](../privacy/jurisdictions/)).
- `risk/`, `security/`, `supply-chain/`, `architecture/`, `resilience/`, `operations/` in full.

### Layer next (Day-30 to Day-90)

- Customisation: adapt jurisdiction annexes to the firm's actual operating model where the library annex is generic.
- Integration: cross-reference the library against any internal frameworks the firm already operates (ISO 27001, NIST CSF, SOC 2 Type II, etc.).

### Defer (Day-90 plus)

- Out-of-scope-by-default sectors the firm does not operate in.

### Skip unless triggered

- AI artefacts only if AI is materially part of the operating model. (At this scale most multi-nationals will trigger this.)

### Sector-conditional content

Multiple sector overlays where the firm operates across sectors (e.g., a financial group with a healthcare-products arm needs both `compliance/financial-services/` and `compliance/healthcare/`).

### Realistic timeline

Day 30: full library copied; assignment of artefacts to internal owners. Day 90: gap analysis against the maturity scorecard at the "Operational" level; remediation roadmap published.

---

## Profile 4: Public-sector adopter

### Define

- Organisation type: government agency, public body, or supplier whose primary customer is the public sector.
- Regulatory exposure: jurisdiction-specific government-cybersecurity requirements (FedRAMP, IL4/IL5, GovAssure, ISM/PSPF, etc.), public-records and freedom-of-information obligations, plus the cross-cutting privacy and security expectations.
- Compliance posture: typically more procedural than risk-based; the goal is "we can demonstrate alignment to the jurisdiction's government-cybersecurity framework".

### Adopt first (Day-1 to Day-30)

- `compliance/public-sector/`: the entire folder.
- `governance/`: the policy, charter, and framework artefacts.
- `security/`: the full set; public-sector cybersecurity frameworks are control-heavy.
- `privacy/`: the policy plus the home-jurisdiction annex; public-records obligations and privacy obligations interact.

### Layer next (Day-30 to Day-90)

- `dev-security/` if the agency builds or maintains software.
- `supply-chain/` for vendor-management obligations (typically heavy in public sector).
- `resilience/` for continuity-of-government and continuity-of-service obligations.

### Defer (Day-90 plus)

- `ai/` unless the agency operates AI-influenced decision systems (in which case it is "Adopt first").

### Skip unless triggered

- Sector overlays from `compliance/<other-sector>/`: only if the agency regulates that sector.

### Sector-conditional content

The home-jurisdiction sub-folder under `compliance/public-sector/` (FedRAMP for US federal, GovAssure for UK, ISM for Australia, etc.).

### Realistic timeline

Day 30: jurisdiction-framework overlay reviewed against current operating posture. Day 90: control-attestation evidence packaged per [`compliance/standard-internal-audit.md`](../compliance/standard-internal-audit.md).

---

## Profile 5: Healthcare adopter

### Define

- Organisation type: provider, payer, medtech, or healthcare platform.
- Regulatory exposure: HIPAA + HITECH (US), NHS DSPT (UK), MDR + IVDR (EU medtech), provincial frameworks (Canada), plus the cross-cutting privacy expectations particularly around special-category data.
- Compliance posture: privacy-heavy and (for medtech) safety-engineering-heavy.

### Adopt first (Day-1 to Day-30)

- `compliance/healthcare/`: the entire folder.
- `privacy/`: full domain plus all relevant jurisdiction annexes; healthcare data is special-category and the privacy regime is the load-bearing exposure.
- `security/`: full set; healthcare data breaches are the largest single category of US breach notifications.
- `governance/` and `risk/`: the core artefacts.

### Layer next (Day-30 to Day-90)

- `dev-security/` and `architecture/` for medtech and healthcare-platform firms shipping software.
- `supply-chain/`: vendor management is heavy in healthcare (EHR vendors, lab vendors, device vendors).
- `ai/`: for any AI-influenced clinical decision support, diagnostic, or operational optimisation.
- `resilience/`: continuity of care obligations.

### Defer (Day-90 plus)

- Cross-sector compliance overlays unless the organisation operates across sectors.

### Skip unless triggered

- `operations/` operational-management artefacts: useful but not load-bearing for the initial healthcare-compliance posture.

### Sector-conditional content

Sub-folders under `compliance/healthcare/` for the relevant healthcare regime; `privacy/framework-childrens-data.md` if paediatric care is in scope.

### Realistic timeline

Day 30: HIPAA or equivalent control-mapping. Day 90: breach-response procedure tested at tabletop level; vendor BAAs mapped.

---

## Profile 6: Financial-services adopter

### Define

- Organisation type: bank, investment firm, insurance, payment provider, or financial-market infrastructure.
- Regulatory exposure: home-jurisdiction prudential and conduct regulators (PRA + FCA, OCC + FRB + FDIC, OSFI, APRA, MAS, etc.), DORA (EU), SOX (US listed), plus the cross-cutting privacy and security regimes.
- Compliance posture: heavy on third-party risk, operational resilience, and conduct.

### Adopt first (Day-1 to Day-30)

- `compliance/financial-services/`: the entire folder.
- `resilience/`: full domain; DORA and equivalents make operational resilience a first-class compliance obligation.
- `supply-chain/`: full domain; third-party risk is the highest-scrutiny area for financial regulators.
- `security/`: full set.
- `governance/`, `risk/`, `privacy/`: core artefacts.

### Layer next (Day-30 to Day-90)

- `dev-security/`: for any firm shipping or operating software (most do at this scale).
- `architecture/`: enterprise-architecture artefacts are commonly required by financial regulators.
- `ai/`: increasingly relevant for credit-decision, trading, and compliance-monitoring AI.

### Defer (Day-90 plus)

- Cross-sector compliance overlays unless the firm operates across sectors.

### Skip unless triggered

- `compliance/healthcare/`, `compliance/energy-and-utilities/`, etc.: only if the firm operates in those sectors.

### Sector-conditional content

Sub-folders under `compliance/financial-services/` for the relevant regulator (currently DORA, SOX; per the [`governance/register-coverage-gaps.md`](../governance/register-coverage-gaps.md) §2.3, country-specific regulator overlays are planned under TODO P5.2).

### Realistic timeline

Day 30: regulator-mapping against the firm's existing control framework. Day 90: third-party-risk programme reconciled with `supply-chain/` artefacts; resilience testing scheduled.

---

## Profile-shape interactions

A real organisation often sits across two profiles. The recurring shapes:

- **Small healthcare practice**: start with Profile 1 (small business), layer Profile 5 (healthcare) sector-conditional content from Day 1.
- **Mid-market multi-national**: start with Profile 2 (mid-market regulated industry), layer Profile 3 (multi-national) multi-jurisdiction privacy from Day 30.
- **Public-sector software vendor**: start with Profile 4 (public-sector), layer Profile 2 (mid-market sector compliance) for software-supplier expectations.

For shapes the table does not cover, follow the decision-tree at [`docs/decision-tree.md`](decision-tree.md) and adapt the nearest profile.

---

## Review questions

When applying a profile, answer the following before going live with the adopted set:

1. Have we copied the artefacts the profile names as "Adopt first"?
2. Have we adapted the placeholders (organisation name, role names, jurisdiction) in those artefacts?
3. Have we removed or commented out the artefacts the profile flags as "Skip unless triggered"?
4. Have we logged the deferred artefacts in our internal roadmap so they are not silently dropped?
5. Have we identified the sector-conditional content the profile materially needs and copied it as well?
6. Have we run an initial maturity-scorecard self-assessment against the adopted set?

---

## Maintenance

This template is updated when:

- A new adopter-profile shape is identified that the existing six profiles do not cover.
- The library adds or removes a domain or a sector overlay that changes the "Adopt first" set.
- The decision-tree at [`docs/decision-tree.md`](decision-tree.md) changes in a way that affects the profile boundaries.

Per-profile guidance must remain compatible with the decision-tree and with the adopter guide; the three documents are read together by adopters and should not contradict.

---

## Licence

CC BY-SA 4.0. Adapt and share, including for commercial use; preserve the licence on derivative works.
