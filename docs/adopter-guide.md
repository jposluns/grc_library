# Adopter guide

**Document Title:** Adopter Guide\
**Document Type:** Guide\
**Version:** 1.3.1\
**Date:** 2026-06-23\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`README.md`](../README.md), [`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md), [`docs/decision-tree.md`](decision-tree.md), [`docs/worked-example.md`](worked-example.md), [`specification-master-project.md`](../specification-master-project.md)\
**Classification:** Public\
**Category:** Documentation\
**Review Frequency:** Annual and upon material change to the library structure or the adoption model\
**Repository Path:** [`docs/adopter-guide.md`](adopter-guide.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Overview

This guide is for organisations that want to use the GRC Documentation Library as the starting point for their own governance corpus. It is a controlled reference artefact: shorter and more prescriptive than the normative library documents, and intended to orient an adopting organisation rather than to state requirements.

### Where this fits among the adopter entry points

The canonical front door for adopters is [`docs/portal.md`](portal.md) (audience-keyed grouping by role). This adopter guide is one of four deeper-dive paths that branch off the portal; it covers the "fork-and-adapt principles" question. The other three are [`docs/template-quickstart.md`](template-quickstart.md) (what to copy on Day 1), [`docs/decision-tree.md`](decision-tree.md) (sequenced reading order), and [`docs/template-implementation-roadmap.md`](template-implementation-roadmap.md) (calendar phasing). The portal's "Other entry points and when to use them" table picks the right path by question; see the portal Overview.

### Two reference registers you will need early

Two registers carry the library's vocabulary and are worth opening before you start reading domain documents:

- [`governance/register-glossary.md`](../governance/register-glossary.md) — Glossary and Acronym Index. Resolves **acronyms and external-domain terms** (regulations, standards, frameworks, regulators, sector programmes, technical concepts).
- [`governance/register-key-terms-and-definitions.md`](../governance/register-key-terms-and-definitions.md) — Key Terms and Definitions Register. Defines **library-internal GRC concepts** (Audit, Authorize, Control, Owner roles, Exception, etc.) that may differ from generic usage.

The split is by term class: external acronyms / regulators / standards in the Glossary; internal GRC vocabulary in the Key Terms register. Each register cross-references the other. Newcomers can keep both open in adjacent tabs while reading the domain documents.

## How the library is meant to be used

Adopting organisations should fork or copy the library, adapt the artefacts to their environment, and maintain the adaptation as part of their own internal governance. The library does not become your governance programme by being copied; the artefacts are a starting structure that your organisation must operate, evidence, and accept residual risk against.

You are not required to adopt the entire library. Most organisations will adopt a subset that matches their domain, sector, jurisdiction, and operating model.

## Three adoption modes

The repository ships both a GRC corpus and a reference implementation for AI-assisted maintenance of that corpus (the audit toolchain in [`tools/`](../tools/) and the operational pack in [`dev-security/claude-rules/`](../dev-security/claude-rules/)). An adopter can engage at any of three levels; pick the mode that matches what you are actually trying to build, not the most ambitious one.

### Mode A — Fork the whole repo (full adoption)

**Audience.** An organisation building or modernising its GRC programme that also wants AI-assisted maintenance of the resulting corpus.

**What you take.** Everything: the eleven domain directories, the `governance/` corpus, the audit toolchain, the pack, the specifications, the CHANGELOG and version-monotonicity discipline, the `docs/` adopter-facing materials.

**What you ignore.** Nothing structural. You will substitute organisation-specific values inside the artefacts (roles, jurisdictions, sector context, vendor names if any) and add organisation-specific overlays alongside the library content, but the structural shape stays.

**Next step.** Follow the Quick start below and the [`docs/decision-tree.md`](decision-tree.md) for prioritisation.

### Mode B — Adopt the corpus only

**Audience.** An organisation that wants the Markdown content as a starting point but has its own maintenance workflow (or no AI assistance in the loop).

**What you take.** The domain directories you need (`governance/`, `security/`, `privacy/`, `risk/`, etc. as applicable to your scope). The Core Reference Set called out in the root [`README.md`](../README.md). The [`specification-master-project.md`](../specification-master-project.md) if you want to preserve the controlled document model.

**What you ignore.** [`tools/`](../tools/) (the audit toolchain) and [`dev-security/claude-rules/`](../dev-security/claude-rules/) (the pack) unless you choose to opt into one or both later. Your maintenance workflow may be Word + SharePoint, Confluence pages, a different toolchain, or human-only review; the library's content is portable to any of those.

**Next step.** Copy the relevant domain directories. Substitute roles and jurisdiction-specific values per the Quick start. The CC BY-SA 4.0 share-alike clause applies to derivatives you redistribute.

### Mode C — Adopt the pack only

**Audience.** A developer or team that is not building or adopting a GRC library, but wants a solid Claude Code baseline for any project: security rules, language-specific patterns, governance disciplines, and skills for the recurring failure modes an AI coding assistant exhibits.

**What you take.** [`dev-security/claude-rules/`](../dev-security/claude-rules/) (the pack). Its own [`README.md`](../dev-security/claude-rules/README.md) is the front door and the [`setup-generator-prompt.md`](../dev-security/claude-rules/setup-generator-prompt.md) is the AI-assisted installer. The pack ships with its own version sequence (independent of the library's; see the pack README header for the current value) and is documented to operate standalone.

**What you ignore.** Everything else in this repository. The pack does not require the GRC corpus to be present; the pack rules are written as project-agnostic disciplines that any Claude Code project benefits from.

**Why this is supported.** This mode emerged in practice: developers found the pack useful as a Claude Code baseline pack, usable on any project regardless of whether it has a GRC corpus, distilled from the disciplines this library required to maintain itself. The provenance is what makes the pack credible as a standalone artefact: every governance rule in the pack was extracted from a real maintenance event recorded in this library's [`CHANGELOG.md`](../CHANGELOG.md), not invented in the abstract.

**Next step.** Either copy [`dev-security/claude-rules/`](../dev-security/claude-rules/) directly into your project (under `dev-security/claude-rules/` or wherever you want it), or use the pack's setup generator to produce a tailored Claude Code configuration for your specific project. The pack's own [`README.md`](../dev-security/claude-rules/README.md) section "How to use" walks both options.

---

## Quick start

1. **Fork or copy the repository.** Fork on GitHub if you intend to track upstream updates. Copy into a private repository if your organisation cannot host a fork.
2. **Pick a starting set.** Browse [`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md). Start with the Core Reference Set called out in the root [`README.md`](../README.md): the governance charter, the document architecture framework, the cross-framework alignment matrix, the document index register, the enterprise governance and risk management policy, the information security policy, and the privacy and data governance policy.
3. **Substitute roles and identifiers.** Every Owner and Approving Authority is role-based. Map each role to a real person in your organisation in a private overlay that you do not commit to a public fork. Do not edit roles into named individuals inside the artefacts themselves.
4. **Validate applicability.** Each artefact contains framework references, regulatory citations, and review-frequency expectations. Validate that each applies to your jurisdiction, sector, processing role, and risk appetite before adopting it.
5. **Track upstream.** If you forked, periodically pull from upstream. Most upstream changes are corrections and additions; conflicts are rare in practice because the corpus uses stable filenames and a controlled metadata block.

