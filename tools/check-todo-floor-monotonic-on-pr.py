#!/usr/bin/env python3
"""Delta gate D12: the public number floor is MONOTONIC across a PR.

``tools/todo-number-floor.json`` records the highest ordinal EVER allocated per public
backlog series (gate 91 generates the ``## Number allocation`` counters from it, and gate 78
reads it for the recycle check). Those checks enforce that a counter is not BELOW the floor,
but nothing stops a hand-edit from LOWERING the floor itself: a lowered floor rewinds a
counter and silently permits recycling a retired id (the floor is its own only witness).

This delta gate closes that direction: it compares the PR's floor against the base revision
and FAILS if any series' floor DECREASED or a series was dropped. The floor may only rise
(a new allocation) or stay put. Runs PR-time, like the other ``check-*-on-pr.py`` gates.

Usage:
  python3 tools/check-todo-floor-monotonic-on-pr.py [BASE_REF] [HEAD_REF]
    BASE_REF defaults to origin/main; HEAD_REF omitted means the working tree.
"""
import json
import os
import subprocess
import sys

FLOOR_PATH = "tools/todo-number-floor.json"


def _git_show(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True)


def _parse(text):
    return {k: int(v) for k, v in json.loads(text).items() if not k.startswith("_")}


def find_violations(base, head):
    """Series where the head floor DECREASED below base or was dropped. Empty = monotonic."""
    out = []
    for series, base_v in base.items():
        if series not in head:
            out.append(f"series {series} dropped (was {base_v})")
        elif head[series] < base_v:
            out.append(f"series {series} floor decreased {base_v} -> {head[series]} "
                       "(rewinds a counter; permits recycling a retired id)")
    return out


def main(argv):
    if len(argv) > 1:
        base_ref = argv[1]
    else:
        gh_base = os.environ.get("GITHUB_BASE_REF")
        base_ref = f"origin/{gh_base}" if gh_base else "origin/main"
    head_ref = argv[2] if len(argv) > 2 else None
    try:
        base_text = _git_show(base_ref, FLOOR_PATH)
    except subprocess.CalledProcessError:
        # the floor did not exist at the base (first introduction): nothing to compare.
        print(f"OK: {FLOOR_PATH} is new at this base ({base_ref}); no prior floor to compare.")
        return 0
    try:
        head_text = _git_show(head_ref, FLOOR_PATH) if head_ref else \
            open(FLOOR_PATH, encoding="utf-8").read()
    except (subprocess.CalledProcessError, FileNotFoundError):
        sys.stderr.write(f"FAIL: {FLOOR_PATH} is missing at HEAD but present at {base_ref} "
                         "(the floor must never be removed).\n")
        return 1
    base, head = _parse(base_text), _parse(head_text)
    violations = find_violations(base, head)
    if violations:
        sys.stderr.write("FAIL: the public number floor is not monotonic vs "
                         f"{base_ref}: {'; '.join(violations)}. The floor may only rise or "
                         f"stay put; restore each decreased value in {FLOOR_PATH}.\n")
        return 1
    print(f"OK: {FLOOR_PATH} is monotonic vs {base_ref} "
          f"({len(base)} series, none decreased or dropped).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
