#!/usr/bin/env python3
"""CHANGELOG detailed-mirror per-PR header-parity audit (gate 59).

The change-tracking discipline keeps two CHANGELOG surfaces in lock-step:
the adopter-facing root ``CHANGELOG.md`` (compact one-line ``date | version | PR`` entries) and
the maintainer-grade detailed mirror (full structured entries, now
resolved from the private-sibling working-state store). Delta check D1
enforces, per commit, that a PR touches the root ``CHANGELOG.md`` (before
PR #1235 it required BOTH files; the detailed mirror has since moved to the
private-sibling working-state store, cross-repo and outside the public
diff, so D1 no longer requires it); it does NOT check that the two carry
the SAME set of per-PR
entry headers (matched in BOTH the compact ``**date | version | PR #N**``
form and the legacy ``## YYYY-MM-DD, Library Version X, PR #N`` form). That cross-commit
integrity is gate-blind: a later PR's commit can overwrite an earlier
PR's detailed-mirror header in place, orphaning the earlier bodies under
the wrong header (the #388 defect, where #386/#387 were orphaned under
#388 and fixed in #392).

This gate closes that gap: it parses the per-PR header set from each
file and requires them to match, so a lost or duplicated detailed-mirror
header fails the build instead of surfacing only at a later manual sweep.

It also asserts CROSS-FILE VERSION AGREEMENT (added in PR #1158): a PR present in
BOTH files must carry the SAME ``Library Version`` in each. Set parity plus
per-file monotonicity left this gate-blind, because two files can each be
independently monotonic while disagreeing on one shared PR's version: PR #1155
shipped ``2026.07.642`` (root ``CHANGELOG.md`` and ``README.md`` at its merge
commit) while the detailed mirror recorded ``2026.07.641``, a version never
shipped at all, and the gate passed. A pair is SKIPPED when either side's
version does not parse, matching the ordering assertion's existing tolerance,
and a PR duplicated within one file is already caught by the duplicate check
rather than by this join.

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
parity moves to git history and to the private-sibling archive. The
compensating controls: the detailed mirror now lives in the private
sibling (``grc_library_private/.working/``), its completed weeks are
archived within that private repository (``grc_library_private/changelog-archive/``),
and git history retains every entry regardless. (The former in-public-repo
sweep script was retired with the working-state move to the private sibling.)

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

from lint_common import REPO_ROOT, read_text_safe, resolve_working

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


def version_mismatches(
    root_records: list[tuple[int, int, tuple[int, int, int] | None, str]],
    mirror_records: list[tuple[int, int, tuple[int, int, int] | None, str]],
) -> list[tuple[int, str, str]]:
    """PRs present in BOTH files whose Library Versions DIFFER.

    Returns ``(pr, root_version_text, mirror_version_text)`` triples, ordered by
    PR. The gate previously checked set parity of PR numbers and strict
    monotonicity WITHIN each file, but never that a PR present in both carried
    the SAME version in each, so a mirror could record a version that was never
    shipped while both files stayed independently monotonic and their PR sets
    matched (PR #1155: root and README both said 2026.07.642, the mirror said
    2026.07.641).

    Two deliberate exclusions:

    - A record whose version did not parse carries ``None``, which the caller
      already tolerates for the ordering assertion; such a pair is SKIPPED here
      too rather than reported, so this check cannot start failing on a shape the
      rest of the gate accepts.
    - A PR appearing MORE THAN ONCE in either file is already a failure via the
      existing duplicate checks, so this join assumes at most one record per PR
      per file and reads the FIRST if that assumption is ever violated. It
      therefore adds no new policy for duplicates and cannot mask them: the
      duplicate check fires independently in the same run.
    """
    root_by_pr: dict[int, tuple[tuple[int, int, int] | None, str]] = {}
    for _lineno, pr, version, version_text in root_records:
        root_by_pr.setdefault(pr, (version, version_text))
    mismatches: list[tuple[int, str, str]] = []
    seen: set[int] = set()
    for _lineno, pr, version, version_text in mirror_records:
        if pr in seen or pr not in root_by_pr:
            continue
        seen.add(pr)
        root_version, root_text = root_by_pr[pr]
        if root_version is None or version is None:
            continue
        if root_version != version:
            mismatches.append((pr, root_text, version_text))
    return sorted(mismatches)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="repository root to scan (default: the audited repository, whose "
             "detailed mirror resolves via lint_common.resolve_working)",
    )
    args = parser.parse_args(argv)

    if args.root is not None:
        # EXPLICIT --root stays verbatim: the regression fixtures build a
        # synthetic tree with its own .working/changelog-details/, read as given.
        root_changelog = args.root / ROOT_CHANGELOG_REL
        detailed_mirror = args.root / DETAILED_MIRROR_REL
    else:
        root_changelog = REPO_ROOT / ROOT_CHANGELOG_REL
        resolved = resolve_working("changelog-details/CHANGELOG-detailed.md")
        if resolved is None:
            # The detailed mirror is maintainer-only working state. Once
            # `.working/` moves to grc_library_private it is absent in public CI
            # and adopter clones, so the gate no-ops there; on the maintainer's
            # machine the private sibling supplies it and per-PR header parity,
            # version agreement, and ordering are all enforced.
            print(
                "OK: the detailed CHANGELOG mirror is not present "
                "(maintainer-only working state; skipping the header-parity "
                "audit in public CI / adopter clone)."
            )
            return 0
        detailed_mirror = resolved

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
    version_diff = version_mismatches(root_records, mirror_records)

    problems = (missing or extra or dup_root or dup_mirror or order_root
                or order_mirror or version_diff)
    if not problems:
        shared = len(set(root_counts))
        print(
            f"OK: root and detailed-mirror CHANGELOG per-PR headers match "
            f"for all {shared} PR(s) at or above #{cutoff}, each "
            f"file's Library Versions strictly decrease top-down, and every "
            f"shared PR carries the SAME Library Version in both files."
        )
        return 0

    if version_diff:
        print(
            "FAIL: PR(s) present in BOTH files with DIFFERENT Library Versions "
            "(the mirror and the root must agree; the shipped version is the one "
            "in README.md at that PR's merge commit): "
            + ", ".join(
                f"#{pr} root={root_text} mirror={mirror_text}"
                for pr, root_text, mirror_text in version_diff
            )
        )
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
        "\nThe root CHANGELOG.md and its maintainer-grade detailed mirror "
        "must carry the same "
        "per-PR header set, with each file's Library Versions strictly "
        "decreasing top-down. Add the missing entry, reconcile the duplicated / "
        "orphaned header, or re-version the out-of-order entry so the two "
        "surfaces stay in lock-step."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
