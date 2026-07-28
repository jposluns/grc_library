# TODO

Forward-looking backlog of planned enhancements for the GRC Documentation Library. Items are added when identified and rotated out when completed. Completed items move to [`.working/DONE.md`](.working/DONE.md) (closed-TODO ledger, keyed by original backlog ID); historical change detail lives in [`CHANGELOG.md`](CHANGELOG.md). This file holds only pending and queued items.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions, with one narrow exception: [`tools/lint-todo-staleness.py`](tools/lint-todo-staleness.py) (gate 45) scans this file for the queued-PR-already-merged drift shape (its companion sweep-cursor-behind-history check reads the resume cursor from [`.working/session-handoff.md`](.working/session-handoff.md)). The intra-document section-reference gate also scans it. Other audit gates skip this file.

**How items are numbered and formatted.** Items are grouped by priority (P1-P7), tiered by work type (maintainer's 2026-06-30 leaning): P1 fix errors and prevent recurrence, P2 fill significant gaps, P3 clean up and tooling, P4 adopter experience, P5-P6 expand the corpus (overlays, then new domains), P7 awaiting decision. **Every item is a `### N.M` subsection; the leading digit is the priority the item was created under** (so a newly-created P3 item is `3.x`; a re-tiered item keeps its original number, so its leading digit records its priority-at-creation, see the permanent-numbering rule below); within a section items run lowest-effort-first. **One item is one functional action / one distinct resolution path** (maintainer-directed 2026-07-10): multiple bullets sit under one number only when they resolve as a single action (same file, same fix, one commit); otherwise they are split into separate numbered items. The `N.M` number is a **permanent id that is never recycled** (maintainer-directed 2026-07-15): each priority section carries a **`Next item number:` counter** stating the next number to assign, and every edit that adds an item (including an item split out of a larger one) draws that number and advances the counter, so one number maps to exactly one item across the whole history of the file and a lookup by number is unambiguous. A closed item's number retires with it and is never reused; existing items are never renumbered when the file is reorganized (renumbering would break the CHANGELOG, DONE, and handoff references that point at them), so a re-tiered item keeps its original number and its leading digit then records the priority it was created under rather than its current section. **Series-consolidation redirect-stub (maintainer-directed 2026-07-23):** when an item's CONTENT is consolidated into a series (relocated under a series umbrella as a new child `X.Y.Z`), the original number `A.B` is neither reassigned nor deleted: the content moves to `X.Y.Z`, and a one-line REDIRECT STUB is left at `A.B` (`### A.B <title>: moved to X.Y.Z (Series ...); content lives there; this stub closes when X.Y.Z closes`). This preserves the never-reassign guarantee, `A.B` still resolves, now as a forwarder, so any reference the same-PR sweep misses lands on the stub and is forwarded, while letting the series read in execution order. The stub holds no content of its own (single source at `X.Y.Z`, no dual-copy drift); the obvious live references (handoff, next-prs, cross-file `§`-refs) are still swept to `X.Y.Z` in the same change (the stub is the backstop for missed ones, not a licence to skip the sweep); and the stub and `X.Y.Z` rotate to DONE together when `X.Y.Z` closes. The heading's `FR-N` / descriptive identifier remains a stable secondary id; the older `(was X.Y)` renumber-breadcrumb practice is discontinued (existing breadcrumbs stay for resolvability), and the redirect stub is its forward-pointing successor for the consolidation case (a breadcrumb pointed backward from the new location; a stub points forward from the old location and stays live until close). **Multi-phase-project series (maintainer-directed 2026-07-26):** a project with distinct phases takes the next umbrella number `N.M` as a GOAL-DESCRIPTION heading (not itself a doable task), and its phases are `N.M.Y` children that are the actual work, each INDEPENDENTLY closeable and never bundled (`N.M.4` may close before `N.M.3`). The umbrella consumes ONE counter number (advancing `N.M` to `N.(M+1)`); the `.Y` children do not consume top-level numbers; each child rotates to DONE as it closes, and the umbrella closes when its last child does. This is the CREATE-as-series form; the Series-consolidation redirect-stub above is the MOVE-existing-content-into-series form. The `## Reference-base work` section is not an `N.M` section; its `SR-N` / `RB-N` coded ids likewise never recycle. Each heading carries `(id, severity, effort)` where severity is `H[critical]` / `H` / `M` / `L` / `FYI` and effort is `XS` / `S` / `M` / `L` / `XL`. A `⚠` marks a persona-quoted finding to verify at action time.

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

**Next item number: 1.27.**

Correctness fixes and the **error-prevention tooling** that keeps the corpus from regressing.

P1 currently holds two standing machinery/guardrail items (§1.14, the external-source currency detection mechanism; and item 1.19 (closed 2026-07-25), the operational-state privatization + adopter-clone portability multi-phase spec), alongside short-lived point-fix items opened and closed here as errors surface (none open at present; §1.20 and §1.21 both closed 2026-07-18, §1.1, the discussion-vs-execution mode gate, closed 2026-07-24 as the fifteenth pack rule `express-authorization-before-execution`, and §1.18, the change-impact surface map, closed 2026-07-24 with its two core deliverables shipped, the surface map in #1104 and the first FP-safe gate 74 in #1107). Its earlier correctness and reference-currency residuals (§1.5 through §1.11) are all closed (the version-currency register shipped in #505; the `needs-reconfirm` sweep ran in #751; the completion-guard, file-type-width, and ref-side items closed through #818). New P1 items are added here as errors or recurrence-risks surface; the routine cadences above are the ongoing preventive half.

### 1.26 Consolidate, harmonize, and distribute the quality machinery across AI toolchains (goal-description umbrella; multi-phase series; maintainer-directed 2026-07-26; ON HOLD pending all Priority 3 tooling)

**ON HOLD until every Priority 3 tooling item is complete.** This series deliberately follows the P3 cleanup-and-tooling wave rather than racing it: the machinery it consolidates is still actively growing there, so starting sooner would consolidate a moving target and immediately re-fragment. When P3 closes, this is the capstone that makes the accumulated machinery coherent, portable, and shared.

The quality system (the audit gates, the PreToolUse hooks and guardrails, the `tools/` scripts, the pack rules and skills) has grown fast and organically, one control at a time, each earned by a real failure. That growth is the system working, but it has left overlap, near-duplicate checks, conventions layered several generations deep, and structure that no longer reads as designed. And the work is no longer the maintainer's alone: many of the team, and some adopters, now run the library on local and custom models, and under the CC BY-SA ShareAlike licence they have submitted their own improvements and suggestions back. This series is where the machinery is made sound and where those contributions are brought home: consolidate and simplify what has accreted, integrate what the community has sent back, reconcile the in-project practice with the public pack, and distribute the result in the idiom every team member's toolchain speaks. The umbrella here is the goal; its phases below are the work, each independently closeable.

### 1.26.1 Consolidate and simplify the in-project machinery (H, XL)

Deduplicate and simplify the gates, guardrails, and tooling: fold overlapping checks together, retire superseded ones, and tighten the seams so each job is done once and done well. Improve efficiency so the per-PR and per-session machinery costs less time and fewer hand-synchronized edits. Verify the structure is sound, that the controls compose into a coherent whole rather than an accreted pile, with each layer's role clear. This is the foundation the rest of the series builds on, so it lands first.

### 1.26.2 Integrate the community's ShareAlike contributions (H, L)

Many of the team and some adopters have implemented the library on local and custom models and, per the CC BY-SA ShareAlike licence, submitted their improvements and suggestions back. This is where those are all integrated: triage each contribution, validate it against the project's standards, and fold the accepted ones into the machinery and the pack, credited per the licence. The submissions from real-world local-model use are also the sharpest signal for what the tool-agnostic distribution in 1.26.4 must get right.

### 1.26.3 Reconcile with the public pack for true parity (H, M)

With the machinery made sound and the community input folded in, reconcile it with the public `dev-security/claude-rules/` pack so the distributed pack is at true parity with the disciplines the project actually runs, closing any drift the pack-parity coupling has not yet caught. One coherent set of rules, tools, and reference material, identical between what is dogfooded here and what is shipped.

### 1.26.4 Distribute in aligned forms across AI toolchains (H, XL)

Broaden distribution beyond a single tool: ship the harmonized pack in aligned forms for the other AI coding tools the team uses (Codex first, then the rest) and a generic, tool-agnostic form usable by local and custom models, which a growing share of the team now runs. The end state is one deduplicated, efficient, community-informed quality system, dogfooded here and distributable anywhere, so any team or adopter, on any AI toolchain, inherits the same hard-won guardrails in the idiom their tool speaks.

### 1.23 Trust-recovery build: validation-coverage + deep-assessment coverage of unvalidated operations (maintainer-directed 2026-07-24, H)

Triggered 2026-07-24 when the orchestrator direct-pushed to `grc_library_private` without validation (no PR, no CI-watch) and its `validate.py` CI was red all day unnoticed until the maintainer flagged the failed-CI emails; a whole operation class bypassed the validation applied everywhere else. Immediate fixes DONE: the 2 `_private` validate failures corrected (CI green); the maintainer set require-PR + block-force-push on `_private`; the `_private`-validate-before-every-push discipline codified in `orchestrator-claude.md`. **Build (maintainer GO 2026-07-24):** (1) **DONE #1147:** `tools/audit-validation-coverage.py`, a cross-repo advisory (per repo: validating-CI-present + direct-push landings on a PR-required repo as the ungated signal, via the commit-to-PR association; assistant token 403 on branch-protection reads so enforcement is maintainer-verify; self-test wired into the regression suite). (2) **DONE #1148:** restructured `/deep-assessment` to bring `_private` into scope (Project-wiring sibling set, phase-1 present check, phase-2 gate, and a new phase-6(d) semantic review of its load-bearing operational docs), wired the coverage tool as a phase-4(e) sub-pass (KEY INSIGHT: deep-assessment examines artefacts and gates, not the operation log, so an unvalidated-operation class is invisible by construction), and added a Parallel-execution subsection making every phase worker-splittable (the phase-2 barrier plus orchestrator-only private-store units). (3) **`_ref` protection (maintainer-action):** the coverage tool found `_ref` currently allows direct-pushes (2 maintainer web-uploads landed direct); protect `_ref` (require-PR + block-force-push) like `_private` so the assistant can never direct-push there unvalidated. (4) **DONE #1164:** the `.claude/CLAUDE.md` em-dashes cleaned. The recorded figure of 26 was right and resolved as **25 prose violations plus 1 legitimate**: the survivor at `:182` is the house-style rule's OWN backticked illustration of the forbidden characters, which must not be changed, so `lint-language.py` on that file now reports exactly that one finding and nothing else. Prose dashes became colons (the definition-list idiom the rule-index and pointer lists use) or a comma in one list continuation. **Remaining: item (3) only, which is maintainer-action** (protect `_ref` with require-PR + block-force-push like `_private`; the assistant's token 403s on branch-protection reads, so it cannot verify or set it).

### 1.19.13 History scrub (Phase 6; deferred, maintainer-gated; H, L)

**SCOPE AMENDED 2026-07-25:** absorbs item 3.16's (closed 2026-07-25) CHANGELOG-history-collapse path-set, which
closed as absorbed. The two are the same operation on different content and share every expensive and
risky part, so if a rewrite ever runs it runs ONCE covering both. **Sequenced AFTER the tooling
catch-up** (maintainer, 2026-07-25); still gated, still reserved for the narrow causes the
artefact-and-branch-discipline rule names.
The git-history purge of the moved operational docs (worklist = the 1.19.8 move-list), per the artefact-and-branch-discipline force-push procedure: document the reason, obtain approval, notify collaborators, preserve the pre-rewrite ref under `refs/preservation/`, re-run version-monotonicity. The REAL purge (the move alone leaves content in public history, per #1 LOCKED). LAST. **PREP (2026-07-18 overnight, #1014):** the force-push history-scrub procedure is drafted at `grc_library_private/history-scrub-procedure-draft.md` (precondition gate + worklist = the 1.19.8 move-list + the artefact-and-branch-discipline steps + residual-risk note). Remains deferred, maintainer-gated, and LAST; execute only after 1.19.8/9 land and with explicit authorization.

### Egress Gated

Items below need an egress-enabled fetch the assistant cannot perform, so they are parked here at
the end of this priority section rather than interleaved with actionable work. **Item numbers are
unchanged**: position carries no meaning, the number is permanent. Every source these items need is
listed in the `_private` maintainer-egress request so it can be batch-downloaded in one pass.

### 1.22 Privatization / guardrail tightening (maintainer-directed 2026-07-19, this-session block, outranks the queue; H, M)
A cohesive block the maintainer surfaced at the 2026-07-19 `/resume`, tightening the the item-1.19 privatization (parent closed 2026-07-25) and adding cross-repo guardrails.
- **1.22.8 Chat text-pacing / read-pause convention (maintainer-directed 2026-07-19; DISCUSS TOMORROW; maintainer-gated).** Recurring problem the maintainer flagged: assistant chat scrolls past too fast to read ("you scrolled text so fast i didn't see anything else"), so answers are missed. The maintainer's existing mitigations are the AskUserQuestion multiple-choice UI (per memory) and the IMPORTANT: marker. Design a durable text-pacing convention so a maintainer-facing answer is readable before the next output scrolls it away (candidates: a pause/acknowledgement gate after answering a maintainer question; shorter chunked messages; a "press to continue" affordance; surfacing key points via AskUserQuestion so they hold on screen). Needs the maintainer's input on the preferred mechanism, so DISCUSS at the next attended boundary before building.
- **1.22.9 Canada.ca AI/privacy-suite egress URLs (maintainer-directed 2026-07-19; overnight action).** Add the DIRECT download URLs for the Canada.ca AI-governance + privacy suite (the 2.25.3 sources, the item formerly at item 2.22 (closed 2026-07-25): TBS Directive on ADM, AIA tool, the AI guides, Guiding Principles, FASTER, GC AI Register, the Voluntary Code; Privacy Act, OPC Fair Information Principles, OPC retention/disposal, the Breach of Security Safeguards Regulations, the TBS Policy on Privacy Protection) to the `_private` maintainer-egress-requests list, since canada.ca is WAF-blocked for automated fetch. Verify each URL (do NOT fabricate; use WebSearch to confirm the canonical canada.ca path, mark any unconfirmed for the maintainer). The maintainer downloads them into `grc_library_ref/ingest/`, then 2.25.3 proceeds. This is the concrete seed for the §1.22.7 egress-gated section's Canada rows.

## Priority 2 — Fill significant gaps

**Next item number: 2.29.**

Deepening thin-but-present content to operational sufficiency, and the significant missing capabilities.

### 2.1 Privacy jurisdiction annex operational deepening (FR-59, H, L)

Privacy jurisdiction annexes are too shallow for operational sufficiency; deepen the remaining source-gated country annexes to operational level. Japan, United States, Canada, and Brazil are deepened (2026-07-04 held-source batch 1); the Latin America correction + standalone Mexico annex shipped in #750 (discharging the fr-59 Mexico accepted-unverified tracker against the held 2025 LFPDPPP). Remaining: the 18 source-gated annexes (gap analysis at `inbox/worker-20260703-a/fr-59-privacy-jurisdiction/research-source-gated-gaps.md`), which wait on maintainer source drops (APAC beyond Japan, and others absent from the reference base). Out of this item by design: the EU annex (fr-74-owned) and the UK annex (already operationally deep).

### 2.3 Crypto-asset / blockchain governance domain (FR-70, H[critical], XL)

New domain for crypto-asset / blockchain governance: digital-asset custody, staking, smart-contract risk, blockchain platform vetting. Regulatory references: DORA, MiCA, NYDFS BitLicense (DORA and MiCA (Regulation (EU) 2023/1114) are HELD; only NYDFS BitLicense (23 NYCRR Part 200) is not held, tracked as MEG-01 in the egress queue, WestLaw-gated). (Cross-references P6.x for domain-level shaping.)

### 2.15 Landing-page standards list: link each item to its authoritative source, MOVED to 2.25.2 (Series A) (maintainer-confirmed 2026-07-15, M, S-M)

**Moved to 2.25.2** (Series A, international AI-governance authority coverage), which absorbs this landing-page standards-to-source linking as its surfacing step. The content lives there. This is a forward redirect stub; it closes when 2.25.2 closes.

### 2.20 Ref-side `last_checked` sweep for the 6 new EU / CA AI sources (M, S; cross-repo)

Stamp `last_checked` on the 6 EU / CA AI sources ingested for the AI-domain delta in `grc_library_ref`'s `catalogue.yml` (a cross-repo `grc_library_ref` PR; OPEN). Pairs with the SR-1 currency mechanism. Re-homed from the retired AI-domain-delta umbrella (Workstream C.2).

**EGRESS-GATED (maintainer-directed 2026-07-25c), cross-referenced as MEG-48.** A worker completed everything around the one blocking field and reported why it stopped: `last_checked` records that someone verified currency AGAINST UPSTREAM, so no amount of held material can establish it and proposing a date would have been the inference the order forbade. Delivered and ready to apply once the upstream pass happens: the item identification (self-verifying at six), per-item held-source evidence, drafted `checked_edition` for all six, and paste-ready `catalogue.yml` hunks with the date left as a placeholder. **Two residuals.** First, the six drafted `upstream_url` values came from knowledge rather than a fetch, so each must be confirmed to resolve before it lands. Second, one of the six deserves priority: the **EU Digital Omnibus** (`catalogue.yml:4934`) is the only one awaiting a specific dateable EVENT rather than a routine date refresh, its held header recording it as provisionally agreed 13 May 2026 but not yet adopted, and its status bears on the EU AI Act entry too. The maintainer's egress queue in `grc_library_private` carries the fetch list; this item stays open until the upstream pass returns.

### 2.21 Further AI-jurisdiction annexes (M, L; partly source-gated)

**SPLIT THREE WAYS 2026-07-25.** (i) **Australia is STRUCK, not deferred**: the annex has existed
since #801 and the deferral text was written three days AFTER it merged. (ii) **BUILDABLE NOW, source
gate cleared**: US Texas (TRAIGA HB 149) and US Illinois (HB 3773, PA 103-0804) become ordinary P2
content work with held sources, no egress. (iii) The remaining jurisdictions stay source-gated and move
behind the Egress Gated divider, each named so the acquisition ask is concrete.

New AI-jurisdiction annexes, split by what is actually held. **Australia is STRUCK, not deferred:** [`ai/jurisdictions/annex-ai-australia.md`](ai/jurisdictions/annex-ai-australia.md) has existed since #801, so the deferral was wrong on arrival (the section text dates to #932, three days after the annex merged). **Source-gate CLEARED, annex not yet built:** US Texas (TRAIGA HB 149) and US Illinois (HB 3773, PA 103-0804), whose full-text primaries are held in the reference base and which #1116 cited in [`ai/policy-ai-compliance.md`](ai/policy-ai-compliance.md) section 7.5 with canonical-citations rows verified 2026-07-24; decide whether the section-7.5 coverage is sufficient or a dedicated annex is wanted, but do NOT re-run acquisition. **Held source, not yet adopted as a citation:** UK (AI Regulation White Paper 2023), Malaysia (National AI Governance and Ethics Guidelines 2024), and US federal (the OMB M-25-21 / M-25-22 / M-26-04 memoranda and the 2025 AI Action Plan) each have a held full text in the reference base but no canonical-citations row, so the gate for these is citation adoption rather than acquisition. Cross-references the P5.9 AI-jurisdiction-overlays umbrella. Re-homed from the retired AI-domain-delta umbrella (Workstream B.3).

### 2.23 CCPA statute (eff. 2026-01-01) currency + alignment review (maintainer-flagged 2026-07-16, M, S; cross-repo, blocked on ref ingestion)

The maintainer added the CCPA statute version effective 2026-01-01 to `grc_library_ref` (`ingest/ccpa_statute_eff_20260101.pdf`, being ingested to `--full-text.md` by a worker as of 2026-07-16). Once the full-text is held, run a currency + alignment review of the corpus content that relies on CCPA/CPRA against the updated statute. Signals it is warranted: `privacy/jurisdictions/annex-privacy-united-states.md` currently characterizes California as "CCPA/CPRA (effective 2023-01-01)" (the CPRA operative date), while the added source is a 2026-01-01 version, so amendments may be unreflected; ~18-19 corpus files mention CCPA/CPRA, of which the reliance-bearing subset (~13, excluding glossary / jurisdiction-index / decision-tree passing mentions) is the review scope: the US annex, `register-automated-decision-making.md`, `procedure-data-subject-rights-management.md`, `framework-consent-management.md`, `framework-childrens-data.md`, `register-cookie-and-tracker.md`, and others. Method: OFFLOAD as a credit-offload order once the full-text lands (a `/reference-audit` new-ingest pass plus a currency/alignment check of the CCPA-citing docs against the held 2026-01-01 text); route findings (stale date, superseded provision, new obligation) to the backlog / a corpus-update PR, each verified against the held source. NOTE: the CPPA cybersecurity-audit REGULATIONS (Cal. Code Regs. tit. 11, the "Article 9" a CPRA cybersecurity audit engages) are a DIFFERENT instrument from this statute; confirm whether they are separately held before relying on an audit-requirement citation. No guessing what changed; the review reads the held full-text. **STATUS (2026-07-16): the REGULATIONS-alignment half is IN PROGRESS.** The `ccpa-regs-2026-alignment` worker delivery (a `/reference-audit` against the held final CCPA REGULATIONS, 11 CCR Div 6 Ch 1 eff 2026-01-01, which are a DISTINCT instrument from the statute) is being applied in per-domain slices, each with at-source re-verification + a skeptical verifier + confirmed upstream currency at the fetchable `cppa.ca.gov`: **slice 1 (#976)** updated the US privacy annex (ADMT/risk-assessment/cyber-audit final regs, corrected the audit/risk-assessment conflation + significant-decision scope), **slice 2 (this PR)** updated `register-automated-decision-making.md` (fixed the `1798.185(a)(16)`->`(a)(15)` statute-sub-paragraph citation error + added the CCPA ADMT opt-out/access/pre-use-notice/human-appeal subject rights). **slice 3 (#978)** updated `procedure-data-subject-rights-management.md` + `annex-privacy-jurisdiction-index.md` + `template-privacy-notice.md` (ADMT opt-out/access/pre-use-notice + the s.7021/s.7221(n) timelines), and **slice 4 (#979)** added the breadth citations to the four framework-alignment tables (`framework-consent-management` s.7004; `framework-childrens-data` ss.7070-7072; `register-cookie-and-tracker` ss.7025-7026; `template-dsar-workflow` s.7021/ss.7221-7222). **The CCPA REGULATIONS-alignment half is now COMPLETE** (primary carriers + breadth). **Separately still open:** the STATUTE-currency half this item was originally framed around (whether the corpus's "CCPA/CPRA effective 2023-01-01" characterization needs updating against the 2026-01-01 STATUTE version, and any superseded/added statutory provision) once the statute full-text is confirmed held; the regs-alignment slices do not close that. Full delivery findings persist on scratch (`results/ccpa-regs-2026-alignment.md`). **Precision follow-up (from #976's `/validate-pr` NOTE 1, non-blocking):** the US annex cyber-audit phasing sentence ties only the first tier to "2026 revenue" and gives the 2029/2030 dollar bands without their per-tier measurement years; the held 11 CCR §7121 (Timing Requirements) keys the 2029 deadline to 2027 revenue and the 2030 deadline to 2028 revenue (§7120 is the audit-requirement/threshold section). Deadlines and bands are all correct (accuracy is fine), so this is an optional precision tightening for the expert review: add the per-tier measurement years to `annex-privacy-united-states.md`. **APPLIED in #982** (annex v1.2.3: the 2029-04-01 tier now names 2027 revenue and the 2030-04-01 tier names 2028 revenue, re-verified against the held §7121 eff-2026-01-01). The statute-currency half of §2.23 remains separately open.

### 2.24 Governance Relationship and Flow Modelling Framework, MOVED to 2.25.1 (Series A) (2026-07-19, L) `[content]`

**Moved to 2.25.1** (Series A, Governance traceability and coverage expansion): the content lives there. This is a forward redirect stub (the series-consolidation redirect-stub convention); it closes when 2.25.1 closes.

### 2.25 Governance traceability and coverage expansion (umbrella; maintainer-directed 2026-07-23, H, XL) `[content+machinery]`

Umbrella for the corpus's control-to-authority traceability model and the coverage expansion that reaches corpus controls up to regulatory and international-policy authorities. Delivers its value independently of OSCAL (Series B, 2.26): every child ships as Markdown or as a generated relationship artefact, with no dependency on OSCAL adoption. Governing constraints from the flow-modelling framework (2.25.1) apply throughout: never conflate mapped, implemented, effective, and sufficient; never treat a reference as a requirement or adoption as compliance.

**Series members, in execution order:** 2.25.1 (relationship framework, the base), 2.25.2 (international AI-governance authorities), 2.25.3 (Canadian public-sector authorities), 2.25.4 (AI assurance and evaluation content), 2.25.5 (governance-maturity measurement model). Existing items consolidated in via a redirect stub: 2.24 into 2.25.1, 2.15 into 2.25.2, 2.22 into 2.25.3.

**Execution:** P2; authored now, executed after all P1 and P3 items are cleared; execute before Series B (2.26).

**Acceptance criteria:** every authority added by Series A is a resolvable node in the regenerated relationship model; all content ships as Markdown; `taxonomy.yml`, the portal, and the scorecard regenerate clean; every new authority is registered in the canonical citations register with edition and trust tier.

### 2.25.1 Graduate the Governance Relationship and Flow Modelling Framework to a generated model (consolidated from 2.24; H, L) `[content+machinery]`

Consolidated from 2.24 (a redirect stub is left there). Two parts. (a) Author the NEW governance `Framework`-type document scoped below (2.24's original scope, moved here). (b) GRADUATE it from prose-core-plus-one-illustrative-record to a GENERATED semantic relationship model: the node classes (control, obligation, external authority, register, assurance) and the authority / applicability / governance / implementation / assurance / risk viewpoints become a generated relationship layer that the maturity metrics in 2.25.5 read from and the OSCAL crosswalks in 2.26.5 serialize. The generated artefact needs a NEW deterministic regeneration gate (a `--check` mode, as gates 33 and 34 have), registered with the gate-name parity self-check (gate 35) and passing the stdlib-only import audit (gate 71). Retain all the anti-patterns in the scope below as governing constraints.

**Depends on:** none.

**Blocks:** 2.25.5; and across series 2.26.5.

**Decision-gate:** graduating the framework to a generated artefact supersedes 2.24's "no new generated / validated artefact" cap; that cap-lift is a maintainer decision, independent of the OSCAL decision. ASK before building the generated layer.

The document scope, moved from 2.24: author a NEW governance `Framework`-type document (an EXISTING document type, NOT a new type) standardizing how GRC entities are modelled as directed relationship flows, PLUS a small reframing edit to the existing [`governance/framework-document-architecture-and-interrelationship.md`](governance/framework-document-architecture-and-interrelationship.md). Scoped from the maintainer's 2026-07-19 proposal (source spec `GovernanceRelationshipFlowFramework-Specification-v1.0.0.md` + an orchestrator-prompt in `grc_library_scratch/inbox/maintainer/`, a WIPEABLE repo, so preserve the source spec durably (for example to `grc_library_private` or the new doc's provenance) if it must survive), assessed and reconciled against the existing framework doc, every scope decision maintainer-confirmed. The apply-ready research is delivered (scratch `results/research-flow-framework-224.md`).

**Confirmed scope decisions (2026-07-19, all maintainer-accepted):**
- **Breadth = LAYERED.** The general entity-relationship modelling method (the reusable core) is the primary content, PLUS a worked corpus-application section applying it to this corpus's own document hierarchy (reusing the existing doc's Charter to Framework to Policy to Standard layering as one worked example).
- **Apparatus = PROSE CORE + ONE non-normative illustrative schema example** (a single small YAML or JSON relationship record). NO new linter, NO new generated/validated artefact, NO exhaustive node-by-verb matrix. The example is marked non-normative (an adopter starting-point for graph-database / traceability builds).
- **Verb vocabulary = FOCUSED canonical set + key distinctions.** A rationalized high-value verb set (issues, requires, specifies, implements, produces, assesses, and similar, de-duplicated from the proposal's candidate lists) with plain definitions and permitted source/destination classes, PLUS the crucial assessed-vs-structural distinction (satisfies / fulfils / conforms to / complies with / meets are ASSESSED or inferred OUTCOMES, not permanent structural edges). NOT the full exhaustive per-verb table.
- **Reconciliation = reframe the existing hierarchy as ONE viewpoint.** The existing doc's fixed document-type hierarchy becomes "the document-architecture viewpoint" (explicitly non-universal); the new framework states that entity placement is CONTEXTUAL across viewpoints; the two docs cross-reference. No contradiction: the existing doc is a document-type layering (about document types), the new framework is entity-relationship modelling (about governance entities generally); they meet only at framework/policy ordering, resolved by the one-viewpoint framing.
- **Diagrams = TEXT-ONLY in the corpus.** The corpus holds ZERO Mermaid, so use the proposal's own `SOURCE VERB DESTINATION` text / fenced-block form for every in-corpus flow example. Provide ADOPTER GUIDANCE (a section) for adopters who WANT to generate diagrams (Mermaid, graph database), as guidance, not as corpus-embedded diagrams.
- **Document types = no new types.** The new doc is the existing `Framework` type. Provide ADOPTER GUIDANCE on document-type options that may suit an adopter's own scenario (guidance, not a corpus change).

**Content to author (the valuable core, distilled from the proposal):** core principles (contextual placement, viewpoint + primary-direction declaration, primary vs associative edges, inferred reverse relationships, structural vs inferred/assessed/temporal/evidence-dependent, evidence-for-conformance); a rationalized node-class taxonomy (external authority/obligation; interpretive/normative sources; organizational governance; scope/operating context; implementation; risk; assurance/outcome; a node may hold more than one category); the six viewpoints (authority, applicability, governance, implementation, assurance, risk) each as a common pattern not a universal hierarchy; the focused verb set; the validation tests (source-action, direction, cycle, structural-fact, verb-precision, cardinality, temporal-validity, authority, evidence); the high-value anti-patterns (treating a mapped control as implemented / an implemented control as effective / an effective control as sufficient for all obligations; treating a reference as a requirement; treating adoption as mandatory compliance; treating compliance as static without assessment/evidence; passive voice; cycles in the primary layout; forcing frameworks and policies into one universal order); ONE illustrative non-normative YAML relationship record; governance/lifecycle (owner, relationship-vocabulary owner, verb-addition + node-class-addition process, review cadence = the CORPUS standard not the proposal's default, change control); and the two adopter-guidance sections (diagram generation; document-type options).

**Corpus-fit requirements (turnkey authoring constraints):** mirror an existing `Framework`-type doc's 13-field metadata block + fixed section model (the proposal's own 25-section structure is CONTENT to distill INTO the corpus section model, never a structure to copy); house style (Canadian / `-ize`, `ensure that` not bare `ensure`, no em/en dashes, numerals, normative language per the corpus convention gate 56); repository-relative VALIDATED cross-references only (validate each against content not title; do not invent paths / identifiers / mappings); do not reproduce copyrighted standards text; prefer ILLUSTRATIVE placeholder codes in the example over real control-code / normative-value citations, to avoid creating a `/matrix-fit` / `/claim-fit` semantic-fit surface. Integration: the reframing edit to the existing interrelationship framework (add the one-viewpoint note + cross-reference, bump its Version + Date); a `governance/register-document-index-and-classification.md` row for the new doc; taxonomy + portal + scorecard regeneration (gates 33/34); cross-references to the compliance matrix, per-doc framework-alignment tables, and the risk docs where the content genuinely bears.

**Apply discipline:** substantive corpus-content work; ONE coherent PR (the new doc + the reframing edit + the index/taxonomy regen are on-topic and non-overlapping, so they belong together; split only if a part proves genuinely independent); skeptical verifier (substantive tier) pre-push; `/reference-audit` per-touch on the new doc; NOT partitionable, single-session. Scheduled into the content tier (maintainer-directed 2026-07-19: detailed TODO now, author later).

### 2.25.3 Canadian public-sector authority coverage (consolidated with 2.22; CANADA-PRIORITY, H, L) `[content]`

**UN-DEFERRED 2026-07-25.** The 'deferred-blocked on currency' status was VOID: all 49 federal
sources are held and were downloaded within the previous two weeks. Now fully actionable. **Partition by
source cluster** (AI-governance / OSFI financial / ITSG-CCCS cyber / Privacy-Act-OPC-PIPEDA / provincial
FOI) and fan the research out to workers while the orchestrator authors. Sequenced after the tooling
catch-up. Absorbs item 2.22 (closed 2026-07-25), which closed as consolidated.

Canadian authority coverage. Consolidates 2.22 (a redirect stub is left there): systematically engage the 49 newly-held Canada.ca federal sources (TBS Directive on Automated Decision-Making, AIA tool and AI guides, OSFI B-13 and E-23, ITSG-33, CCCS ITSP.80.022, the GC cloud control profile, the Pan-Canadian Trust Framework, the Privacy Act, OPC, PIPEDA) across the Canada AI annex, the privacy annex, the matrix and per-doc framework-alignment tables, and the public-sector overlay. PLUS the provincial FOI and privacy gap not covered elsewhere: FIPPA, MFIPPA, FOIP. Ships as Markdown now; CANADA-PRIORITY preserved (government-facing, expert-reviewed, so a high accuracy bar: no fabricated codes, no unverified currency). Register each authority in the citations register; confirm each source is held before authoring. **Status carried from 2.22:** the Canada.ca apply is DEFERRED-BLOCKED on currency (canada.ca WAF-blocks automated re-fetch); the maintainer downloads fresh copies (request in `grc_library_private/maintainer-egress-requests.md`), then the per-domain apply proceeds.

**Depends on:** 1.22.9 (P1, direct canada.ca download URLs) and 3.42 (P3, Canadian captures); references them.

**Blocks:** none.

**Feeds:** 2.25.5; and across series 2.26.5.

### 2.25.4 AI assurance and evaluation content (H, L) `[content]`

New `ai/` content for model evaluation, assurance arguments and safety cases, and post-deployment monitoring, using the held reference maps as inputs. Enterprise-assurance scope (assuring a deployed system), not frontier-risk. Ships as Markdown now. Confirm the reference sources are held before authoring.

**Depends on:** 3.14 (P3, ETSI Securing-AI map); references it as an input. (The ETSI TR 104 128 input, former 3.63, is complete: the held informative TR is engaged as a see-also across the `ai/` domain, the secondary see-also added to the AI security-and-risk standard's alignment table in PR #1122. The MITRE ATLAS 2026.06 map input, former 3.15, is complete: the corpus ATLAS citations were verified current against held 2026.06 and the one LLM02 fit finding applied, PR #1119.)

**Blocks:** none.

### 2.25.5 Governance-maturity measurement model (maintainer-directed 2026-07-23; M, M) `[content]`

Evolve the existing maturity self-assessment template and the generated maturity scorecard into a structured, comparable measurement model whose inputs derive from the 2.25.1 relationship layer (authority coverage, mapped-versus-unmapped controls). Governed by the 2.25.1 anti-patterns: it reports MAPPED coverage only, and must not imply implemented, effective, or compliant.

**Depends on:** 2.25.1.

**Blocks:** none.

### 2.26.1 OSCAL adoption decision and model-scope lock (maintainer-directed 2026-07-23; H, S) `[machinery]`

Bring the adopter-requested OSCAL feature to the maintainer for the adopt / do-not-adopt decision and, if adopted, lock the initial model scope. Models believed stable to target first: catalog (corpus controls) and profile (framework baselines and selections); the adopter-side models (component-definition, system-security-plan, assessment-plan, assessment-results, plan-of-action-and-milestones) are out of corpus scope. Output: a decision record plus, if adopted, the target OSCAL version captured in the canonical citations register (feeds gate 5).

**Depends on:** maintainer decisions (ASK at execution, do not guess).

**Blocks:** 2.26.2, 2.26.3, 2.26.4.

**Decision-gate:** OSCAL version; model set; whether a dedicated crosswalk / mapping model exists in the target release and should be used, or whether alignments are expressed as profile imports plus 2.25.1 relationship records.

### 2.26.2 OSCAL stable-identifier layer (S, M) `[machinery]`

Add the immutable, per-document control-identifier layer OSCAL requires, on top of the stable doc-id scheme delivered by 3.75. Identifiers monotonic and never recycled, consistent with the gate-13 posture. This child is the OSCAL increment only; the base doc-id work stays in 3.75.

**Depends on:** 3.75 (P3, base stable doc-id) and 2.26.1.

**Blocks:** 2.26.4.

### 2.26.3 OSCAL metadata-field alignment (S, M) `[machinery]`

Extend the 13-field metadata block and the `grc_library_ref` `doc_type` facet to carry the fields an OSCAL catalog / profile projection requires (control class, property namespaces, source-authority references). The metadata block stays canonical; OSCAL fields derive from it. OSCAL increment only; the base facet work stays in 3.54.

**Depends on:** 3.54 (P3, base `doc_type` facet) and 2.26.1.

**Blocks:** 2.26.4.

### 2.26.4 OSCAL catalog pilot: one domain, generated, gated (maintainer-directed 2026-07-23; M, XL) `[machinery]`

Generate an OSCAL catalog for a single domain from Markdown source, non-authoritative, alongside the existing generated indexes. Add a gate validating the generated OSCAL against the OSCAL schema and against the stable control-ids from 2.26.2 (a `--check` mode, registered with gate 35, passing gate 71).

**Depends on:** 2.26.1, 2.26.2, 2.26.3.

**Blocks:** 2.26.5.

**Decision-gate:** which domain seeds the pilot (security or ai); whether OSCAL schema validation is achievable stdlib-only, or whether to grant a dependency exception. The stdlib-only exception would break audit-programme design principles, so it is a maintainer decision, not an orchestrator one; ASK, do not add a dependency silently.

### 2.26.5 OSCAL profiles and crosswalks for framework alignments (M, L) `[machinery]`

Express the existing ISO, NIST, CSA, and COBIT alignment tables as OSCAL profiles (and a crosswalk representation per the 2.26.1 decision), generated from the current mapping matrices. Reuse the framework-citation hallucination audit (gate 5) so every control code in a generated crosswalk is a real identifier in the framework it names.

**Depends on:** 2.25.1 (Series A relationship model) and 2.26.4.

**Blocks:** none (terminal).

### 2.28 AI jurisdiction annex + ref ingest: Singapore Model AI Governance Framework for Agentic AI (M, M) `[content]`

Surfaced 2026-07-24 during the §2.19 Singapore GenAI annex build: IMDA and the AI Verify Foundation released a separate, newer Model AI Governance Framework for Agentic AI (unveiled January 2026), a DISTINCT framework rather than a new edition of the GenAI Framework, so §2.19's citation stands. Follow-up: ingest the Agentic AI MGF into `grc_library_ref` as a held primary (confirm currency upstream at ingest), then add a companion jurisdiction annex or fold it into [`ai/standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md), per the maintainer's scope call.

### Egress Gated

Items below need an egress-enabled fetch the assistant cannot perform, so they are parked here at
the end of this priority section rather than interleaved with actionable work. **Item numbers are
unchanged**: position carries no meaning, the number is permanent. Every source these items need is
listed in the `_private` maintainer-egress request so it can be batch-downloaded in one pass.

### 2.18 AI jurisdiction annex: South Korea AI Basic Act (H, M)

New jurisdiction annex for the South Korea AI Basic Act (held primary). `[VERIFY]` the phased effective dates upstream at apply (the catalogue records effective 22 Jan 2026; egress-gated). A government-facing annex, high-assurance harness. Re-homed from the retired AI-domain-delta umbrella (Workstream B.1).

### 2.25.2 Control-to-policy-instrument coverage: international AI-governance authorities (consolidated with 2.15; M, M) `[content]`

New authority coverage for the OECD AI Principles, the UNESCO Recommendation on the Ethics of AI, the G7 Hiroshima Process Code of Conduct, and the Council of Europe Framework Convention on AI, so each becomes a mappable external authority in the 2.25.1 relationship model. Ships as Markdown now. Consolidates 2.15 (a redirect stub is left there) as the surfacing step: the landing-page "Standards and frameworks it maps to" list links each item to its authoritative source (freely-available sources to the primary document or official landing page; licensed sources to the official catalogue / abstract page, never hosting or bypassing paywalled text), sourced from [`grc_library_ref`](../grc_library_ref) `catalogue.yml` and confirmed current at build. Register each instrument in the canonical citations register with edition and trust tier; once they land, move them on the for-ai resource index from "named, not yet covered" to covered. **[VERIFY]** the Council of Europe convention's signature and ratification status, and each instrument's current edition, upstream at apply (egress-gated; currency-material).

**Depends on:** none (content).

**Blocks:** none.

**Feeds:** 2.25.1; and across series 2.26.5.

### 2.26 OSCAL machine-readable representation (umbrella; maintainer-directed 2026-07-23, H, XL) `[machinery]`

Umbrella for adopting NIST OSCAL as an open, machine-readable projection of the corpus. Markdown remains the single source of truth; every OSCAL artefact is generated and non-authoritative, in the manner of `taxonomy.yml`, and is never hand-edited (artefact-and-branch-discipline applies). OSCAL adoption is an adopter-requested feature for the maintainer's consideration, NOT a settled decision; the go / no-go is a maintainer decision brought forward at 2.26.1. Depends on Series A (2.25): it serializes A's relationship model (2.25.1) and maps the authorities A adds; Series A never depends on Series B.

**Series members, in execution order:** 2.26.1 (adopt-decision and model-scope lock), 2.26.2 (stable-id layer), 2.26.3 (metadata alignment), 2.26.4 (catalog pilot), 2.26.5 (profiles and crosswalks).

**Execution:** P2; authored now, executed after all P1 and P3 items are cleared and after Series A.

**Acceptance criteria:** the OSCAL adoption decision is recorded; the pilot catalog generates from Markdown and validates against the OSCAL schema in CI; OSCAL control-ids reconcile with corpus control-ids; profiles and crosswalks generate and pass the framework-citation audit (gate 5); all gates run stdlib-only or under an approved exception.

**[VERIFY]** the current OSCAL release line and model set at NIST before 2.26.1 (egress-gated); do not pin a version in prose until confirmed and recorded in the canonical citations register.

## Priority 3 — Clean up and tooling

**Next item number: 3.187.**

Cross-document consistency cleanup and routine development / quality tooling: lower-priority than gaps, not error-prevention or adopter-facing. Picked deliberately into batches, not from the routine P1/P2 queue.

**Close-out-efficiency cluster (fresh-eyes 2026-07-26, maintainer-directed to EXECUTE EARLY in P3):** the takeover
session found per-PR bookkeeping and wind-down to be ~20-30 minutes of mostly-mechanical work; these six items
(3.133-3.137, plus the adopted fewer-larger-PRs guideline) remove that overhead. Rationale and ranking in
`grc_library_private/fresh-eyes-observations-2026-07-26.md`.

### 3.142 `/sitrep` situation-report command (maintainer-requested; dropped-and-recovered 2026-07-27, M, M) `[machinery]`

A maintainer-facing situation-report slash command: the four status sections (work in flight, the queue, QA state, and the worker fleet), a decisions-owed-you section, and a usage footer (instrumented orchestrator spend plus per-worker estimated spend plus the offload-savings figure). Depends on the per-worker logging (3.131) for the per-worker spend numbers. It was bundled with 3.128 in a prior session's next-actions, never got its own number, and was dropped in the 2026-07-26 emergency wind-down; re-registered here so it persists. Umbrella A (worker/observability tooling).

**Refinements from prototyping the output (2026-07-27, maintainer requested a live sitrep before the tool existed, then directed these be captured in the planning).**
1. **Read LIVE state at invocation, never the orchestrator's in-context memory.** Compose the report from the existing instruments so every line is verifiable rather than narrated: [`tools/audit-worker-saturation.py`](tools/audit-worker-saturation.py) (`--oneline`) for the fleet section, [`tools/collect-deliveries.py`](tools/collect-deliveries.py) (`--dry-run`) for the tray, [`.working/open-findings.md`](.working/open-findings.md) + [`.working/validate-pr/history.md`](.working/validate-pr/history.md) for QA state, [`.working/next-prs.txt`](.working/next-prs.txt) + this file for the queue, and [`.working/merge-bypass-log.md`](.working/merge-bypass-log.md) + [`.working/session-handoff.md`](.working/session-handoff.md) for work-in-flight. The prototype was assembled from memory; the tool must not be, so a wrong figure cannot slip in unverified.
2. **The usage footer needs REAL instrumentation and must NOT fabricate.** In the prototype the per-worker TOKEN spend was UNKNOWN for six of seven orders, because `exec-dispatch.py` captures worker DURATION (from the dispatch status line) but not token counts; the footer honestly read UNKNOWN rather than a fabricated total. Per the measured-not-inferred discipline in [`evidence-grounded-completion`](.claude/rules/governance/evidence-grounded-completion.md): keep MEASURED figures (durations) and ESTIMATED figures (any self-reported token counts) in SEPARATE columns, never summed, and report a gap as UNKNOWN, never zero. Orchestrator spend was likewise not instrumented in-session; the tool should surface whatever real counter the harness exposes or state it is unavailable, not invent one. This is the concrete dependency on 3.131: the per-worker structured logging is what turns the token column from UNKNOWN into measured. Until 3.131 lands, the footer reports durations (measured) plus the offload-savings framing (which QA/research passes ran on worker vs orchestrator credits) and marks token spend UNKNOWN.

### 3.143 Worker-account onboarding process plus an add-account shell script (maintainer-directed 2026-07-27; new accounts arriving, M, M) `[machinery]`

The maintainer is adding one or two more Claude Code worker accounts. Build a repeatable onboarding PROCESS plus a shell script that efficiently adds a new worker account: create its per-account config dir under the worker user, install the read-only worker settings, register it in the `_private` worker-accounts config (id, account, family, config_dir, max_concurrent, tier), and verify the wrapper accepts it while the negative test still rejects any non-wrapper command. Idempotent, safe to re-run per new account. Umbrella A.

### 3.144 Multi-orchestrator / self-refreshing orchestration (SCOPE/SPEC-GATED, needs maintainer discussion; M, XL) `[needs-decision]`

**DEFERRED pending maintainer scope/spec: discuss and agree the approach before any build.** The goal is to defeat long-run orchestrator context degradation WITHOUT a full stop, by refreshing the orchestrator's context at its compaction threshold (the roughly-second-compaction degradation point) rather than winding down until the maintainer returns. Two forms were discussed 2026-07-27 as REFERENCE IDEAS, not yet decided:

- **Form 1, one-shot auto-handoff (the incremental first step).** On an evidence-triggered wind-down, the orchestrator does a proper session-closing handoff (state on main, lease RELEASED), then as its FINAL action injects `/resume` plus Enter into a pre-launched idle claude tmux session (same user/dir/account) via `tmux send-keys`. The fresh session reads Operating-mode from `session-state.md` and resumes in overnight-unattended mode (the AskUserQuestion-unattended hook keeps it from blocking with no maintainer present). Proves the poke mechanism. The caveat it does NOT solve: the poker is winding down, so it cannot verify the poke landed (submit-state indeterminacy), a silent-no-op risk.

- **Form 2, primary plus near-idle standby (the full form).** Exactly ONE orchestrator holds the apply-lease and does all work: the serial-apply invariant is UNCHANGED (never two concurrent appliers, because the shared main-state surfaces, CHANGELOG / TODO / version lines / handoff / QA ledgers, conflict badly). A near-idle standby watches a shared compaction-signal; when the primary signals its second compaction AND a clean handoff-to-main, the standby issues `/clear` plus `/resume` to the primary's tmux, then VERIFIES the resume took (a resumed-at marker) and retries or escalates on failure. The primary refreshes in place with fresh context; the standby stays fresh because idle sessions do not grow context and so do not compact, so no symmetric role-swap is needed. This fixes Form 1's silent-no-op (a live standby verifies). Cost is low: an idle standby burns almost nothing and refreshes are infrequent, so it does not double the scarce orchestrator credits.

- **Transport dimension (maintainer lean, 2026-07-27).** The injection CHANNEL is an open question with many options to assess. The maintainer leans toward a UNIX SOCKET feeding directly into the tmux session, or directly into the orchestrator's AI chat session, rather than `tmux send-keys`, because a socket sidesteps the keystroke-injection fragility and the submit-state indeterminacy that make a poke's success hard to confirm (it would also remove Form 1's silent-no-op risk at the transport layer). Relates to the §3.87 local-VM socket-transport thread. Assess socket-into-tmux vs socket-into-chat-session vs `send-keys` vs other IPC before committing.

**Hard parts to spec before building:** (1) a single-writer lease/handover with NO split-brain (the standby must never apply while the primary is mid-refresh; split-brain on the ORCHESTRATOR is far worse than on a worker); (2) the compaction-signal plus clean-handoff protocol on a shared channel (poke only after state is safely on main, or `/clear` loses in-flight work); (3) the poke-verify-retry-escalate loop. Build incrementally (Form 1 to prove the mechanism, then Form 2). Umbrella A (orchestration infrastructure); needs maintainer sign-off on the lease/handover protocol before any unattended run.

### 3.147 Worker OAuth token refresh does not persist (the --worker-id snapshot deletes it), so accounts expire and need manual re-auth (2026-07-27, M, M) `[machinery]`

The exec'd-worker wrapper's `--worker-id` path (the one that enables concurrency) SNAPSHOTS the account config dir (`cp -a $cfg/. $snap/`, including the OAuth token), runs claude against the snapshot, and DELETES the snapshot on exit. So when claude refreshes the OAuth token mid-run, the refresh lands in the throwaway snapshot and is lost; the BASE config dir's token is never renewed by a worker run, so it expires on its normal TTL (about 1-2h observed) and each new snapshot then copies the already-expired base token, failing auth. Observed 2026-07-27: jposluns-work, then security-work and jeff-mailz all lapsed within about 1-2h of use, each needing a manual `/home/grc/maintainer/reauth-lapsed-agents.sh` re-login. The snapshot ISOLATION that makes same-account concurrency safe is precisely what breaks token-refresh persistence. STRONG hypothesis (it is certain from the wrapper code that a refresh cannot persist; the causal link to the exact TTL should be confirmed). Options for a durable fix: (a) after a run, write the refreshed token back from the snapshot to the base config dir (needs care against concurrent write races and a policy for which snapshot's token wins); (b) a periodic light base-token refresh (a cron running claude briefly against the BASE config dir, not a snapshot); (c) API-key credentials for workers instead of OAuth; (d) accept manual re-auth. Needs a maintainer design decision. This is the fleet-longevity counterpart to the concurrency work: concurrency ITSELF is validated safe (4 workers ran concurrently on one account and each produced correct isolated output 2026-07-27). Umbrella A (fleet reliability). Cross-repo: the wrapper is root-owned `/usr/local/sbin/run-{claude,codex}-worker`.

**DECIDED design (maintainer chose write-back 1.1, 2026-07-27; refined for the multi-worker case).** The fix is MEASURE-FIRST, then write-back, and it has TWO layers because concurrent same-account workers add a rotation problem the write-back lock alone cannot solve. **Step 1, MEASURE claude's token behaviour:** (a) does a refresh ROTATE the refresh token (using `RT0` yields `RT1` and invalidates `RT0` at the provider), and (b) the access-token TTL versus a typical worker-run length. **Step 2, if refresh tokens DO NOT rotate:** plain per-worker write-back is safe, copy the refreshed token from the snapshot back to the base under the per-account lock before deleting the snapshot, since any worker's refreshed access token is valid (Layer 1, the write-back race, is fully handled by the lock). **Step 3, if refresh tokens DO rotate** (the likely case, since a lapsed account needs a full RE-LOGIN rather than only an access refresh, which means its base refresh token was invalidated): per-worker independent refresh CONFLICTS at the provider, N concurrent snapshots all copy the same base `RT0`, the first to refresh rotates it to `RT1` and invalidates `RT0` for the rest, and a naive write-back of a stale snapshot would clobber the good `RT1` (Layer 2, the rotation conflict). The concurrency-safe answer is to **SERIALIZE THE REFRESH, not just the write-back**: the orchestrator refreshes the BASE token ONCE, serially, right before dispatching each concurrent batch (persisting the rotation to base), so every snapshot copies a FRESH access token and, if runs are shorter than the access-token TTL, no worker refreshes mid-run and there is no rotation to conflict over (write-back is then a single-winner safety net under the lock). Only if a run can OUTLIVE the access token is the heavier answer needed: a SINGLE per-account token broker holding the refresh token and handing fresh access tokens to workers, so exactly one thing ever rotates. Build order: measure (step 1) first; it selects the step-2 or step-3 variant.

### 3.146 Group-writable files re-appear in the READ-ONLY repos via the inherited default ACL, not umask (check_perms recurrence, 2026-07-27, M, S) `[machinery]`

The orchestrator session's umask is `0002`, so every NEW file it creates in `grc_library` / `grc_library_ref` (new corpus docs, git checkouts, working records) is group-writable (`-rw-rw----`), violating the worker-access READ-ONLY model (`/home/grc/maintainer/check_perms.sh` flags "group-writable entries must be 0"). On 2026-07-27 this had accumulated to 88 entries; `check_perms --apply` (root) repaired them, but the umask re-introduces them on the next write, so `--apply` is a reactive treadmill. Defence-in-depth only (the AI-permission layer + the read-only worktree cache still block worker writes), but the filesystem layer degrades. **CORRECTED root cause (worker research Z, verified at source 2026-07-27): it is the inherited default ACL, NOT umask.** `grc_library` and `grc_library_ref` carry an inherited POSIX **default ACL** (`default:mask::rwx`, `default:group::r-x`), and the kernel IGNORES umask for a file created in a directory that has a default ACL. So every new file gets ACL `mask::rw-` and DISPLAYS as `-rw-rw----+` (group-writable) whatever the umask, which is why `umask 0027` would NOT fix this (verified by a controlled experiment: with the default ACL present, both umask 0002 and 0027 produce `-rw-rw----`). Important subtlety: the file's EFFECTIVE owning-group permission is `group::r-x` masked by `rw-` = **`r--` (read-only)**, so a worker in group `grc` cannot actually WRITE these files, the READ-ONLY model is satisfied at the effective level, and `check_perms`'s `find -perm -g=w` flag reads the ACL MASK, not the effective permission (so it over-flags). The umask 0002 itself comes from `pam_umask` + `USERGROUPS_ENAB yes` (mailz has a private primary group), a real setting but a RED HERRING for these ACL-governed trees. Durable fix options: (a) lower the `default:mask` (and repair existing entries once) on both READ-ONLY trees so new files inherit a non-group-writable mask (`0640`) at the source; (b) make `check_perms` read the EFFECTIVE ACL group permission via `getfacl` rather than the displayed mask, since the files are already effectively read-only; (c) both (defence in depth: fix the source AND make the auditor ACL-aware). Setting `umask 0027` in mailz's `~/.bash_profile` (the current `su - mailz` login-shell mechanism) helps only NON-ACL contexts and does not fix these trees. There is no orchestrator systemd service today (it is a transient `su - mailz` login scope), so a `UMask=` service directive is not available without first converting the orchestrator to a service. Needs maintainer action for the ACL change (root or the tree owner). **DECIDED (maintainer 2026-07-27): option (c), fix BOTH, lower the `default:mask` on the two READ-ONLY trees at the source AND make `check_perms` read the EFFECTIVE ACL group permission via `getfacl` rather than the raw mask (defence in depth).** Umbrella A (fleet hardening).

### 3.140 Hoist `_check_body` to module scope and add reality fixtures for the two generated-body prune paths and the non-UTF-8 branch (validate-pr-1186 F-2, 2026-07-26, M, S) `[machinery]`

`_check_body` is a closure defined INSIDE `main()`'s `if args.prune:` block ([`tools/sweep-working-records-to-private.py`](tools/sweep-working-records-to-private.py) line 721), so no `--self-test` case can reach it. The #1186 TODO 3.129 fixtures cover only the whole-file BYTE-copy paths (`_files_identical` at line 587 and `oneoff_missing_from_archive` divergent at line 579); the two GENERATED-body paths that `_check_body` guards, the weekly changelog-details archive (`weekly_archive_body`, verified at line 740) and the roll-up rows archive (`rollup_archive_body`, verified at line 751), plus its refuse-closed `UnicodeDecodeError`/`OSError` branch (lines 730-735), have NO reality fixture, so a present-but-divergent GENERATED body or a non-UTF-8 archive could silently regress the refuse behaviour with the suite still green. Hoist `_check_body` to module scope (return a reason-or-None instead of closing over `main`'s `missing` list, or take the accumulator as a parameter) so it is directly testable, then add reality fixtures asserting that a present-but-divergent weekly-archive body REFUSES the prune, a present-but-divergent roll-up body REFUSES, and a present-but-non-UTF-8 (undecodable) archive REFUSES. Same guard-input-authority class as 3.129: a data-safety check that its own self-test cannot reach is not yet a check.

### 3.141 Per-account worker concurrency greater than 1 via config-dir snapshots (design drafted 2026-07-26, M, L) `[machinery]`

The `--account` override (#1187) gives cross-account parallelism (N workers on N distinct accounts, each serialized by its own wrapper flock at 1). Running MORE THAN ONE worker on the SAME account concurrently is a separate, heavier item: the wrapper's blocking flock on a lock file inside the shared config dir (`$CFGBASE/$account/.wrapper.lock`) is BOTH the safety guarantee and the concurrency-1 cap, so loosening it without per-worker state would race the one shared `CLAUDE_CONFIG_DIR` / `CODEX_HOME`. The design candidate (the `design-multiworker-per-account` xhigh delivery, 2026-07-26) covers: a per-worker config-dir snapshot (copy the auth/credential state, isolate session/lock/cache) with cleanup; moving `max_concurrent` enforcement + an in-flight registry/counter into `exec-dispatch.py` (which is stateless today); and the claude-mktemp-workdir vs codex-fixed-shared-workspace asymmetry. First cut: `cp -r` snapshot + a per-account lock counter + `max_concurrent` bumped to 2, verify no auth contention, before the fuller design. Lower priority now that cross-account parallelism covers the immediate need.

### 3.134 Auto-bump-on-commit: extend the version hook from detect to fix (fresh-eyes 2026-07-26; EXECUTE EARLY, M, S) `[machinery]`

Extend [`.claude/hooks/block-unbumped-version-commit.py`](.claude/hooks/block-unbumped-version-commit.py) from DETECT
to FIX: when a staged versioned file's body changed and its Version did not, auto-bump both Version and Date (patch) in
the staged content instead of blocking. The Version-Date co-bump was the single most recurrent self-caught failure of
the takeover session; automating it removes it. Keep the block path as a fallback for ambiguous cases.

### 3.136 Handoff/close-out snapshot generator (fresh-eyes 2026-07-26; EXECUTE EARLY, M, S) `[machinery]`

`tools/handoff-snapshot.py` emits the mechanical facts the handoff and D7 need: library + README versions,
gate/rule/skill/command counts, green-at `<sha>`, and the session-metrics figures. The wind-down pastes a verified
block and writes only the narrative, instead of hand-deriving each number (where the D7 snapshot trap lives).

### 3.137 Close-out speed: changed-files quick guard + reconsider async recursion-avoidance (fresh-eyes 2026-07-26; EXECUTE EARLY, M-L, M) `[machinery]`

Two smaller fresh-eyes items. (a) A `--changed-only` fast path for the pre-push guard's fix loop (full 78-gate suite
once before push; a scoped check for iteration), to stop re-running the ~3-minute full suite after every one-line
self-fix. (b) Reconsider the async recursion-avoidance rule (the prior PR's QA rows batch into the next PR), which
serializes PR N on PR N-1's validate-pr worker round-trip; options: run validate-pr synchronously before finalizing,
or a periodic QA-rows catch-up decoupled from the next feature PR. Structural; a deliberate design look, not a quick
change. The fewer-larger-PRs guideline (do not fragment one theme into separate PRs) is ADOPTED as a convention.

### 3.138 Worker full-suite `/validate` via a per-job writable checkout (2026-07-26, M, M) `[machinery]`
A read-only worker cannot run write-requiring gates: **gate 36** (the linter-regression suite) writes fixtures to in-tree `tests/tmp/` **by design** (the linters walk the repo tree and validate a repo-relative `Repository Path`, so the fixtures must live in-tree). Established at the first exec-worker `/validate` (Sweep 123, 2026-07-26; worker-brief rail 18): a worker `/validate` covers the 77 read-only content gates but not gate 36, which stays orchestrator-side. To let a worker run the full 78 WITHOUT a write-hole in the shared tree, give it its OWN writable checkout: a warm worker-owned clone of `grc_library` (it is group-readable, so a LOCAL clone needs no token) plus a per-job `git worktree` at the pinned SHA (isolated working tree, shared object store) that the worker runs the full suite in and discards. NOT a single shared mirror (that only MOVES the shared-fixture contention). Buys complete offload + worker-side gate-36 coverage on linter-changing PRs. Maintainer-surfaced (rsync-copy idea) 2026-07-26.

### 3.139 Right-size CLAUDE.md (umbrella goal; not itself a task) (2026-07-26, M, L) `[machinery]`
GOAL: CLAUDE.md is ~1960 lines / 23K words loaded EVERY turn (a per-turn performance + token tax). Move activity-scoped and already-backstopped prose out to a `references/` dir and `_private`, keeping only the apex primordials + behavioral core + a lean "activity playbooks" index, so the every-turn load is roughly HALVED (~800-900 lines). The discipline-to-backstop map (built 2026-07-26): the safety-critical MECHANICAL disciplines already have a PreToolUse-hook or CI-gate backstop (`block-unbumped-version-commit`, `-branch-to-main-edit`, `-mandatory-offload`, `-on-open-findings`, `-unjustified-decision`, `-answered-question`, `-verification-pipes`, `-wrong-repo-tool`, `-repeated-tool-failure`, `-operational-without-private`, `-askuserquestion-unattended`, gate 78, and the D-series / gate-50 / gate-59 close-out gates), so THEIR prose can move freely (the hook is the guard, the prose only the explanation); the un-backstopped close-out habits need a new gate FIRST (phase 2); the judgment/behavioral disciplines stay lean in place. Phases are the `.Y` children; each closes on its own.

### 3.139.1 Phase 1: move the hook/gate-backstopped prose out (2026-07-26, M, M) `[machinery]`
Move the 390-line `## Session migration and PR close-out checklist` + the 136-line `## PR workflow` into a new `references/pr-lifecycle.md` (read at the PR-close-out boundary, like a skill), leaving CLAUDE.md a lean checklist that NAMES the enforcing gate/hook for each mechanical item. All of it is already backstopped, so relocation drops no live discipline. Biggest single cut (~530 lines). Update any pack-rule PROJECT-OVERLAY and gate-docstring pointers that reference the moved sections. Guard-validated.

### 3.139.2 Phase 2: build the paired-surface/stale-token delta gate, then move its prose (2026-07-26, M, L) `[machinery]`
Build a per-PR DELTA gate that flags a stale OLD value/surface left behind across the PR's changed files (the multi-surface-incompleteness / bare-token-width / paired-surface / §N-orphan / stale-token class the close-out checklist spends roughly half its length on), plus a CLAUDE.md-SIZE gate (warn above a line ceiling, preventing regrowth). Once those exist, the now-backstopped habits move out of CLAUDE.md. This phase UNLOCKS the deep cut. Guard-validated.

### 3.139.3 Phase 3: dedupe vs the pack + relocate cadence/mechanics (2026-07-26, M, M) `[machinery]`
Slim the 120-line `## Security and governance requirements` to a one-line index of the 15 pack rules (it currently re-describes them); reduce the cadence-SOP prose (matrix-fit / claim-fit / reference-audit / screen-publications / deep-assessment) to one-line pointers to their existing skills; move the worker-mechanics prose (delivery-tray, saturation, pin-to-SHA, codex-single-shot, guard-inputs) to `_private` as project-only operational. Guard-validated.

### 3.139.4 Phase 4: final pass to apex + behavioral core + lean index (2026-07-26, S, M) `[machinery]`
Final consolidation: what remains is the apex primordials + behavioral core (anything-wrong, defence-in-depth, completeness, communication conventions, operating-mode basics) + the `activity playbooks` index. Confirm the CLAUDE.md-size gate passes at the ~800-900-line target and no moved discipline lost its cross-references. Guard-validated.

### 3.118 Route the #1166 and #1167 sweep residuals (2026-07-25, M, S)

Five findings the two offloaded post-merge sweeps returned that were NOT fixed in the session-closing PR, deliberately kept out of it so the closing PR stayed narrow. From `validate-pr-1167`: **(a)** a worker can corrupt [`.working/worker-prompt-log.md`](.working/worker-prompt-log.md), which is the prompt injector's ONLY accountability record, so the log that exists to make keystroke injection auditable is itself unprotected; **(b)** a concurrent drop consumption crashes [`tools/audit-inbox-drops.py`](tools/audit-inbox-drops.py), which its own docstring says never exits non-zero, so the guarantee is false under a race; **(c)** a genuine drop whose filename ends in a staging-shaped suffix (`.log`, `.tmp`) is classified as staging and therefore reported as NOT awaiting a read, which is a false-negative in the one instrument watching that channel; **(d)** the orchestrator-session refusal in [`tools/manage-workers.py`](tools/manage-workers.py) keys on a session NAME rather than on a property, so renaming the orchestrator's session would silently disarm the guard against it prompting itself; **(e)** two unused imports. From `validate-pr-1166`: **(f)** [`tools/audit-delivery-status.py`](tools/audit-delivery-status.py) is mis-described as reading an OUTBOX in prose #1166 touched; **(g)** the merge-bypass log's scope sentence claims unbounded coverage while the backfill covers only one run's merges; **(h)** a factual claim about 15 GitHub PRs sits inside the very sentence arguing the backfill is not asserted, which is the shape of claim that needs its own evidence. Items (a) and (c) are the two that matter most: both are cases where an accountability or observability instrument fails in the direction that makes failure invisible, which is the class this project keeps finding.

**Rebased apply-candidate available** (`opus-worker-3118-rebase-and-routing-2026-07-25`, moved to `done/drops/2026-07/`): a worker delivered a candidate covering items (a), (d), (e) plus the `audit-inbox-drops` (b/c) fix, REBASED against #1169's `self_test()` rewrite in `manage-workers.py` (the original went stale on #1169; the rebase adopts #1169's `expect_refusal` helper, self-test 8→14). Re-verify at source and validate-then-apply when 3.118 is worked; the candidate is worker research, not a merge-ready diff.

### 3.117 A maintainer-placed inbox drop is invisible to every instrument (2026-07-25, M, S)

Found 2026-07-25 when the maintainer surfaced a 13KB codex deep assessment that had sat UNREAD in the file-drop inbox for an entire overnight run, along with a second unread drop of comparable size. Nothing detects that state: the file-drop root is outside every repository, so no audit gate walks it; [`tools/audit-delivery-status.py`](tools/audit-delivery-status.py) reconciles worker OUTBOX deliveries against the backlog, not maintainer-placed drops; and the orchestrator's own sense of "what needs processing" is built from the order queue, which a drop is never part of. **Consequence: the highest-value input available, an external read-only assessment with a sign-off request, was invisible to the one instrument set that is supposed to make work visible, and its discovery depended on the maintainer remembering it.** Two of its findings turned out to concern the assistant's own conduct (an unlogged branch-protection bypass) and to refute the assistant's own diagnosis of a worker fault, so the cost of not reading it was real rather than notional. Candidate fix, mirroring the shape of the delivery-status tool: reconcile the drop directory against a processed-marker (a `results/` archive copy, or a reference from any `.working` record), report anything unreferenced as UNPROCESSED, and surface it at `/resume` alongside the other standing registers. **Design care needed on two points:** the drop directory also holds transient orchestrator staging files (diffs staged for a worker to read), which must not be reported as unprocessed drops; and "processed" must not be inferred from mere file age, since an old drop can be unread and a new one already consumed. Advisory and cross-repo, the same shape as the other sibling-reaching tools, so it exits 0 and no-ops when the drop root is absent.

### 3.119 The Codex hook port is absent, so codex workers run unguarded (2026-07-25, M, S)

Confirmed absent at scratch HEAD, all three paths: `.codex/config.toml`, `.codex/hooks.json`, `.codex/hooks/worker-policy.py`. Found by the `codex-hooks-integration-test` order, which returned **NOT-READY** because there was nothing to probe: no `worker-policy.py` rule can be read, loaded, or exercised, so no hook-loading evidence can exist. **Why this matters beyond the missing files:** the Claude workers are guarded by 11 PreToolUse hooks, and the codex family has none, which is why the 2026-07-25 overnight decision restricted codex to read-only research and triage rather than treating the two families as equivalent. That restriction is a compensating control held by convention alone; the port is what would make it structural. It was carried in a session handoff as "PR-2b UNBUILT" and never reached this file, so it was one prune away from being lost, which is the tracking gap worth noting as much as the port itself.

**A second finding from the same order that this item does NOT cover, recorded so it is not conflated:** the worker also reported that the live codex user configuration at `/home/mailz/.codex/config.toml` carries no hook wiring, with a scan finding no `hooks.json` or `worker-policy.py` under that directory. The orchestrator CANNOT verify this (the path is not readable under its account), so it stands as the worker's evidence rather than a confirmed fact, and confirming it needs either the maintainer or a worker-side re-check. If true it means installing the project port alone would not be sufficient, because the user-level config would also need the wiring.

**Already fixed, so out of scope here (recorded to stop it being re-reported):** the same order's third finding, that a nested `AGENTS.md` below the launch directory is not auto-supplied as initial instructions under `codex --cd /home/grc`, was empirically probed (`NO` from a no-tool query) and is now closed by the launch-root dispatcher installed at `/home/grc/AGENTS.md`, whose own preamble names this failure. The delivery predates that fix.

### 3.148 Two gate-44 fail-open routes of the same class remain open (successor to 3.115; 2026-07-27, M, S)

Successor to 3.115 (four routes closed in #1208), tracking the two routes of the gate-44 subsection-representation fail-open class that #1208 did NOT close, per the re-verify's §7. **Make NO completeness claim about this class, only an ordinal one** (every completeness claim about it has been false: #1158 "the last route" and #1159 "the last reference-form route" were both wrong, caught by the very next sweep), and keep the false-positive census as the gate on any widening. The two open routes: **(1)** an INDENTED code block is not stripped ([`tools/lint-paired-skill-step-parity.py`](tools/lint-paired-skill-step-parity.py)'s `iter_non_code_lines` is fence-only by contract, so an identifier inside a four-space-indented block satisfies a subsection match on its own); **(2)** a table cell of ordinary WORDS that is semantically metadata, the residual of #1208's route (b), which closed only identifier-shaped-atom cells. For (2) the delivered recommendation is that it is NOT a strip-rule problem: the honest instruments are the existing `<!-- parity: command-exempt: <reason> -->` marker and an authoring convention, since a heuristic guessing at "metadata-ness" would be a silent fail-closed risk against prose. **(3) The CONVERSE over-strip residual of route (b)** (claude verify-3115, 2026-07-27): `SLUG_ONLY_CELL_RE`'s three-plus-segment branch is a SHAPE heuristic that cannot distinguish a machine-id slug (`parallel-execution-worker-fan-out`) from a multi-segment English compound (`state-of-the-art`, `up-to-date`), so such a compound in a metadata cell is wrongly stripped, a latent gate-44 FALSE POSITIVE (no registered command file carries one today; `command-exempt` is the escape hatch). The clearer slash-compound case (`read/write`) was fixed in #1208 by requiring a path indicator; the multi-hyphen case has no reliable syntactic signal, so it is documented and tracked rather than force-narrowed. When worked, weigh whether the route-(b) strip earns its keep at all against this over-strip risk. A THIRD, separate pre-existing accuracy gap to fold in when this is worked: the §5 grouped-summary at [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) describes gate 44 as "step-identifier parity" only and never mentions check 2 (subsection representation), which #1208 left as-is to stay focused on the four routes. Umbrella A / gate hygiene.

### 3.149 Colon-adjacent disposition ref is false-blocked by the open-findings grammar (successor to 3.126; validate-pr-1209 F-3; 2026-07-27, L, XS)

`block-on-open-findings.py`'s `_DISPOSITION_RE` requires whitespace (optionally markup) between the `FIXED`/`ROUTED` keyword and the ref, and `disposition_valid` strips `*_`\[\]` but NOT `:`, so a colon-adjacent form (`ROUTED: 3.56a`, `FIXED: #1210`) in `## Open` would false-block the PR create. Latent today: the 8 migrated rows carrying a `ROUTED:`/`FIXED:` first token all live in `## Closed today` (not grammar-checked) and `## Open` is currently empty. The 3.126 contract deliberately allows "whitespace OR markup only between" the keyword and the ref, so a colon is arguably out of contract by design; the fix (if taken) is to allow an optional `[:,]` immediately after the keyword before the ref, with a self-test fixture, OR to document the colon exclusion in the ledger legend so authors use the whitespace form. Weigh fix-vs-document when worked; any grammar change to this PR-blocking guard gets dual-family adversarial verify (both false-pass and false-block directions). Umbrella A / gate hygiene.

### 3.150 Gate-50 `pending`-state recall hardening (successor to 3.120; #1210 pre-push verifier findings; 2026-07-27, M, S)

The #1210 pre-push verifier UPHELD the `pending`-state classifier logic but surfaced three latent false-PASS (recall) gaps in `lint-bookkeeping-parity.py`, all in the safe direction (none spuriously fails the gate) and none a defect in the added code, routed here for hardening: **(1) recall brittleness (LOW):** a stranded row phrased outside the three tokens (`DISPATCHED` / `RESULT PENDING` / leading-`PENDING`) escapes as `normal` (`**OFFLOADED as validate-pr-N**`, `order sent, result not back`, `QA offloaded, awaiting delivery`); honest to the CURRENT convention but not paraphrase-robust. **(2) subsumption-arm collision (LOW-MED, pre-existing):** a stranded row worded `**NOT RUN yet, offloaded**` classifies `subsumption` (the `SUBSUMPTION_FINDINGS` `NOT\s+run` matches first and steals it before the pending arm) and reads GREEN; the live #1169 row's "NOT YET RUN" spelling defeats `NOT\s+run` and correctly falls through to `pending`, so the collision bites only the adjacent "NOT RUN" wording. Not introduced by #1210 (subsumption arm unchanged) but it caps the new check's completeness. **(3) stale-overwrite (LOW, latent, not triggered):** `parse_validate_pr_status` does `status[pr] = row_status` per row, so for a MULTI-row PR the last-iterated (oldest) row wins; a newer `RETURNED` row above an older `DISPATCHED` row would classify `pending` (a false-BLOCK), newly weaponized because `pending` is a failing state, but not currently triggered since the consumption convention edits the row IN PLACE (one row per PR). Candidate fixes: widen the pending token set to a recall-oriented marker family with a false-positive census; make the subsumption/pending arms mutually exclusive (require an affirmative subsumption/exemption marker, not a bare `NOT run`); and pick the NEWEST row per PR (or refuse on multi-row divergence). Any change to this active QA gate gets dual-family adversarial verify. Umbrella A / gate hygiene.

### 3.151 exec-dispatch's dispatch/eligibility error lumps "model not offered" with "account limited", enabling a false "fleet out" read (2026-07-27, M, S)

On 2026-07-27 the orchestrator probed and dispatched with full model IDs (`claude-opus-4-8`, `gpt-5-codex`) while [`tools/exec-dispatch.py`](tools/exec-dispatch.py)'s account config offers models by SHORT name (`opus`, `gpt-5.6-terra`), so `eligible_accounts` correctly returned empty and the dry-run reported `(no eligible account)` while `--dispatch` said `unavailable, limited, or model not offered`. The orchestrator misread this as a fleet-wide cap and self-ran three QA passes (validate-pr-1209, the #1210 pre-push verifier, the #1211 six-PR catch-up) on scarce orchestrator credits that should have been OFFLOADED; a live dispatch with `opus` then succeeded in 10.4s, confirming the fleet was available the whole time. The eligibility LOGIC is correct; the ERROR MESSAGE is the defect (the guard-input-clarity / distinguish-the-states class, same family as the `manage-workers.py` and saturation-observable work). Fixes: **(1)** in `--dry-run`, when 0 accounts pass the model filter, print per-account `model 'X' not in offered set [opus, fable, sonnet, haiku]` rather than a bare `(no eligible account)`, and suggest the nearest offered name; **(2)** in `--dispatch`, split the single `unavailable, limited, or model not offered` message into the ACTUAL cause (model-not-offered-here-[list] vs limited-until-Y vs usage_state != available); **(3)** consider accepting the full model IDs as aliases for the short names, or surfacing the offered names in `--help`. Any change gets a self-test. Orchestrator-side tooling, not pack. (The durable short-name reference is recorded in `.working/session-handoff.md` and `.working/next-prs.txt`.)


### 3.152 Register `Owner Role` cell vs each document's own `**Owner:**` metadata is unguarded, with 27 live divergences (2026-07-28 deep-assessment c2, both families, H, M)

Nothing compares [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md)'s `Owner Role` column to the target document's own `**Owner:**` field; both are individually legal roles so `lint-roles.py` cannot see the conflict. The claude lens re-derived **27 live divergences** across 312 rows (e.g. `policy-exception-and-risk-acceptance-management.md` register `Chief Risk Officer` vs doc `Chief Information Security Officer`, orchestrator-verified). Build a gate comparing the two, and reconcile the 27 (each a per-document decision on the authoritative owner).

### 3.153 Forward/reverse crosswalk pair-consistency is unenforced (an A.8.29 outlier is live) (2026-07-28 deep-assessment c2, H, S)

No tool references [`governance/matrix-reverse-framework-control-crosswalk.md`](governance/matrix-reverse-framework-control-crosswalk.md); its own "the two matrices are pair-consistent" assertion is unchecked. Row `:64` maps `A.8.29` to the pen-test doc whose own alignment table carries no `A.8.29`. Build a pair-consistency gate: each reverse-crosswalk row's control appears in the target doc's alignment table.

### 3.154 Matrix `N/A` is an unaudited escape hatch + semantic-mapping blind spot (2026-07-28 deep-assessment c2, M, S)

`lint-matrix-control-codes.py` accepts `N/A` unconditionally at three sites; `matrix-grc-compliance-alignment.md:385` carries AICM `N/A` while its CCM cell cites `AIS-04/05`, violating the column key. Semantic mapping correctness is the `/matrix-fit` cadence's job, but consider gating a bare `N/A` where a sibling framework column is populated.

### 3.155 Cross-document statutory-date coherence is untracked beyond one term (2026-07-28 deep-assessment c2, M, S)

`lint-cross-doc-numbers.py` tracks only the GDPR 72h window; the Colorado AI Act "30 June 2026" date is restated in 4 files with no gate comparing them. Widen the cross-doc-numbers gate to a curated statutory-date set.

### 3.156 Role-vocabulary closure does not cover body prose (2026-07-28 deep-assessment c2, M, S)

`lint-roles.py` scopes to the two metadata fields only; `Service Owner` (SLM:74) and `Incident Commander` (used 22x) carry normative authority in body prose but are absent from `register-role-authority.md`. Extend role-closure to body-prose authority roles.

### 3.157 Metadata `Classification`/`Confidentiality` allowed-value sets are unenforced (2026-07-28 deep-assessment c2, M, S)

`lint-metadata.py` enforces `ALLOWED_TYPES` for `Document Type` only; `Classification` and `Confidentiality` are presence-only, so changing a doc to `Classification: Restricted` passes all 78 gates while contradicting the CC BY-SA public basis. Add allowed-value sets.

### 3.158 Gate-50 `SUBSUMPTION_FINDINGS` fail-open: incidental "not run" prose mis-classifies a row as exempt (2026-07-28 deep-assessment c3, M, S)

The regex `SUBSUMED|NOT\s+run|maintainer[-\s]authori...` matches anywhere in a Findings cell, evaluated BEFORE the pending check, so 3 ordinary rows (#1186 "do not run --prune", #1044 "did not run the grep", #1035) are mis-classified as exemption rows. A future genuinely-pending row carrying such prose escapes Check 1, a fail-open in the very check TODO 3.120 built. Scope the marker to an authorization context (a dedicated token/cell), not incidental prose. [`tools/lint-bookkeeping-parity.py`](tools/lint-bookkeeping-parity.py):189-190,301-306.

### 3.159 Gate-50 naive pipe-split misparses ledger rows with inline `| pending |` code (2026-07-28 deep-assessment c3, M, S)

`lint-bookkeeping-parity.py:274-276,300` uses `line.split("|")`; inline `| pending |` code in a cell shifts columns. Census at the pin: 12 malformed rows in `validate-pr/history.md`, 18 in `improvement-log.md`. Benign only because `RETURNED` precedes the first inner pipe; a `DISPATCHED`/`PENDING` token after one reads as `normal` (fail-open). Escape cell pipes and/or make the parser code-span-aware; also restore the 5-cell #1169-#1172 rows to 7 columns.

### 3.160 An abbreviated `/validate-pr` stands as the QA-of-record for a gate-logic change (#1210) (2026-07-28 deep-assessment c3, both families, M, S)

#1210's validate-pr row records `RETURNED: PASS, SHIP` while its own text admits "a LIGHTER pass" self-run with no maintainer authorization, for a PR that changed gate 50's own detection logic; #1179/#1172/#1171/#1170/#1169 were one subagent run at ~66s/PR (vs 159-372s/PR formal), no abbreviation disclosure. Re-run a proper `/validate-pr` on #1210's gate-50 change to confirm the logic is sound; the discipline gap is recorded.

### 3.161 The GFM delimiter row in the QA ledgers sits at file-end, not after the header (2026-07-28 deep-assessment c3, M, XS)

`validate-pr/history.md` and `improvement-log.md` carry their table delimiter at the FILE END below all data rows (improvement-log has a duplicated delimiter), so the tables technically have no header-delimiter. Gates pass and the web generator renders, so it is latent; #1201's N1 "delimiter below the two newest rows, ACCEPTED" disposition rests on a description wrong by ~356 rows. Decide whether to correct or document the shape.

### 3.162 The deep-assessment register self-contradicts its own phase state (2026-07-28 deep-assessment c3, L, XS)

`deep-assessment/register.md:31` records r4 `P1..P7 = complete` while the r4 detail file still lists 6 phases `NOT-STARTED`; its `P8` cell holds `signed-off`, outside the documented per-phase vocabulary and post-#1213 sign-off removal; the r2 continuation paragraph sits out of run-order. The register is declared the durable phase-state a bare `/deep-assessment` resumes from, so the contradiction matters.

### 3.163 The #1209 retro row carries a refuted migration count (2026-07-28 deep-assessment c3, L, XS)

`improvement-log.md` #1209 row asserts "the 49-row migration was deterministic" while the #1209 validate-pr F-1 corrected it to 48 (DONE.md says 48); the retro was written in the same PR that landed the correction and still carries the refuted count.

### 3.164 QA-ledger stated-rule-vs-content drifts (incl. bypass-log within-date ordering) (2026-07-28 deep-assessment c3, L, XS)

`merge-bypass-log.md`: the "15 rows above" retrospective pointer is stale (backfilled set #1151-#1165, later rows appended below); the #1151 floor is not stated as an inception boundary; the "newest first within a date" order is violated (2026-07-28 rows read #1215,#1216,#1217,#1218 ascending). `improvement-log.md` "one row per merged PR" omits the handoff carve-out gate 50 correctly encodes. Reconcile the stated rules to the (correct) content.

### 3.165 `audit-worker-saturation.py` reads an UNREADABLE plane as absent, yielding a false NO-WORKERS (2026-07-28 deep-assessment c4, both families, H, M)

An EACCES on the scratch inbox iterdir is read as ABSENT, so the plane collapses to an empty set and the verdict is `NO-WORKERS` while a live worker sits in `inflight.json` (the claude lens reproduced it with its OWN worker entry). `NO-WORKERS` is the one verdict that licenses self-running QA, so a false one defeats the mandatory-offload rule; `--oneline` suppresses even the partial-plane caveat. Route unreadability into `verdict()` as a REFUSE-TO-ASSERT and replace `is_dir()` gates with an `_entries()` distinguishing absent/empty/unreadable. Higher priority than the TF-1 review (this is a confirmed live fail-open).

### 3.166 `audit-delivery-status.py` is single-plane, missing live file-drop deliveries (2026-07-28 deep-assessment c4, codex, H, S)

It reads only the scratch inbox manifest; live `collect-deliveries --dry-run` showed 47 file-drop deliveries while delivery-status reported "nothing to report" because scratch was absent, the same single-plane blindness already fixed once in the saturation tool. A "backlog cleared/applied" claim from it can omit live deliveries. Read both planes.

### 3.167 `collect-deliveries.py` fail-opens (TOCTOU, dry-run mislabel, collision race, EACCES traceback) (2026-07-28 deep-assessment c4, both families, M, S)

(a) TOCTOU between the sentinel-read and `os.replace` (an atomic replace between them sweeps an incomplete body); (b) `--dry-run` reports "collected" for WOULD-COLLECT planned moves, understating pending in a sitrep; (c) collision `tray_exists` checked at discovery not before `os.replace`, overwriting a same-name delivery; (d) an EACCES outbox yields a traceback with no stdout. Add an `_entries()` sibling, a dry-run-aware summary, an attribution cross-check vs the body, and move-time re-validation.

### 3.168 `exec-dispatch.py` eligibility diagnosis collapses distinct causes into "no eligible account" (2026-07-28 deep-assessment c4, both families, M, XS)

Model-mismatch, rate-limit, unavailable, and no-capacity all collapse to one message, so an operator can infer fleet exhaustion and self-run (the #1210/#1211 misread). Extends TODO 3.151. Also REOPEN `open-findings.md`'s #1205 zero-match-exclusion closure claim, which the claude lens judged over-stated.

### 3.169 The permission-denied (EACCES) case is in none of the four delivery-tool self-tests (2026-07-28 deep-assessment c4, claude, M, S)

Add an EACCES fixture to the self-tests of `audit-worker-saturation.py`, `collect-deliveries.py`, `audit-delivery-status.py`, and `manage-workers.py`, so the unreadable-plane path (3.165/3.167) is regression-covered.

### 3.170 "Secret scanning" is cited as ISO `A.8.10` in three files (2026-07-28 deep-assessment c1/#1219 verifier, M, S)

`.claude/rules/cicd-gates.md:136`, `dev-security/claude-rules/pipeline/cicd-gates.md:127`, and `dev-security/standard-devops-security-requirements.md:207` cite `A.8.10` (Information deletion) for secret scanning. Either A.8.10 is wrong there too or the concept differs from "secrets management" (fixed to A.8.24 in #1219); decide one answer (likely A.8.28 secure coding or A.8.24) and apply consistently.

### 3.171 NIST SP 800-63B cited as Rev. 4 by name while carrying Rev. 3 substance (2026-07-28 deep-assessment c5, claude, H, M)

Three sites name Rev. 4 but use Rev. 3 section numbers/substance (the highest-severity instance of the label-drift class). Decide the intended revision and reconcile the citation and the content together.

### 3.172 ISO/IEC 27033-1 title internal conflict (2026-07-28 deep-assessment c5, claude, M, S)

`operations/standard-network-security-and-segmentation.md:172` and `security/policy-network-communications-security.md:147` print "Network Security Architecture and Segmentation" while the corpus's own `register-canonical-citations.md:69` records Part 1 as "Overview and concepts". Align the printed title to the register (27033 is not held, so the register arbitrates).

### 3.173 NIS2 size cap cited as Article 3 (held Art 2(1) has no figures) (2026-07-28 deep-assessment c5, claude, M, S)

`compliance/annex-nis-2-implementation.md:36` cites "Article 3" for the size cap; held Art 2(1) (not Art 3) states no figures, incorporating Recommendation 2003/361/EC by reference, and the flat "or" loses the Recommendation's conjunctive headcount test. Fix the article reference and the phrasing.

### 3.174 Citation-precision phrasing (72h-from-confirmation, PR.AA title, joint-controller allocation) (2026-07-28 deep-assessment c5, codex, M, XS)

`security/procedure-security-incident-response.md:175` says GDPR "72 hours from confirmation" vs the statutory "after becoming aware"; the PR.AA title is truncated at `matrix-reverse:92`; the joint-controller allocation at `template-joint-controller:109` is informed-not-prescribed. Phrasing corrections (a `/claim-fit`-class batch).

### 3.175 Acquire the load-bearing references the reference base does not hold (2026-07-28 deep-assessment c5, both families, H, L; maintainer-gated acquisition)

Confirmed not-held and load-bearing: ISO 22301:2019 (6+ resilience clause-title claims), ISO/IEC 27033 (all parts), ISO/IEC 27007, ISO/IEC 27014, Commission Recommendation 2003/361/EC, and primary privacy law for 16 corpus jurisdictions (china/india/indonesia/kenya/malaysia/new-zealand/nigeria/philippines/saudi-arabia/singapore/south-africa/switzerland/thailand/turkey/uae/vietnam). Every deadline/threshold in those annexes is unadjudicable until acquired. Route to the maintainer source-acquisition queue per the missing-reference SOP; do NOT adjudicate from memory.

### 3.176 Printed-title-vs-catalogue-title check (mechanize the label-drift meta-pattern) (2026-07-28 deep-assessment c5, claude, M, M)

Component 5's meta-pattern: mis-citations are not invented codes (existence gates + 1916 CSA codes clean) but hand-written LABELS substituted for catalogue titles, wrong ~half the time, which `/matrix-fit` cannot catch (it judges code fit via reference-module titles, never the corpus's OWN printed titles). Build a check that diffs corpus-printed control/clause/standard titles against held catalogue titles.

### 3.178 Pack drop-in install leaks a private path and yields 18 dead links (2026-07-28 deep-assessment c6, claude, H, S)

`dev-security/claude-rules/CLAUDE.md:58`'s crypto table defers to `security/policy-encryption-and-key-management.md` as canonical mandate, which a pack-only (mode-3) adopter does not have; the `cp claude-rules/CLAUDE.md ./CLAUDE.md` install (README:167-172) yields 18 dead links because the README never says copy the directory. Qualify the crypto reference and fix the install instruction.

### 3.179 Adopter vs auditor get opposite instructions about the same documents (2026-07-28 deep-assessment c6, claude, H, S)

The register classifies the Governance Library Charter `library-internal` ("adopters delete these") while the adopter guide says "if you read three, pick the Governance three (Charter + ...)". Plus the register index is overclaimed (README:78 says it lists every document with status and related artefacts; it has neither column and zero `docs/` rows), and the portal is blind to Adoption Disposition. Reconcile the routing.

### 3.180 Adopter-facing skills hard-require the private siblings with no degrade branch (2026-07-28 deep-assessment c6, claude, M, S)

`deep-assessment/SKILL.md` and `reference-audit/SKILL.md` require all three private siblings / the full suite to exit 0 before any semantic phase, with no absent/skip/not-applicable branch, so an adopter stalls at an unsatisfiable phase-1 precondition. Add an adopter degrade path.

### 3.181 The adopter on-ramp never mentions `/adopt`, siblings, or `.working` (2026-07-28 deep-assessment c6, both families, M, S)

No public adopter doc (`docs/adopter-guide.md`, `docs/template-quickstart.md`, `CONTRIBUTING.md`) mentions `/adopt`, `adopt-config`, the siblings, or `.working`, so an adopter can complete the entire documented on-ramp and then work on top of the maintainer's queue/handoff/QA registers. Surface `/adopt` in the on-ramp.

### 3.182 `.claude/` security-rule hollowness and mirror path rot are gate-invisible (2026-07-28 deep-assessment c6, claude, M, S)

`.claude/rules/external/kariedo/vulnerability-prevention.md` is a pure index to 6 never-vendored files; `.claude/rules/governance/trust-recovery-escalation.md` mirrors `../skills/...` paths dead in the `.claude/` tree (= component-1 finding). Both are uncaught because `.claude/` is in `DEFAULT_EXEMPT_DIRS` (no gate link-checks it). Vendor the companions or trim the index; make the mirror links tree-relative-safe.

### 3.183 Adopter-facing polish (changelog audience, fork-hook source edit, alarming clean-run output, closed-set framing) (2026-07-28 deep-assessment c6, claude, L, S)

The changelog top entries are maintainer jargon with no adopter banner; the adopter guide tells the adopter to edit `tools/lint_common.py` `DEFAULT_EXEMPT_DIRS` (a source edit that conflicts on every upstream pull); a clean adopter clone prints `ERROR: could not locate the grc_library_ref index` twice; and "five paths"/"seven areas" are framed as complete against 12 `docs/` files / 11 domain dirs. Low-severity adopter-experience cleanups.

### 3.184 Corpus ISO citation currency updates enabled by the 2026-07-28 `_ref` ingest (2026-07-28 ingest follow-up, M, S)

The 2026-07-28 `_ref` egress ingest (PR #105) now holds newer editions the corpus cites at older ones: update `ISO/IEC 27017:2015` citations to `:2026` (second edition supersedes; the corpus cites 2015 across the cloud-security docs and the matrices); update `ISO 19011:2018` citations to `:2026` (fourth edition); and resolve the `ISO/IEC 29134` `:2017`-vs-`:2023` inconsistency to `:2023` (held second edition). Verify each attributed value against the newly-held text (the 27017:2026 control set changed with the ISO/IEC 27002-based restructure, so a mapping review is warranted, not just a version-string bump).

### 3.185 The `TODO.md`-delete invitation similarly breaks ~12 corpus links (2026-07-28 deep-assessment c6, codex verify of #1221, M, S)

Split from 3.177 (closed in #1221, which fixed the `.working/`-delete half). The same false-safety class applies to `TODO.md`: it is a gate-exempt non-deliverable, yet corpus documents link into it, so an adopter who deletes or replaces `TODO.md` breaks ~12 links (verify the exact count at action time). FIX SHAPE: assess whether a delete of `TODO.md` is actually invited anywhere; if so, either add `TODO.md` to gate 53's `GUARDED_TARGET_DIRS` and sever the corpus->`TODO.md` links (the parallel of the #1221 `.working/` fix), or add a truthful caveat. Verify the 12-link figure before acting.

### 3.186 Gate 53 (directional-dependency) misses Markdown reference-style links (2026-07-28 codex verify of #1221, L, S)

`tools/lint-directional-dependency.py`'s `LINK_RE` matches only inline `](target)` links, so a reference-style `[text][ref]` link with a `[ref]: .working/...` (or `.project-governance/...`) definition evades the guard. Pre-existing limitation (predates the #1221 `.working/` widening; not introduced by it) and currently THEORETICAL (a corpus-wide grep found zero live reference-style links into either guarded tree). FIX SHAPE: extend the scan to also resolve reference-style link definitions before classifying, add a regression fixture for the reference-style shape. Low priority while no live evasion exists.

### 3.114 The advisory CHANGELOG-length tool is looser than the gate that enforces it (2026-07-25, L, XS)

[`tools/audit-changelog-entry-length.py`](tools/audit-changelog-entry-length.py) defaults to `--word-warn 130` / `--sentence-warn 65` while the PR-time delta gate [`tools/check-changelog-length-on-pr.py`](tools/check-changelog-length-on-pr.py) FAILS at `--word-max 100` / `--sentence-max 45`. So the advisory tool can report "all entries within the compact-form budget" for an entry the gate then rejects, which is false comfort at exactly the moment the author is trying to avoid a guard failure (it happened in #1157: a 108-word entry passed the advisory tool and failed D8). **Weigh rather than blindly align:** the looseness may be deliberate, because the advisory tool scans EVERY root entry including the long-form historical ones that predate the ceiling, whereas D8 scans only newly-added entries, so simply lowering the defaults could flag a large back-catalogue. Candidate resolutions: (a) have the advisory tool report against BOTH thresholds, naming the gate's ceiling as the binding one for new entries; (b) add a `--new-entries-only` mode that applies the gate's ceiling; (c) keep the defaults and state the divergence plus its reason in the module docstring, so a reader is not misled. Cheapest useful fix is probably (a) or (c).

### 3.113 Worker-id ownership is unvalidated, so two sessions can wear one id (2026-07-25, M, S)

Neither transport has any notion of worker-id ownership: file-drop `_touch_heartbeat` writes the heartbeat file unconditionally with no owner field, and git-scratch `cmd_register` treats a pre-existing registry row as a REJOIN and hands the colliding session the prior `held_order` and `held_token` without testing whether `last_seen` is fresh. On 2026-07-25 two live sessions wore `worker-20260716-a` at once. A candidate fix is already DELIVERED (`results/fix-worker-id-collision-phase1.md`, Recommendation 1 only: a session nonce plus a `--takeover` override, staged as layer 1 warn-but-serve then layer 2 refuse behind an opt-in, so rolling it out cannot wedge a live worker mid-order); the remaining work is orchestrator-side verification and apply, plus deciding when to flip layer 2 on. Do NOT implement the delivered draft's Recommendation 2 (auto-minted ids): that trade-off is the maintainer's and is unrelated now that workers self-mint. **This is also where N2 from #1157's pre-push verifier lands:** `tools/audit-worker-saturation.py` de-duplicates live workers by id across the two planes, so two distinct sessions sharing one id are counted as ONE live worker, under-reporting the fleet. That under-count is a symptom of the missing ownership validation, not a defect in the saturation tool, so it is fixed here rather than there.

### 3.109 Sweep 120: tooling-docstring and record-accuracy residuals (2026-07-25, L, S)

Low-severity Sweep 120 notes, grouped because each is a one-line accuracy fix in a tool docstring or a working record. Full evidence per finding in the Sweep 120 delivery.

- **`tools/lint-skill-internal-refs.py:23`** (gate 76) docstring lists a token class (`section N`) the code deliberately does not flag, and **`:22`** says PR refs match at "three-plus digits" where the pattern caps at five. Docstring-versus-behaviour drift in both directions.
- **`tools/lint-gate-citation-inventory.py:95`** (gate 77) parses the gate inventory from the WHOLE specification rather than the section-6 region, so an inventory-shaped line elsewhere in the spec would be read as a gate row. Behaviour change, so gate it with a fixture.
- **`.working/changelog-details/CHANGELOG-detailed.md:62`** asserts a validation guarantee for the exchange channel that the instrument itself declines to assert. Correct the record's claim to what the tool actually guarantees.
- **`TODO.md:31`** the Priority-1 preamble asserts no point-fix items are open while two P1 sections are open.
- **`TODO.md:53`** mixes bare-`scratch` and `_private` forms in the 1.19 block, against the repo-shorthand convention. The same class was fixed in `.claude/CLAUDE.md` at the Sweep 120 close-out.

### 3.3 CLAUDE.md removal-ledger review cadence (standing) (was 3.12)

Each `/retro` scans the `grc_library_private/claude-md-considerations.md` removal ledger's open RM entries and the periodic hallucination-metrics pass does a deeper scan; if an entry's "evidence the removal was wrong" signal appears, advise the maintainer to restore the cut text, and record the disposition in that entry's Status. Standing tracker; stays open by design.

### 3.6 Register-ageing advisory tool (GR-8 follow-on A, guardrail review 2026-07-02, L, S)

**NOT DEFERRED, LOW PRIORITY (last items) 2026-07-25.** The #698 over-flagging finding stands: the
pending heuristic cannot distinguish a genuine pending formal candidate from an informally-adopted one,
and an advisory tool whose noise gets it ignored is the one counterweight the defence-in-depth directive
names. The root cause is an OPTIONAL disposition token, so the fix order is: make the token mandatory in
the `/retro` row now, let it accumulate, then the tool becomes trivial. Deferral removed.

A small advisory `tools/audit-*.py` (not a gate) reporting improvement-log Proposed-improvement cells still pending after N PRs, the register-side analogue of the brief-freshness tool. **Attempted + deferred 2026-07-08 (#698) with a design finding:** the core heuristic (non-empty Proposed-improvement cell + no disposition token = pending) OVER-FLAGS (cannot distinguish a genuine pending FORMAL candidate from an adopted-in-place habit note; ~78 July cells mostly false-positive). Needs either a formal-candidate classifier or a register-format change (a structured candidate marker the `/retro` skill appends). Not shipped (an over-flagging advisory erodes trust). Revisit once the classifier / register-format decision is made.

### 3.7 Expiry-tail one-pass batch review (GR-8 follow-on B, guardrail review 2026-07-02, IN PROGRESS, M)

A drafted triage proposal (research subagent, orchestrator-verified) over the ~236 aged pending improvement-log candidates (pre-July rows), each with a proposed CODIFIED/EXPIRED/ROUTED/keep verdict, reviewed by the maintainer in one round; tokens land only on the maintainer's dispositions (rejection and expiry are maintainer calls per the register convention).

### 3.12 Bidirectional See-Also parity gate (r7 guardrails, M, M)

**BUILD, after the current tooling queue (decided 2026-07-25).** Reciprocity is mechanical (A names
B, so B must name A) and the miss is confirmed, not hypothetical. Measure the corpus first so it lands
green; if it does not, fix the corpus in the same PR rather than exempting.

[`skill-authoring-discipline`](dev-security/claude-rules/skills/skill-authoring-discipline/SKILL.md) step 6 requires a new skill's `## See Also` "Related skill" links to be reciprocated, but no gate enforces it (gate 32 checks only `derives_from`, gate 41 the README tree, gate 44 PAIRS step-parity). The `publication-screening` delta reproduced the miss (fixed in-window in the 2.11 build). Proposed: a parity gate that, for each skill A whose See Also links sibling B as a "Related skill", asserts B links back to A. Directly mechanizable. **Overnight-deferred 2026-07-15:** a new gate increments the gate count (69 to 70), which ripples into gate-count prose in the protected `.claude/CLAUDE.md`, so the item is drafted in `grc_library_private/deferred-protected-changes.md` item 9 (design + full surface list) for the daytime apply.

### 3.13 Expand the mutation-probe variant library, structured-surface gates (deep-assessment r1 R10 remainder, S)

[`tools/gate-mutation-variants.json`](tools/gate-mutation-variants.json) covered 5 gate classes (language, unbalanced-fence, secrets, links, metadata); the `/deep-assessment` coverage obligation wants each gate class to gain a phase-4 mutation-probe variant, and the library is designed to be extended run over run. **Extended in #768** with 2 append-testable classes, each a DETECT + CLEAN pair verified against the live gates: citation-denylist (`lint-citations.py`, `CSA CCM v5` detect / `CSA CCM v4.1` clean) and standards-currency (`lint-standards-currency.py`, `ISO/IEC 27001:2013` detect / `ISO/IEC 27001:2022` clean). **Remaining**: the structured-surface gates whose detection scans a SPECIFIC surface (not arbitrary appended prose), so an `append_file`/`create_file` payload to `@any-corpus-md` is not scanned by them: control-code (gate 49, the compliance matrix), retention-consistency (gate 55), and cross-doc-numbers. These need bespoke variants whose `create_file`/`append_file` action targets the exact surface the gate reads (e.g. a matrix-shaped fixture for gate 49), one careful variant per gate verified DETECTED by the probe before it lands. Incremental (run over run). **Advanced in #783** with a DETECT + CLEAN pair for the new gate-48 Check 5 (framework-as-column CCM/AICM family-validity, shipped #782): a `create_file` CCM-column fixture carrying `END-04` (probe verdict DETECTED) and one carrying valid `DSP-04, DCS-05` (CLEAN-PASS), both confirmed by `tools/audit-gate-mutation.py`. Check 5 is the one structured-surface check that IS `create_file`-testable, because gate 48 scans corpus-wide; the genuinely fixed-surface gates below (gate 49, the matrix; gate 55, retention pairs; cross-doc-numbers) still cannot be exercised by the probe's append-at-EOF / create-elsewhere actions (the mutation lands outside the gate's fixed target surface), so they need a probe-action enhancement (in-table insertion) that is a larger tooling change, kept for a future increment. Stays open (rescoped, not closed).

### 3.14 ETSI Securing-AI alignment map (L, M) (was 3.16)

Map the held ETSI SAI family (EN 304 223 plus the GR/TR set) against the corpus `ai/` security content: which requirements have no corpus carrier, which corpus claims an ETSI citation would strengthen, and a proposed alignment shape (options for maintainer scoping). Research DELIVERED (`inbox/worker-20260703-a/etsi-sai-alignment-research/`, 2026-07-04); the apply is a later decision. Citation form UNBLOCKED 2026-07-04 (the maintainer-supplied fresh EN 304 223 V2.1.1 copy; scratch PR #100).

### 3.31 `/reference-audit` per-touch staleness backstop (r6 guardrails, M, M; DEFERRED)

**BUILD as a PR-time delta check with a metadata-only carve-out (decided 2026-07-25).** A diff
changing only `Version` / `Date` lines is not a body change in the sense the obligation means; demanding
a reference-breadth run for a typo fix is the noise that gets a check bypassed.

The gate-50-analogue for the per-touch reference-breadth obligation the [`.claude/CLAUDE.md`](.claude/CLAUDE.md) close-out checklist added (a corpus-body-touching PR runs the per-touch tool and refreshes [`.working/reference-audit/doc-state.md`](.working/reference-audit/doc-state.md)). Nothing detects a body-touching PR that omits the per-touch run or the state refresh (the class gate 50 backstops for `/validate-pr` rows). Proposed: a PR-time delta check (a Dn) failing when a PR's diff touches a corpus-domain `.md` body without a matching `doc-state.md` row update or a recorded empty-set note. **DEFERRED (maintainer 2026-07-08) until AFTER the first FULL `/reference-audit` run** establishes the `doc-state.md` delta-anchor baseline (building the hard D8 gate before the baseline exists would fire on the next corpus-body PR). Sequencing: first FULL `/reference-audit` run (populates `doc-state.md`), THEN build this D8. Convention-guarded meanwhile.

### 3.33 Formalize the (severity, effort) convention across surfaces (S)

The `(severity, effort)` tags are in use in this file and the scale is now stated in the header, but the convention is not yet propagated to its sibling surfaces. When the convention formally lands, update: `library-fitness-review/SKILL.md`; `validation-sweep/SKILL.md`; the [`.working/DONE.md`](.working/DONE.md) heading shape; future fitness-review templates and sweep detail files. Schedule: after the current FR backlog closes.

### 3.38 Broaden gate-39 count-idiom coverage (log-mining #272/#465, mechanizable half, S)

Extend the gate-count-consistency audit ([`tools/lint-gate-count-consistency.py`](tools/lint-gate-count-consistency.py), gate 39) count-idiom detection to catch more count-claim phrasings (e.g. `N audits`, additional spelled-word-form numbers) so a stale collection-count in those phrasings is caught mechanically, with a regression fixture per new idiom. This is the **mechanizable half** of the recurring #272/#465 improvement-log candidate. Maintainer disposition (2026-07-10): "do what we can, enhance where possible, drop what won't work": the mechanizable gate-39 idiom-broadening is pursued here; the **free-prose-rule-count half** (parsing an arbitrary `the N governance rules` prose sentence, which no count gate can reliably do) is inherently un-gateable and is **DROPPED** (recorded, not pursued). Scope to gate 39's existing pattern family; do not attempt free-prose parsing. Mined 2026-07-10 (sweep94 log-mining pass). **Assessed 2026-07-15 (overnight):** the mechanizable idioms are largely already covered, the digit forms by P1-P8 (P8 handles `N automated audits`, with a bare `N audits` deliberately EXCLUDED as FP-unsafe on audit-event counts) and the word forms by P9-P12. The remaining FP-safe residual is narrow (e.g. a DIGIT `N governance rules` sibling of the word-form P11, since `governance rules` is specific enough to avoid the bare-`audits` FP problem) and needs a careful per-idiom corpus census plus a tightly-scoped pattern plus a fixture, better done attended / fresh (a mis-scoped idiom over-matches prose and reddens CI). The un-gateable free-prose-rule-count half stays DROPPED per the 2026-07-10 disposition.

### 3.43 Gate-48: non-parsing-token check inside CCM/AICM-headed columns (`/retro` #784, design + FP-analysis needed, S-M)

The `/retro` for PR #784 surfaced the **4th invalid CSA control-code family this session** (`ISM` fixed in #769, `END` fixed in #781, `GVN` fixed in #782, and now the `AI-TM`/`AI-SC`/`AI-PP`/`AI-AU`/`AI-EC` pseudo-codes in `ai/standard-ai-and-agentic-development-security.md` §36). The first three share the well-formed-but-wrong-family `DOMAIN-NN` shape that gate-48 Check 5 (added in #782) now catches; the §36 family is a **distinct shape Check 5 is blind to by construction**: the `AI-XX-NN` pseudo-code has a hyphen before the domain token, so the gate-48 `CODE_RE` excludes it exactly as it excludes the corpus-internal `AI-GOV`/`MODEL-GOV` identifiers. It was caught by the high-assurance review, not a gate. Proposed: extend gate-48 (a Check 6, or widen Check 5) to flag, within a column whose header anchors to `CSA CCM` / `CSA AICM` (reusing `CCM_COLUMN_HEADER_RE`), any non-empty cell token that does NOT parse as a valid CCM/AICM code at all, with an allow-list for legitimate non-code cell content (prose notes, `n/a`, blank). The FP risk is the design work: a CCM/AICM-headed column can legitimately carry non-code prose, so the check needs a tight token-shape gate (only flag things that LOOK like a code, e.g. `[A-Z][A-Z&]{1,4}-\d`, but are not in `CCM_FAMILY`) rather than flagging every non-code cell. Ship guard-first with fixtures (a detect case for the `AI-XX-NN` shape, a clean case for a legit prose cell). Surfaced by the #784 retrospective 2026-07-10. **Live instance found 2026-07-15 (FP-census, overnight; blocks guard-first):** `dev-security/guideline-ai-coding-assistant-security.md` §Framework alignment has a `CSA AICM` column citing 7 fabricated `AI-GOV-01`/`AI-DATA-01`/`AI-SEC-02`/`AI-SEC-03`/`AI-GOV-03`/`AI-SEC-04`/`AI-INC-01` codes (none valid per the held AICM v1.1.0 catalogue; gate 48 blind to them via the `CODE_RE` lookbehind). Guard-first requires fixing this live instance FIRST (else a correct Check 6 fails the corpus at 69/69), and the fix is a semantic matrix-fit judgment (which real AICM code per row) routed to the maintainer in [`.working/pending-decisions.md`](.working/pending-decisions.md). Do the `/matrix-fit` remap (or column removal), THEN build Check 6 guard-first. FP-census note: the naive "flag all multi-segment tokens in a CCM/AICM column" design is NOT FP-safe by construction alone (those 7 tokens are exactly multi-segment), so the census-then-fix ordering is load-bearing.

### 3.47 TODO adoptability: strip internal working-provenance annotations (S)

TODO items carry internal working-provenance that an adopter reading the backlog does not need and that clutters the file: date-stamped `maintainer-directed YYYY-MM-DD` tags, `Surfaced ... during #N` and `Mined ... (sweep N ...)` origin lines, PR-number and sweep-lineage annotations, and residual `(was X.Y)` renumber breadcrumbs. This provenance lives durably in git history, the DONE ledger, and the CHANGELOG; the forward-looking TODO should read as a clean, adoptable backlog of what remains. Sweep the open items to remove these annotations, keeping the actionable content, the stable id in each heading, and the `(severity, effort)` tag. Standing convention going forward: new TODO items omit date, PR, sweep, and maintainer-directed provenance. **SCOPE RESOLVED 2026-07-15 (maintainer):** strip only the date / `Surfaced #N` / `Mined (sweep N)` / PR-number / maintainer-directed provenance, and KEEP the `(was X.Y)` renumber breadcrumbs (per the #929 convention that "existing breadcrumbs stay for resolvability"). Still attended-preferred, not an unattended sweep: a ~85-item single-file editorial pass over the most cross-referenced working file with weak mechanical verification that each item's actionable content survives intact, so it wants fresh-context per-item care. Queued for an attended/fresh session.

### 3.54 Back-fill and surface the `doc_type` facet in grc_library_ref (maintainer-directed 2026-07-12; DISPOSITION 2026-07-24: populate-on-touch + low-priority back-fill; meticulous, maintainer-collaborative, explicitly NOT automated; L, XL)

**Disposition (2026-07-24, maintainer decision):** populate the facet OPPORTUNISTICALLY as `grc_library_ref` items are touched during other work (the primary mode now); the full ~541-item back-fill is a LOW-PRIORITY dedicated pass for when nothing more important is queued, not a campaign to start now. Reference-base (`grc_library_ref`) follow-up. **Context (done, merged):** a `doc_type` facet was added to `grc_library_ref` (ref PR #57): an OPTIONAL, controlled document-type field in `catalogue.yml`, with a controlled vocabulary in `doc-types.md` (values: standard, guideline, framework, code-of-practice, report, regulation, program, template, questionnaire, book) enforced by `grc_library_ref/tools/validate.py`. It is ORTHOGONAL to the trust bucket an item sits in. It is currently populated on exactly ONE item (the ESA Joint Guidelines JC/GL/2024/34 in `frameworks/`, `doc_type: guideline`); the other 541 of 542 catalogued items are untagged.

**Scope (two coupled parts):** (1) Back-fill `doc_type` across the existing catalogue (542 items: standards 241, frameworks 132, legislation 74, publications 32, programs 25, books 22, templates 16). (2) Surface `doc_type` in a generated view (e.g. a "by document type" grouping in `INDEX.md`, which `build_router.py` generates). Part 2 is only worth doing AFTER part 1 has meaningful coverage; a facet view over one tagged item looks broken.

**Why careful and NOT automated:** many per-item judgement calls; classifying by title is a trap (ISO 31000 "Risk management, Guidelines" and the NIST SP 800-63 "Digital Identity Guidelines" series are formal STANDARDS by issuer, NOT `doc_type: guideline`) — classify by the issuer's instrument designation, not by a word in the title. A wrong tag is worse than an absent one: it silently corrupts any filter built on the facet. Some buckets are near 1:1 with `doc_type` (legislation->regulation, templates->template, programs->program, books->book) and add little value; the value concentrates in `standards/`, `frameworks/`, and `publications/`, which are also the most ambiguous. NO bulk sweep, NO scripted auto-classification. Approaches to WEIGH (not pre-decided): phased-by-bucket (near-mechanical buckets first, judgement buckets after) vs. populate-on-touch (tag items opportunistically as they are edited for other reasons).

**Process expectations:** LOW priority; schedule only when the maintainer has time to engage deeply. Expect roughly 20 clarifying questions up front, then MULTIPLE iterations of a written plan for maintainer review, with explicit maintainer sign-off BEFORE any catalogue edits are committed. This is `grc_library_ref` work, gated by ref's `tools/validate.py`; develop on ref's designated branch and merge per ref's ingest/merge SOP (cross-repo PR; the local git proxy 403s direct pushes to ref).

### 3.56 Pack-hygiene Phase-4 routed cleanups + mechanization candidates (pack-hygiene Phase-4 close, S-M)

**Numbering: LEAVE AS IS (maintainer-decided 2026-07-25c).** This item is tracked as `3.56` while
[`DONE.md`](.working/DONE.md) records three post-rule partial closes against `3.56a` (2026-07-24, PRs #1139,
#1138 and #1135). The ids genuinely differ, so nothing resolves to the wrong item and gate 78 is CORRECT to stay
silent; no `EXEMPT` row is needed or wanted. Normalizing either side would make the gate fire three times on
three legitimate partial closes, requiring three exemption rows that exist only to silence a self-inflicted
firing, and a dead row dilutes an auditable record. Recorded here so the question is not re-opened.

Routed from the pack-hygiene Phase-4 triage (full detail: `.working/pack-hygiene-acceptance/2026-07-12-phase4-acceptance.md` (swept to the grc_library_private archive by the §1.22.3 initial sweep; git history retains it)). (a) Three proposed cheap mechanizations (guardrail-machinery candidates, maintainer-decision): a linter scanning skill bodies outside the wiring section for internal-reference token classes (convention-erosion guard); an instrument mapping "gate N (name)" citations in wiring sections/command stubs to the §6 inventory (renumbering guard); the provenance register as a gate-41 enumeration surface (a new rule cannot ship without its entry) **[BUILT (3 of 3; part (a) COMPLETE): the provenance-register-as-gate-41 mechanization is gate 41's fourth rule-enumeration surface (rule-provenance.md under `## Governance rules`); the skill-body internal-ref-token linter is gate 76 (tools/lint-skill-internal-refs.py); and the "gate N (name)"-to-§6-inventory renumbering guard is gate 77 (tools/lint-gate-citation-inventory.py). §3.56a part (a) is done; parts (b) command-stub co-updates, (c) cosmetics, (d) maintainer flags, (e) pack notes remain open below]**. (b) Apply-time command-stub co-updates: the `/fitness` stub's ten-persona step heading; the `/retro` stub's concrete register format. (c) Small pre-existing accuracy cosmetics: vetting-log "Spot-scanned" vocabulary + the line-254 summary; the validation-sweep zero-finding record/register wording; the session-lifecycle "prevented by luck" phrasing; `.working/README.md` activities inventory stale for 8 pre-existing subdirectories; adoption-path numbering (pack 1/2/3 vs adopter-guide A/B/C); root-README "claude.md" lowercase option headings (anchor-safety check first). **ASSESSED 2026-07-13 (c is a partially-stale grab-bag, deferred to attended):** spot-checks found the session-lifecycle "prevented by luck" phrasing and the root-README lowercase-"claude.md" option headings NOT present (already resolved or mislocated), while the vetting-log "Spot-scanned" vocabulary and the docs adoption-path A/B/C-vs-1/2/3 numbering ARE present but each needs the `.working/pack-hygiene-acceptance/2026-07-12-phase4-acceptance.md` (swept to the grc_library_private archive by the §1.22.3 initial sweep; git history retains it) detail plus target-file reading to fix accurately, low-value per-item archaeology better done as one attended pass over the Phase-4 detail than as scattered overnight edits; the `.working/`-tree cosmetics (vetting-log, validation-sweep record, `.working/README.md` inventory) are gate-exempt and non-urgent. (d) Two defensible-judgement flags for the maintainer: the pack README "shaped by the parent library's real maintenance practice" wording; "authoritative" for the reference-audit motivating source. (e) Sweep-100-routed pack project-flavour notes (out-of-window, note-level, low-confidence; neither contradicts the narrowly-worded #846 asserted-clean property): [`dev-security/claude-rules/governance/change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) line ~73 uses `.claude/`/`.working/` directory paths as illustrative examples in a scrubbed pack rule (candidate to genericize to a placeholder path); [`dev-security/claude-rules/governance/project-integrity.md`](dev-security/claude-rules/governance/project-integrity.md) line ~98 names "the consuming GRC library's corpus principle document" (project-integrity was Phase-1 condensed, not Phase-3-scrubbed, so outside the acceptance-sweep scope; candidate to reword to "the consuming library"). Both are optional strict-project-agnosticism polish, protected-file class.

### 3.57 Reference-breadth new-ingest apply (held-but-uncited over the 63 2026-07-12 ref sources, M)

**KEPT OPEN for the Medium rows specifically (decided 2026-07-25).** The High and version-sensitive
`[V]` rows are applied across #866-#883, each verified verbatim against the held source and
currency-confirmed. The Medium residual is treated as real queued work rather than left to the standing
per-touch cadence.

The reference-breadth new-ingest apply wave over the 63 2026-07-12 ref sources (the `grc_library_scratch` PR #163 delivery, `inbox/reference-breadth-2026-07-12/`) is **complete**: all High rows plus the maintainer-named version-sensitive `[V]` rows were applied across #866-#883, each verified verbatim against the held source, upstream-currency-confirmed this turn, refute-verified, and each with a canonical-citations register row (rotated to [`DONE.md`](.working/DONE.md)). **ONE residual keeps this item open:** the deferred **matrix TSC-column mapping** (register-coverage-gaps line 170), a single-file sensitive change needing a `/matrix-fit` follow-up, not the from-scratch citation apply the wave was. When it is scheduled and closed, rotate §3.57 to DONE. See [`pending-decisions.md`](.working/pending-decisions.md).

### 3.60 Per-process test-fixture tempdir to eliminate the concurrent-suite race (surfaced 2026-07-13, S; spun off from the read-only-git codification closed in #870/#871)

The regression suite ([`tests/test_linters.py`](tests/test_linters.py)) builds and removes shared fixtures under `tests/tmp/`, so two concurrent `run_all_audits.sh` runs (the orchestrator's own plus a dispatched subagent's) race on those fixtures and produce spurious gate-36 `FileNotFoundError` failures. #870 and #871 codified that such a failure is a concurrency artefact to re-check standalone (the awareness mitigation), but did not remove the race itself. The deeper fix is to give each suite run its own fixture tempdir (per-process or per-run, e.g. `tempfile.mkdtemp`) so concurrent runs cannot collide. **ASSESSED 2026-07-13 (not a small change):** the fixtures are entangled at ~14 `tests/tmp/` sites in [`tests/test_linters.py`](tests/test_linters.py), including content-embedded `Repository Path` fields (which the metadata linter path-matches), path-based test arguments and assertions, and the orphan-document test's semantic dependence on `tests/tmp/` being a location OUTSIDE the referenced corpus (a random `/tmp` tempdir could change orphan-detection behaviour). So `FIXTURE_DIR` cannot simply become a `mkdtemp`; a per-run refactor must also make each path-dependent fixture derive its embedded path dynamically and preserve the orphan-test's outside-the-corpus semantics. It is a dedicated multi-site refactor, non-urgent, for a fresh session; the interim awareness-mitigation (#870/#871: a shared-fixture-race failure or a not-yet-committed-sibling completeness flag is a concurrency artefact to re-check standalone) stands as the control. Spun off from the read-only-git subagent-rule codification (closed in #870 and #871).

### 3.73 Ledger-table-row-integrity check for the `.working/` bookkeeping tables (Sweep-103 `/validate-pr` escape #915, 2026-07-14, S-M) `[machinery]`

**BUILD AHEAD OF THE REST OF THE TOOLING QUEUE (decided 2026-07-25).** The class is confirmed,
recurring, and has ESCAPED to main once (#915, `.working/validate-sweeps/history.md:15`). It is purely
mechanical, so false positives are near impossible, and the exposure is ACTIVE: the 2026-07-25 session
appended rows to four affected ledgers. A fused row drops a PR's QA record while leaving the ledger
looking populated. Use a real fused row as the regression fixture.

The table-row-join / ledger-row-fusion class (a reverse-chronological ledger row appended via `Edit` whose new row lacks the trailing newline before the preserved next row, merging two rows onto one physical line and dropping the displaced row's leading identifier cells) recurred as #915's Sweep-103 history-row edit (`.working/validate-sweeps/history.md:15`) and, for the FIRST time in the class's history, ESCAPED to `main`. Every prior occurrence (#347/#462/#498/#656/#887/#888/#891) was self-caught pre-commit by gate 50, gate 36, or the pipe-count self-check, which is why the #891 `/retro` declined a gate ("the self-check catches it"); the #915 escape refutes that disposition. It escaped because (a) `validate-sweeps/history.md` is NOT read by gate 50 (which reads only `validate-pr/history.md` and `improvement-log.md`), and (b) the post-edit self-check was skipped. Build a STRUCTURAL table-row-integrity check over the reverse-chronological `.working/` bookkeeping ledgers ([`validate-pr/history.md`](.working/validate-pr/history.md), [`improvement-log.md`](.working/improvement-log.md), [`validate-sweeps/history.md`](.working/validate-sweeps/history.md), [`deep-assessment/register.md`](.working/deep-assessment/register.md)): assert every non-separator table line begins with `|` and carries that ledger's expected column count (counting an escaped `\|` as a literal, not a separator). FP-free (a well-formed ledger yields no findings; a ledger-less fork yields none). Decide gate-vs-advisory and whether to fold it into gate 50 (which already reads two of these ledgers despite the `.working/` exemption) or ship it standalone. Surfaced and routed by the #915 `/retro` (the improvement-log auto-graduation, the class having reached pattern-plus-escape).

**Design analysis (2026-07-14, from the #916/#917 build; BUILD DEFERRED to a fresh session).** A prototype measurement showed the naive design (assert every data row's unescaped-pipe count equals its ledger header's) is NOT FP-free: it flags ~50 pre-existing LEGITIMATE rows across the ledgers (validate-pr/history.md 20, improvement-log.md 17, validate-sweeps/history.md 13; deep-assessment/register.md 0) that carry unescaped `|` inside prose cells (the ledgers were never structurally constrained, being gate-exempt). Shipping that naive check as a hard gate would fire on 50 legitimate rows (a decorative/broken gate, gate-discipline). Also the ledgers are structurally inconsistent: validate-sweeps/history.md and deep-assessment/register.md carry a `|---|` separator row, while validate-pr/history.md and improvement-log.md put data directly under the header (and the latter two have `|---|`-shaped text inside prose cells), so separator-based column detection is unreliable too. An FP-free detector needs a SMARTER signal than a column count: (i) flag a data row that contains, MID-ROW, a second occurrence of the ledger's row-start pattern (`| YYYY-MM-DD | <id> |`) - the row-join-that-retains-the-identifier shape; AND (ii) a per-ledger SEQUENCE-GAP check (a missing expected id, e.g. Sweep 102 absent while 103 present) - the dropped-identifier join shape that F1@#915 actually took (a pure column-count check catches F1 but not FP-free). Options for the fresh build: normalize the ~50 legit rows to escape their prose pipes first (a large risky sweep, then the simple check is FP-free), OR build the smarter detector directly. The build was deferred (not attempted) because it is a subtle FP-free-detector design better done fresh, and because it surfaced during a session already carrying a precision-strain signal on exactly this mechanical-edit class. **Interim mitigation now in force (codified in the #916 retro):** insert a ledger row by anchoring the `Edit` on the HEADER line alone and appending the new row AFTER it, never matching-and-re-appending the next row's leading cells.

**REPAIR DONE (2026-07-26); the GATE is what remains.** Seven lost rows were restored, not six, and the
seventh is a different mechanism. Six were fusions, reconstructed from the intact prior revision of their
own ledger with NOTHING synthesized (the unrecoverable-row branch never fired). The seventh, **Sweep 91**,
was not fused but OVERWRITTEN: in `8d198b2c` an Edit anchored on the Sweep 91 line and replaced it with
Sweep 92's, deleting it outright, and the only surviving trace was its Summary cell stranded as an orphan
mid-line. A verbatim application of the fusion reconstruction would have DELETED that orphan while
appearing to repair the line. It was recovered from `e94b6923` and verified byte-identical at 1502
characters.

The apply was deterministic and re-parsed rather than hand-edited: each absorbed row was proved to BE that
row by a shared Summary prefix against its intact revision (254 to 2927 characters), the surviving tail was
kept rather than the historical text because the tail is NEWER (the dash sweep and the de-link both
post-date it), and the de-link rule was applied so five references to swept detail files did not come back
as dead links. Post-repair verification: zero fusions remain, zero unexplained sequence gaps remain, the
apparent duplicates at 9 and 10 are legitimate multi-iteration sweeps, and gaps 1 to 8 predate the ledger,
whose earliest row is Sweep 9 on 2026-06-20.

**What this means for the gate, and it is a scope change.** The class is LOST ROWS, of which fusion is one
mechanism and same-line overwrite is another. An overwrite leaves a perfectly well-formed, width-normal
table, so the structural fusion detector this item specifies would never fire on it; the only signal is the
SEQUENCE GAP, which must therefore be a first-class check rather than a corroborator. An independent
re-scan using three non-width signals confirmed six fusions and correctly declined to reconstruct Sweep 91
from its gap alone, which is what pointed at the history search that resolved it.

**SCOPE CORRECTED AND SEQUENCED (maintainer-directed 2026-07-25c).** The premise above, that #915 is the
class's first escape, is WRONG. Worker `opus-20260725T121943Z-78ff`, measuring detector candidates for this
item, found **five** fused rows live on `main` in [`validate-sweeps/history.md`](.working/validate-sweeps/history.md)
(lines 44, 45, 46, 84, 103) and one in [`matrix-fit/history.md`](.working/matrix-fit/history.md), confirmed two
independent ways (a cell count exceeding the 7-cell header, and a missing sweep whose per-run detail file is
referenced from inside the flagged line). #915 was the first NOTICED escape, not the first. **Four of the six
fusions DROPPED the displaced row's identifier entirely** (Sweeps 88, 86, 27, and one unidentified, plus one
matrix-fit batch), so QA audit trail has been silently lost rather than merely mis-rendered. Sweep 90's row
survives inside line 44. The consequence for this item is mechanical: **the gate as specified cannot land
green against the current tree.** The maintainer's decision at the 2026-07-25c resume is **REPAIR FIRST, THEN
GATE**: reconstruct the four dropped rows from git history and the per-run detail files, repair all six
fusions, and only then land the detector, so the gate is green on arrival and no grandfathered exemption list
is created. The alternative considered and rejected was landing the gate now with the six exempted, which
would have baked an exemption set that itself drifts and left the dropped rows lost meanwhile.

### 3.121 A sweep order that strips `origin` makes the pre-push-guard claim un-re-derivable (Sweep 122 Part 5, L, XS)

Sweep orders direct the worker to remove `origin` from its clone so the library-version-monotonicity gate does
not fire spuriously. That makes the pre-push guard's PR-time D-series unrunnable: all eight checks fail rc=2 on
merge-base resolution against a missing `origin/main`, an environment error rather than a finding. So a closing
handoff's "pre-push guard green on both runners" assertion comes back **VOID**, neither confirmed nor
contradicted, and no worker can verify it under the current instructions. Two candidate fixes, both naming a
decision the order author must make rather than one a worker may improvise: keep `origin` and give the
monotonicity gate its own exclusion, or clone with `origin` intact and create a local `origin/main` ref at the
base SHA so the D-series can resolve a merge-base. The Sweep 122 worker correctly declined to invent the ref
unasked, on the grounds that it changes what the guard measures.

### 3.122 #1176 merged unvalidated; its `/validate-pr` must return and be dispositioned (maintainer-directed 2026-07-25c, H, S)

#1176 carried 22 files, 813 insertions and **six backlog-item closures**, and merged with its `/validate-pr`
order dispatched but never claimed; the session then closed. A wrongly-closed backlog item is invisible
afterwards, which is exactly why the order asks for those closures to be judged adversarially. The order
`validate-pr-1176` is still queued, pinned to `462352b1`, blocking and priority 0. It has **no eligible
claimant**: both codex workers declined it on a documented independence conflict (one produced the
`validate-pr-1175` sweep whose findings #1176 fixed) and both opus workers are chain-adjacent. Per the rule
#1178 adds, if no worker serves it the orchestrator runs it directly rather than closing over it. This item
closes when the result has RETURNED and every finding has a disposition, not when the order is re-dispatched.

### 3.123 `decisions-search.py` does not scan CLAUDE.md, so it false-negatives on maintainer directives (orchestrator-found 2026-07-25c, M, XS)

`SEARCH_STORES` covers [`pending-decisions.md`](.working/pending-decisions.md), the `_private`
design-decisions record and [`DONE.md`](.working/DONE.md). It does NOT cover
[`.claude/CLAUDE.md`](.claude/CLAUDE.md), which is where a standing maintainer directive is recorded. The tool
therefore reported `NO recorded decision found` for the gate-69-`docs/` scope question, which the maintainer had
answered in writing that same day in the `## Defence in depth is the default` section, quoting their own words on
exactly that question. A guardrail whose whole purpose is preventing a re-ask gave a false negative on a settled
question, which is the same guard-input-authority class as the four other defects of 2026-07-25: the check is
correct and its input cannot answer what is asked of it. Add CLAUDE.md and the pack governance rules to the store
list, and add a self-test case keyed on this exact query so the regression is pinned by the real failure rather
than an invented one. Note the tool is also the backstop the `block-answered-question.py` hook complements, so the
gap widens beyond the manual search.

### 3.124 Two verified `grc_library_ref` catalogue defects, neither needing egress (worker-reported 2026-07-25, H and L, XS; cross-repo)

Both come from the worker inbox drop `opus-worker-maintainer-decisions-2026-07-25.md` and both are held-evidence
findings rather than currency claims, so they are fixable now. **D4 (error):** `catalogue.yml:4922`, the `notes`
field on the **EU Implementing Regulation (EU) 2025/454** entry, describes an **Australian** statute (as-made
authorised version, royal assent, amends the Privacy Act 1988). Three signals establish misplacement rather than
coincidence: an EU implementing regulation has neither royal assent nor any relation to the Privacy Act 1988; the
held EU extract's own header carries no Australian content; and the Australian entry at `:4838` has **no `notes`
field at all**, so the text was MOVED onto the wrong entry rather than duplicated. Both carry
`last_checked: 2026-07-11`, so one editing pass did it. Fix: move the line to the Australian entry after `:4849`,
and give the EU entry notes describing the EU instrument or none. **D5 (note):** `catalogue.yml:5531`'s title
presents the Canada TB Directive on Automated Decision-Making as having a 24 June 2025 to 24 June 2026 compliance
transition, but the held text's sections 1.2.1 and 1.2.2 put that window's end at 2026-06-24, which has passed, so
a closed transition reads as running. **Orchestrator has NOT re-verified either at source**, because `_ref` is a
separate repository and this is a separate PR; re-verify before applying, per apply-time worker correction.

### 3.125 Codex worker guard rails, phase 1: a heartbeat emitted by the work loop, and liveness derived not self-reported (maintainer-directed 2026-07-25c, H, M; cross-repo)

**The maintainer's report is that codex workers misdescribe what they are doing and need to be called out before
they actually work.** The mechanism behind that is structural rather than behavioural: a codex worker's heartbeat
is stamped by a background daemon that is a SEPARATE code path from the work, so a worker whose turn ended an
hour ago still reads `LIVE`, and asking it for its state gets an answer composed from context rather than read
from anything.

**The measured evidence was CORRECTED by its own author before this item was committed, and the corrected picture
is WORSE.** The first drop reported two consecutive codex sessions heartbeating exactly once and never again, and
inferred a startup loop completing one cycle and stopping. The measurement was right at 22:12Z; the inference was
not. `codex-20260725T210500Z-81f5` did not die: it went **163 minutes between its first heartbeat and its second**
and is alive now, still holding its order. Only `codex-20260725T203923Z-83b0` is a genuine never-beat-again case
(202 minutes silent). So it is one dead session and one very slow one, not a pattern of startup death.

Why that is worse rather than better: **163 minutes is roughly eight times the 20-minute stale window, so a LIVE
codex worker reads as DEAD for most of its life.** Three consequences, the first being a live safety defect.
**(1)** The stale-scan cannot safely reclaim from the codex family: during `81f5`'s gap it was a textbook reclaim
candidate (stale 67 minutes, holding an order), and had the scan reclaimed then, two workers could have delivered
the same order id. **(2)** Earlier orphan reports against codex holders are probably false positives, and the
author has withdrawn the `81f5` one. **(3)** The remedy is NOT "wait for a second heartbeat before giving a codex
session work", which on this evidence means waiting up to three hours; the question is why the cadence is so long,
and a serve loop that heartbeats only BETWEEN orders rather than DURING one produces exactly this shape, which is
direct support for change (a) below.

The maintainer chose **guard rails first, runner later** (the VM-local supervised runner is deferred), and chose
to **split** this from the remaining guard rails because it is the load-bearing half and is testable on its own.
Phase 1 is therefore two changes: **(a)** the heartbeat is emitted BY the claim-and-serve loop, so that when the
work stops the heartbeat stops, rather than by a sidecar; and **(b)** every liveness verdict is DERIVED from
artefacts the worker does not author (process liveness, the order's `claimed_at`, available-work ctime, outbox
mtime) rather than from any self-report. The correction adds a third: **(c)** until the cadence is fixed, the
stale-scan must NOT reclaim from the codex family, whether by a per-family stale window or by an explicit refusal,
because reclaiming from a mid-gap live worker is how two workers come to deliver the same order id. Use the
CORRECTED timestamps as the reality fixture (`f8b8` surviving 1187 minutes, `81f5` with a 163-minute gap and alive,
`83b0` silent at 202 minutes and genuinely dead), since a fixture built from the real state is the only thing that
tests an observer against the world rather than against its author's model, and here the first version of that
state was itself wrong. This is the genuine fix behind TODO 3.116, which was
closed with a stall signal that could not fire on a worker heartbeating normally. Phase 2 (evidence-mandatory
delivery format, and an adversarial audit cadence over deliveries) follows as its own item.

### 3.127 `submit_state` residual paths beyond the fixed one (validate-pr-1176 E1 follow-on, M, S)

The FALSE-SUBMITTED path E1 identified is FIXED in #1180: `composer_region` is now told which runtime it is reading
instead of inferring it from the rule count, and returns INDETERMINATE where it genuinely cannot tell, pinned by a
reality fixture built from the actual failing pane shape. What remains is the wider question the fix exposes rather
than answers. The tool reads a 12-line tail (`COMPOSER_TAIL_LINES`) and probes with the payload's FIRST 40
characters, which is the part that scrolls away first, so the check is structurally weakest for the longest payloads.
Consider probing on a TAIL fragment of the payload rather than a head fragment, since the tail is what remains
visible when the box scrolls, and consider whether the tail depth should be derived from the payload's rendered
height rather than fixed. Also still open: the earlier observation that the tool reported NOT SUBMITTED for a pane
whose composer was in fact empty with a completed reply, which the runtime fix may or may not explain and which
should be re-tested against live panes before it is assumed closed. **A concrete residual route is now confirmed (validate-pr-1180 F-1, consumed #1206):** `manage-workers.py:242` (the `claude` branch, `start = rules[-2] + 1`) assumes the last two rule lines are the composer's two borders, so a rule-like line rendering BELOW the composer's bottom border makes `rules[-2]` the bottom border, the returned region is the status area, the probe is not in it, and `submit_state` answers `submitted` for a payload still in the box; a constructed 3-rule pane driven through the real capture path returns `submitted` against ground-truth `not-submitted`. The structural fix is to anchor the composer region on the border PAIR (top and bottom) rather than the last-two-rules heuristic, so an extra rule below cannot shift the window.

### 3.128 The token-spend parser: per-worker display conflates measured and estimated (residual of validate-pr-1176 W1/W2, M, S)

**STATUS (updated 2026-07-26, Sweep 124 W1): W1 and W2 are FIXED in #1189** (`re.S`/DOTALL for W1; the
`gap_is_connector` connector-allowlist that fails closed for W2; self-test 43/43). The item stays OPEN
only for the **per-worker-display residual** described in the ORCHESTRATOR RE-DERIVATION subsection
below (a worker whose figures are mostly unreadable is shown a confident number derived from a minority
of its deliveries, the measured-versus-estimated conflation the pack rule forbids). The original W1/W2
prose is retained below as the record of what #1189 closed; read it as historical, not open.

Two defects (W1/W2, both FIXED in #1189) in [`tools/audit-token-spend.py`](tools/audit-token-spend.py), measured against the real delivery tray
rather than constructed inputs. **W1:** `SPEND_PATTERNS` puts `(.{0,20}?)` between the phrase and the number and `.`
does not match a newline without `re.DOTALL`, so any delivery that places its figure in a `## Token spend` SECTION
(heading, blank line, paragraph) never matches; that is **12 of 31** real deliveries reading UNKNOWN. The failure
direction is safe, which is why it is a warning rather than an error, but it silently understates fleet spend across
roughly two fifths of deliveries. **W2:** the `NEGATION` guard is a closed enumeration that closes exactly the string
the #1175 sweep fed it, while `withheld`, `declined` and `unavailable` all still yield a fabricated 8000 taken from
an adjacent budget figure. Enumerating negations cannot be completed, so the structural fix is to require the number
to be ATTRIBUTABLE to a spend phrase rather than merely near one, which is the same input-authority shape as the rest
of this week's findings.

**ORCHESTRATOR RE-DERIVATION (2026-07-26), and it is worse than W1 states.** Re-run over the live tray: **14 of 36**
deliveries report no readable figure (the worker measured 12 of 31 earlier; the tray has grown since, so the two
agree). The sharper finding is in the PER-WORKER column, which W1 does not mention.
`opus-20260725T121943Z-78ff` displays **about 1,175 estimated across 12 deliveries**, while ONE of those deliveries,
`sweep122-resume-validate`, states "approximately 330,000 input tokens and approximately 30,000 output tokens" in a
`## Token spend` SECTION, exactly the shape the parser cannot cross. So the tool does not merely fall back to UNKNOWN
for these: it prints a confident per-worker figure understating that worker by roughly 300 times, and the fleet TOTAL
is consequently dominated by the one worker whose phrasing happens to parse. That is a wrong-number failure sitting
beside an honest unknown-count, and it is the more dangerous half, because the unknown count carries its own caveat in
the output while the per-worker figure carries none. The fix must therefore also decide what to DISPLAY for a worker
whose figures are mostly unreadable: a number derived from a minority of a worker's deliveries is not that worker's
spend, and presenting it as such is the measured-versus-estimated conflation the pack rule already forbids.

**ROOT-CAUSE + fix pointer (from the `issue-validate-pr-1176-token-spend` inbox drop, 2026-07-26; drop moved to `done/drops/2026-07/`).** The specific mechanism of the wrong-number failure: `find_reported_spend` takes the FIRST `SPEND_PATTERNS[0]` match in the whole document, so a QA delivery that DISCUSSES token spend before reporting its own hits a false figure, for example the prose `(token spend) ... V1175-3` yields `1175`. First-match assumes the first phrase occurrence IS the report, which fails for any delivery that mentions the phrase before its own reporting section. Suggested fix (aligns with 3.128's attributable-not-near direction): anchor the search on the delivery's own reporting SECTION, a `## Token spend` heading (or the LAST phrase occurrence, since the convention puts the report at the end), and search only within it, which fixes W1 and this together as both are failures of WHERE the tool looks.

### 3.130 Portable pack form of the mid-session-death recovery protocol (`/restore-broken` companion, 2026-07-26, M, M) `[pack]`

`/restore-broken` ([`.claude/commands/restore-broken.md`](.claude/commands/restore-broken.md), shipped 2026-07-26) is
the PROJECT-specific slash command for recovering a project whose orchestrator died or ran out of usage mid-session.
The recovery DISCIPLINE it encodes (observe read-only before changing anything; verify the interrupted unit as a
hypothesis, not an inheritance; reconcile the stale lease; the tray-count-is-not-the-unprocessed-count trap; the
turn-end-safety check for an auto-commit stop hook; wind down to a clean green branch, then a same-session resume as
the compensating control) is PORTABLE to any project running multi-session AI-assisted work. Per the pack-parity
coupling, add the portable form: a recovery subsection in the pack
[`session-lifecycle`](dev-security/claude-rules/governance/session-lifecycle.md) rule (or a dedicated pack rule if it
grows), so an adopter inherits the mid-session-death recovery path alongside the normal session lifecycle. Recorded as
a tracked follow-up (the sanctioned pack-parity option) rather than built in the command's own PR, to keep that PR
focused.

### 3.131 Per-worker headless console/event logging to a searchable log file (maintainer-requested 2026-07-26, M, S) `[machinery]`

Workers run headless, so their runtime console messages (claims, heartbeats, progress, errors) are not searchable after
the fact; only the final delivery lands in the outbox. Add per-worker logging to `/home/grc/grc_working/logs/` named
`YYYY-MM-DD_<worker-id>_out.log`, greppable and tailable. Two parts: (a) the exchange helper `credit-offload-filedrop.py`
(`grc_library_scratch:tools/`) writes a structured event line on each `claim` / `heartbeat` / `deliver` / error (clean
text, the primary searchable record); (b) for codex, the `codex exec` sudo-wrapper (post-resume codex build, design in
`grc_library_private`) redirects its stdout, stderr, exit status, and timestamps to the same dated per-worker log at
about zero extra cost. NOTE: a raw capture of the interactive Claude TUI (`tee` / `tmux pipe-pane`) carries ANSI control
codes because of the alternate-screen buffer, so the STRUCTURED event log is the clean approach and `tmux pipe-pane` is
only an optional raw supplement. The helper lives in `grc_library_scratch`, so the primary build is a scratch-side
change; best done post-resume alongside the codex-exec build so both worker families share one `logs/` layout.

### 3.132 Gate 78 enforces only the recorded-retirement half of the never-recycle rule (r16 guardrails, G-1; DECIDED, rotate to DONE) `[machinery]`

**DECIDED 2026-07-26 (maintainer): option (b), ACCEPT the recorded-retirement half of gate 78 as sufficient. DONE.md is
a quick-reference for the maintainer, not a permanence record, so no DONE-heading-id convention is adopted and gate 78
is not extended. This item is RESOLVED; rotate it to DONE at the next close-out.**

Guardrail-review r16 (2026-07-26) GAP finding, re-verified at source. The `TODO.md` never-recycle rule is ABSOLUTE (a
number maps to exactly one item across the whole history), but gate 78 (`tools/lint-todo-number-permanence.py`) enforces
only the RECORDED-retirement half: its own docstring discloses that a `.working/DONE.md` entry heading carrying no
`§N.M` id is invisible to the recycle check (most DONE headings state no id), so a number whose retirement was never
recorded with its id could be recycled undetected. The docstring names the closure (adopt a DONE.md heading convention
that always carries the retired id, then extend gate 78 to it), which was UNQUEUED until this item. MAINTAINER DECISION,
not a defect to fix: either (a) adopt the DONE.md heading-id convention and extend gate 78 to catch unrecorded-retirement
recycling, OR (b) accept the recorded-retirement half as sufficient and record that decision (the gate is honestly
guard-first and discloses its own boundary). Routed as a maintainer-decision proposal per the guardrail-review skill.

### 3.74 Standards-reference-format standardization (maintainer-directed 2026-07-14, M)

**SEQUENCED AFTER the §3.9 edition verifications (decided 2026-07-25).** Adding a release year
converts a bare reference into an EDITION claim, so standardizing first would bake unverified years into
roughly 200 register rows and every framework table. The live `ISO/IEC 29134:2017`-versus-`:2023`
inconsistency is the proof. Resolve the editions (they are on the egress VERIFY list), then apply the
rendering as a single-session corpus-wide sweep, since corpus-wide harmonizations are not partitionable.

The maintainer prefers listing ISO / IEC / IEEE standards with their release year, as more complete and comprehensible, and set "ISO/IEC 5259:2024" as an example of the norm to standardize toward. Review how the corpus references standards across the repo (document bodies, framework-alignment tables, the landing-page standards list, and the canonical-citations register) and standardize the rendering. Points for the review to settle: (a) the release-year form as the default for ISO / IEC / IEEE citations; (b) multi-part series, where ISO/IEC 5259 is parts 5259-1 through 5259-4 (all 2024) with no single unitary edition, so the review decides how to render a series-level reference versus a specific part such as 5259-4:2024, and whether the corpus's current mix (bare series names plus part-and-year citations) is harmonized or left as-is; (c) standards versioned by semantic version rather than year (OWASP ASVS is rendered "OWASP ASVS 5.0" on the landing page while the register records 5.0.0), which need a companion rule since the release-year form does not apply to them. The canonical-citations register ([`governance/register-canonical-citations.md`](governance/register-canonical-citations.md)) is the ground-truth source for each standard's version and year. Surfaced from the landing-page work: a #920 attempt to render 5259 without its year was reverted to the year form per this directive, and the holistic standardization was deferred here rather than applied piecemeal. **Also surfaced (#1123, from the §4.2 pack language-rule review, finding F1):** the pack `dev-security/claude-rules/languages/` files render their Framework-alignment section in two shapes, a chapter-level OWASP-ASVS-plus-Top-10-plus-NIST-SSDF bullet list (`python.md`, `typescript.md`) versus a richer requirement-level ASVS-plus-SSDF-plus-ISO-27001 table (`go.md`, `java.md`); harmonizing that pack-wide alignment-table shape (the review recommends the go/java table form, extended to retain an OWASP Top 10 column so nothing the bullet form carries is lost) is a framework-alignment-table rendering decision that belongs in this pass, not a piecemeal per-file edit.

### 3.75 Website-to-corpus link integrity: generated manifest + resolution gate + resolve-by-id (maintainer-confirmed 2026-07-15, M, M)

**PARTS 1+2 CLOSED AS SHIPPED; part 3 RE-SCOPED as convenience, not correctness (decided
2026-07-25).** Gate 75 already prevents the failure mode: a rename fails CI instead of silently breaking
the public site. So resolve-by-id auto-update is a workflow improvement competing on marginal value, and
its marginal cost is NOT small: a wrong id mapping points the public site at the wrong document
silently, which is worse than a loud failure.

Keep every link from the public site to a corpus document (or its GitHub source) accurate as the corpus changes, with the maintainer notified of breaks and safe auto-update on rename. Maintainer-confirmed shape 2026-07-15 ("manifest + gate + resolve-by-id"). **PARTS 1+2 SHIPPED (#1121):** (1) `.web/build.py` now emits a committed link manifest (`.web/corpus-link-manifest.md`, a generated artefact re-derived from the taxonomy-driven domain/type pages and the curated llms.txt map so it cannot drift, drift-checked by `build.py --check`); (2) a new egress-free gate 75 (`lint-web-corpus-links.py`) resolves every manifest target against the repo and fails on a renamed or deleted corpus document, wired across the four gate surfaces with a regression fixture. **PART 3 REMAINING (deferred, corpus-wide metadata-model change):** resolve links by a stable doc-id carried in corpus-doc metadata rather than a hardcoded path, so a corpus rename auto-resolves at build; this needs a base doc-id field added to every document's metadata block (and the metadata linter), the change §2.26.2 also depends on. The manifest currently keys on the corpus path, so a future doc-id column is an additive migration, not a rework. **Small follow-up (from the #1121 verifier):** the manifest's curated-llms.txt rows re-derive from a `CURATED_CORPUS_LINKS` constant that PARALLELS the links `render_llms_txt` emits inline (they match today but are hand-kept in sync); bind them (a test asserting the two agree, or refactor `render_llms_txt` to consume the constant) so a future edit to one cannot silently leave a curated link ungated. The domain/type-page manifest rows are already drift-proof (re-derived from the same page-render data). Careful QA: an auto-resolved change is validated by the resolution gate plus a skeptical verifier before merge. Serves 2.25.2 (standards-linking, the item formerly at §2.15) and the whole public site's link accuracy.

### 3.79 For-AI page: give corpus coverage to the "named, not yet covered" instruments, then sync the page (maintainer-flagged 2026-07-15, M-L; corpus-first, NOT independent)

**Maintainer priority within P3 (2026-07-15): prioritized ahead of the other P3 items.** The For-AI page ([`.web/templates/for-ai.html`](.web/templates/for-ai.html)) hand-lists instruments under "Named, not yet given dedicated coverage" (US Texas TRAIGA, Illinois HB 3773, California CCPA ADMT, South Korea AI Basic Act, Singapore Model AI Governance Framework, Malaysia guidelines, the UK approach, the African Union AI Strategy; ISO/IEC 8183, 12792, 5338; NIST SP 1270, NIST IR 8312). Give each the appropriate corpus treatment (a dedicated annex/doc, or a citation where a dedicated doc is not warranted), then MOVE it on the page from "Named, not yet covered" to a "Documented in [doc]" entry. **Dependency (maintainer question, 2026-07-15): corpus-first, then a web-page sync; the two are NOT independent** (the page's coverage claim must reflect corpus reality, so the corpus doc/citation lands before the page moves the item). Much of the jurisdiction set is already covered or tracked (California CCPA/ADMT and Singapore shipped as `ai/jurisdictions/` annexes on 2026-07-24; §2.18 South Korea AI Basic Act and §2.21 UK/Malaysia/Australia/US-federal/Texas/Illinois still tracked); several ISO/NIST items are already CITED in corpus docs (e.g. NIST IR 8312) but lack dedicated coverage. So this is the coverage-SYNC umbrella over those: as each coverage item lands, sync the For-AI page's lists, and review the lists for completeness/currency against the corpus. Also decide whether the For-AI instrument lists should stay hand-authored or be generated from the corpus (generation would keep the "documented" entries drift-free; ties to §3.75).

### 3.80 Credit-offload: multi-worker QA + research queue (maintainer-co-designed 2026-07-15, L, XL; cross-repo)

Build the credit-offload scheme designed in `grc_library_private/credit-offload-design.md`: a polling work queue on `grc_library_scratch` that moves the read-only analysis passes (`/validate`, `/validate-pr`, `/matrix-fit`, `/claim-fit`, `/reference-audit`, `/screen-publications`, `verify`, `/fitness`, `/full-qa`, read-only `/deep-assessment` phases) AND research/drafting seeds onto standing worker sessions on other accounts, so the orchestrator (low on usage credits) spends only on author-apply-route-merge. Coordination on scratch-git (split-brain-free across a VM+cloud worker mix); a `/tmp/grc_library_working` local clone-cache with a per-order `git worktree` at a pinned SHA; a lease/fencing lifecycle (5-min heartbeat / 20-min stale; a monotonic fencing token rejects a stale worker's late delivery); a `workers/` liveness registry driving the orchestrator's best-effort-or-self-run fallback; token-budget-aware graceful checkout (best-effort, with the fencing/stale path as the guaranteed backstop); richer metrics plus a check-in/out log on scratch. Phases: (1, DONE 2026-07-16, scratch) the queue protocol + `/credit-offload` worker command + helper tool + a first test order; (2, scratch, IN PROGRESS 2026-07-16) harden the worker loop + onboarding: the two worker-lifecycle hooks (worktree cleanup on wind-down/crash, reconcile on re-register) + the serve-loop self-refresh + the live write-path test (`worker-20260716-a` exercising the offloaded Sweep 108 order); (3, grc_library protected, **APPLIED 2026-07-16**, maintainer-authorized attended) the orchestrator-side enqueue/consume convention + the `## Credit-offload mode` directive wired into `/resume` (step 6 blocking-resume-`/validate` + step 3 queue/results check) and the orchestrator operational extension (`orchestrator-claude.md` A1, relocated from `.claude/CLAUDE.md` by #1044). Phase 0 (maintainer): provision the least-privilege worker account(s) and the shared-VM clone cache (DONE: `worker-20260716-a` live on the VM). §3.80 closes when phase-2 hardening lands and the live write-path test passes. See also §3.81.

### 3.81 Pre-push-verifier offload periodic reassessment (credit-offload thread-3, 2026-07-15, L, standing)

Standing periodic reassessment of the credit-offload decision (§3.80) to keep the pre-push skeptical verifier on the orchestrator account: it sits on the critical path before push, so offloading it would add a blocking wait per substantive push. Revisit whether it should move to a worker (as a blocking order, or offloaded only for high-assurance/sensitive PRs) once the credit-offload queue is proven and the worker-availability and latency profile is known. Reassess at the periodic guardrail-review / deep-assessment cadence; no build until re-decided.

### 3.82 Credit-offload worker degradation check + in-session self-restart (maintainer-flagged 2026-07-16, credit-offload thread-4, M)

Give credit-offload workers a degradation signal and a lightweight self-restart, so a long-running worker session that has degraded is refreshed without manual intervention (the worker analogue of the orchestrator's session-length concern). Maintainer design steer (2026-07-16): a worker's restart is much lighter than the orchestrator's `/resume` because a worker holds NO durable authorial state (it is stateless between orders; all cross-interruption state is on the scratch coordination plane). The restart is just **`/clear` then re-invoke `/credit-offload`** in-session: re-invoking runs `register`, whose **reconcile-on-re-register hook** (built in scratch, the worker-lifecycle-hooks PR) safely rejoins by honouring the fencing token of any held order and pruning stale worktrees. So no handoff document and no manual activity are needed; the worker can potentially self-restart on a cadence or on a degradation signal. To build: (a) decide the worker-degradation SIGNAL (a named, externally-observable one, per `evidence-grounded-completion` un-observable-state: e.g. N delivered orders, elapsed wall-clock, a self-caught error rate, or a token-budget threshold, NOT "I feel degraded"); (b) wire a self-restart step into the `/credit-offload` serve loop (`/clear` + re-invoke) triggered by that signal; (c) confirm the reconcile-on-re-register hook covers the post-`/clear` rejoin cleanly (it should, by construction). Cross-repo (the `/credit-offload` command lives in `grc_library_scratch`). See §3.80/§3.81 and `grc_library_private/credit-offload-design.md`.

### 3.83 Credit-offload worktree-prune TOCTOU race + 3 nits (worker-lifecycle-hooks verifier follow-up, 2026-07-16, S) `[machinery]`

The worker-lifecycle-hooks PR (scratch) left one narrow, non-blocking, adversarial-verifier-flagged shared-VM race, documented in `grc_library_scratch` `queue/README.md`: `cmd_register`/`cmd_checkout` compute the worktree-prune keep-set (`_claimed_order_ids`) from the clone snapshot taken at their top-of-function `reset --hard`, and do not re-fetch between that read and the `wt-*` deletion, so in the sub-millisecond window another same-VM worker could claim an order and create `wt-<order>` that the pruning worker's stale keep-set omits and deletes. Robust closes: re-fetch the keep-set immediately before each prune, OR scope worktree caches per-worker (`wt-<worker-id>-<order-id>`) so no two workers ever share a `wt-` path (the cleaner fix; also removes the revive-collision entirely). Plus three nits: the register resume-vs-clear control flow keys on a substring of the reconcile note (fragile to rewording, make it a boolean); `register` skips the opportunistic prune for a brand-new worker (no existing worker file); and (DONE 2026-07-16, scratch `752c5ae`) the `/credit-offload` command's delivery step now forces a pre-`deliver` `python3 tools/validate.py` house-style pass (it previously did not, so `worker-20260716-b`'s `validate-pr-973` and `-974` results both tripped scratch CI on dashes/bare-`ensure`, fixed post-hoc; the command now requires the worker to run `validate.py` and fix findings before `deliver`). Plus a serve-loop precedence strengthening (surfaced by `validate-pr-974` F1): the command elevates only `blocking` orders above the role-kind preference, so a non-blocking priority-1 order (e.g. a per-PR `/validate-pr`) can be starved behind a role-specialized worker's role preference; give all priority-1 orders precedence over the role preference in the `## Serve loop` ROLE bullet, so urgent QA is never starved behind a role rule even when non-blocking (no live impact while the fleet is all `any`-role, but it closes the design-of-record's stated guarantee). Cross-repo (scratch `tools/credit-offload-queue.py` + `.claude/commands/credit-offload.md`). Plus a token-reporting-format nit: worker results use two formats for the token estimate (worker-b a `## Token spend` section, worker-a a `Proof-of-run` subagent-budget line), so the credit-offload-metrics.md backfill had to parse both; add a one-line "report your token spend in a `## Token spend` section" to the `/credit-offload` worker command so the metrics ledger parse is uniform (non-blocking; the orchestrator reads both today).

### 3.85 Credit-offload worker reference-read model + multi-worker resync coordination (maintainer-flagged 2026-07-16, credit-offload thread-5, M; cross-repo) `[machinery]`

Workers currently read `grc_library_ref` from a single shared `/tmp/grc_library_ref` copy that the maintainer re-syncs (`rsync -av --delete`) after every ref update. This is a shared-mutable-state gap: (a) a ref update mid-order silently changes what a running worker reads, so a worker's read basis is not pinned to its order's `grc_library_ref_sha` the way its `grc_library` read is (via the `/tmp/grc_library_working` per-order worktree at a pinned SHA); and (b) with multiple concurrent worker sessions there is no per-worker signal that a resync is needed, so a worker can read stale reference text without knowing. Design (the maintainer's "add the design item" for "how do multiple worker sessions know to resync the repos?"): give each worker its own `grc_library_ref` read-clone checked out at the order's pinned `grc_library_ref_sha` (mirroring the `grc_library_working` per-order-worktree model), retiring the shared `/tmp/grc_library_ref` copy and its manual rsync; OR, if a shared cache is kept, add a resync-signal the serve-loop checks (e.g. the order's `grc_library_ref_sha` vs the cache's HEAD, resync-on-mismatch before claiming) so a worker never reads a ref SHA older than its order pins. Codify the chosen model in `grc_library_private/credit-offload-design.md` alongside the worker-allocation model (one-at-a-time + role-based soft split). **Permission-isolation rationale (surfaced live by `validate-pr-974` OBS-B, 2026-07-16):** a per-worker read-clone is needed not only for SHA-pinning but for **multi-user permission isolation on a shared VM**: `worker-20260716-b` (Unix user `worker1`) found the shared `grc_library` cache `/tmp/grc_library_working` owned by another user (`worker`) and not writable (`git fetch`/`worktree add` failed EACCES), so it fell back to a private clone `/tmp/grc_library_working_b`. So the single-shared-cache assumption breaks across Unix users; the per-worker-clone target applies to BOTH the `grc_library` working cache and the `grc_library_ref` read cache, not only the ref side. Cross-repo (the read basis is the worker-side `/credit-offload` serve loop in `grc_library_scratch`; the orchestrator-side ref-update SOP is in `grc_library`). See §3.80/§3.82 and the credit-offload "Worker read basis" note in `grc_library_private/orchestrator-claude.md` (group A1).

### 3.87 Credit-offload local-VM exchange transport (maintainer-directed 2026-07-17, credit-offload thread-6, L, XL; cross-repo) `[machinery]`

**PRIORITY BUMPED TO NEAR-TERM (maintainer-directed 2026-07-19).** Under the offload-everything model (the `## Mandatory worker offload` rule + the orchestration primordial rule), the per-exchange git round-trip latency is on the orchestrator's critical path for every dispatch, delivery, and the now-offloaded pre-push verify, so the transport is the throughput enabler, not a nice-to-have. The DESIGN EVOLVED this session to a `/home/grc/grc_working` per-model-family file-drop (`opus`/`fable`/`codex` subdirs, atomic-`mv` claiming, no broker daemon) as part of a `/home/grc` multi-user migration; the full evolved design (permissions, worker bootstrap via SSH+tmux, read-at-pinned-SHA, model routing) is captured in `grc_library_private/design-decisions.md` ("`/home/grc` multi-user migration + same-VM file-drop worker model"). This is a NEXT-SESSION build (the maintainer runs the sudo/user-admin parts; the orchestrator prepares the move-package and the in-repo path edits); worker-a's `/tmp/grc_working` draft from this session is input, re-worked to the `/home/grc` per-family layout. It also carries the **pre-push-verifier-to-workers** move and the `block-mandatory-offload.py` liveness-source repoint (scratch `workers/` registry to `grc_working/<family>/heartbeat`).

Build the local shared-directory exchange transport for the all-on-one-VM case (the maintainer's expected common case going forward), replacing the git-`grc_library_scratch` round-trips that are pure overhead and the root of tonight's friction (stale mirror, canada.ca WAF, git-proxy 403, ~5-min poll gaps) when every process shares one filesystem. Locked design in `grc_library_private/design-decisions.md` "Local-VM exchange transport for credit-offload": `/tmp/grc_exchange/` with per-worker `inbox/`/`outbox/`/`heartbeat` subdirs (world-writable one-time setup, separate Unix users); **push plus stale-reclaim** assignment (orchestrator writes to a specific idle worker's inbox, reclaims on stale heartbeat, no claim/fencing), worker polls its own inbox every ~15-30s (seconds, not minutes); **no crash backup** (unconsumed results are re-runnable, applied work is durable in git); durable outputs unchanged (corpus to `grc_library` git, audit rows to `.working`); coexists with the git-`scratch` cloud transport via `tools/detect-env.py` mode-detection. **This item RESOLVES §3.85** (the shared-ref-mirror staleness gap) outright (no git mirror, just the shared local FS), so §3.85 closes when this lands. Build worker-side and orchestrator-side TOGETHER (a heartbeat-detector alone is useless until workers write to /tmp/grc_exchange), and only when the workers are IDLE (adopting it swaps their transport, like the item-1 helper hot-reload). Touches the scratch `/credit-offload` command, `tools/credit-offload-queue.py`, and the orchestrator-side assignment/liveness wiring. Cross-repo (worker-side in `grc_library_scratch`, orchestrator-side in `grc_library`).

**Design evolution (maintainer-co-designed 2026-07-17, CONTROL-PLANE / DATA-PLANE split; refine the design-decisions.md entry when built):** replace the ~15-30s inbox POLLING with a **unix domain socket at `/tmp/grc_exchange/orchestrator.sock`** as the CONTROL plane, `/tmp/grc_exchange/` staying the DATA plane. Orchestrator is the long-lived socket SERVER (listener); workers connect as clients to register / heartbeat / request-work / notify-delivery (event-driven, no poll gap); the socket SUBSUMES the per-worker `heartbeat` file and the inbox poll. `/tmp/grc_exchange/` holds the file bundles and temporary storage for not-yet-worked items (order specs, seed bundles, delivery bundles); the socket carries only the SIGNALS ("order ready in your inbox", "delivery written to outbox"), the filesystem carries the bytes. **Locked design points:** (a) the FILESYSTEM stays the durable state-of-record and the socket is an accelerator, not the source of truth, so on an orchestrator restart (socket vanishes) workers FALL BACK to scanning their `/tmp/grc_exchange` inbox (preserves the "no crash backup needed" property, results re-runnable, applied work durable in git); (b) SAME-VM only (a unix socket cannot cross hosts), cloud / non-same-VM workers keep the git-`scratch` transport, `detect-env.py` picks the transport; (c) socket-file permissions are the access control if workers run as separate Unix users, no network exposure (keeps the least-privilege line). A unix socket is preferred over a loopback TCP port for same-VM IPC (no port allocation, filesystem-permission-scoped, no network-namespace exposure). Directory name `/tmp/grc_exchange` confirmed (consistent with the file-drop design above). Still a LATER build, OUT of item 1.19 (closed 2026-07-25) execution scope; this records the maintainer's socket design so it is not lost.

**Assessment + refinement (maintainer-directed 2026-07-19).** WORTH BUILDING (efficiency + error-prevention): it removes the ~15-30s git commit/push/fetch round-trip AND the poll gap per exchange (order dispatch + result delivery + heartbeat all go from seconds-plus-poll to sub-second), eliminates the whole §3.93 stale-local-mirror read-error class (messages are direct, not via an un-synced git checkout), and cuts coordination churn (rebase conflicts on concurrent claims, e.g. the 2026-07-19 seed-enqueue rebase). Net: faster pipeline + fewer coordination errors, both real. **Key architecture constraint (load-bearing): a Claude Code session is TURN-BASED, not an event-loop server**, so it cannot truly "listen" on a socket between turns; the "orchestrator is the long-lived socket SERVER" point only holds if a PERSISTENT LISTENER exists, which a turn-based session is not. So the realistic design is a small **broker daemon** (a non-Claude process on the VM) that owns the socket(s) + an in-memory/on-disk message queue and persists to `/tmp/grc_exchange`; the orchestrator and each worker session talk to the broker via a thin `grc-msg send/recv` tool on their turns. This preserves the maintainer's design (socket transport, filesystem durable) while fitting the turn-based reality: the socket removes git-round-trip latency, but a worker still consumes messages when the harness gives it a turn (the broker holds them meanwhile, so no lost message and no poll of a git mirror). **Socket topology:** the maintainer floated per-instance sockets (`worker1.sock`/`worker2.sock`/`orchestrator.sock`); the simpler single `orchestrator.sock` client-server model (workers connect as clients, the broker identifies each by its connection) is sufficient and preferred; per-worker LISTENER sockets are only needed if the broker must push to an idle worker that is not connected, a build-time trade-off. **Does scratch survive?** REDUCED, not eliminated: `grc_library_scratch` (git) stays for (a) cross-VM / cloud workers, since a unix socket is same-VM ONLY (`detect-env.py` picks the transport per the locked design), and (b) the durable audit trail; the same-VM exchange moves to socket-signals + `/tmp/grc_exchange` file bundles. **Repo sharing:** workers read at a PINNED SHA; a shared LIVE orchestrator repo is UNSAFE (the orchestrator's branch switches change what a worker reads mid-task, the #866 shared-tree-collision class). The safe share is orchestrator-materialized **read-only, SHA-pinned git worktrees** under `/tmp/` that workers read but never mutate (the model the existing shared `/tmp/grc_library_ref` already uses); this saves each worker re-cloning while keeping isolation. Recommend building in phases: (1) the broker daemon + `grc-msg` tool + orchestrator/worker wiring behind a same-VM `detect-env` flag, git-scratch staying the fallback; (2) the shared read-only per-SHA worktree provisioning; keep the git-scratch path as the durable record and the cross-VM path throughout. XL, single-VM-only, `[machinery]`.

**Programmatic worker restart via the control channel (maintainer-directed 2026-07-19).** Once the broker/socket control channel exists, it also lets the orchestrator RESTART a wedged worker programmatically instead of advising the maintainer (the current mode-dependent restart-advice, `orchestrator-claude.md` A1): the orchestrator sends a control message that drives the stalled worker session to issue a `/clear` then a `/credit-offload` (re-onboard), so the worker recovers without maintainer involvement. This rests on a load-bearing **asymmetric-trust rule**: the orchestrator MAY feed prompts/commands INTO a worker session (a worker is a subordinate executor), but a worker's output is always DATA the orchestrator interprets and validates, NEVER accepted as a prompt or command directly (a worker can never drive the orchestrator). This is the existing worker-delivery trust asymmetry (worker research is a hypothesis the orchestrator re-verifies, never authoritative) extended to the live channel, and it bounds the blast radius: a compromised or confused worker can only emit data the orchestrator screens, not commands the orchestrator obeys. Gate on the phase-1 broker landing first (the control channel must carry orchestrator->worker commands); the restart is a phase-1-plus capability. This SUPERSEDES nothing in the mode-dependent advice, it is the unattended, socket-era automation of it.

### 3.88 Credit-offload worker-registry stale-entry auto-prune (maintainer-flagged 2026-07-17, credit-offload thread-7, S) `[machinery]`

The scratch `workers/` liveness registry has no auto-prune. `stale-scan` reclaims stale ORDERS (a `claimed` order past the 20-min heartbeat window resets to `pending` with a bumped fencing token) but never touches worker entries; `list-workers` flags a stale worker `[stale/out]` but does not remove it; `register` is worker-id-keyed and prunes nothing but its own entry. So a worker that restarts under the SAME id overwrites its entry (goes fresh), but one that restarts under a NEW id leaves the old entry lingering indefinitely (flagged stale, never pruned), accumulating cruft (surfaced 2026-07-17 when both workers went stale ~8h and the maintainer asked what prunes them). NOT a correctness bug: the orchestrator's availability gate counts only fresh-heartbeat workers (it keys on the `[stale/out]` flag), so a lingering stale entry does not cause a bad offload decision; it is registry hygiene. Fix (cross-repo, scratch-side): auto-prune worker entries stale beyond a GENEROUS threshold (well past the 20-min order-stale window, respecting the same shared-VM safety the worktree-prune code already applies, so a merely-briefly-quiet live worker is never evicted), OR have a re-registering worker drop its own prior stale entry, OR add a `prune-workers` command. Fits the credit-offload thread (§3.82/§3.83); scratch `tools/credit-offload-queue.py`.

### 3.92.a `/resume` must consume the adopt-config validity flags detect-env already emits (S, S) `[machinery]`

**Split out of §3.92 on 2026-07-25 at the maintainer's direction.** THE OBSERVER SHIPPED AND THE
CONSUMER IGNORES IT, which is the inert-guard pattern four defects on 2026-07-25 shared.
[`tools/detect-env.py`](tools/detect-env.py) gained `_adopt_config_status()` plus
`adopt_config_present` / `adopt_config_valid` in #1016 (four references in the source), and
[`.claude/commands/resume.md`](.claude/commands/resume.md) contains ZERO references to either flag:
measured, not inferred. So the already-onboarded decision still rests on an assistant file-PRESENCE
check, which cannot tell onboarded-correctly from onboarded-with-a-malformed-config.

Remaining work is small: `/resume` keys on the emitted flags, with an explicit unknown state that
REFUSES to assume onboarded rather than proceeding. **Authorized 2026-07-25; build it.**

### 3.92.b Pre-flight maintainer-clone guard for `/adopt` (M, S) `[machinery]` `[needs-decision]`

**Split out of §3.92 on 2026-07-25; the maintainer requires this understood before disposition.**
`/adopt` resets working state and is ASSISTANT-EXECUTED, so nothing hard-refuses that reset when the
clone classifies as `maintainer`. Today the dangerous direction is defended by four soft layers: the
host-pinned origin match, step-1 operator confirmation, the config short-circuit, and git
revertability. A pre-flight helper invoked by step 1 that exits non-zero on any non-`adopter`
classification would move the guard from convention to mechanical.

The decision to bring back: this is a textbook defence-in-depth case (small cost, four soft layers
already present, and the failure mode is wiping a maintainer clone's working state), which the
standing directive says prefer. The counter-argument to weigh is that `/adopt` is run roughly once
per clone, so the guard would almost never fire, and a guard that never fires is also never tested.

### 3.92.c Classification-coupling parity across four surfaces (L, S) `[machinery]` `[needs-decision]`

**Split out of §3.92 on 2026-07-25; the maintainer requires this understood before disposition.**
The maintainer / adopter / fresh-machine classification and its STOP/HALT conditions are restated
across FOUR surfaces with no parity gate: `detect-env.py`'s `probe_identity` plus its decisions,
[`.claude/commands/resume.md`](.claude/commands/resume.md), the `/adopt` SKILL step 1, and the
`/adopt` command step 1. Any change to the classification must touch all four, and that coupling is
convention-guarded only.

The decision to bring back: this is the same four-surface parity shape gates 35, 37 and 41 already
enforce elsewhere, so the precedent is strong and the mechanism is known. What needs weighing is
whether the classification is stable enough to be worth gating: it has changed rarely, and a parity
gate over PROSE restatements is harder to keep false-positive-free than one over structured lists.

### 3.94 Landing-page Contents sidebar overflows its viewport, hiding trailing links (maintainer-flagged 2026-07-17, L, S) `[website]`

The landing-page "Contents" sidebar (`.sidenav-inner`) is capped at `max-height: calc(100vh - 2.5rem)` with `overflow-y: auto` at `min-width: 1080px` ([`.web/templates/partials/head-style.html`](.web/templates/partials/head-style.html)). As the nav grew (the Get-started sub-links, the 11 domain links, the 6 Standards sub-groups added across the recent website PRs) it now exceeds a typical laptop viewport, so its last entries ("For AI", "Contributors") scroll below the sidebar's inner fold and read as missing (maintainer report; the links are present in the live DOM). #1002 MITIGATED this by adding a "For AI" footer link (Contributors was already in the footer), so the pages stay reachable, and the maintainer judged the sidebar case now "matters less". This item tracks the underlying sidebar-overflow root cause for a later, lower-priority pass: options include collapsing the Standards/Get-started sub-groups by default, moving the cross-page links (For AI, Contributors) to the top of the sidenav or into the persistent topbar, or a subtler height budget. Website generator/template only; verify with `.web/build.py --check`. **Partial (2026-07-24, #1111):** an offloaded grounded CSS diagnosis reasoned that the `max-height: calc(100vh - 2.5rem)` + `overflow-y: auto` sticky pattern is spec-correct (trailing links are reachable by internal scroll), and identified the one plausible cross-browser mechanical cause: `body { overflow-x: hidden }` can, on some engines, become a scroll container that breaks `.sidenav`'s viewport-relative sticky pin, so its lower portion falls below the fold. #1111 applied the zero-regression `overflow-x: hidden` to `overflow-x: clip` fix (clip suppresses horizontal overflow identically but never establishes a scroll container, guaranteeing the pin). This is the mechanical-robustness half; the primary tracked issue (the nav being too tall for a laptop viewport, so trailing links sit below the internal scroll fold and read as missing) is a UX-discoverability concern that stays open for the attended design pass above. Efficacy of the mechanical fix is to be visually confirmed by the maintainer; it is zero-regression regardless.

### 3.97 `grc_library_ref` `upstream_url` enrichment for FREE trusted-bucket entries (item 1.19 (closed 2026-07-25).7c follow-up, 2026-07-17, M; cross-repo `_ref`) `[machinery]`

The `/adopt` `.ref` bootstrap planner (`tools/adopt-bootstrap-ref.py`, item 1.19 (closed 2026-07-25).7c) can only AUTO-FETCH a FREE source that carries an `upstream_url`; currently only 8 of the 534 FREE trusted-bucket entries have one (all legislation), so 526 FREE sources fall into the "free-manual" bucket. Enrich `grc_library_ref/catalogue.yml` with `upstream_url` for the FREE `standards`/`frameworks`/`programs` entries (authoritative download pages) so the adopter bootstrap auto-fetchable set grows materially. Cross-repo (`grc_library_ref` PR); the manifest + planner then surface the URLs automatically on the next regen. Egress/lookup-heavy (each URL confirmed at its authoritative source); can be partitioned to workers per the research-assistant discipline.

### 1.14 External-source currency detection, Layer B: scheduled upstream-signal sweep (AUTHORIZED 2026-07-25; low priority, after the backlog is caught up)

**Layer A is DONE** (gate 72 plus `audit-register-currency.py`; closed 2026-07-25 on a measured
182-of-182 register coverage, see [`DONE.md`](.working/DONE.md)). Only Layer B remains, and the
maintainer AUTHORIZED its build on 2026-07-25 at low priority, to run after the backlog is caught
up. It is therefore no longer blocked on a decision.

Fetch a lightweight upstream signal per cited source (`Last-Modified` / `ETag`, a landing-page
version string, or a releases feed), compare against the recorded version, and notify on a change.
Constraints: it must NOT live in the read-only PR lint CI, and it must be fail-loud, bounded, and
authenticated per the API-polling guardrails. A detected change is a maintainer-notified PROPOSAL;
any applied citation or version update is upstream-confirmed that turn, verifier-checked, and
gate-validated, never silent.

**Note on the egress blocker:** this needs egress at RUN time, which a scheduled workflow has, so
it does not need an egress grant to the assistant's local session. Worth confirming before treating
the `egress` label as a blocker on the build.

**Item number retained on move.** Numbers are permanent and position carries no meaning; this moved
from Priority 1 to Priority 3 to reflect the maintainer's low-priority sequencing, not a renumber.

### Egress Gated

Items below need an egress-enabled fetch the assistant cannot perform, so they are parked here at
the end of this priority section rather than interleaved with actionable work. **Item numbers are
unchanged**: position carries no meaning, the number is permanent. Every source these items need is
listed in the `_private` maintainer-egress request so it can be batch-downloaded in one pass.

### 3.2 Authoritative standards register + designation-correctness gate (M-H, L; egress-gated)

The durable MECHANICAL solution to the ISO/IEC-designation-accuracy class (the per-occurrence reconcile that CLOSED the former §3.1 fixed the live corpus; this register-and-gate prevents regression): an authoritative register of every standard the project uses, recording each standard's correct issuing-body designation (`ISO` / `IEC` / `ISO/IEC` / `ISO/IEC/IEEE`) verified against the primary source, plus a norm (the corpus uses the correct designation; a direct quote of another source's differing usage is the only sanctioned exemption, marked as a quote); then a gate (sibling to GR-GAP-1, ideally sharing its register) that verifies each registered standard number's designation prefix matches the register, failing on a mismatch. Egress-gated (per-standard primary-source verification, the same egress §3.9 waits on). Design notes: (a) the designation axis is orthogonal to GR-GAP-1's version-year axis (share the register, different columns); (b) sole-ISO standards (27799, 31000, 9001) must stay bare, so the register's designation column is the source of truth, not a blanket "add /IEC"; (c) tripartite standards (12207, 42010) need `ISO/IEC/IEEE`, so the column is free-text designation; (d) the generic-family `ISO 27001` reference carve-out (family-names alongside `NIST CSF`, not edition-pinned citations, at `compliance/register-compliance-obligations-template.md:117`, `NOTICE.md:34`/`:60`) is an acceptable exemption the register records (migrated from the closed §3.1).

### 3.9 Require-registration citation-currency gate (GR-GAP-1, guardrail review 2026-07-02, M-H, M; egress-gated)

Both currency gates are enumeration-scoped (`lint-standards-currency.py` flags only register-recorded patterns; `lint-citations.py` is a hand-curated denylist), so a standard absent from both is structurally ungated (the ISO/IEC 29134 wrong-year escape #162 + recurrence #482). Proposed: a gate extracting every `ISO/IEC NNNNN:YYYY`-shaped citation and failing on any standard-year pair not in the canonical register (require-registration, not deny-known-bad). Boundary: "present in the register" = current-OR-superseded, so a superseded-but-registered pair stays gate 6's finding (no double-fire), and each new pair carries gate-27 re-verification cost. **Register-gap VALIDATED 2026-07-06:** 17 cited pairs have no register row + a live `ISO/IEC 29134:2017`-vs-`:2023` inconsistency, so the gate cannot ship clean until the 17 rows are populated, and populating them accurately needs upstream confirmation (egress-gated, the same egress §3.2 waits on). A future egress session: populate the 17 rows, resolve the 29134 conflict, then build the gate. Gap detail in `grc_library_private/design-decisions.md`. **NIST-side instance measured 2026-07-25 (Sweep 121 F-4):** the scope is not ISO-only. `NIST SP 800-208` is cited by four files ([`security/roadmap-post-quantum-cryptography.md`](security/roadmap-post-quantum-cryptography.md), [`security/policy-encryption-and-key-management.md`](security/policy-encryption-and-key-management.md), [`security/framework-cryptographic-key-lifecycle.md`](security/framework-cryptographic-key-lifecycle.md), and [`governance/register-document-index-and-classification.md`](governance/register-document-index-and-classification.md)) and has NO row in [`governance/register-canonical-citations.md`](governance/register-canonical-citations.md) (`grep` returns rc 1). It is therefore structurally ungated for currency, which matters more than usual for this one: #1156 corrected a FABRICATED title on exactly these citations, so the register row that would have anchored the real title ("Recommendation for Stateful Hash-Based Signature Schemes", confirmed at held source, October 2020 edition) was the missing control. Two consequences for this item's design: the citation-extraction pattern must cover the `NIST SP NNN-NNN` shape as well as `ISO/IEC NNNNN:YYYY`, and the SP 800-208 row is a populate-now candidate that needs NO egress, because the held reference base already carries the title and edition. **DONE 2026-07-25:** that row is now in the register (Final, 2020-10, upstream-verified against the CSRC page this session, HTTP 200 with the title and date both matching, and no errata, revision, withdrawal or superseding publication). The 17 ISO-side rows and the 29134 conflict remain, so the item stays open on those.

### 3.42 New-ingest reference-breadth pass: Canadian/international AI-governance sources (post-ref-resync 2026-07-10, M)

The standing post-PR `grc_library_ref` resync (maintainer-directed 2026-07-10) picked up newly-ingested held sources: **ISO/IEC 5259 parts 1 to 6** (Data quality for analytics and machine learning) and new **Canadian + international AI-governance** source captures. **ISO/IEC 5259 sub-part CLOSED (#1118):** [`ai/procedure-training-data-governance.md`](ai/procedure-training-data-governance.md) already cited parts 2/3/4 specifically (verified title-accurate against the held source), and the one warranted claim-accurate addition, part 5259-5:2025 (data quality governance framework), was added to its framework-alignment table; parts 1 (overview) and TR 6 (visualization) were judged off-claim and excluded. **REMAINING:** the Canadian/international AI-governance captures are candidates for the `ai/` domain documents (a looser, separately-scoped set, some egress-gated). Run `tools/audit-reference-breadth.py --ref-since <resync-sha>` to scope, then judge and apply per the reference-audit skill (trust tiers apply: standards citation-grade; screen any publications-bucket items). Surfaced by the post-PR resync 2026-07-10.

---

## Priority 4 — Adopter experience

**Next item number: 4.32.**

Capability and guidance for organizations adopting the library, and the operator-experience tooling for running the project. Scheduled deliberately, after the fix/gap/cleanup tiers.

### 4.1 Corpus-management discipline as a shareable skill (M, XL)

Package the cumulative documentation-and-corpus discipline as a standalone Claude Code skill anyone managing a documentation corpus with an AI assistant could install. Distillation source: the fifteen `governance/` pack rules (discipline core), `validation-sweep` + `library-fitness-review` (periodic-review surface), the audit-programme architecture (mechanical-enforcement surface). Decided 2026-06-22: skill **family** (not omnibus), **prescriptive-only** (no linter scaffolds), **existing pack 1.x bump**. After the FR backlog closes. UNBLOCKED: the pack adoption-hygiene programme is complete (phases 1-4, closed #846), so the distillation source (the condensed, adoption-clean governance rules) is merged and available.

### 4.3 Overnight unattended-run driver (M, L)

An external driver loop (cron / CI / Agent SDK, outside the corpus) that launches a fresh `claude -p` or SDK session per task-unit, each reading `.working/session-handoff.md` + the TODO/DONE queue, doing one unit, committing, advancing the queue, and exiting. The durable-state layer exists; the missing piece is the driver plus an overnight runbook. Design questions: where the driver runs; merge authority for unattended worker sessions; the stop condition; needs-maintainer vs safe-to-continue signalling; interaction with the change-tracking rule's overnight-work protocol.

### 4.4 Worker-ready brief staging (slice 4) + `/subagent` external-worker entry (M, L)

The remaining build slice of the INPUT half of the multi-session capability: **the `/subagent` slash command** as the external-worker entry point (read the assigned brief, claim it in `claims-ledger.md`, read named main-repo files read-only, produce findings, deliver to `inbox/`, stop; **read-only-on-main enforced by the worker account's permissions, not the prompt**) plus the maintainer-facing quick start in the runbook. Slices 1/2/3/5 SHIPPED (whole backlog covered by staged briefs + verdicts; the close-out pairing line, `/resume` freshness check, and [`tools/audit-brief-freshness.py`](tools/audit-brief-freshness.py)). **Gating maintainer action**: provision the least-privilege worker account (read `grc_library` / write `grc_library_scratch` only). The apply stage stays single-session with full QA regardless.

### 4.5 Adopter reference-base specification: build-your-own-ref guide, source lists, and the corpus-to-sources relevance map (L, L)

Adopters who clone the library do **not** receive `grc_library_ref` (it holds third-party reference works under their own licences and is not redistributable). Give them something better than a bare "good luck": a **specification an adopter's AI assistant can follow to assemble its own reference base**, right-sized to that organization's budget and licences. Deliverables to scope at build:

1. **The build-your-own-ref specification** (the centrepiece): a document written for an adopter's AI to execute, laying out the trust-bucketed tree and catalogue convention mirroring `grc_library_ref` (`standards/` trusted, `frameworks/` trusted-catalogue, `legislation/` version-sensitive, `publications/` screen-first, an `ingest/` staging area), and the ingest workflow (obtain from the authoritative source, extract to AI-readable text, catalogue, validate). It teaches the adopter's AI to reproduce the base, not just describes it.
2. **The public-source list**: every freely and authoritatively obtainable source the corpus cites (NIST publications, ETSI standards, OWASP, MITRE ATT&CK / ATLAS, CSA CCM / AICM, EU legislation via EUR-Lex, national legislation registers, EDPB guidelines, and the rest), each with where to get it from its primary source, so the adopter's AI can fetch and ingest the free tier with no budget at all.
3. **The suggested paid-source list**: the licensed sources worth adding **if the adopter or their organization has the budget** (the ISO/IEC catalogue, PCI SSC documents, and other paywalled standards), each with a one-line note on what coverage it strengthens, so an organization can make an informed spend decision rather than discovering the gap later.
4. **The corpus-to-sources relevance map (the reason this is worth trusting)**: surface, as a first-class adopter-facing artefact, *which* standards, legislation, frameworks, and other documents are relevant to *each* corpus document. A core reason the project maintains its own reference base is exactly this: the work of mapping every corpus file to the authoritative sources that bear on it is already done, and that mapping is kept honest by the citation, currency, and semantic-fit gates plus the `/reference-audit`, `/matrix-fit`, and `/claim-fit` cadences. An adopter who trusts that curation (as they reasonably can) inherits the relevance map for free and never has to rediscover, for each of their documents, which sources matter, the single most tedious and error-prone part of standing up a governance reference base.
5. **Helper scripts + wiring notes**: scaffold the tree, fetch-from-reputable-source where a licence and stable URL permit, extract text for AI-readability, build/refresh the catalogue; and notes on how a fork's base feeds the in-repo validator modules the citation and control-code gates build on, and `/matrix-fit`.

Never bypass paywalls or licensing; treat downloaded `publications/` as untrusted until screened. Low urgency; adopter-experience tier. (Broadened 2026-07-13 from the original fork-facing-scripts framing to lead with the AI-buildable spec, the public/paid source lists, and the corpus-to-sources relevance map as the headline value.)

### 4.6 Fork update-assessment tooling (upstream-change applicability report) (S-f, maintainer-requested 2026-07-04, M-L)

When an adopter's customized fork pulls upstream `grc_library` updates, nothing today helps THEIR AI assistant assess each upstream change against the fork's local customizations and present an accept/adapt/skip decision matrix. Design a fork-side instrument: likely a shareable skill (diff upstream release-to-release, classify each change by carrier class, map against the fork's recorded local divergences, produce the per-change report), plus upstream-side enablers where cheap (machine-readable change-class tags or per-entry applicability hints). Shape and upstream-vs-fork-side split are maintainer-scoped at design time.

---

### 4.29 `/adopt` adjustment + non-destructive tooling-update mode (maintainer-directed 2026-07-19, L) `[machinery]`

Extend the [`/adopt`](.claude/commands/adopt.md) skill (currently a run-once fork-onboarding flow that writes `.claude/adopt-config.json`) with an **adjustment/update mode** (a re-run flag) so an adopter fork can, at any time after the initial adoption: (1) **change earlier `/adopt` choices** (sibling model, ref/private/scratch wiring, which optional capabilities are on) by re-reading and rewriting the adopt-config rather than starting over; and (2) **pull updated TOOLING from a newer `grc_library` origin (the `tools/` audit toolchain, the `dev-security/claude-rules/` pack, the `.claude/` hooks/commands, the gate wiring) WITHOUT clobbering the adopter's own edited CORPUS files**, applying the update **non-destructively and reversibly** (a dry-run/preview of exactly what changes, a clean separation of upstream-owned tooling from adopter-owned content, a backup or git-checkpoint so any apply can be rolled back, and a conflict surface where an adopter has locally edited a tooling file). The driving goal (maintainer 2026-07-19): every piece of tooling that brings value, INCLUDING the operational instruments that currently live maintainer-side (the degradation-watch log and its threshold/validation discipline, the credit-offload design, the session-lifecycle machinery, the QA cadences), should either ship as adopter-usable guidance or be clearly documented as maintainer-only, and `/adopt` should let an adopter opt into and benefit from the ones that are portable, applied safely to their own project. Design questions to resolve at build time: the upstream-vs-adopter file ownership manifest (which paths are tooling the updater may overwrite vs corpus the updater must never touch); the reversibility mechanism (git checkpoint branch vs backup dir); how a locally-customized tooling file is reconciled (three-way merge, or surface-and-defer); and how the portable operational instruments are surfaced to the adopter (the `.private` placeholder path is the natural home). Related to but broader than §4.6 (which is the upstream-change applicability *report*); §4.29 is the *apply/adjust* mechanism that report feeds. Scheduled with the adopter-experience tier.

### 4.30 Full adopter-experience assessment + `.adopt/` adoption kit (maintainer-directed 2026-07-19, P4 umbrella, M-L, multi-phase)

The umbrella for a clean, great adopter experience from a public clone, and for moving maintainer back-end state out of the public repo WITHOUT depriving an adopter who wants it. **Phase 1 (assessment):** from a clean PUBLIC clone, enumerate every adopter-facing process (`/resume`, `/adopt`, the audit gates, the PR workflow, the QA cadences, the skills, the CLAUDE.md rules) and trace what each reads; flag every reference to something that lives in `_private` / `_ref` / `_scratch` (a gap for the adopter); classify each gap as (a) ESSENTIAL machinery-core the adopter's gates or `/resume` need (recreate for them), (b) OPTIONAL back-end capability the adopter might want (offer as per-adopter opt-in; the orchestrator-only files MAY be adopter-useful, maintainer-directed 2026-07-19, so it is the adopter's decision, not ours), or (c) MAINTAINER-PRIVATE (the process degrades gracefully, no adopter reference). **Phase 2 (the `.adopt/` kit):** a root `.adopt/` directory with a README (the decision guide: in-repo `.ref`/`.scratch`/`.private` stubs vs separate sibling repos; how `/adopt` works; how to decide; which back-end capabilities to opt into) and clean TEMPLATES for every essential machinery-core file that moves out (baselines `/adopt` CREATES in the adopter's chosen location, since they no longer ship publicly) PLUS opt-in templates for the back-end capabilities. **Phase 3 (adaptation):** move DONE + improvement-log (confirmed 2026-07-19) and any other assessed-essential file to `_private`; adapt the gates that read them (`check-todo-rotation-on-pr`, `lint-todo-marked-done`, gate 50 bookkeeping-parity, the tension/residual scans) to RESOLVE `_private`-or-adopter-location (the `resolve_sibling` pattern); ensure every adopter-facing process degrades gracefully when an opted-out file is absent; `/adopt` recreates from the `.adopt/` templates. **Coordinates / folds in the existing adoption items** (Phase 1 decides which fully merge vs stay separate): §4.1 (corpus-management shareable skill), §4.5 (adopter reference-base spec + build-your-own-ref guide, likely the `_ref` template piece of the kit), §4.6 (fork update-assessment tooling), §4.9 (pack public-distribution packaging, implemented in #1145: escaping links rewritten, dependencies documented, command names verified), §4.29 (`/adopt` adjustment + non-destructive tooling-update mode, the closest sub-item). **Build notes:** `.adopt/` is a real deliverable, not a gate-70 placeholder stub; check its README against the language + marker-word gates; pairs with the `/home/grc` migration and the `_private` relocation (design in `grc_library_private/design-decisions.md`). **Goal:** clone public, run `/adopt`, get a complete clean working-state set in the chosen location, with per-adopter opt-in to the back-end and zero orchestrator-only clutter.

### 4.31 Publish the governance pack as a standalone methodology (maintainer-directed 2026-07-23; M, M) `[content]`

Publish the `dev-security/claude-rules` pack as a citable, CC BY-SA methodology or reference model: the failure-mode provenance, the enforcement mechanism, the results. Adopter-experience work, hence Priority 4, separate from the P2 series and independent of the OSCAL machinery.

**Depends on:** the Task-1 pack reconciliation (completed 2026-07-23, so the published pack is current), 3.47 (P3, strip internal working-provenance for adoptability), 3.56 (P3), and 1.19 (P1, operational-state privatization and adopter-clone portability, the adoptability work that makes the pack project-agnostic).

**Blocks:** none.

**Alignment:** this is the publication step for the pack updated in Task 1 (the reconciliation completed 2026-07-23); keep it cross-referenced to that work.

## Priority 5 — Expand: country / regulator / programme overlays

**Next item number: 5.10.**

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

The `ai/jurisdictions/` subdirectory and its first annexes (EU AI Act #743, Colorado #749) shipped under the former FR-62. Remaining candidates, source-gated pending maintainer drops: UK AI policy framework; China generative AI rules; Korea AI framework. (Two candidates are STRUCK, not open gaps: Canada AIDA, covered by `ai/jurisdictions/annex-ai-canada.md` which correctly treats AIDA as lapsed (re-confirmed dead upstream 2026-07-24 by the research-canada-aida-status pass); and NYC bias audit law, covered in full by `ai/jurisdictions/annex-ai-us-new-york-city.md` (NYC Local Law 144 of 2021, the AEDT bias-audit law), with the implementing DCWP final rule (6 RCNY 5-300 to 5-304) held in the reference base and currency confirmed 2026-07-24 by the research-nyc-ll144-reconciliation pass. The §5.9 candidate-list reconciliation those passes prompted is now done for Canada and NYC; the three remaining candidates above stay source-gated pending maintainer drops.)

---

## Priority 6 — Expand: new domains

**Next item number: 6.6.**

Entirely new domains, multi-week scope each. The maintainer schedules deliberately. Ordered lowest-effort-first.

### 6.1 Identity-specific content depth (L) (was 6.2)

Customer Identity (CIAM) governance, workforce identity governance, identity federation patterns, passwordless adoption playbooks. Scoping research DELIVERED, with three proposed documents briefed as follow-on work-units in scratch (`research/ciam-governance-research/`, `research/identity-federation-patterns-research/`, `research/passwordless-adoption-research/`, grounded in held NIST SP 800-63-4); the BUILD stays maintainer-schedule-gated.

### 6.2 Quantum cryptography readiness deepening (L) (was 6.3)

The phase-level PQC roadmap exists. #1129 delivered the core content deepening (verified against the now-held FIPS full-text): NIST parameter-set to security-category mappings (ML-KEM / ML-DSA / SLH-DSA) with a category-3 interoperability baseline, a crypto-agility section (primitives as configuration, not hardcoded), ML-DSA-vs-SLH-DSA selection guidance, and the FIPS-205 citation currency, echoed in the encryption-policy PQC row and the crypto pack rule. The former source-gate is CLEARED: FIPS 203/204/205 are held in grc_library_ref and were confirmed current in #1129 (2024-08-13 finals, verified upstream). RESIDUAL (still L, now build-ready since the source-gate cleared): a dedicated PQC migration playbook (step-level how-to beyond the roadmap's phase plan) and post-quantum-ready CA/PKI implementation content. Corpus-internal scoping DELIVERED (`inbox/worker-20260703-a/quantum-pqc-readiness-scoping/`).

### 6.3 Cross-framework matrix expansion (L) (was 6.4)

Expand [`governance/matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md) to additional sectoral and regional frameworks as the P5 content grows.

### 6.4 CMMI capability levels alongside maturity levels (L) (was 6.5)

Low priority, after the FR backlog. Add a capability-level scheme (0-3 per practice area) alongside the 5-tier maturity levels: update [`governance/framework-governance-performance-and-improvement.md`](governance/framework-governance-performance-and-improvement.md) §2, [`docs/template-maturity-self-assessment.md`](docs/template-maturity-self-assessment.md), possibly the DTI thresholds. Research-only integration mapping DELIVERED (`inbox/worker-20260703-a/cmmi-sei-maturity-integration/`, four integration-shape options).

### 6.5 Multi-cloud governance overlay (XL) (was 6.1)

Per-cloud hardening baselines for AWS/Azure/GCP exist; the gap is multi-cloud governance (cross-cloud risk taxonomy, cross-cloud incident coordination, portfolio-level controls). Could live in `operations/` or a new `cloud/` domain. Scoping DELIVERED (`inbox/worker-20260703-a/multi-cloud-governance-scoping/`).

---

## Priority 7 — Awaiting maintainer decision

**Next item number: 7.6.**

### 7.1 Ruleset `non_fast_forward` (force-push) rule (deep-assessment r1 R8b, maintainer-owned)

The "Main Protection" repository ruleset enforces PR + status-check + signatures + no-deletion, but carries no explicit force-push (`non_fast_forward`) rule; the PR requirement makes direct pushes impossible, so this is low-priority hardening. A maintainer-owned GitHub setting, not a repo change: add the `non_fast_forward` rule to the ruleset if desired.

### 7.2 Per-regulation context (FR-104)

Per-regulation context not pursued (dropped-decision audit-trail record; see `grc_library_private/design-decisions.md`).

### 7.3 Portal reorder (FR-130)

Portal reorder not pursued (README stays at decision-tree item 1; dropped-decision audit-trail record).

---

## Time-bounded follow-ups

Non-urgent follow-ups deliberately DEFERRED to a future date, then re-evaluated: a suggested revisit of something already shipped, where acting now would be premature (not enough real-world signal yet). This is NOT the normal forward backlog (those are the Priority sections); an item here is date-gated, not ready-now, and will mostly track "revisit this suggested follow-up after date X". Each entry carries a **Not-before** date (UTC), what to EVALUATE, and the originating PR. `/resume` reads this section and surfaces any entry whose Not-before date has passed, so a due follow-up is not silently forgotten. When a follow-up is acted on (or decided against), rotate it to [`DONE.md`](.working/DONE.md) like any other closed item.

**Next item number: TF-3.**

### TF-2 Review the pack-parity coupling (convention + cadence), decide on the hard gate (2026-07-23, PR #1099)

**Not-before: 2026-08-23.** Evaluate whether the pack-parity-coupling convention (add the matching portable pack entry in the same PR that adopts a guard rail) plus the periodic pack-parity review have kept the published pack at parity with adopted practice, or whether drift recurred. If they proved insufficient, design the deferred hard gate (every project guard rail maps to a pack rule/skill or an explicit project-only annotation, accepting it needs a maintained project-only allow-list); otherwise leave the convention plus cadence as sufficient. Originating decision: the maintainer chose convention plus cadence now, defer the gate (2026-07-23).

### TF-1 Review the worker-saturation guard rail (L1+L2), decide on L3 (2026-07-23, PR #1098)

**Not-before: 2026-08-23.** Evaluate how the L1 statusline observable plus the L2 boundary checkpoint performed over roughly one month: did idle-worker episodes drop, were there false IDLE-CAPACITY signals or missed ones, did the checkpoint change behaviour at task-start and PR boundaries? Then decide whether to build L3 (the non-blocking saturation warning in [`block-mandatory-offload.py`](.claude/hooks/block-mandatory-offload.py)) or leave L1+L2 as sufficient. Originating decision: the maintainer chose option B (build L1+L2 now, defer L3 pending this review), 2026-07-23.

---

## Reference-base work (`grc_library_ref`)

Validated defects / standing work in the reference repo. The one remaining OPEN in-repo item (SR-1) ships as a `grc_library_ref` PR via `gh`.

### SR-1 `last_checked` currency mechanism is inert (item 26, P2, S)

As of 2026-07-05, 5 of 240 `grc_library_ref` `catalogue.yml` items carry a `last_checked` field, and `grc_library_ref`'s `tools/validate.py` checks the field's FORMAT only if present (no presence requirement), so the 7-day-throttle currency discipline has no on-disk footprint for the unstamped items. **Direction DECIDED** (maintainer 2026-07-02): presence + backfill (backfill stamps on the currency-sensitive buckets, then add a presence/due-item check). **Execution egress-gated:** an honest backfill needs a per-document upstream currency check (the same class the §3.2 / §3.9 reference-currency residuals wait on; the older 51-row register sweep is itself discharged). Held for the maintainer's egress instance.

### RB-R6 source-not-held acquisition (deep-assessment r1 R6, maintainer research-agent, S)

Sources cited in the corpus but not held in `grc_library_ref`, so their attributions cannot be adjudicated against held text. The maintainer runs this via a research agent that presents download URLs of the PDFs to fetch and ingest (the assistant cannot download them: iso.org is 403 from the VM and ISO standards are paywalled).

**Comprehensive not-held list compiled 2026-07-24 (RB-R6 research):** the full deduplicated not-held-but-cited set, each verdict `ref-holds.py`-executed, is seeded into the maintainer-egress-requests store with authoritative upstream URLs: 6 Tier-1 load-bearing sources (ISO 37301, ISO 19011, NYC Admin Code sections 20-870 to 20-874, Illinois BIPA, India DPDPA, IMO MSC-FAL.1/Circ.3) plus a Tier-2 register-level set. It SUPERSEDES the 3-example list below. Reconciliation of that older list: ISO 9001 §9.3 was reworded to the safe "planned intervals" framing (#758) so it is no longer an attributed-value dependency, and DORA is now held, so neither remains a Tier-1 acquire; ISO 37301 carries over. Acquisition itself remains maintainer-action (egress-gated). Original examples (retained for their per-citation locators):

- **ISO 37301** (Compliance management systems), Clauses 4-10 — cited at [`compliance/policy-compliance-and-audit-management.md:44`](compliance/policy-compliance-and-audit-management.md) ("Clauses 5 to 10"). Upstream: iso.org/standard/75080.html (paywalled).
- **ISO 9001** (Quality management systems) §9.3 — cited at [`governance/framework-governance-performance-and-improvement.md:55`](governance/framework-governance-performance-and-improvement.md). Upstream: iso.org/standard/62085.html (paywalled).
- **DORA RTS on incident reporting** (the Commission Delegated Regulation carrying the 4h / 72h / 1-month major-incident windows) — cited at [`compliance/financial-services/annex-dora-implementation.md:78`](compliance/financial-services/annex-dora-implementation.md) (already correctly qualified "subject to RTS/ITS", so NO corpus change; this is a value-verification tracker only). Upstream: EUR-Lex (the DORA Art 20 delegated instrument, likely freely fetchable, unlike the ISO standards).

On ingest, the ISO 9001 §9.3 attribution in [`governance/framework-governance-performance-and-improvement.md`](governance/framework-governance-performance-and-improvement.md) (reworded to the safe "planned intervals" framing in PR #758) and the ISO 37301 attribution at [`compliance/policy-compliance-and-audit-management.md:44`](compliance/policy-compliance-and-audit-management.md) can be adjudicated against the held text.

### Reference-base acquisition and assessment queue (`grc_library_ref`; maintainer-directed 2026-07-07)

RB-1 (PCI), RB-2 (staging_ref ISO/CIS), RB-3 (NIST CSRC harvest, ref PRs #5-13), RB-4 (OWASP, ref PRs #14-19 + #22), RB-5 (MITRE, ref PR #20), and FedRAMP (ref PR #21) are COMPLETE (rotate to DONE at the cross-repo morning-processing). Standing watch:

- **RB-6 reference-base currency + draft watch**: standing watch on items whose upstream has a pending revision. (a) Planned-but-unpublished NIST revisions (FIPS 202/203/204/205; FIPS 198-1 -> SP 800-224 draft; SP 800-131A Rev 3 IPD; SP 800-38D; SP 800-46 Rev 3; SP 800-90A Rev 2) — re-check on finalization. (b) Draft-watch (NIST IR 8596 Cyber AI Profile; SP 800-53 COSAiS AI overlays; Privacy Framework 1.1 CSWP 40 IPD). (c) Controlled-vocabulary gap: `grc_library_ref/topics.md` has no `cryptography` tag (the ~15 held crypto standards map to `cybersecurity` only); assess adding one. (d) FedRAMP 2026 evolving-preview: establish a re-snapshot cadence when the daily-updated Public Preview stabilizes. (e) **AICPA TSP 100 held-edition mismatch** (surfaced Sweep 101, 2026-07-13): the canonical-citations register cites the *2017 Trust Services Criteria with revised points of focus (2022)* (upstream-verified against aicpa-cima.com 2026-07-13, real-world-accurate; register-only, no corpus document cites it), but the copy held in `grc_library_ref` (`frameworks/AICPA/AICPA-TSP-100-2017-Trust-Services-Criteria-revised-POF-2022-clean--full-text.md`) is the earlier *March 2020* edition, so the held text does not substantiate the cited 2022-revised-POF designation. Low risk (register-only citation; the citation itself is accurate and upstream-verified). Resolution: attempt to acquire the true 2022-revised-POF edition into `grc_library_ref` per the missing-reference-document SOP (the AICPA download page may be membership-gated), then reconcile the register row's held-edition provenance; if unavailable, qualify the row's provenance to name the held March-2020 edition. Flagged for the `/deep-assessment` `/reference-audit` + `/claim-fit` passes.

- **RB-7 residual (egress-gated follow-ups)**: RB-7's acquire-and-assess is COMPLETE (the four AI-defense-matrix-surfaced frameworks acquired/ingested and their corpus use/cite applied across PRs #1057-#1063; DONE below). (i) **OWASP Top 10 for Agentic Applications** authoritative source: **RESOLVED 2026-07-23** — the maintainer uploaded it, it was ingested into `grc_library_ref/frameworks/OWASP/` (`_ref` PR #101), currency was confirmed upstream (Version 2026, released December 2025, current on genai.owasp.org), and it is now cited authoritatively in the corpus (`ai/register-ai-risk.md` framework-alignment row plus the `governance/register-canonical-citations.md` row upgraded from the wrong-URL crosswalk to the authoritative Top 10). **Follow-up (a `/matrix-fit`-class pass, NOT egress-gated):** the fuller integration into [`ai/standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md) — a §36 alignment-matrix ASI01-ASI10 column mapped per Control Area and a §6 threat-class crosswalk (the verified ASI-to-TC crosswalk is in the scratch `research-owasp-agentic-ingest-cite` delivery), including the maintainer decision on ASI08/ASI09/ASI10, which have no clean single-TC home (cite-only vs adding TC classes). (ii) **Colombia RNBD (Registro Nacional de Bases de Datos), Decreto 886 de 2014** (WAF-blocked 2026-07-22; assess for the LatAm privacy annex once acquired) — still egress-gated.

---

## Standing conventions

Durable behavioural guidance from the maintainer. NOT actionable items; reference material for the orchestrator and future contributors.

- **"More PRs, keep each one clean"** — favor small focused PRs.
- **"One item, one functional action"** (2026-07-10) — split TODO items per distinct resolution path; group bullets under one number only when they resolve as a single action.
- **TODO numbers are permanent and never recycled** (2026-07-15) — each priority section carries a `Next item number:` counter, maintained on every TODO edit; new and split-out items each draw the next number and advance the counter, closed numbers retire with their item, and existing items are not renumbered when the file is reorganized (so a number maps to exactly one item across the file's whole history and lookups by number stay unambiguous). A series-consolidation move is the one exception that still never REASSIGNS a number: the content moves to a new series child `X.Y.Z` and a forward redirect stub is left at the original number (both close together), see the numbering-rule paragraph at the top of this file (2026-07-23).
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
- Design decisions belong in `grc_library_private/design-decisions.md`, not TODO.
- This file is the source of truth for what's queued; conversation history is not.
- Fitness-review backlogs remain the authoritative per-finding evidence source; this file is the action-organized view.

---

## Maintainer or Egress Gated

**No-priority registry (TODO §1.22.7).** Every open item the assistant CANNOT clear alone: it needs a **maintainer action** (a download the assistant cannot fetch, a design or value decision, or an explicit sign-off) OR an **egress-enabled run** the assistant lacks from this VM. Purpose: make "what the assistant cannot do alone" unambiguous, so the run never claims "done all I could" while actionable items remain. Each carries a stable **MEG-NN** reference number so the maintainer can say "I did MEG-14"; egress/download rows carry the source lead where one is recorded (never fabricated). Items also live in their priority sections above; this is the cross-referencing index, not a move. Download rows already in the `grc_library_private` maintainer-egress queue are marked (the queue holds the authoritative fetch list; this section indexes, does not duplicate). **Egress re-test forcing function:** `detect-env` now shows iso-org + nist-csrc reachable (HTTP 200) where earlier sessions saw 403, so the flagged re-test candidates (MEG-02 MiCA via EUR-Lex, MEG-07 ISO, MEG-20 ISO/IEC 5259) must be egress-re-tested and CLEARED into `_ref/ingest` rather than parked (guarding the 2026-07-09 wrongly-egress-gated recurrence); they are candidates, not confirmed-blocked, until the re-test runs.

### Group 1: maintainer-download / source-gated (fetch a source the assistant cannot get)

| Ref | Item | What the maintainer fetches / source lead |
|---|---|---|
| MEG-01 | §2.3 (FR-70) | NYDFS BitLicense (23 NYCRR Part 200), crypto-asset domain. Landing `dfs.ny.gov/virtual_currency_businesses`; full text WestLaw-gated (403). [in egress queue] |
| MEG-02 | §2.3 (FR-70) | MiCA (EU Reg 2023/1114). Freely available on EUR-Lex; **RE-TEST egress + clear to `_ref/ingest`** (not queued). |
| MEG-03 | RB-7 (i) | OWASP Top 10 for Agentic Applications authoritative source. **FULFILLED 2026-07-23** (ingested `_ref` #101, cited #1069); kept for the record. [was in egress queue] |
| MEG-04 | RB-7 (ii) | Colombia RNBD, Decreto 886 de 2014. `funcionpublica.gov.co` WAF-blocked. [in egress queue] |
| MEG-05 | 2.25.3 (formerly item 2.22 (closed 2026-07-25)) | Canada.ca 49-source utilization. **STATUS DRIFT:** the egress-queue Fulfilled record says the 16 sources were ingested (`_ref` #87) and the currency half discharged; reconcile 2.25.3's "DEFERRED-BLOCKED" status (may be dischargeable). [in egress queue] |
| MEG-06 | §1.22 (item 1.22.9) | Add the direct canada.ca AI/privacy-suite download URLs to the `_private` egress list (verify each canonical path, no fabrication). [partial leads recorded] |
| MEG-07 | RB-R6 | Source-not-held acquisition (ISO paywalled/403 historically). Maintainer runs via a research agent; **RE-TEST** iso-org (now 200). |
| MEG-08 | §2.1 (FR-59) | Privacy annex deepening: ~18 source-gated country annexes await maintainer source drops. |
| MEG-09 | §2.21 | Further AI-jurisdiction annexes, deferred pending held sources. |
| MEG-10 | §5.4 | Healthcare country regulator overlays: source-gated except EU MDR/IVDR (held). |
| MEG-11 | §5.7 | Public-sector country/regulator overlays: source-gated. |
| MEG-12 | §5.8 | Privacy jurisdiction gaps (Argentina PDPA 2025, Saudi PDPL): source-gated. |
| MEG-13 | §5.9 | AI jurisdiction overlays (UK, China, Korea): source-gated. Canada AIDA and the NYC bias-audit law are NOT in this queue: both are STRUCK candidates rather than open gaps (AIDA lapsed and re-confirmed dead upstream 2026-07-24; NYC covered in full by its own annex), per the section 5.9 body. Do not acquire sources for either. |
| MEG-14 | §6.2 | Quantum-crypto readiness: source-gate CLEARED in #1129 (FIPS 203/204/205 held + confirmed current); core deepening shipped; residual is a PQC migration playbook + PQC-ready CA/PKI (build-ready). |
| MEG-15 | AI Strategy FPS | Complete re-download of the AI Strategy for the Federal Public Service 2025-2027 full text (LOW; currency, not a content gap). [in egress queue] |

### Group 2: egress-blocked (an egress-enabled run the assistant lacks; not a single download)

| Ref | Item | Note |
|---|---|---|
| MEG-16 | §1.14 Layer B | External-source currency upstream sweep (Layer A shipped as gate 72). Needs a network-enabled runner (DD-10). |
| MEG-17 | §3.2 | Authoritative-standards register + designation gate: per-standard primary-source verification. |
| MEG-18 | §3.9 (GR-GAP-1) | Require-registration citation-currency gate: register-row population from upstream + the 29134:2017-vs-:2023 resolution. |
| MEG-19 | SR-1 | `last_checked` backfill: honest backfill needs a per-document upstream currency check. |
| MEG-20 | §3.42 | New-ingest reference-breadth over Canadian AI-gov sources (ISO/IEC 5259 sub-part CLOSED #1118: 5259-5:2025 added to training-data-governance). |
| MEG-21 | §3.97 | `_ref` `upstream_url` enrichment for FREE entries (egress-heavy; a `_ref` PR; partitionable). |
| MEG-23 | item 3.55 (closed 2026-07-25) | `_ref` bulk-ingest of the ~64 staged `ingest/` files (cross-repo; per-doc currency the egress-facing part). |
| MEG-25 | §2.18 | South Korea AI Basic Act annex: `[VERIFY]` the phased dates upstream at apply (source HELD). |
| MEG-26 | §2.23 (statute half) | CCPA STATUTE-currency review once `ingest/ccpa_statute_eff_20260101.pdf` is ingested to `--full-text.md`. |
| MEG-27 | §2.20 | Ref-side `last_checked` sweep for the 6 new EU/CA AI sources (cross-repo). |

### Group 3: maintainer-decision (a design/policy/value choice; no download)

| Ref | Item | Note |
|---|---|---|
| MEG-30 | §1.22 (item 1.22.8) | Chat text-pacing convention (an AskUserQuestion continue-gate was captured in `_private`; discuss). |
| MEG-31 | §3.3 | Removal-ledger review cadence (standing). |
| MEG-32 | §3.6 | Register-ageing advisory (needs a classifier / register-format decision). |
| MEG-33 | §3.7 | Expiry-tail batch review (maintainer dispositions). |
| MEG-35 | §3.54 | `doc_type` back-fill in `_ref` (explicitly NOT automated; ~20 questions + iterated sign-off). |
| MEG-39 | §3.74 | Standards-reference-format standardization (maintainer preference review). |
| MEG-40 | §3.94 | Landing-page sidebar overflow (lower-priority website call; footer-mitigated). |
| MEG-42 | §7.2 (FR-104) | Per-regulation context (Priority 7, awaiting maintainer decision). |
| MEG-43 | §7.3 (FR-130) | Portal reorder (Priority 7, awaiting maintainer decision). |
| MEG-44 | §3.80/3.81/3.82/3.83/3.88 | Credit-offload design thread: several maintainer-flagged design rows (cross-repo scratch/design; split per row when worked). |

### Group 4: maintainer-sign-off (irreversible / protected-branch; explicit authorization; LAST by design)

| Ref | Item | Note |
|---|---|---|
| MEG-45 | item 1.19 (closed 2026-07-25).13 | History scrub (Phase 6): git-history purge + force-push; MAINTAINER-GATED and LAST (prep drafted in `_private`). |
| MEG-46 | item 3.16 (closed 2026-07-25) | CHANGELOG history-collapse residual: a protected-branch history rewrite (optional; maintainer-gated). |
| MEG-47 | §7.1 | Ruleset `non_fast_forward` (force-push) rule: a maintainer-owned GitHub setting (low-priority hardening). |
| MEG-48 | 2.20 | Upstream currency pass for the 6 EU / CA AI sources in `_ref` `catalogue.yml`, so `last_checked` can be stamped honestly (it records upstream verification, which held material cannot establish). EU Digital Omnibus first: it awaits a dateable adoption event, not a date refresh. Also confirm the 6 drafted `upstream_url` values resolve. Needs an egress-capable run or a maintainer session. |
