#!/usr/bin/env python3
"""On-demand instruction-cut ledger check; stdlib-only Python 3.11.

--extract prints a ledger bound to resolved BASE and --path, initially KEPT.
Review every row. KEPT requires the same path at committed HEAD; MOVED requires
another tracked text file; DROPPED requires a nonblank reason. A move asserts
presence, not that the destination gained the text since BASE.

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

Relative links: every row is first matched exactly, as above, with occurrences
consumed in ledger order. Only a row left without an exact match may then match
a remaining destination unit whose link key equals its own, so resolution can
turn a mismatch into a match but never a match into a mismatch. A link key
exists only when every condition below holds; otherwise the unit is compared
exactly. The unit is a paragraph, list item or heading. Its group (adjacent
units with no blank line between them) contains no |, tab, ]:, escaped
backtick, blockquote marker, or < followed by a letter, /, ! or ?, and is not
inside a multi-line HTML block. Each unit's first line is indented at most
three spaces, list content at most four spaces after its marker, and no later
line starts a heading, thematic break or setext underline. No backtick span
crosses a unit boundary. Every ]( outside code spans closes a plain
[label](target) link or image: the label has no [, ], backtick or backslash;
no backslash or ] precedes it; no www. or :// occurs in the label or earlier
in the same word; the target has no whitespace, parentheses, <, > or
backslash. Every fence line in the file must be a top-level fence that
container-aware CommonMark parses the same way: no container marker before it,
no indentation of four or more spaces, no backtick in a backtick fence's info
string, no fence line outdented from its opener, no deeper potential closer
inside the fence, and no tag-like < in the lines directly above an opener.
Schemed and /-rooted targets stay exact inside a link key. A unit has no link
key if any other target contains & or %, is empty, query-only or anchor-only,
ends in a . or .. segment, or leaves the repository. Remaining targets resolve
lexically against the unit's own file directory: only dot segments are
removed; empty segments, trailing slashes, queries and fragments stay exact.
Reference definitions and reference-style links are never resolved. No
filesystem/symlink resolution, existence check or network access occurs.

Disclosed residual: this lexical partition is not a CommonMark renderer or
semantic proof. HTML comments/blocks, indented code, and blockquote/list
container context are not modeled for exact matches. Wrapping a paragraph in a
multiline HTML comment, or indenting it as code, can still satisfy KEPT. List
indentation is lexical, not relative to a parsed parent. Equal-depth
re-parenting, section moves and ordering are unchecked. A relative or
anchor-only link moved unchanged to another file still matches exactly, as at
base, though it may now point elsewhere. Escaped backticks, HTML/CSS hiding,
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
import json
import os
from pathlib import Path
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


LINK = re.compile(r"\[([^\[\]\\`\0\n]*)\]\(([^\s()<>\\\0]*)\)")
SCHEME = re.compile(r"[A-Za-z][A-Za-z0-9+.-]*:")
TAG = re.compile(r"<[A-Za-z/!?]")
QUOTE = re.compile(r" *(?:(?:[-+*]|[0-9]{1,9}[.)]) +)*>")
CONTAINER = re.compile(r"(?:[ \t]*(?:>|[-+*](?=[ \t]|$)|[0-9]{1,9}[.)](?=[ \t]|$)))*[ \t]*")
HTML_BLOCK = re.compile(r"<(?:(!--)|(\?)|(!\[cdata\[)|(![a-z])|(pre|script|style|textarea)(?=[\s>]|$))")
HTML_END = ("-->", "?>", "]]>", ">")


def unit_lines(unit: dict) -> list[str]:
    text = unit["base_quote"]
    if unit["kind"] != "fence":
        return text.split("\n")
    return [line.removesuffix("\r") for line in text.removesuffix("\n").split("\n")]


def indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def mask(text: str) -> str:
    """Blank exact backtick spans so no link inside one is ever matched."""
    return "".join("\0" * len(part) if literal else part
                   for literal, part in inline_parts(text))


def fence_plain(unit: dict) -> bool:
    """A top-level fence that container-aware CommonMark parses the same way."""
    lines = unit_lines(unit)
    opener = FENCE.match(lines[0])
    width, marker = indent(lines[0]), opener[1]
    if marker[0] == "`" and "`" in opener[2]:
        return False
    if any(line.strip() and indent(line) < width for line in lines[1:]):
        return False
    closer = re.compile(re.escape(marker[0]) + "{" + str(len(marker)) + r",}[ \t]*")
    return not any(closer.fullmatch(line.lstrip(" \t")) for line in lines[1:-1])


def group_plain(group: list[dict]) -> bool:
    """Adjacent units qualify only if no context can change what a link means."""
    text = "\n".join(unit["base_quote"] for unit in group)
    if TAG.search(text) or re.search(r"\||\t|\]:|\\`", text):
        return False
    breaks, offset = set(), 0
    for unit in group:
        lines = unit["base_quote"].split("\n")
        if indent(lines[0]) > 3:
            return False
        if unit["kind"] == "list_item":
            item = LIST.match(lines[0])
            if len(item[0]) - item.end(2) > 4:
                return False
        for number, line in enumerate(lines):
            rest = line.lstrip(" ")
            if QUOTE.match(line):
                return False
            underline = unit["kind"] == "heading" and number == len(lines) - 1
            if number and not underline and (ATX.match(rest) or RULE.fullmatch(rest)
                                             or SETEXT.fullmatch(rest)):
                return False
        offset += len(unit["base_quote"])
        breaks.add(offset)
        offset += 1
    offset = 0
    for literal, part in inline_parts(text):
        if literal and any(offset <= point < offset + len(part) for point in breaks):
            return False
        offset += len(part)
    masked, closed = mask(text), set()
    for link in LINK.finditer(masked):
        word = re.split(r"\s", masked[:link.start()])[-1] + link[1]
        if (masked[link.start() - 1:link.start()] in {"\\", "]"}
                or re.search(r"(?i)www\.|://", word)):
            continue
        closed.add(link.end(1))
    return all(found.start() in closed for found in re.finditer(r"\]\(", masked))


def link_units(units: list[dict]) -> set[int]:
    """Indexes of units in plain groups; none when any fence could parse differently."""
    groups, tainted, html_end = [], set(), None
    for index, unit in enumerate(units):
        adjacent = index > 0 and units[index - 1]["end_line"] + 1 == unit["base_line"]
        joined = adjacent and units[index - 1]["kind"] != "fence"
        if unit["kind"] == "fence":
            if not fence_plain(unit):
                return set()
            if joined and any(TAG.search(units[i]["base_quote"]) for i in groups[-1]):
                return set()
            continue
        if not joined:
            groups.append([])
        groups[-1].append(index)
        for line in unit_lines(unit):
            content = CONTAINER.sub("", line, count=1)
            if content.startswith(("```", "~~~")):
                return set()
            if html_end is not None:
                tainted.add(index)
                if html_end in line.lower():
                    html_end = None
                continue
            opened = HTML_BLOCK.match(content.lower())
            if opened:
                tainted.add(index)
                kind = opened.lastindex
                end = HTML_END[kind - 1] if kind < 5 else "</" + opened[5] + ">"
                if end not in content.lower()[opened.end():]:
                    html_end = end
    return {index for group in groups
            if not tainted.intersection(group) and group_plain([units[i] for i in group])
            for index in group}


def rebase(target: str, path: str):
    """Repository path of a plain relative target, or None when not unambiguous."""
    if not target or target[0] in "?#" or re.search(r"[&%]", target):
        return None
    cut = re.search(r"[?#]|$", target).start()
    segments = target[:cut].split("/")
    if segments[-1] in {".", ".."}:
        return None
    parts = path.split("/")[:-1]
    for segment in segments:
        if segment == "..":
            if not parts:
                return None
            parts.pop()
        elif segment != ".":
            parts.append(segment)
    value = json.dumps(["relative", "/".join(parts), target[cut:]])
    return "\0" + value.encode("ascii").hex() + "\0"


def link_key(unit: dict, path: str):
    """match_key with plain relative targets rebased, or None if any is ambiguous."""
    text, pieces, last = unit["base_quote"], [], 0
    for link in LINK.finditer(mask(text)):
        target = link[2]
        if target.startswith("/") or SCHEME.match(target):
            continue
        value = rebase(target, path)
        if value is None:
            return None
        pieces += [text[last:link.start(2)], value]
        last = link.end(2)
    if not pieces:
        return None
    return match_key(dict(unit, base_quote="".join(pieces) + text[last:]))


def link_keys(units: list[dict], path: str) -> list:
    scope = link_units(units)
    return [link_key(unit, path) if index in scope else None
            for index, unit in enumerate(units)]


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
                                      else "\n".join(lines[start:i]))))
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
            if state not in {"KEPT", "MOVED", "DROPPED"}:
                raise ValueError("unknown state; expected KEPT, MOVED or DROPPED")
            if state == "DROPPED":
                if not row["reason"].strip() or row["destination"] != "":
                    raise ValueError("DROPPED requires nonblank reason and empty destination")
            else:
                repo_path(row["destination"])
                if row["reason"] != "":
                    raise ValueError("KEPT/MOVED require empty reason")
                if state == "KEPT" and row["destination"] != path:
                    raise ValueError("KEPT must use base path")
                if state == "MOVED" and row["destination"] == path:
                    raise ValueError("MOVED must use a different path")
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


def check(root, base, head, path, expected, rows, ledger):
    findings, seen, destinations, unmatched = [], set(), {}, []
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
            exact = {}
            for index, unit in enumerate(units):
                exact.setdefault(match_key(unit), []).append(index)
            destinations[destination] = exact, link_keys(units, destination), set()
        exact, _, used = destinations[destination]
        available = exact.get(match_key(by_line[line]), [])
        if available:
            used.add(available.pop(0))
        else:
            unmatched.append((len(findings), line, destination))
            findings.append(f"{label}: {row['state']} whole clause occurrence missing "
                            f"at HEAD {head}:{destination}")
    if unmatched:
        own = dict(zip(by_line, link_keys(expected, path)))
        for position, line, destination in unmatched:
            _, links, used = destinations[destination]
            match = next((index for index, key in enumerate(links) if key is not None
                          and key == own[line] and index not in used), None)
            if match is not None:
                used.add(match)
                findings[position] = None
    findings = [finding for finding in findings if finding is not None]
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
    print(f"{'FAIL' if findings else 'OK'}: {len(expected)} clauses; "
          f"{dropped} DROPPED with reasons; BASE {base}:{path}; HEAD {head}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
