# TODO

Forward-looking backlog of planned enhancements for the GRC Documentation Library. Items are added when identified and rotated out when completed. Completed items move to `grc_library_private/.working/DONE.md` (closed-TODO ledger, keyed by original backlog ID); historical change detail lives in [`CHANGELOG.md`](CHANGELOG.md). This file holds only pending and queued items.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions, with one narrow exception: [`tools/lint-todo-staleness.py`](tools/lint-todo-staleness.py) (gate 45) scans this file for the queued-PR-already-merged drift shape (its companion sweep-cursor-behind-history check reads the resume cursor from `grc_library_private/.working/session-handoff.md`). The intra-document section-reference gate also scans it. Other audit gates skip this file.

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
- **Integrity-tooling items** live in **P1** (reference version-currency residuals) and **P3** (the gate/lint machinery). Research fan-out (workers produce verified research from `grc_library_private/.working/worker-brief-template.md`; the orchestrator re-verifies every claim at apply-time and authors all final prose) is the standing method for partitionable batches.

---

## Priority 1 — Fix errors and prevent recurrence

**Next item number: 1.28.**

Correctness fixes and the **error-prevention tooling** that keeps the corpus from regressing.

P1 currently holds the **1.26** quality-machinery series (a goal-description umbrella plus its public phases 1.26.2 to 1.26.20, UNBLOCKED with the aiqt/guardrails architecture locked to Option B on 2026-08-02); the private phase 1.26.1 and the former P1 items 1.22 / 1.23 / 1.19.13 moved to the private `P-TODO.md` in the 2026-07-31 public/private split. Point-fix items are opened and closed in place as they arise; the closed ones live in `.working/DONE.md`, not here.

### 1.26 Consolidate, harmonize, and distribute the quality machinery across AI toolchains (goal-description umbrella; multi-phase series; maintainer-directed 2026-07-26; UNBLOCKED 2026-08-02, focus on aiqt.ai) `[public]`

**UNBLOCKED; architecture LOCKED by the maintainer 2026-08-02.** `grc_library` is the authoritative authoring and dogfood source for the AIQT principle, the portable governance core, and the universal skill; the standalone `guardrails` repository (private) is a one-way publication target. The pack relocates from `dev-security/claude-rules/` to root `guardrails/` (a canonical core plus generated coding-agent adapters); the guardrails README orients to aiqt.ai, and `grc_library` directs pack-only adopters there after the cutover. The series is executed via an expensive-QA workflow (prep, execute, dual-family QA, final QA): the prerequisite items first, then the migration, then the repo and site. Full architecture of record below; the strategy and the reconciled dual-family assessment are in the private `aiqt_strategy.md` / `aiqt_strategy_assessment.md`.

The quality system (the audit gates, the PreToolUse hooks and guardrails, the `tools/` scripts, the pack rules and skills) has grown fast and organically, one control at a time, each earned by a real failure. That growth is the system working, but it has left overlap, near-duplicate checks, conventions layered several generations deep, and structure that no longer reads as designed. And the work is no longer the maintainer's alone: many of the team, and some adopters, now run the library on local and custom models, and under the CC BY-SA ShareAlike licence they have submitted their own improvements and suggestions back. This series is where the machinery is made sound and where those contributions are brought home: consolidate and simplify what has accreted, integrate what the community has sent back, reconcile the in-project practice with the public pack, and distribute the result in the idiom every team member's toolchain speaks. The umbrella here is the goal; its phases below are the work, each independently closeable.

**Architecture of record (maintainer-locked 2026-08-02).** The three directional questions previously flagged here are now decided (both expensive dual-family assessors converged; see the private assessment):

- **Authoring direction:** `grc_library` authors and dogfoods the portable core; the standalone `guardrails` repository is a one-way publication target (never an upstream authoring dependency). This is Option B.
- **Canonical release unit:** a root `guardrails/core/` holding the AIQT principle, the maintainer-confirmed governance-rule set, and one canonical universal skill.
- **Adapters:** only coding-agent file-convention forms are adapters, and every adapter is GENERATED from the core; chat products (ChatGPT, Claude, Copilot, Gemini) consume the universal skill directly with no adapter.
- **Anti-drift:** the core is authored once; generated outputs are verified by a network-independent CI `--check` that extends gate 37, and each published release records the source revision and manifest digest.
- **Local-only boundary:** hooks, corpus audit gates, private operational state, the worker exchange machinery, and project overlays stay in `grc_library`; they are never part of the published core.
- **Publication orientation:** the guardrails README points to aiqt.ai; `grc_library` directs pack-only adopters to that public product after the cutover.

Relocating the pack to root and shipping a Codex/ChatGPT-native form are both subsumed by this decision (root `guardrails/` + generated adapters + the universal skill).

**Value-and-proof expansion + early-relocation resequence (maintainer-directed 2026-08-02; three-lens theory-craft review, private synthesis `prep-candidates/theorycraft-SYNTHESIS.md`).** The three assessors converged that the plan was engineering-complete but proof-thin: it defined success as correct PUBLICATION of files, not proven BEHAVIOUR, adoption, or value. Phases 1.26.7 to 1.26.20 add the missing layers: the keystone conformance suite (1.26.7), release governance, the coverage-gap rules (Cost, oversight, incident), the framework-symmetry fix, the provenance-as-proof casebook, the adoption on-ramp, the community flywheel, honest support and certification framing, and the external publication (1.26.20). A durable product proves five things: one canonical discipline, every distributed form traceable to it, its required behaviour testable, its support claims bounded by recorded evidence, and adopters who can start small, verify what they installed, and see outcomes and limits. Sequence: the INTERNAL relocation to root `guardrails/` (1.26.4) is done EARLY, before the new content phases, so everything after is authored at the final location and nothing needs repointing later; 1.26.5 splits into a baseline manifest (early) and a final manifest (pre-publication); the coverage-gap rules (1.26.9, 1.26.11, 1.26.17) and the framework columns (1.26.10) land before the freeze; the conformance suite (1.26.7) and casebook (1.26.12) after the core is classified and authored; the external PUBLICATION (1.26.20) is last, after classify / agnostic / freeze; `3.142` (`/sitrep`) stays a CORE pack skill but is NOT on the release critical path; `3.130` recovery is absorbed into 1.26.6. Not in a rush: do it right the first time. **On COMPLETION of this umbrella (final phase 1.26.20), the CHANGELOG gets a distinguished MILESTONE entry summarizing the whole guardrails achievement, the portable AIQT core, the universal skill, the conformance suite, the adapters, and the publication (maintainer-directed 2026-08-02), not a routine per-PR line.** (The deleted predecessor repository was removed by the maintainer; the sole repo is `jposluns/guardrails`.)

### 1.26.2 Integrate the community's ShareAlike contributions (H, L) `[public]`

Many of the team and some adopters have implemented the library on local and custom models and, per the CC BY-SA ShareAlike licence, submitted their improvements and suggestions back. This is where those are all integrated: triage each contribution, validate it against the project's standards, and fold the accepted ones into the machinery and the pack, credited per the licence. The submissions from real-world local-model use are also the sharpest signal for what the tool-agnostic distribution (1.26.6 and the external publication 1.26.20) must get right.

### 1.26.3 Freeze the true-parity guardrails source snapshot (H, M) `[public]`

After the pack-coupled machinery is consolidated (1.26.1), accepted community input is integrated (1.26.2), the disclosure matrix is signed off (P-1.18), the core is project-agnostic (3.56), the publication source set is classified (1.26.5), and the universal skill is dogfooded (1.26.6), reconcile every core file to true parity with the disciplines the project actually runs and FREEZE the exact pre-publication source snapshot that becomes the first `guardrails` release. This is the last prerequisite before the external publication (1.26.20).

### 1.26.4 Relocate the pack to root `guardrails/` (EARLY: location and references) (H, XL) `[public]`

