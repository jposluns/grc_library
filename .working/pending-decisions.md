# Pending Decisions

**Status:** 1 pending (the §4.10 gate-design disposition below: proceeded-with-defer on the graceful-degradation default, confirm or redirect on resume). The ATLAS decision is fully resolved (parent: "Act on atlas"; scratch sub-question: the maintainer directed defer-the-scratch-half on 2026-06-28, "scratch is now being worked on by another session"). The 4 PRI-* picks were confirmed. The resolved entries rotate out at the next handoff.

This file is the durable queue for the **attended-autonomous operating mode** (see the
`## Attended-autonomous operating mode` section in [`.claude/CLAUDE.md`](../.claude/CLAUDE.md)):
when the assistant surfaces a decision that is genuinely the maintainer's and no answer
arrives (here, because the `AskUserQuestion` primitive errored repeatedly this session, a
transient permission-stream failure), it records the decision here and continues, rather
than stalling.

On `/resume`, the assistant reads this file first, surfaces the still-`pending` entries to
the maintainer, resolves those tasks, and only then continues to the next queued items.

## Entries

### 2026-06-28: TODO §4.10 (TODO/DONE rotation gate) design disposition (proceeded-with-defer; confirm on resume)

The maintainer queued §4.10 as PR #7 of the next-10 and selected the **id-cross-check** shape (flag any FR/DD/P-id that is both an open TODO backlog-item subject and a closed item in a `DONE.md` heading). Building it, the shape was validated against the current clean `main` and produced **4/4 false positives**: FR-167 (multi-part item, shipped sub-batches but legitimately open), FR-44 (same FR tag covers a shipped convention statement and an open derivative sweep), FR-104 / FR-130 ("not pursued" dropped decisions recorded in both DONE and TODO Priority 7). The FR-44 / FR-167 cases are not separable by id-matching without semantic understanding, confirming the change-tracking rule's "this is brittle" verdict. The fallback decision (defer vs the FP-free "marked-done detector" Option B vs build-A-with-exemptions) was surfaced to the maintainer; the `AskUserQuestion` primitive errored (transient permission-stream failure) and the ~2-minute graceful-degradation timer fired with no answer.

- **Status: proceeded-with-defer (conservative default).** §4.10 is deferred (the convention + close-out checklist remain the guard, as the change-tracking rule prescribes); the design note is recorded inline in TODO §4.10. **Confirm or redirect on resume:** defer further, OR build the FP-free Option B (marked-done detector), OR build Option A with a documented exemption set. Reversible (no gate shipped); no corpus change.
### 2026-06-28: MITRE ATLAS scratch version update (pending; needs a maintainer download / egress)

Validating reference currency upstream this turn (the new `## Reference-version currency` SOP), the scratch `ref/frameworks/MITRE/` base holds **ATLAS v5.6.0** (`catalogue.yml`; `ATLAS.yaml` `version: 5.6.0`, header self-declares the line deprecated), while the upstream authority (atlas-data releases) is now **v2026.05** (2026-05-27, format v6.0.0). So scratch ATLAS is superseded. (ATT&CK is current: scratch v19.1 = upstream v19.1.) Per the version-update SOP, updating scratch needs a download (egress-gated, DD-10) and an MCP PR (proxy-403), so the decision was surfaced to the maintainer:

- **(a)** maintainer provides / authorizes the v2026.05 download to scratch now; or
- **(b)** defer the ATLAS currency item (the scratch update + the grc_library `register-canonical-citations.md:169` row, kept coherent) until directed.

**Status: resolved (a), with one narrow sub-question still pending.** The maintainer directed **"Act on atlas"** on 2026-06-28, selecting path (a) (authorize the v2026.05 download / scratch update). Acted on:

- **grc_library register half (done, this PR):** [`register-canonical-citations.md`](../governance/register-canonical-citations.md):168-169 bumped to the upstream-confirmed current versions, **ATT&CK v15 -> v19.1** (2026-05, superseded `v15`) and **ATLAS v4.7 -> v2026.05** (2026-05, superseded `v4.7`). Both re-verified upstream this turn (atlas-data releases `v2026.05` 2026-05-27; attack-stix-data `v19.1` 2026-05-12). Per the maintainer's `## 4.26` note, the superseded **v5.6.0** is NOT written anywhere (it is the deprecated old-scheme line, not a citable version). Corpus sweep for explicit `v15`/`v4.7` MITRE citations: zero in audited scope (corpus docs cite version-less "MITRE ATLAS"/"MITRE ATT&CK"). Register stays the version AUTHORITY; the scratch base is believed-current STORAGE that may lag, per the SOP.
- **grc_library_scratch re-ingest half (authorized; one sub-question surfaced):** the download is authorized, but ATLAS v2026.05 ships a NEW data format (YAML format v6.0.0), and scratch holds no MITRE distill script that produces the existing per-sheet CSV extracts. Reproducing those extracts from the new format risks putting fabricated/wrong data in the reference base (a material downside). The narrow sub-question surfaced to the maintainer: **store the upstream v2026.05 YAML (+ excel assets) as-is and archive v5.6.0 to `ref/.deprecated/MITRE/ATLAS-v5.6.0/`** (recommended; lossless, no fabrication), vs **also reproduce new-format CSV extracts** (needs a new distill script first). On no answer, the SOP default is the recommended store-as-is reconciliation (reversible; the CSVs can be regenerated later when a distill script exists). The scratch write goes via MCP PR (proxy-403 on direct push).
- **Resolved 2026-06-28:** the maintainer directed **defer the scratch half** ("scratch is now being worked on by another session"). This session does NOT do the scratch re-ingest; the grc_library register half is already correct and authoritative (the register leads, scratch storage lags, per the SOP). No further action here; the other session owns the scratch update.

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
