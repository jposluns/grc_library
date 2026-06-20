# SOX IT General Controls Annex

**Document Title:** SOX IT General Controls Annex\
**Document Type:** Annex\
**Version:** 0.0.3\
**Date:** 2026-06-20
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/README.md`](README.md), [`compliance/policy-compliance-and-audit-management.md`](../policy-compliance-and-audit-management.md), [`compliance/standard-internal-audit.md`](../standard-internal-audit.md), [`compliance/procedure-control-testing.md`](../procedure-control-testing.md), [`compliance/procedure-capa.md`](../procedure-capa.md), [`security/policy-identity-and-access-management.md`](../../security/policy-identity-and-access-management.md), [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md), [`operations/framework-it-service-management.md`](../../operations/framework-it-service-management.md), [`dev-security/policy-secure-development-and-engineering.md`](../../dev-security/policy-secure-development-and-engineering.md), [`resilience/procedure-backup-and-recovery.md`](../../resilience/procedure-backup-and-recovery.md)\
**Classification:** Public\
**Category:** Compliance: Sector-Specific\
**Review Frequency:** Annual and upon material PCAOB guidance, COSO framework, or regulator change\
**Repository Path:** [`compliance/financial-services/annex-sox-itgc.md`](annex-sox-itgc.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex describes how organisations subject to the Sarbanes-Oxley Act (SOX) sections 302 and 404, or equivalent financial-reporting integrity regimes elsewhere (J-SOX in Japan, C-SOX in Canada, equivalents), can use the core GRC library to demonstrate IT General Controls (ITGC) supporting Internal Control over Financial Reporting (ICFR). The annex maps the library to the four ITGC domains, identifies the auditor expectations, and lists the artefacts that adopting entities must produce alongside the library to evidence operating effectiveness.

This annex does not reproduce PCAOB Auditing Standard 2201, COSO Internal Control Integrated Framework, or auditor-specific testing procedures. Adopting entities consume those from the official source and their external auditor.

---

## Applicability triggers

This annex applies where the organisation is:

1. A US-listed company subject to SOX 302 and 404.
2. A foreign private issuer with US listings subject to SOX 404(a).
3. A Canadian reporting issuer subject to NI 52-109 (C-SOX).
4. A Japanese listed company subject to J-SOX.
5. A subsidiary in scope of a listed parent's ICFR.
6. A service provider whose services support a listed entity's ICFR, and the listed entity has requested a SOC 1 Type II report.

---

## ICFR scope determination

The audit committee and management identify the significant in-scope systems based on materiality to financial-reporting accounts. Library support: [`compliance/procedure-audit-planning.md`](../procedure-audit-planning.md), [`operations/register-asset-inventory.md`](../../operations/register-asset-inventory.md). Adopting entities maintain a SOX-scope register identifying:

1. Significant accounts and the relevant assertions.
2. In-scope business processes and the IT-dependent steps.
3. In-scope IT systems (ERP, financial reporting systems, consolidation platforms, treasury, billing, payroll, sub-ledgers, data warehouses, integrations, key reports).
4. In-scope cloud services and third parties (with SOC 1 reliance plan).
5. In-scope key reports (system-generated reports relied on for ICFR assertions).

---

## The four ITGC domains

ITGC are organized in four domains. Each domain has a stable set of control objectives independent of the technology platform.

### Domain 1: access to programs and data

| Control objective | Library artefact |
| --- | --- |
| Access provisioning is authorised | [`security/procedure-identity-management.md`](../../security/procedure-identity-management.md), [`security/procedure-access-control.md`](../../security/procedure-access-control.md) |
| Access deprovisioning is timely on termination or transfer | [`security/procedure-onboarding-and-offboarding.md`](../../security/procedure-onboarding-and-offboarding.md) |
| Privileged access is restricted, monitored, and recertified | [`security/standard-privileged-access-management.md`](../../security/standard-privileged-access-management.md) |
| Segregation of duties between conflicting roles | [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md); entity-specific SoD ruleset |
| Periodic access reviews | [`security/procedure-access-control.md`](../../security/procedure-access-control.md) extended with quarterly access certification |
| Authentication strength | [`security/standard-authentication-and-password-management.md`](../../security/standard-authentication-and-password-management.md) |
| Direct database and operating-system access restricted | [`operations/standard-production-security-requirements.md`](../../operations/standard-production-security-requirements.md) |
| Generic, shared, and service accounts controlled | [`security/standard-privileged-access-management.md`](../../security/standard-privileged-access-management.md) |

Typical auditor evidence: ticketed access requests with approvals, ticketed deprovisioning within SLA on termination, quarterly access reviews with reviewer sign-off and remediation, privileged-account log review, SoD analysis output with remediation.

### Domain 2: program changes

| Control objective | Library artefact |
| --- | --- |
| Changes are authorised before development | [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md), [`dev-security/policy-secure-development-and-engineering.md`](../../dev-security/policy-secure-development-and-engineering.md) |
| Changes are tested before production deployment | [`dev-security/standard-quality-assurance-and-testing.md`](../../dev-security/standard-quality-assurance-and-testing.md) |
| Changes are approved by an authorised role before production deployment | [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md) |
| Developers cannot deploy to production unsupervised | [`dev-security/standard-devops-security-requirements.md`](../../dev-security/standard-devops-security-requirements.md) |
| Emergency change procedure exists with post-implementation approval | [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md) |
| Source-control history is the system of record for code changes | [`dev-security/standard-developer-security-requirements.md`](../../dev-security/standard-developer-security-requirements.md), [`dev-security/standard-devops-security-requirements.md`](../../dev-security/standard-devops-security-requirements.md) |
| Configuration changes (not just code) are subject to the same control | [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md) |
| Vendor-applied changes (e.g. SaaS releases) are tracked | [`supply-chain/procedure-supplier-ongoing-monitoring.md`](../../supply-chain/procedure-supplier-ongoing-monitoring.md) |

Typical auditor evidence: change tickets with approval, test evidence, production deployment audit log, segregation between developer and production deployer, post-implementation review of emergency changes, sample-based testing across the period.

### Domain 3: program development

| Control objective | Library artefact |
| --- | --- |
| New systems and significant enhancements follow a documented development methodology | [`dev-security/policy-secure-development-and-engineering.md`](../../dev-security/policy-secure-development-and-engineering.md), [`dev-security/standard-developer-security-requirements.md`](../../dev-security/standard-developer-security-requirements.md) |
| User acceptance testing and sign-off before production cutover | [`dev-security/standard-quality-assurance-and-testing.md`](../../dev-security/standard-quality-assurance-and-testing.md) |
| Data conversion is controlled and reconciled | Outside library scope; per-project conversion plan |
| Acceptance into service before go-live | [`security/policy-acceptance-into-service.md`](../../security/policy-acceptance-into-service.md) |
| Post-implementation review | [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](../../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md) |

Typical auditor evidence: project documentation, UAT sign-offs, conversion reconciliation, go-live approval.

### Domain 4: computer operations

| Control objective | Library artefact |
| --- | --- |
| Production jobs and batch schedules are monitored | [`operations/procedure-security-monitoring-and-alert-management.md`](../../operations/procedure-security-monitoring-and-alert-management.md) |
| Job failures are detected and resolved per SLA | [`operations/framework-it-service-management.md`](../../operations/framework-it-service-management.md) |
| Backups are run on schedule and verified | [`resilience/procedure-backup-and-recovery.md`](../../resilience/procedure-backup-and-recovery.md) |
| Restoration capability is tested | [`resilience/procedure-continuity-and-recovery-testing.md`](../../resilience/procedure-continuity-and-recovery-testing.md) |
| Disaster recovery for in-scope systems is documented and tested | [`resilience/plan-it-disaster-recovery.md`](../../resilience/plan-it-disaster-recovery.md) |
| Operational events are logged and reviewed | [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md) |
| Capacity is managed to maintain availability | [`operations/standard-service-level-management.md`](../../operations/standard-service-level-management.md) |

Typical auditor evidence: job-monitoring log review, ticketed failure resolution, backup-success log, restoration test evidence, DR test evidence, log review evidence.

---

## Auditor-expected artefacts beyond the library

1. **Control matrix** mapping ICFR financial-reporting risks to manual and IT-dependent controls, with control owner, frequency, and key-control designation.
2. **Walkthroughs** documenting how each control operates end to end.
3. **Test of design** for each key control.
4. **Test of operating effectiveness** sampled across the period.
5. **SOC 1 reports** for material third-party service providers, with a complementary user entity controls (CUEC) analysis.
6. **Management deficiency assessment** classifying findings as deficiency, significant deficiency, or material weakness.
7. **Management remediation plan** for each finding, tracked to closure.
8. **Quarterly sub-certifications** under SOX 302 supporting the CEO and CFO certifications.
9. **Annual management assessment of ICFR effectiveness** under SOX 404(a).
10. **External auditor's attestation** of ICFR under SOX 404(b) for accelerated and large accelerated filers.

---

## Library gaps requiring additional documentation

1. **SOX scoping memo** identifying in-scope systems and significant accounts.
2. **Control matrix and walkthrough documentation.**
3. **SoD ruleset and exception process** specific to the ERP and financial systems.
4. **Key-report inventory** with completeness-and-accuracy testing.
5. **Third-party SOC 1 reliance memo** with CUEC mapping per service provider.
6. **Quarterly access certification** template specific to ICFR-relevant systems.
7. **Sub-certification process** for sub-process owners.

---

## Coordination with adjacent regimes

| Regime | Coordination point |
| --- | --- |
| ISAE 3402 / SOC 2 | A SOX-in-scope service provider often produces both; the SOC 1 covers ICFR-relevant controls and the SOC 2 covers security, availability, processing integrity, confidentiality, privacy |
| PCI DSS | Cardholder data environment scoping may overlap with SOX in-scope systems |
| GDPR / UK GDPR | Personal data lifecycle controls may overlap with access and change controls |
| NIST CSF 2.0 | Control catalogue used for security assertions can underlie SOX evidence |
| ISO/IEC 27001:2022 | ISMS controls map to SOX ITGC where the systems are in scope |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| Sarbanes-Oxley Act | Sections 302, 404, 906 | Primary regime (US) |
| PCAOB Auditing Standard 2201 | An Audit of Internal Control over Financial Reporting Integrated with an Audit of Financial Statements | Auditor methodology |
| COSO Internal Control Integrated Framework | 2013 update | Control framework |
| COSO ERM Framework | 2017 update | Risk integration |
| ITGC family | Industry practice | Control taxonomy |
| C-SOX | NI 52-109 (Canada) | Equivalent regime |
| J-SOX | Financial Instruments and Exchange Act (Japan) | Equivalent regime |
| SOC 1 reporting | ISAE 3402; SSAE 18 (AT-C 320) | Third-party reliance |
| ITIL 4 and ISO/IEC 20000 | Industry | Computer operations practice |

---

## Limitations

This annex is a CC BY-SA 4.0 navigation aid. SOX compliance is determined by management assertion and external auditor attestation under PCAOB standards; the library provides architectural baselines but does not produce auditor-ready evidence. Adopting entities work with their external auditor to confirm scope, control selection, evidence format, and test sampling. This annex is not auditor guidance and does not establish SOX compliance.

---

**End of Document**
