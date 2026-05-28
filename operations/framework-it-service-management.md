# IT Service Management Framework

**Document Title:** IT Service Management Framework 
**Document Type:** Framework 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Officer 
**Approving Authority:** Chief Information Officer 
**Related Documents:** [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md), [`operations/standard-service-level-management.md`](standard-service-level-management.md), [`operations/register-it-operations-kpis.md`](register-it-operations-kpis.md), [`resilience/plan-it-disaster-recovery.md`](../resilience/plan-it-disaster-recovery.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`governance/framework-continuous-assurance-and-improvement.md`](../governance/framework-continuous-assurance-and-improvement.md) 
**Classification:** Public 
**Category:** Operations 
**Review Frequency:** Annual and upon material service management or regulatory change 
**Repository Path:** [`operations/framework-it-service-management.md`](framework-it-service-management.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This framework defines the structure, principles, and processes of the organization's IT Service Management (ITSM) function. It consolidates all ITIL-based processes, Incident, Problem, Change, Release, Request, Capacity, Availability, and Service Level Management, into a unified governance model. It aligns with ISO/IEC 20000-1:2018, ITIL 4, COBIT 2025 DSS02 and DSS03, and EU NIS 2 Directive requirements.

---

## Scope

Applies to all IT services, infrastructure, applications, cloud environments, and service delivery functions managed by or on behalf of the organization.

---

## Governance and accountability

| Role | Responsibility |
| --- | --- |
| **CIO** | Accountable for service strategy, alignment with business objectives, and continual improvement of the ITSM framework. |
| **CISO** | Ensures that ITSM integration with incident response and NIS 2 reporting requirements. |
| **Service Management Office (SMO)** | Oversees all ITIL process implementation, reporting, and coordination. |
| **Service Owners** | Manage end-to-end service delivery, availability, and SLAs. |
| **Process Owners** | Define and maintain policies, procedures, and metrics for their assigned ITIL processes. |
| **Change Advisory Board (CAB)** | Reviews and authorizes change requests to mitigate operational risk. |
| **Internal Audit** | Validates ISO/IEC 20000 compliance and governance effectiveness. |

---

## Framework principles

### 1. Incident management

All incidents are logged, categorized, prioritized, and tracked to resolution within defined SLAs. Major incidents trigger immediate escalation to the CIO, CISO, and Crisis Management Team. Significant cybersecurity incidents meet EU NIS 2 reporting timelines (24 hours for early warning; 72 hours for full notification).

### 2. Problem management

Problem records are created for recurring or significant incidents. Root cause analysis is conducted for all major incidents. Known Error Databases are maintained and reviewed monthly to drive proactive resolution.

### 3. Change management

All changes are categorized as Standard, Normal, or Emergency. CAB approval is required for Normal and Emergency changes. Post-implementation reviews assess success criteria and rollback results. Emergency changes are reviewed by the CAB within 5 business days of implementation.

### 4. Service level management

SLAs and OLAs are established for all critical services and reviewed annually. SLA breaches trigger service reviews and root cause analysis. SLA performance is reported to the CIO and ERC quarterly.

### 5. Capacity and availability management

Capacity plans are based on trend analysis and predictive modelling. Availability metrics are continuously monitored with defined service-level targets. Capacity risks are raised to the CIO as part of the quarterly governance reporting cycle.

### 6. AI-enabled automation

AI-based automation tools may augment ITSM workflows for incident triage, root cause prediction, and self-healing actions. AI recommendations must be explainable and validated by human operators. AI tools used in ITSM are subject to governance requirements under the AI Governance and Risk Framework.

### 7. Continual service improvement

ITIL 4 continual improvement cycles are adopted. Service improvement plans are data-driven, documented, and reviewed quarterly. Improvement actions are tracked in the CAPA Register and reported to the ERC.

---

## Service levels

| Priority | Definition | Response | Resolution |
| --- | --- | --- | --- |
| P1: Critical | Complete service outage; major customer impact | Immediate | 4 hours |
| P2: High | Significant degradation; significant user impact | 30 minutes | 8 hours |
| P3: Medium | Partial degradation; workaround available | 4 hours | 3 business days |
| P4: Low | Minor issue; minimal impact | 1 business day | 5 business days |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 20000-1:2018 | IT Service Management Systems | ITSM framework compliance |
| ITIL 4 | Foundation, Practices, and Guiding Principles | Service management process model |
| COBIT 2025 | DSS02: Manage Service Requests and Incidents | Incident and request management |
| COBIT 2025 | DSS03: Manage Problems | Problem management |
| EU NIS 2 Directive | Incident Reporting and Business Continuity | Cybersecurity incident notification |
| CSA CCM v5 | SEF and GOV Domains | Service and governance controls |
| NIST SP 800-61r3 | Computer Security Incident Handling Guide | Incident handling integration |

---

**End of Document**