**Sequenced EARLY (maintainer-directed 2026-08-02): do the internal relocation BEFORE the new content phases so all subsequent work is authored at the final location and no reference or pointer needs repointing later.** Move `dev-security/claude-rules/` to root `guardrails/` (a canonical `guardrails/core/`, deterministic build tooling under `guardrails/build/`, and generated coding-agent adapters under `guardrails/adapters/`, Claude Code + OpenAI Codex first), extend gate 37 with the generator `--check`, repoint the ~493 references to the old `dev-security/claude-rules/` path (private migration inventory), repoint every hook / CI / runner path, and keep the full gate suite green. INTERNAL relocation only: it does NOT require the publication prerequisites (classify / agnostic / freeze), which gate the external publish (1.26.20). Non-partitionable, single atomic PR. The universal skill (chat) needs no adapter. Migration-design prep: the private `1264-migration` worker delivery.

### 1.26.5 Classify the guardrails publication source set (H, M) `[public]`

Create an exhaustive, machine-validated publication manifest covering every current pack file: classify each as guardrails core, generated-adapter input, GRC-only, or excluded, with a disclosure status and rationale, so the release set and the anti-drift `--check` have a definitive source of truth. A prerequisite for the freeze (1.26.3) and the external publication (1.26.20). Sequenced in two stages (2026-08-02): a BASELINE manifest early (to unblock the conformance suite 1.26.7 and the shadow-build) and a FINAL manifest reconciled just before the freeze.

### 1.26.6 Author and dogfood the canonical universal AIQT skill (H, L) `[public]`

Author one provider-neutral skill from the classified governance core: a short AIQT card, a lean full protocol, explicit capability and no-tool degradation, the portable long-session-recovery discipline, and proportional verification. It is the deliverable chat platforms consume directly and the source the coding-agent adapters are generated from. Absorbs the portable parts of the former 4.1 / 3.130 / 3.187 (do not build a competing skill family). The three tiers (card, lean protocol, referenced deep modules) carry a ROUTING line so the situational deep modules (high-assurance, trust-recovery, conformance) are reached rather than left as dead references (2026-08-02).

### 1.26.7 Conformance suite plus a normative AIQT conformance contract (H, L) `[public]`

THE KEYSTONE (all three theory-craft lenses ranked it first): a library of adversarial scenario fixtures, one per discipline, each engineered to tempt a specific violation (dangle a false completion claim, execute off a discussion with no express go, obey an instruction injected in retrieved content, accept a set-completeness trap, silence a failing gate, ask for a findable fact), scored by ACTION TRACE not output vocabulary. It simultaneously proves the pack works, IS the operational definition of model-independence (each assistant family passes a threshold of fixtures with the skill loaded), enables a conformance badge and a CI action, supplies the value metric, and gates community-contributed rules to quality. Self-validate the rubrics with the project's own mutation-testing-of-guards technique (`validate-inference` guard-inputs: who verifies the verifier). Answers the pack's own top named risk (decorative compliance: recite, not apply). CORE-portable; build after the core is classified (1.26.5) and the universal skill authored (1.26.6).

### 1.26.8 Reproducible release provenance and governance (H, M) `[public]`

The release layer a published product needs: each release records the source revision, the manifest digest, and per-adapter generated-output digests, with signed release metadata, a known-limitations statement, a rollback path, an emergency-patch process, and deprecation windows. Closes the one-way-publication-lag risk (a security or correctness fix stuck in the authoring repo while the public copy is stale) and the currency-burden risk. Composes with the gate-37 `--check` and the publication (1.26.20).

### 1.26.9 The Cost tier: a portable cost and runaway-loop discipline (H, M) `[public]`

The missing fourth tier: AIQT names Cost as its lowest priority yet no rule governs it. A portable governance rule bounding token and compute budgets, runaway agentic loops, unbounded fan-out, and the cost of the pack's own dual-family and high-assurance layers, framed correctly (bound cost WITHOUT ever trading down the AIQT tier; cap loops, recursion, and fan-out; escalate when the budget would force an AIQT compromise). Closes the most visible internal asymmetry. Composes with `project-integrity` (the tier) and `session-lifecycle` (bounded retries). CORE-portable.

### 1.26.10 Framework-alignment symmetry: add NIST AI RMF and ISO/IEC 42001 to the governance rules (H, L) `[public]`

Fix the concrete asymmetry: the `ai/*` security rules map to OWASP LLM Top 10, MITRE ATLAS, CSA AICM, and NIST AI RMF, but the 15 governance rules (the actual product) map only to SSDF / CCM / ISO 27001 / ASVS, so they read as software governance rather than AI governance. Add NIST AI RMF and ISO/IEC 42001 columns (and a pack-level crosswalk) to the governance rules; the source mapping largely exists in `project-integrity` and the corpus. HARD constraint: every added cell is a PRESCRIBED mapping verified against the framework text per the pack's own `claim-fit` / `lint-standards-currency` discipline, never a plausible-looking id (a hallucinated cell in a pack that preaches citation precision is self-refuting). Do NOT over-map ATLAS / LLM Top 10 onto the governance rules (attack taxonomies belong on the security rules). CORE-portable.

### 1.26.11 A human-oversight and autonomy-threshold rule, with EU AI Act Art. 14 (H, M) `[public]`

The headline topic of every AI-governance framework, currently absent as a single rule: how much autonomy for which risk class, and what forces a human into the loop. Consolidate the existing pieces (`clarify-before-acting`, `express-authorization`, `decision-classification`, `session-lifecycle` modes, the reversibility gate) into one risk-tiered oversight rule, with a scoped EU AI Act Art. 14 touchpoint (cited conservatively and dated). Mostly consolidation, not net-new. CORE-portable.

### 1.26.12 Provenance-as-proof and the sanitized caught-defect casebook (H, M; disclosure-gated) `[public]`

Make the moat visible: the pack's disciplines are earned from real incidents (`rule-provenance.md`), which no style-prompt pack can claim. Surface, at a safe abstraction, one real caught-defect per discipline (the failure shape, what the rule did, the class of defect prevented) with all project specifics stripped, plus the provenance table (rule from the failure class that created it). HARD-gated on the P-1.18 disclosure matrix (generalize to failure CLASS; keep the safe aggregate; never ship PR numbers or private topology). Doubles as the seed corpus for the 1.26.7 conformance fixtures. CORE-portable after disclosure clearance.

### 1.26.13 Tiered adoption and the two-minute on-ramp (H, M) `[public]`

The adoption path the site needs: a three-tier product (the AIQT card, the lean universal skill, the full pack plus adapters) shown as an explicit adoption ladder, with a per-platform copy button (clipboard gets the correctly-shaped file) and a one-command installer (`npx aiqt init` / `pipx run aiqt`) that detects the project's agent and drops the right adapter. The literal landing-to-using-in-two-minutes on-ramp. Refines 1.26.6's tiering with a routing line so the deep modules are actually reached. Mixed (site project-only; adapters and card CORE).

### 1.26.14 Community flywheel and contribution governance (M, M) `[public]`

Turn adopters into contributors: a submit-a-failure-mode-get-a-rule intake that triages adopters' own agent-failure incidents into new guards (credited per ShareAlike), plus the governance to sustain it (a contribution RFC process, security review of contributed rule prose, and independent pilots) so v1 does not become a frozen one-maintainer artefact. The flywheel that regenerates the provenance stories (1.26.12) that are the moat. Seeded by 1.26.2. CORE-portable process.

### 1.26.15 Capability and compatibility matrix with bounded support claims (M, M) `[public]`

A dated support matrix per tested assistant family: how the skill is supplied, whether it persists across turns, and its conformance pass rate (from 1.26.7). Makes the universal-architecture claim honest and bounded rather than a `SKILL.md` label, and gives adopters an accurate expectation per platform. Pairs with 1.26.7 and 1.26.8. Mixed.

### 1.26.16 AIQT threat model and responsible disclosure (M, M) `[public]`

The security posture a distributed governance artefact needs: a threat model covering malicious contributions, adapter tampering, prompt injection through referenced content, and a responsible-disclosure process. Composes with the community intake (1.26.14) and the release governance (1.26.8). CORE-portable.

### 1.26.17 An AI-incident-response discipline (post-escape) (H, M) `[public]`

