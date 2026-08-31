# Semantic Continuity in Migration and Retirement Standard

**Document Title:** Semantic Continuity in Migration and Retirement Standard\
**Document Type:** Standard\
**Version:** 0.0.2\
**Date:** 2026-08-31\
**Owner:** GRC Programme Manager\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/standard-ai-model-succession-and-identity.md`](../ai/standard-ai-model-succession-and-identity.md), [`ai/procedure-foundation-model-lifecycle.md`](../ai/procedure-foundation-model-lifecycle.md), [`ai/procedure-ai-model-lifecycle-management.md`](../ai/procedure-ai-model-lifecycle-management.md), [`supply-chain/standard-cloud-exit-and-data-portability.md`](../supply-chain/standard-cloud-exit-and-data-portability.md), [`supply-chain/procedure-supplier-exit-and-data-return.md`](../supply-chain/procedure-supplier-exit-and-data-return.md), [`operations/procedure-change-management-and-configuration-control.md`](../operations/procedure-change-management-and-configuration-control.md), [`operations/register-asset-inventory.md`](../operations/register-asset-inventory.md), [`governance/standard-records-retention-and-destruction.md`](standard-records-retention-and-destruction.md)\
**Classification:** Public\
**Category:** Governance\
**Review Frequency:** Annual and upon material change to migration, lifecycle, or retirement practice\
**Repository Path:** [`governance/standard-semantic-continuity-in-migration-and-retirement.md`](standard-semantic-continuity-in-migration-and-retirement.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

This standard requires that, before a predecessor is retired in favour of a successor, the organization demonstrate that the successor preserves the meaning of what the predecessor did, not only that the data and configuration moved completely and intact. It adds a semantic-continuity gate to the existing migration and retirement controls: portability and completeness verification (counts, checksums, readable-and-complete checks) remain necessary but are no longer sufficient to authorize retirement. The gate governs the retirement of a predecessor that has a successor; a decommissioning with no successor is out of scope and is governed by the existing completeness and destruction controls alone.

---

## 1. Purpose and scope

When one thing replaces another, the organization tends to verify that the move was complete: the records transferred, the checksums match, the new system is readable and populated. Completeness answers whether the bits arrived; it does not answer whether the successor decides, classifies, or behaves as the predecessor did. A migration can be complete and lossless at the level of data and still change the meaning of the outputs: a re-mapped code list, a re-trained model, a replacement control that admits a different population. When the predecessor is then retired, that semantic change becomes invisible and irreversible.

This standard governs the retirement or replacement of a predecessor by a successor across five predecessor classes: AI models, systems and applications, services (including a supplier being exited), datasets, and controls (a control retired in favour of a compensating or replacement control). It requires a meaning-preserving comparison between predecessor and successor as a precondition of retiring the predecessor. It is deliberately additive: it does not replace the exit, portability, decommissioning, and destruction controls in Related Documents, it adds a gate those controls must pass before the predecessor is retired. Retirement without a successor (a genuine decommissioning, where nothing inherits the predecessor's function) is out of scope; there is nothing to compare, and the completeness and destruction controls suffice.

## 2. The semantic-continuity gate

Retirement of a predecessor that has a successor is conditioned on a recorded, meaning-preserving comparison demonstrating that the successor preserves the decisions, behaviours, and interpretations the predecessor produced, within pre-declared tolerances. Completeness and portability verification (record counts, checksums, readable-and-complete checks) is necessary but not sufficient: it establishes that the successor has what it needs, not that the successor means the same thing. The gate is a precondition of retirement, not of migration: the successor may be stood up, run in parallel, and operated before the gate is met; what the gate governs is the point at which the predecessor is retired and its outputs can no longer be reproduced or compared.

## 3. Comparison methods by predecessor class

The comparison demonstrates decision, behaviour, and interpretation equivalence, not data equivalence. The method is chosen to fit the predecessor class:

- **AI models and agents:** replay a representative and edge-case set of the predecessor's decisions through the successor and compare outcomes (a golden-set replay, consistent with the eval-suite comparison at model version transition in the foundation-model lifecycle procedure). The succession standard's pause-and-compare validation is one implementation of this gate for AI models.
- **Systems and applications:** sample representative and boundary transactions and compare the successor's outputs, states, and decisions against the predecessor's for the same inputs.
- **Services (including supplier exit):** compare the service's outputs and decision behaviour before and after the transition, not only the returned data's completeness.
- **Datasets:** compare interpretation, not just contents: schema semantics, unit and code-list meaning, and the classification or downstream decisions the data drives, so that a complete-but-re-mapped dataset does not silently change meaning.
- **Controls:** compare the population the replacement control admits, blocks, or flags against the predecessor control's, so that a control retired in favour of a compensating control is shown to cover the same cases.

## 4. Pass criteria and tolerance

Equivalence thresholds and materiality classes are declared before the comparison is run, so that pass and fail are judged against a pre-committed bar rather than rationalized after the result is seen. Each divergence between predecessor and successor is classified as an intended improvement (a deliberate, approved change the successor is meant to introduce), a regression (an unintended loss of fidelity), or an unexplained divergence. An intended improvement that stays within the pre-declared tolerance is recorded and does not fail the gate; an intended improvement that falls outside tolerance, like any regression or unexplained divergence, fails the gate until it is resolved or explicitly accepted under section 5.

## 5. Authorization on a partial pass

Where the comparison passes within tolerance, retirement proceeds. Where it leaves a documented residual divergence, retirement requires an explicit, recorded acceptance by the named approver for the predecessor's class together with the governing forum where one exists (for an AI model, the accountable approver and the AI governance forum; for a control, the control owner and the risk-acceptance authority). The acceptance records the residual divergence, its assessed impact, and the rationale; it is never the default that follows from an incomplete comparison. An absent or inconclusive comparison is not a partial pass and cannot be accepted under this section; it fails the gate.

## 6. Fail path

Where the gate fails and the divergence is not accepted under section 5, the predecessor is not retired. The successor and predecessor are held in parallel (or the predecessor is otherwise retained as a fallback, consistent with the benchmark and fallback retention the AI model lifecycle procedure requires) until the divergence is resolved or accepted. Where the predecessor genuinely cannot be retained (a supplier contract ending, a platform being withdrawn), the inability to retain it is itself escalated to the governing authority as a risk decision, fail-closed, rather than allowed to force an unexamined retirement by default.

## 7. Evidence and retention

The comparison method, the pre-declared tolerances, the divergences and their classifications, any section 5 acceptance, and the retirement decision are recorded and retained as the evidence that the gate was met. Retention follows the records retention and destruction standard; the evidence is retained at least until the successor's own next transition, so that a later question about whether meaning was preserved at this retirement can be answered from the record.

## 8. Relationship to existing controls

This standard is additive and composes with, rather than duplicates, the existing migration and retirement controls. The exit, portability, and supplier-return controls establish that the move is complete and the data is recoverable; this standard adds the meaning-preserving comparison those controls do not perform. The AI model succession and identity standard governs the successor's standing (the approvals, access, and delegations it may or may not inherit) and, for AI models, its pause-and-compare validation is one implementation of this gate; this standard is the broader retirement gate spanning all five predecessor classes. Change and configuration management governs how the transition is executed; this standard governs whether the predecessor may be retired once it has.

## 9. Framework alignment

| Requirement | ISO/IEC 42001:2023 | NIST AI RMF 1.0 | ISO/IEC 20000-1:2018 | NIST SP 800-53 Rev 5 | CSA CCM v4.1 | ISO/IEC 27001:2022 |
| --- | --- | --- | --- | --- | --- | --- |
| Retirement and decommissioning governed as a lifecycle stage | A.6.2 | MANAGE 4.1 | 8.5.2 (service transition, including removal) | SR-12 | CCC-03 | A.8.32 |
| Successor outcome-consistency before supersession (novel; no framework mapping) | n/a | n/a | n/a | n/a | n/a | n/a |
| Impact analysis before the change is implemented | n/a | n/a | 8.5.2 | CM-4 | CCC-03 | A.8.32 |
| Retention of comparison evidence | n/a | n/a | n/a | n/a | DSP-16 | 7.5.3 |

Control identifiers are cited at the objective level; the paired documents in Related Documents carry the operational detail. The alignment is deliberately narrow, and the standard's core requirement, successor outcome-consistency, has no framework mapping at all, which reinforces its novelty. The mapped sources govern the surrounding activities: decommissioning as a lifecycle stage (ISO/IEC 42001 A.6.2 on the AI system life cycle; NIST AI RMF MANAGE 4.1, which names decommissioning within post-deployment monitoring; NIST SP 800-53 SR-12 on component disposal), service removal (ISO/IEC 20000-1 8.5.2), pre-change impact analysis (NIST SP 800-53 CM-4), and evidence retention (ISO/IEC 27001 7.5.3 on the retention and disposition of documented information). None prescribes a meaning-preserving comparison as a retirement precondition; see Limitations.

## 10. Limitations

The core requirement of this standard, a meaning-preserving comparison as a precondition of retiring a predecessor, is a corpus-novel organizational control. No held normative source prescribes it in these terms: the nearest anchors are NIST AI RMF MANAGE 2.4 (mechanisms to supersede or deactivate systems whose outcomes are inconsistent with intended use) and NIST SP 800-53 CM-4 (analyze changes for impact before implementation), both of which this standard exceeds rather than restates. The gate reduces, but does not eliminate, the risk of an undetected semantic change: a comparison is only as good as the representativeness of the cases it replays, and a divergence outside the sampled set can still escape. The standard governs the retirement precondition; it does not govern how the successor is designed or how the migration is executed, which the design, change-management, and portability controls in Related Documents own. Retirement without a successor is out of scope and is governed by the existing completeness and destruction controls.
