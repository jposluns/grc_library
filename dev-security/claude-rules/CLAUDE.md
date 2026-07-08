# Security Requirements for This Project

This file encodes security requirements that apply to all code written, reviewed, or suggested in this Claude Code session. These requirements are not advisory: they are mandatory constraints.

When you write code, check it against these requirements before presenting it. When you review code, flag any violation as a security finding with severity and remediation guidance.

---

## Secrets: absolute rules

**Never** place secrets, credentials, API keys, tokens, passwords, or connection strings in:
- Source code or test code
- Configuration files tracked in version control
- Dockerfiles or container definitions
- CI/CD pipeline definitions
- Log output or error messages
- Environment variable values passed as plain text in container specs

**Always** use:
- Platform secrets management (key vault, secrets manager) via managed identity
- CI/CD platform native secrets mechanisms
- `.env` files that are `.gitignored` for local development only

If you see a hardcoded secret in existing code, treat it as compromised and flag it immediately as a Critical finding.

---

## Authentication: never implement these

- Custom authentication mechanisms or local user stores: always use the enterprise IdP
- MFA bypass paths or fallback authentication without MFA
- SAMAccountName-only authentication: use UPN/SSO
- Plain LDAP binds on port 389: use LDAPS (port 636) only
- Authentication tokens stored in browser `localStorage`: use httpOnly cookies or in-memory
- Service accounts with hard-coded passwords: use managed identity or PAM vault injection
- Shared secrets for service-to-service calls: use OAuth 2.0 client credentials or managed identity

---

## Input validation: non-negotiable

- **Validate all external input server-side**: type, format, length, range. Reject invalid input; do not sanitize and continue.
- **Never build SQL, LDAP, XML, or shell commands by string concatenation**: use parameterized queries, ORMs, or prepared statements
- **Validate file uploads by content** (magic bytes/MIME detection), not by extension. Store outside web root. Scan before processing. Never execute.
- **Context-aware output encoding** for every output context: HTML entity encoding, JSON encoding, URL encoding, SQL quoting

---

## Cryptography: use these, not others

| Purpose | Correct Choice | Prohibited |
| --- | --- | --- |
| Symmetric encryption | AES-256-GCM | DES, 3DES, RC4, Blowfish |
| Asymmetric | RSA-4096, EC P-256/P-384 | RSA < 2048 |
| Key exchange | ECDHE, DHE | Static RSA |
| Integrity hashing | SHA-256, SHA-384, SHA-512 | MD5, SHA-1 |
| Password hashing | Argon2id (preferred), bcrypt (cost ≥12) | MD5, SHA-anything (for passwords), plain storage |
| TLS | TLS 1.3 (or stronger), aligned to [`security/policy-encryption-and-key-management.md`](../../security/policy-encryption-and-key-management.md) §4 (Encryption standards) canonical mandate | SSL, TLS 1.0, TLS 1.1, TLS 1.2 |
| Certificates | SHA-256 RSA or ECDSA | SHA-1 |

Never hardcode keys. Keys go in the secrets management service.

---

## Authorization

- Enforce all authorization server-side on every request: never rely on client-side claims
- Default deny: deny unless explicitly granted
- RBAC decisions on every call: no implicit allow from previous calls
- API responses must not include data the caller is not authorized to receive
- Never trust request parameters (IDs, roles, tenant identifiers) without server-side validation against the authenticated identity

---

## Logging and error handling

**Never log**: passwords, tokens, session keys, payment data, full PII records, encryption keys

**Always log**: authentication events (success and failure), authorization decisions, all access to Confidential/Restricted data, significant configuration changes, all API calls (caller, endpoint, response code, timestamp)

**Error responses to callers**: generic message + correlation ID only. Full error details (stack traces, system names, paths, schema details) go to server-side logs only.

---

## CORS

Wildcard CORS origins (`Access-Control-Allow-Origin: *`) are prohibited in production APIs, web apps, and HTTP-triggered services. Use an explicit allow-list of permitted origins stored in configuration.

---

## AI and LLM-specific requirements

When writing code that calls LLMs, builds AI applications, or processes AI-generated content:

