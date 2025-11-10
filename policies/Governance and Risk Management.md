# Policy: Governance and Risk Management

## Document Control

| Version | Date | Author | Change History |
|----------|------|---------|----------------|
| 0.1 |  |  | Initial Draft |

## Approval

| Role | Name | Approval Date |
|-------|------|---------------|
| Chief Information Officer (CIO) |  |  |
| Chief Information Security Officer (CISO) |  |  |
| Director of Compliance or Legal Counsel |  |  |

## 1. Purpose

This policy establishes the organizational governance and risk management framework, principles, roles, and control requirements that guide consistent identification, assessment, treatment, monitoring, and reporting of risk across the organization.  

It aligns with ISO 31000 Clause 5 Framework and Clause 6 Process, COBIT 2025 APO12 Manage Risk, Cloud Security Alliance (CSA) frameworks, NIST SP 800 39, ISO 23894 for AI risk, and the NIST AI RMF [Unverified 1.1]. It integrates risk, compliance, privacy, security, resilience, ethics, and sustainability across business, technology, data, and AI systems.

## 2. Scope

2.1 Applies to all business units, regions, subsidiaries, and joint ventures where the organization has operational control.  
2.2 Covers strategic, operational, financial, compliance, information security, privacy, safety, environmental, AI, and supply chain risks across on premise, cloud, multi cloud, edge, and supplier hosted services.  
2.3 Applies to employees, contractors, suppliers, and partners who process organizational or regulated data or operate systems on behalf of the organization.  
2.4 Includes all information types, with specific treatment for regulated and sensitive data such as manifests, customs documentation, datasets, prompts, embeddings, models, and AI agents.

## 3. Governance and Accountability

### 3.1 Board and Executive Oversight
a. The Board Risk Committee approves risk appetite and receives enterprise risk reporting.  
b. The CEO and executive committee ensure that risk is embedded in strategic planning and capital allocation.

### 3.2 Three Lines Model
a. First line owns and manages risk within approved appetite.  
b. Second line GRC function sets policy, facilitates risk methodology, challenges assertions, and consolidates reporting.  
c. Third line Internal Audit provides independent assurance over risk governance and control effectiveness.

### 3.3 Risk Sponsors and Owners
Each material risk is assigned an executive sponsor and an operational owner with defined accountability and decision rights.

### 3.4 AI Risk Accountability
The AI Governance Council approves AI risk appetite statements and exceptions for high risk AI uses aligned to ISO 23894 and the NIST AI RMF Govern function.

### 3.5 Committee Structure and Cadence
a. Enterprise Risk Committee meets quarterly for top risks, appetite, and emerging risk review.  
b. Model Risk Committee meets monthly for AI and analytics governance, validation, and monitoring.  
c. Operational procedures and system administration activities are documented and maintained under the IT Operations Documentation Framework to ensure that operational controls remain traceable to governance requirements.

### 3.6 Reporting
Standardized risk metrics and key risk indicators are reported at least monthly, with threshold alerts to executive stakeholders.

## 4. Policy and Control Statements

### 4.1 Risk Framework and Method
a. The organization shall maintain a standard risk framework aligned to ISO 31000 Clause 5 and Clause 6 with common taxonomy, criteria, and registers.  
b. Risk identification shall cover strategic, financial, operational, compliance, information security, privacy, third party, business continuity, and AI specific risks per ISO 23894.  
c. Risk analysis shall use qualitative and quantitative methods, including scenario analysis and stress testing for high exposure risks. Quantitative analysis should incorporate FAIR aligned methods for estimating loss event frequency, magnitude, and exposure, including AI driven processes.

### 4.2 Risk Appetite and Tolerances
a. The Board shall approve risk appetite statements for each material risk category, including AI usage classes and data sensitivity tiers.  
b. Tolerances and thresholds shall be defined for KRIs and AI system performance measures such as model drift and harmful outcome rates.

