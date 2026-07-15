# DONE

Closed-TODO ledger for the GRC Documentation Library. Records work that has shipped, keyed by the original backlog ID (PR number for PR-based items; the TODO `P-X.Y` identifier for backlog items). Reverse-chronological: newest at top.

This file complements two other working-state ledgers:

- [`CHANGELOG.md`](../CHANGELOG.md): records *what landed in each PR* (file-by-file changes, version bumps, verification). Organized by PR. Adopters and downstream consumers read CHANGELOG for the full story.
- [`design-decisions.md`](design-decisions.md): records *design decisions made* (working-state and convention decisions; decisions explicitly dropped). Organized thematically.

DONE records *which backlog items each PR closed*, formatted as **scrolling battle-text**: the `tail -f` view of shipped work. Each entry is a 1-2 sentence headline a maintainer scanning the file can recognize at a glance without parsing prose. Details (file paths, version bumps, verification, rationale) live in CHANGELOG; DONE does the at-a-glance index job. Adopters reading the corpus do not need any of these three files; they are maintainer working state and live under `.working/`.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions. It is exempt from corpus audit gates per the `.working/` directory exemption.

### TODO §3.50: widen gate 69 to the "TODO item N.M" phrasing (2026-07-15)

Widened gate 69 (`tools/lint-positional-backlog-tokens.py`) so its `TODO` arm also accepts an optional `item(s)` qualifier before the section token, catching the `TODO item N.M` phrasing (previously only `TODO §N` / `TODO N.M` / `backlog item PN.M` matched). FP-safe: a corpus census found zero live `TODO item <token>` carriers and confirmed ordinary `TODO item covers ...` prose has no section token, so it is not flagged; the widened regex passed a 9-case behaviour test and the gate stays 0 over the corpus. Added two regression fixtures (the `TODO item 3.4` detect + the `TODO item covers` clean case) and updated the §6 gate-69 narrative + spec version.

### TODO §2.5 (AI-domain delta executed; umbrella retired, remaining workstreams re-homed to §2.17-§2.21): AI-domain post-plan delta (2026-07-15)

