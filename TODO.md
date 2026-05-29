# TODO

Living backlog of planned enhancements for the GRC Documentation Library. Items are added when identified and removed when completed. Completed work is recorded in [`CHANGELOG.md`](CHANGELOG.md); this file holds only pending and queued items.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions. The repository root README, NOTICE, CONTRIBUTING, SECURITY, CHANGELOG, and this TODO file are all maintained at the same conventional level (no per-file versioning).

---

## Priority 1 — foundations

*(Tier 1 foundations completed in Phases 21.1 backlog, 21.2 glossary, and 21.3 standards-currency checker + canonical citations register.)*

---

## Priority 2 — consistency and structural improvements

*(Tier 2 consistency items completed in Phases 21.4 reciprocity-decision, 21.5 library versioning, and 21.6 filename/title alignment audit.)*

---

## Priority 3 — strategic capability

*(Tier 3 strategic capability items completed in Phases 21.7 coverage gap register and 21.8 adopter decision tree.)*

---

## Priority 4 — adopter experience

### 4.1 Quickstart templates per adopter profile

Pre-configured starter sets for common adopter profiles:
- Small business (under 50 employees, single jurisdiction)
- Mid-market regulated industry (50-500 employees, sector compliance)
- Multi-national enterprise (500+ employees, multiple jurisdictions)
- Public-sector adopter
- Healthcare adopter
- Financial-services adopter

### 4.2 Maturity assessment interactive template

The current `docs/maturity-scorecard.md` is auto-generated and static. An interactive form (spreadsheet or guided markdown checklist) lets an adopter self-assess.

### 4.3 Implementation roadmap templates

90-day, 180-day, and one-year implementation roadmaps per adopter profile. Maps to a phased rollout of library artefacts.

---

## Priority 5 — content expansion (deferred until Priority 1–3 foundations land)

### 5.1 Logistics country/programme expansion

The WCO AEO Compendium identifies 77+17 ≈ 94 trusted-trader programmes globally; the library currently covers 4 (BASC, CTPAT-US, AEO-UK, PIP-Canada). Highest-priority additions:
- EU AEO (covers 27 member states under EU Union Customs Code Art 38)
- Mexico NEEC / OEA
- Australia Trusted Trader (ATT)
- Singapore STP / STP-Plus
- Japan AEO
- Korea AEO
- New Zealand Secure Exports Scheme (SES)
- China AEO

### 5.2 Financial-services country regulator overlays

Country-level financial-regulator annexes within `compliance/financial-services/`:
- UK PRA/FCA (`annex-uk-pra-fca.md`)
- US OCC/FRB/FDIC/SEC/FINRA
- Canada OSFI
- Australia APRA
- Singapore MAS
- Japan FSA

### 5.3 Healthcare country regulator overlays

Within `compliance/healthcare/`:
- US HIPAA detail (Privacy Rule, Security Rule, Breach Notification Rule, HITECH)
- UK NHS DSPT (Data Security and Protection Toolkit)
- EU MDR/IVDR (Medical Device Regulation; In-Vitro Diagnostic Regulation)
- Canada PHIPA and provincial frameworks
- Australia My Health Records Act

### 5.4 Energy and utilities country regulator overlays

Within `compliance/energy-and-utilities/`:
- US NERC CIP standards (electricity reliability)
- US TSA pipeline cybersecurity directives
- UK Ofgem cyber requirements
- EU ENISA sectoral guidance

### 5.5 Telecommunications country regulator overlays

Within `compliance/telecommunications/`:
- EU EECC (European Electronic Communications Code)
- UK Ofcom telecom security framework
- US FCC regulations
- Australia ACMA requirements

### 5.6 Public-sector country/regulator overlays

Within `compliance/public-sector/`:
- UK Government Cyber Security Strategy and GovAssure
- Australia ISM (Information Security Manual) and PSPF (Protective Security Policy Framework)
- Canada IT Standards for federal departments
- EU eIDAS public-sector authentication

### 5.7 Privacy jurisdiction gaps

Existing privacy domain covers 25 country annexes. Known gaps or stale entries:
- Argentina (PDPA 2025 update pending)
- Saudi Arabia PDPL (recent updates)
- Mexico LFPDPPP
- Re-review of EU member state derogations where applicable

### 5.8 AI jurisdiction overlays

The library cites EU AI Act extensively but lacks dedicated per-jurisdiction AI annexes (parallel to privacy/jurisdictions/). Candidates:
- EU AI Act detailed annex (`ai/jurisdictions/annex-ai-european-union.md`)
- Canada AIDA
- UK AI policy framework
- US state-by-state AI laws (Colorado AI Act, NYC bias audit law, etc.)
- China generative AI rules
- Korea AI framework

---

## Priority 6 — domain-level expansion (longer-term)

### 6.1 Cloud-specific compliance overlays

AWS, Azure, GCP, and multi-cloud-specific governance content. Could live in `operations/` or warrant a new `cloud/` domain.

### 6.2 Operational technology (OT) / ICS security depth

IEC 62443 mapping, ICS incident response, building management systems, OT-specific change management. Cross-cuts with energy, logistics, and any organisation with operational technology.

### 6.3 Identity-specific content depth

Customer Identity (CIAM) governance, workforce identity governance, identity federation patterns, passwordless adoption playbooks.

### 6.4 Quantum cryptography readiness deepening

Library has a PQC roadmap; could add a PQC migration playbook, crypto-agility patterns, and post-quantum-ready CA management.

### 6.5 Cross-framework matrix expansion

Current matrix covers major frameworks; could expand coverage to additional sectoral and regional frameworks as the country/sector content grows.

---

## Investigation / blocked

Items requiring user decision or external dependency before becoming actionable.

- *(none currently)*

---

## Decisions log

Items considered and explicitly dropped, with rationale. Recorded here so the reasoning is preserved if the question recurs.

### Phase 21.4 (2026-05-28): Strict Related-Documents reciprocity dropped

Original plan: add a linter enforcing that if document A's Related Documents lists B, then B's Related Documents lists A. Empirical run found 1,269 non-reciprocal references across 266 of 280 active documents.

The library's actual convention is **asymmetric** Related Documents: each document lists "what this document consumes / relates to from its own perspective", not "the complete bidirectional graph". This is a reasonable, content-author-friendly convention.

The underlying concern (catching half-updated cross-references during refactors) is already covered by `lint-links.py` (broken-link detection).

Decision: dropped. Not pursued in narrower form (doctype-pair rules) because the marginal value over `lint-links.py` does not justify the maintenance cost of a curated rule set with many exemptions.

---

## Notes on maintenance

- Add new items at the appropriate priority. Move items between priorities as context changes.
- When an item is completed, remove it from this file and record the completion in `CHANGELOG.md`.
- Sub-items can be promoted to their own phase if scope grows.
- This file is the source of truth for what's queued; conversation history is not.
