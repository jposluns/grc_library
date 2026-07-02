# Developer Security Domain

**Document Title:** Developer Security Domain README\
**Document Type:** Register\
**Version:** 1.4.4\
**Date:** 2026-07-02\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`README.md`](../README.md), [`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md), [`security/policy-information-security.md`](../security/policy-information-security.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md)\
**Classification:** Public\
**Category:** Developer Security\
**Review Frequency:** 6 to 12 months and upon material threat, tooling, or framework change\
**Repository Path:** [`dev-security/README.md`](README.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This directory has two layers that share a domain but serve different purposes:

1. **GRC standards for secure development.** Security standards, quick-reference guides, compliance registers, policies, and procedures for developers and DevOps practitioners. Content addresses secure development baseline requirements, CI/CD pipeline security, developer toolchain security, and compliance controls for software development activities. These are normative GRC artefacts of the same shape as content in [`security/`](../security/), [`risk/`](../risk/), and the other domain directories.

2. **The `claude-rules/` operational pack.** A draggable set of CLAUDE.md, rule files, and Claude Code Skills designed to be loaded into a Claude Code session as security and development-governance context. The pack distils disciplines extracted from maintaining this library and is part of the parent library's reference-implementation deliverable. It is also usable as a standalone Claude Code baseline pack, usable on any project regardless of whether it has a GRC corpus, distilled from the disciplines this library required to maintain itself. See [`dev-security/claude-rules/README.md`](claude-rules/README.md) for the pack's own front door and adoption modes.

---

## Active documents

| Type | Title | Path |
| --- | --- | --- |
| Standard | Security Baseline and Standards Reference | [`dev-security/standard-security-baseline-and-standards-reference.md`](standard-security-baseline-and-standards-reference.md) |
| Standard | Developer Security Requirements Standard | [`dev-security/standard-developer-security-requirements.md`](standard-developer-security-requirements.md) |
| Standard | DevOps Security Requirements Standard | [`dev-security/standard-devops-security-requirements.md`](standard-devops-security-requirements.md) |
| Standard | Security Quick Reference | [`dev-security/standard-security-quick-reference.md`](standard-security-quick-reference.md) |
| Policy | Secure Development and Engineering Policy | [`dev-security/policy-secure-development-and-engineering.md`](policy-secure-development-and-engineering.md) |
| Standard | Software Evaluation, Acceptance and Lifecycle Management Standard | [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](standard-software-evaluation-acceptance-and-lifecycle.md) |
| Standard | Quality Assurance and Testing Standard | [`dev-security/standard-quality-assurance-and-testing.md`](standard-quality-assurance-and-testing.md) |
| Register | Compliance Controls and Gap Register | [`dev-security/register-compliance-controls-and-gap-register.md`](register-compliance-controls-and-gap-register.md) |
| Standard | Software Composition Analysis Standard | [`dev-security/standard-software-composition-analysis.md`](standard-software-composition-analysis.md) |
| Guideline | AI Coding Assistant Security Guideline | [`dev-security/guideline-ai-coding-assistant-security.md`](guideline-ai-coding-assistant-security.md) |
| Standard | API Security Standard | [`dev-security/standard-api-security.md`](standard-api-security.md) |
| Standard | Container and Image Security Standard | [`dev-security/standard-container-and-image-security.md`](standard-container-and-image-security.md) |
| Standard | Mobile Application Security Standard | [`dev-security/standard-mobile-application-security.md`](standard-mobile-application-security.md) |
| Procedure | Secure Code Review Procedure | [`dev-security/procedure-secure-code-review.md`](procedure-secure-code-review.md) |
| Standard | AWS Cloud Hardening Baseline Standard | [`dev-security/standard-cloud-hardening-baseline-aws.md`](standard-cloud-hardening-baseline-aws.md) |
| Standard | Azure Cloud Hardening Baseline Standard | [`dev-security/standard-cloud-hardening-baseline-azure.md`](standard-cloud-hardening-baseline-azure.md) |
| Standard | Google Cloud Platform Hardening Baseline Standard | [`dev-security/standard-cloud-hardening-baseline-gcp.md`](standard-cloud-hardening-baseline-gcp.md) |

---

## Domain coverage

### Standards
Developer-facing security requirements covering:

- **Security baseline**: minimum security requirements that apply to all development activities regardless of stack or platform
- **Developer security requirements**: secure coding standards: input validation, output encoding, secrets management, authentication, session handling, cryptographic use, dependency management, logging, and error handling
- **DevOps security requirements**: CI/CD pipeline security, infrastructure as code controls, secrets in pipelines, container image integrity, deployment gates, and environment separation
- **Security quick reference**: concise cheat-sheet format covering the most common development security failures with immediate do/do-not guidance

### Registers
- **Compliance controls and gap register**: template for tracking development security control gaps against applicable standards and frameworks

See the **Claude Code rules pack** section below for the draggable rule files and the AI-assisted setup generator.

---

## Claude Code rules pack

The `claude-rules/` subdirectory ships a set of draggable CLAUDE.md and rule files for Claude Code sessions and AI-assisted development environments. The content is held in this repository as library-canonical material and can be consumed either from disk (local mode) or by fetching it live from the library's canonical raw URL (fetch mode); see [`dev-security/claude-rules/README.md`](claude-rules/README.md) for the four manual placement options and the setup generator's two modes. External rule repositories (TikiTribe, Kariedo, addyosmani, Wiz) are referenced from [`dev-security/claude-rules/README.md`](claude-rules/README.md); they are not loaded automatically at Claude Code session start, but the setup generator's external-source overlay step proposes fetching all four as the default action and lets the consumer accept, modify, or decline before any file is written (EXT-01 vetting is applied per fetch). The Wiz licence (CC-BY-NC-ND-4.0; NonCommercial + NoDerivatives) is surfaced at the offer step so commercial adopters can decline Wiz specifically. The library maintainer back-ports vetted improvements from external sources on the standard freshness cadence and records formal EXT-01 vets in [`dev-security/claude-rules/vetting-log.md`](claude-rules/vetting-log.md).

### Manual setup

Adopters can copy the pack files directly. See [`dev-security/claude-rules/README.md`](claude-rules/README.md) for the four placement options (project-root `CLAUDE.md`, selective rule files under `.claude/rules/`, additions to an existing `CLAUDE.md`, path-scoped rules with `paths:` YAML frontmatter) and the AGENTS interop pattern.

### AI-assisted setup (setup generator)

For consumers who want to skip manual setup, an AI-assisted setup generator at [`dev-security/claude-rules/setup-generator-prompt.md`](claude-rules/setup-generator-prompt.md) analyzes a downstream project and proposes a tailored CLAUDE.md plus rule-file selection, with approval gates before any file is written. It works whether the consumer has a local copy of the pack on disk (local mode) or fetches from the library's first-party canonical source (fetch mode). The pack README covers the three invocation forms (manual paste, `curl` one-liner, and URL-to-Claude) and the first-party trust posture.

### Layout

```
claude-rules/
├── README.md                    Usage guide, placement options, and external source URLs
├── CLAUDE.md                    Root rule file: drag into a project as the always-loaded context
├── setup-generator-prompt.md    AI-assisted setup generator (paste into a Claude Code session)
├── core/
│   ├── secrets.md               Never hardcode credentials, keys, or tokens
│   ├── authentication.md        Secure auth and session requirements
│   ├── input-validation.md      Input validation and output encoding
│   ├── cryptography.md          Approved algorithms and key handling
│   └── owasp.md                 OWASP Top 10:2025, ASVS v5.0.0, and MCP Top 10 alignment rules
├── ai/
│   ├── ai-security.md           LLM and AI application security requirements
│   ├── agent-security.md        Agentic workflow security and trust boundaries
│   ├── rag-security.md          Retrieval-augmented generation data controls
│   └── mcp-security.md          Model Context Protocol server security rules
├── pipeline/
│   └── cicd-gates.md            CI/CD security gates and pipeline controls
└── languages/
    ├── python.md                Python-specific security patterns and anti-patterns
    ├── typescript.md            TypeScript / Node.js security patterns
    ├── csharp.md                C# / .NET security patterns
    ├── java.md                  Java / Spring Boot security patterns
    └── go.md                    Go security patterns
```

---

## External projects and reference sources

This domain draws on and references the following external projects. These references are for alignment and awareness; their content is not reproduced here.

### OWASP projects
- **OWASP Top 10**: Ten most critical web application security risks
- **OWASP LLM Top 10**: Ten most critical risks specific to Large Language Model applications
- **OWASP ASVS** (Application Security Verification Standard): Detailed security requirements for web applications across three levels of assurance
- **OWASP WSTG** (Web Security Testing Guide): Testing methodology and test cases for web application security
- **OWASP Cheat Sheet Series**: Concise developer-facing guidance on specific security topics (authentication, session management, injection, etc.)
- **OWASP SAMM** (Software Assurance Maturity Model): Framework for assessing and improving software security practices

### AI and agentic development references
- **OWASP Generative AI Security Project**: Risks and controls specific to generative AI applications and pipelines: `https://genai.owasp.org/`
- **OWASP LLM Top 10**: Ten most critical risks for Large Language Model applications: `https://owasp.org/www-project-top-10-for-large-language-model-applications/`
- **OWASP MCP Top 10**: Security risks for Model Context Protocol integrations: `https://owasp.org/www-project-mcp-top-10/`
- **MITRE ATLAS**: Adversarial threat landscape for AI systems; attack technique taxonomy for AI-specific threats: `https://atlas.mitre.org/`
- **NIST AI RMF**: AI risk management framework covering Govern, Map, Measure, and Manage functions: `https://www.nist.gov/itl/ai-risk-management-framework`
- **NIST SP 800-218A**: Generative AI Profile augmenting SSDF with AI model development practices: `https://csrc.nist.gov/pubs/sp/800/218/a/final`
- **Google SAIF**: Secure AI Framework for secure development, deployment, execution, and monitoring: `https://saif.google/`
- **TikiTribe**: Open-source rule sets for AI coding assistants; covers AI, agent, MCP, and RAG security; aligns to OWASP LLM Top 10, OWASP MCP Top 10, MITRE ATLAS, and NIST AI RMF: `https://github.com/TikiTribe/claude-secure-coding-rules`

### AI coding assistant rule repositories
- **Wiz Secure Rules Files**: Baseline security rules compatible with Claude Code, Cursor, and Copilot; organized by language and framework: `https://github.com/wiz-sec-public/secure-rules-files`
- **Kariedo Claude Code Security Rules**: Modular rules for Claude Code using `@`-syntax import system: `https://github.com/kariedo/claude-code-security-rules`

### DevSecOps references
- **NIST SP 800-218**: Secure Software Development Framework (SSDF); maps to NIST CSF and provides secure development practices: `https://csrc.nist.gov/pubs/sp/800/218/final`
- **SLSA**: Supply-chain Levels for Software Artifacts; framework for software supply-chain integrity levels: `https://slsa.dev/`
- **CIS Benchmarks**: Configuration security baselines for OS, container, cloud, and application platforms: `https://www.cisecurity.org/cis-benchmarks`
- **CISA Secure by Design**: Principles for shifting security burden to manufacturers; secure default configuration: `https://www.cisa.gov/resources-tools/resources/secure-by-design`
- **MITRE CWE Top 25**: Most dangerous software weaknesses from the Common Weakness Enumeration catalogue: `https://cwe.mitre.org/top25/`

### Compliance frameworks addressed
- ISO/IEC 27001:2022: Information security management (development-relevant controls)
- ISO/IEC 27002:2022: Secure development controls (Annex A.8.25 to A.8.34)
- NIST SP 800-53 Rev. 5: SA (System and Services Acquisition) and SI (System and Information Integrity) families
- CSA CCM v4.1: Application and Interface Security (AIS) domain
- SOC 2 CC6: Logical and physical access controls, change management

---

## Planned expansion

- Java EE / Jakarta EE security standard

---

**End of Document**
