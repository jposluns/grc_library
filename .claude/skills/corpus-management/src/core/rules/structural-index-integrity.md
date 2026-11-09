# Structural index integrity

A documentation corpus organized into domain directories keeps its central
document-index register and its per-domain README indexes complete and
resolvable. Four properties hold: every active domain document (a `.md` file under
a domain directory that is not a README and is not exempt) is referenced by the
central index register; every active domain document is referenced by its own
domain README; every path the index register references exists on disk; and every
path each domain README references exists on disk. A referenced path is the display
text of a Markdown link whose code-span display text ends in `.md` (the convention that
the code-span display carries the repository-relative path). A missing central
index register is a single terminal finding; a missing domain README is a finding
for that domain. The domain list, the index-register path, the files exempt from
the membership rule, and the exempt directory prefixes are project configuration
and are not part of this clause; a corpus whose index register and domain READMEs
are complete and resolvable contributes no findings.
