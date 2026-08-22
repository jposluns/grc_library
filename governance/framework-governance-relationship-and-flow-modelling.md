# Governance Relationship and Flow Modelling Framework

**Document Title:** Governance Relationship and Flow Modelling Framework\
**Document Type:** Framework\
**Version:** 1.0.5\
**Date:** 2026-08-22\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/charter-governance-library.md`](charter-governance-library.md), [`governance/framework-document-architecture-and-interrelationship.md`](framework-document-architecture-and-interrelationship.md), [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md), [`governance/register-key-terms-and-definitions.md`](register-key-terms-and-definitions.md), [`governance/matrix-cross-framework-alignment.md`](matrix-cross-framework-alignment.md), [`architecture/framework-enterprise-architecture.md`](../architecture/framework-enterprise-architecture.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material change to the relationship vocabulary\
**Repository Path:** [`governance/framework-governance-relationship-and-flow-modelling.md`](framework-governance-relationship-and-flow-modelling.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This framework standardizes how governance, risk, and compliance entities are modelled as directed relationships. It defines a relationship grammar, a node-class taxonomy, a controlled verb vocabulary, a set of declared viewpoints, direction and placement rules, and a validation method, so that a relationship asserted anywhere in this library, or in an adopting organization's own registers and matrices, is precise, directional, testable, and free of the ambiguity that vague linkage language such as `relates to` produces.

The framework's central position is that governance entities have no single universal hierarchy. A regulation, a framework, a policy, a control, and an asset order differently depending on the question being asked. Placement is therefore contextual: every rendered view of a relationship model declares the viewpoint it answers and the direction rule it places by, and the same entities may legitimately occupy different layers in different views.

The framework is a modelling method, not a data platform. It introduces no new document type and mandates no generated artefact or validation tooling on an adopter; the library does maintain a generated model of its own relationship-source records, validated by a regeneration gate. It gives authors and adopters a shared vocabulary and a repeatable validation discipline, and it gives adopters guidance for building their own rendered diagrams or graph representations from the text form this library uses.

---

## Scope

This framework applies to relationship modelling across all repository domains: `governance`, `risk`, `compliance`, `security`, `ai`, `operations`, `resilience`, `privacy`, `supply-chain`, and `dev-security`.

It governs the modelling of governance entities generally: authorities, regulations, contractual requirements, frameworks, standards, policies, procedures, control objectives, controls, assets, processes, risks, evidence, assessments, and findings. Corpus documents are one class of governance entity among many; this framework is not limited to documents.

Document-type selection, document-to-document relationship rules, and the document hierarchy of this library remain governed by the [`governance/framework-document-architecture-and-interrelationship.md`](framework-document-architecture-and-interrelationship.md) framework. This framework places that hierarchy in context (see the viewpoints section) and delegates all document-type layering to it.

Three exclusions bound this version:

- All relationship representations inside this library are text form. The library embeds no rendered diagrams; diagram generation is adopter guidance only.
- The single machine-readable relationship record in this document is illustrative and non-normative. No schema is mandated on an adopter's records, and no gate validates them; the library does maintain and validate a generated model of its own relationship-source records (the audit programme's relationship-model sync gate), which imposes nothing on an adopter.
- The framework defines no exhaustive node-by-verb compatibility matrix. Compatibility is expressed at the category level in the verb table, and the validation method carries the per-assertion judgement.

---

## Normative language

In this document the lowercase terms `must`, `must not`, `should`, and `may` express requirement force. The term `must` states an obligation, `must not` states a prohibition, `should` states a strong recommendation that a documented reason may set aside, and `may` states a permitted option.

Requirement force appears only in prose. Fenced examples, including every flow example and the illustrative record, are non-normative illustrations and carry no requirement force.

When this document discusses a relationship verb as a vocabulary token rather than using it in a sentence, the token appears in backticks, for example `implements`.

---

## Core principles

1. **No universal hierarchy.** Governance entities must not be forced into a single fixed ordering. In particular, frameworks and policies have no universal relative rank: an adopted framework sits above the policy it shapes in one view and below the policy that gives it force in another.
2. **Declared viewpoint.** Every rendered view must declare the viewpoint it answers and the primary direction rule it places by, before any node is placed. A view with no declared viewpoint is not evaluable and must not be published.
3. **Directed, active-voice form.** Every relationship must be a directed assertion in which a source performs a controlled verb on a destination, stated in active voice.
4. **Primary edges place, associative edges annotate.** Primary relationships determine node placement in a rendered view. Associative relationships add context, may cross layers, and must not determine placement.
5. **Inverses are inferred by default.** Every directed relationship implies an inverse reading, and the inverse is inferred, not stored. Storing an inverse as its own record requires a recorded justification, such as a recurring navigation need.
6. **Natures stay distinguishable.** A relationship carries at least 1 of 5 natures: structural, inferred, assessed, temporal, or evidence-dependent. A relationship may carry several natures at once, and a model must keep the natures distinguishable rather than flattening them into undifferentiated edges.
7. **Assessed outcomes require support.** A relationship expressing compliance, satisfaction, fulfilment, conformance, or effectiveness must carry evidence, the assessment that established it, a validity period, and a scope. Such a relationship must never be recorded as a permanent structural fact.
8. **Controlled vocabulary.** Every approved verb has a controlled definition, a relationship class, typical source and destination categories (typical rather than strict, since a node's multi-category membership can license a departure in a declared viewpoint), and an inverse reading. A verb outside the controlled set must not appear in a relationship assertion until it is added through the lifecycle process in this document.
9. **Orthogonal dimensions.** Node class, functional category, authority origin, binding force, and layout layer are independent dimensions of a model. Layer is a property of the view, never of the node: no node class carries an intrinsic layer.

---

## Node-class taxonomy

Node classes group into 7 categories. The categories describe function; they carry no intrinsic ordering and no intrinsic layer (principle 9). The short name in the first column is the token the verb table uses.

| Category | Member node classes | Typical role in views |
| --- | --- | --- |
| 1. Authority (external authority and obligation) | Authority, regulator, standards body, regulation or law, contractual requirement, regulatory guidance | The origin of binding force in authority and applicability views |
| 2. Sources (interpretive and normative sources) | Framework, standard, benchmark, guideline, control catalogue | Interpreted or adopted direction in governance and authority views |
| 3. Governance (organizational governance) | Policy, organizational standard, procedure, control objective, risk appetite, exception | Internal direction in governance and implementation views |
| 4. Context (scope and operating context) | Macro-domain, sector, organization, business process, asset, application, workload, data | The scope that obligations and risks attach to |
| 5. Implementation | Administrative control, technical control, physical control, process, configuration, safeguard | The operating layer in implementation, assurance, and risk views |
| 6. Risk | Threat, vulnerability, risk, residual risk | The subject of the risk view |
| 7. Assurance (assurance and outcome) | Evidence, assessment, finding, compliance status | The record and conclusion layer in the assurance view |

A node may belong to more than 1 category, and the same class may carry different functional readings in different contexts: a standard, for example, may be external or internal, mandatory or voluntary, and regulatory, contractual, or organizational in origin. The taxonomy records function only. Authority origin and binding force are properties of relationships and of the authority level recorded on them, so the taxonomy needs no separate class for each binding status.

---

## Relationship form and controlled verb vocabulary

Every relationship is a directed assertion in the form shown below. The source performs the verb on the destination.

```text
SOURCE VERB DESTINATION
```

Assertions must use active voice. Passive constructions conceal the acting entity and are prohibited in relationship assertions (see the anti-patterns section).

### Controlled verb set

The 18 verbs below are the controlled structural vocabulary of this framework. Each row records the verb's definition, its relationship class, its typical source and destination categories (using the taxonomy's short names), its typical layout role, and its inferred inverse reading. The source and destination categories are typical rather than strict: a node's multi-category membership can license a departure in a declared viewpoint, so a mandatory standard, which also carries authority force, may act as the source of a `requires` edge in the authority view. The layout-role column records the typical role only; the operative role is decided per view, and a verb that is associative in most views may be primary in the view whose question it answers.

| Verb | Definition | Relationship class | Typical source to destination | Typical layout role | Inverse reading (inferred) |
| --- | --- | --- | --- | --- | --- |
| `issues` | An authority puts an instrument into force. | Authority | Authority to authority or sources | Primary | Is issued by |
| `mandates` | A source compels adoption of a destination instrument within a scope. | Authority | Authority or governance to sources | Primary | Is mandated by |
| `requires` | A source makes a specific destination obligatory. | Requirement | Authority or governance to governance or implementation | Primary | Is required by |
| `applies to` | A source is applicable within a declared scope. | Applicability | Authority, sources, governance, or risk to context | Primary | Is subject to |
| `contains` | A source structurally comprises a destination as a part. | Containment | Same-category composition (sources to sources, context to context) | Primary | Is contained in |
| `defines` | A source establishes the meaning or existence of a destination. | Definition | Sources or governance to governance | Primary | Is defined by |
| `specifies` | A source states a destination precisely enough to test against. | Specification | Sources or governance to governance or implementation | Primary | Is specified by |
| `implements` | An implementation entity puts a requirement into operation. | Implementation | Implementation to governance | Primary | Is implemented by |
| `enforces` | A mechanism compels conformance with a destination in operation. | Implementation | Implementation to governance | Primary | Is enforced by |
| `produces` | An operating source generates a destination record. | Evidence generation | Implementation or assurance to assurance | Primary | Is produced by |
| `demonstrates` | Evidence exhibits the operation or a property of a destination. | Assurance | Assurance to implementation or assurance | Primary in the assurance view | Is demonstrated by |
| `assesses` | An assurance activity evaluates a destination. | Assurance | Assurance to implementation, risk, or assurance | Primary in the assurance view | Is assessed by |
| `determines` | An assurance conclusion establishes a destination status. | Assurance | Assurance to assurance or risk | Primary in the assurance view | Is determined by |
| `mitigates` | A treatment reduces a destination risk. | Risk treatment | Implementation to risk | Primary in the risk view | Is mitigated by |
| `informs` | A source shapes a destination without mandating it. | Influence | Sources or assurance to governance or assurance | Associative | Is informed by |
| `references` | A source cites a destination without adopting or requiring it. | Citation | Any category to any category | Associative | Is referenced by |
| `adopts` | An organization voluntarily commits to a destination source. | Commitment | Governance or context to sources | Associative | Is adopted by |
| `maps to` | A source is cross-referenced to a destination for traceability. | Correspondence | Sources to authority or sources | Associative | Is mapped from |

### Distinction clusters

The following clusters separate verbs that untrained usage treats as interchangeable. Choosing within a cluster is the verb-precision test in practice.

- **`defines`, `specifies`, and `prescribes`.** Use `defines` when the source establishes what the destination is, and `specifies` when the source states the destination precisely enough to test against. The token `prescribes` is not in the controlled set: normalize it to `requires` when force is meant and to `specifies` when precision is meant.
- **`requires` and `recommends`.** Use `requires` only for obligation. Advisory force is carried by `informs`; an adopter who needs a distinct advisory-requirement edge registers `recommends` through the lifecycle process rather than overloading `requires`.
- **`informs`, `references`, and `adopts`.** A source `informs` a destination when it shapes the destination's content, `references` it when it merely cites it, and an organization `adopts` a source when it voluntarily commits to it. Influence, citation, and commitment are 3 different assertions with 3 different consequences.
- **`maps to` and `aligns with`.** Use `maps to` for an identifier-level cross-reference maintained for traceability. The token `aligns with` asserts a broader consistency judgement, which is an assessed outcome, not a structural fact: record it, if at all, only as an assessed-nature relationship with evidence and validity, per the next subsection.
- **`implements` and `enforces`.** An implementation entity `implements` a requirement when it puts the requirement into operation, and `enforces` it when it compels conformance at run time. A policy interpreting a framework does neither: interpretation is `adopts` or the inverse reading of `informs`, which is why `implements` typically takes an implementation-category source, the operationalization test rather than a strict category rule being what excludes pure interpretation. A governance document that operationalizes a higher instrument, an organizational standard putting a policy into operation or a procedure putting a standard into operation, acts in that implementation capacity (a multi-category reading, since a node may belong to more than one category) and is a valid `implements` source; a document that merely interprets does not operationalize and uses `adopts` or `informs` instead.
- **`verifies`, `validates`, and `demonstrates`.** Verification (checking against a specification) and validation (checking fitness for purpose) are assessment activities: model both with `assesses` and record the check type on the assessment. What evidence does is `demonstrates`. Prefer `demonstrates` over `evidences`.

### Rejected and normalized verbs

- `relates to`, `is associated with`, and every other undirected linkage token are prohibited. They assert nothing testable: no direction, no class, no consequence.
- `covers` and `includes` normalize to `contains` when composition is meant and to `applies to` when applicability is meant. The 2 meanings must not share a verb, because containment and applicability answer different validation tests.
- `evidences` normalizes to `demonstrates`.
- `prescribes` and `recommends` normalize as stated in the distinction clusters above.

### Assessed outcomes are not structural edges

The tokens `satisfies`, `fulfils`, `conforms to`, `complies with`, and `meets` are part of this framework's controlled set alongside the 18 structural verbs, so principle 8's prohibition on out-of-set verbs does not exclude them; they form a distinct assessed-outcome group with a shared controlled contract: their relationship class is assessed outcome, they typically take an implementation-category or governance-category source and a governance-category or authority-category destination, and their inverse reads `is satisfied by`, with `is fulfilled by`, `is conformed to by`, `is complied with by`, and `is met by` as the parallel readings, inferred by default like any inverse (principle 5). They are governed by the conditions below. They express assessed or inferred outcomes. Each depends on evidence, on the assessment that established it, on time, and on scope, and each decays as the implementation, the requirement, or the environment changes. A relationship using any of these verbs must carry the assessed nature, at least 1 evidence reference, a validity period, and the scope within which it was established, and it must never be recorded as a permanent structural edge. A model that stores a control-`satisfies`-objective assertion as a timeless fact has converted an assessment result into an architecture claim, which is the root of several anti-patterns in this framework.

---

## Viewpoints

A viewpoint is the question a rendered view answers. This framework defines 6 viewpoints. Each is a common pattern, not a universal hierarchy: the pattern describes how entities typically order under that question, and a modeller may depart from it where the declared direction rule and the validation tests are still satisfied.

The document hierarchy in [`governance/framework-document-architecture-and-interrelationship.md`](framework-document-architecture-and-interrelationship.md) is the document-architecture viewpoint of this library: a layering of document types within the governance viewpoint, one viewpoint among several, and not a universal ordering of governance entities. That framework remains authoritative for document-type selection and document-to-document relationships; this framework governs entity relationship modelling generally, and the worked application section shows the 2 operating together. For architecture viewpoints applied to systems rather than governance entities, see the architecture viewpoints section of [`architecture/framework-enterprise-architecture.md`](../architecture/framework-enterprise-architecture.md).

### Authority viewpoint

- **Primary question:** who creates, issues, mandates, or governs a requirement, and what gives it force?
- **Typical node categories:** authority, sources, governance.
- **Primary direction rule:** the entity that confers force places above the entity that receives it.
- **Typical relationship classes:** primary: authority and requirement (`issues`, `mandates`, `requires`); associative: commitment and correspondence (`adopts`, `maps to`).

```text
viewpoint: authority
direction rule: the entity that confers force places above the entity that receives it

