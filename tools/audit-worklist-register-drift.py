#!/usr/bin/env python3
"""Detect (and, narrowly, rewrite) drift between the citation-verification worklists'
``Expected value (from register)`` cells and ``governance/register-canonical-citations.md``.

P-1.65. ``--check`` (default, gate-able) is the load-bearing deliverable: it parses each
worklist's verification table by HEADER SIGNATURE (a header carrying both ``Standard ID`` and
an ``Expected value`` column, so batch-metadata / cluster-count / separator rows are ignored),
maps each Standard ID to the register (exact -> alias -> FLAG, never guess), classifies the
register's current-version value as a comparable TOKEN or a free-text DESCRIPTOR (a descriptor
is reported UNVERIFIABLE, never DRIFT: the false-positive fix for register values like
``continuous`` / ``series (...)`` / ``1988, as amended by ...``), and emits VERSION / SUPERSEDES
/ DATE verdicts. The SUPERSEDES check is the #1935 fabricated-supersedes class: a cell that
claims a supersede the register does not record is DRIFT, adjudicated by a human, never by the
tool. ``--check`` exits 1 on any DRIFT / NO-MAP / AMBIGUOUS / ALIAS-BROKEN.

``--write`` is opt-in and correct-by-construction: it rewrites a cell ONLY when the ID resolves
EXACT/ALIAS, the register version is a comparable token, the cell parses under the recognized q2
labelled grammar, and a field actually drifts. It never parses the heterogeneous q4 free-form
cells (their embedded editorial notes would be corrupted); q4 drift is surfaced for manual fix.
Every write is minimal-diff (only the Expected-value column cell's inner text changes; every
other column of the row is byte-identical, guarded by a per-row split-parity check) and is
verified by re-parsing the written file (evidence-grounded apply, not assumed).

Deterministic: no clock, no randomness, no set-iteration-order dependence. Stdlib only.
Advisory in v1 (NOT wired as a blocking gate; a future PR flips it): guarded only by the
regression suite. See the P-1.65 design.

Known limitations (P-1.65; advisory tool , a flagged item is a REVIEW CANDIDATE, not a confirmed defect):
- Compound / 'amended by' register values are reported UNVERIFIABLE for MANUAL review (auto amendment-drift detection produced false positives on incidental dates and cross-references, so it is a routed follow-up, R-a). This is the one deferred class; a compound value is surfaced for a human, never silently OK and never a false DRIFT.
"""
import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTER = ROOT / "governance/register-canonical-citations.md"
# Design D8 named q2+q4; the brief's target is `batch-*.md`. The header-signature parser is
# safe on files with no verification table (0 rows), so the glob generalizes without surprise.
WORKLIST_GLOB = ".project-governance/worklist-citation-verification-batch-*.md"
ALIASES_PATH = ROOT / "tools/citation-worklist-id-aliases.json"

# Embedded known renames (design §1/§5). A sidecar JSON at ALIASES_PATH, if present, overlays
# these. `aliases` and `ambiguous_flag` are kept as SEPARATE maps so an ambiguous id can never
# be silently promoted to an alias.
DEFAULT_ALIASES = {
    "ISO/IEC 27033": "ISO/IEC 27033-1",
    "Canada CPPA": "Canada CPPA / successor C-36 (PPCDA)",
}
DEFAULT_AMBIGUOUS = {
    "BASC International Standard": [
        "BASC International Norm V6-2022 (Control and Security Management System, CSMS)",
        "BASC International Security Standard 6.0.2 (2022, companies with indirect relation to the cargo)",
        "BASC International Security Standard 6.0.3 (2022, companies implementing basic security operational controls)",
    ],
}

FAIL_VERDICTS = {"DRIFT", "NO-MAP", "AMBIGUOUS", "ALIAS-BROKEN"}


# --------------------------------------------------------------------------- shared line helpers
def _read_lines(path):
    return Path(path).read_text(encoding="utf-8").splitlines()


def _cells(ln):
    return [x.strip() for x in ln.strip().strip("|").split("|")]


def _is_sep(ln):
    return bool(re.match(r"^\|[\s:\-|]+\|?\s*$", ln.strip()))


# --------------------------------------------------------------------------- register parser (§3)
@dataclass
class RegRow:
    ver: str
    pub: str
    topic: str
    superseded: list = field(default_factory=list)


def parse_register_lines(lines):
    reg = {}
    for ln in lines:
        if not ln.lstrip().startswith("|") or _is_sep(ln):
            continue
        c = _cells(ln)
        if len(c) != 7 or c[0] in ("Standard ID", ""):
            continue
        sup = [] if c[4] in ("", "-") else [s.strip() for s in c[4].split(",") if s.strip()]
        reg[c[0]] = RegRow(ver=c[1], pub=c[2], topic=c[3], superseded=sup)
    return reg


def parse_register(path):
    return parse_register_lines(_read_lines(path))


# ------------------------------------------------------------ worklist verification parser (§4)
@dataclass
class WLRow:
    sid: str
    expected: str
    line_no: int
    col_idx: int
    ncols: int
    raw: str


