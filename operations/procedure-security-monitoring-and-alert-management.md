# Security Monitoring and Alert Management Procedure

**Document Title:** Security Monitoring and Alert Management Procedure\
**Document Type:** Procedure\
**Version:** 1.3.1\
**Date:** 2026-05-28\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`operations/standard-production-security-requirements.md`](standard-production-security-requirements.md)\
**Classification:** Public\
**Category:** Operations\
**Review Frequency:** Annual and upon material platform or regulatory change\
**Repository Path:** [`operations/procedure-security-monitoring-and-alert-management.md`](procedure-security-monitoring-and-alert-management.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

This procedure defines the operational processes for ingesting logs, triaging SIEM alerts, managing automated incident tickets, escalating to incident response, maintaining detection rules, and reporting security monitoring metrics.

---

## 1. Purpose and scope

### 1.1 Purpose

To ensure that security events from all production systems and environments are collected, normalized, correlated, and acted upon in a timely and consistent manner. This procedure operationalizes the control requirements established in the Logging and Monitoring Standard, providing the Security Operations Centre (SOC) with a clear and repeatable workflow from log ingestion through alert closure or escalation to the Incident Response Procedure.

Effective security monitoring reduces mean time to detect (MTTD) threats, ensures that required alert categories are always active, and provides auditable evidence of continuous monitoring for compliance with ISO/IEC 27002, NIST CSF Detect, and CSA CCM LOG/SEF domains.

### 1.2 Scope

1. Applies to all SIEM-connected log sources including on-premises servers, cloud platform infrastructure, network devices, identity infrastructure, endpoint protection platforms, backup systems, and applications.
2. Applies to all SOC analysts, Security Engineering staff, IT Operations personnel who respond to SIEM-generated alerts or tickets, and the CISO who receives monitoring metrics.
3. Covers alert triage, ticket management, escalation, dashboard operations, rule tuning, and AI-assisted detection.
4. Applies to BASC-certified trade and customs environments where cargo, customs transaction, and seal-verification event logs are ingested into the SIEM.

---

## 2. Governance

| Role | Responsibility |
| --- | --- |
| **CISO** | Accountable for the security monitoring programme; approves the alert rule catalogue; receives monthly metrics; authorizes changes to critical detection rules. |
| **Security Operations Centre (SOC)** | Operates the SIEM; triages and manages alerts; escalates confirmed incidents; maintains dashboards; performs weekly rule tuning; documents all alert dispositions. |
| **Security Engineering** | Designs and maintains correlation rules and detection logic; maps rules to MITRE ATT&CK; implements SIEM integrations for new log sources; manages AI detection configurations. |
| **IT Operations** | Ensures that log source connectivity and agent health; resolves log ingestion failures within defined SLAs; assists with infrastructure-level investigation of alerts. |
| **Internal Audit** | Reviews SOC operational records, SLA adherence, and rule maintenance logs annually. |

Sector-conditional roles (for example, a BASC Regional Compliance Officer who receives escalated notifications for trade-security anomalies and coordinates with customs authorities where required) apply where the organisation participates in a covered sector programme; see [`compliance/`](../compliance/).

---

## 3. Log ingestion and normalization

### 3.1 Ingestion SLA

All log sources must forward events to the SIEM within 60 seconds of generation where technically feasible, as required by the Logging and Monitoring Standard §3.1. Logs must be transmitted over encrypted channels using TLS 1.3 or higher.

IT Operations monitors the log ingestion pipeline daily. Any log source that ceases forwarding logs for more than 10 minutes during business hours triggers an automated alert to both IT Operations and the SOC. Failure of a critical log source (identity infrastructure, endpoint protection, firewall, backup) to forward for more than 30 minutes is treated as a P2 incident.

### 3.2 Time synchronization

All log sources must synchronize to approved enterprise NTP servers. Clock drift exceeding ±1 minute from the enterprise NTP source triggers an automated corrective synchronization request and an alert to IT Operations. Accurate timestamps are essential for correlation and forensic admissibility. Events with timestamps deviating more than ±5 minutes are flagged in the SIEM with a data-quality annotation pending investigation.

### 3.3 Integrity verification

Logs from critical systems must be verified for integrity using SHA-256 cryptographic hashing at the point of collection. Hash values are stored separately from log content. Any mismatch between the stored hash and the received log content is treated as a potential tampering event and escalated immediately to the CISO and SOC lead.

### 3.4 Log normalization

The SIEM normalizes all ingested logs to a common event schema to enable consistent correlation across heterogeneous log sources. The normalization pipeline:

- Maps vendor-specific field names to the enterprise event taxonomy.
- Enriches events with asset context (asset classification, owner, environment tier) from the asset register.
- Resolves IP addresses to hostnames and tags events with network zone designations.
- Tags events from BASC-regulated environments with a BASC scope indicator for targeted rule application.

Normalization rule coverage is reviewed monthly by Security Engineering. Sources with persistent normalization failures are flagged for pipeline remediation.

### 3.5 Log source inventory

Security Engineering maintains a SIEM log source inventory that records, for each source: source name and type; connection method; log format and volume; last successful ingestion timestamp; and normalization pipeline version. The inventory is reconciled against the asset register quarterly. Any production asset not present in the log source inventory is raised as a compliance finding.

---

## 4. SIEM alert rule catalogue

The following alert categories must be configured, tested, and active before any system is promoted to production, as required by the Production Security Requirements Standard §3.1. Each rule must have an assigned severity, a defined triage SLA, and an owner in Security Engineering responsible for ongoing tuning.

| Alert Category | Description | Severity | Triage SLA |
| --- | --- | --- | --- |
| Failed authentication: brute-force threshold | Multiple failed logins from a single source within a rolling time window, exceeding the defined threshold for the account type. | High | 1 hour |
| Privileged access outside approved change windows | Any privileged account login or administrative action occurring outside the approved change or maintenance window schedule. | High | 1 hour |
| Multiple failed PAM login attempts | Consecutive failed authentication attempts against the PAM vault, exceeding the defined threshold. | Critical | 15 minutes |
| Emergency account usage | Use of any break-glass or emergency account at any time. | Critical | 15 minutes |
| PAM bypass | Privileged action performed without a PAM session record, indicating circumvention of the PAM workflow. | Critical | 15 minutes |
| New admin account creation | Creation of a new account with administrative or privileged role membership in any directory or system. | High | 1 hour |
| Directory service and trust changes | Modifications to Group Policy Objects, FSMO role changes, domain or forest trust creation or modification, or schema changes. | High | 1 hour |
| Firewall rule changes | Any addition, deletion, or modification to a firewall or ACL rule set outside an approved change window. | High | 1 hour |
| Backup failure | Any backup job failure or partial failure for a production workload. | High | 1 hour |
| Certificate near-expiry: 60 days | Any production certificate reaching 60 days before expiry. | Medium | Same day |
| Certificate near-expiry: 30 days | Any production certificate reaching 30 days before expiry. | High | 1 hour |
| Endpoint protection alert | Any malware detection, behavioural alert, or tamper event generated by the endpoint detection and response (EDR) platform. | High | 1 hour |
| DNS anomaly | Unusual DNS query volume, queries to newly-registered or categorized malicious domains, DNS tunnelling indicators, or internal DNS configuration changes. | High | 1 hour |
| Backup deletion attempt: immutable repository | Any attempt to delete or modify backup data in the immutable backup repository. | Critical | 15 minutes |
| SIEM workspace deletion attempt | Any attempt to delete or modify the SIEM workspace or its log retention policies. | Critical | 15 minutes |
| Identity threat detection platform alert | Any high or critical alert from the identity threat detection platform, including lateral movement, pass-the-hash, Kerberoasting, and suspicious replication indicators. | Critical | 15 minutes |
| BASC environment anomaly | Unauthorized access attempt to BASC-certified customs or cargo systems, or anomalous cargo manifest modification. | High | 1 hour |

All rules in the catalogue are tested for correct alerting before production deployment and after any SIEM configuration change. Test results are documented and retained as evidence.

### 4.1 Rule severity definitions

| Severity | Definition |
| --- | --- |
| **Critical** | Indicates probable active compromise, privilege escalation, or safety-critical system event. Immediate response required. |
| **High** | Indicates a significant policy violation or indicator of potential compromise. Response required within 1 hour. |
| **Medium** | Indicates a policy deviation or anomaly requiring investigation but with lower immediate risk. Response required same business day. |
| **Low** | Informational finding or minor deviation. Reviewed in next scheduled review cycle. |

---

## 5. Alert triage workflow

### 5.1 Triage slas

| Severity | Time to Initial Triage | Time to Disposition |
| --- | --- | --- |
| Critical | 15 minutes | 1 hour |
| High | 1 hour | 4 hours |
| Medium | Same business day | Next business day |
| Low | Next scheduled review cycle | Within 5 business days |

Triage SLA timers start from the moment the SIEM generates the alert, not from the moment a SOC analyst first views it. Automated alerting to the on-call analyst begins the SLA clock.

### 5.2 Triage steps

For each alert, the triaging SOC analyst must:

1. **Acknowledge** the alert in the SIEM and ITSM platform to stop the SLA escalation clock.
2. **Assess context**: review the alert detail, enrichment data, recent activity from the same source, asset classification, and any related alerts.
3. **Classify the disposition:**
 - **True positive**: a genuine security event; escalate per §6 or §7.
 - **False positive**: the alert fired incorrectly; document the reason and submit to Security Engineering for rule tuning review.
 - **Informational / expected**: a known authorized event that triggered the rule; document and close with justification.
 - **Needs further investigation**: insufficient context to decide; escalate to SOC lead for senior review.
4. **Document the disposition** in the ITSM ticket with timestamps, evidence references, and the analyst's reasoning.
5. **Close or escalate** the ticket with all required fields completed.

No alert may be closed without a documented disposition. Bulk-closing alerts without individual review is prohibited.

### 5.3 After-hours coverage

Critical and High severity alerts must be triaged within SLA at all times, including outside standard business hours. The SOC maintains an on-call rotation for after-hours response. On-call contacts are maintained in the operational state register. If the on-call analyst cannot be reached within 10 minutes of an automated page for a Critical alert, the SOC lead is paged automatically.

---

## 6. Automated ticket creation

All Critical severity alerts must generate an automated incident ticket in the ITSM platform at the moment the SIEM creates the alert. Automated ticket creation must:

- Assign the ticket to the on-duty SOC analyst queue.
- Populate the ticket with: alert name, severity, timestamp, affected asset(s), alert rule identifier, and a direct link to the SIEM alert detail.
- Set the ticket priority to P1 for Critical alerts and P2 for High alerts.
- Trigger the on-call paging workflow for Critical alerts.

The automated ticket creation pipeline is tested weekly by Security Engineering. Any failure in the automated pipeline for Critical alerts is treated as a P2 incident.

High severity alerts generate automated tickets with P2 priority. Medium and Low severity alerts are aggregated into daily review queues in the ITSM platform for SOC analyst review.

---

## 7. Escalation paths

### 7.1 Escalation to incident response

Any alert triaged as a confirmed true positive indicating active compromise, data exfiltration, unauthorized privileged access, or a threat to system availability must be immediately escalated to the Incident Response Procedure. The SOC analyst:

1. Sets the ITSM ticket to "Escalated: Incident Response."
2. Notifies the Incident Commander per the Incident Response Procedure notification chain.
3. Preserves SIEM alert context, timeline, and associated log evidence before any containment action is taken.
4. Maintains the SIEM alert open and linked to the incident ticket for the duration of the incident.

The CISO is notified immediately for any P1 incident declaration arising from a SIEM alert.

### 7.2 P1 escalation decision

A SIEM alert triggers P1 incident declaration when any of the following indicators are present:

- Confirmed malware or ransomware execution on a production server.
- Evidence of lateral movement involving a Tier 0 or Tier 1 asset.
- Confirmed PAM vault breach or emergency account misuse.
- Evidence of data exfiltration of Confidential or Restricted data.
- Active attack on backup or SIEM infrastructure.

In the absence of a clear indicator, the SOC lead escalates ambiguous high-severity situations to the CISO for declaration decision.

### 7.3 Sector-programme anomaly escalation

Where the organisation participates in a sector programme that defines elevated-escalation alert categories (for example, BASC for trade and customs, healthcare-sector escalation for PHI access anomalies, financial-sector escalation for payment-rail anomalies), SIEM alerts tagged with the sector scope indicator that are triaged as true positives within the annex-defined trigger categories are escalated to the sector-conditional role defined by the relevant sector annex (for example, a BASC Regional Compliance Officer for the BASC programme) within the annex's stated timeframe. The sector-conditional role determines whether onward sector-authority notification is required. See [`compliance/`](../compliance/) for sector-specific escalation paths, triggers, and timeframes.

### 7.4 Identity threat escalation

Critical alerts from the identity threat detection platform, including Kerberoasting, pass-the-hash, DCSync, or suspicious replication activity, are automatically escalated to a P1 investigation workflow regardless of the number of affected accounts. The Privileged Access Management team is notified concurrently.

---

## 8. Dashboard and reporting

### 8.1 Real-time dashboards

The SOC operates real-time dashboards providing continuous visibility into:

- Active alert queue by severity and age.
- Log ingestion health: sources, volumes, and last-received timestamps.
- Endpoint protection coverage and agent health.
- Failed authentication counts by source and target.
- Certificate expiry countdown for production certificates.
- Active incident tickets and their current status.
- BASC environment event summary for environments in scope.

Dashboards are accessible to SOC analysts, Security Engineering, IT Operations leads, and the CISO. Dashboard access is role-based and governed by the Identity and Access Management Policy.

### 8.2 Daily review

SOC analysts review critical event logs daily. The daily review must cover:

- All Critical and High alerts from the previous 24 hours and their dispositions.
- Any log source that was offline or degraded in the previous 24 hours.
- Any automated ticket that has not been acknowledged within SLA.
- Any anomalies in log volume that may indicate source failure or suppression.

Daily review findings are recorded in the SOC shift log.

### 8.3 Weekly rule tuning review

Security Engineering conducts a weekly review of correlation rule performance. The review examines:

- False positive rates by rule (target: < 5% per rule).
- Rules that have not fired in the past 30 days (potential dead rules or ingestion gaps).
- New threat intelligence or MITRE ATT&CK technique coverage gaps.
- Rule changes required to address feedback from the week's alert triage.

Outcomes of the weekly review are documented and tracked. Approved rule changes are implemented via the change management process.

### 8.4 Monthly metrics report

Security Engineering compiles a monthly metrics report for the CISO. The report includes all metrics defined in §11 and a narrative summary covering notable incidents, detection improvements, and ongoing tuning actions. The monthly report is presented to the CISO within 5 business days of month-end.

---

## 9. SIEM rule tuning and maintenance

### 9.1 Change control for SIEM rules

All changes to SIEM detection rules, data connectors, and normalization pipelines are governed by the Change Management and Configuration Control Procedure. Changes to critical detection rules (those covering the mandatory alert categories in §4) require High-risk change classification and CISO approval before implementation.

### 9.2 False positive target

The target false positive rate for any individual SIEM correlation rule is less than 5%, measured over a rolling 30-day period. Rules consistently exceeding the false positive target are reviewed by Security Engineering for tuning or replacement. Rules cannot be disabled to reduce false positives without CISO approval and a compensating detection control.

### 9.3 MITRE ATT&CK mapping

All active SIEM correlation rules must be mapped to at least one MITRE ATT&CK technique or sub-technique. Security Engineering maintains the SIEM rule-to-MITRE mapping in the SIEM rule register. The mapping is reviewed quarterly against the current MITRE ATT&CK version to identify new technique coverage opportunities. Coverage gaps for techniques assessed as high-relevance to the organisation's threat profile are prioritized for new rule development.

### 9.4 New log source onboarding

When a new system or application is deployed, the project team must engage Security Engineering at least 10 business days before the go-live date to design and test the log ingestion pipeline and any required new correlation rules. No system may go live without confirmed SIEM ingestion and the alert categories in §4 active, as required by the Production Security Requirements Standard §3.2.

### 9.5 Rule register

Security Engineering maintains a SIEM rule register documenting, for each active rule: rule name and identifier; detection objective; MITRE ATT&CK mapping; severity; triage SLA; last tuning date; false positive rate (30-day rolling); and the Security Engineering owner. The rule register is reviewed by the CISO quarterly.

---

## 10. AI-assisted detection

### 10.1 Anomaly detection capabilities

The SIEM operates AI-driven anomaly detection to identify threats that may not trigger signature or threshold-based rules. Anomaly detection use cases include:

- Compromised account detection: unusual login times, atypical source locations, abnormal access patterns relative to the user's behavioural baseline.
- Access misuse indicators: bulk data access, unusual export volumes, or access to resources outside the user's normal scope.
- Insider threat indicators: anomalous patterns combining access, email, and file activity.
- BASC environment anomalies: unusual cargo manifest activity or atypical customs-system access patterns.

Anomaly models are trained on organisational baseline data and refreshed at minimum quarterly. The baseline period used for training must not include known compromise periods.

### 10.2 Anomaly alert handling

Anomaly detections appear in the SIEM as alerts and are triaged using the same workflow as rule-based alerts. Anomaly alerts are labelled as AI-generated in the SIEM and ITSM ticket to distinguish them from deterministic rule-based alerts. Triage of anomaly alerts must include an assessment of the model's confidence score and the supporting evidence used to generate the detection.

### 10.3 Explainability requirement

All automated AI-generated decisions, including anomaly scores, risk scores, and automated alert enrichments, must be explainable to the triaging analyst. The SIEM must present, alongside each AI-generated alert, a plain-language explanation of the specific behaviours or data points that contributed to the detection. Opaque or unexplainable AI detections must not be used as the sole basis for containment actions.

### 10.4 Audit logging of automated decisions

All AI-generated detections, model decisions, and automated enrichment actions are logged with their input data, model version, confidence score, and output. These logs are retained as part of the SIEM audit trail for a minimum of 7 years, consistent with the Logging and Monitoring Standard §4.1. AI model version changes that affect detection behaviour require Security Engineering review and documentation before deployment.

### 10.5 Model performance review

Security Engineering reviews AI detection model performance monthly. Reviews assess true positive rate, false positive rate, and missed detections (based on confirmed incidents). Models that show degraded performance or excessive false positives are retrained, tuned, or replaced. Model performance reviews are documented and made available to the CISO on request.

---

## 11. Metrics

The following metrics are tracked by the SOC, reported to the CISO monthly, and presented to the Enterprise Risk Committee quarterly:

| Metric | Target |
| --- | --- |
| Alert volume by severity (Critical, High, Medium, Low): monthly | Reviewed; significant unexplained volume changes investigated |
| Triage SLA adherence: Critical (≤ 15 minutes) | ≥ 99% |
| Triage SLA adherence: High (≤ 1 hour) | ≥ 95% |
| Triage SLA adherence: Medium (same day) | ≥ 90% |
| False positive rate per rule (30-day rolling) | < 5% per rule |
| Log source uptime (sources forwarding within SLA) | ≥ 99.5% |
| Automated ticket creation success rate for Critical alerts | 100% |
| MITRE ATT&CK coverage (% of high-relevance techniques with active rule) | Reviewed quarterly; improvement trend required |
| Mean time to detect (MTTD): confirmed incidents | Reviewed; quarter-on-quarter improvement target |
| AI anomaly detection false positive rate | < 10%; reviewed monthly |
| Sector-programme environment alerts escalated to the relevant sector-conditional role within annex SLA (where the organisation participates in a covered programme) | 100% |

---

## 12. Framework alignment

| Control Area | ISO/IEC 27002:2022 | NIST CSF | COBIT 2019 | CSA CCM v4.1 |
| --- | --- | --- | --- | --- |
| Log ingestion and integrity | §8.15 | Detect: DE.CM-7 | DSS05.03 | LOG-01, LOG-04, LOG-07 |
| Time synchronization | §8.15.3 | Detect: DE.CM-1 | DSS01.03 | LOG-03 |
| Alert rules and coverage | §8.16 | Detect: DE.CM-3, DE.CM-4 | DSS05.03 | LOG-09, SEF-01 |
| Alert triage and response | §8.16 | Respond: RS.RP-1 | DSS05.03 | SEF-02, SEF-03 |
| Automated ticket creation | §8.16 | Respond: RS.CO-1 | DSS05.03 | SEF-04 |
| Escalation to incident response | §5.25, §5.26 | Respond: RS.CO-3 | DSS02.01 | SEF-05, SEF-06 |
| Dashboards and reporting | §8.16 | Detect: DE.DP-5 | MEA01.04 | LOG-11, LOG-14 |
| Rule tuning and MITRE mapping | §8.16 | Detect: DE.DP-3 | DSS05.03 | LOG-10, SEF-09 |
| AI-assisted detection | §8.16 | Detect: DE.CM-7 | DSS05.03 | SEF-10 |

---

*This document is released under CC0 1.0 Universal. No rights reserved.*



**End of Document**
