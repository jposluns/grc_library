# Cookie and Tracker Register

**Document Title:** Cookie and Tracker Register\
**Document Type:** Register\
**Version:** 1.0.6\
**Date:** 2026-07-16\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/framework-consent-management.md`](framework-consent-management.md), [`privacy/template-privacy-notice.md`](template-privacy-notice.md), [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/template-record-of-processing-activities.md`](template-record-of-processing-activities.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Quarterly and upon material change to website, mobile application, or marketing technology stack\
**Repository Path:** [`privacy/register-cookie-and-tracker.md`](register-cookie-and-tracker.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customization guidance.

---

## Purpose

This register inventories cookies, similar storage technologies, and tracking technologies operated on the organization's websites, mobile applications, embedded surfaces, and partner-integrated channels. It supports the consent management framework, the privacy notice, and the ePrivacy and equivalent obligations across the EU, UK, Brazil, and other jurisdictions with prior-consent or opt-in requirements for non-essential tracking.

A populated register identifies specific technologies and their providers and is operational data. This template is the structural baseline; populate, classify, and store internally.

---

## Scope

This register covers:

1. HTTP cookies set first-party or third-party on the organization's web properties.
2. Local storage, session storage, IndexedDB entries, and equivalent client-side storage technologies that contain identifiers or are used for tracking.
3. Mobile application equivalents (advertising identifiers, device identifiers, attribution SDKs).
4. Pixel and tracking-image technologies (single-pixel images, web beacons).
5. Server-side tracking and conversion APIs that link to a client-side identifier or to a subject identifier.
6. Fingerprinting techniques (canvas, audio, font, WebGL, network) used for identification or tracking.

---

## Category taxonomy

| Category | Definition | Consent requirement under EU and UK ePrivacy |
| --- | --- | --- |
| Strictly necessary | Used solely to deliver an explicitly requested service. Without these, the requested feature cannot function. | Exempt from prior-consent requirement |
| Functional | Remember user choices (language, region, accessibility preferences) that are not essential for service delivery | Prior consent required |
| Performance and analytics | Measure usage to improve services; first-party analytics with narrow scope may have a lighter regulatory footprint in some jurisdictions but the conservative position is to require prior consent | Prior consent required (conservative position) |
| Advertising and marketing | Track subjects across sites or sessions for targeted advertising, retargeting, attribution, or marketing measurement | Prior consent required |
| Social media | Embedded social platform widgets or share buttons that read or write identifiers | Prior consent required |
| Personalization | Content or product personalization outside the strictly necessary set | Prior consent required |
| Other | Any technology that does not fit the above categories | Default to prior consent required pending Data Protection Officer review |

---

## Register schema

Each entry is one row. Mandatory fields:

| Field | Description |
| --- | --- |
| Tracker ID | Unique identifier within the register |
| Name | Cookie name, storage key, pixel identifier, SDK identifier |
| Technology | HTTP cookie, local storage, session storage, IndexedDB, pixel, advertising identifier, attribution SDK, fingerprinting technique, server-side conversion API, other |
| Category | Per the taxonomy above |
| First or third party | First-party or third-party set |
| Provider | The party that operates the tracker (provider name kept generic in this public template) |
| Domain | The domain or host that sets or reads the tracker |
| Purpose | Plain-language purpose |
| Personal data collected | Identifying, behavioural, device, location, or none (where it is purely technical) |
| Data processed by | Internal team, processor, joint controller, independent controller |
| Cross-border transfer | Destination country and transfer mechanism, where applicable |
| Retention or expiry | Persistent or session; if persistent, the lifetime |
| Lawful basis | Strictly necessary (no consent), Consent, Legitimate interest (rarely applicable for trackers under ePrivacy) |
| Consent control reference | The consent management platform purpose or category that gates this tracker |
| Default state | Set on first visit by default (only valid for strictly necessary); otherwise blocked until consent |
| Opt-out mechanism | How a subject opts out after initially consenting |
| Audit trail | Date of last audit confirming the tracker is in scope and the row is current |
| Status | Active, paused, retired |

---

## Operating expectations

1. **No tracker without a register entry.** New marketing pixels, analytics tags, third-party SDKs, or fingerprinting techniques cannot be deployed without an entry in this register and a Data Protection Officer review.
2. **Default deny for non-essential.** On first visit, no non-essential tracker fires until the subject has given consent in the consent management platform.
3. **Granular categories.** Subjects can accept and reject categories individually. Single accept-all and reject-all controls coexist with the granular controls; reject-all is not less prominent than accept-all.
4. **No dark patterns.** Visual prominence, default selections, button labels, and friction levels are equivalent between accept and reject paths.
5. **Quarterly tag scan.** The Data Protection Officer commissions a quarterly automated scan of the website and mobile applications to detect undeclared trackers. Drift between the scan output and the register is treated as a defect and remediated.
6. **Third-party SDKs.** SDKs that perform tracking are subject to the supplier security and privacy assurance standard in addition to this register.
7. **Cross-jurisdiction differences.** Where the same tracker is permitted in one jurisdiction without consent and requires consent in another, the consent path is enforced wherever the subject is or may be in the consent-required jurisdiction.

---

## Metrics

| Metric | Definition | Target |
| --- | --- | --- |
| Register completeness against quarterly scan | Percentage of detected trackers present in the register | 100% |
| Default-deny adherence | Percentage of non-essential trackers blocked before consent on a sampled crawl | 100% |
| Reject path parity | Pass or fail of the dark-pattern equivalence test (reject path not less prominent than accept path) | Pass |
| Withdrawal honoured within SLA | Percentage of consent withdrawals reflected in tag firing within 24 hours | At least 99% |
| Third-party SDK assurance coverage | Percentage of registered third-party tracking SDKs with an in-date supplier assurance review | At least 95% |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ePrivacy Directive 2002/58/EC (and national transpositions) | Article 5(3) | Prior consent for non-essential storage and access |
| GDPR | Articles 6, 7, 13, 14 | Lawful basis, consent, transparency where personal data is involved |
| UK PECR | Regulation 6 | Cookie consent |
| LGPD | Articles 7, 8, 18 | Consent and information rights where personal data is involved |
| PIPL | Articles 13, 24 | Consent and automated behaviour analysis |
| CCPA / CPRA | Cal. Civ. Code s. 1798.135; CCPA Regs 11 CCR ss. 7025-7026 | Opt-out of sale or sharing; opt-out preference signals (s. 7025, the Global Privacy Control) and requests to opt out of sale/sharing (s. 7026) |
| Brazil ANPD Guidance | Cookies and similar technologies guidance | Local interpretation |

---

## Limitations

This register is a CC BY-SA 4.0 structural baseline. Adopting organizations must populate the rows with real trackers, integrate the register with their consent management platform configuration, validate jurisdictional positions with legal counsel where the position is contested (notably first-party analytics in the EU), and conduct the quarterly drift audit. The register is not legal advice.

---

**End of Document**
