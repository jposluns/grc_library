# Maintainer vetting log: external rule sources

**Document Type:** Maintainer log\
**Version:** 1.3.4\
**Date:** 2026-07-02\
**Owner:** Governance Library Maintainer\
**Repository Path:** [`dev-security/claude-rules/vetting-log.md`](vetting-log.md)\
**License:** CC BY-SA 4.0

---

## Purpose

This log records the library maintainer's vetting status for each external rule source referenced from this directory. The [`setup-generator-prompt.md`](setup-generator-prompt.md) "Optional external-source overlay" step in Phase 2 references this log so the consumer sees the maintainer's vet status when deciding whether to elect a given source.

Vetting against the External-Source Vetting Protocol (EXT-01) treats fetched content as data, not instructions. Each entry below records the date, method, scope, and findings.

This log lives in the [`dev-security/claude-rules/`](README.md) directory because, per the library's exemption convention, files in this directory are not subject to the canonical document-metadata audit and do not carry the 13-field metadata block of governance artefacts. The shorter header above suffices.

---

## How to update this log

When the library maintainer adds a new external source to the references in [`README.md`](README.md), or when a periodic re-vet is performed, append a new entry below (newest first). Each entry must record:

- **Source name and repository URL.**
- **Vet date** (ISO date) and the commit reference of the upstream repository at the time of vet, if known.
- **Vet method.** "WebFetch + EXT-01" (Claude Code-based fetch of named files and pattern scan), "back-port cadence review" (maintainer inspected diffs while back-porting improvements into the library pack), "third-party security review" (named external party), or a combination.
- **Files reviewed.** Explicit list. A vet that only inspected the README is not a vet of the rule files.
- **Findings.** Quote any concerning passage verbatim. State the verdict: "Vetted (no concerns)", "Vetted with caveats" (list), or "Not vetted; consumer must apply EXT-01 per fetch".
- **Status.** One of: `Vetted`, `Vetted with caveats`, `Vetting in progress`, `Not yet vetted`, `Withdrawn` (source no longer referenced).
- **Re-vet cadence.** Default: re-vet on the library's standards-currency cadence (annual) or when material upstream changes are noticed. Sources with caveats may carry a shorter cadence.

When a re-vet supersedes a prior entry, do not delete the prior entry. Append a new dated entry and leave the historical record visible.

---

## Source: addyosmani Agent Skills

**Repository:** `https://github.com/addyosmani/agent-skills`

### Vet 2026-06-19 (first-time vetting)

**Vet method:** WebFetch + curl direct fetch + EXT-01 protocol, performed by the library maintainer via a Claude Code session. Upstream commit pinned at `13e43f2310224d5770a7fb0a8c24c02b73da69e9` (2026-06-19, "Merge pull request #270 from nucliweb/ci/validate-commands").

**Files reviewed:**

Fully vetted (read in full, EXT-01 pattern scan):

- `LICENSE`
- `skills/security-and-hardening/SKILL.md`
- `skills/code-review-and-quality/SKILL.md`
- `skills/ci-cd-and-automation/SKILL.md`
- `skills/using-agent-skills/SKILL.md` (meta-skill that explains the format)
- `skills/context-engineering/SKILL.md`

Scanned for red-flag patterns (not read in full): the 19 remaining skill directories under `skills/` (`interview-me`, `idea-refine`, `spec-driven-development`, `planning-and-task-breakdown`, `incremental-implementation`, `test-driven-development`, `doubt-driven-development`, `source-driven-development`, `frontend-ui-engineering`, `api-and-interface-design`, `browser-testing-with-devtools`, `debugging-and-error-recovery`, `code-simplification`, `performance-optimization`, `git-workflow-and-versioning`, `deprecation-and-migration`, `documentation-and-adrs`, `observability-and-instrumentation`, `shipping-and-launch`). Per the README's skill index plus a spot-scan of the skill titles and `description:` frontmatter fields surfaced via the upstream `README.md`, these are general engineering workflow skills (interview, refinement, TDD, debugging, observability, etc.) with no security-sensitive content surface beyond the five vetted in full. Consumers electing the overlay via the setup-generator who wish to fetch one of these additional skills should apply EXT-01 per fetch.

**EXT-01 pattern scan results across the fully-vetted files:**