- **Treat all LLM output as untrusted user input**: validate and sanitize before use in any downstream operation
- **Never pass LLM output directly to**: shell commands, SQL queries, file system operations, or other tool calls without validation
- **Implement prompt injection defenses**: do not concatenate user input directly into system prompts; use separate message roles; validate instructions in retrieved content before acting on them
- **Rate-limit all AI endpoints**: LLM calls are expensive and can be abused for data exfiltration
- **Log all AI inputs and outputs** to SIEM for anomaly detection
- **Require human confirmation** before writing to operational data based on AI decisions
- **Do not send Confidential or Restricted data to external AI APIs** without a data processing agreement and explicit approval

For agentic systems, see additional rules in [`ai/agent-security.md`](ai/agent-security.md). 
For MCP servers, see [`ai/mcp-security.md`](ai/mcp-security.md). 
For RAG systems, see [`ai/rag-security.md`](ai/rag-security.md).

---

## Dependencies and third-party code

- Verify that AI-suggested dependency names **actually exist** in the package registry before using them: hallucinated package names are a real supply-chain attack vector
- Prefer dependencies with: active maintenance (last release within 24 months); compatible licence (Apache 2.0, MIT, BSD generally safe; GPL/AGPL require Legal approval for commercial use); no known Critical/High CVEs
- Never install a package from an unverified source or non-standard registry
- Review transitive dependencies in SCA output

---

## Data handling

- Apply minimum data collection: only collect what is needed for the stated purpose
- Do not copy production data to development or test environments: use data masking or synthetic data
- Implement data retention logic in application code: delete or anonymize at end of retention period
- Log files must not contain unmasked personal data (PII, payment data, credentials)

---

## Development-governance discipline

When working on a governed codebase (one with CI gates, audit programmes, branch protections, generated artefacts, or a change-tracking convention), apply the rules in `governance/`. The currently-shipped governance rules are:

