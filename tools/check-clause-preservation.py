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

After table-cell splitting, inline Markdown link/image destinations and
reference-definition destinations are resolved lexically against each unit's
own repository file directory. Relative paths normalize dot segments,
Markdown punctuation escapes and semicolon-terminated entities in one pass,
and percent-encoded ASCII unreserved bytes only. Reserved/other percent escapes
and empty path segments remain distinct; query and fragment spelling stays
exact. Empty, query-only and anchor-only destinations refer to the source file.
Schemed URLs, network-path URLs and absolute paths stay byte-exact. A relative target escaping the repository is an input error,
even in a dropped base unit or an unused unit of a named destination file.
No filesystem/symlink resolution, existence checks or network access occurs.
Link labels, titles and delimiters retain the existing normalization rules.
Fences, indented code lines, inline code, autolinks and raw HTML tokens remain
literal. Definition syntax cannot interrupt ordinary paragraph text. Invalid
parenthesized titles are not resolved. Ambiguous container/HTML block context
still requires manual review; this is deliberately a conservative lexer.

Disclosed residual: this lexical partition is not a CommonMark renderer or
semantic proof. HTML block boundaries and blockquote/list container context are not fully
modeled. Indented text retains the old whitespace comparison, but its targets
are not resolved. Wrapping a paragraph in a multiline HTML
comment, or indenting it as code, can still satisfy KEPT. List indentation
is lexical, not relative to a parsed parent. Equal-depth re-parenting,
section moves and ordering are unchecked. Escaped backticks, HTML/CSS hiding,
reference-use binding, duplicate definitions, HTML links and other
renderer-specific effects require
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
import html
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


def table_cells(text: str, normalize_cells: bool = True) -> tuple[str, ...]:
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
    return tuple(normalize(cell) if normalize_cells else cell for cell in cells)


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


PUNCT_ESCAPE = re.compile(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_\x60{|}~])")


def decoded_target(raw: str):
    """Decode escapes/entities once, retaining offsets into the original target."""
    pieces, offsets = [], []
    i = 0
    while i < len(raw):
        escape = PUNCT_ESCAPE.match(raw, i)
        entity = re.match(r"&(?:#[xX][0-9A-Fa-f]{1,6};|#[0-9]{1,7};|[A-Za-z][A-Za-z0-9]*;)", raw[i:])
        if escape:
            value, end = escape[1], escape.end()
        elif entity and (entity[0].startswith("&#") or entity[0][1:] in html.entities.html5):
            value, end = html.unescape(entity[0]), i + entity.end()
        else:
            value, end = raw[i], i + 1
        pieces.append(value)
        offsets.extend([i] * len(value))
        i = end
    return "".join(pieces), offsets


SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
DEFINITION = re.compile(
    r"(?m)^[ \t]*(?:>[ \t]*)*(?:(?:[-+*]|[0-9]{1,9}[.)])[ \t]+)?"
    r"\[(?:\\[^\n]|[^\[\]\\])+\]:[ \t]*(?:\n[ \t]*)?")


def target_key(raw: str, path: str) -> str:
    """Resolve lexical paths; only percent-encoded ASCII unreserved bytes fold."""
    decoded, offsets = decoded_target(raw)
    if decoded.startswith("/") or SCHEME.match(decoded):
        value = ("external", raw)
    else:
        delimiter = re.search(r"[?#]", decoded)
        split = delimiter.start() if delimiter else len(decoded)
        plain = decoded[:split]
        suffix = raw[offsets[split]:] if delimiter else ""
        plain = re.sub(r"%([0-9A-Fa-f]{2})", lambda m:
                       chr(int(m[1], 16)) if chr(int(m[1], 16)) in
                       "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
                       else m[0], plain)
        if "\0" in plain or "\\" in plain or plain.startswith("/"):
            raise ValueError(f"{path}: invalid relative Markdown target {raw!r}")
        parts = path.split("/")[:-1] if plain else path.split("/")
        for part in plain.split("/") if plain else ():
            if part == ".":
                continue
            if part == "..":
                if not parts:
                    raise ValueError(f"{path}: Markdown target outside repository: {raw!r}")
                parts.pop()
            else:
                parts.append(part)
        value = ("relative", "/".join(parts), suffix)
    return "\0" + json.dumps(value, ensure_ascii=True).encode("utf-8").hex() + "\0"


def destination(text: str, start: int):
    """Return target span and next position; support angles and balanced parens."""
    if start < len(text) and text[start] == "<":
        i = start + 1
        while i < len(text):
            if text[i] == "\\" and i + 1 < len(text):
                i += 2
                continue
            if text[i] == ">":
                return start + 1, i, i + 1
            if text[i] in "<\r\n":
                return None
            i += 1
        return None
    i, depth = start, 0
    while i < len(text):
        char = text[i]
        if char == "\\" and i + 1 < len(text):
            i += 2
            continue
        if char in " \t\r\n":
            break
        if char == "(":
            depth += 1
        elif char == ")":
            if not depth:
                break
            depth -= 1
        elif char in "<>" or ord(char) < 32:
            return None
        i += 1
    return None if depth else (start, i, i)


