# Employee Monitoring Notice Template

**Document Title:** Employee Monitoring Notice Template\
**Document Type:** Template\
**Version:** 0.1.1\
**Date:** 2026-09-04\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-workforce-network-monitoring.md`](../security/policy-workforce-network-monitoring.md), [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/template-privacy-notice.md`](template-privacy-notice.md), [`privacy/annex-legitimate-interest-employment-monitoring.md`](annex-legitimate-interest-employment-monitoring.md), [`privacy/standard-presence-inference-limitations.md`](standard-presence-inference-limitations.md), [`privacy/standard-network-telemetry-and-dpi-controls.md`](standard-network-telemetry-and-dpi-controls.md), [`privacy/procedure-data-subject-rights-management.md`](procedure-data-subject-rights-management.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, employment-law, framework, or monitoring-technology change\
**Repository Path:** [`privacy/template-employee-monitoring-notice.md`](template-employee-monitoring-notice.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customization guidance.

---

## Purpose

This template defines the structure of the plain-language notice an organization gives its personnel about workforce network monitoring. It is the transparency instrument that the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) (Section 5, Transparency and notice) requires, and it delivers the advance-disclosure and right-to-object information that the [Legitimate Interest Assessment for Employment Monitoring Annex](annex-legitimate-interest-employment-monitoring.md) (Section 6.3 and Section 7) treats as a required baseline measure of the balancing analysis.

This template specializes the general [Privacy Notice Template](template-privacy-notice.md) for one context, workforce network monitoring; it does not replace it. This monitoring notice supplements the organization's general workforce privacy notice and cross-references it; the general notice, not this monitoring notice, carries the complete Article 13 and 14 information fields (the controller and Data Protection Officer contact details, the categories of recipients and any international transfers, the retention criteria, the full set of data-subject rights, and the source of any indirectly-collected data). Where no general workforce privacy notice is in place, those fields are added to this notice so that, together, the Article 13 and 14 duties are met.

A populated employee monitoring notice is a workforce-facing document specific to an organization; this template intentionally contains no organization-specific content. Adopters populate the bracketed placeholders, validate the lawful-basis selection and jurisdictional coverage with the Data Protection Officer and Legal Counsel, and deliver the notice through the channels described in Operating expectations.

This template implements, and does not supersede, the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md). Where a populated notice and the parent policy (or another authoritative document, including a specific legal obligation) appear to differ, the parent policy governs, the difference is escalated for resolution, and a specific legal obligation prevails where one applies. The notice describes monitoring; it does not authorize it and does not by itself establish a lawful basis.

---

## Scope

This template applies wherever the organization monitors workforce network activity within the meaning of the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) and needs to inform personnel of that monitoring. It covers a standing notice (published and delivered to all personnel) and a just-in-time notice (a short notice delivered at the point of collection); the just-in-time variant is set out in its own section below.

The notice is written to be read by the workforce, not by lawyers. It is accurate about what is and is not monitored, states the purpose separately from the lawful basis, and does not overstate or understate the monitoring the organization performs.

---

## Required content blocks

Each employee monitoring notice instantiated from this template must contain the following blocks. The order may be adjusted for readability, but no block may be omitted unless the omission is documented and justified with the Data Protection Officer.

### 1. Who monitors, and who to contact

State, in plain language:

- The organization (legal entity) responsible for the monitoring: [organization legal name].
- The function that owns the monitoring capability: [monitoring owner, for example the Chief Information Security Officer or the Security Operations function], and how to reach it: [contact route].
- The Data Protection Officer, who is your contact point for privacy questions and objections: [DPO name or office], [DPO contact route, for example an email and a postal address]. The Data Protection Officer independently advises on and reviews the monitoring; the DPO is your route for questions and concerns, and is not the person who approves or runs the monitoring.

### 2. What is monitored, and what is not

State the monitoring scope accurately. Mirror the in-scope and out-of-scope boundaries of the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) (Section 2) exactly; do not draw a wider or a narrower boundary.

**What is monitored.** On organization-owned or managed devices, networks, and services, and for security and compliance purposes, the organization collects:

- network traffic metadata (which systems connect to which, how much, when, and using what protocol), connection, session, and sign-in telemetry;
- security signals generated by endpoints, the network, and cloud services in the course of work; and
- presence and availability signals derived from network connection or system sign-in.

This applies wherever your activity traverses or connects to organization systems or networks, including from an office, from home, and while travelling.

