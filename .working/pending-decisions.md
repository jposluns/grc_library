# Pending Decisions

**Status:** 0 pending (the 4 domain-wide PRI-* mapping picks below were confirmed by the maintainer on 2026-06-28; all four applied defaults retained, no changes)

This file is the durable queue for the **attended-autonomous operating mode** (see the
`## Attended-autonomous operating mode` section in [`.claude/CLAUDE.md`](../.claude/CLAUDE.md)):
when the assistant surfaces a decision that is genuinely the maintainer's and no answer
arrives (here, because the `AskUserQuestion` primitive errored repeatedly this session, a
transient permission-stream failure), it records the decision here and continues, rather
than stalling.

On `/resume`, the assistant reads this file first, surfaces the still-`pending` entries to
the maintainer, resolves those tasks, and only then continues to the next queued items.

## Entries

### 2026-06-28: domain-wide privacy PRI-* to CCM v4.1 mapping (4 judgement-call rows; proceeded with recommended defaults)

PR #428 corrected 7 invalid `PRI-*` CCM citations across 3 privacy files (surfaced as the #427 `/validate-pr` out-of-window finding; `PRI-*` is CCM v3.x, no PRI domain in v4.1). Three were unambiguous and applied directly (PRI-04 to DSP-11, breach PRI-05 to SEF-08, PIA-row PRI-05 to DSP-09). The other four are genuine semantic-mapping choices; they were surfaced to the maintainer with named options and recommendations, the ~2-minute graceful-degradation timer fired with no answer, so the recommended evidence-backed defaults were applied (reversible on-branch; `/matrix-fit` is the backstop). **Confirm or redirect each:**

- `policy-privacy-and-data-governance.md:144` PRI-01 "Governance and accountability" to **GRC-06** "Governance Responsibility Model" (alternatives: GRC-01, or DSP-01 but already used at line 146).
- `policy-...:145` PRI-02 "Lawful processing and consent" to **DSP-12** "Limitation of Purpose in Personal Data Processing" (approximate fit: CCM v4.1 has no dedicated consent / lawful-basis control).
- `policy-...:147` PRI-03 "Cross-border data transfers" to **DSP-10** "Sensitive Data Transfer" (could co-cite DSP-19 "Data Location").
- `charter-privacy-management-programme.md:218` the range "PRI-01 through PRI-07" to **Option A: "Data Security and Privacy Lifecycle Management (DSP) domain"** (framework-level reference matching the table's whole-framework granularity; alternatives B "DSP-01 through DSP-19" valid range, C an enumerated control list). A literal positional PRI-to-DSP renumber was rejected as fabricated.
- **Status**: resolved. Maintainer confirmed all four applied defaults on 2026-06-28 (GRC-06 for PRI-01, DSP-12 for PRI-02, DSP-10 for PRI-03, and the DSP-domain reference for the charter range); no changes. Rotates out at the next handoff per the resolved-entry convention.

No other pending decisions.

The 2026-06-26 §5.3 register-classification decision was resolved by the maintainer
(Option A: `register-coverage-gaps.md` stays corpus; `register-document-review-schedule.md`
migrates to `.project-governance/`) and **applied in PR #381** (the Phase-2 migration). It is
rotated out of this queue at the #382 handoff per the resolved-entry convention. The audit
trail lives in the separation spec §5.3/§5.4, the #381 CHANGELOG entry, and
[`DONE.md`](DONE.md).
- **Status**: resolved (Option A); review-schedule migration queued.
