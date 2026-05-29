# DevOps Security Requirements

**Document Title:** DevOps Security Requirements\
**Document Type:** Standard\
**Version:** 1.0.2\
**Date:** 2026-05-28\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`dev-security/standard-security-baseline-and-standards-reference.md`](standard-security-baseline-and-standards-reference.md), [`dev-security/standard-developer-security-requirements.md`](standard-developer-security-requirements.md), [`dev-security/standard-security-quick-reference.md`](standard-security-quick-reference.md), [`operations/README.md`](../operations/README.md)\
**Classification:** Public\
**Category:** Developer Security\
**Review Frequency:** 6 to 12 months and upon material tooling, threat, or infrastructure change\
**Repository Path:** [`dev-security/standard-devops-security-requirements.md`](standard-devops-security-requirements.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## Purpose

This standard defines security requirements for DevOps engineering: CI/CD pipelines, infrastructure as code, environment management, container security, and automation platform operational security. For production and infrastructure operations controls, see the operations domain. For developer security requirements, see the Developer Security Requirements Standard.

---

## 1. CI/CD pipeline security

### 1.1 Pipeline as code

All pipeline definitions must be stored in version control. Pipeline files must not contain hard-coded credentials, API keys, tokens, or logic that bypasses security gates.

### 1.2 Mandatory pipeline security gates

The following gates are mandatory in every pipeline deploying to Test or Production. The pipeline must fail and halt on any gate failure.

| Gate | Failure Threshold |
| --- | --- |
| Secret scanning | Any secret pattern detected: fail immediately |
| SAST | Critical or High: fail. Medium: warn and log. |
| SCA: dependency scan | Critical CVE: fail. High CVE: fail unless tracked issue exists with 14-day grace. |
| Container image scanning | Critical CVE in base image or layer: fail. |
| IaC scanning | Critical misconfiguration: fail. |
| Licence compliance | GPL/AGPL without Legal approval: fail. |
| SBOM generation | Must generate and archive on every production build. |
| Runtime EOL check | Deployment to EOL runtime version: fail. See Security Baseline Standard. |

Gate results are logged and retained as acceptance-into-service gate audit evidence.

*CCM: CCC-01 through CCC-09, AIS-04 / NIST SSDF PW.8 / SLSA Level 2+*

### 1.3 Pipeline identity

The CI/CD pipeline must use a dedicated service identity, not a human account. For cloud deployments: service connection backed by managed identity or service principal with minimum permissions. For on-premises deployments: PAM-vaulted service account with credential injection. The pipeline identity must not be able to approve its own production deployments.

### 1.4 Branch protection

Protected branches feeding Test or Production pipelines must enforce: at minimum one required reviewer (two for security-sensitive repos); no direct push; SAST, SCA, and secret scanning must pass before merge; branch deletion restricted.

### 1.5 Production deployment approval

Production deployments require manual approval from a designated approver who is not the pipeline author. The approval is recorded as an audit event. Emergency deployments still require approval, which may be asynchronous but must be obtained within 4 hours and documented.

### 1.6 Artifact integrity

All build artefacts deployed to Production must be signed (signing key in the organisation's secrets management service) and the signature verified before deployment. An artefact with an invalid or absent signature must not be deployed.

*CCM: CCC-04, CCC-05 / SLSA Level 3*

---

## 2. Infrastructure as code (iac)

**Everything as code.** All infrastructure provisioning must be defined as code. Manual production changes are prohibited except in declared incidents and must be codified within 24 hours.

**Approved tooling categories:** Terraform, Bicep, ARM templates, Ansible, or equivalent declarative infrastructure tools. Choice must be consistent within a workstream.

### IaC security standards

- IaC scanning must pass with no Critical findings.
- Encryption explicitly configured. Network access explicitly restricted. Logging and diagnostic settings configured for every resource.
- Resource tagging: environment, owner, classification level, and cost centre.
- No secrets in IaC code: use secrets management references or managed identity.

### State management

IaC state must be stored remotely in a cloud object store with versioning and access logging. Not in version control. Not local. State backends require authentication.

---

## 3. Environment separation and promotion

### Three-environment model

| Environment | Identity Domain | Promotion Gate |
| --- | --- | --- |
| Dev | Dedicated dev domain | Developer merge approval |
| Test | Dedicated test domain | Acceptance-into-service gate (security and functional sign-off) |
| Production | Production domain | Acceptance-into-service gate + manual approval + Change Advisory Board (CAB) |

Test consolidates all pre-production testing (integration, QA, UAT). Multiple server or service copies may exist within Test. All are treated as Test-tier for security classification and access control.

### Promotion rules

- Code and configuration move Dev → Test → Production only. No lateral movement. No back-promotion.
- Production data must not flow to Test or Dev. Data masking or synthetic data required.
- Environment-specific configuration must not be shared across environments.
- Developers do not have standing production access. Production access for incident response is time-bound, through PAM, and audited.

*CCM: I&S-05, DSP-15*

---

## 4. Container and platform security

**Base images:** Sourced from approved trusted registries. Minimal (distroless, Alpine) preferred. Must be scanned before use and on a scheduled cadence. Must not run as root. Privileged mode prohibited in production.

**Image versioning:** No `:latest` tag in Test or Production. Digest-pinned or specific version tags only. All images deployed to Production must be signed.

**Runtime security:** EDR tooling mandatory on all servers. Resource limits (CPU, memory) set. Network policies restrict container-to-container communication to required flows. Secrets must not be passed as plain-text environment variables: use platform secrets management integration.

**Image registry:** Private container registry only. No runtime pulls from public registries in production.

*CCM: I&S-04*

---

## 5. Cloud security configuration

All DevOps teams must comply with cloud security configuration requirements when provisioning, configuring, or modifying any cloud resource. DevOps-specific obligations:

- Every application provisioned by a DevOps team must have its own isolated secrets vault. Cross-application secret sharing is prohibited.
- IaC must explicitly configure encryption, network access restrictions, diagnostic settings, and resource tagging on every resource. Defaults are not sufficient.
- Cloud governance policy enforcement must be applied at management group or subscription level. Pipelines must not deploy to EOL runtime versions or resources violating the policy baseline.
- Sandbox subscriptions must have no network path to production data. Cross-subscription connectivity from production to sandbox is prohibited.

---

## 6. Multi-subscription and multi-account governance

- RBAC reviewed across all accounts and subscriptions in a single consolidated quarterly review.
- Service principal or service account assignments spanning multiple accounts documented with business justification.
- Governance policy applied at organisation level; deviations from organisation-level enforcement require documented justification and a compensating-control plan.
- Sandbox accounts must have no network path to production data. Cross-account connectivity from production to sandbox is prohibited.

---

## 7. Automation platform operational security

This section defines deployment-time and operational security requirements for automation platforms (workflow automation and equivalent). Coding-level security requirements for automation workflows are in the Developer Security Requirements Standard.

### Runtime version management

All automation platform runtimes must be on a supported, non-EOL version. A runtime EOL tracking register must be maintained. SIEM alerts fire at 60 and 30 days before any runtime EOL. Pipelines block deployment to EOL runtimes per §1.2. Upgrade sequence: sandbox regression testing first, then production.

### Deployment prerequisites

Before any automation workflow deploys to production:

- Workflow configuration files contain no plain-text secrets: verified by automated secret scan in pipeline.
- Runtime version is supported (not EOL).
- No cross-account resource references from production to sandbox.
- All vendor API endpoint URLs are production endpoints, not development or staging.
- API gateway named values are secrets-management-backed (not plain text).

### OAuth connection re-authorization

Platform OAuth connections expire after a defined period (typically 90 days). A quarterly re-authorization audit of all OAuth-type connections is mandatory. This is an operational obligation enforced by the DevOps team.

---

## 8. API gateway operational requirements

API gateway timeout must equal or exceed worst-case backend response time. All gateway named values must be secrets-management-backed. Gateway observability workspace must be onboarded to the SIEM.

---

## 9. Shared file system security

On-premises shared file systems used by automated workflows as production dependencies must be: access-restricted to the specific service accounts and named administrators that require access; availability-monitored with a SIEM alert on unavailability; included in any applicable migration programme. File permissions audited on any shared file system used in a production automation path.

---

## 10. Application service owner registry

An application service owner registry must be populated before any application onboards to production. Required fields: application name, version, owner, admin contact, operational status, support team, compliance requirements.

---

## 11. Framework and runtime EOL: DevOps requirements

The EOL classification policy and remediation SLAs are defined in the Security Baseline Standard. DevOps obligations:

- All applications must declare their runtime versions explicitly. Undeclared or floating runtime versions are prohibited in production.
- When a runtime enters Class 3 (within 180 days of EOL), create an upgrade task in the team backlog.
- When a runtime is Class 2 (within 90 days of EOL or already EOL), the upgrade must be in active development with a target completion date.
- When a runtime is Class 1 (over 12 months EOL with qualifying CVE), the service must be in emergency remediation. No new feature development occurs until the runtime is upgraded.
- CI/CD pipelines must not deploy code to a runtime version classified as EOL by organisational governance policy. Attempted deployment fails the pipeline.
- Cloud governance policy enforcement and CI/CD pipeline EOL gate are both required. One does not substitute for the other.
- AI-generated code suggestions to use deprecated or EOL package versions must be rejected.

---

## Framework alignment

| Control Area | ISO 27001/27002 | CSA CCM v4 | NIST SSDF | NIST SP 800-53 | SLSA |
| --- | --- | --- | --- | --- | --- |
| CI/CD pipeline security | A.8.25 to 8.27 | CCC-01 to 09, AIS-04 | PW.8 | SA-10, SA-15 | Level 2 to 3 |
| Pipeline secret scanning | A.8.10 | CEK-10 to 21 | PW.8.2 | IA-5 | Level 2 |
| Artifact signing and integrity | A.8.27 | CCC-04 to 05 | DS.2 | SA-12 | Level 3 |
| IaC security | A.8.25 | CCC-06 | PW.4 | CM-2, CM-3 | N/A |
| Environment separation | A.8.31 | I&S-05 | PO.5 | SC-3, SC-7 | N/A |
| Container security | A.8.25 | I&S-04 | PW.2 | CM-7, SI-3 | N/A |
| EOL and patch management | A.8.8 | TVM-01 to 10 | PW.4.4 | SI-2 | N/A |
| Change management | A.8.32 | CCC-01 to 09 | N/A | CM-3 | N/A |

---

**End of Document**
