#!/usr/bin/env python3
"""Provision-sibling audit: for changed documents, every OTHER surface citing the same provisions (advisory).

WHY. The #2649 retro: a PR corrected PIPEDA s. 10.1 on one surface while the
same provision stayed restated, with dropped qualifiers, on other surfaces,
because review searched for the old phrase rather than the provision. Run
on the documents a PR changes, this tool lists, per provision each document
cites, the other surfaces that cite it too, so a QA brief can ask of each
one "does this restatement still match the corrected text?".

WHAT. Every provision key cited (or matched by a seeded uncited phrase) in
each --docs file — at ANY tier; the audited document's own citations are
never tier-filtered — is looked up in the corpus index built by
``tools/provision_citations.py``. Each other surface citing the key at the
TRUSTED tier(s) — by default only ``explicit``, the tier whose instrument
the source itself names — is listed as a sibling with its line, pinpoint,
resolution tier and a snippet. Every other-surface row at a weaker,
inferred tier, and every uncited-phrase hit, is listed after the siblings
under the label ``unverified candidates (inferred instrument)``: two QA
rounds found misattribution families confined to the inferred tiers (the
crosswalk and point-designation shapes; see the residue list in
``tools/build-provision-index.py``), so a reviewer can act on the sibling
list directly but must confirm a candidate row's instrument first.
``--min-tier`` widens the trusted set (``--min-tier document`` trusts every
citation tier, restoring the pre-split single list, except that phrase rows
always stay candidates); the label, and the closing note that names it,
print only when some candidate row does. The document's own lines are
summarized, not listed. Provisions no other surface cites are named on one
line. Advisory: it reports, it never fails a run, and it is not wired into
the gate surfaces.

Usage:
    python3 tools/audit-provision-siblings.py --docs privacy/jurisdictions/annex-privacy-canada.md
    python3 tools/audit-provision-siblings.py --docs a.md b.md --provision "PIPEDA s. 10.1"
    python3 tools/audit-provision-siblings.py --docs a.md --min-tier heading --no-phrases --json
    git diff --name-only --diff-filter=d origin/main...HEAD -- '*.md' \\
        | xargs -r python3 tools/audit-provision-siblings.py --docs

``--scan PATH...`` replaces the default corpus roots (the regression tests
point it at a fixture tree).

Exit codes:
    0   report produced (advisory: sibling hits never fail the run)
    2   usage error: no --docs, a --docs entry that is missing, outside this
        repository, or not a Markdown file (pass only the PR's surviving .md
        files), a refused --scan path, or a --provision naming no instrument

RESIDUE: the extractor's residue applies unchanged (see
``tools/build-provision-index.py``; the inferred-tier misattribution shapes
stated there are why those rows print as unverified candidates here).
Specific to this tool: a sibling is matched at SECTION level, so a PR
touching only s. 10.1(3) still lists every s. 10.1 surface; a changed
document whose edit REMOVED a citation no longer cites it, so that
provision's siblings are not listed (run the tool on the base revision of
the file as well when a citation was deleted); and a restatement that cites
no section and matches no seeded phrase is not found.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict

from lint_common import REPO_ROOT, guard_explicit_paths
from provision_citations import (
    CANDIDATE_LABEL,
    DEFAULT_SCAN_ROOTS,
    TIERS,
    corpus_files,
    format_row,
    group_by_key,
    parse_key_args,
    scan_files,
    split_rows,
    tiers_up_to,
    unique_rows,
)


def audit(docs: "list[str]", roots: "list[str]", *, trusted, phrases: bool, wanted) -> list:
    """Per document: [(key, own lines, trusted sibling rows, unverified candidate rows)].

    Keys are in first-cited order. The document's OWN citations are collected
    at every tier (a document that cites a provision only via a heading or a
    seeded phrase still wants its siblings); ``trusted`` filters only which
    OTHER-surface rows count as siblings rather than candidates.
    """
    index = group_by_key(scan_files(corpus_files(roots)), tiers=TIERS, phrases=phrases)
    report = []
    for doc in docs:
        own = group_by_key(scan_files([REPO_ROOT / doc]), tiers=TIERS, phrases=phrases)
        entries = []
        for key in sorted(own, key=lambda k: (min(c.line for c in own[k]), k)):
            if wanted and key not in wanted:
                continue
            own_lines = sorted(set(c.line for c in own[key]))
            rows = unique_rows(c for c in index.get(key, []) if c.path != doc)
            siblings, candidates = split_rows(rows, trusted)
            entries.append((key, own_lines, siblings, candidates))
        report.append((doc, entries))
    return report


def main(argv: "list[str]") -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--docs", nargs="+", required=True, metavar="PATH",
                        help="The changed Markdown documents to audit.")
    parser.add_argument("--scan", nargs="+", metavar="PATH",
                        help="Corpus roots searched for siblings (default: the corpus surfaces).")
    parser.add_argument("--provision", action="append", default=[], metavar="PROVISION",
                        help="Report only this provision (repeatable), e.g. 'GDPR Art. 33'.")
    parser.add_argument("--min-tier", choices=TIERS, default=TIERS[0],
                        help="Weakest tier listed as a SIBLING (default: explicit). Weaker tiers "
                             "still print, as unverified candidates.")
    parser.add_argument("--no-phrases", action="store_true", help="Omit uncited-phrase candidates.")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit JSON instead of text.")
    args = parser.parse_args(argv[1:])

    wanted = set(parse_key_args(args.provision))
    docs = guard_explicit_paths(args.docs, repo_root=REPO_ROOT)
    for doc in docs:
        if not doc.endswith(".md") or not (REPO_ROOT / doc).is_file():
            print(f"ERROR: --docs {doc}: not a Markdown file; pass the changed .md documents only.",
                  file=sys.stderr)
            return 2
    roots = guard_explicit_paths(args.scan, repo_root=REPO_ROOT) if args.scan else list(DEFAULT_SCAN_ROOTS)
    report = audit(docs, roots, trusted=tiers_up_to(args.min_tier), phrases=not args.no_phrases,
                   wanted=wanted)

    if args.as_json:
        payload = [
            dict(
                doc=doc,
                provisions=[
                    dict(key=key, cited_on_lines=own_lines,
                         other_surfaces=sorted(set(c.path for c in siblings)),
                         siblings=[asdict(c) for c in siblings],
                         candidate_surfaces=sorted(set(c.path for c in candidates)),
                         unverified_candidates=[asdict(c) for c in candidates])
                    for key, own_lines, siblings, candidates in entries
                ],
            )
            for doc, entries in report
        ]
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    for doc, entries in report:
        restated = [e for e in entries if e[2]]
        candidate_only = [e for e in entries if not e[2] and e[3]]
        print(f"=== {doc}: {len(entries)} provision(s) cited, {len(restated)} restated elsewhere "
              f"at the trusted tier(s), {len(candidate_only)} with unverified candidates only")
        for key, own_lines, siblings, candidates in entries:
            if not siblings and not candidates:
                continue
            cited = ", ".join(f"L{n}" for n in own_lines)
            print(f"  {key}  (cited here on {cited}; "
                  f"{len(set(c.path for c in siblings))} trusted sibling surface(s); "
                  f"{len(set(c.path for c in candidates))} unverified candidate surface(s))")
            for c in siblings:
                print(format_row(c))
            if candidates:
                print(f"    {CANDIDATE_LABEL}:")
                for c in candidates:
                    print(format_row(c))
        alone = [key for key, _own, sib, cand in entries if not sib and not cand]
        if alone:
            print("  cited on no other surface: " + ", ".join(alone))
        print()
    if any(e[3] for _doc, entries in report for e in entries):
        print("Advisory (exit 0). Rows above the '" + CANDIDATE_LABEL + "' label resolve at the "
              "trusted tier(s); rows under it are instrument inferences or uncited-phrase "
              "candidates: confirm each surface against the corrected text before editing it.")
    else:
        print("Advisory (exit 0). Every row above resolves at the trusted tier(s): confirm each "
              "surface against the corrected text before editing it.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
