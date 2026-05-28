# Exception and Risk Acceptance Management Policy

**Document Title:** Exception and Risk Acceptance Management Policy 
**Document Type:** Policy 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`governance/charter-governance-library.md`](charter-governance-library.md), [`governance/policy-governance-and-risk-management.md`](policy-governance-and-risk-management.md), [`compliance/policy-compliance-and-audit-management.md`](../compliance/policy-compliance-and-audit-management.md), [`risk/procedure-risk-acceptance.md`](../risk/procedure-risk-acceptance.md) 
**Classification:** Public 
**Category:** Governance 
**Review Frequency:** Annual or as required by regulatory or framework changes 
**Repository Path:** [`governance/policy-exception-and-risk-acceptance-management.md`](policy-exception-and-risk-acceptance-management.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This policy defines the organization-wide process for managing security, risk, compliance, and operational exceptions. It consolidates the former Exception Process, Risk Acceptance Memo Procedure, Temporary Waiver Procedure, and Exception Tracking Log into one cohesive governance artefact.

Its purpose is to ensure that all deviations from policy, control, or standard requirements are risk assessed, time bound, approved at the appropriate authority level, and tracked to closure. The policy aligns with **ISO/IEC 27001:2022 Annex A.5.36 Policy on Exceptions**, **COBIT 2025 APO12.06 Respond to Risk**, **Cloud Security Alliance (CSA)** guidance (CCM v5 GRM-12 Exception Management), and **NIST SP 800-37 Revision 2 RMF Step 6 Authorize the System**.



## Scope

- Applies to all employees, contractors, suppliers, and partners operating or supporting organizational systems across on-premise, cloud, multi-cloud, edge, and AI environments. 
- Covers exceptions to policies, standards, procedures, control requirements, and regulatory or contractual obligations. 
- Includes control configuration baselines, temporary use of unapproved technology, or processes that could affect data integrity or regulated operations. 
- Encompasses trade-security programs under a unified reference model. **Trade and Supply Chain Programs** include WCO SAFE, ISO 28000, BASC, PIP (Canada), CTPAT (United States), AEO (European Union), and equivalent frameworks.



## Governance and accountability

### 1. Governance structure
1.1 The Chief Information Security Officer (CISO) and Chief Information Officer (CIO) co-own the exception management process. 
1.2 The Enterprise Risk Committee (ERC) provides oversight on aggregate risk exposure and expiry compliance. 
1.3 Exception reporting is integrated with enterprise risk dashboards.

### 2. Roles and responsibilities

| Role | Responsibility |
|------|----------------|
| **Requestor** | Initiates the exception request with justification, scope of deviation, proposed compensating controls, and target remediation date. |
| **Risk Owner** | Validates the risk assessment, confirms residual exposure, and ensures that alignment with enterprise risk appetite. |
| **Control Owner** | Confirms impacted control applicability, remediation feasibility, and adequacy of compensating measures. |
| **Chief Information Officer (CIO)** | Approves medium and high-risk exceptions and ensures that exceptions are tracked, reviewed, and reported to executive leadership. |
| **Chief Information Security Officer (CISO)** | Co-approves security-related exceptions, validates risk classification, ensures that technical compensating controls are implemented, and oversees remediation closure. |
| **Chief Compliance Officer (CCO)** | Reviews exceptions impacting regulatory compliance or governance policies, ensuring alignment with ISO 37301 and applicable legal requirements. |
| **Chief Legal Officer / General Counsel (CLO/GC)** | Validates exceptions that could result in regulatory or contractual exposure; provides legal guidance on acceptance documentation. |
| **Enterprise Risk Committee (ERC)** | Reviews aggregated exception metrics, expiry compliance, and exceptions exceeding defined risk appetite. Provides escalation guidance and oversight. |
| **Internal Audit** | Reviews open exceptions, closure evidence, and process adherence. Reports systemic deficiencies and recurring patterns to the Audit Committee. |
| **AI Governance Council** | Reviews exceptions involving AI systems, datasets, or model governance to ensure that alignment with ISO 23894 and NIST AI RMF. Escalates high-risk AI exceptions to the Board Risk Committee. |



## Policy and control statements

### 1. Exception request and registration
1.1 All exceptions shall be documented in the enterprise exception register before deviation occurs. 
1.2 Each entry must include the affected control or standard reference, description and rationale, risk level (low, medium, high, critical), proposed compensating controls, expiry date, approver details, and sign-off evidence. 
1.3 Requests must use the approved template and be submitted via the governance portal or automated workflow.

### 2. Risk assessment and approval
2.1 Exceptions shall undergo risk assessment consistent with ISO 31000 and COBIT APO12.03. 
2.2 Approval levels: 
- **Low risk:** Department Head or equivalent. 
- **Medium risk:** CIO or delegate. 
- **High or critical risk:** Executive Committee or Board Risk Committee. 
- **Trade and customs-related exceptions:** applicable compliance officer co-approval and ERC notification. 
2.3 Exceptions exceeding the organization's defined risk appetite or those impacting trade or customs operations require explicit acceptance by executive authority and validation against trade and supply-chain programs.

### 3. Duration and renewal
3.1 Exceptions shall be time-bound and should not exceed 180 days unless renewed with justification. 
3.2 Renewals must undergo full re-approval and risk reassessment. 
3.3 Expired exceptions must be remediated or escalated immediately.

### 4. Compensating controls and monitoring
4.1 Requestors must implement compensating controls to mitigate risk exposure. 
4.2 Compliance and security teams shall verify compensating control effectiveness within 30 days of approval. 
4.3 Exceptions are subject to monitoring and periodic internal audit review.

### 5. Tracking and reporting
5.1 All active exceptions shall be recorded in a central register with owner, expiry, risk rating, and status metadata. 
5.2 Weekly automated reports shall alert control owners of expiries within 30 days. 
5.3 Quarterly aggregate reports shall summarize exception trends and exposure by domain. A dedicated trade-security exceptions report shall highlight deviations affecting cargo integrity, customs compliance, and logistics controls aligned to the trade and supply-chain programs.

### 6. Closure and verification
6.1 Exception closure requires evidence that corrective actions or control remediation have been implemented. 
6.2 Internal Audit, the CISO, and the CCO must validate closure before record archival. 

### 7. Machine-readable exception registry (future readiness)
7.1 [Unverified] The organization shall implement a machine-readable, API-enabled exception registry mapped to CSA CCM v5 GRM-12. 
7.2 Automated expiry alerts, metadata tagging, and integration with risk dashboards shall support near real-time oversight.

### 8. Continual improvement
8.1 Exception metrics shall be reviewed quarterly for trends, repeat occurrences, and systemic control weaknesses. 
8.2 Lessons learned shall inform control redesign and updates to the risk management framework.



## References and framework alignment

- **ISO/IEC 27001:2022** Annex A.5.36 Policy on Exceptions 
- **ISO 31000:2018** Risk Management 
- **COBIT 2025** APO12.06 Respond to Risk; APO12.03 Assess Risk; MEA01 Monitor Evaluate and Assess 
- **Cloud Security Alliance (CSA)** guidance including CCM v5 GRM-12 Exception Management 
- **NIST SP 800-37 Rev 2** RMF Step 6 Authorize the System; **NIST SP 800-53 Rev 5** CA-6 Authorization 
- **NIST AI RMF 1.1** Govern Function [Unverified] 
- **OECD AI Principles** Accountability and Transparency 
- **Trade and Supply Chain Programs:** WCO SAFE, ISO 28000, BASC, PIP (Canada), CTPAT (United States), AEO (European Union), and equivalents



## Compliance mapping table

| Control Area | ISO/IEC 27001 | COBIT 2025 | CSA | NIST | Legal and Regulatory | Trade and Supply Chain Programs |
|---------------|----------------|-------------|-----|------|----------------------|---------------------------------|
| Governance and oversight | Annex A.5.36 | APO12.06 | CCM GRM-12 | SP 800-37 Step 6 | SOX, GDPR Article 32 Accountability | WCO SAFE equivalence |
| Risk assessment and approval | Clause 6 and ISO 31000 | APO12.03 | CCM GRM-02 | SP 800-30, SP 800-37 Step 3 | CPPA, AIDA | WCO SAFE equivalence |
| Time-bound authorization | Annex A.5.36 | APO12.06 | CCM GRM-12 | SP 800-37 Step 6 | Contractual risk governance | WCO SAFE equivalence |
| Exception tracking and reporting | Annex A.5.36 | MEA01 | CCM GRM-12 | SP 800-53 CA-6 | Audit transparency | WCO SAFE equivalence |
| Closure and validation | Annex A.5.36 | DSS04 | CCM GRM-12 | SP 800-37 Step 6 | Regulatory evidence requirements | WCO SAFE equivalence |
| Machine-readable registry | [Draft 2026 Reference] | APO12.06 | CCM GRM-12 | [Unverified] | Future automation compliance | WCO SAFE equivalence |



## Definitions

Refer to the **Role Authority Register** for definitions of organizational roles and authorities.



**End of Document**
