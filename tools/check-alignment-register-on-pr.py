#!/usr/bin/env python3
"""D15: alignment-citation register check (PR-time, diff-scoped, ADVISORY).

THE CLASS. The canonical-citations register
(``governance/register-canonical-citations.md``) is the positive list of the
standards and regulations whose currency the library tracks; its Maintenance
section asks that a standard is added "before the citing PR merges". Nothing
enforced that: a PR could add a framework-alignment row, or name an EU
instrument in prose, for an instrument with no register row, and the register
(and so the standards-currency gate that reads it) would never learn of it.
The 2026-10-04 PR #2697 is the observed case: it added Directive (EU)
2022/2557 and Recommendation 2003/361/EC in prose, neither of which has a row.

WHAT IT CHECKS. Only lines the PR adds or changes (``git diff`` of the PR head
against its merge base), in Markdown files under the audited domain
directories (``lint_common.AUDITED_DOMAIN_DIRS``; gate 52 forbids a hardcoded
list), minus gate 6's exempt files:

1. **List-form alignment tables**: a table whose first header cell means "each
   row names one framework or standard" (``Framework``, ``Framework /
   Standard``, ``Regulation`` and the other headers in ``LIST_HEADERS``). The
   first cell of each added row is a citation.
2. **Matrix-header alignment tables**: a table under a framework-alignment or
   crosswalk heading whose header row names one framework per column. When the
   PR adds the header row, each header cell after the first is a citation.
3. **Free-text citation-list columns** (``Regulatory``, ``Legal / Regulatory``,
   ``Other`` and the rest of ``FREE_TEXT_HEADERS``) of either table form: each
   ``;`` or ``,`` separated segment of an added cell is a citation once its
   provision suffix (``Art. 32``, ``§3.1``) is removed.
4. **EU/EC instrument numbers** anywhere on an added non-code line
   (``Directive (EU) 2022/2557``, ``Recommendation 2003/361/EC``,
   ``Regulation (EU) No 910/2014``), compared by number against the numbers in
   the register's Standard ID, Current version and Superseded versions cells.

HOW A CITATION RESOLVES. Gate 6 (``tools/lint-standards-currency.py`` and its
pack engine) owns the register parser and the identity normalization; this
check imports both rather than re-implementing them, so the two tools read the
same rows and the same identities. A citation inside gate 6's grammar (ISO/IEC,
NIST, IEEE, ETSI/CEN and the named frameworks) is reported only when gate 6's
own ``resolve`` returns ``UNREGISTERED``; a NONCANONICAL or AMBIGUOUS spelling
has a nearby row and is gate 6's to report, not this check's. Any other
citation is registered when its normalized identity, after a trailing edition
or version is removed, matches a register Standard ID exactly, through a curated
alias or umbrella pattern (``tools/alignment-register-aliases.json``), as a
whole-word suffix of a Standard ID (``GDPR`` for ``EU GDPR``, ``Law 25`` for
``Quebec Law 25``), through an acronym the citation carries in parentheses, or
as a series prefix of a Standard ID (``IEC 62443`` for the ``IEC 62443-*`` part
rows). The series and suffix acceptance is this check's addition to gate 6: it
can only make D15 report less than gate 6 would for the same text, never more.

WHAT IS NOT A FINDING. The exclusion policy
(``tools/alignment-register-exclusions.json``) encodes the maintainer decision
of 2026-10-16 ("Tracked only"): the register covers standards and regulations
whose currency is tracked, so RFCs, vendor guidance and books are not expected
in it. Each policy pattern or entry carries its class and its reason, and the
policy file is validated on load. Generic placeholders (``N/A``, ``Internal``,
``sectoral laws``), bare publisher names (``NIST``, ``OWASP``) and segments
with no citation shape (no acronym or digit, and no instrument word in a
multiword name) are not citations (the ``not_citable`` block of the alias file).

POSTURE. ADVISORY, the D8 precedent: it prints a ``D15 WARN`` line per
unregistered citation and, once its modules load, ALWAYS exits 0. It is wired into the PR-time runner
and the ``pull_request`` job of ``quality.yml`` only, never into
``tools/run_all_audits.sh``: the corpus-gate bar requires near-zero false
positives, and that runner hides a passing gate's warnings. An absent register
(an adopter may drop it) is a NOTE and a no-op, and so is a missing merge base
or an unreadable policy file (fail-open, the guard-malfunction stance).

RESIDUE (what D15 does NOT establish). It is delta-only, so a citation that is
already on main is out of scope (gate 6's report mode inventories those for its
grammar families). It cannot see a citation outside the four surfaces above
(an instrument named in prose without a number, a citation in a table it does
not recognize), a citation the alias or suffix rules accept loosely (``AI Act``
resolves to any registered AI Act), or an EU number that appears only in
another row's Current version cell (the EN 54 row's Construction Products
Regulation (EU) 305/2011 counts as registered).

Usage:
    python3 tools/check-alignment-register-on-pr.py                 # CI (GITHUB_BASE_REF)
    python3 tools/check-alignment-register-on-pr.py origin/main      # locally
    python3 tools/check-alignment-register-on-pr.py BASE HEAD --register-ref REF

Exit code once modules load: always 0 (advisory), including malformed arguments and internal errors.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from aiqt_corpus import iter_non_code_lines  # noqa: E402  # the line model gate 6 reads
from lint_common import AUDITED_DOMAIN_DIRS, PrRangeError, git, resolve_pr_range  # noqa: E402

TOOLS = Path(__file__).resolve().parent
REGISTER_REL = "governance/register-canonical-citations.md"
ALIASES_PATH = TOOLS / "alignment-register-aliases.json"
EXCLUSIONS_PATH = TOOLS / "alignment-register-exclusions.json"
# The three classes the 2026-10-16 decision names; a policy row of any other class is refused.
EXCLUSION_CLASSES = frozenset({"RFC", "vendor guidance", "book"})

# First header cells meaning "each row names one framework or standard".
LIST_HEADERS = frozenset({
    "framework", "frameworks", "framework / standard", "framework or standard",
    "framework / regulation", "standard", "standards", "standard / framework",
    "regulation", "regulations", "regulation / guidance", "regulation / standard",
    "law / regulation",
})
# Column headers whose cells are a free-text list of citations.
FREE_TEXT_HEADERS = frozenset({
    "regulatory", "regulatory references", "regulatory reference", "legal",
    "legal / regulatory", "other", "other references", "trade compliance",
    "framework reference", "framework references", "trade and supply chain programs",
})
# A matrix-header table is recognized only under one of these headings.
ALIGNMENT_HEADING = re.compile(r"framework alignment|crosswalk|standards alignment", re.I)

SEPARATOR = re.compile(r"\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)*\|?\s*")
HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")

# EU/EC instrument numbers. A number counts when the instrument carries an EU/EC marker or
# suffix, or when one side of the number is a four-digit year (the register's own bare
# "Regulation 2016/679" form); ``num`` is compared verbatim with leading zeros dropped.
EU_NUMBER = re.compile(
    r"\b(?P<kind>(?:(?:Commission|Council)\s+)?(?:(?:Implementing|Delegated)\s+)?"
    r"(?:Regulation|Directive|Decision|Recommendation))"
    r"\s+(?:\((?P<marker>EU|EC|EEC|EU,\s*Euratom)\)\s+)?(?:No\.?\s+)?"
    r"(?P<num>\d{1,4}/\d{1,4})(?:/(?P<suffix>EC|EEC|EU))?(?![\w/])"
    r"|\((?P<marker2>EU|EC|EEC)\)\s+(?:No\.?\s+)?(?P<num2>\d{1,4}/\d{1,4})(?![\w/])"
)

# A trailing edition or version written after a framework name.
VERSION_TAIL = re.compile(
    r"(?:[\s:,(]+(?:v(?:ersion)?\s*)?\d+(?:\.\d+)*(?:\s*\(?(?:beta|draft|final)\)?)?\)?"
    r"|[\s:,(]+(?:Rev(?:ision)?\.?\s*\d+(?:\.\d+)*|\d{4}\s+edition|edition\s+\d+|beta|draft)\)?"
    r"|:\d{4})\s*$",
    re.I,
)
# A provision reference written after a citation ("GDPR Art. 32", "EU AI Act: High Risk").
PROVISION_TAIL = re.compile(
    r"\s*(?::\s|\bArt(?:icle)?s?\b\.?|§|\bSch(?:edule)?\b\.?|\bAnnex\b|\bClauses?\b|\bSections?\b"
    r"|\bCh\b\.?\s+[IVX\d]|\bRecital\b|\bpara(?:graph)?\b\.?|\bs\.\s*\d).*$"
)
# A control code or code fragment standing alone ("A.3.4", "DE.CM-09", "SEF-07").
FRAGMENT = re.compile(
    r"(?:[A-Z]{1,4}\.)+[A-Z0-9]{1,4}(?:[.-][A-Z0-9]{1,3})*|[A-Z&]{2,5}-\d{1,3}(?:\.\d+)?"
)
# Trailing control codes in a free-text cell ("CSA CCM LOG-05", "NIST SP 800-53 CA-2"); a
# segment that is nothing but a code becomes empty and is not a citation.
CODE_TAIL = re.compile(r"(?:^|\s+)(?:[A-Z&]{2,5}-\d{1,2}(?:\.\d{1,2})?(?:\(\d+\))?\s*)+$")
ACRONYM = re.compile(r"\b[A-Z][A-Z0-9&]*[A-Z0-9](?:-[A-Z0-9]+)*\b")
INSTRUMENT_WORD = re.compile(
    r"\b(?:Act|Regulations?|Directive|Law|Code|Standard|Framework|Guidelines?|Rules?)\b"
)


def _load_gate6():
    """Gate 6's wrapper (register parser) and its pack engine (identity, discovery, resolve)."""
    spec = importlib.util.spec_from_file_location(
        "lint_standards_currency_for_d15", TOOLS / "lint-standards-currency.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module._engine()


GATE6 = ENGINE = None


def ensure_gate6():
    """Load gate 6 on demand so CLI failures can be reported as advisory notes."""
    global GATE6, ENGINE
    if ENGINE is None:
        GATE6, ENGINE = _load_gate6()


def identity_key(name: str) -> str:
    ensure_gate6()
    return ENGINE.identity_key(name)


class PolicyError(ValueError):
    pass


def load_exclusions(text: str) -> list[dict]:
    """Validate and compile the exclusion policy. Every row names its class (one of the three
    the decision covers) and a reason; a pattern row must compile, an entry row names an exact
    citation. Raises PolicyError on any malformed row."""
    data = json.loads(text)
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise PolicyError("exclusion policy: schema_version 1 required")
    rows = []
    for kind in ("patterns", "entries"):
        items = data.get(kind)
        if not isinstance(items, list):
            raise PolicyError(f"exclusion policy: {kind!r} must be a list")
        for n, item in enumerate(items, 1):
            where = f"exclusion policy {kind}[{n}]"
            if not isinstance(item, dict):
                raise PolicyError(f"{where}: must be an object")
            if item.get("class") not in EXCLUSION_CLASSES:
                raise PolicyError(f"{where}: class must be one of {sorted(EXCLUSION_CLASSES)}")
            reason = item.get("reason")
            if not isinstance(reason, str) or len(reason.strip()) < 10:
                raise PolicyError(f"{where}: a reason of at least ten characters is required")
            key = "pattern" if kind == "patterns" else "name"
            value = item.get(key)
            if not isinstance(value, str) or not value.strip():
                raise PolicyError(f"{where}: {key!r} required")
            if kind == "patterns":
                try:
                    matcher = re.compile(value, re.I)
                except re.error as exc:
                    raise PolicyError(f"{where}: pattern does not compile ({exc})") from None
            else:
                matcher = re.compile(r"(?<!\w)" + re.escape(value) + r"(?!\w)", re.I)
            rows.append(dict(cls=item["class"], reason=reason, label=value, matcher=matcher))
    return rows


def load_aliases(text: str) -> dict:
    """Aliases (corpus name to register Standard ID), umbrella patterns (a family citation to
    the row that covers it) and the not-citable vocabulary."""
    data = json.loads(text)
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise PolicyError("alias file: schema_version 1 required")
    aliases = data.get("aliases", {})
    umbrella = data.get("umbrella", [])
    not_citable = data.get("not_citable", {})
    if not isinstance(aliases, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in aliases.items()
    ):
        raise PolicyError("alias file: 'aliases' must map names to register Standard IDs")
    if not isinstance(umbrella, list):
        raise PolicyError("alias file: 'umbrella' must be a list")
    if not isinstance(not_citable, dict):
        raise PolicyError("alias file: 'not_citable' must be an object")
    for key in ("exact", "patterns"):
        values = not_citable.get(key, [])
        if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
            raise PolicyError(f"alias file: 'not_citable.{key}' must be a list of strings")
    compiled = []
    for n, item in enumerate(umbrella, 1):
        try:
            compiled.append((re.compile(item["pattern"], re.I), item["row"]))
        except (KeyError, TypeError, re.error) as exc:
            raise PolicyError(f"alias file: umbrella[{n}] malformed ({exc})") from None
    exact = {identity_key(v) for v in not_citable.get("exact", [])}
    try:
        patterns = [re.compile(p, re.I) for p in not_citable.get("patterns", [])]
    except re.error as exc:
        raise PolicyError(f"alias file: not_citable pattern does not compile ({exc})") from None
    return dict(
        aliases={identity_key(k): v for k, v in aliases.items()},
        umbrella=compiled,
        not_citable_exact=exact,
        not_citable_patterns=patterns,
    )


def eu_numbers(text: str) -> list[tuple[str, str]]:
    """(observed, number) for each EU/EC instrument number in ``text``."""
    out = []
    for m in EU_NUMBER.finditer(text):
        num = m["num"] or m["num2"]
        marked = bool(m["marker"] or m["suffix"] or m["marker2"])
        left, right = num.split("/")
        if not marked and not any(len(p) == 4 and 1950 <= int(p) <= 2099 for p in (left, right)):
            continue
        out.append((m[0], f"{int(left)}/{int(right)}"))
    return out


class Register:
    """The register rows as gate 6 parses them, plus the lookups this check adds."""

    def __init__(self, text: str):
        ensure_gate6()
        self.entries = GATE6.parse_register_text(text)
        self.ids = {e["identity_key"]: e["id"] for e in self.entries}
        self.numbers = set()
        self.designators = set()
        for e in self.entries:
            cells = e["cells"]
            for cell in (cells[0], cells[1], cells[4]):
                self.numbers.update(num for _, num in eu_numbers(cell))
            self.designators.update(designators(e["id"]))

    def has_id(self, std_id: str) -> bool:
        return identity_key(std_id) in self.ids

    def by_suffix(self, name: str) -> bool:
        """``name`` is the whole-word tail of a Standard ID (``GDPR`` of ``EU GDPR``). A
        one-word name qualifies only when it is an acronym or carries a digit."""
        key = identity_key(name)
        if len(key.split()) < 2 and not (ACRONYM.fullmatch(name) or re.search(r"\d", name)):
            return False
        return any(k.endswith(" " + key) for k in self.ids)

    def by_series(self, key: str) -> bool:
        """``key`` is a series stem of a Standard ID: the ID continues with a part number
        (``IEC 62443`` of ``IEC 62443-3-3``) or with an edition or qualifier (``BASC
        International Security Standard`` of ``... 6.0.2 (2022, ...)``)."""
        for k in self.ids:
            tail = k[len(key):] if k.startswith(key) and len(k) > len(key) else ""
            if (key[-1:].isdigit() and tail[:1] == "-") or re.match(r" (?:\d|series\b|\()", tail):
                return True
        return False

    def by_edition(self, key: str) -> bool:
        """``key`` is a Standard ID followed by an edition and a qualifier (``CSA CCM v4.1 DSP
        domain``): the edition token marks where the registered name ends."""
        return any(re.match(re.escape(k) + r" v?\d", key) for k in self.ids)


# EDPB and Article 29 Working Party designators ("Guidelines 07/2020", "Opinion 05/2014",
# "WP248"), compared with the leading zero dropped, so a long-form citation of a registered
# soft-law document matches its row whatever title wording follows the designator.
DESIGNATOR = re.compile(
    r"\b(?:(Guidelines|Opinion|Recommendations?|Statement)\s+0*(\d{1,2})/(\d{4})|WP\s?(\d{2,3}))\b",
    re.I,
)


def designators(text: str) -> set[str]:
    if not re.search(r"\b(?:EDPB|Article 29|WP\s?\d)", text, re.I):
        return set()
    out = set()
    for m in DESIGNATOR.finditer(text):
        out.add(f"wp{m[4]}" if m[4] else f"{m[1].lower().rstrip('s')} {int(m[2])}/{m[3]}")
    return out


def strip_markdown(cell: str) -> str:
    cell = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", cell)
    cell = re.sub(r"<br\s*/?>", "; ", cell, flags=re.I)
    cell = re.sub(r"<[^>]+>", "", cell)
    cell = cell.replace("\\|", "|")
    cell = re.sub(r"[*_`]", "", cell)
    return re.sub(r"\s+", " ", cell).strip()


def strip_version(name: str) -> str:
    prev = None
    while prev != name:
        prev, name = name, VERSION_TAIL.sub("", name).strip()
    return name


class Resolver:
    def __init__(self, register: Register, aliases: dict, exclusions: list[dict]):
        self.register, self.aliases, self.exclusions = register, aliases, exclusions

    def excluded(self, text: str):
        for row in self.exclusions:
            if row["matcher"].search(text):
                return row
        return None

    def not_citable(self, name: str) -> bool:
        key = identity_key(name)
        if not key or key in self.aliases["not_citable_exact"]:
            return True
        if any(p.fullmatch(name) for p in self.aliases["not_citable_patterns"]):
            return True
        # A leading digit or lowercase letter alone does not make an instrument prose:
        # "21 CFR Part 11" and "ePrivacy Directive" still need register lookup.
        instrument = bool(INSTRUMENT_WORD.search(name) or re.search(r"\bCFR\b", name))
        if FRAGMENT.fullmatch(name):
            return True
        if name[0].isdigit() and not instrument:
            return True
        if name[0].islower() and not (instrument or re.search(r"\d", name)):
            return True
        # A citation has a shape: an acronym, a digit, or an instrument word with a name.
        return not (
            ACRONYM.search(name) or re.search(r"\d", name)
            or (INSTRUMENT_WORD.search(name) and len(name.split()) > 1)
        )

    def name_registered(self, name: str) -> bool:
        reg = self.register
        bare = name.split("(", 1)[0].strip()
        candidates = {name, strip_version(name), bare, strip_version(bare)}
        for inner in re.findall(r"\(([^()]*)\)", name):  # an acronym or alias in parentheses
            candidates |= {inner.strip(), strip_version(inner.strip())}
        for cand in filter(None, candidates):
            key = identity_key(cand)
            if key in reg.ids or (key in self.aliases["aliases"] and reg.has_id(self.aliases["aliases"][key])):
                return True
            if any(p.fullmatch(cand) and reg.has_id(row) for p, row in self.aliases["umbrella"]):
                return True
            if reg.by_suffix(cand) or reg.by_series(key) or reg.by_edition(key):
                return True
        if designators(name) & reg.designators:
            return True
        # A comma list in a name cell ("EU AI Act, GDPR") is registered when every member is.
        parts = [p.strip() for p in bare.split(",")]
        return len(parts) > 1 and all(p and self.name_registered(p) for p in parts)

    def resolve(self, text: str) -> list[tuple[str, str]]:
        """(status, detail) per citation in one cell or segment: status is ``registered``,
        ``excluded``, ``not-citable`` or ``unregistered``. A registered citation is registered
        even when it also matches the exclusion policy (a registered vendor framework stays
        tracked); the policy decides only what an unregistered citation means."""
        text = strip_markdown(text)
        if not text:
            return [("not-citable", "")]
        grammar = [o for o in ENGINE.discover(text, ".md") if o["channel"] == "grammar"]
        if grammar:
            out = []
            for occ in grammar:
                kinds = [k for k, _ in ENGINE.resolve(occ, self.register.entries, GATE6.BARE_EXCEPTIONS)]
                observed = occ["observed"]
                if "UNREGISTERED" in kinds and not (
                    self.register.by_series(occ["identity"]) or self.name_registered(observed)
                ):
                    out.append(self._unregistered(observed))
                else:
                    out.append(("registered", observed))
            return out
        if self.name_registered(text):
            return [("registered", text)]
        return [self._unregistered(text)]

    def _unregistered(self, text: str) -> tuple[str, str]:
        row = self.excluded(text)
        if row:
            return ("excluded", f"{row['cls']}: {row['reason']}")
        if self.not_citable(text):
            return ("not-citable", text)
        return ("unregistered", text)


def split_parts(cell: str, free_text: bool) -> list[str]:
    """Split a cell into citations. Both kinds split on ";" outside parentheses and on " / "
    and " + "; a free-text cell also splits on ",". Each segment loses its provision suffix
    ("Art. 32", ": High Risk"), and a free-text segment its trailing control codes ("CSA CCM
    LOG-05"). A link to a corpus document is an internal reference, not a citation."""
    cell = re.sub(r"\[[^\]]*\]\((?!https?:)[^)]*\.md(?:#[^)]*)?\)", "", cell)
    cell = strip_markdown(cell)
    stops = ";," if free_text else ";"
    depth, buf, parts = 0, [], []
    for ch in cell:
        depth += ch == "("
        depth -= ch == ")" and depth > 0
        if ch in stops and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf))
    out = []
    for part in parts:
        for seg in re.split(r"\s+/\s+|\s+\+\s+", part):
            seg = PROVISION_TAIL.sub("", seg)
            if free_text:
                seg = CODE_TAIL.sub("", seg)
            seg = seg.strip(" .")
            if seg:
                out.append(seg)
    return out


