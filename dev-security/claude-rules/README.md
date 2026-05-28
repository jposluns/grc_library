# Claude Code Security Rules: Usage Guide

**Document Title:** Claude Code Security Rules Usage Guide
**Document Type:** Guideline
**Version:** 1.1.0
**Date:** 2026-05-27
**Owner:** Chief Information Security Officer
**Approving Authority:** Governance Library Maintainer
**Related Documents:** [`dev-security/standard-developer-security-requirements.md`](../standard-developer-security-requirements.md), [`dev-security/standard-devops-security-requirements.md`](../standard-devops-security-requirements.md), [`dev-security/guideline-ai-coding-assistant-security.md`](../guideline-ai-coding-assistant-security.md), [`ai/standard-ai-and-agentic-development-security.md`](../../ai/standard-ai-and-agentic-development-security.md)
**Repository Path:** [`dev-security/claude-rules/README.md`](README.md)
**Classification:** Public
**Category:** Developer Security
**Review Frequency:** 6 to 12 months and upon material threat, tooling, or framework change
**Confidentiality:** Public
**Licence:** CC0 1.0 Universal

---

## What Are These Files?

The `claude-rules/` directory contains a set of Markdown files designed to be loaded into [Claude Code](https://docs.anthropic.com/en/docs/claude-code) sessions as security context. When Claude Code reads these files, either via a `CLAUDE.md` in your project root or via explicit `/add-files`, they encode security and compliance requirements as persistent context that the AI coding assistant applies during development.

These are **draggable rule files**: copy any subset into your project's Claude Code context and Claude will apply those security requirements to code it writes, reviews, and suggests.

---

## Directory Structure

```text
claude-rules/
├── README.md                   This file
├── CLAUDE.md                   Root file — drag this into a project for full coverage
├── core/
│   ├── secrets.md              Never hardcode credentials, keys, or tokens
│   ├── authentication.md       Secure authentication and session requirements
│   ├── input-validation.md     Input validation and output encoding
│   ├── cryptography.md         Approved algorithms and key handling
│   └── owasp.md                OWASP Top 10 (2021/2025) and ASVS v5 alignment rules
├── ai/
│   ├── ai-security.md          LLM and AI application security requirements
│   ├── agent-security.md       Agentic workflow security and trust boundaries
│   ├── rag-security.md         Retrieval-augmented generation data controls
│   └── mcp-security.md         Model Context Protocol server security rules
├── pipeline/
│   └── cicd-gates.md           CI/CD security gates and pipeline controls
└── languages/
    ├── python.md                Python-specific security patterns and anti-patterns
    ├── typescript.md            TypeScript / Node.js security patterns
    ├── csharp.md                C# / .NET security patterns
    ├── java.md                  Java / Spring security patterns
    └── go.md                    Go security patterns
```

---

## How to Use

### Option 1: Copy CLAUDE.md to Your Project Root

The simplest approach. Copy `CLAUDE.md` into your project root. Claude Code will automatically read it at session start. It imports the most critical rules across all categories and includes instructions for Claude to fetch supplementary rules from external sources.

```bash
cp path/to/claude-rules/CLAUDE.md ./CLAUDE.md
```

### Option 2: Selective Rule Files

Copy only the rule files relevant to your project:

```bash
# For a Python web API with AI features
cp path/to/claude-rules/core/secrets.md .claude/rules/
cp path/to/claude-rules/core/input-validation.md .claude/rules/
cp path/to/claude-rules/ai/ai-security.md .claude/rules/
cp path/to/claude-rules/languages/python.md .claude/rules/
```

Then reference them in your project's `CLAUDE.md`:
```markdown
See .claude/rules/ for security requirements that apply to all code in this project.
```

### Option 3: Add to Existing CLAUDE.md

Copy the content of specific rule files into your existing `CLAUDE.md` under a `## Security Requirements` heading.

---

## Rule Files and Their Scope

| File | When to Use |
| --- | --- |
| `core/secrets.md` | All projects. No exceptions. |
| `core/authentication.md` | Any project with user login, service accounts, or APIs |
| `core/input-validation.md` | Any project processing external input |
| `core/cryptography.md` | Any project storing data, using passwords, or transmitting data |
| `core/owasp.md` | Web applications and APIs (covers OWASP Top 10) |
| `ai/ai-security.md` | Any project using LLMs, AI APIs, or AI-generated content |
| `ai/agent-security.md` | Agentic systems, multi-agent workflows, autonomous task execution |
| `ai/rag-security.md` | Retrieval-augmented generation (RAG) systems |
| `ai/mcp-security.md` | Projects building or consuming MCP servers |
| `pipeline/cicd-gates.md` | DevOps/platform engineers configuring CI/CD |
| `languages/python.md` | Python codebases |
| `languages/typescript.md` | TypeScript / Node.js codebases |
| `languages/csharp.md` | C# / .NET codebases |
| `languages/java.md` | Java / Spring Boot codebases |
| `languages/go.md` | Go codebases |

---

## Recursive External Fetch

`CLAUDE.md` instructs Claude Code to fetch supplementary rule sets from external repositories at session start using WebFetch. These external sources are fetched and applied in addition to the local rules. If a fetch fails, the local rules remain in force.

The CLAUDE.md fetches from:
- **TikiTribe** `rules/_core/`: AI, agent, MCP, and RAG security rules (see TikiTribe section below)
- **Wiz** `secure-rules-files`: language and framework baseline rules

This means a single `CLAUDE.md` in your project root gives Claude Code access to both the GRC library rules and the latest external rule sets without manually copying each file.

---

## External References

These rule files draw on and are aligned to the following external projects and standards. All are publicly available and free to reference.

### AI Coding Assistant Rule Repositories

**TikiTribe: Secure Coding Rules for AI Coding Assistants**
- Repository: `https://github.com/TikiTribe/claude-secure-coding-rules`
- Coverage: 100+ rule sets covering 12 programming languages, 5+ backend frameworks, 11 AI/ML frameworks, 51 RAG tools, IaC, containers, CI/CD, OWASP Top 10, OWASP MCP Top 10, MITRE ATLAS, NIST AI RMF, Google SAIF, agentic AI
- Key paths fetched by CLAUDE.md:
 - `rules/_core/ai-security.md`
 - `rules/_core/agent-security.md`
 - `rules/_core/mcp-security.md`
 - `rules/_core/rag-security.md`
- Integration: See [`ai/guide-ai-adversarial-test-reference.md`](../../ai/guide-ai-adversarial-test-reference.md) §B4 for test case overlap rules

**Wiz: Secure Rules Files**
- Repository: `https://github.com/wiz-sec-public/secure-rules-files`
- Coverage: Baseline rules compatible with Claude, Cursor, and Copilot; organized by programming language and framework; open source; AI-generated and human-verified
- Use: Language-specific rules as a second layer over this library's language files

**Kariedo: Claude Code Security Rules**
- Repository: `https://github.com/kariedo/claude-code-security-rules`
- Coverage: Core universal security practices, language-specific rules (Python, JavaScript, Java, PHP, Ruby, Rust, C), common vulnerability prevention, uses `@`-syntax import system for modular organization
- Use: Alternative modular rule set for projects needing broader language coverage

---

### OWASP Projects

**OWASP Top 10 for Web Applications (2021 and 2025)**
- URL: `https://owasp.org/www-project-top-10/`
- Direct application: `core/owasp.md`

**OWASP Top 10 for Large Language Model Applications**
- URL: `https://owasp.org/www-project-top-10-for-large-language-model-applications/`
- Direct application: `ai/ai-security.md`, `ai/agent-security.md`, `ai/rag-security.md`

**OWASP MCP Top 10 (Model Context Protocol)**
- URL: `https://owasp.org/www-project-mcp-top-10/`
- Direct application: `ai/mcp-security.md`, `core/owasp.md`

**OWASP Application Security Verification Standard (ASVS) v5.0.0**
- URL: `https://owasp.org/www-project-application-security-verification-standard/`
- Direct application: `core/owasp.md`, `core/authentication.md`, `core/cryptography.md`

**OWASP Cheat Sheet Series**
- URL: `https://cheatsheetseries.owasp.org/`
- Use: Fetch the cheat sheet for specific security topics during development sessions

**OWASP Software Assurance Maturity Model (SAMM)**
- URL: `https://owasp.org/www-project-samm/`
- Use: Programme-level maturity assessment for development security practices

**OWASP Web Security Testing Guide (WSTG)**
- URL: `https://owasp.org/www-project-web-security-testing-guide/`
- Use: Testing methodology reference for manual security testing

---

### NIST Frameworks

**NIST SSDF: Secure Software Development Framework (SP 800-218)**
- URL: `https://csrc.nist.gov/pubs/sp/800/218/final`
- Coverage: Prepare the Organization (PO), Protect the Software (PS), Produce Well-Secured Software (PW), Respond to Vulnerabilities (RV)
- Direct application: all rule files in `core/` and `pipeline/`

**NIST SP 800-218A: Generative AI Profile**
- URL: `https://csrc.nist.gov/pubs/sp/800/218/a/final`
- Coverage: Augments SP 800-218 with AI model development practices; AI-specific secure development tasks
- Direct application: all rule files in `ai/`

**NIST AI Risk Management Framework (AI RMF 1.0)**
- URL: `https://www.nist.gov/system/files/documents/2023/01/26/AI%20RMF%201.0.pdf`
- Coverage: Govern, Map, Measure, Manage functions for AI systems
- Direct application: `ai/ai-security.md`, `ai/agent-security.md`

---

### MITRE Frameworks

**MITRE ATLAS (Adversarial Threat Landscape for AI Systems)**
- URL: `https://atlas.mitre.org/`
- Coverage: 16 tactics and 84+ techniques for AI-specific attacks (data poisoning, adversarial examples, prompt injection, model extraction, ML supply chain)
- Direct application: `ai/ai-security.md`, `ai/agent-security.md`, `ai/rag-security.md`, `ai/mcp-security.md`

**MITRE CWE Top 25 Most Dangerous Software Weaknesses**
- URL: `https://cwe.mitre.org/top25/`
- Coverage: Annual list of the most dangerous software weaknesses based on CVE data
- Direct application: `core/input-validation.md`, `core/cryptography.md`

---

### Government and Standards Body Guidance

**CISA Secure by Design**
- URL: `https://www.cisa.gov/resources-tools/resources/secure-by-design`
- Coverage: Three principles: take ownership of customer security outcomes, embrace radical transparency, lead from the top; shift-left approach; secure default configuration
- Direct application: `pipeline/cicd-gates.md`, `core/owasp.md`

**SLSA: Supply-chain Levels for Software Artifacts**
- URL: `https://slsa.dev/`
- Coverage: Four levels of build provenance and supply-chain integrity; source integrity, build integrity, dependency tracking
- Direct application: `pipeline/cicd-gates.md`

**Google Secure AI Framework (SAIF)**
- URL: `https://saif.google/`
- Coverage: Secure development, deployment, execution, and monitoring for AI systems; mitigates model stealing, data poisoning, prompt injection, and information extraction
- Direct application: `ai/ai-security.md`, `ai/agent-security.md`

**CIS Benchmarks**
- URL: `https://www.cisecurity.org/cis-benchmarks`
- Coverage: Consensus-based configuration baselines for OS, containers, cloud platforms, databases, and network devices
- Use: Reference for hardening production environments where AI-assisted code is deployed

---

### Cloud Security Alliance

**CSA Cloud Controls Matrix (CCM) v4.0**
- URL: `https://cloudsecurityalliance.org/research/cloud-controls-matrix/`
- Coverage: 207 controls across 17 domains
- Direct application: framework alignment tables in all `core/` rule files

**CSA AI Controls Matrix (AICM) v1.0.3**
- URL: `https://cloudsecurityalliance.org/research/ai-controls-matrix/`
- Coverage: 13 AI-specific security controls mapped to CCM domains
- Direct application: framework alignment tables in all `ai/` rule files

---

## Licence

All content in this directory is released under CC0 1.0 Universal. Copy, modify, and redistribute freely.

External repositories (TikiTribe, Wiz, Kariedo) maintain their own licences: check each repository before redistribution.

---

**End of Document**
