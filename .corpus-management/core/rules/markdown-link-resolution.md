# Markdown link resolution

Every internal markdown link target resolves to an existing path inside the
repository. A link whose target is external (an `http:`, `https:`, `mailto:`,
`tel:`, or `ftp:` URL, or a pure `#`-fragment) is not checked. For an internal
target, a trailing `#anchor` fragment is stripped, the remainder is resolved
relative to the directory containing the source file, and the resolved path must
both exist and lie inside the repository root. A link inside a fenced code block
is illustrative content, not a live reference, so it is skipped (the shared
fence-aware scan toggles state on each fence line). A target that resolves outside
the repository, or to a path that does not exist, is a broken link and is flagged.
