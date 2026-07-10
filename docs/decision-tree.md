# Adopter Decision Tree

**Document Title:** Adopter Decision Tree\
**Document Type:** Guide\
**Version:** 1.0.18\
**Date:** 2026-07-10\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`docs/adopter-guide.md`](adopter-guide.md), [`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md), [`README.md`](../README.md), [`docs/worked-example.md`](worked-example.md)\
**Classification:** Public\
**Category:** Documentation\
**Review Frequency:** Annual and upon material change to the library structure or the adoption model\
**Repository Path:** [`docs/decision-tree.md`](decision-tree.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Overview

A structured navigator for adopting organizations: "I have these characteristics; which library documents should I read first, in what order?" It is a controlled reference artefact that complements [`docs/adopter-guide.md`](adopter-guide.md): the adopter guide gives general adoption principles; this document gives a sequenced reading order.

### Where this fits among the adopter entry points

The canonical front door for adopters is [`docs/portal.md`](portal.md) (audience-keyed grouping by role). This decision tree is one of five deeper-dive paths that branch off the portal; it answers "in what order should I read the documents that apply to me?". The other four are [`docs/adopter-guide.md`](adopter-guide.md) (fork-and-adapt principles), [`docs/template-quickstart.md`](template-quickstart.md) (what to copy on Day 1), [`docs/template-startup-roadmap.md`](template-startup-roadmap.md) (the long-form module-composition workbook), and [`docs/template-implementation-roadmap.md`](template-implementation-roadmap.md) (calendar phasing). The portal's "Other entry points and when to use them" table picks the right path by question; see the portal Overview.

---

## How to use this guide

1. Identify your organization's characteristics across the dimensions in **Section 1** (size, sector, jurisdiction, regulated activities, technology footprint).
2. Read the **Section 2** baseline that applies to every adopter, in the order listed.
3. Layer the **Section 3** sector-conditional content based on your sector (only the sub-directories that apply).
4. Layer the **Section 4** jurisdiction-conditional content based on where you operate and where your data subjects are.
5. Layer the **Section 5** technical-capability content based on your stack and operations.
6. Use the **Section 6** roadmap suggestions to phase adoption over 30 / 90 / 180 days (this tree's own starter / mid-market / enterprise sets in Sections 6.1 to 6.3, the starter set applying to any adopter; a deliberately distinct phasing from the implementation roadmap's 90 / 180 / 365-day reference calendar, which paces module composition rather than adopter size).

For terms and acronyms used below, see [`governance/register-glossary.md`](../governance/register-glossary.md). For known coverage gaps, see [`governance/register-coverage-gaps.md`](../governance/register-coverage-gaps.md).

---

## 1. Adopter dimensions

Answer each of the following to determine your reading path.

### 1.1 Organization size

- **Small** (under 50 employees)
- **Mid-market** (50 to 500)
- **Large enterprise** (500 to 5000)
- **Multi-national enterprise** (5000+)

These bands select reading paths in this document. They are a different axis from the [`docs/adopter-guide.md`](adopter-guide.md) Tier 1 sizing cue ("under approximately 200 staff"), which decides how many documents to START with; a 150-person organization is Mid-market here and, where the guide's other cues also hold (low regulatory exposure, no high-risk AI in production), still a Tier 1 starter there.

### 1.2 Industry sector (select all that apply)

- Logistics (transportation, warehousing, freight forwarding, customs brokerage)
- Financial services (banks, investment, insurance, payments, financial market infrastructure (FMI))
- Healthcare (providers, payers, medtech, healthcare platforms)
- Energy and utilities
- Telecommunications
- Public sector (or service provider to public sector)
- Other / general technology

### 1.3 Jurisdictional footprint (select all that apply)

- European Union
- United Kingdom
- United States (federal)
- United States (state: California, New York, others)
- Canada
- Australia / New Zealand
- Singapore / South-East Asia
- Japan / Korea
- China
- Latin America
- Other

### 1.4 Regulated activities (select all that apply)

- Process personal data of EU residents (GDPR)
- Process personal data of UK residents (UK GDPR)
- Process personal data of California residents (CCPA/CPRA)
- Process personal data of Canadian residents (PIPEDA / Quebec Law 25)
- Operate as a financial-services entity in the EU (DORA in scope)
- Publicly-traded in the US (SOX in scope)
- Provide cloud services to US federal agencies (FedRAMP in scope)
- Operate as a healthcare provider/payer in the US (HIPAA in scope)
- Designated essential or important entity in EU (NIS 2 in scope)
- Rely on the EU Digital Identity Wallet or provide trust services in the EU (eIDAS in scope)
- Participate in a trusted-trader programme (BASC, CTPAT, AEO, PIP)
- Develop, deploy, or procure AI systems (EU AI Act, ISO/IEC 42001 in scope)

### 1.5 Technology footprint

- Cloud-only / cloud-native
- Hybrid (cloud + on-premises)
- On-premises-dominant
- Operational technology / industrial control systems present
- AI/ML in production
- Multi-cloud
- Containerized / Kubernetes

---

## 2. Universal baseline (every adopter reads these)

These documents apply regardless of size, sector, or jurisdiction. Read in this order.

### 2.1 Orientation (read first)

1. [`README.md`](../README.md): repository overview, structure, adoption posture. Acronyms in this file are expanded at first occurrence, so glossary lookup is rarely needed while reading.
2. [`docs/adopter-guide.md`](adopter-guide.md): general adoption principles. Same first-occurrence expansion convention.
3. [`governance/register-glossary.md`](../governance/register-glossary.md): acronym reference. Open this if you encounter an unexplained acronym in any document; the orientation files above expand acronyms inline, so glossary lookup is reserved for the deeper-domain documents in §2.2 and beyond.
4. [`governance/register-coverage-gaps.md`](../governance/register-coverage-gaps.md): what the library does not yet cover.

### 2.2 Governance core

5. [`governance/charter-governance-library.md`](../governance/charter-governance-library.md): library authority model.
6. [`governance/register-role-authority.md`](../governance/register-role-authority.md): the roles the library uses; you will map these to people in your organization.
7. [`governance/framework-document-architecture-and-interrelationship.md`](../governance/framework-document-architecture-and-interrelationship.md): how documents relate.
8. [`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md): comprehensive machine-readable register of every document with type, domain, status, and related artefacts. For audience-keyed navigation, use [`docs/portal.md`](portal.md) (the canonical entry point); the document index is the deeper-dive register for readers who already know what they are looking for.

