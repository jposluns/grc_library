# Positional backlog-token references

Prose does not cite a backlog item by its position: a reference qualified by ``TODO``,
``TODO item(s)``, or ``backlog item(s)`` immediately followed by a section-shaped token
(a ``§``- or ``P``-prefixed number, or a dotted ``N.M``) is flagged, because a backlog
item's position is not a durable identifier and a later renumber silently mis-resolves
the reference. A bare single digit with no prefix and no dot is not matched (too
ambiguous), and a qualifier with no following section token, ordinary prose using the
word ``backlog`` or ``TODO`` alone, a blockquote line, and a match inside an inline code
span or fenced block are all not flagged. The exempt files (the backlog source and its
append-only history, where positional tokens legitimately live) are the project's scan
configuration and are not part of this clause.
