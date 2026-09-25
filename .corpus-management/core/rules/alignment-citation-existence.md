# Fabricated alignment-citation existence

A cited framework-control identifier of a checked family exists in a held edition of
that framework's catalogue. A citation can name an identifier that is well-formed (it
fits the family's code shape) yet appears in no held edition of the framework; that is
a fabricated code, which the citation gates that only check code shape cannot see. The
check reads each document's lines outside fenced code blocks, finds each identifier of a
checked family, and flags any identifier absent from the union of every held edition of
its framework, advising correction to an existing identifier that fits the row.
Validation is against the union of held editions, so a legitimate later-edition
identifier is not false-flagged; only a code absent from all held editions is fabricated.

Three families are recognized by code shape. A category-coded family (code shape
`XX.YY-P` with an optional number) is checked wherever it appears, together with ranges of
it, each range endpoint validated against its own category prefix, so a cross-category
range validates its actual endpoint, not a reconstructed one. A requirement-and-section
family whose identifiers are `V` followed by two or three dot-separated numbers is checked
only in that framework's context, because the same shape is used for other publishers'
document versions: on a line that names the framework by its acronym (a word match, so a
differently named framework that contains the acronym does not count) or by its full name, in
a table cell under a header that names it, or on a row whose first cell names it. Table rows
are split on unescaped pipes, a leading pipe is optional, and a table's header is the row
directly above its separator row. Within that context, a token whose middle number is zero is
a version, never an identifier, because the framework numbers its sections from one; a token
that directly follows the words version, edition, release or revision, another publisher's
document number, or another named framework or standard is that subject's version; and a
token attributed to an edition whose numbering differs from the held one (the nearest
preceding mention of the framework on the line, or the token's column header, names that
edition) is not checked against the held numbering. Two-number tokens are checked against the
held sections and three-number tokens against the held requirements; bare chapter numbers are
not checked. A weakness family (`CWE-` followed by a number, in any letter case) is checked
wherever it appears.

The identifier families and their code shapes are fixed by the check. The valid-identifier
catalogues and the framework names are supplied by the adopter (the reference registry)
and are not part of this clause; a family whose catalogue the adopter does not supply is
not checked. Recognition limits are part of the clause: a requirement identifier written
without its `V` prefix is not recognized, a version string on a line that names the framework
whose prefix is not one of the recognized document numbers, standards or frameworks can be
read as an identifier, and a weakness catalogue that holds only
weaknesses flags a cited category or view identifier. Report-only by default, the check
becomes a blocking gate in strict mode. A document whose identifiers of the checked
families all exist in a held edition contributes no findings.
