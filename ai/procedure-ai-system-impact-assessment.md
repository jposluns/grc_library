# AI System Impact Assessment Procedure

**Document Title:** AI System Impact Assessment Procedure\
**Document Type:** Procedure\
**Version:** 1.0.3\
**Date:** 2026-07-09\
**Owner:** AI Risk Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md), [`governance/procedure-continuous-improvement-register.md`](../governance/procedure-continuous-improvement-register.md), [`resilience/plan-it-disaster-recovery.md`](../resilience/plan-it-disaster-recovery.md), [`privacy/template-dpia.md`](../privacy/template-dpia.md), [`privacy/register-automated-decision-making.md`](../privacy/register-automated-decision-making.md), [`ai/procedure-integrated-ai-and-privacy-assessment.md`](procedure-integrated-ai-and-privacy-assessment.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI risk or regulatory change\
**Repository Path:** [`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure defines a reusable method for assessing AI system impacts before approval, deployment, material change, expanded use, supplier onboarding, or retirement.

The assessment focuses on data lifecycle risk, security risk, privacy risk, operational impact, supplier dependency, human oversight, residual risk, and evidence sufficiency.

---

## Trigger events

An AI impact assessment is required when:

1. A new AI system is proposed.
2. An existing system adds AI capability.
3. A model, dataset, retrieval source, tool, integration, supplier, or operating context materially changes.
4. Sensitive or personal data is introduced.
5. The system is used in a regulated, high-impact, safety-relevant, financial, employment, security, legal, or customer-affecting process.
6. External users, customers, partners, or suppliers interact with the system.
7. The system can trigger actions, transactions, workflow changes, access changes, or operational decisions.
8. The system is retired and data, logs, model endpoints, retrieval stores, or supplier commitments require closure.

---

## Procedure

### Step 1: Register the system

Create or update the AI System Register entry with:

- System name using a generic or internal-safe identifier.
- Business purpose.
- System owner.
- Data owner.
- Supplier owner where applicable.
- Lifecycle status.
- Intended users.
- Deployment model.
- Data categories.
- Initial risk tier.

### Step 2: Define the use case

Document:

- Intended use.
- Prohibited use.
- Output consumers.
- Decision impact.
- Human oversight model.
- Automation level.
- Criticality.
- Failure consequences.

### Step 3: Assess data lifecycle

Evaluate each lifecycle stage:

| Stage | Assessment Questions |
| --- | --- |
| Collection | What data is collected, from whom, under what authority, and for what purpose? |
| Annotation | Are labels, classifications, or human judgements controlled and quality-checked? |
| Storage | Where is data stored, who can access it, and how is it protected? |
| Processing | What transformations, embeddings, retrieval indexes, or derived datasets are created? |
| Training or Fine-Tuning | Is data used to train, fine-tune, improve, or adapt a model? |
| Retrieval | What stores, documents, databases, or memory sources can be retrieved? |
| Inference | What data is submitted in prompts, files, API requests, or context windows? |
| Monitoring | What prompts, outputs, logs, traces, feedback, or evaluation records are retained? |
| Retention | How long is each data class retained, and why? |
| Deletion | Can data, embeddings, logs, and supplier-held copies be deleted or rendered inaccessible? |

### Step 4: Assess threats and control exposure

Assess exposure to:

- Prompt injection.
- Indirect prompt injection.
- Unsafe tool use.
- Data poisoning.
- Retrieval leakage.
- Training data leakage.
- Model inversion.
- Membership inference.
- Cross-user or cross-tenant data exposure.
- Unauthorized model or dataset extraction.
- Shadow AI bypass.
- Excessive agency or automation.
- Supplier failure or terms change.

### Step 5: Assess privacy and legal context

Determine whether the system processes personal data, sensitive data, regulated data, employee data, customer data, confidential business data, or data subject to retention, transfer, or deletion obligations.

Record whether review is required from privacy, legal, compliance, labour, sector regulatory, procurement, or information security roles.

Where personal data is processed, route to the privacy-side instruments through the [Integrated AI and Privacy Assessment Procedure](procedure-integrated-ai-and-privacy-assessment.md): record the activity in the [automated decision-making register](../privacy/register-automated-decision-making.md) where the system makes a solely-automated decision producing legal or similarly significant effects (GDPR Article 22), complete a [DPIA](../privacy/template-dpia.md) where the Article 35 trigger is met, and complete the EU AI Act Article 27 fundamental rights impact assessment (FRIA) where the deployer meets the Article 27(1) test. The FRIA complements the DPIA (Article 27(4)) and does not substitute for it.

### Step 6: Assess supplier and external service dependency

For externally operated services, document:

- Provider role.
- Hosting location and data residency where known.
- Training or improvement use of submitted data.
- Retention commitments.
- Subprocessor or subcontractor exposure.
- Incident notification commitments.
- Audit or assurance evidence.
- Deletion capability.
- Exit capability.
- Availability and continuity commitments.

### Step 7: Assign risk tier

Assign a risk tier using criteria such as:

| Tier | Description |
| --- | --- |
| Low | Limited internal use, low sensitivity data, no material decision impact, no external exposure. |
| Moderate | Business process support, controlled internal users, moderate sensitivity data, human review available. |
| High | Sensitive data, external users, regulated context, material business or individual impact, supplier dependency, or tool execution. |
| Critical | Safety, rights, access, employment, financial, security, legal, regulatory, or critical service impact with limited tolerance for failure. |

### Step 8: Define required controls

Define required controls for:

- Access control.
- Data minimization.
- Logging.
- Encryption.
- Prompt and retrieval controls.
- Tool permissions.
- Human oversight.
- Supplier controls.
- Testing.
- Monitoring.
- Incident response.
- Decommissioning.

### Step 9: Approve or reject

The approving authority must decide one of the following:

- Approved for use.
- Approved with conditions.
- Approved for pilot only.
- Deferred pending remediation.
- Rejected.
- Retired.

Approval must record residual risk, required conditions, control owner, review date, and exception reference where applicable.

### Step 10: Maintain evidence

Retain the assessment, approvals, test results, control evidence, supplier evidence, monitoring records, incident records, and decommissioning records according to defined retention rules.

---

## Roles and responsibilities

- **AI Governance Lead** coordinates and performs the assessment steps (Steps 1 to 10), drawing on the system owner and relevant subject-matter contributors for the evidence each step depends on.
- **System owner** supplies the AI system register entry, the data-lifecycle assessment, and the control and supplier evidence the steps rely on, and owns the resulting control requirements and residual-risk items.
- **Approving authority** makes the Step 9 decision (approve, approve with conditions, pilot, defer, reject, or retire). For high-impact systems or unresolved high residual risk, the decision escalates to the **AI Governance Council**.

---

## Required outputs

- AI System Register entry.
- AI impact assessment record.
- Data lifecycle assessment.
- Risk tiering decision.
- Control requirements.
- Supplier assessment where applicable.
- Approval or rejection decision.
- Residual risk statement.
- Next review date.

---

**End of Document**