REGULATOR issues REGULATION                  (primary, with-primary)
REGULATION mandates SECTOR_STANDARD          (primary, with-primary)
SECTOR_STANDARD requires CONTROL_OBJECTIVE   (primary, with-primary)
POLICY adopts VOLUNTARY_FRAMEWORK            (associative)
```

### Applicability viewpoint

- **Primary question:** what applies to a domain, sector, organization, process, asset, application, workload, or data set, and under what condition?
- **Typical node categories:** authority, sources, governance, context.
- **Primary direction rule:** the source of applicability places above the scope it reaches.
- **Typical relationship classes:** primary: applicability and containment (`applies to`, `contains`); associative: requirement (`requires`, rendered as context rather than placement).

```text
viewpoint: applicability
direction rule: the source of applicability places above the scope it reaches

REGULATION applies to SECTOR             (primary, with-primary)
SECTOR contains ORGANIZATION             (primary, with-primary)
ORGANIZATION contains BUSINESS_PROCESS   (primary, with-primary)
REGULATION requires CONTROL_OBJECTIVE    (associative in this view)
```

### Governance viewpoint

- **Primary question:** how do external obligations and recognized practices become internal direction?
- **Typical node categories:** sources, governance.
- **Primary direction rule:** interpreted sources place above the internal instruments that respond to them.
- **Typical relationship classes:** primary: influence, requirement, and specification (`informs`, `requires`, `specifies`); associative: commitment and citation (`adopts`, `references`). Influence renders as primary here because interpretation is this view's subject.

```text
viewpoint: governance
direction rule: interpreted sources place above the internal instruments that respond to them

