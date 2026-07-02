# Release Management Procedure

**Document Title:** Release Management Procedure\
**Document Type:** Procedure\
**Version:** 1.0.2\
**Date:** 2026-07-02\
**Owner:** Chief Information Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`operations/framework-it-service-management.md`](framework-it-service-management.md), [`operations/procedure-change-management-and-configuration-control.md`](procedure-change-management-and-configuration-control.md), [`operations/standard-site-reliability-engineering.md`](standard-site-reliability-engineering.md), [`operations/standard-observability-and-telemetry.md`](standard-observability-and-telemetry.md), [`operations/procedure-patch-management.md`](procedure-patch-management.md), [`dev-security/standard-devops-security-requirements.md`](../dev-security/standard-devops-security-requirements.md), [`dev-security/procedure-secure-code-review.md`](../dev-security/procedure-secure-code-review.md), [`security/policy-acceptance-into-service.md`](../security/policy-acceptance-into-service.md)\
**Classification:** Public\
**Category:** IT Operations\
**Review Frequency:** Annual and upon material change to deployment platform, regulatory expectations, or release cadence\
**Repository Path:** [`operations/procedure-release-management.md`](procedure-release-management.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure governs the release of software, configuration, and infrastructure changes to production. It complements the change management procedure (which authorizes the change) and the secure code review procedure (which validates the artefact) by governing how changes move from acceptance to live operation safely, predictably, and reversibly.

---

## Scope

This procedure applies to:

1. Production deployments of organizationally-owned software.
2. Production configuration changes that are not strictly software (feature flags, configuration values, parameter changes).
3. Infrastructure-as-code releases to production.
4. AI artefact releases (model weights, prompts, retrieval-augmentation indices, tool definitions, evaluation suites that gate releases).
5. Vendor-supplied releases that the organization deploys (third-party patches, COTS upgrades).

It does not cover patches under the patch management procedure (which has its own cadence and risk class), although critical security patches may also use this procedure for the release mechanics.

---

## Procedure

### Step 1: Release planning

| Activity | Required output |
| --- | --- |
| Release scope | The set of artefacts in the release is named and frozen |
| Release class | Routine, expedited, standard, or emergency per the change management procedure |
| Customer impact | Expected customer impact assessed: no-impact, transparent, brief disruption, breaking |
| Communication plan | Internal communication; customer communication where the change is customer-visible |
| Window | Release window selected per the change calendar |
| Rollback plan | A tested rollback or forward-fix plan is documented |
| Acceptance criteria | Functional and non-functional acceptance criteria defined in advance |

### Step 2: Build and packaging

| Activity | Required output |
| --- | --- |
| Build provenance | Build originates from a known commit; build is reproducible or attested per the SLSA expectations |
| Artefact signing | Artefacts are signed; signatures verifiable at deployment |
| Software bill of materials | SBOM attached to the artefact per the SCA standard |
| Vulnerability gate | No critical or high vulnerabilities exceed the gate threshold without an exception |
| Container image | Aligned with the container and image security standard |
| Versioning | Semantic versioning or equivalent applied; release notes generated |

### Step 3: Pre-production validation

| Activity | Required output |
| --- | --- |
| Functional tests | Pass against the production-representative environment |
| Integration tests | Pass; cross-service contracts validated |
| Performance tests | Pass for material releases per the capacity and performance management standard |
| Security tests | SAST, DAST, dependency scanning, and IaC scanning gates passing |
| AI evaluation | For AI artefact releases, the evaluation suite passes per the AI evaluation procedure |
| Compliance gates | Privacy, regulatory, and licensing gates verified where applicable |
| Pre-flight checks | Production-readiness checklist signed off |

### Step 4: Authorization

| Activity | Required output |
| --- | --- |
| Change approval | Approval per the change management procedure |
| Production access | Privileged production access aligned with the PAM standard |
| Code-freeze checks | If a freeze applies, an exception is recorded |
| Sign-off | Named approver per the change class |
| AI release gate | Where the release is an AI artefact, the AI governance review for that release class is recorded |

### Step 5: Deployment

| Strategy | Description |
| --- | --- |
| Blue-green | New environment built in parallel; traffic switched on cut-over |
| Canary | Small percentage of traffic routed to new version; ramped on green-criteria |
| Rolling | Instances replaced incrementally |
| Recreate | Old stopped; new started; used only where downtime is acceptable |
| Feature flag | Code released dark and exposed via flag |
| Shadow | New version receives a copy of production traffic without affecting customers |

The strategy chosen matches the customer impact assessment and the rollback expectation.

| Activity | Required output |
| --- | --- |
| Deployment automation | Deployment is automated; manual steps are explicit exceptions |
| Telemetry pre-checks | Telemetry indicates pre-deployment baseline is healthy |
| Deploy operator role | A named role executes the deployment; not the change requester alone for material releases |
| Real-time monitoring | Deployer monitors metrics, errors, traces, and customer-experience signals during deployment |
| Halt criteria | Documented criteria that pause or roll back automatically |

### Step 6: Verification

| Activity | Required output |
| --- | --- |
| Smoke tests | Automated smoke tests pass post-deployment |
| Customer journeys | Critical customer journeys verified through synthetic checks |
| Telemetry comparison | Post-deployment telemetry compared to pre-deployment baseline; no regression beyond the gate threshold |
| AI behaviour spot-check | Where the release affects AI behaviour, a spot-check evaluates representative inputs |
| Sign-off | Verification signed off by the deploy operator and the on-call engineer |

### Step 7: Stabilization

| Activity | Required output |
| --- | --- |
| Observation window | Defined window during which the on-call team monitors for emergent issues |
| Customer-facing telemetry | Customer-impact telemetry observed; surges in support contacts treated as a signal |
| Anomaly response | Anomalies trigger investigation; rollback considered if criteria are met |
| Stabilization hand-off | Stabilization ends with a documented hand-off to standard operations |

### Step 8: Rollback or forward-fix

| Decision | Description |
| --- | --- |
| Rollback trigger | Pre-defined: customer impact, telemetry regression, security finding, regulatory concern |
| Rollback execution | Rollback executed via the pre-tested mechanism; not improvised |
| Forward-fix | Where rollback is not viable, a forward-fix is deployed under the same procedure on an expedited path |
| Post-rollback validation | Service health validated after rollback; customers informed if material |

### Step 9: Closure and learning

| Activity | Required output |
| --- | --- |
| Release record | The release record is closed; artefacts, approvals, telemetry, and outcome recorded |
| Customer communication | Final communication delivered where applicable |
| Lessons learned | Significant releases produce a lessons-learned record |
| Continuous improvement | Repeating release issues feed into platform and procedure improvements |

---

## Release classes

| Class | Approval | Gate adjustments |
| --- | --- | --- |
| Routine release | Standard change approval | Full automated gates |
| Expedited release | Documented expedited path; senior engineering approval | Full gates; reduced waiting |
| Emergency release | Emergency change approval; out-of-cycle senior approval | Minimum-viable gates; post-release reconciliation required |
| Standard repeatable release | Pre-authorized template; automated approval where templated | Templated gates |

---

## Roles

| Role | Responsibility |
| --- | --- |
| Release manager | Coordinates the release calendar; arbitrates conflicts; owns this procedure |
| Service owner | Owns the artefact being released and the outcome |
| Deploy operator | Executes the deployment |
| On-call engineer | Monitors during deployment and stabilization |
| Approver | Authorizes the release per its class |
| Communications owner | Owns customer and internal communication |
| AI governance reviewer | Reviews AI artefact releases per the AI release gate |

---

## Coordination with other procedures

| Procedure | Coordination point |
| --- | --- |
| Change management and configuration control | The release is a change; this procedure operates within that framework |
| Secure code review | Releases consist of artefacts whose changes have been reviewed |
| Patch management | Critical patches use this procedure's deployment mechanics |
| Incident response | An incident during release may suspend the release calendar |
| Acceptance into service | Initial release of a new service follows acceptance criteria first |
| Software composition analysis | SBOM and dependency findings are gates in this procedure |
| AI model lifecycle | AI artefact releases coordinate version-transition with this procedure |

---

## Tooling expectations

| Capability | Expected behaviour |
| --- | --- |
| Pipeline | Releases run through a versioned, auditable pipeline |
| Approvals | Approvals captured in the pipeline or in the change record |
| Artefact registry | Artefacts stored in a registry with retention and signing per the supply-chain controls |
| Deployment platform | Supports the selected deployment strategies |
| Telemetry integration | Pipeline annotates telemetry with deployment events |
| Rollback mechanism | Available, tested, and documented |
| Feature-flag platform | Flags have ownership and expiry; per the SRE standard |

---

## Operating expectations

1. Production releases run through this procedure; ad-hoc production changes are incidents.
2. Release cadence is reviewed quarterly; per-service cadence is tuned to risk and customer impact.
3. Rollback paths are exercised periodically; rollback that is documented but untested is not rollback.
4. Repeat failed releases trigger an architectural or process review.
5. Emergency releases are reconciled to standard practice within the post-release window.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ITIL 4 | Release management; deployment management | Service management |
| ISO/IEC 20000-1 | Service management requirements | Service management standard |
| ISO/IEC 27001:2022 | A.8.32 Change management | Information security |
| NIST SP 800-218 | SSDF PO, PS, PW, RV practices | Secure software development |
| OWASP SAMM | Verification, Operations | Software assurance maturity |
| Google SRE | Progressive rollouts; canary; error-budget gating | Reliability practice |
| DORA accelerate metrics | Deployment frequency, lead time, change failure rate, MTTR | Performance baseline |

---

## Limitations

This procedure is a CC BY-SA 4.0 baseline. Release practice is highly tooling-dependent; the procedure expresses requirements rather than vendor-specific implementations. Adopting organizations confirm current tooling and select deployment strategies appropriate to their architecture.

---

**End of Document**