def cells_of(line: str) -> list[str]:
    raw = line.strip()
    if raw.startswith("|"):
        raw = raw[1:]
    if raw.endswith("|") and not raw.endswith("\\|"):
        raw = raw[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", raw)]


def iter_tables(lines: list[str], eligible: set[int]):
    """Yield (header_line_no, header_cells, row_line_nos, heading) for each pipe table."""
    heading, i = "", 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in eligible and re.match(r"#{1,6}\s", line):
            heading = line
        if (
            i + 1 in eligible and line.lstrip().startswith("|")
            and i + 1 < len(lines) and SEPARATOR.fullmatch(lines[i + 1])
        ):
            header = cells_of(line)
            j = i + 2
            rows = []
            while j < len(lines) and lines[j].lstrip().startswith("|") and j + 1 in eligible:
                rows.append(j + 1)
                j += 1
            yield i + 1, header, rows, heading
            i = j
            continue
        i += 1


def scan_text(text: str, added: set[int], resolver: Resolver) -> list[tuple[int, str, str]]:
    """(line_no, surface, citation) for each unregistered citation on an added line of one
    Markdown document. PURE over its inputs, so the unit tests drive it without git."""
    lines = text.splitlines()
    eligible = {ln for ln, _ in iter_non_code_lines(text)}
    found: list[tuple[int, str, str]] = []

    def record(ln, surface, cell, free_text):
        for part in split_parts(cell, free_text):
            for status, detail in resolver.resolve(part):
                if status == "unregistered":
                    found.append((ln, surface, detail))

    for header_ln, header, rows, heading in iter_tables(lines, eligible):
        norm = [identity_key(strip_markdown(h)) for h in header]
        list_form = bool(norm) and norm[0] in LIST_HEADERS
        matrix_form = not list_form and bool(ALIGNMENT_HEADING.search(heading))
        if not (list_form or matrix_form):
            continue
        free_cols = {i for i, h in enumerate(norm) if h in FREE_TEXT_HEADERS}
        if matrix_form and header_ln in added:
            for i, cell in enumerate(header[1:], 1):
                if i not in free_cols:
                    record(header_ln, "alignment-table header", cell, False)
        for ln in rows:
            if ln not in added:
                continue
            row = cells_of(lines[ln - 1])
            if list_form and row:
                record(ln, "alignment-table row", row[0], False)
            for i in sorted(free_cols):
                if i < len(row):
                    record(ln, "citation-list cell", row[i], True)

    for ln in sorted(added & eligible):
        if ln - 1 >= len(lines):
            continue
        for observed, num in eu_numbers(lines[ln - 1]):
            # A table cell already reported as this instrument is not reported twice.
            if num not in resolver.register.numbers and not any(
                f[0] == ln and observed in f[2] for f in found
            ):
                found.append((ln, "EU/EC instrument number", observed))

    seen, out = set(), []
    for item in sorted(found):
        key = (item[0], identity_key(item[2]))
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def added_lines(diff: str) -> set[int]:
    """Head-side line numbers a unified ``-U0`` diff adds or changes."""
    out: set[int] = set()
    for line in diff.splitlines():
        m = HUNK.match(line)
        if m:
            start, count = int(m[1]), int(m[2] if m[2] is not None else 1)
            out.update(range(start, start + count))
    return out


def in_scope(rel: str) -> bool:
    ensure_gate6()
    if not rel.endswith(".md") or rel in GATE6.EXEMPT_FILES:
        return False
    return rel.split("/", 1)[0] in AUDITED_DOMAIN_DIRS and "/" in rel


def build_resolver(register_text: str) -> Resolver:
    return Resolver(
        Register(register_text),
        load_aliases(ALIASES_PATH.read_text(encoding="utf-8")),
        load_exclusions(EXCLUSIONS_PATH.read_text(encoding="utf-8")),
    )


def run(base: str | None, head: str, register_ref: str | None) -> int:
    try:
        merge_base, head = resolve_pr_range(base, head)
    except PrRangeError as exc:
        print(f"D15 NOTE: {exc} Advisory check skipped (fail-open).")
        return 0
    try:
        register_text = subprocess.check_output(
            ["git", "show", f"{register_ref or head}:{REGISTER_REL}"],
            text=True, stderr=subprocess.DEVNULL,
        ).rstrip("\n")
    except subprocess.CalledProcessError:
        print(f"D15 NOTE: {REGISTER_REL} is absent at {register_ref or head}; nothing to check against.")
        return 0
    try:
        resolver = build_resolver(register_text)
    except (OSError, ValueError) as exc:  # PolicyError, RegisterError and JSON errors
        print(f"D15 NOTE: cannot load the register or the D15 policy files ({exc}); advisory check skipped (fail-open).")
        return 0
    try:
        names = git("diff", "--name-only", "--no-renames", "-z", merge_base, head).split("\0")
    except subprocess.CalledProcessError as exc:
        print(f"D15 NOTE: git diff failed ({exc}); advisory check skipped (fail-open).")
        return 0
    files = sorted(n for n in names if n and in_scope(n))
    hits = []
    for rel in files:
        try:
            diff = git("diff", "-U0", "--no-renames", merge_base, head, "--", rel)
            text = git("show", f"{head}:{rel}")
        except subprocess.CalledProcessError:
            continue  # deleted in the PR: nothing added
        for ln, surface, citation in scan_text(text, added_lines(diff), resolver):
            hits.append((rel, ln, surface, citation))
    if not hits:
        print(f"D15 OK: {len(files)} corpus document(s) changed; no added citation lacks a register row.")
        return 0
    for rel, ln, surface, citation in hits:
        print(f"D15 WARN {rel}:{ln}: {surface} {citation!r} has no row in {REGISTER_REL}")
    print(
        f"D15 ADVISORY: {len(hits)} added citation(s) with no register row. Add a row (see the "
        f"register's Maintenance section), curate an alias in "
        f"tools/{ALIASES_PATH.name}, or, for an RFC, vendor guidance or a book, an entry in "
        f"tools/{EXCLUSIONS_PATH.name}. Warning only; exit 0."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    class AdvisoryParser(argparse.ArgumentParser):
        def error(self, message):
            raise PolicyError(f"argument error: {message}")

    try:
        ap = AdvisoryParser(description="D15: advisory alignment-citation register check.")
        ap.add_argument("base", nargs="?", default=None, help="base ref (default: origin/$GITHUB_BASE_REF)")
        ap.add_argument("head", nargs="?", default="HEAD", help="head ref (default: HEAD)")
        ap.add_argument(
            "--register-ref", default=None,
            help="read the register at this ref instead of the head (replays an old PR against today's register)",
        )
        args = ap.parse_args(argv)
        ensure_gate6()
        return run(args.base, args.head, args.register_ref)
    except Exception as exc:
        print(f"D15 NOTE: {exc}; advisory check skipped (fail-open).")
        return 0


if __name__ == "__main__":
    sys.exit(main())
