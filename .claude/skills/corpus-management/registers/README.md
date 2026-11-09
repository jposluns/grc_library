# Project Governance Registers

**Document Title:** Project Governance README\
**Document Type:** Register\
**Version:** 1.0.4\
**Date:** 2026-11-08\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`README.md`](../../../../README.md), [`.claude/skills/corpus-management/specs/specification-project-governance-separation.md`](../specs/specification-project-governance-separation.md), [`governance/register-document-index-and-classification.md`](../../../../governance/register-document-index-and-classification.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Upon migration of an artefact into or out of this directory, and annually\
**Repository Path:** [`.claude/skills/corpus-management/registers/README.md`](README.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This directory holds **project governance registers**: the operational records of running *this* library that remain useful to a public reader, as distinct from the **corpus governance** the library publishes as its deliverable. The distinction, the classifying criterion, and the migration procedure are defined in [`.claude/skills/corpus-management/specs/specification-project-governance-separation.md`](../specs/specification-project-governance-separation.md).

An adopter who clones the library for its governance, risk, and compliance content does not consume these artefacts as their own governance; they document how the maintainer operates and audits the corpus, and they double as worked examples of the reusable patterns in `governance/` (the citation-verification specification, the worklist template) executed against this specific corpus. Purely operational campaign instances (the per-batch citation-verification worklists and the campaign bundle record) are held in the maintainer's private operational store and are not part of the public tree; this README indexes only the public registers below.

This README is the project-side index, the counterpart to the corpus index [`governance/register-document-index-and-classification.md`](../../../../governance/register-document-index-and-classification.md). It exists so the corpus index can stay corpus-only under the one-way dependency rule (project governance may cite corpus governance; corpus governance must not cite project governance).

This directory is **audited, not exempt**: its artefacts receive the full corpus audit sweep (metadata-block completeness, version and date currency, language, citation accuracy, link coverage). It differs from `.working/` (working-state placeholders and frozen records) in exactly that: project-governance registers are maintained and must stay internally honest. The one behaviour that changes is adopter-facing inclusion: the taxonomy, portal, and maturity-scorecard generators, and the corpus document index, treat this directory as outside the published deliverable and do not list its artefacts.

---

## Project-governance artefacts

| Type | Title | Path |
| --- | --- | --- |
| Register | Citation Verifications Register | [`.claude/skills/corpus-management/registers/register-citation-verifications.md`](register-citation-verifications.md) |
| Register | Historical-Context Citation Exceptions Register (rows in [`.claude/skills/corpus-management/registers/register-historical-citation-exceptions.toml`](register-historical-citation-exceptions.toml); the page's table is generated from them) | [`.claude/skills/corpus-management/registers/register-historical-citation-exceptions.md`](register-historical-citation-exceptions.md) |
| Register | Document Review Schedule Register | [`.claude/skills/corpus-management/registers/register-document-review-schedule.md`](register-document-review-schedule.md) |
| Guide | Reference-Acquisition Manifest (the public bibliography of the sources this corpus engages) | [`.claude/skills/corpus-management/registers/reference-acquisition-manifest.md`](reference-acquisition-manifest.md) |

---

**End of Document**
