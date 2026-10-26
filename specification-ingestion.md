# GRC Library Ingestion and Transformation Specification

**Document Title:** GRC Library Ingestion and Transformation Specification\
**Document Type:** Specification\
**Version:** 1.9.2\
**Date:** 2026-10-26\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`README.md`](README.md), [`NOTICE.md`](NOTICE.md), [`governance/charter-governance-library.md`](governance/charter-governance-library.md), [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md), [`governance/framework-document-architecture-and-interrelationship.md`](governance/framework-document-architecture-and-interrelationship.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material repository, licence, or source-framework change\
**Repository Path:** [`specification-ingestion.md`](specification-ingestion.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This specification defines how source material is converted into organization-neutral, library-canonical governance documents for the public GRC Documentation Library. The library is released under CC BY-SA 4.0; ingestion enforces original-authorship and library-canonical structure.

It establishes rules for:

- Assessing source material for licence compatibility.
- Removing identifying and organization-specific information.
- Selecting document type and canonical filename.
- Selecting repository domain.
- Applying metadata and document structure.
- Separating legal obligation, regulatory interpretation, industry practice, contractual requirement, and architectural recommendation.
- Avoiding verbatim reproduction of restricted source material.
- Updating indexes, registers, domain READMEs, and related artefacts.

---

## Scope

This specification applies to all content added to, modified in, or synthesized for this repository.

It applies to source material from internal documents, public standards, control frameworks, legal or regulatory references, audit guidance, questionnaires, implementation guides, metrics catalogues, and user-provided drafts.

---

## Licence compatibility rules

All original repository content is released under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).

The library's principle is that it does not copy external third-party verbatim content, with one exception. Source material is used for non-verbatim reference (framework identifiers, control families, domain-level alignment, applicability structure, original commentary in the library's own words). The exception, the same one [`NOTICE.md`](NOTICE.md) states, covers two kinds of source: a document may carry a short, attributed verbatim quotation of (a) a government or regulatory text (for example a statute, a regulation, or a government policy or directive) or (b) a standard or framework text that is in the public domain or openly licensed (for example a NIST SP or FIPS publication, the NIST CSF, or a framework under CC0 1.0, CC BY 4.0, or CC BY-SA 4.0), where the source licence permits quotation (for example an Open Government Licence whose only condition is attribution) and is compatible with CC BY-SA 4.0, as the licence lists below decide. Standards and frameworks under other licences are paraphrased with pinpoint citations. Short means at most one provision or passage and at most 100 words per quotation, and no longer than what the document relies on. Only a translation that the government itself publishes counts as a government text. Any other translation, including one that a body other than the government publishes (for example the KLRI English translations of Korean statutes), is a third-party translation: it is quoted only under its own publisher's terms, where they permit quotation and are compatible with CC BY-SA 4.0 as the licence lists below decide, and is otherwise paraphrased with pinpoint citations. Everything else from a third-party source is paraphrased or cited, not quoted.

