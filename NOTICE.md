# Notice: External Reference Materials and Licence Boundaries

**Document Title:** Notice: External Reference Materials and Licence Boundaries\
**Document Type:** Policy\
**Version:** 1.6.4\
**Date:** 2026-10-27\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`README.md`](README.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SECURITY.md`](SECURITY.md), [`governance/specification-citation-verification.md`](governance/specification-citation-verification.md), [`governance/register-canonical-citations.md`](governance/register-canonical-citations.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material change to the external reference policy, an added external content source, or a licence posture change\
**Repository Path:** [`NOTICE.md`](NOTICE.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This notice defines how external standards, control frameworks, regulatory texts, questionnaires, guidance documents, metrics catalogues, implementation guides, and audit references are treated by this repository.

The repository content is released under **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**. That licence applies only to original repository content. It does not apply to external reference materials referenced by the library.

The library is built on a clear principle: **we do not copy external third-party content into the library's documents**, except the short, attributed quotation the exception below allows. We reference external standards, frameworks, and resources by name and identifier; we paraphrase publicly documented capabilities; we use external work as inspiration for original synthesis. We do not paste verbatim text, controls, or questionnaire items from standards, frameworks, or other third-party sources beyond that quotation: they are paraphrased with pinpoint citations. The principle governs the library's documents. Vendored third-party material outside them, including the Apache-2.0 rule snapshot in `guardrails/aiqt-rules/`, the vendored AIQT corpus-tool subset in `vendor/aiqt/`, the MIT-licensed rule overlays in `.claude/rules/external/`, the MIT-licensed skills in `.claude/skills/addyosmani-*/`, and the separately copyrighted CC BY-SA 4.0 skill in `.claude/skills/clean-language/` that the Attribution section records, is a separate carve-out that keeps its own licence.

The exception covers two kinds of source. A document may carry a short, attributed verbatim quotation of (a) a government or regulatory text (for example a statute, a regulation, or a government policy or directive) or (b) a standard or framework text that is in the public domain or openly licensed (for example a NIST SP or FIPS publication, the NIST CSF, or a framework under CC0 1.0, CC BY 4.0, or CC BY-SA 4.0), where the source licence permits quotation (for example an Open Government Licence whose only condition is attribution) and is compatible with CC BY-SA 4.0, as the licence lists in [`specification-ingestion.md`](specification-ingestion.md) decide. Standards and frameworks under other licences are paraphrased with pinpoint citations. Short means at most one provision or passage and at most 100 words per quotation, and no longer than what the document relies on. Only a translation that the government itself publishes counts as a government text. Any other translation, including one that a body other than the government publishes (for example the KLRI English translations of Korean statutes), is a third-party translation: it is quoted only under its own publisher's terms, where they permit quotation and are compatible with CC BY-SA 4.0, and is otherwise paraphrased. For a translation, the quoted text is the translation and its publisher is the body that publishes the translation, not the publisher of the original text, so its licence basis is the licence or public-domain status that the held translation or that publisher's terms state. The quoting document records the licence basis in a **Licence basis** statement, as the licence compatibility rules of [`specification-ingestion.md`](specification-ingestion.md) define. Quoted text keeps its source licence and is not relicensed under CC BY-SA 4.0.

**Transition.** Quotations merged to `main` before the maintainer decision of 2026-10-24 23:52Z, and the quotations committed before that decision on branch `content/3b546-osfi`, which the decision lets merge, stay as they are until the publisher's terms are held, whatever their held text shows about their licence, their length, or their source type. Each covered document is to carry a Licence basis statement saying that the transition clause covers it; a tracked follow-up adds those statements. The publisher's terms are held once, after that decision, the publisher's licence or terms of use for the quoted text are acquired into the reference base that holds the library's source texts. For a translation, the publisher and the quoted text are those the exception above names: the body that publishes the translation, and the translation. For a text that its publisher places in the public domain, which leaves no licence to acquire, the terms are the publisher's own statement of that status (for example its copyright or reuse notice). For a text that is in the public domain by statute or by expiry of its copyright term, and whose publisher makes no statement of that status, the terms are held at the covered document's first scheduled review after that decision; its Licence basis then names that status, with the statute or the expiry it rests on, only where the reference base holds them, and otherwise names none. A licence, copyright, or public-domain statement that the held text already carried at the decision does not end the transition. That one event ends the transition on every ground at once (the licence, the length, and a third-party translation or other source type), and the covered document's Licence basis statement then records the date the terms were held and the licence or public-domain status they state: the rule for a new quotation then applies, so the quotation stays only if it meets the exception above and is otherwise paraphrased with pinpoint citations. A quotation of a public-domain text that is longer than 100 words therefore stays until the transition ends for it, and is then cut to a quotation the exception above allows or paraphrased with pinpoint citations. Editing a covered quotation makes it a new quotation, which must meet the exception above.

---

## What the library does

External materials are used for:

- Non-verbatim analysis and original synthesis.
- The short, attributed verbatim quotation that the exception above allows or its transition clause keeps.
- High-level alignment ("this document aligns to ISO/IEC 27001:2022 Annex A.5").
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
- Tables reconstructed from proprietary or otherwise restricted source materials.
- Copyright notices removed from external materials.

These prohibitions apply to every third-party source beyond the short, attributed quotation the exception above allows or its transition clause keeps, and to every part of the repository except the vendored third-party material that this notice records as a separate carve-out, which keeps its own licence and its upstream copyright and licence notices. They exist because the library's content is original synthesis, not aggregation.

---

## Permitted reference patterns

| Pattern | Example |
| --- | --- |
| Framework identifier | Map a document to CSA CCM, ISO/IEC 27001:2022, NIST CSF 2.0, or NIST AI RMF 1.0 at a domain level. |
| Control family | Reference identity, logging, data security, supplier governance, incident management, or resilience as control families. |
| Original requirement | Write a new control requirement using original wording and role-neutral language. |
| Applicability note | State that a document may be relevant where cloud services, AI systems, personal data, regulated operations, or critical services exist. |
| Evidence category | Reference evidence classes such as policy approval, risk register entry, test result, access review, incident record, model card, or supplier assessment. |

---

## Attribution

The library is released under **CC BY-SA 4.0**, which requires attribution of the library when content is redistributed (in original or modified form). Its "ShareAlike" condition requires an adopter who shares an adaptation to license their own contributions to it under CC BY-SA 4.0, a later CC BY-SA version, or a BY-SA-compatible licence. The library's own text stays under CC BY-SA 4.0; quoted or vendored third-party material keeps its own terms, as this notice records.

GRC-original material retains CC BY-SA 4.0. The upstream-owned pinned snapshot in `guardrails/aiqt-rules/` and its local rule derivatives are separately licensed Apache-2.0; retain the verbatim upstream LICENSE and NOTICE in that directory. GRC owns its compatibility rule and the retained legacy procedures. Authority: maintainer decisions D1-D3, 2026-10-02 12:27Z. The minimal subset of the upstream AIQT guardrails pack vendored in `vendor/aiqt/` (the generic corpus-tool module `tools/aiqt_corpus.py`, its digest pin `PIN.toml`, and `RULES.json`, the inventory of the rule snapshot above) keeps its upstream licence; `RULES.json` records that rule snapshot as Apache-2.0, and the directory's own files state no separate licence for the module, so none is named for it here. The third-party rule overlays vendored in `.claude/rules/external/kariedo/` and `.claude/rules/external/tikitribe/` keep their upstream MIT licence, held in the LICENSE file in each directory. The five third-party skills vendored in `.claude/skills/addyosmani-*/` (ci-cd-and-automation, code-review-and-quality, context-engineering, security-and-hardening, and using-agent-skills, from addyosmani) keep their upstream MIT licence, held in the LICENSE file in each skill directory beside its PROVENANCE.md. The Clean Language skill vendored in `.claude/skills/clean-language/` keeps its upstream CC BY-SA 4.0 licence under its own upstream copyright and attribution, which are not folded into the library's, held in the LICENSE and NOTICE.md files in that directory beside its PROVENANCE.md.

See [`CITATION.cff`](CITATION.cff) for machine-readable citation metadata and [`AUTHORS.md`](AUTHORS.md) for the author's attribution preference.

External references should be expressed as framework families or public identifiers, not copied text, other than a quotation the exception above allows or its transition clause keeps. Examples include:

- ISO management system and risk standards.
- NIST cybersecurity, privacy, artificial intelligence, identity, and zero trust publications.
- COBIT governance and management concepts.
- Cloud control and cloud assurance framework families.
- Artificial intelligence control and assurance framework families.
- OWASP LLM risk categories.
- MITRE ATLAS tactics and techniques.
- Regional legal and regulatory regimes.

---

## Personal and organization data exclusion

Repository content must not include:

- Real company names.
- Real personal names.
- Internal titles tied to a specific organization.
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

Roles must be generic, such as Chief Information Officer, Chief Information Security Officer, Data Protection Officer, Chief Compliance Officer, Chief Risk Officer, System Owner, Data Owner, Control Owner, and Process Owner.

---

## Notes for adopters bringing in external content

Adopters using the library may choose to incorporate external content (rule sets, frameworks, tools) from other sources into their own projects on top of the library. When they do so, they are responsible for verifying that the external content's licence is compatible with their use, and for complying with any attribution, share-alike, non-commercial, or no-derivatives restrictions those external sources impose. The library's CC BY-SA 4.0 covers the library content only; it does not relicense anything an adopter brings in from elsewhere.

The setup generator at [`guardrails/setup-generator-prompt.md`](guardrails/setup-generator-prompt.md) surfaces the licence of each external rule source it offers (TikiTribe, Kariedo, addyosmani, Wiz) so the adopter can make an informed decision.

---

## Review requirement

This notice should be reviewed when new external reference materials are introduced into the library and during annual repository review. AI, cloud assurance, and regulatory reference materials should be rechecked on a 6 to 12 month cadence because source versions, licence terms, and assurance programme rules can change.

---

**End of Document**
