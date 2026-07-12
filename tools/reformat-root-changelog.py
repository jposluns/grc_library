#!/usr/bin/env python3
"""Mechanical reformat of the root CHANGELOG to the compact header format.

Stage 3a of the CHANGELOG restructure (TODO 3.19 PR 3): converts every root
``CHANGELOG.md`` entry HEADER from the long form to the compact form, leaving
every body byte untouched:

    ## 2026-07-08, Library Version 2026.07.201, PR #713
becomes
    **2026-07-08 | 2026.07.201 | PR #713**

Early PR-less headers become ``**YYYY-MM-DD | X.Y.Z**``; the one initial-release
header is special-cased (its licence note is preserved as the first body line if
the body does not already carry it). Stage 3b (the compression wave) later merges
a 1-2 sentence summary onto the header line, reaching the target
``**date | version | PR** - summary`` form; the parsers this PR updates accept
the header with or without the ``- summary`` tail, so 3b needs no further parser
change.

Safety model (this edits a 1 MB audit-trail artefact):
- ``--check`` (default): print what would change and the verification result; no
  write.
- ``--write``: transform, VERIFY, and only then replace the file. Verification
  asserts (a) the ordered (date, version, PR) triple sequence is byte-identical
  before and after, (b) every non-header line is byte-identical and in order,
  (c) the transform is idempotent (a second pass changes nothing), and (d) no
  em/en dash was introduced. Any assertion failure leaves the original file in
  place and exits 1.

Exit codes: 0 clean (check ok or write verified); 1 verification failure;
2 usage/internal error. Stdlib-only Python 3.11.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TARGET = REPO_ROOT / "CHANGELOG.md"

LONG_HEADER = re.compile(
    r"^## (\d{4}-\d{2}-\d{2}), Library Version ([0-9.]+)(?:, PR #(\d+))?$")
COMPACT_HEADER = re.compile(
    r"^\*\*(\d{4}-\d{2}-\d{2}) \| ([0-9.]+)(?: \| PR #(\d+))?\*\*(?: - .*)?$")
INITIAL_RELEASE = re.compile(
    r"^## Initial public release \((\d{4}-\d{2}-\d{2}), Library Version "
    r"([0-9.]+)\): (.+)$")
DASH_RE = re.compile("[–—]")


def compact(date: str, version: str, pr: str | None) -> str:
    core = f"{date} | {version}" + (f" | PR #{pr}" if pr else "")
    return f"**{core}**"


def transform(lines: list[str]) -> tuple[list[str], list[tuple]]:
    out: list[str] = []
    triples: list[tuple] = []
    for i, line in enumerate(lines):
        m = LONG_HEADER.match(line)
        if m:
            triples.append((m.group(1), m.group(2), m.group(3)))
            out.append(compact(m.group(1), m.group(2), m.group(3)))
            continue
        m = INITIAL_RELEASE.match(line)
        if m:
            triples.append((m.group(1), m.group(2), None))
            out.append(compact(m.group(1), m.group(2), None))
            # Preserve the header's own information as body text unless the
            # following body already states it.
            tail = "".join(lines[i + 1:i + 6])
            if "Initial public release" not in tail:
                out.append("")
                out.append(f"Initial public release: {m.group(3)}.")
            continue
        out.append(line)
    return out, triples


def parse_triples(lines: list[str]) -> list[tuple]:
    triples = []
    for line in lines:
        m = LONG_HEADER.match(line) or COMPACT_HEADER.match(line)
        if m:
            triples.append((m.group(1), m.group(2), m.group(3)))
            continue
        m = INITIAL_RELEASE.match(line)
        if m:
            triples.append((m.group(1), m.group(2), None))
    return triples


def verify(before: list[str], after: list[str]) -> list[str]:
    problems: list[str] = []
    t_before, t_after = parse_triples(before), parse_triples(after)
    if t_before != t_after:
        problems.append(
            f"triple sequence changed: {len(t_before)} before, "
            f"{len(t_after)} after (first divergence at index "
            f"{next((i for i, (a, b) in enumerate(zip(t_before, t_after)) if a != b), min(len(t_before), len(t_after)))})")
    body_before = [l for l in before
                   if not (LONG_HEADER.match(l) or INITIAL_RELEASE.match(l))]
    body_after = [l for l in after
                  if not (COMPACT_HEADER.match(l)
                          or l.startswith("Initial public release: "))]
    # The special-case may add one blank separator line; normalize runs of
    # blanks for the body comparison, order preserved.
    def squeeze(ls: list[str]) -> list[str]:
        out, prev_blank = [], False
        for l in ls:
            blank = l.strip() == ""
            if not (blank and prev_blank):
                out.append(l)
            prev_blank = blank
        return out
    if squeeze(body_before) != squeeze(body_after):
        problems.append("a non-header body line changed (order-preserving "
                        "comparison failed)")
    again, _ = transform(after)
    if again != after:
        problems.append("transform is not idempotent on its own output")
    introduced = sum(1 for l in after if DASH_RE.search(l)) - \
        sum(1 for l in before if DASH_RE.search(l))
    if introduced > 0:
        problems.append(f"{introduced} em/en dash line(s) introduced")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    ap.add_argument("--write", action="store_true",
                    help="Verify then replace the file (default: check only).")
    args = ap.parse_args(argv)

    try:
        text = args.target.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    lines = text.split("\n")
    converted, triples = transform(lines)
    n_headers = sum(1 for l in lines if LONG_HEADER.match(l)
                    or INITIAL_RELEASE.match(l))
    already = sum(1 for l in lines if COMPACT_HEADER.match(l))
    problems = verify(lines, converted)

    print(f"# Root-CHANGELOG mechanical reformat ({args.target})")
    print(f"- Long-form headers found: {n_headers} (compact already present: "
          f"{already})")
    print(f"- Triples parsed: {len(triples)}; with PR "
          f"{sum(1 for t in triples if t[2])}, without "
          f"{sum(1 for t in triples if not t[2])}")
    if problems:
        for p in problems:
            print(f"- VERIFY FAIL: {p}")
        return 1
    print("- Verification: triples lossless and ordered; bodies byte-identical "
          "(order-preserving); idempotent; no dash introduced.")
    if args.write:
        args.target.write_text("\n".join(converted), encoding="utf-8")
        print(f"- WROTE {args.target}")
    else:
        print("- Check mode: no write. Re-run with --write to apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