Completes the lifecycle (prevent, verify, recover-process, and now RESPOND-to-escape): a rule governing a harmful AI output or action that shipped, contain, roll back, disclose, learn, built from the pack's existing raw material (the revert-path override register, the artefact-and-branch rollback discipline). `trust-recovery-escalation` recovers trust after a discipline lapse; this governs a shipped harmful result. Maps to NIST AI RMF Manage and incident-reporting regimes. CORE-portable.

### 1.26.18 A cautious certification ladder (M, S) `[public]`

Positioning that avoids certification theatre and liability: begin with a self-check, then a reproducible conformance report (from 1.26.7), then, only with independent programme governance, reviewed attestation language. Never claim certified / compliant / universal beyond what the recorded evidence bounds. Governs the trust language across the site and README. Depends on 1.26.7 and 1.26.15.

### 1.26.19 A dogfooding outcome scorecard (M, M; disclosure-gated) `[public]`

Publish privacy-safe aggregate evidence that the pack works: disciplines traced to failure classes, conformance pass-rate trends, and the DUAL-FAMILY DIVERGENCE RATE (how often the second model family caught what the first missed), which empirically justifies the pack's most distinctive control. Governed by the pack's own measured-vs-estimated discipline (never sum a measured figure with an estimated one; UNKNOWN never zero) or it is self-refuting. Disclosure-gated (P-1.18). CORE-portable after clearance.

### 1.26.20 Publish the frozen core to jposluns/guardrails and launch the site (H, L) `[public]`

The one-way EXTERNAL publication, sequenced LATE (after the core is classified, agnostic, and FROZEN: 1.26.5-final and 1.26.3): export the frozen `guardrails/core/` and generated adapters to the standalone `jposluns/guardrails` repository with the release provenance of 1.26.8, and launch aiqt.ai as the adoption-and-evidence product (quickstart, per-platform on-ramp, the conformance report, the framework crosswalk, the casebook, the support matrix, releases, and the contribution flow). Distinct from the EARLY internal relocation (1.26.4): this is the external publish, which needs the frozen publication-ready core.

## Priority 2 — Fill significant gaps

**Next item number: 2.29.**

Deepening thin-but-present content to operational sufficiency, and the significant missing capabilities.

### 2.1 Privacy jurisdiction annex operational deepening (FR-59, H, L) `[public]`

Privacy jurisdiction annexes are too shallow for operational sufficiency; deepen the remaining source-gated country annexes to operational level. Japan, United States, Canada, and Brazil are deepened (2026-07-04 held-source batch 1); the Latin America correction + standalone Mexico annex shipped in #750 (discharging the fr-59 Mexico accepted-unverified tracker against the held 2025 LFPDPPP). Remaining: the 18 source-gated annexes (gap analysis at `inbox/worker-20260703-a/fr-59-privacy-jurisdiction/research-source-gated-gaps.md`), which wait on maintainer source drops (APAC beyond Japan, and others absent from the reference base). Out of this item by design: the EU annex (fr-74-owned) and the UK annex (already operationally deep).

### 2.3 Crypto-asset / blockchain governance domain (FR-70, H[critical], XL) `[public]`

New domain for crypto-asset / blockchain governance: digital-asset custody, staking, smart-contract risk, blockchain platform vetting. Regulatory references: DORA, MiCA, NYDFS BitLicense (DORA and MiCA (Regulation (EU) 2023/1114) are HELD; only NYDFS BitLicense (23 NYCRR Part 200) is not held, tracked as MEG-01 in the egress queue, WestLaw-gated). (Cross-references P6.x for domain-level shaping.)

### 2.15 Landing-page standards list: link each item to its authoritative source, MOVED to 2.25.2 (Series A) (maintainer-confirmed 2026-07-15, M, S-M) `[public]`

**Moved to 2.25.2** (Series A, international AI-governance authority coverage), which absorbs this landing-page standards-to-source linking as its surfacing step. The content lives there. This is a forward redirect stub; it closes when 2.25.2 closes.

### 2.21 Further AI-jurisdiction annexes (M, L; partly source-gated) `[public]`

**SPLIT THREE WAYS 2026-07-25.** (i) **Australia is STRUCK, not deferred**: the annex has existed
since #801 and the deferral text was written three days AFTER it merged. (ii) **BUILDABLE NOW, source
gate cleared**: US Texas (TRAIGA HB 149) and US Illinois (HB 3773, PA 103-0804) become ordinary P2
content work with held sources, no egress. (iii) The remaining jurisdictions stay source-gated, each named so the acquisition ask is concrete.

New AI-jurisdiction annexes, split by what is actually held. **Australia is STRUCK, not deferred:** [`ai/jurisdictions/annex-ai-australia.md`](ai/jurisdictions/annex-ai-australia.md) has existed since #801, so the deferral was wrong on arrival (the section text dates to #932, three days after the annex merged). **Source-gate CLEARED, annex not yet built:** US Texas (TRAIGA HB 149) and US Illinois (HB 3773, PA 103-0804), whose full-text primaries are held in the reference base and which #1116 cited in [`ai/policy-ai-compliance.md`](ai/policy-ai-compliance.md) section 7.5 with canonical-citations rows verified 2026-07-24; decide whether the section-7.5 coverage is sufficient or a dedicated annex is wanted, but do NOT re-run acquisition. **Held source, not yet adopted as a citation:** UK (AI Regulation White Paper 2023), Malaysia (National AI Governance and Ethics Guidelines 2024), and US federal (the OMB M-25-21 / M-25-22 / M-26-04 memoranda and the 2025 AI Action Plan) each have a held full text in the reference base but no canonical-citations row, so the gate for these is citation adoption rather than acquisition. Cross-references the P5.9 AI-jurisdiction-overlays umbrella. Re-homed from the retired AI-domain-delta umbrella (Workstream B.3).

### 2.23 CCPA statute (eff. 2026-01-01) currency + alignment review (maintainer-flagged 2026-07-16, M, S; cross-repo, blocked on ref ingestion) `[public]`

