#!/usr/bin/env python3
"""Merge tool for jposluns/grc_library_new (3b882), part P1: the register row check.

The grc_library_new squash merge is to go only through this tool, which refuses unless both
QA rows for the PR are in this repository's own registers in the operational store:

* the /validate-pr row in ``validate-pr/history-grc_library_new.md``;
* the /retro row in ``improvement-log-grc_library_new.md``.

A row is a Markdown table line outside any fenced block that begins with ``|`` and has at least
three cells, whose first cell is an ISO date (ASCII digits, ``YYYY-MM-DD``) and whose second cell
starts with ``#N`` not followed by a digit (of any script) and contains the literal tag
``[repo: grc_library_new]``. In the improvement log the second cell must start with
``#N (/retro)``. So ``#3`` and ``#310`` never stand for ``#31``, a ``[repo: grc_library]`` or
untagged row never counts, and a row quoted inside a fence never counts.

Decision D1: the registers are read only from the operational store found by lint_common's strict
store resolver (``_store_dir(root, strict=True)``: ``$GRC_STORE``, else ``<repo-parent>/private``),
never from the private sibling or the in-repo ``.working/`` fallbacks, and never from a store that
resolves inside the repository. A store or register that is absent, is not what it should be, or
cannot be read or decoded as UTF-8 refuses, naming it.

This part is read-only: it never merges, writes no file and makes no network call. The merge,
the read-back, the admin-merge log row and the hook are later parts of the plan.

Usage:
    python3 tools/merge-grc-library-new.py --check-rows <PR>
    python3 tools/merge-grc-library-new.py --self-test

Exit codes: 0 both rows present (or the self-test passed); 1 a row is missing (each missing row
is named); 2 usage error, or the store or a register cannot be found or read (each is named).
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent

REPO_TAG = "[repo: grc_library_new]"
# (name, store-relative path, the row's QA kind) in report order.
REGISTERS = (
    ("validate-pr", "validate-pr/history-grc_library_new.md", "/validate-pr"),
    ("retro", "improvement-log-grc_library_new.md", "/retro"),
)
_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", re.ASCII)
_PR_ARG = re.compile(r"[1-9][0-9]{0,5}", re.ASCII)
# A CommonMark fence line: up to three spaces, then three or more backticks or tildes.
_FENCE = re.compile(r" {0,3}(`{3,}|~{3,})")


class RegisterError(Exception):
    """The store or a register cannot be found or read; the message names it."""


def _table_rows(text: str):
    """Yield the cells of each table line outside fenced blocks.

    A fence opens on a fence line and closes on a line of the same character, at least as long,
    with nothing after it but spaces or tabs; an unclosed fence runs to the end of the text. A
    table line begins with ``|`` (no indentation) and has at least three cells."""
    fence = None
    for line in text.split("\n"):
        line = line.rstrip("\r")
        match = _FENCE.match(line)
        if fence is not None:
            if (match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence)
                    and not line[match.end():].strip(" \t")):
                fence = None
            continue
        if match:
            fence = match.group(1)
            continue
        if not line.startswith("|"):
            continue
        cells = line.split("|")[1:]
        if line.rstrip(" \t").endswith("|"):
            cells = cells[:-1]
        if len(cells) >= 3:
            yield [c.strip() for c in cells]


def row_present(text: str, pr: int, *, retro: bool) -> bool:
    """Whether ``text`` holds a dated table row for grc_library_new PR ``pr``.

    The second cell must start with ``#<pr>`` not followed by a digit (or ``#<pr> (/retro)`` when
    ``retro``) and contain the ``[repo: grc_library_new]`` tag."""
    head = f"#{pr} (/retro)" if retro else f"#{pr}"
    lead = re.compile(re.escape(head) + r"(?!\d)")
    for cells in _table_rows(text):
        if _DATE.fullmatch(cells[0]) and lead.match(cells[1]) and REPO_TAG in cells[1]:
            return True
    return False


def missing_rows(validate_text: str, retro_text: str, pr: int) -> list[str]:
    """The names of the rows absent for PR ``pr``, from ``"validate-pr"`` and ``"retro"`` in that
    order: an empty list means both registers hold the PR's row."""
    missing = []
    if not row_present(validate_text, pr, retro=False):
        missing.append("validate-pr")
    if not row_present(retro_text, pr, retro=True):
        missing.append("retro")
    return missing


