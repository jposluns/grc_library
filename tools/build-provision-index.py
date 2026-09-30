#!/usr/bin/env python3
"""Provision-restatement index: every corpus surface citing each statute provision (advisory).

WHY. Correcting one clause of a statute on one surface left the same
provision restated on other surfaces with dropped qualifiers, because
reviewers grepped the old PHRASE, not the PROVISION (the #2649 retro:
PIPEDA s. 10.1). This index groups every surface by provision key, so the
question "where else is PIPEDA s. 10.1 restated?" has a mechanical answer.

WHAT. For every normalized key (``PIPEDA s. 10.1``, ``GDPR Art. 33``), each
surface and line citing it, with the pinpoint as written (``10.1(3)``) and the
resolution tier (explicit, line, heading, section, document; see
``tools/provision_citations.py``), plus uncited-phrase candidates from the
seed table (tier ``phrase``). The report goes to stdout. Nothing is written
and no artefact is committed, so there is no ``--check`` drift gate; the tool
is advisory and is not wired into the gate surfaces.

Usage:
    python3 tools/build-provision-index.py
    python3 tools/build-provision-index.py --key "PIPEDA s. 10.1" --key "GDPR Art. 33"
    python3 tools/build-provision-index.py --min-tier explicit --no-phrases --json
    python3 tools/build-provision-index.py --show-unresolved
    python3 tools/build-provision-index.py privacy security/procedure-security-incident-response.md

Exit codes:
    0   report produced (advisory: what it finds never fails the run)
    2   usage error: an unknown flag, a --key naming no instrument, or a
        refused explicit path (missing, or outside this repository)

RESIDUE (stated, not hidden):
  - False negatives: a restatement that neither cites the section nor uses a
    seeded signature phrase is invisible (the pre-#2649 shape of most PIPEDA
    s. 10.1 surfaces); an instrument outside the alias table, a citation
    whose inference is refused, and a heading-less bare citation in a
    document naming no instrument all land in the unresolved bucket
    (``--show-unresolved``), not under a key; ``Section`` / ``§`` citations
    count only with the instrument adjacent; Recitals, Schedules, Annexes and
    ``Principle 4.3`` forms are not parsed; ranges wider than MAX_RANGE_SPAN
    index their endpoints only.
  - False positives: the explicit tier is syntactic adjacency, so a bare
    ``Art 68(7)`` beside ``DORA (`` is an EXPLICIT DORA record even where
    the surrounding prose means MiCA, and --min-tier explicit does NOT
    remove that shape; the line, heading, section and document tiers are
    inferences, and a table cell whose instrument is named only in the
    header row is still attributed to the last instrument named in an
    earlier cell of the same row; a seeded phrase can restate a different
    regime whose wording matches; keys are section-level, so s. 10.1(1) and
    s. 10.1(6) are siblings even when a change touched only one of them.
  - Refused rather than guessed (in the unresolved bucket): a citation whose
    line earlier names two different instruments, a non-explicit citation
    after a foreign-prefix refusal on the same line, and a bare citation
    whose innermost section body and an enclosing heading name different
    instruments.
  Filter with --min-tier explicit for the highest-precision subset.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import asdict

from lint_common import REPO_ROOT, guard_explicit_paths
from provision_citations import (
    DEFAULT_SCAN_ROOTS,
    PHRASE,
    TIERS,
    UNRESOLVED,
    corpus_files,
    format_row,
    group_by_key,
    key_header,
    parse_key_args,
    scan_files,
    tiers_up_to,
    unique_rows,
)


def main(argv: "list[str]") -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", help="Scan roots (default: the corpus surfaces).")
    parser.add_argument("--key", action="append", default=[], metavar="PROVISION",
                        help="Report only this provision (repeatable), e.g. 'PIPEDA s. 10.1'.")
    parser.add_argument("--min-tier", choices=TIERS, default=TIERS[-1],
                        help="Weakest resolution tier to include (default: document, i.e. every tier).")
    parser.add_argument("--no-phrases", action="store_true", help="Omit uncited-phrase candidates.")
    parser.add_argument("--show-unresolved", action="store_true",
                        help="List the citations whose instrument could not be resolved.")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit JSON instead of text.")
    args = parser.parse_args(argv[1:])

    keys = parse_key_args(args.key)
    # Explicit paths are refused when unsound and normalized otherwise (3b21).
    roots = guard_explicit_paths(args.paths, repo_root=REPO_ROOT) if args.paths else list(DEFAULT_SCAN_ROOTS)
    files = corpus_files(roots)
    citations = scan_files(files)
    grouped = group_by_key(citations, tiers=tiers_up_to(args.min_tier), phrases=not args.no_phrases)
    if keys:
        grouped = {key: grouped.get(key, []) for key in keys}
        order = keys
    else:
        order = sorted(grouped, key=lambda k: (-len(set(c.path for c in grouped[k])), k))
    unresolved = [c for c in citations if c.tier == UNRESOLVED]
    tier_counts = Counter(c.tier for c in citations)

    if args.as_json:
        payload = dict(
            files_scanned=len(files),
            tier_counts=dict(tier_counts),
            keys={key: [asdict(c) for c in unique_rows(grouped[key])] for key in order},
            unresolved_count=len(unresolved),
        )
        if args.show_unresolved:
            payload["unresolved"] = [asdict(c) for c in unresolved]
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print(f"Provision-restatement index (advisory): {len(files)} file(s), "
          f"{len(citations)} citation record(s), {len(order)} provision key(s) shown.")
    print("Tiers: " + ", ".join(f"{t}={tier_counts.get(t, 0)}" for t in (*TIERS, PHRASE, UNRESOLVED)))
    for key in order:
        rows = unique_rows(grouped[key])
        print()
        print(key_header(key, rows))
        if not rows:
            print("    (no surface cites this provision at the selected tiers)")
        for c in rows:
            print(format_row(c))
    print()
    if args.show_unresolved:
        print(f"Unresolved citation records ({len(unresolved)}): instrument not in the alias "
              f"table, or inference refused.")
        for c in unresolved:
            print(format_row(c))
    else:
        print(f"{len(unresolved)} citation record(s) left unresolved (--show-unresolved lists them).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
