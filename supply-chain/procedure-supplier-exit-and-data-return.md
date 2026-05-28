# Supplier Exit and Data Return Procedure

**Document Title:** Supplier Exit and Data Return Procedure 
**Document Type:** Procedure 
**Version:** 1.0.1 
**Date:** 2026-05-28 
**Owner:** Supplier Risk Maintainer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`supply-chain/README.md`](README.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md), [`supply-chain/standard-third-party-risk.md`](standard-third-party-risk.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md), [`supply-chain/standard-cloud-exit-and-data-portability.md`](standard-cloud-exit-and-data-portability.md), [`supply-chain/register-supplier-risk-template.md`](register-supplier-risk-template.md), [`supply-chain/register-subprocessor-template.md`](register-subprocessor-template.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md), [`governance/register-data-retention-schedule.md`](../governance/register-data-retention-schedule.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md), [`security/procedure-access-control.md`](../security/procedure-access-control.md) 
**Classification:** Public 
**Category:** Supply Chain Governance: Exit Management 
**Review Frequency:** Annual and upon significant change to supplier landscape or regulatory requirements 
**Repository Path:** [`supply-chain/procedure-supplier-exit-and-data-return.md`](procedure-supplier-exit-and-data-return.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This procedure defines the steps for managing the termination of a supplier relationship, ensuring that access is revoked, data is returned or securely deleted, contractual obligations are confirmed as fulfilled, and the transition to an alternative supplier or in-house capability is conducted without operational disruption or residual data risk.

---

## Exit triggers

| Trigger Type | Examples |
|---|---|
| **Planned exit** | Contract expiry; strategic decision to change supplier; in-sourcing decision |
| **Performance-driven exit** | Repeated SLA failures; uncorrected security gaps; persistent contractual breaches |
| **Risk-driven exit** | Critical unresolvable security or privacy gap; supplier insolvency or acquisition; loss of trade compliance certification |
| **Regulatory exit** | Supplier placed on sanctions list; regulatory direction to cease relationship |
| **Mutual termination** | Supplier withdraws from market; exits a product line or service area |

---

## Roles and responsibilities

| Role | Responsibility |
|---|---|
| **Contract Owner** | Decision authority for initiating and approving the exit |
| **Supplier Risk Manager** | Leads and coordinates the exit process |
| **IT Operations** | Revokes system access; confirms access removal |
| **Data Protection Officer** | Oversees data return and deletion; confirms personal data obligations met |
| **Legal / Procurement** | Manages contractual notice and termination; confirms obligations fulfilled |
| **Trade Compliance Manager** | Assesses impact of exit on trade compliance programme obligations |
| **Resilience Manager** | Coordinates transition planning to avoid continuity gaps |

---

## Exit planning

### Step 1: Exit decision and notification

| Action | Responsible | Timeframe |
|---|---|---|
| 1.1 Document the exit decision and reason | Contract Owner | Before initiating notice |
| 1.2 Review contract for termination notice period and obligations | Legal | Immediately |
| 1.3 Assess whether the exit triggers any trade compliance programme reporting obligations (e.g., change of approved service providers under CTPAT, AEO-S) | Trade Compliance Manager | Within 3 business days |
| 1.4 Issue formal written notice of termination to the supplier as per contract terms | Legal | Per contract notice period |
| 1.5 Notify internal stakeholders: IT, Finance, Operations, DPO, HR where relevant | Contract Owner / Supplier Risk Manager | Within 3 business days of decision |
| 1.6 Initiate contingency planning: identify alternate supplier or transition path | Resilience Manager / Operations | Immediately for Tier 1 |

### Step 2: Transition planning

| Action | Responsible | Timeframe |
|---|---|---|
| 2.1 Identify all services, integrations, and data assets in scope of the relationship | IT Operations / Supplier Risk Manager | Within 5 business days |
| 2.2 Document data held by the supplier: data types, volumes, formats, storage locations | DPO / IT Operations | Within 5 business days |
| 2.3 Confirm data portability requirements: format and timeline for data return | DPO / Legal | Early in exit planning |
| 2.4 Identify transition dependencies: downstream systems, processes, or trade lanes affected | Operations / IT Operations | Within 5 business days |
| 2.5 Develop transition runbook: step-by-step plan for cutover to new supplier or in-house | IT Operations / Operations | Before transition date |
| 2.6 Schedule data return or export window with the supplier | Supplier Risk Manager | Before transition date |
| 2.7 For cloud or SaaS suppliers: apply [`supply-chain/standard-cloud-exit-and-data-portability.md`](standard-cloud-exit-and-data-portability.md) requirements | IT Operations / DPO | During planning |

---

## Data return and deletion

### Step 3: Data retrieval

| Action | Responsible | Timeframe |
|---|---|---|
| 3.1 Request the supplier to export all organization data in the agreed format and by the agreed deadline | Supplier Risk Manager / DPO | Per contract data return provision |
| 3.2 Verify completeness of returned data against the data inventory compiled in Step 2 | DPO / IT Operations | Within 5 business days of receipt |
| 3.3 Validate integrity of returned data: confirm it is readable and complete | IT Operations | Within 5 business days of receipt |
| 3.4 Ingest returned data into organization-controlled storage | IT Operations | Within 5 business days of verification |
| 3.5 For personal data: confirm the returned data includes all personal data categories identified in the DPA | DPO | Within 5 business days |
| 3.6 Escalate to Legal if supplier fails to return data within the contractual deadline | Legal / DPO | Immediately on deadline breach |

### Step 4: Supplier data deletion

| Action | Responsible | Timeframe |
|---|---|---|
| 4.1 Issue formal instruction to the supplier to securely delete all copies of organization data (including personal data, test data, backup data) | DPO / Legal | Upon data return completion or at contract end |
| 4.2 Request a written deletion certificate from the supplier confirming all data has been deleted | DPO / Supplier Risk Manager | Within 30 days of deletion instruction |
| 4.3 For personal data: confirm deletion complies with DPA deletion obligations (GDPR Article 28(3)(g); UK GDPR) | DPO | Upon receipt of deletion certificate |
| 4.4 Where deletion certificate cannot be obtained: document the gap and risk; escalate to Chief Privacy Officer | DPO | If not received within 30 days |
| 4.5 Retain deletion certificate per [`governance/register-data-retention-schedule.md`](../governance/register-data-retention-schedule.md) | DPO / Legal | Permanent retention recommended |

---

## Access revocation

### Step 5: Access and credential removal

| Action | Responsible | Timeframe |
|---|---|---|
| 5.1 Identify all access accounts, API keys, tokens, certificates, and credentials held by supplier personnel | IT Operations | During exit planning |
| 5.2 Revoke all logical access on the defined exit date (or earlier for risk-driven exits) | IT Operations | On exit date; immediately for risk-driven exits |
| 5.3 Revoke all physical access badges and credentials | Facilities / IT Operations | On exit date |
| 5.4 Rotate any shared secrets, API keys, or credentials that were used by the supplier | IT Operations / Information Security | Within 24 hours of exit |
| 5.5 Confirm access removal: audit logs verification that no supplier accounts remain active | IT Operations | Within 2 business days of exit |
| 5.6 Remove supplier from any allowlists, firewall rules, or network access controls | IT Operations | Within 2 business days of exit |
| 5.7 For Tier 1 exits: conduct a full access audit 30 days after exit to confirm no residual access | IT Operations / CISO | 30 days post-exit |

---

## Contract closure

### Step 6: Contractual and compliance closure

| Action | Responsible | Timeframe |
|---|---|---|
| 6.1 Confirm all contractual obligations have been fulfilled (payments, deliverables, warranties) | Legal / Finance | Before contract closure |
| 6.2 Issue formal written confirmation of contract termination | Legal | Per contract terms |
| 6.3 Confirm any outstanding audit rights have been exercised or waived | Legal / Supplier Risk Manager | Before closure |
| 6.4 Update the supplier risk register to record exit completion: [`supply-chain/register-supplier-risk-template.md`](register-supplier-risk-template.md) | Supplier Risk Manager | Within 5 business days of exit |
| 6.5 Remove supplier from subprocessor register if applicable: [`supply-chain/register-subprocessor-template.md`](register-subprocessor-template.md) | DPO | Within 5 business days |
| 6.6 Notify affected data subjects if required by applicable law (e.g., change in data processor) | DPO / Legal | Per regulatory obligation |

---

## Post-exit review

### Step 7: Lessons learned

| Action | Responsible | Timeframe |
|---|---|---|
| 7.1 Conduct a post-exit review for all Tier 1 exits and all exits triggered by supplier failure | Supplier Risk Manager | Within 30 days of exit completion |
| 7.2 Document lessons learned: what worked well, what should be improved in the exit process | Supplier Risk Manager | During review |
| 7.3 Raise a CAPA if the exit revealed systemic weaknesses in supplier selection, monitoring, or contractual provisions: [`compliance/procedure-capa.md`](../compliance/procedure-capa.md) | Chief Compliance Officer | If applicable |
| 7.4 Update onboarding criteria or monitoring procedures to prevent recurrence: if applicable | Supplier Risk Manager | Within 60 days |

---

## Exit timeline summary

| Exit Type | Access Revocation | Data Return Deadline | Deletion Certificate Deadline |
|---|---|---|---|
| Planned exit (Tier 1) | On contract end date | Per contractual data return provision (typically within 30 days of end) | Within 60 days of end |
| Planned exit (Tier 2/3) | On contract end date | Per contractual provision | Within 90 days of end |
| Risk-driven exit (any tier) | Immediate on decision | Expedited: within 10 business days | Within 30 days |
| Regulatory-mandated exit | Immediate on notice | Per regulatory instruction | Per regulatory instruction |

---

**End of Document**
