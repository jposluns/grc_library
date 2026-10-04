#!/usr/bin/env python3
"""On-demand instruction-cut ledger check; stdlib-only Python 3.11.

--extract prints a ledger bound to resolved BASE and --path, initially KEPT.
Review every row. KEPT requires the same path at committed HEAD; MOVED requires
another tracked text file; DROPPED requires a nonblank reason. A move asserts
presence, not that the destination gained the text since BASE.

REBASED is a reviewer assertion that the clause MOVED with only relative link
targets re-based; like MOVED it needs another tracked file and an empty reason.
It compares raw unit text (CR and line terminators included, nothing
normalized): an unconsumed destination unit must equal the BASE unit except for
substituted target segments. Every target starts after its "](" and any leading
ASCII space, tab, LF, CR, FF or VT. Either unit fails if it holds a backslash
or "<" anywhere, or a "(" in any link target: the text from that start up to
the next ASCII ")", space, tab, LF, CR, FF or VT (or the unit's end), unchanged
targets and any "#" or "?" part included. Each such refusal names its rule,
side and raw offset. A segment starts at that start in both texts, after
identical leading whitespace (otherwise the texts differ), and ends at the
first ASCII ")", "#", "?", space, tab, LF, CR, FF or VT; a target with no
terminator is not a segment. A "#" or "?" terminator starts a suffix that runs
up to the next ")" in BASE: it must be identical, and a "(" in it fails, so no
"](" can occur inside it. Every other "](" is a target position, so "](" in
prose, code, titles and reference definitions is re-based too. A changed
segment must be nonempty, use only A-Z, a-z, 0-9 and "._~/+-", and have no
leading or trailing "/", no empty ("//") or "." component, and no ".." as its
last component. Each side is joined to its file's directory and resolved
lexically step by step; a step above the repository root fails, and the two
repository-relative paths must be equal. Target existence, tracking and
symlinks are not checked, and unchanged segments are not resolved. Both texts
must hold equally many "](". Identical texts fail (use MOVED); other mismatches
name the first differing raw BASE offset. REBASED shares occurrence counting
with MOVED and takes the first matching unit in file order, so row order can
cause a false failure. A reviewer must check every REBASED hunk.

Units are ATX/setext headings, individual list items with adjacent wrapped
continuations, pipe-containing table rows, fenced blocks, thematic breaks,
and paragraphs. Nested items start separate units. Blank lines separate
paragraphs/items. Every LF-delimited physical line belongs to a unit or an
explicit BLANK exclusion. Unclosed fences are input errors.

Matching includes unit kind, list indentation columns (four-column tab stops)
and exact marker, heading level, and table cell boundaries. Fenced blocks
are byte-exact UTF-8, including line endings and the closing line terminator.
Inline backtick spans are exact too. Elsewhere only ASCII spaces, tabs and
wrapped CR/LF breaks within a unit are normalized. Destination units are
consumed once per file. Ledger quotes and spans must match BASE exactly.
Ledger files cannot supply evidence; only committed tracked files can.

Disclosed residual: this lexical partition is not a CommonMark renderer or
semantic proof. HTML comments/blocks, indented code, and blockquote/list
container context are not modeled. Wrapping a paragraph in a multiline HTML
comment, or indenting it as code, can still satisfy KEPT. List indentation
is lexical, not relative to a parsed parent. Equal-depth re-parenting,
section moves and ordering are unchecked. Escaped backticks, HTML/CSS hiding,
link/reference interpretation and other renderer-specific effects require
manual diff review. Top-level fences accept at most three leading spaces;
nested container fences are outside this model. Review each hunk for these
rendering and scope changes even when the ledger passes.

Flags are unchanged (including --repo). The new ledger schema deliberately
rejects old K/M/S ledgers; regenerate with --extract. No files are written.
Exit 0: accounted inventory; 1: preservation findings; 2: input/git error.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import posixpath
import re
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
INPUT_ERRORS = (OSError, UnicodeError, ValueError, RecursionError, RuntimeError)
ATX = re.compile(r"^ {0,3}#{1,6}(?:\s|$)")
SETEXT = re.compile(r"^ {0,3}(?:=+|-+)[ \t]*$")
LIST = re.compile(r"^([ \t]*)([-+*]|[0-9]{1,9}[.)])[ \t]+")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
RULE = re.compile(r"^ {0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$")
TOP_KEYS = {"base_revision", "base_path", "clauses", "excluded_lines"}
UNIT_KEYS = {"base_line", "end_line", "kind", "base_quote"}
ROW_KEYS = UNIT_KEYS | {"state", "destination", "reason"}
TARGET_END = re.compile(r"[)#? \t\n\r\f\v]")
PATH_CHAR = re.compile(r"[A-Za-z0-9._~/+-]")
LINK_TARGET_END = re.compile(r"[) \t\n\r\f\v]")
TARGET_START = re.compile(r"[ \t\n\r\f\v]*")


def inline_parts(text: str):
    """Yield ordinary text and exact, equal-delimiter backtick spans."""
    start = cursor = 0
    while cursor < len(text):
        opening = re.search(r"`+", text[cursor:])
        if opening is None:
            break
        left = cursor + opening.start()
        right = cursor + opening.end()
        closing = re.search(r"(?<!`)" + re.escape(opening.group()) + r"(?!`)",
                            text[right:])
        if closing is None:
            cursor = right
            continue
        end = right + closing.end()
        yield False, text[start:left]
        yield True, text[left:end]
        start = cursor = end
    yield False, text[start:]


def normalize(text: str) -> str:
    """Normalize prose whitespace, preserving literal backtick spans."""
    return "".join(part if literal else re.sub(r"[ \t\r\n]+", " ", part)
                   for literal, part in inline_parts(text)).strip(" ")


def table_cells(text: str) -> tuple[str, ...]:
    """Keep unescaped pipe boundaries outside exact backtick spans."""
    cells = [""]
    for literal, part in inline_parts(text):
        if literal:
            cells[-1] += part
            continue
        slashes = 0
        for char in part:
            if char == "|" and slashes % 2 == 0:
                cells.append("")
            else:
                cells[-1] += char
            slashes = slashes + 1 if char == "\\" else 0
    return tuple(normalize(cell) for cell in cells)


def match_key(unit: dict) -> tuple:
    category, text = unit["kind"], unit["base_quote"]
    if category == "fence":
        return category, text
    if category == "list_item":
        match = LIST.match(text)
        return (category, len(match[1].expandtabs(4)), match[2],
                normalize(text[match.end():]))
    if category == "heading":
        first = text.split("\n", 1)[0]
        if ATX.match(first):
            level = len(first.lstrip(" ").split()[0])
            body = first.lstrip(" ")[level:]
        else:
            body, underline = text.rsplit("\n", 1)
            level = 1 if underline.lstrip().startswith("=") else 2
        return category, level, normalize(body)
    if category == "table_row":
        return category, table_cells(text)
    return category, normalize(text)


def target_error(segment: str) -> str | None:
    """Name the first REBASED rule a substituted link target breaks."""
    if not segment:
        return "empty target"
    if segment.startswith("/"):
        return "leading '/'"
    for char in segment:
        if not PATH_CHAR.fullmatch(char):
            return f"character {char!r}"
    if segment.endswith("/"):
        return "trailing '/'"
    if "//" in segment:
        return "empty path component ('//')"
    if "." in segment.split("/"):
        return "'.' path component"
    if segment.split("/")[-1] == "..":
        return "final '..' component"
    return None


def target_paren(unit: str) -> int:
    """Raw offset of the first "(" inside any link target, or -1."""
    for match in re.finditer(r"\]\(", unit):
        start = TARGET_START.match(unit, match.end()).end()
        end = LINK_TARGET_END.search(unit, start)
        offset = unit.find("(", start, end.start() if end else len(unit))
        if offset >= 0:
            return offset
    return -1


def unit_error(base: str, text: str) -> str | None:
    """Name the first whole-unit REBASED refusal with its side and raw offset."""
    for side, unit in (("BASE", base), ("destination", text)):
        for rule, offset in (("backslash", unit.find("\\")),
                             ("'<'", unit.find("<")),
                             ("'(' in a link target", target_paren(unit))):
            if offset >= 0:
                return f"{rule} in the {side} unit at raw offset {offset}"
    return None


def resolve(directory: str, segment: str) -> str | None:
    """Resolve a target step by step; None when any step leaves the repository."""
    parts = []
    for part in posixpath.join(directory, segment).split("/"):
        if part == "..":
            if not parts:
                return None
            parts.pop()
        elif part not in {"", "."}:
            parts.append(part)
    return "/".join(parts)


def rebased(base: str, base_dir: str, text: str, text_dir: str):
    """Return (substitutions, None), or (first differing BASE offset, reason).

    A whole-unit refusal returns offset -1; its reason names the raw offset.
    """
    problem = unit_error(base, text)
    if problem:
        return -1, problem
    i = j = substitutions = 0
    first, suffix = None, False
    while i < len(base) or j < len(text):
        if i == len(base) or j == len(text) or base[i] != text[j]:
            return i, "text differs"
        suffix = suffix and base[i] != ")"
        if suffix and base[i] == "(":
            return i, "'(' in a '#' or '?' suffix"
        i, j = i + 1, j + 1
        if suffix or base[i - 2:i] != "](" or text[j - 2:j] != "](":
            continue
        start_base = TARGET_START.match(base, i).end()
        start_text = TARGET_START.match(text, j).end()
        if base[i:start_base] != text[j:start_text]:
            continue
        i, j = start_base, start_text
        end_base, end_text = TARGET_END.search(base, i), TARGET_END.search(text, j)
        if not (end_base and end_text):
            continue
        old, new = base[i:end_base.start()], text[j:end_text.start()]
        if old != new:
            pair = f"target {old!r} -> {new!r}"
            problem = target_error(old) or target_error(new)
            if problem:
                return i, f"{pair}: {problem}"
            left, right = resolve(base_dir, old), resolve(text_dir, new)
            if left is None or right is None:
                return i, f"{pair}: outside the repository"
            if left != right:
                return i, f"{pair}: resolves to {left!r} and {right!r}"
            first = i if first is None else first
            substitutions += 1
        i, j = end_base.start(), end_text.start()
        suffix = base.startswith(("#", "?"), i)
    if base.count("](") != text.count("]("):
        return first, (f"'](' count differs: {base.count('](')} in BASE, "
                       f"{text.count('](')} at the destination")
    return substitutions, None


def clauses(text: str) -> tuple[list[dict], list[dict]]:
    """Partition every physical line; retain raw spelling for ledger review."""
    pieces = text.split("\n")
    raw_lines = [piece + "\n" for piece in pieces[:-1]]
    if pieces[-1]:
        raw_lines.append(pieces[-1])
    lines = [line.removesuffix("\n").removesuffix("\r") for line in raw_lines]
    units, excluded = [], []

    def kind(line):
        if FENCE.match(line):
            return "fence"
        if ATX.match(line):
            return "heading"
        if RULE.fullmatch(line):
            return "thematic_break"
        if LIST.match(line):
            return "list_item"
        if "|" in line:
            return "table_row"
        return "paragraph"

    i = 0
    while i < len(lines):
        if not lines[i].strip():
            excluded.append({"line": i + 1, "category": "BLANK"})
            i += 1
            continue
        start, category = i, kind(lines[i])
        if category == "fence":
            marker = FENCE.match(lines[i]).group(1)
            close = re.compile(r"^ {0,3}" + re.escape(marker[0])
                               + "{" + str(len(marker)) + r",}[ \t]*$")
            i += 1
            while i < len(lines) and not close.fullmatch(lines[i]):
                i += 1
            if i == len(lines):
                raise ValueError(f"line {start + 1}: unclosed fenced block")
            i += 1
        elif category in {"heading", "thematic_break", "table_row"}:
            i += 1
        else:
            i += 1
            while i < len(lines) and lines[i].strip():
                if category == "paragraph" and SETEXT.fullmatch(lines[i]):
                    category = "heading"
                    i += 1
                    break
                if kind(lines[i]) != "paragraph":
                    break
                i += 1
        units.append(dict(base_line=start + 1, end_line=i, kind=category,
                          base_quote=("".join(raw_lines[start:i]) if category == "fence"
                                      else "\n".join(lines[start:i])),
                          raw="".join(raw_lines[start:i])))
    return units, excluded


def repo_path(value: str) -> str:
    if (not isinstance(value, str) or not value or value.startswith("/")
            or any(c in value for c in "\\\0\n\r:")
            or any(p in {"", ".", "..", ".git"} for p in value.split("/"))):
        raise ValueError(f"expected canonical repository-relative path: {value!r}")
    return value


def git(root: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "--literal-pathspecs", "-C", str(root), *args],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if result.returncode:
        raise ValueError(result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def commit(root: Path, revision: str) -> str:
    return git(root, "rev-parse", "--verify", "--end-of-options",
               revision + "^{commit}").decode("ascii").strip()


def read_blob(root: Path, revision: str, path: str) -> str:
    try:
        records = git(root, "ls-tree", "-z", revision, "--", repo_path(path))
        entries = [entry for entry in records.split(b"\0") if entry]
        if len(entries) != 1:
            raise ValueError("missing tracked regular file")
        metadata, name = entries[0].split(b"\t", 1)
        mode, kind, oid = metadata.split()
        if (name.decode("utf-8") != path or kind != b"blob"
                or mode not in {b"100644", b"100755"}):
            raise ValueError("expected exact regular file (no directories or symlinks)")
        text = git(root, "cat-file", "blob", oid.decode("ascii")).decode("utf-8")
        if "\0" in text:
            raise ValueError("NUL in text")
        return text
    except INPUT_ERRORS as exc:
        raise ValueError(f"{revision}:{path}: {exc}") from exc


def inventory(root: Path, revision: str, path: str):
    try:
        return clauses(read_blob(root, revision, path))
    except INPUT_ERRORS as exc:
        raise ValueError(f"inventory {revision}:{path}: {exc}") from exc


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError(f"invalid JSON constant: {value}")


def load_ledger(path: Path):
    return json.loads(path.read_text(encoding="utf-8"),
                      object_pairs_hook=unique_keys, parse_constant=invalid_constant)


def validate_ledger(data, base, path, excluded):
    if not isinstance(data, dict) or set(data) != TOP_KEYS:
        raise ValueError(f"ledger must have exactly {sorted(TOP_KEYS)}")
    if data["base_revision"] != base or data["base_path"] != path:
        raise ValueError("ledger base_revision/base_path mismatch")
    if data["excluded_lines"] != excluded:
        raise ValueError("excluded_lines differs from BASE blank-line inventory")
    rows = data["clauses"]
    if not isinstance(rows, list) or not rows:
        raise ValueError("clauses must be a nonempty list")
    for index, row in enumerate(rows, 1):
        try:
            if not isinstance(row, dict) or set(row) != ROW_KEYS:
                raise ValueError(f"row must have exactly {sorted(ROW_KEYS)}")
            for key in ("base_line", "end_line"):
                if type(row[key]) is not int or row[key] < 1:
                    raise ValueError(f"{key} must be a positive integer")
            for key in ("base_quote", "kind", "state", "destination", "reason"):
                if not isinstance(row[key], str) or "\0" in row[key]:
                    raise ValueError(f"{key} must be text without NUL")
            if not row["base_quote"].strip():
                raise ValueError("base_quote must be nonblank")
            state = row["state"]
            if state not in {"KEPT", "MOVED", "REBASED", "DROPPED"}:
                raise ValueError("unknown state; expected KEPT, MOVED, REBASED or DROPPED")
            if state == "DROPPED":
                if not row["reason"].strip() or row["destination"] != "":
                    raise ValueError("DROPPED requires nonblank reason and empty destination")
            else:
                repo_path(row["destination"])
                if row["reason"] != "":
                    raise ValueError("REBASED requires empty reason" if state == "REBASED"
                                     else "KEPT/MOVED require empty reason")
                if state == "KEPT" and row["destination"] != path:
                    raise ValueError("KEPT must use base path")
                if state != "KEPT" and row["destination"] == path:
                    raise ValueError(f"{state} must use a different path")
        except ValueError as exc:
            raise ValueError(f"row {index}: {exc}") from exc
    return rows


def is_ledger(root: Path, destination: str, ledger: Path) -> bool:
    candidate = root / destination
    if candidate.absolute() == ledger.absolute() or candidate.resolve() == ledger.resolve():
        return True
    if candidate.exists() and ledger.exists():
        return os.path.samefile(candidate, ledger)
    return False


def take_rebased(unit, path, destination, units, available, used):
    """Consume the first unconsumed destination unit that re-bases unit."""
    best, identical = None, False
    for index, candidate in enumerate(units):
        if index in used or available[match_key(candidate)] < 1:
            continue
        result, reason = rebased(unit["raw"], posixpath.dirname(path),
                                 candidate["raw"], posixpath.dirname(destination))
        if reason is None and result:
            used.add(index)
            available[match_key(candidate)] -= 1
            return None
        if reason is None:
            identical = True
        elif best is None or result > best[0]:
            best = (result, candidate["base_line"], reason)
    if identical:
        return "texts are identical; use MOVED"
    if best is None:
        return f"no unconsumed {unit['kind']} unit"
    offset, line, reason = best
    if offset < 0:
        return f"refused (BASE line {unit['base_line']}; destination line {line}): {reason}"
    base_line = unit["base_line"] + unit["raw"][:offset].count("\n")
    return (f"first difference at BASE raw offset {offset} (BASE line {base_line}; "
            f"destination line {line}): {reason}")


def check(root, base, head, path, expected, rows, ledger):
    findings, seen, destinations = [], set(), {}
    unit_lists, used = {}, {}
    by_line = {unit["base_line"]: unit for unit in expected}
    for row in rows:
        line = row["base_line"]
        label = f"BASE {base}:{path}:{line}"
        if line in seen:
            findings.append(f"{label}: duplicate ledger row")
            continue
        seen.add(line)
        if line not in by_line:
            findings.append(f"{label}: not an extracted base clause")
            continue
        if any(row[key] != by_line[line][key] for key in UNIT_KEYS):
            findings.append(f"{label}: clause metadata differs from BASE")
            continue
        if row["state"] == "DROPPED":
            continue
        destination = row["destination"]
        if is_ledger(root, destination, ledger):
            raise ValueError(f"HEAD {head}:{destination}: ledger cannot supply evidence")
        if destination not in destinations:
            units, _ = inventory(root, head, destination)
            destinations[destination] = Counter(match_key(unit) for unit in units)
            unit_lists[destination], used[destination] = units, set()
        quote = match_key(by_line[line])
        available = destinations[destination]
        if row["state"] == "REBASED":
            problem = take_rebased(by_line[line], path, destination,
                                   unit_lists[destination], available, used[destination])
            if problem:
                findings.append(f"{label}: REBASED at HEAD {head}:{destination}: {problem}")
            continue
        if available[quote] < 1:
            findings.append(f"{label}: {row['state']} whole clause occurrence missing "
                            f"at HEAD {head}:{destination}")
        else:
            available[quote] -= 1
    for line in sorted(by_line.keys() - seen):
        findings.append(f"BASE {base}:{path}:{line}: missing ledger row")
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=REPO_ROOT)
    parser.add_argument("--base", required=True, help="base git commit or revision")
    parser.add_argument("--path", required=True, help="base repository-relative file")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--extract", action="store_true", help="print JSON ledger template")
    mode.add_argument("--ledger", type=Path, help="JSON file; relative to current directory")
    args = parser.parse_args(argv)
    base, head = args.base, "HEAD (unresolved)"
    try:
        root = Path(git(args.repo, "rev-parse", "--show-toplevel").decode("utf-8").strip())
        path = repo_path(args.path)
        base = commit(root, args.base)
        expected, excluded = inventory(root, base, path)
        if not expected:
            raise ValueError("no base clauses; empty inventory cannot prove preservation")
        if args.extract:
            rows = [dict(unit, state="KEPT", destination=path, reason="") for unit in expected]
            for row in rows:
                del row["raw"]
            print(json.dumps(dict(base_revision=base, base_path=path, clauses=rows,
                                  excluded_lines=excluded), indent=2, ensure_ascii=False))
            return 0
        head = commit(root, "HEAD")
        rows = validate_ledger(load_ledger(args.ledger), base, path, excluded)
        findings = check(root, base, head, path, expected, rows, args.ledger)
    except INPUT_ERRORS as exc:
        print(f"ERROR: clause preservation: BASE {base}:{args.path}; HEAD {head}; "
              f"ledger {args.ledger}: {exc}", file=sys.stderr)
        return 2
    for finding in findings:
        print(f"FAIL: ledger {args.ledger}: {finding}")
    dropped = sum(row["state"] == "DROPPED" for row in rows)
    rebased_rows = sum(row["state"] == "REBASED" for row in rows)
    note = f"; {rebased_rows} REBASED asserted" if rebased_rows else ""
    print(f"{'FAIL' if findings else 'OK'}: {len(expected)} clauses; "
          f"{dropped} DROPPED with reasons{note}; BASE {base}:{path}; HEAD {head}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
