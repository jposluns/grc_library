#!/usr/bin/env python3
"""Sweep worker deliveries out of the per-worker file-drop outboxes into ONE orchestrator tray.

WHY. The exchange lays out a delivery at `<family>/outbox/<worker-id>/<order-id>.md`, so answering
"what is delivered and unprocessed?" means walking every family crossed with every minted worker id.
The orchestrator did exactly that by hand repeatedly on 2026-07-25 and still mis-reported the fleet
once. This tool collapses that to a single directory whose CONTENTS are the pending set, which is the
same location-IS-the-status property that makes the drop channel reliable: nothing is parsed and
nothing is inferred.

THE TWO TRAYS ARE DELIBERATELY SEPARATE (maintainer-directed 2026-07-25).
  inbox/              HIGH-PRIORITY issues a worker raises, read as soon as noticed.
  inbox/deliveries/   routine order results, processed at the next boundary.
Deliveries are the bulk traffic and issues are the thing that must never be missed, so mixing them
would destroy the property that makes the issue channel work, namely that the list is short and every
item on it matters.

FILENAME CARRIES BOTH IDS: `<worker-id>__<order-id>.md`. The result body also names its worker, but
the filename survives without parsing, and the orchestrator needs the worker id for the elevated-QA
trust window (keyed on worker plus model) and for independence routing, which is what forced the
re-issue of `validate-pr-1169` when a sweep's own author was asked to validate the fix to its finding.

TWO INDEPENDENT COMPLETENESS LAYERS, because they catch different failures (maintainer-directed
2026-07-25, defence in depth).

  1. ATOMIC RENAME (the writer's obligation). A worker writes `<order-id>.md.tmp` in the SAME
     directory as the destination and renames it into place. Same directory guarantees the same
     filesystem, which is what makes `rename(2)` atomic; a separate temp tree could sit on another
     mount and silently degrade to a copy. The `.tmp` SUFFIX matters and a dot prefix would not do:
     every reader in both repos globs `*.md`, and pathlib's `glob("*.md")` DOES match `.hidden.md`,
     so only a non-`.md` suffix is genuinely invisible. Verified, not assumed. Consequence: any
     `*.md` present in an outbox has all its bytes, so this tool needs no mtime quiet-period.
  2. END-OF-DELIVERY SENTINEL (the author's assertion). The last non-blank line must be
     `<!-- END OF DELIVERY -->`. Rename proves every byte arrived; the sentinel proves the author
     believed the work was finished. An agent that hits a token limit, writes what it has, and
     renames cleanly passes layer 1 and fails layer 2, and with agent workers that is the likelier
     truncation. An HTML comment is used so it is invisible when rendered, greppable, and will not
     collide with prose.

A FILE HELD BACK IS REPORTED, NEVER SILENTLY SKIPPED. A missing sentinel means the file stays put,
and staying put with no explanation is precisely the failure shape this project keeps meeting, where
silence reads as health (a stalled worker heartbeating, a saturation verdict naming unusable
capacity). Held-back files get their own labelled line in the report and are counted separately.

ADVISORY, like its sibling reconciliation tools: every reporting path exits 0, and only `--self-test`
can exit non-zero. Neither repo's CI can see this tree, so it is an orchestrator step and not a gate.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

FAMILIES = ("opus", "codex", "fable")
SENTINEL = "<!-- END OF DELIVERY -->"
TMP_SUFFIX = ".md.tmp"
NAME_JOIN = "__"
SKIP_NAMES = {"README.md"}


def compose_name(worker_id: str, order_id: str) -> str:
    """PURE. Build the tray filename carrying both ids.

    Kept separate and pure so the self-test pins the naming contract directly rather than inferring
    it from a filesystem effect, and so a future reader of the tray can split on NAME_JOIN.
    """
    return f"{worker_id}{NAME_JOIN}{order_id}.md"


def split_name(tray_name: str) -> tuple:
    """PURE. Recover (worker_id, order_id) from a tray filename, or (None, None).

    The inverse of compose_name, so the round trip is assertable. A worker id contains no `__` and an
    order id contains no `__`, so the first occurrence is the separator.
    """
    if not tray_name.endswith(".md") or NAME_JOIN not in tray_name:
        return None, None
    stem = tray_name[: -len(".md")]
    worker_id, _, order_id = stem.partition(NAME_JOIN)
    if not worker_id or not order_id:
        return None, None
    return worker_id, order_id


def has_sentinel(text: str) -> bool:
    """PURE. Does this delivery assert its own completeness?

    The check is on the LAST NON-BLANK line rather than "anywhere in the file", so a delivery that
    merely quotes or documents the sentinel mid-body (this tool's own docstring does exactly that,
    and so will the worker contract) is not thereby treated as complete.
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return bool(lines) and lines[-1] == SENTINEL


