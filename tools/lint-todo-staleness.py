#!/usr/bin/env python3
"""TODO staleness audit (gate 45).

Catches the recurring TODO drift patterns that have surfaced across
four consecutive validation sweeps (Sweep 10 iter 2, iter 3 close-out,
iter 3 catch-back, Sweep 11 iter 1). The convention amendment in
PR #127 reframed the "Library version at HEAD" snapshot as
"as-of-last-refresh" with explicit drift-is-expected wording (the
version-snapshot field is intentionally allowed to drift). This gate
catches the two harder-to-tolerate drift shapes that remain:

1. **Queued-PR-already-merged**: TODO.md mentions `Next, PR #N` or
   `queued PR #N` for a PR that has actually merged. This breaks the
   resume experience because the maintainer reads "PR #N is next"
   when it has already shipped.

2. **Sweep-cursor-behind-history**: TODO.md's "Last validation sweep"
   line references Sweep N iteration M, but
   `.working/validate-sweeps/history.md` contains a more recent sweep
   iteration row. This breaks the resume experience because the
   maintainer reads a sweep cursor that has been superseded.

The gate does NOT enforce the version-snapshot field's currency. Per
the PR #127 convention amendment, that field is intentionally allowed
to drift as PRs land between session-pause and resume.

The gate is a regular corpus audit gate (runs on every audit cycle,
not just at PR time). This catches drift at audit-time before any
push, so the maintainer can refresh TODO before merging the next PR.

Scope: scans TODO.md by default. Other files adopting the convention
should be added to TARGET_FILES.

Exit codes:
    0 - All checked patterns are current.
    1 - At least one stale pattern detected.
    2 - Invocation or environment error (git, file read failure).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET_FILES: list[str] = [
    "TODO.md",
]
SWEEP_HISTORY_PATH = ".working/validate-sweeps/history.md"

# Queued-PR patterns. Match `Next` / `queued` / `pending` immediately
# adjacent to `PR #<n>`, where "immediately adjacent" means only
# whitespace, commas, colons, dashes, or em-dashes between the marker
# word and the PR ref. The earlier 80-character window produced false
# positives on lines where the queued PR was a placeholder (`PR #N`)
# and the sentence later referenced a real merged PR number in a
# parenthetical historical aside (`...(during PR #133)`). The tighter
# character class limits the match to the queued-PR target form
# `Next, PR #128` / `Next — PR #128` / `queued PR #128` and excludes
# any inline word characters between the marker and the digit-bearing
# PR ref.
QUEUED_PR_PATTERN = re.compile(
    r"\b(?:next|queued|pending|upcoming)\b[\s,:—–-]*PR\s*#(\d+)",
    re.IGNORECASE,
)

# Sweep-cursor pattern. Match `Last validation sweep: Sweep N iteration M`
# or `Last validation sweep: Sweep N iter M`. Tolerates markdown bold
# markers (`**`) around the phrase, e.g. `**Last validation sweep**: Sweep ...`,
# which is the typical form in TODO.md.
SWEEP_CURSOR_PATTERN = re.compile(
    r"\bLast\s+validation\s+sweep[*:\s]+Sweep\s+(\d+)\s+iter(?:ation)?\s+(\d+)",
    re.IGNORECASE,
)

# Sweep history row pattern (matches the table row format in history.md).
# Captures sweep number and iteration number.
HISTORY_ROW_PATTERN = re.compile(
    r"^\|\s*\d{4}-\d{2}-\d{2}\s*"  # date
    r"\|\s*(\d+)\s+iter\s+(\d+)\s*"  # sweep N iter M
    r"\|",
    re.MULTILINE,
)


def run_git(*args: str) -> str:
    """Run `git <args>` from REPO_ROOT and return stdout, stripped."""
    return subprocess.check_output(
        ["git", "-C", str(REPO_ROOT), *args],
        text=True,
    ).strip()


def merged_prs() -> set[int]:
    """Return the set of PR numbers merged into the current branch.

    Parses `git log` for "Merge pull request #N" subject lines.
    """
    try:
        log = run_git("log", "--format=%s", "--all")
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git log failed: {exc}", file=sys.stderr)
        raise

    return {
        int(m.group(1))
        for m in re.finditer(r"Merge pull request #(\d+)", log)
    }


def latest_sweep_iteration(history_path: Path) -> tuple[int, int] | None:
    """Read sweep history file and return (sweep_n, iter_m) of the most
    recent row, or None if no rows present."""
    if not history_path.exists():
        return None
    text = history_path.read_text(encoding="utf-8")
    matches = HISTORY_ROW_PATTERN.findall(text)
    if not matches:
        return None
    # The table is reverse-chronological; first match is the most recent.
    # But to be safe, take the max by (sweep_n, iter_m) tuple.
    rows = [(int(s), int(i)) for s, i in matches]
    return max(rows)


def check_file(path: Path, merged: set[int], latest: tuple[int, int] | None) -> list[str]:
    """Scan a single TODO-shaped file and return finding strings."""
    findings: list[str] = []
    text = path.read_text(encoding="utf-8")

    # Check 1: queued-PR-already-merged.
    # Walk line-by-line so we can report line numbers.
    for lineno, line in enumerate(text.splitlines(), 1):
        for match in QUEUED_PR_PATTERN.finditer(line):
            pr_n = int(match.group(1))
            if pr_n in merged:
                findings.append(
                    f"  L{lineno} [queued-PR-merged] line marks "
                    f"PR #{pr_n} as queued/next/pending/upcoming "
                    f"but PR #{pr_n} has merged into the current "
                    f"branch. Update the line to reflect that the "
                    f"PR has landed (move to PRs-completed list, or "
                    f"remove the queued framing)."
                )

    # Check 2: sweep-cursor-behind-history.
    if latest is not None:
        latest_sweep, latest_iter = latest
        for lineno, line in enumerate(text.splitlines(), 1):
            match = SWEEP_CURSOR_PATTERN.search(line)
            if not match:
                continue
            cursor_sweep = int(match.group(1))
            cursor_iter = int(match.group(2))
            if (cursor_sweep, cursor_iter) < (latest_sweep, latest_iter):
                findings.append(
                    f"  L{lineno} [sweep-cursor-stale] line claims "
                    f"last sweep was Sweep {cursor_sweep} iter "
                    f"{cursor_iter}, but {SWEEP_HISTORY_PATH} has a "
                    f"more recent row at Sweep {latest_sweep} iter "
                    f"{latest_iter}. Update the cursor."
                )

    return findings


def main() -> int:
    try:
        merged = merged_prs()
    except subprocess.CalledProcessError:
        return 2

    latest = latest_sweep_iteration(REPO_ROOT / SWEEP_HISTORY_PATH)

    all_findings: dict[str, list[str]] = {}
    for rel in TARGET_FILES:
        path = REPO_ROOT / rel
        if not path.exists():
            print(
                f"ERROR: target file {rel} does not exist.",
                file=sys.stderr,
            )
            return 2
        findings = check_file(path, merged, latest)
        if findings:
            all_findings[rel] = findings

    if not all_findings:
        n = len(TARGET_FILES)
        print(
            f"OK: TODO staleness audit clean across {n} target file(s)."
        )
        return 0

    for rel, findings in all_findings.items():
        print(f"=== {rel} ===", file=sys.stderr)
        for f in findings:
            print(f, file=sys.stderr)
        print("", file=sys.stderr)

    total = sum(len(v) for v in all_findings.values())
    print(
        f"FAIL: {total} stale pattern(s) detected across "
        f"{len(all_findings)} file(s).",
        file=sys.stderr,
    )
    print(
        "TODO staleness audit (gate 45) catches the recurring drift "
        "shapes the convention amendment in PR #127 reframed at the "
        "source. See dev-security/claude-rules/governance/"
        "change-tracking.md for the convention rationale.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