### 4.3 Treatment and Controls
a. Risk treatment plans shall state option, accountable owner, budget, residual risk, and acceptance criteria aligned to COBIT APO12.06.  
b. Control objectives shall be technology agnostic and mapped to ISO 27001 Annex A control families, Cloud Security Alliance frameworks, and applicable legal requirements.  
c. AI controls shall include dataset governance, model lifecycle governance, safety testing, bias and discrimination testing, human in the loop, secure deployment, and monitoring per ISO 23894 and the NIST AI RMF.

### 4.4 Registers and Records
a. Enterprise and local risk registers shall be maintained with unique identifiers, status, and last review date.  
b. An AI system inventory shall track purpose, risk level, model lineage, datasets, third parties, evaluation results, and deployment status.

### 4.5 Third Party and Cloud Risk
a. Suppliers shall undergo risk assessment, due diligence, contract controls, and ongoing monitoring aligned to COBIT APO10 and Cloud Security Alliance guidance.  
b. Cloud services shall be assessed for jurisdiction, residency, resilience, and shared responsibility clarity.

### 4.6 Business Continuity and Resilience
Business impact analysis, continuity strategies, disaster recovery, and crisis communications are mandatory for critical services per COBIT DSS04 and relevant Cloud Security Alliance guidance.

### 4.7 Privacy and Data Protection
Privacy by design shall be embedded in processes and AI systems, with cross border transfer assessments for GDPR, CPPA, PIPL, LGPD, and CBPR 2.0 where applicable.

### 4.8 Monitoring, Metrics, and Assurance
a. KRIs and control performance indicators shall be defined, baselined, and reviewed at least quarterly.  
b. Independent testing by Internal Audit shall verify design and operating effectiveness of key controls per COBIT MEA01.  
c. AI systems shall undergo pre deployment evaluations and post deployment monitoring for accuracy, robustness, safety, and fairness.

### 4.9 Issue and Exception Management
a. Risk issues and control deficiencies shall have tracked remediation plans and due dates.  
b. Formal risk acceptance is required where residual risk exceeds tolerance, with time bound exceptions and executive approval.

### 4.10 Reporting and Disclosure
a. Material risk changes shall be escalated within two business days.  
b. External reporting shall follow legal requirements and executive approval.

### 4.11 Continual Improvement
a. The risk framework, taxonomy, and metrics shall be reviewed annually for effectiveness and updated against new standards and laws.  
b. Lessons learned from incidents, near misses, and audits shall feed back into policies and controls.  
c. Digital trust indicators shall be used to measure outcomes and maturity per COBIT 2025 guidance.

## 5. Related Standards and Procedures

- Risk Management Standard methodology and taxonomy.  
- Risk Register Procedure and RACI.  
- Third Party Risk Standard and Due Diligence Procedure.  
- Business Continuity and Disaster Recovery Standard and Plans.  
- Privacy Impact Assessment and Cross Border Transfer Procedure.  
- AI Security and Risk Standard including model lifecycle and evaluation procedures.  
- Logging and Monitoring Standard and Control Testing Procedure.

## 6. References and Framework Alignment

- ISO 31000 Risk Management Clause 5 Framework and Clause 6 Process.  
- ISO 23894 AI Risk Management.  
- ISO 27001 and ISO 27002 control families and mappings.  
- COBIT 2025 APO12 Manage Risk, APO10 Manage Suppliers, MEA01 Monitor Evaluate and Assess Performance and Conformance, DSS04 Manage Continuity.  
- Cloud Security Alliance guidance and programs, including CCM and AICM.  
- NIST SP 800 39 Managing Information Security Risk.  
- NIST AI RMF Govern, Map, Measure, Manage [Unverified 1.1].  
- OECD AI Principles transparency, robustness, accountability.  
- Legal and regulatory GDPR, CPPA, PIPL, LGPD, CBPR 2.0, sector regulations as applicable.  
- [Unverified] Draft 2026 reference ISO 27090 series AI security controls for future readiness.

## 7. Compliance Mapping Table