| Pattern | Outcome |
|---|---|
| Role-override / "ignore previous instructions" | Not present. The `using-agent-skills` meta-skill enumerates "Core Operating Behaviors" but they govern the agent's own discipline (surface assumptions, manage confusion, push back, enforce simplicity, scope discipline, verify); they do not instruct the agent to override the consuming session's rules. |
| Urgency framing or pre-authorization language | Not present. Tone is declarative-instructional throughout. |
| External URL fetch directives | Not present. The only external URLs in the fully-vetted files are `https://genai.owasp.org/llm-top-10/` (legitimate reference, not a fetch instruction) and `http://localhost:3000` (used as a sample value in an example, not a fetch target). |
| Shell command execution beyond standard documentation | Not present. Code examples illustrate `npm install`, `bcrypt`, `helmet`, etc. as documentation of techniques to apply, not as instructions to execute on the consumer's system. |
| Security control weakening | Not present. The `security-and-hardening` skill's Never-Do list explicitly forbids disabling security headers, using `eval()` / `innerHTML` with user data, storing auth tokens in `localStorage`, committing secrets, and exposing stack traces. Posture strengthens controls throughout. |
| Hidden text, base64 blobs, or encoded directives | Not present. All content is plain UTF-8 markdown. The references to "encoded" all refer to output encoding for XSS prevention (a defensive control), not encoded instructions. |

