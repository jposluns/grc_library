#!/usr/bin/env python3
"""Provision-restatement index: every corpus surface citing each statute provision (advisory).

WHY. Correcting one clause of a statute on one surface left the same
provision restated on other surfaces with dropped qualifiers, because
reviewers grepped the old PHRASE, not the PROVISION (the #2649 retro:
PIPEDA s. 10.1). This index groups every surface by provision key, so the
question "where else is PIPEDA s. 10.1 restated?" has a mechanical answer.

WHAT. For every normalized key (``PIPEDA s. 10.1``, ``GDPR Art. 33``), each
surface and line citing it, with the pinpoint as cited (``10.1(3)``; a bare
continuation shows its full form, ``53(1)(b)``) and the resolution tier
(explicit, line, heading, section, document; see
``tools/provision_citations.py``), plus uncited-phrase candidates from the
seed table (tier ``phrase``). In the text report each key's explicit-tier
rows are listed first; every inferred-tier row, and every phrase row, is
listed after them under the label ``unverified candidates (inferred
instrument)`` — four QA rounds found misattribution families that are,
after the round-3 and round-4 explicit-tier fixes, confined to the inferred
tiers, so those rows are candidates a reviewer confirms, not verified
surfaces (in the JSON, each record's ``tier`` field carries the same
information). ``--key`` takes a provision as typed (``PIPEDA s.10.1(3)``)
or any key exactly as this report prints it (``PDPA (Singapore) s. 26D``).
The report goes to stdout, every listing in path and line order. Nothing is
written and no artefact is committed, so there is no ``--check`` drift gate;
the tool is advisory and is not wired into the gate surfaces.

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
    ``Principle 4.3`` forms are not parsed, and a citation continued by ``of
    Schedule 1`` or ``of Annex III`` is refused outright rather than keyed
    (a schedule or annex numbers its own clauses, so the parent Act's
    section numbering does not cover them); a range indexes its endpoints
    only when it is wider than MAX_RANGE_SPAN, starts at a decimal section
    (``PIPEDA ss. 10.1 to 10.3`` keys s. 10.1 and s. 10.3, not s. 10.2;
    ``HIPAA §164.400 to 414`` keys neither 164.402 nor the other real
    even-numbered sections inside it), is unresolved, or resolves to an
    instrument outside CONTIGUOUS_NUMBERING (SOX, 45 CFR, Cal. Civ. Code:
    ``SOX ss. 302 to 306`` keys s. 302 and s. 306 only), since only there
    is every interior number known to be a provision; a decimal range
    whose integer endpoint reads two ways or neither (``ss. 3.1 to 5``:
    s. 3.5 or s. 5?) records that endpoint unresolved; the line tier never
    reuses an alias an earlier citation on the line took as its postfix
    instrument, so a bare citation that DOES continue that instrument
    (``Article 33 of the GDPR ... (Art. 34)``) falls to the heading chain
    when the heading names the same instrument, and stays unresolved
    otherwise; a prefix alias followed by ``of the <Name>`` is refused even
    where the name is that instrument's full title (``PIPEDA s. 10.1 of the
    Personal Information Protection and Electronic Documents Act``) or its
    generic noun continued like a title (``of the Act (PIPEDA)``, ``of the
    Regulation on ...``, ``of the Act respecting ...``, ``of the Regulation
    laying down ...``), since only a structural qualifier (``of Chapter
    III``; never ``of Schedule 1`` or ``of Annex I``, whose clauses the
    Act does not number) and the bare generic noun in SELF_NOUNS (``of the
    Act``) are known not to name another instrument; without an adjacent
    alias, ``of
    the Regulation`` still refuses inference; and a lowercase verb outside
    the subordinate-instrument stop list before a lowercase descriptor
    (``Article 5 of the GDPR harmonises regulations``) refuses a correct
    postfix alias.
  - False positives: the explicit tier requires a KNOWN adjacent alias
    whose marker family matches the citation's marker; an unaliased token,
    an ambiguous alias whose jurisdiction contradicts or never resolves
    (the California agency in ``the section 1798.155 CPPA administrative
    fine``), a prefix alias followed, after the citation, by the name of
    another instrument (``Unlike the GDPR, Article 12 of the Data Act``),
    a postfix alias modifying a subordinate instrument (``Article 12 of the
    DORA RTS``, ``s. 7012 CCPA Regulations``), and an alias-led bracket that
    names an alias before closing (``DORA (Art 68(7), citing DORA Arts
    11-12)``, whose Art 68(7) is MiCA's) never key an explicit record: the
    first four leave the record unresolved (or resolve it from the naming
    tail), the bracket gloss falls to the inferred tiers without its lead
    and prints as an unverified candidate. Adjacency is still syntactic: a
    bare citation right after a resolved alias the prose does not mean,
    with nothing after the citation naming another instrument (``Unlike the
    GDPR, Article 12 applies`` in a Data Act paragraph), is still an
    EXPLICIT record of that alias; the subordinate-instrument words are a
    fixed list (RTS, ITS, Regulations, Rules, Implementing, Delegated,
    Guidelines, Technical Standards, Decree, Ordinance, Order, and the
    lowercase regulations, implementing, delegated, guidelines and technical
    standards), so another subordinate form (``Article 5 of the GDPR Code of
    Conduct``; ``s. 7012 of the CCPA rules``, since lowercase ``rules`` is
    too common in prose to count) is still keyed to the alias; the
    SELF_NOUNS exemption trusts ``of the Regulation`` after a GDPR prefix
    even where the prose means another regulation it named earlier (the
    adjacency residue above, in another form), and its title-continuation
    stop list is fixed (on, of, for, to, respecting, concerning, regarding,
    relating, governing, establishing, laying, implementing, amending,
    supplementing, setting), so a noun continued by a word outside it
    (``of the Act against unfair practices``) is still keyed to the alias;
    and a conjoined prefix of two
    instruments that share article numbering (``GDPR / UK GDPR Article
    21``, the only such pair in
    SHARED_NUMBERING) indexes the citation under BOTH, explicitly, even
    where the prose meant to qualify one (the provision is the same text in
    both, so the sibling is real either way). Every other conjoined member
    (``the LGPD and GDPR Article 20``) is keyed at the line tier, as a
    candidate. The line, heading, section and document tiers are INFERENCES
    — hence the ``unverified candidates (inferred instrument)`` label — and
    three shapes systematically defeat them: a CROSSWALK document about an
    instrument OUTSIDE the alias table (the eIDAS annex) attributes that
    instrument's articles at the line and heading tiers to whatever aliased
    instrument the same line or heading compares it with (``## DORA and
    sector-specific lex specialis (Article 4)`` in the NIS2 annex is keyed
    as DORA Art. 4 and collides with the real DORA key); a PROSE line that
    names an instrument in passing (not as a citation's postfix) before a
    bare citation of another attributes that citation to the named one; and
    the line tier never sees a table's header row, so a cell whose
    instrument is named only in the header is attributed to the last
    instrument an earlier cell of the SAME row names (or, with none, to the
    heading chain). An alias-led bracket gloss sends its citation to the
    heading chain without the lead, so a heading naming another instrument
    takes it (``## DORA mapping`` over ``GDPR (Art. 6(1)(f), balanced
    against the GDPR Art. 21 objection)`` is heading-tier DORA Art. 6; the
    same rule resolves the MiCA annex's Art 68(7) to MiCA, correctly). A
    seeded phrase can restate a different regime whose wording matches;
    keys are section-level, so s. 10.1(1) and s. 10.1(6)
    are siblings even when a change touched only one of them.
  - Refused rather than guessed (in the unresolved bucket): a citation whose
    marker family disagrees with the resolved instrument's marker style
    (``CCPA Article 10``: Cal. Civ. Code is an ``s.`` statute, so the ``Art``
    marker means the 11 CCR CCPA Regulations), a citation adjacent to an
    ambiguous alias whose jurisdiction contradicts its table row or never
    resolves (``CPPA Section 63(3)`` with no Canada context is REFUSED even
    though Bill C-27 is meant — recall ceded to keep the California agency
    shape out of the explicit tier; with a ``Section``/``§`` marker the
    refusal drops the record entirely, per the explicit-only rule), a
    citation whose line earlier names two different instruments (a comma
    chain, ``UK GDPR, LGPD Art 37``, never extends prefix adjacency: it is
    a framework enumeration, and only LGPD is keyed), a non-explicit
    citation after a foreign-prefix refusal on the same line, a bare
    citation whose innermost section body and an enclosing heading name
    different instruments, and a bare citation whose earlier aliases on the
    line are bound to earlier postfix citations of an instrument the
    heading chain contradicts (``## NIS2 reporting`` over ``Article 33 of
    the GDPR ...; Article 34 ...``). The ``29`` of a citation-shaped body
    name (``Article 29 Working Party``) is skipped, not recorded at all;
    only that ``29`` is (``Arts. 28 and 29 WP`` keeps Art. 28).
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
    CANDIDATE_LABEL,
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
    split_rows,
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
    # Sorted like every other listing, so the unresolved bucket's order never
    # depends on the order the scan roots were walked in.
    unresolved = sorted((c for c in citations if c.tier == UNRESOLVED),
                        key=lambda c: (c.path, c.line, c.col))
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
        confirmed, candidates = split_rows(rows)
        print()
        print(key_header(key, rows))
        if not rows:
            print("    (no surface cites this provision at the selected tiers)")
        for c in confirmed:
            print(format_row(c))
        if candidates:
            print(f"    {CANDIDATE_LABEL}:")
            for c in candidates:
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
