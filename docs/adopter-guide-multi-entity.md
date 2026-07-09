# Adopting the library across a group or multi-entity structure

**Document Title:** Adopting the Library Across a Group or Multi-Entity Structure\
**Document Type:** Guide\
**Version:** 0.0.1\
**Date:** 2026-07-09\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`docs/adopter-guide.md`](adopter-guide.md), [`docs/decision-tree.md`](decision-tree.md), [`docs/worked-example-adoption.md`](worked-example-adoption.md), [`docs/template-implementation-roadmap.md`](template-implementation-roadmap.md), [`governance/register-role-authority.md`](../governance/register-role-authority.md), [`privacy/annex-privacy-jurisdiction-index.md`](../privacy/annex-privacy-jurisdiction-index.md)\
**Classification:** Public\
**Category:** Documentation\
**Review Frequency:** Annual and upon material change to the adopter guide or the versioning policy\
**Repository Path:** [`docs/adopter-guide-multi-entity.md`](adopter-guide-multi-entity.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

The [`docs/adopter-guide.md`](adopter-guide.md) and its worked example [`docs/worked-example-adoption.md`](worked-example-adoption.md) show a single organization adopting the library. A group, holding company, or multi-entity structure has a further decision the single-entity guidance does not address: how to adopt the library across several legal entities that share governance but differ in jurisdiction, sector, and regulatory exposure. This guide adds that topology layer. It composes the corpus's existing group-scope precedents, the jurisdiction-annex layering model, and the versioning policy by cross-reference; it does not restate the single-entity adoption mechanics, for which the adopter guide governs.

The concepts a group needs, group-wide scope, per-entity variance, new-entity onboarding, and cross-entity aggregation, already appear inside substantive corpus content (the enterprise-risk and compliance policies both state group-wide applicability across their business units, subsidiaries, and organizational entities; the mergers-and-acquisitions procedure covers legal-entity structure; the concentration-risk register treats intra-group concentration between legal entities of the same group as one of its dimensions). What was missing, and what this guide provides, is the adoption-surface view: which topology to choose and what each costs.

## The three adoption topologies

A group choosing how to adopt the library selects one of three topologies. The choice is not permanent; a group can migrate between them as it matures.

1. **Single shared library, group-wide.** One fork or copy is operated centrally, and every entity consumes the same corpus. Per-entity variance is handled with private overlays and the existing sector and jurisdiction annexes rather than separate copies. This is the simplest topology and gives the strongest consistency, at the cost of the weakest per-entity autonomy. It reuses the corpus's own group-wide scope precedents (for example the enterprise governance and risk policy and the legal and regulatory compliance policy both state applicability across the organization's business units, subsidiaries, and entities).

2. **Per-entity forks with a group baseline.** The group maintains a baseline fork upstream, and each entity forks that baseline and adapts it. Entities pull baseline updates using the adopter guide's track-upstream step. This gives the strongest per-entity autonomy, at a real cost: each fork acquires its own version line the moment it diverges, so the group must actively track which entity is on which version (see the versioning section below).

3. **Hub-and-spoke with entity annexes.** A group baseline is layered with per-entity annexes exactly as the privacy jurisdiction annexes layer onto the privacy baseline (per [`privacy/annex-privacy-jurisdiction-index.md`](../privacy/annex-privacy-jurisdiction-index.md), an adopter retains only the annexes that apply to its footprint). Each entity annex carries only that entity's deltas: its jurisdictions, its sector overlays, and its role-authority differences. This balances consistency and autonomy, and it reuses a layering model the corpus already proves. For most groups it is the recommended default.

## Versioning and the CalVer surface per topology

The library carries a single library-wide Calendar Version (the `Library Version` line in [`README.md`](../README.md), format `YYYY.MM.patch`, defined in the master-project specification) plus a per-document semantic version on every document. How that surface behaves depends on the topology:

- **Topology 1 (single shared library):** one CalVer line for the whole group; no divergence. This is the simplest version story, and it is the reason a tightly-integrated group with uniform regulation often chooses it.
- **Topology 2 (per-entity forks):** each fork has its own CalVer line from the moment it diverges from the baseline. The group must decide whether entities track the upstream baseline CalVer (pull and re-stamp) or run independent CalVer sequences. Either way, "which version is entity X on" becomes a real tracking question, and this guide names it as the topology's principal cost.
- **Topology 3 (hub-and-spoke):** the baseline keeps its CalVer, and each entity annex carries its own per-document version. The baseline version answers "what group standard applies"; the annex version answers "what entity delta applies". This is cleaner than per-entity forks because only the deltas version independently, not the whole corpus.

## Role mapping when governance authorities differ per entity

Roles in the library are organization-neutral and are customized per fork ([`governance/register-role-authority.md`](../governance/register-role-authority.md)); the single-entity substitution walk is in [`docs/worked-example-adoption.md`](worked-example-adoption.md). For a group, the same artefact's Approving Authority may be a group function in one topology and an entity function in another:

- In topology 1 the group governance authority approves centrally, and every entity inherits that approval.
- In topologies 2 and 3 each entity names its own Approving Authority (its own role-authority register rows), and the group decides which artefacts are group-reserved (approved once, group-wide) and which are entity-delegated (approved per entity).

The role-authority register's maintenance rule that one organization may combine roles extends naturally to the group case: the group decides which roles are held at the group level and which at the entity level. As in the single-entity case, the mapping of a neutral role to a named function lives in a private overlay; the public fork keeps the neutral role titles, and no named individual is written into a committed artefact.

## Jurisdictional layering

A multi-entity group reuses the privacy jurisdiction-annex layering directly. The privacy jurisdiction index already models a baseline plus retain-only-relevant per-jurisdiction annexes; a group applies the same mechanism per entity. The group baseline carries the cross-cutting content, and each entity retains only the jurisdiction annexes for its own footprint: an entity operating in the European Union keeps the European Union annex, and a United-States-only entity does not. This is the same scoping mechanism a single adopter uses to select its jurisdictions, applied once per entity.

New-entity onboarding threads the mergers-and-acquisitions due-diligence procedure ([`compliance/procedure-mergers-acquisitions-due-diligence.md`](../compliance/procedure-mergers-acquisitions-due-diligence.md) covers legal-entity and governance structure): a newly-acquired entity is layered in as a new spoke (topology 3) or a new fork (topology 2), inheriting the group baseline and adding only its own deltas.

## Trade-offs per topology

| Topology | Consistency | Per-entity autonomy | Version-tracking cost | Best when |
| --- | --- | --- | --- | --- |
| 1 Single shared library | Highest | Lowest | Lowest (one CalVer) | Tightly-integrated group, uniform regulation |
| 2 Per-entity forks | Lowest | Highest | Highest (CalVer divergence) | Loosely-coupled entities, divergent regulation or sector |
| 3 Hub-and-spoke annexes | High | Medium-high | Medium (baseline plus annex versions) | Group baseline with real per-entity deltas (the default for most groups) |

## Limitations and cross-references

- This guide is a reasoned synthesis of adoption topologies grounded in the corpus's existing group-scope statements, the jurisdiction-annex layering model, and the versioning policy; it is not a quote of a pre-existing topology document, because none existed (that gap is what this guide fills). It is adoption guidance, not a control document, so it carries no framework-alignment mapping of its own.
- The single-entity adoption mechanics (how one organization forks, customizes, substitutes roles, and phases its programme) are governed by [`docs/adopter-guide.md`](adopter-guide.md) and walked in [`docs/worked-example-adoption.md`](worked-example-adoption.md); this guide sits at the group-topology layer above them and does not restate them.
- The decision tree [`docs/decision-tree.md`](decision-tree.md) is entered per entity to scope that entity's domains and jurisdictions; the phasing of composition over time is governed by [`docs/template-implementation-roadmap.md`](template-implementation-roadmap.md). This guide governs only the group-topology choice, not the per-entity reading order or the phasing calendar.
- The topology choice is reversible: a group can begin with topology 1 for speed and migrate to topology 3 as per-entity deltas accumulate, or consolidate topology-2 forks back to a hub-and-spoke baseline to regain consistency.