**What is not monitored.**

- **The content of your communications is not routinely inspected.** Baseline monitoring works on metadata and security signals, not on the content of what you write or read. Content is inspected only in rare, specifically approved, time-bound, and narrowly scoped circumstances under the parent policy (Section 4, item 6), and the content of legally privileged or protected communications is never inspected (parent policy Section 7).
- **Your personal devices, personal accounts, and personal premises are not monitored.** If you connect a personal device to organization resources, only that interaction with organization resources is in scope, and only to the extent your device-access terms permit. This exclusion covers both connection metadata and any content inspection.
- **Routine HR and performance management is not a purpose of this monitoring.** Monitoring signals are not the organization's way of managing your performance; that is handled separately through HR management processes.
- **Presence is not treated as proof of work.** Signals showing that your device or account is connected, how long a session lasts, or when you sign in indicate connection, not the work you performed or its value. The organization does not use these signals to measure or compare individual output (see block 6, and the [Presence Inference Limitations Standard](standard-presence-inference-limitations.md)).
- **Sensitive-category information is excluded by design.** Monitoring is configured by default to leave out information that would reveal sensitive matters about you (for example health, religious or philosophical beliefs, political opinions, trade-union membership, or sexual orientation); any narrow, specifically approved exception is handled under the conditions the [Network Telemetry and DPI Controls Standard](standard-network-telemetry-and-dpi-controls.md) (Section 5.2) sets.

### 3. Why the organization monitors (the purpose)

State the specific, legitimate aim the monitoring serves. The purpose is stated here separately from the lawful basis in block 4; a legitimate aim explains why the organization monitors, but it is not by itself the legal ground for doing so.

Typical aims, to be tailored to the organization: to keep organization systems, networks, and data secure; to protect the integrity and availability of those systems; to detect and respond to security threats; and to meet the organization's legal and regulatory obligations. State the aims that actually apply: [list the organization's monitoring aims]. The organization does not monitor "in case it is useful later"; each monitoring capability serves a stated aim.

### 4. The lawful basis

State the legal ground for the monitoring, separately from the purpose above, and for each jurisdiction the notice covers. Work the EU and United Kingdom positions separately; do not merge them.

- **The usual basis is legitimate interests.** For most workforce monitoring the organization relies on its legitimate interests (GDPR / UK GDPR Article 6(1)(f)), balanced against your interests, rights, freedoms, and reasonable expectations. That balancing is documented in the organization's legitimate interest assessment for monitoring; the method is set out in the [Legitimate Interest Assessment for Employment Monitoring Annex](annex-legitimate-interest-employment-monitoring.md). Because this basis is used, you have the right to object (block 7).
- **Consent is not the basis.** In an employment relationship, consent is generally not a valid basis for monitoring, because the imbalance of power between employer and employee means consent cannot be freely given. The organization does not rely on your consent for monitoring, and signing this notice, acknowledging the acceptable-use policy, or continuing in employment is not treated as consent to monitoring.
- **Where another basis applies.** A specific monitoring activity may instead rest on a legal obligation or another Article 6 basis; where it does, that basis is stated for that activity: [state any activity-specific basis].
- **Jurisdictional note.** [EU]: monitoring that processes personal data relies on an Article 6 basis; where a Member State has introduced more specific employment rules under GDPR Article 88, those rules also apply. [United Kingdom]: monitoring relies on a UK GDPR Article 6 basis; UK GDPR Article 88 is not adopted, so there is no UK employment-specific Article 88 regime, and UK employment monitoring relies on the general lawful-basis analysis. [Other jurisdictions]: the legitimate-interest default above is EU/UK-specific and does not carry over automatically. Some regimes have no legitimate-interest basis and rest instead on a specific legal authorization or express consent (for example Chile's Ley 19.628, where workforce monitoring relies on a legal authorization or the worker's express written consent), and some provide no controller legitimate-interest basis at all (for example Colombia's Ley 1581 de 2012); state the lawful basis under the applicable jurisdiction's privacy annex. [Populate the jurisdictions that apply to the organization.]

### 5. What data is collected, how long it is kept, and who can see it

- **Data collected.** State the categories of data collected by the monitoring described in block 2 (connection and traffic metadata, session and sign-in telemetry, security signals, and presence and availability signals). Identify any narrow, separately approved content inspection distinctly.
- **Retention.** State that monitoring data is kept only for as long as necessary for its stated purpose and is then destroyed or de-identified. Retention periods are set by the organization and recorded in the [Data Retention Schedule](../governance/register-data-retention-schedule.md), which is the source of truth for how long each category is kept; the periods are not fixed by this notice. Data kept for an active investigation is kept for the period that investigation needs plus any documented limitation period, and data under a legal hold is kept until the hold is lifted; otherwise monitoring data is kept no longer than its stated purpose requires.
- **Access.** State that access to monitoring data is restricted to the roles that need it for the stated purpose, that access is logged, and that access and use are reviewed. Line managers do not receive individual monitoring signals as a performance or presence measure.

### 6. What the organization will not do with monitoring data

State the following assurances plainly. They mirror the prohibited uses in the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) (Section 7).

