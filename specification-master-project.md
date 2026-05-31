# Master Project Specification

**Document Title:** Master Project Specification\
**Document Type:** Specification\
**Version:** 1.5.0\
**Date:** 2026-05-31\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Chief Risk Officer\
**Related Documents:** [`specification-ingestion.md`](specification-ingestion.md), [`instruction-ai-document-ingestion.md`](instruction-ai-document-ingestion.md), [`README.md`](README.md), [`NOTICE.md`](NOTICE.md), [`governance/charter-governance-library.md`](governance/charter-governance-library.md), [`governance/framework-document-architecture-and-interrelationship.md`](governance/framework-document-architecture-and-interrelationship.md)\
**Classification:** Public\
**Category:** Meta-Governance\
**Review Frequency:** Annual and upon material repository structure, governance, or licence change\
**Repository Path:** [`specification-master-project.md`](specification-master-project.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This specification governs all behaviour, processing, reasoning constraints, file generation, directory placement, and structural rules used by the AI within this project. It defines authoritative requirements for output consistency, safety, determinism, formatting, and governance alignment. All subordinate specifications, including the Ingestion Specification, operate under this Master Project Specification unless explicitly delegated otherwise.

---

## Scope

This specification applies to every AI response within the project, including:

1. Document ingestion and transformation to library-canonical form.
2. Governance document generation.
3. Registers, matrices, templates, and mapping documents.
4. Analysis, interpretation, and architectural planning.
5. Behavioural, linguistic, and formatting constraints.
6. All directories and domain structures governed by this project.

---

## 1. Canonical governing order

1. Master Project Specification (this document).
2. Ingestion Specification (latest version).
3. Domain architecture rules (AI, security, privacy, resilience, etc.).
4. Document-type rules (policy, standard, procedure, etc.).
5. Any user-provided overrides.

When conflict occurs, the highest item prevails. Exception: where any conflict concerns licence compatibility with the library's CC BY-SA 4.0 licence (for example, a proposal to incorporate externally licensed content), the more restrictive rule prevails regardless of document position in this order.

---

## 2. Behavioural requirements for the AI

The AI must:

1. Use a formal, precise, consistent governance tone.
2. Avoid ambiguity unless ambiguity is explicitly required.
3. Interpret user intent without commenting on spelling or grammar.
4. Apply governance, risk, compliance, and security terminology correctly.
5. Produce deterministic, structured outputs.
6. Never hallucinate or invent governance content.
7. Use project rules over internal model defaults.
8. Never expose internal chain-of-thought, hidden reasoning, or engine analysis.
9. Identify rule conflicts and request clarification.
10. Apply regulatory and standards references only when supported by user content or recognized frameworks listed in Section 7.
11. Preserve user intent exactly while improving clarity, structure, and compliance with this specification.

---

## 3. Document output rule

When producing governance documents in a chat or interactive interface, each document must be contained inside exactly one fenced code block. The fenced block must use backticks (` ``` `) with no language tag unless the user specifically requests one. Nothing may appear inside the fence except the document itself. All commentary, analysis, and repository-update registers must appear outside the fenced block. Multi-document outputs require user approval: one document per output.

When working in a git repository via direct file tooling (read, write, edit operations), documents are written directly to files. The code fence rule does not apply to direct file operations.

---

## 4. Repository architecture

Top-level structure for governance artefacts:

```text
/specification-master-project.md
/specification-ingestion.md
/instruction-ai-document-ingestion.md
/README.md
/NOTICE.md
/LICENSE
/governance/
/security/
/ai/
/privacy/
/resilience/
/supply-chain/
/compliance/
/risk/
/dev-security/
/operations/
/architecture/
```

The `/compliance/` domain contains sector-specific sub-directories (`logistics/`, `financial-services/`, `healthcare/`, `energy-and-utilities/`, `telecommunications/`, `public-sector/`) for sector-conditional content; see the compliance README for the structure.

Repository infrastructure directories and files that are not used for governance artefacts but are part of the repository:

```text
/CONTRIBUTING.md       Contribution workflow, metadata block, style and filename rules.
/CHANGELOG.md          Phase-level history of repository changes.
/SECURITY.md           How to report content accuracy defects, licence concerns,
                       organisation or personal data leakage, broken links, tooling defects.
/.pre-commit-config.yaml  Local pre-commit hooks wiring the audit scripts.
/.github/              GitHub Actions workflow that runs the audits on push to main
                       and on every pull request.
/tools/                Stdlib-only Python audit scripts and taxonomy / portal generators.
/docs/                 Adopter-facing documentation not subject to the canonical governance
                       artefact metadata block (adopter guide, worked example, auto-generated
                       portal and maturity scorecard).
/taxonomy.yml          Auto-generated machine-readable registry of every active artefact's
                       canonical metadata. Regenerated from document metadata by
                       tools/build-taxonomy.py.
```

Documents subject to this specification are placed only in the governance-artefact directories above. The infrastructure directories are exempt from the 13-field canonical metadata block and from the structural-membership rules (see Section 5 and the structural auditor exemption list).

### 4.1 Directory rules

1. All documents must be placed in one of the approved directories listed in Section 4.
2. No directory shall contain non-canonical document types.
3. No directory expansions are allowed without explicit user approval.
4. Specifications always remain at root level.
5. Each file must follow canonical naming: `document-type-canonical-name.md`.
6. Each domain directory must contain a [`README.md`](README.md) that lists all active documents in that domain.

### 4.2 Domain purpose summary

| Directory | Primary Governance Purpose |
|---|---|
| `governance/` | Core governance: charter, frameworks, policies, registers, matrices, role authority, document architecture, cross-framework alignment, and assurance metrics |
| `security/` | Information security: policies, standards, procedures, access control, identity, cryptography, logging, classification, and secure operations |
| `ai/` | AI governance, AI security, model risk, AI lifecycle, documentation, assurance, testing, and AI data security |
| `privacy/` | Privacy governance, data protection, cross-border transfer, breach response, records retention, and data subject rights |
| `resilience/` | Business continuity, disaster recovery, crisis management, incident response, resilience testing, and recovery governance |
| `supply-chain/` | Supplier governance, third-party risk, cloud governance, supply-chain security, trade compliance programmes, and service-provider assurance |
| `compliance/` | Compliance management, legal and regulatory obligations, audit governance, sector-specific annexes, and trade compliance controls |
| `risk/` | Enterprise risk management, risk registers, KRIs, risk appetite, quantitative analysis, AI risk methodology, and third-party risk standards |
| `dev-security/` | Secure development standards, DevOps security, software composition analysis, developer quick references, and AI coding agent rule files |
| `operations/` | IT operations, asset management, change management, configuration management, and security operations registers |
| `architecture/` | Enterprise architecture practice: framework, decision records, reference architectures, technology radar, architecture review, API design, data architecture, and integration architecture |
| `compliance/<sector>/` | Sector-conditional sub-directories within compliance (`logistics/`, `financial-services/`, `healthcare/`, `energy-and-utilities/`, `telecommunications/`, `public-sector/`) hold sector-specific annexes, programme overlays (CTPAT, PIP, AEO, BASC, etc.), and sector-conditional artefacts. Organisations not participating in a covered sector or programme can ignore the corresponding sub-directory. |

### 4.3 Document-type definitions

Allowed types:

- Charter
- Framework
- Policy
- Standard
- Procedure
- SOP
- Plan
- Roadmap
- Guideline
- Guide
- Register
- Matrix
- Specification
- Template
- Annex
- Checklist
- Worklist

No additional types may be created without approval.

### 4.4 Type selection guidance

- Procedure versus SOP: a Procedure is a multi-actor or cross-functional workflow that coordinates several roles. An SOP is a single-actor or narrow team sequence with explicit step ownership for one repeatable task.
- Plan versus Roadmap: a Plan is event-triggered or schedule-bound coordination such as incident, recovery, migration, or communication. A Roadmap is a multi-phase forward strategy tied to a strategic outcome with phased milestones and dependencies.
- Guideline versus Guide: a Guideline is advisory interpretation of a policy or standard requirement and reads as governance commentary. A Guide is technical reference material organized for adoption such as patterns, examples, configuration models, or implementation walkthroughs.

### 4.5 Library versioning

The library as a whole carries a Calendar Versioning (CalVer) version separate from the per-document semantic versions defined in section 5. The library-level version answers the question "which snapshot of the library did the adopter take?".

#### Scheme

The library version is `YYYY.MM.patch` where:

- `YYYY` is the four-digit year of the most recent merge to `main`.
- `MM` is the two-digit month of the most recent merge to `main`.
- `patch` is a sequential counter that increments on every merge to `main` within the same `YYYY.MM` window. It resets to `0` when the month rolls over.

Examples: `2026.05.0`, `2026.05.7`, `2026.06.0`, `2026.12.42`.

#### Why CalVer

The library evolves continuously through small phased PRs rather than discrete versioned releases. CalVer is appropriate because:

- The most useful question for an adopter is "how recent is this?", not "is this a backwards-compatible upgrade?".
- The patch counter records cumulative churn within a month, surfacing the high merge frequency that semantic versioning would obscure.
- No judgment is needed to decide between major/minor/patch bumps; the scheme is mechanical.

#### Where the version is recorded

The current library version is displayed in `README.md`'s metadata block as the field `Library Version`. The CHANGELOG records the library version at the time of each phase's completion in the phase heading.

#### Maintenance

Each PR that merges to `main` updates `README.md`'s `Library Version` field as part of the PR:

- If the merge falls in the same calendar month as the current version, increment the patch.
- If the calendar month has changed, set the new version to `YYYY.MM.0`.

The version bump is the author's responsibility on the PR that introduces the change. The audit suite does not automatically enforce monotonicity, but reviewers should verify the bump is present before approving the PR.

#### Relationship to per-document versioning

Per-document versions (section 5, semantic versioning) remain unchanged and continue independently. The library version is the **snapshot identifier** for the corpus as a whole; per-document SemVer is the **evolution marker** for each artefact and carries change-severity signal (major = breaking, minor = additive, patch = correction). The two schemes are deliberately different formats so a reader can tell at a glance which is which: `2026.05.7` is always a library version; `1.2.1` is always a document version. They are not substitutes for each other.

A document may move from `1.2.0` to `1.2.1` within library version `2026.05.7`, and another document in the same PR may move from `0.0.1` to `1.0.0`. The library version aggregates these into a single point-in-time identifier for the corpus.

---

## 5. Metadata requirements

Every generated governance document must include the canonical metadata block with the following fields, in this order:

1. Document Title
2. Document Type
3. Version
4. Date
5. Owner
6. Approving Authority
7. Related Documents
8. Classification
9. Category
10. Review Frequency
11. Repository Path
12. Confidentiality
13. License

Rules:

- Version always begins at `0.0.1`. See the Ingestion Specification for version advancement rules.
- Owner and Approving Authority must be roles, not individuals.
- Dates use ISO 8601 format: `YYYY-MM-DD`.
- Classification defaults to Public unless the user requires otherwise.
- Related Documents must reference canonical filenames using repository-relative paths.
- License is always `CC BY-SA 4.0`.

---

## 6. Formatting and style requirements

1. Use plain Markdown only.
2. No HTML, no images, no emojis.
3. No nested tables.
4. No wide or overflow tables in standard documents.
5. One sentence per line recommended for policies and standards.
6. Section order must follow the canonical order defined in the Ingestion Specification.
7. All text must be globally reusable and must not contain organisation-specific references.
8. Apply the sanitization substitution table in Appendix A of the Ingestion Specification to all content.
9. Use Oxford English with `-ize` forms where applicable.
10. Do not use em dashes or en dashes.
11. Pair `ensure` with `that`; do not use bare `ensure` or `ensures`.
12. Use sentence case for all section headings (H2 through H6). The first word is capitalised; subsequent words are lowercase except proper nouns and acronyms. Section identifiers such as `A1.`, `Step 1:`, and `Category 1:` count as numbering, not as the first word, so the word that follows must be capitalised. H1 document titles may use Title Case where they name a controlled artefact (e.g. policy or standard title).

---

## 7. External framework alignment

When referencing standards and frameworks, the AI must only reference publicly recognized frameworks. The following are confirmed for use in this repository:

### Information security and risk

- ISO/IEC 27001:2022: Information security management systems
- ISO/IEC 27002:2022: Information security controls
- ISO/IEC 27701:2025: Privacy information management (standalone PIMS standard since the 2025 revision)
- ISO/IEC 42001:2023: AI management systems
- ISO/IEC 23894:2023: AI risk management guidance
- ISO/IEC 22301:2019: Business continuity management
- ISO 31000:2018: Risk management
- ISO 9001:2015: Quality management
- NIST CSF 2.0: Cybersecurity Framework
- NIST SP 800-53 Rev 5: Security and privacy controls
- NIST SP 800-37: Risk Management Framework
- NIST SP 800-218: Secure Software Development Framework (SSDF)
- NIST AI RMF: AI Risk Management Framework
- COBIT 2019: IT governance and management
- CSA CCM v4: Cloud Controls Matrix
- CIS Benchmarks: Configuration security baselines
- MITRE ATT&CK: Adversarial tactics and techniques
- MITRE ATLAS: Adversarial ML threat landscape

### Privacy and data protection

- GDPR: General Data Protection Regulation (EU)
- UK GDPR: United Kingdom General Data Protection Regulation
- PIPEDA / CPPA: Canadian privacy legislation
- AIDA: Artificial Intelligence and Data Act (Canada)
- PIPL: Personal Information Protection Law (China)
- LGPD: Lei Geral de Proteção de Dados (Brazil)
- Quebec Law 25: Act respecting the protection of personal information

### AI and emerging technology

- EU AI Act: Regulation on Artificial Intelligence
- OWASP LLM Top 10: Large Language Model application risks
- OWASP Top 10: Web application security risks
- OWASP ASVS: Application Security Verification Standard

### Trade compliance and supply chain

- CTPAT: Customs-Trade Partnership Against Terrorism (US CBP)
- AEO: Authorized Economic Operator (EU)
- AEO-S, Authorized Economic Operator, Security and Safety (UK HMRC)
- PIP: Partners in Protection (Canada CBSA)
- BASC: Business Alliance for Secure Commerce
- NEEC: Nuevo Esquema de Empresas Certificadas (Mexico)
- OEA: Operador Económico Autorizado (Brazil)
- WCO SAFE Framework of Standards
- ISO 28000: Supply chain security management systems

### Resilience and operational technology

- IEC 62443: Industrial cybersecurity
- DORA: Digital Operational Resilience Act (EU)
- NIS 2 Directive: Network and Information Security (EU)
- SLSA: Supply-chain Levels for Software Artifacts

### Financial and sector-specific

- PCI DSS v4.0: Payment card industry data security standard
- HIPAA: Health Insurance Portability and Accountability Act (US)
- SOX: Sarbanes-Oxley Act (US)
- FedRAMP: Federal Risk and Authorization Management Program (US)
- OSFI B-13: Technology and Cyber Risk Management (Canada)

References must be accurate and must not be invented. Do not reference frameworks not appearing in this list without explicit user confirmation that the framework is applicable.

---

## 8. Governance document generation rules

1. All content must be normalized to organisation-neutral, original-authorship language. The library does not incorporate externally licensed verbatim text.
2. Documents must adhere to the canonical structure:
 - Metadata
 - Purpose
 - Scope
 - Objectives (if applicable)
 - Governance and Accountability
 - Policy, Controls, Methods, or Procedures
 - Roles and Responsibilities
 - Monitoring, Metrics, and Reporting
 - Continuous Improvement
 - References and Framework Alignment
3. User intent always prevails over automatic restructuring if conflict arises.

---

## 9. Register and matrix rules

1. Registers and matrices must follow the directory and naming rules.
2. Multi-row matrices must be broken into multiple small tables if they exceed width limits.
3. Cross-framework or cross-jurisdiction mapping documents must follow the Multi-Block Matrix Guidance in the Ingestion Specification.

---

## 10. Index and README maintenance

1. Every new active document must be added to [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md).
2. Every new active document must be added to the Active Documents table in the domain-level [`README.md`](README.md) for its directory.
3. When a planned document becomes active, the Planned Expansion section of the relevant [`README.md`](README.md) must be struck through or removed.
4. The document index version must be incremented when entries are added or removed.

---

## 11. Conflict resolution rules

1. If any project rule conflicts with user instructions, request clarification.
2. If user intent is clear and conflicts with the Ingestion Specification, the Master Project Specification prevails unless the conflict concerns licence-compatibility constraints (the more restrictive rule prevails on licence-compatibility matters).
3. If a conflict exists between this document and any generated content, this document prevails.

---

**End of Document**
