# Claude Code Security Rules: Usage Guide

**Document Title:** Claude Code Security Rules Usage Guide\
**Document Type:** Guideline\
**Version:** 1.49.9\
**Date:** 2026-06-24\
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

The pack covers two areas:

1. **Security and compliance.** Hardcoded-secrets prevention, input validation, cryptography, authentication, OWASP/ASVS alignment, AI/agent/MCP/RAG security, CI/CD pipeline gates, language-specific security patterns. Lives under `core/`, `ai/`, `pipeline/`, and `languages/`.
2. **Development-governance discipline.** Rules that govern how an AI coding assistant collaborates on a governed codebase: gate discipline, change-tracking discipline, evidence-grounded completion, clarify-before-acting on ambiguous requests, artefact-and-branch discipline, action-before-explanation-of-inaction, validate-inference-before-action, AI-assistant workflow disciplines (research-assistant, pipeline construction, apply-time correction, always-split, CI-wait productivity), the trust-recovery escalation tier, and the project-integrity apex rule (lexicographic Quality > Speed > Cost). Lives under `governance/`.

The pack also ships **Claude Code Skills** (`SKILL.md` workflow format) under `skills/`, derived from selected governance rules. The canonical rule remains the source of truth for normative content (framework alignment, exception handling, rationale); the skill is the workflow wrapper (when to invoke, what steps in what order, what verification confirms completion). The directory tree below lists the current set; per-version shipping history lives in the `## Version history` section near the bottom of this README and in the parent library's [`CHANGELOG.md`](../../CHANGELOG.md).

The pack and the parent GRC library are two coordinated halves of one project. The parent library is the GRC corpus; the pack is the operational layer that allowed the maintainer to keep the corpus consistent with Claude Code participating in PRs. Every governance rule in the pack was extracted from a real maintenance event recorded in the parent library's [`CHANGELOG.md`](../../CHANGELOG.md); the pack is the library's lessons learned, made portable.

## Three ways to use this pack

This pack supports three adoption paths, all first-class:

1. **Inside the parent GRC library, as-shipped.** No action required. If you fork the whole parent repository, the pack is already wired into [`.claude/rules/`](../../.claude/rules/) (via the sync audit in [`tools/lint-claude-rules-sync.py`](../../tools/lint-claude-rules-sync.py)) and the skills are discoverable to Claude Code as the parent library is.

2. **Inside a fork of the parent GRC library.** Same as above, plus organisation-specific overlays. An adopting organisation forks, substitutes organisation-specific values across the corpus, and inherits the pack as the operational discipline its Claude Code sessions apply. See the parent library's [`docs/adopter-guide.md`](../../docs/adopter-guide.md) for the full path (Mode A).

3. **As a standalone Claude Code baseline pack, on any project.** A Claude Code baseline pack, usable on any project regardless of whether it has a GRC corpus, distilled from the disciplines this library required to maintain itself. Take this directory only and drop it into your project's Claude Code context. The setup generator at [`setup-generator-prompt.md`](setup-generator-prompt.md) automates this; the manual paths are documented in the "How to use" section below. The pack ships with its own version sequence so consumers in this mode can track pack updates without needing to track the parent library's version.

The third mode is an emergent use that has been adopted by developers in practice; it is supported alongside the primary fork-the-whole-repo path. Provenance is what makes the pack credible as a standalone artefact: every governance rule cites the maintenance event in the parent library's CHANGELOG that justified adding it.

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
├── governance/                 Development-governance discipline (initial rollout complete at pack 1.11.0; extended at 1.21.0, 1.27.0, 1.36.0, 1.47.0, and 1.49.0)
│   ├── gate-discipline.md                       Never weaken a gate to silence a failure; fix the artefact
│   ├── change-tracking.md                       Every PR carries an entry (terse OK for ancillary changes); no skip path
│   ├── evidence-grounded-completion.md          No completion claim or unread-artefact state assertion without enumerated, re-read, quoted, contradiction-searched evidence
│   ├── clarify-before-acting.md                 Surface ambiguity in one sentence and ask; never silently pick
│   ├── artefact-and-branch-discipline.md        Generated artefacts are read-only; protected branches are append-only
│   ├── action-before-explanation-of-inaction.md No inferred reasons for why an external action cannot proceed; attempt the safe action and report the real result, or name the destructive action and ask
│   ├── validate-inference-before-action.md      Validate any inferred premise via tool call before the action that depends on it; cascade failures are what the rule prevents
│   ├── ai-assistant-workflow-disciplines.md     Five disciplines for an AI assistant driving multi-PR work (research-assistant, pipeline construction, apply-time correction, always-split, CI-wait productivity)
│   ├── trust-recovery-escalation.md             Escalation tier when discipline failures need a white-box re-examination: the /full-qa + /fitness suite, every finding routed tiered by severity, maintainer sign-off terminates
│   └── project-integrity.md                     Apex rule: lexicographic Quality > Speed > Cost, project integrity non-negotiable; orders the other rules under a single priority on the optimization-dimension axis
├── ai/
│   ├── ai-security.md          LLM and AI application security requirements
│   ├── agent-security.md       Agentic workflow security and trust boundaries
│   ├── rag-security.md         Retrieval-augmented generation data controls
│   └── mcp-security.md         Model Context Protocol server security rules
├── pipeline/
│   └── cicd-gates.md           CI/CD security gates and pipeline controls
├── skills/                     Claude Code Skills (SKILL.md format) derived from selected pack rules
│   ├── evidence-grounded-completion/SKILL.md          Six-step verification protocol before any completion claim or unread-artefact state assertion
│   ├── gate-discipline-diagnose/SKILL.md              Diagnose-then-fix-the-artefact response to a failing gate
│   ├── clarify-before-acting/SKILL.md                 One-sentence ambiguity surfacing with named alternatives
│   ├── action-before-explanation-of-inaction/SKILL.md Reversibility-gate protocol before any "X is blocked because Y" clause attached to an external action
│   ├── change-tracking-write-entry/SKILL.md           Entry-writing workflow that satisfies the delta gate, link-coverage gate, and version-monotonicity audit in one pass
│   ├── artefact-discipline-check/SKILL.md             Routing workflow that redirects a hand-edit of a generated file (or a protected-branch operation) to the correct path
│   ├── validation-sweep/SKILL.md                      Corpus-wide regression sweep as a follow-up after any issue identified and corrected; loops until clean
│   ├── validation-sweep-pr-scoped/SKILL.md            PR-scoped post-merge validation sweep; Subagent A on the just-merged PR's diff plus a cross-reference check; runs after every merge to catch per-PR drift before it compounds
│   ├── citation-quote-verification/SKILL.md           Verify cited quotes match source text at the cited location; catches what citation-format and currency linters cannot
│   ├── fresh-reader-validation/SKILL.md               Dispatch a fresh subagent to read a new or substantively-revised document and surface tacit-context gaps
│   ├── skill-authoring-discipline/SKILL.md            Apply the pack's structural template and validate trigger accuracy when adding a new skill
│   ├── library-fitness-review/SKILL.md                Whole-corpus library-quality review with ten persona reviewers; periodic deliverable, not a per-PR gate
│   ├── deep-qa-review/SKILL.md                        Trust-recovery deep-QA forensic pass; six AI-failure-pattern subagents over a PR window; pairs with library-fitness-review; findings routed tiered by severity, maintainer sign-off terminates
│   ├── pr-retrospective/SKILL.md                      Post-merge retrospective on each successful PR; appends to the improvement-log register; recurring patterns surface as candidates for pack-rule updates or worker-brief additions
│   └── guardrail-review/SKILL.md                      Periodic structural-integrity review of the governance machinery (rules, skills, gates, wiring surfaces) for overlap / gap / drift the mechanical parity gates cannot see; maintainer-triggered + auto-prompt on machinery change
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
| [`governance/action-before-explanation-of-inaction.md`](governance/action-before-explanation-of-inaction.md) | Any project where an AI coding assistant participates and may need to explain why an external action (a PR merge, a deploy, a permission check, a CI run) is not proceeding; especially projects with branch protections, CI gates, or MCP integrations where the temptation to infer a "system says no" reason without checking is highest |
| [`governance/validate-inference-before-action.md`](governance/validate-inference-before-action.md) | Any project where an AI coding assistant orchestrates multi-step workflows (sweep cycles, audit cascades, multi-PR series) and may infer a premise (state unchanged since prior run, fix complete after one occurrence, prior approval extends to current scope) to drive an action; the rule fires when inference replaces verification at any decision boundary |
| [`governance/ai-assistant-workflow-disciplines.md`](governance/ai-assistant-workflow-disciplines.md) | Any project where an AI coding assistant drives substantive multi-PR work over a long session with research-helper subagents and CI gating. The rule covers research-assistant verification, pipeline PR construction, apply-time worker correction, "split when in doubt", and productive CI-wait use; surfaces when the orchestrator is dispatching multiple workers in parallel, when changes might be bundled, when idle during CI, or when pasting worker prose unverified |
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

