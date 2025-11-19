# GRC Library CC0 Ingestion and Transformation Specification

| Field               | Value                                                          |
|---------------------|----------------------------------------------------------------|
| Document Title      | GRC Library CC0 Ingestion and Transformation Specification     |
| Document Type       | Specification                                                  |
| Version             | 1.1.3                                                          |
| Date                | 2025-11-18                                                     |
| Document Owner      | Chief Compliance Officer                                       |
| Approving Authority | Chief Risk Officer                                             |
| Related Documents   | framework-grc-document-architecture-and-interrelationships.md; master-project-specification.md |
| Classification      | Public – CC0                                                   |
| Category            | Meta-Governance                                                |
| Review Frequency    | Annual or on material process change                           |
| Repository Path     | /specification-ingestion.md                                    |
| Confidentiality     | Public (CC0 License)                                           |

---

## 1. Purpose

This specification defines how content is ingested, normalized, improved, and transformed into CC0-licensed governance documents for the public GRC Library.

It establishes authoritative rules for:
- Interpreting pasted content.  
- Determining document type and canonical filename.  
- Selecting the correct directory.  
- Constructing the metadata table.  
- Normalizing structure and language.  
- Handling matrices and registers.  
- Formatting ingestion outputs as a single, copy-pastable snippet.  

This specification overrides any other project guidance for: CC0 document creation, formatting, metadata, directory placement, and ingestion-output structure.

---

## 2. Scope

This specification applies to all content that is to be:

1. Integrated into the CC0 GRC Library.  
2. Converted into a CC0 governance document using the canonical metadata table.  
3. Normalized for clarity, consistency, and alignment with recognized standards.  
4. Positioned in the correct directory based on type and domain.  
5. Evaluated for overlap or conflict with existing repository documents.  
6. Assessed for required updates to registers, matrices, mapping files, or indices.  

The ingestion engine must apply this specification to every “ingest the following” instruction unless explicitly told otherwise.

---

## 3. Reference Frameworks

All transformations must align with the intent and terminology of:

1. ISO and IEC standards: 27001, 27701, 42001, 22301, 31000, 9001 and related.  
2. NIST frameworks: Cybersecurity Framework 2.0, NIST AI RMF, and relevant 800 series publications.  
3. COBIT 2025 governance and management objectives.  
4. CSA Cloud Controls Matrix v5.  
5. Global regulatory obligations represented in library registers: privacy, cybersecurity, AI governance, ESG, and supply chain integrity.

The ingestion engine must not invent regulatory requirements or unsupported mappings. Any unverified reference must be clearly indicated in the source content and preserved as “Unverified” only if the user supplied it.

---

## 4. Directory Structure

All CC0 documents must be placed into either the core directory or one of the defined domain directories.

### 4.1 Core Directory

Used for documents that are not domain-specific or that provide cross-domain meta-governance.

- /core  

Examples:
- Ingestion specification.  
- Document architecture framework.  
- Cross-framework compliance matrices.  
- Global regulatory mapping registers.

### 4.2 Topic Directories

Used for domain-focused material containing multiple document types.

- /ai  
- /resilience  
- /privacy  
- /supplier  
- /networking  

Rules:

1. Place documents in a topic directory only if content primarily relates to that domain.  
2. Otherwise place the document in /core.  
3. No subdirectories may be created under /core or any topic directory without explicit user instruction.  
4. When the user explicitly authorizes a new top-level domain directory, this specification must be updated to include it.

---

## 5. Document Type Classification

Each pasted document must be assigned one of the following types:

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
- Template  
- Annex  

The document type determines:
- The filename prefix.  
- The expected level of governance abstraction.  
- The canonical section structure.

If the type is ambiguous, the ingestion engine must select the closest match based on purpose and content and, if necessary, ask the user to confirm.

---

## 6. Filename Rules

All filenames must follow this structure:

- document-type + hyphen + canonical-name + .md  