def plan_collection(facts: list, grandfather: bool = False) -> dict:
    """PURE. Decide what moves, what is held back, and why. No filesystem access.

    `facts` is a list of dicts, one per candidate file already discovered:
        {"family", "worker_id", "order_id", "name", "complete": bool, "tray_exists": bool}

    Returns {"move": [...], "held_no_sentinel": [...], "collision": [...]}.

    Purity is the point. Today's discriminability audit found that the ONE tool in this repo with
    zero undetectable-guard sites was the one whose decision logic was a pure function driven by
    constructed facts, and that the defective ones were those whose branches were only reachable
    through the filesystem. So the decision lives here and the executor below only obeys.
    """
    plan = {"move": [], "held_no_sentinel": [], "collision": [], "grandfathered": []}
    for f in facts:
        # Order matters and both properties below are load-bearing.
        # (a) Without grandfathering, INCOMPLETENESS takes precedence over collision: the actionable
        #     fact is that the writer has not finished, and the file is going nowhere either way.
        # (b) Collision is nonetheless checked BEFORE any move, INCLUDING a grandfathered one, so a
        #     migration can never overwrite a delivery already waiting in the tray.
        if not f["complete"] and not grandfather:
            plan["held_no_sentinel"].append(f)
        elif f["tray_exists"]:
            plan["collision"].append(f)
        elif not f["complete"]:
            plan["grandfathered"].append(f)
            plan["move"].append(f)
        else:
            plan["move"].append(f)
    return plan


def gather_facts(root: Path, tray: Path) -> list:
    """Discover candidate deliveries. Reads the filesystem; decides nothing."""
    facts = []
    for fam in FAMILIES:
        base = root / fam / "outbox"
        if not base.is_dir():
            continue
        for wdir in sorted(base.iterdir()):
            if not wdir.is_dir():
                continue
            # `orders/` holds the worker's copy of the order it served, not a delivery.
            for p in sorted(wdir.glob("*.md")):
                if p.name in SKIP_NAMES:
                    continue
                try:
                    text = p.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                order_id = p.stem
                facts.append({
                    "family": fam,
                    "worker_id": wdir.name,
                    "order_id": order_id,
                    "path": p,
                    "name": p.name,
                    "complete": has_sentinel(text),
                    "tray_exists": (tray / compose_name(wdir.name, order_id)).exists(),
                })
    return facts


def execute(plan: dict, root: Path, tray: Path, dry_run: bool) -> None:
    """Obey the plan. os.replace is atomic within a filesystem, and the whole tree is one mount."""
    tray.mkdir(parents=True, exist_ok=True)
    for f in plan["move"]:
        dest = tray / compose_name(f["worker_id"], f["order_id"])
        if dry_run:
            print(f"  WOULD COLLECT {f['family']}/{f['worker_id']}/{f['name']} -> {dest.name}")
            continue
        os.replace(f["path"], dest)
        print(f"  COLLECTED {dest.name}")
        # The order copy the worker served moves out with its result, so the outbox empties.
        served = root / f["family"] / "outbox" / f["worker_id"] / "orders" / f"{f['order_id']}.md"
        if served.is_file():
            done = root / "done" / "orders"
            done.mkdir(parents=True, exist_ok=True)
            target = done / f"{f['order_id']}.md"
            if not target.exists():
                os.replace(served, target)


