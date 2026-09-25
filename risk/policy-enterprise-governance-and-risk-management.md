# Enterprise Governance and Risk Management Policy

**Document Title:** Enterprise Governance and Risk Management Policy\
**Document Type:** Policy\
**Version:** 1.4.20\
**Date:** 2026-09-25\
**Owner:** Chief Risk Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md), [`risk/procedure-risk-register.md`](procedure-risk-register.md), [`risk/procedure-risk-acceptance.md`](procedure-risk-acceptance.md), [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md), [`governance/matrix-cross-framework-alignment.md`](../governance/matrix-cross-framework-alignment.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md)\
**Classification:** Public\
**Category:** Risk Management\
**Review Frequency:** Annual or as required by regulatory or framework changes\
**Repository Path:** [`risk/policy-enterprise-governance-and-risk-management.md`](policy-enterprise-governance-and-risk-management.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This policy establishes the enterprise governance and risk management framework, principles, roles, and control requirements that guide consistent identification, assessment, treatment, monitoring, and reporting of risk across the organization. It is aligned with ISO 31000:2018 Clauses 5 and 6, COBIT 2019 APO12, CSA CCM v4.1 GRC domain, NIST SP 800-39, ISO/IEC 23894:2023 for AI risk, and the NIST AI RMF. The policy integrates risk, compliance, privacy, security, resilience, ethics, and sustainability across business, technology, data, and AI systems.

---

## 2. Scope

1. This policy applies to all business units, regions, subsidiaries, and joint ventures where the organization has operational control.
2. It covers strategic, operational, financial, compliance, information security, privacy, safety, environmental, AI, and supply-chain risks across on-premises, cloud, multi-cloud, edge, and supplier-hosted services.
3. It applies to all employees, contractors, suppliers, and partners who process organizational data or operate organization-controlled systems.
4. Where the organization participates in trade-security and supply-chain programmes (for example, WCO SAFE, ISO 28000:2022, BASC, PIP, CTPAT, AEO, AEO-S, NEEC, OEA, and equivalent frameworks), the relevant sector annex extends this policy with programme-specific obligations; see [`compliance/`](../compliance/) and the transportation and logistics sector annex.

---

## 3. Governance and accountability

| Role | Responsibility |
|---|---|
| Board Risk Committee | Approves risk appetite statements; receives enterprise risk reporting. |
| Enterprise Risk Committee (ERC) | Meets quarterly to oversee risk posture, treatment progress, and escalated items. |
| AI Governance Council (AIGC) | Approves AI risk appetite statements and co-approves AI-related exceptions (in addition to the risk-tier approver in the [Exception and Risk Acceptance Management Policy](../governance/policy-exception-and-risk-acceptance-management.md), §4.2.2), under arrangements informed by ISO/IEC 23894:2023 and the NIST AI RMF Govern function; meets monthly (an organization-defined cadence). |
| Chief Risk Officer | Accountable for the enterprise risk management framework and its alignment with strategic objectives; owns risk strategy, risk-appetite stewardship, and ERM-programme outcomes; reports to the Board Risk Committee. |
| Chief Information Officer | Provides executive support to the ERM programme on technology-risk integration; ensures that IT-strategy risk is reflected in the enterprise risk register. |
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

The organization must maintain a standard risk management framework aligned to ISO 31000:2018 with a common taxonomy, scoring criteria, and risk registers used consistently across all units and regions.

### 4.2 Risk identification

Risk identification must cover strategic, financial, operational, compliance, information security, privacy, third-party, business continuity, and AI-specific risks (the organization's categories, informed by the risk sources in ISO/IEC 23894:2023 Annex B). Identification activities must be conducted at programme inception, upon material change, and at each scheduled review cycle.

### 4.3 Risk analysis

Risk analysis must use both qualitative and quantitative methods. Where AI-driven business processes are involved, FAIR-AI methodologies must be applied to support quantitative loss estimation and scenario analysis.

### 4.4 Risk appetite

The Board must approve risk appetite statements for each material risk category, including defined AI usage classes. Appetite statements must set boundaries for acceptable risk exposure and escalation thresholds.

### 4.5 Risk treatment

Risk treatment plans must document the selected option (one of the canonical six per `risk/standard-enterprise-risk-management.md` Section 6: avoid, mitigate, transfer, accept, exploit, or enhance), the accountable owner, required budget, expected residual risk, and acceptance criteria, consistent with COBIT 2019 APO12.06. Accepted risks must follow the Risk Acceptance Procedure.

### 4.6 AI risk controls

Controls governing AI systems must address, at minimum:

- Dataset governance and lineage tracking.
- Model lifecycle governance (development, validation, deployment, retirement).
- Safety testing and adversarial robustness assessment.
- Bias detection and fairness testing.
- Human-in-the-loop requirements for high-risk decisions.
- Secure deployment and supply-chain integrity.
- Continuous monitoring for model drift, bias recurrence, and ethical deviations.

These requirements are aligned with ISO/IEC 23894:2023 and the NIST AI RMF (GOVERN 1.3, 1.5, 2.1; MAP 1.5; MEASURE 1.1; MANAGE 1.2, 1.3, 1.4).

### 4.7 Risk monitoring and key risk indicators

Key Risk Indicators (KRIs) and control performance indicators must be defined, baselined, and reviewed at minimum quarterly. Material changes in KRI trend must be escalated to the ERC within the reporting cycle in which they are detected.

### 4.8 Reporting

Consolidated enterprise risk reporting must be presented to executive leadership and the Board Risk Committee at least quarterly, with an annual summary. AI risk trends must be included in consolidated reporting.

---

## 5. Roles and responsibilities summary

| Activity | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Risk appetite approval | Board Risk Committee | Board Risk Committee | ERC, AIGC | All employees |
| AI policy exceptions | AIGC | Tiered per the [Exception and Risk Acceptance Management Policy](../governance/policy-exception-and-risk-acceptance-management.md) §4.2.2 (with the §4.3.5 renewal escalation), and AIGC co-approval for AI-related exceptions | CISO | ERC |
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
| ISO 31000:2018 | Clause 4 (principles), Clause 5 (framework), Clause 6 (process) |
| ISO/IEC 23894:2023 | Clause 4 (AI risk principles), Clause 5 (framework), Clause 6 (AI risk process) |
| ISO/IEC 42001:2023 | §5.2, §5.3, §6.1.2, §6.1.3, §6.1.4, §9.1 (AI policy, roles, risk assessment/treatment/impact, monitoring) |
| COBIT 2019 | APO12.01, APO12.02, APO12.03, APO12.04, APO12.05, APO10.04, MEA01.02, MEA01.04, DSS04.02 |
| CSA CCM v4.1 | GRC-01, GRC-02, GRC-04, GRC-06, BCR-02, AIS-06 |
| CSA AICM v1.1 | GRC-11 Bias and Fairness Assessment; GRC-15 Human supervision |
| NIST SP 800-39 | Chapters 2 and 3 (multitiered fundamentals; framing, assessing, responding, monitoring) |
| NIST AI RMF | GOVERN 1.3, 1.5, 2.1; MAP 1.5; MEASURE 1.1; MANAGE 1.2, 1.3, 1.4 |
| OECD AI Principles | Principles 1.3 (transparency and explainability), 1.4 (robustness, security and safety), 1.5 (accountability) |
| GDPR | As applicable to EU personal data |
| PIPEDA | As applicable to Canadian personal information |
| PIPL | As applicable to personal information in China |
| LGPD | As applicable to Brazilian personal data |
| APEC CBPR | Cross-Border Privacy Rules as applicable |

---

## 8. Exceptions

Exceptions to this policy must be documented under the [Exception and Risk Acceptance Management Policy](../governance/policy-exception-and-risk-acceptance-management.md) and approved through its §4.2.2 risk-tier pathway, with CISO co-approval for security-related exceptions in addition to, not in place of, the risk-tier approver; duration and renewal follow its §4.3. AI-related exceptions additionally require AIGC co-approval (in addition to, not in place of, the risk-tier approver). All exceptions must be logged in the enterprise exception register.

---

## 9. Enforcement

Non-compliance with this policy may result in disciplinary action up to and including termination of employment or contract, and may be reported to relevant regulatory authorities where required by law.

---

## 10. Licence

This document is released under the **CC BY-SA 4.0** licence. To the extent possible under law, the organization waives all copyright and related rights to this document.

---

**End of Document**
