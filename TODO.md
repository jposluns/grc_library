# TODO

Forward-looking backlog of planned enhancements for the GRC Documentation Library. This file is an index-only roadmap (one row per open item, in priority bands); the per-item detail lives in the maintainer's private sibling (`grc_library_private/TODO-REFERENCE.md`), joined by the stable id, and is not part of this public repository (maintainer-directed 2026-08-29: the detail does not need public visibility). Items are added when identified and rotated out when completed (the index row is deleted here; the private detail block rotates separately). Completed items move to `grc_library_private/.working/DONE.md` (closed-TODO ledger, keyed by original backlog ID); historical change detail lives in [`CHANGELOG.md`](CHANGELOG.md).

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions: the ordinary CONTENT and METADATA gates skip it. A set of BACKLOG-SPECIFIC gates does intentionally read it, because governing the backlog is their whole job: number-permanence (gate 78), list-tag (gate 81), marked-done (gate 57), and staleness (gate 45) read the public index rows (and, for the maintainer, the private detail); index-reference parity (gate 90) checks the index rows against the private `grc_library_private/TODO-REFERENCE.md` detail blocks (and no-ops in public CI / an adopter clone, which have no private sibling); the retired-section-orphan check (D9) reads the TODO.md index-row diff; and the two-file rotation check (D5) requires the TODO.md index-row edit in a closure diff (the private detail block and the DONE ledger rotate cross-repo, outside the public diff). The intra-document section-reference gate scans this file (the positional section-reference gate deliberately EXEMPTS it). Every ordinary content and metadata gate skips it.

---

## How items are numbered and formatted

Items are grouped into four priority bands by work type: **P1** fix errors and prevent recurrence; **P2** fill significant gaps; **P3** clean up and tooling; **P4** adopter experience and future work (corpus expansion and items awaiting a decision). Within a band, rows run in a deliberate order (roughly lowest-effort-first, maintainer-directed at any time); a row's **position** is the queue order, not its number.

**Every open item is one INDEX ROW here plus one detail block in the private `grc_library_private/TODO-REFERENCE.md`, joined by the stable id.** The row is `| ID | Item | Tags |`; the detail block is `### <id> <title>` followed by the item's scope, dependencies, and status. The `Item` cell carries a one-line title with its `(severity, effort)` tag; `Tags` carries the `[public]`/`[private]` list-membership tag plus any `[content]`/`[machinery]`/`[BLOCKED: ...]` tag.

**The id is a permanent identity, never recycled** (maintainer-directed 2026-07-15) and **decoupled from the display band** (maintainer-directed 2026-08-12): an item keeps its original number when it rebands, so a number's leading digit records the number-series it was drawn from, not its current band. One number maps to exactly one item across the whole history of the file, and a lookup by number is unambiguous. A closed item's number retires with it and is never reused; items are never renumbered when the file is reorganized (renumbering would break the CHANGELOG, DONE, and handoff references that point at them). New numbers are drawn from the `## Number allocation` block below.

**Series-consolidation redirect-stub** (maintainer-directed 2026-07-23): when an item's content is consolidated into a series (relocated under a series umbrella as a new child `X.Y.Z`), the original number `A.B` is neither reassigned nor deleted. The content moves to `X.Y.Z`; a one-line forward redirect stub stays at `A.B` (its own index row + a short `### A.B` reference block noting the move), so `A.B` still resolves as a forwarder while the series reads in execution order. The stub holds no content of its own and closes together with `X.Y.Z`. **Multi-phase-project series** (maintainer-directed 2026-07-26): a project with distinct phases takes an umbrella number `N.M` as a goal-description heading (not itself a doable task) whose phases are `N.M.Y` children that are the actual work, each independently closeable and never bundled; the umbrella consumes one counter number and closes when its last child does.

**Effort scale** (referenced by the `(sev, effort)` tags): **XS** single-line / single-cell (5-15 min, bundle 5-10); **S** single-doc section add (30-90 min, bundle 2-4); **M** multi-doc bounded (2-4 hrs, 1/PR); **L** new artefact + multi-doc propagation (4-8 hrs, 1/PR); **XL** new domain / library-wide reshape (1-3 days, may split). Severity is `H[critical]` / `H` / `M` / `L` / `FYI`. A `⚠` in a detail block marks a persona-quoted finding to verify at action time.

---

## Number allocation

