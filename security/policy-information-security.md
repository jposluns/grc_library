# Information Security Policy

**Document Title:** Information Security Policy  
**Document Type:** Policy  
**Version:** 1.3.0  
**Date:** 2026-05-27  
**Owner:** Chief Information Security Officer  
**Approving Authority:** Governance Library Maintainer  
**Related Documents:** [`security/standard-logging-and-monitoring.md`](standard-logging-and-monitoring.md), [`security/policy-identity-and-access-management.md`](policy-identity-and-access-management.md), [`security/standard-data-classification-and-handling.md`](standard-data-classification-and-handling.md), [`governance/policy-governance-and-risk-management.md`](../governance/policy-governance-and-risk-management.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md)  
**Classification:** Public  
**Category:** Information Security  
**Review Frequency:** Annual and upon material threat, framework, or regulatory change  
**Repository Path:** [`security/policy-information-security.md`](policy-information-security.md)  
**Confidentiality:** Public  
**Licence:** CC0 1.0 Universal  

This policy establishes the overarching framework for protecting the confidentiality, integrity, and availability of information and systems. It merges and supersedes the Access Control Policy, Network Security Policy, Endpoint Security Policy, Vulnerability Management Policy, and Asset Management Policy into a unified Information Security Management System (ISMS) directive.

---

## Purpose

To ensure that information security is systematically managed, risks are mitigated through proportionate controls, and the organization maintains compliance with ISO/IEC 27001:2022, ISO/IEC 27002:2022, NIST Cybersecurity Framework 2.0, COBIT 2025, and CSA CCM v5.

---

## Scope

1. Applies to all business units, employees, contractors, and third parties who access, process, or store organizational or trade data, including personnel supporting BASC-certified logistics and customs operations in Latin America (Colombia, Mexico, Peru, Chile).
2. Covers all information assets including data, systems, networks, hardware, software, cloud environments, AI models, and mobile devices, as well as cargo, customs, and supply-chain systems governed by BASC International Standard v6.
3. Applies to all methods of access whether on-premises, remote, or hybrid, including cross-border data exchange between logistics facilities and customs authorities.
4. Includes all security controls necessary to maintain compliance with ISO/IEC 27001 Annex A, BASC trade-security requirements, and related frameworks.

---

## Governance and Accountability

**ISMS Ownership**
- The Chief Information Security Officer (CISO) is responsible for establishing, maintaining, and continually improving the ISMS.
- The Chief Information Officer (CIO) provides strategic alignment and ensures resourcing.
- An Enterprise Risk Committee reviews risk posture and control effectiveness quarterly.

**Information Security Management System (ISMS)**
- The ISMS shall operate in accordance with ISO/IEC 27001:2022 Clauses 4–10 and Annex A.
- Control ownership shall be assigned for each ISO/IEC 27002 control family and CSA CCM domain.

**Roles and Responsibilities**

| Role | Responsibility |
| --- | --- |
| CISO | Defines and enforces security strategy, policies, and controls. Oversees risk assessments, vulnerability management, and incident response. |
| CIO | Ensures security objectives align with business goals. Oversees infrastructure, architecture, and compliance integration. |
| Security Operations Team | Implements and monitors preventive, detective, and corrective controls. Operates SIEM, vulnerability scanners, and endpoint protection. |
| System and Application Owners | Maintain asset inventories, apply security baselines, and validate access rights. |
| Network and Cloud Engineers | Configure, monitor, and protect network and cloud infrastructure per NIST CSF 2.0 Protect and Detect functions. |
| Employees and Contractors | Adhere to acceptable use and data protection requirements; promptly report incidents or policy violations. |
| Internal Audit | Evaluates ISMS effectiveness and verifies compliance with ISO/IEC 27001. |

**BASC Compliance Oversight**
- Regional BASC Compliance Officers oversee implementation of BASC International Standard (v6 2023) controls across trade, logistics, and customs environments in Latin America.
- BASC audit findings and corrective actions are tracked in the Continuous Improvement Register and reported to the Enterprise Risk Committee quarterly.

---

## Policy Statements

### 1. Information Security Framework

1.1 The organization shall maintain an ISMS aligned to ISO/IEC 27001:2022 Clauses 4–10 and Annex A.
1.2 The ISMS shall integrate risk management, business continuity, privacy, and AI governance.
1.3 Security objectives shall be measurable and reviewed annually.

### 2. Asset Management

2.1 All information assets shall be inventoried and classified by confidentiality, integrity, and availability impact.
2.2 Owners shall be assigned to each asset and responsible for protection throughout its lifecycle.
2.3 Unauthorized assets shall be removed from the network and reported to the CISO.

