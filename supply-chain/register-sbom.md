# Software Bill of Materials Register

**Document Title:** Software Bill of Materials Register\
**Document Type:** Register\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** Supplier Risk Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`supply-chain/framework-supplier-and-cloud-governance.md`](framework-supplier-and-cloud-governance.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](standard-supplier-security-and-privacy-assurance.md), [`supply-chain/procedure-fourth-party-and-nth-party-risk.md`](procedure-fourth-party-and-nth-party-risk.md), [`dev-security/standard-software-composition-analysis.md`](../dev-security/standard-software-composition-analysis.md), [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md), [`security/procedure-vulnerability-management.md`](../security/procedure-vulnerability-management.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md)\
**Classification:** Public\
**Category:** Supply Chain Governance\
**Review Frequency:** Quarterly and continuously updated upon every production build or supplier SBOM refresh\
**Repository Path:** [`supply-chain/register-sbom.md`](register-sbom.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register tracks Software Bill of Materials (SBOM) artefacts for the organisation's internally-built software, for purchased commercial software, and for open-source dependencies in use. The register is the navigation layer over an SBOM repository; the actual SBOM artefacts (CycloneDX, SPDX) are stored as machine-readable files referenced by the register.

A populated SBOM register identifies real products and components and is sensitive operational data; populate, classify, and store internally.

---

## Scope

This register covers:

1. **Internally built software** released or deployed to production, test, or distribution channels.
2. **Commercial off-the-shelf software** purchased from a supplier and deployed in any tier.
3. **Open-source software** whose components are not transitively covered by another supplier's SBOM.
4. **Container images** built by the organisation or pulled from external registries.
5. **Embedded software in physical products** the organisation manufactures.
6. **Cloud-deployed runtime environments** to the extent the supplier discloses the SBOM.

It does not cover SaaS where the supplier delivers software as a service without distribution; SaaS suppliers are governed by the broader supplier assurance standard.

---

## Register schema

Each row records one SBOM. Mandatory fields:

| Field | Description |
| --- | --- |
| SBOM ID | Unique identifier |
| Product name | Internal product name; not vendor name in the public template |
| Product version | Specific build, release, or container tag |
| Producer | Internal team or supplier responsible for producing the SBOM |
| Type | Internally built; commercial purchased; open-source; container; embedded; cloud runtime |
| Format | CycloneDX, SPDX, or other format the supplier produces |
| Format version | Specific version of the format |
| Generation method | Build-time generation, post-build analysis, supplier-provided |
| Storage location | Path or URL to the machine-readable artefact in the internal SBOM repository |
| Hash | Cryptographic hash of the SBOM artefact |
| Generation timestamp | When this SBOM was generated |
| Receipt timestamp | When this SBOM was received and stored (for supplier-provided) |
| Coverage statement | What the SBOM contains: direct dependencies only, transitive included, build tools included, OS layers included, etc. |
| Known gaps | Documented exclusions (e.g. proprietary embedded components without source) |
| Linked vulnerability scan | Reference to the latest vulnerability scan against this SBOM |
| VEX statements | Vulnerability Exploitability eXchange entries that adjust the applicability of CVEs to this product |
| Linked supplier | If supplier-provided, the supplier identifier in the supplier risk register |
| Linked deployment | Where this product is currently deployed or distributed |
| Distribution recipients | If the organisation provides the SBOM to customers, the recipient class |
| Status | Active, superseded, retired |
| Next refresh due | Per the refresh cadence |

---

## SBOM acquisition

The organisation obtains SBOMs through three paths.

### Path 1: produce at build time (internally built software)

| Requirement | Detail |
| --- | --- |
| Build pipeline produces an SBOM artefact on every production build | Per [`dev-security/standard-software-composition-analysis.md`](../dev-security/standard-software-composition-analysis.md) |
| Format | CycloneDX or SPDX |
| Coverage | All direct dependencies plus transitive dependencies present in the runtime artefact |
| Container coverage | Where the artefact is a container, the SBOM covers base image layers and added layers |
| Signing | The SBOM is signed alongside the artefact (typically using sigstore / cosign or equivalent) |
| Storage | Stored in the SBOM repository with the artefact reference |

### Path 2: request from suppliers (commercial purchased software)

| Requirement | Detail |
| --- | --- |
| Tier 1 critical suppliers | SBOM required as a contractual deliverable; refreshed on every minor and major release; provided at minimum quarterly |
| Tier 2 high suppliers | SBOM required as a contractual deliverable; refreshed on every major release |
| Tier 3 moderate suppliers | SBOM requested; provided on best efforts |
| Tier 4 low suppliers | Not required |
| Format | CycloneDX or SPDX accepted; HBOM (hardware) accepted where applicable |
| Coverage | Components included in the product; the supplier states their coverage of transitive dependencies |
| Receipt | SBOM received through a secure channel; stored on receipt with hash recorded |

### Path 3: produce post-deployment (open source and where supplier does not provide)

| Requirement | Detail |
| --- | --- |
| Container scanning produces an SBOM-equivalent inventory | Per the container scanning tool in use |
| Operating system package inventory | For long-lived servers and appliances |
| Embedded firmware analysis | For physical products where the supplier does not provide an SBOM |

---

## Linkage to vulnerability management

Each SBOM is continuously cross-referenced against published vulnerability data:

1. **Daily refresh.** The SBOM-to-CVE matching is refreshed at least daily; new vulnerabilities against components in the SBOM are surfaced.
2. **Severity routing.** Critical and High vulnerabilities route to the responsible owner (development team for internal; supplier and procurement for commercial; security operations for OS-level).
3. **VEX integration.** VEX statements (from the supplier or from internal analysis) adjust applicability. A "not affected" VEX statement with rationale closes a CVE finding for the specific product.
4. **Remediation SLA.** Per the SCA standard and the vulnerability management procedure.

---

## Linkage to procurement and acceptance

1. New software is not accepted into the production environment without an SBOM (or a documented exception for path 3 cases).
2. The acceptance-into-service gate (per [`security/policy-acceptance-into-service.md`](../security/policy-acceptance-into-service.md)) includes SBOM presence and coverage verification.
3. Procurement contracts at Tier 1 and Tier 2 include the SBOM deliverable clause and the refresh cadence.

---

## Linkage to customer-facing transparency

Where the organisation is a software vendor or delivers software-bearing products to customers:

1. Customer contracts at the equivalent tier include the SBOM as a customer-deliverable obligation under EU Cyber Resilience Act, US Executive Order 14028, and applicable sector regulation.
2. Customer-distributed SBOMs are produced from the internal SBOM with consistent format and coverage statement.
3. Customer queries about specific CVEs are answered using the corresponding VEX statement.

---

## Operating expectations

1. The Supplier Risk Maintainer reviews the register quarterly for completeness against the supplier portfolio.
2. SBOM gaps for Tier 1 or Tier 2 suppliers are escalated to the CISO and Procurement for contractual remediation.
3. The SBOM repository is treated as production data: access-controlled, logged, backed up.
4. SBOM data classification balances utility against disclosure risk; internal use is the default, customer distribution follows the customer contract.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| NTIA Minimum Elements of a Software Bill of Materials | NTIA 2021 | SBOM baseline |
| US Executive Order 14028 | EO 14028 §4 | Federal SBOM expectation |
| CISA SBOM guidance | Multiple | SBOM operationalisation |
| EU Cyber Resilience Act | Regulation (EU) 2024/2847 | Mandatory product-level SBOM |
| NIST SP 800-218 | SSDF PW.4, PW.7, PW.8 | Secure software development; SBOM production |
| NIST SP 800-161 Rev 1 | Cybersecurity Supply Chain Risk Management | Supply chain |
| ISO/IEC 5230 (OpenChain) | Open source compliance | OSS programme baseline |
| CycloneDX | OWASP standard | SBOM format |
| SPDX | Linux Foundation standard | SBOM format |
| VEX | CycloneDX / OpenVEX | Vulnerability exploitability |
| SLSA | Supply-chain Levels for Software Artifacts | Build integrity |

---

## Limitations

This register is a CC BY-SA 4.0 structural baseline. SBOM coverage is bounded by the producer's ability and willingness to generate accurate, complete artefacts; transitive dependency visibility decreases with sub-tier supplier maturity. The register supports vulnerability and supply-chain integrity programmes but does not itself remediate vulnerabilities or attest to product security.

---

**End of Document**