def parse_verification_rows_lines(lines):
    rows, in_tbl, id_c, exp_c, ncols = [], False, None, None, 0
    for i, ln in enumerate(lines):
        if not ln.lstrip().startswith("|"):
            in_tbl = False  # a blank/prose line ends the current table
            continue
        if _is_sep(ln):
            continue
        c = _cells(ln)
        if "Standard ID" in c and any("Expected value" in x for x in c):
            in_tbl = True
            ncols = len(c)
            id_c = c.index("Standard ID")
            exp_c = next(k for k, x in enumerate(c) if "Expected value" in x)
            continue
        if in_tbl and len(c) == ncols:
            rows.append(WLRow(sid=c[id_c], expected=c[exp_c], line_no=i,
                              col_idx=exp_c, ncols=ncols, raw=ln))
    return rows


def parse_verification_rows(path):
    return parse_verification_rows_lines(_read_lines(path))


# ----------------------------------------------------------------- id mapping (§5, never guess)
def map_id(sid, reg, aliases, ambiguous):
    if sid in reg:
        return ("EXACT", sid)
    if sid in aliases:
        tgt = aliases[sid]
        return ("ALIAS", tgt) if tgt in reg else ("ALIAS-BROKEN", tgt)
    if sid in ambiguous:
        return ("AMBIGUOUS", None)
    return ("NO-MAP", None)


# ------------------------------------------------------- token-boundary + region helpers (§6/§7)
def _token_present(needle, haystack):
    """True iff `needle` occurs in `haystack` as a whole token (non-alphanumeric or string
    edge on each side), so register 'Rev. 5' does NOT match 'Rev. 50' and supersede
    'Rev. 4' does NOT match claimed 'Rev. 40' (codex P-1.65 finding 2). Case-insensitive;
    internal whitespace in the needle matches flexibly."""
    n = " ".join(needle.strip().lower().split())
    if not n:
        return False
    pat = r"(?<![0-9A-Za-z])" + r"\s+".join(re.escape(tok) for tok in n.split()) + r"(?![0-9A-Za-z])"
    return re.search(pat, haystack.lower()) is not None


def _version_region(cell):
    """The part of the expected-value cell that states the CURRENT version, so a register
    version is matched against the version CLAIM and not incidentally against a
    published-date or supersedes field elsewhere in the cell (codex P-1.65 finding 2,
    cell-wide match)."""
    m = re.match(r"\s*Current:\s*([^;]+)", cell)          # q2 labelled grammar
    if m:
        return m.group(1)
    return re.split(r";|\bpublished\b|\bsupersede[sd]\b", cell, maxsplit=1)[0]  # q4 free-form


# ----------------------------------------------------------- version-value classifier (§6, fix)
_TOKEN_PATTERNS = [
    r"^\d{4}$",                                   # 2022
    r"^Rev\.?\s*\d+$",                            # Rev. 5
    r"^v\d",                                      # v19.2
    r"^\d+\.\d+(\.\d+)?$",                        # 5.0.0
    r"^Regulation\s+\d+/\d+",
    r"^Directive\s+\d+/\d+",
    r"^Edition\s+\d+",
    r"^Part\s+\d+:\d{4}",
]


def classify_version(ver):
    v = ver.strip().strip("()")
    if not v or v.lower() in ("continuous", "series", "-"):
        return "descriptor"
    # An amendment/update marker makes the value compound, so it is NEVER a comparable
    # token however SHORT it is: "v1 amended by v2" and "Regulation 1/2 amended by
    # Regulation 3/4" are both descriptors, not comparable (codex P-1.65 finding 1).
    if re.search(r"\b(?:amended|as\s+updated|as\s+revised)\b", v, re.IGNORECASE):
        return "descriptor"
    if len(v) > 40 or ";" in v or v.count(",") >= 2:  # multi-clause prose
        return "descriptor"
    return "comparable" if any(re.match(p, v) for p in _TOKEN_PATTERNS) else "descriptor"


# ------------------------------------------------------------ supersedes extraction (§7 helper)
def _split_top_level(seg, sep):
    """Split `seg` on `sep` only at PAREN depth 0, so a separator inside parentheses
    ('X (2014-12; per #508)') is part of one value, not a delimiter."""
    parts, depth, cur = [], 0, ""
    for ch in seg:
        if ch == "(":
            depth += 1; cur += ch
        elif ch == ")":
            depth = max(0, depth - 1); cur += ch
        elif ch == sep and depth == 0:
            parts.append(cur); cur = ""
        else:
            cur += ch
    parts.append(cur)
    return parts


def _split_supersede_claims(clause):
    """Split a supersede clause into individual claims at TOP LEVEL (paren depth 0) on
    commas, '&', and the word ' and ', so 'Rev. 4 and Rev. 40' and 'A, B & C' each yield
    DISTINCT claims. Comma-only splitting hid an 'and'-joined fabricated token inside one
    claim (a false negative; the live worklist uses 'supersedes Rev. 2 and Rev. 1'); codex
    P-1.65 finding 6."""
    parts, depth, cur, i = [], 0, "", 0
    low = clause.lower()
    while i < len(clause):
        ch = clause[i]
        if ch == "(":
            depth += 1; cur += ch; i += 1
        elif ch == ")":
            depth = max(0, depth - 1); cur += ch; i += 1
        elif depth == 0 and ch in ",&":
            parts.append(cur); cur = ""; i += 1
        elif depth == 0 and low[i:i + 5] == " and ":
            parts.append(cur); cur = ""; i += 5
        else:
            cur += ch; i += 1
    parts.append(cur)
    return parts


