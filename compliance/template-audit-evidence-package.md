# Audit Evidence Package Template

**Document Title:** Audit Evidence Package Template\
**Document Type:** Template\
**Version:** 1.1.12\
**Date:** 2026-10-28\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/standard-internal-audit.md`](standard-internal-audit.md), [`compliance/procedure-control-testing.md`](procedure-control-testing.md), [`compliance/procedure-audit-planning.md`](procedure-audit-planning.md), [`compliance/register-compliance-obligations-template.md`](register-compliance-obligations-template.md), [`compliance/template-regulator-interaction.md`](template-regulator-interaction.md)\
**Classification:** Public\
**Category:** Compliance\
**Review Frequency:** Annual, and on material change to a covered framework's evidence-presentation expectations\
**Repository Path:** [`compliance/template-audit-evidence-package.md`](template-audit-evidence-package.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template packages per-control evidence into an audit-ready bundle: a single navigable artefact that an external auditor, regulator, or independent assessor can walk through to evaluate control implementation and operating effectiveness over a defined period. For a SOC 2 Type II package, that covers whether the controls were suitably designed throughout the period and whether they operated effectively throughout the period. For a SOC 2 Type I package, it covers whether the controls were suitably designed and implemented as of a point in time (the "as of" date), and not whether they operated effectively.

The library documents per-control evidence requirements across the compliance and risk domains. The packaging step (assembling that evidence into a bundle laid out for an outside reviewer to consume) is what this template covers.

The intent is to reduce the burden of audit preparation. A well-packaged evidence bundle replaces the recurring pattern of an auditor asking ten clarifying questions per control with one structured document per control, navigable from a single cover-page index.

---

## Scope

This template applies to:

- An external financial-audit, SOC 2 Type I, SOC 2 Type II, ISO/IEC 27001:2022, PCI DSS, or framework-specific audit.
- A regulator examination requiring evidence of control implementation (see also [`compliance/template-regulator-interaction.md`](template-regulator-interaction.md) for the regulator-interaction shape).
- An internal audit, where the package becomes the auditor's working artefact.
- A customer due-diligence inquiry that requires evidence at the control level.

The template assumes the controls themselves are already documented elsewhere (typically the relevant policy, standard, or framework artefact in the library, plus any organization-specific control register). This template packages the **evidence**, not the controls.

Out of scope: the audit programme's design (covered by [`compliance/standard-internal-audit.md`](standard-internal-audit.md)); the control test methodology (covered by [`compliance/procedure-control-testing.md`](procedure-control-testing.md)); the regulator-facing shape of the submission (covered by [`compliance/template-regulator-interaction.md`](template-regulator-interaction.md)).

---

## How to use this template

1. **Confirm scope and period.** Identify the audit framework, the period covered (e.g., 1 January to 31 December) or, for a SOC 2 Type I package, the "as of" date (the point in time), and the in-scope systems, processes, or business units. Without these, the package cannot be assembled.
2. **List the in-scope controls.** Extract from the relevant control register or framework crosswalk. Each in-scope control gets a row in the cover-page index and a per-control section in the bundle.
3. **For each control, assemble the evidence.** Use the per-control template below. Evidence is the documentation that demonstrates the control was implemented AND operated as designed during the period. For a SOC 2 Type II package, evidence is the documentation that demonstrates the control was suitably designed throughout the period and operated effectively throughout the period. For a SOC 2 Type I package, evidence is the documentation that demonstrates the control was suitably designed and implemented as of the "as of" date; the package leaves out operating evidence and its tests.
4. **Mark gaps explicitly.** Controls that were not implemented, or were partially implemented, or had operating-effectiveness gaps during the period must be marked. For a SOC 2 Type II package, controls that had a design gap or an operating-effectiveness gap during the period must be marked. For a SOC 2 Type I package, controls that were not implemented, were partially implemented, or had a design gap as of the "as of" date must be marked. Hidden gaps are worse than disclosed ones.
5. **Cross-reference internally.** The bundle is meant to be navigable; from any per-control section, an auditor should be able to follow links to the source artefacts.
6. **Sign off.** The package carries an internal sign-off before it goes to the external auditor or regulator. The sign-off names who assembled it, who reviewed it, and who approved it.
7. **Preserve.** The package and its supporting artefacts are retained per the document-retention period the framework requires (commonly 7 years).

---

## Cover page

```
Audit Evidence Package
======================

