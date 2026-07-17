<!-- SIBLING-PLACEHOLDER: scratch -->
# `.scratch` placeholder

In-repo placeholder for the `grc_library_scratch` sibling repository: the worker-exchange
channel (research seeds, candidate diffs, the credit-offload queue) the orchestrator and
its workers use. The maintainer runs the real sibling beside this repo (resolved at
`../grc_library_scratch`); exchange-dependent tooling prefers that when present, falls
back to this placeholder, then degrades to a clean no-op.

Adopters: point your own exchange channel at `../grc_library_scratch`, or leave this stub
and the worker-exchange advisory tools will skip cleanly. This directory is a placeholder
only: it must contain nothing but this README (a hard gate enforces that). See TODO
section 1.19.
