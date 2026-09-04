# Works Council and Employee Representative Consultation Procedure

**Document Title:** Works Council and Employee Representative Consultation Procedure\
**Document Type:** Procedure\
**Version:** 0.1.0\
**Date:** 2026-09-04\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-workforce-network-monitoring.md`](../security/policy-workforce-network-monitoring.md), [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/standard-presence-inference-limitations.md`](standard-presence-inference-limitations.md), [`privacy/standard-network-telemetry-and-dpi-controls.md`](standard-network-telemetry-and-dpi-controls.md), [`privacy/template-legitimate-interest-assessment.md`](template-legitimate-interest-assessment.md), [`privacy/annex-legitimate-interest-employment-monitoring.md`](annex-legitimate-interest-employment-monitoring.md), [`privacy/template-dpia.md`](template-dpia.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](procedure-privacy-impact-and-cross-border-transfer.md), [`governance/register-data-retention-schedule.md`](../governance/register-data-retention-schedule.md), [`governance/register-role-authority.md`](../governance/register-role-authority.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, employment-law, framework, or monitoring-technology change\
**Repository Path:** [`privacy/procedure-works-council-and-employee-representative-consultation.md`](procedure-works-council-and-employee-representative-consultation.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customization guidance.

---

## Purpose

This procedure defines the steps for consulting works councils and employee representatives where such consultation, or co-determination, is legally required before a workforce monitoring capability is deployed or materially changed. It operationalizes the consultation and co-determination requirement of the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) (Section 4, item 3, and the workforce-representatives role in Section 9), giving the steps, the information to provide, the evidence to retain, and the sign-off that demonstrate the duty was met.

The duty this procedure serves is a duty of national employment and co-determination law, and it varies by jurisdiction. There is no single global rule: some jurisdictions require co-determination (the representative body's agreement) before workforce monitoring may be introduced, some require information and consultation (a reasoned opinion where the regime provides for one, but not agreement), and some impose no representative-body duty at all. Accordingly, the first step of this procedure is to determine, for each applicable jurisdiction, whether consultation is required and in what form. This procedure governs how the consultation is conducted and evidenced; it does not determine that any monitoring is permitted, which the parent policy governs.

This procedure implements, and does not supersede, the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md); where this procedure and the parent policy or another authoritative document appear to differ, the parent policy governs, the difference is escalated for resolution, and a specific legal obligation prevails where one applies.

---

## Scope

1. Applies to the introduction of any new workforce monitoring capability, and to any material change to an existing capability, that is subject to the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md), where personnel of any affected jurisdiction may be represented by a works council, a trade union, or another statutory or agreement-based employee representative body.
2. Covers the determination of whether a consultation or co-determination duty applies; the identification of the representative body; the information to be provided; the conduct of the consultation or negotiation; the conclusion (a works agreement, a collective agreement, a reasoned opinion, or a documented finding of no duty); and the evidence and sign-off retained as the audit trail.
3. Applies across the organization's footprint. Where personnel are located in more than one jurisdiction, the determination and, where required, the consultation are performed per jurisdiction, and the organization operates to the strictest applicable employment, privacy, and consultation rules, consistent with the parent policy (Section 4, items 3 to 5).
4. Out of scope: whether a monitoring capability may be collected at all (legitimate aim, necessity, lawful basis, and notice), which the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) governs; the interpretation of presence signals as a measure of work, which the [Presence Inference Limitations Standard](standard-presence-inference-limitations.md) governs; and the technical telemetry controls, which the [Network Telemetry and DPI Controls Standard](standard-network-telemetry-and-dpi-controls.md) governs. This procedure does not create a consultation duty where none exists in law or agreement, and does not overstate a duty in a jurisdiction that imposes none (Step 6).

---

## Governance and accountability

