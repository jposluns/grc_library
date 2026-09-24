# CCM family-range provider-to-tenant member direction

A CCM control-family range citation on an internal-scope document does not sweep in a
provider-to-tenant ("directional") control member. Some CSA Cloud Controls Matrix
controls state a duty the cloud provider owes the tenant rather than a control the
document's own organization operates; citing a family range (for example "CCC-01 to
09") that spans such a member silently pulls a provider-duty control into an
internal-scope claim. The check reads every line, fenced code blocks included, so no
block structure can hide an active citation; it skips only blockquote lines (quotation)
and inline code spans, read as CommonMark defines them (a code span needs a closing
backtick run of exactly the opening length, and a backslash-escaped backtick is literal).
A range written as an example is therefore placed in a blockquote or an inline code span,
not a fenced block. It finds each single-family
range, expands it to its member codes, and flags any that fall in the tracked
directional-member set, advising that the range be split to exclude them. A
mixed-family range (a range whose two endpoints name different families) is malformed
rather than a single-family citation and is not expanded. The tracked set of
directional provider-to-tenant members is supplied by the adopter and is not part of
this clause; it is extended as new directional members surface. Which documents are
provider-facing, and so outside the internal-scope claim, is likewise project
configuration, declared explicitly rather than inferred from prose. A document whose
family-range citations sweep in no directional member contributes no findings.