def _claimed_supersedes(cell):
    m = re.search(r"\bsupersede[sd]\b\s+(.*)$", cell)
    if not m or "recorded" in m.group(1):  # skip 'no superseded versions recorded'
        return []
    # Take the supersede clause up to the first TOP-LEVEL ';' (paren-aware, so an internal
    # ';' inside a parenthetical annotation - "supersedes Rev. 1, 2014-12 (per #508;
    # defers ...)" - does NOT truncate the clause; codex P-1.65 R-b).
    clause = _split_top_level(m.group(1), ";")[0]
    clause = re.sub(r"\(per register\)", "", clause)
    out = []
    for raw in _split_supersede_claims(clause):
        x = raw.strip()
        if not x:
            continue
        # A YYYY-MM / YYYY-MM-DD token is a date ANNOTATION on the supersede clause, not a
        # distinct superseded version (codex P-1.65 finding 3 + R-b): "supersedes v19.1,
        # 2026-05" and "Rev. 1, 2014-12 (per #508; ...)" carry a date annotation, dropped.
        # The paren-stripped core is used ONLY for the date test; a KEPT token retains its
        # parenthetical, because there the paren is part of the identifier ("2025 (v2.0)",
        # "Edition 1 (2003)") not an annotation, so stripping it would break the match.
        core = re.sub(r"\s*\([^)]*\)?\s*$", "", x).strip()
        if re.fullmatch(r"\d{4}-\d{2}(?:-\d{2})?", core):
            continue
        out.append(x)
    return out



# ------------------------------------------------------------------ per-row verdicts (§7 check)
def check_row(wl, reg_row, ver_class):
    verdicts = []
    # VERSION
    if ver_class == "descriptor":
        # A compound / "amended by" register value cannot be token-compared safely:
        # auto-extracting amendment identifiers produced false positives on incidental
        # dates/cross-references in the prose (P-1.65 codex iter-2/3, e.g. EN 54's
        # "Regulation 305/2011", PIPEDA's "current to 2026-05-26"), and an amendment
        # year (UK GDPR 2025) is indistinguishable by pattern from an incidental year
        # (PIPEDA 2026). So a compound/amended value is FLAGGED UNVERIFIABLE for MANUAL
        # review (not silently OK, not a false-positive DRIFT). Auto amendment-drift
        # detection is a routed follow-up (pending-decisions 2026-09-02 P-1.65).
        amended = bool(re.search(r"amended\s+by", reg_row.ver, re.IGNORECASE))
        verdicts.append(("VERSION", "UNVERIFIABLE",
                         "compound/amended register value; manual review"
                         if amended else "register version is a descriptor, not a token"))
    else:
        core = reg_row.ver.strip().strip("()")
        # Require the FULL register version as a whole TOKEN within the cell's CURRENT-
        # version region (not a substring, not cell-wide): 'Rev. 5' must not accept
        # 'Rev. 50', and a register version appearing only in a published-date/supersedes
        # field is not a match for a drifted current claim (codex P-1.65 finding 2). A cell
        # that phrases the version differently is flagged DRIFT for review (conservative).
        ok = bool(core) and _token_present(core, _version_region(wl.expected))
        verdicts.append(("VERSION", "OK" if ok else "DRIFT",
                         "" if ok else f"register '{reg_row.ver}' absent from cell"))
    # SUPERSEDES (the #1935 fabricated-supersedes class)
    for cs in _claimed_supersedes(wl.expected):
        # "in register" iff a RECORDED register supersede value appears within the
        # cell's claimed value (one-directional): suppresses annotation/prefix noise
        # ("the parts ..." vs "parts ...", "v2026.06 (2026-06)" vs "v2026.06") while
        # still catching a fabricated supersede (register empty, or the recorded value
        # absent) and NOT reintroducing the Rev.9-vs-Rev.4 bug (register 'Rev. 4' is not
        # within cell 'Rev. 9'). P-1.65 codex iter-1/3.
        present = any(_token_present(s, cs) for s in reg_row.superseded)
        if not present:
            verdicts.append(("SUPERSEDES", "DRIFT",
                             f"cell claims supersede '{cs}' not in register {reg_row.superseded}"))
    # DATE (only when register pub is a clean YYYY / YYYY-MM and the cell omits it)
    if re.match(r"^\d{4}(-\d\d)?$", reg_row.pub) and reg_row.pub not in wl.expected:
        verdicts.append(("DATE", "INFO",
                         f"register publication '{reg_row.pub}' not echoed in cell"))
    return verdicts


# ------------------------------------------------------------- q2-grammar rewriter (§8, bounded)
_Q2 = re.compile(
    r"^Current:\s*(?P<ver>[^;]+);"
    r"(?:\s*published\s*(?P<pub>[^;]+);)?"
    r"\s*topic:\s*(?P<topic>[^;]+)"
    r"(?:;\s*(?:supersede[sd]\s*(?P<sup>.+?)|no superseded versions recorded))?\s*$"
)


