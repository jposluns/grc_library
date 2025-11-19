# Master Project Specification  
Version 1.0.2  
Date 2025-11-18  
Owner: Chief Compliance Officer  
Approving Authority: Chief Risk Officer  
Classification: Public  
Category: Meta-Governance  
Review Frequency: Annual  
Repository Path: /specification-master-project.md  
Confidentiality: Public

## Purpose
This specification governs all behavior, processing, reasoning constraints, file generation, directory placement, and structural rules used by the AI within this project. It defines authoritative requirements for output consistency, safety, determinism, formatting, and governance alignment. All subordinate specifications—including the Ingestion Specification—operate under this Master Project Specification unless explicitly delegated otherwise.

## Scope
This specification applies to every AI response within the project, including:  
1. Document ingestion and CC0 transformation.  
2. Governance document generation.  
3. Registers, matrices, templates, and mapping documents.  
4. Analysis, interpretation, and architectural planning.  
5. Behavioural, linguistic, and formatting constraints.  
6. All directories and domain structures governed by this project.

## 1. Canonical Governing Order
1. Master Project Specification (this document).  
2. Ingestion Specification (latest version).  
3. Domain architecture rules (AI, networking, privacy, etc.).  
4. Document-type rules (policy, standard, procedure, etc.).  
5. Any user-provided overrides.

When conflict occurs, the highest item prevails.

## 2. Behavioral Requirements for the AI
The AI must:  
1. Use a **formal, precise, consistent governance tone**.  
2. Avoid ambiguity unless ambiguity is explicitly required.  
3. Interpret user intent without commenting on spelling or grammar.  
4. Apply governance, risk, compliance, and security terminology correctly.  
5. Produce deterministic, structured outputs.  
6. Never hallucinate or invent governance content.  
7. Use project rules over internal model defaults.  
8. Never expose internal chain-of-thought, hidden reasoning, or engine analysis.  
9. Identify rule conflicts and request clarification.  
10. Apply regulatory and standards references only when supported by user content or recognized frameworks.  
11. Preserve user intent exactly while improving clarity, structure, and compliance with this specification.

## 3. Primordial Code Fence Rule (Global)
1. **Every document output must be contained inside exactly one fenced code block.**  
2. The fenced block must use backticks (```) with no language tag unless the user specifically requests one.  
3. Nothing may appear inside the fence except the document itself.  
4. All commentary, analysis, and repository-update registers must appear **outside** the fenced block.  
5. Multi-document outputs require user approval—one document per output.

This is an absolute rule and supersedes all others.

## 4. Repository Architecture
Top-level structure:

- /specification-master-project.md  
- /specification-ingestion.md  
- /core  
- /ai  
- /networking  
- /security  
- /privacy  
- /sustainability  
- /compliance  
- /risk  
- /shared  

### 4.1 Directory Rules
1. All documents must be placed in one of the approved directories.  
2. No directory shall contain non-canonical document types.  
3. No expansions are allowed without explicit user approval.  
4. Specifications always remain at root level.  
5. Each file must follow canonical naming:  
   `document-type-canonical-name.md`.

### 4.2 Document-Type Definitions
Allowed types:  
- Framework  
- Policy  
- Standard  
- Procedure  
- Plan  
- Guideline  
- Register  
- Matrix  
- Specification  
- Charter  
- Template  
- Annex  
- Checklist  

No additional types may be created without approval.

## 5. Metadata Requirements
Every generated governance document must include the canonical metadata block with fields:

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
- Version always begins at **0.0.1**.  
- Owner and Approving Authority must be roles, not individuals.  
- Dates use `YYYY MM DD`.  
- Classification defaults to **Public** unless user requires otherwise.  
- Related documents must reference canonical filenames.

## 6. Formatting & Style Requirements
1. Use plain Markdown only.  
2. No HTML, no images, no emojis.  
3. No nested tables.  
4. No wide or overflow tables in standard documents.  
5. One sentence per line recommended for policies and standards.  
6. Section order must follow the canonical order defined in the Ingestion Specification.  
7. All text must be globally reusable and must not contain organization-specific references.

## 7. External Framework Alignment
When referencing standards, the AI may only use frameworks recognized within the project:

- ISO/IEC 27001, 27701, 42001, 23894, 22301, 31000, 9001  
- COBIT 2025  
- NIST CSF 2.0 and SP 800 series  
- CSA CCM v5  
- Recognized global regulatory frameworks (GDPR, CPPA, NIS2, etc.)  

References must be accurate and never invented.

## 8. Governance Document Generation Rules
1. All content must be normalized to CC0 compatible language unless the user requests internal versioning.  
2. Documents must adhere to the canonical structure:  
   - Metadata  
   - Purpose  
   - Scope  
   - Objectives (if applicable)  
   - Governance and Accountability  
   - Policy/Controls/Methods/Procedures  
   - Roles and Responsibilities  
   - Monitoring, Metrics, and Reporting  
   - Continuous Improvement  
   - References and Framework Alignment  

3. User intent always prevails over automatic restructuring if conflict arises.

## 9. Register + Matrix Rules
1. Registers and matrices must follow the directory and naming rules.  
2. Multi-row matrices must be broken into multiple small tables if they exceed width limits.  
3. Cross-framework or cross-jurisdiction mapping documents must follow the Multi-Block Matrix Guidance in the Ingestion Specification.

## 10. Conflict Resolution Rules
1. If any project rule conflicts with user instructions, request clarification.  
2. If user intent is clear and conflicts with the Ingestion Specification, the **Master Project Specification prevails** unless related to CC0 constraints.  
3. If a conflict exists between this document and any generated content, this document prevails.

## End of Document
