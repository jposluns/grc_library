"""Section 7.1 publisher data: the machine-readable source of record (3b31b redesign).

The citation-verification specification's section 7.1 carries ONE fenced block whose info string
is exactly ``json citation-publishers``. It is the source of record for the publisher allow-list:
``tools/build-citation-publishers.py`` renders the human-readable table from it between the
``BEGIN-GENERATED citation-publishers`` sentinels (gate 102 runs its ``--check``), and
``tools/lint-allowlist-spec-parity.py`` (gate 101) compares the external-link ALLOW_LIST with the
domains it declares. No code parses a Markdown table: nine QA rounds showed that hand-parsing a
GFM table for a gate is an open-ended class (maintainer ruling 2026-09-24, option A).

Schema: a JSON array in render order; each entry is exactly
``{"publisher": str, "domains": [str, ...], "covers": str}``. Every rule below fails loud
(``InputError``), never silently: exactly one block, inside section 7.1; strict JSON (duplicate
keys and NaN/Infinity rejected); exact keys and types; non-empty trimmed strings; publisher and
covers free of ``|``, backticks and line breaks (so the render needs no escaping); every domain a
canonical lowercase host (no scheme, no trailing dot, at least one dot); no duplicate publisher or
domain.
"""
from __future__ import annotations

import json
import re

BLOCK_INFO = "json citation-publishers"
BEGIN = "<!-- BEGIN-GENERATED citation-publishers -->"
END = "<!-- END-GENERATED citation-publishers -->"
KEYS = ("publisher", "domains", "covers")
HOST_RE = re.compile(r"[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)+")
# Any fence-like line naming the block, in ANY fence style (indentation, tildes, longer runs,
# trailing space), is counted, so a second or non-canonical block cannot be silently ignored.
LOOSE_OPEN_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})[ \t]*json[ \t]+citation-publishers\b.*$")
CANONICAL_OPEN = "```" + BLOCK_INFO
CLOSE_RE = re.compile(r"^ {0,3}`{3,}[ \t]*$")
HEADING_RE = re.compile(r"^ {0,3}#{1,3}[ \t]")
SECTION_RE = re.compile(r"^ {0,3}### 7\.1[ \t]")
HEADER = "| Publisher | Canonical domain | Standards covered |\n| --- | --- | --- |\n"


class InputError(Exception):
    """The section 7.1 source of record is missing or malformed."""


def normalize(text: str) -> str:
    """CRLF and CR line endings to LF, and a leading BOM removed, before any structural read."""
    return text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")


def _fence_scan(lines: list[str]) -> tuple[set[int], set[int]]:
    """(lines inside a fenced code block, lines that OPEN a top-level fence), for any backtick or
    tilde fence of 3 or more, so a heading or block inside an example code block is not structure."""
    inside, marker, out, starts = False, "", set(), set()
    for i, line in enumerate(lines):
        m = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if not inside and m:
            inside, marker = True, m.group(1)
            out.add(i)
            starts.add(i)
            continue
        if inside:
            out.add(i)
            if re.match(r"^ {0,3}" + re.escape(marker[0]) + "{" + str(len(marker)) + r",}[ \t]*$", line):
                inside = False
    return out, starts


def opener_line(text: str) -> int:
    """Line index of the single canonical block opener (validated as in block_text)."""
    lines = text.split("\n")
    loose = [i for i, line in enumerate(lines) if LOOSE_OPEN_RE.match(line)]
    if len(loose) != 1:
        raise InputError(f"expected exactly one ```{BLOCK_INFO} block (any fence style counts), found {len(loose)}")
    return loose[0]


def section_bounds(text: str) -> tuple[int, int]:
    """Character span of section 7.1's body (after its heading, up to the next #, ## or ### heading),
    reading headings only outside fenced code blocks and allowing up to three spaces of indent."""
    lines = text.split("\n")
    fenced, _ = _fence_scan(lines)
    heads = [i for i, line in enumerate(lines) if i not in fenced and SECTION_RE.match(line)]
    if len(heads) != 1:
        raise InputError(f"expected exactly one section 7.1 heading outside code blocks, found {len(heads)}")
    h = heads[0]
    nxt = next((k for k in range(h + 1, len(lines)) if k not in fenced and HEADING_RE.match(lines[k])), len(lines))
    start = sum(len(line) + 1 for line in lines[:h + 1])
    end = sum(len(line) + 1 for line in lines[:nxt]) if nxt < len(lines) else len(text)
    return start, end


