# Library Fitness Review History

**Version:** 1.3.3\
**Date:** 2026-06-27\
**License:** CC BY-SA 4.0

Reverse-chronological table of every `/fitness` invocation against this library. New rows on top. Each row is a summary; detail for findings-producing runs lives in the per-run file linked from the **Detail** column.

See [`README.md`](README.md) for the persona catalogue, severity model, output format spec, dispatch declaration discipline, audit-gate exemption notes, and adopter guidance.

## Fitness review runs

| Date | Run | Personas | Findings | Resulting PR | Detail | Summary |
|---|---|---|---|---|---|---|
| 2026-06-27 | r1 | A, B, C, D, E, F, G, H, I, J (all 10) | 32 routed as FR-168 to FR-199 (8 H -> P1, 7 M + 17 L/FYI -> P2); 2 deduped to existing ERC + FR-44-generalisation items | pending (session-closing handoff; remediation deferred to fresh resume) | [`2026-06-27-r1.md`](2026-06-27-r1.md) | Trust-recovery `/fitness` (paired with `/full-qa` deep-qa-review iter 2, run first). Ten personas, whole corpus, maintainer mental model stripped. Cleanest High finding is the GRC-12 citation fix: the policy-exception document cites "CCM v4.1 GRC-12" x8, but GRC-12 is not a CCM v4.1 control (family stops at GRC-08); correct control is GRC-04. The rest of the High set is cross-document value contradictions: risk-scoring divergence (standard vs methodology likelihood basis + the 5x5-matrix pointer), High-residual acceptance-authority conflict (CRO vs Executive Management vs Executive Committee/Board), incident P2 CISO-timing conflict (4h vs 1h vs 2h, including intra-document), ROPA retention (3y vs the schedule's Active+5y), and the India DPDPA in-force conflict (April 2025 vs notified 13 Nov 2025 phased to 2026-2027). The corpus passed all 54 mechanical gates, so this whole set is the gate-blind class; it paired with the `/full-qa` iter-2 forensic pass, which was clean except FR-198 (matrix DSP-10 weak fit) and FR-199 (register soft-law column format). Trust-recovery routing: every confirmed finding tiered by severity to P1/P2, nothing dropped; maintainer signed off this session. |
| 2026-06-22 | r2 | A, B, C, D, E, F, G, H, I, J (all 10) | 27 routed (6 H[critical], 6 H, 9 M, 6 L/FYI) as FR-134 to FR-160; 2 deduped to existing FR-30 / FR-44-generalisation | pending (trust-recovery sign-off) | [`2026-06-22-r2.md`](2026-06-22-r2.md) | Trust-recovery `/fitness` (paired with `/full-qa` deep-qa-review iter 1). Ten personas, whole corpus, maintainer mental model stripped. Six convergent multi-surface contradictions dominate, four H[critical]: risk-scoring divergence (standard vs methodology bands/labels/likelihood, P3+P7), TLS 1.2-vs-1.3 floor contradiction (encryption-policy/dev-req mandate 1.3, quick-ref/baseline permit 1.2, P2+P7), retention conflicts (logging 7y vs schedule/records 1-3y; DSAR 3y vs 2y, P4), CPPA-cited-as-in-force (DSR/breach/policy vs Canada annex, P9); plus DR RPO-vs-backup-gap self-contradiction (P7) and adopter starter-set divergence 6/15/23/37 (P1+P8). All 6 H[critical] + cited High re-verified at source by orchestrator; Medium/Low rest on persona quotes pending re-read. Mechanical baseline green on unshallowed clone (shallow-clone artifact caught by /full-qa). Trust-recovery routing: every confirmed finding to TODO P1 top tagged [fitness:persona]; maintainer triages at sign-off. Zero regressions from the #218-#242 window. |
| 2026-06-22 | r1 | A, B, C, D, E, F, G, H, I, J (all 10) | 27 (6 H[critical], 8 H, 11 M, 2 L/FYI; P5 Policy Editor and P9 Privacy/DPO both returned 0 findings, clean bills on editorial layer and privacy domain). **Pass-1 complete in PR #204**: 19 ✅ (10 actively verified + 9 batch-tagged for closed), 1 ⚠️ (FR-118 broader divergence than original framing), 0 ❌, 0 🤔, 3 maintainer-decided. FR-124 flagged for severity escalation Medium → High. | [#188](https://github.com/jposluns/grc_library/pull/188) | [`2026-06-22-r1.md`](2026-06-22-r1.md) | End-of-evening sweep validating the effectiveness of the day's 6 FR-remediation PRs (#169 access-control polish, #172 README polish bundle, #178 ERM Risk Owner completion, #179 P1.4a small-singletons bundle, plus meta-PRs #176 / #180 / #181 / #182 / #183 / #184 / #185 / #186 / #187). Aggregate: all 14 closed FRs materially addressed their cited symptoms; the corpus is meaningfully better than the 2026-06-21 baseline from every persona's lens. **0 regressions** from the day's PRs. The 27 new findings are NEW issues revealed by fixes or pre-existing issues the 2026-06-21 review missed. Three Convergent Findings dominate: **C1 Risk Owner role insufficiency** (P3+P6+P7, FR-115/116/117/119; the role was added to ERM standard §3 in PR #178 but did not propagate to Role Authority Register, Risk Owner evidence expectations, monitoring cadence for non-Critical, or the exception policy's different "Risk Owner" definition); **C2 Emergency-access trigger ambiguity** (P2+P6+P7, FR-121/122/123/125/126; PR #169 added trigger conditions but "material harm", "declared incident response", "delegated security lead" lack operational definitions); **C3 Retention chain breaks** (P4, FR-128/129; PR #179's 5y→7y bump on control-testing evidence didn't propagate to adjacent CAPA and internal audit report retentions). Plus single-persona findings: FR-127 TLS 1.2 in ZTA vs TLS 1.3 in encryption policy (H[critical], P2); FR-114 DTI tier vocabulary vs framework CMMI (H[critical], P1, related to the 2026-06-21 review's FR-14); FR-130-133 adopter sequencing/discoverability (P8, mostly L/FYI). New FR IDs FR-112 through FR-133 (22 IDs covering 27 findings). All findings `verification: unverified` pending Pass-1 verification in next session. Pass-1 deferred to tomorrow morning per maintainer direction. |
| 2026-06-21 | r1 | A, B, C, D, E, F, G, H, I, J (all 10) | 111 (17 H[critical], 20 H, 57 M, 17 L; counts corrected from PR #124's "95/18/22/31/24" approximation in Sweep 11 iter 1) | [#124](https://github.com/jposluns/grc_library/pull/124) | [`2026-06-21-r1.md`](2026-06-21-r1.md) | First-ever fitness review. Library broadly fit for use; key clusters: maturity ladder fragmentation (3 conflicting models), data classification 4-vs-5-level split, DPO operational templates missing (DPIA/DPA/LIA/TIA/PbD), audit-discipline ceilings absent (exception/CAPA/citation-precision), README onboarding hole (GRC never expanded), 4 entry-point sequences contradict, healthcare/HIPAA + FS-outside-EU/US coverage shallow, SIEM/cloud-log retention contradiction (3y vs 90d). Strong areas: AI/agentic security (exemplar), threat modelling, OT/ICS, post-quantum, supply chain SCA/SBOM, DSAR/breach workflows. Recommendation: not publication-ready; Q1 close of audit-exposure cluster (Rec-2/3/4/5) brings library to publication-grade. |

## Open remediation backlog items

Discrete remediation IDs (`FR-1`, `FR-2`, ...) generated by fitness reviews that have not yet been actioned. Each row tracks the originating review, the work item, and current status. See per-run detail files for full work-item specifications.

For the 2026-06-21 run, the full FR-1 through FR-111 backlog is enumerated in [`2026-06-21-r1.md`](2026-06-21-r1.md) §3 Page-by-Page Findings. For the 2026-06-22 run, the full FR-112 through FR-133 backlog is enumerated in [`2026-06-22-r1.md`](2026-06-22-r1.md) §8 Remediation Backlog. The high[critical] subset across both runs is summarised below; remaining items are tracked in the detail files.

| ID | Originating run | Title | Severity | Status | Assigned PR |
|---|---|---|---|---|---|
| FR-9 | 2026-06-21 | ERM standard owned by CIO (category error; should be CRO or Board) | high[critical] | pending | none |
| FR-14 | 2026-06-21 | Maturity ladder fragmentation (3 conflicting models) | high[critical] | pending | none |
| FR-16 | 2026-06-21 | Exception register lacks max-duration / renewal-count fields | high[critical] | pending | none |
| FR-19 | 2026-06-21 | CAPA target-date extensions lack governance ceiling | high[critical] | pending | none |
| FR-21 | 2026-06-21 | Compliance Obligations Register accepts low-precision regulatory citations | high[critical] | pending | none |
| FR-29 | 2026-06-21 | DPIA methodology and trigger checklist absent | high[critical] | pending | none |
| FR-30 | 2026-06-21 | Article 28 DPA template missing | high[critical] | pending | none |
| FR-31 | 2026-06-21 | Privacy by Design (Art 25) no operational artefact | high[critical] | pending | none |
| FR-32 | 2026-06-21 | LIA template missing | high[critical] | pending | none |
| FR-33 | 2026-06-21 | Article 36 prior-consultation pathway absent | high[critical] | pending | none |
| FR-34 | 2026-06-21 | TIA methodology referenced 3+ places, defined nowhere | high[critical] | pending | none |
| FR-43 | 2026-06-21 | Data classification 4-level vs 5-level split across foundational docs | high[critical] | pending | none |
| FR-70 | 2026-06-21 | Crypto-asset / blockchain governance missing | high[critical] | pending | none |
| FR-71 | 2026-06-21 | M&A due diligence superficial | high[critical] | pending | none |
| FR-72 | 2026-06-21 | Sanctions / OFAC / export control screening superficial | high[critical] | pending | none |
| FR-73 | 2026-06-21 | AI ethics review process superficial | high[critical] | pending | none |
| FR-80 | 2026-06-21 | SIEM/cloud-activity-log retention contradiction (3y vs 90d) | high[critical] | pending | none |
| FR-114 | 2026-06-22 | DTI tier vocabulary vs framework CMMI (4-tier vs 5-tier; closely related to the 2026-06-21 run's FR-14) | high[critical] | pending | none |
| FR-121 | 2026-06-22 | Emergency-access "material business or safety harm" undefined | high[critical] | pending | none |
| FR-122 | 2026-06-22 | "Declared incident response" trigger not tied to specific incident status | high[critical] | pending | none |
| FR-127 | 2026-06-22 | TLS 1.2 in ZTA framework vs TLS 1.3 in encryption policy | high[critical] | closed | [#193](https://github.com/jposluns/grc_library/pull/193) |
| FR-128 | 2026-06-22 | CAPA retention 5y vs control-testing 7y (audit-evidence chain break) | high[critical] | closed | [#194](https://github.com/jposluns/grc_library/pull/194) |
| FR-129 | 2026-06-22 | Internal audit reports retention 5y vs procedures' 7y (audit-evidence chain break) | high[critical] | closed | [#195](https://github.com/jposluns/grc_library/pull/195) |

(High and Medium and Low items from both runs: 93 additional items, tracked in detail files; not enumerated here to keep this table scannable.)

## Discipline observations

*(Notes about pattern-level observations across multiple fitness reviews accumulate here. Populated as runs surface recurring themes.)*
