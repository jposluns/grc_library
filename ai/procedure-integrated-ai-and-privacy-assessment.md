# Integrated AI and Privacy Assessment Procedure

**Document Title:** Integrated AI and Privacy Assessment Procedure\
**Document Type:** Procedure\
**Version:** 0.1.0\
**Date:** 2026-07-11\
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

This router follows the alignment guidance of ISO/IEC 42005:2025 Annex D, which directs an organization to run an AI system impact assessment in conjunction with its existing related assessments so they draw on and contribute to one another rather than duplicate work, through a coordination guide (Annex D.2), an alignment guide (Annex D.3 and Table D.1), and a mapping guide (Annex D.4). Annex D frames those existing assessments as general families, among them the privacy impact assessment (PIA) and the human rights impact assessment (HRIA); this procedure instantiates those families with the specific regimes the library carries (the GDPR DPIA is the data-protection form of a PIA, and the EU AI Act FRIA is the fundamental-rights form of an HRIA) and extends the router beyond the European Union with Canadian and United States limbs (the Treasury Board Directive on Automated Decision-Making, and the NIST Privacy Framework).

---

## Trigger events

Run this procedure when a system, product, or processing operation may be in scope of more than one of the following at the same time:

- **A high-risk personal-data processing** likely to result in a high risk to the rights and freedoms of natural persons (the GDPR Article 35(1) DPIA trigger).
- **A solely-automated decision** producing legal or similarly significant effects on an individual (GDPR Article 22).
- **A high-risk AI system** within the EU AI Act (Article 6 and Annex III).
- **An AI system whose deployer is in scope of the FRIA** (EU AI Act Article 27(1)): a deployer that is a body governed by public law, a private entity providing a public service, or a deployer of a high-risk AI system referred to in points 5(b) and (c) of Annex III. The obligation attaches to high-risk AI systems within Article 6(2) and excludes systems intended to be used in the Annex III point 2 (critical-infrastructure) area; this router screens broadly, and the FRIA instrument confirms the precise scope.
- **An automated decision system in scope of the Canada Treasury Board Directive on Automated Decision-Making** (the Canadian limb): an automated decision system in production used to make, or to assist in making, an administrative decision or a related assessment about a client (Directive section 5.1), where an automated decision system is any technology that assists or replaces the judgment of human decision-makers (Directive Appendix A). The Directive is binding on federal institutions subject to the Policy on Service and Digital and is a leading-practice benchmark for other organizations (Directive section 8).
- **A data-processing activity managed under the United States NIST Privacy Framework** (the United States limb): a context in which the organization manages privacy risk to individuals using the NIST Privacy Framework's enterprise-risk approach, privacy risk being the likelihood and impact of a problematic data action. The NIST Privacy Framework is voluntary and is not itself a legal trigger; this router screens broadly and the Framework's own privacy risk assessment confirms scope.

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
| Automated decision system in scope of the Canada Treasury Board Directive on Automated Decision-Making (in production, making or assisting an administrative decision about a client) | Algorithmic Impact Assessment (AIA), completed and published before the system enters production (Directive section 6.1) | The AIA owns the Canadian automated-decision-governance limb; its impact level (I to IV) sets the proportionate Appendix C requirements. It shares evidence with, and does not substitute for, the DPIA, the AI System Impact Assessment, and the FRIA |
| Privacy-risk context managed under the United States NIST Privacy Framework | NIST Privacy Framework privacy risk assessment, organized by the Identify-P, Govern-P, Control-P, Communicate-P, and Protect-P Functions | Owns the United States privacy-risk limb (privacy risk is the likelihood and impact of a problematic data action); complements, and does not substitute for, the GDPR DPIA limb, and shares the data-map and inventory evidence |
| All of the above (automated decision plus high-risk AI plus an Article 27 deployer) | ADM register entry plus DPIA plus AI System Impact Assessment plus FRIA | One coordinated pass: the DPIA owns the data-protection limb, the AI System Impact Assessment owns the AI-specific limb, and the FRIA owns the fundamental-rights limb complementing the DPIA |

### Step 4: Compose the assessments (limbs, shared evidence, no substitution)

