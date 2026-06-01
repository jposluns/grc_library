# Threat Intelligence and SIEM Operations Procedure

**Document Title:** Threat Intelligence and SIEM Operations Procedure\
**Document Type:** Procedure\
**Version:** 1.3.0\
**Date:** 2026-05-27\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`operations/procedure-security-monitoring-and-alert-management.md`](procedure-security-monitoring-and-alert-management.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md)\
**Classification:** Public\
**Category:** Operations\
**Review Frequency:** Annual and upon material platform or regulatory change\
**Repository Path:** [`operations/procedure-threat-intelligence-and-siem-operations.md`](procedure-threat-intelligence-and-siem-operations.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose and scope

### 1.1 Purpose

This procedure defines the operational processes for managing threat intelligence, operating the Security Information and Event Management (SIEM) platform, developing and maintaining correlation rules, conducting threat hunting, and sharing intelligence with sector peers. It establishes the practices by which threat intelligence is operationalized into detection capability and feeds back into continual improvement of the organisation's security posture.

The procedure is aligned with NIST SP 800-150 (Guide to Cyber Threat Information Sharing), MITRE ATT&CK Enterprise, ISO/IEC 27001:2022 A.5.7, COBIT 2019 DSS05, and CSA CCM v4.1 TVM (Threat and Vulnerability Management) and SEF (Security Incident Management) domain controls.

### 1.2 Scope

1. Applies to all threat intelligence activities undertaken by the Security Operations Centre (SOC) and Threat Intelligence team, including collection, analysis, dissemination, and operationalization of intelligence.
2. Covers the full SIEM platform lifecycle: workspace health, data connector management, correlation rule development and maintenance, and alert triage.
3. Applies to threat hunting activities conducted within all environments under organisational control, including cloud platform, on-premises, and hybrid infrastructure.
4. Includes intelligence sharing with sector partners, government agencies, and industry consortia.

---

## 2. Governance

### 2.1 Roles and responsibilities

| Role | Responsibilities |
| --- | --- |
| **Chief Information Security Officer (CISO)** | Accountable for the threat intelligence and SIEM operations programme. Approves intelligence sharing agreements. Receives escalations for nation-state or advanced persistent threat (APT) activity. Reviews programme effectiveness at the quarterly security governance review. |
| **Threat Intelligence Lead** | Manages threat intelligence sources, validates indicators of compromise (IoCs), oversees the indicator management lifecycle, and maintains relationships with ISACs and government advisory bodies. |
| **SOC Manager** | Responsible for day-to-day SIEM operations, alert triage, correlation rule quality, and hunt programme delivery. Ensures that analyst coverage and escalation paths are maintained. |
| **SOC Analysts (Tier 1 to 3)** | Perform alert triage, initial investigation, indicator enrichment, rule tuning, and threat hunting. Document findings and feed lessons learned back into detection engineering. |
| **Detection Engineer** | Designs, tests, and deploys SIEM correlation rules. Maintains MITRE ATT&CK tactic-to-rule mappings. Validates rule performance metrics. |
| **Legal Counsel** | Advises on intelligence sharing agreements, obligations under information sharing frameworks, and escalation requirements for nation-state threat attribution. |

### 2.2 Governance cadence

| Forum | Frequency | Participants | Purpose |
| --- | --- | --- | --- |
| SOC Operations Review | Weekly | SOC Manager, SOC Analysts, Detection Engineer | Validate correlation rule effectiveness, data normalization quality, ingestion gaps, and alert thresholds |
| Threat Intelligence Review | Monthly | Threat Intelligence Lead, SOC Manager, CISO | Review intelligence feed coverage, new IoCs operationalized, hunt findings, and intelligence sharing activities |
| SIEM Rule Review | Bi-annual | Detection Engineer, SOC Manager, CISO | Full review of all active correlation rules; retire stale rules; validate MITRE ATT&CK coverage gaps |
| Security Governance Review | Quarterly | CISO, CIO, Legal Counsel | Programme metrics, risk posture, significant incidents, and regulatory considerations |

---

## 3. Threat intelligence sources

### 3.1 Source categories

The organisation maintains a diverse, layered threat intelligence programme drawing from the following source categories:

| Source Category | Examples | Ingestion Method |
| --- | --- | --- |
| **Open Source Intelligence (OSINT)** | VirusTotal, Shodan, AlienVault OTX, abuse.ch, Threat Fox | Automated feed ingestion via TAXII/STIX or API |
| **Commercial Vendor Feeds** | Contracted threat intelligence platforms providing curated IoCs, malware signatures, and adversary TTPs | API integration to SIEM and threat intelligence platform (TIP) |
| **Government Advisories** | CISA Known Exploited Vulnerabilities (KEV) catalogue; NCSC (UK) threat advisories; CCCS (Canadian Centre for Cyber Security) alerts and advisories | Manual review and automated feed where available |
| **Sector ISAC Memberships** | Relevant sector Information Sharing and Analysis Centre memberships per the organisation's sector profile | Encrypted email, portal, or STIX/TAXII feed |
| **Dark Web and Criminal Forums** | Monitored via contracted threat intelligence service for credential exposure and pre-attack planning indicators | Vendor-curated alerting |
| **Internal Telemetry** | SIEM-generated indicators from detected incidents, endpoint detection telemetry, DNS anomalies, and authentication failures | Automated from SIEM correlation output |
| **Incident Response Findings** | Indicators and TTPs identified during post-incident reviews | Manual ingestion following PIR completion |

### 3.2 Source evaluation

All threat intelligence sources are assessed at initial onboarding and annually thereafter against:

- **Reliability:** Track record of accurate, timely, and actionable intelligence.
- **Relevance:** Alignment with the organisation's threat landscape, industry, and geographic exposure.
- **Timeliness:** Speed of dissemination from discovery to feed availability.
- **Cost-effectiveness:** Value delivered relative to subscription or operational cost.

The Threat Intelligence Lead maintains a source registry documenting each source, its assessment rating, last review date, and current operational status.

---

## 4. Indicator management lifecycle

All threat intelligence indicators pass through a five-stage lifecycle before operationalization and remain managed until expiry or withdrawal.

### 4.1 Lifecycle stages

| Stage | Description | Responsible Role | Output |
| --- | --- | --- | --- |
| **1. Ingest** | Raw indicators received from all configured sources (OSINT, vendor, ISAC, government, internal). Ingested into the Threat Intelligence Platform (TIP) with source, confidence, and timestamp metadata. | Threat Intelligence Lead / SOC Analyst | Raw indicator record in TIP |
| **2. Validate** | De-duplicate against existing indicators. Verify indicator is not a known false positive (e.g., CDN ranges, internal IP ranges). Cross-reference against at least one additional source where possible. Assign confidence level (High / Medium / Low). | Threat Intelligence Lead | Validated indicator record with confidence score |
| **3. Enrich** | Augment with context: associated adversary group, MITRE ATT&CK tactic and technique, affected sectors, geolocation, associated malware family, and any known TTPs. AI-driven anomaly detection tools may be applied to identify correlated indicators suggesting compromised accounts or insider activity. | SOC Analyst (Tier 2 to 3) / Detection Engineer | Enriched indicator with ATT&CK mapping and contextual metadata |
| **4. Operationalize** | High- and medium-confidence indicators are pushed to the SIEM as watchlist entries, detection rules, or automated block rules (subject to change control). Low-confidence indicators are retained for hunting reference only. | Detection Engineer | Active detection rule or watchlist entry in SIEM |
| **5. Expire / Retire** | Indicators are aged out based on defined TTL (Time-to-Live) values by indicator type. Expired indicators are archived in the TIP and removed from active SIEM detection unless re-validated. | Threat Intelligence Lead | Archived indicator; SIEM rule deactivated or updated |

### 4.2 Indicator time-to-live (TTL) values

| Indicator Type | Default TTL | Rationale |
| --- | --- | --- |
| IP address | 30 days | IP addresses rotate frequently; stale IPs generate false positives |
| Domain name | 90 days | Domain infrastructure persists longer than IPs |
| File hash (MD5/SHA-1) | 180 days | Malware variants may share hashes over extended periods |
| File hash (SHA-256) | 365 days | Higher fidelity; lower false positive risk |
| URL | 30 days | URLs change frequently |
| YARA rule | Review at 180 days | Reviewed rather than auto-expired; may remain valid longer |
| CVE / vulnerability indicator | Until patched or mitigated in environment | Expires upon confirmed remediation |

TTL values may be extended by the Threat Intelligence Lead where intelligence warrants continued active monitoring. Extensions must be documented.

---

## 5. SIEM correlation rule development

### 5.1 Rule development principles

All SIEM correlation rules must:

1. Be mapped to one or more MITRE ATT&CK tactics and techniques, with the mapping documented in the rule metadata.
2. Define a clear detection hypothesis: what adversary behaviour or anomalous condition the rule is designed to detect.
3. Specify expected data sources, log types, and field dependencies.
4. Include a defined alert severity (Critical / High / Medium / Low) consistent with the incident severity framework in [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md).
5. Be tested against historical log data or a representative test dataset before deployment to production.
6. Comply with the pre-go-live SIEM validation requirements in [`operations/standard-production-security-requirements.md`](standard-production-security-requirements.md) §3.1: all required alert categories must be configured and verified before any system enters production.

### 5.2 MITRE ATT&CK tactic coverage

The detection rule library must maintain active coverage across the following MITRE ATT&CK tactics as a minimum baseline. Coverage gaps are reviewed at the bi-annual SIEM Rule Review and drive the detection engineering roadmap.

| MITRE ATT&CK Tactic | Coverage Priority | Notes |
| --- | --- | --- |
| Initial Access (TA0001) | Critical | Phishing, valid accounts, external remote services |
| Execution (TA0002) | Critical | Scripting, command-line interfaces, scheduled tasks |
| Persistence (TA0003) | Critical | Account creation, scheduled tasks, registry modifications |
| Privilege Escalation (TA0004) | Critical | Valid account abuse, exploitation for privilege escalation |
| Defence Evasion (TA0005) | High | Log clearing, masquerading, disabling security tools |
| Credential Access (TA0006) | Critical | Brute force, credential dumping, password spraying |
| Discovery (TA0007) | High | Network scanning, account enumeration |
| Lateral Movement (TA0008) | Critical | Pass-the-hash, remote services exploitation |
| Collection (TA0009) | High | Data staged for exfiltration |
| Command and Control (TA0011) | Critical | Known C2 frameworks, DNS tunnelling, encrypted C2 channels |
| Exfiltration (TA0010) | Critical | Large outbound transfers, data staged to cloud storage |
| Impact (TA0040) | Critical | Ransomware behaviour, data destruction, service disruption |

### 5.3 Rule development and deployment workflow

1. **Draft:** Detection Engineer documents the rule hypothesis, data sources, logic, and ATT&CK mapping.
2. **Peer Review:** A second SOC analyst or Detection Engineer reviews the rule logic, field dependencies, and expected false positive rate.
3. **Test:** Rule is validated against a sample of historical data or a designated test environment. Detection and false positive rates are recorded.
4. **Staging:** Rule is deployed in a monitoring-only (no-alert) mode for a minimum of 5 business days to assess noise level.
5. **Approval:** SOC Manager approves production deployment, noting rule ID, ATT&CK mapping, and test results.
6. **Production Deployment:** Rule is activated through the approved change management process per [`operations/procedure-change-management-and-configuration-control.md`](procedure-change-management-and-configuration-control.md).
7. **Documentation:** Rule is registered in the SIEM Alert Rule Register with all metadata fields completed.

### 5.4 Review cadence

- **Weekly:** SOC operations review validates that active rules are firing as expected and that alert volumes are within threshold.
- **Bi-annual:** Full rule library review reassesses all rules for continued relevance, ATT&CK coverage, and false positive rates. Rules that have not fired in six months are reviewed for retirement or refinement.
- **Post-incident:** Any incident that reveals a detection gap triggers immediate review of relevant rules or creation of a new rule.

---

## 6. SIEM platform operations

### 6.1 Workspace health monitoring

The SOC is responsible for the continuous operational health of the SIEM platform. Health monitoring covers:

| Health Dimension | Monitoring Requirement | Alert Threshold |
| --- | --- | --- |
| **Data connector status** | All configured connectors monitored for active/inactive state | Alert within 15 minutes of any critical connector going inactive |
| **Ingestion volume** | Daily ingestion volume monitored per source; baseline established over 30-day rolling window | Alert if any source drops more than 20% below baseline volume |
| **Ingestion latency** | Time from log generation to availability in SIEM | Alert if latency exceeds 5 minutes for critical sources |
| **Storage capacity** | Workspace storage utilization monitored | Alert at 80% capacity; escalate at 90% |
| **Query performance** | Alert query execution time monitored | Alert if scheduled query takes more than twice the historical average |
| **Rule health** | Active correlation rules monitored for execution errors | Alert on any rule error within 1 hour |

### 6.2 Data connector management

1. All data connectors must be documented in the SIEM connector registry, including: connector name, data source type, log types ingested, ingestion method, responsible owner, and last validated date.
2. New connectors require approval by the SOC Manager and must be tested before production activation.
3. Critical connectors (identity systems, endpoint detection and response (EDR) platform, network firewalls, cloud platform audit logs) must have redundant ingestion paths or compensating monitoring where technically feasible.
4. Connector performance is reviewed monthly. Any connector with persistent gaps is escalated to the SOC Manager for remediation or documented risk acceptance.

### 6.3 Ingestion gap alerting

An ingestion gap is defined as any period during which an expected log source fails to deliver data to the SIEM within its defined ingestion SLA. The following controls apply:

- Automated gap detection rules must be active for all critical log sources.
- Gap alerts are treated as P2 incidents until the gap is explained and resolved.
- Gaps exceeding 4 hours for critical sources are escalated to the CISO.
- Ingestion gap events are recorded in the incident register and reviewed at the weekly SOC operations meeting.

### 6.4 Predictive analytics and AI-assisted monitoring

Predictive analytics and AI-assisted monitoring tools may be used to improve detection accuracy, identify anomalous patterns, and reduce analyst workload. Applications include:

- AI-driven anomaly detection for compromised account behaviour (deviations from baseline authentication and access patterns).
- Automated alert enrichment with contextual threat intelligence.
- Behavioural scoring of user and entity activity to surface high-risk sessions for analyst review.

All AI-assisted detections must be reviewed by a human analyst before any containment or remediation action is initiated. Automated decisions must be explainable and logged for audit review, consistent with [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md) §9.

---

## 7. Threat hunting

### 7.1 Programme overview

Threat hunting is the proactive, hypothesis-driven search for threat actor activity that has evaded automated detection controls. Hunting is conducted within all environments under organisational control and is distinct from reactive alert-driven investigation.

The threat hunting programme operates on a quarterly cadence with targeted hunts triggered by specific intelligence inputs between scheduled cycles.

### 7.2 Hunt methodology

Threat hunts follow a hypothesis-driven approach:

1. **Hypothesis Formation:** Derived from recent threat intelligence, MITRE ATT&CK techniques not covered by existing detection rules, or anomalies surfaced by the SIEM or AI-assisted tools.
2. **Scope Definition:** Define the data sources, time range, and systems in scope for the hunt.
3. **Data Collection and Analysis:** Query SIEM, endpoint telemetry, network flow data, and identity logs. Apply analytics, statistical analysis, and pattern matching to surface anomalies.
4. **Finding Classification:** Classify findings as: Confirmed Threat, Suspicious Activity Requiring Investigation, False Positive / Benign Behaviour, or Detection Gap Identified.
5. **Output and Handoff:** Confirmed threats are escalated as security incidents per [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md). Detection gaps are submitted to the Detection Engineer for new rule development. False positive findings are used to refine existing rules.
6. **Documentation:** All hunt activities are documented in the hunt register, including hypothesis, methodology, data sources queried, findings, and disposition.

### 7.3 Quarterly hunt cadence

| Quarter | Focus Theme | Basis |
| --- | --- | --- |
| Q1 | Credential access and lateral movement | High-frequency ATT&CK techniques in sector threat landscape |
| Q2 | Persistence mechanisms and supply chain implants | ISAC intelligence and vendor advisories |
| Q3 | Data staging and exfiltration preparation | Internal telemetry anomalies and insider threat indicators |
| Q4 | Identity-based attacks and cloud platform misuse | Government advisories (CISA, CCCS, NCSC) and ATT&CK Cloud Matrix |

Hunt themes may be adjusted based on current threat intelligence and organisational priorities, subject to SOC Manager approval.

### 7.4 Hunt output feeding detection engineering

The threat hunting programme feeds directly into SIEM rule improvement:

- Each hunt must produce a list of detection rule recommendations or confirmations.
- New detection rules derived from hunt findings are prioritized for development within 30 days of the hunt conclusion.
- Hunt findings are reviewed at the monthly Threat Intelligence Review and the quarterly Security Governance Review.

---

## 8. Intelligence sharing and escalation

### 8.1 Intelligence sharing

The organisation participates in structured intelligence sharing to contribute to collective sector defence and to receive early warning of threats affecting the organisation's industry and geography.

| Sharing Programme | Description | Responsible Role | Frequency |
| --- | --- | --- | --- |
| **Sector ISAC Contribution** | Submission of validated, anonymized IoCs and TTP observations to relevant sector ISAC | Threat Intelligence Lead | Ongoing; minimum monthly submission |
| **Government Sharing (CISA, CCCS, NCSC)** | Participation in government-coordinated sharing programmes where available; submission of significant incident indicators as appropriate | CISO / Threat Intelligence Lead | As warranted by incident or advisory |
| **Peer Organization Sharing** | Bilateral sharing with peer organisations under executed information sharing agreements | CISO | Subject to active agreement |

All outbound intelligence sharing must comply with the Traffic Light Protocol (TLP). The default sharing classification for outbound indicators is TLP:AMBER unless explicitly approved at a higher level by the CISO.

### 8.2 Escalation: nation-state and APT threats

When threat intelligence or hunting activity indicates a likely nation-state actor or advanced persistent threat (APT) targeting the organisation, the following escalation steps apply:

1. **Immediate Notification:** Threat Intelligence Lead notifies the CISO within 1 hour of forming a credible hypothesis of nation-state or APT activity.
2. **CISO Assessment:** CISO convenes a brief assessment within 2 hours to evaluate the intelligence basis and determine whether a formal incident should be declared.
3. **Legal Counsel Engagement:** Legal Counsel is engaged immediately to assess disclosure obligations, litigation considerations, and potential law enforcement notification requirements.
4. **Government Advisory Bodies:** CISO coordinates with CISA, CCCS, or NCSC as appropriate, sharing indicators under applicable TLP classification with government coordination.
5. **External IR Partner:** CISO may engage the contracted external IR partner for additional forensic support.
6. **Executive Notification:** CIO is notified for all confirmed or credible nation-state incidents.

---

## 9. SIEM rule tuning

### 9.1 False positive management

Excessive false positives degrade analyst efficiency and risk alert fatigue, causing genuine threats to be missed. The following controls manage false positive rates:

1. **Immediate Tuning:** Any rule generating more than 10 false positives per analyst shift is reviewed within 48 hours of the pattern being identified.
2. **Tuning Actions:** May include: scope narrowing (exclude known-good IP ranges, user accounts, or processes), threshold adjustment, additional corroborating condition requirements, or rule suppression during defined maintenance windows.
3. **Approval:** Rule changes to reduce false positives follow the standard rule development and deployment workflow in §5.3. Emergency threshold adjustments may be approved verbally by the SOC Manager and documented within 4 hours.
4. **Documentation:** All tuning actions are recorded in the SIEM Alert Rule Register with: rule ID, change description, reason, approver, and effective date.

### 9.2 Bi-annual full rule review

The bi-annual SIEM Rule Review assesses the complete active rule library against the following criteria:

| Review Criterion | Acceptable Threshold | Action if Below Threshold |
| --- | --- | --- |
| Rule fired at least once in the past 6 months | All active rules | Review for relevance; retire if no longer applicable |
| False positive rate | < 10% of total alerts per rule | Tune or retire |
| MITRE ATT&CK mapping documented | 100% of rules | Update documentation or retire undocumented rules |
| Rule logic reviewed by a second analyst | 100% of rules | Conduct peer review before next review cycle |
| Associated data sources active and ingesting | 100% of rules | Disable rule if data source is absent |

Output of each bi-annual review is a Rule Review Report submitted to the CISO, documenting: total rules reviewed, rules retired, rules updated, new rules added since the last review, and coverage gap assessment.

---

## 10. Metrics

The following metrics are tracked and reported at the monthly SOC Operations Review and quarterly Security Governance Review:

| Metric | Definition | Target |
| --- | --- | --- |
| **TI Feed Coverage (%)** | Percentage of active threat intelligence source categories (OSINT, vendor, government, ISAC) with at least one active, validated feed | ≥ 90% |
| **Indicator Operationalization Rate (%)** | Percentage of high-confidence validated indicators operationalized into SIEM detection within 48 hours of validation | ≥ 85% |
| **New Detection Rules per Quarter** | Number of new or materially revised SIEM correlation rules deployed to production each quarter | Target: ≥ 5 net new rules per quarter |
| **MITRE ATT&CK Coverage (%)** | Percentage of defined priority ATT&CK tactics with at least one active, tested detection rule | ≥ 80% of priority tactics |
| **Threat Hunt Findings per Quarter** | Number of confirmed threats or significant detection gaps identified through threat hunting activities per quarter | Tracked; minimum 1 completed hunt per quarter |
| **False Positive Rate (%)** | Percentage of SIEM alerts determined to be false positives at Tier 1 triage | Target: < 20% overall; < 10% for Critical and High rules |
| **SIEM Ingestion Health (%)** | Percentage of critical data connectors with zero gap events in the reporting period | ≥ 99% |
| **Mean Time to Operationalize (MTTO)** | Average time from receipt of a new high-confidence IoC to active SIEM detection rule deployment | Target: ≤ 48 hours |

Metric trends are reviewed for continual improvement. Lessons learned from incidents and audits inform updates to rules, hunting hypotheses, and intelligence source selections, consistent with [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md) §10.

---

## 11. Framework alignment

| Control Area | Framework Reference |
| --- | --- |
| Threat intelligence programme | NIST SP 800-150; ISO/IEC 27001:2022 A.5.7; CSA CCM TVM domain (Threat and Vulnerability Management) controls |
| SIEM operations and monitoring | CSA CCM SEF-01 to SEF-10; NIST CSF Detect (DE.CM); ISO/IEC 27002:2022 §8.16 |
| Correlation rule development | MITRE ATT&CK Enterprise; NIST SP 800-53 SI-4; CSA CCM LOG-01 to LOG-14 |
| Threat hunting | MITRE ATT&CK; NIST CSF Detect (DE.AE); ISO/IEC 27002:2022 §8.16 |
| Intelligence sharing | NIST SP 800-150 §4; CSA CCM TVM domain controls covering intelligence sharing; CISA TLP Policy |
| Incident escalation | ISO/IEC 27035; NIST SP 800-61 Rev 3; CSA CCM SEF-04 to SEF-05 |
| Pre-go-live SIEM validation | [`operations/standard-production-security-requirements.md`](standard-production-security-requirements.md) §3.1 to §3.2 |
| AI-assisted detection | [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md) §9; NIST AI RMF |
| Records and audit | COBIT 2019 DSS05; ISO/IEC 27001:2022 A.5.28 |

---

*This document is released under the CC BY-SA 4.0 licence. To the extent possible under law, all copyright and related rights are waived. See [`LICENSE`](../LICENSE) in the repository root.*

---

**End of Document**
