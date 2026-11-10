# Reference-vocabulary defaults for the GRC profile (adopter-overridable)

Each `<concern>.toml` here is a versioned profile (`schema_version = 1` plus one
`[<concern>]` table) loaded by `../../tools/profile_loader.py` and registered in
`../../core/profiles.toml`. An adopter overlays a concern by placing their own
`<concern>.toml` in an adopter directory; the overlay is KEY-LEVEL REPLACE (an
adopter value replaces the whole default value for that key, an absent key falls
back to the default, and an explicit empty value clears it), so overriding one
entry of a list means restating the whole list. The first values shipped were
`citations.toml` (the framework-citation denylist); gate 5 loads it as its live
config (its wrapper literals were removed).