def render_q2(reg_row, parsed_topic):
    sup = (f"supersedes {', '.join(reg_row.superseded)}"
           if reg_row.superseded else "no superseded versions recorded")
    return f"Current: {reg_row.ver}; published {reg_row.pub}; topic: {parsed_topic}; {sup}"


def render_cell(wl, reg_row, ver_class):
    """Return (new_cell, reason) for a WRITE, or (None, reason-not-written).

    Bounded exactly as the design specifies: q2 labelled grammar only, comparable register
    version only, and only when a field actually drifts. Everything else returns None so the
    caller leaves the cell untouched and surfaces it for manual review.
    """
    if ver_class != "comparable":
        return (None, "register version is a descriptor, not a comparable token")
    m = _Q2.match(wl.expected)
    if not m:
        return (None, "cell is not recognized q2 grammar (q4 free-form is manual-fix only)")
    drifts = [v for (f_, v, _d) in check_row(wl, reg_row, ver_class) if v == "DRIFT"]
    if not drifts:
        return (None, "no drift")
    return (render_q2(reg_row, m.group("topic").strip()), "rewritten from register")


# ------------------------------------------------------------------------- config loading (§5)
def load_alias_config():
    aliases = dict(DEFAULT_ALIASES)
    ambiguous = {k: list(v) for k, v in DEFAULT_AMBIGUOUS.items()}
    if ALIASES_PATH.exists():
        conf = json.loads(ALIASES_PATH.read_text(encoding="utf-8"))
        aliases.update(conf.get("aliases", {}))
        for k, v in conf.get("ambiguous_flag", {}).items():
            ambiguous[k] = list(v)
    return aliases, ambiguous


def default_worklists():
    return sorted(ROOT.glob(WORKLIST_GLOB))


# ---------------------------------------------------------------------------- --check (default)
@dataclass
class Finding:
    worklist: str
    sid: str
    field: str
    verdict: str
    detail: str


def evaluate_rows(name, rows, reg, aliases, ambiguous):
    """Pure decision half: return (findings, ok_count) for one worklist's rows."""
    findings, ok = [], 0
    for row in rows:
        kind, tgt = map_id(row.sid, reg, aliases, ambiguous)
        if kind in ("NO-MAP", "AMBIGUOUS", "ALIAS-BROKEN"):
            detail = {
                "NO-MAP": "no register match; add an alias or fix the worklist id",
                "AMBIGUOUS": "multiple register candidates; adjudicate, do NOT auto-map",
                "ALIAS-BROKEN": f"alias target '{tgt}' no longer in register",
            }[kind]
            findings.append(Finding(name, row.sid, "MAP", kind, detail))
            continue
        ver_class = classify_version(reg[tgt].ver)
        for fld, verdict, detail in check_row(row, reg[tgt], ver_class):
            if verdict == "OK":
                ok += 1
            else:
                findings.append(Finding(name, row.sid, fld, verdict, detail))
    return findings, ok


def check_paths(register, worklists, aliases, ambiguous, strict=False):
    """Thin I/O shell over evaluate_rows: print verdicts, return exit code."""
    reg = register if isinstance(register, dict) else parse_register(register)
    failed = False
    for wl_path in worklists:
        rows = parse_verification_rows(wl_path)
        findings, ok = evaluate_rows(Path(wl_path).name, rows, reg, aliases, ambiguous)
        for f in findings:
            print(f"{f.worklist}: {f.verdict} [{f.sid}] {f.field}: {f.detail}")
            if f.verdict in FAIL_VERDICTS or (strict and f.verdict == "UNVERIFIABLE"):
                failed = True
        print(f"{Path(wl_path).name}: {len(rows)} verification rows; {ok} field-OK; "
              f"{len(findings)} flagged")
    return 1 if failed else 0


# ------------------------------------------------------------------------------- --write (§8)
def _splice_expected(raw, col_idx, new_cell):
    """Replace only the expected column's inner text in `raw`, preserving every other cell
    byte-for-byte. Returns (new_line, ok): ok is False if the split-parity guard trips."""
    parts = raw.split("|")                       # leading '' from the initial pipe
    target = col_idx + 1
    if target >= len(parts):
        return (raw, False)
    rebuilt = list(parts)
    rebuilt[target] = f" {new_cell} "
    new_line = "|".join(rebuilt)
    check = new_line.split("|")
    if len(check) != len(parts) or any(check[k] != parts[k] for k in range(len(parts)) if k != target):
        return (raw, False)                      # scope guard: nothing but the exp cell moved
    return (new_line, True)


