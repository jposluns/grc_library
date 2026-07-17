<!-- SIBLING-PLACEHOLDER: ref -->
# `.ref` placeholder

In-repo placeholder for the `grc_library_ref` sibling repository: the trust-bucketed
reference knowledge base (standards, frameworks, legislation, publications) the corpus
cites. The maintainer runs the real sibling beside this repo (resolved at
`../grc_library_ref`); reference-dependent tooling prefers that when present, falls back
to this placeholder, then degrades to a clean no-op.

Adopters: point your own reference base at `../grc_library_ref`, or leave this stub and
the reference-breadth advisory tools will skip cleanly. This directory is a placeholder
only: it must contain nothing but this README (a hard gate enforces that, so no reference
content is ever committed to the public repo). See TODO section 1.19.
