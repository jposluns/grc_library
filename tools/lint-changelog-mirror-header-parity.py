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

Dynamic floor (current-week model, 2026-07-08). ``CUTOFF_PR`` is now a
FLOOR, not the comparison boundary: the effective cutoff is
``max(CUTOFF_PR, oldest PR still present in the in-repo detailed
mirror)`` (see ``effective_cutoff``). Under the current-week model the
mirror keeps only the current week's entries in-repo and sweeps
completed weeks to the ``grc_library_scratch`` archive, while the root
``CHANGELOG.md`` keeps every entry; a swept (now scratch-only) entry is
therefore correctly out of parity scope rather than flagged as missing.
Before any sweep the mirror's oldest PR is far below ``CUTOFF_PR`` so the
effective cutoff is ``CUTOFF_PR`` and behaviour is unchanged. A genuine
in-window miss (a root header at or above the mirror's floor with no
mirror counterpart) still fails.

Boundary limitation (honest note). Because the floor IS the mirror's own
oldest surviving PR, an orphan that drops the floor-DEFINING oldest
in-repo entry moves the floor up past it, so that entry's still-present
root counterpart silently falls out of scope and this gate does not
catch it (whereas the earlier form of this gate, with its cutoff pinned
at the constant 463, would). This is an
inherent limit of moving history out of the in-repo mirror: from root +
mirror content alone, "the oldest kept entry was dropped" is
indistinguishable from "that entry was legitimately swept to scratch",
so no purely-content check can tell them apart. Parity is therefore
asserted only for the entries the in-repo mirror still holds; historical
parity moves to git history and to the sweep tool's own guarantees. The
compensating controls: the sweep tool
(``tools/sweep-working-records-to-scratch.py``) partitions
deterministically by entry DATE and re-parses the pruned mirror to
confirm its entry set is EXACTLY the kept current-week set before it
finishes, and git history retains every entry regardless.

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

# The compact root-entry header (the TODO 3.16 root-reformat), with or
# without the stage-3b ``- summary`` tail:
# ``**2026-07-08 | 2026.07.201 | PR #713**`` or the same followed by
# `` - <summary>``. Groups: (2,3,4) the version triple, (5) the PR.
COMPACT_HEADER_RE = re.compile(
    r"^\*\*(\d{4}-\d{2}-\d{2}) \| (\d+)\.(\d+)\.(\d+) \| PR #(\d+)\*\*(?: - .*)?$")

# The Library Version inside a matched per-PR header. Captured as three
# integer groups so ordering compares numerically (tuple compare), never
# lexically.
VERSION_RE = re.compile(r"\bLibrary Version (\d+)\.(\d+)\.(\d+)\b")


def pr_headers(
    text: str,
    cutoff: int = CUTOFF_PR,
) -> list[tuple[int, int, tuple[int, int, int] | None, str]]:
    """Return ordered ``(lineno, pr, version, version_text)`` per header.

    Only headers with ``PR #N`` where ``N >= cutoff`` are returned;
    ``cutoff`` defaults to ``CUTOFF_PR`` but ``main`` passes a
    dynamically-computed effective cutoff (see ``effective_cutoff``).

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
        if m:
            n = int(m.group(1))
            if n < cutoff:
                continue
            v = VERSION_RE.search(line)
            version = tuple(int(g) for g in v.groups()) if v else None
            version_text = ".".join(v.groups()) if v else ""
            records.append((lineno, n, version, version_text))
            continue
        c = COMPACT_HEADER_RE.match(line)
        if not c:
            continue
        n = int(c.group(5))
        if n < cutoff:
            continue
        version = tuple(int(c.group(i)) for i in (2, 3, 4))
        records.append((lineno, n, version,
                        f"{c.group(2)}.{c.group(3)}.{c.group(4)}"))
    return records


def effective_cutoff(mirror_text: str) -> int:
    """The parity-comparison floor: ``max(CUTOFF_PR, oldest PR in the mirror)``.

    The current-week model (2026-07-08) keeps only the current week's
    entries in the in-repo detailed mirror; completed weeks are swept to
    the scratch archive. The root ``CHANGELOG.md`` keeps EVERY entry. So
    the set of PRs that still have an in-repo mirror counterpart is
    exactly ``PR #N >= (oldest PR still in the mirror)``. Scoping the
    parity comparison to that floor means a swept-out (now scratch-only)
    entry is correctly out of scope rather than flagged as missing from
    the mirror, while a genuinely dropped or orphaned in-window header
    still fails.

    The floor never drops below ``CUTOFF_PR`` (which carries the
    pre-split historical exemptions #268/#353/#462). Before any sweep the
    mirror's oldest PR is far below ``CUTOFF_PR``, so the effective cutoff
    is ``CUTOFF_PR`` and behaviour is identical to the pre-2026-07-08
    fixed-constant gate.
    """
    mirror_prs = [pr for _, pr, _, _ in pr_headers(mirror_text, cutoff=0)]
    if not mirror_prs:
        return CUTOFF_PR
    return max(CUTOFF_PR, min(mirror_prs))


def pr_header_counts(text: str, cutoff: int = CUTOFF_PR) -> Counter:
    """Return a Counter of PR numbers (>= cutoff) appearing in per-PR headers."""
    return Counter(pr for _, pr, _, _ in pr_headers(text, cutoff=cutoff))


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
    mirror_text = read_text_safe(detailed_mirror) or ""
    cutoff = effective_cutoff(mirror_text)
    root_records = pr_headers(read_text_safe(root_changelog) or "", cutoff=cutoff)
    mirror_records = pr_headers(mirror_text, cutoff=cutoff)
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
            f"for all {shared} PR(s) at or above #{cutoff}, and each "
            f"file's Library Versions strictly decrease top-down."
        )
        return 0

    if missing:
        print(
            "FAIL: PR header(s) present in root CHANGELOG.md but MISSING from the "
            f"detailed mirror (>= #{cutoff}): "
            + ", ".join(f"#{n}" for n in missing)
        )
    if extra:
        print(
            "FAIL: PR header(s) present in the detailed mirror but MISSING from root "
            f"CHANGELOG.md (>= #{cutoff}): "
            + ", ".join(f"#{n}" for n in extra)
        )
    if dup_root:
        print(
            "FAIL: PR header(s) appearing more than once in root CHANGELOG.md "
            f"(>= #{cutoff}): " + ", ".join(f"#{n}" for n in dup_root)
        )
    if dup_mirror:
        print(
            "FAIL: PR header(s) appearing more than once in the detailed mirror "
            f"(>= #{cutoff}): " + ", ".join(f"#{n}" for n in dup_mirror)
        )
    if order_root:
        print(
            f"FAIL: root CHANGELOG.md Library Version ordering violated "
            f"(>= #{cutoff}):"
        )
        for v in order_root:
            print(f"  {v}")
    if order_mirror:
        print(
            f"FAIL: detailed-mirror Library Version ordering violated "
            f"(>= #{cutoff}):"
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
