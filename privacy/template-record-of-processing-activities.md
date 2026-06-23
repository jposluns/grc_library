# Record of Processing Activities Template

**Document Title:** Record of Processing Activities Template\
**Document Type:** Template\
**Version:** 1.0.5\
**Date:** 2026-06-23\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/charter-privacy-management-programme.md`](charter-privacy-management-programme.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](procedure-privacy-impact-and-cross-border-transfer.md), [`privacy/register-cross-border-data-flow.md`](register-cross-border-data-flow.md), [`governance/register-data-retention-schedule.md`](../governance/register-data-retention-schedule.md), [`supply-chain/register-subprocessor-template.md`](../supply-chain/register-subprocessor-template.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material processing, jurisdiction, supplier, or regulatory change\
**Repository Path:** [`privacy/template-record-of-processing-activities.md`](template-record-of-processing-activities.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organisation uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customisation guidance.

---

## Purpose

This template defines the structure of a Record of Processing Activities (ROPA) sufficient to satisfy GDPR Article 30 and equivalent record-keeping obligations under UK GDPR, LGPD, PIPEDA, CPPA, PIPL, and similar privacy regimes. It provides separate field sets for the controller view and the processor view. Adopting organisations populate one row per processing activity per controller or processor role.

A populated ROPA is sensitive operational data and must not be published in this public CC BY-SA 4.0 repository. Use this template structurally; populate, classify, and store internally.

---

## Scope

This template applies to every processing activity carried out by the organisation or on its behalf where personal data is involved. Each processing activity is described as a discrete row keyed by activity identifier. Each row identifies its applicable jurisdiction or jurisdictions, processing role, and authoritative system of record.

---

## Controller view (GDPR Article 30(1))

| Field | Description | Notes |
| --- | --- | --- |
| Activity ID | Unique identifier within the ROPA | Use a stable identifier; do not reuse on activity termination |
| Activity name | Short human-readable name | Avoid product or vendor names |
| Business owner role | Role accountable for the activity | Role-based; not a named individual |
| Privacy contact role | Role responsible for the privacy aspect | Typically the Data Protection Officer (organisation-wide) or a domain privacy lead |
| Purposes of processing | All purposes for which the data is processed | One row may carry multiple purposes; granular description |
| Lawful basis (per jurisdiction) | Lawful basis under each applicable regime | E.g. GDPR Art 6(1)(b) contract; PIPEDA Schedule 1 Principle 3 consent (CPPA Sec 12 consent is proposed, not in force) |
| Categories of data subjects | Customer, employee, supplier, prospect, visitor, child, patient, etc. | Identify children separately where applicable |
| Categories of personal data | Identifying, contact, demographic, financial, health, biometric, location, behaviour, derived | Identify special-category data separately |
| Source of data | Subject directly, supplier, public source, derived, sensor | Where data is not collected from the subject, this triggers Article 14 information duty |
| Recipients | Internal teams, processors, sub-processors, partners, joint controllers, regulators | Cross-reference to the subprocessor register |
| Third-country transfers | Country, mechanism (adequacy, SCC, BCR, derogation), TIA reference | Cross-reference to the cross-border data flow register |
| Retention period | Per-purpose retention period | Cross-reference to the data retention schedule |
| Deletion mechanism | Automated, manual, cascaded | Note whether deletion is enforceable end-to-end including backups, embeddings, caches |
| Technical and organisational measures | Encryption at rest and in transit, access control, logging, pseudonymisation, monitoring | High-level reference; not a control catalogue |
| Risk tier | Tier classification under the organisation's privacy risk methodology | Drives DPIA threshold |
| DPIA reference | Identifier of the impact assessment if one is required | None if the activity is below threshold |
| Last reviewed | Date of last ROPA review for this row | At least annually |

---

## Processor view (GDPR Article 30(2))

| Field | Description | Notes |
| --- | --- | --- |
| Activity ID | Unique identifier | Distinct from controller-view IDs |
| Controller (customer) name | Generic in this template; populated as customer organisation in adopter use | Public CC BY-SA 4.0 versions do not name controllers |
| Categories of personal data | As specified by the controller | The processor cannot expand scope without instruction |
| Categories of data subjects | As specified by the controller | |
| Sub-processors engaged | Sub-processor name (in private use), service, country, contract date | Cross-reference to the subprocessor register |
| Transfers to third countries | Mechanism per transfer | Cross-reference to cross-border data flow register |
| Technical and organisational measures | TOMs the processor commits to in the data processing agreement | |
| Contract reference | Data processing agreement identifier | Private record only |
| Audit rights | As defined in the contract | |
| Sub-processor notification commitment | Days notice prior to engaging a new sub-processor | |
| Last reviewed | Date | At least annually |

---

## Field-level guidance

1. **Lawful basis per jurisdiction.** The same activity may rely on different lawful bases in different jurisdictions. Record each separately rather than collapsing into a single statement.
2. **Special-category data.** GDPR Article 9 and equivalents impose additional conditions. Identify special-category data separately and record the Article 9 condition where applicable.
3. **Children's data.** Where data subjects include children under the age of consent in any applicable jurisdiction, identify this on the row and cross-reference the children's data framework.
4. **Automated decision-making.** Where the activity includes automated decision-making with legal or similarly significant effect, cross-reference the automated decision-making register.
5. **Retention.** The retention period is the operational retention; legal hold extensions are recorded separately on the activity record at the time the hold is invoked.

---

## Operating expectations

1. ROPA entries are added when a new processing activity is launched and removed (or marked decommissioned) when the activity ends.
2. Material changes to an activity (new purpose, new lawful basis, new third-country transfer, new sub-processor) require a ROPA update within the same review cycle.
3. The ROPA is reviewed at minimum annually and at every supervisory authority request.
4. The populated ROPA is retained for at least three years after the last related processing activity ends, or longer where regulatory or contractual rules apply.
5. Supervisory authorities may request the populated ROPA; the Data Protection Officer owns submission within the authority's requested window.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| GDPR | Article 30 | Records of processing activities |
| UK GDPR | Article 30 | Equivalent obligation |
| ISO/IEC 27701:2025 | Records of PII processing (section numbering changed in 2025 standalone revision) | Privacy information management |
| LGPD | Article 37 | Record of operations |
| CPPA | Schedule 2 (proposed) | Record-keeping |
| PIPL | Article 55 | Compliance audit and recording |
| NIST Privacy Framework | CT.PO-P5 | Identifying and inventorying data |

---

## Limitations

This template is a CC BY-SA 4.0 structural baseline. Adopting organisations must validate field coverage against the specific obligations of their applicable jurisdictions, sectors, and processing roles. The template is not a substitute for legal advice. Populated ROPAs are operationally sensitive; this CC BY-SA 4.0 template does not contain example values for any field.

---

**End of Document**
