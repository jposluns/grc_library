# Worked example: converting a draft into a CC0 artefact

This walkthrough shows how a draft becomes a CC0-compliant artefact in this library. The example traces a hypothetical short procedure from rough notes through to a committed file. It is for adopters and contributors who want to see the ingestion specification applied end to end.

## Starting material

Imagine you have rough notes from an internal meeting describing a quarterly access review:

```
Access review process:

- Each quarter, security ops runs an extract from Entra ID for all
  privileged accounts.
- Microsoft Sentinel correlates against last-90-day login data.
- System owners certify the active list. Anything not certified gets
  disabled after 14 days.
- Evidence stored in SharePoint.
- Quebec data is handled separately because of Quebec Law 25.
- Approved by the CISO.
```

These notes contain everything you need to build a Procedure artefact, but they cannot land in the library as-is because they reference vendor product names, internal storage locations, and a specific role-as-person convention.

## Step 1: pick the document type

The notes describe a recurring multi-actor workflow (Security Ops, System Owners, CISO). This is a Procedure, not an SOP (which would be a narrower single-actor sequence). See `specification-master-project.md` Section 4.4 for the type selection guidance.

## Step 2: pick the domain and filename

This procedure is about identity and access. It belongs in `security/`. Per the filename rules in `specification-ingestion.md`, the filename starts with the type prefix and uses lowercase words separated by single hyphens:

```
security/procedure-quarterly-privileged-access-review.md
```

## Step 3: apply the sanitisation substitution table

Use the Appendix A table in `specification-ingestion.md`:

| Source term | Replacement |
| --- | --- |
| Entra ID | enterprise identity provider |
| Microsoft Sentinel | SIEM |
| SharePoint | collaboration and file storage platform |

Quebec is a legitimate jurisdictional reference, not a sanitisation target. It stays.

## Step 4: replace person- and team-specific text with role-based language

`security ops` becomes the SOC (a generic role). `system owners` is already generic. `CISO` is already a role. No further substitution needed.

## Step 5: write the canonical metadata block

```
# Quarterly Privileged Access Review Procedure

**Document Title:** Quarterly Privileged Access Review Procedure 
**Document Type:** Procedure 
**Version:** 0.0.1 
**Date:** 2026-05-28 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Chief Information Security Officer 
**Related Documents:** [`security/policy-identity-and-access-management.md`](policy-identity-and-access-management.md), [`security/standard-privileged-access-management.md`](standard-privileged-access-management.md), [`security/procedure-access-control.md`](procedure-access-control.md) 
**Classification:** Public 
**Category:** Information Security 
**Review Frequency:** Annual and upon material identity-provider or audit-finding change 
**Repository Path:** [`security/procedure-quarterly-privileged-access-review.md`](procedure-quarterly-privileged-access-review.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 
```

New documents start at `0.0.1`, not `1.0.0`. Promotion to `1.0.0` happens upon first formal approval and publication as a stable active document.

## Step 6: write the body

Apply the canonical body structure (Purpose, Scope, Procedure, Evidence requirements, Limitations, References and framework alignment, `End of Document`). Use sentence-case section headings. Pair `ensure` with `that`. Replace bullet markers with full sentences where it improves clarity.

```
---

## Purpose

This procedure defines the quarterly review of privileged accounts, the
evidence retained, and the decision points that lead to deactivation
when certification is not received.

---

## Scope

This procedure applies to all privileged accounts in the enterprise
identity provider, including human and non-human accounts. It applies
across all jurisdictions including Quebec, where Law 25 imposes
specific accountability and retention conditions.

---

## Procedure

### Step 1: Extract

The SOC extracts the active privileged-account list from the enterprise
identity provider on the first working day of each quarter.

### Step 2: Correlate

The SIEM correlates the extract against authentication telemetry from
the previous 90 days. Inactive accounts are flagged.

### Step 3: Certify

System Owners certify each active account. Certification confirms
business need, role correctness, and continued authorisation.

### Step 4: Deactivate

Accounts that are not certified are disabled 14 calendar days after
the certification deadline. Re-enablement requires SOC and System Owner
joint approval.

---

## Evidence requirements

The SOC retains the quarterly extract, the certification record, and
the deactivation log on the collaboration and file storage platform
under restricted access. Records are retained for the period defined in
the Records Retention and Destruction Standard.

Quebec records are retained and processed under the additional
accountability conditions of Quebec Law 25, including the requirement
to log access by the identity custodian.

---

## Limitations

This procedure is a public-domain baseline. Adopting organisations must
validate the cadence, the certification record format, the
deactivation grace period, and the jurisdictional retention conditions
against their own policy and legal requirements.

---

## References and framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27001:2022 | A.5.15 to A.5.18 | Access control and identity lifecycle |
| NIST SP 800-53 Rev 5 | AC-2; AC-6 | Account management; least privilege |
| CSA CCM v4.1 | IAM-05 | Privileged account management |
| Quebec Law 25 | Articles 8 to 9 | Accountability and access logging |

---

**End of Document**
```

## Step 7: add to the index and domain README

The new artefact must appear in two places:

1. `governance/register-document-index-and-classification.md`: add a new row with Domain, Type, Title, Repository Path, Owner Role, Review Frequency, Primary Alignment Families. Bump the register's version (patch).
2. `security/README.md`: add a new row in the Active Documents table.

## Step 8: run the local audits

```
python3 tools/lint-metadata.py
python3 tools/lint-language.py
python3 tools/lint-links.py
python3 tools/lint-structure.py
```

All four must exit clean.

## Step 9: commit

```
git add security/procedure-quarterly-privileged-access-review.md governance/register-document-index-and-classification.md security/README.md
git commit -m "Add quarterly privileged access review procedure"
```

## Step 10: open a pull request

Reference the issue if one exists. Note the version bump on the index register. List any new external framework references.

## Common pitfalls

- Forgetting to add the new document to both the index and the domain README. The structural linter catches this.
- Leaving `Microsoft`, `Entra`, `Azure`, `Sentinel`, `SharePoint`, or other vendor-product references unsanitised. The language linter has a partial coverage; manual review is still required.
- Using a bare `ensure` (without `that`) or an em or en dash. The language linter catches both.
- Starting the version at `1.0.0` rather than `0.0.1`. New documents always begin at `0.0.1` per the ingestion specification.
- Using British `-ise` endings. The language linter catches a defined list of common endings.

## Summary

The end state is a self-contained, role-based, framework-aligned, CC0-licensed procedure that any organisation can fork and adapt. The path to that state is short: type selection, domain placement, canonical filename, sanitisation, role substitution, metadata block, canonical body structure, index and README updates, audit pass, commit.
