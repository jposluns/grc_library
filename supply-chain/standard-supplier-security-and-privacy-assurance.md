# Supplier Security and Privacy Assurance Standard

**Document Title:** Supplier Security and Privacy Assurance Standard  
**Document Type:** Standard  
**Version:** 1.0.0  
**Date:** 2026-05-27  
**Owner:** Supplier Risk Maintainer  
**Approving Authority:** Governance Library Maintainer  
**Related Documents:** [`supply-chain/README.md`](README.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md), [`supply-chain/standard-third-party-risk.md`](standard-third-party-risk.md), [`supply-chain/procedure-supplier-due-diligence.md`](procedure-supplier-due-diligence.md), [`supply-chain/procedure-supplier-audit.md`](procedure-supplier-audit.md), [`supply-chain/procedure-supplier-onboarding-security-review.md`](procedure-supplier-onboarding-security-review.md), [`supply-chain/procedure-supplier-ongoing-monitoring.md`](procedure-supplier-ongoing-monitoring.md), [`supply-chain/template-supplier-security-questionnaire.md`](template-supplier-security-questionnaire.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`compliance/policy-compliance-and-audit-management.md`](../compliance/policy-compliance-and-audit-management.md), [`security/policy-information-security.md`](../security/policy-information-security.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md)  
**Classification:** Public  
**Category:** Supply Chain Governance — Security and Privacy  
**Review Frequency:** Annual and upon material regulatory change or significant supplier incident  
**Repository Path:** [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md)  
**Confidentiality:** Public  
**Licence:** CC0 1.0 Universal  

---

## Purpose

This standard defines the minimum information security and privacy assurance requirements that suppliers, processors, and other third-party service providers must meet as a condition of doing business with the organisation. It establishes the evidence and contractual obligations the organisation requires, and the assessment methods used to verify compliance.

---

## Scope

This standard applies to all third-party relationships where the supplier:
- Accesses, processes, stores, or transmits the organisation's data or systems
- Delivers services integrated into or dependent on the organisation's IT infrastructure
- Processes personal data on behalf of the organisation as a data processor or subprocessor
- Provides critical operational services whose failure would materially impact the organisation's operations or trade compliance obligations

The tier classification in [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md) determines the depth of assurance required.

---

## Minimum Security Requirements by Tier

### Tier 1 — Critical Suppliers

| Requirement | Standard | Evidence Required |
|---|---|---|
| Information security management system (ISMS) | ISO 27001:2022 or equivalent — certification or documented equivalent | Current ISO 27001 certificate; or detailed control inventory with independent attestation |
| Access control — least privilege, MFA for remote access | Documented access control policy and procedures | Policy documentation; MFA configuration attestation |
| Vulnerability management — critical patches within 30 days, high within 90 days | Documented patch management procedure | Patch management records; vulnerability scan summary |
| Incident response capability — 24-hour detection target; documented escalation | Documented IRP with notification timelines | IRP document; evidence of testing |
| Security incident notification to the organisation | Within 24 hours of confirmed incident affecting organisation data or services | Contractual notification obligation; test notification record |
| Penetration testing | Annual external penetration test by qualified provider | Pen test report or letter of attestation (last 12 months) |
| Security operations monitoring | 24/7 or business-hours SIEM/SOC capability | SOC capability statement; monitoring evidence |
| Business continuity — documented BCP covering service delivery | Tested BCP with RTO/RPO aligned to contractual SLAs | BCP document; test results |
| Sub-contractor security — flow-down of requirements | Written requirements for material sub-contractors | Sub-contractor policy; attestation of flow-down |
| Data classification and handling | Documented data classification policy | Classification policy; handling procedure evidence |

### Tier 2 — High Suppliers

| Requirement | Standard | Evidence Required |
|---|---|---|
| Information security policy | Documented and board-approved | Policy document |
| Access control — least privilege | Documented procedures | Policy; access review evidence |
| Vulnerability management — critical patches within 60 days | Documented process | Self-attestation or scan summary |
| Incident response — documented procedure | Written IRP | IRP document |
| Incident notification | Within 24 hours | Contractual obligation |
| Penetration testing | Annual or most recent within 18 months | Attestation letter or abbreviated report |
| Business continuity plan | Documented | BCP document |
| Sub-contractor disclosure | Notify organisation of material sub-contractors | Notification commitment |

### Tier 3 — Moderate Suppliers (where data access exists)

| Requirement | Standard | Evidence Required |
|---|---|---|
| Information security policy | Documented | Self-attestation |
| Access controls — basic | Described | Self-declaration |
| Incident notification | Within 72 hours | Contractual obligation |
| Data breach response procedure | Documented | Self-attestation |

---

## Privacy Assurance Requirements

For any supplier that processes personal data on behalf of the organisation, the following privacy assurance requirements apply in addition to security requirements.

### All Data Processors

