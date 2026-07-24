# California CCPA Automated Decision-Making Technology (ADMT) Regulatory Requirements

**Document Title:** California CCPA Automated Decision-Making Technology (ADMT) Regulatory Requirements\
**Document Type:** Annex\
**Version:** 0.0.1\
**Date:** 2026-07-24\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](../policy-ai-compliance.md), [`ai/jurisdictions/annex-ai-us-colorado.md`](annex-ai-us-colorado.md), [`ai/jurisdictions/annex-ai-us-new-york-city.md`](annex-ai-us-new-york-city.md), [`privacy/jurisdictions/annex-privacy-united-states.md`](../../privacy/jurisdictions/annex-privacy-united-states.md), [`governance/register-canonical-citations.md`](../../governance/register-canonical-citations.md), [`compliance/register-global-regulatory-applicability.md`](../../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material change to the CCPA ADMT regulations or their compliance dates\
**Repository Path:** [`ai/jurisdictions/annex-ai-us-california.md`](annex-ai-us-california.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex documents California's AI-specific regulatory limb for the AI-domain reader: the California Privacy Protection Agency's CCPA regulations on Automated Decisionmaking Technology (ADMT), which bind a business that uses ADMT to make a significant decision concerning a consumer. It is the `ai/jurisdictions/` view of that limb, parallel to the Colorado and New York City AI annexes, and it adds the framework-alignment crosswalk (NIST AI RMF, ISO/IEC 42001) for AI-governance adopters. The same ADMT obligations are ALSO documented, from the privacy-compliance angle, in [`privacy/jurisdictions/annex-privacy-united-states.md`](../../privacy/jurisdictions/annex-privacy-united-states.md) (its "AI and privacy obligations" section carries the pre-use notice, opt-out, access, and human-appeal-exception detail alongside the CCPA risk-assessment and cybersecurity-audit slices); on the obligation detail the enacted regulation and that privacy annex govern, and this annex cross-references rather than supersedes them.

## Applicable law and regulatory authority

The controlling instruments are the CCPA/CPRA statute (Cal. Civ. Code section 1798.100 et seq.) and the CPPA CCPA Regulations (11 CCR Division 6 Chapter 1), whose Article 11 governs ADMT (sections 7200 to 7222). The regulator is the California Privacy Protection Agency (CPPA). These are BINDING regulations, not voluntary guidance: unlike the Singapore Model AI Governance Framework annex, an in-scope business is legally required to comply. The regulations are the final consolidated text effective 1 January 2026.

## Transition timeline

The CPPA CCPA Regulations are the final consolidated text effective 1 January 2026. ADMT compliance is DEFERRED: a business that uses ADMT for a significant decision must be in compliance with Article 11 no later than 1 January 2027 (section 7200(b)). The adjacent risk-assessment (Article 10) and cybersecurity-audit (Article 9) obligations phase in on their own later dates and are outside this annex's ADMT scope. The held edition is confirmed current against the CPPA as of the date of this annex; the regulation is version-sensitive, so the in-force text and the compliance dates are reconfirmed upstream at corpus-cite time.

## Scope: covered actors and covered decisions

The obligations bind a business, as the CCPA defines that term, that uses ADMT to make a "significant decision concerning a consumer" (section 7200(a)). The definitions of ADMT and of a significant decision are set out in the regulation's definitions section (section 7001). A use of ADMT that does not make a significant decision concerning a consumer is outside Article 11.

## Core obligations

Article 11 places three ADMT obligations on an in-scope business (cited by section number; the operative text is quoted here from the regulation):

- **Pre-use notice (section 7220).** "A business that uses ADMT as set forth in section 7200, subsection (a), must provide consumers with a Pre-use Notice. The Pre-use Notice must inform consumers about the business's use of ADMT and consumers' rights to opt-out of ADMT and to access ADMT, as set forth in this section."
- **Opt-out (section 7221).** "A business must provide consumers with the ability to opt-out of the use of ADMT to make a significant decision concerning the consumer, except as set forth in subsection (b)." Subsection (b) carries the exceptions.
- **Access (section 7222).** "A business that uses ADMT to make a significant decision must provide a consumer with information about this use when responding to a consumer's request to access ADMT," and it must provide that information in plain language.

## Consumer rights

The obligations create three consumer-facing rights: to be notified before ADMT is used to make a significant decision about the consumer (the pre-use notice), to opt out of that ADMT use, and to access information about it. The opt-out is subject to the section 7221(b) exceptions, including a human-appeal alternative. These ADMT rights, and the broader CCPA statutory access and opt-out rights, are documented in the US privacy annex; this annex gives the AI-governance framing of the ADMT-specific rights and cross-references the privacy annex for the full obligation and exception detail.

## Enforcement

The California Privacy Protection Agency holds investigation and enforcement authority over the CCPA regulations, and the CCPA statute carries the underlying enforcement regime. This annex does not restate the enforcement detail; it points at the CPPA regulations and the CCPA statute as the controlling text.

## Relationship to the California privacy layer

This annex and the US privacy annex ([`privacy/jurisdictions/annex-privacy-united-states.md`](../../privacy/jurisdictions/annex-privacy-united-states.md)) both touch the CCPA ADMT limb. The privacy annex documents it within its "AI and privacy obligations" section, from the privacy-compliance angle, alongside the CCPA risk-assessment and cybersecurity-audit slices and the general CCPA consumer-data rights (access, deletion, correction, sale and sharing opt-out); this annex gives the parallel AI-governance view for the `ai/jurisdictions/` reader, with the framework-alignment crosswalk. The two overlap on the ADMT section numbers, dates, and the significant-decision definition, and are kept cross-referenced; on any divergence the enacted regulation and the privacy annex govern the obligation detail. Whether to consolidate the ADMT detail into a single canonical annex, following the pattern the privacy annex already uses for the Colorado AI statute (a brief bullet pointing to the AI annex), is a maintainer follow-up recorded in the backlog.

## Limitations

These are binding regulations, not legal advice; the controlling text is the CPPA regulations and the CCPA statute themselves. The regulation text is version-sensitive: the in-force text and the ADMT compliance date are reconfirmed upstream at corpus-cite time (the held edition is the final consolidated text effective 1 January 2026, with ADMT compliance deferred to 1 January 2027). ADMT scope is narrower than general automated processing, so this annex does not cover automated processing that makes no significant decision concerning a consumer.

## Framework alignment

The requirement column and its section cites are the load-bearing, held-source-grounded content. The NIST AI RMF function tags and the ISO/IEC 42001:2023 Annex A anchors are a crosswalk to help an adopter reuse its existing management-system controls; they are a mapping aid, not an assertion that the binding regulations and those frameworks impose the same obligations.

| Requirement | California CCPA ADMT regulations | NIST AI RMF | ISO/IEC 42001 |
| --- | --- | --- | --- |
| Notice before automated decisioning | section 7220 (pre-use notice) | Govern, Map | Annex A.8 |
| Consumer opt-out of ADMT for significant decisions | section 7221 | Manage, Govern | Annex A.9 |
| Consumer access to ADMT information | section 7222 | Map, Measure | Annex A.8 |
| Covered-use threshold (significant decision) | section 7200 | Map | Annex A.5 |