def find_store(root: Path) -> Path:
    """The operational store by lint_common's strict resolver, or :class:`RegisterError`.

    Only ``_store_dir(root, strict=True)`` is consulted (decision D1): the private sibling and the
    in-repo ``.working/`` fallbacks of ``resolve_working`` are never probed or read."""
    if str(TOOLS_DIR) not in sys.path:
        sys.path.insert(0, str(TOOLS_DIR))
    import lint_common

    try:
        store = lint_common._store_dir(root.resolve(), strict=True)
    except lint_common.InaccessiblePath as exc:
        raise RegisterError(f"operational store {exc.filename}: {exc.strerror}") from exc
    if store is None:
        where = os.environ.get("GRC_STORE") or str(root.resolve().parent / "private")
        raise RegisterError(
            f"operational store {where}: absent, or inside the repository; set GRC_STORE to the "
            "operational store (the sibling and in-repo .working/ fallbacks are never read)")
    return store


def read_register(store: Path, rel: str) -> str:
    """The text of ``<store>/<rel>``, or :class:`RegisterError` naming it."""
    if str(TOOLS_DIR) not in sys.path:
        sys.path.insert(0, str(TOOLS_DIR))
    import lint_common

    path = store / rel
    try:
        kind = lint_common.strict_kind_under(store, rel)
    except lint_common.InaccessiblePath as exc:
        raise RegisterError(f"{path}: {exc.strerror}") from exc
    if kind is None:
        raise RegisterError(f"{path}: absent")
    if kind != "file":
        raise RegisterError(f"{path}: not a regular file ({kind})")
    try:
        if not path.resolve().is_relative_to(store.resolve()):
            raise RegisterError(f"{path}: resolves outside the operational store")
        return path.read_text(encoding="utf-8")
    except (OSError, RuntimeError, UnicodeDecodeError) as exc:
        raise RegisterError(f"{path}: cannot be read: {exc}") from exc


def check_rows(pr: int, *, root: Path = REPO_ROOT) -> tuple[int, list[str]]:
    """Read both registers from the operational store and check PR ``pr``'s rows.

    Returns ``(exit code, report lines)``: 0 with both matched paths; 2 naming the store, or each
    register that cannot be read; 1 naming each register whose row is missing."""
    try:
        store = find_store(root)
    except RegisterError as exc:
        return 2, [f"REFUSED: {exc}"]
    texts, errors = {}, []
    for name, rel, _kind in REGISTERS:
        try:
            texts[name] = read_register(store, rel)
        except RegisterError as exc:
            errors.append(f"REFUSED: {name} register unreadable: {exc}")
    if errors:
        return 2, errors
    missing = missing_rows(texts["validate-pr"], texts["retro"], pr)
    lines = [f"REFUSED: missing {kind} row for #{pr} {REPO_TAG} in {store / rel}"
             for name, rel, kind in REGISTERS if name in missing]
    if lines:
        return 1, lines
    return 0, [f"rows present for #{pr} {REPO_TAG}: {kind} in {store / rel}"
               for _name, rel, kind in REGISTERS]


