# Executive Narrative Authoring Specification

**Document Title:** Executive Narrative Authoring Specification\
**Document Type:** Specification\
**Version:** 0.0.9\
**Date:** 2026-08-07\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`specification-master-project.md`](specification-master-project.md), [`specification-ingestion.md`](specification-ingestion.md), [`README.md`](README.md), [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material change to the narrative layer, its metadata model, its subtype set, or its gate wiring\
**Repository Path:** [`specification-executive-narrative.md`](specification-executive-narrative.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This specification defines how executive narrative pages are authored, classified, gated, and kept current. It is the contract every narrative page conforms to.

The executive narrative layer translates the governance corpus for a governing-body reader. A narrative page explains what the corpus establishes, walks a scenario through the corpus controls, frames a leadership decision, or equips oversight questioning. It never adds to the corpus, restates the corpus as its own authority, or substitutes for the corpus. The corpus documents remain the sole normative surface, and every narrative page is subordinate to the corpus sources it references.

This specification establishes rules for:

- Where narrative pages live and which audit scopes apply to them.
- The single narrative document class and its seven subtypes.
- The metadata block, including the narrative extension fields.
- The narrative status vocabulary and the universal authority disclaimer.
- Claim classes and the causal vocabulary.
- Mandatory sections and the per-subtype section schemas.
- Corpus source references and the advisory executive-review cadence.
- Release, retirement, and the generated narrative registry.

The narrative gate family that mechanically enforces the rules below is built in later phases; the gate intent is recorded in the Gates section. Where a rule is enforced only by review rather than mechanically, this specification says so.

---

## Scope

This specification applies to every file under the top-level `executive/` directory, and to any content anywhere in the repository that carries the `Executive Narrative` document type or a narrative-extension metadata field.

It operates under the Master Project Specification and, for language, organization-neutrality, and licence rules, inherits the Ingestion and Transformation Specification in full, except where the narrative layer deliberately differs (see the language and neutrality section). Where this specification is silent, the ingestion specification applies. Where the two conflict, the more restrictive rule prevails.

---

## Placement and audit scope

Narrative pages live under the top-level `executive/` directory, each in the subdirectory for its subtype (`briefs/`, `scenarios/`, `decision-narratives/`, `oversight-question-sets/`, `stories/`, `journeys/`, `outcome-maps/`). `executive/` is not a corpus domain, and its boundary with the corpus is mechanical, not conventional.

1. **Structural exclusion (domain-list and generator surfaces).** `executive` is not a member of the audited-domain run (`AUDITED_DOMAIN_DIRS`) or of the taxonomy generator's `DOMAINS` list. Its exclusion from the taxonomy, the portal, the maturity scorecard, and every splatting content linter is structural: those walks are restricted to their own lists and never reach `executive/`. This follows the `.project-governance` and `docs/` precedents for structural exclusion.
2. **Active exclusion (corpus-model root-walkers).** Some corpus-model gates walk the repository root rather than a fixed list. Each such gate reaches `executive/` by default and must exclude it explicitly by treating the narrative directory as a root-anchored exclusion. This is a distinct mechanism from item 1: it is an active exclusion the gate performs, not a walk that never arrives. The authoritative, regression-checked classification of which gates exclude structurally, exclude actively, or deliberately include `executive/` is the gate-scope manifest.
3. **Deliberate inclusion (safety and reference-integrity).** `executive/` remains fully inside the cross-cutting safety and reference-integrity gates. The secrets, PII, and external-link-domain gates walk the repository root and cover `executive/` with no additional wiring; `executive/` must never be added to any exempt-directory set, and the narrative-directory set must never be folded into the shared default exemptions. The link-integrity gate enumerates explicit scan roots and carries `executive` as an explicit root.
4. **Listing surface and the entry-point exemption.** The structural auditor exempts `executive/` from the corpus listing surfaces (domain READMEs and the document index register). The narrative layer keeps its own listing surface: a hand-curated concern framing in `executive/README.md` and a generated artefact listing derived from the narrative registry. `executive/README.md` is the layer's entry point, NOT a narrative page: it is a single named, path-scoped exemption from the narrative-page requirements (it does NOT carry the `Executive Narrative` type or the narrative-extension block, and it is not a narrative registry row). This one exemption is applied CONSISTENTLY across every narrative gate that would otherwise require narrative-page form: the symmetric boundary gate, the narrative metadata gate, the disclaimer-presence gate, the registry/completeness gate, and the listing gate all name `executive/README.md` as the sole exempt entry point.

A narrative page found anywhere outside `executive/` is a defect, and the containment is deliberate and loud. The corpus metadata gate is a corpus-structural gate whose scan roots (by-name root files, `docs/`, and the audited-domain run) do not reach `executive/`, so a correctly placed narrative page is simply outside that gate. If a narrative file leaks into a scanned corpus location, that gate fails loudly on the invalid Document Type, because `Executive Narrative` is not a member of the allowed corpus document types and because the filename-prefix check runs only for known types and is therefore skipped for an unknown type. An ordinary unchanged copy (rather than a move) also trips the Repository-Path check (its `Repository Path` still points into `executive/`), so that leak surfaces two failures. This residual containment is NOT complete, and the spec does not claim it is: two escapes are known and are covered by the future symmetric narrative-boundary gate (Gates item 3) and by review, not by the existing corpus metadata gate. First, a page named `README.md` placed in a corpus subdirectory is treated by the metadata gate as a domain README (a loose check of Document Title and License only), so its invalid Document Type is never examined. Second, a page retyped to a valid corpus Document Type and renamed to match, while retaining narrative-extension fields, passes the metadata gate because that gate does not reject unknown narrative-extension fields. The load-bearing properties of the EXISTING residual are therefore narrow: for an unchanged, non-README copy leak the invalid-type failure fires and cannot be silenced except by adding the type or by taking one of the two escapes above; closing the escapes is the symmetric boundary gate's job. The full symmetric boundary (rejecting narrative types or narrative-extension fields anywhere outside `executive/`, and requiring them on every page inside `executive/`) is a narrative-gate-family obligation described under Gates; the single-failure behaviour above is the residual containment that already exists in the corpus metadata gate.

Keeping `Executive Narrative` out of the allowed corpus document types permanently is the whole of that residual mechanism. No one may ever resolve the failure by adding the type.

---

## Document class and subtypes

There is exactly one narrative document type: `Executive Narrative`. Subclassification is carried by the `Narrative Type` metadata field, never by the Document Type field. The closed set of subtypes, their mandatory filename prefixes and subdirectories, and their fixed narrative status:

| Narrative Type | Filename prefix | Subdirectory | Narrative Status |
|---|---|---|---|
| Executive Brief | `brief-` | `briefs/` | Explanatory |
| Scenario | `scenario-` | `scenarios/` | Non-normative |
| Decision Narrative | `decision-` | `decision-narratives/` | Advisory |
| Oversight Question Set | `oversight-questions-` | `oversight-question-sets/` | Advisory |
| Story | `story-` | `stories/` | Non-normative |
| Journey | `journey-` | `journeys/` | Explanatory |
| Outcome Map | `outcome-map-` | `outcome-maps/` | Explanatory |

Filename rules follow the ingestion specification (lowercase, single hyphens, no punctuation, no organization-specific names), with the subtype prefix in place of a document-type prefix. Each page lives in its subtype's subdirectory under `executive/` per the table; the prefix and the subdirectory must both match the `Narrative Type` field exactly.

No other subtype may be introduced without a version bump to this specification and corresponding gate changes. A page that fits no subtype is a signal that it does not belong in the narrative layer.

---

## Canonical metadata and narrative extension

Every narrative page begins with the corpus's 13 canonical metadata fields, in canonical order, followed immediately by the 8-field narrative extension, as one continuous metadata block using the backslash hard-break convention (every line except the block's last line ends with `\`).

```markdown
# Page Title

**Document Title:** Page Title\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** YYYY-MM-DD\
**Owner:** Role Name\
**Approving Authority:** Role Name\
**Related Documents:** [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/decision-narratives/decision-ai-risk-appetite.md`](decision-ai-risk-appetite.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Decision Narrative\
**Narrative Status:** Advisory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md), [`supply-chain/register-concentration-risk.md`](../../supply-chain/register-concentration-risk.md)\
**External Sources:** ISO 31000, NIST CSF (or: None)\
**Claim Classes Present:** citation, sourced, composite\
**Review Record:** NR-YYYY-NNN\
**Last Reviewed:** YYYY-MM-DD
```

The eight extension fields:

1. **Narrative Type:** one of the seven subtypes, matching the filename prefix.
2. **Narrative Status:** one of `Non-normative`, `Advisory`, `Explanatory` (closed set; see the narrative status section). The value is fixed by the subtype table, not chosen by the author.
3. **Audience:** the entity-neutral audience phrase. The canonical value is `Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)`. A page may narrow it (for example to an audit-committee reader) but never names a specific organization's body and never presumes a specific governance model.
4. **Corpus Sources:** the corpus source list. Each entry is a plain markdown link to the corpus document (a path reference, no version suffix). Every corpus document the page relies on for any claim must be listed here; a corpus link in the body absent from this field is a defect. At least one entry is mandatory. Exactly one entry per distinct corpus dependency (no duplicate references to the same target). The list records dependency PATHS only: an executive page refers to corpus documents but never depends on their VERSIONS, so a corpus version bump never invalidates a narrative page.
5. **External Sources:** the named public standards, frameworks, or regulations the page's `sourced` claims rest on, drawn only from the ingestion specification's preserve-without-substitution list, or `None`.
6. **Claim Classes Present:** the subset of `citation`, `sourced`, `composite` that appears on the page.
7. **Review Record:** the identifier of the page's review record, which holds the full per-claim matrices (see the claim classes section). This is an identifier, not a repository path, so a public page never links into a private record store. Review records are project-governance operational records; they live in the maintainer's private working store, not in the published corpus.
8. **Last Reviewed:** ISO 8601 date of the most recent human review of the page. The executive-review cadence is a 6-month advisory (an editorial freshness signal), not a gated CI requirement and not a revalidation against source versions.

The `Approving Authority` field is retained from the canonical model, but on a narrative page it denotes publication approval only. It confers no normative authority, and the page states as much through the universal disclaimer: a narrative page is never a parent of, or an authority over, any corpus document.

The extension is appended inside the single header block after `License`, so on a narrative page `License` carries a trailing backslash and `Last Reviewed` is the block's bare last line. This is consistent with the line-break convention, which requires a trailing `\` on every metadata line except the run's last line and exempts the last line generically; the convention names no specific field as last. The narrative metadata gate validates the extension fields and their closed vocabularies, and (because the shared line-break gate does not scan `executive/`) it owns the backslash hard-break validation for narrative pages; the extended block needs no change to the shared checker's generic last-line logic, only coverage of `executive/` by the new gate.

Derived or computed classification (topic tags, domain coverage, audience facets) never appears in the header and never appears in `taxonomy.yml`; it lives only in the generated narrative registry.

All other metadata conventions follow the ingestion specification: role names only, ISO 8601 dates, markdown-linked paths, and the corpus version-numbering scheme (new pages begin at `0.0.1`; `1.0.0` on first formal approval and publication).

---

## Narrative status and the authority disclaimer

`Narrative Status` is a closed three-value vocabulary describing what kind of reliance a reader may place on the page. It is fixed per subtype (see the document class table); an author never chooses it independently.

- **Non-normative.** The page is illustrative. It depicts events, settings, or narratives that establish nothing and recommend no decision, outcome, or control selection (a page's evidence-to-request section still equips an oversight action, which is not a recommendation). Scenarios and Stories are Non-normative: they make corpus controls legible in motion. Every scenario and story is composite and illustrative, describes no identifiable organization or actual incident, and makes no likelihood or frequency claim.
- **Advisory.** The page frames choices or questions for the reader to act on, without prescribing the outcome. Decision Narratives and Oversight Question Sets are Advisory: they organize a decision or a line of questioning, and the decision itself remains entirely with the reader's organization.
- **Explanatory.** The page restates, in executive language, what the corpus sources establish, and claims nothing beyond them. Executive Briefs, Journeys, and Outcome Maps are Explanatory: their value is faithful translation, and any statement in them that cannot be traced to a corpus source is a defect.

Every narrative page carries the universal authority disclaimer, verbatim, as the first body content after the metadata block's closing `---` separator and before the first section heading:

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

The DECIDED clause is `does not establish requirements; the linked corpus governs`; the surrounding wording above completes it and is fixed by this specification. The disclaimer is universal and identical on every page. Subtype-specific cautions (a scenario's no-likelihood-claim statement, or a caution that a cited legal regime changes without notice) belong in the page's limitations section, never in a modified disclaimer. The disclaimer text is a string-level property the gate proves; the absence of authority confusion in the reader is a review outcome, not a mechanical guarantee.

---

## Claim classes

Every substantive claim on a narrative page belongs to exactly one class:

- **citation.** The claim is traceable to a single corpus source. On-page form: the claim links the corpus document inline, and that document appears in `Corpus Sources`.
- **sourced.** The claim rests on a named external public standard, framework, or regulation. On-page form: the claim names the standard inline, and the standard appears in `External Sources`. Only standards on the ingestion specification's preserve-without-substitution list qualify; the verbatim-reproduction rules from the ingestion specification apply unchanged.
- **composite.** The claim is synthesized across multiple corpus or external sources and has no single anchor. On-page form: no inline anchor is required, but the page's limitations section must acknowledge that composite content requires the adopting organization's own validation.

Public pages show citations and the composite and sourced labels. The full per-claim matrices (claim text, class, contributing sources, verification date, verifier role) live in the page's review record, referenced by the `Review Record` identifier. They never appear on-page: the page stays readable for its audience, and the audit trail stays complete for the maintainer.

Explanatory pages may carry `citation` and `sourced` claims freely and `composite` claims only sparingly. A page whose claims are predominantly `composite` is a signal that it is original analysis rather than narrative translation, and original analysis belongs in the corpus, not the narrative layer.

---

## Causal vocabulary

When a narrative page relates a control, artefact, or practice to an outcome, it must use exactly one of four relationship words, and no other causal verb:

- **contribution.** The control materially advances the outcome without being sufficient for it.
- **dependency.** The outcome requires the named control or condition to hold.
- **prevention.** The control reduces the opportunity for a named failure mode.
- **evidence.** The artefact demonstrates that a control exists or operates.

The word `guarantee`, and any equivalent absolute (`eliminates`, `makes impossible`, `removes all risk`), must never appear in a causal statement. A narrative page states that a control is a contribution to, a dependency of, a prevention against, or evidence for an outcome; it never states that a control guarantees an outcome. Adoption is never presented as effectiveness, and gate passage is never presented as proof that a control operates in an adopter's organization. The absolutes denylist (`guarantee`, `eliminates`, `makes impossible`, `removes all risk`) is enforced PAGE-WIDE as a mechanical string-level check (the vocabulary gate, Gates item 6): these words must not appear in narrative prose at all, which needs no causal-statement classification. The positive rule (that a causal statement uses exactly one of the four approved words and no other causal verb) is a REVIEW outcome, because identifying which sentences are causal statements is a semantic judgement the string-level gate does not make.

Narrative pages must not make likelihood, frequency, or statistical claims unless the claim is `sourced` and the source is named inline.

---

## The qualified-shall rule

Narrative prose harmonizes normative verbs on `must`. An unqualified `shall` must not appear in narrative prose.

A `shall` is permitted only when it is qualified, and a qualified `shall` is defined as a verbatim, attributed source quotation with visible source adjacency: the `shall` appears inside a direct quotation of a named external source, reproduced verbatim, with the source citation visibly adjacent to the quotation (inline, immediately before or after). A `shall` that is not inside such a quotation, or whose source is not visibly adjacent, is an unqualified `shall` and is a defect. This rule proves a string-level property only; it does not certify that the quotation is faithful, which is a review concern.

---

## Mandatory sections and per-subtype schemas

Every narrative page, regardless of subtype, contains:

1. **Evidence to request.** What the reader should ask management for, expressed as evidence classes (reports, registers, test results, attestations), so the page converts understanding into an oversight action. Each entry follows the causal vocabulary (each item is evidence for a named control or outcome).
2. **Limitations.** What the page does not establish: at minimum, that the page creates no compliance, that the adopting organization must validate applicability, and any subtype-specific caution (a scenario's illustrative nature, a legal regime's volatility, composite-claim caveats).

Every page ends with the corpus `**End of Document**` marker.

The per-subtype section schemas (H2 sections, in order; sections marked (optional) may be omitted):

**Executive Brief (`brief-`)**

1. Why this matters
2. What the corpus establishes
3. What this means for the organization
4. Evidence to request
5. Limitations

**Scenario (`scenario-`)**

1. Scenario premise
2. How the event unfolds
3. Where the corpus controls engage
4. What good looks like
5. Evidence to request
6. Limitations

**Decision Narrative (`decision-`)**

1. The decision in front of leadership
2. What the corpus provides
3. Options and their consequences
4. Questions to resolve before deciding
5. Evidence to request
6. Limitations

**Oversight Question Set (`oversight-questions-`)**

1. Context for these questions
2. Questions (grouped by theme; each question paired with a note on what a strong answer contains)
3. Evidence to request
4. Limitations

**Story (`story-`)**

1. Setting
2. The story
3. What the story illustrates
4. Where the corpus controls appear
5. Evidence to request
6. Limitations

**Journey (`journey-`)**

1. Starting state
2. Stages (each stage: what changes, which corpus documents engage, signals of progress)
3. Destination state
4. Evidence to request
5. Limitations

**Outcome Map (`outcome-map-`)**

1. Outcome statement
2. Contribution map (each row relates a corpus control to the outcome using exactly one causal-vocabulary word)
3. Gaps and dependencies (optional)
4. Evidence to request
5. Limitations

Section titles are drafted in sentence case per house style. Where a content wave produces a sound section shape not captured above, this specification is amended to ratify the shape rather than the content being retrofitted; the subtype schemas are frozen only after the flagship and domain content is reconciled against them.

---

## Related Documents on a narrative page

The retained `Related Documents` field on a narrative page carries narrative-to-corpus links only: plain explanatory routes from the page to the corpus documents it explains. It never carries narrative-to-narrative links and never carries typed-edge semantics. Typed relationship edges (governed-by, implemented-by, evidenced-by, assured-by, explained-by) live exclusively in the narrative registry and the render model, never in page source. A narrative node is forbidden as the authoritative or evidence endpoint of any edge; only the explanatory direction may target a narrative node.

The authority boundary is one-way and enforced at source level: a corpus document must never reference `executive/` in any field, including Related Documents. Any corpus-explained-by-narrative view is derived at render time from the narrative registry, never written into corpus source or into `taxonomy.yml`.

---

## Corpus source references and review cadence

An executive narrative page REFERS to corpus documents but does not depend on their VERSIONS. `Corpus Sources` records the page's dependency PATHS only; a corpus version bump never invalidates a narrative page, and there is no source-version pinning, no staleness state machine, and no version-drift revalidation.

1. **Path references.** Every corpus source a page relies on is listed in `Corpus Sources` as a plain markdown link to the corpus document (a path reference, no version suffix). Exactly one reference per dependency; at least one is mandatory. Every corpus document linked in the page body must appear here (a body corpus link absent from the list is a defect).

2. **Structural invalidation is a broken link only.** The single structural failure of a corpus reference is a link that no longer resolves to a live corpus document (a moved or retired source). That is caught by the existing repository link and reference-integrity gates, which already scan `executive/`; the narrative layer adds no separate pin-resolution state machine.

3. **Content rule (point, never reproduce).** A narrative page POINTS TO corpus values; it never REPRODUCES them. A retention period, a threshold, or any specific value stays in the corpus document the page links, and the page directs the reader there rather than restating the value, so a corpus change never silently strands a stale copy in the narrative layer. This is a review outcome, not a mechanical guarantee.

4. **Review cadence (advisory).** A 6-month executive-review cadence is an advisory editorial freshness signal recorded in the `Last Reviewed` date. It is NOT a gated CI requirement: a lapsed review date surfaces in the scheduled review and never blocks a pull request. No generator or tool ever writes a `Corpus Sources` reference or edits page prose; keeping a page current is a human act.

## Release and retirement

The narrative layer follows a stated release and retirement principle; operational detail belongs to the late-wave operations runbook.

- **Versioning.** A narrative page follows the corpus version-numbering scheme. Any prose change or any change to its `Corpus Sources` references records a version and date bump.
- **Release notes.** Material narrative releases carry executive-facing release notes; the detail and cadence are deferred to the operations runbook.
- **Replacement and redirect.** A superseded page is replaced with a redirect to its successor, following the corpus lifecycle-marker precedent adapted to the narrative layer.
- **Retirement on lost corpus support.** When the corpus support a page depends on is removed (a referenced source retired with no successor), the page's corpus link no longer resolves and the existing link-integrity gate fails. If it cannot be re-pointed to a live corpus source, the page is retired. A narrative page must never outlive the corpus it explains.

---

## The narrative registry

`narrative.yml` is the generated, machine-readable registry of the narrative layer, the analogue of `taxonomy.yml` for `executive/`. It is regenerated from page metadata, never hand-edited, and carries per page: path, title, narrative type, narrative status, version, date, corpus source reference paths, external sources, claim classes present, review record identifier, last-reviewed date, and any derived tags.

Derived tags (topic, domain coverage, audience facets) live only here. They never appear in page headers and never appear in `taxonomy.yml`, which remains corpus-only by construction. No narrative row is ever added to `taxonomy.yml`; the two registries join only at render time.

The registry generator provides a `--check` mode that fails loud on an unreadable or malformed candidate page and never discovers pages from the committed registry. Registry completeness is proven by a three-way bijection among the independently enumerated `executive/` files, the registry rows, and the generated listing routes, with named exclusions for entry points and redirects.

---

## Language and neutrality requirements

Narrative pages inherit the ingestion specification's language and organization-neutrality requirements, with these narrative-layer differences and emphases. The narrative layer legitimately differs in voice from corpus house style; the reduced language-and-safety subset below (the dash ban plus the secrets and PII gates) replaces the corpus house-style language gate for narrative content, and the rest of the narrative mechanical set lives in the gate family described in the Gates section.

1. Entity-neutral audience wording throughout: `governing body`, `accountable executive leadership`, and the canonical parenthetical `(board, ELT, or senior management, as applicable)` where the full phrase is needed. Never `the board` alone as the assumed governance model, and never a named organization's structure. The whole layer is entity-neutral.
2. Normative verbs harmonize on `must`; an unqualified `shall` must not appear (see the qualified-shall rule).
3. No em dashes and no en dashes.
4. The organization-neutrality rules of the ingestion specification's Appendix A apply to narrative content without exception; scenarios and stories are composite and fictional by construction.
5. Plain executive register: a narrative page is written to be read in minutes by a non-specialist. Corpus terminology is used accurately but explained on first use.

The separation invariant is the design requirement for all of the above and is not claimed as wholly mechanically proven: the string-level checks (disclaimer presence, the causal denylist, the qualified-shall rule, the dash ban) prove string properties only. Zero authority confusion and zero unsupported claims are review outcomes backed by the per-claim matrices and recorded review evidence.

---

## Gates

This section records the gate intent this specification creates. The narrative gate family is under construction across the Phase-1 sequence; six members now exist, wired and manifest-classified `narrative-only`: the narrative metadata gate (item 4, gate 84), the registry and completeness gate (item 9, gate 85), the symmetric narrative-boundary gate (item 3, gate 86), the one-way authority-boundary gate (item 7 source half, gate 87), the disclaimer-presence gate (item 5, gate 89), and the vocabulary gate (item 6, gate 88). Every item below still marked new is design work for later phases; the specific wiring (which existing gate is extended versus which new gate is created, gate numbering, parity registration, and the four-surface obligation) is settled when each gate is built. Items marked existing are verified mechanisms this specification relies on.

1. **Type containment (existing, partial).** `Executive Narrative` stays out of the corpus metadata gate's allowed types permanently. An ordinary unchanged-copy leak into a scanned corpus location fails that gate loudly on the invalid type (a copied page also trips the Repository-Path check). This is PARTIAL: a leak named `README.md` in a corpus subdirectory (caught only by the loose domain-README check) and a leak retyped to a valid corpus type with narrative-extension fields both escape the existing gate. Closing those escapes is the symmetric boundary gate (item 3); the existing residual only guarantees that, for an unchanged non-README copy, the invalid-type failure cannot be silenced except by adding the type. The invariant to protect is that no one adds the type.
2. **Scan-scope split (existing).** The narrative-directory set and the gate-scope manifest exist and are regression-checked; the safety root-walkers cover `executive/` and the link gate already includes it. The by-name inclusion of `specification-executive-narrative.md` in the corpus metadata gate's root scan set is in place, so this specification is itself governed as a corpus document. No prefix-exemption is needed (the file is `Document Type: Specification` with the matching `specification-` prefix, so it passes the prefix check normally).
3. **Symmetric narrative-boundary gate (existing, gate 86).** Outside `executive/`: reject narrative document types or narrative-extension fields anywhere, README paths included (the README skip becomes path-scoped, not basename-keyed). Inside `executive/`: require the `Executive Narrative` type and the narrative-extension block on every page, and reject corpus document types. Honest residue: a file stripped of both its type marker and all narrative-only fields is not detectable by repository-state rules and is covered by review only.
4. **Narrative metadata gate (existing, gate 84).** Validates every file under `executive/` (except the named `executive/README.md` entry point): the 13 canonical fields plus the 8 extension fields, closed vocabularies for Narrative Type and Narrative Status, the type-to-prefix and type-to-subdirectory parity from the subtype table, the fixed subtype-to-status mapping, `Document Type: Executive Narrative` exactly, at least one `Corpus Sources` reference, and reference syntax (a plain markdown link with no version suffix). It also enforces body-link completeness: every corpus document linked in the page body must appear in `Corpus Sources` (a body corpus link absent from the list is a defect). The shared line-break gate does NOT scan `executive/`, so this narrative metadata gate owns the backslash hard-break validation for narrative pages (the append itself needs no change to the shared checker, whose generic last-line exemption already tolerates the extended block; the coverage of `executive/` is the new gate's obligation).
5. **Disclaimer presence gate (existing, gate 89).** The universal authority disclaimer, verbatim, as the first body content after the metadata block's closing `---` separator and before the first section heading, on every page (the entry-point `executive/README.md` exempt). String-level presence-and-position only; a fenced or indented copy of the disclaimer does not satisfy it (it is body content that is not the rendered disclaimer), and fail-loud on an unreadable page.
6. **Vocabulary gate (existing, gate 88).** No `guarantee` or the listed absolutes anywhere in narrative prose (page-wide, no causal-statement classification needed); no unqualified `shall` (with the qualified-shall definition as the sole exception); no em or en dashes. The existing bare-shall, language, and dash gates do not cover `executive/`, so narrative coverage needs its own wiring, not an `AUDITED_DOMAIN_DIRS` edit, which would wrongly pull `executive/` into every content gate.
7. **One-way authority boundary gate (existing source half, gate 87).** Corpus documents must not reference `executive/` in any field; gate 87 enforces this by scanning corpus document fields AND the generated `taxonomy.yml` (so an `executive/` target that reached the taxonomy is caught). Modelled on the existing directional-dependency gate (gate 53). Two obligations of this item are NOT yet built and remain design work for a later phase: making the taxonomy GENERATOR itself reject `executive/` targets at emission time (gate 87 is the post-hoc scan backstop, not a generator change), and the typed-edge endpoint/direction-matrix validation, which is DEFERRED to the render-model phase (item 12, website track): typed edges are derived at render time from the registry (see the Related Documents section), the generated `narrative.yml` carries no edge data, and with no authored pages there are no edge instances, so an endpoint/direction validator belongs with the renderer that emits edges rather than as a standalone corpus gate now.
8. **Staleness gate: removed by design (2026-08-06).** The executive layer has no corpus-version dependency, so source-version pinning, the staleness state machine, and version-drift revalidation are removed. A page references corpus documents by path only; the sole structural invalidation of a corpus reference is a broken link, already caught by the existing repository link and reference-integrity gates. The 6-month executive-review cadence is retained as an advisory `Last Reviewed` date, not a gated CI requirement.
9. **Registry and completeness gate (existing, gate 85).** `narrative.yml` matches a fresh regeneration (`--check`) and fails loud (exit 2) on an UNEMITTABLE candidate page (unreadable, or missing the Document Title or the `Executive Narrative` type). Corpus source references are recorded as plain dependency paths, with no version resolution and no staleness state. The generator never discovers from the committed registry; a three-way bijection among independently enumerated `executive/` files, registry rows, and generated listing routes, with named exclusions for entry points and redirects.
10. **Listing-surface gate (new).** Every active page under `executive/` appears in the generated listing derived from `narrative.yml`, and `executive/README.md` frames the concerns; the orphan gate keys off the generated listing. The structural auditor's exemption of `executive/` from domain READMEs and the document index register is registered wherever those exemptions live.
11. **Collision-ledger and mixed-diff gate (mixed-diff half built as PR-time delta gate D11).** The pull-request-delta mixed-diff check that rejects a pull request whose delta touches BOTH a narrative content page and a corpus-document path is built as delta gate D11 (the audit-programme specification's PR-only delta gates, §6.1), fail-closed in the interim. Two obligations of this item remain new: the accountably-reviewed override marker (the marker subject to a review rule, never mere presence) is a maintainer-owned governance-design decision, so the interim D11 posture is fail-closed with NO override path (stricter than the specified end state, never looser); and the ledger-to-content bijection check depends on the collision-ledger, which is not yet built.
12. **Renderer confinement (new, website track).** Narrative source paths normalized, repository-relative, regular files, resolved under `executive/` only; reject absolute paths, parent-directory traversal, symlinks, duplicates, and untracked sources; external-domain validation extends to narrative templates and rendered HTML.

Every blocking narrative gate and the registry `--check` carries the standard four-surface obligation (the CI quality workflow, the all-audits runner, the pre-commit set, and the audit-programme specification) with regression fixtures.

---

## Maintenance

This specification is reviewed annually and upon any material change to the narrative layer, its metadata model, its subtype set, or its gate wiring. Changes to the subtype table, the status vocabulary, the claim classes, the causal vocabulary, the qualified-shall definition, or the disclaimer wording are breaking changes and take a major or minor version bump per the corpus version-numbering rules, with a matching update to every gate that encodes the changed vocabulary.

---

**End of Document**
