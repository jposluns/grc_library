# When an AI-suggested dependency turns out to be a malicious package

**Document Title:** When an AI-suggested dependency turns out to be a malicious package\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-09-13\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`dev-security/guideline-ai-coding-assistant-security.md`](../../dev-security/guideline-ai-coding-assistant-security.md), [`dev-security/standard-developer-security-requirements.md`](../../dev-security/standard-developer-security-requirements.md), [`dev-security/standard-software-composition-analysis.md`](../../dev-security/standard-software-composition-analysis.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/scenarios/scenario-ai-suggested-malicious-dependency.md`](scenario-ai-suggested-malicious-dependency.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Scenario\
**Narrative Status:** Non-normative\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`dev-security/guideline-ai-coding-assistant-security.md`](../../dev-security/guideline-ai-coding-assistant-security.md), [`dev-security/standard-developer-security-requirements.md`](../../dev-security/standard-developer-security-requirements.md), [`dev-security/standard-software-composition-analysis.md`](../../dev-security/standard-software-composition-analysis.md), [`dev-security/procedure-secure-code-review.md`](../../dev-security/procedure-secure-code-review.md), [`dev-security/standard-devops-security-requirements.md`](../../dev-security/standard-devops-security-requirements.md), [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](../../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md), [`dev-security/register-compliance-controls-and-gap-register.md`](../../dev-security/register-compliance-controls-and-gap-register.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-035\
**Last Reviewed:** 2026-09-13

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Scenario premise

Under delivery pressure, a developer accepts an AI coding assistant's suggestion to add a third-party package and installs it without verifying that the name exists in an approved registry. The suggested name is fabricated, and a malicious package has been published under it. This scenario walks the event through the controls the dev-security corpus sets, to show a governing body where each engages and what evidence a well-run response leaves behind.

## How the event unfolds

The package was installed outside the verification and vetting controls, not through them. Genuinely urgent work has a formal exception path in the corpus, approved as a policy waiver rather than skipped silently; the failure here is that the controls were bypassed, not that no path existed. What follows is either the fabricated name caught at a control before it ran, or a malicious package discovered after it was in the codebase.

## Where the corpus controls engage

- **The risk named.** The [AI-coding-assistant security guideline](../../dev-security/guideline-ai-coding-assistant-security.md) is where this risk is set out: AI assistants may suggest package names that do not exist, which an attacker can register and populate.
- **The install-time control.** The [developer security-requirements standard](../../dev-security/standard-developer-security-requirements.md) is where AI-suggested dependency names are required to be verified against an approved registry before installation.
- **The systematic supply-chain control.** The [software-composition-analysis standard](../../dev-security/standard-software-composition-analysis.md) is where dependency-confusion and malicious-package risk is managed through approved-registry sourcing, pinning, lock files, and integrity checks.
- **The gate it should have passed.** The [secure-code-review procedure](../../dev-security/procedure-secure-code-review.md) is where a dependency's provenance is inspected before merge, and where an out-of-policy install is an approved waiver rather than a silent one.
- **Containment in delivery.** The [DevOps security-requirements standard](../../dev-security/standard-devops-security-requirements.md) is where pipeline security and environment separation engage to limit how far a compromised build reaches.
- **Controlled acquisition.** The [software evaluation, acceptance, and lifecycle standard](../../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md) is where a new third-party component is evaluated and approved before enterprise use.
- **Governance visibility.** The [compliance-controls and gap register](../../dev-security/register-compliance-controls-and-gap-register.md) is where the resulting control status and any gap are recorded for reporting.

## What good looks like

Because the install skipped verification, the package's legitimacy was never established up front, so a well-run response depends on a later control surfacing it, most directly the code-review provenance inspection of the published-by chain, rather than production being the first to reveal it. Where composition analysis produced a finding, the component was flagged and the disposition recorded. Where the build was affected, pipeline separation limited its reach. The control status and any gap were recorded for governance. Each of those is a control the organization can point to and evidence.

## Evidence to request

- The registry-verification record, or its absence, for the added dependency.
- The code-review record that should have inspected the dependency's provenance.
- The composition-analysis finding where analysis produced one, or the applicable supply-chain control records (approved-registry sourcing, pinning, lock files, integrity checks), and the disposition for the component.
- The pipeline and environment-separation configuration for the affected build path.
- The control-status entry and any recorded gap in the development-security register.

## Limitations

This page is a non-normative executive narrative that creates no compliance by itself; the linked corpus documents govern, and where this page and a corpus document differ, the corpus document prevails. It routes to the corpus rather than reproducing its values: the approved-registry and pinning configuration, the provenance-inspection criteria, the pipeline-security controls, the acquisition-evaluation criteria, and the register schema live in the linked documents and are not restated here. This page carries composite claims: the sequence it describes across the named risk, the install-time control, composition analysis, code review, delivery containment, controlled acquisition, and governance visibility requires validation by the adopting organization against its own arrangements. The scenario is illustrative and makes no likelihood claim; a real event's facts determine which controls engage and how.

**End of Document**
