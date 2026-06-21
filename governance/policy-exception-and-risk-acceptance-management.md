# Exception and Risk Acceptance Management Policy

**Document Title:** Exception and Risk Acceptance Management Policy\
**Document Type:** Policy\
**Version:** 1.1.1\
**Date:** 2026-06-21\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/charter-governance-library.md`](charter-governance-library.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md), [`compliance/policy-compliance-and-audit-management.md`](../compliance/policy-compliance-and-audit-management.md), [`risk/procedure-risk-acceptance.md`](../risk/procedure-risk-acceptance.md)\
**Classification:** Public\
**Category:** Governance\
**Review Frequency:** Annual or as required by regulatory or framework changes\
**Repository Path:** [`governance/policy-exception-and-risk-acceptance-management.md`](policy-exception-and-risk-acceptance-management.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This policy defines the organisation-wide process for managing security, risk, compliance, and operational exceptions. It consolidates the former Exception Process, Risk Acceptance Memo Procedure, Temporary Waiver Procedure, and Exception Tracking Log into one cohesive governance artefact.

Its purpose is to ensure that all deviations from policy, control, or standard requirements are risk assessed, time bound, approved at the appropriate authority level, and tracked to closure. The policy aligns with **ISO/IEC 27001:2022 Annex A.5.36 Policy on Exceptions**, **COBIT 2019 APO12.06 Respond to Risk**, **Cloud Security Alliance (CSA)** guidance (CCM v4.1 GRC-12 Exception Management), and **NIST SP 800-37 Revision 2 RMF Step 6 Authorize the System**.

## Scope

- Applies to all employees, contractors, suppliers, and partners operating or supporting organisational systems across on-premise, cloud, multi-cloud, edge, and AI environments. 
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
1.2 Each entry must include the affected control or standard reference, description and rationale, risk level (low, medium, high, critical), proposed compensating controls, expiry date, approver details, sign-off evidence, the exception's `max_duration` (the absolute maximum cumulative lifetime including all renewals, defaulting to 540 days, see §3.4), and the exception's `renewal_count_limit` (the absolute maximum number of renewals permitted, defaulting to 3, see §3.5). 
1.3 Requests must use the approved template and be submitted via the governance portal or automated workflow.

### 2. Risk assessment and approval
2.1 Exceptions shall undergo risk assessment consistent with ISO 31000 and COBIT APO12.03. 
2.2 Approval levels: 
- **Low risk:** Department Head or equivalent. 
- **Medium risk:** CIO or delegate. 
- **High or critical risk:** Executive Committee or Board Risk Committee. 
- **Trade and customs-related exceptions:** applicable compliance officer co-approval and ERC notification. 
2.3 Exceptions exceeding the organisation's defined risk appetite or those impacting trade or customs operations require explicit acceptance by executive authority and validation against trade and supply-chain programs.

### 3. Duration and renewal
3.1 Exceptions shall be time-bound. The initial term shall not exceed 180 days. 
3.2 Renewals must undergo full re-approval and risk reassessment. 
3.3 Expired exceptions must be remediated or escalated immediately.

3.4 **Maximum cumulative duration (`max_duration`).** The cumulative lifetime of an exception, summed across the initial term and all renewals, shall not exceed 540 days (three 180-day terms) unless an explicit higher cap has been recorded on the register entry and approved by the Board Risk Committee (or, where the organisation has no Board Risk Committee, the highest governance body to which the ERC reports) at the time the exception was first registered. A `max_duration` recorded on the entry is a hard ceiling: when reached, the exception must be remediated, descoped, converted to a documented risk acceptance per [`risk/procedure-risk-acceptance.md`](../risk/procedure-risk-acceptance.md), or replaced by a re-baselined entry per §3.6. Further renewal is not permitted at any authority level.

3.5 **Renewal count limit (`renewal_count_limit`) and renewal-ceiling escalation pathway.** Approval authority for a renewal does not, on its own, authorise an unbounded sequence of renewals. The following hard ceilings apply to every exception regardless of risk classification:

| Renewal number | Required approving authority | Additional requirement |
|----------------|------------------------------|------------------------|
| **1st renewal** | The same authority that approved the original exception under the §2 approval pathway | Documented justification, refreshed risk assessment, evidence that compensating controls remain effective |
| **2nd renewal** | Enterprise Risk Committee (ERC) review and approval | A written remediation-feasibility memo from the requestor; confirmation that compensating controls have been re-validated within the prior 30 days; an explicit ERC determination that the residual exposure remains within risk appetite |
| **3rd renewal** | Board Risk Committee (or, where the organisation has no Board Risk Committee, the highest governance body to which the ERC reports) review and approval | A written root-cause-and-remediation-pathway memo (why has the underlying gap not been closed across two prior renewals? what is the binding remediation deadline?); explicit Board Risk Committee acceptance of the residual risk of continued non-closure; the Board Risk Committee may also require remediation by a fixed date, conversion to a formal risk acceptance, or descope of the underlying requirement in lieu of further renewal |
| **4th renewal or beyond** | Not permitted under this policy | The exception must be closed (with the residual gap formally accepted as a risk under [`risk/procedure-risk-acceptance.md`](../risk/procedure-risk-acceptance.md)), descoped (the underlying control requirement re-scoped or formally waived), or replaced by a re-baselined entry per §3.6. A 4th renewal must not be granted by any authority. |

The `renewal_count_limit` field defaults to 3 (the value at which the 4th-renewal prohibition takes effect). A lower limit may be recorded on individual entries by the approving authority where the risk profile warrants a tighter cap. A higher limit shall not be recorded; the absolute prohibition on a 4th renewal is policy-wide and cannot be raised through the entry field.

The renewal number and the approving authority shall be recorded on the exception register entry as part of each renewal event so the cumulative count is auditable.

3.6 **Re-baselining carve-out.** An exception whose underlying scope has materially changed (for example, a new control requirement supersedes the original or a structural change in the affected system alters the nature of the deviation) may be re-baselined: a fresh exception register entry is opened, the renewal count is reset to zero, the `max_duration` clock is reset, and the new entry undergoes the full §2 approval pathway from scratch. Re-baselining requires ERC approval and is recorded on the register with an explicit cross-reference to the prior entry so the history is auditable; re-baselining is not a renewal and does not consume a renewal slot. Re-baselining must not be used to bypass the ceiling: a re-baseline that does not rest on a materially-changed underlying scope is treated as the next renewal in the sequence (the ERC declines the re-baseline and the count continues).

3.7 **Rationale for the specific numbers.** The 540-day `max_duration` default corresponds to three full 180-day terms and ensures that any exception still active after eighteen months has received governance attention at every approval tier (original approver, ERC, Board Risk Committee). The 2-renewal ERC threshold mirrors the equivalent threshold in [`compliance/procedure-capa.md`](../compliance/procedure-capa.md) §6.3.1 for CAPA extensions, so the two registers escalate on the same cadence when both have been opened against the same underlying gap. The 3-renewal Board Risk Committee threshold reflects that an exception which has been renewed three times is no longer a remediation-programme issue but a governance-risk issue requiring the highest oversight body's explicit acceptance of the residual exposure. The 4-renewal absolute prohibition forces a binary decision (close, descope, convert to risk acceptance, or re-baseline) rather than allowing indefinite drift through serial soft renewals.

### 4. Compensating controls and monitoring
4.1 Requestors must implement compensating controls to mitigate risk exposure. 
4.2 Compliance and security teams shall verify compensating control effectiveness within 30 days of approval. 
4.3 Exceptions are subject to monitoring and periodic internal audit review.

### 5. Tracking and reporting
5.1 All active exceptions shall be recorded in a central register with owner, expiry, risk rating, status metadata, `max_duration` per §3.4, `renewal_count_limit` per §3.5, and current renewal count. 
5.2 Each exception register entry shall record the ID of the related risk-acceptance record (if any) per [`risk/procedure-risk-acceptance.md`](../risk/procedure-risk-acceptance.md) "Required record fields"; record `None` if the exception is a policy/control deviation that did not produce a separate risk acceptance. This linkage makes the exception register and risk-acceptance register cross-traversable: an auditor reviewing a risk acceptance can find the corresponding exception and vice versa. 
5.3 Weekly automated reports shall alert control owners of expiries within 30 days. 
5.4 Quarterly aggregate reports shall summarize exception trends and exposure by domain. A dedicated trade-security exceptions report shall highlight deviations affecting cargo integrity, customs compliance, and logistics controls aligned to the trade and supply-chain programs.

### 6. Closure and verification
6.1 Exception closure requires evidence that corrective actions or control remediation have been implemented. 
6.2 Internal Audit, the CISO, and the CCO must validate closure before record archival. 

### 7. Machine-readable exception registry (recommended where automation is practical)
7.1 Organisations may implement a machine-readable, API-enabled exception registry aligned with CSA CCM v4.1 GRC-12. This is a recommended practice rather than a mandatory requirement; it is appropriate where the exception volume and integration with risk dashboards justify the automation investment.
7.2 Where implemented, automated expiry alerts, metadata tagging, and integration with risk dashboards support near real-time oversight.

### 8. Continual improvement
8.1 Exception metrics shall be reviewed quarterly for trends, repeat occurrences, and systemic control weaknesses. 
8.2 Lessons learned shall inform control redesign and updates to the risk management framework.



## References and framework alignment

- **ISO/IEC 27001:2022** Annex A.5.36 Policy on Exceptions 
- **ISO 31000:2018** Risk Management 
- **COBIT 2019** APO12.06 Respond to Risk; APO12.03 Assess Risk; MEA01 Monitor Evaluate and Assess 
- **Cloud Security Alliance (CSA)** guidance including CCM v4.1 GRC-12 Exception Management 
- **NIST SP 800-37 Rev 2** RMF Step 6 Authorize the System; **NIST SP 800-53 Rev 5** CA-6 Authorization 
- **NIST AI RMF 1.0** Govern Function (with the AI 600-1 Generative AI Profile)
- **OECD AI Principles** Accountability and Transparency 
- **Trade and Supply Chain Programs:** WCO SAFE, ISO 28000, BASC, PIP (Canada), CTPAT (United States), AEO (European Union), and equivalents



## Compliance mapping table

| Control Area | ISO/IEC 27001 | COBIT 2019 | CSA | NIST | Legal and Regulatory | Trade and Supply Chain Programs |
|---------------|----------------|-------------|-----|------|----------------------|---------------------------------|
| Governance and oversight | Annex A.5.36 | APO12.06 | CCM GRC-12 | SP 800-37 Step 6 | SOX, GDPR Article 32 Accountability | WCO SAFE equivalence |
| Risk assessment and approval | Clause 6 and ISO 31000 | APO12.03 | CCM GRC-02 | SP 800-30, SP 800-37 Step 3 | CPPA, AIDA | WCO SAFE equivalence |
| Time-bound authorization | Annex A.5.36 | APO12.06 | CCM GRC-12 | SP 800-37 Step 6 | Contractual risk governance | WCO SAFE equivalence |
| Exception tracking and reporting | Annex A.5.36 | MEA01 | CCM GRC-12 | SP 800-53 CA-6 | Audit transparency | WCO SAFE equivalence |
| Closure and validation | Annex A.5.36 | DSS04 | CCM GRC-12 | SP 800-37 Step 6 | Regulatory evidence requirements | WCO SAFE equivalence |
| Machine-readable registry (recommended) | Annex A.5.36 (extension) | APO12.06 | CCM GRC-12 | SP 800-53 CA-6 (extension) | Future automation compliance | WCO SAFE equivalence |



## Definitions

Refer to the **Role Authority Register** for definitions of organisational roles and authorities.



**End of Document**
