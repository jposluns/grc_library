# Cross-file section references

A document that cites a numbered section of ANOTHER corpus document cites a
section that exists in the resolved target. The check fires on two
high-confidence resolvable-target classes: an adjacent-link reference (a `§N` /
`Section N` reference with a markdown `.md` link within an adjacency window on the
same prose line or table cell), where the link names the target; and a
binding-declaration reference (a line carrying the binding sentinel together with
a `.md` link binds every subsequent bare reference in the file to that target,
the last link ending before the sentinel). The cited number must be a numbered
heading (`## N. Title`, `### N.N Title`, `## Section N: Title`, and deeper) or a
line-initial inline clause (`N.N ...`, at least two levels) in the target;
headings and clauses are read outside fenced code blocks. Numbered headings
and cited references are cut to four levels; inline clauses are recognized
only at two to four levels, so a deeper clause line is not a target section
and a five-level citation to it is checked against its four-level prefix
(a documented residual).
Deliberate exclusions
(recall costs, not gaps): external-standard
context lines (a reference citing an ISO / NIST / OWASP / GDPR clause, and kin);
a target with zero numbered headings and zero inline clauses (a numbered
reference to an unnumbered document is not a stale-heading case); a bare
reference with no adjacent link and no active binding (the intra-document gate
owns those); and name-based references and range second endpoints (no number to
resolve). The shared cross-file reference-extraction config (the reference
patterns, the markdown-link pattern, the binding sentinel, the external-context
vocabulary, and the adjacency window) and the exempt-file set are project
configuration and are not part of this clause; a reference that resolves cleanly,
and a document that cites none, contribute no findings.
Every line is split into cells on unescaped pipes outside matched inline code
spans, and every cell is checked. An unmatched backtick run is literal, and
backslashes inside code spans are literal; escaped pipes and pipes inside code
spans remain within their cells. In a table
row, a reference to a heading in the citing document remains local when no
link precedes it in the cell and a nearby following markdown link, starting
within the configured adjacency window, appears in parentheses after
non-whitespace descriptive text. The text between the reference and the link
must begin with whitespace, hold non-whitespace descriptive text, and end,
ignoring whitespace, with an opening parenthesis; besides that opening
parenthesis it may hold at most one parenthesis, which counts as descriptive
text. A parenthesis is bare when it is outside any inline code span and not
escaped with a backslash. The last opening parenthesis in that text must be
bare; when it is in a code span or escaped, it is text, and the cell is
checked as a citation of the target. Every bare opening parenthesis in that
text must be closed after the link and any citation text, so a bare opening
parenthesis standing as the descriptive character must be closed twice;
nested parentheses are counted, so a nested parenthetical does not close one,
and a parenthesis in a code span or escaped is not counted. A bare closing
parenthesis there can stand only as the descriptive character, before the
last opening parenthesis, and closes none of them. Parentheses before the
reference are neither counted nor required to be closed. A table cell that
meets the other conditions of this exception but does not close every bare
opening parenthesis is refused as malformed, whether or not the target holds
the cited number. `Of the target` identifies
the linked target and does not qualify as local description.
Only the explicit `of [the] target` wording is treated as a target citation in this table-cell local-section exception; `of the policy` remains a documented residual.
A line is a table row for this exception only when its first non-whitespace
character is a pipe, as the corpus writes table rows; a valid row written
without a leading pipe, any cell of which holds a local section, then
descriptive text, then a parenthesized link to the target, is treated as prose
for this exception, so its local section is checked against the adjacent link.
This is a documented residual.
