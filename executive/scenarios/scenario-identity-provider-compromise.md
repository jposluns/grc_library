# When the enterprise identity provider can no longer be trusted

**Document Title:** When the enterprise identity provider can no longer be trusted\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-08-17\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-identity-and-access-management.md`](../../security/policy-identity-and-access-management.md), [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md), [`resilience/procedure-cross-domain-incident-coordination.md`](../../resilience/procedure-cross-domain-incident-coordination.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/scenarios/scenario-identity-provider-compromise.md`](scenario-identity-provider-compromise.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Scenario\
**Narrative Status:** Non-normative\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`risk/register-scenario-risk-catalogue.md`](../../risk/register-scenario-risk-catalogue.md), [`security/policy-identity-and-access-management.md`](../../security/policy-identity-and-access-management.md), [`security/standard-privileged-access-management.md`](../../security/standard-privileged-access-management.md), [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md), [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md), [`resilience/procedure-business-impact-analysis.md`](../../resilience/procedure-business-impact-analysis.md), [`resilience/procedure-cross-domain-incident-coordination.md`](../../resilience/procedure-cross-domain-incident-coordination.md), [`operations/register-asset-inventory.md`](../../operations/register-asset-inventory.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-015\
**Last Reviewed:** 2026-08-17

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Scenario premise

This scenario is a composite illustration. It describes no identifiable organization, no actual identity provider, and no real incident, and it makes no claim about how likely or frequent such an event is.

An organization runs its sign-in through a single enterprise identity provider. People authenticate through it to reach the SaaS estate and internal applications, service and machine identities authenticate through it to reach each other, and privileged roles are activated through it. One morning the security team is reading sign-in records it cannot explain: sessions issued for accounts whose owners were verifiably elsewhere, and a privilege assignment nobody requested. During the day the working hypothesis hardens: the identity provider, or the organization's tenant within it, has been compromised, and every credential and token it has recently issued is in question.

The identity provider is the trust plane the rest of the estate authorizes against. That is why leadership faces three questions at once: which services and privileges are affected, how to contain a failure of trust rather than a failure of one machine, and how to restore access without destroying evidence or losing track of who decided what. The corpus names this class of event as a reference scenario: the [scenario risk catalogue](../../risk/register-scenario-risk-catalogue.md) carries identity-provider compromise as member SCN-CYB-004 of its cyber attack reference set, and that catalogue is where the scenario class and its neighbours live.

## How the event unfolds

**The trust signal.** The first evidence is in the logs. The [logging and monitoring standard](../../security/standard-logging-and-monitoring.md) owns the log-coverage requirement (its section 4.1), centralized collection into the enterprise SIEM (its section 4.3), and the correlation and alerting rules (its section 4.5). The [identity and access management policy](../../security/policy-identity-and-access-management.md) routes identity telemetry into that pipeline: it requires IAM events to be logged to the SIEM per the logging standard and correlated with endpoint and network telemetry (its section 4.7). When the signal fires, the [security incident response procedure](../../security/procedure-security-incident-response.md) owns what happens next: its detection and triage section (its section 4) records the detection sources it recognizes and the ordered triage sequence a SOC analyst follows before any containment action, and that sequence stays in the procedure. The alert record and the triage record are evidence of when the organization knew and what it did first.

**The authority question.** A compromised identity layer puts elevated identities in scope, and the corpus keeps a separate, stricter route for those. The [identity and access management policy](../../security/policy-identity-and-access-management.md) establishes the authoritative identity record (its section 4.1), and places privileged accounts under central management and audit (its section 4.4). The [privileged access management standard](../../security/standard-privileged-access-management.md) owns the privileged control set (its section 4.2) and the privileged account lifecycle (its section 5), and its incident response section treats suspected compromise of a privileged account as a security incident at the severity it assigns, with the immediate actions and notifications recorded there (its section 6). Those records are a dependency of the question leadership needs answered early: which privileges could the attacker have reached, and which of them were active.

**The service question.** A current map of the estate is a dependency of containment, and it must exist before the event. The [asset inventory register](../../operations/register-asset-inventory.md) is the authoritative record of the organization's systems and services, with the record schema it defines (its asset record schema section). The [business impact analysis procedure](../../resilience/procedure-business-impact-analysis.md) records what each critical service depends on, and identity services are among the dependency classes its dependency step names (its Step 3). Management uses the two together to enumerate the services that trust the compromised provider and the critical business outputs behind them. A current inventory and dependency map are a dependency of a complete answer; without them the affected-service list is reconstructed under pressure, during the event, from memory.

**The joined response.** The event is a security incident and a service disruption at once. The services that authorize against the identity layer are a dependency on it, and its containment and their continuity are one problem, not two. The security stream follows the [security incident response procedure](../../security/procedure-security-incident-response.md) (its section 5), where evidence preservation carries the priority its containment principles state. The operations stream carries the continuity of critical outputs. The [cross-domain incident coordination procedure](../../resilience/procedure-cross-domain-incident-coordination.md) is where the streams join: its domain ownership decision rule assigns the primary and participating domains, its joint command structure names the coordinating roles, and its coordination lifecycle adds the cross-stream synchronization points on top of each domain's own procedure. Its cross-stream evidence handling keeps a single evidence index across the streams, a contribution to security containment and service continuity proceeding as one recorded response rather than two competing ones.

**The restoration decision.** Restoring trust is a decision sequence, and the corpus already holds its inputs. Recovery runs under the incident procedure's containment, eradication, and recovery section ([security incident response procedure](../../security/procedure-security-incident-response.md), its section 5), and the order in which services return is a dependency on the recovery objectives, continuity requirements, and approvals the [business impact analysis procedure](../../resilience/procedure-business-impact-analysis.md) has each assessment record (its Steps 5 to 7); the objectives and their values stay in the assessments. Re-established privileged access runs back through the lifecycle the [privileged access management standard](../../security/standard-privileged-access-management.md) records (its section 5) rather than through improvised grants made in the rush to recover.

## Where the corpus controls engage

- **Before the event.** The authoritative identity record ([identity and access management policy](../../security/policy-identity-and-access-management.md), its section 4.1) is a dependency of attributing any session or change to a verified entity. The privileged-access control set the [privileged access management standard](../../security/standard-privileged-access-management.md) records (its section 4.2) is a prevention against a compromised privileged account operating beyond the bounds those controls set. The [asset inventory register](../../operations/register-asset-inventory.md) and the dependency mapping step of the [business impact analysis procedure](../../resilience/procedure-business-impact-analysis.md) (its Step 3) are dependencies of impact identification. Log coverage and centralized collection ([logging and monitoring standard](../../security/standard-logging-and-monitoring.md), its sections 4.1 and 4.3) are contributions to detection, and the resulting logs are evidence of what the identity layer actually did.
- **During the event.** The detection, triage, and containment sections of the [security incident response procedure](../../security/procedure-security-incident-response.md) (its sections 4 and 5) and the ownership rule, joint command structure, and coordination lifecycle of the [cross-domain incident coordination procedure](../../resilience/procedure-cross-domain-incident-coordination.md) are contributions to a response that is joined across security and operations, and the joint decision log that procedure maintains is evidence of what was decided and on whose authority.
- **After the event.** The post-incident review of the [security incident response procedure](../../security/procedure-security-incident-response.md) (its section 7), the access review and certification route of the [identity and access management policy](../../security/policy-identity-and-access-management.md) (its section 4.5), and its compliance and audit route (its section 4.8) are contributions to the restored estate being verified against current records rather than assumed clean; the review contents, cadences, and approval routes stay in those documents.

## What good looks like

The following reading is a composite of the sources above; see the limitations.

In a well-prepared organization, the map existed before the trust failed: the asset inventory and the business impact assessments already record which services depend on the identity provider, and the affected-service question is answerable from records rather than from memory. Response authority is explicit, held in the incident procedure's roles and, once operations engages, in the coordination procedure's joint command, and containment of the identity layer is a decision with a named owner rather than a negotiation. Security and operations work from one evidence index and one joint decision log, keeping the facts and the decisions in one place. Privileged access comes back through the lifecycle the privileged access management standard records, and the recovery is recorded end to end in the incident record (its section 8).

Each of these conditions is defined in the linked corpus document that owns it, and their appearance in this scenario is not evidence that any of them operates in a given organization. Testing that is what the evidence classes below are for.

## Evidence to request

Each item below is an evidence class the governing body can call for from management, and each is evidence for a named control.

- **An affected-service inventory extract for the identity provider**, as evidence for the authoritative-inventory control in the [asset inventory register](../../operations/register-asset-inventory.md).
- **The dependency map for services that rely on the identity provider**, as evidence for the dependency-identification step of the [business impact analysis procedure](../../resilience/procedure-business-impact-analysis.md) (its Step 3) and the evidence class its evidence requirements name.
- **The incident record for the event**, as evidence for the incident documentation requirements of the [security incident response procedure](../../security/procedure-security-incident-response.md) (its section 8).
- **The IAM alert record and the associated log extract**, as evidence for the monitoring and alerting controls of the [logging and monitoring standard](../../security/standard-logging-and-monitoring.md) (its section 4.5) and the IAM event-logging requirement of the [identity and access management policy](../../security/policy-identity-and-access-management.md) (its section 4.7).
- **The privileged-access decision record for the accounts implicated**, as evidence for the privileged account lifecycle and incident response controls of the [privileged access management standard](../../security/standard-privileged-access-management.md) (its sections 5 and 6).
- **The joint decision log**, as evidence for the cross-stream decision control of the [cross-domain incident coordination procedure](../../resilience/procedure-cross-domain-incident-coordination.md) (its joint decision log section).
- **The evidence index for the incident**, as evidence for the evidence-preservation controls of the [security incident response procedure](../../security/procedure-security-incident-response.md) (its section 8) and the cross-stream evidence handling of the [coordination procedure](../../resilience/procedure-cross-domain-incident-coordination.md).
- **The recovery validation record**, as evidence for the recovery controls of the [security incident response procedure](../../security/procedure-security-incident-response.md) (its section 5) and the recovery-and-validation phase of the [coordination procedure](../../resilience/procedure-cross-domain-incident-coordination.md)'s coordination lifecycle.
- **The post-incident review for the event**, as evidence for the post-incident review control of the [security incident response procedure](../../security/procedure-security-incident-response.md) (its section 7).

## Limitations

- This scenario is illustrative and composite. It depicts no identifiable organization, no actual identity provider or product, and no real incident.
- This page makes no likelihood, frequency, or statistical claim, and none of its statements should be read as a probability, a frequency, or a magnitude.
- The compromise mechanism is left deliberately generic and is this page's construction for the telling. The corpus does not predict a mechanism, and this page makes no claim about which mechanisms occur in practice.
- This page creates no compliance and imposes no requirement. The linked corpus documents govern; where this page differs from a corpus document, the corpus document prevails.
- This page carries composite claims. The premise, the sequencing of the event across the identity, privileged-access, incident, logging, continuity, and coordination sources, and the whole of "What good looks like" are synthesized across the listed documents; no single corpus document states that sequence, and the adopting organization validates the reading against its own identity architecture and governance model.
- The corpus documents this page points to carry the specific values and closed sets: the identity and authentication requirements, the privileged-access controls and lifecycle contents, the incident severities, detection sources, response actions, and evidence-record contents, the alerting and review requirements, the recovery objectives and continuity requirements, and the coordination roles, lifecycle, and decision-log contents. This page routes to them and does not reproduce them.

**End of Document**