### 2.3 Risk and compliance foundation

9. [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md): enterprise risk policy.
10. [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md): risk methodology.
11. [`compliance/policy-compliance-and-audit-management.md`](../compliance/policy-compliance-and-audit-management.md): compliance management.
12. [`compliance/policy-legal-and-regulatory-compliance.md`](../compliance/policy-legal-and-regulatory-compliance.md): legal and regulatory tracking.

### 2.4 Security foundation

13. [`security/policy-information-security.md`](../security/policy-information-security.md): security policy.
14. [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md): data classification.
15. [`security/policy-identity-and-access-management.md`](../security/policy-identity-and-access-management.md): IAM foundation.
16. [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md): incident response.

### 2.5 Privacy foundation (where personal data is processed)

17. [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md): privacy policy.
18. [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../privacy/procedure-privacy-impact-and-cross-border-transfer.md): PIA procedure.
19. [`privacy/annex-privacy-jurisdiction-index.md`](../privacy/annex-privacy-jurisdiction-index.md): navigation into per-jurisdiction privacy annexes.

### 2.6 Resilience foundation

20. [`resilience/standard-business-continuity-and-disaster-recovery.md`](../resilience/standard-business-continuity-and-disaster-recovery.md): BC/DR standard.
21. [`resilience/plan-business-continuity-and-crisis-management.md`](../resilience/plan-business-continuity-and-crisis-management.md): BC/CM plan template.

