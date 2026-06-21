#!/usr/bin/env python3
"""Overnight-work file audit (gate 46).

Scans [`.working/overnight-pr.md`](.working/overnight-pr.md) and
enforces the overnight-work protocol documented in
``dev-security/claude-rules/governance/change-tracking.md``.

The file's ``Status`` field encodes whether an overnight session is
in flight, active, or has ended without subsequent morning
processing. Permitted values:

- ``stub`` — no overnight session is in flight (default state and
  post-processing state). Gate passes.
- ``in-flight`` — overnight session is active. Gate passes. Overnight
  PRs commit the file in this state.
- ``done`` — overnight session has ended; next-morning processing PR
  must route content and reset to ``stub``. **Gate fails.**

Any other ``Status`` value triggers a gate failure (malformed file).
A missing file or missing ``Status:`` line also triggers a failure.

The gate's purpose: ensure that overnight-session content does not
linger in the file past the morning processing. The ``done`` value is
the explicit "needs processing" signal; the gate flags it so the
maintainer or assistant runs the morning processing PR before
continuing other work.

Exit codes:
    0 — Status is ``stub`` or ``in-flight``.
    1 — Status is ``done`` (morning processing required) or any other
        invalid value.
    2 — File missing, unreadable, or has no ``Status:`` line.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OVERNIGHT_FILE = REPO_ROOT / ".working" / "overnight-pr.md"

STATUS_PATTERN = re.compile(r"^\*\*Status:\*\*\s+(\S+)\s*$", re.MULTILINE)

VALID_PASS_STATUSES = {"stub", "in-flight"}
VALID_FAIL_STATUSES = {"done"}


def main() -> int:
    if not OVERNIGHT_FILE.exists():
        print(
            f"ERROR: {OVERNIGHT_FILE.relative_to(REPO_ROOT)} does not "
            f"exist. The overnight-work protocol requires this file to "
            f"exist in stub form.",
            file=sys.stderr,
        )
        return 2

    try:
        text = OVERNIGHT_FILE.read_text(encoding="utf-8")
    except OSError as exc:
        print(
            f"ERROR: cannot read {OVERNIGHT_FILE.relative_to(REPO_ROOT)}: "
            f"{exc}",
            file=sys.stderr,
        )
        return 2

    match = STATUS_PATTERN.search(text)
    if not match:
        print(
            f"ERROR: {OVERNIGHT_FILE.relative_to(REPO_ROOT)} has no "
            f"`**Status:** <value>` line. The overnight-work protocol "
            f"requires this field. Permitted values: stub, in-flight, "
            f"done.",
            file=sys.stderr,
        )
        return 2

    status = match.group(1).lower()

    if status in VALID_PASS_STATUSES:
        print(
            f"OK: {OVERNIGHT_FILE.relative_to(REPO_ROOT)} Status: "
            f"{status}. No action required."
        )
        return 0

    if status in VALID_FAIL_STATUSES:
        print(
            f"FAIL: {OVERNIGHT_FILE.relative_to(REPO_ROOT)} Status: "
            f"{status}. The overnight session has ended; the next-"
            f"morning processing PR must route the file's content into "
            f"the appropriate working-state ledgers "
            f"(.working/design-decisions.md for design decisions, "
            f".working/DONE.md for closed work, TODO.md for queued "
            f"follow-ups) and reset this file to the stub form. See "
            f"dev-security/claude-rules/governance/change-tracking.md "
            f"PR finalization protocol section for the routing detail.",
            file=sys.stderr,
        )
        return 1

    print(
        f"FAIL: {OVERNIGHT_FILE.relative_to(REPO_ROOT)} has invalid "
        f"Status value `{status}`. Permitted values: stub, in-flight, "
        f"done.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
