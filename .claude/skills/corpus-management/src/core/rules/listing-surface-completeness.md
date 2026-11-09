# Listing-surface completeness

Every mechanical listing surface enumerates every active document in its scope. Two
such surfaces are checked: the central document-index register (which must list every
domain-prefixed active document under its index section) and each domain README (which
must list every active document in that domain). The canonical set of active documents
is read from the generated taxonomy; a domain-prefixed document is register-required
while a root-level document is exempt (the register is domain-organized). For the
register, the check flags any required document missing from the index section and any
listed path that is not an active document at all (a stale or mistyped entry); for a
domain README, it flags any of that domain's active documents missing from the README
(but not "extra" cross-domain links, which are legitimate), and a domain with active
documents but no README at all. Document paths are read from markdown code spans that
carry a domain-dir prefix, so a bare-filename mention in prose is not mistaken for an
index entry. Semantic surfaces (matrices, glossary, related-documents lists) are not
gated. The corpus layout (the taxonomy path, the register path and its index section)
is supplied by the adopter and is not part of this clause. A corpus whose register and
domain READMEs enumerate every active document in scope, and whose register carries no
stale path (one listed but not an active document), contributes no findings.
