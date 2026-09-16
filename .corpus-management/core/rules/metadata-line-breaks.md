# Metadata-block line breaks

A run of two or more consecutive metadata lines (each of the
`**Field:**` form) carries a Markdown hard-break marker on every line
but its last. Without a hard break, GitHub renders the run as a single
soft-wrapped paragraph rather than as the intended vertical list of
labelled facts. Two hard-break markers are accepted: a trailing
backslash (the library convention) or two or more trailing spaces. The
last line of a run is exempt, because the following blank line or `---`
separator already ends the paragraph. Metadata lines inside a fenced
code block are documentation of the metadata-block format, not a file's
own metadata, so the shared fence-aware scan skips them: a metadata
example inside a fence is not a finding. A run whose non-last lines all
carry a marker, and a single isolated metadata line, are not flagged.
The scanned file set is project configuration and is not part of this
clause.
