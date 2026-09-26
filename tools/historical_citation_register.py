"""The historical-context citation exception register: its data file, table and page sync (3b75).

The rows live in a TOML data file; the Markdown register page is a hand-written view whose table,
between two sentinel comments, is GENERATED from the data (tools/build-historical-citation-
exceptions.py). Gate 6 reads the data file only, so what the page renders can never change what is
sanctioned, and it refuses a page whose generated table differs from the data (maintainer ruling
2026-09-26, after ten QA rounds found Markdown shapes that rendered differently from what a parser
read).

load() applies the structural checks (strict TOML, exact keys, exact types, printable single-line
ASCII strings); the wrapper applies the policy checks on each row. Stdlib only.
"""
from __future__ import annotations

import datetime as _dt
import re
import tomllib

DATA_REL = ".project-governance/register-historical-citation-exceptions.toml"
PAGE_REL = ".project-governance/register-historical-citation-exceptions.md"
BEGIN = ("<!-- BEGIN-GENERATED historical-citation-exceptions: edit the .toml data file, then run "
         "python3 tools/build-historical-citation-exceptions.py -->")
END = "<!-- END-GENERATED historical-citation-exceptions -->"
FIELDS = ("id", "path", "citation", "sentence", "reason", "upstream", "verified")
HEADER = ("Exception ID", "Path", "Citation", "Sentence", "Reason", "Upstream check location",
          "Last verified (UTC)")
_PRINTABLE = re.compile(r"[\x20-\x7e]+")


class RegisterDataError(ValueError):
    """The data file is malformed (exit 1 in gate 6; exit 2 in the build tool's --check)."""


def load(text: str) -> list[dict]:
    """Parse the data file strictly and return its rows in file order."""
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        # The message carries a line and column; the document's content is not echoed.
        raise RegisterDataError(f"historical register data: not valid TOML ({exc})") from None
    if set(data) - {"schema_version", "exception"} or "schema_version" not in data:
        raise RegisterDataError("historical register data: top-level keys must be schema_version "
                                "and, optionally, exception")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise RegisterDataError("historical register data: schema_version must be the integer 1")
    rows = data.get("exception", [])
    if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
        raise RegisterDataError("historical register data: exception must be an array of tables")
    for n, row in enumerate(rows, 1):
        where = f"historical register data: exception {n}"
        if set(row) != set(FIELDS):
            missing = sorted(set(FIELDS) - set(row)); extra = sorted(set(row) - set(FIELDS))
            raise RegisterDataError(f"{where}: fields must be exactly {', '.join(FIELDS)}"
                                    f" (missing {missing or 'none'}, unknown {extra or 'none'})")
        if type(row["verified"]) is not _dt.date:
            # An exact type test: a TOML datetime is a date subclass and is refused.
            raise RegisterDataError(f"{where}: verified must be a TOML date (YYYY-MM-DD)")
        for key in FIELDS[:-1]:
            value = row[key]
            if not isinstance(value, str) or not _PRINTABLE.fullmatch(value) or value != value.strip():
                raise RegisterDataError(f"{where}: {key} must be a non-empty single-line printable "
                                        "ASCII string with no leading or trailing space")
    return rows


def escape(cell: str) -> str:
    """Backslash-escape every ASCII punctuation character, so no cell can introduce markup."""
    return re.sub(r"([!-/:-@\[-`{-~])", r"\\\1", cell)


def render(rows: list[dict]) -> str:
    """The generated block: the sentinels and the table, one row per exception."""
    lines = [BEGIN, "", "| " + " | ".join(HEADER) + " |", "|" + " --- |" * len(HEADER)]
    for row in rows:
        cells = [row[k].isoformat() if k == "verified" else row[k] for k in FIELDS]
        lines.append("| " + " | ".join(escape(c) for c in cells) + " |")
    lines += ["", END]
    return "\n".join(lines)


def page_block(page: str) -> str | None:
    """The page's generated block, sentinels included, or None when the pair is absent or broken."""
    if page.count(BEGIN) != 1 or page.count(END) != 1:
        return None
    start, end = page.index(BEGIN), page.index(END)
    return page[start:end + len(END)] if start < end else None


def sync_problem(page: str | None, rows: list[dict]) -> str | None:
    """Why the page is out of step with the data, or None when it matches."""
    if page is None:
        return f"{PAGE_REL} is missing; run python3 tools/build-historical-citation-exceptions.py"
    block = page_block(page)
    if block is None:
        return f"{PAGE_REL}: the generated-table sentinels are missing or out of order"
    if block != render(rows):
        return (f"{PAGE_REL}: the generated table differs from {DATA_REL}; run "
                "python3 tools/build-historical-citation-exceptions.py")
    # The page must SHOW the generated table as the only table (3b75 QA, codex and claude): the
    # block stands alone at column 1, and the rest of the page carries no front matter, no raw
    # HTML or comment, no fence marker, and no pipe, any of which could hide the real table or
    # show a fake one.
    start = page.index(BEGIN)
    after = start + len(block)
    if re.match(r"\A\ufeff?(?:---|\+\+\+)[ \t]*\n", page):
        # Front matter renders as a table on GitHub (3b75 redesign QA r3, codex).
        return f"{PAGE_REL}: front matter at the top of the page"
    # A Markdown blank line may hold spaces or tabs (3b75 redesign QA r2, codex).
    if not re.search(r"(?:\A|\n[ \t]*\n)\Z", page[:start]) or not re.match(
        r"(?:\n?\Z|\n[ \t]*\n)", page[after:]
    ):
        return f"{PAGE_REL}: the generated block must stand alone, with a blank line before and after it"
    outside = page[:start] + page[after:]
    for n, line in enumerate(outside.splitlines(), 1):
        if re.search(r"<[A-Za-z/!?]", line):
            return f"{PAGE_REL}: raw HTML or a comment outside the generated block"
        if "```" in line or "~~~" in line:
            # Any fence marker, wherever it sits (a quoted or listed fence too; 3b75 redesign QA r3,
            # claude): the page's prose needs none.
            return f"{PAGE_REL}: a fence marker outside the generated block"
        if "|" in line:
            # Any pipe: a GFM table needs one in its delimiter row, with or without outer pipes
            # (3b75 redesign QA r2, claude, codex, gemini), so none may appear outside the block.
            return f"{PAGE_REL}: a table (or a pipe) outside the generated block"
    return None


def with_block(page: str, rows: list[dict]) -> str:
    """The page with its generated block replaced by the rendering of rows."""
    block = page_block(page)
    if block is None:
        raise RegisterDataError(f"{PAGE_REL}: the generated-table sentinels are missing or out of order")
    return page.replace(block, render(rows), 1)
