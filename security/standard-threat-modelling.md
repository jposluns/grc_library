# Threat Modelling Standard

**Document Title:** Threat Modelling Standard\
**Document Type:** Standard\
**Version:** 1.0.5\
**Date:** 2026-07-07\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](policy-information-security.md), [`security/standard-penetration-testing-and-red-team.md`](standard-penetration-testing-and-red-team.md), [`security/procedure-vulnerability-management.md`](procedure-vulnerability-management.md), [`dev-security/policy-secure-development-and-engineering.md`](../dev-security/policy-secure-development-and-engineering.md), [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md), [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md)\
**Classification:** Public\
**Category:** Information Security\
**Review Frequency:** Annual and upon material change to the system's trust-boundary inventory, the threat-actor taxonomy, or the underlying STRIDE / LINDDUN methodology\
**Repository Path:** [`security/standard-threat-modelling.md`](standard-threat-modelling.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This standard defines how the organization conducts threat modelling: the structured analysis that identifies what an attacker could do to a system, where, and how, before that system is built or substantially changed. Threat modelling complements the Penetration Testing Standard (which validates controls in practice) and the Vulnerability Management Procedure (which addresses present, known weaknesses) by surfacing the design-level attack surface that those activities cannot reach.

The standard implements the STRIDE methodology applied per trust boundary, supplemented by abuse cases written alongside the use cases that drive functional requirements. It does not replace specialized methodologies for specific contexts (LINDDUN for privacy threats, PASTA for attack-simulation flow, OCTAVE for organizational risk); it provides the baseline approach the organization applies to every in-scope system unless a specialized methodology is justified.

---

## 2. Scope

This standard applies to:

1. New systems entering the architecture review process.
2. Material changes to existing systems that add a new trust boundary, change the data classification handled, or introduce a new external integration.
3. Systems undergoing acceptance-into-service review.
4. AI / agentic systems, including those that consume LLM output as a data source (LLM output is treated as a trust boundary; see also [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md)).

It does not duplicate the operational threat-actor profiling that the security operations function maintains as a living artefact; this standard governs the per-system design-time analysis that feeds into that operational picture.

---

## 3. Governance and accountability

| Role | Responsibility |
| --- | --- |
| **Chief Information Security Officer (CISO)** | Owns this standard; approves the threat-modelling methodology; reviews threat models for Tier 1 systems before acceptance into service. |
| **Application owner** | Initiates the threat-modelling activity for systems they own; signs off on identified threats and the response posture for each. |
| **Security architect or designate** | Facilitates the threat-modelling workshop; documents the trust-boundary map, the STRIDE per boundary, the abuse cases, and the disposition. |
| **Development team** | Participates in the workshop; produces the data-flow diagram that anchors the boundary identification; implements the disposition for in-scope threats. |
| **Internal audit** | Reviews threat-modelling completion as part of acceptance-into-service audit sampling. |

---

## 4. Methodology

### 4.1 Step 1: Map the trust boundaries

A trust boundary is any place where data crosses between zones whose levels of trust are not the same. The standard requires that the threat-modelling activity catalogue every boundary in scope for the system, at minimum:

| Boundary type | Examples |
| --- | --- |
| External network ingress | Public HTTP, public API, webhook receivers, file upload endpoints, email ingress |
| External network egress | Outbound API calls, webhook send, third-party service calls |
| User-to-system | Authentication boundary, session boundary, browser-to-server data exchange |
| System-to-system within the organization | Internal API calls, message queues, database connections, file-share access |
| Trust-level change within a system | Privilege escalation paths, role transitions, multi-tenancy boundaries |
| Operating-system boundary | Untrusted-code execution, container escape paths, hypervisor boundary |
| AI model boundary | LLM output consumed as data, model input from untrusted source, vector-store retrieval |
| Storage boundary | Encrypted-at-rest crossing, backup egress, off-system replication |

Each boundary is recorded with the classification of the data crossing it, the trust differential between the two sides, and the control responsible for mediating the boundary.

### 4.2 Step 2: Name the assets and the actors

For each system, the threat model names:

- **Assets worth protecting**: credentials, payment data, personal data, regulated data (per [`security/standard-data-classification-and-handling.md`](standard-data-classification-and-handling.md) classifications), trade secrets, signing keys, the integrity of administrative operations, the availability of the service.
- **Threat actors in scope**: external attackers (unauthenticated, authenticated low-privilege, supply-chain), internal authorized users (curious, malicious, coerced), automated agents (LLM output that the system trusts), platform actors (the cloud provider, the operating system, the runtime). The standard does not require modelling every conceivable actor; it requires that the actor list is justified for the system's risk profile.

