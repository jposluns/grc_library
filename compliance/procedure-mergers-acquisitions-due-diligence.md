# Mergers and Acquisitions Due Diligence Procedure

**Document Title:** Mergers and Acquisitions Due Diligence Procedure\
**Document Type:** Procedure\
**Version:** 1.0.1\
**Date:** 2026-06-30\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/procedure-grc-programme-management-and-annual-review.md`](../governance/procedure-grc-programme-management-and-annual-review.md), [`compliance/standard-internal-audit.md`](standard-internal-audit.md), [`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md), [`privacy/template-transfer-impact-assessment.md`](../privacy/template-transfer-impact-assessment.md), [`risk/procedure-risk-register.md`](../risk/procedure-risk-register.md), [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md), [`governance/register-role-authority.md`](../governance/register-role-authority.md)\
**Classification:** Public\
**Category:** Compliance Management\
**Review Frequency:** Annual and upon material change to deal-governance, regulatory, or integration practice\
**Repository Path:** [`compliance/procedure-mergers-acquisitions-due-diligence.md`](procedure-mergers-acquisitions-due-diligence.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose and scope

### 1.1 Purpose

This procedure operationalizes the governance, risk, and compliance (GRC) due diligence required when the organisation acquires, merges with, or takes a controlling interest in another entity. The [GRC Programme Management and Annual Review Procedure](../governance/procedure-grc-programme-management-and-annual-review.md) names a merger, acquisition, or divestiture as a major-organisational-change trigger for a programme review, but provides no transaction-level checklist, pre-close instrument, or integration playbook. This procedure is that instrument: it defines the phases, the GRC dimensions to assess, the deal-breaker escalation path, and the hand-off into the organisation's standing controls.

### 1.2 Scope

This procedure applies to the organisation's own inbound transactions (acquisitions, mergers, controlling investments). Divestitures are out of scope here: while they share several GRC dimensions, they require carve-out-specific handling (data segregation, records and obligation transfer-out, de-provisioning of the divested entity's access) that this version does not cover; run a divestiture through the triggered-review machinery with dimensions adapted to the carve-out. This procedure covers the GRC dimensions of due diligence; it does not replace the financial, tax, and commercial due diligence that the deal team and external advisers perform, and it does not constitute legal advice.

It is distinct from supplier change-of-control monitoring: where an existing supplier is itself acquired, the [Supplier Due Diligence Procedure](../supply-chain/procedure-supplier-due-diligence.md) and the fourth-party and nth-party risk procedure govern, not this procedure.

Deal-approval authority thresholds, materiality thresholds, due-diligence timelines, and the required regulatory-clearance list are organisation-specific and are populated by the adopting organisation; this procedure marks them as *[adopter-defined]* rather than asserting values.

## 2. Roles and responsibilities

| Role | Responsibility in the transaction |
| --- | --- |
| Executive sponsor / deal lead | Owns the transaction and the decision to proceed at each phase gate. |
| Chief Compliance Officer | Owns this procedure and the compliance dimension of due diligence; chairs the GRC due-diligence review. |
| GRC Programme Manager | Coordinates the multi-domain due-diligence review and the post-close hand-off into the triggered-review machinery. |
| Chief Information Security Officer | Owns the security-posture and incident-history assessment. |
| Data Protection Officer | Owns the privacy, data-protection, and data-transfer-inheritance assessment. |
| Chief Risk Officer | Owns the consolidated risk view and the red-flag and deal-breaker register; ensures that findings reach the risk register. |
| Legal Counsel | Owns the legal-entity, contracts, litigation, IP, and regulatory-clearance assessment. |
| Enterprise Risk Committee (ERC) | Reviews material findings and deal-breakers; advises the approving authority. |

The assignment above is the default; an adopting organisation maps these to its own role inventory per [`governance/register-role-authority.md`](../governance/register-role-authority.md).

## 3. Transaction phases

The due diligence runs across four phases, each with a decision gate. A transaction does not pass a gate until the GRC findings for that phase have been reviewed.

1. **Phase 1: screening and pre-LOI** (Section 4): a deal-breaker scan and scope-setting before a letter of intent.
2. **Phase 2: pre-close due diligence** (Sections 5 and 6): the full GRC-dimension review against the target's data room, producing the due-diligence checklist outcomes and the red-flag register.
3. **Phase 3: signing to close** (Section 7): conditions, covenants, representations and warranties, and regulatory clearances.
4. **Phase 4: post-close integration** (Section 8): the hand-off into the organisation's standing controls and the integration playbook.

