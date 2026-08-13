#!/usr/bin/env python3
"""Generate the `## Number allocation` counter block in ``TODO.md`` from the live
union of allocated PUBLIC backlog ids, so a human can never hand-set a counter below
the highest-used number (the recycle hazard gate 78 also guards, defence in depth).

WHAT IS GENERATED. Only the seven ``- **Next item number: X.**`` counter bullets,
between the sentinels ``<!-- BEGIN-GENERATED number-allocation -->`` and
``<!-- END-GENERATED number-allocation -->``. The surrounding prose (the permanence
note and the 3.x counter-less note) is hand-maintained and untouched.

THE PUBLIC NAMESPACE. Public backlog ids are bare ``N.M`` / ``TF-n`` (NOT the ``P-N.M``
private namespace). One shared public namespace spans THREE sources, so the union is:
  1. ``TODO.md`` index-row ids (the live public items).
  2. ``### <id>`` headings in ``TODO-REFERENCE.md`` (live detail) and ``P-TODO.md``
     (migrated items keep their bare public ``N.M``; the private ``P-N.M`` ids are excluded).
  3. Retired PUBLIC ids in ``grc_library_private/.working/DONE.md`` ``### `` headings
     (some series' highest allocated id, e.g. 2.32, exists ONLY as a retired DONE id).

next(series) = max(top-level ordinal of any public id in that series across the union) + 1.
Series 5/6/7 are FROZEN (no new draws) but still render a ``next`` line tagged frozen;
the 3.x series has NO counter line (a hand-maintained prose note handles it).

DONE-EXTRACTION FRAGILITY (documented, non-blocking; surfaced for review 2026-08-13).
DONE headings embed ids in free prose (``### PR #N: <summary>``), so extraction strips
the ``PR #N`` token and the ``P-N.M`` private ids, then reads bare ``N.M`` / ``TF-n``.
A spurious id-shaped token in a DONE summary could OVER-count a counter. That is SAFE
for the recycle invariant (a too-high counter only SKIPS a number, never reuses one) and
the generator is authoritative (regenerate on drift), with gate 78 as the recycle backstop.
The self-test anchors the algorithm to the current committed block as a reality fixture.

Usage:
  python3 tools/build-todo-number-allocation.py            # regenerate in place
  python3 tools/build-todo-number-allocation.py --check    # exit 1 on drift (CI)
  python3 tools/build-todo-number-allocation.py --self-test # unit self-check
"""
import argparse
import re
import sys
from pathlib import Path

from lint_common import REPO_ROOT, resolve_sibling  # noqa: E402

BEGIN = "<!-- BEGIN-GENERATED number-allocation -->"
END = "<!-- END-GENERATED number-allocation -->"

# Active (draw a new number) and frozen (render but draw nothing) series, with the
# label each counter line carries. The 3.x series is deliberately absent (prose note).
ACTIVE = [(1, "P1 / fix series"), (2, "P2 / content series"), (4, "P4 / adopter series")]
FROZEN = [5, 6, 7]

# A bare public id token: N.M (optionally deeper), NOT preceded by a letter/hyphen (so
# ``P-3.2`` and a word-joined figure never match) and NOT followed by a word char.
PUBLIC_ID = re.compile(r"(?<![\w.-])(\d+)\.(\d+)(?![\w.])")
TF_ID = re.compile(r"(?<![\w-])TF-(\d+)\b")
# ``### <id> ...`` detail/backlog headings (bare public or TF; P- excluded downstream).
HEADING_ID = re.compile(r"^### ((?:P-)?\d+(?:\.\d+)+[a-z]?|TF-\d+)\b")


def _index_ids(todo_text):
    """Public ids from TODO.md index rows via the shared parser."""
    import lint_common
    return lint_common.todo_index_ids(todo_text)


