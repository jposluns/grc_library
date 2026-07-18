#!/usr/bin/env python3
"""Session-state lease audit (gate 63).

Scans [`.working/session-state.md`](.working/session-state.md) and
enforces the WELL-FORMEDNESS of the session-concurrency lease that the
multi-session interlock relies on (design record: the design-decisions
record, "Session-concurrency safety"; the
`/resume` command's step 0 reads this file before anything else).

The lease declares which orchestrator session, if any, currently holds
the shared ``main`` state surfaces. Required fields, one per line:

- ``**Active-session:**`` — the active session's branch name, or
  ``none`` when no session holds the lease.
- ``**Status:**`` — ``active`` (a session holds the lease),
  ``winding-down`` (a session is landing its closing handoff PR), or
  ``released`` (no session holds the lease; the clean-close state).
- ``**Operating-mode:**`` — ``fully-attended``, ``attended-autonomous``,
  ``overnight-unattended``, or ``daytime-unattended``. The
  AskUserQuestion-blocking hook reads this and refuses a blocking prompt when
  the mode is unattended, so the value must always be present and current.
- ``**Last-heartbeat-UTC:**`` — a ``YYYY-MM-DDTHH:MM:SSZ`` stamp
  (``date -u +%Y-%m-%dT%H:%M:%SZ``), refreshed at each PR close-out.
- ``**Current-task:**`` — one line of free text.
- ``**Worker-dispatches:**`` — ``none`` or a free-text summary of the
  in-flight worker fan-out (cross-referencing the scratch
  ``claims-ledger.md`` when parallel work is running).

Coherence rules: ``released`` requires ``Active-session: none``;
``active`` and ``winding-down`` require a non-``none`` branch name.
Each field line appears exactly once (a duplicate is a finding), and
the coherence check runs unconditionally alongside the per-field value
checks, so coexisting defects are all reported in one run.

This gate guards the file's SHAPE only. It deliberately passes on all
three status values: CI runs per-branch and cannot see across
concurrent sessions, so the interlock itself (HOLD-and-surface on a
live lease or a recent unmerged sibling branch) lives in the `/resume`
step-0 procedure, not in CI. A malformed lease would silently disable
that procedure, which is the failure this gate exists to catch.

Exit codes:
    0 — all required fields present, valid, and coherent.
    1 — an invalid field value or a status/branch incoherence.
    2 — file missing, unreadable, or a required field line absent.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SESSION_STATE_FILE = REPO_ROOT / ".working" / "session-state.md"

FIELD_PATTERNS = {
    "Active-session": re.compile(
        r"^\*\*Active-session:\*\*\s+(\S+)\s*$", re.MULTILINE
    ),
    "Status": re.compile(r"^\*\*Status:\*\*\s+(\S+)\s*$", re.MULTILINE),
    "Operating-mode": re.compile(
        r"^\*\*Operating-mode:\*\*\s+(\S+)\s*$", re.MULTILINE
    ),
    "Last-heartbeat-UTC": re.compile(
        r"^\*\*Last-heartbeat-UTC:\*\*\s+(\S+)\s*$", re.MULTILINE
    ),
    "Current-task": re.compile(
        r"^\*\*Current-task:\*\*\s+(.+?)\s*$", re.MULTILINE
    ),
    "Worker-dispatches": re.compile(
        r"^\*\*Worker-dispatches:\*\*\s+(.+?)\s*$", re.MULTILINE
    ),
}

VALID_STATUSES = {"active", "winding-down", "released"}

# Operating mode (the AskUserQuestion-blocking hook reads this: it blocks a blocking
# prompt when the mode contains "unattended", so the value must be reliably present).
VALID_MODES = {
    "fully-attended",
    "attended-autonomous",
    "overnight-unattended",
    "daytime-unattended",
}

HEARTBEAT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def check_text(text: str) -> tuple[list[str], list[str]]:
    """Validate lease text; return (missing_field_errors, value_errors)."""
    missing: list[str] = []
    invalid: list[str] = []
    values: dict[str, str] = {}

    for field, pattern in FIELD_PATTERNS.items():
        matches = list(pattern.finditer(text))
        if not matches:
            missing.append(
                f"required field line `**{field}:** <value>` is absent"
            )
            continue
        if len(matches) > 1:
            invalid.append(
                f"field line `**{field}:**` appears {len(matches)} times; "
                f"each field appears exactly once"
            )
        values[field] = matches[0].group(1)

    status = values.get("Status")
    if status is not None and status.lower() not in VALID_STATUSES:
        invalid.append(
            f"Status value `{status}` is invalid; permitted values: "
            f"active, winding-down, released"
        )

    mode = values.get("Operating-mode")
    if mode is not None and mode.lower() not in VALID_MODES:
        invalid.append(
            f"Operating-mode value `{mode}` is invalid; permitted values: "
            f"fully-attended, attended-autonomous, overnight-unattended, daytime-unattended"
        )

    heartbeat = values.get("Last-heartbeat-UTC")
    if heartbeat is not None and not HEARTBEAT_RE.match(heartbeat):
        invalid.append(
            f"Last-heartbeat-UTC value `{heartbeat}` is not a "
            f"YYYY-MM-DDTHH:MM:SSZ stamp (use `date -u +%Y-%m-%dT%H:%M:%SZ`)"
        )

    session = values.get("Active-session")
    if status is not None and session is not None:
        status_lc = status.lower()
        if status_lc == "released" and session.lower() != "none":
            invalid.append(
                f"Status `released` requires `Active-session: none`, "
                f"found `{session}`"
            )
        if status_lc in {"active", "winding-down"} and session.lower() == "none":
            invalid.append(
                f"Status `{status}` requires a branch name in "
                f"Active-session, found `none`"
            )

    return missing, invalid


def main() -> int:
    rel = SESSION_STATE_FILE.relative_to(REPO_ROOT)

    if not SESSION_STATE_FILE.exists():
        print(
            f"ERROR: {rel} does not exist. The session-concurrency lease "
            f"protocol requires this file to exist (released stub at "
            f"minimum).",
            file=sys.stderr,
        )
        return 2

    try:
        text = SESSION_STATE_FILE.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: cannot read {rel}: {exc}", file=sys.stderr)
        return 2

    missing, invalid = check_text(text)

    # Report BOTH classes before exiting so coexisting defects surface in
    # one run; a missing field still takes exit-code precedence (2 over 1).
    for message in missing:
        print(f"ERROR: {rel}: {message}", file=sys.stderr)
    for message in invalid:
        print(f"FAIL: {rel}: {message}", file=sys.stderr)

    if missing:
        return 2

    if invalid:
        return 1

    print(f"OK: {rel} lease is well-formed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
