# Secure Code Review Procedure

**Document Title:** Secure Code Review Procedure\
**Document Type:** Procedure\
**Version:** 0.0.2\
**Date:** 2026-05-28\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`dev-security/policy-secure-development-and-engineering.md`](policy-secure-development-and-engineering.md), [`dev-security/standard-developer-security-requirements.md`](standard-developer-security-requirements.md), [`dev-security/standard-devops-security-requirements.md`](standard-devops-security-requirements.md), [`dev-security/standard-software-composition-analysis.md`](standard-software-composition-analysis.md), [`dev-security/standard-api-security.md`](standard-api-security.md), [`dev-security/standard-quality-assurance-and-testing.md`](standard-quality-assurance-and-testing.md), [`dev-security/guideline-ai-coding-assistant-security.md`](guideline-ai-coding-assistant-security.md), [`security/procedure-vulnerability-management.md`](../security/procedure-vulnerability-management.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md)\
**Classification:** Public\
**Category:** Developer Security\
**Review Frequency:** Annual and upon material change to languages, framework stack, or AI-assisted development practice\
**Repository Path:** [`dev-security/procedure-secure-code-review.md`](procedure-secure-code-review.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure defines how code is reviewed for security defects before merge to a protected branch and before release. It applies to human-authored, AI-assisted, and AI-generated code, and to changes that affect runtime behaviour, dependencies, configuration, infrastructure-as-code, and security-critical components.

---

## Scope

This procedure applies to:

1. All proposed changes to repositories holding production code, customer-facing services, security-relevant configuration, or infrastructure-as-code.
2. All proposed changes to AI agents, prompts, tool definitions, and retrieval pipelines that influence runtime behaviour.
3. Vendor-supplied code, open-source contributions, and third-party patches before adoption.
4. Hotfix branches and emergency release paths.

It does not cover non-production sandboxes used solely for individual experimentation; those repositories follow the developer security requirements at a baseline level.

---

## Procedure

### Step 1: Pre-review preparation

Before requesting review the change author confirms that:

| Item | Expected state |
| --- | --- |
| Pre-commit checks | SAST, secret scanning, lint, formatter, dependency scan, IaC scan all passing |
| Tests | Unit and integration tests passing locally and in CI |
| Change scope | Pull request is decomposed; single logical change per request where feasible |
| Description | Includes intent, impact, risk class, security considerations, and test coverage summary |
| Dependencies | New or upgraded dependencies declared; provenance noted; licence acceptable |
| Secrets | No secrets, credentials, or sensitive identifiers in code, comments, or fixtures |
| AI assistance disclosure | If AI assistants generated material portions, the author declares this and confirms human review of the produced output |
| Linked work | Reference to the issue, design note, or threat-model entry where applicable |

The change is not submitted for review until these preconditions are met.

### Step 2: Reviewer assignment

| Change class | Reviewer requirement |
| --- | --- |
| Routine application change | One peer reviewer with codebase familiarity |
| Security-sensitive change | One peer reviewer plus one designated security reviewer |
| Cryptographic or authentication change | Two reviewers; at least one with subject-matter depth |
| Infrastructure-as-code or platform change | One peer reviewer plus one platform engineer; security reviewer where the change crosses a trust boundary |
| AI agent or prompt change | One peer reviewer plus one AI governance reviewer for agentic or tool-invoking components |
| Third-party or vendor patch | Security reviewer; the change author cannot self-merge |
| Hotfix to production | Reviewer assignment may be reduced in flight; full review completed within the same business day after merge |

Security-sensitive change indicators include: changes touching authentication, authorisation, session management, cryptography, key handling, input handling at trust boundaries, output rendering, deserialisation, file or path handling, command construction, network endpoints, IAM policy, secrets configuration, AI tool permissions, or retrieval augmentation sources.

### Step 3: Reviewer evaluation

Reviewers evaluate the change against the categories below. The reviewer is expected to read the diff in full and to look beyond the diff where the change is non-local.

#### Category A: secrets and credentials

| Check | Description |
| --- | --- |
| No embedded secrets | API keys, tokens, certificates, passwords absent from code, fixtures, tests, comments |
| Configuration source | Secrets sourced from the secrets management service; reference, not value |
| Logging | No credentials, tokens, session IDs in log statements |
| Error paths | No sensitive material returned in errors, stack traces, or telemetry |

#### Category B: input handling and injection

| Check | Description |
| --- | --- |
| Validation at trust boundary | Untrusted input validated against a permissive-deny pattern at boundary entry |
| Output encoding | Output encoded for the destination context; no string concatenation into HTML, SQL, shell, or LDAP |
| Parameterised queries | Database access uses parameterised interfaces; ORM use does not introduce dynamic predicate strings |
| Command and shell | No shell invocation of untrusted input; subprocess invocations use argument lists, not strings |
| Deserialisation | Untrusted deserialisation avoided; safe formats preferred |
| Path handling | Path traversal protected; canonical-path comparison; allow-listed base paths |
| Regular expressions | No catastrophic backtracking patterns on untrusted input |
| Server-side request forgery | Outbound HTTP from untrusted input restricted; metadata endpoints blocked |

#### Category C: authentication, authorisation, and session

| Check | Description |
| --- | --- |
| Authentication | New endpoints honour authentication; no inadvertent anonymous exposure |
| Authorisation enforcement | Per-resource authorisation evaluated server-side; object-level checks present; no client-trusted role claims |
| Session and token handling | Tokens issued and validated correctly; no logging of session identifiers; no token in URL |
| Multi-tenant isolation | Tenant scoping evaluated for every data access path |
| Privilege escalation | Administrative endpoints separated; sensitive operations require step-up where required |

#### Category D: cryptography

| Check | Description |
| --- | --- |
| Algorithm and parameters | Approved algorithms per the encryption policy; no custom cryptography |
| Random number generation | Cryptographic randomness used where required; not for non-security contexts |
| Key handling | Keys sourced from the key management service; no embedded keys; rotation paths preserved |
| TLS use | TLS configuration uses platform defaults; no certificate validation disabled |
| Hashing | Password hashing uses an approved algorithm with appropriate parameters |
| Constant-time comparison | Sensitive comparisons use constant-time primitives |

#### Category E: data handling

| Check | Description |
| --- | --- |
| Data classification | Data classification considered; controls match per the data classification standard |
| Personal data | Personal data handling consistent with privacy framework; minimisation respected |
| Children's data | Where children's data is in scope, the children's data framework applies |
| Storage at rest | Sensitive data at rest is encrypted; storage chosen per the classification |
| Transmission | Transit cryptography enforced; no internal plaintext channels for sensitive data |
| Retention | Retention defaults align with the records retention schedule |
| Deletion | Deletion paths exist and operate correctly where required |

#### Category F: error handling, logging, and telemetry

| Check | Description |
| --- | --- |
| Errors | Errors handled gracefully; no information disclosure in error responses |
| Logs | Logs contain required security event fields; no sensitive payload content |
| Telemetry | Telemetry does not exfiltrate sensitive content; aligned with the logging standard |
| Alerts | New failure modes generate appropriate alerts; alert volume considered |

#### Category G: dependencies and supply chain

| Check | Description |
| --- | --- |
| New dependencies | Necessity justified; vendor reputation considered |
| Versions | Pinned where applicable; lockfile updated |
| Provenance | Source verified; published-by chain inspected for typosquatting and brand-confusion |
| Vulnerability state | No known critical or high vulnerabilities at adoption; per the SCA standard |
| Licence | Licence acceptable per the open-source licence policy |
| Software bill of materials | SBOM artefact regenerated and attached per the SCA standard |

#### Category H: infrastructure as code and platform

| Check | Description |
| --- | --- |
| Identity and access | Principle of least privilege; no wildcard permissions on production resources |
| Public exposure | New public endpoints justified; security groups, firewall rules, ingress rules constrained |
| Encryption configuration | Encryption at rest and in transit enabled by default for new resources |
| Logging configuration | Cloud-native audit logs enabled; routed to the central log destination |
| Secrets in configuration | No secrets in plaintext configuration; references to secrets manager |
| Drift | Changes consistent with the platform baseline; no out-of-band changes |
| Network segmentation | New components placed in the appropriate trust zone |

#### Category I: AI components

| Check | Description |
| --- | --- |
| Prompt injection resistance | Untrusted content treated as data; instructions are not derived from untrusted sources |
| Tool permissions | Agentic tool sets minimized; tool invocations are auditable |
| Output handling | Model output sanitised before use in security-sensitive contexts |
| Sensitive data in prompts | Sensitive data is not passed to models that have not been assessed for that classification |
| Evaluation | Evaluation suite updated where the change materially affects model behaviour |
| Logging | Prompt and completion logging consistent with the [`AI and Agentic Development Security Standard`](../ai/standard-ai-and-agentic-development-security.md) (Inference call logging control) |

#### Category J: change hygiene

| Check | Description |
| --- | --- |
| Diff focus | Diff is focused; unrelated changes split out |
| Dead code | Removed code is removed in full; no commented-out blocks left behind |
| Tests | New behaviour has tests; failing-path tests where the change has security relevance |
| Documentation | User-visible changes are documented; security-relevant behaviour noted in the change description |
| Backwards compatibility | Compatibility considered; deprecations are deliberate |

### Step 4: Reviewer dispositions

Reviewers select one of the following:

| Disposition | Meaning |
| --- | --- |
| Approve | Change is acceptable as proposed |
| Approve with non-blocking comments | Acceptable; comments are suggestions or follow-up items |
| Request changes | Change is not acceptable as proposed; specific findings to address |
| Block on security grounds | Change is not acceptable; the security reviewer documents the basis and the path to remediation |

A change with a security-grounds block cannot be merged until the block is cleared.

### Step 5: Author response

| Response action | Expected behaviour |
| --- | --- |
| Address each comment | Each thread is addressed; either by code change or by explicit reasoning |
| Re-request review | Once changes are made, reviewers are re-notified |
| Disagreement | Disagreement is escalated to a third reviewer or to the relevant maintainer; not bypassed |
| Out-of-scope follow-ups | Filed as issues; not silently dropped |

### Step 6: Merge gate

The change can be merged when:

| Gate | Requirement |
| --- | --- |
| Required reviewers | All required reviewers have approved per Step 2 |
| Status checks | All required CI checks are green; security gates are green |
| Branch protection | Branch protection rules satisfied; no force-push, no bypass |
| Out-of-policy approvals | Any policy waiver is approved in writing by the policy owner |
| Code freeze | If a freeze is in effect, an exception ticket is present |

### Step 7: Post-merge actions

| Action | Description |
| --- | --- |
| Deployment monitoring | Deployment is monitored; rollback path remains available |
| Defect feedback loop | Defects discovered post-merge feed back to the reviewers and to the change author |
| Lessons recorded | Repeated review findings feed into developer training and pattern libraries |

---

## Reviewer competency and rotation

| Element | Requirement |
| --- | --- |
| Reviewer baseline | Trained in the secure-coding curriculum per the awareness and training standard |
| Designated security reviewers | Maintained as a named pool with current training |
| Rotation | Designated security reviewers rotate workload to avoid single-reviewer dependency |
| Calibration | Periodic calibration sessions on findings consistency |
| Feedback | Reviewers receive feedback on coverage from incidents and from penetration tests |

---

## Tooling integration

| Tool class | Role |
| --- | --- |
| SAST | Pre-review automated findings; reviewer confirms triage |
| Secret scanning | Pre-merge gate; reviewer confirms remediation if a finding occurs |
| SCA | Dependency findings surfaced; reviewer confirms accepted versions |
| IaC scanners | Infrastructure-as-code policy findings surfaced |
| Linters and formatters | Style and pattern enforcement; reduces reviewer cognitive load |
| Pull request templates | Security-relevant prompts surfaced; review evidence captured |
| AI review assistants | Suggest findings; the human reviewer remains accountable for the disposition |

Automated findings inform but do not replace the human review.

---

## AI-assisted and AI-generated code

| Consideration | Procedure response |
| --- | --- |
| Disclosure | Author declares AI assistance in the change description |
| Human accountability | Author is accountable for the change as if they wrote it by hand |
| Pattern-recognition risk | Reviewer applies extra scrutiny to common AI-failure patterns: stale APIs, hallucinated libraries, plausible-but-wrong validation, copy-paste from training data |
| Licence risk | Reviewer checks for likely-copied code; flags suspected verbatim third-party code |
| Sensitive context | Sensitive code (cryptography, authentication, security boundaries) receives heightened scrutiny when AI-generated |
| Evaluation | AI-generated tests are reviewed for meaningfulness; assertion strength is verified |

---

## Operating expectations

1. Median time to first review feedback is within one business day; security-blocked items are addressed by the security pool the same business day where feasible.
2. Review thoroughness, not cycle time, is the metric of interest; speed is achieved through smaller changes, not faster scans.
3. Pull-request scope and quality is a developer-skills metric tracked at the team level.
4. Findings repeated across reviews are surfaced into the secure-coding curriculum and the rule library.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| NIST SP 800-218 | SSDF PW.7 (review and analysis) | Secure development practice |
| OWASP SAMM | Verification: secure code review | Software assurance maturity |
| OWASP ASVS v5 | V1 Architecture; V14 Configuration | Verification expectations |
| ISO/IEC 27001:2022 | A.8.28 Secure coding; A.8.29 Security testing in development and acceptance | Secure development |
| ISO/IEC 27002:2022 | 8.28, 8.29, 8.30 | Outsourced development; testing |
| OpenSSF Best Practices | Code review | Open-source baseline |
| SLSA | Build integrity | Supply-chain assurance |
| CIS CSC v8 | Control 16 Application Software Security | Critical controls |

---

## Limitations

This procedure is a CC BY-SA 4.0 baseline. Adopting organisations select reviewer pool size, tooling, and gating thresholds proportionate to their risk profile and engineering culture. Review effectiveness is verified through penetration testing, post-incident review, and periodic process audit.

---

**End of Document**
