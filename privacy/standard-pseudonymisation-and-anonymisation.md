# Pseudonymisation and Anonymisation Standard

**Document Title:** Pseudonymisation and Anonymisation Standard\
**Document Type:** Standard\
**Version:** 1.0.3\
**Date:** 2026-06-22\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md), [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](procedure-privacy-impact-and-cross-border-transfer.md), [`ai/procedure-ai-system-impact-assessment.md`](../ai/procedure-ai-system-impact-assessment.md), [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material cryptographic, statistical, or regulatory change\
**Repository Path:** [`privacy/standard-pseudonymisation-and-anonymisation.md`](standard-pseudonymisation-and-anonymisation.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This standard defines pseudonymisation and anonymisation techniques permitted in the organisation, the requirements for each technique, and the re-identification risk assessment that determines whether a data set has crossed from pseudonymous (still personal data) to anonymous (no longer personal data). It supports lawful data minimisation, secure analytics, AI training data preparation, research, and cross-border transfer scenarios.

---

## Scope

This standard applies whenever personal data is transformed to reduce identifiability for any of the following purposes:

1. Sharing personal data with a third party under a reduced re-identification risk.
2. Internal analytics, machine learning, or AI training where direct identifiers are not required.
3. Long-term retention for statistical or research purposes after the operational purpose has ended.
4. Cross-border transfer where the destination jurisdiction's regime is less protective.
5. Test, development, or staging environments that consume data sourced from production.

---

## Definitions

| Term | Definition |
| --- | --- |
| Personal data | Information relating to an identified or identifiable natural person |
| Pseudonymisation | Processing personal data such that the data can no longer be attributed to a specific subject without additional information, kept separately and subject to controls. The data remains personal data. |
| Anonymisation | Processing such that the subject is not or is no longer identifiable; reasonably likely re-identification by any party using any reasonably available means is not possible. Anonymised data is not personal data. |
| Direct identifier | A value that identifies a subject on its own (name, government identifier, account identifier) |
| Indirect identifier (quasi-identifier) | A value that does not identify on its own but contributes to identification in combination (date of birth, postcode, sex, employer) |
| Re-identification risk | The probability that a subject in a data set can be re-identified by an attacker using any reasonably available means |
| Linkage attack | Re-identification by joining the data set with another external data set |
| Inference attack | Re-identification by inferring sensitive attributes from the released data |
| Singling-out attack | Identifying a subject as a unique row in the data set |

---

## Permitted techniques

| Technique | Category | Description | Typical use case |
| --- | --- | --- | --- |
| Tokenisation | Pseudonymisation | Replace direct identifiers with random tokens; mapping table held separately under access control | Production-to-test data flow, internal analytics |
| Cryptographic hashing with secret salt (e.g. HMAC) | Pseudonymisation | Replace direct identifiers with a keyed hash; key held separately under access control | Linking records across systems without exposing identifiers |
| Format-preserving encryption | Pseudonymisation | Replace direct identifiers with ciphertext of the same shape | Test data that must retain validation properties |
| Generalisation | Pseudonymisation or anonymisation step | Replace specific values with broader categories (full postcode to first three characters, age to decade) | Reducing quasi-identifier granularity |
| Suppression | Pseudonymisation or anonymisation step | Remove fields or specific values that contribute to identification | Removing high-risk quasi-identifiers |
| Microaggregation | Pseudonymisation or anonymisation step | Replace each value with the mean or median of a small cluster of similar records | Numeric quasi-identifiers |
| k-anonymity (k at minimum 5) | Anonymisation requirement | Each combination of quasi-identifiers appears in at least k records | Statistical release |
| l-diversity | Anonymisation requirement | Each k-anonymous group contains at least l distinct values for any sensitive attribute | Mitigates attribute disclosure |
| t-closeness | Anonymisation requirement | Distribution of sensitive attributes within each group is within t of the overall distribution | Mitigates inference attack |
| Differential privacy | Anonymisation technique | Add calibrated noise to query results or training; the privacy loss budget epsilon is bounded | Aggregate analytics, ML training |
| Synthetic data | Anonymisation derivative | Generate data that statistically resembles the original without containing original records | Open data release, model development |

Hashing without a secret key (plain SHA-256 of an identifier) is not pseudonymisation in any meaningful sense and is not permitted as a pseudonymisation technique. Removing the name field while leaving date of birth, postcode, and sex is not anonymisation; it is a partial pseudonymisation step that does not satisfy k-anonymity.

---

## Requirements

### 1. Selection of technique

1. Each transformation use case has an owner role and a documented purpose.
2. Selection of pseudonymisation or anonymisation is recorded with the rationale; downgrading from anonymisation to pseudonymisation requires explicit Data Protection Officer approval.
3. The technique combination is chosen by the Data Protection Officer with cryptographic input from the CISO where keys are involved.

### 2. Separation of mapping data

1. For pseudonymisation, the mapping table or key is held in a different system with different access control from the pseudonymised data.
2. The mapping system is logged; mapping access is reviewed quarterly.
3. The mapping is retained only as long as re-identification is operationally required.

### 3. Re-identification risk assessment

1. For any release outside the original processing boundary, the Data Protection Officer commissions a re-identification risk assessment.
2. The assessment considers linkage attacks against publicly available data sets, inference attacks against known sensitive attributes, and singling-out attacks based on uniqueness of quasi-identifier combinations.
3. The assessment classifies the residual risk as Negligible, Low, Moderate, High, or Unacceptable.
4. Releases at Moderate or higher residual risk require additional controls (contractual restriction, recipient assurance, time-limited access, secure enclave) or rejection.

### 4. Documentation

1. Each transformation use case is documented with: data source, technique, parameters (k, l, t, epsilon), residual risk assessment outcome, controls, owner, last review.
2. The documentation is part of the system's privacy assurance evidence.
3. Material changes to the source data or the technique trigger a re-assessment.

### 5. AI training data

1. AI training data sourced from personal data is pseudonymised or anonymised before training unless the lawful basis explicitly permits training on identifiable data and the data minimisation principle has been applied.
2. Where models are released, the Data Protection Officer assesses model-inversion and membership-inference risk; release is conditional on the assessment outcome.
3. Synthetic data and differential-privacy training are preferred for high-risk personal data categories.

### 6. Test and staging environments

1. Production personal data must not flow to test or staging environments. Use tokenised, format-preserving-encrypted, or fully synthetic data.
2. Where production-equivalent data is required (e.g. for performance testing), the transformation must produce data with k-anonymity at minimum 5 across quasi-identifiers and apply suppression or generalisation as needed.

---

## Risk classification thresholds (default)

| Residual risk | Definition | Permitted use |
| --- | --- | --- |
| Negligible | Re-identification not reasonably likely by any party using reasonably available means; quantitative re-identification risk below 0.1% | Open release acceptable subject to Data Protection Officer sign-off |
| Low | Re-identification not reasonably likely under intended use and recipient profile; quantitative risk between 0.1% and 1% | Controlled release to vetted recipients with contractual restrictions |
| Moderate | Re-identification possible under plausible attacker capability; quantitative risk between 1% and 5% | Restricted to internal use or contracts with strong recipient assurance; usually requires additional controls |
| High | Re-identification likely under plausible attacker capability; quantitative risk above 5% | Treat as personal data; pseudonymisation only; no external release |
| Unacceptable | Re-identification likely under low attacker capability | Reject the transformation as anonymisation; apply additional minimisation or do not release |

The percentages above are default thresholds. Adopting organisations may tighten these thresholds; loosening requires Data Protection Officer and CISO joint approval.

---

## Operating expectations

1. The Data Protection Officer maintains a register of pseudonymisation and anonymisation use cases with their technique, parameters, residual risk classification, and last review date.
2. Re-identification attempts (internal red-team exercises) are conducted at minimum annually against active anonymisation outputs.
3. Where a re-identification attempt succeeds, the affected output is recalled and the technique re-evaluated as a P2 incident.
4. Cryptographic keys used in pseudonymisation are managed under the cryptographic key lifecycle framework.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| GDPR | Article 4(5), Article 25, Recital 26 | Pseudonymisation definition, data protection by design, anonymisation threshold |
| UK GDPR | Same articles | Equivalent provisions |
| ISO/IEC 20889:2018 | Privacy enhancing data de-identification terminology and classification of techniques | Authoritative technique taxonomy |
| ISO/IEC 27559:2022 | Privacy-enhancing data de-identification framework | De-identification programme |
| NIST SP 800-188 | De-identifying government data sets | US de-identification baseline |
| Article 29 Working Party Opinion 05/2014 | Anonymisation techniques | EU regulator guidance (the Article 29 Working Party was the EDPB's predecessor; EDPB was established by the GDPR in May 2018 and assumed the Working Party's role) |
| EDPB Opinion 28/2024 (December 2024) | Use of personal data for AI models | Current EU regulator guidance on AI-model personal-data processing |
| ENISA | Pseudonymisation techniques and best practices | EU technical guidance |

---

## Limitations

This standard is a CC BY-SA 4.0 baseline. Adopting organisations must validate technique selection against their data, jurisdictional rules, and risk appetite. Quantitative thresholds are defaults; specific contexts (low-population groups, sensitive attribute distributions) may require stricter parameters. The standard is not a substitute for a privacy impact assessment when one is otherwise required.

---

**End of Document**
