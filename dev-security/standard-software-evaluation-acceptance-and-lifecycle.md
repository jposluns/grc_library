# Software Evaluation, Acceptance and Lifecycle Management Standard

**Document Title:** Software Evaluation, Acceptance and Lifecycle Management Standard 
**Document Type:** Standard 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Officer 
**Approving Authority:** Chief Information Officer 
**Related Documents:** [`security/policy-acceptance-into-service.md`](../security/policy-acceptance-into-service.md), [`dev-security/policy-secure-development-and-engineering.md`](policy-secure-development-and-engineering.md), [`operations/procedure-patch-management.md`](../operations/procedure-patch-management.md), [`governance/policy-governance-and-risk-management.md`](../governance/policy-governance-and-risk-management.md) 
**Classification:** Public 
**Category:** Developer Security 
**Review Frequency:** Annual and upon material platform or regulatory change 
**Repository Path:** [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](standard-software-evaluation-acceptance-and-lifecycle.md) 
**Confidentiality:** Public 
**Licence:** CC0 1.0 Universal 

---

## Purpose

This standard defines the governance, evaluation, and control requirements for acquiring, testing, approving, deploying, maintaining, and retiring software across the organization. It ensures that all software introduced into the environment is secure, licensed, compliant, and operationally validated before enterprise use, in accordance with the organization's risk, compliance, and change management framework.

---

## Scope

Applies to:

- All business units, subsidiaries, contractors, and research teams introducing or using software.
- Enterprise systems, endpoints, laptops, and mobile devices.
- Cloud, hybrid, or on-premises platforms.
- Open-source, commercial, or internally developed applications.

---

## Governance and Accountability

| Role | Responsibility |
| --- | --- |
| **CIO** | Approves software categories, enterprise standards, and lifecycle governance. |
| **CISO** | Validates cybersecurity and compliance requirements for all software. |
| **IT Operations / Endpoint Management** | Tests deployment, patch, and rollback procedures; manages packaging and rollout. |
| **Procurement** | Ensures that licensing, vendor due diligence, and contract compliance. |
| **Application or System Owner** | Maintains documentation, configuration records, and lifecycle compliance. |
| **Internal Audit** | Conducts periodic reviews of AIS adherence and operational controls. |

---

## 1. Evaluation and Testing

All new or replacement software must undergo structured evaluation and pre-deployment testing including:

- Functional, compatibility, and performance validation.
- Security assessment: vulnerability scanning and threat modelling.
- Licensing verification and vendor security assessment.
- Privacy and data residency verification.

Evaluation environments must be isolated from production systems. Test results are logged in the Acceptance Into Service Register and reviewed by the CISO.

---

## 2. Security and Compliance Review

Before approval, all software must undergo a security and compliance review validating:

- Access control and authentication mechanisms.
- Encryption, key management, and data protection capabilities.
- Logging and audit capabilities.
- Data residency, sovereignty, and third-party processing arrangements.

CSA CCM AIS, SEF, and TVM domains apply to all evaluations.

---

## 3. Acceptance and Approval for Use

Software is formally approved through the Acceptance Into Service Policy and process. The AIS checklist must include:

- Security and privacy validation.
- Business justification.
- Risk classification and mitigation controls.
- Validation of patching, rollback, and support lifecycle.

Formal sign-off is required by the CIO or delegated authority before enterprise deployment.

---

## 4. Deployment and Configuration Control

All deployment activities must comply with the Change Management and Configuration Control Procedure. Requirements include:

- Deployment through authorized automation and endpoint management platforms.
- Phased releases: pilot → controlled → production.
- Rollback and recovery plans validated in testing prior to deployment.

---

## 5. Patch and Update Management

Software patching and updates follow the Vulnerability and Patch Management Standard. Key requirements:

- Critical patches must be applied within 15 days or fewer as determined by the CISO.
- Major version changes require revalidation under the AIS process.
- Patch status is tracked in the IT Asset Management System.

---

## 6. Software Inventory and Version Control

All approved software must be registered in the Asset Inventory Register. Inventory records include:

- Product name, version, and licence details.
- Responsible owner (role title).
- Last review date and next review date.

Unauthorised software detected via automated compliance tools must be removed or quarantined within 24 hours of detection.

---

## 7. Ongoing Review and Retirement

Each software product must undergo annual operational and compliance review. Evaluation includes:

- Vendor support status and end-of-life timeline.
- Licensing status and cost-effectiveness.
- Current vulnerability posture.

Obsolete or unsupported software must be retired following the AIS lifecycle termination workflow and the Continuous Improvement Register Procedure.

---

## Framework Alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 12207 | Software Lifecycle Processes | Software lifecycle governance |
| ISO/IEC 27001:2022 | Information Security Management | Security controls for software |
| ISO/IEC 27002:2022 | Operations and Vulnerability Management | Software security controls |
| ISO/IEC 25010 | System and Software Quality Models | Quality evaluation criteria |
| COBIT 2025 | BAI03: Manage Solutions Identification and Build | Software evaluation and approval |
| COBIT 2025 | BAI07: Manage Change Acceptance and Transitioning | Deployment and acceptance |
| COBIT 2025 | BAI09: Manage Assets | Software asset management |
| COBIT 2025 | DSS05 / DSS06 | Security and operational controls |
| NIST SP 800-53 | SA, CM, SI Control Families | Software assurance controls |
| CSA CCM v5 | AIS, SEF, TVM Domains | Cloud software security evaluation |

---

**End of Document**
