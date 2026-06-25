# AI Security Tooling Landscape Register

**Document Title:** AI Security Tooling Landscape Register\
**Document Type:** Register\
**Version:** 1.1.3\
**Date:** 2026-06-25\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/register-canonical-citations.md`](register-canonical-citations.md), [`governance/specification-citation-verification.md`](specification-citation-verification.md), [`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md), [`ai/standard-ai-model-risk.md`](../ai/standard-ai-model-risk.md), [`ai/guide-ai-adversarial-test-reference.md`](../ai/guide-ai-adversarial-test-reference.md), [`dev-security/guideline-ai-coding-assistant-security.md`](../dev-security/guideline-ai-coding-assistant-security.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual, and on material change to the AI security tooling landscape (project archival, license change, vendor acquisition, major version release)\
**Repository Path:** [`governance/register-ai-security-tooling-landscape.md`](register-ai-security-tooling-landscape.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This register documents the AI security tooling landscape originally surveyed in Wave 1 and Wave 2 of the external-project assessment that informed Phases 23.1 through 23.6 of the library, with subsequent additions and provenance-block enrichment through Phase 23.10 and beyond. It records, for each project: scope, license, library reference status, key capabilities, and the GRC concern or gap each project surfaced for the library's content.

Unlike the Canonical Citations Register, which records citations that library content uses authoritatively, this register is a landscape catalogue. It serves three purposes:

- **Adopter orientation**: organisations adopting library content can use this register to find concrete tooling choices that implement the abstract controls in the library standards.
- **Future-content backing**: as the library expands its AI security coverage, this register identifies the tools and threat-class definitions that converge across multiple independent projects.
- **GRC gap traceability**: each entry records the specific concern or gap the project surfaced, providing an audit trail back to why a given control or threat class exists in the library.

This register is **not** a recommendation list or an endorsement. Inclusion does not imply suitability, fitness, or adoption. Adopting organisations perform their own evaluation against the criteria in the relevant library standards.

---

## 2. Scope

This register includes:

- All 14 directly-provided external projects assessed in Wave 1 of the external-project assessment.
- All ~38 inner-linked projects assessed in Wave 2.
- Projects in both open-source and commercial deployment models, treated at the depth their public documentation supports.

It excludes:

- Projects with no public documentation or source.
- Projects discovered after the Wave 2 cutoff date (2026-05-30); future additions are made through register-version bump per the maintenance section.

---

## 3. How to read this register

Each project block records:

- **Scope**: one sentence describing what the project is and does.
- **License**: SPDX-compatible identifier or "Commercial" / "Proprietary".
- **Library reference status**: one of "Cited" (the project is named in a library document), "Referenced as exemplar" (the project's pattern is reflected in library control language without being named), "Surveyed only" (the project was investigated but neither cited nor referenced).
- **Key capabilities**: bulleted enumeration of the project's documented technical capabilities.
- **GRC concern surfaced**: the specific gap or governance concern this project surfaced for the library.
- **Status notes**: archive status, deprecation, acquisition, or other lifecycle information.
- **Provenance** (added Phase 23.10): traceability anchors for the entry's claims:
  - **Source URL**: the canonical project URL the assessment captured (project repository for open-source projects, vendor product page for commercial vendors).
  - **Version at assessment**: the project release tag, version string, or "default branch HEAD" recorded at assessment time. Where the project does not publish stable versions, the marker indicates which branch state was assessed.
  - **Date assessed**: ISO 8601 date the Wave 1 or Wave 2 agent fetched the source.
  - **Integrity anchor**: for GitHub-hosted projects, the commit SHA of the default branch at assessment time. For non-GitHub sources, the SHA-256 of the captured page content. **This field is filled by the human verifier** under the Citation Verification Specification methodology; the AI verifier records "pending human verification" at entry creation.
  - **Wayback snapshot URL**: `web.archive.org` snapshot of the source URL on the assessment date. **This field is filled by the human verifier**; `web.archive.org` is blocked in the AI verifier's sandbox.
  - **Verification status**: one of "AI-captured-pending-human-verification" (Source URL and Date assessed are AI-captured; integrity anchors are pending), "human-verified" (a human verifier has populated all provenance fields and confirmed), or "re-verification-due" (the prior human-verified entry is past the 6-month re-verification cadence and needs refresh).

The Provenance block makes the register's claims time-bounded and source-anchored: a reader in 2027 can determine that the entry reflects the project as it existed on the recorded assessment date, and can use the Wayback snapshot URL (once populated) to retrieve the publisher-attested state at that date.

Projects are grouped into nine categories. The grouping is for navigation; some projects straddle categories (Mindgard is both a red-team tool and a runtime defence, for example), in which case the project appears in its primary category with cross-references.

---

## 4. Category index

| Category | Project count | Primary library impact |
| --- | --- | --- |
| 4.1 Application-side runtime defence (open-source) | 12 | AI-SEC-INP / AI-SEC-OUT / RUNTIME-SEC controls |
| 4.2 Testing, red-team, and benchmark tools | 18 | ADTEST-SEC, REDTEAM-SEC, AGENT-SEC-15 controls; adversarial test reference |
| 4.3 ML supply chain scanners | 3 | SUPPLY-SEC-07 control |
| 4.4 AI observability platforms | 4 | AI agentic dev security standard §20 (observability and telemetry) |
| 4.5 MCP security | 1 | MCP-SEC-08 / MCP-SEC-09 / MCP-SEC-10 controls |
| 4.6 Dev-rules / coding-assistant baselines | 3 | dev-security guideline and AI security standard §9 |
| 4.7 AI pentest agents (open-source) | 7 | Pending Phase 23.9 governance |
| 4.8 Commercial runtime guardrails | 6 | Vendor-landscape orientation; not library-mandated |
| 4.9 Resource indexes | 1 | Library curated-reference candidate |

Total: 55 entries (some projects appear under bundles: Meta PurpleLlama bundles Llama Guard and CyberSecEval).

---

## 5. Project entries

### 5.1 Application-side runtime defence (open-source)

#### 5.1.1 PROMPTPurify

- **Scope**: Lightweight in-process (Node.js) prompt-injection firewall combining a deterministic structural layer and a from-scratch ONNX classifier.
- **License**: MIT (SDK and model weights); training-corpus licenses tracked in `training/CORPUS_LICENSES.json`.
- **Library reference status**: Referenced as exemplar (Phase 23.1 controls reflect its structural firewall pattern).
- **Key capabilities**:
  - Unicode normalisation: zero-width strip, BIDI smuggling defence, NFKC fold, homoglyph fold, combining-mark collapse, regional-indicator stego decode, per-sink length cap.
  - Per-call nonce fence around each untrusted input.
  - Forged chat-template token neutralisation (`<|im_start|>`, `[INST]`, `<<SYS>>`, etc.).
  - Sink-based policy: distinct rules per input class (trusted instructions, user messages, tool outputs, RAG chunks).
  - Tripwire regex flag-only layer.
  - L5e ML classifier (ONNX, ~14 MB, INT8, single-digit ms CPU inference).
  - Output guard removing markdown image URLs and tracking links to non-allow-listed domains.
- **GRC concern surfaced**: Library codified AI content safety filter mandates at high level but did not require Unicode normalisation, per-call nonces, forged-token neutralisation, sink-policy framework, or output-side silent-exfil defences. Phase 23.1 closed these gaps.
- **Status notes**: Signed npm provenance, Sigstore cosign signatures, SLSA provenance, CycloneDX SBOM. Live adversarial challenge at anton.securelayer7.net.
- **Provenance**:
  - Source URL: `https://github.com/securelayer7/PROMPTPurify`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.1.2 Protect AI llm-guard

- **Scope**: Comprehensive Python toolkit for sanitisation, harmful-language detection, data-leak prevention, and prompt-injection defence on LLM prompts and completions.
- **License**: MIT.
- **Library reference status**: Cited in Phase 23.6 register; referenced as exemplar for input/output scanner inventory in Phase 23.1.
- **Key capabilities**:
  - 16 input scanners: Anonymize, BanCode, BanCompetitors, BanSubstrings, BanTopics, Code, EmotionDetection, Gibberish, InvisibleText, Language, PromptInjection, Regex, Secrets, Sentiment, TokenLimit, Toxicity.
  - 22 output scanners: BanCode, BanCompetitors, BanSubstrings, BanTopics, Bias, Code, Deanonymize, EmotionDetection, FactualConsistency, Gibberish, JSON, Language, LanguageSame, MaliciousURLs, NoRefusal, ReadingTime, Regex, Relevance, Sensitive, Sentiment, Toxicity, URLReachability.
  - PromptInjection: DeBERTa-v3 classifier; ~7.65 ms GPU.
  - Anonymize: Microsoft Presidio + custom regex; default entities include credit cards, person names, phone numbers, emails, IPs, UUIDs, US SSNs, crypto wallets, IBAN.
  - Secrets: Yelp detect-secrets library; AWS/Azure/GitHub/Slack/private keys.
  - InvisibleText: strips Unicode Cf/Cc/Co/Cn categories.
  - MaliciousURLs (output): CodeBERT classifier with default threshold 0.7.
  - URLReachability (output): network-fetch check of LLM-emitted URLs.
  - Deanonymize: PII placeholder re-injection paired with Anonymize.
- **GRC concern surfaced**: Demonstrates that input/output scanner inventory should be enumerated as discrete control categories rather than abstract "content safety filter". OWASP LLM Top 10 per-scanner mapping pattern.
- **Status notes**: Ships as Python library and `llm_guard_api` HTTP service. ONNX optimisation supported.
- **Provenance**:
  - Source URL: `https://github.com/protectai/llm-guard`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.1.3 Protect AI rebuff

- **Scope**: Self-hardening prompt-injection detector with four-layer defence pipeline and learning canary-token loop.
- **License**: Apache-2.0.
- **Library reference status**: Cited in Phase 23.6 register; archive flagged.
- **Key capabilities**:
  - Layer 1: Heuristics: deterministic filters for known malicious-prompt shapes.
  - Layer 2: Dedicated LLM detector: separate LLM classifies whether the input is injection.
  - Layer 3: VectorDB: Pinecone or Chroma; embedding similarity to known attacks; self-hardening write-back.
  - Layer 4: Canary tokens: secret-token insertion; leakage detected if token appears in completion.
  - Python and JS/TS SDKs.
- **GRC concern surfaced**: Demonstrates the multi-layer pattern that has converged across the field: deterministic + ML + similarity-to-known-attacks + canary tokens.
- **Status notes**: Archived May 2025 (read-only).
- **Provenance**:
  - Source URL: `https://github.com/protectai/rebuff`
  - Version at assessment: archived May 2025
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.1.4 ClawGuard

- **Scope**: Runtime security sidecar daemon for tool-augmented LLM agents (OpenClaw), defending against indirect prompt injection by intercepting tool calls.
- **License**: MIT.
- **Library reference status**: Referenced as exemplar (Phase 23.4 MCP-SEC-08/09/10, Phase 23.1 output URL allow-listing).
- **Key capabilities**:
  - Layer 1: Gateway tool block: native OpenClaw tools disabled; restricted to `cg_*` replacements.
  - Layer 2: Rule engine: tri-tier (blacklist / whitelist / supervised) for commands; deny-by-default for sensitive file paths; URL allow-list (npm / PyPI / OpenAI / Anthropic / docs / CDNs) and deny-list (.onion / pastebins / URL shorteners).
  - Layer 3: Sanitizer engine: 15 regex categories bidirectional on tool I/O (AWS keys, GitHub/GitLab tokens, JWT, Bearer, SSH private keys, DB connection strings, Slack/Stripe/SendGrid API keys, generic secrets).
  - Layer 4: Audit log: SQLite, 500 MB cap, 90-day retention.
  - Policy modes: strict / supervised / permissive.
  - Web dashboard for approval queue, timeline, rule editing, audit export.
- **GRC concern surfaced**: Library covered tool-call schema validation but did not articulate a sidecar/proxy interception pattern with bidirectional tool I/O sanitisation. Pattern reflected in MCP-SEC-08 (tool description scanning at load time).
- **Status notes**: Active. Two plugin variants for OpenClaw API breakage.
- **Provenance**:
  - Source URL: `https://github.com/Claw-Guard/ClawGuard`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.1.5 CourtGuard

- **Scope**: Multi-agent LLM-based prompt-injection detector using a courtroom metaphor (defence vs prosecution arguers + judge + extractor).
- **License**: MIT.
- **Library reference status**: Surveyed only (research artefact; not a candidate for production-credible mandate).
- **Key capabilities**:
  - Parallel defence and prosecution agents constructing arguments for/against injection classification.
  - Judge model rendering verdict.
  - Dedicated extractor model normalising judge output (motivated by Gemma lack of structured output).
  - Reference wiring with Gemma-3-12b, Llama-3-8b, Phi-4-mini.
- **GRC concern surfaced**: None requiring library change. Pattern is novel but not yet production-credible.
- **Status notes**: Research artefact; sparse README.
- **Provenance**:
  - Source URL: `https://github.com/isaacwu2000/CourtGuard`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.1.6 NVIDIA NeMo Guardrails

- **Scope**: Programmable rails framework wrapping LLM conversations with input/output/dialog/retrieval/execution controls via the Colang DSL.
- **License**: Apache 2.0.
- **Library reference status**: Cited in Phase 23.6 register; referenced as exemplar for the 5-rail-category framework in Phase 23.1 commentary.
- **Key capabilities**:
  - 5 rail categories: Input, Output, Dialog, Retrieval, Execution.
  - LLM self-checking: self check input, self check output, self check facts, self check hallucination, content safety check input/output.
  - NVIDIA NIM safeguard models (Content Safety, Topic Safety).
  - Community models: AlignScore, Llama Guard, Patronus Lynx, Presidio, ShieldGemma.
  - Third-party API rails: ActiveFence, AutoAlign, Clavata, Cleanlab, GCP Text Moderation, GuardrailsAI integration, Private AI PII, Fiddler, Prompt Security, Pangea AI Guard, Trend Micro Vision One AI Guard.
  - Jailbreak detection: length-per-perplexity + prefix/suffix perplexity + random-forest on snowflake-arctic-embed.
  - Injection detection via YARA rules: code, sqli, template, xss.
- **GRC concern surfaced**: Library treated input and output as the two boundaries. NeMo's framework added dialog, retrieval, and execution as discrete enforcement points. Pattern reflected in Phase 23.4 multimodal section and runtime controls.
- **Status notes**: Active.
- **Provenance**:
  - Source URL: `https://github.com/NVIDIA/NeMo-Guardrails`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.1.7 Guardrails AI

- **Scope**: Python framework + Hub of pluggable input/output validators (RAIL specs) for LLMs.
- **License**: Apache 2.0.
- **Library reference status**: Cited in Phase 23.6 register.
- **Key capabilities**:
  - 30+ validators across PII (DetectPII, SecretsPresent), Safety (ToxicLanguage, NSFWText, DetectJailbreak, BiasCheck), Quality (GibberishText, GroundedAIHallucination), Structured Format (ValidJson, ValidPython, ValidSQL, ValidOpenAPISpec), Business (CompetitorCheck, RestrictToTopic), Similarity/RAG (SimilarToDocument, QARelevanceLLMEval), Code/Data (BugFreeSQL, BugFreePython).
  - Pydantic schema enforcement; RAIL XML spec; LLM-judge validators; reask / fix / filter / refrain / exception actions per validator.
- **GRC concern surfaced**: Demonstrates the validator-as-discrete-control pattern. Each validator addresses a specific risk and ships independently: library control language could be similarly modular.
- **Status notes**: Active.
- **Provenance**:
  - Source URL: `https://github.com/guardrails-ai/guardrails`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.1.8 Vigil-LLM

- **Scope**: Prompt-injection and jailbreak detection toolkit for LLM I/O.
- **License**: Apache 2.0.
- **Library reference status**: Cited in Phase 23.6 register; archive flagged.
- **Key capabilities**:
  - Vector-DB similarity scanner (sentence-transformers or OpenAI ada-002).
  - YARA heuristic scanner with v4.3.2 signatures.
  - Transformer scanner (deepset/deberta-v3-base-injection).
  - Prompt-response similarity scanner.
  - Canary-token scanner.
  - Sentiment analysis scanner.
  - Relevance scanner via LiteLLM judge.
  - Paraphrasing-detection scanner.
  - Prompt-entropy heuristic.
  - REST API + Streamlit UI.
- **GRC concern surfaced**: Multi-scanner layered approach reinforces the Phase 23.1 control pattern.
- **Status notes**: Alpha (v0.10.3), archived. Explicit limitation in README: "Prompt injection attacks are currently unsolvable and there is no defense that will work 100% of the time."
- **Provenance**:
  - Source URL: `https://github.com/deadbits/vigil-llm`
  - Version at assessment: v0.10.3 (alpha, archived)
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.1.9 Stacklok CodeGate

- **Scope**: Local privacy and security gateway between IDE AI coding assistants and LLM providers.
- **License**: Apache 2.0.
- **Library reference status**: Cited in Phase 23.6 register; archive flagged.
- **Key capabilities**:
  - Secrets redaction (pre-flight) with post-response unredaction (reversible pseudonymisation).
  - PII redaction: credit cards, SSNs, generic PII.
  - Dependency-risk scanning: vulnerable packages, outdated packages, hallucinated/non-existent package recommendations.
  - Malicious-package detection.
  - Security-centric review of LLM-suggested code.
  - Workspace management and model muxing.
  - Centralized credential vault.
- **Supported clients**: GitHub Copilot, Cline, Continue, Aider, Open Interpreter.
- **GRC concern surfaced**: Library covered prohibited data categories for AI coding assistants but did not articulate the reversible-pseudonymisation pattern that lets developers benefit from AI on sensitive data with reduced leakage. Phase 23.2 referenced this pattern.
- **Status notes**: Archived June 2025.
- **Provenance**:
  - Source URL: `https://github.com/stacklok/codegate`
  - Version at assessment: archived June 2025
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.1.10 LLM Warden (jackhhao)

- **Scope**: Single-purpose jailbreak-prompt classifier.
- **License**: MIT.
- **Library reference status**: Cited in Phase 23.6 register.
- **Key capabilities**:
  - Binary classifier: jailbreak vs benign.
  - 3 modes: HuggingFace transformers pipeline, Cohere classify, local training.
- **GRC concern surfaced**: None requiring library change. Demonstrates the single-purpose classifier pattern.
- **Status notes**: Active.
- **Provenance**:
  - Source URL: `https://github.com/jackhhao/llm-warden`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.1.11 KOKOSde LocalMod

- **Scope**: Fully offline self-hosted content-moderation API for text and image.
- **License**: MIT.
- **Library reference status**: Cited in Phase 23.6 register.
- **Key capabilities**:
  - Text classifiers: PII, Toxicity (4-model weighted ensemble), Prompt Injection (DeBERTa), Spam (RoBERTa), NSFW Text.
  - Image classifier: NSFW (Falconsai ViT).
  - REST API with batch and image endpoints.
  - Environment-flag-enforced offline mode.
- **GRC concern surfaced**: Demonstrates that self-hosted moderation is a viable alternative for jurisdictions where vendor-AI telemetry is unacceptable. Relevant for the data-residency requirement in [`guideline-ai-coding-assistant-security.md`](../dev-security/guideline-ai-coding-assistant-security.md).
- **Status notes**: Active.
- **Provenance**:
  - Source URL: `https://github.com/KOKOSde/localmod`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.1.12 Meta PurpleLlama bundle (Llama Guard / Prompt Guard / Code Shield / CyberSecEval)

- **Scope**: Meta's purple-team trust and safety bundle: defensive safeguard models plus offensive cybersecurity evaluation suite.
- **License**: Evals and Code Shield MIT; Llama Guard weights Llama Community License v2/v3/v3.2; Prompt Guard Llama 3.2 Community License.
- **Library reference status**: Cited in Phase 23.6 register (PurpleLlama bundle); CyberSecEval separately cited in AI safety evaluation programmes.
- **Key capabilities**:
  - Llama Guard 3: 14-category MLCommons hazard taxonomy (S1 Violent Crimes through S14 Code Interpreter Abuse). Variants 8B, 1B, 11B-vision multimodal. 128k context, 7 languages.
  - Prompt Guard: mDeBERTa-v3-base 86M/192M params; 3 labels (benign / injection / jailbreak); 8 languages; 512-token context.
  - Code Shield: inference-time filter for insecure code generation, command-execution risk, code-interpreter abuse mitigation.
  - CyberSecEval v4 test suite: MITRE ATT&CK compliance tests, False-Refusal-Rate (FRR), Secure Code Generation (Instruct + Autocomplete), Textual Prompt Injection, Visual (multimodal) Prompt Injection, Code Interpreter Abuse, Vulnerability Exploitation (X86-64 CTF), Spear Phishing Capability, Autonomous Offensive Cyber Operations, AutoPatch, CyberSOCEval (Malware Analysis MCQ + Threat Intelligence Reasoning).
- **GRC concern surfaced**: Library did not reference MLCommons hazard taxonomy or CyberSecEval. Both added in Phase 23.6 framework alignment.
- **Status notes**: Active. **Licence note for adopters:** Most of the Meta PurpleLlama bundle (Evals, Code Shield, CyberSecEval) is MIT-licensed, but the Llama Guard model weights are released under Meta's Llama Community License (not MIT). If you deploy Llama Guard in your own systems, read the Llama Community License terms before production use; it has restrictions that MIT does not (acceptable-use limits, branding rules, and a use-only-by-Meta-licensed-recipients clause).
- **Provenance**:
  - Source URL: `https://github.com/meta-llama/PurpleLlama`
  - Version at assessment: Llama Guard 3 + CyberSecEval v4
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

### 5.2 Testing, red-team, and benchmark tools

#### 5.2.1 promptfoo

- **Scope**: CLI/library for evaluating and red-teaming LLM apps with a large plugin catalog of vulnerabilities and attack strategies.
- **License**: MIT.
- **Library reference status**: Cited in Phase 23.6 register; cited in [`standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md) §21 (security testing requirements).
- **Key capabilities**:
  - 71 plugin vulnerability categories: aegis, age-bias, ascii-smuggling, beavertails, bfla, bias, bola, coding-agent, competitors, context-compliance-attack, contracts, coppa, cross-session-leak, custom, cyberseceval, data-exfil, debug-access, disability-bias, divergent-repetition, donotanswer, ecommerce, excessive-agency, ferpa, financial, gender-bias, goal-misalignment, hallucination, harmbench, harmful, hijacking, imitation, indirect-prompt-injection, insurance, intent, malicious-code, mcp, medical, memory-poisoning, model-identification, off-topic, overreliance, pharmacy, pii, pliny, policy, politics, prompt-extraction, race-bias, rag-document-exfiltration, rag-poisoning, rag-source-attribution, rbac, realestate, reasoning-dos, religion, shell-injection, special-token-injection, sql-injection, ssrf, system-prompt-override, teen-safety, telecom, tool-discovery, toxic-chat, unsafebench, unverifiable-claims, vlguard, vlsu, wordplay, xstest.
  - 30 attack strategies: audio, authoritative-markup-injection, base64, basic, best-of-n, citation, composite-jailbreaks, custom, custom-strategy, gcg, goat, hex, homoglyph, hydra, image, indirect-web-pwn, iterative, jailbreak-templates, layer, leetspeak, likert, math-prompt, meta, mischievous-user, multi-turn, other-encodings, prompt-injection, retry, rot13, tree, video.
  - Compliance framework mappings: OWASP LLM Top 10, OWASP Agentic AI, OWASP API Top 10, MITRE ATLAS, NIST AI RMF, EU AI Act, GDPR, ISO 42001, DoD AI Ethics.
  - Multi-input/multimodal attacks (image, audio, video).
- **GRC concern surfaced**: Library cited promptfoo at the use-it level but did not reflect its plugin granularity. RAG-poisoning, RAG-document-exfiltration, and RAG-source-attribution as distinct categories drove Phase 23.4 RAG-SEC-10/11/12. Memory-poisoning plugin and excessive-agency plugin drove Phase 23.4 agentic threats.
- **Status notes**: Active. Largest plugin catalog of the survey.
- **Provenance**:
  - Source URL: `https://github.com/promptfoo/promptfoo`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.2.2 NVIDIA garak

- **Scope**: Generative AI red-team scanner running named probe families paired with detectors.
- **License**: Apache 2.0.
- **Library reference status**: Cited in Phase 23.6 register; cited in [`standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md) §21.
- **Key capabilities**:
  - 40+ probe families: agent_breaker, ansiescape, apikey, atkgen, audio, av_spam_scanning, badchars, continuation, dan, divergence, doctor, donotanswer, dra, encoding, exploitation, fileformats, fitd, glitch, goat, goodside, grandma, latentinjection, leakreplay, lmrc, malwaregen, misleading, packagehallucination, phrasing, promptinject, propile, realtoxicityprompts, sata, smuggling, snowball, suffix, sysprompt_extraction, tap, test, topic, visual_jailbreak, web_injection.
  - atkgen: fine-tuned GPT-2 attacker auto-generates adversarial turns.
  - packagehallucination: slopsquatting bait.
  - visual_jailbreak: multimodal.
  - ANSI-escape terminal-injection probe.
  - leakreplay for training-data memorisation.
- **GRC concern surfaced**: packagehallucination probe reinforces dev-security DEVSEC-AI-04 (already in library) and standard-developer-security-requirements §9 hallucinated-package coverage. ansiescape and visual_jailbreak surface multimodal and out-of-band-channel threats addressed in Phase 23.4 RUNTIME-SEC-07.
- **Status notes**: Active. CI matrix Linux/Windows/macOS.
- **Provenance**:
  - Source URL: `https://github.com/NVIDIA/garak`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.2.3 Microsoft PyRIT

- **Scope**: Python framework for security professionals to compose attack converters, orchestrators, scenarios, and scorers against generative AI systems.
- **License**: MIT.
- **Library reference status**: Cited in Phase 23.6 register; cited in [`standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md) §22 / §23.
- **Key capabilities**:
  - Single-turn attacks: context_compliance, flip_attack, many_shot_jailbreak, prompt_sending, role_play, skeleton_key.
  - Multi-turn attacks: chunked_request, crescendo, multi_prompt_sending, pair, red_teaming, simulated_conversation, tree_of_attacks.
  - 75+ converters: base64, base2048, binary, bin_ascii, hex, url, json_string, atbash, caesar, rot13, leetspeak, morse, braille, nato, unicode_confusable, unicode_replacement, unicode_sub, zero_width, zalgo, random_capital_letters, character_space, insert_punctuation, diacritic, flip, superscript, selective_text, string_join, suffix_append, search_replace, translation, random_translation, scientific_translation, colloquial_wordswap, tense, tone, variation, llm_generic_text, malicious_question_generator, toxic_sentence_generator, text_jailbreak, negation_trap, charswap_attack, transparency_attack, codechameleon, ask_to_decode, denylist, persuasion, add_image_text, add_text_image, image_compression, image_resizing, image_rotation, image_color_saturation, image_overlay, image_prompt_style, audio_echo, audio_frequency, audio_speed, audio_volume, audio_white_noise, azure_speech_audio_to_text, azure_speech_text_to_audio, pdf, word_doc, add_image_to_video, qr_code, ascii_art, emoji, ecoji, noise, math_obfuscation, math_prompt, repeat_token, template_segment, word_level, plus ansi_escape and token_smuggling sub-suites.
  - Scorers: true/false (19) and float-scale (8) including audio, credential_leak, markdown_injection, prompt_shield, regex, gandalf, plagiarism, insecure_code.
  - AIRT scenarios: content_harms, cyber, jailbreak, leakage, psychosocial, rapid_response, scam.
- **GRC concern surfaced**: PyRIT's 75+ converter library drove the encoding-bypass attack-taxonomy expansion identified for [`guide-ai-adversarial-test-reference.md`](../ai/guide-ai-adversarial-test-reference.md). Multimodal converters (image/audio/video/QR/PDF/Word) drove Phase 23.4 RUNTIME-SEC-07 multimodal filtering requirements.
- **Status notes**: Active. Notebook-driven docs; broadest converter library in the survey.
- **Provenance**:
  - Source URL: `https://github.com/microsoft/pyrit`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.2.4 Confident AI deepteam

- **Scope**: Open-source LLM red-team framework targeting agents, RAG pipelines, and chatbots.
- **License**: Apache 2.0.
- **Library reference status**: Cited in Phase 23.6 register.
- **Key capabilities**:
  - 50+ vulnerability categories: Data privacy (PII Leakage, Prompt Leakage); Responsible AI (Bias, Toxicity, Child Protection, Ethics, Fairness); Security (BFLA, BOLA, RBAC, Debug Access, Shell Injection, SQL Injection, SSRF, Tool Metadata Poisoning, Cross-Context Retrieval, System Reconnaissance); Safety (Illegal Activity, Graphic Content, Personal Safety, Unexpected Code Execution); Business (Misinformation, Intellectual Property, Competition); Agentic (Goal Theft, Recursive Hijacking, Excessive Agency, Robustness, Indirect Instruction, Tool Orchestration Abuse, Agent Identity & Trust Abuse, Inter-Agent Communication Compromise, Autonomous Agent Drift, Exploit Tool Agent, External System Abuse).
  - 20+ attack methods: single-turn (Prompt Injection, Roleplay, Leetspeak, ROT13, Base64, Gray Box, Math Problem, Multilingual, Prompt Probing, Adversarial Poetry, System Override, Permission Escalation, Goal Redirection, Linguistic Confusion, Input Bypass, Context Poisoning, Character Stream, Context Flooding, Embedded Instruction JSON, Synthetic Context Injection, Authority Escalation, Emotional Manipulation); multi-turn (Linear Jailbreaking, Tree Jailbreaking, Crescendo Jailbreaking, Sequential Jailbreak, Bad Likert Judge).
  - Framework alignment: OWASP LLM Top 10 2025, OWASP Top 10 for Agents 2026, NIST AI RMF, MITRE ATLAS, BeaverTails, Aegis.
- **GRC concern surfaced**: Agentic vulnerability taxonomy (Goal Theft, Recursive Hijacking, Inter-Agent Communication Compromise, Autonomous Agent Drift) drove Phase 23.4 TC-14, TC-15 and AGENT-SEC-15/16. Tool Metadata Poisoning drove Phase 23.4 TC-12 and MCP-SEC-08. OWASP Agentic AI 2026 cited in Phase 23.6.
- **Status notes**: Active. Builds on DeepEval.
- **Provenance**:
  - Source URL: `https://github.com/confident-ai/deepteam`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.2.5 PISmith

- **Scope**: Research codebase for reinforcement-learning-trained attacker LLM auto-generating prompt-injection payloads against defended targets.
- **License**: MIT.
- **Library reference status**: Cited in Phase 23.6 register.
- **Key capabilities**:
  - RL-trained attacker via Group Relative Policy Optimization (GRPO).
  - Reports 1.00 ASR@10 / 0.87 ASR@1 against Meta-SecAlign-8B.
  - Benchmarked against nine named PI defences (secalign, none, promptguard, promptarmor, sandwich, instructional, datasentinel, piguard, datafilter).
  - Targets PIArena, AgentDojo (workspace/banking/travel/slack), AgentDyn (GitHub/DailyLife/Shopping), InjecAgent.
- **GRC concern surfaced**: Library mandated static adversarial test updates quarterly but did not acknowledge RL-trained adaptive attackers. Drove Phase 23.4 TC-16 and Phase 23.5 §5.5.
- **Status notes**: Research artefact; expects vLLM/local GPU for training.
- **Provenance**:
  - Source URL: `https://github.com/albert-y1n/PISmith`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.2.6 Promptmap

- **Scope**: YAML-rule-driven prompt-injection scanner for custom LLM apps and HTTP-fronted LLM endpoints.
- **License**: GPL-3.0.
- **Library reference status**: Cited for reference; adopter licence caveat (see Status notes).
- **Key capabilities**:
  - 69 rules across 6 directories: jailbreak (23), prompt_stealing (11), harmful (13), distraction (7), hate (11), social_bias (4).
  - Modes: white-box (caller supplies system prompt and target model), black-box (caller supplies HTTP endpoint with YAML request template), firewall mode (test guardrail LLMs).
  - Dual-LLM architecture (target + controller judge).
  - Native black-box HTTP testing with arbitrary headers/encoding/proxy.
- **GRC concern surfaced**: YAML-rule-driven prompt-injection scanner with 69 rules across 6 categories (jailbreak, prompt-stealing, harmful, distraction, hate, social bias); black-box HTTP testing and firewall mode complement the library's coverage of prompt-injection testing approaches.
- **Status notes**: Active. **Licence note for adopters:** Promptmap is GPL-3.0. If you build Promptmap into a product you ship to others, GPL-3.0 requires you to release your full product's source code under GPL-3.0 too (this is called "copyleft"). If your product is internal-only or you use Promptmap as a standalone tool (running it against your code without bundling it in), you are not affected. Check with your legal team before integrating into a shipped product.
- **Provenance**:
  - Source URL: `https://github.com/utkusen/promptmap`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.2.7 ETH Zurich AgentDojo

- **Scope**: Benchmark of tool-using LLM agents in simulated real-world environments under prompt-injection attack, scoring utility and security jointly.
- **License**: MIT.
- **Library reference status**: Cited in Phase 23.6 register (separately and as part of inspect_evals).
- **Key capabilities**:
  - 4 suites: workspace (email/calendar/cloud drive), slack (messages/web/files), banking, travel.
  - 97 user tasks and 629 security/injection test cases.
  - Attacks: manual, direct, ignore_previous, system_message, injecagent, important_instructions variants, tool_knowledge, dos, swearwords_dos, captcha_dos, offensive_email_dos, felony_dos.
  - Defences supported: tool_filter, repeat_user_prompt, spotlighting_with_delimiters, transformers_pi_detector.
- **GRC concern surfaced**: Library did not require agent benchmarking against stateful simulated environments. AgentDojo's pattern reflected in Phase 23.4 AGENT-SEC-15 (goal stability across multi-turn).
- **Status notes**: Active. Adopted by UK AISI inspect_evals.
- **Provenance**:
  - Source URL: `https://github.com/ethz-spylab/agentdojo`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.2.8 HarmBench

- **Scope**: Standardized evaluation framework comparing 18 automated red-teaming methods against 33 LLMs and defences across 510 harmful behaviours.
- **License**: MIT.
- **Library reference status**: Cited in Phase 23.6 register.
- **Key capabilities**:
  - 18 red-team methods: GCG, GCG-Multi, GCG-Transfer, PEZ, GBDA, UAT, AutoPrompt, SFS, ZS, PAIR, TAP, TAP-Transfer, AutoDAN, PAP, Human Jailbreaks, Direct Request, FewShot, EnsembleGCG.
  - 4 functional behaviour categories (standard, contextual, copyright, multimodal); 7 semantic categories (cybercrime, chemical/bio/drugs, copyright, misinformation, harassment, illegal, general harm).
  - HarmBench-CLS classifier (Llama-2-13B fine-tune).
  - R2D2 (Robust Refusal Dynamic Defense) adversarial training recipe.
- **GRC concern surfaced**: Library mandated red team evaluation but did not reference standardized method enumerations. HarmBench's 18-method matrix and R2D2 reflected in Phase 23.5 §5.4 defence categories.
- **Status notes**: Active.
- **Provenance**:
  - Source URL: `https://github.com/centerforaisafety/HarmBench`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.2.9 Trusted-AI ART (Adversarial Robustness Toolbox)

- **Scope**: Linux Foundation flagship Python library covering evasion, poisoning, extraction, and inference attacks plus defences across classical ML and DL.
- **License**: MIT.
- **Library reference status**: Cited in Phase 23.6 register.
- **Key capabilities**:
  - 40+ evasion attacks: FastGradientMethod, ProjectedGradientDescent, BasicIterativeMethod, CarliniL2/LInf/L0Method, DeepFool, NewtonFool, ElasticNet, JSMA, UniversalPerturbation, AdversarialPatch, BoundaryAttack, HopSkipJump, SquareAttack, ZooAttack, SimBA, SpatialTransformation, ThresholdAttack, PixelAttack, Wasserstein, FrameSaliencyAttack, ShadowAttack, GeoDA, BrendelBethgeAttack, FeatureAdversaries, AutoAttack, AutoProjectedGradientDescent, AutoConjugateGradient, DPatch, RobustDPatch, OverTheAirFlickering, ImperceptibleASR, MalwareGDTensorFlow, LowProFool, GraphiteBlackbox/Whitebox, SignOPTAttack, RescalingAutoConjugateGradient.
  - Poisoning attacks: PoisoningAttackBackdoor, CleanLabelBackdoor, PoisoningAttackSVM, FeatureCollisionAttack, BullseyePolytope, AdversarialEmbedding, HiddenTriggerBackdoor, GradientMatching, SleeperAgentAttack, BadDet variants.
  - Extraction: CopycatCNN, KnockoffNets, FunctionallyEquivalentExtraction.
  - Inference: MembershipInferenceBlackBox, LabelOnlyDecisionBoundary, LabelOnlyGapAttack, ShadowModels, AttributeInferenceBlackBox/WhiteBoxLifestyleDecisionTree/WhiteBoxDecisionTree, MIFace, DatabaseReconstruction.
  - Defences: 5 sub-types (preprocessor, postprocessor, trainer, transformer, detector) totalling 30+ defence classes.
- **GRC concern surfaced**: Library is LLM-centric. Classical ML adversarial taxonomy at ART's depth was missing. Drove Phase 23.5 §5.2 classical ML threats and §5.4 defence categories.
- **Status notes**: Active. v1.20.1 (Jul 2025). Underpins HEART.
- **Provenance**:
  - Source URL: `https://github.com/Trusted-AI/adversarial-robustness-toolbox`
  - Version at assessment: v1.20.1 (Jul 2025)
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.2.10 IBM HEART (Hardened Extension of ART)

- **Scope**: DoD-oriented T&E wrapper providing a curated, auditable subset of ART for Test and Evaluation engineers.
- **License**: MIT.
- **Library reference status**: Cited in Phase 23.6 register.
- **Key capabilities**:
  - Attacks: curated ART attacks (PGD, AdversarialPatch, HopSkipJump for image classification and object detection).
  - Estimators: MAITE-compatible model wrappers.
  - Metrics: clean accuracy, robust accuracy, perturbation distance, attack success rate, query budget.
  - Gradio low-code front-end; Jupyter notebooks.
- **GRC concern surfaced**: Demonstrates that ART-based attacks can be wrapped in a T&E governance shell. Relevant for adopters in regulated/DoD contexts.
- **Status notes**: Active. v0.7.0 (Jul 2025). Aligned to DoD CDAO/JAIC T&E protocols and MAITE.
- **Provenance**:
  - Source URL: `https://github.com/IBM/heart-library`
  - Version at assessment: v0.7.0 (Jul 2025)
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.2.11 Open-Prompt-Injection

- **Scope**: Benchmark suite for prompt-injection attacks and defences in LLM-integrated applications (USENIX Security 2024 paper).
- **License**: MIT.
- **Library reference status**: Surveyed only.
- **Key capabilities**:
  - 5 attacks: Naive, Escape Character, Ignore, Fake Completion, Combined.
  - 8+ defences: Paraphrasing, Retokenization, Data Prompt Isolation, Instructional Prevention, Sandwich Prevention, Perplexity-based, Windowed Perplexity, LLM-based detection; plus DataSentinel, PromptLocate.
  - Target tasks/datasets: SST-2, SMS Spam, HSOL, Jfleg, MRPC, RTE, Gigaword, SQuAD.
- **GRC concern surfaced**: Canonical 5-attack / 8-defence matrix is a useful reference structure for adopters but not cited directly by the library.
- **Status notes**: Academic reference implementation.
- **Provenance**:
  - Source URL: `https://github.com/liu00222/Open-Prompt-Injection`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.2.12 BCG-X ARTKIT

- **Scope**: Python framework for automating prompt-based, pipeline-style testing and evaluation of GenAI apps with challenger-bot multi-turn conversations.
- **License**: Apache 2.0.
- **Library reference status**: Surveyed only.
- **Key capabilities**:
  - Functional-pipeline composition (DAGs) with async + caching + lineage tracking.
  - Multi-turn challenger-target conversations.
  - Vendor-agnostic across OpenAI/Anthropic/Bedrock/Vertex/Azure/HF/vLLM/Ollama.
  - Q&A quality, brand-value alignment, demographic bias, safety, security (system-prompt extraction), equivalence/regression testing.
- **GRC concern surfaced**: None requiring library change. Promotes programmable-pipeline pattern (vs config-YAML) for organisations with research-style testing teams.
- **Status notes**: Active.
- **Provenance**:
  - Source URL: `https://github.com/BCG-X-Official/artkit`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.2.13 Giskard

- **Scope**: Open-source AI testing platform with modular giskard-checks (eval), giskard-scan (LLM/agent vuln scanner), giskard-rag (RAG eval/synthetic data).
- **License**: Apache 2.0.
- **Library reference status**: Cited in Phase 23.6 register.
- **Key capabilities**:
  - 55 probes across 11 categories: Hallucination & Misinformation, Harmful Content, Prompt Injection (direct + indirect), Robustness (control-character/typo/unicode), Output Formatting, Information Disclosure (PII), Internal Information Exposure, Stereotypes & Discrimination, Sensitive Information Disclosure, Misuse/Off-topic, Data Leakage / Training-data extraction.
  - Native AVID taxonomy export.
  - Framework alignment: OWASP LLM Top 10, MITRE ATLAS, NIST AI RMF, EU AI Act Article 15.
  - HuggingFace Hub bot, HTML scan reports.
- **GRC concern surfaced**: Native AVID export drove the AVID reference in Phase 23.6.
- **Status notes**: Active.
- **Provenance**:
  - Source URL: `https://github.com/Giskard-AI/giskard`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.2.14 CyberArk FuzzyAI

- **Scope**: CyberArk-maintained automated LLM jailbreak/fuzzing harness with a rich attacker catalog.
- **License**: Apache 2.0.
- **Library reference status**: Surveyed only.
- **Key capabilities**:
  - Attackers: ArtPrompt, Taxonomy/persuasion, PAIR, ManyShot, ASCII Smuggling (Unicode tags), Genetic, Hallucinations (RLHF bypass), DAN, WordGame, Crescendo, ActorAttack (semantic-network multi-turn), Best-of-N, SI-Attack (shuffle inconsistency), Back-To-The-Past, History/Academic Framing, Please-prefix/suffix, Thought Experiment.
  - Plug-in classifier system.
  - Enterprise-style logging.
- **GRC concern surfaced**: ASCII smuggling and Unicode-tag attacks reinforce Phase 23.1 Unicode normalisation requirement.
- **Status notes**: Active.
- **Provenance**:
  - Source URL: `https://github.com/cyberark/FuzzyAI`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.2.15 LLMFuzzer

- **Scope**: First open-source fuzzer for LLM API integrations; pentester-oriented HTTP harness.
- **License**: MIT.
- **Library reference status**: Surveyed only.
- **Key capabilities**:
  - HTTP-endpoint-first fuzzing with proxy + dual-LLM observation.
  - Connectors: JSON-POST, RAW-POST, QUERY-GET.
  - Comparers: response delta, regex, length.
  - HTML report output.
- **GRC concern surfaced**: None.
- **Status notes**: Explicitly unmaintained.
- **Provenance**:
  - Source URL: `https://github.com/mnns/LLMFuzzer`
  - Version at assessment: default branch HEAD (unmaintained)
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.2.16 AIJack

- **Scope**: Security and privacy risk simulator for classical ML and federated learning.
- **License**: Apache 2.0.
- **Library reference status**: Cited in Phase 23.6 register.
- **Key capabilities**:
  - Evasion: Gradient-Descent Attack, FGSM, DIVA.
  - Poisoning: History Attack, Label Flip, MAPF, SVM Poisoning.
  - Backdoor: DBA, Model Replacement.
  - Free-Rider: Delta-Weight.
  - Extraction / Inversion: MI-FACE, DLG, iDLG, GS, CPL, GradInversion, GAN Attack.
  - Inference: Shadow Attack, Norm Attack.
  - Defences: Paillier (HE), DPSGD, AdaDPS, DPlis, Mondrian k-anonymity, PixelDP, Cost-Aware Robust Tree Ensemble, Soteria, FoolsGold, MID, Sparse Gradient, Model Assertions, Rain, Neuron Coverage.
  - FL schemes: FedAVG, FedProx, FedKD, FedGEMS, FedMD, DSFL, MOON, FedExP, SplitNN, SecureBoost.
- **GRC concern surfaced**: Only surveyed project with both federated-learning attacks and HE+DP defences in one library. Drove Phase 23.5 §5.3 federated-learning threats.
- **Status notes**: Active. C++/Python hybrid.
- **Provenance**:
  - Source URL: `https://github.com/Koukyosyumei/AIJack`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.2.17 AIAPwn (karimhabush/aiapwn)

- **Scope**: Automated prompt-injection scanner with recon + payload generation against arbitrary AI endpoints.
- **License**: MIT.
- **Library reference status**: Surveyed only.
- **Key capabilities**:
  - 4 operating modes: Recon, Testing Engine, Evaluation, Generation (target-adaptive payload synthesis).
  - Recon → payload-generation feedback loop.
- **GRC concern surfaced**: Adaptive payload generation reinforces the PISmith-driven Phase 23.4 TC-16 RL-trained adversary threat class.
- **Status notes**: Tiny project (~26 stars), sparse maintenance.
- **Provenance**:
  - Source URL: `https://github.com/karimhabush/aiapwn`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.2.18 UK AISI inspect_evals

- **Scope**: UK AISI / Arcadia Impact / Vector Institute community catalog of LLM evaluations running on the Inspect AI harness.
- **License**: MIT.
- **Library reference status**: Cited in Phase 23.6 register.
- **Key capabilities**:
  - Categories: Coding (HumanEval, SWE-bench, APPS, BigCodeBench, DS-1000, MBPP, competitive-programming); Assistants/Agents (GAIA, AssistantBench, OSWorld, AgentDojo, BrowseComp); Cybersecurity (CVEBench, CyberGym, Cybench, InterCode-CTF, NYU-CTF); Safeguards (StrongREJECT, MASK, ANIMA, AgentHarm, WMDP, XSTest); Mathematics; Reasoning; Knowledge; Scheming (Apollo evals, agentic-misalignment).
  - Standardized harness wrapping third-party benchmarks (HarmBench classifier, AgentDojo, AgentHarm).
  - Sandboxed Docker tool execution.
- **GRC concern surfaced**: Library did not reference UK AISI as a framework. Drove Phase 23.6 AI safety evaluation programmes section.
- **Status notes**: Active. Underpins UK Frontier AI Safety Commitments and EU AI Act Article 55 (GPAI systemic risk) testing.
- **Provenance**:
  - Source URL: `https://github.com/UKGovernmentBEIS/inspect_evals`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

### 5.3 ML supply chain scanners

#### 5.3.1 Protect AI modelscan

- **Scope**: Static scanner inspecting serialized ML model files for unsafe code that would execute on load.
- **License**: Apache-2.0.
- **Library reference status**: Cited in Phase 23.6 register; referenced as exemplar for Phase 23.3 SUPPLY-SEC-07 control.
- **Key capabilities**:
  - Supported formats: pickle, _pickle, cloudpickle, dill, joblib, H5/HDF5, Keras V3, TensorFlow SavedModel.
  - Severity model: Critical / High / Medium / Low.
  - Critical detections: Python builtins (eval, exec, compile, open, breakpoint, __import__, getattr, apply); OS/process (os, nt, posix, sys, subprocess, socket, shutil); debug/runtime (pdb, bdb, pty); serialisation (pickle, _pickle); async/runtime (asyncio, runpy); reflection (operator.attrgetter).
  - High: network/HTTP (webbrowser, httplib, requests.api, aiohttp.client); TF ops (ReadFile, WriteFile, io.MatchingFiles).
  - Medium: Keras Lambda layers, unknown/custom operators.
- **GRC concern surfaced**: Library covered model provenance and trust_remote_code=False but did not mandate scanning. Drove Phase 23.3 SUPPLY-SEC-07.
- **Status notes**: Active. Enterprise variant: Protect AI Guardian.
- **Provenance**:
  - Source URL: `https://github.com/protectai/modelscan`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.3.2 Picklescan

- **Scope**: Lightweight Python scanner detecting suspicious actions in pickle files; engine used by Hugging Face Hub-side scanning.
- **License**: MIT.
- **Library reference status**: Cited in Phase 23.6 register; referenced as exemplar for Phase 23.3.
- **Key capabilities**:
  - Iterates pickle opcode stream and flags dangerous opcodes (GLOBAL, STACK_GLOBAL, INST, OBJ, NEWOBJ, NEWOBJ_EX, REDUCE, BUILD).
  - Explicit unsafe-globals deny list including builtins eval/exec/compile/open/getattr, os.system/popen/execv, subprocess Popen/call/run/check_output, runpy modules, pickle re-entry, webbrowser.open, httplib request methods.
  - File-type sniffing by magic bytes.
  - CLI and library; can scan from URLs and Hugging Face repos.
- **GRC concern surfaced**: Demonstrates the deny-list-of-operators pattern at production-credible depth.
- **Status notes**: Active.
- **Provenance**:
  - Source URL: `https://github.com/mmaitre314/picklescan`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.3.3 Trail of Bits fickling

- **Scope**: Pickle decompiler, static analyser, taint-aware tracer, and bytecode rewriter by Trail of Bits.
- **License**: LGPL-3.0.
- **Library reference status**: Cited in Phase 23.6 register with copyleft-caution flag.
- **Key capabilities**:
  - Decompiles pickle to Python AST for analyst review.
  - Static analyser with severity tiers: LIKELY_SAFE, SUSPICIOUS, LIKELY_UNSAFE, OVERTLY_BAD.
  - Analyses: UnsafeImports, OvertlyBadEvals, NonStandardImports, UnusedVariables, BadCalls.
  - Tracing: prints opcodes and stack effects symbolically.
  - Injection: rewrites pickle to additionally execute attacker code (red-team testing).
  - Runtime guards: fickling.always_check_safety(); import hook activate_safe_ml_environment() that monkey-patches pickle.load*, torch.load, numpy.load, joblib.load.
- **GRC concern surfaced**: Severity-tier taxonomy and runtime import-hook pattern referenced in Phase 23.3 SUPPLY-SEC-07.
- **Status notes**: Active. LGPL-3.0: copyleft caution for downstream embedding.
- **Provenance**:
  - Source URL: `https://github.com/trailofbits/fickling`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

### 5.4 AI observability platforms

#### 5.4.1 LangSmith SDK

- **Scope**: Official Python/JS client SDK for LangSmith, LangChain's hosted tracing-evaluation-monitoring backend.
- **License**: MIT.
- **Library reference status**: Surveyed only; Phase 23.8 will reference if pursued.
- **Key capabilities**:
  - Run trees per invocation with inputs/outputs/intermediate steps/tool calls/retrieved documents/errors/latency/token counts/model/cost/tags.
  - Datasets, examples, feedback, evaluations, experiments, annotation queues.
  - Prompt hub (versioned prompts).
  - Webhooks and rules ("automations") firing on traces matching filters.
- **GRC concern surfaced**: AI observability platforms with security-relevant features (PII detection, key vaulting, retention controls) are absent from library §20 references. Pending Phase 23.8.
- **Status notes**: Active.
- **Provenance**:
  - Source URL: `https://github.com/langchain-ai/langsmith-sdk`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.4.2 Langfuse

- **Scope**: Open-source LLM-engineering platform (self-hostable) covering tracing, prompt management, evaluation, datasets, playground.
- **License**: MIT for OSS; commercial ee/ folders separate.
- **Library reference status**: Surveyed only; Phase 23.8 candidate.
- **Key capabilities**:
  - Nested observations with inputs/outputs/model/usage/cost/latency.
  - Sessions, users, releases, environments, tags.
  - Prompt management with version control and label-based deploy.
  - Evaluations: LLM-as-judge, code evaluators, user feedback, manual labelling queues.
  - Datasets for regression testing.
  - Security features: SSO, RBAC, audit logs (EE), encryption at rest, data masking via SDK callbacks.
- **GRC concern surfaced**: Self-hosting capability addresses data-residency constraints not explicitly handled in library AI observability content.
- **Status notes**: Active. Open-source self-hostable.
- **Provenance**:
  - Source URL: `https://github.com/langfuse/langfuse`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.4.3 Arize Phoenix

- **Scope**: Open-source AI observability and evaluation platform, OpenTelemetry/OpenInference-native.
- **License**: Elastic License 2.0.
- **Library reference status**: Surveyed only; Phase 23.8 candidate.
- **Key capabilities**:
  - Tracing via OpenInference semantic conventions.
  - Evaluators: HallucinationEvaluator, QAEvaluator, RelevanceEvaluator, ToxicityEvaluator, SummarizationEvaluator, SQLEvaluator, CodeReadabilityEvaluator, AIvsHumanEvaluator, UserFrustrationEvaluator, ReferenceLinkEvaluator.
  - Embeddings analysis with UMAP projections, drift / data-quality monitoring.
- **GRC concern surfaced**: Hallucination and toxicity evaluators provide continuous-risk-signal capability not articulated in library §20.
- **Status notes**: Active. Elastic License 2.0: not OSI-approved open source; check redistribution.
- **Provenance**:
  - Source URL: `https://github.com/Arize-ai/phoenix`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.4.4 Helicone

- **Scope**: Open-source LLM observability + AI Gateway.
- **License**: Apache 2.0.
- **Library reference status**: Surveyed only; Phase 23.8 candidate.
- **Key capabilities**:
  - Async logging (OpenLLMetry-compatible) of requests/responses/model/tokens/cost/latency/user/session.
  - AI Gateway with intelligent routing and automatic fallbacks across 100+ providers.
  - Provider-key Vault (Helicone holds provider keys; clients use Helicone tokens).
  - Per-user / per-property custom rate limits.
  - Caching, retries, moderations integration, alerts/webhooks.
- **GRC concern surfaced**: Provider-key Vault pattern is a credential-segmentation control the library has not articulated for AI dev tooling.
- **Status notes**: Active. SOC 2 + GDPR posture.
- **Provenance**:
  - Source URL: `https://github.com/Helicone/helicone`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

### 5.5 MCP security

#### 5.5.1 Lasso MCP Gateway

- **Scope**: Plugin-based local intermediary between MCP clients and downstream MCP servers, applying guardrails to every tool call and response.
- **License**: MIT.
- **Library reference status**: Cited in Phase 23.6 register; referenced as exemplar for Phase 23.4 MCP-SEC-08/09/10.
- **Key capabilities**:
  - basic plugin: token/secret masking (Azure, GitHub, GCP, AWS, JWT, GitLab, Hugging Face, collaboration-platform webhooks, Slack app tokens).
  - presidio plugin: PII masking (credit cards, IPs, emails, phone numbers, SSNs).
  - lasso plugin: real-time prompt-injection detection, harmful-content classification (calls Lasso cloud).
  - Security scanner at load time: reputation score from Smithery/NPM/GitHub (threshold 30); scans tool descriptions for hidden instructions, "ignore previous instructions" patterns, sensitive file paths, exfiltration verbs.
  - xetrack plugin: audit logging to SQLite + DuckDB.
- **GRC concern surfaced**: Tool-description-as-injection-vector pattern. Drove Phase 23.4 MCP-SEC-08 (tool description content scanning), MCP-SEC-09 (rug-pull detection via hash pinning), MCP-SEC-10 (tool-name shadowing detection).
- **Status notes**: Active. Only MCP-specific defence in the awesome-ai-security index.
- **Provenance**:
  - Source URL: `https://github.com/lasso-security/mcp-gateway`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

### 5.6 Dev-rules and coding-assistant baselines

#### 5.6.1 TikiTribe claude-secure-coding-rules

- **Scope**: Claude Code secure-coding-rules repository with AI/agent/MCP/RAG security baselines.
- **License**: MIT.
- **Library reference status**: Cited extensively in [`dev-security/guideline-ai-coding-assistant-security.md`](../dev-security/guideline-ai-coding-assistant-security.md) and [`standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md); cited in Phase 23.6 register.
- **Key capabilities**:
  - 6 _core files: owasp-2025.md, ai-security.md, agent-security.md, mcp-security.md, rag-security.md, graph-database-security.md.
  - 12 languages: cpp, csharp, go, java, javascript, julia, python, r, ruby, rust, sql, typescript.
  - 5 frontend: angular, nextjs, react, svelte, vue.
  - 16 backend: autogen, bentoml, crewai, django, express, fastapi, flask, langchain, mlflow, modal, nestjs, ray-serve, torchserve, transformers, triton, vllm.
  - 30+ RAG files (document processing, embeddings, graph stores, observability, orchestration, search/rerank, vector stores managed and self-hosted).
  - CI/CD, containers, IaC.
  - Framework alignment: OWASP (LLM, MCP, ASVS, SAMM, API, Top 10), NIST (AI RMF, SSDF), MITRE ATLAS, Google SAIF, ISO/IEC 23894, CWE Top 25.
- **GRC concern surfaced**: Already deeply integrated; the most comprehensive coding-assistant rule set in the survey.
- **Status notes**: Active.
- **Provenance**:
  - Source URL: `https://github.com/TikiTribe/claude-secure-coding-rules`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.6.2 Wiz secure-rules-files

- **Scope**: Baseline security rules compatible with Claude Code, Cursor, and Copilot; organized by language and framework.
- **License**: MIT.
- **Library reference status**: Cited in [`dev-security/guideline-ai-coding-assistant-security.md`](../dev-security/guideline-ai-coding-assistant-security.md); cited in Phase 23.6 register.
- **Key capabilities**: Language and framework baselines (less extensive than TikiTribe).
- **GRC concern surfaced**: Demonstrates the rule-file portability pattern across multiple AI coding assistants.
- **Status notes**: Active.
- **Provenance**:
  - Source URL: `https://github.com/wiz-sec-public/secure-rules-files`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.6.3 Kariedo claude-code-security-rules

- **Scope**: Modular Claude Code rules using @-syntax import system.
- **License**: MIT.
- **Library reference status**: Cited in [`dev-security/guideline-ai-coding-assistant-security.md`](../dev-security/guideline-ai-coding-assistant-security.md); cited in Phase 23.6 register.
- **Key capabilities**: Modular rules for Claude Code with @-syntax composition.
- **GRC concern surfaced**: None requiring library change.
- **Status notes**: Active.
- **Provenance**:
  - Source URL: `https://github.com/kariedo/claude-code-security-rules`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

### 5.7 AI pentest agents (open-source)

#### 5.7.1 PentestGPT (GreyDGL/PentestGPT)

- **Scope**: AI-powered autonomous penetration testing agent (USENIX Security 2024).
- **License**: MIT.
- **Library reference status**: Surveyed only; Phase 23.9 candidate.
- **Key capabilities**: Agentic pipeline; session persistence; multi-category support (Web, Crypto, Reversing, Forensics, PWN, PrivEsc); 86.5% success on 104 XBOW benchmarks (reproducible).
- **GRC concern surfaced**: AI-driven pentest agents are a new governance category. Pending Phase 23.9.
- **Status notes**: Active. USENIX-published metrics.
- **Provenance**:
  - Source URL: `https://github.com/GreyDGL/PentestGPT`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.7.2 PentAGI (vxcontrol/pentagi)

- **Scope**: Fully autonomous multi-agent system for complex penetration testing.
- **License**: MIT (note: also includes EULA.md: check before reuse).
- **Library reference status**: Surveyed only.
- **Key capabilities**: 20+ built-in security tools; vector memory (pgvector); Neo4j/Graphiti knowledge graph; isolated browser-based web intelligence; agent delegation.
- **GRC concern surfaced**: Multi-agent autonomous orchestration pattern with knowledge graph.
- **Status notes**: Active.
- **Provenance**:
  - Source URL: `https://github.com/vxcontrol/pentagi`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.7.3 AI-OPS (antoninoLorenzo/AI-OPS)

- **Scope**: Open-source LLM-backed pentest assistant for exploit dev, vuln research, code analysis.
- **License**: OSS (specific identifier not surfaced).
- **Library reference status**: Surveyed only.
- **Key capabilities**: Fully open-source LLM stack via Ollama; web search via Google; CLI + API.
- **GRC concern surfaced**: Operator-augmentation framing rather than full autonomy.
- **Status notes**: Active. URL corrected from `0v3rride/AI-OPS` (404) to canonical.
- **Provenance**:
  - Source URL: `https://github.com/antoninoLorenzo/AI-OPS`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.7.4 HackSynth (aielte-research/HackSynth)

- **Scope**: LLM agent + evaluation framework for autonomous penetration testing.
- **License**: GNU AGPLv3 (copyleft).
- **Library reference status**: Surveyed only.
- **Key capabilities**: Dual-module Planner + Summarizer; iterative command/feedback loop; CTF benchmark evaluation.
- **GRC concern surfaced**: AGPLv3 license restricts downstream commercial use; not a candidate for direct library citation as exemplar.
- **Status notes**: Active. AGPLv3 caution. URL corrected from `HSEcurity/hacksynth` (does not exist) to canonical.
- **Provenance**:
  - Source URL: `https://github.com/aielte-research/HackSynth`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.7.5 HexStrike AI (0x4m4/hexstrike-ai)

- **Scope**: MCP server enabling AI agents to autonomously run 150+ cybersecurity tools.
- **License**: MIT.
- **Library reference status**: Surveyed only.
- **Key capabilities**: 12+ specialist agents; 150+ tool integrations (Nmap, Rustscan, Nuclei, SQLMap, John, Hashcat, GDB, Radare2, Ghidra, Prowler, etc.); 35+ attack categories.
- **GRC concern surfaced**: Vendor-claimed metrics (98.7% detection, 2.1% FP) lack independent benchmark; treat with caution.
- **Status notes**: Active.
- **Provenance**:
  - Source URL: `https://github.com/0x4m4/hexstrike-ai`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.7.6 BurpGPT (aress31/burpgpt)

- **Scope**: Burp Suite extension submitting HTTP traffic to OpenAI GPT models for passive vulnerability analysis.
- **License**: Apache-2.0.
- **Library reference status**: Surveyed only.
- **Key capabilities**: Passive scan check; placeholder-based dynamic prompt customisation; multi-model OpenAI support.
- **GRC concern surfaced**: Explicit data-privacy caveat (traffic sent to OpenAI for analysis): relevant to vendor-telemetry control in dev-security guideline.
- **Status notes**: Active.
- **Provenance**:
  - Source URL: `https://github.com/aress31/burpgpt`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.7.7 Strix (usestrix/strix)

- **Scope**: Autonomous AI agents performing dynamic security testing.
- **License**: Apache-2.0.
- **Key capabilities**:
  - Full HTTP proxy with request/response manipulation.
  - Multi-tab browser automation.
  - Terminal exec, Python runtime for exploit dev.
  - Recon/OSINT, static + dynamic code analysis.
  - GitHub Actions, GitHub repos, Slack, Jira, Linear integration.
  - Attack categories: Access Control, Injection, Server-Side, Client-Side, Business Logic, Auth, Infra misconfig.
- **GRC concern surfaced**: CI/CD integration of AI pentest agents: pending Phase 23.9.
- **Status notes**: Active.
- **Provenance**:
  - Source URL: `https://github.com/usestrix/strix`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

### 5.8 Commercial runtime guardrails

**Honest caveat**: vendor data below is drawn from marketing/product pages and third-party summaries. Depth is shallower than for open-source projects.

#### 5.8.1 Lakera Guard

- **Scope**: Real-time runtime API for input/output classification protecting GenAI apps.
- **License**: Commercial SaaS.
- **Library reference status**: Surveyed only.
- **Key capabilities**: Real-time prompt-injection detection, sensitive-data exposure, policy-violation enforcement, multilingual threat detection.
- **Compliance mapping**: OWASP LLM Top 10 (contributor), AIVSS, MITRE ATLAS, NIST AI RMF.
- **Status notes**: Acquired by Check Point Nov 2025 (~$300M).
- **Provenance**:
  - Source URL: `https://www.lakera.ai/lakera-guard`
  - Version at assessment: product page content at assessment
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (SHA-256 of captured page content)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.8.2 PromptArmor

- **Scope**: LLM application security platform: data exfiltration, phishing, system manipulation.
- **License**: Commercial SaaS.
- **Library reference status**: Surveyed only.
- **Key capabilities**: Auto-updating threat detection engine; input/output/action analysis; real-time flagging; consolidated dashboard; OAuth/SSO; RBAC.
- **Status notes**: YC W24. Distinct from the research project of the same name (ICLR 2026, arXiv 2507.15219).
- **Provenance**:
  - Source URL: `https://www.promptarmor.com/`
  - Version at assessment: product page content at assessment
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (SHA-256 of captured page content)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.8.3 HiddenLayer AIM / AI Runtime Security

- **Scope**: End-to-end AI security: discovery, supply-chain, attack simulation, runtime protection.
- **License**: Commercial SaaS.
- **Library reference status**: Surveyed only.
- **Key capabilities**: AI Discovery; AI Supply Chain Security; AI Attack Simulation (ATLAS-aligned); AI Runtime Security (Detection Guardrails + Firewall); agentic runtime.
- **Compliance mapping**: NIST AI RMF, MITRE ATLAS, ISO 42001, EU AI Act.
- **Status notes**: AWS Marketplace listing.
- **Provenance**:
  - Source URL: `https://www.hiddenlayer.com/platform/ai-runtime-security`
  - Version at assessment: product page content at assessment
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (SHA-256 of captured page content)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.8.4 CalypsoAI Moderator

- **Scope**: LLM security gateway / moderation.
- **License**: Commercial SaaS.
- **Library reference status**: Surveyed only.
- **Key capabilities**: DLP (PII, code, IP); malicious-code/malware detection; full auditability; customisable scanners; ML + rule-based; adversarial simulation; RL-driven red teaming; model-agnostic.
- **Provenance**:
  - Source URL: `https://moderator.calypsoai.com/solutions`
  - Version at assessment: product page content at assessment
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (SHA-256 of captured page content)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.8.5 Mindgard

- **Scope**: Automated AI red teaming and runtime protection.
- **License**: Commercial SaaS.
- **Library reference status**: Surveyed only.
- **Key capabilities**: 170+ attack scenarios; AI reconnaissance (discovers models, agents, MCP/A2A servers, connected tools, shadow AI); runtime vulnerability detection; runtime detection-and-response.
- **Compliance mapping**: SOC 2 Type II, GDPR.
- **Status notes**: Spun out of Lancaster University.
- **Provenance**:
  - Source URL: `https://mindgard.ai/ai-security-platform`
  - Version at assessment: product page content at assessment
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (SHA-256 of captured page content)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

#### 5.8.6 SplxAI / SPLX

- **Scope**: End-to-end AI security: automated red teaming + runtime protection.
- **License**: Commercial SaaS.
- **Library reference status**: Surveyed only.
- **Key capabilities**: Automated LLM pentest covering 20+ GenAI risks; up to 95% risk-surface discovery (vendor-claimed); dynamic mitigation; runtime protection for chatbots/agents.
- **Compliance mapping**: MITRE ATLAS, OWASP LLM Top 10, EU AI Act.
- **Status notes**: Being acquired by Zscaler (pending/announced).
- **Provenance**:
  - Source URL: `https://splx.ai/`
  - Version at assessment: product page content at assessment
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (SHA-256 of captured page content)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

### 5.9 Resource indexes

#### 5.9.1 Awesome AI Security (brinhosa)

- **Scope**: Curated index of AI security, LLM security, prompt injection, red teaming, guardrail, and ML supply chain resources.
- **License**: CC0-1.0.
- **Library reference status**: Cited in Phase 23.6 register; suitable for direct library reuse.
- **Categories (21)**: About, AI Security Testing Tools, Prompt Injection Resources, Jailbreak Detection & Red Teaming, Deliberately Vulnerable AI Applications, Training/Labs/CTF Challenges, Books & Publications, Cheatsheets & Guides, Frameworks & Standards, Defense & Guardrails, Certifications & Courses, Conferences & Events, Research Papers & Datasets, Observability & Monitoring, Penetration Testing Tools, MCP Security, Awesome Lists, Podcasts & Newsletters, YouTube Channels, Other Resources, Thought Leaders.
- **GRC concern surfaced**: The awesome-ai-security index is released under CC0 (public domain). CC0 content can be freely incorporated into the GRC library's CC BY-SA 4.0 work (CC0 is the most permissive Creative Commons option, so it composes with any downstream licence). Drove the Phase 23.6 awesome-ai-security entry. Notable omissions identified during Wave 2 research: PROMPTPurify, deepteam, fickling.
- **Status notes**: Active. Continuously updated.

---
- **Provenance**:
  - Source URL: `https://github.com/brinhosa/awesome-ai-security`
  - Version at assessment: default branch HEAD
  - Date assessed: 2026-05-30 (Wave 1 / Wave 2 agent fetch)
  - Integrity anchor: pending human verification (capture commit SHA of default branch)
  - Wayback snapshot URL: pending human verification (web.archive.org blocked in AI sandbox)
  - Verification status: AI-captured-pending-human-verification

## 6. GRC gap summary

The following table cross-references the gaps surfaced by projects in this register against the phases that closed them:

| GRC gap | Closed by | Projects surfacing |
| --- | --- | --- |
| Unicode normalisation as proactive control | Phase 23.1 AI-SEC-INP-06 | PROMPTPurify, llm-guard, ClawGuard |
| Forged chat-template token neutralisation | Phase 23.1 AI-SEC-INP-07 | PROMPTPurify, promptfoo |
| Per-call nonce fences | Phase 23.1 AI-SEC-INP-08 | PROMPTPurify |
| Flag-only tripwire regex layer | Phase 23.1 AI-SEC-INP-09 | PROMPTPurify, NeMo Guardrails, Vigil-LLM |
| Output URL allow-list (silent-exfil defence) | Phase 23.1 AI-SEC-OUT-05 | llm-guard, ClawGuard, PROMPTPurify |
| Auto-fetch disabling at rendering layer | Phase 23.1 AI-SEC-OUT-06 | PROMPTPurify |
| Dev-side input scanning of files before AI consumption | Phase 23.2 | CodeGate, ClawGuard, awareness in TikiTribe |
| Dev-side output scanning of AI-generated code | Phase 23.2 | CodeGate, llm-guard |
| Session isolation for AI dev tools | Phase 23.2 | implicit across CodeGate, Helicone |
| Vendor telemetry inventory | Phase 23.2 | CodeGate, Helicone, BurpGPT |
| ML model file scanning | Phase 23.3 SUPPLY-SEC-07 | modelscan, picklescan, fickling |
| Tool metadata poisoning | Phase 23.4 TC-12, MCP-SEC-08 | Lasso MCP Gateway, deepteam |
| Multimodal injection | Phase 23.4 TC-13, RUNTIME-SEC-07 | pyrit, promptfoo, garak, HarmBench, Llama Guard 11B-vision |
| Agentic Goal Theft and Drift | Phase 23.4 TC-14, AGENT-SEC-15 | deepteam, agentdojo |
| Inter-Agent Communication Compromise | Phase 23.4 TC-15, AGENT-SEC-16 | deepteam |
| Adaptive / RL-trained adversary | Phase 23.4 TC-16, Phase 23.5 §5.5 | PISmith, AIAPwn |
| RAG test category split (poisoning / exfiltration / source-attribution) | Phase 23.4 RAG-SEC-10/11/12 | promptfoo, agentdojo |
| MCP tool-description rug-pull | Phase 23.4 MCP-SEC-09 | Lasso MCP Gateway |
| MCP tool-name shadowing | Phase 23.4 MCP-SEC-10 | Lasso MCP Gateway |
| Classical ML adversarial taxonomy | Phase 23.5 §5.2 | ART, AIJack, HEART |
| Federated-learning threats | Phase 23.5 §5.3 | AIJack |
| MLCommons hazard taxonomy reference | Phase 23.6 | Llama Guard 3 (PurpleLlama) |
| AVID reference | Phase 23.6 | Giskard |
| UK AISI reference | Phase 23.6 | inspect_evals, agentdojo |
| OWASP Agentic AI 2026 reference | Phase 23.6 | deepteam |
| HarmBench, CyberSecEval references | Phase 23.6 | HarmBench, PurpleLlama |
| AI observability platforms for security | Pending Phase 23.8 | LangSmith, Langfuse, Phoenix, Helicone |
| AI pentest agent governance | Pending Phase 23.9 | PentestGPT, PentAGI, Strix, HexStrike, BurpGPT |

---

## 7. Maintenance

- New projects entering the AI security landscape are added at the maintainer's discretion. Material additions trigger a minor version bump.
- Project status changes (archival, license change, acquisition, major version) trigger an entry update with version bump.
- Annual review confirms each entry's library reference status and capabilities, and identifies projects no longer relevant.
- Citation verification for entries in this register is managed via the Citation Verifications Register under the Q-track methodology.

### Provenance re-verification cadence

Tooling moves faster than standards. The Citation Verification Specification ([`specification-citation-verification.md`](specification-citation-verification.md)) §12 sets the re-verification cadence for canonical citations at 12 months. For this tooling register, the cadence is shorter:

- **Active open-source projects**: 6 months. Re-verification confirms the project is still active, the source URL still resolves, the recorded license has not changed, and the recorded capability claims still match the current project documentation.
- **Archived or unmaintained projects**: 12 months. The entry's archived status is reconfirmed; if the archive is removed or the project resumes maintenance, the entry transitions back to the active cadence.
- **Commercial vendors**: 6 months. Vendor product pages change frequently; the captured page content and Wayback snapshot URL anchor what was assessed.
- **Triggering events forcing immediate re-verification**: project archival, license change, vendor acquisition, major version release with material capability change, or any divergence between recorded capabilities and current project documentation.

Per-entry verification status transitions:

- `AI-captured-pending-human-verification` → `human-verified` when a human verifier populates the Integrity anchor and Wayback snapshot URL fields and confirms the captured text against the live source.
- `human-verified` → `re-verification-due` when the recorded `Date assessed` is older than the cadence above and no triggering event has occurred.
- `human-verified` → `human-verified` (with new Date assessed) when re-verification confirms the entry.
- Any status → `pending-resolution` when a triggering event occurs; resolution may be correction, removal, or transition to archived status with cadence change.

### Provenance freshness linter

The linter [`tools/lint-tooling-provenance-freshness.py`](../tools/lint-tooling-provenance-freshness.py) (shipped as gate 28 of the audit programme per [`governance/specification-audit-programme.md`](specification-audit-programme.md) §6) flags entries whose latest provenance row is past the cadence above. It parses each entry's `Date assessed` and `Verification status` and computes age using calendar-aware month arithmetic; output is structurally similar to [`tools/check-review-cadence.py`](../tools/check-review-cadence.py).

---

**End of Document**
