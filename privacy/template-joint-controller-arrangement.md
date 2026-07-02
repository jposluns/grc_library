# Joint Controller Arrangement Template

**Document Title:** Joint Controller Arrangement Template\
**Document Type:** Template\
**Version:** 1.0.2\
**Date:** 2026-07-02\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/template-record-of-processing-activities.md`](template-record-of-processing-activities.md), [`privacy/template-privacy-notice.md`](template-privacy-notice.md), [`privacy/procedure-data-subject-rights-management.md`](procedure-data-subject-rights-management.md), [`privacy/procedure-data-protection-and-privacy-breach-response.md`](procedure-data-protection-and-privacy-breach-response.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](procedure-privacy-impact-and-cross-border-transfer.md), [`privacy/template-dpia.md`](template-dpia.md), [`privacy/register-cross-border-data-flow.md`](register-cross-border-data-flow.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material change to the joint processing arrangement, joint controllers, or applicable privacy regime\
**Repository Path:** [`privacy/template-joint-controller-arrangement.md`](template-joint-controller-arrangement.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customization guidance.

---

## Purpose

This template defines the structure of a **joint controller arrangement** sufficient to satisfy **GDPR Article 26** and equivalent obligations under UK GDPR. It also accommodates the analogous joint-controller or co-controller concepts in LGPD (Brazil, Article 5(VI) operadores conjuntos), India DPDP Act 2023, and PIPL (China, Article 20 joint personal information handlers). Adopting organizations populate one arrangement per joint-processing context.

A populated arrangement is a binding contractual instrument between joint controllers. It must be signed by authorized representatives of each party, retained as a legal record, and made available to data subjects in essence (see Section 9 below). The populated arrangement is sensitive operational data and must not be published in this public CC BY-SA 4.0 repository; use this template structurally and store the executed instrument internally.

---

## Scope

This template applies to every processing activity where **two or more controllers jointly determine the purposes and means** of the processing (Article 26(1)). Joint controllership is distinct from controller-processor (Article 28) and from independent controllers exchanging data: it requires the controllers to *jointly* determine *both* the purposes *and* the means.

Typical scenarios that trigger joint controllership:

- Two organizations co-design a joint marketing campaign using each party's customer data.
- A platform and a partner co-determine the purposes and means of analytics on shared user data.
- A research consortium jointly determines purposes (research questions) and means (protocols, data combination methods).
- An employer and a benefits provider jointly determine the purposes and means of an employee benefits programme.

Scenarios that are NOT joint controllership:

- A controller engages a service provider that processes data on the controller's documented instructions only (controller-processor, Article 28).
- Two independent controllers exchange personal data but each determines purposes and means for their own use (independent controllers, no joint arrangement required).
- A platform operator determines purposes and means for its platform; a tenant operator on that platform determines purposes and means for its tenant scope (separate controllers, no joint relationship).

When in doubt, conduct a joint-controllership assessment per Article 26(1) before assuming controller-processor; the EDPB Guidelines 07/2020 on the concepts of controller and processor provide the methodology.

---

## Field set

### Section 1: Joint controller identification

| Field | Description | Example |
|---|---|---|
| Arrangement ID | Unique identifier for this joint controller arrangement | JCA-2026-001 |
| Effective date | The date from which the arrangement takes effect | 2026-09-01 |
| Term | The period for which the arrangement applies (with renewal terms if any) | 3 years, renewable for 1-year periods |
| Joint Controller A | Legal name, registered address, jurisdiction of incorporation | <name>, <address>, <jurisdiction> |
| Joint Controller A, authorized representative | Name and title of signatory | <name>, <title> |
| Joint Controller A, DPO contact | Name, email, postal address of DPO (or equivalent privacy lead) | <name>, <email>, <postal> |
| Joint Controller A, EU representative | Where applicable per Article 27 | <name>, <address> |
| Joint Controller B | Legal name, registered address, jurisdiction of incorporation | <name>, <address>, <jurisdiction> |
| Joint Controller B, authorized representative | Name and title of signatory | <name>, <title> |
| Joint Controller B, DPO contact | Name, email, postal address of DPO | <name>, <email>, <postal> |
| Joint Controller B, EU representative | Where applicable per Article 27 | <name>, <address> |
| Additional joint controllers | Same field set repeated for each additional party | n/a or repeat |
| Lead supervisory authority | Per one-stop-shop or by allocation in the arrangement | <name of SA>, <country> |

Where more than two joint controllers exist, repeat the per-party field set.

### Section 2: Joint processing description

| Field | Description |
|---|---|
| Processing purpose(s) | The joint purposes determined by all parties. List each purpose as a separate item. |
| Categories of personal data | Identification data, contact data, demographic data, behavioural data, special categories per Article 9 (with the Article 9(2) legal basis if special categories are processed), criminal-conviction data per Article 10, etc. |
| Categories of data subjects | Customers, employees, prospects, members of the public, children, etc. |
| Approximate volume | Order-of-magnitude estimate of subjects in scope |
| Geographic scope | Jurisdictions where data subjects are located; jurisdictions where processing operations are carried out |
| Lawful basis (per purpose) | Article 6(1)(a) to (f); plus Article 9(2) where special categories; plus Article 10 conditions where criminal-conviction data. Where consent is the basis, identify who collects, who can demonstrate, and how withdrawal cascades to all joint controllers. |
| Means of processing | Systems, platforms, tooling jointly determined by the parties |
| Data flows | Identify which data flows between the joint controllers; the lawful basis for each flow; whether any cross-border transfer is involved |
| Retention period | Maximum retention; deletion or anonymization procedure; alignment between joint controllers' retention schedules |
| ROPA reference | Each joint controller maintains its own Article 30 ROPA referencing this joint arrangement |

### Section 3: Allocation of GDPR responsibilities

This section is the heart of the arrangement under Article 26(1): the parties **transparently determine** their respective responsibilities. The default allocation principle is: **the party closest to the data subject or to the trigger event is allocated the responsibility**, except where one party has materially better operational capacity.

| GDPR obligation | Article(s) | Responsible party (A / B / both / leader-then-coordinated) | Notes |
|---|---|---|---|
| Determination of lawful basis | Article 6(1); Article 9(2); Article 10 | Both (must agree) | Where the basis differs by category, document per category |
| Information to data subjects at collection | Article 13 | Party collecting the data; copies to other party | Where both collect, each provides own notice referencing the joint arrangement |
| Information where data not obtained from subject | Article 14 | Party originating the indirect collection | |
| Right of access | Article 15 | <A / B / both / lead and coordinate> | Per Article 26(3), data subjects may exercise rights against EITHER controller regardless of internal allocation; the allocation here is internal coordination, not a defence against the subject |
| Right to rectification | Article 16 | <A / B / both / lead and coordinate> | Cascading update mechanism between parties to ensure that consistency is maintained |
| Right to erasure | Article 17 | <A / B / both / lead and coordinate> | Both parties must delete; the leading party coordinates and verifies |
| Right to restriction | Article 18 | <A / B / both / lead and coordinate> | |
| Right to data portability | Article 20 | <A / B / both / lead and coordinate> | Data origin determines who exports |
| Right to object | Article 21 | <A / B / both / lead and coordinate> | Includes automated direct marketing |
| Rights re. automated decision-making | Article 22 | <A / B / both / lead and coordinate> | Where AI is involved, see also [`ai/policy-ai-compliance.md`](../ai/policy-ai-compliance.md) |
| Processor engagement and Article 28 contracts | Article 28 | Per party (each party contracts with its own processors) | Where a processor is shared, the arrangement names a single contracting party with the other as named beneficiary |
| Record of Processing Activities | Article 30 | Each party maintains its own | Both ROPAs cross-reference this arrangement |
| Cooperation with supervisory authority | Article 31 | Both (each cooperates with its lead SA and with any SA requesting information about the joint processing) | |
| Security of processing | Article 32 | Both (each is responsible for security in its own infrastructure; jointly responsible for security of inter-controller data flows) | Document the technical and organizational measures (TOMs) for each party |
| Breach notification to SA | Article 33 | Party first aware notifies the lead SA within 72 hours; jointly notify additional SAs where one-stop-shop does not apply | Each party also notifies its own DPO and Legal Counsel |
| Breach notification to data subjects | Article 34 | Lead party communicates; both parties acknowledge in their respective channels | |
| DPIA | Article 35 | Joint DPIA by both parties; lead drafter named in this arrangement | Where one party already has a DPIA covering similar processing, the joint DPIA may incorporate by reference |
| Prior consultation with SA | Article 36 | Joint, with the lead supervisory authority | See [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](procedure-privacy-impact-and-cross-border-transfer.md) Step 5.2 |
| DPO designation | Articles 37-39 | Each party designates its own DPO; this arrangement names both | Where the joint processing scope changes the threshold under Article 37(1), re-assess |
| Cross-border transfer safeguards | Articles 44-49 | Per party (each safeguards its own onward transfers); jointly responsible for transfers between the joint controllers where one is outside the EEA | List SCCs, BCRs, adequacy decisions, or Article 49 derogations applicable to each transfer |
| Contact point for data subjects | Article 26(1) | <named contact point> | Single contact point may be either party, or a shared inbox; published in the essence-of-arrangement notice (Section 9) |
| Joint and several liability awareness | Article 26(3) | Both acknowledge | Internal liability allocation (e.g., indemnity provisions) is contract law; toward the subject the parties are jointly and severally liable |

### Section 4: Operational coordination

| Item | Description |
|---|---|
| Communication channels | Primary email, secondary email, escalation phone, escalation chain between the joint controllers' DPOs and Legal Counsel |
| Routine meetings | Cadence and purpose (e.g., quarterly review meeting; monthly operational coordination) |
| Incident escalation | The escalation chain when one party identifies a privacy issue affecting the joint processing |
| Change management | Process for proposing, reviewing, and adopting changes to the joint processing (purposes, means, parties, data flows) |
| Audit rights | Each party's right to audit the other's compliance with this arrangement; frequency; scope; cost allocation |
| Sub-arrangement governance | Where one party further shares responsibility with a sub-party (e.g., a corporate affiliate), the conditions and notice requirements |

### Section 5: Liability and indemnification

Per Article 26(3), regardless of the internal allocation in Section 3, data subjects may exercise their rights against any one of the joint controllers. This means the joint controllers are jointly and severally liable toward the subject.

Internally, the parties may allocate liability via indemnity provisions:

| Field | Description |
|---|---|
| Indemnity scope | Which categories of claims each party indemnifies the other against (e.g., breach of allocation, processor mismanagement, supervisory authority fines) |
| Liability caps | Per-incident and aggregate liability caps if any |
| Notification of claims | The party named in a claim notifies the other within <N> business days |
| Cooperation in defence | Each party's obligation to cooperate in defence of regulatory or civil actions |
| Insurance | Cyber-insurance and professional-indemnity insurance maintained by each party |

Note: indemnity provisions are an internal liability allocation. They DO NOT reduce or defeat a data subject's right under Article 26(3) to exercise their rights against either controller.

### Section 6: Term and termination

| Field | Description |
|---|---|
| Initial term | <N> years from the effective date |
| Renewal | Automatic renewal for <N>-year periods unless terminated; notice of non-renewal <N> months before expiry |
| Termination for cause | Each party may terminate for material breach of this arrangement by the other; cure period <N> business days |
| Termination for convenience | Each party may terminate on <N> days' notice |
| Effect of termination | Each party returns or deletes personal data held under the joint processing per the data-deletion schedule; data subjects affected by the termination are notified per Article 13/14 amended notices |
| Survival | Indemnity provisions; confidentiality; supervisory authority cooperation obligations; data-subject rights honouring; audit-trail retention survive termination per the regulatory retention period |

### Section 7: Cross-regime alternatives

Joint controllership exists under several regimes with substantively similar requirements but distinct legal language. This template's Section 1-6 structure can be adapted as follows for non-EU jurisdictions:

| Regime | Equivalent concept | Notable variations |
|---|---|---|
| **UK GDPR** (UK) | Joint controllers (same as EU GDPR) | Information Commissioner's Office (ICO) is the lead supervisory authority |
| **LGPD** (Brazil) | Co-controllers / operadores conjuntos (Article 5(VI)) | ANPD is the supervisory authority; written arrangement required |
| **PIPL** (China) | Joint personal information handlers (Article 20) | Public notice of arrangement required; CAC is the supervisory authority |
| **India DPDP Act 2023** | Joint data fiduciaries | Data Protection Board of India is the supervisory authority |
| **PIPEDA** (Canada) | No formal "joint controller" concept; contractual allocation between controllers; OPC is the supervisory authority | Contractual best-practice mirrors GDPR Article 26 |
| **CCPA / CPRA** (California) | "Business-to-business" or "joint operators" patterns; agreement required for shared purposes | California Privacy Protection Agency (CPPA) is the regulator |

For multi-jurisdiction arrangements, the arrangement must satisfy the strictest applicable regime in each section.

### Section 8: Documentation and audit trail

The executed arrangement and all amendments are retained per the organization's privacy records retention schedule (typically 7+ years post-termination per [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md)).

Each amendment is dated, version-numbered, and signed by both parties. The audit trail of amendments must be preserved alongside the original arrangement.

The DPO of each joint controller is responsible for ensuring the arrangement is reflected in the party's Article 30 ROPA and Article 26(2) essence-of-arrangement publication.

### Section 9: Essence-of-arrangement publication (Article 26(2))

Article 26(2) requires the **essence** of the arrangement to be made available to the data subject. This is typically achieved by including a section in each joint controller's public privacy notice with the following elements:

1. The fact of joint controllership for the named processing activity.
2. The identities and contact details (including DPO contact details) of all joint controllers.
3. The categories of personal data and the joint purposes.
4. The data subject's right under Article 26(3) to exercise rights against either controller.
5. The contact point for data subjects exercising rights related to the joint processing (per Section 1).
6. The lawful basis for the joint processing.
7. The retention period.
8. Information on cross-border transfers if applicable.

The essence-of-arrangement notice does NOT publish the internal liability allocation (Section 5) or the internal operational coordination details (Section 4); those are internal contract terms.

---

## Use guidance

Joint controllers populate this template before the joint processing begins. The completed arrangement is signed by authorized representatives of each party and retained per Section 8.

The Article 26(2) essence-of-arrangement publication is added to each joint controller's public privacy notice using [`privacy/template-privacy-notice.md`](template-privacy-notice.md) at the time the joint processing begins.

A populated arrangement is sensitive contractual data. Adopters do NOT publish the populated arrangement in this repository or any equivalent public repository.

---

## Framework alignment

| Requirement | GDPR | UK GDPR | LGPD | PIPL | India DPDP 2023 |
|---|---|---|---|---|---|
| Joint determination of purposes and means | Article 26(1) | Article 26(1) | Article 5(VI) | Article 20 | Section 2(i) "Data Fiduciary" with joint construction |
| Transparent allocation of responsibilities | Article 26(1) | Article 26(1) | Article 39 | Article 20(2) | Section 4 (general accountability) |
| Essence-of-arrangement availability to subjects | Article 26(2) | Article 26(2) | Article 18 transparency principle | Article 17 information rights | Section 6 notice obligations |
| Joint and several liability toward subjects | Article 26(3) | Article 26(3) | Article 42 | Article 20(2) (joint liability) | Section 17 grievance mechanism |
| Contact point designation | Article 26(1) | Article 26(1) | Article 41 (DPO contact) | Article 52 (DPO contact) | Section 10 (Data Protection Officer for Significant Data Fiduciaries) |