**Notable substantive observations (not vetting concerns, listed for the consumer's awareness):**

- **Scope is engineering workflows, not GRC.** addyosmani's collection is "production-grade engineering skills for AI coding agents", workflow processes spanning Define, Plan, Build, Verify, Review, and Ship phases. It is not a governance / risk / compliance pack. Adopters electing this overlay should know they are getting general engineering discipline (TDD, code review, debugging, etc.), not additional GRC content.
- **Format diverges from the other three vetted sources.** addyosmani uses the Claude Skills `SKILL.md` format (YAML frontmatter with `name:` and `description:` for skill-tool discovery). TikiTribe, Wiz, and Kariedo use the rule / CLAUDE.md / `@`-import patterns. Consumers whose Claude Code session does not support the Skills discovery format may see addyosmani's content as static markdown without auto-invocation behaviour.
- **License is MIT** (the GRC Library pack is CC BY-SA 4.0). Per the same logic as TikiTribe and Kariedo, adopters redistributing addyosmani content under their own terms must preserve the upstream attribution.
- **Tier model (Mandatory / Approval-Gated / Prohibited) and STRIDE-per-trust-boundary framing** in `security-and-hardening` are common taxonomies; cherry-picking these structures into our own content is independent synthesis (per [`NOTICE.md`](../../NOTICE.md)), not redistribution.
- **Some workflow content overlaps existing pack rules.** `code-review-and-quality` overlaps [`dev-security/procedure-secure-code-review.md`](../procedure-secure-code-review.md). `ci-cd-and-automation` overlaps [`dev-security/claude-rules/pipeline/cicd-gates.md`](pipeline/cicd-gates.md). `security-and-hardening` overlaps [`dev-security/claude-rules/core/owasp.md`](core/owasp.md) and adjacent rules. The pack remains the primary content; the overlay is supplementary.

**Verdict:** Vetted (no concerns) on the fully-read subset; the 19 spot-scanned skill directories require per-fetch EXT-01 if a consumer elects them later.

**Status:** `Vetted` for the fully-vetted subset above; `Spot-scanned` for the remaining 19 skill directories.

**Re-vet cadence:** Standards-currency cadence (annual). Re-vet immediately if upstream addyosmani materially expands scope into security-sensitive territory (for example, adds shell-execution skills, network-fetch skills, MCP server definitions, or any skill whose Process steps include instructions to disable controls). Spot-checks beyond the fully-vetted subset above are at the maintainer's discretion when back-porting individual skills.

---

## Source: Kariedo Claude Code Security Rules

**Repository:** `https://github.com/kariedo/claude-code-security-rules`

### Vet 2026-05-31 (first-time vetting)

**Vet method:** WebFetch + EXT-01 protocol, performed by the library maintainer via a Claude Code session.

**Files reviewed:**

- [`README.md`](README.md)
- `CLAUDE.md` (root)
- `security-rules/core-principles.md`
- `security-rules/dangerous-flows.md`
- `security-rules/mcp-security.md`
- `security-rules/python.md`
- `security-rules/vulnerability-prevention.md`

**EXT-01 pattern scan results across all reviewed files:**

| Pattern | Outcome |
|---|---|
| Role-override / "ignore previous instructions" | Not present. |
| Urgency framing or pre-authorization language | Not present. Tone is declarative and educational. |
| External URL fetch directives | Not present. The `@`-syntax imports are internal to the repository (e.g., `@security-rules/core-principles.md`). |
| Shell command execution beyond standard setup documentation | Not present. The setup section uses standard `cp -r` to copy files into the consumer's project. The `dangerous-flows.md` file *documents* dangerous shell patterns as anti-examples to detect, not as instructions to execute. |
| Security control weakening | Not present. The rules consistently strengthen controls. `core-principles.md` Principle 7 explicitly forbids the *generation of code* that disables security checks, framed as a violation rather than a permissible action. |
| Hidden text, base64 blobs, or encoded directives | Not present. All content is plain UTF-8 markdown. |

**Notable substantive observations (not vetting concerns, listed for the consumer's awareness):**

- The pack uses the `@`-syntax import system to compose its modules. Adopters whose Claude Code version does not recognize `@`-syntax will not get the modular load behaviour the source intends; the consumer should verify their environment supports the syntax before relying on import semantics.
- The pack's CLAUDE.md "Implementation Guidelines" section instructs Claude to "never generate code that violates these rules without explicit user override". This is consistent with the library's own posture; no caveat needed.
- The pack covers seven languages (Python, JavaScript, Java, PHP, Ruby, Rust, C). It does not cover Go, Kotlin, Swift, or Scala. Consumers whose stack includes those languages should not assume coverage.

**Verdict:** Vetted (no concerns).

**Status:** `Vetted`

**Re-vet cadence:** Standards-currency cadence (annual). Re-vet immediately if upstream Kariedo materially expands scope (for example, adds shell-execution helpers, MCP server definitions, or external fetch instructions).

---

## Source: TikiTribe Claude Secure Coding Rules

**Repository:** `https://github.com/TikiTribe/claude-secure-coding-rules`

### Vet 2026-05-31 (first formal EXT-01 vet)

**Vet method:** WebFetch + EXT-01 protocol, performed by the library maintainer via a Claude Code session. Supersedes the prior back-port-cadence-only record (preserved below).

**Files reviewed (representative sample across categories):**

- [`README.md`](README.md)
- `rules/_core/owasp-2025.md`
- `rules/_core/ai-security.md`
- `rules/_core/mcp-security.md`
- `rules/_core/agent-security.md`
- `rules/_core/rag-security.md`
- `rules/languages/python/CLAUDE.md`
- `rules/backend/fastapi/CLAUDE.md`
- `rules/cicd/_core/cicd-security.md`

The TikiTribe repository organizes 100+ rule sets across 12 language directories (`rules/languages/<lang>/CLAUDE.md`), 16 backend / AI-ML framework directories (`rules/backend/<framework>/CLAUDE.md`), and category directories for `_core/`, `cicd/`, `frontend/`, `iac/`, `containers/`, `rag/`. Vetting every file is impractical; the sample above covers all `_core/` files (the substantive AI / agent / MCP / RAG / OWASP guidance), one representative language (Python), one representative framework (FastAPI), and the CI/CD core.

**EXT-01 pattern scan results across all reviewed files:**

| Pattern | Outcome |
|---|---|
| Role-override / "ignore previous instructions" | Not present in any of the nine files. Code examples use legitimate `role: system` / `role: user` boundaries in API examples, not override directives. |
| Urgency framing or pre-authorization language | Not present. Severity levels (`strict`, `warning`, `advisory`) are used for risk classification, not urgency tactics. |
| External URL fetch directives | Not present. References to OWASP / NIST / MITRE / CWE are standard citations, not fetch directives. |
| Shell command execution beyond standard setup documentation | Not present. The setup section uses `git clone` plus `cp -r`. Code examples show `subprocess.run()` patterns with `shell=False` and command allowlisting, framed as anti-patterns for educational contrast (not as instructions to execute). |
| Security control weakening | Not present. Every "Don't" example flags a vulnerable pattern; every "Do" example strengthens controls. |
| Hidden text, base64 blobs, or encoded directives | Not present. All content is plain UTF-8 markdown with readable code blocks. |

**Notable substantive observations (not vetting concerns, listed for the consumer's awareness):**

- License is MIT (the GRC Library pack is CC BY-SA 4.0). Adopters redistributing TikiTribe content under their own terms must preserve TikiTribe attribution per the MIT license.
- The repository uses a `<category>/<subdir>/CLAUDE.md` pattern (one CLAUDE.md per category subdirectory), which differs from the GRC Library pack's `core/`, `ai/`, etc. flat-file layout. The overlay placement under `.claude/rules/external/tikitribe/` should preserve the upstream directory structure so the consumer can map fetched files back to upstream.
- Coverage is broader than the GRC Library pack: 12 languages (including R, Julia, SQL), 16 backend / AI-ML frameworks (FastAPI, Express, Django, Flask, NestJS, LangChain, CrewAI, AutoGen, BentoML, MLflow, Modal, Ray Serve, TorchServe, Transformers, Triton, vLLM), plus dedicated `frontend/`, `iac/`, `containers/` categories. Consumers with stacks in those areas may benefit materially from the overlay.

**Verdict:** Vetted (no concerns).

**Status:** `Vetted`

**Re-vet cadence:** Standards-currency cadence (annual). Re-vet immediately if upstream TikiTribe materially expands scope (for example, adds shell-execution helpers, external fetch instructions, or any pattern that the back-port cadence would not have inspected as substantive content). Spot-checks beyond the representative sample above are at the maintainer's discretion when back-porting individual files.

### Implicit vet via back-port cadence (pre-2026-05-31; historical, superseded by the entry above)

**Vet method:** Back-port cadence review. The library maintainer reviewed TikiTribe diffs as part of the routine back-porting of vetted improvements into the GRC Library pack ([`dev-security/README.md`](../README.md) §"External projects and reference sources" records the back-port practice). No standalone EXT-01 pattern scan had been performed on the current upstream state of the repository at that time.

**Files reviewed:** Not enumerated explicitly. Back-port-by-back-port basis, focused on the rule files actually incorporated.

**Findings:** No concerns surfaced during back-port reviews to date.

**Verdict (historical):** Vetted with caveats. The back-port-cadence record is a substantive but informal vet; a formal EXT-01 pattern scan against the current upstream state had not been performed. **Superseded by the 2026-05-31 formal EXT-01 vet above.**

**Status (historical):** `Vetted with caveats` -> superseded by `Vetted` on 2026-05-31.

---

## Source: Wiz Secure Rules Files

**Repository:** `https://github.com/wiz-sec-public/secure-rules-files`

### Vet 2026-05-31 (first formal EXT-01 vet)

**Vet method:** WebFetch + EXT-01 protocol, performed by the library maintainer via a Claude Code session. Supersedes the prior back-port-cadence-only record (preserved below).

**Files reviewed (representative sample across categories):**

- [`README.md`](README.md)
- `prompt.md` (Wiz's upstream generator prompt, used to produce the per-stack rule files; not itself a file the overlay would place in a consumer's project)
- `python/flask/CLAUDE.md`
- `python/django/CLAUDE.md`
- `java/spring/CLAUDE.md`
- `javascript/node.js/CLAUDE.md`
- `c/CLAUDE.md`
- `hcl/terraform/CLAUDE.md`

The Wiz repository structure: a root generator (`generate_rules.py` plus `prompt.md`) produces per-language/framework rule files under `python/`, `javascript/`, `java/spring/`, `.net/asp.net_core/`, `c/`, `hcl/terraform/`, `yaml/cloudformation/`. Each leaf directory contains the same content rendered for multiple AI coding assistants (`CLAUDE.md`, `AGENTS.md`, `.clinerules`, `.windsurfrules`, `.mdc` for Cursor, `copilot-instructions.md`, `CONVENTIONS.md`). The overlay step would fetch the `CLAUDE.md` variant from each elected leaf directory.

**EXT-01 pattern scan results across the consumer-consumed rule files (the eight files excluding `prompt.md`):**

| Pattern | Outcome |
|---|---|
| Role-override / "ignore previous instructions" | Not present. Content frames secure-coding rules as guidance, not directives that override the assistant. |
| Urgency framing or pre-authorization language | Not present. |
| External URL fetch directives | Not present. References to OWASP / CWE are standard citations. |
| Shell command execution beyond standard setup documentation | Not present. Code examples are secure-pattern demonstrations. |
| Security control weakening | Not present. Every rule strengthens controls (CSRF protection, parameterized queries, secure headers, input validation, least privilege). |
| Hidden text, base64 blobs, or encoded directives | Not present. Plain UTF-8 markdown with readable code blocks. |

**EXT-01 pattern scan for `prompt.md` (the upstream generator prompt):**

A separate WebFetch review of `prompt.md` flagged four items: an opening "You are an expert software engineer..." role-priming line; an output-format constraint ("Your response should only be the generated cursor rules file, properly formatted, and nothing else"); strong modal language ("Adhere strictly to best practices..."); and a Cursor frontmatter value constraint ("`alwaysApply: MUST BE false`"). On consideration, all four flagged items are **standard LLM prompt-scaffolding patterns** (role priming, output-only-the-result constraints, emphatic style directives, schema-field value constraints) that are widely used in legitimate code-generation prompts. None of them are prompt-injection vectors against a consumer's Claude Code session: `prompt.md` is a development-time artefact Wiz uses to *generate* the per-stack rule files; it is not itself fetched into a consumer's project by the overlay step. The downstream rule files that would actually be placed in a consumer's project all pass cleanly.

**Verdict:** Vetted (no concerns for consumer-consumed rule files). The upstream generator prompt uses standard LLM scaffolding patterns that are over-flagged by conservative pattern scans but do not propagate as injection vectors into the generated rules. Documented for transparency.

### Substantive observations (not vetting concerns, listed for the consumer's awareness)

- **License is CC-BY-NC-ND-4.0** (Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International). This is a **significant caveat** relative to the GRC Library pack (CC BY-SA 4.0) and TikiTribe (MIT): adopters whose use case is commercial, or who want to modify the rule files for their stack, must obtain separate permission from Wiz Inc. or use the content under fair-use principles that vary by jurisdiction. The library does NOT recommend Wiz to commercial-adopter consumers without a license review. The overlay step's offer-message for Wiz should surface this prominently so the consumer makes an informed choice.
- Per-leaf-directory multi-format pattern (CLAUDE.md alongside AGENTS.md, .clinerules, etc.) is a useful adoption convenience. The overlay step only needs to fetch one variant per directory (CLAUDE.md is the natural choice for Claude Code consumers).
- Scope: Python (Flask, Django), JavaScript (React, Node.js), Java (Spring), .NET (ASP.NET Core), C, HCL (Terraform), YAML (CloudFormation). Narrower than TikiTribe but covers the major web stacks plus IaC.

**Status:** `Vetted`

**Re-vet cadence:** Standards-currency cadence (annual). Re-vet immediately if Wiz's license changes, or if the upstream `prompt.md` or any leaf rule file is materially expanded (in particular: any shift toward output-format directives that would alter how a consumer's assistant treats the rules).

### Implicit vet via back-port cadence (pre-2026-05-31; historical, superseded by the entry above)

**Vet method:** Back-port cadence review. Same posture as TikiTribe historical entry: the library maintainer reviewed Wiz content while back-porting language-specific improvements, but no standalone EXT-01 pattern scan against the current upstream state had been recorded at that time.

**Files reviewed:** Not enumerated explicitly. Back-port-by-back-port basis.

**Findings:** No concerns surfaced during back-port reviews to date. License (CC-BY-NC-ND-4.0) was not surfaced as a substantive observation in the back-port-cadence record; the 2026-05-31 formal vet adds that observation.

**Verdict (historical):** Vetted with caveats. **Superseded by the 2026-05-31 formal EXT-01 vet above.**

**Status (historical):** `Vetted with caveats` -> superseded by `Vetted` on 2026-05-31.

---

## How adopters use this log

The setup generator's optional external-source overlay step ([`setup-generator-prompt.md`](setup-generator-prompt.md) Phase 2) reads the status fields above and surfaces them to the consumer at the offer step. A consumer running the generator in their own Claude Code session sees:

- For sources marked `Vetted` (currently: Kariedo, TikiTribe, addyosmani, Wiz): "Library maintainer has applied EXT-01 vetting to this source as of `<vet date>`. The consumer is still expected to verify the fetched content matches the maintainer's record (the SHA-256 provenance header in each placed file enables this) and to apply their own EXT-01 review. Any substantive observations (such as licensing caveats) are recorded in the source's vetting-log section and should be surfaced to the consumer at the offer step."
- `Vetted with caveats` is not currently in use for any source. Reserved for future sources where the maintainer has performed only an informal review.
- For sources marked `Not yet vetted`: "Library maintainer has not vetted this source. Consumer assumes full EXT-01 responsibility per fetch."
- For sources marked `Withdrawn`: "Source has been removed from the library's reference list; do not include."

The consumer's decision is informed but their own; the maintainer's vetting log is one input, not a guarantee.
