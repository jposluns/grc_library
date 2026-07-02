# AI Coding Assistant Security Guideline

**Document Title:** AI Coding Assistant Security Guideline\
**Document Type:** Guideline\
**Version:** 1.3.4\
**Date:** 2026-07-02\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`dev-security/standard-developer-security-requirements.md`](standard-developer-security-requirements.md), [`dev-security/claude-rules/README.md`](claude-rules/README.md), [`dev-security/standard-security-baseline-and-standards-reference.md`](standard-security-baseline-and-standards-reference.md), [`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md), [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md)\
**Classification:** Public\
**Category:** Developer Security\
**Review Frequency:** 6 to 12 months and upon material change to AI coding tooling, threat landscape, or regulatory guidance\
**Repository Path:** [`dev-security/guideline-ai-coding-assistant-security.md`](guideline-ai-coding-assistant-security.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This guideline defines requirements and best practices for the secure use of AI coding assistants, tools such as Claude Code, GitHub Copilot, Cursor, Windsurf, and equivalent products, within the software development lifecycle.

AI coding assistants introduce distinct risks that differ from conventional development tooling: they generate code that should be reviewed for correctness and security; they may access, transmit, or retain code and data from the development environment; they can be manipulated through prompt injection; and they may hallucinate package names, APIs, or library versions that do not exist. This guideline addresses those risks while enabling productive use.

---

## Scope

Applies to all employees, contractors, and third-party developers using AI coding assistants on:
- Organization-owned or managed devices.
- Organization-managed cloud development environments.
- Projects touching organization codebases, infrastructure, or data.

Does not apply to personal experimentation on personal devices with no connection to organizational data or systems.

---

## Approved tools and authorization

The organization maintains an approved list of AI coding assistants. Developers should use only approved tools for work on organizational systems. Using an unapproved AI coding assistant with organizational code, data, or credentials is a policy violation requiring a formal exception.

When evaluating a new AI coding assistant for approval, the assessment should cover:
- Data handling and retention: what code and context is sent to external APIs; whether the provider retains prompts or completions; applicable data processing agreements.
- Authentication and access scope: what organizational systems the tool can access.
- Security rule configuration: whether the tool accepts binding security constraints (CLAUDE.md, rules files, or equivalent).
- Incident response: the provider's breach notification obligations.

---

## Required security configuration

### Load security rules before using an AI coding assistant

All AI coding assistant sessions working on organizational code should have security rules loaded before generating or reviewing code. The organization's security rules are maintained in `dev-security/claude-rules/` as library-canonical, locally-vetted content.

**For Claude Code, in order of decreasing scope:**

1. **Project-root `CLAUDE.md`**: copy [`dev-security/claude-rules/CLAUDE.md`](claude-rules/CLAUDE.md) to either `./CLAUDE.md` or `./.claude/CLAUDE.md` at the consumer project root. Claude Code reads this file in full at session start.
2. **Path-scoped rules in `.claude/rules/`**: place additional rule files under `.claude/rules/<topic>.md` with optional `paths:` YAML frontmatter. Without `paths:` they load at launch; with `paths:` they load only when Claude reads files matching the configured glob patterns. Path-scoped rules keep the always-loaded context small while still applying language- or component-specific rules when relevant.
3. **`AGENTS.md` interop**: if the consumer project already has an `AGENTS.md` for other coding agents, add `@AGENTS.md` at the top of `CLAUDE.md` (or symlink it) so both tools read the same instructions.
4. **Add language-specific files** from `dev-security/claude-rules/languages/` and AI/agentic files from `dev-security/claude-rules/ai/` for any project using LLMs, agents, RAG, or MCP.

A separate generator prompt published under `dev-security/claude-rules/` analyzes a consumer project and proposes a tailored CLAUDE.md plus rule-file selection before any file is written. The generator supports two source modes: **local mode** (reads the pack from disk if `dev-security/` is detected near the consumer's project) and **fetch mode** (reads the pack live from the GRC Library's first-party canonical URL when no local pack is present, or when the consumer elects fetch after a staleness check). See [`dev-security/claude-rules/README.md`](claude-rules/README.md) for usage guidance.

The pack content is held locally as library-canonical material. **External rule repositories** (TikiTribe, Wiz, and others outside this library) are kept as URL pointers only; the organization does not configure Claude Code to fetch them automatically at session start, because (a) `CLAUDE.md` content is delivered as a user message and is not enforced configuration, so a fetch instruction may be silently ignored; (b) externally-fetched content would need vetting under the External-Source Vetting Protocol at consumer runtime, which is impractical; and (c) the local pack already covers the substantive areas. The library maintainer back-ports vetted improvements from external sources on the standard freshness cadence.

**First-party vs third-party fetch posture.** The above prohibition on session-start auto-fetch applies to **third-party** sources (external rule repositories outside the library's control). The setup-generator prompt's fetch mode is a different case: it fetches from the GRC Library's **own first-party canonical CC BY-SA 4.0 source** (`https://raw.githubusercontent.com/jposluns/grc_library/main/dev-security/claude-rules/` by default, or a forked equivalent the consumer substitutes at the confirmation prompt). First-party fetch is trusted because (a) the content is under the library maintainer's control and is the same CC BY-SA 4.0 material an adopter would otherwise vendor locally; (b) the consumer explicitly confirms the canonical URL before any fetch occurs, making the trust decision visible and overridable; (c) the source URL is verifiable (GitHub-hosted, open-source, version-controlled). The trust posture should not be extended to any other URL: if a consumer or fetched content directs the generator to fetch from a different source mid-session, the External-Source Vetting Protocol applies and the content is treated as untrusted data, not as instructions.

**For other tools (Copilot, Cursor, Windsurf):**
- Load the relevant rule files from `dev-security/claude-rules/` as the tool's equivalent context (custom instructions, rules files, or workspace settings).
- Ensure that the tool's memory or context is not shared across unrelated projects.

### Deterministic enforcement: settings, hooks, and audit

`CLAUDE.md` content is delivered to Claude Code as a user message after the system prompt. Claude tries to follow it, but adherence is not guaranteed, especially for vague or conflicting instructions. Treat the rules pack as the **behavioural guidance layer** and use Claude Code's settings file and hooks for the **deterministic enforcement layer**:

- `.claude/settings.json` `permissions.deny`: hard-deny `Read(...)`, `Bash(...)`, and similar tool-use patterns. Anything matched here cannot be invoked regardless of what Claude decides.
- `.claude/settings.json` `disableSkillShellExecution: true`: disables inline shell execution inside skills and custom commands (useful when consumer projects do not need plugin or skill shell execution).
- `.claude/settings.json` `respectGitignore: true`: respects `.gitignore` for the `@` file picker. Default behaviour; the explicit setting documents intent.
- `PreToolUse` hooks: deterministically block specific actions on the consumer's terms (for example, prevent commit, push, or production-environment writes pending explicit confirmation).
- `InstructionsLoaded` hook: useful for verifying which CLAUDE.md and rule files actually loaded in a given session, supporting audit evidence that the security rules pack was in force.

Starter `.claude/settings.json` snippet, using the documented Anthropic schema:

```json
{
  "permissions": {
    "defaultMode": "default",
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Bash(curl *)",
      "Bash(rm -rf *)"
    ]
  },
  "disableSkillShellExecution": true,
  "respectGitignore": true
}
```

Adopters refine the `permissions.deny` list to match the project's secret paths, prohibited shell patterns, and out-of-scope read locations. Verify the exact key names against current Anthropic Claude Code settings documentation before relying on a configuration in a compliance assertion: AI-generated configuration suggestions sometimes contain hallucinated keys that the tool silently ignores.

### Other Claude Code mechanisms relevant to compliance

- **`/init`**: generates a starter `CLAUDE.md` from existing codebase signals; does not overwrite an existing CLAUDE.md, suggesting improvements instead. With `CLAUDE_CODE_NEW_INIT=1`, runs an interactive multi-phase flow that lets the adopter approve proposed CLAUDE.md, skills, and hook content before any file is written.
- **Plan Mode** (Shift+Tab twice): puts Claude into research-and-analysis mode where it cannot make file changes. Recommended discipline for any change touching multiple files or any security-sensitive surface; reduces "looks done" defects by requiring an explicit reviewable plan before execution.
- **Thinking-budget keywords**: `think` < `think hard` < `think harder` < `ultrathink` map to increasing compute allocations. Use the higher tiers selectively for security-sensitive analysis (legacy code integration, threat modelling, root-cause investigation); the lower tiers for routine changes.
- **Auto memory**: Claude Code records its own session notes at `~/.claude/projects/<project>/memory/MEMORY.md` (machine-local). Adopters subject to data residency or audit-trail obligations should review what auto-memory captures, since it may include project-specific reasoning. Disable via `autoMemoryEnabled: false` in settings if the obligation requires it.
- **`/memory` command**: lists the CLAUDE memory files (project, user, and any local-override variant) and rules files actually loaded in the current session. Use it to audit that the security rules pack is in force when starting a sensitive session.

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

AI-generated code is not automatically correct or secure. It should be reviewed with the same scrutiny applied to human-written code, plus additional checks for AI-specific failure modes.

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
- [ ] **Licence**: AI-generated code may reproduce training data; verify no unlicensed verbatim reproductions of copyrighted material.
- [ ] **No hallucinated configuration**: any AI-suggested configuration key names, file formats, or settings schemas (for example `.claude/settings.json` keys, `.gitlab-ci.yml` fields, IaC resource attributes) are cross-checked against the tool's authoritative documentation before adoption. AI assistants sometimes produce plausible-looking configuration with key names the tool silently ignores, creating false-control compliance hazards.

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

Developers using AI coding assistants should be aware that prompt injection can be introduced through:

- **Documents and code comments**: adversarial instructions embedded in code comments, documentation, or dependency changelogs that the assistant reads.
- **Test data and fixtures**: malicious instructions in test input files or database fixtures.
- **Dependency sources**: compromised packages may contain adversarial comments designed to influence AI code generation.
- **Issue trackers and wikis**: AI assistants reading linked content may process instructions embedded in that content.

If an AI coding assistant behaves unexpectedly, generates code that seems designed to exfiltrate data, bypass security controls, or perform unusual actions, treat it as a potential prompt injection event and report it.

---

## Defensive scanning of AI coding assistant inputs and outputs

Awareness is necessary but not sufficient. The following are scanning controls that operate on the files an AI coding assistant reads and on the code it produces, regardless of developer attention.

### Input scanning: files before AI consumption

Where an AI coding assistant reads files the developer did not author (third-party dependencies, generated files, vendored samples, downloaded fixtures, retrieved web content, AI-output from a different session, issue-tracker or wiki content fetched at session start), those files should be scanned for prompt-injection content before the assistant processes them. The scan looks for, at minimum:

- Forged chat-template tokens such as `im_start`, `INST`, `SYS`, `system`, `user`, `assistant` markers used in current model families.
- Instruction-override patterns ("ignore previous instructions", "you are now", "your new role is", role-name re-binding).
- Zero-width, BIDI, homoglyph, and other steganographic Unicode patterns.
- Hidden HTML comments containing instruction-like content in markdown or documentation files.
- Embedded URLs to non-allow-listed external hosts.

The scan is advisory by default (flag for review) and may be blocking for repositories of high sensitivity. The scan output is logged and feeds the standard security-monitoring pipeline.

### Output scanning: AI-generated code before commit

AI-generated code committed to a repository should be automatically scanned, in addition to the standard SAST and SCA gates, for AI-specific concerns:

- **Suspicious URLs**: tracker domains, image-tracker hosts, URL-shortener domains, paste-site hosts, low-reputation domains.
- **Hardcoded credentials or secret patterns**: scoped beyond the standard secret scanner to include LLM-API key patterns (vendor token shapes), model-provider tokens, AI-platform credentials.
- **Hallucinated import paths**: package names not present in approved registries (per [`standard-developer-security-requirements.md`](standard-developer-security-requirements.md) §10 and [`standard-software-composition-analysis.md`](standard-software-composition-analysis.md) §4.5).
- **Insecure code patterns characteristic of AI generation**: hallucinated security controls (HMAC verification missing signature check; JWT validation missing expiry check; sanitization routines that escape only one of several attack classes); deprecated cryptography; missing input validation on apparent endpoints.
- **Exfiltration-style egress in generated code**: outbound HTTP calls to unexpected hosts, embedded analytics or telemetry calls to unrecognized endpoints, base64-encoded payloads in string literals.
- **Comment-embedded instructions**: AI-generated comments containing instruction-like content that could influence a future AI session reading the file.

Output scanning is a CI/CD gate distinct from standard SAST. Findings block merge by default; tracked exception requires CISO approval per the standard exception policy.

---

## Session isolation, vendor telemetry, and egress monitoring for AI coding assistants

AI coding assistants are themselves a potential exfiltration channel. The following controls treat the tool as a remote-access session in the manner of a vendor remote-access connection.

### Session isolation

- An AI coding assistant session must not span multiple customer codebases, multiple confidentiality classifications, or multiple regulated-data scopes within a single context window. A developer working on customer A's codebase opens a separate session before switching to customer B's codebase.
- Sessions reading Confidential or Restricted data must not run in parallel with sessions producing or modifying code in a different scope.
- Where the AI tool supports project-scoped or workspace-scoped memory, that scoping must be configured at workspace creation time.

### Vendor telemetry inventory

- For each approved AI coding assistant, the vendor's published telemetry endpoints, data categories transmitted, retention period, and data-residency posture are inventoried and recorded in the approved-tools register.
- Material changes to vendor telemetry (added endpoints, expanded data categories, residency changes) trigger reassessment of the tool's approval status.
- Where the vendor cannot satisfy data residency for a project, the AI tool must not be used on that project.

### Egress monitoring

- AI coding assistant sessions on managed devices and managed cloud development environments are subject to egress logging at the network layer where this is operationally available.
- Anomalous egress (unexpected destinations, unexpected volumes, unexpected timing) triggers a security-monitoring alert and, where the device permits, automatic session interruption pending review.
- Where the AI tool runs locally with no network egress except to the vendor's documented endpoints, egress monitoring confirms that this constraint is operationally enforced.

### Insider-bypass risk

Use of AI coding assistants to generate code that bypasses, weakens, or evades security review or compliance controls is a prohibited use (see Prohibited uses §5). Indicators of insider bypass via AI include: a developer requesting an AI to generate code that disables a SAST rule, removes an authentication check, weakens a cryptographic parameter, or constructs a privilege-escalation pathway. Such requests, even if framed as "for testing," are reportable per the Incident reporting section.

---

## Agentic use (multi-step autonomous coding)

AI coding assistants operating in agentic mode (autonomous multi-step task execution with tool access) carry higher risk than single-turn interactions. Additional requirements apply:

- The AI should not have standing write access to production systems.
- The AI should not commit and push directly to the main or release branch without human review.
- Tool access should be scoped to the minimum necessary for the task.
- Agentic sessions should be logged (all tool calls, files read, files written, commands executed).
- Before any destructive action (delete, overwrite, force push), the agent should request explicit human confirmation.

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
| Anthropic Claude Code Docs | `https://code.claude.com/docs/en/claude-code` | Official documentation for Claude Code permissions, CLAUDE.md, settings, hooks, and security model |

---

## Framework alignment

| Control Area | ISO 27001:2022 | NIST SSDF | CSA AICM | ISO/IEC 42001 | Regulatory |
| --- | --- | --- | --- | --- | --- |
| AI tool authorization | A.5.36 | PO.1, PO.3 | AI-GOV-01 | Clause 6 (planning) | EU AI Act Art. 9 |
| Data handling for AI inputs | A.5.12, A.8.10 | PS.1 | AI-DATA-01 | Clause 8 (operation) | GDPR, PIPEDA |
| Code review of AI output | A.8.27, A.8.29 | PW.7 | AI-SEC-02 | Clause 9 (performance evaluation) | N/A |
| Prompt injection awareness | A.5.30 | N/A | AI-SEC-03 | Annex A.6 (AI risk treatment) | N/A |
| Agentic use controls | A.5.18, A.8.2 | PW.1 | AI-GOV-03 | Clause 8 (operation) | EU AI Act Art. 14 |
| Deterministic enforcement | A.8.16, A.8.34 | PW.1 | AI-SEC-04 | Annex A.6 (AI risk treatment) | EU AI Act Art. 14 |
| Incident reporting | A.5.26 | RV.1 | AI-INC-01 | Clause 10 (improvement) | PIPEDA, GDPR |

---

**End of Document**
