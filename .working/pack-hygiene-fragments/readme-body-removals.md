# Removed from pack README body (pack-hygiene scrub)

Each entry archives, verbatim, a prose passage removed or genericized from
`dev-security/claude-rules/README.md` (the body outside the `## Version history`
table; the table's pre-thinning archive lives beside this file in
`readme-version-history-original.md`).

## Pack-scope closing paragraph (positioning hunk 1)

Original:

```text
The pack and the parent GRC library are two coordinated halves of one project. The parent library is the GRC corpus; the pack is the operational layer that allowed the maintainer to keep the corpus consistent with Claude Code participating in PRs. Every governance rule in the pack was extracted from a real maintenance event recorded in the parent library's [`CHANGELOG.md`](../../CHANGELOG.md); the pack is the library's lessons learned, made portable.
```

Replacement note: register-aware rewrite per the exemplar payload; the per-rule CHANGELOG-citation claim moves to the new `rule-provenance.md` register (linked), with detailed lineage staying in the parent library's records.

## Adoption-path-3 credibility sentence (positioning hunk 2)

Original:

```text
The third mode is an emergent use that has been adopted by developers in practice; it is supported alongside the primary fork-the-whole-repo path. Provenance is what makes the pack credible as a standalone artefact: every governance rule cites the maintenance event in the parent library's CHANGELOG that justified adding it.
```

Replacement note: register-aware rewrite per the exemplar payload; the credibility claim now points at the pack's own `rule-provenance.md` register (linked) instead of the parent CHANGELOG.

## Directory-tree blurb for `skills/matrix-fit/SKILL.md`

Original:

```text
│   ├── matrix-fit/SKILL.md                            Cadenced semantic-fit audit of the compliance matrix and per-document framework tables; catches the gate-blind "valid code, wrong control" class the existence gates 48/49/54/58/61 cannot; after each FR-167 batch + at completion + ad-hoc
```

Replacement note: parent gate-number enumeration genericized to "the existence gates" and the backlog id "FR-167 batch" genericized to "matrix-expansion batch".

## Directory-tree blurb for `skills/claim-fit/SKILL.md`

Original:

```text
│   ├── claim-fit/SKILL.md                             Cadenced citation-precision audit of normative-attribution claims; catches the gate-blind FR-120 "attributed value, silent source" class the existence and citation gates cannot; one-time Tier-A pass at adoption + after normative-value batches + ad-hoc
```

Replacement note: the backlog id "FR-120" dropped; the class is named by its description alone.