| Role | Responsibility |
|---|---|
| Legal Counsel | Accountable for determining, per applicable jurisdiction, whether a consultation or co-determination duty applies and in what form (consultation, reasoned opinion, or agreement), and for confirming that the outcome reached satisfies the legal duty. Advises on and, where the organization so structures it, leads the negotiation. |
| Data Protection Officer (DPO) | Independently advises on and reviews the lawful basis, the balancing test, and the impact assessment that form part of the information provided to the representative body, and reviews the consultation record for privacy adequacy. Acting as an independent adviser and monitor, the DPO does not determine or approve the monitoring capability or the consultation outcome. |
| Chief Information Security Officer (CISO) | Owns the monitoring capability; provides the capability's aim, scope, data, safeguards, retention, and access detail for the information pack; does not deploy or materially change the capability until any required consultation or agreement is completed and recorded. |
| HR / People Operations | Coordinates the relationship with the works council, trade union, or other representative body; leads or supports the consultation or negotiation; maintains the consultation record. |
| Works council / employee representatives / recognized trade union | The counterparty to the consultation. Receive the information pack, participate in the consultation or negotiation, and, where the applicable regime is co-determination, must agree before the capability is deployed or changed. |
| Internal Audit | Provides independent assurance that the consultation duty was determined, that any required consultation or agreement was completed before deployment, and that the audit trail (Step 5) is retained. |

Deployment of a capability subject to a co-determination duty proceeds only after the required agreement is reached; where residual risk is accepted on any privacy dimension, that acceptance follows the canonical chain in [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md).

---

## Procedure

### Step 1: Determine whether consultation is legally required (trigger determination)

