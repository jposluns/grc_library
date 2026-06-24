# Information Security Policy

**Document Title:** Information Security Policy\
**Document Type:** Policy\
**Version:** 1.3.4\
**Date:** 2026-06-24\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/standard-logging-and-monitoring.md`](standard-logging-and-monitoring.md), [`security/policy-identity-and-access-management.md`](policy-identity-and-access-management.md), [`security/standard-data-classification-and-handling.md`](standard-data-classification-and-handling.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material threat, framework, or regulatory change\
**Repository Path:** [`security/policy-information-security.md`](policy-information-security.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

This policy establishes the overarching framework for protecting the confidentiality, integrity, and availability of information and systems. It merges and supersedes the Access Control Policy, Network Security Policy, Endpoint Security Policy, Vulnerability Management Policy, and Asset Management Policy into a unified Information Security Management System (ISMS) directive.

---

## Purpose

To ensure that information security is systematically managed, risks are mitigated through proportionate controls, and the organisation maintains compliance with ISO/IEC 27001:2022, ISO/IEC 27002:2022, NIST CSF 2.0, COBIT 2019, and CSA CCM v4.1.

---

## Scope

1. Applies to all business units, employees, contractors, and third parties who access, process, or store organisational data.
2. Covers all information assets including data, systems, networks, hardware, software, cloud environments, AI models, and mobile devices.
3. Applies to all methods of access whether on-premises, remote, or hybrid, including cross-border data exchange.
4. Includes all security controls necessary to maintain compliance with ISO/IEC 27001 Annex A and related frameworks.

Sector-specific overlays (for example, BASC-certified trade and logistics operations) apply where the organisation participates in a programme covered by a sector annex; see [`compliance/`](../compliance/).

---

## Governance and accountability

**ISMS Ownership**
- The Chief Information Security Officer (CISO) is responsible for establishing, maintaining, and continually improving the ISMS.
- The Chief Information Officer (CIO) provides strategic alignment and ensures that resourcing.
- An Enterprise Risk Committee reviews risk posture and control effectiveness quarterly.

**Information Security Management System (ISMS)**
- The ISMS shall operate in accordance with ISO/IEC 27001:2022 Clauses 4 to 10 and Annex A.
- Control ownership shall be assigned for each ISO/IEC 27002 control family and CSA CCM domain.

**Roles and Responsibilities**

| Role | Responsibility |
| --- | --- |
| CISO | Defines and enforces security strategy, policies, and controls. Oversees risk assessments, vulnerability management, and incident response. |
| CIO | Ensures that security objectives align with business goals. Oversees infrastructure, architecture, and compliance integration. |
| Security Operations Team | Implements and monitors preventive, detective, and corrective controls. Operates SIEM, vulnerability scanners, and endpoint protection. |
| System and Application Owners | Maintain asset inventories, apply security baselines, and validate access rights. |
| Network and Cloud Engineers | Configure, monitor, and protect network and cloud infrastructure per NIST CSF 2.0 Protect and Detect functions. |
| Employees and Contractors | Adhere to acceptable use and data protection requirements; promptly report incidents or policy violations. |
| Internal Audit | Evaluates ISMS effectiveness and verifies compliance with ISO/IEC 27001. |

Where the organisation participates in a sector-specific security programme (for example, BASC for trade and logistics operations), the corresponding sector annex defines additional oversight roles and reporting cadences. See [`compliance/`](../compliance/).

---

## Policy statements

### 1. Information security framework

1.1 The organisation shall maintain an ISMS aligned to ISO/IEC 27001:2022 Clauses 4 to 10 and Annex A.
1.2 The ISMS shall integrate risk management, business continuity, privacy, and AI governance.
1.3 Security objectives shall be measurable and reviewed annually.

### 2. Asset management

2.1 All information assets shall be inventoried and classified by confidentiality, integrity, and availability impact.
2.2 Owners shall be assigned to each asset and responsible for protection throughout its lifecycle.
2.3 Unauthorized assets shall be removed from the network and reported to the CISO.

### 3. Access control and identity management

3.1 Access shall follow the principle of least privilege and be granted based on approved business need.
3.2 All privileged accounts shall use multi-factor authentication.
3.3 Role-based access controls shall be defined and periodically reviewed for accuracy.
3.4 Access revocation must occur within 24 hours of employee termination or role change.

### 4. Network and infrastructure security

4.1 The network shall be segmented according to sensitivity, criticality, and regulatory requirements.
4.2 Firewalls, intrusion prevention systems, and secure gateways shall be configured, monitored, and updated regularly.
4.3 Cloud environments shall implement shared responsibility models and continuous monitoring aligned to CSA CCM IVS controls.
4.4 All network traffic shall be logged and retained per the Logging and Monitoring Standard.

### 5. Endpoint and mobile security

5.1 All endpoints shall have up-to-date antivirus, endpoint detection, and response capabilities.
5.2 Device encryption shall be enforced for all laptops, tablets, and mobile devices storing organisational data.
5.3 Removable media shall be restricted and encrypted when use is approved.

### 6. Vulnerability and patch management

6.1 Vulnerability scans shall occur at least monthly for all systems and after any major change.
6.2 Critical vulnerabilities must be remediated within seven days; high within fourteen days.
6.3 Patch deployment shall be automated where possible and tracked for compliance metrics.

### 7. Information handling and data protection

7.1 Data classification and labelling shall follow the Data Classification Standard.
7.2 Data at rest and in transit shall be encrypted using approved algorithms (AES-256 or stronger).
7.3 Backups shall be performed daily, tested quarterly, and stored securely in geographically diverse locations.

### 8. AI model and system security

8.1 AI systems and models shall be protected against unauthorized access, modification, or data poisoning.
8.2 Model artifacts shall be version-controlled, integrity-checked, and logged.
8.3 Validation and verification procedures shall be implemented to ensure that accuracy, fairness, and reproducibility.
8.4 AI model risk metrics shall align with NIST CSF 2.0 and NIST AI RMF 1.0 (with the AI 600-1 Generative AI Profile).

### 9. Incident response and reporting

9.1 All suspected or confirmed information security incidents must be reported immediately to the security operations team.
9.2 Incident response shall follow the NIST SP 800-61 Rev. 3 framework (Incident Response Recommendations and Considerations for Cybersecurity Risk Management, 2025) and COBIT DSS02.
9.3 Root cause analysis and lessons learned must be completed within ten business days of incident closure.

### 10. Monitoring and continuous improvement

10.1 The ISMS shall be continuously monitored through defined metrics (mean time to detect, vulnerability closure rate, compliance posture).
10.2 The ISMS shall be audited annually for ISO/IEC 27001 compliance.
10.3 Corrective actions shall be documented, tracked, and verified by Internal Audit.

---

## Framework alignment

| Control Area | ISO/IEC 27001:2022 | ISO/IEC 27002:2022 | NIST CSF 2.0 | COBIT 2019 | CSA CCM v4.1 |
| --- | --- | --- | --- | --- | --- |
| Governance and ISMS | Clauses 4 to 10 | 5.1, 5.2 (policies and roles) | Identify, Protect | DSS01.01 | ISM-01 |
| Asset Management | A.5.9 to A.5.11 | 5.9 to 5.14 | Identify | DSS01.02 | ISM-02 |
| Access Control | A.5.15 to A.5.20 | 5.15 to 5.18; 8.2 to 8.5 | Protect | DSS05 | IAM-01 to 09 |
| Network and Cloud Security | A.5.21 to A.5.23 | 5.14 (information transfer); 8.20 to 8.24 (network security and cryptography) | Protect, Detect | DSS01, DSS04 | I&S-01 to 10 |
| Vulnerability and Patch | A.8.8, A.8.9 | 8.8 (technical vulnerabilities); 8.9 (configuration management) | Detect, Respond | DSS05 | ISM-04 |
| Incident Management | A.5.24 | 5.24 to 5.30; 6.8 (event reporting) | Respond, Recover | DSS02 | ISM-05 |
| AI Model Security | A.8 (emerging) | N/A | Protect, Detect | DSS01.06 | ISM-10 |
| Continuous Improvement | Clause 10 | 5.31 to 5.37 (compliance and review); ISMS continuous improvement is in 27001 Clause 10 | Recover | MEA01 | ISM-12 |

Note: ISO/IEC 27002:2022 reorganised the previous 2013 edition's 14 control clauses (5-18) into four themes covering 93 controls (clause 5 Organisational, 6 People, 7 Physical, 8 Technological). Citations elsewhere in the corpus that use 2013-style chapter numbers (9 to 18) refer to the superseded edition.

**Additional alignments:** ISO 28000:2022; PIPEDA; AIDA. Sector-specific overlays including BASC International Standard (v6 2023) and WCO SAFE Framework (2021) apply where the organisation participates in those programmes; see [`compliance/`](../compliance/).



**End of Document**
