# Metadata-block line breaks

A run is the rendered paragraph: the lines that render into one
paragraph (GitHub Flavored Markdown 0.29-gfm) form one run, whatever their
indentation, including a paragraph inside a block quote or list item,
read without its markers, and a lazy continuation line. A run ends at a
blank line or a line that starts another block: a heading, a thematic
break or setext underline, a block quote, a list item that can
interrupt the paragraph (or a sibling item of an enclosing list), an
HTML block, a table, or a fence. A setext heading's lines are a run,
because the heading shows them joined. In a run holding two or more
metadata lines (each of the `**Field:**` form), every metadata line
that another line of the run follows carries a Markdown hard-break
marker. Without a hard break, GitHub renders the run as a single
soft-wrapped paragraph rather than as the intended vertical list of
labelled facts. Two hard-break markers are accepted: a trailing
backslash (the library convention) or two or more trailing spaces. The
last line of a run is exempt, because the following blank line or `---`
separator already ends the paragraph. Metadata lines inside a code
block, an HTML block or a table are not paragraph text: a metadata
example inside a fence is not a finding, and a fenced block between
metadata lines ends the run (the lines either side of it are not one
paragraph). A fence closes only on a fence of its own character at
least as long as the opening one. Residual: when a lazy continuation
line that omits the markers of two or more nested block quotes is
indented four or more columns and would start a block once unindented,
the gate checks only the lines of its paragraph before that line, and
no line from that line to the next blank line outside every container.
A field name starts with an ASCII letter and runs to its
closing colon without an asterisk, so it may contain hyphens, slashes,
parentheses and underscores. A run whose non-last lines all
carry a marker, and a single isolated metadata line, are not flagged.
The scanned file set is project configuration and is not part of this
clause.