def title_end(text: str, start: int):
    """Parenthesized titles cannot contain unescaped opening parentheses."""
    if start == len(text) or text[start] not in "\"'(":
        return None
    closing = ")" if text[start] == "(" else text[start]
    i = start + 1
    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text):
            i += 2
            continue
        if closing == ")" and text[i] == "(":
            return None
        if text[i] == closing:
            return i + 1
        i += 1
    return None


def link_end(text: str, cursor: int):
    """Accept closing ')' or whitespace followed by an optional Markdown title."""
    i = cursor
    while i < len(text) and text[i] in " \t\r\n":
        i += 1
    if i < len(text) and text[i] == ")":
        return i + 1
    if i == cursor:
        return None
    i = title_end(text, i)
    if i is None:
        return None
    while i < len(text) and text[i] in " \t\r\n":
        i += 1
    return i + 1 if i < len(text) and text[i] == ")" else None


def definition_end(text: str, cursor: int):
    """Find a definition's end, excluding link-like text in its optional title."""
    i = cursor
    while i < len(text) and text[i] in " \t":
        i += 1
    line_end = i
    if i < len(text) and text[i] in "\r\n":
        if text[i:i + 2] == "\r\n":
            i += 2
        else:
            i += 1
        while i < len(text) and text[i] in " \t":
            i += 1
    end = title_end(text, i) if i > cursor else None
    if end is not None:
        while end < len(text) and text[end] in " \t":
            end += 1
        if end == len(text) or text[end] in "\r\n":
            return end
    if line_end == len(text) or text[line_end] in "\r\n":
        return line_end
    return None


def resolve_links(text: str, path: str) -> str:
    """Rewrite destination spans only; leave labels, titles and code untouched."""
    masked = "".join(" " * len(part) if literal else part
                     for literal, part in inline_parts(text))
    # Treat autolinks, raw HTML and indented lines as opaque, like code spans.
    # Over-masking unusual angle syntax is conservative: it cannot approve a move.
    opaque = re.compile(r"<!--[\s\S]*?(?:-->|$)|<\?[\s\S]*?(?:\?>|$)|"
                        r"<!\[CDATA\[[\s\S]*?(?:\]\]>|$)|"
                        r"<(?:\"[^\"]*\"|'[^']*'|[^'\">])*>|"
                        r"(?m:^[ ]{0,3}\t[^\n]*|^[ ]{4}[^\n]*)")
    masked = opaque.sub(lambda m: " " * len(m[0]), masked)
    spans, definitions = {}, {}
    stop = 0
    for match in DEFINITION.finditer(text):
        if (match.start() < stop or text[stop:match.start()].strip()
                or not masked[match.start():match.end()].strip()):
            continue
        found = destination(text, match.end())
        if found is not None:
            left, right, cursor = found
            end = definition_end(text, cursor)
            if end is not None and (right > left or text[match.end():cursor] == "<>"):
                spans[left] = (right, target_key(text[left:right], path))
                definitions[match.start()] = stop = end
    stack = []
    i = 0
    while i < len(masked):
        if i in definitions:
            i = definitions[i]
            continue
        if i in spans:
            i = spans[i][0]
            continue
        if masked[i] == "\\":
            i += 2
            continue
        if masked[i] == "[":
            stack.append(i)
        elif masked[i] == "]" and stack:
            stack.pop()
            if masked[i + 1:i + 2] == "(":
                start = i + 2
                while start < len(text) and text[start] in " \t\r\n":
                    start += 1
                if start > i + 2 and text[start:start + 1] in {"'", '"'}:
                    found = (i + 2, i + 2, i + 2)
                else:
                    found = destination(text, start)
                if found is not None:
                    left, right, cursor = found
                    end = link_end(text, cursor)
                    if end is not None:
                        spans[left] = (right, target_key(text[left:right], path))
                        i = end
                        continue
        i += 1
    for left, (right, value) in sorted(spans.items(), reverse=True):
        text = text[:left] + value + text[right:]
    return text


def file_key(unit: dict, path: str) -> tuple:
    """Split table structure before resolving any destination inside a cell."""
    text = unit["base_quote"]
    if re.match(r"^(?: {4}| {0,3}\t)", text):
        return match_key(unit)
    if unit["kind"] == "table_row":
        unit = dict(unit, base_quote="|".join(resolve_links(cell, path)
                    for cell in table_cells(text, normalize_cells=False)))
        return match_key(unit)
    if unit["kind"] != "fence":
        unit = dict(unit, base_quote=resolve_links(unit["base_quote"], path))
    return match_key(unit)


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
        units, excluded = clauses(read_blob(root, revision, path))
        for unit in units:
            file_key(unit, path)  # Validate even --extract and DROPPED units.
        return units, excluded
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
    findings, seen, destinations = [], set(), {}
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
            destinations[destination] = Counter(file_key(unit, destination) for unit in units)
        quote = file_key(by_line[line], path)
        available = destinations[destination]
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
