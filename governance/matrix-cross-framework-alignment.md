# Cross-Framework Alignment Matrix

**Document Title:** Cross-Framework Alignment Matrix\
**Document Type:** Matrix\
**Version:** 1.1.13\
**Date:** 2026-07-23\
**Owner:** Control Framework Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/charter-governance-library.md`](charter-governance-library.md), [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md), [`governance/matrix-reverse-framework-control-crosswalk.md`](matrix-reverse-framework-control-crosswalk.md), [`NOTICE.md`](../NOTICE.md), [`governance/framework-human-capital-and-ethical-conduct.md`](framework-human-capital-and-ethical-conduct.md), [`governance/framework-sustainability-and-responsible-technology.md`](framework-sustainability-and-responsible-technology.md), [`governance/guideline-esg-and-ai-ethics-disclosure.md`](guideline-esg-and-ai-ethics-disclosure.md), [`risk/guideline-quantitative-risk-analysis.md`](../risk/guideline-quantitative-risk-analysis.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** 6 to 12 months and upon material source-framework change\
**Repository Path:** [`governance/matrix-cross-framework-alignment.md`](matrix-cross-framework-alignment.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This matrix provides an original, non-verbatim alignment structure for mapping repository documents to recognized framework families. It is not an official mapping, certification claim, legal opinion, or reproduction of third-party framework content.

---

## Mapping principles

1. Use framework families and control domains only where source licence terms restrict reproduction.
2. Do not copy third-party control text, questionnaire text, guidance text, or metrics text.
3. Distinguish legal obligation from industry practice and architectural recommendation.
4. Map repository artefacts to evidence classes that adopting organizations can implement internally.
5. State limitations where framework coverage requires organization-specific validation.

---

## Alignment matrix

| Repository Domain | Repository Artefact | External Reference Family | Alignment Type | Applicability Condition | Evidence Class |
| --- | --- | --- | --- | --- | --- |
| Governance | Governance Library Charter | ISO governance, risk, compliance, quality, information security, privacy, and AI management families | Industry practice | Organization maintains a formal governance corpus. | Approved charter, review record, role authority register. |
| Governance | Document Architecture and Interrelationship Framework | COBIT governance concepts, ISO management system documentation practices | Architectural recommendation | Organization requires traceability from governance intent to evidence. | Document dependency map, index register, approval workflow. |
| Governance | Cross-Framework Alignment Matrix | ISO, NIST, COBIT, CCM, AICM, OWASP, MITRE ATLAS, MITRE ATT&CK | Evidence category | Organization maps controls to multiple frameworks. | Mapping register, review log, source version register. |
| Governance | Global Regulatory Applicability Register | Privacy, cybersecurity, AI, resilience, trade, and sector regulatory families | Regulatory interpretation | Organization operates across jurisdictions or regulated sectors. | Obligation register, applicability assessment, legal review note. |
| Governance | Digital Trust and Assurance Metrics Register | Governance, assurance, cloud control, and continuous monitoring metrics families | Industry practice | Organization measures control performance. | KPI register, test results, audit findings, remediation log. |
| Risk | Enterprise Risk Management Standard | ISO 31000 risk management, NIST RMF, COBIT APO12, FAIR quantitative risk analysis | Architectural recommendation | Organization requires a documented risk methodology and register. | Risk register, treatment plan, acceptance record, KRI report. |
| Compliance | Compliance and Audit Management Policy | ISO 37301 compliance management, ISO 19011 auditing, COBIT MEA01, NIST SP 800-53 CA family | Industry practice or regulatory interpretation | Organization operates under regulatory, contractual, or certification obligations. | Obligations register, audit plan, CAPA record, compliance evidence. |
| AI | AI Governance and Risk Framework | ISO/IEC 23894 AI risk, NIST AI RMF, OECD AI Principles, EU AI Act, AI management families | Industry practice | AI systems materially affect business, security, legal, operational, or human outcomes. | AI system inventory, risk tiering, lifecycle evidence, model documentation. |
| AI | AI Security and Risk Standard | OWASP LLM Top 10, MITRE ATLAS, AI control, cloud control, secure engineering, and adversarial AI references | Architectural recommendation | AI systems process sensitive data, invoke tools, use retrieval, or expose inference interfaces. | Threat model, data flow, prompt injection test, access review, monitoring record. |
| AI | AI and Agentic Development Security Standard | OWASP LLM Top 10 (excessive agency), MITRE ATLAS, CSA AICM (agentic and autonomy domains), NIST AI RMF, ISO/IEC 42001 operational families | Architectural recommendation | AI systems use agentic tools, autonomous or semi-autonomous actions, MCP servers, code execution, or production action capability. | Agent threat model, tool allow-list, reversibility classification, recovery-test result, production-authority evidence record, immutable audit trail. |
| AI | AI System Impact Assessment Procedure | Privacy, security, human oversight, AI governance, and supplier risk families | Evidence category | AI system is proposed, changed, retired, or materially repurposed. | Impact assessment, risk decision, mitigation plan, approval record. |
| Privacy | Privacy and Data Governance Policy | GDPR, PIPEDA, Quebec Law 25, PIPL, LGPD, privacy management and data protection families | Legal obligation or regulatory interpretation | Personal data or regulated data is processed. | Data inventory, impact assessment, transfer assessment, retention schedule. |
| Supply Chain | Supplier and Cloud Governance Framework | Supplier risk, cloud assurance, NIST SP 800-161 SCRM, security, privacy, and resilience families | Industry practice or contractual requirement | External providers process data, host workloads, operate critical services, or provide AI capabilities. | Due diligence record, contractual control schedule, supplier risk register, exit plan. |
| Supply Chain | Trade and Supply-Chain Continuity Controls | WCO SAFE, ISO 28000, CTPAT, BASC, PIP, AEO, AEO-S, NEEC, OEA | Regulatory interpretation or contractual requirement | Organization participates in customs, logistics, or trade-security programmes. | Programme audit record, gap assessment, corrective action evidence. |
| Resilience | Business Continuity and Resilience Framework | ISO 22301 continuity, NIST SP 800-34 continuity planning, COBIT DSS04, operational resilience families | Industry practice or regulatory interpretation | Services have recovery, availability, regulatory, or customer-impact obligations. | BIA, RTO/RPO register, test report, recovery plan, corrective action log. |
| Dev Security | Developer Security Requirements Standard | OWASP Top 10, OWASP ASVS, OWASP LLM Top 10, NIST SSDF (SP 800-218), NIST SP 800-53 SA/SI families, ISO/IEC 27001 Annex A.8.25 to A.8.34, SLSA | Architectural recommendation | Organization develops or maintains software, AI systems, or automated pipelines. | Secure code review, SAST/DAST results, dependency scan, pipeline gate evidence. |

---

## Risk management control area mappings

The following table maps the enterprise risk management control areas to external framework families. It supports the Enterprise Governance and Risk Management Policy, the Enterprise Risk Management Standard, and the underlying risk procedures.

| Control Area | ISO 31000 | ISO/IEC 23894 | NIST SP 800-39 | NIST AI RMF | COBIT 2019 | CSA CCM v4.1 | Legal and Regulatory | Trade and Supply-Chain Programmes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Risk framework and governance | Clause 5 Framework | Clause 5 Governance | Organization-wide RMF | Govern | EDM03 Ensured Risk Optimization | GRC domain | Corporate governance charters | WCO SAFE, ISO 28000, BASC, PIP, CTPAT, AEO, AEO-S |
| Risk identification and analysis | Clause 6.4.2 Risk identification; Clause 6.4.3 Risk analysis (ISO 31000:2018) | Clause 6.2 Identification; Clause 6.3 Analysis | Tasks 1 and 2 | Map; Measure | APO12.02 Analyze risk | GRC domain | GDPR Article 25; PIPEDA accountability | WCO SAFE equivalence |
| Risk appetite and tolerance | Clause 6.3.4 Defining risk criteria (ISO 31000:2018) | Clause 5 Governance | Organizational risk strategy | Govern | EDM03.01 Evaluate risk management | GRC domain | Board-approved appetite statements | WCO SAFE equivalence |
| Treatment and control selection | Clause 6.5 Risk treatment (ISO 31000:2018) | Clause 6.4 Treatment | Task 3 Respond | Manage | APO12.06 Respond to risk | GRC domain | ISO/IEC 27001 Annex A controls | WCO SAFE equivalence |
| Monitoring and review | Clause 6.6 Monitoring and review (ISO 31000:2018) | Clause 6.5 Monitoring | Task 4 Monitor | Manage | MEA01; MEA02 | GRC domain | Regulatory reporting duties | WCO SAFE equivalence |
| AI model governance | Clause 6 Process applied iteratively across the AI lifecycle (ISO 31000:2018) | Clauses 5 and 6 lifecycle | Organizational context | Govern; Manage | APO12; BAI03; DSS06 | AIS domain | EU AI Act; Treasury Board Directive on Automated Decision-Making (Canada; AIDA lapsed) | Not applicable |
| Third-party and supply-chain risk | Clause 6.3 Scope, context, criteria (third-party scope inclusion) and Clause 5.3 Integration (ISO 31000:2018) | Clause 6.2 Context and third-party data | Organizational context | Govern | APO10 Managed Vendors | STA domain | Contractual clauses; data processing agreements; transfer impact assessments | WCO SAFE equivalence |
| Business continuity and resilience | Clause 5.2 Leadership | Not applicable | Organizational resilience context | Manage | DSS04 Managed Continuity | BCR domain | Local continuity regulations | WCO SAFE equivalence |
| Exception and acceptance | Clause 6.5 Risk treatment, acceptance option (ISO 31000:2018) | Clause 6.4 Acceptance criteria | Risk response acceptance | Govern | APO12.06 Respond to risk | GRC domain | Documented approvals and durations | WCO SAFE equivalence |

---

## Minimum mapping fields for adopting organizations

Adopting organizations should extend this matrix with:

- Source framework version.
- Source domain or public identifier.
- Internal control ID.
- Internal control owner.
- Evidence repository location.
- Test frequency.
- Test result.
- Residual risk.
- Exception reference.
- Approval record.

---

## Limitations

This matrix does not reproduce external framework content and does not establish compliance. Adopting organizations must validate source terms, applicability, control implementation, evidence quality, and operating effectiveness.

---

**End of Document**
