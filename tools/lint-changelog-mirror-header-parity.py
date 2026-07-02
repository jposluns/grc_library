#!/usr/bin/env python3
"""CHANGELOG detailed-mirror per-PR header-parity audit (gate 59).

The change-tracking discipline keeps two CHANGELOG surfaces in lock-step:
the adopter-facing root ``CHANGELOG.md`` (lead-paragraph summaries) and
the maintainer-grade detailed mirror
``.working/changelog-details/CHANGELOG-detailed.md`` (full structured
entries). Delta check D1 enforces, per commit, that a PR touches BOTH
files; it does NOT check that the two carry the SAME set of per-PR
``## YYYY-MM-DD, Library Version X, PR #N`` headers. That cross-commit
integrity is gate-blind: a later PR's commit can overwrite an earlier
PR's detailed-mirror header in place, orphaning the earlier bodies under
the wrong header (the #388 defect, where #386/#387 were orphaned under
#388 and fixed in #392).

This gate closes that gap: it parses the per-PR header set from each
file and requires them to match, so a lost or duplicated detailed-mirror
header fails the build instead of surfacing only at a later manual sweep.

It also asserts Library-Version ORDERING (the GR-1 extension): entries
are newest-first, so within each file the cutoff-scoped headers'
``Library Version`` values must be STRICTLY DECREASING top-down (the
change-tracking rule's "version numbers across CHANGELOG entries
strictly increase in the order the entries appear" stated for a
reverse-chronological file). Versions compare as integer tuples, never
strings (``2026.06.9`` above ``2026.06.10`` is a violation a string
compare would miss). This is the CHANGELOG version-monotonicity control
the change-tracking rule describes; gate 13 deliberately skips
CHANGELOG.md (no ``Version`` metadata field), so before this extension
the described control did not exist anywhere.

Cutoff-scoped (maintainer decision 2026-07-01). The check
compares only headers for ``PR #N`` with ``N >= CUTOFF_PR``. Three
pre-split-era PRs have a root header with no matching detailed-mirror
header (#268, a handoff PR; #353 and #462), a historical state that
predates this gate and is accepted as an exemption rather than
retroactively reconstructed (the change-tracking rule cautions against
retroactive entries). Scoping from a cutoff forward is false-positive-free
by construction and still delivers the gate's whole purpose: preventing
FUTURE drift. Historical entries are immutable, so no new gap can appear
below the cutoff.

The ordering assertion reuses the same ``CUTOFF_PR`` scope: the only
non-decreasing pairs in either file's history sit in the 2026-06-21
PR #170-#175 window, far below the cutoff, so the scoped assertion is
false-positive-free by construction with no second baseline constant.

Exit codes:
    0   the per-PR header multisets match at or above the cutoff and
        each file's cutoff-scoped Library Versions strictly decrease
    1   one or more headers are missing, extra, or duplicated, or a
        Library Version is out of order (equal or increasing top-down)
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

from lint_common import REPO_ROOT, read_text_safe

# Paths of the two surfaces, relative to the repository root.
ROOT_CHANGELOG_REL = "CHANGELOG.md"
DETAILED_MIRROR_REL = ".working/changelog-details/CHANGELOG-detailed.md"

# Compare only PRs at or above this number. The three pre-cutoff root
# headers with no detailed-mirror counterpart (#268, #353, #462) are an
# accepted historical exemption; see the module docstring.
CUTOFF_PR = 463

# A per-PR entry header, e.g. "## 2026-07-01, Library Version 2026.07.8, PR #520".
HEADER_RE = re.compile(r"^##\s+\d{4}-\d{2}-\d{2},.*\bPR #(\d+)\b")

# The Library Version inside a matched per-PR header. Captured as three
# integer groups so ordering compares numerically (tuple compare), never
# lexically.
VERSION_RE = re.compile(r"\bLibrary Version (\d+)\.(\d+)\.(\d+)\b")


def pr_headers(
    text: str,
) -> list[tuple[int, int, tuple[int, int, int] | None, str]]:
    """Return ordered ``(lineno, pr, version, version_text)`` per header.

    ``version`` is the header's Library Version as an int 3-tuple (for
    numeric comparison), or ``None`` when the matched header carries no
    parseable version (not a current corpus shape; the ordering
    assertion skips such a header rather than crashing).
    ``version_text`` is the version EXACTLY as it appears in the header
    (leading zeros preserved), for failure messages.
    """
    records: list[tuple[int, int, tuple[int, int, int] | None, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        m = HEADER_RE.match(line)
        if not m:
            continue
        n = int(m.group(1))
        if n < CUTOFF_PR:
            continue
        v = VERSION_RE.search(line)
        version = tuple(int(g) for g in v.groups()) if v else None
        version_text = ".".join(v.groups()) if v else ""
        records.append((lineno, n, version, version_text))
    return records


def pr_header_counts(text: str) -> Counter:
    """Return a Counter of PR numbers (>= CUTOFF_PR) appearing in per-PR headers."""
    return Counter(pr for _, pr, _, _ in pr_headers(text))


def ordering_violations(
    records: list[tuple[int, int, tuple[int, int, int] | None, str]],
) -> list[str]:
    """Return human-readable strictly-decreasing violations in file order.

    Entries are newest-first, so each versioned header's Library Version
    must be strictly GREATER than the next versioned header's below it.
    Equal and increasing pairs are reported with distinct wording so
    triage is immediate.
    """
    versioned = [r for r in records if r[2] is not None]
    violations: list[str] = []
    for (a_line, a_pr, a_v, a_s), (b_line, b_pr, b_v, b_s) in zip(
        versioned, versioned[1:]
    ):
        if a_v > b_v:
            continue
        if a_v == b_v:
            violations.append(
                f"line {a_line} (PR #{a_pr}) and line {b_line} (PR #{b_pr}) "
                f"share Library Version {a_s}; each entry must carry its own"
            )
        else:
            violations.append(
                f"line {a_line} (PR #{a_pr}, {a_s}) sits above line {b_line} "
                f"(PR #{b_pr}, {b_s}) but carries the SMALLER version; entries "
                f"are newest-first, so versions must strictly decrease top-down"
            )
    return violations


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="repository root to scan (default: the audited repository)",
    )
    args = parser.parse_args(argv)

    root_changelog = args.root / ROOT_CHANGELOG_REL
    detailed_mirror = args.root / DETAILED_MIRROR_REL
    root_records = pr_headers(read_text_safe(root_changelog) or "")
    mirror_records = pr_headers(read_text_safe(detailed_mirror) or "")
    root_counts = Counter(pr for _, pr, _, _ in root_records)
    mirror_counts = Counter(pr for _, pr, _, _ in mirror_records)

    missing = sorted(set(root_counts) - set(mirror_counts))
    extra = sorted(set(mirror_counts) - set(root_counts))
    dup_root = sorted(n for n, c in root_counts.items() if c > 1)
    dup_mirror = sorted(n for n, c in mirror_counts.items() if c > 1)
    order_root = ordering_violations(root_records)
    order_mirror = ordering_violations(mirror_records)

    problems = missing or extra or dup_root or dup_mirror or order_root or order_mirror
    if not problems:
        shared = len(set(root_counts))
        print(
            f"OK: root and detailed-mirror CHANGELOG per-PR headers match "
            f"for all {shared} PR(s) at or above #{CUTOFF_PR}, and each "
            f"file's Library Versions strictly decrease top-down."
        )
        return 0

    if missing:
        print(
            "FAIL: PR header(s) present in root CHANGELOG.md but MISSING from the "
            f"detailed mirror (>= #{CUTOFF_PR}): "
            + ", ".join(f"#{n}" for n in missing)
        )
    if extra:
        print(
            "FAIL: PR header(s) present in the detailed mirror but MISSING from root "
            f"CHANGELOG.md (>= #{CUTOFF_PR}): "
            + ", ".join(f"#{n}" for n in extra)
        )
    if dup_root:
        print(
            "FAIL: PR header(s) appearing more than once in root CHANGELOG.md "
            f"(>= #{CUTOFF_PR}): " + ", ".join(f"#{n}" for n in dup_root)
        )
    if dup_mirror:
        print(
            "FAIL: PR header(s) appearing more than once in the detailed mirror "
            f"(>= #{CUTOFF_PR}): " + ", ".join(f"#{n}" for n in dup_mirror)
        )
    if order_root:
        print(
            f"FAIL: root CHANGELOG.md Library Version ordering violated "
            f"(>= #{CUTOFF_PR}):"
        )
        for v in order_root:
            print(f"  {v}")
    if order_mirror:
        print(
            f"FAIL: detailed-mirror Library Version ordering violated "
            f"(>= #{CUTOFF_PR}):"
        )
        for v in order_mirror:
            print(f"  {v}")
    print(
        "\nThe root CHANGELOG.md and its detailed mirror "
        "(.working/changelog-details/CHANGELOG-detailed.md) must carry the same "
        "per-PR header set, with each file's Library Versions strictly "
        "decreasing top-down. Add the missing entry, reconcile the duplicated / "
        "orphaned header, or re-version the out-of-order entry so the two "
        "surfaces stay in lock-step."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
