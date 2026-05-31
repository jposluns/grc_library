# Insider Risk Programme Framework

**Document Title:** Insider Risk Programme Framework\
**Document Type:** Framework\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/policy-acceptable-use.md`](policy-acceptable-use.md), [`security/standard-personnel-security-screening.md`](standard-personnel-security-screening.md), [`security/standard-data-loss-prevention.md`](standard-data-loss-prevention.md), [`security/standard-logging-and-monitoring.md`](standard-logging-and-monitoring.md), [`security/standard-privileged-access-management.md`](standard-privileged-access-management.md), [`security/procedure-security-disciplinary-process.md`](procedure-security-disciplinary-process.md), [`security/procedure-onboarding-and-offboarding.md`](procedure-onboarding-and-offboarding.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`governance/framework-human-capital-and-ethical-conduct.md`](../governance/framework-human-capital-and-ethical-conduct.md), [`governance/procedure-whistleblower-and-incident-reporting.md`](../governance/procedure-whistleblower-and-incident-reporting.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material change to workforce, regulator-expected posture, or threat-actor pattern\
**Repository Path:** [`security/framework-insider-risk-programme.md`](framework-insider-risk-programme.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This framework defines the organisation's approach to insider risk: the risk that current or former employees, contractors, or trusted third parties act in ways (intentional or unintentional) that harm the organisation. It establishes the programme objectives, the governance model, the detection and response capabilities, the privacy and due-process safeguards, and the coordination with HR, Legal, Privacy, and Internal Audit.

This framework is one of the highest-risk programmes to operate poorly. It is published as a controlled framework precisely to make the safeguards explicit.

---

## Scope

This framework applies to:

1. **Employees** in all roles, all locations, all employment types.
2. **Contractors and consultants** with access to organisation systems or data.
3. **Vendors and partners** with elevated trust including those with privileged access or sensitive-data exposure.
4. **Departing personnel** during the notice period and offboarding window.
5. **Former personnel** where retained access (alumni accounts, contractor return engagements) creates ongoing exposure.

It does not apply to general personnel monitoring outside the security context; routine HR and performance management are outside scope.

---

## Programme objectives

| Objective | Description |
| --- | --- |
| Prevent | Reduce the likelihood of insider events through proportional pre-employment screening, awareness, access discipline, and culture |
| Detect | Identify insider events early through signal correlation and behaviour analysis |
| Respond | Investigate and respond proportionally with due process, evidentiary discipline, and privacy safeguards |
| Learn | Feed lessons into culture, training, and control updates |
| Protect personnel | Safeguard personnel against false-positive accusation; preserve dignity and due process |

---

## Insider risk categories

The framework recognises distinct risk profiles requiring different controls and responses.

| Category | Description | Typical signals |
| --- | --- | --- |
| Unintentional | Mistakes, misconfiguration, accidental disclosure, falling for phishing | Repeated DLP triggers; misaddressed mail; accidental commits |
| Negligent | Knowing departure from policy without malicious intent (e.g. taking work home on a personal drive for convenience) | Policy violation patterns; unsanctioned tooling |
| Compromised | The insider is acting under external compromise (account takeover, coercion, social engineering) | Anomalous access patterns; impossible travel; behaviour change |
| Malicious | Deliberate harm, theft, sabotage, fraud, espionage | Targeted exfiltration patterns; access escalation outside need; coordination signals |
| Departing | Higher-risk window from notice through offboarding | Bulk downloads; resignation timing patterns; access to data outside current role |

---

## Governance model

| Body or role | Responsibility |
| --- | --- |
| Insider Risk Steering Committee | Quarterly governance; reviews aggregate trends, programme performance, and significant cases; comprises CISO, Chief Privacy Officer, Chief HR Officer or equivalent, Legal Counsel, Chief Compliance Officer, Internal Audit Lead |
| Insider Risk Programme Lead | Operational ownership; reports to the CISO |
| Insider Risk Analyst | Investigates referred signals; coordinates with HR, Legal, Privacy |
| HR Lead | Owns employment-side coordination; manages due-process discipline; coordinates with line management |
| Privacy Officer | Reviews programme controls for lawful basis, proportionality, and subject rights |
| Legal Counsel | Advises on disciplinary, evidentiary, and litigation matters; reviews surveillance posture |
| Internal Audit | Independent assurance over the programme's controls including over-collection, false-positive handling, and personnel-protection safeguards |
| Whistleblower Reporting Lead | Coordinates with the insider risk programme on referrals where appropriate |

---

## Pillars

### Pillar 1: prevention

| Control area | Requirement |
| --- | --- |
| Pre-employment screening | Per the personnel security screening standard; depth proportionate to role risk |
| Joiner orientation | Acceptable use policy, code of conduct, data handling, insider-risk awareness |
| Periodic awareness | Annual refresher; role-targeted content for high-risk roles |
| Culture of reporting | Visible whistleblower path; psychologically safe escalation |
| Access discipline | Least privilege per IAM standards; recertification cadence |
| Privileged access management | Per the PAM standard; just-in-time access for highest-sensitivity actions |
| Data classification awareness | Per the data classification and handling standard |
| Departure protocols | Heightened controls during the notice period for departing personnel |

### Pillar 2: detection

| Detection input | Source |
| --- | --- |
| Data loss prevention signals | Per the DLP standard |
| Identity and access anomalies | Per the IAM standard and ITDR coverage |
| Endpoint behaviour signals | EDR-derived behavioural signals |
| Cloud and SaaS posture signals | SSPM and cloud-native detection |
| Code repository signals | Anomalous clone, download, or commit patterns |
| Email signals | Bulk forwarding to external addresses; sensitive content patterns |
| Print and removable-media signals | Where the environment uses controlled print and USB |
| Badge and physical-access signals | Where badge data is available and proportionate |
| HR signals (in defined scopes only) | Employment-status change; notice period; documented performance escalation, only with HR's controlled handoff |
| Triggered review based on whistleblower or peer report | Per the whistleblower procedure |

Detection content is risk-tuned and scoped: not every signal is investigated by the insider risk team. False-positive ceilings apply per the SOC standard.

### Pillar 3: response

| Stage | Required action |
| --- | --- |
| Referral | Signal arrives from detection or whistleblower channel; case opened by the Insider Risk Analyst |
| Validation | Confirm the signal is not a false positive before escalating; consult HR if employment context is needed |
| Joint review | The Insider Risk Steering Committee or its delegated subgroup reviews material cases before action |
| Investigation | Per documented investigation procedure with evidence handling; privileged where Legal designates |
| Containment | Targeted access restriction proportionate to the threat; full access revocation only when the case warrants it |
| Disciplinary process | Per the security disciplinary process procedure; HR-led |
| Law enforcement engagement | Per Legal Counsel where statutorily required or risk-justified |
| Closure | Documented closure including evidence retention, lessons learned, and any control updates |

### Pillar 4: learning

| Activity | Cadence |
| --- | --- |
| Quarterly aggregate trend report | To the Insider Risk Steering Committee; redacted of identifying information |
| Detection content refresh | Quarterly |
| Awareness content refresh | Annually and after material learning |
| Procedure update | After significant cases |
| Annual programme review | External or independent review at minimum every two years |

---

## Privacy and due-process safeguards

The framework requires the following safeguards on every detection capability and every investigation.

| Safeguard | Requirement |
| --- | --- |
| Lawful basis | The Privacy Officer documents the lawful basis for each detection capability per applicable privacy law; for personal data processed under legitimate interest, a balancing test is documented |
| Proportionality | Each detection capability collects the minimum data necessary; mass surveillance is prohibited |
| Notice | Personnel are informed of the existence of the programme and of the broad categories of monitoring in the privacy notice and the acceptable use policy; specific detection content is not disclosed |
| Purpose limitation | Data collected for insider risk is not used for performance management, marketing, or other purposes |
| Retention | Insider-risk data retained only for the period necessary for the investigation plus the documented limitation period |
| Access | Access to insider-risk data is restricted to the named programme team; privileged access logged and reviewed |
| Anti-bias safeguards | Detection content reviewed for adverse impact on protected groups; statistical bias monitoring conducted |
| False-positive handling | False positives logged; personnel falsely flagged informed where the false positive surfaced into HR or disciplinary process; programme corrective action |
| Due process in discipline | Per the security disciplinary process procedure; representation and appeal rights upheld |
| Cross-jurisdiction | Programme operates within the strictest applicable employment, privacy, and consultation rules across the organisation's footprint, including works councils and trade unions where applicable |
| Independent oversight | Internal Audit reviews the programme at minimum annually against these safeguards |

---

## Out-of-scope deliberate exclusions

The framework deliberately does not include:

1. **Content surveillance for content's sake.** Inspection of personal communications, browsing history outside security-relevant contexts, or other intrusive monitoring not justified by a specific signal.
2. **Predictive behaviour scoring.** Algorithmic ranking of personnel by predicted risk of malicious behaviour absent a triggering signal.
3. **Pre-emptive disciplinary action.** Sanctions before a finding of fact under a documented investigation.
4. **Monitoring outside working systems.** Personal devices, personal accounts, and personal premises are out of scope.
5. **Coercive or covert techniques.** Covert recording, social engineering of personnel, and other techniques are prohibited.

---

## Coordination with adjacent programmes

| Adjacent | Coordination point |
| --- | --- |
| Whistleblower programme | Bidirectional referral path with documented separation of evidence chains |
| HR performance management | Strict separation; HR data flows only on documented handoff |
| Privacy programme | Joint review at design and at material change |
| Legal | Engaged at every material case; ongoing advice on lawful posture |
| Internal Audit | Independent assurance over programme integrity |
| Security incident response | Compromised-insider cases route into the IR procedure |
| Privacy breach response | Insider-driven personal data breaches route to the privacy breach procedure |
| Cross-domain incident coordination | Multi-domain insider events convene the Joint Command |

---

## Metrics

| Metric | Definition | Target |
| --- | --- | --- |
| Cases opened | Per quarter | Trend-monitored |
| Cases closed with action | Per quarter | Trend-monitored |
| False-positive rate | Cases closed with no finding of impropriety | Trend-monitored; high rate triggers detection-content review |
| Median time to triage | From signal to validation decision | At most 5 business days |
| Median time to closure | From open to documented closure | Defined per case complexity |
| Disciplinary process adherence | Percentage of cases following the documented disciplinary process end to end | 100% |
| Privacy and proportionality findings from Internal Audit | Open audit findings against programme safeguards | Zero open above Low severity |
| Personnel awareness of the programme | Annual survey | At least 80% awareness |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27001:2022 | A.6.1 to A.6.5 (people controls); A.8.2 to A.8.5 | People and access controls |
| ISO/IEC 27002:2022 | Same plus implementation guidance | Implementation |
| NIST SP 800-53 Rev 5 | PS family; AT family | Personnel security and awareness |
| CERT Insider Threat Center | Carnegie Mellon | Insider risk research |
| NITTF | National Insider Threat Task Force | US federal model |
| GDPR / UK GDPR | Articles 5, 6, 13, 14, 22, 88 | Lawful basis, transparency, ADM, employment context |
| ILO Conventions on the right to privacy in employment | International | Worker protections |
| Local works council and trade union law | Per jurisdiction | Consultation and codetermination |

---

## Limitations

This framework is a CC BY-SA 4.0 baseline. Insider risk programmes are operationally and culturally sensitive; the controls and the safeguards are equally important. Adopting organisations consult specialist HR, employment-law, and privacy counsel at every material decision and engage workforce representation where it exists. The framework is not a substitute for that engagement.

---

**End of Document**