Example:
- policy-governance-and-risk-management.md  
- framework-grc-document-architecture-and-interrelationships.md  
- standard-networking-and-communications.md  

### 6.1 Canonical Name Rules

1. All lowercase letters.  
2. Spaces become a single hyphen.  
3. All punctuation removed.  
4. Ampersand becomes “and”.  
5. No leading or trailing hyphens.  
6. No duplicate hyphens.  
7. Stop words are not removed.  
8. No version numbers or dates in filenames.

The ingestion engine must derive the canonical name from the Document Title, normalize it, and use it consistently in the metadata table and repository path.

---

## 7. Metadata Table Requirements

Every document must begin with:

1. An H1 title line (e.g., “# Policy: Governance and Risk Management”).  
2. A metadata table immediately below the title.

### 7.1 Mandatory Metadata Fields

The metadata table must contain at least the following fields:

- Document Title  
- Document Type  
- Version  
- Date  
- Document Owner  
- Approving Authority  
- Related Documents  
- Classification  
- Category  
- Review Frequency  
- Repository Path  
- Confidentiality  

Field names must appear exactly as above.

### 7.2 Metadata Table Format

1. The metadata must be a single Markdown table with “Field” and “Value” columns.  
2. Document Owner and Approving Authority must be roles, not personal names.  
3. Related Documents must list canonical names and filenames, separated by semicolons or commas.  
4. Classification defaults to “Public – CC0” unless the user explicitly directs otherwise.  
5. Confidentiality must be “Public (CC0 License)” for all library documents, unless the user has authorized a higher classification.

No narrative text may appear between the H1 title and the metadata table.

---

## 8. Content Normalization Rules

The ingestion engine must:

1. Remove document control tables, numbering, author fields, and employer identifiers.  
2. Remove or generalize organization-specific names and labels.  
3. Rewrite text for clarity, consistency, and alignment with referenced frameworks while preserving meaning.  
4. Remove references to proprietary document numbers (e.g., “Document 36”) and replace them with canonical filenames where possible.  
5. Use American English consistently.  
6. Maintain a precise governance tone.  
7. Avoid en and em dashes; use simple hyphenation.  
8. Ensure all content is globally reusable and suitable for CC0.

If removal of organization-specific data would materially change meaning, the engine must generalize instead of deleting.

---

## 9. Canonical Document Structure

Unless otherwise specified by the user, all CC0 documents must follow this order:

1. H1 Title  
2. Metadata Table  
3. Purpose  
4. Scope  
5. Objectives (if applicable)  
6. Governance and Accountability (for governance artefacts)  
7. Policy or Control Statements or Methodology or Procedures (as appropriate for the type)  
8. Roles and Responsibilities (if not covered in Governance section)  
9. Monitoring, Metrics, and Reporting  
10. Continuous Improvement  
11. References and Framework Alignment  
12. Definitions (if required)  
13. A closing marker: “**End of Document**”

Where a document type does not logically require every section (e.g., a short Template or Checklist), the ingestion engine may omit non-applicable sections, but Purpose and Scope must always be present.

---

## 10. Matrix and Table Construction Rules

This section governs any document whose primary role is mapping, cross-referencing, or tabular evidence presentation (Registers and Matrices in particular).

### 10.1 Block Matrix Pattern (Mandatory for Large Matrices)

To preserve readability and render correctly in GitHub:

1. Large multi-framework or multi-jurisdiction matrices must be organized into “blocks” by regulation, framework, or domain.  
2. Each block must be under a distinct heading (e.g., “## GDPR (EU 2016/679)”).  
3. Each block must use tables with no more than 4 columns.  
4. Where more columns are logically needed, they must be split into multiple tables (e.g., “Mapped Documents”, “Primary Obligations”, “Framework References”).  
5. No nested tables are permitted.  
6. Tables must avoid excessive width that causes horizontal scrolling.

### 10.2 Prohibited Matrix Patterns

The ingestion engine must avoid:

1. Single mega-tables spanning many frameworks, jurisdictions, or domains.  
2. Tables with more than 4 columns unless the user explicitly requests otherwise.  
3. Complex row-spanning or column-spanning layouts that will not render well in Markdown.  
4. Tables designed only for Confluence or word-processor layouts.

---

## 11. Primordial Code-Fence Enforcement Rule

This rule governs how the ingestion engine produces CC0 documents back to the user.

1. Every ingestion output must contain one and only one fenced code block containing the complete CC0 document.  
2. The fenced code block must be declared with a Markdown language hint (e.g., “markdown”).  
3. No other fenced code blocks may appear anywhere in the response.  
4. Inside the fenced code block there must be only the canonical CC0 document content.  
5. Repository update information, explanations, or commentary must appear outside the fenced block.  
6. The ingestion engine must self-validate that:  
   - The fenced block is syntactically complete.  
   - The document starts with an H1 and a metadata table.  
   - The document ends with “**End of Document**”.  

If any of these checks fail, the ingestion engine must correct the output before sending it.

This rule is primordial and overrides any other formatting guidance.

---

## 12. Comparative Analysis Workflow

If a document with the same canonical filename already exists in the repository:

1. The ingestion engine must not overwrite it automatically.  
2. The engine must perform a comparative analysis between the existing document and the newly ingested content.  
3. The engine must identify:  
   - Alignment and common sections.  
   - Deltas, gaps, and improvements.  
   - Potential regressions or losses of detail.  
4. The engine must recommend whether to:  
   - Replace the existing document.  
   - Merge content.  
   - Retain the existing document as-is.  
5. The engine must clearly request user approval before any replacement.

Only after explicit user confirmation may the engine propose a replacement file or merged version.

---

## 13. Repository Update Register Rules

Every ingestion response must include a repository update register outside the main code block.

The register must list:

1. Files requiring updates (mandatory or recommended).  
2. Any new registers, matrices, or supporting documents required.  
3. Any new topics requiring directory expansion.  
4. Any required additions to the key terms and definitions register.  

The register must be concise and structured so that it can be easily transcribed into a change log or task list.

---

## 14. New Supporting Document Workflow

If a transformation indicates that a new register, mapping table, annex, template, checklist, or index is required, the ingestion engine must:

1. Identify it explicitly in the repository update register.  
2. Provide a recommended document title and canonical filename.  
3. Provide a brief description of the document’s purpose and domain.  
4. Ask whether the user wants that supporting document created next.

The engine must not auto-generate supporting documents unless the user instructs it to do so.

---

## 15. Terms and Definitions Handling

1. The GRC Library must maintain a central register key-terms-and-definitions.md.  
2. Documents must reference the central register for shared terminology rather than defining common terms locally.  
3. Local definitions should be used only when needed for clarity or when a term is used in a specialized way.  
4. Any new terms identified during ingestion must be captured in the repository update register as candidates for inclusion in the central register.

---

## 16. Final Output Rules

Every ingestion operation must produce:

1. A single fenced code block containing the complete CC0 document, ready for direct copy and paste into the repository.  
2. A repository update register outside the code block.  

Inside the CC0 document:

- No meta operational data.  
- No failure audit data.  
- No system or assistant context.  
- No prose explanations of the ingestion process.

All CC0 documents must be fully usable by a human reader and automation tooling without editing.

---

## 17. Change History

| Version | Date       | Summary                                                          |
|---------|------------|------------------------------------------------------------------|
| 1.1.3   | 2025-11-18 | Added metadata-table requirement, block-matrix rules, and primordial code-fence enforcement; reorganized structure. |
| 1.1.2   | 2025-11-17 | Added Template as allowed document type; clarified directory rules. |
| 1.1.1   | 2025-11-16 | Harmonized metadata fields and canonical filename rules.         |
| 1.1.0   | 2025-11-15 | Initial ingestion specification for CC0 GRC Library.            |

**End of Document**
