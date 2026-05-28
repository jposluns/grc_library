# Quantitative Risk Analysis Guideline

**Document Title:** Quantitative Risk Analysis Guideline 
**Document Type:** Guideline 
**Version:** 1.0.1 
**Date:** 2026-05-28 
**Owner:** Chief Risk Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`risk/README.md`](README.md), [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md), [`risk/procedure-risk-assessment-methodology.md`](procedure-risk-assessment-methodology.md), [`risk/template-enterprise-risk-register.md`](template-enterprise-risk-register.md), [`risk/template-risk-appetite-statement.md`](template-risk-appetite-statement.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md) 
**Classification:** Public 
**Category:** Risk Management: Quantitative Analysis 
**Review Frequency:** Annual and upon material methodology update 
**Repository Path:** [`risk/guideline-quantitative-risk-analysis.md`](guideline-quantitative-risk-analysis.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This guideline provides voluntary guidance for applying quantitative risk analysis techniques alongside the qualitative 5×5 matrix approach defined in [`risk/procedure-risk-assessment-methodology.md`](procedure-risk-assessment-methodology.md). Quantitative methods complement qualitative scoring by expressing risk in financial terms, supporting capital allocation decisions, cyber insurance sizing, and Board-level risk reporting.

The primary methodology referenced is **FAIR (Factor Analysis of Information Risk)**, an open quantitative risk analysis standard. This guideline does not require formal FAIR tool adoption and can be applied manually for individual high-priority risk analyses.

---

## When to use quantitative analysis

Quantitative analysis is appropriate when:

- A risk is rated High or Critical in the qualitative register and investment decisions are required
- Comparing treatment options to determine cost-effectiveness (cost of control vs. annualized loss expectancy)
- Setting cyber insurance coverage limits or premiums
- Preparing risk disclosures for the Board, investors, or regulators
- Evaluating the financial impact of supply chain disruption scenarios
- Supporting go/no-go decisions on major technology or operational changes

Quantitative analysis is not required for Low or Medium risks unless specifically requested by the Chief Risk Officer or Board.

---

## FAIR model overview

FAIR decomposes risk into two primary factors:

```
Risk = Loss Event Frequency × Loss Magnitude
```

### Loss event frequency (LEF)

LEF estimates how often a loss event is expected to occur per year. It is derived from:

| Component | Definition |
|---|---|
| **Threat Event Frequency (TEF)** | How often a threat actor contacts the asset of interest |
| **Vulnerability (Vuln)** | Probability that the threat succeeds given contact |
| **Loss Event Frequency (LEF)** | TEF × Vuln = expected loss events per year |

### Loss magnitude (LM)

LM estimates the expected financial impact per loss event. It is composed of:

| Loss Form | Description | Examples |
|---|---|---|
| **Primary Loss** | Direct losses experienced by the organisation | Response costs; system recovery; downtime; data reconstruction |
| **Secondary Loss** | Downstream losses from secondary stakeholders | Regulatory fines; litigation; customer compensation; reputational damage |

#### Primary loss components

| Component | Definition |
|---|---|
| **Productivity loss** | Revenue or operational value lost during disruption |
| **Response costs** | Incident response, forensics, containment, remediation |
| **Replacement costs** | Hardware, software, or data restoration costs |
| **Competitive advantage loss** | Loss of intellectual property or market position |

#### Secondary loss components

| Component | Definition |
|---|---|
| **Regulatory fines and penalties** | Fines from regulators (e.g., ICO, CNIL, CBP) for non-compliance |
| **Litigation costs** | Legal defence, settlements, judgements |
| **Reputation damage** | Customer attrition, brand remediation, PR costs |
| **Contract penalties** | SLA breach penalties; customer contract terminations |

---

## Estimating ranges (monte carlo approach)

Rather than single-point estimates, FAIR uses probabilistic ranges. For each factor, estimate:

- **Minimum (Low):** Value in the lowest 5th percentile of outcomes
- **Most Likely (ML):** Most probable single value
- **Maximum (High):** Value in the 95th percentile of outcomes

These three values define a PERT distribution suitable for Monte Carlo simulation.

### Simplified manual estimation

For teams without simulation tools, use the following approximation:

```
Expected Value = (Min + 4 × Most Likely + Max) / 6
```

---

## Step-by-step quantitative analysis process

### Step 1: Define the risk scenario
Start from a qualitatively identified risk in the enterprise risk register. Define:
- Asset at risk (system, data set, service, revenue stream)
- Threat actor (internal, external, environmental)
- Threat type (malicious attack, error, natural event)
- Effect (confidentiality breach, availability loss, integrity compromise)

### Step 2: Estimate loss event frequency

| Sub-Step | Action |
|---|---|
| 2a | Estimate Threat Event Frequency (TEF) per year (range: min, ML, max) |
| 2b | Estimate Vulnerability: probability threat succeeds per contact (0 to 1, as %) |
| 2c | Calculate LEF range = TEF × Vulnerability |

**Example: Ransomware scenario:**
- TEF: 2 to 12 targeted attempts per year (ML: 6)
- Vulnerability: 2% to 15% (ML: 6%)
- LEF: 0.04 to 1.8 events per year (ML: 0.36)

### Step 3: Estimate primary loss magnitude

| Sub-Step | Action |
|---|---|
| 3a | Estimate productivity loss (hourly revenue × estimated hours of disruption) |
| 3b | Estimate response and recovery costs |
| 3c | Estimate replacement and remediation costs |
| 3d | Sum primary loss components for min, ML, max |

**Example: Ransomware primary loss:**
- Productivity: 48 to 240 hours disruption × hourly revenue
- Response costs: external IR retainer; forensics team; media specialist
- Recovery costs: system rebuild; data restoration from backup
- Primary loss range: *[example figures to be populated with organisational data]*

### Step 4: Estimate secondary loss magnitude

| Sub-Step | Action |
|---|---|
| 4a | Identify applicable secondary loss forms (regulatory, litigation, reputation) |
| 4b | Estimate probability and magnitude of each secondary loss |
| 4c | Apply secondary loss probability to magnitude for expected secondary loss |

**Example: Ransomware secondary loss:**
- Regulatory fines: If personal data affected: GDPR up to 4% global turnover; UK ICO discretionary fine
- Litigation: Class action probability × settlement estimate
- Reputation: Customer attrition rate × customer lifetime value

### Step 5: Calculate annualized loss expectancy (ALE)

```
ALE = LEF × (Primary Loss Magnitude + Secondary Loss Magnitude)
```

ALE represents the expected annual financial cost of the risk scenario.

### Step 6: Evaluate treatment options

For each proposed treatment:
1. Re-estimate LEF or LM with the control in place (post-control scenario)
2. Calculate post-control ALE
3. Compute **Risk Reduction Value = Pre-control ALE − Post-control ALE**
4. Compare Risk Reduction Value against cost of implementing and maintaining the control
5. Controls where Cost < Risk Reduction Value are economically justified

### Step 7: Document and report

| Output | Content |
|---|---|
| Risk analysis summary | Scenario description, assumptions, estimates, ALE calculation |
| Sensitivity analysis | Which inputs most influence the result |
| Control recommendations | Economically justified controls; prioritization |
| Confidence level | Statement on data quality and estimation uncertainty |

---

## Data sources for estimation

| Source Type | Examples |
|---|---|
| **Internal incident history** | Past breach or disruption costs; incident response records |
| **Industry benchmarks** | Verizon DBIR; IBM Cost of a Data Breach Report; Ponemon Institute studies |
| **Regulatory guidance** | GDPR fine precedents; ICO published penalty decisions; CBP enforcement history |
| **Actuarial data** | Cyber insurance loss experience; industry loss distributions |
| **Expert elicitation** | Structured interviews with technical experts for TEF and Vulnerability estimates |

---

## Cyber insurance integration

Quantitative risk analysis outputs directly support cyber insurance procurement:

| Insurance Decision | Quantitative Input |
|---|---|
| Coverage limit selection | Maximum credible loss (95th percentile of LM distribution) |
| Deductible selection | Expected primary loss for most likely scenarios |
| Premium benchmarking | Compare premium to ALE for covered scenarios |
| Coverage gap analysis | Compare policy exclusions against identified loss forms |

---

## Limitations

Quantitative analysis is only as reliable as its inputs. Practitioners should:

- Document all assumptions explicitly
- Express results as ranges, not single-point estimates
- Acknowledge where data is sparse and estimation uncertainty is high
- Avoid false precision: a range of $1M to $10M is more honest than $4.7M
- Review and update estimates as new internal and external data becomes available

---

**End of Document**