### 2.7 Supplier and third-party foundation

22. [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md): supplier governance.
23. [`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md): due diligence procedure.

---

## 3. Sector-conditional content

Read the sub-section matching your sector. Skip the others.

### 3.1 If logistics

Read the sector-overview annex first, then the programme overlays for programmes your organization participates in.

1. [`compliance/logistics/README.md`](../compliance/logistics/README.md): sector + programme index.
2. [`compliance/logistics/annex-logistics-sector-requirements.md`](../compliance/logistics/annex-logistics-sector-requirements.md): sector overview.
3. Then the trusted-trader programmes you participate in:
   - **CTPAT (US)**: [`compliance/logistics/register-ctpat-united-states-it-controls.md`](../compliance/logistics/register-ctpat-united-states-it-controls.md) and [`compliance/logistics/register-ctpat-united-states-msc-controls.md`](../compliance/logistics/register-ctpat-united-states-msc-controls.md)
   - **AEO-UK**: [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](../compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md) and [`compliance/logistics/procedure-aeo-united-kingdom-self-assessment.md`](../compliance/logistics/procedure-aeo-united-kingdom-self-assessment.md)
   - **PIP (Canada)**: [`compliance/logistics/register-pip-canada-controls.md`](../compliance/logistics/register-pip-canada-controls.md)
   - **BASC (multi-country)**: [`compliance/logistics/annex-basc-programme-overview.md`](../compliance/logistics/annex-basc-programme-overview.md), [`compliance/logistics/policy-basc-information-security.md`](../compliance/logistics/policy-basc-information-security.md), [`compliance/logistics/register-basc-it-responsibilities.md`](../compliance/logistics/register-basc-it-responsibilities.md), [`compliance/logistics/register-basc-it-compliance-kpis.md`](../compliance/logistics/register-basc-it-compliance-kpis.md)
4. [`compliance/logistics/template-trade-compliance-gap-assessment.md`](../compliance/logistics/template-trade-compliance-gap-assessment.md): gap-assessment template across programmes.

### 3.2 If financial services

1. [`compliance/financial-services/README.md`](../compliance/financial-services/README.md): sector index.
2. [`compliance/financial-services/annex-financial-services-sector-requirements.md`](../compliance/financial-services/annex-financial-services-sector-requirements.md): sector overview.
3. If EU-regulated: [`compliance/financial-services/annex-dora-implementation.md`](../compliance/financial-services/annex-dora-implementation.md): DORA implementation.
4. If US publicly-traded: [`compliance/financial-services/annex-sox-itgc.md`](../compliance/financial-services/annex-sox-itgc.md): SOX IT general controls.

### 3.3 If healthcare

1. [`compliance/healthcare/README.md`](../compliance/healthcare/README.md): sector index.
2. [`compliance/healthcare/annex-healthcare-sector-requirements.md`](../compliance/healthcare/annex-healthcare-sector-requirements.md): sector overview.
3. If subject to US HIPAA: [`compliance/healthcare/annex-healthcare-united-states.md`](../compliance/healthcare/annex-healthcare-united-states.md): US HIPAA operational overlay.

### 3.4 If energy and utilities

1. [`compliance/energy-and-utilities/README.md`](../compliance/energy-and-utilities/README.md): sector index.
2. [`compliance/energy-and-utilities/annex-energy-and-utilities-sector-requirements.md`](../compliance/energy-and-utilities/annex-energy-and-utilities-sector-requirements.md): sector overview.

### 3.5 If telecommunications

1. [`compliance/telecommunications/README.md`](../compliance/telecommunications/README.md): sector index.
2. [`compliance/telecommunications/annex-telecommunications-sector-requirements.md`](../compliance/telecommunications/annex-telecommunications-sector-requirements.md): sector overview.

### 3.6 If public sector or providing services to public sector

1. [`compliance/public-sector/README.md`](../compliance/public-sector/README.md): sector index.
2. [`compliance/public-sector/annex-public-sector-requirements.md`](../compliance/public-sector/annex-public-sector-requirements.md): sector overview.
3. If providing cloud services to US federal agencies: [`compliance/public-sector/annex-fedramp-requirements.md`](../compliance/public-sector/annex-fedramp-requirements.md): FedRAMP.
4. If relying on the EU Digital Identity Wallet or providing trust services in the EU: [`compliance/public-sector/annex-eidas-requirements.md`](../compliance/public-sector/annex-eidas-requirements.md): eIDAS.

### 3.7 If "Other / general technology": no sector overlay

Skip Section 3. The universal baseline (Section 2) plus jurisdiction-conditional (Section 4) and capability-conditional (Section 5) reading will suffice.

---

## 4. Jurisdiction-conditional content

Layer the privacy jurisdiction annexes for every jurisdiction in which you process personal data.

### 4.1 Privacy jurisdictions (per Section 1.3)

Each is found in [`privacy/jurisdictions/`](../privacy/jurisdictions/). The directory carries jurisdiction annexes for every region the library covers (currently 26 jurisdictions, including the Anglosphere examples listed below and additional non-Anglosphere jurisdictions across Asia-Pacific, Latin America, Middle East, Africa, and Europe). For the complete list, see the [jurisdiction index](../privacy/annex-privacy-jurisdiction-index.md).

Common Anglosphere selections (representative, not exhaustive):

- EU residents: [`privacy/jurisdictions/annex-privacy-european-union.md`](../privacy/jurisdictions/annex-privacy-european-union.md)
- UK residents: [`privacy/jurisdictions/annex-privacy-united-kingdom.md`](../privacy/jurisdictions/annex-privacy-united-kingdom.md)
- US residents (CCPA): [`privacy/jurisdictions/annex-privacy-united-states.md`](../privacy/jurisdictions/annex-privacy-united-states.md)
- Canadian residents: [`privacy/jurisdictions/annex-privacy-canada.md`](../privacy/jurisdictions/annex-privacy-canada.md)

For other jurisdictions (Australia, Singapore, India, Brazil, Japan, South Korea, China, and others), consult the [jurisdiction index](../privacy/annex-privacy-jurisdiction-index.md) above for the full list of available annexes.

### 4.2 Cross-sector horizontal regulations

If in scope:

- EU NIS 2 (essential or important entities): [`compliance/annex-nis-2-implementation.md`](../compliance/annex-nis-2-implementation.md)

### 4.3 Trusted-trader jurisdictions

See Section 3.1 above (these live under `compliance/logistics/`).

---

## 5. Capability-conditional content

### 5.1 If you develop, deploy, or procure AI

Read in this order:

1. [`ai/charter-ai-governance-council.md`](../ai/charter-ai-governance-council.md): AI governance authority.
2. [`ai/framework-ai-governance-and-risk.md`](../ai/framework-ai-governance-and-risk.md): AI governance framework.
3. [`ai/policy-ai-compliance.md`](../ai/policy-ai-compliance.md): AI compliance policy.
4. [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md): AI security and risk standard.
5. [`ai/procedure-ai-system-impact-assessment.md`](../ai/procedure-ai-system-impact-assessment.md): impact assessment procedure.
6. [`ai/register-ai-risk.md`](../ai/register-ai-risk.md): AI risk register template.
7. [`ai/template-ai-system-register.md`](../ai/template-ai-system-register.md): AI system inventory.

If you build agentic AI:

8. [`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md)
9. [`ai/standard-ai-access-and-agent-permissions.md`](../ai/standard-ai-access-and-agent-permissions.md)
10. [`ai/register-mcp-server.md`](../ai/register-mcp-server.md)

