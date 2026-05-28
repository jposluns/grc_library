# Logging and Monitoring Standard

**Document Title:** Logging and Monitoring Standard  
**Document Type:** Standard  
**Version:** 1.3.0  
**Date:** 2026-05-27  
**Owner:** Chief Information Security Officer  
**Approving Authority:** Governance Library Maintainer  
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/procedure-incident-response.md`](procedure-incident-response.md), [`governance/register-digital-trust-and-assurance-metrics.md`](../governance/register-digital-trust-and-assurance-metrics.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md)  
**Classification:** Public  
**Category:** Information Security  
**Review Frequency:** Annual and upon material threat, framework, or regulatory change  
**Repository Path:** [`security/standard-logging-and-monitoring.md`](standard-logging-and-monitoring.md)  
**Confidentiality:** Public  
**Licence:** CC0 1.0 Universal  

This standard establishes enterprise-wide requirements for system logging, monitoring, telemetry collection, and alert management to support threat detection, forensic analysis, and compliance verification. Consolidates the former Logging Policy, Monitoring Procedure, and SIEM Integration Standard.

---

## Purpose

To ensure consistent, auditable, and secure handling of log data aligned with ISO/IEC 27002:2022 §8.15, NIST SP 800-92, COBIT 2025 DSS05, CSA CCM v5 IVS-09 and SEF-01, and the EU NIS 2 Directive.

---

## Scope

1. Applies to all systems, applications, services, network devices, cloud environments, and AI systems that process or store organizational or trade data, including BASC-certified logistics, customs, and supply-chain environments operating in Latin America.
2. Includes infrastructure managed internally or by third parties, including SaaS, PaaS, and IaaS services supporting trade, cargo, or customs-related processes.
3. Applies to logs generated for security, operational, compliance, AI accountability, and BASC trade-security assurance purposes.

---

## Governance and Accountability

- The CISO is accountable for centralized logging and monitoring capabilities.
- The Security Operations Center (SOC) manages log collection, storage, correlation, and alerting.
- The CIO ensures integration with enterprise infrastructure and business systems.
- System owners and third-party service providers are responsible for compliant logging configurations.
- Regional BASC Compliance Officers oversee logging for BASC-certified logistics and customs systems, with trade-security logs capturing cargo inspection results, customs-transaction records, and personnel screening activities.

---

## Control Statements

### 1. Log Generation and Coverage

1.1 All systems shall generate security, operational, and access logs sufficient to reconstruct significant events including authentication, privilege changes, configuration modifications, and data transfers.

1.2 Logs must include at minimum:
- Timestamp (UTC or synchronized to NTP).
- Event type and category.
- Source and destination identifiers (IP, hostname, process ID, or user ID).
- Result or status code.
- Identity of the initiating user or system component.

1.3 Logs for cloud or AI systems shall include provider identifiers, API actions, and model inference events.

1.4 BASC-regulated trade and customs platforms must log: cargo manifest creation, customs document transmission, cargo inspection results, and seal verification events. Each entry shall include user ID, timestamp, facility identifier, and cargo reference number per BASC Section 6. Tamper-proof logging or WORM storage is mandatory for customs data records.

### 2. Time Synchronization

2.1 All log sources must synchronize to approved enterprise NTP servers.
2.2 Any drift exceeding ±1 minute shall trigger an automatic alert and corrective synchronization.

### 3. Centralized Log Collection

3.1 All logs shall be forwarded to the enterprise SIEM within 60 seconds of generation where technically feasible.
3.2 Transmission must occur over encrypted channels (TLS 1.3 or better).
3.3 Logs from critical systems must be collected in near-real-time and verified for integrity through cryptographic hashing (SHA-256 minimum).

### 4. Retention and Protection

4.1 Security and audit logs shall be retained for a minimum of seven years or longer where legally mandated, including BASC-governed trade and customs logs required for regional audit and customs validation.
4.2 Log archives must be stored in write-once, read-many (WORM) or tamper-evident repositories, with BASC trade-data logs maintained in secure BASC-approved data centres or validated cloud regions.
4.3 Access to logs must be limited to authorized personnel with MFA and role-based access controls.
4.4 Logs containing personal, regulated, or customs data must be protected in accordance with GDPR, CPPA, PIPL, and BASC data-protection requirements.

### 5. Monitoring and Alerting

5.1 The SOC shall define correlation rules for detecting anomalies, intrusion attempts, and unauthorized activities aligned with MITRE ATT&CK and NIST CSF Detect Function, including alerts for cargo data tampering, unauthorized customs-system access, and BASC Section 6 trade-security controls.
5.2 Alerts must be triaged within 15 minutes for high severity and one hour for medium severity events.
5.3 Automated incident tickets must be generated for all critical alerts.
5.4 Dashboards shall display real-time metrics on system health, event volume, and incident trends.

### 6. AI System Logging and Traceability

6.1 AI models and pipelines shall produce event logs capturing training, testing, inference, and deployment activities.
6.2 Logs must include model identifiers, dataset references, input sources, output summaries, and decision outcomes.
6.3 AI security events (model drift, adversarial input, data poisoning) must be integrated with SIEM alerts for unified visibility.

### 7. Cloud and Third-Party Logging

7.1 Service providers must deliver audit logs meeting enterprise requirements as part of contractual agreements.
7.2 Cloud-native logging (AWS CloudTrail, GCP Audit Logs, and cloud monitoring services) must be ingested into the enterprise SIEM via secure APIs.
7.3 Vendor log retention must be validated annually as part of the third-party assurance process.

### 8. Log Review and Use

8.1 SOC analysts shall review critical event logs daily.
8.2 Weekly reviews shall validate that correlation rules, thresholds, and data normalization remain effective.
8.3 Findings must feed into the risk register and continual improvement cycle. BASC-related log anomalies shall be reported to Regional BASC Compliance Officers for trade-security audit follow-up.

### 9. Automation and AI Integration

9.1 Automation scripts shall handle repetitive log correlation, threat scoring, and alert enrichment.
9.2 Predictive analytics and AI-assisted monitoring tools may be used to identify anomalies and improve detection accuracy.
9.3 All automated decisions shall be explainable and logged for audit review.

### 10. Continual Improvement

10.1 Log coverage, retention, and detection rules shall be reassessed annually.
10.2 Lessons learned from incidents and audits shall inform updates to this standard.

---

## Framework Alignment

| Control Area | ISO/IEC 27002 | NIST | COBIT 2025 | CSA CCM v5 | Legal |
| --- | --- | --- | --- | --- | --- |
| Log management | §8.15 | SP 800-92 | DSS05.01 | IVS-09 | GDPR Art. 32, CPPA |
| Time synchronization | §8.15.3 | SP 800-92 §4.2 | DSS01.03 | ISM-04 | SOX |
| Central collection and retention | §8.15.5 | CSF Detect | DSS05.02 | SEF-01 | NIS 2 Directive |
| Access and protection | §8.15.7 | SP 800-53 AC-6 | DSS05.04 | ISM-03 | Privacy laws |
| AI system traceability | — | AI RMF | DSS05.06 | IVS-09 | ENISA AI Certification Scheme |
| Monitoring and alerting | §8.16 | CSF Respond | DSS05.03 | SEF-01 | Incident reporting laws |
| BASC trade logging | — | — | — | — | BASC v6, WCO SAFE, ISO 28000 |



**End of Document**
