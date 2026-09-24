# Symmetric narrative-boundary

A documentation corpus that carries a separate executive-narrative tree keeps a symmetric
placement boundary between the two sides. OUTSIDE the narrative-root tree, no file carries
the narrative document type or any narrative-extension metadata field, anywhere in the
repository (README paths included): a narrative page living outside the tree, or a page
retyped to a corpus document type that retains narrative-extension fields, is a defect
(move the page, never retype it). INSIDE the narrative-root tree, every page carries the
narrative document type and the full narrative-extension field block and carries no corpus
document type; the single path-scoped exemption is the entry-point page (a nested README
under the tree is not exempt). Detection is line-anchored (a metadata-field line at line
start, not a prose mention of a field name) and fence-aware (a fenced example block is not
scanned; a marker-aware scan tracks the opening fence's character and run length, so a
mismatched fence inside it is content, not a toggle). A file that ends inside an open
fence is a fail-loud finding naming the opening line, never a silent skip of the remainder.
The fence model is a local marker-aware approximation, not a full CommonMark parser (any
leading indentation is accepted, a backtick info string may contain a backtick, and
container blocks are not modelled), so the residue that stays silent is a fence
boundary or extent the model gets wrong while its scan still closes before the end of
the file: a line it mis-recognizes as an opener followed by a later closer, or a fence
that CommonMark ends at the edge of its list or blockquote container but this model
carries on to a later fence line. An unreadable or non-UTF-8 file on
either side is a fail-loud finding, never a silent pass. The narrative document type, the
path-scoped entry-point exemption, the narrative-extension field set, the allowed corpus
document-type set, the two line-anchored marker patterns, and the repository scan scope
are supplied by the adopter and are not part of this clause; the fence-aware,
line-anchored scan logic is fixed by the check. A repository whose files honour the
boundary on both sides contributes no findings.
