# Procedure: Crisis Management & EOC Activation

## Metadata

| Field | Details |
|-------|----------|
| **Document Title** | Crisis Management & Emergency Operations Center (EOC) Activation Procedure |
| **Document Type** | Procedure |
| **Version** | 0.1 |
| **Date** |  |
| **Document Owner** | Chief Information Officer (CIO) |
| **Approving Authority** | Chief Risk Officer (CRO) |
| **Related Documents** | Plan: Business Continuity & Crisis Management; Plan: Crisis Communication; Framework: Business Continuity & Resilience; Policy: Business Continuity and Disaster Recovery; Standard: Business Continuity & Disaster Recovery; Procedure: Incident Response |
| **Classification** | Public – Open Access |
| **Category** | Crisis Management / Operational Response |
| **Review Frequency** | Annual or following major incident or exercise |
| **Repository Path** | /resilience/procedure-crisis-management-eoc-activation |
| **Confidentiality** | None (Public Domain, CC0 License) |

---

## Document Control

| Version | Date | Author | Change History |
|----------|------|---------|----------------|
| 0.1 |  |  | Initial Draft |

---

## Approval

| Role | Name | Approval Date |
|-------|------|---------------|
| Chief Information Officer (CIO) |  |  |
| Chief Risk Officer (CRO) |  |  |
| Chief Information Security Officer (CISO) |  |  |
| Chief Compliance Officer (CCO) |  |  |
| Chief Legal Officer / General Counsel (CLO/GC) |  |  |
| Chief Security Officer (Physical) |  |  |

---

## Purpose

This procedure defines the activation, operation, and deactivation process of the **Crisis Management Team (CMT)** and the **Emergency Operations Center (EOC)**.  
It ensures structured command, coordination, and communication during enterprise-level incidents and crises.

---

## Scope

- Applies to all enterprise incidents escalated to Level 2 (Major Incident) or Level 3 (Crisis) per the Business Continuity & Crisis Management Plan.  
- Covers activation and management of both virtual and physical EOCs.  
- Applies to all departments, regions, and partner organizations participating in crisis management, continuity, or recovery activities.  

---

## Objectives

1. Provide a clear activation and escalation process for crisis management.  
2. Define the structure, membership, and operating rhythm of the CMT and EOC.  
3. Establish command, control, and communication protocols that support rapid, coordinated decision-making.  
4. Ensure documentation, auditability, and traceability of all crisis actions.  

---

## Activation Triggers

Crisis management and EOC activation may occur under any of the following conditions:

- A **Level 2 (Major Incident)** or **Level 3 (Crisis)** is declared by the CIO, CRO, or CEO.  
- Disruption to multiple business units or critical systems exceeds defined RTO thresholds.  
- Confirmed compromise of regulated or trade-security data (GDPR, BASC, NIS 2).  
- Physical security or life-safety threats require coordinated emergency management.  
- External agencies (regulators, law enforcement, customs) request unified command engagement.

---

## Activation Process

### Step 1 – Incident Escalation and Assessment
1. The Business Continuity Manager (BCM) or Incident Response Coordinator (IRC) notifies the CIO and CRO of a potential crisis.  
2. The CIO, in consultation with the CRO and CISO, evaluates scope, severity, and business impact.  
3. If escalation criteria are met, the CIO formally declares **Crisis Activation** and instructs the BCM to initiate the EOC setup.

### Step 2 – Notification and Mobilization
1. The BCM issues notifications to all CMT members and alternates via Teams, SMS, and email.  
2. The initial alert must include:  
   - Nature of the incident.  
   - Impacted locations or systems.  
   - Time of activation and expected next update.  
   - Instructions for EOC attendance (virtual or physical).  
3. The Crisis Communication Plan is activated in parallel to prepare initial internal messaging.

### Step 3 – EOC Setup
1. The BCM configures the **Virtual EOC** (Microsoft Teams / Confluence workspace).  
2. If network access is impaired, the **Physical EOC** is activated at the designated alternate site.  
3. The following minimum resources must be available:  
   - Secure conferencing capability.  
   - Situation dashboard and log template.  
   - Contact directory and decision-log register.  
   - Communication links to legal, compliance, and external partners.

### Step 4 – CMT Initial Briefing
1. The CIO or delegate conducts the first CMT meeting within 60 minutes of activation.  
2. Agenda:  
   - Incident summary and scope.  
   - Current impact and containment status.  
   - Immediate priorities (safety, communications, continuity).  
   - Assignment of roles and tasking for next operational period.  