### 3. Access Control and Identity Management

3.1 Access shall follow the principle of least privilege and be granted based on approved business need.
3.2 All privileged accounts shall use multi-factor authentication.
3.3 Role-based access controls shall be defined and periodically reviewed for accuracy.
3.4 Access revocation must occur within 24 hours of employee termination or role change.

### 4. Network and Infrastructure Security

4.1 The network shall be segmented according to sensitivity, criticality, and regulatory or trade-compliance requirements, including BASC logistics-network segregation between operational, administrative, and customs zones.
4.2 Firewalls, intrusion prevention systems, and secure gateways shall be configured, monitored, and updated regularly.
4.3 Cloud environments shall implement shared responsibility models and continuous monitoring aligned to CSA CCM IVS controls and BASC International Standard Section 6.
4.4 All network traffic, including cargo, customs, and trade data, shall be logged and retained per the Logging and Monitoring Standard and BASC record keeping obligations.

### 5. Endpoint and Mobile Security

5.1 All endpoints shall have up-to-date antivirus, endpoint detection, and response capabilities.
5.2 Device encryption shall be enforced for all laptops, tablets, and mobile devices storing organizational data.
5.3 Removable media shall be restricted and encrypted when use is approved.

### 6. Vulnerability and Patch Management

6.1 Vulnerability scans shall occur at least monthly for all systems and after any major change.
6.2 Critical vulnerabilities must be remediated within seven days; high within fourteen days.
6.3 Patch deployment shall be automated where possible and tracked for compliance metrics.

### 7. Information Handling and Data Protection

7.1 Data classification and labelling shall follow the Data Classification Standard, assigning all trade and customs data a minimum classification of Restricted under BASC Section 6.
7.2 Data at rest and in transit shall be encrypted using approved algorithms (AES-256 or stronger), including BASC-required PKI validation for customs and cargo data transmissions.
7.3 Backups shall be performed daily, tested quarterly, and stored securely in geographically diverse locations, with BASC-governed trade and customs data stored only in BASC-approved or validated facilities.

### 8. AI Model and System Security

8.1 AI systems and models shall be protected against unauthorized access, modification, or data poisoning.
8.2 Model artifacts shall be version-controlled, integrity-checked, and logged.
8.3 Validation and verification procedures shall be implemented to ensure accuracy, fairness, and reproducibility.
8.4 AI model risk metrics shall align with NIST CSF 2.0 and AI RMF 1.1.

### 9. Incident Response and Reporting

9.1 All suspected or confirmed information security incidents, including trade and customs data breaches or BASC control failures, must be reported immediately to the security operations team and the Regional BASC Compliance Officer.
9.2 Incident response shall follow the NIST 800-61 framework, COBIT DSS02, and BASC incident-handling procedures aligned to WCO SAFE.
9.3 Root cause analysis and lessons learned must be completed within ten business days of incident closure.

### 10. Monitoring and Continuous Improvement

10.1 The ISMS shall be continuously monitored through defined metrics (mean time to detect, vulnerability closure rate, compliance posture).
10.2 The ISMS shall be audited annually for ISO/IEC 27001 compliance.
10.3 Corrective actions shall be documented, tracked, and verified by Internal Audit.

---

## Framework Alignment

| Control Area | ISO/IEC 27001 | ISO/IEC 27002 | NIST CSF 2.0 | COBIT 2025 | CSA CCM v5 |
| --- | --- | --- | --- | --- | --- |
| Governance and ISMS | Clauses 4–10 | A.5 | Identify, Protect | DSS01.01 | ISM-01 |
| Asset Management | A.5.9–A.5.11 | 8.1–8.3 | Identify | DSS01.02 | ISM-02 |
| Access Control | A.5.15–A.5.20 | 9.1–9.4 | Protect | DSS05 | IAM-01–09 |
| Network and Cloud Security | A.5.21–A.5.23 | 10.1–10.5 | Protect, Detect | DSS01, DSS04 | IVS-01–10 |
| Vulnerability and Patch | A.8.8, A.8.9 | 12.1–12.6 | Detect, Respond | DSS05 | ISM-04 |
| Incident Management | A.5.24 | 16.1–16.3 | Respond, Recover | DSS02 | ISM-05 |
| AI Model Security | A.8 (emerging) | — | Protect, Detect | DSS01.06 | ISM-10 |
| Continuous Improvement | Clause 10 | 18.1 | Recover | MEA01 | ISM-12 |

**Additional alignments:** BASC International Standard (v6 2023); WCO SAFE Framework (2021); ISO 28000:2022; PIPEDA; AIDA.



**End of Document**