## Applicability decision tree

Use this to decide which domains and sector annexes your organisation needs.

| Question | If yes, adopt | If no, skip |
| --- | --- | --- |
| Does the organisation handle any personal data of identifiable individuals? | `privacy/` domain + applicable jurisdiction annexes in `privacy/jurisdictions/` | All of privacy/ |
| Does the organisation operate AI systems, services, or agents in production? | `ai/` domain | All of ai/ (but keep the framework as reference) |
| Does the organisation operate cloud workloads? | `dev-security/standard-cloud-hardening-baseline-{aws,azure,gcp}.md` for the platforms in use | The non-relevant cloud baselines |
| Does the organisation deliver customer-facing services? | [`operations/standard-site-reliability-engineering.md`](../operations/standard-site-reliability-engineering.md), [`operations/standard-observability-and-telemetry.md`](../operations/standard-observability-and-telemetry.md), `resilience/` domain | The SLA-related operations content |
| Does the organisation participate in BASC trade-security certification? | `compliance/logistics/` | All of compliance/logistics/ |
| Does the organisation participate in CTPAT, AEO, AEO-S, or PIP trade programmes? | The relevant programme annexes in `compliance/` | The non-relevant trade-compliance annexes |
| Does the organisation operate in a sector with sector-specific regulation (financial services, healthcare, transportation/logistics, telecoms, energy/utilities, public sector)? | The corresponding `compliance/annex-*` | Non-relevant sector annexes |
| Does the organisation operate under SOX or equivalent financial reporting controls? | [`compliance/financial-services/annex-sox-itgc.md`](../compliance/financial-services/annex-sox-itgc.md) | This annex |
| Does the organisation operate under DORA, NIS 2, or equivalent EU resilience regulation? | The corresponding implementation annex in `compliance/` | These annexes |
| Does the organisation have a software development practice? | `dev-security/` domain | Most of dev-security/ (keep the policy as reference) |
| Does the organisation have a formal architecture practice? | `architecture/` domain | Most of architecture/ (keep ADR standard as a useful reference regardless) |
| Does the organisation have suppliers with material operational or data access? | `supply-chain/` domain + [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md) | Most of supply-chain/ |

