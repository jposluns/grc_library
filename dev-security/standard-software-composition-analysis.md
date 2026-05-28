# Software Composition Analysis Standard

**Document Title:** Software Composition Analysis Standard 
**Document Type:** Standard 
**Version:** 1.1.1 
**Date:** 2026-05-28 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`dev-security/README.md`](README.md), [`dev-security/policy-secure-development-and-engineering.md`](policy-secure-development-and-engineering.md), [`dev-security/standard-developer-security-requirements.md`](standard-developer-security-requirements.md), [`dev-security/standard-devops-security-requirements.md`](standard-devops-security-requirements.md), [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](standard-software-evaluation-acceptance-and-lifecycle.md), [`dev-security/standard-quality-assurance-and-testing.md`](standard-quality-assurance-and-testing.md), [`dev-security/register-compliance-controls-and-gap-register.md`](register-compliance-controls-and-gap-register.md), [`security/policy-acceptance-into-service.md`](../security/policy-acceptance-into-service.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`compliance/policy-compliance-and-audit-management.md`](../compliance/policy-compliance-and-audit-management.md) 
**Classification:** Public 
**Category:** Developer Security: Software Supply Chain 
**Review Frequency:** 6 to 12 months and upon material tooling change, significant supply chain incident, or new regulatory guidance on SBOM or software provenance 
**Repository Path:** [`dev-security/standard-software-composition-analysis.md`](standard-software-composition-analysis.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This standard defines the requirements for Software Composition Analysis (SCA) across all software development, evaluation, and procurement activities. SCA identifies, tracks, and manages the security and licensing risks introduced by open-source components, third-party libraries, and their transitive dependencies.

Software supply chain attacks, including dependency confusion, typosquatting, and malicious package injection, have become a primary threat vector. This standard provides controls to address that risk systematically throughout the software development lifecycle.

---

## Scope

This standard applies to:
- All internally developed software that includes open-source or third-party library dependencies
- All software procured from third parties or SaaS vendors where source code or SBOM is accessible
- All AI and machine learning systems that use open-source model frameworks, datasets, or inference libraries
- All containerized workloads and container images
- All infrastructure-as-code (IaC) that references external modules or provider plugins

This standard applies to all languages and package ecosystems in use across the organisation including but not limited to Python (pip/PyPI), JavaScript/TypeScript (npm, yarn), Java (Maven, Gradle), C# (.NET/NuGet), Go (Go modules), Ruby (Gems), and Rust (Cargo).

---

## Definitions

| Term | Definition |
|---|---|
| **Software Composition Analysis (SCA)** | Automated analysis of software to identify open-source and third-party components, their versions, known vulnerabilities, and associated licenses |
| **Software Bill of Materials (SBOM)** | A structured, machine-readable inventory of all components, libraries, and their metadata included in a software artefact |
| **Transitive Dependency** | A component that is not directly declared but is included because a direct dependency depends on it |
| **Dependency Confusion Attack** | An attack where a malicious package with the same name as an internal package is published to a public registry and automatically resolved |
| **Typosquatting** | Publishing a malicious package under a name similar to a popular legitimate package |
| **CVE** | Common Vulnerabilities and Exposures: standardized identifiers for known vulnerabilities |
| **CVSS** | Common Vulnerability Scoring System: a numeric score (0 to 10) representing the severity of a vulnerability |
| **PURL** | Package URL: a standardized scheme for identifying packages across ecosystems |
| **SLSA** | Supply-chain Levels for Software Artifacts: a framework for supply-chain integrity levels |

---

## SCA requirements

### 1. Tool integration

SCA tools must be integrated at multiple points in the software development lifecycle:

| Integration Point | Requirement | Timing |
|---|---|---|
| **Developer workstation** | SCA plugin or pre-commit hook alerts developer to new vulnerable dependencies before code is committed | At dependency addition |
| **CI/CD pipeline: build stage** | SCA scan runs automatically on every build; build fails if any Critical-severity vulnerability is introduced | Every build |
| **CI/CD pipeline: release gate** | Full SCA report generated and reviewed before any production deployment; unresolved High+ vulnerabilities block release unless formally accepted | Pre-deployment gate |
| **Container image scanning** | All container images scanned for OS-level and application-level vulnerabilities before promotion to any non-development registry | At image build and registry push |
| **Scheduled background scan** | All active repositories and deployed artefacts scanned weekly for newly disclosed vulnerabilities in existing dependencies | Weekly |
| **SBOM generation** | SBOM generated as an artefact of every production build in CycloneDX or SPDX format | Every production build |

### 2. Vulnerability remediation slas

| CVSS Score | Severity | Maximum Age in Production | Escalation on Breach |
|---|---|---|---|
| 9.0 to 10.0 | Critical | 7 calendar days | CISO; executive leadership |
| 7.0 to 8.9 | High | 30 calendar days | CISO |
| 4.0 to 6.9 | Medium | 90 calendar days | Security Champion |
| 0.1 to 3.9 | Low | 180 calendar days or at next release | Development team |
| 0.0 | None / Informational | At next scheduled maintenance | Development team |

Where a fix is not available (no patched version exists), the following actions must be taken within the SLA for the severity:
1. Document the vulnerability and remediation blocker in the risk register
2. Implement a compensating control (e.g., input validation, network isolation, WAF rule)
3. Obtain formal risk acceptance from the CISO if the vulnerability will remain open beyond the SLA
4. Monitor for patch availability daily for Critical, weekly for High

### 3. Licence compliance

All open-source licences in use must be reviewed and approved before use in the organisation's products or services.

| Licence Category | Examples | Use Permitted | Conditions |
|---|---|---|---|
| **Permissive** | MIT; Apache 2.0; BSD 2-clause; BSD 3-clause; ISC | Yes: no special conditions | Attribution required; retain licence notices |
| **Weak Copyleft** | LGPL 2.1; LGPL 3.0; MPL 2.0; EUPL 1.2 | Yes: with conditions | Must not statically link LGPL components into proprietary code without compliance review; MPL modifications must be shared |
| **Strong Copyleft** | GPL 2.0; GPL 3.0; AGPL 3.0 | Conditional, requires legal review | GPL components in products distributed externally require legal review; AGPL requires source disclosure for network services, escalate to Legal before use |
| **Proprietary / Commercial** | Custom commercial licences | Subject to procurement and legal review | Licence terms must be reviewed; ensure that scope covers intended use |
| **Unknown / Unlicensed** | No licence file present | Prohibited without legal clearance | Treat as "All rights reserved"; obtain written clarification from author |
| **Incompatible / Prohibited** | SSPL; BUSL; Commons Clause | Prohibited in production: requires exception | These licences impose restrictions incompatible with commercial use; escalate to Legal |

**Licence inventory obligations:**
- All production dependencies must have an identified and approved licence
- Transitive dependencies must be included in licence review
- SCA tooling must produce a licence inventory as part of the SBOM
- Legal must be consulted before introducing any Strong Copyleft or Unknown licence dependency

### 4. Software bill of materials (SBOM)

#### Minimum SBOM content

SBOMs must comply with the NTIA Minimum Elements for a Software Bill of Materials and must include:

| Field | Description |
|---|---|
| Supplier name | Name of the component's author or publisher |
| Component name | Name of the component |
| Version | Version string or commit hash |
| Other unique identifiers | PURL (Package URL); CPE (Common Platform Enumeration) where available |
| Dependency relationship | Whether direct or transitive; parent component |
| Author of SBOM data | Tool or person that generated this SBOM entry |
| Timestamp | Date and time the SBOM was generated |

#### SBOM format

SBOMs must be produced in at least one of:
- **CycloneDX** (preferred): XML or JSON; supports VEX (Vulnerability Exploitability eXchange)
- **SPDX**: tag-value, JSON, or RDF; widely adopted in open-source tooling

#### SBOM retention and distribution

| Use Case | Requirement |
|---|---|
| Internal artefact store | SBOM retained alongside each release artefact; minimum 3 years |
| Customer requests | SBOM must be provided to customers on written request within 30 days |
| Regulatory requests | SBOM must be provided to regulatory authorities on lawful request |
| Incident response | SBOM must be immediately accessible to incident responders to assess blast radius of disclosed CVE |

### 5. Supply chain attack mitigations

#### Dependency confusion and package integrity

| Control | Requirement |
|---|---|
| **Private registries for internal packages** | All internally developed packages must be published to and consumed from a private registry. Internal package names must use organisation-controlled namespace prefixes that cannot be registered on public registries. |
| **Registry scoping** | Package manager configuration files (`.npmrc`, `pip.conf`, `nuget.config`, `settings.xml`) must scope internal packages to the private registry only; public registry fallback must be disabled for namespaces used internally. |
| **Dependency pinning** | All direct dependencies must be pinned to an exact version in the dependency manifest. Ranges (e.g., `^1.0.0`, `>=2.0`) are prohibited for production builds. |
| **Lock files** | Dependency lock files (`package-lock.json`, `yarn.lock`, `poetry.lock`, `requirements.txt` with hashes, `go.sum`) must be committed to version control and treated as authoritative for builds. Lock files must not be regenerated without explicit approval. |
| **Package hash verification** | CI/CD pipelines must verify package integrity using cryptographic hashes at install time. |
| **Subresource Integrity (SRI)** | For web applications loading third-party scripts via CDN, SRI hashes must be included in HTML `<script>` and `<link>` tags. |

#### Source and build integrity (SLSA alignment)

The organisation targets the following SLSA levels by system type:

| System Type | Target SLSA Level | Rationale |
|---|---|---|
| Externally accessible applications | SLSA Level 2 | Build-as-code; signed provenance |
| Internal tooling | SLSA Level 1 | Documented build process |
| Critical infrastructure code | SLSA Level 3 | Hermetic, reproducible builds; hardened build platform |

SLSA Level 2 minimum requirements:
- Build process defined in version-controlled build scripts
- Build platform generates signed provenance (build inputs, outputs, timestamps)
- Provenance verified before artefacts are deployed

### 6. Triaging and exceptions

Not all CVEs require immediate remediation. Developers must triage each finding using the following criteria:

| Triage Factor | Consideration |
|---|---|
| **Exploitability** | Is an exploit publicly known and weaponized? (EPSS score; CISA KEV catalogue) |
| **Reachability** | Is the vulnerable code path actually called by the application? (Use SAST or reachability analysis) |
| **Attack surface** | Is the vulnerable component exposed to untrusted input? (e.g., parsing user-supplied data vs. internal tooling) |
| **Compensating controls** | Do network controls, WAF rules, or input validation already mitigate the attack vector? |

Findings assessed as not exploitable in context must be documented using a **VEX (Vulnerability Exploitability eXchange)** statement in the SBOM, specifying the justification status (`not_affected`; `in_triage`; `affected`; `fixed`) and rationale.

Formal exceptions to SLA timelines must be approved by the CISO and documented in the risk register.

### 7. AI and machine learning dependencies
SCA controls apply to all ML and AI codebases with the following additional requirements:

| Requirement | Description |
|---|---|
| **Model framework dependencies** | All ML framework dependencies (TensorFlow, PyTorch, scikit-learn, Hugging Face Transformers, etc.) must be included in SCA scans |
| **Pre-trained model provenance** | Pre-trained models obtained from public repositories (Hugging Face Hub, TensorFlow Hub, etc.) must be verified for provenance: model card review, author verification, checksum validation |
| **Dataset licence review** | Open-source datasets used in training must be reviewed for licence compatibility and provenance documentation |
| **Supply chain risk for LLM APIs** | Third-party LLM API dependencies (model provider libraries, SDK versions) must be assessed for vulnerability using the same SCA process |

---

### 8. Tool acceptance criteria

The SCA programme is tool-agnostic; the requirements above govern what every tool must produce, not which tool to use. When evaluating, selecting, or replacing a tool, apply the following acceptance criteria. The criteria are listed in priority order; a tool that fails a higher-priority criterion is rejected regardless of how well it satisfies lower-priority criteria.

| Criterion | Acceptance requirement | Verification method |
| --- | --- | --- |
| Language and ecosystem coverage | Covers every first-party language and package ecosystem in production use, including transitive dependencies | Inventory of in-scope projects mapped against the tool's supported ecosystems |
| Vulnerability database currency | Vulnerability data refreshed at least daily from authoritative sources (NVD, vendor advisories, language-specific advisory databases) | Tool documentation review plus a sample query for a CVE disclosed within the last seven days |
| Detection accuracy | False-positive rate measured against a representative repository sample remains below 10% after suppression rules are applied | One-time evaluation harness comparing tool output against a hand-curated baseline |
| SBOM generation | Produces machine-readable SBOM in CycloneDX or SPDX, including transitive dependencies, hashes, and licence fields | Generate an SBOM for a known project and inspect the output against the format specification |
| CI/CD integration | Native integration with the CI/CD platform in use, with an exit code or annotation that blocks merge on a configurable severity threshold | Run in a pipeline against a known-vulnerable test repository and confirm the pipeline fails |
| Vulnerability suppression and exception workflow | Permits suppression with reason code, expiry, and audit trail; suppressions surface in reports | Suppress a finding, verify it appears in the suppression register, expire the suppression, confirm the finding returns |
| VEX support | Permits attaching VEX statements to declare a vulnerability not applicable, with the rationale travelling with the SBOM | Generate a VEX statement and verify it embeds correctly in the produced SBOM |
| Open-source dependency licensing | Tool licence permits the intended use (commercial, internal, redistribution) | Licence review by Legal |
| Data residency | Tool processes code or metadata only in jurisdictions consistent with the data residency standard | Tool deployment model review; for SaaS tools, vendor data residency attestation |
| Cost transparency | Pricing model documented and aligned with the IT financial management standard | Procurement evaluation |

A tool that passes the criteria is documented in the security architecture registry. Tool changes require re-evaluation; the prior tool's findings are migrated and reconciled before the new tool replaces it in the CI/CD pipeline.

---

## Roles and responsibilities

| Role | Responsibilities |
|---|---|
| **Developer** | Perform triage on SCA findings in their codebase; remediate within SLA; document VEX justifications for non-exploitable findings |
| **Security Champion** | Review SCA reports for their team; escalate unresolved High+ findings; advise on compensating controls |
| **DevOps / Platform Team** | Maintain and configure SCA tooling in CI/CD pipelines; ensure that SBOM generation is automated; manage private registry configuration |
| **CISO** | Approve exceptions to remediation SLAs; set organisational risk acceptance thresholds; review Critical vulnerability escalations |
| **Legal** | Review and approve licence exceptions; advise on SBOM distribution obligations |
| **Procurement** | Require SBOMs from commercial software vendors; include SBOM provision clauses in software procurement contracts |

---

## Metrics

| Metric | Target | Reporting Frequency |
|---|---|---|
| Mean time to remediate Critical vulnerabilities | ≤ 7 days | Weekly |
| Mean time to remediate High vulnerabilities | ≤ 30 days | Monthly |
| Percentage of production builds with SBOM generated | 100% | Monthly |
| Percentage of dependencies with pinned exact versions | ≥ 95% | Quarterly |
| Licence compliance coverage (all dependencies reviewed) | 100% | Quarterly |
| Number of Critical findings open beyond SLA | 0 | Weekly |

---

## Framework and regulatory alignment

| Framework / Requirement | Relevance |
|---|---|
| **NIST SSDF (SP 800-218)** | PW.4, Reuse well-secured software; PS.1/PS.2, Protect software supply chain |
| **NIST SP 800-53 Rev 5** | SA-12 Memory Protection; SR-3 Supply Chain Controls; SR-4 Provenance; SR-11 Component Authenticity |
| **US Executive Order 14028** | SBOM minimum elements requirement; software supply chain security for federal use |
| **EU Cyber Resilience Act (CRA)** | Product cybersecurity requirements including vulnerability handling and SBOM obligations for products with digital elements; applies from 2027 |
| **SLSA Framework** | Build integrity levels 1 to 4; provenance requirements |
| **OWASP Dependency-Check** | Reference tooling for vulnerability identification in Java, .NET, Python, Ruby, Node.js |
| **CycloneDX / SPDX** | SBOM format standards |
| **ISO/IEC 27002:2022** | A.8.30, Outsourced development; A.8.31, Separation of development, test, and production environments |
| **NIST CSF 2.0** | ID.AM-3, Software asset inventory; GV.SC, Supply chain risk management |

---

**End of Document**