def write_worklists(register, worklists, aliases, ambiguous, normalize=False):
    reg = register if isinstance(register, dict) else parse_register(register)
    total_written, manual = 0, []
    for wl_path in worklists:
        wl_path = Path(wl_path)
        lines = _read_lines(wl_path)
        rows = parse_verification_rows_lines(lines)
        changed = False
        for row in rows:
            kind, tgt = map_id(row.sid, reg, aliases, ambiguous)
            if kind not in ("EXACT", "ALIAS"):
                if kind in FAIL_VERDICTS:
                    manual.append(f"{wl_path.name}: {kind} [{row.sid}] (needs adjudication)")
                continue
            ver_class = classify_version(reg[tgt].ver)
            new_cell, reason = render_cell(row, reg[tgt], ver_class)
            if new_cell is None:
                if any(v == "DRIFT" for (_f, v, _d) in check_row(row, reg[tgt], ver_class)):
                    manual.append(f"{wl_path.name}: manual-fix [{row.sid}] ({reason})")
                continue
            new_line, ok = _splice_expected(lines[row.line_no], row.col_idx, new_cell)
            if not ok:
                manual.append(f"{wl_path.name}: SKIPPED [{row.sid}] (scope guard tripped)")
                continue
            lines[row.line_no] = new_line
            changed = True
            total_written += 1
            print(f"{wl_path.name}: wrote [{row.sid}] -> {new_cell}")
        if changed:
            wl_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            # Evidence-grounded apply: re-parse and assert no written row still shows VERSION drift.
            reparsed = parse_verification_rows_lines(_read_lines(wl_path))
            residual, _ok = evaluate_rows(wl_path.name, reparsed, reg, aliases, ambiguous)
            for f in residual:
                if f.field == "VERSION" and f.verdict == "DRIFT" and map_id(
                        f.sid, reg, aliases, ambiguous)[0] in ("EXACT", "ALIAS") and _Q2.match(
                        next((r.expected for r in reparsed if r.sid == f.sid), "")):
                    raise AssertionError(
                        f"post-write verification failed: {f.sid} still drifts after rewrite")
    print(f"--write: {total_written} q2 cell(s) rewritten")
    if manual:
        print("--write: the following drift is NOT auto-applied (manual adjudication):")
        for m in manual:
            print(f"  {m}")
    # Truthful exit signal: reflect any residual drift the bounded write could not resolve.
    return check_paths(reg, worklists, aliases, ambiguous)


