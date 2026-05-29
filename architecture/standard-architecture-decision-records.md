# Architecture Decision Records Standard

**Document Title:** Architecture Decision Records Standard\
**Document Type:** Standard\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** Chief Technology Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`architecture/framework-enterprise-architecture.md`](framework-enterprise-architecture.md), [`architecture/procedure-architecture-review.md`](procedure-architecture-review.md), [`dev-security/procedure-secure-code-review.md`](../dev-security/procedure-secure-code-review.md), [`governance/framework-document-architecture-and-interrelationship.md`](../governance/framework-document-architecture-and-interrelationship.md)\
**Classification:** Public\
**Category:** Architecture\
**Review Frequency:** Annual and upon material change to architecture documentation practice\
**Repository Path:** [`architecture/standard-architecture-decision-records.md`](standard-architecture-decision-records.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## Purpose

This standard defines how significant architecture decisions are recorded. Architecture decision records (ADRs) capture the context, the decision, the alternatives considered, the trade-offs accepted, and the consequences expected. They are the durable, searchable record of architecture practice.

---

## Scope

This standard applies to:

1. Decisions affecting the architecture of any production service or platform.
2. Decisions affecting cross-product or cross-team architecture concerns.
3. Decisions accepting material technical debt.
4. Technology selection decisions (build vs buy; vendor selection).
5. Significant integration, data, and AI architecture decisions.

It does not apply to routine implementation choices within an existing reference architecture.

---

## Section 1: principles

| Principle | Description |
| --- | --- |
| Immutable | An ADR is not edited after acceptance; superseding decisions create new ADRs |
| Searchable | ADRs are stored where they can be found by engineers, architects, and reviewers |
| Linked | ADRs link to the artefacts, runbooks, code, and other ADRs they affect |
| Proportionate | ADR length matches decision significance; brief is better than padded |
| Honest | Trade-offs are recorded honestly; uncomfortable trade-offs are not hidden |
| Forward-looking | The ADR explains the future consequences as well as the present rationale |
| Co-located | ADRs sit with the code or system they govern where possible |

---

## Section 2: when to write an ADR

An ADR is written when a decision:

| Trigger | Examples |
| --- | --- |
| Affects multiple teams | A shared platform, a cross-product contract |
| Constrains future architecture | A choice of database engine, a choice of cloud provider |
| Is hard to reverse | A primary identifier scheme, an event schema, a contract with a customer |
| Carries material risk | Security, privacy, AI, supplier-concentration implications |
| Affects regulated capability | Authentication, financial calculation, regulated data handling |
| Introduces or retires a major technology | A new programming language, framework, or platform |
| Accepts material technical debt | Including the expected cost of repayment |
| Is contested | The rationale needs to survive personnel turnover |

When in doubt, write an ADR; the cost of writing one is low compared to the cost of an unrecorded contested decision.

---

## Section 3: ADR template

The minimum structure is:

| Section | Description |
| --- | --- |
| Title | Imperative voice; one sentence (e.g. "Use a single primary identifier for customers") |
| Status | Proposed, Accepted, Superseded, Deprecated, Rejected |
| Date | When the decision was made or last updated for status |
| Decision owner | The named architect or engineer accountable |
| Context | The situation, forces, and constraints driving the decision |
| Decision | The decision in clear, declarative language |
| Alternatives considered | The options that were considered and the reason each was not selected |
| Consequences | Positive, negative, and neutral consequences |
| Compliance considerations | Regulatory, security, privacy, AI implications |
| Linked records | Other ADRs, reference architectures, decision records the ADR depends on or supersedes |
| Review and supersession | Conditions under which the decision should be revisited |

Optional additional sections:

| Section | When used |
| --- | --- |
| Stakeholders consulted | When the decision was discussed broadly |
| Cost analysis | When the decision has material cost implications |
| Risk register linkage | When the decision creates or addresses an entry in the enterprise risk register |
| Sustainability considerations | When the decision has material sustainability implications |
| Migration plan | When the decision implies migration from an existing state |

---

## Section 4: status lifecycle

| Status | Meaning |
| --- | --- |
| Proposed | Drafted; under review; not yet binding |
| Accepted | Approved; binding; reflected in code and operations |
| Superseded | Replaced by a newer ADR; reference to the successor recorded |
| Deprecated | No longer in force; not yet replaced |
| Rejected | Considered but not adopted; the rationale is preserved |

Status changes are appended to the status section with a date; the body of the ADR is otherwise immutable.

---

## Section 5: review and approval

| Decision type | Review required |
| --- | --- |
| Local team decision | Team lead and one peer reviewer |
| Cross-team decision | Domain architect plus the affected teams |
| Significant architecture decision | Architecture review board per the architecture review procedure |
| Decision involving security, privacy, or AI | Relevant domain reviewer added to the above |
| Decision involving supplier selection | Procurement and supplier risk reviewers added |
| Decision affecting regulated capability | Compliance reviewer added |

Approval is recorded in the ADR; the approver's role (not name only) is included.

---

## Section 6: storage and discoverability

| Element | Requirement |
| --- | --- |
| Storage location | Co-located with the system the ADR governs; cross-cutting ADRs in an architecture repository |
| File format | Markdown preferred; consistent across the organisation |
| Naming | Sequential identifier and short title (e.g. ADR-0042-single-customer-identifier.md) |
| Index | A searchable index across systems lists ADRs by title, status, and tag |
| Tags | Domain tags (security, data, AI, integration, etc.) support discovery |
| Linking | ADRs link to and from architecture documents, reference architectures, runbooks, and risk register entries |

---

## Section 7: integration with adjacent processes

| Process | Integration |
| --- | --- |
| Architecture review | The architecture review procedure references the ADR as the durable record of the decision |
| Secure code review | Code that implements an ADR is reviewed in context |
| Risk management | ADRs that create or address material risk are linked to the risk register |
| Acceptance into service | Acceptance reviews check that significant architecture decisions are recorded |
| Change management | Significant changes reference the ADRs they implement |
| Onboarding | New engineers learn the system's architecture by reading its ADRs |

---

## Section 8: AI-aware ADR practice

| Concern | Practice |
| --- | --- |
| AI model selection | Decision to use a specific model or model family is an ADR |
| Foundation-model dependency | Decision to depend on a foundation-model provider is an ADR; linked to the foundation-model lifecycle procedure |
| Agentic capability | Decision to enable agentic tool invocation is an ADR; references the AI access and agent permissions standard |
| Data-sharing with AI provider | Decision is an ADR; references training-data governance |
| AI-generated content | Decision affecting customer-facing AI-generated content is an ADR; references AI evaluation expectations |
| AI replaces human judgement | Where AI replaces a human-judgement step, the ADR records the rationale and the safeguards |

---

## Section 9: quality expectations

| Quality | Indicator |
| --- | --- |
| Useful to a future reader | A reader without prior context can understand why the decision was made |
| Honest about trade-offs | Negative consequences are not omitted |
| Short | The ADR is as short as possible while remaining clear |
| Decisive | The decision is stated in declarative language |
| Forward-looking | The ADR helps future readers know when to revisit it |

---

## Section 10: anti-patterns

| Anti-pattern | Why it harms |
| --- | --- |
| Retrospective ADR-as-justification | Records a decision already made without honest alternative consideration |
| Excessive length | A 30-page ADR is rarely read |
| Omitted rejected alternatives | The reader cannot understand why this option won |
| Status that does not change | Decisions that should have been deprecated are presented as current |
| Locked to one author's vocabulary | Highly idiosyncratic language prevents future readers from understanding |
| Aspirational without commitment | A decision recorded but not enforced becomes irrelevant |

---

## Operating expectations

1. Significant architecture decisions are recorded; absence of an ADR for a contested decision is itself a finding.
2. ADRs are written close to the time the decision is made, not months later.
3. ADRs are reviewed annually within the system they govern; outdated ADRs are deprecated or superseded.
4. New engineers are pointed at the ADR set as part of system onboarding.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| Michael Nygard ADR practice | Original ADR concept | Reference practice |
| ISO/IEC/IEEE 42010:2022 | Architecture description | Architecture documentation |
| Open Group TOGAF Standard | Architecture deliverables | Enterprise architecture |
| C4 model | Documentation conventions | Compatibility |
| OWASP SAMM | Design | Software assurance maturity |
| NIST SP 800-218 | SSDF PO Plan | Secure software development |

---

## Limitations

This standard is a public-domain baseline. The specific template, storage tooling, indexing approach, and approval forum are organisation-specific. The standard expresses what an ADR is and what makes it useful, not a specific tool or layout.

---

**End of Document**