Organization: <legal name>
Framework: <e.g. ISO/IEC 27001:2022 / SOC 2 Type I / SOC 2 Type II / PCI DSS v4.0.1 / DORA / FedRAMP Moderate>
Audit type: <External / Internal / Regulator examination / Customer DDQ>
Audit firm or assessor: <if external>
Auditor lead contact: <name and contact>

Period covered: <YYYY-MM-DD to YYYY-MM-DD; for a SOC 2 Type I package, replace this line with "As of: <YYYY-MM-DD>", the point in time>
Package version: <e.g. 1.0; bump on material revision before audit close>
Package assembled date: <YYYY-MM-DD>

Scope summary
- In-scope systems: <list or pointer to scope document>
- In-scope processes: <list>
- In-scope business units: <list>
- Out-of-scope (explicit): <list with rationale; required for SOC 2 and many other frameworks>

Internal assembly team
- Package lead: <named role; typically Head of Compliance or Internal Audit Lead>
- Contributing teams: <list with the team and the artefact category they own>
- Reviewer: <named role>
- Approving authority: <named role per the framework's signatory requirements>

Document retention
- Required retention period: <per framework; e.g. 7 years from audit close>
- Retention location: <secure repository path or document-management system>
```

---

## Control inventory index

The cover page is followed by a flat index of all in-scope controls. The index is the auditor's primary navigation surface; every control links to its per-control section below.

```
| # | Control ID | Control title | Framework reference | Implementation status | Operating effectiveness | Section link |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | <e.g. AC-2> | <e.g. Account management> | <e.g. ISO/IEC 27001:2022 Annex A.5.16 / NIST SP 800-53 Rev. 5 AC-2> | <Implemented / Partially implemented / Not implemented> | <Effective / Partially effective / Ineffective / Not yet assessed> | [link to per-control section] |
| 2 | ... | ... | ... | ... | ... | ... |
[continue per in-scope control]
```

### Index status legend

**Implementation status** (during the period, or as of the point in time for a SOC 2 Type I package):
- *Implemented*: the control was in place during the entire period; for a SOC 2 Type I package, the control was in place as of the point in time.
- *Partially implemented*: the control was in place for part of the period, or had a documented limitation during the period; for a SOC 2 Type I package, the control had a documented limitation as of the point in time.
- *Not implemented*: the control was not in place during the period, or as of the point in time for a SOC 2 Type I package; a compensating control may exist (named in the per-control section).

**Operating effectiveness** (over the period; a SOC 2 Type I examination does not address operating effectiveness, so a Type I package omits this column):
- *Effective*: the control operated as designed throughout the period; test results demonstrate this.
- *Partially effective*: the control operated as designed but with documented deviations or exceptions.
- *Ineffective*: the control did not operate as designed; remediation is in progress (named in the per-control section).
- *Not yet assessed*: tests have not been completed for the period; package will be re-issued when the assessment closes.

Frameworks differ on these axes. A SOC 2 Type I examination addresses whether the service organization's description presents the system as designed and implemented as of a point in time, and whether the controls were suitably designed as of that point in time. A SOC 2 Type II examination addresses the description and the suitability of design throughout the period rather than as of a point in time, and also whether the controls operated effectively throughout the period. Some control-attestation frameworks combine the two. Adapt the index columns to the framework before assembling.

---

## Per-control section template

For each control in the inventory, the bundle contains a section using the template below. The per-control section is the page an auditor lands on when following an index link.

```
## Control <#>: <Control ID> - <Control title>

