# AI Red Team Report Template

**Document Title:** AI Red Team Report Template\
**Document Type:** Template\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** AI Security Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/guide-ai-adversarial-test-reference.md`](guide-ai-adversarial-test-reference.md), [`ai/guideline-adversarial-evaluation-suite-development.md`](guideline-adversarial-evaluation-suite-development.md), [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`ai/plan-ai-incident-response.md`](plan-ai-incident-response.md), [`security/standard-penetration-testing-and-red-team.md`](../security/standard-penetration-testing-and-red-team.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material change to red team methodology or to threat catalogues\
**Repository Path:** [`ai/template-ai-red-team-report.md`](template-ai-red-team-report.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template defines the format of a structured AI red team engagement report. It is used for both internally-run engagements and externally-commissioned engagements against the organisation's AI systems. The output is the durable record of the engagement, the findings, the recommendations, and the corrective actions tracked to closure.

A populated AI red team report identifies real systems and the specific weaknesses found and is highly sensitive operational material. This CC BY-SA 4.0 template contains no example values.

---

## Scope

This template applies to all adversarial-testing engagements against the organisation's AI systems including:

1. Pre-release red team for new AI features.
2. Annual red team for production Tier 1 AI systems.
3. Ad-hoc red team after material model, prompt, retrieval, or agent-capability changes.
4. Supplier-commissioned third-party red team against the organisation's customer-facing AI.
5. Bug-bounty submissions consolidated into a red team report where the volume justifies.

---

## Section 1: engagement profile

| Field | Required content |
| --- | --- |
| Engagement ID | Unique identifier |
| Engagement type | Pre-release, periodic, ad-hoc, supplier-commissioned, bug-bounty consolidation |
| System under test | AI system identifier from the AI System Register |
| Models under test | Model identifiers from the Model Registry |
| Scope | In-scope capabilities, surfaces, integrations |
| Out of scope | Explicit exclusions |
| Engagement window | Start and end dates |
| Engagement team | Internal red team or external provider; team size; lead identity (role in public version) |
| Authorisation | Approving role; documented authorisation per the penetration testing standard |
| Rules of engagement | Documented rules: production vs staging; what evidence may be exfiltrated to demonstrate impact; safety guardrails; communications channel |
| Coordination | The Incident Coordinator who manages any unintended impact |

---

## Section 2: methodology

| Field | Required content |
| --- | --- |
| Threat model | The threat model the engagement tested |
| Attack frameworks consulted | OWASP LLM Top 10 (2025) categories, MITRE ATLAS tactics and techniques, in-house threat library |
| Tooling | Automated tools (e.g. red team automation frameworks, LLM scanners), manual techniques, social-engineering simulations where applicable |
| Test cases executed | Reference to the test case library; coverage statement against the categories |
| Attacker personas | The personas tested (e.g. unauthenticated external user, authenticated low-privilege user, malicious insider, compromised upstream supplier, malicious end customer) |
| Realism boundaries | What the engagement did not simulate (e.g. multi-month patience, supply-chain compromise) |

---

## Section 3: findings

Each finding is recorded as a standalone subsection with the following structure:

| Field | Required content |
| --- | --- |
| Finding ID | Unique within the engagement |
| Title | Short descriptive title |
| Category | OWASP LLM Top 10 category; MITRE ATLAS technique where applicable |
| Severity | Critical, High, Medium, Low (per the severity criteria below) |
| Affected components | Specific models, prompt templates, retrieval indexes, tools, agent configurations |
| Attack narrative | Step-by-step description of how the attack was executed |
| Evidence | Specific prompts used, screenshots or output excerpts, traces |
| Reproduction steps | Concrete instructions to reproduce the finding |
| Impact | What an attacker could achieve in production; safety, security, privacy, compliance, reputation impact |
| Likelihood | Estimated likelihood under the threat model |
| Recommended remediation | Specific actions; the recommended owner role |
| Compensating controls | Where remediation will take time, the interim mitigation |
| Detection improvements | How the organisation could detect this in production |
| Linked corrective action | Cross-reference to the corrective action register |

### Severity criteria

| Severity | Definition |
| --- | --- |
| Critical | Arbitrary action execution by the AI; complete system-prompt extraction; cross-tenant data access; autonomous action without approval; ability to manipulate safety-critical AI output at will |
| High | Partial instruction override that enables sensitive disclosure; tool-scope escape; PII exfiltration; consistent jailbreak success against a deployed safety classifier |
| Medium | System configuration disclosure; partial context leakage; safety-classifier bypass in narrow conditions; supplier-side telemetry exposure |
| Low | Verbose error messages revealing model identity or backend detail; minor behaviour deviations; documented limitations being exercised by adversarial inputs |

Critical and High findings block production deployment of the affected component until remediated and verified.

---

## Section 4: coverage assessment

| Threat category | Tested | Findings | Note |
| --- | --- | --- | --- |
| LLM01 prompt injection (direct and indirect) | Yes / No / Partial | Count by severity | |
| LLM02 sensitive information disclosure | Yes / No / Partial | Count by severity | |
| LLM03 supply chain | Yes / No / Partial | Count by severity | |
| LLM04 data and model poisoning | Yes / No / Partial | Count by severity | |
| LLM05 improper output handling | Yes / No / Partial | Count by severity | |
| LLM06 excessive agency | Yes / No / Partial | Count by severity | |
| LLM07 system prompt leakage | Yes / No / Partial | Count by severity | |
| LLM08 vector and embedding weaknesses | Yes / No / Partial | Count by severity | |
| LLM09 misinformation and hallucination | Yes / No / Partial | Count by severity | |
| LLM10 unbounded consumption | Yes / No / Partial | Count by severity | |
| MITRE ATLAS reconnaissance, initial access, ML attack staging, exfiltration, impact | Yes / No / Partial | Count by severity | |
| Application-specific tests (per the system under test) | Yes / No / Partial | Count by severity | |

---

## Section 5: positive observations

This section is mandatory. Record:

1. Controls that worked: where the safety classifier, agent permission framework, prompt template, or other control mitigated an attack.
2. Practices that worked: incident-handling under simulated discovery; communication clarity; rollback effectiveness.
3. Patterns worth replicating across other systems.

Absence of positive observations is itself a finding.

---

## Section 6: recommendations

Grouped by recommendation category:

| Category | Examples |
| --- | --- |
| Prompt and template | Specific prompt template changes; delimitation; structured output enforcement |
| Safety classifiers | New classifier categories; threshold adjustments; ensemble approaches |
| Tool and agent | Allow-list refinement; confirmation rules; rate and chain-length tightening; identity propagation |
| Retrieval and context | Source allow-list; indirect-injection mitigations; access propagation |
| Monitoring and detection | New SIEM rules; metric coverage |
| Process | Procedure updates; eval-suite additions; training-data hygiene |
| Architecture | Structural changes to the system or its integrations |
| Supplier | Items to raise with model or platform suppliers |

Each recommendation is mapped to a corrective action with owner, deadline, and acceptance criteria.

---

## Section 7: validation and retest

For each remediated finding:

| Field | Required content |
| --- | --- |
| Remediation deployed | Date |
| Retest performed | Date |
| Retest outcome | Pass, Fail, Partial |
| Residual risk | Any residual exposure documented |
| Risk acceptance | If residual risk is accepted, the role and the conditions |

Retests are conducted by the same red team (where independence allows) or by an independent reviewer.

---

## Section 8: distribution

The completed red team report is classified Restricted by default. Distribution is restricted to:

| Recipient role | Rationale |
| --- | --- |
| AI Security Maintainer | Owns the corrective action programme |
| CISO | Executive accountability |
| CIO | Where production AI systems are affected |
| AI Governance Council | Where governance updates are recommended |
| System owners affected | Per-finding distribution to the responsible role |
| Internal Audit | On request |
| External regulator | Where regulatory obligation requires |
| External customer | Sanitised summary only where the contract requires |

A summary of findings (without exploit detail) feeds the AI risk register and the resilience metrics register.

---

## Section 9: signatures

| Approver role | Date |
| --- | --- |
| Red team lead | |
| AI Security Maintainer | |
| CISO (for Critical and High findings) | |
| External provider point of contact (if applicable) | |

---

## Operating expectations

1. Every red team engagement produces a report from this template.
2. The report is delivered within 10 business days of engagement close for engagements under two weeks; longer engagements deliver within 20 business days.
3. Findings rated Critical or High in active production systems are reported to the AI Security Maintainer and CISO within 2 business days of identification, not awaiting the full report.
4. Corrective actions are tracked in the corrective action register; ageing actions escalate per the CAPA procedure.
5. Reports are archived for at least seven years; longer where litigation hold or regulatory request applies.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| OWASP LLM Top 10 (2025) | Categories and prevention guidance | Threat taxonomy |
| MITRE ATLAS | Tactics, techniques, case studies | Adversarial ML threat catalogue |
| NIST AI RMF | MEASURE | Test, evaluation, validation, verification |
| ISO/IEC 42001:2023 | §9 performance evaluation | AI assurance |
| EU AI Act | Article 15 (accuracy, robustness, cybersecurity); Article 17 (quality management) | High-risk AI obligations |
| ISO/IEC 27001:2022 | A.8.29 | Security testing |
| PTES | Penetration Testing Execution Standard | Underlying engagement methodology |
| OWASP GenAI Red Teaming Guide | Industry guidance | Methodology reference |

---

## Limitations

This template is a CC BY-SA 4.0 baseline. AI red team methodology is evolving rapidly; new attack categories and new evaluation techniques emerge frequently. Adopting organisations populate the template with engagement-specific findings, integrate the corrective action tracking with their existing CAPA workflow, and adapt the severity criteria to their risk appetite. The template is not a substitute for the red team engagement itself or for the underlying security and AI testing standards.

---

**End of Document**
