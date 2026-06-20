# Regulator Interaction Templates

**Document Title:** Regulator Interaction Templates\
**Document Type:** Template\
**Version:** 1.0.0\
**Date:** 2026-06-20\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/policy-compliance-and-audit-management.md`](policy-compliance-and-audit-management.md), [`compliance/standard-internal-audit.md`](standard-internal-audit.md), [`compliance/register-compliance-obligations-template.md`](register-compliance-obligations-template.md), [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md)\
**Classification:** Public\
**Category:** Compliance\
**Review Frequency:** Annual, and on material change to a covered regulator's reporting requirements\
**Repository Path:** [`compliance/template-regulator-interaction.md`](template-regulator-interaction.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template consolidates the recurring regulator-facing interactions into reusable shapes. The library ships incident-notification language inside per-jurisdiction privacy annexes (under [`privacy/jurisdictions/`](../privacy/jurisdictions/)) and inside industry compliance overlays (under [`compliance/<sector>/`](.)), but the shape of an organisation-to-regulator interaction is broadly similar across jurisdictions and sectors. This template provides five reusable sub-templates so adopters facing first-time regulator contact have a starting structure.

Each sub-template is shape-only. Jurisdiction-specific or sector-specific timing, format, and submission-channel requirements live in the relevant annex or sector folder; this template names what to put in each submission, not when or where.

The intent is reduced synthesis burden. An adopter handling its first regulator interaction does not need to reverse-engineer the structure from prior submissions; the structure is here.

---

## Scope

Five sub-templates:

1. **Breach notification** to a regulator (privacy regulator, security regulator, sector regulator).
2. **Attestation submission** (compliance attestation, audit attestation, framework attestation).
3. **Examination support** (planned regulator examination, on-site or remote).
4. **Periodic report submission** (recurring reports the framework requires).
5. **Regulatory inquiry response** (ad-hoc inquiry not on the periodic schedule).

Each sub-template is generic. The adopter:

- Replaces placeholder names and dates.
- Consults the relevant jurisdiction annex or sector folder for the timing, format, and channel requirements that apply.
- Adapts the section list to the regulator's specific schema where one is mandated.

The sub-templates do not cover internal interactions (board reports, internal audit submissions, customer due-diligence responses); those are out of scope for this consolidated template.

---

## Sub-template 1: Breach notification

### When to use

When an event meets the regulator-notification threshold under the applicable framework (e.g., GDPR Article 33 personal data breach; SEC Form 8-K cybersecurity incident; HIPAA Breach Notification Rule; sector-specific incident-reporting duties).

### Timing

Determined by the framework. Common patterns:

- **GDPR Article 33**: not later than 72 hours after becoming aware.
- **SEC Form 8-K cybersecurity item**: four business days after determination of materiality.
- **HIPAA Breach Notification Rule**: 60 days from discovery (Secretary notification thresholds vary).
- **NIS 2 (EU)**: 24 hours early warning, 72 hours incident notification, one month final report.
- **DORA (EU financial)**: tiered reporting timelines depending on incident classification.

Determine the applicable timing from the relevant annex or sector folder before drafting.

### Template

```
To: <regulator name and reporting-contact address/portal>
From: <organisation legal name>
Date of notification: <YYYY-MM-DD HH:MM timezone>
Reference number assigned by us: <internal incident ID>
Reference number assigned by the regulator: <if known; otherwise "to be assigned">

Subject: Notification under <framework section, e.g. GDPR Article 33>

1. Discovery
   Date and time of discovery: <YYYY-MM-DD HH:MM timezone>
   Discovery mechanism: <e.g. SIEM alert, customer report, vendor notification>
   Initial discoverer (role, not name): <e.g. SOC analyst, customer-support agent>

2. Nature of the incident
   Brief description: <one paragraph, factual; reserve interpretation for later sections>
   Incident type: <unauthorised access / data exfiltration / availability event / integrity event / other>
   Asset and data categories affected: <list>
   Approximate number of records or affected data subjects: <best estimate at time of notification; mark as preliminary if not yet refined>
   Approximate number of individuals materially affected: <best estimate>