def _reject_duplicate_keys(pairs):
    keys = [k for k, _ in pairs]
    dup = sorted({k for k in keys if keys.count(k) > 1})
    if dup:
        raise InputError(f"duplicate key(s) in a publisher entry: {', '.join(dup)}")
    return dict(pairs)


def _reject_constant(name):
    raise InputError(f"non-finite number {name} is not allowed")


def block_lines(text: str) -> tuple[int, int]:
    """(opener line index, closing-fence line index) of the single validated block in section 7.1."""
    start, end = section_bounds(text)
    lines = text.split("\n")
    i = opener_line(text)
    if i not in _fence_scan(lines)[1]:
        raise InputError(f"the {BLOCK_INFO} block is nested inside another code block")
    if lines[i] != CANONICAL_OPEN:
        raise InputError(f"the {BLOCK_INFO} block must open with exactly ```{BLOCK_INFO} (unindented, backticks)")
    offset = sum(len(line) + 1 for line in lines[:i])
    if not start <= offset < end:
        raise InputError(f"the ```{BLOCK_INFO} block is not inside section 7.1")
    try:
        close = next(k for k in range(i + 1, len(lines)) if CLOSE_RE.match(lines[k]))
    except StopIteration:
        raise InputError(f"the ```{BLOCK_INFO} block is not closed") from None
    if sum(len(line) + 1 for line in lines[:close]) >= end:
        raise InputError(f"the ```{BLOCK_INFO} block runs past the end of section 7.1")
    return i, close


def source_span(text: str) -> tuple[int, int]:
    """Character span of the whole source block, opener line through closing-fence line."""
    i, close = block_lines(text)
    lines = text.split("\n")
    return sum(len(line) + 1 for line in lines[:i]), sum(len(line) + 1 for line in lines[:close + 1])


def block_text(text: str) -> str:
    """The JSON body of the single ``json citation-publishers`` block inside section 7.1."""
    i, close = block_lines(text)
    return "\n".join(text.split("\n")[i + 1:close])


def parse_block(text: str) -> list[dict]:
    """Validated publisher entries, in render order, from the specification text."""
    raw = block_text(normalize(text))
    try:
        data = json.loads(raw, object_pairs_hook=_reject_duplicate_keys, parse_constant=_reject_constant)
    except json.JSONDecodeError as exc:
        raise InputError(f"malformed JSON in the ```{BLOCK_INFO} block: {exc}") from None
    if not isinstance(data, list) or not data:
        raise InputError("the publisher block must be a non-empty JSON array")
    seen_pub: set[str] = set()
    seen_dom: set[str] = set()
    for n, entry in enumerate(data, 1):
        where = f"entry {n}"
        if not isinstance(entry, dict) or tuple(sorted(entry)) != tuple(sorted(KEYS)):
            raise InputError(f"{where}: must be an object with exactly the keys {', '.join(KEYS)}")
        for key in ("publisher", "covers"):
            value = entry[key]
            if not isinstance(value, str) or not value.strip() or value != value.strip():
                raise InputError(f"{where}: {key!r} must be a non-empty, trimmed string")
            if any(ch in value for ch in "|`\n\r"):
                raise InputError(f"{where}: {key!r} must not contain a pipe, a backtick or a line break")
        pub = entry["publisher"]
        if pub in seen_pub:
            raise InputError(f"{where}: duplicate publisher {pub!r}")
        seen_pub.add(pub)
        domains = entry["domains"]
        if not isinstance(domains, list) or not domains:
            raise InputError(f"{where} ({pub}): 'domains' must be a non-empty array")
        for dom in domains:
            if not isinstance(dom, str) or len(dom) > 253 or not HOST_RE.fullmatch(dom):
                raise InputError(f"{where} ({pub}): {dom!r} is not a canonical lowercase host")
            if dom in seen_dom:
                raise InputError(f"{where} ({pub}): duplicate domain {dom!r}")
            seen_dom.add(dom)
    return data


def render(entries: list[dict]) -> str:
    """The deterministic GFM table for the entries (header, delimiter, one row per entry)."""
    rows = [
        f"| {e['publisher']} | {', '.join('`' + d + '`' for d in e['domains'])} | {e['covers']} |\n"
        for e in entries
    ]
    return HEADER + "".join(rows)


def domains(text: str) -> set[str]:
    """Every domain the section 7.1 source of record declares."""
    return {d for e in parse_block(text) for d in e["domains"]}
