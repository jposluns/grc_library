# Fail-Closed Automation Principle

**Document Title:** Fail-Closed Automation Principle\
**Document Type:** Principle\
**Version:** 0.0.1\
**Date:** 2026-08-30\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/principle-capability-is-not-authority.md`](principle-capability-is-not-authority.md), [`security/framework-zero-trust-architecture.md`](../security/framework-zero-trust-architecture.md), [`operations/standard-network-security-and-segmentation.md`](../operations/standard-network-security-and-segmentation.md), [`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md), [`privacy/framework-privacy-by-design.md`](../privacy/framework-privacy-by-design.md), [`resilience/framework-business-continuity-and-resilience.md`](../resilience/framework-business-continuity-and-resilience.md), [`governance/principle-integrity-and-trustworthiness.md`](principle-integrity-and-trustworthiness.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material governance, AI, or regulatory change\
**Repository Path:** [`governance/principle-fail-closed-automation.md`](principle-fail-closed-automation.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This document states, in citable adopter-facing form, a foundational design principle for automated systems: **automation fails closed**. When an automated system encounters an error, an ambiguous input, or the loss of a condition its correct operation depends on, it enters a known, controlled, safe state rather than continuing into an unsafe or permissive one. The corpus already enforces this piecemeal (network default-deny, privacy-by-default, fail-closed handling of AI errors), but never states it as a principle a control can cite. This document makes it citable and generalizes it across every automated boundary.

It is the safe-state counterpart to [`principle-capability-is-not-authority`](principle-capability-is-not-authority.md): that principle fixes that a capability is never authority, and this one fixes that when the check cannot be made, the automated default is deny and halt, not allow and proceed.

## Scope

Applies to every automated decision, control, gateway, pipeline, and agent the corpus governs: access and network enforcement, AI and agentic actions, data-processing pipelines, deployment automation, and safety-relevant controls. It is a principle, not a control: it fixes the direction a system fails in, and it names the machinery that enforces that direction. The enforcing controls live in the access, network, resilience, privacy, and AI documents; this document does not restate them. It concerns the direction and controllability of failure, not the prevention of failure, which the resilience and testing disciplines address.

## 1. The principle

**Automation fails closed. On error, ambiguity, or loss of a required condition, an automated system enters a known, controlled, safe state rather than continuing into an unsafe or permissive one; degraded modes preserve safety, observability, and the ability to stop.**

Two readings are foreclosed:

- **A failure is not an implicit allow.** A check that cannot complete (a validation error, a timeout, an unreachable dependency, a malformed input) resolves to deny and halt, never to a permissive fall-through. "It broke, so it let everything through" is the failure this principle forecloses.
- **The safe state is defined, not emergent.** The state a system falls into is decided in advance and validated, not whatever state the failure happens to leave behind.

## 2. The facets of fail-closed automation

### 2.1 Known controlled state
The state an automated system enters on failure is specified in advance (a denial, a halt, a safe mode), and the transition into it is deterministic. An undefined or emergent post-failure state is itself a defect.

### 2.2 Safe over permissive
The direction of failure is toward the more protective outcome: deny rather than allow, halt rather than proceed, withhold rather than disclose. This composes with [`principle-capability-is-not-authority`](principle-capability-is-not-authority.md): where an authorization cannot be confirmed, the automated default is deny ([`security/framework-zero-trust-architecture.md`](../security/framework-zero-trust-architecture.md), [`operations/standard-network-security-and-segmentation.md`](../operations/standard-network-security-and-segmentation.md)).

### 2.3 Degraded modes preserve safety, observability, and stop-ability
A system that continues in a reduced or degraded mode still cannot leave its safety envelope, still emits the telemetry needed to observe its state, and still exposes the control needed to stop it. A degraded mode that goes dark or becomes unstoppable is not a safe degradation.

### 2.4 Tested, not assumed
The safe state and the transition to it are exercised and validated, not assumed to work. A fail-closed claim that has never been tested is an assumption, not a control.

## 3. Fail-open as a deliberate, authorized exception

In a minority of systems, availability itself is the safety property, and failing closed would cause the harm the system exists to prevent (the canonical case is a physical egress control that must release on a fire alarm). In those cases fail-open is a legitimate choice, but only when it is deliberate, authorized by the accountable owner, documented with its rationale, and bounded to the specific condition that justifies it. Fail-open is never the default, never implicit, and never the residue of an unhandled error; an unexamined fall-through to permissive is the defect this principle names, not an exercise of this exception.

## 4. Instantiation in the corpus

This principle is the statement of a rule the corpus already enforces piecewise.

| Instantiation | Corpus control | Facet |
| --- | --- | --- |
| Default-deny zone and perimeter rules | [`operations/standard-network-security-and-segmentation.md`](../operations/standard-network-security-and-segmentation.md) | Safe over permissive |
| Never trust, always verify (deny on unverified access) | [`security/framework-zero-trust-architecture.md`](../security/framework-zero-trust-architecture.md) | Safe over permissive |
| Fail closed on AI error or validation failure | [`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md) | Known controlled state |
| Privacy as the default (default-deny accessibility, conservative defaults, tested) | [`privacy/framework-privacy-by-design.md`](../privacy/framework-privacy-by-design.md) | Safe over permissive; tested not assumed |

## 5. Adoption guidance

An adopter reusing this library inherits fail-closed as the default failure direction for every automated control. To operationalize it: define, for each automated system, the known state it enters on failure, and make that state deny/halt unless a documented fail-open exception applies; require degraded modes to keep the safety envelope, telemetry, and a stop control; test the safe-state transition rather than assuming it; and treat any unexamined permissive fall-through as a defect. Where availability is genuinely the safety property, record the fail-open decision, its authority, and its bound. The principle is the "why" an adopter cites when asked why a broken check denies access rather than ignoring the failure.

## Framework alignment

The alignment below is analogical (each row aligns with or is informed by the cited reference) and at the control-family and category level, not a prescriptive crosswalk; the functional-safety references govern physical safety systems, whose fail-safe/safe-state concept this principle generalizes to automation broadly. NIST and ISO control identifiers are verified against held source texts; the IEC editions are confirmed against the canonical-citations register (their source texts are not held).

| Requirement | NIST SP 800-53 Rev. 5 | ISO/IEC 27001:2022 | NIST CSF 2.0 | Functional safety |
| --- | --- | --- | --- | --- |
| On failure, enter a known controlled (safe) state | SC-24 (Fail in Known State); CP-12 (Safe Mode) | A.5.29 (Information security during disruption) | PR.IR | IEC 61508:2010; IEC 61511:2016 |
| Fail toward the protective outcome (deny, halt) | SI-17 (Fail-safe Procedures) | A.8.20 (Networks security) | PR.IR | IEC 61508:2010 |
| Recover to a known-good state after a safe halt | CP-10 (System Recovery and Reconstitution) | A.5.29 (Information security during disruption) | RC.RP | IEC 61511:2016 |

NIST SP 800-53 SC-24 (Fail in Known State) is the primary reference for the known-controlled-state facet this principle expresses; IEC 61508 and IEC 61511 are the functional-safety root of the fail-safe concept the principle generalizes.
