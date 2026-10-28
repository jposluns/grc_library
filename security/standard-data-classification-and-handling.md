# Data Classification and Handling Standard

**Document Title:** Data Classification and Handling Standard\
**Document Type:** Standard\
**Version:** 1.9.2\
**Date:** 2026-10-27\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md), [`compliance/register-global-regulatory-applicability.md`](../compliance/register-global-regulatory-applicability.md), [`operations/standard-cloud-security-configuration-baseline.md`](../operations/standard-cloud-security-configuration-baseline.md), [`compliance/public-sector/annex-canada-public-sector-requirements.md`](../compliance/public-sector/annex-canada-public-sector-requirements.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material threat, framework, or regulatory change\
**Repository Path:** [`security/standard-data-classification-and-handling.md`](standard-data-classification-and-handling.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

This standard defines the classification, labelling, protection, retention, and destruction requirements for all information assets. The five classification levels (Public, Controlled, Internal, Confidential, Restricted) are authoritative for the corpus; subordinate documents that handle data must enumerate or reference the same five levels.

---

## 1. Purpose

To ensure that information is handled consistently according to its sensitivity, regulatory obligations, and business impact, while supporting confidentiality, integrity, and availability. Aligns with ISO/IEC 27002:2022 §§5.12 to 5.15, COBIT 2019 DSS05, CSA CCM v4.1 DSP-04, GDPR Article 32, ISO/IEC 27701:2025 (data retention and deletion; section numbering changed in 2025 standalone revision), and the applicable BASC International Security Standard (6.0.2 or 6.0.3).

---

## 2. Scope

1. Applies to all information assets owned, controlled, or processed, including digital and physical records, databases, documents, emails, collaboration tools, backups, and AI datasets and model artifacts.
2. Applies to all employees, contractors, suppliers, and partners with access to systems or data.
3. Covers all storage and communication media: servers, endpoints, cloud, and mobile devices.
4. Encompasses regional data handling obligations including BASC compliance for Latin American logistics and trade data.

---

## 3. Governance and accountability

| Role | Responsibility |
| --- | --- |
| CIO | Approves data classification framework and ensures that enterprise-wide adoption is achieved. |
| CISO | Enforces encryption, labelling, and protection controls. |
| Data Owners / Department Heads | Classify and label data assets according to business and regulatory sensitivity. |
| IT Operations / Cloud Administrators | Implement and maintain automated labelling, DLP, and encryption solutions. |
| Data Protection Officer | Ensures that alignment with privacy and data protection laws is maintained. |
| AI Governance Council | Oversees classification and protection of AI datasets and model data. |

Sector-conditional roles (for example, a sector-conditional compliance role that oversees classification of customs, trade, and cargo data for BASC-certified operations) apply where the organization participates in a covered sector programme; see [`compliance/`](../compliance/).

---

## 4. Data classification levels

| Classification | Definition | Handling Requirements | Examples |
| --- | --- | --- | --- |
| **Public** | Information approved for open distribution. | No restriction. Public dissemination allowed. | Press releases, marketing materials, published reports. |
| **Controlled** | Information that may be shared externally at discretion; disclosure poses low risk. | Share externally under context; management awareness required. | Product overviews, proposals, general client communications. |
| **Internal** | Restricted to employees and authorized contractors; external sharing requires approval or NDA. | Store in internal systems; encryption required for databases and backups (full at-rest requirements including portable devices in the encryption-requirements table). | Internal procedures, reports, project data. |
| **Confidential** | Contains sensitive business, financial, or personal data. Unauthorized disclosure may cause harm. | Encryption at rest and in transit; access by authorization only. | Contracts, client data, payroll, incident reports. |
| **Restricted** | Highest sensitivity; includes trade secrets, privileged data, or AI model code. | Strong encryption, strict access control, PAM enforcement, audit logging. | Source code, credentials, merger data, customs and cargo data from BASC-certified operations, AI model weights. |

---

## 5. Classification and labelling

5.1 Data Owners are responsible for classifying data upon creation or receipt.
5.2 All digital files must display classification labels within document metadata, filenames, or headers.
5.3 Automated classification and handling enforcement via the data classification platform is required (cloud productivity platform).
5.4 Physical records must be stamped or marked with classification level on each page or cover.
5.5 System-generated or AI-derived data inherits the classification of its source unless explicitly reclassified.

---

## 6. Handling requirements

| Control Area | Requirement |
| --- | --- |
| Storage | Use encrypted storage for Confidential and Restricted data (AES-256). |
| Transmission | Use TLS 1.3 or stronger encryption for data transfers. |
| Access Control | Grant least-privilege access based on role. |
| Collaboration | Share via approved platforms with classification awareness. |
| Logging and Monitoring | Record all access to Restricted and Confidential data in the SIEM. |
| Printing and Disposal | Print only when necessary; shred Confidential or higher data after use. |
| Cloud DLP | Enforce classification-based DLP policies across cloud productivity and storage platforms. |

---

## 7. AI data classification and handling

7.1 AI datasets, model artifacts, and logs must follow equivalent or stricter handling than Confidential data.
7.2 Datasets containing personal or proprietary information must be anonymized, pseudonymized, or encrypted.
7.3 AI model weights, training scripts, and inference APIs classified as Restricted must reside in secure, access-controlled repositories.
7.4 Model outputs with potential regulatory or ethical implications (e.g., automated decision logs) must be preserved per the Records Retention Standard.
7.5 For AI systems supporting BASC or customs automation:
- Training and operational data must comply with BASC confidentiality controls and the organization's trade-data protection requirements, consistent with its ISO 28000:2022 supply-chain security management system. ISO 28000:2022 is not held in the reference base; confirm its requirements against the standard before treating this attribution as verified. <!-- ref-absence: ISO 28000:2022 -->
- AI model audit logs must be tamper-proof and available for customs review.

---

## 8. Retention and destruction

8.1 Data retention periods are defined in the Records Retention and Destruction Standard.
8.2 Upon expiration of retention, data must be securely destroyed, or, for Public paper, may go to normal disposal, only after confirming that no legal hold or investigation applies, using the two-part confirmation in rule 2 of the lost or stolen device decision table in [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) §5.2.1, applied to the data concerned. A check of the GRC platform and Records Register confirms only whether a hold is recorded. Under that rule, Legal Counsel or the Incident Commander or, for security P3 and P4 where no Incident Commander is assigned, the SOC lead confirms whether an investigation under [`security/procedure-security-incident-response.md`](procedure-security-incident-response.md) treats the data as evidence. Only Legal Counsel confirms whether an investigation by an external authority treats the data as evidence, and whether a hold is required but not yet recorded. Where a legal hold or investigation applies, or that status cannot be confirmed, destruction must be deferred until Legal Counsel, in writing, formally releases the hold or narrows it to exclude the affected data, or confirms in writing that an investigation without a legal hold no longer treats the data as evidence. This follows the Records Retention and Destruction Standard §7 and, for data on a device, rule 8 of the lost or stolen device decision table in [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) §5.2.1. Once permitted, destruction or disposal uses:
- For data on logical or cloud storage, cryptographic erasure under NIST SP 800-88 Rev. 2 §3.2, only where no sensitive data has been stored on it in plaintext, since its last sanitization with an appropriate technique, if it was previously sanitized (§3.2.2), with every copy of the target cryptographic keys sanitized and all keys hierarchically below them eliminated or actively erased. Cryptographic erasure is not relied on where the storage or its keys may have been backed up or escrowed, unless every copy of the keys is accounted for, including how and where it was stored and managed outside the storage, and sanitized (§§3.2.2 and 3.2.3). Cryptographic erasure leaves the data on the storage as encrypted text, so it protects the data only while the encryption stays strong. Some sensitive data must stay confidential for decades, and future weaknesses in the encryption or new computing capabilities, such as quantum computing, could make the data recoverable (§3.2.2). For Restricted data, the CISO judges whether the data must stay confidential for a long time. Where it must, cryptographic erasure is used only where the CISO confirms that the encryption is expected to stay adequate for as long as the data stays sensitive; otherwise another method is used. Where cryptographic erasure destroys data whose retention period has expired, including on media sanitized for reuse under §7.1 of [`operations/procedure-media-handling-and-transport.md`](../operations/procedure-media-handling-and-transport.md), it is a destruction action, so the CISO's confirmation is recorded in the Destruction Register under §8.2 of [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md). Only where media is sanitized for reuse and no records are destroyed is the confirmation not recorded. Where cryptographic erasure is the only purge option for the storage (§§3.1.2 and 3.2.2) and that adequacy cannot be confirmed, keeping the data past its retention period is ad hoc retention beyond the schedule under §5 of that standard: it needs Legal Counsel's written approval before it exceeds 7 years, the data stays under its retention controls until adequacy is confirmed or another method becomes available, and the decision is recorded in the Destruction Register under §8.2 of that standard. For other digital data and electronic storage media, a method that §8.1 of [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md) accepts for the highest classification held, applied under §§7.1 and 7.2 of [`operations/procedure-media-handling-and-transport.md`](../operations/procedure-media-handling-and-transport.md) (NIST SP 800-88 Rev. 2 and IEEE 2883-2022); media-based cryptographic erasure is accepted only where the prerequisites in IEEE 2883-2022 6.5.3 and the condition on backed-up or escrowed keys set out above for logical or cloud storage are met and, for Restricted data, the CISO's judgement and confirmation set out above are also met.
- For paper whose highest classification of information held is Public, normal disposal (see [`governance/register-key-terms-and-definitions.md`](../governance/register-key-terms-and-definitions.md)) under §8.1 of that standard, as §3 of that procedure allows, or a method in the next bullet. Paper that holds any information classified above Public is not Public paper, and this exception covers paper only.
- For other paper and for all other physical records, cross-cut shredding or a contracted secure disposal service under §8.1 of that standard; for Confidential and Restricted records, cross-cut shredding at DIN 66399 Level P-4 or higher (strip-cut shredding is not accepted) or a contracted secure document destruction service that meets an equivalent standard, as §7.3 of that procedure requires.
8.3 Certificates of Destruction must be logged and archived for seven years.
8.4 AI datasets and BASC-certified trade data undergo destruction validation to ensure that data-lineage-tracking integrity is preserved.

---

## 9. Encryption requirements

| Classification | Encryption Requirement |
| --- | --- |
| Public | Not required. |
| Controlled | Optional; required if transmitted externally. |
| Internal | Required for databases, backups, and portable devices. |
| Confidential | Mandatory (AES-256 at rest, TLS 1.3 in transit). |
| Restricted | Mandatory; hardware security modules (HSMs) and key rotation every 90 days. |

Encryption keys must be managed under the Encryption and Key Management Policy.

---

## 10. Sector-programme data handling overlays

Where the organization participates in a sector programme that imposes additional handling requirements on programme-specific data (for example, customs, cargo, and personnel data in BASC-certified operations; healthcare regulation for PHI; financial-services regulation for payment-card or fraud data), the corresponding sector annex states the additional classification, storage, physical-copy, and incident-treatment requirements. See [`compliance/`](../compliance/).

---

## 11. Monitoring and compliance

11.1 The CISO and Compliance Manager perform quarterly reviews of classification and handling adherence.
11.2 Automated DLP reports must be analyzed monthly to detect potential misclassifications or policy breaches.
11.3 Noncompliance or mishandling triggers investigation and remediation under the Corrective and Preventive Action Procedure.
11.4 Annual ISO and BASC certification audits verify adherence to the organization's classification and handling controls.

---

## 12. Framework alignment

| Control Area | ISO/IEC 27002:2022 | COBIT 2019 | CSA CCM v4.1 | Legal / Regulatory |
| --- | --- | --- | --- | --- |
| Classification and labelling | §5.12, §5.13 | APO01.07 | DSP-01, DSP-04 | GDPR Art. 32, PIPEDA |
| Encryption | §8.24 | DSS05.02, DSS05.03 | CEK-03, CEK-04, CEK-12 | N/A |
| Retention and disposal | §8.10 | APO14.09 | DSP-02, DSP-16 | ISO/IEC 27701:2025 Annex A.1.4.8 to A.1.4.9, A.2.4.3 |
| AI data handling | 5.34 (privacy and protection of PII); 8.11 (data masking) | APO14.08 | DSP-04, DSP-16, DSP-17, LOG-10 | AIDA (lapsed), PIPEDA |
| Trade data (BASC) | N/A | N/A | N/A | BASC Security Standard 6.0.2/6.0.3, ISO 28000:2022. ISO 28000:2022 is not held in the reference base; confirm its requirements against the standard before treating this alignment as verified. <!-- ref-absence: ISO 28000:2022 --> |

This standard also aligns with ISO/IEC 27040:2024 (Storage security) for the secure storage, retention, and sanitization of classified data at rest.

For cloud-hosted information, this standard also aligns with ISO/IEC 27017:2026 (second edition, 2026-07), clause 5.13 (Labelling of information), whose cloud-service guidance advises the cloud service customer to label information and other associated assets held in the cloud under its own labelling procedures, and allows it to use labelling functionality that the cloud service provider offers, where applicable; this supports rule 5.2 and the labelling element of rule 5.3.

For personal data, this standard also aligns with ISO/IEC 29151:2026 (second edition, 2026-07). Clause 5.12 (Classification of information) advises classifying all information that contains PII, using categories that reflect legal and contractual obligations, the sensitivity of the information, and the risk of harm from a breach; this supports classifying personal data, and section 4 places sensitive personal data in the Confidential level. Annex A.6 (Data minimization), items f) to h), advises deciding which PII to anonymize or de-identify, de-identifying it according to its form and the risks identified, and de-identifying or anonymizing publicly available data used for AI training where consent cannot be obtained from the people concerned; this supports rule 7.2. Items f) and g) are risk-based guidance on de-identification and item h) is limited to publicly available data used for AI training where consent cannot be obtained, whereas rule 7.2 is a mandatory requirement that also accepts encryption and also covers proprietary information: this citation shows alignment, not that ISO/IEC 29151 requires rule 7.2.

