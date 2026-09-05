# Maturity Assessment Methodology Standard

**Document Title:** Maturity Assessment Methodology Standard\
**Document Type:** Standard\
**Version:** 1.1.1\
**Date:** 2026-09-05\
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

This standard defines the methodology for assessing governance programme maturity across the library's domains. It documents five things that the corpus previously applied without a single authoritative reference:

1. The five-tier maturity ladder.
2. The median-of-medians aggregation that produces per-domain and overall programme tiers.
3. The limitation of that aggregation: a single critically-weak domain does not move the aggregate tier.
4. The compensating floor-check that surfaces such a domain regardless of the aggregate tier.
5. The structured, comparable measurement model that derives objective maturity signals from the relationship model.

It is the authoritative methodology reference behind the maturity-assessment section of the [`Governance Performance and Improvement Framework`](framework-governance-performance-and-improvement.md) and the [`Adopter Maturity Self-Assessment Template`](../docs/template-maturity-self-assessment.md). Those documents apply the ladder in context; this standard states the method, its limitation, and the compensating control in one place.

---

## 2. Scope

1. Applies to programme-maturity assessment across all governance domains: governance, risk, compliance, crypto, privacy, security, operations, resilience, supply chain, architecture, developer security, and AI.
2. Covers the maturity ladder, the aggregation method, its outlier-masking limitation, the compensating floor-check, and the relationship-model-derived measurement model.
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

The per-domain median produces an integer or a half-value (the latter where an even count of question scores leaves two middle tiers that differ by an odd number, so their average lands on a half); the overall median, taken over those per-domain scores, can additionally produce a quarter-value (for example, the median of the domain scores 2.0 and 2.5 is 2.25). This standard documents the method; it does not change the mechanics the template records step by step, and it is independent of the generated document-maturity scoring (section 8).

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

## 10. Structured, comparable measurement model

Sections 4 and 5 produce a self-assessed tier: a domain owner scores each question against the ladder, and the median-of-medians aggregation yields per-domain and overall tiers. This section adds an objective, evidence-grounded layer over that self-assessment: a set of measurable signals derived from the machine-readable [`relationship model`](relationship-model.generated.json), so a tier claim is corroborated by corpus evidence and is comparable across domains, over time, and across adopters.

### 10.1 Relationship-model-derived signals

The relationship model can record typed relationships among corpus entities across the governance relationship framework's full relationship-class vocabulary (fifteen classes). This measurement model derives its signals from seven of those classes, each selected because it maps to a distinct maturity dimension; each of the seven yields one normalized maturity signal:

| Relationship class | Derived signal | What it measures |
| --- | --- | --- |
| requirement | Requirement coverage | Share of applicable requirements that a corpus document expresses |
| implementation | Implementation coverage | Share of required controls that an implementing document realizes |
| correspondence | Framework-alignment breadth | Share of controls carrying at least one cross-framework mapping |
| applicability | Scoping completeness | Share of entities carrying an explicit applicability determination |
| assessed outcome | Assurance density | Share of controls carrying a recorded assessed outcome |
| influence | Dependency articulation | Share of entities whose influencing relationships are recorded |
| containment | Structural completeness | Share of collections whose members are enumerated |

A domain's **measured profile** is the vector of its seven signals.

### 10.2 Comparability basis

Each signal is a normalized ratio in the range 0 to 1, not a raw count. Normalization is what makes the model comparable: a ratio is independent of corpus size, so a domain with forty controls and a domain with four hundred are measured on the same scale, the same domain is comparable to itself over successive assessments (a longitudinal trend), and two adopters of different corpus scales are comparable to each other. Raw counts support none of these comparisons; the ratio basis supports all three. Each signal's denominator is the domain's recorded count of the relevant entity class (its controls, requirements, entities, or collections), so a value is a share within that range whenever the eligible population is completely recorded. Where the eligible population is itself incompletely recorded (for example a requirement that should exist but has not been captured), the ratio can over-state or under-state true coverage and is therefore not a reliable comparable share: the signal is reported as indeterminate and excluded from comparison rather than read as a bound. A domain with no relevant entities has no denominator; its signal is reported as not applicable, never computed as zero over zero. Recording completeness is thus a precondition for a comparable measurement, in the same spirit as the aggregate-masking limitation in section 6.

### 10.3 Evidence-tempering of the self-assessed tier

The measured profile corroborates or tempers the ladder self-assessment. A self-assessed tier is evidence-supported only when the domain's measured signals meet that tier's expected floor; a tier claimed above its measured evidence is surfaced as an exception, in the same spirit as the floor-check of section 7, except that the comparison here is self-assessment against measured evidence rather than aggregate median against an outlier. The tier-to-evidence expectations are the proposed defaults; an organization sets them to its own risk appetite:

| Tier | Expected measured floor |
| --- | --- |
| 1 Initial | No expectation; signals may be absent |
| 2 Managed | Requirement and implementation coverage have begun (signals above zero) |
| 3 Defined | Requirement coverage, implementation coverage, and scoping completeness are substantive |
| 4 Quantitatively Managed | Assurance density is substantive, so measured outcomes exist to manage against objectives |
| 5 Optimized | The signals show a sustained improving trend across successive assessments |

An organization tunes the "begun", "substantive", and "sustained" thresholds to its exposure, exactly as it tunes the floor-check defaults in section 7.

### 10.4 Source population and current state

The signals compute from the relationship model once its source is populated with the corpus's real relationships. The model ships today as a schema scaffold: [`relationship-model-source.json`](relationship-model-source.json) carries representative example entities and one record for each of the seven signal-bearing classes, demonstrating the structure without asserting real corpus relationships. Until the source is populated, this measurement model defines the derivation only; computing live signal values additionally requires a generator over the populated relationship model, which the follow-up work below establishes. Populating the relationship-model source with the corpus's real relationships is the downstream enablement that turns the defined derivation into live, comparable measurement; it is tracked as separate follow-up work and is not a change to this methodology.

---

## 11. Application and review cadence

Maturity assessment is conducted at least annually, per the governance review process in the Governance Performance and Improvement Framework, and on material change to the programme's scope. The assessor uses the adopter template to record per-domain and per-question scores, applies the aggregation in section 5 and the floor-check in section 7, and reports both the aggregate tiers and the floor-check exceptions to the ERC through the Maturity Assessment Report.

This standard is reviewed annually, or on material change to the maturity model or the assessment methodology.

---

## 12. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| CMMI | Maturity-level model | Lineage of the five-tier maturity ladder |
| COBIT 2019 | MEA01: Managed Performance and Conformance Monitoring | Governance maturity and performance monitoring |
| ISO/IEC 42001:2023 | §9.1: Monitoring, measurement, analysis and evaluation | AI governance maturity indicators feed the AI-domain tier |
| ISO 9001:2015 | §9 to 10: Performance Evaluation and Improvement | Performance evaluation and continual-improvement basis |

---

*This document is released under the CC BY-SA 4.0 licence. No rights reserved.*



**End of Document**
