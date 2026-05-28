# Quality Assurance and Testing Standard

**Document Title:** Quality Assurance and Testing Standard 
**Document Type:** Standard 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Officer 
**Approving Authority:** Chief Information Officer 
**Related Documents:** [`dev-security/policy-secure-development-and-engineering.md`](policy-secure-development-and-engineering.md), [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](standard-software-evaluation-acceptance-and-lifecycle.md), [`security/policy-acceptance-into-service.md`](../security/policy-acceptance-into-service.md), [`ai/framework-ai-governance-and-risk.md`](../ai/framework-ai-governance-and-risk.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md) 
**Classification:** Public 
**Category:** Developer Security 
**Review Frequency:** Annual and upon material framework or platform change 
**Repository Path:** [`dev-security/standard-quality-assurance-and-testing.md`](standard-quality-assurance-and-testing.md) 
**Confidentiality:** Public 
**Licence:** CC0 1.0 Universal 

---

## Purpose

This standard defines the Quality Assurance (QA) and testing framework for software, infrastructure, and system changes to ensure that consistent reliability, performance, and compliance across all organizational technology environments. It establishes testing lifecycle stages, quality gates, acceptance criteria, and validation requirements for projects and releases.

---

## Scope

1. Applies to all software, infrastructure, data pipeline, and AI system development and deployment activities.
2. Covers code quality validation, performance testing, security testing, and user acceptance testing (UAT).
3. Applies to projects managed internally or by third-party vendors.
4. Includes testing for AI models, datasets, and automation pipelines.

---

## Governance and Accountability

| Role | Responsibility |
| --- | --- |
| **CIO** | Provides executive oversight of QA programme effectiveness and resourcing. |
| **CISO** | Ensures that security testing integration, vulnerability management, and compliance. |
| **QA Manager** | Owns QA framework, defines testing standards, ensures that adherence to lifecycle requirements. |
| **Developers / Engineers** | Perform unit, integration, and regression testing per QA standards. |
| **Project Managers** | Ensure that QA milestones are achieved before release; coordinate test planning. |
| **Business Owners** | Approve UAT completion and verify functional acceptance. |
| **AI Governance Council (AIGC)** | Reviews AI-related testing for explainability, fairness, and performance validation. |
| **Internal Audit** | Reviews test documentation and evidence for compliance and quality verification. |

---

## QA and Testing Lifecycle

| Stage | Objective | Responsible Party |
| --- | --- | --- |
| **1: Planning** | Define testing strategy, scope, and acceptance criteria | QA Manager / Project Manager |
| **2: Design** | Develop test cases, scripts, and test data | QA / Development Team |
| **3: Execution** | Run manual and automated tests across environments | QA / Engineers |
| **4: Defect Management** | Identify, log, and resolve issues before release | QA / Developers |
| **5: Acceptance and Sign-Off** | Confirm successful test results and stakeholder approval | Business Owner / Project Manager |
| **6: Continuous Improvement** | Review lessons learned and update QA artefacts | QA Manager / Internal Audit |

---

## Quality Gates and Release Criteria

No release may proceed without documented approval of quality gate checkpoints:

- 100% completion of critical and high-severity defect fixes.
- Minimum 95% test coverage achieved.
- Successful completion of performance, regression, and security testing.
- Verified rollback plan and backup integrity confirmed.
- UAT sign-off by the business owner.

**Defect severity resolution targets:**

| Severity | Target Resolution |
| --- | --- |
| Critical | Immediate / before release |
| High | Within 3 business days |
| Medium | Within 7 business days |
| Low | Next scheduled release |

---

## Testing Types and Requirements

### Security and Vulnerability Testing

Security testing must align with the Vulnerability and Patch Management Standard and the Secure Development and Engineering Policy, including:

- Static Application Security Testing (SAST).
- Dynamic Application Security Testing (DAST).
- Software Composition Analysis (SCA).
- Penetration testing for major releases and annually.
- All critical vulnerabilities must be remediated before release.

### AI Model Testing

AI model testing is governed by the AI Testing, Validation and Documentation Standard and must include:

- Model accuracy, robustness, and explainability validation.
- Dataset fairness and bias analysis.
- Reproducibility verification.
- Adversarial input resilience testing.
- AIGC review for High-risk AI systems.

### Performance Testing

- Load and stress testing must be conducted for all Tier 1 and Tier 2 systems before production deployment.
- Performance benchmarks are defined in test plans and compared against actual results.
- Performance regressions must be investigated and resolved before release.

---

## Test Environment Requirements

- Test environments must be logically isolated from production.
- Production data must not be used in non-production environments unless it has been fully anonymized.
- Test environment configuration must mirror production security controls where technically feasible.

---

## Framework Alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO 9001:2015 | §8.6: Release of Products and Services | Quality gate and release requirements |
| ISO/IEC 27001:2022 | Annex A.8.29 | Security testing in development |
| COBIT 2025 | BAI03: Manage Solutions Identification and Build | Solution quality assurance |
| CSA CCM v5 | SEF-06: Testing and Quality Assurance | Cloud software testing controls |
| NIST SP 800-53 | SA: System and Services Acquisition Family | Software assurance controls |

---

**End of Document**