### 4.3 Step 3: Apply STRIDE per boundary

For each boundary identified in Step 1, the workshop walks through the six STRIDE categories and records which are credible for that boundary, what the corresponding threat is, and what the response posture is.

| Category | Question | Example threat at an HTTP boundary |
| --- | --- | --- |
| **S**poofing | Can an attacker impersonate a legitimate principal across this boundary? | Bearer-token forgery, session fixation, JWT signature bypass |
| **T**ampering | Can an attacker modify data in transit or at rest across this boundary? | Parameter pollution, header injection, body modification of a webhook |
| **R**epudiation | Can an actor on either side deny an action they performed? | Missing audit log, replayable signed message, log-injection attack obscuring evidence |
| **I**nformation disclosure | Can an attacker read data they should not see across this boundary? | Verbose error response, debug endpoint, predictable resource enumeration, side-channel timing leak |
| **D**enial of service | Can an attacker degrade or stop the service through this boundary? | Unbounded resource consumption, slow-loris, amplification attack |
| **E**levation of privilege | Can an attacker gain privileges they should not have through this boundary? | Authorization bypass, IDOR, JWT scope manipulation, privilege confused-deputy |

For systems consuming LLM output (per [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md)), STRIDE is applied to the LLM-output boundary explicitly: the model is the spoofer, the tamperer, and the elevation-of-privilege actor. LLM output that flows into SQL, shell commands, file paths, HTML rendering, or evaluator functions is a STRIDE T (tampering) and E (elevation of privilege) candidate that the system designer cannot dismiss.

### 4.4 Step 4: Write abuse cases alongside use cases

Every use case in the requirements has a corresponding abuse case: the description of how an attacker would attempt to defeat or weaponize that use case. The abuse case is recorded in the same artefact as the use case, with the same identifier scheme (UC-001 has an accompanying ABC-001).

This step is the principal contribution that threat modelling makes to the development lifecycle: it forces the design phase to consider the adversarial perspective alongside the functional one.

### 4.5 Step 5: Disposition each identified threat

Each identified threat is assigned a disposition by the application owner with security-architect concurrence. The standard defines three response tiers:

| Tier | Meaning | Examples |
| --- | --- | --- |
| **Mandatory** | The threat is in scope and the corresponding control is required. The system cannot enter production without the control implemented and evidenced. | Input validation at external boundaries; parameterized database queries; password hashing with a vetted algorithm (per [`security/policy-encryption-and-key-management.md`](policy-encryption-and-key-management.md)); HTTPS enforcement; security headers; dependency vulnerability gates in CI; output encoding to defeat injection. |
| **Approval-Gated** | The threat is real and the chosen mitigation is a deviation from the standard pattern that requires explicit approval before the system enters production. | New authentication flow; new sensitive-data category; new external integration; CORS configuration that broadens the default; file-upload mechanism; rate-limit relaxation; permission grant to a new principal class. |
| **Prohibited** | The behaviour is forbidden regardless of the development team's preference. | Committing secrets to source control; logging unredacted sensitive data; trusting client-side validation as the only validation; disabling configured security headers; using dangerous evaluator functions with untrusted input; storing authentication tokens in browser-accessible client storage; exposing stack traces or framework version banners to unauthenticated users. |

The tier names are deliberately neutral: the standard does not negotiate the Mandatory tier per project, and the Prohibited tier is not subject to per-project waiver under the secure-development policy.

### 4.6 Step 6: Record the artefact

The threat model is recorded as a stand-alone artefact attached to the system's design documentation. The artefact includes:

- The data-flow diagram (or equivalent textual description) anchoring the trust-boundary map.
- The asset list, the actor list, and the STRIDE-per-boundary table.
- The abuse-case set alongside the use-case set.
- Each threat's disposition (tier and the named control or deviation approval).
- The signatures of the application owner and the security architect.
- The date of the workshop and the names of the participants.

The artefact is version-controlled with the system's design documentation and refreshed when the boundary inventory changes substantively.

---

## 5. Application to specific system types

### 5.1 Web applications and APIs

The web-stack OWASP Top 10 categorizes common findings, but it does not substitute for STRIDE-per-boundary analysis. A web application has an HTTP-ingress boundary that must be analyzed for all six STRIDE categories; the OWASP findings populate the threat list but do not define the boundaries. The [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md) controls implement the Mandatory-tier responses for the HTTP-ingress boundary by default.

### 5.2 AI / agentic systems