Item numbers are permanent identity, never recycled, and decoupled from the P1-P4 display bands (an item keeps its number when it rebands). A new item draws the next number in the series matching its band's work type; the counter for that series then advances. Series 5, 6, and 7 are **frozen**: their items rebanded into P2 and P4, and no new 5.x / 6.x / 7.x numbers are drawn (the numbers already allocated in those series stay retired-or-live as permanent ids). Time-bounded follow-ups use the `TF-` series.

<!-- BEGIN-GENERATED number-allocation -->
- **Next item number: 1.32.** (P1 / fix series)
- **Next item number: 2.34.** (P2 / content series)
- **Next item number: 3.250.** (P3 / tooling series)
- **Next item number: 4.32.** (P4 / adopter series)
- **Next item number: 5.10.** (frozen; series 5 takes no new items)
- **Next item number: 6.7.** (frozen; series 6 takes no new items)
- **Next item number: 7.6.** (frozen; series 7 takes no new items)
- **Next item number: TF-4.** (time-bounded follow-ups)
<!-- END-GENERATED number-allocation -->

The 3.x (P3 / tooling) counter above is drawn from the public floor [`tools/todo-number-floor.json`](tools/todo-number-floor.json) like the other active series. Series-3 is a single bare-`N.M` namespace shared with the private `P-TODO.md` (the `P-N.M` namespace is separate); the floor records the highest bare-`N.M` series-3 ordinal ever allocated across both lists (`TODO.md` and `P-TODO.md`, including retired numbers), so a public clone computes the next number without `DONE.md`, and this generated block is the single authority for the next series-3 number.

---

## Queueing rules

- Orchestrator picks the next batch from **Priority 1 first, then Priority 2**, in highest-severity order; within a chosen band the row order helps assemble like-effort batches.
- **Start-side worker-collision check (before starting any item).** Before starting to build any item, check the scratch `claims-ledger.md` and `research/COVERAGE.md` for an in-flight claim or a pending inbox delivery covering it; a claimed or delivered item is apply-work (validate-then-apply on the delivery), not build-work. This fires whenever the queue is resumed mid-session, not only at `/orch`.
- **1-8 PRs per batch** (logical grouping); `/validate` after each batch.
- Maintainer direction supersedes the orchestrator's pick at any time.
- Lower-band items (P3-P4 expansion / future) are picked deliberately, not from the routine batch queue, unless the maintainer triggers them.
- **Integrity-tooling items** live in P1 (reference version-currency residuals) and P3 (the gate/lint machinery). Research fan-out (workers produce verified research from the worker-brief template; the orchestrator re-verifies every claim at apply-time and authors all final prose) is the standing method for partitionable batches.

---

## Priority 1 — Fix errors and prevent recurrence

Fix errors and prevent their recurrence. Worked first; the routine `/validate`, `/validate-pr`, `/matrix-fit`, and `/claim-fit` cadences are the reactive half.

| ID | Item | Tags |
| --- | --- | --- |
| 1.29 | EU AI Act Digital Omnibus reconciliation: correct the corpus for the in-force Regulation (EU) 2026/1744 (H, M) | `[content]` `[public]` |
| 1.31 | BASC clause-citation re-mapping to the held BASC sources (high-assurance) (H, L) | `[content]` `[public]` |

## Priority 2 — Fill significant gaps

Fill significant gaps: deepen thin-but-present content to operational sufficiency, and add the significant missing capabilities.

