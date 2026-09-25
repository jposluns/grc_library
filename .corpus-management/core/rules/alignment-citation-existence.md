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
differently named framework that contains the acronym does not count) or by its full name (not
when it is part of the mobile standard's name), in a table cell under a header that names it (a header that also signals a version, a tool
or another standard marks such a column instead),
in the body of a table with a header cell that names it (except a column whose header signals a
version, a tool or another standard, unless the token's own cell names the framework), or on a row whose first cell names it. A header row's own tokens are checked only in a cell that names the
framework. Table rows are
split on unescaped pipes, leading and trailing pipes are optional, a separator cell is one or
more hyphens with optional colons, a table's header is the row directly above its first
separator row (a later separator-shaped row is an ordinary body row), and a table ends at the
first line with no unescaped pipe, at a heading, blockquote or list item, or where a fenced block
intervenes. Within that context, a token whose middle number is zero is a
version, never an identifier, because the framework numbers its sections from one; and a token
that directly follows the words version, edition, release or revision, a listed publisher's
document number (the ETSI forms), or a listed framework or standard (CMMI, TOGAF, ITIL, COBIT,
SAMM, CSF, NIST, PCI DSS, CIS, BSI, CWE, CAPEC, ATLAS, ATT&CK, MASVS, IEEE, ISO, read with
markdown links, code and emphasis removed), optionally with its
own capitalized short name, a generic word such as standard or framework, a document number joined
by a space or hyphen, an amendment or
corrigendum, a year (bracketed or not) and a closing parenthesis, is that subject's version.

Editions are handled by scope. A mention of the framework names an edition when an edition
number from 1 to 9 follows it, with any markdown emphasis or link target in between and not
followed by the words levels or chapters: after the words version, edition or release in any
form, and otherwise
written dotted or with a lowercase `v`, or as a capital-`V` token whose middle number is zero; a
bare integer (a count, a footnote marker, a section sign) is never an edition, and a capital `V`
with a dotless number or a non-zero middle number directly after the name is a chapter or an
identifier. An edition with a zero middle number written directly before the name ("3.0.1 ASVS",
"version 3.0 of the ASVS") also names it. Identifiers are validated against the union of the held editions, which the adopter
supplies. A prose line that names an edition that is not held is not checked. In a table, a token
is not checked when its own cell or its column header names such an edition, or when its row's
first cell does and its column header does not name a held edition. Two-number tokens
are checked against the held sections and three-number tokens against the held requirements;
bare chapter numbers are not checked. A weakness family (`CWE-` followed by a number, in any
letter case, leading zeros ignored) is checked wherever it appears.

The identifier families and their code shapes are fixed by the check. The valid-identifier
catalogues and the framework names are supplied by the adopter (the reference registry)
and are not part of this clause; a family whose catalogue the adopter does not supply is
not checked. Recognition limits are part of the clause: an identifier valid only in another held edition
passes; a fabricated identifier on a prose line, cell or row scoped out by an edition that is not
held is not checked; a requirement identifier written
without its `V` prefix is not recognized, a range is checked at its endpoints only, a token with a letter suffix (`V1.2.3a`, `CWE-79a`) or a
bare weakness number is not recognized, a token after a comma that follows a listed standard is
read as that standard's, a table body
row written without pipes or a header spread over several rows is not read as table structure,
a version token in an ASVS-table column whose header does not signal a version, or after a
standard that is not listed, can be read as an identifier, a version string on a line that names the framework
whose prefix is not one of the recognized document numbers, standards or frameworks can be
read as an identifier, and a weakness catalogue that holds only
weaknesses flags a cited category or view identifier. Report-only by default, the check
becomes a blocking gate in strict mode. A document whose identifiers of the checked
families all exist in a held edition contributes no findings.
