# GRC LIBRARY CC ZERO INGESTION AND TRANSFORMATION SPECIFICATION  
Version 1.1.2

## PURPOSE
This specification defines how content is ingested, normalized, improved, and transformed into CC Zero licensed governance documents for the public GRC Library. It establishes authoritative rules for interpreting pasted content, determining its document type, transforming it into the approved structure, naming it, placing it in the correct directory, and identifying repository updates.

This specification overrides the Master Project Specification for all CC0 document creation, formatting, metadata, and placement operations.

---

## SCOPE
This specification applies to all pasted content that is to be:

1. Integrated into the CC Zero GRC Library.  
2. Converted into a CC0 governance document using the canonical metadata block.  
3. Normalized for clarity, consistency, and alignment with recognized standards.  
4. Positioned in the correct directory based on type and domain.  
5. Evaluated for overlap or conflict with existing repository documents.  
6. Assessed for required updates to registers, matrices, mapping files, or indices.

The output always consists of:

1. A CC Zero licensed Markdown document inside a single fenced code block.  
2. A repository update register outside the code block.

Internal governance versions are produced only when explicitly requested.

---

## REFERENCE FRAMEWORKS AND ALIGNMENT EXPECTATIONS
Transformations must align with recognized frameworks, including:

- ISO/IEC 27001, 27701, 42001, 22301, 31000, 9001  
- NIST Cybersecurity Framework 2.0, NIST AI RMF, NIST SP 800 series  
- COBIT 2025 governance and management objectives  
- CSA Cloud Controls Matrix v5  
- Global privacy, cybersecurity, AI governance, ESG, and supply-chain regulatory obligations represented in library registers  

The assistant must not invent regulatory requirements or unsupported mappings.

---

## DIRECTORY STRUCTURE

### Core Directory
Used for documents not tied to a domain:
```
/core
```

### Topic Directories
Used for domain-focused material:
```
/ai
/resilience
/privacy
/supplier
```

Directory rules:

1. Place documents in a topic directory only if content primarily relates to that domain.  
2. Otherwise place in `/core`.  
3. No subdirectories may be created without explicit user instruction.

---

## DOCUMENT TYPE CLASSIFICATION  
**Allowed document types (v1.1.2):**

- Policy  
- Framework  
- Standard  
- Procedure  
- Plan  
- Guideline  
- Register  
- Matrix  
- Checklist  
- Specification  
- Charter  
- **Template (NEW in v1.1.2)**

The document type determines the filename prefix.

---

## FILENAME RULES
Filenames must follow the structure:

```
document-type-canonical-name.md
```

Examples:

- `policy-enterprise-access-control.md`  
- `framework-governance-charter.md`  
- `standard-logging-and-monitoring.md`  
- `procedure-identity-management.md`  
- `template-model-card.md`  
- `template-system-card.md`

Canonical name rules:

1. All lowercase letters.  
2. Spaces become single hyphens.  
3. All punctuation removed.  
4. Ampersand becomes “and”.  
5. No leading or trailing hyphens.  
6. No duplicate hyphens.  
7. Stop words are not removed.

---

## METADATA BLOCK REQUIREMENTS

Every document must begin with this metadata block (vertical key/value pairs, each on its own line):

```
Document Title
[Title]

Document Type
[Type]

Version
0.0.1

Date
[Year Month Day]

Owner
[Role only]

Approving Authority
[Generic role]

Related Documents
[List using canonical names + filenames]

Classification
Public

Category
[Domain category]

Review Frequency
[Schedule]

Repository Path
[/directory/document-type-canonical-name.md]

Confidentiality
Public
```

Metadata rules:

1. All new CC0 documents start at version **0.0.1**.  
2. Only substantive content changes increment the version.  
3. Document Title must match the canonical name in readable form.  
4. Owner must be a role, not a person.  
5. Approving Authority must use generic roles.  
6. Related Documents must reference canonical names and filenames.  
7. Classification defaults to **Public**.  
8. Confidentiality must always be **Public**.  
9. Repository Path must match directory and filename.  
10. No internal metadata, revision histories, or author fields may appear.

---

## CONTENT NORMALIZATION RULES

The assistant must:

1. Remove document control tables, authors, and organization-specific identifiers.  
2. Remove placeholders and proprietary terminology.  
3. Rewrite text for clarity and alignment with referenced frameworks.  
4. Remove document numbers and internal version histories.  
5. Maintain precise governance language.  
6. Use standard hyphenated grammar; avoid en and em dashes.  
7. Ensure content is globally reusable.  
8. Maintain clean GitHub-ready Markdown formatting.

---

## CANONICAL DOCUMENT STRUCTURE

Every CC0 document must follow:

1. Metadata Block  
2. Purpose  
3. Scope  
4. Objectives (if applicable)  
5. Governance and Accountability  
6. Policy or Control Statements / Methodology / Procedures  
7. Roles and Responsibilities  
8. Monitoring, Metrics, and Reporting  
9. Continuous Improvement  
10. References and Framework Alignment

Templates may replace #6 with a structured, reusable form section.

---

## COMPARATIVE ANALYSIS WORKFLOW

If a document with the same canonical filename already exists:

1. Compare pasted content to the existing version.  
2. Identify alignment, deltas, gaps, regressions, and improvements.  
3. Recommend replace, merge, or retain.  
4. Await user approval before updating.  
5. Perform no unauthorized overwrites.

---

## REPOSITORY UPDATE REGISTER RULES

Every transformation must list:

1. Files requiring updates.  
2. Any new registers, matrices, templates, or supporting documents required.  
3. Required additions to the key-terms-and-definitions register.  
4. Required directory or taxonomy updates (if any).

---

## NEW SUPPORTING DOCUMENT WORKFLOW

When content indicates the need for additional artefacts:

1. Identify the required supporting document explicitly.  
2. Provide a recommended name and filename.  
3. Provide a brief description of purpose.  
4. Ask whether the user wants it created next.

---

## TERMS AND DEFINITIONS HANDLING

1. Reference the `key-terms-and-definitions.md` register.  
2. Define terms locally only when essential.  
3. Identify new required terms in the update register.

---

## FINAL OUTPUT RULES

1. Exactly one fenced code block per generated CC0 document.  
2. Repository update register outside the code block.  
3. No commentary inside the CC0 document.  
4. Strict adherence to canonical filenames.  
5. Confidentiality and classification always Public.  
6. No operational or meta-system data allowed in documents.

---

# End of Specification v1.1.2
