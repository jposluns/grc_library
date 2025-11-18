# Mapping: In Model Risk Framework and Standard

## Metadata

| Field | Details |
|-------|----------|
| **Document Title** | In Model Risk Mapping |
| **Document Type** | Mapping |
| **Version** | 0.1 |
| **Date** |  |
| **Document Owner** | Chief Compliance Officer (CCO) |
| **Approving Authority** | Chief Legal Officer and General Counsel (CLO/GC) |
| **Related Documents** | Framework: In Model Risk; Standard: In Model Risk; Framework: AI Governance; Framework: AI System Audit and Certification; Standard: AI Lifecycle Governance |
| **Classification** | Internal |
| **Category** | Artificial Intelligence |
| **Review Frequency** | Annual |
| **Repository Path** | /ai/mapping-ai-in-model-risk.md |
| **Confidentiality** | Internal Use Only |



## Document Control

| Version | Date | Author | Change History |
|----------|------|---------|----------------|
| 0.1 |  |  | Initial Draft |



## Approval

| Role | Name | Approval Date |
|-------|------|---------------|
| Chief Information Officer (CIO) |  |  |
| Chief Risk Officer (CRO) |  |  |
| Chief Information Security Officer (CISO) |  |  |
| Chief Compliance Officer (CCO) |  |  |
| Chief Legal Officer / General Counsel (CLO/GC) |  |  |
| Chief Technology Officer (CTO) |  |  |
| Chair, AI Governance Council |  |  |



# Purpose

This mapping document links the requirements of the **In Model Risk Framework** and the **In Model Risk Standard** to established governance, security, and AI assurance frameworks.  
It enables consistent audit interpretation, traceability of enterprise controls, and alignment with global best practices for safe and transparent AI systems.

Mapped frameworks include:

- ISO 42001  
- ISO 23894  
- ISO 24028  
- NIST AI Risk Management Framework  
- COBIT 2025  
- CSA CCM v5  



# Scope

This document applies to all enterprise AI and ML systems and all lifecycle phases included within the In Model Risk Framework and the In Model Risk Standard.

Mappings cover:

- interpretability  
- representation risk  
- adversarial robustness  
- alignment and drift  
- lifecycle governance  
- evidence expectations  
- monitoring and incident management  



# Mapping Overview Table

| In Model Risk Domain or Control | ISO 42001 | ISO 23894 | ISO 24028 | NIST AI RMF | COBIT 2025 | CSA CCM v5 |
|---------------------------------|-----------|-----------|-----------|-------------|-------------|-------------|
| Interpretability baseline | 6.4.2 Transparency | 7.2 Explainability Risk | 6.2 Transparency | Govern 2.1, Measure 2.3 | APO14.03, BAI03.05 | AIS 01, AIS 02 |
| Feature attribution | 6.4.3 Model Documentation | 7.3 Data and Model Analysis | 6.4 Explainability Techniques | Govern 2.3, Map 3.3 | BAI03.06 | AIS 05 |
| Representation analysis | 6.4.4 Technical Controls | 7.4 Bias and Fairness Evaluation | 7.4 Bias Considerations | Map 3.4, Measure 2.4 | DSS06.02 | GRM 02, AIS 05 |
| Mechanistic interpretability | 6.4.5 Advanced Interpretability | 8.2 Risk Treatment | 6.5 Technical Assurance | Govern 2.4, Measure 2.5 | BAI08.03 | AIS 06 |
| Adversarial robustness | 6.5.4 Security and Safety Controls | 8.3 Adversarial Risk | 6.6 Robustness | Measure 2.6, Manage 3.4 | DSS05.02, DSS05.04 | SEF 02, AIS 07 |
| Gradient and perturbation tests | 6.5.4 | 8.3.2 | 6.6.2 | Measure 2.6 | DSS05.03 | AIS 07 |
| Red team evaluation | 6.5.4, 7.3.2 | 8.3.3 | 6.6.3 | Govern 2.5, Manage 3.4 | DSS05.05 | SEF 03, AIS 07 |
| Out of distribution testing | 6.5.4 | 8.4 | 6.7 | Measure 2.4 | DSS06.03 | AIS 06 |
| Alignment validation | 6.3.3 Ethical Alignment | 6.6 | 7.3 | Govern 1.4, Govern 2.1 | EDM01.02 | GRM 01 |
| Drift detection | 6.6.2 Monitoring | 9.2 Performance Evaluation | 7.5 Monitoring | Manage 3.5 | DSS01.03 | LOG 01 |
| Data provenance and lineage | 6.4.2, 6.4.3 | 7.2 | 6.3 | Map 3.2 | BAI03.02 | DSI 02 |
| Training data documentation | 6.4.3 | 7.2 | 6.3.2 | Map 3.1 | BAI03.03 | DSI 01 |
| Model cards | 6.4.3 | 7.3 | 6.2 | Govern 2.3 | BAI03.05 | AIS 01 |
| System cards | 6.4.3, 6.4.4 | 7.3 | 6.2 | Govern 2.3 | BAI03.05 | AIS 01 |
| Deployment approval | 6.7 Validation | 8.2, 8.4 | 6.8 | Govern 1.2 | BAI05.06 | GRM 02 |
| Continuous monitoring | 6.6.2 | 9.2 | 7.5 | Manage 3.5 | DSS01.03 | LOG 01 |
| Periodic re evaluation | 6.7.1 | 10.2 | 7.6 | Manage 3.6 | MEA01.02 | GRM 03 |
| Incident integration | 6.6.3 | 10.3 | 7.6.3 | Manage 3.4 | DSS02.02 | SEF 04 |



# Framework Alignment Notes

### ISO 42001  
The In Model Risk Framework aligns with ISO 42001 requirements for governance, transparency, robustness, monitoring, and lifecycle controls.

### ISO 23894  
This mapping supports ISO 23894’s emphasis on AI risk management, bias mitigation, and risk treatment initiatives.

### ISO 24028  
Interpretability, transparency, robustness, and trustworthiness mappings are consistent with ISO 24028’s trustworthiness guidelines.

### NIST AI Risk Management Framework  
The Model Risk Framework reflects NIST’s Govern, Map, Measure, and Manage functions and aligns with evaluation and documentation activities.

### COBIT 2025  
Control objectives map directly to governance, assurance, and monitoring elements in BAI, DSS, APO, EDM, and MEA domains.

### CSA CCM v5  
Mappings align with AIS, SEF, LOG, DSI, and GRM control areas governing AI, security, logging, data handling, and risk management.



## Definitions

Key terms and acronyms used in this document are defined in the **Key Terms and Definitions Register**.

Definitions of organizational roles and authorities are provided in the **Role Authority Register**.



**End of Document**
