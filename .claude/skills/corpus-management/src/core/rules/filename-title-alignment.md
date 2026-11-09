# Filename and document-title alignment

A document's filename aligns with its declared title. The filename stem, taken after its
document-type prefix, and the ``Document Title`` field are each tokenized (lowercased,
hyphens to spaces, non-alphanumerics dropped, connector stopwords and single-character
tokens removed, project synonyms expanded), and the two token sets share at least a
minimum number of significant content words (by default one, so only a document with zero
shared words is flagged). A document with no title field, a filename that does not begin
with a known document-type prefix, or an empty token set on either side is not applicable
and is not flagged. The document-type prefix set, the synonym map, and the minimum-overlap
threshold are project configuration and are not part of this clause.
