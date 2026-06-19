# Claude Code Security Rules: Usage Guide

**Document Title:** Claude Code Security Rules Usage Guide\
**Document Type:** Guideline\
**Version:** 1.20.2\
**Date:** 2026-06-19\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`dev-security/standard-developer-security-requirements.md`](../standard-developer-security-requirements.md), [`dev-security/standard-devops-security-requirements.md`](../standard-devops-security-requirements.md), [`dev-security/guideline-ai-coding-assistant-security.md`](../guideline-ai-coding-assistant-security.md), [`ai/standard-ai-and-agentic-development-security.md`](../../ai/standard-ai-and-agentic-development-security.md)\
**Repository Path:** [`dev-security/claude-rules/README.md`](README.md)\
**Classification:** Public\
**Category:** Developer Security\
**Review Frequency:** 6 to 12 months and upon material threat, tooling, or framework change\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## What are these files?

The `claude-rules/` directory contains a set of Markdown files designed to be loaded into [Claude Code](https://code.claude.com/docs/en/claude-code) sessions as security and development-governance context. When Claude Code reads these files, either via a `CLAUDE.md` in your project root, via `.claude/rules/*.md` files with optional path-scoped frontmatter, or via explicit `/add-files`, they encode security, compliance, and development-governance requirements as persistent context that the AI coding assistant applies during development.

These are **draggable rule files**: copy any subset into your project's Claude Code context and Claude will apply those security and governance requirements to code it writes, reviews, and suggests.

---

## Pack scope

Historically this pack covered security and compliance only. As of pack version 1.6.0 (Library 2026.05.139, 2026-06-01), the pack's contract broadened to cover both:

1. **Security and compliance** (original and largest scope). Hardcoded-secrets prevention, input validation, cryptography, authentication, OWASP/ASVS alignment, AI/agent/MCP/RAG security, CI/CD pipeline gates, language-specific security patterns. This content lives under `core/`, `ai/`, `pipeline/`, and `languages/`.
2. **Development-governance discipline** (expanding scope). Rules that govern how an AI coding assistant collaborates on a governed codebase: gate discipline (never weaken a check to silence a failure; fix the artefact), change-tracking discipline (CHANGELOG-on-PR with explicit opt-out trailers), evidence-grounded completion (no completion claims without enumerated, re-read, quoted, contradiction-searched evidence), clarify-before-acting on ambiguous requests, and artefact-and-branch discipline (no direct push to protected branches; version-monotonicity contract; never hand-edit generated artefacts). This content lives under the `governance/` subdirectory and is being delivered in a phased rollout. Pack version 1.7.0 (Library 2026.05.140) shipped [`governance/gate-discipline.md`](governance/gate-discipline.md); pack version 1.8.0 (Library 2026.05.141) shipped [`governance/change-tracking.md`](governance/change-tracking.md); pack version 1.9.0 (Library 2026.05.142) shipped [`governance/evidence-grounded-completion.md`](governance/evidence-grounded-completion.md); pack version 1.10.0 (Library 2026.05.143) shipped [`governance/clarify-before-acting.md`](governance/clarify-before-acting.md); pack version 1.11.0 (Library 2026.05.144) ships [`governance/artefact-and-branch-discipline.md`](governance/artefact-and-branch-discipline.md). With this release the phased governance rollout announced at pack version 1.6.0 is complete.

Pack version 1.20.0 (Library 2026.06.20) introduces a third pack-content type: **Claude Code Skills** in the `SKILL.md` workflow format, under the `skills/` subdirectory. Skills are derived from selected governance rules and are consumed by Claude Code's Skill tool (discovered by YAML frontmatter `name:` and `description:`), distinct from the rule files which are loaded as session-start context. The first three skills are [`skills/evidence-grounded-completion/SKILL.md`](skills/evidence-grounded-completion/SKILL.md), [`skills/gate-discipline-diagnose/SKILL.md`](skills/gate-discipline-diagnose/SKILL.md), and [`skills/clarify-before-acting/SKILL.md`](skills/clarify-before-acting/SKILL.md), each derived from the corresponding governance rule with the rule remaining as the source of truth for normative content (framework alignment, exception handling, rationale); the skill is the workflow wrapper (when to invoke, what steps in what order, what verification confirms completion).

The pack remains under `dev-security/` in the parent library because the discoverability assumption is that developers (and their AI agents) shop for *"security rules"*, not for *"GRC rules"* or *"development discipline"*. The directory name is the shelf label; this README is the table of contents and articulates the broader scope. If a future scope expansion outgrows this framing, the directory name will be revisited at that time, not pre-emptively.

---

## Directory structure

```text
claude-rules/
├── README.md                   This file
├── CLAUDE.md                   Root file: drag this into a project for full coverage
├── setup-generator-prompt.md   AI-assisted setup generator prompt for downstream consumers
├── vetting-log.md              Maintainer vetting log for the external rule sources referenced below
├── core/                       Security and compliance rules (secrets, auth, input validation, crypto, OWASP)
│   ├── secrets.md              Never hardcode credentials, keys, or tokens
│   ├── authentication.md       Secure authentication and session requirements
│   ├── input-validation.md     Input validation and output encoding
│   ├── cryptography.md         Approved algorithms and key handling
│   └── owasp.md                OWASP Top 10:2025 and ASVS v5 alignment rules
├── governance/                 Development-governance discipline (rollout complete at pack 1.11.0)
│   ├── gate-discipline.md                  Never weaken a gate to silence a failure; fix the artefact
│   ├── change-tracking.md                  CHANGELOG-on-PR by default; documented opt-out trailer for genuine exceptions
│   ├── evidence-grounded-completion.md     No completion claim without enumerated, re-read, quoted, contradiction-searched evidence
│   ├── clarify-before-acting.md            Surface ambiguity in one sentence and ask; never silently pick
│   └── artefact-and-branch-discipline.md   Generated artefacts are read-only; protected branches are append-only
├── ai/
│   ├── ai-security.md          LLM and AI application security requirements
│   ├── agent-security.md       Agentic workflow security and trust boundaries
│   ├── rag-security.md         Retrieval-augmented generation data controls
│   └── mcp-security.md         Model Context Protocol server security rules
├── pipeline/
│   └── cicd-gates.md           CI/CD security gates and pipeline controls
├── skills/                     Claude Code Skills (SKILL.md format) derived from selected pack rules
│   ├── evidence-grounded-completion/SKILL.md   Six-step verification protocol before any completion claim
│   ├── gate-discipline-diagnose/SKILL.md       Diagnose-then-fix-the-artefact response to a failing gate
│   └── clarify-before-acting/SKILL.md          One-sentence ambiguity surfacing with named alternatives
└── languages/
    ├── python.md                Python-specific security patterns and anti-patterns
    ├── typescript.md            TypeScript / Node.js security patterns
    ├── csharp.md                C# / .NET security patterns (server-side)
    ├── java.md                  Java / Spring security patterns (server-side)
    ├── go.md                    Go security patterns
    ├── swift.md                 Swift / iOS (and Objective-C) mobile security patterns
    ├── kotlin.md                Kotlin / Android (and Java for Android) mobile security patterns
    ├── react-native.md          React Native (with or without Expo) cross-platform mobile security patterns
    ├── flutter.md               Flutter / Dart cross-platform mobile security patterns
    ├── dotnet-maui.md           .NET MAUI (and Blazor Hybrid) cross-platform mobile security patterns
    └── capacitor-ionic.md       Capacitor / Ionic (WebView-based hybrid) cross-platform mobile security patterns
```

---

## How to use

### Option 1: copy claude.md to your project root

The simplest approach. Copy `CLAUDE.md` into your project root at either `./CLAUDE.md` or `./.claude/CLAUDE.md`. Claude Code reads it in full at session start.

```bash
cp path/to/claude-rules/CLAUDE.md ./CLAUDE.md
```

### Option 2: selective rule files

Copy only the rule files relevant to your project into `.claude/rules/`:

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

### Option 3: add to existing claude.md

Copy the content of specific rule files into your existing `CLAUDE.md` under a `## Security Requirements` heading.

### Option 4: path-scoped rules (most context-efficient)

Place rule files in `.claude/rules/` with optional `paths:` YAML frontmatter so Claude Code loads them only when reading matching files. Rules without `paths:` load at launch; rules with `paths:` load conditionally:

```markdown
---
paths:
  - "src/**/*.py"
  - "tests/**/*.py"
---

# Python security rules
(content from claude-rules/languages/python.md)
```

This is the "L4 abstracted" pattern: language-specific or component-specific rules apply only when relevant, keeping the always-loaded `CLAUDE.md` lean.

### AGENTS.md interop

If your project already has an `AGENTS.md` for other coding agents (Codex, Cursor, OpenCode, Zed), add `@AGENTS.md` at the top of `CLAUDE.md`, or symlink one to the other, so both tools read the same instructions without duplicating content.

---

## Rule files and their scope

| File | When to Use |
| --- | --- |
| [`core/secrets.md`](core/secrets.md) | All projects. No exceptions. |
| [`core/authentication.md`](core/authentication.md) | Any project with user login, service accounts, or APIs |
| [`core/input-validation.md`](core/input-validation.md) | Any project processing external input |
| [`core/cryptography.md`](core/cryptography.md) | Any project storing data, using passwords, or transmitting data |
| [`core/owasp.md`](core/owasp.md) | Web applications and APIs (covers OWASP Top 10) |
| [`ai/ai-security.md`](ai/ai-security.md) | Any project using LLMs, AI APIs, or AI-generated content |
| [`ai/agent-security.md`](ai/agent-security.md) | Agentic systems, multi-agent workflows, autonomous task execution |
| [`ai/rag-security.md`](ai/rag-security.md) | Retrieval-augmented generation (RAG) systems |
| [`ai/mcp-security.md`](ai/mcp-security.md) | Projects building or consuming MCP servers |
| [`pipeline/cicd-gates.md`](pipeline/cicd-gates.md) | DevOps/platform engineers configuring CI/CD |
| [`governance/gate-discipline.md`](governance/gate-discipline.md) | Any project with CI gates, audit programmes, or branch protections (i.e., all of them) |
| [`governance/change-tracking.md`](governance/change-tracking.md) | Any project with a CHANGELOG (or that should have one); especially projects with downstream consumers who need to read change history |
| [`governance/evidence-grounded-completion.md`](governance/evidence-grounded-completion.md) | Any project where an AI coding assistant participates (because the failure mode this rule prevents is dominant for AI assistants); doubly relevant for projects with audit programmes that gate completion claims |
| [`governance/clarify-before-acting.md`](governance/clarify-before-acting.md) | Any project where an AI coding assistant participates; especially projects with multiple active branches, conventions that vary by request type, or trade-offs the user reasonably wants to weigh in on |
| [`governance/artefact-and-branch-discipline.md`](governance/artefact-and-branch-discipline.md) | Any project with generated artefacts (build outputs, schema dumps, taxonomies, doc portals, lockfiles) or protected branches with branch-protection rules; doubly relevant for projects with version-monotonicity contracts |
| [`languages/python.md`](languages/python.md) | Python codebases |
| [`languages/typescript.md`](languages/typescript.md) | TypeScript / Node.js codebases |
| [`languages/csharp.md`](languages/csharp.md) | C# / .NET codebases |
| [`languages/java.md`](languages/java.md) | Java / Spring Boot codebases |
| [`languages/go.md`](languages/go.md) | Go codebases |
| [`languages/swift.md`](languages/swift.md) | iOS applications written in Swift or Objective-C; implements the iOS-specific controls of [`standard-mobile-application-security.md`](../standard-mobile-application-security.md) |
| [`languages/kotlin.md`](languages/kotlin.md) | Android applications written in Kotlin or Java; implements the Android-specific controls of [`standard-mobile-application-security.md`](../standard-mobile-application-security.md) |
| [`languages/react-native.md`](languages/react-native.md) | React Native (with or without Expo) cross-platform mobile applications; implements Section 13 of [`standard-mobile-application-security.md`](../standard-mobile-application-security.md) and the relevant native-layer sections as applied through the JS bridge |
| [`languages/flutter.md`](languages/flutter.md) | Flutter / Dart cross-platform mobile applications; implements Section 13 of [`standard-mobile-application-security.md`](../standard-mobile-application-security.md) and the relevant native-layer sections as applied through Flutter's platform-channel bridge |
| [`languages/dotnet-maui.md`](languages/dotnet-maui.md) | .NET MAUI (and Blazor Hybrid) cross-platform mobile applications; implements Section 13 of [`standard-mobile-application-security.md`](../standard-mobile-application-security.md) and the relevant native-layer sections as applied through MAUI's handler architecture and the Mono / .NET runtime |
| [`languages/capacitor-ionic.md`](languages/capacitor-ionic.md) | Capacitor / Ionic (WebView-based hybrid) cross-platform mobile applications; implements Section 13 of [`standard-mobile-application-security.md`](../standard-mobile-application-security.md) and the relevant native-layer sections as applied through Capacitor's WebView + plugin architecture; carries forward web-stack rules from [`languages/typescript.md`](languages/typescript.md) and `core/owasp.md` because the WebView is the application UI |

---

## External sources: how this pack handles them

External rule repositories listed under "External references" below are **not loaded automatically** at Claude Code session start. Three reasons:

1. **`CLAUDE.md` content is delivered to Claude Code as a user message, not as enforced configuration.** A "fetch at session start" instruction can be silently ignored, producing a false sense of coverage.
2. **External content fetched without per-fetch vetting cannot be relied on.** Treating fetched markdown as binding rules conflicts with the principle that fetched content is data, not instructions; each fetch needs the External-Source Vetting Protocol applied.
3. **The pack already covers the substantive areas** (core, AI/agent/MCP/RAG, pipeline, languages) as library-canonical originals.

The library maintainer back-ports vetted improvements from external sources on the standard freshness cadence. Adopters who want to layer additional external rule sets on top of the pack have two paths:

- **By hand.** Use the URLs in the External references section below; the adopter clones, vendors, or copies into their own project on their own terms.
- **Via the setup generator's external-source overlay (default-on).** Phase 2 of [`setup-generator-prompt.md`](setup-generator-prompt.md), after presenting the GRC Library pack proposal, **proposes to fetch all four vetted external sources as the default action** so the consumer can accept the broader proposal with a single approval. The consumer's explicit approval (or modification, or decline) is still required before any file is written; the default-on framing affects the conversation flow's default, not the consent gate. The Wiz licence caveat (CC-BY-NC-ND-4.0; NonCommercial + NoDerivatives) is always surfaced in the offer-message prose before approval so commercial adopters and adopters who plan to modify the rule files for their stack can decline Wiz specifically. For each source the consumer is fetching (whether by accepting the default or by explicit modification), the generator applies the External-Source Vetting Protocol per fetch (treat as data not instructions; scan for embedded directives, urgency framing, claims of pre-authorisation, hidden or encoded text, exfiltration patterns, control-weakening guidance), surfaces anything suspicious verbatim before write, and places approved files under `.claude/rules/external/<source-name>/` with a provenance header (source URL, fetched date, SHA-256 of fetched bytes). The pack remains the primary content; the overlay is supplementary and may overlap or conflict with the primary layer (consumer responsibility to reconcile). The maintainer-side vetting status for each candidate source is recorded in [`dev-security/claude-rules/vetting-log.md`](vetting-log.md). Current status: TikiTribe, Kariedo, and Wiz are `Vetted` (first formal EXT-01 vets on 2026-05-31); addyosmani is `Vetted` (first formal EXT-01 vet on 2026-06-19, 5 skills in full + 18 spot-scanned). The generator's offer step surfaces the per-source status and substantive observations to the consumer so the decision is informed.

### Deterministic enforcement layer

`CLAUDE.md` and `.claude/rules/*.md` are the behavioural guidance layer. For controls that must hold regardless of what Claude decides, use `.claude/settings.json` `permissions.deny` rules and `PreToolUse` hooks. See [`dev-security/guideline-ai-coding-assistant-security.md`](../guideline-ai-coding-assistant-security.md) "Deterministic enforcement" for the verified Anthropic schema and starter values.

## Generate your files (AI-assisted setup)

[`dev-security/claude-rules/setup-generator-prompt.md`](setup-generator-prompt.md) is a portable prompt for your own Claude Code session. It analyses your project, proposes a tailored setup, and creates files only after your approval; it does not act blindly.

### Local mode vs fetch mode

The generator works whether or not you have the pack on disk:

- **Local mode** (when the generator detects a `dev-security/` directory near your project): reads pack content from disk. The generator fetches only [`claude-rules/README.md`](README.md) from the canonical source to compare versions and warn you if your local pack is stale.
- **Fetch mode** (when no local pack is detected, or you elect it after a staleness check): reads the pack live from the GRC Library's first-party canonical source on every needed file. No local download required. **Default canonical URL prefix**: `https://raw.githubusercontent.com/jposluns/grc_library/main/dev-security/claude-rules/`. The generator asks you to confirm or substitute this URL before any fetch, so the trust decision is explicit. If you have forked the GRC Library to your own org, substitute your fork's URL at the confirm prompt.

### Three ways to invoke

Pick whichever fits your workflow.

**Form 1: manual paste (most conservative)**. Open [`setup-generator-prompt.md`](setup-generator-prompt.md) on GitHub, click the **Raw** button, select all, copy, paste into Claude Code as your first message. You see every word of the prompt before any action.

**Form 2: one-line `curl` to clipboard (recommended for terminal users)**. Pulls the prompt's raw content directly to your clipboard, then paste it into Claude Code.

```bash
# macOS
curl -fsSL https://raw.githubusercontent.com/jposluns/grc_library/main/dev-security/claude-rules/setup-generator-prompt.md | pbcopy

# Linux (X11 + xclip)
curl -fsSL https://raw.githubusercontent.com/jposluns/grc_library/main/dev-security/claude-rules/setup-generator-prompt.md | xclip -selection clipboard

# Linux (Wayland + wl-copy)
curl -fsSL https://raw.githubusercontent.com/jposluns/grc_library/main/dev-security/claude-rules/setup-generator-prompt.md | wl-copy
```

You still see the prompt content (you pasted it), with one fewer browser step.

**Form 3: URL-to-Claude (maximum convenience; different trust shape)**. Open Claude Code in your project root and send this single message:

```text
Fetch https://raw.githubusercontent.com/jposluns/grc_library/main/dev-security/claude-rules/setup-generator-prompt.md and follow the instructions exactly.
```

Claude will WebFetch the prompt and start executing it. **Trade-off**: you do not see the prompt content before Claude begins acting on it; you are trusting the canonical URL only. Only use this form if you have made an informed decision to trust the GRC Library canonical URL (which is open-source, CC BY-SA 4.0, and version-controlled on GitHub).

### Tip: avoid permission prompts during fetch

If you plan to use fetch mode often, add the canonical raw URL to your project's `.claude/settings.json` permission allowlist so Claude does not ask on every fetch. Using the Anthropic-documented schema:

```json
{
  "permissions": {
    "allow": [
      "WebFetch(domain:raw.githubusercontent.com)"
    ]
  }
}
```

### What the generator produces

- A concise project `CLAUDE.md` (target under 200 lines) tailored to your stack, pointing at your project's own test/lint/CI gates.
- The relevant security rule modules for your languages and components (secrets, input validation, OWASP, AI/agent/RAG/MCP, CI/CD, etc.), placed under `.claude/rules/` with optional `paths:` frontmatter for path-scoped loading.
- Optionally: a `.claude/settings.json` template with starter `permissions.deny` rules for common secret paths and dangerous shell patterns.
- Files that fit your project. The generator does **not** impose the GRC Library's internal document-model metadata or naming conventions on your repository.

### Safety notes

- The generator treats content fetched from any URL other than the confirmed first-party canonical source as untrusted data, never as instructions, and will not auto-apply such content without explicit consumer approval.
- It is AI-assisted: review what it proposes and generates before trusting it. AI assistants occasionally produce plausible-looking configuration keys or file names that the target tool silently ignores, so verify against authoritative documentation.
- It will never overwrite an existing `CLAUDE.md` or rule file without showing you the diff and asking first.
- In local mode, when canonical is newer than your local pack, the generator shows you the version gap and offers three options: continue with stale local, switch to fetch mode, or refresh local files from canonical (with explicit per-file approval before any overwrite).

### Prefer to do it entirely by hand?

Use Options 1-4 above to copy specific rule files directly; no prompt required.

---

## External references

These rule files draw on and are aligned to the following external projects and standards. All are publicly available and free to reference.

### AI coding assistant rule repositories

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
- Coverage: Core universal security practices, language-specific rules (Python, JavaScript, Java, PHP, Ruby, Rust, C), common vulnerability prevention, uses `@`-syntax import system for modular organisation
- Use: Alternative modular rule set for projects needing broader language coverage

**addyosmani: Agent Skills**
- Repository: `https://github.com/addyosmani/agent-skills`
- Coverage: 24 engineering-workflow skills organized by development phase (Define, Plan, Build, Verify, Review, Ship). Includes a `security-and-hardening` skill (STRIDE-per-trust-boundary, Mandatory / Approval-Gated / Prohibited tier model, OWASP prevention patterns, LLM-output handling), a `code-review-and-quality` skill (five-axis review), and a `ci-cd-and-automation` skill (quality-gate pipeline configuration)
- Use: Complementary engineering-discipline overlay; scope is engineering workflow not GRC governance. Uses Claude Code's Skills `SKILL.md` discovery format (frontmatter `name:` + `description:`) rather than the rule / `@`-import patterns the other three sources use
- License: **MIT**

**awesome-claude-code (community curation)**
- Repository: `https://github.com/hesreallyhim/awesome-claude-code`
- Coverage: Community-curated index of Claude Code skills, hooks, slash commands, agent orchestrators, applications, and plugins
- Use: Discovery resource for additional skills/hooks/MCP integrations beyond the security-rules scope of this pack

---

### OWASP projects

**OWASP Top 10 for Web Applications (2025 current; 2021 superseded)**
- URL: `https://owasp.org/www-project-top-10/`
- Direct application: [`core/owasp.md`](core/owasp.md)

**OWASP Top 10 for Large Language Model Applications**
- URL: `https://owasp.org/www-project-top-10-for-large-language-model-applications/`
- Direct application: [`ai/ai-security.md`](ai/ai-security.md), [`ai/agent-security.md`](ai/agent-security.md), [`ai/rag-security.md`](ai/rag-security.md)

**OWASP MCP Top 10 (Model Context Protocol)**
- URL: `https://owasp.org/www-project-mcp-top-10/`
- Direct application: [`ai/mcp-security.md`](ai/mcp-security.md), [`core/owasp.md`](core/owasp.md)

**OWASP Application Security Verification Standard (ASVS) v5.0.0**
- URL: `https://owasp.org/www-project-application-security-verification-standard/`
- Direct application: [`core/owasp.md`](core/owasp.md), [`core/authentication.md`](core/authentication.md), [`core/cryptography.md`](core/cryptography.md)

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

### NIST frameworks

**NIST SSDF: Secure Software Development Framework (SP 800-218)**
- URL: `https://csrc.nist.gov/pubs/sp/800/218/final`
- Coverage: Prepare the Organisation (PO), Protect the Software (PS), Produce Well-Secured Software (PW), Respond to Vulnerabilities (RV)
- Direct application: all rule files in `core/` and `pipeline/`

**NIST SP 800-218A: Generative AI Profile**
- URL: `https://csrc.nist.gov/pubs/sp/800/218/a/final`
- Coverage: Augments SP 800-218 with AI model development practices; AI-specific secure development tasks
- Direct application: all rule files in `ai/`

**NIST AI Risk Management Framework (AI RMF 1.0)**
- URL: `https://www.nist.gov/system/files/documents/2023/01/26/AI%20RMF%201.0.pdf`
- Coverage: Govern, Map, Measure, Manage functions for AI systems
- Direct application: [`ai/ai-security.md`](ai/ai-security.md), [`ai/agent-security.md`](ai/agent-security.md)

---

### MITRE frameworks

**MITRE ATLAS (Adversarial Threat Landscape for AI Systems)**
- URL: `https://atlas.mitre.org/`
- Coverage: 16 tactics and 84+ techniques for AI-specific attacks (data poisoning, adversarial examples, prompt injection, model extraction, ML supply chain)
- Direct application: [`ai/ai-security.md`](ai/ai-security.md), [`ai/agent-security.md`](ai/agent-security.md), [`ai/rag-security.md`](ai/rag-security.md), [`ai/mcp-security.md`](ai/mcp-security.md)

**MITRE CWE Top 25 Most Dangerous Software Weaknesses**
- URL: `https://cwe.mitre.org/top25/`
- Coverage: Annual list of the most dangerous software weaknesses based on CVE data
- Direct application: [`core/input-validation.md`](core/input-validation.md), [`core/cryptography.md`](core/cryptography.md)

---

### Government and standards body guidance

**CISA Secure by Design**
- URL: `https://www.cisa.gov/resources-tools/resources/secure-by-design`
- Coverage: Three principles: take ownership of customer security outcomes, embrace radical transparency, lead from the top; shift-left approach; secure default configuration
- Direct application: [`pipeline/cicd-gates.md`](pipeline/cicd-gates.md), [`core/owasp.md`](core/owasp.md)

**SLSA: Supply-chain Levels for Software Artifacts**
- URL: `https://slsa.dev/`
- Coverage: Four levels of build provenance and supply-chain integrity; source integrity, build integrity, dependency tracking
- Direct application: [`pipeline/cicd-gates.md`](pipeline/cicd-gates.md)

**Google Secure AI Framework (SAIF)**
- URL: `https://saif.google/`
- Coverage: Secure development, deployment, execution, and monitoring for AI systems; mitigates model stealing, data poisoning, prompt injection, and information extraction
- Direct application: [`ai/ai-security.md`](ai/ai-security.md), [`ai/agent-security.md`](ai/agent-security.md)

**CIS Benchmarks**
- URL: `https://www.cisecurity.org/cis-benchmarks`
- Coverage: Consensus-based configuration baselines for OS, containers, cloud platforms, databases, and network devices
- Use: Reference for hardening production environments where AI-assisted code is deployed

---

### Cloud security alliance

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

All content in this directory is released under CC BY-SA 4.0. Copy, modify, and redistribute freely.

External repositories (TikiTribe, Wiz, Kariedo) maintain their own licenses: check each repository before redistribution.

---

**End of Document**
