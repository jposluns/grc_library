# Logging and Monitoring Standard

**Document Title:** Logging and Monitoring Standard\
**Document Type:** Standard\
**Version:** 1.4.13\
**Date:** 2026-07-10\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/procedure-security-incident-response.md`](procedure-security-incident-response.md), [`governance/register-digital-trust-and-assurance-metrics.md`](../governance/register-digital-trust-and-assurance-metrics.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material threat, framework, or regulatory change\
**Repository Path:** [`security/standard-logging-and-monitoring.md`](standard-logging-and-monitoring.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

This standard establishes enterprise-wide requirements for system logging, monitoring, telemetry collection, and alert management to support threat detection, forensic analysis, and compliance verification. Consolidates the former Logging Policy, Monitoring Procedure, and SIEM Integration Standard.

---

## 1. Purpose

To ensure that consistent, auditable, and secure handling of log data is maintained, aligned with ISO/IEC 27002:2022 §8.15, NIST SP 800-92, COBIT 2019 DSS05, CSA CCM v4.1 LOG-01 and LOG-03, and the EU NIS 2 Directive.

---

## 2. Scope

1. Applies to all systems, applications, services, network devices, cloud environments, and AI systems that process or store organizational data.
2. Includes infrastructure managed internally or by third parties, including SaaS, PaaS, and IaaS services.
3. Applies to logs generated for security, operational, compliance, and AI accountability purposes. Where the organization participates in a sector-specific programme (for example, BASC trade-security), the corresponding sector annex extends this standard with programme-specific log categories and retention overlays; see [`compliance/`](../compliance/).

### 2.1 Scope boundary with the operations observability and telemetry standard

This standard governs security-relevant logging, monitoring, and SIEM operations. The operations observability and telemetry standard ([`operations/standard-observability-and-telemetry.md`](../operations/standard-observability-and-telemetry.md)) governs operational health signals (metrics, traces, latency, error rate, customer-experience telemetry).

| Event class | Authoritative destination |
| --- | --- |
| Authentication, authorization, privilege changes, secret access, security-policy outcomes | SIEM (per this standard) |
| Data access, data export, classification-tagged operations | SIEM (per this standard) |
| Incident and threat-detection signals, anti-malware, EDR, DLP | SIEM (per this standard) |
| Service availability, latency, throughput, error rate, request traces | Observability platform (per the observability standard) |
| Capacity, saturation, resource utilization | Observability platform |
| Customer-experience signals (real-user monitoring, synthetic checks) | Observability platform |
| Events that are both security-relevant and operational (e.g. an authentication failure inside a request, or a privileged action during an outage) | Both: emitted to SIEM and to the observability platform, correlated by trace identifier and request identifier so the two backends can be joined for investigation |

Where an event is genuinely dual-purpose, the producer service emits the security record to the security pipeline and the operational record to the observability platform; both records share the same trace identifier per the observability standard. This avoids security teams missing operational context for threat analysis and operational teams missing security implications of operational events.

---

## 3. Governance and accountability

- The CISO is accountable for centralized logging and monitoring capabilities.
- The Security Operations Center (SOC) manages log collection, storage, correlation, and alerting.
- The CIO ensures that integration with enterprise infrastructure and business systems is maintained.
- System owners and third-party service providers are responsible for compliant logging configurations.

Sector-conditional roles (for example, a BASC Regional Compliance Officer who oversees logging for BASC-certified logistics and customs systems, with trade-security logs capturing cargo inspection results, customs-transaction records, and personnel screening activities) apply where the organization participates in a covered sector programme; see [`compliance/`](../compliance/).

---

## 4. Control statements

### 4.1 Log generation and coverage

4.1.1 All systems must generate security, operational, and access logs sufficient to reconstruct significant events including authentication, privilege changes, configuration modifications, and data transfers.

4.1.2 Logs must include at minimum:
- Timestamp (UTC or synchronized to NTP).
- Event type and category.
- Source and destination identifiers (IP, hostname, process ID, or user ID).
- Result or status code.
- Identity of the initiating user or system component.

4.1.3 Logs for cloud or AI systems must include provider identifiers, API actions, and model inference events.

4.1.4 BASC-regulated trade and customs platforms must log: cargo manifest creation, customs document transmission, cargo inspection results, and seal verification events. Each entry must include user ID, timestamp, facility identifier, and cargo reference number per BASC Section 6. Tamper-proof logging or WORM storage is mandatory for customs data records.

### 4.2 Time synchronization

4.2.1 All log sources must synchronize to approved enterprise NTP servers.
4.2.2 Any drift exceeding ±1 minute must trigger an automatic alert and corrective synchronization.

### 4.3 Centralized log collection

4.3.1 All logs must be forwarded to the enterprise SIEM within 60 seconds of generation where technically feasible.
4.3.2 Transmission must occur over encrypted channels (TLS 1.3 or better).
4.3.3 Logs from critical systems must be collected in near-real-time and verified for integrity through cryptographic hashing (SHA-256 minimum).

### 4.4 Retention and protection

4.4.1 Security and audit logs must be retained per the tiered retention periods in [`governance/register-data-retention-schedule.md`](../governance/register-data-retention-schedule.md), which is authoritative and sets retention by log class (for example: access logs 1 year, privileged-access session logs 2 years, SIEM event logs 1 year hot plus 2 years cold, security incident records 7 years, AI decision and detection logs 7 years or 5 years after system decommission, whichever is longer). Sector-mandated logs are retained longer where legally required, including BASC-governed trade and customs logs required for regional audit and customs validation.
4.4.2 Log archives must be stored in write-once, read-many (WORM) or tamper-evident repositories, with BASC trade-data logs maintained in secure BASC-approved data centres or validated cloud regions.
4.4.3 Access to logs must be limited to authorized personnel with MFA and role-based access controls.
4.4.4 Logs containing personal, regulated, or customs data must be protected in accordance with GDPR, PIPEDA, PIPL, and BASC data-protection requirements.

### 4.5 Monitoring and alerting

4.5.1 The SOC must define correlation rules for detecting anomalies, intrusion attempts, and unauthorized activities aligned with MITRE ATT&CK and NIST CSF Detect Function, including alerts for cargo data tampering, unauthorized customs-system access, and BASC Section 6 trade-security controls.
4.5.2 Alerts must be triaged within 15 minutes for high severity and one hour for medium severity events.
4.5.3 Automated incident tickets must be generated for all critical alerts.
4.5.4 Dashboards must display real-time metrics on system health, event volume, and incident trends.

### 4.6 AI system logging and traceability

4.6.1 AI models and pipelines must produce event logs capturing training, testing, inference, and deployment activities.
4.6.2 Logs must include model identifiers, dataset references, input sources, output summaries, and decision outcomes.
4.6.3 AI security events (model drift, adversarial input, data poisoning) must be integrated with SIEM alerts for unified visibility.

### 4.7 Cloud and third-party logging

4.7.1 Service providers must deliver audit logs meeting enterprise requirements as part of contractual agreements.
4.7.2 Cloud-native logging (AWS CloudTrail, GCP Audit Logs, and cloud monitoring services) must be ingested into the enterprise SIEM via secure APIs.
4.7.3 Vendor log retention must be validated annually as part of the third-party assurance process.

### 4.8 Log review and use

4.8.1 SOC analysts must review critical event logs daily.
4.8.2 Weekly reviews must validate that correlation rules, thresholds, and data normalization remain effective.
4.8.3 Findings must feed into the risk register and continual improvement cycle. Sector-programme log anomalies (for example, BASC-related log anomalies where the organization participates in BASC) must be reported to the sector-conditional role defined by the relevant sector annex for sector-programme audit follow-up; see [`compliance/`](../compliance/).

### 4.9 Automation and AI integration

4.9.1 Automation scripts must handle repetitive log correlation, threat scoring, and alert enrichment.
4.9.2 Predictive analytics and AI-assisted monitoring tools may be used to identify anomalies and improve detection accuracy.
4.9.3 All automated decisions must be explainable and logged for audit review.

### 4.10 Continual improvement

4.10.1 Log coverage, retention, and detection rules must be reassessed annually.
4.10.2 Lessons learned from incidents and audits must inform updates to this standard.

---

## 5. Framework alignment

| Control Area | ISO/IEC 27002 | NIST | COBIT 2019 | CSA CCM v4.1 | Legal |
| --- | --- | --- | --- | --- | --- |
| Log management | §8.15 | SP 800-92 | DSS05.01 | LOG-01 | GDPR Art. 32, PIPEDA |
| Time synchronization | §8.15.3 | SP 800-92 §4.2 | DSS01.03 | LOG-06 | SOX |
| Central collection and retention | §8.15.5 | CSF Detect | DSS05.02 | LOG-02 | NIS 2 Directive |
| Access and protection | §8.15.7 | SP 800-53 AC-6 | DSS05.04 | LOG-04 | Privacy laws |
| AI system traceability | N/A | AI RMF | DSS05.06 | LOG-09 | ENISA AI Certification Scheme |
| Monitoring and alerting | §8.16 | CSF Respond | DSS05.03 | LOG-03 | Incident reporting laws |
| BASC trade logging | N/A | N/A | N/A | N/A | BASC v6, WCO SAFE, ISO 28000 |



**End of Document**