# ------------------------------------------------------------------------------- self-test (§9)
def _self_test():
    import unittest

    ALIASES = {"ISO/IEC 27033": "ISO/IEC 27033-1", "X Broken": "X Nonexistent"}
    AMBIG = {"BASC International Standard": ["cand a", "cand b", "cand c"]}
    REG_LINES = [
        "| Standard ID | Current version | Publication date | Topic | Superseded versions | Upstream check location | Last verified (UTC) |",
        "| --- | --- | --- | --- | --- | --- | --- |",
        "| ISO/IEC 27033-1 | 2015 | 2015 | Network security | 2013 | http://x | verified 2026-01-01 |",
        "| EU eIDAS | Regulation 910/2014 as amended by Regulation 2024/1183 (eIDAS 2) | 2024-04 (amend) | Trust services | - | http://x | verified 2026-01-01 |",
        "| CSA STAR | continuous | 2026-01 | Cloud registry | - | http://x | verified 2026-01-01 |",
        "| ISO/IEC 27001 | 2022 | 2022-10 | ISMS | 2013 | http://x | verified 2026-01-01 |",
    ]
    # A worklist mixing verification tables with the metadata/cluster noise the parser must skip.
    WL_LINES = [
        "| Batch identifier | q-test |",
        "| Batch opened | 2026-01-01 |",
        "",
        "| Standard ID | Publisher | Expected primary URL | Field(s) to verify | Expected value (from register) | Notes |",
        "| --- | --- | --- | --- | --- | --- |",
        "| ISO/IEC 27033 | ISO | `u` | all | Current: 2020; topic: Network security; no superseded versions recorded |  |",
        "| EU eIDAS | ISO | `u` | all | Regulation 2024/1183; supersedes Regulation 910/2014 (eIDAS 1) |  |",
        "| CSA STAR | ISO | `u` | all | continuous registry snapshot |  |",
        "| ISO/IEC 27001 | ISO | `u` | all | Current: 2022; published 2022-10; topic: ISMS; supersedes 2013 |  |",
        "",
        "| 3.1 NIST | 4 |",
        "| **Total** | 4 |",
    ]

    class T(unittest.TestCase):
        def setUp(self):
            self.reg = parse_register_lines(REG_LINES)
            self.rows = parse_verification_rows_lines(WL_LINES)

        def test_register_parse(self):
            self.assertIn("ISO/IEC 27033-1", self.reg)
            self.assertEqual(self.reg["ISO/IEC 27033-1"].ver, "2015")
            self.assertEqual(self.reg["ISO/IEC 27001"].superseded, ["2013"])
            self.assertEqual(self.reg["CSA STAR"].superseded, [])

        def test_header_signature_excludes_metadata_and_cluster_rows(self):
            # 4 verification rows only; the 4 metadata/cluster pseudo-rows are excluded.
            self.assertEqual(len(self.rows), 4)
            self.assertEqual([r.sid for r in self.rows],
                             ["ISO/IEC 27033", "EU eIDAS", "CSA STAR", "ISO/IEC 27001"])

        def test_map_id_exact_alias_ambiguous_nomap_broken(self):
            self.assertEqual(map_id("ISO/IEC 27001", self.reg, ALIASES, AMBIG), ("EXACT", "ISO/IEC 27001"))
            self.assertEqual(map_id("ISO/IEC 27033", self.reg, ALIASES, AMBIG), ("ALIAS", "ISO/IEC 27033-1"))
            self.assertEqual(map_id("BASC International Standard", self.reg, ALIASES, AMBIG), ("AMBIGUOUS", None))
            self.assertEqual(map_id("Totally Unknown", self.reg, ALIASES, AMBIG), ("NO-MAP", None))
            self.assertEqual(map_id("X Broken", self.reg, ALIASES, AMBIG), ("ALIAS-BROKEN", "X Nonexistent"))

        def test_classify_version_token_vs_descriptor(self):
            for tok in ("2015", "Rev. 5", "5.0.0", "v19.2", "Regulation 2024/1183"):
                self.assertEqual(classify_version(tok), "comparable", tok)
            for desc in ("continuous", "series (CEN/TC 72)", "1988, as amended by X, Y",
                         "Regulation 910/2014 as amended by Regulation 2024/1183 (eIDAS 2)", "-", ""):
                self.assertEqual(classify_version(desc), "descriptor", desc)

        def test_claimed_supersedes_skips_negation_and_strips_marker(self):
            self.assertEqual(_claimed_supersedes("no superseded versions recorded"), [])
            self.assertEqual(_claimed_supersedes("Current: 2022; supersedes 2013"), ["2013"])
            self.assertEqual(_claimed_supersedes("supersedes 2013 (per register)"), ["2013"])
            self.assertEqual(_claimed_supersedes("supersedes A, B"), ["A", "B"])

        def test_version_drift_true_positive(self):
            row = next(r for r in self.rows if r.sid == "ISO/IEC 27033")
            v = check_row(row, self.reg["ISO/IEC 27033-1"], "comparable")
            self.assertIn(("VERSION", "DRIFT", "register '2015' absent from cell"), v)

        def test_descriptor_version_suppresses_false_positive(self):
            row = next(r for r in self.rows if r.sid == "CSA STAR")
            v = check_row(row, self.reg["CSA STAR"], classify_version(self.reg["CSA STAR"].ver))
            self.assertTrue(any(f == "VERSION" and verd == "UNVERIFIABLE" for (f, verd, _d) in v))
            self.assertFalse(any(verd == "DRIFT" for (_f, verd, _d) in v))

        def test_supersedes_fabrication_catch_eidas(self):
            row = next(r for r in self.rows if r.sid == "EU eIDAS")
            v = check_row(row, self.reg["EU eIDAS"], classify_version(self.reg["EU eIDAS"].ver))
            self.assertTrue(any(f == "SUPERSEDES" and verd == "DRIFT" for (f, verd, _d) in v))

        def test_version_partial_token_rejected(self):
            # Soundness (codex #2): a first-token prefix must NOT accept a wrong revision.
            wl = WLRow(sid="X", expected="Current: Rev. 4", line_no=0, col_idx=0, ncols=0, raw="")
            reg = RegRow(ver="Rev. 5", pub="2024", topic="t")
            v = check_row(wl, reg, "comparable")
            self.assertTrue(any(f == "VERSION" and verd == "DRIFT" for (f, verd, _d) in v))

        def test_supersedes_dotted_fabrication_not_substring_matched(self):
            # Soundness (codex #3): 'Rev. 9' must not match register 'Rev. 4' via substring.
            wl = WLRow(sid="X", expected="supersedes Rev. 9", line_no=0, col_idx=0, ncols=0, raw="")
            reg = RegRow(ver="Rev. 5", pub="2024", topic="t", superseded=["Rev. 4"])
            v = check_row(wl, reg, "comparable")
            self.assertTrue(any(f == "SUPERSEDES" and verd == "DRIFT" for (f, verd, _d) in v))

        def test_descriptor_incidental_number_not_flagged(self):
            # Soundness (codex re-verify): an incidental number in descriptor prose (not in
            # an 'amended by' clause, e.g. EN 54's cross-ref to Regulation 305/2011) must NOT
            # produce false VERSION DRIFT; it stays UNVERIFIABLE.
            wl = WLRow(sid="X", expected="parts 2017 to 2023, fire detection", line_no=0, col_idx=0, ncols=0, raw="")
            reg = RegRow(ver="series (25+ parts; refers to Regulation 305/2011 CPR)", pub="various", topic="t")
            v = check_row(wl, reg, classify_version(reg.ver))
            self.assertFalse(any(verd == "DRIFT" for (_f, verd, _d) in v))
            self.assertTrue(any(f == "VERSION" and verd == "UNVERIFIABLE" for (f, verd, _d) in v))

        def test_amended_value_flagged_unverifiable_not_drift(self):
            # P-1.65 codex iter-2/3: a compound/"amended by" register value is FLAGGED
            # UNVERIFIABLE for manual review (auto amendment-drift detection is a routed
            # follow-up), never a false-positive DRIFT and never silently OK.
            wl = WLRow(sid="X", expected="Regulation 2024/1689", line_no=0, col_idx=0, ncols=0, raw="")
            reg = RegRow(ver="Regulation 2024/1689 as amended by Regulation (EU) 2026/1744 (Digital Omnibus)",
                         pub="2024", topic="t")
            v = check_row(wl, reg, classify_version(reg.ver))
            self.assertFalse(any(verd == "DRIFT" for (_f, verd, _d) in v))
            self.assertTrue(any(f == "VERSION" and verd == "UNVERIFIABLE"
                                and "manual review" in d for (f, verd, d) in v))

        def test_short_amended_value_is_descriptor(self):
            # codex P-1.65 finding 1: a SHORT compound/amendment value must classify
            # descriptor (not comparable via a leading token), so it goes UNVERIFIABLE.
            self.assertEqual(classify_version("v1 amended by v2"), "descriptor")
            self.assertEqual(classify_version("Regulation 1/2 amended by Regulation 3/4"), "descriptor")
            self.assertEqual(classify_version("2019 as updated 2024"), "descriptor")

        def test_version_token_boundary_rejects_superstring(self):
            # codex P-1.65 finding 2: register 'Rev. 5' must NOT match cell 'Rev. 50'.
            wl = WLRow(sid="X", expected="Current: Rev. 50", line_no=0, col_idx=0, ncols=0, raw="")
            reg = RegRow(ver="Rev. 5", pub="2024", topic="t")
            v = check_row(wl, reg, "comparable")
            self.assertTrue(any(f == "VERSION" and verd == "DRIFT" for (f, verd, _d) in v))

        def test_supersedes_token_boundary_rejects_superstring(self):
            # codex P-1.65 finding 2: register supersede 'Rev. 4' must NOT accept 'Rev. 40'.
            wl = WLRow(sid="X", expected="supersedes Rev. 40", line_no=0, col_idx=0, ncols=0, raw="")
            reg = RegRow(ver="Rev. 5", pub="2024", topic="t", superseded=["Rev. 4"])
            v = check_row(wl, reg, "comparable")
            self.assertTrue(any(f == "SUPERSEDES" and verd == "DRIFT" for (f, verd, _d) in v))

        def test_version_region_scoped_not_cell_wide(self):
            # codex P-1.65 finding 2 (cell-wide): register '2015' appearing only in the
            # published field must NOT satisfy a drifted current claim of 2020.
            wl = WLRow(sid="X", expected="Current: 2020; published 2015; topic: t",
                       line_no=0, col_idx=0, ncols=0, raw="")
            reg = RegRow(ver="2015", pub="2015", topic="t")
            v = check_row(wl, reg, "comparable")
            self.assertTrue(any(f == "VERSION" and verd == "DRIFT" for (f, verd, _d) in v))

        def test_supersede_date_annotation_not_a_claim(self):
            # codex P-1.65 finding 3: a YYYY-MM date annotation on a supersede clause is
            # not a distinct supersede claim, so it is not flagged; a bare YYYY is kept.
            self.assertEqual(_claimed_supersedes("supersedes v19.1, 2026-05"), ["v19.1"])
            self.assertEqual(_claimed_supersedes("supersedes 2019"), ["2019"])
            wl = WLRow(sid="X", expected="v19.2, 2026-05; supersedes v19.1, 2026-05",
                       line_no=0, col_idx=0, ncols=0, raw="")
            reg = RegRow(ver="v19.2", pub="2026-05", topic="t", superseded=["v19.1"])
            v = check_row(wl, reg, "comparable")
            self.assertFalse(any(f == "SUPERSEDES" and verd == "DRIFT" for (f, verd, _d) in v))

        def test_supersede_internal_semicolon_in_parens_not_truncated(self):
            # codex P-1.65 R-b: an internal ';' inside a parenthetical annotation must NOT
            # truncate the clause or yield a spurious flag; the date-annotation core is
            # dropped and the real superseded version ('Rev. 1') matches the register.
            self.assertEqual(
                _claimed_supersedes("supersedes Rev. 1, 2014-12 (per #508; defers to IEEE 2883:2022)"),
                ["Rev. 1"])
            # a semantic parenthetical (part of the identifier) is retained, not stripped:
            self.assertEqual(_claimed_supersedes("supersedes 2025 (v2.0)"), ["2025 (v2.0)"])
            wl = WLRow(sid="X",
                       expected="Rev. 2, 2025-09; supersedes Rev. 1, 2014-12 (per #508; defers to IEEE 2883:2022)",
                       line_no=0, col_idx=0, ncols=0, raw="")
            reg = RegRow(ver="Rev. 2", pub="2025-09", topic="t", superseded=["Rev. 1"])
            v = check_row(wl, reg, "comparable")
            self.assertFalse(any(f == "SUPERSEDES" and verd == "DRIFT" for (f, verd, _d) in v))

        def test_supersedes_and_ampersand_split_finds_fabrication(self):
            # codex P-1.65 finding 6: an 'and'/'&'-joined claim must split so a fabricated
            # token is not hidden inside one comma-claim. Register supersedes ['Rev. 4']; a
            # claim 'Rev. 4 and Rev. 40' must still flag 'Rev. 40' as fabricated.
            self.assertEqual(_claimed_supersedes("supersedes Rev. 4 and Rev. 40"),
                             ["Rev. 4", "Rev. 40"])
            self.assertEqual(_claimed_supersedes("supersedes A & B"), ["A", "B"])
            wl = WLRow(sid="X", expected="supersedes Rev. 4 and Rev. 40",
                       line_no=0, col_idx=0, ncols=0, raw="")
            reg = RegRow(ver="Rev. 5", pub="2024", topic="t", superseded=["Rev. 4"])
            v = check_row(wl, reg, "comparable")
            self.assertTrue(any(f == "SUPERSEDES" and verd == "DRIFT"
                                and "Rev. 40" in d for (f, verd, d) in v))
            # a legitimate 'A and B' both recorded -> no drift
            wl2 = WLRow(sid="X", expected="supersedes Rev. 2 and Rev. 1",
                        line_no=0, col_idx=0, ncols=0, raw="")
            reg2 = RegRow(ver="Rev. 3", pub="2024", topic="t", superseded=["Rev. 2", "Rev. 1"])
            v2 = check_row(wl2, reg2, "comparable")
            self.assertFalse(any(f == "SUPERSEDES" and verd == "DRIFT" for (f, verd, _d) in v2))

        def test_render_q2_preserves_topic_and_canonicalizes(self):
            out = render_q2(self.reg["ISO/IEC 27001"], "ISMS")
            self.assertEqual(out, "Current: 2022; published 2022-10; topic: ISMS; supersedes 2013")

        def test_render_cell_only_writes_q2_comparable_drift(self):
            r27033 = next(r for r in self.rows if r.sid == "ISO/IEC 27033")
            new, _why = render_cell(r27033, self.reg["ISO/IEC 27033-1"], "comparable")
            self.assertEqual(new, "Current: 2015; published 2015; topic: Network security; supersedes 2013")
            rcsa = next(r for r in self.rows if r.sid == "CSA STAR")
            none_descriptor, _ = render_cell(rcsa, self.reg["CSA STAR"],
                                             classify_version(self.reg["CSA STAR"].ver))
            self.assertIsNone(none_descriptor)  # descriptor register value -> never rewritten
            r1 = next(r for r in self.rows if r.sid == "ISO/IEC 27001")
            none_nodrift, _ = render_cell(r1, self.reg["ISO/IEC 27001"], "comparable")
            self.assertIsNone(none_nodrift)     # no drift -> untouched

        def test_splice_scope_guard_touches_only_expected_cell(self):
            row = next(r for r in self.rows if r.sid == "ISO/IEC 27033")
            new_line, ok = _splice_expected(row.raw, row.col_idx, "REPLACED")
            self.assertTrue(ok)
            before, after = row.raw.split("|"), new_line.split("|")
            self.assertEqual(len(before), len(after))
            for k in range(len(before)):
                if k != row.col_idx + 1:
                    self.assertEqual(before[k], after[k])
            self.assertEqual(after[row.col_idx + 1].strip(), "REPLACED")

        def test_evaluate_and_exit_code(self):
            findings, ok = evaluate_rows("wl", self.rows, self.reg, ALIASES, AMBIG)
            verds = {(f.sid, f.field): f.verdict for f in findings}
            self.assertEqual(verds.get(("ISO/IEC 27033", "VERSION")), "DRIFT")
            self.assertEqual(verds.get(("EU eIDAS", "SUPERSEDES")), "DRIFT")
            self.assertEqual(verds.get(("CSA STAR", "VERSION")), "UNVERIFIABLE")
            self.assertTrue(any(f.verdict in FAIL_VERDICTS for f in findings))

    suite = unittest.TestLoader().loadTestsFromTestCase(T)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    return 0 if result.wasSuccessful() else 1


