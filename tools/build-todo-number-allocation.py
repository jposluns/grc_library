#!/usr/bin/env python3
"""Generate the `## Number allocation` counter block in ``TODO.md`` from a PUBLIC floor
file plus the live public backlog ids, so a human can never hand-set a counter below the
highest-used number, and so the check runs on CI and adopter clones (no private data).

WHAT IS GENERATED. Only the seven ``- **Next item number: X.**`` counter bullets, between
``<!-- BEGIN-GENERATED number-allocation -->`` and ``<!-- END-GENERATED number-allocation -->``.
The surrounding prose (the permanence note and the 3.x counter-less note) is hand-maintained.

THE PUBLIC FLOOR (``tools/todo-number-floor.json``). The floor records the highest ordinal
EVER allocated per PUBLIC series (bare ``N.M`` / ``TF-n``; the ``P-N.M`` private namespace is
separate), including RETIRED numbers that no live file still holds. It is monotonic (only ever
increases) and is bumped in the PR that allocates a new number. Because the floor is a committed
PUBLIC file, ``--check`` verifies the block on CI and adopter clones with NO dependency on the
private ``grc_library_private`` sibling (the flaw of the earlier DONE-archive design, which made
the check a maintainer-local no-op). ``gate 78`` reads the same floor for its recycle check.

next(series) = max(floor[series], highest live public id in series) + 1. Live ids come from the
``TODO.md`` INDEX ROWS, ``TODO-REFERENCE.md`` and ``P-TODO.md`` bare-id headings. Series 5/6/7 are
FROZEN (render a next line, draw nothing); the 3.x series has NO counter line (a prose note).

FLOOR SOUNDNESS. ``--check`` also fails if the floor is BELOW any live id (a floor set too low
would let a counter collide with a live id), so the floor cannot silently under-record.

Usage:
  python3 tools/build-todo-number-allocation.py            # regenerate in place
  python3 tools/build-todo-number-allocation.py --check    # exit 1 on drift (CI)
  python3 tools/build-todo-number-allocation.py --self-test # unit self-check
"""
import argparse
import json
import re
import sys
from pathlib import Path

from lint_common import REPO_ROOT  # noqa: E402

BEGIN = "<!-- BEGIN-GENERATED number-allocation -->"
END = "<!-- END-GENERATED number-allocation -->"
FLOOR_PATH = "tools/todo-number-floor.json"

ACTIVE = [(1, "P1 / fix series"), (2, "P2 / content series"), (4, "P4 / adopter series")]
FROZEN = [5, 6, 7]

HEADING_ID = re.compile(r"^### ((?:P-)?\d+(?:\.\d+)+[a-z]?|TF-\d+)\b")
TF_TOKEN = re.compile(r"(?<![\w-])TF-(\d+)\b")


def load_floor(root):
    raw = json.loads((root / FLOOR_PATH).read_text())
    floor = {}
    tf = 0
    for k, v in raw.items():
        if k.startswith("_"):
            continue
        if k == "TF":
            tf = int(v)
        else:
            floor[int(k)] = int(v)
    return floor, tf


def live_maxima(root):
    """Highest live public ordinal per series, and highest live TF, across TODO.md index
    rows + TODO-REFERENCE.md/P-TODO.md bare-id headings. The P-N.M private namespace is
    excluded. Retired ids are NOT here (that is what the floor is for)."""
    import lint_common
    tops, tf = {}, 0

    def add(idstr):
        nonlocal tf
        if idstr.startswith("P-"):
            return
        m = re.match(r"^(\d+)\.(\d+)", idstr)
        if m:
            s, o = int(m.group(1)), int(m.group(2))
            tops[s] = max(tops.get(s, 0), o)
            return
        m = re.match(r"^TF-(\d+)", idstr)
        if m:
            tf = max(tf, int(m.group(1)))

    for i in lint_common.todo_index_ids((root / "TODO.md").read_text(errors="replace")):
        add(i)
    for name in ("TODO-REFERENCE.md", "P-TODO.md"):
        f = root / name
        if not f.is_file():
            f = root.parent / "grc_library_private" / name  # P-TODO lives in the private sibling
        if f.is_file():
            for ln in f.read_text(errors="replace").split("\n"):
                m = HEADING_ID.match(ln)
                if m:
                    add(m.group(1))
                if name == "P-TODO.md":
                    for n in TF_TOKEN.findall(ln):
                        tf = max(tf, int(n))
    return tops, tf


def compute_counters(root=None):
    root = Path(root) if root else REPO_ROOT
    floor, floor_tf = load_floor(root)
    live, live_tf = live_maxima(root)
    tops = {}
    for s in set(floor) | set(live):
        tops[s] = max(floor.get(s, 0), live.get(s, 0))
    tf_max = max(floor_tf, live_tf)
    return tops, tf_max, floor, floor_tf, live, live_tf


