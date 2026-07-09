# Integrated AI and Privacy Assessment Procedure

**Document Title:** Integrated AI and Privacy Assessment Procedure\
**Document Type:** Procedure\
**Version:** 0.0.1\
**Date:** 2026-07-09\
**Owner:** AI Risk Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md), [`ai/checklist-ai-algorithmic-compliance.md`](checklist-ai-algorithmic-compliance.md), [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`privacy/register-automated-decision-making.md`](../privacy/register-automated-decision-making.md), [`privacy/template-dpia.md`](../privacy/template-dpia.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI risk or regulatory change\
**Repository Path:** [`ai/procedure-integrated-ai-and-privacy-assessment.md`](procedure-integrated-ai-and-privacy-assessment.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

A single system can fall in scope of more than one assessment regime at once: the data protection impact assessment (DPIA) under GDPR Article 35, the automated decision-making (ADM) provisions of GDPR Article 22, the AI System Impact Assessment for a high-risk AI system, and the fundamental rights impact assessment (FRIA) under EU AI Act Article 27. The library carries each instrument separately. This procedure is the router that ties them together: given a system's regime triggers, it says which assessments to run, which limb each one owns, and how they compose into one coordinated pass.

This procedure does not reproduce the content of the assessments it routes to. It does not restate the Article 35(7) DPIA content checklist, the ten steps of the [AI System Impact Assessment Procedure](procedure-ai-system-impact-assessment.md), or the control items of the [algorithmic compliance checklist](checklist-ai-algorithmic-compliance.md). It references them and defines the hand-offs between them.

---

## Trigger events

Run this procedure when a system, product, or processing operation may be in scope of more than one of the following at the same time:

- **A high-risk personal-data processing** likely to result in a high risk to the rights and freedoms of natural persons (the GDPR Article 35(1) DPIA trigger).
- **A solely-automated decision** producing legal or similarly significant effects on an individual (GDPR Article 22).
- **A high-risk AI system** within the EU AI Act (Article 6 and Annex III).
- **An AI system whose deployer is in scope of the FRIA** (EU AI Act Article 27(1)): a deployer that is a body governed by public law, a private entity providing a public service, or a deployer of a high-risk AI system referred to in points 5(b) and (c) of Annex III. The obligation attaches to high-risk AI systems within Article 6(2) and excludes systems intended to be used in the Annex III point 2 (critical-infrastructure) area; this router screens broadly, and the FRIA instrument confirms the precise scope.

Where only one trigger is present, run that single instrument directly; this router is for the multi-regime case.

---

## Procedure

### Step 1: Enter the system in the inventory

Record the activity in the [automated decision-making register](../privacy/register-automated-decision-making.md). The register is the single inventory entry point; its `DPIA reference` and `AI System Register cross-reference` fields link the coordinated assessments to one another and to the AI System Register.

### Step 2: Determine the regime triggers

Identify which of the trigger events above are present. The determination is per system and per material change, not once per organization.

### Step 3: Route to the required assessments

| Regime trigger present | Assessment(s) required | Composition |
| --- | --- | --- |
| High-risk personal-data processing (GDPR Article 35(1)) | DPIA | The DPIA is the base data-protection assessment |
| Solely-automated decision with legal or similarly significant effect (GDPR Article 22) | ADM register entry plus a DPIA | GDPR Article 35(3)(a) makes a DPIA required for systematic automated evaluation that produces such decisions; the DPIA covers the data-protection limb |
| High-risk AI system (EU AI Act Article 6, Annex III) | AI System Impact Assessment plus the EU AI Act deployer obligations | The AI System Impact Assessment covers the AI-specific limb |
| High-risk AI system whose deployer meets the EU AI Act Article 27(1) test (public-law body, private provider of a public service, or a deployer of an Annex III point 5(b) or (c) system) | FRIA | The FRIA complements the DPIA (Article 27(4)); it may reuse a previously conducted FRIA or an existing impact assessment (Article 27(2)) |
| All of the above (automated decision plus high-risk AI plus an Article 27 deployer) | ADM register entry plus DPIA plus AI System Impact Assessment plus FRIA | One coordinated pass: the DPIA owns the data-protection limb, the AI System Impact Assessment owns the AI-specific limb, and the FRIA owns the fundamental-rights limb complementing the DPIA |

### Step 4: Compose the assessments (limbs, shared evidence, no substitution)

- **One limb each.** The DPIA owns the data-protection limb, the AI System Impact Assessment owns the AI-specific limb, and the FRIA owns the fundamental-rights limb. This limb split follows the DPIA template's existing statement that, for an AI system, "the DPIA addresses the data protection limb and the AI System Impact Assessment addresses the AI-specific limb" ([`privacy/template-dpia.md`](../privacy/template-dpia.md)).
- **Shared evidence and mutual reference.** The assessments share evidence and reference each other, rather than re-collecting the same facts. The DPIA template already states this for the DPIA and the AI System Impact Assessment; this procedure extends the same rule to the FRIA.
- **The FRIA complements the DPIA; it does not substitute for it.** Where an Article 27 obligation is already met through the GDPR Article 35 DPIA, the EU AI Act (Article 27(4)) requires the fundamental rights impact assessment to complement that data protection impact assessment. A FRIA is therefore never a replacement for a required DPIA, and a DPIA is never a replacement for a required FRIA; where both are triggered, both are performed, with the FRIA building on the DPIA's shared evidence.

### Step 5: Confirm applicability and timing

- **GDPR Article 22 and Article 35** are in force; the ADM register entry and the DPIA apply whenever their triggers are met.
- **The EU AI Act Article 27 FRIA deployer obligation applies from 2 August 2026** (Regulation (EU) 2024/1689, Article 113: the Regulation applies from that date, and Article 27 falls under the general application date rather than the earlier or later carve-outs). A deployer in scope performs the FRIA before deploying an in-scope high-risk AI system on or after that date. Confirm the current in-force position of any cited provision against the official consolidated text before relying on it, since a regulation's consolidated version can be amended.

---

## Roles and responsibilities

| Role | Responsibility |
| --- | --- |
| AI System Inventory Keeper | Maintains the AI System Register entry and its cross-reference to the ADM register |
| Data Protection Officer | Owns the DPIA and the ADM register entry; confirms the data-protection limb |
| AI Risk Maintainer | Owns the AI System Impact Assessment; confirms the AI-specific limb |
| Deployer accountable owner | Owns the FRIA where the Article 27 test is met; confirms the fundamental-rights limb complements, and does not replace, the DPIA |
| Legal and compliance | Confirm the regime-trigger determination and the applicability position of each cited provision |

---

## Required outputs

- An ADM register entry with the `DPIA reference` and `AI System Register cross-reference` fields populated.
- The DPIA, AI System Impact Assessment, and FRIA that the routing table required for the system, each completed through its own instrument, sharing evidence and referencing one another.
- A record of the regime-trigger determination and the composition decision, retained with the assessments.

---

**End of Document**
