# Secure Development and Engineering Policy

**Document Title:** Secure Development and Engineering Policy\
**Document Type:** Policy\
**Version:** 1.0.10\
**Date:** 2026-07-23\
**Owner:** Chief Information Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md), [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](standard-software-evaluation-acceptance-and-lifecycle.md), [`dev-security/standard-quality-assurance-and-testing.md`](standard-quality-assurance-and-testing.md), [`security/policy-acceptance-into-service.md`](../security/policy-acceptance-into-service.md), [`ai/framework-ai-governance-and-risk.md`](../ai/framework-ai-governance-and-risk.md), [`operations/procedure-patch-management.md`](../operations/procedure-patch-management.md)\
**Classification:** Public\
**Category:** Developer Security\
**Review Frequency:** Annual and upon material framework or regulatory change\
**Repository Path:** [`dev-security/policy-secure-development-and-engineering.md`](policy-secure-development-and-engineering.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This policy establishes mandatory requirements for secure software development, engineering practices, and lifecycle management across all applications, systems, and code repositories.

It merges and replaces the Secure Software Development Lifecycle (SDLC) Policy, Code Management Policy, Open-Source Policy, Testing Standard, and Peer-Review Guideline into a unified framework for secure design, development, testing, and maintenance.

The policy aligns with ISO/IEC 27034 Application Security, ISO/IEC 27002:2022 controls, NIST Secure Software Development Framework (SSDF), COBIT 2019 BAI03 and BAI07, CSA CCM v4.1 SEF domain, and OWASP ASVS v5.

It incorporates forward-looking controls for AI-generated code verification and ISO/IEC 27002 clause 5 AI security control mapping.

---

## 2. Scope

1. Applies to all software, scripts, infrastructure-as-code, AI models, APIs, and automation developed, maintained, or integrated by the organization.
2. Covers both internal and outsourced development, including open-source and third-party components.
3. Applies to all personnel involved in software design, coding, testing, deployment, and maintenance.
4. Encompasses both traditional and AI-assisted development environments.

---

## 3. Governance and accountability

### 3.1 Executive oversight

1. The Chief Information Officer (CIO) is accountable for secure development governance and ensuring integration with enterprise risk management.
2. The Chief Information Security Officer (CISO) enforces application security controls and maintains the secure SDLC framework.
3. The Software Engineering and Security Architecture teams jointly manage design assurance, security testing, and peer review programmes.
4. The Enterprise Risk Committee (ERC) receives quarterly reports on development security posture, vulnerabilities, and audit findings.

### 3.2 Roles and responsibilities

| Role | Responsibility |
| --- | --- |
| **CISO** | Defines secure coding standards, oversees vulnerability remediation, and enforces compliance with NIST SSDF and ISO 27034. |
| **CIO** | Oversees policy enforcement and ensures that secure design principles are embedded across all engineering teams. |
| **Development Team Leads** | Implement secure SDLC controls, manage peer review workflows, and track remediation timelines. |
| **Developers / Engineers** | Follow approved secure coding practices, maintain code integrity, and complete annual secure coding training. |
| **QA and Testing Teams** | Conduct security testing, validate vulnerabilities, and confirm code meets ASVS v5 assurance levels. |
| **AI Development Teams** | Verify accuracy and security of AI-generated code through human-in-the-loop review and static analysis. |
| **Internal Audit** | Validates adherence to this policy and secure development metrics within COBIT BAI03 and MEA01 frameworks. |

---

## 4. Policy statements

### 4.1 Secure development lifecycle (SDLC)

4.1.1 All applications must follow a defined SDLC that incorporates security checkpoints at each phase: planning, design, development, testing, deployment, and maintenance.

4.1.2 Security requirements must be defined at the design stage and traceable through release and deployment.

4.1.3 Project plans must include threat modelling, risk assessments, and secure design reviews. The organization's threat-modelling methodology, including the STRIDE-per-trust-boundary analysis, the abuse-case-alongside-use-case authoring, and the Mandatory / Approval-Gated / Prohibited disposition tiers, is defined in [`security/standard-threat-modelling.md`](../security/standard-threat-modelling.md).

### 4.2 Code management and version control

4.2.1 All source code must reside in approved version control repositories with enforced access controls and audit logging.

4.2.2 Commits and merges must require multi-person review and automated validation.

4.2.3 Code branching strategies must separate development, testing, and production releases with automated build validation pipelines.

### 4.3 Secure coding practices

4.3.1 Developers must follow OWASP ASVS v5 and language-specific secure coding standards.

4.3.2 Code must be free of hardcoded secrets, credentials, or API keys.

4.3.3 All cryptographic implementations must use approved libraries and comply with ISO/IEC 19790 FIPS 140-3 standards.

4.3.4 Input validation, output encoding, and proper error handling must be enforced for all applications.

### 4.4 AI-generated code governance

4.4.1 AI-assisted code generation tools must be approved and monitored by the CISO.

4.4.2 All AI-generated code must undergo static and dynamic security scanning before integration.

4.4.3 Human review and sign-off are mandatory for any AI-generated code merged into production repositories.

4.4.4 AI-generated libraries or logic blocks must be tagged for traceability and be auditable within code repositories.

### 4.5 Open-source and third-party component management

4.5.1 Open-source libraries must be vetted using approved dependency scanning tools.

4.5.2 Only components with permissive and compatible licenses (e.g., MIT, Apache 2.0) may be used.

4.5.3 Vulnerable components must be patched or replaced within the severity-based remediation SLAs in [`../security/procedure-vulnerability-management.md`](../security/procedure-vulnerability-management.md) section 2 (the single source of truth).

4.5.4 A Software Bill of Materials (SBOM) must be maintained for all applications per NIST Executive Order 14028 guidance.

### 4.6 Testing and validation

4.6.1 Static Application Security Testing (SAST), Dynamic Application Security Testing (DAST), and Software Composition Analysis (SCA) are mandatory for all releases.

4.6.2 Penetration testing must occur annually or after major updates.

4.6.3 Unit, integration, and acceptance testing must include security criteria and pass/fail thresholds.

4.6.4 Test evidence and reports must be stored in the quality assurance repository for audit review.

### 4.7 Peer review and approval

4.7.1 All code changes must be peer-reviewed by at least one qualified developer and one security reviewer.

4.7.2 Peer reviews must verify functionality, maintainability, and adherence to secure coding standards.

4.7.3 Review comments and approvals must be logged within the version control platform.

### 4.8 Continuous integration and deployment (CI/CD)

4.8.1 CI/CD pipelines must include automated security scanning, dependency checks, and signature validation.

4.8.2 Deployment pipelines must require approval gates based on test results and risk severity levels.

4.8.3 Build environments must be isolated and signed artefacts must be validated before release.

### 4.9 Secure configuration and environment management

4.9.1 Development environments must mirror production security configurations where feasible.

4.9.2 Configuration baselines and infrastructure-as-code templates must be stored in controlled repositories.

4.9.3 Secrets and credentials must be stored in approved secrets management systems with role-based access.

### 4.10 Continual improvement and metrics

4.10.1 Development teams must track metrics including vulnerability density, code coverage, and remediation time.

4.10.2 Annual secure coding training must be mandatory for all developers.

4.10.3 Lessons learned from incidents or audits must drive updates to the SDLC framework.

---

## 5. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27034:2011 | Application Security Framework | Secure SDLC governance and assurance |
| ISO/IEC 27002:2022 | Application security controls | Secure coding and testing controls |
| NIST SSDF | Secure Software Development Framework | Secure development lifecycle |
| OWASP ASVS v5 | Application Security Verification Standard | Secure coding requirements |
| COBIT 2019 | BAI03: Managed Solutions Identification and Build | Solution design and build |
| COBIT 2019 | BAI07: Managed IT Change Acceptance and Transitioning | Release and deployment controls |
| CSA CCM v4.1 | SEF: Software Engineering and Development | Software engineering and security controls |
| EU AI Act | Annex IV | AI-generated code governance |

---

**End of Document**
