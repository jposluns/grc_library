# Adopter guide

**Document Title:** Adopter Guide\
**Document Type:** Guide\
**Version:** 1.0.0\
**Date:** 2026-06-19\
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

## How the library is meant to be used

Adopting organisations should fork or copy the library, adapt the artefacts to their environment, and maintain the adaptation as part of their own internal governance. The library does not become your governance programme by being copied; the artefacts are a starting structure that your organisation must operate, evidence, and accept residual risk against.

You are not required to adopt the entire library. Most organisations will adopt a subset that matches their domain, sector, jurisdiction, and operating model.

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

If your organisation is small (under approximately 200 staff, low regulatory exposure, no high-risk AI in production), start with these 15 documents and operate them well before adding more:

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
| Severity definitions and notification windows | [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) | Replace with the thresholds your incident commander uses. Regulatory windows (e.g. GDPR 72 hours) are fixed. |
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
