# What happens when a critical AI supplier fails

**Document Title:** What happens when a critical AI supplier fails\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-08-15\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`supply-chain/procedure-third-party-ai-due-diligence.md`](../../supply-chain/procedure-third-party-ai-due-diligence.md), [`resilience/procedure-cross-domain-incident-coordination.md`](../../resilience/procedure-cross-domain-incident-coordination.md), [`ai/plan-ai-incident-response.md`](../../ai/plan-ai-incident-response.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/scenarios/scenario-critical-supplier-outage.md`](scenario-critical-supplier-outage.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Scenario\
**Narrative Status:** Non-normative\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`supply-chain/procedure-third-party-ai-due-diligence.md`](../../supply-chain/procedure-third-party-ai-due-diligence.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../../supply-chain/standard-supplier-security-and-privacy-assurance.md), [`supply-chain/procedure-supplier-ongoing-monitoring.md`](../../supply-chain/procedure-supplier-ongoing-monitoring.md), [`ai/plan-ai-incident-response.md`](../../ai/plan-ai-incident-response.md), [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md), [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../../privacy/procedure-data-protection-and-privacy-breach-response.md), [`resilience/procedure-cross-domain-incident-coordination.md`](../../resilience/procedure-cross-domain-incident-coordination.md), [`supply-chain/register-concentration-risk.md`](../../supply-chain/register-concentration-risk.md), [`ai/register-model-registry.md`](../../ai/register-model-registry.md), [`ai/template-ai-vendor-security-questionnaire.md`](../../ai/template-ai-vendor-security-questionnaire.md), [`supply-chain/procedure-supplier-exit-and-data-return.md`](../../supply-chain/procedure-supplier-exit-and-data-return.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-012\
**Last Reviewed:** 2026-08-15

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Scenario premise

This scenario is a composite illustration. It describes no identifiable organization, no actual provider, and no real incident, and it makes no claim about how frequent or probable such an event is.

An organization has adopted an external AI service provider for a customer-facing assistant and internal workflows. The provider hosts fine-tuned models built from the organization's data, stores prompts and retrieval content, and holds derived artefacts such as embeddings. One morning the provider's service stops responding: the assistant is down, the internal workflows halt, and the provider's status page confirms a service disruption. Later the same day, the provider's security advisory states that the disruption began with a security incident in its own infrastructure, and that customer-supplied data and customer-specific model artefacts were exposed to an unauthorized party. The organization now has three problems at once: keeping the dependent services running, establishing what it has lost, and deciding whether the relationship continues, while meeting its own obligations to regulators and affected individuals.

## How the event unfolds

The first signals are operational. The [AI Incident Response Plan](../../ai/plan-ai-incident-response.md) names a supplier model incident as one of its AI incident classes, and its detection triggers for that class (which the plan lists) fit this event. The plan's containment menu (its Contain step) offers actions fitted to AI systems, applied per the severity and the system architecture. The plan reserves external disclosure of a specific incident as a decision of the AI governance body it names, in coordination with legal.

The provider's advisory arrives through the contractual notification channel. Where the contract follows the corpus pattern, it obliges the provider to notify within the window the [Third-Party AI Due Diligence Procedure](../../supply-chain/procedure-third-party-ai-due-diligence.md) records and to state the notification contents it specifies (its section 6.3).

The next internal question is exposure. The [Model Registry](../../ai/register-model-registry.md) is the corpus's authoritative inventory of every model the organization uses in production or pre-production, and its scope includes foundation models consumed from a provider, recorded at the specific version and configuration the organization depends on; each entry cross-references the AI systems that depend on the model, and its lineage records exist to allow traceability for incident response and supplier-incident impact analysis. The register is a dependency of a complete impact assessment: enumerating the affected models, systems, and derived artefacts requires the inventory the register holds.

The event now runs in four streams at once: an operational outage, a security incident, a privacy matter, and a supplier matter. The [Cross-Domain Incident Coordination Procedure](../../resilience/procedure-cross-domain-incident-coordination.md) assigns ownership for exactly these classes, and it supplies the joint command structure and the hand-off checklists that coordinate the parallel streams (the checklist items it enumerates).

In parallel, the privacy stream applies the AI-specific assessment dimensions the [Data Protection and Privacy Breach Response Procedure](../../privacy/procedure-data-protection-and-privacy-breach-response.md) applies to an AI breach (its section 4.3). That procedure also has the organization confirm that the supplier met its contractual notification obligation and document the confirmation, and it carries the analysis of how the contractual supplier notification window relates to the regulatory notification clock. Whether and when regulators and individuals are notified is governed there and in the [Security Incident Response Procedure](../../security/procedure-security-incident-response.md), whose notification obligations summary records the regimes, triggers, deadlines, and notifying roles; this page routes to those tables and reproduces none of them.

The supplier stream starts its own clock. Under the [Supplier Ongoing Monitoring Procedure](../../supply-chain/procedure-supplier-ongoing-monitoring.md), a supplier breach disclosure triggers an immediate unscheduled review outside the scheduled cycle, among the triggers its table records. The [Third-Party and Supply Chain Risk Standard](../../risk/standard-third-party-and-supply-chain-risk.md) sets the response sequence for incidents within the supplier and organizational-impact scope it defines (its section 8.1).

The outage also forces the continuity question. The same standard requires a supply chain continuity risk assessment as part of the business impact analysis for the supplier tier it names, including the continuity elements it specifies (its section 7); the corpus locates the fallback question before the failure, not during it.

The response then reaches a second question: the same provider underpins other, unrelated services. The [Concentration Risk Register](../../supply-chain/register-concentration-risk.md) exists to identify single points of failure and shared dependencies that would cause cross-portfolio impact if a concentrated dependency fails, and its service-class dimension flags an over-concentrated AI-provider dependency as an indicative concentration concern. Its operating expectations escalate findings at the severity ratings it defines within the review cycle they are identified, and it defines the treatment menu the response chooses from.

Leadership finally faces the continuation decision. The [Supplier Exit and Data Return Procedure](../../supply-chain/procedure-supplier-exit-and-data-return.md) classifies a critical unresolvable security or privacy gap as a risk-driven exit trigger, and its data-deletion step defines the deletion mechanics (its Step 4). The [due diligence procedure](../../supply-chain/procedure-third-party-ai-due-diligence.md) sets the on-termination deletion, certified-confirmation, and record-retention requirements (its section 8.2), with the windows and floors recorded there.

## Where the corpus controls engage

- **Before the engagement.** The [AI Vendor Security Questionnaire](../../ai/template-ai-vendor-security-questionnaire.md) records the provider's responses, before signature, across the AI-service risk areas it covers. The general AI contract clauses the [third-party risk standard](../../risk/standard-third-party-and-supply-chain-risk.md) sets (its section 5.1) bind the relationship; the breach-specific duty is the incident-notification clause the [due diligence procedure](../../supply-chain/procedure-third-party-ai-due-diligence.md) records (its section 6.3). The executed contract clauses are a dependency of every response step that invokes a contractual right; the recorded questionnaire responses are a contribution to a response that begins from prior answers rather than discovery.
- **At notification.** The incident-notification clause and the [minimum contract clauses of the supplier assurance standard](../../supply-chain/standard-supplier-security-and-privacy-assurance.md), which record the supplier's notification and termination terms, are a contribution to timely supplier notification; the relationship between the supplier's contractual window and the regulatory clock is analyzed in the [privacy breach procedure](../../privacy/procedure-data-protection-and-privacy-breach-response.md).
- **During the response.** The [cross-domain coordination procedure](../../resilience/procedure-cross-domain-incident-coordination.md)'s joint command structure and hand-off checklists are a contribution to a joined response across the four streams, and the [AI incident plan](../../ai/plan-ai-incident-response.md) supplies the containment menu the AI stream selects from, applied per the severity and the system architecture.
- **After the event.** The [monitoring procedure](../../supply-chain/procedure-supplier-ongoing-monitoring.md)'s trigger-based review, the [concentration register](../../supply-chain/register-concentration-risk.md)'s escalation expectations and treatment menu, and the [exit procedure](../../supply-chain/procedure-supplier-exit-and-data-return.md)'s deletion mechanics are the corpus controls the reassess-or-exit decision and its execution draw on.

## What good looks like

This section is a composite synthesis across the sources above; the limitations state the validation it requires. In a well-prepared organization, the questionnaire answers and contract clauses were obtained before signature; obtaining them is a contribution to a response that begins from recorded answers rather than discovery. The model registry already lists the affected models at the version and configuration the organization depends on, with the dependent systems cross-referenced. The continuity assessment already names pre-qualified alternates, a contribution to the outage decision. The four parallel streams are coordinated through one joint command, and notification decisions are made against the corpus procedures. The concentration finding was already registered, a contribution to choosing among prepared treatments. The event still occurs in a well-prepared organization: preparation is a contribution to a controlled response, and the artefacts it produces are evidence to inspect when testing whether the controls operated.

## Evidence to request

- The provider's completed AI vendor security questionnaire and the executed AI contract clauses: evidence for the pre-engagement due diligence control and for the contractual rights the response invokes ([questionnaire](../../ai/template-ai-vendor-security-questionnaire.md); [due diligence procedure](../../supply-chain/procedure-third-party-ai-due-diligence.md)).
- The model registry extract for the affected provider, showing the recorded versions, configurations, and dependent systems: evidence for the inventory control the impact assessment depends on ([model registry](../../ai/register-model-registry.md)).
- The supply chain continuity risk assessment for the affected supplier, including the identified alternates: evidence for the continuity-planning control ([third-party risk standard](../../risk/standard-third-party-and-supply-chain-risk.md)).
- The joint decision log and the completed hand-off checklists: evidence for the cross-domain coordination control operating during the event ([coordination procedure](../../resilience/procedure-cross-domain-incident-coordination.md)).
- The breach assessment and the documented notification decisions: evidence for the privacy and security notification controls ([privacy breach procedure](../../privacy/procedure-data-protection-and-privacy-breach-response.md); [security incident procedure](../../security/procedure-security-incident-response.md)).
- The unscheduled supplier review output and the updated residual risk rating: evidence for the monitoring control ([monitoring procedure](../../supply-chain/procedure-supplier-ongoing-monitoring.md)).
- The concentration register entry for the provider: evidence for the concentration-management control ([concentration register](../../supply-chain/register-concentration-risk.md)).
- Where exit is chosen, the deletion certificate or the documented-gap escalation: evidence for the exit and data-return control ([exit procedure](../../supply-chain/procedure-supplier-exit-and-data-return.md)).

## Limitations

- This scenario is illustrative and composite. It depicts no identifiable organization, provider, or incident, and it makes no claim about how frequent or probable supplier outages or supplier breaches are.
- This page establishes no requirement and creates no compliance. The linked corpus documents govern, and every notification window, day count, tier name, severity rating, retention period, and named coordinating or approving body lives in them, not on this page.
- The scenario joins an outage and a disclosed breach in one event so that both the continuity stream and the notification stream are visible. A real event can present either alone, and the linked corpus documents state which obligations attach to which facts.
- Composite content, including the premise, the narrative frame, and the whole of "What good looks like", is synthesis across sources and requires the adopting organization's own validation against its actual contracts, registers, and governance model.

**End of Document**
