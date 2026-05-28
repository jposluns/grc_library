# AI Coding Assistant Security Guideline

**Document Title:** AI Coding Assistant Security Guideline 
**Document Type:** Guideline 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`dev-security/standard-developer-security-requirements.md`](standard-developer-security-requirements.md), [`dev-security/claude-rules/README.md`](claude-rules/README.md), [`dev-security/standard-security-baseline-and-standards-reference.md`](standard-security-baseline-and-standards-reference.md), [`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md), [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md) 
**Classification:** Public 
**Category:** Developer Security 
**Review Frequency:** 6 to 12 months and upon material change to AI coding tooling, threat landscape, or regulatory guidance 
**Repository Path:** [`dev-security/guideline-ai-coding-assistant-security.md`](guideline-ai-coding-assistant-security.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This guideline defines requirements and best practices for the secure use of AI coding assistants, tools such as Claude Code, GitHub Copilot, Cursor, Windsurf, and equivalent products, within the software development lifecycle.

AI coding assistants introduce distinct risks that differ from conventional development tooling: they generate code that must be reviewed for correctness and security; they may access, transmit, or retain code and data from the development environment; they can be manipulated through prompt injection; and they may hallucinate package names, APIs, or library versions that do not exist. This guideline addresses those risks while enabling productive use.

---

## Scope

Applies to all employees, contractors, and third-party developers using AI coding assistants on:
- Organization-owned or managed devices.
- Organization-managed cloud development environments.
- Projects touching organization codebases, infrastructure, or data.

Does not apply to personal experimentation on personal devices with no connection to organizational data or systems.

---

## Approved tools and authorization

The organization maintains an approved list of AI coding assistants. Developers must use only approved tools for work on organizational systems. Using an unapproved AI coding assistant with organizational code, data, or credentials is a policy violation requiring a formal exception.

When evaluating a new AI coding assistant for approval, the assessment must cover:
- Data handling and retention: what code and context is sent to external APIs; whether the provider retains prompts or completions; applicable data processing agreements.
- Authentication and access scope: what organizational systems the tool can access.
- Security rule configuration: whether the tool accepts binding security constraints (CLAUDE.md, rules files, or equivalent).
- Incident response: the provider's breach notification obligations.

---

## Required security configuration

### Load security rules before using an AI coding assistant

All AI coding assistant sessions working on organizational code must have security rules loaded before generating or reviewing code. The organization's security rules are maintained in `dev-security/claude-rules/`.

**For Claude Code:**
1. Copy [`dev-security/claude-rules/CLAUDE.md`](claude-rules/CLAUDE.md) to the project root. Claude Code reads this file automatically at session start.
2. Add language-specific rule files as needed from `dev-security/claude-rules/languages/`.
3. Add AI/agentic rule files from `dev-security/claude-rules/ai/` for any project using LLMs, agents, RAG, or MCP.

CLAUDE.md also instructs Claude Code to fetch supplementary rule sets from the following external repositories at session start:
- TikiTribe secure coding rules: `https://github.com/TikiTribe/claude-secure-coding-rules`
- Wiz secure rules files: `https://github.com/wiz-sec-public/secure-rules-files`

These are fetched via WebFetch and applied in addition to the local rules.

**For other tools (Copilot, Cursor, Windsurf):**
- Load the relevant rule files from `dev-security/claude-rules/` as the tool's equivalent context (custom instructions, rules files, or workspace settings).
- Ensure that the tool's memory or context is not shared across unrelated projects.

---

## Data handling requirements

### What may and may not be sent to AI coding assistants

| Data Category | May Send | Conditions |
| --- | --- | --- |
| Source code (internal use only) | Yes | With approved tool and active DPA |
| Source code (public or open source) | Yes | No restrictions |
| Configuration files (no secrets) | Yes | Verify no credentials embedded |
| Test data (synthetic or anonymized) | Yes | Confirm no real PII in dataset |
| Personal data (customer PII) | No | Never: regardless of tool |
| Authentication credentials, tokens, keys | No | Never: treat any accidental send as a credential leak |
| Confidential business data (contracts, financials) | No | Requires explicit approval and DPA |
| Restricted data (as defined by data classification standard) | No | Never |

If credentials or personal data are accidentally included in a prompt, treat the event as a potential breach: rotate the credentials immediately and report to the security team.

### Data residency

When using AI coding assistants that send prompts to external APIs:
- Verify that the provider's data processing occurs within approved regions.
- For projects subject to data residency requirements (e.g., GDPR, Quebec Law 25, PIPEDA), confirm the tool provider can satisfy those requirements before use.
- Prefer locally-running models (self-hosted LLMs) for highly sensitive development contexts.

---

## Code review requirements for AI-generated code

AI-generated code is not automatically correct or secure. It must be reviewed with the same scrutiny applied to human-written code, plus additional checks for AI-specific failure modes.

### Mandatory review checklist for AI-generated code

Before committing AI-generated code:

- [ ] **Correctness**: the code does what was intended; edge cases are handled.
- [ ] **No hallucinated dependencies**: verify every import and package reference exists in approved registries under the exact name suggested.
- [ ] **No hardcoded credentials**: scan for API keys, passwords, tokens, or connection strings.
- [ ] **Injection vulnerabilities**: SQL, command, template, and LDAP injection patterns reviewed.
- [ ] **Authentication and authorization**: all endpoints enforce authentication; all authorization decisions are server-side.
- [ ] **Input validation**: all external input is validated server-side before use.
- [ ] **Cryptography**: only approved algorithms used; no custom crypto; no deprecated algorithms.
- [ ] **Logging**: no sensitive data in logs; required security events logged.
- [ ] **Error handling**: internal error details not exposed to callers.
- [ ] **License**: AI-generated code may reproduce training data; verify no unlicensed verbatim reproductions of copyrighted material.

### SAST gate

All code (AI-generated or human-written) passes through SAST before merge. AI-generated code does not reduce the obligation to fix SAST findings. Do not override SAST findings with "AI generated this" as justification.

---

## Prohibited uses

The following uses of AI coding assistants are prohibited without explicit CIO/CISO approval and a formal risk acceptance:

1. Generating code that handles personal data without a human security design review.
2. Using AI to modify production infrastructure or configuration directly (no human review step).
3. Using AI coding assistants on production systems (read access to production data is prohibited).
4. Training or fine-tuning AI models on organizational source code without Legal and CISO sign-off.
5. Using AI coding assistants to bypass security controls (no "write code to disable this security check").
6. Sharing organizational code with AI coding assistant providers that do not have an applicable data processing agreement.
7. Using unapproved AI coding assistants for organizational work.

---

## Prompt injection awareness

Developers using AI coding assistants must be aware that prompt injection can be introduced through:

- **Documents and code comments**: adversarial instructions embedded in code comments, documentation, or dependency changelogs that the assistant reads.
- **Test data and fixtures**: malicious instructions in test input files or database fixtures.
- **Dependency sources**: compromised packages may contain adversarial comments designed to influence AI code generation.
- **Issue trackers and wikis**: AI assistants reading linked content may process instructions embedded in that content.

If an AI coding assistant behaves unexpectedly, generates code that seems designed to exfiltrate data, bypass security controls, or perform unusual actions, treat it as a potential prompt injection event and report it.

---

## Agentic use (multi-step autonomous coding)

AI coding assistants operating in agentic mode (autonomous multi-step task execution with tool access) carry higher risk than single-turn interactions. Additional requirements apply:

- The AI must not have standing write access to production systems.
- The AI must not commit and push directly to the main or release branch without human review.
- Tool access must be scoped to the minimum necessary for the task.
- Agentic sessions must be logged (all tool calls, files read, files written, commands executed).
- Before any destructive action (delete, overwrite, force push), the agent must request explicit human confirmation.

For detailed agentic security requirements, see [`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md) and [`dev-security/claude-rules/ai/agent-security.md`](claude-rules/ai/agent-security.md).

---

## Incident reporting

Report the following events to the security team immediately:

- Credentials, tokens, or personal data accidentally included in a prompt.
- An AI coding assistant that appears to have been influenced by a prompt injection.
- AI-generated code that was committed containing a security vulnerability.
- Unauthorized use of an unapproved AI coding assistant on organizational code.

---

## External reference sources

The following publicly available resources provide additional guidance for AI coding assistant security:

| Source | URL | Relevance |
| --- | --- | --- |
| TikiTribe Secure Coding Rules | `https://github.com/TikiTribe/claude-secure-coding-rules` | Primary rule set for AI coding assistants; includes AI, MCP, RAG, and agent security rules |
| Wiz Secure Rules Files | `https://github.com/wiz-sec-public/secure-rules-files` | Language/framework baseline rules compatible with Claude Code, Cursor, Copilot |
| Kariedo Claude Code Security Rules | `https://github.com/kariedo/claude-code-security-rules` | Modular rules for Claude Code covering core security patterns |
| OWASP LLM Top 10 | `https://owasp.org/www-project-top-10-for-large-language-model-applications/` | Primary threat taxonomy for LLM-specific risks |
| OWASP MCP Top 10 | `https://owasp.org/www-project-mcp-top-10/` | Security risks for MCP-integrated AI systems |
| NIST SP 800-218A (Generative AI Profile) | `https://csrc.nist.gov/pubs/sp/800/218/a/final` | Augments SSDF with AI model development security practices |
| MITRE ATLAS | `https://atlas.mitre.org/` | Adversarial ML techniques including prompt injection and supply chain attacks |
| CISA Secure by Design | `https://www.cisa.gov/resources-tools/resources/secure-by-design` | Principles for building security into products from the start |
| Google SAIF | `https://saif.google/` | Secure AI framework covering development, deployment, and monitoring |
| Anthropic Claude Code Docs | `https://docs.anthropic.com/en/docs/claude-code` | Official documentation for Claude Code permissions, CLAUDE.md, and security model |

---

## Framework alignment

| Control Area | ISO 27001:2022 | NIST SSDF | CSA AICM | Regulatory |
| --- | --- | --- | --- | --- |
| AI tool authorization | A.5.36 | PO.1, PO.3 | AI-GOV-01 | EU AI Act Art. 9 |
| Data handling for AI inputs | A.5.12, A.8.10 | PS.1 | AI-DATA-01 | GDPR, CPPA |
| Code review of AI output | A.8.27, A.8.29 | PW.7 | AI-SEC-02 | N/A |
| Prompt injection awareness | A.5.30 | N/A | AI-SEC-03 | N/A |
| Agentic use controls | A.5.18, A.8.2 | PW.1 | AI-GOV-03 | EU AI Act Art. 14 |
| Incident reporting | A.5.26 | RV.1 | AI-INC-01 | PIPEDA, GDPR |

---

**End of Document**
