# Maturity Assessment Methodology Standard

**Document Title:** Maturity Assessment Methodology Standard\
**Document Type:** Standard\
**Version:** 1.0.0\
**Date:** 2026-07-06\
**Owner:** GRC Programme Manager\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/framework-governance-performance-and-improvement.md`](framework-governance-performance-and-improvement.md), [`docs/template-maturity-self-assessment.md`](../docs/template-maturity-self-assessment.md), [`governance/register-digital-trust-and-assurance-metrics.md`](register-digital-trust-and-assurance-metrics.md), [`governance/framework-continuous-assurance-and-improvement.md`](framework-continuous-assurance-and-improvement.md), [`docs/maturity-scorecard.md`](../docs/maturity-scorecard.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual, or upon material change to the maturity model or assessment methodology\
**Repository Path:** [`governance/standard-maturity-assessment-methodology.md`](standard-maturity-assessment-methodology.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines the methodology for assessing governance programme maturity across the library's domains. It documents four things that the corpus previously applied without a single authoritative reference:

1. The five-tier maturity ladder.
2. The median-of-medians aggregation that produces per-domain and overall programme tiers.
3. The limitation of that aggregation: a single critically-weak domain does not move the aggregate tier.
4. The compensating floor-check that surfaces such a domain regardless of the aggregate tier.

It is the authoritative methodology reference behind the maturity-assessment section of the [`Governance Performance and Improvement Framework`](framework-governance-performance-and-improvement.md) and the [`Adopter Maturity Self-Assessment Template`](../docs/template-maturity-self-assessment.md). Those documents apply the ladder in context; this standard states the method, its limitation, and the compensating control in one place.

---

## 2. Scope

1. Applies to programme-maturity assessment across all governance domains: governance, risk, compliance, privacy, security, operations, resilience, supply chain, architecture, developer security, and AI.
2. Covers the maturity ladder, the aggregation method, its outlier-masking limitation, and the compensating floor-check.
3. Governs **programme maturity** (how mature an organization's use of the governance programme is), not **document maturity** (the stability classification the generated scorecard assigns each library document). The two are distinguished in section 8.
4. Documents the existing maturity-level model. It does not introduce process capability levels, which are a distinct model (section 9).

---

## 3. Governance and accountability

| Role | Responsibility |
| --- | --- |
| **GRC Programme Manager** | Owns this methodology; coordinates the annual maturity assessment; consolidates the per-domain scores into the overall programme tier; maintains the aggregation rule and the floor-check. |
| **Domain Owners** | Score their own domains against the ladder and supply the evidence supporting each tier. |
| **Assessor (internal or external)** | Conducts the assessment, applies the aggregation in section 5, runs the floor-check in section 7, and records the lowest domain and per-question scores. |
| **Internal Audit** | Independently validates the assessment basis and the reliability of the scores and their evidence. |
| **Enterprise Risk Committee (ERC)** | Reviews the maturity outcomes and the floor-check exceptions, and approves the resulting improvement roadmap. |

---

## 4. The maturity ladder

The ladder follows the CMMI maturity-level model: five tiers from Initial to Optimized. A programme is rated against the ladder per domain and overall.

| Tier | Name | Definition |
| --- | --- | --- |
| 1 | Initial | Processes are ad hoc and undocumented, dependent on individual knowledge; activity is reactive and incident-driven. |
| 2 | Managed | Processes are repeatable and tracked, with basic metrics defined; ownership is assigned for the core activities. |
| 3 | Defined | Processes are standardized and documented for organization-wide consistency; a documented review cadence is applied. |
| 4 | Quantitatively Managed | Processes are measured against quantitative objectives, with statistical controls applied; adjustments are driven by data rather than opinion. |
| 5 | Optimized | A continuous-improvement loop is in place; measured trends drive incremental and innovative change. |

A programme can sit at different tiers per domain: a heavily-regulated domain often matures faster than one under less external pressure. The overall tier (section 5) summarizes the per-domain tiers; it does not replace them.

The same five tier names anchor the maturity-assessment section of the Governance Performance and Improvement Framework (in governance-domain terms) and the Adopter Maturity Self-Assessment Template (in adopter-artefact terms). This standard states the canonical ladder that both apply.

---

## 5. Aggregation methodology (median-of-medians)

The assessment aggregates individual scores into tiers in two steps:

1. **Per-domain tier:** the median of that domain's per-question tiers.
2. **Overall programme tier:** the median of the per-domain scores.

The median, not the mean, is used at both steps. The median resists distortion by a single outlying score: one spurious low score does not drag a domain down, and one spurious high score does not inflate it. This robustness is the reason the method is used, and it is also the source of the limitation documented in section 6.

The aggregation produces a tier value (an integer, or a half-value where an even count of scores straddles two adjacent tiers). This standard documents the method; it does not change the mechanics the template records step by step, and it is independent of the generated document-maturity scoring (section 8).

---

## 6. The outlier-masking limitation

The property that makes the median robust to a single outlier is also its limitation at the aggregate level: **a single critically-weak domain does not move the overall median.** If ten domains score Tier 4 and one scores Tier 1, the overall median is 4, and the Tier-1 domain, which may be the highest-risk gap in the programme, does not change the headline tier. The same masking applies within a domain: a single Tier-1 question among Tier-4 questions does not move the domain median.

The aggregate tier can therefore overstate programme health when one domain, or one control area, is severely deficient. This is inherent to median aggregation; it is not a defect to be corrected in the computation. It is compensated by the floor-check in section 7, which reports the weak point alongside the aggregate rather than altering how the aggregate is computed.

---

## 7. The compensating floor-check

After computing the median-based per-domain and overall tiers, the assessor also records:

- the lowest per-domain score across all domains, and
- the lowest per-question score within each domain.

The assessor then surfaces, alongside the aggregate tier and regardless of the overall median:

1. **Absolute floor:** any domain or question at Tier 1 (Initial).
2. **Relative floor:** any domain scoring two or more tiers below the overall programme tier.

Either condition raises a floor-check exception. In the worked example of section 6 (one Tier-1 domain among Tier-4 domains), the absolute floor catches the Tier-1 domain, and the relative floor also catches it (four minus one is three, at or beyond the two-tier gap), so the masked weakness is visible next to the aggregate.

The floor tier and the relative gap are the proposed defaults; an organization sets them to its own risk appetite and exposure weighting. A high-exposure domain warrants a stricter floor than a low-exposure one: a Tier-1 score in a high-exposure domain is more urgent than a Tier-2 score in a low-exposure domain.

The floor-check is an assessor step, not a change to the median computation. The median-based tiers are reported as computed, and the floor-check exceptions are reported alongside them, so a masked critical weakness appears next to the headline tier rather than being buried by it. A floor-check exception feeds the improvement roadmap, and, where the exposure warrants, the risk register.

---

## 8. Programme maturity, document maturity, and other maturity surfaces

The library uses the word "maturity" for more than one thing. This standard governs the first of the following only; the distinction matters because the two are scored differently and mean different things.

- **Programme maturity (this standard).** How mature an organization's use of the governance programme is, scored on the five-tier ladder and aggregated by median-of-medians. It is consumed by the framework's maturity-assessment section and the adopter template.
- **Document maturity (not this standard).** The stability classification (Mature, Baseline, Draft) that the generated [`Document Maturity Scorecard`](../docs/maturity-scorecard.md) assigns to each library document from its semantic version. This describes the library's own documents, not an organization's programme; its scoring is derived by the portal generator and is independent of this methodology.

A reader should not read a programme-maturity tier as a document-maturity classification or the reverse: the first rates an adopter's operations on a 1-to-5 ladder, the second rates a library file's version stability in three bands.

The Digital Trust Index thresholds in the [`Digital Trust and Assurance Metrics Register`](register-digital-trust-and-assurance-metrics.md) map a 0-to-5 DTI score onto these same five tier names. The ladder here is the shared tier vocabulary those thresholds use; the DTI applies it to a different, continuous 0-to-5 scale rather than to the discrete per-domain tiers this standard aggregates.

---

## 9. Boundary: maturity levels, not capability levels

This standard documents the **maturity-level** model: how consistently, and how measurably, a programme operates, rated tier 1 to 5 and aggregated across domains. It does not introduce process **capability** levels, a distinct per-process rating scheme that measures the capability of an individual process rather than the maturity of the programme as a whole.

A capability-level scheme, if the organization adopts one, is a separate model layered on top of this ladder, and is out of scope for this standard.

---

## 10. Application and review cadence

Maturity assessment is conducted at least annually, per the governance review process in the Governance Performance and Improvement Framework, and on material change to the programme's scope. The assessor uses the adopter template to record per-domain and per-question scores, applies the aggregation in section 5 and the floor-check in section 7, and reports both the aggregate tiers and the floor-check exceptions to the ERC through the Maturity Assessment Report.

This standard is reviewed annually, or on material change to the maturity model or the assessment methodology.

---

## 11. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| CMMI | Maturity-level model | Lineage of the five-tier maturity ladder |
| COBIT 2019 | MEA01: Managed Performance and Conformance Monitoring | Governance maturity and performance monitoring |
| ISO/IEC 42001:2023 | §10: AI Governance Improvement | AI governance maturity indicators feed the AI-domain tier |
| ISO 9001:2015 | §9 to 10: Performance Evaluation and Improvement | Performance evaluation and continual-improvement basis |

---

*This document is released under the CC BY-SA 4.0 licence. No rights reserved.*



**End of Document**
