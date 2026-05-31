# Supplier Security Questionnaire

**Document Title:** Supplier Security Questionnaire\
**Document Type:** Template\
**Version:** 1.0.1\
**Date:** 2026-05-28\
**Owner:** Supplier Risk Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`supply-chain/README.md`](README.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md), [`supply-chain/procedure-supplier-onboarding-security-review.md`](procedure-supplier-onboarding-security-review.md), [`supply-chain/procedure-supplier-ongoing-monitoring.md`](procedure-supplier-ongoing-monitoring.md), [`supply-chain/register-supplier-risk-template.md`](register-supplier-risk-template.md), [`compliance/logistics/register-ctpat-united-states-it-controls.md`](../compliance/logistics/register-ctpat-united-states-it-controls.md), [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](../compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md)\
**Classification:** Public\
**Category:** Supply Chain Governance: Assessment\
**Review Frequency:** Annual and upon significant standards revision\
**Repository Path:** [`supply-chain/template-supplier-security-questionnaire.md`](template-supplier-security-questionnaire.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This questionnaire is issued to suppliers and third-party service providers to gather information about their information security and privacy controls. Responses are used to assess whether the supplier meets the organisation's requirements under [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md).

**Instructions for suppliers:** Complete all applicable sections. Where a question does not apply to your organisation, enter "N/A" and provide a brief explanation. Responses may be verified through independent evidence or audit. Provision of false or misleading information may result in disqualification from the selection process or termination of an existing contract.

---

## Section 1: organisation profile

| Question | Response |
|---|---|
| 1.1 Legal entity name | |
| 1.2 Primary business address and registered jurisdiction | |
| 1.3 Does your organisation have a parent company? If yes, provide name. | |
| 1.4 Number of employees | |
| 1.5 Describe the services you provide to the Organisation | |
| 1.6 What countries and regions will you process or store the Organisation's data in? | |

---

## Section 2: security governance

| Question | Yes/No | Evidence / Comment |
|---|---|---|
| 2.1 Does your organisation have a documented and approved information security policy? | | |
| 2.2 Is the policy reviewed and updated at least annually? | | |
| 2.3 Does your organisation have a designated information security officer or equivalent? | | |
| 2.4 Does your organisation hold a current ISO 27001:2022 certification? (If yes, provide certificate details.) | | |
| 2.5 Does your organisation have a current SOC 2 Type II report? (If yes, provide opinion date and service scope.) | | |
| 2.6 Has your organisation undergone any security audits in the past 24 months by an external assessor? | | |
| 2.7 Does your organisation have a documented risk management process? | | |

---

## Section 3: access control and identity management

| Question | Yes/No | Evidence / Comment |
|---|---|---|
| 3.1 Does your organisation enforce a documented access control policy based on least privilege? | | |
| 3.2 Is multi-factor authentication (MFA) required for: (a) all remote access; (b) privileged accounts; (c) cloud management consoles? | | |
| 3.3 Are user accounts reviewed at least quarterly for appropriateness? | | |
| 3.4 Are accounts disabled within 24 hours of an employee's departure or role change? | | |
| 3.5 Are shared or generic accounts prohibited for privileged access? | | |
| 3.6 Is privileged access management (PAM) or just-in-time privilege activation in use? | | |

---

## Section 4: vulnerability and patch management

| Question | Yes/No | Evidence / Comment |
|---|---|---|
| 4.1 Does your organisation conduct periodic vulnerability scanning of internet-facing and internal systems? | | |
| 4.2 What is your target patching timeline for critical-severity vulnerabilities? | | |
| 4.3 What is your target patching timeline for high-severity vulnerabilities? | | |
| 4.4 Has your organisation conducted an external penetration test in the last 12 months? If yes, provide test date and tester's qualification (e.g., CREST, CHECK, OSCP). | | |
| 4.5 Are penetration test findings tracked to remediation? | | |
| 4.6 Is endpoint detection and response (EDR) deployed on all managed devices? | | |

---

## Section 5: network and infrastructure security

| Question | Yes/No | Evidence / Comment |
|---|---|---|
| 5.1 Are firewalls deployed to control inbound and outbound network traffic? | | |
| 5.2 Are intrusion detection or prevention systems (IDS/IPS) deployed? | | |
| 5.3 Are production, development, and test environments logically separated? | | |
| 5.4 Is data encrypted in transit using TLS 1.2 or higher? | | |
| 5.5 Is sensitive data encrypted at rest? | | |
| 5.6 Are network access logs retained and reviewed? | | |

---

## Section 6: incident response

| Question | Yes/No | Evidence / Comment |
|---|---|---|
| 6.1 Does your organisation have a documented incident response plan (IRP)? | | |
| 6.2 Is the IRP tested at least annually? | | |
| 6.3 Do you have 24/7 security monitoring capability? If not, what are your monitoring hours? | | |
| 6.4 What is your target time to detect a security incident? | | |
| 6.5 What is your target time to notify clients of a security incident affecting their data or services? | | |
| 6.6 Please describe a significant security incident from the past 24 months and how it was handled. (If none, state so.) | | |

---

## Section 7: data protection and privacy

| Question | Yes/No | Evidence / Comment |
|---|---|---|
| 7.1 Does your organisation process personal data on behalf of your clients? | | |
| 7.2 Does your organisation have a documented privacy policy and data protection procedures? | | |
| 7.3 Is your organisation subject to GDPR or UK GDPR? If yes, is a Data Protection Officer (DPO) appointed? | | |
| 7.4 Are you willing to sign a Data Processing Agreement (DPA) with the Organisation? | | |
| 7.5 Will any personal data be transferred to countries outside the EEA or UK? If yes, what transfer mechanism is used (adequacy, SCCs, IDTA, BCRs)? | | |
| 7.6 Does your organisation have a documented data breach notification procedure? | | |
| 7.7 Have you had any personal data breaches in the past 24 months? If yes, briefly describe. | | |
| 7.8 Does your organisation have a process for honouring individual rights requests (access, erasure, portability)? | | |

---

## Section 8: business continuity and resilience

| Question | Yes/No | Evidence / Comment |
|---|---|---|
| 8.1 Does your organisation have a documented Business Continuity Plan (BCP)? | | |
| 8.2 Has the BCP been tested in the past 12 months? | | |
| 8.3 What are your target Recovery Time Objective (RTO) and Recovery Point Objective (RPO) for services provided to the Organisation? | | |
| 8.4 Do you have an IT Disaster Recovery Plan? | | |
| 8.5 Are backups performed and tested regularly? What is your backup retention period? | | |
| 8.6 Do you have redundant data centre or cloud region capability? | | |

---

## Section 9: sub-contractors and fourth parties

| Question | Yes/No | Evidence / Comment |
|---|---|---|
| 9.1 Will you use sub-contractors to deliver services to the Organisation? | | |
| 9.2 If yes, please list material sub-contractors and the services they provide. | | |
| 9.3 Do you require sub-contractors to meet equivalent security standards? | | |
| 9.4 Do you conduct security assessments of material sub-contractors? | | |
| 9.5 Will any sub-contractors process personal data on behalf of the Organisation? If yes, identify them. | | |

---

## Section 10: trade compliance (for logistics suppliers)

*Complete this section only if you provide logistics, freight, customs, or supply chain services.*

| Question | Yes/No | Evidence / Comment |
|---|---|---|
| 10.1 Is your organisation a member of CTPAT? If yes, provide membership number and tier (Certified / Validated / Status). | | |
| 10.2 Does your organisation hold UK AEO-S certification? If yes, provide authorization number and HMRC reference. | | |
| 10.3 Does your organisation hold EU AEO certification? If yes, provide EORI number and certification reference. | | |
| 10.4 Does your organisation hold PIP certification? If yes, provide CBSA-assigned number. | | |
| 10.5 Does your organisation hold BASC certification? | | |
| 10.6 Does your organisation hold NEEC certification? | | |
| 10.7 Does your organisation hold OEA (Brazil) certification? | | |
| 10.8 Does your organisation adhere to the WCO SAFE Framework? | | |
| 10.9 Are your sub-contractors / freight agents required to maintain equivalent trade compliance programme memberships? | | |

---

## Section 11: AI systems

*Complete this section if you use or provide AI-enabled systems as part of your services.*

| Question | Yes/No | Evidence / Comment |
|---|---|---|
| 11.1 Does your service incorporate AI or machine learning systems? | | |
| 11.2 If yes, are AI systems subject to pre-deployment testing and bias assessment? | | |
| 11.3 Are AI system decisions explainable and auditable? | | |
| 11.4 Is your organisation subject to or preparing for EU AI Act obligations? | | |
| 11.5 Are any AI systems classified as High Risk under the EU AI Act? | | |

---

## Section 12: certifications and evidence attached

Please attach the following documents where applicable:

| Document | Attached | Not Applicable | Will Provide On Request |
|---|---|---|---|
| ISO 27001 certificate (current) | | | |
| SOC 2 Type II report (current: within 12 months) | | | |
| Penetration test attestation letter (within 12 months) | | | |
| ISO 27701 or privacy certification | | | |
| CTPAT membership confirmation | | | |
| UK AEO-S authorization confirmation | | | |
| EU AEO certificate | | | |
| PIP membership confirmation | | | |
| BASC certification | | | |
| Business Continuity test summary | | | |

---

## Declaration

I certify that the information provided in this questionnaire is accurate and complete to the best of my knowledge. I understand that material inaccuracies may result in disqualification or contract termination.

| Field | Value |
|---|---|
| Completed by (role title) | |
| Organisation | |
| Date | |
| Signature | |

---

**End of Document**
