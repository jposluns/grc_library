# Main Branch Protection Configuration Register

**Document Title:** Main Branch Protection Configuration Register\
**Document Type:** Register\
**Version:** 1.0.9\
**Date:** 2026-06-20\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`dev-security/claude-rules/governance/artefact-and-branch-discipline.md`](../dev-security/claude-rules/governance/artefact-and-branch-discipline.md), [`governance/specification-audit-programme.md`](specification-audit-programme.md), [`governance/procedure-library-quality-and-review-cadence.md`](procedure-library-quality-and-review-cadence.md), [`README.md`](../README.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon any change to the configured ruleset, the audit programme's required-checks list, or the bypass-actors list\
**Repository Path:** [`governance/register-main-branch-protection.md`](register-main-branch-protection.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register is a snapshot of the GitHub branch-protection configuration applied to the `main` branch of this repository as of the **Date** field above. It exists so that drift between the configured state and the [`dev-security/claude-rules/governance/artefact-and-branch-discipline.md`](../dev-security/claude-rules/governance/artefact-and-branch-discipline.md) pack rule can be detected by inspection at the next review.

The configured rules are enforced server-side by GitHub. This register does not replace that enforcement; it records the operator-visible intent so the configured state can be audited without a privileged settings-page view.

---

## Scope

The configuration recorded here covers the `main` branch only. No other branches are protected.

The configuration is expressed via GitHub Rulesets (the modern UI) rather than the classic branch-protection settings. Both mechanisms work; this repository uses Rulesets.

---

## Configured rules

| Setting | State | Pack-rule alignment |
| --- | --- | --- |
| Restrict deletions | Enabled | Required (prevents branch deletion) |
| Require signed commits | Enabled | Optional in pack rule; this repository takes the stricter posture |
| Require a pull request before merging | Enabled | Required |
| Required approvals | 1 | Required minimum; pack rule allows higher for security-sensitive repositories |
| Dismiss stale pull request approvals when new commits are pushed | Enabled | Recommended |
| Require conversation resolution before merging | Enabled | Recommended |
| Allowed merge methods | Merge, Squash, Rebase | Per project convention |
| Require status checks to pass | Enabled | Required |
| Required status check | `Lint markdown corpus` | The CI job that runs the 42-gate audit programme |
| Require branches to be up to date before merging | Enabled | Recommended |
| Block force pushes | Enabled | Required (prevents history rewrite on `main`) |

---

## Rules explicitly left off

Each is permitted by the pack rule as project preference; the deliberate-off state is recorded here so future audits do not flag it as drift.

| Setting | State | Rationale |
| --- | --- | --- |
| Restrict creations | Off | Not relevant to a single-branch-protected repository |
| Restrict updates | Off | Off pairs with the existing `Require a pull request before merging` rule |
| Require linear history | Off | The project uses merge-commits as the default merge mechanism; squash and rebase are also allowed but not required |
| Require deployments to succeed | Off | No deployment environments are configured for this repository |
| Require review from Code Owners | Off | No `CODEOWNERS` file is configured |
| Require approval of the most recent reviewable push | Off | Stricter than the pack rule requires for a non-security-sensitive content library |
| Require code scanning results | Off | Code scanning is not configured |
| Require code quality results | Off | Code quality tools are not configured |
| Automatically request Copilot code review | Off | Per project preference |

---

## Bypass list

| Actor | Bypass mode | Added | Rationale |
| --- | --- | --- | --- |
| `jposluns` (maintainer) | For pull requests | 2026-06-02 | Solo-maintainer posture: the project currently has one human maintainer, who is also the actor authoring PRs via the GitHub MCP / API. GitHub's hard-coded self-review prohibition prevents the maintainer from approving their own PR; without a bypass entry, no PR authored by the maintainer can be merged. The bypass enables in-chat / API-driven merges for maintainer-authored PRs while leaving the "≥1 approving review" rule in force for any future external contributor (whose PRs are not bypassed). This is a documented exception per the [`dev-security/claude-rules/governance/gate-discipline.md`](../dev-security/claude-rules/governance/gate-discipline.md) exception-handling protocol; review trigger: addition of any second maintainer to the repository. |

### What the bypass affects

In "For pull requests" mode the listed actor bypasses **all** rules in the table above when merging a PR they authored. That includes the `Lint markdown corpus` required status check: the maintainer can technically merge a PR whose CI is failing. The operational discipline that the maintainer continues to wait for CI green before merging is therefore behavioural, not gate-enforced; this is acceptable for the current solo-maintainer posture and is reviewed at the trigger above. Direct push to `main` is still prevented (the PR mechanism is still required, even with the bypass), and force-push and branch deletion remain blocked for the bypass actor by the lower-level `Block force pushes` and `Restrict deletions` rules (which are not part of the PR-merge bypass scope).

### Exception-handling cross-reference

The bypass is logged here in lieu of a separate exception register. The pack rule [`dev-security/claude-rules/governance/gate-discipline.md`](../dev-security/claude-rules/governance/gate-discipline.md) section "Exception-handling protocol" specifies that such exceptions are time-bounded; the time-bound for this bypass is the project's transition out of solo-maintainer posture (no calendar deadline because no second maintainer is yet planned). If the maintainer set grows beyond one, this entry is removed and PRs authored by that maintainer go through the standard review path the same as any other contributor's.

---

## Configuration on adjacent settings pages

The following settings are configured outside the ruleset but contribute to the same discipline:

| Location | Setting | State |
| --- | --- | --- |
| Settings → General → Pull Requests | Automatically delete head branches | Enabled (head branches deleted on PR merge so dangling refs do not accumulate) |

---

## Drift-detection procedure

This register is a snapshot, not a live source of truth. The configured state can drift if a maintainer modifies the ruleset without updating this file. To detect drift:

1. On every scheduled review (per the **Review Frequency** field above), open the GitHub repository's Settings → Rules → Rulesets page and compare each row of the "Configured rules" table to the live configuration.
2. On any change to the configured ruleset (new check required, bypass actor added, rule toggled), update this register in the same PR.
3. The [`dev-security/claude-rules/governance/artefact-and-branch-discipline.md`](../dev-security/claude-rules/governance/artefact-and-branch-discipline.md) pack rule names the settings that the audit programme depends on; if the pack rule changes its expectations, this register is reviewed against the updated expectations and rules are adjusted if needed.

---

## Audit-trail relationship

The 42-gate audit programme assumes the `Lint markdown corpus` check is required-to-merge. Without that requirement, gates 1-42 still run on each PR but their pass/fail status does not gate the merge. The "Required status check" row above is therefore the load-bearing dependency between the audit programme and the merge-gating mechanism; do not remove or rename the check without updating both surfaces in the same PR.

---

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 | SLSA |
| --- | --- | --- | --- | --- |
| Protected-branch enforcement | PO.5 | CCC-04 | A.8.32 | Level 2 |
| Required reviewer | PO.5 | CCC-01 to 03 | A.8.32 | Level 2 |
| Required status check before merge | PO.5, PW.7 | CCC-04, AIS-04 | A.8.28 | Level 2 |
| Force-push prevention | PO.5, PS.1 | CCC-04 | A.8.32 | Level 2 |
| Auditable configuration snapshot | PS.1, RV.1 | LOG-02, GRC-04 | A.5.36, A.8.15 | Level 3 |
