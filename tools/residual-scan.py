#!/usr/bin/env python3
"""Post-fix residual scan: find every carrier of a corrected token, full lines, no truncation.

The GR-12 aid (TODO 3.15; guardrail review 2026-07-02). When a fix corrects a token
(a count, a title, a spelling, a value), the recurring miss is the SIBLING carrier:
the named occurrence is fixed while another carrier of the same token survives in the
same file or a parallel surface. The narrow-scan class recurred well past the GR-P3
third-occurrence bar (the #443 bare-token lesson; four fix-named-miss-sibling
instances in the #573/#574 window alone), so the deterministic scan step is tooling,
not a checklist line.

Usage:
    python3 tools/residual-scan.py TOKEN [TOKEN ...]
    python3 tools/residual-scan.py --substring TOKEN ...
    python3 tools/residual-scan.py --regex PATTERN ...
    python3 tools/residual-scan.py --all TOKEN ...

Behaviour:
  - Scans every text surface in the working tree (markdown, python, shell,
    yaml, cff, toml, txt, json; the .git tree excluded; no git-tracked filter,
    so untracked local files are scanned too, erring toward recall), never an
    enumerated input set:
    the completion-verification lesson is that an input-set scan self-corroborates
    a file-discovery omission.
  - Matches on word boundaries by default (the bare-token discipline: a
    phrasing-specific grep misses word-order variants); --substring disables the
    boundary, --regex treats each argument as a raw regular expression, and the
    two flags are mutually exclusive (exit 2 when combined). A token whose edge
    character is not a word character (a leading hyphen, a flag like --all)
    cannot match under the boundary lookarounds; use --substring for those.
  - Prints every hit as path:line-number followed by the FULL line, untruncated.
    The Sweep-82 lesson is binding: a hit is READ IN FULL before it is triaged;
    never classify a hit from a truncated excerpt or from the match alone.
  - Labels each hit LIVE, FROZEN-RECORD (any dated per-run file DIRECTLY under
    a .working activity directory, depth two, any year: frozen-state archives
    quoting findings verbatim; a deeper-nested dated file conservatively
    labels LIVE), or LEDGER (append-only history surfaces: CHANGELOG.md,
    its detailed mirror, DONE.md, the improvement-log and hallucination-metrics
    registers, and every per-activity history.md, where PRE-EXISTING entries legitimately
    quote old values; a hit in a line this PR ADDS is still live in substance).
    FROZEN-RECORD hits are suppressed unless --all is given; LEDGER hits are
    always shown because the tool cannot tell an old entry from a new one.
  - Exit code 1 when any LIVE hit is found, else 0, so the scan chains as a
    completion check: fix, then `python3 tools/residual-scan.py "old token"`
    must exit 0 (after the LEDGER hits are read and judged historical).

This is an aid, not a numbered audit gate: it has no fixed token vocabulary to
gate on (the tokens are per-fix), so it cannot run unattended in CI. The
authoritative gates still run in CI; this tool makes the close-out checklist's
bare-token and full-file-grep guards a deterministic step instead of a manual one.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

TEXT_SUFFIXES = {".md", ".py", ".sh", ".yml", ".yaml", ".cff", ".toml", ".txt", ".json"}

EXCLUDED_DIRS = {".git", "node_modules", "__pycache__"}

# Dated per-run archive: any .working/<activity>/<YYYY-...> file, any year.
FROZEN_RECORD_RE = re.compile(r"^\.working/[^/]+/\d{4}-")

# Per-activity append-only history tables, plus the top-level append-only ledgers.
LEDGER_RE = re.compile(r"^\.working/[^/]+/history\.md$")

LEDGER_PATHS = (
    "CHANGELOG.md",
    ".working/changelog-details/CHANGELOG-detailed.md",
    ".working/DONE.md",
    ".working/improvement-log.md",
    ".working/hallucination-metrics.md",
)


def classify(rel: str) -> str:
    if LEDGER_RE.match(rel) or rel in LEDGER_PATHS:
        return "LEDGER"
    if FROZEN_RECORD_RE.match(rel):
        return "FROZEN-RECORD"
    return "LIVE"


def iter_files() -> list[Path]:
    files = []
    for path in sorted(REPO_ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        files.append(path)
    return files


def build_patterns(tokens: list[str], substring: bool, regex: bool) -> list[re.Pattern]:
    patterns = []
    for token in tokens:
        if not token.strip():
            print("residual-scan: empty token rejected", file=sys.stderr)
            raise SystemExit(2)
        if regex:
            try:
                patterns.append(re.compile(token))
            except re.error as exc:
                print(f"residual-scan: invalid regex {token!r}: {exc}", file=sys.stderr)
                raise SystemExit(2)
        elif substring:
            patterns.append(re.compile(re.escape(token)))
        else:
            patterns.append(re.compile(r"(?<!\w)" + re.escape(token) + r"(?!\w)"))
    return patterns


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("tokens", nargs="+", help="corrected token(s) to hunt residuals of")
    parser.add_argument("--substring", action="store_true", help="match anywhere, no word boundary")
    parser.add_argument("--regex", action="store_true", help="treat tokens as raw regular expressions")
    parser.add_argument("--all", action="store_true", help="also show FROZEN-RECORD hits")
    args = parser.parse_args()

    if args.substring and args.regex:
        print("residual-scan: --substring and --regex are mutually exclusive", file=sys.stderr)
        return 2

    patterns = build_patterns(args.tokens, args.substring, args.regex)
    counts = {"LIVE": 0, "LEDGER": 0, "FROZEN-RECORD": 0}

    for path in iter_files():
        rel = path.relative_to(REPO_ROOT).as_posix()
        label = classify(rel)
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as exc:
            print(f"WARN unreadable {rel}: {exc}", file=sys.stderr)
            continue
        for lineno, line in enumerate(lines, 1):
            if any(p.search(line) for p in patterns):
                counts[label] += 1
                if label == "FROZEN-RECORD" and not args.all:
                    continue
                print(f"[{label}] {rel}:{lineno}: {line}")

    suppressed = counts["FROZEN-RECORD"] if not args.all else 0
    print(
        f"\nresidual-scan: {counts['LIVE']} LIVE, {counts['LEDGER']} LEDGER, "
        f"{counts['FROZEN-RECORD']} FROZEN-RECORD hit(s)"
        + (f" ({suppressed} suppressed; use --all to show)" if suppressed else "")
    )
    if counts["LIVE"]:
        print("residual-scan: LIVE residual(s) remain; read each full line above before triage.")
        return 1
    print("residual-scan: no LIVE residuals; read any LEDGER hits to confirm they are historical entries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
