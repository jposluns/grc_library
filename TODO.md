# TODO

Forward-looking backlog of planned enhancements for the GRC Documentation Library. Items are added when identified and rotated out when completed. Completed items move to [`.working/DONE.md`](.working/DONE.md) (closed-TODO ledger, keyed by original backlog ID); historical change detail lives in [`CHANGELOG.md`](CHANGELOG.md). This file holds only pending and queued items.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions, with one narrow exception: [`tools/lint-todo-staleness.py`](tools/lint-todo-staleness.py) (gate 45) scans this file for the queued-PR-already-merged drift shape (its companion sweep-cursor-behind-history check now reads the resume cursor from [`.working/session-handoff.md`](.working/session-handoff.md), where the former `## Session resume metadata` block was relocated so TODO stays purely forward-looking). All other audit gates skip this file.

Items are organised by priority (P1-P7). Within each priority section, items are listed **lowest-effort-first → highest-effort-last** (the maintainer's 2026-06-23 ordering directive). Each item carries its identifier (FR-N, DD-N, or descriptive ID), a tag in the form `(severity, effort)` where severity is `H[critical]` / `H` / `M` / `L` / `FYI` and effort is `XS` / `S` / `M` / `L` / `XL` (per the scale in 4.2), and a one-line description plus the location reference. Effort labels added in the 2026-06-23 restructure for items that previously lacked one are first-pass estimates, to be calibrated in review. A `⚠` marks a persona-quoted finding to verify at action time.

---

## Queueing rules

- Orchestrator picks the next batch from **Priority 1 first, then Priority 2**, in highest-severity order; within a chosen section the effort ordering helps assemble like-effort batches.
- **1-8 PRs per batch** (logical grouping); `/validate` after each batch.
- Maintainer direction supersedes the orchestrator's pick at any time.
- Lower priorities (P3-P7) are picked deliberately, not from the routine batch queue, unless the maintainer triggers them.
- **Maintainer-directed running order (2026-06-23)**: (1) **FR-167** (comprehensive matrix; top substantive priority); (2) then the **deferred-decision work** (DD-2..DD-12, now queued as ordinary items in P2/P3); (3) then **reduce the backlog by treating the smallest items in batches**, using 10+ well-briefed research-assistant agents (workers produce verified research from briefs built off [`.working/worker-brief-template.md`](.working/worker-brief-template.md); the orchestrator re-verifies every worker claim at apply-time and authors all final prose).
- **Maintainer-directed next phase after the XS/S batch (2026-06-24)**: once the XS/S batch is complete (PR-I, PR-J, PR-K1, PR-K2, the FR-144 template), pivot to an **integrity-tooling / guard-rails phase**: codify the queued retro guard rails (§4.8 — the orchestrator-side apply-time disciplines: bare-token contradiction search, parallel-case verification, compute-don't-ask, new-skill-drafting checklist, the README/ledger Date-on-version-bump line from #295's `/retro`), build the new gates (§4.5 S3, §4.6 QA-cadence mechanical gate, §4.10 TODO/DONE rotation gate), and add any further validations/checks that keep the orchestrator meticulously consistent and assure integrity. The metrics recompute (#295) makes the case concrete: worker hallucination is controlled, and the active failure class is now orchestrator-side multi-surface incompleteness, which is exactly what this phase's gates/checks would catch mechanically.

---

## Priority 1 — Urgent quality (High[critical] and High severity)

The trust-recovery suite findings (signed off 2026-06-22) and the deferred-decision items are integrated here and in P2/P3 by severity; full evidence lives in [`.working/full-qa/2026-06-22-iter1.md`](.working/full-qa/2026-06-22-iter1.md) and [`.working/fitness-reviews/2026-06-22-r2.md`](.working/fitness-reviews/2026-06-22-r2.md). The six H[critical] FR-134..139 and the High FR-141 already shipped (see [`.working/DONE.md`](.working/DONE.md)).

- **FR-73 (H[critical], M)**: Separate AI ethics review from the compliance/risk body in [`ai/charter-ai-governance-council.md`](ai/charter-ai-governance-council.md); introduce an independent ethics panel or challenge mechanism.
- **FR-58 (H, M)**: Define inheritance vocabulary (library-internal vs template vs reference content); multiple documents are inconsistent on what kind of content is being referenced. **Decided (maintainer 2026-06-25): apply the canonical 3-label scheme corpus-wide** (`library-internal` = cross-references between library documents; `template` = adopter-fillable content; `reference` = external-standard / source content cited, not authored), with per-document apply-time verification; surface any document that does not fit cleanly.
- **FR-145 (H, M) ⚠**: Two AI security standards have overlapping scope with no precedence/crosswalk — [`ai/standard-ai-security-and-risk.md`](ai/standard-ai-security-and-risk.md) vs [`ai/standard-ai-and-agentic-development-security.md`](ai/standard-ai-and-agentic-development-security.md). Decided (maintainer 2026-06-23): keep both; add a scope/precedence note + a crosswalk table (verify exact overlap at action time before authoring the precedence statement). **Reference-base aid (2026-06-27 scratch-review S-10)**: the scratch `grc_library_scratch/ref/CROSSWALK.md` registers source-cited cross-framework mappings already held (ISO/IEC 27701<->GDPR, ISO 27001 Annex A<->27002, COBIT<->CSF, plus untrusted DORA<->ISO and AIUC-1<->OWASP-Agentic to corroborate before use); consult it when authoring this crosswalk rather than reconstructing from memory.
- **FR-31 (H[critical], L)**: Ship `privacy/framework-privacy-by-design.md` operationalising GDPR Article 25 by mapping the seven foundational privacy-by-design principles to architecture and dev-security workflows.
- **FR-32 (H[critical], L)**: Ship `privacy/template-legitimate-interest-assessment.md` (LIA) covering the three-part balancing test (purpose, necessity, balancing) per Article 6(1)(f).
- **FR-34 (H[critical], L)**: Ship `privacy/template-transfer-impact-assessment.md` covering the EDPB Recommendation 01/2020 six-step methodology. Consolidates with FR-74.
- **FR-71 (H[critical], L)**: Ship a dedicated M&A due-diligence procedure. `procedure-grc-programme-management-and-annual-review.md` names M&A as a trigger but has no checklist, pre-close template, or integration playbook.
- **FR-72 (H[critical], L)**: Ship a dedicated sanctions / OFAC / export-control framework with UBO (ultimate-beneficial-owner) verification and denied-party-list integration. Current treatment is superficial.
- **FR-59 (H, L)**: Privacy jurisdiction annexes are too shallow for operational sufficiency; deepen the 25 country annexes to operational level. **Reference-base aid (2026-06-27 scratch-review S-7)**: `grc_library_scratch/ref/legislation/` now holds primary-source full-text for Japan APPI, Virginia VCDPA, Colorado Privacy Act, and the LATAM laws (Mexico, Brazil, Argentina, Colombia, Uruguay); author the deepening against those held sources. Honest caveat: APAC beyond Japan (Singapore, Australia, Korea, China, India) remains maintainer-drop (absent from the ref base).
- **FR-60 (H, L)**: HIPAA adopter has no operational detail beyond a single 261-line sector annex in `compliance/healthcare`. Deepen.
- **FR-61 (H, L)**: Financial-services adopters outside EU/US lack regulatory regimes: UK PRA/FCA, US OCC/FRB/FDIC, MAS, FSA, APRA, OSFI, HKMA, FINMA.
- **FR-167 (H, L)**: Expand [`compliance/matrix-grc-compliance-alignment.md`](compliance/matrix-grc-compliance-alignment.md) to **comprehensive** coverage across all 8 framework columns (CSA CCM v4.1 / ISO 27001:2022 / NIST CSF 2.0 / CTPAT / PIP / BASC v6 / WCO SAFE / AEO-S), honest N/A where a customs/trade column does not apply; the orchestrator authors and verifies every cell at apply-time (a wrong control mapping is not gate-caught). **All 11 per-domain batches have shipped** (architecture through privacy, #275 to #404; see [`.working/DONE.md`](.working/DONE.md)). **The CSA AICM v1.1 column SHIPPED in PR-B** (the maintainer-decided 2026-06-28 structural addition; AICM v1.1 is CSA's AI-focused extension of CCM v4.1, so the column carries only the AICM-only AI-specific delta): 68 AICM-only-coded rows / 261, `N/A` elsewhere; gate 49 (extended in #447) validates the column; semantic fit verified by a two-verifier adversarial pass (Verifier A caught 9 misses among the title-based `N/A`s; Verifier B confirmed/tightened every code against the AICM titles, 3 tightenings) plus a deterministic rendered-cell re-parse (0 mismatches). **Remaining for FR-167 closure** (FR-167 stays OPEN until these land): the [`tools/audit-matrix-semantic-fit.py`](tools/audit-matrix-semantic-fit.py) AICM-scoping extension **SHIPPED** (PR-C: `KNOWN_TITLES` now loads `AICM_V11` so the 40 AICM-only titles are assessable; `scan_matrix` reads the "CSA AICM v1.1" column; the inline self-test gained two AICM cases; the closing-audit worklist is 62 rows). (a) run the formal tool-driven **closing whole-matrix `/matrix-fit`** (the matrix-completion close-check) over that 62-row worklist; (b) **matrix gap-fill**, add rows for any substantive corpus document not yet in the matrix (the "comprehensive coverage" goal; the matrix is a living document per its coverage summary). The earlier 8-column comprehensive coverage across all 11 per-domain batches shipped #275 to #404.
- **FR-144 (H, L)**: Breach individual-notification has no internal clock, and each regulator's requirement differs. Create an adopter-fillable breach-notification regulator register template (per-regulator: jurisdiction, authority, trigger, regulatory deadline, individual-notification requirement, internal target) and wire it into [`privacy/procedure-data-protection-and-privacy-breach-response.md`](privacy/procedure-data-protection-and-privacy-breach-response.md) §6 so the organization acts within the strictest applicable requirement. (Re-scoped 2026-06-23 from a fixed internal clock to a register template, per maintainer direction.)
- **FR-70 (H[critical], XL)**: New domain for crypto-asset / blockchain governance — digital-asset custody, staking, smart-contract risk, blockchain platform vetting. Regulatory references: DORA, MiCA, NYDFS BitLicense. (Cross-references P6.x for domain-level shaping.)

---

## Priority 2 — Substantive improvements (Medium severity)

Individual documents or focused multi-doc improvements. The deferred-decision items DD-2..DD-8 (maintainer-triaged 2026-06-23) and the Medium trust-recovery findings are integrated here. Research files for queued clusters are prepared in advance per the research-assistant discipline in [`ai-assistant-workflow-disciplines.md`](.claude/rules/governance/ai-assistant-workflow-disciplines.md).

- **FR-62 (M, S)**: AI jurisdiction annexes absent. (Cross-references P5.8.) **Reference-base aid (2026-06-27 scratch-review S-8)**: `grc_library_scratch/ref/legislation/` holds the Colorado AI Act and EU AI Act full-text, and `ref/frameworks/ETSI/` holds the Securing-AI TR/GR set + EN 304 223 (AI baseline); ground the US-state and EU AI-annex authoring in those held sources.
- **FR-99 (M, M) ⚠**: Per-control effectiveness metrics (continuous assurance / 3LoD).
- **FR-15 (M, M)**: Maturity-ladder methodology — median-of-medians scoring concern.
- **FR-23 (M, M) ⚠**: Audit-evidence assembler-verification standard absent.
- **FR-24 (M, M)**: Control-testing procedure thinner than peers.
- **FR-63 (M, M)**: Worked example walks ingestion not adoption.
- **FR-74 (M, M)**: Schrems II-light treatment. Consolidates with FR-34 (Transfer Impact Assessment, P1).
- **FR-154 [fitness:P6] (M, M) ⚠**: Operational-vagueness cluster: DSR forward immediate-vs-same-day ([`privacy/procedure-data-subject-rights-management.md`](privacy/procedure-data-subject-rights-management.md):52/:84); DSR restriction clock start (:70); critical-risk interim authority ([`risk/procedure-risk-assessment-methodology.md`](risk/procedure-risk-assessment-methodology.md):124); supplier remediation gate ([`supply-chain/procedure-supplier-due-diligence.md`](supply-chain/procedure-supplier-due-diligence.md):85); whistleblower timelines ([`governance/procedure-whistleblower-and-incident-reporting.md`](governance/procedure-whistleblower-and-incident-reporting.md):103); dept-continuity template blanks; incident-reporting escalation thresholds; model-lifecycle thresholds. **Decided (maintainer 2026-06-25): deepen all of the thin-baseline cluster** (FR-15, FR-23, FR-24, FR-63, FR-74, FR-99, FR-154) to operational depth; this overrides the earlier "calibrate first, several are deliberately-thin baselines" guidance.
- **FR-41 (M, L)**: AI Article 22 + EU AI Act + FRIA dual/triple-compliance workflow not documented as a unified workflow. (Privacy completion; FR-37/38/39/40/42 closed in #224-#228.)
- **FR-48 (M, L)**: H2 numbering patterns drift — multi-doctype structural rename. Deferred until a dedicated session is scheduled.

---

## Priority 3 — Low-priority cleanup (Low severity / FYI)

Deferred to a routine cleanup batch when convenient. The Low/FYI trust-recovery findings and the decided low-severity deferred decision DD-10 are integrated here.

- **ERC acronym expansion inconsistency, RESIDUAL (Low, S), bulk reconciled in #456; one semantic edge remains**: the corpus drift between "Enterprise Risk Committee" and "Executive Risk Committee" was bulk-reconciled in #456, which canonicalized all 10 clearly-drifted occurrences across 9 documents to "Enterprise Risk Committee" (the glossary canonical, the `ERC` entry in [`governance/register-glossary.md`](governance/register-glossary.md); the drift was confirmed same-body by the table-vs-prose pattern). **Remaining (authorial judgment, NOT a blanket replace):** [`governance/guideline-minimum-viable-governance-structure.md`](governance/guideline-minimum-viable-governance-structure.md) still uses "Executive Risk Committee" at its Tier-1 table (line 58, a spurious duplicate of the "Enterprise Risk Committee" library-forum row 59) and its Tier-2 consolidation mapping (line 80, "Executive Committee | Executive Management, Executive Risk Committee, Audit Committee ..."), where a blind canonicalization would create a contradiction with the adjacent Enterprise-Risk-Committee row (81) or a redundant duplicate row. This doc's tier-consolidation tables need an authorial pass: decide whether the Tier-1 spurious row collapses into the Enterprise row, and whether the Tier-2 "Executive Risk Committee" is a drift for "Enterprise Risk Committee" or an intentionally distinct consolidated-body label, then reconcile. Left for maintainer judgment (do not silently merge what the tier tables may treat as distinct).
- **Sweep 3 follow-up (L, S)**: Cross-document term-and-identifier consistency gap (the prose-and-numbering C3 surface mechanical gates 35/39/41 don't cover). Candidate for a future mechanical gate; a manual sweep closes the open items meanwhile.
- **CHANGELOG detailed-mirror per-PR-header parity check (Low, S) — surfaced 2026-06-27 (`/full-qa` finding F-1)**: the detailed CHANGELOG mirror can lose a per-PR `##` header when a later PR's commit overwrites the prior header in place (PR #388 orphaned the #386 and #387 bodies under #388; fixed in PR #392). Delta gate D1 checks per-commit root+detailed lock-step *presence*, not cross-commit header integrity, so the class is gate-blind. Consider a mechanical check asserting the detailed mirror's per-PR `##`-header set equals the root [`CHANGELOG.md`](CHANGELOG.md)'s. Low; pairs with the next CHANGELOG-gate edit.- **Per-document ISO Annex A code validation (L, M) — deferred follow-up to the gate-49-extension track (maintainer-confirmed 2026-06-26)**: extend [`tools/lint-document-control-codes.py`](tools/lint-document-control-codes.py) (gate 54, NIST CSF 2.0 only) to also validate ISO/IEC 27001:2022 Annex A codes (and clause refs) where they appear in per-document framework-reference / crosswalk tables, reusing gate 49's `check_iso_token` logic. Deferred from the gate-54 build because per-document ISO codes are higher-false-positive (clause refs `§10.2`, ranges `A.5.19 to A.5.22`, mixed editions) and the matrix's ISO column is already covered by gate 49; scope a precision-first design before building. **Reference-base aid (2026-06-27 scratch-review S-4)**: the chief blocker the matrix-fit aid records ([`tools/audit-matrix-semantic-fit.py`](tools/audit-matrix-semantic-fit.py):54 "ISO 27001:2022 codes are not assessed (no title source in the repo)") is now addressable: `grc_library_scratch/ref/standards/ISO/` holds the ISO/IEC 27001:2022 Annex A + 27002:2022 control-title extracts. A maintainer-local ISO Annex A title map (proprietary: cite by clause, do not commit the verbatim titles if licence-sensitive) would let both gate 54 and `/matrix-fit` assess ISO-column rows. Licence-handling of the proprietary titles is a maintainer decision.
- **Citation-verification pass against the scratch `ref/` base (Low, M) — surfaced 2026-06-27 (scratch-review S-2/S-3/S-9)**: the scratch `ref/standards/` (ISO/IEC, NIST, ETSI) and `ref/frameworks/` (COBIT 19 docs, CSA CCM/AICM CSVs, MITRE, OWASP) now hold full-text / control-catalogue extracts for many [`register-canonical-citations.md`](governance/register-canonical-citations.md) rows. Run a verification pass confirming the register's ISO / NIST / CSA / COBIT version+date rows against the now-held local extracts (per [`governance/specification-citation-verification.md`](governance/specification-citation-verification.md)), recording results in the Citation Verifications Register. This is a local-ground-truth substitute for the previously egress-blocked verification. Sub-decision: whether to add ETSI rows to the register (EN 303 645 consumer IoT, EN 319 401 trust services, held in `ref/standards/ETSI/`) — the register currently lists no ETSI; maintainer call on scope.
- **`docs/` house-style (em/en-dash) enforcement gap (Low, S) — surfaced 2026-06-29 (Sweep 76, Finding 2)**: `docs/` authored prose carries 71 em/en-dashes across 4 files ([`docs/decision-tree.md`](docs/decision-tree.md) 58, [`docs/adopter-guide.md`](docs/adopter-guide.md) 5, [`docs/template-quickstart.md`](docs/template-quickstart.md) 4, [`docs/template-implementation-roadmap.md`](docs/template-implementation-roadmap.md) 4), which violate the CLAUDE.md house-style ("em-dashes and en-dashes are forbidden in prose") but sit outside [`tools/lint-language.py`](tools/lint-language.py)'s path scope (its `main()` default set is `AUDITED_DOMAIN_DIRS` + named files, not `docs/`), so gate 51-class dash enforcement never sees them. **Maintainer-decided 2026-06-29: Option A** (the long-term solution, "always go with the long term best solution rather than a one time fix"): extend the dash check to cover `docs/` (close the gate-blind path-scope gap permanently) AND fix all 71. Queued as a PR after the §4.10 complementary check. Design: either widen [`tools/lint-language.py`](tools/lint-language.py)'s default path set to include `docs/`, or add `docs/` to the gate-51-class working-prose/dash scope; fix all 71 em/en-dashes across the 4 files in the same PR (with the per-document Version/Date bumps the touched `docs/` files need). Out-of-window (pre-existing); routed per the `/validate` out-of-window protocol.

---

## Priority 4 — Adopter experience (process and meta improvements)

Items that affect how the library is used, evolved, or extended. Not direct corpus content changes. The `4.N` numbers are **stable ids** (referenced from the handoff, retro log, and CHANGELOG), not sequence positions; the subsections below are ordered lowest-effort-first per the 2026-06-23 directive.

### 4.8 Retro-log open-loop consolidation (S, S) — surfaced 2026-06-23

A review of [`.working/improvement-log.md`](.working/improvement-log.md) found that the **convention/checklist layer** absorbs retro candidates well (lint-language pre-flight, grep-after-convention-change, CHANGELOG-link front-loading are codified in the CLAUDE.md close-out checklist and holding), but the **mechanical-gate and rule-codification layers** accumulate "queued, apply next time" candidates that do not self-clear. Still open (action deliberately, not at a long-turn tail):

- **Codify the orchestrator-side apply-time disciplines into the pack layer**: (a) **bare-token contradiction search** (#261/#262 — search the bare token for a changed concept, inspect+classify each hit, never state a corpus-wide completeness claim from a phrasing-specific search); (b) **parallel-case verification scope** (#271 — when an edit rewrites a clause enumerating parallel cases, re-verify EVERY enumerated case). Candidate homes: the CLAUDE.md close-out checklist and/or `ai-assistant-workflow-disciplines.md` §3.
- **Codify compute-don't-ask** (#269) into the `clarify-before-acting` rule's "ask vs default" test — it currently distinguishes ask-vs-sensible-default but not ask-vs-self-compute.
- **New-skill-drafting checklist** (#213) — enumerate the parallel surfaces (link depths, pack-README skills-table row, PAIRS registry, language pre-flight, slash-command sibling).
- **Broaden the count gate (remainder)**: gate 39 P8 closed "N automated audits" (#273); still open are word-form counts ("forty-six") via a word→number map and the free-prose rule-count gate (gate 41 can't parse "the N governance rules").
- **Corpus-wide-scrub narrative-surface scope** (#320 `/retro`): when scrubbing a fact corpus-wide (a terminology/regime/version rename), the scrub must scan the **narrative and currency-summary surfaces** (update-summary bullets, status notes, prose) of EVERY touched file for the same fact, not only the structured lists/tables. #320's DD-8 CPPA→PIPEDA scrub edited `privacy/annex-privacy-jurisdiction-index.md`:45 (a framework-list row) but missed :133's "2026 Update summary" bullet asserting Bill C-27 "Remained under parliamentary study as of early 2026" (contradicts the lapsed-2025 consensus the scrub itself asserts); `/validate-pr` caught it (fix bundled into the next PR). Sweep 41 then found a **third** carrier in the same file, :102's cross-jurisdiction summary row ("adequacy under CPPA"; "CAD 25M / 5% revenue (CPPA)"), a structured-table surface (not just narrative) the #320 scrub also missed, reinforcing that the scrub-completeness scan must cover every surface of a touched file (structured tables AND narrative), not stop at the first list edited. Same multi-surface-incompleteness class as the gate-behaviour item below. Candidate homes: the corpus-wide-scrub worker-brief and the CLAUDE.md close-out checklist.
- **Version-bump artefact-regen-order checklist line** (#323 `/retro`, **3rd instance, earns the line**): after any per-document `Version` bump, regenerate `taxonomy.yml` **FIRST**, then `docs/portal.md` + `docs/maturity-scorecard.md` (the latter two derive from taxonomy); do **not** trust a `tools/build-portal.py --check` taken before the taxonomy regen completes (it returns a false-clean against the stale taxonomy). Recurring friction: #318 gate-33 amend loop, the #317/#318 retro candidate, and #323's gate-34 post-commit catch (the scorecard tracks per-doc Version). Caught post-commit each time (nothing reached CI), but the amend loop is avoidable. Candidate home: CLAUDE.md `## Version-bump discipline` (the four-question operationalization) + the worker-brief template.
- **Gate-behaviour-changed paired-surfaces checklist item** (#312 `/retro`): when a linter's detection logic changes, the [`governance/specification-audit-programme.md`](governance/specification-audit-programme.md) §6 narrative for that gate is a REQUIRED parallel surface alongside the module docstring and the regression tests, updated in the same PR. Sweep 38 found the §6 gate-48 prose still said "checks two things" after #308/#309 enhanced the linter+docstring+tests to four checks (F3). A mechanical docstring-vs-spec sync check is hard on free prose; the cheap guard is a CLAUDE.md close-out-checklist line (candidate home) until §4.6's QA-cadence gate family lands. This is another instance of the orchestrator-side multi-surface-incompleteness class §4.8 tracks.
- **Full-file-grep-for-prose-fact-corrections checklist line** (#340 `/retro`, the **3rd consecutive multi-surface-incompleteness occurrence** #336→#338→#340): the CLAUDE.md close-out checklist's "grep the OLD phrasing across the full changed file AND every sibling surface" line is currently framed for convention/count/routing-rule changes; extend it to explicitly cover prose-**fact** corrections (a stale claim, an overstatement, a superseded fact), and require greping the FULL touched file (every line and string: comments, docstrings, assertion messages, prose) for the offending phrase with zero residual confirmed BEFORE commit, rather than editing the named lines the orchestrator recalled. #340 missed a 4th carrier of an overstatement in the same test method it was explicitly correcting (the assertion failure-message string), because the find-every-carrier fix targeted named lines not a phrase grep; `/validate-pr` caught it. For ungated prose this discipline IS the backstop; it pairs with the queued directory-scan-scope parity meta-check above for structured scan-scopes. Candidate home: the CLAUDE.md `## Session migration and PR close-out checklist` grep line.

### 4.2 Backlog effort-sizing labels convention (M, S)

Backlog items now carry `(severity, effort)`; this item formalises the convention. Proposed scale:

| Label | Per-item effort | Bundleable per PR |
|---|---|---|
| **XS** (single-line / single-cell) | 5-15 min | 5-10 items |
| **S** (single-doc section add) | 30-90 min | 2-4 items |
| **M** (multi-doc, bounded) | 2-4 hrs | 1 item |
| **L** (new artefact, multi-doc propagation) | 4-8 hrs | 1 item |
| **XL** (new domain, library-wide reshape) | 1-3 days | 1 item, may split |

**Surfaces to update when the convention formally lands**: `library-fitness-review/SKILL.md`; `validation-sweep/SKILL.md`; this file (already in use); `.working/DONE.md` heading shape; future fitness-review templates and sweep detail files. Schedule: after the current FR backlog closes.

### 4.5 Audit-gate candidates from the 2026-06-22 review (M, S each)

Decided 2026-06-23 (maintainer triage): **build them all** from the 2026-06-22 review. **S3 remains** (the only open item in this section); the original S1 retention-consistency gate shipped in #462, S2 was closed in #463 as a register consolidation (the role-consistency check already existing as gate 8 `lint-roles.py`), and **S4 (no-bare-normative-`shall`) shipped in #466** (gate 56). Each is a `lint-*.py` + 4-surface wiring + regression fixture; one gate per PR to keep diffs reviewable.

- **S3 Citation-precision-for-claim gate**: flag "aligned with [normative source] X" claims and verify X actually contains the supporting language (catches FR-120-class issues).

### 4.3 Standard-version-upgrade process (M, M)

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

### 4.4 Pack: dev-security/claude-rules language coverage review (M, M)

Review the language-specific security rules in [`dev-security/claude-rules/`](dev-security/claude-rules/). Today the pack ships Python-focused guidance plus external overlay rules. Decided 2026-06-22: baseline subset = **JS/TS + Go + Java** (others deferred); **explicitly position the pack as pointing to OWASP cheat sheets / dedicated technical-security sources rather than duplicating them**. Scope: one or more small PRs each adding a language baseline file (mirror `python.md`'s shape) OR updating the pack README's positioning.

### 4.6 QA-cadence mechanical enforcement (M, M)

Surfaced from the Sweep 22 (2026-06-22) discipline-failure assessment. The pack rule, SKILL files, and `.claude/CLAUDE.md` now forbid orchestrator abbreviation of `/validate-pr` and `/retro`, but the only enforcement is the maintainer's manual catch. Candidate gate compares the post-merge history files (`.working/validate-pr/history.md`, `.working/improvement-log.md`) against the merged-PR list and fails when a PR's row is missing or marked abbreviated without a maintainer-authorised exception trailer.

- **Design questions**: where the gate lives (pre-commit / CI / nightly?); the "abbreviated" detection rule; how a maintainer-authorised exception is recorded mechanically.
- **Handoff-PR exemption (must be designed in)**: session-closing handoff PRs intentionally have no `/validate-pr`/`/retro` row (the loop-break); the gate must recognize the handoff-PR exemption and not fail on the legitimately-absent row.
- **Co-design with 4.10** (the TODO/DONE rotation gate) as one "post-merge bookkeeping parity" gate family.

### 4.10 TODO/DONE rotation mechanical gate (M) — surfaced 2026-06-23

Escalated from a convention reminder by two consecutive misses (#278 DD-1, #279 DD-9 — the latter on the very PR fixing the former, for the PR's own newly-shipped item). A lint that flags any TODO resolution line marked "SHIPPED in #N" (or any DD/FR id whose disposition references a merged PR) when the same id still appears as an open backlog item or is absent from [`.working/DONE.md`](.working/DONE.md). The rotation analogue of the existing delta/parity gates: deterministic, catches the exact miss-class twice-observed. Co-design with 4.6 as one "post-merge bookkeeping parity" gate family; share the handoff-PR exemption logic. Until it exists, the close-out-checklist item holds: for EVERY DD/FR a PR ships (including ones first surfaced in that PR), rotate TODO→DONE in the same diff.

**Design note (2026-06-28 validation; deferred).** A first build attempt was scoped and the design space narrowed: the maintainer-chosen "id cross-check" shape (flag any FR/DD/P-id that is BOTH an open TODO backlog-item subject AND a closed item in a `DONE.md` heading) was validated against the current clean `main` and produced **4/4 false positives** (FR-167, a multi-part item with shipped sub-batches but legitimately open; FR-44, where the same FR tag covers a shipped convention statement and an open derivative sweep; FR-104 / FR-130, "not pursued" dropped decisions recorded in both DONE and TODO Priority 7). The FR-44 (same-tag-different-scope) and FR-167 (multi-part) cases are NOT separable by id-matching without semantic understanding, confirming the change-tracking rule's own "this is brittle; the convention is cheaper" verdict. **Disposition: DECIDED (maintainer, 2026-06-28 resume) — build Option B, the "marked-done detector."** The id-cross-check (Option A) is rejected (4/4 FPs, not separable without semantic understanding); the maintainer chose the FP-free **marked-done detector**: flag a TODO item that marks ITSELF done (strikethrough `~~`, `[done]` / `Status: completed` suffix, or a bare `SHIPPED` marker) — it keys on self-marking, not cross-file id overlap, so it carries no id-granularity FP; narrower than the id-cross-check but shippable clean. Build the project way (a `lint-*.py` + four-surface wiring + regression fixture), co-designed with the §4.6 QA-cadence gate and the §4.11(4) worker-provenance gate as the "post-merge bookkeeping parity" gate family; share the handoff-PR exemption logic. Queued in the guard-rails phase of this session's plan; the convention + close-out checklist remain the guard until it lands.

**Update 2026-06-29 (maintainer-decided, building): "build Option B, add the complementary CHANGELOG-asserts-closure check."** Two checks. (1) The **marked-done detector SHIPPED as gate 57 in #468** ([`tools/lint-todo-marked-done.py`](tools/lint-todo-marked-done.py)), scoped to the three FP-free structural markers (strikethrough span, `[done]`/`[completed]` tag, `Status: completed`/`done` field). The bare-`SHIPPED` facet the 2026-06-28 design note listed was **dropped**: it false-positives on open multi-part items (FR-167's "column SHIPPED in PR-B"), the same multi-part FP that rejected the id-cross-check, so per the "long-term best solution" directive it is excluded and the complementary check covers that case instead. (2) **REMAINING (the next PR): the complementary CHANGELOG-asserts-closure PR-time check** — a PR whose added CHANGELOG asserts it closes a TODO item (e.g. "closing TODO §X") must touch BOTH [`TODO.md`](TODO.md) and [`.working/DONE.md`](.working/DONE.md) in the same diff; it catches the wholesale-forgotten rotation (#466's class, which the marked-done detector cannot see because TODO is never edited). Build it as a PR-time delta check in [`tools/run-pr-time-checks.sh`](tools/run-pr-time-checks.sh) (and CI's pull_request section), with the handoff-PR exemption shared with the §4.6 family. §4.10 stays OPEN until the complementary check lands.

### 4.7 Overnight unattended-run driver (M, L)

Deferred to a future session (maintainer-directed 2026-06-22). For longer unattended runs, a single overnight session is the wrong shape (it degrades like any long session). The sound architecture is an **external driver loop** (cron / CI / Agent SDK script, outside the corpus) that launches a **fresh `claude -p` or SDK session per task-unit**, each reading `.working/session-handoff.md` + the TODO/DONE queue, doing one unit, committing, advancing the queue, and exiting. The durable-state layer already exists (`session-handoff.md`, `/resume`, the green-merge-as-last-act + loop-break disciplines); the missing piece is the driver plus an overnight runbook.

- **Design questions**: where the driver runs; merge authority for unattended worker sessions; the stop condition; how a worker signals "needs maintainer" vs "safe to continue"; interaction with the `## overnight-work protocol` in the change-tracking rule.
- **Building blocks confirmed** (2026-06-22): `claude -p` fresh-by-default; Agent SDK fresh-session-per-call; no built-in overnight/auto-reset scheduler in CLI or web.

### 4.1 Corpus-management discipline as a shareable skill (M, XL)

Package the cumulative documentation-and-corpus discipline this project has accumulated as a standalone Claude Code skill that anyone managing a documentation corpus with an AI coding assistant could install.

- **Distillation source**: the twelve `governance/` pack rules form the discipline core; `validation-sweep` and `library-fitness-review` form the periodic-review surface; the audit-programme architecture forms the mechanical-enforcement surface.
- **Generalisation**: carry the patterns and discipline without the GRC-specific control-set citations; adopters supply their own document-type model and metadata-field set.
- **Open questions resolved 2026-06-22**: skill **family** (not omnibus); **prescriptive-only** (no linter scaffolds); **existing pack 1.x bump** (not a new pack). Sequencing: after the FR backlog closes.

### 4.11 Multi-session / multi-worker orchestration codification (track; maintainer-scheduled) (M, L)

Stand up the parallel-worker capability per the **"Multi-session / multi-worker orchestration model"** entry in [`.working/design-decisions.md`](.working/design-decisions.md) (the authoritative design; recovered to `main` in #316). A deliberately-scheduled meta/process track, not a routine backlog fix.

Deliverables 1-3 have shipped: the runbook [`.working/multi-session-orchestration.md`](.working/multi-session-orchestration.md), the Model-B worker section in [`.working/worker-brief-template.md`](.working/worker-brief-template.md), and the light-SOP default in [`.claude/CLAUDE.md`](.claude/CLAUDE.md) + the [`ai-assistant-workflow-disciplines`](dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md) rule. **Remaining (the residue):**

4. A **worker-provenance audit gate**, co-designed with the queued **§4.6** (QA-cadence) and **§4.10** (rotation) gates as one "bookkeeping-parity" gate family, built the project way (`tools/lint-*.py` + four-surface wiring + regression fixture), honest-backstop framing per [`gate-discipline`](dev-security/claude-rules/governance/gate-discipline.md) (it enforces the PRESENCE of the verification record and provenance attestation, not semantic correctness). The separate pre-push-runner gate (folding gate-40/gate-31 into [`tools/run-pr-time-checks.sh`](tools/run-pr-time-checks.sh)) already shipped in #333, so this gate extends rather than duplicates it. The codification PR is itself NOT partitionable (single orchestrator session).

- **Feasibility note:** `grc_library_scratch` is in scope, reachable, and now populated (the `ref/` base). The in-session subagent primitive is exercised; the separate-session external-collaborator primitive and harness support for repo-event subscription remain to confirm at implementation time (the design gates event-driven triggering as opt-in, not the default).
- **SCHEDULING (maintainer decides when):** default is to implement this AFTER the Priority 1 and Priority 2 backlog items are addressed. **Standing exception (do NOT self-authorize):** if at any point the orchestrator judges that standing up this capability would clear the REMAINING P1/P2 backlog faster than working solo on those items, net of the codification cost and counting only partitionable remaining work, surface a pull-forward recommendation with the reasoning (estimated remaining partitionable volume, expected speedup, build cost) and let the maintainer decide.

### 4.12 Publications-assessment / poisoning-detection process for the scratch reference base (M, M) — surfaced 2026-06-25

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
with the §4.11 multi-session track (the scratch ref base is part of that capability) and
the existing `governance/` trust disciplines. Honest-backstop framing: the process raises
the bar against poisoned reference input; it does not by itself guarantee detection.

### 4.16 Multi-session research-brief staging + `/subagent` external-worker entry (M, M) — maintainer-requested 2026-06-26 (timing: maintainer-directed, "tomorrow")

Stand up the INPUT half of the §4.11 multi-session capability so separate-session / separate-account workers can pick up research tasks (the existing §4.11 work delivered the runbook, the worker `CLAUDE.md` contract, the light SOP, and the bookkeeping-parity gate; this adds the brief-staging input channel and the worker entry command). Design advised 2026-06-26; deliverables:

1. **A `research/<work-unit-id>/brief.md` convention in [`grc_library_scratch`](https://github.com/jposluns/grc_library_scratch)** (one brief per partitionable TODO or per FR-167 batch), orchestrator-authored from [`.working/worker-brief-template.md`](.working/worker-brief-template.md): the task, the exact main-repo target paths, the verified-disjoint partition, the `path:line` evidence requirement, the deliverable shape (research, not final prose), the stop-don't-merge and verify-against-live-main invariants, and a pointer to the scratch worker `CLAUDE.md` for the general contract (reference, do not duplicate). Workers deliver findings to the existing `inbox/<worker-id>/`.
2. **A `/subagent` slash command** as the external-worker entry point: read the assigned brief, claim it in `claims-ledger.md`, read the named main-repo files read-only, produce findings, deliver to `inbox/`, stop. **Read-only-on-main MUST be enforced by the worker GitHub account's permissions, not by the prompt** (a prompt is not a security boundary, per [`.claude/rules/secrets.md`](.claude/rules/secrets.md) / the security rules).
3. **Codify both** in the runbook [`.working/multi-session-orchestration.md`](.working/multi-session-orchestration.md); add the `/subagent` command file.

**Gating maintainer action**: provision the least-privilege worker account (read `grc_library` / write `grc_library_scratch` only). In-session `Agent` fan-out works today (shares the orchestrator's credentials, spends its budget); the external-worker path needs the account. **Partitionability**: the decided-content TODOs (FR-30/31/32/34/71/72 net-new docs, deepen-all baselines, FR-58) are the cleanest fit (separate files); FR-167 research partitions per batch but the matrix apply stays single-session. **The apply stage stays single-session with full QA regardless** (the validate-then-apply no-bypass invariant: worker provenance never reduces the QA a change receives). Pairs with §4.11 and §4.12 (the publications-assessment process).

### 4.18 Session-concurrency safety: session-state lease + git cross-check (M, M) — maintainer-requested 2026-06-26

Build the concurrent-session interlock so a `/resume` issued while a prior session is still live cannot corrupt shared `main` state (handoff / TODO / DONE / validate-sweeps / detailed CHANGELOG / the four version surfaces). Full design (problem, options A/B/C, recommended mechanism, honest limitations, build steps, open sub-decisions) is captured in [`.working/design-decisions.md`](.working/design-decisions.md) under "Session-concurrency safety". Summary of the recommended option (C): a gate-exempt `.working/session-state.md` lease (active-session branch, status, `date -u` heartbeat, worker-dispatch list) PLUS a `git fetch` cross-check of recent unmerged `origin/claude/*` branches, wired as a new `/resume` step 0 that HOLDs + surfaces when a session looks live. Deliverables: the lease file + schema; `/resume` step 0; acquire/refresh/release lifecycle wiring in `.claude/CLAUDE.md` + the handoff; optionally a `lint-overnight-file`-style well-formedness gate (four-surface-wired). **Open sub-decisions for the maintainer to confirm at build time**: the staleness-window value (proposed 60 min), advisory-HOLD vs hard-block on a fresh-heartbeat active lease (proposed advisory), and whether to build the well-formedness gate now or defer. Honest scope note: this is an advisory interlock, not a hard mutex (no cross-container lock primitive exists); it prevents the realistic accidental-double-resume, not a determined simultaneous launch. Pairs with §4.11 (multi-session) and the §4.6/§4.10 bookkeeping-parity gate family.

### 4.19 Orchestrator main-loop token instrumentation for session-metrics (L, S) — maintainer-requested 2026-06-27

The [`.working/session-metrics.md`](.working/session-metrics.md) ledger records measured `subagent_tokens` per phase, but the **Orchestrator tokens** column is always `not instrumented` (the convention forbids a fabricated figure). Maintainer-flagged 2026-06-27 to close the gap if feasible. **Feasibility investigated this session (PR #388)**: orchestrator main-loop tokens are NOT instrumentable from inside a session, because (a) no tool surfaces the orchestrator's own per-turn usage (the `Agent` tool returns only `subagent_tokens` for subagents), and (b) no main-session transcript carrying per-message `usage` / `output_tokens` is written to a readable on-disk location during the session (the session project dir holds only `subagents/` and `tool-results/` subdirectories; `~/.claude/sessions/<n>.json` is bare process metadata with no token fields). The realistic paths, none assistant-self-instrumentable today: (1) **harness support**, surface main-loop `usage` the way the `Agent` tool already surfaces `subagent_tokens`, or expose an end-of-session usage-summary (the clean fix; needs a Claude Code feature, so it is a feature request, not an in-repo build); (2) **maintainer-side external measurement**, read total session token usage from the Claude Code UI or the Anthropic Console usage view and record it out-of-band into the metrics row (available today; maintainer action, not assistant self-instrumentation); (3) **post-hoc transcript analysis**, IF a main-session conversation JSONL with `usage` fields is persisted to a readable location after the session ends (the subagent JSONLs persist under `projects/.../subagents/`, so a main transcript may appear post-session, but this is not verifiable from inside a live session), a small summing script over `output_tokens` would then be a low-effort build. Until a path lands the column stays `not instrumented`, which is the honest state the convention already mandates. Next concrete step (maintainer-gated): confirm whether a main-session `*.jsonl` carrying `usage` is retrievable post-session; if yes, a post-hoc summing aid is a small build; if no, the gap is a harness-feature request to file. This item closes when either the aid ships or the maintainer accepts `not instrumented` as the permanent state.

### 4.21 Fork-facing guidance + scripts for building an own reference base (L, L) — maintainer-directed 2026-06-27

Enable people who fork this library to assemble their **own** reference knowledge base (the authoritative source texts that authoring and citation work draws on) instead of depending on the maintainer's private one. The library is CC BY-SA 4.0 prose, but the source standards it cites (ISO/IEC 27001:2022 and the wider ISO catalogue, CSA CCM v4.1 / AICM v1.1 / CAIQ, NIST CSF 2.0, MITRE, OWASP, jurisdiction legislation) are proprietary or licence-restricted and are **not** redistributed in the corpus. The maintainer keeps those source texts in the separate `grc_library_scratch` repo's `ref/` tree (trust-bucketed `standards/` trusted, `legislation/` trusted-but-version-sensitive, `publications/` assess-first; plus an `ingest/` staging area, a `catalogue.yml`, and PDF-to-text / XLSX-to-CSV extracts for AI-readability). **That scratch repo is the maintainer's own private usage-and-reference and is NOT to be shared / not redistributed** (it holds licensed third-party works); this item is explicitly NOT "publish our scratch repo", it is "give a forker the method and tooling to build their own equivalent from sources they are licensed to hold".

Maintainer note (2026-06-27): the scratch `ref/` now holds the ISO references and is being expanded across the other source families; it stands as the maintainer's reference for content. The fork-facing capability mirrors its proven structure without exposing its contents.

Deliverables to scope at build (none built yet, this item only records the work):

1. **A fork-facing guidance doc** (candidate home: a `docs/` adopter guide, scope-and-confirm at build): where to obtain each cited standard from a known reputable / authoritative source (the issuing body's own store or an authorized distributor), the licensing posture (what a forker may hold privately vs redistribute), and how to upload their own licensed copies (e.g. purchased ISO PDFs) into a local reference tree.
2. **The trust-model and tree convention** a forker should adopt, mirroring the scratch `ref/` model: `standards/` (trusted ground truth, one dir per issuing body) vs `publications/` (assess-first, screen for bias / poisoning before use, per §4.12) vs `legislation/` (authoritative but version-sensitive), with an `ingest/` staging area and a machine-readable catalogue.
3. **Helper scripts** (`tools/`-style, scope precision at build): scaffold the `ref/` tree; fetch-from-reputable-source where a licence and a stable URL permit (never bypass paywalls / licensing); extract text for AI-readability (PDF to `--full-text.md`, spreadsheet to per-sheet CSV) mirroring the scratch extraction form; build / refresh the catalogue. Honour the security rules: no credential-bearing fetches in tracked config; treat downloaded `publications/` content as untrusted until screened.
4. **Wiring notes**: how a forker's reference base feeds the in-repo validator modules ([`tools/ccm_aicm_reference.py`](tools/ccm_aicm_reference.py), [`tools/nist_csf_reference.py`](tools/nist_csf_reference.py)) that gates 48/49/54 build on, and the `/matrix-fit` semantic-fit audit (the [`matrix-fit`](dev-security/claude-rules/skills/matrix-fit/SKILL.md) skill, shipped #399), so a fork can validate control-code citations against its own ground truth.

Low urgency (maintainer flagged it as deferred, "a priority 5 item"); it is filed here in Priority 4 (adopter experience / tooling) because it is fork-facing tooling + guidance, the same class as the other Priority 4 tooling items, rather than the country / regulator content overlays Priority 5 enumerates. Pairs with §4.12 (the publications-assessment / poisoning-detection process) and the standing reference-base discipline the `/resume` Reference-knowledge-base step and the [`multi-session-orchestration`](.working/multi-session-orchestration.md) runbook §6 describe.

### 4.22 Document the scratch `ref/` base as the standing citation ground-truth (S, S) — surfaced 2026-06-27 (scratch-review S-5/S-11/S-12)

The scratch `grc_library_scratch/ref/` base is now the maintainer's standing reference for every task (per the `/resume` Reference-knowledge-base step and the [`multi-session-orchestration`](.working/multi-session-orchestration.md) runbook §6), but no corpus-facing spec tells an author "verify a citation against `ref/`, here is the trust model, here is the proprietary-no-redistribute rule". The [`specification-citation-verification.md`](governance/specification-citation-verification.md) and the [`register-canonical-citations.md`](governance/register-canonical-citations.md) Maintenance section both predate the ref base. Add a short pointer in one of those (S-11) describing `ref/` as the local verification source, its trust tiers (`standards/` > `frameworks/` > `publications/`; `legislation/`/`programs/` authoritative-in-domain; `templates/` scaffolding), and the proprietary-no-redistribute constraint. Also record (S-5) that the `/matrix-fit` reference base for control-title lookups is the `ref/` CCM/AICM CSVs + CSF OSCAL (+ the ISO Annex A title map once S-4 lands), so the cadence is reproducible rather than memory-bound. Minor follow-on (S-12, FYI): the 16 ISACA policy templates in `ref/templates/` are usable as structural scaffolding for template-type corpus docs (e.g. the remaining privacy templates FR-31/32/34), trusted issuer but proprietary, adapt-don't-copy. This pairs with §4.21 (the fork-facing mirror of the same model).

### 4.23 TODO-hygiene completion pass + accretion guard (S, S) — surfaced 2026-06-27 (maintainer flag + research scan)

The maintainer flagged (2026-06-27) that shipped/historical content had accreted in TODO instead of rotating out. Parts (a) and (b) shipped in the TODO-hygiene PR: (a) §4.11 (multi-session orchestration) trimmed to its residue (deliverable 4, the worker-provenance gate; deliverables 1-3 shipped) after verifying against the gate inventory of the time; (b) the unambiguous shipped/closed clauses deleted (the Queueing-rules "FR-166/DD-1/DD-9 already shipped" note, the P3-intro "B2 closed #408 / DD-12 closed" parenthetical, the §4.8 "actioned in #275" line, the §4.18 "D4 shipped in #366" clause, the Backlog-totals "closed in #N" clauses).

**Remaining (open):** (c) **whether the `## Standing conventions`, `## Backlog totals`, and `## Priority 7` (audit-trail-only) sections belong in TODO at all** or in a conventions / design-decisions doc. This is a **maintainer call** (they are non-forward-looking but appear intentionally retained); filed for decision in `## Priority 7`. The **accretion guard** is the §4.10 TODO/DONE-rotation gate (consider extending gate 45 to flag shipped-PR-number history accreting inside an open TODO item, so rotation is mechanically prompted rather than convention-only).

### 4.25 Wind-down / overnight-mode SOP refinements (maintainer-directed 2026-06-28) (S, S)

Two maintainer-directed refinements to codify in the `## Wind-down decision framework`, `## Attended-autonomous operating mode`, and overnight-protocol sections of [`.claude/CLAUDE.md`](.claude/CLAUDE.md) (a focused PR; flagged "not urgent, handle later today"). Effective behaviorally on direction; codification queued here.

1. **Overnight-mode toggle is not a no-answer default.** Do NOT decide to turn off overnight mode unless the maintainer explicitly says so, or (if unsure) pause and ask. If no answer arrives in the ~2-minute graceful-degradation window, **MAINTAIN overnight mode** and re-ask the next time the maintainer messages. This carves the overnight-OFF decision out of the general wind-down no-answer-to-handoff default (a handoff silently ends overnight mode, the recurrence the maintainer flagged after the #425 wind-down default ended the overnight run while they were briefly up).
2. **Continue-as-default while quality holds, even when context is heavy.** Heavy context alone is NOT a wind-down trigger; the decision is evidence-based, not inference. The only exception is a run of expected chained large PRs where historical metrics show quality is likely to suffer very soon. Adjust the self-assessment SOP so context-heaviness is not treated as a quasi-trigger.

### 4.26 Reference version-currency register + scratch superseded-archival (maintainer-directed 2026-06-28) (M, L)

Maintainer-directed: a fork-friendly mechanism so the project never relies on a stale belief about an external reference's version. Four parts: (1) a more-than-one-week staleness cadence (when over a week has passed since a reference's version was last verified, re-check it upstream before relying on it, scratch `ref/` copies especially); (2) a register of where to check the latest version of everything the project references (upstream links), shipped as a usable, fork-extensible artefact; (3) the principle that the scratch `ref/` base is believed-current STORAGE, not a version authority (the authoritative answer to "is this current?" is the upstream link, never scratch); (4) a scratch superseded-archival workflow: on finding a newer version, download it to scratch if egress allows, keep the old version but move its files (extracted text plus original) into scratch's `ref/.superseded/` store (bucket-mirrored layout per scratch `CONTRIBUTING.md`).

**Assistant assessment (2026-06-28, per the suggest/advise interpretation rule)**: the need is real and evidence-backed (the MITRE `v15` to `v19.1` and ATLAS `v4.7` to `v5.6.0` drift found this session; the earlier ISO/IEC 27701:2019 to 2025 catch; the ISO 29134 hallucination). Recommended shape: do NOT build a new parallel register. Extend the existing [`governance/register-canonical-citations.md`](governance/register-canonical-citations.md) (already tracks Current version / Publication date / Superseded) with `Upstream check location` and `Last verified (UTC)` columns, and wire the cadence into the existing [`governance/specification-citation-verification.md`](governance/specification-citation-verification.md) plus its Citation Verifications Register, so there is one source of truth. Reconcile with the related queued items before designing: §4.3 (standard-version-upgrade process), §4.21 (fork-facing reference-base guidance), §4.22 (scratch `ref/` as citation ground-truth, whose framing must be squared with part 3: scratch is content ground-truth for citation TEXT, not the authority for version CURRENCY). Caveats: the download step needs network egress (intermittently blocked here, per DD-10), so the workflow degrades to surface-and-defer; the staleness check should be an advisory tool (like the matrix-fit worklist), NOT a hard CI gate (a gate would fail whenever egress is blocked, an environment condition not a defect). Fresh-context-best (large row-set, cross-repo). Folds in the standing MITRE version-currency fix (`ATT&CK v15` to `v19.1`, `ATLAS v4.7` to `v5.6.0`, both confirmed 2026-06-28: ATT&CK live against MITRE releases, ATLAS from the held atlas-data at 2026-05-27) as the first rows updated under the new columns.

**Decided (maintainer 2026-06-28): the extend-the-existing-register approach is accepted.** Extend [`register-canonical-citations.md`](governance/register-canonical-citations.md) with `Upstream check location` and `Last verified (UTC)` columns and wire the cadence into [`specification-citation-verification.md`](governance/specification-citation-verification.md) plus its Citation Verifications Register; the staleness check is an advisory tool, not a hard CI gate; the scratch `ref/.superseded/` archival convention and the scratch-is-not-a-version-authority principle are codified in the scratch repo. Build as a fresh-context session task.

**Validated 2026-06-28 (upstream-checked at the handoff-staleness resume): the ATLAS target above is CORRECTED.** Upstream authority (mitre-atlas/atlas-data releases) shows current = **v2026.05** (2026-05-27, YAML format v6.0.0); the **v5.6.0** the assessment line cites is the DEPRECATED old-scheme line (the `ATLAS.yaml` header self-declares it deprecated) and is what scratch currently holds. ATT&CK **v19.1** is confirmed current and matches scratch. So the register's ATLAS row must move to **v2026.05**, NOT v5.6.0, and scratch needs the superseded-archival update (move v5.6.0 into scratch's `ref/.superseded/` store, download v2026.05). That scratch update is egress / maintainer-download-gated and is logged as a **pending decision** in [`pending-decisions.md`](../.working/pending-decisions.md); per the `## Reference-version currency` SOP, do NOT write the superseded v5.6.0 anywhere, and keep the register row and the scratch base coherent (fix them together).

### 4.27 CLAUDE.md removal-ledger review cadence (standing) — added 2026-06-28 (PR #441)

The PR #441 condense of [`.claude/CLAUDE.md`](.claude/CLAUDE.md) moved the cut rationale, war-stories, and provenance into [`.working/claude-md-considerations.md`](.working/claude-md-considerations.md) (the removal ledger), each entry carrying an "evidence the removal was wrong" signal. Standing activity (not a one-time task): each `/retro` does a quick scan of the ledger's open RM entries and the periodic hallucination-metrics pass does a deeper one; if an entry's signal appears, advise the maintainer to restore the cut text or make a new CLAUDE.md change, and record the disposition in that entry's Status. Wired into [`.working/improvement-log.md`](.working/improvement-log.md)'s Convention section. This item is the durable tracker so the cadence is not lost; it stays open by design.

### 4.28 CLAUDE.md-optimization diagnostic skill (L, S) — maintainer-directed 2026-06-28 (low priority)

Decision (maintainer 2026-06-28, after the PR #441 condense): the keep-and-condense method is documented as pack guidance ([`guidance-claude-md-optimization.md`](dev-security/claude-rules/guidance-claude-md-optimization.md), shipped 2026-06-28); a full optimization skill was declined as too judgment-heavy to mechanize (the keep-versus-cut call is exactly the part a skill cannot do). The tractable mechanical aid is a NARROW read-only diagnostic, a `/claude-md-audit`-style reporter over a target rules file that surfaces file length, section count, an actionable-token-density heuristic (ratio of greppable rule tokens such as commands, paths, gate numbers, and thresholds to total prose), and a "no removal ledger referenced" flag. Advisory output only, never a gate (the keep/cut decision stays the maintainer's). Low priority: build only if the guidance doc proves insufficient on its own. Pairs with the §4.27 ledger-review cadence.

---

## Priority 5 — Content expansion (country / programme / regulator overlays)

Adding new content / coverage to existing domains. Each subitem is a separate small or medium PR; the maintainer schedules deliberately. (Subsections are similar-effort country/regulator overlays, so the document order is retained.)

### 5.1 Logistics country / programme expansion

The WCO AEO Compendium identifies ~94 trusted-trader programmes globally; the library covers 4 (BASC, CTPAT-US, AEO-UK, PIP-Canada). Highest-priority additions: EU AEO (covers 27 member states under EU UCC Art 38), Mexico NEEC / OEA, Australia Trusted Trader (ATT), Singapore STP / STP-Plus, Japan AEO, Korea AEO, New Zealand Secure Exports Scheme (SES), China AEO.

### 5.2 Financial-services country regulator overlays

Within `compliance/financial-services/`: UK PRA / FCA (`annex-uk-pra-fca.md`); US OCC / FRB / FDIC / SEC / FINRA; Canada OSFI; Australia APRA; Singapore MAS; Japan FSA.

### 5.3 Healthcare country regulator overlays

Within `compliance/healthcare/`: US HIPAA detail (Privacy/Security/Breach-Notification Rules, HITECH); UK NHS DSPT; EU MDR / IVDR; Canada PHIPA and provincial frameworks; Australia My Health Records Act.

### 5.4 Energy and utilities country regulator overlays

Within `compliance/energy-and-utilities/`: US NERC CIP standards; US TSA pipeline cybersecurity directives; UK Ofgem cyber requirements; EU ENISA sectoral guidance.

### 5.5 Telecommunications country regulator overlays

Within `compliance/telecommunications/`: EU EECC; UK Ofcom telecom security framework; US FCC regulations; Australia ACMA requirements.

### 5.6 Public-sector country / regulator overlays

Within `compliance/public-sector/`: UK Government Cyber Security Strategy and GovAssure; Australia ISM and PSPF; Canada IT Standards for federal departments; EU eIDAS public-sector authentication.

### 5.7 Privacy jurisdiction gaps

Existing privacy domain covers 25 country annexes. Known gaps or stale entries: Argentina (PDPA 2025 update pending); Saudi Arabia PDPL (recent updates pending); Mexico LFPDPPP (standalone annex possible); re-review of EU member-state derogations where applicable.

### 5.8 AI jurisdiction overlays

The library cites EU AI Act extensively but lacks a dedicated `ai/jurisdictions/` subdirectory parallel to `privacy/jurisdictions/`. Candidates: EU AI Act detailed annex; Canada AIDA; UK AI policy framework; US state-by-state AI laws (Colorado AI Act, NYC bias audit law); China generative AI rules; Korea AI framework.

---

## Priority 6 — Domain-level expansion (new domains, longer-term)

Entirely new domains, multi-week scope each. The maintainer schedules deliberately. (Ordered lowest-effort-first; `6.N` numbers are stable ids.)

### 6.2 Identity-specific content depth (L)

Customer Identity (CIAM) governance, workforce identity governance, identity federation patterns, passwordless adoption playbooks. The library has IAM policy and procedure but no dedicated content for these patterns.

### 6.3 Quantum cryptography readiness deepening (L)

The library has a phase-level PQC roadmap ([`security/roadmap-post-quantum-cryptography.md`](security/roadmap-post-quantum-cryptography.md)) but not detailed implementation content. Pending: a PQC migration playbook (operational steps per system class), crypto-agility patterns (key abstraction, algorithm switching, hybrid schemes), and post-quantum-ready CA / PKI management.

### 6.4 Cross-framework matrix expansion (L)

Current matrix ([`governance/matrix-cross-framework-alignment.md`](governance/matrix-cross-framework-alignment.md)) covers major frameworks; expand to additional sectoral and regional frameworks as the P5 country/sector content grows.

### 6.5 CMMI capability levels alongside maturity levels (L)

Per maintainer direction 2026-06-22 (low priority, after the FR backlog completes). The corpus uses the 5-tier maturity-level scale at both organisation-wide and per-domain granularity; CMMI distinguishes the two (maturity levels 1-5 org-wide; capability levels 0-3 per practice area). Introducing capability levels would: (1) add a capability-level scheme to [`governance/framework-governance-performance-and-improvement.md`](governance/framework-governance-performance-and-improvement.md) §2; (2) update [`docs/template-maturity-self-assessment.md`](docs/template-maturity-self-assessment.md) to use capability levels per domain and aggregate to maturity levels at the programme rollup; (3) possibly extend [`governance/register-digital-trust-and-assurance-metrics.md`](governance/register-digital-trust-and-assurance-metrics.md) DTI thresholds with a capability-level surface.

### 6.1 Multi-cloud governance overlay (XL)

Per-cloud hardening baselines for AWS, Azure, and GCP exist in `dev-security/`. The remaining gap is multi-cloud governance (cross-cloud risk taxonomy, cross-cloud incident coordination, cloud-portfolio-level controls). Could live in `operations/` or warrant a new `cloud/` domain.

---

## Priority 7 — Awaiting maintainer decision

One open decision pending (§4.23(c), below). The 16 deferred decisions triaged 2026-06-23 are now queued work in P1-P3, and B2 (decided) moved to P3. The FR-104 / FR-130 entries are NOT pending decisions; they are dropped-decision audit-trail records (see [`.working/design-decisions.md`](.working/design-decisions.md) "Decisions explicitly dropped" for rationale).

- **§4.23(c) — do the audit-trail-only sections (`## Standing conventions`, `## Backlog totals`, `## Priority 7`) belong in TODO at all, or in a conventions / design-decisions doc?** They are non-forward-looking but appear intentionally retained. Maintainer call; left in place pending the decision.
- **FR-104**: Per-regulation context not pursued.
- **FR-130**: Portal reorder not pursued (README stays at decision-tree item 1).

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
- **Compute-don't-ask** (maintainer-flagged 2026-06-23) — before surfacing a question, apply a "can I compute/verify this myself?" gate; surface the result, not the raw question. (Pending codification into the `clarify-before-acting` rule — see 4.8.)

---

## Backlog totals

Approximate active counts after the 2026-06-23 restructure (the priority sections themselves are the source of truth; these drift):

- **P1 (urgent quality)**: ~18 items (8 H[critical] + 10 H).
- **P2 (substantive improvements)**: ~36 items (Medium fitness findings + the former Phase 2 clusters + DD-2/3/4/5/8/11 + relocations + loop-break-generalize).
- **P3 (low-priority cleanup)**: ~19 items (Low/FYI findings + DD-10 + routine cleanup).
- **P4 (adopter experience)**: 9 subsections (4.1-4.8, 4.10; 4.9 closed in PR #295).
- **P5 (content expansion)**: 8 subsections (5.1-5.8).
- **P6 (domain-level)**: 5 items (6.1-6.5).
- **P7 (awaiting decision)**: 1 pending (§4.23(c)) + 2 dropped-decision audit-trail entries.

---

## Notes on maintenance

- Add new items at the appropriate priority; within a section keep the lowest-effort-first ordering. Move items between priorities as context changes.
- When an item is completed, delete it from this file (no strikethroughs, no `[done]` suffixes) and add an entry to [`.working/DONE.md`](.working/DONE.md) in the same PR. The rotation discipline is documented in the PR-finalization-protocol section of [`.claude/rules/governance/change-tracking.md`](.claude/rules/governance/change-tracking.md).
- Design decisions belong in [`.working/design-decisions.md`](.working/design-decisions.md), not in TODO. The P7 "dropped-decision" entries cross-reference those decisions for audit-trail completeness without duplicating the rationale.
- This file is the source of truth for what's queued; conversation history is not.
- Fitness-review backlogs remain the authoritative per-finding evidence source; this file is the action-organized view, kept in sync at fitness-review-cycle time.