LLM output is a trust boundary. The agent's planner, executor, or tool-call mechanism that consumes model output must analyze the boundary for all six STRIDE categories. The model is the spoofing actor (prompt injection makes the model speak as if it were a different principal); the tampering actor (the model can rewrite the planner's intent); the elevation-of-privilege actor (the model can request capabilities the user did not authorize). Storage and retrieval boundaries for retrieval-augmented generation (RAG) are likewise in scope: the vector store is a boundary; poisoning is a tampering threat; cross-tenant retrieval is an information-disclosure threat. See [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md) for the AI-specific control taxonomy.

### 5.3 Multi-tenant systems

Multi-tenancy introduces a within-system trust boundary between tenants. Cross-tenant data access through a shared service is an information-disclosure threat that requires explicit modelling; "the application checks tenant ID on every query" is the Mandatory-tier control but is not self-evidently true and must be evidenced.

### 5.4 Privileged operations and administrative paths

Administrative APIs and privileged operations sit behind an internal trust boundary. STRIDE applied to that boundary surfaces the elevation-of-privilege paths that an attacker who has already authenticated as a low-privilege user might exploit. The [`security/standard-privileged-access-management.md`](standard-privileged-access-management.md) controls implement the Mandatory-tier responses.

### 5.5 Privacy-sensitive systems

Where the threat being modelled is privacy harm rather than (or as well as) security harm, the threat-modelling activity is supplemented by the LINDDUN methodology (Linkability, Identifiability, Non-repudiation, Detectability, Disclosure of information, Unawareness, Non-compliance). The disposition tier model in Step 5 applies to LINDDUN findings as well.

---

## 6. Triggers for re-modelling

A system's threat model is refreshed when any of the following occurs:

- A new trust boundary is added (a new external integration, a new tenant separation, a new privileged operation).
- The data classification handled changes (the system newly handles regulated, personal, or payment data).
- A new threat actor enters scope (a new partner integration, a public-facing surface added to a previously-internal system).
- A material change to the underlying STRIDE methodology or the LINDDUN methodology is published by its maintainer.
- A breach, near-miss, or red-team finding indicates the prior threat model missed a path the attacker exploited.
- Annual review per the Review Frequency field above.

---

## 7. Programme metrics

| Metric | Target |
| --- | --- |
| Percentage of Tier 1 systems entering acceptance into service with a current threat model | 100% |
| Percentage of threat models with named application-owner and security-architect signatures | 100% |
| Median time between trigger event and threat-model refresh | 30 days |
| Percentage of Mandatory-tier dispositions evidenced in production | 100% per system |
| Percentage of Prohibited-tier behaviours found in any production system | 0% |

---

## 8. Framework alignment

| Requirement | NIST SSDF | NIST SP 800-53 | ISO/IEC 27001:2022 | OWASP ASVS | CSA CCM |
| --- | --- | --- | --- | --- | --- |
| Design-time threat analysis | PW.1, PW.2 | SA-11, SA-15 | A.8.25, A.8.28 | V1.1 | AIS-04, CCC-06 |
| Documented data-flow diagrams | PW.1 | SA-15 | A.8.27 | V1.1 | CCC-04 |
| Boundary-level control mapping | PW.7 | SA-8, SA-11 | A.8.28 | V14.1 | IAM-02 |
| AI / model-output boundary in scope | PW.1, PW.6 | SA-11 | A.5.36 (controls assessment) | V14.1 | AIS-04 |
| Abuse-case authoring | PW.1, PW.6 | SA-11 | A.8.27 | V1.1 | CCC-06 |
| Privacy threat modelling (LINDDUN) | PO.1, PW.1 | PT-2, PT-3 | A.5.34 | V1.1 | DSP-02 |

---

## 9. References

The methodology rests on two long-standing public taxonomies:

- **STRIDE** (Microsoft): six-category threat taxonomy (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege). Introduced by Loren Kohnfelder and Praerit Garg in 1999; integrated into the Microsoft Security Development Lifecycle (SDL) Threat Modeling Tool documentation. See [`governance/register-canonical-citations.md`](../governance/register-canonical-citations.md) for the canonical reference.
- **LINDDUN** (KU Leuven imec-DistriNet): seven-category privacy threat taxonomy. See [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md) and [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../privacy/procedure-privacy-impact-and-cross-border-transfer.md) for the privacy-engineering application.

Supplementary frameworks the workshop may reference for specific contexts: OWASP ASVS (Application Security Verification Standard); OWASP Top 10 for LLM Applications; MITRE ATT&CK; MITRE ATLAS (for AI-system adversarial techniques); the OWASP Threat Modeling Cheat Sheet (data-flow and data-centric threat-modelling methodology).
