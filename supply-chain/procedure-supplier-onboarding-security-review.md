# Supplier Onboarding Security Review Procedure

**Document Title:** Supplier Onboarding Security Review Procedure 
**Document Type:** Procedure 
**Version:** 1.0.1 
**Date:** 2026-05-28 
**Owner:** Supplier Risk Maintainer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`supply-chain/README.md`](README.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md), [`supply-chain/procedure-supplier-due-diligence.md`](procedure-supplier-due-diligence.md), [`supply-chain/template-supplier-security-questionnaire.md`](template-supplier-security-questionnaire.md), [`supply-chain/register-supplier-risk-template.md`](register-supplier-risk-template.md), [`supply-chain/register-subprocessor-template.md`](register-subprocessor-template.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../privacy/procedure-privacy-impact-and-cross-border-transfer.md), [`compliance/policy-compliance-and-audit-management.md`](../compliance/policy-compliance-and-audit-management.md) 
**Classification:** Public 
**Category:** Supply Chain Governance: Onboarding 
**Review Frequency:** Annual and upon significant process change or regulatory update 
**Repository Path:** [`supply-chain/procedure-supplier-onboarding-security-review.md`](procedure-supplier-onboarding-security-review.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This procedure defines the steps, gates, and responsibilities for conducting a security review as part of the supplier onboarding process. It ensures that every new supplier is risk-classified, assessed against the requirements of [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md), and approved before receiving access to organisation systems, data, or networks.

---

## Trigger

This procedure is triggered when:
- A business unit proposes engaging a new supplier, vendor, or service provider
- An existing supplier materially expands its scope of service or access
- A supplier is acquired by or merged with another entity

---

## Roles and responsibilities

| Role | Responsibility |
|---|---|
| **Requesting Business Unit** | Initiates the onboarding request; provides business justification and proposed scope |
| **Supplier Risk Manager** | Coordinates and leads the security review; owns the process |
| **Legal / Procurement** | Reviews and executes contractual requirements; ensures that DPA where applicable |
| **Data Protection Officer (DPO)** | Advises on privacy requirements; approves DPA; directs DPIA where needed |
| **Information Security** | Technical security review for Tier 1 and Tier 2 suppliers |
| **IT Operations** | Reviews access and integration requirements; provisions access post-approval |
| **Chief Risk Officer** | Final approval for Tier 1 and high-risk Tier 2 suppliers |

---

## Procedure steps

### Step 1: Onboarding request and initial classification

| Action | Responsible | Timeframe |
|---|---|---|
| 1.1 Submit onboarding request including: proposed supplier name and services; business justification; scope of data access; anticipated system integrations; trade compliance programme relevance | Requesting Business Unit | Before any supplier engagement |
| 1.2 Assign a Supplier ID using the organisation's supplier registry | Supplier Risk Manager | Within 2 business days |
| 1.3 Classify the supplier into Tier 1 to 4 using criteria in [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md) | Supplier Risk Manager | Within 2 business days |
| 1.4 Determine if the supplier will process personal data (triggers DPA requirement) | Supplier Risk Manager / DPO | Within 2 business days |
| 1.5 Determine if the supplier is a logistics partner subject to trade compliance programme requirements (CTPAT, AEO-S, PIP, BASC) | Supplier Risk Manager / Trade Compliance | Within 2 business days |
| 1.6 Record classification in [`supply-chain/register-supplier-risk-template.md`](register-supplier-risk-template.md) | Supplier Risk Manager | Within 2 business days |

### Step 2: Security and privacy assessment

| Action | Responsible | Timeframe |
|---|---|---|
| 2.1 Send the supplier security questionnaire ([`supply-chain/template-supplier-security-questionnaire.md`](template-supplier-security-questionnaire.md)) appropriate to their tier | Supplier Risk Manager | Within 3 business days of classification |
| 2.2 Request supporting evidence as required by tier (ISO 27001 certificate; SOC 2 report; pen test attestation; etc.): see [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md) | Supplier Risk Manager | With questionnaire |
| 2.3 Conduct a DPIA screening: determine whether a full DPIA is required using [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../privacy/procedure-privacy-impact-and-cross-border-transfer.md) | DPO | Within 3 business days of Step 1 |
| 2.4 If cross-border data transfer: confirm adequate transfer mechanism (SCCs, IDTA, adequacy) and conduct transfer impact assessment if required | DPO / Legal | Before contract execution |
| 2.5 Review completed questionnaire and evidence against assurance requirements | Supplier Risk Manager / Information Security | Within 5 business days of receipt |
| 2.6 For Tier 1: conduct reference checks; review any publicly available incident history; assess financial solvency | Supplier Risk Manager | During Step 2 |
| 2.7 For logistics suppliers: verify current CTPAT / AEO-S / PIP / BASC / NEEC / OEA certification status as applicable | Trade Compliance Manager | During Step 2 |

**Supplier response deadlines:** Tier 1, 10 business days; Tier 2, 10 business days; Tier 3: 15 business days. Escalate to Requesting Business Unit if supplier does not respond.

### Step 3: Gap analysis and risk assessment

| Action | Responsible | Timeframe |
|---|---|---|
| 3.1 Document any security or privacy gaps against [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md) requirements | Supplier Risk Manager | Within 3 business days of assessment |
| 3.2 Assign inherent and residual risk scores using [`risk/procedure-risk-assessment-methodology.md`](../risk/procedure-risk-assessment-methodology.md) | Supplier Risk Manager | During Step 3 |
| 3.3 Determine risk rating and whether residual risk is within appetite ([`risk/template-risk-appetite-statement.md`](../risk/template-risk-appetite-statement.md)) | Supplier Risk Manager / CRO | During Step 3 |
| 3.4 For High or Critical residual risk: document treatment options and required contractual protections | Supplier Risk Manager / CRO | During Step 3 |
| 3.5 If DPIA required: complete full DPIA and obtain DPO sign-off | DPO | Before contract execution |
| 3.6 For suppliers where residual risk exceeds appetite: escalate to CRO for approval decision (proceed / do not proceed / proceed with conditions) | Supplier Risk Manager | Before contract execution |

### Step 4: Contract and agreement execution

| Action | Responsible | Timeframe |
|---|---|---|
| 4.1 Confirm minimum contract clauses required per [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md) are included | Legal / Supplier Risk Manager | Before contract execution |
| 4.2 Execute Data Processing Agreement where personal data will be processed | DPO / Legal | Before any personal data is shared |
| 4.3 For logistics suppliers: confirm trade compliance programme obligations are included in contract (where applicable) | Trade Compliance / Legal | Before contract execution |
| 4.4 Obtain signed confidentiality and data handling acknowledgement from supplier where applicable | Legal | Before any data is shared |
| 4.5 File executed contract and DPA in the contract management system | Legal / Procurement | Upon execution |

### Step 5: Access provisioning

| Action | Responsible | Timeframe |
|---|---|---|
| 5.1 Access provisioning gate check: confirm Steps 1 to 4 are complete before access is granted | Supplier Risk Manager | Before any access |
| 5.2 Provision access following least-privilege principle: request only required access | IT Operations | Within 5 business days of gate check |
| 5.3 Create user accounts with organisation-assigned credentials (not shared) | IT Operations | During Step 5 |
| 5.4 Enable MFA for all remote access | IT Operations | During provisioning |
| 5.5 Record access grants in the access control system | IT Operations | At provisioning |
| 5.6 Set access review reminder (Tier 1: quarterly; Tier 2: semi-annual; Tier 3: annual) | IT Operations / Supplier Risk Manager | At provisioning |

### Step 6: Register update and handover

| Action | Responsible | Timeframe |
|---|---|---|
| 6.1 Update [`supply-chain/register-supplier-risk-template.md`](register-supplier-risk-template.md) with full onboarding record | Supplier Risk Manager | Within 2 business days of access provisioning |
| 6.2 If supplier is a personal data processor: add to [`supply-chain/register-subprocessor-template.md`](register-subprocessor-template.md) | DPO / Supplier Risk Manager | Within 2 business days |
| 6.3 Notify contract owner and business unit of approved onboarding and monitoring schedule | Supplier Risk Manager | At completion |
| 6.4 Schedule first monitoring review per tier cadence | Supplier Risk Manager | At completion |

---

## Decision gates

| Gate | Condition | Outcome |
|---|---|---|
| **Gate 1: Pre-Assessment** | Is onboarding request complete and supplier classification confirmed? | Proceed to Step 2 if yes; return to requester if no |
| **Gate 2: Security Review** | Does the supplier meet minimum assurance requirements for their tier? | Proceed if yes; document gaps; escalate if High/Critical gaps |
| **Gate 3: Privacy Review** | Is the DPA executed (where required)? Is the transfer mechanism valid? | Proceed if yes; do not proceed if DPA absent and personal data involved |
| **Gate 4: Contractual** | Are all required contract clauses in place? | Proceed if yes; resolve with legal if gaps exist |
| **Gate 5: Access** | Have all gates 1 to 4 been passed? | Access may be provisioned only after all gates passed |

---

## Escalation matrix

| Scenario | Escalation Path | Timeframe |
|---|---|---|
| Tier 1 supplier with Critical residual risk | Supplier Risk Manager → CRO → executive leadership | Within 24 hours |
| DPIA identifies High risk to individuals | DPO → CISO → Chief Privacy Officer | Within 24 hours |
| Supplier fails to provide assurance evidence | Supplier Risk Manager → Requesting Business Unit; delay access | After deadline passes |
| Breach of trade compliance programme membership | Trade Compliance Manager → CRO; consider alternatives | Immediately on discovery |

---

**End of Document**
