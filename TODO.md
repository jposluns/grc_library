# TODO

Living backlog of planned enhancements for the GRC Documentation Library. Items are added when identified and removed when completed. Completed work is recorded in [`CHANGELOG.md`](CHANGELOG.md); this file holds only pending and queued items.

This file is informational and is not subject to the library's metadata-block, audit-conformance, or version-tracking conventions. The repository root README, NOTICE, CONTRIBUTING, SECURITY, CHANGELOG, and this TODO file are all maintained at the same conventional level (no per-file versioning).

---

## Priority 1 — foundations (next up)

These prevent drift across the library as content scales. Doing them before country/sector content expansion means later additions are auto-audited and consistent.

### 1.1 Glossary / acronym index

`governance/register-glossary.md` — single resolved reference for the 60+ acronyms the library uses (CTPAT, AEO, BASC, NIS 2, DORA, OEA, PIP, MSC, AIMS, AIDA, SBOM, KRI, RTO, RPO, IAM, PAM, ZTNA, etc.) and the canonical terms behind them.

Rationale: every reader hits acronyms; every new country/sector annex introduces new ones. A single resolved source prevents inconsistent expansions across documents.

### 1.2 Standards-currency checker + canonical citations catalogue

Two artefacts working together:
- `governance/register-canonical-citations.md` — positive list of standards with current versions, publication dates, scope summaries, and replacement notes for superseded versions (e.g., "ISO/IEC 42006:2025 — Requirements for bodies providing audit and certification of AI management systems"; "ISO/IEC 27006:2015 — successor: ISO/IEC 27006:2024").
- `tools/lint-standards-currency.py` — new audit. Flags citations of "(draft)" markers, year-only version labels where the standard has been published, and any standards citation not appearing in the canonical list.

Rationale: prevents the kind of drift hit in Phase 19.4/19.6 (ISO 42006 cited as draft after publication; then misattributed to AI Impact Assessment when ISO 42005:2025 is the impact-assessment standard). Every new country/sector annex will cite standards; without this, each PR requires manual citation audit; with this, the audit is automatic.

---

## Priority 2 — consistency and structural improvements

### 2.1 Related-Documents reciprocity check

Extend `tools/lint-structure.py` (or add a new linter) to verify that if document A's Related Documents lists B, then B's Related Documents lists A (or B explicitly marks A as a one-way reference). Catches the half-updated cross-reference state that accumulates across phases.

### 2.2 Library-level versioning policy

Currently each document carries its own version; the library as a whole has no declared version scheme. Pick and document one in `specification-master-project.md`:
- CalVer (e.g., `2026.05`) — by year and month, simple
- Milestone-based (e.g., `v2.0` after Phase 22) — semantic, more work
- Rolling-main (no library version, only document versions) — current de facto

Strategic value: lets adopters say "we adopted GRC Library 2026.05" rather than "as of commit 9cea9d1".

### 2.3 Filename ↔ Document Title alignment audit

New linter that warns when a file's filename (after the doctype prefix) and its Document Title diverge significantly. Catches cases like `annex-aeo-s-it-cybersecurity-requirements.md` with title `UK AEO-S IT and Cybersecurity Security Requirements` (the "Security Security" mistake we caught manually in Phase 20.1). Not strictly enforceable but useful as a warning.

---

## Priority 3 — strategic capability

### 3.1 Coverage gap analysis register

`governance/register-coverage-gaps.md` — structured catalogue of known coverage gaps: sectors not covered (manufacturing, retail, hospitality, education, defence, mining, agriculture), jurisdictions not covered, regulations referenced but not detailed, and AI capabilities not addressed. Honest disclosure helps adopters set expectations and helps contributors target gaps.

### 3.2 Adopter decision tree

`docs/decision-tree.md` — "I'm a 50-person fintech in the EU — what do I read first?" structured navigation. Uses glossary (Priority 1.1) and coverage gaps (Priority 3.1) as inputs.

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

## Notes on maintenance

- Add new items at the appropriate priority. Move items between priorities as context changes.
- When an item is completed, remove it from this file and record the completion in `CHANGELOG.md`.
- Sub-items can be promoted to their own phase if scope grows.
- This file is the source of truth for what's queued; conversation history is not.
