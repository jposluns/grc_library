#!/usr/bin/env python3
"""Sweep worker deliveries out of the per-worker file-drop outboxes into ONE orchestrator tray.

WHY. The exchange lays out a delivery at `<family>/outbox/<worker-id>/<order-id>.md`, so answering
"what is delivered and unprocessed?" means walking every family crossed with every minted worker id.
The orchestrator once did exactly that by hand repeatedly and still mis-reported the fleet
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
re-issue of a per-PR validation order when a sweep's own author was asked to validate the fix to its finding.

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
silence reads as health (a stalled worker still heartbeating while no longer working). Held-back files get their own labelled line in the report and are counted separately.

STICKY-OUTBOX FALLBACK. An outbox directory can carry the sticky bit with delivery files owned by
another account; such a directory permits group members to read and create files but forbids
renaming or unlinking a file they do not own, so the atomic-move collection fails with
PermissionError even though every byte is readable. On that error the sweep falls back to a durable
COPY into the tray (written under a non-.md, pid-suffixed partial name, size-verified, then renamed
into place within the tray) plus a `<name>.collected` marker beside the source. The marker proves a
copy landed in the tray, NOT that the source was removed: the outbox retains the original until its
owner cleans it, and the scanner skips any delivery carrying a sibling marker so nothing is ever
collected twice. If the marker write itself fails AFTER the copy landed, the outcome is recorded as
COPIED+UNMARKED, the honest state (tray copy complete, idempotency marker missing), and the next
sweep SELF-HEALS it: a marker-less source whose same-name tray file is byte-identical routes to a
REMARK step that writes only the missing marker, no copy; a differing twin is a genuine collision
and still refuses.

ADVISORY, like its sibling reconciliation tools: every reporting path exits 0 EXCEPT three cases,
which exit non-zero: `--self-test` with any failing case; a FAILED per-file collection outcome (a
planned file that neither moved nor copied); and a COPIED+UNMARKED outcome (the copy landed but the
marker write failed, so nothing is lost yet the state needs the operator's eye until the next
sweep's remark self-heal). One file's failure never aborts the sweep; the remaining planned files
still process. Neither repo's CI can see this tree, so it is an orchestrator step and not a gate.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

FAMILIES = ("opus", "codex", "fable")
SENTINEL = "<!-- END OF DELIVERY -->"
TMP_SUFFIX = ".md.tmp"
MARKER_SUFFIX = ".collected"
PARTIAL_SUFFIX = ".partial"
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
        {"family", "worker_id", "order_id", "name", "complete": bool, "tray_exists": bool,
         "marker_exists": bool, "tray_identical": bool}

    Returns {"move": [...], "held_no_sentinel": [...], "collision": [...], "grandfathered": [...],
    "already_collected": [...], "remark": [...]}.

    Purity is the point. Today's discriminability audit found that the ONE tool in this repo with
    zero undetectable-guard sites was the one whose decision logic was a pure function driven by
    constructed facts, and that the defective ones were those whose branches were only reachable
    through the filesystem. So the decision lives here and the executor below only obeys.
    """
    plan = {"move": [], "held_no_sentinel": [], "collision": [], "grandfathered": [],
            "already_collected": [], "remark": []}
    for f in facts:
        # Order matters and the properties below are load-bearing.
        # (0) A sibling `.collected` marker takes precedence over EVERYTHING: it is only ever
        #     written after a size-verified copy landed in the tray, so the delivery is collected
        #     and must never be re-collected (idempotency). Residue, stated where the marker is
        #     honoured: the marker proves the copy landed, not that the source was removed; the
        #     outbox retains the original until its owner cleans it. And a marker outlives its
        #     source's CONTENT: a same-path rewrite after collection is skipped here, so
        #     owner-side hygiene (the P-3.235 class) is the remedy for a marked outbox, never
        #     this sweep.
        # (0a) INCOMPLETENESS outranks remark ON ROUTINE RUNS: routinely this tool only copies
        #     sentinel-complete files, so a byte-identical twin of a sentinel-LESS source cannot
        #     be this tool's work; freezing a still-writing file under a marker would mask its
        #     completed form. A held file whose writer finishes collects normally on a later
        #     sweep. Under --grandfather-existing this precedence deliberately inverts: the flag
        #     ASSUMES completeness for sentinel-less files (one-time migration, per its help
        #     text), so an identical twin there reads as a prior grandfathered copy whose marker
        #     write failed, and remark is the correct self-heal.
        # (0b) A marker-LESS COMPLETE source whose same-name tray file is BYTE-IDENTICAL routes to remark:
        #     an earlier copy landed but its marker write failed (COPIED+UNMARKED), so the only
        #     missing artefact is the marker itself. Residue, stated where remark is honoured:
        #     byte-equality proves the tray copy is the same artifact, so writing the marker is
        #     safe; a DIFFERING twin is a genuine collision and still refuses below.
        # (a) Without grandfathering, INCOMPLETENESS takes precedence over collision: the actionable
        #     fact is that the writer has not finished, and the file is going nowhere either way.
        # (b) Collision is nonetheless checked BEFORE any move, INCLUDING a grandfathered one, so a
        #     migration can never overwrite a delivery already waiting in the tray.
        if f.get("marker_exists"):
            plan["already_collected"].append(f)
        elif not f["complete"] and not grandfather:
            plan["held_no_sentinel"].append(f)
        elif f.get("tray_exists") and f.get("tray_identical"):
            plan["remark"].append(f)
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
                tray_file = tray / compose_name(wdir.name, order_id)
                tray_exists = tray_file.exists()
                tray_identical = False
                if tray_exists:
                    # Observation only; the planner decides. Byte-compare the source against its
                    # same-name tray file so a marker-less survivor of a marker-write failure is
                    # recognizable as already collected (the remark self-heal) while a genuinely
                    # different twin stays a collision.
                    try:
                        tray_identical = tray_file.read_bytes() == p.read_bytes()
                    except OSError:
                        tray_identical = False
                facts.append({
                    "family": fam,
                    "worker_id": wdir.name,
                    "order_id": order_id,
                    "path": p,
                    "name": p.name,
                    "complete": has_sentinel(text),
                    "tray_exists": tray_exists,
                    "tray_identical": tray_identical,
                    # A `.collected` name never matches the *.md glob, so a marker is never itself
                    # gathered as a delivery; this key only records whether THIS delivery has one.
                    "marker_exists": p.with_name(p.name + MARKER_SUFFIX).exists(),
                })
    return facts


