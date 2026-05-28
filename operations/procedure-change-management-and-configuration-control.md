# Change Management and Configuration Control Procedure

**Document Title:** Change Management and Configuration Control Procedure 
**Document Type:** Procedure 
**Version:** 1.3.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`operations/standard-production-security-requirements.md`](standard-production-security-requirements.md), [`security/policy-information-security.md`](../security/policy-information-security.md), [`security/procedure-vulnerability-management.md`](../security/procedure-vulnerability-management.md), [`dev-security/standard-devops-security-requirements.md`](../dev-security/standard-devops-security-requirements.md) 
**Classification:** Public 
**Category:** Operations 
**Review Frequency:** Annual and upon material platform or regulatory change 
**Repository Path:** [`operations/procedure-change-management-and-configuration-control.md`](procedure-change-management-and-configuration-control.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

This procedure defines the end-to-end process for classifying, approving, scheduling, implementing, and reviewing changes to production infrastructure, applications, and security configurations.

---

## Purpose

To ensure that changes to production systems are controlled, traceable, and reversible, minimizing disruption to services and preventing unauthorized modifications to security-critical configurations.

---

## Scope

1. Applies to all changes to production infrastructure, applications, cloud configurations, network devices, security controls (identity, PAM, PKI, firewall), and operational data.
2. Applies to IT Operations, Development Teams, Cloud Engineers, Security Engineering, and any third party with access to production environments.
3. Covers on-premises, cloud platform, and hybrid environments.
4. Does not govern changes to development or test environments unless those changes are promoted to production via a deployment pipeline.

---

## Governance and accountability

| Role | Responsibility |
| --- | --- |
| **CIO** | Approves Emergency and High-risk changes; chairs or delegates CAB chair. |
| **CISO** | Co-approves High-risk changes (identity, PAM, PKI, production network); reviews security impact of Normal changes. |
| **Change Manager** | Administers the change process; chairs the CAB; maintains the change schedule; ensures that rollback plans are present. |
| **Change Advisory Board (CAB)** | Reviews and approves Normal and High-risk changes; validates rollback plans. |
| **IT Operations / Engineering** | Submits change requests; implements approved changes; executes post-implementation reviews. |
| **System Owners** | Validate impact scope of changes affecting their systems. |
| **Internal Audit** | Reviews change process compliance and segregation of duties annually. |

---

## 1. Change classification

All changes must be classified before submission to the change process.

| Change Type | Description | Approval Authority | CAB Review |
| --- | --- | --- | --- |
| **Standard** | Pre-approved, low-risk, repeatable changes following a documented procedure (e.g., OS patch from approved list, password reset, user provisioning via standard role). | Team Lead | No |
| **Normal** | Any change not pre-approved that does not meet Emergency or High-risk criteria. | Delegated authority (typically IT Operations Manager) | Yes |
| **Emergency** | Unplanned change required to resolve or prevent a critical service outage or active security incident. | CIO or equivalent | Retrospective within 24 hours |
| **High-risk** | Changes to identity systems, PAM, PKI, production network topology, firewall rule bases, or security monitoring infrastructure. | CIO or CISO (joint approval) | Yes |

---

## 2. Change lifecycle

### 2.1 Request

The change initiator submits a Change Request (CR) via the ITSM platform, including:

- Description of the change and business justification.
- Systems and services affected.
- Change type classification.
- Implementation plan with step-by-step actions.
- Tested rollback plan (mandatory for all CAB-reviewed changes).
- Risk assessment (impact and likelihood of failure or disruption).
- Scheduled implementation window.
- Post-implementation review plan.

### 2.2 Assessment

The Change Manager reviews the CR for completeness and correct classification. Security Engineering reviews changes with security impact. The CISO reviews all High-risk changes before CAB submission.

### 2.3 Approval

| Change Type | Approval Path |
| --- | --- |
| Standard | Team Lead approves from the standard change catalogue; no CAB required. |
| Normal | Change Manager confirms completeness; CAB votes at weekly CAB meeting. |
| Emergency | CIO or equivalent approves verbally or by written authorization; retrospective CAB held within 24 hours. |
| High-risk | CISO and CIO provide written approval; CAB reviews and confirms. |

### 2.4 Scheduling

Approved Normal and High-risk changes are placed on the forward schedule of change (FSC). Standard maintenance windows are defined per environment and published. Changes outside maintenance windows require additional justification.

### 2.5 Implementation

Changes must be implemented exactly as described in the approved CR. All production changes must be executed through the approved infrastructure-as-code (IaC) pipeline. Direct manual changes to production systems are prohibited except during declared incidents; any manual change made during an incident must be codified in the IaC pipeline within 24 hours.

### 2.6 Post-implementation review (PIR)

Within the same or next business day following implementation, the implementer completes a PIR confirming:

- Change implemented as planned.
- Service functionality verified.
- Monitoring confirms expected behaviour.
- Rollback was not required, or if it was, the cause is documented.

Failed changes that required rollback are escalated for root cause analysis.

---

## 3. Change advisory board (CAB)

### 3.1 Composition

The CAB includes: Change Manager (chair); CISO or Security Engineering representative; IT Operations representative; relevant System Owners for changes on the agenda; and Business stakeholder representatives for user-impacting changes.

### 3.2 Meeting cadence

The CAB meets weekly. An emergency CAB can be convened within 4 hours for urgent Normal changes or retrospective Emergency change reviews.

### 3.3 Decision criteria

The CAB evaluates each CR against:

- Is the implementation plan complete and unambiguous?
- Is the rollback plan tested and viable?
- Is the scheduled window appropriate?
- Has the security impact been assessed?
- Are affected parties notified?

A majority vote approves the change. The CISO holds a veto for changes with unresolved security concerns.

---

## 4. Emergency change process

Emergency changes follow an accelerated path:

1. CIO or equivalent authorizes the change verbally or in writing.
2. The change is implemented with all actions logged in real time.
3. A retrospective CR is created in the ITSM platform within 4 hours of implementation.
4. Retrospective CAB review is held within 24 hours.
5. Any permanent configuration change resulting from an emergency change must be submitted as a Normal change within 5 business days.

The CISO must be notified of all Emergency changes within 1 hour of initiation.

---

## 5. Iac and configuration baseline

### 5.1 Infrastructure-as-code requirement

All production infrastructure configurations must be managed as code in the approved IaC repository. No production resources may exist outside the IaC baseline without a documented exception.

### 5.2 Configuration drift management

Automated configuration drift detection compares deployed configuration against the IaC baseline. Detected drift is alerted to IT Operations and Security Engineering. High-risk drift (critical security control disabled or authentication bypass introduced) is classified as a P2 incident.

### 5.3 Baseline documentation

The following must be maintained as living artefacts and updated within 30 days of any change:

- Network architecture diagram and VLAN/subnet register.
- ACL and firewall rule register with business justification and owner.
- Server and VM inventory with OS version and patch level.
- Certificate inventory with expiry dates.

---

## 6. Rollback planning

Every CAB-reviewed change must include a documented rollback plan that has been tested or reviewed for viability before CAB submission. The rollback plan must specify:

- Trigger conditions for initiating rollback.
- Step-by-step rollback actions.
- Estimated rollback duration.
- Responsible person.
- Verification steps to confirm successful rollback.

Rollback plans that have not been tested must be explicitly flagged in the CR; the CAB may defer approval pending testing.

---

## 7. Records and evidence

All change records must be retained in the ITSM platform and archived for a minimum of 3 years. Required evidence includes: the approved CR with all attachments; CAB meeting minutes and vote records; implementation log with timestamps; PIR sign-off; and rollback evidence where applicable.

---

## 8. Metrics

The following metrics are reported to the CISO and CIO monthly:

| Metric | Target |
| --- | --- |
| Change success rate (no rollback required) | ≥ 95% |
| Emergency change percentage of total changes | ≤ 5% |
| Changes with tested rollback plan | 100% of CAB-reviewed changes |
| CAB cycle time (CR submission to approval) | ≤ 5 business days for Normal |
| Post-implementation review completion rate | 100% |

---

## Framework alignment

| Control Area | ISO/IEC 20000 | ISO/IEC 27001 | COBIT 2019 | CSA CCM v4.1 | NIST |
| --- | --- | --- | --- | --- | --- |
| Change management | §8.5 | A.8.32 | CCC-01 to CCC-04 | CCC-01 to CCC-05 | SP 800-128 §4 |
| Configuration management | §8.5 | A.8.9 | CCC-05 to CCC-07 | CCC-06 to CCC-09 | SP 800-128 §3 |
| Emergency change | §8.5 | A.8.32 | CCC-03 | CCC-03 | SP 800-128 §4.4 |
| CAB governance | §8.5 | A.5.32 | CCC-02 | CCC-02 | N/A |
| IaC and drift | N/A | A.8.9 | CCC-07 | CCC-07 | SP 800-128 §3.2 |



**End of Document**