## 4. Phase 1: Screening and pre-LOI

Before a letter of intent is signed:

1. Confirm the transaction crosses the *[adopter-defined]* materiality threshold that invokes this procedure.
2. Run a deal-breaker scan across the highest-severity dimensions: sanctions and financial-crime exposure, unresolved regulatory enforcement, a material unmanaged breach or incident history, and any prohibited-jurisdiction or prohibited-counterparty exposure.
3. Set the scope and timeline of the pre-close due diligence, and assign the dimension owners from Section 2.
4. Record the screening outcome and the decision to proceed to a letter of intent.

A deal-breaker identified at this phase is escalated immediately per Section 6 rather than deferred to the full review.

## 5. GRC due-diligence checklist (Phase 2)

For each dimension, the assigned owner assesses the target against the data room and records the finding, the supporting evidence, and a residual-risk rating. Each dimension cross-references the standing corpus instrument that governs it post-close.

| Dimension | What to assess | Governing corpus instrument |
| --- | --- | --- |
| Governance and legal entity | Board and ownership structure, delegation of authority, subsidiaries, and beneficial ownership. | [`governance/register-role-authority.md`](../governance/register-role-authority.md) |
| Regulatory and licensing | Applicable regimes, licences held, open enforcement actions, and notification or approval obligations triggered by the change of control. | [`compliance/policy-legal-and-regulatory-compliance.md`](policy-legal-and-regulatory-compliance.md) |
| Privacy and data protection | Lawful bases relied on, consent inheritance, records of processing, and open data-subject-rights or breach matters. | [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`privacy/framework-consent-management.md`](../privacy/framework-consent-management.md) |
| Cross-border data transfers | Whether the target relies on restricted transfers and whether each has a valid mechanism and assessment that survive the transaction. | [`privacy/template-transfer-impact-assessment.md`](../privacy/template-transfer-impact-assessment.md), [`privacy/register-cross-border-data-flow.md`](../privacy/register-cross-border-data-flow.md) |
| Security posture and incident history | Control maturity, known vulnerabilities, and the history and handling of security incidents and breaches. | [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) |
| Compliance obligations and findings | The target's obligation inventory and any open corrective actions or audit findings. | [`compliance/procedure-capa.md`](procedure-capa.md), [`compliance/standard-internal-audit.md`](standard-internal-audit.md) |
| Contracts and third-party risk | Material contracts, change-of-control clauses, and inherited supplier and third-party risk. | [`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md) |
| Financial-crime and sanctions exposure | Sanctions, export-control, anti-bribery, and money-laundering exposure of the target, its owners, and its counterparties. | [`compliance/standard-sanctions-and-export-control-screening.md`](standard-sanctions-and-export-control-screening.md); [`supply-chain/procedure-fourth-party-and-nth-party-risk.md`](../supply-chain/procedure-fourth-party-and-nth-party-risk.md) for supplier-tier exposure |
| Intellectual property and data assets | Ownership and encumbrance of IP and key data assets, including AI models and training data where relevant. | [`ai/register-ai-risk.md`](../ai/register-ai-risk.md) (and adopter IP records) |
| Human capital and conduct | Key-person dependency, conduct and ethics matters, and culture-integration risk. | [`governance/framework-human-capital-and-ethical-conduct.md`](../governance/framework-human-capital-and-ethical-conduct.md) |
| Technology and integration | Architecture compatibility, technical debt, and the effort and risk of integration. | [`architecture/procedure-architecture-review.md`](../architecture/procedure-architecture-review.md), [`operations/procedure-change-management-and-configuration-control.md`](../operations/procedure-change-management-and-configuration-control.md) |
| Litigation and liabilities | Pending or threatened litigation, contingent liabilities, and indemnities. | (adopter legal records; feeds the risk register) |
| Records and data-room handling | Classification and protection of the due-diligence data room itself, which typically contains the target's most sensitive material. | [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md), [`security/standard-data-loss-prevention.md`](../security/standard-data-loss-prevention.md) |

## 6. Red-flag and deal-breaker register

Findings that may alter or stop the transaction are recorded here and escalated; the register travels with the deal and feeds the [risk register](../risk/procedure-risk-register.md).

| Field | Content |
| --- | --- |
| Finding | The red flag, with its dimension from Section 5. |
| Severity | Deal-breaker / material / monitor. |
| Basis and evidence | The data-room evidence and the assessment supporting the rating. |
| Escalation | Deal-breaker and material findings are escalated to the Chief Risk Officer and the Enterprise Risk Committee; deal-breakers are escalated to the executive sponsor before any further commitment. |
| Disposition | Withdraw / re-price or restructure / accept with conditions / accept with a post-close remediation plan. |

A deal-breaker is not closed by acceptance alone: it is resolved by withdrawal, by a restructure that removes it, or by an explicit, authority-level risk acceptance recorded against the organisation's risk appetite.

## 7. Phase 3: Signing to close

Between signing and closing:

1. Capture the GRC-relevant conditions to closing (for example regulatory clearances, consents to assignment, and remediation of deal-breakers).
2. Capture the representations, warranties, and indemnities that allocate the GRC risks identified in Phase 2.
3. Track interim covenants that constrain the target's conduct between signing and closing.
4. Confirm that all *[adopter-defined]* regulatory clearances and change-of-control notifications are obtained or filed before closing.
5. Re-confirm the deal-breaker register is resolved or its residual risk is accepted at the appropriate authority before closing.

## 8. Phase 4: Post-close integration and hand-off

On closing, the transaction hands off into the organisation's standing controls:

1. **Invoke the triggered review.** Record the completed transaction as a major-organisational-change trigger in the [GRC Programme Management and Annual Review Procedure](../governance/procedure-grc-programme-management-and-annual-review.md), which assigns owners and a completion window for bringing the acquired entity into the programme.
2. **Schedule the post-close audit.** The [Internal Audit Standard](standard-internal-audit.md) provides for an audit of the affected domains following a significant organisational change; schedule it within that window.
3. **Migrate findings into the risk register.** Open Phase 2 findings and accepted residual risks are recorded in the [risk register](../risk/procedure-risk-register.md) with owners and target dates.
4. **Integrate the GRC artefacts.** Bring the acquired entity's records of processing, supplier inventory, obligation inventory, and incident history into the organisation's corresponding registers; re-run the relevant assessments (for example a [Transfer Impact Assessment](../privacy/template-transfer-impact-assessment.md) for any inherited restricted transfer) where the change of control affects their validity.
5. **Close the integration playbook.** Track the integration actions to completion and confirm the acquired entity is operating within the organisation's governance, risk, and compliance framework.

## 9. Evidence and records

The due-diligence checklist outcomes, the red-flag and deal-breaker register, the signing-to-close conditions, and the post-close integration record are retained as the evidence of the GRC due diligence, per the [records retention and destruction standard](../governance/standard-records-retention-and-destruction.md). The data room and the populated due-diligence artefacts are themselves sensitive (they contain the target's most confidential material) and are classified and protected accordingly; access is restricted to the deal team and the dimension owners.

## 10. Related documents

- [`governance/procedure-grc-programme-management-and-annual-review.md`](../governance/procedure-grc-programme-management-and-annual-review.md): the triggered-review machinery this procedure feeds on close.
- [`compliance/standard-internal-audit.md`](standard-internal-audit.md): the post-close audit of affected domains.
- [`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md): the sibling due-diligence procedure for suppliers, and the governing instrument where an existing supplier is acquired.
- [`privacy/template-transfer-impact-assessment.md`](../privacy/template-transfer-impact-assessment.md): the instrument for inherited restricted transfers.
- [`risk/procedure-risk-register.md`](../risk/procedure-risk-register.md): the destination for accepted and open findings.

## 11. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO 31000:2018 | Risk management principles and guidelines | The risk-assessment discipline applied to the transaction. |
| ISO 37301:2021 | Compliance management systems | The compliance-obligation and regulatory dimensions of due diligence. |
| COBIT 2019 | EDM03 (ensured risk optimization), APO12 (managed risk), BAI05 (managed organizational change) | Governance of transaction risk and the post-close organizational change. |
| NIST CSF 2.0 | GV (Govern) function | Governance and risk-management outcomes assessed and integrated through the transaction. |

## 12. Limitations

This procedure is a CC BY-SA 4.0 baseline. It is not legal, financial, or tax advice, and it does not replace the transaction-specific due diligence performed by the deal team and external advisers. Adopting organisations must populate the materiality and approval thresholds, the regulatory-clearance list, and the timelines marked *[adopter-defined]*, and must extend the intellectual-property and litigation dimensions with their own records where this library has no dedicated instrument. The financial-crime and sanctions dimension (the lead deal-breaker in Phase 1) is governed by the [sanctions and export-control screening standard](standard-sanctions-and-export-control-screening.md), with the fourth-party and nth-party risk procedure covering supplier-tier exposure.

---

**End of Document**
