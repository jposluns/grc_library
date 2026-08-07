# What the governing body should require for AI data governance and classification

**Document Title:** What the governing body should require for AI data governance and classification\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-08-07\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/standard-ai-security-and-risk.md`](../../ai/standard-ai-security-and-risk.md), [`security/standard-data-classification-and-handling.md`](../../security/standard-data-classification-and-handling.md), [`ai/procedure-training-data-governance.md`](../../ai/procedure-training-data-governance.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/briefs/brief-ai-data-governance-and-classification.md`](brief-ai-data-governance-and-classification.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Executive Brief\
**Narrative Status:** Explanatory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`ai/standard-ai-security-and-risk.md`](../../ai/standard-ai-security-and-risk.md), [`security/standard-data-classification-and-handling.md`](../../security/standard-data-classification-and-handling.md), [`ai/procedure-training-data-governance.md`](../../ai/procedure-training-data-governance.md), [`privacy/policy-privacy-and-data-governance.md`](../../privacy/policy-privacy-and-data-governance.md), [`ai/standard-ai-data-quality-and-readiness-validation.md`](../../ai/standard-ai-data-quality-and-readiness-validation.md), [`ai/template-dataset-datasheet.md`](../../ai/template-dataset-datasheet.md), [`governance/register-data-retention-schedule.md`](../../governance/register-data-retention-schedule.md), [`privacy/register-cross-border-data-flow.md`](../../privacy/register-cross-border-data-flow.md), [`ai/standard-ai-access-and-agent-permissions.md`](../../ai/standard-ai-access-and-agent-permissions.md), [`ai/guide-ai-board-oversight.md`](../../ai/guide-ai-board-oversight.md), [`architecture/standard-data-architecture.md`](../../architecture/standard-data-architecture.md), [`ai/procedure-integrated-ai-and-privacy-assessment.md`](../../ai/procedure-integrated-ai-and-privacy-assessment.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-004\
**Last Reviewed:** 2026-08-07

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Why this matters

Every AI system the organization operates is built on data, and the corpus makes the data question one of the governing body's own oversight questions: what data the organization's AI uses, under what authority, and how its quality and provenance are governed (the [board oversight guide](../../ai/guide-ai-board-oversight.md), its section 5). The [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) places classification at the front of the data lifecycle: it requires that data used by an AI system is classified before use and that its provenance and lineage are documented (its section 4.2).

The governing body does not classify datasets or run pipelines. Its oversight is a dependency on management operating the data governance layer the corpus defines, and on management producing the evidence that each control exists and operates. This brief points to where the corpus places each control; the division of labour it describes is a composite reading, and the limitations say so.

## What the corpus establishes

- **Classification comes before use.** The [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) requires that data used by an AI system is classified before use, that provenance is documented across training, retrieval, prompt, inference, and monitoring data, that lineage identifies source through to deletion method, and that sensitive data is not used unless authorized, risk-assessed, and controlled (its section 4.2).
- **AI data has a handling floor.** The [data classification and handling standard](../../security/standard-data-classification-and-handling.md) defines the organization's classification levels (its section 4) and sets the handling floor for AI datasets, model artefacts, and logs by reference to those levels (its section 7). It also assigns oversight of AI dataset classification to the governance roles it names (its section 3). This brief points to the standard for the levels, the floor, and the named roles, and does not reproduce them.
- **Classification travels with the data.** The [data classification and handling standard](../../security/standard-data-classification-and-handling.md) states that AI-derived data inherits the classification of its source unless explicitly reclassified (its section 5), and the [data architecture standard](../../architecture/standard-data-architecture.md) has classification tags propagate with data through transformation and marks data unsuitable for AI prompts or training as AI-sensitive (its section 5).
- **Training data has its own lifecycle procedure.** The [training data governance procedure](../../ai/procedure-training-data-governance.md) records each dataset's source and lawful basis (its Step 1), requires sensitive-content removal before training (its Step 2), places an approval gate before any training pipeline consumes a dataset, with the approving roles it names (its Step 4), records lineage for each training event (its Step 5), and defines how deletion propagates from a dataset to the models derived from it (its Step 6).
- **Policy backs the procedure.** The [privacy and data governance policy](../../privacy/policy-privacy-and-data-governance.md) requires that all data assets are classified (its section 4.2), that AI models are trained only on datasets meeting privacy, consent, and licensing obligations with provenance metadata (its section 4.7), that retention schedules cover AI training artifacts (its section 4.4), and that privacy impact assessments cover AI model training activities (its section 4.5).
- **Quality is gated, not asserted.** The [AI data quality and readiness validation standard](../../ai/standard-ai-data-quality-and-readiness-validation.md) records a readiness sign-off before a dataset trains or operates an AI system at scale; a dataset that has not passed the gate is not used at scale, and a dataset that misses its targets carries an improvement plan before it can pass (its sections 3.2 and 3.7).
- **Every dataset is documented.** The [dataset datasheet template](../../ai/template-dataset-datasheet.md) is required for every dataset in the AI System Register; a datasheet is produced before a dataset is used and updated on material change (its Purpose and Operating expectations sections).
- **Retention and cross-border movement are governed by registers.** The [data retention schedule](../../governance/register-data-retention-schedule.md) carries the retention rows for AI governance records, including training data provenance and AI decision logs (its section 7); the periods live there and only there. The [cross-border data flow register](../../privacy/register-cross-border-data-flow.md) documents transfers of personal data across jurisdictions, and maintaining it is a policy requirement (the [privacy and data governance policy](../../privacy/policy-privacy-and-data-governance.md), its section 4.6).
- **Access rules follow the data into retrieval.** The [AI access and agent permissions standard](../../ai/standard-ai-access-and-agent-permissions.md) binds retrieval scope to the user's identity, applies source-document access control to embedding stores, and propagates deletion and restriction into embeddings (its section 7). This is a prevention against an AI system becoming a route around the organization's data access controls.
- **The assessments are routed, not improvised.** The [integrated AI and privacy assessment procedure](../../ai/procedure-integrated-ai-and-privacy-assessment.md) determines, from a system's regime triggers, which data protection and AI assessments are required and how they compose (its Step 3).

## What this means for the organization

For the governing body and accountable executive leadership, the corpus position reads as follows. (This reading is a composite of the sources above; see the limitations.)

- **The governing body requires the layer, management operates it.** The [board oversight guide](../../ai/guide-ai-board-oversight.md) has the governing body set appetite and policy direction while management operates within it (its section 4). Applied to data, the governing body's contribution is to require that classification, lineage, quality gating, retention, and access control exist as the corpus defines them, and to ask for the evidence that they operate.
- **Dataset gates sit beneath the system gate.** The corpus places dataset-level controls (the approval to train, the readiness sign-off, the datasheet) before any system that consumes the data reaches its own production decision. A system-level approval built on ungoverned data answers the wrong question first.
- **Some answers are weak answers.** A quality claim without the recorded readiness sign-off the [AI data quality and readiness validation standard](../../ai/standard-ai-data-quality-and-readiness-validation.md) defines is an assertion, not evidence. A retention answer that does not resolve to the [data retention schedule](../../governance/register-data-retention-schedule.md) leaves the periods unowned. And a claim that retrieval "only sees what the user can see" is checkable against the specific controls in the [AI access and agent permissions standard](../../ai/standard-ai-access-and-agent-permissions.md) (its section 7).
- **The values stay in the corpus.** Classification levels, retention periods, approval roles, and assessment triggers are corpus values. The governing body should expect management's answers to point into those documents rather than restate them from memory, for the same reason this brief does.

## Evidence to request

Each item below is an evidence class the governing body can call for from management, and each is evidence for a named control or outcome. The [board oversight guide](../../ai/guide-ai-board-oversight.md) frames the questions (its section 5); the guide's section 7 sets what the governing body should expect to receive on a regular cadence.

- **The data classification record for each AI system's data**, as evidence for the classification-before-use control in the [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) (its sections 4.2 and 5).
- **The dataset datasheet**, as evidence that each dataset in the AI System Register is documented per the [dataset datasheet template](../../ai/template-dataset-datasheet.md).
- **Provenance and lineage records**, as evidence for the lineage controls in the [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) (its section 4.2) and the [training data governance procedure](../../ai/procedure-training-data-governance.md) (its Step 5).
- **The approval-to-train record**, as evidence that the dataset approval gate operated with the approvers the [training data governance procedure](../../ai/procedure-training-data-governance.md) names (its Step 4).
- **The readiness sign-off record**, as evidence for the data-quality gate in the [AI data quality and readiness validation standard](../../ai/standard-ai-data-quality-and-readiness-validation.md) (its sections 3.7 and 4).
- **The retention mapping for AI records**, as evidence that AI governance records are held to the rows in the [data retention schedule](../../governance/register-data-retention-schedule.md) (its section 7).
- **The cross-border transfer entries**, as evidence for transfer governance per the [cross-border data flow register](../../privacy/register-cross-border-data-flow.md) and the [privacy and data governance policy](../../privacy/policy-privacy-and-data-governance.md) (its section 4.6).
- **The retrieval access-control design**, as evidence for the AI-to-data controls in the [AI access and agent permissions standard](../../ai/standard-ai-access-and-agent-permissions.md) (its section 7).
- **Deletion propagation records**, as evidence that dataset deletion cascades to derived models per the [training data governance procedure](../../ai/procedure-training-data-governance.md) (its Step 6), and that retirement handles datasets and retrieval stores per the [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) (its section 4.11).
- **The assessment routing record**, as evidence that the required data protection and AI assessments were identified and run per the [integrated AI and privacy assessment procedure](../../ai/procedure-integrated-ai-and-privacy-assessment.md) (its Step 3).

## Limitations

- This page creates no compliance and imposes no requirement. The linked corpus documents govern; where this page differs from a corpus document, the corpus document prevails.
- This page carries composite claims. The division of labour it describes (the governing body requires the data governance layer and asks for evidence; management operates the controls; dataset gates sit beneath the system production gate) is synthesized across several corpus sources, and the adopting organization validates that reading against its own governance and committee structure.
- The corpus documents this page points to carry the classification levels, handling floors, retention periods, approval roles, assessment triggers, and named oversight bodies. This page routes to them and does not reproduce them, so the corpus remains the single source for every value.
- This page makes no claim about how likely any failure is, and none of its statements should be read as a probability or a frequency.

**End of Document**
