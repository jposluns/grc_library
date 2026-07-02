# Compliance Obligations Register Template

**Document Title:** Compliance Obligations Register Template\
**Document Type:** Register\
**Version:** 1.0.10\
**Date:** 2026-07-02\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/README.md`](README.md), [`compliance/policy-compliance-and-audit-management.md`](policy-compliance-and-audit-management.md), [`compliance/policy-legal-and-regulatory-compliance.md`](policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](register-global-regulatory-applicability.md), [`compliance/matrix-grc-compliance-alignment.md`](matrix-grc-compliance-alignment.md), [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md), [`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md)\
**Classification:** Public\
**Category:** Compliance Management\
**Review Frequency:** Annual and upon material regulatory or framework change\
**Repository Path:** [`compliance/register-compliance-obligations-template.md`](register-compliance-obligations-template.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template defines the structure, schema, and population guidance for an organization's Compliance Obligations Register. The register provides a single consolidated inventory of all applicable legal, regulatory, contractual, and voluntary obligations, enabling the organization to track compliance status, assign ownership, and prioritize remediation.

---

## Register schema

Each obligation record in the register captures the following fields.

### Identification fields

| Field | Description | Example |
|---|---|---|
| **Obligation ID** | Unique identifier in format `OBL-[YYYY]-[NNN]` | `OBL-2026-001` |
| **Obligation Name** | Short descriptive name | GDPR Article 32: Security of Processing |
| **Source Type** | Legislation / Regulation / Contract / Standard / Voluntary Commitment | Legislation |
| **Source Reference** | Specific law, regulation, clause, or standard section at full granularity. Citations must identify the version (revision, year, or edition) and the specific provision (article, clause, control, or sub-control) so an auditor can resolve the obligation to a single unambiguous source location. See "Source Reference granularity requirements" below. | GDPR Article 32(1)(b); Recital 83 |
| **Jurisdiction** | Applicable jurisdiction(s) | EU; UK (UK GDPR) |

#### Source Reference granularity requirements

The Source Reference field must resolve the obligation to a single unambiguous source location. Each citation type has a minimum granularity requirement; populators must meet or exceed it.

| Source type | Minimum granularity | Acceptable | Unacceptable |
|---|---|---|---|
| **NIST publications** (SP 800-series, FIPS, NIST CSF) | Revision or version *and* control family or specific control ID | `NIST SP 800-53 Rev. 5 AC-2(7)`; `NIST SP 800-171 Rev. 3 §3.1.5`; `NIST CSF 2.0 PR.AA-05` | `NIST 800-53`; `NIST CSF` |
| **ISO/IEC standards** | Standard number *and* year *and* clause or Annex control | `ISO/IEC 27001:2022 Annex A.5.10`; `ISO/IEC 27701:2025 §6.2.1`; `ISO/IEC 27017:2015 CLD.6.3.1` | `ISO 27001`; `ISO/IEC 27001:2022` (without clause) |
| **Statutes and regulations** | Statute/regulation identifier *and* article, section, or subsection | `GDPR Article 28(3)(c)`; `DORA Article 6(2)`; `HIPAA 45 CFR §164.308(a)(1)(ii)(D)`; `SOX §404(b)` | `GDPR`; `DORA`; `HIPAA Security Rule` |
| **COBIT** | Version *and* governance/management objective ID | `COBIT 2019 DSS05.02`; `COBIT 2019 APO13.01` | `COBIT`; `COBIT 2019` (without objective) |
| **PCI DSS** | Version *and* requirement ID | `PCI DSS v4.0 Requirement 8.3.6`; `PCI DSS v4.0.1 §3.5.1.1` | `PCI DSS`; `PCI DSS v4` (without requirement) |
| **Cloud Security Alliance CCM** | Version *and* control ID | `CSA CCM v4.1 IAM-09` | `CCM`; `CSA CCM` |
| **Contracts** | Counterparty *and* contract identifier or title *and* clause | `MSA with Acme Corp, §12.4 (Data Processing)`; `DPA-2026-014 §7` | `customer contract`; `vendor MSA` |
| **Voluntary commitments** | Commitment identifier *and* specific pledge or principle | `UN Global Compact Principle 10`; `TCFD Recommendation B (Strategy) a` | `UN Global Compact`; `TCFD` |

Where an obligation derives from multiple provisions of the same source, list each provision separately rather than collapsing to the standard name. Where the source is a draft or proposed instrument, include the draft identifier and date (e.g., `EU AI Act final text 13 June 2024 Article 9(2)`).

Drift in source versions is itself an obligation-management event: when the underlying standard or statute is updated (for example, a NIST SP publishes a new revision, or an ISO/IEC standard issues a new edition that supersedes a prior one), the register entry must be reviewed and the Source Reference updated as part of the review cycle defined under Ownership and monitoring fields.

### Applicability fields

| Field | Description | Example |
|---|---|---|
| **Trigger Condition** | Condition(s) that make this obligation applicable | Processing personal data of EU/UK data subjects |
| **Applies to Organization?** | Yes / No / Conditional | Yes |
| **Applicability Rationale** | Brief explanation of why the obligation applies | Organization processes EU and UK personal data as a controller |
| **Data Categories Affected** | If privacy-related: categories of personal data in scope | Special category data, financial data |
| **Departments in Scope** | Business functions subject to this obligation | All; IT Operations; HR |

### Obligation content fields

| Field | Description | Example |
|---|---|---|
| **Obligation Summary** | Plain-language statement of what is required | Implement appropriate technical and organizational measures to ensure that data security proportionate to risk is maintained |
| **Specific Requirements** | Discrete requirements derived from the obligation | (1) Encryption of data at rest; (2) Encryption in transit; (3) Ongoing confidentiality and integrity assurance; (4) Ability to restore data; (5) Regular testing of measures |
| **Obligation Type** | Preventive / Detective / Corrective / Reporting / Disclosure | Preventive |
| **Deadline / Trigger Date** | Fixed deadline, recurring date, or event-triggered | Ongoing; by processing start date |

### Control mapping fields

| Field | Description | Example |
|---|---|---|
| **Mapped Controls** | Control IDs or policy references implementing this obligation | ISO 27001 Annex A.8.24; [`security/policy-information-security.md`](../security/policy-information-security.md) |
| **Control Owner** | Role responsible for control implementation | Chief Information Security Officer |
| **Implementation Status** | Not Started / In Progress / Implemented / Verified | Implemented |
| **Implementation Evidence** | Where evidence of compliance can be found | Encryption configuration records; annual control testing report |
| **Gaps Identified** | Known gaps between requirement and current implementation | Mobile device encryption not yet enforced for BYOD |

### Ownership and monitoring fields

| Field | Description | Example |
|---|---|---|
| **Obligation Owner** | Role accountable for this obligation | Data Protection Officer |
| **Reviewer** | Role responsible for periodic review | Legal Counsel |
| **Last Reviewed** | Date of most recent review | 2026-05-01 |
| **Next Review Date** | Scheduled next review | 2027-05-01 |
| **Compliance Status** | Compliant / Partially Compliant / Non-Compliant / Under Assessment | Compliant |
| **Regulatory Risk Rating** | High / Medium / Low: based on penalty, reputational impact | High |

### Reporting and escalation fields

| Field | Description | Example |
|---|---|---|
| **Regulatory Body** | Authority responsible for enforcement | Information Commissioner's Office (ICO); CNIL |
| **Reporting Obligation** | Whether breach or non-compliance must be reported to regulator | Yes: within 72 hours of awareness of breach |
| **Notification Threshold** | Conditions triggering mandatory notification | High risk to individuals; systemic breach |
| **Self-Assessment Due Date** | Date of next regulatory self-assessment or return | Annual; Q1 each calendar year |
| **Notes** | Additional context, related obligations, or cross-references | Cross-reference OBL-2026-002 (UK GDPR Article 33) |

---

## Obligation categories

Populate the register across the following obligation categories. Each category should have its own table or tab in the implementing register.

| Category | Typical Sources | Priority |
|---|---|---|
| **Data Protection and Privacy** | GDPR, UK GDPR, PIPEDA, PIPL, LGPD, Quebec Law 25 | High |
| **Information Security** | ISO 27001, NIST CSF, sector-specific cybersecurity regulations | High |
| **Trade and Customs Compliance** | CTPAT, PIP, AEO-S, BASC, NEEC, OEA, WCO SAFE, import/export regulations | High |
| **AI and Algorithmic Systems** | EU AI Act, AIDA, proposed national AI regulations | High |
| **Employment and Labour Law** | Employment standards legislation per jurisdiction | Medium |
| **Financial Compliance** | Anti-money laundering, financial reporting, tax obligations | Medium |
| **Environmental and Sustainability** | Environmental reporting, emissions disclosure, TCFD | Medium |
| **Contractual Obligations** | Material customer and supplier contractual commitments | Medium |
| **Voluntary Commitments** | ISO certifications, BASC membership, CSR pledges | Low |

---

## Population guidance

### Step 1: Identify applicable obligations
Use [`compliance/register-global-regulatory-applicability.md`](register-global-regulatory-applicability.md) as the source of truth for which jurisdictions and regulatory regimes apply. For each applicable regime, enumerate the specific legal obligations that apply to the organization's activities, data categories, and processing roles.

### Step 2: Assign obligation ids
Use the format `OBL-[YYYY]-[NNN]` where YYYY is the year the obligation was entered into the register. Number sequentially from 001 within each year.

### Step 3: Map to controls
For each obligation, identify the policy, standard, procedure, or control that fulfils it. Where no control exists, record as a gap and initiate a CAPA using [`compliance/procedure-capa.md`](procedure-capa.md).

### Step 4: Assign ownership
Each obligation must have a named role as Obligation Owner. Ownership should align with accountability for the regulated activity, not merely the legal or compliance function.

### Step 5: Set review cadence
High-risk obligations should be reviewed at least annually. Obligations tied to pending regulation should be reviewed as regulatory developments occur.

---

## Compliance status definitions

| Status | Definition |
|---|---|
| **Compliant** | All requirements of the obligation are implemented and verified through evidence |
| **Partially Compliant** | Some requirements implemented; known gaps exist with remediation planned |
| **Non-Compliant** | Obligation is not met; remediation is required immediately |
| **Under Assessment** | Applicability or implementation status is being evaluated |
| **Not Applicable** | Organization has confirmed this obligation does not apply; rationale documented |

---

## Risk rating guidance

Assign Regulatory Risk Rating based on potential consequences of non-compliance:

| Rating | Criteria |
|---|---|
| **High** | Significant financial penalty (e.g., GDPR fines up to 4% global annual turnover); criminal liability; suspension of operating licence; material reputational damage |
| **Medium** | Moderate financial penalty; regulatory warning; potential for escalation to High if not remediated |
| **Low** | Minor administrative penalty; low enforcement priority; limited reputational impact |

---

## Integration with other processes

| Process | Integration Point |
|---|---|
| **Risk Management** | High and Medium-risk obligations should be captured in the enterprise risk register ([`risk/template-enterprise-risk-register.md`](../risk/template-enterprise-risk-register.md)) |
| **Internal Audit** | Compliance obligations register is an input to the annual audit planning process ([`compliance/procedure-audit-planning.md`](procedure-audit-planning.md)) |
| **CAPA** | Non-Compliant and Partially Compliant obligations should have CAPAs raised ([`compliance/procedure-capa.md`](procedure-capa.md)) |
| **Supplier Management** | Contractual obligations to customers and suppliers should flow down to supplier assessments ([`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md)) |

---

**End of Document**
