# Executive narrative layer

**Status:** Early. The authoring specification and the narrative gate family are in place, and published narrative pages are live; further narrative content arrives in later phases.

This directory is the GRC Library's executive narrative layer: non-normative, advisory, and explanatory material for a governing body or accountable executive leadership (board, ELT, or senior management, as applicable). It explains what the corpus governs and why it matters at the leadership level.

**This layer does not establish requirements; the linked corpus governs.** Nothing in this directory is a policy, a standard, a control, a source of any obligation, or evidence that a control operates. Every narrative page resolves to the authoritative corpus documents that do govern. The full contract is the [Executive Narrative Authoring Specification](../specification-executive-narrative.md); copyable subtype skeletons are in the [subtype templates](../governance/template-executive-narrative-subtypes.md).

## How to read this layer

Each management concern below frames a leadership question. Under each concern, the supported routes (executive briefs, scenarios, decision narratives, oversight question sets, stories, journeys, and outcome maps) are curated from published narrative pages, using the generated narrative registry as the inventory of what is published. A concern with no supported route yet is shown as a declared coverage gap, not hidden: coverage is measured by decision areas with supported routes, never by page count.

## Management concerns

### 1. Accountability and decision rights
Who owns which governance decision, and where the corpus fixes the accountable role. Supported routes: [What the governing body should require before an AI system goes into production](briefs/brief-ai-production-approval.md) (Executive Brief).

### 2. AI and autonomous systems
How the corpus governs AI from intake through oversight, retirement, and incident response. Supported routes: [What the governing body should require before an AI system goes into production](briefs/brief-ai-production-approval.md) (Executive Brief); [What the governing body should require for AI incident-response readiness before production](briefs/brief-ai-incident-response-readiness.md) (Executive Brief).

### 3. Cybersecurity and operational resilience
How the corpus establishes protective controls and the ability to withstand and recover from disruption. Supported routes: [What the governing body should require for AI resilience and continuity](briefs/brief-ai-resilience-continuity.md) (Executive Brief).

### 4. Data, privacy, and information lifecycle
How the corpus governs personal and sensitive information across its lifecycle. Supported routes: [What the governing body should require for AI data governance and classification](briefs/brief-ai-data-governance.md) (Executive Brief).

### 5. Supplier and cloud dependency
How the corpus addresses concentration, exit, and assurance over third parties. Supported routes: [What the governing body should require for third-party and AI supply-chain risk oversight](briefs/brief-ai-supply-chain-oversight.md) (Executive Brief).

### 6. Compliance and assurance
How the corpus maps controls to obligations and produces evidence an assurer can test. Supported routes: none yet (declared coverage gap).

### 7. Risk acceptance and exceptions
How the corpus frames defensible risk acceptance and time-bound exceptions. Supported routes: [What the governing body should require before an AI system goes into production](briefs/brief-ai-production-approval.md) (Executive Brief).

### 8. Enterprise architecture and technology debt
How the corpus relates architecture decisions to governance and to accumulated technology debt. Supported routes: none yet (declared coverage gap).

### 9. Workforce, conduct, and operating model
How the corpus addresses people, roles, and the operating model that runs the controls. Supported routes: none yet (declared coverage gap).

### 10. Programme establishment and maturity
How the corpus supports standing up a governance programme and measuring its maturity. Supported routes: none yet (declared coverage gap).

## Boundaries of this directory

This directory is deliberately outside the corpus document model: it has its own document class, its own registry, and its own gate family. It remains fully inside the repository's safety gates (secrets, PII, link integrity, external link domains). The narrative registry is `narrative.yml`; it is generated, never hand-edited.

**License:** CC BY-SA 4.0