def durable_copy(src: Path, dest: Path) -> None:
    """Durable copy for a rename the source directory forbids: partial, size-verify, promote.

    The copy lands under a non-.md partial name (invisible to every *.md reader, the same suffix
    reasoning as TMP_SUFFIX), is size-verified against the source, and is renamed into place
    WITHIN the destination directory (same directory, so atomic). The partial name carries this
    process's pid, so two concurrent collectors each own their temp file and neither can
    overwrite or unlink the other's; the failure cleanup below targets only its own partial. A
    stale FOREIGN partial (a dead collector's leftover) is invisible to every *.md reader and is
    overwritten only by a process holding the same pid or removed by owner-side hygiene (the
    P-3.235 class); it never corrupts a later sweep. Shared by the delivery copy fallback and the
    served-order archive fallback so both get the same partial+verify+promote guarantees.
    """
    partial = dest.with_name(f"{dest.name}{PARTIAL_SUFFIX}.{os.getpid()}")
    try:
        shutil.copy2(src, partial)
        if partial.stat().st_size != src.stat().st_size:
            raise OSError(f"partial copy of {src.name}: size mismatch, copy discarded")
        os.replace(partial, dest)
    except OSError:
        partial.unlink(missing_ok=True)
        raise


def write_marker(src: Path, dest: Path) -> None:
    """Write the `.collected` idempotency marker beside a source whose copy landed in the tray.

    Called only AFTER a size-verified tray copy exists (durable_copy, or the remark self-heal on
    a byte-identical twin), so the marker never exists without a complete tray copy. Residue
    (guard-inputs discipline, stated at the point of use): the marker proves a size-verified copy
    landed in the tray, NOT that the source was removed; the outbox retains the original until
    its owner cleans it. The marker also outlives the source's CONTENT, so a same-path rewrite
    after collection is skipped by later sweeps; owner-side hygiene (the P-3.235 class) is the
    remedy for that residue.
    """
    marker = src.with_name(src.name + MARKER_SUFFIX)
    marker.write_text(
        f"copied to tray as {dest.name}; the source directory forbids rename by a non-owner, so "
        "the original is retained here until its owner cleans it. This marker proves the copy "
        "landed in the tray, not that the source was removed.\n", encoding="utf-8")