| ID | Item | Tags |
| --- | --- | --- |
| 2.1 | Privacy jurisdiction annex operational deepening (FR-59, H, L) | `[public]` |
| 2.3 | Crypto-asset / blockchain governance domain (FR-70, H[critical], XL) | `[public]` |
| 2.15 | Landing-page standards list: link each item to its authoritative source, MOVED to 2.25.2 (Series A) (maintainer-confirmed 2026-07-15, M, S-M) | `[public]` |
| 2.21 | Further AI-jurisdiction annexes (M, L; partly source-gated) | `[public]` |
| 2.23 | CCPA statute (eff. 2026-01-01) currency + alignment review (maintainer-flagged 2026-07-16, M, S; cross-repo, blocked on ref ingestion) | `[public]` |
| 2.25 | Governance traceability and coverage expansion (umbrella; maintainer-directed 2026-07-23, H, XL) | `[content+machinery]` `[public]` |
| 2.25.3 | Canadian public-sector authority coverage (consolidated with 2.22; CANADA-PRIORITY, H, L) | `[content]` `[public]` |
| 2.25.4 | AI assurance and evaluation content (H, L) | `[content]` `[public]` |
| 2.25.5 | Governance-maturity measurement model (maintainer-directed 2026-07-23; M, M) | `[content]` `[public]` |
| 2.26.1 | OSCAL adoption decision and model-scope lock (maintainer-directed 2026-07-23; H, S) | `[machinery]` `[public]` |
| 2.26.2 | OSCAL stable-identifier layer (S, M) | `[machinery]` `[public]` |
| 2.26.3 | OSCAL metadata-field alignment (S, M) | `[machinery]` `[public]` |
| 2.26.4 | OSCAL catalog pilot: one domain, generated, gated (maintainer-directed 2026-07-23; M, XL) | `[machinery]` `[public]` |
| 2.26.5 | OSCAL profiles and crosswalks for framework alignments (M, L) | `[machinery]` `[public]` |
| 2.28 | AI jurisdiction annex + ref ingest: Singapore Model AI Governance Framework for Agentic AI (M, M) | `[content]` `[public]` |
| 2.29 | Latin-American privacy jurisdiction annexes + corpus alignment for the newly-held primaries (M, M) | `[content]` `[public]` |
| 2.30 | Enterprise AI adoption governance (goal-description umbrella; scheduled after the relocated AIQT umbrella (private backlog) and the post-AIQT error pass; maintainer-directed 2026-08-03) | `[public]` |
| 2.30.1 | AI value-and-decision-governance framework: close the four absent value constructs (H, L) | `[content]` `[public]` |
| 2.30.2 | Name the AI human overseer in the role-based training surfaces (M, S-M) | `[content]` `[public]` |
| 2.18 | AI jurisdiction annex: South Korea AI Basic Act (H, M) | `[public]` |
| 2.25.2 | Control-to-policy-instrument coverage: international AI-governance authorities (consolidated with 2.15; M, M) | `[content]` `[public]` |
| 2.26 | OSCAL machine-readable representation (umbrella; maintainer-directed 2026-07-23, H, XL) | `[machinery]` `[public]` |
| 2.33 | Canada-specific executive/jurisdiction document series (maintainer-directed 2026-08-17; content; moved from private P-1.38 2026-08-30) | `[public]` |
| 3.184 | Corpus ISO citation currency updates enabled by the 2026-07-28 `_ref` ingest (2026-07-28 ingest follow-up, M, S) | `[public]` |
| 3.14 | ETSI Securing-AI alignment map (L, M) (was 3.16) | `[public]` |

## Priority 3 — Clean up and tooling

Clean up and tooling: the gate/lint machinery and internal-apparatus items.

| ID | Item | Tags |
| --- | --- | --- |
| 3.47 | TODO adoptability: strip internal working-provenance annotations (S) | `[public]` |

## Priority 4 — Adopter experience and future

Adopter experience and future work: capability and guidance for organizations adopting the library, corpus expansion, and items awaiting a maintainer decision. Scheduled deliberately, after the fix/gap/cleanup tiers.

| ID | Item | Tags |
| --- | --- | --- |
| 3.183 | Adopter overlay-exemption config: replace the `DEFAULT_EXEMPT_DIRS` source-edit instruction with a non-source config surface (2026-07-28 deep-assessment c6, claude, L, S; re-scoped 2026-08-29 to sub-part 2) | `[public]` |
| 4.1 | Corpus-management discipline as a shareable skill (M, XL) | `[public]` |
| 4.5 | Adopter reference-base specification: build-your-own-ref guide, source lists, and the corpus-to-sources relevance map (L, L) | `[public]` |
| 4.6 | Fork update-assessment tooling (upstream-change applicability report) (S-f, maintainer-requested 2026-07-04, M-L) | `[public]` |
| 4.29 | `/adopt` adjustment + non-destructive tooling-update mode (maintainer-directed 2026-07-19, L) | `[machinery]` `[public]` |
| 4.30 | Full adopter-experience assessment + `.adopt/` adoption kit (maintainer-directed 2026-07-19, P4 umbrella, M-L, multi-phase) | `[public]` |
| 5.2 | Logistics country / programme expansion (was 5.1) | `[public]` |
| 5.3 | Financial-services country regulator overlays (was 5.2) | `[public]` |
| 5.4 | Healthcare country regulator overlays (was 5.3) | `[public]` |
| 5.5 | Energy and utilities country regulator overlays (was 5.4) | `[public]` |
| 5.6 | Telecommunications country regulator overlays (was 5.5) | `[public]` |
| 5.7 | Public-sector country / regulator overlays (was 5.6) | `[public]` |
| 5.8 | Privacy jurisdiction gaps (was 5.7) | `[public]` |
| 5.9 | AI jurisdiction overlays (was 5.8) | `[public]` |
| 6.1 | Identity-specific content depth (L) (was 6.2) | `[public]` |
| 6.2 | Quantum cryptography readiness deepening (L) (was 6.3) | `[public]` |
| 6.3 | Cross-framework matrix expansion (L) (was 6.4) | `[public]` |
| 6.4 | CMMI capability levels alongside maturity levels (L) (was 6.5) | `[public]` |
| 6.5 | Multi-cloud governance overlay (XL) (was 6.1) | `[public]` |
| 6.6 | Java EE / Jakarta EE security standard (L) | `[public]` |

