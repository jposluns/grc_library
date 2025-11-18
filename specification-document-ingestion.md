# GRC Library CC Zero Ingestion and Transformation Specification  
Version 1.1.1

## 1. Purpose

This specification defines authoritative rules for ingesting, transforming, normalizing, and producing CC Zero licensed governance documents for the public GRC Library. It ensures consistent structure, terminology, formatting, metadata, naming conventions, and directory placement. This specification overrides all other project specifications when producing CC0 governance outputs.

## 2. Scope

This specification applies to all user-submitted content intended to be transformed into CC0 governance documents, including policies, standards, procedures, frameworks, plans, guidelines, registers, matrices, checklists, specifications, and charters.

It governs:
1. Document type determination.  
2. Canonical filename construction.  
3. Directory placement.  
4. Canonical metadata block formatting and values.  
5. Content normalization.  
6. Removal of internal references or identifiers.  
7. Production of CC0-ready Markdown.  
8. Generation of repository update registers.  
9. Identification and extraction of reusable annexes or matrices.

Internal governance versions are produced only when explicitly requested.

## 3. Reference Frameworks and Alignment

Transformations must align with:
1. ISO and IEC standards including 27001, 27002, 27701, 42001, 22301, 31000, 9001, and 23894.  
2. NIST Cybersecurity Framework 2.0, NIST AI RMF, and NIST SP 800 series.  
3. COBIT 2025 governance and management objectives.  
4. CSA Cloud Controls Matrix v5.  
5. Global regulatory obligations reflected in library registers.  
6. AI governance and safety frameworks.  
7. Supply chain security frameworks including WCO SAFE, ISO 28000, BASC, PIP, CTPAT, and AEO.

No regulatory requirements may be invented or implied without reference support.

## 4. Directory Structure

Documents must be placed in one of the following directories:

- /core  
- /ai  
- /resilience  
- /privacy  
- /supplier

Rules:
1. Use topic directories only when the document primarily belongs to that domain.  
2. All other documents go in /core.  
3. No new directories may be created without explicit user instruction.  
4. Reusable annexes or matrices must be separate CC0 documents stored in the appropriate domain directory.

## 5. Document Type Classification

Each document must be classified as exactly one of the following types, which determines the filename prefix:

Policy, Framework, Standard, Procedure, Plan, Guideline, Register, Matrix, Checklist, Specification, Charter.

## 6. Filename Rules

Filenames must follow:

document-type-canonical-name.md

Canonical-name rules:
1. Lowercase only.  
2. Spaces replaced with single hyphens.  
3. All punctuation removed.  
4. Ampersands replaced with "and".  
5. No duplicate or trailing hyphens.  
6. Stop words are not removed.

Examples:
- policy-enterprise-access-control.md  
- standard-ai-lifecycle-governance.md  

## 7. Metadata Block Requirements

Every CC0 document must begin with the following metadata block, in this exact order and format:

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

Rules:
1. Initial version is always 0.0.1.  
2. Only minor version increments occur for substantive updates.  
3. Document Title must be readable and must not include the document type.  
4. Owner must be a role, not an individual.  
5. Approving Authority must be one generic role (e.g., Chief Compliance Officer).  
6. Related Documents must list titles and filenames, one per line.  
7. Classification must be one of: Public, Internal, Restricted (default: Public).  
8. Review Frequency must be a discrete interval such as "Annual".  
9. Repository Path must reflect the directory and canonical filename.  
10. Confidentiality must match the classification.  
11. Tables are not permitted in metadata.  
12. No author names, approval tables, or revision histories are permitted.

## 8. Content Normalization Rules

The assistant must:
1. Remove document control tables, revision histories, approval records, author names, or employer identifiers.  
2. Remove internal numbering such as document IDs or references to internal frameworks.  
3. Rewrite content to be globally reusable, jurisdiction-neutral, and organization-agnostic.  
4. Replace organization-specific roles with standardized governance roles.  
5. Remove placeholders and incomplete sections.  
6. Avoid en and em dashes.  
7. Preserve unverified references but label them “[Unverified]”.  
8. Align AI content with ISO 23894 and NIST AI RMF.  
9. Align supply chain references with global, vendor-neutral frameworks.

## 9. Canonical CC0 Document Structure

All CC0 documents must follow this structure and ordering:

1. Metadata Block  
2. Purpose  
3. Scope  
4. Objectives (optional but recommended)  
5. Governance and Accountability  
6. Policy or Control Statements / Methodology / Procedures  
7. Roles and Responsibilities  
8. Monitoring, Metrics, and Reporting  
9. Continuous Improvement  
10. References and Framework Alignment

Rules:
1. Document Control and Approval sections are not included in CC0 documents.  
2. Definitions sections must be minimal; new terms must be added to global registers.  
3. Mapping tables or matrices must not be embedded directly.

## 10. Rules for Matrices and Annexes

1. Any reusable matrix, mapping table, or annex must be extracted into a separate CC0 file.  
2. The parent document must reference the matrix through Related Documents and within body text where relevant.  
3. Matrix documents must use the “Matrix” document type and follow all metadata and filename rules.  
4. Annexes are not embedded in CC0 documents and must be published as standalone documents.  
5. When users provide embedded matrices, the assistant must extract them, create standalone matrix files, and reference them in the repository update register.

## 11. Comparative Analysis Workflow

When a document with the same canonical filename already exists:
1. Compare new content with the existing file.  
2. Identify improvements, regressions, gaps, and conflicts.  
3. Recommend whether to replace, merge, or retain the existing document.  
4. Summarize differences clearly.  
5. Await explicit approval before modifying existing content.

## 12. Repository Update Register Rules

Each ingestion must include a repository update register that identifies:
1. Newly created files.  
2. Files requiring updates.  
3. Required new matrices, registers, or supporting documents.  
4. Required additions to the key terms and definitions register.  
5. Recommended new documents or expansions.  
6. Any potential impacts to existing files.

The repository update register appears after the CC0 document and is not inside the code block.

## 13. Terms and Definitions Handling

1. The authoritative source is key-terms-and-definitions.md.  
2. Local Definitions sections are permitted only when necessary.  
3. New terms must be added to the repository update register.  
4. Role definitions may reference a role-authority-register.md if present.  
5. All definitions must be globally neutral.

## 14. Final Output Rules

1. The CC0 document must be delivered in exactly one fenced code block.  
2. No commentary or operational notes may appear inside the code block.  
3. Document must comply with directory and filename rules.  
4. Repository update register follows the code block.  
5. No meta-operational, system, or audit data may appear in CC0 outputs.
