# Departmental Continuity Plan Template

**Document Title:** Departmental Continuity Plan Template\
**Document Type:** Template\
**Version:** 1.1.2\
**Date:** 2026-07-09\
**Owner:** Resilience Owner\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`resilience/framework-business-continuity-and-resilience.md`](framework-business-continuity-and-resilience.md), [`resilience/policy-business-continuity-and-disaster-recovery.md`](policy-business-continuity-and-disaster-recovery.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](standard-business-continuity-and-disaster-recovery.md), [`resilience/procedure-business-impact-analysis.md`](procedure-business-impact-analysis.md), [`resilience/procedure-continuity-and-recovery-testing.md`](procedure-continuity-and-recovery-testing.md), [`resilience/plan-business-continuity-and-crisis-management.md`](plan-business-continuity-and-crisis-management.md)\
**Classification:** Public\
**Category:** Resilience\
**Review Frequency:** Annual and upon material process, service, supplier, data, workforce, facility, or system change\
**Repository Path:** [`resilience/template-departmental-continuity-plan.md`](template-departmental-continuity-plan.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template provides a reusable structure for documenting departmental or function-level continuity plans. It must be adapted by adopting organizations and must not be populated in the public repository with real department names, people names, contact details, system names, supplier names, locations, customer names, or recovery evidence.

---

## Use requirements

1. Completed continuity plans should be classified according to internal data classification requirements.
2. Completed plans should be stored in a restricted internal location.
3. Plans should align with business impact analysis and approved recovery objectives.
4. Plans should be reviewed after material process, workforce, supplier, facility, technology, AI system, data, or regulatory change.
5. Public CC BY-SA 4.0 examples must remain generic and non-identifying.

---

## Continuity plan fields

### 1. Department or function overview

| Field | Entry |
| --- | --- |
| Department or Function | |
| Plan Owner Role | |
| Alternate Owner Role | |
| Critical Services Supported | |
| Primary Operating Mode | |
| Alternate Operating Mode | |
| Last Review Date | |
| Next Review Date | |

### 2. Critical processes

Derive the Maximum Tolerable Disruption (MTD), Recovery Time Objective (RTO), and Recovery Point Objective (RPO) for each critical process from the organization's Business Impact Analysis (see [`resilience/procedure-business-impact-analysis.md`](procedure-business-impact-analysis.md)), applying the constraints that the MTD is greater than or equal to the RTO and that the RPO is set by the process's data-loss tolerance (consistent with ISO 22301). Complete one row per critical process; the illustrative row shows the expected granularity and is replaced with the department's own processes.

| Process | Criticality Tier | Maximum Tolerable Disruption | Recovery Time Objective | Recovery Point Objective | Minimum Service Level | Manual Workaround |
| --- | --- | --- | --- | --- | --- | --- |
| Payroll run (illustrative) | Tier 1 | 5 business days | 24 hours | 4 hours | One pay cycle processed | Provider fallback using a pre-agreed manual template |
| | | | | | | |

### 3. Dependencies

| Dependency Type | Dependency Description | Owner Role | Alternate or Workaround | Recovery Constraint |
| --- | --- | --- | --- | --- |
| People | | | | |
| Facility | | | | |
| Application or System | | | | |
| Data Set | | | | |
| Supplier | | | | |
| Cloud Service | | | | |
| AI System or Automation | | | | |
| Communication Channel | | | | |

### 4. Continuity actions

| Disruption Scenario | Immediate Action | Sustained Workaround | Escalation Role | Evidence to Capture |
| --- | --- | --- | --- | --- |
| Loss of primary system | | | | |
| Loss of critical data | | | | |
| Supplier failure | | | | |
| Facility unavailable | | | | |
| Workforce unavailable | | | | |
| AI system unavailable or unsafe | | | | |

### 5. Communication requirements

| Audience | Message Purpose | Approval Role | Channel Class | Timing |
| --- | --- | --- | --- | --- |
| Internal stakeholders | | | | |
| Customers or users | | | | |
| Suppliers | | | | |
| Regulators or authorities | | | | |

### 6. Restoration and return to normal

| Step | Description | Owner Role | Validation Evidence |
| --- | --- | --- | --- |
| Confirm service stability | | | |
| Validate data integrity | | | |
| Reconcile manual workarounds | | | |
| Confirm control state | | | |
| Record residual risk | | | |
| Approve return to normal | | | |

### 7. Testing and maintenance

| Test or Review | Frequency | Owner Role | Evidence |
| --- | --- | --- | --- |
| Plan review | | | |
| Tabletop exercise | | | |
| Manual workaround test | | | |
| Supplier escalation test | | | |
| AI fallback or disablement test | | | |

---

## Limitations

This template is a CC BY-SA 4.0 baseline. Completed departmental continuity plans can contain sensitive operational dependencies and should not be published under CC BY-SA 4.0 without sanitization.

---

**End of Document**
