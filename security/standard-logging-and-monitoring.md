# Logging and Monitoring Standard

**Document Title:** Logging and Monitoring Standard
**Document Type:** Standard
**Version:** 0.0.1
**Date:** 2026 05 26
**Owner:** Chief Information Security Officer
**Approving Authority:** Governance Library Maintainer
**Related Documents:** `security/policy-information-security.md`, `security/procedure-incident-response.md`, `governance/register-digital-trust-and-assurance-metrics.md`, `ai/standard-ai-security-and-risk.md`
**Classification:** Public
**Category:** Information Security
**Review Frequency:** Annual and upon material architecture, threat, or regulatory change
**Repository Path:** `security/standard-logging-and-monitoring.md`
**Confidentiality:** Public
**Licence:** CC0 1.0 Universal

---

## Purpose

This standard defines minimum logging, monitoring, alerting, retention, and evidence requirements for systems, services, identities, applications, cloud environments, suppliers, and AI systems.

---

## Requirements

### 1. Log Source Coverage

Logging coverage should include, proportionate to risk:

- Authentication and authorization events.
- Privileged access activity.
- Administrative actions.
- Configuration changes.
- Security control events.
- Network access events.
- Application and API access events.
- Data access and data export events.
- Cloud control plane activity.
- Endpoint and server security events.
- Supplier portal and managed service activity where available.
- AI prompts, tool calls, retrieval events, model outputs, policy blocks, and administrative AI configuration changes where appropriate and lawful.

### 2. Log Content

Logs should contain sufficient context to support investigation, including timestamp, actor, source, target, action, outcome, session or request identifier, affected object, and relevant control decision.

Logs must not retain more sensitive data than necessary. Prompt, file, output, and data-access logs for AI systems must be governed as data records.

### 3. Monitoring

Monitoring must identify unauthorized access, policy violation, suspicious behaviour, control failure, data leakage, suspicious AI tool use, abnormal retrieval activity, anomalous administrative action, and material service degradation.

### 4. Alerting

Alerts must have severity, owner, response expectation, escalation path, and closure criteria. Alert logic must be reviewed to reduce noise and prevent evidence burial under operational confetti.

### 5. Retention

Retention must reflect legal, regulatory, contractual, operational, security, privacy, and investigation requirements. Retention must avoid unnecessary storage of sensitive prompt, output, personal, or regulated data.

### 6. Integrity and Access

Security-relevant logs must be protected against unauthorized modification, deletion, and disclosure. Access to logs must be limited, reviewed, and monitored.

### 7. Evidence

Logging and monitoring configurations, alert rules, review records, incident links, and exception approvals must be retained as evidence.

---

## Minimum Evidence

- Logging coverage register.
- Monitoring rule register.
- Alert runbook.
- Log retention schedule.
- Access review for log platforms.
- Test evidence for critical alerts.
- Incident records linked to alerts.
- Exceptions and compensating controls.

---

**End of Document**
