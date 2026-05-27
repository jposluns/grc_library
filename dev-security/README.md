# Developer Security Domain

**Document Title:** Developer Security Domain README  
**Document Type:** Register  
**Version:** 1.0.0  
**Date:** 2026-05-27  
**Owner:** Chief Information Security Officer  
**Approving Authority:** Governance Library Maintainer  
**Related Documents:** `README.md`, `governance/register-document-index-and-classification.md`, `security/policy-information-security.md`, `ai/standard-ai-security-and-risk.md`  
**Classification:** Public  
**Category:** Developer Security  
**Review Frequency:** 6 to 12 months and upon material threat, tooling, or framework change  
**Repository Path:** `dev-security/README.md`  
**Confidentiality:** Public  
**Licence:** CC0 1.0 Universal

---

## Purpose

This directory contains security standards, quick-reference guides, compliance registers, and draggable rule files for developers and DevOps practitioners. Content addresses secure development baseline requirements, CI/CD pipeline security, developer toolchain security, and compliance controls for software development activities.

The `claude-rules/` subdirectory provides a set of draggable CLAUDE.md and rule files designed to be dropped directly into a Claude Code session or project directory. These files encode security and compliance requirements as context that AI coding agents can enforce during development.

---

## Active Documents

*Expansion in progress. See planned content below.*

---

## Domain Coverage

### Standards
Developer-facing security requirements covering:

- **Security baseline** — minimum security requirements that apply to all development activities regardless of stack or platform
- **Developer security requirements** — secure coding standards: input validation, output encoding, secrets management, authentication, session handling, cryptographic use, dependency management, logging, and error handling
- **DevOps security requirements** — CI/CD pipeline security, infrastructure as code controls, secrets in pipelines, container image integrity, deployment gates, and environment separation
- **Security quick reference** — concise cheat-sheet format covering the most common development security failures with immediate do/do-not guidance

### Registers
- **Compliance controls and gap register** — template for tracking development security control gaps against applicable standards and frameworks

### claude-rules/
Draggable rule files for Claude Code sessions and AI-assisted development environments. See `dev-security/claude-rules/README.md` for usage guidance.

---

## External Projects and Reference Sources

This domain draws on and references the following external projects. These references are for alignment and awareness; their content is not reproduced here.

### OWASP Projects
- **OWASP Top 10** — Ten most critical web application security risks
- **OWASP LLM Top 10** — Ten most critical risks specific to Large Language Model applications
- **OWASP ASVS** (Application Security Verification Standard) — Detailed security requirements for web applications across three levels of assurance
- **OWASP WSTG** (Web Security Testing Guide) — Testing methodology and test cases for web application security
- **OWASP Cheat Sheet Series** — Concise developer-facing guidance on specific security topics (authentication, session management, injection, etc.)
- **OWASP SAMM** (Software Assurance Maturity Model) — Framework for assessing and improving software security practices

### AI and Agentic Development References
- **OWASP Generative AI Security Project** — Risks and controls specific to generative AI applications and pipelines
- **MITRE ATLAS** — Adversarial threat landscape for AI systems; provides attack technique taxonomy for AI-specific threats
- **NIST AI RMF** — AI risk management framework covering Govern, Map, Measure, and Manage functions
- **TikiTribe** — Open-source project providing AI agent security testing utilities, adversarial prompt libraries, and agentic workflow attack surface enumeration tools; used for testing MCP server security, tool-call injection resistance, and multi-agent trust boundary validation

### DevSecOps References
- **NIST SP 800-218** — Secure Software Development Framework (SSDF); maps to NIST CSF and provides secure development practices
- **SLSA** (Supply-chain Levels for Software Artifacts) — Framework for software supply-chain integrity levels
- **CIS Benchmarks** — Configuration security baselines for OS, container, cloud, and application platforms
- **SANS CWE Top 25** — Most dangerous software weaknesses from the Common Weakness Enumeration catalogue

### Compliance Frameworks Addressed
- ISO/IEC 27001:2022 — Information security management (development-relevant controls)
- ISO/IEC 27002:2022 — Secure development controls (Annex A.8.25–A.8.34)
- NIST SP 800-53 Rev 5 — SA (System and Services Acquisition) and SI (System and Information Integrity) families
- CSA CCM v4 — Application and Interface Security (AIS) domain
- SOC 2 CC6 — Logical and physical access controls, change management

---

## Planned Expansion

### Standards
- `standard-security-baseline-and-standards-reference.md`
- `standard-developer-security-requirements.md`
- `standard-devops-security-requirements.md`
- `standard-security-quick-reference.md`

### Registers
- `register-compliance-controls-and-gap-register.md`

### claude-rules/ (draggable Claude Code rule files)
```
claude-rules/
├── README.md               Usage guide and composition instructions
├── CLAUDE.md               Root rule file — drag this into a project
├── core/
│   ├── secrets.md          Never hardcode credentials, keys, or tokens
│   ├── authentication.md   Secure auth and session requirements
│   ├── input-validation.md Input validation and output encoding
│   ├── cryptography.md     Approved algorithms and key handling
│   └── owasp.md            OWASP Top 10 and ASVS alignment rules
├── ai/
│   ├── ai-security.md      LLM and AI application security requirements
│   ├── agent-security.md   Agentic workflow security and trust boundaries
│   ├── rag-security.md     Retrieval-augmented generation data controls
│   └── mcp-security.md     Model Context Protocol server security rules
├── pipeline/
│   └── cicd-gates.md       CI/CD security gates and pipeline controls
└── languages/
    ├── python.md            Python-specific security patterns and anti-patterns
    ├── typescript.md        TypeScript / Node.js security patterns
    └── csharp.md            C# / .NET security patterns
```

---

**End of Document**