3. Cause and contributing factors (preliminary)
   <Best current understanding. Mark explicitly as preliminary; commit to update.>

4. Containment and immediate actions
   <List the actions taken to contain the incident and limit further harm, with timestamps where known.>

5. Mitigation in progress
   <Actions in flight, with expected completion dates.>

6. Affected individuals' notification
   Required: <yes / no / under assessment>
   Planned date: <YYYY-MM-DD or "TBD pending assessment">
   Channel: <e.g. email, postal, in-app notice>

7. External parties notified
   <Law enforcement: yes/no, agency, date. Other regulators: list. Insurers: yes/no.>

8. Contact for follow-up
   Primary contact: <role and direct contact, e.g. CISO, +44 ... or equivalent>
   Backup contact: <role and contact>

9. Follow-up commitments
   Next update to the regulator: <date>
   Final report expected: <date or "per framework requirements">

Signed: <named senior officer per the framework's signatory requirements; e.g. DPO, CISO, CCO>
```

### Notes

- Keep the language factual and precise. Avoid interpretation that may not survive forensic review.
- Mark every preliminary item as preliminary; the next update is the chance to refine or correct.
- Preserve a copy of the submission in the incident artefact trail.

---

## Sub-template 2: Attestation submission

### When to use

When the framework requires the organisation to attest to its compliance or its control posture (e.g., SOX Section 302/404 management attestations, PCI DSS Attestation of Compliance, FedRAMP annual attestation, ISO 27001 statement-of-applicability submission, DORA control attestation).

### Timing

Per the framework. Most attestations are annual; some are quarterly or event-driven.

### Template

```
To: <regulator or designated attestation receiver>
From: <organisation legal name>
Attestation period covered: <YYYY-MM-DD to YYYY-MM-DD>
Date of attestation: <YYYY-MM-DD>

Subject: Attestation under <framework name and section reference>

1. Scope of attestation
   Systems, processes, or business units in scope: <list>
   Systems, processes, or business units explicitly out of scope: <list with rationale>
   Framework version against which attestation is made: <e.g. ISO 27001:2022, PCI DSS v4.0, SOC 2 Type II Trust Services Criteria 2017>

2. Attestation statement
   <One paragraph stating the attestation. Match the framework's required wording where prescribed (some frameworks require verbatim language).>

3. Qualifications
   <If the attestation is qualified, list the qualifications here. If unqualified, state so explicitly.>

4. Material findings during the period
   <List material findings from internal audit, external audit, regulator examination, or incident response that affect the attestation. None acceptable if true; do not omit findings to make the attestation simpler.>

5. Compensating controls
   <Where a control was not fully implemented during the period, describe the compensating control and the residual risk.>

6. Changes since the prior attestation
   <Material changes to the control set, scope, or organisational structure since the prior attestation period.>

7. Supporting artefacts
   <List of supporting artefacts maintained internally: control register, evidence package, internal audit reports, external audit opinion.>

8. Signatory
   Signed: <named senior officer per the framework's signatory requirements>
   Title: <role>
   Date: <YYYY-MM-DD>

   Witness or counter-signatory (if framework requires): <name, role, date>
```

### Notes

- Frameworks often require specific signatory roles (CEO, CFO, CISO, CCO); confirm against the framework before signing.
- Qualifications are not weakness; an unqualified attestation that should have been qualified is a much worse outcome than a qualified attestation that is honest.
- Preserve the attestation under document retention for the period the framework requires (commonly 5 to 7 years).

---

## Sub-template 3: Examination support

### When to use

When a regulator has notified the organisation of an upcoming examination (on-site or remote). The template covers the period from notification through closing meeting.

### Timing

Examinations are usually scheduled with weeks to months of advance notice. The framework or regulator letter sets the cadence.

### Template

```
Examination identifier: <regulator reference number>
Regulator: <name>
Examination scope: <one paragraph>
Examination period (the period being examined): <YYYY-MM-DD to YYYY-MM-DD>
On-site dates: <YYYY-MM-DD to YYYY-MM-DD or "remote">
Lead examiner (regulator-side): <name and role if known>