The maintainer added the CCPA statute version effective 2026-01-01 to `grc_library_ref` (`ingest/ccpa_statute_eff_20260101.pdf`, being ingested to `--full-text.md` by a worker as of 2026-07-16). Once the full-text is held, run a currency + alignment review of the corpus content that relies on CCPA/CPRA against the updated statute. Signals it is warranted: `privacy/jurisdictions/annex-privacy-united-states.md` currently characterizes California as "CCPA/CPRA (effective 2023-01-01)" (the CPRA operative date), while the added source is a 2026-01-01 version, so amendments may be unreflected; ~18-19 corpus files mention CCPA/CPRA, of which the reliance-bearing subset (~13, excluding glossary / jurisdiction-index / decision-tree passing mentions) is the review scope: the US annex, `register-automated-decision-making.md`, `procedure-data-subject-rights-management.md`, `framework-consent-management.md`, `framework-childrens-data.md`, `register-cookie-and-tracker.md`, and others. Method: OFFLOAD as a credit-offload order once the full-text lands (a `/reference-audit` new-ingest pass plus a currency/alignment check of the CCPA-citing docs against the held 2026-01-01 text); route findings (stale date, superseded provision, new obligation) to the backlog / a corpus-update PR, each verified against the held source. NOTE: the CPPA cybersecurity-audit REGULATIONS (Cal. Code Regs. tit. 11, the "Article 9" a CPRA cybersecurity audit engages) are a DIFFERENT instrument from this statute; confirm whether they are separately held before relying on an audit-requirement citation. No guessing what changed; the review reads the held full-text. **STATUS (2026-07-16): the REGULATIONS-alignment half is IN PROGRESS.** The `ccpa-regs-2026-alignment` worker delivery (a `/reference-audit` against the held final CCPA REGULATIONS, 11 CCR Div 6 Ch 1 eff 2026-01-01, which are a DISTINCT instrument from the statute) is being applied in per-domain slices, each with at-source re-verification + a skeptical verifier + confirmed upstream currency at the fetchable `cppa.ca.gov`: **slice 1 (#976)** updated the US privacy annex (ADMT/risk-assessment/cyber-audit final regs, corrected the audit/risk-assessment conflation + significant-decision scope), **slice 2 (this PR)** updated `register-automated-decision-making.md` (fixed the `1798.185(a)(16)`->`(a)(15)` statute-sub-paragraph citation error + added the CCPA ADMT opt-out/access/pre-use-notice/human-appeal subject rights). **slice 3 (#978)** updated `procedure-data-subject-rights-management.md` + `annex-privacy-jurisdiction-index.md` + `template-privacy-notice.md` (ADMT opt-out/access/pre-use-notice + the s.7021/s.7221(n) timelines), and **slice 4 (#979)** added the breadth citations to the four framework-alignment tables (`framework-consent-management` s.7004; `framework-childrens-data` ss.7070-7072; `register-cookie-and-tracker` ss.7025-7026; `template-dsar-workflow` s.7021/ss.7221-7222). **The CCPA REGULATIONS-alignment half is now COMPLETE** (primary carriers + breadth). **Separately still open:** the STATUTE-currency half this item was originally framed around (whether the corpus's "CCPA/CPRA effective 2023-01-01" characterization needs updating against the 2026-01-01 STATUTE version, and any superseded/added statutory provision) once the statute full-text is confirmed held; the regs-alignment slices do not close that. Full delivery findings persist on scratch (`results/ccpa-regs-2026-alignment.md`). **Precision follow-up (from #976's `/validate-pr` NOTE 1, non-blocking):** the US annex cyber-audit phasing sentence ties only the first tier to "2026 revenue" and gives the 2029/2030 dollar bands without their per-tier measurement years; the held 11 CCR §7121 (Timing Requirements) keys the 2029 deadline to 2027 revenue and the 2030 deadline to 2028 revenue (§7120 is the audit-requirement/threshold section). Deadlines and bands are all correct (accuracy is fine), so this is an optional precision tightening for the expert review: add the per-tier measurement years to `annex-privacy-united-states.md`. **APPLIED in #982** (annex v1.2.3: the 2029-04-01 tier now names 2027 revenue and the 2030-04-01 tier names 2028 revenue, re-verified against the held §7121 eff-2026-01-01). The statute-currency half of §2.23 remains separately open.

### 2.24 Governance Relationship and Flow Modelling Framework, MOVED to 2.25.1 (Series A) (2026-07-19, L) `[content]` `[public]`

**Moved to 2.25.1** (Series A, Governance traceability and coverage expansion): the content lives there. This is a forward redirect stub (the series-consolidation redirect-stub convention); it closes when 2.25.1 closes.

### 2.25 Governance traceability and coverage expansion (umbrella; maintainer-directed 2026-07-23, H, XL) `[content+machinery]` `[public]`

Umbrella for the corpus's control-to-authority traceability model and the coverage expansion that reaches corpus controls up to regulatory and international-policy authorities. Delivers its value independently of OSCAL (Series B, 2.26): every child ships as Markdown or as a generated relationship artefact, with no dependency on OSCAL adoption. Governing constraints from the flow-modelling framework (2.25.1) apply throughout: never conflate mapped, implemented, effective, and sufficient; never treat a reference as a requirement or adoption as compliance.

**Series members, in execution order:** 2.25.1 (relationship framework, the base), 2.25.2 (international AI-governance authorities), 2.25.3 (Canadian public-sector authorities), 2.25.4 (AI assurance and evaluation content), 2.25.5 (governance-maturity measurement model). Existing items consolidated in via a redirect stub: 2.24 into 2.25.1, 2.15 into 2.25.2, 2.22 into 2.25.3.

**Execution:** P2; authored now, executed after all P1 and P3 items are cleared; execute before Series B (2.26).

**Acceptance criteria:** every authority added by Series A is a resolvable node in the regenerated relationship model; all content ships as Markdown; `taxonomy.yml`, the portal, and the scorecard regenerate clean; every new authority is registered in the canonical citations register with edition and trust tier.

### 2.25.1 Graduate the Governance Relationship and Flow Modelling Framework to a generated model (consolidated from 2.24; H, L) `[content+machinery]` `[public]`

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

### 2.25.3 Canadian public-sector authority coverage (consolidated with 2.22; CANADA-PRIORITY, H, L) `[content]` `[public]`

**UN-DEFERRED 2026-07-25.** The 'deferred-blocked on currency' status was VOID: all 49 federal
sources are held and were downloaded within the previous two weeks. Now fully actionable. **Partition by
source cluster** (AI-governance / OSFI financial / ITSG-CCCS cyber / Privacy-Act-OPC-PIPEDA / provincial
FOI) and fan the research out to workers while the orchestrator authors. Sequenced after the tooling
catch-up. Absorbs item 2.22 (closed 2026-07-25), which closed as consolidated.

Canadian authority coverage. Consolidates 2.22 (a redirect stub is left there): systematically engage the 49 newly-held Canada.ca federal sources (TBS Directive on Automated Decision-Making, AIA tool and AI guides, OSFI B-13 and E-23, ITSG-33, CCCS ITSP.80.022, the GC cloud control profile, the Pan-Canadian Trust Framework, the Privacy Act, OPC, PIPEDA) across the Canada AI annex, the privacy annex, the matrix and per-doc framework-alignment tables, and the public-sector overlay. PLUS the provincial FOI and privacy gap not covered elsewhere: FIPPA, MFIPPA, FOIP. Ships as Markdown now; CANADA-PRIORITY preserved (government-facing, expert-reviewed, so a high accuracy bar: no fabricated codes, no unverified currency). Register each authority in the citations register; confirm each source is held before authoring. **Status carried from 2.22:** the Canada.ca apply is DEFERRED-BLOCKED on currency (canada.ca WAF-blocks automated re-fetch); the maintainer downloads fresh copies (request in `grc_library_private/maintainer-egress-requests.md`), then the per-domain apply proceeds.

**Depends on:** 1.22.9 (P1, direct canada.ca download URLs) and 3.42 (P3, Canadian captures); references them.

**Blocks:** none.

**Feeds:** 2.25.5; and across series 2.26.5.

### 2.25.4 AI assurance and evaluation content (H, L) `[content]` `[public]`

New `ai/` content for model evaluation, assurance arguments and safety cases, and post-deployment monitoring, using the held reference maps as inputs. Enterprise-assurance scope (assuring a deployed system), not frontier-risk. Ships as Markdown now. Confirm the reference sources are held before authoring.

**Depends on:** 3.14 (P3, ETSI Securing-AI map); references it as an input. (The ETSI TR 104 128 input, former 3.63, is complete: the held informative TR is engaged as a see-also across the `ai/` domain, the secondary see-also added to the AI security-and-risk standard's alignment table in PR #1122. The MITRE ATLAS 2026.06 map input, former 3.15, is complete: the corpus ATLAS citations were verified current against held 2026.06 and the one LLM02 fit finding applied, PR #1119.)

**Blocks:** none.

### 2.25.5 Governance-maturity measurement model (maintainer-directed 2026-07-23; M, M) `[content]` `[public]`

Evolve the existing maturity self-assessment template and the generated maturity scorecard into a structured, comparable measurement model whose inputs derive from the 2.25.1 relationship layer (authority coverage, mapped-versus-unmapped controls). Governed by the 2.25.1 anti-patterns: it reports MAPPED coverage only, and must not imply implemented, effective, or compliant.

**Depends on:** 2.25.1.

**Blocks:** none.

### 2.26.1 OSCAL adoption decision and model-scope lock (maintainer-directed 2026-07-23; H, S) `[machinery]` `[public]`

Bring the adopter-requested OSCAL feature to the maintainer for the adopt / do-not-adopt decision and, if adopted, lock the initial model scope. Models believed stable to target first: catalog (corpus controls) and profile (framework baselines and selections); the adopter-side models (component-definition, system-security-plan, assessment-plan, assessment-results, plan-of-action-and-milestones) are out of corpus scope. Output: a decision record plus, if adopted, the target OSCAL version captured in the canonical citations register (feeds gate 5).

**Depends on:** maintainer decisions (ASK at execution, do not guess).

**Blocks:** 2.26.2, 2.26.3, 2.26.4.

**Decision-gate:** OSCAL version; model set; whether a dedicated crosswalk / mapping model exists in the target release and should be used, or whether alignments are expressed as profile imports plus 2.25.1 relationship records.

### 2.26.2 OSCAL stable-identifier layer (S, M) `[machinery]` `[public]`

Add the immutable, per-document control-identifier layer OSCAL requires, on top of the stable doc-id scheme delivered by 3.75. Identifiers monotonic and never recycled, consistent with the gate-13 posture. This child is the OSCAL increment only; the base doc-id work stays in 3.75.

**Depends on:** 3.75 (P3, base stable doc-id) and 2.26.1.

**Blocks:** 2.26.4.

### 2.26.3 OSCAL metadata-field alignment (S, M) `[machinery]` `[public]`

Extend the 13-field metadata block and the `grc_library_ref` `doc_type` facet to carry the fields an OSCAL catalog / profile projection requires (control class, property namespaces, source-authority references). The metadata block stays canonical; OSCAL fields derive from it. OSCAL increment only; the base facet work stays in 3.54.

**Depends on:** 3.54 (P3, base `doc_type` facet) and 2.26.1.

**Blocks:** 2.26.4.

### 2.26.4 OSCAL catalog pilot: one domain, generated, gated (maintainer-directed 2026-07-23; M, XL) `[machinery]` `[public]`

Generate an OSCAL catalog for a single domain from Markdown source, non-authoritative, alongside the existing generated indexes. Add a gate validating the generated OSCAL against the OSCAL schema and against the stable control-ids from 2.26.2 (a `--check` mode, registered with gate 35, passing gate 71).

**Depends on:** 2.26.1, 2.26.2, 2.26.3.

**Blocks:** 2.26.5.

**Decision-gate:** which domain seeds the pilot (security or ai); whether OSCAL schema validation is achievable stdlib-only, or whether to grant a dependency exception. The stdlib-only exception would break audit-programme design principles, so it is a maintainer decision, not an orchestrator one; ASK, do not add a dependency silently.

### 2.26.5 OSCAL profiles and crosswalks for framework alignments (M, L) `[machinery]` `[public]`

Express the existing ISO, NIST, CSA, and COBIT alignment tables as OSCAL profiles (and a crosswalk representation per the 2.26.1 decision), generated from the current mapping matrices. Reuse the framework-citation hallucination audit (gate 5) so every control code in a generated crosswalk is a real identifier in the framework it names.

**Depends on:** 2.25.1 (Series A relationship model) and 2.26.4.

**Blocks:** none (terminal).

### 2.28 AI jurisdiction annex + ref ingest: Singapore Model AI Governance Framework for Agentic AI (M, M) `[content]` `[public]`

Surfaced 2026-07-24 during the §2.19 Singapore GenAI annex build: IMDA and the AI Verify Foundation released a separate, newer Model AI Governance Framework for Agentic AI (unveiled January 2026), a DISTINCT framework rather than a new edition of the GenAI Framework, so §2.19's citation stands. Follow-up: ingest the Agentic AI MGF into `grc_library_ref` as a held primary (confirm currency upstream at ingest), then add a companion jurisdiction annex or fold it into [`ai/standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md), per the maintainer's scope call.

### 2.18 AI jurisdiction annex: South Korea AI Basic Act (H, M) `[public]`

New jurisdiction annex for the South Korea AI Basic Act (held primary). `[VERIFY]` the phased effective dates upstream at apply (the catalogue records effective 22 Jan 2026; egress-gated). A government-facing annex, high-assurance harness. Re-homed from the retired AI-domain-delta umbrella (Workstream B.1).

### 2.25.2 Control-to-policy-instrument coverage: international AI-governance authorities (consolidated with 2.15; M, M) `[content]` `[public]`

New authority coverage for the OECD AI Principles, the UNESCO Recommendation on the Ethics of AI, the G7 Hiroshima Process Code of Conduct, and the Council of Europe Framework Convention on AI, so each becomes a mappable external authority in the 2.25.1 relationship model. Ships as Markdown now. Consolidates 2.15 (a redirect stub is left there) as the surfacing step: the landing-page "Standards and frameworks it maps to" list links each item to its authoritative source (freely-available sources to the primary document or official landing page; licensed sources to the official catalogue / abstract page, never hosting or bypassing paywalled text), sourced from [`grc_library_ref`](../grc_library_ref) `catalogue.yml` and confirmed current at build. Register each instrument in the canonical citations register with edition and trust tier; once they land, move them on the for-ai resource index from "named, not yet covered" to covered. **[VERIFY]** the Council of Europe convention's signature and ratification status, and each instrument's current edition, upstream at apply (egress-gated; currency-material).

**Depends on:** none (content).

**Blocks:** none.

**Feeds:** 2.25.1; and across series 2.26.5.

### 2.26 OSCAL machine-readable representation (umbrella; maintainer-directed 2026-07-23, H, XL) `[machinery]` `[public]`

Umbrella for adopting NIST OSCAL as an open, machine-readable projection of the corpus. Markdown remains the single source of truth; every OSCAL artefact is generated and non-authoritative, in the manner of `taxonomy.yml`, and is never hand-edited (artefact-and-branch-discipline applies). OSCAL adoption is an adopter-requested feature for the maintainer's consideration, NOT a settled decision; the go / no-go is a maintainer decision brought forward at 2.26.1. Depends on Series A (2.25): it serializes A's relationship model (2.25.1) and maps the authorities A adds; Series A never depends on Series B.

**Series members, in execution order:** 2.26.1 (adopt-decision and model-scope lock), 2.26.2 (stable-id layer), 2.26.3 (metadata alignment), 2.26.4 (catalog pilot), 2.26.5 (profiles and crosswalks).

**Execution:** P2; authored now, executed after all P1 and P3 items are cleared and after Series A.

**Acceptance criteria:** the OSCAL adoption decision is recorded; the pilot catalog generates from Markdown and validates against the OSCAL schema in CI; OSCAL control-ids reconcile with corpus control-ids; profiles and crosswalks generate and pass the framework-citation audit (gate 5); all gates run stdlib-only or under an approved exception.

**[VERIFY]** the current OSCAL release line and model set at NIST before 2.26.1 (egress-gated); do not pin a version in prose until confirmed and recorded in the canonical citations register.

### 3.174 Joint-controller Art 26(1) informed-not-prescribed reword (Parts 1-2 GDPR-clock + PR.AA-title fixed #1259; Part 3 routed to maintainer) (2026-07-28 deep-assessment c5, codex, W, XS) `[public]`
Parts 1-2 FIXED in #1259 (held-source-verified): GDPR clock `:175` "from confirmation"->"after becoming aware" (Art 33(1)); PR.AA title `matrix-reverse:92` untruncated (CSF 2.0). REMAINS (routed to maintainer, pending-decisions): Part 3, `privacy/template-joint-controller-arrangement.md:91` (NOT :109; line drifted) - the allocation heuristic reads as prescribed by Art 26(1) which only requires transparent determination; proposed value-retaining reword awaits maintainer confirm (rewords authored design prose).

### 3.184 Corpus ISO citation currency updates enabled by the 2026-07-28 `_ref` ingest (2026-07-28 ingest follow-up, M, S) `[public]`
The 2026-07-28 `_ref` egress ingest (PR #105) now holds newer editions the corpus cites at older ones: update `ISO/IEC 27017:2015` citations to `:2026` (second edition supersedes; the corpus cites 2015 across the cloud-security docs and the matrices); update `ISO 19011:2018` citations to `:2026` (fourth edition); and resolve the `ISO/IEC 29134` `:2017`-vs-`:2023` inconsistency to `:2023` (held second edition). Verify each attributed value against the newly-held text (the 27017:2026 control set changed with the ISO/IEC 27002-based restructure, so a mapping review is warranted, not just a version-string bump).

## Priority 3 — Clean up and tooling

### 3.180 Adopter-facing skills hard-require the private siblings with no degrade branch (2026-07-28 deep-assessment c6, claude, M, S) `[public]`

`deep-assessment/SKILL.md` and `reference-audit/SKILL.md` require all three private siblings / the full suite to exit 0 before any semantic phase, with no absent/skip/not-applicable branch, so an adopter stalls at an unsatisfiable phase-1 precondition. Add an adopter degrade path.

### 3.181 The adopter on-ramp never mentions `/adopt`, siblings, or `.working` (2026-07-28 deep-assessment c6, both families, M, S) `[public]`

No public adopter doc (`docs/adopter-guide.md`, `docs/template-quickstart.md`, `CONTRIBUTING.md`) mentions `/adopt`, `adopt-config`, the siblings, or `.working`, so an adopter can complete the entire documented on-ramp and then work on top of the maintainer's queue/handoff/QA registers. Surface `/adopt` in the on-ramp.

### 3.183 Adopter-facing polish (changelog audience, fork-hook source edit, alarming clean-run output, closed-set framing) (2026-07-28 deep-assessment c6, claude, L, S) `[public]`

The changelog top entries are maintainer jargon with no adopter banner; the adopter guide tells the adopter to edit `tools/lint_common.py` `DEFAULT_EXEMPT_DIRS` (a source edit that conflicts on every upstream pull); a clean adopter clone prints `ERROR: could not locate the grc_library_ref index` twice; and "five paths"/"seven areas" are framed as complete against 12 `docs/` files / 11 domain dirs. Low-severity adopter-experience cleanups.

### 3.14 ETSI Securing-AI alignment map (L, M) (was 3.16) `[public]`

Map the held ETSI SAI family (EN 304 223 plus the GR/TR set) against the corpus `ai/` security content: which requirements have no corpus carrier, which corpus claims an ETSI citation would strengthen, and a proposed alignment shape (options for maintainer scoping). Research DELIVERED (`inbox/worker-20260703-a/etsi-sai-alignment-research/`, 2026-07-04); the apply is a later decision. Citation form UNBLOCKED 2026-07-04 (the maintainer-supplied fresh EN 304 223 V2.1.1 copy; scratch PR #100).

### 3.47 TODO adoptability: strip internal working-provenance annotations (S) `[public]`

TODO items carry internal working-provenance that an adopter reading the backlog does not need and that clutters the file: date-stamped `maintainer-directed YYYY-MM-DD` tags, `Surfaced ... during #N` and `Mined ... (sweep N ...)` origin lines, PR-number and sweep-lineage annotations, and residual `(was X.Y)` renumber breadcrumbs. This provenance lives durably in git history, the DONE ledger, and the CHANGELOG; the forward-looking TODO should read as a clean, adoptable backlog of what remains. Sweep the open items to remove these annotations, keeping the actionable content, the stable id in each heading, and the `(severity, effort)` tag. Standing convention going forward: new TODO items omit date, PR, sweep, and maintainer-directed provenance. **SCOPE RESOLVED 2026-07-15 (maintainer):** strip only the date / `Surfaced #N` / `Mined (sweep N)` / PR-number / maintainer-directed provenance, and KEEP the `(was X.Y)` renumber breadcrumbs (per the #929 convention that "existing breadcrumbs stay for resolvability"). Still attended-preferred, not an unattended sweep: a ~85-item single-file editorial pass over the most cross-referenced working file with weak mechanical verification that each item's actionable content survives intact, so it wants fresh-context per-item care. Queued for an attended/fresh session.

### 3.197 Portal is blind to Adoption Disposition (3.179 part 3 follow-up) (2026-07-31, deep-assessment c6 / 3.179 spin-off, M, M) `[public]`

The generated portal ([`docs/portal.md`](docs/portal.md)) does not surface each document's Adoption Disposition (library-internal / template / adopter-facing), so an adopter cannot see at the portal which documents to fork vs keep-as-reference vs delete. Surfaced by the 3.179 research (#1297). Adoption Disposition is NOT one of the 13 per-document metadata fields; it lives only as a column the register (`governance/register-document-index-and-classification.md`) maintains. Two paths: (a) add a 14th per-document metadata field across ~312 docs + update `build-taxonomy.py`/`build-portal.py`/`lint-metadata.py` (a corpus-wide schema migration that creates a second disposition source-of-truth to keep in sync with the register, the exact drift this class is about); (b, lean) have `build-portal.py` parse the register table directly into a path->disposition lookup and tag each portal entry (lighter, but a new markdown-table parser + join + output-format change). A genuine generator feature, deliberately split out of 3.179 to keep that HIGH/S routing fix small.

### 3.198 Pack README directory-tree annotation promotes the single-file `CLAUDE.md` install (2026-07-31, deep-assessment c6 / 3.196 spin-off, dual-family vpr #1300 codex, S, S) `[public]`

The pack README [`dev-security/claude-rules/README.md`](dev-security/claude-rules/README.md):92 directory-tree annotation says the root `CLAUDE.md` is dragged into a project "for full coverage", the single-file-install defect class (#1296/#1300) surviving in the pack README's own tree and contradicting its Option 1 (:169-180, which correctly requires the whole-directory copy plus `@`-mention). Reword the annotation to point to Option 1. Pack surface, so it needs a pack Version bump (1.66.10 to 1.66.11) + a `## Version history` row (D6), which is why it was routed out of the corpus-scoped #1300 rather than bundled. Found by the dual-family `/validate-pr` on #1300 (codex corpus-wide carrier sweep).

## Priority 4 — Adopter experience

**Next item number: 4.32.**

Capability and guidance for organizations adopting the library, and the operator-experience tooling for running the project. Scheduled deliberately, after the fix/gap/cleanup tiers.

### 4.1 Corpus-management discipline as a shareable skill (M, XL) `[public]`

Package the cumulative documentation-and-corpus discipline as a standalone Claude Code skill anyone managing a documentation corpus with an AI assistant could install. Distillation source: the fifteen `governance/` pack rules (discipline core), `validation-sweep` + `library-fitness-review` (periodic-review surface), the audit-programme architecture (mechanical-enforcement surface). Decided 2026-06-22: skill **family** (not omnibus), **prescriptive-only** (no linter scaffolds), **existing pack 1.x bump**. After the FR backlog closes. UNBLOCKED: the pack adoption-hygiene programme is complete (phases 1-4, closed #846), so the distillation source (the condensed, adoption-clean governance rules) is merged and available.

### 4.5 Adopter reference-base specification: build-your-own-ref guide, source lists, and the corpus-to-sources relevance map (L, L) `[public]`

Adopters who clone the library do **not** receive `grc_library_ref` (it holds third-party reference works under their own licences and is not redistributable). Give them something better than a bare "good luck": a **specification an adopter's AI assistant can follow to assemble its own reference base**, right-sized to that organization's budget and licences. Deliverables to scope at build:

1. **The build-your-own-ref specification** (the centrepiece): a document written for an adopter's AI to execute, laying out the trust-bucketed tree and catalogue convention mirroring `grc_library_ref` (`standards/` trusted, `frameworks/` trusted-catalogue, `legislation/` version-sensitive, `publications/` screen-first, an `ingest/` staging area), and the ingest workflow (obtain from the authoritative source, extract to AI-readable text, catalogue, validate). It teaches the adopter's AI to reproduce the base, not just describes it.
2. **The public-source list**: every freely and authoritatively obtainable source the corpus cites (NIST publications, ETSI standards, OWASP, MITRE ATT&CK / ATLAS, CSA CCM / AICM, EU legislation via EUR-Lex, national legislation registers, EDPB guidelines, and the rest), each with where to get it from its primary source, so the adopter's AI can fetch and ingest the free tier with no budget at all.
3. **The suggested paid-source list**: the licensed sources worth adding **if the adopter or their organization has the budget** (the ISO/IEC catalogue, PCI SSC documents, and other paywalled standards), each with a one-line note on what coverage it strengthens, so an organization can make an informed spend decision rather than discovering the gap later.
4. **The corpus-to-sources relevance map (the reason this is worth trusting)**: surface, as a first-class adopter-facing artefact, *which* standards, legislation, frameworks, and other documents are relevant to *each* corpus document. A core reason the project maintains its own reference base is exactly this: the work of mapping every corpus file to the authoritative sources that bear on it is already done, and that mapping is kept honest by the citation, currency, and semantic-fit gates plus the `/reference-audit`, `/matrix-fit`, and `/claim-fit` cadences. An adopter who trusts that curation (as they reasonably can) inherits the relevance map for free and never has to rediscover, for each of their documents, which sources matter, the single most tedious and error-prone part of standing up a governance reference base.
5. **Helper scripts + wiring notes**: scaffold the tree, fetch-from-reputable-source where a licence and stable URL permit, extract text for AI-readability, build/refresh the catalogue; and notes on how a fork's base feeds the in-repo validator modules the citation and control-code gates build on, and `/matrix-fit`.

Never bypass paywalls or licensing; treat downloaded `publications/` as untrusted until screened. Low urgency; adopter-experience tier. (Broadened 2026-07-13 from the original fork-facing-scripts framing to lead with the AI-buildable spec, the public/paid source lists, and the corpus-to-sources relevance map as the headline value.)

### 4.6 Fork update-assessment tooling (upstream-change applicability report) (S-f, maintainer-requested 2026-07-04, M-L) `[public]`

When an adopter's customized fork pulls upstream `grc_library` updates, nothing today helps THEIR AI assistant assess each upstream change against the fork's local customizations and present an accept/adapt/skip decision matrix. Design a fork-side instrument: likely a shareable skill (diff upstream release-to-release, classify each change by carrier class, map against the fork's recorded local divergences, produce the per-change report), plus upstream-side enablers where cheap (machine-readable change-class tags or per-entry applicability hints). Shape and upstream-vs-fork-side split are maintainer-scoped at design time.

---

### 4.29 `/adopt` adjustment + non-destructive tooling-update mode (maintainer-directed 2026-07-19, L) `[machinery]` `[public]`

Extend the [`/adopt`](.claude/commands/adopt.md) skill (currently a run-once fork-onboarding flow that writes `.claude/adopt-config.json`) with an **adjustment/update mode** (a re-run flag) so an adopter fork can, at any time after the initial adoption: (1) **change earlier `/adopt` choices** (sibling model, ref/private/scratch wiring, which optional capabilities are on) by re-reading and rewriting the adopt-config rather than starting over; and (2) **pull updated TOOLING from a newer `grc_library` origin (the `tools/` audit toolchain, the `dev-security/claude-rules/` pack, the `.claude/` hooks/commands, the gate wiring) WITHOUT clobbering the adopter's own edited CORPUS files**, applying the update **non-destructively and reversibly** (a dry-run/preview of exactly what changes, a clean separation of upstream-owned tooling from adopter-owned content, a backup or git-checkpoint so any apply can be rolled back, and a conflict surface where an adopter has locally edited a tooling file). The driving goal (maintainer 2026-07-19): every piece of tooling that brings value, INCLUDING the operational instruments that currently live maintainer-side (the degradation-watch log and its threshold/validation discipline, the credit-offload design, the session-lifecycle machinery, the QA cadences), should either ship as adopter-usable guidance or be clearly documented as maintainer-only, and `/adopt` should let an adopter opt into and benefit from the ones that are portable, applied safely to their own project. Design questions to resolve at build time: the upstream-vs-adopter file ownership manifest (which paths are tooling the updater may overwrite vs corpus the updater must never touch); the reversibility mechanism (git checkpoint branch vs backup dir); how a locally-customized tooling file is reconciled (three-way merge, or surface-and-defer); and how the portable operational instruments are surfaced to the adopter (the `.private` placeholder path is the natural home). Related to but broader than §4.6 (which is the upstream-change applicability *report*); §4.29 is the *apply/adjust* mechanism that report feeds. Scheduled with the adopter-experience tier.

### 4.30 Full adopter-experience assessment + `.adopt/` adoption kit (maintainer-directed 2026-07-19, P4 umbrella, M-L, multi-phase) `[public]`

The umbrella for a clean, great adopter experience from a public clone, and for moving maintainer back-end state out of the public repo WITHOUT depriving an adopter who wants it. **Phase 1 (assessment):** from a clean PUBLIC clone, enumerate every adopter-facing process (`/resume`, `/adopt`, the audit gates, the PR workflow, the QA cadences, the skills, the CLAUDE.md rules) and trace what each reads; flag every reference to something that lives in `_private` / `_ref` / `_scratch` (a gap for the adopter); classify each gap as (a) ESSENTIAL machinery-core the adopter's gates or `/resume` need (recreate for them), (b) OPTIONAL back-end capability the adopter might want (offer as per-adopter opt-in; the orchestrator-only files MAY be adopter-useful, maintainer-directed 2026-07-19, so it is the adopter's decision, not ours), or (c) MAINTAINER-PRIVATE (the process degrades gracefully, no adopter reference). **Phase 2 (the `.adopt/` kit):** a root `.adopt/` directory with a README (the decision guide: in-repo `.ref`/`.scratch`/`.private` stubs vs separate sibling repos; how `/adopt` works; how to decide; which back-end capabilities to opt into) and clean TEMPLATES for every essential machinery-core file that moves out (baselines `/adopt` CREATES in the adopter's chosen location, since they no longer ship publicly) PLUS opt-in templates for the back-end capabilities. **Phase 3 (adaptation):** move DONE + improvement-log (confirmed 2026-07-19) and any other assessed-essential file to `_private`; adapt the gates that read them (`check-todo-rotation-on-pr`, `lint-todo-marked-done`, gate 50 bookkeeping-parity, the tension/residual scans) to RESOLVE `_private`-or-adopter-location (the `resolve_sibling` pattern); ensure every adopter-facing process degrades gracefully when an opted-out file is absent; `/adopt` recreates from the `.adopt/` templates. **Coordinates / folds in the existing adoption items** (Phase 1 decides which fully merge vs stay separate): §4.1 (corpus-management shareable skill), §4.5 (adopter reference-base spec + build-your-own-ref guide, likely the `_ref` template piece of the kit), §4.6 (fork update-assessment tooling), §4.9 (pack public-distribution packaging, implemented in #1145: escaping links rewritten, dependencies documented, command names verified), §4.29 (`/adopt` adjustment + non-destructive tooling-update mode, the closest sub-item). **Build notes:** `.adopt/` is a real deliverable, not a gate-70 placeholder stub; check its README against the language + marker-word gates; pairs with the `/home/grc` migration and the `_private` relocation (design in `grc_library_private/design-decisions.md`). **Goal:** clone public, run `/adopt`, get a complete clean working-state set in the chosen location, with per-adopter opt-in to the back-end and zero orchestrator-only clutter.

### 4.31 Publish the governance pack as a standalone methodology (maintainer-directed 2026-07-23; M, M) `[content]` `[public]`

Publish the `dev-security/claude-rules` pack as a citable, CC BY-SA methodology or reference model: the failure-mode provenance, the enforcement mechanism, the results. Adopter-experience work, hence Priority 4, separate from the P2 series and independent of the OSCAL machinery.

**Depends on:** the Task-1 pack reconciliation (completed 2026-07-23, so the published pack is current), 3.47 (P3, strip internal working-provenance for adoptability), 3.56 (P3), and 1.19 (P1, operational-state privatization and adopter-clone portability, the adoptability work that makes the pack project-agnostic).

**Blocks:** none.

**Alignment:** this is the publication step for the pack updated in Task 1 (the reconciliation completed 2026-07-23); keep it cross-referenced to that work.

## Priority 5 — Expand: country / regulator / programme overlays

**Next item number: 5.10.**

Adding new coverage to existing domains. Each subitem is a separate small or medium PR; the maintainer schedules deliberately.

### 5.2 Logistics country / programme expansion (was 5.1) `[public]`

The WCO AEO Compendium identifies ~94 trusted-trader programmes globally; the library covers 4 (BASC, CTPAT-US, AEO-UK, PIP-Canada). Highest-priority additions: EU AEO (27 member states under EU UCC Art 38), Mexico NEEC / OEA, Australia Trusted Trader, Singapore STP / STP-Plus, Japan AEO, Korea AEO, New Zealand SES, Brazil OEA, China AEO.

### 5.3 Financial-services country regulator overlays (was 5.2) `[public]`

Within `compliance/financial-services/`: UK PRA / FCA; US OCC / FRB / FDIC / SEC / FINRA; Canada OSFI; Australia APRA; Singapore MAS; Japan FSA.

### 5.4 Healthcare country regulator overlays (was 5.3) `[public]`

Within `compliance/healthcare/`: EU MDR / IVDR (full text now held in the reference base); Canada PHIPA and provincial frameworks; Australia My Health Records Act; UK NHS DSPT. The remaining bullets stay source-gated except EU MDR/IVDR, which is a delicate build queued for a fresh session's context.

### 5.5 Energy and utilities country regulator overlays (was 5.4) `[public]`

Within `compliance/energy-and-utilities/`: US NERC CIP standards; US TSA pipeline cybersecurity directives; UK Ofgem cyber requirements; EU ENISA sectoral guidance.

### 5.6 Telecommunications country regulator overlays (was 5.5) `[public]`

Within `compliance/telecommunications/`: EU EECC; UK Ofcom telecom security framework; US FCC regulations; Australia ACMA requirements.

### 5.7 Public-sector country / regulator overlays (was 5.6) `[public]`

Within `compliance/public-sector/`: UK Government Cyber Security Strategy and GovAssure; Australia ISM and PSPF; Canada IT Standards for federal departments. The other bullets stay source-gated.

### 5.8 Privacy jurisdiction gaps (was 5.7) `[public]`

Existing privacy domain covers 26 country annexes. Known gaps or stale entries: Argentina (PDPA 2025 update pending); Saudi Arabia PDPL (recent updates pending); re-review of EU member-state derogations where applicable. The Argentina and Saudi bullets stay source-gated.

### 5.9 AI jurisdiction overlays (was 5.8) `[public]`

The `ai/jurisdictions/` subdirectory and its first annexes (EU AI Act #743, Colorado #749) shipped under the former FR-62. Remaining candidates, source-gated pending maintainer drops: UK AI policy framework; China generative AI rules; Korea AI framework. (Two candidates are STRUCK, not open gaps: Canada AIDA, covered by `ai/jurisdictions/annex-ai-canada.md` which correctly treats AIDA as lapsed (re-confirmed dead upstream 2026-07-24 by the research-canada-aida-status pass); and NYC bias audit law, covered in full by `ai/jurisdictions/annex-ai-us-new-york-city.md` (NYC Local Law 144 of 2021, the AEDT bias-audit law), with the implementing DCWP final rule (6 RCNY 5-300 to 5-304) held in the reference base and currency confirmed 2026-07-24 by the research-nyc-ll144-reconciliation pass. The §5.9 candidate-list reconciliation those passes prompted is now done for Canada and NYC; the three remaining candidates above stay source-gated pending maintainer drops.)

---

## Priority 6 — Expand: new domains

**Next item number: 6.6.**

Entirely new domains, multi-week scope each. The maintainer schedules deliberately. Ordered lowest-effort-first.

### 6.1 Identity-specific content depth (L) (was 6.2) `[public]`

Customer Identity (CIAM) governance, workforce identity governance, identity federation patterns, passwordless adoption playbooks. Scoping research DELIVERED, with three proposed documents briefed as follow-on work-units in scratch (`research/ciam-governance-research/`, `research/identity-federation-patterns-research/`, `research/passwordless-adoption-research/`, grounded in held NIST SP 800-63-4); the BUILD stays maintainer-schedule-gated.

### 6.2 Quantum cryptography readiness deepening (L) (was 6.3) `[public]`

The phase-level PQC roadmap exists. #1129 delivered the core content deepening (verified against the now-held FIPS full-text): NIST parameter-set to security-category mappings (ML-KEM / ML-DSA / SLH-DSA) with a category-3 interoperability baseline, a crypto-agility section (primitives as configuration, not hardcoded), ML-DSA-vs-SLH-DSA selection guidance, and the FIPS-205 citation currency, echoed in the encryption-policy PQC row and the crypto pack rule. The former source-gate is CLEARED: FIPS 203/204/205 are held in grc_library_ref and were confirmed current in #1129 (2024-08-13 finals, verified upstream). RESIDUAL (still L, now build-ready since the source-gate cleared): a dedicated PQC migration playbook (step-level how-to beyond the roadmap's phase plan) and post-quantum-ready CA/PKI implementation content. Corpus-internal scoping DELIVERED (`inbox/worker-20260703-a/quantum-pqc-readiness-scoping/`).

### 6.3 Cross-framework matrix expansion (L) (was 6.4) `[public]`

Expand [`governance/matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md) to additional sectoral and regional frameworks as the P5 content grows.

### 6.4 CMMI capability levels alongside maturity levels (L) (was 6.5) `[public]`

Low priority, after the FR backlog. Add a capability-level scheme (0-3 per practice area) alongside the 5-tier maturity levels: update [`governance/framework-governance-performance-and-improvement.md`](governance/framework-governance-performance-and-improvement.md) §2, [`docs/template-maturity-self-assessment.md`](docs/template-maturity-self-assessment.md), possibly the DTI thresholds. Research-only integration mapping DELIVERED (`inbox/worker-20260703-a/cmmi-sei-maturity-integration/`, four integration-shape options).

### 6.5 Multi-cloud governance overlay (XL) (was 6.1) `[public]`

Per-cloud hardening baselines for AWS/Azure/GCP exist; the gap is multi-cloud governance (cross-cloud risk taxonomy, cross-cloud incident coordination, portfolio-level controls). Could live in `operations/` or a new `cloud/` domain. Scoping DELIVERED (`inbox/worker-20260703-a/multi-cloud-governance-scoping/`).

---

## Priority 7 — Awaiting maintainer decision

**Next item number: 7.6.**

### 7.2 Per-regulation context (FR-104) `[public]`

Per-regulation context not pursued (dropped-decision audit-trail record; see `grc_library_private/design-decisions.md`).

### 7.3 Portal reorder (FR-130) `[public]`

Portal reorder not pursued (README stays at decision-tree item 1; dropped-decision audit-trail record).

---

## Time-bounded follow-ups

Non-urgent follow-ups deliberately DEFERRED to a future date, then re-evaluated: a suggested revisit of something already shipped, where acting now would be premature (not enough real-world signal yet). This is NOT the normal forward backlog (those are the Priority sections); an item here is date-gated, not ready-now, and will mostly track "revisit this suggested follow-up after date X". Each entry carries a **Not-before** date (UTC), what to EVALUATE, and the originating PR. `/resume` reads this section and surfaces any entry whose Not-before date has passed, so a due follow-up is not silently forgotten. When a follow-up is acted on (or decided against), rotate it to `grc_library_private/.working/DONE.md` like any other closed item.

**Next item number: TF-4.**

- **TF-3 / Not-before: 2026-09-01** (recurring MONTHLY): run `python3 tools/check-clean-language-upstream.py`. If it reports DRIFT, re-vendor the changed `.claude/skills/clean-language/` files from upstream `jposluns/ai-language` (`gh api repos/jposluns/ai-language/contents/clean-language/<file> --jq .content | base64 -d > .claude/skills/clean-language/<file>`) and commit, updating the skill's PROVENANCE.md. Then advance this Not-before by one month (this is a RECURRING check, so it does NOT rotate to DONE; it re-arms). Originating PR: #1328 (P-1.13, the Clean-Language skill install + auto-update check, maintainer-directed 2026-08-01).

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
- When an item is completed, delete it (no strikethroughs, no `[done]` suffixes) and add a `grc_library_private/.working/DONE.md` entry in the same PR. Rotation discipline: the PR-finalization-protocol section of [`.claude/rules/governance/change-tracking.md`](.claude/rules/governance/change-tracking.md).
- Design decisions belong in `grc_library_private/design-decisions.md`, not TODO.
- This file is the source of truth for what's queued; conversation history is not.
- Fitness-review backlogs remain the authoritative per-finding evidence source; this file is the action-organized view.
