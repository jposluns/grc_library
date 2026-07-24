# Training Data Governance Procedure

**Document Title:** Training Data Governance Procedure\
**Document Type:** Procedure\
**Version:** 0.0.11\
**Date:** 2026-07-24\
**Owner:** AI Data Steward\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`ai/standard-ai-model-risk.md`](standard-ai-model-risk.md), [`ai/template-dataset-datasheet.md`](template-dataset-datasheet.md), [`ai/register-model-registry.md`](register-model-registry.md), [`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`privacy/standard-pseudonymization-and-anonymization.md`](../privacy/standard-pseudonymization-and-anonymization.md), [`privacy/procedure-data-subject-rights-management.md`](../privacy/procedure-data-subject-rights-management.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** Annual and upon material change to training-data sources, regulation, or supplier landscape\
**Repository Path:** [`ai/procedure-training-data-governance.md`](procedure-training-data-governance.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure governs the lifecycle of data used to train, fine-tune, or otherwise shape model behaviour. It addresses sourcing, lawful basis, consent, sensitive-content removal, lineage, deletion propagation, supplier disclosure, and the recurring obligations that arise when a model derived from a dataset remains in use after the dataset itself has changed.

---

## Scope

This procedure applies to all training-data activities including: pre-training corpora used by foundation models the organization builds or substantially shapes; fine-tuning datasets; reinforcement-learning feedback data; evaluation datasets where evaluation results materially influence model selection; retrieval indices whose content affects model output. It applies regardless of whether the data is internally generated, licensed, scraped under documented rules, or synthetically produced.

It does not cover purely transactional logging (per the logging standard) or business-process data flows that do not feed an AI training or fine-tuning step.

---

## Procedure

### Step 1: Source identification

For each candidate dataset, the AI Data Steward records:

| Field | Required content |
| --- | --- |
| Source | Internal generation, supplier licence, scrape under documented rules, public corpus, synthetic generation, mixed |
| Lawful basis | Lawful basis under each applicable regime (GDPR Article 6 and 9; LGPD; PIPL; CCPA; sector regimes) |
| Consent evidence | Where consent is the basis, the capture mechanism and evidence retention |
| Licence terms | For licensed corpora; restrictions on use (training, evaluation, redistribution, derivative works) |
| Subject notification | Whether subjects whose data is in the corpus have been notified, or the rationale for not notifying |
| Geographical scope | Countries from which the data originates |
| Cross-border transfer | Mechanism per GDPR Chapter V or equivalent |
| Acquisition contract | Reference to the supplier contract where applicable |
| Sensitive categories present | Special-category data, children's data, regulated business data |

### Step 2: Sensitive-content removal

Before the dataset is used for training:

| Action | Required output |
| --- | --- |
| PII detection | Run PII detection across the corpus; record categories detected and the volume |
| Redaction or removal | Apply the technique appropriate to the use case (removal, redaction, pseudonymization, anonymization per the pseudonymization standard) |
| CSAM and prohibited content filtering | Run prohibited-category classifiers; remove with audit trail |
| Hate, violence, and high-toxicity filtering | Apply per the responsible-use policy; thresholds documented |
| Copyrighted content review | Where the corpus is web-crawled or may contain copyright-protected material: confirm lawful access (no circumvention of paywalls or technical protection measures per Directive 2001/29/EC Article 6(3)); identify and honour machine-readable rights reservations and text-and-data-mining opt-outs expressed under Article 4(3) of Directive (EU) 2019/790, including the Robot Exclusion Protocol (robots.txt, IETF RFC 9309); and document the use rationale and any opt-out mechanism the upstream source provides. Where the organization is a general-purpose AI provider placing a model on the EU market, this is part of the copyright policy required by EU AI Act Article 53(1)(c), for which the EU GPAI Code of Practice (Copyright Chapter, July 2025) is the Article 56 co-regulatory instrument. |
| De-identification verification | For corpora claimed anonymized, the re-identification risk assessment per the pseudonymization standard |
| Output of step | A cleaned dataset; the datasheet annex documenting all transformations |

### Step 3: Consent and subject rights mechanism

Where the dataset contains personal data:

| Action | Required output |
| --- | --- |
| ROPA entry | Cross-reference to the record of processing activities |
| Privacy notice | Subjects notified per the privacy notice template |
| Rights mechanism | Mechanism by which subjects can exercise rights against this dataset and against models derived from it |
| Deletion propagation policy | Documented cascade rule from dataset deletion to derived models and embeddings |
| Children's data | Where applicable, per the children's data framework |
| Special-category condition | Where Article 9 special-category data is present, the Article 9 condition and the additional safeguards |

### Step 4: Approval to train

Before any training, fine-tuning, or RL pipeline consumes the dataset:

| Approval | Trigger | Approver |
| --- | --- | --- |
| Dataset acceptance | Every new dataset or material refresh | AI Data Steward with Data Protection Officer co-sign if personal data; Legal Counsel co-sign if licensed corpus |
| Data-quality readiness | Every new dataset or material refresh, before the training pipeline consumes it | AI Data Steward, per the [AI Data Quality and Readiness Validation Standard](standard-ai-data-quality-and-readiness-validation.md) readiness sign-off gate |
| Use-case fit | Per training run | Service owner |
| Risk assessment | High-risk training run (e.g. foundation-model-scale, regulated-sector model, agentic system) | AI Governance Council |
| Sustainability check | High-compute training | Per the sustainability framework |

### Step 5: Lineage tracking

Each training event produces lineage records:

| Lineage element | Required content |
| --- | --- |
| Dataset versions consumed | Specific dataset version identifiers and hashes |
| Pipeline version | Cleaning and preparation pipeline version |
| Training compute and configuration | Hyperparameters, compute, environment, base model if fine-tune |
| Output model artefact | Model identifier, hash, version |
| Evaluation results | Cross-reference to evaluation registry |
| Approval signatures | Approver roles and timestamps |

Lineage is recorded so any subsequent dataset change can be traced through to affected models.

### Step 6: Deletion propagation

When a data subject exercises a right to deletion, or when a corpus is retired under retention rules, the procedure propagates the deletion:

| Step | Action | SLA |
| --- | --- | --- |
| 1 | Identify all dataset versions containing the subject's data | Within 7 calendar days |
| 2 | Remove or pseudonymize per the dataset's policy; produce a new dataset version | Within 14 calendar days of identification |
| 3 | Identify all derived models, fine-tunes, and embeddings | Within 21 calendar days |
| 4 | Treat per the derived-artefact policy: retrain from cleaned dataset where economically feasible; otherwise document the residual exposure and risk-accept per the exception process | Per the retraining schedule; risk acceptance within 30 calendar days |
| 5 | Confirm deletion to the subject through the DSAR workflow | Within the subject-rights regulatory window |
| 6 | Update the AI risk register where derived-artefact retention is risk-accepted | Same cycle as step 4 |

The procedure recognizes that derived models often cannot be perfectly "unlearned" today. Where retraining is not feasible, the residual exposure is documented and the risk acceptance is reviewed at every model lifecycle event.

#### Limits of deletion propagation (honest scope)

The procedure guarantees the following deletion outcomes within the stated SLAs:

| Outcome | Guarantee level |
| --- | --- |
| Dataset and dataset-version-store removal | Guaranteed - verifiable by hash and version absence |
| Embeddings derived from the dataset in active vector stores | Guaranteed - verifiable by re-indexing or vector-store version |
| Backup copies of the dataset | Guaranteed within the backup-retention cycle (verifiable by next-cycle attestation) |
| Production-served models trained on the dataset | Best-effort - retraining is scheduled where economically feasible; residual exposure is risk-accepted with documented rationale where not |
| Fine-tunes and adapters derived from the dataset | Best-effort - same as above |
| Logs of past inferences that reflected the deleted data | Per the logging retention policy; not retroactively scrubbed unless the inference logs themselves are personal data |
| External models the organization does not control | Out of scope; addressed contractually via no-training and right-to-deletion clauses with providers |

Adopting organizations honestly distinguish what they can guarantee from what is best-effort when communicating to data subjects and regulators.

### Step 7: Supplier-provided training data

Where the organization acquires training data from a supplier:

| Action | Required output |
| --- | --- |
| Supplier datasheet | Acquired alongside the dataset |
| Provenance attestation | Supplier's documented sources and lawful-basis chain |
| Licence compliance | Legal review of the use rights |
| Subject-rights flow-through | How the supplier honours deletion that propagates from the organization's customers |
| Indemnity | Coverage for IP claims arising from the supplier's data |
| Refresh cadence | Frequency at which the supplier provides updated provenance attestations |

### Step 8: Synthetic data

Where the organization generates or acquires synthetic training data:

| Field | Required content |
| --- | --- |
| Generation method | Statistical, simulation, model-generated |
| Seed dataset | The seed dataset's datasheet |
| Realism and bias assessment | Statistical comparison to real-world target distribution |
| Mode collapse risk | Where the synthetic data is model-generated, the risk that the source model's biases are amplified |
| Labelling as synthetic | Synthetic content is identifiable as such where it could be confused with real data downstream |

### Step 9: Retrieval index content

Where a retrieval index materially shapes model output:

| Action | Required output |
| --- | --- |
| Source documentation | Each document or chunk source is documented with its provenance |
| Access propagation | Retrieval respects the user's access permissions on the underlying source |
| Update cadence | Documented refresh cycle |
| Removal handling | Documents removed from the underlying source are removed from the retrieval index within a defined window |
| Indirect-injection mitigation | Per the AI security standard |

### Step 10: Periodic review

| Review type | Cadence |
| --- | --- |
| Per-dataset acceptance review | At every material refresh |
| Privacy review of training-data corpora | At minimum annually |
| Sensitive-content removal pipeline review | At minimum annually and at every new sensitive category becoming relevant |
| Supplier provenance review | At the supplier's attestation cadence and at minimum annually |
| Lineage completeness audit | At minimum quarterly for production datasets |
| Deletion-propagation backlog review | Monthly while open requests exist |

---

## Coordination with adjacent governance

| Adjacent | Coordination point |
| --- | --- |
| Dataset datasheet | One datasheet per dataset version |
| Model registry | Each model row references its training and fine-tuning datasets |
| AI system register | Each AI system row references its consuming model and indirectly its datasets |
| Privacy and data governance policy | Lawful basis, consent, subject rights |
| Data subject rights management procedure | DSAR workflow integration |
| Pseudonymization and anonymization standard | De-identification techniques |
| ROPA | Personal-data-bearing datasets recorded |
| Children's data framework | Where children's data is present |
| Sustainability and responsible technology framework | Training compute energy and emissions |
| Third-party AI due diligence procedure | Supplier-provided training data |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| EU AI Act | Articles 10 (data and data governance), 11 (technical documentation) | Training data obligations |
| EU GPAI Code of Practice (Copyright Chapter, July 2025) | Commitment 1 / Measures 1.1 to 1.3 (copyright policy; lawful-access crawling; identify and comply with text-and-data-mining rights reservations under Article 4(3) of Directive (EU) 2019/790) | Article 56 co-regulatory instrument for demonstrating AI Act Article 53(1)(c) compliance; applies where the organization is a GPAI provider |
| ISO/IEC 42001:2023 | §7.5 documented information | AI management system |
| GDPR / UK GDPR | Articles 5, 6, 9, 17, 22, 25, 30, 35 | Lawful basis, subject rights, by design, ROPA, DPIA |
| LGPD | Articles 7, 9, 18 | Brazilian lawful basis and rights |
| PIPL | Articles 13, 14, 24, 44 to 50 | Chinese lawful basis and rights |
| NIST AI RMF | MAP, MEASURE | AI risk management |
| ISO/IEC 5259-2:2024 | Data quality measures | Data-quality model, measures, and targets |
| ISO/IEC 5259-3:2024 | Data quality management requirements | Data-quality plan, verification and validation, and supply chain |
| ISO/IEC 5259-4:2024 | Data quality process framework | Plan, evaluate, improve, and validate loop and data-use approval |
| ISO/IEC 5259-5:2025 | Data quality governance framework | Data-quality governance roles, policies, and oversight across the training-data lifecycle |
| ISO/IEC 8183:2023 | AI data life cycle framework | Data lifecycle for AI training data |
| OECD AI Principles | All five values | Foundational principles |

---

## Limitations

This procedure is a CC BY-SA 4.0 baseline. Training-data governance is an evolving area; specific obligations under the EU AI Act, sector regulations, and emerging litigation (notably copyright) change frequently. Adopting organizations consult specialist counsel at each material decision. The procedure recognizes that some technical mitigations (e.g. machine unlearning at scale) remain immature; the exception process captures unavoidable residual exposure.

---

**End of Document**