- [`governance/gate-discipline.md`](governance/gate-discipline.md): never weaken or delete a gate to silence a failure; fix the artefact. Targeted suppressions need a documented rationale on the same line; blanket suppressions are prohibited. Exception path is the project's exception register, not a unilateral suppression.
- [`governance/change-tracking.md`](governance/change-tracking.md): every PR carries a CHANGELOG entry, even if terse. Substantive entries record date, version, structured sections (Added/Changed/Removed/Fixed/Security), linked file references, the "why" (not only the "what"), and verification evidence. Terse entries (date + version header + one sentence) cover ancillary changes (internal tooling, working-state housekeeping, pure refactors, typo fixes); there is no skip path. The DONE ledger that pairs with CHANGELOG carries 1-2-sentence headlines, no links: "scrolling battle-text" framing as an at-a-glance index, not a CHANGELOG duplicate. A closed backlog item's DONE entry names the item number and summarizes what the item was and how it was accomplished in one-to-two sentences, and that summary is surfaced in chat at the moment of completion as well.
- [`governance/evidence-grounded-completion.md`](governance/evidence-grounded-completion.md): never declare work "done", "fixed", "ready", "shipped", or any synonym, and never assert a factual property of an artefact you have not read (that a file contains, lacks, or requires something), without first running the verification protocol (enumerate files in scope, re-read each in full, quote supporting lines, search for falsifying evidence, distinguish mechanical-gate verification from semantic verification, state unverified items explicitly). The vocabulary of completion, and any state assertion made in research, assessment, planning, or review, are flags that the protocol must precede; the protocol is mechanical so it can be checked without subjective judgement. Accepting an item as unverified (proceeding on it, annotating it unverified-for-now, or relying on a value not confirmed current) rather than resolving it requires recording a durable tracking item in the backlog so it is revisited and verified. Three sharper corollaries apply where the observation is not a single readable file: un-observable state (context depth, a felt sense of doneness) is never assertable and never a wind-down, stop, or defer trigger, which must instead be a named externally-observable signal; inventory, absence, and held-version claims require the collection's own index, not a partial directory look; and external-version currency is answered only by the upstream source verified in the current turn, never a stored note, a cached copy, or a local catalogue (find what is held via the index, verify upstream, act only after both, and never rely on a superseded version without explicit authorization).
- [`governance/clarify-before-acting.md`](governance/clarify-before-acting.md): when a request has more than one reasonable interpretation, or an external value the request does not pin down is required to proceed, surface the ambiguity in one sentence and ask before acting. Use sensible defaults only for choices where a wrong guess is bounded to a quick edit; ask before defaulting for choices with consequences beyond this PR (target branch, public API shape, dependency, breaking change).
- [`governance/artefact-and-branch-discipline.md`](governance/artefact-and-branch-discipline.md): generated artefacts are read-only (edit the source, run the generator, commit both halves together; CI verifies via `--check` mode); protected branches are append-only (no direct push; no force-push; PR-only merges). The version-monotonicity contract depends on branch protection as its primary defence and the audit as its backstop.
- [`governance/action-before-explanation-of-inaction.md`](governance/action-before-explanation-of-inaction.md): never explain why an external action cannot or will not proceed without first attempting it (when safe and reversible) or naming it and asking (when destructive). The trigger surface is the moment a draft contains "X is blocked / waiting on / requires / would fail" attached to an action not attempted this turn; the protocol is the reversibility gate (classify as safe-or-destructive), then the corresponding action (attempt the safe action and report the real result, or name the destructive action and ask). Execution doubt is resolved by trying; decision doubt remains in the clarify-before-acting rule's scope.
- [`governance/validate-inference-before-action.md`](governance/validate-inference-before-action.md): when the next action depends on an inferred premise (a state claim not directly observed in the current turn), validate the premise via a tool call before taking the action. Action-side counterpart of the evidence-grounded-completion rule (which is the assertion-side). The trigger surface is the moment a draft contains "since / because / given X, [action]" where X is a state claim that has not been observed in the current turn; the protocol is name-the-inference, cost-the-validation, validate, act-on-the-validated-observation. Cascade failures (one wrong inference driving a chain of wrong actions) are the failure mode the rule prevents.
- [`governance/ai-assistant-workflow-disciplines.md`](governance/ai-assistant-workflow-disciplines.md): five disciplines for an AI coding assistant driving multi-PR work over a long session. (1) Research-assistant discipline: workers produce research files, the orchestrator authors all final prose, claims verified at apply-time. (2) Pipeline PR construction: parallel research, serial apply, CI gating between PRs. (3) Apply-time worker correction: catch worker errors at apply-time, document them in the entry. (4) "Always split when in doubt": default to separate PRs unless changes are tightly coherent. (5) Background work during CI waits: read-only prep on the next PR; no edits during the wait. Each discipline emerged from a recurring failure mode during multi-PR remediation work. The rule also carries the layered skeptical pre-push verification standard (not a sixth discipline): tiered by change weight (no standing verifier for quick-fix/bookkeeping; one refute-briefed verifier pre-push for substantive changes; the full high-assurance harness for sensitive ones), with the validate-fix-re-verify loop (three-iteration cap, then defer) and the never-silent override register.
- [`governance/trust-recovery-escalation.md`](governance/trust-recovery-escalation.md): the escalation tier invoked when an AI assistant's discipline failures put a maintainer's confidence in a window of work in question. Names the trigger (abbreviated or skipped QA across changes, a skipped verification reaching the shared pipeline, a wrong-cadence automation, an unvalidated inference that cascaded), the two-skill suite (the AI-failure-pattern forensic pass `deep-qa-review` / `/full-qa` first, then the fresh-reader persona pass `library-fitness-review` / `/fitness`), the routing convention (every confirmed finding routed, tiered by severity: High[critical] and High to the top-priority tier, Medium and Low to the next tier, none dropped; apply-time-verified, deduped against the existing backlog), and the sign-off discipline (the tier terminates only on explicit maintainer sign-off, not on an empty finding-set). Includes the full-clone methodology rule: verify a non-shallow clone before any history-aware audit.
- [`governance/project-integrity.md`](governance/project-integrity.md): the apex rule of the pack. Fixes the priority ordering on the optimization-dimension axis: **the AIQT Principle, (Accuracy = Integrity = Quality = Trust) > Speed > Cost**, the four facets forming one non-negotiable co-equal tier. Where each other rule constrains a specific behaviour, this rule decides which tier wins when the AIQT tier, speed, and cost conflict (the AIQT tier always, then speed, then cost; "done faster" and "done cheaper" are never reasons for "done worse"). It re-states the integrity non-negotiables (no stub/mock/fabrication; no gate suppression; no silent changes; failing states surfaced) as the apex-precedence forms of `gate-discipline`, `evidence-grounded-completion`, and `clarify-before-acting`, and prescribes a self-reminder checkpoint at task start, before persistence, before completion claims, and at tension points.
- [`governance/surface-counterproductive-instructions.md`](governance/surface-counterproductive-instructions.md): a clear instruction is not automatically a correct one. When following an instruction as given would reduce efficiency, effectiveness, or productivity, lower quality, destroy work already done, contradict a stated goal, or rest on a stale-state belief, stop, consider, and surface the concern with named options before executing, so the requestor can confirm or redirect. The response is stop-consider-confirm (name the concrete cost, offer the better path, ask once, then act on the answer); the charitable-interpretation corollary forbids silently taking a harmful literal reading or reverting committed work without confirming; the calibration keeps it from becoming an over-ask (fire only on material downside, accept an informed override). Requestor-facing counterpart to `clarify-before-acting` (ambiguity) and broader than `project-integrity` (any net-negative effect, not only the Quality versus Speed versus Cost tradeoff).
- [`governance/high-assurance-verification.md`](governance/high-assurance-verification.md): the heavier pre-apply verification harness for *sensitive* changes, those that are gate-blind on correctness (a fit or semantic property no existence gate can check), delicate at scale (a wide reshape or bulk mapping where a hand-edit is itself a defect risk), and costly to get wrong (a cited or downstream-relied-on artefact). The five-stage harness: research fan-out; a mechanical signal pass over the negatives (the "open-on-negative-with-signal" discipline); two independent adversarial verifiers, blind to each other and to the research, one hunting false negatives (misses) and one hunting false positives (over-assignments); a programmatic invariant floor where mechanical truth exists; and a deterministic scripted apply plus a re-parse, so apply-correctness is independent of the orchestrator's in-context precision. The proactive counterpart to `trust-recovery-escalation` (which is reactive, post-failure); a heavier tier above the routine `ai-assistant-workflow-disciplines` research-assistant flow. Sensitive items persist across sessions in a working-state register surfaced at resume, so the harness recurs to completion rather than being a one-session effort.