For cloud-hosted data, **CCCS ITSP.50.103 (Security Categorization of Cloud-Based Services)** provides an injury-based security-categorization methodology that bridges this standard's sensitivity classification to cloud control-profile selection. It defines security categorization as "the process of identifying the potential injuries that could result from compromises to business" processes and information (section 2), and makes categorization "fundamental" because it "provides the basis for selecting the appropriate cloud capabilities, security control profile" (section 1). ITSP.50.103 "applies to both private and public-sector organizations" (section 1.2), so it is usable as a categorization-to-control-profile bridge alongside this standard's classification model rather than as a public-sector-only instrument. Its section 7 covers selecting a security control profile from the resulting category; the cloud configuration controls that follow are in the [Cloud Security Configuration Baseline](../operations/standard-cloud-security-configuration-baseline.md).

For a Canadian federal department or other entity to which the Treasury Board Policy on Government Security applies (Policy 6.1), security categorization follows the Directive on Security Management, Appendix J: Standard on Security Categorization (the held text, which states that it takes effect on 1 July 2019, J.1.1), which details the categorization requirement in subsection 4.3.1 of the Directive (J.2.1). Paraphrased with its pinpoints: the injury that a loss of confidentiality, integrity or availability could cause is examined separately (J.2.2.1), and either one security category for the overall impact or separate categories for each loss is assigned (J.2.2.2); the general categories are impact levels from low to very high, set by the degree of injury that could reasonably be expected (J.2.3.1); and information confidentiality categories are Classified (Confidential, Secret or Top Secret) where unauthorized disclosure could injure the national interest (J.2.4.1), and Protected A, B or C where the injury falls outside the national interest (J.2.4.2). The category of a repository reflects aggregation (J.2.2.4), and the confidentiality category takes account of the exemption and exclusion criteria of the Access to Information Act and the Privacy Act (J.2.2.6). These categories are a separate scale from this standard's five classification levels in section 4; this standard does not map one onto the other, and no Protected or Classified category is inferred from a level here. The force and applicability of the federal instruments are set out in the federal security and cyber baseline under domain cluster 3 of the [Canada public-sector annex](../compliance/public-sector/annex-canada-public-sector-requirements.md#federal-security-and-cyber-baseline).



**End of Document**