EXTERNAL_FRAMEWORK informs POLICY                     (primary in this view, with-primary)
POLICY requires ORGANIZATIONAL_STANDARD               (primary, with-primary)
ORGANIZATIONAL_STANDARD specifies CONTROL_OBJECTIVE   (primary, with-primary)
PROCEDURE implements ORGANIZATIONAL_STANDARD          (primary, against-primary)
```

### Implementation viewpoint

- **Primary question:** how are requirements put into operation in processes and technology?
- **Typical node categories:** governance, context, implementation.
- **Primary direction rule:** the requirement places above the entities that put it into operation.
- **Typical relationship classes:** primary: specification, implementation, and applicability (`specifies`, `implements`, `enforces`, `applies to`); associative: citation (`references`).

```text
viewpoint: implementation
direction rule: the requirement places above the entities that put it into operation

ORGANIZATIONAL_STANDARD specifies CONTROL_OBJECTIVE   (primary, with-primary)
TECHNICAL_CONTROL implements CONTROL_OBJECTIVE        (primary, against-primary)
TECHNICAL_CONTROL applies to WORKLOAD                 (primary, with-primary)
CONFIGURATION enforces ORGANIZATIONAL_STANDARD        (primary, against-primary)
```

### Assurance viewpoint

- **Primary question:** does the implementation operate, and what do the records establish?
- **Typical node categories:** implementation, assurance.
- **Typical relationship classes:** primary: evidence generation and assurance (`produces`, `assesses`, `demonstrates`, `determines`); associative: influence (`informs`).
- **Primary direction rule:** assurance flows from operation to conclusion; operating entities place first and conclusions last.

```text
viewpoint: assurance
direction rule: assurance flows from operation to conclusion