def report(plan: dict, tray: Path, oneline: bool = False) -> None:
    """Report BOTH planes, always: the tray AND what is still sitting in worker outboxes.

    Reporting only the tray would under-count whenever the sweep has not run, and the sweep only
    runs while the orchestrator is alive, so between sessions results accumulate un-swept. A reader
    that saw only the tray would answer "nothing pending" with deliveries waiting, which is the
    exact bug class already fixed once in the saturation observable (#1157, which read one of two
    exchange planes) and still live in the scratch `list-workers`. So the pending figure below is
    the UNION, and its two components are named separately rather than summed into one number.
    """
    n_move, n_held = len(plan["move"]), len(plan["held_no_sentinel"])
    n_coll = len(plan["collision"])
    pending = sorted(tray.glob("*.md")) if tray.is_dir() else []
    unswept = n_held + n_coll
    if oneline:
        print(f"deliveries: {len(pending)} tray / {unswept} unswept"
              + (f" / {n_held} held" if n_held else ""))
        return
    print(f"collect-deliveries: {n_move} collected, {n_held} held back, {n_coll} collision(s); "
          f"{len(pending)} pending in the tray, {unswept} still in worker outboxes "
          f"(union is what is actually outstanding).")
    if n_held:
        # Never silent: a file that stays put without explanation is the failure shape where
        # silence reads as health.
        print(f"\nHELD BACK ({n_held}), no `{SENTINEL}` on the last non-blank line, so the writer "
              "may still be generating or was truncated. These are NOT collected and NOT lost:")
        for f in plan["held_no_sentinel"]:
            print(f"    {f['family']}/{f['worker_id']}/{f['name']}")
    if plan.get("grandfathered"):
        g = plan["grandfathered"]
        print(f"\nGRANDFATHERED ({len(g)}), collected DESPITE having no `{SENTINEL}`, because "
              "--grandfather-existing was passed. These predate the sentinel convention, so their "
              "completeness is ASSUMED rather than asserted by their author. Named individually "
              "because an assumption recorded as a fact is how a migration hides a truncated file:")
        for f in g:
            print(f"    {f['family']}/{f['worker_id']}/{f['name']}")
    if n_coll:
        print(f"\nCOLLISION ({n_coll}), a tray file of that name already exists, so nothing was "
              "overwritten. Process or rename the existing one first:")
        for f in plan["collision"]:
            print(f"    {f['family']}/{f['worker_id']}/{f['name']}")


def working_root(explicit: str | None) -> Path | None:
    for cand in (explicit, os.environ.get("GRC_WORKING"), "/home/grc/grc_working"):
        if cand and Path(cand).is_dir():
            return Path(cand)
    return None


