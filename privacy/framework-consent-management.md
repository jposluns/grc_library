# Consent Management Framework

**Document Title:** Consent Management Framework\
**Document Type:** Framework\
**Version:** 1.0.4\
**Date:** 2026-06-22\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/template-privacy-notice.md`](template-privacy-notice.md), [`privacy/register-cookie-and-tracker.md`](register-cookie-and-tracker.md), [`privacy/template-record-of-processing-activities.md`](template-record-of-processing-activities.md), [`privacy/procedure-data-subject-rights-management.md`](procedure-data-subject-rights-management.md), [`privacy/framework-childrens-data.md`](framework-childrens-data.md), [`privacy/annex-privacy-jurisdiction-index.md`](annex-privacy-jurisdiction-index.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material regulatory, jurisdictional, or product change\
**Repository Path:** [`privacy/framework-consent-management.md`](framework-consent-management.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organisation uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customisation guidance.

---

## Purpose

This framework defines the operating model for capturing, recording, refreshing, and honouring consent across the organisation. It distinguishes consent from other lawful bases, sets the validity standard, identifies the granularity required for different purposes, and defines the audit trail that supports a defensible position with supervisory authorities and data subjects.

This framework supports GDPR, UK GDPR, ePrivacy expectations, LGPD, PIPL, CPPA, COPPA, and equivalent regimes. It supports both web and mobile interfaces and in-product or service-channel consent flows.

---

## Scope

This framework applies to all consent collection from data subjects across all channels, products, services, and jurisdictions in which the organisation operates. It does not displace contractual, legitimate interest, vital interest, public task, or legal obligation lawful bases; where one of those bases is lawful and appropriate, consent is not required.

---

## When consent is the lawful basis

Consent is the lawful basis where:

1. The processing is voluntary in nature and not necessary for contract, legitimate interest, vital interest, public task, or legal obligation.
2. The subject has a free choice without negative consequences for refusal or withdrawal.
3. The processing falls within a category where consent is legally required (for example most ePrivacy cookie use cases, special-category data under GDPR Article 9, certain transfers, marketing communications under most regimes, and processing of children's data under COPPA and equivalents).
4. The subject's freely-given, specific, informed, and unambiguous indication is required.

Where consent is not appropriate (for example processing necessary to perform a contract), the organisation does not collect consent for that purpose; it identifies the actual lawful basis in the privacy notice and the ROPA.

---

## Validity standard

Consent must satisfy each of the following elements. Failure of any element invalidates the consent and the processing must stop or fall back to a different lawful basis.

| Element | Requirement |
| --- | --- |
| Freely given | No bundling with contract execution where the processing is not necessary for the contract. No detriment for refusal beyond the loss of the optional feature itself. No pre-ticked boxes or default-on switches. |
| Specific | A separate, granular indication per distinct purpose. One overall consent covering "marketing, analytics, and product personalisation" does not satisfy this element. |
| Informed | The subject has been given the controller identity, the purposes, the data categories, the third-party recipients, the international transfers, the retention, and the rights, before consent is captured. |
| Unambiguous | Captured through a clear affirmative action: ticked box, button press, biometric gesture, explicit utterance. Inactivity, silence, or continued browsing does not constitute consent. |
| Withdrawable | The subject can withdraw consent at any time through a route as easy as the route used to give it. Withdrawal has no retrospective effect on processing before withdrawal. |

---

## Granularity rules

1. Each purpose has a separate consent control. Bundling is prohibited except where multiple purposes are inseparable in the eyes of an informed subject (e.g. delivering a specific service whose nature requires the bundle).
2. Each third-party recipient category whose processing is independent of the controller has a separate consent control.
3. Each special-category data type has a separate consent control where consent is the Article 9 condition.
4. Profiling and automated decision-making with legal or similarly significant effect has its own consent control even where the underlying processing has another lawful basis.
5. Cookies and similar tracking technologies are governed by the cookie and tracker register; the consent control granularity matches the register.

---

## Consent record

Each consent capture event produces a record stored in the consent register. The record is the audit artefact for the organisation's lawful-basis claim.

| Field | Description |
| --- | --- |
| Consent ID | Unique identifier |
| Subject identifier | Internal subject identifier; not necessarily the public account identifier |
| Purpose | Specific purpose the consent covers |
| Granularity context | The product, feature, page, or in-product surface where consent was captured |
| Notice version | Version of the privacy notice in force at the time |
| Lawful basis claimed | Always "Consent" for entries in this register; cross-referenced to the ROPA |
| Capture mechanism | Web form, biometric gesture, in-product flow, IVR, paper signature, etc. |
| Affirmative action evidence | The user-interface state and the action taken (e.g. "checkbox ticked then Save pressed") |
| Capture timestamp (UTC) | |
| Locale and language | The language and locale in which the consent text was presented |
| Subject's jurisdiction at capture | As inferred from authentication, declared address, or geolocation |
| Withdrawal channel offered | Description of the route by which the subject can withdraw |
| Refresh interval | If applicable; consent is refreshed at this cadence |
| Linked privacy notice | Pointer to the exact version of the notice in force |
| Validity status | Active, Withdrawn, Expired, Superseded |
| Withdrawal timestamp (UTC) | If withdrawn |
| Withdrawal source | The channel the subject used to withdraw |

---

## Withdrawal

1. Withdrawal is available through the same channel through which consent was given, plus the privacy contact route published in the notice.
2. Withdrawal takes effect within 24 hours of receipt across all systems that rely on the consent.
3. Withdrawal is recorded in the consent register as a state change; the original consent record is retained for audit.
4. Withdrawal does not affect the lawfulness of processing before withdrawal.
5. Where the data has already been transferred to a third party or sub-processor, the controller communicates the withdrawal to the recipient within the same window.

---

## Refresh and expiry

Consent does not automatically expire under most regimes, but stale consent is a defensibility risk. Refresh consent under the following conditions:

| Condition | Refresh action |
| --- | --- |
| Material change to purpose or recipient category | New consent required before further processing under the changed purpose |
| Subject inactivity beyond a defined dormancy window | Pause processing and refresh consent on return |
| Material change to privacy notice that affects this purpose | Refresh consent rather than rely on tacit acceptance of the new notice |
| Lapse of a defined refresh interval where the regime requires periodic re-consent (e.g. certain marketing regimes, special-category processing) | Refresh per the interval |
| Subject moves to a jurisdiction with stricter requirements | Refresh under the stricter regime |

---

## Children's data

Where a subject is below the age of digital consent in the applicable jurisdiction, the consent of a parent or guardian is required and the consent record additionally captures the parental-consent verification mechanism. Cross-reference the children's data framework.

---

## Cookie consent under ePrivacy

For cookies and similar tracking technologies, consent is governed by the cookie and tracker register. Strictly necessary cookies do not require consent. All other categories require prior consent satisfying the validity standard above. Pre-ticked boxes, scroll-to-consent, and consent walls (where refusal degrades the core service disproportionately) are not valid.

---

## Operating expectations

1. Each consented purpose has a single owning role accountable for the consent flow's validity.
2. Material UI or text changes to a consent flow follow a Data Protection Officer review before release.
3. Consent capture flows are tested at least annually against the validity standard, including for accessibility (screen readers, high-contrast modes).
4. Consent records are retained for the lifetime of the processing plus the period in which a claim under applicable law could be brought.
5. The consent register is one of the artefacts presented during supervisory authority engagement.

---

## Metrics

| Metric | Definition | Target |
| --- | --- | --- |
| Consent flow validity score | Percentage of audited consent flows that pass the validity standard | 100% |
| Withdrawal honoured within SLA | Percentage of withdrawals reflected in dependent systems within 24 hours | At least 99% |
| Refresh adherence | Percentage of refresh-eligible consents refreshed within their refresh interval | At least 95% |
| Bundled-purpose violations | Count of consent flows that bundle distinct purposes | Zero |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| GDPR | Articles 4(11), 6(1)(a), 7, 8, 9(2)(a) | Consent definition, conditions, child consent, special-category consent |
| UK GDPR | Same articles | Equivalent provisions |
| ePrivacy Directive 2002/58/EC and national transpositions | Article 5(3) and member-state rules | Cookie and similar technologies consent |
| LGPD | Articles 7(I), 8 | Consent as lawful basis |
| PIPL | Articles 13, 14 | Consent definition and conditions |
| COPPA | 16 CFR 312 | Verifiable parental consent |
| CPPA | Sections 14, 18 (proposed) | Express versus implied consent |
| CCPA / CPRA | Section 1798.120 to 1798.121 | Opt-out and opt-in |
| ISO/IEC 29184:2020 | Online notice and consent | Consent capture structure |

---

## Limitations

This framework is a CC BY-SA 4.0 baseline. Adopting organisations must validate jurisdictional rules, integrate with their specific consent management platform, populate the per-purpose consent record fields, and confirm the dormancy and refresh intervals applicable to their regimes. The framework is not legal advice.

---

**End of Document**
