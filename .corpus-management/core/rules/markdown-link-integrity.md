# Markdown link integrity

No scanned markdown file contains a nested markdown link of the form
`[[text](url)](url)`, a link whose visible text is itself a link. In
GitHub-flavoured Markdown it renders as a broken literal `[` followed by a
dangling `](url)`. The malformation is invisible to a link-coverage check (the
inner link is well-formed) and to a broken-link check (the inner link
resolves), so it is caught here by its `[[X](url)](url)` structure. Inline code
spans are neutralized before the check, so a code-span description of the
pattern in prose is not flagged while a live malformation still is; to describe
the pattern in prose, wrap the whole token in a backtick code span.