def collect_public(tops, tf_max, text, headings_only=False):
    """Fold the public ids found in ``text`` into ``tops`` (series -> max ordinal) and
    ``tf_max``. ``headings_only`` restricts to ``### `` heading lines (for reference /
    P-TODO, where non-heading prose must not seed the counters)."""
    if headings_only:
        for ln in text.split("\n"):
            m = HEADING_ID.match(ln)
            if not m:
                continue
            hid = m.group(1)
            if hid.startswith("P-"):
                continue  # private namespace
            mm = re.match(r"^(\d+)\.(\d+)", hid)
            if mm:
                s, o = int(mm.group(1)), int(mm.group(2))
                tops[s] = max(tops.get(s, 0), o)
            tm = re.match(r"^TF-(\d+)", hid)
            if tm:
                tf_max = max(tf_max, int(tm.group(1)))
        return tf_max
    # free-text mode (DONE headings, pre-stripped of PR#/P- tokens by the caller)
    for s, o in PUBLIC_ID.findall(text):
        s, o = int(s), int(o)
        if 1 <= s <= 7:
            tops[s] = max(tops.get(s, 0), o)
    for n in TF_ID.findall(text):
        tf_max = max(tf_max, int(n))
    return tf_max


def compute_counters(root=None):
    """Return (tops, tf_max) for the public namespace union. ``root`` overrides the
    grc_library repo root (for the self-test); DONE is read from the private sibling."""
    root = Path(root) if root else REPO_ROOT
    tops, tf_max = {}, 0

    todo = (root / "TODO.md").read_text(errors="replace")
    for i in _index_ids(todo):
        m = re.match(r"^(\d+)\.(\d+)", i)
        if m:
            s, o = int(m.group(1)), int(m.group(2))
            tops[s] = max(tops.get(s, 0), o)
        tm = re.match(r"^TF-(\d+)", i)
        if tm:
            tf_max = max(tf_max, int(tm.group(1)))

    ref = root / "TODO-REFERENCE.md"
    if ref.is_file():
        tf_max = collect_public(tops, tf_max, ref.read_text(errors="replace"), headings_only=True)

    # private sibling: P-TODO bare-id headings + DONE retired public ids
    private = resolve_sibling("private")
    if private is not None:
        ptodo = private / "P-TODO.md"
        if ptodo.is_file():
            ptext = ptodo.read_text(errors="replace")
            tf_max = collect_public(tops, tf_max, ptext, headings_only=True)
            # P-TODO also carries `- **TF-n` bullets (not ### headings)
            for n in TF_ID.findall(ptext):
                tf_max = max(tf_max, int(n))
        done = private / ".working" / "DONE.md"
        if done.is_file():
            for ln in done.read_text(errors="replace").split("\n"):
                if not ln.startswith("### "):
                    continue
                body = re.sub(r"PR #\d+", "", ln)           # drop the PR-number token
                body = re.sub(r"\bP-\d+(?:\.\d+)+", "", body)  # drop private ids
                tf_max = collect_public(tops, tf_max, body)
    return tops, tf_max


def render_block(tops, tf_max):
    """The generated counter block (the 7 bullet lines), without the sentinels."""
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
    """Replace the text between the sentinels with ``block``; return the new TODO text.
    Raises if the sentinels are absent or malformed."""
    if BEGIN not in todo_text or END not in todo_text:
        raise ValueError(f"allocation sentinels not found ({BEGIN} / {END})")
    pre, rest = todo_text.split(BEGIN, 1)
    _, post = rest.split(END, 1)
    return f"{pre}{BEGIN}\n{block}\n{END}{post}"


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="exit 1 on drift, do not write")
    ap.add_argument("--self-test", action="store_true", help="run the unit self-check")
    args = ap.parse_args(argv[1:])
    if args.self_test:
        return self_test()

    # The counter union needs DONE.md (retired public ids, e.g. series 2's highest),
    # which lives in the private sibling. Absent it (CI, an adopter clone) the union is
    # incomplete, so --check cannot verify and regenerate must not write a wrong block:
    # no-op OK on --check (enforcement is maintainer-local, at the pre-push guard),
    # skip on regenerate. This mirrors the other sibling-reaching tools' graceful no-op.
    if resolve_sibling("private") is None:
        if args.check:
            print("OK: private sibling absent; number-allocation --check is maintainer-local (skipped).")
            return 0
        print("SKIP: private sibling absent; cannot regenerate without DONE.md (maintainer-local).")
        return 0

    todo_path = REPO_ROOT / "TODO.md"
    todo = todo_path.read_text(errors="replace")
    tops, tf_max = compute_counters()
    new_todo = _splice(todo, render_block(tops, tf_max))

    if args.check:
        if new_todo != todo:
            sys.stderr.write(
                "FAIL: TODO.md `## Number allocation` block is out of sync with the live "
                "backlog union. Regenerate: python3 tools/build-todo-number-allocation.py\n")
            return 1
        print("OK: TODO.md number-allocation block is in sync.")
        return 0
    todo_path.write_text(new_todo)
    print("Regenerated TODO.md number-allocation block.")
    return 0


