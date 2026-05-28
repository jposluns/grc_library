# Security Quick Reference

**Document Title:** Security Quick Reference 
**Document Type:** Standard 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Chief Information Officer 
**Related Documents:** [`dev-security/standard-security-baseline-and-standards-reference.md`](standard-security-baseline-and-standards-reference.md), [`dev-security/standard-developer-security-requirements.md`](standard-developer-security-requirements.md), [`dev-security/standard-devops-security-requirements.md`](standard-devops-security-requirements.md) 
**Classification:** Public 
**Category:** Developer Security 
**Review Frequency:** 6 to 12 months and upon material threat, regulatory, or framework change 
**Repository Path:** [`dev-security/standard-security-quick-reference.md`](standard-security-quick-reference.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## How to use this document

If you are unsure whether something is allowed, check this guide first. If the answer is not here, check the relevant standard: Developer Security Requirements (for developers), DevOps Security Requirements (for pipeline/platform engineers), or the Production Security Requirements Standard (for operations). If still unclear, ask the security team before proceeding.

**When in doubt: stop, ask, document.**

---

## NEVER do these things

Absolute prohibitions. No exception exists without written CIO or CISO approval, and most have no exception path at all.

| # | Prohibition | Why |
| --- | --- | --- |
| 1 | Put a secret, credential, API key, token, or password in source code or a config file in version control | Exposed to everyone with repository access and persists in git history forever. |
| 2 | Copy production data to Test or Dev | Breaches PIPEDA, Quebec Law 25, and data governance policy. Documented masking process required. |
| 3 | Use NTLMv1 anywhere | Prohibited. Cannot be used in any environment. |
| 4 | Deploy to production from a local script or developer workstation | All production deployments go through the approved pipeline with gates and approval. |
| 5 | Make a manual production change outside a declared incident | All production changes require a documented change request, CAB review where applicable, and pipeline execution. Manual changes leave no audit trail and introduce untracked drift. |
| 6 | Give a service account Domain Admin or equivalent permanent elevated membership | Minimum required permissions only. |
| 7 | Use SAMAccountName-only authentication in new code | LDAPS and UPN/SSO are the required patterns. |
| 8 | Use MD5, SHA-1, RC4, 3DES, SSL, or TLS 1.0/1.1 | All deprecated. AES-256, SHA-256+, TLS 1.2+ only. |
| 9 | Send personal or Confidential data to an external AI service without a data processing agreement and CIO approval | Violates privacy law and organisational policy. |
| 10 | Bypass a pipeline security gate | Gates exist for a reason. Disable nothing without security team approval. |
| 11 | Reimage or modify a system you suspect is compromised | Preserve evidence. Alert the security team first. |
| 12 | Use `:latest` as a container image tag in Test or Production | Digest-pinned or explicit version tags only. |
| 13 | Create a shadow IT system or unapproved cloud resource | All resources must be under organisational governance and in approved cloud environments. |
| 14 | Store IaC state locally or in version control | Remote state backend with versioning and access logging only. |
| 15 | Leave a self-signed certificate in production | CA-issued certificate required. Internal PKI for internal services; an approved external CA for external-facing services. |
| 16 | Process personal data in a new system without completing a Privacy Impact Assessment | Mandatory under Quebec Law 25. |
| 17 | Put any secret in a workflow configuration file that is tracked in version control | Configuration files in source control are exposed to everyone with repository access. |
| 18 | Hardcode a personal email address as an error notification or approval recipient | When that person leaves, every alert silently fails. |
| 19 | Route production automation traffic to a test workflow endpoint or a disabled workflow | Routes to test endpoints serve wrong responses. Routes to disabled workflows cause silent data loss. |
| 20 | Use unapproved platforms or non-compliant hosted services for production data | Unapproved platforms are ungoverned. Non-compliant hosting may violate data residency requirements. |
| 21 | Run an automation platform host on an EOL runtime | Runtime stability and security patches are not guaranteed after EOL. |
| 22 | Hardcode an entity identifier (customer ID, account ID, tenant identifier) in workflow code | Hard to maintain, breaks multi-tenancy, and is a source of silent data errors. Use configurable parameters. |
| 23 | Store authentication tokens in browser local storage in a web application | Local storage is accessible to any JavaScript in the browser context. Vulnerable to XSS-based token exfiltration. |
| 24 | Modify a production workflow that is a critical financial or operational gate without CIO approval and a formal risk assessment | Any latency or logic change to a financial approval or operational gate carries direct financial exposure. |
| 25 | Use wildcard CORS origins (`origins: "*"`) in any production API, web app, or automation platform HTTP trigger | Wildcard CORS allows any origin to make credentialed requests. Use an explicit allow-list only. |
| 26 | Download or save corporate data to local device storage or personal cloud storage | Violates acceptable use policy and remote working security standard. Corporate data must stay in company-managed storage. |
| 27 | Connect unapproved USB drives or external storage to company devices | Exceptions require CISO approval. |
| 28 | Promote to production without an approved change record | Every production change requires a documented, approved change request. Emergency changes require retrospective CAB review within 24 hours. |
| 29 | Allow a critical or high vulnerability to remain unpatched beyond its SLA | Unpatched critical vulnerabilities are an active security risk. Patch SLAs are mandatory, not targets. |

---

## Authentication decision tree

**Human user accessing the system?** 
Use the enterprise IdP. MFA is mandatory. No bypass permitted. 
For Tier 0 (identity systems, PAM, PKI): phishing-resistant MFA (FIDO2 or certificate-based) required.

**Service-to-service call?** 
Cloud workload caller: use platform managed identity with minimum RBAC. 
Non-cloud caller: PAM-vaulted service account with credential injection, or OAuth 2.0 client credentials with registered application identity. 
Either way: no hard-coded credentials. No shared secrets.

**Directory integration (LDAP bind)?** 
LDAPS (port 636) only. Simple binds on port 389 prohibited. Kerberos AES-256 preferred. RC4 Kerberos: not in new systems.

**External API / gateway integration?** 
OAuth 2.0 client credentials flow validated by IdP token validation policy at the gateway layer. Gateway subscription keys are an additional layer: not the sole mechanism.

---

## Data classification: what to do

| Classification | Encryption at Rest | Encryption in Transit | Who Can Access | Can It Leave the Primary Region? |
| --- | --- | --- | --- | --- |
| Public | Not required (good practice) | HTTPS for web | Anyone | Yes |
| Internal | Required for databases and backups | TLS 1.2+ required | Employees and approved contractors | Yes, with appropriate controls |
| Confidential | Required. AES-256 minimum. | TLS 1.2+ mandatory | Authorized personnel on a need-to-know basis | Requires data residency risk assessment and CIO/Legal approval |
| Restricted | Required. AES-256. Key in secrets vault. | TLS 1.2+ mandatory | Named individuals only. PAM-controlled access where applicable. | Prohibited except with explicit Legal sign-off and documented justification |

If you are unsure what classification applies, classify one level higher until clarified.

---

## Secrets management reference

| Where Are You Working? | Approved Store |
| --- | --- |
| Cloud workloads | Platform secrets management service (key vault) via managed identity |
| On-premises application | PAM vault (credential injection, no password reveal) |
| CI/CD pipeline | CI/CD platform service connections or equivalent pipeline secrets mechanism |
| Application configuration | Secrets reference in configuration, not the secret value |
| Automation workflows | Platform-native secrets management references. Never in config files tracked in version control. |
| API gateway named values | Secrets-management-backed values only. Never hardcoded plain text in gateway policies. |
| Developer local testing | Developer's own isolated secrets vault or local `.env` file that is `.gitignored`. Never in source code. |

Secret rotation must work without a code deployment. If rotating requires a deployment, the secrets management design is wrong.

---

## Environment rules

| Transition | Allowed? | Gate |
| --- | --- | --- |
| Dev → Test | Yes | Merge + pipeline gates pass |
| Test → Prod | Yes | Acceptance-into-service gate + CAB/CIO approval + manual pipeline approval |
| Prod → Dev or Test | Never | Back-promotion prohibited |
| Production data → Test | Never | Masking/synthetic data only |
| Production data → Dev | Never | N/A |

Access in Dev: normal access, limited blast radius. 
Access in Test: elevated review. Security team can be consulted. 
Access in Prod: PAM only. Time-bound. Session recorded. Alert fires.

---

## CI/CD pipeline gate summary

Every pipeline touching Test or Production must include these checks in order. Pipeline fails on Critical findings unless a tracked exception exists.

1. Secret scanning: fail on any secret detected
2. SAST: fail on Critical/High
3. SCA (dependency scan): fail on Critical CVE; High requires tracked issue
4. Container image scan (if containers used): fail on Critical CVE in image
5. IaC scan (if IaC present): fail on Critical misconfiguration
6. License check: fail on unapproved copyleft license
7. Runtime EOL check: fail on deployment to EOL runtime version
8. SBOM generation (production builds only): must generate and archive
9. Manual approval gate (production deployments): human approval required

---

## Change management: quick reference

| Change Type | Approval | CAB Review |
| --- | --- | --- |
| Standard (pre-approved, low-risk) | Team lead | No |
| Normal | CIO delegate | Yes |
| Emergency | CIO | Retrospective within 24 hours |
| High-risk (identity, PAM, PKI, production network) | CIO or CISO | Yes |

Every CAB-reviewed change must include a tested rollback plan. Emergency changes must be codified in IaC within 24 hours.

---

## Patch and vulnerability SLA: quick reference

| Severity | SLA |
| --- | --- |
| Critical (CVSS 9.0 to 10.0) | 24 hours if actively exploited; 72 hours if publicly disclosed; 7 days otherwise |
| High (CVSS 7.0 to 8.9) | 14 days |
| Medium (CVSS 4.0 to 6.9) | 30 days |
| Low (CVSS 0.1 to 3.9) | 90 days or next maintenance window |

These are mandatory SLAs, not targets. Critical findings trigger immediate alert regardless of exploitation status.

---

## Encryption algorithm cheatsheet

| Use Case | Use This | Not This |
| --- | --- | --- |
| Encrypting data at rest | AES-256-GCM | DES, 3DES, RC4 |
| TLS for transit | TLS 1.3 (preferred), TLS 1.2 (minimum) | TLS 1.1, TLS 1.0, SSL anything |
| Hashing for integrity | SHA-256, SHA-384, SHA-512 | MD5, SHA-1 |
| Hashing passwords | Argon2id, bcrypt (cost ≥12) | SHA-256 (for passwords), MD5, plain storage |
| Asymmetric encryption | RSA-4096, EC P-256/P-384 | RSA < 2048 |
| Key exchange | ECDHE, DHE | Static RSA key exchange |
| Signing certificates | SHA-256 RSA or ECDSA | SHA-1 |

---

## Application production onboarding checklist

All of the following must be confirmed before any application onboards to a production environment.

- [ ] UPN/SSO authentication fully implemented and tested (no SAMAccountName-only dependency)
- [ ] All directory binds use LDAPS (port 636). No plain LDAP.
- [ ] All service credentials in platform secrets management service or PAM vault. No hard-coded credentials.
- [ ] SAST, SCA, and secret scanning passing in CI/CD pipeline.
- [ ] Threat model documented and reviewed.
- [ ] Data flow documentation produced.
- [ ] Privacy Impact Assessment completed where personal data is processed.
- [ ] Database deployed in an isolated network segment with no direct internet access.
- [ ] SBOM generated for the release.
- [ ] Integration endpoints documented and firewall/ACL rules approved.
- [ ] Application service owner entry populated in the application registry.

---

## Production go-live security checklist

Evidence required for all of the following before any system promotes to production.

- [ ] Trust configuration: domain trust filtering, selective authentication, and Kerberos-first confirmed
- [ ] NTLM audit: no NTLMv1; NTLM fallback restricted
- [ ] Tier isolation: cross-tier logon attempts denied and verified
- [ ] PAM workflow: approval, credential injection, rotation, and session recording confirmed
- [ ] Network segmentation: allow-listed flows succeed; blocked flows verified blocked
- [ ] Backup immutability: deletion blocked; restore test successful
- [ ] SIEM: critical event categories visible with correct alert routing
- [ ] Break-glass: emergency accounts functional; alerts fire on use

---

## AI development minimum checklist

Before building any AI or ML feature:

- [ ] AI risk classification completed (high-impact or standard?)
- [ ] Threat model updated for AI-specific threats (prompt injection, model poisoning, adversarial inputs, tool-call manipulation)
- [ ] Training data classified and documented
- [ ] If training data contains personal data: Privacy Impact Assessment completed
- [ ] Model documentation created (model card or equivalent)
- [ ] Adversarial attack analysis conducted (reference: OWASP LLM Top 10, MITRE ATLAS, TikiTribe for agentic workflows)
- [ ] Model artefacts signed and checksummed
- [ ] Output validation implemented (AI output treated as untrusted input to downstream systems)
- [ ] Monitoring for model drift and anomalous outputs configured in SIEM
- [ ] AI acceptable use compliance confirmed (no Confidential data to external AI APIs without approval)
- [ ] Open model risk assessment completed if using a public pre-trained model
- [ ] If using an AI service unavailable in the primary cloud region: data residency exception initiated before project begins

---

## Automation workflow deployment checklist

Before any automation workflow deploys to production:

- [ ] Workflow configuration files contain no plain-text secrets (automated scan confirms)
- [ ] All notification and approval recipients are distribution lists, not personal addresses
- [ ] All routing cases point to enabled, active target workflows
- [ ] No routing to test endpoints in production
- [ ] Runtime version is supported (not EOL)
- [ ] All API gateway named values are secrets-management-backed (not plain text)
- [ ] OAuth-based platform connections re-authorized within the last 90 days
- [ ] No wildcard CORS origins

---

## Customer-facing and AI feature security checklist

Before any customer-facing portal, external user interface, or AI-enabled feature goes to production:

- [ ] Authentication tokens NOT stored in browser local storage (use httpOnly cookies or in-memory)
- [ ] Customer or tenant data isolation enforced server-side on every API call: not reliant on frontend claims
- [ ] External users authenticate via external identity management platform with MFA enforced
- [ ] Mobile application uses approved authentication SDK with secure token storage
- [ ] For AI features: AI risk classification completed
- [ ] For AI features: threat model updated for prompt injection and adversarial inputs
- [ ] For AI features: output validation implemented: AI output treated as untrusted before use
- [ ] For AI features: human confirmation required for any write to operational data
- [ ] For AI features: input and output logging configured in SIEM
- [ ] For AI features: rate limiting on all AI endpoints
- [ ] Acceptance-into-service gate completed including AI impact assessment where applicable

---

## Incident response: what to do

1. Do not try to fix it quietly. Silent remediation of a security incident is a serious policy violation.
2. Do not reimage, restart, or modify the affected system.
3. Preserve evidence: take screenshots, capture logs without modifying the system.
4. Alert the security team immediately. If unreachable, escalate to the CIO directly.
5. Follow instructions from the incident commander only.
6. Document everything with timestamps in the incident ticket.

Personal data breach? CIO must be notified immediately. Quebec Law 25 requires notification to the provincial regulator within 72 hours of a breach with serious harm risk.

---

## Key reference areas

| Need | Reference |
| --- | --- |
| Framework authority and principles | Security Baseline and Standards Reference |
| Developer requirements | Developer Security Requirements Standard |
| DevOps requirements | DevOps Security Requirements Standard |
| Production/infrastructure requirements | Operations domain |
| AI security requirements | AI and Agentic Development Security Standard |
| Compliance and gap tracking | Compliance Controls and Gap Register |
| Authentication requirements | Authentication and Password Management Standard |
| Network security requirements | Network Security and Segmentation Standard |
| Data retention requirements | Data Retention Schedule Register |
| Privacy programme | Privacy and Data Governance Policy |
| Cloud exit and portability | Cloud Exit and Data Portability Standard |
| Exception request | CIO or CISO: document in Exception Register |
| Privacy Impact Assessment | Privacy Officer / Legal |

---

**End of Document**
