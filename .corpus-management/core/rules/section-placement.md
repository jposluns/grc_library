# Section placement

A named section appears in its required position within a document: near the top, or
near the bottom, as the project's placement model specifies. A placement rule names a
set of accepted heading spellings, a position constraint (within the top N sections, or
within the bottom N), and an optional set of document types the rule applies to. A rule
scoped to document types is checked only for a document declaring one of those types; an
unscoped rule is checked for every scanned document. A document with no sections, a
section that matches no rule, and a scoped rule against a document of another type are
all left unflagged; headings inside fenced code blocks are not counted. A matching
section that falls outside its required position is flagged. The placement model (which
sections, which positions, which types) is project configuration, not part of this clause.
