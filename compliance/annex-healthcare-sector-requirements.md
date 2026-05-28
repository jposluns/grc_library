# Healthcare Sector GRC Requirements Annex

**Document Title:** Healthcare Sector GRC Requirements Annex 
**Document Type:** Annex 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Compliance Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`compliance/README.md`](README.md), [`compliance/policy-legal-and-regulatory-compliance.md`](policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](register-global-regulatory-applicability.md), [`compliance/matrix-grc-compliance-alignment.md`](matrix-grc-compliance-alignment.md), [`compliance/register-compliance-obligations-template.md`](register-compliance-obligations-template.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`privacy/annex-regional-privacy-requirements.md`](../privacy/annex-regional-privacy-requirements.md), [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md), [`security/policy-information-security.md`](../security/policy-information-security.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](../resilience/standard-business-continuity-and-disaster-recovery.md) 
**Classification:** Public 
**Category:** Compliance: Sector-Specific 
**Review Frequency:** Annual and upon material regulatory change in applicable jurisdictions 
**Repository Path:** [`compliance/annex-healthcare-sector-requirements.md`](annex-healthcare-sector-requirements.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This annex identifies the additional GRC obligations that apply to organizations operating in or adjacent to the healthcare sector. It maps applicable regulatory frameworks to the core GRC library controls and identifies gap areas requiring sector-specific supplementation.

This annex applies where an organization:
- Is a healthcare provider, health insurer, or healthcare clearinghouse (covered entity under HIPAA)
- Processes electronic protected health information (ePHI) or equivalent health data on behalf of a covered entity (business associate)
- Manufactures, distributes, or services connected medical devices
- Provides health information technology, electronic health records (EHR), or clinical decision support systems
- Conducts clinical research involving human subject data
- Handles personal health data under GDPR Article 9 (EU), UK GDPR, or equivalent

---

## Regulatory landscape overview

### United states

| Regulation | Authority | Scope |
|---|---|---|
| **HIPAA Privacy Rule** (45 CFR Part 164, Subpart E) | HHS Office for Civil Rights (OCR) | Covered entities and business associates handling PHI |
| **HIPAA Security Rule** (45 CFR Part 164, Subpart C) | HHS OCR | Covered entities and business associates handling ePHI |
| **HIPAA Breach Notification Rule** (45 CFR Part 164, Subpart D) | HHS OCR | Covered entities and business associates |
| **HITECH Act** (42 U.S.C. §17921 et seq.) | HHS | Strengthens HIPAA; enhanced penalties; meaningful use |
| **21st Century Cures Act** | HHS ONC | Information blocking prohibitions; FHIR interoperability |
| **FDA Cybersecurity Guidance for Medical Devices** (2023) | FDA | Device manufacturers; 510(k) and PMA submissions |
| **FedRAMP** (where applicable) | GSA | Health IT products used by federal healthcare programmes |
| **42 CFR Part 2** | SAMHSA | Substance use disorder treatment records |
| **State breach notification laws** | Varies | Many states have additional or stricter requirements |

### Canada

| Regulation / Standard | Authority | Scope |
|---|---|---|
| **PIPEDA / CPPA** (personal health information provisions) | OPC | Health information about identifiable individuals |
| **PHIPA**: Personal Health Information Protection Act | Ontario IPC | Ontario health information custodians |
| **PIPA** (Alberta) | OIPC Alberta | Alberta health organizations |
| **HIA**: Health Information Act | Alberta | Alberta custodians of health information |
| **PHIA** (Manitoba, Nova Scotia, etc.) | Provincial | Province-specific health information custodians |
| **FINTRAC** | FINTRAC | Pharmacies (AML obligations in some provinces) |

### United kingdom

| Regulation / Standard | Authority | Scope |
|---|---|---|
| **UK GDPR + Data Protection Act 2018** | ICO | All health data processing |
| **NHS Data Security and Protection Toolkit (DSPT)** | NHS England | NHS organizations and their suppliers |
| **CQC Data Security Standards** | Care Quality Commission | Regulated health and social care providers |
| **Caldicott Principles** | National Data Guardian (NDG) | NHS and social care organizations |
| **MHRA regulations** | MHRA | Medical device manufacturers and distributors in UK |

### European union

| Regulation | Authority | Scope |
|---|---|---|
| **GDPR Article 9** | National DPAs | Processing special category data including health data |
| **EU AI Act: High Risk (Annex III)** | EU AI Office | AI systems used in healthcare diagnosis, treatment, monitoring |
| **Medical Device Regulation (MDR) 2017/745** | European Commission / national authorities | Medical device manufacturers and importers in EU |
| **In Vitro Diagnostic Regulation (IVDR) 2017/746** | European Commission | In vitro diagnostic device manufacturers |
| **EU NIS 2 Directive** | National competent authorities | Healthcare essential entities |
| **European Health Data Space (EHDS)** | European Commission | Health data holders and processors: Regulation proposed |

### Global

| Standard | Body | Scope |
|---|---|---|
| **ISO 27799**, Health informatics, Information security management | ISO | Health organizations implementing information security |
| **HL7 FHIR Security** | HL7 International | FHIR API implementers |
| **ISO 13485**: Medical devices quality management | ISO | Medical device manufacturers |
| **IEC 62304**: Medical device software lifecycle | IEC | Medical device software developers |
| **IEC 62443** (cybersecurity for connected devices) | IEC | Medical device manufacturers with network-connected devices |

---

## Key regulatory requirements

### HIPAA security rule

The HIPAA Security Rule establishes three categories of safeguards for ePHI:

#### Administrative safeguards (§164.308)

| Standard | Required / Addressable | GRC Library Mapping |
|---|---|---|
| Security management process: risk analysis | Required | [`risk/procedure-risk-assessment-methodology.md`](../risk/procedure-risk-assessment-methodology.md); [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md) |
| Security management process: risk management | Required | [`risk/template-enterprise-risk-register.md`](../risk/template-enterprise-risk-register.md); [`compliance/procedure-capa.md`](procedure-capa.md) |
| Assigned security responsibility | Required | CISO role definition |
| Workforce training and awareness | Required | [`governance/framework-human-capital-and-ethical-conduct.md`](../governance/framework-human-capital-and-ethical-conduct.md) |
| Access management: authorization and supervision | Addressable | [`security/procedure-access-control.md`](../security/procedure-access-control.md) |
| Workforce clearance procedure | Addressable | Personnel security controls |
| Security incident procedures: response and reporting | Required | [`resilience/procedure-incident-response.md`](../resilience/procedure-incident-response.md) |
| Contingency plan: data backup | Required | [`resilience/procedure-backup-and-recovery.md`](../resilience/procedure-backup-and-recovery.md) |
| Contingency plan: disaster recovery | Required | [`resilience/plan-it-disaster-recovery.md`](../resilience/plan-it-disaster-recovery.md) |
| Contingency plan: emergency mode operations | Required | [`resilience/procedure-crisis-management-eoc-activation.md`](../resilience/procedure-crisis-management-eoc-activation.md) |
| Evaluation: periodic technical and non-technical evaluation | Required | [`compliance/procedure-control-testing.md`](procedure-control-testing.md); [`compliance/standard-internal-audit.md`](standard-internal-audit.md) |
| Business associate contracts | Required | [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md): supplement with BAA template |

#### Physical safeguards (§164.310)

| Standard | GRC Library Mapping |
|---|---|
| Facility access controls | Physical security controls (supplement core library) |
| Workstation use policies | [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md) |
| Device and media controls: disposal | [`operations/register-asset-inventory.md`](../operations/register-asset-inventory.md); media disposal procedures |

#### Technical safeguards (§164.312)

| Standard | Required / Addressable | GRC Library Mapping |
|---|---|---|
| Access control: unique user IDs | Required | [`security/procedure-identity-management.md`](../security/procedure-identity-management.md) |
| Access control: emergency access | Required | Emergency access procedure (supplement) |
| Access control: automatic logoff | Addressable | Endpoint configuration standards |
| Access control: encryption and decryption | Addressable | [`security/framework-cryptographic-key-lifecycle.md`](../security/framework-cryptographic-key-lifecycle.md) |
| Audit controls: hardware and software activity records | Required | [`operations/register-it-security-operations.md`](../operations/register-it-security-operations.md) |
| Integrity controls | Addressable | Data integrity controls |
| Transmission security, encryption | Addressable | [`security/framework-cryptographic-key-lifecycle.md`](../security/framework-cryptographic-key-lifecycle.md), TLS 1.2+ required |

### HIPAA breach notification rule

| Obligation | Threshold | Timeline |
|---|---|---|
| Notification to affected individuals | Any breach of unsecured PHI | Without unreasonable delay; no later than 60 calendar days |
| Notification to HHS | Breaches affecting fewer than 500 individuals | Within 60 days of year end |
| Notification to HHS | Breaches affecting 500+ individuals in a state or jurisdiction | Within 60 days of breach discovery |
| Notification to prominent media | Breaches affecting 500+ individuals in a state | Without unreasonable delay; within 60 days |
| Business associate breach notification to covered entity | Any breach affecting the covered entity's PHI | Within 60 days of discovery |

**HHS OCR investigation triggers:** Any breach affecting 500+ individuals will be investigated by OCR. Penalties up to US$1.9M per violation category per year.

### NHS DSPT (UK)

The NHS Data Security and Protection Toolkit is mandatory for all organizations that access NHS patient data or systems. It is structured around the 10 National Data Guardian Standards.

| NDG Standard | Core Requirement | GRC Library Mapping |
|---|---|---|
| 1. Personal confidential data | Staff understand their responsibilities | [`governance/framework-human-capital-and-ethical-conduct.md`](../governance/framework-human-capital-and-ethical-conduct.md); [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md) |
| 2. Staff responsibilities | All staff have appropriate training | [`governance/framework-human-capital-and-ethical-conduct.md`](../governance/framework-human-capital-and-ethical-conduct.md) |
| 3. Training | Data security training completed annually | Training completion records |
| 4. Managing data access | Access based on legitimate relationship | [`security/procedure-access-control.md`](../security/procedure-access-control.md) |
| 5. Process reviews | Annual review of processes involving patient data | [`compliance/standard-internal-audit.md`](standard-internal-audit.md) |
| 6. Responding to incidents | Processes in place for data security incidents | [`resilience/procedure-incident-response.md`](../resilience/procedure-incident-response.md); [`resilience/procedure-data-protection-and-privacy-breach-response.md`](../resilience/procedure-data-protection-and-privacy-breach-response.md) |
| 7. Continuity planning | Continuity planning incorporating data security | [`resilience/standard-business-continuity-and-disaster-recovery.md`](../resilience/standard-business-continuity-and-disaster-recovery.md) |
| 8. Unsupported systems | Handles risks from unsupported systems | [`operations/register-asset-inventory.md`](../operations/register-asset-inventory.md); lifecycle management |
| 9. IT protection | Cyber security measures deployed | [`security/policy-information-security.md`](../security/policy-information-security.md) |
| 10. Accountable suppliers | Contracts include data security requirements | [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md) |

DSPT submission is annual. Organizations must achieve at minimum "Standards Met" status to maintain NHS data access.

### FDA cybersecurity for medical devices (2023 guidance)

For device manufacturers submitting 510(k), De Novo, or PMA applications after 2023-03-29:

| Requirement | Detail | GRC Library Mapping |
|---|---|---|
| **Cybersecurity management plan** | Plan demonstrating post-market cybersecurity management | [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md): supplement with device-specific plan |
| **SBOM** | Complete SBOM for all device software components | [`dev-security/standard-software-composition-analysis.md`](../dev-security/standard-software-composition-analysis.md) |
| **Threat modelling** | Pre-market threat modelling documentation | Risk assessment methodology: supplement with threat modelling procedure |
| **Vulnerability assessment** | Assessment of known vulnerabilities in SBOM components | [`dev-security/standard-software-composition-analysis.md`](../dev-security/standard-software-composition-analysis.md) |
| **Penetration testing** | Pre-market security testing of device software | [`resilience/procedure-continuity-and-recovery-testing.md`](../resilience/procedure-continuity-and-recovery-testing.md): supplement |
| **Patch management plan** | Plan for timely security patch deployment post-clearance | [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md) |
| **Coordinated vulnerability disclosure** | Policy and process for accepting and responding to security reports | Supplement: vulnerability disclosure policy |
| **Secure by design** | Implement security by design principles | [`dev-security/policy-secure-development-and-engineering.md`](../dev-security/policy-secure-development-and-engineering.md); [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md) |

### GDPR article 9: special category health data

Processing health data as special category data under GDPR requires additional safeguards:

| Obligation | Requirement | GRC Library Mapping |
|---|---|---|
| **Explicit consent or Article 9(2) basis** | Special category health data requires explicit consent or one of the Article 9(2) derogations | [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md); supplement with health data processing basis documentation |
| **Data Protection Impact Assessment** | DPIA mandatory before processing health data at scale | [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../privacy/procedure-privacy-impact-and-cross-border-transfer.md) |
| **Data minimization** | Only collect and process health data actually necessary | Privacy-by-design requirements |
| **Pseudonymization** | Apply pseudonymization where possible | [`security/framework-cryptographic-key-lifecycle.md`](../security/framework-cryptographic-key-lifecycle.md); [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md) |
| **Access controls** | Strict access controls; logs of all access to health records | [`security/procedure-access-control.md`](../security/procedure-access-control.md); [`operations/register-it-security-operations.md`](../operations/register-it-security-operations.md) |
| **Breach notification** | High risk health data breaches require notification within 72 hours | [`resilience/procedure-data-protection-and-privacy-breach-response.md`](../resilience/procedure-data-protection-and-privacy-breach-response.md) |

### Caldicott principles (UK NHS)

In addition to UK GDPR, NHS and social care organizations must apply the 7 Caldicott Principles:

1. Justify the purpose for using confidential information
2. Use only the minimum necessary identifiable information
3. Use the minimum necessary identifiable information
4. Access must be on a strict need-to-know basis
5. Everyone with access must understand their responsibilities
6. Comply with the law
7. The duty to share information can be as important as the duty to protect it

Governance processes should document how each Caldicott Principle is applied to health data processing activities.

---

## Gap analysis: core library vs. healthcare requirements

| Gap Area | Applicable Regulation | Action Required |
|---|---|---|
| Business Associate Agreement (BAA) template | HIPAA §164.314 | Create BAA template for use with all processors of ePHI |
| HIPAA risk analysis methodology | HIPAA §164.308(a)(1) | Document HHS OCR-compliant risk analysis approach using core risk methodology |
| HIPAA breach notification procedure | HIPAA §164.400 to 414 | Create HIPAA-specific breach notification procedure including media notification for 500+ records |
| NHS DSPT annual submission procedure | DSPT | Create DSPT submission procedure and evidence library |
| Caldicott principle compliance documentation | Caldicott / NDG | Document Caldicott principle application to each processing activity |
| Medical device SBOM and cybersecurity plan | FDA 2023 Guidance; MDR/IVDR | Supplement SCA standard with device-specific SBOM and patch management obligations |
| Clinical research data governance | Research ethics frameworks; ICH GCP | Create research data governance procedure |
| ICD / SNOMED / HL7 FHIR data standards compliance | 21st Century Cures; EHDS | Supplement data architecture standards with health data interoperability requirements |
| AI in healthcare high-risk classification | EU AI Act Annex III; FDA SaMD guidance | Supplement AI risk methodology with healthcare-specific AI risk considerations |

---

## Key healthcare-specific controls

The following controls have elevated importance or specific implementation requirements in healthcare:

| Control | Healthcare Requirement | Implementation Guidance |
|---|---|---|
| **Encryption** | ePHI must be rendered unusable/unreadable to fall within HIPAA's safe harbour (reduces breach notification obligation) | Apply NIST SP 800-111 encryption standards; use [`security/framework-cryptographic-key-lifecycle.md`](../security/framework-cryptographic-key-lifecycle.md) |
| **Audit logging** | All access to ePHI must be logged; logs reviewed for suspicious activity | Enhanced logging requirements: log all read access, not just changes |
| **Minimum necessary** | Access to patient data limited to minimum necessary for task | [`security/procedure-access-control.md`](../security/procedure-access-control.md): implement role-based access tied to clinical function |
| **Emergency access** | Documented procedure for emergency access to ePHI when normal authentication is unavailable | Supplement [`security/procedure-access-control.md`](../security/procedure-access-control.md) with break-glass procedure |
| **Workstation security** | Screen locks; automatic logoff for workstations in clinical areas | Endpoint configuration standard: clinical environment settings |
| **Mobile device management** | ePHI on mobile devices must be encrypted and remotely wipeable | Endpoint management platform MDM configuration for clinical devices |
| **Training** | Healthcare privacy training must cover patient confidentiality, right of access, disclosure restrictions | Annual HIPAA/DSPT-specific training track |

---

**End of Document**
