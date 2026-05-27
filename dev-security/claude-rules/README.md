# Claude Code Security Rules — Usage Guide

**Document Title:** Claude Code Security Rules Usage Guide  
**Document Type:** Guideline  
**Version:** 1.0.0  
**Date:** 2026-05-27  
**Owner:** Chief Information Security Officer  
**Repository Path:** `dev-security/claude-rules/README.md`  
**Classification:** Public  
**Licence:** CC0 1.0 Universal

---

## What Are These Files?

The `claude-rules/` directory contains a set of Markdown files designed to be loaded into [Claude Code](https://docs.anthropic.com/en/docs/claude-code) sessions as security context. When Claude Code reads these files — either via a `CLAUDE.md` in your project root or via explicit `/add-files` — they encode security and compliance requirements as persistent context that the AI coding assistant applies during development.

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
│   └── owasp.md                OWASP Top 10 and ASVS alignment rules
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
    └── csharp.md                C# / .NET security patterns
```

---

## How to Use

### Option 1: Copy CLAUDE.md to Your Project Root

The simplest approach. Copy `CLAUDE.md` into your project root. Claude Code will automatically read it at session start. It imports the most critical rules across all categories.

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

---

## External References

These rules draw on and reference the following external projects and standards:

- **OWASP Top 10** — Most critical web application security risks
- **OWASP LLM Top 10** — Most critical risks for LLM applications
- **OWASP ASVS** — Application Security Verification Standard
- **OWASP Cheat Sheet Series** — Developer-focused security implementation guides
- **MITRE ATLAS** — Adversarial threat landscape for AI systems
- **NIST AI RMF** — AI risk management framework
- **NIST SSDF (SP 800-218)** — Secure Software Development Framework
- **TikiTribe** — Open-source AI agent security testing utilities; adversarial prompt libraries and agentic workflow attack surface tools; used for MCP server security testing, tool-call injection resistance verification, and multi-agent trust boundary validation
- **CSA CCM v4** — Cloud Controls Matrix
- **CSA AICM v1** — AI Controls Matrix

---

## Licence

All content in this directory is released under CC0 1.0 Universal. Copy, modify, and redistribute freely.

---

**End of Document**
