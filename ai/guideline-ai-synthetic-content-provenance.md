# AI Synthetic-Content Provenance Guideline

**Document Title:** AI Synthetic-Content Provenance Guideline\
**Document Type:** Guideline\
**Version:** 0.0.2\
**Date:** 2026-07-12\
**Owner:** AI Security Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](policy-ai-compliance.md), [`ai/framework-ai-model-documentation-and-transparency.md`](framework-ai-model-documentation-and-transparency.md), [`ai/template-ai-vendor-security-questionnaire.md`](template-ai-vendor-security-questionnaire.md), [`ai/procedure-foundation-model-lifecycle.md`](procedure-foundation-model-lifecycle.md), [`ai/template-system-card.md`](template-system-card.md), [`ai/jurisdictions/annex-ai-european-union.md`](jurisdictions/annex-ai-european-union.md), [`ai/procedure-training-data-governance.md`](procedure-training-data-governance.md), [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI framework or regulatory change\
**Repository Path:** [`ai/guideline-ai-synthetic-content-provenance.md`](guideline-ai-synthetic-content-provenance.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This guideline provides implementation guidance for the AI-generated-content transparency obligations that [`ai/policy-ai-compliance.md`](policy-ai-compliance.md) Section 9.2 and the EU jurisdiction annex state at the policy and regulatory level. Those surfaces establish *what* must be labelled and *when*; this guideline is the *how*: the digital content transparency techniques an implementer selects and operates so that AI-generated or manipulated output is marked, detectable, and disclosed.

It is advisory guidance, not a control. Its technical content is drawn from the informative overview NIST AI 100-4, *Reducing Risks Posed by Synthetic Content: An Overview of Technical Approaches to Digital Content Transparency* (US Artificial Intelligence Safety Institute, November 2024), and its regulatory anchoring from the EU AI Act (Regulation (EU) 2024/1689), Article 50. NIST AI 100-4 is an overview of technical approaches rather than a mandate: it observes that the efficacy of many of these approaches is not fully examined and that most may be years away from widespread deployment. This guideline therefore describes techniques and their tradeoffs; it does not require any single technique.

## Scope

In scope: transparency for AI-generated or manipulated **output** (audio, image, video, and text) produced by systems the organization builds, operates, or procures.

Out of scope, and covered elsewhere:

- Labelling of synthetic **training-input** data, which is governed by [`ai/procedure-training-data-governance.md`](procedure-training-data-governance.md) (a different limb: input data, not generated output).
- Model and dataset supply-chain provenance and integrity (cryptographic hashing, dataset lineage), which is governed by [`ai/standard-ai-and-agentic-development-security.md`](standard-ai-and-agentic-development-security.md).

## Digital content transparency techniques

NIST AI 100-4 groups the technical approaches into provenance data tracking (recorded at or after generation) and detection (recovering the signal afterward).

**Provenance data tracking** records information about a content item's origins and history. NIST AI 100-4 describes two current methods:

- **Digital watermarking** embeds information into the content itself (via the pixels, words, or samples), without a separate channel such as a metadata field; embedded information may include content origins, ownership details, timestamps, and unique identifiers. Watermarks may be **overt** (perceptible, such as a visible logo or an audible tone) or **covert** (imperceptible, requiring a detector that carries a non-zero false-positive and false-negative rate).
- **Metadata recording** associates descriptive information (origin, creation time and date, author, ownership, edit history) with the content item. NIST AI 100-4 notes that cryptographically signed metadata contributes most to transparency because it explicitly and tamper-evidently describes the content's origins (the signature notarizes the recorded metadata; it does not by itself verify that the metadata is accurate).

**Detection** recovers the transparency signal. NIST AI 100-4 describes three non-exclusive categories:

- **Provenance data detection**, which looks for provenance data already tracked via watermarks or metadata (metadata and covert watermarks are machine-readable; overt watermarks typically are not).
- **Automated content-based detection**, which identifies synthetic content from traces left during generation; NIST AI 100-4 cautions that this is a "cat-and-mouse game" and that detectors are often tied to, and perform well only on, specific generators.
- **Human-assisted detection**, in which reviewers, labelers, or domain experts augment automated tools.

## Choosing a technique: attributes and limitations

NIST AI 100-4 identifies design parameters an implementer weighs rather than a single correct choice: accurate detectability with a low false-positive and low false-negative rate; blind versus non-blind detection (whether the original content is needed to detect the mark); and robust versus fragile design (whether the mark should survive transformations or break to signal tampering). It also records that watermarks can be stripped or removed, that content-based detectors degrade against new generators, and a privacy consideration: a covert watermark that embeds sensitive information could disclose a tool's user without their knowledge, so covert marks that carry any sensitive information can make privacy controls harder.

The selection therefore records, per output surface, the technique(s) chosen, the residual detectability limits accepted, and the review cadence, rather than asserting a technique as complete.

## Disclosure and labelling

NIST AI 100-4 distinguishes **indirect disclosure** (machine-readable provenance data, such as metadata or a covert watermark) from **direct disclosure** (a human-perceivable label). Most provenance techniques produce indirect disclosures; to make people aware that AI was involved, the machine-readable data typically must be surfaced as a direct disclosure. Direct-disclosure techniques it describes include overt watermarks (visible icons, audible cues), in-content labels (warning, pre-roll, or interstitial labels; font differences for AI-generated text), and user-interface disclosures (disclaimers and symbols). NIST AI 100-4 notes limited consensus on how such labels should be designed for reliable human perception.

The labelling mechanism selected here is documented in the relevant system card per [`ai/policy-ai-compliance.md`](policy-ai-compliance.md) Section 9.2 and [`ai/template-system-card.md`](template-system-card.md).

## Standards and specifications

NIST AI 100-4 reports several provenance specifications the implementer may adopt. The Coalition for Content Provenance and Authenticity (C2PA) publishes a freely available specification for provenance data tracking that stores and signs metadata (assertions about origins, edit history, and a chain of provenance) for image, audio, and video, using hash functions, digital signatures, certificates with public-private key pairs, and trust lists of certificate authorities, in both embedded and external forms. NIST AI 100-4 also references file-signature and broadcast approaches beyond C2PA.

These specifications are described here as NIST AI 100-4 reports them; the C2PA specification text and the other named tools are not independently held in the organization's reference base, so no normative requirement in this guideline rests on their primary text. An implementer adopting one confirms its current specification at the source.

## Testing and evaluating transparency techniques

NIST AI 100-4 treats testing and evaluation as a first-class activity, with distinct evaluation considerations for watermarking, metadata recording, provenance data detection, automated content-based detection, and human-assisted detection. A transparency technique is verified against its stated false-positive and false-negative targets and its robustness assumptions before it is relied on for a disclosure obligation, and re-evaluated on the review cadence because detector efficacy drifts as generators change. This testing is recorded alongside the model's other evaluation evidence per [`ai/procedure-foundation-model-lifecycle.md`](procedure-foundation-model-lifecycle.md).

## Regulatory anchoring

The EU AI Act (Regulation (EU) 2024/1689) Article 50 states the binding transparency obligations this guideline helps implement:

- **Article 50(2):** providers of AI systems (including general-purpose systems) that generate synthetic audio, image, video, or text mark the outputs in a machine-readable format and make them detectable as artificially generated or manipulated, with technical solutions that are effective, interoperable, robust, and reliable as far as technically feasible; the obligation does not apply where the system performs an assistive function for standard editing or does not substantially alter the input.
- **Article 50(4):** deployers of a deepfake (generated or manipulated image, audio, or video) disclose that the content is artificially generated or manipulated (with an artistic-work carve-out), and deployers of AI-generated text published to inform the public on matters of public interest disclose it (with a human-editorial-review carve-out).
- **Article 50(5):** the disclosure is provided clearly and distinguishably at the latest at the time of first interaction or exposure.
- **Article 50(7):** the AI Office facilitates codes of practice on the detection and labelling of artificially generated or manipulated content.

The per-regime status, and any pending amendment to Article 50 (a proposed EU Digital Omnibus is not adopted and does not change the in-force obligation), are maintained in [`ai/jurisdictions/annex-ai-european-union.md`](jurisdictions/annex-ai-european-union.md); this guideline anchors to the in-force Regulation (EU) 2024/1689 and defers the version-sensitive status to that annex.

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| NIST AI 100-4 (November 2024) | Provenance data tracking, detection, labels, testing (informative overview) | The technique taxonomy and tradeoffs |
| EU AI Act (Regulation (EU) 2024/1689) | Article 50 | The binding output-transparency and deepfake-disclosure obligations |
| NIST AI RMF (2023) | Govern, Map, Measure, Manage | Situates transparency within the AI lifecycle (NIST AI 100-4 applies its concepts to the AI RMF lifecycle) |
| ISO/IEC 42001:2023 | Clause 8.1 | Operational control of AI transparency |

## Limitations

This guideline is original CC BY-SA 4.0 content; it is advisory, not a control, and adopting it does not by itself discharge a legal obligation. Its technical content restates the informative overview NIST AI 100-4, which observes that many of these approaches are immature, not fully examined for efficacy, and potentially years from widespread deployment, and that consensus on label design is limited; an implementer treats technique selection as a risk-weighted, re-evaluated decision, not a solved problem. The regulatory content anchors to the in-force EU AI Act Article 50; currency of that obligation and of any pending amendment is confirmed against the EU jurisdiction annex before reliance.

---

**End of Document**
