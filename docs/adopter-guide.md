# Adopter guide

This guide is for organisations that want to use the GRC Documentation Library as the starting point for their own governance corpus. It is not part of the library's controlled artefact set, so it is shorter and more prescriptive than the library itself.

## How the library is meant to be used

Adopting organisations should fork or copy the library, adapt the artefacts to their environment, and maintain the adaptation as part of their own internal governance. The library does not become your governance programme by being copied; the artefacts are a starting structure that your organisation must operate, evidence, and accept residual risk against.

You are not required to adopt the entire library. Most organisations will adopt a subset that matches their domain, sector, jurisdiction, and operating model.

## Quick start

1. **Fork or copy the repository.** Fork on GitHub if you intend to track upstream updates. Copy into a private repository if your organisation cannot host a fork.
2. **Pick a starting set.** Browse [`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md). Start with the Core Reference Set called out in the root [`README.md`](../README.md): the governance charter, the document architecture framework, the cross-framework alignment matrix, the document index register, the enterprise governance and risk management policy, the information security policy, and the privacy and data governance policy.
3. **Substitute roles and identifiers.** Every Owner and Approving Authority is role-based. Map each role to a real person in your organisation in a private overlay that you do not commit to a public fork. Do not edit roles into named individuals inside the artefacts themselves.
4. **Validate applicability.** Each artefact contains framework references, regulatory citations, and review-frequency expectations. Validate that each applies to your jurisdiction, sector, processing role, and risk appetite before adopting it.
5. **Track upstream.** If you forked, periodically pull from upstream. Most upstream changes are corrections and additions; conflicts are rare in practice because the corpus uses stable filenames and a controlled metadata block.

## What to change after copying

These items almost always need adapting before the artefacts become operational in your organisation:

| Item | Where it appears | What to change |
| --- | --- | --- |
| Owner and Approving Authority roles | Every document's metadata block | Map each role to a named function in your organisation, recorded in a private overlay. |
| Risk appetite and thresholds | `risk/` and `governance/` policies and standards | Replace illustrative thresholds with values your board has approved. |
| Severity definitions and notification windows | `security/procedure-security-incident-response.md`, `privacy/procedure-data-protection-and-privacy-breach-response.md` | Replace with the thresholds your incident commander uses. Regulatory windows (e.g. GDPR 72 hours) are fixed. |
| Jurisdiction scope | `privacy/jurisdictions/` and `compliance/` sector annexes | Remove jurisdictions and sectors you do not operate in. Keep the relevant ones. Do not delete documents merely because they do not apply yet; mark them deprecated in the index so you do not lose the option. |
| Framework references | Throughout | Confirm that each cited framework is current. Frameworks change versions; the corpus is reviewed annually for currency. |
| Tier classification and supplier categories | `risk/standard-third-party-and-supply-chain-risk.md`, `supply-chain/standard-supplier-security-and-privacy-assurance.md` | Adapt the criteria to your supplier landscape. |
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
2. Run the four local audits to confirm your fork is still conformant after the merge.
3. Resolve any version conflicts by keeping your fork's version on the artefact and recording an upstream-reconciliation note in your local change record.

## When to file an issue upstream

File an issue at https://github.com/jposluns/grc_library/issues if you find:

- A factual error in an artefact.
- A broken or stale framework reference.
- A CC0 licence concern.
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
