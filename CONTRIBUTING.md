# Contributing to the GRC Documentation Library

Thank you for considering a contribution. This library is released under CC0 1.0 Universal, which means every contribution is dedicated to the public domain. Before submitting a change, please read the two governing specifications:

- [`specification-master-project.md`](specification-master-project.md): document model, type vocabulary, metadata block, formatting rules.
- [`specification-ingestion.md`](specification-ingestion.md): how new content is ingested, CC0 compatibility checks, sanitisation substitution table, filename rules.

## What contributions are welcome

- New original CC0 artefacts that fit one of the ten governance domains and one of the sixteen allowed document types.
- Corrections to existing artefacts (clarity, accuracy, framework alignment, broken links).
- Translations are not currently accepted; the library is English-only.
- New tooling, audit scripts, and CI improvements that align with the existing tooling pattern (Python 3 stdlib, no third-party dependencies).

## What contributions are not welcome

- Verbatim third-party control text, questionnaire text, audit guidance text, or metrics catalogue text whose source license restricts modification or redistribution. See [`NOTICE.md`](NOTICE.md).
- Organisation-specific identifiers (company names, personal names, tenant identifiers, internal system names, incident details, IP addresses, contract numbers, email addresses, phone numbers).
- Translations of existing English artefacts.
- Marketing language, certification claims, or statements implying that adopting the library makes an organisation compliant with any regulation.

## Workflow

1. **Open an issue first** if the change is non-trivial (a new document, a new section, a structural change to the index). Use the issue to agree the scope before authoring.
2. **Fork or branch.** Develop your change on a feature branch named after the work, for example `add-fedramp-annex` or `fix-sop-references`.
3. **Run the local audits before committing.** All four must pass.

   ```
   python3 tools/lint-metadata.py
   python3 tools/lint-language.py
   python3 tools/lint-links.py
   python3 tools/lint-structure.py
   ```

   Optionally install pre-commit to run the audits automatically:

   ```
   pip install pre-commit
   pre-commit install
   ```

4. **Update the index and domain README.** Every new active document must appear in `governance/register-document-index-and-classification.md` and in its domain's `README.md` Active Documents table.
5. **Bump versions appropriately.** Patch (`x.y.z` increments the patch segment) for minor corrections; minor (`x.y.0`) for substantive content additions or structural changes; major (`x.0.0`) for breaking structural or material policy revisions. See [`specification-ingestion.md`](specification-ingestion.md) Version numbering.
6. **Open a pull request.** Reference the issue. Describe what changed and why. Note any version flags raised. List any new external framework references.
7. **CI must pass.** The same four audits run in GitHub Actions.

## Metadata block

Every document begins with the canonical 13-field metadata block. The example below shows the canonical order, format, and link syntax for `Repository Path` and `Related Documents`:

```
# Document Title

**Document Title:** Document Title 
**Document Type:** Policy 
**Version:** 0.0.1 
**Date:** YYYY-MM-DD 
**Owner:** Role Name 
**Approving Authority:** Role Name 
**Related Documents:** [`domain/related.md`](relative-path/related.md), [`other-domain/other.md`](../other-domain/other.md) 
**Classification:** Public 
**Category:** Domain Name 
**Review Frequency:** Annual and upon material change 
**Repository Path:** [`domain/file-name.md`](file-name.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 
```

Each value line ends with a trailing space and the line break is two spaces or a `\n` that Markdown renders as a soft break. Owner and Approving Authority must be role-based (no individual names).

## Style requirements

- Use Oxford English with `-ize` forms (e.g. organize, prioritize, recognize).
- Pair `ensure` with `that` (e.g. "ensure that all logs are retained" rather than "ensure all logs are retained").
- No em dashes or en dashes.
- Use sentence case for H2 to H6 headings; first word capitalised, subsequent words lowercase except proper nouns and acronyms. Section identifiers like `A1.`, `Step 1:`, and `Category 1:` count as numbering, so the word that follows must be capitalised.
- Document titles in H1 may use Title Case where they name a controlled artefact.

## Filename rules

- Lowercase letters and single hyphens between words only.
- Filename must start with the document type prefix (`charter-`, `framework-`, `policy-`, `standard-`, `procedure-`, `sop-`, `plan-`, `roadmap-`, `guideline-`, `guide-`, `register-`, `matrix-`, `specification-`, `template-`, `annex-`, `checklist-`).
- No vendor or product names in filenames.

## Review

A maintainer reviews each pull request for CC0 compatibility, organisation neutrality, accuracy of external framework references, and conformance to the specifications. Changes that touch core artefacts (charter, document architecture framework, document index register) or that introduce a new domain folder require explicit user approval beyond the standard review.

## License

By submitting a contribution, you dedicate it to the public domain under [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/). If you cannot make that dedication for the material you are submitting, do not submit it.