### Framework references

- Primary: <e.g. ISO/IEC 27001:2022 Annex A.5.16>
- Secondary (where the same control maps to multiple frameworks): <e.g. NIST SP 800-53 Rev. 5 AC-2; CIS Control 5; SOC 2 CC6.1>
- Internal control identifier (if different): <e.g. organization's internal control number>

### Control description

<One paragraph describing what the control does in the organization's own language. Reference the source policy or standard document.>

Source artefact: <link to the policy, standard, or procedure that documents the control>

### Implementation evidence (during the period, or as of a point in time for a SOC 2 Type I examination)

Verification basis: <Independently verified / Owner-asserted / Auditor-to-verify>. For Independently verified, name the supporting independent test artefact (per [`compliance/procedure-control-testing.md`](procedure-control-testing.md), tester not the control owner); for Owner-asserted, name the asserting control owner; for Auditor-to-verify, the status is presented for the external auditor to test.

Evidence type 1: <e.g. Policy approval record>
- Artefact: <link>
- Date: <YYYY-MM-DD>
- Relevant section or page: <if the artefact is long>
- Notes: <if any>

Evidence type 2: <e.g. Configuration screenshot>
- Artefact: <link or attached file reference>
- Date: <YYYY-MM-DD>
- System or environment: <production / staging / etc.>
- Notes: <if any>

[continue per evidence type]

### Operating evidence (over the period; not part of a SOC 2 Type I package)

<A SOC 2 Type I package leaves out this section and its tests, because a Type I examination addresses design and implementation as of a point in time, not operating effectiveness. A Type II or other period-based package completes it as follows.>

Verification basis: <Independently verified / Owner-asserted / Auditor-to-verify>. Operating effectiveness is Independently verified when an independent test (tester not the control owner, per [`compliance/procedure-control-testing.md`](procedure-control-testing.md)) supports it; Owner-asserted when the control owner asserts it without an independent test this period; Auditor-to-verify when it is presented for the external auditor to test.

Test 1: <e.g. Quarterly access review>
- Frequency: <e.g. quarterly>
- Test date(s) during the period: <YYYY-MM-DD list>
- Test method: <e.g. 100% population review of the quarterly access recertifications performed in the period, each checked against role definitions>
- **Sampling justification**: <statistical or judgemental basis for the chosen sample size. [`compliance/procedure-control-testing.md`](procedure-control-testing.md) §2.2 states: "Sample sizes for inspection-based tests follow a risk-based sampling methodology:", followed by "High-risk controls: 25 to 40 samples or 100% population if feasible.", "Medium-risk controls: 15 to 25 samples." and "Low-risk controls: 5 to 15 samples." §2.2 also states: "The chosen sample size and selection method are recorded in the test's "Sampling justification" field in the audit-evidence package". Choose the selection method from the §2.3 table; its **Full population (100%)** row reads: "Low-volume populations (broadly, 25 or fewer occurrences), and any population for a control whose failure is individually consequential". §2.3 states: "The population definition, its size, and the source from which it was drawn are recorded in the evidence package." It also states: "The tester records, in the evidence package, the population definition, the sample size, the selection method, the selection rationale, and any limitation on the conclusion the sample supports (for example, that a judgemental sample does not support a statistical projection across the population). A sample that surfaces one or more exceptions is not silently expanded to seek a clean result: the exception is evaluated on its merits under section 4, and any extension of the sample is documented with its rationale." If the test reviews 100% of the population, state "100% population review" and record the same §2.3 items, including the selection rationale.>
- Tester: <named role>
- Result: <Pass / Pass with exception / Fail>
- Test artefact: <link to test record>
- Exceptions (if any): <list with remediation status>

