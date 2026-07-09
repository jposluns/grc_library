# United States HIPAA Sector Requirements Annex

**Document Title:** United States HIPAA Sector Requirements Annex\
**Document Type:** Annex\
**Version:** 0.0.1\
**Date:** 2026-07-09\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/README.md`](../README.md), [`compliance/healthcare/README.md`](README.md), [`compliance/healthcare/annex-healthcare-sector-requirements.md`](annex-healthcare-sector-requirements.md), [`compliance/healthcare/procedure-hipaa-operational-compliance.md`](procedure-hipaa-operational-compliance.md), [`privacy/jurisdictions/annex-privacy-united-states.md`](../../privacy/jurisdictions/annex-privacy-united-states.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../policy-legal-and-regulatory-compliance.md), [`security/policy-information-security.md`](../../security/policy-information-security.md), [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md)\
**Classification:** Public\
**Category:** Compliance: Sector-Specific\
**Review Frequency:** Annual and upon material HIPAA rule (Security, Privacy, Breach Notification) or HHS OCR guidance change\
**Repository Path:** [`compliance/healthcare/annex-healthcare-united-states.md`](annex-healthcare-united-states.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex describes how an organization subject to the US Health Insurance Portability and Accountability Act (HIPAA) can use the core GRC library to meet HIPAA's operational obligations, and where HIPAA requires artefacts and processes the library does not itself produce. It deepens the sector-generic [healthcare annex](annex-healthcare-sector-requirements.md) into a rule-by-rule operational view: role determination, the Security Rule safeguard families, the Privacy Rule use-and-disclosure core, the Breach Notification Rule mechanics and timelines, the enforcement and penalty structure, and the mapping of these obligations to library documents through the NIST SP 800-66r2 implementation crosswalk.

This annex does not reproduce the text of 45 CFR Parts 160, 162, and 164, the HHS Office for Civil Rights (OCR) guidance, or the NIST SP 800-66r2 crosswalk tables. Adopting organizations consume those from the official source. The annex cites obligations by their regulatory section identifier so a reader can locate the controlling text.

Two boundaries keep this annex from duplicating content the library already holds:

- The **HIPAA regulatory landscape and overview** (the three rules, the HITECH Act, and the pending Security Rule Notice of Proposed Rulemaking) live in the sector-generic [healthcare annex](annex-healthcare-sector-requirements.md). This annex references that overview and does not restate it.
- The **privacy-law framing of HIPAA** (covered-entity and business-associate status as it bears on the US privacy-law landscape, cross-border transfer, and the interaction with state privacy statutes) lives in the [US privacy jurisdiction annex](../../privacy/jurisdictions/annex-privacy-united-states.md). This annex treats HIPAA at the healthcare-operational level and cross-references the privacy annex for the privacy-law view.

The individual-rights response clocks, the Notice of Privacy Practices and minimum-necessary duties, the six-year documentation-retention schedule, the four-factor breach-determination test, and the business associate agreement content requirement are operationalized step-by-step in the [HIPAA Operational Compliance Procedure](procedure-hipaa-operational-compliance.md); this annex is the regime map, and the procedure is the executable detail.

---

## Applicability triggers

The library is relevant to HIPAA where the organization:

1. Is a **covered entity**: a health plan, a health care clearinghouse, or a health care provider that transmits health information electronically in connection with a HIPAA transaction.
2. Is a **business associate**: a person or entity that creates, receives, maintains, or transmits protected health information (PHI) on behalf of a covered entity, or that provides services to a covered entity involving PHI.
3. Is a **subcontractor** of a business associate that creates, receives, maintains, or transmits PHI on the business associate's behalf (bound through the flow-down at 45 CFR 164.308(b) and 164.314(a)).

The library is not relevant to HIPAA where the organization neither handles PHI nor provides a PHI-touching service to a covered entity or business associate. HIPAA applicability is independent of, and additional to, any state privacy-law obligation; an organization can be subject to both.

---

## Role determination

The obligations that attach to an organization depend on its HIPAA role, so role determination is the first operational step.

| Role | Test | Principal obligations |
| --- | --- | --- |
| Covered entity | Health plan, clearinghouse, or provider transmitting health information electronically for a HIPAA transaction | The Privacy Rule (45 CFR 164 Subpart E), the Security Rule (Subpart C), and the Breach Notification Rule (Subpart D) in full; execute business associate agreements with each business associate |
| Business associate | Creates, receives, maintains, or transmits PHI for a covered entity | The Security Rule in full; the Breach Notification Rule obligation to notify the covered entity (164.410); the applicable use-and-disclosure limits carried through the business associate agreement (164.314(a), 164.504(e)) |
| Subcontractor | Handles PHI on a business associate's behalf | The same business-associate obligations, bound through the flow-down agreement the business associate must obtain (164.308(b), 164.314(a)) |

A single organization can hold more than one role for different data flows (for example, a covered entity for its own members and a business associate for another covered entity's members); role determination is per data flow, not per organization.

---

## Obligations by rule

This section states the obligations at the rule and safeguard-family level and cites the controlling section. It does not reproduce the regulatory text.

### Security Rule (45 CFR 164 Subpart C)

The Security Rule protects electronic PHI (ePHI). Its general-requirements standard (164.306) requires covered entities and business associates to protect the confidentiality, integrity, and availability of all ePHI they hold, and adopts a **flexibility-of-approach** model: the safeguards are scaled to the organization's size, complexity, capabilities, technical infrastructure, cost, and the probability and criticality of the risks. Each implementation specification is marked **Required** or **Addressable**; an addressable specification must be implemented where reasonable and appropriate, or, where it is not, the organization documents why and adopts an equivalent alternative measure where reasonable and appropriate. Addressable does not mean optional.

The safeguards fall in three families plus an organizational and a documentation standard:

| Safeguard family | Section | Scope |
| --- | --- | --- |
| Administrative safeguards | 164.308 | The Security Management Process (including the risk analysis and risk management that anchor the rule), workforce security, information-access management, awareness and training, incident procedures, contingency planning, evaluation, and business associate contracts |
| Physical safeguards | 164.310 | Facility access controls, workstation use and security, and device and media controls |
| Technical safeguards | 164.312 | Access control, audit controls, integrity, person-or-entity authentication, and transmission security |
| Organizational requirements | 164.314 | Business associate contract content and group-health-plan provisions |
| Policies, procedures, and documentation | 164.316 | Reasonable and appropriate policies and procedures, with documentation retained for six years from creation or last-effective date, whichever is later |

The currently-in-force Security Rule is the 2003 rule as amended by HITECH (2009) and the Omnibus Rule (2013). A Notice of Proposed Rulemaking to strengthen the Security Rule (HHS OCR) was published in the Federal Register on 6 January 2025 and, as of this annex's date, remains proposed and not finalized; if finalized it would materially change the safeguard obligations (proposed mandatory encryption and multi-factor authentication among them). The proposal is described in the [healthcare sector annex](annex-healthcare-sector-requirements.md); adopters track its status and do not implement to a proposed rule as though it were in force.

### Privacy Rule (45 CFR 164 Subpart E)

The Privacy Rule governs the use and disclosure of PHI in all forms. Its operational core, treated here and framed for privacy law in the [US privacy jurisdiction annex](../../privacy/jurisdictions/annex-privacy-united-states.md), comprises: the permitted uses and disclosures and the minimum-necessary standard (164.502, 164.514); the treatment, payment, and health-care-operations uses (164.506); authorizations for other uses (164.508); the Notice of Privacy Practices (164.520); the individual rights of access, amendment, and an accounting of disclosures (164.524, 164.526, 164.528); and the administrative requirements including the six-year retention of privacy documentation (164.530). The response clocks and content requirements for these rights are executed in the [HIPAA Operational Compliance Procedure](procedure-hipaa-operational-compliance.md).

### Breach Notification Rule (45 CFR 164 Subpart D)

A breach is an acquisition, access, use, or disclosure of PHI not permitted under the Privacy Rule that compromises the security or privacy of the PHI, unless a four-factor risk assessment shows a low probability that the PHI was compromised (164.402). PHI that is rendered unusable, unreadable, or indecipherable through a technology or methodology the Secretary has specified is **unsecured** only if it is not so rendered; securing PHI to that standard removes the notification obligation (the encryption safe harbour). A breach is treated as discovered on the first day it is known, or by reasonable diligence would have been known, to the organization.

| Notification | Recipient | Timing |
| --- | --- | --- |
| Individual notice (164.404) | Each affected individual | Without unreasonable delay and no later than 60 calendar days after discovery |
| Media notice (164.406) | Prominent media serving the State or jurisdiction, for a breach involving more than 500 residents of that State or jurisdiction | Same 60-day outer limit |
| Secretary notice (164.408) | HHS, via the HHS website | For 500 or more individuals, contemporaneously with the individual notice; for fewer than 500, logged and reported no later than 60 days after the calendar year's end |
| Business associate notice (164.410) | The covered entity | Without unreasonable delay and no later than 60 calendar days after discovery |

A law-enforcement request can delay notification (164.412). The organization carries the burden of proof to show that the required notifications were made, or that the use or disclosure did not constitute a breach (164.414). The step-by-step application of the four-factor determination test that decides whether the notification clock starts is in the [HIPAA Operational Compliance Procedure](procedure-hipaa-operational-compliance.md).

---

## Library coverage and gaps

The library provides the control baselines that implement most HIPAA safeguards. Adopting organizations implement and evidence the controls; the library is not a substitute for the organization's own risk analysis, policies, and documentation, which HIPAA requires the organization to produce and retain. NIST SP 800-66r2 (Implementing the HIPAA Security Rule, February 2024) is the implementation bridge: its Section 5.1 maps to the 164.308 administrative safeguards, Section 5.2 to the 164.310 physical safeguards, and Section 5.3 to the 164.312 technical safeguards.

| HIPAA obligation | Library coverage |
| --- | --- |
| Administrative safeguards (164.308), including the Security Management Process risk analysis | [`security/policy-information-security.md`](../../security/policy-information-security.md), [`risk/procedure-risk-assessment-methodology.md`](../../risk/procedure-risk-assessment-methodology.md), [`security/procedure-access-control.md`](../../security/procedure-access-control.md), [`security/standard-security-awareness-and-training.md`](../../security/standard-security-awareness-and-training.md) |
| Physical safeguards (164.310) | [`operations/standard-physical-security-of-it-infrastructure.md`](../../operations/standard-physical-security-of-it-infrastructure.md), [`operations/procedure-media-handling-and-transport.md`](../../operations/procedure-media-handling-and-transport.md) |
| Technical safeguards (164.312) | [`security/policy-identity-and-access-management.md`](../../security/policy-identity-and-access-management.md), [`security/standard-authentication-and-password-management.md`](../../security/standard-authentication-and-password-management.md), [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md), [`security/policy-encryption-and-key-management.md`](../../security/policy-encryption-and-key-management.md) |
| Breach Notification Rule (164 Subpart D) | [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md), [`operations/procedure-security-monitoring-and-alert-management.md`](../../operations/procedure-security-monitoring-and-alert-management.md), and the four-factor determination in [`compliance/healthcare/procedure-hipaa-operational-compliance.md`](procedure-hipaa-operational-compliance.md) |
| Privacy Rule (164 Subpart E) | [`privacy/jurisdictions/annex-privacy-united-states.md`](../../privacy/jurisdictions/annex-privacy-united-states.md), [`privacy/policy-privacy-and-data-governance.md`](../../privacy/policy-privacy-and-data-governance.md), and the individual-rights clocks in [`compliance/healthcare/procedure-hipaa-operational-compliance.md`](procedure-hipaa-operational-compliance.md) |

Obligations the adopter meets outside the library:

1. **The organization's HIPAA risk analysis and risk management** (164.308(a)(1)). The library's risk-assessment methodology is the input; the HIPAA-specific analysis, and its documentation, are the organization's own artefact.
2. **The business associate agreement** (164.314(a), 164.504(e)). A per-relationship contract; the library does not ship a BAA template.
3. **The HHS OCR breach-portal submission** (164.408). An external process on the HHS website.
4. **The Notice of Privacy Practices** (164.520). A published, organization-specific notice.
5. **Six-year documentation retention** (164.316(b), 164.530(j)). The library's records-retention standard is the mechanism; the HIPAA-specific retention schedule is applied on top.

---

## Enforcement and penalties

HHS OCR enforces HIPAA. Civil money penalties are set on a four-tier culpability structure (45 CFR 160.404):

| Tier | Culpability |
| --- | --- |
| 1 | The organization did not know, and by exercising reasonable diligence would not have known, of the violation |
| 2 | The violation was due to reasonable cause and not to willful neglect |
| 3 | The violation was due to willful neglect but was corrected within the 30-day period beginning when the organization knew or should have known of it |
| 4 | The violation was due to willful neglect and was not corrected within that 30-day period |

The per-violation amounts and the annual cap for identical violations rise across the tiers. This annex does not state a dollar figure: the amounts codified in 160.404 are statutory base figures that HHS adjusts for inflation annually and publishes at **45 CFR part 102**, so a current figure is taken from part 102 (or the current HHS OCR enforcement notice), not from a static citation. In determining an amount, the Secretary weighs the factors at 160.408 (the nature and extent of the violation and of the resulting harm, the organization's compliance history, its financial condition, and other matters justice may require). An affirmative defense is available where the violation was not due to willful neglect and was corrected within the 30-day period (160.410).

---

## Operating expectations

1. The organization completes and maintains a current HIPAA risk analysis (164.308(a)(1)) and drives its safeguard implementation from it; the library's risk-assessment methodology is the input, not a substitute.
2. Each safeguard implementation traces to a library document and to any organization-specific extension, using the NIST SP 800-66r2 crosswalk as the bridge from the Security Rule standard to the control.
3. Business associate agreements are executed before PHI is shared, and flow-down agreements are obtained from subcontractors (164.308(b), 164.314(a)).
4. The incident-response process recognizes the HIPAA breach-determination test and the 60-day and 500-individual notification thresholds, layered on the library's incident lifecycle.
5. HIPAA documentation is retained for six years from creation or last-effective date, whichever is later (164.316(b), 164.530(j)).
6. The organization tracks the status of the proposed Security Rule revision and does not implement to it as though it were in force until it is finalized.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| HIPAA Security Rule | 45 CFR 164 Subpart C | Safeguard obligations for ePHI |
| HIPAA Privacy Rule | 45 CFR 164 Subpart E | Use-and-disclosure and individual-rights obligations |
| HIPAA Breach Notification Rule | 45 CFR 164 Subpart D | Breach determination and notification |
| HIPAA Enforcement / Civil Money Penalties | 45 CFR 160 Subparts C and D | Investigation and penalty structure |
| HIPAA Administrative Simplification identifiers | 45 CFR 162 | Transactions, code sets, and the National Provider Identifier |
| HITECH Act | 42 U.S.C. 17921 et seq. | Strengthens HIPAA; breach notification; enhanced penalties |
| NIST SP 800-66r2 | Implementing the HIPAA Security Rule (February 2024) | Security Rule implementation crosswalk |
| NIST SP 800-53 Rev. 5 | Security and Privacy Controls | Underlying control catalogue the library baselines align with |

---

## Limitations

This annex is a CC BY-SA 4.0 navigation aid. HIPAA compliance requires the organization's own risk analysis, policies, business associate agreements, Notice of Privacy Practices, and retained documentation, none of which this library produces on the organization's behalf. The annex states obligations by section identifier and does not reproduce the regulatory text; adopting organizations consult 45 CFR Parts 160, 162, and 164, the HHS OCR guidance, the inflation-adjusted penalty figures at 45 CFR part 102, and the status of the proposed Security Rule revision before relying on any obligation stated here. This annex is not legal advice.

---

**End of Document**
