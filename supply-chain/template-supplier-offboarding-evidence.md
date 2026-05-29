# Supplier Offboarding Evidence Template

**Document Title:** Supplier Offboarding Evidence Template\
**Document Type:** Template\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** Supplier Risk Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`supply-chain/procedure-supplier-exit-and-data-return.md`](procedure-supplier-exit-and-data-return.md), [`supply-chain/standard-cloud-exit-and-data-portability.md`](standard-cloud-exit-and-data-portability.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md), [`supply-chain/register-supplier-risk-template.md`](register-supplier-risk-template.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md), [`security/procedure-access-control.md`](../security/procedure-access-control.md)\
**Classification:** Public\
**Category:** Supply Chain Governance\
**Review Frequency:** Annual and upon material exit, data-return obligation, or regulatory change\
**Repository Path:** [`supply-chain/template-supplier-offboarding-evidence.md`](template-supplier-offboarding-evidence.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## Purpose

This template defines the evidence record produced at supplier offboarding to demonstrate that access has been revoked, organisational data has been returned or destroyed, residual obligations are documented, and the relationship has closed cleanly. The record is the auditable trail required by GDPR Article 28, DORA exit-strategy obligations, sector regulators, and the supplier exit procedure.

A populated offboarding record identifies real suppliers and is sensitive operational data. This public CC0 template intentionally contains no example values.

---

## Scope

This template covers offboarding for all in-scope third-party relationships ending in any of the following ways: contract expiry, contract termination by either party, supplier insolvency, change of ownership requiring re-onboarding, organisational decision to exit, and forced exit due to non-remediable breach.

It does not cover offboarding of individual personnel from a continuing supplier relationship (that is governed by the supplier ongoing-monitoring procedure).

---

## Offboarding evidence record

### Section 1: Relationship identification

| Field | Description |
| --- | --- |
| Supplier ID | Internal identifier in the supplier risk register |
| Supplier name | Private record; not in public CC0 template |
| Service description | What the supplier provided |
| Contract reference | Master agreement and any in-scope statements of work |
| Service tier | Tier classification at the time of offboarding |
| Personal data processed | Yes or no; data categories if yes |
| Relationship start date | |
| Relationship end date | |
| Reason for offboarding | Expiry, organisation-initiated termination, supplier-initiated termination, insolvency, change of ownership, breach, mutual termination |
| Notice period followed | Yes or no; if not, the contractual basis for waiving notice |
| Offboarding initiated by | Role |
| Offboarding owner | Supplier Relationship Owner (SRO) |

### Section 2: Access revocation evidence

| Access type | Evidence required | Confirmation timestamp (UTC) | Confirming role |
| --- | --- | --- | --- |
| Application and service accounts | Audit log of account deactivation in each in-scope system | | |
| API keys and tokens | Revocation log; key rotation evidence for any keys shared with the supplier | | |
| Certificates | Revocation in the certificate authority; CRL or OCSP update | | |
| Network access | Firewall rule removal; VPN account revocation; private network connection termination | | |
| Physical access | Badge deactivation; key return; biometric template removal | | |
| Federated identity | Removal from the identity provider; revocation of any persistent SSO session | | |
| Privileged access | PAM vault rotation of any credentials the supplier could have memorised | | |
| Email and collaboration | Distribution-list removal; mailbox handoff or deactivation | | |
| Code repository | Repository access revoked; outstanding tokens revoked | | |
| Customer-facing access | Removal from customer-data viewing surfaces if the supplier had any |  | |

Access revocation target: within 24 hours of the formal offboarding declaration. Exceptions documented with rationale, time-limit, and remediation plan.

### Section 3: Data return and destruction evidence

| Data category | Action | Evidence | Confirmation timestamp |
| --- | --- | --- | --- |
| Personal data | Return to organisation OR destruction | Return: secure transfer log; destruction: certificate of destruction signed by the supplier | |
| Customer data | Return OR destruction | As above | |
| Confidential business data | Return OR destruction | As above | |
| Trade or regulated data (e.g. BASC, customs) | Return OR destruction per BASC retention rule | As above | |
| Backup copies | Destruction within the contracted retention window after the operational data is returned or destroyed | Supplier attestation; backup-system log where accessible | |
| Embeddings, vectors, derived data | Destruction or anonymisation | Supplier attestation describing the technical action | |
| Logs and monitoring data | Retention per contract; destruction at end of retention | Supplier attestation | |
| Documentation and configuration | Return or destruction | As above | |

The certificate of destruction states: the items destroyed, the method (e.g. NIST SP 800-88 Clear / Purge / Destroy), the date, and the signing authority on the supplier side. For personal data, the certificate cites the GDPR Article 28(3)(g) obligation (or jurisdictional equivalent).

### Section 4: Service-continuity handover

| Item | Required content |
| --- | --- |
| Successor arrangement | Identification of the successor (in-house, alternate supplier, customer-managed) |
| Knowledge transfer evidence | Documentation handover; recorded sessions; runbook updates |
| Production data migration | Successful migration confirmed by data integrity check |
| Customer notification | Where the change affects customer-facing service, notification record |
| Regulator notification | Where required by sector regulator |
| Hand-off acceptance | Sign-off by the receiving role |
| Cut-over timing | Date and time of effective transition |

### Section 5: Residual obligations

| Obligation type | Description | Owner role | Review cadence | End date |
| --- | --- | --- | --- | --- |
| Confidentiality | Per the contract's surviving confidentiality clause | Legal | Annual | Per contract |
| Non-disclosure | Per any in-force NDA | Legal | Annual | Per NDA |
| Warranty | Per any in-force warranty | Service Owner | Per warranty | Per warranty |
| Indemnity | Per any in-force indemnity | Legal | Annual | Per contract |
| Audit rights | Where the contract permits post-termination audit | Internal Audit | As needed | Per contract |
| Source-code escrow | If applicable; release conditions | Procurement | Annual | Per escrow agreement |
| Sub-processor obligations | Where the supplier was a processor; sub-processor offboarding cascade | Privacy Officer | Until cascade complete | Per cascade |
| Regulatory record retention | Records the organisation must keep beyond the relationship | Records Management | Annual | Per retention schedule |
| Insurance | Tail coverage where applicable | Insurance / Risk | Annual | Per policy |
| Outstanding payment or refund | Per contract | Procurement | Until resolved | Until resolved |

### Section 6: Contract closure

| Item | Status |
| --- | --- |
| All deliverables accepted | |
| Final invoice issued and paid | |
| Any disputed amounts resolved or escalated | |
| Acceptance into service revoked where applicable | |
| Asset return (devices, badges, manuals) completed | |
| Subscription auto-renewal disabled | |
| Vendor records updated to "offboarded" status | |
| Single source of contact for residual matters identified | |

### Section 7: Post-exit review

A short review within 30 business days of completion records:

1. What worked well in the offboarding process.
2. Gaps identified (access not revoked timely; data return delays; documentation gaps).
3. Corrective actions for future offboardings; tracked in the corrective action register.
4. Whether the supplier's exit-strategy clauses operated as intended.
5. Whether any concentration risk position has changed as a result of the exit.

### Section 8: Approval

| Approver role | Signature evidence | Date |
| --- | --- | --- |
| Supplier Relationship Owner | | |
| Supplier Risk Maintainer | | |
| Service Owner | | |
| Privacy Officer (if personal data) | | |
| Legal Counsel (if material) | | |
| CISO (Tier 1 exits) | | |

The approval set confirms that the offboarding evidence record is complete, verified, and archived per the records retention standard.

---

## Operating expectations

1. Each completed offboarding produces a record from this template; partial completions are escalated to the Supplier Risk Maintainer.
2. The completed record is archived for at least seven years; longer where contractual or regulatory rules apply.
3. The record is reviewed at the next supplier risk register review cycle and feeds the year-end supplier risk report.
4. Forced exits (insolvency, breach) follow an abbreviated path where the supplier's cooperation cannot be assumed; the record documents the actions the organisation took unilaterally.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| GDPR / UK GDPR | Article 28(3)(g) | Processor return-or-delete obligation |
| DORA | Article 28 (exit strategies) | Mandatory exit strategy and termination procedure |
| EBA Guidelines on outsourcing arrangements | EBA/GL/2019/02 | Exit strategy detail |
| ISO/IEC 27036 | Information security for supplier relationships | Termination |
| ISO 28000 | Security management for supply chains | Termination |
| NIST SP 800-88 Rev 1 | Guidelines for Media Sanitization | Destruction method |
| CSA CCM v4.1 | IPY-04, IPY-05 (interoperability and portability) | Exit assistance |
| ISO/IEC 27001:2022 | A.5.22 (information security in supplier relationships) | Closure |

---

## Limitations

This template is a public-domain structural baseline. Adopting organisations populate per-supplier evidence rows, integrate with their procurement and HR offboarding systems, and adapt the residual-obligations section to their contract templates. The template is not a substitute for legal review of an in-progress termination dispute and does not address insolvency-specific procedures (e.g. administration, liquidation) which require specialist counsel.

---

**End of Document**