Test 2: <e.g. Annual policy review>
- Frequency: <e.g. annual>
- Test date(s): <YYYY-MM-DD list>
- Test method: <e.g. policy reviewed by Owner and Approving Authority; review record signed>
- **Sampling justification**: <as above; for single-artefact controls like policy reviews, state "100% population review" and record the §2.3 items listed above, including the selection rationale.>
- Result: <Pass / Pass with exception / Fail>
- Test artefact: <link to review record>

[continue per test]

### Gaps and compensating controls

<If the control is fully implemented and fully effective, state "No gaps identified during the period" and proceed to sign-off. For a SOC 2 Type II package, state this only if the control was suitably designed throughout the period and operated effectively throughout the period. For a SOC 2 Type I package, if the control is suitably designed and fully implemented as of the "as of" date, state "No gaps identified as of <YYYY-MM-DD>" and proceed to sign-off.>

<If there are gaps:>
Gap 1: <one-line description>
- Period during which the gap was present: <YYYY-MM-DD to YYYY-MM-DD; for a SOC 2 Type I package, "Present as of <YYYY-MM-DD>">
- Impact: <named risk; or "no material impact" with rationale>
- Compensating control: <if any, named with link to its per-control section>
- Remediation: <plan, named owner, target date>

[continue per gap]

### Sign-off (per control)

Evidence assembler: <name, role, date>
Control owner: <name, role, date>
Reviewer: <name, role, date>
```

---

## Per-domain summaries (optional)

For larger packages (50+ controls), insert a per-domain summary between the index and the per-control sections. Each summary aggregates the controls for one library domain (governance, security, privacy, etc.) and gives the auditor a one-page overview of the domain's posture.

```
## Domain summary: <Domain name>

Controls in scope from this domain: <count>
Controls fully implemented and effective: <count> (SOC 2 Type II: suitably designed and operated effectively throughout the period; SOC 2 Type I: suitably designed and fully implemented as of the "as of" date)
Controls partially implemented or partially effective: <count> (SOC 2 Type II: with a design gap or an operating-effectiveness gap during the period; SOC 2 Type I: partially implemented, or with a design gap, as of the "as of" date)
Controls not implemented (with compensating control): <count>
Controls not implemented (without compensating control): <count>

Material findings during the period, or as of the "as of" date for SOC 2 Type I (from this domain):
- <Finding 1 brief; link to per-control section>
- <Finding 2 brief; link to per-control section>

Domain-level remediation in progress:
- <Remediation 1 brief; named owner, target date>
```

The per-domain summary is intended for auditor orientation, not for asserting status. The per-control sections remain the source of truth.

---

## Cross-reference index (optional)

For audits where the same evidence supports multiple controls (e.g., an access-review record supports both NIST SP 800-53 Rev. 5 AC-2 and AC-6), include a cross-reference index at the back of the package. The index maps evidence artefacts to the controls they support, so the auditor can confirm an artefact's reuse without independently locating it for each control.

```
| Evidence artefact | Supports controls |
| --- | --- |
| <link to artefact 1> | <control IDs> |
| <link to artefact 2> | <control IDs> |
[continue per shared artefact]
```

---

## Package-level sign-off

The cover-page sign-off is the package's final attestation: that the package was assembled honestly, reviewed by someone other than the assembler, and approved by the framework-required signatory.

```
Package assembly sign-off

Assembler statement
- I confirm that the per-control sections in this package accurately reflect the evidence available for the period covered, or as of the "as of" date for a SOC 2 Type I package.
- I confirm that gaps and partial implementations are disclosed in their respective per-control sections.
- I confirm that the supporting artefacts referenced by link or pointer remain available under the document-retention period the framework requires.
- I confirm that each per-control implementation status and operating effectiveness (implementation status only, for a SOC 2 Type I package) is labelled with its verification basis, and that an owner-asserted status is not presented as independently verified unless an independent test (per [`compliance/procedure-control-testing.md`](procedure-control-testing.md)) supports it.
Signed: <named role, e.g. Internal Audit Lead>
Date: <YYYY-MM-DD>

