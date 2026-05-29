# Data Architecture Standard

**Document Title:** Data Architecture Standard\
**Document Type:** Standard\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** Chief Technology Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`architecture/framework-enterprise-architecture.md`](framework-enterprise-architecture.md), [`architecture/standard-architecture-decision-records.md`](standard-architecture-decision-records.md), [`architecture/standard-integration-architecture.md`](standard-integration-architecture.md), [`architecture/standard-api-design.md`](standard-api-design.md), [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`ai/procedure-training-data-governance.md`](../ai/procedure-training-data-governance.md), [`governance/register-data-retention-schedule.md`](../governance/register-data-retention-schedule.md)\
**Classification:** Public\
**Category:** Architecture\
**Review Frequency:** Annual and upon material change to data platforms, sources, or governance practice\
**Repository Path:** [`architecture/standard-data-architecture.md`](standard-data-architecture.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## Purpose

This standard governs the data architecture practice: how data is modelled, owned, integrated, served, and retired across the organisation. It complements the data classification and handling standard (which governs the controls applied to data) and the privacy and data governance policy (which governs the organisation's privacy posture) by addressing the architectural choices that determine how data flows and is consumed.

---

## Scope

This standard applies to:

1. Operational data inside production systems.
2. Analytical data in lakes, warehouses, lakehouses, and feature stores.
3. Master and reference data shared across systems.
4. Customer-facing data products.
5. Event streams treated as primary or persistent data.
6. Data exposed to AI training and AI retrieval pipelines.

It does not govern ephemeral telemetry beyond its data shape (the observability and telemetry standard governs that).

---

## Section 1: principles

| Principle | Description |
| --- | --- |
| Data as a product | Data has owners, contracts, quality measures, and consumers |
| Domain alignment | Data ownership aligns to business domains; not centralized by default |
| Source of truth | Each significant data element has a single source of truth |
| Schema discipline | Schemas are explicit, versioned, and reviewed |
| Quality is built in | Data quality is designed for, not patched at consumption |
| Privacy by design | Personal data is minimized, classified, and controlled from the start |
| Lineage | Where data came from and how it was derived is recorded |
| Interoperability | Standard formats and identifiers are preferred over bespoke |
| Cost and value awareness | Storage, query, and movement costs are considered alongside utility |
| AI-aware | Data used for training, fine-tuning, and retrieval is governed per the training data governance procedure |

---

## Section 2: data domains and ownership

| Element | Description |
| --- | --- |
| Domain map | Data is organized into domains aligned with business capabilities |
| Domain owner | Each domain has a named owner accountable for the domain's data |
| Data product owner | Each data product within a domain has an owner |
| Steward role | Per-domain data stewards operate the quality and access processes |
| Cross-domain coordination | A federated data council coordinates cross-domain concerns |
| Master data | Master entities (customer, product, supplier, location) have a designated master and a clear consumption pattern |

---

## Section 3: data classification and sensitivity

| Element | Description |
| --- | --- |
| Classification | Per the data classification and handling standard |
| Personal data | Per the privacy framework; ROPA-linked |
| Special-category data | Per the privacy framework |
| Children's data | Per the children's data framework |
| Regulated data | Per the applicable sector regulation (e.g. payment card, health) |
| AI-sensitive data | Where the data is unsuitable for inclusion in AI prompts or training, marked as such |
| Tagging | Classification tags propagate with the data through transformation |

---

## Section 4: schemas and contracts

| Element | Description |
| --- | --- |
| Schema source of truth | Schemas live in a registry or repository with version control |
| Contract publication | Data contracts are published to consumers |
| Schema review | Schema changes are reviewed; breaking changes go through architecture review |
| Compatibility | Forward, backward, full compatibility expectations are documented per stream |
| Reference data alignment | Reference data (currencies, country codes, units) uses standard identifiers |
| Identifiers | Stable, opaque, and minimal-leak identifiers per the API design standard |
| Naming | Documented naming conventions; consistent across domains where the value is shared |

---

## Section 5: data integration

| Element | Description |
| --- | --- |
| Integration pattern | Per the integration architecture standard; choice justified |
| Replication | Where data is replicated, the source of truth is unambiguous |
| Change-data capture | Where used, schema-evolution and downstream-consumer handling is documented |
| Event-as-record | Event streams used as primary records have retention and replay semantics defined |
| Cross-region | Cross-region replication aligned with data residency and the cross-border register |
| Cross-system | Cross-system integration is contract-based, not direct database access |
| Bulk loads | Documented; subject to the same classification and lineage controls |

---

## Section 6: data quality

| Element | Description |
| --- | --- |
| Quality dimensions | Accuracy, completeness, consistency, timeliness, uniqueness, validity |
| Quality measures | Per-data-product measures defined |
| Quality SLOs | Per data product, where appropriate |
| Detection | Automated detection where feasible; outliers and anomalies surfaced |
| Treatment | Quality issues are tracked to closure; chronic issues drive root-cause action |
| Reporting | Quality is reported to data product owners and to consumers |

---

## Section 7: lineage and provenance

| Element | Description |
| --- | --- |
| Source recording | Each data element's origin is recorded |
| Transformation recording | Transformations are recorded; queries and pipelines are versioned |
| Cross-system lineage | Lineage tracks cross-system flow |
| AI training lineage | Per the training data governance procedure |
| Reverse-ETL | Where data flows out of analytical to operational, lineage is preserved |
| Deletion propagation | Deletion follows lineage; per privacy and retention obligations |

---

## Section 8: data lifecycle

| Stage | Description |
| --- | --- |
| Capture | Data is captured at known sources with documented schema |
| Storage | Data is stored according to its classification and access pattern |
| Use | Data is used by named consumers with documented purposes |
| Sharing | Data sharing inside and outside the organisation is governed per the data sharing register |
| Retention | Per the records retention schedule |
| Deletion | Deletion is propagated reliably, including from backups per the retention policy |
| Archival | Long-term archival is distinct from retention for active use |

---

## Section 9: analytical and AI data platforms

| Element | Description |
| --- | --- |
| Lake, warehouse, lakehouse | Choice is deliberate; each platform's role is documented |
| Feature store | Where used, governed for feature lineage and feature quality |
| Vector store | Per the AI security and risk standard for vector store controls |
| Reverse-ETL | Where used, sanctioned and lineage-preserving |
| Notebooks | Production-relevant notebooks are versioned and reviewed |
| Workspace governance | Analyst and data-scientist workspaces have classification-aware controls |
| Synthetic data | Per the training data governance procedure |

---

## Section 10: data sharing and customer-facing data

| Element | Description |
| --- | --- |
| Internal sharing | Sharing across teams is contract-based; documented data products |
| External sharing | External sharing follows privacy, regulatory, and contractual constraints |
| Open data | Where the organisation publishes open data, the publication pipeline is governed |
| Data exports for customers | Customer-facing data exports have documented schema, integrity, and access controls |
| Data clean rooms | Where used, governance follows the relevant privacy framework |
| Marketplaces | Inbound and outbound data marketplaces are governed |

---

## Section 11: master data and reference data

| Element | Description |
| --- | --- |
| Master entities | Identified master entities; designated master system per entity |
| Reference data | Centrally curated; consumers do not maintain their own copies |
| Identifier mapping | Where multiple identifiers exist, mapping is governed |
| Match and merge | Match-and-merge rules are explicit |
| Hierarchy | Hierarchies are versioned; changes are recorded |
| Conformity | Reference data uses recognized standards where they exist |

---

## Section 12: governance forum and roles

| Role | Description |
| --- | --- |
| Chief Data Officer (or equivalent) | Owns the data architecture practice |
| Data council | Owns this standard; reviews cross-domain concerns |
| Domain owners | Own their domain's data |
| Data product owners | Own individual data products |
| Data stewards | Operate quality, access, and lineage processes within a domain |
| Privacy and AI representatives | Engaged in data architecture reviews |
| Security representative | Engaged where the architecture touches sensitive data classification |

---

## Section 13: relationship to adjacent governance artefacts

| Artefact | Relationship |
| --- | --- |
| Data classification and handling standard | Provides the classification scheme and the controls that flow from it |
| Privacy and data governance policy | Sets the privacy frame; this standard expresses architectural mechanics |
| Records retention schedule | Retention requirements drive lifecycle |
| Training data governance procedure | AI training and retrieval data are governed there |
| Cross-border data flow register | International flow recorded there |
| AI security and risk standard | Vector store, RAG, and AI-data controls are stated there |
| API design standard | Data exposed via APIs follows the API design standard |
| Integration architecture standard | Data movement patterns governed by integration architecture |

---

## Section 14: anti-patterns

| Anti-pattern | Why it harms |
| --- | --- |
| Direct production database access by other services | Couples consumers to the producer's schema; impedes change |
| Personal data accumulating without classification | Privacy and security risk silently grow |
| Multiple sources of truth | Consumers disagree; reconciliation effort grows |
| Schema-by-discovery | Consumers reverse-engineer schemas; producers do not know who depends on what |
| Aspirational lineage | Lineage that is documented but not reliable misleads decisions |
| Hidden data products | Data products that exist but are not catalogued cannot be governed |

---

## Operating expectations

1. Every significant data product has a named owner, a documented contract, and a current classification.
2. Schemas are versioned and reviewed; breaking changes are deliberate.
3. Lineage is maintained for material data flows.
4. Deletion is propagated; retention is honoured.
5. AI use of data is governed per the training data governance procedure.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| DAMA-DMBOK 2 | Data management body of knowledge | Data management baseline |
| ISO/IEC 38505-1 | Governance of data | Data governance |
| ISO 8000 | Data quality | Data quality |
| Data Mesh (Zhamak Dehghani) | Domain-aligned data architecture | Modern data architecture |
| Open Group TOGAF Standard | Data Architecture | Enterprise architecture cross-walk |
| ISO/IEC 27001:2022 | A.5.12, A.5.13, A.5.34 | Information classification, labelling, privacy |
| GDPR / UK GDPR | Articles 5, 25, 32 | Privacy by design |
| ISO/IEC 42001:2023 | AI management system | AI data governance |

---

## Limitations

This standard is a public-domain baseline. Data platform choices, ownership topology, and tooling are organisation-specific. The standard expresses outcomes and architectural principles, not specific platforms or commercial products.

---

**End of Document**
