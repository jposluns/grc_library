# Cross-Framework Alignment Matrix

**Document Title:** Cross-Framework Alignment Matrix 
**Document Type:** Matrix 
**Version:** 1.1.1 
**Date:** 2026-05-28 
**Owner:** Control Framework Maintainer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`governance/charter-governance-library.md`](charter-governance-library.md), [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md), [`governance/matrix-reverse-framework-control-crosswalk.md`](matrix-reverse-framework-control-crosswalk.md), [`NOTICE.md`](../NOTICE.md), [`governance/framework-human-capital-and-ethical-conduct.md`](framework-human-capital-and-ethical-conduct.md), [`governance/framework-sustainability-and-responsible-technology.md`](framework-sustainability-and-responsible-technology.md), [`governance/guideline-esg-and-ai-ethics-disclosure.md`](guideline-esg-and-ai-ethics-disclosure.md), [`risk/guideline-quantitative-risk-analysis.md`](../risk/guideline-quantitative-risk-analysis.md) 
**Classification:** Public 
**Category:** Core Governance 
**Review Frequency:** 6 to 12 months and upon material source-framework change 
**Repository Path:** [`governance/matrix-cross-framework-alignment.md`](matrix-cross-framework-alignment.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This matrix provides an original, non-verbatim alignment structure for mapping repository documents to recognized framework families. It is not an official mapping, certification claim, legal opinion, or reproduction of third-party framework content.

---

## Mapping principles

1. Use framework families and control domains only where source license terms restrict reproduction.
2. Do not copy third-party control text, questionnaire text, guidance text, or metrics text.
3. Distinguish legal obligation from industry practice and architectural recommendation.
4. Map repository artefacts to evidence classes that adopting organisations can implement internally.
5. State limitations where framework coverage requires organisation-specific validation.

---

## Alignment matrix

| Repository Domain | Repository Artefact | External Reference Family | Alignment Type | Applicability Condition | Evidence Class |
| --- | --- | --- | --- | --- | --- |
| Governance | Governance Library Charter | ISO governance, risk, compliance, quality, information security, privacy, and AI management families | Industry practice | Organisation maintains a formal governance corpus. | Approved charter, review record, role authority register. |
| Governance | Document Architecture and Interrelationship Framework | COBIT governance concepts, ISO management system documentation practices | Architectural recommendation | Organisation requires traceability from governance intent to evidence. | Document dependency map, index register, approval workflow. |
| Governance | Cross-Framework Alignment Matrix | ISO, NIST, COBIT, CCM, AICM, OWASP, MITRE ATLAS, MITRE ATT&CK | Evidence category | Organisation maps controls to multiple frameworks. | Mapping register, review log, source version register. |
| Governance | Global Regulatory Applicability Register | Privacy, cybersecurity, AI, resilience, trade, and sector regulatory families | Regulatory interpretation | Organisation operates across jurisdictions or regulated sectors. | Obligation register, applicability assessment, legal review note. |
| Governance | Digital Trust and Assurance Metrics Register | Governance, assurance, cloud control, and continuous monitoring metrics families | Industry practice | Organisation measures control performance. | KPI register, test results, audit findings, remediation log. |
| Risk | Enterprise Risk Management Standard | ISO 31000 risk management, NIST RMF, COBIT APO12, FAIR quantitative risk analysis | Architectural recommendation | Organisation requires a documented risk methodology and register. | Risk register, treatment plan, acceptance record, KRI report. |
| Compliance | Compliance and Audit Management Policy | ISO 37301 compliance management, ISO 19011 auditing, COBIT MEA01, NIST SP 800-53 CA family | Industry practice or regulatory interpretation | Organisation operates under regulatory, contractual, or certification obligations. | Obligations register, audit plan, CAPA record, compliance evidence. |
| AI | AI Governance and Risk Framework | ISO 23894 AI risk, NIST AI RMF, OECD AI Principles, EU AI Act, AI management families | Industry practice | AI systems materially affect business, security, legal, operational, or human outcomes. | AI system inventory, risk tiering, lifecycle evidence, model documentation. |
| AI | AI Security and Risk Standard | OWASP LLM Top 10, MITRE ATLAS, AI control, cloud control, secure engineering, and adversarial AI references | Architectural recommendation | AI systems process sensitive data, invoke tools, use retrieval, or expose inference interfaces. | Threat model, data flow, prompt injection test, access review, monitoring record. |
| AI | AI System Impact Assessment Procedure | Privacy, security, human oversight, AI governance, and supplier risk families | Evidence category | AI system is proposed, changed, retired, or materially repurposed. | Impact assessment, risk decision, mitigation plan, approval record. |
| Privacy | Privacy and Data Governance Policy | GDPR, CPPA, PIPEDA, Quebec Law 25, PIPL, LGPD, privacy management and data protection families | Legal obligation or regulatory interpretation | Personal data or regulated data is processed. | Data inventory, impact assessment, transfer assessment, retention schedule. |
| Supply Chain | Supplier and Cloud Governance Framework | Supplier risk, cloud assurance, NIST SP 800-161 SCRM, security, privacy, and resilience families | Industry practice or contractual requirement | External providers process data, host workloads, operate critical services, or provide AI capabilities. | Due diligence record, contractual control schedule, supplier risk register, exit plan. |
| Supply Chain | Trade and Supply-Chain Continuity Controls | WCO SAFE, ISO 28000, CTPAT, BASC, PIP, AEO, AEO-S, NEEC, OEA | Regulatory interpretation or contractual requirement | Organisation participates in customs, logistics, or trade-security programmes. | Programme audit record, gap assessment, corrective action evidence. |
| Resilience | Business Continuity and Resilience Framework | ISO 22301 continuity, NIST SP 800-34 continuity planning, COBIT DSS04, operational resilience families | Industry practice or regulatory interpretation | Services have recovery, availability, regulatory, or customer-impact obligations. | BIA, RTO/RPO register, test report, recovery plan, corrective action log. |
| Dev Security | Developer Security Requirements Standard | OWASP Top 10, OWASP ASVS, OWASP LLM Top 10, NIST SSDF (SP 800-218), NIST SP 800-53 SA/SI families, ISO 27001 Annex A.8.25 to A.8.34, SLSA | Architectural recommendation | Organisation develops or maintains software, AI systems, or automated pipelines. | Secure code review, SAST/DAST results, dependency scan, pipeline gate evidence. |

---

## Risk management control area mappings

The following table maps the enterprise risk management control areas to external framework families. It supports the Enterprise Governance and Risk Management Policy, the Enterprise Risk Management Standard, and the underlying risk procedures.

| Control Area | ISO 31000 | ISO 23894 | NIST SP 800-39 | NIST AI RMF | COBIT 2019 | CSA CCM v4.1 | Legal and Regulatory | Trade and Supply-Chain Programmes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Risk framework and governance | Clause 5 Framework | Clause 5 Governance | Organisation-wide RMF | Govern | APO12.01 Define risk context | GRM domain; GOV domain | Corporate governance charters | WCO SAFE, ISO 28000, BASC, PIP, CTPAT, AEO, AEO-S |
| Risk identification and analysis | Clause 6 Identify; Clause 6 Analyse | Clause 6.2 Identification; Clause 6.3 Analysis | Tasks 1 and 2 | Map; Measure | APO12.03 Assess risk | GRM domain | GDPR Article 25; CPPA accountability | WCO SAFE equivalence |
| Risk appetite and tolerance | Clause 5.4 Integration; Clause 5.6 Evaluation | Clause 5 Governance | Organisational risk strategy | Govern | APO12.02 Define risk appetite | GRM domain | Board-approved appetite statements | WCO SAFE equivalence |
| Treatment and control selection | Clause 6 Treat | Clause 6.4 Treatment | Task 3 Respond | Manage | APO12.06 Respond to risk | GRM domain | ISO 27001 Annex A controls | WCO SAFE equivalence |
| Monitoring and review | Clause 6 Monitor and review | Clause 6.5 Monitoring | Task 4 Monitor | Manage | MEA01; MEA02 | GRM domain | Regulatory reporting duties | WCO SAFE equivalence |
| AI model governance | Clause 6 lifecycle | Clauses 5 and 6 lifecycle | Organisational context | Govern; Manage | APO12; BAI03; DSS06 | AIS domain | EU AI Act; AIDA (pending, Canada) | Not applicable |
| Third-party and supply-chain risk | Clause 5.3 Design | Clause 6.2 Context and third-party data | Organisational context | Govern | APO10 Manage Suppliers | STA domain | Contractual clauses; data processing agreements; transfer impact assessments | WCO SAFE equivalence |
| Business continuity and resilience | Clause 5.2 Leadership | Not applicable | Organisational resilience context | Manage | DSS04 Manage Continuity | BCR domain | Local continuity regulations | WCO SAFE equivalence |
| Exception and acceptance | Clause 6 Treat decision | Clause 6.4 Acceptance criteria | Risk response acceptance | Govern | APO12.07 Risk acceptance | GRM domain | Documented approvals and durations | WCO SAFE equivalence |

---

## Minimum mapping fields for adopting organisations

Adopting organisations should extend this matrix with:

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

This matrix does not reproduce external framework content and does not establish compliance. Adopting organisations must validate source terms, applicability, control implementation, evidence quality, and operating effectiveness.

---

**End of Document**