| Control area | ISO 31000 | ISO 23894 | NIST SP 800 39 | NIST AI RMF | COBIT 2025 | CSA frameworks | Legal and policy |
|--------------|-----------|-----------|----------------|-------------|------------|----------------|------------------|
| Risk framework and governance | Clause 5 Framework | 5 Governance | Organization wide RMF | Govern | APO12.01 Define risk context | CCM GRM, related CSA guidance | Corporate governance charters |
| Risk identification and analysis | Clause 6 Identify Analyse | 6.2 Identification 6.3 Analysis | Tasks 1 and 2 | Map and Measure | APO12.03 Assess risk | CCM GRM, related CSA guidance | GDPR Art 25 privacy by design, CPPA requirements |
| Risk appetite and tolerance | 5.4 Integration 5.6 Evaluation | 5 Governance | Organization risk strategy | Govern | APO12.02 Define risk appetite | CCM GRM | Board approved appetite statements |
| Treatment and control selection | Clause 6 Treat | 6.4 Treatment | Task 3 Respond | Manage | APO12.06 Respond to risk | CCM GRM, AICM where applicable | ISO 27001 Annex A aligned controls |
| Monitoring and review | Clause 6 Monitor Review | 6.5 Monitoring | Task 4 Monitor | Manage | MEA01, MEA02 | CCM GRM | Regulatory reporting duties |
| AI model governance | [Unverified explicit clause numbering] | 5 and 6 full lifecycle | [Unverified] | Govern and Manage | APO12, BAI03, DSS06 | CSA AIS guidance where applicable | EU AI Act applicability, AIDA [Unverified] |
| Third party and cloud risk | 5.3 Design | 6.2 Context and third party data | Organization wide context | Govern | APO10 Manage Suppliers | CCM GRM, CSA GOV A | Contractual clauses and DPIAs |
| Business continuity and resilience | 5.2 Leadership | Not directly applicable | Organization resilience context | Manage | DSS04 Manage Continuity | CCM BCR | Local continuity regulations |
| Exception and acceptance | Clause 6 Treat decision | 6.4 Acceptance criteria | Risk response acceptance | Govern | APO12.07 Risk acceptance | CCM GRM | Documented approvals and durations |

**Note:** [Unverified] indicates areas where explicit sub clause numbering or 2026 readiness references may require validation against the most recent publications.

## 8. Development, Implementation, and Monitoring

8.1 All governance artefacts follow the organizational change management process. Version control and archival of superseded versions are mandatory for audit traceability. Each update must identify its parent and dependent documents per the Document Architecture and Interrelationship Framework.  
8.2 Approved versions are stored in the GRC repository as the authoritative source.  
8.3 Approved artefacts must be implemented by accountable leaders, who ensure training, adoption, and demonstrable compliance.  
8.4 Monitoring is performed through audits, metrics, and maturity assessments defined in the GRC Metrics and Digital Trust Performance Framework.  
8.5 All deviations follow the Exception Process.

## 9. Exception Process

a. Submission: Employees may submit an exception request through the designated process portal.  
b. Evaluation: Each request must include business justification, risk level, duration, and compensating controls.  
c. Approval:  
   - Temporary under 90 days: CIO approval.  
   - Extended or high risk: CIO and CISO approval and Legal review.  
d. Tracking: All exceptions are logged, assigned expiry dates, and reviewed periodically.

## 10. Definitions

Refer to the Role Authority Register for definitions of organizational roles and authorities.

## 11. Summary of Alignment

- ISO 31000 Clauses 5 and 6 reflected in governance, process, and continual improvement.  
- ISO 23894 integrated for AI risk taxonomy, lifecycle governance, evaluation, and monitoring.  
- NIST SP 800 39 integrated for organizational risk context, response, and monitoring.  
- NIST AI RMF Govern, Map, Measure, Manage incorporated for AI systems [Unverified 1.1].  
- COBIT 2025 APO12, APO10, MEA01, DSS04 referenced for governance, supplier, assurance, and continuity.  
- Cloud Security Alliance guidance used for cloud and AI control alignment.  
- OECD AI Principles addressed via transparency, robustness, human oversight, and accountability clauses.  
- Data protection and cross border requirements acknowledged for GDPR, CPPA, PIPL, LGPD, and CBPR 2.0.

**End of Policy**