TECHNICAL_CONTROL produces EVIDENCE    (primary, with-primary)
ASSESSMENT assesses EVIDENCE           (primary, against-primary)
ASSESSMENT produces FINDING            (primary, with-primary)
FINDING determines COMPLIANCE_STATUS   (primary, with-primary)
```

### Risk viewpoint

- **Primary question:** which threats and vulnerabilities create which risks, what treats them, and what remains?
- **Typical node categories:** risk, implementation, context, assurance.
- **Primary direction rule:** causation and treatment flow toward residual risk.
- **Typical relationship classes:** primary: risk treatment, applicability, and assurance (`mitigates`, `applies to`, `determines`); associative: assurance input (`assesses`). The focused vocabulary covers treatment and determination; an adopter modelling the full causal chain, for example an `exploits` edge from threat to vulnerability, registers the additional verbs through the lifecycle process.

```text
viewpoint: risk
direction rule: causation and treatment flow toward residual risk

RISK applies to BUSINESS_PROCESS        (primary, with-primary)
TECHNICAL_CONTROL mitigates RISK        (primary, against-primary)
ASSESSMENT assesses TECHNICAL_CONTROL   (associative in this view)
ASSESSMENT determines RESIDUAL_RISK     (primary, with-primary)
```

---

## Direction and placement rules

**Direction is semantic.** An edge's direction follows from its grammar: the source performs the verb on the destination. Direction must never be reversed for layout convenience. A view that renders flow in the opposite visual order changes its direction rule, which is a placement convention of the view, and leaves every stored edge untouched.

**Two assertions are 2 edges.** When 2 entities relate in both directions, the 2 readings are distinct assertions with distinct verbs, classes, and natures, never a single edge drawn both ways. The pair below is the canonical example: the assessment acting on the record, and the record shaping the assessment, are different facts.

```text
ASSESSMENT assesses EVIDENCE   (primary in the assurance view; the activity acts on the record)
EVIDENCE informs ASSESSMENT    (associative; the record shapes the activity's conclusion)
```

**Direction roles.** Every rendered edge carries 1 of 4 direction roles relative to the view's declared direction rule:

- **With-primary:** a primary edge whose semantic direction matches the rendered flow.
- **Against-primary:** a primary edge whose semantic direction opposes the rendered flow. The view places its nodes by the edge's inferred inverse reading; the stored edge keeps its semantic direction. A procedure-`implements`-standard edge in a top-down governance view is the standing example.
- **Lateral:** an edge between peers of the same layer in the current view.
- **Cross-layer:** an associative edge that skips layers. Cross-layer edges are permitted and must not determine placement.

**Contextual vertical dominance.** Because layer is a property of the view (principle 9), vertical order between the same 2 entities may legitimately differ between views. The recurring case is an adopted external framework and the internal policy that adopts it: the framework places above the policy in the governance view and below it in the authority view. The worked application section renders the pair; neither view contradicts the other, because each declares the question it answers.

---

## Relationship validation method

Every asserted relationship must pass the 9 tests below before it enters a register, a matrix, a rendered view, or a machine-readable record. The tests are a review method for authors and reviewers; the library additionally mechanizes several of them as build-time validation rules over its own relationship-source records (the audit programme's relationship-model sync gate), fatally covering the cycle, structural-fact, verb-precision, temporal-validity, and evidence tests, with the source-action test applied as an advisory category check; an adopter applies all nine as a review method.

1. **Source-action test.** Can the source, as classed, logically perform the verb on the destination? An assertion whose source cannot perform the action fails regardless of how familiar the pairing reads.
2. **Direction test.** Does the assertion run in the semantic direction the verb defines? An edge written backward to suit a diagram fails this test by construction.
3. **Cycle test.** Would the edge create a directed cycle among the primary edges of a single declared viewpoint within a single context (time, jurisdiction, scope)? The test applies to that filtered slice only, never to the union of all views: a cycle formed only across different viewpoints, or only when associative edges are included, is not a defect. This context-slice rule is what prevents the false cycle findings a whole-model check produces.
4. **Structural-fact test.** Is the relationship an enduring structural fact, or does it depend on evidence, assessment, time, version, jurisdiction, or scope? Dependence is not a defect; it means the edge must carry the matching natures and supporting fields rather than posing as structural.
5. **Verb-precision test.** Is the verb the most precise controlled token available? A vague verb where a distinction cluster offers a sharper one fails; a verb outside the controlled set fails until registered.
6. **Cardinality test.** Is the assertion's cardinality (1-to-1, 1-to-many, many-to-1, many-to-many) stated or evident, and consistent with the classes involved?
7. **Temporal-validity test.** Does the relationship carry the effective date, expiry, version, jurisdiction, and sector conditions it depends on? Supersession of one instrument version by another is a temporal relationship; an adopter who needs an explicit `supersedes` edge registers it through the lifecycle process.
8. **Authority test.** What force does the relationship carry? Use the alignment-type vocabulary the [`governance/matrix-cross-framework-alignment.md`](matrix-cross-framework-alignment.md) matrix already carries (legal obligation, regulatory interpretation, contractual requirement, industry practice, architectural recommendation, evidence category), extended with the 2 force levels internal to an organization: organizationally mandatory and organizationally recommended. A parallel authority taxonomy must not be invented. Binding force is orthogonal to a relationship's nature (principle 9): an assessed edge still carries one of these forces, and `assessed` names the nature, never the force.
9. **Evidence test.** Does establishing, validating, or maintaining the relationship require evidence? Every assessed-nature edge does, and the evidence references must be recorded on the edge.

---

## Anti-patterns

Each pattern below records a recurring modelling failure and the correction this framework requires.

1. **Treating a mapped control as implemented.** A `maps to` correspondence establishes traceability only. Implementation is a separate `implements` assertion with its own validation.
2. **Treating an implemented control as effective.** Implementation is structural; effectiveness is an assessed outcome that requires evidence and an assessment, and it decays.
3. **Treating an effective control as sufficient.** Effectiveness against one objective says nothing about the other obligations that apply in scope; sufficiency is a per-obligation judgement.
4. **Treating a reference as a requirement.** `references` carries no force. Escalating a citation into an obligation fails the authority test.
5. **Treating adoption as compliance.** `adopts` records a voluntary commitment. Compliance is an assessed outcome against the adopted source, established by assessment and evidence.
6. **Treating compliance as static.** A compliance status without a validity period and supporting evidence is a stale claim, not a fact.
7. **Passive voice in assertions.** `is required by` as a stored form conceals the acting entity and inverts direction silently. Passive readings exist only as inferred inverses.
8. **Cycles among primary edges.** A directed cycle within one viewpoint's primary slice makes placement undecidable and almost always signals a verb-precision or direction error.
9. **Forcing a universal order.** Ranking frameworks and policies (or any other entity pair) once for all purposes erases the contextual placement this framework exists to preserve.
10. **Overloading `implements`.** Using one verb for both governance interpretation and technical deployment collapses the governance and implementation viewpoints into each other.
11. **Vague verbs.** `relates to` and its equivalents assert nothing that any of the 9 tests can evaluate.
12. **Confusing containment with applicability.** `contains` states composition; `applies to` states reach. Interchanging them corrupts both the applicability view and the cycle test's slice.

---

## Worked corpus application

### The document-architecture viewpoint

This library's own document layering, Charter to Framework to Policy to Standard and onward, is the governance viewpoint specialized to document types. The document-type nodes map onto the taxonomy: a framework and a guideline are interpretive and normative sources (category 2), a policy, an organizational standard, and a procedure are organizational governance (category 3), and a charter is the organizational-governance root that the sibling framework treats as the repository-root authority anchor. They are the document-architecture viewpoint's rendering, not new node classes. Rendered in this framework's form:

```text
viewpoint: governance (document-architecture specialization)
direction rule: direction-setting documents place above the documents that carry their direction out

CHARTER defines FRAMEWORK                      (primary, with-primary)
FRAMEWORK defines POLICY                       (primary, with-primary)
ORGANIZATIONAL_STANDARD implements POLICY      (primary, against-primary)
PROCEDURE implements ORGANIZATIONAL_STANDARD   (primary, against-primary)
GUIDELINE informs PROCEDURE                    (associative)
```

These edges carry the derive-and-implement semantics the document hierarchy records, not a mandate. The `defines` edges read as derivation: a policy derives its architectural context from a framework, and a framework from the charter, so the definer places above. The framework does not compel a policy to exist, and a policy does not compel a standard; the sibling establishes that a policy is derived from a framework and a standard implements a policy, which is why the `requires` verb would misstate the relationship here. The `implements` edges keep their semantic direction: a standard implements a policy and a procedure implements a standard, so the view places each implementer below by the inferred inverse reading. The full document hierarchy table in [`governance/framework-document-architecture-and-interrelationship.md`](framework-document-architecture-and-interrelationship.md) is this viewpoint elaborated to document-type granularity, and it remains authoritative at that granularity.

### The contextual placement pair

The same 2 entities, an internal policy and the external framework it adopts, order oppositely in 2 legitimate views.

```text
viewpoint: governance
direction rule: interpreted sources place above the internal instruments that respond to them

EXAMPLE_FRAMEWORK_A informs ACCESS_POLICY   (primary in this view, with-primary)
ACCESS_POLICY adopts EXAMPLE_FRAMEWORK_A    (associative)
```

```text
viewpoint: authority
direction rule: the instrument that carries binding force places above what it binds

ACCESS_POLICY mandates EXAMPLE_FRAMEWORK_A   (primary, with-primary)
ACCESS_POLICY applies to ORGANIZATION        (primary, with-primary)
```

Both views are simultaneously correct. In the governance view the framework shapes the policy's content, so it places above. In the authority view a voluntarily adopted framework binds nobody by itself; the policy is what confers force on it in scope, so the policy places above. A modeller who forces these into a single order either overstates the framework's authority or erases its influence, and the declared viewpoints are what keep the pair from reading as a cycle: the cycle test evaluates each view's primary slice separately.

### A justified stored inverse

The library's own matrices illustrate the inverse-storage rule. The forward `maps to` assertions live in [`governance/matrix-cross-framework-alignment.md`](matrix-cross-framework-alignment.md), and [`governance/matrix-reverse-framework-control-crosswalk.md`](matrix-reverse-framework-control-crosswalk.md) stores the inverse reading as a separate navigation view because reverse lookup is a recurring adopter task: that recurring need is precisely the recorded justification principle 5 requires before an inverse is stored rather than inferred.

---

## Illustrative machine-readable relationship record

The record below is non-normative. It is a starting point for an adopter who wants to hold relationship assertions in a register, a traceability tool, or a graph database, and it is deliberately expressed with placeholder identifiers: no real standard, control, or framework identifier appears, and no third-party text is reproduced. This library mandates no schema on an adopter's records. It does validate its own relationship-source records through a regeneration gate, but that governs the library's records alone; an adopter's records carry no such requirement.

The example deliberately records an assessed outcome, the most demanding case, because it shows every field that principle 7 and the assessed-outcome subsection place on such an edge: the assessed nature, the evidence, the assessment provenance, the validity window, and the scope within which it was established. A structural edge would omit the evidence and validity content and carry the structural nature alone.

```yaml
# Non-normative illustrative record. Placeholder identifiers only; this is an
# adopter starting point, not a corpus requirement and not a real mapping.
id: rel-example-0001
source:
  id: EXAMPLE-CONTROL-01
  class: technical control
verb: satisfies
destination:
  id: EXAMPLE-OBJECTIVE-01
  class: control objective
relationship_class: assessed outcome
layout_role: associative
nature:
  - assessed
  - temporal
  - evidence-dependent
viewpoint: assurance
direction_rule: the asserting entity points to the requirement whose satisfaction is asserted
inverse:
  verb: is satisfied by
  storage: inferred
validity:
  from: 2026-01-01
  to: null
authority_level: evidence category
evidence_refs:
  - EXAMPLE-EVIDENCE-01
provenance: EXAMPLE-ASSESSMENT-01
scope: EXAMPLE-SCOPE-01
status: active
```

| Field | Meaning |
| --- | --- |
| `id` | Stable identifier of the relationship record itself. |
| `source`, `destination` | The 2 endpoints, each with an identifier and a node class. |
| `verb` | The relationship verb. A structural edge uses a structural verb; an assessed-outcome verb (here `satisfies`), also part of the controlled set, is permitted only when the natures and supporting fields below accompany it. |
| `relationship_class` | The class the verb belongs to (authority, requirement, applicability, containment, definition, specification, implementation, evidence generation, assurance, risk treatment, influence, citation, commitment, correspondence, or assessed outcome). |
| `layout_role` | Whether the edge places nodes (primary) or annotates (associative) in the declared viewpoint. |
| `nature` | One or more of: structural, inferred, assessed, temporal, evidence-dependent. |
| `viewpoint` | The declared viewpoint under which the record was validated. |
| `direction_rule` | The placement rule the validating view declared. |
| `inverse` | The inverse reading and its storage disposition; `inferred` is the default, and a stored inverse carries a justification instead. |
| `validity` | ISO 8601 effective and expiry dates; an open end is `null`, never an empty string. |
| `authority_level` | The force the edge carries, from the authority test's vocabulary. |
| `evidence_refs` | Identifiers of the evidence supporting an assessed or evidence-dependent edge. |
| `provenance` | The activity or source that established the record, here the assessment. |
| `scope` | The macro-domain, sector, jurisdiction, or asset boundary within which the assessed relationship was established (principle 7); an assessed edge is valid only within it. |
| `status` | Lifecycle state of the record, for example active or retired. |

---

## Adopter guidance: diagram and graph generation

All relationship content in this library is text form. An adopter who wants rendered diagrams or a queryable graph generates them from the text form; the corpus embeds neither. The generation sequence below preserves the framework's guarantees; skipping the filtering and validation steps is how false cycles and misplaced nodes enter rendered views.

1. Select the viewpoint the diagram answers.
2. Select and state the primary direction rule.
3. Filter the relationship set by context: time, jurisdiction, sector, and scope.
4. Validate every remaining triple against the 9 tests.
5. Separate primary edges from associative edges.
6. Infer inverse readings; store none without a recorded justification.
7. Cycle-check the filtered primary slice, and only that slice.
8. Place nodes using primary edges only.
9. Overlay associative edges without letting them move any node.
10. Record any ambiguity, unresolved conflict, or excluded edge alongside the rendered view rather than silently dropping it.

Mermaid and comparable text-to-diagram tools suit rendered views; graph databases suit queryable models, with the record structure of the previous section as a starting shape. An adopter who renders diagrams should also: declare the viewpoint and direction rule in the diagram title, label every edge with its verb, distinguish primary from associative edges by line treatment with a legend rather than by colour alone, and never encode meaning in colour alone, because colour does not survive monochrome reproduction or reach every reader.

---

## Adopter guidance: document-type options

In this library the modelling method lives in a Framework document because it defines an operating model: principles, a taxonomy, a vocabulary, viewpoints, and a lifecycle. An adopter embedding the method in their own corpus may reasonably choose a different type for parts of it.

| Type | Choose it when |
| --- | --- |
| Framework | The adopter wants the whole method as an operating model, as this library does. |
| Standard | The adopter makes relationship records mandatory and needs measurable requirements and acceptance criteria for them. |
| Specification | The adopter fixes a binding field-level schema for relationship records or interfaces, beyond the illustrative record here. |
| Guideline | The adopter offers the method as advisory interpretation support without binding force. |

This guidance supports an adopter's own document architecture; it changes nothing in this library's.

---

## Governance and lifecycle

The Owner named in this document's metadata owns the relationship vocabulary: the controlled verb set, the distinction clusters, the normalizations, and the node-class taxonomy.

Adding a verb follows 4 steps:

1. Propose the verb with a definition, a relationship class, typical source and destination categories, a typical layout role, and an inverse reading.
2. Check distinctness against the existing set and the distinction clusters; a candidate that an existing verb or a recorded normalization already covers is rejected.
3. Record the term in [`governance/register-key-terms-and-definitions.md`](register-key-terms-and-definitions.md) and add the verb's row to the controlled set in this document.
4. Bump this document's version under the library's change control.

Adding a node class follows the same shape: propose the class with its category (or make the case that a genuinely new category is needed rather than a new member of the existing 7), check distinctness, record, and bump. Category additions should be rare; most proposals are members of an existing category.

Review of this framework follows the cadence in the metadata block: annual, and upon material change to the relationship vocabulary.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO 31000:2018 | Risk management guidelines | The risk viewpoint's chain from risk through treatment to residual risk, and the separation of assessment from treatment |
| COBIT 2019 | Governance and management objectives | The authority and governance viewpoints' separation of direction-setting from implementation |

---

## Limitations

- The framework models assertions about entities, never the truth of what they assert. A validated edge is a well-formed claim; whether the claim holds in the world is established by assessment and evidence, outside the model.
- Assessed outcomes decay. A compliance or satisfaction edge is only as current as its validity period and its most recent supporting assessment.
- The library's generated relationship model and its regeneration gate (the audit programme's relationship-model sync gate) validate the library's own relationship-source records only. An adopter's records are neither validated nor schema-mandated, and the illustrative record is an adopter starting point only.
- The framework deliberately contains no exhaustive node-by-verb compatibility matrix and no embedded diagrams. Category-level compatibility in the verb table, the 9 validation tests, and the generation guidance carry that weight in prose.
- A `maps to` correspondence, however well validated, does not establish compliance or certification against any external framework or regulation.

---

**End of Document**