3. The BCM records all actions, owners, and due times in the EOC Action Log.

---

## Crisis Management Structure

| Position | Core Responsibilities |
|-----------|-----------------------|
| **Incident Commander (CIO)** | Leads crisis response; approves strategic actions and external statements. |
| **Deputy Commander (CRO)** | Coordinates risk assessment and escalation to executive leadership. |
| **CISO** | Oversees cybersecurity, ICT continuity, and data-protection measures. |
| **CCO** | Ensures compliance with regulatory frameworks and certification standards. |
| **CLO/GC** | Provides legal counsel, manages contractual and liability considerations. |
| **CSO (Physical)** | Manages site security, facility control, and staff safety. |
| **BCM** | Facilitates EOC operations, documentation, and logistics. |
| **Communications Director** | Executes communication plan and media management. |
| **HR Lead** | Handles staffing, welfare, and internal communications. |
| **AI Governance Council Representative** | Advises on AI-related risk or ethics issues. |

---

## Operating Rhythm

| Interval | Activity | Deliverable |
|-----------|-----------|-------------|
| **First Hour** | Initial CMT meeting and situation assessment. | Situation Report 0 (SitRep 0). |
| **Every 2–4 Hours** | CMT status meeting and action updates. | Updated SitRep. |
| **Daily** | Executive briefing and external communications review. | Daily Summary Report. |
| **Post-Event** | After-Action Review within 10 business days. | Lessons-Learned Report; Improvement Actions. |

---

## Communication Protocols

1. All outbound communications follow the **Crisis Communication Plan** approval workflow.  
2. Regulatory and stakeholder notifications are coordinated through Legal and Compliance.  
3. Only the CIO, CEO, or Communications Director may issue public or press statements.  
4. The BCM maintains the **EOC Communication Log**, recording:  
   - Message date/time.  
   - Sender and recipient.  
   - Content summary and approval reference.

---

## Documentation Requirements

During activation, the BCM ensures maintenance of:

- **EOC Action Log** – all assigned tasks, owners, and completion times.  
- **Situation Reports (SitReps)** – issued at regular intervals to record evolving status.  
- **Decision Log** – rationale for critical decisions and approving authority.  
- **Resource Tracker** – personnel assignments, facilities, and logistics support.  
- **After-Action Report (AAR)** – compiled following deactivation for ERC review.

All records are retained within the governance repository for a minimum of seven years.

---

## Deactivation Process

1. The CIO, in consultation with the CRO, declares crisis closure once:  
   - Operations are restored and validated.  
   - Communication and regulatory obligations are complete.  
   - Residual risks are within accepted tolerance.  
2. The BCM issues a **Stand-Down Notice** to all participants.  
3. The final SitRep and AAR are distributed to the ERC and archived.  
4. Identified improvement actions are entered into the corrective-action and improvement tracking processes.

---

## Training and Exercising

- CMT and EOC staff shall participate in at least **one tabletop** and **one simulation exercise** annually.  
- Each exercise must test:  
  - Activation and notification speed.  
  - Role clarity and decision flow.  
  - Communication and documentation accuracy.  
- Performance metrics and lessons learned feed into improvement tracking for ERC review.

---

## Continuous Improvement

Findings and improvement actions from each activation or exercise must be documented and tracked through:

- The Corrective and Preventive Action Procedure  
- The Continuous Improvement Register Procedure  
- The Digital Trust Performance Framework  

Actions remain open until verified as effective through re-testing or management validation.

---

## References and Framework Alignment

| Framework | Reference | Objective |
|------------|------------|-----------|
| **ISO 22361:2022** | Clauses 4–9 | Crisis-management leadership, structure, and decision-making. |
| **ISO 22301:2019** | Clauses 8–10 | Integration of crisis and continuity processes within BCMS. |
| **ISO 27031:2011** | Clause 7 | ICT readiness and technical resilience. |
| **NIST SP 800-34 r1** | Chapters 3–5 | Contingency-planning structure and activation. |
| **COBIT 2025** | DSS04, DSS05 | Manage continuity, availability, and security services. |
| **CSA CCM v5** | BCR-01, BCR-02 | Business continuity and resilience governance. |

---

## Definitions

Refer to the **Role Authority Register** for definitions of organizational roles and authorities.

---

**End of Document**
