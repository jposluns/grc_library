# Worked example: adopting the library into a running programme

**Document Title:** Worked Example: Adopting the Library into a Running Programme\
**Document Type:** Guide\
**Version:** 1.0.0\
**Date:** 2026-07-08\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`docs/worked-example.md`](worked-example.md), [`docs/adopter-guide.md`](adopter-guide.md), [`docs/template-quickstart.md`](template-quickstart.md), [`docs/template-startup-roadmap.md`](template-startup-roadmap.md), [`docs/template-implementation-roadmap.md`](template-implementation-roadmap.md), [`docs/decision-tree.md`](decision-tree.md)\
**Classification:** Public\
**Category:** Documentation\
**Review Frequency:** Annual and upon material change to the adopter guide or the adoption tooling\
**Repository Path:** [`docs/worked-example-adoption.md`](worked-example-adoption.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

This walkthrough follows one fictional organization from cloning the library through its first year of operating a governance programme, showing the file-by-file decisions an adopter makes at each stage. It is the companion to [`docs/worked-example.md`](worked-example.md), which walks the opposite direction (converting a draft into a library artefact): that example is for contributors, this one is for adopters. It does not restate the adopter tooling. It references [`docs/template-quickstart.md`](template-quickstart.md), [`docs/template-startup-roadmap.md`](template-startup-roadmap.md), [`docs/template-implementation-roadmap.md`](template-implementation-roadmap.md), [`docs/decision-tree.md`](decision-tree.md), and [`docs/adopter-guide.md`](adopter-guide.md) at each step, and shows how they fit together for a single concrete adopter.

## The adopter

The adopter is the mid-size SaaS company that [`docs/template-startup-roadmap.md`](template-startup-roadmap.md) uses as its Example 1. The profile: a roughly 60-person software-as-a-service company, with customers across the EU, the UK, and the US. It develops software in-house and ships an external-facing SaaS product, and it uses AI in production for feature delivery (text summarization and recommendation). It is lightly regulated (general privacy law, no dominant sector regulator). Its GRC capacity is one privacy person plus a part-time engineering-security lead, which the startup roadmap classes as capacity tier E2 bordering on E3.

In the startup-roadmap module vocabulary the composition is the core baseline plus in-house development, external SaaS, AI in operations, customer personal data, cross-border transfers (EU plus US), a contract-type module, light exposure, and the E2 capacity pace. This walkthrough sequences that composition over a first year. Every later decision is grounded in this profile.

## Step 1: Clone or fork

The adopter follows the [`docs/adopter-guide.md`](adopter-guide.md) quick start: fork the repository on GitHub to track upstream corrections, or copy it into a private repository where a public fork is not acceptable. Because this adopter wants upstream corrections and is willing to run the audit toolchain, it forks and expects to adopt the corpus (and later, optionally, the `tools/`), rather than taking the governance pack alone. The three adoption modes in the adopter guide frame that choice; the walkthrough does not restate them.

## Step 2: Copy the Day-1 six-artefact floor

Before composing anything larger, the adopter takes the Day-1 floor named in [`docs/template-quickstart.md`](template-quickstart.md). It is six artefacts, and it is a strict subset of the adopter guide's 17-document Tier 1 set:

- [`security/policy-information-security.md`](../security/policy-information-security.md)
- [`security/policy-acceptable-use.md`](../security/policy-acceptable-use.md)
- [`security/policy-identity-and-access-management.md`](../security/policy-identity-and-access-management.md)
- [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md)
- [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), plus the home-jurisdiction annex from [`privacy/jurisdictions/`](../privacy/jurisdictions/)
- [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md)

For this adopter the privacy annex is chosen by where the company and its data subjects sit: with EU, UK, and US customers it starts with [`privacy/jurisdictions/annex-privacy-european-union.md`](../privacy/jurisdictions/annex-privacy-european-union.md) and layers the UK and US annexes as it works the decision tree (Step 4). Copying and customizing these six gives a defensible floor in a single working session, per the quickstart.

## Step 3: Substitute roles and identifiers

Every artefact names roles, never people. The adopter maps each role to a real function in a private overlay that it does not commit to the public fork. A worked mapping: [`security/policy-identity-and-access-management.md`](../security/policy-identity-and-access-management.md) names an Owner of Chief Information Security Officer. This company has no CISO, so the part-time engineering-security lead holds that authority; the adopter records the mapping (Chief Information Security Officer to Head of Engineering Security, acting) in its private role-mapping overlay and leaves the artefact's role text unchanged. The library's role vocabulary is [`governance/register-role-authority.md`](../governance/register-role-authority.md), and the overlay is keyed to it. To keep such real values out of the linted tree, the adopter follows the adopter guide's guidance on running the audit toolchain on a fork and keeps the overlay in a directory the linters skip. The adopter must ensure that no named individual is written into a committed artefact.

## Step 4: Phase 1 (days 1 to 90), reach the floor

With the six floor artefacts copied, the adopter sequences the first quarter using [`docs/template-implementation-roadmap.md`](template-implementation-roadmap.md) phase 1 (days 1 to 90 at the E2 reference pace). It customizes the six baseline artefacts, names owners and approving authorities in the metadata by roughly day 60, populates the risk register with real top risks, and desk-checks the incident-response procedure before day 90. For the EU privacy obligation it works [`docs/decision-tree.md`](decision-tree.md): the privacy foundation plus the EU jurisdiction annex, and, because personal data crosses the Atlantic, the cross-border privacy-impact procedure [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../privacy/procedure-privacy-impact-and-cross-border-transfer.md). The acceptance criteria for the phase are the ones the implementation roadmap lists: the six baseline artefacts customized, signed off, and owned; an initial maturity self-assessment recorded; and the incident-response procedure desk-checked at least once.

## Step 5: Phase 2 (days 91 to 180), operationalize and add AI

In the second phase ([`docs/template-implementation-roadmap.md`](template-implementation-roadmap.md) phase 2, days 91 to 180 at the E2 pace) the artefacts move from existing to being used: the adopter stands up a review cadence with [`governance/template-document-review-record.md`](../governance/template-document-review-record.md), runs a full incident-response tabletop, and refreshes the maturity self-assessment. This is where the AI feature set is brought under governance. The adopter guide's Tier 2 growth set adds the `ai/` core artefacts once the starter set is operating reliably; the startup roadmap's AI-in-operations module names the concrete first files. The adopter adopts the AI compliance policy [`ai/policy-ai-compliance.md`](../ai/policy-ai-compliance.md), inventories each AI system with [`ai/template-ai-system-register.md`](../ai/template-ai-system-register.md), documents its higher-tier systems with [`ai/template-system-card.md`](../ai/template-system-card.md), and reads the AI capability path in [`docs/decision-tree.md`](decision-tree.md) for the governance-council and AI-security artefacts. Because it uses AI for feature delivery rather than training its own models, it takes the AI-in-operations set, not the heavier model-development set. The acceptance criteria are the implementation roadmap's phase 2 list: a review-cadence schedule covering every adopted artefact, at least one completed review wave, measurable maturity movement, and a tabletop that produced an artefact-update list.

## Step 6: Year-1 close and tracking upstream

[`docs/template-implementation-roadmap.md`](template-implementation-roadmap.md) phase 3 (days 181 to 365 at the E2 pace) reaches steady state: the adopter deepens the domains its phase 2 self-assessment flagged, introduces a small measurement layer (a handful of programme metrics, not dozens), runs a programme-level governance review, and publishes a year-1 retrospective and a year-2 plan signed off by the governance authority. From there the programme runs on its own cadence.

To stay current with the library the adopter follows the adopter guide's guidance on tracking upstream updates: read the CHANGELOG entry for the period since the last pull, run `tools/run_all_audits.sh` to confirm the fork is still conformant, and resolve version-monotonicity conflicts by keeping the fork's own version line and recording the upstream version it reconciled against. The adopter guide names the recurring pull cases (merge conflicts in edited artefacts, a new upstream gate the fork trips, and version-monotonicity conflicts); this adopter's customized privacy annexes and role overlays make the merge-conflict case the common one.

## Common pitfalls

- Copying more than the six-artefact floor on day 1. The floor is deliberately small; the Tier 1 (17-document) and sector-conditional sets are grown into, not taken all at once (see [`docs/template-quickstart.md`](template-quickstart.md) and [`docs/adopter-guide.md`](adopter-guide.md)).
- Editing role names into named individuals inside the artefacts. Keep the artefact text role-based and map roles to people in a private overlay only.
- Committing real role-holders, system names, or credentials into a public fork and tripping [`tools/lint-pii-in-content.py`](../tools/lint-pii-in-content.py) or [`tools/lint-secrets-in-content.py`](../tools/lint-secrets-in-content.py). Keep organization-specific values in an exempt overlay directory or out of the committed fork.
- Treating the roadmap dates as a contract. A roadmap is a forecast; the value is the sequence and the acceptance criteria, not the exact calendar dates.
- Adopting the AI artefacts before the security and privacy floor is operating. AI governance is phase 2 and Tier 2 work: it sits on top of the floor, not instead of it.

## Summary

One adopter, one year: fork the library, copy and customize the six-artefact Day-1 floor, map roles to people in a private overlay, then sequence the composition the startup roadmap identifies over the implementation roadmap's three phases, using the decision tree to pick the EU privacy annexes and the AI capability path. The adopter guide governs how the fork is customized and tracked. Each adopter document answers one question; this walkthrough shows them working together for a single concrete organization.