If you place AI systems on the EU market, put them into service in the EU, or your AI system's output is used in the EU:

11. [`ai/jurisdictions/annex-ai-european-union.md`](../ai/jurisdictions/annex-ai-european-union.md): EU AI Act (Regulation (EU) 2024/1689) per-regime consolidated view (operator roles, risk tiers, obligation chains, timeline, penalties).

If you develop or deploy AI that makes consequential decisions affecting Colorado residents:

12. [`ai/jurisdictions/annex-ai-us-colorado.md`](../ai/jurisdictions/annex-ai-us-colorado.md): Colorado AI statute (SB 24-205, re-enacted by SB 26-189) two-regime per-regime view (developer and deployer duties, consumer rights, meaningful human review, enforcement, transition timeline).

### 5.2 If you operate cloud workloads

1. [`operations/standard-cloud-security-configuration-baseline.md`](../operations/standard-cloud-security-configuration-baseline.md): cloud baseline.
2. [`operations/standard-network-security-and-segmentation.md`](../operations/standard-network-security-and-segmentation.md): network segmentation.
3. [`supply-chain/standard-cloud-exit-and-data-portability.md`](../supply-chain/standard-cloud-exit-and-data-portability.md): cloud exit.

### 5.3 If you develop software in-house

1. [`dev-security/policy-secure-development-and-engineering.md`](../dev-security/policy-secure-development-and-engineering.md): secure development policy.
2. [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md): developer requirements.
3. [`dev-security/standard-devops-security-requirements.md`](../dev-security/standard-devops-security-requirements.md): DevOps requirements.
4. [`dev-security/standard-software-composition-analysis.md`](../dev-security/standard-software-composition-analysis.md): SCA / SBOM.
5. If using AI coding assistants: [`dev-security/guideline-ai-coding-assistant-security.md`](../dev-security/guideline-ai-coding-assistant-security.md).

