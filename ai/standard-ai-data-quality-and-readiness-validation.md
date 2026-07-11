# AI Data Quality and Readiness Validation Standard

**Document Title:** AI Data Quality and Readiness Validation Standard\
**Document Type:** Standard\
**Version:** 0.0.1\
**Date:** 2026-07-11\
**Owner:** AI Data Steward\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/procedure-training-data-governance.md`](procedure-training-data-governance.md), [`ai/template-dataset-datasheet.md`](template-dataset-datasheet.md), [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md), [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md), [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material data, model, or regulatory change\
**Repository Path:** [`ai/standard-ai-data-quality-and-readiness-validation.md`](standard-ai-data-quality-and-readiness-validation.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard sets the measurable data-quality requirements and the readiness sign-off gate that a dataset must satisfy before it is used to train, fine-tune, evaluate, or operate an AI system at scale. It owns the data-quality model, the measures and targets, and the data-use approval that the training-data governance procedure, the dataset datasheet, and the AI System Register reference.

It does not restate the data-lifecycle steps of the [training-data governance procedure](procedure-training-data-governance.md) or the field layout of the [dataset datasheet](template-dataset-datasheet.md); it defines the acceptance criteria and the sign-off gate those instruments record against. The requirements are organization-neutral and rest on the ISO/IEC 5259 data-quality series, the ISO/IEC 8183 data life cycle framework, and the data-quality provisions of ISO/IEC 42005:2025; adopters map them to their own tooling and risk tolerance.

## 2. Applicability

This standard applies to every dataset that materially feeds an AI system: training, fine-tuning, reinforcement, evaluation, and retrieval-augmentation corpora, and any dataset whose quality bears on a decision the system makes. It applies at initial dataset assembly and at each material data refresh. The depth of validation is proportionate to the system's impact level (see the [AI System Impact Assessment Procedure](procedure-ai-system-impact-assessment.md) Step 7): a higher impact level warrants tighter acceptance targets and a more independent readiness sign-off.

## 3. Requirements

### 3.1 Adopt a data-quality model

For each in-scope dataset, select the data-quality characteristics that apply to its context and record why, adopting the data-quality model of ISO/IEC 5259-2:2024 (Clause 5 and Clause 6). ISO/IEC 5259-2 organizes its data-quality characteristics into four groups (inherent; inherent and system-dependent; system-dependent; and additional characteristics for analytics and machine learning), 23 characteristics in total; an organization selects the subset relevant to the dataset's use rather than asserting all of them. The selected characteristics, and the rationale for the selection, are documented against the dataset.

### 3.2 Define measures, targets, and results

For each selected characteristic, define one or more data-quality measures, a target value for each measure, and record the measured result, following the reporting structure of ISO/IEC 5259-2:2024 Clause 8: the data-quality model, the selected measures and their target values, the results, an assessment of whether the dataset meets its data-quality requirements, and a plan for improvement where it does not. Acceptance criteria may be quantitative or qualitative (ISO/IEC 5259-2:2024 Clause 5). A dataset that does not meet its targets carries a documented improvement plan and does not pass the readiness gate (Section 3.7) until the plan is executed or the residual risk is formally accepted.

### 3.3 Maintain a data-quality plan and run the process loop

Maintain a data-quality plan for each project, referenced in the project plan, that plans the activities for achieving data quality and is reviewed and updated regularly (ISO/IEC 5259-3:2024 Clause 12.6). Run the data-quality process loop of ISO/IEC 5259-4:2024 Clause 6 across the data life cycle: plan the data-quality management, evaluate quality against the targets, improve the data where it falls short, and validate that the data-quality processes ensure that the data meet requirements, feeding results back into improvement.

### 3.4 Verify and validate at each life-cycle stage

Apply the verification and validation quality gates of ISO/IEC 5259-3:2024 Clause 8.3: each data life-cycle stage specifies objectively assessable quality targets for its work products, and a stage is entered only with verified and validated input. Verification establishes objective evidence that the data-quality requirements have been met; validation establishes that the data meet the intended objectives. The results of verification and validation are documented. Align the life-cycle stages to the ten-stage AI data life cycle of ISO/IEC 8183:2023 Clause 5.

### 3.5 Set acceptance criteria and control labelling quality

Set the acceptance criteria for the dataset from Section 3.2's targets. Where the dataset is labelled, control the labelling quality per ISO/IEC 5259-4:2024 Clause 8.4: inspect labelled data against the acceptance criteria, return failing samples to the annotator, and set the inspection proportion and method (for example, reviewing a sample proportion of the labelled data for a lower-risk task, or full inspection for a higher-risk one), with stricter inspection for outsourced or crowdsourced labelling. Where a statistical acceptance-sampling scheme is used, ISO/IEC 5259-4:2024 references the acceptance-quality-limit sampling scheme of ISO 2859-1 for selecting sample sizes; adopt that scheme by reference where lot-by-lot inspection is appropriate.

### 3.6 Assure supply-chain data quality

Where data is acquired from a supplier, apply the supply-chain data-quality requirements of ISO/IEC 5259-3:2024 Clause 9: state the data and quality requirements in the request for quotation, and record a development-interface agreement that assigns the data-quality management activities, the shared work products, the qualitative and quantitative benchmark requirements, auditor access, and decommissioning responsibilities between the organization and the supplier. Retain the supplier-selection report, the development-interface agreement, and the quality-assessment report.

### 3.7 Record the readiness sign-off gate

Before a dataset is used to train, fine-tune, or operate an AI system at scale, an appropriate set of stakeholders approves the use of the data for the specified context (the data-use approval of ISO/IEC 5259-4:2024 Clause 6, and the approved use of the dataset by appropriate interested parties documented per ISO/IEC 42005:2025 Clause 6.4.3). The approval, its conditions, and the approving stakeholders are recorded against the `Data Quality Validation Status` field of the [AI System Register](template-ai-system-register.md). A dataset that has not passed this gate is not used at scale.

### 3.8 Decommission data-quality artefacts

When a dataset is retired, decommission it per ISO/IEC 8183:2023 Clause 6.10 and ISO/IEC 5259-3:2024 Clause 12.9: dispose of data no longer used (secure deletion, archiving, or repurposing), retain the categories required for audit (for example, records proving compliance), and decommission the model itself where it retains residual elements of the training data or where security, privacy, licensing, or legal requirements demand it. Record the decommissioning decision and its basis.

## 4. Evidence requirements

- The selected data-quality model and the rationale for the characteristic selection (Section 3.1).
- The data-quality report: measures, target values, results, the meets-requirements assessment, and any improvement plan (Section 3.2).
- The data-quality plan and the process-loop records (Section 3.3).
- The verification and validation results per life-cycle stage (Section 3.4).
- The labelling-inspection record, where applicable (Section 3.5).
- The supplier selection report, development-interface agreement, and quality-assessment report, where data is acquired externally (Section 3.6).
- The readiness sign-off record, referenced from the AI System Register (Section 3.7).
- The decommissioning record (Section 3.8).

## 5. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 5259-2:2024 | Clause 5 (model); Clause 6 (characteristics); Clause 8 (measures, targets, reporting) | Data-quality model, measures, and reporting (Sections 3.1, 3.2) |
| ISO/IEC 5259-3:2024 | Clause 8.3 (verification and validation gates); Clause 9 (supply chain); Clause 12.6 (data-quality plan); Clause 12.9 (decommissioning) | Data-quality management, life-cycle gates, and supply chain (Sections 3.3, 3.4, 3.6, 3.8) |
| ISO/IEC 5259-4:2024 | Clause 6 (process loop and data-use approval); Clause 8.4 (labelling quality control) | Process loop, readiness sign-off, and labelling QA (Sections 3.3, 3.5, 3.7) |
| ISO/IEC 8183:2023 | Clause 5 (data life cycle stages); Clause 6.10 (data decommissioning) | Life-cycle alignment and decommissioning (Sections 3.4, 3.8) |
| ISO/IEC 42005:2025 | Clause 6.4.3 (data-quality documentation and approved use) | Readiness sign-off and impact-assessment hook (Section 3.7) |
| ISO 2859-1 | Acceptance-quality-limit sampling scheme (referenced by ISO/IEC 5259-4:2024) | Acceptance sampling for labelling inspection (Section 3.5) |
| EU AI Act (2024) | Article 10: data and data governance | Training, validation, and testing data-quality obligations for high-risk AI |
| ISO/IEC 42001:2023 | Clause 8.4 | Operational data controls in the AI management system |

## 6. Limitations

This standard is original library content. It does not reproduce the text of the ISO/IEC standards it cites; adopters consult the source standards for the full requirements. The acceptance-quality-limit sampling detail is defined by ISO 2859-1, which this library does not hold; where an adopter needs the specific sampling schemes, consult ISO 2859-1 directly. The data-quality characteristics and their measures are selected per context; this standard sets the process, not a fixed universal target, because acceptance targets are properly a function of the dataset's use and the system's impact level.

---

**End of Document**