def archive_served_order(root: Path, f: dict) -> None:
    """Move the order copy the worker served to done/orders, so the outbox empties.

    Best-effort by design, and EVERY failure in here is a NOTE, never an abort: the delivery
    itself already reached the tray before this runs, so nothing in this function may take the
    sweep down. That includes the done-tree mkdir, which previously sat outside the per-file
    error handling and could abort the whole sweep on one bad archival. The same
    sticky-directory class that forbids the delivery rename can forbid this one; the fallback is
    the same durable partial+verify+promote copy as the delivery path (durable_copy), the
    pre-existing-target guard keeps a later sweep from re-copying, and the leftover original is
    the same stated residue as a marker-retained delivery.
    """
    served = root / f["family"] / "outbox" / f["worker_id"] / "orders" / f"{f['order_id']}.md"
    if not served.is_file():
        return
    done = root / "done" / "orders"
    try:
        done.mkdir(parents=True, exist_ok=True)
        target = done / f"{f['order_id']}.md"
        if target.exists():
            return
    except OSError as exc:
        print(f"  NOTE: order copy for {f['order_id']} not archived ({exc}); "
              "the delivery itself is collected.")
        return
    try:
        os.replace(served, target)
    except PermissionError:
        try:
            durable_copy(served, target)
        except OSError as exc:
            print(f"  NOTE: order copy for {f['order_id']} not archived ({exc}); "
                  "the delivery itself is collected.")
            return
        print(f"  NOTE: order copy for {f['order_id']} was copied, not moved (the outbox "
              "forbids the rename); the owner retains the original.")
    except OSError as exc:
        print(f"  NOTE: order copy for {f['order_id']} not archived ({exc}); "
              "the delivery itself is collected.")


def needs_attention(outcomes: list) -> bool:
    """PURE. Name the outcomes that make the run exit non-zero.

    FAILED is a real loss of sweep completeness: a planned file neither moved nor copied.
    COPIED+UNMARKED lost nothing (the copy landed, size-verified) but the idempotency marker is
    missing, so the state needs the operator's eye until the next sweep's remark self-heal
    restores the marker. Everything else (MOVED, COPIED+MARKED, REMARKED) is a clean outcome.
    """
    return any(o["outcome"] in ("FAILED", "COPIED+UNMARKED") for o in outcomes)


def execute(plan: dict, root: Path, tray: Path, dry_run: bool) -> list:
    """Obey the plan; return one outcome per acted-on file: MOVED, COPIED+MARKED,
    COPIED+UNMARKED, REMARKED, or FAILED.

    os.replace is atomic within a filesystem and the whole tree is one mount, so the atomic move
    is the default path. A sticky-bit outbox owned by another account forbids renaming that
    account's files, so PermissionError falls back to durable_copy plus write_marker (module
    docstring). The marker write runs in its OWN try: a marker failure after a landed copy is
    recorded COPIED+UNMARKED, the honest state, never FAILED, which would falsely claim nothing
    was copied and then read as a permanent collision on every later sweep. Every per-file
    failure is caught, reported, and recorded so ONE bad file never aborts the rest of the
    sweep; the caller derives the exit code from the outcomes via needs_attention.
    """
    tray.mkdir(parents=True, exist_ok=True)
    outcomes = []
    for f in plan["move"]:
        dest = tray / compose_name(f["worker_id"], f["order_id"])
        if dry_run:
            print(f"  WOULD COLLECT {f['family']}/{f['worker_id']}/{f['name']} -> {dest.name}")
            continue
        try:
            os.replace(f["path"], dest)
            outcome, reason = "MOVED", None
            print(f"  COLLECTED {dest.name}")
        except PermissionError:
            try:
                durable_copy(f["path"], dest)
            except OSError as exc:
                outcomes.append({"name": f["name"], "family": f["family"],
                                 "worker_id": f["worker_id"], "outcome": "FAILED",
                                 "reason": str(exc)})
                print(f"  FAILED {f['family']}/{f['worker_id']}/{f['name']}: {exc} "
                      "(left in place; the sweep continues)")
                continue
            # The copy has landed; the marker write gets its OWN try so its failure is never
            # conflated with a failed copy (which would misread as a permanent collision later).
            try:
                write_marker(f["path"], dest)
                outcome, reason = "COPIED+MARKED", None
                print(f"  COLLECTED {dest.name} (copied; source retained under its "
                      f"{MARKER_SUFFIX} marker)")
            except OSError as exc:
                outcome, reason = "COPIED+UNMARKED", str(exc)
                print(f"  COLLECTED {dest.name} (copied), but the {MARKER_SUFFIX} marker write "
                      f"failed: {exc}. The copy landed and nothing is lost; the missing marker "
                      "self-heals on the next sweep (remark).")
        except OSError as exc:
            outcomes.append({"name": f["name"], "family": f["family"],
                             "worker_id": f["worker_id"], "outcome": "FAILED",
                             "reason": str(exc)})
            print(f"  FAILED {f['family']}/{f['worker_id']}/{f['name']}: {exc} "
                  "(left in place; the sweep continues)")
            continue
        outcomes.append({"name": dest.name, "family": f["family"],
                         "worker_id": f["worker_id"], "outcome": outcome, "reason": reason})
        # The order copy the worker served moves out with its result, so the outbox empties.
        archive_served_order(root, f)
    # The self-heal half of the marker-failure story: a source whose same-name tray file is
    # byte-identical needs ONLY its missing marker written, never a second copy. Residue as
    # stated in plan_collection (0b): byte-equality is what makes the marker write safe here.
    for f in plan.get("remark", []):
        dest = tray / compose_name(f["worker_id"], f["order_id"])
        if dry_run:
            print(f"  WOULD REMARK {f['family']}/{f['worker_id']}/{f['name']} "
                  "(byte-identical tray twin; only the marker is missing)")
            continue
        try:
            write_marker(f["path"], dest)
            outcomes.append({"name": f["name"], "family": f["family"],
                             "worker_id": f["worker_id"], "outcome": "REMARKED", "reason": None})
            print(f"  REMARKED {f['family']}/{f['worker_id']}/{f['name']} (identical tray copy "
                  "already collected; the missing marker is restored, no copy made)")
        except OSError as exc:
            outcomes.append({"name": f["name"], "family": f["family"],
                             "worker_id": f["worker_id"], "outcome": "COPIED+UNMARKED",
                             "reason": str(exc)})
            print(f"  COPIED+UNMARKED {f['family']}/{f['worker_id']}/{f['name']}: the tray copy "
                  f"is landed and byte-identical but the marker write failed again: {exc}")
    return outcomes


