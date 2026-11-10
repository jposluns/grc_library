# TODO

Forward-looking backlog of planned enhancements for the GRC Documentation Library. This file is an index-only roadmap (one row per open item, in priority bands); the per-item detail lives in a private operational store, where the project keeps one, joined by the stable id, and is not part of this public repository. Items are added when identified and rotated out when completed (the index row is deleted here; the detail block and the closure record, keyed by original backlog ID, are kept outside this repository); historical change detail lives in [`.working/CHANGELOG.md`](CHANGELOG.md).

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions: the ordinary CONTENT and METADATA gates skip it. A set of BACKLOG-SPECIFIC gates does intentionally read it, because governing the backlog is their whole job: number-permanence (gate 78), list-tag (gate 81), marked-done (gate 57), and staleness (gate 45) read the public index rows (and, where a private store is present, the private detail); index-reference parity (gate 90) checks the index rows' format and their one-to-one match (id, title, band, and order) with the `### <id>` detail blocks of a `TODO-REFERENCE.md`, read from the private store when one is present and otherwise from the repository root (when neither holds that file, it checks .working/TODO.md only for presence and readability); the retired-section-orphan check (D9) reads the .working/TODO.md index-row diff; and the two-file rotation check (D5) requires the .working/TODO.md index-row edit in a closure diff (the private detail block and the closure record rotate in the private store, outside the public diff). The intra-document section-reference gate scans this file (the positional section-reference gate deliberately EXEMPTS it). Every ordinary content and metadata gate skips it.

---

## How items are numbered and formatted

Items are grouped into four priority bands by work type: **P1** fix errors and prevent recurrence; **P2** fill significant gaps; **P3** clean up and tooling; **P4** adopter experience and future work (corpus expansion and items awaiting a decision). Within a band, rows run in a deliberate order (roughly lowest-effort-first, reordered by the maintainer at any time); a row's **position** is the queue order, not its number.

**Every open item is one INDEX ROW here plus one detail block, joined by the stable id.** The row is `| ID | Item | Tags |`; the detail block is `### <id> <title>` followed by the item's scope, dependencies, and status. The `Item` cell carries a one-line title with its `(severity, effort)` tag; `Tags` carries the `[public]`/`[private]` list-membership tag plus any `[content]`/`[machinery]`/`[BLOCKED: ...]` tag.

**The id is a permanent identity, never recycled** and **decoupled from the display band**: an item keeps its original number when it rebands, so a number's leading digit records the number-series it was drawn from, not its current band. One number maps to exactly one item across the whole history of the file, and a lookup by number is unambiguous. A closed item's number retires with it and is never reused; items are never renumbered when the file is reorganized (renumbering would break the changelog and other references that point at them). New numbers are drawn from the `## Number allocation` block below.

**Series-consolidation redirect-stub**: when an item's content is consolidated into a series (relocated under a series umbrella as a new child `X.Y.Z`), the original number `A.B` is neither reassigned nor deleted. The content moves to `X.Y.Z`; a one-line forward redirect stub stays at `A.B` (its own index row + a short `### A.B` reference block noting the move), so `A.B` still resolves as a forwarder while the series reads in execution order. The stub holds no content of its own and closes together with `X.Y.Z`. **Multi-phase-project series**: a project with distinct phases takes an umbrella number `N.M` as a goal-description heading (not itself a doable task) whose phases are `N.M.Y` children that are the actual work, each independently closeable and never bundled; the umbrella consumes one counter number and closes when its last child does.

**Effort scale** (referenced by the `(sev, effort)` tags): **XS** single-line / single-cell (5-15 min, bundle 5-10); **S** single-doc section add (30-90 min, bundle 2-4); **M** multi-doc bounded (2-4 hrs, 1/PR); **L** new artefact + multi-doc propagation (4-8 hrs, 1/PR); **XL** new domain / library-wide reshape (1-3 days, may split). Severity is `H[critical]` / `H` / `M` / `L` / `FYI`.

---

## Number allocation

