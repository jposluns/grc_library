#!/usr/bin/env python3
"""Verify a PR that asserts it closes a TODO item also rotates it to DONE (delta gate D5).

This is the PR-time, CHANGELOG-asserts-closure half of the §4.10 TODO/DONE
rotation bookkeeping-parity gate family. Its static companion is the corpus
gate "Backlog marked-done audit" (gate 57, `lint-todo-marked-done.py`), which
flags an item self-marked done IN PLACE. This check covers the case gate 57
cannot see: a PR that CLOSES a TODO item (its CHANGELOG says so) but never
edits `TODO.md` at all, so there is nothing self-marked for the static gate to
catch. That is the #466 failure mode (it built gate 56 "closing TODO §4.5 S4"
but omitted the rotation; the omission surfaced only in the post-merge sweep).

The rule (change-tracking PR-finalization protocol): when a PR closes a TODO
item, the item is deleted from `TODO.md` and an entry is added to
`.working/DONE.md` in the SAME diff. This gate enforces that mechanically at PR
time: if any line ADDED to the CHANGELOG (root or detailed mirror) asserts a
TODO-item closure, the PR's changed-file set must include BOTH `TODO.md` and
`.working/DONE.md`.

Trigger (deliberately precise, to stay false-positive-free): an added CHANGELOG
line matching the canonical closure phrasing ``clos(e|es|ed|ing) [the] TODO §``.
This matches "closing TODO §4.5 S4" (the genuine-closure convention) and not
incidental mentions such as "closing the #466 finding" (no ``TODO §`` adjacency)
or "TODO §4.10 updated" (no closure verb). A closure phrased WITHOUT the
``TODO §`` form (a bare ``§X`` or an ``FR-N``-keyed closure) is out of the
trigger's scope by design: broadening to those would false-fire on the many
CHANGELOG entries that merely mention an FR or a section, and the cost of a
standing PR-time gate that false-fails real PRs is high. The static marked-done
gate and the close-out-checklist convention cover the residual.

Opt-out / exemption: any commit in the PR range carrying a

    TodoRotation: <one-line-reason>

trailer satisfies the gate. This covers (a) a CHANGELOG entry that NARRATES a
past closure (e.g. quoting "closing TODO §X" while describing a prior PR), which
would otherwise false-trigger, and (b) the session-closing handoff-PR case (the
shared handoff-exemption logic of the bookkeeping-parity gate family). The
trailer is the same proven shape as the ``Changelog:`` opt-out of delta gate D1.

Usage:
    # In CI (uses GITHUB_BASE_REF):
    python3 tools/check-todo-rotation-on-pr.py

    # Locally, comparing HEAD to a specific base:
    python3 tools/check-todo-rotation-on-pr.py origin/main
    python3 tools/check-todo-rotation-on-pr.py origin/main HEAD

Exit codes:
    0 : no closure assertion in the added CHANGELOG lines, OR both TODO.md and
        DONE.md are in the diff, OR an opt-out trailer is present, OR empty diff.
    1 : a closure is asserted but TODO.md and/or .working/DONE.md is missing.
    2 : invocation or environment error (cannot determine base/head, git failure).
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

CHANGELOG_PATHS = ("CHANGELOG.md", ".working/changelog-details/CHANGELOG-detailed.md")
TODO_PATH = "TODO.md"
DONE_PATH = ".working/DONE.md"

# Canonical TODO-item closure phrasing: a closure verb, an optional "the", then
# "TODO §". Case-insensitive on the verb; "TODO" is the established uppercase
# token but IGNORECASE keeps it robust.
CLOSURE_PATTERN = re.compile(
    r"\bclos(?:e|es|ed|ing)\b\s+(?:the\s+)?TODO\s+§",
    re.IGNORECASE,
)

TRAILER_PATTERN = re.compile(
    r"^\s*TodoRotation:\s*(\S.*?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def asserts_todo_closure(added_lines: list[str]) -> str | None:
    """Return the first added line that asserts a TODO-item closure, or None.

    Pure helper (no git), unit-tested directly: this is the false-positive-
    critical part of the gate.
    """
    for line in added_lines:
        if CLOSURE_PATTERN.search(line):
            return line
    return None


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def added_changelog_lines(merge_base: str, head: str) -> list[str]:
    """The '+' lines (added content, not '+++' headers) of the CHANGELOG diff."""
    try:
        diff = git("diff", merge_base, head, "--", *CHANGELOG_PATHS)
    except subprocess.CalledProcessError:
        return []
    out: list[str] = []
    for line in diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            out.append(line[1:])
    return out


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check that a PR asserting a TODO-item closure also rotates the "
            "item (touches TODO.md and .working/DONE.md)."
        ),
    )
    parser.add_argument("base", nargs="?", help="Base ref (default: origin/$GITHUB_BASE_REF in CI).")
    parser.add_argument("head", nargs="?", default="HEAD", help="Head ref (default: HEAD).")
    args = parser.parse_args(argv[1:])

    base = args.base
    if not base:
        github_base = os.environ.get("GITHUB_BASE_REF")
        if not github_base:
            print(
                "ERROR: base ref not provided and GITHUB_BASE_REF is unset. "
                "Pass a base ref as the first positional argument when running "
                "locally (e.g. origin/main).",
                file=sys.stderr,
            )
            return 2
        base = f"origin/{github_base}"
    head = args.head

    try:
        merge_base = git("merge-base", base, head)
    except subprocess.CalledProcessError as exc:
        print(
            f"ERROR: could not determine merge-base of {base}..{head}: {exc}. "
            f"In GitHub Actions, ensure actions/checkout uses fetch-depth: 0.",
            file=sys.stderr,
        )
        return 2

    try:
        changed = [ln for ln in git("diff", "--name-only", merge_base, head).splitlines() if ln]
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git diff failed: {exc}", file=sys.stderr)
        return 2

    if not changed:
        print(f"OK: no files changed between {merge_base[:8]} and {head}.")
        return 0

    closure_line = asserts_todo_closure(added_changelog_lines(merge_base, head))
    if closure_line is None:
        print("OK: no TODO-item closure asserted in the added CHANGELOG lines.")
        return 0

    if TODO_PATH in changed and DONE_PATH in changed:
        print(
            f"OK: CHANGELOG asserts a TODO-item closure and the diff rotates it "
            f"(both {TODO_PATH} and {DONE_PATH} are in the diff)."
        )
        return 0

    # Closure asserted but a rotation surface is missing: check the opt-out trailer.
    try:
        commit_shas = git("log", "--format=%H", f"{merge_base}..{head}").splitlines()
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git log failed: {exc}", file=sys.stderr)
        return 2
    for sha in commit_shas:
        match = TRAILER_PATTERN.search(git("log", "-1", "--format=%B", sha))
        if match:
            print(
                f"OK: commit {sha[:8]} carries opt-out trailer: "
                f"'TodoRotation: {match.group(1)}'."
            )
            return 0

    missing = [p for p in (TODO_PATH, DONE_PATH) if p not in changed]
    print(
        f"FAIL: an added CHANGELOG line asserts a TODO-item closure but the diff "
        f"does not rotate it: {', '.join(missing)} not in the diff.",
        file=sys.stderr,
    )
    print(f"  asserting line: {closure_line.strip()[:160]}", file=sys.stderr)
    print("", file=sys.stderr)
    print(
        "When a PR closes a TODO item, delete it from TODO.md and add a row to "
        ".working/DONE.md in the same diff (the change-tracking rotation discipline). "
        "If the CHANGELOG line merely narrates a past closure, add a "
        "'TodoRotation: <reason>' trailer to any commit to opt out.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