def self_test() -> int:
    """Exercise the pure row check and the store reads against temporary fixtures only."""
    import tempfile

    v_row = "| 2026-11-14 | #31 [repo: grc_library_new] | train 1 | claude | IDS | done |"
    r_row = "| 2026-11-14 | #31 (/retro) [NEW31-RETRO] [repo: grc_library_new] | t | a | b | c |"
    cases = [
        ("both rows", missing_rows(v_row, r_row, 31), []),
        ("validate-pr missing", missing_rows("", r_row, 31), ["validate-pr"]),
        ("retro missing", missing_rows(v_row, "", 31), ["retro"]),
        ("#3 is not #31", missing_rows(v_row.replace("#31", "#3"), r_row.replace("#31", "#3"), 31),
         ["validate-pr", "retro"]),
        ("#310 is not #31", missing_rows(v_row.replace("#31", "#310"), r_row.replace("#31", "#310"), 31),
         ["validate-pr", "retro"]),
        ("#31 is not #3", missing_rows(v_row, r_row, 3), ["validate-pr", "retro"]),
        ("fullwidth digits", missing_rows(v_row.replace("#31", "#３１"), r_row, 31),
         ["validate-pr"]),
        ("grc_library tag", missing_rows(v_row.replace(REPO_TAG, "[repo: grc_library]"), r_row, 31),
         ["validate-pr"]),
        ("untagged", missing_rows(v_row.replace(" " + REPO_TAG, ""), r_row, 31), ["validate-pr"]),
        ("retro marker absent", missing_rows(v_row, r_row.replace(" (/retro)", ""), 31), ["retro"]),
        ("fenced rows", missing_rows("```\n" + v_row + "\n```", "~~~\n" + r_row + "\n~~~", 31),
         ["validate-pr", "retro"]),
        ("closed fence", missing_rows("```\nx\n```\n" + v_row, r_row, 31), []),
        ("prose line", missing_rows("Moved #31 " + REPO_TAG + " on 2026-11-14.", r_row, 31),
         ["validate-pr"]),
        ("undated row", missing_rows(v_row.replace("2026-11-14", "PR"), r_row, 31), ["validate-pr"]),
    ]
    failures = [f"{name}: got {got}, want {want}" for name, got, want in cases if got != want]
    saved = os.environ.get("GRC_STORE")
    try:
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            root = parent / "repo"
            root.mkdir()
            store = parent / "store"
            (store / "validate-pr").mkdir(parents=True)
            os.environ["GRC_STORE"] = str(store)
            (store / REGISTERS[1][1]).write_text(r_row + "\n", encoding="utf-8")
            store_cases = [("validate-pr register absent", 2)]
            got = [check_rows(31, root=root)[0]]
            (store / REGISTERS[0][1]).write_bytes(b"\xff" + v_row.encode() + b"\n")
            store_cases.append(("invalid UTF-8", 2))
            got.append(check_rows(31, root=root)[0])
            (store / REGISTERS[0][1]).write_text(v_row.replace("#31", "#310") + "\n", encoding="utf-8")
            store_cases.append(("row missing", 1))
            got.append(check_rows(31, root=root)[0])
            (store / REGISTERS[0][1]).write_text(v_row + "\n", encoding="utf-8")
            store_cases.append(("both rows", 0))
            got.append(check_rows(31, root=root)[0])
            os.environ["GRC_STORE"] = str(parent / "absent")
            store_cases.append(("store absent", 2))
            got.append(check_rows(31, root=root)[0])
            os.environ["GRC_STORE"] = str(root)
            store_cases.append(("store inside the repository", 2))
            got.append(check_rows(31, root=root)[0])
            failures += [f"{name}: exit {code}, want {want}"
                         for (name, want), code in zip(store_cases, got) if code != want]
            count = len(cases) + len(store_cases)
    finally:
        if saved is None:
            os.environ.pop("GRC_STORE", None)
        else:
            os.environ["GRC_STORE"] = saved
    if failures:
        for line in failures:
            print("FAIL:", line, file=sys.stderr)
        return 1
    print(f"merge-grc-library-new.py self-test OK ({count} cases)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check grc_library_new's QA register rows for a PR (read-only).")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check-rows", metavar="PR",
                      help="exit 0 only when both the /validate-pr and /retro rows are present")
    mode.add_argument("--self-test", action="store_true", help="run the built-in self-test")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if not _PR_ARG.fullmatch(args.check_rows):
        print(f"usage error: --check-rows takes a PR number (1 to 999999, no leading zero), "
              f"got {args.check_rows!r}", file=sys.stderr)
        return 2
    code, lines = check_rows(int(args.check_rows))
    for line in lines:
        print(line, file=sys.stderr if code else sys.stdout)
    return code


if __name__ == "__main__":
    sys.exit(main())