---

## Time-bounded follow-ups

Non-urgent follow-ups deliberately DEFERRED to a future date, then re-evaluated: a suggested revisit of something already shipped, where acting now would be premature (not enough real-world signal yet). This is NOT the normal forward backlog (those are the priority bands); an item here is date-gated, not ready-now, and will mostly track "revisit this suggested follow-up after date X". Each entry carries a **Not-before** date (UTC), what to EVALUATE, and the originating PR. `/orch` reads this section and surfaces any entry whose Not-before date has passed. When a follow-up is acted on (or decided against), rotate it to `grc_library_private/.working/DONE.md` like any other closed item. (The `TF-` counter is in the `## Number allocation` block.)

---

## Standing conventions

Durable behavioural guidance from the maintainer. NOT actionable items; reference material for the orchestrator and future contributors.

- **"More PRs, keep each one clean"** — favor small focused PRs.
- **"One item, one functional action"** (2026-07-10) — split items per distinct resolution path; group bullets under one number only when they resolve as a single action.
- **Item numbers are permanent, never recycled, and decoupled from the display band** (2026-07-15, 2026-08-12) — new items draw from the `## Number allocation` series counters; a closed number retires with its item; items are not renumbered when the file is reorganized, so a number maps to exactly one item across the file's whole history. A series-consolidation move never REASSIGNS a number: the content moves to a new series child `X.Y.Z` and a forward redirect stub is left at the original number (both close together).
- **"I prefer /validate, not /validation-sweep"** — short slash commands; skill names stay descriptive.
- **"Don't explicitly name or link `.working/`"** in template-content files that adopters see.
- **"Inference must be validated before committing or before anything else uses that information"** — operationalized in [`validate-inference-before-action.md`](guardrails/governance/validate-inference-before-action.md).
- **Activity directories should be self-contained** — the canonical `.working/<activity>/` layout.
- **Zero-finding sweeps still need history rows but no detail files** — validation-sweep [`SKILL.md`](guardrails/skills/validation-sweep/SKILL.md) step 9.
- **Sweep history is project-application, not template content** — operationalized by keeping the history file in `.working/`.
- **TODO is forward-looking; historical state rotates to DONE.md** — [`change-tracking.md`](guardrails/governance/change-tracking.md).
- **After completing a merge, list the next 5 planned PRs from the `## Up next` queue at the top of the private `P-TODO.md`** (the single ordered work queue across both backlogs; `/orch` itself continues from the handoff Next-actions, not this queue) — [`.claude/CLAUDE.md`](.claude/CLAUDE.md) PR-workflow section.
- **Validate cadence is 1-8 PRs per batch, not strictly 5.**
- **DONE keeps its own H3 format** — DONE uses `### PR #N:` headings; it does NOT mirror the TODO index-row format (the two diverged in the TODO-rework).
- **Compute-don't-ask** — before surfacing a question, apply a "can I compute/verify this myself?" gate; codified into `clarify-before-acting`.

---

## Notes on maintenance

- Add new items at the appropriate band; a row's position is its queue order. Move items between bands as context changes (the number never changes).
- When an item is completed, delete its index row here (no strikethroughs, no `[done]` suffixes); the item's `### <id>` detail block in the private `grc_library_private/TODO-REFERENCE.md` and the `grc_library_private/.working/DONE.md` entry rotate in the private sibling. Rotation discipline: the PR-finalization-protocol section of [`.claude/rules/governance/change-tracking.md`](.claude/rules/governance/change-tracking.md).
- Design decisions belong in `grc_library_private/design-decisions.md`, not TODO.
- This file (the public index; per-item detail in the private `grc_library_private/TODO-REFERENCE.md`) is the source of truth for what's queued; conversation history is not.
- Fitness-review backlogs remain the authoritative per-finding evidence source; this file is the action-organized view.
