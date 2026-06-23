#!/usr/bin/env python3
"""Paired-skill step-parity audit.

For each known paired surface (a SKILL.md + slash-command .md
describing the same workflow), verify that the set of step
identifiers in the two files matches by symmetric difference.

The motivating finding is Sweep 3 in the validation-sweep history
register: PR #78 introduced the deterministic pre-flight scanner
as ``### 3.5.`` in the SKILL.md heading and as ``3a.`` in the
slash-command numbered list. The two surfaces named the same
logical step with two different identifiers; the drift was caught
by subagent A's semantic triage in Sweep 3 and fixed in PR #80.
This gate catches the same shape mechanically on future drift.

Scope: only paired surfaces in the PAIRS registry are checked. Skills
that ship both a SKILL.md and a slash-command counterpart must be
registered in PAIRS to inherit the parity check; missing the
registration is a discipline gap the orchestrator must close at
ship time (per `ai-assistant-workflow-disciplines.md` §3 Apply-time
worker correction).

Step-identifier extraction:
- SKILL.md headings: ``### N. Title`` or ``### N<suffix>. Title``
  (where suffix is a lowercase letter or `.N`, e.g. ``3a``, ``3.5``).
- Slash-command numbered items: ``N. **Title**:`` at line start.
- Slash-command prose mentions: ``Step N`` (case-sensitive S),
  to catch the ``Step 8 (only when...)`` form the validation-sweep
  command file uses for the final step.

Exit codes:
    0 - All paired surfaces have matching step-identifier sets.
    1 - At least one pair has a symmetric-difference mismatch.

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from lint_common import REPO_ROOT, read_text_safe


# Each entry: (skill_path, command_path). Add a pair when a new
# skill ships a slash-command counterpart.
PAIRS: list[tuple[str, str]] = [
    (
        "dev-security/claude-rules/skills/validation-sweep/SKILL.md",
        ".claude/commands/validate.md",
    ),
    (
        "dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md",
        ".claude/commands/validate-pr.md",
    ),
    (
        "dev-security/claude-rules/skills/library-fitness-review/SKILL.md",
        ".claude/commands/fitness.md",
    ),
    (
        "dev-security/claude-rules/skills/pr-retrospective/SKILL.md",
        ".claude/commands/retro.md",
    ),
    (
        "dev-security/claude-rules/skills/deep-qa-review/SKILL.md",
        ".claude/commands/full-qa.md",
    ),
    (
        "dev-security/claude-rules/skills/guardrail-review/SKILL.md",
        ".claude/commands/guardrails.md",
    ),
]

# SKILL.md step heading: `### N. ` or `### N<suffix>. ` where
# suffix is a lowercase letter or `.N` continuation (e.g. `3a`,
# `3.5`). Captures the identifier portion (digits + optional
# alphanumeric/dot suffix).
SKILL_STEP_RE = re.compile(
    r"^###\s+(\d+(?:[a-z]|\.\d+)?)\.\s",
    re.MULTILINE,
)

# Slash-command numbered list item: `N. **Title**:` at line start.
# Captures the identifier the same way as SKILL_STEP_RE.
COMMAND_NUMBERED_RE = re.compile(
    r"^(\d+(?:[a-z]|\.\d+)?)\.\s+\*\*",
    re.MULTILINE,
)

# Slash-command prose mention: `Step N` (case-sensitive S).
# Used for steps mentioned in narrative rather than as numbered
# items (e.g. the validation-sweep command file's
# "Step 8 (only when the sweep produced findings)" form).
COMMAND_PROSE_RE = re.compile(r"\bStep\s+(\d+(?:[a-z]|\.\d+)?)\b")


def extract_skill_steps(text: str) -> set[str]:
    return set(SKILL_STEP_RE.findall(text))


def extract_command_steps(text: str) -> set[str]:
    return (
        set(COMMAND_NUMBERED_RE.findall(text))
        | set(COMMAND_PROSE_RE.findall(text))
    )


def main() -> int:
    findings: list[str] = []
    pairs_checked = 0
    for skill_rel, command_rel in PAIRS:
        skill_path = REPO_ROOT / skill_rel
        command_path = REPO_ROOT / command_rel
        if not skill_path.is_file():
            findings.append(
                f"missing SKILL file: {skill_rel} (configured in PAIRS)"
            )
            continue
        if not command_path.is_file():
            findings.append(
                f"missing slash-command file: {command_rel} "
                f"(configured in PAIRS)"
            )
            continue
        skill_text = read_text_safe(skill_path)
        command_text = read_text_safe(command_path)
        if skill_text is None or command_text is None:
            findings.append(
                f"unreadable file in pair: {skill_rel} / {command_rel}"
            )
            continue
        skill_steps = extract_skill_steps(skill_text)
        command_steps = extract_command_steps(command_text)
        only_in_skill = skill_steps - command_steps
        only_in_command = command_steps - skill_steps
        if only_in_skill or only_in_command:
            findings.append(
                f"pair drift: {skill_rel} (steps {sorted(skill_steps)}) "
                f"vs {command_rel} (steps {sorted(command_steps)}). "
                f"Only in SKILL: {sorted(only_in_skill)}; "
                f"only in command: {sorted(only_in_command)}. "
                "Same logical step in both files must use the same "
                "identifier; rename one to match the other."
            )
        pairs_checked += 1

    if findings:
        for f in findings:
            print(f"FAIL: {f}", file=sys.stderr)
        return 1
    print(
        f"OK: {pairs_checked} paired skill+slash-command surface(s) "
        "have matching step-identifier sets."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
