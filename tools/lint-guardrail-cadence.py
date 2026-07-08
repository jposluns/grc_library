#!/usr/bin/env python3
"""Verify guardrail-review currency against machinery-inventory drift (gate 60).

The guardrail-review skill's auto-prompt cadence (a structural-integrity review
after any PR that adds, removes, or renames a rule, skill, or gate) is a prose
convention with no mechanical backstop, and it was not honoured: between the
first run (2026-06-25, against a materially smaller inventory; the r1 history
row carries the as-of counts) and
the 2026-07-02 review, the machinery grew on every axis with no review recorded
(the GR-5 finding of the 2026-07-02 review itself). This gate is the GR-5
mechanization: it compares the CURRENT machinery inventory against the as-of
counts recorded in the most recent guardrail-review history row, and fails when
the accumulated drift exceeds a threshold, so sustained machinery growth
mechanically forces the review the cadence already calls for.

Mechanics:
  - The most recent row of `.working/guardrail-reviews/history.md` (rows are
    reverse-chronological, newest on top) must carry an inventory token of the
    form ``inventory N gates / N rules / N skills / N commands`` (the commands
    axis is optional for pre-convention rows) in its Summary cell.
  - The live counts are derived from the canonical sources: gate rows in the
    section-6 inventory table of
    `governance/specification-audit-programme.md` (the same table gates 35
    and 39 key on), governance-rule files under
    `dev-security/claude-rules/governance/`, `SKILL.md` files under
    `dev-security/claude-rules/skills/`, and command files under
    `.claude/commands/`.
  - Drift is the sum of absolute per-axis deltas. Zero drift passes silently;
    drift below the threshold passes with a warning line naming the deltas
    (the review is not yet due); drift at or above ``FAIL_DRIFT_THRESHOLD``
    fails: run the guardrail-review skill and record its history row (with the
    fresh inventory token), which resets the baseline.
  - A missing history file, no parseable data row, or a top row without an
    inventory token fails closed: the gate exists precisely because the record
    convention was not being honoured, so an unparseable record is a finding,
    not a skip.

The threshold (3, sum of absolute deltas) is the maintainer's calibration:
the 2026-07-02 return round redirected the build-time proceeded default of 5
to the stricter 3 (the decision trail is in `.working/pending-decisions.md`).
It is deliberately larger than one so a single gate-adding PR (including the
PR that shipped this gate) warns rather than blocks, and small enough that a
wave of machinery growth cannot run past the cadence unreviewed.

Usage:
    python3 tools/lint-guardrail-cadence.py

Exit codes:
    0   drift below the threshold (with a warning line when non-zero)
    1   drift at/above the threshold, or the history record is unusable
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lint_common import REPO_ROOT, read_text_safe

HISTORY = ".working/guardrail-reviews/history.md"
SPEC = "governance/specification-audit-programme.md"
RULES_DIR = "dev-security/claude-rules/governance"
SKILLS_DIR = "dev-security/claude-rules/skills"
COMMANDS_DIR = ".claude/commands"

# Sum of absolute per-axis deltas at/above which the gate fails. See the
# docstring for the calibration rationale (maintainer-set at the 2026-07-02
# return round, tightening the build-time proceeded default of 5).
FAIL_DRIFT_THRESHOLD = 3

# The as-of inventory token a guardrail-review history row's Summary cell
# carries, e.g. "inventory N gates / N rules / N skills / N commands"
# (placeholder counts: the regex matches any digits, and hardcoding the live
# totals here re-stales the comment on every inventory change, so it stays
# count-free by design). The commands axis is optional: the r1 row predates it.
INVENTORY_RE = re.compile(
    r"inventory\s+(\d+)\s+gates?\s*/\s*(\d+)\s+rules?\s*/\s*(\d+)\s+skills?"
    r"(?:\s*/\s*(\d+)\s+commands?)?",
    re.IGNORECASE,
)

# A history data row: leading pipe, an ISO date cell.
DATA_ROW_RE = re.compile(r"^\|\s*\d{4}-\d{2}-\d{2}\s*\|")

# A section-6 inventory table data row: "| <gate number> | ...".
GATE_ROW_RE = re.compile(r"^\|\s*\d+\s*\|")
SECTION_6_RE = re.compile(r"^## 6\.")
SECTION_END_RE = re.compile(r"^## ")


def recorded_inventory(text: str) -> tuple[dict[str, int], str] | None:
    """Return ({axis: count}, row_date) from the newest history row, or None."""
    for line in text.splitlines():
        if not DATA_ROW_RE.match(line):
            continue
        m = INVENTORY_RE.search(line)
        if m is None:
            return None  # newest row carries no inventory token: fail closed
        counts = {
            "gates": int(m.group(1)),
            "rules": int(m.group(2)),
            "skills": int(m.group(3)),
        }
        if m.group(4) is not None:
            counts["commands"] = int(m.group(4))
        date = line.split("|")[1].strip()
        return counts, date
    return None


def live_inventory(root: Path) -> dict[str, int] | None:
    """Count the live machinery from its canonical sources."""
    spec_text = read_text_safe(root / SPEC) if (root / SPEC).is_file() else None
    if spec_text is None:
        return None
    # Scope the row count to the section-6 inventory (the same region gates
    # 35 and 39 parse): a future numeric-first-cell table elsewhere in the
    # spec must not inflate the live gate count (the routed #577 sweep L2).
    gates = 0
    in_section_6 = False
    for ln in spec_text.splitlines():
        if SECTION_6_RE.match(ln):
            in_section_6 = True
            continue
        if in_section_6 and SECTION_END_RE.match(ln):
            break
        if in_section_6 and GATE_ROW_RE.match(ln):
            gates += 1
    rules = len(list((root / RULES_DIR).glob("*.md")))
    skills = len(list((root / SKILLS_DIR).glob("*/SKILL.md")))
    commands = len(list((root / COMMANDS_DIR).glob("*.md")))
    return {"gates": gates, "rules": rules, "skills": skills, "commands": commands}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Verify guardrail-review currency against machinery-inventory drift."
    )
    parser.add_argument(
        "--root",
        default=str(REPO_ROOT),
        help="Repository root (defaults to the live repo; overridden in regression tests).",
    )
    args = parser.parse_args(argv[1:])
    root = Path(args.root)

    history_path = root / HISTORY
    history_text = read_text_safe(history_path) if history_path.is_file() else None
    if history_text is None:
        print(f"FAIL: cannot read the guardrail-review history at {HISTORY}.")
        return 1

    recorded = recorded_inventory(history_text)
    if recorded is None:
        print(
            f"FAIL: the newest guardrail-review history row in {HISTORY} carries no "
            f"parseable 'inventory N gates / N rules / N skills [/ N commands]' token "
            f"(or the table has no data row). Record the review's as-of inventory in "
            f"its Summary cell; the cadence gate keys on it."
        )
        return 1
    baseline, baseline_date = recorded

    live = live_inventory(root)
    if live is None:
        print(f"FAIL: cannot read the gate inventory source at {SPEC}.")
        return 1

    deltas = {
        axis: live[axis] - baseline[axis]
        for axis in baseline
    }
    drift = sum(abs(d) for d in deltas.values())
    delta_text = ", ".join(
        f"{axis} {baseline[axis]}->{live[axis]} ({d:+d})"
        for axis, d in deltas.items()
        if d
    )

    if drift >= FAIL_DRIFT_THRESHOLD:
        print(
            f"FAIL: machinery inventory has drifted {drift} (threshold "
            f"{FAIL_DRIFT_THRESHOLD}) since the last guardrail review "
            f"({baseline_date}): {delta_text}. Run the guardrail-review skill "
            f"(/guardrails) and record its history row with a fresh inventory "
            f"token, which resets this baseline."
        )
        return 1

    if drift:
        print(
            f"OK (warning): machinery inventory has drifted {drift} since the last "
            f"guardrail review ({baseline_date}): {delta_text}. A /guardrails run is "
            f"due when the drift reaches {FAIL_DRIFT_THRESHOLD}."
        )
        return 0

    print(
        f"OK: machinery inventory matches the last guardrail review "
        f"({baseline_date}): "
        + ", ".join(f"{baseline[a]} {a}" for a in baseline)
        + "."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
