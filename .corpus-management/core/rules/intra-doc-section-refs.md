# Intra-document section references

An in-document section reference (`§N`, `§N.N`, `Section N`, `Section N.N`, and
deeper) matches a numbered heading in the same document. Numbered headings
(`## N. Title`, `### N.N Title`, `## Section N: Title`, and deeper) are
extracted outside fenced code blocks. References and headings are compared
at full numeric depth: `§1.2.300.4.5` does not match heading `1.2.300.4`.
The cross-file section-reference gate cuts headings and cited references to
four levels; it recognizes inline clauses only at two to four levels, so a
deeper clause line is not a target section (a documented residual).

A reference whose numeric identifier is not among the headings is flagged
unless a cross-document heuristic claims it for another document: a nearby
markdown link or `.md` filename within a short window on either side, a
document-type word (standard, procedure, policy, and kin), or an external
framework name (ISO, NIST, OWASP, and kin). The link or `.md` window is
checked first.

Regime names match case-sensitively as written: GDPR, CPPA, PIPEDA, HIPAA,
PCI DSS, and SOC 2. They match as whole words, so `UKGDPR` and `SOC 25`
do not name a regime. When a line names one of these regimes, every section
mark on that line is external context unless the mark has an explicit local
cue. A local cue is `see` (optionally `see also`) immediately before the mark,
or `above`, `below`, `here`, `herein`, `in this` plus one word, or `of this`
plus one word immediately after it. Cues match in any case. A dotted
single-letter suffix such as `.a` directly after the number, or parenthesized
groups directly after it, may precede a trailing cue. `§99.99a`, `§99.99.ab`,
`§99.99 (a)`, and `§99.99, below,` are uncued. A `GDPR: see §99.99` mark
beside a link to `guide.md` is treated
as a reference to that linked document. Otherwise, a cued mark is checked
against this document's headings even if another document type or framework
is named on the line: `GDPR: see §5.1 of ISO 27001` is reported when stale.

This also reports externally meant cues such as `GDPR §33 in this context
requires notice` and `For breach notice, see §33 of the GDPR.`; these are
known false positives. Lines without a regime retain the document-type and
framework behaviour, including `See §99.99 of this standard.` An uncued stale
internal mark on a regime line (for example, `GDPR §33 and §99.99 apply.`)
is not checked.

The cross-document heuristic vocabulary is fixed in the check
implementation; the exempt-file set (meta-documents that legitimately
discuss section references, not their own headings) is project
configuration. A document with no numbered headings contributes no findings.