- **One limb each.** The DPIA owns the data-protection limb, the AI System Impact Assessment owns the AI-specific limb, and the FRIA owns the fundamental-rights limb. This limb split follows the DPIA template's existing statement that, for an AI system, "the DPIA addresses the data protection limb and the AI System Impact Assessment addresses the AI-specific limb" ([`privacy/template-dpia.md`](../privacy/template-dpia.md)).
- **Shared evidence and mutual reference.** The assessments share evidence and reference each other, rather than re-collecting the same facts. The DPIA template already states this for the DPIA and the AI System Impact Assessment; this procedure extends the same rule to the FRIA.
- **The FRIA complements the DPIA; it does not substitute for it.** Where an Article 27 obligation is already met through the GDPR Article 35 DPIA, the EU AI Act (Article 27(4)) requires the fundamental rights impact assessment to complement that data protection impact assessment. A FRIA is therefore never a replacement for a required DPIA, and a DPIA is never a replacement for a required FRIA; where both are triggered, both are performed, with the FRIA building on the DPIA's shared evidence.

### Step 5: Confirm applicability and timing

- **GDPR Article 22 and Article 35** are in force; the ADM register entry and the DPIA apply whenever their triggers are met.
- **The EU AI Act Article 27 FRIA deployer obligation applies from 2 August 2026** (Regulation (EU) 2024/1689, Article 113: the Regulation applies from that date, and Article 27 falls under the general application date rather than the earlier or later carve-outs). A deployer in scope performs the FRIA before deploying an in-scope high-risk AI system on or after that date. Confirm the current in-force position of any cited provision against the official consolidated text before relying on it, since a regulation's consolidated version can be amended.
- **The Canada Treasury Board Directive on Automated Decision-Making** is in force (current version dated 24 June 2025, following the directive's third review; automated decision systems developed or procured before that date have until 24 June 2026 to meet the new or updated requirements). A federal institution subject to the Policy on Service and Digital completes and publishes the AIA before an in-scope automated decision system enters production; other organizations apply it as a leading practice.
- **The NIST Privacy Framework** is a voluntary privacy-risk-management framework, not a statute, and carries no commencement date; it applies wherever the organization elects to manage privacy risk under it.

---

## Roles and responsibilities

| Role | Responsibility |
| --- | --- |
| AI System Inventory Keeper | Maintains the AI System Register entry and its cross-reference to the ADM register |
| Data Protection Officer | Owns the DPIA and the ADM register entry; confirms the data-protection limb |
| AI Risk Maintainer | Owns the AI System Impact Assessment; confirms the AI-specific limb |
| Deployer accountable owner | Owns the FRIA where the Article 27 test is met; confirms the fundamental-rights limb complements, and does not replace, the DPIA |
| Jurisdiction limb owner | Owns the Algorithmic Impact Assessment where the Canada Treasury Board Directive applies, and the NIST Privacy Framework privacy risk assessment in a United States privacy-risk context; confirms each jurisdiction limb complements, and does not substitute for, the others |
| Legal and compliance | Confirm the regime-trigger determination and the applicability position of each cited provision |

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 42005:2025 | Annex D.2 to D.4: aligning the AI system impact assessment with other assessments | The coordinate-not-duplicate router model (Purpose; Step 4 composition) |
| EU GDPR (Regulation (EU) 2016/679) | Article 35 (DPIA); Article 22 (automated decisions) | Data-protection limb (DPIA and automated-decision routing) |
| EU AI Act (Regulation (EU) 2024/1689) | Article 27: fundamental rights impact assessment | Fundamental-rights limb (FRIA routing) |
| Canada Treasury Board Directive on Automated Decision-Making | Sections 5, 6.1, and 8; the Algorithmic Impact Assessment | Canadian automated-decision-governance limb |
| NIST Privacy Framework 1.0 | Core Functions (Identify-P, Govern-P, Control-P, Communicate-P, Protect-P); ID.RA-P Risk Assessment | United States privacy-risk limb |

---

## Required outputs

- An ADM register entry with the `DPIA reference` and `AI System Register cross-reference` fields populated.
- The DPIA, AI System Impact Assessment, FRIA, Algorithmic Impact Assessment, and NIST Privacy Framework privacy risk assessment that the routing table required for the system, each completed through its own instrument, sharing evidence and referencing one another.
- A record of the regime-trigger determination and the composition decision, retained with the assessments.

---

**End of Document**
