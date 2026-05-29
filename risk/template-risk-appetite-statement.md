# Risk Appetite Statement Template

**Document Title:** Risk Appetite Statement Template\
**Document Type:** Template\
**Version:** 1.0.0\
**Date:** 2026-05-27\
**Owner:** Chief Risk Officer\
**Approving Authority:** Board of Directors\
**Related Documents:** [`risk/README.md`](README.md), [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md), [`risk/template-enterprise-risk-register.md`](template-enterprise-risk-register.md), [`risk/procedure-risk-acceptance.md`](procedure-risk-acceptance.md), [`risk/procedure-risk-assessment-methodology.md`](procedure-risk-assessment-methodology.md), [`risk/register-key-risk-indicators.md`](register-key-risk-indicators.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md)\
**Classification:** Public\
**Category:** Risk Management\
**Review Frequency:** Annual; and upon material strategic change, significant incident, or Board direction\
**Repository Path:** [`risk/template-risk-appetite-statement.md`](template-risk-appetite-statement.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## Purpose

This template defines the structure for the organisation's Risk Appetite Statement (RAS). The RAS translates the Board's strategic risk tolerance into measurable thresholds and qualitative statements that guide risk identification, assessment, treatment, and acceptance decisions across the enterprise.

---

## Part 1: overall risk philosophy

*Populate this section with a brief statement of the organisation's overall approach to risk-taking. This should reflect the Board's mandate.*

The organisation's risk philosophy acknowledges that risk-taking is inherent to delivering value and achieving strategic objectives. The Board accepts that some level of risk is unavoidable and distinguishes between risks it is willing to accept in pursuit of strategic goals and risks it is unwilling to accept under any circumstances.

The organisation pursues a **conservative to moderate** overall risk appetite: seeking competitive advantage through operational excellence, innovation, and supply chain performance, while maintaining rigorous controls over safety, compliance, data protection, and financial integrity.

---

## Part 2: risk appetite by category

For each risk category, the RAS defines:
- **Appetite Level:** None / Low / Moderate / High
- **Qualitative Statement:** Describes the organisation's willingness to accept risk in this category
- **Risk Tolerance Thresholds:** Quantitative boundaries within which residual risk must remain
- **Escalation Trigger:** Condition requiring Board or senior leadership attention

| Risk Category | Appetite Level | Qualitative Statement | Tolerance Threshold | Escalation Trigger |
|---|---|---|---|---|
| **Strategic** | Moderate | The organisation accepts measured strategic risk in pursuit of growth, market expansion, and operational transformation, provided risks are identified and actively managed. | No single strategic initiative should carry unmitigated exposure above *[High: define threshold]*. | Any strategic risk assessed as Critical residual; Board decision required. |
| **Operational** | Low | The organisation maintains low tolerance for disruptions to core logistics and supply chain operations. Operational risk must be actively mitigated to acceptable levels. | Maximum tolerable unplanned disruption to critical services: *[define hours/days]*. | Any P1 or P2 operational incident; escalate to executive leadership within *[define timeframe]*. |
| **Cybersecurity** | Low | The organisation has a low appetite for cybersecurity risk. Cyber threats that could compromise customer or operational data, logistics systems, or supply chain integrity must be mitigated to Low residual. | No unmitigated High or Critical cybersecurity residual risk to remain open for more than *[define days]*. | Any confirmed cyber breach; ransomware event; data exfiltration: escalate immediately. |
| **Privacy** | None to Low | The organisation has no appetite for privacy violations that result in harm to individuals, regulatory sanctions, or reputational damage. Personal data must be processed lawfully, fairly, and with appropriate safeguards. | Zero tolerance for confirmed data breaches involving special category data or data affecting children. | Any breach requiring regulatory notification (GDPR 72-hour threshold; PIPEDA); escalate immediately. |
| **AI** | Low to Moderate | The organisation accepts moderate risk in deploying AI systems for operational efficiency but maintains low appetite for AI-related harms including bias, opacity, or regulatory non-compliance. | No AI system deployed without completed pre-deployment testing; no high-risk AI deployed without DPA and risk acceptance. | Any AI system causing material harm, regulatory inquiry, or bias finding: escalate within *[define timeframe]*. |
| **Supplier** | Low to Moderate | The organisation accepts moderate supplier risk for non-critical relationships but requires active management of critical and sole-source supplier dependencies. | No critical supplier without an assessed Business Impact Analysis (BIA) and continuity plan. No single supplier representing more than *[define %]* of revenue without dual-source contingency. | Critical supplier insolvency or material non-performance; escalate within 24 hours. |
| **Resilience** | Low | The organisation maintains low tolerance for prolonged operational disruption. Recovery time and recovery point objectives must be met for all Tier 1 and Tier 2 systems. | Maximum tolerable data loss and recovery times as defined in [`resilience/plan-it-disaster-recovery.md`](../resilience/plan-it-disaster-recovery.md). | Any event requiring Business Continuity Plan activation; escalate to crisis management team immediately. |
| **Financial** | Low | The organisation has low appetite for financial risk arising from poor controls, fraud, or misreporting. Financial risk is managed within budget and treasury policies. | No unbudgeted financial exposure above *[define threshold]* without Board approval. | Any fraud investigation; material financial misstatement; escalate immediately. |
| **Legal and Regulatory** | None | The organisation has zero appetite for deliberate non-compliance with applicable laws and regulations. Technical breaches must be promptly identified and remediated. | Zero tolerance for knowing non-compliance with mandatory regulatory obligations. | Any confirmed regulatory breach or enforcement action; escalate immediately. |
| **Technology** | Low | The organisation has low tolerance for unplanned system outages affecting logistics, customs, or customer-facing services. Technology risk must be managed through rigorous lifecycle and change management. | Unplanned downtime of Tier 1 systems: maximum *[define hours]* before escalation. | Any Tier 1 system outage exceeding RTO; escalate within *[define timeframe]*. |
| **Human Capital** | Low to Moderate | The organisation accepts moderate risk in talent acquisition and retention in competitive markets, while maintaining low appetite for ethical violations, discrimination, or workplace safety breaches. | Zero tolerance for substantiated harassment, discrimination, or retaliation. Succession coverage target: *[define %]* of critical roles. | Any confirmed ethics violation; safety incident; escalate within 24 hours. |
| **Physical** | Low | The organisation has low tolerance for physical security breaches affecting cargo, facilities, or personnel. Physical risks must be mitigated through access controls, monitoring, and emergency response. | Any physical security breach must be reported and investigated within *[define hours]*. | Any facility breach; injury; criminal activity: escalate immediately. |

---

## Part 3: risk tolerance boundaries

The following quantitative boundaries define the outer limits of acceptable residual risk. Risks exceeding these boundaries require immediate escalation and treatment or formal acceptance by the Board.

| Boundary Type | Threshold | Applicable to |
|---|---|---|
| **Maximum residual risk score for open risks** | No risk rated Critical (score 17 to 25) to remain open without a Board-approved treatment plan for more than *[define days]* | All categories |
| **Maximum High risks without treatment plans** | No more than *[define number]* High-rated risks without active treatment plans | All categories |
| **Mandatory acceptance authority** | Residual risks rated High require CRO acceptance; Critical requires Board acceptance | All categories |
| **Financial loss tolerance** | Single incident: *[define]*: Aggregate annual: *[define]* | Financial; Operational; Cybersecurity |
| **Data records tolerance** | Zero records for which retention periods have been exceeded without documented justification | Privacy; Legal and Regulatory |

---

## Part 4: appetite vs. tolerance vs. capacity

| Term | Definition | Governance Use |
|---|---|---|
| **Risk Appetite** | Amount and type of risk the organisation is willing to accept in pursuit of objectives | Sets the target risk profile; informs strategy |
| **Risk Tolerance** | Acceptable variation around risk appetite thresholds: the boundary before escalation is required | Informs treatment decisions and acceptance authority |
| **Risk Capacity** | Maximum risk the organisation could absorb before it threatens survival or mission | Ultimate constraint; must never be exceeded |

---

## Part 5: changes to risk appetite

Risk appetite thresholds are reviewed annually as part of the Board's strategic planning cycle. Interim revisions may be triggered by:

- Material change in strategic direction
- Significant adverse incident
- Material regulatory change
- Merger, acquisition, or divestiture
- Board direction

All changes to the Risk Appetite Statement require Board approval before taking effect.

---

## Part 6: linkage to risk register

Risk owners must compare each risk's residual risk score against this statement when completing [`risk/template-enterprise-risk-register.md`](template-enterprise-risk-register.md). The field "Within Risk Appetite?" must be completed for every risk entry. Risks rated as outside appetite must have an active treatment plan or a formal acceptance record ([`risk/procedure-risk-acceptance.md`](procedure-risk-acceptance.md)).

---

## Approval and review record

| Version | Date | Approved By | Summary of Changes |
|---|---|---|---|
| 1.0.0 | | Board of Directors | Initial adoption |
| | | | |

---

**End of Document**
