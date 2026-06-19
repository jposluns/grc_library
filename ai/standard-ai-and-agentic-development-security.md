# AI and Agentic Development Security Standard

**Document Title:** AI and Agentic Development Security Standard\
**Document Type:** Standard\
**Version:** 1.8.0\
**Date:** 2026-06-19\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/guide-ai-security-technical-implementation.md`](guide-ai-security-technical-implementation.md), [`ai/guide-ai-adversarial-test-reference.md`](guide-ai-adversarial-test-reference.md), [`ai/standard-ai-access-and-agent-permissions.md`](standard-ai-access-and-agent-permissions.md), [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`ai/template-system-card.md`](template-system-card.md), [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md), [`dev-security/standard-devops-security-requirements.md`](../dev-security/standard-devops-security-requirements.md), [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md), [`operations/standard-production-security-requirements.md`](../operations/standard-production-security-requirements.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material AI framework or regulatory change\
**Repository Path:** [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Scope

This standard applies to any system that incorporates:

- LLMs via managed AI inference service, third-party APIs, or self-hosted inference
- AI chat assistants, copilots, or AI-augmented interfaces
- AI-generated or AI-assisted code committed to any repository
- RAG (Retrieval-Augmented Generation) systems and vector database integrations
- Autonomous or semi-autonomous agents acting on business systems
- MCP (Model Context Protocol) servers, clients, or tool-calling integrations
- Workflow automation or integration platform workflows that invoke AI APIs or route on AI-derived outputs
- AI analytics, scoring, classification, or prediction features in any application
- AI inference infrastructure, model registries, or prompt repositories
- Claude Code, GitHub Copilot, or equivalent AI coding tools used in development

This standard does not apply to deterministic rule-based automation without LLM or ML inference.

---

## 2. Threat model

| Threat | Description |
| --- | --- |
| **T-01** Hostile inputs are inevitable | Every AI input surface, user prompts, retrieved documents, webhook payloads, email content in workflow automation, must be treated as potentially adversarially controlled. |
| **T-02** Retrieved content is untrusted | Documents, emails, database records, and web pages surfaced by RAG pipelines may carry embedded instructions. The retrieval boundary is an injection surface. |
| **T-03** AI outputs are not trusted inputs | LLM outputs must never be passed directly to shell execution, SQL queries, file operations, or downstream service calls without structural validation. |
| **T-04** Tool permissions are a privilege escalation surface | Every tool granted to an agent is a potential exfiltration or abuse channel. |
| **T-05** Agent context is a confidentiality boundary | System prompts, retrieved data, and conversation turns may contain PII, credentials, or Confidential business data. |
| **T-06** Multi-agent systems compound trust failures | Trust must not propagate implicitly through agent chains. |
| **T-07** AI-generated code has no inherent quality guarantee | It requires at minimum the same security review as human-written code: and in practice more. |
| **T-08** Model supply chain is attackable | Third-party model weights, prompt templates, and AI frameworks are supply chain risk vectors equivalent to third-party libraries. |
| **T-09** Managed AI service isolation is not sufficient | Content filter bypass, token leakage through error messages, and prompt leakage through logging are real risks in managed AI service environments. |
| **T-10** Regulatory exposure is elevated | AI systems processing personal data trigger applicable privacy legislation obligations. See Privacy Management Programme. |

---

## 3. Trust zones

| Zone | Trust Level |
| --- | --- |
| Human-authored, peer-reviewed code in main/release branch | High |
| AI-assisted code after human security review | Medium |
| AI-generated code awaiting review | Untrusted |
| User-provided prompt input | Untrusted |
| Retrieved document content (RAG) | Untrusted |
| LLM output | Untrusted until structurally validated |
| Third-party model weights | Untrusted until hash-verified |
| External MCP servers | Untrusted |
| Agent output passed to another agent | Untrusted |

Enforcement points: input validation before inference; output validation before action; tool authorization per agent role; session-scoped context isolation.

---

## 4. Security architecture principles

| ID | Principle |
| --- | --- |
| P-01 | AI components are untrusted subsystems. They must not have direct write access to production data, infrastructure configuration, or security controls. |
| P-02 | Validate at every boundary. Input validation at the API gateway does not substitute for output validation before tool execution. |
| P-03 | Require structured outputs for action-bearing responses. Validate against JSON Schema before acting. Never parse free text with regex to extract action parameters. |
| P-04 | Tool access is explicit allow-list only. Define exactly which tools each agent role may invoke. Everything else is denied. |
| P-05 | Human approval is mandatory for irreversible actions. Sending email, modifying production records, financial transactions, infrastructure changes, data deletion: all require human confirmation. No exception. |
| P-06 | Fail closed on AI errors. Malformed response or validation failure means deny the action, not fall through to a permissive default. |
| P-07 | Observability is a security control. Every inference call, tool invocation, and agent action must produce a structured audit event. |
| P-08 | Secrets never enter inference context. Credentials, API keys, and PII must not appear in system prompts, user turns, retrieved context, or tool call parameters. |

---

## 5. Secure-by-default requirements

| Parameter | Required Default |
| --- | --- |
| LLM temperature | ≤ 0.3 for action-bearing agents; ≤ 0.7 for assistants |
| Tool access | None; explicitly granted per agent role |
| Agent internet egress | Blocked; explicitly allow-listed per endpoint |
| Context persistence | Session-scoped; no cross-session memory |
| Model output | Treated as Untrusted until validated |
| RAG retrieval | Source attribution required |
| AI content filtering | Strictest available setting; documented exception required to loosen |
| Inference call logging | Enabled; request hash, response hash, token count, tool calls |
| PII in prompts | Blocked; requires data handling justification |
| AI-generated code in CI | Flagged for security review; does not auto-merge |

---

## 6. Threat classes

| Class | Description |
| --- | --- |
| **TC-01** Prompt Injection | Direct injection via user input overriding system prompt directives. Indirect injection via retrieved documents, email content, or database records containing embedded instructions. Hidden channels via unicode characters, HTML comments, or metadata fields. |
| **TC-02** RAG Poisoning | Attacker-controlled documents ingested into the vector store, including embedding poisoning: crafted documents achieving high similarity scores to displace legitimate context. |
| **TC-03** Context Contamination and Replay | Prior conversation context or retrieved content from one session leaking into another. Attacker-controlled content from an earlier turn persisted to affect later interactions. |
| **TC-04** Tool Misuse and Agent Overreach | Legitimate tools used unintendedly: bulk record extraction via a read tool, exfiltration via a send tool. Autonomous execution of shell commands, infrastructure changes, or production modifications without human approval. |
| **TC-05** Unsafe Code Generation | AI-generated code introducing SQL injection, hardcoded secrets, deprecated cryptography, path traversal, or SSRF. Hallucinated dependency names creating typosquatting risk. |
| **TC-06** Supply Chain Compromise | Backdoored model weights, compromised prompt templates, malicious fine-tuning datasets, compromised AI framework packages. |
| **TC-07** Credential and Secret Exfiltration | System prompts containing credentials leaked via injection or verbose error messages. Token leakage through API error responses. Sensitive content captured in logs. |
| **TC-08** Agent Privilege Escalation and Chain Compromise | A limited-permission agent calling a higher-privilege agent and inducing elevated permissions through crafted payloads. Compromised downstream agent injecting instructions into its response. |
| **TC-09** MCP-Specific Threats | Tool poisoning via false tool descriptions. Context contamination through MCP tool results. Permission escalation via over-scoped MCP server access. |
| **TC-10** Hallucinated Security Controls | AI-generated code that appears to implement a security control but does not: HMAC verification that skips signature checking, JWT validation that ignores expiry. |
| **TC-11** Memory Poisoning | Injected summarization introducing false information into persistent memory. Cross-session memory contamination where one user's data affects another user's memory context. |
| **TC-12** Tool Metadata Poisoning | An attacker-supplied tool exposes a description, parameter docstring, or schema text containing hidden instructions intended to influence the calling model. The injection vector is the tool definition itself, not its arguments or return values. Distinct from TC-09 in that the model never invokes the tool: it reads the catalogue. |
| **TC-13** Multimodal Injection | Adversarial content carried in non-text modalities reaches the model: text rendered in images (visual jailbreak), instructions encoded in audio that the model transcribes, embedded instructions in PDF metadata or alternative text, OCR-extracted hidden text, QR codes carrying payloads, video frames carrying instruction overlays. |
| **TC-14** Agentic Goal Theft and Drift | An agent is induced over a multi-turn session to pursue an objective different from the user-authorised goal. Goal Theft is acute substitution by adversarial input; Drift is gradual divergence driven by long-context pressure, accumulated tool feedback, or chained intermediate objectives. |
| **TC-15** Inter-Agent Communication Compromise | In a multi-agent orchestration, an upstream agent injects directives into a downstream agent through the response channel; or a sibling agent is impersonated; or message authentication is bypassed by content shape that the receiver treats as instruction. Distinct from TC-08 in that no privilege escalation is required: lateral movement is sufficient. |
| **TC-16** Adaptive / RL-Trained Adversary | An adversary uses reinforcement-learning-trained attacker models to generate payloads that adapt to observed defences. Static defensive test suites become insufficient at the rate at which adaptive attackers iterate. |

---

## 7. Mandatory input and output controls

**AI-SEC-INP-01:** All user-supplied text must pass through an AI content safety prompt shield service before reaching the LLM.

**AI-SEC-INP-02:** System prompts and user turns must use the API's native role separation. Never concatenate system instructions and user input into a single string.

**AI-SEC-INP-03:** Retrieved content must be presented in explicitly delimited context blocks framed as untrusted external data, not instructions. See the AI Security Technical Implementation Guide for the required template.

**AI-SEC-INP-04:** Maximum token budget for user input must be enforced at the application layer.

**AI-SEC-INP-05:** PII detection must run on all user inputs before logging. Detected PII must be masked before writing to any log system.

**AI-SEC-INP-06:** Untrusted input must pass through a Unicode normalisation layer before reaching the LLM. The layer applies, at minimum: NFKC normalisation (Unicode Annex 15), zero-width and format-character stripping (Unicode general categories Cf, Cc, Co, Cn), bidirectional-control character removal, homoglyph folding to a canonical script, combining-mark collapse, and a per-sink length cap. Normalisation precedes any classifier-based detection so that adversarial steganographic content is reduced to a canonical form first. Aligns with Unicode Technical Standard 39 (Security Considerations).

**AI-SEC-INP-07:** Untrusted input must have forged chat-template tokens neutralised before reaching the LLM. Examples for current deployed model families include `<|im_start|>`, `<|im_end|>`, `[INST]`, `[/INST]`, `<<SYS>>`, `<</SYS>>`, `<|system|>`, `<|user|>`, `<|assistant|>`, and `<|begin_of_text|>`. Neutralisation may be escape, removal, or HTML-style entity encoding; the requirement is that the token's role-boundary semantic is destroyed before tokenisation by the model. The set of neutralised tokens must be maintained per the deployed model family and reviewed when model versions change.

**AI-SEC-INP-08:** Structural delimiters wrapping untrusted content in prompts must use per-call nonces rather than static markers. The nonce is a cryptographically unique session-scoped string generated at prompt construction time; static markers (for example, `[DOCUMENT_START]`) used across multiple calls allow adversaries to pre-include matching delimiters in retrieved or supplied content. The nonce is unique per call, embedded in both the system instruction and the surrounding delimiter pair, and discarded after the call.

**AI-SEC-INP-09:** A tripwire layer matching known jailbreak and prompt-injection signatures must run on every untrusted input. The tripwire is flag-only by default (not authoritative block) and feeds rate-limiting, SIEM detection rules, and security-event logging. The tripwire is distinct from the content safety filter and the ML-based classifier; its purpose is signal generation and rate-control, not authoritative decisioning. Tripwire rule sets are reviewed and updated quarterly under the adversarial-testing cadence (`ADTEST-SEC-01`).

**AI-SEC-OUT-01:** LLM output driving a tool call, API call, database operation, or file operation must be validated against a JSON Schema before the action executes. Schema failure results in action denial and a security event log.

**AI-SEC-OUT-02:** LLM output must not be passed to eval(), exec(), subprocess, os.system(), or shell execution equivalents in any language.

**AI-SEC-OUT-03:** LLM output rendered in a web interface must be HTML-escaped. dangerouslySetInnerHTML, innerHTML, and equivalents with unescaped LLM output are prohibited.

**AI-SEC-OUT-04:** LLM outputs containing email addresses, URLs, or file paths must be validated against allow-lists before use in downstream operations.

**AI-SEC-OUT-05:** LLM output rendered in any user-visible surface must have outbound URLs validated against an allow-list before rendering. The control applies to URLs embedded in markdown image references, markdown hyperlinks, embedded HTML resource tags (`img`, `iframe`, `video`, `audio`, `source`, `link`, `script`), and CSS url-function references. Non-allow-listed URLs must be stripped, rewritten to a non-functional substitute, or wrapped with an out-of-band warning. The control mitigates silent exfiltration via attacker-crafted image-fetch and tracking-link vectors in adversary-controlled output.

**AI-SEC-OUT-06:** Where the deployed surface renders markdown or HTML produced by an LLM, automatic resource fetch (images, iframes, fonts, prefetched links) must be disabled by default or constrained to the same allow-list as `AI-SEC-OUT-05`. Lazy-load fallback and user-confirmation patterns are acceptable where the surface cannot disable auto-fetch globally.

---

## 8. Prohibited engineering patterns

Absolute prohibitions. No exception without written CIO/CISO approval.

| # | Prohibited | Risk |
| --- | --- | --- |
| P-01 | LLM output passed directly to shell execution (subprocess, eval, exec, os.system) | Arbitrary code execution |
| P-02 | Production credentials, API keys, or secrets in any prompt | Credential exfiltration |
| P-03 | Agent direct write access to production databases without human approval gate | Uncontrolled data modification |
| P-04 | AI-generated infrastructure code deployed without human security review | Misconfigured cloud resources |
| P-05 | AI-generated code in auth, cryptography, or access control paths without security review | Hallucinated security controls |
| P-06 | LLM conversation context persisted across user sessions without explicit consent | Context contamination, privacy breach |
| P-07 | Unsigned or unverified model weights in any system | Supply chain compromise |
| P-08 | Third-party MCP servers without security team review and approval | Tool poisoning |
| P-09 | Agent internet egress without explicit endpoint allow-list | Data exfiltration |
| P-10 | AI-generated SQL queries without parameterization | SQL injection |
| P-11 | Full prompt content including retrieved documents logged without PII masking | Sensitive data in logs |
| P-12 | Agent permissions exceeding those of a human user in the same role | Privilege escalation |
| P-13 | Irreversible actions executed without human approval | Unrecoverable production damage |
| P-14 | trust_remote_code=True when loading model weights | Arbitrary code execution at load time |
| P-15 | LLM output as innerHTML or dangerouslySetInnerHTML | XSS via AI-generated content |
| P-16 | Confidential or Restricted data sent to external AI services without a data processing agreement and CIO approval | Privacy breach, regulatory violation |
| P-17 | Multi-agent systems where downstream agents implicitly trust upstream agent output | Agent chain compromise |
| P-18 | Prompt templates hardcoded in application code without version control | Untracked prompt modification |
| P-19 | AI-suggested dependency names used without registry verification | Dependency confusion / typosquatting |
| P-20 | AI content safety filters disabled without documented exception and CIO/CISO approval | Jailbreak exposure |

---

## 9. AI-assisted development controls

### Approved tools

Approved AI coding tools:

- **Claude Code**: for development sessions with appropriate secure coding rule files deployed
- **GitHub Copilot**: within the approved organisation and tier

Use of other AI coding tools, including public web interfaces, to generate code for production systems requires CIO approval.

### Secure coding rules deployment

The library's CC BY-SA 4.0 secure-coding rules pack at [`dev-security/claude-rules/`](../dev-security/claude-rules/) is the approved Claude Code rules framework. Either copy the relevant rule files into the project's `.claude/rules/` directory (with optional `paths:` YAML frontmatter for path-scoped loading), copy [`dev-security/claude-rules/CLAUDE.md`](../dev-security/claude-rules/CLAUDE.md) to the project root as `./CLAUDE.md` or `./.claude/CLAUDE.md`, or use the AI-assisted setup generator at [`dev-security/claude-rules/setup-generator-prompt.md`](../dev-security/claude-rules/setup-generator-prompt.md). See [`dev-security/guideline-ai-coding-assistant-security.md`](../dev-security/guideline-ai-coding-assistant-security.md) for full deployment options.

| Project Type | Recommended Rule Files (from `dev-security/claude-rules/`) |
| --- | --- |
| Any project with user-facing interfaces | [`core/owasp.md`](../dev-security/claude-rules/core/owasp.md) |
| Any project incorporating AI/LLM features | [`ai/ai-security.md`](../dev-security/claude-rules/ai/ai-security.md) |
| Any project with agentic behaviour | [`ai/agent-security.md`](../dev-security/claude-rules/ai/agent-security.md) |
| Any project with RAG | [`ai/rag-security.md`](../dev-security/claude-rules/ai/rag-security.md) |
| Any project using MCP tools | [`ai/mcp-security.md`](../dev-security/claude-rules/ai/mcp-security.md) |
| Python workloads | [`languages/python.md`](../dev-security/claude-rules/languages/python.md) |
| TypeScript/Node.js workloads | [`languages/typescript.md`](../dev-security/claude-rules/languages/typescript.md) |
| .NET workloads | [`languages/csharp.md`](../dev-security/claude-rules/languages/csharp.md) |
| Java/Spring workloads | [`languages/java.md`](../dev-security/claude-rules/languages/java.md) |
| Go workloads | [`languages/go.md`](../dev-security/claude-rules/languages/go.md) |
| CI/CD pipelines | [`pipeline/cicd-gates.md`](../dev-security/claude-rules/pipeline/cicd-gates.md) |

External rule repositories (TikiTribe, Wiz, Kariedo) referenced in [`dev-security/claude-rules/README.md`](../dev-security/claude-rules/README.md) are URL pointers only; per the trust-posture decision recorded in Phase 23.66, they are not configured to fetch automatically at session start. Rule deployment is verified in CI per the gate matrix below; builds fail if required rule files are absent when AI-generated code is detected in the commit.

### AI-generated code requirements

**DEVSEC-AI-01:** All AI-generated code must include AI attribution disclosure in the commit message or inline comment identifying the tool and model version.

**DEVSEC-AI-02:** AI-generated code passes the same CI/CD security gates as human-written code. No exemptions.

**DEVSEC-AI-03:** The following code paths require explicit human security review regardless of origin: authentication and session management; authorization and access control logic; cryptographic operations; input validation and sanitization; database queries and ORM operations; API key and secret handling; infrastructure-as-code; CI/CD pipeline definitions; agent tool definitions and permission grants.

**DEVSEC-AI-04:** AI-suggested dependency names must be verified to exist in approved package registries before installation.

**DEVSEC-AI-05:** AI-generated IaC must pass Checkov or tfsec with no Critical findings before deployment.

**DEVSEC-AI-06:** No AI-generated code deploys to production until it passes the production onboarding security checklist gate.

### Engineering coding standards (AI modules)

| Requirement | Standard |
| --- | --- |
| Unit test coverage | ≥ 85% for all AI-enabled modules |
| SAST | OWASP-aligned (Bandit, Semgrep) mandatory per commit |
| Schema validation | Pydantic (Python) or Zod (TypeScript) on all AI API inputs |
| Dependency management | All AI dependencies pinned, hash-verified, CVE-scanned weekly |
| Structured logging | All agent actions emit structured JSON logs with trace_id, agent_id, action, result |
| AI code review | All AI code PRs require peer review plus one security reviewer |
| Secrets management | Secrets stored in secrets management service; never in code |
| Security testing | SAST and DAST reports required for every production release |
| Observability | Distributed tracing on every agent run |
| SLOs | Latency and availability thresholds defined for all AI services |

---

## 10. Agent security requirements

**AGENT-SEC-01:** Each agent must operate under a dedicated, scoped identity. Agents use managed identity or a dedicated service principal with minimum required RBAC. Shared agent identities are prohibited.

**AGENT-SEC-02:** Agent tool permissions are defined as explicit allow-lists in version-controlled configuration. Permissions embedded in system prompts do not count.

**AGENT-SEC-03:** Agents must not modify their own permission grants. Permission changes require a separate privileged process with human approval.

**AGENT-SEC-04:** In multi-agent systems, each called agent must independently authenticate the caller and validate parameters against its own policy. Trust is not inherited.

**AGENT-SEC-05:** Every tool must have an explicit schema defining allowed parameter ranges and formats. Tool calls violating the schema are rejected before execution.

**AGENT-SEC-06:** Tools that perform write operations require human confirmation before execution unless explicitly classified as low-risk and reversible in the agent's governance documentation.

**AGENT-SEC-07:** Tool invocation rate limits must be enforced per agent per tool. Limit breaches generate a SIEM alert.

**AGENT-SEC-08:** Tool responses are treated as Untrusted input and validated before being passed back into agent context.

**AGENT-SEC-09:** Email-sending tools must restrict recipient fields to an approved domain allow-list enforced at the tool layer, not in the system prompt.

**AGENT-SEC-10:** Database tools use read-only connections by default. Write access requires explicit elevation, documented justification, and human approval per write action.

**AGENT-SEC-11:** Agents must classify every proposed action as Read, Write, Send, Execute, or Deploy. Write, Send, Execute, and Deploy require human approval unless pre-approved and documented.

**AGENT-SEC-12:** A maximum autonomous action chain length must be defined per agent in its governance documentation. Reaching the limit halts the agent and requests human input.

**AGENT-SEC-13:** Agents must not spawn additional agent instances, modify their own configuration, or extend their own permissions during a session.

**AGENT-SEC-14:** Code-executing agents must run in an isolated sandbox with no network access except to explicitly allow-listed endpoints and no persistence between sessions.

**AGENT-SEC-15:** Goal stability must be tested across multi-turn agent sessions. The test exercises whether sustained pressure (prolonged context, sequential tool feedback, chained intermediate objectives, role-play framing) causes the agent to pursue a different objective from the one authorised at session start. Goal-stability tests are part of the adversarial test suite per §22; failures are P1 or P2 incidents per the AI Incident Response Plan depending on production exposure.

**AGENT-SEC-16:** Inter-agent communications must be authenticated and the receiving agent must validate the content shape before treating any portion as instruction. Specifically: an agent receiving output from another agent treats that output as Untrusted (per Trust zones §3), validates against schema before downstream use, and does not infer caller identity from content. Channel-level authentication (signed messages, mutual TLS in mesh deployments, signed envelopes with verified claims) is mandatory between any two agents that propagate authority.

**AGENT-SEC-17:** Where the deployed surface uses multiple modalities (text, image, audio, video, document upload, OCR pipeline), content from each modality must pass through a modality-appropriate adversarial-content filter before reaching the model. Text-only content safety filters are insufficient for image, audio, and document inputs.

---

## 11. RAG security requirements

**RAG-SEC-01:** Documents may only be ingested from approved source systems. Ingestion from arbitrary sources is prohibited.

**RAG-SEC-02:** Documents must be scanned at ingestion for injection patterns and PII. Documents containing detected injection patterns must be quarantined.

**RAG-SEC-03:** A SHA-256 hash of each ingested document must be stored alongside the vector embeddings to support tampering detection.

**RAG-SEC-04:** Vector store namespaces must be isolated by data classification. Confidential content must not be retrievable in contexts authorized only for Internal.

**RAG-SEC-05:** Retrieved chunks must carry source attribution metadata (document ID, source system, ingestion timestamp, hash).

**RAG-SEC-06:** Retrieval must be bounded. Maximum result count and similarity threshold must be enforced.

**RAG-SEC-07:** Retrieved chunks must be scanned for injection patterns at retrieval time, not only at ingestion time.

**RAG-SEC-08:** Documents modified since ingestion (detected by hash comparison) must not be used until re-ingested and re-validated.

**RAG-SEC-09:** Cloud vector search services must use enterprise identity provider RBAC. API key authentication must be disabled in production. Private endpoint required.

**RAG-SEC-10 (RAG Poisoning testing):** The adversarial test suite must include RAG-poisoning tests that simulate attacker-controlled documents entering the retrieval corpus and measure the influence on model behaviour. The test exercises both direct ingestion of adversarial documents (where ingestion governance is bypassed or relaxed) and embedding-space poisoning (crafted documents that achieve high similarity to legitimate context and displace it). RAG-poisoning tests are repeated at every material change to the ingestion pipeline or the embedding model.

**RAG-SEC-11 (RAG Document Exfiltration testing):** The adversarial test suite must include tests that confirm retrieval cannot return chunks from tenants, users, classifications, or data-residency scopes other than the requestor's authorised scope. The test exercises crafted queries designed to bypass the retrieval scope binding (`RAG-SEC-04`) and crafted prompts designed to induce the model to reveal retrieved-but-not-rendered content.

**RAG-SEC-12 (RAG Source Attribution testing):** The adversarial test suite must include tests that confirm retrieved-content attribution metadata (per `RAG-SEC-05`) is preserved and surfaced in user-visible output. The test exercises attempts to induce the model to misattribute content provenance, to attribute attacker-controlled content to a trusted source, or to omit attribution where attribution is required.

---

## 12. MCP security requirements

**MCP-SEC-01:** Only organisation-controlled MCP servers are permitted in production. Third-party MCP servers require security team review before any integration.

**MCP-SEC-02:** MCP server tool manifests must be signed and version-controlled. The client must verify signatures before trusting tool descriptions.

**MCP-SEC-03:** MCP servers must authenticate all client connections. No anonymous MCP connections in production.

**MCP-SEC-04:** MCP servers must implement per-tool RBAC. Server-level authentication does not grant access to all tools.

**MCP-SEC-05:** MCP tool results must be sanitized before return. Tool results are treated as Untrusted input.

**MCP-SEC-06:** All MCP server access must be logged to the SIEM with tool name, calling identity, parameter hash, and result status.

**MCP-SEC-07:** The number of MCP tools available in any given agent session must be the minimum required for the task.

**MCP-SEC-08:** MCP tool descriptions, parameter docstrings, and schema text are content that the model reads. They must be scanned at server-load time and before any session that exposes the tool to the model. The scan looks for, at minimum: forged chat-template tokens (per `AI-SEC-INP-07`), instruction-override patterns ("ignore previous instructions", role re-binding), embedded URLs to non-allow-listed hosts, steganographic Unicode (per `AI-SEC-INP-06`), and references to sensitive file paths or exfiltration verbs. Findings block tool registration in the agent's tool allow-list pending review.

**MCP-SEC-09:** Tool descriptions that change between sessions (rug-pull pattern: the server publishes one description at registration time and a different description on subsequent calls) must be detected. The agent runtime cryptographically pins the description hash at registration time and rejects any divergence on subsequent calls.

**MCP-SEC-10:** Tool-name shadowing across MCP servers must be detected. Where two MCP servers in the same agent session expose tools with the same name, the agent runtime rejects the configuration; resolution requires explicit naming or namespacing.

---

## 13. Prompt security requirements

**PROMPT-SEC-01:** System prompts must be stored in a version-controlled prompt registry or secrets management service with versioning. Changes are tracked and approved as code changes.

**PROMPT-SEC-02:** System prompts must include explicit statements of what the agent may and may not do, including an explicit instruction for handling override attempts.

**PROMPT-SEC-03:** Prompt templates inserting user input or retrieved content must use structural delimiter patterns separating instruction context from data context. See the AI Security Technical Implementation Guide for required templates.

**PROMPT-SEC-04:** System prompts must not contain secrets, credentials, internal hostnames, or data classified above Internal.

**PROMPT-SEC-05:** Every production system prompt must have a corresponding prompt test suite covering functional correctness, injection resistance, boundary conditions, and adversarial inputs.

**PROMPT-SEC-06:** Prompt test suites run in CI on every change. A system prompt change causing regression in injection resistance tests is rejected.

---

## 14. Context isolation requirements

**CTX-ISO-01:** Each user session must have a dedicated, isolated context buffer enforced at the application layer.

**CTX-ISO-02:** Multi-tenant AI deployments must enforce tenant isolation at the infrastructure layer. Prompt-only isolation is insufficient and prohibited as the sole isolation mechanism.

**CTX-ISO-03:** Context windows are bounded by both token count and time-to-live. Unbounded context accumulation is prohibited.

**CTX-ISO-04:** Context that includes retrieved documents must tag each chunk with source identifier, sensitivity classification, and retrieval timestamp.

---

## 15. Memory security requirements

**MEM-SEC-01:** Persistent cross-session memory is prohibited by default. Enabling it requires design approval and a Privacy Impact Assessment. See Privacy Management Programme.

**MEM-SEC-02:** Where approved, persistent memory must be implemented as explicit, user-visible records with user consent. Users must be able to view, edit, and delete their memory records.

**MEM-SEC-03:** Memory stores must be access-controlled per user identity. Cross-user memory access is prohibited.

**MEM-SEC-04:** Memory content containing Confidential or Restricted data must be encrypted at rest with customer-managed keys and access-logged.

**MEM-SEC-05:** Memory records must have a maximum retention TTL and must be automatically purged on expiry. See Data Retention Schedule for applicable periods.

---

## 16. Runtime enforcement controls

**RUNTIME-SEC-01:** All production AI systems must have AI content safety filters enabled. Hate, self-harm, sexual content, violence, jailbreak detection, and indirect attack detection must be active at the highest available sensitivity.

**RUNTIME-SEC-02:** Content safety filter changes are High-risk changes requiring security team approval. Disabling or loosening filters requires CIO/CISO approval.

**RUNTIME-SEC-03:** Content safety block events must be logged to the SIEM with the request hash and block category.

**RUNTIME-SEC-04:** All AI endpoints must implement per-user and per-tenant rate limiting enforced at the API management gateway.

**RUNTIME-SEC-05:** Token budget limits must be enforced per session, per user, and per day.

**RUNTIME-SEC-06:** Anomalous usage must generate SIEM alerts.

**RUNTIME-SEC-07 (Multimodal content filtering):** Where the deployed surface accepts non-text inputs (images, audio, video, PDF, Office documents, OCR pipelines, QR-code scanners), each modality must pass through a modality-appropriate adversarial-content filter before reaching the model. Filtering categories per modality, at minimum:

- **Image**: visual jailbreak detection (text rendered in images), embedded-instruction detection (instruction-shaped overlays, alt-text injection), NSFW classifier, optical-character-recognition pass that subjects extracted text to the same controls as user input.
- **Audio**: speech-to-text transcription pass that subjects extracted text to the same controls as user input; adversarial-audio detection where the model is known to be vulnerable to acoustic perturbations.
- **Video**: per-frame visual filtering plus per-frame OCR pass; audio-track filtering.
- **PDF / Office documents**: text-extraction pass subjecting extracted text to the same controls as user input; metadata field scanning; embedded-resource (images, attachments) scanning; macro detection and rejection where the surface does not execute macros.
- **OCR**: extracted text is treated as Untrusted input (per Trust zones §3) and re-enters the input pipeline at `AI-SEC-INP-01`.
- **QR codes**: decoded payloads are validated against URL allow-lists (`AI-SEC-OUT-05`) and instruction-pattern scanners before any tool action is taken on them.

**RUNTIME-SEC-08 (Modality-cross-contamination):** Text controls do not transfer to images. A surface that filters text but accepts images without an image-aware filter is vulnerable. Adopting organisations document, per AI system, which modalities are accepted and which modality-specific filters apply.

---

## 17. Infrastructure security requirements

**INFRA-SEC-01:** Containers hosting AI workloads must be network-integrated with egress through a cloud firewall or egress gateway with explicit allow-list rules.

**INFRA-SEC-02:** Container images for AI workloads must be built from approved base images, scanned for vulnerabilities, and stored in the container registry with image signing enabled.

**INFRA-SEC-03:** Managed AI inference service instances must use private endpoints with public network access disabled.

**INFRA-SEC-04:** AI inference service RBAC: application workloads use managed identity with minimum required role. Contributor-level roles are restricted to DevOps pipelines.

**INFRA-SEC-05:** Managed AI inference service diagnostic logs must be forwarded to the SIEM. Token consumption metrics must flow to the application telemetry platform.

**INFRA-SEC-06:** Managed AI inference service model version must be pinned. Automatic model updates must be disabled.

**INFRA-SEC-07:** All AI workload secrets are stored in the secrets management service. Direct environment variable injection is not permitted in production.

**INFRA-SEC-08:** Secrets management service hosting AI workload secrets must have soft-delete and purge protection enabled.

**INFRA-SEC-09:** On-premises servers hosting AI inference workloads are subject to physical access controls including restricted room access, access logging, and environmental monitoring.

---

## 18. AI supply chain security

**SUPPLY-SEC-01:** All AI Python packages must be pinned to specific versions with hash verification. Unpinned AI dependencies are a Critical CI finding.

**SUPPLY-SEC-02:** AI dependencies must be scanned for known CVEs on every build. Critical CVEs block deployment; High CVEs require a tracked exception.

**SUPPLY-SEC-03:** An SBOM must be generated for every production AI workload and stored with the build artifact in SPDX or CycloneDX format.

**SUPPLY-SEC-04:** Models used in production must be sourced from approved providers: managed cloud AI service (approved); open-source via cloud ML platform (approved with security review); self-hosted (require security review and malware scan).

**SUPPLY-SEC-05:** Model artifacts must have a verified provider checksum validated before deployment.

**SUPPLY-SEC-06:** Fine-tuned models must have documented dataset provenance. Training datasets from unvetted external sources require quality and bias review before production use. See Third-Party AI Due Diligence Procedure.

**SUPPLY-SEC-07:** Serialized ML model files must be scanned for unsafe operators before being loaded by a production process or accepted into a model registry. Scope and pattern:

1. **In-scope file formats**: pickle and pickle-derived (`.pkl`, `.pickle`, `cloudpickle`, `dill`, `joblib`), PyTorch (`.bin`, `.pt`, ZIP-based PyTorch archives), HDF5 (`.h5`), Keras V3, TensorFlow SavedModel (Protocol Buffer), NumPy object arrays (`.npy` with `allow_pickle=True`).
2. **Out-of-scope (lower attack surface)**: ONNX, Safetensors, GGUF, TensorRT plan files. These restrict to ML computation without code execution at load time. Weight manipulation remains theoretically possible but is not addressed by file-content scanning.
3. **Required detection categories** (Critical severity, deployment blocking unless explicitly accepted by CISO):
   - Python builtins enabling code execution: `eval`, `exec`, `compile`, `open`, `breakpoint`, `__import__`, `getattr`, `apply`.
   - OS / process / network modules: `os`, `nt`, `posix`, `sys`, `subprocess`, `socket`, `shutil`.
   - Debug and runtime: `pdb`, `bdb`, `pty`, `asyncio`, `runpy`.
   - Serialisation re-entry: `pickle`, `_pickle`.
   - Reflection: `operator.attrgetter`, `getattr` chains.
   - For Keras: `Lambda` layers carrying code objects.
4. **High severity** (deployment requires documented justification): network/HTTP modules (`webbrowser`, `httplib`, `requests.api`, `aiohttp.client`), TensorFlow file-IO operations (`ReadFile`, `WriteFile`, `io.MatchingFiles`).
5. **Medium severity** (review before adoption): unknown custom operators lacking a parent-library mapping.
6. **Adoption gate**: every model artefact entering the model registry from outside the organisation (Hugging Face Hub, vendor download, supplier delivery) passes through this scan before the registry entry is approved. The scan is repeated when the artefact version changes.
7. **Production-load gate**: production AI workloads loading model artefacts at runtime use scanner-aware loaders or run with `trust_remote_code=False` (per `P-14` in §8) and rely on the adoption-gate scan as the integrity record.
8. **Exception path**: organisations may grant a CISO-approved exception for a model artefact that requires a Critical operator for legitimate reasons; the exception is recorded in the AI risk register with compensating controls (network isolation of the loading host, restricted-identity execution).

The control is informed by the byte-level scanning patterns established by open-source tools modelscan (Apache-2.0), picklescan (MIT, the engine used by Hugging Face Hub-side scanning), and fickling (LGPL-3.0, pickle decompiler and symbolic tracer). Tool choice is at the organisation's discretion; the deny-list categories above are the minimum coverage. The scanner must produce a machine-readable report retained alongside the model registry entry.

---

## 19. CI/CD pipeline controls

Every CI/CD pipeline for AI-enabled systems must include the following gates in addition to the standard DevOps pipeline gates:

| Gate | Tool | Failure Condition |
| --- | --- | --- |
| Secret scanning (AI API key patterns) | gitleaks + custom AI patterns | Any secret detected → fail |
| SAST with AI-specific rules | Semgrep with AI-security rule packs (community LLM-pattern rules; Semgrep Pro AI rules where licensed). Note: Semgrep takes YAML or registry rule configs, not Markdown; the Claude Code context-rules pack (e.g., TikiTribe's `rules/_core/` markdown files) is a different artefact type and does not function as a Semgrep config. | Critical or High → fail |
| Dependency audit | pip-audit or npm audit | Critical CVE → fail; High CVE → fail within 14-day tracked exception |
| SBOM generation | syft or cdxgen | Must generate and archive every build |
| Prompt linting | Custom rules or promptfoo | Format violations, missing delimiters, hardcoded secrets → fail |
| Prompt regression testing | promptfoo | Functional or security regression → fail |
| Adversarial prompt testing | promptfoo + adversarial test suite | New injection vulnerabilities → fail |
| Container scanning | Trivy | Critical CVE in base image → fail |
| IaC scanning | Checkov | Critical AI service misconfiguration → fail |
| Secure-coding rules deployment verification | Custom CI check that confirms the pack rule files (from `dev-security/claude-rules/` or equivalents copied into `.claude/rules/`) are present in the project for the detected stack | Required rule files absent → fail |

---

## 20. AI observability and telemetry

| Event | Required Fields | Destination |
| --- | --- | --- |
| Inference request | trace_id, session_id (anonymized), model, deployment, token_count_input, timestamp | Application telemetry platform |
| Inference response | trace_id, token_count_output, latency_ms, content_filter_result, finish_reason | Application telemetry platform |
| Tool invocation | trace_id, agent_id, tool_name, parameter_hash (not values), timestamp | SIEM |
| Tool result | trace_id, tool_name, result_status, result_schema_valid | SIEM |
| Human approval event | trace_id, agent_id, action_type, approver_id, decision, timestamp | SIEM |
| Security block | trace_id, block_type, timestamp | SIEM |
| Context isolation event | session_id, event_type, timestamp | Application telemetry platform |

**OBS-SEC-01:** Full prompt content must not be logged. Log request hash and token count only.

**OBS-SEC-02:** PII detected in prompts or responses must be masked in all log systems before writing.

**OBS-SEC-03:** AI observability tooling used for the destinations above must support, at minimum: structured trace recording with semantic conventions for LLM and agent operations, hash-based content recording with selective unmasking limited to authorised operators, evaluator integration for continuous-risk-signal calculation (hallucination, toxicity, refusal-rate), data masking via SDK-side or proxy-side hooks before bytes leave the workload, and a self-hosting deployment option where data residency requires it. Reference open-source platforms implementing these requirements include Langfuse (Apache 2.0 / self-hostable), Arize Phoenix (Elastic License 2.0, OpenTelemetry/OpenInference-native), and Helicone (Apache 2.0; provider-key vault pattern). Vendor-hosted equivalents may be used where data-residency posture and contractual data-processing terms permit.

**OBS-SEC-04:** Where AI dev tooling sessions transit a vendor proxy (such as an AI gateway that mediates between client and LLM provider), the proxy is itself an AI observability surface. Logs from the proxy must be inventoried, retention defined, and access controlled equivalently to the application telemetry platform.

Log retention per Data Retention Schedule.

---

## 21. Security testing requirements

### Pre-production gate

- Prompt injection resistance (promptfoo): pass with no open findings
- Garak vulnerability scan: pass all required probe categories
- Context isolation verification: confirmed session A cannot access session B data
- Tool permission scope test: each tool operates within its defined parameter constraints
- Secret leakage test: system prompt content is not extractable via adversarial input
- Data classification boundary test: Confidential data not returned in Internal-authorized contexts
- Human approval gate test: irreversible actions blocked without explicit human confirmation
- Recovery test: for each Reversible or Compensable action class, the reversal or compensating mechanism is exercised and confirmed to return the affected system to an equivalent prior state (`AGENT-PROD-03`)

### Regression schedule

| Test Type | Frequency | Trigger |
| --- | --- | --- |
| Prompt regression (promptfoo functional) | Every PR | Any change to system prompt, model, or tool definitions |
| Injection resistance (promptfoo security) | Every PR | Any change to system prompt, model, or retrieval pipeline |
| Garak scan | Pre-release | Model version change, major system prompt change |
| PyRIT red team | Quarterly | Continuous operation; or major architecture change |
| Manual penetration test | Annually | Per Penetration Testing and Red Team Standard |

---

## 22. Adversarial testing requirements

The adversarial test suite must cover five categories on every system in scope. Required categories and test cases are in the AI Adversarial Test Reference.

**ADTEST-SEC-01:** The test suite must be updated quarterly with new techniques sourced from OWASP GenAI Security Project, MITRE ATLAS, GitHub Security Lab AI research, and internal incident-derived cases.

**ADTEST-SEC-02:** Test cases may not be removed from the suite without CISO approval.

---

## 23. Red team requirements

**REDTEAM-SEC-01:** All AI systems handling Confidential data or capable of initiating actions with financial or operational impact must undergo red team evaluation before production go-live and annually thereafter.

**REDTEAM-SEC-02:** Red team scope must include full kill chain exercise, multi-turn attack scenarios, RAG poisoning simulation, tool abuse, context contamination, and agent chain attacks where applicable. See AI Adversarial Test Reference for methodology.

**REDTEAM-SEC-03:** Critical and High red team findings block production deployment until remediated and verified.

**REDTEAM-SEC-04:** Red team tooling must include PyRIT for automated multi-turn attack simulation. Manual testing by a qualified practitioner is required in addition.

---

## 24. Human approval boundaries

| Action | Minimum Approval | Reversibility |
| --- | --- | --- |
| Send external email | Session supervisor | Low |
| Modify production database records | Named data owner | Partial |
| Delete any record or data | Named data owner + security team | None |
| Create or modify user accounts or permissions | IT administrator | Reversible |
| Deploy or modify infrastructure | DevOps lead (CIO for production) | Disruptive |
| Execute code in a production environment | DevOps lead | Partial |
| Initiate a financial transaction or workflow | Finance approver | Partial |
| Invoke an external API with real-world effects | Business owner | Varies |

---

## 25. Data security requirements

**DATA-SEC-01:** Data entering AI systems must be classified before processing. Restricted-classified data must not be sent to any external AI API.

**DATA-SEC-02:** A Privacy Impact Assessment is mandatory before deploying any AI system that processes personal data in a new way. See Privacy Management Programme.

**DATA-SEC-03:** Data minimization applies. Only the minimum personal data required for the function must be included in AI prompts or retrieval context.

**DATA-SEC-04:** Data residency requirements apply. Managed AI inference services must be deployed in approved cloud regions meeting data residency requirements.

**DATA-SEC-05:** AI systems must not retain input data beyond the session TTL unless explicit data retention authorization exists. See Data Retention Schedule.

---

## 26. Secret handling requirements

**SECRET-SEC-01:** Secrets must never appear in prompts, prompt templates, retrieved context, tool call parameters, or any payload sent to an LLM API. Absolute prohibition.

**SECRET-SEC-02:** AI workload secrets are stored in the secrets management service and injected at runtime via managed identity.

**SECRET-SEC-03:** Secret scanning in CI must include custom patterns for AI-specific secret formats: AI inference service subscription-key headers, AI API keys, model provider tokens.

**SECRET-SEC-04:** A secret detected in a prompt, retrieved document, or log file is treated as compromised. Standard rotation procedures apply.

---

## 27. Model governance requirements

**MODEL-GOV-01:** Each deployed model must have a Model Registry entry documenting: model name and version, provider, deployment date, use case, data types processed, data residency status, content filter configuration, and approved-for-production status. See AI Risk Register.

**MODEL-GOV-02:** Model version changes in production are High-risk changes per the Production Security Requirements Standard.

**MODEL-GOV-03:** Model performance and behaviour drift must be monitored. Significant output distribution changes must trigger alert and human review.

**MODEL-GOV-04:** For AI systems making or informing decisions affecting individuals, an AI Impact Assessment and Bias and Fairness Assessment are mandatory before production deployment.

**MODEL-GOV-05:** Models processing personal data must have a documented lawful basis under applicable privacy legislation. AI-generated decisions must be explainable to affected individuals on request.

---

## 28. Logging and audit requirements

**LOG-SEC-01:** All AI system operations must generate structured JSON audit logs. Minimum required log format is defined in the AI Security Technical Implementation Guide.

**LOG-SEC-02:** AI audit logs must be forwarded to the SIEM. Retention per Logging and Monitoring Standard and Data Retention Schedule.

**LOG-SEC-03:** AI audit logs must be immutable. Delete access is prohibited.

**LOG-SEC-04:** Human approval decision events must be logged with approver identity, action, timestamp, and context hash.

---

## 29. Incident detection and response

### AI incident indicators

- Confirmed prompt injection: user input or retrieved content successfully overrode system prompt behaviour
- Unexpected data exfiltration: AI output containing another user's context or above-authorized classification
- Tool scope escape: agent invoked tool parameters outside defined constraints
- Human approval gate bypass: agent performed an irreversible action without required approval
- Content filter circumvention: prohibited content generated despite active filters
- Autonomous action breach: agent performed an action outside its defined autonomous scope

### AI-specific IR additions

When an AI security incident is declared, the following steps apply in addition to the standard Incident Response Procedure:

- Immediately isolate the affected AI endpoint before diagnosing.
- Preserve conversation logs before any TTL expiry or log rotation.
- Do not reproduce adversarial inputs against the production system.
- Assess blast radius: what data was accessible, what tools were available, what actions occurred.
- Notify the CIO/CISO immediately if the incident involves data exfiltration, tool scope escape, or human approval gate bypass.
- Add a new adversarial test case derived from the attack before the system returns to production.

---

## 30. Autonomous action constraints

**AUTON-SEC-01:** AI systems operate in Supervised Autonomous mode by default. Agents may plan and prepare actions autonomously; consequential execution requires human confirmation.

**AUTON-SEC-02:** The following action categories are permanently classified as requiring human confirmation and cannot be reclassified as autonomous:

- Any action sending data outside the organisational cloud tenant
- Any action modifying a production database record
- Any action initiating a financial transaction
- Any action creating, modifying, or deleting user accounts or permissions
- Any action triggering external notification to a customer, partner, or regulator

**AUTON-SEC-03:** Actions pre-approved as autonomous must be documented in the agent's governance document, reviewed by the security team, and reassessed quarterly.

---

## 31. Secure agent orchestration

**ORCH-SEC-01:** Agent security policies are not inherited through orchestration. The orchestrator may reduce but not expand a called agent's permission set.

**ORCH-SEC-02:** Orchestrator-to-agent communications must be authenticated. An agent must verify the orchestrator's identity before acting on instructions.

**ORCH-SEC-03:** Output from one agent passed to another is treated as Untrusted input by the receiving agent.

**ORCH-SEC-04:** Circular agent invocation patterns are prohibited. Maximum orchestration depth must be defined and enforced.

**ORCH-SEC-05 (Workflow automation):** Workflow automation actions invoking AI inference must authenticate using managed identity. API key authentication requires explicit justification.

**ORCH-SEC-06 (Workflow automation):** Workflow automation actions inserting AI-generated output into database records, document stores, or email must validate AI output against a defined schema before insertion.

**ORCH-SEC-07 (Workflow automation):** AI-generated email content must be reviewed by a human before sending unless the content is classified as low-risk, tightly constrained, and that classification is documented.

---

## 32. Sandbox and isolation

**SANDBOX-SEC-01:** Agents executing code must do so in isolated sandbox containers with no persistent filesystem access, no network access except to allow-listed endpoints, CPU/memory limits, and maximum execution time limits.

**SANDBOX-SEC-02:** Sandbox containers must not have access to platform credential metadata endpoints.

**SANDBOX-SEC-03:** Sandbox environments must be ephemeral. Fresh sandbox per session. No state between instances.

**SANDBOX-SEC-04:** Sandbox isolation uses separate container environments with restricted egress profiles and no cloud RBAC permissions on the sandbox identity.

---

## 33. AI-driven offensive security tooling governance

AI-driven penetration testing and offensive security agents (PentestGPT, PentAGI, Strix, HexStrike AI, BurpGPT, and equivalent tools that run security testing autonomously or semi-autonomously) are a category that did not exist when the prior AI security standard was first written. They straddle two existing governance regimes: the Penetration Testing and Red Team Standard governs the offensive activity, and the agent-permissions and agentic-security controls in this standard govern the agent. The controls below specify how the two regimes combine for AI-driven offensive tooling.

**OFFAI-SEC-01:** AI-driven offensive security tools must be authorised under the Penetration Testing and Red Team Standard before any use against any system in any environment. Authorisation includes scope (target list with explicit allow-list), time window, rules of engagement, and approver identity. Use of an AI-driven offensive tool without prior authorisation is treated as an unauthorised security testing incident.

**OFFAI-SEC-02:** AI-driven offensive security tools are agents under §10 of this standard. Tool permissions, capability scopes (Bounded / Operational / Cross-system per the AI Access and Agent Permissions Standard), and human approval requirements apply without exception. Where the tool's vendor framing assumes broader autonomy than the library's agent permission model permits, the library's model takes precedence.

**OFFAI-SEC-03:** AI-driven offensive tools that integrate with CI/CD pipelines (for example, Strix's GitHub Actions integration) execute under a dedicated service identity with PAM-vaulted credentials per the developer-security DevOps requirements. The service identity has explicit allow-list scope; it does not run against production targets except under authorised engagements.

**OFFAI-SEC-04:** AI-driven offensive tool runs produce auditable evidence of every action taken. The audit log includes target host, action class, parameters (sanitised where they may contain secrets), result, and timestamp. The log is forwarded to the SIEM with retention per the logging and monitoring standard.

**OFFAI-SEC-05:** AI-driven offensive tools that send organisational target details, code, or data to vendor LLM backends are subject to the vendor-telemetry inventory and data-residency controls in the AI Coding Assistant Security Guideline. Where the engagement covers regulated data or in-scope-of-regulation targets, the tool's data-handling posture must satisfy the regulatory regime before use.

**OFFAI-SEC-06:** AI-driven offensive tool vendor-claimed metrics (detection rates, false-positive rates, success rates) are treated as marketing-grade and do not substitute for engagement-specific evidence of effectiveness. Where the vendor's metrics derive from published academic benchmarks with reproducible methodology, the metrics are recorded with the citation; vendor self-reported metrics without independent benchmark are recorded as such.

**OFFAI-SEC-07:** AI-driven offensive tools that use LLM-driven planning are subject to the prompt-injection threat model. A target environment containing adversarial content can attempt to manipulate the planning model. Engagements run such tools in sandbox isolation per §32 and validate the tool's planned actions against the engagement scope before execution. Tools that act on plans without per-action validation are not permitted for engagements against production targets.

**OFFAI-SEC-08:** Findings produced by AI-driven offensive tools are subject to the same triage as findings from human-driven offensive testing per the Penetration Testing and Red Team Standard. AI-driven tools have characteristic failure modes (hallucinated vulnerabilities, misidentified target systems, fabricated proof-of-concept artefacts) that require operator verification before findings are accepted into the remediation pipeline.

**OFFAI-SEC-09:** Use of AI-driven offensive tools must not bypass the human-approval gates in §24 of this standard for any action the tool plans. Where the tool's autonomous mode would execute an action that requires human approval per §24, the autonomous mode must be configured to halt and request approval.

**OFFAI-SEC-10:** AI-driven offensive tool licences are reviewed per the open-source licence policy. Tools under copyleft licences (AGPLv3, GPL-3.0) restrict downstream distribution and may not be embedded in proprietary tooling chains; tools under permissive licences (MIT, Apache 2.0) are preferred for embedding scenarios. The licence determination is recorded with the tool's approval.

---

## 34. Verification and enforcement

Compliance with this standard is verified through: CI/CD pipeline gate results (automated, per commit); pre-production security checklist gate (per deployment); quarterly security review of AI systems (manual); and annual red team evaluation per §23.

Any AI system found non-compliant with a Critical or High requirement must be remediated within the timeframes defined in the Production Security Requirements Standard. Continued operation requires explicit CIO risk acceptance documented in the Exception Register.

This standard is reviewed and updated at minimum annually, or when any of the following occurs: a new confirmed AI threat technique affects deployed AI surface; a significant new AI capability is introduced; OWASP LLM Top 10 or NIST AI RMF is materially updated; or an AI security incident occurs.

---

## 35. Agent production authority, reversibility, and recovery

This section applies only to agents with production action capability: tool, API, workflow-automation, code-execution, transaction, database-write, identity, security-tooling, or production-configuration access. It does not apply to passive AI assistance or to decision-support outputs that a human must act on; those are governed by the model-governance and human-oversight controls elsewhere in this standard. The distinction is the control boundary: where the agent can cause a production effect without a human performing the action, this section applies.

The governing principle is that authority sits in the system boundary, not in the agent. The permissions model, the approval path, the immutable audit trail, the reversal mechanism, and a named accountable human are the authority; the agent is the channel. Agent safety is therefore treated as a governance, identity, data-lineage, change-control, evidence, and operational-resilience problem, not primarily as a model-behaviour problem.

**AGENT-PROD-01:** An action-capable agent must not be granted production action authority, whether autonomous or semi-autonomous execution, until all four of the following are designed, tested, and governed, with evidence recorded per `AGENT-PROD-06`: (a) permission boundaries per §10 and the AI Access and Agent Permissions Standard; (b) immutable auditability per §28 and `AGENT-PROD-04`; (c) reversibility per `AGENT-PROD-02` with recovery testing per `AGENT-PROD-03`; (d) named human accountability per `AGENT-PROD-05`. Where any of the four is absent, the agent is restricted to Supervised Autonomous mode (`AUTON-SEC-01`) with per-action human confirmation. This precondition is verified at the acceptance-into-service gate (see the Software Evaluation, Acceptance and Lifecycle Management Standard) and is re-verified on the material-change thresholds in the AI Governance and Risk Framework.

**AGENT-PROD-02:** Every production-impacting action class an agent can perform must carry a documented reversibility classification: Reversible (an automatic reversal is defined), Compensable (a compensating transaction is defined that returns the system to an equivalent prior state), or Irreversible. Reversible and Compensable classes must have their reversal or compensating mechanism defined in the agent's governance documentation before production authority is granted. Action classes that remain Irreversible are permanently subject to per-action human confirmation (`AUTON-SEC-02`, §24) and cannot be reclassified as autonomous.

**AGENT-PROD-03:** The reversal or compensating mechanism for each Reversible or Compensable action class must be tested before production go-live and re-tested at every material change to the action class, the tool, or the target system. The test confirms that the mechanism returns the affected system to an equivalent prior state within its defined recovery objective. Recovery testing is part of the pre-production gate (§21); a missing or failing recovery test blocks production authority for that action class.

**AGENT-PROD-04:** The immutable audit trail (§28, `LOG-SEC-03`) must allow an auditor to reconstruct, for any agent-performed production action, the full lineage from the originating prompt or trigger, to the agent decision, to the tool invocation, to the system action, to a reference identifying the resulting data or configuration change (record identifier, change reference, or transaction identifier). The correlating identifier (`trace_id` per §20) must be carried through to the downstream system's change record. Lineage that stops at the tool invocation and does not reach the resulting change does not satisfy this control.

**AGENT-PROD-05:** Each action-capable agent has a single named accountable owner (a human role per the Role and Authority Register), recorded in the AI System Register. Accountability for actions the agent performs within its approved autonomous envelope remains with that owner and with the approver of the envelope; it does not transfer to the agent. The agent is never the accountable party. Where an action required human approval (§24), accountability also attaches to the approver recorded in the approval event.

**AGENT-PROD-06:** The decision to grant production action authority must produce an evidence record, held within the agent's AI System Register entry and system card, sufficient for audit, assurance, and risk acceptance. The record references the permission-boundary configuration; the reversibility classification (`AGENT-PROD-02`); the recovery-test results (`AGENT-PROD-03`); the lineage design (`AGENT-PROD-04`); the named accountable owner (`AGENT-PROD-05`); the pre-production gate (§21) and red-team (§23) results; and any risk acceptance recorded in the Exception Register. Continued authority requires the record to remain current through the review cadence.

This section governs autonomous and semi-autonomous production action. It does not raise the bar for passive AI assistance, decision support that a human acts on, or read-only agent capability; those remain governed by the controls already defined in this standard. The progression from passive assistance, to decision support, to semi-autonomous workflow execution, to autonomous production action is a progression in required controls, and production action authority is the point at which all four preconditions above become mandatory.

---

## Framework alignment

| Control Area | OWASP LLM Top 10 | MITRE ATLAS | CSA AICM v1 | NIST AI RMF |
| --- | --- | --- | --- | --- |
| Prompt injection | LLM01 | AML.T0051 | AI-TM-01 to 05 | GOVERN 1.1 |
| Supply chain | LLM03 | AML.T0010 to T0013 | AI-SC-01 to 08 | MANAGE 2.2 |
| Sensitive data disclosure | LLM02 | N/A | AI-PP-01 to 05 | MAP 1.6 |
| Tool misuse / overreach | LLM06 | AML.T0048 | AI-TM-08 | GOVERN 2.2 |
| Unsafe code generation | LLM05 | N/A | AI-SC-05 | MAP 1.1 |
| Excessive agency | LLM06 | N/A | AI-AU-01 to 06 | MANAGE 1.3 |
| Overreliance | LLM09 | N/A | AI-EC-01 | MANAGE 4.1 |
| Model resource exhaustion / DoS | LLM10 Unbounded Consumption | AML.T0037 | AI-SC-06 | N/A |
| Hallucination/output validation | LLM09 | N/A | AI-EC-03 | MAP 3.5 |



**End of Document**