Where a contributor proposes to incorporate verbatim or near-verbatim third-party content, which the library accepts only as a quotation the exception allows, the contributor must confirm that the source licence permits quotation and is compatible with CC BY-SA 4.0 and that the contribution preserves the source's attribution and licence notices. A quoting document records its licence basis in one place: a **Licence basis** statement beside the document's quotation convention (beside each convention where the document quotes more than one baseline of sources), naming, for each quoted source, the licence or public-domain status that the held text of that source states or, once the publisher's terms for it are held, that those acquired terms state; a one-off quotation, which no quotation convention covers, carries its Licence basis beside the quotation itself. Where neither the held text nor any acquired terms state a licence, the statement says so and names none; a licence or public-domain status is not inferred from the publisher's identity or from general knowledge. For a translation, the quoted source is the translation and its publisher is the body that publishes the translation (the government for a translation that the government itself publishes), not the publisher of the original text, as [`NOTICE.md`](NOTICE.md) defines; its Licence basis names the licence or public-domain status that the held translation or that publisher's acquired terms state. A new quotation needs a Licence basis that names a licence, or a public-domain status, permitting quotation; a statement that names none does not permit a new quotation. **Transition:** a quotation merged to `main` before the maintainer decision of 2026-10-24 23:52Z, or committed before that decision on branch `content/3b546-osfi`, which the decision lets merge, stays as it is until the publisher's terms are held (the event that [`NOTICE.md`](NOTICE.md) defines, which ends every ground at once), whatever its held text shows about its licence, its length, or its source type; the rule for a new quotation then applies to it. Each covered document is to carry a Licence basis statement saying that the transition clause covers it, which, once the publisher's terms are held, records the date they were held: the date the publisher's terms were acquired or, for a text in the public domain by statute or by expiry of its copyright term whose publisher makes no statement of that status, the date of the covered document's first scheduled review after that decision, at which [`NOTICE.md`](NOTICE.md) treats the terms as held; a tracked follow-up adds those statements. Editing a covered quotation makes it a new quotation. Quoted text keeps its source licence and is not relicensed under CC BY-SA 4.0. The licence lists below are the licence test a quotation under the exception must pass; a compatible licence does not by itself permit verbatim text outside the exception. Inbound licences known to be compatible with CC BY-SA 4.0 are: CC0 1.0 Universal (most permissive), CC BY 4.0 (with attribution), CC BY-SA 4.0 (the library's own licence, with attribution), an Open Government Licence whose only condition is attribution (with the attribution statement it requires; the Licence basis names the licence's version and jurisdiction and that statement), the MIT License and the Apache License 2.0 (each with the copyright and licence notices it requires, which the Licence basis names), and a public-domain status that the held text or the acquired terms state. The Open Government Licence is on this list under the maintainer decision of 2026-10-24 23:52Z, which names it as an example of a licence that permits quotation; CC0 1.0 and CC BY 4.0 are on it under the maintainer decision of 2026-10-25 01:01Z, which names CC-licensed frameworks among the openly licensed sources that may be quoted. Under the maintainer rulings of 2026-10-25 19:55Z and 19:57Z, the MIT License and the Apache License 2.0 are on it with their notices, and an Open Government Licence counts only where its only condition is attribution and its version and jurisdiction are named; another Open Government Licence is a licence not on this list. A licence not on this list is not treated as compatible without a maintainer ruling. A licence with a NonCommercial or NoDerivatives term is not compatible, whatever its version, so a CC-licensed framework under such a term is paraphrased. Inbound licences known to be incompatible include: CC BY-NC, CC BY-ND, CC BY-NC-SA, CC BY-NC-ND, GPL family (one-way the other direction), and proprietary or all-rights-reserved content; text under them is paraphrased with pinpoint citations. Third-party material vendored outside the library's documents is the separate carve-out that [`NOTICE.md`](NOTICE.md) records, under its own licence, not a quotation.

Do not copy into this repository, beyond the short, attributed quotation that [`NOTICE.md`](NOTICE.md) allows or its transition clause keeps, and other than the vendored third-party material that [`NOTICE.md`](NOTICE.md) records as a separate carve-out:

- Third-party control statements.
- Questionnaire text or answer options.
- Implementation guidance.
- Audit guidance.
- Metrics catalogue text.
- Tables reconstructed from restricted sources.
- Proprietary examples.
- Organization-specific evidence.

Permitted use includes independent synthesis, framework name references, high-level domain alignment, original commentary, evidence category mapping, non-verbatim applicability analysis, and the short, attributed quotation that [`NOTICE.md`](NOTICE.md) allows or its transition clause keeps.

---

## Organization-neutrality requirements

Repository content must not include:

- Real company names.
- Real people names.
- Email addresses.
- Phone numbers.
- Physical addresses.
- Tenant IDs.
- Domain names.
- IP addresses.
- Customer names.
- Supplier names.
- Contract references.
- Internal system names.
- Incident-specific details.
- Audit evidence.
- Screenshots or exports from internal systems.

Replace organization-specific details with generic roles, generic system categories, generic data classes, generic supplier classes, and generic evidence classes. Apply the organization-neutrality rules in Appendix A to all source content before producing output.

---

## Repository domains

Documents must be placed in the domain that best reflects their primary governance purpose.

```text
governance/    Core governance, charter, frameworks, policies, registers, matrices, role authority,
               document architecture, cross-framework alignment, and assurance metrics.

security/      Information security policies, standards, procedures, access control, identity,
               cryptography, logging, data classification, and secure operations.

ai/            AI governance, AI security, model risk, AI lifecycle, AI documentation, AI assurance,
               AI testing, and AI data security.

privacy/       Privacy governance, data protection, cross-border transfer, breach response,
               records retention, and data subject rights.

resilience/    Business continuity, disaster recovery, crisis management, incident response,
               resilience testing, emergency response, and recovery governance.

supply-chain/  Supplier governance, third-party risk, cloud governance, supply-chain security,
               trade compliance programmes, and service-provider assurance.

compliance/    Compliance management, legal and regulatory obligations, audit governance,
               sector-specific requirements, and trade compliance controls registers.

crypto/       Crypto-asset and blockchain governance: crypto-asset classification,
              custody and key control, blockchain-platform vetting, staking, and smart-contract risk.

risk/          Enterprise risk management, risk registers, key risk indicators, risk appetite,
               quantitative analysis, AI risk methodology, and third-party risk standards.

dev-security/  Secure development standards, DevOps security, software composition analysis,
               and developer quick references.

operations/    IT operations, asset management, change management, configuration management,
               and security operations registers.

architecture/  Enterprise architecture: framework, decision records, reference architectures,
               integration and data architecture, and technology radar.
```

The following directories and files exist in the repository but are not used for governance artefacts and are not in scope of this ingestion specification:

```text
CONTRIBUTING.md       Contribution workflow and rules.
CHANGELOG.md          Phase-level history.
SECURITY.md           Defect reporting path.
.pre-commit-config.yaml  Local pre-commit hooks.
.github/              GitHub Actions workflow.
tools/                Audit scripts and taxonomy / narrative registry / portal generators.
docs/                 Adopter documentation (not subject to canonical metadata; includes the auto-generated portal and maturity scorecard).
taxonomy.yml          Auto-generated machine-readable registry of artefact metadata and document structure.
narrative.yml         Auto-generated registry of executive narrative pages from executive/.
guardrails/           Portable Claude Code governance pack (rules, skills, meta); not a governance-artefact domain.
```

The structural auditor exempts these paths from the requirement that every markdown file appear in a domain README and in the document index register.

---

## Filename rules

Filenames must:

1. Use lowercase letters.
2. Use single hyphens between words.
3. Remove punctuation.
4. Replace ampersands with `and`.
5. Start with the document type prefix.
6. Avoid duplicate, trailing, or leading hyphens.
7. Avoid organization-specific product, vendor, system, or service names.

Examples:

- [`policy-information-security.md`](security/policy-information-security.md)
- [`standard-logging-and-monitoring.md`](security/standard-logging-and-monitoring.md)
- [`procedure-risk-register.md`](risk/procedure-risk-register.md)
- [`framework-ai-governance-and-risk.md`](ai/framework-ai-governance-and-risk.md)
- [`template-ai-system-register.md`](ai/template-ai-system-register.md)
- [`matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md)

---

## Document types

Allowed document types are:

- Charter
- Framework
- Policy
- Principle
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

### Type selection guidance

- Procedure versus SOP: a Procedure is a multi-actor or cross-functional workflow that coordinates several roles. An SOP is a single-actor or narrow team sequence with explicit step ownership for one repeatable task.
- Plan versus Roadmap: a Plan is event-triggered or schedule-bound coordination such as incident, recovery, migration, or communication. A Roadmap is a multi-phase forward strategy tied to a strategic outcome with phased milestones and dependencies.
- Guideline versus Guide: a Guideline is advisory interpretation of a policy or standard requirement and reads as governance commentary. A Guide is technical reference material organized for adoption such as patterns, examples, configuration models, or implementation walkthroughs.
- Template versus Worklist: a Template is a reusable blank skeleton meant to be copied into instances. A Worklist is a per-instance working artefact derived from a template, scoped to one batch or task, and typically retired or archived when the work is closed (the authoritative record migrates to a register or log).

The canonical filename prefix must match the Document Type field. Filenames use lowercase: `sop-`, `roadmap-`, and `guide-` are valid prefixes for the corresponding types.

---

## Canonical metadata

Every document must start with this metadata pattern. Every line of the metadata block except the last ends with a backslash character (`\`), which is CommonMark §6.7 syntax for a hard line break. This ensures GitHub and other CommonMark renderers display each metadata field on its own line:

```markdown
# Document Title

**Document Title:** Document Title\
**Document Type:** Policy\
**Version:** 1.0.0\
**Date:** YYYY-MM-DD\
**Owner:** Role Name\
**Approving Authority:** Role Name\
**Related Documents:** [`domain/related.md`](relative-path/related.md), [`domain/other.md`](../other-domain/other.md)\
**Classification:** Public\
**Category:** Domain Name\
**Review Frequency:** Annual and upon material change\
**Repository Path:** [`domain/file-name.md`](file-name.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0
```

Notes on the backslash-newline convention:

- Every metadata line except the last must end with `\` immediately before the line terminator.
- The last line (typically `License`) does not require the marker because the following blank line and `---` separator already create a paragraph break.
- Do not use two trailing spaces; that variant is also valid CommonMark but is invisible in source and is fragile against editor whitespace-stripping. The backslash is visible and editor-safe.
- The [`lint-metadata.py`](tools/lint-metadata.py) audit enforces this convention.

Related Documents and Repository Path use markdown links. The display text is the root-relative path. The link target is relative to the current file's directory: same-directory files use the bare filename; cross-directory files use `../` traversal.

Metadata must use role names only and must not use named individuals.

Dates must use ISO 8601 format: `YYYY-MM-DD`.

`Classification` and `Confidentiality` are distinct fields, not duplicates, even though every document in this corpus carries `Public` for both. `Classification` is the document's handling category within the library's own classification model (`Public` or `Reference Only`; see [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md)): it records whether a document is publishable or retained only for reference. Lifecycle is deliberately NOT part of this field: a superseded document keeps `Classification: Public` and inserts the optional lifecycle marker `**Status:** Superseded` after `Document Type` as a fourteenth metadata line, which the stub, required-sections, and section-placement audits key their redirect-notice exemption on (the 2026-07-02 lifecycle-marker migration; the former `Deprecated` classification value overloaded the field and is retired from active use). `Confidentiality` is the information-sensitivity tier of the content itself (the conventional information-security confidentiality label); for this organization-neutral, openly-licensed corpus it is always `Public`. The two coincide at `Public` here because the corpus is public on both axes, but they are conceptually independent: an adopter who forks the library may, for example, hold a document that is `Reference Only` on the handling axis while being `Confidential` on the sensitivity axis. Both fields are retained so a fork inherits both axes rather than conflating them.

---

## Version numbering

- All new documents begin at version `0.0.1`.
- Increment the patch segment (`0.0.x`) for corrections to content within an existing version (patch = correction).
- Increment the minor segment (`0.x.0`) for additive changes: substantive content additions, structural changes that break nothing, and policy revisions that add a requirement or permission while leaving existing content valid (minor = additive).
- Advance to `1.0.0` upon first formal approval and publication as a stable active document.
- Increment the major segment (`x.0.0`) for breaking changes: a structural or policy change that removes, reverses, or invalidates content or a requirement that existing documents or adopters rely on (major = breaking).

These are the per-document version rules (major = breaking, minor = additive, patch = correction). Section 4.5 of [`specification-master-project.md`](specification-master-project.md) summarizes them, and its section 5 points here for them.

---

## Required structural pattern

After metadata, documents should use this structure unless the document type requires a different structure:

1. Purpose.
2. Scope or Applicability.
3. Requirements, Policy Statements, Procedure, or Framework Components.
4. Evidence Requirements.
5. Limitations.
6. Maintenance or Review Requirements.
7. End of Document marker.

Documents must use `---` to separate major sections and must end with:

```markdown
**End of Document**
```

---

## Language requirements

Documents must use precise, organization-neutral language. They must avoid vendor-marketing language, unsupported maturity claims, and statements implying compliance, certification, regulatory approval, or operating effectiveness without implementation evidence.

Use Oxford English with `-ize` forms where applicable. Do not use em dashes or en dashes. Pair `ensure` with `that`; do not use bare `ensure` or `ensures`.

Use sentence case for all section headings (H2 through H6). The first word of the heading text is capitalized and subsequent words are lowercase except proper nouns and acronyms. Section identifiers such as `A1.`, `Step 1:`, and `Category 1:` count as numbering rather than as the first word, so the word that follows must be capitalized. H1 document titles may use Title Case where they name a controlled artefact such as a policy, standard, or charter title.

Do not state that a document ensures that compliance. State that it provides a baseline, structure, evidence class, or control model that adopting organizations must validate.

---

## Regulatory and framework mapping rules

Mappings must classify each statement as one of:

- Legal obligation.
- Regulatory interpretation.
- Contractual requirement.
- Industry practice.
- Architectural recommendation.
- Evidence category.

Mappings must include applicability conditions where jurisdiction, sector, processing role, deployment model, data residency, data category, or contractual obligation materially affects interpretation.

---

## AI content rules

AI documents must treat data as the primary risk surface and must address relevant lifecycle stages:

- Collection.
- Annotation.
- Storage.
- Processing.
- Training.
- Retrieval.
- Inference.
- Monitoring.
- Retention.
- Deletion.
- Decommissioning.

AI documents must explicitly consider prompt injection, indirect prompt injection, data poisoning, model inversion, membership inference, training data leakage, retrieval leakage, unsafe tool use, shadow AI, provenance, lineage, retention, and enforceable deletion where relevant.

---

## Quality gate

Before committing a document, validate that:

1. Metadata is complete and follows the canonical pattern including the `License` field.
2. Repository path matches actual file path.
3. License is CC BY-SA 4.0.
4. No prohibited identifiers are present; the Appendix A organization-neutrality rules have been applied.
5. No restricted third-party text is copied.
6. Roles are generic and role-based.
7. Classification is Public.
8. Framework and regulatory statements are scoped and not overstated.
9. Related Documents field references existing files using canonical paths.
10. The domain-level [`README.md`](README.md) Active Documents table is updated for all new documents.
11. The document index register ([`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md)) is updated for all new active documents.
12. The listing surfaces for each new document have been reviewed via [`tools/suggest-listing-surfaces.py`](tools/suggest-listing-surfaces.py) `<doc-path>`, which enumerates the MECHANICAL surfaces (items 10 and 11 above, plus the generated outputs it derives from the generator stages of [`tools/pre-push-guard.sh`](tools/pre-push-guard.sh), such as the taxonomy, the portal and the web corpus-link manifest, hard-gated by the listing-surface-completeness audit and each generator's own `--check`) and the SEMANTIC surfaces (the framework matrices and crosswalks, the glossary, and the document's own Related Documents field, which a human ratifies because their inclusion is relevance-based).

---

## Appendix a: organization-neutrality rules

Before producing any output, replace organization-specific detail with a generic category equivalent. Substitution is case-insensitive.

### Organization-specific terms

Replace any specific organization name, data-centre name, internal programme name, product, vendor, or system name with a generic category description (for example: the organization; the primary data centre; an enterprise identity provider; a SIEM; a secrets management service; an endpoint management platform; an ITSM portal; an external IR partner; an HR management system). Standard, publicly-recognized vendor products and services may be named directly where doing so does not identify a specific organization's environment.

### Incident and case references

Replace any named or numbered security incident or internal case reference with a generic form (for example: a prior security incident). Omit any confidential internal reference entirely.

### Personal names

| Source Term | Replacement |
|---|---|
| Any real person's name | omit or replace with role title |

### Terms to preserve without substitution

The following are public standards, frameworks, regulatory citations, and programme names that must not be substituted: ISO, NIST, COBIT, CSA CCM, BASC, WCO, ISO 28000, GDPR, PIPEDA, AIDA, CPPA, PIPL, LGPD, Quebec Law 25, UK GDPR, EU AI Act, FIDO2, MITRE ATT&CK, OWASP, PTES, OSCP, CREST, CVSS, CTPAT, PIP, AEO, AEO-S, HMRC, NEEC, OEA, DORA, NIS 2, PCI DSS, HIPAA, HITECH, SOX, FedRAMP, SLSA, FAIR, VEX, SBOM, HL7, FHIR, IEC 62443, IMO, ICAO, TSA, and all other recognized public regulatory, standards, or programme acronyms.

### Named open-source projects

Open-source projects whose canonical name includes a vendor parent (for example PyRIT, originating from a vendor) may be referenced by the project name alone, without the vendor parent, qualified by an explanatory phrase such as "open-source AI red team automation framework". Do not retain the vendor name in body text. Vendor-only proprietary products remain subject to the organization-neutrality rules above.

---

**End of Document**
