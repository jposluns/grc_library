# Telecommunications Sector Requirements Annex

**Document Title:** Telecommunications Sector Requirements Annex\
**Document Type:** Annex\
**Version:** 0.0.2\
**Date:** 2026-05-28\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/README.md`](README.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](../register-global-regulatory-applicability.md), [`compliance/annex-nis-2-implementation.md`](../annex-nis-2-implementation.md), [`security/policy-information-security.md`](../../security/policy-information-security.md), [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../../supply-chain/framework-supplier-and-cloud-governance.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md), [`privacy/policy-privacy-and-data-governance.md`](../../privacy/policy-privacy-and-data-governance.md)\
**Classification:** Public\
**Category:** Compliance: Sector-Specific\
**Review Frequency:** Annual and upon material licence, lawful-access, or sector-supervision change\
**Repository Path:** [`compliance/telecommunications/annex-telecommunications-sector-requirements.md`](annex-telecommunications-sector-requirements.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex identifies the overlay obligations that apply when the organisation operates a public electronic communications network or service, or provides services that depend on one. It covers network security, lawful interception, data retention, emergency calling and resilience, vendor and supply-chain restrictions, customer privacy under sector-specific rules, and number- and addressing-resource obligations.

This annex does not reproduce national licence conditions or regulator-published guidance. Adopting entities consume those from the national regulator (Ofcom in the UK, BNetzA in Germany, ACMA in Australia, FCC in the US, CRTC in Canada, ARCEP in France, AGCOM in Italy, equivalents elsewhere).

---

## Applicability triggers

This annex applies where the organisation:

1. Holds a telecoms licence or registration as a public electronic communications network or service provider.
2. Provides interpersonal communications services (number-based or number-independent).
3. Operates internet exchange points, top-level domain name registries, DNS service infrastructure, content delivery networks at scale, or other critical digital infrastructure.
4. Provides over-the-top messaging or voice that triggers regulatory parity rules in the applicable jurisdiction.
5. Operates managed services for any of the above on behalf of a regulated entity.

---

## Overlay area 1: sector cybersecurity obligations

Most jurisdictions impose telecoms-specific cybersecurity obligations that overlay general regimes (NIS 2 in the EU, the Telecommunications (Security) Act 2021 in the UK, equivalent national regimes).

| Obligation | Library support |
| --- | --- |
| Sector-specific cybersecurity duty | [`security/policy-information-security.md`](../../security/policy-information-security.md), supporting standards |
| Network and information system security (controls catalogue) | [`operations/standard-network-security-and-segmentation.md`](../../operations/standard-network-security-and-segmentation.md), [`operations/standard-cloud-security-configuration-baseline.md`](../../operations/standard-cloud-security-configuration-baseline.md), [`security/standard-data-loss-prevention.md`](../../security/standard-data-loss-prevention.md) |
| Security testing | [`security/standard-penetration-testing-and-red-team.md`](../../security/standard-penetration-testing-and-red-team.md) |
| Vulnerability management with telecoms-specific severity criteria | [`security/procedure-vulnerability-management.md`](../../security/procedure-vulnerability-management.md) |
| Incident notification to the sector regulator | Library incident procedure plus regulator-specific reporting template |
| Board accountability for security duty | [`governance/charter-governance-library.md`](../../governance/charter-governance-library.md), [`governance/register-role-authority.md`](../../governance/register-role-authority.md) |
| Annual sector security report | Outside library scope; regulator-template |
| Penalties for non-compliance | Jurisdiction-specific |

EU specifics: NIS 2 designates providers of public electronic communications networks or services as Essential entities; see the NIS 2 implementation annex.

UK specifics: Telecommunications (Security) Act 2021 plus the Electronic Communications (Security Measures) Regulations 2022 plus Ofcom code of practice. Two tiers of provider with differentiated obligations.

US specifics: CSRIC best practices, FCC cybersecurity reporting (forthcoming under recent NPRMs), CISA cyber incident reporting under CIRCIA when finalized.

---

## Overlay area 2: lawful interception and lawful-access cooperation

Telecoms providers are typically required to maintain technical interception capability and to cooperate with lawful access requests from law enforcement and national security authorities.

| Obligation | Library support |
| --- | --- |
| Interception capability per the national lawful-interception standard (e.g. ETSI 102 232 series; CALEA in the US) | Outside library scope; built into the network platform |
| Designated point of contact and 24/7 response | Library incident-coordination procedure with sector-specific contact roster |
| Lawful-access requests handled under documented procedure | Outside library scope; per-jurisdiction workflow with strong separation from commercial functions |
| Transparency reporting where permitted | Per the provider's transparency policy |
| Training and clearances for personnel handling lawful access | Library personnel security supports the baseline |

This obligation is national-security sensitive. Documentation, personnel, and infrastructure handling lawful access are typically separated from the commercial operation and subject to additional clearance and audit.

---

## Overlay area 3: data retention

Many jurisdictions impose specific telecoms-data-retention rules that overlay general privacy regimes. These rules are subject to ongoing legal challenge and vary materially by jurisdiction.

| Obligation | Library support |
| --- | --- |
| Retain defined categories of communications metadata for the statutory period | [`governance/standard-records-retention-and-destruction.md`](../../governance/standard-records-retention-and-destruction.md) provides the structure; the telecoms schedule is added as an overlay |
| Restrict access to retained data to authorised purposes | [`security/policy-identity-and-access-management.md`](../../security/policy-identity-and-access-management.md), [`security/standard-privileged-access-management.md`](../../security/standard-privileged-access-management.md) |
| Destroy after the statutory period | [`governance/register-data-retention-schedule.md`](../../governance/register-data-retention-schedule.md) |
| Provide statistics to the regulator | Per the regulator template |

EU: Court of Justice case law (Tele2 Sverige, La Quadrature du Net) restricts general retention; targeted retention may be lawful. National laws diverge.

UK: Investigatory Powers Act 2016 framework.

Canada: PIPEDA does not require telecoms data retention; lawful-access requests handled per the IPA-equivalent framework.

---

## Overlay area 4: customer privacy under sector rules

In addition to general privacy regimes (GDPR, UK GDPR, PIPEDA, equivalents), telecoms providers face sector-specific privacy rules.

| Obligation | Library support |
| --- | --- |
| ePrivacy obligations (cookies, traffic data, location data, marketing communications) | [`privacy/framework-consent-management.md`](../../privacy/framework-consent-management.md), [`privacy/register-cookie-and-tracker.md`](../../privacy/register-cookie-and-tracker.md) |
| Caller-line identification and presentation | Outside library scope |
| Directory enquiry and subscriber-information rules | Per regulator |
| Unsolicited marketing rules (PECR in UK; CAN-SPAM and TCPA in US; CASL in Canada) | [`privacy/template-privacy-notice.md`](../../privacy/template-privacy-notice.md) for transparency; product-specific configuration outside library |
| Location-based service consent | [`privacy/framework-consent-management.md`](../../privacy/framework-consent-management.md) |
| Subscriber identifier protection | [`security/standard-data-classification-and-handling.md`](../../security/standard-data-classification-and-handling.md) |

---

## Overlay area 5: emergency calling and resilience

Public communications providers must support emergency calling and operate to enhanced resilience standards.

| Obligation | Library support |
| --- | --- |
| Emergency calls always free, prioritized, and accessible | Outside library scope; network design |
| Caller location to emergency services per the national standard | Outside library scope |
| Battery backup on customer premises equipment per regulator | Outside library scope |
| Continuity targets and outage notification to regulator | [`resilience/framework-business-continuity-and-resilience.md`](../../resilience/framework-business-continuity-and-resilience.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](../../resilience/standard-business-continuity-and-disaster-recovery.md), [`resilience/plan-it-disaster-recovery.md`](../../resilience/plan-it-disaster-recovery.md) |
| Resilience reporting (e.g. ATIS Network Reliability Steering Committee) | Per regulator |

---

## Overlay area 6: vendor and supply-chain restrictions

National security concerns have led to vendor- and country-specific restrictions in telecoms supply chains.

| Obligation | Library support |
| --- | --- |
| Approved-vendor list per national security guidance | [`supply-chain/framework-supplier-and-cloud-governance.md`](../../supply-chain/framework-supplier-and-cloud-governance.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md) |
| Specific vendor or country exclusions | National regime; e.g. UK Designated Vendor Direction; US Section 889 NDAA, Rip-and-Replace; EU 5G Toolbox |
| Lifecycle attestation for critical components | [`dev-security/standard-software-composition-analysis.md`](../../dev-security/standard-software-composition-analysis.md) for SBOM elements |
| Supply chain integrity reporting to the regulator | Per regulator |

---

## Overlay area 7: numbering and addressing resources

Numbering plans and number portability are regulated.

| Obligation | Library support |
| --- | --- |
| Allocation, return, and porting of numbering resources per the national numbering plan | Outside library scope |
| IP address allocation per RIR policy where the provider operates routing | Outside library scope |
| Anti-fraud and anti-spoofing measures (STIR / SHAKEN in North America; equivalents elsewhere) | Outside library scope; specialist platform |

---

## Library gaps requiring additional documentation

1. **Telecoms-specific cybersecurity duty register** mapping the local statute or licence condition to library artefacts.
2. **Lawful interception procedure and roster**, with separation from commercial operations.
3. **Telecoms data retention schedule** approved against the local statute.
4. **Emergency calling resilience procedure** with outage notification windows.
5. **Approved-vendor list and exclusion list** per national security guidance.
6. **Numbering plan administration procedure.**
7. **Sector-specific incident notification templates** per regulator.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| EU EECC | Directive (EU) 2018/1972 | European Electronic Communications Code |
| EU ePrivacy Directive | 2002/58/EC and national transpositions | Sector privacy |
| EU NIS 2 | (EU) 2022/2555 | Cybersecurity for public electronic communications |
| UK Telecommunications (Security) Act 2021 | UK statute | Security duty |
| UK PECR | SI 2003/2426 | ePrivacy transposition |
| US Communications Act, FCC rules | 47 CFR | Sector framework |
| US CALEA | 47 USC 1001-1010 | Lawful interception |
| Canada Telecommunications Act | RSC 1993 c 38 | Sector framework |
| ETSI TS 102 232 series | ETSI | Lawful interception standards |
| ITU-T Recommendations | ITU | International telecoms standards |

---

## Limitations

This annex is a CC BY-SA 4.0 navigation aid. Telecoms compliance requires alignment to the national licence conditions, the regulator's published code of practice, the national security service's specific requirements for lawful access, and sector-specific incident reporting. Adopting providers consult the national regulator, their licence documentation, and specialist counsel. This annex is not legal advice and does not address national-security-sensitive obligations in detail because such obligations are typically not public.

---

**End of Document**
