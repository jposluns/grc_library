# Enterprise Governance and Risk Management Policy

**Document Title:** Enterprise Governance and Risk Management Policy 
**Document Type:** Policy 
**Version:** 1.4.0 
**Date:** 2026-05-28 
**Owner:** Chief Information Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md), [`risk/procedure-risk-register.md`](procedure-risk-register.md), [`risk/procedure-risk-acceptance.md`](procedure-risk-acceptance.md), [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md), [`governance/matrix-cross-framework-alignment.md`](../governance/matrix-cross-framework-alignment.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md) 
**Classification:** Public 
**Category:** Risk Management 
**Review Frequency:** Annual or as required by regulatory or framework changes 
**Repository Path:** [`risk/policy-enterprise-governance-and-risk-management.md`](policy-enterprise-governance-and-risk-management.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## 1. Purpose

This policy establishes the enterprise governance and risk management framework, principles, roles, and control requirements that guide consistent identification, assessment, treatment, monitoring, and reporting of risk across the organization. It is aligned with ISO 31000 Clauses 5 and 6, COBIT 2025 APO12, CSA CCM v5 GRM domain, NIST SP 800-39, ISO 23894 for AI risk, and the NIST AI RMF. The policy integrates risk, compliance, privacy, security, resilience, ethics, and sustainability across business, technology, data, and AI systems.

---

## 2. Scope

1. This policy applies to all business units, regions, subsidiaries, and joint ventures where the organization has operational control, including BASC-certified logistics operations in Latin America (Colombia, Mexico, Peru, and Chile).
2. It covers strategic, operational, financial, compliance, information security, privacy, safety, environmental, AI, and supply-chain risks across on-premises, cloud, multi-cloud, edge, and supplier-hosted services.
3. It applies to all employees, contractors, suppliers, and partners who process organizational or trade data, handle cargo, or operate customs-facing systems.
4. It encompasses trade-security and supply-chain risk management aligned to globally recognized programmes including WCO SAFE, ISO 28000, BASC, PIP (Canada), CTPAT (United States), AEO (European Union), AEO-S (United Kingdom), NEEC (Mexico), OEA (Brazil), and equivalent frameworks.

---

## 3. Governance and accountability

| Role | Responsibility |
|---|---|
| Board Risk Committee | Approves risk appetite statements; receives enterprise risk reporting. |
| Enterprise Risk Committee (ERC) | Meets quarterly to oversee risk posture, treatment progress, and escalated items. |
| AI Governance Council (AIGC) | Approves AI risk appetite statements and exceptions for high-risk AI uses per ISO 23894 and NIST AI RMF Govern function; meets monthly. |
| Chief Information Officer | Accountable for the enterprise risk management framework. |
| Chief Information Security Officer | Responsible for information security, privacy, and AI risk integration. |
| Second Line: GRC Function | Sets policy; consolidates risk reporting across the organization. |
| Third Line: Internal Audit | Provides independent assurance on governance and control effectiveness. |
| Executive Sponsors | Each material risk category is assigned an executive sponsor. |
| Operational Risk Owners | Manage day-to-day risk identification, control execution, and residual exposure reporting. |

The organization operates the **Three Lines Model**:

- **First Line:** Business units and process owners own and manage risk within their domains.
- **Second Line:** The GRC function sets policy, frameworks, and consolidated reporting.
- **Third Line:** Internal Audit provides independent, objective assurance.

---

## 4. Policy statements

### 4.1 Risk framework

The organization shall maintain a standard risk management framework aligned to ISO 31000 with a common taxonomy, scoring criteria, and risk registers used consistently across all units and regions.

### 4.2 Risk identification

Risk identification shall cover strategic, financial, operational, compliance, information security, privacy, third-party, business continuity, and AI-specific risks as defined in ISO 23894. Identification activities shall be conducted at programme inception, upon material change, and at each scheduled review cycle.

### 4.3 Risk analysis

Risk analysis shall use both qualitative and quantitative methods. Where AI-driven business processes are involved, FAIR-AI methodologies shall be applied to support quantitative loss estimation and scenario analysis.

### 4.4 Risk appetite

The Board shall approve risk appetite statements for each material risk category, including defined AI usage classes. Appetite statements shall set boundaries for acceptable risk exposure and escalation thresholds.

### 4.5 Risk treatment

Risk treatment plans shall document the selected option (avoid, mitigate, transfer, accept, or exploit), the accountable owner, required budget, expected residual risk, and acceptance criteria, consistent with COBIT 2025 APO12.06. Accepted risks shall follow the Risk Acceptance Procedure.

### 4.6 AI risk controls

Controls governing AI systems shall address, at minimum:

- Dataset governance and lineage tracking.
- Model lifecycle governance (development, validation, deployment, retirement).
- Safety testing and adversarial robustness assessment.
- Bias detection and fairness testing.
- Human-in-the-loop requirements for high-risk decisions.
- Secure deployment and supply-chain integrity.
- Continuous monitoring for model drift, bias recurrence, and ethical deviations.

These requirements are aligned with ISO 23894 and the NIST AI RMF (Govern, Map, Measure, Manage functions).

### 4.7 Risk monitoring and key risk indicators

Key Risk Indicators (KRIs) and control performance indicators shall be defined, baselined, and reviewed at minimum quarterly. Material changes in KRI trend shall be escalated to the ERC within the reporting cycle in which they are detected.

### 4.8 Reporting

Consolidated enterprise risk reporting shall be presented to executive leadership and the Board Risk Committee at least quarterly, with an annual summary. AI risk trends shall be included in consolidated reporting.

---

## 5. Roles and responsibilities summary

| Activity | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Risk appetite approval | Board Risk Committee | Board Risk Committee | ERC, AIGC | All employees |
| AI risk appetite and exceptions | AIGC | CIO | CISO | ERC |
| Enterprise risk register | Risk Manager / Compliance Officer | CIO | Process Owners | ERC |
| Control design and operation | Process and System Owners | Executive Sponsors | CISO | Internal Audit |
| Independent assurance | Internal Audit | Chief Audit Executive | GRC | Board Risk Committee |
| Quarterly risk reporting | GRC Function | CIO | CISO | ERC, Board |

---

## 6. Related documents

- Enterprise Risk Management Standard: methodology, taxonomy, and scoring
- Risk Register Procedure
- Third-Party Risk Standard and Due Diligence Procedure
- Business Continuity and Disaster Recovery Standard
- Privacy Impact Assessment and Cross-Border Transfer Procedure
- AI Security and Risk Standard
- Logging and Monitoring Standard

---

## 7. Framework alignment

| Framework | Relevant Clauses or Functions |
|---|---|
| ISO 31000:2018 | Clause 5, Framework; Clause 6, Process |
| ISO 23894:2023 | AI Risk Management |
| ISO/IEC 42001:2023 | AI Management System |
| COBIT 2025 | APO12 Manage Risk; APO10 Manage Suppliers; MEA01; DSS04 |
| CSA CCM v5 | GRM domain; BCR domain; GOV domain; AIS domain |
| NIST SP 800-39 | Managing Information Security Risk |
| NIST AI RMF | Govern, Map, Measure, Manage |
| OECD AI Principles | Transparency, robustness, accountability |
| GDPR | As applicable to EU personal data |
| CPPA | As applicable to Canadian personal information |
| PIPL | As applicable to personal information in China |
| LGPD | As applicable to Brazilian personal data |
| CBPR 2.0 | Cross-Border Privacy Rules as applicable |

---

## 8. Exceptions

Exceptions to this policy require documented justification, a compensating control, approval by the CIO, and time-bounded review. AI-related exceptions additionally require AIGC approval. All exceptions shall be logged in the risk register.

---

## 9. Enforcement

Non-compliance with this policy may result in disciplinary action up to and including termination of employment or contract, and may be reported to relevant regulatory authorities where required by law.

---

## 10. License

This document is released under the **CC0 1.0 Universal** public domain dedication. To the extent possible under law, the organization waives all copyright and related rights to this document.

---

**End of Document**
