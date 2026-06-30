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
- **Maintainer-directed running order (2026-06-30 work-type re-tier)**: work the tiers in order. **P1** first (the cheap fix/prevent items: FR-48 and the Per-document-ISO gate-fix, then the §1.3 / §1.4 / §1.5 integrity tooling); then **P2** gaps (FR-59 and FR-60 deepenings and the deepen-baselines cluster first, then **FR-70**, the XL crypto-asset domain, last); then **P3** clean-up-and-tooling; then **P4** adopter experience. **P5 / P6 expansion waits** (maintainer: expansion can wait). The standing **fix-issues-first** directive (2026-06-27) governs within each tier, and the routine `/validate`, `/validate-pr`, and `/matrix-fit` cadences are the reactive half of P1. FR-167, the NIST SP 800 ingestion, and the OT post-ingestion validation are COMPLETE (2026-06-30; ingestion in `grc_library_scratch`, validation in #495).
- **Integrity-tooling items** (the former "guard-rails phase"): the queued retro guard rails (§1.3), the citation-precision gate (§1.4 S3), and the reference version-currency register (§1.5) live in **P1** (fix errors and prevent recurrence); the QA-cadence and TODO/DONE-rotation surfaces are already covered by the bookkeeping-parity gate family (gates 50 and 57, plus the D5 PR-time check). Research fan-out (workers produce verified research from [`.working/worker-brief-template.md`](.working/worker-brief-template.md); the orchestrator re-verifies every claim at apply-time and authors all final prose) is the standing method for partitionable batches.

---

## Priority 1 — Fix errors and prevent recurrence

Correctness fixes and the **error-prevention tooling** that keeps the corpus from regressing. The routine `/validate`, `/validate-pr`, and `/matrix-fit` cadences are the reactive half of this tier; the items below are the standing preventive half.

### 1.1 H2 numbering-pattern drift (FR-48, M, L)

H2 numbering patterns drift — multi-doctype structural rename. Deferred until a dedicated session is scheduled.

### 1.2 Per-document ISO Annex A code validation (L, M) — deferred follow-up to the gate-49-extension track (maintainer-confirmed 2026-06-26)

Extend [`tools/lint-document-control-codes.py`](tools/lint-document-control-codes.py) (gate 54, NIST CSF 2.0 only) to also validate ISO/IEC 27001:2022 Annex A codes (and clause refs) where they appear in per-document framework-reference / crosswalk tables, reusing gate 49's `check_iso_token` logic. Deferred from the gate-54 build because per-document ISO codes are higher-false-positive (clause refs `§10.2`, ranges `A.5.19 to A.5.22`, mixed editions) and the matrix's ISO column is already covered by gate 49; scope a precision-first design before building. **Reference-base aid (2026-06-27 scratch-review S-4)**: the chief blocker the matrix-fit aid records ([`tools/audit-matrix-semantic-fit.py`](tools/audit-matrix-semantic-fit.py):54 "ISO 27001:2022 codes are not assessed (no title source in the repo)") is now addressable: `grc_library_scratch/ref/standards/ISO/` holds the ISO/IEC 27001:2022 Annex A + 27002:2022 control-title extracts. A maintainer-local ISO Annex A title map (proprietary: cite by clause, do not commit the verbatim titles if licence-sensitive) would let both gate 54 and `/matrix-fit` assess ISO-column rows. Licence-handling of the proprietary titles is a maintainer decision.

### 1.3 Retro-log open-loop consolidation (S, S) — surfaced 2026-06-23 (was 4.8)

A review of [`.working/improvement-log.md`](.working/improvement-log.md) found that the **convention/checklist layer** absorbs retro candidates well (lint-language pre-flight, grep-after-convention-change, CHANGELOG-link front-loading are codified in the CLAUDE.md close-out checklist and holding), but the **mechanical-gate and rule-codification layers** accumulate "queued, apply next time" candidates that do not self-clear. Still open (action deliberately, not at a long-turn tail):

**The close-out-checklist apply-time disciplines were codified in #478** (three CLAUDE.md `## Session migration and PR close-out checklist` bullets): **audit-gate change completeness** (the audit-programme spec's detailed-prose enumeration, its per-gate narrative, the grouped-list, the module docstring, and the regression fixture are parallel surfaces no parity gate inspects, folding in #312 gate-behaviour-changed paired-surfaces and the Sweep-77-A1 gate-57 detailed-prose miss, plus the `WORKFLOW_DELTA_GATE_STEPS` note); **full-file-grep and parallel-case re-verification for prose corrections** (folding in #271 parallel-case verification, #340 full-file-grep for prose-fact corrections, and #320 corpus-wide-scrub narrative-surface scope); and **generated-artefact regen order** (#323, taxonomy first then portal/scorecard). The bare-token contradiction search (#261/#262) was already codified in the earlier close-out-checklist bullet. **Residual (still open):**

- **New-skill-drafting checklist** (#213) — enumerate the parallel surfaces (link depths, pack-README skills-table row, PAIRS registry, language pre-flight, slash-command sibling).
- **Broaden the count gate (remainder)**: gate 39 P8 closed "N automated audits" (#273); still open are word-form counts ("forty-six") via a word→number map and the free-prose rule-count gate (gate 41 can't parse "the N governance rules"). This one is a gate change, not a checklist line.

### 1.4 Audit-gate candidates from the 2026-06-22 review (M, S each) (was 4.5)

Decided 2026-06-23 (maintainer triage): **build them all** from the 2026-06-22 review. **S3 remains** (the only open item in this section); the original S1 retention-consistency gate shipped in #462, S2 was closed in #463 as a register consolidation (the role-consistency check already existing as gate 8 `lint-roles.py`), and **S4 (no-bare-normative-`shall`) shipped in #466** (gate 56). Each is a `lint-*.py` + 4-surface wiring + regression fixture; one gate per PR to keep diffs reviewable.

- **S3 Citation-precision-for-claim gate**: flag "aligned with [normative source] X" claims and verify X actually contains the supporting language (catches FR-120-class issues).

### 1.5 Citation version-upgrade follow-ups (from the register version-currency build, #505) (S each)

The §1.5 reference version-currency register **shipped in #505**: the `Upstream check location` + `Last verified (UTC)` columns across all 16 register tables (100 rows verified 2026-06-30, 51 `needs-reconfirm`), the advisory staleness cadence in [`specification-citation-verification.md`](governance/specification-citation-verification.md) §12.3, the scratch-is-storage / upstream-is-authority principle, the §7 publisher allow-list extension, and 7 upstream-confirmed register corrections (built under the high-assurance harness, dual-verifier-checked). Three standard-version upgrades were **deferred** because they ripple into corpus citations and need a coordinated per-document fix (gate-6 plus per-doc Version/Date bump), one tightly-scoped PR each. **ISO/IEC 27033 -> 27033-1:2015 shipped in #506** and **ISO/IEC 27036-2 2014 -> 2022 shipped in #507**; the one remaining:

- **NIST SP 800-88 Rev. 1 -> Rev. 2** (Rev. 1 withdrawn 2025-09-26): 1 doc ([`operations/procedure-media-handling-and-transport.md`](operations/procedure-media-handling-and-transport.md)) for the substantive sanitization-guidance re-point, not a bare version-string swap; note the broader version-bearing citer set to sweep at the start (the register row, plus `supply-chain/template-supplier-offboarding-evidence.md` which cites `Rev. 1` / `800-88r1`).

Also open (not corpus-blocking): the **MITRE ATLAS scratch superseded-archival** (move the deprecated `v5.6.0` to scratch `ref/.superseded/`, fetch `v2026.05`) is MCP / maintainer-download-gated, logged in [`pending-decisions.md`](../.working/pending-decisions.md); the register's ATLAS row already reads `v2026.05`, so the corpus side is correct. The **51 `needs-reconfirm` rows** (iso.org, the IEC webstore, and several government sources block automated fetch) await a browser or different-egress reconfirm pass to fill their `Upstream check location` URLs and stamp a verified date.


---

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

Operational-vagueness cluster: DSR forward immediate-vs-same-day ([`privacy/procedure-data-subject-rights-management.md`](privacy/procedure-data-subject-rights-management.md):52/:84); DSR restriction clock start (:70); critical-risk interim authority ([`risk/procedure-risk-assessment-methodology.md`](risk/procedure-risk-assessment-methodology.md):124); supplier remediation gate ([`supply-chain/procedure-supplier-due-diligence.md`](supply-chain/procedure-supplier-due-diligence.md):85); whistleblower timelines ([`governance/procedure-whistleblower-and-incident-reporting.md`](governance/procedure-whistleblower-and-incident-reporting.md):103); dept-continuity template blanks; incident-reporting escalation thresholds; model-lifecycle thresholds. **Decided (maintainer 2026-06-25): deepen all of the thin-baseline cluster** (FR-15, FR-23, FR-24, FR-63, FR-74, FR-99, FR-154) to operational depth; this overrides the earlier "calibrate first, several are deliberately-thin baselines" guidance.

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


---

## Priority 3 — Clean up and tooling

Cross-document consistency cleanup and routine development / quality tooling: lower-priority than gaps, not error-prevention or adopter-facing. Picked deliberately into batches, not from the routine P1/P2 queue.

### 3.1 Sweep 3 follow-up: cross-document term/identifier consistency (L, S)

Cross-document term-and-identifier consistency gap (the prose-and-numbering C3 surface mechanical gates 35/39/41 don't cover). Candidate for a future mechanical gate; a manual sweep closes the open items meanwhile.

### 3.2 CHANGELOG detailed-mirror per-PR-header parity check (Low, S) — surfaced 2026-06-27 (`/full-qa` F-1)

The detailed CHANGELOG mirror can lose a per-PR `##` header when a later PR's commit overwrites the prior header in place (PR #388 orphaned the #386 and #387 bodies under #388; fixed in PR #392). Delta gate D1 checks per-commit root+detailed lock-step *presence*, not cross-commit header integrity, so the class is gate-blind. Consider a mechanical check asserting the detailed mirror's per-PR `##`-header set equals the root [`CHANGELOG.md`](CHANGELOG.md)'s. Low; pairs with the next CHANGELOG-gate edit.

### 3.3 Citation-verification pass against the scratch `ref/` base (Low, M) — surfaced 2026-06-27 (scratch-review S-2/S-3/S-9)

The scratch `ref/standards/` (ISO/IEC, NIST, ETSI) and `ref/frameworks/` (COBIT 19 docs, CSA CCM/AICM CSVs, MITRE, OWASP) now hold full-text / control-catalogue extracts for many [`register-canonical-citations.md`](governance/register-canonical-citations.md) rows. Run a verification pass confirming the register's ISO / NIST / CSA / COBIT version+date rows against the now-held local extracts (per [`governance/specification-citation-verification.md`](governance/specification-citation-verification.md)), recording results in the Citation Verifications Register. This is a local-ground-truth substitute for the previously egress-blocked verification. Sub-decision: whether to add ETSI rows to the register (EN 303 645 consumer IoT, EN 319 401 trust services, held in `ref/standards/ETSI/`) — the register currently lists no ETSI; maintainer call on scope.

### 3.4 Backlog effort-sizing labels convention (M, S) (was 4.2)

Backlog items now carry `(severity, effort)`; this item formalises the convention. Proposed scale:

| Label | Per-item effort | Bundleable per PR |
|---|---|---|
| **XS** (single-line / single-cell) | 5-15 min | 5-10 items |
| **S** (single-doc section add) | 30-90 min | 2-4 items |
| **M** (multi-doc, bounded) | 2-4 hrs | 1 item |
| **L** (new artefact, multi-doc propagation) | 4-8 hrs | 1 item |
| **XL** (new domain, library-wide reshape) | 1-3 days | 1 item, may split |

**Surfaces to update when the convention formally lands**: `library-fitness-review/SKILL.md`; `validation-sweep/SKILL.md`; this file (already in use); `.working/DONE.md` heading shape; future fitness-review templates and sweep detail files. Schedule: after the current FR backlog closes.

### 3.5 Standard-version-upgrade process (M, M) (was 4.3)

When an external standard the corpus cites is republished (e.g., `ISO/IEC 27001:2013` → `2022`; future COBIT release), the library needs a documented transition process. Sweep 15's `ISO/IEC 29134:2023` hallucination plus the FR-21 `ISO/IEC 27701:2019 → 2025` catch show ad-hoc updates produce drift.

The seven-step process:
1. Diff old and new version; use the publisher's transition guide as authoritative input.
2. Sweep the corpus (grep + canonical-citations register) for every cited location.
3. Classify each citation as positional-only or substantive.
4. Apply updates per classification (positional: year bump; substantive: rewrite with per-document version bump).
5. Update [`governance/register-canonical-citations.md`](governance/register-canonical-citations.md) and the verifications register; mark the old version superseded with effective-date.
6. Confirm gate 6 (`tools/lint-standards-currency.py`) flags the supersession.
7. CHANGELOG entry covering the upgrade campaign (often multi-PR); TODO row if substantive rewrites span multiple PRs.

**Deliverable**: `governance/procedure-standard-version-upgrade.md` documenting the process with worked examples. **Side benefit**: documents the canonical-citations register discipline.

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

### 3.9 Document the scratch `ref/` base as the standing citation ground-truth (S, S) — surfaced 2026-06-27 (scratch-review S-5/S-11/S-12) (was 4.22)

The scratch `grc_library_scratch/ref/` base is now the maintainer's standing reference for every task (per the `/resume` Reference-knowledge-base step and the [`multi-session-orchestration`](.working/multi-session-orchestration.md) runbook §6), but no corpus-facing spec tells an author "verify a citation against `ref/`, here is the trust model, here is the proprietary-no-redistribute rule". The [`specification-citation-verification.md`](governance/specification-citation-verification.md) and the [`register-canonical-citations.md`](governance/register-canonical-citations.md) Maintenance section both predate the ref base. Add a short pointer in one of those (S-11) describing `ref/` as the local verification source, its trust tiers (`standards/` > `frameworks/` > `publications/`; `legislation/`/`programs/` authoritative-in-domain; `templates/` scaffolding), and the proprietary-no-redistribute constraint. Also record (S-5) that the `/matrix-fit` reference base for control-title lookups is the `ref/` CCM/AICM CSVs + CSF OSCAL (+ the ISO Annex A title map once S-4 lands), so the cadence is reproducible rather than memory-bound. Minor follow-on (S-12, FYI): the 16 ISACA policy templates in `ref/templates/` are usable as structural scaffolding for template-type corpus docs, trusted issuer but proprietary, adapt-don't-copy. This pairs with §4.5 (the fork-facing mirror of the same model).

### 3.10 TODO-hygiene completion pass + accretion guard (S, S) — surfaced 2026-06-27 (was 4.23)

The maintainer flagged (2026-06-27) that shipped/historical content had accreted in TODO instead of rotating out. Parts (a) and (b) shipped in the TODO-hygiene PR: (a) §3.6 (multi-session orchestration) trimmed to its residue (deliverable 4, the worker-provenance gate; deliverables 1-3 shipped) after verifying against the gate inventory of the time; (b) the unambiguous shipped/closed clauses deleted (the Queueing-rules "FR-166/DD-1/DD-9 already shipped" note, the P3-intro "B2 closed #408 / DD-12 closed" parenthetical, the §1.3 "actioned in #275" line, the §3.7 "D4 shipped in #366" clause, the Backlog-totals "closed in #N" clauses).

**Remaining (open):** (c) **whether the `## Standing conventions`, `## Backlog totals`, and `## Priority 7` (audit-trail-only) sections belong in TODO at all** or in a conventions / design-decisions doc. This is a **maintainer call** (they are non-forward-looking but appear intentionally retained); filed for decision in `## Priority 7`. The **accretion guard** is the TODO/DONE-rotation gate family, now shipped (gate 57 catches in-place self-marking; the D5 PR-time check catches a wholesale-forgotten rotation when a PR's CHANGELOG asserts a backlog-item closure). A possible extension (consider) is teaching gate 45 to flag shipped-PR-number history accreting inside an open TODO item, so accretion is mechanically prompted rather than convention-only.

### 3.11 Wind-down / overnight-mode SOP refinements (S, S) — maintainer-directed 2026-06-28 (was 4.25)

Two maintainer-directed refinements to codify in the `## Wind-down decision framework`, `## Attended-autonomous operating mode`, and overnight-protocol sections of [`.claude/CLAUDE.md`](.claude/CLAUDE.md) (a focused PR; flagged "not urgent, handle later today"). Effective behaviorally on direction; codification queued here.

1. **Overnight-mode toggle is not a no-answer default.** Do NOT decide to turn off overnight mode unless the maintainer explicitly says so, or (if unsure) pause and ask. If no answer arrives in the ~2-minute graceful-degradation window, **MAINTAIN overnight mode** and re-ask the next time the maintainer messages. This carves the overnight-OFF decision out of the general wind-down no-answer-to-handoff default (a handoff silently ends overnight mode, the recurrence the maintainer flagged after the #425 wind-down default ended the overnight run while they were briefly up).
2. **Continue-as-default while quality holds, even when context is heavy.** Heavy context alone is NOT a wind-down trigger; the decision is evidence-based, not inference. The only exception is a run of expected chained large PRs where historical metrics show quality is likely to suffer very soon. Adjust the self-assessment SOP so context-heaviness is not treated as a quasi-trigger.

### 3.12 CLAUDE.md removal-ledger review cadence (standing) — added 2026-06-28, PR #441 (was 4.27)

The PR #441 condense of [`.claude/CLAUDE.md`](.claude/CLAUDE.md) moved the cut rationale, war-stories, and provenance into [`.working/claude-md-considerations.md`](.working/claude-md-considerations.md) (the removal ledger), each entry carrying an "evidence the removal was wrong" signal. Standing activity (not a one-time task): each `/retro` does a quick scan of the ledger's open RM entries and the periodic hallucination-metrics pass does a deeper one; if an entry's signal appears, advise the maintainer to restore the cut text or make a new CLAUDE.md change, and record the disposition in that entry's Status. Wired into [`.working/improvement-log.md`](.working/improvement-log.md)'s Convention section. This item is the durable tracker so the cadence is not lost; it stays open by design.

### 3.13 CLAUDE.md-optimization diagnostic skill (L, S) — maintainer-directed 2026-06-28, low priority (was 4.28)

Decision (maintainer 2026-06-28, after the PR #441 condense): the keep-and-condense method is documented as pack guidance ([`guidance-claude-md-optimization.md`](dev-security/claude-rules/guidance-claude-md-optimization.md), shipped 2026-06-28); a full optimization skill was declined as too judgment-heavy to mechanize (the keep-versus-cut call is exactly the part a skill cannot do). The tractable mechanical aid is a NARROW read-only diagnostic, a `/claude-md-audit`-style reporter over a target rules file that surfaces file length, section count, an actionable-token-density heuristic (ratio of greppable rule tokens such as commands, paths, gate numbers, and thresholds to total prose), and a "no removal ledger referenced" flag. Advisory output only, never a gate (the keep/cut decision stays the maintainer's). Low priority: build only if the guidance doc proves insufficient on its own. Pairs with the §3.12 ledger-review cadence.

### 3.14 Gate-2 coverage of generator emitted-prose strings (L, S) — surfaced 2026-06-30 (Sweep 78 B-1)

Sweep 78 found a Commonwealth `customised` hard-coded in a [`tools/build-portal.py`](tools/build-portal.py) emitted-prose string (rendered into the `GENERATED_DOCS`-exempt [`docs/portal.md`](docs/portal.md)), doubly blind to gate 2 ([`tools/lint-language.py`](tools/lint-language.py)): the gate scans only `.md` files (so the `.py` generator source is never seen) and excludes the generated output. The `-ize`/dash/house-style house rules therefore do not reach the adopter-facing prose the `tools/build-*.py` generators emit. Candidate: extend gate 2 (or add a narrow sibling check) to scan the emitted-prose string literals in the `tools/build-*.py` generators, so a house-style violation in generator-authored prose is caught at gate time rather than at the next corpus-wide `/validate`. Low priority (the generators are few and their prose is small); pairs with the §1.4 audit-gate work. The companion non-tooling residual (gate-exempt `.claude/` forward `§`-pointers left stale by a TODO renumber) needs no new rule, it is the existing section-close cross-FILE cleanup close-out-checklist line, to be reinforced to span gate-exempt forward pointers when that line is next edited.


---

## Priority 4 — Adopter experience

Capability and guidance for organisations adopting the library, and the operator-experience tooling for running the project. Scheduled deliberately, after the fix/gap/cleanup tiers.

### 4.1 Corpus-management discipline as a shareable skill (M, XL)

Package the cumulative documentation-and-corpus discipline this project has accumulated as a standalone Claude Code skill that anyone managing a documentation corpus with an AI coding assistant could install.

- **Distillation source**: the twelve `governance/` pack rules form the discipline core; `validation-sweep` and `library-fitness-review` form the periodic-review surface; the audit-programme architecture forms the mechanical-enforcement surface.
- **Generalisation**: carry the patterns and discipline without the GRC-specific control-set citations; adopters supply their own document-type model and metadata-field set.
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

Per maintainer direction 2026-06-22 (low priority, after the FR backlog completes). The corpus uses the 5-tier maturity-level scale at both organisation-wide and per-domain granularity; CMMI distinguishes the two (maturity levels 1-5 org-wide; capability levels 0-3 per practice area). Introducing capability levels would: (1) add a capability-level scheme to [`governance/framework-governance-performance-and-improvement.md`](governance/framework-governance-performance-and-improvement.md) §2; (2) update [`docs/template-maturity-self-assessment.md`](docs/template-maturity-self-assessment.md) to use capability levels per domain and aggregate to maturity levels at the programme rollup; (3) possibly extend [`governance/register-digital-trust-and-assurance-metrics.md`](governance/register-digital-trust-and-assurance-metrics.md) DTI thresholds with a capability-level surface.

### 6.5 Multi-cloud governance overlay (XL) (was 6.1)

Per-cloud hardening baselines for AWS, Azure, and GCP exist in `dev-security/`. The remaining gap is multi-cloud governance (cross-cloud risk taxonomy, cross-cloud incident coordination, cloud-portfolio-level controls). Could live in `operations/` or warrant a new `cloud/` domain.


---

## Priority 7 — Awaiting maintainer decision

One open decision pending (§3.10(c), the TODO audit-trail-only sections question). The FR-104 / FR-130 entries are dropped-decision audit-trail records (see [`.working/design-decisions.md`](.working/design-decisions.md)).

### 7.1 Do the audit-trail-only sections belong in TODO? (§3.10(c))

Do the audit-trail-only sections (`## Standing conventions`, `## Backlog totals`, `## Priority 7`) belong in TODO at all, or in a conventions / design-decisions doc? They are non-forward-looking but appear intentionally retained. Maintainer call; left in place pending the decision.

### 7.2 Per-regulation context (FR-104)

Per-regulation context not pursued.

### 7.3 Portal reorder (FR-130)

Portal reorder not pursued (README stays at decision-tree item 1).

---

## Standing conventions

Durable behavioural guidance from the maintainer. NOT actionable items; reference material for the orchestrator and future contributors.

- **"More PRs, keep each one clean"** — favor small focused PRs.
- **"I prefer /validate, not /validation-sweep"** — short slash commands; skill names stay descriptive.
- **"Don't explicitly name or link `.working/`"** in template-content files that adopters see.
- **"Inference must be validated before committing or before anything else uses that information"** — operationalised in [`validate-inference-before-action.md`](dev-security/claude-rules/governance/validate-inference-before-action.md).
- **Activity directories should be self-contained** — operationalised in the canonical `.working/<activity>/` layout.
- **Zero-finding sweeps still need history rows but no detail files** — operationalised in the validation-sweep [`SKILL.md`](dev-security/claude-rules/skills/validation-sweep/SKILL.md) step 9.
- **Sweep history is project-application, not template content** — operationalised by keeping the history file in `.working/`.
- **TODO is forward-looking; historical state rotates to DONE.md** — operationalised in [`change-tracking.md`](dev-security/claude-rules/governance/change-tracking.md) PR-finalization-protocol section.
- **After completing a merge, list the upcoming next 5 planned PRs from TODO** — operationalised in [`.claude/CLAUDE.md`](.claude/CLAUDE.md) PR-workflow section and the same pack rule.
- **Validate cadence is 1-8 PRs per batch, not strictly 5** — the 5-PR cadence is default; the batch boundary is chosen at the natural seam.
- **DONE format mirrors TODO format** — DONE H3 headings carry `FR-N (severity)` so the two ledgers are scannable in the same shape. Harmonised in PR #163.
- **Compute-don't-ask** (maintainer-flagged 2026-06-23) — before surfacing a question, apply a "can I compute/verify this myself?" gate; surface the result, not the raw question. (Codified 2026-06-30 into the `clarify-before-acting` rule's compute-first gate, #504.)

---

## Backlog totals

Approximate active counts after the 2026-06-30 work-type re-tier and renumber (the priority sections themselves are the source of truth; these drift).

- **P1 (fix errors and prevent recurrence)**: 5 items (1.1 FR-48, 1.2 Per-document ISO, 1.3 retro guard rails, 1.4 audit-gate candidates, 1.5 reference version-currency).
- **P2 (fill significant gaps)**: 11 items (2.1-2.10 the FR deepenings FR-59 / 60 / 70 / 99 / 15 / 23 / 63 / 74 / 154 / 41, plus 2.11 publications-assessment).
- **P3 (clean up and tooling)**: 14 items (3.1-3.14).
- **P4 (adopter experience)**: 5 items (4.1-4.5).
- **P5 (expand: country / regulator / programme overlays)**: 9 items (5.1-5.9).
- **P6 (expand: new domains)**: 5 items (6.1-6.5).
- **P7 (awaiting decision)**: 1 pending (7.1) + 2 dropped-decision audit-trail entries (7.2 / 7.3).

---

## Notes on maintenance

- Add new items at the appropriate priority; within a section keep the lowest-effort-first ordering. Move items between priorities as context changes.
- When an item is completed, delete it from this file (no strikethroughs, no `[done]` suffixes) and add an entry to [`.working/DONE.md`](.working/DONE.md) in the same PR. The rotation discipline is documented in the PR-finalization-protocol section of [`.claude/rules/governance/change-tracking.md`](.claude/rules/governance/change-tracking.md).
- Design decisions belong in [`.working/design-decisions.md`](.working/design-decisions.md), not in TODO. The P7 "dropped-decision" entries cross-reference those decisions for audit-trail completeness without duplicating the rationale.
- This file is the source of truth for what's queued; conversation history is not.
- Fitness-review backlogs remain the authoritative per-finding evidence source; this file is the action-organized view, kept in sync at fitness-review-cycle time.