### 5.4 If you operate identity infrastructure

1. [`security/standard-authentication-and-password-management.md`](../security/standard-authentication-and-password-management.md)
2. [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md)
3. [`security/procedure-onboarding-and-offboarding.md`](../security/procedure-onboarding-and-offboarding.md)

### 5.5 If you operate operational technology / ICS

Start with the [`operations/ot/`](../operations/ot/) suite (OT security overview, OT/ICS security standard, OT change management, OT incident response, the OT asset-inventory register, and the BMS overlay), plus the universal baseline and the energy-and-utilities annex (Section 3.4). Deeper IEC 62443 alignment is a backlog candidate (not currently scheduled in TODO); see [`governance/register-coverage-gaps.md`](../governance/register-coverage-gaps.md) section 5.

---

## 6. Phased adoption suggestions

These are illustrative rather than prescriptive. Adapt to your context.

### 6.1 30-day starter set (any adopter)

1. Universal baseline orientation (2.1) and governance core (2.2): read.
2. Universal baseline risk and compliance foundation (2.3): read.
3. Identify your sector and read the sector index README (3.x).
4. Identify your jurisdiction and read the relevant privacy annex (4.1).
5. Map the library's roles ([`register-role-authority.md`](../governance/register-role-authority.md)) to people in your organization.
6. Decide which library documents you will adopt as-is, adapt, or omit.

Deliverable: a one-page adoption plan listing the library documents you will operate.

### 6.2 90-day implementation (mid-market)

1. Adopt the universal baseline policies and standards (2.3, 2.4, 2.5).
2. Implement sector-conditional content (Section 3).
3. Implement the privacy jurisdiction content for your operating regions (4.1).
4. Stand up the incident-response procedure (Section 2.4 item 16) and run a tabletop.
5. Stand up the supplier due-diligence procedure (Section 2.7 item 23).
6. Run an initial gap-assessment using the [maturity scorecard](maturity-scorecard.md).

Deliverable: an operating GRC programme covering the baseline.

### 6.3 180-day expansion (large enterprise / multi-national)

