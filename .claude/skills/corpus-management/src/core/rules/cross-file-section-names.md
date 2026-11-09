# Cross-file section names

A reference that pairs a section NUMBER with a heading TITLE of another corpus
document cites the title's actual number in the resolved target. This is the
title-fit layer above the numbers phase (cross-file-section references): where a
citation names a target section by number AND quotes or parenthesizes a title, the
quoted title must belong to the numbered heading actually cited. The check fires on
the same two resolvable-target classes (an adjacent-link reference, and a
binding-declaration reference that binds subsequent bare references to a declared
target), and it owns one seam the numbers phase excludes: on a table row, an
anchored-title reference to a number that is not a numbered heading in the target
is flagged here. A title candidate is a parenthetical or a double-quoted run
immediately after the reference; titles are read from markdown headings (an inline
clause carries no title). A candidate that matches no heading title in the target
is not treated as a title claim (it may be ordinary prose); only a candidate that
IS some heading's title anchors the check, and the finding names which heading
actually carries that title. The shared cross-file reference-extraction config and
the exempt-file set are project configuration and are not part of this clause; a
reference whose number+title agree, and a document that makes no such pairing,
contribute no findings.
