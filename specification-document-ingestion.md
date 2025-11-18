GRC LIBRARY CC ZERO INGESTION AND TRANSFORMATION SPECIFICATION
VERSION 1.1.0

PURPOSE
This specification defines how content is ingested, normalized, improved, and transformed into CC Zero licensed governance documents for the public GRC library. It establishes authoritative rules for interpreting pasted content, determining its document type, transforming it into the approved structure, naming it, placing it in the correct directory, and identifying repository updates. This specification overrides the Master Project Specification for all CC0 document creation, formatting, metadata, and placement operations.

SCOPE
This specification applies to all pasted content that is to be:
1. Integrated into the CC Zero GRC library.
2. Converted into a CC0 governance document using the canonical metadata block.
3. Normalized for clarity, consistency, and alignment with recognized standards.
4. Positioned in the correct directory based on type and domain.
5. Evaluated for overlap or conflict with existing repository documents.
6. Assessed for required updates to registers, matrices, mapping files, or indices.

The output always consists of:
1. A CC Zero licensed Markdown document inside a single fenced code block.
2. A repository update register outside the code block.

This specification governs CC0 outputs exclusively. Internal governance versions are produced only when explicitly requested.

REFERENCE FRAMEWORKS AND ALIGNMENT EXPECTATIONS
All transformations must align with recognized frameworks including:
1. ISO and IEC standards: 27001, 27701, 42001, 22301, 31000, 9001 and related.
2. NIST frameworks: Cybersecurity Framework 2.0, NIST AI RMF, and the 800 series.
3. COBIT 2025 governance and management objectives.
4. CSA Cloud Controls Matrix v5.
5. Global regulatory obligations represented in library registers: privacy, cybersecurity, AI governance, ESG, and supply chain integrity.

The assistant must not invent regulatory requirements or unsupported mappings.

DIRECTORY STRUCTURE
All CC0 documents must be placed into either the core directory or one of the defined domain directories.

CORE DIRECTORY
Used for documents that are not domain specific.

/core

TOPIC DIRECTORIES
Used for domain-focused material with multiple document types.
/ai
/resilience
/privacy
/supplier

Directory rules:
1. Place documents in a topic directory only if content primarily relates to that domain.
2. Otherwise place in /core.
3. No subdirectories may be created under /core or any topic directory without explicit user instruction.

DOCUMENT TYPE CLASSIFICATION
Each pasted document must be assigned one of the following types:
Policy
Framework
Standard
Procedure
Plan
Guideline
Register
Matrix
Checklist
Specification
Charter

The document type determines the filename prefix.

FILENAME RULES
All filenames must follow the structure:

document-type dash canonical-name dot md

Examples:
policy-enterprise-access-control.md
framework-governance-charter.md
standard-logging-and-monitoring.md
procedure-identity-management.md
register-document-index-and-classification.md

Canonical name rules:
1. All lowercase letters.
2. Spaces become a single hyphen.
3. All punctuation removed.
4. Ampersand becomes “and”.
5. No leading or trailing hyphens.
6. No duplicate hyphens.
7. Stop words are not removed.

METADATA BLOCK REQUIREMENTS
Every document must begin with this metadata block:

Document Title
Document Type
Version
Date
Owner
Approving Authority
Related Documents
Classification
Category
Review Frequency
Repository Path
Confidentiality

Metadata rules:
1. Version must always be 0.0.1 for initial creation.
2. Only minor version increments occur on substantive content changes (not formatting or grammar).
3. Document Title must match the canonical name in a readable form.
4. Owner must be a role (not a person).
5. Approving Authority must use generic roles such as Chief Compliance Officer or Chief Legal Officer.
6. Related Documents must be listed by canonical name and filename, not numbers.
7. Classification defaults to Public unless the user requires Higher Classification.
8. Repository Path must reflect the directory and filename.
9. Dates use year space month space day format.
10. No internal metadata, confidentiality labels, authors, or revision histories may appear.

CONTENT NORMALIZATION RULES
The assistant must:
1. Remove document control tables, numbering, author fields, and employer identifiers.
2. Rewrite text for clarity, consistency, and alignment with referenced frameworks.
3. Remove placeholders and remove organization-specific language.
4. Remove references to document numbers.
5. Maintain a precise governance tone.
6. Use standard hyphenated grammar in sentences; hyphens in filenames only.
7. Avoid en and em dashes entirely.
8. Ensure all content is globally reusable and suitable for CC0.

CANONICAL DOCUMENT STRUCTURE
All CC0 documents must follow this order:

1. Metadata Block  
2. Purpose  
3. Scope  
4. Objectives (if applicable)  
5. Governance and Accountability  
6. Policy or Control Statements or Methodology or Procedures  
7. Roles and Responsibilities  
8. Monitoring, Metrics, and Reporting  
9. Continuous Improvement  
10. References and Framework Alignment  

COMPARATIVE ANALYSIS WORKFLOW
If a document with the same canonical name exists:
1. Compare pasted content to the existing repository version.
2. Identify alignment, deltas, gaps, regressions, and improvements.
3. Recommend whether to replace, merge, or retain the existing document.
4. Identify sections requiring updates.
5. Await user approval before replacing or updating.

REPOSITORY UPDATE REGISTER RULES
Every transformation must include a repository update register listing:
1. Files requiring updates (mandatory or recommended).
2. Any new registers, matrices, or supporting documents required.
3. Any new topics requiring directory expansion.
4. Any required additions to the key terms and definitions register.

NEW SUPPORTING DOCUMENT WORKFLOW
If a transformation indicates a new register, mapping table, annex, or index is required:
1. Identify it explicitly in the repository update register.
2. Provide a recommended name and filename.
3. Provide a brief description of the document’s purpose.
4. Ask whether the user wants it created next.

TERMS AND DEFINITIONS HANDLING
1. Reference the register key-terms-and-definitions.md file for shared terminology.
2. Define terms locally only when needed for clarity.
3. Identify any needed new terms in the repository update register.

FINAL OUTPUT RULES
1. Provide exactly one fenced code block for the complete CC0 document.
2. The repository update register must appear outside the code block.
3. No commentary or explanation may appear inside the document’s code block.
4. All content must comply with CC0 licensing rules.
5. Filename and directory placement rules must be strictly followed.
6. No operational, meta, or failure audit data may appear in CC0 outputs.

END OF INGESTION AND TRANSFORMATION SPECIFICATION