Item numbers are permanent identity, never recycled, and decoupled from the P1-P4 display bands (an item keeps its number when it rebands). A new item draws the next number in the series matching its band's work type; the counter for that series then advances. Series 5, 6, and 7 are **frozen**: their items rebanded into P2 and P4, and no new 5.x / 6.x / 7.x numbers are drawn (the numbers already allocated in those series stay retired-or-live as permanent ids). Time-bounded follow-ups use the `TF-` series.

<!-- BEGIN-GENERATED number-allocation -->
- **Next item number: 1.32.** (P1 / fix series)
- **Next item number: 2.37.** (P2 / content series)
- **Next item number: 3.250.** (P3 / tooling series)
- **Next item number: 4.33.** (P4 / adopter series)
- **Next item number: 5.10.** (frozen; series 5 takes no new items)
- **Next item number: 6.7.** (frozen; series 6 takes no new items)
- **Next item number: 7.6.** (frozen; series 7 takes no new items)
- **Next item number: TF-5.** (time-bounded follow-ups)
<!-- END-GENERATED number-allocation -->

The 3.x (P3 / tooling) counter above is drawn from the public floor [`.claude/skills/corpus-management/tools/todo-number-floor.json`](../.claude/skills/corpus-management/tools/todo-number-floor.json) like the other active series. Series-3 is a single bare-`N.M` namespace shared with any private backlog list the project keeps; the floor records the highest bare-`N.M` series-3 ordinal ever allocated across both lists (this file and the private list, including retired numbers), so a public clone computes the next number without the closure records, and this generated block is the single authority for the next series-3 number.

---

## Priority 1 — Fix errors and prevent recurrence

Fix errors and prevent their recurrence. Worked first; the routine `/validate`, `/validate-pr`, `/matrix-fit`, and `/claim-fit` cadences are the reactive half.

| ID | Item | Tags |
| --- | --- | --- |

## Priority 2 — Fill significant gaps

Fill significant gaps: deepen thin-but-present content to operational sufficiency, and add the significant missing capabilities.

| ID | Item | Tags |
| --- | --- | --- |
| 2.1 | Privacy jurisdiction annex operational deepening (H, L) | `[public]` `[BLOCKED:source-acquisition (awaiting maintainer source drop)]` |
| 2.3 | Crypto-asset / blockchain governance domain (H[critical], XL) | `[public]` |
| 2.15 | Landing-page standards list: link each item to its authoritative source, MOVED to 2.25.2 (M, S-M) | `[public]` |
| 2.25 | Governance traceability and coverage expansion (umbrella; H, XL) | `[content+machinery]` `[public]` |
| 2.25.3 | Canadian public-sector authority coverage (CANADA-PRIORITY, H, L) | `[content]` `[public]` |
| 2.25.4 | AI assurance and evaluation content (H, L) | `[content]` `[public]` |
| 2.35 | Populate the governance relationship-model source with real corpus relationships (M, M) | `[content]` `[public]` |
| 2.36 | Semantic layer and business-definition governance standard (M, L) | `[content]` `[public]` |
| 2.26.1 | OSCAL adoption decision and model-scope lock (H, S) | `[machinery]` `[public]` |
| 2.26.2 | OSCAL stable-identifier layer (S, M) | `[machinery]` `[public]` |
| 2.26.3 | OSCAL metadata-field alignment (S, M) | `[machinery]` `[public]` |
| 2.26.4 | OSCAL catalog pilot: one domain, generated, gated (M, XL) | `[machinery]` `[public]` |
| 2.26.5 | OSCAL profiles and crosswalks for framework alignments (M, L) | `[machinery]` `[public]` |
| 2.29 | Latin-American privacy jurisdiction annexes + corpus alignment for the newly-held primaries (M, M) | `[content]` `[public]` |
| 2.25.2 | Control-to-policy-instrument coverage: international AI-governance authorities (M, M) | `[content]` `[public]` |
| 2.26 | OSCAL machine-readable representation (umbrella; H, XL) | `[machinery]` `[public]` |
| 2.33 | Canada-specific executive/jurisdiction document series (content) | `[public]` |
| 2.34 | Workforce monitoring and network-telemetry compliance suite (umbrella; H, L) | `[content]` `[public]` |

## Priority 3 — Clean up and tooling

