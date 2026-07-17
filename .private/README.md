<!-- SIBLING-PLACEHOLDER: private -->
# `.private` placeholder

In-repo placeholder for the `grc_library_private` sibling repository: the maintainer's
durable operational state and process narrative (living design docs, dated archives, aged
roll-up rows). The maintainer runs the real sibling beside this repo (resolved at
`../grc_library_private`); operational-state tooling prefers that when present, falls back
to this placeholder, then degrades to a clean no-op.

Adopters: point your own private operational store at `../grc_library_private`, or leave
this stub and run self-contained. This directory is a placeholder only: it must contain
nothing but this README (a hard gate enforces that, so no private operational state is
ever committed to the public repo). See TODO section 1.19.