1. Add capability-conditional content (Section 5) for AI, cloud, software development, identity, OT as applicable.
2. Add jurisdiction-conditional content for every jurisdiction in which you operate.
3. Implement the resilience programme (Section 2.6) end-to-end including testing.
4. Establish the metrics, KPIs, and assurance cycles documented in [`governance/framework-metrics-monitoring-and-performance-reporting.md`](../governance/framework-metrics-monitoring-and-performance-reporting.md) and [`governance/framework-continuous-assurance-and-improvement.md`](../governance/framework-continuous-assurance-and-improvement.md).

Deliverable: a substantive enterprise GRC implementation covering size, sector, jurisdictional, and capability dimensions.

---

## 7. Frequently asked navigation questions

**"I'm a 50-person fintech in the EU. What do I read first?"**

Universal baseline (Section 2), then `compliance/financial-services/` (3.2), then [`compliance/financial-services/annex-dora-implementation.md`](../compliance/financial-services/annex-dora-implementation.md), then [`privacy/jurisdictions/annex-privacy-european-union.md`](../privacy/jurisdictions/annex-privacy-european-union.md), then [`compliance/annex-nis-2-implementation.md`](../compliance/annex-nis-2-implementation.md) if in scope. About 25 documents for this sector-conditional EU-fintech path; this is larger than the universal Day-1 floor (six artefacts in [`docs/template-quickstart.md`](template-quickstart.md)) and the 17-document Tier 1 starter set in [`docs/adopter-guide.md`](adopter-guide.md), which it builds on rather than replaces.

**"I'm a 200-person third-party logistics provider (3PL) operating in the US, Canada, and Mexico. What do I read first?"**

Universal baseline (Section 2), then `compliance/logistics/` (3.1), then the CTPAT and PIP overlays (3.1 sub-bullets), then [`privacy/jurisdictions/annex-privacy-united-states.md`](../privacy/jurisdictions/annex-privacy-united-states.md) and [`annex-privacy-canada.md`](../privacy/jurisdictions/annex-privacy-canada.md). Mexico's NEEC/OEA programme is not yet covered (TODO backlog: logistics country / programme expansion); use the BASC programme overview as a structural reference until added.

**"I'm a 5-person early-stage SaaS in the UK with no specific sector. What do I read first?"**

Universal baseline orientation (2.1), governance core (2.2, but treat as aspirational; many roles will collapse to the founder), risk policy (2.3 item 9), security policy (2.4 item 13), incident response (2.4 item 16), UK privacy annex (4.1). Aim for a minimum-viable governance posture rather than full adoption; see [`governance/guideline-minimum-viable-governance-structure.md`](../governance/guideline-minimum-viable-governance-structure.md) for how to consolidate roles.

**"I'm a multinational healthcare system. Where do I start?"**

Universal baseline (Section 2). Then `compliance/healthcare/` (3.3). Then privacy jurisdiction annexes for every country your patients reside in or where data is processed (4.1). Then capability-conditional sections for AI (5.1) if you operate clinical AI, cloud (5.2), identity (5.4). US HIPAA has a dedicated operational overlay in the healthcare sector (`compliance/healthcare/annex-healthcare-united-states.md`, see 3.3).

**"I'm building AI products. Where do I start?"**

Universal baseline (Section 2), then capability-conditional AI section (5.1). Sector and jurisdiction overlays as applicable. The EU AI Act and the Colorado AI statute each have a dedicated jurisdiction annex in `ai/jurisdictions/` (see 5.1).

---

## 8. When this guide does not have your answer

- Check [`governance/register-coverage-gaps.md`](../governance/register-coverage-gaps.md) for whether your situation is recorded as Planned, Deferred, or Out of scope.
- Check [`TODO.md`](../TODO.md) for what's queued for future work.
- Check [`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md) for the full document inventory.
- Open an issue or PR proposing the addition.

---

**End of guide.**