def self_test():
    import unittest

    class T(unittest.TestCase):
        def test_render_shape(self):
            block = render_block({1: 30, 2: 32, 4: 31, 5: 9, 6: 6, 7: 5}, 3)
            self.assertIn("- **Next item number: 1.31.** (P1 / fix series)", block)
            self.assertIn("- **Next item number: 2.33.** (P2 / content series)", block)
            self.assertIn("- **Next item number: 4.32.** (P4 / adopter series)", block)
            self.assertIn("- **Next item number: 5.10.** (frozen; series 5 takes no new items)", block)
            self.assertIn("- **Next item number: TF-4.** (time-bounded follow-ups)", block)
            self.assertNotIn("Next item number: 3.", block)  # no 3.x counter line

        def test_public_id_excludes_private_and_versions(self):
            tops, tf = {}, 0
            tf = collect_public(tops, tf, "closed P-3.99 and 2.5; version 1.17.94; date 2026.08", False)
            self.assertEqual(tops.get(2), 5)      # 2.5 (clean 2-part) counted
            self.assertNotIn(3, tops)             # P-3.99 excluded (private namespace)
            self.assertNotIn(1, tops)             # 1.17.94 excluded (3-part version, not a 2-part id)

        def test_headings_only_skips_prose(self):
            tops, tf = {}, 0
            text = "### 4.31 Real item\nprose mentioning 4.99 not a heading\n### P-1.5 private\n"
            tf = collect_public(tops, tf, text, headings_only=True)
            self.assertEqual(tops.get(4), 31)     # heading counted
            self.assertNotIn(1, tops)             # P-1.5 heading excluded (private)
            self.assertNotEqual(tops.get(4), 99)  # prose 4.99 NOT counted in heading mode

        def test_splice_roundtrip(self):
            todo = f"pre\n{BEGIN}\nOLD\n{END}\npost\n"
            out = _splice(todo, "NEW1\nNEW2")
            self.assertEqual(out, f"pre\n{BEGIN}\nNEW1\nNEW2\n{END}\npost\n")

        def test_splice_missing_sentinel_raises(self):
            with self.assertRaises(ValueError):
                _splice("no sentinels here", "X")

        def test_reproduces_committed_block(self):
            """Reality anchor: the live union must regenerate the CURRENTLY committed
            block byte-for-byte (proven at build time 2026-08-13). Needs the private
            sibling (DONE.md); skipped where it is absent (CI, an adopter clone)."""
            if resolve_sibling("private") is None:
                self.skipTest("private sibling absent; reality-anchor is maintainer-local")
            tops, tf_max = compute_counters()
            block = render_block(tops, tf_max)
            todo = (REPO_ROOT / "TODO.md").read_text()
            if BEGIN in todo:
                cur = todo.split(BEGIN, 1)[1].split(END, 1)[0].strip("\n")
                self.assertEqual(block, cur,
                                 "generated block drifted from the committed allocation block")

    runner = unittest.TextTestRunner(verbosity=1)
    ok = runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(T)).wasSuccessful()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
