# Fabricated alignment-citation existence

A cited framework-control identifier of the checked family exists in a held edition of
that framework's catalogue. A citation can name an identifier that is well-formed (it
fits the family's code shape) yet appears in no held edition of the framework; that is
a fabricated code, which the citation gates that only check code shape cannot see. The
check recognizes one identifier family by its code shape, reads each document's lines
outside fenced code blocks, finds each identifier of that family and each range of them
(validating both range endpoints against their own category prefixes, so a
cross-category range validates its actual endpoint, not a reconstructed one), and flags
any identifier absent from the union of every held edition of the framework, advising
correction to an existing identifier that fits the row. Validation is against the union
of held editions, so a legitimate later-edition identifier is not false-flagged; only a
code absent from all held editions is fabricated. The identifier family and its code
shape are fixed by the check; the valid-identifier catalogue and the framework name are
supplied by the adopter (the reference registry) and are not part of this clause.
Report-only by default, the check becomes a blocking gate in strict mode. A document
whose identifiers of the checked family all exist in a held edition contributes no
findings.