The cross-cutting documents (`governance/`, top-level [`README.md`](../README.md), `risk/` core artefacts, `security/` core policies) apply to virtually every organisation and are the starting baseline.

## Maturity progression

Most adopting organisations cannot operate all of the library's controls on day one. The library is meant to be a progressive adoption target, not a one-shot implementation. Use the maturity tiers from [`governance/guideline-minimum-viable-governance-structure.md`](../governance/guideline-minimum-viable-governance-structure.md) to choose a target tier and progress towards it.

### Tier 1 starter set (minimum viable)

If your organisation is small (under approximately 200 staff, low regulatory exposure, no high-risk AI in production), start with these 15 documents and operate them well before adding more. This Tier 1 set overlaps the six-artefact Day-1 floor named in [`docs/template-quickstart.md`](template-quickstart.md): it shares four of those six artefacts, while the Day-1 floor additionally names the acceptable-use and identity-and-access-management policies that this Tier 1 set leaves for a later pass. Tier 1 in turn sits within the larger sector-conditional sets the [`docs/decision-tree.md`](decision-tree.md) builds (for example about 25 documents for an EU-fintech path). The three sizes are complementary starting points rather than competing ones.

**Approximate reading time**: 4 to 6 hours to read all 15 documents once at a moderate pace; substantially longer to internalise. **If you only read three** to get an immediate orientation, pick the three Governance documents in the table below (Charter + Framework + Role Authority Register); they ground the structure that the rest of Tier 1 operationalises.

| Type | Document |
| --- | --- |
| Charter | [`governance/charter-governance-library.md`](../governance/charter-governance-library.md) |
| Framework | [`governance/framework-document-architecture-and-interrelationship.md`](../governance/framework-document-architecture-and-interrelationship.md) |
| Register | [`governance/register-role-authority.md`](../governance/register-role-authority.md) |
| Register | [`governance/register-key-terms-and-definitions.md`](../governance/register-key-terms-and-definitions.md) |
| Policy | [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md) |
| Standard | [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md) |
| Procedure | [`risk/procedure-risk-assessment-methodology.md`](../risk/procedure-risk-assessment-methodology.md) |
| Procedure | [`risk/procedure-risk-acceptance.md`](../risk/procedure-risk-acceptance.md) |
| Policy | [`security/policy-information-security.md`](../security/policy-information-security.md) |
| Standard | [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md) |
| Procedure | [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) |
| Policy | [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md) |
| Procedure | [`privacy/procedure-data-subject-rights-management.md`](../privacy/procedure-data-subject-rights-management.md) |
| Procedure | [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) |
| Standard | [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md) (if you do software development) |

Use [`governance/guideline-minimum-viable-governance-structure.md`](../governance/guideline-minimum-viable-governance-structure.md) Tier 1 forum structure to operate them.

### Tier 2 growth set (mid-market addition)

When you have the starter set operating reliably and your organisation has grown to mid-market complexity, add these:

- `ai/` core artefacts: framework, governance council charter, model registry, foundation-model lifecycle procedure, AI security and risk standard.
- `supply-chain/` core artefacts: third-party risk standard (now consolidated in [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md)), supplier due-diligence procedure, supplier ongoing monitoring procedure.
- `resilience/` core artefacts: business continuity and disaster recovery policy, framework, IT disaster recovery plan, recovery runbook template.
- `compliance/` core artefacts: compliance and audit management policy, internal audit standard, the sector annexes relevant to your context.
- `operations/` core artefacts: change management procedure, patch management procedure, observability and telemetry standard.
- `dev-security/` core artefacts: secure development policy, API security standard, the cloud hardening baselines for your platforms.

Use Tier 2 forum structure.

### Tier 3 enterprise set

The full library is intended to be operable at Tier 3 by a large, regulated, multi-jurisdiction organisation. Every active document in the index is in scope.

## Sector-conditional content

Sector-conditional content lives in sub-directories of `compliance/` (`compliance/logistics/`, and others as they are introduced). Most organisations adopt only the sub-directories matching their industry sector. For example, the `compliance/logistics/` sub-directory contains industry-wide logistics annexes plus trusted-trader programme overlays (CTPAT, PIP, AEO, BASC). If your organisation does not operate in the logistics sector, the directory is informational only.

## What to change after copying

These items almost always need adapting before the artefacts become operational in your organisation:

| Item | Where it appears | What to change |
| --- | --- | --- |
| Owner and Approving Authority roles | Every document's metadata block | Map each role to a named function in your organisation, recorded in a private overlay. |
| Risk appetite and thresholds | `risk/` and `governance/` policies and standards | Replace illustrative thresholds with values your board has approved. |
| Severity definitions and notification windows | [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) | Replace with the thresholds your incident commander uses. Regulatory windows (e.g. GDPR 72 hours) are fixed. Where more than one regulator applies with different clocks (for example a privacy regulator plus a sector regulator plus a US state breach law), set the procedure to the shortest binding window. |
| Enforcement and disciplinary clauses | Policy `## Enforcement` sections (for example [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md) section 9) and the privacy jurisdiction annexes | Reconcile disciplinary language ("up to and including termination") and regulatory-reporting language with your HR policy, employment contracts, and local labour law before going live. |
| Jurisdiction scope | `privacy/jurisdictions/` and `compliance/` sector annexes | Remove jurisdictions and sectors you do not operate in. Keep the relevant ones. Do not delete documents merely because they do not apply yet; mark them deprecated in the index so you do not lose the option. |
| Framework references | Throughout | Confirm that each cited framework is current. Frameworks change versions; the corpus is reviewed annually for currency. |
| Tier classification and supplier categories | [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md) | Adapt the criteria to your supplier landscape. |
| Trade-security programmes | `compliance/` and `supply-chain/` trade artefacts | Remove if your organisation is not involved in customs or international trade. |

## What not to change

- Do not edit Owner or Approving Authority into a named individual. Keep roles role-based even after adoption. Map roles to people in a separate, private overlay.
- Do not remove the metadata block, the License field, or the `End of Document` marker.
- Do not insert organisation-specific identifiers (real names, IP addresses, internal system names, contract numbers, customer names) into a public fork.

## Minimum quality bar before going live

Before treating an adopted artefact as operational in your organisation:

1. The artefact has been read end-to-end by the named role Owner.
2. The Approving Authority has signed off (electronically or in a documented decision record).
3. Any framework reference, regulatory citation, or threshold inconsistent with your environment has been corrected or removed.
4. The artefact has been added to your organisation's evidence repository with traceability to the upstream version it was adapted from.
5. The control statements within the artefact have a named operational owner.

## Tracking upstream updates

The library publishes phase-level releases through the [CHANGELOG](../CHANGELOG.md). When pulling from upstream:

1. Read the changelog entry for the period since your last pull.
2. Run `tools/run_all_audits.sh` to confirm your fork is still conformant after the merge.
3. Resolve any version conflicts by keeping your fork's version on the artefact and recording an upstream-reconciliation note in your local change record.

A customised fork hits three recurring cases the pull does not resolve on its own:

- **Merge conflicts in artefacts you have edited.** Where you have adapted an artefact and upstream also changed it, resolve the conflict in favour of your adaptation, then re-apply any upstream correction that still matters (a fixed citation, a new control) on top. Record what you took and what you kept in your local change record.
- **A new upstream audit gate your fork now fails.** Upstream sometimes adds a gate that your customised content trips (see "Running the audit toolchain on your fork" below). The library's own posture is to fix the artefact rather than weaken the gate; an adopter may instead relax or scope a gate locally where a customisation legitimately requires it, but should document the deviation and a review date in the local change record (the same exception discipline the pack's gate-discipline rule describes) rather than silently disabling the check.
- **Version-monotonicity conflicts.** If both you and upstream bumped the same artefact, keep your fork's version line and record the upstream version you reconciled against, so your local history stays monotonic.

### Running the audit toolchain on your fork

Some audit gates are calibrated for this library's organisation-neutral public corpus and will raise false positives once you insert real values. In particular, [`tools/lint-pii-in-content.py`](../tools/lint-pii-in-content.py) and [`tools/lint-secrets-in-content.py`](../tools/lint-secrets-in-content.py) will flag the real role-holders, names, internal system names, or credentials a fork legitimately carries. Keep organisation-specific values in a private overlay directory the linters do not scan (the toolchain reads its exempt directories from `DEFAULT_EXEMPT_DIRS` in [`tools/lint_common.py`](../tools/lint_common.py); add your overlay directory there), or keep those values out of the committed fork entirely. Relax or scope a gate only with a documented deviation, per the upstream-tracking guidance above.

## When to file an issue upstream

File an issue at https://github.com/jposluns/grc_library/issues if you find:

- A factual error in an artefact.
- A broken or stale framework reference.
- A licence concern.
- An auditor false positive or false negative.

Do not file issues asking for adaptations specific to your organisation. Those are the adopter's responsibility.

## Adopter checklist

A short copy-paste checklist for first-time adoption:

```
[ ] Repository forked or copied
[ ] Core Reference Set identified and read end-to-end
[ ] Roles mapped to organisation in private overlay
[ ] Jurisdictional scope confirmed
[ ] Sectoral applicability confirmed
[ ] Risk appetite values replaced with board-approved figures
[ ] Severity and notification windows replaced with internal thresholds
[ ] Framework references confirmed current
[ ] Trade-security programmes retained or removed as appropriate
[ ] Audit and approval governance signed off
[ ] Evidence repository linked to adopted artefacts
[ ] Upstream tracking schedule established (e.g. quarterly pull)
```
