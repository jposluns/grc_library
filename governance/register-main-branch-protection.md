# Main Branch Protection Configuration Register

**Document Title:** Main Branch Protection Configuration Register\
**Document Type:** Register\
**Version:** 1.0.0\
**Date:** 2026-06-02\
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
| Required status check | `Lint markdown corpus` | The CI job that runs the 34-gate audit programme |
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

The ruleset's bypass-actor list is empty as of the **Date** above. No actor is exempt from the rules in the table above.

If a bypass becomes necessary in future (for example, an embargoed security fix that cannot wait for a PR review), the exception is recorded per the protocol in [`dev-security/claude-rules/governance/artefact-and-branch-discipline.md`](../dev-security/claude-rules/governance/artefact-and-branch-discipline.md) section "Exception-handling protocol". That protocol includes the procedure to preserve the pre-rewrite ref under a `refs/preservation/`-prefixed namespace (with the short reason and the ISO date appended, then the original ref name) when a force-push is the only available remediation.

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

The 34-gate audit programme assumes the `Lint markdown corpus` check is required-to-merge. Without that requirement, gates 1-34 still run on each PR but their pass/fail status does not gate the merge. The "Required status check" row above is therefore the load-bearing dependency between the audit programme and the merge-gating mechanism; do not remove or rename the check without updating both surfaces in the same PR.

---

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 | SLSA |
| --- | --- | --- | --- | --- |
| Protected-branch enforcement | PO.5 | CCC-04 | A.8.32 | Level 2 |
| Required reviewer | PO.5 | CCC-01 to 03 | A.8.32 | Level 2 |
| Required status check before merge | PO.5, PW.7 | CCC-04, AIS-04 | A.8.28 | Level 2 |
| Force-push prevention | PO.5, PS.1 | CCC-04 | A.8.32 | Level 2 |
| Auditable configuration snapshot | PS.1, RV.1 | LOG-02, GRC-04 | A.5.36, A.8.15 | Level 3 |
