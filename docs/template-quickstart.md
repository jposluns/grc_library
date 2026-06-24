# Adopter Quickstart Template

**Document Title:** Adopter Quickstart Template\
**Document Type:** Template\
**Version:** 3.0.4\
**Date:** 2026-06-24\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`docs/template-startup-roadmap.md`](template-startup-roadmap.md), [`docs/adopter-guide.md`](adopter-guide.md), [`docs/decision-tree.md`](decision-tree.md), [`docs/template-implementation-roadmap.md`](template-implementation-roadmap.md), [`README.md`](../README.md)\
**Classification:** Public\
**Category:** Adopter Experience\
**Review Frequency:** Annual, and on material change to the core baseline\
**Repository Path:** [`docs/template-quickstart.md`](template-quickstart.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

A 10-minute on-ramp for an adopter who wants to take a defensible starting set from the library today. This quickstart names the minimum viable adoption; the deeper composition workbook lives in [`docs/template-startup-roadmap.md`](template-startup-roadmap.md).

### Where this fits among the adopter entry points

The canonical front door for adopters is [`docs/portal.md`](portal.md) (audience-keyed grouping by role). This quickstart is one of the deeper-dive paths that branch off the portal; it answers "what do I copy on Day 1?". For "what do I add later?" see [`docs/template-startup-roadmap.md`](template-startup-roadmap.md) (the full composition workbook). For fork-and-adapt principles see [`docs/adopter-guide.md`](adopter-guide.md); for sequenced reading order see [`docs/decision-tree.md`](decision-tree.md); for calendar phasing see [`docs/template-implementation-roadmap.md`](template-implementation-roadmap.md). The portal's "Other entry points and when to use them" table picks the right path by question.

---

## The minimum viable adoption

Every adopter needs these three things in the first session, regardless of size or sector:

1. **Copy the core baseline.** Six artefacts that constitute the floor below which the programme cannot be defended:
   - [`security/policy-information-security.md`](../security/policy-information-security.md) (foundational policy)
   - [`security/policy-acceptable-use.md`](../security/policy-acceptable-use.md) (acceptable use)
   - [`security/policy-identity-and-access-management.md`](../security/policy-identity-and-access-management.md) (identity and access)
   - [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) (incident response)
   - [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md) plus the relevant file from [`privacy/jurisdictions/`](../privacy/jurisdictions/) (privacy policy and home-jurisdiction annex)
   - [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md) (enterprise risk governance policy; aligns with the Tier 1 starter set in [`docs/adopter-guide.md`](adopter-guide.md))

2. **Substitute the role names.** Every artefact in the library names roles, not people. Map each role to a real person in your organisation in a private overlay. Do not edit named individuals into the artefacts themselves.

3. **Point at the portal.** Browse [`docs/portal.md`](portal.md) to see which other documents fit your audience (CIO, CISO, DPO (Data Protection Officer), auditor, engineering team, etc.). Take only the documents that match your sector, jurisdiction, and operating model.

That is the quickstart. An organisation that has done these three things has a defensible floor. These six artefacts are the Day-1 floor, and all six now also appear in the adopter guide's 17-document Tier 1 set, so the Day-1 floor is a strict subset of Tier 1. The Day-1 floor, the Tier 1 set, and the sector-conditional sets the decision tree builds are progressively-nested, complementary starting points rather than competing ones.

---

## Next steps

When ready to go beyond the floor, the adopter paths are designed to be used in the order [`docs/portal.md`](portal.md) describes: this quickstart composes the starting set, the decision tree sequences it, the implementation roadmap calendars it, and the adopter guide governs how you fork and customise it.

- **[`docs/decision-tree.md`](decision-tree.md)** — the conditional applicability decision tree for the sector, jurisdiction, and capability questions that sequence which domains you adopt.
- **[`docs/template-implementation-roadmap.md`](template-implementation-roadmap.md)** — once the composition is set, this template calendars the modules into 90 / 180 / 365-day phases.
- **[`docs/adopter-guide.md`](adopter-guide.md)** — the controlled reference on how the library is meant to be adopted, including the three adoption modes (fork the whole repo, adopt the corpus only, adopt the pack only) and the Tier 1 / Tier 2 / Tier 3 growth path.

To plan the fuller composition (what to add beyond the floor), see **[`docs/template-startup-roadmap.md`](template-startup-roadmap.md)** — the full composition workbook. Five dimensions (activity, data scope, audience, regulatory exposure, GRC capacity), 23 modules, three worked examples. Plan on an afternoon.

---

## Licence

CC BY-SA 4.0. Adapt and share, including for commercial use; preserve the licence on derivative works.