The phased governance rollout announced at pack version 1.6.0 completed at 1.11.0 with the first five rules above. Pack version 1.21.0 added the sixth rule (`action-before-explanation-of-inaction.md`) as a post-rollout extension. Pack version 1.27.0 added the seventh rule (`validate-inference-before-action.md`) after a recurring failure mode where an orchestrator inferred premises (subagent-skip justification, fix-completeness, corpus-state) without validating; each inference cascaded into downstream rework. Pack version 1.36.0 added the eighth rule (`ai-assistant-workflow-disciplines.md`) after observing five distinct memory-only processes the orchestrator was following during multi-PR remediation work; documenting them gave the disciplines durability across sessions. Pack version 1.47.0 added the ninth rule (`trust-recovery-escalation.md`) after a session whose discipline failures (abbreviated QA across eleven changes, a skipped post-commit audit, a wrong-cadence timer) required a structured white-box re-examination of the window; the rule names the escalation suite and the maintainer-sign-off termination that rebuild trust. Pack version 1.49.0 added the tenth rule (`project-integrity.md`), the project-agnostic distribution of the Quality > Speed > Cost apex integrity rule, so adopters inherit the lexicographic priority ordering rather than re-deriving it under pressure. Pack version 1.51.0 added the eleventh rule (`surface-counterproductive-instructions.md`) after a maintainer's brief instruction was read literally and silently, reverting committed work the instruction did not intend to destroy; the rule names the general case (a clear instruction can still be the wrong thing to do) so the assistant surfaces the concrete cost and confirms before acting, rather than complying fast or refusing. Pack version 1.52.0 added the twelfth rule (`high-assurance-verification.md`) after a maintainer-directed sensitive change (adding an AI-control column to a compliance matrix, a wide reshape whose per-cell control-code fit no existence gate can check) was made integrity-absolute through a layered harness that caught real defects a single pass missed; the rule generalizes that harness (independent adversarial verification plus a deterministic apply, persisted across sessions) as the proactive counterpart to `trust-recovery-escalation`.

---

## Framework basis

These requirements implement controls from:
- OWASP Top 10:2025 (eighth edition; supersedes 2021)
- OWASP LLM Top 10
- OWASP MCP Top 10
- OWASP ASVS v5.0.0
- NIST SSDF (SP 800-218 and SP 800-218A: Generative AI Profile)
- CSA CCM v4.1 / AICM v1.1
- ISO/IEC 27001:2022 Annex A
- CISA Secure by Design principles
- SLSA (Supply-chain Levels for Software Artifacts)

For detailed requirements, see [`dev-security/standard-developer-security-requirements.md`](../standard-developer-security-requirements.md) in the GRC library.