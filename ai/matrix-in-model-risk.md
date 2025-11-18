Document Title
In Model Risk Mapping

Document Type
Matrix

Version
0.0.1

Date
2025 November 18

Owner
Chief Compliance Officer

Approving Authority
Chief Legal Officer

Related Documents
In Model Risk Framework (framework-in-model-risk.md)
In Model Risk Standard (standard-in-model-risk.md)
AI Governance Framework (framework-ai-governance.md)
AI System Audit and Certification Framework (framework-ai-system-audit-and-certification.md)
AI Lifecycle Governance Standard (standard-ai-lifecycle-governance.md)

Classification
Public

Category
Artificial Intelligence

Review Frequency
Annual

Repository Path
/ai/matrix-in-model-risk.md

Confidentiality
Public

---

## Purpose

This matrix maps requirements from the In Model Risk Framework and the In Model Risk Standard to leading governance, assurance, and AI-risk frameworks. It supports audit traceability, consistent interpretation of controls, and alignment with international best practices for AI assurance.

Mapped frameworks include ISO 42001, ISO 23894, ISO 24028, NIST AI RMF, COBIT 2025, and CSA CCM v5.

## Scope

This matrix applies to all AI and machine learning systems covered under the In Model Risk Framework and In Model Risk Standard. Mappings span interpretability, representation risk, adversarial robustness, alignment, lifecycle governance, documentation, and monitoring.

## In Model Risk Mapping Matrix

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

## Framework Alignment Notes

### ISO 42001  
Mappings align to governance, transparency, robustness, monitoring, and lifecycle requirements.

### ISO 23894  
Coverage reflects risk identification, bias evaluation, risk treatment, and monitoring.

### ISO 24028  
Mappings align to interpretability, transparency, robustness, and trustworthiness.

### NIST AI RMF  
Mappings align with the Govern, Map, Measure, and Manage functions.

### COBIT 2025  
Control mappings align to APO, BAI, DSS, EDM, and MEA governance objectives.

### CSA CCM v5  
Mappings align to AIS, SEF, LOG, DSI, and GRM AI and security control domains.

## References

- In Model Risk Framework  
- In Model Risk Standard  
- Key Terms and Definitions Register  
- Role Authority Register
