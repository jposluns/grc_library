# AI and LLM Application Security Rules

Apply these rules to all code that calls LLMs, uses AI APIs, processes AI-generated content, or builds AI-powered features. These rules implement OWASP LLM Top 10 and MITRE ATLAS controls.

---

## Core Principle: AI Output Is Untrusted Input

Treat every LLM response, every model output, and every AI-generated value as if it came from an untrusted external user. Validate it. Encode it. Never execute it directly.

---

## Prompt Injection Defense (OWASP LLM01)

**Direct prompt injection**: user input reaching the system prompt:
- Never concatenate raw user input into system prompts
- Use structured message formats with clear role separation (system / user / assistant)
- Validate that user-supplied text does not contain instruction-like patterns before including in prompts: consider a content filter or structural boundary

**Indirect prompt injection**: instructions embedded in retrieved documents, web pages, tool outputs, or database records:
- Treat all retrieved content as potentially adversarial
- Do not act on instructions found in retrieved content without explicit user authorization
- Sanitize document content before including in prompts: strip markdown that could carry instruction structure
- Log all indirect content sources for anomaly detection
- Apply the same defense to MCP tool outputs, function call results, and memory store results

**References:** OWASP LLM01, MITRE ATLAS AML.T0051: Prompt Injection

---

## Sensitive Information Disclosure (OWASP LLM02)

- Never include secrets, credentials, API keys, or PII in prompts sent to external AI APIs
- Implement PII detection and redaction before sending user-generated content to AI services
- Do not log full prompt content in production: log metadata (token count, model, latency) but not the prompt text unless required for specific audit purposes
- Scrub AI responses for potential training data leakage before returning to users
- Set up output content scanning to detect when the model reveals system prompt content, training data, or organizational configuration

**References:** OWASP LLM02, MITRE ATLAS AML.T0024: Training Data Exfiltration

---

## Supply Chain and Model Source Security (OWASP LLM03)

- Source models and model APIs only from approved, verified providers
- Verify model checksums/signatures when downloading open-weight models
- Document all model dependencies (model name, version, provider, licence, data provenance where known)
- Never use a model that has been fine-tuned on unverified data for production applications handling Confidential data
- Assess and document model licences: some open-weight models have usage restrictions

**References:** OWASP LLM03, OWASP LLM06 (Excessive Agency)

---

## Excessive Agency and Authorization (OWASP LLM06)

- **Minimize tools and permissions granted to AI agents**: give the model access only to tools it needs for the current task
- Every tool that writes, deletes, or modifies data must require **human confirmation** before execution
- Do not allow AI systems to grant additional permissions to themselves or to other agents
- Validate all tool arguments before execution: LLM-generated tool arguments are untrusted
- Implement hard limits on tool-call chains and recursion depth
- Log every tool call with full arguments and results

**References:** OWASP LLM06, MITRE ATLAS AML.T0048: Exploit Public-Facing Application (via AI Agent)

---

## Overreliance and Output Validation (OWASP LLM09)

- Validate AI output before using it in downstream operations, especially:
 - Code generation → run SAST and security review
 - SQL generation → validate against schema; use parameterized execution
 - Decisions affecting users → require human review for high-impact decisions
 - Content for external display → validate and sanitize for XSS and injection
- Implement confidence thresholds: reject low-confidence outputs or route them to human review
- Test for model hallucinations in security-sensitive contexts (e.g., package names, API endpoints, permissions)

**References:** OWASP LLM09

---

## Input and Output Rate Limiting

- Rate-limit all AI API endpoints: per user, per IP, and globally
- Implement token-count tracking to prevent cost-exploitable prompt amplification
- Alert on unusually large prompt inputs or outputs
- Reject inputs exceeding a defined maximum token budget

---

## AI Logging Requirements

Every AI-powered endpoint must log:
- Request ID and session ID (not the full prompt in production)
- Model name and version
- Token count (input and output)
- Response time
- Tool calls made (name and arguments)
- Human confirmation decisions (approved or rejected)
- Error and exception events

Route all AI logs to the SIEM for anomaly detection.

---

## Adversarial Testing Requirements

Before any AI feature reaches production, adversarial testing must include:
- Direct prompt injection attempts using standard jailbreak and injection payloads
- Indirect prompt injection via crafted document content
- Data exfiltration probing through model outputs
- Tool-call manipulation (malformed arguments, privilege escalation attempts)
- Model inversion probing (attempts to recover training or system prompt data)

**Recommended testing resources:**
- OWASP LLM Top 10 test cases
- MITRE ATLAS adversarial technique catalogue
- **TikiTribe**: open-source adversarial prompt library and agentic workflow attack surface enumeration; provides structured test suites for tool-call injection, MCP server exploitation, and multi-agent trust boundary attacks

---

## Framework Alignment

| Requirement | OWASP LLM Top 10 | MITRE ATLAS | CSA AICM | NIST AI RMF |
| --- | --- | --- | --- | --- |
| Prompt injection | LLM01 | AML.T0051 | TVM-12 | Measure 2.5 |
| Sensitive disclosure | LLM02 | AML.T0024 | DSP-05 | Measure 2.7 |
| Supply chain | LLM03 | AML.T0010 | STA-05 | Govern 1.7 |
| Excessive agency | LLM06 | AML.T0048 | IAM-04 | Manage 1.3 |
| Output validation | LLM09 | N/A | AIS-02 | Measure 2.9 |