# Section-anchor resolution

A markdown link of the form `[text](path#anchor)` (or a same-document
`[text](#anchor)`) resolves its `#anchor` to a real heading in the target file.
Headings are read outside fenced code blocks and slugified per the GitHub flavour
rules (lowercase; drop characters that are not alphanumeric, space, hyphen, or
underscore; spaces to hyphens; consecutive hyphens collapsed); an anchor matching
no heading slug in its resolved target is flagged. An external-scheme URL
(`http://`, `https://`, `mailto:`) is skipped, as is a link whose target file does
not exist (the separate link-existence check owns that case). The link title text
after the anchor is ignored (only the `#anchor` fragment is validated). A file with
no such anchored link contributes no findings.
