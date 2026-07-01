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

Exit codes:
    0   the per-PR header multisets match at or above the cutoff
    1   one or more headers are missing, extra, or duplicated
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


def pr_header_counts(text: str) -> Counter:
    """Return a Counter of PR numbers (>= CUTOFF_PR) appearing in per-PR headers."""
    counts: Counter = Counter()
    for line in text.splitlines():
        m = HEADER_RE.match(line)
        if m:
            n = int(m.group(1))
            if n >= CUTOFF_PR:
                counts[n] += 1
    return counts


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
    root_counts = pr_header_counts(read_text_safe(root_changelog) or "")
    mirror_counts = pr_header_counts(read_text_safe(detailed_mirror) or "")

    missing = sorted(set(root_counts) - set(mirror_counts))
    extra = sorted(set(mirror_counts) - set(root_counts))
    dup_root = sorted(n for n, c in root_counts.items() if c > 1)
    dup_mirror = sorted(n for n, c in mirror_counts.items() if c > 1)

    problems = missing or extra or dup_root or dup_mirror
    if not problems:
        shared = len(set(root_counts))
        print(
            f"OK: root and detailed-mirror CHANGELOG per-PR headers match "
            f"for all {shared} PR(s) at or above #{CUTOFF_PR}."
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
    print(
        "\nThe root CHANGELOG.md and its detailed mirror "
        "(.working/changelog-details/CHANGELOG-detailed.md) must carry the same "
        "per-PR header set. Add the missing entry (or reconcile the duplicated / "
        "orphaned header) so the two surfaces stay in lock-step."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
