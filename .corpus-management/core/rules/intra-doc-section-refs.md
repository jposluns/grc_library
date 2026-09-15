# Intra-document section references

An in-document section reference (`§N`, `§N.N`, `Section N`, `Section N.N`, and
deeper) matches a numbered heading in the same document. Numbered headings
(`## N. Title`, `### N.N Title`, `## Section N: Title`, and deeper) are extracted
outside fenced code blocks; a reference whose numeric identifier is not among them
is flagged, unless a cross-document heuristic claims the reference for another
document: a nearby markdown link or a `.md` filename within a short window either
side of the reference, a document-type word (standard, procedure, policy, and
kin), or an external-framework name (ISO, NIST, OWASP, and kin) anywhere on the
line. The cross-document heuristic vocabulary is fixed in the check
implementation; the exempt-file set (meta-documents that legitimately discuss
section references, not their own headings) is project configuration. A document
with no numbered headings contributes no findings.
