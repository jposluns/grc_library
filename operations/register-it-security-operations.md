# IT Security Operations Register

**Document Title:** IT Security Operations Register 
**Document Type:** Register 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Chief Information Officer 
**Related Documents:** [`operations/register-asset-inventory.md`](register-asset-inventory.md), [`security/framework-cryptographic-key-lifecycle.md`](../security/framework-cryptographic-key-lifecycle.md), [`security/procedure-access-control.md`](../security/procedure-access-control.md), [`operations/procedure-patch-management.md`](procedure-patch-management.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md) 
**Classification:** Public 
**Category:** Operations 
**Review Frequency:** Continuous; CISO review monthly; full review annually 
**Repository Path:** [`operations/register-it-security-operations.md`](register-it-security-operations.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This register defines the schema, governance model, and section structure for the IT Security Operations Register. The register is the single authoritative source for current operational security state across all IT platforms and environments. It does not contain security requirements: those are defined in security policies and standards. This register records the current implementation state and tracks remediation of identified gaps.

The operational register is maintained in the GRC platform and updated continuously. This document defines its structure and governance.

---

## Register governance

| Principle | Requirement |
| --- | --- |
| **Update obligation** | Any team member who changes the state of any item in this register must update the relevant section within 5 business days |
| **CISO review** | Monthly: CISO reviews register for staleness and escalates unaddressed items |
| **Vendor assignments** | Reviewed annually in Q4 |
| **Distribution** | IT Operations, DevOps, Infrastructure, and Security teams |

---

## Register sections

### Section 1: vendor and partner assignments

Records current vendor and partner relationships for security and operational functions including:
- Security monitoring and SOC services.
- Endpoint security management.
- Infrastructure delivery services.
- Identity and access management tooling.
- Incident response partners.

For each vendor, the register records: function, contract reference, renewal schedule, and scope notes. Vendor assignments are reviewed and confirmed annually.

### Section 2: application platform inventory

Records the security baseline status for each application platform in scope. For each platform:
- Platform name and description.
- Security baseline status (Not Started / In Progress / Complete).
- Identified gaps (referenced by gap ID).
- Last updated date.

Platforms are linked to the Asset Inventory Register for lifecycle and asset management details.

### Section 3: unapproved platforms

Records platforms identified as in use but not formally approved through the Acceptance Into Service process. For each unapproved platform:
- Platform name.
- Reason not approved (security, compliance, data residency, etc.).
- Required action.
- Responsible owner.
- Target resolution date.

Unapproved platforms present in the production environment are treated as risks and tracked until resolved.

### Section 4: cloud subscription and environment architecture

Records the organizational cloud environment structure including:
- Subscription / account names and purposes.
- Environment classification (Production / Non-Production / Sandbox).
- Cross-environment connectivity rules.
- RBAC review schedule.

Cross-environment connectivity from production to non-production is prohibited unless documented with risk acceptance.

### Section 5: end-of-life (EOL) violations

Records all systems and runtimes that have passed their vendor-supported end-of-life date. For each violation:
- Runtime or system name.
- EOL date.
- Affected systems.
- Risk classification (Class 1 = immediate / Class 2 = high / Class 3 = medium).
- Owner.
- Remediation target date and status.

Class 1 EOL violations require remediation within 30 days. Class 2 within 90 days. All EOL items are escalated to the CIO monthly.

### Section 6: active security findings

Records active operational security findings not yet resolved. For each finding:
- Finding ID.
- Description.
- Severity.
- Affected system or component.
- Owner.
- Target resolution date.
- Status.

Critical findings are escalated to the CISO and CIO immediately. All findings are reviewed in the monthly CISO register review.

### Section 7: identity and access operational state

Records current state of identity management including:
- Status of privileged identity management deployment.
- OAuth and service connection health.
- Service account inventory status.
- Access review completion status.

### Section 8: infrastructure programme gate mapping

Records security acceptance criteria for each phase of the current infrastructure programme and tracks current status. Links programme milestones to security baseline requirements.

### Section 9: active operational constraints

Records any active "do not modify" or restricted-change constraints on production systems, including:
- System or component name.
- Constraint description.
- Reason for constraint.
- Approval required before modification.
- Owner.

---

## Relationship to other documents

| Register / Document | Relationship |
| --- | --- |
| Asset Inventory Register | Source of truth for asset metadata; this register records security state of those assets |
| Security policies and standards | Define the requirements; this register records implementation state |
| CAPA Register | Active nonconformities are tracked in CAPA; this register flags findings that become CAPAs |
| Continuous Improvement Register | Proactive improvements to the operational state are tracked in CIR |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27001:2022 | §9.1: Monitoring, Measurement, Analysis and Evaluation | Operational security monitoring |
| NIST SP 800-53 | CA-7: Continuous Monitoring | Continuous operational assurance |
| COBIT 2025 | DSS05: Manage Security Services | Security operations governance |
| CSA CCM v5 | SEF: Security Engineering and Development | Cloud security operations |

---

**End of Document**