# ------------------------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description="Detect/rewrite worklist-vs-register citation drift (P-1.65).")
    ap.add_argument("--register", type=Path, default=DEFAULT_REGISTER,
                    help="canonical citations register (default: governance/register-canonical-citations.md)")
    ap.add_argument("--worklist", type=Path, action="append", dest="worklists",
                    help="worklist path (repeatable; default: all batch-* verification worklists)")
    ap.add_argument("--check", action="store_true", help="detect drift (default mode); exits 1 on any flag")
    ap.add_argument("--write", action="store_true", help="conservatively rewrite recognized q2-grammar cells")
    ap.add_argument("--normalize", action="store_true", help="(reserved) also canonicalize non-drifting q2 phrasing")
    ap.add_argument("--strict", action="store_true", help="promote UNVERIFIABLE to a failing verdict")
    ap.add_argument("--self-test", action="store_true", help="run the inline unit suite and exit")
    a = ap.parse_args(argv)

    if a.self_test:
        return _self_test()

    aliases, ambiguous = load_alias_config()
    reg = parse_register(a.register)
    worklists = a.worklists if a.worklists else default_worklists()

    if a.write:
        return write_worklists(reg, worklists, aliases, ambiguous, normalize=a.normalize)
    return check_paths(reg, worklists, aliases, ambiguous, strict=a.strict)


if __name__ == "__main__":
    sys.exit(main())