Clean up and tooling: the gate/lint machinery and internal-apparatus items.

| ID | Item | Tags |
| --- | --- | --- |

## Priority 4 — Adopter experience and future

Adopter experience and future work: capability and guidance for organizations adopting the library, corpus expansion, and items awaiting a maintainer decision. Scheduled deliberately, after the fix/gap/cleanup tiers.

| ID | Item | Tags |
| --- | --- | --- |
| 4.1 | Corpus-management discipline as a shareable skill (M, XL) | `[public]` |
| 4.5 | Adopter reference-base specification: build-your-own-ref guide, source lists, and the corpus-to-sources relevance map (L, L) | `[public]` |
| 4.6 | Fork update-assessment tooling (upstream-change applicability report) (S-f, M-L) | `[public]` |
| 4.29 | `/adopt` adjustment + non-destructive tooling-update mode (L) | `[machinery]` `[public]` |
| 4.30 | Full adopter-experience assessment + `.adopt/` adoption kit (P4 umbrella, M-L, multi-phase) | `[public]` |
| 5.2 | Logistics country / programme expansion | `[public]` |
| 5.3 | Financial-services country regulator overlays | `[public]` |
| 5.4 | Healthcare country regulator overlays | `[public]` |
| 5.5 | Energy and utilities country regulator overlays | `[public]` |
| 5.6 | Telecommunications country regulator overlays | `[public]` |
| 5.7 | Public-sector country / regulator overlays | `[public]` `[BLOCKED:source-acquisition (awaiting maintainer source drop)]` |
| 5.8 | Privacy jurisdiction gaps | `[public]` `[BLOCKED:source-acquisition (awaiting maintainer source drop)]` |
| 5.9 | AI jurisdiction overlays | `[public]` `[BLOCKED:source-acquisition (awaiting maintainer source drop)]` |
| 6.1 | Identity-specific content depth (L) | `[public]` |
| 6.2 | Quantum cryptography readiness deepening (L) | `[public]` |
| 6.3 | Cross-framework matrix expansion (L) | `[public]` |
| 6.4 | CMMI capability levels alongside maturity levels (L) | `[public]` |
| 6.5 | Multi-cloud governance overlay (XL) | `[public]` |

---

## Time-bounded follow-ups

Non-urgent follow-ups deliberately DEFERRED to a future date, then re-evaluated: a suggested revisit of something already shipped, where acting now would be premature (not enough real-world signal yet). This is NOT the normal forward backlog (those are the priority bands); an item here is date-gated, not ready-now, and will mostly track "revisit this suggested follow-up after date X". Each entry carries a **Not-before** date (UTC), what to EVALUATE, and the originating PR. Review this section regularly and evaluate each entry whose Not-before date has passed. When a follow-up is acted on (or decided against), close it like any other item. (The `TF-` counter is in the `## Number allocation` block.)

---

## Notes on maintenance

- Add new items at the appropriate band; a row's position is its queue order. Move items between bands as context changes (the number never changes).
- One item, one functional action: split items per distinct resolution path; group bullets under one number only when they resolve as a single action.
- Item numbers are permanent, never recycled, and decoupled from the display band: new items draw from the `## Number allocation` series counters; a closed number retires with its item; items are not renumbered when the file is reorganized, so a number maps to exactly one item across the file's whole history. A series-consolidation move never REASSIGNS a number: the content moves to a new series child `X.Y.Z` and a forward redirect stub is left at the original number (both close together).
- Favour small, focused pull requests.
- Slash commands use short names (for example `/validate`); skill and procedure names stay descriptive.
- Template-content files that adopters see do not name or link `.working/`.
- When an item is completed, delete its index row here (no strikethroughs, no `[done]` suffixes); rotate its `### <id>` detail block and record its closure. Rotation discipline: the PR-finalization rules of the AIQT change-tracking discipline (https://aiqt.ai).
- Record design decisions outside this file, for example in a private operational store, where the project keeps one.
- This file (the public index) is the source of truth for what is queued.
- Review findings keep their authoritative per-finding evidence outside this file (for example, in a private operational store, where the project keeps one); this file is the action-organized view.
