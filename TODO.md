# TODO

Forward-looking backlog of planned enhancements for the GRC Documentation Library. Items are added when identified and rotated out when completed. Completed items move to [`.working/DONE.md`](.working/DONE.md) (closed-TODO ledger, keyed by original backlog ID); historical change detail lives in [`CHANGELOG.md`](CHANGELOG.md). This file holds only pending and queued items.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions, with one narrow exception: [`tools/lint-todo-staleness.py`](tools/lint-todo-staleness.py) (gate 45) scans this file for the queued-PR-already-merged drift shape (its companion sweep-cursor-behind-history check reads the resume cursor from [`.working/session-handoff.md`](.working/session-handoff.md)). The intra-document section-reference gate also scans it. Other audit gates skip this file.

**How items are numbered and formatted.** Items are grouped by priority (P1-P7), tiered by work type (maintainer's 2026-06-30 leaning): P1 fix errors and prevent recurrence, P2 fill significant gaps, P3 clean up and tooling, P4 adopter experience, P5-P6 expand the corpus (overlays, then new domains), P7 awaiting decision. **Every item is a `### N.M` subsection whose leading digit is its priority** (so a P3 item is `3.x`); within a section items run lowest-effort-first. The `N.M` number is a position, not a permanent id, so it changes if an item is re-tiered or resequenced; the **stable id is the `FR-N` / descriptive identifier in the heading**, and a `(was X.Y)` tag preserves the prior number for one cycle so older references (CHANGELOG, handoff, retro log, tool docstrings) stay resolvable. Each heading carries `(id, severity, effort)` where severity is `H[critical]` / `H` / `M` / `L` / `FYI` and effort is `XS` / `S` / `M` / `L` / `XL` (scale in 3.4). A `⚠` marks a persona-quoted finding to verify at action time.

---

## Queueing rules

- Orchestrator picks the next batch from **Priority 1 first, then Priority 2**, in highest-severity order; within a chosen section the effort ordering helps assemble like-effort batches.
- **1-8 PRs per batch** (logical grouping); `/validate` after each batch.
- Maintainer direction supersedes the orchestrator's pick at any time.
- Lower priorities (P3-P7) are picked deliberately, not from the routine batch queue, unless the maintainer triggers them.
- **Maintainer-directed running order (2026-06-30 work-type re-tier)**: work the tiers in order. **P1** first (the cheap fix/prevent items: FR-48 and the §1.4 / §1.5 integrity tooling); then **P2** gaps (FR-59 and FR-60 deepenings and the deepen-baselines cluster first, then **FR-70**, the XL crypto-asset domain, last); then **P3** clean-up-and-tooling; then **P4** adopter experience. **P5 / P6 expansion waits** (maintainer: expansion can wait). The standing **fix-issues-first** directive (2026-06-27) governs within each tier, and the routine `/validate`, `/validate-pr`, and `/matrix-fit` cadences are the reactive half of P1. FR-167, the NIST SP 800 ingestion, and the OT post-ingestion validation are COMPLETE (2026-06-30; ingestion in `grc_library_scratch`, validation in #495).
- **Integrity-tooling items** (the former "guard-rails phase"): the citation-precision gate (§1.4 S3) and the reference version-currency residuals (§1.5) live in **P1** (fix errors and prevent recurrence); the QA-cadence and TODO/DONE-rotation surfaces are already covered by the bookkeeping-parity gate family (gates 50 and 57, plus the D5 PR-time check), and the retro guard rails (the former retro-log consolidation item) closed across #510 (the new-skill-drafting checklist) and #511 (the word-form count gate). Research fan-out (workers produce verified research from [`.working/worker-brief-template.md`](.working/worker-brief-template.md); the orchestrator re-verifies every claim at apply-time and authors all final prose) is the standing method for partitionable batches.

---

## Priority 1 — Fix errors and prevent recurrence

Correctness fixes and the **error-prevention tooling** that keeps the corpus from regressing. The routine `/validate`, `/validate-pr`, and `/matrix-fit` cadences are the reactive half of this tier; the items below are the standing preventive half.

### 1.1 H2 numbering-pattern drift, entangled residual (FR-48, M, L)

Policy and standard documents used three H2 numbering patterns (fully-numbered `## N.`, fully-unnumbered `## Title`, and `## Section N:` labels). Maintainer decision 2026-07-01: normalize to **fully-numbered** (`## N.` H2 + hierarchical `### N.M` H3), taking the **safe subset first and deferring the entangled docs**. The safe subset (28 docs with no inbound `§N`/"Section N" citation, no anchor link, no intra-doc section self-reference, and no inline prose clause numbering coupled to the headings) was normalized via deterministic scripted apply + re-parse in this PR. **Residual (deferred, this item):** the 13 remaining entangled docs (of the originally-deferred 38; 25 renumbered through #548) whose sections ARE cited elsewhere, self-referenced, or coupled to inline clause numbers and would require a lockstep citation/clause remap (the full enumerated set, with each doc's entanglement reason, is the worklist in [`.working/fr48-deferred-worklist.md`](.working/fr48-deferred-worklist.md)), across four reference forms: (a) `§N`/`§N.M` subsection citations, markdown-link or bare-parenthetical (e.g. `policy-exception-and-risk-acceptance-management`, `standard-enterprise-risk-management`, `standard-logging-and-monitoring`, `policy-compliance-and-audit-management` cited `§4.3` by `procedure-capa.md`); (b) "Section N" prose citations (e.g. `standard-mobile-application-security`, which was cited by 6 `dev-security/claude-rules/languages/*.md` pack files plus the pack `README.md` (7 pack files total), all renumbered in #548; done); (c) intra-doc "Section N" self-references (`architecture/standard-technology-radar` and `architecture/standard-integration-architecture` were this class; both done, so the open set is classes (a), (b), and (d)); (d) inline prose clause numbering keyed to the old headings (`policy-compliance-and-audit-management`, `policy-legal-and-regulatory-compliance`, `policy-secure-development-and-engineering`, `policy-network-communications-security`, `policy-information-security`; a pre-push verifier caught these mid-PR, so they were reverted). Each needs its old-section-number to new-`§N` map applied to every citer and inline clause in the same PR; the numbering itself is gate-blind (gate 38 strips numbering), so this is editorial-consistency, not error-prevention. A dedicated effort (**one document per PR**, deterministic apply + citation remap + re-parse) is the shape being worked, per the maintainer's 2026-07-01 directive: one document at a time with maximal QA, no mass change until certain the renumber leaves zero broken links or references anywhere (this supersedes the earlier "one domain-batch per PR" framing, chosen for its smaller per-PR blast radius on a high-risk structural change).

### 1.4 Audit-gate candidates from the 2026-06-22 review (M, S each) (was 4.5)

Decided 2026-06-23 (maintainer triage): **build them all** from the 2026-06-22 review. **S3 remains** (the only open item in this section); the original S1 retention-consistency gate shipped in #462, S2 was closed in #463 as a register consolidation (the role-consistency check already existing as gate 8 `lint-roles.py`), and **S4 (no-bare-normative-`shall`) shipped in #466** (gate 56). Each is a `lint-*.py` + 4-surface wiring + regression fixture; one gate per PR to keep diffs reviewable.

- **S3 Citation-precision-for-claim gate**: flag "aligned with [normative source] X" claims and verify X actually contains the supporting language (catches FR-120-class issues).

### 1.5 Reference version-currency residuals (from the register version-currency build, #505) (S each)

The §1.5 reference version-currency register **shipped in #505** (the `Upstream check location` + `Last verified (UTC)` columns across all 16 register tables, the advisory staleness cadence in [`specification-citation-verification.md`](governance/specification-citation-verification.md) §12.3, the scratch-is-storage / upstream-is-authority principle, the §7 publisher allow-list extension, and 7 upstream-confirmed register corrections), and **all three citation version-upgrade follow-ups have now shipped** (ISO/IEC 27033 -> 27033-1:2015 #506; ISO/IEC 27036-2 2014 -> 2022 #507; NIST SP 800-88 Rev. 2 re-point + IEEE 2883 introduction #508). Remaining residuals:

- The **51 `needs-reconfirm` rows** (iso.org, the IEC webstore, and several government sources block automated fetch) await a browser or different-egress reconfirm pass to fill their `Upstream check location` URLs and stamp a verified date.

## Priority 2 — Fill significant gaps

Deepening thin-but-present content to operational sufficiency, and the significant missing capabilities. The deepen-baselines cluster (FR-15 / 23 / 63 / 74 / 99 / 154 / 41) was decided for operational deepening (maintainer 2026-06-25).

### 2.1 Privacy jurisdiction annex operational deepening (FR-59, H, L)

Privacy jurisdiction annexes are too shallow for operational sufficiency; deepen the 25 country annexes to operational level. **Reference-base aid (2026-06-27 scratch-review S-7)**: `grc_library_scratch/ref/legislation/` now holds primary-source full-text for Japan APPI, Virginia VCDPA, Colorado Privacy Act, and the LATAM laws (Mexico, Brazil, Argentina, Colombia, Uruguay); author the deepening against those held sources. Honest caveat: APAC beyond Japan (Singapore, Australia, Korea, China, India) remains maintainer-drop (absent from the ref base).

### 2.2 HIPAA operational deepening (FR-60, H, L)

HIPAA adopter has no operational detail beyond a single 261-line sector annex in `compliance/healthcare`. Deepen.

### 2.3 Crypto-asset / blockchain governance domain (FR-70, H[critical], XL)

New domain for crypto-asset / blockchain governance — digital-asset custody, staking, smart-contract risk, blockchain platform vetting. Regulatory references: DORA, MiCA, NYDFS BitLicense. (Cross-references P6.x for domain-level shaping.)

### 2.4 Per-control effectiveness metrics (FR-99, M, M) ⚠

Per-control effectiveness metrics (continuous assurance / 3LoD).

### 2.5 Maturity-ladder methodology (FR-15, M, M)

Maturity-ladder methodology — median-of-medians scoring concern.

### 2.6 Audit-evidence assembler-verification standard (FR-23, M, M) ⚠

Audit-evidence assembler-verification standard absent.

### 2.7 Worked example: adoption, not ingestion (FR-63, M, M)

Worked example walks ingestion not adoption.

### 2.8 Schrems II operational deepening (FR-74, M, M)

Schrems II-light treatment. **Update 2026-06-30: the TIA instrument shipped in #483 (FR-34), which delivers the six-step transfer-impact assessment; FR-74's residual is the Schrems II operational deepening of the EU jurisdiction annex and the cross-border procedure (per the FR-154 "deepen to operational depth" decision). The TIA cross-reference wiring shipped in #489.** Consolidates with FR-34 (Transfer Impact Assessment, now shipped).

### 2.9 Operational-vagueness cluster (FR-154, M, M) ⚠

Operational-vagueness cluster: DSR forward immediate-vs-same-day ([`privacy/procedure-data-subject-rights-management.md`](privacy/procedure-data-subject-rights-management.md):52/:88, pointers as of the #572 state); DSR restriction clock start (:70); critical-risk interim authority ([`risk/procedure-risk-assessment-methodology.md`](risk/procedure-risk-assessment-methodology.md):124); supplier remediation gate ([`supply-chain/procedure-supplier-due-diligence.md`](supply-chain/procedure-supplier-due-diligence.md):85); whistleblower timelines ([`governance/procedure-whistleblower-and-incident-reporting.md`](governance/procedure-whistleblower-and-incident-reporting.md):103); dept-continuity template blanks; incident-reporting escalation thresholds; model-lifecycle thresholds. **Decided (maintainer 2026-06-25): deepen all of the thin-baseline cluster** (FR-15, FR-23, FR-24, FR-63, FR-74, FR-99, FR-154) to operational depth; this overrides the earlier "calibrate first, several are deliberately-thin baselines" guidance.

### 2.10 AI Article 22 + EU AI Act + FRIA unified workflow (FR-41, M, L)

AI Article 22 + EU AI Act + FRIA dual/triple-compliance workflow not documented as a unified workflow. (Privacy completion; FR-37/38/39/40/42 closed in #224-#228.)

### 2.11 Publications-assessment / poisoning-detection process for the scratch reference base (M, M) — surfaced 2026-06-25 (was 4.12)

The `grc_library_scratch` reference knowledge base is split by trust into `ref/standards/`
(accepted standards, trusted, cite-as-authoritative) and `ref/publications/` (vendor
explainers, surveys, threat reports, interpretive guidance, **untrusted by default**).
The publications bucket is an AI trust-boundary / attack surface (an untrusted external
document in an AI's reference context can carry bias, error, or prompt-injection /
poisoning). **Maintainer-directed 2026-06-25**: create a formal process to (a) assess each
publication for useful and relevant information, and (b) identify poisoning or false
information, before any publication's content informs corpus work. Deliverables: a process
doc (likely a `skills/`-style workflow + a `ref/publications/README.md` protocol pointer)
covering intake screening (provenance, integrity, instruction-like-content detection per
the OWASP LLM prompt-injection / improper-output-handling guidance the corpus already
cites), an assess-and-tag step (relevant/useful vs discard; corroborate load-bearing
claims against a `standards/` source), and a recorded assessment per publication. Pairs
with the §3.6 multi-session track (the scratch ref base is part of that capability) and
the existing `governance/` trust disciplines. Honest-backstop framing: the process raises
the bar against poisoned reference input; it does not by itself guarantee detection.

### 2.13 Cross-document control and timing contradictions (audit 2026-07-02, one routed note remaining)

Items 12-14 and 16-19 closed in the C8 PR (stricter-safe or canonical-source resolutions, each logged in its CHANGELOG entry); item 11 (the GDPR DSR clock wording) closed in the DSR-clock PR. Remaining: the routed acceptance-authority note carrying three carriers (blocked on the GDPR-Article-36-to-High-band mapping decision, a morning item).

- **(routed note, #561 verifier, L, S) PIA high-residual acceptance signatory.** [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](privacy/procedure-privacy-impact-and-cross-border-transfer.md):220 has the CIO (acting DPO) signing the residual-risk acceptance for high-residual-risk processing, which sits uneasily beside the canonical High-acceptance authority (Executive Committee or Board Risk Committee). Not a retired-authority carrier; the open question is whether privacy "high-residual-risk processing" (the GDPR Article 36 prior-consultation threshold) maps 1:1 to the risk matrix's High band before the signatory is judged misaligned. Decide the mapping, then align or annotate. Same-class siblings from the #561 `/validate-pr` (word-form "accepted", invisible to the "approv" scan): [`governance/procedure-grc-programme-management-and-annual-review.md`](governance/procedure-grc-programme-management-and-annual-review.md):262 ("formally accepted in writing by the CIO or above", satisfiable by a CIO-alone signature for a High or Critical residual) and :266 ("Residual risks accepted at ERC level", asserting an ERC acceptance level the role register does not grant). Align all three to the canonical chain in one pass once the mapping question is decided.

---

## Priority 3 — Clean up and tooling

Cross-document consistency cleanup and routine development / quality tooling: lower-priority than gaps, not error-prevention or adopter-facing. Picked deliberately into batches, not from the routine P1/P2 queue.

### 3.1 Sweep 3 follow-up: cross-document term/identifier consistency (L, S)

Cross-document term-and-identifier consistency gap (the prose-and-numbering C3 surface mechanical gates 35/39/41 don't cover). Candidate for a future mechanical gate; a manual sweep closes the open items meanwhile.

### 3.4 Backlog effort-sizing labels convention (M, S) (was 4.2)

Backlog items now carry `(severity, effort)`; this item formalizes the convention. Proposed scale:

| Label | Per-item effort | Bundleable per PR |
|---|---|---|
| **XS** (single-line / single-cell) | 5-15 min | 5-10 items |
| **S** (single-doc section add) | 30-90 min | 2-4 items |
| **M** (multi-doc, bounded) | 2-4 hrs | 1 item |
| **L** (new artefact, multi-doc propagation) | 4-8 hrs | 1 item |
| **XL** (new domain, library-wide reshape) | 1-3 days | 1 item, may split |

**Surfaces to update when the convention formally lands**: `library-fitness-review/SKILL.md`; `validation-sweep/SKILL.md`; this file (already in use); `.working/DONE.md` heading shape; future fitness-review templates and sweep detail files. Schedule: after the current FR backlog closes.

### 3.6 Multi-session / multi-worker orchestration codification (M, L) — track; maintainer-scheduled (was 4.11)

Stand up the parallel-worker capability per the **"Multi-session / multi-worker orchestration model"** entry in [`.working/design-decisions.md`](.working/design-decisions.md) (the authoritative design; recovered to `main` in #316). A deliberately-scheduled meta/process track, not a routine backlog fix.

Deliverables 1-3 have shipped: the runbook [`.working/multi-session-orchestration.md`](.working/multi-session-orchestration.md), the Model-B worker section in [`.working/worker-brief-template.md`](.working/worker-brief-template.md), and the light-SOP default in [`.claude/CLAUDE.md`](.claude/CLAUDE.md) + the [`ai-assistant-workflow-disciplines`](dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md) rule. **Remaining (the residue):**

4. A **worker-provenance audit gate**, co-designed with the shipped bookkeeping-parity gate family (gate 50 QA-cadence parity, plus gate 57 and the D5 PR-time check for rotation) as one "bookkeeping-parity" gate family, built the project way (`tools/lint-*.py` + four-surface wiring + regression fixture), honest-backstop framing per [`gate-discipline`](dev-security/claude-rules/governance/gate-discipline.md) (it enforces the PRESENCE of the verification record and provenance attestation, not semantic correctness). The separate pre-push-runner gate (folding gate-40/gate-31 into [`tools/run-pr-time-checks.sh`](tools/run-pr-time-checks.sh)) already shipped in #333, so this gate extends rather than duplicates it. The codification PR is itself NOT partitionable (single orchestrator session).

- **Feasibility note:** `grc_library_scratch` is in scope, reachable, and now populated (the `ref/` base). The in-session subagent primitive is exercised; the separate-session external-collaborator primitive and harness support for repo-event subscription remain to confirm at implementation time (the design gates event-driven triggering as opt-in, not the default).
- **SCHEDULING (maintainer decides when):** default is to implement this AFTER the Priority 1 and Priority 2 backlog items are addressed. **Standing exception (do NOT self-authorize):** if at any point the orchestrator judges that standing up this capability would clear the REMAINING P1/P2 backlog faster than working solo on those items, net of the codification cost and counting only partitionable remaining work, surface a pull-forward recommendation with the reasoning (estimated remaining partitionable volume, expected speedup, build cost) and let the maintainer decide.

### 3.7 Session-concurrency safety: session-state lease + git cross-check (M, M) — maintainer-requested 2026-06-26 (was 4.18)

Build the concurrent-session interlock so a `/resume` issued while a prior session is still live cannot corrupt shared `main` state (handoff / TODO / DONE / validate-sweeps / detailed CHANGELOG / the four version surfaces). Full design (problem, options A/B/C, recommended mechanism, honest limitations, build steps, open sub-decisions) is captured in [`.working/design-decisions.md`](.working/design-decisions.md) under "Session-concurrency safety". Summary of the recommended option (C): a gate-exempt `.working/session-state.md` lease (active-session branch, status, `date -u` heartbeat, worker-dispatch list) PLUS a `git fetch` cross-check of recent unmerged `origin/claude/*` branches, wired as a new `/resume` step 0 that HOLDs + surfaces when a session looks live. Deliverables: the lease file + schema; `/resume` step 0; acquire/refresh/release lifecycle wiring in `.claude/CLAUDE.md` + the handoff; optionally a `lint-overnight-file`-style well-formedness gate (four-surface-wired). **Open sub-decisions for the maintainer to confirm at build time**: the staleness-window value (proposed 60 min), advisory-HOLD vs hard-block on a fresh-heartbeat active lease (proposed advisory), and whether to build the well-formedness gate now or defer. Honest scope note: this is an advisory interlock, not a hard mutex (no cross-container lock primitive exists); it prevents the realistic accidental-double-resume, not a determined simultaneous launch. Pairs with §3.6 (multi-session) and the bookkeeping-parity gate family (gate 50 QA-cadence parity plus gate 57 and the D5 PR-time check for rotation).

### 3.8 Orchestrator main-loop token instrumentation for session-metrics (L, S) — maintainer-requested 2026-06-27 (was 4.19)

The [`.working/session-metrics.md`](.working/session-metrics.md) ledger records measured `subagent_tokens` per phase, but the **Orchestrator tokens** column is always `not instrumented` (the convention forbids a fabricated figure). Maintainer-flagged 2026-06-27 to close the gap if feasible. **Feasibility investigated this session (PR #388)**: orchestrator main-loop tokens are NOT instrumentable from inside a session, because (a) no tool surfaces the orchestrator's own per-turn usage (the `Agent` tool returns only `subagent_tokens` for subagents), and (b) no main-session transcript carrying per-message `usage` / `output_tokens` is written to a readable on-disk location during the session (the session project dir holds only `subagents/` and `tool-results/` subdirectories; `~/.claude/sessions/<n>.json` is bare process metadata with no token fields). The realistic paths, none assistant-self-instrumentable today: (1) **harness support**, surface main-loop `usage` the way the `Agent` tool already surfaces `subagent_tokens`, or expose an end-of-session usage-summary (the clean fix; needs a Claude Code feature, so it is a feature request, not an in-repo build); (2) **maintainer-side external measurement**, read total session token usage from the Claude Code UI or the Anthropic Console usage view and record it out-of-band into the metrics row (available today; maintainer action, not assistant self-instrumentation); (3) **post-hoc transcript analysis**, IF a main-session conversation JSONL with `usage` fields is persisted to a readable location after the session ends (the subagent JSONLs persist under `projects/.../subagents/`, so a main transcript may appear post-session, but this is not verifiable from inside a live session), a small summing script over `output_tokens` would then be a low-effort build. Until a path lands the column stays `not instrumented`, which is the honest state the convention already mandates. Next concrete step (maintainer-gated): confirm whether a main-session `*.jsonl` carrying `usage` is retrievable post-session; if yes, a post-hoc summing aid is a small build; if no, the gap is a harness-feature request to file. This item closes when either the aid ships or the maintainer accepts `not instrumented` as the permanent state.

### 3.10 TODO-hygiene completion pass + accretion guard (S, S) — surfaced 2026-06-27 (was 4.23)

The maintainer flagged (2026-06-27) that shipped/historical content had accreted in TODO instead of rotating out. Parts (a) and (b) shipped in the TODO-hygiene PR: (a) §3.6 (multi-session orchestration) trimmed to its residue (deliverable 4, the worker-provenance gate; deliverables 1-3 shipped) after verifying against the gate inventory of the time; (b) the unambiguous shipped/closed clauses deleted (the Queueing-rules "FR-166/DD-1/DD-9 already shipped" note, the P3-intro "B2 closed #408 / DD-12 closed" parenthetical, the retro-log section's "actioned in #275" line, the §3.7 "D4 shipped in #366" clause, the Backlog-totals "closed in #N" clauses).

**Remaining (open):** (c) **whether the `## Standing conventions`, `## Backlog totals`, and `## Priority 7` (audit-trail-only) sections belong in TODO at all** or in a conventions / design-decisions doc. This is a **maintainer call** (they are non-forward-looking but appear intentionally retained); filed for decision in `## Priority 7`. The **accretion guard** is the TODO/DONE-rotation gate family, now shipped (gate 57 catches in-place self-marking; the D5 PR-time check catches a wholesale-forgotten rotation when a PR's CHANGELOG asserts a backlog-item closure). A possible extension (consider) is teaching gate 45 to flag shipped-PR-number history accreting inside an open TODO item, so accretion is mechanically prompted rather than convention-only.

### 3.12 CLAUDE.md removal-ledger review cadence (standing) — added 2026-06-28, PR #441 (was 4.27)

The PR #441 condense of [`.claude/CLAUDE.md`](.claude/CLAUDE.md) moved the cut rationale, war-stories, and provenance into [`.working/claude-md-considerations.md`](.working/claude-md-considerations.md) (the removal ledger), each entry carrying an "evidence the removal was wrong" signal. Standing activity (not a one-time task): each `/retro` does a quick scan of the ledger's open RM entries and the periodic hallucination-metrics pass does a deeper one; if an entry's signal appears, advise the maintainer to restore the cut text or make a new CLAUDE.md change, and record the disposition in that entry's Status. Wired into [`.working/improvement-log.md`](.working/improvement-log.md)'s Convention section. This item is the durable tracker so the cadence is not lost; it stays open by design.

### 3.13 Audit-surfaced gate / tooling extensions (audit 2026-07-02) (M each)

Mechanical-coverage extensions the 2026-07-02 audit surfaced; each is a `tools/` change built the project way (four-surface wiring + regression fixture where a new/changed gate). Several are coupled to a fix item and should land after that item's canonical values are set.

- **(GR-P3 graduation, #565 retro, M, S) Partial-rewrite tension-marker check.** The late-adopted-fix propagation facet hit three occurrences (#563/#564/#565: a scope-adding fix or rewrite touching part of a block while hedges or stale framings survive elsewhere in the same block) and graduates to a gate proposal per the GR-P3 convention: a PR-time check that, for any diff hunk rewriting part of a TODO bullet or ledger row, re-lints the WHOLE containing block for tension markers ("likely", "NEEDS-UPSTREAM", "pending", "TBD") contradicting the block's own status framing (e.g. "upstream-CONFIRMED"). Design alongside the shipped GR-12 residual-scan aid ([`tools/residual-scan.py`](tools/residual-scan.py)); both are residual-scan tooling.
- **(from item 9) COBIT + ISO 31000 citation coverage.** Gates 48/49/54/58 cover CCM/NIST/ISO-Annex-A control-code existence but not COBIT practice codes or ISO 31000 clause numbers, so the APO12.07 fabrication and the ISO 31000 clause swap in [`governance/matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md) were gate-blind (both fixed in the C6 PR; the coverage gap remains for future edits). Extend `/matrix-fit` coverage or add a dedicated existence check (scratch has held the COBIT 2019 Governance and Management Objectives full text since 2026-06-27, so the COBIT half is buildable; ISO 31000:2018 is still not held, so the ISO 31000 half stays source-gated). Routed note (C6, extended by its verifier): the canonical-title corrections expose four semantic-fit questions for an ad-hoc `/matrix-fit` pass or this gate's design: in the matrix, APO12.01 "Collect data" on the framework-and-governance row, APO12.02 "Analyze risk" on the risk-appetite row (where ISO 31000's closest semantic home is arguably 6.3.4 Defining risk criteria), and APO12.03 "Maintain a risk profile" on the identification-and-analysis row; and in the exception policy, APO12.03 in the risk-assessment intent at three carriers that move together on any recode (the :130 framework bullet, now canonically titled, plus the bare codes at :66 and :144) where APO12.02 may fit better. Title-only corrections shipped; any recode is the fit pass's call. Adjacent parallel case, FIXED in the batch-A PR: the two risk-doc cells citing `APO10 Manage Suppliers` were corrected to the COBIT 2019 canonical `APO10 Managed Vendors`, confirmed at the held scratch COBIT 2019 Governance and Management Objectives full text and at the in-corpus canonical carrier in [`risk/standard-third-party-and-supply-chain-risk.md`](risk/standard-third-party-and-supply-chain-risk.md). (The batch-A first draft deferred this on a stale no-COBIT-held claim; the pre-push verifier refuted it against the scratch index, the inventory-claim lesson.)
- **(from item 20) Positional-backlog-token lint.** Optional: a lint flagging `TODO P?N.M` positional tokens in gate-scanned corpus prose (they are renumber-fragile), nudging references toward stable FR-ids / topic names. Same class as the CLAUDE.md §N-orphan guard.

### 3.14 Low-severity cleanup batch (audit 2026-07-02 low-sev + items 15,22,23,24) (L, XS-S)

Cheap, mostly-mechanical corrections re-validated at source; bundle into one or a few small PRs. The mechanical half shipped in the batch-A PR and the judgment tier (the rollout-phasing note, the two retention resolutions, the two genericizations) in the batch-B PR; the remaining bullets are the maintainer-answered items L-j and the coverage-gaps status triage (L-k shipped separately). (One audit low-sev candidate, the glossary CalVer/PR, was REFUTED: the glossary carries the standard 13-field block like its peers, and no document carries a Library Version/PR in its metadata, so it is not a finding.)

- **(routed note, C9 verifier extended by the #568 sweep, L, S) Coverage-gaps dangling-pointer status triage.** Fifteen register cells pointed at backlog work TODO does not carry: C9 reworded eight to the evidence-accurate "Backlog candidate: ... (not currently scheduled in TODO)" form (the IEC 62443 row, the three adopter-experience rows, the four deferred sector rows) plus a ninth mention inline in the manufacturing row's Notes prose, and C10 reworded seven more the #568 sweep found mis-mapped (the AWS/Azure/GCP and Kubernetes overlay rows, whose subjects the multi-cloud TODO item explicitly excludes, and the PCI DSS / Basel III / SWIFT CSP rows, which are not country regulators). Several rows' Coverage/Status cells may also be stale: the adopter-experience asks are partly shipped in docs/; OT shipped as a suite; the AWS/Azure/GCP rows say Coverage "None" while the per-cloud hardening baselines exist in dev-security/. Maintainer triage: re-grade those rows or confirm the candidate framing.
- **(L-j, S, maintainer decision + gate co-change; batch-A research 2026-07-02) Classification field overloaded, and the value is LOAD-BEARING.** [`privacy/annex-regional-privacy-requirements.md`](privacy/annex-regional-privacy-requirements.md):10 `Classification: Deprecated` overloads the Classification metadata field with a lifecycle status, AND three linters key their skip on exactly that value ([`tools/lint-required-sections.py`](tools/lint-required-sections.py):119, [`tools/lint-section-placement.py`](tools/lint-section-placement.py):163, [`tools/lint-stub-documents.py`](tools/lint-stub-documents.py):101), so restoring `Classification: Public` alone turns three gates red on the redirect stub. The fix needs a design choice (a dedicated lifecycle marker the three linters key on instead, changed with fixtures in the same PR, or maintainer acceptance of the overload as a documented convention); not XS-mechanical.

### 3.15 Guardrail-review machinery extensions (guardrail review 2026-07-02) (M mostly, S-M each)

Machinery findings from the 2026-07-02 guardrail review (gates, rules, skills, and toolchain assessed as a system; the corpus-audit siblings are §3.13/§3.14, nothing below duplicates them). Every claim re-verified at source at intake; one lens-agent claim (a "gates 32 and 33" comment alleged in the date-staleness linter) was REFUTED at intake (zero grep hits) and is not carried. Each gate-shaped item is built the project way (four-surface wiring + regression fixture).

- **(GR-3 residual, M, S) Metadata-parser migration, waves 2-3.** Wave 1 shipped in the W3 PR: `parse_metadata_block()` + `parse_iso_date()` live in [`tools/lint_common.py`](tools/lint_common.py), and gate 31 now fails loud on a present-but-malformed Date (a trailing annotation is a finding, not a `skipped_no_date`; skip counts reported in its OK line). Remaining: wave 2, migrate the Version-window trio (gate 40 plus the D2/D4 delta checks, which share the identical head-window and regex; caveat from the #556 verifier: the trio tolerates leading whitespace where the shared `METADATA_FIELD_RE` does not, so the migration slightly narrows, and D4's private Date parse still treats an annotated Date as a missing canonical line); wave 3, decide whether gate 1's `extract_metadata` (block-boundary semantics differ; note gate 31 is now STRICTER than gate 1 for an empty Date value, coherent under fail-loud) and [`tools/build-taxonomy.py`](tools/build-taxonomy.py)'s duplicate field pattern fold into the shared parser or stay (their parsing is already fail-loud).
- **(GR-4 residual, L, XS) Unbalanced-fence detection home.** The `~~~` toggle shipped in the W3 PR ([`tools/lint_common.py`](tools/lint_common.py) `iter_non_code_lines` toggles on both fence characters; the corpus census found zero tilde or unbalanced fences, so the change was preventive). Residual: an UNBALANCED fence still silently suppresses scanning of everything after it; detection needs a home decision (no structural markdown gate exists, and a warning inside the iterator does not fit its generator contract), so pick a host gate or a tiny standalone check, then wire + fixture.
- **(routed, #577 sweep L2, S) Gate-60 live gate-count parse scoped to the section-6 table.** [`tools/lint-guardrail-cadence.py`](tools/lint-guardrail-cadence.py) counts numeric-first-cell rows across the whole spec file, where gates 35 and 39 scope their parse to the section-6 heading. No live defect (the spec has exactly one such table today, so the whole-file count equals the gate-39-verified inventory), but a future numeric-first-cell table elsewhere in the spec would inflate the live count and manufacture spurious drift. Mirror the gate-39 scoped parse; the regression fixture's synthetic spec gains the section heading in the same change. Pairs naturally with GR-6 (both parse the section-6 surface).
- **(routed, #577 sweep I2, L, XS) Gate-39 vanished-file tolerance.** Run concurrently with the regression suite in the same tree, gate 39 crashed on a transient tests temp fixture (FileNotFoundError mid-scan); serial CI is unaffected and a serial re-run passes. Harden the scan loop to tolerate files vanishing between discovery and read.
- **(GR-6, M, S) Audit-programme detailed-prose presence check.** For each gate in the [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) inventory, the detailed-prose enumeration must carry the paired "Gate N is a ..." description and "Gate N is appended ..." sentence; gate 35 checks only the table and gate 39 only counts rows, so a shipped gate's missing prose pair recurs (gate 57 at Sweep 77; the gate-55-in-section-5 case now in §3.14). Presence-only check, not semantic.
- **(GR-8, M, S) Close the two watch-loops.** (a) Removal-ledger dispositions: [`.working/claude-md-considerations.md`](.working/claude-md-considerations.md) has 15 of 15 RM entries at "Status: open" with zero dispositions ever recorded, so the §3.12 standing cadence exists on paper only; run a disposition pass and record per-entry outcomes (including the RM-6 watch-list recurrences and the gate-57 coverage-gap note, "Option B would not have caught #466", in the retained superseded section-4.10/4.6 note of [`.working/pending-decisions.md`](.working/pending-decisions.md)). (b) Retro proposed-improvements closure: [`.working/improvement-log.md`](.working/improvement-log.md) proposals accumulate un-codified and their classes recur (#446 then #450; #471 then #472); adopt a closure discipline so each proposal is codified, rejected, or expired.
- **(GR-9, L, XS) Scratch-bucket misdescription in orchestration surfaces.** [`.working/worker-brief-template.md`](.working/worker-brief-template.md):50 places the CSA CCM/AICM catalogue CSVs in the scratch repo's `ref/standards/` and :163-167 lists CSA CCM/AICM/CAIQ under `ref/standards/`; scratch actually holds CSA/MITRE/OWASP/COBIT under `ref/frameworks/` (`ref/standards/` holds ETSI/IEEE/ISO/NIST). Same misdescription in [`.working/multi-session-orchestration.md`](.working/multi-session-orchestration.md):144-146,176-182 and [`.claude/commands/resume.md`](.claude/commands/resume.md):25 (a protected-tree touch: log it when edited).
- **(GR-10, L, S) History-aware gate subprocess batching.** Gate 31 spawns a git subprocess per document (200-plus spawns, run twice per pre-push via the guard) and gate 40 is heavier; a batched `git log --name-only` pass would trade `--follow` fidelity for one subprocess. Optimization only; correctness unaffected; queue behind the functional items.
- **(GR-11, L, XS) Preflight-changelog internal hygiene.** [`tools/preflight-changelog.py`](tools/preflight-changelog.py) uses two inconsistent code-span parsers in one file, and its 0/1/2 exit-code convention is sound but undocumented in the docstring.


---

## Priority 4 — Adopter experience

Capability and guidance for organizations adopting the library, and the operator-experience tooling for running the project. Scheduled deliberately, after the fix/gap/cleanup tiers.

### 4.1 Corpus-management discipline as a shareable skill (M, XL)

Package the cumulative documentation-and-corpus discipline this project has accumulated as a standalone Claude Code skill that anyone managing a documentation corpus with an AI coding assistant could install.

- **Distillation source**: the twelve `governance/` pack rules form the discipline core; `validation-sweep` and `library-fitness-review` form the periodic-review surface; the audit-programme architecture forms the mechanical-enforcement surface.
- **Generalization**: carry the patterns and discipline without the GRC-specific control-set citations; adopters supply their own document-type model and metadata-field set.
- **Open questions resolved 2026-06-22**: skill **family** (not omnibus); **prescriptive-only** (no linter scaffolds); **existing pack 1.x bump** (not a new pack). Sequencing: after the FR backlog closes.

### 4.2 Pack: dev-security/claude-rules language coverage review (M, M) (was 4.4)

Review the language-specific security rules in [`dev-security/claude-rules/`](dev-security/claude-rules/). Today the pack ships Python-focused guidance plus external overlay rules. Decided 2026-06-22: baseline subset = **JS/TS + Go + Java** (others deferred); **explicitly position the pack as pointing to OWASP cheat sheets / dedicated technical-security sources rather than duplicating them**. Scope: one or more small PRs each adding a language baseline file (mirror `python.md`'s shape) OR updating the pack README's positioning.

### 4.3 Overnight unattended-run driver (M, L) (was 4.7)

Deferred to a future session (maintainer-directed 2026-06-22). For longer unattended runs, a single overnight session is the wrong shape (it degrades like any long session). The sound architecture is an **external driver loop** (cron / CI / Agent SDK script, outside the corpus) that launches a **fresh `claude -p` or SDK session per task-unit**, each reading `.working/session-handoff.md` + the TODO/DONE queue, doing one unit, committing, advancing the queue, and exiting. The durable-state layer already exists (`session-handoff.md`, `/resume`, the green-merge-as-last-act + loop-break disciplines); the missing piece is the driver plus an overnight runbook.

- **Design questions**: where the driver runs; merge authority for unattended worker sessions; the stop condition; how a worker signals "needs maintainer" vs "safe to continue"; interaction with the `## overnight-work protocol` in the change-tracking rule.
- **Building blocks confirmed** (2026-06-22): `claude -p` fresh-by-default; Agent SDK fresh-session-per-call; no built-in overnight/auto-reset scheduler in CLI or web.

### 4.4 Multi-session research-brief staging + `/subagent` external-worker entry (M, M) — maintainer-requested 2026-06-26 (was 4.16)

Stand up the INPUT half of the §3.6 multi-session capability so separate-session / separate-account workers can pick up research tasks (the existing §3.6 work delivered the runbook, the worker `CLAUDE.md` contract, the light SOP, and the bookkeeping-parity gate; this adds the brief-staging input channel and the worker entry command). Design advised 2026-06-26; deliverables:

1. **A `research/<work-unit-id>/brief.md` convention in [`grc_library_scratch`](https://github.com/jposluns/grc_library_scratch)** (one brief per partitionable TODO or per FR-167 batch), orchestrator-authored from [`.working/worker-brief-template.md`](.working/worker-brief-template.md): the task, the exact main-repo target paths, the verified-disjoint partition, the `path:line` evidence requirement, the deliverable shape (research, not final prose), the stop-don't-merge and verify-against-live-main invariants, and a pointer to the scratch worker `CLAUDE.md` for the general contract (reference, do not duplicate). Workers deliver findings to the existing `inbox/<worker-id>/`.
2. **A `/subagent` slash command** as the external-worker entry point: read the assigned brief, claim it in `claims-ledger.md`, read the named main-repo files read-only, produce findings, deliver to `inbox/`, stop. **Read-only-on-main MUST be enforced by the worker GitHub account's permissions, not by the prompt** (a prompt is not a security boundary, per [`.claude/rules/secrets.md`](.claude/rules/secrets.md) / the security rules).
3. **Codify both** in the runbook [`.working/multi-session-orchestration.md`](.working/multi-session-orchestration.md); add the `/subagent` command file.

**Gating maintainer action**: provision the least-privilege worker account (read `grc_library` / write `grc_library_scratch` only). In-session `Agent` fan-out works today (shares the orchestrator's credentials, spends its budget); the external-worker path needs the account. **Partitionability**: the decided-content TODOs (the FR-59 / FR-60 deepenings and the deepen-baselines cluster, separate files) are the cleanest fit; a corpus-wide sweep, rename, or single matrix stays single-session. **The apply stage stays single-session with full QA regardless** (the validate-then-apply no-bypass invariant: worker provenance never reduces the QA a change receives). Pairs with §3.6 and §2.11 (the publications-assessment process).

### 4.5 Fork-facing guidance + scripts for building an own reference base (L, L) — maintainer-directed 2026-06-27 (was 4.21)

Enable people who fork this library to assemble their **own** reference knowledge base (the authoritative source texts that authoring and citation work draws on) instead of depending on the maintainer's private one. The library is CC BY-SA 4.0 prose, but the source standards it cites (ISO/IEC 27001:2022 and the wider ISO catalogue, CSA CCM v4.1 / AICM v1.1 / CAIQ, NIST CSF 2.0, MITRE, OWASP, jurisdiction legislation) are proprietary or licence-restricted and are **not** redistributed in the corpus. The maintainer keeps those source texts in the separate `grc_library_scratch` repo's `ref/` tree (trust-bucketed `standards/` trusted, `legislation/` trusted-but-version-sensitive, `publications/` assess-first; plus an `ingest/` staging area, a `catalogue.yml`, and PDF-to-text / XLSX-to-CSV extracts for AI-readability). **That scratch repo is the maintainer's own private usage-and-reference and is NOT to be shared / not redistributed** (it holds licensed third-party works); this item is explicitly NOT "publish our scratch repo", it is "give a forker the method and tooling to build their own equivalent from sources they are licensed to hold".

Maintainer note (2026-06-27): the scratch `ref/` now holds the ISO references and is being expanded across the other source families; it stands as the maintainer's reference for content. The fork-facing capability mirrors its proven structure without exposing its contents.

Deliverables to scope at build (none built yet, this item only records the work):

1. **A fork-facing guidance doc** (candidate home: a `docs/` adopter guide, scope-and-confirm at build): where to obtain each cited standard from a known reputable / authoritative source (the issuing body's own store or an authorized distributor), the licensing posture (what a forker may hold privately vs redistribute), and how to upload their own licensed copies (e.g. purchased ISO PDFs) into a local reference tree.
2. **The trust-model and tree convention** a forker should adopt, mirroring the scratch `ref/` model: `standards/` (trusted ground truth, one dir per issuing body) vs `publications/` (assess-first, screen for bias / poisoning before use, per §2.11) vs `legislation/` (authoritative but version-sensitive), with an `ingest/` staging area and a machine-readable catalogue.
3. **Helper scripts** (`tools/`-style, scope precision at build): scaffold the `ref/` tree; fetch-from-reputable-source where a licence and a stable URL permit (never bypass paywalls / licensing); extract text for AI-readability (PDF to `--full-text.md`, spreadsheet to per-sheet CSV) mirroring the scratch extraction form; build / refresh the catalogue. Honour the security rules: no credential-bearing fetches in tracked config; treat downloaded `publications/` content as untrusted until screened.
4. **Wiring notes**: how a forker's reference base feeds the in-repo validator modules ([`tools/ccm_aicm_reference.py`](tools/ccm_aicm_reference.py), [`tools/nist_csf_reference.py`](tools/nist_csf_reference.py)) that gates 48/49/54 build on, and the `/matrix-fit` semantic-fit audit (the [`matrix-fit`](dev-security/claude-rules/skills/matrix-fit/SKILL.md) skill, shipped #399), so a fork can validate control-code citations against its own ground truth.

Low urgency (maintainer flagged it as deferred, "a priority 5 item"); it is filed here in Priority 4 (adopter experience / tooling) because it is fork-facing tooling + guidance, the same class as the other Priority 4 tooling items, rather than the country / regulator content overlays Priority 5 enumerates. Pairs with §2.11 (the publications-assessment / poisoning-detection process) and the standing reference-base discipline the `/resume` Reference-knowledge-base step and the [`multi-session-orchestration`](.working/multi-session-orchestration.md) runbook §6 describe.

### 4.6 Adopter-experience enhancements (audit 2026-07-02, S-a..S-e; FYI/L, XS-M) — suggestions for maintainer triage

Fresh-reader suggestions from the 2026-07-02 audit's persona pass; factual basis re-validated. These are enhancement suggestions (not defects); the maintainer triages which to pursue.

- **(S-a, L, M) Portal audience + maturity tags.** [`docs/portal.md`](docs/portal.md) has audience sections for CIO/CISO/GRC/architecture/privacy/compliance/audit/resilience/engineering but no Board/CEO section, and entries carry no inline maturity/status tag, so Draft v0.x annexes are indistinguishable from mature docs.
- **(S-b, XS) decision-tree unreachable from README.** [`docs/decision-tree.md`](docs/decision-tree.md) (the stated reading order) is not linked from the [`README.md`](README.md) routing table (reachable only via the portal). Add a routing-table link.
- **(S-c, M) No adopter-direction demo.** The adoption path terminates in [`docs/worked-example.md`](docs/worked-example.md), which is a contributor/ingestion walkthrough; there is no adopter-direction role-substitution demo.
- **(S-d, M) No multi-entity/group-structure adoption guidance.** No `docs/` adoption-surface guidance for adopting the library across a group / multi-entity / subsidiary structure (the concept appears only in substantive domain content).
- **(S-e, XS) Approving-Authority legend.** Add a legend note explaining the meta-role "Governance Library Maintainer" (285 docs) as an approving authority. NOTE: the audit framed [`dev-security/policy-secure-development-and-engineering.md`](dev-security/policy-secure-development-and-engineering.md):8 (approved by CIO) as a lone outlier; that is PARTIAL: CIO is the second-most-common approving authority (39 docs), so it is not anomalous.


### 4.7 Pack design improvements (guardrail review 2026-07-02) (M/L, S-L each)

Pack-architecture findings from the 2026-07-02 guardrail review; design-tier work scheduled last in the overnight sequence per the maintainer's interleave-by-risk direction.

- **(GR-P1, M, M) Session-lifecycle pack rule.** The wind-down / attended-autonomous / overnight / handoff apparatus lives only in the project [`.claude/CLAUDE.md`](.claude/CLAUDE.md); adopters inherit none of it, against the pack's own rule-is-the-distributable-form theory. Distribute it as a governance pack rule.
- **(GR-P2, M, L) Rule operative-core condense.** The 12 governance rules total roughly 31,000 words always-on, with fixed per-rule scaffolding (framework tables, why-sections, AI-assistant closers, repeated restatements of the audit-trail axiom) that is rationale, not operative instruction. Two-layer split per the PR #441 CLAUDE.md method: an always-on operative core plus on-demand rationale/provenance, with a removal ledger; per-rule PRs, `lint-language` run on each before first commit. Routed note (#560 `/validate-pr`, out-of-window): the change-tracking rule's two-file-split text says the root CHANGELOG entry carries "the same lead-paragraph wording as the detailed entry", but every entry in practice pairs matching headers with divergent lead wording (root long-form, mirror short-form); reconcile the rule text to the practice (or vice versa) when this rule is condensed.
- **(GR-P3, M, S) Third-occurrence-to-gate escalation convention.** The guardrail review's effectiveness finding: only false-positive-free mechanical gates extinguish failure classes; checklist/convention prose reduces but never stops recurrence (the narrow-scan class has recurred repeatedly across checklist lines, most recently inside Sweep 82's own verification). Codify: a failure class caught three or more times graduates automatically to a gate proposal (an improvement-log column plus a `/retro` step).
- **(GR-P4, L, S) Overlay primary-wins pointers and pruning stance.** The external overlay files under [`.claude/rules/external/`](.claude/rules/external/addyosmani/using-agent-skills.md) carry only a "supplementary" provenance tag; the primary-pack-wins-on-conflict resolution lives only in the project CLAUDE.md. Add a one-line pointer per overlay provenance comment, and record a pruning/refresh stance for the near-duplicate wrapper skills the review identified.
- **(GR-P5, L, S) `derives_from` re-point + coverage gaps.** [`dev-security/claude-rules/skills/deep-qa-review/SKILL.md`](dev-security/claude-rules/skills/deep-qa-review/SKILL.md) and [`dev-security/claude-rules/skills/library-fitness-review/SKILL.md`](dev-security/claude-rules/skills/library-fitness-review/SKILL.md) derive from `evidence-grounded-completion` (which already anchors many skills) rather than `trust-recovery-escalation` (the rule that defines them as its two-skill suite), leaving that rule looking skill-orphaned; re-point them. `validate-inference-before-action` and `surface-counterproductive-instructions` have no derived skill (the strongest candidates for one). Also hoist the exception-register "absent means strict mode" disclosure to the top of the rules that carry it: the hoistable sentence exists in gate-discipline and change-tracking only (artefact-and-branch-discipline carries a cross-reference, not the sentence), and the [`.claude/CLAUDE.md`](.claude/CLAUDE.md) Boundaries line names the wrong trio (it cites evidence-grounded-completion, which has zero exception-register mentions, instead of artefact-and-branch-discipline); correct that carrier in the same PR (a protected-file factual touch, logged per the overnight deferral rules).


---

## Priority 5 — Expand: country / regulator / programme overlays

Adding new coverage to existing domains. Each subitem is a separate small or medium PR; the maintainer schedules deliberately.

### 5.1 AI jurisdiction annexes (FR-62, M, S)

AI jurisdiction annexes absent. (Cross-references P5.9.) **Reference-base aid (2026-06-27 scratch-review S-8)**: `grc_library_scratch/ref/legislation/` holds the Colorado AI Act and EU AI Act full-text, and `ref/frameworks/ETSI/` holds the Securing-AI TR/GR set + EN 304 223 (AI baseline); ground the US-state and EU AI-annex authoring in those held sources.

### 5.2 Logistics country / programme expansion (was 5.1)

The WCO AEO Compendium identifies ~94 trusted-trader programmes globally; the library covers 4 (BASC, CTPAT-US, AEO-UK, PIP-Canada). Highest-priority additions: EU AEO (covers 27 member states under EU UCC Art 38), Mexico NEEC / OEA, Australia Trusted Trader (ATT), Singapore STP / STP-Plus, Japan AEO, Korea AEO, New Zealand Secure Exports Scheme (SES), China AEO.

### 5.3 Financial-services country regulator overlays (was 5.2)

Within `compliance/financial-services/`: UK PRA / FCA (`annex-uk-pra-fca.md`); US OCC / FRB / FDIC / SEC / FINRA; Canada OSFI; Australia APRA; Singapore MAS; Japan FSA.

### 5.4 Healthcare country regulator overlays (was 5.3)

Within `compliance/healthcare/`: US HIPAA detail (Privacy/Security/Breach-Notification Rules, HITECH); UK NHS DSPT; EU MDR / IVDR; Canada PHIPA and provincial frameworks; Australia My Health Records Act.

### 5.5 Energy and utilities country regulator overlays (was 5.4)

Within `compliance/energy-and-utilities/`: US NERC CIP standards; US TSA pipeline cybersecurity directives; UK Ofgem cyber requirements; EU ENISA sectoral guidance.

### 5.6 Telecommunications country regulator overlays (was 5.5)

Within `compliance/telecommunications/`: EU EECC; UK Ofcom telecom security framework; US FCC regulations; Australia ACMA requirements.

### 5.7 Public-sector country / regulator overlays (was 5.6)

Within `compliance/public-sector/`: UK Government Cyber Security Strategy and GovAssure; Australia ISM and PSPF; Canada IT Standards for federal departments; EU eIDAS public-sector authentication.

### 5.8 Privacy jurisdiction gaps (was 5.7)

Existing privacy domain covers 25 country annexes. Known gaps or stale entries: Argentina (PDPA 2025 update pending); Saudi Arabia PDPL (recent updates pending); Mexico LFPDPPP (standalone annex possible); re-review of EU member-state derogations where applicable.

### 5.9 AI jurisdiction overlays (was 5.8)

The library cites EU AI Act extensively but lacks a dedicated `ai/jurisdictions/` subdirectory parallel to `privacy/jurisdictions/`. Candidates: EU AI Act detailed annex; Canada AIDA; UK AI policy framework; US state-by-state AI laws (Colorado AI Act, NYC bias audit law); China generative AI rules; Korea AI framework.


---

## Priority 6 — Expand: new domains

Entirely new domains, multi-week scope each. The maintainer schedules deliberately. Ordered lowest-effort-first.

### 6.1 Identity-specific content depth (L) (was 6.2)

Customer Identity (CIAM) governance, workforce identity governance, identity federation patterns, passwordless adoption playbooks. The library has IAM policy and procedure but no dedicated content for these patterns.

### 6.2 Quantum cryptography readiness deepening (L) (was 6.3)

The library has a phase-level PQC roadmap ([`security/roadmap-post-quantum-cryptography.md`](security/roadmap-post-quantum-cryptography.md)) but not detailed implementation content. Pending: a PQC migration playbook (operational steps per system class), crypto-agility patterns (key abstraction, algorithm switching, hybrid schemes), and post-quantum-ready CA / PKI management.

### 6.3 Cross-framework matrix expansion (L) (was 6.4)

Current matrix ([`governance/matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md)) covers major frameworks; expand to additional sectoral and regional frameworks as the P5 country/sector content grows.

### 6.4 CMMI capability levels alongside maturity levels (L) (was 6.5)

Per maintainer direction 2026-06-22 (low priority, after the FR backlog completes). The corpus uses the 5-tier maturity-level scale at both organization-wide and per-domain granularity; CMMI distinguishes the two (maturity levels 1-5 org-wide; capability levels 0-3 per practice area). Introducing capability levels would: (1) add a capability-level scheme to [`governance/framework-governance-performance-and-improvement.md`](governance/framework-governance-performance-and-improvement.md) §2; (2) update [`docs/template-maturity-self-assessment.md`](docs/template-maturity-self-assessment.md) to use capability levels per domain and aggregate to maturity levels at the programme rollup; (3) possibly extend [`governance/register-digital-trust-and-assurance-metrics.md`](governance/register-digital-trust-and-assurance-metrics.md) DTI thresholds with a capability-level surface.

### 6.5 Multi-cloud governance overlay (XL) (was 6.1)

Per-cloud hardening baselines for AWS, Azure, and GCP exist in `dev-security/`. The remaining gap is multi-cloud governance (cross-cloud risk taxonomy, cross-cloud incident coordination, cloud-portfolio-level controls). Could live in `operations/` or warrant a new `cloud/` domain.


---

## Priority 7 — Awaiting maintainer decision

One open decision pending (§7.1 the TODO audit-trail-only sections question / §3.10(c)). The FR-104 / FR-130 entries are dropped-decision audit-trail records (see [`.working/design-decisions.md`](.working/design-decisions.md)).

### 7.1 Do the audit-trail-only sections belong in TODO? (§3.10(c))

Do the audit-trail-only sections (`## Standing conventions`, `## Backlog totals`, `## Priority 7`) belong in TODO at all, or in a conventions / design-decisions doc? They are non-forward-looking but appear intentionally retained. Maintainer call; left in place pending the decision.

### 7.2 Per-regulation context (FR-104)

Per-regulation context not pursued.

### 7.3 Portal reorder (FR-130)

Portal reorder not pursued (README stays at decision-tree item 1).

---

## Scratch reference-base work (`grc_library_scratch`; ships via MCP PR per the git-proxy issue)

Validated defects in the `grc_library_scratch` reference repo from the 2026-07-02 audit. These ship as PRs to `grc_library_scratch` (not this repo); tracked here for visibility. Item 33 (tracked EPUBs) was decided 2026-07-02: keep tracked under the private-forever promise with watermark scrubbing gated (see [`.working/design-decisions.md`](.working/design-decisions.md)); item 32's corpus-side carrier is noted in SR-5.

### SR-1 `last_checked` currency mechanism is inert (item 26, P2, S)

0 of 233 `ref/catalogue.yml` items carry a `last_checked` field (even the 2026-07-01 ATLAS refresh did not stamp it), and `tools/validate.py`:72-74 checks the field's FORMAT only if present (no presence requirement), so the 7-day-throttle currency discipline in `CONTRIBUTING.md` has no on-disk footprint. Backfill stamps on currency-sensitive buckets and add a presence/due-item check, OR amend the documented SOP. (Design decision: whether to require presence.)

### SR-2 no publications screening-record check (item 27, P2, M; pairs §2.11)

`tools/validate.py` has no publications screening-record check; 15 of 27 publication extracts (the EDPB/WP29 batch) have no per-extract screening record, and the batch's poisoning screen is provenance-only (`ingest-queue.md:92-94`). Pairs with §2.11 (the publications-assessment / poisoning-detection process).

### SR-3 `validate.py` binary-scan coverage gaps (items 28-29, P3, M)

(item 28) The disk->catalogue orphan check (`validate.py`:206) covers only `--full-text.md`; ~20 substantive CSV extracts (ATLAS/ATT&CK tactics + mitigations CSVs, CSA implementation/auditing-guideline tabs) are uncatalogued and unchecked. (item 29) The watermark/PII scan (`validate.py`:219-221) covers `.pdf` only; 22 EPUB + 16 office docs are unscanned. The audit directly scanned all 22 EPUBs and found NO watermark strings (a scan-coverage gap, not a live exposure); the .doc/.docx residual is unchecked. Widen both checks. The 2026-07-02 maintainer directive (watermarks always removed and never in the scratch repo; condition 3 of the keep-tracked decision) makes the item-29 widening load-bearing rather than hygiene: the widened scan is the mechanical enforcement of the scrub promise, so it covers every tracked binary format, not `.pdf` alone.

### SR-4 catalogue / extract hygiene (items 30-31, P3, XS)

(item 30) `ref/publications/WP-BCR-P-Processor-Application-Form--full-text.md` is a 589-byte failed conversion ("conversion produced no text; consult the .doc original") catalogued as a usable extract; drop it from the catalogue or redo the .doc conversion. (item 31) `ref/publications/README.md`:19 says 13 report PDFs (12 on disk; the 13th was reclassified to standards), and `ingest-queue.md`:31-33 says "the 12 KEEP extracts are trimmed" when only 9 are KEEP-TRIM (3 are KEEP-FULL); correct both counts.

### SR-5 ETSI designation is wrong: "EN 304 223" -> "TS 104 223" (item 32, P2, H)

Scratch labels the ETSI AI baseline "ETSI EN 304 223 V2.1.1 (2025-12)" as a formal adopted European Standard in `ref/standards/ETSI/`, `catalogue.yml`:636, and the indexes. Upstream (verified this turn) the document is **ETSI TS 104 223 V1.1.1 (2025-04)**, a **Technical Specification** (a lower normative tier than an EN), titled "Securing Artificial Intelligence (SAI); Baseline Cyber Security Requirements for AI Models and Systems". Wrong on type, number, and version; the "cite-as-authoritative European Standard" trust framing rides on the incorrect designation. Correct across all scratch surfaces, re-assess the `standards/` vs `frameworks/` bucketing, regenerate indexes; if the held PDF genuinely reads "EN 304 223 V2.1.1", escalate as a source-integrity question. **Corpus-side coupling:** this repo's [`TODO.md`](TODO.md) §5.1 carries the same wrong "EN 304 223" designation, to be corrected when SR-5 lands.

---

## Standing conventions

Durable behavioural guidance from the maintainer. NOT actionable items; reference material for the orchestrator and future contributors.

- **"More PRs, keep each one clean"** — favor small focused PRs.
- **"I prefer /validate, not /validation-sweep"** — short slash commands; skill names stay descriptive.
- **"Don't explicitly name or link `.working/`"** in template-content files that adopters see.
- **"Inference must be validated before committing or before anything else uses that information"** — operationalized in [`validate-inference-before-action.md`](dev-security/claude-rules/governance/validate-inference-before-action.md).
- **Activity directories should be self-contained** — operationalized in the canonical `.working/<activity>/` layout.
- **Zero-finding sweeps still need history rows but no detail files** — operationalized in the validation-sweep [`SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) step 9.
- **Sweep history is project-application, not template content** — operationalized by keeping the history file in `.working/`.
- **TODO is forward-looking; historical state rotates to DONE.md** — operationalized in [`change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) PR-finalization-protocol section.
- **After completing a merge, list the upcoming next 5 planned PRs from TODO** — operationalized in [`.claude/CLAUDE.md`](.claude/CLAUDE.md) PR-workflow section and the same pack rule.
- **Validate cadence is 1-8 PRs per batch, not strictly 5** — the 5-PR cadence is default; the batch boundary is chosen at the natural seam.
- **DONE format mirrors TODO format** — DONE H3 headings carry `FR-N (severity)` so the two ledgers are scannable in the same shape. Harmonized in PR #163.
- **Compute-don't-ask** (maintainer-flagged 2026-06-23) — before surfacing a question, apply a "can I compute/verify this myself?" gate; surface the result, not the raw question. (Codified 2026-06-30 into the `clarify-before-acting` rule's compute-first gate, #504.)

---

## Backlog totals

Approximate active counts after the 2026-06-30 work-type re-tier and the 2026-07-02 audit intake (the priority sections themselves are the source of truth; these drift).

- **P1 (fix errors and prevent recurrence)**: 3 items (1.1 FR-48, 1.4 audit-gate candidates, 1.5 reference version-currency; the 2026-07-02 audit P1 cluster is fully closed).
- **P2 (fill significant gaps)**: 12 items (2.1-2.10 the FR deepenings FR-59 / 60 / 70 / 99 / 15 / 23 / 63 / 74 / 154 / 41, 2.11 publications-assessment, plus the 2026-07-02 audit remainder in 2.13; sections 2.12 and 2.14 fully closed).
- **P3 (clean up and tooling)**: 10 items (3.1, 3.4, 3.6-3.8, 3.10, 3.12, plus 3.13 audit tooling extensions, 3.14 low-severity cleanup batch, and 3.15 the 2026-07-02 guardrail-review machinery extensions).
- **P4 (adopter experience)**: 7 items (4.1-4.5, plus 4.6 adopter-experience enhancements and 4.7 the 2026-07-02 guardrail-review pack-design improvements).
- **P5 (expand: country / regulator / programme overlays)**: 9 items (5.1-5.9).
- **P6 (expand: new domains)**: 5 items (6.1-6.5).
- **P7 (awaiting decision)**: 1 pending (7.1) + 2 dropped-decision audit-trail entries (7.2 / 7.3).
- **Scratch reference-base work (`grc_library_scratch`)**: 5 items (SR-1 last_checked, SR-2 screening-record check, SR-3 validate.py binary-scan gaps, SR-4 catalogue/extract hygiene, SR-5 ETSI designation).

---

## Notes on maintenance

- Add new items at the appropriate priority; within a section keep the lowest-effort-first ordering. Move items between priorities as context changes.
- When an item is completed, delete it from this file (no strikethroughs, no `[done]` suffixes) and add an entry to [`.working/DONE.md`](.working/DONE.md) in the same PR. The rotation discipline is documented in the PR-finalization-protocol section of [`.claude/rules/governance/change-tracking.md`](.claude/rules/governance/change-tracking.md).
- Design decisions belong in [`.working/design-decisions.md`](.working/design-decisions.md), not in TODO. The P7 "dropped-decision" entries cross-reference those decisions for audit-trail completeness without duplicating the rationale.
- This file is the source of truth for what's queued; conversation history is not.
- Fitness-review backlogs remain the authoritative per-finding evidence source; this file is the action-organized view, kept in sync at fitness-review-cycle time.
