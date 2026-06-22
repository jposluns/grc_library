# Security Operations Centre Operating Model Standard

**Document Title:** Security Operations Centre Operating Model Standard\
**Document Type:** Standard\
**Version:** 1.0.2\
**Date:** 2026-06-22\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/standard-logging-and-monitoring.md`](standard-logging-and-monitoring.md), [`security/procedure-security-incident-response.md`](procedure-security-incident-response.md), [`security/sop-incident-escalation-matrix.md`](sop-incident-escalation-matrix.md), [`security/sop-security-ticket-reporting-scheme.md`](sop-security-ticket-reporting-scheme.md), [`operations/procedure-security-monitoring-and-alert-management.md`](../operations/procedure-security-monitoring-and-alert-management.md), [`operations/procedure-threat-intelligence-and-siem-operations.md`](../operations/procedure-threat-intelligence-and-siem-operations.md), [`security/standard-penetration-testing-and-red-team.md`](standard-penetration-testing-and-red-team.md), [`resilience/procedure-cross-domain-incident-coordination.md`](../resilience/procedure-cross-domain-incident-coordination.md), [`ai/plan-ai-incident-response.md`](../ai/plan-ai-incident-response.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material change to capability tier, supplier model, or detection portfolio\
**Repository Path:** [`security/standard-soc-operating-model.md`](standard-soc-operating-model.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This standard defines the operating model for the security operations centre (SOC). It covers capability tiers, staffing model, tool stack, coverage hours, detection engineering, threat hunting, intelligence integration, on-call governance, shift handover, MTTD and MTTR targets, and the supplier-managed-SOC model where one is used.

---

## Scope

This standard applies to the team or function (internal, hybrid, or supplier-managed) that performs security monitoring, alert triage, incident response coordination, threat hunting, and security telemetry engineering. It does not duplicate the security incident response procedure or the logging and monitoring standard; it defines the operating model that runs them.

---

## Section 1: capability tiers

The SOC operates a tiered capability model. Adopting organisations select the tier appropriate to their risk appetite, complexity, and budget; the standard defines what each tier minimally provides.

| Capability tier | Description | Suitable for |
| --- | --- | --- |
| Tier A: Basic | Business-hour monitoring; alert triage; escalation to engineering; supplier-managed-SOC option for 24/7 watch | Small or low-risk organisations |
| Tier B: Operational | 24/7 watch; in-house triage; defined escalation; detection engineering capacity; basic threat intelligence | Mid-sized organisations or regulated industries |
| Tier C: Advanced | 24/7 watch; tiered analysts; detection engineering team; active threat hunting; intelligence-driven operations; metrics-driven optimisation | Large or high-risk organisations |
| Tier D: Mature | Tier C plus deception operations; purple teaming; embedded incident response capability; threat-actor-specific hunting; intelligence sharing partnerships | High-target organisations |

Adopting organisations document the current tier and the target tier in the security architecture roadmap.

---

## Section 2: staffing model

| Role | Responsibilities |
| --- | --- |
| SOC Manager | Operational leadership; shift governance; SLA accountability; supplier relationship if hybrid |
| SOC Analyst (Tier 1) | Initial triage; alert validation; routine investigation; documented response per playbook |
| SOC Analyst (Tier 2) | Deep investigation; correlation across alerts; incident commander for P3 and P4 |
| SOC Analyst (Tier 3) or Senior Incident Responder | Complex investigation; incident commander for P1 and P2; forensic work; co-ordination with external IR partner |
| Detection Engineer | Detection content authoring, tuning, lifecycle; metric ownership |
| Threat Intelligence Analyst | Intelligence collection, analysis, dissemination; sector and threat-actor tracking |
| Threat Hunter | Hypothesis-driven hunting; produces detection content from findings |
| SOC Architect or Engineer | SIEM, EDR, SOAR, and adjacent tool engineering; data pipeline integrity |
| On-call rota | Out-of-hours coverage where the SOC is not 24/7 in-house |

Smaller SOCs combine roles. Larger SOCs additionally include red team, purple team, and embedded data-engineering capacity.

---

## Section 3: tool stack

| Capability | Tool category |
| --- | --- |
| Log centralisation | SIEM or log lake with searchable retention |
| Endpoint detection | EDR with response capabilities |
| Network detection | NDR or equivalent (NetFlow, packet capture for targeted use) |
| Identity threat detection | ITDR or equivalent integrated with the identity provider |
| Cloud detection | CDR or cloud-platform-native detection coverage |
| Email security | Per the email security standard |
| Vulnerability data | Vulnerability management platform feeding detection content |
| Threat intelligence platform | Indicator and intelligence lifecycle management |
| SOAR | Automated response orchestration; runbook automation |
| Case management | Single source of truth for alerts, incidents, evidence |
| Forensic and DFIR tooling | Disk and memory forensics; cloud and SaaS forensic readiness |
| Sandboxing | Per the email security standard |
| Asset and identity context | Authoritative inventory feeds for enrichment |
| AI-aware detection content | Per the AI incident response plan |

Tools support open standards (STIX, TAXII, SCAP, OpenC2, MITRE ATT&CK mapping). Vendor lock-in is documented in the supplier risk register.

---

## Section 4: coverage hours

| Posture | Description | Use case |
| --- | --- | --- |
| Business hours only | SOC active during local business hours; automated alerting and on-call rota for out-of-hours | Tier A with low-criticality service |
| Extended business hours | Two shifts covering 12 to 16 hours per day | Some Tier B |
| Follow-the-sun | Coverage across multiple regional shifts | Tier B and Tier C with global operations |
| 24/7/365 | Continuous coverage with dedicated shift teams | Tier B regulated; Tier C; Tier D |

Where supplier-managed-SOC provides out-of-hours coverage, the contract specifies the handover protocol with the in-house team at shift change.

---

## Section 5: detection engineering

| Practice | Requirement |
| --- | --- |
| Detection-as-code | Detection content version-controlled, peer-reviewed, and deployed through a pipeline |
| Use-case management | Each detection mapped to a documented use case with the threat it addresses |
| MITRE ATT&CK coverage | Per-technique coverage tracked; gaps identified and prioritized |
| Tuning loop | False-positive rate per rule tracked; tuning planned and recorded |
| Decommissioning | Rules retired when the threat no longer applies or the rule is replaced |
| Quality gate | New rules tested in shadow mode before production; performance and false-positive ceiling applied |
| Documentation | Each rule documents intent, expected signal, expected triage steps, escalation criteria |
| AI-aware content | Detection content for AI-specific incident classes per the AI incident response plan |

---

## Section 6: threat hunting

| Practice | Requirement |
| --- | --- |
| Hypothesis-driven hunting | Hunts start from a hypothesis grounded in intelligence, prior incidents, or environment changes |
| Documented hunts | Hunt scope, hypothesis, queries, findings, and outcomes recorded |
| Detection output | Successful hunts produce detection content where the pattern is durable |
| Frequency | Cadence per tier (e.g. weekly for Tier C; monthly for Tier B) |
| Purple teaming | Coordination between hunts and red team to validate detection coverage |

---

## Section 7: intelligence integration

| Practice | Requirement |
| --- | --- |
| Intelligence sources | Combination of commercial feeds, open-source intelligence, industry sharing groups, and government advisories where the organisation is eligible |
| Sector and geographic tracking | Coverage matched to the organisation's sector and operating geographies |
| Threat actor tracking | Specific actors relevant to the organisation are tracked |
| Indicator lifecycle | Indicators ingested with provenance, confidence, and expiry |
| Strategic intelligence | Quarterly strategic intelligence briefing to the Executive Sponsor and the AI Governance Council |
| Information sharing | Per the threat intelligence and SIEM operations procedure |

---

## Section 8: on-call and shift governance

| Practice | Requirement |
| --- | --- |
| On-call rota | Documented schedule with primary and secondary on-call |
| Handover at shift change | Structured handover covering active incidents, pending investigations, environmental anomalies, intelligence highlights |
| Escalation contacts | Up-to-date roster including IR partner, supplier-managed-SOC, executive sponsor |
| Out-of-hours capability | Documented authority for out-of-hours decisions; clear thresholds for waking the executive sponsor |
| Tooling availability | All SOC tools accessible from on-call paths; no single point of access dependency |
| Fatigue management | Maximum hours per shift; minimum rest between shifts; rotation policy |

---

## Section 9: metrics and SLAs

| Metric | Definition | Target by tier |
| --- | --- | --- |
| Mean time to detect (MTTD) | Time from incident onset to first SOC awareness | Tier A: best effort; Tier B: under 4 hours for P1/P2; Tier C: under 1 hour for P1/P2 |
| Mean time to triage (MTTT) | Time from alert ingestion to triage decision | Tier B: under 30 minutes for P1; Tier C: under 15 minutes |
| Mean time to contain (MTTC) | Time from declaration to confirmed containment | Per the security incident response procedure |
| Mean time to recover (MTTR) | Time from declaration to full service | Per the resilience programme |
| Alert volume per analyst | Daily volume per role | Trend-monitored; persistent above-baseline triggers tuning or staffing review |
| False-positive rate | Per-rule and aggregate | Trend-monitored; per-rule threshold per tuning policy |
| Detection coverage against ATT&CK | Per-technique coverage | Tier C and above: at least 70% of relevant techniques |
| Hunt-to-detection conversion | Percentage of hunts producing detection content | Tier C: at least 30%; Tier D: at least 50% |
| Burnout indicators | Sick leave; turnover; satisfaction survey | Reviewed quarterly |
| Intelligence-feed actionability | Percentage of feed indicators producing useful detection or response | Reviewed quarterly per feed; low-actionability feeds reviewed for retention |

---

## Section 10: supplier-managed-SOC

Where the SOC is supplier-managed in whole or in part:

| Item | Requirement |
| --- | --- |
| Contract | Per the supplier security and privacy assurance standard with additional clauses specific to SOC operations |
| Tenancy | Customer data segregated from other supplier customers; documented isolation |
| Data residency | Telemetry and case data location aligned to the organisation's data-residency requirements |
| Custodianship | Evidence chain of custody preserved across the supplier and organisation boundary |
| Transparency | Defined access to the supplier's analyst notes and case timeline |
| Concentration | The supplier-managed-SOC included in the concentration risk register |
| Exit | Exit strategy documented; case data and detection content portable on exit |
| Performance reporting | Per the supplier resilience monitoring standard and per SOC metrics above |

---

## Section 11: continuous improvement

| Practice | Cadence |
| --- | --- |
| Post-incident review feeds | Every P1 and P2 PIR produces an action item routed into detection, tooling, or training |
| Quarterly capability assessment | Per-pillar score against the maturity ladder |
| Annual SOC strategy review | Roadmap update including target tier, tool stack, staffing model |
| Tabletop and exercise programme | Per the resilience programme |
| Red team and purple team | Per the penetration testing standard |
| External assessment | Independent SOC maturity assessment at minimum every two years for Tier C and above |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| NIST CSF 2.0 | DETECT, RESPOND | Functional alignment |
| NIST SP 800-61 Rev. 3 | Incident Response Recommendations and Considerations for Cybersecurity Risk Management (CSF 2.0 Community Profile) | Incident handling |
| NIST SP 800-150 | Guide to Cyber Threat Information Sharing | Intelligence operations |
| NIST SP 800-92 | Guide to Computer Security Log Management | Logging baseline |
| ISO/IEC 27001:2022 | A.5.7, A.5.24 to A.5.28, A.8.15 to A.8.16 | Threat intelligence, incident management, logging |
| ISO/IEC 27035 series | Information security incident management | Lifecycle baseline |
| MITRE ATT&CK | Adversarial tactics and techniques | Coverage framework |
| MITRE D3FEND | Defensive countermeasures | Defensive framework |
| SOC-CMM | Security Operations Centre Capability Maturity Model | Independent maturity model reference |
| FIRST CSIRT Services Framework | FIRST | CSIRT capability model |

---

## Limitations

This standard is a CC BY-SA 4.0 baseline. SOC operations are highly variable across organisations and across maturity tiers. Adopting organisations select the appropriate tier and adapt the staffing, tooling, and SLA targets to their risk profile and budget. The standard is not a SOC-platform mandate; it expresses operating-model requirements rather than product-specific configuration.

---

**End of Document**
