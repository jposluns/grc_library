# What the governing body should require for secure-development governance oversight

**Document Title:** What the governing body should require for secure-development governance oversight\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-09-13\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`dev-security/policy-secure-development-and-engineering.md`](../../dev-security/policy-secure-development-and-engineering.md), [`dev-security/procedure-secure-code-review.md`](../../dev-security/procedure-secure-code-review.md), [`dev-security/register-compliance-controls-and-gap-register.md`](../../dev-security/register-compliance-controls-and-gap-register.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/briefs/brief-secure-development-governance-oversight.md`](brief-secure-development-governance-oversight.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Executive Brief\
**Narrative Status:** Explanatory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`dev-security/policy-secure-development-and-engineering.md`](../../dev-security/policy-secure-development-and-engineering.md), [`dev-security/standard-developer-security-requirements.md`](../../dev-security/standard-developer-security-requirements.md), [`dev-security/standard-devops-security-requirements.md`](../../dev-security/standard-devops-security-requirements.md), [`dev-security/procedure-secure-code-review.md`](../../dev-security/procedure-secure-code-review.md), [`dev-security/standard-software-composition-analysis.md`](../../dev-security/standard-software-composition-analysis.md), [`dev-security/standard-quality-assurance-and-testing.md`](../../dev-security/standard-quality-assurance-and-testing.md), [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](../../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md), [`dev-security/guideline-ai-coding-assistant-security.md`](../../dev-security/guideline-ai-coding-assistant-security.md), [`dev-security/register-compliance-controls-and-gap-register.md`](../../dev-security/register-compliance-controls-and-gap-register.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-033\
**Last Reviewed:** 2026-09-13

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Why this matters

Software is where an organization builds its own risk. The governing body's question is not whether software ships, but whether it can require, and see in evidence, that software is designed, coded, reviewed, tested, and its dependencies vetted under a controlled secure-development model, rather than on the trust that each team does the right thing.

## What the corpus establishes

- The [secure-development and engineering policy](../../dev-security/policy-secure-development-and-engineering.md) is the **dependency** of the programme: it defines the mandatory framework for secure development, engineering practice, and lifecycle management.
- The [developer security-requirements standard](../../dev-security/standard-developer-security-requirements.md) is a **prevention** control against insecure application code: it defines the secure-coding design constraints that apply from the first line of code.
- The [DevOps security-requirements standard](../../dev-security/standard-devops-security-requirements.md) is a **prevention** control against an insecure delivery pipeline: it defines the security requirements for CI/CD, infrastructure as code, environment management, and automation.
- The [secure-code-review procedure](../../dev-security/procedure-secure-code-review.md) is a **prevention** control against security defects reaching a protected branch: it defines how code, human-authored and AI-generated alike, is reviewed for security before merge and release.
- The [software-composition-analysis standard](../../dev-security/standard-software-composition-analysis.md) is a **prevention** control against supply-chain attack through dependencies: it defines how open-source and third-party components are identified, tracked, and risk-managed.
- The [quality-assurance and testing standard](../../dev-security/standard-quality-assurance-and-testing.md) makes a **contribution** to reliable, validated releases: it defines the testing lifecycle, quality gates, and acceptance criteria.
- The [software evaluation, acceptance, and lifecycle standard](../../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md) makes a **contribution** to controlled software acquisition and lifecycle: it defines how software is evaluated, approved, maintained, and retired.
- The [AI-coding-assistant security guideline](../../dev-security/guideline-ai-coding-assistant-security.md) makes a **contribution** to the secure use of AI coding assistants: it defines the practices for code they generate and the data they may access.
- The [compliance-controls and gap register](../../dev-security/register-compliance-controls-and-gap-register.md) is the **evidence** structure for development-security control status: it defines the traceability schema mapping controls to their status.

## What this means for the organization

- **Require a governance model, not just shipped software.** Development that runs without a secure-development policy, secure-coding constraints, and code review is shipping on trust; the corpus starts from the model.
- **Expect evidence, not assurances.** The organization's populated code-review records, promotion-gate and quality-gate results, SCA findings, and control-status register are the evidence classes; a control the organization cannot evidence is not demonstrably operating. The routed corpus standards and register are the governing schemas, not evidence of the organization's own state.
- **A dependency introduced outside the assessment path is a risk the organization has not assessed.** An open-source, transitive, or AI-suggested component that enters the codebase without the prescribed software-composition-analysis controls bypasses the corpus's dependency-risk assessment path.

## Evidence to request

- The recent code-review records showing security review before merge, including for AI-generated code.
- The promotion-gate and quality-gate results for a recent release.
- The software-composition-analysis findings and the disposition of the open items.
- The control-status entries of the development-security compliance-controls register.

## Limitations

This page is a non-normative executive narrative that creates no compliance by itself; the linked corpus documents govern, and where this page and a corpus document differ, the corpus document prevails. It routes to the corpus rather than reproducing its values: the assurance levels and control identifiers, the dependency and end-of-life timelines, the licence classes, the review cadences, and the register schema live in the linked documents and are not restated here. This page carries composite claims: the division of labour it describes across the secure-development policy, developer and DevOps requirements, code review, composition analysis, quality assurance, software lifecycle, AI-assistant guidance, and the control register requires validation by the adopting organization against its own arrangements.

**End of Document**