The maintainer-directed AI-domain delta is executed and the §2.5 umbrella retired. Landed: Workstream A EU/CA source fold-ins, A.4/A.5 Commission Guidelines (#843), A.2 GPAI Safety-Security (#844), A.3 GPAI Copyright (#847), A.1 GPAI Transparency + Model-Documentation-Form mapping (#849, blocker resolved by ingesting the Form into grc_library_ref ref PR #77); C.1 Canada TBS third-review dates reconfirmed (#850), C.3 IEEE 7000 /claim-fit (#850), C.4 ISO/PAS 8800 no-action (resolved). The remaining distinct workstreams were re-homed to their own new P2 items via the counter: A.6 California CCPA/ADMT to §2.17, B.1 South Korea AI Basic Act to §2.18, B.2 Singapore Model AI Governance to §2.19, C.2 ref-side last_checked sweep to §2.20, and the deferred B.3 further-jurisdiction set to §2.21. Standing reminder carried forward (the reference-version-currency SOP): the EU AI Act full text is held in grc_library_ref, so each load-bearing AI Act article citation is verified against the held text with upstream currency confirmed for version-sensitive points.

### TODO §2.4 (website build complete and live; item stays open until the maintainer's publish go): public presence at grclibrary.ai (2026-07-15)

The public landing site is built and live on Cloudflare Pages at grclibrary.ai, developed across a maintainer live-review loop: the build + polish round #919-#924 (the `.web/` live-corpus generator, 11 per-domain pages, feature-card and doc-title corpus links, and the responsive contents sidebar), the adoption round #925-#926 (a dedicated `/pack` governance-pack page and the landing restructure with a "Get started" section and a standalone licence section), and the nav-consistency fixes #928 (comprehensive hero CTAs, the pack sidebar listing all 23 skills, Get-started cards matching the page pattern). §2.4 stays open for the remaining maintainer-gated items only: further live-review fixes, the confirmed follow-ups §2.15/§2.16, the §2.6 Cloudflare-console watch-paths, and the publish go-decision.

### TODO §3.57 (apply wave complete; item stays open for the matrix TSC-column residual): reference-breadth new-ingest apply (2026-07-15)

The reference-breadth new-ingest apply over the 63 2026-07-12 ref sources landed across #866-#883: the High EDPB-privacy cluster (4/2019 #866, 05/2020 #867, 01/2022 #868, 9/2022 #869, 07/2022 #873) plus the version-sensitive rows AICPA TSP 100 (#876), EU 2021/915 (#877), ANPD 18/2024 (#878), SOR/2018-64 (#879), EDPB 28/2024 (#880), NIS2 2024/2690 (#881), EDPB 8/2022 (#882), and the Brazil Resolution 4/2023 follow-up (#883), each verified verbatim against the held source, upstream-currency-confirmed this turn, refute-verified, and each with a canonical-citations register row. Split out per the 2026-07-15 numbering hygiene: §3.57 stays open only for the deferred matrix TSC-column mapping (a `/matrix-fit` single-file sensitive change).

### TODO §3.63 (both routed findings resolved; item stays open for the RB-ETSI secondary see-also): reference-breadth FULL routed findings (2026-07-15)

The two genuine findings from the first `/reference-audit` FULL run (deep-assessment r3 Phase-3) are resolved: RB-FFIEC-CAT (the FFIEC sunset the Cybersecurity Assessment Tool 31 Aug 2025; the financial-services annex row corrected stricter-safe in #899) and the primary half of RB-ETSI-104128 (the ETSI TR 104 128 corroborative see-also added to the AI security technical-implementation guide in #907). Split out per numbering hygiene: §3.63 stays open only for the secondary RB-ETSI see-also in the AI security-and-risk standard's alignment table.

### TODO §3.68 (clear conversions complete; item stays open for the routed divergent carriers): vuln-remediation-SLA single-source-of-truth (2026-07-15)

The clear stricter-safe conversions to the vuln-management-procedure SoT (section 2) landed in #912: the production-security full-table restatement, the patch-management deployment-timeline column, the dev-security secure-development restatement, and the software-evaluation "15 days or fewer" looser Critical, all re-anchored to cite the SoT. Split out per numbering hygiene: §3.68 stays open only for the four ROUTED divergent-value carriers that need a maintainer judgment call (pentest, supplier-tier, patch-exception-deferral, and the BASC-KPI drift-hardening), not mechanical conversions.

### TODO §3.62 (resolved proposals built/expired; item stays open for the G1 hook decision): guardrail-review r10 routed machinery proposals (2026-07-15)

The r10 `/guardrails` routed proposals are dispositioned: G3 (register row-order guard) built as gate 50 Check 5 in #913, G5 (#376 paired-surface candidate) formally EXPIRED in #909 as superseded by gate 50 Check 4 plus the convention, and the gate-41 docstring cross-reference symmetry added in #909. Split out per numbering hygiene: §3.62 stays open only for G1 (the branch-to-main edit-guard hook, a maintainer build-or-keep-convention decision); G2/G4 are already-tracked cross-references, not new work.

### TODO §1.2: Root CHANGELOG #902+ compact plain-language reformat + readability guardrail (2026-07-14)

Reformatted the root CHANGELOG entries for #902-#914 from long, dense, semicolon-chained run-on sentences (67-140 words) back to the compact plain-language two-sentence form a general reader can follow (each compression research-drafted, then verified against the detailed mirror; every `**date | version | PR #N**` header left byte-unchanged so gate-59 parity holds). Also strengthened the advisory guardrail `tools/audit-changelog-entry-length.py` with a longest-single-sentence signal (WARN when any one sentence exceeds 65 words), which catches the dense sub-130-word run-ons the prior word-count-only threshold missed. Closes the P1 recurrence of the exact drift #908 had just fixed for #887-#901.

### TODO §3.72: ISO/IEC 20000-1 clause-attribution accuracy pass (2026-07-14)

Ran a full-cluster `/claim-fit` pass over all 9 corpus docs citing ISO/IEC 20000-1, judging each cited clause against the held 20000-1:2018 TOC (routed from #910's reference-breadth research, which spot-caught 2 of them). #911 corrected 11 clause citations across 7 docs: the fabricated "§8.6 Service management" label (capacity->§8.4.3, observability->§9.1), the coarse §8.3 in the SLM doc (table + prose ->§8.3.3), two imprecise document-level citations made precise (release->§8.5.3, financial->§8.4.1), the change-management doc's 4 §8.5 cells (Configuration mgmt ->§8.2.6 wrong-clause, Change/Emergency/CAB ->§8.5.1, header ->ISO/IEC 20000-1; initially missed because its column header omits the "-1"), and the governance doc-index register's SLM row (§8.3->§8.3.3; outside the 9-doc operations scope) - the last two both caught by the pre-push skeptical verifier. SRE left document-level (no clean clause home). Every clause title verified verbatim against the held source; a whole-corpus re-grep confirms every clause-carrying 20000-1 citation is now consistent with the held TOC.

### TODO §3.67: ISO/IEC 20000 family review + corpus reference-breadth pass (2026-07-14)

Reviewed the newly-held ISO/IEC 20000 family (12 held items) via a research-worker `/reference-audit` new-ingest pass. Finding: the corpus already engages the normative ISO/IEC 20000-1:2018 well (9 docs cite it); the other parts are informative guidance/vocabulary/cert-body standards that would be citation-stuffing to load as compliance rows. #910 added the one strongest, well-grounded addition, an informative ISO/IEC TS 20000-11:2021 (20000-1↔ITIL relationship) see-also row on `operations/framework-it-service-management.md` (whose thesis is exactly that bridge); candidates 20000-10 (vocabulary, no natural terms-section home) and TS 20000-15 (Agile/DevOps, lower fit) were assessed and not added per the anti-stuffing guard. The DA-ISO20000 20000-1 citation was already verified in #907. An incidental clause-mis-attribution finding (existing 20000-1 §-citations in the ITSM cluster) was routed to §3.72 as a full-cluster `/claim-fit` pass rather than fixed piecemeal.

### TODO §3.64: deep-assessment r3 Phase-4/5 routed findings, cluster fully resolved (2026-07-14)

The r3 dead-gate/ground-truth cluster (5 findings) is fully closed and rotated: DA-ASVS ASVS 4.0.3->5.0.0 chapter remap (#902, high-assurance harness; Class 2 generic-governance citations spun out to §3.66), DA-DORA-A12 article mislabel (#899+#900, corpus-wide), DA-AIACT-A26 AI Act over-attribution (#899), DA-ISO20000 citation verified against the now-held ISO/IEC 20000-1:2018 (#907), and DA-gate25-scaffold retired (#909). §3.66 (DA-ASVS Class 2) remains the one live continuation, re-pointed at its #902 origin.

### TODO §3.65: root CHANGELOG compact-form reformat + advisory length guard (2026-07-14)

Reformatted root `CHANGELOG.md` entries #887-#901 from long multi-sentence paragraphs (109-262 words, the deep-assessment r3 session's drift) back to the adopted compact one-liner form (each compression verified against the detailed mirror), and shipped a light advisory guard `tools/audit-changelog-entry-length.py` (advisory, exit 0, WARN over 130 words; not gate-wired) so future root-entry drift is surfaced. Closed in #908.

### TODO §3.58: delivery-pipeline reconciliation and stale-seed disposition (2026-07-13)

Reconciled the scratch-inbox delivery pipeline: closed under the maintainer's disposition rule (for scratch deliveries older than 5 days, keep ONLY pure-research seeds, discard the rest), executed in scratch PR #164, which removed the five consumed / stale-non-pure-research inbox drops (gr-10-history-gate-batching, changelog-root-reformat-build, atlas-crosswalk-317, ai-gaps-expansion-plan, the claude-pack-hygiene programme) and annotated the claims-ledger + COVERAGE dispositions, keeping the pure-research seeds available as input. The residual tooling weakness (the recycled-number token map that made this a describe-the-work exercise) is spun off as §3.61.

### TODO §3.59: read-only-git rule for validation/verifier subagents (2026-07-13)

Codified the rule that a dispatched verifier or validation subagent sharing the orchestrator's working tree inspects git history read-only (`git show`/`git diff`/`git log`) and never moves the tree's branch or HEAD (`checkout`/`switch`/`reset`/`stash`), preventing the #866 shared-tree branch-collision (a subagent's checkout mis-branched a commit onto local main; caught fail-loud at PR-create, repaired). Project surfaces (the /validate-pr + /validate command stubs + a CLAUDE.md note) in #870; the pack-distribution half (the ai-assistant-workflow-disciplines rule, both trees, project-agnostic) in #871. The secondary concurrent-suite fixture-race observation was assessed and documented as a re-check-standalone artefact; the deeper per-process-tempdir tooling fix is spun off as §3.60.

### TODO §1.2 (recycled number): SP 800-154 "held source" wording accuracy (2026-07-13)

Corrected the reference-audit guidance's motivating example: NIST SP 800-154 (a never-finalized NIST draft, not held in `grc_library_ref`, verified this turn) was described as a "held source" and as a source that "sits in the reference base". Reframed it accurately as a relevant-but-unavailable source that surfaced the general "held but unused" class, across the four scanned carriers (parent CLAUDE.md reference-breadth-cadence section, the `/reference-audit` command stub, the pack README skill-tree line and the reference-audit version-history row); the class definition itself was already correct and unchanged. Distinct from #509's §1.2 (per-document ISO Annex A validity, gate 58), which reused the same number.

### TODO §4.8: Pack adoption-hygiene programme, phases 1-4 (2026-07-12)

The four-phase programme that made the `dev-security/claude-rules/` pack project-agnostic for public distribution: Phase 1 condensed all 13 governance rules (operative-core / on-demand-rationale split, #835-#840); Phase 2 generalized the 14 project-wired skills, added 2 derived skills + the rule-provenance register (#842); Phase 3 scrubbed the 14 residual project wirings from 6 governance rules and added the 13 PROJECT-OVERLAY blocks (#845); Phase 4 ran the acceptance sweep (PASS), triaged the routed findings to §1.2/§3.56/§3.57/§4.9, and closed the programme (#846). The pack now carries zero out-of-pack relative links and zero project instantiations in its governance rules; gate 37 enforces the pack/`.claude` overlay sync. Unblocks §4.1 (corpus-management shareable skill).

### TODO §4.7 (deep-assessment r1 R13): RESUME.md maintainer-internal label (2026-07-12)

Added an in-file "maintainer-internal; adopters can ignore or delete" note to the top of `RESUME.md` (the README maintenance-file table already carried the same framing at line 167), so the adopter-visible root file now signals it is not an adopter document on both surfaces.

### TODO §5.9-R1 + §6.3-R3 (deep-assessment r1): stale sub-bullets closed as already-resolved (2026-07-12)

Verified both were already fixed in the corpus and removed the stale TODO sub-bullets: the privacy jurisdiction-index US cell already names the SB 26-189 / 2027 Colorado regime (R1), and `register-coverage-gaps.md` §3 already carries the SOC 2 (TSC) disclosure row (R3). No corpus change; TODO housekeeping only.

### TODO §3.53 (deep-assessment r2): missing-reference-document SOP distributed to the pack (2026-07-12)

Distributed the project's missing-reference-document SOP into the pack `evidence-grounded-completion` rule (source + byte-identical `.claude/` mirror) as a project-agnostic missing-load-bearing-reference corollary in the external-version-currency section: acquire the reference from its primary source and ingest, else surface with named options, never route a "source-not-held" finding without first attempting acquisition. Generalizes the held-but-superseded version-currency discipline to the not-held case. Pack `1.59.6` to `1.59.7`; project `.claude/CLAUDE.md` "queued" pointer updated to "shipped"; `lint-language` clean.

### TODO §3.52 (deep-assessment r2 citation-fit): 42001/27001 clause-8.4 remaps (2026-07-12)

Applied the two clause-8.4 citation-fit best-fits the r2 F1 verifier surfaced (surfaced for maintainer confirm-or-redirect in `pending-decisions.md`): the transparency/notice rows in the 5 AI jurisdiction annexes remapped from the wrong ISO/IEC 42001 Clause 8.4 (impact assessment) to 42001 Annex A.8 (Information for interested parties); the compliance matrix's dataset-datasheet / model-card / system-card rows remapped from a non-existent ISO/IEC 27001 §8.4 to §7.5 (Documented information). Both verified against the held standards; skeptical verifier SHIP. Also fixed the #830 `/validate-pr` finding (the ISO/IEC 30111 note's procedure-scope overstatement) in the same PR.

### TODO §3.51 (deep-assessment r2 reference-breadth): 3 held-but-unused sources cited (2026-07-12)

Added the three additive reference-breadth citations the r2 reference-audit surfaced, each read at attach-time and confirmed held + current upstream: ISO/IEC 30111:2019 (vulnerability-handling process standard) as a process-standard note in `security/procedure-vulnerability-management.md`; MITRE CAPEC v3.9 (attack-pattern enumeration) as a supplementary threat-list input in `security/standard-threat-modelling.md`; and NIST IR 8374 Rev.1 (ransomware CSF 2.0 community profile) as an optional control-prioritization overlay in `resilience/procedure-backup-and-recovery.md`. ISO/IEC 29147 (the "also" secondary) was not held, so it was not cited. Skeptical verifier SHIP.

### TODO §3.48 (deep-assessment r2 F5): DORA reporting-window verification and citation (2026-07-12)

Verified the DORA major-incident reporting windows against the already-held RTS Delegated Reg (EU) 2025/301, and corrected `compliance/financial-services/annex-dora-implementation.md` so the initial-notification window states BOTH bounds (within 4 hours of classification as major AND no later than 24 hours from becoming aware, the outer bound the prior "4 hours" phrasing omitted), with the intermediate (72h from the initial notification) and final (one month after the intermediate report) windows made precise and the RTS/ITS citations added (2024/1772 classification, 2025/301 content and time limits, 2025/302 forms; Articles 18/19/20). The sources were already held in `grc_library_ref`; no ingest was needed (a redundant ingest branch was opened and closed after a stale-local-checkout misread). Closes r2 F5.

## How items get here

When a PR closes a TODO item, the maintainer (or the AI assistant under the corpus-management discipline) rotates the item from [`TODO.md`](../TODO.md) into this file as part of the PR's diff. The rotation is enforced by convention rather than by a gate, per the discipline section in [`dev-security/claude-rules/governance/change-tracking.md`](../dev-security/claude-rules/governance/change-tracking.md).

The format for each entry:

- `### PR #N: FR-X (severity): short title (YYYY-MM-DD merge date)`, primary header for a fitness-remediation PR that closes one FR. Severity values mirror the TODO backlog tiers: `high[critical]`, `high`, `medium`, `low`. The Pass-1 ⚠️ confirmed-with-modification flag is informational and stays in the body, not the heading.
- `### PR #N: FR-X (sev) + FR-Y (sev): short title (YYYY-MM-DD)`, for multi-FR PRs.
- `### PR #N: Sweep N iter M close-out: short title (YYYY-MM-DD)`, for validation-sweep close-out PRs (no single FR anchor; bundle multiple findings).
- `### PR #N: short title (YYYY-MM-DD)`, for non-FR PRs (workflow/infrastructure changes).
- `### FR-X (severity): short title (closed by PR #N, YYYY-MM-DD)`, for FR-N cross-reference entries that need separate callouts (items closed across multiple PRs or items whose own narrative deserves its own H3 separate from the closing PR's entry).
- **One or two sentences** describing what was accomplished. No file links, no version bumps, no rationale. The narrative job belongs to CHANGELOG; the at-a-glance index job belongs to DONE.

The heading convention was harmonised with TODO's backlog format in PR #163 (2026-06-21) so a maintainer reading either file can scan FR-N + severity at the heading level without parsing the body paragraph. The "scrolling battle-text" body convention (1-2 sentences, no links, no version bumps) was adopted in PR #174 (2026-06-21); PR #175 retroactively shortened earlier entries to the new shape.

---

## Closed items

### PR #899: deep-assessment r3 clear-mechanical remediation batch (6 findings) (2026-07-13)

Maintainer-signed-off r3 remediation: closed FR-207 (added the Board/CEO audience to the README x2, the build-portal.py docstring + emitted portal overview, and regenerated the portal), FR-209 (three quickstart->startup-roadmap composition carriers in the implementation roadmap), FR-213 (dropped the stale INAI reconciliation caveat in the Mexico annex), RB-FFIEC-CAT (marked the FFIEC CAT retired 31 Aug 2025 with its successors in the FS annex), DA-DORA-A12 (corrected the DORA Article-12 label to backup/restoration/recovery), and DA-AIACT-A26 (dropped the "efficient use" mis-attribution from EU AI Act Article 26). The DA-ASVS High + the FR-200/FR-201 Highs were routed to a fresh session per the maintainer's sign-off direction.

### PR #826: reconcile the guardrail-review routing-tag convention (closes TODO §3.49) (2026-07-12)

Deep-assessment r2 finding F2: reworded the [`guardrail-review` skill](../dev-security/claude-rules/skills/guardrail-review/SKILL.md) (the routing and verification sections) from the prescribed `[guardrails]` bracket tag to the `(rN guardrails, size, effort)` parenthetical convention the backlog actually uses (0 bracket tags vs 5 parentheticals). Traceability preserved; matches practice. Closes TODO §3.49.

### PR #824: positional backlog-token audit gate 69 (closes TODO §3.4) (2026-07-11)

Landed the HELD, reconciled gate 69 (the `worker-20260708-fable/positional-token-lint-313` delivery) as the `/deep-assessment` r2 coverage obligation: a new corpus lint ([`tools/lint-positional-backlog-tokens.py`](../tools/lint-positional-backlog-tokens.py)) flagging renumber-fragile positional backlog references (a `TODO` / `backlog item` qualifier followed by a `§`/`P`-prefixed or dotted section token) that should use a stable coded id or topic name, the mechanical form of the CLAUDE.md §N-orphan guard scoped to the corpus. Wired across all four gate-parity surfaces with a five-case regression class; the three live carriers (two in the audit-programme spec, one in the citation-verification spec) were reworded to green it. The held branch was landed onto post-#823 `main` by taking its substance files (gate, wiring, fixture, spec, carrier fixes, SKILL count) onto a fresh branch and re-authoring the version/CHANGELOG/DONE bookkeeping for #824; the gate was re-run on current `main` and confirmed 0 residual carriers (the set stable since the branch's derivation). Closes TODO §3.4.

### PR #820: small-cleanup batch, breadcrumb collisions + AIDA bare-listing annotation (closes TODO §3.37, §3.45) (2026-07-11)

Closed two P3 tidies. **§3.37:** dropped the two colliding `(was X.Y)` renumber breadcrumbs (`(was 3.22)` on §3.19, `(was 3.24)` on §3.20) whose numbers had been reused by since-closed items, resolving the latent ambiguity. **§3.45:** annotated the four neutral AIDA bare-listing reference cells "(lapsed)" for corpus-wide uniformity (policy-exception risk-approval row; security AI-data-handling row; the doc-index register's AI-compliance-policy and AI-risk-methodology reference cells). Also opened §3.47 (TODO adoptability: strip internal working-provenance annotations) per the maintainer's direction, and fixed the #819 `/validate-pr` P1-intro contradiction.

### PR #819: §N-orphan reference-key-width clause codified (closes TODO §3.46) + #818 findings (2026-07-11)

Codified the reference-key-width axis into the [`.claude/CLAUDE.md`](../.claude/CLAUDE.md) §N-orphan close-out guard (a section/item close greps every key form the closed thing is cited by, `§N` / `PN.M` / `item N` / ranges `§A-§B`, not only bare `§N`), extinguishing the class that recurred three times this session (#814 §3.36-vs-item-7; #817 §1.5-§1.8 range; #818 CLAUDE.md §1.8 line). Also fixed the two #818 in-window `/validate-pr` findings: the stale CLAUDE.md §1.8-residual line (now "§1.5 through §1.8 all closed") and the stale TODO P1 intro (the §1.5 "residuals split below" prose the maintainer flagged, P1 now has no open items). Closes TODO §3.46.

### PR #818: ref-side corrections complete (closes TODO §1.8) (2026-07-11)

Closed TODO §1.8 (ref-side corrections). Confirmable corrections landed in `grc_library_ref` PR #52 (b NERC CIP-015-2 not-yet-in-force annotation + version_sensitive; c CAN/DGSI 101:2025 title; d TBS Directive in-force framing; e OECD revised 3 May 2024); (a) WCO SAFE 2021 to 2025 edition refresh applied via the maintainer's ingest (ref #53, 2021 retired to .superseded/); and the (c) filename slug rename applied in ref #54. Corpus side: the register WCO SAFE row was already at the 2025 edition (#751); its verified date is bumped to 2026-07-11 to sync with the ref ledger's fresh upstream confirmation. Also carries the #817 /validate-pr CLAUDE.md stale-range fix.

### PR #817: register-currency drift-check tool (closes TODO §1.7) (2026-07-11)

Built [`tools/audit-register-currency.py`](../tools/audit-register-currency.py) per the `currency-ledger-sync` delivery spec: an advisory (not-gate) cross-repo tool reporting drift between the `grc_library_ref` currency ledger (`catalogue.yml`) and the corpus register `register-canonical-citations.md` across five checks (register-behind, version-disagreement, upstream-URL-mismatch, ledger-held-stale, unmatched-rows). Stdlib-only line parser (no PyYAML); exact-then-shortest-prefix designation matching; edition-token version comparison; `--ledger`/`--register`/`--strict`/`--self-test`; exits 0 by default (skip+0 if the ref checkout is absent). Its first live run flagged 4 register rows behind the ledger and the WCO SAFE 2021->2025 held-stale (which §1.8 addresses ref-side).

### PR #816: AI gaps-and-expansion workstream complete (closes TODO §2.2) (2026-07-11)

Closed TODO §2.2 (the maintainer-directed AI gaps-and-expansion workstream, PRs 0-10): PR 0 shipped the five corpus-accuracy fixes (#784-#788); PR 1-10 shipped the content-authoring builds including the six new documents A1-A6 (A5 value-and-decision-governance authored as original governance constructs in #815, A6c synthetic-content provenance in #809), each with per-PR QA and a skeptical or high-assurance verifier. The whole-project `/deep-assessment` is a separate maintainer-invoked decision (not part of this item and not a TODO); it is decoupled from §2.2 at the maintainer's 2026-07-11 direction.

### PR #814: CHANGELOG per-PR sweep-step wiring (closes TODO §3.17) (2026-07-11)

Closed TODO §3.17 (per-PR sweep-step wiring): satisfied by #813, which added the advisory detailed-mirror-sweep close-out bullet to `.claude/CLAUDE.md`. Also the in-window fix for the #813 `/validate-pr` finding: #813's deletion of deferred-protected-changes item 7 left §3.17's body pointing at the now-removed item; closing §3.17 (its deliverable done) resolves the dangling reference, and the §3.36 body's `§3.16/§3.17` sweep-model citation was repointed to §3.16.

### PR #812: completion-verification file-type-width axis (closes TODO §1.9) (2026-07-11)

Closed TODO §1.9 (log-mining #688/#689): added a fourth axis, FILE-TYPE WIDTH, to the [`.claude/CLAUDE.md`](../.claude/CLAUDE.md) completion / contradiction-grep guard (beside pattern width, scope width, and separator tolerance). A rename, cutover, token-migration, or completion grep must now run over ALL file types the token can inhabit (`.py` and docstrings, `.yml`, `.json`, `.sh`, and the gate-exempt `.claude/` and `.working/` trees), not `.md` alone, because the prior axes were implicitly `.md`-scoped. Cites the #746-to-#811 recycled-section-number stale-pointer as the class it guards. Protected CLAUDE.md edit; lint-language run pre-commit.

### PR #811: unheld-citation acquisition complete (closes TODO §1.11) (2026-07-11)

Closed TODO §1.11 (the WS 0.5 unheld-citation acquisition, routed to the maintainer source-drop queue in #788): all seven citations are now held in `grc_library_ref` (six ingested in ref PR #41; IEEE 7000-2021 ingested separately by a maintainer worker), and the one corroborative IEEE 7000-2021 §7.3 locator was verified against the held text during PR 1. Bookkeeping close with the §N-orphan cross-file cleanup: reworded the §2.2 historical reference and fixed a pre-existing stale `.claude/CLAUDE.md` example pointer (it still cited the recycled §1.11 number for the Brazil-citation tracker closed in #746).

### PR #810: privacy-domain AIDA section-29 residual reconcile (closes TODO §1.10) (2026-07-11)

Closed the privacy-domain residual of TODO §1.10: the lapsed AIDA section 29 was still mapped as a LIVE AI-impact / DPIA obligation in `privacy/template-dpia.md`, `privacy/procedure-privacy-impact-and-cross-border-transfer.md`, and `privacy/annex-privacy-jurisdiction-index.md`, plus stale AIDA/CPPA "(pending)" hedges in the compliance matrix and the document-index register. Reconciled to the in-force Canadian instruments (Quebec Law 25 CQLR P-39.1 sections 3.3/12.1, private sector; Treasury Board Directive on Automated Decision-Making section 6.1 Algorithmic Impact Assessment, federal institutions), with AIDA marked lapsed, verified against the held Quebec Law 25 and TBS Directive texts. The four neutral bare-listing AIDA cells were correctly left neutral. §1.10 fully closed.

### PR #808: nested-markdown-link detection gate, gate 68 (closes TODO 3.44) (2026-07-11)

Added gate 68 ([`tools/lint-nested-markdown-links.py`](../tools/lint-nested-markdown-links.py)), a code-span-aware detector of the `[[text](url)](url)` nested-link malformation that recurred in #802 (gate-blind to the link-coverage and broken-link gates), with a regression fixture and the four-surface wiring; closes TODO 3.44 (part 1 cleanup landed in #807, part 2 gate here). Also tightened the #807 grep-fidelity overclaim surfaced by the #807 `/validate-pr` (F1).

### PR #806: AI workstream, AIDA / EO-14110 obligation-carrier reconcile (advances TODO §1.10) (2026-07-11)

Reconciled the AIDA live-framing obligation, alignment, and applicability carriers across eight non-privacy corpus documents, and both US EO-14110 carriers, to the lapsed / rescinded framing (citing the in-force Treasury Board Directive on Automated Decision-Making and the federal Voluntary Code of Conduct on Generative AI); the EO-14110 rescission (20 January 2025) was confirmed upstream against the Federal Register. TODO §1.10 is narrowed to the remaining privacy-domain AIDA section-29 obligation-mapping residual (routed to a privacy follow-up).

### PR #804: AI workstream, OECD-AI-Principles year harmonization (closes the TODO §1.10 OECD bullet, corpus side) (2026-07-11)

Harmonized the five corpus carriers of the OECD AI Principles citation year off the stale "2023" form to the current "(2019, updated 2024)" form (four docs) and the "(2019 Recommendation as updated 2024)" form (policy-ai-compliance §12, matching its own §1.1), resolving the #798/#785/#786-flagged inconsistency; the 2023-vs-2024 currency was resolved upstream in #798 (OECD/LEGAL/0449 revised both 8 November 2023 and 3 May 2024, 2024 current). The `grc_library_ref` catalogue "revised 2023" correction is folded into TODO 1.8(e) as the cross-repo ref-side half.

### PR #784: AI workstream PR 0.1, §36 CSA AICM re-map (advances TODO §2.2) (2026-07-10)

Re-mapped the invalid `AI-TM/SC/PP/AU/EC-*` pseudo-code family (a fourth invalid CSA control-code family, gate-48-invisible because the `AI-XX-NN` shape is excluded by the domain-token regex like the corpus-internal `AI-GOV` IDs) across all 9 rows of `ai/standard-ai-and-agentic-development-security.md` §36 to real AICM v1.1.0 controls, via the full high-assurance harness (research fan-out, invariant floor, deterministic apply + re-parse, and an independent refute-briefed adversarial-verifier SHIP): prompt-injection to AIS-15/AIS-09, supply-chain to STA-10/STA-09, sensitive-data to DSP-17/IAM-16, tool-misuse to AIS-11/IAM-18, unsafe-code to AIS-10/AIS-05, excessive-agency to IAM-18/IAM-05, overreliance to GRC-15/GRC-13, resource-exhaustion/DoS to I&S-02/I&S-09, hallucination to AIS-10/LOG-16. Also corrected the header to "CSA AICM v1.1.0" and the two LLM09 cells to "LLM09 Misinformation" (the OWASP LLM Top 10 v2.0 rename the doc already commits to via "LLM10 Unbounded Consumption"). Gate 48's Check 5 (built #782) now mechanically validates the re-mapped column. Also discharged the #783 fragile-token finding (the two `§3.40` test-comment refs reworded to `PR #782`).

### PR #782: Deep-assessment r1 R11 §3.40, framework-column CCM/AICM family-validation gate (closes TODO §3.40) (2026-07-10)

Hardened gate 48 (`lint-ccm-aicm-citations.py`) with Check 5: a control-code-shaped token in a framework-alignment column headed "CSA CCM" / "AICM" whose domain prefix is outside the CCM/AICM family (the blind spot the recognized-prefix code-validity check leaves) is now flagged as an unknown family, scoped to that named column so other frameworks' codes are untouched. On first corpus run it immediately caught a third invalid family, `GVN-05`, in two pack AI-security docs (after the `ISM` family R11 closed and the `END` family §3.41 closed), corrected to `GRC-15` and `IAM-10` (maintainer-confirmed). Added a detect + false-positive-guard regression fixture and updated the docstring and the §6 narrative in lockstep; no new gate (count stays 67).

### PR #781: Deep-assessment r1 R11 residue §3.41, matrix-fit loose-supporting reconciliation + an invalid CCM code family (closes TODO §3.41) (2026-07-10)

Closed §3.41 via a held-source-verified control-fit remap across 6 corpus docs plus the compliance matrix: the loose-supporting rows (media-handling DSP-07 to DSP-04/DSP-10/DCS-04/DSP-02, library-quality COBIT APO01 to APO11 "Managed Quality", logging LOG-12 to LOG-09) and the two matrix-vs-per-doc divergences (threat-modelling CCC-06 dropped to match the doc's TVM-04; media-handling matrix set reconciled to DSP-04/DCS-05/DSP-02). A held-source judge caught two mis-attributions beyond the routed scope, both fixed: an entire invalid `END-01`..`END-05` CCM family in the endpoint doc (the real endpoint domain is `UEM`, a §3.40-class correctness defect the existence gates skip) remapped to UEM controls, and `CEK-14` "Key Destruction" mis-cited on the media digital-transfer row corrected to `CEK-03` "Data Protection". The two stale paired surfaces in the doc-index register were updated; §3.40 gained the END family as its second confirming instance.

### PR #778: Deep-assessment r1 §1.6, EN 54 series currency confirmed + stamped (closes TODO §1.6) (2026-07-10)

The EN 54 fire-detection register row was `needs-reconfirm`; confirmed upstream that EN 54 is an active CEN/TC 72 series (25+ parts, many harmonized under the Construction Products Regulation (EU) 305/2011), and the corpus cites it only at series level (BMS overlay annex + doc-index register), so stamped the row `verified 2026-07-10` at series level rather than enumerating 25+ parts the corpus does not cite at part level. Also added TODO §3.42 (the ISO/IEC 5259 + AI-governance new-ingest reference-breadth pass surfaced by the post-PR ref-repo resync).

### PR #777: Deep-assessment r1 §1.5, ICAO Doc 10026 mis-citation corrected to Annex 17 (closes TODO §1.5) (2026-07-10)

The corpus cited "ICAO Doc 10026" as the Manual on Aviation Security across three carriers (canonical-citations register, logistics sector annex, and the Q4 citation-verification worklist whose fabricated 404 store URL seeded the error); Doc 10026 is actually the Report of the Legal Commission and the AVSEC manual is the Restricted Doc 8973. Per the maintainer's decision, corrected all three to ICAO Annex 17 (Chicago Convention), confirmed upstream (title + Edition 12, 2022).

### PR #776: Deep-assessment r1 R12, reference-breadth citations (closes TODO §3.29) (2026-07-10)

The r1 `/reference-audit` reference-breadth track: 27 held-but-unused authoritative citations across 7 domain clusters (risk/ERM, privacy, IAM, incident-response, resilience/EA, AI, dev-security/cloud/metrics/workforce), plus 2 bonus precision fixes (the NIST SP 800-207A citation-title correction and the ISO/IEC 27017 dangling-registration resolution), applied per-cluster across PRs #770-#776. Each cluster was held-edition-confirmed, refute-briefed-verifier-SHIP'd, and post-merge `/validate-pr` 0-findings. Closes §3.29 and discharges the r1 `/deep-assessment` reference-breadth findings.

### PR #769: Deep-assessment r1 R11, `/matrix-fit` source-doc semantic-fit pass (closes TODO §3.25) (2026-07-10)

Ran `/matrix-fit` over the 27 source-doc framework-table rows the r1 pass deferred; two refute-briefed judges surfaced 12 held-verified valid-but-wrong-control mismatches (SEF-06->CCC-02, I&S-09/SEF-01->LOG codes, CCC-06/CCC-04->TVM-04, DSP-02->DSP-08, DSP-07->DCS-05/DSP-02), all fixed in-window, plus an invalid `ISM-xx` code family (8 instances cited as CSA CCM in 2 docs) remapped to real CCM controls; routed the gate blind-spot to §3.40 and the loose-supporting residue to §3.41.

### PR #767: Deep-assessment r1 R9, CI workflow hardening (closes TODO §3.30) (2026-07-10)

Hardened [`.github/workflows/quality.yml`](../.github/workflows/quality.yml) per the project's own CI/CD-gates and supply-chain rules: added a least-privilege top-level `permissions: contents: read` block (the lint job is read-only) and SHA-pinned both GitHub actions (`actions/checkout` to `34e1148…` # v4, `actions/setup-python` to `a26af69…` # v5, real SHAs fetched via `gh api`) with version comments. A follow-on TODO (§3.39) tracks the Dependabot-vs-manual refresh decision so the SHA-pins do not silently rot.

### PR #766: Deep-assessment r1 R2, portal generator emits `ai/jurisdictions/` + routes Compliance to the reverse crosswalk (closes TODO §3.21) (2026-07-10)

The audience-shaped portal generator ([`tools/build-portal.py`](../tools/build-portal.py)) omitted the AI jurisdiction annexes (no audience selected an `ai`-domain `Annex`) and never routed the Compliance audience to the reverse framework crosswalk. Added an `ai/jurisdictions/` path-prefix selector and a `Reverse Framework` title selector to the Compliance audience; the regenerated `docs/portal.md` now lists the EU AI Act and Colorado AI Act annexes and the Reverse Framework Control Crosswalk under Compliance (closes the Sweep-92 B-5 gap and the r1 R2 finding as one generator change).

### PR #765: Deep-assessment r1 R7, `/screen-publications` added to the `/deep-assessment` phase-3 set (closes TODO §4.10) (2026-07-10)

Added `/screen-publications` (the publications-screening cadence shipped #722) to all four hardcoded phase-3 instrument lists in the `deep-assessment` SKILL and command, completed the `## See Also` with the previously-omitted `reference-audit` plus `publication-screening`, and reconciled the "count-free / inventory-deriving" claim with the obligation-synced named enumeration; pack `1.59.4` to `1.59.5`. (The TODO §4.10 rotation was missed in #765 itself and is completed here in #766, an in-window catch.)

### TODO §3.5: Deep-assessment r1 R8a, gate-31 future-dated-Date detection (closed by PR #764, rotation completed in the Sweep 95 close-out, 2026-07-10)

Gate 31 (`lint-document-date-staleness.py`) was extended in #764 to also fail on a metadata Date dated after the current UTC date (a "last updated" field cannot be in the future), with a far-future regression fixture and the §5 gate-31 narrative updated. #764's CHANGELOG did not use a "closes TODO §3.5" phrasing, so gate 57 did not flag the missing rotation; Sweep 95 Subagent-adjacent triage caught the stale §3.5 heading and this close-out completes the rotation.

### PR #759: Deep-assessment r1 matrix GRC-07 semantic-fit corrections (closes TODO §3.24) (2026-07-10)

Corrected three compliance-matrix regulatory-mapping rows that carried off-subject GRC controls where GRC-07 (Information System Regulatory Mapping) is the on-point control: the Global Regulatory Applicability register (GRC-06 to GRC-07) and the Privacy Jurisdiction Index (GRC-03 to GRC-07) had their off-subject codes replaced, and the Compliance Obligations Template gained GRC-07 alongside its existing GRC-06 (which fits its obligation-ownership aspect). Held-verified by the r1 matrix-fit judge against the CCM v4.1 control titles.

### PR #758: Deep-assessment r1 claim-fit precision fixes (closes TODO §3.26 + §3.27) (2026-07-10)

Two held-verified claim-precision corrections: narrowed the EU AI Act serious-incident reporting citation from the over-broad "Article 65 to 74" to Article 73 (plus the Article 26(5) deployer duty) in the legal-and-regulatory-compliance policy; and reworded the executive-review cadence from "at least annually per ISO 9001 §9.3 and ISO/IEC 27001 §9.3" to "at planned intervals (the organization sets at least annually)", since ISO/IEC 27001 §9.3 prescribes planned intervals, not an annual cadence. The ISO 9001 §9.3 held-verification continues in RB-R6 (source-not-held).

### PR #757: Deep-assessment r1 EU AI Act citation-accuracy sweep (closes TODO §3.28) (2026-07-10)

Corrected the EU AI Act structure citations from stale 2021-proposal-era "Title" numbering to the enacted Regulation 2024/1689 Chapters across four docs (Chapter II for prohibited practices at Article 5, Chapter V for GPAI-with-systemic-risk, Chapter IX for post-market monitoring / serious-incident reporting), and aligned the serious-incident Art 3(49) paraphrase to the four statutory limbs. Bundles the r1 clear-fix F12 (which a full-file grep widened from one flagged line to seven carriers) with the same-doc §3.28 claim-precision fix (F17); all verified against the held EU AI Act text.

### PR #750: Mexico LFPDPPP privacy annex, closes TODO §5.8 Mexico bullet (2026-07-09)

New `privacy/jurisdictions/annex-privacy-mexico.md`, a standalone per-regime annex for Mexico's 2025 LFPDPPP (DOF 20 March 2025): the Secretaría Anticorrupción y Buen Gobierno authority (the former INAI extinguished), Article 5 principles, consent and privacy notice, ARCO rights (20-day response), cross-border transfers, security and breach, and UMA-based enforcement (up to 320,000 UMA, doubled for sensitive data). Corrected the stale 2010/INAI/MXN-320m facts in the Latin America annex and wired the standalone into the privacy jurisdiction index, doc-index, and coverage-gaps; discharged the fr-59 Mexico accepted-unverified tracker. Verified against the held 2025 text with WebSearch currency confirmation.

### PR #749: FR-62 (medium): Colorado AI Act jurisdiction annex, closes FR-62 (2026-07-09)

New `ai/jurisdictions/annex-ai-us-colorado.md`, the second founding annex of the AI jurisdictions subdirectory: a two-regime view of Colorado's AI statute (SB 24-205 re-enacted by SB 26-189, operative for consequential decisions on or after 1 January 2027), covering developer and deployer duties, consumer rights and meaningful human review, AG-exclusive enforcement with a 60-day cure, and the SB24-205-to-SB26-189 transition. Closes FR-62: both founding AI-jurisdiction annexes (EU #743, Colorado #749) are now applied; remaining jurisdictions are the source-gated §5.9 expansion.

### PR #746: TODO 1.11 Brazil ANPD citation verification, primary-source close (2026-07-09)

Closed the last P1 residual: the ANPD Resolution CD/ANPD No. 15/2024 small-agent deadline-doubling sub-clause (Article 6 §8, Article 9 §6, "contados em dobro"), previously confirmed only at secondary tier, upgraded to a PRIMARY-source confirmation against the held Diário Oficial da União text (DOU 26 April 2024, now in `grc_library_ref` ref #35). Dropped the "primary re-confirmation pending" notes from `privacy/jurisdictions/annex-privacy-brazil.md` and the breach-response matrix; the canonical-citations register row needed no change (version-currency and content-attribution axes kept separate, per the TODO instruction). Discharges the accepted-unverified tracker. Also carried the LOW citation-name harmonization (Whistleblower to Whistleblowing) in the whistleblower procedure, #745's QA batch, and a restructure of the handoff Current-truth line.

### PR #745: FR-154 sub-item 5, whistleblower feedback ceiling (closes TODO 2.9) (2026-07-09)

Closed the last open FR-154 sub-item (§2.9), the whistleblower investigation feedback ceiling, now that the EU Whistleblower Directive 2019/1937 is held in `grc_library_ref`. Made `governance/procedure-whistleblower-and-incident-reporting.md` §4.4 operationally precise: feedback within a reasonable timeframe not exceeding three months from acknowledgment (internal-channel ceiling, verified against held Article 9(1)(f)), with the Article 11 external-channel timeframe (up to six months in duly justified cases) noted. TODO §2.9 fully CLOSED (5 of 6 sub-items in #738, sub-item 5 here; sub-items 2 and 7 did not reproduce).

### PR #744: TODO 4.6 S-c closed as satisfied (2026-07-09)

Closed TODO 4.6 item S-c (adopter-direction role-substitution demo) as SATISFIED by the existing `docs/worked-example-adoption.md` (whose Step 3 already walks role substitution, the missing-role case, and the private-overlay rule), per the maintainer's 2026-07-09 decision. No new document was built (a third overlapping adopter doc was avoided); the stale delivery gap analysis had been superseded by `worked-example-adoption.md` landing after the worker's source read. Bookkeeping PR also carried #743's QA batch and a handoff append-not-reconcile-residual fix.

### PR #743: EU AI Act jurisdiction annex (TODO 5.1/5.9, part 1 of 2) (2026-07-09)

Applied the `worker-20260703-a/fr-62-eu-ai-act-annex` delivery as a new `ai/jurisdictions/annex-ai-european-union.md` (founds the `ai/jurisdictions/` subdirectory), an 11-section per-regime view of EU AI Act Regulation (EU) 2024/1689: operator roles (Art 3), risk tiers (Art 5/6 + Annex III), the high-risk provider chain (Art 16/49/50), the deployer chain (Art 26/27), GPAI (Art 51/53/55, the 10^25 FLOP systemic threshold), the phased timeline (Art 113, applies 2 Aug 2026), and penalties (Art 99/101). Every article verified against the held enacted text; a Limitations caveat flags the pending, not-adopted Digital Omnibus on AI (COM(2025) 836). Wired into ai/README, the doc-index register, the decision-tree §5.1, and the glossary. Maintainer-approved (2026-07-09) merge-as-is + caveat. Sibling Colorado AI Act annex (the second §5.1/5.9 founding annex) remains to build.

### PR #742: multi-entity adoption guidance (TODO 4.6 S-d) (2026-07-09)

Closed TODO 4.6 item S-d: applied the `worker-20260703-a/s-d-multi-entity-adoption` delivery as a new `docs/adopter-guide-multi-entity.md`, group/multi-entity adoption guidance covering three topologies (single shared library, per-entity forks with a group baseline, hub-and-spoke with entity annexes) with per-topology versioning/CalVer, role-mapping-when-authorities-differ, jurisdictional layering (reusing the jurisdiction-annex model), and a trade-offs table. Corpus-grounded synthesis (no external source); wired via the adopter-guide cross-reference (docs/ meta-documents are outside the taxonomy/doc-index scope). The sibling S-c was NOT built (its gap was already filled by `docs/worked-example-adoption.md`); it stays open pending a maintainer decision.

### PR #739: eIDAS2 public-sector annex (section 5.7 EU eIDAS bullet) (2026-07-09)

Closed the EU eIDAS bullet of TODO §5.7: applied the `worker-20260703-a/eidas2-public-sector-annex` delivery as a new `compliance/public-sector/annex-eidas-requirements.md` (8-section FedRAMP-shape annex), grounding eIDAS (Regulation 910/2014 as amended by Regulation 2024/1183, "eIDAS2") by role, wallet-relying party (Art 5b: registration, data-minimization, self-identification, pseudonym acceptance), trust-service provider (qualified/non-qualified + NIS2 Art 31 supervision cooperation), public-sector body (Art 5f(1) immediate acceptance), and wallet provider (Art 5a: assurance-high, dashboard/GDPR-erasure, conformity certification). The 24-month wallet and 36-month private-relying-party (Art 5f(2)) phase-in clocks framed as relative to the implementing acts (not fixed dates); penalties (Art 16(2)) as a floor-on-the-maximum (EUR 5 000 000 or 1% turnover, whichever higher, for trust-service providers). Every anchor verified against the held eIDAS2 text; the file name is a stricter-safe default (FedRAMP `annex-<regime>-requirements.md` convention) logged in pending-decisions. Also fixed the #738 TODO:60 dangling link. The other §5.7 overlays stay source-gated.

### PR #738: FR-154 operational-vagueness cluster, 5 of 6 sub-items (2026-07-09)

Advanced TODO §2.9 (FR-154; NOT closed, sub-item 5 deferred): applied 5 of the 6 reproducing operational-vagueness sub-items across 5 files under the maintainer's orchestrator-sets-stricter-safe decision model, sub-item 1 (DSR forward-clock harmonized in `privacy/procedure-data-subject-rights-management.md`), 3 (Critical-risk interim containment authority in `risk/procedure-risk-assessment-methodology.md`), 4 (tier/severity-conditioned supplier remediation gate in `supply-chain/procedure-supplier-due-diligence.md`), 6 (dept-continuity-template MTD/RTO/RPO derivation guidance + illustrative row in `resilience/template-departmental-continuity-plan.md`, per the BIA + ISO 22301), and 8 (model-lifecycle recorded-threshold obligation in `ai/procedure-ai-model-lifecycle-management.md`, per ISO/IEC 42001 Section 9). Each value anchored to an internal canonical source; logged in `pending-decisions.md` for confirm-or-redirect. Sub-items 2 and 7 do not reproduce (already operational). Sub-item 5 (whistleblower feedback ceiling) DEFERRED, its 3-month anchor rests on the unheld EU Whistleblower Directive 2019/1937; §2.9 stays open for it.

### PR #737: NIS2 annex operational deepening (2026-07-09)

Closed TODO section 2.13 (NIS2): applied the `worker-20260703-a/nis2-implementation-deepening` delivery to `compliance/annex-nis-2-implementation.md` (1.1.0 to 1.2.0). Added a "DORA and sector-specific lex specialis (Article 4)" section (the reciprocal of the #736 DORA-side boundary: financial entities in scope of DORA follow DORA for the equivalent risk-management and incident-reporting requirements, NIS2 Articles 21/23 and Chapter VII not applying to that extent; scoped displacement, not blanket exemption; cross-referenced to the DORA annex) and a "Supervision and penalties (Articles 32 to 34)" section (essential = comprehensive ex-ante+ex-post per Art 32, important = ex-post-only per Art 33 with the distinction framed in recital 122; Art 34 directive-level fine floors EUR 10M/2% essential, EUR 7M/1,4% important). Existing Art 20/21/23 mappings verified accurate (not corrected). All anchors verified against the held NIS2 directive; completes the DORA/NIS2 boundary pair.

### PR #736: DORA annex operational deepening (2026-07-09)

Closed TODO section 2.12 (DORA): applied the `worker-20260703-a/dora-operational-deepening` delivery to `compliance/financial-services/annex-dora-implementation.md` (0.0.5 to 0.0.6). Deepened the thin Critical-ICT-TPP subsection (ESA designation and Article 31(2) criteria, Lead Overseer appointment and Article 35 investigation/inspection powers, the Article 31(12) Union-subsidiary requirement for third-country providers, and the adopter consequence), added the Article 28(3) register-of-information operational detail (entity/sub-consolidated/consolidated levels, critical/important distinction, at-least-yearly reporting), enriched Pillar 3 TLPT scope (Article 26(2) live-production/critical-functions), and added a NIS2 Article 4 lex-specialis boundary cross-referenced to the NIS2 annex. Apply-time reconciliation: the live annex already carried the TLPT cadence ("every three years"), so it was verified accurate (Article 26(1)) rather than re-added; DORA is in force (17 January 2025). All anchors verified against the held DORA/NIS2 text.

### PR #735: FR-41 unified ADM/AI/FRIA workflow (2026-07-09)

Closed TODO section 2.10 (FR-41): applied the `worker-20260703-a/fr-41-article-22-fria` delivery as a new Procedure, `ai/procedure-integrated-ai-and-privacy-assessment.md` (home dir maintainer-chosen), the router that, given a system's regime triggers, decides which of the GDPR Article 35 DPIA, the AI System Impact Assessment, the GDPR Article 22 ADM register entry, and the EU AI Act Article 27 FRIA are required and how they compose (one limb each, shared evidence, FRIA complements not substitutes for the DPIA per Article 27(4)). Wired the four carriers (ADM register, DPIA template, AI-IA procedure Step 5 closing the one-way link, algorithmic checklist with a semantic B3 correction from "PIA or AI-IA / FRIA" alternatives to the composed set). Anchored to held GDPR Article 22/35 and EU AI Act Article 27; the FRIA applicability date (2 August 2026) is cited from the held Article 113. Also fixed the stale P2 count block (the #734 /validate-pr F1: 7 to 5 open items, adding the 2.8 and 2.10 closures).

### PR #734: FR-74 Schrems II operational deepening (2026-07-09)

Closed TODO section 2.8 (FR-74): applied the `worker-20260703-a/fr-74-schrems-ii` delivery, deepening the EU cross-border treatment in `privacy/procedure-privacy-impact-and-cross-border-transfer.md` Step 4 from a one-line SCC stub to a full GDPR Chapter V / Schrems II operational sequence (transfer-tool selection ladder, the six-step assessment run through the shipped TIA template, supplementary-measures selection, the suspend-or-notify hard stop, and re-assessment triggers), with a pointer from the EU jurisdiction annex's transfer-mechanism inventory. Anchored to GDPR Chapter V (held) and the shipped TIA; kept mechanism-generic (points to the annex's current adequacy list rather than asserting a specific adequacy decision, since EUR-Lex is unfetchable to confirm the DPF status upstream); EDPB methodology routed via the TIA's existing attribution, not the untrusted publications extract.

### PR #733: US HIPAA healthcare annex (section 5.4 US bullet) (2026-07-09)

Closed the US HIPAA bullet of TODO section 5.4: applied the `worker-20260703-a/us-hipaa-healthcare-deepening` delivery as a new `compliance/healthcare/annex-healthcare-united-states.md` (US operational regime map), deepening the sector annex with role determination, the Security Rule safeguard families (45 CFR 164 Subpart C), the Breach Notification mechanics and 60-day/500-individual timelines (Subpart D), the four-tier civil-money-penalty structure (45 CFR 160 Subpart D, amounts deferred to the inflation-adjusted 45 CFR part 102 rather than asserted), and the NIST SP 800-66r2 crosswalk. Deepens by cross-reference (the NPRM and privacy-law framing stay in the sector and privacy annexes). Citations verified against the held 45 CFR 160/162/164 extracts; codified Security Rule confirmed current upstream (Subpart C unchanged since 2016; the 2024 NPRM remains proposed, no final rule as of 2026-07-09). The remaining section-5.4 overlays (UK NHS DSPT, EU MDR/IVDR, Canada, Australia) stay open.

### PR #732: Session-depth handoff calibration codification (2026-07-09)

None (maintainer-directed discipline calibration, not a backlog item). Codified the maintainer's 2026-07-09 direction that session depth is a CONTRIBUTING (never SOLE) factor to a handoff PROPOSAL into the `.claude/CLAUDE.md` wind-down framework and the project-agnostic `session-lifecycle` pack rule (byte-identical mirror synced; pack `1.59.3` to `1.59.4`): depth warrants an offered handoff only alongside a very-long-run-ahead or excessively-sensitive fresh-context work (the first `/deep-assessment` run), never on its own. Also closed a #731 `/validate-pr` Low (removed the closed FR-60 from TODO's egress-deferred list).

### PR #731: TODO 2.2 FR-60 HIPAA operational deepening (2026-07-09)

Closed FR-60 (§2.2): applied the `worker-20260703-a/fr-60-hipaa-deepening` research delivery as a new `compliance/healthcare/procedure-hipaa-operational-compliance.md` Procedure (Option B, maintainer-chosen) operationalizing the HIPAA clocks and content duties: individual right of access (30 days + one extension, 164.524), amendment and accounting (60 days, 164.526/528), Notice of Privacy Practices and minimum necessary (164.520/502/514), six-year documentation retention (164.316(b)(2), 164.530(j)), the four-factor breach-determination test and notification clocks (164.402/404/406/408/410/414), and business associate agreement content (164.502(e)/504(e)/314(a)). Citations verified against the held 45 CFR 164 extract and confirmed current upstream (eCFR: Part 164 unchanged since 2024-06-25; the 2026-07-02 Title-45 amendment did not touch it). The annex links to it; the healthcare README and the document-index register carry it.

### PR #730: Delivery-status anti-recurrence preventions (2026-07-09)

Not a pre-existing TODO item; a maintainer-directed anti-recurrence action after a session-level failure (a false "scratch backlog applied" claim, ~20 applicable deliveries mislabeled "egress-gated" without per-item checking, and a narrated-not-executed start-side check for TODO 3.13 while its delivery existed). Shipped three preventions: `tools/audit-delivery-status.py` (advisory inbox-vs-`TODO.md` reconciliation, PENDING/APPLIED/UNMAPPED, plus an `--item` executed start-side check), a `.claude/CLAUDE.md` delivery-status-claim discipline (quote the tool's output; per-item blocking reasons never generalized), and `/resume` step-3 wiring. The tool immediately surfaced 33 PENDING unapplied deliveries.

### PR #729: TODO 3.23 gate-67 region-scoping + SR-5 ref-tool polish close (2026-07-09)

Closed 3.23 (region-scope gate 67's Document-Type enumeration parity checks): checks 3 and 4 now read each surface's specific doctype table/list block (a heading block for the six heading-bearing surfaces, the distinctive prefix-list line for the heading-less AI-ingestion numbered list) via a new `doctype_region` helper and per-surface anchor maps, rather than scanning the whole file, closing the latent false-pass vector where a type word in an unrelated table or a prefix in a document-link filename could satisfy the presence check; 3 new regression tests (including the false-pass-vector proof) plus the docstring and §6 narrative. Also closed SR-5 (grc_library-side): the ref-tool cosmetic polish shipped as `grc_library_ref` #31 (dead TEXT_EXTS entry removed, EPUB note widened, MuPDF stdout noise suppressed).

### PR #728: SR-3 `grc_library_ref` binary-scan coverage + TODO 3.20-B1 cross-reference (2026-07-09)

Closed SR-3 (reference-base `validate.py` binary-scan gaps, items 28-29) via `grc_library_ref` #30: check 12 widened to flag CSV extracts whose workbook-family and directory both lack catalogue presence (per-sheet extracts of a catalogued workbook not flagged, 0 false positives on the 50 uncatalogued per-sheet CSVs), and check 13 widened from PDF-only to every tracked binary (PDF+EPUB via PyMuPDF, OOXML via `zipfile`, legacy via a raw latin-1 + utf-16-le scan); 0 findings on the live base, detection fire-tested per format. Also discharged the deferred TODO 3.20-B1 fragment: added the reference-audit SKILL See Also bullet (and a `/reference-audit` command note) cross-referencing the complementary `audit-reference-acquisition-gaps.py` cited-but-not-held tool shipped in #718.

### PR #727: TODO 4.7 GR-P3 / GR-P4 / GR-P5a pack-design batch (2026-07-09)

Closed three GR-P pack-design items: GR-P3 (the third-occurrence-to-gate escalation convention, codified in the pr-retrospective SKILL step 4 + the `/retro` command mirror + an improvement-log `## Convention` bullet), GR-P4 (a `PROVENANCE.md` in each of the three external overlay directories stating the primary-pack-wins precedence + the pruning/refresh stance, plus that stance appended to the project CLAUDE.md overlay paragraph), and GR-P5a (re-pointed the `deep-qa-review` and `library-fitness-review` `derives_from` to `trust-recovery-escalation`, the rule that defines them as its two-skill suite). GR-P5b (exception-register hoist) folded into the GR-P2 condense; GR-P5c validated already-correct (no-op); the GR-P5 derived-skill-coverage-gap residual stays open.

### PR #725: TODO 4.7 GR-P1 session-lifecycle pack rule (2026-07-09)

Closed the GR-P1 pack-design item: shipped the 13th governance rule `session-lifecycle.md`, distilling the project's own session apparatus (durable reconciled handoff, explicit operator-set operating modes, graceful degradation with an absolute reversibility gate, evidence-gated wind-down, the green-merge close with its loop-break, and the advisory concurrency lease) into a project-agnostic discipline any multi-session AI-assisted project inherits. Wired across all rule-enumeration surfaces (README tree + two-areas list + scope table, pack + project CLAUDE.md, the byte-identical `.claude/rules` mirror + MIRROR_MAP, the gate-39 word-form and collection-enum docstring counts); pack `1.58.0`→`1.59.0`. Applied the Fable `session-lifecycle-rule-build` delivery; the project CLAUDE.md sections it distills are retained (project-specific operationalization). GR-P2..P5 stay open.

### PR #724: TODO 3.18 execution-environment probe for `/resume` (2026-07-09)

Closed the environment-detection item: shipped `tools/detect-env.py` (gh presence/auth/rate, hook-firing diagnosis, sibling-repo access with launch-bound `--add-dir`/`settings.local.json` fix lines, per-family egress classes with a HEAD-to-GET fallback; detect-and-adapt only, never a runtime self-grant, always exits 0) and wired it into the `/resume` step-3 verify-state step, with a `.gitignore` line for the machine-local settings override. Applied the Fable `env-detection-build` delivery; at apply the tool's pipe-guard prediction was corrected to an ASSISTANT-PROBE (it had over-generalized from its cloud test, but the NUC harness fires the hook despite `CLAUDE_PROJECT_DIR` being unset), and run on the NUC to capture that profile.

### PR #723: TODO 3.21 AIQT general-framework columns claim-fit-verified (2026-07-09)

Closed the accepted-unverified tracker for the AIQT principle document: ran `/claim-fit` over the 25 general-framework citations (SSDF / CCM / ISO 27001) against the held source texts; 21 fit/inform consistent with the corpus-convention labelling, 2 findings disposed per the maintainer's decision (CCM `LOG-08` "Audit Logs Sanitization" migrated to `LOG-04, LOG-10` in both audit-trail rows; ISO `A.8.34` swapped to `A.5.33` "Protection of records" in both Integrity rows), each re-verified against the held CCM v4.1 / ISO 27001:2022 texts. The pack-wide `LOG-02, LOG-08` convention migration + the apex-rule A.8.34 row fold into GR-P2.

### PR #722: TODO 2.11 publications-screening process + SR-2 screening-record check (2026-07-09)

Closed the publications-assessment / poisoning-detection process (former TODO 2.11) and its paired reference-base gap (SR-2), applying the Fable `publications-screening-build` delivery as a two-repo build. Corpus side (this PR): the `publication-screening` pack skill (twenty-first skill) + `/screen-publications` command + the advisory instruction-content scanner + gate-44 PAIRS + pack `1.58.0` + a project CLAUDE.md cadence section. Reference-base side (`grc_library_ref` #29): the `publications/SCREENING.md` register (29 rows, 16 screened, 13 pending), `validate.py` check 14, and the README protocol section (resolving SR-2's "15 of 27 without records"). The 13 pending EDPB/WP29 rows become the screening wave, TODO 3.24.

### PR #719: TODO 4.6 S-a/S-b/S-e, adopter-experience batch (2026-07-09)

Applied the Fable adopter-experience-sabe batch: a README routing-table link to the decision tree (S-b), a glossary legend for the "Governance Library Maintainer" meta-role (S-e), and a portal Board/CEO audience section plus inline per-entry maturity tags via a `build-portal.py` generator change (S-a). S-c/S-d stay pending their separate worker-20260703-a research deliveries; S-f remains a design item, so §4.6 stays open.

### PR #718: TODO 3.20 bullet 1, not-held-source detection (2026-07-09)

Closed the not-held-source-detection residual: applied the Fable delivery `tools/audit-reference-acquisition-gaps.py`, which diffs the corpus canonical-citations register against the `grc_library_ref` catalogue and worklists cited-but-not-held standards as acquisition candidates (feeding the ref-base acquisition queue); the untractable never-cited-never-held direction stays judge-led per TODO 2.14, and 3.20's publications-inclusion bullet stays open. The reference-audit-skill cross-reference sentence (B1) was deferred to a later pack-touching batch.

### PR #710: TODO 3.15 r6 guardrail G2, worker-brief gate-number rail (2026-07-08)

Codified the r6 guardrail-review gap finding G2 (routed to TODO 3.15 in #707): added DO-rail 14 to `.working/worker-brief-template.md`, requiring every gate NUMBER a delivery cites to be verified against the audit-programme spec §6 (and any asserted corpus-gate interaction by running the gate) before propagating into prose. Targets the gate-42/44 mislabel class that cost the #702/#703/#704 churn. The sibling r6 finding G1 (the per-touch backstop D8 check) stays open in 3.15 for its own PR.

### PR #707: TODO 2.14 `/reference-audit` cadenced skill (2026-07-08)

Closed TODO 2.14 (maintainer-directed 2026-07-07): built the `/reference-audit` cadenced skill and slash command, the reference-BREADTH layer above `/matrix-fit` (control-fit) and `/claim-fit` (claim-precision), which judges whether the corpus draws on the best held authoritative sources for each topic in both directions (held-but-unused and touched-doc-vs-new-ingest). Shipped across two PRs like the sibling cadences: the advisory tool `tools/audit-reference-breadth.py` in #706 (PR A), the skill + command + wiring + the per-touch close-out obligation here (PR B). Three build residuals routed to TODO (not-held-source detection, publications-after-2.11, and the per-touch mechanical backstop as a `[guardrails]` item).

### PR #705: AIQT Principle apex-rule codification (2026-07-08)

Reframed the pack's apex rule as the **AIQT Principle**, (Accuracy = Integrity = Quality = Trust) > Speed > Cost: the four facets named as one co-equal non-negotiable tier, each mapped to its enforcing machinery, superseding the "Quality > Speed > Cost" formulation and the "Integrity check:" chant across every live pack and project surface (substance unchanged; the new checkpoint is "AIQT check: ..."). Added the copy-paste AIQT baseline block to the pack README. Not previously a TODO item (a maintainer-directed 2026-07-08 build from a Fable worker delivery, scratch #110); the corpus principle document is the required follow-up PR 2.

### PR #702: /deep-assessment skill, command, register, and hooks (2026-07-08)

Shipped the rare, maintainer-invoked whole-project deep-assessment instrument: the pack skill plus its paired `/deep-assessment` command (count-free and inventory-deriving, register-backed and re-entrant, sign-off-terminated), wired across the gate-44 PAIRS registry, `/resume` step 7, the pack README (skills tree plus a minor version bump), a project CLAUDE.md section, and the working-records sweep; the two advisory gate-efficacy tools (blind-spot map, mutation probe) shipped in the paired #701. Not previously a TODO item (a maintainer-directed 2026-07-08 build from a Fable worker delivery, scratch #109); also codifies that any future quality-check process or tool is included in the deep assessment by construction.

### PR #697: FR-63 (2.7): adoption worked example (2026-07-08)

Added a narrative adoption worked example ([`docs/worked-example-adoption.md`](../docs/worked-example-adoption.md)) following one fictional adopter (a mid-size SaaS with EU customers and AI features, reused from the startup-roadmap composition example) from clone through the Day-1 six-artefact floor and the staged Phase 1 and Phase 2 programme with file-by-file decisions; wired it to the ingestion worked example and the adopter guide via mutual Related-Documents pointers (no five-path entry-point-list edit, which would have triggered a count cascade). Closes TODO §2.7 / FR-63.

### PR #692: TODO 1.13 (S): SP 800-154 to OWASP Threat Modeling Cheat Sheet (2026-07-07)

Replaced the 2 never-finalized NIST SP 800-154 (data-centric threat modelling) citations with the OWASP Threat Modeling Cheat Sheet, in the threat-modelling standard and the document-index framework-lists (maintainer-chosen substitute; the standard is already STRIDE/MITRE-anchored). Same PR rescoped TODO 1.11 to its small-agent-sub-clause residual, fixed a stale 19/2023, and batched the #691 `/validate-pr` + `/retro` rows.

### PR #687: Sweep 88 iter 1 close-out + TODO 1.12 (annual-review-domain-scope, low): architecture domain (2026-07-07)

Closed TODO 1.12: added `architecture` to the annual-review procedure's §2.1 Scope enumeration (`procedure-grc-programme-management-and-annual-review.md:29`), aligning all three "spans all governance domains" completeness enumerations at 11 domains, and regenerated the taxonomy/portal/scorecard. The `/resume` first PR: ran the loop-break Sweep 88 corpus-wide `/validate` over the #685..#686 deltas (2 out-of-window low-severity findings, both fixed this PR: TODO 1.12 plus a stale illustrative inventory comment in `lint-guardrail-cadence.py`), pruned and reconciled the handoff to daytime-unattended + the scratch->scratch+`grc_library_ref` reference split, and acquired the concurrency lease.

### PR #683: FR-23 (medium): audit-evidence assembler-verification (2026-07-06)

Closed TODO 2.6 (FR-23): added a per-status verification-basis field (independently verified / owner-asserted / auditor-to-verify) and a strengthened assembler statement to the audit-evidence package template, with a supporting section 8.4 in the internal-audit standard, so a package distinguishes verified control status from a management assertion awaiting test. Also carried the batched #682 QA rows and the Note-3 reciprocal-Related-Documents fix on the maturity self-assessment template.

### PR #682: FR-15 (medium): maturity-ladder methodology standard (2026-07-06)

Closed TODO 2.5 (FR-15): added a governance methodology standard documenting the five-tier maturity ladder, the median-of-medians aggregation, its outlier-masking limitation, and a compensating floor-check (absolute Tier-1 plus relative two-tier-gap), with bounded pointers from the performance framework, the adopter template, and the two governance indexes; the generator's document-maturity scoring is unchanged. Also carried the batched #681 QA rows and fixed the #681-surfaced control-testing section 8.1 second-line shorthand.

### PR #681: FR-99 per-control effectiveness metrics (2026-07-06)

Closed TODO 2.4 (FR-99): added a per-control effectiveness metric (an effectiveness band per control from its latest result, recurrence signal, and open corrective-action state, with owner, cadence, threshold, and consuming line of defence) defined in the assurance-metrics register and wired across control-testing, continuous-assurance (section 4.4, named three-lines-of-defence consumption), and metrics-reporting. Applied from the scratch-inbox worker delivery (Option A); the gap was re-verified real at apply-time.

### PR #680: Sweep 86 iter 1 close-out + TODO 3.15 D8 rest-on-convention (2026-07-06)

The `/resume` loop-break corpus-wide `/validate` (Sweep 86 over the #662..#679 deltas); the compensating control PASSED with no in-window regression and no asserted-expectation contradiction. Fixed 3 pre-existing gate-blind ISO-designation findings (spec-master `ISO/IEC 22301`->`ISO 22301`, single-body ISO/TC 292; obligations-template filled example `ISO/IEC 27001:2022 Annex A.8.24`; two orphaned pre-flight-scanner exemptions re-pointed), routed F2 to TODO 1.11 and F4 to TODO 3.1, and closed the TODO 3.15 D8 section-close-orphan candidate on the maintainer's rest-on-convention decision (the event-triggered advisory was census-vetoed, 18 candidates / 0 true positives; rely on the close-out §N-orphan grep). Also pruned the session handoff (keep current + 1 prior) and acquired the concurrency lease for the resumed `claude/resume-chptc7` session.

### PR #677: TODO 1.9 RM-10 pipe-guardrail hardening, closed as a documented harness limitation (2026-07-06)

Closes P1 item 1.9. The `block-verification-pipes.py` PreToolUse hook does not fire in resumed/child sessions; the 2026-07-06 root-cause investigation pinned why (a child session leaves `CLAUDE_PROJECT_DIR` unset, so the `settings.json` hook command resolves to a nonexistent path and the Bash tool proceeds unblocked), and found no portable corpus-side fallback, so the fix is harness-level. The maintainer directed closing 1.9 as a documented harness limitation: parts (a)-(d) shipped 2026-07-03/04, the compensating controls (the RM-10 unpiped-verification habit and the guard's `PRE_PUSH_GUARD_ALLOW_PIPE`-gated pipe self-defence) fully cover the underlying risk, and the limitation is recorded in `.working/third-party-issues.md` so a future session does not mistake it for a regression.

### PR #675: TODO 3.15 #637 F3, the D5 eighth closure-form and form-6 markdown-link widening (2026-07-06)

Closes the #637-verifier F3 bullet. Widened `tools/check-todo-rotation-on-pr.py` (delta gate D5) with an eighth closure form (the bare `TODO N.M ... closed` phrasing, no `section` word and no `§`, the #637 lead shape) and a link-tolerant widening of the rotation-assertion form 6 (a markdown-linked DONE target, the #640 shape), both census-validated FP-clean, with fixtures. Co-updated all surfaces in the same PR: the linter docstring and module comment, the protected `.claude/CLAUDE.md` closure-form count (SEVEN to EIGHT), and the `governance/specification-audit-programme.md` §6 D5 narrative. The bullet's diff-side-companion design proposal is subsumed by the still-open D8-candidate bullet. Second protected-backlog PR of the 2026-07-06 daytime session; TODO 3.15 stays open on its GR-8/GR-10/GR-GAP tooling bullets.

### PR #674: /claim-fit cadence section, completing the TODO 3.15 r5 CLAUDE.md close-out-clause bundle (2026-07-06)

Closes the r5 close-out-clause bundle (its first three clauses shipped in #652 and #659). Added a `## Normative-attribution claim-precision cadence (/claim-fit)` section to `.claude/CLAUDE.md`, sibling to the `/matrix-fit` section, documenting the cadence for the `/claim-fit` citation-precision audit (the gate-blind "attributed value, silent source" FR-120 class): the one-time Tier-A adoption pass (#630), the per-batch cadence, and ad-hoc use. TODO 3.15 stays open on its remaining bullets (the #637 F3 D5 eighth-form and the GR-8/GR-10/GR-GAP tooling items). First protected-backlog PR of the 2026-07-06 daytime session.

### PR #671: QA-report intake runbook subsection (TODO 3.15 r4 G-7) (2026-07-06)

Closes the TODO 3.15 r4 G-7 bullet. Codified the three-layer QA-report intake channel (a worker findings report is a hypothesis-set → an independent validation subagent re-reads each cited source → a transcription-fidelity verifier confirms the report-to-record transcription) as `.working/multi-session-orchestration.md` §5.2, with the maintainer's standing revisit note to assess the full-skill option on the channel's next recurrence. The channel had lived only in the #626 records.

### PR #670: Acronym-linter digit-initial blind spot (TODO 3.15 #637 F4/F6) (2026-07-06)

Closes the TODO 3.15 #637-verifier F4/F6 bullet (gate 20, `lint-acronym-consistency.py`). Widened `GLOSSARY_ROW_RE` and `INLINE_DEF_RE` to `[A-Z0-9]`-initial so digit-initial numeronym rows (`3PL`, and future `2FA`-class) are parsed and matched rather than silently skipped, with three regression fixtures; gate 20 stays green on the live corpus. The paired "assess a lowercase-tolerant inline pattern" half was assessed against the full corpus and REJECTED with evidence (a lowercase-starting run over-captures incidental leading context, so it would false-positive on many consistent definitions or, flagging only zero-overlap, on incidental parentheticals; an initialism anchor fails for numeronyms/stopword-dropping acronyms), so the Title-Case-expansion requirement is documented as a deliberate false-positive control rather than widened. Surfaced to the maintainer for confirmation.

### PR #668: PCI DSS v4 to v4.0.1 normalization (TODO 3.21(d) follow-through) (2026-07-06)

Not a new TODO item: completes TODO 3.21(d), which #667 had left unchanged. The maintainer clarified the same night that the standing preference is the full latest version `PCI DSS v4.0.1` (family label `v4` only when quoting another document), so the three cloud-hardening baseline framework-alignment cells (AWS/Azure/GCP) were normalized from bare `PCI DSS v4` to `PCI DSS v4.0.1`; the citation-form template's discouraged-example `PCI DSS v4` was left as an illustration. The preference is recorded in design-decisions.md as a durable convention.

### PR #667: TODO 3.21 citation and naming hygiene residuals CLOSED (2026-07-06)

Closes TODO section 3.21, its four decision-parked residuals resolved on the maintainer's calls: (a) the compliance-matrix framework-key cell reading "C-TPAT Minimum Security Criteria" (a legacy document-title quote) normalized to bare `C-TPAT`; (b) FQ-F1, the five identical `tools/` PR-delta error strings reworded from bare "ensure" to the house-style `ensure that`; (c) FQ-B1, the master spec's line-214 monotonicity claim replaced with the verifier's round-3 wording (gate 13 non-decrease, the CHANGELOG-coupling gates 29/59 catching a forgotten bump), gate identities re-verified against the linter docstrings before shipping; (d) the three `PCI DSS v4` cloud-baseline family-label citations left as-is (maintainer chose leave over normalizing to `v4.0.1`, no code change).

### PR #664: Matrix ISO-header gate-49-coupled lockstep (ISO/IEC designation) (2026-07-05)

Harmonized the compliance matrix's 11 per-domain ISO column headers plus the legend to `ISO/IEC 27001:2022` in lockstep with gate 49's `ISO_HEADER` constant, its regression fixtures, docstring, and OK message, the shared `iso_27001_reference.py` finding messages, gate 58's own diagnostic messages (the ISO-gate pair fully harmonized, gate 58's deliberate both-form-input documentation kept bare), the `/matrix-fit` worklist-tool docstring, and the gate-49 references in the audit-programme spec. Gated on proving gate 49 still fires post-rename (injected `A.5.99` caught under the new header; old bare header no longer recognized), verified by two independent adversarial verifiers. Closes TODO 3.1 part (a) (the last of the four 2026-07-05 daytime-round pending items after Brazil/#662 and FIT-8/#663); the base-unverified gap tail (part b, task tracked) and the authoritative-register+gate item remain open.

### PR #663: ISO/IEC designation-accuracy corpus-wide sweep (base-verified subset) (2026-07-05)

Executed the maintainer's accuracy-principle redirect (joint ISO/IEC standards must be listed as joint; single-body standards list only the one; accuracy is critical to integrity): a corpus-wide migration of the 13 base-confirmed joint standards from bare `ISO NNNNN` to `ISO/IEC NNNNN` (232 conversions across 31 files) via the high-assurance harness (two adversarial verifiers, deterministic scripted apply, re-parse). Subsumes the FIT-8 register-cell pending-decisions item (register cells now uniformly `/IEC`; row 274 internally consistent). Base-unverified joint-standard gaps (23247, 27033/27034, 12207-tripartite, etc.) left bare and tracked in TODO 3.1's new gap bullet; the gate-49-coupled compliance-matrix header harmonization remains its own pending lockstep PR.

### PR #659: TODO 3.15 r5 close-out-checklist clauses (D7-naming + summary/description-lag) (2026-07-05)

Added two grouped `.claude/CLAUDE.md` close-out-checklist clauses: (1) the reconcile bullet now names the D7 handoff-snapshot freshness check as the mechanical backstop for the version-token half of the Current-truth reconcile (the gate-50 naming pattern); (2) a new summary/description-lag bullet (when a PR resolves or lands a summary surface, or a reword changes a primary surface, update the paired detail surface in the same commit). TODO 3.15 stays open; the `/claim-fit` cadence clause is the last remaining CLAUDE.md close-out item (#660).

### PR #658: design-decisions ledger light-restructure (2026-07-05)

Added an Index (a thematic-section list plus a reverse-chronological list of the 16 standalone dated decision sections) to the design-decisions ledger and corrected its stale "append to the relevant section" ordering note to match the file's actual two-register structure. Not previously a TODO line; surfaced from the 2026-07-05 maintainer request to tidy the ledger, done as a small item.

### PR #657: 3.15 D-F3, evidence-grounded-completion corollaries, project-CLAUDE.md remnant (2026-07-05)

Closed TODO 3.15 D-F3 fully: the project `.claude/CLAUDE.md` evidence-grounded-completion index bullet gained the condensed clause naming the rule's un-observable-state, inventory, and external-version-currency corollaries, matching the three pack surfaces shipped in #656 (the pack half), so all four enumeration surfaces now name the corollaries. 3.15 stays open on its remaining sub-items (the r5 close-out clauses defer to #658).

### PR #655: 3.15 D-F2, guardrail-review SKILL cadence clause (2026-07-05)

Closed the r4 D-F2 sub-item of TODO 3.15: the guardrail-review SKILL's auto-prompt bullet implied unbounded maintainer deferral and never named gate 60, so one clause was added noting the deferral is bounded by gate 60 (guardrail-review cadence currency), which warns while the summed machinery-inventory drift is 1 or 2 and fails the build once it reaches 3 (threshold verified against `tools/lint-guardrail-cadence.py`). 3.15 stays open on its remaining sub-items.

### PR #654: 3.18, pack-tree MITRE ATLAS technique-ID currency refresh (2026-07-05)

Closed the pack half of TODO 3.18 (the corpus half shipped in #635): the eight `AML.T0048` citations across the four `dev-security/claude-rules/ai/` files (all LLM06 excessive-agency tool/permission rows) re-point from External Harms to `AML.T0053` (AI Agent Tool Invocation), mirroring the corpus half's verified resolution, and two gloss drifts on otherwise-correct IDs are corrected in `ai-security.md` (`AML.T0024` to "Exfiltration via AI Inference API", `AML.T0051` to "LLM Prompt Injection"), all grounded in the ATLAS 2026.06 CSVs with v2026.06 upstream-confirmed current at apply time; T0010, T0020, and T0054 were re-verified current and unchanged.

### PR #651: 3.25, decision-tree residual acronym glossary coverage (2026-07-05)

Added six glossary rows (AI, BC, CM, CPRA, ML, PIA) for acronyms the #637 verifier flagged as unexpanded and unresolved in the decision tree; CCPA and DR (the CCPA/CPRA and BC/DR compound neighbours) already had rows. The decision tree defers acronym resolution to the glossary so no decision-tree edit was needed; the bare-AI applier's call chose add-the-row over strike-as-household.

### PR #649: 3.22, PCI DSS v4.0.1 currency migration + linter v-prefix widening (2026-07-05)

Closed across two PRs (maintainer decision B1): #648 migrated the 12 `PCI DSS v4.0` citations to `v4.0.1` across 8 files and moved the citation-form template's taught form; #649 widened `tools/lint-standards-currency.py`'s separator regex to catch a `v`-prefixed superseded label (regression fixture added, preserving the continuation guard that protects the current `v4.0.1`). The three bare `PCI DSS v4` family-label residual moved to 3.21(d).

### PR #647: 3.24, AI access-permissions ISO mapping reconciliation (2026-07-05)

Judged via ad-hoc `/matrix-fit` against the ISO/IEC 27002:2022 control titles: the compliance matrix mapped the AI Access and Agent Permissions Standard to A.8.3 (Information access restriction) while dropping A.5.17, but the document's agent-permissions and privileged-access scope fits A.8.2 (Privileged access rights) plus A.5.17 (Authentication information), so the matrix row was corrected to A.5.15, A.5.16, A.5.17, A.5.18, A.8.2 to match the document's own authoritative table, and the document-index ISO summary was aligned to include A.8.2.

### PR #646: 3.23, patch-vs-vulnerability SLA reconciliation (2026-07-05)

Split patch-management's Standard Critical classification into PoC-available (72h) and no-known-exploitation (7 days) rows to mirror the vulnerability-management source table (maintainer decision B2), resolving the two-answers-from-two-citable-procedures conflict; the section-7.4 metric was generalized from "within 72 hours" to "within classification SLA" so the document stays coherent.

### PR #643: 3.15 r4 G-4, cross-file shared-constant hoist (2026-07-04)

The five reference-extraction constants gates 62 and 65 duplicated copy-with-comment (REF_PATTERNS, MD_LINK_RE, BINDING_SENTINEL, EXTERNAL_CONTEXT_RE, ADJACENCY_WINDOW) hoisted into lint_common's CROSS_* block as the single source of truth; both linters import them aliased, so a sentinel or window change can no longer drift between the phases. Also carries the #642 QA batch and its section-5 in-window fix.

### PR #642: 3.15 r4 G-3, gate-64 delta-check extension (2026-07-04)

Gate 64 extended with the delta-check half: the section-6.1 D-row table now requires a "Delta gate Dn ..." narrative per row and must match the parity linter's WORKFLOW_DELTA_GATE_STEPS registry exactly in both directions (informational entries exempt), so a stale registry entry for a removed delta check fails loud. Four new fixtures (suite 341).

### PR #641: 3.15 GR-4, gate 66 unbalanced-fence audit (2026-07-04)

The GR-4 standalone-check half built as gate 66: no scanned markdown file may end inside an open fenced code block (an odd fence count silently suppresses every fence-aware linter's scan of the remainder). Four-surface wiring, section-6 prose pair, section-5 category clause, three fixtures (suite 337); the build-time census found zero unbalanced fences, so the gate is preventive.

### PR #640: 3.15 GR-DRIFT-1, gate-54 four-surface rename (2026-07-04)

Gate 54 renamed to "Per-document NIST CSF 2.0 control-code validity audit" across the four parity surfaces plus the section-6 narrative opener and section-5 grouped-list phrase, matching its docstring's actual NIST-CSF-2.0-only scope (the sibling gate-58 naming pattern). Name approved at the morning round; not previously an FR-keyed item.

### PR #639: TODO 3.21 build-only half, citation and naming hygiene (2026-07-04)

Three validated fixes shipped: ERC expanded at first use in the vulnerability-management procedure; the non-matrix legacy C-TPAT occurrence normalized to CTPAT; the fresh-reader skill's reciprocal See-Also link to the fitness skill (pack 1.54.1). The fourth, FQ-B1, descoped at the verifier-loop cap (maintainer decision); 3.21 rescoped in place to its three decision-parked residuals.

### PR #638: TODO 3.20 startup-roadmap module-count fix (2026-07-04)

The two live 23-module carriers corrected to the roadmap's actual 24 module subheadings (E0 added after the count was authored): the hardcoded string in the portal generator (with regen) and the quickstart line. The frozen historical CHANGELOG carrier left per the no-retroactive-edits convention.

### PR #637: TODO 3.19 decision-tree hygiene bundle (2026-07-04)

Three validated fresh-reader defects closed: maintainer-internal PR/FR provenance parentheticals stripped from the decision tree's adopter-facing prose; FMI and 3PL expanded at first use with new glossary rows (a 0-9 section added for 3PL); a size-band note reconciling the tree's under-50 Small band with the adopter guide's under-200 Tier 1 cue.

### PR #636: TODO 3.18 corpus half, ATLAS technique-ID currency fix (2026-07-04)

The AI/agentic standard's three stale ATLAS framework-alignment rows re-mapped against the ATLAS 2026.06 CSVs (upstream-confirmed current at apply time): supply chain to AML.T0010, tool misuse to AML.T0053, resource exhaustion/DoS to AML.T0029 + AML.T0034. The apply's close-out grep surfaced the same class in the pack tree; 3.18 rescoped in place to that pack half.

### PR #635: TODO 1.9(d) RM-10 self-test wiring + the no-long-check-ins codification (2026-07-04)

Both RM-10 enforcers' self-tests (the PreToolUse pipe-blocking hook, the tail-safe wrapper) wired into the regression suite so a broken enforcer fails loud (the worker QA run's GR-GAP-3); section 1.9 now stays open only on the next-session hook-firing validation. Also codifies the maintainer's 2026-07-04 no-long-interval-check-ins directive in the CLAUDE.md background-task SOP.

### PR #634: delta gate D7, handoff-snapshot freshness check (2026-07-04)

The maintainer-accepted mechanization of the append-not-reconcile class (seven logged occurrences): a PR-time delta check validating the handoff Current-truth line's labelled version tokens against the PR head's live headers, duplicate tokens failing too. The section-3.15 snapshot-check bullet closes; not previously an FR-keyed item.

### PR #633: TODO 1.10 Quebec Law 25 72-hour confabulation sweep (2026-07-04)

Corrected the confabulated 72-hour CAI breach clock to the statute's promptness standard on the seven remaining corpus carriers across five documents (the two Canada-annex carriers were fixed in #631, which surfaced the class); companions: the breach-response ANPD rename and the FR-141 frozen-history disposition. Item added and closed same-day from the #631 verifier catch.

### S3 PR B: section 1.4 CLOSED, the /claim-fit skill + Tier-A adoption pass (2026-07-04)

The S3 citation-precision instrument's second half: the `claim-fit` pack skill (eighteenth skill, slash command `/claim-fit`, pack 1.54.0) plus the one-time full Tier-A judging pass over all 11 census rows. The pass fixed five documents' attribution phrasing in-window (the 7-year AI-log retention carriers and the 24-hour supplier-notification carriers, values kept as the organization's canonical/contractual choices per the FR-120 precedent) and queued three source-drop requests (DORA Art 20 RTS, UK GDPR, PIPL). Closes the former TODO section 1.4 (S1/S2/S4 had shipped earlier); carries the #629 QA batch, both routed #629 finding fixes, and the maintainer-accepted snapshot-check TODO item.

### PR #629: section-1.9 (c) closed + D-F4+F6 closed + GR-3 CLOSED (2026-07-04)

The maintainer-authorized CLAUDE.md touch bundle: the RM-10 clause widened from the guard to every verification command (naming the tail-safe wrapper and the hook, whose named-command and sink sets also widened with proof-case self-tests), the seven staged 1.9(c) clauses landed on the close-out checklist (#614, #619 widened to the snapshot line, #593, #594, #612, #625, #620), and the D-F4+F6 operating-mode rewords plus the #627 F2 delivery-time seed-removal reword applied. GR-3 wave 3 closed as the maintainer's keep-as-is decision (design record); the 2026-07-04 morning decision rounds (thirteen answers) executed into TODO and the ledgers; S-f (fork update-assessment tooling) added at maintainer request. Carries the #628 QA batch and both its finding fixes.

### PR #628: GR-8 CLOSED: retro proposed-improvement closure discipline (2026-07-04)

GR-8's remaining half (b) shipped as the register disposition-token convention plus `/retro` step 6 (disposition scan + carried-candidates check, which also closes the r3 G-F4 note bullet): the #627/#621/#624(b) candidates codified (record-vs-diff clauses in the three QA-record steps, the verifier-loop class-width clause, the runbook close-out ordering line), the #593/#594/#612/#620/#625 candidates routed to the TODO 1.9(c) authorized-touch bundle, and eight register rows dispositioned. The expiry tail (#233, #235, habit-band rows), the option-B ageing tool, and the vocabulary confirm-or-redirect sit with the maintainer in pending-decisions. Seventh resolution of the 2026-07-04 overnight run, closed out at the morning boundary; the PR also routes and resets the overnight file and closes the r4 D-F5 bullet both ways (the stub pruned to the single latest closure note AND the change-tracking rule's stub form admitting that note).

### PR #627: names-phase gate 65 + /guardrails r4 run (2026-07-04)

Two section-3.15 closures in one PR: the cross-file section-name audit shipped as gate 65 (title-anchoring rule from the same-day corpus survey; table rows deliberately scanned; the r4 O-1 seam closed at build time; suite 326) and the /guardrails r4 review ran at its gate-60 threshold (19 findings: 10 fixed in-window with two partial, 8 routed as seven bullets, 1 cadence note; inventory re-baselined at 65 gates). Fifth and sixth resolutions of the 2026-07-04 overnight run.


### PR #625: GR-6: gate 64, audit-spec detailed-prose presence audit; SR-5 closed by refutation (2026-07-04)

Two items closed: the GR-6 section-3.15 bullet shipped as gate 64 (`lint-audit-spec-detailed-prose.py`, floors 35/47, with the gates 43/44 description backfill and the four-surface wiring), and SR-5 closed by refutation (the maintainer-supplied fresh EN 304 223 V2.1.1 copy confirmed the item's designation was correct). Third and fourth resolutions of the 2026-07-04 overnight run.


### PR #624: r3 O-F1: gate-18 trailing-link cross-doc seam closed (2026-07-04)

One section-3.15 bullet closed: `lint-intra-doc-refs.py`'s cross-doc filter extended with a trailing 60-char window (mirroring gate 62's bidirectional link adjacency) plus a regression fixture, so a `see section 5.4 in [foo](foo.md)` line is claimed by the cross-doc side on both gates. Second build-only pick of the 2026-07-04 overnight run; also adds the four wave-6 ad-hoc-brief TODO items and the P6 research-state notes.

### PR #623: D6 pack-README version-history co-bump delta check (2026-07-04)

One section-3.15 bullet closed: the D-check candidate shipped as delta gate D6 (`check-pack-readme-cobump-on-pr.py` + runner/workflow/parity/spec wiring + four fixtures), mechanizing the paired-surface checklist instance (a). First build-only pick of the 2026-07-04 overnight run.

### PR #614: GR-9 + S-4 + GR-11 + r3 O-F2: guardrail hygiene batch (2026-07-03)

Four section-3.15 bullets closed in one batch: the scratch-bucket misdescription corrected on every live carrier (GR-9, which also surfaced that `verify-reference-modules.py` was functionally broken by the re-bucketing; repaired and re-anchored to the `ref/` root), the aid extended with COBIT/ISO 31000 parity coverage (S-4), the preflight two-parser seam documented as deliberate gate-parity mirroring (GR-11), and the gate-9/gate-12 shared-token boundary documented in both docstrings (r3 O-F2). Both #613 sweep findings fixed in-window.

### PR #612: section 3.6: multi-session codification complete, worker-provenance attestation activated in gate 50 (2026-07-03)

The last section-3.6 deliverable (the worker-provenance audit gate): gate 50's dormant check 3 activated, validating the new `**Worker provenance:**` marking convention (a detailed-mirror CHANGELOG line naming the scratch `inbox/<worker-id>/` delivery path) now that both preconditions exist (the marking convention this PR defines; the external-collaborator primitive via the scratch WORKER-ONBOARDING flow). Runbook, CLAUDE.md checklist, spec narrative, and five fixtures shipped with it; both #611 sweep findings fixed in-window. Second injected concurrency priority: with #611, the second-session prerequisites are complete.

### PR #611: section 3.7: session-concurrency lease + git cross-check, shipped with gate 63 (2026-07-03)

The maintainer-requested concurrent-session interlock (design captured 2026-06-26, all three sub-decisions locked 2026-07-02: 60-minute staleness window, advisory HOLD, well-formedness gate in the same PR): the `.working/session-state.md` lease with the acquire/refresh/release lifecycle, `/resume` step 0 (lease read + git cross-check of unmerged sibling branches, HOLD-and-surface on a live signal), CLAUDE.md close-out wiring, and the shape-guarding gate 63 four-surface-wired with nine fixtures. First of the two maintainer-injected concurrency priorities; section 3.6 (worker-provenance gate) is next.

### PR #609: section 1.6: D5 seventh closure form + CLAUDE.md D5/RM-10 codifications (2026-07-03)

The D5 PR-time check gains the space-separated `TODO section N.M ... closed` form (census: four full-history hits, all genuine, zero false positives) with fixtures and the audit-spec narrative; the CLAUDE.md step-7 description refreshed to the seven-form set and the RM-10 unpiped-guard sentence added to step 2, closing the last open removal-ledger entry as dispositioned-codified. Section 1.6 closed the same day it was intaken.

### PR #608: morning processing: overnight run routed, sections 3.8, 3.10, and former-7.1 closed at the 2026-07-03 decision rounds (2026-07-03)

The 18-merge overnight run's file routed and reset to stub; the #607 QA trio recorded (zero-finding sweep); the maintainer's morning rounds confirmed the four DPO defaults and closed three backlog items by decision: section 3.8 (orchestrator tokens stay honestly not-instrumented, permanent), section 3.10 (the audit-trail-only TODO sections KEEP by design, its accretion-guard half already shipped), and the former Priority-7 item 7.1 (the same keep decision). The seven queue-de-blocking directives are recorded in pending-decisions.

### PR #607: FR-48 (section 1.1): H2 numbering-pattern entangled residual, series complete (2026-07-03)

The final entangled document (information-security policy, 33 clauses plus the carried 27002 cell fix) renumbered in #607, completing the 38-document FR-48 deferred worklist: the first 25 deferred docs through #548, the internal-audit standard confirmed canonical in #594, and the 12 entangled docs one per PR in #596 through #607 under the full HA harness (the separate 28-doc safe subset was normalized in #520). Section 1.1 closed and rotated.

### PR #595: 3.15 machinery wave 2a: D5 closure-form widening, gate-60 scoped parse, gate-39 vanished-file tolerance (2026-07-03)

Three routed section-3.15 tooling bullets closed in one mechanical batch: D5's form 3 gains the bullet(s) noun and a decimal-dot-tolerant clause run (census: three new hits, all true positives) with form 6's short guarded rotation assertion, gate 60 counts only section-6 inventory rows, and gate 39 skips files that vanish mid-scan. The GR-6 census results are recorded on its TODO bullet with the gate-60 sequencing prerequisite.

### PR #593: MEA02 title-and-fit pass: two title fixes + four MEA04 recodes; section 3.14 closed (2026-07-03)

The routed MEA02 finding judged per carrier: the CAPA procedure and document-review template keep MEA02 with the canonical title, the audit-planning procedure, internal-audit standard, assurance-map register (with its doc-index companion), and AI-audit procedure recode to MEA04 Managed Assurance; the low-severity cleanup batch (section 3.14) fully closed and rotated.

### PR #592: ad-hoc /matrix-fit pass: three recodes + two rewords; sec-IR authority residuals closed (2026-07-03)

The routed fit candidates judged: due-diligence BAI05 to APO10 Managed Vendors, the compliance-governance row to EDM01, the audit-planning row to MEA04 Managed Assurance, the digital-trust gloss and retirement pointer reworded; the #591 sweep's sharing-list and Incident-Commander carve-out fixes; a five-carrier MEA02 mis-title finding routed. Closes the section-3.14 fit-pass and retirement-recording bullets.

### PR #591: coverage-gaps third batch: eight re-grades + the Brazil OEA row (2026-07-03)

The routed #586-sweep residue executed: Mexico NEEC and the five candidates-list programmes to Referenced, China generative-AI and the PQC migration playbook to Partial, the Brazil OEA row added with mutual-recognition evidence, every grade leaning on a named batch-2 precedent; plus the sec-IR authority-residual fix and the #590 QA trio.

### PR #590: section-1.3 DPO role-separation sweep + section-2.13 PIA acceptance authority (2026-07-03)

The maintainer-directed sweep separated the CIO/DPO composite across all ten carrier documents plus four verifier-caught siblings (81 edits: role tables, sign-off chains, notification authorities, Owner fields per the document index), reframed the charter's interim block as adopter guidance, and applied the answered PIA authority (DPO advises, Executive Committee accepts) with the two GRC-programme siblings aligned to the canonical chain. Sections 1.3 and 2.13 closed.

### PR #589: small fixes: retention approval re-target + lifecycle pointer + GR-8(a) RM disposition pass (2026-07-03)

The retention standard's 7-year approval gate re-targeted to ad-hoc extensions beyond the schedule (the answered section-2.13 note), the quality-cadence Supersede pointer re-pointed at the charter, and all 15 removal-ledger entries dispositioned (12 reviewed-keep-out, RM-6 and RM-8 inspired-change, RM-10 held open on a morning item).

### PR #588: COBIT fit-pass recodes + ISO 31000 6.6 swap + MEA01 titles (2026-07-02)

The seven maintainer-pre-authorized COBIT semantic-fit recodes applied (cross-framework matrix rows to EDM03/EDM03.01/APO12.02 with the ISO appetite cell to 6.3.4, the exception policy's three APO12.03 carriers to APO12.02, the four BAI05.02 supplier carriers to APO10.05), plus the #587 verifier's ISO 31000 6.7-to-6.6 correction on three carriers, four MEA01 practice-title restores, and the nine-carrier MEA01 objective-title canonicalization.

### PR #587: gate 61 shipped, COBIT + ISO 31000 citation existence, both halves of the section-3.13 build (2026-07-02)

The section-3.13 citation-coverage item closed per the maintainer's both-in-one-PR answer: a new reference module derived deterministically from the source specifications (40 objectives, 231 practices, the ISO 31000:2018 clause tree), the gate wired four-surface with eight fixtures, the /matrix-fit worklist tool extended to COBIT and ISO 31000, and the gate's three day-one catches fixed (two fabricated practice codes, one wrong designation). The seven fit-pass recode verdicts routed to their own PR.

### PR #586: coverage-gaps second batch re-graded; Partial definition widened (2026-07-02)

The routed section-3.14 second coverage-gaps batch (#581 sweep M-1 plus I-1) closed per the maintainer's return-round answer: sixteen rows re-graded with corpus evidence verified at file (UK PRA/FCA, OSFI, NHS DSPT, UK AI, and Manufacturing to Partial; eleven regulator, AI, trade, and framework rows to Referenced), and the vocabulary's Partial definition widened to cover dedicated-adjacent-artefact cases.

### PR #585: lifecycle vocabulary aligned to Superseded across the four carriers (2026-07-02)

The routed section-3.14 lifecycle-vocabulary fork (#579 sweep L-2) closed per the maintainer's return-round answer: the charter's stage 5, the health-report template's count row, the adopter-guide's index advice, and the build-taxonomy docstring now say "Superseded" (anchored to the Status: Superseded marker), with "Retired" kept as the distinct removal stage.

### PR #582: GR-P3 tension-marker check shipped as an advisory aid (2026-07-02)

The partial-rewrite tension-marker item (GR-P3 graduation, the #565 retro) shipped as the diff-scoped advisory aid `tools/tension-scan.py` rather than a standing gate: a build-time census over the live TODO and ledger surfaces found 91 status+hedge pair coincidences, essentially all legitimate, so the bookkeeping-gate family's zero-false-positive bar is unreachable and the contradiction judgment stays human (the aid flags rewritten blocks carrying a status+hedge pair for an end-to-end read; the aid-not-gate shape is a logged proceeded default).

### PR #581: coverage-gaps register re-graded with evidence (2026-07-02)

Eleven stale Coverage cells re-graded against verified corpus artefacts per the maintainer's re-grade-with-evidence answer: the AWS/Azure/GCP overlay rows, Kubernetes, Serverless/FaaS, ITIL 4, and the quickstart, roadmap-template, and interactive-assessment capability rows to Partial, and SWIFT CSP and ISO 14001 to Referenced, each Notes cell carrying the re-grade provenance and the remaining gap; this closes the section-3.14 coverage-gaps triage bullet. (Entry corrected in #582: the original said seven cells and graded Kubernetes Referenced, contradicting the shipped register's eleven re-grade notes and Kubernetes's Partial grade, the #581 verifier's raise not reflected back into this ledger at ship time.)

### PR #580: the two flat AI retention rows composed with the domain minimum (2026-07-02)

The AI-incident-records and AI-decision-and-detection-logs register rows gain the whichever-is-longer composition with the AI-Systems domain minimum (the maintainer's compose-both answer), matching the adjacent composed rows' shape; the two citing AI standards' 7-year floor statements stay true, and the pending-decisions sibling-triage note is closed. Not previously a TODO item; surfaced by the #574 sweep's sibling catch and decided in the 2026-07-02 round.

### PR #579: L-j, the Classification overload migrated to a lifecycle marker (2026-07-02)

The superseded privacy annex now carries Status: Superseded as the lifecycle marker with Classification restored to Public; the three linters that keyed their redirect-notice exemption on the Classification overload (stub, required-sections, section-placement) are re-keyed on the Status marker with fixtures pinning both the new exemption and that the old overload no longer exempts.

### PR #578: L-k, pre-commit regen-before-check reorder (2026-07-02)

The pre-commit-only regenerate-derived-artefacts hook moved after the taxonomy and portal --check hooks, so local drift now fails loud at the checks instead of being silently regenerated into a false green (CI was never affected, check-only there); moving the regen hook rather than the check hooks keeps the gate order identical across the four parity surfaces.

### PR #577: GR-5, guardrail-review cadence mechanized as gate 60 + the r2 record backfilled (2026-07-02)

The prose-only auto-prompt cadence now has a mechanical backstop: gate 60 compares the live machinery inventory (gates/rules/skills/commands) against the newest guardrail-review history row's as-of token, warning on drift and failing at the threshold; the 2026-07-02 five-lens review's missing history row and per-run record were backfilled from the intake artefacts (the gap the finding itself named).

### PR #576: 3.13 gates-widening: gate 55 to eight retention pairs, D5 to six closure forms, gate 50 dual-spelling marker (2026-07-02)

The audit-surfaced widening bullet closed in one PR: gate 55 now locks the five reconciled retention rows (breach, PIA, AI-IA, AI-audit, supplier-audit) beside the original three, with the AI-audit anchor sentence reworded, the supplier-audit retention sentence authored, and both register matches notes added; D5 gains the section-name, item-number, and rotation-assertion closure forms (the #567 vacuous pass closed; the generalized form rejected on census FPs); gate 50 accepts the -ized marker spelling. Fixtures grew with all three.

### PR #575: GR-12: the post-fix residual-scan aid shipped (2026-07-02)

The deterministic residual-scan step is now tooling: given a corrected token, the aid scans every text surface in the working tree (not an enumerated input set), prints every hit as an untruncated full line labelled LIVE / LEDGER / FROZEN-RECORD, and exits non-zero on live residuals so it chains as a completion check; escalated ahead of the tension-marker gate on the four-in-two-PRs fix-named-miss-sibling recurrence.

### PR #574: 3.14 batch B: the judgment-tier cleanup set (2026-07-02)

Five more 3.14 items closed: the decision-tree 30/90/180 phasing annotated as deliberately distinct from the roadmap's 90/180/365 calendar; the privacy charter's hardcoded four-region scope genericized to the applicability register plus an adopter bracket; five sector leaks genericized in the risk-appetite template (the four enumerated plus the Technology-row carrier the research found); the incident-records retention row raised stricter-safe to the 7-year evidence floor with its logging-standard echo; and the AI-audit retention row composed with the domain minimum (both value choices logged in pending-decisions for confirm-or-redirect).

### PR #573: 3.14 batch A: the mechanical low-severity cleanup set (2026-07-02)

Eight of the 3.14 items closed in one mechanical batch: 39 Commonwealth prose flips across 19 tools files (identifiers and word-reference carriers deliberately kept), the TLS 1.3-canonical caveat on the pack's two ASVS TLS 1.2 lines (pack 1.53.12), gate 55 spliced into the audit-spec section-5 category-3 list plus its stale example (1.16.34), the protected CLAUDE.md D1-D5 and coded-id closure-form lines (item 24 closed), the pending-decisions stale summary, the FR-48 residual reframed to the true 13-of-38, the Japan APPI transliteration, and the COBIT APO12 "Managed Risk" trio plus the APO10 "Managed Vendors" cells confirmed against COBIT; plus the six #572 sweep dispositions and the L-j load-bearing-Classification finding routed back to TODO as a design decision.

### PR #572: 2.13 item 11: GDPR DSR clock corrected to the statutory one month (2026-07-02)

The DSR rights catalogue, workflow-template SLA, and privacy-policy timeframe corrected from "30 days" to the GDPR Article 12(3) one-month clock with the two-further-months extension and first-month notice, the PIPEDA 30-day clock kept where PIPEDA is the cited instrument, and the CCPA/CPRA 45-day window (extendable once by 45) added beside the rights table; every value quote-verified against the GDPR, CCPA, and PIPEDA full texts.

### PR #571: Overnight cleanup: ledger routing + 7.5 keep-tracked decision + mode-exit priority codification + the nine #570 sweep dispositions (2026-07-02)

The 18-PR overnight run's morning processing: the overnight ledger routed and reset to stub, the reference-file keep-tracked decision recorded (7.5 rotated here; the untrack-and-purge direction superseded before execution), the mode-exit priority ordering and the model-tiering direction recorded, and all nine #570 sweep findings dispositioned (the "practised" irregular-flip residual plus its editorial-carve-out documentation, the HA register restructure, the four-ledger count corrections, the test-comment and linter-docstring fixes, the README AEO reflow).

### PR #570: TODO 7.4 (decision executed) + 3.13 item-25: full Commonwealth-spelling harmonization + gate-2 coverage extension (2026-07-02)

The maintainer-locked full-normalization decision executed: ~2000 "-isation"/"-ise"/"-yse" occurrences flipped to the Canadian forms across ~330 files under the high-assurance harness (classified research map, deterministic masked apply, verbatim-quote carve-outs for the GDPR Article 25(1) quote, the OECD name, and the WP216 title), with the pseudonymization standard renamed and gate 2 extended (40 new verb stems, a generic -isation noun check, the -yse family, the allow-span mask). Also batches the #569 QA rows.

### PR #569: L-d (M): verbless "ensure that" sentences repaired corpus-wide (2026-07-02)

All 54 verbless "ensure(s) that + noun" carriers across 36 documents repaired by a deterministic scripted apply, the full-corpus 170-occurrence read having raised the enumerated 22 to the true 54 (each repair supplies the missing verb; none deletes "that"), with the in-repo mechanical-sweep root-cause hypothesis refuted: every traced carrier was introduced at the initial public-release commit. Also dispositions the eleven #568 sweep findings (decision-tree tokens and OT answer, linter rationale, portal schema-constant bump, seven more register cell rewordings, the stale DONE count).

### PR #568: section-2.14: positional-token migration + the five-paths count; C-wave complete (2026-07-02)

The coverage-gaps register's 56 renumber-fragile positional TODO tokens (14 distinct, written against a numbering two re-tiers old) replaced with stable row-subject-verified topic phrases via a scripted apply with census; the portal generator's hardcoded "four deeper-dive paths" corrected to five with the startup roadmap's function added, and the same stale count fixed in four sibling documents (the audit named two; the parallel-case guard found two more). Also rewrites L-d as the promoted C10 corpus-repair item with the pattern-named 22-carrier inventory, and fixes the three #567 sweep Lows. Sections 2.12, 2.13 (to its remainder), and 2.14 now all processed; the planned C-wave is complete.

### PR #567: section-2.13 items 12-14 and 16-19: seven cross-document conflicts resolved (2026-07-02)

The ops-conflict batch, each stricter-safe or canonical-source: the P1 executive clock aligned to immediate; MFA made exception-eligible with the explicit Section-5 carve per the locked decision (the baseline reference reconciled too; privileged activations stay absolute); Internal-tier encryption required for databases, backups, and portable devices; Tier-3 supplier notifications carry the 24-hour personal-data precedence; the AI-audit Major/Minor findings crosswalked to CAPA High/Moderate; CMS accountability moved to the CCO (the canonical owner); and the risk-acceptance procedure gained the 540-day cumulative ceiling with the conversion anti-evasion clause. Section 2.13 down to item 11 plus the mapping-blocked routed note.

### PR #566: section-2.12 items 7 and 10: BASC and ANPD value sweeps; section closed (2026-07-02)

The two upstream-confirmed value sweeps: sixteen BASC "v6 2023" carriers (fifteen across twelve corpus documents plus the verifier-caught Q4-worklist expected value) reconciled to the register's V6-2022 (the 2023 the citers carried is the certification-transition date); the three ANPD carriers rewritten from the wrong Resolution No. 2 (2 business days) to Resolution CD/ANPD No. 15/2024 (3 business days to the ANPD and data subjects, staged communication, doubled for small agents) with the hedges dropped and a new canonical-citations register row anchoring the regulation. Section 2.12 fully closed.

### PR #565: section-2.12 items 6, 8, 9: citation title/domain/label corrections (2026-07-02)

Three upstream-or-source-confirmed citation fixes: the privacy policy's v3.x CCM "PRI" domain dropped (DSP stands alone); the exception policy's fabricated "A.5.36 Policy on Exceptions" title corrected twice to the true Annex A title; the cross-framework matrix's nonexistent APO12.07 replaced with APO12.06 Respond to risk, four non-canonical APO12 practice titles made canonical (three in the matrix plus a verifier-caught case-variant in the exception policy's framework list), and the ISO 31000 appetite-row citation corrected to Clause 5.4 Design (appetite lives in 5.4.2). Items 7 and 10 stay queued as upstream-confirmed value sweeps (C7).

### PR #564: section-1.8 DSAR operational conflicts closed; audit P1 cluster complete (2026-07-02)

The DSAR pair reconciled to the canonical procedure: the template's Low/Medium/High ladder replaced with the procedure's Standard/Enhanced/Re-verification levels with fail-to-suspend (not close) and the 10-business-day outer clock; denial independence supplied by a mandatory Legal Counsel written concurrence recorded in the DSR register (the CIO acting-DPO sign-off retained per policy 4.8); the 72-hour restriction acknowledgement clarified as a calendar-clock ceiling on the intake receipt. Section 1.8 fully closed, completing the 2026-07-02 audit P1 cluster (sections 1.6, 1.7, 1.8).

### PR #563: section-1.7 retention-value conflicts reconciled to the 7-year floor (2026-07-02)

The section-1.7 retention conflicts resolved stricter-safe: AI-audit and supplier-audit retention raised to the compliance policy's seven-year audit-records floor (procedure and register rows), privacy-breach notifications raised to the breach procedure's 7-year evidence minimum, and the PIA and AI-IA values composed as 7-years-or-decommission-plus-5-whichever-is-longer (the AI-IA sibling caught by the pre-push verifier); the breach procedure's consistency claim re-anchored from the retention standard (which carries no per-record value table) to the register. Section 1.7 fully closed.

### PR #562: section-1.6 item 3, risk-taxonomy reconcile + misroute + band + spelling (2026-07-02)

The ERM standard's 10-category taxonomy and the register procedure's 8-plus-other Domain enumeration reconciled to the register template's canonical 12 categories (Environmental examples redistributed, none lost; two canonical-wins defaults logged in pending-decisions); the AI-annex misroute (AI risks to "Supplier category") corrected to the AI category; the acceptance table's "Moderate" band renamed Medium; the register template's "Not Tested" respelled Untested. Section 1.6 fully closed.

### PR #561: section-1.6 item 2, FR-171 residual carrier realigned (2026-07-02)

The risk methodology's two pre-FR-171 authority lines (roles table and 6.3) realigned to the canonical chain: High and Critical risk acceptances approved by the Executive Committee or Board Risk Committee with the ERC reviewing and recommending, closing the surface FR-171 (#412/#416) missed. Also fixes the two #560 /validate-pr in-window Lows (the item-2 locator resolved by this rotation; the two bare standard citations now linked).

### PR #560: section-1.6 item 1, residual-risk formula reconcile (2026-07-02)

The methodology's multiplicative-discount residual model replaced with the canonical re-scored Residual likelihood x Residual impact (matching the ERM standard's register field model and the register template); control effectiveness stays categorical; the 1-to-25 tolerance bands now provably apply to both inherent and residual scores. First C-wave corpus fix of the overnight run.

### PR #559: GR-13, D5 coded-id closure-pattern widening (2026-07-02)

The D5 major-closure marker widened from `FR-N CLOSED` to any two-to-four-letter uppercase coded id (FR/GR/SR families), re-tested false-positive-free against the whole CHANGELOG history; lowercase narration stays excluded by the case-sensitivity guard. Positive and negative fixture cases extended in the existing D5 unit tests.

### PR #558: GR-7 + L-a + item 24 tool carriers, docstring/stale-pointer batch (2026-07-02)

Six comment/docstring corrections across five tool files: the working-prose-hygiene "gate 19" mis-cite and stale D3 filename (GR-7), the two closed-section-1.3 lineage pointers (L-a), and the two tool-side "D1-D4" carriers updated to D1-D5 (item 24; its protected CLAUDE.md carrier stays as a maintainer-gated residual).

### PR #557: GR-1, gate 59 Library-Version ordering extension (2026-07-02)

Gate 59 now asserts each CHANGELOG file's cutoff-scoped Library Versions strictly decrease top-down (integer-tuple compare), closing the change-tracking rule's described-but-nonexistent CHANGELOG version-monotonicity control. Four new fixtures; suite 254 to 258; the historical pre-cutoff non-monotonic window stays exempt by the existing cutoff.

### PR #555: GR-2, delta-check + pre-push-guard regression tests (2026-07-02)

Nineteen new fixtures: two-commit temp-repo behavioural tests for D1/D2/D3/D5 (pass, fail, and exemption/trailer cases each) plus the pre-push-guard exit-code chain (the #439 regression class pinned); suite grows 228 to 247. First GR item closed from the 2026-07-02 guardrail-review intake (GR-2 rotated out of TODO section 3.15).

### §3.11 + §3.13 + §3.14: protected `.claude/CLAUDE.md` wind-down / checklist cleanup (closed by PR #523, 2026-07-01)

Maintainer-authorized protected-file batch. §3.11: codified two wind-down SOP refinements into `.claude/CLAUDE.md` (overnight-mode-OFF is never a no-answer default, requiring an explicit maintainer signal; and a narrow metrics-grounded exception to "heavy context is never a trigger"). §3.14: reinforced the section-close cross-FILE cleanup checklist line to explicitly span gate-exempt forward `§`/`P` pointers (`.claude/` and tool docstrings). §3.13: closed as decided (the CLAUDE.md-optimization skill was declined 2026-06-28; the guidance doc shipped, the narrow diagnostic stays build-only-if-needed), no edit required.

### §3.3: Citation-verification consistency cross-check vs the scratch `ref/` base (closed by PR #522, 2026-07-01)

Ran the resume-resolved model-B consistency cross-check (register version+date vs the reference-base record, no register row): 33 ISO/IEC, NIST, CSA, COBIT, and MITRE citations present in both `governance/register-canonical-citations.md` and the reference base compared, **0 version mismatches**, so no register change. ETSI-scope sub-decision moot under model B (register-recording dropped).

### §3.2: CHANGELOG detailed-mirror per-PR-header parity check (gate 59, closed by PR #521, 2026-07-01)

Added gate 59 (CHANGELOG mirror header-parity audit), a cutoff-scoped (PR >= #463) check that the root CHANGELOG and its detailed mirror carry the same per-PR entry-header set, closing the cross-commit orphaned-header gap (the #388 defect) that per-commit delta check D1 is blind to. Wired across all four parity surfaces with a four-case regression fixture; the guardrail-review growth-narrative count advanced to fifty-nine.

### §3.5 (was 4.3): Standard Version Upgrade Procedure (2026-07-01)

Authored `governance/procedure-standard-version-upgrade.md` (Procedure, 1.0.0), the seven-step corpus-wide edition-transition process (authoritative diff, corpus-wide sweep, positional-vs-substantive classification, per-classification apply, register + verifications-register supersession, gate-6 confirmation, campaign CHANGELOG) with roles, framework alignment, and a limitations baseline. Registered in `governance/README.md` and the document-index register (gate 47/38); regenerated taxonomy/portal/scorecard.

### §3.14 (tooling half): gate-2 coverage of generator emitted-prose strings (2026-07-01)

Extended gate 2 (`tools/lint-language.py`) to scan the `tools/build-portal.py` and `tools/build-taxonomy.py` generators' non-docstring string literals (parsed via `ast`) for the three prose house-style rules (dash, `-ise`, `ensure that`), closing the double-blind gap where the generated `docs/` output is excluded and the `.py` source was never scanned as markdown. Two regression tests added (emitted-prose flagged; docstring exempt). §3.14 trimmed to its companion non-tooling residual (a maintainer-gated close-out-checklist reinforcement).

### §3.9 (was 4.22): document the scratch `ref/` base as the standing citation ground-truth (closed by PR #515, 2026-07-01)

Added §6.6 to `governance/specification-citation-verification.md` describing the scratch `ref/` tree as the local citation-verification source, its trust buckets mapped to the §6.1 tiers, the believed-current-storage constraint, and the `/matrix-fit` control-title reference base (S-11 + S-5; S-12 was FYI-only). Rotation completed 2026-07-01 after #515 closed the item without rotating it out of TODO.

### §1.5 residual: MITRE ATLAS reference-version currency (closed 2026-07-01)

Brought the `grc_library_scratch` MITRE ATLAS reference current: archived the deprecated v5.6.0 (legacy data-format) set to `ref/.superseded/frameworks/MITRE/` and installed v2026.06 (the current v6.0.0-format release, upstream-verified 2026-07-01) with re-extracted tactics/techniques/mitigations CSVs, catalogue/README/index/REGISTER updates, and `validate.py` OK. The corpus register was already at v2026.06 from #512, so register and scratch are now coherent. The 51 `needs-reconfirm` register rows remain the standing §1.5 residual (awaiting a browser-egress reconfirm pass).

### PR #511: TODO §1.3-B word-form count gate (broadened gate 39, closes §1.3, P1) (2026-06-30)

Broadened gate 39 (`lint-gate-count-consistency.py`) with a word->number map (1-99) and narrow, anchored word-form patterns (P9-P12), closing the gate-39-blind word-form class that let a stale "fifty-seven" survive until #510 fixed it by hand. Detects word-form gate counts ("<word> audit gates", "<word>-gate"), the qualified rule count ("<word> governance rules"), and the growth-narrative "rules/skills/gates to <word>" (the only skill-count check); pervasive bare small-numbers ("two rules", "one gate") never match, and `## Version history` sections are skipped as frozen logs. Maintainer-chose the narrow precision-first design (over full coverage or won't-fix). Closes TODO §1.3 entirely (§1.3-A closed in #510). 222 regression tests (217 + 5). Spec 1.16.25 to 1.16.26.

### PR #510: TODO §1.3-A new-skill-drafting checklist (completed skill-authoring-discipline, P1) (2026-06-30)

Completed the `skill-authoring-discipline` skill's Process with the four parallel new-skill surfaces it left implicit (repository-internal link depth, the slash-command sibling, the PAIRS registry for gate-44 step-parity, and the `lint-language` pre-flight), with matching Verification and a Common Rationalizations row. Placed in skill-authoring-discipline (its owner) rather than the worker-brief template the #213 retro had guessed, per the maintainer's 2026-06-30 decision. Also advanced the gate-39-blind word-form gate count in guardrail-review ("fifty-seven" to "fifty-eight", stale since gate 58 landed in #509). Pack 1.53.7 to 1.53.8. §1.3-B (broaden the count gate) remains open.

### PR #509: TODO §1.2 Per-document ISO Annex A validity audit (gate 58, P1) (2026-06-30)

Shipped gate 58 (`lint-document-iso-annex-a.py`), the ISO-column sibling of gate 54 and per-document counterpart of gate 49's ISO column: validates ISO/IEC 27001:2022 Annex A codes, theme-only refs, same-theme ranges, and clauses in ISO-labelled per-document framework tables (matrix and pack excluded), edition-pinned and table-scoped so a bare prose `§N` is never mis-read. Extracted the shared `iso_27001_reference` module (gate 49 refactored to import it so the two ISO gates cannot drift); wired all four surfaces + a 9-test regression fixture. Maintainer-chosen separate-gate, theme-only-valid design.

### PR #508: NIST SP 800-88 Rev. 2 re-point + IEEE 2883 introduction (§1.5 follow-up #3, P1) (2026-06-30)

Re-pointed media sanitization to NIST SP 800-88 Rev. 2 (final 2025-09-26; Rev. 1 withdrawn) and introduced IEEE 2883:2022 as a newly-cited standard (new register `## IEEE standards` section + allow-list domain) for the Clear/Purge/Destruct techniques Rev. 2 now defers to; updated 4 corpus surfaces + the lead doc's framework-alignment column. Maintainer-chosen faithful+IEEE option; verified against the maintainer-supplied IEEE 2883 PDF. **Closes the §1.5 version-upgrade follow-ups** (27033/27036-2/800-88 all shipped).

### PR #507: ISO/IEC 27036-2 2014 -> 2022 citation upgrade (§1.5 follow-up #2, P1) (2026-06-30)

Upgraded the superseded `ISO/IEC 27036-2:2014` to the current `ISO/IEC 27036-2:2022` (Cybersecurity, Supplier relationships, Part 2: Requirements; Edition 2 cancels and replaces the 2014 first edition) in the register row and the 1 version-bearing corpus citer (`supply-chain/procedure-supplier-due-diligence.md`). Upstream-confirmed via WebSearch (iso.org 82060). Second of the 3 §1.5 version-upgrades; only NIST SP 800-88 Rev.2 remains.

### PR #506: ISO/IEC 27033 -> 27033-1:2015 citation correction (§1.5 follow-up, P1) (2026-06-30)

Corrected the non-existent `ISO/IEC 27033:2020` to `ISO/IEC 27033-1:2015` (Part 1, Overview and concepts; current 2nd ed., confirmed unchanged 2021) across the register row and the 2 corpus framework-alignment tables that inherited the phantom year. Upstream-confirmed via WebSearch (iso.org 63461). First of the 3 §1.5 citation-impact version-upgrades; 27036-2 and 800-88 remain.

### PR #505: §1.5 reference version-currency register (P1) (2026-06-30)

Added `Upstream check location` + `Last verified (UTC)` columns to all 16 tables of the canonical-citations register (100 rows upstream-verified 2026-06-30, 51 `needs-reconfirm`), wired the advisory staleness cadence + scratch-is-storage principle into the citation-verification spec (§12.3, §7 allow-list), and applied 7 upstream-confirmed register corrections; built under the high-assurance harness (deterministic apply + re-parse + dual adversarial verifiers, one finding fixed). Three citation-impacting version-upgrades (27033, 27036-2, 800-88) and the ATLAS scratch-archival deferred as follow-ups (new §1.5 / pending-decisions).

### PR #504: §1.3 compute-don't-ask codified into clarify-before-acting (P1) (2026-06-30)

Closed the §1.3 compute-don't-ask residual (#269): added a **compute-first gate** to the `clarify-before-acting` pack rule (and its byte-identical `.claude/` mirror) so a findable fact is retrieved, not asked; updated the paired skill for parity. The other two §1.3 residuals (new-skill-drafting checklist #213, count-gate remainder) stay open.

### PR #501: §1.3 backlog-rotation prevention for prose-named items (P1) (2026-06-30)

Closed the §1.3 rotation-prevention sub-item (the #495/#496 miss): broadened the D5 PR-time rotation check to detect `FR-N CLOSED` and prose `clos... the ... item/directive` closures (not only `clos... TODO §`), chosen empirically for zero historical false-positives, and reworded the protected `.claude/CLAUDE.md` rotation lines to be backlog-item-keyed (a prose-named or maintainer-directed item rotates like any TODO item). Bare lowercase `Closes FR-N` deliberately left undetected (narration false-positives); maintainer decision. The rest of §1.3 (compute-don't-ask, new-skill-drafting checklist, count-gate remainder) stays open.

### PR #499: lint-language `-ises` inflection gap closed (P1) (2026-06-30)

Closed the P1 lint-language `-ises` item: widened gate 2's `ISE_PATTERN` so each Commonwealth `-ise` verb stem carries all four inflections (it had missed the third-person `-ises`, so `recognises` / `operationalises` passed unflagged). Canadianized the 24 occurrences the widened gate surfaced (across 23 files: 16 corpus/project docs, one with two, plus 7 `dev-security/claude-rules/` pack files, the pack edits maintainer-approved as mechanical spelling-only), added a regression fixture. The gate-widening and the cleanup shipped coupled (the gate is red without the fixes).

### PR #497: FR-58: inheritance-vocabulary Adoption Disposition column added corpus-wide (2026-06-30)

Closed FR-58 (the maintainer-decided 3-label inheritance vocabulary): added an Adoption Disposition column to the Document Index and Classification Register classifying all 292 active documents as `library-internal` (8), `template` (282, the default), or `reference` (2), defined the vocabulary in the Key Terms register, and added the disposition-model section + a maintenance rule. Locus chosen by the maintainer (index-register column, no metadata-block change). A pre-push skeptical verifier drove three corrections: the library quality-cadence procedure and its health-report template reclassified to `library-internal` (library-maintenance machinery, not adopter deliverables), and (maintainer decision) the four framework-alignment matrices that were labelled `reference` to `template` (they are library-authored mappings of the library's own documents, not external content kept as-cited; the fifth matrix was already `template`), leaving `reference` = the 2 external-citation/tool catalogue registers. Non-template docs were individually apply-time-verified; the template defaults were classified by Type-rule.

### PR #495: OT post-ingestion validation: OT corpus confirmed sound vs NIST SP 800-82r3 + ISO 27019 (2026-06-30)

Closed the maintainer-directed OT source-validation P1 item: an audit subagent read the 6 `operations/ot/*` docs and the 6 PR-#494 OT matrix rows against NIST SP 800-82r3 + ISO/IEC 27019:2024 and found the OT work sound (IEC 62443 correctly primary, CSF choices aligned, ISO 27019 correctly energy-scoped). Applied the one low finding (GAP-1, safety-as-overarching note in `annex-ot-security-overview.md`); GAP-2 assessed immaterial. Rotation completed late in the following PR (the #495 close-out omitted the TODO-to-DONE rotation; maintainer-flagged).

### NIST SP 800 ingestion (completed in grc_library_scratch; rotated 2026-06-30)

Closed the maintainer-prioritized NIST SP 800-series relevance-review P1 item: this row rotates the grc_library tracking item out of TODO.

### PR #494: FR-167 CLOSED: compliance-matrix gap-fill (6 OT docs + AI Security Tooling Landscape register) (2026-06-30)

Added the final 7 matrix rows via the high-assurance dual-verifier harness, closing FR-167 (item (a) closing `/matrix-fit` #490; item (b) net-new docs #491, OT + AI register #494). The FP verifier fixed 6 control-code mis-fits, the FN verifier added 3 grounded codes and confirmed the customs columns are correctly N/A; the deprecated `annex-regional-privacy-requirements.md` stub was excluded (maintainer decision). Carries the #493 `/validate-pr` + `/retro` rows.

### PR #492: FR-24: Control-testing procedure deepened to operational depth (2026-06-30)

Deepened `compliance/procedure-control-testing.md` (153 to 235 lines) to peer operational depth: sampling methodology, working-paper/evidence standards, per-result response requirements, reporting distribution, overdue-remediation escalation chain, independent effectiveness validation, a Control Testing Register, and metrics. Via the high-assurance-tier skeptical verifier, which caught and fixed a pre-existing fabricated records-retention domain name. The result-classification-scheme reconciliation (SOX vs canonical) was deferred to the maintainer (pending-decisions), not folded in.

### PR #489: TIA cross-reference wiring (2026-06-30)

Wired the new Transfer Impact Assessment template into the docs that reference a TIA: the cross-border-transfer procedure (Related Documents), the EU privacy annex, the DPIA template (which deferred TIAs to "a separate template" without linking it), the cross-border data flow register (reciprocal), and the governance glossary's TIA entry. Five versioned-body co-bumps; bookkeeping-tier discoverability wiring (lint-links + the post-merge /validate-pr as controls; no harness). Closes the queued TIA-wiring follow-up (#483); FR-74's residual is now just the Schrems II operational deepening.

### PR #488: FR-61 (high): Financial-services prudential regulators outside EU/US (2026-06-30)

Extended the financial-services sector annex's regulatory-landscape overview with the missing prudential regulators: a new Asia-Pacific subsection (MAS Singapore, APRA Australia, HKMA Hong Kong, JFSA/FSA Japan), a Switzerland subsection (FINMA), and an explicit US federal-banking-regulators row (OCC/FRB/FDIC). Named structurally (regulator + supervisory domain + iconic instruments, no pinned versions) with an adopter-confirm note, since no authoritative financial-services prudential source was available. Closes FR-61 (all nine listed regulators now mapped; PRA/FCA + OSFI were pre-existing). Authored via the high-assurance harness; FP verifier 0 defects with all six instruments upstream-confirmed via WebSearch, FN verifier 0 content gaps + 1 heading-case warning fixed. Annex co-bumped 1.0.4 -> 1.0.5.

### PR #487: FR-144 (high): Breach Notification Regulator Register Template (2026-06-30)

Shipped `privacy/template-breach-notification-regulator-register.md`: an adopter-fillable register (one row per applicable regulator) with the six §6.2 columns plus the missing internal-target deadline (the "no internal clock" gap), and a strictest-applicable-requirement rule (earliest deadline + broadest individual-notification obligation when multiple regimes engage). Wired into the breach-response procedure §6.2 (the fixed table framed as illustrative; the adopter register is authoritative; co-bump 1.4.16 -> 1.4.17). Closes FR-144. Authored via the high-assurance harness; both verifiers clean (FP 0 defects, illustrative rows non-authoritative, no over-claim; FN 0 content gaps, one metadata field-order warning fixed). Also fixed the #486 /validate-pr finding (stale AIGC ethics-review KPI in `governance/framework-continuous-assurance-and-improvement.md` reattributed to the Panel; 1.0.4 -> 1.0.5). Listed in privacy/README and the document-index register.

### PR #486: FR-73 (high[critical]): AI Ethics Review Panel Charter (2026-06-30)

Split AI ethics review out of the AI Governance Council into a new independent `ai/charter-ai-ethics-review-panel.md` with a structured five-step challenge-and-escalation mechanism (the Panel can challenge an AIGC decision on ethical grounds, forcing documented reconsideration, and escalate an unresolved objection to the Board above the AIGC). Panel owned by the CRO (independent of the AIGC's CIO/CISO line); chair + voting majority outside the AIGC; challenge-not-veto (approval stays with the AIGC). Edited the AIGC charter (1.2.2 -> 1.2.3) to cede independent ethical review to the Panel and remove its residual ethics-review self-claim. Closes FR-73. Authored via the high-assurance harness; both verifiers clean (FN completeness/independence 0 gaps; FP citation/authority/contradiction 0 defects). Listed in ai/README and the document-index register.

### PR #485: FR-72 (high[critical]): Sanctions and Export-Control Screening Standard (2026-06-30)

Shipped `compliance/standard-sanctions-and-export-control-screening.md`: a dedicated sanctions / OFAC / export-control screening Standard with denied-party / restricted-party screening (onboarding, periodic, event-driven, transaction), beneficial-ownership / UBO verification (incl. the OFAC 50% aggregate-ownership rule, attributed), and export-control regime coverage (EAR/BIS, ITAR/DDTC, EU dual-use, Wassenaar), all named structurally with no pinned list versions. Closes FR-72 (sanctions treatment was previously incidental). Placed in `compliance/` as a Standard per fitness-review Rec-14. Authored via the high-assurance harness: both adversarial verifiers clean (FP 0 defects, no pinned versions, OFAC 50% rule attributed/unpinned, AML scope-fenced; FN 0 error-level gaps + 4 operability refinements folded in). Re-wired the M&A procedure's financial-crime/sanctions dimension to this standard (replacing "is planned"). Listed in compliance/README and the document-index register.

### PR #484: FR-71 (high[critical]): M&A Due Diligence Procedure (2026-06-30)

Shipped `compliance/procedure-mergers-acquisitions-due-diligence.md`: a GRC M&A due-diligence procedure (four phases with gates; a 13-dimension due-diligence checklist each cross-referenced to its governing corpus instrument; a red-flag/deal-breaker register; hand-off into the governance triggered review, the post-close internal audit, and the risk register, incl. a TIA re-trigger for inherited transfers). Closes the gap the GRC programme procedure's M&A trigger pointed at. Placed in `compliance/` per the originating fitness-review Rec-14 plan. Authored via the high-assurance harness: FP verifier 0 defects (ISO 31000/37301, COBIT EDM03/APO12/BAI05, NIST CSF GV all verified; no COSO; no phantom links; no invented thresholds); two FN completeness improvements applied (divestiture scoped out cleanly; sanctions coverage-gap noted in Limitations). Listed in compliance/README and the document-index register.

### PR #483: FR-34 (high[critical]): Transfer Impact Assessment (TIA) template (2026-06-30)

Shipped `privacy/template-transfer-impact-assessment.md`: the EDPB Recommendations 01/2020 six-step methodology (map, identify tool, assess effectiveness/Schrems II, supplementary measures, procedural steps, re-evaluate) as adopter-fillable fill-tables, grounded in GDPR Chapter V (Arts 44 to 49, held and quotable) with the methodology attributed to the EDPB Recommendation (not held, framed in own prose) and SCCs referenced generically (no unverified version pinned). Authored via the high-assurance harness; both verifiers clean on citations (0 false positives), two FN completeness improvements applied in-window (Art 46(2)(e)/(f) tool routes; Art 48 foreign-disclosure-order assessment). FR-74 consolidates: its instrument half is delivered, residual is the annex/procedure deepening (left open). Listed in privacy/README and the document-index register; TIA cross-ref wiring queued as a follow-up.

### PR #482: FR-31 (high[critical]): Privacy by Design Framework (GDPR Article 25) (2026-06-30)

Shipped `privacy/framework-privacy-by-design.md`: operationalizes GDPR Art 25 (by design, by default, certification) by mapping the seven foundational privacy-by-design principles (attributed to Cavoukian, distinguished from the Art 25 legal duty) to architecture and dev-security workflows, with the four Art 25(2) by-default dimensions as testable defaults and a supporting-instruments map (DPIA, LIA, pseudonymisation, data classification). Authored via the high-assurance harness; the dual verifiers caught an orchestrator-introduced `ISO/IEC 29134:2023` hallucination (recurrence of a logged class) and it was fixed to `:2017` pre-merge. Listed in privacy/README and the document-index register.

### PR #481: FR-145 (high): AI security standards scope/precedence note + crosswalk (2026-06-30)

Resolved the overlapping-scope-with-no-precedence gap between `ai/standard-ai-security-and-risk.md` (governance baseline) and `ai/standard-ai-and-agentic-development-security.md` (technical implementation): added a "Relationship" section + 12-row crosswalk to the former and a prose back-reference to the latter, with a cumulative altitude-based precedence note (both apply; the more-specific technical control governs implementation; neither relaxes the other). Verified by a refute-briefed skeptical verifier (0 substantive defects). No hard seniority or ownership change asserted (the two retain distinct Owners). Also bundled the #480 /validate-pr fix (LIA `recognises`->`recognizes`).

### PR #480: FR-32 (high[critical]): Legitimate Interest Assessment (LIA) template (2026-06-30)

Shipped `privacy/template-legitimate-interest-assessment.md`: the GDPR Article 6(1)(f) three-part test (purpose, necessity, balancing) as adopter-fillable tables, plus the public-authority threshold exclusion, the Article 9 special-category caveat, the Article 21 right-to-object handling (with the Article 21(4) prominence prompt), and the Article 5(2) accountability link. Authored via the high-assurance harness (two independent adversarial verifiers); listed in privacy/README and the document-index register.

### PR #477: ERC acronym residual (P3): lowercase-drift fix + tier-table reconcile (2026-06-30)

Closed the P3 ERC residual: fixed the 3 lowercase "executive risk committee" occurrences Sweep 77 (B-1/2/3) found (#456's title-case reconcile had missed them) in the DLP standard and the board-risk-report template, and applied the maintainer-answered tier-table reconcile to the minimum-viable-governance guideline (collapse the Tier-1 duplicate row, drop the Tier-2 stray). Canonical body is "Enterprise Risk Committee (ERC)" per the role-authority register; no distinct "Executive Risk Committee" body exists. Corpus-wide grep confirms 0 residual.

### PR #471: §4.6 (P4): QA-cadence mechanical enforcement closed as satisfied (2026-06-29)

Closed §4.6 as substantially-satisfied by the existing gate 50 Check 1 (`lint-bookkeeping-parity.py`), which already enforces §4.6's mechanically-valuable missing-row half corpus-wide (every in-window PR needs a `validate-pr` + `/retro` row, with the handoff/subsumption exemptions). The residual abbreviated-marker half is not FP-free-mechanizable on the free-prose row schema (the S3-shaped finding), so it stays the CLAUDE.md "Throughput pressure does not authorise QA abbreviation" convention. Maintainer-decided "close 4.6 as satisfied". No new gate.

### PR #470: docs/ house-style enforcement gap closed (P3) (2026-06-29)

Brought the authored `docs/` adopter guides under the gate-2 language/style audit (scan extended to `docs/`, generated artefacts excluded, worked-example meta-tutorial exempted from heading-case/sanitisation/ensure) and fixed all 117 accumulated findings (71 dashes, 25 `-ise`, 4 heading-case, 1 vendor name). Maintainer-decided "full house-style now".

### PR #469: §4.10 (P4): TODO/DONE-rotation gate family completed (2026-06-29)

Closes TODO §4.10. The rotation gate family is now complete across two PRs: gate 57 (the static marked-done detector, `lint-todo-marked-done.py`) shipped in #468, and this PR adds the complementary **D5 PR-time check** (`check-todo-rotation-on-pr.py`) that fails when a PR's added CHANGELOG lines assert a TODO-item closure (`clos... TODO §X`) but the diff does not rotate the item (touch both TODO.md and DONE.md), with a `TodoRotation:` opt-out trailer and the handoff-PR exemption. D5 caught the #466-class wholesale-forgotten rotation that gate 57 cannot see.

### PR #466: §4.5 S4: gate 56 bare-normative-shall audit (2026-06-29)

Closes TODO §4.5 S4. New gate 56 (`lint-bare-normative-shall.py`) flags a bare normative `shall` in authored corpus prose (the FR-44 `shall`->`must` harmonized form), the plain-form complement to gate 9 (which only fires on a `shall` adjacent to an uncertainty marker), excluding the 3 preserved classes. 4-surface wired with a 5-case fixture; gate count 55 to 56. (Rotation itself shipped in the follow-up PR per the #466 `/validate-pr` in-window finding.)

### PR #463: S2 resolved by promoting 5 maintainer roles into the role-authority register (2026-06-29)

Closes TODO §4.5 S2. The scoped "role-consistency gate" was already shipped as gate 8 (`lint-roles.py`), so S2 reframed (maintainer choice) to migrating the 5 roles in that gate's `EXTRA_KNOWN_ROLES` allow-list (GRC Programme Manager, Compliance/Information Security/Security Architecture Maintainer, Governance Library Maintainer) into the register as the single source of truth; allow-list emptied. No new gate, no gate-count change.

### PR #462: S1 cross-document retention-consistency gate (gate 55) (2026-06-29)

Closes TODO §4.5 S1: new `tools/lint-retention-consistency.py` (gate 55) verifying that the evidence-retention period each of three procedures (CAPA, internal-audit, control-testing) cites matches its canonical row in the Data Retention Schedule register; the mechanical enforcement of the register rows' existing "matches ..." cross-reference notes. Wired into all four parity surfaces + a 4-case regression fixture; gate count 54 to 55.

### PR #461: codify the skeptical pre-push verification standard (2026-06-29)

Maintainer-directed (not previously in TODO): a tiered verifier standard layered on the five disciplines (not a sixth), no verifier for quick fixes, one refute-briefed verifier pre-push for substantive changes, the full high-assurance harness for sensitive ones; with the validate-fix-re-verify loop (three-strikes-then-defer), the "overruling a verifier is never silent" log (finding + reasoning + revert path), and the new override register [`.working/verifier-overrides.md`](verifier-overrides.md) surfaced at the next attended boundary / `/resume` step 7. Stricter early-run oversight kept in memory, not codified, per maintainer direction.

### PR #460: correct the wind-down decision framework (default is continue, not hand off) (2026-06-29)

Maintainer-directed after ~13 of 15 assistant-proposed handoffs were the wrong call: the default is now CONTINUE, a handoff needs named degradation evidence (work-size/shape/length are NOT triggers), large series are worked PR-by-PR with skeptical verifier subagents. Put through a skeptical verifier before commit (its first real use), which caught a residual section-level contradiction; fixed and re-verified clean. The skeptical-verifier standard + override-logging discipline is queued as a follow-up.

### PR #459: act on the #458 /retro improvements (verification-scope checklist line + queue S4 gate) (2026-06-29)

Shipped improvement #1 as a `.claude/CLAUDE.md` close-out-checklist line (a corpus-wide completion claim must be verified by greping the full corpus, not the change's own input set, the scope-width companion to the bare-token line); queued improvement #2 (the "no bare normative shall" gate) in TODO §4.5 as candidate S4. One facet of §4.8; §4.8 stays open. Batches the #458 /validate-pr + /retro rows.

### PR #458: Sweep 75 iter 1 close-out + FR-44 completion fix (2026-06-29)

The `/resume` loop-break corpus-wide `/validate` over the #451..#457 deltas surfaced one escalation finding (it contradicted a #457 asserted-clean claim): the #455 FR-44 sweep had missed dev-security/policy-secure-development-and-engineering.md entirely (absent from #455's 17-doc list), leaving 12 bare normative "shall"; this PR converted them to "must" and the corpus is now genuinely shall-free outside the 3 preserved classes. Not previously a separate TODO item; surfaced by Sweep 75 as the completion of FR-44.

### PR #455: FR-44: corpus-wide shall->must normative-verb harmonization (2026-06-29)

Converted all 125 normative "shall"/"shall not" to "must"/"must not" across 17 documents (per master-spec §6.1's must/must-not register) and fixed the stale glossary doctype definitions that still sanctioned "shall"; a deterministic scripted apply preserved the 3 non-normative occurrences (the lint-shall-near-uncertainty.py filename references and a backticked word-reference).

### PR #454: §4.24: pack-README rule-scope table completed (2026-06-29)

Added the four missing governance-rule rows (9 to 12: trust-recovery-escalation, project-integrity, surface-counterproductive-instructions, high-assurance-verification) to the pack README "Rule files and their scope" table, which had fallen behind as the pack grew past rule 8; the table is exhaustive by design, so completed rather than scoped.

### PR #444: gate 50 check 4 (version-history parity) + DD-10 completion (2026-06-28)

Added gate 50's fourth internal check (version-history parity: a file's metadata Version must appear as a row in its own `## Version history` table; the #376 mechanizable half, no new gate, no count ripple) and bundled the #443 `/validate-pr` HIGH fix (vetting-log Status line, the third "18" carrier, to 19).

### PR #443: DD-10 (low): addyosmani spot-scanned skill count corrected 18 to 19 (2026-06-28)

Web-verified the upstream addyosmani/agent-skills repo at 24 skills; the EXT-01 vetting examined all 24 (5 fully vetted + 19 spot-scanned, the latter explicitly listed in the vetting-log), so the propagated "18 spot-scanned" undercount was corrected across the vetting-log, the pack README, and the setup-generator prompt.

### PR #435: S-1 MITRE ATT&CK / ATLAS version-currency register reconciliation (2026-06-28)

Closed scratch-review S-1: bumped [`register-canonical-citations.md`](../governance/register-canonical-citations.md) MITRE rows to the upstream-confirmed current versions (ATT&CK v15 -> v19.1, ATLAS v4.7 -> v2026.05; both re-verified upstream this turn), with the corpus sweep updating the four stale MITRE entries in the in-scope Q4 verification worklist (audited domain docs cite version-less forms). Also fixed the #434 /validate-pr finding (resume.md:25 standards-vs-frameworks self-contradiction); the scratch re-ingest half stays open under §4.26 + pending-decisions.

### PR #434: codify "never assert a state you cannot observe" (2026-06-28)

Not previously in TODO; maintainer-directed after the discipline was breached this session. Extended the evidence-grounded-completion pack rule (+mirror) with the un-observable-state / inventory / external-version-currency corollary (pack 1.51.1), sharpened the wind-down framework (named observable signal required), and added the Reference-version-currency SOP + scratch-index-load to /resume + handoff + runbook §6; applied it to catch that scratch ATLAS v5.6.0 is deprecated vs upstream v2026.05 (logged pending).

### PR #433: handoff pruning convention + Sweep 71 (2026-06-28)

Not previously in TODO; maintainer-directed. Pruned the session handoff from 426 lines / 47 stacked session blocks to ~120 (keep current + 1 prior) and codified the prune-at-resume convention across the handoff, the /resume command (step 6a), and the CLAUDE.md close-out checklist. Ran the loop-break Sweep 71 (A/C clean; B 2 gate-exempt notes resolved by the prune; no asserted-expectations contradiction).

### PR #431: suggest/advise interpretation rule codified + version-register directive captured (2026-06-28)

Not previously in TODO; maintainer-directed. Added the suggest/advise interpretation bullet to the Communication conventions section of .claude/CLAUDE.md, and captured the maintainer's reference version-currency register directive as TODO 4.26 (with the extend-the-canonical-citations-register recommendation and the egress/scope caveats).

### PR #430: Communication-conventions codification (2026-06-28)

Not previously in TODO; maintainer-directed during the #429 close-out. Added a Communication conventions section to .claude/CLAUDE.md: no decorative honesty-intensifiers, and use IMPORTANT: as the emphasis marker.

### PR #429: FR-188 (low) + FR-198 (low): trust-recovery tail (2026-06-28)

Closed the last two low-severity trust-recovery findings: FR-188 retargeted the supplier-exit deletion-certificate escalation off the DPO (the responsible party) to Legal and the Contract Owner; FR-198 swapped the matrix Pseudonymisation row's loose DSP-10 for DSP-16 (Data Retention and Deletion).

### PR #428: Domain-wide privacy PRI-* CCM citation correction (low) (2026-06-28)

Completed the invalid-`PRI-*` correction across the remaining 3 privacy files (7 citations: the policy framework-mapping table x5, the charter range, the PIA row) after the #427 `/validate-pr` found the class was domain-wide. Three unambiguous mappings (DSP-11/SEF-08/DSP-09) plus four recommended-default judgement-calls (GRC-06/DSP-12/DSP-10/charter DSP-domain reference) recorded in pending-decisions for confirm/redirect. Not previously a standalone TODO item; the domain-wide remainder of the #427 privacy-code class.

### PR #427: Privacy source-doc framework-table CCM code defects (low) (2026-06-28)

Corrected five mis-cited CSA CCM codes across two privacy procedures: PRI-04 to DSP-11 (data-subject rights), PRI-05 to SEF-08 (breach-notification programme), SEF-02 to SEF-06 (SIEM/event triage), each validated against the in-repo CCM v4.1 reference module. Closes the TODO P3 "Privacy source-document framework-table control-code defects" item (surfaced in FR-167 batch 11 research).

### PR #424: FR-178 (medium) + FR-194 (low) + FR-199 (low): P2 editorial/format remainder (2026-06-28)

FR-178: both the information-security and privacy policies converted fully to "must" (maintainer Option B, 31 + 23 occurrences); FR-194: ELT (Executive Leadership Team) added to the glossary; FR-199: the two soft-law register "Current version" cells (WP216, EDPB Opinion 28/2024) normalized to "Original (no later revision)". Rebuilt from the abandoned-#422 carry-forward.

### PR #423: surface-counterproductive-instructions governance rule (the 11th) + #422 fold-in (2026-06-28)

Added the eleventh pack governance rule (stop, consider, confirm before acting on a clear-but-counterproductive instruction; charitable-interpretation corollary; anti-over-ask calibration), maintainer-directed after a literal "wind down" reading reverted committed work (not previously in TODO). Also folded in the abandoned #422 handoff's #421 `/validate-pr` + `/retro` rows and fixed the adopter-guide:60 "Core reference set" casing residue.

### PR #421: FR-182 (medium) + FR-195 (FYI) + FR-196 (low) + FR-197 (FYI): README and adopter-guide navigation reconciliation (2026-06-28)

Fourth P2 batch (navigation cluster): FR-182 made the README:271 "grow-toward catalogue" framing canonical (README:80 and adopter-guide:83/:228 now point to the Day-1 floor + Tier 1 starter set as the day-one start, Core reference set as the grow-toward catalogue); FR-195 added a discoverability pointer after the catalogue intro (lower-effort than linking 39 titles); FR-196 relabelled the 7 README bullets "thematic areas" and bridged them to the 11 domain directories; FR-197 assessed as no-change (deliberate two-tier funnel, portal generated). Batches the #420 `/validate-pr` (0) + `/retro` rows.

### PR #420: FR-181 (medium) + FR-192 (low) + FR-193 (low): privacy jurisdiction and breach-notification reconciliation (2026-06-28)

Third P2 batch (privacy cluster): FR-181 made the EU AI Act Annex III index entry forward-looking ("become applicable in August 2026"); FR-192 added a Breach notification (Articles 48 to 49) bullet to the Brazil annex, propagating the breach-response procedure's attributed ANPD figure under a verify-before-reliance qualifier; FR-193 added India to the §6.2 breach-notification table, the §1.2 scope, and the §12 framework-alignment table, grounded in the India annex's DPDPA duties (no fabricated clock). Batches the #419 `/validate-pr` (0) + `/retro` rows.

### PR #419: FR-191 (low) + FR-189 (low) + FR-190 (FYI): incident and resilience procedure reconciliation (2026-06-28)

Second P2 batch (incident/resilience cluster): FR-191 harmonized the P1/P2 post-incident-review deadline to 5 business days corpus-wide (the maintainer's library default; cross-domain joint, privacy-breach, AI-incident, and remote-working device-loss PIRs all moved 10 to 5, P3/P4 tiers unchanged), grep-confirmed none left at 10; FR-189 named the Executive Sponsor as the EOC activation authority in the crisis-management procedure; FR-190 assessed as no-change (informational, mitigated by Limitations clauses). Batches the #418 `/validate-pr` (0) + `/retro` rows.

### PR #418: FR-176 (medium) + FR-183 (low) + FR-184 (low): security cross-reference and Wi-Fi floor cluster (2026-06-27)

First P2 trust-recovery-finding batch (security floor/cross-reference cluster, fan-out research): FR-176 added a crosswalk note linking the encryption policy's data-classification key-rotation cadence to the key-lifecycle framework's key-type cadence (no value change); FR-183 pointed the authentication standard's password-Storage row to the Encryption and Key Management Policy as the governing hashing-parameter floor; FR-184 (maintainer decision) raised home-network Wi-Fi to WPA3 with an IoT carve-out and reconciled the surrounding "encouraged"/"does not mandate" framing. Batches the clean Sweep 68 loop-break `/validate` row.

### PR #416: FR-175 (high): India DPDPA in-force-date reconciliation (2026-06-27)

Last remaining trust-recovery High closed: the privacy jurisdiction index said the India DPDP Rules 2025 were "published February 2025 and entered into force April 2025", contradicting the India annex (notified 13 Nov 2025, phased commencement). Web-verified the MeitY notification (Gazette G.S.R. 846(E), 13 Nov 2025; draft published 3 Jan 2025) against two independent legal sources, then reconciled the index entry to the annex and the already-correct canonical citations register. Clears the entire decided-value + verified High set (FR-168..175).

### PR #415: FR-174 (high) + FR-179 (medium) + FR-180 (medium): incident-response reconciliation (2026-06-27)

Fourth trust-recovery-remediation batch (the incident-response cluster, researched via a fan-out worker): FR-174 reconciled the P2 CISO-notification timing to 1 hour (maintainer-chosen, strictest) across the incident-response procedure (:48 4h to 1h, resolving the intra-doc conflict with the already-canonical :79) and the escalation matrix (:41 2h to 1h; CIO stays 2h as an escalation ladder); FR-179 corrected the superseded NIST SP 800-61 Rev.2 title at three citers to the register's verified Rev.3 title ("Incident Response Recommendations and Considerations for Cybersecurity Risk Management (CSF 2.0 Community Profile)"); FR-180 added a severity crosswalk to the resilience intake procedure mapping its Low/moderate/high/critical scale to P1-P4 (crosswalk, not flatten, retaining "pending"). The last remaining High finding is FR-175 (India DPDPA, deferred to a fresh session for external-source verification). Batches the #414 `/validate-pr` (0) + `/retro` rows.

### PR #414: FR-172 (high) + FR-186 (low) + FR-187 (low): retention-schedule reconciliation (2026-06-27)

Third trust-recovery-remediation batch (the retention cluster, all reconciled to the canonical data-retention-schedule register): FR-172 reconciled the ROPA template's "at least three years" retention to the schedule's "Active + 5 years" (Article 30 ROPA, stricter-safe); FR-186 replaced the consent-management framework's vague consent-record retention with the schedule's "duration of processing + 3 years" (GDPR Article 7) + cross-reference; FR-187 added a reconciling clause to the records-retention standard clarifying the RRS register is DPO-owned / CIO-approved with the Compliance Manager/Records Officer maintaining it operationally. Also fixed the two in-window findings #413's `/validate-pr` surfaced (the audit-programme §5/§6 gate-45 sweep-cursor description + the design-decisions stale "frozen in TODO" claim, both stale after #413's gate-45 re-point) and batched the #413 `/validate-pr` (2, fixed here) + `/retro` rows.

### PR #413: TODO hygiene: relocate resume-metadata to session-handoff + rotate FR-167 batches (2026-06-27)

TODO-hygiene pass (maintainer-flagged): moved the `## Session resume metadata` sweep-history block out of TODO into [`session-handoff.md`](session-handoff.md) (a machine-readable "Resume cursor" section) so TODO stays purely forward-looking, and re-pointed gate 45's sweep-cursor check to read the cursor there (queued-PR check still scans TODO); rotated the FR-167 inline shipped-batch ledger to DONE and trimmed the FR-167 bullet to its forward-looking remainder. Queued the deferred broader TODO-hygiene pass as §4.23.

### FR-167 batches 1-11: comprehensive compliance-matrix per-domain expansion (#275 through #404, rotated 2026-06-27)

All eleven per-domain matrix batches shipped (rotated to DONE in bulk in PR #413 after the maintainer flagged the shipped history left inline in the FR-167 TODO bullet): batch 1 architecture (#275), 2 risk (#313), 3 dev-security (#317), 4 supply-chain (#341), 5 resilience (#378), 6 operations (#380), 7 compliance (#383), 8 governance (#384), 9 security (#385), 10 ai (#402, new AI section, matrix 1.9.1 to 1.10.0), 11 privacy (#404, the final per-domain batch, matrix 1.10.0 to 1.11.0). Remaining FR-167 work (the matrix's partial sections, completion, and the closing whole-matrix `/matrix-fit`, plus the open AICM-column decision) stays in TODO as the trimmed FR-167 bullet.

### PR #412: FR-169 (high) + FR-171 (high) + FR-177 (medium) + FR-185 (low): risk scoring & acceptance-authority reconciliation (2026-06-27)

Second trust-recovery-remediation batch, the risk-domain reconciliation: FR-169 reconciled the ERM standard's likelihood scale to the canonical threat-precedent anchors in the risk-assessment methodology (maintainer-chosen over the standard's time-frequency anchors); FR-171 aligned the risk-acceptance procedure and risk-appetite template to the single canonical High/critical acceptance authority (Executive Committee or Board Risk Committee, per the exception/risk-acceptance policy §2.2), replacing the divergent "Executive Management" and "CRO" values; FR-177 aligned the ERM standard's Low-band action verb to the methodology ("Accept; monitor annually"); FR-185 narrowed the ERM §5.2 three-document-match over-claim (the register references the scale rather than independently defining it). Batches the #411 `/validate-pr` (0) + `/retro` rows.

### PR #411: FR-168 (high) + FR-170 (high) + FR-173 (high): cheap-certain trust-recovery High remediation batch (2026-06-27)

First remediation of the trust-recovery routed backlog (High-first, fix-issues-before-new-content): FR-168 corrected the policy-exception policy's eight `GRC-12` citations (an AICM-only code) to the real CCM v4.1 `GRC-04` "Policy Exception Process"; FR-170 repointed the risk-register template's 5×5-matrix reference from the methodology procedure (which holds only the scales and thresholds) to the canonical grid in the ERM standard §5.2; FR-173 repaired three broken section cross-references in the onboarding/offboarding procedure (Section 9→10 privileged-access timeline, two Section 10→11 deprovisioning-checklist refs). Also batches the clean Sweep 67 history row.

### PR #408: B2 (low): add five EDPB / WP29 soft-law citations to the canonical-citations register (2026-06-27)

Added WP216 (Opinion 05/2014 anonymisation), WP248 rev.01 (DPIA), EDPB Guidelines 07/2020 (controller/processor), Guidelines 3/2018 (territorial scope), and Opinion 28/2024 (AI models) to the soft-law section of `register-canonical-citations.md`, each verified against the freshly-ingested `grc_library_scratch/ref/publications/` extracts. Unblocked by the two 2026-06-27 EDPB maintainer drops; closes the long-deferred-on-egress B2.

### PR #405: FR-30: GDPR Article 28 Data Processing Agreement template (2026-06-27)

Shipped `privacy/template-dpa-article-28.md`, the controller-to-processor DPA template consolidating the eight Article 28(3)(a) to (h) clauses + sub-processor (28(2)/(4)) and written-form (28(9)) requirements into one populatable instrument; wired into the matrix, document index, and privacy README. Closes the H[critical] FR-30 (no DPA template previously existed).

### PR #399: P-4.20 PR B: the /matrix-fit semantic-fit audit skill + command + cadence (2026-06-27)

Shipped PR B of §4.20, completing the cadenced semantic-fit instrument for the gate-blind "valid code, wrong control" class: the `matrix-fit` skill (sixteenth pack skill) + `/matrix-fit` command judge each cited control code against the source TITLE over the PR-A worklist; cadence wired into CLAUDE.md and the worker-brief (after each FR-167 batch, at completion, ad-hoc). §4.20 fully closed (PR A was #394).

### PR #397: FR-140-followup (low): README Core-reference-set catalogue label corrected (2026-06-27)

Fixed the README:277 catalogue row for the enterprise governance-and-risk policy: title corrected to "Enterprise Governance and Risk Management Policy" and the domain label moved Governance to Risk (the row relocated into the Risk block), matching the artefact's home domain (maintainer-confirmed).

### PR #392: Trust-recovery /full-qa remediation: matrix + source-doc control-code semantic-fit fixes (2026-06-27)

A maintainer-invoked `/full-qa` over the FR-167 matrix found 9 "valid code, wrong control" and structural defects (all Medium/Low); all fixed: 8 matrix cells, the detailed-CHANGELOG-mirror header repair (F-1), and the 7 source documents whose own framework tables carried the same class (closing the Source-doc framework-table control-code corrections item). Also populated 3 governance trade cells (maintainer redirect) and ended overnight mode.

### PR #381: project-governance separation §5.3 resolved + Phase 2 review-schedule migration (2026-06-26)

Closed the §5.3 deferred-classifications item: `register-coverage-gaps.md` stays corpus (adopter-routing role), and `register-document-review-schedule.md` migrated to `.project-governance/` (Phase 2) with its 7 corpus citers severed or re-pointed to the reusable corpus patterns. The separation spec gained a distinct §5.4 Phase-2 subsection.

### PR #372: gate-49 extension wired as gate 54 (track PR 3/3, closes the gate-49-extension item) (2026-06-26)

Wired [`tools/lint-document-control-codes.py`](../tools/lint-document-control-codes.py) into all four audit surfaces as **gate 54** (per-document control-code validity), now that PR #371 left the corpus clean; added the runs-clean-on-corpus-at-HEAD smoke test, the §5/§6 spec entries, and bumped the gate count 53→54 across the prose carriers (including the gate-39-blind guardrail-SKILL word-form). Closes the gate-49-extension item; the per-document defect class (CSF-1.1 codes in NIST tables) is now a standing mechanical check. ISO Annex A per-document validation deferred to a P3 follow-up.

### PR #371: DD-12 corpus-wide CSF-1.1 to CSF 2.0 migration (gate-49-extension track PR 2/3) (2026-06-26)

Closed DD-12: migrated the 5 surviving CSF-1.1-era NIST codes in per-document framework tables to CSF 2.0, using the #370 scanner to verify the corpus clean (310 docs). `ID.SC`→`GV.SC` dedup (risk), `RS.RP-1`→`RS.MA-02` + `DE.DP-5`→`DE.AE-06` + `DE.DP-3`→`DE.AE-07` (operations), `RC.IM`→`ID.IM` (compliance), all grounded in NIST CSWP 29 subcategory text with the maintainer's by-row-activity choice for the removed DE.DP category. PR 3 wires the scanner as a gate.

### PR #368: §4.14 CHANGELOG-hygiene first-commit pre-flight aid (2026-06-26)

Closed TODO §4.14: added [`tools/preflight-changelog.py`](../tools/preflight-changelog.py), a commit-gating aid run as `python3 tools/preflight-changelog.py && git commit ...` that exits non-zero when the added lines of the root CHANGELOG or its detailed mirror carry an em/en dash in prose or an unlinked path-shaped reference, closing the recurring commit-then-amend loop (#341/#347/#349/#355). A standalone helper rather than a pre-commit hook because no pre-commit git hook fires on commits in this environment. Batches the #367 `/validate-pr` (0 findings) + `/retro` rows.

### PR #367: §4.15 audit-programme functional-category-index currency (2026-06-26)

Closed TODO §4.15: brought the audit-programme spec §5 functional-category list current with gates 49-53 (49→Content-drift; 50/52→Programme-and-index-integrity; 51→Language-and-style with the em-dash gate 9; 53→Reference-integrity as a link-target check) and recorded the gate-ordering decision (keep numeric append-order; §5 is the orthogonal functional view, §6 the canonical numbered inventory). Batches the #366 `/validate-pr` (0 findings) + `/retro` rows.

### PR #366: §4.17 Version-Date co-bump check (delta gate D4) (2026-06-26)

Closed TODO §4.17: added PR-only delta gate D4 (`tools/check-date-cobump-on-pr.py`), which fails when a PR bumps a versioned document's Version but leaves its Date not equal to the bump commit's UTC date, closing the residue gates 40 and 31 leave open (gate 31's 1-day tolerance passed the #325/#352 cases). Built as a delta gate rather than a gate-40 extension because prototyping showed a HEAD-state form has a 78-doc historical false-positive surface; the delta form has none. Wired into quality.yml, the PR-time runner, and spec §6.1 with a `DateCobumpOnPrTests` regression class. Also batches the Sweep 53 loop-break `/validate` row (1 out-of-window note, cross-referenced into DD-12).

### PR #362: corpus-to-project directional-dependency gate (gate 53) (2026-06-26)

Closed the TODO P2 directional-dependency gate: added gate 53 (`tools/lint-directional-dependency.py`), the mechanical backstop for the project-governance-separation spec §4 one-way dependency rule, flagging any deliverable-corpus document that links into `.project-governance/` (the §4 counterpart to gate 52's §7.4 scan-scope parity); deliverable-corpus scan set derived from `AUDITED_DOMAIN_DIRS` minus `.project-governance` plus the root specs, pack subtree excluded per §4. Wired into all four surfaces with a `DirectionalDependencyTests` regression class; §7.3 rewritten from "queued" to built, §4 cross-reference updated. Also batches the Sweep 52 loop-break `/validate` row (0 findings).

### PR #360: directory-scan-scope parity meta-check (gate 52) (2026-06-26)

Closed the TODO P2 directory-scan-scope parity meta-check: added gate 52 (`tools/lint-scan-scope-parity.py`), the mechanical backstop for the project-governance-separation spec §7.4, forbidding any content linter from hardcoding the audited-domain run now that PR #359 gave it a single source of truth (`lint_common.AUDITED_DOMAIN_DIRS`); robust to all three declaration styles because it matches literal directory names, with a documented EXEMPT set for the corpus-only-set divergent files (section-placement gate, taxonomy generator, collection-candidate helper). Wired into all four surfaces with a `ScanScopeParityTests` regression class; §7.4 narrative updated to the single-source-of-truth model.

### PR #357: Gate 51 (working-tree prose-hygiene) added to the audit programme (2026-06-26)

Added gate 51 forbidding em-dashes and en-dashes in `.working/` prose (allowed inside inline code spans and fenced blocks), ratcheting the #353 `.working/` em-dash conformance so it cannot silently regress; wired into all four surfaces with a `WorkingProseHygieneTests` regression class, and the gate-39-blind guardrail-review growth-narrative word-form bumped to fifty-one. Not previously a TODO P-item; from the handoff 20-PR integrity-tooling plan. Also batches the deferred Sweep 50 loop-break `/validate` row (0 findings).

### PR #344: §4.13: 50-gate `/guardrails` coherence review (2026-06-25)

Ran the first `/guardrails` structural-integrity review (maintainer-directed, auto-prompted by the gate-50 addition) over the 50 gates + 10 rules + 15 skills: 0 overlap findings, 0 drift findings, machinery verdict coherent. Routed two new low-severity items (§4.14 CHANGELOG-hygiene pre-flight aid; §4.15 §5 functional-category-index currency + the keep-append-order gate-ordering decision); three gap candidates were dedup-confirmed against already-queued TODO 61/62/88.

### PR #343: Gate 50 (bookkeeping-parity) added to the audit programme (2026-06-25)

Added the §4.11 worker-provenance / bookkeeping-parity gate (`tools/lint-bookkeeping-parity.py`): QA-cadence parity + TODO/DONE rotation parity + a dormant worker-provenance stub, wired into all four surfaces (49→50 gates) with a 13-case regression class. Its first live run caught a real pre-existing gap (#342's missing handoff-exemption row).

### PR #336: Project-governance separation Phase 1: citation-verification cluster migration (2026-06-25)

Executed the §8.1 migration: created the audited-not-exempt `.project-governance/` directory with its own README index and moved the six citation-verification campaign artefacts (verifications register, bundle index, four batch worklists) out of `governance/`, severing every corpus→project inbound citation per the one-way dependency rule. Re-pointed the two path-targeted linters and added `.project-governance` to the explicit-list content linters so the new dir gets the full §6.3 audit sweep; generators exclude it by their include-list design. Closes the R2 cluster relocation.

### PR #326: §4.6a: gate 49 NIST CSF 2.0 category-membership + 17-cell remap (2026-06-24)

Closed the §4.6a follow-up: extended gate 49 to validate each NIST token's CATEGORY against the authoritative CSF 2.0 22-Category set (wired `nist_csf_reference.py`, sourced from NIST CSWP 29), and remapped the 17 CSF-1.1-era cells the membership check flags (`ID.SC`×5 → `GV.SC`, `ID.BE`×1 → `GV.OC`, `PR.IP`×11 to per-row 2.0 categories). Gate 49 now checks well-formedness + membership; matrix `1.3.0`→`1.3.1`.

### PR #325: gate 49: matrix control-code validity audit (2026-06-24)

Built the §4.6a control-code-validity gate (`lint-matrix-control-codes.py`) over the FR-167 compliance matrix: ISO 27001:2022 Annex A membership + clause format, NIST CSF 2.0 well-formedness; CCM stays gate 48's job; customs/trade columns free-text/out-of-scope. Wired into all four surfaces + a regression class; 48→49 gates. NIST category-membership + the 17 CSF-1.1-cell remap deferred to the §4.6a follow-up (kept open in TODO; the maintainer supplied NIST CSWP.29 for it).

### PR #324: handoff asserted-expectations convention (2026-06-24)

Codified the maintainer-accepted handoff-QA convention: a session-closing handoff records what it asserts clean (scoped to surfaces it actually verified) plus a green-at-sha mechanical baseline, and the next `/resume` `/validate` cross-checks findings against those claims. Replaces the rejected (wasteful, noisy) two-run-diff idea. Not previously in TODO; surfaced as the maintainer's `/resume` design question this session.

### PR #323: Sweep 41 close-out: jurisdiction-index:102 CPPA-as-live fix (2026-06-24)

The `/resume` loop-break corpus-wide `/validate` (control for handoff #322) found and fixed one out-of-window finding: the privacy jurisdiction-index cross-jurisdiction row presented CPPA adequacy + max-fine as operative (a third carrier after :45/#320 and :133/#321), qualified "(if enacted)". Also corrected the stale sweep cursor (handoff said "Sweep 40"; Sweep 40 had already run as the #319 control).

### PR #321: FR-140 (high): adopter starter-set divergence (2026-06-24)

Resolved the starter-set count/scope divergence: added `policy-acceptable-use` and `policy-identity-and-access-management` to the adopter-guide Tier 1 set (15 → 17 docs) so the 6-artefact Day-1 floor is now a strict subset, harmonized the 15→17 count and reconciliation prose across quickstart/adopter-guide/decision-tree, and reframed the README "Core reference set" (and added the two floor artefacts it was missing, acceptable-use and incident-response, ~37 → ~39) so its catalogue no longer competes with the starter tiers and the floor nests cleanly inside it. Bundled the #320 `/validate-pr` out-of-window fix (annex-privacy-jurisdiction-index Bill C-27 "under parliamentary study" → lapsed-2025 consensus) per recursion-avoidance.

### PR #320: DD-8: CPPA-as-live → PIPEDA scrub (medium) (2026-06-24)

Corpus-wide scrub of the live-regime-sense Consumer Privacy Protection Act (CPPA, lapsed Bill C-27) to PIPEDA (the in-force Canadian federal privacy law) across 29 documents, full principled scrub per maintainer choice: bare CPPA in live-applicable lists → PIPEDA, "PIPEDA / CPPA" pairs → drop the redundant live-CPPA, CPPA-specific content (algorithmic-transparency row, jurisdiction-coverage index) qualified "(proposed)/(pending)", and the glossary "PIPEDA being superseded by CPPA" factual error fixed. Preserved the distinct California Privacy Protection Agency sense and all already-qualified pending/proposed mentions. Surfaced by PR #264 (FR-138), which scrubbed three privacy docs and deferred the broader sweep.

### PR #318: DD-4/DD-5: TLS 1.3 (medium) (2026-06-24)

Completed the FR-135-deferred TLS-1.3 rewrite of the pack's `languages/go.md` (MinVersion now TLS 1.3; dropped the now-prohibited explicit TLS-1.2 cipher-suite list, which Go ignores under a 1.3 minimum) and raised supplier-questionnaire Q5.4 from "TLS 1.2 or higher" to "TLS 1.3 or higher". The operations media-handling surface was already TLS 1.3 (no change needed); `core/owasp.md` intentionally left at the OWASP ASVS baseline.

### PR #314: Project-governance separation specification; R2 closed by principle (2026-06-24)

Added `governance/specification-project-governance-separation.md` defining the corpus-versus-project governance boundary: the reusable-pattern-versus-operational-instance criterion, the one-way dependency rule (project may cite corpus; corpus must not cite project), the `.project-governance/` destination convention (dot-prefixed, not exempt, fully audited), and the phased migration procedure. Closes R2: the citation-verification cluster is classified project governance and migrates in Phase 1; `register-canonical-citations.md` resolved to stays-corpus; R1 confirmed correct in `tools/`.

### PR #310: DD-2/3/11: risk-vocabulary harmonization to the canonical ERM scale (medium) (2026-06-24)

Aligned every risk-scoring scale label across four docs to the canonical ERM scale (likelihood Very Low/Low/Medium/High/Very High; impact Negligible/Minor/Moderate/Major/Catastrophic; rating Low/Medium/High/Critical): concentration-risk (Rare…Almost Certain → canonical likelihood; Severe → Catastrophic), operational-risk-register (Moderate → Medium likelihood + sample rating; Severe → Catastrophic impact; casing), procedure (impact-5 Critical → Catastrophic), and enterprise-risk-register template (impact-5 Critical → Catastrophic in two fields + the matrix header). The rating-top "Critical" (17-25) was preserved everywhere; the impact-5/rating "Critical" conflation is resolved. Corpus-wide grep confirmed all risk-scoring docs now agree.

### PR #309: S5: gate-48 bare-domain-code check (medium) (2026-06-24)

Added Check 4 to `tools/lint-ccm-aicm-citations.py`: a bare superseded/fabricated CCM domain code (no `-NN` suffix) is flagged when its line names the matrices or sits under a CCM/AICM section and is not a historical rename-note, the family-list / domain-keyed-crosswalk residual class gate 48 was previously blind to. Precision-first (zero corpus false positives: `.NET`, currency `AUD`, MODEL-GOV, and rename-notes all pass; TODO meta-exempted); four regression cases added. Completes the gate-48 enhancement pair with S4.

### PR #308: S4: gate-48 section-aware + cross-catalogue title check (medium) (2026-06-24)

Extended `tools/lint-ccm-aicm-citations.py` to look up control-listing titles section-aware (a row under a `## CSA CCM` heading checks against CCM v4.1.0, under `## AICM` against AICM v1.1.0, else the union) and added a cross-catalogue check that flags a divergent-title control (I&S-07) cited with the other catalogue's distinctive word, the gate-escaping class the #299 `/validate-pr` had to catch by hand. Two regression cases added; gate stays clean on the corpus.

### PR #307: Working-state relocation R1: closed won't-move (medium) (2026-06-24)

The `tools/sweep-preflight-exemptions.json` relocation was closed **won't-move**: the file is the pre-flight scanner's config and belongs with the scanner in `tools/`; moving it to `.working/` would bake a `.working/` path into the two distributable pack SKILLs that reference it. Maintainer-decided. (R2, the citation-cluster relocation, stays deferred.) Closed in the morning-processing PR alongside resetting the overnight file to stub.

### PR #305: Generalize the handoff-PR QA loop-break into the pack layer (medium) (2026-06-24)

Named the session-closing-handoff-PR exception (the one sanctioned skip of the mandatory per-PR `/validate-pr` + `/retro`) in the two distributable pack surfaces (the `validation-sweep-pr-scoped` SKILL and the `ai-assistant-workflow-disciplines.md` no-skip clause + its `.claude/` mirror), with the loop-termination rationale and the corpus-wide-`/validate`-on-resume compensating control, so adopters inherit the exemption. Previously the exception lived only in this project's `.claude/CLAUDE.md` + `/resume`.

### PR #304: Working-state relocation R3: register-main-branch-protection.md → .working/ (medium) (2026-06-24)

Relocated the Main Branch Protection Configuration Register (a snapshot of *this* repo's GitHub branch protection, project-application state meaningless to adopters) from `governance/` into `.working/`, per the PR #116 corpus-doc-relocation precedent: slimmed its metadata to a working-state header, deleted its rows from the governance README and the document-index register, and regenerated taxonomy/portal/scorecard. One of the three queued working-state relocations (R1 the exemption-file and R2 the citation cluster remain; R1 deferred for a pack-design decision, see overnight-pr morning-review).

### PR #303: Day-1-floor risk-artefact drift (medium): harmonize the named 6th floor artefact (2026-06-24)

Resolved the two "six-artefact Day-1 floor" definitions disagreeing on the risk artefact: the startup-roadmap named `procedure-risk-register.md` while the quickstart and adopter-guide Tier 1 named `policy-enterprise-governance-and-risk-management.md`. Per maintainer option A, the policy is now the named risk floor artefact in both surfaces, with register-population kept as recommended-follow-on guidance. Also resolves the "different 6th artefact" sub-part of FR-140 (which remains open for the starter-set count divergence and Tier 1 omissions).

### PR #299: Gate 48 (CCM/AICM citation-accuracy audit) + gap-register full title alignment (2026-06-24)

Shipped the mechanical backstop for the CCM/AICM citation class: gate 48 (`lint-ccm-aicm-citations.py`) validates domain/range and code-to-title against a fair-use catalogue reference (`ccm_aicm_reference.py`, derived from CSA CCM v4.1.0 / AICM v1.1.0, no normative content), wired into all four surfaces + regression fixture; gate count 47 to 48. Fully aligned the compliance-controls gap register's control titles to authoritative values (the PR #298 `/validate-pr` finding, found to be systematic). Implements the #298 `/retro` proposed improvement (the code-to-title gate). Carries the batched #298 `/validate-pr` + `/retro` rows.

### PR #298: Sweep 35 close-out + corpus-wide CCM/AICM citation reconciliation; DD-12(a) (2026-06-24)

Sweep 35 `/validate` (the #297 handoff loop-break control) found A-1 (GRM→GRC matrix) and B-1 (AI-log 12mo→7yr); verifying A-1 exposed a systemic CCM/AICM citation problem, and the maintainer supplied the authoritative CSA CCM v4.1.0 + AICM v1.1.0 catalogues for a full reconciliation. Removed the fabricated `GOV` domain (no such domain in either; governance is `GRC`) across ~9 docs (GOV-01..08→GRC; fabricated GOV-09/10 removed with A&A / AICM GRC-10/11/12 add-backs where real); renamed the superseded `IVS`→`I&S` (34×, corpus + pack); mapped the non-existent `NET`→real I&S network controls (resolving **DD-12 part a**); fixed out-of-range `IPY-05`→`IPY-04`; bumped AICM v1.0.3→v1.1; tightened loose `CCM v4`/`v4.0.12`→`v4.1`. A catalogue-derived validator confirms zero residual invalid codes. Catalogues kept in scratchpad only (no-redistribution licence). A `lint-ccm-aicm-citations.py` gate is queued next.

### PR #297: Session-closing handoff (2026-06-24 resume session); FR-160 third-surface fix (2026-06-24)

Session-closing handoff PR for the 2026-06-24 resume session (which shipped #293 Sweep 34 close-out, #294 PR-H, #295 metrics refresh, #296 PR-I). Discharges the #296 `/validate-pr` finding: `operations/register-asset-inventory.md` DR tier labels "Essential"/"Important" → "Business Essential"/"Standard" (`1.0.3`→`1.0.4`), so all three carriers (DR plan, SLM standard, asset inventory) now agree, completing FR-160's harmonization. Carries the batched #296 `/validate-pr` + `/retro` records and the session-handoff refresh (queues the relocation bundle R1/R2/R3 with full ripple map, then the integrity-tooling phase). Wound down on the SOP's large-series clause (the relocation bundle is the atomic-or-break series, deferred to a focused next session, matching a prior session's identical judgment). Skips its own trailing `/validate-pr` + `/retro` per the handoff-PR exception; Sweep 35 is the next `/resume` compensating control.

### PR #296: FR-149 + FR-150 + FR-151 + FR-159 + FR-160 + FR-165 + FR-12 (medium/low/FYI): cross-document consistency bundle (PR-I) (2026-06-24)

Cross-document consistency bundle (PR-I): the AI security standard's adversarial-test-category claim is genericized to count-agnostic (FR-149, the guide's 6th category is an application-specific template and §B4 treats five as the fixed set, so the naive five→six fix would over-count); the children's-data framework's unsupported "Under 18/under 15" Japan APPI age is softened to a no-fixed-statutory-age hedge matching the PIPEDA row (FR-150); the cross-domain incident-coordination PIR deadline (§86) now defers to the per-severity table (P1 5 days, not a blanket 10) (FR-151); the portal generator points the Overview at the glossary (FR-159); the DR plan's Tier 2/3 labels align to the SLM standard's canonical "Business Essential"/"Standard" (FR-160); and a frozen Sweep-22 record's overstatement (claiming abbreviated /validate-pr rows were relabelled) is corrected with a footnote that preserves the original text and the honest abbreviation record, not by relabelling the rows (FR-165). FR-12 was already closed by PR #239 (stale TODO line deleted). Also lands the two #294 /validate-pr retention-ripple fixes (records-retention standard range 1-5→1-7 years; logging standard example list) and the #295 README-Date fix. Carries the batched #295 /validate-pr + /retro records.

### PR #295: TODO §4.9: refresh the frozen hallucination-metrics summary table (2026-06-24)

Recomputed the worker-hallucination metrics summary table (frozen since PR #176) from the live catches/escapes logs. The recompute surfaced two clarifications: the log had conflated worker-draft errors (the defined metric) with orchestrator-side discipline catches (now counted separately), and the worker-draft escape rate is low and falling (no worker-draft escape logged since #167) while the active failure class is now orchestrator-side multi-surface incompleteness. Working-state only; carries the batched #294 `/validate-pr` + `/retro` records.

### PR #294: FR-120 + FR-155 + FR-53 + FR-109 + DD-6/DD-7 + FR-75 + FR-76 (medium/low): governance/registers + ESG bundle (PR-H) (2026-06-23)

Seven governance/register/ESG fitness items shipped as PR-H: the exception policy's 180-day baseline attribution is softened to state that neither NIST 800-53 CA-6 nor ISO 27001 Clause 9.2 prescribes a fixed interval (FR-120); the enterprise-risk policy's stale CSA CCM v3 "GRM" domain id is corrected to v4.1 "GRC" (FR-155, one line, the other two cited files were already correct); the ingestion spec now documents the Classification (lifecycle) vs Confidentiality (content-sensitivity) distinction so the two metadata fields are non-redundant (FR-53, decided: document not deprecate); the governance-library charter's dense purpose paragraph is tightened (FR-109); the AI-compliance checklist's AI-log retention is reconciled up from 12 months to the canonical 7 years and a matching AI decision-and-detection-logs row (7 yr; ISO 42001 + EU AI Act Annex IV) added to the data-retention schedule, also fixing a broken "12 months per logging standard" cross-reference (DD-6/DD-7); the ESG disclosure guideline gains a qualitative double-materiality assessment process for the materiality threshold (FR-75); and the sustainability framework gains qualitative ESG escalation triggers, CIO to ERC to Board (FR-76). B2 (five EDPB/WP29 soft-law citations) was deferred from this PR: verifying the citation titles/years/bodies needs web egress that is policy-blocked this session.

### PR #291: FR-153 + BYOD-MDM/MAM + FR-90 + FR-84 + FR-85 + FR-86 (medium/low): security/crypto bundle (PR-F) (2026-06-23)

Six security/crypto fitness items shipped as PR-F: the encryption policy's password-based KDF requirement is updated to Argon2id-preferred (OWASP min params) or PBKDF2-HMAC-SHA256 at 600,000 iterations (SHA-512 at 220,000), replacing the stale unqualified 310,000 (FR-153); the BYOD policy is reframed from MAM-only to present MDM and MAM as adopter-selectable deployment models with explicit enrolment-consent requirements for MDM (BYOD, maintainer-directed); the developer-security standard gains CSP / Trusted Types / HSTS-preload browser-hardening requirements (FR-90); the patch-management regression-testing checklist is reformatted into a tick-through table artefact (FR-84); the breach-response 24-hour initial assessment now assigns a per-question lead (DPO / CISO / Legal) instead of diffuse joint ownership (FR-85); and the recovery runbook's communications section now cross-references the Crisis Communication Plan (FR-86).

### PR #290: FR-64 + FR-65 + FR-66 + FR-78 + FR-152 + FR-69 + FR-68 + FR-156 + FR-157 + FR-158 (medium/low): adopter/docs-UX bundle (PR-E) (2026-06-23)

Ten adopter-experience fitness items shipped as PR-E: CONTRIBUTING now points new-sector/jurisdiction contributors at exemplar annexes to mirror (FR-64); the adopter guide's upstream-sync section now covers merge conflicts, adopter-side gate relaxation (relax-and-document), and version-monotonicity, plus a new "running the audit toolchain on your fork" note on the PII/secrets gates and the exemption mechanism (FR-65, FR-66); the framework-architecture doc drops the "audit theatre with nicer fonts" maintainer aside (FR-78); the quickstart "Next steps" is reordered to the portal's canonical workflow sequence with startup-roadmap set apart as the "add later" path (FR-152); the 6 / 15 / ~25 starter-set sizes are now cross-referenced as nesting rather than competing across the quickstart, adopter guide, and decision tree (FR-69); the startup-roadmap's incoherent "minus the A1 elements" wording is corrected so the skip applies to the optional A1 module not the mandatory baseline (FR-68); the adopter guide gains an enforcement/disciplinary-clause "what to change" row (FR-156); "DPO" is expanded on the quickstart Day-1 path (FR-157); and the adopter guide adds shortest-binding-window guidance for multi-regulator overlap (FR-158).

### PR #287: FR-147 + FR-148 + FR-101 + FR-102 + FR-100 + FR-77 + FR-83 (medium): assurance/3LoD + audit/CAPA bundle (2026-06-23)

Seven Medium fitness items shipped as one PR-C: the internal-audit standard now acknowledges the audit-planning procedure's 15-business-day final-report extension (FR-147); the CAPA procedure anchors the policy's 90-business-day post-implementation effectiveness validation by Internal Audit or Compliance (FR-148); the assurance-map closure step now names first-line-proposes / second-line-confirms sign-off (FR-101); the change-management procedure gains a compensating-control pathway as an alternative to deferring an untested-rollback change (FR-102); the cloud security configuration baseline expands its ISO row and adds a per-section CIS/ISO/NIST mapping table (FR-100); the key-terms register defines the Three Lines Model (FR-77); and the security IR and privacy breach procedures each gain a one-page 60-minute / 4-hour / 24-hour incident-command execution checklist (FR-83, whose TODO gloss "independent challenge" was a mislabel for the incident-command checklist).

### PR #283: FR-161 + FR-162 + FR-163 + FR-146 (medium): risk/AI register vocabulary aligned to canonical ERM set (2026-06-23)

Aligned the AI risk register and AI risk-methodology annex Treatment Option lists to the canonical six (Avoid / Mitigate / Transfer / Accept / Exploit / Enhance), and reconciled the retired/conflated Status values in the AI register and the ERM-template sample rows to the canonical lifecycle Open / Closed. PR-B of the XS/S batch.

### PR #282: FR-142 (high) + FR-143 (high): AI-procedure step roles + de-looped supplier escalation (2026-06-23)

FR-142: added a "Roles and responsibilities" subsection to both AI assessment procedures (model-risk and system-impact), naming the AI Governance Lead, the model/system owner, and the AI Governance Approver/Council. FR-143: fixed the circular DPO→CISO→Data Protection Officer escalation row in the supplier-onboarding procedure to terminate at the Chief Risk Officer. First PR of the XS/S batch-reduction sweep.

### PR #279: DD-9 (low): DR backup-requirements header broadened to "All systems" (2026-06-23)

Broadened the disaster-recovery plan's "Backup and restore requirements" header from "All Tier 1 and Tier 2 systems must have:" to "All systems must have:", matching its bullets which already span all four tiers after the FR-139 / Sweep-28 edits. Also closed the three #278 `/validate-pr` bookkeeping findings in the same PR.

### PR #278: DD-1 (low): new-entries-only CHANGELOG dash gate (D3) (2026-06-23)

Resolved DD-1 with a PR-time delta gate (D3, `check-changelog-dash-on-pr.py`) that flags em/en dashes only in lines a PR adds to `CHANGELOG.md`, leaving the ~130 historical dashes untouched. Scope narrowed from "extend to all of CHANGELOG" at action time after the dash count proved far larger than the backlog item assumed.

### PR #273: count-gate coverage: stale-count fix + gate-39 P8 (2026-06-23)

Fixed the stale "32 automated audits" in the library-health-report template (now count-agnostic; the programme has 47 gates) that PR #272's `/validate-pr` surfaced, and broadened gate 39 with pattern P8 (`<N> automated audits`) so the idiom that escaped patterns P1-P7 is now caught. Closes the #272 out-of-window finding + the broaden-the-count-gate P4 candidate.

### PR #272: FR-166 (high): corpus listing-surface completeness gate + authoring tool (2026-06-23)

Shipped audit gate 47 (`lint-listing-surface-completeness.py`), which hard-gates the MECHANICAL listing surfaces (the document-index register + all 11 domain READMEs) against the taxonomy active-document set, with root-level meta-specs exempt by a documented rule; plus `tools/suggest-listing-surfaces.py`, which reports MECHANICAL present/missing + ranked SEMANTIC candidates for a new doc. Fully wired across all four audit-programme surfaces with a regression fixture; SEMANTIC surfaces (matrices, glossary, Related Documents) left to suggestions + a `/validate` coverage-drift check, not a hard gate.

### PR #271: Sweep 28 `/validate` close-out: DR Tier-2 backup-cadence fix (2026-06-23)

The `/resume` compensating-control corpus-wide `/validate` found one in-window defect: FR-139/#265 fixed Tier 1's backup cadence but left Tier 2 on "daily" while binding it to a 4-hour gap/RPO, reproducing the "compliant system permanently in P2 escalation" trap one tier down (and escaping #265's own `/validate-pr`). Fixed: Tier 2 cadence now "at least every 4 hours", daily scoped to Tier 3/4.

### PR #267: FR-141 (high): remove invented PIPEDA breach "72-hour target" (2026-06-23)

PIPEDA's Breach of Security Safeguards Regulations set no fixed statutory clock ("as soon as feasible"), so the invented "(72-hour target)" was removed from the Canada-federal breach-notification deadline at both surfaces the bare-token search found: the privacy breach-response procedure (§6.2 jurisdiction table) and the security incident-response procedure (§6 regulatory-notification table). Both now read "As soon as feasible (no fixed statutory deadline)". The security-incident-response cell's separate "CPPA (Canada)" label remains for the deferred broader-CPPA sweep.

### PR #265: FR-139 (high[critical]): DR Tier-1 backup cadence meets the 1h RPO (2026-06-23)

Resolved the DR-plan self-contradiction where Tier 1 carried a 1-hour RPO but the backup section mandated "daily backups" and allowed a "24-hour gap" (so every Tier-1 backup would permanently breach the RPO and trigger P2 escalation). The backup cadence now requires continuous/near-continuous data protection for Tier 1's 1h RPO, and the backup-gap limit is aligned per tier (1h Tier 1, 4h Tier 2, 24h/72h Tier 3/4). **Completes the 6-item H[critical] locked-criticals batch (FR-134 through FR-139).**

### PR #264: FR-138 (high[critical]): scrub CPPA-as-live (3 named docs) (2026-06-23)

Removed Consumer Privacy Protection Act (CPPA, lapsed Bill C-27) treatment-as-in-force from the three named privacy documents: the data-subject-rights procedure (rights table + summary table + §8.3 + intro now cite PIPEDA Schedule 1 Principle 9/Principle 3, with a new "Canadian legal basis" note explaining PIPEDA lacks erasure/automated-decision rights and CPPA is pending reintroduction), the breach-response procedure (Canada federal basis = PIPEDA Breach of Security Safeguards Regulations; CPPA pending), and the privacy policy (rights + control-mapping cells). Broader corpus CPPA-as-live mentions (security incident-response, document-index framework tags, matrices, other privacy templates) deferred to a follow-up sweep.

### PR #263: FR-137 (high[critical]): DSAR retention harmonized to 3 years (2026-06-23)

Aligned the DSAR-record retention to the authoritative schedule's 3-year value: the records standard's DSR row and the data-subject-rights procedure §9.2 moved from "2 years post-closure" to "3 years post-closure", citing `register-data-retention-schedule.md` (Data subject access request records: 3 years, GDPR Article 30). The register was already canonical and unchanged.

### PR #262: FR-136 (high[critical]): log-retention schedule authoritative (2026-06-23)

Resolved the log-retention conflict by making `register-data-retention-schedule.md` authoritative: the logging standard §4.1 (flat "seven years") and the records standard's IT/Security row ("1 to 3 years") now defer to the schedule's tiered, by-log-class periods. Reconciled a downstream citer (security-monitoring §298, which cited §4.1 for a 7-year AI-decision-log retention) onto the established ISO/IEC 42001 + EU AI Act Annex IV basis, preserving its 7-year retention. Also forward-corrected PR #261's over-broad TLS verification claim.

### PR #261: FR-135 (high[critical]): TLS 1.3 everywhere (2026-06-23)

Migrated every org TLS-floor surface from "TLS 1.2 minimum" / "1.2+" to TLS 1.3 (or stronger), with TLS 1.2 moved to the prohibited set, across the security quick-reference, baseline reference, mobile-app-security, production-security (B2B/EDI adapter, unconditionally), the healthcare HIPAA annex, and the pack cryptography + MCP-security rules. Two surfaces deferred to maintainer review: `core/owasp.md` (represents OWASP ASVS, which permits 1.2) and `languages/go.md` (TLS code example needs coherent rewrite).

### PR #260: FR-134 (high[critical]): one canonical risk-scoring scale (2026-06-23)

Aligned the enterprise risk standard's §5.2 likelihood labels (Rare→Almost Certain ⇒ Very Low→Very High) and score-to-rating bands (1-5/6-10/11-15/16-25 ⇒ 1-4/5-9/10-16/17-25) to the canonical risk-assessment procedure, and fixed the register template's stale likelihood labels, so a given score now yields the same rating/cadence/escalation across all three risk documents. Fourth surface (concentration-risk register) and the impact-5 label divergence surfaced to the maintainer, not folded in.

### PR #258: P4.0: project-integrity.md tenth governance rule (2026-06-23)

Distributed the PRIMORDIAL RULE (Quality > Speed > Cost apex ordering) as the tenth pack governance rule `project-integrity.md` + byte-identical `.claude/rules/` mirror, wired across all three enumeration surfaces + sync-map + rule-count. Closes TODO P4.0; resolves the PRIMORDIAL RULE's "queued as P4.0" forward-reference.

### PR #257: guardrail-review skill + /guardrails (2026-06-23)

Shipped the fifteenth pack skill `guardrail-review` (`/guardrails`): the periodic structural-integrity review of the governance machinery (rules, skills, gates, wiring surfaces) for overlap, gap, and drift the mechanical parity gates cannot judge. Closes the trust-recovery-batch structural-review codification item; wired across SKILL + command + PAIRS + README tree + version bumps.

### PR #254: /trust-recovery convenience wrapper (2026-06-23)

Added the thin non-paired `/trust-recovery` command that sequences the escalation suite (full-clone check → `/full-qa` → `/fitness` → hold for sign-off). Closes the optional-wrapper codification item.

### PR #252 + #253: Trust-recovery routing convention severity-tiered (2026-06-22/23)

Revised the trust-recovery findings-routing convention from "every finding to one top tier" to severity-tiered (H[critical]/High → top tier, Medium/Low → next; nothing dropped), propagated across the rule, both SKILLs, the commands, and both CLAUDE.md bullets (#252), then completed two same-file spots the propagation missed (#253). Closes the routing-revision codification item.

### PR #247: Session migration protocol + bookkeeping cleanup (2026-06-22)

Adds [`.working/session-handoff.md`](session-handoff.md) + the `/resume` command + the CLAUDE.md session-migration / PR-close-out-checklist section, so a fresh session resumes with one command (the long-session-degradation defence). Also rotated FR-164 and the shipped codification-checklist items into DONE, fixed a stale governance-rule count in TODO, and carried the #246 validate-pr/retro rows.

### PR #246: Ninth governance rule trust-recovery-escalation + FR-164 (2026-06-22)

Shipped the ninth pack governance rule (the trust-recovery escalation tier: /full-qa + /fitness suite, top-priority findings routing, maintainer-sign-off termination) across all three enumeration surfaces + the `.claude/rules/` mirror. Closed FR-164 (collection-enumeration docstring "seven" → "nine").

### PR #245: PRIMORDIAL RULE: project integrity (2026-06-22)

Added the apex Quality > Speed > Cost integrity rule to `.claude/CLAUDE.md`; queued P4.0 to distribute it as a project-agnostic pack governance rule.

### PR #244: deep-qa-review skill (/full-qa) (2026-06-22)

Codified the trust-recovery AI-failure-pattern forensic pass as the `deep-qa-review` skill + `/full-qa` command, with the shallow-clone full-clone step-0 rule baked in.

### PR #243: Trust-recovery suite routing + re-tier (2026-06-22)

Ran `/full-qa` + `/fitness` r2 (32 findings; a shallow-clone gate-31 false positive caught and excluded); routed and re-tiered findings to TODO P1/P2/P3 after maintainer sign-off.

### PR #242: Sweep 22 iter 1 close-out + discipline-failure corrective actions (2026-06-22)

Sweep 22 reconciled 11 consecutive PRs (#231-#241) where the orchestrator had recorded "abbreviated spot-check" rows in `validate-pr/history.md` without dispatching the formal Subagent A; 4 in-window errors surfaced (treatment-vocab propagation gaps in 4 risk-domain files from PR #238/#239 surface drift), all fixed. SKILL files, pack-rule copies, and `.claude/CLAUDE.md` all updated with explicit abbreviation prohibition and throughput-pressure clause; P4.6 mechanical-enforcement gate candidate queued.

### PR #241: Closes FR-97 + FR-98 (P2.3 cross-framework matrix bundle, both M, S) (2026-06-22)

`governance/matrix-cross-framework-alignment.md` v1.1.4: ISO 31000 clause numbers corrected against actual ISO 31000:2018 §§6.4.2/6.4.3/6.5/6.6/6.3/5.3 (closes FR-97). `compliance/annex-nis-2-implementation.md` v1.1.0: Article 21.2 sub-measures table gains Evidence class column for all 10 sub-measures (closes FR-98). PR-E in Batch 2.

### PR #240: Closes FR-93 + FR-94 (P2.6 KRI/KPI bundle, both M, S) (2026-06-22)

`risk/register-key-risk-indicators.md` v1.1.0: KRI schema gains Red-Threshold Escalation Owner + Red-Threshold Evidence Class fields (closes FR-93). `risk/register-assurance-map.md` v1.1.0: Linked-controls field text expanded to name it as adopter-defined, explain the placeholder-ID convention, and bootstrap path (closes FR-94). PR-D in Batch 2.

### PR #239: Closes FR-12 cross-doc (M, S): procedure-risk-register treatment vocab aligned with ERM standard canonical 6 (2026-06-22)

`risk/procedure-risk-register.md` v1.1.0: Step 8 "Select Treatment" now references the standard's canonical 6 options (Avoid/Mitigate/Transfer/Accept/Exploit/Enhance). "Monitor" / "Further Analysis" remapped to Treatment Status workflow values (Pending / In Progress / Complete). Register-field row split into Treatment Option + Treatment Status to match PR #238's standard §7.1 schema. PR-C in Batch 2.

### PR #238: Closes FR-118 (H, S): ERM §6/§7 treatment-vocab internal inconsistency resolved (2026-06-22)

`risk/standard-enterprise-risk-management.md` v1.6.0: §6 gains terminology paragraph distinguishing Treatment Option (6 choices) / Treatment Status (workflow: Pending/In Progress/Complete) / Status (risk-record lifecycle: Open/Closed). §7.1 register fields update: Treatment Status field added; Status value set narrowed from "Open/Mitigated/Accepted/Closed" to "Open/Closed" with explanatory prose. Closes the ambiguity surfaced during Pass-2 reshape (Avoided risks had no clean Status value). PR-B in Batch 2.

### PR #237: Closes FR-36 (H, S): GDPR Article 8 child-consent age table per Member State (2026-06-22)

`privacy/jurisdictions/annex-privacy-european-union.md` v1.1.0: new section between Cross-border-transfers and Enforcement covering 30 Member States (27 EU + 3 EEA) with each state's chosen age (13/14/15/16) and national implementing-law citation. `privacy/framework-childrens-data.md` v1.0.5 row updated to cross-reference the new table. PR-A in Batch 2 effort-first run. Also carries Sweep 21 zero-finding history row + PR #236 register rows.

### PR #236: Closes P7 maintainer decisions (A2 + B4 + FR-47): role-authority cross-ref + canonical-citations soft-law scope (2026-06-22)

PR-G in Batch 1 effort-first run. **A2**: `governance/register-role-authority.md` v1.5.1 DPO row gains cross-reference to the charter's Article 38(3)(6) independence + conflict-of-interest framework. **B4**: `governance/register-canonical-citations.md` v1.5.0 scope extended to soft-law supervisory guidance; new "Soft-law supervisory guidance" section added with WP243 rev.01 (Article 29 Working Party Guidelines on DPOs, endorsed by EDPB May 2018) as first entry. **FR-47**: formally closed (surface-consolidated in PR #218; maintainer review now recorded).

### PR #235: Closes C2 convergent finding bundle (FR-121+122+123+124+125+126): emergency-access operational clarity (2026-06-22)

`security/procedure-access-control.md` v1.2.0: 6 fixes ship with maintainer-approved sample-data defaults + section-level "Sample data, adjust upon adoption" callout. FR-121 material-harm defined (P1/P2 incident threshold); FR-122 declared-incident tied to P1/P2 severity; FR-123 Delegated Security Lead role row added (sample data: senior IRT member or deputy CISO); FR-124 access-review revocation timeline contradiction resolved (24h window for revocation processing post-flag, distinct from immediate-upon-instruction case); FR-125 emergency-access revocation gains 30-min/30-min escalation chain (Identity Team → SOC L2 → CISO); FR-126 auto-escalation made explicit (ITSM SLA timer, no human trigger). PR-E in Batch 1.

### PR #234: Closes FR-67 (L, XS): zero-headcount-with-contractor sub-tier E0 in Dimension E (2026-06-22)

`docs/template-startup-roadmap.md` v2.2.0: new E0 sub-tier inserted before E1 in the Dimension E (GRC team capacity) ladder, covering the case where GRC function is entirely outsourced to a third-party contractor or fractional consultant. Adopter retains accountability; contractor executes. Same artefact subset as E1; operational difference is who holds the pen. PR-D in Batch 1.

### PR #233: Closes FR-89 + FR-91: security XS bundle (JWT algorithm-key-type binding + webhook signing precision) (2026-06-22)

`dev-security/standard-api-security.md` v0.0.5: Token validation row gains JWT algorithm-key-type binding requirement per RFC 8725 (prevents RSA-public-key-as-HMAC-secret confusion). Webhook signing row gains canonical-string definition + constant-time comparison requirement. Replay-prevention row gains explicit 5-minute replay window + seen-nonce cache. 2 L XS items closed. PR-C in Batch 1 effort-first run.

### PR #232: Closes FR-107 + FR-108 + FR-111: newcomer-UX bundle in adopter-guide (2026-06-22)

`docs/adopter-guide.md` v1.2.0: new "Two reference registers you will need early" subsection surfaces both the Glossary (acronyms + external-domain terms) and the Key Terms register (library-internal GRC concepts) BEFORE the How-the-library-is-meant-to-be-used section, explaining the split-by-term-class. Tier 1 starter set gains a "4-6 hours" reading-time estimate plus "if you only read three" pick (Charter + Framework + Role Authority Register). Closes 3 Low-severity XS items in one PR. PR-B in Batch 1 effort-first run.

### PR #231: Closes FR-112 (M) + FR-131 (FYI): adopter-facing maintainer-context cleanup (2026-06-22)

`README.md` line 58 audit-toolchain framing clarified (toolchain is maintainer's QA machinery, not an adopter dependency). `docs/template-quickstart.md` line 39 risk anchor switched from risk-register procedure to enterprise risk policy, aligning the quickstart core baseline with the adopter-guide Tier 1 starter set. Per-doc template-quickstart `3.0.0 → 3.0.1`. First PR in the effort-first batching run (Batch 1).

### PR #230: TODO reorganization (maintainer-directed): every item fits into P1-P7 priorities (2026-06-22)

Restructured `TODO.md` from 453 lines (mix of per-topic sections + dedicated fitness-review backlogs) to a priority-based layout: P1 Urgent quality (H[critical] + H, 14 items) / P2 Substantive improvements (M, ~30) / P3 Low-priority cleanup (L + FYI, ~16) / P4 Adopter experience (5 process/meta) / P5 Content expansion (8 country/regulator subsections) / P6 Domain-level (5 new-domain items) / P7 Awaiting maintainer decision. Fitness review backlogs from both 2026-06-21 r1 and 2026-06-22 r1 distributed by severity into matching priorities. "Investigation / blocked" promoted to P7. "Critical user feedback" renamed "Standing conventions" as meta-section. Item shape standardised: `**FR-N (severity, effort)**: description with location reference`. Also carries deferred PR #229 /validate-pr + /retro register rows.

### PR #229: /validate Sweep 20 iter 1 close-out: 3 glossary entries + cross-doc drift fix (2026-06-22)

Sweep 20 iter 1 (post PRs #220-#228) surfaced 4 in-window warnings + 2 maintainer-surfaced notes. Fixed: 3 new glossary entries (AEAD per RFC 8439 + NIST SP 800-38D; CIIO per Cybersecurity Law of China + PIPL Arts 38/40; HKDF per RFC 5869); cross-reference sentence added to `privacy/policy-privacy-and-data-governance.md:46` pointing at the charter's Article 38(6) framework. Pattern observed: 3 newly-introduced acronyms missed glossary entries in same batch; worker-brief candidate queued. Maintainer-surfaced: A2 (DPO row in role-authority register) and B4 (WP243/EDPB scope in canonical-citations register). Also carries deferred PR #228 /validate-pr + /retro register rows.

### PR #228: Closes FR-42 (medium, P2.1): DPO independence Article 38(3) + conflict-of-interest Article 38(6) framework (2026-06-22)

`privacy/charter-privacy-management-programme.md` previously had a one-line "Interim Accountability" note declaring the CIO assumes DPO responsibilities. Added subsection making the Article 38(6) conflict (CIO acting as DPO) visible rather than silent: Article 38(3) 3-row independence requirements; Article 38(6) WP243 conflict-of-interest list; explicit "known conflict" framing with 3 adopter paths (formal DPO designation, mitigation controls, exemption analysis); 5-row mitigation controls table; cross-regime equivalents (UK GDPR, LGPD Art 41, PIPL Art 52, India DPDP). Per-doc `1.4.0 → 1.5.0`. Also carries deferred PR #227 /validate-pr + /retro register rows.

### PR #227: Closes FR-40 (medium, P2.1): PIPL Articles 38-40 cross-border outbound mechanics operationalised (2026-06-22)

`privacy/procedure-privacy-impact-and-cross-border-transfer.md` previously had one line on PIPL cross-border. Expanded into 7-step workflow covering applicability + CIIO assessment, Article 38 mechanism selection (5-tier volume table with 2024 CAC Provisions safe harbors and thresholds), Article 39 separate consent, Article 40 CIIO domestic-storage default, PIA per Article 55, documentation/re-assessment cadence, and coordinated triggers across regimes. Per-doc `1.4.1 → 1.5.0`. Also carries deferred PR #226 /validate-pr + /retro register rows.

### PR #226: Closes FR-39 (medium, P2.1): EU representative Article 27 appointment process (2026-06-22)

`privacy/charter-privacy-management-programme.md` previously mentioned the EU representative only in passing. New subsection under Privacy accountability structure covering Article 3(2) trigger, Article 27(2) 4-criterion exemption, Article 27(3)(4) representative criteria, 7-step designation process, maintenance triggers, Article 27(5) liability clarification, and cross-regime equivalents (UK GDPR, LGPD, PIPL Art 53, India DPDP, Saudi PDPL). Per-doc `1.3.3 → 1.4.0`. Also carries deferred PR #225 /validate-pr + /retro register rows.

### PR #225: Closes FR-38 (medium, P2.1): GDPR Article 12(5) assessment checklist (2026-06-22)

`privacy/procedure-data-subject-rights-management.md` §7 expanded from one line on Article 12(5) into a 7-subsection checklist: default free of charge; 4-criterion manifestly-unfounded test; 4-criterion manifestly-excessive test; either/or action options (fee or refuse); 5-step burden-of-proof documentation; reasonable-fee cost-recovery calculation; cross-regime equivalents (UK GDPR, LGPD, PIPL, CPPA/PIPEDA, CCPA/CPRA, APPI). Per-doc `1.3.5 → 1.4.0`. Also carries deferred PR #224 /validate-pr + /retro register rows.

### PR #224: Closes FR-37 (medium, P2.1): Joint controller arrangement template (Article 26) (2026-06-22)

New template `privacy/template-joint-controller-arrangement.md` (v1.0.0) covering GDPR Article 26 joint controller arrangements with 9 sections (identification, joint processing, allocation of GDPR responsibilities table, operational coordination, liability, termination, cross-regime alternatives for UK GDPR / LGPD / PIPL / India DPDP / CPPA / CCPA, documentation, essence-of-arrangement publication). Cross-listed in privacy/README and document-index register. Also carries deferred PR #223 /validate-pr + /retro register rows.

### PR #223: Closes FR-49 (medium, P1.5): H2 label drift "Governance" → "Governance and accountability" (14 files, 2026-06-22)

14 files used bare `## Governance` H2; canonical form `## Governance and accountability` (20+ uses). Renamed via line-anchored regex (`^## Governance$`) so `## Governance Council` etc. were preserved. Per-doc Version patch-bumps; taxonomy/portal/maturity-scorecard regenerated. Also carries deferred PR #222 /validate-pr + /retro register rows.

### PR #222: Closes FR-82 (medium, P1.6): AI/model crypto "key hashing" ambiguity (2026-06-22)

`security/policy-encryption-and-key-management.md:56` "AI and Model Data" row's `"AES-256 + key hashing (SHA-512)"` conflated encryption, integrity, and key derivation; SHA-512 alone is NOT a KDF. Replaced with explicit per-purpose specification: AES-256-GCM (AEAD encryption with built-in integrity); HKDF-SHA-256 for key derivation from high-entropy material; Argon2id (or scrypt) for password-derived keys; explicit note that SHA-512 alone is a hash, not a KDF. Per-doc `1.3.1 → 1.3.2`. Also carries deferred PR #221 /validate-pr + /retro register rows.

### PR #221: Closes FR-33 (H[critical]): GDPR Article 36 prior-consultation pathway (2026-06-22)

Step 5 of `privacy/procedure-privacy-impact-and-cross-border-transfer.md` previously conflated internal ERC executive sign-off with the GDPR Article 36 regulatory prior-consultation pathway. Restructured into three substeps: 5.1 internal escalation (prior content), 5.2 NEW Article 36 prior consultation (trigger per Art 36(1), six-item content table per Art 36(3), 8+6 week timeline per Art 36(2), supervisory authority Art 58 corrective powers, 5-step interaction with internal pathway, non-EU equivalents to LGPD/PIPL/UK GDPR), 5.3 documentation requirements split by pathway. Per-doc `1.3.4 → 1.4.0`. Also carries deferred PR #220 /validate-pr + /retro register rows.

### PR #220: Sweep 19 iter 1 close-out + deferred PR #219 /validate-pr + /retro rows (2026-06-22)

/validate corpus-wide sweep on the post-PR-#219 state surfaced 2 in-window warnings in `governance/guideline-minimum-viable-governance-structure.md` (lines 67 and 114, stale "CPO" in executive-role enumerations missed by PR #218's spelled-out-only rename script). Both fixed; per-doc Version `1.0.1 → 1.0.2`. Pattern now at second occurrence (signal stage): "corpus-wide rename script: incomplete substitution coverage", queued worker-brief candidate strengthened. Carries PR #219 /validate-pr history row (0 findings) and /retro register row.

### PR #219: At-top "Role-name convention" notes in 24 privacy-relevant docs + PR #218 /validate-pr fixes (2026-06-22)

Follow-up to PR #218's DPO-canonical flip. Adds a blockquote callout note immediately after the metadata block (before the first H2 heading) in 24 privacy-relevant documents (privacy core 16, AI 3, supply-chain 3, security 1, governance 1) naming **Data Protection Officer (DPO)** as canonical, **Chief Privacy Officer (CPO)** as adopter substitution, and pointing to `governance/register-role-authority.md`. Bundles two PR #218 /validate-pr fixes per the recursion-avoidance rule: `tools/build-portal.py:95` "Data Protection Officer or Data Protection Officer" collapse fix (regen `docs/portal.md`); `risk/register-key-risk-indicators.md:142` stale "CPO" → "DPO" replacement. /validate-pr record + history row + /retro register row all carried in this PR. **No formal FR closed** (PR #218 closed FR-46/-47); this is the operational follow-through.

### PR #218: FR-46 DPO consolidation (medium): canonical flipped to Data Protection Officer (2026-06-22)

Reverses the CPO-canonical direction of PR #210 (Privacy Officer → Chief Privacy Officer rename) + PR #217 (closed unmerged when maintainer redirected). Maintainer-directed canonical: **Data Protection Officer**, globally-applicable, legislatively mandated in many regimes (GDPR Art 37, LGPD Art 41, India DPDP Act 2023 §10, Malaysia PDPA, etc.). Canonical surfaces flipped: register-role-authority CPO row → Data Protection Officer row with adopter-customisation note; glossary DPO entry extended; privacy/README Role terminology section added. Corpus prose rename across 73 files via one-shot Python script with synonym-pattern pre-cleanup; ~30 OWNER-FIELD metadata flips; build-portal.py + portal + maturity-scorecard + taxonomy regenerated. **PR-2 follows**: at-top "Role-name convention" notes in privacy-relevant docs.

### PR #214: Overnight-PR morning processing + PR #213 batched items (2026-06-22)

Morning-processing PR for the overnight session ending at PR #213: routed two design decisions (FR-104 and FR-130 explicit-drop closures) into `.working/design-decisions.md`, transitioned `.working/overnight-pr.md` back to stub form, and updated TODO and Next-up recommendations to reflect FR-119 / FR-14+FR-114 closures. Also carried the PR #213 batched items per the recursion-avoidance rule: stale forward-ref fix in `validation-sweep-pr-scoped/SKILL.md:175`, validate-pr history row for PR #213, improvement-log row for PR #213 with pattern observation #1 surfaced (new-skill drafting checklist candidate).

### FR-104 (medium): decision-tree per-regulation context not pursued (decided by maintainer, recorded PR #214, 2026-06-22)

Maintainer decided 2026-06-22 not to add per-regulation context to decision-tree §1.4. Rationale logged at [`.working/design-decisions.md`](design-decisions.md) § Decisions explicitly dropped.

### FR-130 (medium): decision-tree portal entry-point reorder not pursued (decided by maintainer, recorded PR #214, 2026-06-22)

Maintainer decided 2026-06-22 to keep README at decision-tree item 1; portal reorder not pursued. Rationale logged at [`.working/design-decisions.md`](design-decisions.md) § Decisions explicitly dropped.

### PR #213: Continuous process-improvement loop: /retro skill + improvement-log register (2026-06-22)

New pack skill `pr-retrospective` (slash command `/retro`) and the paired `.working/improvement-log.md` register. Post-merge retrospective on each successful PR; output is one entry per PR; recurring patterns surface as candidates for pack-rule updates / worker-brief additions / new audit gates. Wired into PR workflow step 5b in CLAUDE.md. Closes the three-layer learning loop (worker-brief template + apply-time catch tracking + PR retrospective). Pack `1.44.1 → 1.45.0`.

### PR #212: FR-14 + FR-114 (H[critical]): CMMI 5-tier maturity reconciliation (2026-06-22)

Maintainer-confirmed canonical: CMMI 5-tier (Initial/Managed/Defined/Quantitatively Managed/Optimized). Two surfaces aligned: template-maturity-self-assessment.md (Tier 2 Developing→Managed, Tier 4 Managed→Quantitatively Managed, Tier 5 Optimising→Optimized, all definitions extended with CMMI process-property language); register-digital-trust-and-assurance-metrics.md (DTI thresholds replaced from 4-tier variant with even 1.0-band 5-tier CMMI). Framework already canonical (no change). Closes the single largest cross-document issue in either fitness review.

### PR #211: FR-119 (medium): Risk Owner unification across ERM standard + exception policy (2026-06-22)

Maintainer-approved (decision 9): same role. ERM standard §3 Risk Owner extended from 5 to 6 accountability actions (added exception-request validation); §9.2 evidence table extended to 6 rows. Exception policy §2 cross-references the canonical ERM definition. **Convergent Finding C1 (Risk Owner role insufficiency) now fully closed** across FR-115/116/117/119.

### PR #210: FR-46 Privacy Officer rename (medium); DPO assessment surfaced (2026-06-22)

Maintainer-approved (decision 6): "Privacy Officer" not preceded by "Chief" → "Chief Privacy Officer" corpus-wide. 36 files modified, per-doc Version+Date patch bumped. DPO scope assessment: strong evidence that DPO and CPO are the same role (canonical register has only one entry, 8+ explicit equivalence statements, jurisdictions treat DPO as the privacy lead). DPO consolidation queued for separate maintainer go-ahead with named options A/B/C.

### PR #209: FR-52 (medium): Review-frequency "AND" form (2026-06-22)

Maintainer-approved (decision 5): canonical review-frequency form is "annually AND on material change" (both triggers required). Two corpus documents using OR form ("Annual or upon ...") converted to AND form.

### PR #208: FR-51 (medium): ISO 27001 Annex-form sweep: 12 files (2026-06-22)

Maintainer-approved (decision 4): canonical form is `Annex A.X` with prefix. Corpus-wide sweep converted `27001 A.X` → `27001 Annex A.X` across 7 corpus files + 5 pack SKILL.md files. Pattern tightly anchored on `27001` to avoid disturbing ISO 42001/27017/27018/27701 references. Multi-control `/`-separated lists got single Annex prefix per publisher convention.

### PR #207: FR-50 (medium): NIST citation format sweep: 50 files, 91 occurrences (2026-06-22)

Maintainer-approved (decision 3): canonical NIST citation format is `Rev. N` (with period, publisher convention). Corpus-wide sweep converted `Rev N` → `Rev. N` across 50 files (excluded: CHANGELOG historical entries and `.working/` archives). All 50 files received per-doc Version+Date patch bumps in the same commit. Template's "Rev. 4 → Rev. 5" example reworded to generic framing to avoid standards-currency gate false-positive on the illustrative-of-drift use case.

### PR #206: FR-87 + FR-88 (medium): SSRF range list + cipher suite enumeration (2026-06-22)

Maintainer-approved (decision 2). Pack core/owasp.md SSRF guidance updated with canonical IPv4 + IPv6 ranges + RFC citations (previously missed IPv6 entirely and used non-CIDR notation). Dev-security standard-api-security.md cipher row enumerated TLS 1.3 AEAD suites per NIST SP 800-52 Rev. 2 §3.3.1.

### PR #205: FR-81 fully closed (medium) + PR #204 /validate-pr fixes (2026-06-22)

Maintainer-approved: pack `dev-security/claude-rules/CLAUDE.md` TLS row aligned to canonical encryption-policy mandate (TLS 1.3+ with TLS 1.2 in Prohibited). Same shape as PR #193/#201. FR-81 fully closed (all 3 named surfaces). Also bundles 3 /validate-pr fixes from PR #204: stale count, in-flight self-correction prose in CHANGELOG, FR-114 double-counted.

### PR #204: Pass-1 verification of the 2026-06-22 fitness review (2026-06-22)

First Pass-1 verification in the project. r2 report file gains a new §9 (Pass-1 Verification Results) with verdict tags: 10 ✅ actively verified, 1 ⚠️ (FR-118 broader divergence than original framing), 0 ❌, 0 🤔, 9 ✅ batch-tagged for findings closed in overnight PRs, 3 maintainer-decided. FR-124 severity flagged for escalation Medium → High (12-month risk window). Pass-2 (maintainer-interactive bucket processing) is next.

### PR #203: FR-133 (FYI): Jurisdiction-index pointer prominence (2026-06-22)

Closes FR-133 by restructuring `docs/decision-tree.md` §4.1: the jurisdiction-index pointer is now a stand-alone lead paragraph noting the full 25-jurisdiction coverage; common Anglosphere selections are framed as "representative, not exhaustive"; a closing sentence names example non-Anglosphere annexes (Australia, Singapore, India, Brazil, Japan, South Korea, China) with redirect to the jurisdiction index. Also bundles PR #202's out-of-window TODO drift cleanup (C1/C2/C3 next-up narrative rotated to reflect overnight closures).

### PR #202: Overnight session wrap-up (2026-06-22)

Final overnight-batch PR. Updates `.working/overnight-pr.md` with the 9-PR build-progress list (PRs #193-#201, closing FR-127/128/129/113/115/116/117/132 fully + FR-81 partial), the files-modified inventory, the files-NOT-touched inventory, and the 9-item open-ambiguities list for maintainer morning review. Status remains `in-flight`; the morning-processing PR will transition to `stub` after routing content.

### PR #201: FR-81 partial (medium): TLS 1.3+ alignment in dev-security standards (2026-06-22)

Two of three FR-81 surfaces aligned to the canonical encryption policy's TLS 1.3+ mandate: `dev-security/standard-developer-security-requirements.md`:151 and `dev-security/standard-api-security.md`:109. Pack `dev-security/claude-rules/CLAUDE.md` surface deferred (pack-rule edit; approval-needed). Same canonical-source pattern as PR #193's FR-127 ZTA framework alignment.

### PR #200: FR-132 (low): Decision-tree glossary-order annotation (2026-06-22)

Closes FR-132 by annotating `docs/decision-tree.md` §2.1 Orientation list: items 1-2 (README, adopter-guide) get inline notes that acronyms are expanded at first occurrence per FR-4 / FR-106 / FR-113 polish; item 3 (glossary) gets a note about its scope (reserved for deeper-domain docs). Adopts the recommendation's option (b) "note recent improvements" rather than option (a) "move glossary to item 1" (the existing entry-point pattern is preserved).

### PR #199: FR-117 (medium): Risk Owner evidence by accountability action (2026-06-22)

Closes FR-117 by adding a new §9.2 to the ERM standard mapping each of the five Risk Owner accountability actions (per §3) to the evidence type from §9.1 that proves execution. Mechanical mapping using existing canonical sources; no new policy. C1 Convergent Finding 3 of 4 closed (FR-115/116/117); FR-119 deferred (needs decision).

### PR #198: FR-116 (medium): Risk Owner monitoring cadence by score band (2026-06-22)

Closes FR-116 by extending ERM standard §8.1 with explicit Risk Owner review cadences per score band (Low/annual, Moderate/quarterly, High/monthly, Critical/monthly), aligning to the §5.2 scoring-threshold table's review-interval column. Mechanical alignment, no new policy. Partial C1 close (after PR #197's FR-115).

### PR #197: FR-115 (high): Risk Owner row in Role Authority Register (2026-06-22)

Closes FR-115 by adding the Risk Owner row to the canonical Role Authority Register, mirroring the verbatim Primary Accountability text from the ERM standard §3 (added in PR #178) and adding a reciprocal cross-reference. Partial close of Convergent Finding C1; FR-116/FR-117 still doable, FR-119 deferred (needs decision).

### PR #196: FR-113 (medium): CAPA + SIEM acronym expansion in README (2026-06-22)

Closes FR-113 by expanding `CAPA` and `SIEM` acronyms at first occurrence in `README.md`'s Repository Structure block, restoring the acronym-expansion pattern established in PRs #172 and #179. Also bundles the mechanical cleanup of fitness-reviews backlog-table rotation for FR-127/128/129 (pre-existing discipline gap surfaced by PR #195's /validate-pr).

### PR #195: FR-129 (H[critical]): Internal audit reports retention 5y → 7y (2026-06-22)

Closes FR-129 by raising internal audit reports retention in `governance/register-data-retention-schedule.md` from 5y to 7y, aligning with the internal-audit standard §8.3 canonical 7-year mandate. With PR #194's FR-128 closure, the C3 Convergent Finding (audit-evidence chain breaks) is fully resolved.

### PR #194: FR-128 (H[critical]): CAPA retention 5y → 7y (2026-06-22)

Closes FR-128 by raising CAPA records retention in `governance/register-data-retention-schedule.md` from 5y to 7y, aligning with the CAPA procedure's §12 canonical 7-year mandate and closing the audit-evidence chain break with control-testing-evidence retention. Also fixes PR #193's /validate-pr finding (stale FR-127 entry in TODO's "Next-up recommendations" section) per the batching rule.

### PR #193: FR-127 (H[critical]): TLS 1.2 → TLS 1.3 in ZTA framework (2026-06-22)

Closes FR-127 by aligning the ZTA framework's Pillar 3 transport-encryption maturity row with the canonical encryption policy's TLS 1.3+ mandate. First overnight-batch PR; carries PR #192's /validate-pr history row.

### PR #192: Codify batching-into-next-PR rule for /validate-pr and /validate (2026-06-22)

New "Batching into the next PR (recursion-avoidance)" sub-section in both /validate and /validate-pr SKILL.md surfaces + slash commands: /validate-pr outputs (zero-finding history rows AND findings-producing fixes) bundle into the next PR whatever its purpose, eliminating dedicated hot-fix and housekeeping PRs. /validate retains an optional dedicated close-out PR for numerous or coherent corpus-wide findings. Carries PR #191's deferred /validate-pr history row as the rule's first application. Closes the day's cascade loop.

### PR #191: Record /validate-pr for PR #190 (0 findings; cascade terminated) (2026-06-22)

`.working/` changes for local project: appended the history row recording the zero-finding /validate-pr run against PR #190. Four-PR cascade (#187 → #188 → #189 → #190 = 2+2+2+0 findings) terminated by PR #190's structural fix (full-date Originating run column + UTC convention + chat-surfacing discipline).

### PR #190: Hot-fix /validate-pr findings on PR #189 + UTC convention + chat-surfacing discipline (2026-06-22)

Three bundled threads: hot-fix the two multi-surface incompleteness findings from /validate-pr on PR #189 (the r2→r1 relabel missed `.working/fitness-reviews/history.md` line 22 narrative + the H[critical] backlog table's "Originating run" column; resolved structurally by switching cross-date column to full dates); codified the UTC convention in CLAUDE.md (assistant works in UTC for all date-bearing fields); codified the chat-surfacing discipline in /validate and /validate-pr SKILL.md + slash commands (findings surface in chat with per-finding shape, not buried in .working/ files). Third consecutive findings-producing /validate-pr.

### PR #189: Hot-fix /validate-pr findings on PR #188 (2026-06-22)

Two in-window findings from /validate-pr on PR #188 fixed: the fitness-review file's internal "r2" labels and history.md row corrected to "r1" per the per-date `rN` convention (8 internal references plus the history row); pack README's 1.40.1 row catch-attribution reworded from "gate 31 caught it" to credit /validate-pr deep-read (gate 31 didn't actually fire due to a timezone-boundary edge case). Recorded /validate-pr on PR #188 history row plus per-PR detail file. Second consecutive findings-producing /validate-pr (the discipline is converging).

### PR #188: Close-out: /validate-pr fixes on #187 + record /fitness r2 (2026-06-22)

End-of-evening close-out bundling three independent threads: two hot-fixes for PR #187's `/validate-pr` findings (slash-command "no skip" wording harmonized to match SKILL.md verbatim; pack README Date bumped 2026-06-21→2026-06-22 with Version 1.40.0→1.40.1 patch); committing the /fitness r2 report (27 findings across 10 personas; 22 new FR IDs FR-112 through FR-133; three Convergent Findings dominate; zero regressions from the day's PRs); and the /validate-pr history record for PR #187 itself.

### PR #187: Codify no-orchestrator-skip-discretion discipline + fix paired-skill docstring (2026-06-22)

Hot-fix after maintainer flagged that the orchestrator skipping /validate-pr on PRs #185/#186 was a real policy deviation. Three surfaces gain explicit "no skip" language (SKILL, slash command, pack-rule anti-patterns); paired-skill linter docstring updated; new failure-mode class C-9 captured in hallucination-metrics with a future-gate candidate for mechanical enforcement.

### PR #186: Sweep 17 iter 1 close-out: SKILL forward-reference + gate 44 PAIRS registry (2026-06-21)

Sweep 17 (second full sweep of the day). Two in-window findings closed: validation-sweep-pr-scoped SKILL.md:151 stale "/retro queued for PR #185" → "PR #186"; gate 44 PAIRS registry extended with the new validation-sweep-pr-scoped + /validate-pr pair (was a real defect, gate not validating new skill).

### PR #185: Record first /validate-pr invocation (PR #184, 0 findings) (2026-06-21)

`.working/` changes for local project: appended the history row recording the first real `/validate-pr` invocation (run post-merge on PR #184; 0 findings; full Subagent A coverage). Housekeeping PR; no corpus content changes. Re-numbers tomorrow's planned PRs: /retro becomes #186, FR-33 becomes #187.

### PR #184: Worker-brief template + hallucination-assessment update protocol (2026-06-21)

New project-local worker-brief template at `.working/worker-brief-template.md` plus pack-rule update codifying the self-improving loop: when an apply-time catch occurs, log it, classify the fix, update the template inline. Initial template ships with four guard rails from the four known apply-time-catch classes.

### PR #183: Add /validate-pr skill + slash command for post-merge per-PR validation (2026-06-21)

New pack skill and slash command for PR-scoped post-merge validation; runs after every merge to catch per-PR drift before it compounds. Complements the existing corpus-wide /validate sweep (every 10 merges).

### PR #182: Corpus-wide count-genericization sweep (2026-06-21)

Applied PR #181's count-genericization principle corpus-wide. Found one additional candidate (`specification-audit-programme.md:64` "seven functional categories" → generic); negative findings (ten persona reviewers, five disciplines, external CCM/FedRAMP counts) documented per assessment criterion.

### PR #181: Sweep 16 iter 1 close-out: TODO narrative refresh + skill-authoring genericization (2026-06-21)

Sweep 16 close-out (first full sweep since Sweep 15 at PR #167; 13-PR window). Two in-window findings closed: TODO.md:22 PR-range narrative refreshed to current state; skill-authoring-discipline SKILL.md:26 "seven governance rules" rewritten as generic phrasing per maintainer's count-genericization direction.

### PR #180: Extend version-bump discipline to four surfaces (add per-document Date) (2026-06-21)

Closed the discipline gap surfaced by PR #179's gate-31 catch: the apply-time checklist now pairs Version-bump with Date-bump on every body-changing commit. Pack rule and project CLAUDE.md updated; pack version 1.36.0 → 1.37.0.

### PR #179: FR-18 + FR-25 + FR-79 + FR-105 + FR-106 + FR-110 (all medium): P1.4a small singletons bundle (2026-06-21)

Six medium-tier singleton findings closed in one PR: exception 180-day baseline anchored to a library convention, control-testing evidence retention raised 5y→7y, tabletop template Slack→generic, ISMS NIST CSF name normalised, README trade-programme acronyms expanded, decision-tree document-index reframed. FR-33 (high[critical]) split out to P1.4b per "always split when in doubt".

### PR #178: FR-11 (medium) + FR-12 (medium): ERM standard Risk Owner role definition + within-document treatment vocabulary harmonisation (2026-06-21)

§3 governance table gains a Risk Owner role definition; treatment vocabulary harmonised within the ERM standard (Treat→Mitigate, Exploit/Enhance row-split, Treatment Option enum extension). Cross-document harmonisation against procedure-risk-register deferred.

### PR #177: Rotate Phase 1 / Phase 2 execution plan into TODO (2026-06-21)

Moved the multi-PR Phase 1 + Phase 2 execution plan out of session memory into TODO's Queued-sequence section so it survives session-end; identifies the `/fitness` pause point at end of Phase 2.

### PR #176: Document five memory-only AI-assistant workflow disciplines as a new pack rule + hallucination-metrics tracking file (2026-06-21)

New pack rule `ai-assistant-workflow-disciplines.md` covers research-assistant discipline, pipeline PR construction, apply-time worker correction, "always split when in doubt", and background work during CI waits; `.working/hallucination-metrics.md` ships as the project's tracking artefact for the catch / escape ratio.

### PR #175: Shorten historical DONE entries to scrolling-battle-text convention (2026-06-21)

Retroactively shortened every existing DONE entry to the 1-2-sentence, no-links, no-version-bumps shape adopted in PR #174.

### PR #174: Retire CHANGELOG skip trailer; adopt terse-entry convention; reshape DONE as scrolling battle-text (2026-06-21)

Replaced the `Changelog: skip` opt-out in the change-tracking pack rule with a terse-entry convention (every PR carries an entry, even if a one-liner); reshaped the DONE-ledger guidance to 1-2 sentences, no links, at-a-glance index rather than CHANGELOG duplicate.

### PR #173: CHANGELOG backfill for PRs #170 and #171 (2026-06-21)

Backfilled the missing CHANGELOG entries for the two `.claude/`-only PRs that shipped under the (then-active) skip-trailer exemption, repairing the visible #169 → #172 jump in the audit trail.

### PR #172: FR-4 (medium) + FR-5 (medium) + FR-6 (medium) + FR-7 (medium) + FR-8 (medium, ⚠️): README polish bundle (2026-06-21)

Five medium README polish findings closed in one PR: acronym expansion, doc count pointer, CalVer placement, audience-signal panel, version-line demote.

### PR #171: CLAUDE.md PR-activity-subscription + 60s-timer discipline (2026-06-21)

Added the discipline that every `mcp__github__subscribe_pr_activity` call arms a paired 60-second fallback timer, since subscriptions reliably deliver failure events but not all success transitions.

### PR #170: CLAUDE.md three-surface version-bump discipline (2026-06-21)

Codified the three-sentence version-bump rule (per-doc per body-change commit; library CalVer once per PR in the last commit; README Version paired with CalVer) after PR #169's gate 40 catch.

### PR #169: FR-26 (medium) + FR-27 (medium) + FR-28 (medium): access-control procedure decision-path gaps (2026-06-21)

Three medium-tier access-control polish findings closed: escalation ladder added to the 3-day approval SLA, vague "appropriate" replaced with four bounded review criteria, and emergency verbal approval gained trigger conditions plus a revocation consequence.

### PR #168: Sweep 15 follow-up: BASC information security 5-level classification expansion (2026-06-21)

Expanded the BASC logistics policy from 3 classification levels to the canonical 5 (Public, Controlled, Internal, Confidential, Restricted) to align with the rest of the corpus.

### PR #167: Sweep 15 iter 1 close-out: roadmap metadata + DPIA ISO/IEC citation + TODO narrative refresh (2026-06-21)

Three in-window fixes: roadmap Review Frequency metadata stale after FR-57 rename; DPIA template's ISO/IEC 29134:2023 citation corrected to 2017; TODO narrative refresh.

### PR #166: FR-57 (high): rename long quickstart to startup-roadmap; ship new 10-minute quickstart (2026-06-21)

Renamed the 319-line composition workbook to `template-startup-roadmap.md` and shipped a true 10-minute quickstart as the new `template-quickstart.md`; portal updated to surface both with distinct questions.

### PR #165: FR-56 (high): adopter entry-point reconciliation: portal declared canonical front door (2026-06-21)

Declared `docs/portal.md` the canonical adopter entry point; four other adopter-facing documents gained a "Where this fits among the adopter entry points" preface naming the portal as canonical.

### PR #164: FR-43 (high[critical]): data-classification 5-level scheme propagated library-wide (2026-06-21)

Propagated the canonical 5-level classification scheme (Public / Controlled / Internal / Confidential / Restricted) into six subordinate documents that previously enumerated only four levels.

### PR #163: DONE format harmonisation with TODO: surface FR-N and severity at heading level (2026-06-21)

Retrofitted 22 DONE H3 headings to surface `FR-N (severity)` at the heading level, matching TODO's tier-grouped bullet format for at-a-glance symmetry.

### PR #162: FR-29 (high[critical]): Data Protection Impact Assessment template with Article 35 trigger / EDPB WP248 / Article 35(7) content checklists (2026-06-21)

Shipped a new DPIA template covering GDPR Article 35's three limbs (trigger checklist, EDPB WP248 nine-criteria framework, Article 35(7) content checklist).

### PR #161: FR-17 (high): reconcile exception-approval authority between policy and Role Authority Register (2026-06-21)

Reconciled the exception policy's §2.2 approval pathway with the Role Authority Register's "Approve exception" RACI row, replacing a stub placeholder with the tiered pathway and adding a reciprocal cross-reference.

### PR #160: Sweep 14 iter 1 close-out: FR-44-self-violations + TODO queued-sequence refresh (2026-06-21)

Sweep 14 close-out: fixed three FR-44 self-violations in the master spec and exception policy (legacy "shall" / "may not" → "must" / "must not"), plus a stale TODO queued-sequence narrative.

### PR #159: FR-44 (high): requirement-language convention documented in master spec (2026-06-21)

Documented the library's requirement-language convention in the master spec: "must" / "must not" canonical; "should" / "should not" for recommendations; "may" for permission; "shall" reserved for external-standard quotation.

### PR #158: FR-80 (high[critical]): SIEM / cloud-activity-log retention reconciliation (2026-06-21)

Reconciled the apparent contradiction between the 3-year SIEM-events retention and the 90-day cloud-activity-log retention by reframing the 90-day figure as the platform-side forwarding floor; the SIEM remains the authoritative retention authority.

### PR #157: FR-16 (high[critical]): exception register hard caps + renewal-ceiling escalation pathway (2026-06-21)

Strengthened the exception policy with two new required schema fields (`max_duration` 540 days default, `renewal_count_limit` 3 default), a hard 180-day initial cap, and a 1-2-3 renewal-ceiling escalation (ERC at 2nd, Board at 3rd, prohibition at 4th).

### PR #156: FR-2 (high): README "How to use" step 1 leads with the audience-keyed portal (2026-06-21)

Reordered the README's "How to use" step 1 so the audience-keyed portal is the primary pointer; the 300-row document index becomes the secondary pointer for readers who already know what they want.

### PR #155: FR-1 (high): README reframing (corpus is the headline, AI-maintenance is the methodology) (2026-06-21)

Reframed the README so the GRC documentation corpus is the unambiguous headline product; the audit toolchain and the dev-security pack are positioned as the operational layer used to maintain corpus consistency.

### PR #154: Sweep 13 iter 1 close-out: FR-45 + FR-92 generalisations (2026-06-21)

Sweep 13 close-out: three FR-45-class "may not" → "must not" fixes in AI standards; one FR-92-class addition of Escalation Owner + Remediation Sign-off columns to the BASC IT KPIs table; one metadata document-history backfill.

### PR #153: FR-92 (high): KPI Escalation Owner + Remediation Sign-off columns (2026-06-21)

Added Escalation Owner + Remediation Sign-off columns to every KPI table in the IT operations register; roles drawn from the Role Authority Register, with ERC as the escalation target when the KPI's Owner is already CIO or CISO.

### PR #152: FR-19 (high[critical]) + FR-20 (high): CAPA governance ceiling + root-cause quality checklist (2026-06-21)

CAPA procedure gains a 1-2-3 extension-ceiling (ERC at 2nd, Board Risk Committee at 3rd, prohibition at 4th) and a five-criterion root-cause quality checklist (Specific / Causal / Actionable / Bounded / Evidence-anchored).

### PR #151: FR-35 (high): explicit GDPR Article 33(2) processor-awareness clock (2026-06-21)

Made the GDPR Article 33(2) two-clock asymmetry explicit in the privacy breach-response procedure: the 24-hour processor-to-controller window starts at processor awareness; the 72-hour Article 33(1) controller clock runs from controller awareness.

### PR #150: FR-45 (high): RFC 2119 "may not" → "must not be" in two security standards (2026-06-21)

Replaced "may not" with "must not be" in two security standards where the intent was a prohibition rather than a permissible-negative-possibility per strict RFC 2119 reading.

### PR #149: FR-21 (high[critical]): Compliance-obligations Source Reference granularity (2026-06-21)

Tightened the compliance-obligations Source Reference field so register citations resolve to a single unambiguous source location, with minimum-precision patterns per source type (NIST, ISO, statutes, COBIT, PCI DSS, CSA CCM, contracts, voluntary commitments).

### FR-21 (high[critical]): Compliance-obligations Source Reference granularity (closed by PR #149, 2026-06-21)

Template previously accepted low-precision citations like "NIST 800-53" without revision or control number; closure tightened the field to require resolvable source locations.

### PR #148: Sweep 12 iter 1 close-out (2026-06-21)

Sweep 12 close-out: three in-window findings fixed (cross-doc stale CIO-as-ERM-accountable, missing sampling-justification cross-reference, missing reciprocal risk-acceptance link).

### PR #147: FR-3 (high): README "New to GRC?" introductory block (2026-06-21)

Added a "New to GRC? Start here" §2 to the README expanding the acronym, defining Governance / Risk / Compliance in plain language, and signposting five role/intent-keyed next steps.

### PR #146: FR-96 (high): Risk-acceptance procedure cross-reference to exception register (2026-06-21)

Added a `Related exception register entry` field to the risk-acceptance procedure's required record fields so the exception and risk-acceptance registers are cross-traversable for auditors.

### PR #145: FR-95 (high): Risk register compensating-controls field (2026-06-21)

Added a `Compensating Controls` field to the risk register Acceptance section so the acceptance record is self-contained and auditable.

### PR #144: FR-22 (high): Audit-evidence sampling-justification field (2026-06-21)

Added a mandatory `Sampling justification` field to the audit-evidence template's per-control operating-evidence section, capturing population, sample size, selection method, and confidence-level assumption.

### PR #143: FR-9 (high[critical]) + FR-10 (high): Chief Risk Officer in enterprise risk management standard (2026-06-21)

Changed the ERM standard's Owner from CIO to CRO and added a CRO row to §3 Governance scoped to risk strategy, risk appetite stewardship, and ERM-programme outcomes reporting.

### FR-10 (high): Chief Risk Officer in ERM §3 governance table (closed by PR #143, 2026-06-21)

ERM §3 governance table omitted CRO despite CRO being a defined role; closed alongside FR-9.

### FR-9 (high[critical]): Enterprise risk management Owner: CIO → CRO (closed by PR #143, 2026-06-21)

ERM-standard Owner field changed from "Chief Information Officer" to "Chief Risk Officer"; enterprise risk is a CRO accountability in most operating models.

### PR #142: Fitness quick wins: FR-13 (medium) + FR-54 (low) + FR-55 (low) + FR-103 (low) (2026-06-21)

First fitness-remediation PR. Four single-file unambiguous findings closed at maintainer direction as quick wins while the rest of the backlog was under review.

### FR-103 (low): Add Chief Compliance Officer row to framework-continuous-assurance governance table (closed by PR #142, 2026-06-21)

Continuous Assurance framework's governance table omitted CCO despite CCO being relevant to compliance-domain assurance closure; CCO row added.

### FR-55 (low): Document `roadmap-` doctype prefix (closed by PR #142, 2026-06-21)

Closed alongside FR-54 by adding an explicit prefix-to-doctype mapping table to the master spec listing all 17 doctypes and their canonical filename prefixes.

### FR-54 (low): Document `sop-` doctype prefix (closed by PR #142, 2026-06-21)

Same prefix-mapping table as FR-55, also covering `sop-`.

### FR-13 (medium): Disambiguate `CPPA` in enterprise risk management standard (closed by PR #142, 2026-06-21)

`CPPA` in the framework alignment table expanded to "Canadian Consumer Privacy Protection Act, Bill C-27" to disambiguate from the California Privacy Protection Agency.

### PR #141: Fitness backlog Pass-2: maintainer-interactive triage; structured TODO backlog (2026-06-21)

Pass-2 triage of the 111 fitness findings: ✅ batch accepted (Low deferred to later cleanup); ⚠️ batch accepted with modifications; FR-14 + FR-110 resolved to ✅; FR-43 + FR-53 reshaped. Structured backlog added to TODO.

### PR #140: Fitness backlog Pass-1: orchestrator verification of all 111 FR-N findings (2026-06-21)

Pass-1 verification of the 111 FR-N findings via five parallel subagents: 93 ✅ confirmed-as-stated, 14 ⚠️ confirmed-with-modification, 2 🤔 ambiguous, 2 ❌ rejected.

### PR #139: Fitness skill amendment: unverified→confirmed labelling discipline (2026-06-21)

Amended the library-fitness-review skill to introduce per-finding Pass-1 (orchestrator verification) and Pass-2 (maintainer-interactive triage) before any finding lands in the remediation backlog.

### PR #138: Shipped Priority 4 items rotation (2026-06-21)

Rotated five completed Priority-4 TODO items (P4.1-P4.5) into DONE as their own cross-reference entries; P4.6 remains forward-looking.

### TODO P4.1: Quickstart templates per adopter profile (shipped 2026-06-20)

Shipped as `docs/template-quickstart.md` v2.0.0: core baseline plus five stacking dimensions with about twenty modules and three worked examples (the v1.0.0 fixed-profile shape was rejected as too rigid).

### TODO P4.2: Maturity assessment interactive template (shipped 2026-06-20)

Shipped as `docs/template-maturity-self-assessment.md`: guided checklist across 11 library domains on a 5-tier maturity ladder with per-tier next-step guidance.

### TODO P4.3: Implementation roadmap templates (shipped 2026-06-20)

Shipped as `docs/template-implementation-roadmap.md`: three-phase (Floor / Operational / Year-1 close) sequence at 90 / 180 / 365 days, with pace adjustments for E1/E3/E4 capacity tiers.

### TODO P4.4: Regulator interaction templates (shipped 2026-06-20)

Shipped as `compliance/template-regulator-interaction.md`: five sub-templates (breach notification, attestation submission, examination support, periodic report, regulatory inquiry response) in one consolidated document.

### TODO P4.5: Audit evidence package templates (shipped 2026-06-20)

Shipped as `compliance/template-audit-evidence-package.md`: cover page, control inventory, per-control sections with framework references and evidence, per-domain summaries, package-level sign-off.

### PR #137: Overnight-work protocol: stub format for `overnight-pr.md` + audit gate 46 + pack rule amendment (2026-06-21)

Implemented the overnight-work protocol: stub-form `overnight-pr.md` with three-state `Status` field, new audit gate 46 that fails on `Status: done`, and a pack-rule subsection documenting the lifecycle.

### PR #135: Restructure design-decisions into its own file; clean up `overnight-pr.md` (2026-06-21)

Created `design-decisions.md` as the new home for design-decision content; rotated misplaced sections out of DONE and TODO; deleted the procedural-detail `overnight-pr.md` content from the prior session.

### PR #134: Gate 45 false-positive fix: tighten queued-PR regex (2026-06-21)

Tightened gate 45's regex so the queued-PR marker must be the immediately-following PR reference, not any PR reference within 80 characters; fix for a false positive on `main` post-PR-#133 merge.

### PR #133: Document the project's Canadian-first language convention (2026-06-21)

Documented the project's language convention as "Canadian English first, Commonwealth second, other dialects last"; Canadian-shared-with-Oxford `-ize` orthography is the linter behaviour, not an American mandate.

### PR #132: Add Ryk Edelstein to `AUTHORS.md` (2026-06-21)

Single-line addition to AUTHORS.md's Acknowledged contributors list; first PR using the post-PR-#131 steady-state of TODO/DONE rotation in the same PR.

### PR #131: DONE.md infrastructure + TODO refactored to forward-looking only (2026-06-21)

Bootstrap PR for this file: introduced `.working/DONE.md` as the closed-TODO ledger; rotated "PRs completed this session" and "design decisions made this session" content out of TODO; added the PR finalization protocol section to the change-tracking pack rule.

### PR #130: Remove decorative gate-count narrations (2026-06-21)

Replaced 11 `"the N-gate audit programme"` prose references across 7 files with `"the audit programme"`; the spec §6 inventory remains the canonical source for the gate list and current count.

### PR #129: PR #128 catch-up: TODO drift caught by gate 45 on post-merge `main` (2026-06-21)

Gate 45's first production catch: post-merge `push`-event CI on `main` flagged TODO still framing PR #128 as "Next" after its merge; TODO rotated and the gate validated as the intended drift-detection mechanism.

### PR #128: Gate 45 (TODO staleness audit) + PR-time-checks wrapper (2026-06-21)

New gate 45 catches the two TODO drift shapes (queued PR already merged; sweep cursor behind history); bundled with `run-pr-time-checks.sh` so every gate the CI workflow runs has a local invocation path before push.

### PR #127: Sweep 11 iter 1 close-out (2026-06-21)

Sweep 11 close-out: eight in-window findings including a corpus-wide count-mismatch correction (111/17/20/57/17 across six surfaces); reframed TODO's session-pause snapshot as "as-of-last-refresh".

### PR #126: `.working/README.md` Activities table row for `changelog-details/` (2026-06-21)

Single-row addition to `.working/README.md`'s Activities table for the `changelog-details/` activity that was introduced in PR #125 but missed in that PR's README update.

### PR #125: CHANGELOG two-file split: root keeps lead paragraphs, detailed mirror keeps full structured entries (2026-06-21)

Split CHANGELOG into a two-file convention: root carries lead-paragraph summaries (adopter-facing), detailed mirror at `.working/changelog-details/CHANGELOG-detailed.md` carries full structured-section entries (maintainer-grade). 2926 → 675 lines in root.

### PR #124: First-ever fitness review (run r1, ten persona subagents) (2026-06-21)

First invocation of the library-fitness-review skill: ten persona subagents dispatched in parallel, producing 111 unique findings (FR-1 through FR-111) that became the fitness-remediation backlog.

### PR #123: Sweep 10 iter 3 close-out (2026-06-21)

Sweep 10 iter 3 close-out: one in-window Medium finding actioned (TODO version-snapshot drift); convergence narrowing from iter 2's 7 findings to 1.

### PR #122: TODO cleanup: removed completed Steps A/C/D/E from queued sequence (2026-06-21)

Pure TODO maintenance: removed completed steps from the queued sequence section and renumbered the next step; no library content change.

### PR #121: Sweep 10 iter 2 close-out: post-overnight-sequence cleanup (2026-06-21)

Sweep 10 iter 2 close-out: seven in-window findings actioned post the three-PR overnight sequence (PRs #118-#120), including preflight exemption refresh, TODO snapshot refresh, and CHANGELOG narration correction.

### PR #120: `/fitness` skill (`library-fitness-review`) (2026-06-21)

Added the `/fitness` slash command and the library-fitness-review skill: whole-corpus library-quality review dispatching ten persona reviewers in parallel; authored end-to-end during an overnight session under explicit maintainer authorisation.

### PR #119: TODO update only (session-resume context capture) (2026-06-21)

Session-resume context capture in TODO; no library content change.

### PR #118: Restructure `.working/<activity>/` to canonical layout (2026-06-21)

Restructured `.working/validate-sweeps/` to the canonical `<activity>/{README, history, detail-files}` layout that becomes the standard for any `.working/<activity>/` subdirectory.

### PR #117: Sweep 10 iter 1 close-out: six prose-drift findings post-PRs-#114-#116 (2026-06-21)

Sweep 10 iter 1 close-out: six prose-drift findings from the three-PR `.working/` sequence (stale step counts, stale subdir inventory, section-header drift, "Four rules" → "Six rules" updates).

### PR #116: Move validation-sweep history file from `governance/` to `.working/` (2026-06-21)

Moved the validation-sweep history file from `governance/` to `.working/` since validation-sweep history is project-specific application of the discipline, not template content for adopters.

### PR #115: `/validate` slash command rename + per-iteration record convention (2026-06-21)

Renamed the `/validation-sweep` slash command to `/validate` for short ergonomic verbs; added the per-iteration record convention (detail files only when findings exist; history-table row for every iteration).

### PR #114: `.working/` top-level convention infrastructure (2026-06-21)

Established the `.working/` top-level convention for maintainer working state; created `.working/README.md` and added `.working/` to the linters' default exempt directories.

### PR #113: Sweep 9 iter 3 close-out: three documentation findings from Subagent A's deep-review of PR #112 (2026-06-21)

Sweep 9 iter 3 close-out: three documentation findings from Subagent A's deep review of PR #112; convergence narrowing from iter 2.

### PR #112: 7th governance rule (`validate-inference-before-action.md`) + gate 39 pattern P7 (2026-06-21)

Added the seventh pack rule, `validate-inference-before-action.md`: when the next action depends on an inferred premise, validate the premise via tool call before acting. Action-side counterpart of the evidence-grounded-completion rule.

### PR #111: Sweep 9 closure: Subagent C findings + Rule 5.6 (subagent-dispatch declaration discipline) (2026-06-21)

Sweep 9 closure: actioned Subagent C findings; added Rule 5.6 to the validation-sweep skill requiring every iteration to declare which subagents were dispatched in the history register's `Subagents` column.

### PR #110: Corpus stale gate-count fixes + gate 39 pattern P6 (2026-06-21)

Corpus-wide stale gate-count reference fixes (the cascade-class issue PR #130 later addressed at the source by removing decorative gate-count narrations); gate 39 pattern P6 added.
