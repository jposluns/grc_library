# Sanctions and Export-Control Screening Standard

**Document Title:** Sanctions and Export-Control Screening Standard\
**Document Type:** Standard\
**Version:** 1.0.1\
**Date:** 2026-07-02\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/policy-legal-and-regulatory-compliance.md`](policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](register-global-regulatory-applicability.md), [`compliance/procedure-mergers-acquisitions-due-diligence.md`](procedure-mergers-acquisitions-due-diligence.md), [`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md), [`supply-chain/procedure-fourth-party-and-nth-party-risk.md`](../supply-chain/procedure-fourth-party-and-nth-party-risk.md), [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md), [`governance/register-role-authority.md`](../governance/register-role-authority.md)\
**Classification:** Public\
**Category:** Compliance Management\
**Review Frequency:** Annual and upon material change to sanctions, export-control, or denied-party-list regulatory regimes\
**Repository Path:** [`compliance/standard-sanctions-and-export-control-screening.md`](standard-sanctions-and-export-control-screening.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose and scope

### 1.1 Purpose

This standard defines the minimum control structure for screening the organization's counterparties, transactions, products, and ownership relationships against economic-sanctions and export-control regimes, and for verifying beneficial ownership to the extent sanctions screening requires it. It exists because sanctions and export-control exposure is currently addressed only incidentally across the corpus (as a trigger in supplier and merger procedures), with no dedicated screening method.

This standard is a governance baseline and is **not legal advice**. Sanctions and export-control law is jurisdiction-specific, fast-moving, and carries strict-liability exposure in several regimes; screening failures can result in significant penalties. Adopting organizations must obtain qualified sanctions and export-control legal counsel for the regimes that bind them and for any transaction in doubt. This standard defines control structure, not a substitute for licensed advice or for the authoritative text of any regime.

### 1.2 Scope

This standard applies to screening across the relationships and events that create sanctions or export-control exposure: customer and counterparty onboarding, supplier and third-party engagement, transactions and payments, cross-border movement of goods, software, technology, and technical data, and mergers, acquisitions, and investments. It covers denied-party and restricted-party screening, sanctioned-jurisdiction and sectoral exposure, export classification and licensing referral, and beneficial-ownership verification for sanctions purposes.

**Scope fence with anti-money-laundering.** This standard governs sanctions and export-control screening. It does not define the organization's anti-money-laundering and counter-terrorist-financing (AML/CFT) programme (customer due diligence, suspicious-activity reporting, transaction monitoring), which is sector-conditional and governed separately. Beneficial-ownership verification here is scoped to sanctions-ownership screening, not full AML customer due diligence.

**Jurisdiction applicability.** Which sanctions and export-control regimes bind the organization depends on its nexus (for example its incorporation and establishment, the citizenship or residence of its people, its currencies of settlement, and the origin of its goods and technology). The applicable regimes are *[adopter-defined]* and recorded in the [global regulatory applicability register](register-global-regulatory-applicability.md). This standard names the major regimes structurally; it does not assert that any one jurisdiction's rules bind every adopter.

## 2. Governance and roles

| Role | Responsibility |
| --- | --- |
| Chief Compliance Officer | Owns this standard and the screening programme; accountable for escalation and for engaging sanctions counsel. |
| Screening operations | Runs onboarding, periodic, and transaction screening; performs initial match review and false-positive disposition. |
| Legal Counsel (sanctions and export-control) | Determines applicable regimes, adjudicates true matches, and owns licensing and voluntary-disclosure decisions. |
| Chief Risk Officer | Maintains the consolidated view of sanctions and export-control risk and its place in the risk register. |
| Business and transaction owners | Submit counterparties and transactions for screening before commitment; do not proceed past a positive screen without disposition. |

The assignment above is the default; an adopting organization maps these to its own role inventory per [`governance/register-role-authority.md`](../governance/register-role-authority.md).

## 3. Sanctions regimes in scope

The organization screens against the consolidated lists and programmes of the sanctions authorities whose regimes apply to it. The major regimes, named structurally (the authoritative list contents and their versions change continually and are obtained from each authority, never from this document):

- **United States: the Office of Foreign Assets Control (OFAC)**, including the Specially Designated Nationals and Blocked Persons (SDN) list and the sectoral and other non-SDN restricted lists.
- **United Nations Security Council** consolidated sanctions list.
- **European Union** consolidated sanctions list.
- **United Kingdom: the Office of Financial Sanctions Implementation (OFSI)** consolidated list.
- **Other applicable national or regional regimes** as determined by the organization's nexus (*[adopter-defined]*).

The organization screens for direct listing, for ownership or control by listed persons (Section 6), and for nexus to comprehensively sanctioned jurisdictions and sectoral restrictions. The specific in-scope regimes, list sources, and screening-tool configuration are *[adopter-defined]*.

## 4. Export-control regimes in scope

Where the organization produces, handles, or moves controlled goods, software, technology, or technical data, it screens against the applicable export-control regimes, named structurally:

- **United States Export Administration Regulations (EAR)**, administered by the Bureau of Industry and Security, covering dual-use items and the associated restricted-party lists.
- **United States International Traffic in Arms Regulations (ITAR)**, administered by the Directorate of Defense Trade Controls, covering defence articles and services.
- **European Union dual-use** export-control regulation.
- The **Wassenaar Arrangement** and other multilateral export-control regimes as the international context for national controls.

Export classification (determining whether and how an item is controlled), licensing determination, and deemed-export considerations for technology and technical data are *[adopter-defined]* against the regimes that bind the organization, and are referred to Legal Counsel where control or licensing is uncertain. This standard does not assert specific classification codes or control-list entries.

## 5. Denied-party and restricted-party screening

1. **Screen at onboarding.** Every new customer, supplier, third party, and counterparty is screened before the relationship is established.
2. **Re-screen periodically, against current lists.** Existing counterparties are re-screened on a defined cadence (*[adopter-defined]*) and whenever the applicable lists are updated, because list membership changes without notice. Screening is performed against the current version of each list, so keeping list ingestion and refresh current is itself a control.
3. **Re-screen on a material event.** Beyond the periodic cadence, re-screen a counterparty when a material event changes its exposure (for example, a new sanctions designation, or a change in the counterparty's jurisdiction of operation), rather than waiting for the next scheduled cycle.
4. **Screen at transaction.** Transactions, payments, and shipments are screened before execution where the counterparty, destination, or item creates exposure.
5. **Define match handling.** Screening produces potential matches against a configured match threshold; each potential match is reviewed and dispositioned (false positive with recorded rationale, or escalation) before the relationship or transaction proceeds.
6. **Block on a true match.** A confirmed match to a sanctioned person, or exposure to a sanctioned jurisdiction or sector, stops the relationship or transaction; the matter is escalated to Legal Counsel, and assets are frozen or the transaction rejected as the applicable regime requires.

## 6. Beneficial-ownership and ultimate-beneficial-owner verification

Sanctions screening reaches beyond named parties to the persons who own or control them.

1. **Identify beneficial owners.** For counterparties, identify the natural persons who ultimately own or control the entity, including through layered or indirect ownership, to the ownership threshold the applicable regime sets (*[adopter-defined]*; a 25 percent threshold is common for beneficial-ownership identification, but the governing threshold is jurisdiction-set).
2. **Apply ownership-aggregation rules.** Per OFAC guidance, an entity that is owned 50 percent or more, in the aggregate, by one or more blocked persons is itself treated as blocked even if it is not separately listed; aggregate indirect and combined ownership accordingly. Other regimes apply their own ownership and control tests, which the organization applies as they bind it.
3. **Screen the owners.** Identified beneficial owners and controllers are screened against the Section 3 regimes, not only the entity itself.
4. **Re-verify on change.** Ownership and control are re-verified on a material change in ownership and on the periodic cadence.

## 7. Screening workflow and disposition

| Step | Requirement |
| --- | --- |
| Submission | The business or transaction owner submits the counterparty, owner, transaction, or item for screening before commitment. |
| Match review | Screening operations reviews each potential match; clear false positives are dispositioned with a recorded rationale, and unresolved or likely matches are escalated. |
| Segregation of duties | The person who clears or dispositions a potential match is not the sole authority who releases the held relationship or transaction; true-match clearance and the release of a blocked item require independent review (four-eyes), so a single operator cannot self-clear a hit. |
| Escalation | Escalated matches go to Legal Counsel for adjudication against the applicable regime. |
| Blocking, freezing, rejecting | On a true match or sanctioned-jurisdiction or sectoral exposure, the relationship or transaction is blocked, assets are frozen, or the transaction is rejected as the regime requires. |
| Licensing and authorization | Where a licence, authorization, or exemption may permit an otherwise-prohibited dealing, Legal Counsel determines and pursues it; the dealing does not proceed without it. |
| Reporting and disclosure | Reports to the relevant authority (for example blocked-property or rejected-transaction reports) and any voluntary self-disclosure are made on the regime's required timelines (*[adopter-defined]*; the organization records the binding reporting timeline for each regime that applies to it), owned by Legal Counsel. |

The organization does not proceed past a positive screen on the basis of commercial pressure; the disposition gates this standard defines are mandatory.

## 8. Recordkeeping and retention

Screening evidence (what was screened, against which lists, when, the match results, and the disposition rationale), escalation and adjudication records, licensing records, and any reports filed are retained as the evidence of the screening programme, per the [records retention and destruction standard](../governance/standard-records-retention-and-destruction.md) and any longer retention the applicable regime requires (*[adopter-defined]*; several regimes set multi-year minimums). The records support both internal assurance and any regulatory examination.

## 9. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO 37301:2021 | Compliance management systems | The compliance-management discipline within which sanctions and export-control obligations are identified, controlled, and assured. |
| ISO 31000:2018 | Risk management principles and guidelines | The risk basis for the screening cadence and the prioritization of exposure. |
| COBIT 2019 | APO12 (managed risk) | Governance of the compliance and sanctions risk this standard controls. |
| NIST CSF 2.0 | GV (Govern) function | The governance and risk-management outcomes the screening programme supports. |
| Sanctions and export-control regulatory regimes | OFAC, UN, EU, UK OFSI sanctions; US EAR and ITAR; EU dual-use (named structurally) | The external regulatory drivers; adopters confirm the current authoritative text and applicability for their jurisdictions, which this document does not reproduce. |

## 10. Limitations

This standard is a CC BY-SA 4.0 structural baseline and is not legal advice. Sanctions and export-control regimes are jurisdiction-specific and change without notice; this standard names the major regimes structurally and does not reproduce, version, or pin any list, classification code, or regulation, all of which the organization obtains from the authoritative source for its jurisdictions. Adopting organizations must determine which regimes bind them, populate the *[adopter-defined]* thresholds, cadences, licensing authorities, and reporting timelines, configure their own screening tooling, and obtain qualified legal counsel for adjudication, licensing, and disclosure. Beneficial-ownership verification here is scoped to sanctions screening and does not constitute a full anti-money-laundering customer-due-diligence programme.

---

**End of Document**