def report(plan: dict, tray: Path, oneline: bool = False, outcomes: list | None = None) -> None:
    """Report BOTH planes, always: the tray AND what is still sitting in worker outboxes.

    Reporting only the tray would under-count whenever the sweep has not run, and the sweep only
    runs while the orchestrator is alive, so between sessions results accumulate un-swept. A reader
    that saw only the tray would answer "nothing pending" with deliveries waiting, which is the
    exact single-plane-reading bug class still live in the scratch `list-workers` (it reads one of two
    exchange planes). So the pending figure below is
    the UNION, and its two components are named separately rather than summed into one number.
    """
    n_move, n_held = len(plan["move"]), len(plan["held_no_sentinel"])
    n_coll = len(plan["collision"])
    n_marked = len(plan.get("already_collected", []))
    failed = [o for o in (outcomes or []) if o["outcome"] == "FAILED"]
    copied = [o for o in (outcomes or []) if o["outcome"] == "COPIED+MARKED"]
    unmarked = [o for o in (outcomes or []) if o["outcome"] == "COPIED+UNMARKED"]
    remarked = [o for o in (outcomes or []) if o["outcome"] == "REMARKED"]
    pending = sorted(tray.glob("*.md")) if tray.is_dir() else []
    unswept = n_move + n_held + n_coll + len(failed)
    if oneline:
        print(f"deliveries: {len(pending)} tray / {unswept} unswept"
              + (f" / {n_move} ready" if n_move else "")
              + (f" / {n_held} held" if n_held else "")
              + (f" / {len(failed)} FAILED" if failed else ""))
        return
    n_done = n_move - len(failed) if outcomes is not None else n_move
    print(f"collect-deliveries: {n_done} collected"
          + (f" ({len(failed)} of {n_move} planned FAILED)" if failed else "")
          + f", {n_held} held back, {n_coll} collision(s); "
          f"{len(pending)} pending in the tray, {unswept} still in worker outboxes "
          f"(union is what is actually outstanding).")
    if failed:
        print(f"\nFAILED ({len(failed)}), neither moved nor copied; each is left in place and "
              "will be retried on the next sweep. One failure never aborts the sweep:")
        for o in failed:
            print(f"    {o['family']}/{o['worker_id']}/{o['name']}: {o['reason']}")
    if copied:
        print(f"\nCOPIED+MARKED ({len(copied)}), the outbox directory forbade the rename, so each "
              "was durably copied into the tray and marked beside its source. The marker proves "
              "the copy landed, not that the source was removed; the outbox retains the original "
              "until its owner cleans it:")
        for o in copied:
            print(f"    {o['family']}/{o['worker_id']} -> {o['name']}")
    if unmarked:
        print(f"\nCOPIED+UNMARKED ({len(unmarked)}), the size-verified copy landed in the tray "
              "but the idempotency marker write beside the source failed, so nothing is lost and "
              "nothing was double-collected; the missing marker self-heals on the next sweep "
              "(remark on the byte-identical twin). The exit is non-zero because the state still "
              "needs the operator's eye:")
        for o in unmarked:
            print(f"    {o['family']}/{o['worker_id']}/{o['name']}: {o['reason']}")
    if remarked:
        print(f"\nREMARKED ({len(remarked)}), a byte-identical tray twin proved the earlier copy "
              "landed, so only the missing marker was written; nothing was copied or moved:")
        for o in remarked:
            print(f"    {o['family']}/{o['worker_id']}/{o['name']}")
    if n_marked:
        print(f"\nALREADY COLLECTED ({n_marked}), retained in an outbox under a "
              f"`{MARKER_SUFFIX}` marker from an earlier copy-fallback sweep; skipped, never "
              "re-collected. The retained originals are residue, not pending work. A marker also "
              "outlives its source's CONTENT, so a same-path rewrite after collection is skipped "
              "here; owner-side hygiene (the P-3.235 class) is the remedy for that residue.")
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

    Written against the lesson from a prior discriminability audit, which found 28 self-test
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
          compose_name("opus-20260101T000000Z-anon", "sweep-n"),
          "opus-20260101T000000Z-anon__sweep-n.md")
    check("split_name recovers both ids",
          split_name("opus-20260101T000000Z-anon__sweep-n.md"),
          ("opus-20260101T000000Z-anon", "sweep-n"))
    check("split_name round-trips a hyphenated order id",
          split_name(compose_name("codex-abc", "validate-pr-n-b")),
          ("codex-abc", "validate-pr-n-b"))
    # The empty-part guard, previously BLIND: the cases below covered a non-tray name and a wrong
    # extension, so disabling the guard changed nothing observable and it read as covered. Found by
    # tools/audit-selftest-discriminability.py. Without the guard these return ("", "x") and
    # ("x", ""), and a caller would then use an empty worker id, which downstream
    # consumers must never receive.
    check("split_name rejects an empty worker id", split_name("__x.md"), (None, None))
    check("split_name rejects an empty order id", split_name("x__.md"), (None, None))
    check("split_name rejects a non-tray filename", split_name("sweep-n.md"), (None, None))
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
    def fact(order_id, complete=True, tray_exists=False, tray_identical=False):
        return {"family": "opus", "worker_id": "w1", "order_id": order_id,
                "name": f"{order_id}.md", "complete": complete, "tray_exists": tray_exists,
                "tray_identical": tray_identical}

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
    check("a grandfathered sentinel-less file with a byte-identical tray twin self-heals via remark "
          "(the flag assumes completeness; comment 0a's routine precedence deliberately inverts here)",
          [b for b, fs in
           plan_collection([fact("g4", complete=False, tray_exists=True, tray_identical=True)],
                           grandfather=True).items() if fs],
          ["remark"])
    check("grandfathering a complete file does not mark it grandfathered",
          plan_collection([fact("g3")], grandfather=True)["grandfathered"], [])

    # the .collected marker outranks every other bucket, including collision and incompleteness:
    # the marker is only written after a size-verified tray copy, so the delivery IS collected.
    mfact = dict(fact("m1", complete=False, tray_exists=True), marker_exists=True)
    mp = plan_collection([mfact])
    check("a marker routes a file to already_collected and nowhere else",
          [b for b, fs in mp.items() if fs], ["already_collected"])

    # the remark bucket: a marker-less file whose tray twin is byte-identical is already
    # collected in substance (the COPIED+UNMARKED survivor); only the marker is missing.
    check("planner routes an identical marker-less twin to remark and nowhere else",
          [b for b, fs in plan_collection(
              [dict(fact("r1", tray_exists=True), tray_identical=True)]).items() if fs],
          ["remark"])
    check("a DIFFERING twin stays a collision: byte-equality is the safety proof for remark",
          [b for b, fs in plan_collection(
              [dict(fact("r2", tray_exists=True), tray_identical=False)]).items() if fs],
          ["collision"])
    check("incompleteness outranks remark: a sentinel-less source is held, never frozen under a marker",
          [b for b, fs in plan_collection(
              [dict(fact("r3", complete=False, tray_exists=True), tray_identical=True)]).items() if fs],
          ["held_no_sentinel"])
    check("a marker still outranks remark",
          [b for b, fs in plan_collection(
              [dict(fact("r4", tray_exists=True), tray_identical=True,
                    marker_exists=True)]).items() if fs],
          ["already_collected"])

    # the exit-code discriminator is pure and pinned per outcome kind
    check("needs_attention fires on FAILED",
          needs_attention([{"outcome": "FAILED"}]), True)
    check("needs_attention fires on COPIED+UNMARKED",
          needs_attention([{"outcome": "COPIED+UNMARKED"}]), True)
    check("needs_attention stays quiet on the clean outcomes",
          needs_attention([{"outcome": "MOVED"}, {"outcome": "COPIED+MARKED"},
                           {"outcome": "REMARKED"}]), False)

    # report() was ENTIRELY UNTESTED: all four of its branches were genuine coverage gaps, found by
    # an independent control-bracketed audit (mutation-audit-todays-three-tools). It is the function
    # that tells the operator what was held back and why, so an untested report is how a held-back
    # file becomes a silent skip, which is the exact failure this tool's design forbids. Captured
    # rather than eyeballed, so each branch is pinned by an assertion on its output.
    def _report_text(plan, tray_path, oneline=False, outcomes=None):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            report(plan, tray_path, oneline, outcomes)
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
        ready_plan = {"move": [fact("r1")], "held_no_sentinel": [], "collision": [],
                      "grandfathered": [], "remark": [], "already_collected": []}
        one_ready = _report_text(ready_plan, empty_tray, oneline=True)
        check("oneline counts a ready (planned-move) outbox delivery as unswept",
              "1 unswept" in one_ready and "1 ready" in one_ready, True)

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

    # --- the sticky-outbox fallback: copy+marker, marker-skip, and one-failure-does-not-abort ---
    # SYNTHETIC fixtures: every worker id and order id below is invented for this test and
    # mirrors no real worker, family layout aside.
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        wdir = root / "codex" / "outbox" / "codex-w2"
        (wdir / "orders").mkdir(parents=True)
        tray = root / "inbox" / "deliveries"
        (wdir / "sticky-one.md").write_text(f"result A\n\n{SENTINEL}\n")
        (wdir / "sticky-two.md").write_text(f"result B\n\n{SENTINEL}\n")
        (wdir / "orders" / "sticky-one.md").write_text("the order it served")

        real_replace = os.replace

        def deny_outbox_renames(src, dst, *args, **kwargs):
            # Simulate the sticky-directory class: a rename OUT OF the outbox raises
            # PermissionError (another account owns the file), while the tray-internal rename
            # that promotes the .partial copy still works.
            if str(src).startswith(str(wdir)):
                raise PermissionError(1, "Operation not permitted")
            return real_replace(src, dst, *args, **kwargs)

        os.replace = deny_outbox_renames
        try:
            plan6 = plan_collection(gather_facts(root, tray))
            buf6 = io.StringIO()
            with contextlib.redirect_stdout(buf6):
                out6 = execute(plan6, root, tray, dry_run=False)
        finally:
            os.replace = real_replace
        exec6 = buf6.getvalue()
        check("fallback lands both deliveries in the tray despite the forbidden rename",
              sorted(q.name for q in tray.glob("*.md")),
              ["codex-w2__sticky-one.md", "codex-w2__sticky-two.md"])
        check("fallback outcomes are COPIED+MARKED, not MOVED",
              sorted(o["outcome"] for o in out6), ["COPIED+MARKED", "COPIED+MARKED"])
        check("a marker sits beside each retained source",
              sorted(q.name for q in wdir.glob(f"*{MARKER_SUFFIX}")),
              ["sticky-one.md.collected", "sticky-two.md.collected"])
        check("the source is retained: the marker proves the copy, never the removal",
              (wdir / "sticky-one.md").is_file(), True)
        check("the tray copy is byte-identical to the source",
              (tray / "codex-w2__sticky-one.md").read_text(), f"result A\n\n{SENTINEL}\n")
        check("no .partial residue is left in the tray",
              sorted(tray.glob(f"*{PARTIAL_SUFFIX}*")), [])

        # the served-order archive fallback gets the SAME durable copy plus a success-path NOTE
        check("archive fallback durably copies the served order despite the forbidden rename",
              (root / "done" / "orders" / "sticky-one.md").read_text(), "the order it served")
        check("archive fallback NOTEs its success path: copied, not moved, owner retains",
              "copied, not moved" in exec6 and "owner retains the original" in exec6, True)
        check("the owner-retained served order stays in the outbox",
              (wdir / "orders" / "sticky-one.md").is_file(), True)
        check("no .partial residue is left in done/orders either",
              sorted((root / "done" / "orders").glob(f"*{PARTIAL_SUFFIX}*")), [])

        # marker-skip on re-scan: retained sources are never re-collected (idempotency)
        plan7 = plan_collection(gather_facts(root, tray))
        check("a marked delivery is skipped on the next sweep, never re-collected",
              len(plan7["move"]), 0)
        check("a marked delivery routes to already_collected, not to collision or held",
              sorted(f["order_id"] for f in plan7["already_collected"]),
              ["sticky-one", "sticky-two"])

        # a marker is itself never a delivery: wrong suffix, invisible to the *.md glob
        check("a .collected marker is never gathered as a delivery candidate",
              [f["name"] for f in gather_facts(root, tray)
               if f["name"].endswith(MARKER_SUFFIX)], [])

        # the residue is stated in the report, at the point the operator reads it
        check("report names the already-collected residue as skipped, never pending",
              "ALREADY COLLECTED" in _report_text(plan7, tray), True)
        empty_plan = {"move": [], "held_no_sentinel": [], "collision": [],
                      "grandfathered": [], "already_collected": []}
        check("report states the copy-fallback residue: copy proved, removal not",
              "not that the source was removed" in _report_text(empty_plan, tray,
                                                                outcomes=out6), True)

    # one failure must not abort the sweep, and it alone drives a FAILED outcome
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        wdir = root / "opus" / "outbox" / "opus-w3"
        wdir.mkdir(parents=True)
        tray = root / "inbox" / "deliveries"
        (wdir / "bad-order.md").write_text(f"doomed\n\n{SENTINEL}\n")
        (wdir / "good-order.md").write_text(f"fine\n\n{SENTINEL}\n")

        real_replace = os.replace

        def fail_one(src, dst, *args, **kwargs):
            # A NON-permission OSError, so the copy fallback is not invoked: the file simply
            # fails, and the sweep must carry on to the next planned file regardless.
            if Path(src).name == "bad-order.md":
                raise OSError(5, "Input/output error")
            return real_replace(src, dst, *args, **kwargs)

        os.replace = fail_one
        try:
            plan8 = plan_collection(gather_facts(root, tray))
            out8 = execute(plan8, root, tray, dry_run=False)
        finally:
            os.replace = real_replace
        check("one failing file does not abort the sweep: the other file still collected",
              (tray / "opus-w3__good-order.md").is_file(), True)
        check("the failing file is recorded FAILED with its reason",
              [(o["outcome"], "Input/output error" in (o["reason"] or "")) for o in out8
               if o["outcome"] == "FAILED"], [("FAILED", True)])
        check("the failing file stays in place for the next sweep",
              (wdir / "bad-order.md").is_file(), True)
        check("a failed file gets no marker (nothing landed in the tray for it)",
              (wdir / f"bad-order.md{MARKER_SUFFIX}").exists(), False)
        check("the report names the failure and says the sweep continued",
              "FAILED (1)" in _report_text(plan8, tray, outcomes=out8), True)

    # --- a marker-write failure after a LANDED copy is COPIED+UNMARKED, and the next sweep
    #     self-heals it via remark. SYNTHETIC fixtures mirroring no real worker. ---
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        wdir = root / "fable" / "outbox" / "fable-w4"
        wdir.mkdir(parents=True)
        tray = root / "inbox" / "deliveries"
        (wdir / "heal-one.md").write_text(f"heal body\n\n{SENTINEL}\n")

        real_replace = os.replace

        def deny_outbox_renames(src, dst, *args, **kwargs):
            if str(src).startswith(str(wdir)):
                raise PermissionError(1, "Operation not permitted")
            return real_replace(src, dst, *args, **kwargs)

        real_marker = globals()["write_marker"]

        def failing_marker(src, dest):
            raise OSError(13, "Permission denied: marker")

        os.replace = deny_outbox_renames
        globals()["write_marker"] = failing_marker
        try:
            planU = plan_collection(gather_facts(root, tray))
            bufU = io.StringIO()
            with contextlib.redirect_stdout(bufU):
                outU = execute(planU, root, tray, dry_run=False)
        finally:
            os.replace = real_replace
            globals()["write_marker"] = real_marker
        check("a marker-write failure after a landed copy is COPIED+UNMARKED, never FAILED",
              [o["outcome"] for o in outU], ["COPIED+UNMARKED"])
        check("the tray copy from the unmarked collection is complete",
              (tray / "fable-w4__heal-one.md").read_text(), f"heal body\n\n{SENTINEL}\n")
        check("no marker exists after the marker write failed",
              (wdir / f"heal-one.md{MARKER_SUFFIX}").exists(), False)
        check("COPIED+UNMARKED still drives the non-zero exit", needs_attention(outU), True)
        repU = _report_text(planU, tray, outcomes=outU)
        check("the report tells the truth: copy landed, marker missing, self-heals",
              "copy landed" in repU and "self-heals" in repU, True)
        check("the unmarked file is NOT reported as neither moved nor copied",
              "neither moved nor copied" in repU, False)

        # the SELF-HEAL: the next sweep observes the byte-identical twin and only re-marks
        factsH = gather_facts(root, tray)
        check("gather observes the byte-identical tray twin (observation only)",
              [f2["tray_identical"] for f2 in factsH], [True])
        planH = plan_collection(factsH)
        check("the planner routes the identical twin to remark, not to collision",
              [b for b, fs in planH.items() if fs], ["remark"])
        outH = execute(planH, root, tray, dry_run=False)
        check("remark writes ONLY the missing marker",
              (wdir / f"heal-one.md{MARKER_SUFFIX}").is_file(), True)
        check("remark records the REMARKED outcome",
              [o["outcome"] for o in outH], ["REMARKED"])
        check("remark makes no second copy: the tray twin is untouched",
              (tray / "fable-w4__heal-one.md").read_text(), f"heal body\n\n{SENTINEL}\n")
        check("a REMARKED outcome alone does not drive a non-zero exit",
              needs_attention(outH), False)
        check("the report names the remark self-heal",
              "REMARKED" in _report_text(planH, tray, outcomes=outH), True)

        # the third sweep sees the restored marker: already_collected, steady state
        planS = plan_collection(gather_facts(root, tray))
        check("after the self-heal the delivery is already_collected, steady state",
              [b for b, fs in planS.items() if fs], ["already_collected"])

    # --- the fallback's own failure modes: FAILED stays honest and no partial ever lingers ---
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        wdir = root / "codex" / "outbox" / "codex-w6"
        wdir.mkdir(parents=True)
        tray = root / "inbox" / "deliveries"
        (wdir / "no-copy.md").write_text(f"body\n\n{SENTINEL}\n")

        real_replace = os.replace
        real_copy2 = shutil.copy2

        def deny_outbox_renames(src, dst, *args, **kwargs):
            if str(src).startswith(str(wdir)):
                raise PermissionError(1, "Operation not permitted")
            return real_replace(src, dst, *args, **kwargs)

        def refuse_copy(src, dst, *args, **kwargs):
            raise OSError(30, "Read-only file system")

        os.replace = deny_outbox_renames
        shutil.copy2 = refuse_copy
        try:
            planF = plan_collection(gather_facts(root, tray))
            outF = execute(planF, root, tray, dry_run=False)
        finally:
            os.replace = real_replace
            shutil.copy2 = real_copy2
        check("a copy failure AFTER PermissionError records FAILED with its reason",
              [(o["outcome"], "Read-only" in (o["reason"] or "")) for o in outF],
              [("FAILED", True)])
        check("a failed copy leaves no marker",
              (wdir / f"no-copy.md{MARKER_SUFFIX}").exists(), False)
        check("a failed copy leaves no tray file",
              (tray / "codex-w6__no-copy.md").exists(), False)
        check("a failed copy leaves no partial behind",
              sorted(tray.glob(f"*{PARTIAL_SUFFIX}*")), [])
        check("the source stays put for the next sweep", (wdir / "no-copy.md").is_file(), True)

        # a truncated copy trips the size verify, raises, and cleans its own partial
        def truncating_copy2(src, dst, *args, **kwargs):
            Path(dst).write_bytes(Path(src).read_bytes()[:-3])

        os.replace = deny_outbox_renames
        shutil.copy2 = truncating_copy2
        try:
            planT = plan_collection(gather_facts(root, tray))
            outT = execute(planT, root, tray, dry_run=False)
        finally:
            os.replace = real_replace
            shutil.copy2 = real_copy2
        check("a size mismatch is refused: FAILED, with the mismatch named",
              [(o["outcome"], "size mismatch" in (o["reason"] or "")) for o in outT],
              [("FAILED", True)])
        check("the mismatched partial is cleaned up, never promoted",
              sorted(tray.glob(f"*{PARTIAL_SUFFIX}*")) + sorted(tray.glob("*.md")), [])

    # --- an archival done-tree failure is a NOTE, never a sweep abort ---
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        wdir = root / "opus" / "outbox" / "opus-w7"
        (wdir / "orders").mkdir(parents=True)
        tray = root / "inbox" / "deliveries"
        (wdir / "arch-one.md").write_text(f"r1\n\n{SENTINEL}\n")
        (wdir / "orders" / "arch-one.md").write_text("order copy")
        (wdir / "arch-two.md").write_text(f"r2\n\n{SENTINEL}\n")
        (root / "done").write_text("a FILE squatting where the done directory belongs")
        bufA = io.StringIO()
        with contextlib.redirect_stdout(bufA):
            outA = execute(plan_collection(gather_facts(root, tray)), root, tray, dry_run=False)
        outtext = bufA.getvalue()
        check("an archival mkdir failure never aborts the sweep: both deliveries collected",
              sorted(o["outcome"] for o in outA), ["MOVED", "MOVED"])
        check("the archival mkdir failure is a NOTE naming the order and the cause",
              "NOTE: order copy for arch-one not archived" in outtext, True)

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
    outcomes = []
    if not a.oneline:
        outcomes = execute(plan, root, tray, a.dry_run)
    report(plan, tray, a.oneline, outcomes)
    # The non-advisory exits, named by the pure needs_attention: a FAILED file (neither moved nor
    # copied, a real loss of sweep completeness) and a COPIED+UNMARKED file (copy landed, marker
    # missing; self-heals next sweep but the operator must see it happened).
    return 1 if needs_attention(outcomes) else 0


if __name__ == "__main__":
    sys.exit(main())
