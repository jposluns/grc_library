#!/usr/bin/env python3
"""Sync the "Expected value" cells of a citation-verification worklist to the canonical
citations register, DETERMINISTICALLY and WITHOUT FABRICATION.

WHY THIS EXISTS (P-1.65). The worklist "Expected value (from register)" cells were AI-prefilled
at a PAST register state and drift as the register moves (EU AI Act, CCPA, CMMC, NERC CIP, ...).
Hand-sync proved error-prone (a fabricated "supersedes" was introduced once). The register
(governance/register-canonical-citations.md) is the single source of truth for a citation's
Current version / Publication date / Superseded versions, keyed by Standard ID.

WHAT IS AND IS NOT DERIVABLE. Version, publication date, and superseded list are 1:1 register
fields. TOPIC IS NOT: every worklist PARAPHRASES it, so this tool NEVER regenerates topic; it
preserves the cell's topic and any editorial prose verbatim and rewrites ONLY the version token
and the superseded-list value.

SAFETY MODEL (never fabricate; a row is edited only when it is unambiguously safe, else reported):
  * Join by EXACT (whitespace-normalized) Standard ID. No exact register row => UNMATCHED, no edit.
  * A cell is edited ALL-OR-NOTHING: if any needed change is unsafe, the whole row is left and
    reported (no half-edited cells; keeps the run idempotent).
  * DELIMITER-COLLISION: a register value that would inject the cell's structural delimiter
    (", " for comma-positional cells, "; " for labelled/semicolon cells) is REFUSED. This routes
    every long-narrative register value (CCPA, CMMC, UK GDPR, NIST 1900, EN 54, Basel III,
    NERC CIP, HIPAA, Australia Privacy Act) to a human, uncorrupted.
  * SUPERSEDES-STRUCTURE: if the register and the cell disagree on whether a supersedes clause is
    PRESENT (register says none but the cell asserts one, or vice versa), the row is REFUSED. This
    is the eIDAS / OECD "amended-base-not-superseded" reframe, and refusing it is the exact guard
    against the fabricated-supersedes incident.
  * UNPARSEABLE: a cell whose structure the tool cannot round-trip (ISO 16484's multi-part
    "Current:" field embeds "; ") is left and reported.
  * Publication-date divergences are ADVISORY (reported, never auto-edited): they are usually
    granularity noise (e.g. "2025" vs "2025-02") and the positional-comma cases are collision-prone.

IDEMPOTENCE. Re-running changes nothing once a row is synced: the new version token equals the
register value, so recomputation is a no-op. --check re-derives and compares; it never writes.

SCOPE. Reads register-canonical-citations.md. Operates on ONE worklist file naming an
"Expected value (from register)" or "Expected value" column (batch Q2 and Q4). Batch Q3.1 shares
the format (currently drift-free). Batch Q3 (AI tooling provenance) has NO such column and is
out of scope; pointing the tool at it yields "no expected-value column found".

Usage:
  python3 tools/sync-citation-worklist-baseline.py --worklist <path>            # apply safe edits
  python3 tools/sync-citation-worklist-baseline.py --worklist <path> --check    # drift check (CI-parity)
  python3 tools/sync-citation-worklist-baseline.py --worklist <path> --report   # dry-run, list every row
  python3 tools/sync-citation-worklist-baseline.py --self-test                  # in-process unit self-check

--check exits 1 ONLY on a SAFE-SYNC drift (a row the tool could and should sync but has not).
NEEDS-HUMAN / UNMATCHED / advisory rows are reported but do NOT fail --check (they are not the
tool's to fix), so a maintainer who has run the tool sees a clean --check.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_common import REPO_ROOT  # noqa: E402

DEFAULT_REGISTER = REPO_ROOT / "governance" / "register-canonical-citations.md"

# Column headers that identify the expected-value column across the worklist variants.
EXPECTED_HEADERS = ("Expected value (from register)", "Expected value")
STANDARD_ID_HEADERS = ("Standard ID",)

# Register table header cells we key on. A register table is parsed only if it has a
# "Current version" column; the Standard-ID column is "Standard ID" or "Project".
REG_ID_HEADERS = ("Standard ID", "Project")
REG_VERSION_HEADER = "Current version"
REG_PUBDATE_HEADERS = ("Publication date", "Registration date")
REG_SUPERSEDED_HEADER = "Superseded versions"

SUPERSEDE_RE = re.compile(r";\s*(supersedes|superseded)\s+(.+?)(\s*\(per register\))?\s*$",
                          re.IGNORECASE)
NO_SUPERSEDE_RE = re.compile(r";\s*no superseded versions recorded\s*$", re.IGNORECASE)


# ----------------------------------------------------------------------------- register parse
def _split_row(line):
    """Split a markdown table row into trimmed cell texts (drop the outer empties)."""
    parts = [c.strip() for c in line.strip().strip("|").split("|")]
    return parts


def _is_separator(cells):
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c != "")


def norm_id(text):
    return re.sub(r"\s+", " ", text).strip()


def parse_register(text):
    """Return {normalized Standard ID: {'version','pubdate','superseded','raw_id'}}.

    Only tables carrying a 'Current version' column are read; the last-seen header row governs
    the following data rows until the next header or a blank line ends the block.
    """
    reg = {}
    header = None  # list of header cell texts
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            header = None
            continue
        cells = _split_row(line)
        if _is_separator(cells):
            continue
        if header is None:
            if REG_VERSION_HEADER in cells and any(h in cells for h in REG_ID_HEADERS):
                header = cells
            continue
        # data row under an active header
        idx = {h: i for i, h in enumerate(header)}
        id_col = next((idx[h] for h in REG_ID_HEADERS if h in idx), None)
        ver_col = idx.get(REG_VERSION_HEADER)
        if id_col is None or ver_col is None or id_col >= len(cells):
            continue
        raw_id = cells[id_col]
        if not raw_id or raw_id in REG_ID_HEADERS:
            continue
        pub_col = next((idx[h] for h in REG_PUBDATE_HEADERS if h in idx), None)
        sup_col = idx.get(REG_SUPERSEDED_HEADER)
        reg[norm_id(raw_id)] = {
            "raw_id": raw_id,
            "version": cells[ver_col].strip() if ver_col < len(cells) else "",
            "pubdate": cells[pub_col].strip() if pub_col is not None and pub_col < len(cells) else "",
            "superseded": cells[sup_col].strip() if sup_col is not None and sup_col < len(cells) else "-",
        }
    return reg


# ----------------------------------------------------------------------------- cell model
class Cell:
    """A parsed expected-value cell. grammar is 'labelled' | 'comma' | 'semicolon'."""
    def __init__(self, grammar, ver_start, ver_end, sup_present, sup_value, sup_span):
        self.grammar = grammar
        self.ver_start, self.ver_end = ver_start, ver_end
        self.sup_present = sup_present
        self.sup_value = sup_value
        self.sup_span = sup_span  # (start,end) of the supersede VALUE, or None


def parse_cell(cell):
    """Structurally parse a cell, or return None if it cannot be round-tripped safely."""
    if not cell.strip():
        return None
    # supersedes clause (terminal): value only, "(per register)" suffix preserved outside span.
    sup_present, sup_value, sup_span = False, None, None
    m = SUPERSEDE_RE.search(cell)
    if m:
        sup_present, sup_value = True, m.group(2).strip()
        sup_span = (m.start(2), m.end(2))
    elif NO_SUPERSEDE_RE.search(cell):
        sup_present, sup_value = False, None  # explicit "none recorded"
    # version token
    if cell.startswith("Current:"):
        grammar = "labelled"
        vs = len("Current:")
        while vs < len(cell) and cell[vs] == " ":
            vs += 1
        ve = cell.find(";", vs)
        if ve == -1:
            ve = len(cell)
        # a labelled cell whose Current field itself contains "; " before the next label is
        # ambiguous (ISO 16484): refuse.
        rest = cell[ve:]
        if not re.match(r";\s*(published|topic:|supersedes|superseded|no superseded)", rest, re.IGNORECASE) \
           and rest.strip() not in ("",):
            return None
        return Cell("labelled", vs, ve, sup_present, sup_value, sup_span)
    # positional: comma-first or semicolon-first, whichever delimiter appears first
    comma = cell.find(", ")
    semi = cell.find("; ")
    if comma == -1 and semi == -1:
        return None
    if comma != -1 and (semi == -1 or comma < semi):
        return Cell("comma", 0, comma, sup_present, sup_value, sup_span)
    return Cell("semicolon", 0, semi, sup_present, sup_value, sup_span)


def _field_delim(grammar):
    return ", " if grammar == "comma" else "; "


# ----------------------------------------------------------------------------- pure decision core
def decide(cell_text, reg):
    """Pure function. Return (status, new_cell_text_or_None, detail).

    status in {'OK','SYNC','UNMATCHED','UNPARSEABLE','DELIMITER-COLLISION',
               'SUPERSEDES-STRUCTURE','NON-APPEND','ADVISORY'}.
    Only 'SYNC' yields a new_cell_text.
    """
    if reg is None:
        return ("UNMATCHED", None, "no exact register row for this Standard ID")
    parsed = parse_cell(cell_text)
    if parsed is None:
        return ("UNPARSEABLE", None, "cell structure not recognized / not round-trippable")

    delim = _field_delim(parsed.grammar)
    old_version = cell_text[parsed.ver_start:parsed.ver_end].strip()
    reg_version = reg["version"].strip()
    reg_sup = reg["superseded"].strip()
    reg_has_sup = reg_sup not in ("", "-")

    # supersedes structure must agree before any edit (avoid the reframe / fabrication class).
    if reg_has_sup != parsed.sup_present:
        return ("SUPERSEDES-STRUCTURE", None,
                f"register supersedes={'present' if reg_has_sup else 'none'} but cell "
                f"supersedes={'present' if parsed.sup_present else 'none'}")

    changes = []
    new_cell = cell_text

    # version token
    version_changed = norm_id(old_version) != norm_id(reg_version)
    # a case-only difference is cosmetic, not drift: treat as no change.
    if version_changed and norm_id(old_version).lower() == norm_id(reg_version).lower():
        version_changed = False
    if version_changed:
        if delim in reg_version or "; " in reg_version:
            return ("DELIMITER-COLLISION", None,
                    f"register version {reg_version!r} contains a structural delimiter; "
                    f"cannot inject into a {parsed.grammar} cell")
        # a register version whose text the supersedes parser would read as a clause (";supersedes",
        # even with no space or a tab) must be refused: injecting it fabricates a supersedes structure.
        if re.search(r";\s*(supersedes|superseded|no superseded versions recorded)", reg_version, re.IGNORECASE):
            return ("DELIMITER-COLLISION", None,
                    f"register version {reg_version!r} embeds a supersedes-clause token; "
                    f"injecting it would fabricate a supersedes structure")
        # SAFE-SYNC only when the register value APPENDS to the cell value (no information
        # lost). A non-append change (shortening, reformat, or a replacement) would delete a
        # human annotation the worklist deliberately carries, so it routes to a human.
        if not (norm_id(reg_version).startswith(norm_id(old_version))
                and len(norm_id(reg_version)) > len(norm_id(old_version))):
            return ("NON-APPEND", None,
                    f"version divergence is not a safe append: cell {old_version!r} vs "
                    f"register {reg_version!r}; a human decides (the cell may carry intended "
                    f"annotation the register lacks)")
        changes.append(("version", old_version, reg_version))

    # supersedes value (only when both present)
    sup_changed = False
    if reg_has_sup and parsed.sup_present:
        if norm_id(parsed.sup_value).lower() != norm_id(reg_sup).lower() \
           and norm_id(parsed.sup_value) != norm_id(reg_sup):
            if "; " in reg_sup:
                return ("DELIMITER-COLLISION", None,
                        f"register superseded {reg_sup!r} contains '; '")
            # mirror the version-branch structural-token guard (CITATION-SYNC-001-RESIDUAL): a
            # superseded value whose text the parser would read as a further supersedes clause
            # (";supersedes", even with a tab/NBSP and no space) must be refused, not injected.
            if re.search(r";\s*(supersedes|superseded|no superseded versions recorded)", reg_sup, re.IGNORECASE):
                return ("DELIMITER-COLLISION", None,
                        f"register superseded {reg_sup!r} embeds a supersedes-clause token; "
                        f"injecting it would fabricate clause structure")
            if not (norm_id(reg_sup).startswith(norm_id(parsed.sup_value))
                    and len(norm_id(reg_sup)) > len(norm_id(parsed.sup_value))):
                return ("NON-APPEND", None,
                        f"superseded divergence is not a safe append: cell "
                        f"{parsed.sup_value!r} vs register {reg_sup!r}; a human decides")
            sup_changed = True
            changes.append(("superseded", parsed.sup_value, reg_sup))

    # pubdate: advisory only (never auto-edited).
    advisory = None
    if reg["pubdate"] and reg["pubdate"] != "-":
        # best-effort: note when the cell clearly omits/mismatches the register pubdate token
        if reg["pubdate"] not in cell_text:
            advisory = f"publication date {reg['pubdate']!r} not present in cell (advisory only)"

    if not changes:
        if advisory:
            return ("ADVISORY", None, advisory)
        return ("OK", None, "in sync")

    # apply all-or-nothing, rightmost span first so earlier offsets stay valid.
    edits = []
    if version_changed:
        edits.append((parsed.ver_start, parsed.ver_end, reg_version))
    if sup_changed:
        edits.append((parsed.sup_span[0], parsed.sup_span[1], reg_sup))
    for start, end, repl in sorted(edits, key=lambda e: e[0], reverse=True):
        new_cell = new_cell[:start] + repl + new_cell[end:]

    # round-trip guard: re-parse and confirm the tool's own read of the new cell matches the
    # register on BOTH the version token AND the supersedes structure (presence + value). This is
    # the backstop against an edit that fabricates or drops a supersedes clause (CITATION-SYNC-001).
    rt = parse_cell(new_cell)
    if rt is None or norm_id(new_cell[rt.ver_start:rt.ver_end].strip()) != norm_id(reg_version):
        return ("UNPARSEABLE", None, "post-edit round-trip check failed; refused")
    if rt.sup_present != reg_has_sup:
        return ("SUPERSEDES-STRUCTURE", None,
                "post-edit supersedes structure diverges from register; refused (no fabrication)")
    if reg_has_sup and norm_id(rt.sup_value) != norm_id(reg_sup):
        return ("UNPARSEABLE", None, "post-edit supersedes value diverges from register; refused")
    detail = "; ".join(f"{f}: {o!r} -> {n!r}" for f, o, n in changes)
    return ("SYNC", new_cell, detail)


# ----------------------------------------------------------------------------- worklist observer
def process(worklist_text, register):
    """Return (new_text, results). results is a list of (standard_id, status, detail)."""
    lines = worklist_text.splitlines(keepends=True)
    header = None
    id_col = exp_col = None
    results = []
    out = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            header = None
            out.append(line)
            continue
        cells = _split_row(line)
        if _is_separator(cells):
            out.append(line)
            continue
        if header is None:
            exp = next((h for h in EXPECTED_HEADERS if h in cells), None)
            sid = next((h for h in STANDARD_ID_HEADERS if h in cells), None)
            if exp and sid:
                header = cells
                id_col = cells.index(sid)
                exp_col = cells.index(exp)
            out.append(line)
            continue
        # data row
        if id_col >= len(cells) or exp_col >= len(cells):
            out.append(line)
            continue
        sid = cells[id_col]
        status, new_cell, detail = decide(cells[exp_col], register.get(norm_id(sid)))
        results.append((sid, status, detail))
        if status == "SYNC" and new_cell is not None:
            # BYTE-SURGICAL edit: replace ONLY the target cell's trimmed content, preserving the
            # row's pipe structure and every other cell's original whitespace/padding.
            nl = "\n" if line.endswith("\n") else ""
            body = line[:len(line) - len(nl)] if nl else line
            segs = body.split("|")  # segs[0] and segs[-1] are the outer empties; data in segs[1:-1]
            di = exp_col + 1
            if 0 < di < len(segs) - 1:
                seg = segs[di]
                lead = seg[:len(seg) - len(seg.lstrip())]
                trail = seg[len(seg.rstrip()):]
                segs[di] = lead + new_cell + trail
                out.append("|".join(segs) + nl)
            else:
                out.append(line)
        else:
            out.append(line)
    return "".join(out), results


# ----------------------------------------------------------------------------- CLI
def _load(path):
    return Path(path).read_text(encoding="utf-8")


def run(worklist_path, register_path, mode):
    register = parse_register(_load(register_path))
    text = _load(worklist_path)
    new_text, results = process(text, register)
    would_sync = [r for r in results if r[1] == "SYNC"]
    needs_human = [r for r in results if r[1] in
                   ("UNMATCHED", "UNPARSEABLE", "DELIMITER-COLLISION", "SUPERSEDES-STRUCTURE",
                    "NON-APPEND")]
    advisory = [r for r in results if r[1] == "ADVISORY"]

    def _dump(label, rows):
        if rows:
            print(f"\n{label} ({len(rows)}):")
            for sid, status, detail in rows:
                print(f"  [{status}] {sid}: {detail}")

    if mode == "check":
        _dump("SAFE-SYNC drift (run without --check to apply)", would_sync)
        _dump("NEEDS-HUMAN (reword by hand; not the tool's to fix)", needs_human)
        _dump("ADVISORY", advisory)
        if would_sync:
            print(f"\n--check: DRIFT, {len(would_sync)} row(s) can be safely synced.")
            return 1
        print("\n--check: OK (no safe-sync drift; NEEDS-HUMAN/advisory rows do not fail the check).")
        return 0

    if mode == "report":
        _dump("WOULD-SYNC", would_sync)
        _dump("NEEDS-HUMAN", needs_human)
        _dump("ADVISORY", advisory)
        print(f"\nreport: {len(would_sync)} syncable, {len(needs_human)} need human, "
              f"{len(advisory)} advisory, {len(results)} rows scanned.")
        return 0

    # apply
    if new_text != text:
        Path(worklist_path).write_text(new_text, encoding="utf-8")
    _dump("SYNCED", would_sync)
    _dump("NEEDS-HUMAN (left untouched; reword by hand)", needs_human)
    _dump("ADVISORY", advisory)
    print(f"\napply: {len(would_sync)} row(s) synced, {len(needs_human)} left for human, "
          f"{len(advisory)} advisory.")
    return 0


def self_test():
    reg = {
        "STD A": {"raw_id": "STD A", "version": "2 as amended by X (Y)", "pubdate": "2024-07",
                  "superseded": "-"},
        "STD B": {"raw_id": "STD B", "version": "4 as amended by Z", "pubdate": "2020-09",
                  "superseded": "Rev. 3"},
        "STD C": {"raw_id": "STD C", "version": "long (a; b) prose", "pubdate": "2017", "superseded": "-"},
        "STD D": {"raw_id": "STD D", "version": "v2", "pubdate": "2024", "superseded": "-"},
        "STD E": {"raw_id": "STD E", "version": "Rev. 5", "pubdate": "2020-09", "superseded": "-"},
        "STD F": {"raw_id": "STD F", "version": "v2", "pubdate": "2020", "superseded": "Rev. 1"},
        "STD G": {"raw_id": "STD G", "version": "v1", "pubdate": "2024",
                  "superseded": "v0;\tsupersedes v-1"},
    }
    cases = []
    # comma-positional, APPEND version injection -> SYNC (register extends the cell value)
    s, n, _ = decide("2, 2024-07, topic prose", reg["STD A"])
    cases.append(("A append-sync", s == "SYNC" and n == "2 as amended by X (Y), 2024-07, topic prose"))
    # already synced -> OK (idempotence)
    s2, _, _ = decide("2 as amended by X (Y), 2024-07, topic prose", reg["STD A"])
    cases.append(("A idempotent", s2 == "OK"))
    # labelled, APPEND version, topic preserved, superseded unchanged -> SYNC
    s, n, _ = decide("Current: 4; published 2020-09; topic: Foo; supersedes Rev. 3", reg["STD B"])
    cases.append(("B append-sync", s == "SYNC" and "topic: Foo" in n and "4 as amended by Z" in n))
    # NON-APPEND version replacement (would replace, not extend) -> refused to human
    s, n, _ = decide("Current: 4; published 2020-09; topic: Foo", reg["STD E"])
    cases.append(("E non-append", s == "NON-APPEND" and n is None))
    # NON-APPEND superseded shortening (version MATCHES so the superseded branch is reached;
    # register value is shorter and would DELETE the cell annotation) -> refused.
    s, n, d = decide("v2, 2020, topic; supersedes Rev. 1, 2014 (per note #42)", reg["STD F"])
    cases.append(("F sup-shorten", s == "NON-APPEND" and n is None and "superseded" in d.lower()))
    # delimiter collision -> refused
    s, n, _ = decide("2, 2017, topic", reg["STD C"])
    cases.append(("C collision", s == "DELIMITER-COLLISION" and n is None))
    # supersedes reframe (cell asserts one, register none) -> refused
    s, n, _ = decide("v1, 2024, topic; supersedes v0", reg["STD D"])
    cases.append(("D reframe", s == "SUPERSEDES-STRUCTURE" and n is None))
    # superseded value embedding a clause token (";\tsupersedes") -> refused, no injection
    # (CITATION-SYNC-001-RESIDUAL: the superseded branch mirrors the version-branch guard).
    s, n, _ = decide("v1, 2024, topic; supersedes v0", reg["STD G"])
    cases.append(("G sup-clause-inject", s == "DELIMITER-COLLISION" and n is None))
    # unmatched id -> refused
    s, n, _ = decide("anything", None)
    cases.append(("unmatched", s == "UNMATCHED" and n is None))
    ok = all(p for _, p in cases)
    for name, p in cases:
        print(f"  {'PASS' if p else 'FAIL'}: {name}")
    print("self-test:", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="Sync worklist expected-value cells to the citations register.")
    ap.add_argument("--worklist")
    ap.add_argument("--register", default=str(DEFAULT_REGISTER))
    ap.add_argument("--check", action="store_true", help="drift check; exit 1 on safe-sync drift")
    ap.add_argument("--report", action="store_true", help="dry-run; list every row, exit 0")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.worklist:
        ap.error("--worklist is required (unless --self-test)")
    # 3b50b2e1: a missing, empty or directory --worklist / --register raised a traceback.
    for flag, path in (("--worklist", args.worklist), ("--register", args.register)):
        if not path.strip() or not Path(path).is_file():
            print(f"ERROR: {flag} {path!r}: not a regular file; nothing would be synced.",
                  file=sys.stderr)
            return 2
    mode = "check" if args.check else "report" if args.report else "apply"
    return run(args.worklist, args.register, mode)


if __name__ == "__main__":
    raise SystemExit(main())
