# Project Governance

**Document Title:** Project Governance README\
**Document Type:** Register\
**Version:** 1.0.1\
**Date:** 2026-06-26\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`README.md`](../README.md), [`governance/specification-project-governance-separation.md`](../governance/specification-project-governance-separation.md), [`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Upon migration of an artefact into or out of `.project-governance/`, and annually\
**Repository Path:** [`.project-governance/README.md`](README.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This directory holds **project governance**: the operational records of running *this* library, as distinct from the **corpus governance** the library publishes as its deliverable. The distinction, the classifying criterion, and the migration procedure are defined in the corpus specification [`governance/specification-project-governance-separation.md`](../governance/specification-project-governance-separation.md).

An adopter who clones the library for its governance, risk, and compliance content does not consume these artefacts; they document how the maintainer operates and audits the corpus. They are the filled-in operational instances produced when the reusable patterns in `governance/` (the citation-verification specification, the worklist template) are executed against this specific corpus.

This README is the project-side index, the counterpart to the corpus index [`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md). It exists so the corpus index can stay corpus-only under the one-way dependency rule (project governance may cite corpus governance; corpus governance must not cite project governance).

This directory is **audited, not exempt**: its artefacts receive the full corpus audit sweep (metadata-block completeness, version and date currency, language, citation accuracy, link coverage). It differs from `.working/` (frozen-state archives, unmaintained after write, gate-exempt) in exactly that: project-governance records are maintained and must stay internally honest. The one behaviour that changes is adopter-facing inclusion: the taxonomy, portal, and maturity-scorecard generators, and the corpus document index, treat `.project-governance/` as outside the published deliverable and do not list its artefacts.

---

## Project-governance artefacts

The project-governance artefacts migrated here under the project-governance separation (see the separation specification §5.2, the Phase 2 subsection, and §8.1). Phase 1 migrated the citation-verification campaign cluster; the Phase 2 migration moved the document review schedule register (this project's filled-in review schedule, a §3.2 operational instance):

| Type | Title | Path |
| --- | --- | --- |
| Register | Citation Verifications Register | [`.project-governance/register-citation-verifications.md`](register-citation-verifications.md) |
| Register | Citation Verification Bundle Index | [`.project-governance/register-citation-verification-bundle.md`](register-citation-verification-bundle.md) |
| Worklist | Citation Verification Worklist: Batch Q2 (ISO and ISO/IEC) | [`.project-governance/worklist-citation-verification-batch-q2-iso-iec.md`](worklist-citation-verification-batch-q2-iso-iec.md) |
| Worklist | Citation Verification Worklist: Batch Q3 (AI Tooling Provenance) | [`.project-governance/worklist-citation-verification-batch-q3-ai-tooling.md`](worklist-citation-verification-batch-q3-ai-tooling.md) |
| Worklist | Citation Verification Worklist: Batch Q3.1 (New Canonical Citations) | [`.project-governance/worklist-citation-verification-batch-q3-1-new-citations.md`](worklist-citation-verification-batch-q3-1-new-citations.md) |
| Worklist | Citation Verification Worklist: Batch Q4 (Remaining Canonical Citations) | [`.project-governance/worklist-citation-verification-batch-q4-canonical-citations.md`](worklist-citation-verification-batch-q4-canonical-citations.md) |
| Register | Document Review Schedule Register | [`.project-governance/register-document-review-schedule.md`](register-document-review-schedule.md) |

---

**End of Document**
