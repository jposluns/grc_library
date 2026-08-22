#!/usr/bin/env python3
"""Generate the `## Number allocation` counter block in ``TODO.md`` from a PUBLIC floor
file plus the live public backlog ids, so a human can never hand-set a counter below the
highest-used number, and so the check runs on CI and adopter clones (no private data).

WHAT IS GENERATED. Only the eight ``- **Next item number: X.**`` counter bullets, between
``<!-- BEGIN-GENERATED number-allocation -->`` and ``<!-- END-GENERATED number-allocation -->``.
The surrounding prose (the permanence note) is hand-maintained.

THE PUBLIC FLOOR (``tools/todo-number-floor.json``). The floor records the highest ordinal
EVER allocated per PUBLIC series (bare ``N.M`` / ``TF-n``; the ``P-N.M`` private namespace is
separate), including RETIRED numbers that no live file still holds. It is monotonic (only ever
increases) and is bumped in the PR that allocates a new number. Because the floor is a committed
PUBLIC file, ``--check`` verifies the block on CI and adopter clones with NO dependency on the
private ``grc_library_private`` sibling (the flaw of the earlier DONE-archive design, which made
the check a maintainer-local no-op). ``gate 78`` reads the same floor for its recycle check.

next(series) = max(floor[series], highest live public id in series) + 1. Live ids come from the
``TODO.md`` INDEX ROWS and ``TODO-REFERENCE.md`` bare-id headings (PUBLIC files only; the
floor covers retired numbers AND migrated bare ids that now live in the private P-TODO.md). Series 5/6/7 are
FROZEN (render a next line, draw nothing). Series 3 draws like the other ACTIVE series.

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

ACTIVE = [(1, "P1 / fix series"), (2, "P2 / content series"),
          (3, "P3 / tooling series"), (4, "P4 / adopter series")]
FROZEN = [5, 6, 7]

# C3 (r21 + closing-window residue): a FROZEN series takes NO new allocations.
# Two independent laundering paths must therefore be closed: raising its floor
# in lock-step with a new high id, and inserting a previously unrecorded id into
# a gap below the frozen ceiling. EXPECTED_FROZEN_FLOOR pins the immutable
# ceilings; EXPECTED_LIVE_FROZEN_IDS snapshots the already-live allocations.
# Their key sets are checked against FROZEN in executable code.
EXPECTED_FROZEN_FLOOR = {5: 9, 6: 6, 7: 5}
EXPECTED_LIVE_FROZEN_IDS = {
    5: frozenset({"5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.8", "5.9"}),
    6: frozenset({"6.1", "6.2", "6.3", "6.4", "6.5", "6.6"}),
    7: frozenset({"7.2", "7.3"}),
}


def frozen_floor_violations(floor, live_ids=()):
    """Frozen configuration, immutable-floor, or live-allocation violations."""
    bad = []
    frozen_keys = set(FROZEN)
    floor_keys = set(EXPECTED_FROZEN_FLOOR)
    live_snapshot_keys = set(EXPECTED_LIVE_FROZEN_IDS)

    if floor_keys != frozen_keys:
        bad.append(
            f"FROZEN keys {sorted(frozen_keys)} != "
            f"EXPECTED_FROZEN_FLOOR keys {sorted(floor_keys)}"
        )
    if live_snapshot_keys != frozen_keys:
        bad.append(
            f"FROZEN keys {sorted(frozen_keys)} != "
            f"EXPECTED_LIVE_FROZEN_IDS keys {sorted(live_snapshot_keys)}"
        )

    bad.extend(
        f"series {s}.{floor.get(s, 0)} != frozen ceiling {s}.{ceiling}"
        for s, ceiling in EXPECTED_FROZEN_FLOOR.items()
        if floor.get(s, 0) != ceiling
    )

    for item_id in sorted(set(live_ids)):
        match = re.match(r"^(\d+)\.", item_id)
        if not match:
            continue
        series = int(match.group(1))
        if (series in frozen_keys
                and item_id not in EXPECTED_LIVE_FROZEN_IDS.get(series, frozenset())):
            bad.append(f"unrecorded live frozen id {item_id}")
    return bad

HEADING_ID = re.compile(r"^### ((?:P-)?\d+(?:\.\d+)+[a-z]?|TF-\d+)\b")


def live_public_ids(root):
    """Exact live PUBLIC ids in TODO.md and TODO-REFERENCE.md (the ``P-N.M``
    private namespace is excluded)."""
    import lint_common

    ids = {
        item_id
        for item_id in lint_common.todo_index_ids(
            (root / "TODO.md").read_text(errors="replace")
        )
        if not item_id.startswith("P-")
    }
    ref = root / "TODO-REFERENCE.md"
    if ref.is_file():
        for line in ref.read_text(errors="replace").splitlines():
            match = HEADING_ID.match(line)
            if match and not match.group(1).startswith("P-"):
                ids.add(match.group(1))
    return ids


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
    """Highest live PUBLIC ordinal per series, and highest live TF, across the PUBLIC
    files only: TODO.md index rows + TODO-REFERENCE.md ``### `` bare-id headings. The
    ``P-N.M`` private namespace is excluded. This reads NO private data (no P-TODO.md, no
    grc_library_private): the public FLOOR is the authority for the highest EVER allocated
    ordinal (including retired numbers AND migrated bare ids that now live in the private
    P-TODO.md), so next = max(floor, live) is floor-dominated and fully public-deterministic.
    Retired ids are NOT here; that is what the floor is for."""
    tops, tf = {}, 0

    def add(idstr):
        nonlocal tf
        m = re.match(r"^(\d+)\.(\d+)", idstr)
        if m:
            s, o = int(m.group(1)), int(m.group(2))
            tops[s] = max(tops.get(s, 0), o)
            return
        m = re.match(r"^TF-(\d+)", idstr)
        if m:
            tf = max(tf, int(m.group(1)))

    for item_id in live_public_ids(root):
        add(item_id)
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
    nb, ne = todo_text.count(BEGIN), todo_text.count(END)
    if nb != 1 or ne != 1:
        raise ValueError(f"allocation sentinels must appear exactly once ({BEGIN} / {END}); "
                         f"found {nb} BEGIN and {ne} END")
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
    frozen_bad = frozen_floor_violations(floor, live_public_ids(REPO_ROOT))
    if frozen_bad:
        sys.stderr.write("FAIL: the FROZEN allocation invariant changed; frozen series take no new "
                         f"allocations: {'; '.join(frozen_bad)}\n")
        return 1
    try:
        new_todo = _splice(todo, render_block(tops, tf_max))
    except ValueError as exc:
        sys.stderr.write(f"FAIL: {exc}. Restore the number-allocation sentinels in TODO.md.\n")
        return 1
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
        def test_frozen_floor_immutable(self):
            # C3 (r21): frozen-series floor at its ceiling passes; a raise fails.
            self.assertEqual(frozen_floor_violations({5: 9, 6: 6, 7: 5}), [])
            self.assertTrue(frozen_floor_violations({5: 10, 6: 6, 7: 5}))

        def test_splice_requires_exactly_one_sentinel(self):
            # C4 (r21): a duplicate END sentinel must raise, not be accepted.
            good = f"a\n{BEGIN}\nX\n{END}\nb"
            self.assertIn("Y", _splice(good.replace("X", "Y"), "Y"))
            dup = f"a\n{BEGIN}\nX\n{END}\nb\n{END}\n"
            with self.assertRaises(ValueError):
                _splice(dup, "X")

        def test_render_shape(self):
            block = render_block({1: 30, 2: 32, 3: 248, 4: 31, 5: 9, 6: 6, 7: 5}, 3)
            self.assertIn("- **Next item number: 1.31.** (P1 / fix series)", block)
            self.assertIn("- **Next item number: 2.33.** (P2 / content series)", block)
            self.assertIn("- **Next item number: 3.249.** (P3 / tooling series)", block)
            self.assertIn("- **Next item number: 5.10.** (frozen; series 5 takes no new items)", block)
            self.assertIn("- **Next item number: TF-4.** (time-bounded follow-ups)", block)

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