Internal lead: <role; typically Head of Compliance or designate>
Internal support team: <list of roles and the artefacts they own>

1. Pre-examination documentation packet (assembled within X days of notification)
   - Control register relevant to scope
   - Prior attestations covering the examination period
   - Internal audit reports covering the examination period
   - Prior examination findings and their closure status
   - Risk register entries relevant to scope
   - Incident log entries relevant to scope (filtered to in-scope assets)
   - Policy and procedure documents in scope, with their review history
   - Evidence-package index (with portal or evidence-room access details for the examiner)

2. Pre-examination briefing (held with internal teams, X days before on-site or remote start)
   Topics:
   - Examination scope and expected duration
   - Examiner-side contact list
   - Internal-side responsibility map (which team owns which artefact category)
   - Communication rules (single point of contact; no parallel channels to the examiner)
   - Escalation path (which findings need same-day senior-leadership involvement)

3. During the examination
   - Daily-update cadence: <e.g. end-of-day stand-up, internal-only, 15 minutes>
   - Document-request log: every regulator request is logged with date, requestor, item, response date, and responder
   - Open-item tracker: items the regulator has flagged but not yet closed
   - Privileged communication: any item involving counsel goes through counsel before reaching the examiner

4. Closing meeting
   Format: <regulator-led summary of findings, organisation response opportunity>
   Internal preparation: <prepare draft responses to anticipated findings 24 to 48 hours in advance>
   Attendees: <senior leadership per the framework's requirements; counsel where applicable>

5. Post-examination
   - Findings letter receipt: log the date received; confirm internal acknowledgement timeline
   - Findings response: per the regulator's framework (commonly 30 days), submit a written response with:
     - Each finding's classification (agreed / disagreed / partially agreed)
     - Remediation plan with named owner and date for each agreed finding
     - Evidence-of-remediation submission cadence
   - Internal follow-up: each finding becomes a tracked item in the CAPA register

6. Closure
   - All agreed findings remediated and evidence submitted
   - Regulator confirms closure (in writing where possible)
   - Lessons-learned review held internally; outcomes feed into the control register and the policy/procedure updates
```

### Notes

- Single point of contact between the organisation and the examiner. Avoid parallel channels.
- Document everything; the daily-update notes and the request log are the audit trail for the audit trail.
- Counsel involvement is jurisdiction- and framework-specific; consult before the examination begins.

---

## Sub-template 4: Periodic report submission

### When to use

When the framework requires the organisation to submit a recurring report (e.g., annual cybersecurity assessment under DFS Part 500; annual report under NIS 2; quarterly returns under sector regulators).

### Timing

Per the framework. Set internal deadlines 4 to 8 weeks ahead of the regulator deadline to allow for review and sign-off.

### Template

```
Report identifier: <regulator reference, e.g. NIS-2-AR-2026>
Reporting period: <YYYY-MM-DD to YYYY-MM-DD>
Regulator: <name>
Submission deadline: <YYYY-MM-DD>
Internal deadline: <YYYY-MM-DD; typically 4 to 8 weeks ahead>
Submission channel: <regulator portal / email / postal>

Required sections (per framework):
1. <Section title per framework>
   Data source: <internal system or register>
   Owner: <role>
   Status: <draft / under review / approved>
2. <Section title>
   ...
[continue per framework]

Internal review and sign-off
- Author: <role>
- Reviewer: <role>
- Approving authority: <role per framework>
- Sign-off date: <YYYY-MM-DD>

