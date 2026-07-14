# Software Evaluation, Acceptance and Lifecycle Management Standard

**Document Title:** Software Evaluation, Acceptance and Lifecycle Management Standard\
**Document Type:** Standard\
**Version:** 1.0.6\
**Date:** 2026-07-14\
**Owner:** Chief Information Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`security/policy-acceptance-into-service.md`](../security/policy-acceptance-into-service.md), [`dev-security/policy-secure-development-and-engineering.md`](policy-secure-development-and-engineering.md), [`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md), [`operations/procedure-patch-management.md`](../operations/procedure-patch-management.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md)\
**Classification:** Public\
**Category:** Developer Security\
**Review Frequency:** Annual and upon material platform or regulatory change\
**Repository Path:** [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](standard-software-evaluation-acceptance-and-lifecycle.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines the governance, evaluation, and control requirements for acquiring, testing, approving, deploying, maintaining, and retiring software across the organization. It ensures that all software introduced into the environment is secure, licensed, compliant, and operationally validated before enterprise use, in accordance with the organization's risk, compliance, and change management framework.

---

## 2. Scope

Applies to:

- All business units, subsidiaries, contractors, and research teams introducing or using software.
- Enterprise systems, endpoints, laptops, and mobile devices.
- Cloud, hybrid, or on-premises platforms.
- Open-source, commercial, or internally developed applications.

---

## 3. Governance and accountability

| Role | Responsibility |
| --- | --- |
| **CIO** | Approves software categories, enterprise standards, and lifecycle governance. |
| **CISO** | Validates cybersecurity and compliance requirements for all software. |
| **IT Operations / Endpoint Management** | Tests deployment, patch, and rollback procedures; manages packaging and rollout. |
| **Procurement** | Ensures that licensing, vendor due diligence, and contract compliance are managed. |
| **Application or System Owner** | Maintains documentation, configuration records, and lifecycle compliance. |
| **Internal Audit** | Conducts periodic reviews of AIS adherence and operational controls. |

---

## 4. Evaluation and testing

All new or replacement software must undergo structured evaluation and pre-deployment testing including:

- Functional, compatibility, and performance validation.
- Security assessment: vulnerability scanning and threat modelling.
- Licensing verification and vendor security assessment.
- Privacy and data residency verification.

Evaluation environments must be isolated from production systems. Test results are logged in the Acceptance Into Service Register and reviewed by the CISO.

---

## 5. Security and compliance review

Before approval, all software must undergo a security and compliance review validating:

- Access control and authentication mechanisms.
- Encryption, key management, and data protection capabilities.
- Logging and audit capabilities.
- Data residency, sovereignty, and third-party processing arrangements.

CSA CCM AIS, SEF, and TVM domains apply to all evaluations.

---

## 6. Acceptance and approval for use

Software is formally approved through the Acceptance Into Service Policy and process. The AIS checklist must include:

- Security and privacy validation.
- Business justification.
- Risk classification and mitigation controls.
- Validation of patching, rollback, and support lifecycle.
- For systems incorporating an action-capable AI agent: the agent production-authority precondition (`AGENT-PROD-01` in the AI and Agentic Development Security Standard) is satisfied and evidenced, including tested reversibility or compensating-transaction mechanisms for production-impacting action classes. Acceptance is withheld until the precondition is met.

Formal sign-off is required by the CIO or delegated authority before enterprise deployment.

---

## 7. Deployment and configuration control

All deployment activities must comply with the Change Management and Configuration Control Procedure. Requirements include:

- Deployment through authorized automation and endpoint management platforms.
- Phased releases: pilot → controlled → production.
- Rollback and recovery plans validated in testing prior to deployment.

---

## 8. Patch and update management

Software patching and updates follow the Vulnerability and Patch Management Standard. Key requirements:

- Critical patches must be applied within the severity-based remediation SLAs in [`../security/procedure-vulnerability-management.md`](../security/procedure-vulnerability-management.md) section 2 (the single source of truth); that procedure governs on any discrepancy.
- Major version changes require revalidation under the AIS process.
- Patch status is tracked in the IT Asset Management System.

---

## 9. Software inventory and version control

All approved software must be registered in the Asset Inventory Register. Inventory records include:

- Product name, version, and licence details.
- Responsible owner (role title).
- Last review date and next review date.

Unauthorized software detected via automated compliance tools must be removed or quarantined within 24 hours of detection.

---

## 10. Ongoing review and retirement

Each software product must undergo annual operational and compliance review. Evaluation includes:

- Vendor support status and end-of-life timeline.
- Licensing status and cost-effectiveness.
- Current vulnerability posture.

Obsolete or unsupported software must be retired following the AIS lifecycle termination workflow and the Continuous Improvement Register Procedure.

---

## 11. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 12207 | Software Lifecycle Processes | Software lifecycle governance |
| ISO/IEC 27001:2022 | Information Security Management | Security controls for software |
| ISO/IEC 27002:2022 | Operations and Vulnerability Management | Software security controls |
| ISO/IEC 25010 | System and Software Quality Models | Quality evaluation criteria |
| COBIT 2019 | BAI03: Manage Solutions Identification and Build | Software evaluation and approval |
| COBIT 2019 | BAI07: Manage Change Acceptance and Transitioning | Deployment and acceptance |
| COBIT 2019 | BAI09: Manage Assets | Software asset management |
| COBIT 2019 | DSS05 / DSS06 | Security and operational controls |
| NIST SP 800-53 | SA, CM, SI Control Families | Software assurance controls |
| CSA CCM v4.1 | AIS, SEF, TVM Domains | Cloud software security evaluation |

---

**End of Document**
