# Pending Decisions

**Status:** 1 pending (the S2 role-drift authorial decision, 2026-06-29; see `## Pending` below). The four overnight-clarification questions were answered by the maintainer 2026-06-28 via screenshot; recorded below as RESOLVED standing directives for the overnight run, not open questions.

This file is the durable queue for the **attended-autonomous operating mode** (see the
`## Attended-autonomous operating mode` section in [`.claude/CLAUDE.md`](../.claude/CLAUDE.md)):
when the assistant surfaces a decision that is genuinely the maintainer's and no answer
arrives (for example because the `AskUserQuestion` primitive errors, a transient
permission-stream failure), it records the decision here and continues, rather than
stalling.

On `/resume`, the assistant reads this file first, surfaces the still-`pending` entries to
the maintainer, resolves those tasks, and only then continues to the next queued items.

## Pending (open; surface at next attended boundary / `/resume`)

### S2 role-drift resolution (2026-06-29; deferred-blocked, needs maintainer authorial decision)

Building the **S2 role-definition-consistency gate** (TODO §4.5) with the low-FP design (check the `Owner:` / `Approving Authority:` metadata fields and RACI-table roles against [`governance/register-role-authority.md`](../governance/register-role-authority.md)) surfaced **5 roles used as document Owners/Approvers but absent from the register's 35 canonical roles**:

- **GRC Programme Manager** (Owner on ~7 docs)
- **Compliance Maintainer**, **Information Security Maintainer**, **Security Architecture Maintainer** (Owners; siblings of register rows like *AI Security Maintainer*, *Supplier Risk Maintainer*, *Control Framework Maintainer*, which ARE registered)
- **Governance Library Maintainer** (the register's own Owner/Approving Authority; a library-meta role)

These are pre-existing FR-115-class role drift. The gate cannot ship green until they are resolved, and the resolution is **authorial** (defining governance accountabilities for the 4 substantive roles, and deciding whether the library-meta role belongs in an org-role register), which "Proceed" (build S2 with the low-FP design) did not delegate. The `AskUserQuestion` primitive errored (permission-stream flake) when surfacing this, so it is recorded here per the attended-autonomous defer-and-skip path.

**Options put to the maintainer** (recommended first): (A) I draft register rows for the 4 substantive roles by mirroring their sibling rows' accountability pattern, for maintainer review, and handle Governance Library Maintainer as a library-meta row or a documented scope-exclusion, then build the gate; (B) scope-exclude all 5 as library-internal/meta roles via a documented allow-list and build the gate now; (C) defer S2 and build S3/S4 next.

**Proceeded with C (defer-and-skip; reversible, no authorial guess):** S2 is parked pending this decision; routed around to **S4 (no-bare-normative-`shall` gate)** as the next independent gate, which does not hit this fork. The `claude/guardrail-gate-s2` branch was renamed to the S4 build; the §4.5 forward set keeps S2 listed. Resolve A/B/C on resume.

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
