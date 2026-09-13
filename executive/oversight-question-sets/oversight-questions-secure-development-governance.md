# What the governing body should ask about the organization's secure-development model, code review, dependencies, pipelines, and release quality

**Document Title:** What the governing body should ask about the organization's secure-development model, code review, dependencies, pipelines, and release quality\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-09-13\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`dev-security/policy-secure-development-and-engineering.md`](../../dev-security/policy-secure-development-and-engineering.md), [`dev-security/procedure-secure-code-review.md`](../../dev-security/procedure-secure-code-review.md), [`dev-security/register-compliance-controls-and-gap-register.md`](../../dev-security/register-compliance-controls-and-gap-register.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/oversight-question-sets/oversight-questions-secure-development-governance.md`](oversight-questions-secure-development-governance.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Oversight Question Set\
**Narrative Status:** Advisory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`dev-security/policy-secure-development-and-engineering.md`](../../dev-security/policy-secure-development-and-engineering.md), [`dev-security/procedure-secure-code-review.md`](../../dev-security/procedure-secure-code-review.md), [`dev-security/standard-developer-security-requirements.md`](../../dev-security/standard-developer-security-requirements.md), [`dev-security/standard-software-composition-analysis.md`](../../dev-security/standard-software-composition-analysis.md), [`dev-security/standard-devops-security-requirements.md`](../../dev-security/standard-devops-security-requirements.md), [`dev-security/guideline-ai-coding-assistant-security.md`](../../dev-security/guideline-ai-coding-assistant-security.md), [`dev-security/standard-quality-assurance-and-testing.md`](../../dev-security/standard-quality-assurance-and-testing.md), [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](../../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md), [`dev-security/register-compliance-controls-and-gap-register.md`](../../dev-security/register-compliance-controls-and-gap-register.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-034\
**Last Reviewed:** 2026-09-13

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Context for these questions

Each question below is paired with the evidence a strong answer produces, and routes to the corpus document that governs it. The evidence is the organization's own populated artifact (its code-review records, its composition-analysis findings, its quality-gate results), not the routed corpus standard or register, which is the governing schema rather than evidence of the organization's state. A governing body learns more from the evidence a question produces than from an assurance that a control exists.

## Questions

**Theme: governance model. Do we develop software under one controlled model?**

- *Is all our software development, internal, outsourced, traditional, and AI-assisted, governed by one secure-development policy rather than team by team?* A strong answer produces the records showing development runs under the [secure-development and engineering policy](../../dev-security/policy-secure-development-and-engineering.md), not a set of separate team practices.

**Theme: secure code and review. Are changes reviewed and held to a coding bar before they ship?**

- *For recent changes to the repositories the review procedure covers, was each reviewed for security defects before merge, including AI-generated code, with any hotfix reviewed in full afterward?* A strong answer produces the security code-review records the [secure-code-review procedure](../../dev-security/procedure-secure-code-review.md) defines, covering human-authored and AI-generated code alike.
- *Where our secure-coding constraints are not met, does that block promotion?* A strong answer produces the promotion-gate results against the constraints the [developer security-requirements standard](../../dev-security/standard-developer-security-requirements.md) defines, not an assurance that the bar is applied.

**Theme: dependencies and supply chain. Do we know, and vet, what we run?**

- *For our open-source and third-party components, do we detect vulnerable or mis-licensed dependencies, including transitive ones where source or an SBOM is available?* A strong answer produces the composition-analysis findings the [software-composition-analysis standard](../../dev-security/standard-software-composition-analysis.md) defines, with the disposition of the open items.
- *Are AI-suggested dependency names verified against an approved registry before they are installed?* A strong answer produces the approved-registry sourcing controls and the pre-install name verification the [developer security-requirements standard](../../dev-security/standard-developer-security-requirements.md) requires.

**Theme: pipeline and delivery. Are our build and deployment paths secured and separated?**

- *Are our CI/CD pipelines, infrastructure as code, and environments secured and separated, and do changes traverse the pipeline's controlled gates?* A strong answer produces the pipeline-security and environment-separation configuration, the infrastructure-as-code security controls, and the logged gate results the [DevOps security-requirements standard](../../dev-security/standard-devops-security-requirements.md) defines as acceptance evidence.

**Theme: AI-assisted development. Do we govern the tools that now write code with us?**

- *Is our use of AI coding assistants governed for the distinct risks they introduce, unreviewed generated code, data exposure, and fabricated packages?* A strong answer produces the governed configuration and usage records the [AI-coding-assistant security guideline](../../dev-security/guideline-ai-coding-assistant-security.md) describes.

**Theme: quality, acceptance, and traceability. Do releases and acquired software clear defined gates, and can we show it?**

- *Are releases held to defined quality gates and acceptance criteria before they go live?* A strong answer produces the quality-gate and acceptance results the [quality-assurance and testing standard](../../dev-security/standard-quality-assurance-and-testing.md) defines.
- *Is third-party and acquired software evaluated and approved before enterprise use, and then lifecycle-managed while in use?* A strong answer produces the evaluation and approval records and the ongoing lifecycle evidence, patch status, software inventory, periodic reviews, and retirement, the [software evaluation, acceptance, and lifecycle standard](../../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md) defines.
- *Can we produce current development-security control status and gaps for audit and this body's reporting?* A strong answer produces the organization's populated entries in the [compliance-controls and gap register](../../dev-security/register-compliance-controls-and-gap-register.md).

**A weak answer in any theme:** an assurance in place of a record. "Code is reviewed" with no review record; "dependencies are safe" with no composition-analysis findings; "we use AI tools responsibly" with no governed configuration; "releases are tested" with no quality-gate results.

## Evidence to request

- The records showing development runs under the secure-development policy, and the security code-review records for recent changes to the covered repositories, including AI-generated code and any post-merge hotfix reviews.
- The promotion-gate results against the secure-coding constraints.
- The composition-analysis findings and their disposition, and the approved-registry sourcing controls and pre-install name verification for AI-suggested dependencies.
- The pipeline-security and environment-separation configuration, the infrastructure-as-code security controls, and the logged gate results; and the governed AI-coding-assistant configuration and usage records.
- The quality-gate and acceptance results; the third-party evaluation and approval records and the ongoing lifecycle evidence (patch status, inventory, reviews, retirement); and the organization's populated development-security control-status entries.

## Limitations

This page is a non-normative executive narrative that creates no compliance by itself; the linked corpus documents govern, and where this page and a corpus document differ, the corpus document prevails. It routes to the corpus rather than reproducing its values: the assurance levels and control identifiers, the severity tiers and remediation timelines, the coverage thresholds, the licence classes, and the register schema live in the linked documents and are not restated here. This page carries composite claims: the division of oversight it describes across the secure-development policy, code review, developer and DevOps requirements, composition analysis, AI-assistant guidance, quality assurance, software lifecycle, and the control register requires validation by the adopting organization against its own arrangements.

**End of Document**
