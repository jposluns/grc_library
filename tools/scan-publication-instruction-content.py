#!/usr/bin/env python3
"""Instruction-content scan over reference-base publication extracts.

WHAT THIS IS (and is NOT). An advisory dev-AID feeding the /screen-publications
skill (TODO 2.11), not an audit gate. It always exits 0 after printing its report
(2 only on internal or usage error). It performs the MECHANICAL half of the
skill's instruction-content screen: a pattern scan over publication text extracts
for the shapes prompt-injection and instruction-smuggling payloads take (OWASP
LLM01 prompt injection; LLM05 improper output handling), plus encoding anomalies
that can hide them. A hit is a candidate for the screening judge to read in
context, never a verdict: legitimate security literature QUOTES injection strings
when describing attacks, so quoted-example hits are expected and are cleared by
the human-or-judge read, not by this scan. A clean scan is one input to the
screening verdict, not the verdict: semantic poisoning (biased framing, false
claims, misattributed standards content) has no lexical shape and is the skill's
step-4 corroboration read.

Scope: the ``publications/`` bucket's ``*--full-text.md`` extracts in the sibling
``grc_library_ref`` checkout by default; ``--files`` scans named files instead
(any text file). ``--all-buckets`` widens to every extract in the reference base
(useful before trusting a new ingest in any bucket).

Pattern classes (each finding names its class):
  imperative-to-assistant   second-person imperatives addressed to an AI/assistant
  override-instruction      ignore/disregard/forget prior-instruction shapes
  role-reassignment         "you are now" / "act as" / system-prompt reassignment
  exfiltration-hook         send/post/exfiltrate-to-URL imperatives
  tool-invocation           tool-call / command-execution looking directives
  hidden-text               zero-width characters, HTML comments, suspicious
                            control characters in prose
  encoded-blob              long base64-looking runs that could carry a payload

Usage:
    python3 tools/scan-publication-instruction-content.py [--ref-base PATH]
    python3 tools/scan-publication-instruction-content.py --files F [F ...]
    python3 tools/scan-publication-instruction-content.py --all-buckets

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REF_BASE = REPO_ROOT.parent / "grc_library_ref"

# Each class: (name, compiled pattern). Patterns are deliberately recall-oriented;
# the screening judge clears quoted-example hits in context.
PATTERN_CLASSES: list[tuple[str, re.Pattern]] = [
    ("imperative-to-assistant", re.compile(
        r"\b(?:you\s+(?:must|should|will)\s+(?:now\s+)?(?:respond|reply|answer|"
        r"output|write|say|translate|summarize)|as\s+an\s+ai\b[^.\n]{0,60}"
        r"\b(?:you|your)\b)", re.IGNORECASE)),
    ("override-instruction", re.compile(
        r"\b(?:ignore|disregard|forget|override)\s+(?:all\s+|any\s+|your\s+)?"
        r"(?:previous|prior|above|earlier|preceding|system)\s+"
        r"(?:instructions?|prompts?|rules?|context|messages?)", re.IGNORECASE)),
    ("role-reassignment", re.compile(
        r"\b(?:you\s+are\s+now\s+(?:a|an|the)\b|act\s+as\s+(?:a|an|the)\s+"
        r"(?:unrestricted|unfiltered|jailbroken|developer)|new\s+system\s+prompt|"
        r"your\s+new\s+(?:instructions?|persona|role)\s+(?:is|are))",
        re.IGNORECASE)),
    ("exfiltration-hook", re.compile(
        r"\b(?:send|post|transmit|exfiltrate|forward)\s+(?:this|the|all|your)\s+"
        r"[^.\n]{0,40}\bto\s+https?://", re.IGNORECASE)),
    ("tool-invocation", re.compile(
        r"(?:^|\n)\s*(?:<tool_call>|<function_call|\{\s*\"tool\"\s*:|"
        r"run\s+the\s+following\s+command\s+without)", re.IGNORECASE)),
    ("hidden-text", re.compile(
        "[\\u200b\\u200c\\u200d\\u2060\\ufeff\\u00ad]|<!--[^>]{40,}-->")),
    ("encoded-blob", re.compile(r"\b[A-Za-z0-9+/]{120,}={0,2}\b")),
]


def scan_text(text: str) -> list[tuple[str, int, str]]:
    findings = []
    for name, pat in PATTERN_CLASSES:
        for m in pat.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            snippet = m.group(0)[:80].replace("\n", " ")
            findings.append((name, line_no, snippet))
    return findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ref-base", type=Path, default=DEFAULT_REF_BASE)
    ap.add_argument("--files", nargs="+", type=Path, default=None,
                    help="Scan these files instead of the publications bucket.")
    ap.add_argument("--all-buckets", action="store_true",
                    help="Scan every --full-text.md in the reference base.")
    args = ap.parse_args(argv)

    # Adopter graceful-degradation (TODO 3.91): no explicit --files and the default
    # ref-base (no --ref-base override) with no grc_library_ref dir -> no-op exit 0, so
    # a bare adopter clone runs this maintainer-only advisory green rather than crashing.
    # An explicit --files or --ref-base still proceeds (and errors below on a bad path).
    if (not args.files and args.ref_base == DEFAULT_REF_BASE
            and not args.ref_base.is_dir()):
        print("scan-publication-instruction-content: grc_library_ref not present; no-op "
              "(publication-scan is a maintainer-only advisory, nothing to report).")
        return 0

    try:
        if args.files:
            targets = list(args.files)
        else:
            ref = args.ref_base.resolve()
            if not ref.is_dir():
                raise RuntimeError(f"reference base not found: {ref}")
            root = ref if args.all_buckets else ref / "publications"
            targets = sorted(p for p in root.rglob("*--full-text.md")
                             if ".superseded" not in p.parts)
        if not targets:
            raise RuntimeError("no scan targets found")
    except (RuntimeError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    total = 0
    clean = 0
    print(f"# Instruction-content scan ({len(targets)} extract(s))\n")
    for path in targets:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"- UNREADABLE {path}: {exc}")
            continue
        findings = scan_text(text)
        if not findings:
            clean += 1
            continue
        total += len(findings)
        print(f"## {path.name} ({len(findings)} candidate(s))")
        for name, line_no, snippet in findings[:20]:
            print(f"- [{name}] line {line_no}: {snippet}")
        if len(findings) > 20:
            print(f"- ... plus {len(findings) - 20} more (count is complete)")
        print()
    flagged = len(targets) - clean
    print(f"Summary: {clean} clean extract(s), {total} candidate finding(s) "
          f"across {flagged} flagged extract(s). Candidates "
          f"are judge-reads, not verdicts: quoted attack examples in security "
          f"literature are expected hits.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
