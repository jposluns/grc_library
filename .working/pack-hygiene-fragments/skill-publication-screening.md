# Removed from skills/publication-screening/SKILL.md (pack-hygiene scrub)

Each entry records a project-specific fragment removed or genericized in the
pack-hygiene generalization pass, verbatim, with the replacement named. The concrete
values now live in the file's `## Project wiring` section.

## Frontmatter `description` (scanner tool path)

```
It combines a mechanical instruction-content scan (`tools/scan-publication-instruction-content.py`) with a provenance, integrity, and corroboration read
```

Replaced by: "It combines a mechanical instruction-content scan (the project's advisory scanner) with a provenance, integrity, and corroboration read".

## Overview, paragraph 1 (bucket path styling)

```
are trusted ground truth, and `publications/` is untrusted by default (vendor
```

Replaced by: "are trusted ground truth, and the publications bucket is untrusted by default (vendor"; the concrete `publications/` path is in the project wiring.

## Overview, paragraph 2 (dated maintainer directive, TODO key, scanner path)

```
`publication-screening` is the formal process (maintainer-directed 2026-06-25, TODO
2.11). It is a two-part instrument: the mechanical half is the advisory scanner
`tools/scan-publication-instruction-content.py` (recall-oriented pattern classes:
```

Replaced by: "`publication-screening` is the formal process. It is a two-part instrument: the mechanical half is the advisory scanner named in the project wiring (recall-oriented pattern classes:".

## Overview, paragraph 2 (register path)

```
The durable record is the reference base's
`publications/SCREENING.md` register (one row per publications catalogue item, exact
catalogue title as the join key), and the reference-base validation gate fails on a
```

Replaced by: "The durable record is the reference base's screening register (named in the project wiring; one row per publications catalogue item, exact catalogue title as the join key), and the reference-base validation gate fails on a".

## Overview, closing paragraph (TODO-key attribution of the honest-backstop framing)

```
for use-time corroboration. Honest-backstop framing (the TODO 2.11 wording): the
process raises the bar against poisoned reference input; it does not by itself
```

Replaced by: "for use-time corroboration. Honest-backstop framing: the process raises the bar against poisoned reference input; it does not by itself" (the framing is kept; only the backlog-key attribution is dropped).

## When to Use, first bullet (bucket path styling)

```
- **On every new `publications/` ingest**, as part of the ingest workflow (the value
```

Replaced by: "- **On every new publications-bucket ingest**, as part of the ingest workflow (the value".

## When to Use, last bullet (scanner flag)

```
  templates follow their own currency and integrity disciplines; the scanner's
  `--all-buckets` mode is available as a cheap paranoia pass on any new ingest, but
  the register and this protocol govern the publications bucket.
```

Replaced by: the same bullet with "the scanner's whole-base mode"; the `--all-buckets` flag name is in the project wiring.

## Process step 1 (register path, catalogue file, gate command)

```
re-screen. Read the reference base's `publications/SCREENING.md` register and
`catalogue.yml` publications section, and confirm the reference-base validation gate
(`python3 tools/validate.py` in the reference repo) is green before screening; the
```

Replaced by: "re-screen. Read the reference base's screening register and its catalogue's publications section, and confirm the reference-base validation gate (the project wiring names the command) is green before screening; the".

## Process step 3 (scanner invocation)

```
Run `python3 tools/scan-publication-instruction-content.py --files <extract paths>`
(or bucket-wide without `--files`). The scanner always exits 0; its findings are
```

Replaced by: "Run the mechanical scanner named in the project wiring over the in-scope extract paths (or bucket-wide). The scanner always exits 0; its findings are".

## See Also (scanner bullet and reference-base conventions bullet)

```
- The advisory scanner [`tools/scan-publication-instruction-content.py`](../../../../tools/scan-publication-instruction-content.py):
  the mechanical half (pattern classes, `--files`, `--all-buckets`; not a gate; always
  exits 0).
- The reference base's own conventions: the `publications/` README (bucket trust
  posture and the ingest steps), `publications/SCREENING.md` (the register this
  protocol writes), and the reference-base `tools/validate.py` gate (the enforcement
  half; never weaken it to pass, fix the artefact).
```

Replaced by: an unlinked "advisory scanner named in the project wiring" bullet (recall-oriented pattern classes; per-file and whole-base modes) and a genericized conventions bullet ("its publications-bucket README ... the screening register this protocol writes ... the reference-base validation gate"), each closing with a pointer to the project wiring for concrete names.
