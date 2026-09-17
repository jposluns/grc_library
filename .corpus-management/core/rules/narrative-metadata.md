# Executive-narrative metadata contract

Every page inside the executive-narrative tree, except the path-scoped entry-point, conforms to
the narrative metadata contract. The page carries the narrative document type and the full
canonical and narrative-extension metadata blocks in the fixed field order, with every
metadata-run line but the last ending in a hard-break marker and the last line bare; its
Narrative Type is a known subtype and its Narrative Status and Claim Classes Present values are
drawn from the closed vocabularies; a subtype fixes the required status and the subdirectory the
page must live in; the Corpus Sources field carries at least one pin, and every pin plus every
body link that resolves to a corpus target must be a pin to a held corpus path (an unpinned
corpus-target body link, or a pin whose target is not a corpus path, is a defect); and the Last
Reviewed value is a valid ISO date. A metadata-run line missing its hard break, a non-bare last
line, a field out of order, an unknown or missing required field, an out-of-vocabulary value, a
missing or mis-placed subtype, an unpinned corpus link, or a malformed date is a finding; an
unreadable or non-UTF-8 page is a fail-loud finding. The narrative document type, the
path-scoped entry-point exemption, the canonical and extension field orders, the subtype table,
the status and claim-class vocabularies, the corpus domain prefixes and root corpus documents,
and the repository root are supplied by the adopter and are not part of this clause; the
markdown pin and body-link patterns and the metadata-contract scan logic are fixed by the check.
A narrative tree whose pages all conform contributes no findings.
