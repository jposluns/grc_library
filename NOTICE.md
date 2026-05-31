# Notice: External Reference Materials and Licence Boundaries

**Version:** 1.2.0\
**Date:** 2026-05-31\
**Classification:** Public\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0 for original repository content only

---

## Purpose

This notice defines how external standards, control frameworks, regulatory texts, questionnaires, guidance documents, metrics catalogues, implementation guides, and audit references are treated by this repository.

The repository content is released under **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**. That licence applies only to original repository content. It does not apply to external reference materials referenced by the library.

The library is built on a clear principle: **we do not copy externally licensed content into this repository.** We reference external standards, frameworks, and resources by name and identifier; we paraphrase publicly documented capabilities; we use external work as inspiration for original synthesis. We do not paste verbatim text, controls, or questionnaire items from licensed third-party sources.

---

## What the library does

External materials are used for:

- Non-verbatim analysis and original synthesis.
- High-level alignment ("this document aligns to ISO 27001 A.5").
- Framework name and identifier reference.
- Control family or domain-level mapping.
- Applicability assessment structure.
- Commentary describing governance intent, risk context, and implementation considerations in the library's own words.

## What the library does not do (and what contributors must not commit)

Do not commit any of the following:

- Verbatim control statements from third-party frameworks.
- Verbatim questionnaire questions or answer options.
- Full or partial third-party implementation guidance text.
- Full or partial third-party audit guidance text.
- Full or partial third-party metrics catalogue text.
- Tables reconstructed from proprietary or restrictively licensed source materials.
- Copyright notices removed from external materials.

These prohibitions apply regardless of any external material's licence terms. They exist because the library's content is original synthesis, not aggregation.

---

## Permitted reference patterns

| Pattern | Example |
| --- | --- |
| Framework identifier | Map a document to CSA CCM, ISO 27001, NIST CSF, or NIST AI RMF at a domain level. |
| Control family | Reference identity, logging, data security, supplier governance, incident management, or resilience as control families. |
| Original requirement | Write a new control requirement using original wording and role-neutral language. |
| Applicability note | State that a document may be relevant where cloud services, AI systems, personal data, regulated operations, or critical services exist. |
| Evidence category | Reference evidence classes such as policy approval, risk register entry, test result, access review, incident record, model card, or supplier assessment. |

---

## Attribution

The library is released under **CC BY-SA 4.0**, which requires attribution of the library when content is redistributed (in original or modified form). The licence requires that derivatives be released under CC BY-SA 4.0 as well (the "ShareAlike" condition).

See [`CITATION.cff`](CITATION.cff) for machine-readable citation metadata and [`AUTHORS.md`](AUTHORS.md) for the author's attribution preference.

External references should be expressed as framework families or public identifiers, not copied text. Examples include:

- ISO management system and risk standards.
- NIST cybersecurity, privacy, artificial intelligence, identity, and zero trust publications.
- COBIT governance and management concepts.
- Cloud control and cloud assurance framework families.
- Artificial intelligence control and assurance framework families.
- OWASP LLM risk categories.
- MITRE ATLAS tactics and techniques.
- Regional legal and regulatory regimes.

---

## Personal and organisation data exclusion

Repository content must not include:

- Real company names.
- Real personal names.
- Internal titles tied to a specific organisation.
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
- Incident details.
- Audit evidence.
- Screenshots or exports from internal systems.

Roles must be generic, such as Chief Information Officer, Chief Information Security Officer, Chief Privacy Officer, Chief Compliance Officer, Chief Risk Officer, System Owner, Data Owner, Control Owner, and Process Owner.

---

## Notes for adopters bringing in external content

Adopters using the library may choose to incorporate external content (rule sets, frameworks, tools) from other sources into their own projects on top of the library. When they do so, they are responsible for verifying that the external content's licence is compatible with their use, and for complying with any attribution, share-alike, non-commercial, or no-derivatives restrictions those external sources impose. The library's CC BY-SA 4.0 covers the library content only; it does not relicense anything an adopter brings in from elsewhere.

The setup generator at [`dev-security/claude-rules/setup-generator-prompt.md`](dev-security/claude-rules/setup-generator-prompt.md) surfaces the licence of each external rule source it offers (TikiTribe, Wiz, Kariedo) so the adopter can make an informed decision.

---

## Review requirement

This notice should be reviewed when new external reference materials are introduced into the library and during annual repository review. AI, cloud assurance, and regulatory reference materials should be rechecked on a 6 to 12 month cadence because source versions, licence terms, and assurance programme rules can change.

---

**End of Document**