| Requirement | Legal Basis | Evidence |
|---|---|---|
| Data Processing Agreement (DPA) executed | GDPR Article 28; UK GDPR; PIPEDA; applicable law | Signed DPA on file |
| Processing limited to documented purposes | GDPR Article 28(3)(a); UK GDPR | DPA scope clause; processing instructions |
| Technical and organisational measures proportionate to risk | GDPR Article 32; UK GDPR | TOM schedule or statement |
| Sub-processor notification and approval process | GDPR Article 28(2); UK GDPR | Sub-processor clause in DPA; sub-processor list |
| Individual rights support — DSAR assistance | GDPR Articles 12–23; UK GDPR | Contractual commitment; process evidence |
| Data breach notification within 24 hours of awareness | GDPR Article 33(2); UK GDPR | DPA notification clause |
| Data return or secure deletion on contract end | GDPR Article 28(3)(g); UK GDPR | DPA termination clause; deletion certificate capability |
| Compliance audit support | GDPR Article 28(3)(h); UK GDPR | Audit rights clause in DPA |

### Cross-Border Transfer Suppliers

Where the supplier transfers personal data outside the EEA or UK:

| Requirement | Legal Basis | Evidence |
|---|---|---|
| Adequacy decision or valid transfer mechanism in place | GDPR Chapter V; UK GDPR Schedule 21 | SCCs, IDTA, or BCRs on file; or adequacy confirmation |
| Transfer impact assessment completed where required | Post-Schrems II / UK TRA obligations | TIA documentation |
| Data residency and transfer restrictions honoured | Contractual commitment | DPA data location clause; configuration records |

---

## Assurance Evidence Hierarchy

The organisation accepts supplier security assurance in the following priority order. Higher-tier evidence is preferred.

| Tier | Evidence Type | Applicability |
|---|---|---|
| 1 | Independent certification (ISO 27001; SOC 2 Type II; CSA STAR Level 2) | Highest confidence; accepted for Tier 1 without supplemental review |
| 2 | Third-party audit report (ISAE 3000; SOC 2 Type I; penetration test by named CREST/CHECK provider) | Accepted for Tier 1 and Tier 2; review findings for exceptions |
| 3 | Regulatory approval or certification (PCI DSS; FedRAMP; NHS DSPT) | Accepted within scope of certification |
| 4 | Completed security questionnaire with supporting evidence | Accepted for Tier 2 and Tier 3; Tier 1 requires supplemental evidence |
| 5 | Self-declaration without supporting evidence | Acceptable only for Tier 3 and Tier 4 non-data-access suppliers |

---

## Minimum Contract Clauses

Contracts with suppliers in scope of this standard must include the following minimum security and privacy clauses.

| Clause | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Information security obligations aligned to this standard | Mandatory | Mandatory | Abbreviated |
| Audit and inspection rights (direct or through third party) | Mandatory | Mandatory — audit report right | Where applicable |
| Incident notification timeline (24 hours) | Mandatory | Mandatory | 72 hours |
| Penetration test results sharing | Mandatory | Mandatory | Not required |
| Sub-contractor approval or notification | Written consent required | Written consent required | Notification |
| Data Processing Agreement | Mandatory where personal data processed | Mandatory where personal data processed | Mandatory where personal data processed |
| Data return and deletion obligations | Mandatory | Mandatory | Mandatory where data shared |
| Right to terminate for security or privacy breach | Mandatory | Mandatory | Mandatory |
| Liability for security and privacy incidents | Negotiated minimum | Negotiated minimum | Standard T&Cs |

---

## Ongoing Assurance Activities

| Activity | Tier 1 | Tier 2 | Tier 3 | Responsible |
|---|---|---|---|---|
| Annual security questionnaire refresh | Mandatory | Mandatory | Where applicable | Supplier Risk Manager |
| Certification or audit report renewal review | Mandatory | Mandatory | Not required | Supplier Risk Manager |
| Security ratings service monitoring | Continuous (where available) | Semi-annual | Not required | Supplier Risk Manager |
| Contract security clause review at renewal | Mandatory | Mandatory | Mandatory | Legal; Supplier Risk |
| Supplier security incident review | Trigger-based | Trigger-based | Trigger-based | CISO; Supplier Risk |

See [`supply-chain/procedure-supplier-ongoing-monitoring.md`](procedure-supplier-ongoing-monitoring.md) for operating procedures.

---

## Non-Compliance and Escalation

Where a supplier fails to meet the requirements of this standard:

1. **Document the gap** — record in the supplier's risk record in [`supply-chain/register-supplier-risk-template.md`](register-supplier-risk-template.md)
2. **Issue a corrective action notice** — give the supplier a defined timeframe to remediate (typically 30–90 days depending on severity)
3. **Escalate to senior management** if the supplier does not remediate within the agreed timeframe
4. **Initiate exit proceedings** if the supplier is unwilling or unable to meet minimum requirements — follow [`supply-chain/procedure-supplier-exit-and-data-return.md`](procedure-supplier-exit-and-data-return.md)
5. **Notify the Data Protection Officer** if the gap involves a personal data processing risk

---

## Framework Alignment

| Framework | Alignment |
|---|---|
| ISO 27001:2022 | A.5.19–A.5.22 Supplier relationships |
| ISO 27036 | Information security for supplier relationships |
| NIST SP 800-53 Rev 5 | SA-9 External System Services; SA-12 Supply Chain Protection |
| GDPR / UK GDPR | Article 28 — Processor obligations |
| NIST Privacy Framework | CT-P.2 — Data processing ecosystem management |
| CSA CCM v4 | STA — Supply Chain Management, Transparency, and Accountability |

---

**End of Document**
