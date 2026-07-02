# Contributing to the GRC Documentation Library

**Document Title:** Contributing to the GRC Documentation Library\
**Document Type:** Guideline\
**Version:** 1.2.2\
**Date:** 2026-07-02\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`README.md`](README.md), [`specification-master-project.md`](specification-master-project.md), [`specification-ingestion.md`](specification-ingestion.md), [`SECURITY.md`](SECURITY.md), [`NOTICE.md`](NOTICE.md), [`AUTHORS.md`](AUTHORS.md), [`CHANGELOG.md`](CHANGELOG.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material change to the contribution workflow, audit programme, or licence posture\
**Repository Path:** [`CONTRIBUTING.md`](CONTRIBUTING.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

Thank you for considering a contribution. This library is released under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0). By submitting a contribution, you license your contribution to the library and downstream adopters under the same CC BY-SA 4.0 terms (see Licence section below for full details). Before submitting a change, please read the two governing specifications:

- [`specification-master-project.md`](specification-master-project.md): document model, type vocabulary, metadata block, formatting rules.
- [`specification-ingestion.md`](specification-ingestion.md): how new content is ingested, licence-compatibility checks, sanitization substitution table, filename rules.

## AI-assisted authorship

A substantial portion of this library was authored with AI assistance and then reviewed and edited by humans. AI assistance is acceptable for contributions provided that:

- The contributor remains accountable for the content as if they wrote it directly.
- Framework citations (ISO, NIST, OWASP, COBIT, CSA, regulatory references, etc.) are verified against primary sources before submission. The [`tools/lint-citations.py`](tools/lint-citations.py) denylist prevents reintroduction of known hallucinations but is not a substitute for verification of new citations.
- The contribution remains organization-neutral and free of sanitization residue.
- The contribution passes the local audit suite (see Workflow below).

This statement is informational; contributors are not required to declare whether AI assisted their authorship.

## What contributions are welcome

- New original artefacts that fit one of the governance domains and one of the allowed document types (see [`specification-master-project.md`](specification-master-project.md) §4 for the canonical lists).
- Corrections to existing artefacts (clarity, accuracy, framework alignment, broken links).
- Translations are not currently accepted; the library is English-only.
- New tooling, audit scripts, and CI improvements that align with the existing tooling pattern (Python 3 stdlib, no third-party dependencies).
- New pack rules under [`dev-security/claude-rules/`](dev-security/claude-rules/) and new Claude Code Skills under [`dev-security/claude-rules/skills/`](dev-security/claude-rules/skills/), where the rule or skill is grounded in a real failure mode observed while maintaining a governed codebase. Per the existing pack discipline, each new governance rule must cite the maintenance event that justified it (a dated CHANGELOG entry or a documented session incident); each skill must derive from a canonical pack rule via its `derives_from` frontmatter field, enforced by [`tools/lint-skill-derives-from.py`](tools/lint-skill-derives-from.py). See [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md) for the pack's contribution conventions and version-bump rules.

The most common net-new artefact is an overlay for a sector or jurisdiction the library does not yet cover. Author it by mirroring an existing same-type annex rather than inventing a structure: for a new jurisdiction, follow a privacy jurisdiction annex in [`privacy/jurisdictions/`](privacy/jurisdictions/) (for example [`privacy/jurisdictions/annex-privacy-european-union.md`](privacy/jurisdictions/annex-privacy-european-union.md)); for a new sector, follow an existing sector annex such as [`compliance/telecommunications/annex-telecommunications-sector-requirements.md`](compliance/telecommunications/annex-telecommunications-sector-requirements.md) or [`compliance/public-sector/annex-fedramp-requirements.md`](compliance/public-sector/annex-fedramp-requirements.md). Keep the metadata block, section model, and filename rules below; the audit programme enforces them.

## What contributions are not welcome

- Verbatim third-party control text, questionnaire text, audit guidance text, or metrics catalogue text whose source licence restricts modification or redistribution. See [`NOTICE.md`](NOTICE.md).
- Organization-specific identifiers (company names, personal names, tenant identifiers, internal system names, incident details, IP addresses, contract numbers, email addresses, phone numbers).
- Translations of existing English artefacts.
- Marketing language, certification claims, or statements implying that adopting the library makes an organization compliant with any regulation.

## Workflow

1. **Open an issue first** if the change is non-trivial (a new document, a new section, a structural change to the index). Use the issue to agree the scope before authoring.
2. **Fork or branch.** Develop your change on a feature branch named after the work, for example `add-fedramp-annex` or `fix-sop-references`.
3. **Run the local audits before committing.** All must pass.

   ```
   tools/run_all_audits.sh
   ```

   The script runs the full audit programme (every gate listed in [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) §6) in the same order as CI. `FAIL_FAST=1 tools/run_all_audits.sh` stops on first failure.

   Optionally install pre-commit to run the audit programme automatically on every commit:

   ```
   pip install pre-commit
   pre-commit install
   ```

4. **Update the index and domain README.** Every new active document must appear in [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md) and in its domain's [`README.md`](README.md) Active Documents table.
5. **Bump versions appropriately.** Patch (`x.y.z` increments the patch segment) for minor corrections; minor (`x.y.0`) for substantive content additions or structural changes; major (`x.0.0`) for breaking structural or material policy revisions. See [`specification-ingestion.md`](specification-ingestion.md) Version numbering.
6. **Open a pull request.** Reference the issue. Describe what changed and why. Note any version flags raised. List any new external framework references.
7. **CI must pass.** The same audit programme runs in GitHub Actions.

## Reporting content issues without contributing a fix

Readers who notice issues but do not want to submit a code change can report content concerns by opening an issue on the repository. Useful issue categories include:

| Category | Examples |
| --- | --- |
| Factual error | A framework citation is incorrect; a control identifier doesn't exist; a regulatory reference is stale or wrong. |
| Cross-document inconsistency | Two documents disagree about the same control, responsibility, or threshold. |
| Sanitization residue | A document contains a real company name, internal hostname, real IP address, customer or vendor name, or other identifying detail. |
| Ambiguous responsibility | The library assigns a responsibility without naming a clear role, or two roles overlap in a way that creates confusion. |
| Unsafe guidance | Guidance that, if followed literally, could create a security or operational hazard. |
| Operational unrealism | A control or procedure that is not realistically executable. |

For security-related defects (licence concerns, security flaws in code samples, leakage of organizational identifiers), use the path in [`SECURITY.md`](SECURITY.md) instead.

## Metadata block

Every document begins with the canonical 13-field metadata block. The example below shows the canonical order, format, and link syntax for `Repository Path` and `Related Documents`:

```
# Document Title

**Document Title:** Document Title\
**Document Type:** Policy\
**Version:** X.Y.Z\
**Date:** YYYY-MM-DD\
**Owner:** Role Name\
**Approving Authority:** Role Name\
**Related Documents:** [`domain/related.md`](relative-path/related.md), [`other-domain/other.md`](../other-domain/other.md)\
**Classification:** Public\
**Category:** Domain Name\
**Review Frequency:** Annual and upon material change\
**Repository Path:** [`domain/file-name.md`](file-name.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0 
```

Each value line ends with a trailing space and the line break is two spaces or a `\n` that Markdown renders as a soft break. Owner and Approving Authority must be role-based (no individual names).

## Style requirements

- **Language convention: Canadian English first, Commonwealth (UK / Australian) second, other dialects last.** Canadian English shares its `-ize` / `-ization` orthography with American English (the Oxford convention adopted in Canadian usage), so the linter-enforced `-ize` rule is the Canadian-orthography manifestation of the convention, not a generic American mandate. Where Canadian English has no opinion (vocabulary or grammar features that vary across other English dialects), Commonwealth forms are preferred; where neither has an opinion, other dialects' usage is acceptable.
- Use `-ize` forms (e.g. organize, prioritize, recognize) per the Canadian-orthography rule above.
- Pair `ensure` with `that` (e.g. "ensure that all logs are retained" rather than "ensure all logs are retained").
- No em dashes or en dashes; use commas, colons, or parentheses.
- Use sentence case for H2 to H6 headings; first word capitalized, subsequent words lowercase except proper nouns and acronyms. Section identifiers like `A1.`, `Step 1:`, and `Category 1:` count as numbering, so the word that follows must be capitalized.
- Document titles in H1 may use Title Case where they name a controlled artefact.

## Filename rules

- Lowercase letters and single hyphens between words only.
- Filename must start with the document type prefix (`charter-`, `framework-`, `policy-`, `standard-`, `procedure-`, `sop-`, `plan-`, `roadmap-`, `guideline-`, `guide-`, `register-`, `matrix-`, `specification-`, `template-`, `annex-`, `checklist-`).
- No vendor or product names in filenames.

## Review

A maintainer reviews each pull request for licence compliance (original authorship; no externally-licensed verbatim text), organization neutrality, accuracy of external framework references, and conformance to the specifications. Changes that touch core artefacts (charter, document architecture framework, document index register) or that introduce a new domain folder require explicit user approval beyond the standard review.

## Licence

By submitting a contribution to this repository, you license your contribution to the library and to all downstream recipients under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). You retain copyright in your contribution; the licence grants the library and downstream adopters the right to use, modify, and redistribute it under the same CC BY-SA 4.0 terms ("inbound = outbound").

Contributions must be your own original work, or work for which you have the right to grant a CC BY-SA 4.0 licence. Do not contribute material whose original licence is incompatible with CC BY-SA 4.0 (for example: CC BY-NC, CC BY-ND, CC BY-NC-ND, or proprietary content). If you cannot grant a CC BY-SA 4.0 licence to the material you are submitting, do not submit it.