Reviewer statement
- I have reviewed this package and confirm it is complete, internally consistent, and ready for external review.
Signed: <named role, e.g. Head of Compliance>
Date: <YYYY-MM-DD>

Approving authority statement
- I approve the release of this package to the external auditor or regulator named on the cover page.
Signed: <named role per framework requirements; e.g. CISO, CCO, CFO>
Date: <YYYY-MM-DD>
```

---

## Anti-patterns to watch

When assembling an evidence package, the following patterns weaken the package's defensibility:

- **Evidence that is just a screenshot without a date or context.** Screenshots are point-in-time. An undated screenshot proves nothing about whether the control operated for the period covered, or, for a SOC 2 Type I package, whether it was in place as of the "as of" date. Include the date the screenshot was taken, the system, and (if relevant) the user role under which it was taken.
- **Tests with a sample size of one and no recorded basis.** Record the sample size and its basis in the test's Sampling justification field, as §2.2 and §2.3 of [`compliance/procedure-control-testing.md`](procedure-control-testing.md) state them (quoted in the per-control template above). Where a single instance is the whole population, such as a control that operates once in the period, record it as a "100% population review" under §2.3's **Full population (100%)** selection method, with the §2.3 items, including the selection rationale.
- **"See attached" without an attachment.** The package is the artefact; if evidence is attached separately, the per-control section names the attachment by name and version, and the attachment travels with the package.
- **Compensating controls without a remediation plan.** A compensating control is acceptable for an audit period, or, for a SOC 2 Type I package, as of the "as of" date; an absent remediation plan signals the gap will persist. Most frameworks require remediation plans for ineffective controls; check the framework's specific requirements.
- **Mixing "we will do this" with "we did this".** The package covers a period in the past, or, for a SOC 2 Type I package, a past point in time. Future commitments belong in a remediation plan, not in the operating-evidence section (for a SOC 2 Type I package, not in the implementation-evidence section). The auditor will treat any future-tense language in evidence sections as a finding.
- **Bundles that grow beyond practical navigability.** Above ~150 in-scope controls the per-domain summaries become load-bearing; below that, the index is enough. Plan navigation before the package crosses the threshold.
- **Sign-off by the same person as the assembler.** The reviewer must be different from the assembler. Self-review is not review.

---

## Review questions

Before releasing a package, answer the following:

1. Have we identified the framework's specific evidence-presentation requirements (some frameworks have a prescribed schema)?
2. Have we included every in-scope control in the index, including those that are not implemented?
3. For each partial or ineffective control, is the gap and the compensating control or remediation plan explicit?
4. For each test, is the sample size justifiable for the framework's expectations?
5. For each control, is the verification basis recorded, and are owner-asserted statuses distinguished from independently-verified status (with the supporting independent test named for the latter)?
6. Are all internal links valid, and are all referenced external artefacts available?
7. Has the package been reviewed by someone other than the assembler?
8. Has the framework-required signatory approved the package?
9. Is the package retained at the location named on the cover page, with the required retention period set?

---

## Maintenance

This template is updated when:

- A covered framework materially changes its evidence-presentation requirements.
- An organizational change moves package assembly to a new team (the role assignments in the cover page need to reflect the team).
- Adopter feedback identifies a per-control field that consistently produces ambiguity.

Per-framework evidence specifics (the exact schema PCI DSS expects, the SOC 2 description-criteria, etc.) live in the relevant sector overlay or framework-specific annex, not in this template. Updates to those specifics do not require updates here.

---

## Licence

CC BY-SA 4.0. Adapt and share, including for commercial use. When you share this document or an adaptation of it, attribute the library and indicate any changes; when you share an adaptation, license your own contributions to it under CC BY-SA 4.0, a later CC BY-SA version, or a BY-SA-compatible licence. The library's own text stays under CC BY-SA 4.0.
