#!/usr/bin/env python3
"""Pack-owned standards-currency engine.

The original compile_entry_patterns/check_file/run API remains available.
coverage_report adds register-independent discovery and review inventories.
The project wrapper supplies parsed entries, files, policy and CLI defaults.

Report mode blocks only findings produced by the original Markdown
check_file path. Newly discovered stale forms, HTML findings and coverage
findings remain advisory. Explicit enforce mode additionally blocks
recognized stale, unregistered, noncanonical and unpinned citations.
Ambiguity, candidate forms and unresolved editions remain review inventories.
coverage_report also accepts wrapper-validated historical-context declarations;
the engine masks only the declared occurrences inside one bound sentence, and a
declaration that does not bind blocks in every mode (3b75).

No register schema, repository roots, publisher lookup or current-version
catalogue is owned here.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise ImportError(
        "the aiqt_corpus module is unavailable: run through the project wrapper "
        "(python3 tools/lint-standards-currency.py), which bootstraps the vendored copy, "
        "or put the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc


def compile_entry_patterns(
    entries: list[dict[str, object]],
) -> list[tuple[str | None, re.Pattern[str], str]]:
    """Compile one (prefilter, pattern, finding-message) triple per (entry, superseded version).

    Compiled once per run rather than per scanned line: the patterns depend only on the
    register entries, and rebuilding them inside the per-line scan loop dominated runtime.
    The triple order preserves the register's entry order and each entry's superseded-list
    order, so the per-line finding order is unchanged.

    ``prefilter`` is the lower-cased standard id when the id is pure ASCII, else ``None``.
    Every pattern begins with the escaped standard id under ``re.IGNORECASE``. The prefilter
    substring test is applied ONLY when the LINE is ASCII (see ``check_file``): on an ASCII
    line ``str.lower`` and ``re.IGNORECASE`` agree exactly, so an ASCII id absent from the
    lower-cased line cannot match the pattern, making the skip a pure fast-path. A non-ASCII
    line, or a non-ASCII id (prefilter ``None``), bypasses the prefilter and runs the full
    pattern; both preserve exact equivalence with running every pattern on every line.
    """
    compiled: list[tuple[str | None, re.Pattern[str], str]] = []
    for entry in entries:
        std_id = entry["id"]
        current = entry["current"]
        superseded_list = entry["superseded"]  # type: ignore[assignment]
        if not isinstance(superseded_list, list):
            continue

        std_id_re = re.escape(str(std_id))
        for superseded in superseded_list:
            # A register marker written "v1.1" is matched without its "v", so the
            # optional "v?" below admits BOTH forms: an added "v" against a bare
            # marker ("PCI DSS v4.0" for "4.0") and a dropped "v" against a
            # v-prefixed marker ("SLSA 1.1" for "v1.1"). Only a "v" directly before
            # a digit is treated as a prefix, so a marker such as "Version 2" is
            # left intact.
            # A marker may carry the standard's own id prefix (COBIT lists "COBIT 5");
            # strip it, as the discovery path does, so the pattern is "COBIT 5" and not
            # "COBIT COBIT 5" (3b38).
            superseded_core = re.sub(
                r"^" + re.escape(str(std_id)) + r"\s+", "", superseded, flags=re.IGNORECASE
            )
            bare = (
                superseded_core[1:]
                if re.match(r"[vV]\d", superseded_core)
                else superseded_core
            )
            sup_re = re.escape(bare)
            # The ID is bounded by (?<!\w) and (?!\w) rather than \b: for an ID that
            # starts and ends with a word character they are equivalent, but \b makes
            # the pattern for an ID ending in punctuation (for example a closing
            # parenthesis) impossible to match (3b35). The marker end uses (?!\w) for the
            # same reason: a marker ending in ")", such as "2025 (v2.0)", could never match.
            # The negative lookahead (?![.\-][\d\w]) prevents matching inside a longer
            # version string (e.g. "PCI DSS 4.0" must NOT match within "PCI DSS 4.0.1").
            pattern = re.compile(
                rf"(?<!\w){std_id_re}(?!\w)\s*(?::|\(|\s+)\s*v?{sup_re}(?!\w)(?![.\-][\d\w])",
                flags=re.IGNORECASE,
            )
            id_text = str(std_id)
            prefilter = id_text.lower() if id_text.isascii() else None
            compiled.append(
                (
                    prefilter,
                    pattern,
                    f"stale citation '{std_id} {superseded_core}' "
                    f"(current: {current})",
                )
            )
    return compiled


def check_file(
    path: Path, compiled: list[tuple[str | None, re.Pattern[str], str]]
) -> list[tuple[int, str]]:
    """Return list of (line-number, message) findings for the file."""
    text = read_text_safe(path)
    if text is None:
        return []
    return check_text(text, compiled)


def check_text(
    text: str, compiled: list[tuple[str | None, re.Pattern[str], str]],
    eligible_from: str | None = None,
) -> list[tuple[int, str]]:
    """check_file over text already read (3b75: sanctioned spans masked). With
    ``eligible_from``, which lines are code is decided from THAT text (the original), so masking
    can never create or remove a fence and change what else is checked (3b75 QA r4)."""
    findings: list[tuple[int, str]] = []
    pairs = iter_non_code_lines(text)
    if eligible_from is not None:
        keep = {ln for ln, _ in iter_non_code_lines(eligible_from)}
        masked_lines = text.splitlines()  # the SAME line model as iter_non_code_lines (r5)
        pairs = [(ln, masked_lines[ln - 1]) for ln in sorted(keep) if ln - 1 < len(masked_lines)]
    for ln, line in pairs:
        line_lower = line.lower()
        line_is_ascii = line.isascii()
        for prefilter, pattern, message in compiled:
            if prefilter is not None and line_is_ascii and prefilter not in line_lower:
                continue
            if pattern.search(line):
                findings.append((ln, message))

    return findings


def legacy_match_spans(
    text: str, compiled: list[tuple[str | None, re.Pattern[str], str]],
    eligible_from: str | None = None,
) -> list[tuple[int, int, int, str]]:
    """Where check_text's patterns match: (line, first column, last column, message), columns
    1-based and inclusive, over exactly the lines check_text reads (3b88)."""
    pairs = iter_non_code_lines(text)
    if eligible_from is not None:
        keep = {ln for ln, _ in iter_non_code_lines(eligible_from)}
        masked_lines = text.splitlines()
        pairs = [(ln, masked_lines[ln - 1]) for ln in sorted(keep) if ln - 1 < len(masked_lines)]
    spans = []
    for ln, line in pairs:
        line_lower = line.lower()
        line_is_ascii = line.isascii()
        for prefilter, pattern, message in compiled:
            if prefilter is not None and line_is_ascii and prefilter not in line_lower:
                continue
            for m in pattern.finditer(line):
                spans.append((ln, m.start() + 1, max(m.end(), m.start() + 1), message))
    return spans


def run(
    files: list[Path],
    compiled: list[tuple[str | None, re.Pattern[str], str]],
    num_entries: int,
    *,
    repo_root: Path,
) -> int:
    total_findings = 0
    by_file: dict[str, list[tuple[int, str]]] = {}
    for f in files:
        rel = f.relative_to(repo_root).as_posix()
        findings = check_file(f, compiled)
        if findings:
            by_file[rel] = findings
            total_findings += len(findings)

    if total_findings == 0:
        print(
            f"OK: no standards-currency findings (checked {num_entries} standards "
            f"across {len(files)} files)."
        )
        return 0

    for rel, findings in sorted(by_file.items()):
        print(f"=== {rel} ===")
        for ln, msg in findings:
            print(f"  L{ln}: {msg}")

    print()
    print(
        f"FAIL: {total_findings} standards-currency finding(s) "
        f"across {len(by_file)} file(s)."
    )
    return 1


from bisect import bisect_right
from collections import Counter
from html import unescape
from html.parser import HTMLParser
import json


IDENTIFIERS = [
    (
        "ISO/IEC",
        r"(?:ISO(?:\s*/\s*(?:IEC|IEEE|SAE)){0,2}"
        r"|IEC(?:\s*/\s*IEEE)?|ISA\s*/\s*IEC)"
        r"(?:\s+(?:TR|TS|PAS))?\s+\d{4,6}(?:-\d{1,3})*",
    ),
    (
        "NIST",
        r"(?:NIST\s+(?:"
        r"SP\s+\d{3,4}(?:-\d+[A-Z]?(?:-\d+)?|\s+series)?"
        r"|IR\s+\d+[A-Z]?"
        r"|AI\s+\d+-\d+"
        r"|AI\s+RMF|CSF|RMF|Privacy\s+Framework)"
        r"|NISTIR\s+\d+[A-Z]?"
        r"|(?:NIST\s+)?FIPS(?:\s+PUB)?\s+\d+(?:-\d+)?)",
    ),
    (
        "IEEE",
        r"IEEE(?:\s+Std)?\s+\d{3,5}(?:\.\d+)*(?:[a-z])?",
    ),
    (
        "ETSI/CEN",
        r"(?:(?:ETSI|CEN)\s+(?:EN|TS|TR|GS)\s+\d{3,6}|EN\s+\d{2,6})"
        r"(?:\s+\d{3}){0,1}(?:-\d{1,3})*",
    ),
    ("named", r"CIS\s+Controls|ITIL|WCAG|COBIT|SLSA"),
]

ID_RE = re.compile(
    r"(?<![\w/.-])(?:" + "|".join(
        "(?P<F%d>%s)%s" % (
            i,
            p,
            r"(?![A-Za-z0-9]|\.\d|-\d)" if i not in {1, 2}
            else (
                r"(?:(?![A-Za-z0-9]|\.\d|-\d)|(?=[re]\d))"
                if i == 1 else r"(?![A-Za-z0-9]|\.\d)"
            ),
        )
        for i, (_, p) in enumerate(IDENTIFIERS)
    ) + r")",
    re.I,
)

BROAD_RE = re.compile(
    r"\b(?:ISO(?:\s*/\s*IEC)?|IEC|NIST(?:IR)?|FIPS|IEEE|ETSI|CEN"
    r"|CIS|ITIL|WCAG|COBIT|SLSA)\b"
    r"|(?<!\w)[A-Z][A-Za-z0-9]+(?:[ \t]+[A-Za-z]+){0,3}[ \t]+"
    r"(?:Framework|Controls|Standard)[ \t]+v?\d+(?:\.\d+)*"
)

REV = r"(?:Rev(?:ision)?\.?\s*|r)(\d+(?:\.\d+)*)"
NUM = r"\d+(?:\.\d+)*(?:-\d+)*"
END = r"(?![\w]|\.\d|-\d)"
BLOCK_TAGS = set(
    "address article aside blockquote br caption dd details div dl dt "
    "fieldset figcaption figure footer form h1 h2 h3 h4 h5 h6 header hr li "
    "main menu nav ol p pre section summary table tbody td th thead tr ul".split()
)
# Pure text-level formatting tags render with NO whitespace boundary, so an
# end tag from this set must not inject a space that would split a citation
# number or edition (ISO/IEC <b>2700</b>1 renders 27001). Any OTHER inline
# tag (span, a, ...) may carry a display:block style that IS a real visual
# boundary (the landing-page biblio .id spans), so it keeps a soft space.
FORMATTING_TAGS = set(
    "b i em strong code sub sup small mark u s tt kbd samp var cite q "
    "abbr dfn time data bdi bdo ins del big wbr".split()
)


def identity_key(value):
    value = unescape(value).replace("\xa0", " ")
    value = value.translate(
        str.maketrans({"\u2013": "-", "\u2011": "-", "\u2212": "-"})
    )
    value = re.sub(r"\s*/\s*", "/", value)
    return re.sub(r"\s+", " ", value).strip().casefold()


def edition_key(value):
    value = value.strip().strip("()").strip()
    m = re.fullmatch(REV, value, re.I)
    if m:
        return "rev:" + m[1]
    value = re.sub(
        r"^(?:version\s+|v)", "", value, flags=re.I
    )
    if re.fullmatch(r"e\d{4}", value, re.I):
        return "edition:" + value.lower()
    if re.fullmatch(NUM, value):
        return "version:" + value
    return None


class TextExtractor(HTMLParser):
    """Logical text blocks with source offsets for their characters."""

    def __init__(self, source, base=0, markdown=False):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.base = base
        self.markdown = markdown
        self.starts = [0] + [
            m.end() for m in re.finditer("\n", source)
        ]
        self.blocks = []
        self.chars = []
        self.offsets = []
        self.hidden = []

    def source_offset(self):
        line, col = self.getpos()
        return self.base + self.starts[line - 1] + col

    def flush(self):
        if self.chars:
            self.blocks.append(
                ("".join(self.chars), self.offsets)
            )
        self.chars, self.offsets = [], []

    def add(self, value, pos, literal=True):
        for i, c in enumerate(value):
            if self.markdown and c in "*_~\x60":
                continue
            self.chars.append(
                " " if c.isspace() else c.translate(
                    str.maketrans({"\u2013": "-", "\u2011": "-", "\u2212": "-"})
                )
            )
            self.offsets.append(pos + (i if literal else 0))

    def add_encoded(self, value, pos):
        end = 0
        for match in re.finditer(
            r"&(?:#\d+|#x[0-9a-f]+|[a-z][a-z0-9]+);",
            value,
            re.I,
        ):
            self.add(value[end:match.start()], pos + end)
            self.add(
                unescape(match[0]), pos + match.start(), False
            )
            end = match.end()
        self.add(value[end:], pos + end)

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.flush()
            self.hidden.append(tag)
            return
        if self.hidden:
            return
        if tag in BLOCK_TAGS:
            self.flush()

        # Human-facing attributes are independent blocks. Tokenize the raw
        # tag into COMPLETE name=value pairs left-to-right, so a name=
        # embedded in another attribute's quoted value is consumed as that
        # value and never matched as its own attribute; append each
        # human-facing one as its own block WITHOUT flushing the visible
        # stream (an inline tag must not split surrounding visible text).
        raw = self.get_starttag_text()
        for m in re.finditer(
            r"""([^\s=/<>"']+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""",
            raw,
        ):
            if m[1].lower() not in {"alt", "title", "aria-label"}:
                continue
            g = next(gi for gi in (2, 3, 4) if m[gi] is not None)
            saved_chars, saved_offsets = self.chars, self.offsets
            self.chars, self.offsets = [], []
            self.add_encoded(m[g], self.source_offset() + m.start(g))
            self.flush()
            self.chars, self.offsets = saved_chars, saved_offsets

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if self.hidden:
            if tag == self.hidden[-1]:
                self.hidden.pop()
            return
        if tag in BLOCK_TAGS:
            self.flush()
        elif (
            tag not in FORMATTING_TAGS
            and self.chars
            and not self.chars[-1].isspace()
        ):
            # A non-formatting inline tag (span/a/...) may be a display:block
            # visual boundary; keep a soft space so adjacent biblio spans do
            # not concatenate a citation and its neighbour (landing.html).
            self.add(" ", self.source_offset(), False)

    def handle_data(self, data):
        if not self.hidden:
            self.add(data, self.source_offset())

    def handle_entityref(self, name):
        if not self.hidden:
            self.add(
                unescape("&" + name + ";"),
                self.source_offset(),
                False,
            )

    def handle_charref(self, name):
        if not self.hidden:
            self.add(
                unescape("&#" + name + ";"),
                self.source_offset(),
                False,
            )


def text_blocks(source, suffix):
    if suffix == ".html":
        parser = TextExtractor(source)
        parser.feed(source)
        parser.close()
        parser.flush()
        return parser.blocks

    # Mask destinations, retaining source positions.
    masked = list(source)

    def erase(a, b):
        for j in range(a, b):
            if masked[j] != "\n":
                masked[j] = " "

    for m in re.finditer(
        r"(?m)^[ \t]{0,3}\[[^\]\n]+\]:[^\n]*"
        r"|https?://[^\s<>]+"
        r"|<[^<>\n]*@[^<>\n]*>",
        source,
    ):
        erase(m.start(), m.end())

    # Balanced inline-link destinations, including nested parentheses.
    # One left-to-right pass pairs each "(" with its matching ")"; the
    # per-"](" lookup is then O(1), avoiding the quadratic rescan a
    # malformed run of "](" would otherwise cause.
    close_of, open_stack, k, n = {}, [], 0, len(source)
    while k < n:
        ch = source[k]
        if ch == "\\":
            k += 2
            continue
        if ch == "(":
            open_stack.append(k)
        elif ch == ")" and open_stack:
            close_of[open_stack.pop()] = k
        k += 1
    # A high-water mark erases each character at most once, so overlapping
    # or nested destinations (a balanced "](" * n + ")" * n run) stay O(n)
    # rather than re-erasing an already-blanked span per destination.
    erased_to = 0
    for m in re.finditer(r"\]\(", source):
        # A backslash-escaped "]" does not close an inline-link label (odd
        # run of preceding backslashes), so the following "(...)" is visible
        # text, not a destination to erase.
        bs, i = 0, m.start() - 1
        while i >= 0 and source[i] == "\\":
            bs, i = bs + 1, i - 1
        if bs % 2 == 1:
            continue
        close = close_of.get(m.end() - 1)
        if close is not None:
            a = max(m.start(), erased_to)
            if a < close + 1:
                erase(a, close + 1)
                erased_to = close + 1

    for m in re.finditer(r"\]\[[^\]\n]*\]", source):
        # An escaped "]" (odd backslash run) does not close a link label,
        # so the following "[...]" is visible text, not a reference to mask.
        bs, i = 0, m.start() - 1
        while i >= 0 and source[i] == "\\":
            bs, i = bs + 1, i - 1
        if bs % 2 == 1:
            continue
        erase(m.start(), m.end())

    # Inline paths are authoring references, not citation labels. A path is a
    # single token (no whitespace) with a directory separator or a
    # source-file extension; a code span containing whitespace is prose
    # ("(7 years, ISO/IEC 42001)"), so a citation inside it is preserved.
    for m in re.finditer(r"\x60[^\x60\n]*\x60", source):
        content = m[0][1:-1]
        if content and not re.search(r"\s", content) and (
            "/" in content
            or re.search(r"\.(?:md|html|py)\b", content)
        ):
            erase(m.start(), m.end())

    allowed = {ln for ln, _ in iter_non_code_lines(source)}
    blocks, offset, start, pending = [], 0, 0, []

    def flush():
        nonlocal pending
        if pending:
            value = "".join(pending)
            parser = TextExtractor(value, start, markdown=True)
            parser.feed(value)
            parser.close()
            parser.flush()
            blocks.extend(parser.blocks)
            pending = []

    for ln, line in enumerate(
        "".join(masked).splitlines(keepends=True), 1
    ):
        raw = source[offset:offset + len(line)]
        if ln not in allowed or not line.strip():
            flush()
        elif "|" in raw:
            flush()
            cell_start = offset
            for cell in line.split("|"):
                parser = TextExtractor(
                    cell, cell_start, markdown=True
                )
                parser.feed(cell)
                parser.close()
                parser.flush()
                blocks.extend(parser.blocks)
                cell_start += len(cell) + 1
        else:
            if re.match(
                r"^\s*(?:#{1,6}\s|[-+*]\s|\d+\.\s|>)", raw
            ):
                flush()
            if not pending:
                start = offset
            pending.append(line)
        offset += len(line)
    flush()
    return blocks


def version_after(text, end, family):
    tail = text[end:]
    if family == "NIST":
        embedded = re.match(r"(e\d{4})" + END, tail, re.I)
        if embedded:
            return embedded[1], end + embedded.end()
        m = re.match(
            r"\s*(?:[:(,]\s*)?(" + REV + ")" + END,
            tail,
            re.I,
        )
        if m:
            return m[1], end + m.end()

    # A parenthesized edition "(2022)" is accepted like the colon and
    # whitespace forms, WITHOUT requiring an immediate close: a real edition
    # is often followed by a qualifier inside the parens ("(1.0 core + 1.1
    # IPD draft)" for the NIST Privacy Framework), and requiring the close
    # discarded that real edition. A rare parenthetical prose quantity
    # ("(2022 respondents)") is the accepted residual (no corpus occurrence).
    if family == "ISO/IEC":
        pat = r"\s*(?::\s*|\(\s*|\s)(\d{4})" + END
    elif family == "IEEE":
        pat = r"\s*(?:[-:]\s*|\(\s*|\s)(\d{4})" + END
    else:
        pat = (
            r"\s*(?:[:(]\s*|\s+|(?=v))"
            r"((?:version\s+|v)?" + NUM + ")" + END
        )
    m = re.match(pat, tail, re.I)
    return (m[1], end + m.end()) if m else ("", end)


def discover(source, suffix):
    starts = [0] + [
        m.end() for m in re.finditer("\n", source)
    ]

    def location(offset):
        n = bisect_right(starts, offset)
        return [n, offset - starts[n - 1] + 1]

    occurrences = []
    for text, offsets in text_blocks(source, suffix):
        covered = []

        def emit(a, b, family, observed, version, channel):
            covered.append((a, b))
            occurrences.append(dict(
                family=family,
                observed=observed,
                identity=identity_key(observed),
                version=version,
                channel=channel,
                context=text,
                span=[
                    location(offsets[a]),
                    location(offsets[b - 1]),
                ],
            ))

        for m in ID_RE.finditer(text):
            family = IDENTIFIERS[int(m.lastgroup[1:])][0]
            version, end = version_after(
                text, m.end(), family
            )
            emit(
                m.start(), end, family, m[0], version, "grammar"
            )

            # Directly coordinated ISO identifiers with colon-year pins.
            # No arbitrary numeric prose inherits a publisher.
            if family == "ISO/IEC":
                prefix = re.match(r".*?(?=\d)", m[0])[0]
                while True:
                    carry = re.match(
                        r"\s*(?:,\s*(?:and\s+)?|and\s+|&\s*)"
                        r"(\d{4,6}(?:-\d{1,3})*):(\d{4})" + END,
                        text[end:],
                    )
                    if not carry:
                        break
                    a = end + carry.start(1)
                    end += carry.end()
                    emit(
                        a, end, family, prefix + carry[1],
                        carry[2], "grammar",
                    )

        grammar_spans = list(covered)
        for m in BROAD_RE.finditer(text):
            if any(
                a <= m.start() < b for a, b in grammar_spans
            ):
                continue
            end = len(text)
            stop = re.search(r"[;|]", text[m.end():end])
            if stop:
                end = m.end() + stop.start()
            observed = text[m.start():end].strip()
            token = m[0].upper()
            family = (
                "ISO/IEC" if token.startswith(("ISO", "IEC"))
                else "NIST" if token.startswith(("NIST", "FIPS"))
                else "IEEE" if token.startswith("IEEE")
                else "ETSI/CEN" if token.startswith(("ETSI", "CEN"))
                else "named" if token.startswith(
                    ("CIS", "ITIL", "WCAG", "COBIT", "SLSA")
                )
                else "other"
            )
            emit(
                m.start(), max(m.end(), end),
                family, observed, "", "candidate",
            )
    return occurrences


def diagnostic_key(value):
    key = identity_key(value)
    # Suggestions only: preserve kind, number, part and publication series.
    m = re.fullmatch(
        r"(?:iso/iec|iso|iec)\s+"
        r"((?:(?:tr|ts|pas)\s+)?\d+(?:-\d+)*)",
        key,
    )
    if m:
        return ("iso-suggestion", m[1])
    key = re.sub(r"^nistir\s+", "nist ir ", key)
    key = re.sub(r"^ieee std\s+", "ieee ", key)
    key = re.sub(
        r"^(?:nist )?fips pub\s+", "fips ", key
    )
    return ("spelling-suggestion", key)


def resolve(occurrence, entries, bare_exceptions=None):
    if occurrence["channel"] == "candidate":
        return [
            ("CANDIDATE", "Classify unsupported publisher/framework form.")
        ]

    key = occurrence["identity"]
    exact = [
        e for e in entries
        if identity_key(str(e["id"])) == key
    ]
    if not exact:
        nearby = [
            e for e in entries
            if diagnostic_key(str(e["id"]))
            == diagnostic_key(occurrence["observed"])
        ]
        if len(nearby) > 1:
            return [(
                "AMBIGUOUS",
                "Possible rows: "
                + ", ".join(str(e["id"]) for e in nearby),
            )]
        if nearby:
            return [(
                "NONCANONICAL_ID",
                "Suggest " + str(nearby[0]["id"]) + "; not accepted.",
            )]
        # A bare NIST SP number without a hyphenated part is NOT reliably a
        # series prefix (SP 330, SP 811 are concrete publications), so an
        # unmatched one stays UNREGISTERED. Registered series identities are
        # recognized by the grammar's explicit "... series" suffix (F3a).
        return [("UNREGISTERED", "No canonical register row.")]

    if len(exact) != 1:
        return [("AMBIGUOUS", "Multiple canonical rows.")]

    entry = exact[0]
    version = occurrence["version"]
    if not version:
        reason = (bare_exceptions or {}).get(key)
        if reason:
            return []
        # A register row whose current value BEGINS with a series marker
        # declares no single edition to pin to (editions vary per part): a
        # bare citation of such a series is not UNPINNED. Anchored to the
        # start so a concrete edition with an incidental "series" note in
        # its current cell is not wrongly exempted.
        if str(entry["current"]).strip().lower().startswith(
            ("series", "subseries")
        ):
            return []
        return [(
            "UNPINNED",
            "Required edition missing; register: "
            + str(entry["current"]),
        )]

    observed = edition_key(version)
    # A superseded marker may carry the standard's own id prefix (the
    # register lists COBIT's superseded editions as "COBIT 5, COBIT 4.1");
    # strip a leading id prefix so the bare edition key matches the observed
    # version and the citation resolves STALE rather than UNRESOLVED_EDITION.
    _id_prefix = re.compile(
        r"^" + re.escape(str(entry["id"])) + r"\s+", re.I
    )
    superseded = {
        edition_key(_id_prefix.sub("", str(v)))
        for v in entry["superseded"]
    } - {None}
    if observed in superseded:
        return [(
            "STALE",
            "Registered superseded edition; current: "
            + str(entry["current"]),
        )]
    current = edition_key(str(entry["current"]))
    if current is not None and current == observed:
        return []
    return [(
        "UNRESOLVED_EDITION",
        "Observed edition is not a comparable current/superseded "
        "register marker: " + str(entry["current"]),
    )]


KINDS = (
    "STALE", "UNREGISTERED", "NONCANONICAL_ID", "UNPINNED",
    "AMBIGUOUS", "UNRESOLVED_EDITION", "CANDIDATE",
    "HISTORICAL", "INVALID_EXCEPTION",
)

# 3b75: sanctioned historical-context citations. The wrapper validates each
# declaration (policy, reason, evidence, historical wording); the engine binds
# it to exactly one whole sentence of one Markdown file and masks ONLY the
# declared superseded occurrences inside that sentence, so every other
# citation on the line, stale or not, is checked exactly as before.


_ABBREV = re.compile(r"\b(?:e\.g|i\.e|cf|etc|vs|viz|al|approx|no|fig)\.[\"')\]*_]*\s*$", re.I)
_INTERNAL_BREAK = re.compile(r"[.!?;:][\"')]*\s")
# A sanctioned sentence is plain ASCII text: letters, digits, spaces and a few punctuation marks.
# Anything that can change what renders (markup, a backslash escape, a character reference, a
# tilde or backtick run, emphasis) is refused rather than modelled (3b75 QA r6, codex, claude),
# and so is a non-ASCII letter, which can be a lookalike a reader and a word screen miss (r7, claude).
SENTENCE_TEXT = re.compile(r"[A-Za-z0-9 .,;:'\"()/%-]+[.!?]")
_FENCE_LINE = re.compile(r"\s*(?:```|~~~)")


def _simple_fences(lines):
    """True when every fence-shaped line (what the toggle line model reads as a fence) is one a
    Markdown renderer reads the same way: at column 1, a run of exactly three, an opener whose
    backtick info string carries no backtick, and a closer of the opener's character with nothing
    after it, with no block left open (3b75 QA r6, claude: a 4-backtick fence around a 3-backtick
    line is one code block to a renderer and two toggles to the line model)."""
    open_char = None
    for line in lines:
        text = line.rstrip("\r\n")
        if not _FENCE_LINE.match(text):
            continue
        run = re.match(r"(`+|~+)", text)
        if run is None or len(run.group(1)) != 3:
            return False
        rest = text[3:]
        if open_char is None:
            if run.group(1)[0] == "`" and "`" in rest:
                return False
            open_char = run.group(1)[0]
        elif run.group(1)[0] == open_char and not rest.strip(" \t"):
            open_char = None
        else:
            return False
    return open_char is None


def _whole_unit(lines, idx, start, end, sentence):
    """True when lines[idx][start:end] is a STANDALONE PARAGRAPH (3b75 QA r3: every structural
    branch allowed so far, table cells and list items, was talked around, so exactly one shape is
    accepted). The line holds nothing but the sentence, starting at column 1; the sentence does not
    begin with a list, heading, blockquote, table or indentation marker; the raw lines above and
    below are blank (or the file boundary); and the sentence ends with `.`, `!` or `?` (not an
    abbreviation's period) with no other sentence or clause break."""
    body = sentence.rstrip()
    if not SENTENCE_TEXT.fullmatch(body):
        return False  # plain text only, ending in a terminator (3b75 QA r4, r6)
    if _INTERNAL_BREAK.search(body[:-1]) or _ABBREV.search(body):
        return False
    line = lines[idx].rstrip("\n")
    if start != 0 or line[end:].strip():
        return False
    if re.match(r"(?:\s|[-+*]\s|\d+[.)]\s|#{1,6}\s|>|\|)", sentence):
        return False

    def blank(k):
        # Markdown blank lines are ASCII spaces and tabs only; a no-break space is text (r4).
        return k < 0 or k >= len(lines) or not lines[k].strip(" \t\r\n")

    return blank(idx - 1) and blank(idx + 1)


def apply_historical_exceptions(
    source, rel, exceptions, entries, bare_exceptions=None, raw=None
):
    """Return (masked_source, sanctioned, errors) for one Markdown file.

    A declaration binds when its sentence occurs exactly once on a non-code
    line, is sentence-bounded there, and contains at least one grammar
    occurrence of the declared identity and edition that resolves STALE.
    Anything else is an INVALID_EXCEPTION, which always blocks."""
    lines = source.splitlines(keepends=True)
    # A document whose line model is ambiguous, or that carries raw HTML, cannot carry a
    # sanction: Python and a Markdown renderer disagree on where lines end (U+2028, form feed,
    # NEL, a lone CR and kin), and raw HTML can wrap the paragraph in a container whatever the
    # Markdown says. Deny by default (3b75 QA r5).
    # ``raw`` is the file's untranslated text: a universal-newline read has already turned a lone
    # CR into LF (3b75 QA r6, codex). HTML comments get no carve-out: comment markers inside a
    # code span, an escaped or a `<!-->` marker all blank real HTML to a regex (r6, all three).
    ambiguous = re.search(
        r"[\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029]|\r(?!\n)", source if raw is None else raw
    )
    html = re.search(r"<[A-Za-z/!?]", source)
    fences = _simple_fences(lines)
    allowed = {ln for ln, _ in iter_non_code_lines(source)}
    masked = [list(line) for line in lines]
    sanctioned, errors, occs = [], [], None
    for ex in exceptions:
        if ex["path"] != rel:
            continue
        sites = [
            (i, m.start())
            for i, line in enumerate(lines) if i + 1 in allowed
            for m in re.finditer(re.escape(ex["sentence"]), line)
        ]
        problem, hits, span = None, [], [[1, 1], [1, 1]]
        if ambiguous:
            problem = "the document uses line separators other than LF or CRLF"
        elif html:
            problem = "the document carries raw HTML or an HTML comment"
        elif not fences:
            problem = "the document's fenced blocks are not all simple three-character fences"
        elif len(sites) != 1:
            problem = (
                "declared sentence not found" if not sites
                else "declared sentence occurs %d times" % len(sites)
            )
        else:
            idx, start = sites[0]
            end = start + len(ex["sentence"])
            span = [[idx + 1, start + 1], [idx + 1, end]]
            if not _whole_unit(lines, idx, start, end, ex["sentence"]):
                problem = (
                    "declared sentence is not a standalone paragraph at its site (the whole "
                    "line from column 1, blank lines above and below)"
                )
        if problem is None:
            if occs is None:
                occs = [
                    o for o in discover(source, ".md")
                    if o["channel"] == "grammar"
                ]
            for o in occs:
                (l1, c1), (l2, c2) = o["span"]
                if (
                    l1 == l2 == idx + 1 and start < c1 and c2 <= end
                    and o["identity"] == ex["identity"]
                    and edition_key(o["version"]) == ex["edition"]
                    and [k for k, _ in resolve(
                        o, entries, bare_exceptions
                    )] == ["STALE"]
                ):
                    hits.append(o)
            # Exactly one occurrence, written exactly as the row's citation (3b75 QA r2): a row
            # sanctions the citation it names, not every written form of the same edition.
            if ex.get("citation") is not None:  # a wrapper that names the written citation
                hits = [
                    o for o in hits
                    if lines[o["span"][0][0] - 1][o["span"][0][1] - 1:o["span"][1][1]]
                    == ex["citation"]
                ]
            if len(hits) != 1:
                problem = (
                    "no registered superseded citation of the declared "
                    "edition inside the declared sentence" if not hits
                    else "the declared citation occurs more than once in the sentence"
                )
        if problem:
            errors.append(dict(
                kind="INVALID_EXCEPTION", family="exception",
                identity=ex["id"], observed=ex["id"], version="",
                channel="exception", context=ex["sentence"], path=rel,
                suffix=".md", span=span, detail=ex["id"] + ": " + problem,
                legacy=False,
            ))
            continue
        for o in hits:
            (l1, c1), (_, c2) = o["span"]
            for j in range(c1 - 1, c2):
                masked[l1 - 1][j] = " "
            sanctioned.append(dict(
                o, path=rel, suffix=".md", kind="HISTORICAL",
                detail=ex["id"] + ": " + ex["reason"], legacy=False,
            ))
    return "".join("".join(line) for line in masked), sanctioned, errors

VERSION_CELL = re.compile(
    r"(?:v)?\d{1,4}(?:\.\d+)*|Rev\.?\s*\d+(?:\.\d+)*|\d{4}", re.I
)
TABLE_SEP = re.compile(r"\s*\|?[\s:|-]+\|?\s*")


def table_column_version(source, line_no):
    """A framework cited in a Markdown table whose header has an explicit
    Version/Edition column carries its edition in THAT column, not inline.
    Return that row's version-column value (a lone version token) so the
    citation is not a false UNPINNED. Only an explicit Version/Edition
    header associates a neighbouring cell, so an unrelated cell in an
    ordinary table never inherits a value (boundary between cells kept)."""
    lines = source.splitlines()
    idx = line_no - 1
    if not (0 <= idx < len(lines)) or "|" not in lines[idx]:
        return None
    top = idx
    while top > 0 and "|" in lines[top - 1]:
        top -= 1
    # A real table has a header row then a |---| separator directly under it.
    if top + 1 >= len(lines) or not TABLE_SEP.fullmatch(lines[top + 1]):
        return None
    header = [c.strip().lower() for c in lines[top].split("|")]
    col = next(
        (i for i, h in enumerate(header) if h in ("version", "edition")),
        None,
    )
    if col is None:
        return None
    cells = [c.strip() for c in lines[idx].split("|")]
    if col < len(cells) and VERSION_CELL.fullmatch(cells[col]):
        return cells[col]
    return None


def coverage_report(
    files, entries, *, repo_root, mode="report", bare_exceptions=None,
    historical_exceptions=None,
):
    compiled = compile_entry_patterns(entries)
    findings, occurrences, file_counts = [], [], Counter()

    for path in files:
        # UTF-8/read failures are environmental errors, never silent skips.
        source = path.read_text(encoding="utf-8")
        rel = path.relative_to(repo_root).as_posix()
        suffix = path.suffix
        file_counts[suffix] += 1

        masked, sanctioned_spans = source, set()
        if suffix == ".md" and historical_exceptions:
            masked, sanctioned, errors = apply_historical_exceptions(
                source, rel, historical_exceptions, entries, bare_exceptions,
                raw=(
                    path.read_bytes().decode("utf-8")
                    if any(ex["path"] == rel for ex in historical_exceptions) else None
                ),
            )
            # Discovery reads the ORIGINAL text and skips only the sanctioned spans (3b75 QA r1:
            # masking before discovery erased a neighbouring bare series member's context).
            sanctioned_spans = {
                tuple(map(tuple, f["span"])) for f in sanctioned
            }
            findings.extend(sanctioned + errors)
            occurrences.extend(
                {k: v for k, v in f.items()
                 if k not in ("kind", "detail", "legacy")}
                for f in sanctioned
            )

        # This exact HEAD check alone controls PR1 blocking behavior.
        legacy_spans = []
        if suffix == ".md":
            legacy_spans = legacy_match_spans(
                masked, compiled, eligible_from=source if sanctioned_spans else None
            )
            for line, message in check_text(
                masked, compiled, eligible_from=source if sanctioned_spans else None
            ):
                findings.append(dict(
                    kind="STALE",
                    family="legacy",
                    identity=message,
                    observed=message,
                    version="",
                    path=rel,
                    suffix=suffix,
                    span=[[line, 1], [line, 1]],
                    detail=message,
                    legacy=True,
                ))

        for occurrence in discover(source, suffix):
            if tuple(map(tuple, occurrence["span"])) in sanctioned_spans:
                continue
            occurrence.update(path=rel, suffix=suffix)
            # A framework cited in a Markdown table with an explicit
            # Version/Edition column carries its edition in that column,
            # not inline; associate it so the citation is not a false
            # UNPINNED (dev-security baseline table: "| COBIT | 2019 |").
            if (
                suffix != ".html"
                and occurrence["channel"] == "grammar"
                and not occurrence["version"]
            ):
                tv = table_column_version(
                    source, occurrence["span"][0][0]
                )
                if tv:
                    occurrence["version"] = tv
            occurrences.append(occurrence)
            for kind, detail in resolve(
                occurrence, entries, bare_exceptions
            ):
                # A normalized occurrence is legacy (BLOCKING) only where a legacy pattern for
                # its identifier matches at its own position, and it replaces exactly the legacy
                # findings it covers: a second citation on the line keeps its label, and another
                # edition or spelling the legacy check misses does not inherit one (3b88).
                (line_no, first), (_, last) = occurrence["span"]
                prefix = ("stale citation '" + occurrence["observed"] + " ").casefold()
                covering = {
                    message for ln, start, end, message in legacy_spans
                    if kind == "STALE" and ln == line_no and start <= last and end >= first
                    and message.casefold().startswith(prefix)
                }
                matched = [
                    f for f in findings
                    if f["legacy"] and f["family"] == "legacy" and f["path"] == rel
                    and f["span"][0][0] == line_no and f["detail"] in covering
                ]
                for f in matched:
                    findings.remove(f)
                findings.append(dict(
                    occurrence,
                    kind=kind,
                    detail=detail,
                    legacy=bool(covering),
                ))

    order = lambda x: (
        x["path"], x["span"][0], x.get("kind", ""), x["observed"]
    )
    findings.sort(key=order)
    occurrences.sort(key=order)

    legacy = sum(f["legacy"] for f in findings)
    blocking_kinds = {
        "STALE", "UNREGISTERED", "NONCANONICAL_ID", "UNPINNED",
    }
    new_blocking = sum(
        f["kind"] in blocking_kinds and not f["legacy"]
        for f in findings
    )
    invalid = sum(f["kind"] == "INVALID_EXCEPTION" for f in findings)
    status = int(bool(
        legacy or invalid or (mode == "enforce" and new_blocking)
    ))

    inventories = {}
    for kind in KINDS:
        subset = [f for f in findings if f["kind"] == kind]
        inventories[kind] = dict(
            identities=len({f["identity"] for f in subset}),
            occurrences=len(subset),
            legacy=sum(f["legacy"] for f in subset),
        )

    census = []
    for suffix in sorted(file_counts):
        for family in sorted({
            o["family"] for o in occurrences
            if o["suffix"] == suffix
        }):
            group = [
                o for o in occurrences
                if o["suffix"] == suffix and o["family"] == family
            ]
            issues = [
                f for f in findings
                if f["suffix"] == suffix and f["family"] == family
            ]
            census.append(dict(
                suffix=suffix,
                family=family,
                recognized=sum(
                    o["channel"] == "grammar" for o in group
                ),
                candidates=sum(
                    o["channel"] == "candidate" for o in group
                ),
                identities=len({
                    o["identity"] for o in group
                    if o["channel"] == "grammar"
                }),
                findings=dict(sorted(
                    Counter(f["kind"] for f in issues).items()
                )),
            ))

    return dict(
        mode=mode,
        exit=status,
        entries=len(entries),
        census=census,
        files=dict(sorted(file_counts.items())),
        inventories=inventories,
        occurrences=occurrences,
        findings=findings,
    )


def print_coverage(report, *, as_json=False):
    if as_json:
        print(json.dumps(
            report, ensure_ascii=False, indent=2, sort_keys=True
        ))
        return

    print("Coverage mode:", report["mode"])
    print("Files:", report["files"], "Register rows:", report["entries"])
    print("Scope:", report.get("scope", {}))
    for kind, count in report["inventories"].items():
        noun = "distinct forms" if kind == "CANDIDATE" else "identities"
        print(
            "%s: %d %s; %d occurrences (%d legacy)" % (
                kind, count["identities"], noun,
                count["occurrences"], count["legacy"],
            )
        )
        subset = [
            f for f in report["findings"] if f["kind"] == kind
        ]
        if not subset:
            print("  (none)")
        for f in subset:
            label = "BLOCKING" if (
                f["legacy"] or kind == "INVALID_EXCEPTION"
            ) or (
                report["mode"] == "enforce"
                and kind in {
                    "STALE", "UNREGISTERED",
                    "NONCANONICAL_ID", "UNPINNED",
                }
            ) else "SANCTIONED" if kind == "HISTORICAL" else "ADVISORY"
            print(
                "  %s:%s:%s %s %s %r edition=%r: %s" % (
                    f["path"], *f["span"][0], label, f["family"],
                    f["observed"], f["version"], f["detail"],
                )
            )

    if report["exit"]:
        print("FAIL: blocking findings remain.")
    elif report["findings"]:
        print("REPORT: no blocking findings; advisory review remains.")
    else:
        print("OK: no findings within the declared scope and grammars.")