- **No automated discipline.** A monitoring signal does not, by itself, discipline, rank, restrict, penalize, or otherwise take employment action against you. Any employment consequence that could follow from a monitoring signal requires a human to review and validate the signal against context first, and is handled through the applicable due-process procedure.
- **Presence is not proof of work.** Connection, session duration, sign-in timing, and activity volume are not used as a productivity or performance measure, and are not used to rank or compare individuals. These signals show connection, not contribution.
- **No secondary-purpose reuse.** Data collected for a stated monitoring purpose is not quietly reused for an unrelated purpose (for example HR, performance, or marketing). A new purpose would need its own legal basis, assessment, and notice.
- **No monitoring beyond scope.** Monitoring is not used to profile your lawful off-duty conduct, and does not extend to your personal devices, accounts, or premises beyond the narrow organization-resource interaction.
- **Monitoring is not covert.** The organization does not conduct covert or undisclosed monitoring under this notice.

### 7. Your rights, and how to raise a question or objection

State the rights that apply, and make the right to object prominent and separate from the rest of the notice, consistent with GDPR / UK GDPR Article 21(4).

- **Your right to object (GDPR / UK GDPR Article 21).** Where the organization monitors on the basis of its legitimate interests, you have the right to object, on grounds relating to your particular situation, to the processing of your data. If you object, the organization stops processing your data for that monitoring unless it can demonstrate compelling legitimate grounds that override your interests, rights, and freedoms, or the processing is needed for the establishment, exercise, or defence of legal claims. To object, contact [DPO or privacy contact route].
- **Your other rights.** Depending on your jurisdiction, you also have rights of access, rectification, erasure, restriction, and portability, rights concerning solely automated decisions, and the right to complain to your data protection supervisory authority: [name the authority or point to the jurisdiction annex]. To exercise a right, follow the [Data Subject Rights Management Procedure](procedure-data-subject-rights-management.md) or contact [privacy contact route].
- **Questions and concerns.** For any question about this monitoring, or to raise a concern, contact the Data Protection Officer at [DPO contact route]. You will receive a response within [response window].

### 8. Changes to this notice

State the version and date of the notice, and how personnel are told about material changes (for example an intranet notice, an email, or a formal communication). Material changes are communicated, not merely posted.

---

## Plain-language drafting requirements

1. The notice is written in plain language suitable for all personnel, not in legal or technical language. Where a technical or legal term is unavoidable, it is given a short plain-language explanation the first time it is used.
2. Sentences are short; paragraphs are short; headings describe what the section tells the reader.
3. The notice is accurate: it neither overstates the monitoring (to appear thorough) nor understates it (to appear benign). The scope in block 2 matches the parent policy exactly.
4. The purpose (block 3) and the lawful basis (block 4) are kept as distinct statements; the notice does not present a legitimate aim as though it were the legal basis.
5. Legal citations include enough context for a reader to follow, and the EU and United Kingdom positions are stated separately wherever they differ.
6. The notice is offered in every language required by applicable law or by the workforce it addresses, and each translation is locked to the version of the source-language notice it renders.

---

## Just-in-time notice variant

For a short notice delivered at the point of collection (for example a sign-in banner, an enrolment screen when a device connects to organization resources, or a first-use prompt for a monitored service), an abbreviated notice is acceptable provided it contains, in a few plain sentences:

1. **Who:** that [organization name] monitors activity on this organization system or network.
2. **What and why:** that it collects connection metadata, telemetry, and security signals for security and compliance purposes, and that it does not routinely inspect the content of communications and does not monitor personal devices beyond the organization-resource interaction.
3. **Lawful basis:** in EU/UK regimes, that the monitoring relies on the organization's legitimate interests (Article 6(1)(f)), not on your consent; in other jurisdictions, the basis that applies under that jurisdiction's annex (which may instead be a legal authorization or consent).
4. **Not a work measure:** that these signals are not used to measure your work and do not, by themselves, trigger any employment consequence.
5. **Your right to object, and where to go:** a clear pointer to the right to object and a link to the full monitoring notice and the rights information.

The just-in-time notice supplements the full notice; it does not replace it, and the full notice remains accessible from the point where the short notice is shown.

---

## Operating expectations

1. The monitoring notice is delivered to personnel before monitoring applies to them, at joining, and on an ongoing basis, coordinated with the awareness activities the parent policy (Section 5, item 5) requires.
2. The full notice is published and accessible to all personnel through every channel where the just-in-time notice appears.
3. The right to object is surfaced prominently and separately, at the latest at the first communication with the individual, consistent with GDPR / UK GDPR Article 21(4); a right buried in a general acknowledgement is not surfaced.
4. Where applicable law or agreement requires consultation with, or the agreement of, workforce representatives (for example works councils or trade unions) before monitoring is introduced or materially changed, that consultation is completed and its outcome recorded before the notice is relied on; the organization operates to the strictest applicable employment, privacy, and consultation rules across its footprint.
5. The notice is reviewed at least annually and upon any material change to the monitoring, its purpose, its lawful basis, the applicable jurisdictions, or the monitoring technology.
6. The Data Protection Officer maintains a change log for the notice, recording the version, the date, the jurisdictions affected, and a brief description of each change.
7. Translations are version-locked to the source-language notice.

---

## Framework alignment

The table maps only the controls this template substantively implements.

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27001:2022 | A.5.34 Privacy and protection of personal identifiable information (PII) | The notice is the transparency element of protecting personal data processed in monitoring: it informs personnel of the processing and their rights. |
| GDPR (EU) | Article 5(1)(a) transparency; Article 12 and the monitoring-specific elements of Articles 13 and 14 (controller identity, the purposes and the Article 6(1)(f) basis, the right to object); Article 6(1)(f) legitimate interests; Article 21 right to object; Article 88 processing in the context of employment | This notice delivers the Article 5(1)(a) transparency principle and the monitoring-specific elements of the Article 12 to 14 information duties; the complete Article 13 and 14 field set is carried by the general workforce privacy notice this notice supplements. It states the Article 6(1)(f) basis, surfaces the Article 21 right to object, and reflects the employment context Article 88 permits Member States to regulate. These provisions inform the notice; the notice does not assert that any single article prescribes its wording. |
| UK GDPR | Article 12 and the monitoring-specific elements of Articles 13 and 14 (the general workforce privacy notice carries the complete field set); Article 6(1)(f) legitimate interests; Article 21 right to object; Article 88 not adopted (UK employment monitoring relies on the general lawful-basis analysis); Article 22 replaced by Articles 22A to 22D (Data (Use and Access) Act 2025, in force 2026-02-05, see the [United Kingdom privacy annex](jurisdictions/annex-privacy-united-kingdom.md)) | The UK information-duty and automated-decision positions differ from the EU regime and are worked separately; do not conflate the two. |

---

## Limitations

This template is a CC BY-SA 4.0 baseline and is not legal advice. It provides the structure of a workforce monitoring notice; it does not authorize any monitoring, and it does not itself establish a lawful basis. The authority for what monitoring is permitted is the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md); the lawful-basis balancing method is the [Legitimate Interest Assessment for Employment Monitoring Annex](annex-legitimate-interest-employment-monitoring.md); the presence-signal and telemetry limits are the [Presence Inference Limitations Standard](standard-presence-inference-limitations.md) and the [Network Telemetry and DPI Controls Standard](standard-network-telemetry-and-dpi-controls.md). Adopting organizations must validate the lawful-basis selection, the jurisdictional coverage (including the EU and United Kingdom distinctions and any works-council, trade-union, or codetermination requirements), and the framework mappings for their operating jurisdictions with the Data Protection Officer and Legal Counsel before publishing a populated notice. This template implements, and does not supersede, the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md); where a populated notice and the parent policy or another authoritative document appear to differ, the parent policy governs, the difference is escalated for resolution, and a specific legal obligation prevails where one applies.

---

**End of Document**
