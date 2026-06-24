# Security Baseline and Standards Reference

**Document Title:** Security Baseline and Standards Reference\
**Document Type:** Standard\
**Version:** 1.1.2\
**Date:** 2026-06-24\
**Owner:** Chief Information Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`dev-security/standard-developer-security-requirements.md`](standard-developer-security-requirements.md), [`dev-security/standard-devops-security-requirements.md`](standard-devops-security-requirements.md), [`dev-security/standard-security-quick-reference.md`](standard-security-quick-reference.md), [`security/policy-information-security.md`](../security/policy-information-security.md), [`governance/charter-governance-library.md`](../governance/charter-governance-library.md)\
**Classification:** Public\
**Category:** Developer Security\
**Review Frequency:** Annual or upon material threat, regulatory, or framework change\
**Repository Path:** [`dev-security/standard-security-baseline-and-standards-reference.md`](standard-security-baseline-and-standards-reference.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose and scope

This document establishes the security framework, governing principles, data classification model, identity architecture, and network security model applicable to all computing environments, development programmes, and activities within an organisation's security boundary. It applies to all cloud environments, all internal and outsourced development, and all personnel, contractors, and service providers with access to organisational systems, data, or code repositories.

All requirements in the developer security requirements, DevOps security requirements, and production security requirements standards flow from this document. When this document conflicts with any subordinate standard, this document takes precedence.

---

## 1. Governing framework hierarchy

In the event of conflict, higher layers take precedence.

### Layer 1: statute and regulation

| Obligation | Jurisdiction | Relevance |
| --- | --- | --- |
| PIPEDA / Bill C-27 / Quebec Law 25 | Canada | Personal data processing, breach notification, data residency |
| Canada Artificial Intelligence and Data Act (AIDA) | Canada | AI system governance, high-impact AI risk classification |
| Criminal Code of Canada (cybercrime provisions) | Canada | Unauthorized access, data destruction |
| State and provincial breach notification laws | Multiple | Customer and partner data exposure |
| GDPR (Article 3 extraterritorial scope) | EU | Where EU data subjects are processed |
| BASC International Standard | Latin America / Global | Customs and trade security for Latin American operations |
| WCO SAFE Framework | Global | Customs data integrity and trade security |
| CTPAT | USA | Cross-border trade security |

### Layer 2: primary security frameworks

| Framework | Version | Role |
| --- | --- | --- |
| CSA Cloud Controls Matrix (CCM) | v4.1.0 | Primary cloud security control framework. 207 controls across 17 domains. |
| CSA AI Controls Matrix (AICM) | v1.0.3 | AI-specific controls. Mandatory for all AI/ML workloads. |
| COBIT | 2019 | IT governance framework. Process-level traceability for audit and board reporting. |
| ISO/IEC 27001:2022 | 2022 | Information Security Management System (ISMS). |
| ISO/IEC 27002:2022 | 2022 | Security controls implementation guidance. |
| NIST SSDF | SP 800-218 and SP 800-218A (Generative AI Profile) | Secure-by-design development. Mandatory for all net-new development. SP 800-218A applies to all AI and ML workloads. |
| OWASP ASVS | v5.0.0 | Application security testing baseline. |

### Layer 3: internal governance documents

The governance library includes authoritative artefacts in the following areas: information security policy; secure development and engineering policy; acceptance into service policy; identity and access management policy; privileged access management standard; authentication and password management standard; encryption and key management policy; privacy and data governance policy; network security and segmentation standard; logging and monitoring standard; physical security of IT infrastructure standard; remote working security standard; penetration testing and red team programme standard; bring-your-own-device policy; media handling and transport procedure; cloud exit and data portability standard; change management procedure; vulnerability management procedure; incident response procedure; AI compliance policy; AI governance and ethics framework; AI security and risk standard; post-quantum cryptography readiness roadmap.

### Layer 4: architectural standards

Current architectural authority documents define infrastructure delivery standards, network design, and approved tooling. Adopting organisations should maintain a current-state register of approved platforms, tooling, and vendor assignments.

---

## 2. Core security principles

Deviations require a formal exception approved by the CIO or CISO.

| Principle | Statement |
| --- | --- |
| **Secure by Design** | Security controls are built in from the first design decision. Not added after build. |
| **Zero Standing Privilege** | No person or service account holds permanently elevated access. All privileged access is time-bound, approved, and recorded. |
| **Least Privilege** | Every identity receives only the permissions required to perform its defined function. |
| **Default Deny** | All access, network flows, and service-to-service communication is denied by default. Only explicitly approved flows are permitted. |
| **Separation of Environments** | Production, Test, and Dev are distinct environments with dedicated identity domains, network segments, and access controls. No shared credentials or paths between them. |
| **Immutable and Auditable** | All significant actions generate audit records that cannot be deleted by the actor. Logs are forwarded to the SIEM immediately. Backup repositories use immutable (WORM) storage. |
| **Data Residency First** | All data is hosted in primary cloud regions by default. Non-default hosting requires a risk assessment, CIO/Legal approval, and privacy impact assessment where personal data is involved. |
| **Encryption Everywhere** | Data at rest, in transit, and in use is encrypted. TLS 1.3 (or stronger). RC4, 3DES, SSL, TLS 1.0/1.1/1.2 prohibited. AES-256 for symmetric encryption. NTLMv1 prohibited. |
| **Supply Chain Integrity** | All third-party code, libraries, models, and services are evaluated before use. Software Bill of Materials (SBOM) maintained for all applications. |
| **Privacy by Design** | Personal data processing is minimized and purposeful. Privacy Impact Assessments (PIAs) completed before any new system processing personal data is deployed. |

---

## 3. Data classification

| Classification | Description | Examples |
| --- | --- | --- |
| **Public** | Approved for unrestricted external disclosure. | Marketing materials, public website content |
| **Controlled** | May be shared externally on demand where disclosure poses low risk. | Product overviews, proposals, general client communications |
| **Internal** | For organisational internal use only. | Operational procedures, internal reports |
| **Confidential** | Sensitive business data requiring controlled access. | Customer records, financial data, contracts, trade data, personnel information |
| **Restricted** | Highest sensitivity; access strictly controlled. | Credentials, encryption keys, audit logs with PII, investigation materials |

Always classified as Confidential or Restricted regardless of context: personal identifiable information (PII); payment data; customs declarations; salary and HR data; credentials and API keys; architecture diagrams containing security controls; incident response documentation; AI training datasets containing personal data.

---

## 4. Regulatory obligations

### 4.1 Canadian privacy law

Quebec Law 25 requires: PIA before any technology deployment involving personal information; data residency justification for storage outside Quebec; breach notification to the provincial privacy regulator within 72 hours of a high-risk breach; designated privacy officer. See the privacy management programme charter for the full privacy governance model.

### 4.2 Trade security compliance (BASC)

BASC International Standard requires: documented access controls to logistics and trade systems; protection of customs and shipment data; supply chain integrity controls; incident response and reporting for trade operations. IT responsibilities should be mapped in a dedicated compliance register.

### 4.3 Trusted-trader programmes (CTPAT and equivalents)

Requirements include: documented cybersecurity programme; password and access control standards; periodic security assessments; and business partner vetting. Refer to the authentication and password management standard and the penetration testing programme standard.

### 4.4 AI regulation

Canada's AIDA requires: risk classification of AI systems; algorithmic impact assessments before deployment; transparency and explainability; retention of compliance records. Treat as near-term compliance target. Refer to the AI and agentic development security standard for AI security requirements.

---

## 5. Cloud hosting policy

**Default:** Primary cloud region designated by the organisation.

**Non-default hosting process:** Initiate data residency risk assessment; Legal and Compliance review; PIA where personal data is involved; written CIO approval with Legal sign-off; recorded in Exception Register; reviewed annually.

**Multi-cloud:** Multiple cloud platforms may be approved for specific workloads. All multi-cloud workloads must comply with this security baseline and be included in SIEM monitoring.

**AI service residency:** Some AI services may not be available in preferred cloud regions. Any project using such a service must complete the non-default hosting exception process before deployment. Adopting organisations should identify approved fallback services for workloads with contractual data residency requirements.

**Cloud exit:** All cloud services must have a documented exit plan per the cloud exit and data portability standard.

---

## 6. Identity and access architecture

### 6.1 Identity authority

An enterprise identity provider (IdP) serves as the authoritative identity authority for all environments. On-premises identity domains should be separate security boundaries from resource domains. Administrative access must not cross trust boundaries.

### 6.2 Authentication standards

Multi-factor authentication (MFA) is mandatory for all human access without exception. Phishing-resistant MFA (e.g., FIDO2 or certificate-based) is required for Tier 0 access. Service accounts use platform managed identities or PAM-vaulted accounts. LDAPS (port 636) is the only permitted directory integration protocol. Kerberos AES-256 is required; RC4 Kerberos is prohibited in all new builds.

### 6.3 Privileged access management

Just-in-time privileged access, approval workflows, and audit trails must be implemented for all privileged access. PAM tiers:

| Tier | Assets | Controls |
| --- | --- | --- |
| **Tier 0** | Domain Controllers, PKI, PAM, identity services | Privileged access workstation (PAW) only. Approval mandatory. Session recording mandatory. Rotate every checkout, max 24 hours. |
| **Tier 1** | Hypervisor, storage, backup, virtualization infrastructure | No Tier 0 access. MFA and session recording mandatory. Rotate every 24 to 48 hours. |
| **Tier 2** | Application and database servers | No Tier 0/1 access unless explicitly approved. MFA mandatory. Rotate every 7 days. |

### 6.4 Service identities

Service identities must be named per approved convention, hold minimum required permissions, be registered in the PAM vault or managed identity registry, and be reviewed quarterly. No service identity may hold standing domain administrator membership. Cloud workloads should use platform managed identity for all service-to-service authentication wherever technically feasible.

---

## 7. Network security architecture

All inter-segment communication is default-deny. Production, Test, and Dev are fully segregated with separate identity domains, network segments, and access controls. Storage segments are non-routable. Database segments have no outbound internet access. DMZ systems cannot initiate connections to database, storage, or backup segments. All administrative access is from a privileged access workstation (PAW) or approved jump host only. Perimeter controls include a cloud-based web application firewall (WAF) and next-generation firewalls enforcing north-south traffic policy.

Applications must document required network flows before deployment. No access control list (ACL) or firewall change is permitted without a documented, approved change request.

---

## 8. Logging and monitoring

Logging is mandatory and is not a post-deployment activity. A SIEM is the primary platform for log aggregation and alerting across Production and Test environments. All systems must forward logs to the SIEM.

### Minimum log retention

| Environment | Hot Retention | Archive |
| --- | --- | --- |
| Production / Test | 90 days | 12 months |
| Dev | 30 days | N/A |
| Security logs | 12 months minimum | 24 months recommended |

### Required log sources: all systems

Authentication events; privileged access events; administrative actions; network boundary events; application errors and security exceptions; backup events; certificate lifecycle events.

### Applications additionally log

All authentication attempts; all authorization decisions; all Confidential/Restricted data access events; all API calls with caller, endpoint, response code, and timestamp; significant configuration changes.

### Log integrity

Logs must not be modifiable by the actor that generated them. SIEM workspace deletion is restricted to break-glass roles only.

---

## 9. Incident response obligations

- Report any suspected incident immediately to the security team. No silent remediation.
- Preserve evidence. Do not reimage, restart, or modify affected systems without IR team instruction.
- A designated SOC/IR partner or internal incident response capability should be engaged by the CIO/CISO for Priority 1 incidents.
- Regulatory breach notification under PIPEDA and Quebec Law 25 is time-critical. 72 hours for high-risk breaches under Quebec Law 25. CIO must be notified immediately on any suspected breach involving personal data.

---

## 10. Framework and runtime end-of-life policy

Running application frameworks, language runtimes, or middleware that have reached vendor End-of-Life (EOL) is a security risk. EOL runtimes do not receive security patches. CVEs identified after the EOL date will remain unmitigated permanently. This policy applies to all runtimes including .NET, Node.js, Java, Python, OS versions, database engines, and on-premises middleware.

### EOL classification and remediation SLA

| Class | Definition | Remediation SLA | Interim Controls |
| --- | --- | --- | --- |
| **Class 1: Critical** | Runtime EOL for more than 12 months AND a CVE rated CVSS 7.0 or above published against it since EOL | 30 days. No extension without CIO approval and documented compensating controls. | Network isolation where feasible; enhanced monitoring; no new features on the affected service. |
| **Class 2: High** | Runtime EOL date has passed with no qualifying CVE yet, OR runtime reaches EOL within 90 days | 90 days for already-EOL. Upgrade initiated before EOL date for imminent EOL. | Upgrade plan documented and tracked. Interim monitoring in place. |
| **Class 3: Medium** | Runtime reaches EOL within 180 days | Upgrade plan must exist before the 90-day threshold is reached. | Planning and procurement only. |

### EOL tracking and enforcement

A runtime EOL tracking register is maintained by the DevOps lead and reviewed quarterly. SIEM alerts fire at 180 days, 90 days, and 30 days before any runtime reaches EOL. Cloud governance policy should block deployment to EOL runtime versions at the subscription or organisational level. Policy exceptions require a documented waiver with a maximum 30-day duration and CIO approval.

---

## Framework alignment

| Control Area | ISO 27001/27002 | CSA CCM v4.1 | NIST SP 800-218 | OWASP ASVS | Regulatory |
| --- | --- | --- | --- | --- | --- |
| Security governance and principles | A.5 | GRC-01 to 06 | PW.1 to PW.4 | N/A | ISO 37301, COBIT |
| Data classification | A.5.10 to 5.13 | DSP-01 to 07 | N/A | V9 | PIPEDA, Law 25, GDPR |
| Identity and access | A.5.15 to 5.18 | IAM-01 to 14 | N/A | V2, V4 | PIPEDA, BASC |
| Network security | A.8.20 to 8.23 | I&S-03, I&S-08, I&S-09 | N/A | V9 | CTPAT |
| Logging and monitoring | A.8.15 to 8.16 | LOG-01 to 13 | RV.1 to RV.2 | V7 | Quebec Law 25 |
| Cryptography | A.8.24 to 8.25 | CEK-01 to 21 | N/A | V6 | FIPS 140-3 guidance |
| Incident response | A.5.26 | SEF-01 to 06 | RS.1 to RS.2 | N/A | PIPEDA, Law 25 |
| Supplier and third-party | A.5.19 to 5.22 | STA-01 to 09 | N/A |: | CTPAT, BASC, WCO SAFE |
| EOL and vulnerability management | A.8.8 | TVM-01 to 10 | PW.4.4 | N/A | BASC |

---

**End of Document**
