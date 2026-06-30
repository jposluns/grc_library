# Pending Decisions

**Status:** 0 pending. §4.6 (QA-cadence mechanical enforcement) was RESOLVED 2026-06-29 by the maintainer ("close 4.6 as satisfied", in chat after `AskUserQuestion` flaked a 3rd time): close §4.6 as substantially-satisfied by gate 50 Check 1 (which already enforces the missing-row half corpus-wide); the abbreviated-marker residual stays the CLAUDE.md "Throughput pressure does not authorise QA abbreviation" convention. See the §4.6 entry below. The S3 design fork (TODO §4.5; surfaced 2026-06-29) was RESOLVED 2026-06-29 by the maintainer (defer/park S3 pending a clearer design, since gates 48/49/54 already cover control-code existence corpus-wide; move to §4.6 / §4.8 next). The earlier 2026-06-29 decisions are RESOLVED by the maintainer: the §4.10/§4.6 gate-family (build Option B marked-done PLUS the complementary CHANGELOG-asserts-closure check; the marked-done half shipped as gate 57 in #468, the complementary check shipped as the D5 PR-time check in #469) and the `docs/` house-style (Option A then refined to "full house-style now": extend the gate-2 language audit to `docs/` and fix all 117 findings; shipped in #470). See the resolved entries below. The S2 role-drift decision (2026-06-29) was RESOLVED by the maintainer (the "migrate allow-list to register" reframe), shipped as PR #463 (since merged). The four overnight-clarification questions were answered by the maintainer 2026-06-28 via screenshot; recorded below as RESOLVED standing directives. **Two resume-session decisions resolved 2026-06-29 (maintainer screenshot):** operating model = **full project PR workflow** (per-PR feature branch, open + self-merge green PRs via GitHub MCP, attended-autonomous), overriding the wrong harness-config "single-branch / no-PR" text (the maintainer confirmed the harness config was wrong; no cleanup needed since no work was committed under it); next focus = **guard-rail gates + codifications**. Recorded here for durability across compaction.

This file is the durable queue for the **attended-autonomous operating mode** (see the
`## Attended-autonomous operating mode` section in [`.claude/CLAUDE.md`](../.claude/CLAUDE.md)):
when the assistant surfaces a decision that is genuinely the maintainer's and no answer
arrives (for example because the `AskUserQuestion` primitive errors, a transient
permission-stream failure), it records the decision here and continues, rather than
stalling.

On `/resume`, the assistant reads this file first, surfaces the still-`pending` entries to
the maintainer, resolves those tasks, and only then continues to the next queued items.

## Pending (open; surface at next attended boundary / `/resume`)

_None open. The 2026-06-29 and 2026-06-30 entries below are RESOLVED (retained for the audit trail)._

## Resolved overnight directives (maintainer-answered 2026-06-30, `/resume` into overnight mode; standing for this run)

The `/resume` put the session into **overnight mode** (maintainer asleep; a mid-night prompt does NOT exit overnight mode; anything needing maintainer input is deferred). Three authorial decisions were surfaced up front (via `AskUserQuestion`, then confirmed by maintainer screenshot, both agreeing) so items would not defer:

1. **Net-new authority = self-merge green + harness.** Author AND self-merge green P1/P2 net-new content PRs; run the high-assurance adversarial-verification harness (independent false-negative + false-positive verifiers, deterministic apply, re-parse) on EACH net-new standalone document BEFORE merge; record each in [`high-assurance/register.md`](high-assurance/register.md). (Same as the prior run's directive 1, re-confirmed for this run.)
2. **Missing sources = attempt download, then defer.** Deepen ref-covered jurisdictions now; for each primary source the scratch `ref/` base lacks (APAC privacy beyond Japan; non-EU/US financial regulators for FR-61), attempt to download the primary-source legislation into scratch via the MCP-PR ingestion workflow (egress permitting per DD-10); defer only the truly-unavailable, recording it.
3. **ERC tier-table reconcile (TODO P3) = collapse dup; drop Tier-2 stray.** In [`governance/guideline-minimum-viable-governance-structure.md`](../governance/guideline-minimum-viable-governance-structure.md): Tier-1 delete the duplicate "Executive Risk Committee" row (line 58), keep "Enterprise Risk Committee" (line 59); Tier-2 remove "Executive Risk Committee" from the Executive Committee combined-forums list (line 80), since the risk committee is its own Tier-2 body (line 81). Treats both residuals as drift/duplication. Closes the ERC residual P3 item.

**Overall directive (maintainer `/resume` args):** work Priority 1, 2, and 3 items to reduce the list as much as possible overnight; **fix-issues-first, new-content-second**; correct any errors discovered; continue (do not wind down) absent evidence of hallucination/drift.

### §4.6 QA-cadence mechanical enforcement: close as satisfied (surfaced 2026-06-29; RESOLVED 2026-06-29, maintainer chose close-as-satisfied)

Scoping §4.6 (a candidate gate that "compares the post-merge history files against the merged-PR list and fails when a PR's row is missing or marked abbreviated") surfaced that its mechanically-valuable core, the **missing-row half**, is **already shipped as gate 50 Check 1** ([`tools/lint-bookkeeping-parity.py`](../tools/lint-bookkeeping-parity.py):27-48, "Check 1, QA-cadence parity (the §4.6 surface)"): it derives the merged-PR list from CHANGELOG headers, requires a [`validate-pr/history.md`](validate-pr/history.md) row + (for substantive PRs) an [`improvement-log.md`](improvement-log.md) row per in-window PR, and handles the handoff / subsumption exemptions and `KNOWN_HANDOFF_NO_ROW`. The §4.6 design questions (where the gate lives, the handoff exemption, mirroring the rotation family) are all already answered by gate 50. The only residual, the **abbreviated-marker half** (detecting a row that exists but is a sham, the literal Sweep 22 "abbreviated spot-check, 0 findings" failure), is **not FP-free-mechanizable** on the free-prose Findings/Summary cells (an honest abbreviation-admission has no unambiguous shape, unlike the strikethrough / uppercase-`SHIPPED` markers the family's precision-first discipline relies on); building it would violate the gate-48/gate-50 FP-free discipline, and an FP-prone gate gets worked around (the `gate-discipline` concern). This is the same shape as the S3 item (parked) and the S2/#463 resolution (the "new gate" was redundant with existing gate 8). Surfaced via `AskUserQuestion` (flaked, 3rd time this session). **RESOLVED 2026-06-29 (maintainer, in chat): "close 4.6 as satisfied"** (Option A, recommended): §4.6 closes as substantially-satisfied by gate 50 Check 1; the abbreviated-marker residual stays the existing CLAUDE.md "Throughput pressure does not authorise QA abbreviation" convention (no new gate, no schema change). §4.6 deleted from TODO and rotated to DONE in the closing PR.

### §4.5 S3 citation-precision-for-claim gate: design fork (surfaced 2026-06-29; RESOLVED 2026-06-29, maintainer chose defer/park)

Scoping the S3 "citation-precision-for-claim" gate surfaced that it is **not mechanizable as a corpus gate**: the corpus holds no external-standard source text to check a claim's precision against (the source text lives in the separate `grc_library_scratch` `ref/` base, unreachable from CI). Three options were surfaced (the `AskUserQuestion` primitive flaked, so the fork was held): (A) a narrower mechanical gate (existence/format only, reusing the gate 48/49/54 validators); (B) a cadenced `/matrix-fit`-style skill using the scratch `ref/` source text (not a CI gate); (C) defer S3 and move to §4.6 / §4.8. **RESOLVED 2026-06-29 (maintainer, by screenshot): defer/park S3** ("Defer S3; move to §4.6 / §4.8 next. Park S3 pending a clearer design (gates 48/49/54 already cover control-code existence corpus-wide, so S3's marginal mechanical value is unclear). Proceed to the §4.6 QA-cadence gate or the §4.8 apply-time-discipline codifications, which have no feasibility fork."). S3 stays in TODO §4.5 marked parked-pending-design; the next work is §4.6 or §4.8.

### §4.10 / §4.6 bookkeeping-parity gate-family design + sequencing (surfaced 2026-06-29, post-#466/#467; RESOLVED 2026-06-29)

**RESOLVED 2026-06-29 (maintainer):** "build Option B, add the complementary CHANGELOG-asserts-closure check." Both checks are to be built. The **marked-done detector** shipped as **gate 57** in **#468** (scoped to the three FP-free structural markers, strikethrough / `[done]` / `Status: completed`; the bare-`SHIPPED` facet was dropped because it false-positives on open multi-part items like FR-167's "column SHIPPED in PR-B", per the maintainer's "long-term best solution" directive, and the complementary check covers that case instead). The **complementary CHANGELOG-asserts-closure PR-time check** (a PR whose added CHANGELOG asserts it closes a TODO item must touch both [`TODO.md`](../TODO.md) and [`.working/DONE.md`](DONE.md), with the handoff-PR exemption) **shipped as the D5 PR-time delta check** ([`tools/check-todo-rotation-on-pr.py`](../tools/check-todo-rotation-on-pr.py), wired into [`tools/run-pr-time-checks.sh`](../tools/run-pr-time-checks.sh) and the `quality.yml` pull_request section), which closes §4.10. With both halves shipped, §4.10 is fully closed. Sequencing thereafter: the `docs/` dash extension (Option A, next), then §4.5 S3, then §4.8 codifications (deliberately, not at a long-turn tail), then §4.4 / §4.3.

### §4.10 / §4.6 superseded pending note (the original open framing, retained)

The #466 `/retro` surfaced a coverage gap in the maintainer-decided §4.10 design. §4.10 was DECIDED 2026-06-28 as **Option B, the "marked-done detector"** (flag a TODO item that marks ITSELF done via `~~` / `[done]` / `SHIPPED`). But #466's actual failure (the omitted §4.5 S4 rotation, fixed in #467) was a **wholesale-forgotten** rotation: TODO.md was never edited, so there was nothing self-marked for Option B to detect. **Option B would not have caught #466.** A complementary check would: a PR whose CHANGELOG asserts it closes a TODO item (regex on "closing TODO §X" / "closes TODO §X") must touch BOTH [`TODO.md`](../TODO.md) and [`.working/DONE.md`](DONE.md) in the same diff. **Surfaced to the maintainer** (chat, post-#467) with the coverage-gap note plus the next-5 sequencing question. **Decision needed:** (1) build Option B as decided, (2) build the complementary CHANGELOG-closure-claim check instead/additionally, or (3) some other shape; AND confirm the sequencing among §4.10/§4.6 (gate family), §4.5 S3, §4.8 codifications, §4.4, §4.3. **Authorial / not auto-defaulted** (building the wrong gate wastes real effort and gives false confidence); the gate build is deferred-blocked pending steer. Route-around considered: §4.8 codification is independent of this decision, BUT §4.8's own TODO entry says "action deliberately, not at a long-turn tail", so it was NOT auto-started on the 2026-06-29 graceful-degradation timeout; the assistant idled for maintainer steer instead (no degradation signal, so not a wind-down handoff). On `/resume`: resolve this gate-family decision and the sequencing, then proceed.

### `docs/` dash house-style decision (Sweep-76 Finding 2, surfaced 2026-06-29; RESOLVED 2026-06-29)

**RESOLVED 2026-06-29 (maintainer): Option A, then refined to "full house-style now"** ("always go with the long term best solution for the project rather than a one time fix"): extend the language gate to cover `docs/` (close the gate-blind path-scope gap permanently) AND fix the violations. On implementation (PR #470), bringing `docs/` under the actual gate surfaced **117 findings, not the 71 dashes the original framing assumed** (71 dashes + 25 `-ise` + 14 heading-case + 5 sanitisation + 2 ensure); the scope fork was surfaced and the maintainer chose **"full house-style now"** (the full gate, not a dash-only check). **SHIPPED in PR #470**: gate 2 scan extended to `docs/` (generated artefacts excluded, the worked-example meta-tutorial exempted from the three checks it demonstrates), all 117 findings fixed. The original options are retained below for the audit trail.

Sweep 76 found `docs/` authored prose carries 71 em/en-dashes across 4 files ([`docs/decision-tree.md`](../docs/decision-tree.md) 58, [`docs/adopter-guide.md`](../docs/adopter-guide.md) 5, [`docs/template-quickstart.md`](../docs/template-quickstart.md) 4, [`docs/template-implementation-roadmap.md`](../docs/template-implementation-roadmap.md) 4), violating the CLAUDE.md house-style but outside [`tools/lint-language.py`](../tools/lint-language.py)'s path scope. Surfaced to the maintainer with named options; the `AskUserQuestion` primitive is flaky this session, so it is recorded here per the attended-autonomous defer path and tracked in TODO P3. **Options put to the maintainer** (recommended first): (A) extend the dash check to `docs/` and fix all 71 (closes the gate-blind gap permanently); (B) document `docs/` as an intentional house-style carve-out (no fix); (C) one-time fix the 71 without extending the gate. Out-of-window / pre-existing; reversible / on-branch when actioned. **Not auto-defaulted** (it is a gate-scope authorial decision); held for the maintainer. Does not block other queued work.

### S2 role-drift resolution (2026-06-29; RESOLVED 2026-06-29, maintainer chose the allow-list to register reframe)

Building the **S2 role-definition-consistency gate** (TODO §4.5) with the low-FP design (check the `Owner:` / `Approving Authority:` metadata fields and RACI-table roles against [`governance/register-role-authority.md`](../governance/register-role-authority.md)) surfaced **5 roles used as document Owners/Approvers but absent from the register's 35 canonical roles**:

- **GRC Programme Manager** (Owner on ~7 docs)
- **Compliance Maintainer**, **Information Security Maintainer**, **Security Architecture Maintainer** (Owners; siblings of register rows like *AI Security Maintainer*, *Supplier Risk Maintainer*, *Control Framework Maintainer*, which ARE registered)
- **Governance Library Maintainer** (the register's own Owner/Approving Authority; a library-meta role)

These are pre-existing FR-115-class role drift. The gate cannot ship green until they are resolved, and the resolution is **authorial** (defining governance accountabilities for the 4 substantive roles, and deciding whether the library-meta role belongs in an org-role register), which "Proceed" (build S2 with the low-FP design) did not delegate. The `AskUserQuestion` primitive errored (permission-stream flake) when surfacing this, so it is recorded here per the attended-autonomous defer-and-skip path.

**Options put to the maintainer** (recommended first): (A) I draft register rows for the 4 substantive roles by mirroring their sibling rows' accountability pattern, for maintainer review, and handle Governance Library Maintainer as a library-meta row or a documented scope-exclusion, then build the gate; (B) scope-exclude all 5 as library-internal/meta roles via a documented allow-list and build the gate now; (C) defer S2 and build S3/S4 next.

**RESOLVED 2026-06-29 (maintainer choice, superseding the earlier defer-and-skip).** On resuming the build, the orchestrator discovered that gate 8 (`lint-roles.py`, "Owner and Approving Authority role audit", wired across all four parity surfaces) ALREADY validates every `Owner` / `Approving Authority` value against the register, and the 5 "missing" roles above were exactly its `EXTRA_KNOWN_ROLES` allow-list entries. The originally-scoped "new S2 gate" was therefore redundant with gate 8. The orchestrator surfaced this with named options; the maintainer chose **"migrate allow-list to register"** (confirmed by screenshot of the `AskUserQuestion` selection plus "Add rows and draft"): add the 5 roles as register rows so the register is the single source of truth, empty the linter allow-list, no new gate, no gate-count change. Shipped as **PR #463**, which is **held for maintainer review of the drafted accountability prose** (the prose is semantically authorial; gate 8 stays green regardless of its wording, so the maintainer can revise it freely before merge). RACI-cell checking was deliberately excluded (descriptive composites, high-FP, against the low-FP directive). S2 is closed in TODO §4.5.

## Resolved overnight directives (maintainer-answered 2026-06-28; standing instructions for the overnight run)

The `AskUserQuestion` primitive errored twice (permission-stream closed); the maintainer
answered all four in plain text (screenshot). These are now standing directives the overnight
session follows directly. No longer pending.

1. **Overnight merge authority = FULL AUTONOMY, with mandatory adversarial verification on
   net-new.** The orchestrator authors and self-merges green PRs for ALL P1/P2 content,
   including net-new standalone documents, WITHOUT holding for morning review. **The one
   condition: run the new high-assurance adversarial-verification harness (the
   [`high-assurance-verification`](../dev-security/claude-rules/governance/high-assurance-verification.md)
   process, independent false-negative + false-positive verifier agents over the net-new
   content) on ANYTHING net-new BEFORE accepting/merging it.** Record each net-new item and
   its harness outcome in [`high-assurance/register.md`](high-assurance/register.md). (This
   directly operationalizes the rule shipped this session: net-new domain docs are exactly the
   gate-blind, high-escaped-cost class the harness is for.)

2. **Source-absent jurisdictions/regimes (FR-59 / FR-61 / FR-62) = cover sourced, ATTEMPT to
   download the missing legislation, defer only the truly-unavailable.** Deepen the
   ref-base-covered ones; for each missing source, ATTEMPT to download the primary-source
   legislation and add it to the appropriate `grc_library_scratch/ref/legislation/` (or
   `ref/standards/`) directory via the scratch ingestion workflow (MCP PR to scratch; egress
   permitting per DD-10). Only where a source cannot be obtained, defer that jurisdiction and
   record it. (Redirect from the "defer all source-absent" default: the maintainer wants the
   download attempted first.)

3. **Out-of-overnight-scope = multi-session orchestration tracks (§4.7 / §4.11 / §4.16 /
   §4.18), FR-48 (H2 rename), and FR-167 gap-fill.** The procedural closing `/matrix-fit` may
   still run. **FR-70 (crypto-asset / blockchain domain) is IN overnight scope** (the
   maintainer's list omitted it): treat it as net-new and run the adversarial-verification
   harness on it before merging, per directive 1.

4. **ISO/IEC 27001:2022 Annex A control TITLES are usable (NOT proprietary).** The maintainer
   clarified: a control title is like a detailed table of contents and is commonly reproduced;
   the proprietary material is the section CONTENT the title heads, not the title. So the ISO
   title-map may carry the verbatim Annex A titles (unblocking the queued P3 ISO-validation
   gate-54 extension and the `/matrix-fit` ISO-column assessment); do NOT reproduce the ISO
   control body/implementation text. Build the ISO title-map from the scratch
   `ref/standards/ISO/` Annex A extracts.

The audit trail lives here, in the [`session-handoff.md`](session-handoff.md) next-actions
queue, and in the session-closing chat message.