**CSA Cloud Controls Matrix (CCM) v4.1.0**
- URL: `https://cloudsecurityalliance.org/research/cloud-controls-matrix/`
- Coverage: 207 controls across 17 domains
- Direct application: framework alignment tables in all `core/` rule files

**CSA AI Controls Matrix (AICM) v1.1.0**
- URL: `https://cloudsecurityalliance.org/research/ai-controls-matrix/`
- Coverage: 247 controls across 18 domains (CCM's 17 plus the AI-specific Model Development and Security (MDS) domain)
- Direct application: framework alignment tables in all `ai/` rule files

---

## Version history

| Pack | Library | Date | Notable change |
| --- | --- | --- | --- |
| 1.49.9 | 2026.06.298 | 2026-06-24 | Sweep 40 (`/resume` corpus-wide `/validate`) note, folded into the DD-8 PR by maintainer choice: the [`languages/go.md`](languages/go.md) TLS-config comment grouped `PreferServerCipherSuites` with `CipherSuites` as "apply only to TLS 1.2 and below", but per Go's `crypto/tls` docs `PreferServerCipherSuites` is a deprecated, ignored field (distinct from `CipherSuites` being TLS-1.2-scoped). Reworded so the deprecated/ignored status is stated; the #318 load-bearing claim (TLS 1.3 cipher suites not configurable; TLS 1.2 prohibited by the pack mandate) is unchanged and accurate. Pack `1.49.8` to `1.49.9` (patch; pack-prose precision). |
| 1.49.8 | 2026.06.296 | 2026-06-24 | DD-4/DD-5: completed the FR-135-deferred TLS rewrite of [`languages/go.md`](languages/go.md). The TLS-config example now sets `MinVersion: tls.VersionTLS13` and drops the explicit TLS-1.2 cipher-suite list, with a comment noting that Go does not allow configuring TLS 1.3 cipher suites (the `CipherSuites` and `PreferServerCipherSuites` fields apply only to TLS 1.2 and below) and that TLS 1.2 is prohibited by the pack cryptography mandate. [`core/owasp.md`](core/owasp.md) is intentionally left at the OWASP ASVS baseline (which permits TLS 1.2), the other FR-135 deferral. Pack `1.49.7` to `1.49.8` (patch; deferred-rewrite completion). |
| 1.49.7 | 2026.06.283 | 2026-06-24 | Generalized the session-closing-handoff-PR QA loop-break exception into the distributable pack layer (it previously lived only in this project's `.claude/CLAUDE.md` and `/resume` command). Named the exception in the [`validation-sweep-pr-scoped`](skills/validation-sweep-pr-scoped/SKILL.md) SKILL (the one sanctioned skip of the otherwise-mandatory per-PR `/validate-pr`) and in the no-skip clause of [`governance/ai-assistant-workflow-disciplines.md`](governance/ai-assistant-workflow-disciplines.md), each with the loop-termination rationale and the stronger compensating control (a full corpus-wide validation sweep at the next session's start), so adopters inherit the exemption and any future mechanical QA-cadence gate knows to build it in. Pack `1.49.6 → 1.49.7` (minor; distributable-exception generalization). |
| 1.49.6 | 2026.06.280 | 2026-06-24 | Sweep 36 finding (separate theme from the #301 close-out): the [`guardrail-review`](skills/guardrail-review/SKILL.md) SKILL growth-narrative count "a dozen gates to **forty-seven**" corrected to "**forty-eight**" (gate 48 was added by #299 after Sweep 34; this is a free-prose word-form count, invisible to gate 39's digit-form check). Pack `1.49.5 → 1.49.6` (patch; stale-count). |
| 1.49.5 | 2026.06.279 | 2026-06-24 | Sweep 36 close-out, pack surface: refreshed the external-reference framework versions in the "Cloud security alliance" section, CCM `v4.0` to `v4.1.0` and AICM `v1.0.3` to `v1.1.0`, and corrected the AICM coverage line from "13 AI-specific security controls" (which is the MDS-domain subset) to "247 controls across 18 domains" (the full v1.1.0 scope: CCM's 17 domains plus the AI-specific Model Development and Security domain). Part of the corpus-wide CCM/AICM citation-residual completion: the #298 reconciliation was token-scoped (it checked `<DOMAIN>-<NN>` codes and `\| CODE \| title \|` rows) and so left bare domain-code mentions and framework-version-currency strings uncorrected. Pack `1.49.4 → 1.49.5` (patch; citation currency). |
| 1.49.4 | 2026.06.276 | 2026-06-24 | CCM/AICM citation-accuracy reconciliation, pack surfaces (part of the corpus-wide reconciliation grounded in the uploaded authoritative CSA CCM v4.1.0 and AICM v1.1.0 catalogues): corrected the superseded CCM v4.0 domain code `IVS` to the authoritative v4.1.0 `I&S` in [`ai/mcp-security.md`](ai/mcp-security.md), [`core/cryptography.md`](core/cryptography.md), and [`pipeline/cicd-gates.md`](pipeline/cicd-gates.md) (the same fix landed in the byte-identical [`.claude/rules/`](../../.claude/rules/cicd-gates.md) mirror), and tightened the loose framework-basis reference `CSA CCM v4 / AICM v1` to `CSA CCM v4.1 / AICM v1.1` in [`CLAUDE.md`](CLAUDE.md). Pack `1.49.3 → 1.49.4` (patch; citation fixes). |
| 1.49.3 | 2026.06.250 | 2026-06-23 | FR-166 pack-surface touches (the new project audit gate 47 itself is project tooling, not pack content): the [`validation-sweep`](skills/validation-sweep/SKILL.md) SKILL's Subagent B scope gains a SEMANTIC listing-surface coverage-drift check (the framework matrices and crosswalks, the glossary and key-terms registers, per-document `Related Documents`), since the MECHANICAL surfaces (document-index register, domain READMEs) are now hard-gated by gate 47 and the sweep's value is the relevance-based surfaces a gate cannot enforce; and the [`guardrail-review`](skills/guardrail-review/SKILL.md) SKILL growth-narrative count "a dozen gates to **forty-six**" corrected to "**forty-seven**" (free-prose count, invisible to the gate-39 digit-form check). Pack `1.49.2 → 1.49.3` (patch; SKILL scope + stale-count). |
| 1.49.2 | 2026.06.244 | 2026-06-23 | Corpus-wide `/validate` (Sweep 25) close-out fix: the `guardrail-review` SKILL's growth-narrative count "grew from five rules to **nine**" corrected to "**ten**" (project-integrity.md, the 10th rule, was added in pack 1.49.0 / PR #258 but this free-prose count (invisible to the gate-41 enumeration check) was missed). Pack `1.49.1 → 1.49.2` (patch; stale-count fix). |
| 1.49.1 | 2026.06.239 | 2026-06-23 | FR-135 (corpus-wide TLS-floor consistency): migrated the pack rules' TLS floor from "TLS 1.2 minimum / 1.3 preferred" to **TLS 1.3 (or stronger)** with TLS 1.2 moved to the prohibited set, aligning [`core/cryptography.md`](core/cryptography.md) (the cryptography table + the TLS-config block) and [`ai/mcp-security.md`](ai/mcp-security.md) (MCP transport) to the canonical mandate already in pack [`CLAUDE.md`](CLAUDE.md) and [`security/policy-encryption-and-key-management.md`](../../security/policy-encryption-and-key-management.md) §1 (the same migration FR-81 began). Part of the same FR-135 PR that fixed the residual TLS-1.2 surfaces in the corpus standards. Two pack surfaces deferred to maintainer review (not force-migrated): [`core/owasp.md`](core/owasp.md) (represents OWASP ASVS, which permits TLS 1.2 at baseline) and [`languages/go.md`](languages/go.md) (the TLS code example needs a coherent rewrite, since Go ignores the explicit 1.2 cipher-suite list under a 1.3 minimum). Pack `1.49.0 → 1.49.1` (patch; consistency fix). |
| 1.49.0 | 2026.06.236 | 2026-06-23 | Added the **tenth governance rule** [`governance/project-integrity.md`](governance/project-integrity.md): the **apex rule** of the pack, the project-agnostic distribution of the project's PRIMORDIAL RULE. Fixes the priority ordering on the optimization-dimension axis (lexicographic **Quality > Speed > Cost**, project integrity non-negotiable): where each other rule constrains a specific behaviour, this rule decides which dimension wins when quality, speed, and cost conflict, and re-states the integrity non-negotiables (no stub/mock/fabrication, no gate suppression, no silent changes, failing states surfaced) as the apex-precedence forms of `gate-discipline`, `evidence-grounded-completion`, and `clarify-before-acting`, with a self-reminder checkpoint cadence. Wired across the three governance-rule enumeration surfaces (this README tree + the "two areas" prose list, pack [`CLAUDE.md`](CLAUDE.md), project `.claude/CLAUDE.md`) plus the `.claude/rules/governance/` byte-identical mirror and its [`tools/lint-claude-rules-sync.py`](../../tools/lint-claude-rules-sync.py) MIRROR_MAP entry; the collection-enumeration linter docstring updated "nine" → "ten" governance rules; the project CLAUDE.md PRIMORDIAL RULE forward-reference ("queued as TODO P4.0") now points at the shipped rule. Closes TODO P4.0. Pack `1.48.0 → 1.49.0` (minor; new rule). |
| 1.48.0 | 2026.06.235 | 2026-06-23 | Added the **fifteenth skill** [`guardrail-review`](skills/guardrail-review/SKILL.md) (slash command `/guardrails`): the periodic structural-integrity review of the governance machinery itself (rules, skills, gates, and their wiring surfaces) through three lenses the mechanical parity gates cannot apply: overlap (redundant or contradictory coverage), gap (a stated discipline no gate enforces, a recurring failure mode no rule names), and drift (a meaning diverged across wiring surfaces below the parity gates' resolution). Distinct from the content sweeps (`/validate`, `/validate-pr`) and the trust-recovery suite (`/full-qa`, `/fitness`): those review the corpus or a window of work, this reviews the machinery. Maintainer-triggered + auto-prompt after any PR that adds/removes/renames a rule, skill, or gate. Single-pass (not a fix-loop): structural findings are maintainer-decision proposals, routed tagged `[guardrails]`, tiered by severity, none dropped. `derives_from` [`gate-discipline.md`](governance/gate-discipline.md). New slash command at [`.claude/commands/guardrails.md`](../../.claude/commands/guardrails.md) with step-identifier parity (steps 1-6); [`tools/lint-paired-skill-step-parity.py`](../../tools/lint-paired-skill-step-parity.py) PAIRS registry extended with the `guardrail-review` to `guardrails.md` pair; pack-skills enumeration updated (14 to 15 skills). Pack `1.47.3 → 1.48.0` (minor; new skill). |
| 1.47.3 | 2026.06.234 | 2026-06-23 | **Completed the 1.47.1 routing-convention propagation in this README's own directory tree** and **corrected a stale governance-rule enumeration**. The corpus-wide `/validate` at session resume found three residual prose defects in this file that the 1.47.0/1.47.1 multi-surface edits missed: the "two areas" item-2 governance-rule enumeration omitted the ninth rule (`trust-recovery-escalation.md`), and the directory-tree one-line descriptions of `trust-recovery-escalation.md` and `deep-qa-review/SKILL.md` still carried the superseded "every finding to backlog top" single-tier routing phrasing. All three harmonized to the current state (nine rules; severity-tiered routing). Pack `1.47.2 → 1.47.3` (patch; prose correction). |
| 1.47.2 | 2026.06.231 | 2026-06-22 | **Completed the 1.47.1 routing-convention revision** in [`skills/deep-qa-review/SKILL.md`](skills/deep-qa-review/SKILL.md): two same-file spots the 1.47.1 propagation missed (the Verification completion criterion and a Common-Rationalizations cell still asserted the superseded single-top-priority-tier routing) are harmonized to the severity-tiered convention. Caught in-window by the PR #252 `/validate-pr` Subagent A (a multi-surface-incompleteness defect introduced by omission). Pack `1.47.1 → 1.47.2` (patch; completes 1.47.1). |
| 1.47.1 | 2026.06.230 | 2026-06-22 | **Revised the trust-recovery findings-routing convention** in [`governance/trust-recovery-escalation.md`](governance/trust-recovery-escalation.md) from "every confirmed finding to a single top-priority tier regardless of severity" to **severity-tiered routing**: High[critical] and High to the top-priority tier, Medium and Low to the next-priority tier, with the invariant (nothing dropped; the maintainer, not the assistant, decides what to defer) and the maintainer-sign-off termination unchanged. Maintainer direction 2026-06-22 ("routing flag only"). Propagated across the convention's surfaces in lock-step: the rule and its `.claude/rules/governance/` mirror, the [`deep-qa-review`](skills/deep-qa-review/SKILL.md) SKILL + `/full-qa` command, the [`library-fitness-review`](skills/library-fitness-review/SKILL.md) SKILL (new step 5.5 routing-flag) + `/fitness` command, and the pack + project `CLAUDE.md` rule-description bullets. Pack `1.47.0 → 1.47.1` (patch; within-rule revision). |
| 1.47.0 | 2026.06.224 | 2026-06-22 | Added the **ninth governance rule** [`governance/trust-recovery-escalation.md`](governance/trust-recovery-escalation.md): the escalation tier invoked when an AI assistant's discipline failures put a maintainer's confidence in a window of work in question. Names the trigger (abbreviated/skipped QA across changes, a skipped verification reaching the pipeline, a wrong-cadence automation, an unvalidated inference that cascaded), the two-skill suite (the AI-failure-pattern forensic pass [`deep-qa-review`](skills/deep-qa-review/SKILL.md) / `/full-qa` first, then the fresh-reader persona pass [`library-fitness-review`](skills/library-fitness-review/SKILL.md) / `/fitness`), the routing convention (every confirmed finding to the backlog's top priority regardless of severity, apply-time-verified, deduped), and the sign-off discipline (the tier terminates only on explicit maintainer sign-off, not on an empty finding-set). Includes the full-clone methodology rule. Wired across the three governance-rule enumeration surfaces (this README tree, pack [`CLAUDE.md`](CLAUDE.md), project `.claude/CLAUDE.md`) plus the `.claude/rules/governance/` local mirror and its sync mapping; the `deep-qa-review` SKILL's forward references to the rule are now linkified. Closes FR-164 (the collection-enumeration linter docstring's stale "seven governance rules" → "nine"). Pack `1.46.0 → 1.47.0` (minor; new rule). A project-only apex form of the same Quality > Speed > Cost integrity already lives in the project CLAUDE.md (PR #245); a project-agnostic distributable integrity rule remains queued (TODO P4.0) |
| 1.46.0 | 2026.06.222 | 2026-06-22 | Added the [`deep-qa-review` skill](skills/deep-qa-review/SKILL.md) (slash command `/full-qa`): the AI-failure-pattern half of the trust-recovery escalation tier (pairs with [`library-fitness-review`](skills/library-fitness-review/SKILL.md) / `/fitness`). A six-subagent forensic pass (recent-PR deep review, corpus-wide stale-reference, audit-programme integrity, citation forensic, generated-artefact forensic, discipline-violation forensic) over a maintainer-named PR window, with a binding step-0 rule to verify a full (non-shallow) clone before any git-history-aware audit (gates 31/40 emit false positives on a shallow clone via `git log --follow` mis-attribution). Findings route to the backlog top priority tagged `[full-qa]`; the pass terminates on maintainer sign-off, not empty-delta. New slash command at [`.claude/commands/full-qa.md`](../../.claude/commands/full-qa.md) with step-identifier parity (steps 0-6); [`tools/lint-paired-skill-step-parity.py`](../../tools/lint-paired-skill-step-parity.py) PAIRS registry extended with the `deep-qa-review` to `full-qa.md` pair; pack-skills enumeration updated (13 to 14 skills). First run (2026-06-22) caught a shallow-clone gate-31 false positive (153 documents) before it reached the backlog. Pack `1.45.2 → 1.46.0` (minor; new skill). The companion ninth governance rule (`trust-recovery-escalation.md`) and the `/fitness` routing-flag amendment follow in subsequent PRs |
| 1.45.0 | 2026.06.192 | 2026-06-22 | Added the [`pr-retrospective` skill](skills/pr-retrospective/SKILL.md) (slash command `/retro`) and the paired improvement-log register at [`.working/improvement-log.md`](../../.working/improvement-log.md). The skill is the orchestrator-side process-improvement loop: post-merge retrospective on each successful PR, output is one entry per PR in the register; recurring patterns surface as candidates for pack-rule updates, worker-brief template additions, or new audit gates. Pairs with the worker-side worker-brief template and the apply-time-catch tracking in hallucination-metrics.md to close the per-PR learning loop. Wired into the PR workflow step 5b in [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) (sequence: validate-pr → retro → next-PR planning). Pack `1.44.1 → 1.45.0` (minor; new skill addition); `tools/lint-paired-skill-step-parity.py` PAIRS registry extended with the new `pr-retrospective` ↔ `retro.md` pair; pack-skills enumeration in pack README updated. Discipline: chat-surfacing for Pattern/Proposed-improvement entries; recursion-avoidance batching of register-row commits into the next substantive PR; no orchestrator-side skip discretion (every merge gets a `/retro` entry even when conclusion is "nothing to learn") |
| 1.44.1 | 2026.06.187 | 2026-06-22 | FR-51 sweep touched 5 pack `skills/*/SKILL.md` files (action-before-explanation-of-inaction, artefact-discipline-check, change-tracking-write-entry, evidence-grounded-completion, gate-discipline-diagnose) with `27001 A.X` → `27001 Annex A.X` editorial alignment to the maintainer-approved canonical form. Pack patch bump for the SKILL-file edits |
| 1.44.0 | 2026.06.185 | 2026-06-22 | Closes **FR-87** and **FR-88** (maintainer-approved). [`core/owasp.md`](core/owasp.md):145 SSRF range list completed: IPv4 ranges restated in canonical CIDR notation with RFC citations (10.0.0.0/8, 172.16.0.0/12 with explicit /12-span note, 192.168.0.0/16, 169.254.0.0/16 with cloud-metadata note, 127.0.0.0/8, 100.64.0.0/10 CGNAT); IPv6 ranges added (::1/128 loopback, fc00::/7 ULA, fe80::/10 link-local with cloud-metadata variants). [`dev-security/standard-api-security.md`](../standard-api-security.md):110 cipher row enumerated TLS 1.3 AEAD suites per NIST SP 800-52 Rev. 2 §3.3.1 (TLS_AES_256_GCM_SHA384 recommended; TLS_AES_128_GCM_SHA256 and TLS_CHACHA20_POLY1305_SHA256 also accepted; rejected suites enumerated). The standard-api-security per-doc Version `0.0.3 → 0.0.4` |
| 1.43.0 | 2026.06.184 | 2026-06-22 | Closes the third FR-81 surface (maintainer-approved): [`dev-security/claude-rules/CLAUDE.md`](CLAUDE.md):58 TLS row updated from `TLS 1.3 (preferred), TLS 1.2 (minimum)` → `TLS 1.3 (or stronger), aligned to security/policy-encryption-and-key-management.md §1 (Encryption standards) canonical mandate`. TLS 1.2 added to the Prohibited column. Same alignment as PR #193 (ZTA framework) and PR #201 (dev-security standards). FR-81 fully closed |
| 1.42.0 | 2026.06.171 | 2026-06-22 | Added a "Batching into the next PR (recursion-avoidance)" sub-section to both [`skills/validation-sweep/SKILL.md`](skills/validation-sweep/SKILL.md) and [`skills/validation-sweep-pr-scoped/SKILL.md`](skills/validation-sweep-pr-scoped/SKILL.md) (mirrored into the matching slash commands at [`.claude/commands/validate.md`](../../.claude/commands/validate.md) and [`.claude/commands/validate-pr.md`](../../.claude/commands/validate-pr.md)). The naive interpretation of "every merge gets /validate-pr; every invocation gets a history row" creates a PR cascade: each PR's /validate-pr generates a new PR (for the row or for hot-fixes), which itself triggers /validate-pr, ad infinitum. The new sub-section codifies the resolution: /validate-pr outputs are **batched into the next PR, whatever its substantive purpose**. Two sub-cases: (1) zero-finding invocations append the history row to the next PR's diff. (2) findings-producing /validate-pr invocations bundle the fix(es) into the next PR (do NOT open a dedicated hot-fix PR; the next PR absorbs the fixes alongside its own work). A findings-producing `/validate` (corpus-wide sibling) may still warrant its own close-out PR when findings are numerous or coherent enough; for `/validate-pr` the bundle is always the default. This terminates the recursion the day's #187 → #188 → #189 → #190 cascade made apparent. Maintainer direction: "If there's nothing to actually fix or correct, then keep findings to bundle into the next PR whatever it is. If there are multiple PRs queued, then the fix of anything found in validate-pr can be bundled into the next PR whatever it is. Only the full validate should have its own PR for fixing multiple things." |
| 1.41.0 | 2026.06.169 | 2026-06-22 | Added a "Surfacing findings in chat" section to both [`skills/validation-sweep/SKILL.md`](skills/validation-sweep/SKILL.md) and [`skills/validation-sweep-pr-scoped/SKILL.md`](skills/validation-sweep-pr-scoped/SKILL.md) (mirrored into the matching slash commands at [`.claude/commands/validate.md`](../../.claude/commands/validate.md) and [`.claude/commands/validate-pr.md`](../../.claude/commands/validate-pr.md)). The new section makes explicit a discipline that was implicit in the "Report back" instruction: when findings exist, surface them prominently in the chat reply (per-finding ruleId, severity, `path:line`, evidence quote, impact, recommendation, in-window classification) rather than burying them in `.working/validate-pr/` files or `CHANGELOG-detailed.md`. The maintainer reads findings in chat for triage; the per-PR / per-iteration record remains the authoritative archive. Surfaced by maintainer direction after PR #189's findings were not prominently surfaced in chat ("I want the info in chat so I can be aware without looking for changelog detailed or some other file after the merge"). Same direction codified for both /validate and /validate-pr because the chat-surfacing discipline applies to both sweeps |
| 1.40.2 | 2026.06.168 | 2026-06-22 | Hot-fix amending the previous row's catch-attribution claim. The 1.40.1 row above (committed in PR #188) said "gate 31 caught it via the second `/validate-pr` cycle"; that wording conflated two distinct mechanisms (the gate 31 audit and the `/validate-pr` workflow's Subagent A), and the gate-31 framing was wrong on the facts: gate 31 did not actually fire on the pack README's stale Date because the lag was zero days at PR #187's merge time and only opened post-merge after midnight UTC. The /validate-pr sweep's Subagent A deep-read caught it post-hoc. The 1.40.1 row's prose has been corrected to credit /validate-pr deep-read; this 1.40.2 row records the correction. The error was caught by /validate-pr on PR #188 (the close-out PR that introduced the 1.40.1 row) |
| 1.40.1 | 2026.06.167 | 2026-06-22 | Patch release: harmonized the "no orchestrator-side skip discretion" wording across the two paired surfaces ([`skills/validation-sweep-pr-scoped/SKILL.md`](skills/validation-sweep-pr-scoped/SKILL.md) and [`.claude/commands/validate-pr.md`](../../.claude/commands/validate-pr.md)) after `/validate-pr` on PR #187 surfaced a multi-surface-incompleteness finding: the two surfaces previously expressed the same discipline in slightly different language (different lists of rejected rationales; different "proof-of-discipline" framing). Synced verbatim. Also corrected this README's own per-document `Date` from `2026-06-21` to `2026-06-22` (PR #187 bumped Version 1.39.0 → 1.40.0 but missed Date; the `/validate-pr` sweep on PR #187 (Subagent A deep-read) caught it post-hoc. Gate 31 itself did not fire, a timezone-boundary edge case: at PR #187's merge time both commit-date and the Date field were `2026-06-21`, so gate 31's lag check saw a 0-day window; the lag opened only after midnight UTC, post-merge). No discipline change; the discipline was already correctly expressed in PR #187, just inconsistently across the two surfaces |
| 1.40.0 | 2026.06.166 | 2026-06-22 | Codified the **no orchestrator-side skip discretion** discipline across three surfaces after a maintainer-flagged policy deviation. The orchestrator deliberately skipped `/validate-pr` on PRs #185 and #186 citing "circular" / "redundant" rationale; the maintainer flagged this as a real policy deviation, since the discipline says every merge gets `/validate-pr` and the orchestrator does NOT have discretion to skip QA based on unilateral judgment. Updated three surfaces with explicit "no skip" language: [`skills/validation-sweep-pr-scoped/SKILL.md`](skills/validation-sweep-pr-scoped/SKILL.md) When-to-Use section; [`.claude/commands/validate-pr.md`](../../.claude/commands/validate-pr.md) Termination section; [`governance/ai-assistant-workflow-disciplines.md`](governance/ai-assistant-workflow-disciplines.md) Prohibited-anti-patterns gains a new "Orchestrator-side judgment-call skipping of mandatory QA/testing steps" anti-pattern with explicit failure-mode description and fix. Same language mirrored to [`.claude/rules/governance/ai-assistant-workflow-disciplines.md`](../../.claude/rules/governance/ai-assistant-workflow-disciplines.md). Also fixed a docstring staleness in [`tools/lint-paired-skill-step-parity.py`](../../tools/lint-paired-skill-step-parity.py) that claimed "Currently only validation-sweep has both a SKILL.md and a slash-command counterpart" (stale after library-fitness-review and validation-sweep-pr-scoped joined the registry); rewrote to be generic. Captured as new failure-mode class C-9 in [`.working/hallucination-metrics.md`](../../.working/hallucination-metrics.md) with future-gate candidate (mechanical check that every merged PR appears in `.working/validate-pr/history.md`) |
| 1.39.0 | 2026.06.163 | 2026-06-21 | Extended [`governance/ai-assistant-workflow-disciplines.md`](governance/ai-assistant-workflow-disciplines.md) §1 (Research-assistant discipline) with a new "Worker-brief template and hallucination-assessment update protocol" subsection. Codifies the discipline of maintaining a project-local worker-brief template that the orchestrator uses as the starting point for every worker dispatch, with explicit guard rails (DO and DO-NOT lists) that prevent recurring worker-side failure modes. When a new failure class is caught at apply-time, the protocol calls for (a) logging the catch, (b) classifying the fix as worker-side instruction / orchestrator-side check / new mechanical gate, (c) updating the template inline (or queueing as a follow-up), (d) referencing the template update from the catch entry. This makes the discipline self-improving: each new failure class becomes a permanent guard rail. The project's worker-brief template ships in parallel at [`.working/worker-brief-template.md`](../../.working/worker-brief-template.md) with initial guard rails derived from the four known failure classes (file-path confabulation; stale external citations; wrong PR / FR cross-references; absolute current version numbers in drafts). Mirrored to [`.claude/rules/governance/ai-assistant-workflow-disciplines.md`](../../.claude/rules/governance/ai-assistant-workflow-disciplines.md). Project-agnostic discipline; adopters create their own template at a project-appropriate location |
| 1.38.0 | 2026.06.162 | 2026-06-21 | Added [`skills/validation-sweep-pr-scoped/SKILL.md`](skills/validation-sweep-pr-scoped/SKILL.md) and the [`/validate-pr` slash command](../../.claude/commands/validate-pr.md): PR-scoped post-merge validation sweep that runs after every merge to catch per-PR drift before it compounds across subsequent PRs. Dispatches Subagent A on the just-merged PR's diff (same eight failure-mode classes as the corpus-wide `validation-sweep` SKILL, scoped to the touched files), plus a lightweight cross-reference check on files that cite the touched files. Complements the corpus-wide `/validate` sweep (the two are not substitutes; they cover different scopes at different cadences). New working-state activity directory at [`.working/validate-pr/`](../../.working/validate-pr/) with `README.md`, `history.md`, and per-PR detail files convention matching the existing [`.working/validate-sweeps/`](../../.working/validate-sweeps/) structure. First real per-PR sweep will land starting with the FR-33 PR (the first FR PR shipped under the new discipline) |
| 1.37.0 | 2026.06.159 | 2026-06-21 | Extended [`governance/ai-assistant-workflow-disciplines.md`](governance/ai-assistant-workflow-disciplines.md) §3 (Apply-time worker correction) to include the per-file metadata-bump check as an explicit numbered step: when editing a versioned document's body, the orchestrator bumps **both** `Version` and `Date` in the same commit (not Version alone). The Common-patterns enumeration is extended to call out "orchestrator bumping Version but missing Date" as a recurring failure mode. Surfaced after PR #179's gate-31 catch on `security/policy-information-security.md` (Date `2026-05-27`, lag 25 days) and `resilience/template-tabletop-exercise.md` (Date `2026-06-02`, lag 19 days). Mirrored to [`.claude/rules/governance/ai-assistant-workflow-disciplines.md`](../../.claude/rules/governance/ai-assistant-workflow-disciplines.md) per the pack sync convention. The project-local [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) `## Version-bump discipline` section was also expanded from three surfaces (Version, library CalVer, README Version) to four (adding `Date`), with the operationalization checklist now four questions instead of three |
| 1.36.0 | 2026.06.155 | 2026-06-21 | Added [`governance/ai-assistant-workflow-disciplines.md`](governance/ai-assistant-workflow-disciplines.md), a new pack rule covering five disciplines for an AI coding assistant driving multi-PR work over a long session: (1) research-assistant discipline (workers produce research, orchestrator authors final prose, claims verified at apply-time); (2) pipeline PR construction (parallel research, serial apply, CI gating between PRs); (3) apply-time worker correction (catch worker errors at apply-time, document them in the entry); (4) "always split when in doubt" PR discipline (default to splitting unless changes are tightly coherent); (5) background work during CI waits (read-only prep on the next PR; no edits during the wait). Each discipline emerged from a recurring failure mode observed during the corpus-remediation work that drove the pack's recent evolution. Mirrored to [`.claude/rules/governance/ai-assistant-workflow-disciplines.md`](../../.claude/rules/governance/ai-assistant-workflow-disciplines.md) and added to the pack-sync mapping in [`tools/lint-claude-rules-sync.py`](../../tools/lint-claude-rules-sync.py). This project also creates [`.working/hallucination-metrics.md`](../../.working/hallucination-metrics.md) as the project-specific tracking artefact for the discipline's catch / escape ratios |
| 1.35.0 | 2026.06.154 | 2026-06-21 | Amended [`governance/change-tracking.md`](governance/change-tracking.md) and [`skills/change-tracking-write-entry/SKILL.md`](skills/change-tracking-write-entry/SKILL.md) to retire the `Changelog: skip` opt-out path in favour of a terse-entry convention. Every PR now carries an entry; substantive entries (the existing structured-section form) cover anything that ships, modifies, or removes adopter-facing content; terse entries (date + version header + one sentence describing what was accomplished) cover ancillary changes (internal tooling, working-state housekeeping, pure refactors, typo fixes). The paired DONE-ledger guidance is also revised: entries are 1-2 sentences, no links, no version bumps, "scrolling battle-text" framing as an at-a-glance index rather than a CHANGELOG duplicate. Mirrored to [`.claude/rules/governance/change-tracking.md`](../../.claude/rules/governance/change-tracking.md) per the pack sync convention. The corresponding CHANGELOG-delta CI gate ([`tools/check-changelog-on-pr.py`](../../tools/check-changelog-on-pr.py)) still accepts the legacy skip trailer as a transition-window back-compat measure; tightening the gate to match the rule is queued as a follow-up |
| 1.34.0 | 2026.06.121 | 2026-06-21 | Amended `skills/library-fitness-review/SKILL.md` Step 5 with the unverified→confirmed labelling discipline. Subagent findings are now `verification: unverified` at output time; Pass-1 (orchestrator re-reads cited source and tags each finding with one of four verdict tags `✅` / `⚠️` / `❌` / `🤔`); Pass-2 (maintainer-interactive bucket processing with batch confirmation for `✅`, per-finding prompts for `⚠️` and `🤔`, batch presentation with optional escalation for `❌`); triage by severity applies only to confirmed findings. Confirmed findings produce TODO entries with `FR-<n>` ID + run reference + verification date. Slash command [`.claude/commands/fitness.md`](../../.claude/commands/fitness.md) updated in parallel (paired-skill step-parity gate). `.working/fitness-reviews/README.md` and the existing `2026-06-21-r1.md` report annotated; the existing 111 findings retroactively marked `unverified` pending Pass-1 in the next PR |
| 1.33.0 | 2026.06.119 | 2026-06-21 | Amended `governance/change-tracking.md` with a new "Overnight-work protocol" subsection (under PR finalization protocol). Documents the lifecycle of an overnight session: file starts in `Status: stub`; first overnight PR transitions to `Status: in-flight`; each overnight PR ships with `in-flight`; session end transitions to `Status: done`; next-morning processing PR routes content to working-state ledgers and resets to `stub`. The corresponding audit gate accepts `stub` and `in-flight`; fails on `done`. Three-state field rather than binary so overnight PRs land cleanly while still applying mechanical pressure for morning processing. Mirrored to `.claude/rules/governance/change-tracking.md` per the pack sync convention. Project-agnostic; adopters supply the overnight-file location |
| 1.32.0 | 2026.06.114 | 2026-06-21 | Amended `governance/change-tracking.md` with a new "PR finalization protocol" section covering three disciplines: (a) TODO is forward-looking; historical state rotates out (delete on close, no strikethroughs); (b) DONE ledger keyed by original backlog ID complements the CHANGELOG (CHANGELOG by PR, DONE by closed item); (c) after-merge protocol of listing the next-N planned PRs from TODO (default N=5), surfacing the queue so the maintainer can redirect early. Mirrored to `.claude/rules/governance/change-tracking.md` per the pack sync convention. Project-agnostic; adopters supply the DONE-ledger location |
| 1.31.0 | 2026.06.109 | 2026-06-21 | Amended `governance/change-tracking.md` to recognize the two-file CHANGELOG split convention. Root `CHANGELOG.md` carries lead-paragraph summaries (adopter-facing); detailed mirror (project-specific location) carries the full structured-section entries (maintainer-grade). The delta-gate (`tools/check-changelog-on-pr.py`) requires both files to move in lock-step when the split is in use. Mirrored to `.claude/rules/governance/change-tracking.md` per the pack sync convention |
| 1.30.0 | 2026.06.105 | 2026-06-21 | Added `skills/library-fitness-review`: comprehensive whole-corpus library-quality review with ten persona reviewers (executive, security practitioner, GRC practitioner, auditor, policy editor, process owner, skeptical reader, adoption practitioner, privacy officer, newcomer). Periodic deliverable (after major changes or quarterly), not a per-PR gate. Output is an 8-section combined report with a discrete remediation backlog. Complements `validation-sweep` (per-PR regression check); the two are not substitutes |
| 1.29.0 | 2026.06.104 | 2026-06-21 | `validation-sweep` skill steps 8 and 9 restructured: step 8 now writes a history-table row on every iteration (new `Subagents` column per Rule 5.6); step 9 writes a per-iteration detail file only when findings exist (zero-finding iterations leave only a row in the history table). This is the canonical convention for any `.working/<activity>/` subdirectory going forward: `README.md` for static convention info, `history.md` for the cumulative reverse-chronological table, `<dated>.md` files for per-run detail when findings exist |
| 1.28.2 | 2026.06.103 | 2026-06-21 | Sweep 10 iter 1 close-out: stale step-count narratives in `validation-sweep` SKILL.md (step intro "seven steps" → "nine steps") and in the `/validate` slash command preamble ("eight-step" → "nine-step"); stale "Four rules, no ceremony" in step 5 intro → "Six rules" (Rules 5.1-5.6 exist); awkward possessive on closing parenthesis at step 5 cross-reference; section-header convention drift across the three per-iteration-record-spec surfaces (SKILL.md / slash command / `.working/validate-sweeps/README.md`) reconciled to comma form |
| 1.28.1 | 2026.06.102 | 2026-06-21 | `validation-sweep` skill steps 5 and 8 updated for the relocation of the project's sweep history file from `governance/register-sweep-history.md` to `.working/validate-sweeps-history.md` (the file is project-specific application of the discipline, not template content; SKILL.md now uses path-agnostic language). No process change |
| 1.28.0 | 2026.06.101 | 2026-06-21 | Added step 9 to the `validation-sweep` skill: every iteration writes a per-iteration record to the project's working directory (in this project: `.working/validate-sweeps/`). The record captures full subagent transcripts and orchestrator synthesis, complementing the cumulative summary in the sweep history file. Adopters relocate the working directory to a project-appropriate path. Slash command for the skill is `/validate` in this project (skill name remains `validation-sweep`) |
| 1.27.0 | 2026.06.98 | 2026-06-21 | Added the seventh governance rule (`validate-inference-before-action.md`) after a recurring orchestrator-skip cascade pattern: an inferred premise (state unchanged since prior run, fix complete after one occurrence) drove a downstream action without validation; the rule fires at the inference-driven-action surface as the action-side counterpart of `evidence-grounded-completion` |
| 1.26.0 | 2026.06.61 | 2026-06-20 | Added three new skills (`citation-quote-verification`, `fresh-reader-validation`, `skill-authoring-discipline`) recreated as in-house CC BY-SA 4.0 content from cross-source research (kfchou wiki-skills and anthropics doc-coauthoring / skill-creator as reference; not imported as external overlay to keep licence accumulation bounded) |
| 1.25.0 | 2026.06.48 | 2026-06-20 | Added `skills/validation-sweep`: corpus-wide regression sweep as a follow-up after any issue identified and corrected; derives from `evidence-grounded-completion` and operationalises its worked example at corpus scope |
| 1.24.0 | 2026.06.43 | 2026-06-19 | Trimmed `Pack scope` to the load-bearing content; introduced this `Version history` section |
| 1.23.0 | 2026.06.40 | 2026-06-19 | Dual-deliverable reframe across project framing surfaces (new `Three ways to use this pack` section; the pack named as the library's lessons learned made portable) |
| 1.22.0 | 2026.06.39 | 2026-06-19 | Added `skills/change-tracking-write-entry` and `skills/artefact-discipline-check`; closed out the post-S.3 skills evaluation |
| 1.21.0 | 2026.06.38 | 2026-06-19 | Added the sixth governance rule (`action-before-explanation-of-inaction`) and its skill mirror |
| 1.20.x | 2026.06.20 onwards | 2026-06-19 | Introduced the `skills/` subdirectory; shipped the first three skills (evidence-grounded-completion, gate-discipline-diagnose, clarify-before-acting); patches broadened evidence-grounded-completion to cover unread-artefact state assertions |
| 1.12.0 to 1.19.0 | 2026.06.x | 2026-06-02 | Incremental language-rule additions (Swift, Kotlin, React Native, Flutter, .NET MAUI, Capacitor/Ionic) and expansion of the external-overlay source set (addyosmani as a fourth vetted source) |
| 1.11.0 | 2026.05.144 | 2026-06-01 | Completed the phased governance rollout (`artefact-and-branch-discipline`) |
| 1.10.0 | 2026.05.143 | 2026-06-01 | `clarify-before-acting` |
| 1.9.0 | 2026.05.142 | 2026-06-01 | `evidence-grounded-completion` |
| 1.8.0 | 2026.05.141 | 2026-06-01 | `change-tracking` |
| 1.7.0 | 2026.05.140 | 2026-06-01 | First governance rule: `gate-discipline` |
| 1.6.0 | 2026.05.139 | 2026-06-01 | Scope broadened from security-only to include development-governance discipline |

Per-PR detail for each pack version is in the parent library's [`CHANGELOG.md`](../../CHANGELOG.md). The pack does not maintain its own per-version changelog; the parent CHANGELOG is the source of truth. Pack versions before 1.6.0 covered the pack's original security-and-compliance scope; per-version detail for that earlier era is also in the parent CHANGELOG.

---

## Licence

All content in this directory is released under CC BY-SA 4.0. Copy, modify, and redistribute freely.

External repositories (TikiTribe, Kariedo, addyosmani, Wiz) maintain their own licenses: check each repository before redistribution.

---

**End of Document**
