# AI Model Risk Standard

**Document Title:** AI Model Risk Standard\
**Document Type:** Standard\
**Version:** 1.1.2\
**Date:** 2026-07-02\
**Owner:** AI Governance Approver\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-model-risk.md`](framework-ai-model-risk.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`ai/procedure-ai-model-risk-assessment.md`](procedure-ai-model-risk-assessment.md), [`ai/template-model-card.md`](template-model-card.md), [`ai/template-system-card.md`](template-system-card.md), [`ai/guideline-ethical-ai-use.md`](guideline-ethical-ai-use.md), [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material model, data, threat, regulatory, or assurance change\
**Repository Path:** [`ai/standard-ai-model-risk.md`](standard-ai-model-risk.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines minimum requirements for assessing and managing AI model risk. It operationalizes the AI Model Risk Framework through enforceable expectations for data provenance, interpretability, representation, robustness, alignment, monitoring, documentation, approval, and retirement.

---

## 2. Applicability

This standard applies to models and model-enabled systems that materially affect business, security, privacy, legal, operational, financial, customer, employee, or public outcomes.

It applies to internally developed models, externally supplied models, fine-tuned models, embedded models, retrieval-augmented systems, generative systems, predictive systems, and models used through external services.

---

## 3. Requirements

### 3.1 Model inventory and ownership

1. Each model or model-enabled system must be recorded in an AI system or model inventory.
2. Each model must have an assigned owner, data owner, control owner, and supplier owner where applicable.
3. Each model must have an approved purpose, prohibited use conditions, risk tier, lifecycle status, and review date.

### 3.2 Data provenance and lineage

1. Training, tuning, retrieval, evaluation, monitoring, and inference data must have documented provenance and permitted-use basis.
2. Data lineage must identify source, transformation, storage, access, retention, deletion, and supplier handling where applicable.
3. Sensitive, personal, regulated, confidential, or restricted data must not be used unless authorized, assessed, and controlled.
4. Data poisoning, evaluation contamination, unauthorized secondary use, and training data leakage must be considered during assessment.

### 3.3 Interpretability and documentation

1. Interpretability expectations must be proportionate to model risk and use context.
2. High-impact models must maintain evidence explaining material output drivers, limitations, assumptions, and known failure conditions.
3. Model cards or equivalent documentation must describe purpose, data, risk tier, evaluation results, limitations, intended use, prohibited use, monitoring, and approval status.
4. System cards or equivalent deployment-context documentation must describe integrations, users, data flows, access controls, tool access, logging, supplier dependencies, and human oversight.

### 3.4 Representation and bias review

1. Models using embeddings, features, labels, or latent representations must be assessed for unstable, sensitive, biased, or unauthorized patterns proportionate to risk.
2. Sensitive attribute and proxy risk must be reviewed where model outputs can materially affect individuals, groups, access, eligibility, pricing, safety, employment, finance, or regulated decisions.
3. Findings must be remediated, controlled, or accepted through documented risk governance.

### 3.5 Robustness and adversarial testing

Model testing must address, proportionate to risk and model class. The taxonomy below distinguishes LLM and generative-system threats from classical ML threats, federated-learning threats, and the defence categories that apply across them. Coverage depth follows model class and deployment context, not all threats apply to all models.

#### 3.5.1 LLM and generative-system threats

- Prompt injection (direct).
- Indirect prompt injection (via retrieved or supplied content).
- Jailbreak attempts and content-filter circumvention.
- Training data poisoning of pre-training, fine-tuning, or alignment corpora.
- Training data extraction or leakage in model output.
- Retrieval leakage across users, tenants, classifications, or scopes.
- Unsafe tool use and excessive agency in agentic systems.
- Memory poisoning across sessions where persistent memory exists.
- Agentic goal theft and gradual drift across multi-turn sessions.
- Inter-agent communication compromise in multi-agent orchestrations.
- Hallucinated security controls in AI-generated code.
- Multimodal injection via image, audio, video, document, OCR, or QR-code inputs.

#### 3.5.2 Classical ML threats (non-LLM models)

Where the model is a classical ML model (image classifier, object detector, tabular predictor, audio model, speech recognition, time-series model), testing must address the following categories proportionate to risk and adversary capability:

- **Evasion attacks**: gradient-based methods such as FGSM, PGD (projected gradient descent), Carlini-Wagner family (L0, L2, LInf), DeepFool, AutoAttack; decision-boundary methods such as BoundaryAttack and HopSkipJump; score-based methods such as SquareAttack and ZooAttack; patch and physical attacks such as AdversarialPatch, DPatch for object detection, RobustDPatch; universal perturbations; transformation attacks such as SpatialTransformation; audio-specific attacks such as ImperceptibleASR; video-specific attacks such as OverTheAirFlickering; tabular attacks such as LowProFool.
- **Poisoning attacks**: data poisoning to induce backdoor behaviour (PoisoningAttackBackdoor, PoisoningAttackCleanLabelBackdoor); poisoning to induce class-targeted misclassification (FeatureCollisionAttack, BullseyePolytope); hidden-trigger backdoors; gradient-matching attacks; sleeper-agent attacks; object-detection-specific poisoning (BadDet global misclassification, regional misclassification, object generation, object disappearance).
- **Extraction attacks** (model theft): CopycatCNN-style query-based extraction; KnockoffNets-style label-only extraction; functionally-equivalent extraction. Mitigations include query rate limiting, output randomization, and watermarking.
- **Inference attacks** (privacy): membership inference (black-box, label-only decision-boundary, label-only gap, shadow-model); attribute inference (black-box, white-box decision-tree variants); model inversion (MIFace and equivalents); training-data reconstruction (DatabaseReconstruction).

#### 3.5.3 Federated-learning threats (where applicable)

Where the model is trained or fine-tuned via federated learning or split learning, additional threats apply:

- Distributed backdoor attacks (DBA) where multiple clients collude to embed backdoor triggers.
- Model replacement attacks in federated aggregation.
- Free-rider attacks where a participant contributes synthetic or replayed updates to extract the model while contributing nothing.
- Label leakage via norm-attack on shared gradients.
- Gradient inversion attacks (DLG, iDLG, GS, CPL, GradInversion, GAN attack) that reconstruct training data from shared gradients.

#### 3.5.4 Defence categories

Defences are applied proportionate to risk, threat class, and deployment context. Categories applicable across LLM and classical ML where the threat applies:

- **Preprocessor defences**: feature squeezing, spatial smoothing, JPEG compression, total-variation minimization, thermometer encoding, Gaussian augmentation.
- **Postprocessor defences**: reverse sigmoid, high-confidence filtering, output rounding, Gaussian noise injection, label-set restriction.
- **Adversarial training**: standard adversarial training, Madry-style PGD adversarial training, TRADES, fast-better-faster (FBF), differentially-private adversarial training.
- **Transformer defences**: defensive distillation, NeuralCleanse for backdoor removal, STRIP, activation-defence for poisoning detection.
- **Detectors**: binary input detectors, binary activation detectors, subset-scanning detectors.
- **Privacy defences**: differential privacy (DP-SGD, AdaDPS, DPlis), homomorphic encryption, k-anonymity for tabular inputs, federated-learning aggregation defences (FoolsGold against Sybil patterns, Mondrian, MID).
- **Output egress controls**: query rate limiting, watermarking, output randomization against extraction.
- **Certified defences**: where applicable to model class, certified-robustness training and certified adversarial training.

#### 3.5.5 Adaptive-attacker testing

Static defensive test suites become insufficient at the rate at which adaptive attackers iterate. Where the deployed model class is known to be vulnerable to reinforcement-learning-trained adversaries (per the AI threat model), adaptive-attacker testing is required at the cadence in `ADTEST-SEC-01` of the AI and Agentic Development Security Standard. The test exercises a trained-attacker model against the current defensive posture and measures attack success rate over time; baseline test suites that the production system has already passed are reused as the lower-bound floor.

#### 3.5.6 Out-of-distribution and operational robustness

Across all model classes, testing must address out-of-distribution behaviour, input perturbation sensitivity outside the adversarial threat model (sensor noise, image compression artefacts, audio bitrate variation, distribution shift between training and operational data), and operational degradation under load.

### 3.6 Alignment and human oversight

1. Model outputs and behaviours must be assessed against approved purpose, operating constraints, user expectations, and risk tolerance.
2. Human oversight must be defined where outputs may affect rights, access, eligibility, employment, finance, safety, security, legal exposure, or critical operations.
3. Reviewers must have authority and information sufficient to challenge, override, reject, or escalate model outputs.

### 3.7 Monitoring and re-evaluation

1. Deployed models must have monitoring proportionate to risk.
2. Monitoring should address performance, drift, misuse, leakage, prompt injection attempts, anomalous retrieval, unsafe tool activity, incidents, and control exceptions.
3. Re-evaluation must occur at defined cadence and upon material change to model, data, supplier, deployment context, threat pattern, or legal or regulatory context.

### 3.8 Incident and exception management

1. Model-related incidents must be managed through incident response.
2. Exceptions must record owner, scope, risk, rationale, compensating controls, expiry, and approval.
3. Critical or high-impact unresolved model risks must not proceed without explicit residual risk acceptance by the appropriate accountable authority.

### 3.9 Retirement and deletion

Retirement must address model endpoint removal, access removal, service account removal, data retention, retrieval store deletion, prompt and output log handling, evaluation artefact retention, supplier deletion confirmation, and inventory status update.

---

## 4. Evidence requirements

Evidence should include inventory entry, model card, system card where applicable, data provenance record, lineage record, evaluation report, adversarial test summary, access review, monitoring plan, incident records, exception records, approval record, and retirement or deletion record.

---

## 5. Limitations

This standard is original library content. It does not reproduce external control text and does not establish compliance, certification, safety, or assurance by itself. Adopting organizations must validate applicability and operating effectiveness.

---

**End of Document**
