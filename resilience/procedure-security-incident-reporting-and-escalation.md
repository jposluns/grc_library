# Security Incident Reporting and Escalation Procedure

**Document Title:** Security Incident Reporting and Escalation Procedure
**Document Type:** Procedure
**Version:** 0.0.1
**Date:** 2026 05 26
**Owner:** Security Owner
**Approving Authority:** Governance Library Maintainer
**Related Documents:** `security/policy-information-security.md`, `security/standard-logging-and-monitoring.md`, `resilience/procedure-incident-response.md`, `resilience/procedure-data-protection-and-privacy-breach-response.md`, `resilience/plan-crisis-communication.md`, `resilience/framework-business-continuity-and-resilience.md`
**Classification:** Public
**Category:** Resilience
**Review Frequency:** Annual and upon material incident, threat, legal, regulatory, supplier, privacy, or AI change
**Repository Path:** `resilience/procedure-security-incident-reporting-and-escalation.md`
**Confidentiality:** Public
**Licence:** CC0 1.0 Universal

---

## Purpose

This procedure defines a reusable process for reporting, triaging, escalating, documenting, and transferring security incidents into incident response, privacy breach response, crisis management, supplier escalation, or risk governance processes.

---

## Scope

This procedure applies to suspected or confirmed incidents affecting information systems, identities, data, cloud services, suppliers, endpoints, networks, applications, logs, AI systems, physical-digital dependencies, or critical business services.

---

## Reportable Events

Events should be reported when they involve or may involve:

- Unauthorized access or attempted unauthorized access.
- Privileged access misuse.
- Credential compromise.
- Malware, ransomware, destructive activity, or suspicious code execution.
- Data loss, leakage, corruption, unauthorized disclosure, or unauthorized retention.
- Security monitoring or logging failure affecting investigation.
- Supplier security incident affecting services or data.
- Cloud control plane compromise or material misconfiguration.
- AI prompt injection, indirect prompt injection, unsafe tool execution, data poisoning, retrieval leakage, model inversion, membership inference, unauthorized model use, or training data exposure.
- Business service outage with security, privacy, legal, or customer impact.

---

## Procedure

### Step 1: Report

Reports may originate from users, monitoring, suppliers, customers, audit, privacy, compliance, support channels, or automated detection. Reports must be captured in an approved internal record system by adopting organizations.

### Step 2: Triage

Initial triage must confirm known facts, affected systems, affected data classes, identities involved, supplier involvement, business impact, privacy impact, AI system impact, and immediate containment needs.

### Step 3: Classify Severity

Severity should consider data sensitivity, business criticality, attacker activity, privilege level, service impact, supplier exposure, privacy exposure, legal or regulatory implications, and potential harm.

### Step 4: Escalate

Escalate to incident response, privacy, legal, compliance, supplier, resilience, communications, executive, or crisis management roles according to severity and impact.

### Step 5: Preserve Evidence

Preserve relevant logs, alerts, messages, access records, system records, supplier notifications, AI prompts and outputs where appropriate, tool execution records, retrieval logs, and decision records according to internal evidence handling requirements.

### Step 6: Track Actions

Record containment actions, assigned owners, deadlines, decisions, communications, supplier actions, residual risk, and transfer to other processes.

### Step 7: Close or Transfer

Close only when the event is determined not to be an incident or after transfer to incident response, privacy breach response, crisis management, or corrective action governance.

---

## Minimum Record Fields

| Field | Description |
| --- | --- |
| Event ID | Internal identifier. |
| Reporter Role | Role or source reporting the event. |
| Date and Time | Event report time. |
| Event Summary | Factual summary without speculation. |
| Affected Assets | Systems, data classes, suppliers, AI systems, or services. |
| Initial Severity | Low, moderate, high, critical, or pending. |
| Escalation Path | Roles or processes notified. |
| Evidence Preserved | Evidence classes captured. |
| Immediate Actions | Containment or investigation actions. |
| Status | Open, transferred, false positive, closed. |

---

## Limitations

This procedure is a public-domain baseline. Adopting organizations must define actual contact channels, escalation thresholds, legal notification requirements, regulatory timelines, evidence handling rules, and internal tooling.

---

**End of Document**
