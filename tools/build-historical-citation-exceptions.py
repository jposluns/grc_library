#!/usr/bin/env python3
"""Render the historical-context citation exception table from its data file (3b75).

Writes the generated block of .project-governance/register-historical-citation-exceptions.md from
.project-governance/register-historical-citation-exceptions.toml. An absent data file renders an
empty table. --check writes nothing: exit 0 in sync, 1 on drift, 2 on malformed input. Gate 6
(tools/lint-standards-currency.py) refuses the same drift, so a stale page cannot pass CI.

Usage: python3 tools/build-historical-citation-exceptions.py [--check] [--root DIR]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import historical_citation_register as H  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="report drift; write nothing")
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = ap.parse_args(argv)
    data, page_path = args.root / H.DATA_REL, args.root / H.PAGE_REL
    try:
        rows = H.load(data.read_bytes().decode("utf-8")) if data.exists() else []
        page = page_path.read_bytes().decode("utf-8")
        new = H.with_block(page, rows)
    except (H.RegisterDataError, OSError, UnicodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.check:
        if new != page:
            print(f"DRIFT: {H.PAGE_REL} differs from {H.DATA_REL}; run without --check", file=sys.stderr)
            return 1
        print(f"OK: {H.PAGE_REL} is in sync ({len(rows)} row(s)).")
        return 0
    if new != page:
        page_path.write_bytes(new.encode("utf-8"))
        print(f"Wrote {H.PAGE_REL} ({len(rows)} row(s)).")
    else:
        print(f"OK: {H.PAGE_REL} already in sync ({len(rows)} row(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
