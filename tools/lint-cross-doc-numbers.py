#!/usr/bin/env python3
"""Detect cross-document numerical drift on canonical-term thresholds.

Library documents repeatedly mention certain numeric thresholds. When the
same threshold appears with different values in different documents, the
inconsistency is a real defect that adopters will encounter.

This linter is deliberately conservative: it focuses on a curated set of
canonical terms with well-defined numeric values, extracted via specific
regex. False positives are minimized by requiring the term to appear
close to the number on the same line.

Terms currently tracked (see TERM_PATTERNS for the live set):

  - Privileged-role activation maximum (in minutes or hours; PAM-authoritative)
  - GDPR breach-notification window (in hours)

The privileged-role-activation-maximum pattern binds the authoritative
PAM Section 4.2 value to the self-contained portable authentication
guardrail. It matches both the PAM term-before-value form and the
guardrail value-before-term form. This term is intentionally scanned
inside fenced blocks because the guardrail renders its normative timeout
row in a code fence.

The dormant P1/P2/P3 acknowledgement scaffold patterns (added narrow per
the Phase 23.26 false-positive analysis, matching 0 documents and kept
as forward scaffolding) were RETIRED per the deep-assessment r3
DA-gate25-scaffold finding: they matched no corpus content, so they
added no protection while implying coverage the gate did not provide.
The empirical rationale for NOT broadening SLA-dimension patterns to
resolution / MTTR / convene / notification times still holds (each SLA
dimension legitimately carries different per-Pn values across the
corpus), so no replacement pattern is introduced; the gate stays active
on the GDPR-breach-notification term below.

The GDPR-breach-notification pattern was added in Phase 23.35 after
empirical confirmation that 8+ documents reference the statutory
72-hour deadline and all currently agree on the value. The regex
requires GDPR (or UK GDPR) to appear before an N-hours fragment on the
same line, capturing the number. Any divergent value introduced by a
future edit will produce a finding.

RTO, RPO, retention periods, P4 acknowledgement, NIS 2 reporting
windows, and DORA reporting windows are not curated. They are either
context-dependent (RTO/RPO vary by tier and adopter), have multiple
legitimate sub-deadlines that need per-deadline patterns (NIS 2 has
24-hour early-warning, 72-hour report, 1-month final), or appear too
few times in the corpus to justify a curated pattern (DORA 4-hour
appears in one document).

TERM_PATTERNS currently has two live entries. The activation-maximum term
accepts minute/hour units; the GDPR-breach-notification term's unit capture
group is always "hour". The day/business-day rows of UNIT_TO_MINUTES remain
forward scaffolding for a future term.

Usage:
    python3 tools/lint-cross-doc-numbers.py

Exit codes:
    0   no divergence detected (each tracked term has at most one
        canonical value across the scanned corpus)
    1   divergence detected: the same term carries different values
        across documents
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import guard_explicit_paths_cwd, REPO_ROOT, iter_markdown_targets  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

DEFAULT_PATHS = [str(REPO_ROOT)]

EXEMPT_FILES = {
    # The CHANGELOG quotes specific numeric thresholds when describing
    # the linter's term set; treating it as a target would produce
    # spurious "divergent value" findings against its own historical
    # narrative.
    "CHANGELOG.md",
}


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_cross_doc_numbers  # the pack-owned engine (source of record)
    return gate_lint_cross_doc_numbers


def scan(path: Path) -> dict[str, set[tuple[int, str]]]:
    """Thin shim delegating to the pack engine's pure per-file check.

    Kept in the wrapper as a module-global because the scan-scope regression
    test patches ``mod.scan`` and runs ``main``; the tracked-term regexes and the
    normalization logic live in the engine.
    """
    return _engine().scan(path)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect cross-document numerical drift on canonical-term thresholds."
    )
    parser.add_argument("paths", nargs="*", default=None)
    args = parser.parse_args(argv[1:])
    # 3b48: explicit paths are refused when missing or outside this tree, else normalized.
    args.paths = guard_explicit_paths_cwd(args.paths, repo_root=REPO_ROOT) if args.paths else DEFAULT_PATHS
    targets = iter_markdown_targets(args.paths, exempt_files=EXEMPT_FILES)
    # term -> {normalised_value -> [(doc, raw_text)]}
    aggregate: dict[str, dict[int, list[tuple[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for t in targets:
        rel = t.relative_to(REPO_ROOT).as_posix() if t.is_relative_to(REPO_ROOT) else str(t)
        per_file = scan(t)
        for term, value_set in per_file.items():
            for norm, raw in value_set:
                aggregate[term][norm].append((rel, raw))
    divergent: list[tuple[str, dict[int, list[tuple[str, str]]]]] = []
    for term, values in aggregate.items():
        if len(values) > 1:
            divergent.append((term, values))
    if not divergent:
        terms_count = len(aggregate)
        print(f"OK: no cross-document numerical drift detected ({terms_count} tracked term(s); scanned {len(targets)} files).")
        return 0
    for term, values in divergent:
        print(f"=== {term} ===")
        for norm, occurrences in sorted(values.items()):
            print(f"  {norm} minutes ({occurrences[0][1]}): {len(occurrences)} occurrence(s)")
            for doc, raw in occurrences[:5]:
                print(f"    - {doc}: {raw}")
            if len(occurrences) > 5:
                print(f"    ...and {len(occurrences) - 5} more")
    print(f"\nFAIL: {len(divergent)} term(s) with divergent values across documents.")
    print(
        "The same canonical term carries different numeric values in different "
        "documents. Reconcile to a single canonical value, or document the "
        "reason for variance per scope."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
