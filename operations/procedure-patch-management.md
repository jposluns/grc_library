# Patch Management Procedure

**Document Title:** Patch Management Procedure 
**Document Type:** Procedure 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** IT Operations Lead 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`operations/standard-production-security-requirements.md`](standard-production-security-requirements.md), [`security/procedure-vulnerability-management.md`](../security/procedure-vulnerability-management.md), [`operations/procedure-change-management-and-configuration-control.md`](procedure-change-management-and-configuration-control.md), [`security/policy-information-security.md`](../security/policy-information-security.md) 
**Classification:** Public 
**Category:** Operations Security 
**Review Frequency:** Annual and upon material threat, framework, or regulatory change 
**Repository Path:** [`operations/procedure-patch-management.md`](procedure-patch-management.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This procedure defines the end-to-end process for identifying, classifying, testing, authorizing, deploying, and verifying security patches and software updates across the organisation's technology estate. It operationalizes the patch remediation SLAs established in the Production Security Requirements Standard and the Vulnerability Management Procedure, translating policy obligations into repeatable operational steps.

Effective patch management reduces the window of exposure between public vulnerability disclosure and remediation, limits the attack surface available for exploitation, and demonstrates measurable compliance with regulatory and framework obligations.

---

## Scope

1. Applies to all managed assets including: endpoints (workstations, laptops, mobile devices); servers (physical and virtual); network devices (firewalls, switches, routers, load balancers); cloud workloads (virtual machines, container images, serverless functions); applications (first-party and third-party); firmware (hardware management controllers, network device firmware); and third-party and open-source software libraries.
2. Applies to production, staging, and development environments. Non-production environments are not exempt from patch SLAs where they share infrastructure with production or process sensitive data.
3. Applies to IT Operations, Cloud Engineers, Development Teams, and any System Owner accountable for an in-scope asset.

---

## Governance and accountability

| Role | Responsibility |
| --- | --- |
| **IT Operations Lead** | Owns the patch management programme; operates the patching infrastructure; produces compliance reports. |
| **Chief Information Security Officer (CISO)** | Sets patch SLAs; approves exceptions and emergency patches; receives monthly compliance reporting. |
| **Change Advisory Board (CAB)** | Authorizes Standard patch deployments; receives post-notification for Emergency patches. |
| **System Owners** | Accountable for ensuring patches are applied to their assets within defined SLAs; raise deferrals where operationally required. |
| **Development Teams** | Responsible for patching application dependencies and open-source libraries; integrate SCA tooling into CI/CD pipelines. |
| **Internal Audit** | Reviews programme compliance, exception governance, and SLA adherence annually. |

---

## 1. Patch classification

Every patch or update is classified on receipt to determine the required deployment pathway and timeline. Classification is based on CVSS score and active exploitation status.

| Classification | Trigger Condition | Deployment Timeline | Authorization |
| --- | --- | --- | --- |
| **Emergency** | Actively exploited vulnerability (CISA KEV listed or credible equivalent intelligence) | Deploy within 24 hours | CISO approval; CAB post-notification |
| **Standard Critical** | CVSS ≥ 9.0; not yet actively exploited | Deploy within 72 hours after testing | CAB approval via standard change |
| **Standard High** | CVSS 7.0 to 8.9 | Deploy within 14 days | CAB approval via standard change |
| **Standard Medium** | CVSS 4.0 to 6.9 | Deploy within 30 days | Standard change or scheduled maintenance window |
| **Standard Low** | CVSS < 4.0 | Deploy within 90 days | Scheduled maintenance window |
| **Vendor-Recommended Update** | Vendor advisory without CVE assignment | Deploy at next maintenance window unless reclassified higher | Standard change |

IT Operations reviews newly published CISA KEV entries daily. A KEV listing for a vulnerability affecting in-scope assets triggers immediate reclassification to Emergency regardless of previously assigned CVSS score.

---

## 2. Patch testing

### 2.1 Staging requirement

Standard patch classifications (Critical, High, Medium, Low) require deployment to a staging environment before production. The staging environment must be representative of the production configuration being patched.

### 2.2 Emergency patch exception

Emergency patches may be deployed directly to production without prior staging when the 24-hour window makes staging impractical. Direct-to-production Emergency deployments must include:

1. Pre-deployment backup or snapshot of affected systems.
2. Rollback plan documented before deployment commences.
3. Enhanced post-deployment monitoring for a minimum of 24 hours.
4. Retrospective staging validation completed within 72 hours of production deployment.

### 2.3 Regression testing

Before any Standard patch is promoted to production, IT Operations and the relevant System Owner must complete a regression testing checklist covering:

- Service availability verification (critical functions operational post-patch).
- Integration point validation (downstream and upstream dependencies unaffected).
- Security configuration verification (patch has not altered security-relevant settings).
- Performance baseline comparison where applicable.

---

## 3. Deployment authorization

| Classification | Authorization Pathway |
| --- | --- |
| **Emergency** | CISO approval (verbal or written) before deployment; CAB notified post-deployment within 2 hours; retrospective CAB review within 5 business days |
| **Standard Critical** | CAB approval via standard change request; expedited CAB review within 24 hours of submission |
| **Standard High** | CAB approval via standard change request; standard review cycle |
| **Standard Medium / Low** | Standard change request or inclusion in scheduled maintenance window; CAB approval not required if within pre-approved maintenance window scope |

All deployments, regardless of classification, must be documented in the ITSM platform with the patch identifier, affected systems, deployment timestamp, and post-deployment verification result.

---

## 4. Exceptions and deferrals

Where an operational dependency prevents patching within the required SLA, for example, system stability risk, vendor-imposed patching constraints, or application compatibility issues, a formal exception must be raised before the SLA deadline lapses.

| Requirement | Detail |
| --- | --- |
| **Approval authority** | CISO approval required for all exceptions. CIO co-approval required for Critical and Emergency exceptions. |
| **Documentation** | Business justification; risk assessment; compensating controls implemented; target remediation date. |
| **Maximum deferral** | 30 days for Critical and High; 90 days for Medium; 180 days for Low. |
| **Compensating controls** | Required for all Critical and High deferrals. Examples: network isolation, WAF rule, egress restriction, enhanced monitoring. |
| **Register** | All exceptions logged in the Exception Register with status and review dates tracked. |
| **Review** | Open exceptions reviewed monthly by IT Operations and the CISO. Extended deferrals beyond maximum duration require CIO escalation. |

---

## 5. End-of-life system management

End-of-life (EOL) systems no longer receive security patches from vendors. No EOL system is permitted in production without a CIO-approved exception, consistent with the Production Security Requirements Standard.

Upon a system reaching EOL status:

1. IT Operations immediately notifies the relevant System Owner and the CISO.
2. The CIO is notified within 24 hours of confirmed EOL status in production.
3. A formal risk acceptance or decommission plan must be approved and documented within 30 days.
4. Where risk acceptance is approved, enhanced compensating controls are mandatory: network segmentation, access restriction, and continuous monitoring.
5. EOL status and associated exceptions are reviewed monthly until the system is decommissioned or replaced.

EOL tracking is maintained in the asset register, with automated alerts at 180, 90, and 30 days before each asset's EOL date as specified in the Vulnerability Management Procedure.

---

## 6. Third-party and open-source library patching

Application dependencies, including open-source libraries, third-party SDKs, and container base images, are subject to the same patch SLA table as infrastructure assets.

1. **Software Bill of Materials (SBOM):** Development Teams maintain an SBOM for each production application. SBOMs are updated on every release and reviewed for newly published vulnerabilities weekly.
2. **SCA pipeline integration:** Software Composition Analysis (SCA) tooling is integrated into the CI/CD pipeline. Builds that introduce or fail to remediate High or Critical dependency vulnerabilities are blocked from promotion to production.
3. **SAST integration:** Static Application Security Testing (SAST) is run on every commit. Findings are triaged and remediated under the same severity classification and SLA framework as infrastructure patches.
4. **Container base images:** Container images are rebuilt against patched base images within the same SLA timelines as server-class systems. Deployed container images are rescanned weekly.

---

## 7. Monitoring and reporting

### 7.1 Patch compliance dashboard

IT Operations maintains a real-time patch compliance dashboard covering all in-scope assets. The dashboard displays:

- Assets patched within SLA vs. overdue, by classification.
- Open exceptions count and age.
- EOL assets in production.
- Emergency patch deployment status and post-deployment verification state.

### 7.2 SIEM alerting

The SIEM generates an alert if a Critical or High patch has not been deployed within its SLA. Alerts are routed to IT Operations and the CISO. Unacknowledged alerts escalate to the CIO after 4 hours for Critical and 24 hours for High.

### 7.3 Reporting

| Report | Frequency | Audience |
| --- | --- | --- |
| Patch compliance report | Monthly | CISO |
| Exception status review | Monthly | CISO, relevant System Owners |
| Programme effectiveness summary | Quarterly | Executive Risk Committee (ERC) |
| Annual programme review | Annual | CISO, CIO, Internal Audit |

### 7.4 Key metrics

| Metric | Target |
| --- | --- |
| Emergency patch deployment within 24 hours | 100% |
| Critical patch deployment within 72 hours | ≥ 95% |
| High patch deployment within 14 days | ≥ 90% |
| Medium patch deployment within 30 days | ≥ 90% |
| EOL assets in production without approved exception | 0 |
| Open Critical/High exceptions beyond maximum deferral | 0 |

---

## 8. Evidence retention

| Record Type | Retention Period |
| --- | --- |
| Patch deployment records (ITSM tickets, change records, verification evidence) | 3 years |
| Exception records (approvals, risk assessments, compensating control documentation) | 7 years |
| Emergency patch authorization records | 7 years |
| EOL risk acceptance records | 7 years from date of decommission or acceptance |

Retention timelines are subject to the Records Retention and Destruction Standard. Records must be retrievable for audit purposes within 5 business days of a request.

---

## Framework alignment

| Control Area | NIST SP 800-40 Rev 4 | ISO/IEC 27001:2022 | CSA CCM v4.1 | CIS Controls v8 | COBIT 2019 |
| --- | --- | --- | --- | --- | --- |
| Patch planning and classification | §2 (Planning) | A.8.8 | TVM-08 | Control 7.1 | DSS05.07 |
| Patch testing | §3 (Testing) | A.8.8 | TVM-08 | Control 7.4 | DSS05.07 |
| Deployment authorization | §3 (Deploying) | A.8.8 | TVM-08 | Control 7.3 | BAI06.01 |
| Exception governance | §4 (Exceptions) | A.5.20 | TVM-12 | Control 7.2 | APO12.06 |
| EOL lifecycle management | §4 (Unsupported software) | A.8.8 | TVM-01, TVM-02 | Control 7.5 | DSS05.07 |
| Third-party / library patching | §3 (Third-party) | A.8.8 | TVM-08 | Control 7.6 | DSS05.07 |
| Monitoring and reporting | §2 (Metrics) | A.8.8 | TVM-09 | Control 7.7 | MEA01.04 |

---

**End of Document**