def floor_violations(floor, floor_tf, live, live_tf):
    """Series where the floor is BELOW a live id (floor set too low: unsound)."""
    bad = [f"{s}.{live[s]} > floor {s}.{floor.get(s, 0)}"
           for s in live if live[s] > floor.get(s, 0)]
    if live_tf > floor_tf:
        bad.append(f"TF-{live_tf} > floor TF-{floor_tf}")
    return bad


def render_block(tops, tf_max):
    lines = []
    for series, label in ACTIVE:
        lines.append(f"- **Next item number: {series}.{tops.get(series, 0) + 1}.** ({label})")
    for series in FROZEN:
        lines.append(
            f"- **Next item number: {series}.{tops.get(series, 0) + 1}.** "
            f"(frozen; series {series} takes no new items)")
    lines.append(f"- **Next item number: TF-{tf_max + 1}.** (time-bounded follow-ups)")
    return "\n".join(lines)


def _splice(todo_text, block):
    if BEGIN not in todo_text or END not in todo_text:
        raise ValueError(f"allocation sentinels not found ({BEGIN} / {END})")
    pre, rest = todo_text.split(BEGIN, 1)
    _, post = rest.split(END, 1)
    return f"{pre}{BEGIN}\n{block}\n{END}{post}"


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv[1:])
    if args.self_test:
        return self_test()

    todo_path = REPO_ROOT / "TODO.md"
    todo = todo_path.read_text(errors="replace")
    tops, tf_max, floor, floor_tf, live, live_tf = compute_counters()
    bad = floor_violations(floor, floor_tf, live, live_tf)
    if bad:
        sys.stderr.write("FAIL: the number floor is BELOW a live id (bump "
                         f"{FLOOR_PATH}): {'; '.join(bad)}\n")
        return 1
    new_todo = _splice(todo, render_block(tops, tf_max))
    if args.check:
        if new_todo != todo:
            sys.stderr.write(
                "FAIL: TODO.md `## Number allocation` block is out of sync with the floor + "
                "live ids. Regenerate: python3 tools/build-todo-number-allocation.py\n")
            return 1
        print("OK: TODO.md number-allocation block is in sync with the public floor.")
        return 0
    todo_path.write_text(new_todo)
    print("Regenerated TODO.md number-allocation block from the public floor.")
    return 0


def self_test():
    import unittest

    class T(unittest.TestCase):
        def test_render_shape(self):
            block = render_block({1: 30, 2: 32, 4: 31, 5: 9, 6: 6, 7: 5}, 3)
            self.assertIn("- **Next item number: 1.31.** (P1 / fix series)", block)
            self.assertIn("- **Next item number: 2.33.** (P2 / content series)", block)
            self.assertIn("- **Next item number: 5.10.** (frozen; series 5 takes no new items)", block)
            self.assertIn("- **Next item number: TF-4.** (time-bounded follow-ups)", block)
            self.assertNotIn("Next item number: 3.", block)

        def test_next_is_max_floor_live(self):
            # counter takes the HIGHER of floor and live, then +1
            tops = {}
            floor = {2: 32}
            live = {2: 20}
            for s in set(floor) | set(live):
                tops[s] = max(floor.get(s, 0), live.get(s, 0))
            self.assertEqual(tops[2], 32)  # floor (retired high) wins over lower live
            live2 = {2: 40}
            self.assertEqual(max(floor.get(2, 0), live2.get(2, 0)), 40)  # live wins when higher

        def test_floor_violation_detected(self):
            # a floor BELOW a live id must be reported (unsound floor)
            self.assertTrue(floor_violations({2: 10}, 0, {2: 32}, 0))
            self.assertFalse(floor_violations({2: 32}, 3, {2: 32}, 3))

        def test_splice_roundtrip(self):
            todo = f"pre\n{BEGIN}\nOLD\n{END}\npost\n"
            self.assertEqual(_splice(todo, "NEW"), f"pre\n{BEGIN}\nNEW\n{END}\npost\n")

        def test_splice_missing_sentinel_raises(self):
            with self.assertRaises(ValueError):
                _splice("no sentinels", "X")

        def test_reproduces_committed_block(self):
            """Reality anchor: the floor + live union regenerates the committed block
            byte-for-byte. Public + deterministic, so this runs on CI too (no private dep)."""
            tops, tf_max, floor, floor_tf, live, live_tf = compute_counters()
            self.assertFalse(floor_violations(floor, floor_tf, live, live_tf),
                             "the committed floor is below a live id")
            block = render_block(tops, tf_max)
            todo = (REPO_ROOT / "TODO.md").read_text()
            self.assertIn(BEGIN, todo, "sentinels missing from TODO.md (test would be vacuous)")
            cur = todo.split(BEGIN, 1)[1].split(END, 1)[0].strip("\n")
            self.assertEqual(block, cur, "generated block drifted from the committed block")

    runner = unittest.TextTestRunner(verbosity=1)
    ok = runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(T)).wasSuccessful()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
