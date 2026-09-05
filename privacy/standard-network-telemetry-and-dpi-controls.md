# Network Telemetry and DPI Controls Standard

**Document Title:** Network Telemetry and DPI Controls Standard\
**Document Type:** Standard\
**Version:** 0.1.1\
**Date:** 2026-09-05\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-workforce-network-monitoring.md`](../security/policy-workforce-network-monitoring.md), [`privacy/standard-presence-inference-limitations.md`](standard-presence-inference-limitations.md), [`security/policy-byod.md`](../security/policy-byod.md), [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`operations/standard-observability-and-telemetry.md`](../operations/standard-observability-and-telemetry.md), [`privacy/standard-pseudonymization-and-anonymization.md`](standard-pseudonymization-and-anonymization.md), [`governance/register-data-retention-schedule.md`](../governance/register-data-retention-schedule.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, employment-law, framework, or monitoring-technology change\
**Repository Path:** [`privacy/standard-network-telemetry-and-dpi-controls.md`](standard-network-telemetry-and-dpi-controls.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customization guidance.

---

## 1. Purpose

This standard defines the technical controls applied to network telemetry used in workforce network monitoring: flow telemetry (connection and traffic metadata) and deep-packet-inspection (DPI) telemetry (telemetry derived from inspecting packet content). It sets requirements for how such telemetry is scoped, minimized, and configured so that the collection stays confined to metadata wherever the aim allows, by default excludes special-category-revealing data and personal-device traffic before that data enters the pipeline (subject only to the narrow, documented, approval-gated exception this standard defines for special-category data), and, where telemetry is aggregated, resists re-identification.

This standard implements the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) and adds technical controls under that policy's authority. It does not itself authorize collecting any telemetry: whether a given monitoring capability may collect network flow or DPI data at all is a question of legitimate aim, necessity, lawful basis, notice, and proportionality that the parent policy governs (Sections 3, 4, and 5). Network telemetry collection is itself an intrusion on workforce privacy that the parent policy governs; this standard constrains how a capability the parent policy has authorized is built and configured. Where a signal reaches the interpretation of presence as a measure of work, the [Presence Inference Limitations Standard](standard-presence-inference-limitations.md) applies in addition to this standard.

---

## 2. Scope

### 2.1 In scope

This standard governs the technical configuration of the following telemetry classes where they are collected from organization networks under the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md):

1. **Flow telemetry:** connection and traffic metadata that does not inspect payload content, for example NetFlow-style or IPFIX-style records (source and destination address, port, protocol, byte and packet counts, timing, and interface). This is metadata about a connection, not its content.
2. **DPI (content-inspecting) telemetry:** telemetry produced by inspecting packet payloads or reconstructing application-layer content, whether for security detection, data-leakage prevention, or protocol analysis. DPI is content inspection within the meaning of the parent policy and is subject to that policy's limits on content inspection (Section 3, item 4, and Section 4, item 6).

These telemetry classes overlap the network-traffic-metadata and security-signal classes the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) (Section 2.1) places in scope; this standard does not expand that scope. Where this standard and the parent policy describe the telemetry differently, the parent policy governs.

### 2.2 Out of scope

1. **Personal and BYOD devices and traffic**, except the organization-resource interaction, are excluded from this standard's telemetry, both flow (metadata) telemetry and DPI (content) inspection, except the organization-resource interaction, consistent with the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) (Section 2.2) and the [Bring Your Own Device (BYOD) Policy](../security/policy-byod.md). See Section 5, "Personal-device and BYOD exclusion".
2. **Operational-health and capacity telemetry** (metrics, latency, saturation) not collected for security or compliance purposes, which is governed by the [Observability and Telemetry Standard](../operations/standard-observability-and-telemetry.md), not this standard.
3. **The security detection logic** that consumes telemetry and the incident and insider-risk processes that act on it, which operate under the [Logging and Monitoring Standard](../security/standard-logging-and-monitoring.md), the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md), and the insider-risk framework. This standard governs the telemetry controls; it does not govern the downstream investigative use of telemetry, which those documents govern.
4. **The interpretation of presence signals as a measure of work**, which is governed by the [Presence Inference Limitations Standard](standard-presence-inference-limitations.md).
5. **The legal-basis, necessity, and notice questions** for whether a capability may collect at all, which the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) governs.

---

## 3. Definitions

| Term | Definition |
| --- | --- |
| Flow telemetry | Connection and traffic metadata that records the existence and characteristics of a network flow (addresses, ports, protocol, counts, timing) without inspecting payload content. |
| Deep packet inspection (DPI) | Inspection of packet payload or reconstructed application-layer content, as distinct from inspection of connection metadata alone. |
| Content telemetry | Telemetry derived from the content of a communication or transfer, as opposed to metadata about it. DPI telemetry is content telemetry. |
| Special-category data | Personal data that, under the applicable regime, reveals or concerns categories the regime protects at a heightened level (for example health, racial or ethnic origin, religious or philosophical beliefs, political opinions, trade-union membership, genetic data, biometric data processed for the purpose of uniquely identifying a natural person, or data concerning sex life or sexual orientation). |
| Special-category-revealing telemetry | Telemetry that, though not itself a health or belief record, reveals or allows inference of special-category data, for example a flow record showing a connection to a site or service associated with a specific health condition, religion, trade union, or sexual orientation. |
| Ingestion | The point at which telemetry enters the monitoring pipeline for storage, indexing, correlation, or analysis. |
| Minimum cohort size | A configurable threshold (a k-anonymity-style minimum) below which an aggregate is suppressed or further generalized so that no aggregate value is effectively attributable to one identifiable individual. |
| Differencing attack | Re-identification of an individual by comparing two or more aggregates (for example the same aggregate before and after one person joins or leaves a cohort, or two overlapping cohorts) so that the difference isolates that individual. |
| Aggregate form | Telemetry combined across a group such that no value is attributable to an identified or identifiable individual. |

---

## 4. Relationship to the parent policy and to lawful basis

1. **This standard implements the parent policy; it does not supersede or override it.** The [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) is the authority for what monitoring is permitted, for the lawful basis of each capability, and for the prohibited uses of monitoring signals. This standard adds technical controls on the telemetry under that authority. Where this standard and the parent policy (or another authoritative document, including a specific legal obligation) appear to differ, the parent policy governs, the difference is escalated for resolution, and a specific legal obligation prevails where one applies.
2. **A control here is not an authorization to collect.** The controls in this standard bound how telemetry is scoped and configured; they do not establish that any telemetry may be collected. A legitimate aim is necessary but not sufficient, and a separate lawful basis under the applicable privacy and employment law is required for each capability that processes personal data, per the parent policy (Section 3 and Section 4) and the [Privacy and Data Governance Policy](policy-privacy-and-data-governance.md). Do not read a technical control in this standard as a lawful basis.
3. **Least intrusive means and metadata-first.** Consistent with the parent policy (Section 3), where an aim can be met with flow metadata rather than DPI content telemetry, the metadata option is used; DPI is the exceptional case governed by Section 5.

---

## 5. Requirements

### 5.1 Telemetry data minimization

1. Each telemetry capability collects the minimum fields necessary for its documented aim. Collection of a field "in case it is useful later" is not a legitimate basis, per the parent policy (Section 3, item 5).
2. Flow metadata is preferred over content telemetry wherever the aim can be met with metadata. DPI content inspection is exceptional, individually justified, time-bound, and narrowly scoped, and is approved under the parent policy's exceptional-content-inspection path (Section 4, item 6, requiring advance approval by the Chief Information Security Officer and Legal Counsel with the Data Protection Officer's independent advice, and never applied to legally privileged or protected communications).
3. Telemetry fields, their retention, and the aim they serve are recorded for each capability as part of its monitoring inventory entry under the parent policy (Section 6, item 1). Field selection is reviewed at each material change.
4. Where a field is collected only to support correlation or investigation, it is minimized to aggregate or de-identified form as early as the purpose allows, consistent with the parent policy (Section 8, item 5) and the [Pseudonymization and Anonymization Standard](standard-pseudonymization-and-anonymization.md).

### 5.2 Special-category exclusion at or before ingestion

1. By default, telemetry pipelines are configured to exclude special-category-revealing data at or before ingestion, not to collect it and filter it afterwards. The exclusion is a property of the pipeline design (for example, not resolving or retaining the specific destinations, hostnames, URLs, or content markers that would reveal a special category), applied before the data is stored, indexed, or correlated. This default applies even to fields the [Logging and Monitoring Standard](../security/standard-logging-and-monitoring.md) otherwise records (such as source, destination, or initiating identity): where such a field would reveal a special category, it is masked, suppressed, or excluded for the telemetry-privacy purpose this standard governs.
2. **DPI is not configured to reveal special-category data** except in the narrow case where all of the following are documented and approved before deployment: an Article 6 lawful basis, an applicable Article 9(2) condition (a legitimate security aim does not by itself satisfy Article 9), and approval under the parent policy's exceptional-content-inspection path. Where that narrow case applies, only the specific data the condition permits is processed, minimized to that purpose and handled under the safeguards the Article 9(2) condition requires; it is not ingested into general telemetry stores. Where any element is absent, the special-category-revealing configuration is not deployed and the default exclusion in item 1 governs.
3. This requirement applies to telemetry that *reveals* a special category by inference, not only to telemetry that records it directly. A flow record of a connection to a service associated with a specific health condition, religion, trade union, or sexual orientation is special-category-revealing and is treated under this requirement.
4. **Regime note.** The Article 9 analysis above states the EU position. The United Kingdom regime retains an equivalent special-category prohibition, but the conditions permitting such processing are set out under the UK regime (including the Data Protection Act 2018) and differ from the EU conditions; do not conflate the two. Adopters apply the special-category analysis required by each applicable jurisdiction's own regime (the applicable Article 9 conditions and any associated national conditions); see the [Privacy and Data Governance Policy](policy-privacy-and-data-governance.md). Where a jurisdiction annex does not set out those special-category conditions, the adopter applies the regime's requirements directly rather than relying on the annex.

### 5.3 Personal-device and BYOD exclusion

1. Personal and BYOD devices and their traffic are excluded from this standard's telemetry, both flow (metadata) telemetry and DPI (content) inspection, except the organization-resource interaction, consistent with the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) (Section 2.2, item 1) and the [Bring Your Own Device (BYOD) Policy](../security/policy-byod.md). Only the interaction with organization resources is in scope, and only to the extent the applicable device-access terms permit.
2. This is consistent with the boundaries the BYOD policy states for the mobile application management (MAM) model, under which the organization does not monitor personal application usage, browsing history, personal email, or personal files, and does not track device location (see the [Bring Your Own Device (BYOD) Policy](../security/policy-byod.md), "What the organization does not do"). Telemetry capabilities are configured so that inspection does not extend to personal-device traffic beyond the organization-resource interaction.
3. Where an organization operates a mobile device management (MDM) or managed-work-profile route that extends its reach on a personal device, telemetry within that route stays confined to the corporate container or work profile and to what the enrolment notice discloses; it does not extend to the personal partition of the device.

### 5.4 Minimum cohort size and differencing-attack defences

Where telemetry is used in aggregate form, the following configurable technical controls apply. Each has a default that the adopting organization sets in its control baseline; the defaults below are recommended starting points, not values prescribed by this standard or attributed to any external standard.

1. **Minimum cohort size.** An aggregate is produced or displayed only where the cohort contributing to it meets a configured minimum cohort size (a k-anonymity-style threshold). Below the threshold, the aggregate is suppressed or further generalized so that no value is effectively attributable to one identifiable individual. The recommended default aligns the minimum cohort size with the k-anonymity baseline in the [Pseudonymization and Anonymization Standard](standard-pseudonymization-and-anonymization.md) (k at minimum 5); the adopter may set a higher threshold and, for small-population or sensitive contexts, should.
2. **Differencing-attack defences.** Aggregation is configured to resist re-identification by differencing, that is, by comparing aggregates to isolate an individual. Configurable defences include: suppressing small cells; using stable, non-overlapping cohort definitions rather than cohorts that differ by a single member; restricting the ability to query the same population before and after a single individual joins or leaves; and, where the analytical question allows, applying generalization or calibrated noise consistent with the techniques in the [Pseudonymization and Anonymization Standard](standard-pseudonymization-and-anonymization.md).
3. **No re-individualization.** Aggregate telemetry analytics are not re-individualized to reach a judgement about a specific person, consistent with the [Presence Inference Limitations Standard](standard-presence-inference-limitations.md) (Section 5.4, item 2). The minimum-cohort and differencing controls reduce the risk that aggregate outputs are reduced back to an individual; they do not eliminate re-identification risk arising from linkage, attribute inference, singling-out, or auxiliary information. Where aggregate outputs are produced, the residual re-identification risk is assessed and managed under the [Pseudonymization and Anonymization Standard](standard-pseudonymization-and-anonymization.md).
4. **Configuration is recorded and reviewed.** The configured minimum cohort size, the differencing defences in force, and their rationale are recorded for each aggregate telemetry output and reviewed at each material change.

### 5.5 Retention and minimization

Network flow and DPI telemetry is retained only for as long as necessary for its stated purpose and is then destroyed or de-identified, consistent with the parent policy (Section 8) and the [Data Retention Schedule](../governance/register-data-retention-schedule.md). Retention periods are organization-defined and recorded in the retention schedule; they are not prescribed by this standard or attributed to any external standard. DPI content telemetry, being the more intrusive class, is retained for the shortest period consistent with its exceptional, time-bound justification.

---

## 6. Roles and responsibilities

| Role | Responsibility |
| --- | --- |
| **Chief Information Security Officer (CISO)** | Owns the parent monitoring capability; approves the technical scope of each telemetry capability; configures or directs the configuration of flow and DPI telemetry within the limits of this standard; joint approver, with Legal Counsel, of any exceptional DPI content inspection under the parent policy (Section 4, item 6). |
| **Data Protection Officer (DPO)** | Independently advises on and reviews the lawful basis, special-category exclusion, minimization, and aggregation controls for each telemetry capability; advises on the special-category and cross-jurisdiction analysis in Section 5. Acting as an independent adviser, the DPO does not determine or approve the telemetry capabilities themselves. |
| **IT / Network Operations** | Configures telemetry pipelines to implement the exclusions and controls in this standard: special-category exclusion at or before ingestion (Section 5), personal-device and BYOD exclusion (Section 5), and the minimum-cohort and differencing defences (Section 5); records the configured fields, thresholds, and defences. |
| **Telemetry and analytics owners** | Define telemetry outputs and aggregates only for a documented, legitimate aim under the parent policy; attach and maintain the minimum-cohort and differencing configuration; submit each new or materially changed telemetry capability for DPO review before use. |
| **Legal Counsel** | Advises on the special-category conditions and cross-jurisdiction position; joint approver, with the CISO, of any exceptional DPI content inspection. |
| **Internal Audit** | Provides independent assurance that special-category exclusion, personal-device exclusion, minimization, and the minimum-cohort and differencing controls are configured and effective, and that DPI content telemetry stays within its exceptional, approved, time-bound scope. |

---

## 7. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27001:2022 | A.5.34 Privacy and protection of personal identifiable information (PII) | Bounds the handling of personal data derived from network telemetry. |
| NIST CSF 2.0 | GV.OC Organizational Context; GV.PO Policy | Governs the organizational-context and policy constraints on telemetry. |
| NIST Privacy Framework 1.0 | CT.DM-P Data Processing Management; CT.DP-P Disassociated Processing | Field-level telemetry minimization and disassociation of flow data (k-anonymity and differencing defences) |
| CSA CCM v4.1 | DSP-08 Data Privacy by Design and Default; DSP-12 Limitation of Purpose in Personal Data Processing | Privacy-by-default in telemetry design and purpose limitation on telemetry. |
| GDPR (EU) | Article 5 (data minimization, purpose limitation, storage limitation); Article 6 (lawful basis); Article 9 (prohibition on processing special-category data absent an Article 9(2) condition); Article 25 (data protection by design and by default) | Aligns the standard's minimization, exclusion-by-design, and special-category-exclusion requirements. These principles inform the standard; the standard does not assert that any single article prescribes a specific threshold or field-level control, and a purpose or legitimate aim is not itself an Article 6 basis or an Article 9 condition. |
| UK GDPR | The UK retains an equivalent special-category prohibition; processing requires an Article 6 lawful basis, a UK GDPR Article 9 condition, and, for several of those conditions, an associated Data Protection Act 2018 Schedule 1 condition. The permitting conditions are set under the UK regime and are not identical to the EU conditions. | Do not conflate the EU and UK special-category regimes. |

---

## 8. Limitations

This standard is a CC BY-SA 4.0 baseline. It defines technical controls on network flow and DPI telemetry; it does not authorize any monitoring, does not establish a lawful basis, and does not define the security detection logic that consumes telemetry. The minimum-cohort size and differencing defences are configurable controls whose defaults the adopting organization sets; low-population or sensitive contexts may require stricter thresholds. Adopting organizations must validate the framework mappings and the applicable privacy and employment law for their jurisdictions, including the special-category analysis, which differs between the EU and UK regimes. This standard implements, and does not supersede, the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md); where this standard and the parent policy or another authoritative document appear to differ, the parent policy governs, the difference is escalated for resolution, and a specific legal obligation prevails where one applies.

---

**End of Document**