Before any consultation is scoped, and before the capability is deployed or materially changed, Legal Counsel determines, for each jurisdiction in which affected personnel are located, whether a consultation or co-determination duty applies and in what form. Co-determination and consultation duties are national law and vary; the determination is made per jurisdiction against the law and any applicable collective or works agreement in force there. The determination is recorded, per jurisdiction, as one of: **co-determination required** (the representative body's agreement is required before deployment), **information and consultation required** (the body must be informed and consulted, and, where the regime requires or provides for it, give a reasoned opinion, but its agreement is not required), or **no representative-body duty** (Step 6).

Jurisdiction-aware examples, to be verified against the current law of each applicable jurisdiction at the time of the determination:

- **European Union (GDPR Article 88).** GDPR Article 88(1) permits member states, by law or by collective agreement, to provide more specific rules for processing employees' personal data in the employment context, and expressly contemplates collective agreements and employee-representation mechanisms; Article 88(2) requires such rules to include suitable and specific measures, including on transparency of processing and monitoring systems at the workplace. Article 88 is an enabling provision for more specific employee-data rules; the consultation and co-determination duties themselves arise under national employment law or collective agreement, not under Article 88, and Article 88 does not itself create a consultation duty or serve as a lawful basis for the processing.
- **Germany (Betriebsverfassungsgesetz, BetrVG).** Where a works council (Betriebsrat) exists, the introduction and use of technical devices designed to monitor the behaviour or performance of employees is subject to the works council's **co-determination** right under BetrVG Section 87(1)(6): the capability may not be introduced without the works council's agreement, and where no agreement is reached the matter is decided by the conciliation committee (Einigungsstelle).
- **France (Comité Social et Économique, CSE).** Where a CSE exists, the employer must inform and consult the CSE before introducing means or techniques enabling the monitoring of employees' activity, and the CSE renders a reasoned opinion; this is an **information-and-consultation** duty, not a co-determination veto. Individual employees must also be informed in advance of the monitoring means used.
- **Other EU and EEA co-determination and information-consultation regimes.** Several member states operate works-council or union information-consultation or co-determination regimes under their national employment law; where such a regime carries more specific employee-data rules, those rules are enabled by Article 88, but the consultation and co-determination regimes themselves arise under national law. The applicable regime and its form (consultation or agreement) are determined per jurisdiction.

The determination also fixes, per jurisdiction, the **statutory timeline** for the consultation (the minimum period the body must be given, and any deadline for its opinion or for reaching agreement), which governs Step 4.

### Step 2: Identify the representative body and the required form

For each jurisdiction where Step 1 found a duty, identify the specific representative body with standing for the affected personnel (the works council for the relevant establishment or group, the recognized trade union and the scope of its recognition, the CSE, or another statutory body) and confirm the form of the duty (consultation, reasoned opinion, or co-determination agreement). Where more than one body has standing, each is engaged as its mandate requires. Where Step 1 found **no representative-body duty** in a jurisdiction, no consultation step is performed there; that finding is carried to Step 6.

### Step 3: Notify the body and provide the required information

Notify the identified body and provide the information the applicable regime requires and that the body reasonably needs to form a view. The information pack includes, at least:

1. The **purpose and legitimate aim** of the monitoring capability, and the categories of personnel and systems it affects.
2. The **scope**: what is and is not monitored, stated consistently with the parent policy's in-scope and out-of-scope boundaries (including the personal-device and BYOD exclusion and the exclusion of routine HR and performance management), so the description does not overstate or understate the capability.
3. The **data collected**: the categories of telemetry, metadata, and presence signals, and, where applicable, whether any content inspection is involved and under what exceptional, approved conditions.
4. The **safeguards**: the necessity and proportionality analysis, the access controls, the retention approach, the prohibited-use limits (including that presence is not proof of work and that monitoring signals do not trigger automated discipline), and the transparency and notice measures.
5. The **impact assessment and lawful-basis analysis**: the completed privacy impact assessment or data protection impact assessment for the capability (using [`privacy/template-dpia.md`](template-dpia.md) where a GDPR Article 35 DPIA applies, per the [Privacy Impact and Cross-Border Transfer Procedure](procedure-privacy-impact-and-cross-border-transfer.md)), and, where the lawful basis relied on is a legitimate interest, the completed legitimate-interest assessment using the [Legitimate Interest Assessment template](template-legitimate-interest-assessment.md). Where the [Legitimate Interest Assessment for Employment Monitoring Annex](annex-legitimate-interest-employment-monitoring.md) applies, the completed employment-monitoring legitimate-interest assessment it frames is the LIA source provided to the body.
6. Where GDPR applies, the DPIA process itself contemplates seeking the views of data subjects or their representatives on the intended processing (GDPR Article 35(9)); this consultation discharges that step where the representative body is the appropriate channel, and the views obtained are recorded in the DPIA.

The information provided is accurate and complete for the purpose of the consultation; specific security detection logic and thresholds may be withheld only where disclosure would defeat the security purpose, consistent with the parent policy's transparency safeguard (Section 5, item 3), and withholding operational detail never permits withholding the existence, nature, or purpose of the monitoring.

### Step 4: Conduct genuine consultation or negotiation

Conduct the consultation within the statutory timeline fixed in Step 1, and do not deploy or materially change the capability during the consultation period.

1. **Information and consultation.** Where the regime is information and consultation, give the body the information and a genuine opportunity to examine it, respond to its questions, consider in good faith any opinion it gives (a reasoned opinion where the regime provides for one), and record that opinion or response and the organization's response. The organization is not bound to agree, but the consultation must be genuine, not a formality after a settled decision.
2. **Co-determination (agreement required).** Where the regime is co-determination, the capability may not be introduced without the body's agreement. Negotiate in good faith toward a works agreement or collective agreement that governs the capability, and, where no agreement is reached, follow the jurisdiction's escalation mechanism (for example the conciliation committee, where the applicable regime provides one) rather than proceeding unilaterally.
3. **Strictness across jurisdictions.** Where the same capability affects personnel in more than one jurisdiction, each jurisdiction's duty is met on its own terms, and the design is held to the strictest applicable standard unless a documented, approved jurisdiction-specific carve-out applies (parent policy, Section 4, items 4 and 5).

### Step 5: Conclude, evidence, and sign off

Conclude the consultation for each jurisdiction and assemble the audit trail that demonstrates the duty was met. Retain, as the evidence of consultation:

1. The **per-jurisdiction determination** from Step 1 (the duty and its form, with the legal basis for the determination).
2. The **notice** given to each body and the **information pack** provided (Step 3), including the impact assessment and, where applicable, the legitimate-interest assessment.
3. The **minutes or record** of the consultation or negotiation, the body's reasoned opinion where one was given, and the organization's response.
4. The **concluding instrument**: the works agreement or collective agreement (co-determination); the record of the consultation and the organization's response, including any reasoned opinion the regime provided for (information and consultation); or the documented finding of no duty (Step 6).
5. A **dated sign-off** confirming that, for each affected jurisdiction, the required consultation or agreement was completed before deployment or material change, signed by the accountable roles (Legal Counsel for the legal-duty determination and its satisfaction; the CISO as capability owner; and HR / People Operations for the consultation record), with the DPO's independent review noted.

The capability owner (CISO) does not deploy or materially change the capability until this sign-off is complete for every affected jurisdiction. Records are retained per the [Data Retention Schedule](../governance/register-data-retention-schedule.md); retention periods are organization-defined and recorded in that register and are not prescribed by this procedure or attributed to any external standard.

### Step 6: Where no works council or employee representative body exists

Where Step 1 finds no statutory or agreement-based consultation or co-determination duty in a jurisdiction (for example a non-unionized workforce with no works council, or a jurisdiction with no co-determination regime), there is no consultation or co-determination step to perform there, and this procedure does not manufacture one. In that case the procedure requires instead that:

1. The **finding of no duty** is recorded for the jurisdiction, with the basis for it, so the audit trail shows the determination was made rather than skipped.
2. The **transparency, notice, and impact-assessment obligations still apply**: personnel are informed of the nature, purpose, and scope of the monitoring before it applies to them (parent policy, Section 5), and the impact assessment and lawful-basis analysis (including the legitimate-interest assessment where relied on) are completed and retained (parent policy, Section 4, items 1 and 2). These duties are independent of any consultation duty and are not waived by the absence of a representative body.
3. Where a jurisdiction provides a mechanism short of co-determination (for example a right for employees to request an information-and-consultation arrangement, or collective bargaining with a recognized union over terms and conditions that may include monitoring), that mechanism is honoured where it is triggered, but it is not overstated into a co-determination veto that the jurisdiction's law does not confer.

The absence of a representative body reduces the consultation step to a recorded determination; it does not reduce the transparency, lawful-basis, and impact-assessment obligations the parent policy imposes.

### Step 7: Re-consultation on material change, and review

1. A **material change** to a consulted capability (a change to the aim, the data collected, the scope, the safeguards, or the retention or access model) re-triggers this procedure from Step 1 for each affected jurisdiction: the determination is refreshed, and any renewed consultation or agreement is completed and evidenced before the change is deployed.
2. The per-jurisdiction determinations are reviewed on the document's review cadence and whenever the applicable employment, privacy, or co-determination law materially changes, so that a determination of "no duty" or a settled works agreement does not silently go stale.

---

## Framework alignment

| Framework | Reference | Relevance |
|---|---|---|
| ISO/IEC 27001:2022 | A.5.31 Legal, statutory, regulatory and contractual requirements; A.5.34 Privacy and protection of personal identifiable information (PII) | Step 1 determines the applicable employment and co-determination requirement, and the procedure requires it to be met and evidenced for personal-data processing in the monitoring context. |
| NIST CSF 2.0 | GV.OC Organizational Context; GV.PO Policy | Determining the applicable jurisdiction's legal and regulatory requirements (GV.OC) and governing the consultation through documented policy (GV.PO). |
| CSA CCM v4.1 | GRC-07 Information System Regulatory Mapping; A&A-04 Requirements Compliance | Step 1 maps the applicable co-determination or consultation regulation to the monitoring deployment (GRC-07); Steps 5 and 6 evidence compliance with the mapped requirement (A&A-04). |
| GDPR (EU) | Article 88 (more specific rules for employee-data processing, by law or collective agreement); Article 35(9) (seeking the views of data subjects or their representatives on the intended processing); Article 5(1)(a) and Article 5(2) (lawfulness, fairness, transparency; accountability) | Article 88 is the enabling provision for more specific employee-data rules; the consultation and co-determination duties themselves arise under national employment law or agreement, not under Article 88. Article 35(9) is the DPIA step this consultation can discharge. These provisions frame and evidence the duty; Article 88 is not itself a lawful basis for the processing. |
| UK GDPR | Article 88 is not adopted (there is no UK employment-specific Article 88 regime); Article 35(9) DPIA consultation; Article 5 principles. Illustrative and subject to current-law verification: the UK has no general works-council co-determination regime equivalent to the German BetrVG, and UK employee-consultation mechanisms (for example the Information and Consultation of Employees Regulations 2004, an information-and-consultation right rather than a co-determination veto, or collective bargaining with a recognized union) arise under UK employment law and are verified against current law at the point of determination. | The UK consultation posture differs from EU member-state co-determination regimes; do not read a BetrVG-style veto into the UK position, and do not conflate the EU and UK regimes. |

Note: German BetrVG, French CSE, and United Kingdom employee-consultation mechanisms (for example the Information and Consultation of Employees Regulations 2004 and collective bargaining) are national employment law cited as jurisdiction examples wherever they appear in this procedure; they are not entries in the bundled control registries and are flagged for verification against current law at the point of determination.

---

**End of Document**