Submission record
- Submitted on: <YYYY-MM-DD>
- Submitter: <role>
- Confirmation reference: <regulator-assigned reference, if any>
- Submission artefact stored at: <internal repository location>
```

### Notes

- Periodic reports tend to be cumulative; each report builds on the prior one. Cross-reference the prior submission and note changes.
- Set internal deadlines ahead of regulator deadlines. A submission that meets the regulator deadline at the cost of skipping internal review is a deferred risk, not a successful submission.
- Retain the submission under document retention for the period the framework requires.

---

## Sub-template 5: Regulatory inquiry response

### When to use

When a regulator sends an ad-hoc inquiry not on the periodic schedule. Examples: a request following a public incident, a follow-up to a prior attestation, a request for evidence of a specific control's implementation, a request prompted by a customer complaint.

### Timing

Per the regulator's request. Commonly 14 to 30 days; sometimes much faster for incident-prompted inquiries. Acknowledge receipt promptly even when the substantive response will take longer.

### Template

```
Inquiry identifier: <regulator reference number or internal-assigned>
Regulator: <name and contact>
Inquiry received: <YYYY-MM-DD>
Requested response date: <YYYY-MM-DD>
Acknowledgement sent: <YYYY-MM-DD>

Inquiry summary
<One paragraph summarising what the regulator is asking. Use the regulator's own words where helpful.>

Internal triage
- Owning team: <which internal team owns the response>
- Owning role: <named role, e.g. Head of Compliance>
- Supporting teams: <which teams provide evidence>
- Counsel review required: <yes / no>
- Escalation: <was the inquiry escalated to senior leadership; date>

Response sections
1. <Topic 1 the inquiry asks about>
   Response: <draft text>
   Supporting evidence: <list of evidence items>
   Reviewer: <role>
2. <Topic 2>
   ...
[continue per inquiry]

Internal sign-off
- Author: <role>
- Reviewer: <role>
- Approving authority: <role>
- Sign-off date: <YYYY-MM-DD>

Submission record
- Submitted on: <YYYY-MM-DD>
- Submitter: <role>
- Submission channel: <email / portal / postal>
- Confirmation reference: <if any>
- Submission artefact stored at: <internal repository location>

Follow-up
- Acknowledgement from regulator received: <YYYY-MM-DD or "pending">
- Further questions: <log of subsequent inquiries, if any>
- Closure: <date and reference if the inquiry was formally closed>
```

### Notes

- Acknowledge receipt within 1 to 2 business days even if the substantive response will take weeks. Silence reads as inattention.
- Counsel involvement for inquiries that may relate to litigation, sanctions, or enforcement; consult before responding.
- The inquiry-response artefact and the supporting evidence become discoverable records; treat them with the same care as the original control evidence.

---

## Review questions

When using these templates, answer the following before submitting:

1. Have we identified the framework-specific timing, format, and channel requirements (this template is shape-only; jurisdiction- and sector-specific requirements live in the relevant annex or sector folder)?
2. Have we filled placeholders with real values rather than leaving any TBD entries that will go to the regulator?
3. Have we had the relevant internal reviewer and approving authority sign off?
4. Have we preserved a copy of the submission and the supporting evidence under our document retention policy?
5. Have we logged the submission in the relevant register (incident register for breach notifications, attestation history for attestations, CAPA register for examination findings)?
6. For inquiry responses involving litigation, sanctions, or enforcement exposure: have we cleared the response with counsel before submission?

---

## Maintenance

This template is updated when:

- A covered framework materially changes its required sections, timing, or signatory requirements.
- A new recurring interaction shape is identified (e.g., a new framework introduces a sixth interaction type not covered here).
- Adopter feedback identifies a section that consistently produces ambiguity or rework.

Per-framework specifics (GDPR Article 33 timing, SEC 8-K thresholds, etc.) live in the relevant annex or sector overlay, not in this template. Updates to those specifics do not require updates here.

---

## Licence

CC BY-SA 4.0. Adapt and share, including for commercial use; preserve the licence on derivative works.