def self_test() -> int:
    """Pin every decision branch, each on a DISTINCT observable.

    Written against the lesson from the 2026-07-25 discriminability audit, which found 28 self-test
    sites across 8 tools in this repo whose cases could not detect the removal of the guard they
    named, because each asserted a value that several branches shared. So no case here asserts a bare
    boolean or a count alone: each asserts WHICH bucket a file landed in and WHERE it ended up, and
    the pure planner is driven with constructed facts so every branch is reachable without a
    filesystem.
    """
    import contextlib
    import io
    import tempfile
    failures, total = [], [0]

    def check(name, got, want):
        total[0] += 1
        ok = got == want
        print(f"  {'PASS' if ok else 'FAIL'}: {name}" + ("" if ok else f" -> {got!r}, expected {want!r}"))
        if not ok:
            failures.append(name)

    # --- the pure naming contract, and its round trip ---
    check("compose_name carries both ids",
          compose_name("opus-20260725T122030Z-6443", "sweep-121"),
          "opus-20260725T122030Z-6443__sweep-121.md")
    check("split_name recovers both ids",
          split_name("opus-20260725T122030Z-6443__sweep-121.md"),
          ("opus-20260725T122030Z-6443", "sweep-121"))
    check("split_name round-trips a hyphenated order id",
          split_name(compose_name("codex-abc", "validate-pr-1169-b")),
          ("codex-abc", "validate-pr-1169-b"))
    # The empty-part guard, previously BLIND: the cases below covered a non-tray name and a wrong
    # extension, so disabling the guard changed nothing observable and it read as covered. Found by
    # tools/audit-selftest-discriminability.py. Without the guard these return ("", "x") and
    # ("x", ""), and a caller would then use an empty worker id, which the saturation tool's
    # phantom-pending retirement now depends on being well-formed.
    check("split_name rejects an empty worker id", split_name("__x.md"), (None, None))
    check("split_name rejects an empty order id", split_name("x__.md"), (None, None))
    check("split_name rejects a non-tray filename", split_name("sweep-121.md"), (None, None))
    check("split_name rejects a non-md file", split_name("w__o.txt"), (None, None))

    # --- the sentinel check, on the LAST non-blank line specifically ---
    check("sentinel present on the last non-blank line", has_sentinel(f"body\n\n{SENTINEL}\n"), True)
    check("sentinel absent", has_sentinel("body\nmore body\n"), False)
    check("sentinel mid-body does NOT count as complete",
          has_sentinel(f"body\n{SENTINEL}\nstill writing...\n"), False)
    check("an empty file is not complete", has_sentinel(""), False)
    check("trailing blank lines do not defeat the sentinel",
          has_sentinel(f"body\n{SENTINEL}\n\n\n"), True)

    # --- the pure planner: one case per bucket, asserting WHICH bucket ---
    def fact(order_id, complete=True, tray_exists=False):
        return {"family": "opus", "worker_id": "w1", "order_id": order_id,
                "name": f"{order_id}.md", "complete": complete, "tray_exists": tray_exists}

    p = plan_collection([fact("a"), fact("b", complete=False), fact("c", tray_exists=True)])
    check("planner routes a complete, non-colliding file to move",
          [f["order_id"] for f in p["move"]], ["a"])
    check("planner holds back a file with no sentinel",
          [f["order_id"] for f in p["held_no_sentinel"]], ["b"])
    check("planner reports a collision instead of overwriting",
          [f["order_id"] for f in p["collision"]], ["c"])
    check("an incomplete file is held back even when it would NOT collide",
          plan_collection([fact("d", complete=False, tray_exists=False)])["held_no_sentinel"][0]["order_id"],
          "d")
    check("incompleteness takes precedence over collision",
          [b for b, fs in plan_collection([fact("e", complete=False, tray_exists=True)]).items() if fs],
          ["held_no_sentinel"])

    # the one-time migration path, and its two safety properties
    gp = plan_collection([fact("g1", complete=False)], grandfather=True)
    check("grandfathering collects a sentinel-less file",
          [f["order_id"] for f in gp["move"]], ["g1"])
    check("and names it as grandfathered, not as a normal collect",
          [f["order_id"] for f in gp["grandfathered"]], ["g1"])
    check("grandfathering still refuses to overwrite a tray file",
          [f["order_id"] for f in
           plan_collection([fact("g2", complete=False, tray_exists=True)], grandfather=True)["collision"]],
          ["g2"])
    check("grandfathering a complete file does not mark it grandfathered",
          plan_collection([fact("g3")], grandfather=True)["grandfathered"], [])

    # report() was ENTIRELY UNTESTED: all four of its branches were genuine coverage gaps, found by
    # an independent control-bracketed audit (mutation-audit-todays-three-tools). It is the function
    # that tells the operator what was held back and why, so an untested report is how a held-back
    # file becomes a silent skip, which is the exact failure this tool's design forbids. Captured
    # rather than eyeballed, so each branch is pinned by an assertion on its output.
    def _report_text(plan, tray_path, oneline=False):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            report(plan, tray_path, oneline)
        return buf.getvalue()

    with tempfile.TemporaryDirectory() as td2:
        empty_tray = Path(td2) / "tray"
        held_plan = {"move": [], "held_no_sentinel": [fact("h1", complete=False)],
                     "collision": [], "grandfathered": []}
        out = _report_text(held_plan, empty_tray)
        check("report names a held-back file individually, never only a count",
              "h1.md" in out, True)
        check("report explains WHY a file was held back", SENTINEL in out, True)
        check("report states the file is not lost", "NOT collected and NOT lost" in out, True)

        coll_plan = {"move": [], "held_no_sentinel": [], "collision": [fact("c1")],
                     "grandfathered": []}
        out = _report_text(coll_plan, empty_tray)
        check("report names a collision and says nothing was overwritten",
              "c1.md" in out and "overwritten" in out, True)

        gf_plan = {"move": [fact("g1", complete=False)], "held_no_sentinel": [],
                   "collision": [], "grandfathered": [fact("g1", complete=False)]}
        out = _report_text(gf_plan, empty_tray)
        check("report names each grandfathered file, since completeness is ASSUMED there",
              "g1.md" in out and "GRANDFATHERED" in out, True)

        quiet_plan = {"move": [], "held_no_sentinel": [], "collision": [], "grandfathered": []}
        out = _report_text(quiet_plan, empty_tray)
        check("report is silent about held-back files when there are none",
              "HELD BACK" in out, False)

        # --oneline is the statusline form: exactly one line, and it must still carry the unswept count
        one = _report_text(held_plan, empty_tray, oneline=True)
        check("oneline emits exactly one line", len(one.strip().splitlines()), 1)
        check("oneline still surfaces the held count", "held" in one, True)

    # --- end to end on a real tree, including the .tmp invisibility that layer 1 relies on ---
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        wdir = root / "opus" / "outbox" / "opus-w1"
        (wdir / "orders").mkdir(parents=True)
        tray = root / "inbox" / "deliveries"
        (wdir / "done-order.md").write_text(f"result body\n\n{SENTINEL}\n")
        (wdir / "orders" / "done-order.md").write_text("the order it served")
        (wdir / "truncated.md").write_text("half a result, no marker\n")
        (wdir / f"in-flight{TMP_SUFFIX}").write_text("partial")
        (wdir / "README.md").write_text(f"not a delivery\n{SENTINEL}\n")

        facts = gather_facts(root, tray)
        seen = sorted(f["order_id"] for f in facts)
        check("gather ignores a .tmp file (layer 1: wrong suffix, invisible to *.md)",
              "in-flight" in seen, False)
        check("gather ignores README.md", "README" in seen, False)
        check("gather finds exactly the two real candidates", seen, ["done-order", "truncated"])

        plan = plan_collection(facts)
        execute(plan, root, tray, dry_run=False)
        check("the complete delivery landed in the tray under its composed name",
              (tray / "opus-w1__done-order.md").is_file(), True)
        check("the truncated delivery STAYED in the outbox",
              (wdir / "truncated.md").is_file(), True)
        check("the truncated delivery did NOT reach the tray",
              (tray / "opus-w1__truncated.md").exists(), False)
        check("the served order copy moved to done/orders",
              (root / "done" / "orders" / "done-order.md").is_file(), True)
        check("the collected delivery left the outbox",
              (wdir / "done-order.md").exists(), False)
        check("tray content survives the move byte-for-byte",
              (tray / "opus-w1__done-order.md").read_text(), f"result body\n\n{SENTINEL}\n")

        # idempotency: a second sweep must not duplicate, lose, or overwrite
        facts2 = gather_facts(root, tray)
        plan2 = plan_collection(facts2)
        execute(plan2, root, tray, dry_run=False)
        check("a second sweep collects nothing new", len(plan2["move"]), 0)
        check("a second sweep still holds back the truncated file",
              [f["order_id"] for f in plan2["held_no_sentinel"]], ["truncated"])
        check("the tray still holds exactly one delivery",
              sorted(p.name for p in tray.glob("*.md")), ["opus-w1__done-order.md"])

        # the sentinel arriving later is what releases the held file, with no other change
        (wdir / "truncated.md").write_text(f"half a result, no marker\n\n{SENTINEL}\n")
        plan3 = plan_collection(gather_facts(root, tray))
        execute(plan3, root, tray, dry_run=False)
        check("a held file is released once its sentinel appears",
              (tray / "opus-w1__truncated.md").is_file(), True)

        # An order id already archived in done/orders must not be clobbered by a re-serve.
        # Added after a mutation sweep of THIS self-test showed the guard was unreachable: no case
        # exercised a pre-existing done/orders entry, so neutralizing it changed nothing observable.
        (root / "done" / "orders").mkdir(parents=True, exist_ok=True)
        (root / "done" / "orders" / "reserved.md").write_text("the FIRST archived order copy")
        (wdir / "reserved.md").write_text(f"a re-serve result\n\n{SENTINEL}\n")
        (wdir / "orders" / "reserved.md").write_text("a SECOND order copy, must not clobber")
        plan5 = plan_collection(gather_facts(root, tray))
        execute(plan5, root, tray, dry_run=False)
        check("a re-served order does not clobber the archived order copy",
              (root / "done" / "orders" / "reserved.md").read_text(),
              "the FIRST archived order copy")
        check("the re-serve result itself still collected",
              (tray / "opus-w1__reserved.md").is_file(), True)

        # a genuine collision is refused rather than clobbering the pending tray file
        (wdir / "done-order.md").write_text(f"a DIFFERENT result, same order id\n\n{SENTINEL}\n")
        plan4 = plan_collection(gather_facts(root, tray))
        execute(plan4, root, tray, dry_run=False)
        check("a colliding delivery is refused, not collected",
              [f["order_id"] for f in plan4["collision"]], ["done-order"])
        check("the pre-existing tray file was NOT overwritten",
              (tray / "opus-w1__done-order.md").read_text(), f"result body\n\n{SENTINEL}\n")

    if failures:
        print(f"\nself-test: FAILED ({len(failures)} of {total[0]})")
        return 1
    print(f"\nself-test: {total[0]}/{total[0]} passed")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", help="file-drop root (default $GRC_WORKING or the VM path)")
    ap.add_argument("--dry-run", action="store_true", help="report what would move; change nothing")
    ap.add_argument("--grandfather-existing", action="store_true",
                    help="ONE-TIME migration: collect files that lack the end-of-delivery sentinel "
                         "because they predate the convention. Each is named in the report; "
                         "completeness is assumed, not asserted. Not for routine use.")
    ap.add_argument("--oneline", action="store_true",
                    help="one-line form for the console statusline")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    root = working_root(a.root)
    if root is None:
        print("collect-deliveries: no file-drop root resolved; nothing to do (no-op).")
        return 0
    tray = root / "inbox" / "deliveries"
    plan = plan_collection(gather_facts(root, tray), a.grandfather_existing)
    # --oneline is the STATUSLINE form, so it is read-only AND silent apart from its single line.
    # It previously routed through execute() in dry-run mode, which prints a WOULD COLLECT line per
    # candidate, so the statusline emitted N+1 lines instead of 1. The console is the maintainer's
    # live window and extra lines there are the specific harm the no-diffs-in-chat convention names.
    if not a.oneline:
        execute(plan, root, tray, a.dry_run)
    report(plan, tray, a.oneline)
    return 0


if __name__ == "__main__":
    sys.exit(main())
