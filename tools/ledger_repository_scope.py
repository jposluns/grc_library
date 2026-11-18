"""Which repository owns one open-findings ledger row: the one repository-tag rule.

The operational store's open-findings ledger is shared with the successor repository
(grc_library_new). A `[repo: <name>]` clause in a row's Disposition cell names the repository
that owns the row; no clause means this repository. ``row_repository`` is the only reading of
that clause. tools/check-class-attestation-on-pr.py uses it to skip the successor's rows and to
fail closed on an unclassifiable tag, and tools/open-findings-row.py uses it to refuse writing a
row that the check would fail closed on as an unclassifiable repository tag, so the writer and
the check cannot disagree on a row's repository.

THE RULE. A `[repo: ...]` clause inside a `[class: "<token>" @ n]` span is part of the
declared token and is ignored. A clause inside a `[class-exempt: ...]` clause is not ignored: it
is read like any other clause. Any other clause is the row's repository tag only when it is the
final token of the Disposition cell (nothing but whitespace after it) and the brackets before the
tag's own `[` are balanced (every `[` is closed by a matching `]` before the tag, no `]` comes
while no `[` is open, and a closed class span is skipped as a unit, so brackets inside it do not
count). No tag, or exactly one final `[repo: grc_library]`, is 'own'. Exactly one final
`[repo: grc_library_new]` is 'foreign' only when the Found cell is exactly one ISO date on or
after SUCCESSOR_FIRST_FOUND. Everything else is 'bad': two or more tags, a tag anywhere but the
final token, a final tag after an unclosed `[` or a stray `]` (one with no `[` open) before the
tag (for example `FIXED #1 [class: "a [repo: grc_library_new]`,
`FIXED #1 [class-exempt: bogus [repo: grc_library_new]` or `ROUTED see a] [repo: grc_library]`),
any other value, or a successor tag with an earlier, annotated or invalid Found date.

Standard library only; no command-line interface.
"""
from __future__ import annotations

import datetime
import re

# A Found cell that is exactly one ISO date (full match of the stripped cell).
FOUND_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")

# A `[repo: <name>]` clause in the Disposition cell names the repository that owns the row; no
# clause means this repository.
REPO_TAG_RE = re.compile(r"\[repo:\s*([^\]\r\n]*?)\s*\]", re.IGNORECASE)
THIS_REPOSITORY = "grc_library"
FOREIGN_REPOSITORIES = ("grc_library_new",)
# The first day of the successor repository: no row of it can be found earlier.
SUCCESSOR_FIRST_FOUND = datetime.date(2026, 11, 8)


def _prefix_balanced(prefix: str, class_spans: list[tuple[int, int]]) -> bool:
    """PURE. True when the brackets in ``prefix`` are balanced: every `[` is closed by a matching
    `]` within the prefix and no `]` comes with no `[` open. Each closed class span (offsets into
    the same cell, as ``hook.CLASS_ATTEST_RE`` matched them) that lies wholly inside the prefix is
    skipped as a unit, so brackets inside it do not count and a bracket quoted in a closed token
    never unbalances it."""
    skip = {a: b for (a, b) in class_spans if b <= len(prefix)}
    depth = 0
    i = 0
    while i < len(prefix):
        if i in skip:
            i = skip[i]
            continue
        if prefix[i] == "[":
            depth += 1
        elif prefix[i] == "]":
            if depth == 0:
                return False
            depth -= 1
        i += 1
    return depth == 0


def row_repository(found_cell: str, disp: str, hook) -> str:
    """PURE. 'own' | 'foreign' | 'bad': which repository a well-formed ledger row belongs to.

    Reads the RAW Disposition cell. A `[repo: ...]` clause that falls inside a
    `[class: "<token>" @ n]` span (``hook.CLASS_ATTEST_RE``) is part of the declared token and is
    ignored; one inside a `[class-exempt: ...]` clause is not ignored. Any other `[repo: ...]`
    clause is the row's repository tag only when it is the final token of the cell (nothing but
    whitespace after it) and the brackets before the tag's own `[` are balanced
    (``_prefix_balanced``: every `[` is closed by a matching `]` before the tag, no `]` comes
    while no `[` is open, and a closed class span is skipped as a unit, so brackets inside it do
    not count). No tag, or exactly one final `[repo: grc_library]`, is 'own'. Exactly one final
    `[repo: grc_library_new]` is 'foreign' only when the Found cell is exactly one ISO date (the
    full match ``in_window`` uses) on or after SUCCESSOR_FIRST_FOUND. Everything else is 'bad'
    (fail-closed): two or more tags, a tag anywhere but the final token, a final tag after an
    unclosed `[` or a stray `]` (one with no `[` open) before the tag, any other value, or a
    successor tag with an earlier, annotated or invalid Found date.

    RESIDUAL. The balance test is a depth counter over brackets only, so the `[` of a `[class:`
    opener whose token is not closed is closed by the `]` that brings the depth back to the
    opener's level, even when that `]` sits inside the token's quotes. With no other bracket in
    the token, that is the first `]`: with a Found date on or after SUCCESSOR_FIRST_FOUND,
    `FIXED #1 [class: "a ] [repo: grc_library_new]` reads as 'foreign', not 'bad'. A bracket pair
    inside the token is counted first, so `FIXED #1 [class: "a [b] ] [repo: grc_library_new]`
    closes the opener at its second `]` and reads as 'foreign' too. The same reading makes a
    closed, unquoted class-like bracket that ``hook.CLASS_ATTEST_RE`` does not match (for example
    `[class: some-name]`) one balanced pair, as live successor rows need."""
    class_spans = [m.span() for m in hook.CLASS_ATTEST_RE.finditer(disp)]
    tags = [
        m
        for m in REPO_TAG_RE.finditer(disp)
        if not any(a <= m.start() and m.end() <= b for (a, b) in class_spans)
    ]
    if not tags:
        return "own"
    if len(tags) > 1:
        return "bad"
    if disp[tags[0].end():].strip():
        return "bad"
    if not _prefix_balanced(disp[:tags[0].start()], class_spans):
        return "bad"
    value = tags[0].group(1)
    if value == THIS_REPOSITORY:
        return "own"
    if value not in FOREIGN_REPOSITORIES:
        return "bad"
    m = FOUND_DATE_RE.fullmatch((found_cell or "").strip())
    if not m:
        return "bad"
    try:
        found_date = datetime.date.fromisoformat(m.group(1))
    except ValueError:
        return "bad"
    return "foreign" if found_date >= SUCCESSOR_FIRST_FOUND else "bad"
