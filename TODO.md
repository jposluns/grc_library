# TODO

Forward-looking backlog of planned enhancements for the GRC Documentation Library. Items are added when identified and rotated out when completed. Completed items move to [`.working/DONE.md`](.working/DONE.md) (closed-TODO ledger, keyed by original backlog ID); historical change detail lives in [`CHANGELOG.md`](CHANGELOG.md). This file holds only pending and queued items.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions, with one narrow exception: [`tools/lint-todo-staleness.py`](tools/lint-todo-staleness.py) (gate 45) scans this file for the queued-PR-already-merged drift shape (its companion sweep-cursor-behind-history check reads the resume cursor from [`.working/session-handoff.md`](.working/session-handoff.md)). The intra-document section-reference gate also scans it. Other audit gates skip this file.

**How items are numbered and formatted.** Items are grouped by priority (P1-P7), tiered by work type (maintainer's 2026-06-30 leaning): P1 fix errors and prevent recurrence, P2 fill significant gaps, P3 clean up and tooling, P4 adopter experience, P5-P6 expand the corpus (overlays, then new domains), P7 awaiting decision. **Every item is a `### N.M` subsection whose leading digit is its priority** (so a P3 item is `3.x`); within a section items run lowest-effort-first. **One item is one functional action / one distinct resolution path** (maintainer-directed 2026-07-10): multiple bullets sit under one number only when they resolve as a single action (same file, same fix, one commit); otherwise they are split into separate numbered items. The `N.M` number is a position, not a permanent id, so it changes if an item is re-tiered, resequenced, or split; the **stable id is the `FR-N` / descriptive identifier in the heading**, and a `(was X.Y)` tag preserves the prior number for one cycle so older references (CHANGELOG, handoff, retro log, tool docstrings) stay resolvable. Each heading carries `(id, severity, effort)` where severity is `H[critical]` / `H` / `M` / `L` / `FYI` and effort is `XS` / `S` / `M` / `L` / `XL`. A `⚠` marks a persona-quoted finding to verify at action time.

**Effort scale** (referenced by the `(sev, effort)` tags): **XS** single-line / single-cell (5-15 min, bundle 5-10); **S** single-doc section add (30-90 min, bundle 2-4); **M** multi-doc bounded (2-4 hrs, 1/PR); **L** new artefact + multi-doc propagation (4-8 hrs, 1/PR); **XL** new domain / library-wide reshape (1-3 days, may split).

---

## Queueing rules

- Orchestrator picks the next batch from **Priority 1 first, then Priority 2**, in highest-severity order; within a chosen section the effort ordering helps assemble like-effort batches.
- **Start-side worker-collision check (before starting any item).** Before starting to build any TODO item, check the scratch `claims-ledger.md` and `research/COVERAGE.md` for an in-flight claim or a pending inbox delivery covering it; a claimed or delivered item is apply-work (validate-then-apply on the delivery), not build-work, so starting to build it would duplicate a worker's effort or collide with a pending delivery. This is the start-side complement to the close-out worker-brief coverage-pairing obligation, and it fires whenever the queue is resumed mid-session, not only at `/resume`. The operational form is in the multi-session-orchestration runbook.
- **1-8 PRs per batch** (logical grouping); `/validate` after each batch.
- Maintainer direction supersedes the orchestrator's pick at any time.
- Lower priorities (P3-P7) are picked deliberately, not from the routine batch queue, unless the maintainer triggers them.
- **Maintainer-directed running order (2026-06-30 work-type re-tier)**: work the tiers in order. **P1** first (the cheap fix/prevent items); then **P2** gaps (FR-59 deepenings first, then **FR-70**, the XL crypto-asset domain, last); then **P3** clean-up-and-tooling; then **P4** adopter experience. **P5 / P6 expansion waits.** The standing **fix-issues-first** directive (2026-06-27) governs within each tier, and the routine `/validate`, `/validate-pr`, `/matrix-fit`, and `/claim-fit` cadences are the reactive half of P1.
- **Integrity-tooling items** live in **P1** (reference version-currency residuals) and **P3** (the gate/lint machinery). Research fan-out (workers produce verified research from [`.working/worker-brief-template.md`](.working/worker-brief-template.md); the orchestrator re-verifies every claim at apply-time and authors all final prose) is the standing method for partitionable batches.

---

## Priority 1 — Fix errors and prevent recurrence

Correctness fixes and the **error-prevention tooling** that keeps the corpus from regressing. The routine `/validate`, `/validate-pr`, `/matrix-fit`, and `/claim-fit` cadences are the reactive half of this tier; the standing preventive half is the fix-and-prevent items listed here when any are open.

P1 currently holds one open item (§1.1, the discussion-vs-execution mode gate). Its earlier correctness and reference-currency residuals (§1.5 through §1.11) are all closed (the version-currency register shipped in #505; the `needs-reconfirm` sweep ran in #751; the completion-guard, file-type-width, and ref-side items closed through #818). New P1 items are added here as errors or recurrence-risks surface; the routine cadences above are the ongoing preventive half.

### 1.1 Discussion-vs-execution mode gate (guardrail against assistant overeagerness) (H, M)

Design a guardrail against a recurring assistant failure class: treating a conceptual or planning discussion as licence to begin execution ("I'll start building this now"), or treating a conditional / sequenced GO (deliver X, wait, then go) as immediate self-authorization and executing before the maintainer's explicit go. The guardrail is an explicit **discussion-mode vs execution-mode gate**: execution begins only on an express maintainer GO that names the work, and a conditional GO is not satisfied until its condition is maintainer-confirmed. Design scope: state the gate in the project [`.claude/CLAUDE.md`](.claude/CLAUDE.md) and the worker-brief / onboarding surfaces; draft a candidate pack rule or rule-amendment for it (adjacent to `clarify-before-acting` and `session-lifecycle`, but its own failure class); and assess whether a mechanical or hook-level backstop is feasible. This is a recurring failure mode (seen repeatedly in worker sessions), which is why it is P1. Record-only; do not begin the design until the item is picked.

---

## Priority 2 — Fill significant gaps

Deepening thin-but-present content to operational sufficiency, and the significant missing capabilities.

### 2.1 Privacy jurisdiction annex operational deepening (FR-59, H, L)

Privacy jurisdiction annexes are too shallow for operational sufficiency; deepen the remaining source-gated country annexes to operational level. Japan, United States, Canada, and Brazil are deepened (2026-07-04 held-source batch 1); the Latin America correction + standalone Mexico annex shipped in #750 (discharging the fr-59 Mexico accepted-unverified tracker against the held 2025 LFPDPPP). Remaining: the 18 source-gated annexes (gap analysis at `inbox/worker-20260703-a/fr-59-privacy-jurisdiction/research-source-gated-gaps.md`), which wait on maintainer source drops (APAC beyond Japan, and others absent from the reference base). Out of this item by design: the EU annex (fr-74-owned) and the UK annex (already operationally deep).

### 2.3 Crypto-asset / blockchain governance domain (FR-70, H[critical], XL)

New domain for crypto-asset / blockchain governance: digital-asset custody, staking, smart-contract risk, blockchain platform vetting. Regulatory references: DORA, MiCA, NYDFS BitLicense (MiCA / NYDFS BitLicense not held; source-gated). (Cross-references P6.x for domain-level shaping.)

### 2.4 Public presence at grclibrary.ai (Cloudflare Pages, auto-updating) (maintainer-directed 2026-07-12, M, L; ATTENDED-ONLY)

Publish a public landing site at the maintainer's `grclibrary.ai` domain, expanding the library's availability to entities who do not use GitHub by default (the maintainer's stated rationale for P2). A finalized design and a build/deploy spec are staged in scratch at `inbox/grclibrary-landing-page/` (`BRIEF.md`, `MANIFEST.md`, and a self-contained sample `grclibrary-landing.html` with light/dark themes and seven sections). Build shape: a top-level `.web/` generator in this repo that reads the corpus **live** at build and recomputes every figure from `taxonomy.yml` / the audit-programme inventory (never hardcode; the gate suite is described qualitatively, never as a gate count, per the maintainer's direction); the rendered HTML is an ephemeral build artefact (only the generator source and templates are committed). Deploy via **Cloudflare Pages** (maintainer has a PRO plan), auto-building on push to the production branch, with build watch-paths scoped to content-affecting changes (include the published content dirs + `.web/`; exclude `tools/`, `tests/`, `.working/`, `.claude/`, `.github/`). Add a **generator-health CI check** (dry-run that fails if the generator cannot parse the corpus it depends on; not a sync gate, since the site keeps no committed corpus copies). **Hard dependency: the §4.8 pack adoption-hygiene refactor must merge first** (section 03 of the page features and links the `dev-security/claude-rules/` pack, which must be made project-agnostic and free of project-internal references before the site publishes). **ATTENDED-SESSION-ONLY (maintainer-directed 2026-07-12):** the work requires maintainer interactivity, so it does not run unattended. Open items for the maintainer at build/deploy time: the publication go-decision (the sample stays preview-only until then), the production branch name, the Cloudflare Pages project settings, and the About credential strip (CGEIT/CISSP framing) against the bio prose. Confirm current Cloudflare watch-path-bypass thresholds and deploy-hook rate limits against live vendor docs before relying on exact figures. A scratch delivery exists, so this item is apply/build-work gated on §4.8, not a from-scratch design; the coverage-refresh sync re-points its row at `inbox/grclibrary-landing-page/`.

---

## Priority 3 — Clean up and tooling

Cross-document consistency cleanup and routine development / quality tooling: lower-priority than gaps, not error-prevention or adopter-facing. Picked deliberately into batches, not from the routine P1/P2 queue.

### 3.1 Base-unverified ISO/IEC designation debt tracker (L, S)

The #663 corpus-wide accuracy sweep converted only the 13 joint standards confirmed against the held `grc_library_ref` base; a further set were NOT base-confirmed, so the sweep left their remaining bare occurrences in a MIXED bare / `ISO/IEC` state (accuracy over form). Candidates with their 2026-07-05 bare / `/IEC` counts: `ISO 27033` (3/15), `ISO 27034` (3/2), `ISO 27559` (1/2), `ISO 29184` (1/4), `ISO 20889` (1/2), `ISO 25010` (2/1), `ISO 30134` (2/2), `ISO 5259` (1/9), `ISO 38505` (1/2), `ISO 23247` (3/0, the only uniformly-bare one), `ISO 12207` (tripartite ISO/IEC/IEEE, 2/1). For each, verify the correct issuing-body designation against the held base (or a primary source), then reconcile every occurrence to the confirmed form. Until verified the mixed state stands as tracked debt. The generic-family `ISO 27001` reference carve-out (Sweep-86 F4: framework-family names alongside `NIST CSF`, not edition-pinned citations, at `compliance/register-compliance-obligations-template.md:117`, `NOTICE.md:34`, `NOTICE.md:60`) is adjudicated as part of building §3.2 (likely an acceptable carve-out). This is the accepted-unverified tracker for the #663 sweep's deliberate scope boundary.

### 3.2 Authoritative standards register + designation-correctness gate (M-H, L; egress-gated)

The durable MECHANICAL solution to the ISO/IEC-designation-accuracy class §3.1 tracks: an authoritative register of every standard the project uses, recording each standard's correct issuing-body designation (`ISO` / `IEC` / `ISO/IEC` / `ISO/IEC/IEEE`) verified against the primary source, plus a norm (the corpus uses the correct designation; a direct quote of another source's differing usage is the only sanctioned exemption, marked as a quote); then a gate (sibling to GR-GAP-1, ideally sharing its register) that verifies each registered standard number's designation prefix matches the register, failing on a mismatch. Egress-gated (per-standard primary-source verification, the same egress §3.9 waits on). Design notes: (a) the designation axis is orthogonal to GR-GAP-1's version-year axis (share the register, different columns); (b) sole-ISO standards (27799, 31000, 9001) must stay bare, so the register's designation column is the source of truth, not a blanket "add /IEC"; (c) tripartite standards (12207, 42010) need `ISO/IEC/IEEE`, so the column is free-text designation.

### 3.3 CLAUDE.md removal-ledger review cadence (standing) (was 3.12)

Each `/retro` scans the [`.working/claude-md-considerations.md`](.working/claude-md-considerations.md) removal ledger's open RM entries and the periodic hallucination-metrics pass does a deeper scan; if an entry's "evidence the removal was wrong" signal appears, advise the maintainer to restore the cut text, and record the disposition in that entry's Status. Standing tracker; stays open by design.

### 3.6 Register-ageing advisory tool (GR-8 follow-on A, guardrail review 2026-07-02, L, S)

A small advisory `tools/audit-*.py` (not a gate) reporting improvement-log Proposed-improvement cells still pending after N PRs, the register-side analogue of the brief-freshness tool. **Attempted + deferred 2026-07-08 (#698) with a design finding:** the core heuristic (non-empty Proposed-improvement cell + no disposition token = pending) OVER-FLAGS (cannot distinguish a genuine pending FORMAL candidate from an adopted-in-place habit note; ~78 July cells mostly false-positive). Needs either a formal-candidate classifier or a register-format change (a structured candidate marker the `/retro` skill appends). Not shipped (an over-flagging advisory erodes trust). Revisit once the classifier / register-format decision is made.

### 3.7 Expiry-tail one-pass batch review (GR-8 follow-on B, guardrail review 2026-07-02, IN PROGRESS, M)

A drafted triage proposal (research subagent, orchestrator-verified) over the ~236 aged pending improvement-log candidates (pre-July rows), each with a proposed CODIFIED/EXPIRED/ROUTED/keep verdict, reviewed by the maintainer in one round; tokens land only on the maintainer's dispositions (rejection and expiry are maintainer calls per the register convention).

### 3.8 History-aware gate subprocess batching (GR-10, guardrail review 2026-07-02, L, S)

Gate 31 spawns a git subprocess per document (200-plus spawns, run twice per pre-push via the guard) and gate 40 is heavier; a batched `git log --name-only` pass would trade `--follow` fidelity for one subprocess. Optimization only; correctness unaffected.

### 3.9 Require-registration citation-currency gate (GR-GAP-1, guardrail review 2026-07-02, M-H, M; egress-gated)

Both currency gates are enumeration-scoped (`lint-standards-currency.py` flags only register-recorded patterns; `lint-citations.py` is a hand-curated denylist), so a standard absent from both is structurally ungated (the ISO/IEC 29134 wrong-year escape #162 + recurrence #482). Proposed: a gate extracting every `ISO/IEC NNNNN:YYYY`-shaped citation and failing on any standard-year pair not in the canonical register (require-registration, not deny-known-bad). Boundary: "present in the register" = current-OR-superseded, so a superseded-but-registered pair stays gate 6's finding (no double-fire), and each new pair carries gate-27 re-verification cost. **Register-gap VALIDATED 2026-07-06:** 17 cited pairs have no register row + a live `ISO/IEC 29134:2017`-vs-`:2023` inconsistency, so the gate cannot ship clean until the 17 rows are populated, and populating them accurately needs upstream confirmation (egress-gated, the same egress §3.2 waits on). A future egress session: populate the 17 rows, resolve the 29134 conflict, then build the gate. Gap detail in [`.working/design-decisions.md`](.working/design-decisions.md).

### 3.10 Fence-predicate consolidation (r5 guardrails, M, S)

The fence-toggle predicate exists in at least ten carriers in three variants, and six private copies are TILDE-BLIND (gates 54 and 58's linters, `lint-links.py`, `lint-changelog-link-coverage.py`, `lint-shall-near-uncertainty.py`, `lint-directional-dependency.py`), so a file pairing one backtick fence with one tilde fence passes gate 66 while a tilde-blind linter sticks in code mode to EOF (the GR-4 silent-suppression class surviving in the copies). Consolidate on a shared `is_fence_line()` predicate (or the iterator) in `lint_common.py`. Latent today (zero tilde fences in the census).

### 3.11 Gate-66 default-population shape call (r5 guardrails, L, XS)

Gate 66's default walk skips `.claude/`, but the mandated new-pack-prose `lint-language.py` run scans `.claude/` files via explicit paths with no exempt filter, so an unbalanced fence there suppresses that invocation's tail unseen (zero current findings). Options: widen the default population to include `.claude/` (keep `.working/` exempt), or add a checklist half-line to run gate 66 on the same explicit paths.

### 3.12 Bidirectional See-Also parity gate (r7 guardrails, M, M)

[`skill-authoring-discipline`](dev-security/claude-rules/skills/skill-authoring-discipline/SKILL.md) step 6 requires a new skill's `## See Also` "Related skill" links to be reciprocated, but no gate enforces it (gate 32 checks only `derives_from`, gate 41 the README tree, gate 44 PAIRS step-parity). The `publication-screening` delta reproduced the miss (fixed in-window in the 2.11 build). Proposed: a parity gate that, for each skill A whose See Also links sibling B as a "Related skill", asserts B links back to A. Directly mechanizable.

### 3.13 Expand the mutation-probe variant library, structured-surface gates (deep-assessment r1 R10 remainder, S)

[`tools/gate-mutation-variants.json`](tools/gate-mutation-variants.json) covered 5 gate classes (language, unbalanced-fence, secrets, links, metadata); the `/deep-assessment` coverage obligation wants each gate class to gain a phase-4 mutation-probe variant, and the library is designed to be extended run over run. **Extended in #768** with 2 append-testable classes, each a DETECT + CLEAN pair verified against the live gates: citation-denylist (`lint-citations.py`, `CSA CCM v5` detect / `CSA CCM v4.1` clean) and standards-currency (`lint-standards-currency.py`, `ISO/IEC 27001:2013` detect / `ISO/IEC 27001:2022` clean). **Remaining**: the structured-surface gates whose detection scans a SPECIFIC surface (not arbitrary appended prose), so an `append_file`/`create_file` payload to `@any-corpus-md` is not scanned by them: control-code (gate 49, the compliance matrix), retention-consistency (gate 55), and cross-doc-numbers. These need bespoke variants whose `create_file`/`append_file` action targets the exact surface the gate reads (e.g. a matrix-shaped fixture for gate 49), one careful variant per gate verified DETECTED by the probe before it lands. Incremental (run over run). **Advanced in #783** with a DETECT + CLEAN pair for the new gate-48 Check 5 (framework-as-column CCM/AICM family-validity, shipped #782): a `create_file` CCM-column fixture carrying `END-04` (probe verdict DETECTED) and one carrying valid `DSP-04, DCS-05` (CLEAN-PASS), both confirmed by `tools/audit-gate-mutation.py`. Check 5 is the one structured-surface check that IS `create_file`-testable, because gate 48 scans corpus-wide; the genuinely fixed-surface gates below (gate 49, the matrix; gate 55, retention pairs; cross-doc-numbers) still cannot be exercised by the probe's append-at-EOF / create-elsewhere actions (the mutation lands outside the gate's fixed target surface), so they need a probe-action enhancement (in-table insertion) that is a larger tooling change, kept for a future increment. Stays open (rescoped, not closed).

### 3.14 ETSI Securing-AI alignment map (L, M) (was 3.16)

Map the held ETSI SAI family (EN 304 223 plus the GR/TR set) against the corpus `ai/` security content: which requirements have no corpus carrier, which corpus claims an ETSI citation would strengthen, and a proposed alignment shape (options for maintainer scoping). Research DELIVERED (`inbox/worker-20260703-a/etsi-sai-alignment-research/`, 2026-07-04); the apply is a later decision. Citation form UNBLOCKED 2026-07-04 (the maintainer-supplied fresh EN 304 223 V2.1.1 copy; scratch PR #100).

### 3.15 MITRE ATLAS 2026.06 alignment and currency map (L, M) (was 3.17)

Coverage and identifier-currency map of the held ATLAS 2026.06 refresh against the corpus adversarial-AI content, with a proposed update shape. Research DELIVERED (`inbox/worker-20260703-a/atlas-adversarial-alignment-research/`, 2026-07-04). Pack-tree note (#654 verifier): a future `/matrix-fit`-style pass over the pack `dev-security/claude-rules/ai/` LLM02 rows should weigh the kept `AML.T0024` against `AML.T0057`.

### 3.16 CHANGELOG restructure: root reformat + compression (maintainer-directed 2026-07-08, M, M) (was 3.19 PR3+)

Mechanical reformat of the ~678 root `CHANGELOG.md` entries to the compact `**date | version | PR** - summary` format, then compress each historical entry to 1-2 sentences. PR 1 (gate-59 dynamic cutoff, the sweep tool, `.gitattributes export-ignore`, model write-up) and PR 2 (the initial sweep to `grc_library_scratch/archive/`, in-repo mirror pruned to the current week) are DONE (grc_library #708 + scratch #113). This is the remaining PR 3+. Note: the sweep tidies the working tree; true clone / fork cleanliness still needs the deferred history-collapse.

**Enhanced-simplification directive + scheduling (maintainer-directed 2026-07-11).** The maintainer confirmed the root `CHANGELOG.md` is currently too complex for standard readers (long, maintainer-grade lead paragraphs full of internal jargon: PR numbers, workstream codes like "WS 0.5", "FR-167", gate numbers). The target is stronger than the original compact-format plan: **enhance the simplification** so a standard reader (an adopter, not the maintainer) can understand each entry, plain-language and jargon-free, with the maintainer-grade detail remaining in the detailed mirror / git history. **Scheduling:** do this in the cleanup phase AFTER the next `/deep-assessment` (not in the current AI-workstream session); it is a large ~678-entry reformat best done on fresh context. Confirm the exact target format (how terse, whether grouped by release, how much plain-language rewriting per entry) with the maintainer at that time.

### 3.18 `/reference-audit` publications-bucket inclusion decision (post-build 2026-07-08, S) (was 3.20)

The `/reference-audit` skill excludes `grc_library_ref/publications/` by default (`--include-publications` only under an explicit screening decision). The screening process now exists; after the §3.20 screening wave, revisit whether `/reference-audit` should include screened publications in its default candidate set and how the tier ceiling treats them (likely recommendation-tier until a per-source trust decision).

### 3.19 Cross-repo worker-provenance link convention review (post-#715 `/validate-pr`, 2026-07-08, S)

The detailed-CHANGELOG `**Worker provenance:**` lines link the scratch-side manifest via a cross-repo relative target that resolves against a fresh scratch checkout at `main` but not a stale local tree, and cross-repo links are un-gate-checkable. Decide the durable convention: keep as-is (accept expected-fragile), convert to plain backticked text (no link), or another form; the decision affects prior entries and the gate-50 interaction. Not urgent.

### 3.20 Publications screening wave (post-2.11-build, 2026-07-09, S each, M total)

Work the 13 `pending` EDPB / WP29 rows in the reference base's `publications/SCREENING.md` register through `/screen-publications` (per-item screen: provenance + integrity, the instruction-content scan, corroboration of load-bearing claims against held texts), flipping each to `screened` (or `quarantined` / `discard-candidate`), recorded as `grc_library_ref` PRs through the ref validation gate. Partitionable worker research (apply through validate-then-apply). Cross-references §3.18 (the inclusion decision follows this wave).

### 3.22 D7 handoff-snapshot version-token check defeated by the #746 restructure (deep-assessment Sweep-92, S)

[`tools/check-handoff-snapshot-on-pr.py`](tools/check-handoff-snapshot-on-pr.py) (PR-time check D7) locates version tokens on the handoff's `Current truth` marker line, but the #746 restructure moved the tokens onto a separate `**Version snapshot (D7 validates these tokens):**` sub-line, so D7 validates 0 tokens and passes trivially. Fix: update D7's marker to locate the `Version snapshot` sub-line, re-confirm it flags a deliberately-stale token in a fixture, and keep the CLAUDE.md convention-guard note consistent.

### 3.23 New-jurisdiction/sector-annex discoverability checklist (deep-assessment Sweep-92, S)

A recurring multi-surface-incompleteness class: new jurisdiction/sector annexes (#733 US HIPAA, #743 EU AI Act) wired the primary surfaces but left sibling discoverability surfaces stale (decision-tree FAQ §7, decision-tree §3.3, register-coverage-gaps §2.5). Codify a new-annex discoverability checklist enumerating the FULL surface set a new annex must touch (README/doc-index, decision-tree §5.1/§3.3/FAQ §7, register-coverage-gaps §2.5, glossary, taxonomy/portal/scorecard). Convention-level (a CLAUDE.md close-out line or a worker-brief rail); no gate fits cleanly.

### 3.39 Dependabot refresh-companion for the SHA-pinned CI actions (R9 follow-on, maintainer decision, XS)

R9 (#767) SHA-pinned the two GitHub actions in [`.github/workflows/quality.yml`](.github/workflows/quality.yml) (`actions/checkout`, `actions/setup-python`) to exact commits with `# v4` / `# v5` comments. SHA-pins do not auto-update, so without a refresh mechanism they go stale and miss upstream security patches. Decide the refresh approach: add a `.github/dependabot.yml` for the `github-actions` ecosystem (weekly/monthly; keeps the SHA-pins current with low-noise PRs on a two-action docs repo) OR accept manual periodic bumps. Maintainer-owned because it adds repo automation (Dependabot PRs). Low urgency (the lint CI is read-only, `permissions: contents: read`, so the stale-pin blast radius is small). Surfaced building R9 2026-07-10.

### 3.31 `/reference-audit` per-touch staleness backstop (r6 guardrails, M, M; DEFERRED)

The gate-50-analogue for the per-touch reference-breadth obligation the [`.claude/CLAUDE.md`](.claude/CLAUDE.md) close-out checklist added (a corpus-body-touching PR runs the per-touch tool and refreshes [`.working/reference-audit/doc-state.md`](.working/reference-audit/doc-state.md)). Nothing detects a body-touching PR that omits the per-touch run or the state refresh (the class gate 50 backstops for `/validate-pr` rows). Proposed: a PR-time delta check (a Dn) failing when a PR's diff touches a corpus-domain `.md` body without a matching `doc-state.md` row update or a recorded empty-set note. **DEFERRED (maintainer 2026-07-08) until AFTER the first FULL `/reference-audit` run** establishes the `doc-state.md` delta-anchor baseline (building the hard D8 gate before the baseline exists would fire on the next corpus-body PR). Sequencing: first FULL `/reference-audit` run (populates `doc-state.md`), THEN build this D8. Convention-guarded meanwhile.

### 3.32 Count-vs-enumeration advisory candidate (r5 guardrails, L-M, S; close-candidate)

The figure-drift family's mechanizable subset: a delta-scoped advisory (not a gate) over added CHANGELOG/TODO lines flagging a spelled-or-numeral count that directly introduces a parenthesized enumeration whose marker count disagrees (the #636 five-vs-four shape). **ATTEMPTED and census-VETOED (2026-07-06):** the advisory was built and the full-history FP census run; it flagged 63 candidates with ZERO true positives (worst class: a parenthetical breakdown summing to the count, e.g. `5 findings (1 Critical, 2 Medium, 2 Low)`), because the count-vs-adjacent-enumeration match is not mechanically separable from correct prose. Per the bullet's reserved outcome the tool was discarded and we REST on the EXPEDITE (the #676 `Meta-prose state-claim measurement` recount clause). **Close-candidate on the maintainer's confirm** (kept open until then rather than dropped silently). Census evidence in [`.working/design-decisions.md`](.working/design-decisions.md).

### 3.33 Formalize the (severity, effort) convention across surfaces (S)

The `(severity, effort)` tags are in use in this file and the scale is now stated in the header, but the convention is not yet propagated to its sibling surfaces. When the convention formally lands, update: `library-fitness-review/SKILL.md`; `validation-sweep/SKILL.md`; the [`.working/DONE.md`](.working/DONE.md) heading shape; future fitness-review templates and sweep detail files. Schedule: after the current FR backlog closes.

### 3.34 Detailed-mirror markdown-link resolution check (log-mining #715, S)

[`tools/preflight-changelog.py`](tools/preflight-changelog.py) checks that added CHANGELOG lines are dash-free and that path-shaped references are WRAPPED as markdown links, but it does not check that each link TARGET RESOLVES; and the detailed mirror lives under `.working/` (gate-exempt), so the corpus broken-link gate (gate 3) does not scan it. A dangling relative-link target in [`.working/changelog-details/CHANGELOG-detailed.md`](.working/changelog-details/CHANGELOG-detailed.md) is therefore ungated. Proposed: extend `preflight-changelog.py` (or a companion advisory) to verify every bare-relative markdown-link target in the detailed mirror resolves against the repo, failing on a dangling target. Distinct from §3.19 (cross-repo worker-provenance links). Also closes the `.working/`-prose "bare-code-span / dangling-link" residue the hallucination-metrics ungated-residue note names. Mined 2026-07-10 (sweep94 log-mining pass).

### 3.35 Path-resolution fixture rail for path-enumerating gates (log-mining #634, XS)

A gate-building convention line: any new gate or check whose config enumerates live repo paths ships a path-resolution fixture that asserts every configured path exists and its parse target matches (the F6 class). Precedent: D7's `test_surfaces_table_paths_resolve_in_real_repo`. A small convention/test-rail line (worker-brief rail or CLAUDE.md gate-building note). Mined 2026-07-10 (sweep94 log-mining pass).

### 3.36 Improvement-log cycle-to-scratch mechanism (log-mining, maintainer-directed 2026-07-10, M)

The `/retro` register ([`.working/improvement-log.md`](.working/improvement-log.md)) grows one row per PR (~469 rows and counting) and accumulates a large aged-pending tail that is no longer useful for forward improvement once mined and dispositioned. Mirror the CHANGELOG sweep-to-scratch model (§3.16 and the change-tracking rule's current-week-model section): a tool that moves fully-dispositioned improvement-log rows older than a cutoff (below the TODO-mining cursor and past a date/PR window) into a `grc_library_scratch` archive, keeping the live register to a recent window; the aged rows stay recoverable but stop weighing on every session's mining. Pairs with the TODO-mining cursor added to the register 2026-07-10. Maintainer-directed at the sweep94 resume. Mined 2026-07-10 (sweep94 log-mining pass).

### 3.38 Broaden gate-39 count-idiom coverage (log-mining #272/#465, mechanizable half, S)

Extend the gate-count-consistency audit ([`tools/lint-gate-count-consistency.py`](tools/lint-gate-count-consistency.py), gate 39) count-idiom detection to catch more count-claim phrasings (e.g. `N audits`, additional spelled-word-form numbers) so a stale collection-count in those phrasings is caught mechanically, with a regression fixture per new idiom. This is the **mechanizable half** of the recurring #272/#465 improvement-log candidate. Maintainer disposition (2026-07-10): "do what we can, enhance where possible, drop what won't work": the mechanizable gate-39 idiom-broadening is pursued here; the **free-prose-rule-count half** (parsing an arbitrary `the N governance rules` prose sentence, which no count gate can reliably do) is inherently un-gateable and is **DROPPED** (recorded, not pursued). Scope to gate 39's existing pattern family; do not attempt free-prose parsing. Mined 2026-07-10 (sweep94 log-mining pass).

### 3.42 New-ingest reference-breadth pass: ISO/IEC 5259 + Canadian/international AI-governance sources (post-ref-resync 2026-07-10, M)

The standing post-PR `grc_library_ref` resync (maintainer-directed 2026-07-10) picked up newly-ingested held sources: **ISO/IEC 5259 parts 1 to 6** (Data quality for analytics and machine learning; 5259-1:2024 through TR 5259-6:2026) and new **Canadian + international AI-governance** source captures. Per the `/reference-audit` new-ingest cadence (mode 3, `--ref-since <sha>`), judge which corpus documents these newly-held sources topically match and do not yet cite. Known candidate: [`ai/procedure-training-data-governance.md`](ai/procedure-training-data-governance.md) already cites "ISO/IEC 5259 series" generically (now held) and could cite the specific relevant parts (e.g. 5259-3 data-quality-management, 5259-4 process framework, 5259-5 governance framework); the Canadian/international AI-governance captures are candidates for the `ai/` domain documents. Run `tools/audit-reference-breadth.py --ref-since <resync-sha>` to scope, then judge and apply per the reference-audit skill (trust tiers apply: standards citation-grade; screen any publications-bucket items). Surfaced by the post-PR resync 2026-07-10.

---

### 3.43 Gate-48: non-parsing-token check inside CCM/AICM-headed columns (`/retro` #784, design + FP-analysis needed, S-M)

The `/retro` for PR #784 surfaced the **4th invalid CSA control-code family this session** (`ISM` fixed in #769, `END` fixed in #781, `GVN` fixed in #782, and now the `AI-TM`/`AI-SC`/`AI-PP`/`AI-AU`/`AI-EC` pseudo-codes in `ai/standard-ai-and-agentic-development-security.md` §36). The first three share the well-formed-but-wrong-family `DOMAIN-NN` shape that gate-48 Check 5 (added in #782) now catches; the §36 family is a **distinct shape Check 5 is blind to by construction**: the `AI-XX-NN` pseudo-code has a hyphen before the domain token, so the gate-48 `CODE_RE` excludes it exactly as it excludes the corpus-internal `AI-GOV`/`MODEL-GOV` identifiers. It was caught by the high-assurance review, not a gate. Proposed: extend gate-48 (a Check 6, or widen Check 5) to flag, within a column whose header anchors to `CSA CCM` / `CSA AICM` (reusing `CCM_COLUMN_HEADER_RE`), any non-empty cell token that does NOT parse as a valid CCM/AICM code at all, with an allow-list for legitimate non-code cell content (prose notes, `n/a`, blank). The FP risk is the design work: a CCM/AICM-headed column can legitimately carry non-code prose, so the check needs a tight token-shape gate (only flag things that LOOK like a code, e.g. `[A-Z][A-Z&]{1,4}-\d`, but are not in `CCM_FAMILY`) rather than flagging every non-code cell. Ship guard-first with fixtures (a detect case for the `AI-XX-NN` shape, a clean case for a legit prose cell). Surfaced by the #784 retrospective 2026-07-10.

### 3.47 TODO adoptability: strip internal working-provenance annotations (S)

TODO items carry internal working-provenance that an adopter reading the backlog does not need and that clutters the file: date-stamped `maintainer-directed YYYY-MM-DD` tags, `Surfaced ... during #N` and `Mined ... (sweep N ...)` origin lines, PR-number and sweep-lineage annotations, and residual `(was X.Y)` renumber breadcrumbs. This provenance lives durably in git history, the DONE ledger, and the CHANGELOG; the forward-looking TODO should read as a clean, adoptable backlog of what remains. Sweep the open items to remove these annotations, keeping the actionable content, the stable id in each heading, and the `(severity, effort)` tag. Standing convention going forward: new TODO items omit date, PR, sweep, and maintainer-directed provenance.

### 3.50 Widen gate 69 to the "TODO item N.M" phrasing (S)

Gate 69 ([`tools/lint-positional-backlog-tokens.py`](tools/lint-positional-backlog-tokens.py)) matches "backlog item(s)" followed by a `§`/`P`-prefixed or dotted token, but its `TODO` arm requires the section token immediately after `TODO`, so the phrasing "TODO item 3.4" (qualifier + "item" + dotted token) is not matched. No live carrier exists today (corpus grep returns 0), so this is a latent gap, not a current defect. Widen the regex to also match the `TODO item N.M` form, with a false-positive analysis first (the "item" alternation must not over-match ordinary prose such as "TODO item list"), or document the omission as intentional.

### 3.53 Distribute the missing-reference-document SOP to the pack (S)

The missing-reference-document SOP codified in [`.claude/CLAUDE.md`](.claude/CLAUDE.md) (pause, attempt download+ingest to the reference base, else surface with named options) is project-specific; distribute its project-agnostic form into the [`evidence-grounded-completion`](dev-security/claude-rules/governance/evidence-grounded-completion.md) rule's external-source corollary (the pack-distributable governance form), so adopters inherit it.

### 3.54 Back-fill and surface the `doc_type` facet in grc_library_ref (maintainer-directed 2026-07-12, L, XL; meticulous, maintainer-collaborative, explicitly NOT automated)

Reference-base (`grc_library_ref`) follow-up. **Context (done, merged):** a `doc_type` facet was added to `grc_library_ref` (ref PR #57): an OPTIONAL, controlled document-type field in `catalogue.yml`, with a controlled vocabulary in `doc-types.md` (values: standard, guideline, framework, code-of-practice, report, regulation, program, template, questionnaire, book) enforced by `grc_library_ref/tools/validate.py`. It is ORTHOGONAL to the trust bucket an item sits in. It is currently populated on exactly ONE item (the ESA Joint Guidelines JC/GL/2024/34 in `frameworks/`, `doc_type: guideline`); the other 541 of 542 catalogued items are untagged.

**Scope (two coupled parts):** (1) Back-fill `doc_type` across the existing catalogue (542 items: standards 241, frameworks 132, legislation 74, publications 32, programs 25, books 22, templates 16). (2) Surface `doc_type` in a generated view (e.g. a "by document type" grouping in `INDEX.md`, which `build_router.py` generates). Part 2 is only worth doing AFTER part 1 has meaningful coverage; a facet view over one tagged item looks broken.

**Why careful and NOT automated:** many per-item judgement calls; classifying by title is a trap (ISO 31000 "Risk management, Guidelines" and the NIST SP 800-63 "Digital Identity Guidelines" series are formal STANDARDS by issuer, NOT `doc_type: guideline`) — classify by the issuer's instrument designation, not by a word in the title. A wrong tag is worse than an absent one: it silently corrupts any filter built on the facet. Some buckets are near 1:1 with `doc_type` (legislation->regulation, templates->template, programs->program, books->book) and add little value; the value concentrates in `standards/`, `frameworks/`, and `publications/`, which are also the most ambiguous. NO bulk sweep, NO scripted auto-classification. Approaches to WEIGH (not pre-decided): phased-by-bucket (near-mechanical buckets first, judgement buckets after) vs. populate-on-touch (tag items opportunistically as they are edited for other reasons).

**Process expectations:** LOW priority; schedule only when the maintainer has time to engage deeply. Expect roughly 20 clarifying questions up front, then MULTIPLE iterations of a written plan for maintainer review, with explicit maintainer sign-off BEFORE any catalogue edits are committed. This is `grc_library_ref` work, gated by ref's `tools/validate.py`; develop on ref's designated branch and merge per ref's ingest/merge SOP (cross-repo PR; the local git proxy 403s direct pushes to ref).

---

## Priority 4 — Adopter experience

Capability and guidance for organizations adopting the library, and the operator-experience tooling for running the project. Scheduled deliberately, after the fix/gap/cleanup tiers.

### 4.1 Corpus-management discipline as a shareable skill (M, XL)

Package the cumulative documentation-and-corpus discipline as a standalone Claude Code skill anyone managing a documentation corpus with an AI assistant could install. Distillation source: the thirteen `governance/` pack rules (discipline core), `validation-sweep` + `library-fitness-review` (periodic-review surface), the audit-programme architecture (mechanical-enforcement surface). Decided 2026-06-22: skill **family** (not omnibus), **prescriptive-only** (no linter scaffolds), **existing pack 1.x bump**. After the FR backlog closes. Depends on the §4.8 Pack adoption-hygiene programme: Phase 1 (GR-P2 condense) provides the distillation source, so this begins after Phase 1 merges.

### 4.2 Pack: dev-security/claude-rules language coverage review (M, M) (was 4.4-labelled)

Review the language-specific security rules in [`dev-security/claude-rules/`](dev-security/claude-rules/). The `languages/` tree already ships 11 baseline files, so the live work is the REVIEW of the existing subset (JS/TS + Go + Java decided) against `python.md`'s shape plus the positioning stance (explicitly point to OWASP cheat sheets rather than duplicate them), not greenfield authoring. Small PRs, one per subset file where the review finds a gap, or a README positioning update. (Related: the §4.8 Pack adoption-hygiene programme; this is a distinct language-rule quality pass and stays standalone.)

### 4.3 Overnight unattended-run driver (M, L)

An external driver loop (cron / CI / Agent SDK, outside the corpus) that launches a fresh `claude -p` or SDK session per task-unit, each reading `.working/session-handoff.md` + the TODO/DONE queue, doing one unit, committing, advancing the queue, and exiting. The durable-state layer exists; the missing piece is the driver plus an overnight runbook. Design questions: where the driver runs; merge authority for unattended worker sessions; the stop condition; needs-maintainer vs safe-to-continue signalling; interaction with the change-tracking rule's overnight-work protocol.

### 4.4 Worker-ready brief staging (slice 4) + `/subagent` external-worker entry (M, L)

The remaining build slice of the INPUT half of the multi-session capability: **the `/subagent` slash command** as the external-worker entry point (read the assigned brief, claim it in `claims-ledger.md`, read named main-repo files read-only, produce findings, deliver to `inbox/`, stop; **read-only-on-main enforced by the worker account's permissions, not the prompt**) plus the maintainer-facing quick start in the runbook. Slices 1/2/3/5 SHIPPED (whole backlog covered by staged briefs + verdicts; the close-out pairing line, `/resume` freshness check, and [`tools/audit-brief-freshness.py`](tools/audit-brief-freshness.py)). **Gating maintainer action**: provision the least-privilege worker account (read `grc_library` / write `grc_library_scratch` only). The apply stage stays single-session with full QA regardless.

### 4.5 Fork-facing guidance + scripts for building an own reference base (L, L)

Enable forkers to assemble their **own** reference knowledge base instead of depending on the maintainer's private `grc_library_ref` (which is NOT redistributed: it holds third-party reference works). Deliverables to scope at build: (1) a fork-facing guidance doc (where to obtain each cited standard from an authoritative source, the licensing posture, how to upload own copies); (2) the trust-model and tree convention mirroring the `grc_library_ref` model (standards/ trusted, publications/ assess-first, legislation/ version-sensitive, an ingest/ area, a catalogue); (3) helper scripts (scaffold the tree, fetch-from-reputable-source where a licence and stable URL permit, extract text for AI-readability, build/refresh the catalogue); (4) wiring notes (how a fork's base feeds the validator modules gates 48/49/54/58/61 build on, and `/matrix-fit`). Low urgency. Never bypass paywalls / licensing; treat downloaded `publications/` as untrusted until screened.

### 4.6 Fork update-assessment tooling (upstream-change applicability report) (S-f, maintainer-requested 2026-07-04, M-L)

When an adopter's customized fork pulls upstream `grc_library` updates, nothing today helps THEIR AI assistant assess each upstream change against the fork's local customizations and present an accept/adapt/skip decision matrix. Design a fork-side instrument: likely a shareable skill (diff upstream release-to-release, classify each change by carrier class, map against the fork's recorded local divergences, produce the per-change report), plus upstream-side enablers where cheap (machine-readable change-class tags or per-entry applicability hints). Shape and upstream-vs-fork-side split are maintainer-scoped at design time.

### 4.7 RESUME.md maintainer-internal label (deep-assessment r1 R13, XS)

[`RESUME.md`](RESUME.md) sits at the adopter-visible repository root but is purely maintainer-internal (it points into `.claude/` and `.working/`, trees the adopter corpus excludes) and carries no "not an adopter document" signal. Add a one-line "(maintainer-internal; adopters can ignore)" note, or list it in the README maintenance-file table with that framing. Low priority; design choice.

### 4.8 Pack adoption-hygiene programme (phases 1-4) (GR-P2 + GR-P5 + pack-design GR-P3/GR-P4, phases 1-2 OVERNIGHT-AUTHORIZED, phase 3 worker-gated, M, XL) (consolidates the former GR-P5 residual item)

**AUTHORIZED to proceed (maintainer 2026-07-12): phases 1-2 are OK to apply overnight; the HOLD is lifted for the overnight session.** Apply from the consolidated scratch drop now merged on scratch `main` at `inbox/claude-pack-hygiene/` (entry `MANIFEST.md`, then `MASTER-PLAN.md` with the phase status board), NOT the removed old drops (`gr-p2-rule-condense*` / `pack-design-gr345-batch`, superseded and removed scratch-side). Phases 1-2 are apply-ready and worker-tested; note GR-345's GR-P3/P4/P5a content is ALREADY APPLIED via #727, only its GR-P5b section stays live (used by phase 1). Apply phases 1-2 through the normal serial-apply + per-PR QA + skeptical-verifier pipeline (these are protected `.claude/` + `dev-security/claude-rules/` pack edits, local-instance-authorized).

**Phase 3** (rules-scrub + PROJECT-OVERLAY architecture: pack-design GR-P3/GR-P4 + the pack governance-rule scrub) is built by the pack-hygiene WORKER on the merged post-phase-1 base; the worker is gated on the maintainer's explicit ping and will NOT self-start.

**STANDING REMINDER OBLIGATION (maintainer-directed 2026-07-12).** **Remind the maintainer IN THE MORNING to have the pack-hygiene worker continue phase 3 of the hygiene tasks.** The worker stays idle without the ping; surface the reminder prominently at the morning boundary rather than assuming it is remembered.

The pack adoption-hygiene work (making [`dev-security/claude-rules/`](dev-security/claude-rules/) adoption-clean for distribution) and the GR-P2 operative-core condense are one phased programme:

- **Phase 1, GR-P2 condense apply.** Two-layer operative-core / on-demand-rationale split across the 13 governance rules per the PR #441 method, with the removal ledger [`.working/claude-rules-considerations.md`](.working/claude-rules-considerations.md); KEEP a compact framework-alignment table in each condensed rule; `lint-language` on each before first commit. Tranche 1 shipped 2026-07-09 (method + ledger + `gate-discipline.md` condensed, keeping the operative core + framework table); tranches 2-12 are folded here (they proceed on the maintainer-confirmed keep-the-table direction). Phase-1 folded-in fixes: (a) migrate the pack-wide `LOG-02, LOG-08` audit-trail-row convention to `LOG-02, LOG-04, LOG-10` (LOG-08 "Audit Logs Sanitization" is a mis-fit; LOG-04 + LOG-10 fit; bare-token census first) and swap the apex rule's Integrity-row `A.8.34` to `A.5.33`; (b) reconcile the change-tracking rule's two-file-split "same lead-paragraph wording" text to the divergent-lead practice (#560).
- **Phase 2, tested sync-gate + skills + README payloads apply.** The new tested pack-to-project sync gate, the skills payloads (including the former **GR-P5** derived-skill coverage gap item: `validate-inference-before-action` and `surface-counterproductive-instructions` have no derived skill; GR-P5a re-point shipped, GR-P5b folded into Phase 1, GR-P5c confirmed no-op at #713), and the README payloads.
- **Phase 3, rules scrub + PROJECT-OVERLAY architecture** (the worker builds this only AFTER Phase 1 merges). The pack-design **GR-P3** (third-occurrence-to-gate escalation) and **GR-P4** (overlay primary-wins pointers + pruning stance) deliveries, plus the pack governance-rule scrub for adoption-cleanliness.
- **Phase 4, acceptance sweep, close-out, and routed-findings triage.**

Dependency re-pointed here: §4.1 (corpus-management shareable skill; its distillation source is the condensed rules, so it begins after Phase 1 merges). The public-site item is not in this TODO yet (a maintainer scratch-side item, not yet tracked); it will reference this programme when it lands here. The GR-P design staging in [`.working/deferred-protected-changes.md`](.working/deferred-protected-changes.md) item 6 feeds this programme and is likewise on hold.


---

## Priority 5 — Expand: country / regulator / programme overlays

Adding new coverage to existing domains. Each subitem is a separate small or medium PR; the maintainer schedules deliberately.

### 5.2 Logistics country / programme expansion (was 5.1)

The WCO AEO Compendium identifies ~94 trusted-trader programmes globally; the library covers 4 (BASC, CTPAT-US, AEO-UK, PIP-Canada). Highest-priority additions: EU AEO (27 member states under EU UCC Art 38), Mexico NEEC / OEA, Australia Trusted Trader, Singapore STP / STP-Plus, Japan AEO, Korea AEO, New Zealand SES, Brazil OEA, China AEO.

### 5.3 Financial-services country regulator overlays (was 5.2)

Within `compliance/financial-services/`: UK PRA / FCA; US OCC / FRB / FDIC / SEC / FINRA; Canada OSFI; Australia APRA; Singapore MAS; Japan FSA.

### 5.4 Healthcare country regulator overlays (was 5.3)

Within `compliance/healthcare/`: EU MDR / IVDR (full text now held in the reference base); Canada PHIPA and provincial frameworks; Australia My Health Records Act; UK NHS DSPT. (The US HIPAA bullet closed in #733.) The remaining bullets stay source-gated except EU MDR/IVDR, which is a delicate build queued for a fresh session's context.

### 5.5 Energy and utilities country regulator overlays (was 5.4)

Within `compliance/energy-and-utilities/`: US NERC CIP standards; US TSA pipeline cybersecurity directives; UK Ofgem cyber requirements; EU ENISA sectoral guidance.

### 5.6 Telecommunications country regulator overlays (was 5.5)

Within `compliance/telecommunications/`: EU EECC; UK Ofcom telecom security framework; US FCC regulations; Australia ACMA requirements.

### 5.7 Public-sector country / regulator overlays (was 5.6)

Within `compliance/public-sector/`: UK Government Cyber Security Strategy and GovAssure; Australia ISM and PSPF; Canada IT Standards for federal departments. (The EU eIDAS bullet closed in #739.) The other bullets stay source-gated.

### 5.8 Privacy jurisdiction gaps (was 5.7)

Existing privacy domain covers 26 country annexes. Known gaps or stale entries: Argentina (PDPA 2025 update pending); Saudi Arabia PDPL (recent updates pending); re-review of EU member-state derogations where applicable. (Mexico's standalone annex shipped in #750.) The Argentina and Saudi bullets stay source-gated.

### 5.9 AI jurisdiction overlays (was 5.8)

The `ai/jurisdictions/` subdirectory and its first two annexes (EU AI Act #743, Colorado #749) shipped under the former FR-62. Remaining candidates, source-gated pending maintainer drops: Canada AIDA; UK AI policy framework; NYC bias audit law; China generative AI rules; Korea AI framework. **Also here (deep-assessment r1 R1, S):** the privacy jurisdiction-index Colorado summary-lag at [`privacy/annex-privacy-jurisdiction-index.md:104`](privacy/annex-privacy-jurisdiction-index.md) (the US-row cell headlines the superseded 2026-06-30 effective date; the operative forward regime the full annexes carry is SB 26-189, consequential decisions on/after 2027-01-01). Refresh the cell to name the SB 26-189 / 2027 regime, or accept as an intentional one-line summary.

---

## Priority 6 — Expand: new domains

Entirely new domains, multi-week scope each. The maintainer schedules deliberately. Ordered lowest-effort-first.

### 6.1 Identity-specific content depth (L) (was 6.2)

Customer Identity (CIAM) governance, workforce identity governance, identity federation patterns, passwordless adoption playbooks. Scoping research DELIVERED, with three proposed documents briefed as follow-on work-units in scratch (`research/ciam-governance-research/`, `research/identity-federation-patterns-research/`, `research/passwordless-adoption-research/`, grounded in held NIST SP 800-63-4); the BUILD stays maintainer-schedule-gated.

### 6.2 Quantum cryptography readiness deepening (L) (was 6.3)

The phase-level PQC roadmap exists but not detailed implementation content. Pending: a PQC migration playbook, crypto-agility patterns, post-quantum-ready CA/PKI. Corpus-internal scoping DELIVERED (`inbox/worker-20260703-a/quantum-pqc-readiness-scoping/`); the regime half is source-gated (no PQC standard held) and the BUILD schedule-gated.

### 6.3 Cross-framework matrix expansion (L) (was 6.4)

Expand [`governance/matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md) to additional sectoral and regional frameworks as the P5 content grows. **Also here (deep-assessment r1 R3, S):** SOC 2 Type II is named as a target attestation corpus-wide (templates, glossary, assurance map) but no matrix maps SOC 2 Trust Services Criteria to library documents and [`governance/register-coverage-gaps.md`](governance/register-coverage-gaps.md) §3 does not disclose SOC 2 as an undetailed framework (it discloses PCI DSS, SWIFT CSP, etc.). Add a SOC 2 (TSC) row to §3 with a Status/Planned-target; optionally add SOC 2 CC-series to the reverse crosswalk.

### 6.4 CMMI capability levels alongside maturity levels (L) (was 6.5)

Low priority, after the FR backlog. Add a capability-level scheme (0-3 per practice area) alongside the 5-tier maturity levels: update [`governance/framework-governance-performance-and-improvement.md`](governance/framework-governance-performance-and-improvement.md) §2, [`docs/template-maturity-self-assessment.md`](docs/template-maturity-self-assessment.md), possibly the DTI thresholds. Research-only integration mapping DELIVERED (`inbox/worker-20260703-a/cmmi-sei-maturity-integration/`, four integration-shape options).

### 6.5 Multi-cloud governance overlay (XL) (was 6.1)

Per-cloud hardening baselines for AWS/Azure/GCP exist; the gap is multi-cloud governance (cross-cloud risk taxonomy, cross-cloud incident coordination, portfolio-level controls). Could live in `operations/` or a new `cloud/` domain. Scoping DELIVERED (`inbox/worker-20260703-a/multi-cloud-governance-scoping/`).

---

## Priority 7 — Awaiting maintainer decision

### 7.1 Ruleset `non_fast_forward` (force-push) rule (deep-assessment r1 R8b, maintainer-owned)

The "Main Protection" repository ruleset enforces PR + status-check + signatures + no-deletion, but carries no explicit force-push (`non_fast_forward`) rule; the PR requirement makes direct pushes impossible, so this is low-priority hardening. A maintainer-owned GitHub setting, not a repo change: add the `non_fast_forward` rule to the ruleset if desired.

### 7.2 Per-regulation context (FR-104)

Per-regulation context not pursued (dropped-decision audit-trail record; see [`.working/design-decisions.md`](.working/design-decisions.md)).

### 7.3 Portal reorder (FR-130)

Portal reorder not pursued (README stays at decision-tree item 1; dropped-decision audit-trail record).

---

## Reference-base work (`grc_library_ref`)

Validated defects / standing work in the reference repo. The one remaining OPEN in-repo item (SR-1) ships as a `grc_library_ref` PR via `gh`.

### SR-1 `last_checked` currency mechanism is inert (item 26, P2, S)

As of 2026-07-05, 5 of 240 `grc_library_ref` `catalogue.yml` items carry a `last_checked` field, and `grc_library_ref`'s `tools/validate.py` checks the field's FORMAT only if present (no presence requirement), so the 7-day-throttle currency discipline has no on-disk footprint for the unstamped items. **Direction DECIDED** (maintainer 2026-07-02): presence + backfill (backfill stamps on the currency-sensitive buckets, then add a presence/due-item check). **Execution egress-gated:** an honest backfill needs a per-document upstream currency check (the same class the §3.2 / §3.9 reference-currency residuals wait on; the older 51-row register sweep is itself discharged). Held for the maintainer's egress instance.

### RB-R6 source-not-held acquisition (deep-assessment r1 R6, maintainer research-agent, S)

Sources cited in the corpus but not held in `grc_library_ref`, so their attributions cannot be adjudicated against held text. The maintainer runs this via a research agent that presents download URLs of the PDFs to fetch and ingest (the assistant cannot download them: iso.org is 403 from the VM and ISO standards are paywalled). Sources to acquire:

- **ISO 37301** (Compliance management systems), Clauses 4-10 — cited at [`compliance/policy-compliance-and-audit-management.md:44`](compliance/policy-compliance-and-audit-management.md) ("Clauses 5 to 10"). Upstream: iso.org/standard/75080.html (paywalled).
- **ISO 9001** (Quality management systems) §9.3 — cited at [`governance/framework-governance-performance-and-improvement.md:55`](governance/framework-governance-performance-and-improvement.md). Upstream: iso.org/standard/62085.html (paywalled).
- **DORA RTS on incident reporting** (the Commission Delegated Regulation carrying the 4h / 72h / 1-month major-incident windows) — cited at [`compliance/financial-services/annex-dora-implementation.md:78`](compliance/financial-services/annex-dora-implementation.md) (already correctly qualified "subject to RTS/ITS", so NO corpus change; this is a value-verification tracker only). Upstream: EUR-Lex (the DORA Art 20 delegated instrument, likely freely fetchable, unlike the ISO standards).

On ingest, the ISO 9001 §9.3 attribution in [`governance/framework-governance-performance-and-improvement.md`](governance/framework-governance-performance-and-improvement.md) (reworded to the safe "planned intervals" framing in PR #758) and the ISO 37301 attribution at [`compliance/policy-compliance-and-audit-management.md:44`](compliance/policy-compliance-and-audit-management.md) can be adjudicated against the held text.

### Reference-base acquisition and assessment queue (`grc_library_ref`; maintainer-directed 2026-07-07)

RB-1 (PCI), RB-2 (staging_ref ISO/CIS), RB-3 (NIST CSRC harvest, ref PRs #5-13), RB-4 (OWASP, ref PRs #14-19 + #22), RB-5 (MITRE, ref PR #20), and FedRAMP (ref PR #21) are COMPLETE (rotate to DONE at the cross-repo morning-processing). Standing watch:

- **RB-6 reference-base currency + draft watch**: standing watch on items whose upstream has a pending revision. (a) Planned-but-unpublished NIST revisions (FIPS 202/203/204/205; FIPS 198-1 -> SP 800-224 draft; SP 800-131A Rev 3 IPD; SP 800-38D; SP 800-46 Rev 3; SP 800-90A Rev 2) — re-check on finalization. (b) Draft-watch (NIST IR 8596 Cyber AI Profile; SP 800-53 COSAiS AI overlays; Privacy Framework 1.1 CSWP 40 IPD). (c) Controlled-vocabulary gap: `grc_library_ref/topics.md` has no `cryptography` tag (the ~15 held crypto standards map to `cybersecurity` only); assess adding one. (d) FedRAMP 2026 evolving-preview: establish a re-snapshot cadence when the daily-updated Public Preview stabilizes.

---

## Standing conventions

Durable behavioural guidance from the maintainer. NOT actionable items; reference material for the orchestrator and future contributors.

- **"More PRs, keep each one clean"** — favor small focused PRs.
- **"One item, one functional action"** (2026-07-10) — split TODO items per distinct resolution path; group bullets under one number only when they resolve as a single action.
- **"I prefer /validate, not /validation-sweep"** — short slash commands; skill names stay descriptive.
- **"Don't explicitly name or link `.working/`"** in template-content files that adopters see.
- **"Inference must be validated before committing or before anything else uses that information"** — operationalized in [`validate-inference-before-action.md`](dev-security/claude-rules/governance/validate-inference-before-action.md).
- **Activity directories should be self-contained** — the canonical `.working/<activity>/` layout.
- **Zero-finding sweeps still need history rows but no detail files** — validation-sweep [`SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) step 9.
- **Sweep history is project-application, not template content** — operationalized by keeping the history file in `.working/`.
- **TODO is forward-looking; historical state rotates to DONE.md** — [`change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md).
- **After completing a merge, list the upcoming next 5 planned PRs from TODO** — [`.claude/CLAUDE.md`](.claude/CLAUDE.md) PR-workflow section.
- **Validate cadence is 1-8 PRs per batch, not strictly 5.**
- **DONE format mirrors TODO format** — DONE H3 headings carry `FR-N (severity)`.
- **Compute-don't-ask** — before surfacing a question, apply a "can I compute/verify this myself?" gate; codified into `clarify-before-acting`.

---

## Notes on maintenance

- Add new items at the appropriate priority; within a section keep lowest-effort-first. Move items between priorities as context changes.
- When an item is completed, delete it (no strikethroughs, no `[done]` suffixes) and add a [`.working/DONE.md`](.working/DONE.md) entry in the same PR. Rotation discipline: the PR-finalization-protocol section of [`.claude/rules/governance/change-tracking.md`](.claude/rules/governance/change-tracking.md).
- Design decisions belong in [`.working/design-decisions.md`](.working/design-decisions.md), not TODO.
- This file is the source of truth for what's queued; conversation history is not.
- Fitness-review backlogs remain the authoritative per-finding evidence source; this file is the action-organized view.
