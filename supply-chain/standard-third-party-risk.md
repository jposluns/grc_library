# Third-Party Risk Management Standard

**Document Title:** Third-Party Risk Management Standard 
**Document Type:** Standard 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Supplier Risk Maintainer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md), [`supply-chain/procedure-supplier-due-diligence.md`](procedure-supplier-due-diligence.md), [`supply-chain/procedure-supplier-audit.md`](procedure-supplier-audit.md), [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md), [`risk/procedure-risk-register.md`](../risk/procedure-risk-register.md), [`compliance/procedure-capa.md`](../compliance/procedure-capa.md) 
**Classification:** Public 
**Category:** Supply Chain Governance | Third-Party Risk 
**Review Frequency:** Annual and upon material supplier, regulatory, or framework change 
**Repository Path:** [`supply-chain/standard-third-party-risk.md`](standard-third-party-risk.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This standard defines the framework, methodology, and control requirements for identifying, assessing, and managing risks associated with vendors, partners, suppliers, and outsourced service providers.

It integrates with the Supplier and Cloud Governance Framework, the Enterprise Risk Management Standard, and the Risk Register Procedure to establish a consistent, lifecycle-based approach to third-party risk across all business units and geographies.

---

## Scope

1. Applies to all third-party relationships involving access to the organization's data, systems, networks, or facilities.
2. Includes suppliers, contractors, managed service providers, software vendors, cloud service providers, and AI model or data suppliers.
3. Covers the full supplier lifecycle from onboarding to contract termination, including subcontractors engaged by third parties.
4. Applies globally across all business units and regional operations.

---

## Governance

| Role | Responsibility |
| --- | --- |
| Chief Information Officer | Executive oversight and final approval of supplier risk posture and engagement decisions. |
| Chief Information Security Officer | Ensures that supplier security assessments, ongoing monitoring, and incident escalation are performed to standard. |
| Procurement | Manages onboarding, due diligence, and contract lifecycle in coordination with the CISO. |
| Legal Counsel | Reviews data protection, liability, and regulatory compliance clauses in all third-party contracts. |
| Supplier Relationship Owner | Monitors supplier performance and adherence to contractual obligations on an ongoing basis. |
| Enterprise Risk Committee | Reviews critical supplier risks, concentration exposure, and systemic supply-chain dependencies. |

---

## Third-party risk management lifecycle

### 1. Planning and supplier classification

All third parties must be classified into one of four tiers prior to engagement. Tier assignment determines the required depth of due diligence, monitoring frequency, and review cadence.

| Tier | Classification | Criteria |
| --- | --- | --- |
| Tier 1 | Critical | Access to sensitive or regulated data, core infrastructure, AI model supply, or mission-critical processing. |
| Tier 2 | High | Material operational impact or limited access to sensitive data; cloud or key service dependencies. |
| Tier 3 | Moderate | Minimal data or system access; indirect service dependencies with limited organizational impact. |
| Tier 4 | Low | No direct data or system access; negligible organizational impact. |

### 2. Due diligence and risk assessment

Before onboarding, each third party must undergo a structured risk assessment evaluating the following domains:

- Information security practices and certifications (ISO/IEC 27001, SOC 2).
- Data protection and privacy measures (GDPR, CPPA, PIPL).
- Financial stability and reputational standing.
- Subcontracting arrangements and offshore data-handling practices.
- Business continuity and incident response readiness.
- AI-specific controls per the ENISA AI Cybersecurity Certification Scheme 2026, where applicable.

A Third-Party Risk Assessment Questionnaire (TPRAQ) must be completed by the supplier and reviewed jointly by Procurement and the CISO. High-risk findings must trigger a documented mitigation plan, contractual adjustments, or rejection of the engagement.

### 3. Contracting and security clauses

All third-party contracts must include the following minimum provisions:

- Confidentiality and data protection clauses aligned to applicable regulatory obligations.
- Breach notification requirements within 24 hours of discovery.
- Right-to-audit and compliance reporting obligations.
- Data residency, processing, and retention limits.
- Termination provisions tied to security breaches or material noncompliance.

For AI service providers, contracts must additionally require:

- Dataset lineage documentation demonstrating data provenance.
- Model validation and explainability measures per ISO/IEC 42001 §9.
- Assurance of ethical data sourcing and absence of prohibited training data.

### 4. Continuous monitoring and performance review

Supplier risk posture and performance must be monitored on an ongoing basis using the following mechanisms:

- Security rating and threat intelligence tools.
- Periodic reassessments using the TPRAQ.
- SLA compliance tracking and incident reporting metrics.
- Vulnerability scanning results and audit attestation reviews.

Tier 1 Critical suppliers must undergo semi-annual formal assessments and independent audits where contractually and operationally feasible.

### 5. Incident management

All third parties must report security incidents or data breaches to the organization within 24 hours of discovery. Incidents involving personal data or regulated data categories must be escalated in accordance with the Data Protection and Privacy Breach Response Procedure.

Suppliers that fail to comply with breach notification requirements may be subject to contract suspension or termination.

### 6. Offboarding and contract termination

Upon contract termination or expiry, the supplier must:

1. Return or securely delete all organizational data in accordance with the contracted retention schedule.
2. Revoke all system access credentials within 24 hours of termination.
3. Provide written confirmation of data destruction or return.

Residual risks identified during offboarding must be reviewed, documented, and logged in the Risk Register for closure validation.

---

## Control alignment

| Requirement | Aligned Framework |
| --- | --- |
| Supplier risk classification and lifecycle management | ISO/IEC 27036-3:2013 |
| Third-party governance and oversight | COBIT 2019 APO10 |
| Supply chain security controls | CSA CCM v4.1 STA-02 |
| Supply chain risk management practices | NIST SP 800-161r2 |

---

## Related documents

- Supplier and Cloud Governance Framework: [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md)
- Supplier Due Diligence Procedure: [`supply-chain/procedure-supplier-due-diligence.md`](procedure-supplier-due-diligence.md)
- Supplier Audit Procedure: [`supply-chain/procedure-supplier-audit.md`](procedure-supplier-audit.md)
- Enterprise Risk Management Standard: [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md)
- Risk Register Procedure: [`risk/procedure-risk-register.md`](../risk/procedure-risk-register.md)
- Corrective and Preventive Action Procedure: [`compliance/procedure-capa.md`](../compliance/procedure-capa.md)

---

## References

- ISO/IEC 27036-3:2013: Information security for supplier relationships: Guidelines for information and communication technology supply chain security.
- COBIT 2019 APO10: Managed Vendors.
- CSA Cloud Controls Matrix v5, STA-02: Supply Chain Management, Transparency, and Accountability.
- NIST SP 800-161r2: Cybersecurity Supply Chain Risk Management Practices for Systems and Organizations.

---

**End of Document**
