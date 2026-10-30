# AI Algorithmic Compliance Checklist

**Document Title:** AI Algorithmic Compliance Checklist\
**Document Type:** Checklist\
**Version:** 1.0.31\
**Date:** 2026-10-30\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](policy-ai-compliance.md), [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md), [`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md), [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`ai/template-model-card.md`](template-model-card.md), [`ai/template-system-card.md`](template-system-card.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI governance or regulatory change\
**Repository Path:** [`ai/checklist-ai-algorithmic-compliance.md`](checklist-ai-algorithmic-compliance.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose and usage

This checklist provides a structured assessment tool for evaluating AI system compliance before deployment and at periodic review intervals. It is used by the AIGC and CISO as part of the AI System Impact Assessment Procedure ([`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md)) and the AI System Audit and Certification Framework ([`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md)).

The checklist is completed by the AI System Owner in the first instance, reviewed by the CISO, and reviewed by the Data Protection Officer for items in Section B. For AI systems classified High under the organizational AI risk classification, the completed checklist is submitted to the AIGC for approval before deployment.

### Completion instructions

- For each item, select the status: **Yes**, **No**, **Partial**, or **N/A**.
- **Evidence:** Record the document, record, test result, or system reference that substantiates the status selected.
- **Owner:** Record the role responsible for the control.
- **Notes:** Record any relevant context, caveats, or links to associated CAPA records.
- **N/A** may only be used where the item genuinely does not apply to the system. The reason must be recorded in the Notes field.

---

## Checklist header

| Field | Entry |
|---|---|
| AI System Name | |
| AI System Register ID | |
| Risk Tier (EU AI Act) | |
| Organizational AI risk classification (informed by NIST AI RMF 1.0) | |
| Assessment Type | Pre-deployment / Annual review / Post-incident review / Post-modification review |
| Assessment Date | |
| Assessed By | |
| CISO Review Date | |
| Data Protection Officer Review Date | |
| AIGC Approval Date (high-risk systems only) | |

---

## Section a: governance and documentation

*Synthesized from: EU AI Act Art. 11, 13; ISO/IEC 42001:2023 §8.4; ISO/IEC 42005:2025 §5.7, §6.3; NIST AI RMF 1.0 Govern function; Canada Treasury Board Algorithmic Impact Assessment*

| # | Control Item | Status (Yes / No / Partial / N/A) | Evidence | Owner | Notes |
|---|---|---|---|---|---|
| A1 | AI system registered in the AI System Register with complete metadata, including system name, version, deployment context, risk classification, impact level, intended use, and data categories | | | | |
| A2 | Risk classification documented for both the EU AI Act tier and the organizational AI risk classification (Minimal, Limited, High, Unacceptable; informed by the NIST AI RMF 1.0, which prescribes no tier taxonomy), per the EU AI Act scoping in [`ai/policy-ai-compliance.md`](policy-ai-compliance.md) Section 4; classification reviewed and approved by the AIGC | | | | |
| A3 | Model card completed and current, reflecting the model version in production ([`ai/template-model-card.md`](template-model-card.md)) | | | | |
| A4 | System card completed and current, reflecting the current deployment context, human oversight design, and known limitations ([`ai/template-system-card.md`](template-system-card.md)) | | | | |
| A5 | AI system owner (technical accountability) and operational owner (business accountability) designated and documented in the AI System Register | | | | |
| A6 | Training data provenance documented and validated, including data sources, data quality measures, data exclusions, and governance agreements | | | | |
| A7 | Data quality and bias assessment completed before deployment and at the most recent periodic audit; methodology and results documented | | | | |
| A8 | Explainability approach documented, including the method used, its limitations, and how outputs are communicated to users and overseers | | | | |
| A9 | Intended use, prohibited use cases, and operational limitations clearly defined in the system card and communicated to users and business unit owners | | | | |
| A10 | Human oversight mechanism documented in the system card and tested: designated overseers identified; override capability verified; training completed | | | | |
| A11 | AI system impact level assessed and recorded per the [AI System Impact Assessment Procedure](procedure-ai-system-impact-assessment.md) Step 7 (low, moderate, high, or critical), as entered in the Impact Level field of the AI System Register; and, separately, the Canada Treasury Board Algorithmic Impact Assessment (AIA) impact level recorded (Level I little-to-no, Level II moderate, Level III high, or Level IV very high), scoring the impact on individuals' rights and freedoms; their equality, dignity, privacy, and autonomy; their health and well-being; their economic interests; and environmental-ecosystem sustainability; where the two levels differ, the higher governs (Step 7) and drives the proportionate controls; where the Treasury Board AIA level is the higher, the Impact Level field carries the procedure level aligned to it in the Step 7 table (Level II Moderate, Level III High, Level IV Critical), not the lower level from the procedure's own criteria | | | | |

---

## Section b: data and privacy compliance

*Synthesized from: GDPR Art. 5, 9, 22, 25, 35; EU AI Act Art. 10, 13; ISO/IEC 42001:2023 §8.4; ISO/IEC 27701:2025*

| # | Control Item | Status (Yes / No / Partial / N/A) | Evidence | Owner | Notes |
|---|---|---|---|---|---|
| B1 | Personal data processing performed by the AI system has been mapped; lawful basis for each processing activity is documented | | | | |
| B2 | Data minimization principle applied to training and inference data: only data necessary for the stated purpose is collected and processed | | | | |
| B3 | The required impact assessments (a DPIA under GDPR Article 35, the AI System Impact Assessment, and the EU AI Act Article 27 fundamental rights impact assessment (FRIA) where triggered) are completed and composed per the [Integrated AI and Privacy Assessment Procedure](procedure-integrated-ai-and-privacy-assessment.md); where a FRIA is required it does not substitute for the DPIA, and under Article 27(4) as amended the deployer may cross-reference the DPIA in the FRIA | | | | |
| B4 | Where the AI system may process data relating to children, specific safeguards are implemented and documented | | | | |
| B5 | Cross-border data transfer controls are in place and documented for any training or inference data transferred across jurisdictions | | | | |
| B6 | Data retention and deletion obligations for training data, inference logs, and output data are documented and implemented | | | | |
| B7 | Training data has been subject to a re-identification risk assessment; residual re-identification risk is documented and accepted by the Data Protection Officer | | | | |
| B8 | Where consent is the lawful basis for using training data, consent validity has been verified and records are maintained | | | | |

---

## Section c: security controls

*Synthesized from: OWASP LLM Top 10 (2026); MITRE ATLAS adversarial ML evaluation; EU AI Act Art. 15; NIST AI RMF 1.0 Measure 2.7; ISO/IEC 42001:2023 §8.3*

| # | Control Item | Status (Yes / No / Partial / N/A) | Evidence | Owner | Notes |
|---|---|---|---|---|---|
| C1 | Prompt injection attack resistance tested (OWASP LLM01:2026): system has been assessed for direct and indirect prompt injection; findings documented and remediated | | | | |
| C2 | Training data poisoning controls in place (OWASP LLM05:2026 Data and Model Poisoning): data provenance validated; integrity controls applied; adversarial data injection tested | | | | |
| C3 | Model inversion and membership inference risks assessed (NIST AI RMF 1.0 Measure 2.7; not a distinct OWASP LLM Top 10:2026 category but related to LLM02:2026 Sensitive Information Disclosure): risk assessment documented; mitigations implemented where risk is material | | | | |
| C4 | Output validation implemented before AI outputs are used in downstream decisions or communicated to users: validation logic documented and tested | | | | |
| C5 | AI system access controls verified: principle of least privilege applied; service accounts are isolated; privileged access is logged and reviewed | | | | |
| C6 | AI system logs (inputs, outputs, decisions, anomalies) forwarded to the SIEM platform and retained for a minimum of 7 years per the AI decision and detection logs row in [`governance/register-data-retention-schedule.md`](../governance/register-data-retention-schedule.md) | | | | |
| C7 | Adversarial robustness testing completed per MITRE ATLAS evaluation: test scenarios documented; results recorded; findings remediated or risk-accepted | | | | |
| C8 | Third-party model and API dependencies assessed for supply chain risk: provider security posture reviewed; dependency inventory maintained; fallback arrangements documented | | | | |

---

## Section d: operational controls

*Synthesized from: EU AI Act Art. 14, 26; NIST AI RMF 1.0 Manage function; IEEE 7000-2021; Canada Treasury Board Algorithmic Impact Assessment*

| # | Control Item | Status (Yes / No / Partial / N/A) | Evidence | Owner | Notes |
|---|---|---|---|---|---|
| D1 | Human oversight assigned and documented for all automated or AI-assisted decisions that directly affect individuals: oversight responsibilities are role-specific and not delegated entirely to the AI system | | | | |
| D2 | Automated decision-making with significant impact on individuals is subject to a human review pathway: individuals can request human review; the pathway is tested and documented | | | | |
| D3 | Model performance monitoring is active: accuracy, data drift, and bias drift metrics are captured; alerting thresholds are set; monitoring results are reviewed regularly | | | | |
| D4 | Incident response plan includes AI-specific scenarios: prompt injection, model compromise, adversarial attack, biased output at scale, and GPAI model outage are included | | | | |
| D5 | AI system user notification and transparency disclosures are in place: users are informed they are interacting with an AI system before or at the point of first interaction | | | | |
| D6 | AI-generated content and deployer transparency implemented per EU AI Act Art. 50: as a PROVIDER, synthetic audio, image, video, or text outputs are marked as artificially generated in a machine-readable format (Art. 50(2)), except for assistive standard-editing or non-substantially-altering functions and law-authorized uses; as a DEPLOYER (Art. 50(4)), deep-fake image, audio, or video content is disclosed as artificially generated or manipulated, except where the use is authorized by law to detect, prevent, investigate or prosecute criminal offences (where the content forms part of an evidently artistic, creative, satirical, fictional or analogous work or programme, the disclosure is limited to the existence of such generated or manipulated content in an appropriate manner that does not hamper the display or enjoyment of the work), and AI-generated or manipulated text published with the purpose of informing the public on matters of public interest is disclosed as artificially generated or manipulated, except where the use is authorized by law to detect, prevent, investigate or prosecute criminal offences or where the content has undergone a process of human review or editorial control and a natural or legal person holds editorial responsibility for its publication; as a DEPLOYER of an emotion recognition or biometric categorization system (Art. 50(3)), the natural persons exposed to it are informed of the operation of the system in a clear and distinguishable manner at the latest at the time of the first interaction or exposure, in a form that conforms to the applicable accessibility requirements (Art. 50(5), which applies the same timing and accessibility requirement to the Art. 50(4) disclosures) and the personal data is processed in accordance with Regulations (EU) 2016/679 and (EU) 2018/1725 and Directive (EU) 2016/680, as applicable, except for a system permitted by law to detect, prevent or investigate criminal offences, subject to appropriate safeguards for the rights and freedoms of third parties and in accordance with Union law | | | | |
| D7 | Reversibility and duration of the decision's impacts assessed and recorded (reversible, likely reversible, difficult to reverse, or irreversible; and brief, lasting months, lasting years, or perpetual), consistent with the Canada Treasury Board Algorithmic Impact Assessment impact axes; the assessment informs the human-review pathway (D2) and any escalation | | | | |

---

## Section e: regulatory compliance

*Synthesized from: EU AI Act 2024 (Regulation (EU) 2024/1689); Canada TBS Directive on Automated Decision-Making and ISED Voluntary Code (AIDA lapsed with Bill C-27 at the January 2025 prorogation); UK AI regulation white paper (CP 815) and government response (CP 1019); ISO/IEC 42001:2023; NIST AI RMF 1.0 Govern function*

| # | Control Item | Status (Yes / No / Partial / N/A) | Evidence | Owner | Notes |
|---|---|---|---|---|---|
| E1 | EU AI Act compliance obligations identified and documented for this specific system: risk tier confirmed; applicable Articles listed; deployer obligations addressed | | | | |
| E2 | Canada automated-decision-making governance assessed and documented: applicability of the TBS Directive on Automated Decision-Making determined (binding on federal institutions subject to the Policy on Service and Digital; a leading-practice benchmark otherwise); ISED Voluntary Code commitments considered for generative-AI systems; AIDA tracked as a lapsed planning indicator (Bill C-27 died on the 2025-01-06 prorogation; per a June 2025 ministerial statement not held in the reference base, AIDA is reported not to return in its original form, which an adopter confirms directly), monitored for any successor AI-governance instrument rather than treated as pending reintroduction <!-- ref-absence: AIDA ministerial statement --> | | | | |
| E3 | UK AI regulation framework reviewed: the five cross-sectoral principles mapped to AI-governance controls; ICO AI and data protection guidance and applicable sector regulators' AI guidance considered | | | | |
| E4 | ISO/IEC 42001:2023 alignment gaps for this system identified and tracked: gaps are recorded in the CAPA system and assigned to owners | | | | |
| E5 | Post-market monitoring plan in place for high-risk systems: plan documents metrics, thresholds, frequency, responsible party, and escalation path | | | | |
| E6 | Serious incident reporting pathway established: reporting contacts documented; internal escalation path tested; the EU AI Act Art. 73 reporting deadlines acknowledged, each day limit counted from when the provider or, where applicable, the deployer becomes aware of the serious incident (immediately after the provider has established a causal link between the AI system and the serious incident, or the reasonable likelihood of such a link, and in any event no later than 15 days, the period taking account of the incident's severity (Art. 73(2)); immediately, and no later than 2 days, for a widespread infringement or a serious and irreversible disruption of the management or operation of critical infrastructure (Art. 3(49)(b); Art. 73(3)); immediately after the provider or the deployer has established, or as soon as it suspects, a causal relationship between the high-risk AI system and the serious incident, and no later than 10 days, for the death of a person (Art. 73(4))); recipients are, for providers of high-risk AI systems placed on the Union market, the market surveillance authorities of the Member States where the incident occurred under Article 73(1), or, by way of derogation from Article 73 for providers of high-risk AI systems subject to the AI Office's competence under Article 75(1), the AI Office under Article 75(1a), with Article 73(2) to (9) applying mutatis mutandis and the AI Office promptly transmitting the relevant information to the market surveillance authority of the Member State in whose territory the provider or its legal representative is situated; for those Article 73(1) providers, where the high-risk AI system is a safety component of a device, or is itself a device, covered by Regulations (EU) 2017/745 and (EU) 2017/746, notification is limited to Article 3, point (49)(c) incidents and is made to the national competent authority chosen for that purpose by the Member States where the incident occurred (Article 73(10)); for high-risk AI systems referred to in Annex III that are placed on the market or put into service by providers subject to Union legislative instruments laying down reporting obligations equivalent to those set out in the EU AI Act, notification on the Article 73(1) route and, because Article 75(1a) applies Article 73(2) to (9) mutatis mutandis, on the Article 75(1a) route is limited to Article 3, point (49)(c) incidents and is made to that route's recipient, since Article 73(9) names none (Article 73(9)); where the organization, acting as a deployer of a high-risk AI system, has identified a serious incident, it immediately informs first the provider, and then the importer or distributor and the relevant market surveillance authorities of that incident (Article 26(5)); the duty does not cover sensitive operational data of deployers that are law enforcement authorities (Article 26(5)), and whether this also limits a fallback report made under Article 73 is not settled by the held text, so Legal confirms it; if the organization cannot reach the provider, the Article 73 procedure applies to it mutatis mutandis (Article 26(5)), and, as reasoning rather than express text, applying Article 73(1) mutatis mutandis (Article 26(5)), it reports, subject to the separate-entity case below, to the market surveillance authorities of the Member States where the incident occurred; Article 26(5) applies Article 73 without limiting it to particular paragraphs, so Article 73(10) also applies: where the high-risk AI system is a safety component of a device, or is itself a device, covered by Regulations (EU) 2017/745 and (EU) 2017/746, the organization's fallback notification is limited to Article 3, point (49)(c) incidents and, subject to the separate-entity case below, is made to the national competent authority chosen for that purpose by the Member States where the incident occurred; for the same reason Article 73(9) also applies, although its condition concerns the provider: where the high-risk AI system is referred to in Annex III and is placed on the market or put into service by a provider subject to Union legislative instruments laying down reporting obligations equivalent to those set out in the EU AI Act, the organization's fallback notification is limited to Article 3, point (49)(c) incidents, and, since Article 73(9) names no recipient, goes to the fallback recipient set out in this item, subject to the separate-entity case below; the Article 75(1a) route names providers; Article 75(1) applies the AI Office's exclusive competence for supervision and enforcement to the deployers of the systems it lists "only when they are also the provider or form part of the same undertaking as the provider"; as reasoning, since Article 75(1a) names only providers, a deployer's fallback report follows Article 73 (Article 26(5)), subject to the separate-entity case below; where the organization is itself the provider, it reports as provider on whichever of the provider routes above applies; where neither applies, for example a system it only puts into service for its own use outside the AI Office's Article 75(1) competence, Legal confirms the route; for a deployer of a system within the AI Office's Article 75(1) competence that is a separate entity in the provider's undertaking, the held texts do not state the recipient of a fallback report; Legal confirms it; the statutory Article 26 duty follows the application dates in Section 5 of the AI compliance policy; earlier internal escalation remains required | | | | |

---

## Scoring and disposition guidance

### Scoring

1. Count the total number of applicable items (excluding N/A).
2. Count the number of items with a status of **Yes**.
3. Calculate the compliance score as: (Yes count / Applicable item count) × 100.

| Score | Disposition |
|---|---|
| 95% or above | Compliant: proceed to deployment or confirm continued deployment |
| 80% to 94% | Conditional: CAPA records must be raised for all No and Partial items before deployment is approved for systems classified High under the organizational AI risk classification; for systems in production, remediation plan required within 60 days |
| Below 80% | **High finding**: system must not be deployed until score reaches at least 80%; systems already in production require a formal remediation plan approved by the AIGC within 60 days; CISO reports to AIGC at next scheduled meeting |

### Mandatory CAPA requirements for high-risk systems

For any AI system classified High under the organizational AI risk classification:

- Any item in **Section A** with a status of **No** or **Partial** must generate a CAPA record before deployment is approved.
- Any item in **Section C** with a status of **No** or **Partial** must generate a CAPA record before deployment is approved.
- CAPAs raised as a condition of deployment must be completed and verified by the CISO before the AI system goes live.

CAPA records are managed per [`compliance/policy-compliance-and-audit-management.md`](../compliance/policy-compliance-and-audit-management.md).

### Re-assessment triggers

This checklist must be re-completed when:

- The AI system undergoes a substantial modification.
- The AI system is deployed in a new context or to a new user population.
- A serious AI incident involving the system is resolved and the system is returned to production.
- Applicable regulations or standards are materially updated.
- The AIGC or CISO determines a re-assessment is warranted based on post-market monitoring signals.

---

**End of Document**
