# AI Assurance Evidence and Attestation Framework

**Document Title:** AI Assurance Evidence and Attestation Framework\
**Document Type:** Framework\
**Version:** 1.0.0\
**Date:** 2026-09-05\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md), [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md), [`ai/procedure-ai-evaluation.md`](procedure-ai-evaluation.md), [`ai/standard-ai-model-risk.md`](standard-ai-model-risk.md), [`ai/procedure-ai-audit.md`](procedure-ai-audit.md), [`ai/framework-ai-model-documentation-and-transparency.md`](framework-ai-model-documentation-and-transparency.md), [`ai/template-ai-red-team-report.md`](template-ai-red-team-report.md), [`ai/template-model-card.md`](template-model-card.md), [`ai/template-system-card.md`](template-system-card.md), [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`ai/matrix-etsi-sai-baseline-alignment.md`](matrix-etsi-sai-baseline-alignment.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI governance or regulatory change\
**Repository Path:** [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose and scope

### 1.1 Purpose

This framework defines the assurance-evidence and attestation model for AI systems: the claim taxonomy, evidence classes, attestation tiers, and sufficiency criteria by which the organization organizes the outputs of its existing assurance activities into a standing, audit-ready evidence base across the AI lifecycle. Its object is the evidence, not the activity that produces it: it indexes, grades, and marshals what the assurance activities already generate so that any assurance claim about an AI system can be traced to the artefacts that support it, at a known weight and currency, on demand.

### 1.2 Scope

The framework applies to every AI system recorded in the AI System Register, to all evidence produced by the assurance activities the corpus already defines, and to evidence received from third parties (developers, providers, and independent assessors). It defines the model for organizing that evidence; it does not define or restate any assurance activity. Testing and validation requirements remain owned by [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md), the evaluation process by [`ai/procedure-ai-evaluation.md`](procedure-ai-evaluation.md), adversarial evaluation by [`ai/guideline-adversarial-evaluation-suite-development.md`](guideline-adversarial-evaluation-suite-development.md) and [`ai/guide-ai-adversarial-test-reference.md`](guide-ai-adversarial-test-reference.md), red-team reporting by [`ai/template-ai-red-team-report.md`](template-ai-red-team-report.md), and model-risk requirements by [`ai/standard-ai-model-risk.md`](standard-ai-model-risk.md). The framework is the evidence-marshalling counterpart to [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md), which owns the independent-assessment side (the audit programme, tier frequencies, the certification pathway, and the per-tier evidence catalogue an audit demands at audit time): this framework keeps that catalogue satisfiable on demand, and the assurance cases it maintains are what an audit under that framework consumes. Where [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md) names a one-line evidence class per lifecycle stage, this framework elaborates those classes into the full evidence model without altering the lifecycle itself.

## 2. Governance

### 2.1 AI System Owner: assurance-case custodian

The AI System Owner produces and maintains the assurance case for each system they own: the claims-by-evidence record described in section 3.5, kept current across the lifecycle and marshalled into an evidence pack ahead of each approval or audit gate.

### 2.2 CISO: evidence-model owner

The Chief Information Security Officer owns this framework: the claim taxonomy, the evidence classes, the attestation tiers, and the sufficiency criteria. The CISO adjudicates borderline tier and sufficiency determinations and maintains the evidence-to-activity index in section 4 as the referenced documents evolve.

### 2.3 AI Governance Council: consumer at the gates

The AI Governance Council consumes assurance cases at deployment-approval and periodic-review gates, and refers a system whose assurance case shows an undocumented gap on a material claim back to its owner before the gate is cleared.

## 3. The assurance evidence and attestation model

### 3.1 Assurance claims

An assurance claim is a bounded assertion about an AI system that evidence can support or refute. The claim taxonomy is keyed to the NIST AI RMF (NIST AI 100-1) MEASURE 2 subcategories, with two organizational claims the corpus lifecycle adds. Each claim is discharged by evidence marshalled under sections 3.2 to 3.4, never by the presence of this framework.

| Claim | Assertion | NIST AI RMF anchor |
| --- | --- | --- |
| Valid and reliable | The system is demonstrated to be valid and reliable, and the limitations of its generalizability are documented | MEASURE 2.5 |
| Safe | The system is demonstrated to be safe, its residual negative risk does not exceed the risk tolerance, and it can fail safely | MEASURE 2.6 |
| Secure and resilient | The system's security and resilience are evaluated and documented | MEASURE 2.7 |
| Transparent and accountable | The risks associated with transparency and accountability are examined and documented | MEASURE 2.8 |
| Explainable | The model is explained, validated, and documented | MEASURE 2.9 |
| Privacy-preserving | The privacy risk of the system is examined and documented | MEASURE 2.10 |
| Fair | Fairness and bias are evaluated and the results are documented | MEASURE 2.11 |
| Monitored in operation | Functionality and behaviour are monitored in production | MEASURE 2.4 (with MEASURE 3.1) |
| Governed and approved | Accountable ownership, approvals, and oversight are in place | Corpus lifecycle model (Approval stage) |

### 3.2 Evidence classes

Evidence is organized into seven artefact classes, each produced by an activity the corpus already owns and none produced by this framework:

- **Design evidence**: model cards, system cards, threat models, and architecture records.
- **Test and evaluation evidence**: test plans and results, evaluation reports, and adversarial-suite execution records.
- **Independent-assessment evidence**: internal audit reports, third-party red-team reports, and certification and conformity records.
- **Review and approval evidence**: approval records, exception records, and governance-council minutes.
- **Operational evidence**: monitoring logs, drift metrics, and incident records.
- **Attestations**: control-owner attestations, deletion or retention attestations, and supplier declarations.
- **Received third-party evidence**: developer-shared testing and evaluation findings, provider transparency documentation, and vendor questionnaire responses. This class is anchored to ETSI EN 304 223 provision 5.2.5-3, under which developers ensure that the findings from testing and evaluation are shared with system operators to inform the operators' own testing and evaluation.

### 3.3 Attestation tiers

The attestation tier records evidence weight by the independence of its producer. The tiers grade weight; they do not substitute for one another.

| Tier | Producer | Basis |
| --- | --- | --- |
| A | Independent third party: accredited certification body, external red team, or external auditor | Highest weight; fully independent of development and operation |
| B | Internally independent assessor: internal experts who did not serve as front-line developers, or independent internal security testers | NIST AI RMF MEASURE 1.3; ETSI EN 304 223 provision 5.2.5-2.1 |
| C | First-party test and evaluation by the developing or operating team, with method documentation | NIST AI RMF MEASURE 2.1 (test sets, metrics, and tools documented) |
| D | Self-attestation and declaration | Lowest weight; the producer asserts the fact without an assessment |

A Tier A certificate does not discharge a claim that has no underlying Tier C test and evaluation evidence, and a Tier D attestation alone never discharges a high-risk claim.

### 3.4 Sufficiency criteria

Evidence supporting a claim is sufficient when it satisfies five dimensions:

- **Coverage**: the claim's scope is measured, and any risk or trustworthiness characteristic that will not or cannot be measured is documented (NIST AI RMF MEASURE 1.1).
- **Currency**: the evidence was produced within the review window for the system's risk tier and re-produced on material change, per the thresholds in [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md).
- **Independence**: the attestation tier meets the minimum the system's risk tier requires (section 5).
- **Method traceability**: the test sets, metrics, and tools are documented (NIST AI RMF MEASURE 2.1).
- **Deployment-representative demonstration**: performance or assurance criteria are measured and demonstrated for conditions similar to the deployment setting, and the measures are documented (NIST AI RMF MEASURE 2.3).

### 3.5 The assurance case

The assurance case for a system is a claims-by-evidence record maintained by the AI System Owner across the eleven lifecycle stages of the governance framework's lifecycle model (Intake through Retirement, reused as defined there). For each claim it records the supporting artefacts, their evidence class, their attestation tier, their currency, and any documented gap. The marshalled assurance case is the pack that satisfies the section 4 evidence catalogue of [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md) and the evidence-collection step of [`ai/procedure-ai-audit.md`](procedure-ai-audit.md). The effectiveness of the evidence-producing processes is itself evaluated and documented (NIST AI RMF MEASURE 2.13), so the assurance case is periodically tested against the activities that feed it, not only assembled from them.

## 4. Evidence-to-activity index

Each row maps a claim and evidence class to the corpus document whose activity produces that evidence. The rows are pointers only: each artefact's requirements live in the linked document, and this framework restates none of them.

| Claim | Evidence class | Producing activity | Artefact |
| --- | --- | --- | --- |
| Valid and reliable | Test and evaluation | [`standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md); [`procedure-ai-evaluation.md`](procedure-ai-evaluation.md) | Functional validation results; evaluation report |
| Safe | Test and evaluation; operational | [`procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md); [`standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md) | Impact assessment; monitoring outputs |
| Secure and resilient | Test and evaluation; independent assessment | [`guideline-adversarial-evaluation-suite-development.md`](guideline-adversarial-evaluation-suite-development.md); [`guide-ai-adversarial-test-reference.md`](guide-ai-adversarial-test-reference.md); [`template-ai-red-team-report.md`](template-ai-red-team-report.md); [`standard-ai-model-risk.md`](standard-ai-model-risk.md) | Security test results; suite execution records; red-team report |
| Transparent and accountable | Design; attestation | [`framework-ai-model-documentation-and-transparency.md`](framework-ai-model-documentation-and-transparency.md); [`template-model-card.md`](template-model-card.md); [`template-system-card.md`](template-system-card.md) | Model card; system card; transparency disclosures |
| Explainable | Test and evaluation; design | [`standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md); [`procedure-ai-evaluation.md`](procedure-ai-evaluation.md) | Explainability validation output |
| Privacy-preserving | Test and evaluation | [`procedure-integrated-ai-and-privacy-assessment.md`](procedure-integrated-ai-and-privacy-assessment.md); [`standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md) | Privacy test results; integrated assessment |
| Fair | Test and evaluation | [`standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md); [`procedure-ai-evaluation.md`](procedure-ai-evaluation.md) | Bias and fairness results |
| Monitored in operation | Operational | [`standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md); [`plan-ai-incident-response.md`](plan-ai-incident-response.md); [`register-ai-risk.md`](register-ai-risk.md) | Monitoring logs; incident records |
| Governed and approved | Review and approval; attestation | [`framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md); [`charter-ai-governance-council.md`](charter-ai-governance-council.md); [`standard-ai-human-oversight.md`](standard-ai-human-oversight.md) | Approval records; oversight records; control-owner attestations |
| All claims (data foundation) | Design | [`procedure-training-data-governance.md`](procedure-training-data-governance.md); [`standard-ai-data-quality-and-readiness-validation.md`](standard-ai-data-quality-and-readiness-validation.md); [`template-dataset-datasheet.md`](template-dataset-datasheet.md) | Data provenance and quality records |
| All claims (independent verification) | Independent assessment | [`framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md); [`procedure-ai-audit.md`](procedure-ai-audit.md) | Audit reports; certification and conformity records |
| All claims (third-party systems) | Received third-party | [`template-ai-vendor-security-questionnaire.md`](template-ai-vendor-security-questionnaire.md); [`procedure-foundation-model-lifecycle.md`](procedure-foundation-model-lifecycle.md) | Questionnaire responses; developer-shared findings (ETSI EN 304 223 provision 5.2.5-3) |
| Model-risk composite | Multiple | [`standard-ai-model-risk.md`](standard-ai-model-risk.md) | The model-risk evidence list, placed into the classes above |

## 5. Requirements

The framework adds only the small set of normative requirements below; every other requirement lives in the indexed documents.

1. **Evidence-record minimum fields.** Each evidence record must carry: the AI System Register reference; the claim or claims it supports; its evidence class and attestation tier; the producing activity (a corpus document reference); a method reference; a production date and currency window; the lifecycle stage; a storage location and integrity control; and any documented gaps or unmeasured aspects.
2. **Gap documentation.** A claim that lacks sufficient evidence must carry a documented gap in the assurance case, stating what is missing and the plan to close it; an undocumented gap on a material claim blocks the approval or audit gate.
3. **Currency by risk tier.** Evidence for a high-risk system must be current within that system's review window and re-produced on material change; the windows are those the governance framework sets per risk tier.
4. **Independence minimum for high-risk security evidence.** Security and resilience evidence for a high-risk system must reach at least attestation Tier B (an internally independent assessor), consistent with ETSI EN 304 223 provision 5.2.5-2.1.
5. **Marshalling obligation.** The AI System Owner must marshal the assurance case into an evidence pack before each deployment-approval and audit gate, so the demand-side catalogue of the audit-certification framework is satisfiable without ad-hoc collection.

## 6. Framework alignment

| Framework | Reference point | Relevance |
| --- | --- | --- |
| NIST AI 100-1 (AI RMF 1.0) | MEASURE 2.1, 2.3, 2.5, 2.13 | Documented TEVV evidence, deployment-representative demonstration, validity demonstration, and meta-evaluation of the TEVV processes: the core of the evidence model |
| NIST AI 100-1 (AI RMF 1.0) | MEASURE 1.1, 1.3 | Documentation of unmeasured risks (gap documentation) and independent assessors (attestation tiers) |
| NIST AI 100-1 (AI RMF 1.0) | MEASURE 2.4, 3.1 | In-production monitoring evidence and risk-tracking documentation |
| ETSI EN 304 223 V2.1.1 | Provisions 5.2.5-2.1, 5.2.5-3 | Independent security testers (attestation tier minimum) and developer-to-operator findings transfer (received third-party evidence class) |
| ISO/IEC 42001:2023 | Clause 9 (performance evaluation) | The management-system performance-evaluation activity that consumes the marshalled evidence at certification; see-also, not a control mapping |

## 7. Limitations

Organizing assurance evidence does not itself establish assurance: an assurance case is only as strong as the underlying activities that produce its evidence, and a complete index over weak evidence is not a strong claim. The framework does not reproduce the requirements, control text, or evidence catalogues of the documents it indexes, and it does not perform any assurance activity. It does not create legal or regulatory compliance by itself. Adopters validate applicability to their own AI systems, risk tiers, and regulatory context before relying on the model.
