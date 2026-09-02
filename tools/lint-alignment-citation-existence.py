#!/usr/bin/env python3
"""Fabricated alignment-citation existence audit (registry-driven).

Catches control/section identifiers cited in the corpus that do NOT exist in the
named framework EDITION's catalogue -- the "fabricated code" class the framework
existence gates 48/49/54/58/61 do not cover for these frameworks (a wrong control
*mapping* stays an authorial judgement; a nonexistent *code* is mechanically
checkable). Same philosophy and shape as `lint-ssdf-control-ids.py`.

It consumes ONLY the committed factual registry `alignment_citation_reference.py`
(never the held `grc_library_ref` at run time), so it works in a sibling-free clone
(portability). Only an unknown identifier attributed to a catalogue marked
`status="complete"` is a fabricated-code error.

Coverage in this initial cut: NIST Privacy Framework 1.0 (the smallest complete,
edition-pinned catalogue: 18 categories, 100 subcategories). The PF `XX.YY-P`
family is unique in the corpus (no other cited framework uses the `-P` suffix on a
letter.letter code), so any such token is a Privacy-Framework citation (the same
family-uniqueness argument `lint-ssdf-control-ids.py` mode A uses).

RANGE-AWARE: a range cite such as `CT.PO-P1 to P5` is expanded and its endpoints
validated -- the exact bare-token/RANGE shape the per-PR D13 stranded-code gate does
not scan (resume /validate 2026-09-02, template-privacy-notice.md:162).

Modes:
  * default (report-only): print any fabricated code, exit 0. Use during the
    report-first rollout to inventory + clear the baseline.
  * --strict: exit 1 on any fabricated code (blocking-gate mode, wired once the
    baseline is clean).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_common import (  # noqa: E402
    REPO_ROOT, iter_markdown_targets, read_text_safe, iter_non_code_lines,
)
from alignment_citation_reference import REGISTRY  # noqa: E402

# Files where a code-shaped string is historical description / an example, not a live cite.
# Markdown files where a code-shaped string is historical description / an example, not
# a live citation. (The walker is iter_markdown_targets, so only .md files reach here;
# the registry and this lint are .py and are never scanned.)
EXEMPT_SUFFIXES = (
    "CHANGELOG.md",
    "governance/specification-audit-programme.md",        # gate-description prose uses example codes
    "governance/specification-citation-verification.md",  # ditto
)

# The Privacy-Framework catalogue (only complete catalogue in this cut).
_PF = REGISTRY["nist-privacy-framework-1.0"]
_PF_ALL = _PF["all"]
_PF_NAME = f'{_PF["name"]} {_PF["edition"]}'

# A single PF identifier: XX.YY-P optionally with a subcategory number.
_PF_SINGLE = re.compile(r"\b([A-Z]{2}\.[A-Z]{2}-P)(\d+)?\b")
# A PF range: "CT.PO-P1 to P5" / "CT.PO-P1 to CT.PO-P5" / hyphen or en-dash separated.
_ENDASH = "\u2013"  # en-dash, kept out of the source as a literal glyph (ungated-dash gate)
_PF_RANGE = re.compile(
    r"\b([A-Z]{2}\.[A-Z]{2}-P)(\d+)\s*(?:to|through|[-" + _ENDASH + r"])\s*"
    r"([A-Z]{2}\.[A-Z]{2}-P)?P?(\d+)\b"
)


def _check_pf(code: str) -> bool:
    """True if `code` (a category `XX.YY-P` or subcategory `XX.YY-Pn`) exists in PF."""
    return code in _PF_ALL


def check_file(path: Path, rel: str) -> list[str]:
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[str] = []
    for lineno, raw in iter_non_code_lines(text):
        # Ranges first (so their endpoints are not double-reported as singles).
        range_spans: list[tuple[int, int]] = []
        for m in _PF_RANGE.finditer(raw):
            base1, start = m.group(1), int(m.group(2))
            base2, end = m.group(3), int(m.group(4))
            range_spans.append(m.span())
            # Each endpoint is validated against ITS OWN category prefix: a
            # cross-category range (CT.PO-P1 to CM.AW-P5) validates CM.AW-P5, not a
            # reconstructed CT.PO-P5.
            for code in (f"{base1}{start}", f"{base2 or base1}{end}"):
                if not _check_pf(code):
                    findings.append(
                        f"{rel}:{lineno}: '{code}' (from range '{m.group(0)}') is not a valid "
                        f"{_PF_NAME} identifier"
                    )
        for m in _PF_SINGLE.finditer(raw):
            # skip tokens already covered by a range match
            if any(s <= m.start() < e for s, e in range_spans):
                continue
            base, num = m.group(1), m.group(2)
            code = f"{base}{num}" if num else base
            if not _check_pf(code):
                findings.append(
                    f"{rel}:{lineno}: '{code}' is not a valid {_PF_NAME} identifier "
                    f"(the {base} category's subcategories do not include this number)"
                )
    return findings


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Fabricated alignment-citation existence audit.")
    ap.add_argument("paths", nargs="*", default=[str(REPO_ROOT)],
                    help="files or directories to scan (default: the whole repository)")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 on any fabricated code (blocking-gate mode); default is report-only (exit 0)")
    args = ap.parse_args(argv[1:])
    findings: list[str] = []
    for path in iter_markdown_targets(args.paths or [str(REPO_ROOT)]):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel.endswith(EXEMPT_SUFFIXES):
            continue
        findings.extend(check_file(path, rel))
    if findings:
        label = "FAIL" if args.strict else "REPORT"
        print(f"{label}: fabricated alignment citation(s) found ({len(set(findings))}):")
        for f in sorted(set(findings)):
            print(f"  - {f}")
        print(f"\nEach cites an identifier absent from the named framework edition's catalogue. "
              f"Correct to an existing identifier that fits the row.")
        return 1 if args.strict else 0
    print(f"OK: all alignment citations exist in their named framework edition "
          f"(coverage: {_PF_NAME}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
