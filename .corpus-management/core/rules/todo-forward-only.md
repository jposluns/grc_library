# Forward-looking backlog (no item marked done in place)

A backlog item is not marked done in place: it carries no strikethrough span
(``~~...~~``), no bracketed ``[done]`` or ``[completed]`` status tag, and no
``Status: completed`` or ``Status: done`` field. A forward-looking backlog holds only
open work, so a closed item is removed from it (its completion recorded in the project's
change history or a separate closed-work ledger), never annotated done and left in place.
Each line is read outside fenced code blocks, and inline backtick code spans are stripped
before matching, so a backticked mention of a marker (naming the strikethrough or a tag in
prose) is not flagged; a line carrying none of the three done-markers is not flagged.
